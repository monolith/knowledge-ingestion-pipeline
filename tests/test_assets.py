"""Tables recovered as grids, and the fidelity classes that go with them."""

from __future__ import annotations

import pytest

from kip.assets import (
    ASSET_TABLE,
    FIDELITY_EXACT,
    FIDELITY_INFERRED,
    FIDELITY_TRANSCRIBED,
    build_asset,
    resolve_cell,
)
from kip.html_tables import compact, extract_tables

# The shape that broke: an iXBRL filing table. No <th> anywhere, the currency
# symbol in a column of its own, spacer cells between every value, and rows of
# differing width because a row without a currency symbol has one cell fewer.
FILING_TABLE = """
<table>
 <tr><td>SEGMENT REVENUE AND PROFIT</td><td></td><td>2025</td><td></td><td>2024</td></tr>
 <tr><td>Equipment</td><td>$</td><td>8,304</td><td>$</td><td>7,106</td></tr>
 <tr><td>Services</td><td>25,010</td><td></td><td>19,775</td><td></td></tr>
 <tr><td>Segment profit margin</td><td>26.6</td><td>%</td><td>26.2</td><td>%</td></tr>
</table>
"""


def _grid(html: str):
    tables = extract_tables(html)
    assert tables, "no table recovered"
    return compact(tables[0])


def test_a_filing_table_becomes_a_grid_a_reader_would_recognize():
    grid = _grid(FILING_TABLE)
    assert (grid.n_rows, grid.n_cols) == (4, 3), grid.to_text()
    assert grid.to_text().splitlines()[0] == "SEGMENT REVENUE AND PROFIT | 2025 | 2024"


def test_every_value_resolves_to_its_own_row_and_column_headers():
    """The defect this exists to close.

    Flattened, the row was `Total segment revenue$33,314 $26,881 $23,855` and
    the year-to-column mapping survived only in the model's prose. A citation
    to the flat string verified `True` whichever way the columns were read.
    """
    asset = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                        fidelity=FIDELITY_EXACT, extractor="html_tables_v1",
                        payload=_grid(FILING_TABLE).as_dict())
    assert resolve_cell(asset, 1, 1) == {
        "value": "$8,304", "row": 1, "col": 1,
        "column_headers": ["2025"], "row_headers": ["Equipment"],
    }
    assert resolve_cell(asset, 1, 2)["column_headers"] == ["2024"]
    assert resolve_cell(asset, 3, 2)["value"] == "26.2%"


def test_a_currency_symbol_prefixes_and_a_percent_suffixes():
    """Opposite directions. Reversing either silently relabels every figure."""
    grid = _grid(FILING_TABLE)
    values = {c.text for c in grid.cells}
    assert "$8,304" in values and "8,304" not in values
    assert "26.6%" in values and "26.6" not in values


def test_a_year_is_allowed_to_be_a_header():
    """A plain numeric test rejects exactly the tables this matters most for."""
    grid = _grid(FILING_TABLE)
    assert [c.text for c in grid.cells if c.row == 0 and c.is_header] == [
        "SEGMENT REVENUE AND PROFIT", "2025", "2024",
    ]


def test_a_money_figure_is_not_allowed_to_be_a_header():
    grid = _grid("""
    <table>
      <tr><td>Equipment</td><td>$8,304</td><td>$7,106</td></tr>
      <tr><td>Services</td><td>25,010</td><td>19,775</td></tr>
    </table>
    """)
    assert not any(c.is_header for c in grid.cells), grid.to_text()


def test_rowspan_and_colspan_land_where_they_belong():
    grid = _grid("""
    <table>
      <tr><th>Region</th><th colspan="2">Revenue</th></tr>
      <tr><th>2025</th><td>10</td><td>20</td></tr>
      <tr><td rowspan="2">US</td><td>30</td><td>40</td></tr>
      <tr><td>50</td><td>60</td></tr>
    </table>
    """)
    assert grid.cell_at(0, 1).text == "Revenue"


def test_a_ragged_table_is_left_alone_rather_than_guessed_at():
    """No alignment can be inferred, so none is invented."""
    grid = _grid("""
    <table>
      <tr><td>a</td><td>1</td><td>2</td><td>3</td></tr>
      <tr><td>b</td><td>4</td></tr>
      <tr><td>c</td><td>5</td><td>6</td></tr>
    </table>
    """)
    assert grid.n_rows == 3


def test_layout_tables_are_not_assets():
    assert extract_tables("<table><tr><td>spacer</td></tr></table>") == []


def test_fidelity_is_part_of_the_record_and_is_checked():
    """Three classes that must not be stored as though they were equal."""
    for fidelity in (FIDELITY_EXACT, FIDELITY_TRANSCRIBED, FIDELITY_INFERRED):
        asset = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                            fidelity=fidelity, extractor="x", payload={})
        assert asset["fidelity"] == fidelity
    with pytest.raises(ValueError, match="unknown fidelity"):
        build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                    fidelity="verbatim", extractor="x", payload={})


def test_an_asset_is_sealed_against_edits():
    a = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                    fidelity=FIDELITY_EXACT, extractor="x",
                    payload=_grid(FILING_TABLE).as_dict())
    b = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                    fidelity=FIDELITY_EXACT, extractor="x",
                    payload=_grid(FILING_TABLE).as_dict())
    assert a["content_sha256"] == b["content_sha256"]
    c = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                    fidelity=FIDELITY_TRANSCRIBED, extractor="x",
                    payload=_grid(FILING_TABLE).as_dict())
    assert c["content_sha256"] != a["content_sha256"]
