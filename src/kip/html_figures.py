"""Figures out of HTML: the images a document uses to carry content.

A chart is the one kind of source content this pipeline had no path for at all.
A table survives as a grid and a formula as LaTeX, but a line chart is pixels,
and until now an `<img>` inside an HTML document was not extracted in any form --
so an article whose central result is a graph contributed nothing about it.

The rule here is the same as everywhere else in the asset layer and it is worth
stating plainly: NOTHING READS THE IMAGE. The figure is captured, its caption
and heading are captured, it is anchored to the text around it, and it is
displayed. No model describes what the chart shows, because a description of a
chart is not evidence -- it is a reading with no way to check it, and the
`inferred` fidelity class exists precisely to mark that and is deliberately left
unused.

WHICH IMAGES COUNT. Most `<img>` elements in a real document are furniture:
spacers, logos, navigation buttons, social icons. The Sharpe reprint's only
image is a `home.jpg` button below the closing rule. So an image qualifies as a
figure when the document treats it as content -- it sits in a `<figure>`, or has
a caption, or carries alt text substantial enough to be a description rather
than a label. An image that is none of those is chrome and is skipped, which is
a judgment that will occasionally be wrong in both directions and is recorded in
`extractor` so it can be revisited.
"""

from __future__ import annotations

import html as html_module
import re
from typing import Any

from .assets import ASSET_FIGURE, FIDELITY_TRANSCRIBED, build_asset

_IMG = re.compile(r"<img\b[^>]*>", re.I | re.S)
_FIGURE = re.compile(r"<figure\b.*?</figure\s*>", re.I | re.S)
_FIGCAPTION = re.compile(r"<figcaption\b[^>]*>(.*?)</figcaption\s*>", re.I | re.S)
_HEADING = re.compile(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]\s*>", re.I | re.S)
_TAGS = re.compile(r"<[^>]+>")

#: Classes that mark an image as a rendering of something already captured
#: elsewhere. MediaWiki emits its equations as PNGs with the TeX in `alt`; those
#: are formulas and `html_formulas` already has them exactly.
_NOT_A_FIGURE = re.compile(r"mwe-math|\bicon\b|\blogo\b|\bspacer\b|\bavatar\b", re.I)

#: Alt text shorter than this is a label ("logo", "home"), not a description.
_MIN_ALT = 25


def _attr(name: str, fragment: str) -> str:
    found = re.search(rf"\b{name}\s*=\s*\"([^\"]*)\"|\b{name}\s*=\s*'([^']*)'",
                      fragment, re.I)
    if not found:
        return ""
    return html_module.unescape(found.group(1) or found.group(2) or "").strip()


def _plain(fragment: str) -> str:
    return re.sub(r"\s+", " ", html_module.unescape(_TAGS.sub(" ", fragment))).strip()


def _heading_before(html_text: str, position: int) -> str:
    """The nearest section heading above this point in the document."""
    last = ""
    for match in _HEADING.finditer(html_text, 0, position):
        text = _plain(match.group(1))
        if text:
            last = text
    return last


def _context(html_text: str, start: int, end: int, width: int = 200) -> str:
    before = _plain(html_text[max(0, start - width * 4):start])[-width:]
    after = _plain(html_text[end:end + width * 4])[:width]
    return f"{before} … {after}".strip()


def extract_figures(html_text: str) -> list[dict[str, Any]]:
    """Every image the document treats as content, in document order."""
    # A <figure> wrapper is the document saying "this is content", so those are
    # collected first and their images are not reconsidered as bare <img>.
    claimed: set[int] = set()
    out: list[dict[str, Any]] = []

    for block in _FIGURE.finditer(html_text):
        fragment = block.group(0)
        img = _IMG.search(fragment)
        if not img:
            continue
        claimed.add(block.start() + img.start())
        caption_match = _FIGCAPTION.search(fragment)
        out.append({
            "src": _attr("src", img.group(0)),
            "alt": _attr("alt", img.group(0)),
            "caption": _plain(caption_match.group(1)) if caption_match else "",
            "heading": _heading_before(html_text, block.start()),
            "surrounding_text": _context(html_text, block.start(), block.end()),
            "position": block.start(),
            "reason": "figure_element",
        })

    for img in _IMG.finditer(html_text):
        if img.start() in claimed:
            continue
        fragment = img.group(0)
        if _NOT_A_FIGURE.search(fragment):
            continue
        alt = _attr("alt", fragment)
        src = _attr("src", fragment)
        if not src:
            continue
        if len(alt) < _MIN_ALT:
            continue
        out.append({
            "src": src,
            "alt": alt,
            "caption": "",
            "heading": _heading_before(html_text, img.start()),
            "surrounding_text": _context(html_text, img.start(), img.end()),
            "position": img.start(),
            "reason": "descriptive_alt",
        })

    out.sort(key=lambda f: f["position"])
    return out


def figure_assets(html_text: str, source_id: str, start_index: int = 1,
                  copy_into: Any = None, source_dir: Any = None) -> list[dict[str, Any]]:
    """Figure assets, with the image copied alongside where it is a local file.

    A remote image is recorded without its bytes rather than fetched: a run must
    not reach the network, and a URL the reader can follow is more honest than a
    copy that may not be what the page served.
    """
    from pathlib import Path
    from shutil import copyfile

    out: list[dict[str, Any]] = []
    for found in extract_figures(html_text):
        payload: dict[str, Any] = {
            "src": found["src"],
            "alt": found["alt"],
            "caption": found["caption"],
            "heading": found["heading"],
            "surrounding_text": found["surrounding_text"],
            "detected_by": found["reason"],
        }
        if copy_into is not None and source_dir is not None and "://" not in found["src"]:
            origin = Path(source_dir) / found["src"]
            if origin.is_file():
                target = Path(copy_into) / origin.name
                target.parent.mkdir(parents=True, exist_ok=True)
                copyfile(origin, target)
                payload["image"] = f"{target.parent.name}/{target.name}"
        out.append(build_asset(
            kind=ASSET_FIGURE, source_id=source_id, index=start_index + len(out),
            # Nothing read it, so nothing was recovered from markup and nothing
            # was transcribed. The class is the weakest honest one until the
            # taxonomy has a name for "captured, not interpreted".
            fidelity=FIDELITY_TRANSCRIBED,
            extractor="html_figure_v1",
            text=found["caption"] or found["alt"],
            payload=payload,
        ))
    return out
