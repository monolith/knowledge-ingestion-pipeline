"""Tests for `kip validate` itself -- the gate the rest of the design leans on.

Eight of the validator's thirteen error branches could be deleted with the whole
suite still green: dangling ids, uncited assertions, a missing normalized
source, an excerpt absent from its source, a non-distinct auditor, a queue event
for an unapproved candidate, and a duplicate idempotency key. A gate nobody
tests is a gate nobody knows the state of, so each branch is corrupted here in
isolation and asserted on by its message.

The other half of this file covers the two ways the gate used to fail without
reporting anything: a bare KeyError on a record missing a required field (a CI
job reads a traceback as a crashed job, not a failed corpus), and ok:true on a
run id that does not exist or whose artifacts were deleted mid-run.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import pytest

from kip.artifacts import (
    RunContext,
    seal,
    text_hash,
    write_json_atomic,
    write_jsonl_atomic,
)
from kip.validate import validate_run

NORMALIZED = "Recall improved 8.2% in the sleep-extension group.\n"
EXCERPT = "Recall improved 8.2% in the sleep-extension group."



def _build_run(root: Path) -> RunContext:
    """A minimal but complete and internally consistent run.

    Complete on purpose: every corruption below is a single-field edit to this
    tree, so the only thing a failing assertion can be blaming is that field.
    """
    ctx = RunContext(run_id="run-v", root=root)
    rel = "01_normalized/src-doc/normalized.txt"
    path = ctx.run_dir / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(NORMALIZED, encoding="utf-8")

    write_jsonl_atomic(ctx.source_registry, [{
        "source_id": "src-doc",
        "filename": "doc.txt",
        "normalization_status": "success",
        "original_sha256": "",
        "normalized_path": rel,
    }])

    write_jsonl_atomic(ctx.units, [seal({
        "unit_id": "u-1",
        "source_id": "src-doc",
        "independence_group": "group-a",
        "canonical_statement": EXCERPT,
        "gates_fired": 1,
        "multi_fire": False,
        "modality": None,
        "flags": ["negative_result"],
        "quantitative": True,
        "node_kind": "unit",
        "entity_mentions": [],
        "classifier_model": "m",
        "decision": "keep", "grounding": "attributable",
        "evidence": [{
            "source_id": "src-doc",
            "normalized_path": rel,
            "normalized_line_start": 1,
            "normalized_line_end": 1,
            "normalized_char_start": 0,
            "normalized_char_end": len(EXCERPT),
            "excerpt": EXCERPT,
            "excerpt_sha256": text_hash(EXCERPT),
            "excerpt_verified": True,
        }],
    })])

    write_jsonl_atomic(ctx.clusters, [seal({
        "cluster_id": "cl-001", "topic_label": "t", "unit_ids": ["u-1"],
    })])
    write_jsonl_atomic(ctx.assessments, [seal({
        "assessment_id": "asmt-0001",
        "cluster_id": "cl-001",
        "canonical_claim": "c",
        "coarse_stance": "supports",
        "relationship_bucket": "singleton",
        "relationship_subtype": "singleton",
        "supporting_unit_ids": ["u-1"],
        "opposing_unit_ids": [],
        "qualifying_unit_ids": [],
        "uncertainty": "low",
        "synthesis": "s",
    })])

    candidate = {
        "candidate_id": "cand-001",
        "candidate_version": 1,
        "title": "T", "slug": "t", "knowledge_state": "supported", "summary": "s",
        "assertions": [{"text": "a", "assessment_ids": ["asmt-0001"]}],
        "source_unit_ids": ["u-1"],
        "suggested_operation": "create",
    }
    write_jsonl_atomic(ctx.candidates, [seal(dict(candidate))])
    write_jsonl_atomic(ctx.audits, [seal({
        "audit_id": "audit-cand-001",
        "candidate_id": "cand-001",
        "verdict": "pass",
        "auditor_distinct_from_proposer": True,
    })])
    approved = dict(candidate, candidate_id="cand-001-r1", candidate_version=2,
                    audit_ids=["audit-cand-001"])
    write_jsonl_atomic(ctx.approved, [seal(dict(approved))])
    write_jsonl_atomic(ctx.enqueue, [{
        "queue_event_id": "q-1",
        "idempotency_key": "k1",
        "candidate_id": "cand-001-r1",
        "audit_ids": ["audit-cand-001"],
        "payload": {},
    }])
    write_json_atomic(ctx.manifest, {"run_id": ctx.run_id, "spec_version": "3.1.0"})
    return ctx


def _rewrite(path: Path, mutate: Callable[[list[dict[str, Any]]], None]) -> None:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    mutate(records)
    write_jsonl_atomic(path, records)


def test_the_baseline_run_is_clean(tmp_path: Path):
    """Every corruption test below depends on this being true first."""
    report = validate_run(_build_run(tmp_path))
    assert report["ok"], report["errors"]


# --- One corruption per error branch ------------------------------------------

CORRUPTIONS: list[tuple[str, str, Callable[[RunContext], None]]] = [
    (
        "dangling cluster unit id",
        "unknown unit u-ghost",
        lambda ctx: _rewrite(ctx.clusters, lambda rs: rs[0].__setitem__("unit_ids", ["u-ghost"])),
    ),
    (
        "dangling assessment unit id",
        "unknown unit u-ghost",
        lambda ctx: _rewrite(
            ctx.assessments, lambda rs: rs[0].__setitem__("supporting_unit_ids", ["u-ghost"])
        ),
    ),
    (
        "assertion citing no assessment",
        "assertion without assessment_ids",
        lambda ctx: _rewrite(
            ctx.candidates,
            lambda rs: rs[0].__setitem__("assertions", [{"text": "a", "assessment_ids": []}]),
        ),
    ),
    (
        "assertion citing a nonexistent assessment",
        "unknown assessment asmt-9999",
        lambda ctx: _rewrite(
            ctx.candidates,
            lambda rs: rs[0].__setitem__(
                "assertions", [{"text": "a", "assessment_ids": ["asmt-9999"]}]
            ),
        ),
    ),
    (
        "candidate with no assertions at all",
        "no assertions",
        lambda ctx: _rewrite(ctx.candidates, lambda rs: rs[0].__setitem__("assertions", [])),
    ),
    (
        "candidate citing no source units",
        "no source_unit_ids",
        lambda ctx: _rewrite(ctx.candidates, lambda rs: rs[0].__setitem__("source_unit_ids", [])),
    ),
    (
        "audit for a candidate that does not exist",
        "unknown candidate",
        lambda ctx: _rewrite(ctx.audits, lambda rs: rs[0].__setitem__("candidate_id", "cand-999")),
    ),
    (
        "auditor was the proposer",
        "not distinct from the proposer",
        lambda ctx: _rewrite(
            ctx.audits, lambda rs: rs[0].__setitem__("auditor_distinct_from_proposer", False)
        ),
    ),
    (
        "queue event for an unapproved candidate",
        "candidate was never approved",
        lambda ctx: _rewrite(ctx.enqueue, lambda rs: rs[0].__setitem__("candidate_id", "cand-x")),
    ),
    (
        "two queue events sharing one idempotency key",
        "duplicate idempotency key",
        lambda ctx: _rewrite(
            ctx.enqueue, lambda rs: rs.append(dict(rs[0], queue_event_id="q-2"))
        ),
    ),
    (
        "queue event with no audit reference",
        "queued without an audit reference",
        lambda ctx: _rewrite(ctx.enqueue, lambda rs: rs[0].__setitem__("audit_ids", [])),
    ),
    (
        "excerpt that is not in the normalized source",
        "excerpt not present in normalized source",
        lambda ctx: _rewrite(
            ctx.units,
            lambda rs: rs[0]["evidence"][0].update(
                {"excerpt": "never written", "excerpt_sha256": text_hash("never written")}
            ),
        ),
    ),
    (
        "excerpt whose stored hash does not match its text",
        "excerpt hash mismatch",
        lambda ctx: _rewrite(
            ctx.units, lambda rs: rs[0]["evidence"][0].__setitem__("excerpt_sha256", "0" * 64)
        ),
    ),
    (
        "normalized source deleted from under the evidence",
        "normalized source missing",
        lambda ctx: (ctx.run_dir / "01_normalized/src-doc/normalized.txt").unlink(),
    ),
    (
        "hand-edited assertion behind an intact hash",
        "unit u-1: content hash mismatch",
        lambda ctx: _rewrite(
            ctx.units, lambda rs: rs[0].__setitem__("canonical_statement", "Recall did not improve.")
        ),
    ),
    (
        "hand-edited APPROVED candidate, the record the queue copies",
        "approved cand-001-r1: content hash mismatch",
        lambda ctx: _rewrite(
            ctx.approved,
            lambda rs: rs[0].update(
                {"title": "Definitively cures memory loss", "knowledge_state": "established"}
            ),
        ),
    ),
    (
        "two units sharing one unit_id",
        "duplicate unit_id",
        lambda ctx: _rewrite(ctx.units, lambda rs: rs.append(dict(rs[0]))),
    ),
]


@pytest.mark.parametrize(
    "description,expected,corrupt",
    CORRUPTIONS,
    ids=[c[0].replace(" ", "-") for c in CORRUPTIONS],
)
def test_validate_catches(tmp_path: Path, description: str, expected: str, corrupt):
    ctx = _build_run(tmp_path)
    corrupt(ctx)
    report = validate_run(ctx)
    assert not report["ok"], f"{description} was not caught"
    assert any(expected in error for error in report["errors"]), report["errors"]


# --- Failing loudly rather than crashing --------------------------------------

MISSING_ID_CASES = [
    ("units", "unit_id", "unit #0: missing unit_id"),
    ("clusters", "cluster_id", "cluster #0: missing cluster_id"),
    ("assessments", "assessment_id", "assessment #0: missing assessment_id"),
    ("candidates", "candidate_id", "candidate #0: missing candidate_id"),
]


@pytest.mark.parametrize("artifact,field,expected", MISSING_ID_CASES)
def test_a_record_missing_its_id_is_reported_not_raised(
    tmp_path: Path, artifact: str, field: str, expected: str
):
    """A KeyError traceback out of the gate is an outage, not a verdict."""
    ctx = _build_run(tmp_path)
    _rewrite(getattr(ctx, artifact), lambda rs: rs[0].pop(field))
    report = validate_run(ctx)  # must not raise
    assert not report["ok"]
    assert any(expected in error for error in report["errors"]), report["errors"]


def test_an_audit_missing_its_candidate_id_is_reported_not_raised(tmp_path: Path):
    ctx = _build_run(tmp_path)
    _rewrite(ctx.audits, lambda rs: rs[0].pop("candidate_id"))
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("unknown candidate" in error for error in report["errors"]), report["errors"]


def test_a_queue_event_missing_its_key_is_reported_not_raised(tmp_path: Path):
    ctx = _build_run(tmp_path)
    _rewrite(ctx.enqueue, lambda rs: rs[0].pop("idempotency_key"))
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("missing idempotency_key" in error for error in report["errors"]), report["errors"]


# --- Blindness: a run that is not there, or no longer whole -------------------


def test_a_run_that_was_never_created_is_not_ok(tmp_path: Path):
    """A typo'd run id used to return ok:true with exit code 0."""
    report = validate_run(RunContext(run_id="run-that-never-existed", root=tmp_path))
    assert not report["ok"]
    assert any("does not exist" in error for error in report["errors"]), report["errors"]


def test_deleting_an_upstream_artifact_is_not_a_clean_run(tmp_path: Path):
    """Half a corpus is not a valid corpus, however few errors are left in it."""
    ctx = _build_run(tmp_path)
    ctx.units.unlink()
    ctx.clusters.unlink()
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("upstream" in error for error in report["errors"]), report["errors"]


def test_a_hand_assembled_tree_is_checked_but_not_held_to_a_full_chain(tmp_path: Path):
    """Validating an artifact subset is legitimate; it is only marked as such.

    The chain check keys on run_manifest.json -- the orchestrator's own marker --
    so inspecting a units-only tree reports a warning rather than a missing pass.
    """
    ctx = RunContext(run_id="run-partial", root=tmp_path)
    write_jsonl_atomic(ctx.units, [seal({
        "unit_id": "u-1", "source_id": "s", "canonical_statement": "x",
        "evidence": [], "decision": "keep", "grounding": "attributable",
    })])
    report = validate_run(ctx)
    assert report["ok"], report["errors"]
    assert any("not produced by a completed pipeline run" in w for w in report["warnings"])


def test_a_fabricated_entity_mention_is_surfaced(tmp_path: Path):
    """Entity mentions are copied verbatim, so an absent surface was invented.

    They are excluded from content_sha256 by contract (they are in the derived
    block), so rewriting the whole list moves no hash and the integrity check
    stays silent. Locating each surface in the source is what closes that gap.
    """
    ctx = _build_run(tmp_path)
    _rewrite(ctx.units, lambda rs: rs[0].__setitem__(
        "entity_mentions", [{"surface": "Acme Corp (fabricated)", "line": 1}]
    ))
    report = validate_run(ctx)
    # A warning, not an error: the field is optional and best-effort, and the
    # wiki that consumes it resolves entities independently.
    assert report["ok"], report["errors"]
    assert any("do not appear in their source text" in w for w in report["warnings"])


def test_a_real_entity_mention_is_not_flagged(tmp_path: Path):
    ctx = _build_run(tmp_path)
    _rewrite(ctx.units, lambda rs: rs[0].__setitem__(
        "entity_mentions", [{"surface": "sleep-extension group", "line": 1}]
    ))
    assert not any(
        "do not appear" in w for w in validate_run(ctx)["warnings"]
    )


def test_an_edited_original_file_is_caught(tmp_path: Path):
    """The provenance chain must not end at a file that changed under it."""
    original = tmp_path / "doc.txt"
    original.write_text(NORMALIZED, encoding="utf-8")

    ctx = _build_run(tmp_path / "ws")
    _rewrite(ctx.source_registry, lambda rs: rs[0].update({
        "original_path": str(original),
        "original_sha256": text_hash(NORMALIZED),
    }))
    assert validate_run(ctx)["ok"], validate_run(ctx)["errors"]

    original.write_text("Something else was here all along.\n", encoding="utf-8")
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("original_sha256 recorded at intake" in e for e in report["errors"])


def test_two_originals_sharing_a_filename_are_compared_separately(tmp_path: Path):
    """The check must not look a source up by basename.

    Discovery is recursive, so q1/report.md and q2/report.md are two documents
    with one filename -- searching by name would compare each record against
    whichever copy the glob happened to return first and report a phantom edit.
    """
    for quarter, body in (("q1", "First.\n"), ("q2", "Second.\n")):
        (tmp_path / quarter).mkdir(parents=True)
        (tmp_path / quarter / "report.md").write_text(body, encoding="utf-8")

    ctx = _build_run(tmp_path / "ws")
    _rewrite(ctx.source_registry, lambda rs: rs.__setitem__(slice(None), [
        {**rs[0], "source_id": f"src-report-{quarter}", "filename": "report.md",
         "original_path": str(tmp_path / quarter / "report.md"),
         "original_sha256": text_hash(body)}
        for quarter, body in (("q1", "First.\n"), ("q2", "Second.\n"))
    ]))
    report = validate_run(ctx)
    assert not any("original_sha256" in e for e in report["errors"]), report["errors"]


def test_a_unit_cannot_claim_attributable_on_a_quote_that_was_never_found(tmp_path):
    """`grounding` is self-report, and self-report has already been measured
    unreliable once in this pipeline. So it is checked against the one thing
    that is mechanical: a unit claiming every clause traces to the source, while
    resting on an excerpt that could not be found in that source, is making a
    claim nobody can check.
    """
    from kip.validate import _check_grounding

    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}
    _check_grounding(
        [{
            "unit_id": "u-1",
            "grounding": "attributable",
            "evidence": [{"excerpt": "invented", "excerpt_verified": False, "role": "primary"}],
        }],
        errors, warnings, counts,
    )
    assert any("cannot be checked" in e for e in errors)


def test_unattributed_content_is_counted_for_review_not_failed(tmp_path):
    """A corpus carrying outside knowledge needs review, not deletion. Failing
    the run would destroy the evidence needed to do the review.
    """
    from kip.validate import _check_grounding

    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}
    _check_grounding(
        [{"unit_id": "u-1", "grounding": "unattributed_content", "evidence": []},
         {"unit_id": "u-2", "grounding": "attributable", "evidence": []}],
        errors, warnings, counts,
    )
    assert errors == []
    assert counts["units_unattributed"] == 1
    assert any("marked for review" in w for w in warnings)


def test_imported_context_without_a_supporting_citation_is_flagged(tmp_path):
    """Sufficiency licenses importing context; it does not license asserting it
    uncited. A unit that records an import but cites only its primary passage
    has gone beyond that passage with nothing licensing the difference.
    """
    from kip.validate import _check_grounding

    errors: list[str] = []
    warnings: list[str] = []
    counts: dict[str, int] = {}
    _check_grounding(
        [{
            "unit_id": "u-1",
            "grounding": "attributable",
            "decontextualization_note": "Imported the definitional precondition.",
            "evidence": [{"excerpt": "q", "excerpt_verified": True, "role": "primary"}],
        }],
        errors, warnings, counts,
    )
    assert any("cites no supporting excerpt" in w for w in warnings)
