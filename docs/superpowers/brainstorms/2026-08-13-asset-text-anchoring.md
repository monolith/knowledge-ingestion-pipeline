# Brainstorm: anchoring assets to text

**Date:** 2026-08-13
**Next step:** Write spec → `docs/superpowers/specs/2026-08-13-asset-text-anchoring-spec.md`

## Context

The asset layer (tables, formulas, figures kept beside `normalized.txt` rather
than flattened into it) shipped earlier today. A run folder README now reports
how many assets are cited by at least one unit, and the numbers prompted this
conversation:

| run | assets | cited | uncited |
|---|---|---|---|
| GE 10-K | 100 tables | 8 | 92 |
| Wikipedia Black–Scholes | 119 | 33 | 86 |
| De Bondt & Thaler | 18 | 13 | 5 |

Investigating the uncited assets found three different situations counted as one
number:

1. **Not content.** GE's cover page (state of incorporation, IRS number, ticker
   listings, filer-status checkboxes), Wikipedia's six navigation boxes, the
   four De Bondt page renders that exist so a transcription can be checked
   against the image it was read from. Correctly uncited.
2. **Content nothing needed to cite.** 80 of Black–Scholes' 86 are inline
   symbol-names — `\tau`, `C(S,t)`. Worth capturing because the flat text
   mangles them; worth citing by nobody.
3. **Real content nobody used.** 63 of GE's 92 carry four or more money figures:
   the Statement of Cash Flows (74 figures), the pension plan funded status
   (78), the Statement of Changes in Shareholders' Equity, segment revenue and
   operating profit, the tax rate reconciliation.

Two mechanical contributors were found while investigating:

- `_render_assets` caps the extraction prompt at 60 tables. GE has 100, so 40
  were never put in front of the extractor. The prompt says "(40 further tables
  not shown)" rather than hiding it, but the extractor could not cite what it
  never saw.
- The De Bondt rerun dropped `asset_ref` when carrying prior-run units forward,
  so Table I's two cell citations were lost. A regression introduced 2026-08-13.

## The problem, as Anatoly stated it

> "i don't like loding extracted data. citation for tables, formulas, and
> eventually charts should be different from text."

An asset currently survives into the output only if some unit happens to cite it
as evidence. That is the text model — quote it or lose it — applied to things
that are not text.

> "essrntially we need to a) feel comfortable that The extraction worked
> correctly and 2) tie it back to the text to which it is relevant (so a
> relationship), and 3) the text itself... like jsonl and readme, should contain
> the asset linkage information (and read me show the firmula/table/chart...
> whether tovshow it or butvdepends on whether the text is shown"

Three requirements: verify the extraction, relate each asset to the text it
belongs to, and carry that linkage in both the JSONL and the README — with the
README showing an asset where it shows the text the asset is anchored to.

## Decisions

### Anchoring: character span, deterministic

Each asset anchors to a character range in `normalized.txt`. A unit is related
to an asset when any of its evidence spans overlaps that range.

Chosen over model-judged relevance (a call per asset, not reproducible) and over
a hybrid. Anatoly: *"Character span, deterministic"*.

Available inputs, confirmed by inspection:
- HTML: the table's flattened text is already inside `normalized.txt`, so the
  span can be located directly.
- PDF: `locator_map.jsonl` maps character spans to page numbers, so a page
  render and anything read off it anchors to that page's region.
- No asset carries `char_start` today; `build_asset` accepts the field and
  nothing passes it.

### Orphan assets: name the coverage gap

An asset whose anchor overlaps no unit is reported as a gap — "the Statement of
Cash Flows sits in a region of the source no unit was extracted from" — and
becomes a finding the coverage audit acts on. Nothing is forced.

Chosen over forcing extraction to cover every asset (which would manufacture
units for the filer-status checkboxes) and over shipping orphans unattached
(unreviewed material in the knowledge base). Anatoly: *"Name it as a coverage
gap"*.

### Verifying a transcription: numeric reconciliation, render retained

Digits usually survive a damaged text layer even when structure does not. For a
`transcribed` asset, check what fraction of its numeric tokens appear in that
page's raw text, and record the fraction and the misses. The page render stays
beside it for a human check.

Chosen over a second independent read (one extra vision call per page) and over
both. Anatoly: *"Numeric reconciliation + keep the render"*.

## Not decided here

- Where the line sits between a table that deserves a unit and one that does
  not. Raised in conversation as an open judgment: *"I can say the GE extraction
  under-used its tables. I can't say all 63 should have been cited."* Not
  resolved.
- Charts. Deferred by Anatoly earlier: *"ok let's skip charts."* The design must
  not preclude them — he wrote "tables, formulas, and eventually charts" — but
  no chart work is in scope.
- The 60-table prompt cap. Found during this investigation; not discussed as a
  decision.

## Related

- `demo/real-runs/README.md` — the fidelity classes and what the runs measured.
- `research/2026-08-13-non-textual-content-research.md` — evidence behind
  `exact` / `transcribed` / `inferred`.
