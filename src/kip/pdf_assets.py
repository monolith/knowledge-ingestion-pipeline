"""Formulas and figures out of a PDF, by rendering the page and reading it.

A PDF stores an equation as positioned glyphs, not as mathematics. Every text
extractor therefore returns something that looks like text and is not: the
De Bondt & Thaler t-statistic reached this pipeline's corpus as the literal
string `Tt = ARw,t/(st/ViN)`, in which `Vi` is a square-root sign and the
subscripts are gone. No amount of better text extraction recovers that, because
the information was never in the text layer.

None of the five sources this pipeline has processed carries math markup of any
kind -- no MathML, no LaTeX. So a formula is not a text problem. It is a visual
one, and the established answer is the same one the field uses: render the
region and have a model read it.

WHY NO ML STACK. The obvious route is a document-understanding library, and the
obvious library pulls PyTorch and, on a default install, several gigabytes of
CUDA wheels onto a host with no GPU. That trade is wrong twice over: the
transcription is a vision-model call this pipeline already knows how to make,
and under the handoff runtime the vision model is the agent running the CLI.
So the only new dependency is a renderer -- pypdfium2, about 20 MB, CPU-only --
and the PNG writing reuses the encoder already in `ccitt.py`.

WHAT FIDELITY THIS PRODUCES. `transcribed`, never `exact`. A transcription is a
reading of a picture, and the research behind this design is specific about what
follows: string comparison is the wrong check for one. UniMERNet scores 0.48
exact-match against 0.81 when outputs are rendered and compared visually, so
roughly a third of correct transcriptions differ textually from the reference
(Wang et al., CVPR 2025). A formula asset therefore carries the crop it was read
from, and the crop is what makes the claim checkable -- by a human or by a
second model -- rather than a string comparison that would reject correct
answers.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .assets import ASSET_FIGURE, ASSET_FORMULA, FIDELITY_TRANSCRIBED, build_asset

#: Rendering scale. 2x of a 1985 journal scan is legible to a vision model
#: without producing files too large to hand around.
RENDER_SCALE = 2

#: Marks left behind when a text extractor meets mathematics. These are not
#: math -- they are the damage, and their presence on a page is the signal that
#: the page holds something the text layer could not represent.
_MATH_DAMAGE = re.compile(
    r"(?:"
    r"[=<>]\s*\[|\]\s*/|"          # bracketed expressions with operators
    r"\bV[iI'’]\s*[A-Z]|"          # a square-root sign read as V + a letter
    r"\b\d\s*S\d\s*/\s*[A-Z]|"     # squared terms flattened, e.g. 2S2/N
    r"[A-Za-z]\s*,\s*[a-z]\s*[/)]" # subscript commas surviving as punctuation
    r")"
)

#: A page needs more than one mark to qualify. Ordinary prose produces the
#: occasional false positive; a page of mathematics produces many.
_MIN_MARKS = 2


def pages_with_math(text: str, page_marker: re.Pattern[str] | None = None) -> list[int]:
    """Page numbers whose text shows the damage mathematics leaves behind.

    A detector rather than a classifier, and deliberately cheap: it decides
    which pages are worth rendering, and a page rendered unnecessarily costs one
    image while a page missed costs the formula. The threshold is set to be
    generous in the direction that is recoverable.
    """
    marker = page_marker or re.compile(r"\[\[PAGE (\d+)\]\]")
    pages: dict[int, int] = {}
    current = 0
    for line in text.splitlines():
        found = marker.search(line)
        if found:
            current = int(found.group(1))
            continue
        hits = len(_MATH_DAMAGE.findall(line))
        if hits:
            pages[current] = pages.get(current, 0) + hits
    return sorted(page for page, count in pages.items() if count >= _MIN_MARKS and page)


def render_pages(pdf: Path, pages: list[int], out_dir: Path, *,
                 scale: int = RENDER_SCALE) -> dict[int, Path]:
    """Render the given 1-based pages to PNG. Returns page -> file.

    Raises nothing on a missing renderer: a source whose formulas cannot be
    rendered still has usable text, and losing the text over a formula is the
    wrong trade.
    """
    try:
        import pypdfium2
    except ImportError:
        return {}
    from .ccitt import write_png_rgb

    out_dir.mkdir(parents=True, exist_ok=True)
    written: dict[int, Path] = {}
    document = pypdfium2.PdfDocument(str(pdf))
    try:
        for page in pages:
            if not 1 <= page <= len(document):
                continue
            bitmap = document[page - 1].render(scale=scale)
            target = out_dir / f"page-{page:04d}.png"
            write_png_rgb(bitmap.width, bitmap.height, bytes(bitmap.buffer), target,
                          channels=bitmap.n_channels, stride=bitmap.stride)
            written[page] = target
    finally:
        document.close()
    return written


def formula_asset(*, source_id: str, index: int, page: int, image_rel: str,
                  latex: str = "", surrounding: str = "",
                  extractor: str = "pdf_render_v1+vision") -> dict[str, Any]:
    """A formula, as the crop it was read from plus the reading itself.

    `latex` is empty until a vision pass fills it. An asset with no transcription
    is still useful -- it records that a formula exists on a page and where -- and
    it is honest about not having been read yet, which an omitted asset is not.
    """
    return build_asset(
        kind=ASSET_FORMULA, source_id=source_id, index=index,
        fidelity=FIDELITY_TRANSCRIBED, extractor=extractor,
        text=latex,
        payload={"latex": latex, "image": image_rel, "surrounding_text": surrounding,
                 "transcribed": bool(latex)},
        page=page,
    )


def page_image_asset(*, source_id: str, index: int, page: int, image_rel: str,
                     extractor: str = "pdf_render_v1") -> dict[str, Any]:
    """The rendered page itself, so a consumer can check a transcription."""
    return build_asset(
        kind=ASSET_FIGURE, source_id=source_id, index=index,
        fidelity=FIDELITY_TRANSCRIBED, extractor=extractor,
        text="", payload={"image": image_rel, "kind": "page_render"}, page=page,
    )
