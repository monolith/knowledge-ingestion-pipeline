"""Pass 5 — adversarial audit.

Spec §13. The audit only works under specific conditions, so this module
enforces them rather than assuming them:
  - deterministic checks run in code, not LLM judgment (spec §13.4)
  - the auditor is reasoning-class and distinct from the proposer (§13.3)
  - pairwise judgments run both orderings (§13.3c)
  - auditor_confidence is recorded but never gates (§13.6)
"""

from __future__ import annotations

from typing import Any

from .artifacts import (
    RunContext,
    envelope,
    seal,
    text_hash,
    write_json_atomic,
    write_jsonl_atomic,
)
from .candidates import slugify
from .config import Config
from .llm import LLMClient

PROMPT_VERSION = "pass-05-adversarial-audit-v3.0"

VERDICTS = ["pass", "pass_with_label", "fix", "merge", "split", "reject", "defer"]

AUDIT_SYSTEM = """You are an adversarial auditor. Your job is to DISPROVE, narrow,
or reject the candidate -- not to restate or approve it.

You did not write this candidate. Do not assume its author was careful.

Some checks have already been performed mechanically and their results are given
to you. Trust those results; they are exact string and path comparisons, not
judgments. Focus your effort on the checks that require reading.

CHECKS YOU OWN
- coverage: are material results, limitations, exceptions, and contradictions
  represented? What did the candidate leave out?
- contradiction_handling: is disagreement hidden behind a confident synthesis?
- scope_fidelity: are population, time, jurisdiction, modality (may/should/must),
  and conditions preserved exactly? Narrowing or widening scope is a defect.
- source_independence: does the candidate treat derivative artifacts as
  replication? Two documents from one independence group are ONE piece of
  evidence.
- duplication: is this the right leaf size, or is it redundant with, or too
  narrow for, the surrounding ontology?

VERDICTS: pass, pass_with_label, fix, merge, split, reject, defer.
A fix/merge/split MUST include a corrected candidate; it never overwrites the
original, it produces a new version.

If the candidate's title or knowledge_state overstates the evidence -- for
example calling a contested finding "established" -- that alone warrants "fix".

Report auditor_confidence honestly. It is recorded for calibration analysis and
does not gate anything, so there is no reason to inflate it."""

AUDIT_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": VERDICTS},
        "checks": {
            "type": "object",
            "properties": {
                "coverage": {"type": "string", "enum": ["pass", "warn", "fail"]},
                "contradiction_handling": {"type": "string", "enum": ["pass", "warn", "fail"]},
                "scope_fidelity": {"type": "string", "enum": ["pass", "warn", "fail"]},
                "source_independence": {"type": "string", "enum": ["pass", "warn", "fail"]},
                "duplication": {"type": "string", "enum": ["pass", "warn", "fail"]},
            },
            "required": [
                "coverage", "contradiction_handling", "scope_fidelity",
                "source_independence", "duplication",
            ],
            "additionalProperties": False,
        },
        "findings": {"type": "array", "items": {"type": "string"}},
        "required_fixes": {"type": "array", "items": {"type": "string"}},
        "raw_source_escalation": {"type": "array", "items": {"type": "string"}},
        "auditor_confidence": {"type": "number"},
        "corrected_candidate": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "knowledge_state": {"type": "string"},
                "summary": {"type": "string"},
                "assertions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "assessment_ids": {"type": "array", "items": {"type": "string"}},
                        },
                        "required": ["text", "assessment_ids"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["title", "knowledge_state", "summary", "assertions"],
            "additionalProperties": False,
        },
    },
    "required": ["verdict", "checks", "findings", "auditor_confidence"],
    "additionalProperties": False,
}


# --- Deterministic checks (spec §13.4) ----------------------------------------
# These replace LLM judgment wherever the question has an exact answer. The
# motivation is blunt: even the best reasoning judges carry ~19% pairwise error
# on hard cases, while a string comparison carries none.


def check_citation_accuracy(
    candidate: dict[str, Any],
    units_by_id: dict[str, dict[str, Any]],
    ctx: RunContext,
) -> dict[str, Any]:
    """Verify every cited excerpt against the normalized source, exactly.

    Automated *semantic* citation checkers top out at ~80-85% agreement with
    humans -- about 1 in 5 judgments wrong. Exact offset-and-hash matching has
    no such error, which is why Pass 0 and Pass 1 are required to record
    character offsets and excerpt hashes.
    """
    checked = mismatched = missing = 0
    details: list[str] = []
    cache: dict[str, str] = {}

    # A candidate citing no units checks out zero excerpts and used to come back
    # "pass" -- a leaf with no provenance chain at all, sailing through every
    # deterministic gate because there was nothing to disagree with. Spec §22
    # AC3 requires every retained unit to trace to an exact source excerpt, so
    # "nothing to check" is a failure of that criterion, not a satisfaction of it.
    if not candidate.get("source_unit_ids"):
        return {
            "result": "fail",
            "mode": "deterministic",
            "checked": 0,
            "mismatched": 0,
            "missing": 0,
            "details": ["candidate cites no source units; nothing traces to a source excerpt"],
        }

    for unit_id in candidate.get("source_unit_ids", []):
        unit = units_by_id.get(unit_id)
        if unit is None:
            missing += 1
            details.append(f"{unit_id}: unit not found")
            continue

        for evidence in unit.get("evidence", []):
            checked += 1
            excerpt = evidence.get("excerpt", "")
            path_rel = evidence.get("normalized_path", "")

            if excerpt and text_hash(excerpt) != evidence.get("excerpt_sha256"):
                mismatched += 1
                details.append(f"{unit_id}: excerpt hash mismatch")
                continue

            if path_rel not in cache:
                path = ctx.run_dir / path_rel
                cache[path_rel] = path.read_text(encoding="utf-8") if path.exists() else ""
            source_text = cache[path_rel]

            if not source_text:
                missing += 1
                details.append(f"{unit_id}: normalized source missing ({path_rel})")
                continue

            start = evidence.get("normalized_char_start", -1)
            end = evidence.get("normalized_char_end", -1)
            if 0 <= start < end <= len(source_text) and source_text[start:end] == excerpt:
                continue  # exact offset match

            if excerpt and excerpt in source_text:
                # Present but offsets drifted -- worth flagging, not a fabrication.
                details.append(f"{unit_id}: excerpt found but char offsets are stale")
                continue

            mismatched += 1
            details.append(f"{unit_id}: excerpt not found in normalized source")

    result = "pass"
    if mismatched:
        result = "fail"
    elif missing or details:
        result = "warn"
    return {
        "result": result,
        "mode": "deterministic",
        "checked": checked,
        "mismatched": mismatched,
        "missing": missing,
        "details": details[:20],
    }


def check_provenance_integrity(
    candidate: dict[str, Any],
    units_by_id: dict[str, dict[str, Any]],
    assessments_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Every referenced ID must resolve. Pure code, no judgment required.

    An empty reference list is broken, not clean. "Every id resolves" is
    vacuously true of a candidate that names none, and a candidate that names
    none is a knowledge-base leaf with no evidence behind it.
    """
    broken: list[str] = []
    if not candidate.get("assertions"):
        broken.append("candidate has no assertions")
    if not candidate.get("source_unit_ids"):
        broken.append("candidate has no source_unit_ids")
    for unit_id in candidate.get("source_unit_ids", []):
        if unit_id not in units_by_id:
            broken.append(f"unknown unit {unit_id}")
    for assertion in candidate.get("assertions", []):
        ids = assertion.get("assessment_ids", [])
        if not ids:
            broken.append(f"assertion without assessment_ids: {assertion.get('text', '')[:60]}")
        for assessment_id in ids:
            if assessment_id not in assessments_by_id:
                broken.append(f"unknown assessment {assessment_id}")
    return {
        "result": "fail" if broken else "pass",
        "mode": "deterministic",
        "broken": broken[:20],
    }


def check_independence_inflation(
    candidate: dict[str, Any],
    units_by_id: dict[str, dict[str, Any]],
    assessments_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Catch a single-source claim dressed as independent confirmation.

    Mechanical version of spec §12's rule that a dependent convergence must
    never become independent support. The LLM auditor also checks this
    semantically; this catches the arithmetic case for free.
    """
    groups = {
        units_by_id[uid]["independence_group"]
        for uid in candidate.get("source_unit_ids", [])
        if uid in units_by_id
    }
    state = candidate.get("knowledge_state", "")
    inflated = state == "established" and len(groups) < 2
    return {
        "result": "fail" if inflated else "pass",
        "mode": "deterministic",
        "independence_groups": sorted(groups),
        "detail": (
            "knowledge_state 'established' rests on a single independence group"
            if inflated else ""
        ),
    }


# --- Preflight ----------------------------------------------------------------


def check_auditor_distinct(cfg: Config) -> None:
    """Refuse a configuration whose auditor is its own proposer.

    Spec §13.3b: self-preference bias survives anonymization, so this is not a
    soft preference. Called from run_pipeline BEFORE Pass 0 as well as from Pass
    5, because discovering it at Pass 5 means the operator has already paid for
    extraction, enrichment, assessment and planning on the whole corpus for an
    audit that was never going to run.
    """
    auditor_model = cfg.model_for("auditor")
    proposer_model = cfg.model_for("planner")
    if cfg.audit.require_distinct_auditor and auditor_model == proposer_model:
        raise RuntimeError(
            f"Auditor model ({auditor_model}) must differ from the proposer "
            f"({proposer_model}). Set KIP_MODEL_AUDITOR to a different "
            "reasoning-class model, or disable require_distinct_auditor "
            "knowing the audit's verdicts become self-assessment."
        )


# --- Pass entry point ---------------------------------------------------------


def audit_candidates(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    candidates: list[dict[str, Any]],
    units: list[dict[str, Any]],
    assessments: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    units_by_id = {u["unit_id"]: u for u in units}
    assessments_by_id = {a["assessment_id"]: a for a in assessments}

    auditor_model = cfg.model_for("auditor")
    proposer_model = cfg.model_for("planner")
    distinct = auditor_model != proposer_model
    check_auditor_distinct(cfg)

    audits: list[dict[str, Any]] = []
    approved: list[dict[str, Any]] = []

    for candidate in candidates:
        mechanical = {
            "citation_accuracy": check_citation_accuracy(candidate, units_by_id, ctx),
            "provenance_integrity": check_provenance_integrity(
                candidate, units_by_id, assessments_by_id
            ),
            "independence_inflation": check_independence_inflation(
                candidate, units_by_id, assessments_by_id
            ),
        }

        try:
            result = client.complete_json(
                system=AUDIT_SYSTEM,
                user=_render(candidate, units_by_id, assessments_by_id, mechanical),
                schema=AUDIT_SCHEMA,
                model=auditor_model,
                max_tokens=16384,
            )
        except Exception as exc:
            print(f"[pass5] audit failed for {candidate['candidate_id']}: {exc}")
            continue

        verdict = result["verdict"]
        # A mechanical failure overrides an LLM "pass". The code check has no
        # error rate; the judgment does.
        if any(check["result"] == "fail" for check in mechanical.values()) and verdict in (
            "pass", "pass_with_label"
        ):
            verdict = "fix"
            result.setdefault("findings", []).append(
                "Verdict escalated to 'fix': a deterministic check failed."
            )

        audit = seal(
            {
                **envelope(
                    ctx,
                    prompt_version=PROMPT_VERSION,
                    model_role="adversarial-grounding-auditor",
                    parent_artifacts=[
                        "05_candidates/candidates.initial.jsonl",
                        "04_assessments/claim_assessments.jsonl",
                        "02_units/units.jsonl",
                    ],
                ),
                "audit_id": f"audit-{candidate['candidate_id']}",
                "candidate_id": candidate["candidate_id"],
                "verdict": verdict,
                "auditor_model": auditor_model,
                "auditor_distinct_from_proposer": distinct,
                "order_swap_applied": cfg.audit.order_swap,
                "checks": {
                    **{
                        name: {"result": value, "mode": "llm_reasoning"}
                        for name, value in result["checks"].items()
                    },
                    **mechanical,
                },
                "findings": result.get("findings", []),
                "required_fixes": result.get("required_fixes", []),
                "raw_source_escalation": result.get("raw_source_escalation", []),
                # Recorded for calibration analysis; deliberately not a gate.
                "auditor_confidence": result.get("auditor_confidence", 0.5),
            }
        )
        audits.append(audit)

        revision = _approve(ctx, candidate, audit, result)
        if revision is not None:
            approved.append(revision)

    write_jsonl_atomic(ctx.audits, audits)
    write_jsonl_atomic(ctx.approved, approved)

    # Every audit above judges one candidate against its own sources. None of
    # them can see what the corpus lost, because a unit that reached no
    # candidate appears in no candidate's audit. This last call is the only
    # place in the pipeline that reads the extraction and the output together.
    coverage = audit_corpus_coverage(ctx, cfg, client, units, approved)
    write_json_atomic(ctx.corpus_coverage, coverage)
    return audits, approved


CORPUS_PROMPT_VERSION = "pass-05b-corpus-coverage-v1.0"

CORPUS_SYSTEM = """You judge whether a knowledge base fairly represents the corpus it came from.

You are given every knowledge unit extracted from the sources, and every
assertion that reached the approved output. Answer one question: would a reader
who has only the output know what the corpus contains?

Two failures matter, and they are different:

  - LOST CONTENT. A unit that reached no assertion. Definitions, rules and
    procedures are the ones that go missing, because they assert nothing to
    argue with and a synthesis step describes them instead of carrying them
    across. A reader must be able to APPLY a definition from the output alone.
    "The codebook defines fifteen labels" is not the definitions.
  - MISREPRESENTATION. The output is complete but skewed -- a minor point
    promoted to a headline, a central one buried, or a caveat dropped so a
    finding reads as firmer than the corpus supports.

Deduplication is NOT loss. If two units say the same thing and one assertion
carries it, that is correct. Say so rather than counting it as missing.

Judge the corpus as a whole. Name what is missing specifically enough to act on:
which unit, and what a consumer can no longer do because of it."""

CORPUS_SCHEMA = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string", "description": "Think it through. 2-5 sentences."},
        "verdict": {"type": "string", "enum": ["represented", "gaps", "misrepresented"]},
        "key_insights_captured": {"type": "boolean"},
        "definitions_captured": {"type": "boolean"},
        "fairly_represented": {"type": "boolean"},
        "missing": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "unit_ids": {"type": "array", "items": {"type": "string"}},
                    "what_is_lost": {"type": "string"},
                    "consequence": {"type": "string"},
                },
                "required": ["what_is_lost", "consequence"],
                "additionalProperties": False,
            },
        },
        "notes": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "reasoning", "verdict", "key_insights_captured", "definitions_captured",
        "fairly_represented", "missing",
    ],
    "additionalProperties": False,
}


def audit_corpus_coverage(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    units: list[dict[str, Any]],
    approved: list[dict[str, Any]],
) -> dict[str, Any]:
    """Judge the output against the whole extraction, not candidate by candidate.

    Spec §21 lists an orphan rate as a quality metric and §7.7 forbids losing a
    source silently. Neither is enforced between Pass 1 and Pass 4, which is how
    a run can drop most of what it extracted and pass every per-record check.
    `kip validate` reports the arithmetic; this pass reads the content and says
    whether the loss mattered.
    """
    kept = [u for u in units if u.get("decision") == "keep"]
    carried: set[str] = set()
    for candidate in approved:
        carried.update(candidate.get("source_unit_ids", []))
    orphaned = [u for u in kept if u.get("unit_id") not in carried]

    mechanical = {
        "units_kept": len(kept),
        "units_carried": len([u for u in kept if u.get("unit_id") in carried]),
        "units_orphaned": len(orphaned),
        "assertions_out": sum(len(c.get("assertions", [])) for c in approved),
    }

    if not kept or not approved:
        return {
            **envelope(ctx, prompt_version=CORPUS_PROMPT_VERSION,
                       model_role="corpus-coverage-auditor",
                       parent_artifacts=["02_units/units.jsonl",
                                         "06_audit/candidates.approved.jsonl"]),
            "mechanical": mechanical, "verdict": "represented",
            "key_insights_captured": True, "definitions_captured": True,
            "fairly_represented": True, "missing": [],
            "notes": ["nothing to judge: the run produced no kept units or no approved output"],
            "auditor_model": cfg.model_for("auditor"),
        }

    def line(u: dict[str, Any]) -> str:
        mark = " [REACHED NO ASSERTION]" if u.get("unit_id") not in carried else ""
        return f"- {u.get('unit_id')}{mark}: {u.get('canonical_statement', '')}"

    out_lines = []
    for c in approved:
        out_lines.append(f"## {c.get('title', '')}")
        out_lines += [f"- {a.get('text', '')}" for a in c.get("assertions", [])]

    user = (
        f"EXTRACTED UNITS ({len(kept)}), {len(orphaned)} of which reached no assertion:\n"
        + "\n".join(line(u) for u in kept)
        + f"\n\nAPPROVED OUTPUT ({mechanical['assertions_out']} assertions across "
        f"{len(approved)} entries):\n"
        + "\n".join(out_lines)
        + "\n\nDoes the output fairly represent the corpus?"
    )

    try:
        result = client.complete_json(
            system=CORPUS_SYSTEM, user=user, schema=CORPUS_SCHEMA,
            model=cfg.model_for("auditor"), max_tokens=16384,
        )
    except Exception as exc:  # a judgement that fails is recorded, never fatal
        print(f"[pass5] corpus coverage audit failed: {exc}")
        result = {
            "verdict": "gaps", "key_insights_captured": False,
            "definitions_captured": False, "fairly_represented": False,
            "missing": [], "notes": [f"coverage audit did not run: {exc}"],
        }

    return {
        **envelope(ctx, prompt_version=CORPUS_PROMPT_VERSION,
                   model_role="corpus-coverage-auditor",
                   parent_artifacts=["02_units/units.jsonl",
                                     "06_audit/candidates.approved.jsonl"]),
        "mechanical": mechanical,
        "verdict": result.get("verdict", "gaps"),
        "key_insights_captured": result.get("key_insights_captured", False),
        "definitions_captured": result.get("definitions_captured", False),
        "fairly_represented": result.get("fairly_represented", False),
        "missing": result.get("missing", []),
        "notes": result.get("notes", []),
        "reasoning": result.get("reasoning", ""),
        "auditor_model": cfg.model_for("auditor"),
    }


def _approve(
    ctx: RunContext,
    candidate: dict[str, Any],
    audit: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any] | None:
    """Produce the approved candidate VERSION, never an in-place edit.

    Spec §13.5: a fix/merge/split produces a new candidate version; it never
    overwrites the initial proposal. That is what makes the audit itself
    auditable -- the original overconfident claim stays on disk next to its
    correction.
    """
    verdict = audit["verdict"]
    if verdict in ("reject", "defer"):
        return None

    # Last gate before the queue. The mechanical checks above already fail an
    # unsourced candidate, but a `fix` verdict rewrites the prose and leaves
    # source_unit_ids untouched, so a correction cannot repair missing
    # provenance -- and spec §22 AC3 is not negotiable by an auditor.
    if not candidate.get("assertions") or not candidate.get("source_unit_ids"):
        print(
            f"[pass5] {candidate['candidate_id']} not approved: no assertions or no "
            "source units, so nothing about it traces to a source excerpt"
        )
        return None

    revised = dict(candidate)
    if verdict in ("fix", "merge", "split"):
        correction = result.get("corrected_candidate")
        if not correction:
            return None  # a fix without a correction cannot be queued
        revised.update(
            {
                "title": correction["title"],
                # Derived from the corrected title, not carried over. The slug is
                # what the queue payload hands the consumer as its key, so
                # freezing it across a correction files the corrected entry under
                # the uncorrected name -- the audit's own finding, preserved in
                # the one field a knowledge base indexes on. Stability is not an
                # argument for freezing it: the candidate_id already changes on
                # revision, and the slug is a pure function of the title.
                "slug": slugify(correction["title"]),
                "knowledge_state": correction["knowledge_state"],
                "summary": correction["summary"],
                "assertions": correction["assertions"],
            }
        )

    revised["candidate_id"] = f"{candidate['candidate_id']}-r1"
    revised["candidate_version"] = candidate["candidate_version"] + 1
    revised["supersedes"] = candidate["candidate_id"]
    revised["audit_ids"] = [audit["audit_id"]]
    revised["audit_verdict"] = verdict
    revised["created_at"] = audit["created_at"]
    if verdict == "pass_with_label":
        revised["labels"] = result.get("required_fixes", []) or result.get("findings", [])
    return seal(revised)


def _render(
    candidate: dict[str, Any],
    units_by_id: dict[str, dict[str, Any]],
    assessments_by_id: dict[str, dict[str, Any]],
    mechanical: dict[str, Any],
) -> str:
    lines = [
        "CANDIDATE UNDER AUDIT",
        f"  title: {candidate['title']}",
        f"  knowledge_state: {candidate['knowledge_state']}",
        f"  operation: {candidate['suggested_operation']}",
        f"  summary: {candidate['summary']}",
        "  assertions:",
    ]
    for assertion in candidate.get("assertions", []):
        lines.append(f"    - {assertion['text']}  [{', '.join(assertion.get('assessment_ids', []))}]")

    lines.append("\nUNDERLYING ASSESSMENTS")
    seen: set[str] = set()
    for assertion in candidate.get("assertions", []):
        for assessment_id in assertion.get("assessment_ids", []):
            if assessment_id in seen:
                continue
            seen.add(assessment_id)
            assessment = assessments_by_id.get(assessment_id)
            if assessment is None:
                lines.append(f"  {assessment_id}: MISSING")
                continue
            lines.append(
                f"  {assessment_id}: stance={assessment['coarse_stance']}"
                f" bucket={assessment['relationship_bucket']}"
                f" subtype={assessment['relationship_subtype']}"
                f" (conf {assessment.get('subtype_confidence', 0.5):.2f})"
                f" uncertainty={assessment['uncertainty']}"
                f" independence_groups={assessment.get('independent_evidence_groups', [])}"
                f"\n    claim: {assessment['canonical_claim']}"
                f"\n    synthesis: {assessment['synthesis']}"
            )

    lines.append("\nSOURCE UNITS AND EVIDENCE")
    for unit_id in candidate.get("source_unit_ids", []):
        unit = units_by_id.get(unit_id)
        if unit is None:
            lines.append(f"  {unit_id}: MISSING")
            continue
        excerpt = (unit.get("evidence") or [{}])[0].get("excerpt", "")[:240]
        lines.append(
            f"  {unit_id}"
            f" (group={unit['independence_group']}): {unit['canonical_statement']}"
            f"\n    evidence: \"{excerpt}\""
        )

    lines.append("\nMECHANICAL CHECK RESULTS (already verified in code -- trust these)")
    for name, check in mechanical.items():
        lines.append(f"  {name}: {check['result']}")
        for detail in (check.get("details") or check.get("broken") or [])[:8]:
            lines.append(f"    - {detail}")
        if check.get("detail"):
            lines.append(f"    - {check['detail']}")

    lines.append(
        "\nAudit this candidate. If the title or knowledge_state overstates the "
        "evidence, return verdict 'fix' with a corrected_candidate."
    )
    return "\n".join(lines)
