"""Render a run's units as readable markdown.

The artifacts are JSONL because that is what the pipeline writes and what
downstream consumes. This is for reading them.

    python demo/real-runs/render.py demo/real-runs/02-sharpe-v41

The argument is a kip *workspace* -- a directory containing `runs/<run-id>/` --
because that is the shape kip actually writes. The renderer reads the artifacts
from their canonical paths inside it and writes UNITS.md beside the workspace.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def _only_run(workspace: Path) -> Path:
    """The single run directory inside a demo workspace."""
    runs = sorted(p for p in (workspace / "runs").iterdir() if p.is_dir())
    if len(runs) != 1:
        raise SystemExit(f"{workspace}: expected exactly one run, found {len(runs)}")
    return runs[0]


def render(workspace: Path) -> str:
    run_dir = _only_run(workspace)
    units = [json.loads(l)
             for l in (run_dir / "02_units/units.jsonl").read_text().splitlines() if l.strip()]
    om_path = run_dir / "02_units/omissions.jsonl"
    omissions = ([json.loads(l) for l in om_path.read_text().splitlines() if l.strip()]
                 if om_path.exists() else [])

    # The normalized text is what every excerpt was cut from and what the density
    # figure is measured against -- not the original file, which may be a PDF.
    normalized = sorted((run_dir / "01_normalized").glob("*/normalized.txt"))
    if len(normalized) != 1:
        raise SystemExit(f"{run_dir}: expected one normalized.txt, found {len(normalized)}")
    words = len(normalized[0].read_text().split())
    meta_path = workspace / "meta.json"

    header = [f"# {workspace.name}", "",
              f"Rendered from `runs/{run_dir.name}/` — the run tree kip wrote. "
              f"Everything below is in those artifacts; nothing is added here.", ""]
    if meta_path.exists():
        meta_doc = json.loads(meta_path.read_text())
        if meta_doc.get("source"):
            header += [f"**Source.** {meta_doc['source']}", ""]
        if meta_doc.get("source_note"):
            header += [meta_doc["source_note"], ""]
    out = header + [
        f"- source: {words:,} words",
        f"- units: {len(units)}  (one per {words // max(len(units),1):,} words)",
        f"- omissions flagged: {len(omissions)}", ""]

    for i, u in enumerate(units, 1):
        out += [f"## {i}. {u['canonical_statement']}", ""]
        if u.get("context_note"):
            out += [f"**Role in the source.** {u['context_note']}", ""]
        for e in u.get("evidence", []):
            role = e.get("role", "primary")
            mark = "✓" if e.get("excerpt_verified") else "✗ UNVERIFIED"
            quote = e["excerpt"].replace("\n", " ")
            out += [f"- *{role}* {mark} (lines {e.get('normalized_line_start')}–"
                    f"{e.get('normalized_line_end')}): “{quote}”"]
        meta = [f"grounding: `{u.get('grounding','—')}`",
                f"decision: `{u['decision']}`",
                f"quantitative: `{u.get('quantitative')}`"]
        if u.get("candidate_topics"):
            meta.append("topics: " + ", ".join(f"`{t}`" for t in u["candidate_topics"]))
        out += ["", " · ".join(meta), ""]
        if u.get("decontextualization_note"):
            out += [f"> imported: {u['decontextualization_note']}", ""]

    if omissions:
        out += ["## What the omission check said was missing", ""]
        for o in omissions:
            out += [f"- **{o.get('kind','?')}** — {o.get('description','')}"]
        out += [""]
    return "\n".join(out)


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        path = Path(arg)
        (path / "UNITS.md").write_text(render(path))
        print("wrote", path / "UNITS.md")
