"""Render a run's units as readable markdown.

The artifacts are JSONL because that is what the pipeline writes and what
downstream consumes. This is for reading them.

    python demo/real-runs/render.py demo/real-runs/02-sharpe-v41
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def render(run_dir: Path) -> str:
    units = [json.loads(l) for l in (run_dir / "units.jsonl").read_text().splitlines() if l.strip()]
    om_path = run_dir / "omissions.jsonl"
    omissions = ([json.loads(l) for l in om_path.read_text().splitlines() if l.strip()]
                 if om_path.exists() else [])

    # Most runs ship their source beside the artifacts. A run over a copyrighted
    # document cannot, so it records the word count in meta.json instead -- the
    # density figure is the point of these runs and must not depend on whether
    # the source could be redistributed.
    source = run_dir / "source.md"
    meta_path = run_dir / "meta.json"
    if source.exists():
        words = len(source.read_text().split())
    elif meta_path.exists():
        words = int(json.loads(meta_path.read_text())["source_words"])
    else:
        raise SystemExit(f"{run_dir}: needs source.md or meta.json with source_words")

    header = [f"# {run_dir.name}", ""]
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
