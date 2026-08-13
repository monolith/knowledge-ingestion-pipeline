"""Render a run folder's README: an overview for a person, a map for a model.

    python demo/real-runs/render.py demo/real-runs/<run-folder> [...]

Writes `README.md` beside the workspace, NOT inside `runs/`, so the artifact
tree stays exactly what the pipeline wrote. Nothing in the pipeline produces or
consumes this file.

WHY IT LOOKS LIKE THIS. A run folder is eight numbered directories of JSONL and
a person opening it has no idea where to start; a model opening it has the
opposite problem, since the readable summary is the one file it should NOT be
reading -- the machine-readable handoff is `07_enqueue/enqueue.jsonl` and the
evidence is in `02_units/units.jsonl` and `01_normalized/*/assets.jsonl`. So the
README does three things: says what the run is, tells a model exactly which
files to read and in what order, and then shows the content -- including the
assets, rendered, because a table nobody can see is a table nobody checks.

Everything here is read out of the run's own artifacts. Nothing is added from
elsewhere, so the README cannot claim more than the run does.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

#: What each directory holds. Fixed text, because the layout is fixed by the
#: pipeline -- but the row is only emitted when the directory is present, so a
#: run that stopped early does not advertise files it never wrote.
FOLDERS = [
    ("00_original_sources", "The source documents exactly as ingested, byte for byte."),
    ("01_normalized", "One directory per source: `normalized.txt` (the flat text every "
                      "citation resolves against), `assets.jsonl` (tables, formulas and "
                      "figures the flat text could not hold), `manifest.json`, and "
                      "`assets/` for any rendered page images."),
    ("02_units", "`units.jsonl` — every extracted knowledge unit with its verbatim "
                 "evidence and character offsets. `omissions.jsonl` — what the "
                 "completeness check found missing. `rejects.jsonl` if any record "
                 "failed materialization."),
    ("03_clusters", "Which units were routed together for comparison, and why."),
    ("04_assessments", "One judgment per claim: does the evidence support it, contradict "
                       "it, or settle nothing, and how many INDEPENDENT sources it rests on."),
    ("05_candidates", "Proposed knowledge-base entries, before audit."),
    ("06_audit", "`audits.jsonl` — the adversarial review of each candidate, with "
                 "deterministic check results. `corpus_coverage.json` — whether the "
                 "output fairly represents the whole corpus."),
    ("07_enqueue", "**`enqueue.jsonl` is the handoff.** One idempotent event per "
                   "approved entry. This is the file a consuming knowledge base reads."),
    ("_handoff", "The complete record of every model call: `pending.jsonl` holds the "
                 "requests, `responses.jsonl` the answers. Copying `responses.jsonl` "
                 "into a fresh workspace replays the entire run from cache."),
]

FIDELITY_NOTE = {
    "exact": "structure recovered from markup the source itself carried — citable as a quote",
    "transcribed": "a model or geometry read it — a READING, not a quote; compare by "
                   "meaning, not by string",
    "inferred": "a model described what it could not transcribe — never evidence",
}


def _only_run(workspace: Path) -> Path:
    runs = sorted(p for p in (workspace / "runs").iterdir() if p.is_dir())
    if len(runs) != 1:
        raise SystemExit(f"{workspace}: expected exactly one run, found {len(runs)}")
    return runs[0]


def _jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _rel(run_dir: Path, workspace: Path, *parts: str) -> str:
    return "/".join(("runs", run_dir.name) + parts)


def _table_markdown(payload: dict[str, Any], limit: int = 12) -> list[str]:
    """A stored grid as a markdown table, headers first.

    Rendered rather than described because the whole point of keeping a table as
    a grid is that a reader can see which column a figure sits under. A cell
    reference in a citation is checkable only against something visible.
    """
    from kip.assets import from_payload  # noqa: PLC0415

    table = from_payload(payload)
    if not table.n_rows or not table.n_cols:
        return []
    rows: list[list[str]] = []
    for r in range(min(table.n_rows, limit)):
        row = []
        for c in range(table.n_cols):
            cell = table.cell_at(r, c)
            text = (cell.text if cell else "").replace("|", "\\|").replace("\n", " ")
            row.append(text.strip() or " ")
        rows.append(row)
    if not rows:
        return []
    out = ["| " + " | ".join(rows[0]) + " |",
           "|" + "|".join(["---"] * len(rows[0])) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
    if table.n_rows > limit:
        out.append("")
        out.append(f"*({table.n_rows - limit} further rows in the stored grid.)*")
    return out


def _assets_section(run_dir: Path, workspace: Path, units: list[dict]) -> list[str]:
    """Every asset, with its fidelity, its provenance and its content shown."""
    normalized = run_dir / "01_normalized"
    bundles = [(d, _jsonl(d / "assets.jsonl")) for d in sorted(normalized.iterdir())
               if d.is_dir()] if normalized.exists() else []
    bundles = [(d, a) for d, a in bundles if a]
    if not bundles:
        return [
            "## Assets", "",
            "None. This source carried no tables, formulas or figures — the flat text in "
            "`01_normalized/` is the whole of it. An empty asset bundle is a result, not "
            "a gap.", "",
        ]

    # Which units cite which asset, so a reader can go from the picture to the claim.
    citers: dict[str, list[str]] = {}
    for u in units:
        for e in u.get("evidence", []):
            aid = (e.get("asset_ref") or {}).get("asset_id")
            if aid:
                citers.setdefault(aid, []).append(u["unit_id"])

    out = ["## Assets", ""]
    total = sum(len(a) for _, a in bundles)
    kinds: dict[str, int] = {}
    fidelities: dict[str, int] = {}
    for _, assets in bundles:
        for a in assets:
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
            fidelities[a["fidelity"]] = fidelities.get(a["fidelity"], 0) + 1
    cited_n = sum(1 for _, assets in bundles for a in assets if a["asset_id"] in citers)
    out += [
        f"**{total} asset{'s' if total != 1 else ''}** — "
        + ", ".join(f"{n} {k}" for k, n in sorted(kinds.items())) + ". "
        + f"{cited_n} cited by at least one unit"
        + (f", {total - cited_n} not cited." if total - cited_n else "."),
        "",
        ("An uncited asset is not a failure. A source carries structure that is not "
         "content -- a navigation box marked up as a table, a page rendered to check "
         "one equation on it -- and capturing it losslessly while citing nothing from "
         "it is the correct outcome." if total - cited_n else ""),
        "",
        "Fidelity is part of the record, because the kinds are not equally trustworthy:",
        "",
    ]
    for f, n in sorted(fidelities.items()):
        out.append(f"- **{f}** ({n}) — {FIDELITY_NOTE.get(f, '')}")
    out += ["", "Evidence cites an asset with `asset_ref {asset_id, row, col}` for a table "
                "cell, or `{asset_id}` for a formula. A cell reference resolves to the "
                "value **and** the headers governing it, which is what makes a figure "
                "checkable rather than merely quoted.", ""]

    for src_dir, assets in bundles:
        rel_dir = _rel(run_dir, workspace, "01_normalized", src_dir.name)
        out += [
            f"### `{src_dir.name}`", "",
            f"[`normalized.txt`]({rel_dir}/normalized.txt) · "
            f"[`assets.jsonl`]({rel_dir}/assets.jsonl) · "
            f"[`manifest.json`]({rel_dir}/manifest.json)", "",
        ]
        for a in assets:
            payload = a.get("payload", {})
            page = f" · page {a['page']}" if a.get("page") else ""
            cited = citers.get(a["asset_id"], [])
            cite_note = (f" · cited by {len(cited)} unit{'s' if len(cited) != 1 else ''}"
                         if cited else " · not cited by any unit")
            out += [
                f"#### `{a['asset_id']}`", "",
                f"{a['kind']} · **{a['fidelity']}** · extractor `{a['extractor']}`"
                f"{page}{cite_note}", "",
            ]
            if a["kind"] == "formula":
                latex = payload.get("latex", "")
                if latex:
                    # Displayed as math so it is legible, and repeated as source so
                    # the exact string that a citation is checked against is visible.
                    out += [f"$${latex}$$", "", "```latex", latex, "```", ""]
                else:
                    out += ["*No LaTeX recovered; the presentation markup is kept in "
                            "`assets.jsonl` so a later pass can read it.*", ""]
                if payload.get("surrounding_text"):
                    out += [f"> {payload['surrounding_text']}", ""]
            elif a["kind"] == "table":
                if payload.get("caption"):
                    out += [f"**{payload['caption']}**", ""]
                grid = _table_markdown(payload)
                if grid:
                    out += grid + [""]
            elif a["kind"] == "figure":
                image = payload.get("image")
                if image:
                    out += [f"![{a['asset_id']}]({rel_dir}/{image})", ""]
            if cited:
                out += ["Cited by: " + ", ".join(f"`{c}`" for c in cited[:8])
                        + (" …" if len(cited) > 8 else ""), ""]
    return out


def render(workspace: Path) -> str:
    run_dir = _only_run(workspace)
    events = _jsonl(run_dir / "07_enqueue" / "enqueue.jsonl")
    if not events:
        raise SystemExit(f"{run_dir}: no 07_enqueue/enqueue.jsonl -- run did not reach pass 6")
    units = _jsonl(run_dir / "02_units" / "units.jsonl")
    omissions = _jsonl(run_dir / "02_units" / "omissions.jsonl")
    audits = _jsonl(run_dir / "06_audit" / "audits.jsonl")
    registry = _jsonl(run_dir / "01_normalized" / "source_registry.jsonl")
    coverage_path = run_dir / "06_audit" / "corpus_coverage.json"
    coverage = json.loads(coverage_path.read_text()) if coverage_path.exists() else {}

    citations = [e for u in units for e in u.get("evidence", [])]
    verified = sum(1 for e in citations if e.get("excerpt_verified"))
    run = run_dir.name

    out = [
        f"# {workspace.name}", "",
        f"A complete run of the `kip` ingestion pipeline over "
        + ", ".join(f"`{m['title']}`" for m in registry) + ".",
        "",
        f"**{len(units)} knowledge units** · **{len(citations)} citations** "
        f"({verified} verified) · **{len(events)} entries handed off** · run `{run}` "
        f"· schema `{events[0]['schema_version']}`",
        "",
        "---", "",
        "## Reading this folder",
        "",
        "**If you are a person:** the [entries](#the-knowledge-handed-off) below are the "
        "output — what a knowledge base would receive. The [assets](#assets) are the "
        "tables, formulas and page images recovered from the source, shown as they are "
        "stored.",
        "",
        "**If you are a model asked to ingest this run, do not work from this file.** It "
        "is a rendering and it is lossy. Read, in order:",
        "",
        f"1. [`{_rel(run_dir, workspace, '07_enqueue', 'enqueue.jsonl')}`]"
        f"({_rel(run_dir, workspace, '07_enqueue', 'enqueue.jsonl')}) — **the handoff.** "
        "One JSON event per approved entry, each with `payload.title`, "
        "`payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This "
        "is the only file you need in order to ingest; everything below is for checking "
        "what it says.",
        f"2. [`{_rel(run_dir, workspace, '02_units', 'units.jsonl')}`]"
        f"({_rel(run_dir, workspace, '02_units', 'units.jsonl')}) — the evidence. Each "
        "unit carries verbatim excerpts with character offsets into `normalized.txt`, "
        "and `asset_ref` where the evidence is a table cell or a formula. Follow "
        "`payload.source_unit_ids` from an entry to get here.",
        "3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. "
        "**Check `fidelity` before you trust a comparison:** `exact` came from the "
        "source's own markup and can be compared as a string; `transcribed` was read "
        "off an image and must not be.",
        "4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset "
        "citation resolves against, by character offset.",
        f"5. [`{_rel(run_dir, workspace, '00_original_sources')}/`]"
        f"({_rel(run_dir, workspace, '00_original_sources')}) — the raw source, "
        "unmodified. Go here when you need to check the pipeline itself.",
        "",
        "Everything else records how the output was arrived at: the routing, the "
        "judgments, the candidates before audit, and the audit findings.",
        "",
        "## What is in each folder", "",
        "| folder | contents |",
        "|---|---|",
    ]
    for name, desc in FOLDERS:
        if (run_dir / name).exists():
            out.append(f"| [`{name}`]({_rel(run_dir, workspace, name)}) | {desc} |")
    out += [""]

    if coverage:
        verdict = coverage.get("verdict", "?")
        out += [
            "## Does the output represent the corpus?", "",
            f"The run's own corpus-coverage audit returned **`{verdict}`**"
            + (f", with {len(coverage.get('missing', []))} gap(s) named."
               if coverage.get("missing") else "."),
            "",
        ]
        for m in coverage.get("missing", []):
            out += [f"- **{m.get('what_is_lost', '')}** {m.get('consequence', '')}", ""]
        for note in coverage.get("notes", [])[:4]:
            out += [f"> {note}", ""]
        out += [f"Full judgment: [`06_audit/corpus_coverage.json`]"
                f"({_rel(run_dir, workspace, '06_audit', 'corpus_coverage.json')}).", ""]

    if omissions or audits:
        kept = sum(1 for a in audits if a["verdict"] in ("pass", "pass_with_label"))
        out += [
            "## What the checks found", "",
            f"- The completeness check reported **{len(omissions)} finding(s)** against "
            f"the first extraction: [`02_units/omissions.jsonl`]"
            f"({_rel(run_dir, workspace, '02_units', 'omissions.jsonl')}).",
            f"- The adversarial audit reviewed **{len(audits)} candidate(s)** and passed "
            f"{kept} without requiring a correction: [`06_audit/audits.jsonl`]"
            f"({_rel(run_dir, workspace, '06_audit', 'audits.jsonl')}).",
            "",
        ]

    out += _assets_section(run_dir, workspace, units)

    out += ["## The knowledge handed off", "",
            f"Rendered from [`07_enqueue/enqueue.jsonl`]"
            f"({_rel(run_dir, workspace, '07_enqueue', 'enqueue.jsonl')}) — "
            f"{len(events)} event(s), target `{events[0]['target_engine']}`.", ""]

    for i, e in enumerate(events, 1):
        p = e["payload"]
        out += [
            "---", "",
            f"### {i}. {p['title']}", "",
            f"`{e['operation']}` · knowledge state **{p['knowledge_state']}** "
            f"· status `{e['status']}` · candidate `{e['candidate_id']}` "
            f"v{e['candidate_version']}", "",
            f"**Slug** `{p['slug']}`", "",
            p["summary"], "",
            f"**Assertions ({len(p['assertions'])})**", "",
        ]
        for n, a in enumerate(p["assertions"], 1):
            backing = ", ".join(f"`{x}`" for x in a.get("assessment_ids", [])) or "—"
            out += [f"{n}. {a['text']}", "", f"   *backed by* {backing}", ""]
        if p.get("related_topics"):
            out += ["**Related topics** " + ", ".join(f"`{t}`" for t in p["related_topics"]), ""]
        if p.get("labels"):
            out += ["**Labels**", ""] + [f"- {x}" for x in p["labels"]] + [""]
        out += [
            f"**Source units ({len(p['source_unit_ids'])})** "
            + ", ".join(f"`{u}`" for u in p["source_unit_ids"]), "",
            f"**Traceability** — idempotency key `{e['idempotency_key']}` · queue event "
            f"`{e['queue_event_id']}` · audits "
            + (", ".join(f"`{a}`" for a in e.get("audit_ids", [])) or "—"), "",
            "<details><summary>Provenance chain</summary>", "",
        ]
        out += [f"- `{k}` → `{v}`" for k, v in sorted(e["provenance_chain"].items())]
        out += ["", "</details>", ""]

    return "\n".join(out)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
    for arg in sys.argv[1:]:
        path = Path(arg)
        (path / "README.md").write_text(render(path))
        legacy = path / "enqueue.md"
        if legacy.exists():
            legacy.unlink()
        print("wrote", path / "README.md")
