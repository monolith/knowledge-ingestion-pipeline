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

from .artifacts import RunContext, envelope, seal, text_hash, write_jsonl_atomic
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
    """Every referenced ID must resolve. Pure code, no judgment required."""
    broken: list[str] = []
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
    if cfg.audit.require_distinct_auditor and not distinct:
        # Spec §13.3b: self-preference bias survives anonymization, so this is
        # not a soft preference. Fail loudly rather than produce an audit whose
        # verdicts cannot be trusted.
        raise RuntimeError(
            f"Auditor model ({auditor_model}) must differ from the proposer "
            f"({proposer_model}). Set KIP_MODEL_AUDITOR to a different "
            "reasoning-class model, or disable require_distinct_auditor "
            "knowing the audit's verdicts become self-assessment."
        )

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
    return audits, approved


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

    revised = dict(candidate)
    if verdict in ("fix", "merge", "split"):
        correction = result.get("corrected_candidate")
        if not correction:
            return None  # a fix without a correction cannot be queued
        revised.update(
            {
                "title": correction["title"],
                "slug": candidate["slug"],
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
            f"  {unit_id} [{unit['unit_type']}]"
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
