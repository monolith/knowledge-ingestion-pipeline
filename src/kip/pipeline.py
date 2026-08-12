"""Pipeline orchestration — the pass sequence with resume.

Spec §18. Each pass is a durable job keyed on its output artifact; a failed run
resumes from the last valid artifact rather than starting over.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from . import assess, audit, candidates, enqueue, extract, normalize, route
from .artifacts import (
    RunContext,
    fingerprint_paths,
    fingerprint_records,
    read_jsonl,
    run_stage,
    utc_now,
    write_json_atomic,
)
from .config import SCHEMA_VERSION, Config
from .llm import LLMClient


def discover_sources(source_dir: Path) -> list[Path]:
    return sorted(p for p in source_dir.rglob("*") if p.is_file() and not p.name.startswith("."))


def run_pipeline(
    ctx: RunContext,
    cfg: Config,
    source_dir: Path,
    *,
    stop_after: str | None = None,
    force: bool = False,
    client: LLMClient | None = None,
) -> dict[str, Any]:
    """Run passes 0-6 in order, resuming completed stages.

    `stop_after` takes a pass name so an operator can inspect intermediate
    artifacts before paying for the next stage -- useful because Pass 1 is the
    expensive one and everything downstream depends on its quality.

    `client` is an injection point, not a convenience: the demo and the
    integration tests must drive all six passes with a scripted client on a host
    with no API key and no network, and they should exercise THIS orchestrator
    rather than a parallel copy of the pass sequence that can drift from it.
    """
    stages = ["normalize", "extract", "route", "assess", "candidates", "audit", "enqueue"]
    if stop_after and stop_after not in stages:
        raise ValueError(f"unknown stage {stop_after!r}; expected one of {stages}")

    # Config errors that will abort a later pass are checked before the first
    # paid call, not when the pass they concern is reached.
    audit.check_auditor_distinct(cfg)

    def should_run(stage: str) -> bool:
        if stop_after is None:
            return True
        return stages.index(stage) <= stages.index(stop_after)

    summary: dict[str, Any] = {"run_id": ctx.run_id, "started_at": utc_now()}

    def llm() -> LLMClient:
        # Constructed lazily so Pass 0 (and the tests) never require an API key.
        nonlocal client
        if client is None:
            client = LLMClient(cfg=cfg)
        return client

    # --- Pass 0 ---------------------------------------------------------------
    # Fingerprinted on the source FILES themselves. Without this, adding a
    # document to a run and re-running the same run id resumed the old registry
    # and ignored the new file, and editing an ingested file left the registry's
    # original_sha256 pointing at content that no longer existed -- both silent.
    sources = discover_sources(source_dir)
    registry = run_stage(
        ctx=ctx,
        name="pass0-normalize",
        output_path=ctx.source_registry,
        produce=lambda: normalize.normalize_sources(ctx, sources),
        force=force,
        inputs_fingerprint=fingerprint_paths(sources),
    )
    summary["sources"] = len(registry)
    summary["quarantined"] = sum(
        1 for r in registry if r.get("normalization_status") != "success"
    )
    if not should_run("extract"):
        return _finish(ctx, cfg, summary, client)

    # --- Pass 1 ---------------------------------------------------------------
    units = run_stage(
        ctx=ctx,
        name="pass1-extract",
        output_path=ctx.units,
        produce=lambda: extract.extract_units(ctx, cfg, llm(), registry),
        force=force,
        inputs_fingerprint=fingerprint_records(registry),
    )
    summary["units"] = len(units)
    if not should_run("route"):
        return _finish(ctx, cfg, summary, client)

    # --- Pass 2 ---------------------------------------------------------------
    clusters = run_stage(
        ctx=ctx,
        name="pass2-route",
        output_path=ctx.clusters,
        produce=lambda: route.route_and_cluster(ctx, cfg, llm(), units),
        force=force,
        inputs_fingerprint=fingerprint_records(units),
    )
    summary["clusters"] = len(clusters)
    if not should_run("assess"):
        return _finish(ctx, cfg, summary, client)

    # --- Pass 3 ---------------------------------------------------------------
    assessments = run_stage(
        ctx=ctx,
        name="pass3-assess",
        output_path=ctx.assessments,
        produce=lambda: assess.assess_clusters(ctx, cfg, llm(), units, clusters),
        force=force,
        inputs_fingerprint=fingerprint_records(units + clusters),
    )
    summary["assessments"] = len(assessments)
    if not should_run("candidates"):
        return _finish(ctx, cfg, summary, client)

    # --- Pass 4 ---------------------------------------------------------------
    proposals = run_stage(
        ctx=ctx,
        name="pass4-candidates",
        output_path=ctx.candidates,
        produce=lambda: candidates.plan_candidates(ctx, cfg, llm(), assessments, units),
        force=force,
        inputs_fingerprint=fingerprint_records(assessments),
    )
    summary["candidates"] = len(proposals)
    if not should_run("audit"):
        return _finish(ctx, cfg, summary, client)

    # --- Pass 5 ---------------------------------------------------------------
    if ctx.audits.exists() and not force:
        audits = read_jsonl(ctx.audits)
        approved = read_jsonl(ctx.approved) if ctx.approved.exists() else []
        print(f"[pass5-audit] resume: {len(audits)} audits, {len(approved)} approved")
    else:
        audits, approved = audit.audit_candidates(
            ctx, cfg, llm(), proposals, units, assessments
        )
        print(f"[pass5-audit] wrote {len(audits)} audits, {len(approved)} approved")
    summary["audits"] = len(audits)
    summary["approved"] = len(approved)
    summary["verdicts"] = _count(a["verdict"] for a in audits)
    if not should_run("enqueue"):
        return _finish(ctx, cfg, summary, client)

    # --- Step 6 ---------------------------------------------------------------
    events = run_stage(
        ctx=ctx,
        name="pass6-enqueue",
        output_path=ctx.enqueue,
        produce=lambda: enqueue.enqueue_approved(ctx, approved),
        force=force,
        inputs_fingerprint=fingerprint_records(approved),
    )
    summary["queue_events"] = len(events)
    return _finish(ctx, cfg, summary, client)


def _count(values) -> dict[str, int]:
    out: dict[str, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return out


def _finish(
    ctx: RunContext, cfg: Config, summary: dict[str, Any], client: LLMClient | None
) -> dict[str, Any]:
    summary["finished_at"] = utc_now()
    # A scripted client spends no tokens and carries no usage counter, so the
    # field is reported only when there is something real to report.
    usage = getattr(client, "usage", None)
    if usage is not None:
        summary["usage"] = usage.as_dict()

    # Spec §7: the run manifest records the evidence-tier configuration in force
    # -- which checker did grounding, whether the auditor differed from the
    # proposer, batch size -- because all three change the output's error rate.
    write_json_atomic(
        ctx.manifest,
        {
            "run_id": ctx.run_id,
            "spec_version": SCHEMA_VERSION,
            "config": cfg.manifest_fragment(),
            "summary": summary,
        },
    )
    return summary
