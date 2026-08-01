"""Pass 1 — molecular knowledge extraction, plus the omission check.

Spec §9. The central v3 change lives here: units are *molecular*
(decontextualized but minimal), not maximally atomic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import RunContext, envelope, seal, text_hash, write_jsonl_atomic
from .config import Config
from .llm import DATA_BOUNDARY_NOTE, LLMClient, wrap_untrusted

PROMPT_VERSION = "pass-01-molecular-extraction-v3.0"
OMISSION_PROMPT_VERSION = "pass-01b-omission-check-v3.0"

UNIT_TYPES = [
    "fact", "claim", "definition", "quantitative_result", "null_result",
    "study_design", "method", "decision", "obligation", "prohibition",
    "exception", "deadline", "dependency", "risk", "limitation",
    "contradiction", "recommendation", "open_question", "observation",
    "metadata",
]

# --- System prompt ------------------------------------------------------------
# Every rule below is a spec decision, and the wording is deliberately close to
# the spec's own. Prompts are versioned code (spec §19.1).

EXTRACTION_SYSTEM = """You extract durable, source-backed knowledge units from documents.

{boundary}

GRANULARITY — this is the most important rule.
Each unit must be MOLECULAR, which means both of:
  - DECONTEXTUALITY: it can be interpreted correctly standing alone, without
    its neighbours or the surrounding prose. Resolve pronouns and vague
    references ("the study", "this policy") into what they refer to.
  - MINIMALITY: it adds the LEAST information required to achieve
    decontextuality, and no more.

Do NOT decompose maximally. A fragment that cannot be interpreted on its own is
a defect, not a smaller unit. Split a statement only when the parts are BOTH
independently evaluable AND independently interpretable. Candidate reasons to
split: differing truth value, actor, population, intervention, outcome, time
horizon, modality (may/should/must), confidence, scope, or exception.

CARDINALITY: return as many units as the source warrants. Never target a fixed
number. A short source may yield two units; a dense one may yield thirty.

LENGTH: canonical_statement is normally one sentence, two only when the second
carries an inseparable qualifier. Target {lo}-{hi} words; warn past {warn}.
There is NO character cap.

EVIDENCE: every unit cites one to three minimal excerpts, quoted VERBATIM from
the document, under {eviwords} words total. Quote exactly -- excerpts are
verified by exact string match downstream, and a paraphrased excerpt fails.

SCORING: score 0-3 on specificity, retrieval_value, connection_value,
evidence_strength, novelty. The decision is NOT a simple sum: mandatory
obligations, contradictions, critical limitations, and rare exceptions may be
kept even when scores are low.

Never invent evidence. If something is implied but not stated, either omit it or
mark it in qualifiers. Report only what the document supports."""

OMISSION_SYSTEM = """You check an extraction for completeness against its source document.

{boundary}

You are given the document and the units already extracted from it. Report what
is MISSING or MIS-SHAPED. Ask:
  - Which decisions, exceptions, limitations, negative results, dependencies,
    and numerical findings are not represented?
  - Which retained unit bundles claims that could be independently true or false?
  - Which unit cannot be understood without hidden context?

Report each finding separately with the exact source excerpt it concerns. Do not
restate what is already covered. If nothing is missing, return an empty list."""


# --- Schemas ------------------------------------------------------------------

EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "excerpt": {"type": "string", "description": "Verbatim quote from the document."},
        "line_start": {"type": "integer"},
        "line_end": {"type": "integer"},
    },
    "required": ["excerpt", "line_start", "line_end"],
    "additionalProperties": False,
}

UNIT_SCHEMA = {
    "type": "object",
    "properties": {
        "units": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "unit_type": {"type": "string", "enum": UNIT_TYPES},
                    "canonical_statement": {"type": "string"},
                    "context_note": {"type": "string"},
                    "decontextualization_note": {
                        "type": "string",
                        "description": "What was added to make this stand alone.",
                    },
                    "qualifiers": {"type": "array", "items": {"type": "string"}},
                    "candidate_topics": {"type": "array", "items": {"type": "string"}},
                    "evidence": {"type": "array", "items": EVIDENCE_SCHEMA},
                    "scores": {
                        "type": "object",
                        "properties": {
                            "specificity": {"type": "integer", "enum": [0, 1, 2, 3]},
                            "retrieval_value": {"type": "integer", "enum": [0, 1, 2, 3]},
                            "connection_value": {"type": "integer", "enum": [0, 1, 2, 3]},
                            "evidence_strength": {"type": "integer", "enum": [0, 1, 2, 3]},
                            "novelty": {"type": "integer", "enum": [0, 1, 2, 3]},
                        },
                        "required": [
                            "specificity", "retrieval_value", "connection_value",
                            "evidence_strength", "novelty",
                        ],
                        "additionalProperties": False,
                    },
                    "decision": {"type": "string", "enum": ["keep", "drop", "review"]},
                    "drop_reason": {"type": "string"},
                    "extraction_confidence": {"type": "number"},
                },
                "required": [
                    "unit_type", "canonical_statement", "evidence", "scores", "decision",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["units"],
    "additionalProperties": False,
}

OMISSION_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": ["missing", "bundled", "needs_context", "unsupported"],
                    },
                    "description": {"type": "string"},
                    "excerpt": {"type": "string"},
                    "affected_unit_ids": {"type": "array", "items": {"type": "string"}},
                    "suggested_action": {
                        "type": "string",
                        "enum": ["add", "split", "merge", "downgrade", "drop"],
                    },
                },
                "required": ["kind", "description", "suggested_action"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


# --- Extraction ---------------------------------------------------------------


def _numbered(text: str) -> str:
    """Number lines so the model can cite line ranges it can actually see."""
    return "\n".join(f"{i + 1:5d}| {line}" for i, line in enumerate(text.splitlines()))


def extract_units(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    registry: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract molecular units from every successfully normalized source."""
    boundary = DATA_BOUNDARY_NOTE.format(marker=cfg.datamark_char)
    system = EXTRACTION_SYSTEM.format(
        boundary=boundary,
        lo=cfg.granularity.soft_target_words[0],
        hi=cfg.granularity.soft_target_words[1],
        warn=cfg.granularity.warn_words,
        eviwords=cfg.granularity.max_evidence_words,
    )

    all_units: list[dict[str, Any]] = []
    all_omissions: list[dict[str, Any]] = []

    for manifest in registry:
        if manifest.get("normalization_status") != "success":
            continue
        source_id = manifest["source_id"]
        normalized_path = ctx.run_dir / manifest["normalized_path"]
        text = normalized_path.read_text(encoding="utf-8")

        result = client.complete_json(
            system=system,
            user=(
                f"Document title: {manifest['title']}\n"
                f"Media type: {manifest['media_type']}\n\n"
                f"{wrap_untrusted(_numbered(text), cfg)}\n\n"
                "Extract every durable, source-backed molecular knowledge unit."
            ),
            schema=UNIT_SCHEMA,
            model=cfg.model_for("extractor"),
        )

        units = _materialize_units(ctx, cfg, manifest, result.get("units", []), text)
        all_units.extend(units)

        # Omission check (spec §9.6). Kept as a separate call with its own
        # prompt: the evidence for it is a *detect-and-refine* step, and 24.9%
        # of refined facts flipped correctness once incompleteness was resolved.
        omission = client.complete_json(
            system=OMISSION_SYSTEM.format(boundary=boundary),
            user=(
                f"{wrap_untrusted(_numbered(text), cfg)}\n\n"
                "Units already extracted:\n"
                + "\n".join(
                    f"- {u['unit_id']} [{u['unit_type']}] {u['canonical_statement']}"
                    for u in units
                )
                + "\n\nWhat is missing or mis-shaped?"
            ),
            schema=OMISSION_SCHEMA,
            model=cfg.model_for("omission"),
        )
        all_omissions.extend(
            _materialize_omissions(ctx, source_id, omission.get("findings", []))
        )

    write_jsonl_atomic(ctx.omissions, all_omissions)
    return all_units


def _materialize_units(
    ctx: RunContext,
    cfg: Config,
    manifest: dict[str, Any],
    raw_units: list[dict[str, Any]],
    text: str,
) -> list[dict[str, Any]]:
    source_id = manifest["source_id"]
    lines = text.splitlines()
    units: list[dict[str, Any]] = []

    for index, raw in enumerate(raw_units, start=1):
        unit_id = f"u-{source_id}-{index:04d}"
        evidence = [
            _resolve_evidence(manifest, e, text, lines)
            for e in raw.get("evidence", [])
        ]
        record = {
            **envelope(
                ctx,
                prompt_version=PROMPT_VERSION,
                model_role="molecular-extractor",
                parent_artifacts=[manifest["normalized_path"]],
            ),
            "unit_id": unit_id,
            "source_id": source_id,
            "source_family_id": manifest["source_family_id"],
            "independence_group": manifest["independence_group"],
            "unit_type": raw["unit_type"],
            "canonical_statement": raw["canonical_statement"].strip(),
            "context_note": raw.get("context_note", ""),
            "decontextualization_note": raw.get("decontextualization_note", ""),
            "qualifiers": raw.get("qualifiers", []),
            "candidate_topics": raw.get("candidate_topics", []),
            "evidence": evidence,
            "scores": raw["scores"],
            "decision": raw["decision"],
            "drop_reason": raw.get("drop_reason"),
            "extraction_confidence": raw.get("extraction_confidence", 0.8),
            "granularity_policy": cfg.granularity.name,
        }
        units.append(seal(record))
    return units


def _resolve_evidence(
    manifest: dict[str, Any],
    raw: dict[str, Any],
    text: str,
    lines: list[str],
) -> dict[str, Any]:
    """Turn a model-reported excerpt into a verifiable evidence record.

    The model reports an excerpt and a line range; we independently locate the
    excerpt in the source text and record TRUE character offsets. This is what
    makes Pass 5's citation check deterministic rather than a second LLM
    judgment -- and it catches paraphrased "quotes" at extraction time, where
    they are cheapest to detect.
    """
    excerpt = (raw.get("excerpt") or "").strip()
    char_start = text.find(excerpt) if excerpt else -1
    verified = char_start >= 0

    if verified:
        char_end = char_start + len(excerpt)
        line_start = text.count("\n", 0, char_start) + 1
        line_end = text.count("\n", 0, char_end) + 1
    else:
        # Fall back to the model's claimed line range so the record stays
        # traceable, but mark it unverified so the audit can escalate.
        line_start = max(1, int(raw.get("line_start", 1)))
        line_end = max(line_start, int(raw.get("line_end", line_start)))
        char_start = sum(len(l) + 1 for l in lines[: line_start - 1])
        char_end = char_start + sum(len(l) + 1 for l in lines[line_start - 1 : line_end])

    return {
        "source_id": manifest["source_id"],
        "normalized_path": manifest["normalized_path"],
        "normalized_line_start": line_start,
        "normalized_line_end": line_end,
        "normalized_char_start": char_start,
        "normalized_char_end": char_end,
        "original_locator_start": {},
        "original_locator_end": {},
        "excerpt": excerpt,
        "excerpt_sha256": text_hash(excerpt),
        "excerpt_verified": verified,
    }


def _materialize_omissions(
    ctx: RunContext, source_id: str, findings: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Structured per-omission findings (spec §9.6).

    The simple end-to-end LLM omission pass beats decomposition-based
    alternatives, but its measured cost is "reduced robustness, interpretability
    and result granularity". Emitting one structured record per finding is what
    buys the interpretability back.
    """
    records = []
    for index, finding in enumerate(findings, start=1):
        records.append(
            seal(
                {
                    **envelope(
                        ctx,
                        prompt_version=OMISSION_PROMPT_VERSION,
                        model_role="omission-checker",
                        parent_artifacts=["02_units/units.jsonl"],
                    ),
                    "omission_id": f"om-{source_id}-{index:03d}",
                    "source_id": source_id,
                    "kind": finding["kind"],
                    "description": finding["description"],
                    "excerpt": finding.get("excerpt", ""),
                    "affected_unit_ids": finding.get("affected_unit_ids", []),
                    "suggested_action": finding["suggested_action"],
                    "resolved": False,
                }
            )
        )
    return records
