# Real runs

Six complete runs on real documents, all produced through the CLI in
`--mode handoff` with **no API key**. Every model call was answered by the agent
operating the CLI, one call at a time, against the request the pipeline actually
wrote — so these are model output on real sources, not fixtures.

All six go through **all seven passes** and pass `kip validate` with zero
errors and zero warnings. Four are argument, evidence and reference; one is a
narrative, included because it is the shape the others are not; and one is
almost entirely mathematics, included because that is the shape a text pipeline
handles worst.

**Start with `enqueue.md` in any run folder.** It is the queue handoff — what a
consuming knowledge base would actually receive — rendered as markdown.
Everything else is the machine-readable material behind it.

## What each run shows

| run | source | words | units | density | approved entries |
|---|---|---|---|---|---|
| [`sharpe-arithmetic-of-active-management`](sharpe-arithmetic-of-active-management/enqueue.md) | Sharpe, *The Arithmetic of Active Management* (1991) | 1,650 | 38 | 1 per 43 words | 7 |
| [`debondt-thaler-does-the-stock-market-overreact`](debondt-thaler-does-the-stock-market-overreact/enqueue.md) | De Bondt & Thaler, *Does the Stock Market Overreact?* (1985) | 6,284 | 58 | 1 per 108 words | 20 |
| [`andersen-the-little-mermaid`](andersen-the-little-mermaid/enqueue.md) | Andersen, *The Little Mermaid* (1837) | 9,212 | 42 | 1 per 219 words | 7 |
| [`statement-classifier-specification`](statement-classifier-specification/enqueue.md) | the statement-classifier taxonomy specification | 12,311 | 136 | 1 per 91 words | 33 |
| [`ge-aerospace-10k-fy2025`](ge-aerospace-10k-fy2025/enqueue.md) | GE Aerospace (General Electric) Form 10-K, FY2025 | 56,836 | 112 | 1 per 507 words | 24 |
| [`wikipedia-black-scholes-model`](wikipedia-black-scholes-model/enqueue.md) | Wikipedia, *Black–Scholes model* (CC BY-SA) | 10,507 | 73 | 1 per 144 words | 12 |

Density is not a function of length. The densest source is the shortest: Sharpe
packs a proof, its definitions, three named measurement failures and five
load-bearing footnotes into 1,650 words. The longest non-fiction source is the
sparsest by a wide margin, and the second-longest is the second-densest — it is
a reference document whose fifteen label definitions and nineteen pairwise
separations each have to survive individually. Length predicts nothing; what
predicts density is how much of the document is doing work.

The fairy tale is the outlier at one unit per 219 words, and that is the
expected result rather than a failure: a narrative carries long stretches that
assert nothing. What it does carry is stated rules — an age threshold, a
lifespan, the conditions on obtaining a soul, the terms of a bargain — and those
are what the extraction keeps. Events appear only where a rule or a consequence
hangs on them, so the output is not a retelling.

Every excerpt in all five runs verifies verbatim against `normalized.txt`:
57, 137, 91, 488 and 230 quotes respectively, none corrected, none unverified.

**The 10-K is where density breaks.** At 56,836 words it is 4.6x the next largest
document and the only one where a single extraction call does not reach the end:
96 units came out of the first pass, almost all from the front half of the
filing, and everything from Note 3 onward was nearly unrepresented. This is the
failure the windowing section below describes, caught in the wild.

What recovered it was the omission check plus the repair round. The check named
ten specific missing sections -- the pension note, legal and environmental
matters, commitments, the geographic split, the free-cash-flow reconciliation --
and the repair round extracted 16 more units covering all ten, including the
$5.4bn pension deficit, shareholder litigation running since 2018, and the fact
that non-US revenue ($27.7bn) exceeds US revenue ($18.2bn). None of that was in
the first pass. Corpus coverage still returns `gaps` rather than `represented`,
because the consolidated statements and most note schedules remain unextracted --
and it says so rather than claiming otherwise.

The specification source is the taxonomy spec from the sibling
`statement-classifier` repo, copied in as
[`statement-classifier-specification/runs/spec/00_original_sources/SPECIFICATION.md`](statement-classifier-specification/runs/spec/00_original_sources/SPECIFICATION.md).
It is **not** this repo's `docs/SPECIFICATION.md`, which is a different and
shorter document.

## Each folder is a workspace

Every folder here is a `kip` **workspace** — `runs/<run-id>/` with the pass
directories laid out exactly as the pipeline lays them out, rather than a
flattened copy. The CLI works on them unchanged:

```bash
kip --workspace demo/real-runs/debondt-thaler-does-the-stock-market-overreact show dt units --pretty
kip --workspace demo/real-runs/debondt-thaler-does-the-stock-market-overreact validate dt
kip --workspace demo/real-runs/statement-classifier-specification trace spec <candidate-id>
```

```
debondt-thaler-does-the-stock-market-overreact/
├── enqueue.md         ← reading aid, generated by render.py
└── runs/dt/           ← everything below here is the artifact tree
    ├── 00_original_sources/debondt-thaler-1985-overreact.pdf
    ├── 01_normalized/
    │   ├── source_registry.jsonl
    │   └── src-debondt-thaler-1985-overreact-d07fdf64/
    │       ├── normalized.txt      the text every quote is checked against
    │       ├── manifest.json       digests, normalizer version
    │       └── locator_map.jsonl   character spans → page numbers
    ├── 02_units/{units,omissions}.jsonl
    ├── 03_clusters/{clusters,enriched_units}.jsonl
    ├── 04_assessments/claim_assessments.jsonl
    ├── 05_candidates/candidates.initial.jsonl
    ├── 06_audit/{audits,candidates.approved}.jsonl + corpus_coverage.json
    ├── 07_enqueue/enqueue.jsonl
    ├── _handoff/{pending,responses}.jsonl
    ├── run_manifest.json
    └── stage_fingerprints.json
```

`enqueue.md` is **not a pipeline artifact** — it is written for this repo by
[`render.py`](render.py), entirely from `07_enqueue/enqueue.jsonl`, so it cannot
say more than the handoff itself does. What each artifact under `runs/` is, and
why you would open it, is documented once in the top-level README under
[What a run writes](../../README.md#what-a-run-writes).

`02_units/rejects.jsonl` appears in no run: it is written only when the model
returns a malformed unit, and none did.

## What the runs are for

**They are the pipeline's own regression evidence.** Two coverage failures were
found and fixed against these documents, and the current runs are what shows the
fixes hold.

The specification run is the one that failed hardest. An early version of it
produced 12 units for 12,311 words. A later one produced 93, of which **34
reached no approved candidate — including all fifteen label definitions**. The
cause was not length: a candidate is `title / summary / assertions`, which is the
shape of a *proposition*, and a definition asserts nothing to argue with, so the
planner described the definitions instead of carrying them. It was compounded by
a planning prompt that showed the planner unit IDs without unit text.

Both are fixed, and this run is the proof: **136 units, 0 orphaned**, and all
fifteen definitions arrive in
[`enqueue.md`](statement-classifier-specification/enqueue.md) with their cues and
exclusions intact — applicable without the source, which is the standard a
codebook has to meet.

Pass 5 now closes with a **corpus-coverage audit** that reads the whole
extraction against the whole approved output and answers one question: would a
reader who has only the output know what the corpus contains? Five of the six
runs return `represented` with zero orphans.

The sixth returns **`gaps`** — and it is the more useful result, because it is a
gap that arithmetic could not have found. The Black–Scholes run has zero orphans
too: all 73 units reached an assertion. What it lacks is a definition nobody
extracted. Four of the five Greeks are written in terms of N′(x), the standard
normal *density*, and the output defines only N(x), the cumulative function. A
reader has the shape of gamma, vega and both thetas and cannot evaluate any of
them. Nothing upstream could catch that: no unit was dropped, no citation
failed, and the missing formula asserts nothing to argue with — which is exactly
the profile of content this pipeline is known to lose.
`06_audit/corpus_coverage.json` carries both the mechanical arithmetic and the
judgment, and the two disagree here on purpose.

## What the audit changed

The audit is adversarial by construction — it is told to disprove, narrow or
reject, and its model must differ from the planner's. Across the six runs it
returned `fix` 35 times and `pass_with_label` 67 times, against exactly **one**
bare `pass` in 103 audits. A one-percent clean rate is worth reading skeptically
rather than as a compliment to the planner: an auditor that almost never
approves anything outright is either finding real defects or has a standard no
candidate can meet, and the corrections below are the evidence for the first
reading.

Three kinds of correction recur:

- **Deterministic overclaim.** `independence_inflation` is a code check, not a
  judgment: `knowledge_state 'established' rests on a single independence group`.
  It fired on every entry that called a one-document result established, and each
  was corrected to `authoritative` or `supported`. A corrected entry gets a new
  version beside the original — the audit never overwrites — and its slug is
  regenerated from the corrected title, so a correction cannot be filed under the
  uncorrected name.
- **Coverage the planner lost.** The specification's fine-to-coarse label mapping
  was described rather than carried, and the correction states all fifteen rows.
  The fifteen definitions were carried but their thirty exemplars were not, and
  the correction records that so a consumer knows to go to the source.
- **Content filed in two places.** On the Black–Scholes run the planner put the
  same statement under two leaves — the no-dividend assumption under both the
  model definition and the assumptions, the extension scope under both the
  assumptions and the dividends leaf. Two copies of one claim is one claim that
  can be edited in one place and not the other, and the audit removed the
  duplicate from the leaf that did not own the unit.

## The omission check finds real gaps at every length

`02_units/omissions.jsonl` is Pass 1's self-check: it reads the source against
the units just extracted and reports what is missing or mis-shaped. It found 6,
7, 7, 8, 11 and 13 findings across the six runs — including on the shortest.

On Sharpe it found that three of the four opening quotations — the practitioner
claims the whole paper is written to refute — had reached no unit at all, so a
reader of the output would not know what was being answered. On De
Bondt & Thaler it found the abstract's own summary of the contribution. On the
specification it found the thirty missing exemplars and the eleven unanchored
rows of the mapping table. On Black–Scholes it found the entire Greeks table:
five closed-form sensitivities, the substance of the section, and no unit had
touched them.

Findings marked `add` now feed a **repair round** — one extra extraction call
over the same document, given the findings and the assets. It recovered 18 units
on Black–Scholes, including all five Greeks, and 5 on Sharpe — which is why the
Sharpe run now carries 38 units against the 23 it produced before the round
existed. One round, never a loop: a check-repair cycle has no natural fixed
point and each turn costs a call over the whole document.

Findings the repair round does not act on — `split`, `merge`, `downgrade`,
`drop` — stay diagnostic, because reshaping a sealed unit is a larger change than
extracting content that is missing. Coverage degrades gradually with document
density, not at a cliff with length.

## What the narrative run showed

The non-fiction documents share a property the fairy tale does not: they make
claims. Sharpe argues, De Bondt & Thaler measure, the specification stipulates,
Wikipedia states a model — and a knowledge unit is a natural output for all of
them. A story
asserts nothing about the world, so the question was open: what is a unit here?

The answer, on this document, is that the extractable content is the world's
**stated rules** and the **causal chain** between them. The story specifies an
age threshold, a lifespan, the exact conditions under which a mermaid can obtain
an immortal soul, and a bargain whose price, irreversibility and failure clause
are all disclosed before it is accepted. Those are conditional and quantitative,
so they survive being read cold — a consumer can check the ending against them.
The rest, the moment-to-moment action, does not become units: an entry per event
would be a plot summary in JSONL and none of it stands alone.

That is also why the density is half the others'. It is a property of the source,
not a coverage failure: `units_orphaned` is 0 and corpus coverage returns
`represented`, the same as the rest.

## Non-textual content: tables, formulas, figures

Flattening a source to one text file destroys everything that is not prose, and
the table case was actively dangerous. A filing row arrived as `Total segment
revenue$33,314 $26,881 $23,855` with its headers fused on another line, so the
year-to-column mapping survived only in the model's prose reconstruction. A unit
that read the columns backwards still had a citation that verified `True` --
verbatim checking confirms digits were copied, not that they were assigned to
the right year.

A source is now a **bundle**: the text plus typed assets in
`01_normalized/<src>/assets.jsonl`, each with a stable id. Evidence can cite a
cell with `asset_ref {asset_id, row, col}`, which resolves to the value *and*
the headers governing it.

**Fidelity is part of the record**, because the three kinds are not equally
trustworthy:

| | meaning | citable as |
|---|---|---|
| `exact` | structure from markup the source carried | a quote |
| `transcribed` | a model or geometry read it | a reading, with the crop attached |
| `inferred` | a model described what it could not transcribe | never evidence |

Where the asset comes from decides its fidelity, and the two directions are
opposite on purpose.

**From markup, when the source carries it.** The GE filing yields **100 `exact`
tables** from its own `<table>` elements. The Black–Scholes article yields
**112 `exact` formulas and 7 `exact` tables from one page** — MathML carries the
author's own TeX in `<annotation encoding="application/x-tex">`, so the
Black–Scholes equation is recovered as

```
{\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV=0
```

which is what the author wrote, not a reading of a picture of it. Rendering that
page to transcribe an equation already present in the markup would throw away
the distinction the fidelity field exists to record.

**From a rendering, when it does not.** The De Bondt PDF yields **4 formulas and
Table I as `transcribed`** — its equations had reached the corpus as
`Tt = ARw,t/(st/ViN)`, where `Vi` is a square-root sign, and no better text
extraction recovers that because the information was never in the text layer.
Those pages are rendered and read instead. Image files (`.png`, `.jpg`, …) are
ingestable as sources and take the same path: an image is a page that arrived on
its own.

The Black–Scholes run is the clearest measure of what the asset layer is worth,
because normalization damages that document almost completely. The PDE reaches
`normalized.txt` as

```
∂
V
∂
t
+
1
```

— twenty-nine lines of loose symbols for one equation. **32 of the run's 125
citations are to formula assets and 8 are to table cells**; without them those
40 citations would have had nothing quotable behind them. Citing an equation is checked against the
asset rather than against the flat text, and the comparison ignores spacing and
redundant braces but not bracket placement: `\ln(S/K)+r\tau` and
`\ln(S/K+r\tau)` are different equations and must not compare equal.

Two results from the same run are worth stating plainly. Six of the seven
recovered tables are MediaWiki **navigation boxes** — lists of related articles
marked up as `<table>`. They are `exact` because they really are tables, and
they produced no units, which is correct. And the *seventh* is the Greeks table,
which the first extraction pass skipped entirely: every Greek stated in closed
form, and not one of them reached a unit. The omission check caught it, and the
repair round recovered all five by citing cells — `(row 1, col 2)` is delta for
a call, `(row 1, col 3)` delta for a put, and the grid is what keeps those two
apart.

Citation for a transcription is deliberately looser than the verbatim rule:
string comparison is the wrong check. UniMERNet scores 0.48 exact-match against
0.81 rendered-and-compared, so about a third of *correct* transcriptions differ
textually from the reference. The crop is what makes the claim checkable. See
[`research/2026-08-13-non-textual-content-research.md`](../../research/2026-08-13-non-textual-content-research.md).

## What verbatim citation does and does not guarantee

A citation is checked byte for byte against `normalized.txt`. That guarantees
fidelity to **the source as ingested** — it says nothing about whether the
source is faithful to what was published, and the Sharpe run is a good example
of the difference.

Its source is the author-hosted HTML reprint, which is a lossy transcription of
the Financial Analysts Journal original. Comparing the two: the print footnote 4
reads "they may have to trade with active managers; **at such times, the active
managers may gain from the passive managers,** because of the active managers'
willingness to provide desired liquidity (at a price)", and the HTML silently
deletes the twelve-word clause and splices the sentence back together. Print
"Security analysts … must eat" became "Security analysis"; "such perceptions"
became "such misperceptions"; "a fortiori" was mangled into "a fortior" plus a
stray italic "i".

Two units quote affected passages, and both citations verify — correctly, since
they reproduce the ingested source exactly. The pipeline is doing its job. The
limit is that its job stops at the source boundary, and no amount of internal
checking crosses it.

The practical consequence is that provenance quality is an input decision, not
something the pipeline can repair. Where the original is paywalled and the
available copy is a transcription, that fact belongs in the record rather than
in a footnote to it.

## The retention guard

Units whose statements match a configured taxonomy's surface cues are stamped
`protected_by`, and that flag reaches the planner as `[MUST CARRY]` and the
coverage audit as an escalation. It flagged 19 of 23, 31 of 53 and 124 of 136
units in these runs — deliberately generous, because a false positive costs one
unit carried forward that need not have been, and a false negative costs a
definition nobody can find. It assigns no type and no label; classification runs
separately, after digestion. Point `KIP_TAXONOMY` at your own file to change what
is protected.

## The handoff protocol

`_handoff/pending.jsonl` and `_handoff/responses.jsonl` are the two ends of the
CLI runtime. Each request carries a content-addressed `call_id` over the system
prompt, user message, schema and model, which is what makes a run resumable:
re-running produces byte-identical requests for work already done, so answered
calls are cache hits and only the frontier advances.

```
kip run --sources docs/ --mode handoff   → pending.jsonl, exit 10
(agent answers)                          → re-run, next call, exit 10
                                         → exit 0
```

The content addressing is also what makes an answer un-fakeable: an answer
written against a misremembered prompt produces a different `call_id` and is
simply never read.

## Reproducing

```bash
kip --workspace /tmp/ws run \
    --sources demo/real-runs/sharpe-arithmetic-of-active-management/runs/sharpe/00_original_sources \
    --run-id sharpe --mode handoff
```

Answer each request by appending `{"call_id": "...", "response": {...}}` to
`_handoff/responses.jsonl` and re-running. Copying this run's
`_handoff/responses.jsonl` into the fresh workspace replays the whole run from
cache, because the call ids are identical.
