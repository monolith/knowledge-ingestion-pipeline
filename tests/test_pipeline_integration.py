"""End-to-end wiring test for passes 1-6 using a scripted fake LLM.

This exercises every artifact hand-off, the audit's escalation logic, the
approved-version discipline, enqueueing, validation, and tracing -- without an
API key and without spending tokens. It verifies WIRING, not model quality.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from kip import assess, audit, candidates, enqueue, extract, normalize, route
from kip.artifacts import RunContext, read_jsonl
from kip.config import Config
from kip.trace import trace_leaf
from kip.validate import validate_run

SOURCE_A = """Sleep Extension and Memory: Randomized Trial
Delayed word recall improved 8.2% in the extension group versus 1.1% in controls.
The trial was not blinded and follow-up lasted four weeks.
"""

SOURCE_B = """Replication Study
The replication found no statistically significant overall effect on delayed recall.
"""


class FakeClient:
    """Returns canned, schema-shaped responses keyed by the calling pass.

    Deliberately dumb: it keys off marker text in the prompt rather than trying
    to be a model. The point is to prove the pipeline moves the right data
    between stages, so the responses are fixed and inspectable.
    """

    def __init__(self) -> None:
        self.calls: list[str] = []

    def complete_json(self, *, system: str, user: str, schema: dict, model: str, **kw) -> dict:
        if "molecular knowledge unit" in system or "GRANULARITY" in system:
            self.calls.append("extract")
            return self._extract(user)
        if "completeness" in system:
            self.calls.append("omission")
            return {"findings": [{
                "kind": "missing",
                "description": "Sample size is not represented as a unit.",
                "suggested_action": "add",
            }]}
        if "retrieval context" in system:
            self.calls.append("enrich")
            return {"context": "From a sleep-and-memory study.", "entities": ["sleep extension"]}
        if "label a cluster" in system:
            self.calls.append("label")
            return {"topic_label": "Sleep extension and delayed recall",
                    "routing_reason": "Shared intervention and outcome."}
        if "coarse stance" in system:
            self.calls.append("assess")
            return self._assess(user)
        if "proposed knowledge-base operations" in system:
            self.calls.append("plan")
            return self._plan(user)
        if "adversarial auditor" in system:
            self.calls.append("audit")
            return self._audit(user)
        raise AssertionError(f"unexpected call with system prompt: {system[:80]}")

    def _extract(self, user: str) -> dict:
        # Key off a SINGLE token: datamarking replaces spaces, so any
        # multi-word phrase is mangled by the time it reaches the model. That
        # mangling is the defense working -- the same thing happens to an
        # instruction hidden in an ingested document.
        if "8.2%" in user:
            return {"units": [{
                "unit_type": "quantitative_result",
                "canonical_statement": "Delayed word recall improved 8.2% in the sleep-extension group versus 1.1% in controls.",
                "decontextualization_note": "Named the intervention explicitly.",
                "evidence": [{
                    "excerpt": "Delayed word recall improved 8.2% in the extension group versus 1.1% in controls.",
                    "line_start": 2, "line_end": 2,
                }],
                "scores": {"specificity": 3, "retrieval_value": 3, "connection_value": 2,
                           "evidence_strength": 3, "novelty": 2},
                "decision": "keep",
            }]}
        return {"units": [{
            "unit_type": "null_result",
            "canonical_statement": "A replication found no statistically significant overall effect of sleep extension on delayed recall.",
            "decontextualization_note": "Named the intervention and outcome.",
            "evidence": [{
                "excerpt": "The replication found no statistically significant overall effect on delayed recall.",
                "line_start": 2, "line_end": 2,
            }],
            "scores": {"specificity": 3, "retrieval_value": 3, "connection_value": 3,
                       "evidence_strength": 3, "novelty": 2},
            "decision": "keep",
        }]}

    def _assess(self, user: str) -> dict:
        ids = [line.split()[0] for line in user.splitlines() if line.startswith("u-")]
        return {"assessments": [{
            "canonical_claim": "Sleep extension improves delayed recall in healthy adults.",
            "coarse_stance": "contradicts",
            "relationship_bucket": "contested",
            "relationship_subtype": "partially_contradicts",
            "subtype_confidence": 0.55,
            "supporting_unit_ids": ids[:1],
            "opposing_unit_ids": ids[1:2],
            "contradiction_evidence": [{"unit_id": ids[0] if ids else "u-x",
                                        "excerpt": "improved 8.2%"}],
            "uncertainty": "high",
            "synthesis": "One trial is positive; an independent replication is null.",
            "recommended_action": "Create a contested-evidence leaf.",
        }]}

    def _plan(self, user: str) -> dict:
        assessment_ids = [w.strip(":") for w in user.split() if w.startswith("asmt-")]
        # Deliberately OVERCONFIDENT so the audit has something real to catch.
        return {"candidates": [{
            "title": "Sleep extension improves delayed recall in adults",
            "knowledge_state": "established",
            "priority": 3,
            "summary": "Sleep extension improves delayed recall.",
            "assertions": [{"text": "Sleep extension improves delayed recall.",
                            "assessment_ids": assessment_ids[:1]}],
            "source_unit_ids": [],
            "suggested_operation": "create",
        }]}

    def _audit(self, user: str) -> dict:
        return {
            "verdict": "fix",
            "checks": {"coverage": "pass", "contradiction_handling": "fail",
                       "scope_fidelity": "warn", "source_independence": "pass",
                       "duplication": "pass"},
            "findings": ["The title presents contested evidence as established."],
            "required_fixes": ["Use a mixed-evidence title and the contested state."],
            "raw_source_escalation": [],
            "auditor_confidence": 0.7,
            "corrected_candidate": {
                "title": "Sleep extension and adult memory: mixed evidence",
                "knowledge_state": "contested",
                "summary": "One trial found improvement; an independent replication found none.",
                "assertions": [{"text": "One randomized trial reported improved delayed recall.",
                                "assessment_ids": ["asmt-0001"]}],
            },
        }


@pytest.fixture
def run(tmp_path: Path):
    sources = tmp_path / "src"
    sources.mkdir()
    (sources / "trial.txt").write_text(SOURCE_A, encoding="utf-8")
    (sources / "replication.txt").write_text(SOURCE_B, encoding="utf-8")

    ctx = RunContext(run_id="run-it", root=tmp_path / "ws")
    cfg = Config()
    client = FakeClient()

    registry = normalize.normalize_sources(ctx, sorted(sources.iterdir()))
    units = extract.extract_units(ctx, cfg, client, registry)
    from kip.artifacts import write_jsonl_atomic
    write_jsonl_atomic(ctx.units, units)
    clusters = route.route_and_cluster(ctx, cfg, client, units)
    assessments = assess.assess_clusters(ctx, cfg, client, units, clusters)
    proposals = candidates.plan_candidates(ctx, cfg, client, assessments)
    audits, approved = audit.audit_candidates(ctx, cfg, client, proposals, units, assessments)
    events = enqueue.enqueue_approved(ctx, approved)

    return {
        "ctx": ctx, "client": client, "registry": registry, "units": units,
        "clusters": clusters, "assessments": assessments, "candidates": proposals,
        "audits": audits, "approved": approved, "events": events,
    }


def test_every_pass_produces_artifacts(run):
    ctx = run["ctx"]
    for path in (ctx.source_registry, ctx.units, ctx.omissions, ctx.enriched_units,
                 ctx.clusters, ctx.assessments, ctx.candidates, ctx.audits,
                 ctx.approved, ctx.enqueue):
        assert path.exists(), f"{path.name} was not written"


def test_extraction_verifies_excerpts_verbatim(run):
    """Excerpts are located in the source at extraction time, not trusted."""
    for unit in run["units"]:
        for evidence in unit["evidence"]:
            assert evidence["excerpt_verified"], unit["unit_id"]
            assert evidence["normalized_char_start"] >= 0


def test_omission_findings_are_structured(run):
    """Spec §9.6: the E2E omission pass must emit per-finding records."""
    omissions = read_jsonl(run["ctx"].omissions)
    assert omissions
    assert {"kind", "description", "suggested_action"} <= set(omissions[0])


def test_enrichment_never_replaces_the_statement(run):
    """Spec §10.2: enrichment is an index-time artifact only."""
    enriched = read_jsonl(run["ctx"].enriched_units)
    units_by_id = {u["unit_id"]: u for u in run["units"]}
    for record in enriched:
        assert record["canonical_statement"] == units_by_id[record["unit_id"]]["canonical_statement"]
        assert record["enrichment_context"] in record["index_text"]


def test_independence_groups_are_recomputed_not_trusted(run):
    """Two separate sources = two independence groups, derived from metadata."""
    assessment = run["assessments"][0]
    assert len(assessment["independent_evidence_groups"]) == 2


def test_audit_catches_the_overconfident_candidate(run):
    """The whole point of Pass 5: an audit that actually changes the result."""
    proposal = run["candidates"][0]
    assert proposal["knowledge_state"] == "established"

    audit_record = run["audits"][0]
    assert audit_record["verdict"] == "fix"
    assert audit_record["auditor_distinct_from_proposer"] is True

    approved = run["approved"][0]
    assert approved["knowledge_state"] == "contested"
    assert "mixed evidence" in approved["title"]


def test_audit_produces_a_new_version_not_an_overwrite(run):
    """Spec §13.5: the original overconfident claim stays on disk."""
    original = run["candidates"][0]
    approved = run["approved"][0]
    assert approved["candidate_id"] != original["candidate_id"]
    assert approved["candidate_version"] == original["candidate_version"] + 1
    assert approved["supersedes"] == original["candidate_id"]
    assert read_jsonl(run["ctx"].candidates)[0]["knowledge_state"] == "established"


def test_only_approved_versions_reach_the_queue(run):
    approved_ids = {c["candidate_id"] for c in run["approved"]}
    for event in run["events"]:
        assert event["candidate_id"] in approved_ids
        assert event["audit_ids"]


def test_validation_passes_on_a_clean_run(run):
    report = validate_run(run["ctx"])
    assert report["ok"], report["errors"]


def test_validation_catches_a_tampered_excerpt(run):
    """Corrupt a stored excerpt; validation must notice."""
    ctx = run["ctx"]
    from kip.artifacts import write_jsonl_atomic
    units = read_jsonl(ctx.units)
    units[0]["evidence"][0]["excerpt"] = "a quote that was never in the source"
    write_jsonl_atomic(ctx.units, units)

    report = validate_run(ctx)
    assert not report["ok"]
    assert any("excerpt" in e for e in report["errors"])


def test_trace_reaches_the_original_file(run):
    """Spec §22.10: reconstruct the full chain from a queue event."""
    chain = trace_leaf(run["ctx"], run["events"][0]["queue_event_id"])
    assert chain is not None
    for expected in ("queue event", "candidate", "audit", "assessment", "unit",
                     "evidence", "original file"):
        assert expected in chain, f"missing {expected!r} in trace"


def test_trace_of_a_unit_shows_provenance(run):
    chain = trace_leaf(run["ctx"], run["units"][0]["unit_id"])
    assert "granularity_policy" in chain
    assert "original file" in chain


def test_pipeline_called_every_expected_pass(run):
    """Guard against a pass being silently skipped by a wiring change."""
    assert set(run["client"].calls) == {"extract", "omission", "enrich", "label", "assess", "plan", "audit"}
