"""Pass 3 — claim relationship and evidence synthesis.

Spec §11. Two stages: cheap candidate matching in code, then LLM judgment on
*presented pairs*. Never open-ended "does this cluster contain contradictions".
"""

from __future__ import annotations

from typing import Any

from .artifacts import RunContext, envelope, rotate, seal, write_jsonl_atomic
from .config import Config
from .llm import LLMClient
from .route import BM25, tokenize

PROMPT_VERSION = "pass-03-relationship-judgment-v3.0"

# Coarse stance is the tier established benchmarks validate (spec §11.3).
COARSE_STANCES = ["supports", "contradicts", "insufficient_evidence"]

# Buckets are the system's TRUST BOUNDARY. Downstream passes may rely on these;
# they may not rely on the fine subtype without independent confirmation.
BUCKETS = ["convergent", "contested", "singleton", "complementary"]

SUBTYPES = [
    "duplicate", "paraphrase", "convergent_independent", "convergent_dependent",
    "partially_contradicts", "scope_difference", "temporal_update",
    "methodological_qualification", "complementary", "singleton",
    "singleton_hypothesis", "authoritative_composite", "operational_composite",
]

ASSESS_SYSTEM = """You judge the relationship between knowledge units that have
already been retrieved as likely related. You are given specific candidate
groups -- judge what is presented; do not go looking for other relationships.

STEP A — coarse stance. This is the judgment you are trusted on. For the claim
under assessment, classify the evidence as:
  - supports: the units agree on the claim
  - contradicts: at least one unit is incompatible with another
  - insufficient_evidence: the units do not settle the claim

STEP B — subtype. Only after fixing the coarse stance, assign a finer label, and
report subtype_confidence honestly. Fine-grained relationship typing is
measurably unreliable; a low confidence is more useful than a confident guess.

EVIDENCE REQUIREMENT: if your coarse stance is "contradicts", you MUST quote the
specific conflicting text from each side. A contradiction without quoted
evidence is not reportable.

SOURCE INDEPENDENCE: count independent evidence GROUPS, not documents. Two
artifacts sharing an independence_group describe the SAME underlying study,
meeting, or pilot -- they are one piece of evidence, not two. Never label
same-group agreement as convergent_independent.

EVIDENCE WEIGHTING: weigh directness, source authority, study quality,
preregistration and sample size, scope match, and known limitations. Recency
matters only when the fact is time-sensitive. A source that merely summarizes
another adds no independent weight.

TEMPORAL: if one unit supersedes another in time, use temporal_update and set
t_valid/t_invalid rather than discarding the older claim.

Preserve disagreement. Do not resolve a genuine conflict into a confident
synthesis."""

ASSESS_SCHEMA = {
    "type": "object",
    "properties": {
        "assessments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "canonical_claim": {"type": "string"},
                    "coarse_stance": {"type": "string", "enum": COARSE_STANCES},
                    "relationship_bucket": {"type": "string", "enum": BUCKETS},
                    "relationship_subtype": {"type": "string", "enum": SUBTYPES},
                    "subtype_confidence": {"type": "number"},
                    "supporting_unit_ids": {"type": "array", "items": {"type": "string"}},
                    "opposing_unit_ids": {"type": "array", "items": {"type": "string"}},
                    "qualifying_unit_ids": {"type": "array", "items": {"type": "string"}},
                    "contradiction_evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "unit_id": {"type": "string"},
                                "excerpt": {"type": "string"},
                            },
                            "required": ["unit_id", "excerpt"],
                            "additionalProperties": False,
                        },
                    },
                    "independent_evidence_groups": {"type": "array", "items": {"type": "string"}},
                    "support_strength": {"type": "number"},
                    "importance_score": {"type": "number"},
                    "uncertainty": {"type": "string", "enum": ["low", "moderate", "high"]},
                    "synthesis": {"type": "string"},
                    "recommended_action": {"type": "string"},
                    "t_valid": {"type": "string"},
                    "t_invalid": {"type": "string"},
                },
                "required": [
                    "canonical_claim", "coarse_stance", "relationship_bucket",
                    "relationship_subtype", "subtype_confidence", "synthesis",
                    "recommended_action", "uncertainty",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["assessments"],
    "additionalProperties": False,
}


# The fields _materialize indexes without a default. Named here so the guard and
# the reader cannot disagree about what "malformed" means.
REQUIRED_RAW_FIELDS = (
    "canonical_claim",
    "coarse_stance",
    "relationship_bucket",
    "relationship_subtype",
    "uncertainty",
    "synthesis",
    "recommended_action",
)


def match_candidates(units: list[dict[str, Any]], top_k: int = 6) -> list[list[str]]:
    """Stage 1: retrieve plausible comparison groups, cheaply and in code.

    This exists because of the strongest evidence chain in the research:
    unguided whole-document contradiction detection runs at ~50-54% accuracy
    (near chance, 8% recall for GPT-4), while the SAME model given a specific
    candidate finds the contradicting counterpart 77.2% of the time. Localizing
    before judging is worth roughly 25 accuracy points.
    """
    if len(units) <= 2:
        return [[u["unit_id"] for u in units]] if units else []

    docs = [tokenize(u["canonical_statement"]) for u in units]
    bm25 = BM25(docs)
    groups: list[list[str]] = []
    seen: set[frozenset[str]] = set()

    for i, unit in enumerate(units):
        scored = sorted(
            ((bm25.score(docs[i], j), j) for j in range(len(units)) if j != i),
            reverse=True,
        )
        members = [i] + [j for score, j in scored[: top_k - 1] if score > 0]
        key = frozenset(units[m]["unit_id"] for m in members)
        if len(members) > 1 and key not in seen:
            seen.add(key)
            groups.append([units[m]["unit_id"] for m in members])
    return groups


def assess_clusters(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    units: list[dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_id = {u["unit_id"]: u for u in units}
    assessments: list[dict[str, Any]] = []
    counter = 0

    for cluster_index, cluster in enumerate(clusters):
        members = [by_id[uid] for uid in cluster["unit_ids"] if uid in by_id]
        if not members:
            continue

        # Spec §11.8 / §17: rotate ordering so different units occupy the
        # disadvantaged middle of the prompt across clusters. A fixed order
        # systematically penalizes whatever sits in the centre by up to 22pp.
        if cfg.batch.rotate_ordering:
            members = rotate(members, cluster_index)

        for batch in _batches(members, cfg.batch.target_size):
            pairs = match_candidates(batch)
            payload = _render(batch, pairs)
            try:
                result = client.complete_json(
                    system=ASSESS_SYSTEM,
                    user=payload,
                    schema=ASSESS_SCHEMA,
                    model=cfg.model_for("judge"),
                    max_tokens=16384,
                )
            except Exception as exc:
                print(f"[pass3] assessment failed for {cluster['cluster_id']}: {exc}")
                continue

            for raw in result.get("assessments", []):
                # Skip-and-report, never raise: one malformed assessment used to
                # abort Pass 3 and discard every assessment already produced for
                # every cluster. The judgment is per-item, so the failure should
                # be too.
                missing = [f for f in REQUIRED_RAW_FIELDS if f not in raw] if isinstance(
                    raw, dict
                ) else ["(not a JSON object)"]
                if missing:
                    print(
                        f"[pass3] skipped a malformed assessment in "
                        f"{cluster['cluster_id']}: missing {', '.join(missing)}"
                    )
                    continue
                counter += 1
                assessments.append(
                    _materialize(ctx, cluster, raw, by_id, counter)
                )

    write_jsonl_atomic(ctx.assessments, assessments)
    return assessments


def _batches(items: list[Any], size: int) -> list[list[Any]]:
    return [items[i : i + size] for i in range(0, len(items), size)] or [[]]


def _render(units: list[dict[str, Any]], pairs: list[list[str]]) -> str:
    lines = ["Units under comparison:"]
    for unit in units:
        evidence = unit.get("evidence") or [{}]
        excerpt = (evidence[0].get("excerpt") or "")[:300]
        lines.append(
            f"\n{unit['unit_id']} [{unit['unit_type']}]"
            f" (source={unit['source_id']}, independence_group={unit['independence_group']})"
            f"\n  statement: {unit['canonical_statement']}"
            f"\n  qualifiers: {', '.join(unit.get('qualifiers', [])) or 'none'}"
            f"\n  evidence: \"{excerpt}\""
        )
    if pairs:
        lines.append("\nRetrieved candidate comparison groups (judge these):")
        for group in pairs[:40]:
            lines.append(f"  - {', '.join(group)}")
    lines.append(
        "\nProduce one assessment per distinct claim these units bear on. "
        "Judge only the groups presented above."
    )
    return "\n".join(lines)


def _materialize(
    ctx: RunContext,
    cluster: dict[str, Any],
    raw: dict[str, Any],
    by_id: dict[str, dict[str, Any]],
    counter: int,
) -> dict[str, Any]:
    supporting = raw.get("supporting_unit_ids", [])
    opposing = raw.get("opposing_unit_ids", [])

    # Independence is recomputed from metadata rather than trusted from the
    # model. Spec §11.5 forbids counting documents; this is the mechanical
    # guarantee behind that rule, and it is what stops two artifacts describing
    # one pilot from inflating into two confirmations.
    groups = sorted(
        {
            by_id[uid]["independence_group"]
            for uid in supporting + opposing
            if uid in by_id
        }
    )

    stance = raw["coarse_stance"]
    evidence = raw.get("contradiction_evidence", [])
    flags: list[str] = []

    # Spec §11.4: a contradicts verdict without quoted evidence is not
    # reportable. Rather than dropping the assessment, downgrade it and say why
    # -- the audit needs to see the downgrade.
    if stance == "contradicts" and not evidence:
        stance = "insufficient_evidence"
        flags.append("contradiction_downgraded_missing_evidence")

    # A dependent convergence must never be reported as independent support.
    subtype = raw["relationship_subtype"]
    if subtype == "convergent_independent" and len(groups) < 2:
        subtype = "convergent_dependent"
        flags.append("subtype_corrected_single_independence_group")

    return seal(
        {
            **envelope(
                ctx,
                prompt_version=PROMPT_VERSION,
                model_role="claim-relationship-judge",
                parent_artifacts=["03_clusters/clusters.jsonl", "02_units/units.jsonl"],
            ),
            "assessment_id": f"asmt-{counter:04d}",
            "cluster_id": cluster["cluster_id"],
            "canonical_claim": raw["canonical_claim"],
            "coarse_stance": stance,
            "relationship_bucket": raw["relationship_bucket"],
            "relationship_subtype": subtype,
            # Advisory to Pass 4, not determinative (spec §11.3).
            "subtype_confidence": raw.get("subtype_confidence", 0.5),
            "supporting_unit_ids": supporting,
            "opposing_unit_ids": opposing,
            "qualifying_unit_ids": raw.get("qualifying_unit_ids", []),
            "contradiction_evidence": evidence,
            "independent_evidence_groups": groups,
            "source_validity_flags": flags,
            "t_valid": raw.get("t_valid"),
            "t_invalid": raw.get("t_invalid"),
            "support_strength": raw.get("support_strength", 1.0),
            "importance_score": raw.get("importance_score", 1.0),
            "uncertainty": raw["uncertainty"],
            "synthesis": raw["synthesis"],
            "recommended_action": raw["recommended_action"],
            "raw_source_escalations": [],
        }
    )
