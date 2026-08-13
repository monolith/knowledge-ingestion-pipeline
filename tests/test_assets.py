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


# --- Formulas: a reading of a picture, not a quote -----------------------------


def test_math_damage_is_detected_from_what_the_text_extractor_left_behind():
    """The signal is the damage, not the mathematics.

    A PDF stores an equation as positioned glyphs, so a text extractor returns
    something that looks like text and is not: the De Bondt & Thaler t-statistic
    reached this pipeline as `Tt = ARw,t/(st/ViN)`, in which `Vi` is a square
    root. Those marks are what identify a page worth rendering.
    """
    from kip.pdf_assets import pages_with_math

    damaged = "\n".join([
        "[[PAGE 7]]",
        "means equals 2S2/N and the t-statistic is therefore",
        "Tt = [ACARL, t- ACARw,J]/ 2St/N.",
        "Tt = ARw,t/(st/ViN).",
    ])
    assert pages_with_math(damaged) == [7]


def test_ordinary_prose_is_not_mistaken_for_mathematics():
    from kip.pdf_assets import pages_with_math

    prose = "\n".join([
        "[[PAGE 1]]",
        "The little mermaid swam to the surface and saw the ship.",
        "Revenue increased 18% compared with the prior year.",
    ])
    assert pages_with_math(prose) == []


def test_a_formula_is_transcribed_and_never_exact():
    """Fidelity is the whole point.

    A transcription is a reading of a picture. The field's own evidence says
    string comparison is the wrong check for one -- UniMERNet scores 0.48
    exact-match against 0.81 rendered-and-compared -- so the asset carries the
    crop it was read from and is never marked `exact`.
    """
    from kip.assets import FIDELITY_EXACT, FIDELITY_TRANSCRIBED
    from kip.pdf_assets import formula_asset

    asset = formula_asset(source_id="dt", index=1, page=7,
                          image_rel="assets/page-0007.png",
                          latex=r"T_t = AR_{W,t} / (s_t/\sqrt{N})")
    assert asset["fidelity"] == FIDELITY_TRANSCRIBED
    assert asset["fidelity"] != FIDELITY_EXACT
    assert asset["payload"]["image"], "a transcription must carry what it was read from"
    assert asset["payload"]["transcribed"] is True
    assert asset["page"] == 7


def test_an_unread_formula_is_recorded_rather_than_omitted():
    """Honest about not having been read, which an omitted asset is not."""
    from kip.pdf_assets import formula_asset

    asset = formula_asset(source_id="dt", index=1, page=7,
                          image_rel="assets/page-0007.png")
    assert asset["payload"]["transcribed"] is False
    assert asset["payload"]["image"]


def test_rendering_without_the_renderer_is_not_fatal(tmp_path, monkeypatch):
    """A source whose formulas cannot be rendered still has usable text."""
    import builtins

    from kip.pdf_assets import render_pages

    real_import = builtins.__import__

    def no_pypdfium(name, *args, **kwargs):
        if name == "pypdfium2":
            raise ImportError("not installed")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_pypdfium)
    assert render_pages(tmp_path / "x.pdf", [1], tmp_path) == {}


# --- Citing a cell, and what that catches --------------------------------------


def _asset_from(html: str, asset_id: str = "tbl-s-0001"):
    from kip.assets import ASSET_TABLE, FIDELITY_EXACT, build_asset

    grid = _grid(html)
    asset = build_asset(kind=ASSET_TABLE, source_id="s", index=1,
                        fidelity=FIDELITY_EXACT, extractor="html_tables_v1",
                        payload=grid.as_dict(), text=grid.to_text())
    asset["asset_id"] = asset_id
    return asset


def test_a_cited_cell_resolves_with_the_headers_that_govern_it():
    """The check the flattened row could not perform.

    `Total segment revenue$33,314 $26,881 $23,855` reads identically whichever
    order the columns are in, so quoting it proves the digits were copied and
    not that they were read from the right year.
    """
    from kip.extract import _verify_asset_ref

    assets = [_asset_from(FILING_TABLE)]
    out = _verify_asset_ref({"asset_id": "tbl-s-0001", "row": 1, "col": 1}, assets)
    assert out["asset_verified"] is True
    assert out["asset_value"] == "$8,304"
    assert out["asset_column_headers"] == ["2025"]
    assert out["asset_row_headers"] == ["Equipment"]


def test_citing_a_cell_that_does_not_exist_is_reported_not_ignored():
    from kip.extract import _verify_asset_ref

    assets = [_asset_from(FILING_TABLE)]
    out = _verify_asset_ref({"asset_id": "tbl-s-0001", "row": 99, "col": 99}, assets)
    assert out["asset_verified"] is False
    assert "no cell" in out["asset_note"]

    out = _verify_asset_ref({"asset_id": "tbl-nope-0001", "row": 0, "col": 0}, assets)
    assert out["asset_verified"] is False


def test_evidence_without_an_asset_reference_is_unaffected():
    """Text citation is untouched; the asset path is additive."""
    from kip.extract import _verify_asset_ref

    assert _verify_asset_ref(None, []) == {}


def test_the_extractor_is_shown_the_grid_and_told_to_cite_cells():
    from kip.extract import _render_assets

    rendered = _render_assets([_asset_from(FILING_TABLE)])
    assert "tbl-s-0001" in rendered
    assert "SEGMENT REVENUE AND PROFIT | 2025 | 2024" in rendered
    assert "asset_ref" in rendered
    assert _render_assets([]) == "", "no tables, no section"


# --- Formulas from markup: exact, not transcribed -------------------------------


MATHML = """
<p>The equation is
<math display="block" alttext="{\\displaystyle E = mc^{2}}">
 <semantics><mrow><mi>E</mi></mrow>
 <annotation encoding="application/x-tex">{\\displaystyle E = mc^{2}}</annotation>
 </semantics></math>
which follows.</p>
"""


def test_a_formula_carried_by_markup_is_exact_not_transcribed():
    """The opposite treatment from the PDF path, and deliberately so.

    A PDF stores an equation as glyphs, so it must be rendered and read. HTML
    with MathML usually carries the author's own TeX in the markup, and reading
    a picture of it instead would be a transcription where an exact copy was
    available -- discarding the distinction the fidelity field exists to record.
    """
    from kip.assets import FIDELITY_EXACT
    from kip.html_formulas import formula_assets

    assets = formula_assets(MATHML, "s")
    assert len(assets) == 1
    assert assets[0]["fidelity"] == FIDELITY_EXACT
    assert assets[0]["payload"]["latex"] == "E = mc^{2}"
    assert assets[0]["payload"]["display"] == "block"


def test_the_displaystyle_wrapper_is_presentation_and_is_stripped():
    """Two spellings of one formula must compare equal."""
    from kip.html_formulas import extract_formulas

    a = extract_formulas('<math alttext="{\\displaystyle x^{2}}"></math>')
    b = extract_formulas('<math alttext="x^{2}"></math>')
    assert a[0]["latex"] == b[0]["latex"] == "x^{2}"


def test_mathml_without_any_tex_is_recorded_rather_than_dropped():
    """'A formula is here and could not be read' is information."""
    from kip.assets import FIDELITY_TRANSCRIBED
    from kip.html_formulas import formula_assets

    assets = formula_assets("<math><mrow><mi>x</mi><mo>+</mo><mi>y</mi></mrow></math>", "s")
    assert len(assets) == 1
    assert assets[0]["fidelity"] == FIDELITY_TRANSCRIBED
    assert assets[0]["payload"]["latex"] == ""
    assert assets[0]["payload"]["mathml"], "the presentation markup is kept to read later"


def test_a_lone_symbol_is_not_a_formula():
    from kip.html_formulas import extract_formulas

    assert extract_formulas('<math alttext="x"></math>') == []


def test_the_mediawiki_image_fallback_still_yields_its_tex():
    """Older output renders the equation as a PNG and puts the TeX in alt."""
    from kip.html_formulas import extract_formulas

    found = extract_formulas(
        '<img class="mwe-math-fallback-image-inline" alt="a^{2}+b^{2}=c^{2}" src="x.png">')
    assert found[0]["latex"] == "a^{2}+b^{2}=c^{2}"


def test_an_image_source_is_normalized_to_a_placeholder_and_an_asset(tmp_path):
    """An image is a page that arrived on its own: no text layer, all content
    in the picture, recovered by the same visual read the PDF path uses."""
    from kip.normalize import _handler_for

    handler, normalizer = _handler_for(tmp_path / "scan.png")
    assert normalizer == "image_v1"
    text, markers = handler(tmp_path / "scan.png")
    assert "[[IMAGE scan.png]]" in text
    assert "assets.jsonl" in text


# --- Citing a formula ----------------------------------------------------------


FORMULA_ASSET = {
    "asset_id": "fml-s-0001", "source_id": "s", "kind": "formula", "fidelity": "exact",
    "text": "E=mc^{2}",
    "payload": {"latex": "E=mc^{2}", "display": "block", "mathml": ""},
}


def test_a_formula_quoted_as_latex_counts_as_a_citation():
    """It cannot be in the flat text -- normalization is what destroyed it."""
    from kip.extract import _resolve_evidence

    got = _resolve_evidence(
        {"source_id": "s", "normalized_path": "n.txt"},
        {"excerpt": "E = mc^{2}", "line_start": 3, "line_end": 3,
         "asset_ref": {"asset_id": "fml-s-0001"}},
        "the mass-energy equivalence\nE\n=\nm\nc\n2\n", ["a", "b", "c"], [FORMULA_ASSET])
    assert got["excerpt_verified"] is True
    assert got["excerpt_source"] == "asset", "and the record says where it was checked"
    assert got["asset_value"] == "E=mc^{2}"
    assert got["asset_fidelity"] == "exact", "so a reader can tell copied from read"


def test_a_different_equation_is_not_the_cited_one():
    """The loosening is about spelling, not about what the formula says."""
    from kip.extract import _resolve_evidence

    got = _resolve_evidence(
        {"source_id": "s", "normalized_path": "n.txt"},
        {"excerpt": "E = mc^{3}", "line_start": 1, "line_end": 1,
         "asset_ref": {"asset_id": "fml-s-0001"}},
        "text", ["text"], [FORMULA_ASSET])
    assert got["excerpt_verified"] is False


def test_citing_an_asset_that_does_not_exist_fails():
    from kip.extract import _resolve_evidence

    got = _resolve_evidence(
        {"source_id": "s", "normalized_path": "n.txt"},
        {"excerpt": "E=mc^{2}", "line_start": 1, "line_end": 1,
         "asset_ref": {"asset_id": "fml-s-9999"}},
        "text", ["text"], [FORMULA_ASSET])
    assert got["excerpt_verified"] is False
    assert got["asset_verified"] is False


def test_spacing_and_sizing_directives_do_not_break_a_match():
    """Two authors write one equation with different amounts of this."""
    from kip.extract import _matches_asset

    asset = {"kind": "formula", "payload": {"latex": r"\left(\frac{a}{b}\right)\,=\,c"}}
    assert _matches_asset(r"\left( \frac {a}{b} \right) = c", asset)


def test_the_loosening_stops_at_spelling():
    """Brackets are not noise: they say what the operation applies to."""
    from kip.extract import _matches_asset

    asset = {"kind": "formula", "payload": {"latex": r"\ln(S/K)+r\tau"}}
    assert not _matches_asset(r"\ln(S/K+r\tau)", asset)


def test_only_a_formula_the_document_carries_can_be_cited():
    """An excerpt matching nothing in the bundle is not evidence."""
    from kip.extract import _matches_asset

    assert not _matches_asset("x=1", {"kind": "formula", "payload": {"latex": ""}})


def test_the_extractor_is_shown_statements_not_symbol_names():
    """112 formulas of which 100 are `\\tau` buries the dozen that assert something."""
    from kip.extract import _significant_formulas

    assets = [
        {"kind": "formula", "payload": {"latex": r"\tau", "display": "inline"}},
        {"kind": "formula", "payload": {"latex": "C(S,t)", "display": "inline"}},
        {"kind": "formula", "payload": {"latex": "N(d_{+})=e^{x}", "display": "inline"}},
        {"kind": "formula", "payload": {"latex": "rV", "display": "block"}},
    ]
    shown = _significant_formulas(assets)
    assert [a["payload"]["latex"] for a in shown] == ["N(d_{+})=e^{x}", "rV"]


def test_an_image_source_asset_is_the_shape_the_visual_read_looks_for(tmp_path):
    """The wiring between the two halves, which nothing else checks.

    Pass 0 emits the asset and Pass 1 selects which assets to read. Each is
    tested; the seam between them is where an image source would silently
    produce a figure nobody ever reads.
    """
    from kip.normalize import _image_assets

    img = tmp_path / "scan.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\0" * 32)
    assets = _image_assets(img, "s", tmp_path / "assets")

    assert len(assets) == 1
    selected = [a for a in assets
                if a.get("kind") == "figure" and a.get("payload", {}).get("image")]
    assert selected == assets, "the visual read's own filter must select it"


# --- Detecting mathematics by the damage it leaves ------------------------------


def test_an_operator_ending_a_line_means_its_right_hand_side_is_gone():
    """The most valuable signal, because the loss it marks is total.

    Measured on the De Bondt scan: `CU_j = \\sum_{t=-35}^{0} u_{jt}` reaches the
    text layer as `CUj = ` and the summation is simply absent -- not garbled,
    absent. Nothing downstream can recover a definition whose right-hand side
    was never extracted, so the page has to be rendered and read.
    """
    from kip.pdf_assets import pages_with_math

    text = ("[[PAGE 1]]\n"
            "we compute the cumulative excess returns CUj = \n"
            "t_35 ujt for the prior 36 months (the portfolio formation period\n"
            "and the portfolios are ranked from low to high, so that ACARw,t < \n")
    assert pages_with_math(text) == [1]


def test_prose_is_not_flagged():
    from kip.pdf_assets import pages_with_math

    text = ("[[PAGE 1]]\n"
            "The main principle behind the model is to hedge the option by buying\n"
            "and selling the underlying asset in a specific way to eliminate risk.\n"
            "This type of hedging is called continuously revised delta hedging.\n")
    assert pages_with_math(text) == []


def test_a_capital_I_where_a_vertical_bar_belongs():
    """Conditional expectation is the densest notation in an empirical paper,
    and the bar is what a scan loses first: `E(u_jt | F_{t-1})` arrives as
    `E(li2t 1IF-)`, which no amount of better text extraction repairs."""
    from kip.pdf_assets import pages_with_math

    text = ("[[PAGE 4]]\n"
            "(Rjt -Em(Rjt I Fm 1) I Ft-,) = E(li2t 1IF-) = 0\n"
            "where Ft-1 represents the complete set of information at time t - 1\n"
            "hypothesis implies that E(twt I Ft-,) = E(i2Lt I Ft-) = 0. As explained\n")
    assert pages_with_math(text) == [4], (
        "one mark is prose noise; a page of mathematics produces many")


def test_the_pronoun_I_does_not_look_like_a_vertical_bar():
    """`I` is a common English word; the signal has to be narrower than that."""
    from kip.pdf_assets import pages_with_math

    text = ("[[PAGE 2]]\n"
            "In this paper I argue that the market overreacts, and I show that\n"
            "the effect (which I first noticed in 1980) is asymmetric.\n"
            "As I noted above (see I. Introduction), the evidence is mixed.\n")
    assert pages_with_math(text) == []


def test_both_gates_accept_an_asset_backed_citation(tmp_path):
    """The audit and the validator must resolve a citation the same way.

    They did not, for one run: the validator learned about asset-backed
    excerpts and the audit did not, so seven candidates whose units cited a
    transcribed formula were failed by the auditor as fabrications and never
    reached the queue. The excerpt was correct; only one of the two checkers
    knew where to look for it.
    """
    import json

    from kip.assets import asset_for

    src = tmp_path / "01_normalized" / "s"
    src.mkdir(parents=True)
    (src / "normalized.txt").write_text("CUj = \nt_35 ujt for the prior 36 months\n")
    asset = {"asset_id": "fml-s-0001", "kind": "formula", "fidelity": "transcribed",
             "payload": {"latex": r"CU_j = \sum_{t=-35}^{t=0} u_{jt}"}}
    (src / "assets.jsonl").write_text(json.dumps(asset) + "\n")

    cache: dict = {}
    found = asset_for(tmp_path, "01_normalized/s/normalized.txt", "fml-s-0001", cache)
    assert found is not None, "resolved relative to the source that owns it"
    assert asset_for(tmp_path, "01_normalized/s/normalized.txt", "fml-s-9999", cache) is None


# --- Captions and headings belong to the asset ---------------------------------


def test_a_table_whose_title_is_its_first_row_gets_that_title_as_a_caption():
    """The shape every GE financial statement takes: the title is typeset
    inside the table, so a strict reading of `<caption>` leaves the record
    holding a grid of figures nobody can identify."""
    from kip.html_tables import extract_tables

    html = ("<h2>Segment results</h2><table>"
            "<tr><td>STATEMENT OF CASH FLOWS</td><td></td><td></td></tr>"
            "<tr><td>Year</td><td>2025</td><td>2024</td></tr>"
            "<tr><td>Net cash</td><td>$1,200</td><td>$900</td></tr></table>")
    table = extract_tables(html)[0]
    assert table.caption == "STATEMENT OF CASH FLOWS"
    assert table.heading == "Segment results"
    assert table.n_rows == 3, "promoted, not removed -- a citation to row 2 must still mean row 2"


def test_a_first_row_of_figures_is_data_and_not_a_title():
    from kip.html_tables import extract_tables

    html = ("<table><tr><td>1,240</td><td></td><td></td></tr>"
            "<tr><td>a</td><td>b</td><td>c</td></tr>"
            "<tr><td>d</td><td>e</td><td>f</td></tr></table>")
    assert extract_tables(html)[0].caption == ""


def test_a_content_image_becomes_a_figure_and_furniture_does_not():
    """The Sharpe reprint's only image is a `home.jpg` navigation button. An
    extractor that captured it would report a figure where the document has
    none."""
    from kip.html_figures import extract_figures

    html = ('<h2>Results</h2>'
            '<figure><img src="car.png">'
            '<figcaption>Figure 1. Cumulative average residuals.</figcaption></figure>'
            '<img src="spacer.gif" alt="">'
            '<img class="logo" src="l.png" alt="Company logo mark for the corporation">'
            '<a href="home.htm"><img\n src="../../home.jpg" border="0"></a>')
    found = extract_figures(html)
    assert [f["src"] for f in found] == ["car.png"]
    assert found[0]["caption"].startswith("Figure 1.")
    assert found[0]["heading"] == "Results"


def test_a_chart_identified_only_by_its_alt_text_is_still_a_figure():
    from kip.html_figures import extract_figures

    html = '<img src="c.png" alt="Line chart of implied volatility against strike price">'
    assert len(extract_figures(html)) == 1


def test_a_mediawiki_equation_image_is_not_a_figure():
    """It is a picture of a formula the formula extractor already has exactly,
    and capturing it again would double-count the same content at a worse
    fidelity."""
    from kip.html_figures import extract_figures

    html = ('<img class="mwe-math-fallback-image-inline" src="eq.png" '
            'alt="a^{2}+b^{2}=c^{2} which is the Pythagorean theorem">')
    assert extract_figures(html) == []


def test_a_pdf_page_carrying_a_figure_caption_is_found_with_its_caption():
    """The caption is both the signal and the content: a scanned page is one
    big image, so asking whether a page contains a picture answers yes
    everywhere, and a chart without its caption is pixels nobody can use."""
    from kip.pdf_assets import pages_with_figures

    text = ("[[PAGE 8]]\nordinary prose about the results\n"
            "[[PAGE 9]]\nFigure 1. Cumulative Average Residuals for Winner and Loser\n"
            "Portfolios of 35 Stocks\n")
    assert pages_with_figures(text) == {
        9: "Figure 1. Cumulative Average Residuals for Winner and Loser"}


def test_a_title_row_does_not_hide_the_header_row_beneath_it():
    """Measured on the GE 10-K, and it defeats the whole point of a stored grid.

    A filing typesets the statement's name inside the table, so the header row
    is row 1. A header test that only ever looks at row 0 finds the title,
    decides it is not a header, and leaves every column unlabelled -- so
    `$8,698` resolves with no year attached, which is exactly the confusion the
    asset layer exists to prevent.
    """
    from kip.assets import resolve_cell
    from kip.html_tables import extract_tables

    html = ("<table>"
            "<tr><td>STATEMENT OF CASH FLOWS</td><td></td><td></td></tr>"
            "<tr><td>For the years ended December 31</td><td>2025</td><td>2024</td></tr>"
            "<tr><td>Net income (loss)</td><td>$8,698</td><td>$6,566</td></tr></table>")
    table = extract_tables(html)[0]
    asset = {"kind": "table", "payload": table.as_dict()}
    got = resolve_cell(asset, 2, 1)
    assert got["value"] == "$8,698"
    assert got["column_headers"] == ["2025"], "the year the figure belongs to"
    assert got["row_headers"][0] == "Net income (loss)"


# --- Markdown: the format nobody thinks of as a format --------------------------


MEMO = """# Assessment

## Cost

**Table 2. Pack economics at 2025 volumes**

| Chemistry | Energy density (Wh/kg) | Pack cost ($/kWh) |
|---|---|---|
| Sodium-ion | 165 | 87 |
| LFP | 280 | 95 |

The total cost of ownership is

$$
TCO = C_{pack} N_{replace} + C_{install}
$$

where N is the replacement count.
"""


def test_a_markdown_table_becomes_a_grid_not_a_flattened_row():
    """The gap this closes. A memo's comparison table used to reach the corpus
    as `| Sodium-ion | 165 | 87 |` — readable, and no grid, so a unit quoting
    that row proved the digits were copied and not that they were assigned to
    the right column. That is the failure the asset layer exists to prevent,
    sitting in the format most likely to be handed to it."""
    from kip.assets import FIDELITY_EXACT, resolve_cell
    from kip.md_assets import markdown_assets

    table = [a for a in markdown_assets(MEMO, "s") if a["kind"] == "table"][0]
    assert table["fidelity"] == FIDELITY_EXACT, "the columns are the author's, not a guess"
    got = resolve_cell(table, 1, 2)
    assert got["value"] == "87"
    assert got["column_headers"] == ["Pack cost ($/kWh)"]
    assert got["row_headers"][0] == "Sodium-ion"


def test_a_markdown_table_carries_its_caption_and_heading():
    from kip.md_assets import markdown_assets

    table = [a for a in markdown_assets(MEMO, "s") if a["kind"] == "table"][0]
    assert table["payload"]["caption"] == "Table 2. Pack economics at 2025 volumes"
    assert table["payload"]["heading"] == "Cost"


def test_display_math_is_captured_and_inline_dollars_are_not():
    """A lone `$` is a dollar sign far more often than it is mathematics, and
    this refuses to guess which — the memo above prices packs in $/kWh."""
    from kip.md_assets import extract_formulas

    found = extract_formulas(MEMO)
    assert len(found) == 1
    assert found[0]["latex"].startswith("TCO =")


def test_a_pipe_table_needs_its_delimiter_row():
    """`|` appears in prose and in code. The delimiter row is the grammar."""
    from kip.md_assets import extract_tables

    assert extract_tables("a | b\nc | d\n") == []


def test_both_runtimes_refuse_an_image_the_api_cannot_carry(tmp_path):
    """A `.tif` is an ingestable source and produces a figure asset that reads
    perfectly under handoff — the agent opens the file itself — and 400s under
    the SDK, four times, then gets swallowed. Refusing in shared code is the
    difference between the two runtimes disagreeing about a model and
    disagreeing about a document."""
    import pytest

    from kip.handoff import HandoffClient, HandoffInvalid
    from kip.llm import LLMError, _user_content

    bad = tmp_path / "chart.tif"
    bad.write_bytes(b"II*\x00")
    with pytest.raises(LLMError, match="image/tiff"):
        _user_content("read this", [str(bad)])

    client = HandoffClient(root=tmp_path / "_handoff")
    with pytest.raises(HandoffInvalid):
        client.complete_json(system="s", user="u", schema={"type": "object"},
                             model="m", images=[str(bad)])


def test_a_supported_image_passes_both(tmp_path):
    from kip.llm import _user_content

    good = tmp_path / "page.png"
    good.write_bytes(b"\x89PNG\r\n\x1a\n")
    blocks = _user_content("read this", [str(good)])
    assert blocks[0]["source"]["media_type"] == "image/png"
