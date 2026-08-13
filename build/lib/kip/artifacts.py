"""Artifact plumbing: canonical hashing, JSONL I/O, run context, stage runner.

Spec §7 (global artifact envelope), §16 (JSONL as source of truth),
§18 (orchestration and resumability).
"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator

from .config import SCHEMA_VERSION


class PipelineError(RuntimeError):
    """Raised for any contract violation that must stop the pipeline."""


# --- Hashing ------------------------------------------------------------------
# Canonical JSON (sorted keys, no incidental whitespace) makes content hashes
# stable across runs and machines. Without canonicalization, two semantically
# identical records hash differently and every resume looks like a change.


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


# --- JSONL --------------------------------------------------------------------


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise PipelineError(f"Missing artifact: {path}")
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                # Spec §16: one malformed record can be isolated. Name the line
                # so a human can repair it without re-running the whole pass.
                raise PipelineError(f"{path}:{line_number}: {exc}") from exc
    return records


def iter_jsonl(path: Path) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def write_jsonl_atomic(path: Path, records: Iterable[dict[str, Any]]) -> int:
    """Write via temp file + atomic replace.

    A partially written artifact is worse than a missing one: the stage runner
    below treats "file exists" as "stage complete", so a truncated file would be
    silently accepted on resume. Atomic replace makes that impossible.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            for record in records:
                handle.write(canonical_json(record) + "\n")
                count += 1
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return count


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise


# --- Run context --------------------------------------------------------------


@dataclass(frozen=True)
class RunContext:
    run_id: str
    root: Path

    @property
    def run_dir(self) -> Path:
        return self.root / "runs" / self.run_id

    def path(self, *parts: str) -> Path:
        return self.run_dir.joinpath(*parts)

    # Canonical artifact locations (spec §6).
    @property
    def sources_dir(self) -> Path:
        return self.path("00_original_sources")

    @property
    def normalized_dir(self) -> Path:
        return self.path("01_normalized")

    @property
    def source_registry(self) -> Path:
        return self.path("01_normalized", "source_registry.jsonl")

    @property
    def units(self) -> Path:
        return self.path("02_units", "units.jsonl")

    @property
    def omissions(self) -> Path:
        return self.path("02_units", "omissions.jsonl")

    @property
    def enriched_units(self) -> Path:
        return self.path("03_clusters", "enriched_units.jsonl")

    @property
    def clusters(self) -> Path:
        return self.path("03_clusters", "clusters.jsonl")

    @property
    def assessments(self) -> Path:
        return self.path("04_assessments", "claim_assessments.jsonl")

    @property
    def candidates(self) -> Path:
        return self.path("05_candidates", "candidates.initial.jsonl")

    @property
    def audits(self) -> Path:
        return self.path("06_audit", "audits.jsonl")

    @property
    def approved(self) -> Path:
        return self.path("06_audit", "candidates.approved.jsonl")

    @property
    def corpus_coverage(self) -> Path:
        return self.path("06_audit", "corpus_coverage.json")

    @property
    def enqueue(self) -> Path:
        return self.path("07_enqueue", "enqueue.jsonl")

    @property
    def manifest(self) -> Path:
        return self.path("run_manifest.json")


def envelope(
    ctx: RunContext,
    *,
    prompt_version: str,
    model_role: str,
    parent_artifacts: list[str],
) -> dict[str, Any]:
    """Fields every record carries (spec §7)."""
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": ctx.run_id,
        "created_at": utc_now(),
        "prompt_version": prompt_version,
        "model_role": model_role,
        "parent_artifacts": parent_artifacts,
    }


# --- Content identity ---------------------------------------------------------
# Content identity is the ASSERTION -- the statement, its evidence, and its
# source lineage -- never the labels applied to it. Classification is a
# derivation: a pure function of (canonical_statement, prompt_version,
# classifier_model). Braiding a derived label into the hash means re-deriving a
# classification forges a new content hash and validate.py rejects the corpus,
# which would make re-deriving a field a content change.
#
# Schema 3.1.0 introduced this exclusion set, so 3.0.0 content hashes are NOT
# comparable with 3.1.0 ones. That break is intentional and one-time.

DERIVED_FIELDS = frozenset(
    {
        "content_sha256",
        "created_at",
        # Legacy and current classification labels, both derived.
        "modality",
        # Retention protection: a pure function of (canonical_statement,
        # taxonomy). Changing the taxonomy must not forge a new content hash --
        # the same rule that excludes classification labels, for the same reason.
        "protected_by",
        # A deontic modal the model reported on a unit that did not resolve to
        # `rule`. Derived from the same six answers as `modality` itself, so it
        # belongs on this side of the line for the same reason.
        "suppressed_modality",
        "flags",
        "quantitative",
        "node_kind",
        "entity_mentions",
        # Stamps identifying which derivation produced the labels above.
        "migration_note",
    }
)


def seal_payload(record: dict[str, Any]) -> dict[str, Any]:
    """The subset of a record that content_sha256 is taken over.

    Exported and shared: validate.py re-seals with THIS function rather than a
    private copy, because two copies of one rule is exactly how the writer and
    the checker drift apart.
    """
    return {k: v for k, v in record.items() if k not in DERIVED_FIELDS}


def seal(record: dict[str, Any]) -> dict[str, Any]:
    """Attach content_sha256 over the semantically relevant content.

    created_at is excluded because it moves every time a pass is recomputed --
    including a `--force` recompute of the SAME run -- and a digest that changes
    when nothing was asserted differently is a digest that cannot detect
    tampering. Derived classification fields are excluded for the reason given
    above DERIVED_FIELDS.

    SCOPE, stated because the exclusion list invites the opposite reading: this
    is a WITHIN-RUN record digest, not a cross-run content identity. The
    envelope fields run_id, prompt_version, model_role and parent_artifacts are
    all inside the payload, so the same sentence extracted from the same file by
    two different runs hashes differently. Nothing in this pipeline dedups
    across runs, and adding run_id to DERIVED_FIELDS would silently change what
    `kip validate` is checking, so the honest fix is to say what the field is
    rather than to widen it.
    """
    record["content_sha256"] = stable_hash(seal_payload(record))
    return record


# --- Stage input fingerprints -------------------------------------------------
# "Output file exists" answers "did this stage finish", not "did it finish over
# the inputs it has now". Without the second answer, adding a source to a run and
# re-running the same run id silently ignores the new file, and editing an
# already-ingested file leaves the registry's original_sha256 pointing at content
# that no longer exists. Both look like clean resumes.


def fingerprint_paths(paths: Iterable[Path]) -> str:
    """Fingerprint a set of input FILES by name and content."""
    return stable_hash(sorted((p.name, file_hash(p)) for p in paths if p.is_file()))


def fingerprint_records(records: Iterable[dict[str, Any]]) -> str:
    """Fingerprint a set of input RECORDS by content, not by envelope.

    Deliberately ignores created_at and the other per-execution envelope fields:
    a stage should re-run when its inputs say something different, not when they
    were merely rewritten.
    """
    keys = ("unit_id", "cluster_id", "assessment_id", "candidate_id", "audit_id", "source_id")
    digest: list[tuple[str, str]] = []
    for record in records:
        identity = next((str(record[k]) for k in keys if k in record), "")
        content = record.get("content_sha256") or stable_hash(seal_payload(record))
        digest.append((identity, str(content)))
    return stable_hash(sorted(digest))


def _fingerprint_store(ctx: RunContext) -> Path:
    return ctx.path("stage_fingerprints.json")


def _read_fingerprints(ctx: RunContext) -> dict[str, str]:
    path = _fingerprint_store(ctx)
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return value if isinstance(value, dict) else {}


def _record_fingerprint(ctx: RunContext, name: str, fingerprint: str) -> None:
    stored = _read_fingerprints(ctx)
    stored[name] = fingerprint
    write_json_atomic(_fingerprint_store(ctx), stored)


# --- Idempotent stage runner --------------------------------------------------


def run_stage(
    *,
    ctx: RunContext,
    name: str,
    output_path: Path,
    produce: Callable[[], list[dict[str, Any]]],
    force: bool = False,
    inputs_fingerprint: str | None = None,
) -> list[dict[str, Any]]:
    """Run a pass once; on resume, return the existing artifact.

    Spec §18: a failed pass resumes from the last valid artifact, and unchanged
    sources are not reprocessed. The completion marker *is* the output file --
    combined with atomic writes above, existence implies completeness.

    `inputs_fingerprint` is what makes "unchanged" a checked claim rather than an
    assumption. When it is supplied and does not match the fingerprint recorded
    when the artifact was written, resuming would produce a corpus that is half
    old and half new with no marker anywhere saying so, so this refuses instead.
    Refusing is the conservative choice: recomputing silently would throw away
    downstream artifacts the operator may still want.
    """
    if output_path.exists() and not force:
        if inputs_fingerprint is not None:
            recorded = _read_fingerprints(ctx).get(name)
            if recorded is not None and recorded != inputs_fingerprint:
                raise PipelineError(
                    f"[{name}] cannot resume: the inputs to this stage changed since "
                    f"{output_path.name} was written (recorded {recorded[:12]}, now "
                    f"{inputs_fingerprint[:12]}). A source was added, removed, or edited. "
                    "Re-run with --force to recompute this run, or use a new run id to "
                    "keep the existing artifacts."
                )
        records = read_jsonl(output_path)
        print(f"[{name}] resume: {len(records)} records from {output_path.name}")
        return records
    records = produce()
    written = write_jsonl_atomic(output_path, records)
    if inputs_fingerprint is not None:
        _record_fingerprint(ctx, name, inputs_fingerprint)
    print(f"[{name}] wrote {written} records -> {output_path}")
    return records


def batched(items: list[Any], size: int) -> Iterator[list[Any]]:
    for start in range(0, len(items), size):
        yield items[start : start + size]


def rotate(items: list[Any], offset: int) -> list[Any]:
    """Rotate a list so different items occupy the disadvantaged middle.

    Spec §17 / §11.8. Position within a prompt is worth up to 22pp of accuracy,
    so a fixed order systematically penalizes whatever sits in the middle. This
    is deterministic (offset-driven, not random) to keep runs reproducible.
    """
    if not items:
        return items
    offset %= len(items)
    return items[offset:] + items[:offset]
