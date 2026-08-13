"""An asset belongs to a place in the text, and survives with it."""

from kip.anchors import (
    CAPTION_LOCATED,
    CONTEXT_LOCATED,
    NONE,
    OWN_TEXT,
    PAGE_REGION,
    apply_links,
    link,
    locate,
    orphans,
    page_spans_from_locator,
    reconcile,
)

TEXT = (
    "Segment results for the year\n"                       # 0
    "STATEMENT OF CASH FLOWS | 2025 | 2024\n"              # 29
    "Net cash from operating activities | $1,200 | $900\n"
    "The company also reported a pension deficit.\n"
    "Figure 1. Cumulative average residuals for the portfolios\n"
)


def _asset(**kw):
    base = {"asset_id": "a-1", "source_id": "s", "kind": "table",
            "fidelity": "exact", "extractor": "t", "text": "", "payload": {}}
    base.update(kw)
    return base


# --- Where an asset sits --------------------------------------------------


def test_a_table_parsed_from_markup_anchors_to_its_own_text():
    """The tightest anchor there is: the object, where the normalizer put it."""
    asset = _asset(text="STATEMENT OF CASH FLOWS | 2025 | 2024\n"
                        "Net cash from operating activities | $1,200 | $900")
    anchor = locate(asset, TEXT)
    assert anchor["method"] == OWN_TEXT
    assert TEXT[anchor["char_start"]:anchor["char_end"]].startswith("STATEMENT OF CASH")


def test_a_transcription_falls_through_to_its_caption():
    """Its own text is a reading and is not in the flat file at all; the caption
    line usually survived, because a scan mangles structure before it mangles
    a sentence."""
    asset = _asset(kind="figure", fidelity="transcribed",
                   text="",
                   payload={"caption": "Figure 1. Cumulative average residuals "
                                       "for the portfolios"})
    assert locate(asset, TEXT)["method"] == CAPTION_LOCATED


def test_surrounding_prose_anchors_a_formula_the_text_layer_destroyed():
    asset = _asset(kind="formula", fidelity="transcribed",
                   payload={"latex": r"\sum x_i",
                            "surrounding_text": "The company also reported a pension "
                                                "deficit. … more"})
    assert locate(asset, TEXT)["method"] == CONTEXT_LOCATED


def test_a_page_render_falls_back_to_the_whole_page():
    """Coarse, and the record says so: every unit on that page relates to it."""
    asset = _asset(kind="figure", fidelity="transcribed", page=4, payload={})
    anchor = locate(asset, TEXT, {4: (10, 90)})
    assert anchor["method"] == PAGE_REGION
    assert (anchor["char_start"], anchor["char_end"]) == (10, 90)


def test_an_asset_that_cannot_be_placed_says_so_rather_than_guessing():
    asset = _asset(kind="figure", payload={"caption": "nowhere in this document"})
    assert locate(asset, TEXT)["method"] == NONE


def test_page_spans_are_the_union_of_a_page_s_segments():
    rows = [
        {"original_locator_start": {"page": 1}, "normalized_char_start": 0,
         "normalized_char_end": 10},
        {"original_locator_start": {"page": 1}, "normalized_char_start": 11,
         "normalized_char_end": 40},
        {"original_locator_start": {"page": 2}, "normalized_char_start": 41,
         "normalized_char_end": 60},
    ]
    assert page_spans_from_locator(rows) == {1: (0, 40), 2: (41, 60)}


# --- Is the reading corroborated? ------------------------------------------


def test_a_transcription_whose_figures_survive_the_text_layer_scores_one():
    """Digits usually survive a scan even when structure does not, so the
    wreckage can corroborate the numbers it cannot corroborate the shape of."""
    asset = _asset(text="Net cash | $1,200 | $900")
    got = reconcile(asset, "Netcash 1200 900 garbled")
    assert got["ratio"] == 1.0
    assert got["not_found"] == []


def test_a_figure_the_page_never_showed_is_named():
    asset = _asset(text="Net cash | $1,200 | $77,777")
    got = reconcile(asset, "Netcash 1200 900")
    assert got["ratio"] < 1.0
    assert "77777" in got["not_found"]


def test_formatting_is_not_counted_as_misreading():
    """`$8,698` and `8698` are the same figure; a scan that dropped the comma
    did not drop the number."""
    asset = _asset(text="$8,698 and (1,234) and 21.0%")
    assert reconcile(asset, "8698 1234 21.0")["ratio"] == 1.0


def test_a_table_of_words_reconciles_to_nothing_rather_than_to_zero():
    """No numbers is not the same as no corroboration, and reporting 0.0 would
    read as a failed check on a table that has nothing to check."""
    assert reconcile(_asset(text="Yes | No | Maybe"), "anything")["ratio"] is None


# --- Travelling with the text ----------------------------------------------


def _unit(uid, start, end, cites=None):
    evidence = {"normalized_char_start": start, "normalized_char_end": end}
    if cites:
        evidence["asset_ref"] = {"asset_id": cites}
    return {"unit_id": uid, "evidence": [evidence]}


def test_a_unit_relates_to_an_asset_it_never_quoted():
    """The whole point. A unit extracted from the paragraph a table sits in is
    related to that table, and the table survives on the strength of that text
    rather than on having been cited."""
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    links = link([_unit("u-1", 150, 160)], [asset])
    assert len(links) == 1
    assert links[0]["cited"] is False, "related, and honestly not a citation"


def test_a_citation_is_recorded_as_one():
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    links = link([_unit("u-1", 150, 160, cites="a-1")], [asset])
    assert links[0]["cited"] is True


def test_text_elsewhere_in_the_document_does_not_pull_an_asset_along():
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    assert link([_unit("u-1", 900, 950)], [asset]) == []


def test_a_citation_links_even_when_the_spans_do_not_overlap():
    """A formula citation quotes LaTeX that is not in the flat text at all, so
    its stored offsets fall back to a line range that need not sit inside the
    anchor. The citation is the stronger claim of the two and must survive."""
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    links = link([_unit("u-1", 900, 950, cites="a-1")], [asset])
    assert len(links) == 1
    assert links[0]["cited"] is True
    assert links[0]["unit_span"] is None, "honest: no overlap produced this link"


def test_a_citation_is_not_reported_as_mere_proximity():
    """Reading `cited` off whichever evidence record happened to overlap first
    reported every formula citation in the De Bondt run as an accident."""
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    unit = {"unit_id": "u-1", "evidence": [
        {"normalized_char_start": 150, "normalized_char_end": 160},
        {"normalized_char_start": 900, "normalized_char_end": 950,
         "asset_ref": {"asset_id": "a-1"}},
    ]}
    assert link([unit], [asset])[0]["cited"] is True


def test_an_unplaceable_asset_relates_to_nothing():
    asset = _asset(anchor={"char_start": None, "char_end": None, "method": NONE})
    assert link([_unit("u-1", 0, 10)], [asset]) == []


def test_the_relationship_is_written_onto_the_unit_too():
    """Both files are read independently; a link visible in only one is
    invisible to half the readers."""
    asset = _asset(anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    units = [_unit("u-1", 150, 160)]
    apply_links(units, link(units, [asset]))
    assert units[0]["related_asset_ids"] == ["a-1"]


def test_an_orphan_is_an_asset_in_text_nobody_read():
    """A different question from 'was it cited', and a sharper one: no unit was
    lost here, none was ever made."""
    placed = _asset(asset_id="a-1",
                    anchor={"char_start": 100, "char_end": 200, "method": OWN_TEXT})
    stranded = _asset(asset_id="a-2",
                      anchor={"char_start": 800, "char_end": 900, "method": OWN_TEXT})
    units = [_unit("u-1", 150, 160)]
    links = link(units, [placed, stranded])
    assert [a["asset_id"] for a in orphans([placed, stranded], links)] == ["a-2"]
