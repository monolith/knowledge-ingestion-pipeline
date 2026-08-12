"""The retention guard: protect content synthesis is known to drop."""

from __future__ import annotations

import json

import pytest

from kip.retention import annotate, load_taxonomy, protected_ids


@pytest.fixture()
def taxonomy():
    tax = load_taxonomy()
    assert tax is not None, "the shipped default taxonomy must load"
    return tax


def _unit(uid: str, statement: str) -> dict:
    return {"unit_id": uid, "canonical_statement": statement, "decision": "keep"}


def test_a_definition_is_protected(taxonomy):
    hits = taxonomy.protections_for(
        "A drawdown is defined as the peak-to-trough decline in a portfolio's value."
    )
    assert [h["label"] for h in hits] == ["definition"]
    assert hits[0]["cue"], "the firing cue is recorded so a match can be audited"


def test_a_rule_and_a_prohibition_are_protected(taxonomy):
    assert "obligation" in [h["label"] for h in taxonomy.protections_for(
        "Clients must submit the reconciliation before close.")]
    assert "prohibition" in [h["label"] for h in taxonomy.protections_for(
        "Analysts must not exceed the intraday limit.")]


def test_an_ordinary_finding_is_not_protected(taxonomy):
    """The guard must not fire on everything, or it protects nothing."""
    assert taxonomy.protections_for(
        "Loser portfolios outperformed winner portfolios over the following three years."
    ) == []


def test_annotate_stamps_units_and_reports_the_count(taxonomy):
    units = [
        _unit("u-1", "A drawdown is defined as the peak-to-trough decline."),
        _unit("u-2", "Returns were higher in January than in other months."),
        _unit("u-3", "The model requires a positive-definite covariance matrix."),
    ]
    assert annotate(units, taxonomy) == 2
    assert protected_ids(units) == {"u-1", "u-3"}
    assert "protected_by" not in units[1]


def test_no_taxonomy_configured_is_not_an_error(monkeypatch, tmp_path):
    """Digestion must still work where no taxonomy is configured."""
    monkeypatch.setattr("kip.retention.DEFAULT_TAXONOMY", tmp_path / "absent.json")
    monkeypatch.delenv("KIP_TAXONOMY", raising=False)
    assert load_taxonomy() is None
    units = [_unit("u-1", "A drawdown is defined as the peak-to-trough decline.")]
    assert annotate(units, None) == 0


def test_a_configured_taxonomy_that_is_missing_does_raise(monkeypatch, tmp_path):
    """Silently running unprotected is the failure this module exists to stop."""
    monkeypatch.setenv("KIP_TAXONOMY", str(tmp_path / "nope.json"))
    with pytest.raises(FileNotFoundError):
        load_taxonomy()


def test_a_deployment_can_point_at_its_own_taxonomy(tmp_path):
    path = tmp_path / "custom.json"
    path.write_text(json.dumps({
        "taxonomy_version": "acme-v2",
        "source": "acme handbook",
        "protected": [{"label": "policy", "why": "x", "cues": [r"\bper policy\b"]}],
    }))
    tax = load_taxonomy(path)
    assert tax.version == "acme-v2"
    assert [h["label"] for h in tax.protections_for("Per policy, trades settle T+1.")] == ["policy"]
    assert tax.protections_for("A drawdown is defined as a decline.") == []


def test_a_protected_orphan_is_reported_separately_from_the_rest(tmp_path):
    """Losing a definition is the specific failure the taxonomy exists to stop.

    It must not be buried inside a general orphan count, or the count that
    matters is invisible in the count that does not.
    """
    import sys
    sys.path.insert(0, "tests")
    from test_validate import _build_run  # the shared clean-run fixture
    from kip.artifacts import read_jsonl, seal, write_jsonl_atomic
    from kip.validate import validate_run

    ctx = _build_run(tmp_path)
    base = read_jsonl(ctx.units)[0]
    base.pop("content_sha256", None)
    units = [
        seal({**base, "unit_id": "u-1", "decision": "keep"}),
        seal({**base, "unit_id": "u-2", "decision": "keep",
              "canonical_statement": "A drawdown is defined as a peak-to-trough decline.",
              "protected_by": [{"label": "definition", "cue": r"\bis defined as\b"}]}),
    ]
    write_jsonl_atomic(ctx.units, units)

    report = validate_run(ctx)
    assert report["counts"]["units_orphaned"] == 1
    assert report["counts"]["units_orphaned_protected"] == 1
    assert any("retention protection" in w for w in report["warnings"])
    assert any("u-2" in w for w in report["warnings"])
