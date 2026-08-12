"""Pass 4 — candidate leaf generation.

Spec §12. Plans knowledge-base operations; never writes to the durable wiki.
"""

from __future__ import annotations

import re
from typing import Any

from .artifacts import RunContext, envelope, seal, write_jsonl_atomic
from .config import Config
from .llm import LLMClient

PROMPT_VERSION = "pass-04-candidate-planning-v3.1"  # v3.1: combine, never drop

OPERATIONS = ["create", "update", "create_or_update", "merge", "split", "link", "no_op", "defer"]
KNOWLEDGE_STATES = [
    "established", "supported", "contested", "preliminary",
    "internal-observation", "operational", "authoritative",
]

PLAN_SYSTEM = """You turn claim assessments into proposed knowledge-base operations.

You are PLANNING, not writing. Nothing you produce reaches the knowledge base
until it passes an independent audit.

RULES
- State knowledge_state explicitly and honestly. A claim supported by one
  exploratory analysis is "preliminary", not "established". A claim where a
  larger independent replication disagrees is "contested", not "supported".
- Every assertion must cite the assessment IDs it rests on.
- Create coherent topics, not one leaf per unit. Avoid fragmentation: prefer
  COMBINING a narrow finding into a broader leaf when the ontology allows.
  Combining means carrying it across as its own assertion under a wider title --
  it does NOT mean summarizing several units into one sentence. The point of
  grouping is to remove duplication and noise, never to drop content: if two
  units say the same thing, keep one; if they say different things, keep both.
- EVERY unit you were given must end up somewhere. Each one either becomes an
  assertion, is folded into an assertion that already carries its content, or is
  a duplicate of one that is. A unit that is none of those has not been
  incorporated -- it has been lost, and a definition or a rule is exactly the
  kind of content that gets lost this way, because it states no claim to argue
  with. When a unit is a definition, a rule, or a procedure, carry its content
  across rather than describing it: a reader must be able to apply it from the
  assertion alone, without going back to the source.
- Preserve negative and null findings. A well-evidenced "no effect" is
  knowledge.
- NEVER convert a dependent convergence into independent support. If the
  assessment says the evidence comes from one independence group, the candidate
  must not imply replication.

RELIABILITY: relationship_bucket is trustworthy. relationship_subtype is
ADVISORY and carries a confidence score -- do not build a claim that depends on
a low-confidence subtype being exactly right. Roughly a fifth to a third of
upstream relationship labels are expected to be wrong; write candidates that
survive that."""

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "candidates": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "knowledge_state": {"type": "string", "enum": KNOWLEDGE_STATES},
                    "priority": {"type": "integer", "enum": [1, 2, 3]},
                    "summary": {"type": "string"},
                    "assertions": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "assessment_ids": {"type": "array", "items": {"type": "string"}},
                            },
                            "required": ["text", "assessment_ids"],
                            "additionalProperties": False,
                        },
                    },
                    "source_unit_ids": {"type": "array", "items": {"type": "string"}},
                    "related_topics": {"type": "array", "items": {"type": "string"}},
                    "suggested_operation": {"type": "string", "enum": OPERATIONS},
                },
                "required": [
                    "title", "knowledge_state", "summary", "assertions",
                    "source_unit_ids", "suggested_operation",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["candidates"],
    "additionalProperties": False,
}


# The fields the materializer below indexes without a default.
REQUIRED_RAW_FIELDS = (
    "title",
    "knowledge_state",
    "summary",
    "assertions",
    "source_unit_ids",
    "suggested_operation",
)


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")[:80] or "leaf"


def plan_candidates(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    assessments: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not assessments:
        write_jsonl_atomic(ctx.candidates, [])
        return []

    candidates: list[dict[str, Any]] = []
    counter = 0

    # Group by cluster so each planning call sees one coherent topic, keeping
    # the item count well inside the safe batch band (spec §17).
    by_cluster: dict[str, list[dict[str, Any]]] = {}
    for assessment in assessments:
        by_cluster.setdefault(assessment["cluster_id"], []).append(assessment)

    for cluster_id, group in by_cluster.items():
        try:
            result = client.complete_json(
                system=PLAN_SYSTEM,
                user=_render(group),
                schema=PLAN_SCHEMA,
                model=cfg.model_for("planner"),
                max_tokens=16384,
            )
        except Exception as exc:
            print(f"[pass4] planning failed for {cluster_id}: {exc}")
            continue

        for raw in result.get("candidates", []):
            # Same rule as Pass 1 and Pass 3: a malformed proposal is one lost
            # candidate, not a lost pass. Raising here discarded every candidate
            # planned for every earlier cluster too.
            missing = (
                [f for f in REQUIRED_RAW_FIELDS if f not in raw]
                if isinstance(raw, dict)
                else ["(not a JSON object)"]
            )
            if missing:
                print(
                    f"[pass4] skipped a malformed candidate in {cluster_id}: "
                    f"missing {', '.join(missing)}"
                )
                continue
            counter += 1
            candidates.append(
                seal(
                    {
                        **envelope(
                            ctx,
                            prompt_version=PROMPT_VERSION,
                            model_role="candidate-leaf-planner",
                            parent_artifacts=["04_assessments/claim_assessments.jsonl"],
                        ),
                        "candidate_id": f"cand-{counter:03d}",
                        "candidate_version": 1,
                        "cluster_id": cluster_id,
                        "title": raw["title"],
                        "slug": slugify(raw["title"]),
                        "knowledge_state": raw["knowledge_state"],
                        "priority": raw.get("priority", 2),
                        "summary": raw["summary"],
                        "assertions": raw["assertions"],
                        "source_unit_ids": raw["source_unit_ids"],
                        "related_topics": raw.get("related_topics", []),
                        "suggested_operation": raw["suggested_operation"],
                        # Spec §12: every candidate is flagged for audit. There
                        # is no path to the queue that skips Pass 5.
                        "audit_required": True,
                    }
                )
            )

    write_jsonl_atomic(ctx.candidates, candidates)
    return candidates


def _render(assessments: list[dict[str, Any]]) -> str:
    lines = ["Assessments for this topic cluster:"]
    for a in assessments:
        lines.append(
            f"\n{a['assessment_id']}"
            f"\n  claim: {a['canonical_claim']}"
            f"\n  coarse_stance: {a['coarse_stance']}  (trustworthy)"
            f"\n  bucket: {a['relationship_bucket']}  (trustworthy)"
            f"\n  subtype: {a['relationship_subtype']}"
            f" (advisory, confidence {a.get('subtype_confidence', 0.5):.2f})"
            f"\n  independent_evidence_groups: {len(a.get('independent_evidence_groups', []))}"
            f" {a.get('independent_evidence_groups', [])}"
            f"\n  uncertainty: {a['uncertainty']}"
            f"\n  supporting: {a.get('supporting_unit_ids', [])}"
            f"\n  opposing: {a.get('opposing_unit_ids', [])}"
            f"\n  synthesis: {a['synthesis']}"
            f"\n  recommended_action: {a['recommended_action']}"
        )
        if a.get("source_validity_flags"):
            lines.append(f"  NOTE — pipeline corrections applied: {a['source_validity_flags']}")
    lines.append("\nPropose candidate knowledge-base operations.")
    return "\n".join(lines)
