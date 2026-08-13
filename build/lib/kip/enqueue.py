"""Step 6 — queue handoff. Deterministic code, not an LLM reasoning pass.

Spec §14. Produces idempotent events for the existing leaf engine, which remains
the sole authority for merge, bubbling, linking, and durable materialization.
"""

from __future__ import annotations

from typing import Any

from .artifacts import RunContext, read_jsonl, stable_hash, utc_now, write_jsonl_atomic
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
    idempotency key is derived from the event's content rather than generated
    randomly -- replaying this pass produces byte-identical events, so a retry is
    provably harmless.

    What goes INTO the key is the part that has to be right. `candidate_id` is
    only a per-run counter ("cand-001"), so keying on (target, candidate,
    version) alone made every run's Nth approved candidate share one key: a
    consumer doing exactly what this docstring tells it to do would discard every
    run after the first, silently, forever. The key therefore also carries the
    run id and a digest of the payload -- the payload digest is what actually
    makes a replay idempotent, and the run id keeps two runs' proposals distinct
    even when they say the same thing about the same topic.
    """
    # The travel rule: an entry carries every asset related to any of its
    # source units. An asset's survival is decided by whether the text it sits
    # in survived -- a judgment about the text, already made on the text's
    # merits -- and not by whether some unit happened to quote it.
    links_path = ctx.units.parent / "asset_links.jsonl"
    links = read_jsonl(links_path) if links_path.exists() else []
    assets_by_unit: dict[str, list[str]] = {}
    for row in links:
        ids = assets_by_unit.setdefault(row["unit_id"], [])
        if row["asset_id"] not in ids:
            ids.append(row["asset_id"])

    events: list[dict[str, Any]] = []

    for candidate in approved:
        candidate_id = candidate["candidate_id"]
        version = int(candidate["candidate_version"])
        payload = {
            "title": candidate["title"],
            "slug": candidate["slug"],
            "knowledge_state": candidate["knowledge_state"],
            "summary": candidate["summary"],
            "assertions": candidate["assertions"],
            "source_unit_ids": candidate["source_unit_ids"],
            "related_topics": candidate.get("related_topics", []),
            "labels": candidate.get("labels", []),
            "related_asset_ids": sorted({
                asset_id
                for unit_id in candidate["source_unit_ids"]
                for asset_id in assets_by_unit.get(unit_id, [])
            }),
        }
        key = stable_hash(
            {
                "target": target_engine,
                "run_id": ctx.run_id,
                "candidate_id": candidate_id,
                "version": version,
                "payload_sha256": stable_hash(payload),
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
                "payload": payload,
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
