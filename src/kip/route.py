"""Pass 2 — contextual enrichment, hybrid routing, clustering.

Spec §10. Routes units into comparison sets WITHOUT deciding whether they agree.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from typing import Any, Callable, Iterable

from .artifacts import RunContext, envelope, seal, write_jsonl_atomic
from .config import Config
from .llm import LLMClient

ENRICH_PROMPT_VERSION = "pass-02a-contextual-enrichment-v3.0"
CLUSTER_PROMPT_VERSION = "pass-02b-cluster-labeling-v3.0"

ENRICH_SYSTEM = """You write a short retrieval context for a knowledge unit.

Given a unit and its source document's title and summary, write 1-2 sentences
situating the unit: what document it came from, what subject area it belongs to,
and what entities or study it concerns.

This text is used ONLY to improve retrieval. It is never shown as evidence and
never replaces the unit's own statement. Do not add facts that are not already
implied by the unit and its source metadata. Do not speculate."""

ENRICH_SCHEMA = {
    "type": "object",
    "properties": {
        "context": {"type": "string"},
        "entities": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["context", "entities"],
    "additionalProperties": False,
}

LABEL_SYSTEM = """You label a cluster of related knowledge units with a topic.

Give a short human-readable topic label and a one-sentence routing reason
explaining what comparison question these units share.

You are NOT deciding whether the units agree, contradict, or qualify each other.
That judgment happens later. Label the comparison set only."""

LABEL_SCHEMA = {
    "type": "object",
    "properties": {
        "topic_label": {"type": "string"},
        "routing_reason": {"type": "string"},
        "related_existing_topics": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["topic_label", "routing_reason"],
    "additionalProperties": False,
}

_TOKEN = re.compile(r"[a-z0-9][a-z0-9\-']*")
_STOP = {
    "the", "a", "an", "and", "or", "of", "to", "in", "for", "on", "at", "by",
    "with", "is", "are", "was", "were", "be", "been", "that", "this", "it",
    "as", "from", "not", "no", "but", "than", "then", "when", "which", "we",
}


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]


# --- Lexical similarity (BM25) ------------------------------------------------
# Spec §10.3 mandates hybrid dense+sparse retrieval: embeddings miss exact-match
# strings (identifiers like "TS-999") that BM25 catches. BM25 is implemented
# inline so the default install needs no extra dependency; the dense half is
# pluggable via `embedder` because Anthropic exposes no embeddings endpoint --
# supply Voyage/OpenAI/local vectors to complete the hybrid.


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = docs
        self.n = len(docs)
        self.freqs = [Counter(d) for d in docs]
        self.lengths = [len(d) for d in docs]
        self.avg_len = (sum(self.lengths) / self.n) if self.n else 0.0
        df: Counter[str] = Counter()
        for doc in docs:
            df.update(set(doc))
        self.idf = {
            term: math.log(1 + (self.n - count + 0.5) / (count + 0.5))
            for term, count in df.items()
        }

    def score(self, query: list[str], index: int) -> float:
        freq = self.freqs[index]
        length = self.lengths[index] or 1
        total = 0.0
        for term in query:
            if term not in freq:
                continue
            tf = freq[term]
            denom = tf + self.k1 * (1 - self.b + self.b * length / (self.avg_len or 1))
            total += self.idf.get(term, 0.0) * tf * (self.k1 + 1) / denom
        return total


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


# --- Pass entry point ---------------------------------------------------------


def route_and_cluster(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    units: list[dict[str, Any]],
    embedder: Callable[[list[str]], list[list[float]]] | None = None,
) -> list[dict[str, Any]]:
    kept = [u for u in units if u.get("decision") != "drop"]
    if not kept:
        write_jsonl_atomic(ctx.enriched_units, [])
        return []

    enriched = _enrich(ctx, cfg, client, kept)
    write_jsonl_atomic(ctx.enriched_units, enriched)

    sim = _similarity_matrix(enriched, embedder)
    groups = _cluster(sim, len(enriched), cfg)
    return _label_clusters(ctx, cfg, client, enriched, groups)


def _enrich(
    ctx: RunContext, cfg: Config, client: LLMClient, units: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Prepend generated context to each unit before indexing (spec §10.2).

    This is the one evidence-backed technique v2.0 lacked entirely. Anthropic
    measured a 49% reduction in top-20 retrieval failures from contextual
    enrichment; independent replications report a smaller 5-15% gain. The
    enrichment is an INDEX-TIME artifact only -- it must never leak into the
    unit's own statement or its evidence.
    """
    out: list[dict[str, Any]] = []
    for unit in units:
        try:
            result = client.complete_json(
                system=ENRICH_SYSTEM,
                user=(
                    f"Source: {unit['source_id']} (family {unit['source_family_id']})\n"
                    f"Statement: {unit['canonical_statement']}\n"
                    f"Topics: {', '.join(unit.get('candidate_topics', [])) or 'none'}\n\n"
                    "Write the retrieval context."
                ),
                schema=ENRICH_SCHEMA,
                model=cfg.model_for("enricher"),
                add_thinking=False,  # too small a task to pay for a reasoning field
            )
            context = result.get("context", "")
            entities = result.get("entities", [])
        except Exception as exc:  # enrichment is an optimization, never a gate
            context, entities = "", []
            print(f"[pass2] enrichment failed for {unit['unit_id']}: {exc}")

        out.append(
            seal(
                {
                    **envelope(
                        ctx,
                        prompt_version=ENRICH_PROMPT_VERSION,
                        model_role="contextual-enricher",
                        parent_artifacts=["02_units/units.jsonl"],
                    ),
                    "unit_id": unit["unit_id"],
                    "source_id": unit["source_id"],
                    "source_family_id": unit["source_family_id"],
                    "independence_group": unit["independence_group"],
                    "canonical_statement": unit["canonical_statement"],
                    "candidate_topics": unit.get("candidate_topics", []),
                    "enrichment_context": context,
                    "entities": entities,
                    # Extraction-time mentions, carried through verbatim.
                    # `entities` above is the enricher's own loose list, used
                    # only for routing affinity and then dropped; the wiki's
                    # entity resolution needs the raw surface forms and their
                    # line numbers, and re-asking a model for what Pass 1
                    # already reported would pay twice for the same answer.
                    "entity_mentions": unit.get("entity_mentions", []),
                    "index_text": f"{context} {unit['canonical_statement']}".strip(),
                }
            )
        )
    return out


def _similarity_matrix(
    enriched: list[dict[str, Any]],
    embedder: Callable[[list[str]], list[list[float]]] | None,
) -> list[list[float]]:
    texts = [u["index_text"] for u in enriched]
    docs = [tokenize(t) for t in texts]
    bm25 = BM25(docs)

    vectors: list[list[float]] | None = None
    if embedder is not None:
        try:
            vectors = embedder(texts)
        except Exception as exc:
            print(f"[pass2] embedder failed, continuing lexical-only: {exc}")

    n = len(enriched)
    raw = [[0.0] * n for _ in range(n)]
    best = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            lexical = bm25.score(docs[i], j) + bm25.score(docs[j], i)
            raw[i][j] = raw[j][i] = lexical
            best = max(best, lexical)

    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            # Normalized lexical score is the sparse half of the hybrid.
            score = (raw[i][j] / best) if best else 0.0
            if vectors is not None:
                # Fusion weight is deliberately a knob, not a constant: BM25
                # fusion helps small embedders but has been measured to REDUCE
                # effectiveness with a top-tier embedder (spec §10.3).
                score = 0.5 * score + 0.5 * max(0.0, _cosine(vectors[i], vectors[j]))
            score += _metadata_affinity(enriched[i], enriched[j])
            matrix[i][j] = matrix[j][i] = score
    return matrix


def _metadata_affinity(a: dict[str, Any], b: dict[str, Any]) -> float:
    """Non-lexical routing signals (spec §10.3): topics, entities, lineage."""
    bonus = 0.0
    topics_a, topics_b = set(a.get("candidate_topics", [])), set(b.get("candidate_topics", []))
    if topics_a & topics_b:
        bonus += 0.25 * len(topics_a & topics_b) / max(1, len(topics_a | topics_b))
    ents_a = {e.lower() for e in a.get("entities", [])}
    ents_b = {e.lower() for e in b.get("entities", [])}
    if ents_a & ents_b:
        bonus += 0.25 * len(ents_a & ents_b) / max(1, len(ents_a | ents_b))
    # Same underlying study/pilot: likely the same comparison set. This does NOT
    # imply agreement -- and Pass 3 uses the same field to refuse to count them
    # as independent confirmation.
    if a["independence_group"] == b["independence_group"]:
        bonus += 0.1
    return bonus


def _cluster(sim: list[list[float]], n: int, cfg: Config) -> list[list[int]]:
    """Greedy agglomerative clustering with spec-mandated size caps.

    Spec §10.4: prefer coherent clusters of ~20-50 units; split above ~75;
    preserve singletons -- unrelated content is not a failure. Flat clustering
    is deliberate: eager LLM graph construction costs ~1000x more at indexing
    for a measured +0.47 average gain on general QA (vs +27.23 on multi-hop).
    """
    threshold = 0.22
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edges = sorted(
        ((sim[i][j], i, j) for i in range(n) for j in range(i + 1, n) if sim[i][j] >= threshold),
        reverse=True,
    )
    sizes = [1] * n
    for score, i, j in edges:
        ri, rj = find(i), find(j)
        if ri == rj:
            continue
        if sizes[ri] + sizes[rj] > cfg.batch.hard_split_above:
            continue  # never merge past the hard split point
        parent[ri] = rj
        sizes[rj] += sizes[ri]

    groups: dict[int, list[int]] = defaultdict(list)
    for index in range(n):
        groups[find(index)].append(index)

    out: list[list[int]] = []
    for members in groups.values():
        if len(members) <= cfg.batch.hard_split_above:
            out.append(sorted(members))
        else:  # defensive: chunk anything that slipped past the size guard
            members = sorted(members)
            step = cfg.batch.target_size
            out.extend(members[i : i + step] for i in range(0, len(members), step))
    return sorted(out, key=lambda g: (-len(g), g[0]))


def _label_clusters(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    enriched: list[dict[str, Any]],
    groups: list[list[int]],
) -> list[dict[str, Any]]:
    clusters: list[dict[str, Any]] = []
    for index, members in enumerate(groups, start=1):
        units = [enriched[m] for m in members]
        listing = "\n".join(
            f"- {u['canonical_statement']}" for u in units[:60]
        )
        try:
            labelled = client.complete_json(
                system=LABEL_SYSTEM,
                user=f"Units in this cluster:\n{listing}\n\nLabel the comparison set.",
                schema=LABEL_SCHEMA,
                model=cfg.model_for("enricher"),
                add_thinking=False,
            )
        except Exception as exc:
            print(f"[pass2] labeling failed for cluster {index}: {exc}")
            labelled = {
                "topic_label": f"cluster-{index}",
                "routing_reason": "automatic grouping; labeling unavailable",
            }

        clusters.append(
            seal(
                {
                    **envelope(
                        ctx,
                        prompt_version=CLUSTER_PROMPT_VERSION,
                        model_role="semantic-router",
                        parent_artifacts=["03_clusters/enriched_units.jsonl"],
                    ),
                    "cluster_id": f"cl-{index:03d}",
                    "topic_label": labelled["topic_label"],
                    "unit_ids": [u["unit_id"] for u in units],
                    "routing_reason": labelled.get("routing_reason", ""),
                    "related_existing_topics": labelled.get("related_existing_topics", []),
                    "independence_groups": sorted({u["independence_group"] for u in units}),
                    "routing_confidence": 0.8,
                }
            )
        )
    write_jsonl_atomic(ctx.clusters, clusters)
    return clusters
