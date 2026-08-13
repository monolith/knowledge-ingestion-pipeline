# Spec: anchoring assets to text

**Brainstorm:** `docs/superpowers/brainstorms/2026-08-13-asset-text-anchoring.md`
**Next step:** Write plan → `docs/superpowers/plans/2026-08-13-asset-text-anchoring-plan.md`

## Goal

An asset stops depending on being cited to survive. Each one anchors to a
character range in `normalized.txt`; every unit whose evidence overlaps that
range is related to it; the linkage travels in the JSONL and in the README.
(BS: Decisions — Anchoring)

## Decisions

### Anchor

- Every asset carries `anchor: {char_start, char_end, method}` into
  `normalized.txt`. (BS: "Each asset anchors to a character range in
  `normalized.txt`")
- A unit is related to an asset when any of its evidence spans overlaps the
  anchor range. (BS: "A unit is related to an asset when any of its evidence
  spans overlaps that range")
- [NEW — confirm] `method` records how the anchor was found, because the
  precisions differ by an order of magnitude and a consumer must be able to tell
  them apart:
  - `html_text` — the asset's own flattened text located in `normalized.txt`.
    Tight.
  - `context_located` — the asset's `surrounding_text` located in
    `normalized.txt`. Tight; used for a formula read off a page.
  - `page_region` — the character span of the page the asset came from, via
    `locator_map.jsonl`. Coarse: a whole page, so every unit on that page
    relates to it.
  - `none` — no anchor could be computed. The asset is an orphan by definition.
- Anchors are computed where the asset is created: Pass 0 for assets from markup
  and page renders, Pass 1 for assets produced by the visual read. (BS:
  "Available inputs, confirmed by inspection" — the visual read runs in Pass 1)
- [NEW — confirm] An asset from a page render narrows to `context_located` when
  its `surrounding_text` can be located, and falls back to `page_region`
  otherwise. Without narrowing, all thirteen De Bondt formulas would anchor to
  three whole pages and relate to every unit on them, which defeats the purpose
  of relating a specific formula to specific text.

### Relationship

- [NEW — confirm] Stored in both directions: `related_asset_ids` on each unit in
  `units.jsonl`, and `02_units/asset_links.jsonl` holding one record per
  (asset, unit) pair with the overlap that produced it. Both files are read
  independently by consumers, and a relationship that exists in only one of them
  is a relationship half the readers cannot see.
- [NEW — confirm] `assets.jsonl` is NOT rewritten to carry `related_unit_ids`.
  It is sealed in Pass 0 with a content hash; adding a field that depends on
  Pass 1 output would require re-sealing a Pass 0 artifact. The relationship
  lives in its own file instead.
- [NEW — confirm] The enqueue payload gains `related_asset_ids`, the union over
  the entry's source units, so a consumer gets the linkage without opening
  `units.jsonl`. (BS: "the jsonl ... should contain the asset linkage
  information" — `enqueue.jsonl` is the JSONL a consumer reads)

### Orphan assets — REVISED 2026-08-13, after the GE run

The brainstorm decided an orphan is a coverage gap to be named. Running it on
the GE filing showed that is the wrong frame, and Anatoly revised it:

> "we only care about tables and formulas and charts that directly relate and
> improve understanding of an enqueu item. just like we don't worry about
> dropped paragraphs that don't add understanding value, neither are we worried
> about tables and formulas that don't add value. whether some thing adds value
> i think is already established by the process that generates enqeue items"

So:

- An asset whose anchor overlaps no unit sits in a passage the extraction read
  and drew nothing from. That is the same decision the extraction makes about a
  paragraph, and neither is tracked as a defect.
- The count is recorded — `counts.assets_unrelated` in `kip validate` — and is
  NOT a warning.
- The coverage audit is handed the list as context and told explicitly not to
  treat it as omissions. It is retained for one reason only: a run where nearly
  every asset is unrelated means the extractor never saw them, which is a wiring
  failure rather than a reading decision, and the GE prompt cap was exactly
  that.
- Nothing is forced. (BS: "Nothing is forced" — unchanged)

Superseded: the earlier decision to name each orphan as a coverage gap, and the
GE run's `fairly_represented: false`, which asserted a purpose the pipeline was
never told.

### Verifying a transcription

- Every `transcribed` asset carries `verification: {numeric_tokens,
  found_in_text_layer, ratio, not_found}`. (BS: Decisions — Verifying a
  transcription)
- The comparison text is the asset's anchored region where the anchor is
  `page_region`, and the whole normalized text otherwise. [NEW — confirm] —
  the brainstorm says "that page's raw text" and does not say what to compare
  against when the asset is not page-anchored.
- [NEW — confirm] Numeric tokens are compared after stripping `$ , % ( ) -` and
  surrounding whitespace, so `$8,698` in a transcription matches `8698` in a
  damaged text layer. Comparing raw strings would report failures that are
  formatting, not misreading.
- [NEW — confirm] `ratio` gates nothing. It is recorded and surfaced; no
  threshold rejects an asset. Consistent with `auditor_confidence`, which the
  spec already records without gating (§13.6).
- An `exact` asset gets no numeric reconciliation. Its verification is that the
  anchor resolved: the parse agrees with the normalizer about what the source
  says. (BS: verification decision is scoped to `transcribed`)

### README

- An asset is shown under the entries whose source units are related to it. (BS:
  "the README showing an asset where it shows the text the asset is anchored
  to")
- [NEW — confirm] Orphan assets are shown in their own section, labelled as the
  coverage gap they are. The brainstorm's display rule would hide them, and its
  orphan rule says to name them; showing them under a heading that says what
  they are satisfies both.
- The flat asset inventory stays, because it is where fidelity, extractor and
  anchor method are reported per asset.

### Captions and headings belong to the asset

- An asset carries its own caption and its own heading where the source has
  them. Anatoly: *"note that if tables or charts or formulas havevheadings and
  or captions, those should be part of that asset"*.
- `payload.caption` — the caption the source attaches to the object: an HTML
  `<caption>` or `<figcaption>`, a PDF figure or table caption line
  (`Figure 1. ...`, `Table I ...`), an equation number.
- `payload.heading` — the nearest preceding section heading, so an asset knows
  where in the document it sits.
- [NEW — confirm] A caption is also anchor material and is tried before
  `surrounding_text`, because a caption sits immediately beside its object and
  is more distinctive than the prose around it. This makes `caption_located` a
  fourth anchor method.
- [NEW — confirm] For a table whose title is the first spanning row of the grid
  rather than a separate element — the shape every GE financial statement takes,
  e.g. `STATEMENT OF COMPREHENSIVE INCOME (LOSS)` — that row is ALSO promoted to
  `caption`, and left in the grid. Removing it would change the row indices that
  existing citations resolve against.
- The README shows the caption and heading with the asset. A chart without its
  caption is an image nobody can interpret, which is the case that motivated
  this.

### Travel rule

- An entry carries every asset related to any of its source units. Anatoly:
  *"if the text is shown to be important enough that ut made it to enqueu then
  any of it's assets travel with it"*.
- This is what decides an asset's survival. Not citation — the anchored text
  surviving. An asset is dropped only when the text it is anchored to was
  dropped, which is a decision about the text and was already made.

### Prompt cap

- The cap is removed, not raised. Anatoly: *"no table cap"*. `_render_assets`
  renders every table and every significant formula the source produced.

### Charts

- Charts use the same mechanism, with no new one. Anatoly: *"i think charts work
  the same way. if they are extracted as images, they can be displayed/linked to
  the surrounding text"*.
- A chart is captured as an IMAGE asset, anchored to surrounding text, related
  to units by the same overlap rule, and displayed in the README. Nothing reads
  it and nothing describes it. The `inferred` fidelity class stays unused.
- [NEW — confirm] Capture is built now rather than designed-for-later, on two
  paths, because without it "charts travel with their text" cannot be tested:
  - HTML `<img>` becomes a figure asset. This also closes a gap flagged earlier
    in conversation and never addressed: an `<img>` inside an HTML page is not
    extracted today, so a chart in an HTML article is silently dropped.
  - A PDF page carrying a figure caption (`Figure N.`) is rendered, the same way
    a page carrying damaged mathematics already is. De Bondt has three such
    pages (9, 11, 12) and the pipeline currently captures nothing from them.

## Non-goals

- Interpreting a chart. No model describes what a chart shows; the image is
  carried and anchored, and that is all. (Follows from the charts decision:
  "extracted as images ... displayed/linked".)
- Deciding which tables deserve a unit. (BS: Not decided here — and the travel
  rule makes it moot for asset survival: the question is about the text, not the
  asset.)

## Open questions

- What fidelity a figure asset carries when it holds only an image and no
  reading. `exact` is defined as structure recovered from markup, which a raster
  is not; `transcribed` says a model read it, which nothing did. Page renders
  are currently `transcribed`. Not resolved, and it gates nothing in this work.

## Acceptance criteria

- Every asset in every demo run carries an `anchor` with a `method`, or is
  reported as having none.
- `02_units/asset_links.jsonl` exists in every run that has assets, and every
  link's overlap is reproducible from the stored spans.
- De Bondt's Table I is related to the units discussing Table I, without any
  unit citing it — demonstrating that the relationship no longer depends on
  citation.
- GE's Statement of Cash Flows is either related to a unit or reported by name
  as an orphan in `corpus_coverage.json`.
- Every `transcribed` asset carries a `verification` record with a ratio.
- Every enqueued entry carries `related_asset_ids` covering every asset related
  to any of its source units, and a spot check confirms an asset no unit cited
  still travels.
- A chart captured from De Bondt or from an HTML source is anchored, related and
  displayed without any model having described it.
- `kip validate` returns zero errors on all six demo runs.
- A run's README shows each related asset under the entry it relates to, and
  orphans under a heading naming them as a gap.
