---
name: knowledge-ingestion
description: Use when ingesting documents into a knowledge base — extracting source-backed knowledge units from PDFs, Word docs, slide decks, emails, HTML or notes; comparing claims across documents to find agreement and contradiction; auditing proposed knowledge-base entries against their sources; or tracing a knowledge-base claim back to the exact text it came from. Triggers on "ingest these documents", "extract knowledge from", "what do these sources say about", "do these documents contradict each other", "where did this claim come from".
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
| 0 normalize | files → plain text + locator map (page/char offsets) | code |
| 1 extract | text → molecular, source-backed knowledge units | LLM |
| 2 route | contextual enrichment, then hybrid BM25 clustering | LLM + code |
| 3 assess | match candidate pairs, then judge relationships | code + LLM |
| 4 candidates | assessments → proposed KB operations | LLM |
| 5 audit | adversarial audit; deterministic + reasoning checks | code + LLM |
| 6 enqueue | idempotent queue events for the KB engine | code |

Nothing reaches a knowledge base without passing Pass 5.

## Setup

```bash
pip install -e "${CLAUDE_PLUGIN_ROOT}[parse-lite]"
export ANTHROPIC_API_KEY=sk-ant-...
```

`parse-lite` adds PDF/DOCX/PPTX/XLSX support (a few MB). Use `[parse]` instead
for Docling, which gives bounding-box provenance but pulls a multi-GB ML stack.

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

## Inspecting results

```bash
kip --workspace .kip show <run-id> units --pretty --limit 5
kip --workspace .kip show <run-id> audits --pretty
kip --workspace .kip validate <run-id>      # provenance + integrity check
kip --workspace .kip trace <run-id> <queue-event-id|candidate-id|unit-id>
```

`trace` prints the full chain from a queue event back to the original file and
the exact quoted excerpt. `validate` fails loudly if any excerpt no longer
matches its source, any ID dangles, or any audit ran without a distinct auditor.

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

## When a run looks wrong

1. `kip validate <run-id>` first — it catches fabricated quotes, dangling IDs,
   and missing sources mechanically.
2. Check `02_units/omissions.jsonl` — the omission pass records what the
   extractor missed, and roughly a quarter of resolved omissions flip a
   downstream conclusion.
3. Check `quarantined` in the run summary — an unparseable source is
   quarantined with a reason, never silently skipped.
4. Compare `05_candidates/candidates.initial.jsonl` against
   `06_audit/candidates.approved.jsonl` — the diff is what the audit changed.

## Security posture

Source documents are treated as untrusted data. Untrusted text is datamarked
and tag-wrapped, and no LLM pass has tool access — so an injected instruction
can at worst corrupt a field value, never take an action. Injection cannot be
eliminated (the best models still break ~0.5% of the time under adaptive
attack), so validate outputs rather than assuming clean input. See
specification §20.
