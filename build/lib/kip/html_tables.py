"""Recover tables from HTML as grids, rather than flattening them to a line.

Pass 0's HTML path stripped tags with a regex that inserted a newline after
`</p|div|li|tr|h1-6>` and nothing after `</td>`. Cells inside a row therefore
concatenated with no separator at all, which is how a header row in the GE
10-K reached the corpus as `SEGMENT REVENUE AND PROFIT202520242023` and its
data row as `Total segment revenue$33,314 $26,881 $23,855`.

Adding `td` to that regex fixes the fusing and not the loss: a separator gives
a consumer three values in a row and still no way to know which year each
belongs to. The mapping is what a citation needs, so the table has to survive
as a grid.

No new dependency. `html.parser` is in the standard library and an HTML table
is a well-specified structure -- this is not a layout-analysis problem, the
markup already says what the cells are. That distinction matters: recovering a
grid from markup is `exact` fidelity, while recovering one from a PDF's
geometry is a model's reading of a picture, and the pipeline records them
differently.

Rowspan and colspan are resolved into an occupancy grid so a cell's true
coordinates are its coordinates, not its position in the source order.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from typing import Any

from .assets import Cell, Table

_CELL_TAGS = {"td", "th"}
_SKIP_TAGS = {"script", "style"}
_WS = re.compile(r"[\s ]+")


def _clean(text: str) -> str:
    return _WS.sub(" ", text).strip()


class _TableCollector(HTMLParser):
    """Collect every table in a document, innermost-first order preserved.

    Nested tables are common in filings -- a layout table wrapping a data
    table -- so a stack is kept rather than assuming one table at a time. Each
    table is emitted independently; the caller decides which are worth keeping.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[Table] = []
        self._stack: list[dict[str, Any]] = []
        self._skip = 0
        # The nearest heading seen so far, stamped onto each table as it opens.
        # A financial statement titled only "2025" is uninterpretable without
        # the section it sits under.
        self._heading = ""
        self._in_heading = False
        self._heading_buf: list[str] = []

    # --- structure ---------------------------------------------------------
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip += 1
            return
        if self._skip:
            return
        attributes = {k.lower(): (v or "") for k, v in attrs}
        if tag in _HEADING_TAGS:
            self._in_heading = True
            self._heading_buf = []
            return
        if tag == "table":
            self._stack.append({"rows": [], "current": None, "caption": [],
                                "heading": self._heading})
            return
        if not self._stack:
            return
        top = self._stack[-1]
        if tag == "tr":
            top["current"] = []
            top["rows"].append(top["current"])
        elif tag in _CELL_TAGS:
            if top["current"] is None:
                top["current"] = []
                top["rows"].append(top["current"])
            top["current"].append({
                "text": [],
                "is_header": tag == "th",
                "row_span": _span(attributes.get("rowspan")),
                "col_span": _span(attributes.get("colspan")),
            })
        elif tag == "caption":
            top["in_caption"] = True

    def handle_endtag(self, tag: str) -> None:
        if tag in _HEADING_TAGS and self._in_heading:
            self._in_heading = False
            text = _clean("".join(self._heading_buf))
            if text:
                self._heading = text
            return
        if tag in _SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
            return
        if self._skip or not self._stack:
            return
        top = self._stack[-1]
        if tag == "caption":
            top.pop("in_caption", None)
        elif tag == "table":
            self.tables.append(_to_table(self._stack.pop()))

    def handle_data(self, data: str) -> None:
        if self._in_heading:
            self._heading_buf.append(data)
            return
        if self._skip or not self._stack:
            return
        top = self._stack[-1]
        if top.get("in_caption"):
            top["caption"].append(data)
            return
        row = top.get("current")
        if row:
            row[-1]["text"].append(data)


def _span(value: str | None) -> int:
    try:
        n = int((value or "1").strip())
    except (TypeError, ValueError):
        return 1
    # A span of 0 means "to the end of the section" in HTML, and a huge span is
    # almost always a typo in generated markup. Either way, refusing to honour
    # it keeps the grid finite.
    return n if 1 <= n <= 1000 else 1


def _to_table(raw: dict[str, Any]) -> Table:
    """Lay cells onto a grid, honouring spans.

    `occupied` tracks which (row, col) positions are already taken by an
    earlier cell's span, so the next cell lands where it actually belongs.
    """
    occupied: set[tuple[int, int]] = set()
    cells: list[Cell] = []
    max_col = 0
    for row_index, row in enumerate(raw["rows"]):
        col = 0
        for spec in row:
            while (row_index, col) in occupied:
                col += 1
            text = _clean("".join(spec["text"]))
            cell = Cell(row=row_index, col=col, text=text,
                        row_span=spec["row_span"], col_span=spec["col_span"],
                        is_header=spec["is_header"])
            cells.append(cell)
            for r in range(row_index, row_index + cell.row_span):
                for c in range(col, col + cell.col_span):
                    occupied.add((r, c))
            col += cell.col_span
            max_col = max(max_col, col)
    table = Table(cells=cells, n_rows=len(raw["rows"]), n_cols=max_col,
                  caption=_clean("".join(raw["caption"])),
                  heading=raw.get("heading", ""))
    _promote_header_row(table)
    _promote_title_row(table)
    return table


#: Tags whose text is a section heading.
_HEADING_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


def _promote_title_row(table: Table) -> None:
    """A table whose title is its own first row gets that title as a caption.

    Every financial statement in the GE filing takes this shape: row 0 holds
    `STATEMENT OF CASH FLOWS` in one cell and nothing in the rest, because the
    title is typeset inside the table rather than in a `<caption>` element. Left
    alone, those tables reach the record captionless and a reader looking at a
    grid of figures cannot tell which statement it is.

    The row is promoted, NOT removed. Deleting it would shift every row index
    below it, and a row index is what a citation resolves against -- a stored
    citation to row 7 must still mean row 7 after this runs.
    """
    if table.caption or table.n_rows < 2 or table.n_cols < 2:
        return
    first = [c for c in table.cells if c.row == 0 and c.text.strip()]
    if len(first) != 1:
        return
    title = first[0].text.strip()
    # A title is words. A lone figure in the first row is data, not a heading.
    if not title or not any(ch.isalpha() for ch in title):
        return
    if sum(ch.isdigit() for ch in title) > len(title) / 3:
        return
    table.caption = title


def _promote_header_row(table: Table) -> None:
    """Treat a first row of bare `<td>` as headers when it reads like one.

    Financial filings very often mark no cells as `<th>` at all -- the GE 10-K
    marks none in its segment tables -- so a strict reading leaves every table
    headerless and every column unlabelled, which is the defect this module
    exists to fix. The test is deliberately narrow: only the first row, only
    when it is entirely non-numeric and the row beneath it is not. That
    combination is a header in a financial table and is rarely anything else.

    This is a convention applied to the source, not a fact read from it. It is
    the one inference in an otherwise `exact` extraction, and it is confined to
    a flag: the cell text is untouched either way.
    """
    if table.n_rows < 2 or any(c.is_header for c in table.cells):
        return
    # Step over a title row. A filing typesets the statement's name inside the
    # grid, so the header row is row 1 and a test that only ever looks at row 0
    # finds a title, decides it is not a header, and leaves every column of the
    # cash-flow statement unlabelled -- which is precisely the failure a stored
    # grid exists to prevent.
    top = 0
    while top + 2 < table.n_rows:
        populated = [c for c in table.cells if c.row == top and c.text.strip()]
        if len(populated) == 1 and table.n_cols > 1:
            top += 1
            continue
        break
    first = [c for c in table.cells if c.row == top and c.text]
    second = [c for c in table.cells if c.row == top + 1 and c.text]
    if not first or not second:
        return
    # A year is numeric and is still a header. That is not an edge case in
    # financial tables, it is the normal case -- `2025 2024 2023` is what the
    # column labels ARE -- so a plain numeric test rejects exactly the tables
    # this matters most for. A period label is allowed through; a money figure
    # is not.
    if any(_numeric(c.text) and not _period_label(c.text) for c in first):
        return
    if not any(_numeric(c.text) and not _period_label(c.text) for c in second):
        return
    for cell in first:
        cell.is_header = True


_NUMERICISH = re.compile(r"^[\s$€£(]*-?[\d,.]+\s*[)%]?\s*$")
#: A bare four-digit year, or a short period label. Deliberately narrow: it must
#: not admit a money figure, which is why there is no comma, decimal or symbol.
_PERIOD = re.compile(r"^(19|20)\d{2}$")


def _period_label(text: str) -> bool:
    return bool(_PERIOD.match(text.strip()))


def _numeric(text: str) -> bool:
    return bool(_NUMERICISH.match(text)) and any(ch.isdigit() for ch in text)


def extract_tables(html_text: str, *, min_cells: int = 4) -> list[Table]:
    """Every table worth keeping, in document order.

    `min_cells` drops the layout tables that carry one cell of chrome. A real
    data table has at least a couple of rows and columns; a spacer does not.
    """
    parser = _TableCollector()
    try:
        parser.feed(html_text)
        parser.close()
    except Exception:  # malformed markup is common and is not fatal
        pass
    out: list[Table] = []
    for table in parser.tables:
        populated = [c for c in table.cells if c.text]
        if len(populated) < min_cells or table.n_rows < 2 or table.n_cols < 2:
            continue
        out.append(table)
    return out

_CURRENCY_ONLY = re.compile(r"^[$€£¥]+$")
_SUFFIX_ONLY = re.compile(r"^[%)]+$")


def compact(table: Table) -> Table:
    """Drop layout padding so a cell's coordinates are meaningful.

    An iXBRL filing lays six numbers out across thirty-four columns: empty
    spacers between every value, the currency symbol in a column of its own,
    and the percent sign in another. Addressing a cell by (row, column) is only
    useful if the columns are the ones a reader would count.

    Symbol columns are folded in the direction they actually belong -- a
    currency symbol prefixes the value to its right, a percent or closing
    parenthesis suffixes the value to its left. Getting that backwards silently
    relabels every figure in the table, so the two cases are handled
    separately rather than by one rule.

    Content is not otherwise altered, and the merge only ever reattaches a
    symbol that was already adjacent in the source.
    """
    # Recorded at the cell's ORIGIN only. `cell_at` answers for every position a
    # span covers, so reading the grid position by position would record one
    # spanning header three times and compaction would keep all three.
    text_at: dict[tuple[int, int], str] = {}
    header_at: dict[tuple[int, int], bool] = {}
    span_at: dict[tuple[int, int], tuple[int, int]] = {}
    for cell in table.cells:
        if cell.text:
            text_at[(cell.row, cell.col)] = cell.text
            header_at[(cell.row, cell.col)] = cell.is_header
            span_at[(cell.row, cell.col)] = (cell.row_span, cell.col_span)

    def column(c: int) -> list[str]:
        return [text_at[(r, c)] for r in range(table.n_rows) if (r, c) in text_at]

    # Fold symbol cells into their neighbour, ROW BY ROW.
    #
    # Column-wise folding cannot work here: filing tables are ragged, so a row
    # carrying a currency symbol puts its value one column further right than a
    # row without one, and the same column holds symbols in some rows and values
    # in others. Folding within the row is the only reading that survives that.
    #
    # Direction matters and the two cases are opposite: a currency symbol
    # prefixes the value to its right, a percent or closing parenthesis suffixes
    # the value to its left. Reversing either silently relabels every figure.
    absorbed: set[tuple[int, int]] = set()
    for r in range(table.n_rows):
        cols = sorted(c for (rr, c) in text_at if rr == r)
        for i, c in enumerate(cols):
            value = text_at[(r, c)]
            if _CURRENCY_ONLY.match(value):
                for nxt in cols[i + 1:]:
                    if (r, nxt) not in absorbed:
                        text_at[(r, nxt)] = f"{value}{text_at[(r, nxt)]}"
                        absorbed.add((r, c))
                        break
            elif _SUFFIX_ONLY.match(value):
                for prev in reversed(cols[:i]):
                    if (r, prev) not in absorbed:
                        text_at[(r, prev)] = f"{text_at[(r, prev)]}{value}"
                        absorbed.add((r, c))
                        break
    for key in absorbed:
        text_at.pop(key, None)

    # Align the columns.
    #
    # After folding, a row that carried a currency symbol still holds its value
    # one position right of a row that did not, because the source laid them out
    # that way. Column coordinates are useless while that is true -- 2025 would
    # be column 1 in one row and column 2 in the next.
    #
    # The rule is deliberately conservative: densify only when the populated
    # rows agree on a shape. Rows holding the modal number of cells are laid out
    # left to right; a row holding exactly one cell is a section label and keeps
    # column 0. Anything else means the table is genuinely ragged and no
    # alignment can be inferred, so the columns are left as the source had them
    # and no false precision is introduced.
    per_row = {r: sorted(c for (rr, c) in text_at if rr == r) for r in range(table.n_rows)}
    widths = [len(cols) for cols in per_row.values() if len(cols) > 1]
    if widths:
        modal = max(set(widths), key=widths.count)
        if all(len(cols) in (0, 1, modal) for cols in per_row.values()):
            aligned: dict[tuple[int, int], str] = {}
            aligned_header: dict[tuple[int, int], bool] = {}
            for r, cols in per_row.items():
                for i, c in enumerate(cols):
                    key = (r, i if len(cols) == modal else 0)
                    aligned[key] = text_at[(r, c)]
                    aligned_header[key] = header_at.get((r, c), False)
            text_at, header_at = aligned, aligned_header

    keep_cols = [c for c in range(table.n_cols)
                 if any((r, c) in text_at for r in range(table.n_rows))]
    keep_rows = [r for r in range(table.n_rows)
                 if any((r, c) in text_at for c in keep_cols)]
    col_index = {c: i for i, c in enumerate(keep_cols)}
    row_index = {r: i for i, r in enumerate(keep_rows)}

    cells = [Cell(row=row_index[r], col=col_index[c], text=text_at[(r, c)],
                  is_header=header_at.get((r, c), False))
             for r in keep_rows for c in keep_cols if (r, c) in text_at]
    # Spans are dropped deliberately: after padding is removed a spanning
    # header no longer covers the columns it did in the source layout, and a
    # stale span would make `cell_at` answer for cells that are not there.
    out = Table(cells=cells, n_rows=len(keep_rows), n_cols=len(keep_cols),
                caption=table.caption)
    _promote_header_row(out)
    return out
