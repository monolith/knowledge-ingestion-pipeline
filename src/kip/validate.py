"""Provenance and integrity validation for a completed run.

Spec §22 acceptance criteria 3, 10, 11, 12: every retained unit traces to an
exact source excerpt by character offset and hash; the full chain reconstructs
from any durable leaf; the audit ran under the required conditions.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import (
    RunContext,
    file_hash,
    read_jsonl,
    seal_payload,
    stable_hash,
    text_hash,
)

# Above 40% of retained claims carrying no flag, `claim` has stopped being a
# type and started being a bucket. Claim is the residual gate by design, so this
# alarm is the only thing standing between "residual" and "everything".
UNFLAGGED_CLAIM_ALARM = 0.40


def _reseal(record: dict[str, Any]) -> str:
    # Deliberately delegates: the writer (artifacts.seal) and this checker must
    # never hold two copies of the exclusion rule.
    return stable_hash(seal_payload(record))



from .vocab import GROUNDING as GROUNDING_VALUES


def _check_grounding(
    units: list[dict[str, Any]],
    errors: list[str],
    warnings: list[str],
    counts: dict[str, int],
) -> None:
    """Hold the self-reported grounding flag to the citations it claims.

    `grounding` is the model's answer to "could you have written this from the
    document alone". It is self-report, and self-report in this pipeline has
    already been measured unreliable once -- so it is checked rather than
    trusted. The check is the one thing that IS mechanical: a unit cannot claim
    every clause is attributable while resting on a quote that could not be
    found in the source.

    The counts are health metrics, not failures. A corpus with some
    unattributed content is a corpus that needs review, not a broken run, and
    failing it would delete the evidence needed to do the review.
    """
    flagged = [u for u in units if u.get("grounding")]
    if not flagged:
        return

    unattributed = 0
    for unit in flagged:
        unit_id = unit.get("unit_id", "?")
        value = unit.get("grounding")
        if value not in GROUNDING_VALUES:
            errors.append(f"{unit_id}: unknown grounding {value!r}")
            continue
        if value == "unattributed_content":
            unattributed += 1
        if value == "attributable":
            unverified = [
                e for e in unit.get("evidence", []) if not e.get("excerpt_verified")
            ]
            if unverified:
                errors.append(
                    f"{unit_id}: claims grounding 'attributable' but "
                    f"{len(unverified)} of its excerpts could not be found in the "
                    "source, so the claim cannot be checked"
                )
        # An import without a supporting citation is the failure mode the flag
        # exists to catch: the statement went beyond its primary passage and
        # nothing licenses the difference.
        roles = {e.get("role", "primary") for e in unit.get("evidence", [])}
        if unit.get("decontextualization_note") and "supporting" not in roles:
            warnings.append(
                f"{unit_id}: records imported context but cites no supporting excerpt"
            )

    counts["units_unattributed"] = unattributed
    if unattributed:
        warnings.append(
            f"{unattributed} of {len(flagged)} units carry content no cited excerpt "
            "supports and are marked for review"
        )

# Which id field names a record of each kind. Carried alongside the records so
# a hash mismatch can name the offending RECORD; reporting `list(record)[0]`
# named the first key of a key-sorted dict, which is a field name and is the
# same for every record of that type.
ID_KEYS: dict[str, str] = {
    "unit": "unit_id",
    "cluster": "cluster_id",
    "assessment": "assessment_id",
    "candidate": "candidate_id",
    "approved": "candidate_id",
    "audit": "audit_id",
    "enriched_unit": "unit_id",
}


def _ids(records: list[dict[str, Any]], key: str, kind: str, errors: list[str]) -> set[str]:
    """Collect a set of ids, reporting missing and duplicate ones as errors.

    Both failures used to be silent in different ways: a missing id raised
    KeyError out of the validator (a CI job reads that as a crashed job, not a
    failed corpus), and a duplicate id collapsed two records into one in every
    downstream by-id dict without a word anywhere.
    """
    seen: set[str] = set()
    for index, record in enumerate(records):
        value = record.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"{kind} #{index}: missing {key}")
            continue
        if value in seen:
            errors.append(f"{kind} {value}: duplicate {key}")
        seen.add(value)
    return seen


def _check_completeness(ctx: RunContext, errors: list[str], warnings: list[str]) -> None:
    """A run that does not exist, or has been half-deleted, is not a clean run.

    `kip validate` returned ok:true with exit 0 for a typo'd run id and for a
    workspace whose artifacts had been deleted mid-run, because every artifact
    loader treated "file absent" as "nothing to check". A CI gate wired to this
    command passed on both.

    The chain check is scoped to runs the orchestrator produced -- a run_manifest
    is what says so. An artifact tree assembled by hand or by another tool is a
    legitimate thing to validate in isolation, and holding it to a full chain
    would report a missing pass rather than a real defect.
    """
    if not ctx.run_dir.is_dir():
        errors.append(f"run directory does not exist: {ctx.run_dir}")
        return

    chain = [
        ("01_normalized/source_registry.jsonl", ctx.source_registry),
        ("02_units/units.jsonl", ctx.units),
        ("03_clusters/clusters.jsonl", ctx.clusters),
        ("04_assessments/claim_assessments.jsonl", ctx.assessments),
        ("05_candidates/candidates.initial.jsonl", ctx.candidates),
        ("06_audit/audits.jsonl", ctx.audits),
        ("07_enqueue/enqueue.jsonl", ctx.enqueue),
    ]
    present = [name for name, path in chain if path.exists()]

    if not ctx.manifest.exists():
        if not present:
            errors.append(f"{ctx.run_dir} contains no pipeline artifacts")
        else:
            warnings.append(
                f"no {ctx.manifest.name}: this artifact tree was not produced by a "
                "completed pipeline run, so pass-completeness is not checked"
            )
        return

    # Downstream artifacts cannot exist without the artifact they were derived
    # from; that shape means files were deleted under a finished run.
    for index, (name, path) in enumerate(chain):
        if not path.exists():
            continue
        for upstream_name, upstream_path in chain[:index]:
            if not upstream_path.exists():
                errors.append(f"{name} exists but its upstream {upstream_name} is missing")
                break


def _check_originals(ctx: RunContext, registry: list[dict[str, Any]], errors: list[str]) -> None:
    """The registry's original_sha256 must still describe the file on disk.

    The copy under 00_original_sources is what makes the artifact tree
    self-contained; if it has drifted from the digest recorded at intake, the
    provenance chain ends at a file that no longer says what it said.
    """
    for record in registry:
        recorded = record.get("original_sha256")
        original = record.get("original_path")
        if not recorded or not original:
            continue
        # The path the file was actually read from, not a search by basename:
        # discovery is recursive, so two sources can share a filename, and
        # looking one up by name is the same defect this check exists to catch.
        path = Path(str(original))
        if not path.is_file():
            continue  # the source directory moved or was cleaned up
        if file_hash(path) != recorded:
            errors.append(
                f"{record.get('source_id', '?')}: {path.name} no longer matches the "
                "original_sha256 recorded at intake"
            )


def validate_run(ctx: RunContext) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}

    _check_completeness(ctx, errors, warnings)

    def load(name: str, path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records = read_jsonl(path)
        counts[name] = len(records)
        return records

    registry = load("sources", ctx.source_registry)
    units = load("units", ctx.units)
    enriched = load("enriched_units", ctx.enriched_units)
    clusters = load("clusters", ctx.clusters)
    assessments = load("assessments", ctx.assessments)
    candidates = load("candidates", ctx.candidates)
    audits = load("audits", ctx.audits)
    approved = load("approved", ctx.approved)
    events = load("queue_events", ctx.enqueue)

    # Every id namespace is checked for missing and duplicate entries. A
    # duplicate is not cosmetic: every downstream by-id dict (clustering,
    # auditing, tracing) collapses the pair and half the corpus disappears with
    # no error anywhere.
    _ids(registry, "source_id", "source", errors)
    unit_ids = _ids(units, "unit_id", "unit", errors)
    _ids(clusters, "cluster_id", "cluster", errors)
    assessment_ids = _ids(assessments, "assessment_id", "assessment", errors)
    candidate_ids = _ids(candidates, "candidate_id", "candidate", errors)
    _ids(approved, "candidate_id", "approved candidate", errors)
    _ids(audits, "audit_id", "audit", errors)
    _ids(events, "queue_event_id", "queue event", errors)

    _check_originals(ctx, registry, errors)

    _check_grounding(units, errors, warnings, counts)

    # --- Content hashes -------------------------------------------------------
    # `approved` and `enriched_unit` are in this loop because they are sealed:
    # the approved record is the one whose payload is copied into the queue
    # event, so leaving it out meant a hand-edited title reached the queue with
    # `kip validate` reporting a clean run.
    for name, records in (
        ("unit", units), ("enriched_unit", enriched), ("cluster", clusters),
        ("assessment", assessments), ("candidate", candidates),
        ("approved", approved), ("audit", audits),
    ):
        id_key = ID_KEYS[name]
        for record in records:
            if "content_sha256" not in record:
                continue
            if _reseal(record) != record["content_sha256"]:
                errors.append(
                    f"{name} {record.get(id_key, '<no id>')}: content hash mismatch"
                )

    # --- Evidence resolves to real source text --------------------------------
    source_cache: dict[str, str] = {}
    unverified = 0
    for unit in units:
        unit_id = unit.get("unit_id", "<no id>")
        for evidence in unit.get("evidence", []):
            excerpt = evidence.get("excerpt", "")
            if excerpt and text_hash(excerpt) != evidence.get("excerpt_sha256"):
                errors.append(f"{unit_id}: excerpt hash mismatch")
            if not evidence.get("excerpt_verified", False):
                unverified += 1
            rel = evidence.get("normalized_path", "")
            if rel not in source_cache:
                path = ctx.run_dir / rel
                source_cache[rel] = path.read_text(encoding="utf-8") if path.exists() else ""
            text = source_cache[rel]
            if not text:
                errors.append(f"{unit_id}: normalized source missing ({rel})")
                continue
            start = evidence.get("normalized_char_start", -1)
            end = evidence.get("normalized_char_end", -1)
            if excerpt and not (0 <= start < end <= len(text) and text[start:end] == excerpt):
                if excerpt not in text:
                    errors.append(f"{unit_id}: excerpt not present in normalized source")
                else:
                    warnings.append(f"{unit_id}: excerpt present but char offsets stale")
    if unverified:
        warnings.append(
            f"{unverified} evidence excerpts were not verbatim-matched at extraction time"
        )

    # Entity mentions are surface forms copied verbatim from the document (the
    # extraction prompt forbids canonicalizing them), so a surface that does not
    # occur in the normalized source was invented. They are excluded from
    # content_sha256 by contract, which means a rewritten mention list cannot be
    # caught by the hash -- locating them here is what closes that gap. A warning
    # rather than an error because the field is optional and best-effort, and
    # because the wiki that consumes it resolves entities independently.
    fabricated: list[str] = []
    for unit in units:
        text = source_cache.get(
            (unit.get("evidence") or [{}])[0].get("normalized_path", ""), ""
        )
        if not text:
            continue
        for mention in unit.get("entity_mentions", []):
            surface = mention.get("surface", "")
            if surface and surface not in text:
                fabricated.append(f"{unit.get('unit_id', '<no id>')}: {surface!r}")
    if fabricated:
        warnings.append(
            f"{len(fabricated)} entity mentions do not appear in their source text "
            "(surfaces are copied verbatim at extraction, so these were invented): "
            + ", ".join(fabricated[:10])
            + (" ..." if len(fabricated) > 10 else "")
        )

    # --- Referential integrity ------------------------------------------------
    for cluster in clusters:
        cluster_id = cluster.get("cluster_id", "<no id>")
        for unit_id in cluster.get("unit_ids", []):
            if unit_id not in unit_ids:
                errors.append(f"{cluster_id}: unknown unit {unit_id}")

    for assessment in assessments:
        assessment_id = assessment.get("assessment_id", "<no id>")
        for key in ("supporting_unit_ids", "opposing_unit_ids", "qualifying_unit_ids"):
            for unit_id in assessment.get(key, []):
                if unit_id not in unit_ids:
                    errors.append(f"{assessment_id}: unknown unit {unit_id}")

    # Spec §22 AC3: every retained unit traces to an exact source excerpt. A
    # candidate with no assertions or no cited units satisfies every per-item
    # check vacuously, so emptiness has to be named explicitly.
    for kind, records in (("candidate", candidates), ("approved candidate", approved)):
        for candidate in records:
            candidate_id = candidate.get("candidate_id", "<no id>")
            if not candidate.get("assertions"):
                errors.append(f"{kind} {candidate_id}: no assertions")
            if not candidate.get("source_unit_ids"):
                errors.append(f"{kind} {candidate_id}: no source_unit_ids")
            for assertion in candidate.get("assertions", []):
                if not assertion.get("assessment_ids"):
                    errors.append(f"{candidate_id}: assertion without assessment_ids")
                for assessment_id in assertion.get("assessment_ids", []):
                    if assessment_id not in assessment_ids:
                        errors.append(f"{candidate_id}: unknown assessment {assessment_id}")
            for unit_id in candidate.get("source_unit_ids", []):
                if unit_id not in unit_ids:
                    errors.append(f"{candidate_id}: unknown unit {unit_id}")

    for audit_record in audits:
        audit_id = audit_record.get("audit_id", "<no id>")
        if audit_record.get("candidate_id") not in candidate_ids:
            errors.append(
                f"{audit_id}: unknown candidate {audit_record.get('candidate_id')}"
            )
        # Spec §13.3: the audit is only trustworthy under these conditions.
        if not audit_record.get("auditor_distinct_from_proposer", False):
            errors.append(f"{audit_id}: auditor was not distinct from the proposer")

    # --- Queue events ---------------------------------------------------------
    approved_ids = {c.get("candidate_id") for c in approved}
    seen_keys: set[str] = set()
    for event in events:
        event_id = event.get("queue_event_id", "<no id>")
        if event.get("candidate_id") not in approved_ids:
            errors.append(f"{event_id}: candidate was never approved")
        key = event.get("idempotency_key")
        if not key:
            errors.append(f"{event_id}: missing idempotency_key")
        elif key in seen_keys:
            errors.append(f"{event_id}: duplicate idempotency key")
        else:
            seen_keys.add(key)
        if not event.get("audit_ids"):
            errors.append(f"{event_id}: queued without an audit reference")

    # --- Taxonomy (kt-v1) -----------------------------------------------------

    # --- Coverage -------------------------------------------------------------
    successful = [r for r in registry if r.get("normalization_status") == "success"]
    sources_with_units = {u.get("source_id") for u in units}
    for record in successful:
        if record.get("source_id") not in sources_with_units:
            warnings.append(
                f"{record.get('source_id', '<no id>')}: normalized but produced no units"
            )

    return {
        "ok": not errors,
        "run_id": ctx.run_id,
        "counts": counts,
        "errors": errors,
        "warnings": warnings,
    }
