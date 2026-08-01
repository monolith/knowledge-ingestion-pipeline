"""Provenance tracing — follow any artifact back to the original file.

Spec §3.10 and §22.10: every durable assertion is traceable backward through
queue event, audited candidate, assessment, cluster, unit, normalized text
location, and original file.
"""

from __future__ import annotations

from typing import Any

from .artifacts import RunContext, read_jsonl


def _index(records: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {r[key]: r for r in records if key in r}


def trace_leaf(ctx: RunContext, target: str) -> str | None:
    """Render the full chain for a queue event, candidate, or unit."""
    events = read_jsonl(ctx.enqueue) if ctx.enqueue.exists() else []
    approved = read_jsonl(ctx.approved) if ctx.approved.exists() else []
    audits = read_jsonl(ctx.audits) if ctx.audits.exists() else []
    candidates = read_jsonl(ctx.candidates) if ctx.candidates.exists() else []
    assessments = read_jsonl(ctx.assessments) if ctx.assessments.exists() else []
    clusters = read_jsonl(ctx.clusters) if ctx.clusters.exists() else []
    units = read_jsonl(ctx.units) if ctx.units.exists() else []
    registry = read_jsonl(ctx.source_registry) if ctx.source_registry.exists() else []

    units_by_id = _index(units, "unit_id")
    sources_by_id = _index(registry, "source_id")
    assessments_by_id = _index(assessments, "assessment_id")

    # A unit target renders the short chain: unit -> source excerpt -> file.
    if target in units_by_id:
        return _render_unit_chain(units_by_id[target], sources_by_id, clusters)

    event = next((e for e in events if target in (e["queue_event_id"], e["candidate_id"])), None)
    candidate = next((c for c in approved + candidates if c["candidate_id"] == target), None)
    if event is None and candidate is None:
        return None
    if candidate is None:
        candidate = next(
            (c for c in approved + candidates if c["candidate_id"] == event["candidate_id"]), None
        )
    if candidate is None:
        return None

    lines: list[str] = []
    if event:
        lines.append(f"queue event {event['queue_event_id']}  (op={event['operation']}, status={event['status']})")
        lines.append(f"  idempotency_key {event['idempotency_key'][:16]}...")
        lines.append("  <-")

    lines.append(f"candidate {candidate['candidate_id']} v{candidate['candidate_version']}")
    lines.append(f"  title: {candidate['title']}")
    lines.append(f"  knowledge_state: {candidate['knowledge_state']}")
    if candidate.get("supersedes"):
        lines.append(f"  supersedes: {candidate['supersedes']} (audit produced a new version)")

    for audit_id in candidate.get("audit_ids", []):
        audit = next((a for a in audits if a["audit_id"] == audit_id), None)
        if audit is None:
            continue
        lines.append("  <-")
        lines.append(f"audit {audit['audit_id']}  verdict={audit['verdict']}")
        lines.append(f"  auditor: {audit.get('auditor_model')} (distinct={audit.get('auditor_distinct_from_proposer')})")
        for finding in audit.get("findings", [])[:5]:
            lines.append(f"    - {finding}")

    assessment_ids: list[str] = []
    for assertion in candidate.get("assertions", []):
        for assessment_id in assertion.get("assessment_ids", []):
            if assessment_id not in assessment_ids:
                assessment_ids.append(assessment_id)

    unit_ids: list[str] = []
    for assessment_id in assessment_ids:
        assessment = assessments_by_id.get(assessment_id)
        if assessment is None:
            continue
        lines.append("  <-")
        lines.append(
            f"assessment {assessment_id}  stance={assessment['coarse_stance']}"
            f" bucket={assessment['relationship_bucket']}"
            f" subtype={assessment['relationship_subtype']}"
            f" (conf {assessment.get('subtype_confidence', 0.5):.2f})"
        )
        lines.append(f"  claim: {assessment['canonical_claim']}")
        groups = assessment.get("independent_evidence_groups", [])
        lines.append(f"  independent evidence groups: {len(groups)} {groups}")
        for key in ("supporting_unit_ids", "opposing_unit_ids", "qualifying_unit_ids"):
            for unit_id in assessment.get(key, []):
                if unit_id not in unit_ids:
                    unit_ids.append(unit_id)

    for unit_id in unit_ids or candidate.get("source_unit_ids", []):
        unit = units_by_id.get(unit_id)
        if unit is None:
            continue
        lines.append("  <-")
        lines.append(f"unit {unit_id} [{unit['unit_type']}]  group={unit['independence_group']}")
        lines.append(f"  {unit['canonical_statement']}")
        for evidence in unit.get("evidence", []):
            source = sources_by_id.get(evidence["source_id"], {})
            verified = "verbatim" if evidence.get("excerpt_verified") else "UNVERIFIED"
            lines.append(
                f"    evidence [{verified}] {evidence['normalized_path']}"
                f":{evidence['normalized_line_start']}-{evidence['normalized_line_end']}"
                f" chars {evidence['normalized_char_start']}-{evidence['normalized_char_end']}"
            )
            lines.append(f'      "{evidence["excerpt"][:160]}"')
            if source:
                lines.append(f"    <- original file: {source.get('filename')} (sha256 {source.get('original_sha256', '')[:12]}...)")

    return "\n".join(lines)


def _render_unit_chain(
    unit: dict[str, Any],
    sources_by_id: dict[str, dict[str, Any]],
    clusters: list[dict[str, Any]],
) -> str:
    lines = [f"unit {unit['unit_id']} [{unit['unit_type']}]"]
    lines.append(f"  {unit['canonical_statement']}")
    if unit.get("decontextualization_note"):
        lines.append(f"  decontextualization: {unit['decontextualization_note']}")
    lines.append(f"  granularity_policy: {unit.get('granularity_policy')}")
    member_of = [c["cluster_id"] for c in clusters if unit["unit_id"] in c.get("unit_ids", [])]
    if member_of:
        lines.append(f"  clusters: {', '.join(member_of)}")
    for evidence in unit.get("evidence", []):
        source = sources_by_id.get(evidence["source_id"], {})
        verified = "verbatim" if evidence.get("excerpt_verified") else "UNVERIFIED"
        lines.append(
            f"  <- evidence [{verified}] {evidence['normalized_path']}"
            f":{evidence['normalized_line_start']}-{evidence['normalized_line_end']}"
        )
        lines.append(f'       "{evidence["excerpt"][:200]}"')
        if source:
            lines.append(f"  <- original file: {source.get('filename')}")
    return "\n".join(lines)
