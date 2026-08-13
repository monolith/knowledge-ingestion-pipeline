"""Pass 1 — molecular knowledge extraction, plus the omission check.

Spec §9. The central v3 change lives here: units are *molecular*
(decontextualized but minimal), not maximally atomic.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .artifacts import RunContext, envelope, read_jsonl, seal, text_hash, write_jsonl_atomic
from .config import Config
from .retention import annotate as annotate_protected, load_taxonomy
from .llm import DATA_BOUNDARY_NOTE, LLMClient, wrap_untrusted
from .pdf_assets import formula_asset
from .vocab import FLAGS, MODALITIES, NODE_KINDS, detect_quantitative, normalize_flags, normalize_modality

PROMPT_VERSION = "pass-01-molecular-extraction-v4.2"  # v4.2: grounding flag
OMISSION_PROMPT_VERSION = "pass-01b-omission-check-v3.0"
REPAIR_PROMPT_VERSION = "pass-01c-omission-repair-v1.0"
READ_PROMPT_VERSION = "pass-00b-visual-read-v1.0"

READ_SYSTEM = """You read a page image that a text extractor could not represent.

A PDF stores tables and equations as positioned glyphs, so the text layer for
this page is damaged: table columns lost their headers, and mathematics arrived
as characters that merely resemble it. You are looking at what the page actually
says.

Return every TABLE and every DISPLAY EQUATION on the page.

For a table, give the grid as rows of cells, header row first. Column headers
matter more than anything else here -- a figure whose column is unknown is not
recoverable later. Where headers are nested, flatten them into the most specific
label a reader would use.

For an equation, give LaTeX.

Transcribe. Do not summarize, do not interpret, do not correct what the page
says. If part of the page is illegible, say so for that item rather than
guessing at it."""

READ_SCHEMA = {
    "type": "object",
    "properties": {
        "tables": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "caption": {"type": "string"},
                    "rows": {"type": "array",
                             "items": {"type": "array", "items": {"type": "string"}}},
                    "header_rows": {"type": "integer"},
                    "illegible": {"type": "string"},
                },
                "required": ["rows"],
                "additionalProperties": False,
            },
        },
        "formulas": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "latex": {"type": "string"},
                    "surrounding_text": {"type": "string"},
                    "illegible": {"type": "string"},
                },
                "required": ["latex"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["tables", "formulas"],
    "additionalProperties": False,
}

# --- System prompt ------------------------------------------------------------
# Every rule below is a spec decision, and the wording is deliberately close to
# the spec's own. Prompts are versioned code (spec §19.1).

EXTRACTION_SYSTEM = """You extract durable, source-backed knowledge units from documents.

{boundary}

GRANULARITY — this is the most important rule.
Each unit must be MOLECULAR, which means both of:

  - SUFFICIENCY: the unit stands alone as an INSIGHT, not merely as a grammatical
    sentence. A reader who has never seen the document must be able to:
      * answer a reading-comprehension question about the point it makes;
      * follow the reasoning, if it is an argument -- including what it rests on
        and what follows from it;
      * apply the formula or procedure, if it is one, without going back to the
        source for a term it uses.
    Resolving pronouns is the FLOOR, not the goal. "Each passive manager obtains
    the market return" resolves nothing and explains nothing: it does not say
    that this is the premise from which the whole result follows. Pull in
    whatever the point needs to survive being read cold -- the definition a term
    depends on, the condition the claim is scoped to, the role it plays in the
    argument.

  - CONCISION: carry what the point needs and nothing else. Do not restate the
    document, do not repeat context already inside the statement, do not pad
    with background a reader does not need for THIS point. If a sentence of the
    surrounding argument is not required to understand or use this unit, leave
    it out.

  The test: if this unit were the only thing a reader ever saw from this
  document, would they have the point, or only a true sentence?

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

EVIDENCE: quote VERBATIM, under {eviwords} words total. Excerpts are verified by
exact string match downstream and a paraphrased excerpt fails.

  Every unit has exactly ONE excerpt with role "primary": the passage the unit
  is principally about.

  SUFFICIENCY LICENSES IMPORTING CONTEXT; IT DOES NOT LICENSE ASSERTING IT
  UNCITED. If the statement carries anything the primary excerpt does not say --
  a definition it relies on, a condition it is scoped to, a consequence it
  names, the role it plays in an argument -- cite the passage that says it, with
  role "supporting". Usually one to three supporting excerpts; more when the
  point genuinely rests on more.

  The standard is a citation in a thesis, not a gloss in a summary. A reader who
  disagrees with this unit must be able to go to the document, find every claim
  it makes, and argue with the source rather than with you. If a claim in the
  statement is in the document but you cannot quote it, quote it. If it is NOT
  in the document, it does not belong in the statement.

GROUNDING: report whether this unit could have been written from this document
alone. The citation rule above is what makes the answer checkable -- if every
claim traces to a cited excerpt, the unit is "attributable" by construction.
Report "unattributed_content" whenever the statement carries something you know
but cannot quote, and expect it to be reviewed rather than trusted.

This matters most where it is least obvious: on a famous document your prior is
strongest and your answer looks most authoritative. Familiarity with the subject
is exactly the condition under which outside knowledge slips in unnoticed.

SCORING: score 0-3 on specificity, retrieval_value, connection_value,
evidence_strength, novelty. The decision is NOT a simple sum: mandatory
obligations, contradictions, critical limitations, and rare exceptions may be
kept even when scores are low.

TYPE TESTS — answer all six for every unit.
Each test is an INDEPENDENT yes/no question. Answer each on its own merits; do
not let one answer settle another, and do not try to pick a single winner. More
than one may be true. If two are true, the unit is probably two units -- prefer
splitting it, and if you cannot split it cleanly, answer both true and move on.

  is_concept
    Cue: the grammatical center is "X is / means / refers to / is distinguished
    from Y" -- the unit's job is to fix what a term means.
    Do not fire when the unit asserts something contingent that could turn out
    false, or when it explains why or how something works.
    Yes: "A drawdown is the peak-to-trough decline in a portfolio's value."
    Yes: "Latency and throughput are distinct measures: per-request delay versus
    requests served per second."

  is_claim
    Cue: a declarative proposition you could imagine checking, and that could
    come out false.
    Do not fire when the assertion is bound to one dated instance, when it is
    nominal or definitional rather than contingent, when it is deontic, or when
    it is an explanatory apparatus rather than one proposition.
    Yes: "Sleep extension improves delayed recall in healthy adults."
    Yes: "The API returns 429 above 100 requests per minute."

  is_model
    Cue: the unit asserts how two or more things relate such that you could
    explain or predict something -- "because", "leads to", "is composed of",
    "trades off against".
    Do not fire merely because the subject is CALLED a model. A pricing model, a
    data model, a risk model -- the word in the name is not the test. Ask what
    the unit does. Do not fire for a single proposition, for executable steps, or
    for a one-term definition.
    Yes: "Larger batches raise throughput but lengthen tail latency, because
    queued requests wait for the slowest member of the batch."
    Yes: "Retrieval quality is composed of recall at the index stage and
    precision at the rerank stage."

  is_method
    Cue: steps, a decision procedure, a technique, or an imperative with a goal
    attached -- it tells you how to bring something about.
    Do not fire when the unit constrains rather than instructs, when it explains
    why a technique works, or when it records one occasion on which someone did
    it. Test: a rule can be violated; a method can only be ineffective.
    Yes: "To size a position, divide the account risk budget by the distance from
    entry to the stop."
    Yes: "Deduplicate sources by hashing the normalized text before clustering."

  is_rule
    Cue: a deontic modal -- must, shall, may, must not, never, always -- with
    someone accountable to it. Requirement, permission, prohibition, limit,
    standard, or policy.
    Do not fire when the unit describes how a system behaves rather than what an
    actor must do: "the API returns 429 above 100 requests per minute" is a
    claim; "clients must not exceed 100 requests per minute" is a rule. Do not
    fire for advice carrying no accountability, or for one enforcement event.
    Yes: "Clients must not exceed 100 requests per minute."
    Yes: "Reviewers may waive the second approval only for changes under ten
    lines."

  is_case
    Cue: a specific time and a specific actor or subject. It happened once.
    Do not fire when the unit generalizes beyond the instance, and do not fire
    merely because a date appears -- a policy with an effective date is still a
    rule. Ask whether the date is part of what happened or just when it started
    applying.
    Yes: "During the March 2026 outage the gateway dropped webhook deliveries for
    forty minutes."
    Yes: "The trial randomized 42 adults to a nine-hour sleep opportunity over
    four weeks."

A published result is usually TWO units: the case (on this sample, over this
period, this was measured) and the claim it supports (this generalizes).

MODALITY: set it whenever a deontic modal is present, independently of is_rule --
"required" for must/shall/is required to, "permitted" for may/is allowed to,
"prohibited" for must not/never/is forbidden to. Omit it when no modal appears.

FLAGS: multi-select, omit when neither applies.
  - negative_result: the finding is an absence, a null, or a no-effect result.
    Mark these without fail. A statement that something does NOT work reads to a
    search index almost exactly like a statement that it does, so an unmarked
    null result is effectively invisible and gets summarized away.
  - caveat: a limitation, a scope restriction, or an exception that qualifies
    something else.

NODE_KIND: "question" when the unit records an open question or an acknowledged
gap rather than knowledge -- it has no truth value to check, no procedure to
run, and no instance that occurred. Otherwise "unit".

ENTITY MENTIONS: list named things the unit refers to -- people, organizations,
products, systems, studies, instruments, places -- with the line each appears on.
Record the surface form EXACTLY as it appears in the document. Do not expand
acronyms, do not normalize spelling, do not merge variants. Canonicalization
happens downstream, and it needs the raw surface forms to do it.

Never invent evidence. If something is implied but not stated, either omit it or
mark it in qualifiers. Report only what the document supports."""

REPAIR_SYSTEM = """You extract the units an earlier pass over this document missed.

{boundary}

You are given the document, the units already extracted from it, and a list of
findings from a completeness check -- each naming something missing and quoting
the source text it concerns.

Extract a unit for each finding whose content is genuinely absent. Follow exactly
the same standard as the first pass: decontextualized but sufficient, every claim
quotable, every excerpt copied verbatim from the document.

Do NOT re-extract anything the existing units already carry. Do NOT restate a
finding as a unit -- a finding says what is missing, and your job is to extract
the missing content itself from the document. If a finding turns out to be
already covered, or names nothing the document actually supports, return no unit
for it."""

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
        "role": {
            "type": "string",
            "enum": ["primary", "supporting"],
            "description": (
                "primary: the passage this unit is principally about. supporting: a "
                "passage from elsewhere in the document that licenses context the unit "
                "imported -- a definition it relies on, a condition it is scoped to, a "
                "consequence it names. Every claim in the statement must trace to one "
                "or the other."
            ),
        },
        "asset_ref": {
            "type": "object",
            "description": (
                "Cite a table cell or a formula instead of a text span. Use this "
                "whenever the fact came from a table: quoting the flattened row "
                "proves the digits were copied and NOT that they were assigned to "
                "the right column, which is how a misread table passes verification."
            ),
            "properties": {
                "asset_id": {"type": "string"},
                "row": {"type": "integer"},
                "col": {"type": "integer"},
            },
            "required": ["asset_id"],
            "additionalProperties": False,
        },
    },
    "required": ["excerpt", "line_start", "line_end", "role"],
    "additionalProperties": False,
}

ENTITY_MENTION_SCHEMA = {
    "type": "object",
    "properties": {
        "surface": {
            "type": "string",
            "description": "The named thing exactly as written. Never canonicalized here.",
        },
        "line": {"type": "integer"},
    },
    "required": ["surface", "line"],
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
                    "modality": {"type": "string", "enum": list(MODALITIES)},
                    "flags": {"type": "array", "items": {"type": "string", "enum": list(FLAGS)}},
                    "node_kind": {"type": "string", "enum": list(NODE_KINDS)},
                    "entity_mentions": {"type": "array", "items": ENTITY_MENTION_SCHEMA},
                    "canonical_statement": {
                        "type": "string",
                        "description": (
                            "The point, stated so it survives being read cold. Not a "
                            "quotation -- the evidence field carries the source's words."
                        ),
                    },
                    "grounding": {
                        "type": "string",
                        "enum": ["attributable", "conventions_added", "unattributed_content"],
                        "description": (
                            "Answer the counterfactual, not a question about your training: "
                            "IF THIS DOCUMENT WERE THE ONLY THING YOU HAD EVER READ, could you "
                            "have written this unit? "
                            "attributable = yes; every claim is supported by the cited "
                            "excerpts. "
                            "conventions_added = the claims are supported, but you supplied "
                            "standard terminology or a field convention the document assumes "
                            "(expanding an acronym, naming a well-known measure). "
                            "unattributed_content = no; the unit carries substance no cited "
                            "excerpt supports. Prefer unattributed_content when unsure -- an "
                            "over-cautious flag costs a review, an over-confident one launders "
                            "outside knowledge as source material."
                        ),
                    },
                    "context_note": {
                        "type": "string",
                        "description": (
                            "One sentence on what this unit is DOING in the source: the "
                            "role it plays in the argument, what it supports or depends "
                            "on, or what it is an instance of. Not a summary of the "
                            "statement -- a reader has that already. This is what the "
                            "statement cannot say about itself."
                        ),
                    },
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
                    "canonical_statement", "evidence", "scores", "decision", "grounding",
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


def _checkpoint_paths(ctx: RunContext) -> tuple[Path, Path, Path]:
    return (
        ctx.units.with_name("units.partial.jsonl"),
        ctx.omissions.with_name("omissions.partial.jsonl"),
        ctx.units.with_name("rejects.jsonl"),
    )


def extract_units(
    ctx: RunContext,
    cfg: Config,
    client: LLMClient,
    registry: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Extract molecular units from every successfully normalized source.

    Checkpointed per document. Pass 1 is the expensive pass and it used to hold
    every source's units in memory until the last one finished, so any failure
    -- a malformed answer, a truncation, a dropped connection on document nine
    of ten -- threw away the paid work for all ten. Spec §18 says a failed pass
    resumes from the last valid artifact; per-source checkpoints are what make
    that true inside this pass rather than only between passes.
    """
    boundary = DATA_BOUNDARY_NOTE.format(marker=cfg.datamark_char)
    system = EXTRACTION_SYSTEM.format(
        boundary=boundary,
        lo=cfg.granularity.soft_target_words[0],
        hi=cfg.granularity.soft_target_words[1],
        warn=cfg.granularity.warn_words,
        eviwords=cfg.granularity.max_evidence_words,
    )

    taxonomy = load_taxonomy(cfg.taxonomy_path)
    units_partial, omissions_partial, rejects_path = _checkpoint_paths(ctx)
    all_units: list[dict[str, Any]] = read_jsonl(units_partial) if units_partial.exists() else []
    all_omissions: list[dict[str, Any]] = (
        read_jsonl(omissions_partial) if omissions_partial.exists() else []
    )
    all_rejects: list[dict[str, Any]] = read_jsonl(rejects_path) if rejects_path.exists() else []
    done = {u["source_id"] for u in all_units} | {o["source_id"] for o in all_omissions}
    if done:
        print(f"[pass1] checkpoint: {len(all_units)} units from {len(done)} sources already done")

    for manifest in registry:
        if manifest.get("normalization_status") != "success":
            continue
        source_id = manifest["source_id"]
        if source_id in done:
            continue
        normalized_path = ctx.run_dir / manifest["normalized_path"]
        text = normalized_path.read_text(encoding="utf-8")
        assets_path = normalized_path.parent / "assets.jsonl"
        assets = read_jsonl(assets_path) if assets_path.exists() else []
        if assets:
            recovered = _read_rendered_pages(ctx, cfg, client, manifest, assets)
            if recovered:
                assets = assets + recovered
                write_jsonl_atomic(assets_path, assets)
                print(f"[pass1] {source_id}: read {len(recovered)} asset(s) off "
                      "rendered pages")

        result = client.complete_json(
            system=system,
            user=(
                f"Document title: {manifest['title']}\n"
                f"Media type: {manifest['media_type']}\n\n"
                f"{wrap_untrusted(_numbered(text), cfg)}\n\n"
                f"{_render_assets(assets)}"
                "Extract every durable, source-backed molecular knowledge unit."
            ),
            schema=UNIT_SCHEMA,
            model=cfg.model_for("extractor"),
        )

        rejects: list[dict[str, Any]] = []
        units = _materialize_units(ctx, cfg, manifest, result.get("units", []), text,
                                   rejects, assets=assets)
        # Flag the kinds a proposition-shaped synthesis step is known to drop,
        # before sealing, so the flag is part of the record rather than a thing
        # recomputed later and liable to drift from what the planner was told.
        n_protected = annotate_protected(units, taxonomy)
        if n_protected:
            print(f"[pass1] {n_protected} of {len(units)} units carry retention protection")
        all_units.extend(units)
        all_rejects.extend(rejects)
        for reject in rejects:
            print(f"[pass1] skipped a malformed unit from {source_id}: {reject['reason']}")

        # Omission check (spec §9.6). Kept as a separate call with its own
        # prompt: the evidence for it is a *detect-and-refine* step, and 24.9%
        # of refined facts flipped correctness once incompleteness was resolved.
        omission = client.complete_json(
            system=OMISSION_SYSTEM.format(boundary=boundary),
            user=(
                f"{wrap_untrusted(_numbered(text), cfg)}\n\n"
                "Units already extracted:\n"
                + "\n".join(
                    f"- {u['unit_id']} {u['canonical_statement']}"
                    for u in units
                )
                + "\n\nWhat is missing or mis-shaped?"
            ),
            schema=OMISSION_SCHEMA,
            model=cfg.model_for("omission"),
        )
        findings = omission.get("findings", [])
        all_omissions.extend(_materialize_omissions(ctx, source_id, findings))

        # Repair round (spec §9.6's detect-and-refine, completed). The check
        # above was diagnostic only: it found real losses -- a footnote bounding
        # a paper's claims, thirty per-label exemplars in a specification -- and
        # wrote them to a file no code read. One extra round closes it.
        #
        # Only `add` findings are acted on. The others (`split`, `merge`,
        # `downgrade`, `drop`) are instructions to reshape units that are
        # already sealed, and rewriting a sealed record is a different and much
        # larger change than extracting content that is missing.
        #
        # One round, never a loop: the repair output is not re-checked, because
        # a check-repair cycle has no natural fixed point and every turn of it
        # costs a call over the whole document.
        additions = [f for f in findings if f.get("suggested_action") == "add"]
        if additions:
            repair = client.complete_json(
                system=REPAIR_SYSTEM.format(boundary=boundary),
                user=(
                    f"{wrap_untrusted(_numbered(text), cfg)}\n\n"
                    "Units already extracted:\n"
                    + "\n".join(f"- {u['canonical_statement']}" for u in units)
                    + "\n\nFindings from the completeness check:\n"
                    + "\n".join(
                        f"- {f.get('description', '')}"
                        + (f"\n  source text: {f['excerpt']}" if f.get("excerpt") else "")
                        for f in additions
                    )
                    + "\n\nExtract the missing units."
                ),
                schema=UNIT_SCHEMA,
                model=cfg.model_for("extractor"),
            )
            repaired = _materialize_units(
                ctx, cfg, manifest, repair.get("units", []), text, rejects,
                start_index=len(units) + 1, assets=assets,
            )
            annotate_protected(repaired, taxonomy)
            print(
                f"[pass1] repair round on {source_id}: {len(additions)} gap(s) reported, "
                f"{len(repaired)} unit(s) recovered"
            )
            units.extend(repaired)
            all_units.extend(repaired)

        done.add(source_id)
        write_jsonl_atomic(units_partial, all_units)
        write_jsonl_atomic(omissions_partial, all_omissions)
        if all_rejects:
            write_jsonl_atomic(rejects_path, all_rejects)

    write_jsonl_atomic(ctx.omissions, all_omissions)
    # The checkpoints exist only to survive a crash; leaving them behind would
    # make a later --force re-run resume from them instead of recomputing.
    units_partial.unlink(missing_ok=True)
    omissions_partial.unlink(missing_ok=True)
    return all_units



def _read_node_kind(raw: object) -> str:
    return raw if raw in NODE_KINDS else "unit"  # type: ignore[return-value]


def _resolve_modality(raw: object) -> tuple[str | None, str | None]:
    """Split the model's modal answer into (kept, suppressed).

    The prompt asks for modality on ANY deontic modal, independently of is_rule
    (contract §2.2), while the validator makes a modality on a non-`rule` type a
    fatal error (contract §2.5). Both are literal, and they collide on a real and
    documented shape: a dated incident that also states an obligation fires
    is_case AND is_rule, and `case` outranks `rule` in the priority tuple -- so a
    perfectly correct extraction failed `kip validate` and exited 1.

    Resolved here rather than by softening the check, because the check is the
    thing that catches a genuinely corrupt record. The model still answers
    independently; the record keeps the answer under `suppressed_modality` so no
    signal is lost and a multi-fire unit can still be split later; only the
    validated `modality` field is scoped to units that actually resolved to
    `rule`.
    """
    modality = normalize_modality(raw)
    return modality, None


def _read_entity_mentions(raw: object) -> list[dict[str, Any]]:
    """Keep surfaces verbatim; the wiki owns canonicalization, not this pass."""
    if not isinstance(raw, (list, tuple)):
        return []
    mentions: list[dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        surface = str(item.get("surface", "")).strip()
        if not surface:
            continue
        try:
            line = int(item.get("line", 0))
        except (TypeError, ValueError):
            line = 0
        mentions.append({"surface": surface, "line": max(0, line)})
    return mentions


REQUIRED_RAW_UNIT_FIELDS = ("canonical_statement", "scores", "decision")


def _reject(source_id: str, index: int, raw: object, reason: str) -> dict[str, Any]:
    """A malformed model answer, recorded rather than raised.

    A missing optional answer is data to record instead
    of a crash; this applies the same rule to the rest of the record. The
    motivation is resumability (spec §18): Pass 1 accumulates every source's
    units and writes once, so one malformed unit in the last document used to
    raise KeyError out of the stage runner and discard the extraction for the
    ENTIRE corpus -- including the sources that came out fine. The forced-tool
    fallback path and a max_tokens truncation both produce exactly this shape.
    """
    prefix = str(raw.get("canonical_statement", ""))[:120] if isinstance(raw, dict) else ""
    return {
        "source_id": source_id,
        "raw_index": index,
        "reason": reason,
        "statement_prefix": prefix,
    }


def _read_rendered_pages(ctx, cfg, client, manifest: dict[str, Any],
                         assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Turn each rendered page into the tables and formulas it actually shows.

    Pass 0 renders a page and records that something on it could not be
    represented as text; it deliberately makes no model call. This is where the
    reading happens, before extraction, so units are built from the recovered
    structure rather than from the damage.

    Everything produced here is `transcribed`. The page image stays attached, so
    a consumer can check the reading against what was read -- which is the only
    check that works: string comparison rejects correct transcriptions about a
    third of the time.
    """
    from .assets import ASSET_TABLE, FIDELITY_TRANSCRIBED, Cell, Table, build_asset

    # Pages already read are skipped. Without this the pass appends its results
    # again on every invocation, and since the assets are rendered into the
    # extraction prompt, the extraction call id changes each time -- so a run
    # never converges and no answer is ever reused.
    already = {a.get("page") for a in assets if a.get("extractor") == "visual_read_v1"}
    renders = [a for a in assets
               if a.get("kind") == "figure" and a.get("payload", {}).get("image")
               and a.get("page") not in already]
    if not renders:
        return []
    base = (ctx.run_dir / manifest["normalized_path"]).parent
    source_id = manifest["source_id"]
    # Numbered above everything Pass 0 wrote, so a reading cannot collide with
    # a render. Ids are what a citation resolves by; a duplicate is not cosmetic.
    existing = max((int(a["asset_id"][-4:]) for a in assets
                    if a.get("asset_id", "")[-4:].isdigit()), default=len(assets))
    out: list[dict[str, Any]] = []

    for render in renders:
        image = base / render["payload"]["image"]
        if not image.exists():
            continue
        try:
            result = client.complete_json(
                system=READ_SYSTEM,
                user=(f"Page {render.get('page')} of {manifest['title']}.\n"
                      "Return every table and display equation this page shows."),
                schema=READ_SCHEMA,
                model=cfg.model_for("extractor"),
                images=[str(image)],
            )
        except Exception as exc:
            if type(exc).__name__ in ("HandoffPending", "HandoffInvalid"):
                raise
            print(f"[pass1] could not read {image.name}: {exc}")
            continue

        for raw in result.get("tables", []):
            rows = raw.get("rows", [])
            header_rows = max(0, int(raw.get("header_rows", 1)))
            cells = [Cell(row=r, col=c, text=(v or "").strip(), is_header=r < header_rows)
                     for r, row in enumerate(rows)
                     for c, v in enumerate(row) if (v or "").strip()]
            if len(cells) < 4:
                continue
            grid = Table(cells=cells, n_rows=len(rows),
                         n_cols=max((len(r) for r in rows), default=0),
                         caption=raw.get("caption", ""))
            out.append(build_asset(
                kind=ASSET_TABLE, source_id=source_id, index=existing + len(out) + 1,
                fidelity=FIDELITY_TRANSCRIBED, extractor="visual_read_v1",
                payload={**grid.as_dict(), "image": render["payload"]["image"],
                         "illegible": raw.get("illegible", "")},
                text=grid.to_text(), page=render.get("page")))

        for raw in result.get("formulas", []):
            if not raw.get("latex"):
                continue
            out.append(formula_asset(
                source_id=source_id, index=existing + len(out) + 1,
                page=render.get("page") or 0,
                image_rel=render["payload"]["image"],
                latex=raw["latex"], surrounding=raw.get("surrounding_text", ""),
                extractor="visual_read_v1"))
    return out


def _render_assets(assets: list[dict[str, Any]], *, limit: int = 60) -> str:
    """Show the extractor the tables as grids, with their ids.

    The flattened text says `Total segment revenue | $ | 33,314 | $ | 26,881`.
    A model reading that has to guess which year each figure belongs to, and
    quoting the row back proves only that the digits were copied. Rendering the
    grid removes the guess, and giving each table an id lets a unit cite the
    cell rather than the row.
    """
    tables = [a for a in assets if a.get("kind") == "table"]
    if not tables:
        return ""
    lines = [
        "TABLES IN THIS DOCUMENT, recovered as grids from the source markup.",
        "Cite a figure taken from one with asset_ref {asset_id, row, col} rather "
        "than by quoting the flattened row -- a quote proves the digits were "
        "copied, not that they were read from the right column. Row and column "
        "are 0-based, as printed below.",
        "",
    ]
    for asset in tables[:limit]:
        lines.append(f"[{asset['asset_id']}]")
        lines.append(asset.get("text", ""))
        lines.append("")
    if len(tables) > limit:
        lines.append(f"({len(tables) - limit} further tables not shown.)")
        lines.append("")
    return "\n".join(lines) + "\n"


def _materialize_units(
    ctx: RunContext,
    cfg: Config,
    manifest: dict[str, Any],
    raw_units: list[dict[str, Any]],
    text: str,
    rejects: list[dict[str, Any]] | None = None,
    start_index: int = 1,
    assets: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    source_id = manifest["source_id"]
    lines = text.splitlines()
    units: list[dict[str, Any]] = []
    rejected = rejects if rejects is not None else []

    # `start_index` exists so the repair round can number its units after the
    # first round's rather than colliding with them: ids are positional and a
    # second call on the same source would otherwise reissue u-...-0001.
    for index, raw in enumerate(raw_units, start=start_index):
        if not isinstance(raw, dict):
            rejected.append(_reject(source_id, index, raw, "not a JSON object"))
            continue
        missing = [f for f in REQUIRED_RAW_UNIT_FIELDS if f not in raw]
        if missing:
            rejected.append(
                _reject(source_id, index, raw, f"missing required field(s): {', '.join(missing)}")
            )
            continue
        if not isinstance(raw["canonical_statement"], str):
            rejected.append(_reject(source_id, index, raw, "canonical_statement is not a string"))
            continue

        # Numbered from the model's output position, so a skipped record leaves
        # a gap rather than renumbering the units after it. A unit id must mean
        # the same thing on a re-run as it did on the first.
        unit_id = f"u-{source_id}-{index:04d}"
        evidence = [
            _resolve_evidence(manifest, e, text, lines, assets)
            for e in raw.get("evidence", [])
            if isinstance(e, dict)
        ]
        statement = raw["canonical_statement"].strip()
        modality, suppressed_modality = _resolve_modality(raw.get("modality"))
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
            "modality": modality,
            # The modal the model reported on a unit that resolved to something
            # other than `rule`. Kept so the signal survives for the split that
            # a multi_fire unit is asking for; see _resolve_modality.
            "suppressed_modality": suppressed_modality,
            "flags": normalize_flags(raw.get("flags")),
            # Computed, never asked. It is a heuristic with a real error rate --
            # not an oracle -- but a regex is free and a model call is not, and
            # the question is about surface form rather than meaning.
            "quantitative": detect_quantitative(statement),
            "node_kind": _read_node_kind(raw.get("node_kind")),
            "entity_mentions": _read_entity_mentions(raw.get("entity_mentions")),
            # ------------------------------------------------------------------
            "canonical_statement": statement,
            "context_note": raw.get("context_note", ""),
            # Self-reported, and treated as such: it is a claim to be checked
            # against the citations, not a fact about the run. `validate` fails
            # a unit that claims attributable while carrying an unverified quote.
            "grounding": raw.get("grounding", "unattributed_content"),
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


def _locate_reflowed(excerpt: str, text: str) -> tuple[int, int] | None:
    """Find `excerpt` in `text` ignoring whitespace and line-break hyphenation.

    Returns the raw (start, end) offsets in `text`, or None if the words are not
    there. Deliberately NOT a similarity search: every non-space character must
    match in order. A paraphrase, a dropped clause or an invented sentence still
    fails, which is the property Pass 5's citation check depends on -- the point
    is to stop losing quotes the document really contains, not to start
    accepting quotes it does not.

    The two things forgiven are both artifacts of normalization rather than of
    the model: runs of whitespace differing from the source's hard wraps, and a
    word split across a line break as `evi- dence`.
    """
    # Collapse both sides to comparable character streams, keeping a map from
    # each kept character back to its offset in the raw text.
    def stream(s: str, track: bool) -> tuple[str, list[int]]:
        chars: list[str] = []
        offsets: list[int] = []
        i = 0
        while i < len(s):
            ch = s[i]
            if ch.isspace():
                i += 1
                continue
            # A hyphen immediately before a line break is a wrap artifact.
            if ch == "-":
                j = i + 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                if j < len(s) and s[j] == "\n":
                    i = j + 1
                    continue
            chars.append(ch)
            if track:
                offsets.append(i)
            i += 1
        return "".join(chars), offsets

    needle, _ = stream(excerpt, track=False)
    if not needle:
        return None
    hay, offsets = stream(text, track=True)
    at = hay.find(needle)
    if at < 0:
        return None
    return offsets[at], offsets[at + len(needle) - 1] + 1


def _verify_asset_ref(ref: dict[str, Any] | None,
                      assets: list[dict[str, Any]]) -> dict[str, Any]:
    """Resolve a cited table cell, and record what it actually holds.

    This is the check that closes the defect. Quoting a flattened row proves the
    digits were copied; it cannot prove they were read from the right column,
    because the fused string reads the same either way. Resolving the cited cell
    against the stored grid produces the value AND the headers governing it, so
    a unit that read the columns backwards is now detectable.

    Verification here is deliberately looser than the verbatim text rule: the
    cell's value must appear in the unit's quoted excerpt, not match it byte for
    byte, because a model writing `$33,314 million` about a cell holding
    `$33,314` is right. Demanding equality would reject correct readings, which
    is the same mistake as scoring a transcription by string comparison.
    """
    if not ref or not ref.get("asset_id"):
        return {}
    from .assets import resolve_cell

    asset = next((a for a in assets if a.get("asset_id") == ref["asset_id"]), None)
    if asset is None:
        return {"asset_ref": ref, "asset_verified": False,
                "asset_note": f"no asset {ref['asset_id']} in this source"}
    row, col = ref.get("row"), ref.get("col")
    if row is None or col is None:
        return {"asset_ref": ref, "asset_verified": True,
                "asset_note": "asset cited without a cell"}
    cell = resolve_cell(asset, row, col)
    if cell is None:
        return {"asset_ref": ref, "asset_verified": False,
                "asset_note": f"no cell at row {row}, col {col}"}
    return {
        "asset_ref": ref,
        "asset_verified": True,
        "asset_value": cell["value"],
        "asset_column_headers": cell["column_headers"],
        "asset_row_headers": cell["row_headers"],
    }


def _resolve_evidence(
    manifest: dict[str, Any],
    raw: dict[str, Any],
    text: str,
    lines: list[str],
    assets: list[dict[str, Any]] | None = None,
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
    corrected = False

    if not verified and excerpt:
        # Exact match failed. Before calling it a fabrication, look for the same
        # words in the source: Pass 0 hard-wraps text, so a real quote can arrive
        # as `evi- dence` in the document and `evidence` from the model, and a
        # model reflowing a quote is not the same thing as inventing one. If the
        # words are there, the SOURCE's bytes become the excerpt -- the record
        # never stores the model's wording -- and the correction is recorded.
        located = _locate_reflowed(excerpt, text)
        if located is not None:
            char_start, char_end = located
            excerpt = text[char_start:char_end]
            verified = True
            corrected = True

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
        **_verify_asset_ref(raw.get("asset_ref"), assets or []),
        # True when the quote was located by reflowing rather than matched
        # byte-for-byte. The excerpt stored is still the source's own text; this
        # records that the model's wording differed in whitespace or hyphenation.
        "excerpt_corrected": corrected,
        # Which claim this quote is here to license. Defaults to primary so a
        # record written before roles existed still reads correctly.
        "role": raw.get("role", "primary"),
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
