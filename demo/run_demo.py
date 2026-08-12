"""Runnable end-to-end demo: two bundled documents through passes 0-6.

Runs with NO API key by default. Every model call is served by the scripted
client below, so the demo is deterministic, free, and offline -- which is the
only way it can double as a regression test (tests/test_pipeline_integration.py
executes this file).

What it demonstrates, in one run:

- the kt-v1 type block being derived in code from six independent boolean
  answers, and surviving every artifact hand-off intact;
- `quantitative` computed by regex rather than asked for, so its value here is
  whatever `taxonomy.detect_quantitative` actually returns, not a scripted
  answer;
- the audit catching a deliberately overconfident candidate -- one positive
  trial and one null replication proposed as "established" -- and producing a
  corrected version beside it rather than overwriting it.

`--live` swaps in the real Anthropic client. It costs money, needs a key, and is
not what this demo is for; it exists so the same code path can be checked
against a real model when one is available.

Usage:
    python demo/run_demo.py                     # scripted, temp workspace
    python demo/run_demo.py --workspace .kip    # keep the artifacts somewhere
    python demo/run_demo.py --live              # real API (key required)
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# The demo lives beside the package rather than inside it, so a plain
# `python demo/run_demo.py` out of a fresh checkout has to find src/ itself.
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from kip.artifacts import RunContext, read_jsonl  # noqa: E402
from kip.config import Config, default_config  # noqa: E402
from kip.pipeline import run_pipeline  # noqa: E402
from kip.testing import ScriptedClientBase  # noqa: E402
from kip.validate import validate_run  # noqa: E402

SOURCES_DIR = Path(__file__).resolve().parent / "sources"


# --- Scripted client ----------------------------------------------------------
# Marker dispatch, call counting and schema checking all live in
# kip.testing.ScriptedClientBase, which the integration tests' FakeClient also
# subclasses. Build contract §4.2 says extend the one pattern rather than invent
# a second; a prompt edit that breaks routing should break one place, not two
# that must then be repaired separately.
#
# What is specific to the demo is only the transcript below: the tests' fake
# proves WIRING with two throwaway documents, while this one plays a full canned
# transcript against the two documents bundled here, so the demo's output is a
# realistic corpus rather than a fixture.
#
# Extraction keys off the document TITLE, which arrives as trusted metadata
# outside the <untrusted_document> block. Anything inside that block has had its
# spaces replaced by the datamark character, so multi-word markers would not
# survive there -- that mangling is the injection defense working as designed.


class ScriptedClient(ScriptedClientBase):
    """Canned responses for every pass, checked against each pass's schema."""

    # -- Pass 1 ---------------------------------------------------------------

    def _pass_extract(self, user: str) -> dict[str, Any]:
        if "sleep extension trial" in user:
            return {"units": TRIAL_UNITS}
        if "memory consolidation review" in user:
            return {"units": REVIEW_UNITS}
        raise AssertionError("extraction asked about an unbundled document")

    def _pass_omission(self, user: str) -> dict[str, Any]:
        if "sleep extension trial" in user or "randomized" in user:
            return {
                "findings": [
                    {
                        "kind": "missing",
                        "description": (
                            "The baseline measurement occasion is not represented as a unit."
                        ),
                        "suggested_action": "add",
                    }
                ]
            }
        return {"findings": []}

    # -- Pass 2 ---------------------------------------------------------------

    def _pass_enrich(self, user: str) -> dict[str, Any]:
        if "src-sleep-extension-trial" in user:
            return {
                "context": "From a randomized trial of sleep extension and delayed recall.",
                "entities": ["sleep extension", "delayed recall"],
            }
        return {
            "context": "From a practitioner review of sleep and memory consolidation.",
            "entities": ["slow-wave sleep", "delayed recall"],
        }

    def _pass_label(self, user: str) -> dict[str, Any]:
        if "8.2%" in user or "no statistically significant" in user:
            return {
                "topic_label": "Sleep extension and delayed recall",
                "routing_reason": "These units bear on whether extending sleep improves recall.",
            }
        return {
            "topic_label": "Sleep laboratory practice",
            "routing_reason": "These units concern how the recall protocol is run and scored.",
        }

    # -- Pass 3 ---------------------------------------------------------------

    def _pass_assess(self, user: str) -> dict[str, Any]:
        positive = _ids_stating(user, "improved 8.2%")
        null = _ids_stating(user, "no statistically significant")

        if positive and null:
            # The contradiction the whole pipeline exists to preserve: one
            # positive trial, one independent null replication.
            return {
                "assessments": [
                    {
                        "canonical_claim": (
                            "Sleep extension improves delayed recall in healthy adults."
                        ),
                        "coarse_stance": "contradicts",
                        "relationship_bucket": "contested",
                        "relationship_subtype": "partially_contradicts",
                        "subtype_confidence": 0.55,
                        "supporting_unit_ids": positive,
                        "opposing_unit_ids": null,
                        "contradiction_evidence": [
                            {"unit_id": positive[0], "excerpt": "improved 8.2%"},
                            {"unit_id": null[0], "excerpt": "no statistically significant"},
                        ],
                        "uncertainty": "high",
                        "synthesis": (
                            "One randomized trial reported improvement; an independent "
                            "replication found none."
                        ),
                        "recommended_action": "Create a contested-evidence leaf.",
                    }
                ]
            }

        ids = _unit_ids(user)
        return {
            "assessments": [
                {
                    "canonical_claim": _first_statement(user),
                    "coarse_stance": "insufficient_evidence",
                    "relationship_bucket": "complementary" if len(ids) > 1 else "singleton",
                    "relationship_subtype": "complementary" if len(ids) > 1 else "singleton",
                    "subtype_confidence": 0.5,
                    "supporting_unit_ids": ids,
                    "opposing_unit_ids": [],
                    "uncertainty": "moderate",
                    "synthesis": "These units describe procedure and terminology; nothing conflicts.",
                    "recommended_action": "Record as reference material.",
                }
            ]
        }

    # -- Pass 4 ---------------------------------------------------------------

    def _pass_plan(self, user: str) -> dict[str, Any]:
        assessment_ids = _ids(user, r"asmt-\d+")
        unit_ids = _ids(user, r"u-src-[a-z0-9\-]+")

        if "coarse_stance: contradicts" in user:
            # Deliberately overconfident. The audit below is supposed to catch
            # this, and a demo where nothing is caught demonstrates nothing.
            return {
                "candidates": [
                    {
                        "title": "Sleep extension improves delayed recall in adults",
                        "knowledge_state": "established",
                        "priority": 3,
                        "summary": "Extending sleep opportunity improves delayed recall.",
                        "assertions": [
                            {
                                "text": "Sleep extension improves delayed recall.",
                                "assessment_ids": assessment_ids[:1],
                            }
                        ],
                        "source_unit_ids": unit_ids,
                        "suggested_operation": "create",
                    }
                ]
            }

        return {
            "candidates": [
                {
                    "title": "Delayed-recall protocol: definitions and laboratory rules",
                    "knowledge_state": "operational",
                    "priority": 2,
                    "summary": (
                        "How delayed recall is defined, scored, and what participants "
                        "must avoid before a session."
                    ),
                    "assertions": [
                        {
                            "text": "Delayed recall is scored as a proportion of learned items.",
                            "assessment_ids": assessment_ids[:1],
                        }
                    ],
                    "source_unit_ids": unit_ids,
                    "suggested_operation": "create",
                }
            ]
        }

    # -- Pass 5 ---------------------------------------------------------------

    # -- Pass 5b ---------------------------------------------------------------

    def _pass_corpus_coverage(self, user: str) -> dict[str, Any]:
        """The demo plans one leaf from ten units, so most of them are orphaned.

        Answered honestly rather than optimistically: this transcript exists to
        exercise the wiring, and a canned "represented" would make the one pass
        that detects lost content useless as a demonstration of it.
        """
        return {
            "reasoning": (
                "Ten units were extracted and one candidate reached the queue, carrying two "
                "of them. The trial's design details and the review's qualifying statements "
                "are not deduplication -- they say different things and none of them reached "
                "an assertion."),
            "verdict": "gaps",
            "key_insights_captured": True,
            "definitions_captured": True,
            "fairly_represented": False,
            "missing": [{
                "what_is_lost": (
                    "The trial's sample size and duration, and the review's scope "
                    "qualifications, reached no assertion."),
                "consequence": (
                    "A reader of the output cannot tell how large or how long the trial was, "
                    "so cannot weigh it against the replication that disagrees."),
            }],
            "notes": ["scripted demo transcript; the single-leaf plan is the demo's, not a "
                      "recommendation"],
        }

    def _pass_audit(self, user: str) -> dict[str, Any]:
        assessment_ids = _ids(user, r"asmt-\d+")
        overstated = "knowledge_state: established" in user

        if not overstated:
            return {
                "verdict": "pass",
                "checks": {
                    "coverage": "pass",
                    "contradiction_handling": "pass",
                    "scope_fidelity": "pass",
                    "source_independence": "pass",
                    "duplication": "pass",
                },
                "findings": [],
                "required_fixes": [],
                "raw_source_escalation": [],
                "auditor_confidence": 0.8,
            }

        return {
            "verdict": "fix",
            "checks": {
                "coverage": "pass",
                "contradiction_handling": "fail",
                "scope_fidelity": "warn",
                "source_independence": "pass",
                "duplication": "pass",
            },
            "findings": [
                "The candidate presents contested evidence as established.",
                "The null replication is absent from the summary.",
            ],
            "required_fixes": ["Use a mixed-evidence title and the contested state."],
            "raw_source_escalation": [],
            "auditor_confidence": 0.7,
            "corrected_candidate": {
                "title": "Sleep extension and adult memory: mixed evidence",
                "knowledge_state": "contested",
                "summary": (
                    "One randomized trial reported improved delayed recall; an "
                    "independent replication found no significant effect."
                ),
                "assertions": [
                    {
                        "text": (
                            "One randomized trial reported improved delayed recall, and an "
                            "independent replication did not reproduce it."
                        ),
                        "assessment_ids": assessment_ids[:1],
                    }
                ],
            },
        }


# --- Prompt parsing helpers ---------------------------------------------------
# The scripted client reads the rendered prompts the same way a model would --
# by looking at the text it was given -- so it keeps working if unit ids or
# cluster membership change.


def _ids(text: str, pattern: str) -> list[str]:
    seen: list[str] = []
    for match in re.findall(pattern, text):
        if match not in seen:
            seen.append(match)
    return seen


def _unit_ids(text: str) -> list[str]:
    return [line.split()[0] for line in text.splitlines() if line.startswith("u-")]


def _ids_stating(text: str, marker: str) -> list[str]:
    """Unit ids whose rendered statement contains `marker` (Pass 3 layout)."""
    found: list[str] = []
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("u-"):
            current = line.split()[0]
        elif current and "statement:" in line and marker in line:
            found.append(current)
    return found


def _first_statement(text: str) -> str:
    for line in text.splitlines():
        if "statement:" in line:
            return line.split("statement:", 1)[1].strip()
    return "Reference material."


# --- Canned extraction output -------------------------------------------------
# Note what these records do NOT contain: no `type`, no `family`, no
# `quantitative`, no `gates_fired`. A model answers six independent booleans and
# nothing else; every derived field in the artifact tree is computed by
# the statement text.



def _scores(**overrides: int) -> dict[str, int]:
    base = {
        "specificity": 3,
        "retrieval_value": 3,
        "connection_value": 2,
        "evidence_strength": 3,
        "novelty": 2,
    }
    base.update(overrides)
    return base


TRIAL_UNITS: list[dict[str, Any]] = [
    {
        "node_kind": "unit",
        "entity_mentions": [{"surface": "nine-hour sleep opportunity", "line": 5}],
        "canonical_statement": (
            "A randomized trial assigned 42 healthy adults to a nine-hour sleep "
            "opportunity or their habitual schedule for four weeks."
        ),
        "decontextualization_note": "Named the design and the population.",
        "evidence": [
            {
                "excerpt": (
                    "The trial randomized 42 healthy adults to a nine-hour sleep "
                    "opportunity or to their habitual schedule over four weeks."
                ),
                "line_start": 5,
                "line_end": 5,
                "role": "primary",
            }
        ],
        "scores": _scores(),
        "decision": "keep", "grounding": "attributable",
    },
    {
        # Two tests fire on purpose: a measurement taken on one sample is a
        # case, and the generalization it is offered as support for is a claim.
        # That is the documented split signal, and it must reach the artifacts
        # as multi_fire rather than being silently resolved.
        "node_kind": "unit",
        "entity_mentions": [{"surface": "extension group", "line": 10}],
        "canonical_statement": (
            "Delayed word recall improved 8.2% in the sleep-extension group versus "
            "1.1% in controls."
        ),
        "decontextualization_note": "Named the intervention explicitly.",
        "evidence": [
            {
                "excerpt": (
                    "Delayed word recall improved 8.2% in the extension group versus "
                    "1.1% in controls."
                ),
                "line_start": 10,
                "line_end": 10,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=3),
        "decision": "keep", "grounding": "attributable",
    },
    {
        "node_kind": "unit",
        "entity_mentions": [{"surface": "extension group", "line": 11}],
        "canonical_statement": (
            "Total sleep time rose by 47 minutes per night in the sleep-extension group."
        ),
        "decontextualization_note": "Named the group the increase applies to.",
        "evidence": [
            {
                "excerpt": "Total sleep time rose by 47 minutes per night in the extension group.",
                "line_start": 11,
                "line_end": 11,
                "role": "primary",
            }
        ],
        "scores": _scores(),
        "decision": "keep", "grounding": "attributable",
    },
    {
        "flags": ["caveat"],
        "node_kind": "unit",
        "entity_mentions": [],
        "canonical_statement": (
            "The sleep-extension trial was not blinded and followed participants for "
            "only four weeks, so durability beyond one month is unknown."
        ),
        "decontextualization_note": "Named the trial the limitation applies to.",
        "evidence": [
            {
                "excerpt": (
                    "The trial was not blinded, and follow-up lasted only four weeks, so "
                    "durability beyond one month is unknown."
                ),
                "line_start": 15,
                "line_end": 15,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=1),
        "decision": "keep", "grounding": "attributable",
    },
    {
        # Nothing fires: a question has no truth value to check, no procedure to
        # run, and no instance that occurred. It leaves the type system and is
        # carried as a question node instead.
        "node_kind": "question",
        "entity_mentions": [],
        "canonical_statement": (
            "Whether sleep extension improves delayed recall in adults over sixty-five "
            "is untested."
        ),
        "decontextualization_note": "Named the intervention and the untested population.",
        "evidence": [
            {
                "excerpt": "Whether the same effect holds in adults over sixty-five remains untested.",
                "line_start": 19,
                "line_end": 19,
                "role": "primary",
            }
        ],
        "scores": _scores(specificity=2, evidence_strength=1),
        "decision": "keep", "grounding": "attributable",
    },
]

REVIEW_UNITS: list[dict[str, Any]] = [
    {
        "node_kind": "unit",
        "entity_mentions": [{"surface": "Delayed recall", "line": 5}],
        "canonical_statement": (
            "Delayed recall is the proportion of learned items a participant reproduces "
            "after a retention interval of twelve hours or more."
        ),
        "decontextualization_note": "None needed; the sentence already stands alone.",
        "evidence": [
            {
                "excerpt": (
                    "Delayed recall is the proportion of learned items a participant "
                    "reproduces after a retention interval of twelve hours or more."
                ),
                "line_start": 5,
                "line_end": 5,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=1),
        "decision": "keep", "grounding": "attributable",
    },
    {
        "node_kind": "unit",
        "entity_mentions": [{"surface": "Hippocampal replay", "line": 9}],
        "canonical_statement": (
            "Hippocampal replay during slow-wave sleep strengthens cortical traces, so "
            "shortening slow-wave sleep reduces next-day recall."
        ),
        "decontextualization_note": "None needed; the mechanism is stated in full.",
        "evidence": [
            {
                "excerpt": (
                    "Hippocampal replay during slow-wave sleep strengthens cortical "
                    "traces, so shortening slow-wave sleep reduces next-day recall."
                ),
                "line_start": 9,
                "line_end": 9,
                "role": "primary",
            }
        ],
        "scores": _scores(),
        "decision": "keep", "grounding": "attributable",
    },
    {
        # The one unanimous flag. "X had no effect" reads to a search index
        # almost exactly like "X had an effect", so an unmarked null result is
        # effectively invisible and gets summarized out of existence.
        "flags": ["negative_result"],
        "node_kind": "unit",
        "entity_mentions": [{"surface": "sleep-extension protocol", "line": 13}],
        "canonical_statement": (
            "An independent replication of the sleep-extension protocol found no "
            "statistically significant effect on delayed recall."
        ),
        "decontextualization_note": "Named the protocol that was replicated.",
        "evidence": [
            {
                "excerpt": (
                    "An independent replication of the sleep-extension protocol found no "
                    "statistically significant overall effect on delayed recall."
                ),
                "line_start": 13,
                "line_end": 13,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=3),
        "decision": "keep", "grounding": "attributable",
    },
    {
        "modality": "prohibited",
        "node_kind": "unit",
        "entity_mentions": [],
        "canonical_statement": (
            "Participants must not consume caffeine within eight hours of a scheduled "
            "sleep session."
        ),
        "decontextualization_note": "None needed; the actor and the constraint are explicit.",
        "evidence": [
            {
                "excerpt": (
                    "Participants must not consume caffeine within eight hours of a "
                    "scheduled sleep session."
                ),
                "line_start": 17,
                "line_end": 17,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=1),
        "decision": "keep", "grounding": "attributable",
    },
    {
        "node_kind": "unit",
        "entity_mentions": [],
        "canonical_statement": (
            "To score the delayed-recall task, count the correctly reproduced items and "
            "divide by the number of items presented at learning."
        ),
        "decontextualization_note": "Named the task being scored.",
        "evidence": [
            {
                "excerpt": (
                    "To score the recall task, count the correctly reproduced items and "
                    "divide by the number of items presented at learning."
                ),
                "line_start": 18,
                "line_end": 18,
                "role": "primary",
            }
        ],
        "scores": _scores(novelty=1),
        "decision": "keep", "grounding": "attributable",
    },
]


# --- Reporting ----------------------------------------------------------------


def _bar(count: int, width: int = 24) -> str:
    return "#" * min(count, width)



def dual_write_table(units: list[dict[str, Any]]) -> list[str]:
    """Legacy label beside the derived type -- the evaluation's control arm."""
    lines = [f"  {'legacy unit_type':<22}{'type':<14}{'family':<12}statement"]
    for unit in units:
        statement = unit["canonical_statement"]
        if len(statement) > 58:
            statement = statement[:55] + "..."
        lines.append(
            f"  {unit.get('unit_type', '?'):<22}"
            f"{unit.get('type', '?'):<14}"
            f"{unit.get('family') or '-':<12}"
            f"{statement}"
        )
    return lines


def print_report(
    ctx: RunContext,
    summary: dict[str, Any],
    client: Any,
    live: bool,
) -> dict[str, Any]:
    units = read_jsonl(ctx.units)
    enriched = read_jsonl(ctx.enriched_units)
    candidates = read_jsonl(ctx.candidates)
    approved = read_jsonl(ctx.approved)
    report = validate_run(ctx)

    def section(title: str) -> None:
        print()
        print(title)
        print("-" * len(title))

    section("pipeline")
    for key in ("sources", "units", "clusters", "assessments", "candidates",
                "audits", "approved", "queue_events"):
        if key in summary:
            print(f"  {key:<14} {summary[key]}")
    if not live:
        counts = client.call_counts()
        print(f"  {'model calls':<14} {sum(counts.values())} (scripted, no tokens spent)")
        for name, count in sorted(counts.items()):
            print(f"      {name:<16} {count}")

    section("knowledge types (kt-v1)")

    section("dual write: the retained legacy label beside the derived type")
    for line in dual_write_table(units):
        print(line)

    section("entity mentions carried into 03_clusters/enriched_units.jsonl")
    mentions = [m["surface"] for record in enriched for m in record.get("entity_mentions", [])]
    print(f"  {len(mentions)} mentions on {len(enriched)} enriched units")
    for surface in sorted(set(mentions)):
        print(f"      {surface}")

    section("what the audit changed")
    if candidates and approved:
        initial, final = candidates[0], approved[0]
        print(f"  proposed : [{initial['knowledge_state']}] {initial['title']}")
        print(f"  approved : [{final['knowledge_state']}] {final['title']}")
        print(f"  verdict  : {final.get('audit_verdict')}  "
              f"(v{initial['candidate_version']} kept on disk, v{final['candidate_version']} queued)")

    section("validation")
    print(f"  ok: {report['ok']}")
    for error in report["errors"]:
        print(f"  ERROR   {error}")
    for warning in report["warnings"]:
        print(f"  warning {warning}")

    section("artifacts")
    print(f"  {ctx.run_dir}")
    print(f"  kip --workspace {ctx.root} show {ctx.run_id} units --pretty")
    print(f"  kip --workspace {ctx.root} trace {ctx.run_id} {units[0]['unit_id']}")
    return report


# --- Entry point --------------------------------------------------------------


def build_client(live: bool, cfg: Config) -> Any:
    if not live:
        return ScriptedClient()
    # Imported here, not at module scope: the scripted path must keep working on
    # a host with no anthropic package and no API key.
    from kip.llm import LLMClient

    return LLMClient(cfg=cfg)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="run_demo.py",
        description="Run the knowledge ingestion pipeline over two bundled documents.",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="Artifact root (default: a fresh temp directory, printed on exit)",
    )
    parser.add_argument("--run-id", default=None)
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call the real API instead of the scripted client (needs ANTHROPIC_API_KEY)",
    )
    args = parser.parse_args(argv)

    root = Path(args.workspace).resolve() if args.workspace else Path(
        tempfile.mkdtemp(prefix="kip-demo-")
    )
    run_id = args.run_id or "demo-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    ctx = RunContext(run_id=run_id, root=root)
    cfg = default_config()
    client = build_client(args.live, cfg)

    print("knowledge-ingestion demo")
    print(f"  mode      : {'live API' if args.live else 'scripted client (offline, free)'}")
    print(f"  sources   : {SOURCES_DIR}")
    print(f"  workspace : {ctx.run_dir}")
    print()

    summary = run_pipeline(ctx, cfg, SOURCES_DIR, client=client)
    report = print_report(ctx, summary, client, args.live)

    # Warnings are expected output here -- a multi-fire unit and an abstaining
    # question unit are both in the bundled documents on purpose. Only errors
    # mean the demo is broken.
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
