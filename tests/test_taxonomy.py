"""Tests for the kt-v1 knowledge-type taxonomy and its migration.

Everything here is pure and offline: the vocabulary, the derivations, the legacy
map, the content-identity invariant that makes re-classification possible at
all, and the validator's health checks. No API key, no network.
"""

from __future__ import annotations

import hashlib

from pathlib import Path

import pytest

from kip.artifacts import DERIVED_FIELDS, RunContext, seal, seal_payload, write_jsonl_atomic
from kip.config import SCHEMA_VERSION
from kip.migrate import MIGRATED_TAXONOMY_VERSION, migrate_run, migrate_unit, migrate_units
from kip.taxonomy import (
    FAMILIES,
    FAMILY_OF,
    FLAGS,
    LEGACY_MAP,
    LEGACY_TYPES,
    LEGACY_UNMAPPED,
    MODALITIES,
    NODE_KINDS,
    TAXONOMY_VERSION,
    TYPE_TESTS,
    TYPES,
    UNCLASSIFIED,
    derive_family,
    derive_type,
    detect_quantitative,
    gates_fired,
    legacy_summary,
    multi_fire,
    normalize_flags,
    normalize_modality,
)
from kip.extract import UNIT_TYPES, UNIT_SCHEMA
from kip.validate import validate_run


def fired(*names: str) -> dict[str, bool]:
    return {name: name in names for name in TYPE_TESTS}


# --- Vocabulary ---------------------------------------------------------------
# Build contract §1: the vocabulary is duplicated verbatim across plugins, so it
# is pinned by value here rather than by reference to itself.


def test_vocabulary_matches_the_contract():
    assert TAXONOMY_VERSION == "kt-v1"
    assert TYPES == ("case", "rule", "method", "concept", "model", "claim")
    assert UNCLASSIFIED == "unclassified"
    assert TYPE_TESTS == (
        "is_case", "is_rule", "is_method", "is_concept", "is_model", "is_claim",
    )
    assert FAMILY_OF == {
        "case": "episodic",
        "rule": "procedural",
        "method": "procedural",
        "concept": "semantic",
        "model": "semantic",
        "claim": "semantic",
    }
    assert FAMILIES == ("semantic", "procedural", "episodic")
    assert MODALITIES == ("required", "permitted", "prohibited")
    assert FLAGS == ("negative_result", "caveat")
    assert NODE_KINDS == ("unit", "question")


def test_every_type_has_a_test_and_a_family():
    assert len(TYPE_TESTS) == len(TYPES)
    for test_name, type_name in zip(TYPE_TESTS, TYPES):
        assert test_name == f"is_{type_name}"
        assert FAMILY_OF[type_name] in FAMILIES


# --- derive_type / derive_family ----------------------------------------------


@pytest.mark.parametrize("test_name,expected", list(zip(TYPE_TESTS, TYPES)))
def test_derive_type_maps_each_test_to_its_type(test_name: str, expected: str):
    assert derive_type(fired(test_name)) == expected


def test_derive_type_abstains_when_nothing_fires():
    """No silent default: an unfired classification is a visible terminal state."""
    assert derive_type(fired()) == UNCLASSIFIED
    assert derive_type({}) == UNCLASSIFIED


def test_derive_type_uses_tuple_order_as_priority():
    """Earlier entries win. Case beats everything; claim wins only alone."""
    assert derive_type(fired("is_case", "is_claim")) == "case"
    assert derive_type(fired("is_rule", "is_method", "is_claim")) == "rule"
    assert derive_type(fired("is_method", "is_model")) == "method"
    assert derive_type(fired("is_concept", "is_model", "is_claim")) == "concept"
    assert derive_type(fired("is_model", "is_claim")) == "model"
    assert derive_type(fired("is_claim")) == "claim"


def test_derive_type_ignores_unknown_keys():
    assert derive_type({"is_vibe": True, "is_rule": True}) == "rule"


def test_derive_family():
    assert derive_family("case") == "episodic"
    assert derive_family("rule") == "procedural"
    assert derive_family("method") == "procedural"
    assert derive_family("concept") == "semantic"
    assert derive_family("model") == "semantic"
    assert derive_family("claim") == "semantic"
    assert derive_family(UNCLASSIFIED) is None
    assert derive_family("nonsense") is None


# --- gates_fired / multi_fire -------------------------------------------------


def test_gates_fired_counts_only_known_tests():
    assert gates_fired(fired()) == 0
    assert gates_fired(fired("is_claim")) == 1
    assert gates_fired(fired("is_case", "is_claim")) == 2
    assert gates_fired(dict(fired("is_claim"), is_vibe=True)) == 1


def test_multi_fire_is_two_or_more():
    """Uncertainty is structural: no confidence number is asked for or stored."""
    assert multi_fire(fired()) is False
    assert multi_fire(fired("is_claim")) is False
    assert multi_fire(fired("is_case", "is_claim")) is True
    assert multi_fire(fired("is_case", "is_rule", "is_claim")) is True


def test_no_confidence_field_anywhere_in_the_unit_schema():
    unit_properties = UNIT_SCHEMA["properties"]["units"]["items"]["properties"]
    assert "classification_confidence" not in unit_properties
    assert "type_confidence" not in unit_properties


# --- normalizers --------------------------------------------------------------


def test_normalize_flags_drops_unknowns_and_duplicates():
    assert normalize_flags(["caveat", "caveat", "risk", "negative_result"]) == [
        "caveat", "negative_result",
    ]
    assert normalize_flags(None) == []
    assert normalize_flags("caveat") == []


def test_normalize_modality():
    assert normalize_modality("required") == "required"
    assert normalize_modality("recommended") is None
    assert normalize_modality(None) is None


# --- detect_quantitative ------------------------------------------------------

QUANTITATIVE_POSITIVES = [
    "Recall improved 8.2% in the sleep-extension group.",
    "The index holds 1,200 documents.",
    "Monthly cost fell to $1,200 after the migration.",
    "The ratio of winners to losers was 3:1.",
    "End-to-end latency sits between 5-10 ms.",
    "Throughput exceeds 100 requests per minute.",
    "n=240 participants completed the protocol.",
    "The effect was significant at p<0.01.",
    "Spawns are capped at 4 per agent.",
    "The working set grew to 115k tokens.",
    "Retrieval failures dropped by 49 percent.",
    "The 95% CI was 0.31 to 0.62.",
]

# The documented false positives. Each of these has a digit in it and none of
# them carries quantitative force -- that distinction is the whole point of
# computing this field instead of asking a model whether a number is present.
QUANTITATIVE_NEGATIVES = [
    "The trial ran in 2026.",                                    # bare year
    "The policy took effect in 2019 and remains in force.",      # bare year
    "See §9.3 for the unit schema.",                             # section reference
    "Upgrade to v3.0 before deploying.",                         # version number
    "Python 3.12 is the minimum supported runtime.",             # version number
    "The outage began on 2026-08-08.",                           # ISO date
    "The incident review was filed on 8/8/2026.",                # slashed date
    "The report is dated August 8 and was circulated.",          # written date
    "Ticket TS-999 tracks the regression.",                      # ticket id
    "Step 3 normalizes the source text.",                        # list ordinal
    "Claims are the residual type in this taxonomy.",            # no digits at all
]


@pytest.mark.parametrize("statement", QUANTITATIVE_POSITIVES)
def test_detect_quantitative_positives(statement: str):
    assert detect_quantitative(statement) is True


@pytest.mark.parametrize("statement", QUANTITATIVE_NEGATIVES)
def test_detect_quantitative_negatives(statement: str):
    assert detect_quantitative(statement) is False


def test_detect_quantitative_handles_empty_input():
    assert detect_quantitative("") is False


def test_date_is_stripped_before_the_year_pattern_runs():
    """Order in _NON_QUANTITATIVE matters: strip whole dates before bare years.

    Removing "2026" from "2026-08-08" first would leave "-08-08", which the
    numeric-range pattern then matches. This asserts the ordering directly
    rather than trusting a comment.
    """
    assert detect_quantitative("The window closed 2026-08-08 without incident.") is False


# --- Legacy map ---------------------------------------------------------------


def test_legacy_labels_are_fully_accounted_for():
    """Every one of the 20 legacy labels is mapped or explicitly deferred."""
    assert set(UNIT_TYPES) == set(LEGACY_TYPES)
    assert len(UNIT_TYPES) == 20
    assert set(LEGACY_MAP) & set(LEGACY_UNMAPPED) == set()
    assert set(LEGACY_MAP) | set(LEGACY_UNMAPPED) == set(UNIT_TYPES)


def test_the_honest_count_is_fifteen_of_twenty():
    assert len(LEGACY_MAP) == 15
    assert len(LEGACY_UNMAPPED) == 5
    assert "15 of 20" in legacy_summary()


def test_legacy_map_targets_are_valid_vocabulary():
    for legacy, (unit_type, modality, flags) in LEGACY_MAP.items():
        assert unit_type in TYPES or unit_type is None, legacy
        assert modality in MODALITIES or modality is None, legacy
        assert set(flags) <= set(FLAGS), legacy
        # Modality is only meaningful on a rule; the validator treats anything
        # else as an error, so the map must never seed one.
        if modality is not None:
            assert unit_type == "rule", legacy


# --- Content identity ---------------------------------------------------------
# The blocker this whole change set exists to clear.


def _unit_record(**overrides: object) -> dict[str, object]:
    record = {
        "unit_id": "u-src-0001",
        "source_id": "src",
        "canonical_statement": "Recall improved 8.2% in the sleep-extension group.",
        # Empty by default so these records can go through the real validator
        # without needing a normalized source on disk; the hash tests below add
        # evidence explicitly.
        "evidence": [],
        "scores": {"specificity": 3},
        "decision": "keep",
        "created_at": "2026-08-08T00:00:00+00:00",
        "unit_type": "quantitative_result",
        "type": "claim",
        "family": "semantic",
        "type_tests": fired("is_claim"),
        "gates_fired": 1,
        "multi_fire": False,
        "modality": None,
        "flags": [],
        "quantitative": True,
        "node_kind": "unit",
        "entity_mentions": [],
        "taxonomy_version": TAXONOMY_VERSION,
        "classifier_model": "some-model",
    }
    record.update(overrides)
    return record


def test_schema_version_is_bumped():
    assert SCHEMA_VERSION == "3.1.0"


def test_seal_payload_excludes_every_derived_field():
    payload = seal_payload(_unit_record())
    assert set(payload) & DERIVED_FIELDS == set()
    assert "canonical_statement" in payload
    assert "evidence" in payload


def test_reclassification_does_not_change_content_sha256():
    """Content identity is the assertion, not the labels applied to it.

    Without this, re-deriving a classification forges a new content hash and
    `kip validate` rejects the corpus -- which would make the taxonomy
    migration structurally impossible.
    """
    original = seal(_unit_record())

    reclassified = seal(
        _unit_record(
            unit_type="observation",
            type="case",
            family="episodic",
            type_tests=fired("is_case", "is_claim"),
            gates_fired=2,
            multi_fire=True,
            modality="required",
            flags=["caveat"],
            quantitative=False,
            node_kind="question",
            entity_mentions=[{"surface": "Sleep Study", "line": 3}],
            taxonomy_version="kt-v2-imaginary",
            classifier_model="a-different-model",
            migration_note="re-derived by hand",
        )
    )

    assert reclassified["content_sha256"] == original["content_sha256"]


def test_changing_the_assertion_does_change_content_sha256():
    """The seal must still catch real tampering; the exclusion is narrow."""
    cited = _unit_record(evidence=[{"excerpt": "improved 8.2%", "excerpt_sha256": "abc"}])
    original = seal(dict(cited))

    edited = seal(dict(cited, canonical_statement="Recall did not improve."))
    assert edited["content_sha256"] != original["content_sha256"]

    evidence_edited = seal(
        dict(cited, evidence=[{"excerpt": "not in the source", "excerpt_sha256": "abc"}])
    )
    assert evidence_edited["content_sha256"] != original["content_sha256"]


def test_validate_reseal_uses_the_same_rule_as_seal(tmp_path: Path):
    """One copy of the exclusion rule, exercised through the real validator."""
    ctx = RunContext(run_id="run-seal", root=tmp_path)
    write_jsonl_atomic(ctx.units, [seal(_unit_record())])

    from kip.artifacts import read_jsonl

    units = read_jsonl(ctx.units)
    units[0]["type"] = "case"
    units[0]["family"] = "episodic"
    units[0]["type_tests"] = fired("is_case")
    write_jsonl_atomic(ctx.units, units)

    report = validate_run(ctx)
    assert not [e for e in report["errors"] if "content hash mismatch" in e], report["errors"]


# --- Migration ----------------------------------------------------------------


def _legacy_unit(unit_id: str, unit_type: str, statement: str) -> dict[str, object]:
    return seal(
        {
            "unit_id": unit_id,
            "source_id": "src",
            "unit_type": unit_type,
            "canonical_statement": statement,
            "evidence": [],
            "decision": "keep",
            "created_at": "2026-01-01T00:00:00+00:00",
        }
    )


@pytest.mark.parametrize("legacy", sorted(LEGACY_MAP))
def test_every_mapped_legacy_label_migrates_to_valid_vocabulary(legacy: str):
    migrated = migrate_unit(_legacy_unit("u-1", legacy, "A statement."))
    assert migrated["type"] in TYPES + (UNCLASSIFIED,)
    assert migrated["family"] == FAMILY_OF.get(migrated["type"])
    assert migrated["taxonomy_version"] == MIGRATED_TAXONOMY_VERSION
    assert migrated["migration_note"] is None
    assert set(migrated["flags"]) <= set(FLAGS)


def test_open_question_becomes_a_question_node_not_a_type():
    migrated = migrate_unit(_legacy_unit("u-1", "open_question", "Does it scale?"))
    assert migrated["node_kind"] == "question"
    assert migrated["type"] == UNCLASSIFIED
    assert migrated["family"] is None


def test_null_result_keeps_its_negative_result_flag():
    """The one unanimous flag: an unmarked null result is invisible to search."""
    migrated = migrate_unit(_legacy_unit("u-1", "null_result", "No effect was found."))
    assert migrated["type"] == "claim"
    assert migrated["flags"] == ["negative_result"]


def test_obligation_and_prohibition_carry_modality():
    assert migrate_unit(_legacy_unit("u-1", "obligation", "X must Y."))["modality"] == "required"
    assert (
        migrate_unit(_legacy_unit("u-2", "prohibition", "X must not Y."))["modality"]
        == "prohibited"
    )


@pytest.mark.parametrize("legacy", sorted(LEGACY_UNMAPPED))
def test_unmapped_labels_are_reported_never_guessed(legacy: str):
    migrated = migrate_unit(_legacy_unit("u-1", legacy, "A statement."))
    assert migrated["type"] == UNCLASSIFIED
    assert migrated["family"] is None
    assert legacy in migrated["migration_note"]


def test_migration_re_derives_quantitative_by_code():
    """The legacy label is not trusted; the regex answers it either way."""
    labelled = migrate_unit(
        _legacy_unit("u-1", "quantitative_result", "The trial ran in 2026.")
    )
    assert labelled["quantitative"] is False

    unlabelled = migrate_unit(_legacy_unit("u-2", "fact", "Latency fell to 12 ms."))
    assert unlabelled["quantitative"] is True


def test_migration_preserves_content_sha256():
    original = _legacy_unit("u-1", "fact", "Latency fell to 12 ms.")
    before = original["content_sha256"]
    assert migrate_unit(original)["content_sha256"] == before


def test_migration_is_idempotent():
    once = migrate_unit(_legacy_unit("u-1", "exception", "Except on weekends."))
    twice = migrate_unit(dict(once))
    assert once == twice


def test_migration_summary_reports_honest_counts():
    units = [
        _legacy_unit("u-1", "fact", "Latency fell to 12 ms."),
        _legacy_unit("u-2", "null_result", "No effect was found."),
        _legacy_unit("u-3", "observation", "Someone saw something."),
        _legacy_unit("u-4", "metadata", "Author: someone."),
        _legacy_unit("u-5", "open_question", "Does it scale?"),
    ]
    migrated, summary = migrate_units(units)

    assert summary["units"] == 5
    assert summary["mapped"] == 3
    assert summary["unmapped"] == 2
    assert summary["unmapped_by_label"] == {"metadata": 1, "observation": 1}
    assert summary["questions"] == 1
    assert summary["quantitative"] == 1
    # u-1 (fact -> claim, no flags) is the only unflagged claim; u-2 carries
    # negative_result and is therefore not residual.
    assert summary["unflagged_claims"] == 1
    assert summary["type_histogram"]["claim"] == 2
    assert summary["type_histogram"][UNCLASSIFIED] == 3
    assert all(u["taxonomy_version"] == MIGRATED_TAXONOMY_VERSION for u in migrated)


def test_migration_reseals_a_corpus_written_under_schema_3_0_0(tmp_path: Path):
    """The upgrade path. 3.0.0 hashed `unit_type`, so its hashes do not verify
    under 3.1.0 -- `kip migrate-taxonomy` is what repairs that, and it is the
    first thing anyone upgrading an existing run will hit.
    """
    from kip.artifacts import read_jsonl, stable_hash

    def old_seal(record: dict[str, object]) -> dict[str, object]:
        payload = {k: v for k, v in record.items() if k not in ("content_sha256", "created_at")}
        record["content_sha256"] = stable_hash(payload)
        return record

    ctx = RunContext(run_id="run-3-0-0", root=tmp_path)
    write_jsonl_atomic(
        ctx.units,
        [
            old_seal(
                {
                    "unit_id": "u-1",
                    "source_id": "src",
                    "unit_type": "fact",
                    "canonical_statement": "Latency fell to 12 ms.",
                    "evidence": [],
                    "decision": "keep",
                    "created_at": "2026-01-01T00:00:00+00:00",
                }
            )
        ],
    )

    before = validate_run(ctx)
    assert not before["ok"]
    assert any("content hash mismatch" in e for e in before["errors"])

    migrate_run(ctx)
    after = validate_run(ctx)
    assert after["ok"], after["errors"]
    assert read_jsonl(ctx.units)[0]["type"] == "claim"


def test_migrate_run_rewrites_the_artifact_and_validates(tmp_path: Path):
    ctx = RunContext(run_id="run-migrate", root=tmp_path)
    write_jsonl_atomic(
        ctx.units,
        [
            _legacy_unit("u-1", "fact", "Latency fell to 12 ms."),
            _legacy_unit("u-2", "obligation", "Clients must not exceed the limit."),
        ],
    )

    summary = migrate_run(ctx)
    assert summary["units"] == 2

    from kip.artifacts import read_jsonl

    migrated = read_jsonl(ctx.units)
    assert {u["taxonomy_version"] for u in migrated} == {MIGRATED_TAXONOMY_VERSION}

    # Re-running must be a no-op, not a compounding rewrite.
    assert migrate_run(ctx)["units"] == 2
    assert read_jsonl(ctx.units) == migrated


# --- Validator health checks --------------------------------------------------


def _write_units(tmp_path: Path, units: list[dict[str, object]]) -> RunContext:
    ctx = RunContext(run_id="run-validate", root=tmp_path)
    write_jsonl_atomic(ctx.units, [seal(u) for u in units])
    return ctx


def test_validate_rejects_an_unknown_type(tmp_path: Path):
    ctx = _write_units(tmp_path, [_unit_record(type="anecdote", family="semantic")])
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("unknown type" in e for e in report["errors"])


def test_validate_rejects_an_inconsistent_family(tmp_path: Path):
    ctx = _write_units(tmp_path, [_unit_record(type="claim", family="episodic")])
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("inconsistent with" in e for e in report["errors"])


def test_validate_rejects_modality_on_a_non_rule(tmp_path: Path):
    ctx = _write_units(tmp_path, [_unit_record(type="claim", modality="required")])
    report = validate_run(ctx)
    assert not report["ok"]
    assert any("non-rule type" in e for e in report["errors"])


def test_validate_warns_on_residual_claim_absorption(tmp_path: Path):
    units = [
        _unit_record(unit_id=f"u-{i}", type="claim", family="semantic", flags=[])
        for i in range(4)
    ]
    units.append(_unit_record(unit_id="u-rule", type="rule", family="procedural"))
    ctx = _write_units(tmp_path, units)

    report = validate_run(ctx)
    assert report["ok"], report["errors"]
    assert any("residual-absorption alarm" in w for w in report["warnings"])
    assert report["counts"]["unflagged_claims"] == 4


def test_validate_warns_about_dead_labels_split_candidates_and_abstains(tmp_path: Path):
    units = [
        _unit_record(
            unit_id="u-split",
            type="case",
            family="episodic",
            type_tests=fired("is_case", "is_claim"),
            gates_fired=2,
            multi_fire=True,
        ),
        _unit_record(
            unit_id="u-none",
            type=UNCLASSIFIED,
            family=None,
            type_tests=fired(),
            gates_fired=0,
        ),
    ]
    ctx = _write_units(tmp_path, units)

    report = validate_run(ctx)
    assert report["ok"], report["errors"]
    assert any("split candidates" in w for w in report["warnings"])
    assert any("unclassified" in w for w in report["warnings"])
    assert any("'claim' was never used" in w for w in report["warnings"])
    assert report["counts"]["multi_fire"] == 1
    assert report["counts"]["unclassified"] == 1


def test_validate_ignores_units_that_predate_the_taxonomy(tmp_path: Path):
    """An unmigrated corpus is still a valid corpus."""
    ctx = _write_units(
        tmp_path,
        [
            {
                "unit_id": "u-old",
                "source_id": "src",
                "unit_type": "fact",
                "canonical_statement": "Something.",
                "evidence": [],
                "created_at": "2026-01-01T00:00:00+00:00",
            }
        ],
    )
    report = validate_run(ctx)
    assert report["ok"], report["errors"]
    assert "classified_units" not in report["counts"]


# --- Known limits of the quantitative heuristic -------------------------------
# `detect_quantitative` is a heuristic with a measurable error rate, not an
# oracle, and taxonomy.py is byte-identical across the ingestion and wiki
# plugins by contract -- so a gap is recorded here rather than patched in one
# copy and left in the other. These are xfail, not skip: a revision that closes
# a gap makes the case XPASS, which is the signal to delete the entry and
# tighten the assertion. See docs/SPECIFICATION.md §9.3.

QUANTITATIVE_FALSE_POSITIVES = [
    "Follow steps 1-3 to configure the gateway.",   # plural escapes the `step \d` strip
    "See sections 2 to 4 of the handbook.",
    "Call the on-call engineer at 555-0134.",       # phone number reads as a range
    "The meeting runs from 9:00 to 10:30.",         # clock time reads as a ratio
]


@pytest.mark.xfail(
    reason="the strip list is keyed on singular and symbol forms real prose rarely uses",
    strict=False,
)
@pytest.mark.parametrize("statement", QUANTITATIVE_FALSE_POSITIVES)
def test_step_ranges_and_clock_times_are_a_known_false_positive(statement: str):
    assert detect_quantitative(statement) is False


def test_the_rate_family_is_detected():
    """"N <plural noun> per <period>" carries force and must not be missed.

    This is the extraction prompt's own is_claim example, so a miss here would
    contradict the documentation in the same repository.
    """
    for statement in (
        "The API returns 429 above 100 requests per minute.",
        "The gateway handled 2000 messages per day.",
        "The team closed 15 tickets per week.",
        "Throughput reached 500 documents per hour.",
    ):
        assert detect_quantitative(statement) is True, statement


def test_a_non_string_statement_never_reaches_the_regex():
    """detect_quantitative takes a string; the callers must not hand it anything else.

    `migrate.py` read `canonical_statement` straight out of a record, so a unit
    whose field was missing or numeric aborted the entire migration with a
    TypeError raised three frames down inside a regex.
    """
    from kip.migrate import migrate_unit

    for bad in (3.5, None, ["a list"], {"a": "dict"}):
        unit = {"unit_id": "u-1", "unit_type": "fact", "canonical_statement": bad}
        assert migrate_unit(unit)["quantitative"] is False, bad


def test_nothing_in_the_pipeline_gates_on_the_heuristic():
    """Why the gaps above are tolerable: a wrong answer costs a retrieval hint.

    Recorded as a test so that turning `quantitative` into a filter -- which is
    what would make its error rate expensive -- fails here first.
    """
    package = Path(__file__).resolve().parent.parent / "src" / "kip"
    for path in sorted(package.glob("*.py")):
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            for forbidden in ('if unit["quantitative"]', 'if u["quantitative"]',
                              'if record["quantitative"]'):
                assert forbidden not in stripped, f"{path.name}: {stripped}"


# sha256 of taxonomy.py with line 3 (the plugin-identifying docstring line)
# removed -- the same constant the wiki-graph suite pins. Enforced in both repos
# so a standalone install still detects vocabulary drift, with no sibling
# checkout to compare against. A deliberate vocabulary change updates this hash
# in BOTH repos in the same commit.
CANONICAL_BODY_SHA256 = "3fe0b65a5a54603cf8f909a35c5a5e2295b275ca82d901e983d79c637322857a"


def test_taxonomy_matches_the_pinned_canonical_hash():
    from pathlib import Path as _Path

    from kip import taxonomy as _taxonomy

    lines = _Path(_taxonomy.__file__).read_text(encoding="utf-8").splitlines()
    del lines[2]
    digest = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    assert digest == CANONICAL_BODY_SHA256, (
        "taxonomy.py has drifted from the canonical vocabulary. If the edit was "
        "deliberate, apply it to BOTH plugins and update CANONICAL_BODY_SHA256 "
        "in both test suites."
    )
