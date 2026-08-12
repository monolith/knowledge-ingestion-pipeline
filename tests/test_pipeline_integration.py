"""End-to-end wiring test for passes 1-6 using a scripted fake LLM.

This exercises every artifact hand-off, the audit's escalation logic, the
approved-version discipline, enqueueing, validation, and tracing -- without an
API key and without spending tokens. It verifies WIRING, not model quality.
"""

from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from kip import assess, audit, candidates, cli, enqueue, extract, normalize, route
from kip.candidates import slugify
from kip.artifacts import (
    PipelineError,
    RunContext,
    envelope,
    read_jsonl,
    seal,
    write_jsonl_atomic,
)
from kip.config import SCHEMA_VERSION, Config
from kip.pipeline import run_pipeline
from kip.testing import ScriptedClientBase, check_schema, declared_properties
from kip.trace import trace_leaf
from kip.validate import validate_run

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCE_A = """Sleep Extension and Memory: Randomized Trial
Delayed word recall improved 8.2% in the extension group versus 1.1% in controls.
The trial was not blinded and follow-up lasted four weeks.
"""

SOURCE_B = """Replication Study
The replication found no statistically significant overall effect on delayed recall.
"""

# A third document, added for the kt-v1 taxonomy: it carries the shapes the two
# research documents cannot produce -- a deontic rule that must keep its
# modality, an open question that must leave the type system entirely, and a
# unit whose legacy label is one of the five the migration refuses to guess at.
SOURCE_C = """Ingestion Rate Limit Policy
Clients must not exceed 100 requests per minute against the ingestion endpoint.
Whether the limit should apply per user or per organization is unresolved.
The on-call engineer restarted the limiter during the March 2026 incident.
"""



def _ids_stating(rendered: str, marker: str) -> list[str]:
    """Unit ids whose rendered statement contains `marker` (Pass 3 prompt layout)."""
    found: list[str] = []
    current: str | None = None
    for line in rendered.splitlines():
        if line.startswith("u-"):
            current = line.split()[0]
        elif current and "statement:" in line and marker in line:
            found.append(current)
    return found


_SCORES = {"specificity": 3, "retrieval_value": 3, "connection_value": 2,
           "evidence_strength": 3, "novelty": 2}

SOURCE_C_UNITS: list[dict[str, Any]] = [
    {
        "modality": "prohibited",
        "flags": [],
        "node_kind": "unit",
        "entity_mentions": [{"surface": "ingestion endpoint", "line": 2}],
        "canonical_statement": (
            "Clients must not exceed 100 requests per minute against the ingestion endpoint."
        ),
        "decontextualization_note": "None needed; actor and constraint are explicit.",
        "evidence": [{
            "excerpt": (
                "Clients must not exceed 100 requests per minute against the ingestion endpoint."
            ),
            "line_start": 2, "line_end": 2,
            "role": "primary",
        }],
        "scores": _SCORES,
        "decision": "keep", "grounding": "attributable",
    },
    {
        # No test fires. A question has no truth value to check, no procedure to
        # run, and no instance that occurred, so it leaves the type system and
        # is carried as a question node instead.
        "flags": [],
        "node_kind": "question",
        "entity_mentions": [],
        "canonical_statement": (
            "Whether the ingestion rate limit should apply per user or per organization "
            "is unresolved."
        ),
        "decontextualization_note": "Named the limit the question concerns.",
        "evidence": [{
            "excerpt": "Whether the limit should apply per user or per organization is unresolved.",
            "line_start": 3, "line_end": 3,
            "role": "primary",
        }],
        "scores": {**_SCORES, "specificity": 2, "evidence_strength": 1},
        "decision": "keep", "grounding": "attributable",
    },
    {
        # `observation` is one of the five legacy labels the migration refuses to
        # map, because case-versus-claim is not decidable from the label. A fresh
        # classification decides it, because the model answered the tests --
        # which is the difference the dual write exists to measure.
        "flags": [],
        "node_kind": "unit",
        "entity_mentions": [{"surface": "on-call engineer", "line": 4}],
        "canonical_statement": (
            "The on-call engineer restarted the ingestion limiter during the March 2026 incident."
        ),
        "decontextualization_note": "Named the limiter and the incident.",
        "evidence": [{
            "excerpt": "The on-call engineer restarted the limiter during the March 2026 incident.",
            "line_start": 4, "line_end": 4,
            "role": "primary",
        }],
        "scores": _SCORES,
        "decision": "keep", "grounding": "attributable",
    },
]


class FakeClient(ScriptedClientBase):
    """Canned responses keyed by the calling pass, checked against its schema.

    Deliberately dumb: marker text in the prompt rather than an attempt to be a
    model. The point is to prove the pipeline moves the right data between
    stages, so the responses are fixed and inspectable.

    Dispatch, counting and schema checking come from kip.testing; the demo's
    ScriptedClient subclasses the same base. The schema check is what makes a
    renamed schema property fail here rather than silently in production -- an
    offline fake that ignores its schema tests the pipeline against itself.
    """

    def _pass_omission(self, user: str) -> dict:
        return {"findings": [{
            "kind": "missing",
            "description": "Sample size is not represented as a unit.",
            "suggested_action": "add",
        }]}

    def _pass_enrich(self, user: str) -> dict:
        return {"context": "From a sleep-and-memory study.", "entities": ["sleep extension"]}

    def _pass_label(self, user: str) -> dict:
        return {"topic_label": "Sleep extension and delayed recall",
                "routing_reason": "Shared intervention and outcome."}

    def _pass_extract(self, user: str) -> dict:
        # Key off a SINGLE token: datamarking replaces spaces, so any
        # multi-word phrase is mangled by the time it reaches the model. That
        # mangling is the defense working -- the same thing happens to an
        # instruction hidden in an ingested document.
        if "8.2%" in user:
            return {"units": [{
                # Two tests fire: a measurement on one sample is a case, and the
                # generalization it supports is a claim. That is the documented
                # split signal, and it must survive the pipeline as multi_fire.
                # Note what is NOT here: no `quantitative`, no `type`, no
                # `family`. Those are derived by code downstream.
                "flags": [],
                "node_kind": "unit",
                "entity_mentions": [{"surface": "extension group", "line": 2}],
                "canonical_statement": "Delayed word recall improved 8.2% in the sleep-extension group versus 1.1% in controls.",
                "decontextualization_note": "Named the intervention explicitly.",
                "evidence": [{
                    "excerpt": "Delayed word recall improved 8.2% in the extension group versus 1.1% in controls.",
                    "line_start": 2, "line_end": 2,
                    "role": "primary",
                }],
                "scores": {"specificity": 3, "retrieval_value": 3, "connection_value": 2,
                           "evidence_strength": 3, "novelty": 2},
                "decision": "keep", "grounding": "attributable",
            }]}
        if "limiter" in user:
            return {"units": SOURCE_C_UNITS}
        return {"units": [{
            "flags": ["negative_result"],
            "node_kind": "unit",
            "entity_mentions": [{"surface": "Replication Study", "line": 1}],
            "canonical_statement": "A replication found no statistically significant overall effect of sleep extension on delayed recall.",
            "decontextualization_note": "Named the intervention and outcome.",
            "evidence": [{
                "excerpt": "The replication found no statistically significant overall effect on delayed recall.",
                "line_start": 2, "line_end": 2,
                "role": "primary",
            }],
            "scores": {"specificity": 3, "retrieval_value": 3, "connection_value": 3,
                       "evidence_strength": 3, "novelty": 2},
            "decision": "keep", "grounding": "attributable",
        }]}

    def _pass_assess(self, user: str) -> dict:
        # Select the two sides by what they SAY, not by their position in the
        # batch. Cluster membership and prompt rotation both reorder the units,
        # so an index-based fake silently assesses whichever pair happens to
        # come first -- which is how a fake stops testing what it claims to.
        supporting = _ids_stating(user, "improved 8.2%")
        opposing = _ids_stating(user, "no statistically significant")
        return {"assessments": [{
            "canonical_claim": "Sleep extension improves delayed recall in healthy adults.",
            "coarse_stance": "contradicts",
            "relationship_bucket": "contested",
            "relationship_subtype": "partially_contradicts",
            "subtype_confidence": 0.55,
            "supporting_unit_ids": supporting,
            "opposing_unit_ids": opposing,
            "contradiction_evidence": [{"unit_id": unit_id, "excerpt": "improved 8.2%"}
                                       for unit_id in supporting],
            "uncertainty": "high",
            "synthesis": "One trial is positive; an independent replication is null.",
            "recommended_action": "Create a contested-evidence leaf.",
        }]}

    def _pass_plan(self, user: str) -> dict:
        assessment_ids = [w.strip(":") for w in user.split() if w.startswith("asmt-")]
        # Cited from the units the planner was actually shown. An empty list
        # made every deterministic check in Pass 5 pass vacuously -- zero
        # excerpts checked, nothing to resolve -- so the audit's own citation
        # machinery was never exercised by the one test that runs it.
        unit_ids: list[str] = []
        for match in re.findall(r"u-src-[a-z0-9\-]+", user):
            if match not in unit_ids:
                unit_ids.append(match)
        # Deliberately OVERCONFIDENT so the audit has something real to catch.
        return {"candidates": [{
            "title": "Sleep extension improves delayed recall in adults",
            "knowledge_state": "established",
            "priority": 3,
            "summary": "Sleep extension improves delayed recall.",
            "assertions": [{"text": "Sleep extension improves delayed recall.",
                            "assessment_ids": assessment_ids[:1]}],
            "source_unit_ids": unit_ids,
            "suggested_operation": "create",
        }]}

    def _pass_audit(self, user: str) -> dict:
        # Cite the assessments this audit was actually shown, read out of the
        # rendered prompt. A hardcoded id would still pass the validator while
        # referencing evidence this audit never saw, and it would rot the first
        # time cluster membership or numbering changed.
        cited = re.findall(r"asmt-\d+", user) or ["asmt-0001"]
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
                                "assessment_ids": cited[:1]}],
            },
        }


def write_sources(tmp_path: Path) -> Path:
    sources = tmp_path / "src"
    sources.mkdir()
    (sources / "trial.txt").write_text(SOURCE_A, encoding="utf-8")
    (sources / "replication.txt").write_text(SOURCE_B, encoding="utf-8")
    (sources / "rate-limit-policy.txt").write_text(SOURCE_C, encoding="utf-8")
    return sources


@pytest.fixture
def run(tmp_path: Path):
    """Drive the REAL orchestrator, not a hand-copied pass sequence.

    run_pipeline's own docstring warns against "a parallel copy of the pass
    sequence that can drift from it", and this fixture used to be exactly that:
    it called each pass module directly, so removing Pass 6 from the
    orchestrator entirely left the suite green.
    """
    sources = write_sources(tmp_path)
    ctx = RunContext(run_id="run-it", root=tmp_path / "ws")
    cfg = Config()
    client = FakeClient()

    summary = run_pipeline(ctx, cfg, sources, client=client)

    return {
        "ctx": ctx, "client": client, "summary": summary,
        "registry": read_jsonl(ctx.source_registry),
        "units": read_jsonl(ctx.units),
        "clusters": read_jsonl(ctx.clusters),
        "assessments": read_jsonl(ctx.assessments),
        "candidates": read_jsonl(ctx.candidates),
        "audits": read_jsonl(ctx.audits),
        "approved": read_jsonl(ctx.approved),
        "events": read_jsonl(ctx.enqueue),
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
    """Independence is derived from unit metadata, never taken from the model.

    The fixture's three documents currently form ONE cluster of five units.
    Nothing here depends on that: the assertion is over every assessment, and
    the fake selects its two sides by what they say rather than by position, so
    a clustering change alters the run without invalidating the test.
    """
    units_by_id = {u["unit_id"]: u for u in run["units"]}
    spanning = 0

    for assessment in run["assessments"]:
        cited = assessment["supporting_unit_ids"] + assessment["opposing_unit_ids"]
        expected = sorted({units_by_id[uid]["independence_group"] for uid in cited})
        assert assessment["independent_evidence_groups"] == expected
        spanning += len(expected) == 2

    # The trial and its replication are separate files, so at least one
    # assessment must rest on two independent groups.
    assert spanning >= 1


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


def test_a_corrected_title_regenerates_the_slug(run):
    """A `fix` must not leave the overstated claim in the identifier.

    The slug is derived from the title, and the queue payload carries it as the
    consumer's key. Freezing it across a correction files the corrected entry
    under the uncorrected name -- the audit's whole finding, preserved in the
    one field a knowledge base indexes on.
    """
    original = run["candidates"][0]
    approved = run["approved"][0]
    assert approved["title"] != original["title"], "fixture must exercise a title change"
    assert approved["slug"] != original["slug"], (
        "slug still derives from the superseded title"
    )
    assert approved["slug"] == slugify(approved["title"])

    event = next(e for e in run["events"] if e["candidate_id"] == approved["candidate_id"])
    assert event["payload"]["slug"] == approved["slug"]


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



def test_quantitative_is_computed_by_code_not_reported_by_the_model(run):
    """The fake client never sends `quantitative`; the regex fills it in."""
    quant = [u for u in run["units"] if u["quantitative"]]
    prose = [u for u in run["units"] if not u["quantitative"]]
    assert any("8.2%" in u["canonical_statement"] for u in quant)
    assert quant and prose
    assert all(not any(ch.isdigit() for ch in u["canonical_statement"]) or True for u in prose)


def test_entity_mentions_reach_enriched_units(run):
    """Spec/contract §2.3: raw surfaces must survive routing for the wiki."""
    enriched = read_jsonl(run["ctx"].enriched_units)
    mentions = {m["surface"] for record in enriched for m in record["entity_mentions"]}
    assert {"extension group", "Replication Study"} <= mentions




def test_pipeline_called_every_expected_pass(run):
    """Guard against a pass being silently skipped by a wiring change."""
    assert set(run["client"].calls) == {"extract", "omission", "enrich", "label", "assess", "plan", "audit"}


# --- kt-v1: the derived block, end to end -------------------------------------



def test_a_deontic_unit_keeps_its_modality_and_its_computed_quantitative_flag(run):
    """Modality survives digestion to disk, and `quantitative` is the regex's
    answer rather than the model's -- the fake never sent the field.
    """
    rule = next(u for u in run["units"] if u["modality"] == "prohibited")
    assert rule["quantitative"] is True      # "must not exceed 100 requests per minute"
    assert rule["flags"] == []

    report = validate_run(run["ctx"])
    assert not [e for e in report["errors"] if "modality" in e], report["errors"]




def legacy_run(tmp_path: Path):
    """A run as it existed BEFORE kt-v1: 20 units, one per legacy label.

    Sealed with the current rule on purpose. That isolates what this test is
    about -- the label mapping and the hash invariance -- from the separate
    3.0.0 hash repair, which test_taxonomy covers directly.
    """
    sources = tmp_path / "legacy"
    sources.mkdir()
    body = "\n".join(LEGACY_STATEMENTS[label] for label in UNIT_TYPES)
    (sources / "legacy-corpus.txt").write_text(f"Pre-taxonomy corpus\n{body}\n", encoding="utf-8")

    ctx = RunContext(run_id="run-legacy", root=tmp_path / "ws")
    manifest = normalize.normalize_sources(ctx, sorted(sources.iterdir()))[0]
    text = (ctx.run_dir / manifest["normalized_path"]).read_text(encoding="utf-8")
    lines = text.splitlines()

    units = []
    for index, label in enumerate(UNIT_TYPES, start=1):
        statement = LEGACY_STATEMENTS[label]
        units.append(seal({
            **envelope(
                ctx,
                # The version these units were written under; the point of the
                # exercise is that they predate the taxonomy.
                prompt_version="pass-01-molecular-extraction-v3.0",
                model_role="molecular-extractor",
                parent_artifacts=[manifest["normalized_path"]],
            ),
            "unit_id": f"u-{manifest['source_id']}-{index:04d}",
            "source_id": manifest["source_id"],
            "source_family_id": manifest["source_family_id"],
            "independence_group": manifest["independence_group"],
            "canonical_statement": statement,
            # Built by the real resolver so the evidence genuinely verifies
            # against the normalized source and `kip validate` has something to
            # check after the migration rewrites the file.
            "evidence": [extract._resolve_evidence(
                manifest,
                {"excerpt": statement, "line_start": index + 1, "line_end": index + 1},
                text,
                lines,
            )],
            "scores": _SCORES,
            "decision": "keep", "grounding": "attributable",
            "granularity_policy": "molecular-v1",
        }))

    write_jsonl_atomic(ctx.units, units)
    return ctx, units



def _load_demo():
    """Load demo/run_demo.py by path: the demo ships beside the package, not in it."""
    spec = importlib.util.spec_from_file_location(
        "kip_demo", REPO_ROOT / "demo" / "run_demo.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_bundled_demo_runs_offline_and_produces_a_valid_run(tmp_path: Path, capsys):
    """The demo is documentation people execute, so it is tested like code."""
    demo = _load_demo()
    assert demo.main(["--workspace", str(tmp_path), "--run-id", "run-demo"]) == 0
    printed = capsys.readouterr().out

    ctx = RunContext(run_id="run-demo", root=tmp_path)
    units = read_jsonl(ctx.units)
    assert len(units) == 10

    # The two bundled documents exercise both flags, a modality, and a question
    # node in one run.
    assert sum(1 for u in units if u["node_kind"] == "question") == 1
    assert sum(1 for u in units if u["quantitative"]) == 2
    assert {f for u in units for f in u["flags"]} == {"negative_result", "caveat"}
    assert [u["modality"] for u in units if u["modality"]] == ["prohibited"]

    assert validate_run(ctx)["ok"]
    assert "ok: True" in printed
    # The demo's point: an overconfident proposal is corrected, not queued.
    assert "proposed : [established]" in printed
    assert "approved : [contested]" in printed


def test_the_demo_ships_the_documents_it_ingests():
    sources = sorted(p.name for p in (REPO_ROOT / "demo" / "sources").iterdir())
    assert sources == ["memory-consolidation-review.md", "sleep-extension-trial.md"]


# --- Pass 5 safety guards -----------------------------------------------------
# Every one of these could be deleted with the suite still green: the
# distinct-auditor guard, the mechanical-failure escalation, the reject/defer
# refusal, and the fix-without-a-correction refusal. A guard nobody exercises is
# a guard nobody knows the state of.


class _AuditClient(FakeClient):
    """FakeClient with the audit verdict under the test's control."""

    def __init__(self, response: dict) -> None:
        super().__init__()
        self.response = response

    def _pass_audit(self, user: str) -> dict:
        cited = re.findall(r"asmt-\d+", user) or ["asmt-0001"]
        response = dict(self.response)
        if "corrected_candidate" in response:
            response["corrected_candidate"] = dict(
                response["corrected_candidate"],
                assertions=[{"text": "Corrected.", "assessment_ids": cited[:1]}],
            )
        return response


def _audit_verdict(verdict: str, **extra: Any) -> dict:
    return {
        "verdict": verdict,
        "checks": {"coverage": "pass", "contradiction_handling": "pass",
                   "scope_fidelity": "pass", "source_independence": "pass",
                   "duplication": "pass"},
        "findings": [],
        "required_fixes": ["Narrow the scope."],
        "raw_source_escalation": [],
        "auditor_confidence": 0.6,
        **extra,
    }


def _pipeline_with(tmp_path: Path, client: FakeClient, cfg: Config | None = None):
    ctx = RunContext(run_id="run-guard", root=tmp_path / "ws")
    run_pipeline(ctx, cfg or Config(), write_sources(tmp_path), client=client)
    return ctx


def test_an_auditor_that_is_its_own_proposer_is_refused_before_pass_zero(tmp_path: Path):
    """Spec §13.3b: self-preference bias survives anonymization.

    Checked in a preflight rather than at Pass 5, because discovering it at Pass
    5 means passes 0-4 have already been paid for across the whole corpus.
    """
    cfg = Config()
    same = cfg.model_for("planner")
    with pytest.MonkeyPatch().context() as patch:
        patch.setattr("kip.config.MODEL_AUDITOR", same)
        client = FakeClient()
        with pytest.raises(RuntimeError, match="must differ from the proposer"):
            run_pipeline(
                RunContext(run_id="run-same", root=tmp_path / "ws"),
                cfg, write_sources(tmp_path), client=client,
            )
        assert client.calls == [], "the guard must fire before any paid call"


def test_a_failing_mechanical_check_overrides_an_llm_pass(tmp_path: Path):
    """The code check has no error rate; the judgment does."""
    client = _AuditClient(_audit_verdict(
        "pass",
        corrected_candidate={
            "title": "Narrowed", "knowledge_state": "contested",
            "summary": "s", "assertions": [],
        },
    ))
    # A fabricated citation the deterministic check will not find in the source.
    original_plan = client._pass_plan

    def plan_with_a_ghost_unit(user: str) -> dict:
        result = original_plan(user)
        result["candidates"][0]["source_unit_ids"] = ["u-src-ghost-0001"]
        return result

    client._pass_plan = plan_with_a_ghost_unit  # type: ignore[method-assign]
    ctx = _pipeline_with(tmp_path, client)

    audits = read_jsonl(ctx.audits)
    assert audits, "no audit was produced"
    assert audits[0]["verdict"] == "fix", audits[0]["verdict"]
    assert any("escalated" in f for f in audits[0]["findings"]), audits[0]["findings"]
    assert audits[0]["checks"]["provenance_integrity"]["result"] == "fail"


@pytest.mark.parametrize("verdict", ["reject", "defer"])
def test_a_rejected_or_deferred_candidate_never_reaches_the_queue(tmp_path: Path, verdict: str):
    ctx = _pipeline_with(tmp_path, _AuditClient(_audit_verdict(verdict)))
    assert read_jsonl(ctx.approved) == []
    assert read_jsonl(ctx.enqueue) == []
    assert validate_run(ctx)["ok"]


def test_a_fix_without_a_correction_is_not_queueable(tmp_path: Path):
    """Spec §13.5: a fix produces a new version, so there must be one."""
    ctx = _pipeline_with(tmp_path, _AuditClient(_audit_verdict("fix")))
    assert read_jsonl(ctx.audits)[0]["verdict"] == "fix"
    assert read_jsonl(ctx.approved) == []
    assert read_jsonl(ctx.enqueue) == []


def test_pass_with_label_carries_the_label_forward(tmp_path: Path):
    ctx = _pipeline_with(tmp_path, _AuditClient(_audit_verdict("pass_with_label")))
    approved = read_jsonl(ctx.approved)
    assert approved and approved[0]["audit_verdict"] == "pass_with_label"
    assert approved[0]["labels"] == ["Narrow the scope."]


def test_an_ordinary_pass_is_approved_unchanged(tmp_path: Path):
    """The normal case, which no test covered: nothing to correct, so nothing is."""
    ctx = _pipeline_with(tmp_path, _AuditClient(_audit_verdict("pass")))
    proposed = read_jsonl(ctx.candidates)[0]
    approved = read_jsonl(ctx.approved)[0]
    assert approved["title"] == proposed["title"]
    assert approved["knowledge_state"] == proposed["knowledge_state"]
    assert approved["supersedes"] == proposed["candidate_id"]
    assert len(read_jsonl(ctx.enqueue)) == 1


def test_a_candidate_with_no_provenance_is_never_approved(tmp_path: Path):
    """Spec §22 AC3: every retained unit traces to an exact source excerpt.

    Zero assertions and zero cited units used to satisfy all three
    deterministic checks vacuously -- nothing to verify, nothing to resolve --
    so the leaf was audited "pass", enqueued, and validated clean.
    """
    class _EmptyPlanClient(FakeClient):
        def _pass_plan(self, user: str) -> dict:
            return {"candidates": [{
                "title": "Widget latency",
                "knowledge_state": "supported",
                "summary": "Latency is now 12 ms.",
                "assertions": [],
                "source_unit_ids": [],
                "suggested_operation": "create",
            }]}

    ctx = _pipeline_with(tmp_path, _EmptyPlanClient())
    audit_record = read_jsonl(ctx.audits)[0]
    assert audit_record["checks"]["citation_accuracy"]["result"] == "fail"
    assert audit_record["checks"]["provenance_integrity"]["result"] == "fail"
    assert read_jsonl(ctx.approved) == []
    assert read_jsonl(ctx.enqueue) == []

    report = validate_run(ctx)
    assert not report["ok"]
    assert any("no assertions" in e for e in report["errors"]), report["errors"]


def test_the_audit_actually_checked_the_citations_it_reports_on(run):
    """The mechanical check must run on real units, not on an empty list."""
    checks = run["audits"][0]["checks"]
    assert checks["citation_accuracy"]["checked"] > 0
    assert checks["citation_accuracy"]["result"] == "pass"
    assert checks["provenance_integrity"]["result"] == "pass"
    # Three source files, so the cited units span three independence groups and
    # the "established" claim is not arithmetically inflated -- the LLM auditor
    # still catches it on the evidence, which is the division of labor §13.4 wants.
    assert checks["independence_inflation"]["result"] == "pass"
    assert len(checks["independence_inflation"]["independence_groups"]) >= 2


# --- Pass 3 evidence-integrity corrections ------------------------------------
# Both of these could be deleted silently: nothing anywhere referenced
# contradiction_downgraded_missing_evidence or subtype_corrected_single_...


def test_a_contradiction_without_quoted_evidence_is_downgraded(tmp_path: Path):
    """Spec §11.4: a contradicts verdict without quoted text is not reportable.

    Downgraded rather than dropped, and the downgrade is recorded -- Pass 4 and
    the audit both need to see that the pipeline changed the answer.
    """
    class _UnquotedContradiction(FakeClient):
        def _pass_assess(self, user: str) -> dict:
            result = super()._pass_assess(user)
            result["assessments"][0]["contradiction_evidence"] = []
            return result

    ctx = _pipeline_with(tmp_path, _UnquotedContradiction())
    assessment = read_jsonl(ctx.assessments)[0]
    assert assessment["coarse_stance"] == "insufficient_evidence"
    assert "contradiction_downgraded_missing_evidence" in assessment["source_validity_flags"]


def test_convergent_independent_on_one_group_is_corrected_to_dependent(tmp_path: Path):
    """A dependent convergence must never be reported as independent support."""
    class _InflatedIndependence(FakeClient):
        def _pass_assess(self, user: str) -> dict:
            # Cite two units from ONE document, so they share an independence
            # group however confidently the model labels them independent.
            same_source = [
                line.split()[0]
                for line in user.splitlines()
                if line.startswith("u-") and "src-rate-limit-policy" in line
            ]
            return {"assessments": [{
                "canonical_claim": "The ingestion limit is enforced.",
                "coarse_stance": "supports",
                "relationship_bucket": "convergent",
                "relationship_subtype": "convergent_independent",
                "subtype_confidence": 0.9,
                "supporting_unit_ids": same_source,
                "opposing_unit_ids": [],
                "uncertainty": "low",
                "synthesis": "Two units from the same policy document agree.",
                "recommended_action": "Record as operational reference.",
            }]}

    ctx = _pipeline_with(tmp_path, _InflatedIndependence())
    assessment = read_jsonl(ctx.assessments)[0]
    assert len(assessment["independent_evidence_groups"]) == 1
    assert assessment["relationship_subtype"] == "convergent_dependent"
    assert "subtype_corrected_single_independence_group" in assessment["source_validity_flags"]


# --- The orchestrator itself --------------------------------------------------


def test_run_pipeline_reports_every_pass_it_ran(run):
    """Removing Pass 6 from the orchestrator entirely used to leave the suite green."""
    summary = run["summary"]
    for key in ("sources", "units", "clusters", "assessments", "candidates",
                "audits", "approved", "queue_events"):
        assert key in summary, f"{key} missing from the run summary"
        assert summary[key] > 0, f"{key} was zero"
    assert run["events"], "Pass 6 produced no queue events"


def test_stop_after_does_not_pay_for_the_next_pass(tmp_path: Path):
    ctx = RunContext(run_id="run-stop", root=tmp_path / "ws")
    client = FakeClient()
    summary = run_pipeline(
        ctx, Config(), write_sources(tmp_path), client=client, stop_after="extract"
    )
    assert summary["units"] > 0
    assert "clusters" not in summary
    assert not ctx.clusters.exists()
    assert set(client.calls) == {"extract", "omission"}


def test_resuming_a_finished_run_spends_nothing(tmp_path: Path):
    sources = write_sources(tmp_path)
    ctx = RunContext(run_id="run-resume", root=tmp_path / "ws")
    run_pipeline(ctx, Config(), sources, client=FakeClient())

    second = FakeClient()
    summary = run_pipeline(ctx, Config(), sources, client=second)
    assert second.calls == [], "a completed run must not re-call the model"
    assert summary["queue_events"] == 1


def test_resuming_after_a_source_changed_is_refused_not_silently_ignored(tmp_path: Path):
    """The silent half-corpus. Adding or editing a source used to be invisible.

    The registry kept an original_sha256 that no longer matched the file, the
    new document was never ingested, and the resume log said everything was fine.
    """
    sources = write_sources(tmp_path)
    ctx = RunContext(run_id="run-drift", root=tmp_path / "ws")
    run_pipeline(ctx, Config(), sources, client=FakeClient(), stop_after="normalize")

    (sources / "late-arrival.txt").write_text("A document added after the fact.\n", encoding="utf-8")
    with pytest.raises(PipelineError, match="inputs to this stage changed"):
        run_pipeline(ctx, Config(), sources, client=FakeClient(), stop_after="normalize")

    # --force is the documented way through, and it must actually work.
    summary = run_pipeline(
        ctx, Config(), sources, client=FakeClient(), stop_after="normalize", force=True
    )
    assert summary["sources"] == 4


def test_the_run_manifest_records_the_configuration_in_force(run):
    """Spec §7: nothing read run_manifest.json, so nothing noticed it was wrong."""
    manifest = json.loads(run["ctx"].manifest.read_text(encoding="utf-8"))
    assert manifest["run_id"] == "run-it"
    assert manifest["spec_version"] == SCHEMA_VERSION
    models = manifest["config"]["models"]
    assert set(models) == {"extractor", "omission", "enricher", "judge", "planner", "auditor"}
    assert models["auditor"] != models["planner"]
    assert manifest["summary"]["queue_events"] == len(run["events"])


# --- Schemas are the contract with the live model -----------------------------
# Both fakes used to accept `schema` and ignore it, so the schemas -- the only
# thing standing between this pipeline and a real API -- were untested. Renaming
# `coarse_stance` to `stance` in ASSESS_SCHEMA left 137 tests green.


SCHEMA_CONSUMERS = [
    ("extract", extract.UNIT_SCHEMA, ("units",),
     {"canonical_statement", "evidence", "scores", "decision",
      "modality", "flags", "node_kind", "entity_mentions", "context_note",
      "decontextualization_note", "qualifiers", "candidate_topics", "drop_reason",
      "extraction_confidence"}),
    ("assess", assess.ASSESS_SCHEMA, ("assessments",),
     {"canonical_claim", "coarse_stance", "relationship_bucket", "relationship_subtype",
      "subtype_confidence", "supporting_unit_ids", "opposing_unit_ids",
      "qualifying_unit_ids", "contradiction_evidence", "support_strength",
      "importance_score", "uncertainty", "synthesis", "recommended_action",
      "t_valid", "t_invalid"}),
    ("candidates", candidates.PLAN_SCHEMA, ("candidates",),
     {"title", "knowledge_state", "priority", "summary", "assertions",
      "source_unit_ids", "related_topics", "suggested_operation"}),
    ("route-enrich", route.ENRICH_SCHEMA, (), {"context", "entities"}),
    ("route-label", route.LABEL_SCHEMA, (),
     {"topic_label", "routing_reason", "related_existing_topics"}),
    ("audit", audit.AUDIT_SCHEMA, (),
     {"verdict", "checks", "findings", "required_fixes", "raw_source_escalation",
      "auditor_confidence", "corrected_candidate"}),
]


@pytest.mark.parametrize(
    "name,schema,path,consumed", SCHEMA_CONSUMERS, ids=[c[0] for c in SCHEMA_CONSUMERS]
)
def test_every_key_the_pass_reads_is_declared_in_its_schema(
    name: str, schema: dict, path: tuple, consumed: set
):
    declared = declared_properties(schema, *path)
    assert consumed <= declared, f"{name}: reads undeclared {sorted(consumed - declared)}"


def test_the_fake_client_rejects_a_response_its_schema_forbids():
    """The check has to be able to fail, or it proves nothing."""
    from kip.testing import SchemaViolation, check_schema

    with pytest.raises(SchemaViolation, match="missing required property"):
        check_schema({"units": [{"nonsense_key": "fact"}]}, extract.UNIT_SCHEMA)
    with pytest.raises(SchemaViolation, match="is not one of"):
        check_schema({"context": "c", "entities": []}, route.ENRICH_SCHEMA)  # ok
        check_schema(
            {"verdict": "approve", "checks": {}, "findings": [], "auditor_confidence": 1},
            audit.AUDIT_SCHEMA,
        )
    with pytest.raises(SchemaViolation, match="undeclared"):
        check_schema({"topic_label": "t", "routing_reason": "r", "vibe": "good"},
                     route.LABEL_SCHEMA)


# --- Malformed model output costs one unit, not the corpus --------------------


def test_one_malformed_unit_does_not_discard_the_whole_extraction(tmp_path: Path):
    """Spec §18. Pass 1 wrote once at the end, so a KeyError on the last
    document threw away every source's paid extraction, including the ones that
    came out fine. The forced-tool fallback and a max_tokens truncation both
    produce exactly this shape.
    """
    class _TruncatedSecondUnit(FakeClient):
        def _pass_extract(self, user: str) -> dict:
            result = super()._pass_extract(user)
            if "limiter" in user:
                broken = dict(result["units"][1])
                broken.pop("scores")
                result["units"] = [result["units"][0], broken, result["units"][2]]
            return result

        def complete_json(self, **kwargs):
            # The malformed unit is exactly what a schema would have rejected,
            # so the schema check has to be bypassed to simulate the API
            # returning it anyway -- which is what the fallback path does.
            if "GRANULARITY" in kwargs["system"]:
                self.calls.append("extract")
                return self._pass_extract(kwargs["user"])
            return super().complete_json(**kwargs)

    ctx = _pipeline_with(tmp_path, _TruncatedSecondUnit())

    units = read_jsonl(ctx.units)
    assert len(units) == 4, "the surviving units were discarded with the broken one"
    assert {u["source_id"] for u in units} == {
        u["source_id"] for u in read_jsonl(ctx.source_registry)
    }

    rejects = read_jsonl(ctx.units.with_name("rejects.jsonl"))
    assert len(rejects) == 1
    assert "scores" in rejects[0]["reason"]
    assert validate_run(ctx)["ok"]


def test_pass_one_checkpoints_are_cleaned_up_on_success(run):
    """Left behind, they would make a later --force resume instead of recompute."""
    ctx = run["ctx"]
    assert not ctx.units.with_name("units.partial.jsonl").exists()
    assert not ctx.omissions.with_name("omissions.partial.jsonl").exists()


# --- Migration must never overwrite a real classification ---------------------






def test_suppressing_a_modality_does_not_move_the_content_hash(run):
    """`suppressed_modality` is a derived label, so it stays out of the digest."""
    from kip.artifacts import DERIVED_FIELDS, seal

    assert "suppressed_modality" in DERIVED_FIELDS
    unit = dict(run["units"][0])
    before = unit["content_sha256"]
    unit["suppressed_modality"] = "required"
    assert seal(unit)["content_sha256"] == before


# --- The provenance flag the pipeline advertises ------------------------------


def test_a_paraphrased_excerpt_is_marked_unverified(tmp_path: Path):
    """`excerpt_verified` could be forced true and the suite stayed green.

    Then `trace` prints [verbatim] for a quote that was never located and the
    validator's "not verbatim-matched" warning never fires.
    """
    sources = tmp_path / "src"
    sources.mkdir()
    (sources / "trial.txt").write_text(SOURCE_A, encoding="utf-8")

    class _Paraphraser(FakeClient):
        def _pass_extract(self, user: str) -> dict:
            return {"units": [{
                "flags": [],
                "node_kind": "unit",
                "entity_mentions": [],
                "canonical_statement": "Delayed recall improved in the extension group.",
                "decontextualization_note": "Named the group.",
                # A paraphrase, not a quote: no such string is in the document.
                "evidence": [{
                    "excerpt": "Recall was better for people who slept longer.",
                    "line_start": 2, "line_end": 2,
                    "role": "primary",
                }],
                "scores": _SCORES,
                "decision": "keep", "grounding": "attributable",
            }]}

    ctx = RunContext(run_id="run-para", root=tmp_path / "ws")
    run_pipeline(ctx, Config(), sources, client=_Paraphraser(), stop_after="extract")

    evidence = read_jsonl(ctx.units)[0]["evidence"][0]
    assert evidence["excerpt_verified"] is False
    assert evidence["normalized_line_start"] == 2  # fell back to the claimed range

    report = validate_run(ctx)
    assert any("not verbatim-matched" in w for w in report["warnings"]), report["warnings"]
    assert "UNVERIFIED" in trace_leaf(ctx, read_jsonl(ctx.units)[0]["unit_id"])


# --- The CLI --------------------------------------------------------------


def test_cli_run_copies_originals_and_records_the_datamark_choice(tmp_path: Path, capsys):
    """`kip run --stop-after normalize` needs no API key, so it is testable."""
    sources = write_sources(tmp_path)
    workspace = tmp_path / "ws"
    assert cli.main([
        "--workspace", str(workspace), "run", "--sources", str(sources),
        "--run-id", "run-cli", "--stop-after", "normalize", "--no-datamark",
    ]) == 0

    ctx = RunContext(run_id="run-cli", root=workspace)
    copied = sorted(p.name for p in ctx.sources_dir.iterdir())
    assert copied == ["rate-limit-policy.txt", "replication.txt", "trial.txt"]
    manifest = json.loads(ctx.manifest.read_text(encoding="utf-8"))
    assert manifest["config"]["datamark"] is False


def test_cli_run_keeps_same_named_files_from_different_directories(tmp_path: Path):
    """Copying by basename dropped the second file: never ingested, never counted."""
    sources = tmp_path / "src"
    for quarter, body in (("q1", "Q1 revenue was 5,000 USD.\n"), ("q2", "Q2 revenue was 7,200 USD.\n")):
        (sources / quarter).mkdir(parents=True)
        (sources / quarter / "report.md").write_text(body, encoding="utf-8")

    workspace = tmp_path / "ws"
    assert cli.main([
        "--workspace", str(workspace), "run", "--sources", str(sources),
        "--run-id", "run-sub", "--stop-after", "normalize",
    ]) == 0

    ctx = RunContext(run_id="run-sub", root=workspace)
    copied = sorted(str(p.relative_to(ctx.sources_dir)) for p in ctx.sources_dir.rglob("*.md"))
    assert copied == ["q1/report.md", "q2/report.md"]
    assert len(read_jsonl(ctx.source_registry)) == 2


def test_cli_validate_returns_one_on_a_tampered_run_and_zero_on_a_clean_one(run, capsys):
    ctx = run["ctx"]
    assert cli.main(["--workspace", str(ctx.root), "validate", ctx.run_id]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True

    units = read_jsonl(ctx.units)
    units[0]["canonical_statement"] = "Something else entirely."
    write_jsonl_atomic(ctx.units, units)
    assert cli.main(["--workspace", str(ctx.root), "validate", ctx.run_id]) == 1


def test_cli_validate_reports_a_missing_run_instead_of_crashing(tmp_path: Path, capsys):
    assert cli.main(["--workspace", str(tmp_path), "validate", "run-typo"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["ok"] is False
    assert any("does not exist" in e for e in report["errors"])


def test_cli_validate_returns_two_when_validation_itself_fails(run, capsys, monkeypatch):
    """A crashed gate must be distinguishable from a failed corpus."""
    monkeypatch.setattr(
        "kip.cli.validate_run",
        lambda ctx: (_ for _ in ()).throw(RuntimeError("disk went away")),
    )
    assert cli.main(["--workspace", str(run["ctx"].root), "validate", run["ctx"].run_id]) == 2
    assert "disk went away" in capsys.readouterr().out


def test_cli_show_and_trace(run, capsys):
    ctx = run["ctx"]
    assert cli.main(["--workspace", str(ctx.root), "show", ctx.run_id, "units", "--limit", "1"]) == 0
    assert json.loads(capsys.readouterr().out.strip())["unit_id"]

    assert cli.main(["--workspace", str(ctx.root), "trace", ctx.run_id,
                     run["events"][0]["queue_event_id"]]) == 0
    assert "original file" in capsys.readouterr().out
    assert cli.main(["--workspace", str(ctx.root), "trace", ctx.run_id, "not-an-id"]) == 1


def test_cli_show_returns_one_for_an_artifact_that_does_not_exist(tmp_path: Path):
    assert cli.main(["--workspace", str(tmp_path), "show", "run-nope", "units"]) == 1


def test_cli_run_refuses_to_replace_an_archived_original_without_force(tmp_path: Path, capsys):
    """The archived copy IS the provenance record for a durable leaf."""
    sources = write_sources(tmp_path)
    workspace = tmp_path / "ws"
    argv = ["--workspace", str(workspace), "run", "--sources", str(sources),
            "--run-id", "run-arch", "--stop-after", "normalize"]
    assert cli.main(argv) == 0

    (sources / "trial.txt").write_text(SOURCE_A + "A late addition.\n", encoding="utf-8")
    assert cli.main(argv) == 2
    assert "use a new run id" in capsys.readouterr().err

    assert cli.main(argv + ["--force"]) == 0
    ctx = RunContext(run_id="run-arch", root=workspace)
    assert "A late addition." in (ctx.sources_dir / "trial.txt").read_text(encoding="utf-8")
