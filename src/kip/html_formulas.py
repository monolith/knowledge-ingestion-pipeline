"""Formulas out of HTML, from the markup rather than from a picture of it.

The PDF path recovers a formula by rendering the page and reading it, because a
PDF stores an equation as positioned glyphs and there is nothing else to work
with. HTML is the opposite case and deserves the opposite treatment: when a
document carries MathML, the author's own LaTeX is usually sitting in the markup
already, and reading a rendered image of it would be strictly worse -- a
transcription where an exact copy was available.

That distinction is the whole point of the fidelity field. A formula recovered
from `<annotation encoding="application/x-tex">` is `exact`: nobody inferred it,
it is what the author wrote. A formula read off a rendered page is
`transcribed`, and the field's own evidence says string comparison is the wrong
check for one of those. Storing both at the same fidelity would throw away the
difference.

Three sources of markup, in descending order of trust:

  1. `<annotation encoding="application/x-tex">` inside `<semantics>` -- the
     canonical MathML carrier for the original TeX. Wikipedia and arXiv's HTML
     both emit it.
  2. The `alttext` attribute on `<math>` -- the same string in practice, and
     present when the annotation is not.
  3. `<img class="mwe-math-fallback-image...">` with LaTeX in `alt` -- older
     MediaWiki output, where the equation is a picture and the alt text is the
     source.

MathML with neither annotation nor alttext is recorded with its presentation
markup and an empty `latex`, because "a formula is here and could not be read"
is information and omitting it is not.
"""

from __future__ import annotations

import html as html_module
import re
from typing import Any

from .assets import ASSET_FORMULA, FIDELITY_EXACT, build_asset

#: `<math>` through its closing tag. Non-greedy, and tolerant of attributes.
_MATH = re.compile(r"<math\b[^>]*>.*?</math\s*>", re.I | re.S)
_ANNOTATION = re.compile(
    r"<annotation\b[^>]*encoding\s*=\s*[\"']application/x-tex[\"'][^>]*>(.*?)</annotation\s*>",
    re.I | re.S)
_ALTTEXT = re.compile(r"\balttext\s*=\s*\"([^\"]*)\"|\balttext\s*=\s*'([^']*)'", re.I)
_DISPLAY = re.compile(r"\bdisplay\s*=\s*[\"']?block", re.I)
#: MediaWiki's image fallback: the equation is a PNG and the alt text is its TeX.
_FALLBACK_IMG = re.compile(
    r"<img\b[^>]*\bclass\s*=\s*[\"'][^\"']*mwe-math[^\"']*[\"'][^>]*>", re.I)
_ALT = re.compile(r"\balt\s*=\s*\"([^\"]*)\"|\balt\s*=\s*'([^']*)'", re.I)
_TAGS = re.compile(r"<[^>]+>")

#: MediaWiki wraps its TeX in a \displaystyle directive that is presentation,
#: not content. Stripped so two spellings of the same formula compare equal.
_DISPLAYSTYLE = re.compile(r"^\s*\{\s*\\displaystyle\s*(.*)\}\s*$", re.S)


def _clean_latex(raw: str) -> str:
    text = html_module.unescape(raw).strip()
    match = _DISPLAYSTYLE.match(text)
    if match:
        text = match.group(1).strip()
    return re.sub(r"\s+", " ", text).strip()


def _attr(pattern: re.Pattern[str], fragment: str) -> str:
    found = pattern.search(fragment)
    if not found:
        return ""
    return found.group(1) if found.group(1) is not None else (found.group(2) or "")


def extract_formulas(html_text: str, *, context_chars: int = 160) -> list[dict[str, Any]]:
    """Every formula the markup carries, in document order.

    Each result is a dict with `latex`, `display` (block or inline), `mathml`
    and `surrounding_text`. The surrounding text is what lets a consumer place
    the formula in the document: an equation with no context is unusable however
    exactly it was captured.
    """
    out: list[dict[str, Any]] = []
    seen: set[str] = set()

    for match in _MATH.finditer(html_text):
        fragment = match.group(0)
        latex = _clean_latex(
            (_ANNOTATION.search(fragment).group(1) if _ANNOTATION.search(fragment) else "")
            or _attr(_ALTTEXT, fragment))
        # Inline variables -- a lone symbol -- are not formulas worth carrying.
        if latex and len(latex) < 3:
            continue
        key = latex or fragment[:120]
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "latex": latex,
            "display": "block" if _DISPLAY.search(fragment) else "inline",
            "mathml": fragment if not latex else "",
            "surrounding_text": _context(html_text, match.start(), match.end(), context_chars),
        })

    for match in _FALLBACK_IMG.finditer(html_text):
        latex = _clean_latex(_attr(_ALT, match.group(0)))
        if len(latex) < 3 or latex in seen:
            continue
        seen.add(latex)
        out.append({"latex": latex, "display": "block", "mathml": "",
                    "surrounding_text": _context(html_text, match.start(), match.end(),
                                                 context_chars)})
    return out


def _context(html_text: str, start: int, end: int, width: int) -> str:
    before = _TAGS.sub(" ", html_text[max(0, start - width * 3):start])
    after = _TAGS.sub(" ", html_text[end:end + width * 3])
    before = re.sub(r"\s+", " ", html_module.unescape(before)).strip()[-width:]
    after = re.sub(r"\s+", " ", html_module.unescape(after)).strip()[:width // 2]
    return f"{before} … {after}".strip()


def formula_assets(html_text: str, source_id: str, start_index: int = 1) -> list[dict[str, Any]]:
    """Formula assets from markup. `exact` when the LaTeX was in the document.

    A formula whose MathML carried no TeX annotation is still recorded, with an
    empty `latex` and its presentation markup kept, so a later vision pass can
    fill it in. It is marked `transcribed` rather than `exact` in that case,
    because whatever eventually reads it will be reading rather than copying.
    """
    from .assets import FIDELITY_TRANSCRIBED

    out: list[dict[str, Any]] = []
    for found in extract_formulas(html_text):
        exact = bool(found["latex"])
        out.append(build_asset(
            kind=ASSET_FORMULA, source_id=source_id, index=start_index + len(out),
            fidelity=FIDELITY_EXACT if exact else FIDELITY_TRANSCRIBED,
            extractor="html_mathml_v1",
            text=found["latex"],
            payload={"latex": found["latex"], "display": found["display"],
                     "mathml": found["mathml"], "transcribed": exact,
                     "surrounding_text": found["surrounding_text"]},
        ))
    return out
