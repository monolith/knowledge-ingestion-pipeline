"""Step 6 — queue handoff. Deterministic code, not an LLM reasoning pass.

Spec §14. Produces idempotent events for the existing leaf engine, which remains
the sole authority for merge, bubbling, linking, and durable materialization.
"""

from __future__ import annotations

from typing import Any

from .artifacts import RunContext, stable_hash, utc_now, write_jsonl_atomic
from .config import SCHEMA_VERSION

TARGET_ENGINE = "existing-leaf-engine"


def enqueue_approved(
    ctx: RunContext,
    approved: list[dict[str, Any]],
    target_engine: str = TARGET_ENGINE,
) -> list[dict[str, Any]]:
    """Emit one idempotent queue event per approved candidate version.

    Outbox semantics (spec §14): the relay may publish a message more than once,
    so delivery is at-least-once and the CONSUMER must deduplicate. The
    idempotency key is derived from (target, candidate, version) rather than
    generated randomly -- replaying this pass produces byte-identical events, so
    a retry is provably harmless.
    """
    events: list[dict[str, Any]] = []

    for candidate in approved:
        candidate_id = candidate["candidate_id"]
        version = int(candidate["candidate_version"])
        key = stable_hash(
            {
                "target": target_engine,
                "candidate_id": candidate_id,
                "version": version,
            }
        )
        events.append(
            {
                "schema_version": SCHEMA_VERSION,
                "run_id": ctx.run_id,
                "created_at": utc_now(),
                "queue_event_id": f"q-{key[:16]}",
                "idempotency_key": key,
                "target_engine": target_engine,
                "operation": candidate["suggested_operation"],
                "candidate_id": candidate_id,
                "candidate_version": version,
                "audit_ids": candidate.get("audit_ids", []),
                "payload": {
                    "title": candidate["title"],
                    "slug": candidate["slug"],
                    "knowledge_state": candidate["knowledge_state"],
                    "summary": candidate["summary"],
                    "assertions": candidate["assertions"],
                    "source_unit_ids": candidate["source_unit_ids"],
                    "related_topics": candidate.get("related_topics", []),
                    "labels": candidate.get("labels", []),
                },
                # The full chain, so a durable leaf can be walked back to the
                # original file without consulting this pipeline's code.
                "provenance_chain": {
                    "approved_candidates": "06_audit/candidates.approved.jsonl",
                    "audits": "06_audit/audits.jsonl",
                    "initial_candidates": "05_candidates/candidates.initial.jsonl",
                    "assessments": "04_assessments/claim_assessments.jsonl",
                    "clusters": "03_clusters/clusters.jsonl",
                    "units": "02_units/units.jsonl",
                    "omissions": "02_units/omissions.jsonl",
                    "source_registry": "01_normalized/source_registry.jsonl",
                },
                "status": "ready",
            }
        )

    write_jsonl_atomic(ctx.enqueue, events)
    return events
