"""Non-textual source content, kept as addressable assets instead of flattened.

Pass 0 used to emit exactly one representation of a source: `normalized.txt`.
Everything downstream cites a character span in it, and that is the whole basis
of the pipeline's guarantee -- a quote is checked against the source byte for
byte. It works for prose and it destroys everything else.

Measured on the five documents in `demo/real-runs/`: a 1985 t-statistic reached
the corpus as the literal string `Tt = ARw,t/(st/ViN)`, and a table row reached
it as `Total segment revenue$33,314 $26,881 $23,855` with its column headers
fused into `SEGMENT REVENUE AND PROFIT202520242023` on a different line.

The table case is the dangerous one, and it is worth being precise about why.
The year-to-column mapping survives only in the *model's* prose reconstruction
of the row. The stored evidence is the flat string, so a model that read the
columns backwards produces a unit whose citation still verifies `True`. Verbatim
verification confirms the digits were copied. It cannot confirm they were
assigned to the right year, and nothing else was checking.

So a source becomes a bundle: the text, plus a typed asset per non-textual
object. A table asset carries its grid, so a cell is addressable as
(row, column) with its headers attached, and a citation to it is checkable in a
way that a citation to a fused string is not.

FIDELITY IS PART OF THE RECORD. The three kinds of asset are not equally
trustworthy and must not be stored as though they were:

  - `exact`       Structure recovered losslessly from markup the source already
                  carried -- an HTML `<table>`, an XBRL fact. Nothing inferred.
                  A citation to this is as good as a quote.
  - `transcribed` A model or OCR read the source and produced a representation
                  of it -- a formula rendered to LaTeX. The content is a
                  READING, not a quote, and the field's own evidence says string
                  comparison is the wrong check: UniMERNet scores 0.48 exact
                  match against 0.81 when rendered and compared visually, so
                  about a third of correct transcriptions differ textually from
                  the reference (Wang et al., CVPR 2025).
  - `inferred`    A model described something it could not transcribe -- what a
                  chart shows. This is not evidence and must never be cited as
                  though it were.

`research/2026-08-13-non-textual-content-research.md` records the evidence
behind those three classes and the systems each follows.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Iterable

#: Structure recovered from markup, no inference. Citable as a quote is.
FIDELITY_EXACT = "exact"
#: A model or OCR read it. A reading, not a quote.
FIDELITY_TRANSCRIBED = "transcribed"
#: A model described what it could not transcribe. Never evidence.
FIDELITY_INFERRED = "inferred"

FIDELITIES = (FIDELITY_EXACT, FIDELITY_TRANSCRIBED, FIDELITY_INFERRED)

ASSET_TABLE = "table"
ASSET_FORMULA = "formula"
ASSET_FIGURE = "figure"


@dataclass
class Cell:
    """One table cell, with the span information a header lookup needs."""

    row: int
    col: int
    text: str
    row_span: int = 1
    col_span: int = 1
    is_header: bool = False

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"row": self.row, "col": self.col, "text": self.text}
        if self.row_span != 1:
            out["row_span"] = self.row_span
        if self.col_span != 1:
            out["col_span"] = self.col_span
        if self.is_header:
            out["is_header"] = True
        return out


@dataclass
class Table:
    """A grid, kept as a grid.

    `column_headers` and `row_headers` are resolved once here rather than left
    for each consumer to re-derive, because re-deriving them is exactly the step
    that goes wrong: the published metrics for table structure are close to
    blind to header association specifically (TEDS correlates r~0.68 with human
    judgment of whether a cell maps to its headers, against 0.93 for an LLM
    judge -- arXiv 2603.18652). If the association is computed once and stored,
    a consumer cannot get it wrong a second way.
    """

    cells: list[Cell] = field(default_factory=list)
    n_rows: int = 0
    n_cols: int = 0
    caption: str = ""
    #: The nearest section heading above the table. A caption says what the
    #: object is; a heading says where in the document it sits, and a table
    #: titled "2025" is uninterpretable without it.
    heading: str = ""

    def cell_at(self, row: int, col: int) -> Cell | None:
        for cell in self.cells:
            if (cell.row <= row < cell.row + cell.row_span
                    and cell.col <= col < cell.col + cell.col_span):
                return cell
        return None

    def _is_title_row(self, row: int) -> bool:
        """A row carrying the table's title and nothing else.

        Filings typeset the title inside the grid, so the header row is not row
        zero and a walk that stops at the first non-header cell finds no headers
        at all. Measured on the GE 10-K: the cash-flow statement's year columns
        were unreachable for exactly this reason, which defeats the one thing a
        stored grid is for -- knowing which year a figure belongs to.
        """
        populated = [c for c in self.cells if c.row == row and c.text.strip()]
        return len(populated) == 1 and self.n_cols > 1

    def column_headers(self, col: int) -> list[str]:
        """Header labels governing a column, outermost first."""
        out: list[str] = []
        for row in range(self.n_rows):
            cell = self.cell_at(row, col)
            if cell is not None and cell.is_header:
                if cell.text and cell.text not in out:
                    out.append(cell.text)
                continue
            # Step over a title row rather than stopping at it; stop at the
            # first row of actual data.
            if not out and self._is_title_row(row):
                continue
            break
        return out

    def row_headers(self, row: int) -> list[str]:
        """Label(s) identifying a row: its leading header or first-column cell.

        Financial tables rarely mark a stub column with `<th>`, so the leading
        cell is accepted as the row label when no header cell is present. That
        is a convention, not a fact about the source, and it is why a row header
        is reported alongside the coordinates rather than instead of them.
        """
        out: list[str] = []
        for col in range(self.n_cols):
            cell = self.cell_at(row, col)
            if cell is None:
                continue
            if cell.is_header or col == 0:
                if cell.text and cell.text not in out:
                    out.append(cell.text)
                if not cell.is_header:
                    break
            else:
                break
        return out

    def as_dict(self) -> dict[str, Any]:
        return {
            "n_rows": self.n_rows,
            "n_cols": self.n_cols,
            "caption": self.caption,
            "heading": self.heading,
            "cells": [c.as_dict() for c in self.cells],
        }

    def to_text(self) -> str:
        """A readable rendering, for the flat text and for prompts.

        Pipe-separated rather than fused. This is what `normalized.txt` gets, so
        even a consumer that ignores assets entirely stops seeing
        `Total segment revenue$33,314 $26,881 $23,855`.
        """
        lines: list[str] = []
        if self.caption:
            lines.append(self.caption)
        for row in range(self.n_rows):
            seen: set[int] = set()
            values: list[str] = []
            for col in range(self.n_cols):
                cell = self.cell_at(row, col)
                if cell is None or id(cell) in seen:
                    values.append("")
                    continue
                seen.add(id(cell))
                values.append(cell.text)
            if any(v for v in values):
                lines.append(" | ".join(values))
        return "\n".join(lines)


def make_asset_id(kind: str, source_id: str, index: int) -> str:
    prefix = {ASSET_TABLE: "tbl", ASSET_FORMULA: "fml", ASSET_FIGURE: "fig"}[kind]
    return f"{prefix}-{source_id}-{index:04d}"


def build_asset(
    *,
    kind: str,
    source_id: str,
    index: int,
    fidelity: str,
    extractor: str,
    payload: dict[str, Any],
    text: str = "",
    page: int | None = None,
    bbox: list[float] | None = None,
    char_start: int | None = None,
    char_end: int | None = None,
) -> dict[str, Any]:
    """One asset record.

    `extractor` names what produced it, because the three fidelity classes are
    only meaningful if a consumer can tell which tool made the claim -- an HTML
    table parser and a vision model both emit tables and they are not the same
    evidence.
    """
    if fidelity not in FIDELITIES:
        raise ValueError(f"unknown fidelity {fidelity!r}; expected one of {FIDELITIES}")
    record = {
        "asset_id": make_asset_id(kind, source_id, index),
        "source_id": source_id,
        "kind": kind,
        "fidelity": fidelity,
        "extractor": extractor,
        "text": text,
        "payload": payload,
    }
    if page is not None:
        record["page"] = page
    if bbox is not None:
        record["bbox"] = bbox
    if char_start is not None:
        record["char_start"] = char_start
        record["char_end"] = char_end
    record["content_sha256"] = hashlib.sha256(
        json.dumps({k: v for k, v in record.items() if k != "content_sha256"},
                   sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    return record


def resolve_cell(asset: dict[str, Any], row: int, col: int) -> dict[str, Any] | None:
    """The value at (row, col) with the headers that govern it.

    This is what makes an asset citation checkable. A consumer asking for
    row 3, column 2 of a table gets the value AND the labels it sits under, so
    a claim that "2025 total segment revenue was $33,314" can be tested against
    the source rather than against a model's memory of the column order.
    """
    if asset.get("kind") != ASSET_TABLE:
        return None
    table = from_payload(asset["payload"])
    cell = table.cell_at(row, col)
    if cell is None:
        return None
    return {
        "value": cell.text,
        "row": row,
        "col": col,
        "column_headers": table.column_headers(col),
        "row_headers": table.row_headers(row),
    }


def from_payload(payload: dict[str, Any]) -> Table:
    cells = [
        Cell(row=c["row"], col=c["col"], text=c.get("text", ""),
             row_span=c.get("row_span", 1), col_span=c.get("col_span", 1),
             is_header=c.get("is_header", False))
        for c in payload.get("cells", [])
    ]
    return Table(cells=cells, n_rows=payload.get("n_rows", 0),
                 n_cols=payload.get("n_cols", 0), caption=payload.get("caption", ""),
                 heading=payload.get("heading", ""))


def asset_for(run_dir, normalized_rel: str, asset_id: str,
              cache: dict[str, dict[str, dict]]) -> dict[str, Any] | None:
    """The named asset from one source's bundle, or None.

    Lives here rather than in either checker because BOTH the audit and the
    validator have to resolve an asset citation the same way. They did not, for
    one run: the validator learned about asset-backed excerpts and the audit did
    not, so a formula citation passed one gate and was rejected by the other as
    a fabrication. Two copies of a rule is one copy that will be updated.

    Assets sit beside `normalized.txt` rather than in a central file, so a
    citation resolves within its own source and an id cannot accidentally match
    one belonging to a different document.
    """
    from pathlib import Path

    from .artifacts import read_jsonl

    if normalized_rel not in cache:
        assets_path = Path(run_dir) / normalized_rel
        assets_path = assets_path.parent / "assets.jsonl"
        rows = read_jsonl(assets_path) if assets_path.exists() else []
        cache[normalized_rel] = {a["asset_id"]: a for a in rows if a.get("asset_id")}
    return cache[normalized_rel].get(asset_id)


def write_assets(path, assets: Iterable[dict[str, Any]]) -> None:
    from .artifacts import write_jsonl_atomic

    write_jsonl_atomic(path, list(assets))
