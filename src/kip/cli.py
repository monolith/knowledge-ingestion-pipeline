"""Command-line interface.

Spec §16: JSONL is the source of truth; every command here reads or writes it.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from .artifacts import RunContext, read_jsonl
from .config import default_config
from .pipeline import discover_sources, run_pipeline
from .trace import trace_leaf
from .validate import validate_run


def _default_run_id() -> str:
    return "run-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def cmd_run(args: argparse.Namespace) -> int:
    root = Path(args.workspace).resolve()
    ctx = RunContext(run_id=args.run_id or _default_run_id(), root=root)
    source_dir = Path(args.sources).resolve()
    if not source_dir.is_dir():
        print(f"error: --sources is not a directory: {source_dir}", file=sys.stderr)
        return 2

    cfg = default_config()
    if args.no_datamark:
        cfg = type(cfg)(**{**cfg.__dict__, "datamark": False})

    # Copy originals into the run so the artifact tree is self-contained and the
    # provenance chain survives the source directory changing later (spec §3.1).
    ctx.sources_dir.mkdir(parents=True, exist_ok=True)
    for path in discover_sources(source_dir):
        target = ctx.sources_dir / path.name
        if not target.exists():
            shutil.copy2(path, target)

    print(f"run_id: {ctx.run_id}")
    print(f"workspace: {ctx.run_dir}")
    summary = run_pipeline(
        ctx, cfg, ctx.sources_dir, stop_after=args.stop_after, force=args.force
    )
    print("\n--- summary ---")
    print(json.dumps(summary, indent=2))
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    ctx = RunContext(run_id=args.run_id, root=Path(args.workspace).resolve())
    report = validate_run(ctx)
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


def cmd_trace(args: argparse.Namespace) -> int:
    ctx = RunContext(run_id=args.run_id, root=Path(args.workspace).resolve())
    chain = trace_leaf(ctx, args.target)
    if chain is None:
        print(f"error: nothing found for {args.target!r}", file=sys.stderr)
        return 1
    print(chain)
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    ctx = RunContext(run_id=args.run_id, root=Path(args.workspace).resolve())
    paths = {
        "units": ctx.units,
        "omissions": ctx.omissions,
        "clusters": ctx.clusters,
        "assessments": ctx.assessments,
        "candidates": ctx.candidates,
        "audits": ctx.audits,
        "approved": ctx.approved,
        "enqueue": ctx.enqueue,
    }
    path = paths[args.artifact]
    if not path.exists():
        print(f"error: {path} does not exist", file=sys.stderr)
        return 1
    for record in read_jsonl(path)[: args.limit]:
        print(json.dumps(record, indent=2 if args.pretty else None))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="kip",
        description="Knowledge Ingestion Pipeline (spec v3.0)",
    )
    parser.add_argument(
        "--workspace", default=".kip", help="Artifact root (default: .kip)"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run the pipeline over a directory of sources")
    run.add_argument("--sources", required=True, help="Directory of input files")
    run.add_argument("--run-id", default=None)
    run.add_argument(
        "--stop-after",
        default=None,
        choices=["normalize", "extract", "route", "assess", "candidates", "audit", "enqueue"],
        help="Stop after this pass so intermediate artifacts can be inspected",
    )
    run.add_argument("--force", action="store_true", help="Recompute completed passes")
    run.add_argument(
        "--no-datamark",
        action="store_true",
        help="Disable injection datamarking (not recommended; see spec §20.4)",
    )
    run.set_defaults(func=cmd_run)

    validate = sub.add_parser("validate", help="Check provenance and schema integrity")
    validate.add_argument("run_id")
    validate.set_defaults(func=cmd_validate)

    trace = sub.add_parser("trace", help="Print the provenance chain for a candidate or unit")
    trace.add_argument("run_id")
    trace.add_argument("target", help="candidate_id, queue_event_id, or unit_id")
    trace.set_defaults(func=cmd_trace)

    show = sub.add_parser("show", help="Print records from an artifact")
    show.add_argument("run_id")
    show.add_argument(
        "artifact",
        choices=["units", "omissions", "clusters", "assessments", "candidates",
                 "audits", "approved", "enqueue"],
    )
    show.add_argument("--limit", type=int, default=10)
    show.add_argument("--pretty", action="store_true")
    show.set_defaults(func=cmd_show)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
