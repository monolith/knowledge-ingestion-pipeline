"""Provenance and integrity validation for a completed run.

Spec §22 acceptance criteria 3, 10, 11, 12: every retained unit traces to an
exact source excerpt by character offset and hash; the full chain reconstructs
from any durable leaf; the audit ran under the required conditions.
"""

from __future__ import annotations

from typing import Any

from .artifacts import RunContext, read_jsonl, stable_hash, text_hash


def _reseal(record: dict[str, Any]) -> str:
    payload = {k: v for k, v in record.items() if k not in ("content_sha256", "created_at")}
    return stable_hash(payload)


def validate_run(ctx: RunContext) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}

    def load(name: str, path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records = read_jsonl(path)
        counts[name] = len(records)
        return records

    registry = load("sources", ctx.source_registry)
    units = load("units", ctx.units)
    clusters = load("clusters", ctx.clusters)
    assessments = load("assessments", ctx.assessments)
    candidates = load("candidates", ctx.candidates)
    audits = load("audits", ctx.audits)
    approved = load("approved", ctx.approved)
    events = load("queue_events", ctx.enqueue)

    unit_ids = {u["unit_id"] for u in units}
    assessment_ids = {a["assessment_id"] for a in assessments}
    candidate_ids = {c["candidate_id"] for c in candidates}

    # --- Content hashes -------------------------------------------------------
    for name, records in (
        ("unit", units), ("cluster", clusters), ("assessment", assessments),
        ("candidate", candidates), ("audit", audits),
    ):
        for record in records:
            if "content_sha256" not in record:
                continue
            if _reseal(record) != record["content_sha256"]:
                errors.append(f"{name} {record.get('artifact_id') or list(record)[0]}: content hash mismatch")

    # --- Evidence resolves to real source text --------------------------------
    source_cache: dict[str, str] = {}
    unverified = 0
    for unit in units:
        for evidence in unit.get("evidence", []):
            excerpt = evidence.get("excerpt", "")
            if excerpt and text_hash(excerpt) != evidence.get("excerpt_sha256"):
                errors.append(f"{unit['unit_id']}: excerpt hash mismatch")
            if not evidence.get("excerpt_verified", False):
                unverified += 1
            rel = evidence.get("normalized_path", "")
            if rel not in source_cache:
                path = ctx.run_dir / rel
                source_cache[rel] = path.read_text(encoding="utf-8") if path.exists() else ""
            text = source_cache[rel]
            if not text:
                errors.append(f"{unit['unit_id']}: normalized source missing ({rel})")
                continue
            start, end = evidence.get("normalized_char_start", -1), evidence.get("normalized_char_end", -1)
            if excerpt and not (0 <= start < end <= len(text) and text[start:end] == excerpt):
                if excerpt not in text:
                    errors.append(f"{unit['unit_id']}: excerpt not present in normalized source")
                else:
                    warnings.append(f"{unit['unit_id']}: excerpt present but char offsets stale")
    if unverified:
        warnings.append(
            f"{unverified} evidence excerpts were not verbatim-matched at extraction time"
        )

    # --- Referential integrity ------------------------------------------------
    for cluster in clusters:
        for unit_id in cluster["unit_ids"]:
            if unit_id not in unit_ids:
                errors.append(f"{cluster['cluster_id']}: unknown unit {unit_id}")

    for assessment in assessments:
        for key in ("supporting_unit_ids", "opposing_unit_ids", "qualifying_unit_ids"):
            for unit_id in assessment.get(key, []):
                if unit_id not in unit_ids:
                    errors.append(f"{assessment['assessment_id']}: unknown unit {unit_id}")

    for candidate in candidates:
        for assertion in candidate.get("assertions", []):
            if not assertion.get("assessment_ids"):
                errors.append(f"{candidate['candidate_id']}: assertion without assessment_ids")
            for assessment_id in assertion.get("assessment_ids", []):
                if assessment_id not in assessment_ids:
                    errors.append(f"{candidate['candidate_id']}: unknown assessment {assessment_id}")

    for audit in audits:
        if audit["candidate_id"] not in candidate_ids:
            errors.append(f"{audit['audit_id']}: unknown candidate {audit['candidate_id']}")
        # Spec §13.3: the audit is only trustworthy under these conditions.
        if not audit.get("auditor_distinct_from_proposer", False):
            errors.append(f"{audit['audit_id']}: auditor was not distinct from the proposer")

    # --- Queue events ---------------------------------------------------------
    approved_ids = {c["candidate_id"] for c in approved}
    seen_keys: set[str] = set()
    for event in events:
        if event["candidate_id"] not in approved_ids:
            errors.append(f"{event['queue_event_id']}: candidate was never approved")
        if event["idempotency_key"] in seen_keys:
            errors.append(f"{event['queue_event_id']}: duplicate idempotency key")
        seen_keys.add(event["idempotency_key"])
        if not event.get("audit_ids"):
            errors.append(f"{event['queue_event_id']}: queued without an audit reference")

    # --- Coverage -------------------------------------------------------------
    successful = [r for r in registry if r.get("normalization_status") == "success"]
    sources_with_units = {u["source_id"] for u in units}
    for record in successful:
        if record["source_id"] not in sources_with_units:
            warnings.append(f"{record['source_id']}: normalized but produced no units")

    return {
        "ok": not errors,
        "run_id": ctx.run_id,
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
    }
