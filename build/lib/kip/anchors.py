"""Tying an asset to the text it belongs to.

An asset used to survive into the output only if some unit happened to quote it.
That is the rule for text -- quote it or lose it -- applied to things that are
not text, and measured on the demo runs it lost a great deal: 63 of the GE
filing's tables carry four or more money figures, including the Statement of
Cash Flows, and nothing pointed at any of them.

So an asset is no longer evidence waiting to be cited. It is an object anchored
to a range of `normalized.txt`, and every unit whose own evidence overlaps that
range is RELATED to it, whether or not the unit quoted it. What follows from
that is the rule this module exists to make true: if a unit survived into the
output, the assets anchored to its text survive with it. An asset is dropped
only when the text it sits in was dropped -- a decision about the text, made on
the text's merits, which is where it belongs.

The anchor is a character span and nothing else, deliberately. A model asked
which units a table is "relevant to" gives a different answer each run and costs
a call per asset; an overlap of two integer ranges gives the same answer
forever. What the span cannot express -- a table discussed three pages from
where it is printed -- is left unexpressed rather than guessed at.

HOW PRECISE THE ANCHOR IS VARIES, AND THE RECORD SAYS SO. Locating a table's own
text in the flat file pins it to the paragraph. Falling back to the page it came
from pins it to a page, and every unit on that page then relates to it. Those
are different claims and `method` is what tells them apart.
"""

from __future__ import annotations

import re
from typing import Any

#: The asset's own text, found in the flat file. The tightest anchor: this is
#: the object itself, where the normalizer put it. Not format-specific -- an
#: HTML table's grid and a PDF figure's caption line both land here.
OWN_TEXT = "own_text"
#: The caption, found in the flat file. Nearly as tight -- a caption sits
#: immediately beside its object -- and it survives in cases the object's own
#: text does not, because a transcription is not in the flat text at all while
#: its caption line usually is.
CAPTION_LOCATED = "caption_located"
#: The surrounding prose, found in the flat file.
CONTEXT_LOCATED = "context_located"
#: The whole page the asset came from. Coarse by construction.
PAGE_REGION = "page_region"
#: Nothing could be located. The asset is an orphan by definition.
NONE = "none"


def locate_reflowed(needle: str, text: str) -> tuple[int, int] | None:
    """Find `needle` in `text` ignoring whitespace and line-break hyphenation.

    Returns the raw (start, end) offsets in `text`, or None if the characters
    are not there in order. Deliberately NOT a similarity search: every
    non-space character must match in sequence. A paraphrase, a dropped clause
    or an invented sentence still fails, which is the property the citation
    check depends on -- the point is to stop losing quotes the document really
    contains, not to start accepting quotes it does not.

    The two things forgiven are both artifacts of normalization rather than of
    the model: runs of whitespace differing from the source's hard wraps, and a
    word split across a line break as `evi- dence`.
    """

    def stream(s: str, track: bool) -> tuple[str, list[int]]:
        chars: list[str] = []
        offsets: list[int] = []
        i = 0
        while i < len(s):
            ch = s[i]
            if ch.isspace():
                i += 1
                continue
            # A hyphen immediately before a line break is a wrap artifact.
            if ch == "-":
                j = i + 1
                while j < len(s) and s[j] in " \t":
                    j += 1
                if j < len(s) and s[j] == "\n":
                    i = j + 1
                    continue
            chars.append(ch)
            if track:
                offsets.append(i)
            i += 1
        return "".join(chars), offsets

    found, _ = stream(needle, track=False)
    if not found:
        return None
    hay, offsets = stream(text, track=True)
    at = hay.find(found)
    if at < 0:
        return None
    return offsets[at], offsets[at + len(found) - 1] + 1


def _first_lines(text: str, n: int = 2) -> str:
    """The opening of a multi-line asset rendering.

    A whole table rarely locates: the normalizer wraps and the grid renderer
    does not, so the two disagree somewhere in fifty rows. The first row or two
    is both distinctive enough to pin a position and short enough to survive
    that disagreement.
    """
    lines = [line for line in text.splitlines() if line.strip()]
    return "\n".join(lines[:n])


def _row_labels(payload: dict[str, Any]) -> list[str]:
    """The most findable phrase in each row, top to bottom.

    Used to span a table rather than to point at it. Anchoring to one cell gives
    a span a few dozen characters wide, and a fifty-four-row cash-flow statement
    then relates only to a unit that happened to quote that one cell -- which is
    the citation rule again, wearing a different hat. Locating a label from the
    top of the grid and one from the bottom gives a range covering the whole
    object, which is what "the text this table sits in" means.
    """
    by_row: dict[int, str] = {}
    for cell in payload.get("cells", []):
        value = (cell.get("text") or "").strip()
        if len(value) < 12 or not any(ch.isalpha() for ch in value):
            continue
        row = cell.get("row", 0)
        if len(value) > len(by_row.get(row, "")):
            by_row[row] = value
    return [by_row[r] for r in sorted(by_row)]


def _distinctive_cell(payload: dict[str, Any]) -> str:
    """The longest label in a grid: the phrase most likely to be findable.

    A table cannot be anchored by its own rendering, and the GE filing shows why
    with no ambiguity. The normalizer puts a row holding one populated cell on a
    line of its own; the grid renderer keeps that row's empty columns as `|`
    separators. So the same table reads `STATEMENT OF COMPREHENSIVE INCOME
    (LOSS)` in the flat file and `STATEMENT OF COMPREHENSIVE INCOME (LOSS) | | |`
    in the asset, and the two disagree on exactly the characters a whitespace-
    insensitive search does not forgive. Ninety-four of a hundred tables failed
    to anchor on that difference alone.

    A cell has no separators in it, so it reads the same in both. The longest
    one is chosen because length is what makes a phrase unique in a 3MB filing:
    `2025` appears everywhere, `Less: net income attributable to noncontrolling
    interests` appears once.
    """
    best = ""
    for cell in payload.get("cells", []):
        value = (cell.get("text") or "").strip()
        if len(value) > len(best) and any(ch.isalpha() for ch in value):
            best = value
    return best


def locate(asset: dict[str, Any], text: str,
           page_spans: dict[int, tuple[int, int]] | None = None) -> dict[str, Any]:
    """Where in `text` this asset belongs.

    Tried in descending precision, and the first that lands wins. The order is
    self-selecting across formats rather than branching on them: a table parsed
    out of HTML markup has its own text in the flat file and stops at the first
    attempt, while the same table transcribed off a page image does not and
    falls through to its caption, then to its surrounding prose, then to the
    page it came from.
    """
    payload = asset.get("payload", {})

    if asset.get("kind") == "table":
        # Locate a label from each end of the grid and span between them, so the
        # anchor covers the table rather than pointing at one cell of it.
        ordered = _row_labels(payload)
        probes = ordered[:2] + ordered[-2:] if len(ordered) > 2 else ordered
        hits = [h for h in (locate_reflowed(probe, text) for probe in probes) if h]
        if hits:
            # A label like "Total revenues" occurs in a dozen tables of a
            # filing, so a probe taken from the bottom of this grid can match
            # text belonging to another one three hundred thousand characters
            # away. The table's own rendered length bounds how far its region
            # can plausibly reach; hits outside that are matches on some other
            # table and are dropped.
            own_len = len(asset.get("text", ""))
            reach = 3 * own_len + 1000
            seat = min(h[0] for h in hits)
            near = [h for h in hits if h[0] - seat <= reach]
            end = max(h[1] for h in near)
            # The located labels cluster; the table between and around them does
            # not. A grid rendering five hundred characters wide occupies about
            # that much of the flat file, so the span is extended to its own
            # footprint rather than left covering only the phrases that matched.
            # Erring wide is the recoverable direction: a slightly generous
            # anchor relates one extra neighbouring unit, a short one drops the
            # table from the paragraph it belongs to.
            return {"char_start": seat,
                    "char_end": min(len(text), max(end, seat + own_len)),
                    "method": OWN_TEXT}

    own = asset.get("text", "") or payload.get("latex", "")
    if own.strip():
        found = locate_reflowed(_first_lines(own), text)
        if found:
            return {"char_start": found[0], "char_end": found[1], "method": OWN_TEXT}

    for field, method in (("caption", CAPTION_LOCATED),
                          ("heading", CAPTION_LOCATED),
                          ("surrounding_text", CONTEXT_LOCATED)):
        value = (payload.get(field) or "").strip()
        # The surrounding-text field is stored as `before … after`; only the
        # part before the object is a contiguous run of the document.
        value = value.split(" … ")[0].strip()
        if len(value) >= 12:
            found = locate_reflowed(value, text)
            if found:
                return {"char_start": found[0], "char_end": found[1], "method": method}

    page = asset.get("page")
    if page is not None and page_spans and page in page_spans:
        start, end = page_spans[page]
        return {"char_start": start, "char_end": end, "method": PAGE_REGION}

    return {"char_start": None, "char_end": None, "method": NONE}


def page_spans_from_locator(rows: list[dict[str, Any]]) -> dict[int, tuple[int, int]]:
    """Character span of each page, from `locator_map.jsonl`.

    The locator map records one segment per line of the normalized text with the
    page it came from; a page's span is the union of its segments.
    """
    spans: dict[int, tuple[int, int]] = {}
    for row in rows:
        page = (row.get("original_locator_start") or {}).get("page")
        if page is None:
            continue
        start = row.get("normalized_char_start")
        end = row.get("normalized_char_end")
        if start is None or end is None:
            continue
        if page in spans:
            spans[page] = (min(spans[page][0], start), max(spans[page][1], end))
        else:
            spans[page] = (start, end)
    return spans


#: A number as a document prints one: `$8,698`, `(1,234)`, `21.0%`, `-0.076`.
_NUMERIC = re.compile(r"-?\(?\$?\d[\d,]*\.?\d*\)?%?")


def _digits(token: str) -> str:
    """A number stripped to what a damaged text layer would still show.

    `$8,698` and `8698` are the same figure; a scan that lost the dollar sign
    and the comma did not lose the number. Comparing raw strings would report
    formatting as misreading, which is the mistake this whole area of the
    pipeline exists to avoid making about transcriptions.
    """
    return re.sub(r"[^\d.]", "", token)


def reconcile(asset: dict[str, Any], comparison_text: str) -> dict[str, Any]:
    """How much of a transcription's arithmetic is corroborated by the text layer.

    A page whose structure a text extractor destroyed usually still yields its
    DIGITS -- the columns collapse and the headers fuse, but `33,314` survives
    as characters somewhere on the line. So the numbers in a transcription can
    be checked against the wreckage even though the structure cannot, and that
    check is the cheapest available evidence that a model read the page rather
    than invented it.

    It gates nothing. A low ratio is a reason to look at the page image, which
    is retained beside the asset for exactly that purpose, not a reason to
    discard the reading -- a table of percentages that the text layer dropped
    entirely would score zero while being perfectly transcribed.
    """
    text = asset.get("text", "") or ""
    payload = asset.get("payload", {})
    if payload.get("cells"):
        text += " " + " ".join(str(c.get("text", "")) for c in payload["cells"])
    tokens = [t for t in (_digits(m) for m in _NUMERIC.findall(text)) if t and t != "."]
    if not tokens:
        return {"numeric_tokens": 0, "found_in_text_layer": 0, "ratio": None,
                "not_found": []}

    haystack = re.sub(r"[^\d.]", "", comparison_text)
    found, missing = 0, []
    for token in tokens:
        if token in haystack:
            found += 1
        else:
            missing.append(token)
    return {
        "numeric_tokens": len(tokens),
        "found_in_text_layer": found,
        "ratio": round(found / len(tokens), 4),
        # Capped: a wholly-invented table would otherwise print its whole self.
        "not_found": sorted(set(missing))[:20],
    }


def overlaps(a: tuple[int | None, int | None], b: tuple[int | None, int | None]) -> bool:
    if a[0] is None or b[0] is None:
        return False
    return a[0] < b[1] and b[0] < a[1]


def link(units: list[dict[str, Any]],
         assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """One record per (asset, unit) pair whose spans overlap.

    Written to its own file rather than back into `assets.jsonl`, which Pass 0
    sealed with a content hash. A relationship discovered in Pass 1 is not a
    property of the Pass 0 artifact and re-sealing one to hold it would make the
    seal mean less.
    """
    links: list[dict[str, Any]] = []
    for asset in assets:
        anchor = asset.get("anchor") or {}
        span = (anchor.get("char_start"), anchor.get("char_end"))
        for unit in units:
            # A citation is checked across ALL of the unit's evidence, not only
            # the record that happened to overlap. A formula citation quotes
            # LaTeX that is not in the flat text at all, so its stored offsets
            # fall back to a line range that need not overlap the anchor -- and
            # reading `cited` off the overlapping record reported every one of
            # them as an accident of proximity.
            cited = any((e.get("asset_ref") or {}).get("asset_id") == asset["asset_id"]
                        for e in unit.get("evidence", []))
            hit = None
            if span[0] is not None:
                for evidence in unit.get("evidence", []):
                    ev_span = (evidence.get("normalized_char_start"),
                               evidence.get("normalized_char_end"))
                    if ev_span[0] is not None and overlaps(span, ev_span):
                        hit = ev_span
                        break
            # Linked when the spans overlap OR when the unit quoted the asset.
            # A citation is the stronger claim of the two and must not be lost
            # because the quote lives outside the anchored range.
            if hit is None and not cited:
                continue
            links.append({
                "asset_id": asset["asset_id"],
                "unit_id": unit["unit_id"],
                "source_id": asset.get("source_id", ""),
                "anchor_method": anchor.get("method", NONE),
                "asset_span": [span[0], span[1]],
                "unit_span": list(hit) if hit else None,
                # Both are relationships; only one is a citation, and a consumer
                # weighing evidence needs to tell them apart.
                "cited": cited,
                "relation": "cited" if cited else "same_region",
            })
    return links


def apply_links(units: list[dict[str, Any]], links: list[dict[str, Any]]) -> None:
    """Write `related_asset_ids` onto each unit, in place.

    Both directions are stored because both files are read independently: a
    consumer walking `units.jsonl` should not have to open a second file to
    discover that a unit has a table attached to it.
    """
    from .artifacts import seal

    by_unit: dict[str, list[str]] = {}
    for link_row in links:
        ids = by_unit.setdefault(link_row["unit_id"], [])
        if link_row["asset_id"] not in ids:
            ids.append(link_row["asset_id"])
    for unit in units:
        related = by_unit.get(unit["unit_id"], [])
        if not related:
            continue
        unit["related_asset_ids"] = related
        # Re-seal. The unit was sealed when it was materialized and this adds a
        # field to it; leaving the old digest in place would make every unit
        # with an asset fail the integrity check the pipeline runs on itself,
        # which is the check that would catch real tampering.
        unit.update(seal(unit))


def orphans(assets: list[dict[str, Any]], links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Assets no unit relates to.

    Not the same question as "which assets went uncited", and a much sharper
    one. An uncited asset may sit squarely in a well-covered passage that simply
    had no reason to quote it. An orphan sits in a region of the source from
    which nothing was extracted at all, which is a hole in the reading rather
    than a judgment about evidence.
    """
    related = {link_row["asset_id"] for link_row in links}
    return [a for a in assets if a["asset_id"] not in related]


def anchor_assets(assets: list[dict[str, Any]], text: str,
                  locator_rows: list[dict[str, Any]] | None = None) -> None:
    """Anchor and verify every asset in place, then re-seal it.

    Called wherever assets are written -- Pass 0 for everything recovered from
    markup or rendered, Pass 1 for whatever the visual read produces -- because
    an asset without an anchor cannot be related to anything and would be an
    orphan by construction rather than by fact.

    The record is re-sealed after the fields are added: `content_sha256` covers
    the record, so adding to it and leaving the old hash would make every asset
    fail the integrity check the pipeline runs on itself.
    """
    from .assets import FIDELITY_TRANSCRIBED

    spans = page_spans_from_locator(locator_rows or [])
    for asset in assets:
        asset["anchor"] = locate(asset, text, spans)
        if asset.get("fidelity") == FIDELITY_TRANSCRIBED:
            anchor = asset["anchor"]
            # Compare against the page the asset came from where we know it,
            # and against the whole document where we do not. A page-scoped
            # comparison is the stronger check: a figure that appears elsewhere
            # in the document would otherwise corroborate itself.
            if anchor["method"] == PAGE_REGION:
                window = text[anchor["char_start"]:anchor["char_end"]]
            else:
                window = text
            asset["verification"] = reconcile(asset, window)
        asset["content_sha256"] = _reseal(asset)


def _reseal(asset: dict[str, Any]) -> str:
    import hashlib
    import json as _json

    body = {k: v for k, v in asset.items() if k != "content_sha256"}
    return hashlib.sha256(
        _json.dumps(body, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
