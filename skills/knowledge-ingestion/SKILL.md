---
name: knowledge-ingestion
description: Use when ingesting documents into a knowledge base — extracting source-backed knowledge units from PDFs, Word docs, slide decks, emails, HTML, images or notes; recovering tables, formulas and charts as citable assets rather than flattened text; comparing claims across documents to find agreement and contradiction; auditing proposed knowledge-base entries against their sources; or tracing a knowledge-base claim back to the exact text or table cell it came from. Triggers on "ingest these documents", "extract knowledge from", "what do these sources say about", "do these documents contradict each other", "where did this claim come from".
---

# Knowledge Ingestion Pipeline

Turns a folder of heterogeneous documents into audited, fully traceable
knowledge-base entries. Implements specification v3.0
(`${CLAUDE_PLUGIN_ROOT}/docs/SPECIFICATION.md`), whose design decisions are
backed by adversarially-verified research in `${CLAUDE_PLUGIN_ROOT}/research/`.

## What it does

Seven passes, each writing an append-only JSONL artifact:

| Pass | Does | Mode |
|---|---|---|
| 0 normalize | files → plain text + locator map + **typed assets** | code |
| 1 extract | text → molecular, source-backed knowledge units; reads rendered pages; links assets to text | LLM + code |
| 2 route | contextual enrichment, then hybrid BM25 clustering | LLM + code |
| 3 assess | match candidate pairs, then judge relationships | code + LLM |
| 4 candidates | assessments → proposed KB operations | LLM |
| 5 audit | adversarial audit; deterministic + reasoning checks; corpus coverage | code + LLM |
| 6 enqueue | idempotent queue events for the KB engine | code |

Nothing reaches a knowledge base without passing Pass 5.

## Setup

```bash
pip install -e "${CLAUDE_PLUGIN_ROOT}[parse-lite,parse-pdf]"
export ANTHROPIC_API_KEY=sk-ant-...
```

Two extras, and you want both for anything but plain text:

- `parse-lite` — text out of PDF/DOCX/PPTX/XLSX (a few MB).
- `parse-pdf` — `pypdfium2` to render a page and `pdfplumber` to read tables the
  PDF draws with ruling lines. **Formula and chart capture from PDFs need this**;
  without it those pages are skipped, and the run says so rather than going
  quiet.

`[parse]` adds Docling instead, which gives bounding-box provenance but pulls a
multi-GB ML stack. Pass 2's BM25 needs no package — it is implemented in
`route.py`.

Credentials resolve in three tiers: `ANTHROPIC_API_KEY`, then a Claude Code
OAuth token, then Bedrock/Vertex settings. A 401 mid-run re-reads the token from
disk once before failing, because Claude Code refreshes in place.

The auditor model **must differ** from the planner model — the pipeline refuses
to run otherwise, because self-preference bias survives anonymization. Override
with `KIP_MODEL_AUDITOR` / `KIP_MODEL_PLANNER` if needed.

## Running it

```bash
# Full run
kip --workspace .kip run --sources ./documents

# Stop early to inspect before paying for later passes
kip --workspace .kip run --sources ./documents --stop-after extract

# Resume: completed passes are reused, only the missing ones run
kip --workspace .kip run --sources ./documents --run-id run-20260801-120000
```

Cost control matters here: Pass 1 is the expensive pass and everything
downstream depends on it. Use `--stop-after extract`, inspect the units, then
continue — a resumed run does not repeat completed passes.

### Running with no API key: handoff mode

```bash
kip --workspace .kip run --sources ./documents --mode handoff
```

In handoff mode the pipeline makes no network calls. It writes each model
request to `_handoff/pending.jsonl` and exits 10; **you** answer it by appending
one line to `_handoff/responses.jsonl`, then re-run the same command. Completed
passes resume; the pipeline blocks on the next unanswered call.

```json
{"call_id": "da905b168331296c", "response": {...}}
```

This is how every run in `${CLAUDE_PLUGIN_ROOT}/demo/real-runs/` was produced —
an agent answering its own pipeline's calls, one at a time. Two properties make
it worth knowing about:

- **A `call_id` is content-addressed** over (system, user, schema, model, images).
  Copying a `responses.jsonl` into a fresh workspace replays the entire run from
  cache, and changing a prompt invalidates exactly the calls it changed.
- **An answer is schema-checked on the way in.** The SDK runtime gets schema
  enforcement from the API; a hand-written answer has nothing, so an answer of
  the wrong shape would sail through and fail two passes later, far from its
  cause. It is also size-checked against the declared `max_tokens`, because
  nothing stops a hand-written answer exceeding what the API would have emitted.

## Non-textual content: assets

Flattening a source to one text file destroys everything that is not prose, and
the table case is actively dangerous. A filing row arrives as
`Total segment revenue$33,314 $26,881 $23,855` with its headers fused onto
another line — so a unit that read the columns backwards still has a citation
that verifies `True`. Verbatim checking confirms the digits were copied. It
cannot confirm they were assigned to the right year.

So a source is a **bundle**: the flat text, plus typed assets in
`01_normalized/<source>/assets.jsonl`.

| kind | recovered from |
|---|---|
| `table` | HTML `<table>`; a Markdown pipe table; PDF ruling lines; a rendered page read by a model |
| `formula` | MathML `<annotation encoding="application/x-tex">`; Markdown `$$…$$` or a ```math fence; a rendered page |
| `figure` | HTML `<img>`; a PDF page carrying a `Figure N.` caption; an image file given as a source |

Markdown is worth calling out because it is the format most documents arrive in
that nobody thinks of as a format. A pipe table's columns are delimited by the
author, so the grid is `exact` — the same standing as HTML. Inline `$…$` is
deliberately NOT read as mathematics: a lone `$` is a dollar sign far more often
than it is an equation, and a memo pricing something in $/kWh would produce
nonsense.

**Fidelity is part of the record**, because the kinds are not equally
trustworthy and a consumer must not compare them the same way:

- `exact` — structure recovered from markup the source itself carried. Citable
  as a quote is; comparable as a string.
- `transcribed` — a model or geometry read it. A READING, not a quote. String
  comparison is the wrong check: UniMERNet scores 0.48 exact-match against 0.81
  when rendered and compared visually, so about a third of *correct*
  transcriptions differ textually from the reference.
- `inferred` — a model described what it could not transcribe. Never evidence,
  and deliberately unused: nothing in this pipeline describes a chart.

Every asset carries its **caption** and **heading** where the source has them. A
chart without its caption is an image nobody can interpret; a table titled only
`2025` is a grid nobody can identify.

A `transcribed` asset also carries `verification`: what fraction of its numbers
appear in that page's raw text layer. Digits usually survive a damaged scan even
when structure does not, so this corroborates a reading cheaply. It gates
nothing — a low ratio is a reason to open the retained page image.

### Citing an asset

Evidence can cite an asset instead of a text span:

```json
{"excerpt": "$8,698", "asset_ref": {"asset_id": "tbl-...-0028", "row": 2, "col": 1}}
```

A cell reference resolves to the value **and the headers governing it** —
`2025` × `Net income (loss)` — which is what makes a figure checkable rather
than merely quoted. A formula is cited by `{asset_id}` alone and its excerpt is
the LaTeX, checked against the asset because normalization is what destroyed the
equation in the first place.

### Assets travel with their text

An asset does not have to be cited to survive. Each one **anchors** to a
character range in `normalized.txt`, and every unit whose evidence overlaps that
range is related to it. `02_units/asset_links.jsonl` records one row per
relationship, marked `cited` or `same_region`; the same ids appear on each unit
as `related_asset_ids` and on each queue event as `payload.related_asset_ids`.

**If a unit reaches the output, the assets anchored to its text go with it.** An
asset is dropped only when the text it sits in was dropped.

The anchor records how precisely it was placed — `own_text`, `caption_located`,
`context_located`, `page_region` (a whole page, so every unit on it relates), or
`none`. Treat `page_region` as the coarse claim it is.

**An asset related to nothing is a coverage finding, not a filing error.** It
means no unit was extracted from the passage it sits in — a hole in the reading.
`kip validate` warns, and Pass 5's corpus-coverage audit is handed the list by
caption. On the GE 10-K demo, 61 of 100 tables are unrelated and the audit
correctly returns `fairly_represented: false`.

## Inspecting results

```bash
kip --workspace .kip show <run-id> units --pretty --limit 5
kip --workspace .kip show <run-id> audits --pretty
kip --workspace .kip validate <run-id>      # provenance + integrity check
kip --workspace .kip trace <run-id> <queue-event-id|candidate-id|unit-id>
```

`trace` prints the full chain from a queue event back to the original file and
the exact quoted excerpt. `validate` fails loudly if any excerpt no longer
matches its source, any ID dangles, or any audit ran without a distinct auditor;
it warns on orphaned assets and on duplicate slugs.

## Reading the output honestly

The pipeline reports its own uncertainty, and that reporting is load-bearing:

- **`relationship_bucket` is trustworthy; `relationship_subtype` is advisory.**
  Coarse stance (supports/contradicts/insufficient) is the tier benchmarks
  validate at ~70–80%. Fine subtypes measured far worse. Every subtype carries
  `subtype_confidence` — respect it.
- **A `contradicts` verdict is reliable; the absence of one is not.** Flagged
  contradictions are ~88% precise, but most real contradictions get missed.
  Never read "no contradiction found" as "consistent."
- **`auditor_confidence` is not calibrated.** It is recorded for analysis, and
  deliberately gates nothing.
- **Deterministic checks beat LLM checks.** In an audit record, checks with
  `"mode": "deterministic"` (citation accuracy, provenance integrity,
  independence inflation) have no error rate. Checks with
  `"mode": "llm_reasoning"` carry roughly one-in-five error on hard cases.
- **Verbatim citation guarantees fidelity to the source AS INGESTED**, and says
  nothing about whether that source is faithful to what was published. The
  Sharpe demo's source is a lossy HTML reprint that silently drops a twelve-word
  clause from a footnote; every citation to it verifies, correctly. Provenance
  quality is an input decision the pipeline cannot repair.

## When a run looks wrong

1. `kip validate <run-id>` first — it catches fabricated quotes, dangling IDs,
   and missing sources mechanically.
2. Check `02_units/omissions.jsonl` — the omission pass records what the
   extractor missed, and roughly a quarter of resolved omissions flip a
   downstream conclusion. Findings marked `add` feed one repair round.
3. Check `06_audit/corpus_coverage.json` — whether the output represents the
   whole corpus, including which assets sit in unread passages.
4. Check `quarantined` in the run summary — an unparseable source is
   quarantined with a reason, never silently skipped.
5. Compare `05_candidates/candidates.initial.jsonl` against
   `06_audit/candidates.approved.jsonl` — the diff is what the audit changed.

## Worked examples

`${CLAUDE_PLUGIN_ROOT}/demo/real-runs/` holds six complete runs on real
documents — a journal paper scan, a 10-K, a Wikipedia article, a fairy tale, a
specification and a three-page essay. Each folder's `README.md` shows the assets
rendered, names the ingestion order for a model, and describes every artifact
directory. Each replays byte-identically from its shipped
`_handoff/responses.jsonl`.

Read `demo/real-runs/README.md` first for what the six runs measured against
each other.

## Security posture

Source documents are treated as untrusted data. Untrusted text is datamarked
and tag-wrapped, and no LLM pass has tool access — so an injected instruction
can at worst corrupt a field value, never take an action. Injection cannot be
eliminated (the best models still break ~0.5% of the time under adaptive
attack), so validate outputs rather than assuming clean input. See
specification §20.

## Research

Every design rule in the specification traces to a file in
`${CLAUDE_PLUGIN_ROOT}/research/`. Rounds 1–4 carry 3-vote adversarial
verification; round 5 and the briefs are sourced-and-quoted only. Each file
lists its own refuted claims — those must never be cited as support.

- `2026-08-13-non-textual-content-research.md` — the evidence behind the three
  fidelity classes and the systems each follows: why TEDS is close to blind to
  header association, why exact-match scoring understates correct formula
  transcription, what chart understanding actually measures.
- `2026-08-08-knowledge-type-taxonomy-research.md` — whether a small,
  cognitively-framed type taxonomy (Concepts / Claims / Models / Methods /
  Rules / Cases) is a sound organizing scheme, and what DITA, Information
  Mapping, Diátaxis, CoALA, A-MEM, Zep and Mem0 actually measured. Evidence base
  for `docs/KNOWLEDGE-TYPE-TAXONOMY.md`.
