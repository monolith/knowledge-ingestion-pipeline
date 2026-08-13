"""Tables and formulas out of Markdown, from the markup rather than a reading.

Markdown is the format most documents arrive in that nobody thinks of as a
format, and until this existed it was the one common input with no asset path at
all. A memo's comparison table survived into `normalized.txt` as
`| Sodium-ion | 165 | 87 | 4,000 |` -- readable, and no grid. So a unit quoting
that row proved the digits were copied and not that they were assigned to the
right column, which is the exact failure the asset layer was built to prevent,
sitting in the format most likely to be handed to it.

Both extractors here produce `exact` fidelity, and the reason is the same one
that makes HTML `exact`: the structure is in the source. A pipe table's columns
are delimited by the author, not inferred by a parser, and `$$...$$` carries the
author's own LaTeX. Nothing is read off a picture and nothing is guessed.

WHAT IS DELIBERATELY NOT DONE. Markdown has no caption element, so a table's
caption is taken from the nearest heading above it and from a bold line
immediately preceding it -- and where neither exists, the caption is empty
rather than invented from the first row. A pipe table's first row is its header
by syntax, not by convention, so unlike the HTML path there is no title-row
promotion to do: promoting it would delete a real header.
"""

from __future__ import annotations

import re
from typing import Any

from .assets import (
    ASSET_FORMULA,
    ASSET_TABLE,
    FIDELITY_EXACT,
    Cell,
    Table,
    build_asset,
)

#: The row that makes a pipe table a table: `|---|:---:|---:|`. Its presence is
#: the whole grammar, which is why detection here is exact rather than heuristic.
_DELIMITER = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)+\|?\s*$")
_HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
#: A bold or emphasised line on its own, the closest Markdown has to a caption.
_CAPTION_LINE = re.compile(r"^\s*(?:\*\*|__)(.+?)(?:\*\*|__)\s*:?\s*$")
#: Display mathematics. Inline `$x$` is deliberately excluded: a lone `$` is a
#: dollar sign far more often than it is mathematics, and this module refuses to
#: guess which.
_DISPLAY_MATH = re.compile(r"^\s*\$\$\s*$(.*?)^\s*\$\$\s*$", re.M | re.S)
_FENCED_MATH = re.compile(r"^\s*```\s*(?:math|latex)\s*$(.*?)^\s*```\s*$", re.M | re.S)


def _split_row(line: str) -> list[str]:
    """Cells of one pipe row, with escaped pipes preserved."""
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|") and not stripped.endswith("\\|"):
        stripped = stripped[:-1]
    parts = re.split(r"(?<!\\)\|", stripped)
    return [p.replace("\\|", "|").strip() for p in parts]


def _context_above(lines: list[str], index: int) -> tuple[str, str]:
    """The caption and heading governing a table starting at `index`."""
    caption = ""
    for back in range(index - 1, max(-1, index - 4), -1):
        text = lines[back].strip()
        if not text:
            continue
        found = _CAPTION_LINE.match(text)
        if found:
            caption = found.group(1).strip()
        break
    heading = ""
    for back in range(index - 1, -1, -1):
        found = _HEADING.match(lines[back])
        if found:
            heading = found.group(1).strip()
            break
    return caption, heading


def extract_tables(text: str) -> list[Table]:
    """Every pipe table in the document, in order."""
    lines = text.splitlines()
    out: list[Table] = []
    i = 0
    while i < len(lines) - 1:
        if "|" not in lines[i] or not _DELIMITER.match(lines[i + 1]):
            i += 1
            continue
        header = _split_row(lines[i])
        width = len(header)
        rows = [header]
        j = i + 2
        while j < len(lines) and "|" in lines[j] and lines[j].strip():
            rows.append(_split_row(lines[j]))
            j += 1
        caption, heading = _context_above(lines, i)
        cells: list[Cell] = []
        for r, row in enumerate(rows):
            for c, value in enumerate(row[:width]):
                cells.append(Cell(row=r, col=c, text=value, is_header=(r == 0)))
        out.append(Table(cells=cells, n_rows=len(rows), n_cols=width,
                         caption=caption, heading=heading))
        i = j
    return out


def extract_formulas(text: str) -> list[dict[str, Any]]:
    """Display mathematics: `$$...$$` blocks and ```math fences."""
    lines = text.splitlines()
    out: list[dict[str, Any]] = []
    for pattern in (_DISPLAY_MATH, _FENCED_MATH):
        for match in pattern.finditer(text):
            latex = " ".join(match.group(1).split()).strip()
            if len(latex) < 3:
                continue
            line_no = text.count("\n", 0, match.start())
            _, heading = _context_above(lines, line_no)
            before = text[max(0, match.start() - 400):match.start()].strip().splitlines()
            out.append({
                "latex": latex,
                "display": "block",
                "heading": heading,
                "surrounding_text": (before[-1].strip() if before else ""),
            })
    return out


def markdown_assets(text: str, source_id: str, start_index: int = 1) -> list[dict[str, Any]]:
    """Table and formula assets from a Markdown source, all `exact`."""
    from .html_tables import compact

    out: list[dict[str, Any]] = []
    for table in extract_tables(text):
        grid = compact(table)
        if grid.n_rows < 2 or grid.n_cols < 2:
            continue
        grid.caption = grid.caption or table.caption
        grid.heading = grid.heading or table.heading
        out.append(build_asset(
            kind=ASSET_TABLE, source_id=source_id, index=start_index + len(out),
            fidelity=FIDELITY_EXACT, extractor="markdown_tables_v1",
            payload=grid.as_dict(), text=grid.to_text(),
        ))
    for found in extract_formulas(text):
        out.append(build_asset(
            kind=ASSET_FORMULA, source_id=source_id, index=start_index + len(out),
            fidelity=FIDELITY_EXACT, extractor="markdown_math_v1",
            text=found["latex"], payload=found,
        ))
    return out
