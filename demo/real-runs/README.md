# Real runs

Four complete runs on real documents, produced by the CLI in `--mode handoff`
with **no API key** — the agent running the CLI answered every model call. These
are the pipeline's actual output, not fixtures.

**Start with `UNITS.md` in any run folder.** Everything else is the machine-
readable material behind it.

## What the files in a run folder are

Read them in this order. The first three are all most readers need.

| file | what it is |
|---|---|
| **`UNITS.md`** | The readable render — every unit, its quotes, and what each one is doing in the argument, then the omission findings. Generated from the `.jsonl` files by `render.py`; nothing is in it that is not in them. |
| **`source.md`** | The document the run digested, exactly as Pass 0 produced it. Every quote is a literal substring of this file, so you can check any of them by searching it. `[[PAGE n]]` markers are inserted by the normalizer. |
| **`units.jsonl`** | **The pipeline's real output.** One JSON record per knowledge unit: the standalone statement, its evidence (each with the verbatim quote, its character and line offsets into `source.md`, and whether the quote was found there), the five scores, the keep/drop decision, and the grounding flag. |
| `omissions.jsonl` | What the omission check found missing or mis-shaped after reading the document *against* the units just extracted from it. One record per finding. This is the pass that audits the extraction, so it is where a run admits its own gaps. |
| `handoff-requests.jsonl` | The exact requests sent to the model: system prompt, user message (which contains the whole document), JSON schema, model name, and a `call_id` that is a hash of all four. |
| `handoff-answers.jsonl` | The answers given back, keyed by the same `call_id`. Together with the requests this makes a run replayable with no model and no API key — see [The handoff protocol](#the-handoff-protocol). |
| `manifest.json` | Pass 0 provenance: sha256 of both the original file and the normalized text, the normalizer version, line count. What lets someone confirm they are looking at the same bytes this run read. |
| `locator_map.jsonl` | Maps character spans in `source.md` back to locations in the original file — page, slide, sheet. How a quote resolves to "page 801 of the journal". |
| `meta.json` | Citation and source word count for the run folder. Read by `render.py`. Not a pipeline artifact. |
| `VERIFY.md` | How to check the run yourself, where a run has one. Not a pipeline artifact. |

**Not every run has every file**, and the differences are meaningful rather than
accidental:

- **Only `01-sharpe-v31` was taken through all seven passes**, so only it carries
  `clusters.jsonl` (Pass 2 groupings), `claim_assessments.jsonl` (Pass 3
  relationship judgments), `candidates.initial.jsonl` (Pass 4 proposals) and
  `audits.jsonl` (Pass 5 verdicts). Runs 02–04 stop after extraction, which is
  the pass under study.
- **`02-sharpe-v41/omissions.jsonl` is empty on purpose** — the omission check
  ran and found nothing missing.
- **Only `04-debondt-thaler` carries `manifest.json`, `locator_map.jsonl`,
  `meta.json` and `VERIFY.md`.** It is the only run whose source is a scanned
  PDF rather than text written for the purpose, so page mapping and provenance
  actually have something to say.

## What each run shows

| run | source | units | density | what it demonstrates |
|---|---|---|---|---|
| `01-sharpe-v31` | Sharpe excerpt, 223 words | 9 | 1 per 25 words | the original **minimality** prompt |
| `02-sharpe-v41` | same 223 words | 7 | 1 per 31 words | **sufficiency + cited imports** |
| `03-spec-long` | the statement-classifier spec, 12,311 words | 12 | **1 per 1,025 words** | **the windowing failure** |
| `04-debondt-thaler` | De Bondt & Thaler (1985), 6,284 words | 35 | 1 per 179 words | a long document that did **not** collapse |

The run-03 source is the taxonomy specification from the sibling
`statement-classifier` repo, copied in as
[`03-spec-long/source.md`](03-spec-long/source.md) — a dense nine-section
technical document. It is **not** this repo's `docs/SPECIFICATION.md`, which is a
different and shorter document.

## 01 → 02: what changed, and why

The first run produced statements that were grammatically standalone and
argumentatively orphaned. This is the same point in both:

> **v3.1** — "Each passive manager obtains precisely the market return, before
> costs."

> **v4.1** — "The market return over any period is the weighted average of the
> returns on every security in the market, weighted by each security's market
> value at the start of the period. Because a passive investor holds the market
> in exactly those proportions, each passive manager earns precisely this return
> before costs."
> *Role in the source: the first premise of the proof, and the step connecting
> the definition of passive holding to a specific return.*

The v3.1 version is true and useless: it does not say that this is the premise
the whole result rests on. The prompt's fault, not the model's — it asked for
**minimality**, "the LEAST information required", which is an explicit
instruction to strip exactly the context that makes a point a point.

v4.0 replaced minimality with **sufficiency**: a unit must stand alone as an
*insight*, such that a reader who never saw the document could answer a
comprehension question about it, follow its reasoning, or apply its formula.

v4.1 added the constraint that keeps sufficiency honest: **importing context
licenses nothing unless the import is cited**. Evidence now carries a `role`:

- `primary` — the passage the unit is principally about
- `supporting` — a passage elsewhere in the document licensing something the
  unit imported

Unit count went *down*, 9 → 7, because two pairs merged: the two definitions
became one unit (neither is usable without the other), and the weighted-average
definition merged with its passive-manager consequence. Sufficiency does not
mean longer chunks — it moves where the cuts fall, and small pieces of an
argument are rubble.

Applying the citation rule also deleted a claim. v4.0 said of unit 1 that "it is
not a claim that active managers lack skill" — true, standard, and **not in the
excerpt**. Under v4.1 it had to be quoted or removed. That is the rule working
on its own author.

## 03: where it breaks

Same extractor, same prompt, same rules, on a 12,311-word document:

```
Sharpe excerpt      223 words →  9 units   (1 per 25 words)
classifier spec  12,311 words → 12 units   (1 per 1,025 words)
```

**A 41× collapse in density.** `extract` sends the whole document in one call —
87,000 characters, ~24,000 tokens here — and **there is no windowing anywhere in
the pipeline**. The `context_reservation` knob in `config.py` is never read.

It is not that the model gets lazy. One pass over 12,000 words with an
instruction to "return as many units as the source warrants" produces a
*summary-shaped* answer, because nothing forces it to work through the document
section by section.

The omission check caught this in its own run, and its findings are in
`03-spec-long/UNITS.md`: fifteen label definitions, twenty-two pairwise rules,
three field vocabularies, a whole section on conversational statements and the
entire evidence register — all unrepresented, and all exactly the kind of
durable content a knowledge base exists to hold.

**Everything else held at 12k words.** Every citation verified against the
source, all twelve units `attributable`, median 45 words. The quality machinery
works; the coverage does not.

## 04: length alone is not what breaks it

Run 04 digests De Bondt & Thaler's 1985 *Does the Stock Market Overreact?* —
6,284 words of argument rather than a reference document — and produced 35 units
at one per 179 words, with `kip validate` clean: no errors, no warnings, all 82
excerpts verified, all 35 units `attributable`.

```
Sharpe excerpt      223 words →  7 units   (1 per    32 words)
De Bondt & Thaler 6,284 words → 35 units   (1 per   179 words)
classifier spec  12,311 words → 12 units   (1 per 1,025 words)
```

So a document five times longer than the Sharpe excerpt did not collapse. Two
things confound reading this as proof that coverage is fine:

**The agent answering the call knew what was being tested.** These runs are
answered by the agent operating the CLI, and this one was made while
investigating the density question. Treat one-per-179 as an existence proof —
6,000 words *can* yield 35 verified standalone units in a single call — not as a
measurement of unprompted model behaviour. The clean version of the test runs
this document through `--mode sdk`.

**The omission check still found eight gaps**, concentrated in the statistical
apparatus of Section I.A and in the footnotes, which is where the competing
explanations and the caveats live. It also caught that Table I's strongest row —
the five-year experiment, reversing 0.319 at 60 months with t = 3.28 — is
stronger than the three-year result the extraction treated as the headline. So
coverage degrades gradually with length rather than falling off a cliff, and it
is already imperfect at 6,000 words.

The source document is not in the repo; see
[`04-debondt-thaler/meta.json`](04-debondt-thaler/meta.json).

## What run 04 exposed in `normalize`

Three of the extraction's quotes failed verbatim verification on the first
attempt, and the cause is in Pass 0 rather than in the model:

1. **Words split across a line break are never rejoined.** The text contains
   `evi- dence`, `follow- ing`, `com- panies`, `predict- able`. The word
   `evidence` does not occur in `normalized.txt` at all. A model quoting
   faithfully writes "evidence", the exact-match check fails, and the excerpt is
   silently marked unverified — which then degrades the unit's grounding. This
   fires on every page, not only at page boundaries.
2. **Running heads are kept as body text.** `Does the Stock Market Overreact? 801`
   and `794 The Journal of Finance` appear twelve times as if they were prose,
   in the middle of sentences that span a page. `docs/SPECIFICATION.md` §8
   already requires "deterministic-and-logged header/footer stripping only"; it
   was specified and never implemented.
3. `[[PAGE n]]` markers themselves are **correct** and should stay — they are how
   an excerpt resolves back to a page in the original.

## The handoff protocol

`handoff-requests.jsonl` and `handoff-answers.jsonl` are the two ends of the
CLI runtime. Each request carries a content-addressed `call_id` over the system
prompt, user message, schema and model, which is what makes a run resumable:
re-running produces byte-identical requests for work already done, so answered
calls are cache hits and only the frontier advances.

```
kip run --sources docs/ --mode handoff   → pending.jsonl, exit 10
(agent answers)                          → re-run, next call, exit 10
                                         → exit 0
```

`01-sharpe-v31` is the only run taken through all seven passes; its
`claim_assessments.jsonl`, `candidates.initial.jsonl` and `audits.jsonl` show
the relationship judgment, the planning step and the adversarial audit. Two
things there are worth reading:

- The relationship pass marked the four units behind Sharpe's identity as
  `convergent_dependent` — one deductive chain, not four independent
  confirmations — and marked the before-costs and after-costs claims as
  `scope_difference` rather than a contradiction.
- The audit returned **fix**, and a *deterministic* check caught the planner's
  overclaim independently of the LLM auditor:
  `independence_inflation: fail — knowledge_state 'established' rests on a
  single independence group`.

## Reproducing

```bash
kip --workspace /tmp/ws run --sources demo/real-runs/02-sharpe-v41 \
    --run-id sharpe --mode handoff --show-request
```

Answer each request by appending `{"call_id": "...", "response": {...}}` to
`_handoff/responses.jsonl` and re-running. The answers in
`handoff-answers.jsonl` are valid for the same call ids, so copying that file
into a fresh run's `_handoff/` replays these results exactly.
