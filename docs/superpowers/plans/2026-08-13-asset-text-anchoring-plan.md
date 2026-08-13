# Plan: anchoring assets to text

**Spec:** `docs/superpowers/specs/2026-08-13-asset-text-anchoring-spec.md`

## Tasks (ordered)

1. **Anchor computation**
   - Implements: every asset carries `anchor {char_start, char_end, method}` (Spec: Decisions § Anchor)
   - Files: new `src/kip/anchors.py`
   - Contents: `locate(asset, text, locator_map)` returning an anchor dict.
     Order of attempt: the asset's own flattened text (`html_text`), then its
     `surrounding_text` (`context_located`), then the page span from the locator
     map (`page_region`), then `none`.
   - Verify: `pytest tests/test_anchors.py` — one test per method, plus one
     asserting a formula read off a page narrows past `page_region` when its
     context is locatable.

2. **Numeric reconciliation**
   - Implements: `verification {numeric_tokens, found_in_text_layer, ratio, not_found}` on transcribed assets (Spec: Decisions § Verifying a transcription)
   - Files: `src/kip/anchors.py`
   - Contents: `reconcile(asset, comparison_text)`; tokens normalized by
     stripping `$ , % ( ) -`. Gates nothing.
   - Verify: a test where a transcription's figures are present in a damaged
     text layer scores 1.0, and one where an invented figure is absent scores
     below 1.0 and names it.
   - Depends on: task 1 (needs the anchor to pick the comparison text)

3. **Set anchors where assets are created**
   - Implements: anchors computed in Pass 0 for markup/render assets, Pass 1 for visual-read assets (Spec: Decisions § Anchor)
   - Files: `src/kip/normalize.py`, `src/kip/extract.py`
   - Verify: `kip run --stop-after normalize` on the Black–Scholes and De Bondt
     sources; every asset has an anchor with a method.
   - Depends on: tasks 1, 2

4. **Remove the table cap**
   - Implements: "The cap is removed, not raised" (Spec: Decisions § Prompt cap)
   - Files: `src/kip/extract.py` (`_render_assets`)
   - Verify: the GE extraction prompt contains 100 `[tbl-` markers, not 60.

5. **Chart capture: HTML `<img>`**
   - Implements: "HTML `<img>` becomes a figure asset" (Spec: Decisions § Charts)
   - Files: new extractor in `src/kip/html_figures.py`, wired in `normalize.py`
   - Contents: every `<img>` with a resolvable local source becomes a figure
     asset with its `alt` text and surrounding context; remote sources are
     recorded without bytes.
   - Verify: a test on markup with one content image and one layout image.

6. **Chart capture: PDF figure pages**
   - Implements: "A PDF page carrying a figure caption is rendered" (Spec: Decisions § Charts)
   - Files: `src/kip/pdf_assets.py` (`pages_with_figures`), wired in `normalize.py`
   - Verify: De Bondt flags pages 9, 11, 12 and no others.
   - Depends on: task 3

7. **Relationship: link units to assets**
   - Implements: `related_asset_ids` on units and `02_units/asset_links.jsonl` (Spec: Decisions § Relationship)
   - Files: `src/kip/anchors.py` (`link`), `src/kip/extract.py` (call before sealing)
   - Verify: De Bondt's Table I is related to the units discussing Table I with
     no unit citing it.
   - Depends on: task 3

8. **Orphans into coverage and validate**
   - Implements: orphan count handed to the coverage audit; validate warning (Spec: Decisions § Orphan assets)
   - Files: `src/kip/audit.py`, `src/kip/validate.py`
   - Verify: GE's Statement of Cash Flows is named as an orphan or related.
   - Depends on: task 7

9. **Travel rule in the enqueue payload**
   - Implements: an entry carries every asset related to any source unit (Spec: Decisions § Travel rule)
   - Files: `src/kip/enqueue.py`
   - Verify: an enqueued entry carries `related_asset_ids` including an asset no
     unit cited.
   - Depends on: task 7

10. **Captions and headings**
    - Implements: an asset carries its own caption and heading (Spec: Decisions § Captions and headings belong to the asset)
    - Files: `src/kip/html_tables.py`, `src/kip/html_figures.py`, `src/kip/html_formulas.py`, `src/kip/extract.py` (visual read schema)
    - Contents: `payload.caption` and `payload.heading`; the caption becomes the
      first anchor attempt (`caption_located`); a table's spanning title row is
      promoted to `caption` and left in the grid.
    - Verify: De Bondt's Figure 1 carries "Figure 1. Cumulative Average
      Residuals for Winner and Loser Portfolios..."; GE's cash-flow table
      carries `STATEMENT OF CASH FLOWS`.
    - Depends on: task 1

11. **README: assets under the text they belong to**
    - Implements: asset shown under the entries it relates to; orphans in a named section (Spec: Decisions § README)
    - Files: `demo/real-runs/render.py`
    - Verify: regenerate all six; every link and image resolves.
    - Depends on: tasks 9, 10

12. **Re-run the affected demos**
    - Implements: acceptance criteria
    - Verify: `kip validate` zero errors on all six runs.
    - Depends on: task 10

## Open questions

Carried from the spec. Neither blocks any task below.

- What fidelity a figure asset carries when it holds only an image and no
  reading. `exact` is defined as structure recovered from markup, which a raster
  is not; `transcribed` says a model read it, which nothing did. Page renders
  keep their current class until decided.
