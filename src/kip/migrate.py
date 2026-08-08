"""Backfill kt-v1 taxonomy fields onto units written before the taxonomy existed.

Build contract §2.4. Writes the new fields ALONGSIDE `unit_type` -- the legacy
label is never removed, because it is the control arm of the taxonomy
evaluation and a migration that destroys the comparison destroys the point of
running one.

Three properties this pass must have, and the reasons they are not optional:

- **Idempotent.** Re-running it re-derives from `unit_type` and the statement,
  which are both unchanged, so the second run produces the same bytes as the
  first. Re-running must never compound.
- **Hash-preserving.** `content_sha256` is taken over the assertion, never over
  its labels (`artifacts.DERIVED_FIELDS`), so adding a classification to a unit
  leaves its content identity alone. Before schema 3.1.0 this pass was
  impossible for exactly that reason. This module VERIFIES that rather than
  asserting it in prose: `migrate_unit` recomputes the digest and refuses a unit
  whose stored hash disagrees. Re-sealing unconditionally, which is what it used
  to do, would launder a hand-edited statement past `kip validate` -- the
  migration would overwrite the evidence of the edit and then report success.
- **Non-destructive.** Contract §3.9: any stage may re-derive, no stage may
  overwrite. A unit already carrying a real `kt-v1` classification holds six
  independent answers from a model; the legacy label holds one coarse guess.
  Rebuilding the first from the second is a downgrade that no later check can
  detect, because every field it touches is excluded from the content hash by
  design. Such units are skipped and counted unless `reclassify=True` says
  otherwise explicitly.

Migrated units are stamped `taxonomy_version="kt-v1-migrated"` rather than
`kt-v1`. A label inferred from a coarser legacy label is weaker evidence than
one a model produced against the type tests, and any evaluation that mixes the
two without being able to tell them apart is measuring its own migration.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .artifacts import (
    PipelineError,
    RunContext,
    read_jsonl,
    seal,
    seal_payload,
    stable_hash,
    write_jsonl_atomic,
)
from .taxonomy import (
    LEGACY_MAP,
    LEGACY_UNMAPPED,
    TAXONOMY_VERSION,
    UNCLASSIFIED,
    TYPE_TESTS,
    derive_family,
    detect_quantitative,
    legacy_summary,
)

MIGRATED_TAXONOMY_VERSION = "kt-v1-migrated"

# The mapping runs on labels, not on statements: no model is called here, so
# there is no classifier to name. Recording that explicitly keeps a migrated
# unit from being read as a classified one.
MIGRATION_CLASSIFIER = "legacy-label-map"


def _tests_for(unit_type: str) -> dict[str, bool]:
    """Reconstruct the six booleans a fresh classification would have produced.

    Exactly one fires, or none for the unmapped labels. This is a reconstruction
    from a coarser signal, not a measurement -- which is why `gates_fired` is
    written but `multi_fire` can never be true for a migrated unit, and why the
    version stamp above marks these records as second-class evidence.
    """
    fired = f"is_{unit_type}"
    return {name: name == fired for name in TYPE_TESTS}


def already_classified(unit: dict[str, Any]) -> bool:
    """True when this unit holds a real classification, not a migrated one.

    `kt-v1-migrated` is deliberately NOT protected: re-running the migration
    over its own output is the idempotence property, and it produces the same
    bytes. `kt-v1` is protected, because that stamp means a model answered the
    six tests directly.
    """
    return unit.get("taxonomy_version") == TAXONOMY_VERSION


def migrate_unit(unit: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of `unit` carrying kt-v1 fields derived from `unit_type`."""
    legacy = unit.get("unit_type", "")
    migrated = dict(unit)

    node_kind = "unit"
    migration_note: str | None = None

    if legacy in LEGACY_MAP:
        unit_type, modality, flags = LEGACY_MAP[legacy]
        if unit_type is None:
            # `open_question` is the one mapped label with no type: a question
            # has no truth value to check, no procedure to run, and no instance
            # that occurred, so it leaves the type system entirely.
            unit_type = UNCLASSIFIED
            node_kind = "question"
    elif legacy in LEGACY_UNMAPPED:
        # Never guess. These five are undecidable from the label alone, and a
        # plausible guess here is indistinguishable downstream from a real
        # classification.
        unit_type, modality, flags = UNCLASSIFIED, None, ()
        migration_note = f"legacy label {legacy!r}: {LEGACY_UNMAPPED[legacy]}"
    else:
        unit_type, modality, flags = UNCLASSIFIED, None, ()
        migration_note = f"unknown legacy label {legacy!r}"

    tests = _tests_for(unit_type)
    # Coerced rather than trusted: `detect_quantitative` takes a string, and a
    # unit whose statement is missing or numeric would otherwise abort the whole
    # migration with a TypeError raised three frames down inside a regex.
    raw_statement = unit.get("canonical_statement")
    statement = raw_statement if isinstance(raw_statement, str) else ""

    migrated.update(
        {
            "type_tests": tests,
            "type": unit_type,
            "family": derive_family(unit_type),
            "gates_fired": sum(1 for value in tests.values() if value),
            "multi_fire": False,
            "modality": modality,
            "flags": list(flags),
            # Re-derived by code rather than trusted from the legacy
            # `quantitative_result` label, which was applied by a model and
            # covers a different question than "does this carry a number".
            "quantitative": detect_quantitative(statement),
            "node_kind": node_kind,
            "entity_mentions": unit.get("entity_mentions", []),
            "taxonomy_version": MIGRATED_TAXONOMY_VERSION,
            "classifier_model": MIGRATION_CLASSIFIER,
            "migration_note": migration_note,
        }
    )
    # VERIFY the hash rather than re-stamp it. Every field written above is in
    # artifacts.DERIVED_FIELDS, so a correct migration of a 3.1.0 record cannot
    # move the digest -- which means a moved digest says the record's ASSERTION
    # changed since it was sealed, and re-sealing would erase the only evidence
    # of that. Re-sealing unconditionally laundered a hand-edited statement past
    # `kip validate`: it failed before the migration and passed after it.
    stored = unit.get("content_sha256")
    if stored is not None and stored != stable_hash(seal_payload(migrated)):
        # ...except for the one legitimate reason a stored digest disagrees:
        # schema 3.0.0 hashed `unit_type`, so an untouched pre-taxonomy record
        # verifies under the OLD rule and not the new one. Repairing exactly
        # those is what the upgrade path is for. Anything matching neither rule
        # was edited.
        if stored != stable_hash(_schema_3_0_0_payload(unit)):
            raise PipelineError(
                f"{unit.get('unit_id', '?')}: content hash matches neither the 3.1.0 "
                "rule nor the 3.0.0 rule. The unit's statement, evidence, or source "
                "lineage was edited after it was sealed. Migrating would overwrite "
                "the hash and hide the edit; repair the record or re-extract instead."
            )
    return seal(migrated)


def _schema_3_0_0_payload(unit: dict[str, Any]) -> dict[str, Any]:
    """The pre-3.1.0 seal rule, kept only to recognize an untouched old record.

    3.0.0 hashed every field except content_sha256 and created_at -- including
    the derived `unit_type`, which is the defect schema 3.1.0 exists to fix.
    """
    return {k: v for k, v in unit.items() if k not in ("content_sha256", "created_at")}


def migrate_units(
    units: list[dict[str, Any]], *, reclassify: bool = False
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Migrate a list of unit records and report honestly on what happened."""
    migrated: list[dict[str, Any]] = []
    considered: list[dict[str, Any]] = []
    skipped: list[str] = []
    for unit in units:
        if already_classified(unit) and not reclassify:
            migrated.append(unit)
            skipped.append(str(unit.get("unit_id", "?")))
            continue
        considered.append(unit)
        migrated.append(migrate_unit(unit))

    unmapped_by_label: Counter[str] = Counter()
    for unit in considered:
        legacy = unit.get("unit_type", "")
        if legacy not in LEGACY_MAP:
            unmapped_by_label[legacy] += 1

    type_histogram = Counter(unit.get("type", UNCLASSIFIED) for unit in migrated)
    claims = [u for u in migrated if u.get("type") == "claim"]
    unflagged_claims = [u for u in claims if not u.get("flags")]
    unflagged_claim_share = (len(unflagged_claims) / len(migrated)) if migrated else 0.0

    summary = {
        "units": len(migrated),
        "migrated": len(considered),
        # Skipped units are reported, never hidden: a run that is mostly
        # already-classified should look like one in the output.
        "skipped_already_classified": len(skipped),
        "skipped_unit_ids": skipped[:20],
        "mapped": len(considered) - sum(unmapped_by_label.values()),
        "unmapped": sum(unmapped_by_label.values()),
        "unmapped_by_label": dict(sorted(unmapped_by_label.items())),
        "type_histogram": dict(sorted(type_histogram.items())),
        "questions": sum(1 for u in migrated if u.get("node_kind") == "question"),
        "quantitative": sum(1 for u in migrated if u.get("quantitative")),
        "unflagged_claims": len(unflagged_claims),
        "unflagged_claim_share": round(unflagged_claim_share, 4),
        "taxonomy_version": MIGRATED_TAXONOMY_VERSION,
        "reclassified_kt_v1": reclassify,
        "legacy_coverage": legacy_summary(),
    }
    return migrated, summary


def migrate_run(ctx: RunContext, *, reclassify: bool = False) -> dict[str, Any]:
    """Migrate a run's `units.jsonl` in place. Safe to run more than once."""
    units = read_jsonl(ctx.units)
    migrated, summary = migrate_units(units, reclassify=reclassify)
    write_jsonl_atomic(ctx.units, migrated)
    summary["run_id"] = ctx.run_id
    summary["path"] = str(ctx.units)
    return summary


def format_summary(summary: dict[str, Any]) -> str:
    """Human-readable report. States the honest counts, including the bad ones."""
    lines = [
        f"run {summary.get('run_id', '?')}: {summary['units']} units -> "
        f"{summary['taxonomy_version']}",
        f"  migrated                 : {summary['migrated']}",
        f"  mapped deterministically : {summary['mapped']}",
        f"  needing review           : {summary['unmapped']}",
    ]
    if summary["skipped_already_classified"]:
        lines.append(
            f"  left untouched (already {TAXONOMY_VERSION}): "
            f"{summary['skipped_already_classified']}"
        )
        for unit_id in summary["skipped_unit_ids"]:
            lines.append(f"      {unit_id}")
        lines.append(
            "      re-derive these with --reclassify only if you mean to replace a "
            "model's six answers with one legacy label"
        )
    for label, count in summary["unmapped_by_label"].items():
        lines.append(f"      {label or '(missing unit_type)'}: {count}")
    lines.append("  resulting types:")
    for type_name, count in summary["type_histogram"].items():
        lines.append(f"      {type_name}: {count}")
    lines.append(f"  questions       : {summary['questions']}")
    lines.append(f"  quantitative    : {summary['quantitative']} (re-derived by code)")
    share = summary["unflagged_claim_share"]
    alarm = " ** above the 40% residual-absorption alarm **" if share > 0.40 else ""
    lines.append(
        f"  unflagged claims: {summary['unflagged_claims']} "
        f"({share:.1%} of all units){alarm}"
    )
    lines.append(f"  {summary['legacy_coverage']}")
    return "\n".join(lines)
