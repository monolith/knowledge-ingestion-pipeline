# Knowledge Ingestion Pipeline

Turns a folder of heterogeneous documents — PDFs, Word files, slide decks,
emails, HTML, notes — into audited knowledge-base entries where every claim can
be traced back to the exact sentence it came from.

It **digests** documents: it breaks them into standalone chunks and works out
how those chunks relate to each other. It does not label them. Deciding what
kind of thing a chunk is happens afterwards, in a separate classifier that reads
the finished statement — see [How digestion works](#how-digestion-works).

Built from [specification v3.0](docs/SPECIFICATION.md), whose design decisions
are backed by [adversarially-verified research](research/) rather than
convention.

## The problem it solves

Feeding documents to a model and asking "what do these say?" produces confident
prose you cannot check. This pipeline is the opposite bet: it keeps every
intermediate step as machine-readable JSONL, cites the exact character offsets
of every quote, and puts an adversarial audit between the model's proposals and
your knowledge base.

Concretely, it is designed to catch the failure that matters most — a candidate
entry that says *"sleep extension improves memory: established"* when one trial
was positive and a larger independent replication was null. The audit rewrites
that to *"mixed evidence: contested"* and keeps the original on disk beside it.

## Install

```bash
pip install -e ".[parse-lite,dev]"
export ANTHROPIC_API_KEY=sk-ant-...
```

- `parse-lite` — PDF/DOCX/PPTX/XLSX support, a few MB
- `parse` — Docling instead: bounding-box provenance, multi-GB ML stack
- neither — plain text, Markdown, HTML and email still work

## Use

```bash
kip --workspace .kip run --sources ./documents           # full run
kip --workspace .kip run --sources ./docs --stop-after extract   # inspect first
kip --workspace .kip validate <run-id>                   # integrity check
kip --workspace .kip trace <run-id> <candidate-id>       # full provenance chain
kip --workspace .kip show <run-id> audits --pretty       # what the audit changed
```

Runs resume: a completed pass is reused rather than recomputed, so an
interrupted or extended run never repeats the expensive extraction step.

Two runtimes serve the model calls. `--mode sdk` (the default) calls the
Anthropic API and needs a credential. `--mode handoff` needs neither: it writes
each request to `_handoff/pending.jsonl` and exits 10, so an agent already
running the CLI can answer it and re-run. Completed stages resume from their
checkpoints and answered calls are cache hits, so each re-run advances exactly
one call. Every example under [`demo/real-runs/`](demo/real-runs/) was produced
that way, on a host with no API key.

## Demo — no API key needed

```bash
python demo/run_demo.py                    # scripted client, temp workspace
python demo/run_demo.py --workspace .kip   # keep the artifact tree somewhere
python demo/run_demo.py --live             # same code path, real API (costs money)
```

Ingests the two documents in [`demo/sources/`](demo/sources/) — a randomized
trial and a practitioner review that disagree about the same effect — through
all seven passes, then prints the extracted units, the entity mentions that
reached the enriched units, what the audit changed, and the validation report.
The artifact tree it writes is real: `kip show` and `kip trace` work on it.

Every model call is served by a canned transcript, so the run is free,
deterministic, and offline. The test suite executes it.

For output from a **real** model rather than a canned one, read
[`demo/real-runs/`](demo/real-runs/README.md) — three complete runs on real
documents, including the one that fails.

## As a Claude Code plugin

The repo is a plugin. Install it, then use `/kip-ingest <folder>` and
`/kip-trace <run-id> <id>`, or just describe the task — the
`knowledge-ingestion` skill activates on requests like *"do these documents
contradict each other"*.

## How digestion works

Digestion is one job stated two ways: **break the document into chunks that
stand on their own, and work out how those chunks relate.** Everything below
serves one or the other.

### 1. A chunk is a point, not a sentence

The unit of output is a **knowledge unit** — one point from the document,
written so it survives being read cold by somebody who never saw the source.

That is a higher bar than "grammatically complete", and the gap between the two
is the whole design. Both of these came out of the same 223 words of Sharpe's
arithmetic of active management:

> **Not a unit** — "Each passive manager obtains precisely the market return,
> before costs."

> **A unit** — "The market return over any period is the weighted average of the
> returns on every security in the market, weighted by each security's market
> value at the start of the period. Because a passive investor holds the market
> in exactly those proportions, each passive manager earns precisely this return
> before costs."

The first is true and useless: nothing in it says this is the premise the whole
result rests on. The second can be read, argued with, and cited without the
paper in hand.

The standard, stated as a test: a reader holding only this unit should be able
to answer a comprehension question about it, follow its reasoning if it is an
argument, or apply it if it is a formula.

### 2. The cuts fall where a point closes

There is no chunk size — no word count, no token budget, no target number of
units per document. A document yields as many units as it has points.

Two sentences that only mean something together are one unit. One sentence
carrying two claims that could be independently true is two. Because a fragment
of an argument is rubble rather than a smaller unit, the rule for splitting is
deliberately narrow: split only when the parts are **both** independently
evaluable and independently interpretable — different truth value, actor,
population, time horizon, modality, scope, or exception.

Changing the prompt from "add the least information required" to "the unit must
stand alone as an insight" moved that 223-word excerpt from nine units to seven,
the median unit from 22 words to 46, and citations from 1.0 per unit to 2.3.
The unit count went **down**: two pairs merged, because neither half was usable
alone. Standing alone is not a length target — it moves where the cuts fall.
Both runs are in [`demo/real-runs/`](demo/real-runs/README.md).

### 3. The whole document is in view while the cuts are made

A point in section 9 often rests on a definition in section 2. A model cannot
build that point out of a passage it never saw, so extraction is not handed a
pre-sliced document: the full text is in view while the units are cut from it.

Slicing the *input* would leave the model two bad options on every
cross-referencing unit — drop the context and emit a thin chunk, or assert the
context from memory and cite nothing. Both are exactly what the next rule exists
to prevent.

This is a rule about *what the model can see*, not a claim that documents are
never cut. A document too large to hold at once has to be cut somewhere; the
constraint here says where — at a boundary self-contained enough that nothing
inside it rests on anything outside. That case is
[not built yet](#not-built-yet-documents-too-long-to-hold-at-once).

### 4. Every claim in a unit has to be quotable

Each unit carries evidence in one of two roles:

- **primary** — the passage the unit is principally about. Exactly one.
- **supporting** — a passage elsewhere in the document licensing something the
  unit imported: a definition it relies on, a condition it is scoped to, a
  consequence it names.

Standing alone licenses *importing* context. It does not license *asserting* it
uncited. If the statement says something the primary passage does not, the
passage that does say it gets quoted too.

Verification is code, not judgment: each excerpt is located in the source by
exact string match and its true character offsets recorded, so a paraphrased
"quote" fails at extraction time, where it is cheapest to catch. The standard is
a citation in a thesis — a reader who disagrees with a unit must be able to open
the document, find every claim it makes, and argue with the source rather than
with us.

### 5. Each unit says whether the document alone could have produced it

Models know things the document does not say, and on a famous document that
outside knowledge is hardest to spot: the prior is strongest exactly where the
answer looks most authoritative. So each unit answers a counterfactual it can
actually answer — **if this document were the only thing you had ever read,
could you have written this unit?**

- `attributable` — yes; every claim traces to a cited excerpt.
- `conventions_added` — the claims are supported, but standard terminology the
  document assumes was supplied (an acronym expanded, a well-known measure
  named).
- `unattributed_content` — no; the unit carries substance no excerpt supports.

The answer is checked, not trusted. `kip validate` errors on a unit claiming
`attributable` while resting on an excerpt that failed verification, warns when a
unit records imported context but cites no supporting excerpt, and counts
unattributed units as a health metric rather than failing the run.

### 6. Then: how the chunks relate

Chunks alone are a pile. The rest of the pipeline turns them into a structure.

```
files ─▶ 0 normalize ─▶ 1 extract ─▶ 2 route ─▶ 3 assess ─▶ 4 plan ─▶ 5 audit ─▶ 6 enqueue
         (code)          (LLM)        (LLM+code)  (code+LLM)  (LLM)    (code+LLM)  (code)
```

- **0 normalize** turns any input format into plain text plus a locator map back
  into the original — page, slide, sheet. Deterministic; no model involved.
- **1 extract** is everything above, plus a second call that reads the document
  against the units already pulled from it and reports what is missing or
  mis-shaped.
- **2 route** writes a short retrieval context for each unit and groups units
  into comparison sets — *without* deciding whether they agree.
- **3 assess** judges relationships between *presented pairs*, never an
  open-ended "does this pile contradict itself".
- **4 plan** proposes knowledge-base operations. It never writes to the wiki.
- **5 audit** attacks those proposals: deterministic checks in code first, then a
  reasoning-class model that must be different from the one that proposed.
- **6 enqueue** emits idempotent events for the leaf engine, which remains the
  sole authority for durable writes.

Artifacts land under `runs/<run-id>/`, one JSONL file per pass, each record
carrying a content hash and pointers to its parents. They are listed in full
under [What a run writes](#what-a-run-writes) below, and four real runs you can
open are in [`demo/real-runs/`](demo/real-runs/README.md).

### Not built yet: documents too long to hold at once

Everything above assumes the document fits in one call. Measured on the same
extractor and the same prompt:

```
Sharpe excerpt      223 words →  7 units   (1 per    31 words)
De Bondt & Thaler 6,284 words → 35 units   (1 per   179 words)
classifier spec  12,311 words → 12 units   (1 per 1,025 words)
```

Length alone is not the variable. [De Bondt &
Thaler (1985)](demo/real-runs/04-debondt-thaler/UNITS.md) is five times longer
than the Sharpe excerpt and held up: 35 units, `kip validate` clean, all 82
excerpts verified. The [classifier
specification](demo/real-runs/03-spec-long/runs/spec/00_original_sources/SPECIFICATION.md) is a dense reference
document — fifteen label definitions, twenty-two pairwise rules, an evidence
register — and it is the one that collapsed. Some of the 32× gap is document
shape rather than extractor failure.

Everything except coverage held at 12,000 words: all fourteen citations verified
against the source, all twelve units `attributable`, statements the same length
as in the short run. And the omission check diagnosed its own run — fifteen
label definitions, twenty-two pairwise rules, three field vocabularies and an
entire section, none of them represented. The quality machinery works; the
coverage does not. See
[`demo/real-runs/03-spec-long/`](demo/real-runs/03-spec-long/).

Two separate limits are tangled in that number and neither is addressed.
`max_tokens` on the shared model-call seam is 8,192 — about 28 units at the
observed cost per unit — so a dense document's answer has nowhere to go. And a
document large enough to strain the context window has to be cut regardless of
the output budget, at boundaries where a section is self-contained enough that
nothing it rests on falls outside the cut.

Coverage is imperfect before either limit binds: at 6,284 words the omission
check still found eight gaps, concentrated in the statistical apparatus and the
footnotes. It degrades gradually with length rather than at a cliff.

### Not built yet: line-break repair in `normalize`

Run 04 exposed two Pass 0 defects that corrupt verbatim quoting of any paginated
PDF. Words split across a line break are never rejoined — the document holds
`evi- dence` and `follow- ing`, so a faithful quote fails the exact-match check
and the excerpt is silently marked unverified. And running heads are kept as
body text, landing mid-sentence wherever a sentence spans a page. §8 of the
specification already requires header/footer stripping. Details in
[`demo/real-runs/`](demo/real-runs/README.md).

## What a run writes

Everything a run produces lives under `<workspace>/runs/<run-id>/`. Nothing is
hidden in a database; every file below is plain text you can open, diff, and
grep.

```
runs/<run-id>/
├── 00_original_sources/          the input files, copied and never modified
├── 01_normalized/
│   ├── source_registry.jsonl     one record per source: id, hashes, status
│   └── <source-id>/
│       ├── normalized.txt        the full text everything downstream reads
│       ├── manifest.json         per-source provenance and digests
│       └── locator_map.jsonl     character spans → page / slide / sheet
├── 02_units/
│   ├── units.jsonl               THE KNOWLEDGE UNITS — the primary output
│   ├── omissions.jsonl           what the omission check found missing
│   └── rejects.jsonl             malformed answers, recorded not raised
├── 03_clusters/
│   ├── enriched_units.jsonl      units plus a retrieval context, for indexing
│   └── clusters.jsonl            comparison sets, with no verdict attached
├── 04_assessments/
│   └── claim_assessments.jsonl   relationship judgments on presented pairs
├── 05_candidates/
│   └── candidates.initial.jsonl  proposed knowledge-base operations
├── 06_audit/
│   ├── audits.jsonl              every verdict, including the rejections
│   ├── candidates.approved.jsonl what survived the audit
│   └── corpus_coverage.json      did the output keep what was extracted?
├── 07_enqueue/
│   └── enqueue.jsonl             idempotent events for the leaf engine
├── run_manifest.json             config in force + summary counts
├── stage_fingerprints.json       what each stage consumed, for resume
└── _handoff/                     `--mode handoff` only
    ├── pending.jsonl             the request the run is waiting on
    └── responses.jsonl           answers, keyed by content-addressed call id
```

**The directory numbers are one ahead of the pass numbers.** Pass 0 (normalize)
writes `01_normalized/`, Pass 1 (extract) writes `02_units/`, and so on to Pass 6
writing `07_enqueue/`. `00_original_sources/` holds inputs rather than output,
which is where the offset comes from.

| artifact | written by | what it is |
|---|---|---|
| `00_original_sources/` | code | Byte-for-byte copies of the input files. Immutable: everything downstream refers back here by hash, never re-reads the user's originals. |
| `source_registry.jsonl` | code | One record per discovered source — `source_id`, original and normalized sha256, media type, and `normalization_status`. A source that failed to parse is **quarantined here rather than dropped**, so it shows up in coverage counts instead of vanishing. |
| `normalized.txt` | code | The plain-text form of one source, with `[[PAGE n]]` / `[[SLIDE n]]` / `[[SHEET name]]` markers. **This is what every quote is checked against**, so it is the file to open when an excerpt is disputed. |
| `manifest.json` | code | Per-source provenance: both digests, normalizer name and version, line count, language, warnings. What proves two runs read the same bytes. |
| `locator_map.jsonl` | code | Maps character spans in `normalized.txt` back to a location in the original — page, slide, sheet. How an excerpt resolves to "page 801". |
| **`units.jsonl`** | **LLM** | **The primary output.** One record per knowledge unit: the standalone statement, evidence (verbatim quote, char and line offsets, `excerpt_verified`, `primary`/`supporting` role), the five scores, keep/drop/review, `grounding`, `context_note`, entity mentions, and a `content_sha256` over the assertion. |
| `omissions.jsonl` | LLM | One record per completeness finding: kind, description, the excerpt it concerns, and a suggested action. This is where a run records its own gaps. |
| `rejects.jsonl` | code | Units the model returned malformed — a truncated answer, a missing required field. Recorded with the reason instead of raising, so one bad record cannot discard a corpus. Absent when there were none. |
| `enriched_units.jsonl` | LLM | Each unit plus a short retrieval context for indexing. **Index-time only** — it never replaces `canonical_statement` and never leaks into evidence. |
| `clusters.jsonl` | LLM + code | Units grouped into comparison sets, deliberately with **no** judgment about whether members agree. Deciding that is Pass 3's job on specific pairs. |
| `claim_assessments.jsonl` | code + LLM | Relationship judgments over pairs the code selected, each with a coarse stance, an optional finer subtype, and both orderings of the pair. |
| `candidates.initial.jsonl` | LLM | Proposed knowledge-base operations — create, update, merge, split, link, defer — with a knowledge state and the assessment ids each assertion rests on. Proposals only; nothing is written to the wiki. |
| `audits.jsonl` | code + LLM | Every audit verdict, rejections included. A `fix`, `merge` or `split` never edits the proposal in place — it emits a **new candidate version**, so the original stays on disk beside it and a rewrite remains followable. |
| `candidates.approved.jsonl` | code | The subset that survived. Only these reach Pass 6. |
| `corpus_coverage.json` | code + LLM | The one judgment made over the **whole** run rather than one candidate. Counts how many kept units reached an approved candidate and how many were orphaned, then asks a reasoning-class model whether the key insights and definitions survived and whether the corpus is fairly represented. Every other check validates a record against its parent; this is the only one that validates a parent against its children. |
| `enqueue.jsonl` | code | Idempotent events for the downstream leaf engine, which remains the sole authority for durable writes. Re-running produces the same events rather than duplicates. |
| `run_manifest.json` | code | The evidence-tier configuration in force — models per role, whether the auditor differed from the proposer, batch sizing, datamarking — plus summary counts. Recorded because all of it changes the output's error rate. |
| `stage_fingerprints.json` | code | A digest of what each stage consumed. Resuming a run whose inputs moved is **refused** with the changed stage named, rather than silently producing a half-old corpus. |
| `_handoff/pending.jsonl` | code | The request the run is currently blocked on, in `--mode handoff`. |
| `_handoff/responses.jsonl` | you | Answers keyed by a `call_id` that hashes the system prompt, user message, schema and model — which is what makes a run resumable and replayable. |

Two files are transient: `units.partial.jsonl` and `omissions.partial.jsonl` are
written after each document so a failure on document nine of ten does not
discard the first eight, and are removed when the pass completes. Seeing them in
a finished run means the run did not finish.

> **The folders in [`demo/real-runs/`](demo/real-runs/README.md) do not look like
> this.** They are flat, hand-picked copies of run trees, with some files renamed
> — `02_units/units.jsonl` appears there as `units.jsonl`, and
> `01_normalized/<source-id>/normalized.txt` as `source.md`. That folder's README
> carries the full mapping. The tree above is what `kip` actually writes.

`kip show <run-id> <artifact>` prints eight of them by short name — `units`,
`omissions`, `clusters`, `assessments`, `candidates`, `audits`, `approved`,
`enqueue`. The rest are read directly from disk. `kip trace <run-id> <id>` walks
the chain from a candidate back to the sentence it came from, and
`kip validate <run-id>` checks the whole tree for the integrity failures the
design leans on.

## Design decisions worth knowing

These are the places the research overturned the obvious choice:

**Chunks are molecular, not maximally atomic.** Splitting claims into the
smallest possible pieces is the intuitive move and it is wrong here — fully
atomic facts lose the context needed to interpret them, and decomposition
measurably *hurts* accuracy when strong models do the downstream work, which is
exactly this setup. That evidence is what section 2 above implements.

**Never ask "does this pile contradict itself?"** Open-ended contradiction
detection runs near chance even for frontier models. Ask about a specific
retrieved pair and the same model succeeds ~77% of the time. Pass 3 therefore
matches candidates in code before any judgment happens.

**The auditor must be a different, reasoning-class model.** Non-reasoning judges
score near chance on hard correctness calls. And self-preference bias survives
anonymization — a model shown its own work favors it even when it doesn't know
it's its own. The pipeline refuses to run if planner and auditor match.

**Mechanical checks beat model judgment wherever the question has an exact
answer.** Citation accuracy, provenance resolution, and independence arithmetic
run as code with no error rate, instead of as LLM judgment with about one-in-five
error on hard cases.

**A retention guard, which is not typing coming back.** Synthesis is a
proposition-shaped step: a candidate is title, summary and assertions, which is
the shape of a *claim*. A definition asserts nothing to argue with, so a planner
describes it — "the codebook defines fifteen labels" — instead of carrying it
across, and the content a reader actually needs never arrives. Measured on a
12,311-word specification: 93 units extracted, 34 reaching no approved
candidate, all fifteen definitions among them. `src/kip/retention.py` flags
units whose statements match a configured taxonomy's surface cues, and that flag
travels to the planner as `[MUST CARRY]` and to the coverage audit as an
escalation. It assigns no type and no label — it answers only "would losing this
be the failure we already measured?" The cues are deliberately loose, because
classification runs separately after digestion and a false positive costs one
unit carried forward that need not have been. Point `KIP_TAXONOMY` at your own
file to change what is protected.

**Typing is not digestion's job, and used to be.** Every unit once carried a
type — case, rule, method, concept, model, claim — produced in pass 1 and read
as decoration everywhere downstream. Nothing branched on it, which is what made
it safe to remove. Deciding what kind of thing a statement is belongs to a
classifier that reads the finished statement, and it is also needed for text
that never goes through this pipeline at all. `src/kip/vocab.py` holds what was
never a classification — modalities, flags, node kinds, grounding — and its
docstring says the package must not grow typing back.

**A derived label never touches content identity.** A unit's content hash covers
the assertion — statement, evidence, source lineage — and deliberately excludes
anything derived from it. An earlier version hashed the type along with
everything else, so re-labelling a corpus forged new hashes and the integrity
check rejected it. Re-labelling is free; overwriting is still forbidden.

**Injection can't be eliminated, so the architecture absorbs it.** No LLM pass
has tool access and all output is schema-constrained, which means an injected
instruction can at worst corrupt a field value — never take an action.
Untrusted text is datamarked, the single highest-payoff defense measured.

Each of these cites its evidence inline in the [specification](docs/SPECIFICATION.md).

## Tests

```bash
pytest -q          # or: PYTHONPATH=src python -m pytest tests/ -q
```

180 cases from 149 test functions (the difference is parametrization), no API
key and no network needed. They cover the deterministic half directly —
normalization (including PDF, DOCX, PPTX, XLSX and multipart email, each built
in the test), the CCITT decoder for scanned PDFs, locator maps, hashing,
citation verification, grounding checks, independence arithmetic, idempotent
enqueueing, resume, and the handoff runtime's call identity — and the LLM passes
through a scripted fake client that verifies wiring.

The integration tests drive the real orchestrator, not a copy of the pass
sequence, over three documents: `--stop-after`, resume, and the run manifest are
all asserted on, so a pass cannot be removed without the suite noticing. The
fake client validates every canned response against the schema its pass
declared, which is what makes schema drift — the whole contract with the live
model — visible offline.

The safety machinery has its own tests because it is what the design leans on:
each of `kip validate`'s error branches is exercised by corrupting exactly one
field; the audit's distinct-auditor guard, mechanical-failure escalation, and
reject/defer refusal each have a case; a candidate with no provenance is proved
unqueueable; and a source added mid-run is proved to stop the resume rather than
to vanish from it. The demo runs as a test too.

## Status

Initial implementation. Passes 0 and 6 and all deterministic checks are verified
end-to-end on real files. Passes 1–5 have now been driven by a real model through
the handoff runtime rather than a script — output in
[`demo/real-runs/`](demo/real-runs/README.md) — but only on short documents, and
the SDK runtime has not been exercised against the live API.

**The known gap is coverage on long documents**, described under
[Not built yet](#not-built-yet-documents-too-long-to-hold-at-once): quality holds
at 12,000 words and completeness does not.

The classifier that was supposed to consume these units does not exist. Typing
was removed from this pipeline deliberately; nothing downstream replaces it yet,
so digestion currently produces untyped units with nowhere to send them for
labelling.

Open questions the research left unresolved — including whether the fine-grained
relationship vocabulary is reliable enough to trust — are listed in
[specification §23](docs/SPECIFICATION.md#23-open-questions). Note that the
specification still describes the classification layer this pipeline no longer
implements.
