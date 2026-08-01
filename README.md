# Knowledge Ingestion Pipeline

Turns a folder of heterogeneous documents — PDFs, Word files, slide decks,
emails, HTML, notes — into audited knowledge-base entries where every claim can
be traced back to the exact sentence it came from.

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

## As a Claude Code plugin

The repo is a plugin. Install it, then use `/kip-ingest <folder>` and
`/kip-trace <run-id> <id>`, or just describe the task — the
`knowledge-ingestion` skill activates on requests like *"do these documents
contradict each other"*.

## How it works

```
files ─▶ 0 normalize ─▶ 1 extract ─▶ 2 route ─▶ 3 assess ─▶ 4 plan ─▶ 5 audit ─▶ 6 enqueue
         (code)          (LLM)        (LLM+code)  (code+LLM)  (LLM)    (code+LLM)  (code)
```

Artifacts land under `runs/<run-id>/`, one JSONL file per pass, each record
carrying a content hash and pointers to its parents.

## Design decisions worth knowing

These are the places the research overturned the obvious choice:

**Units are molecular, not maximally atomic.** Splitting claims into the
smallest possible pieces is the intuitive move and it is wrong here — fully
atomic facts lose the context needed to interpret them, and decomposition
measurably *hurts* accuracy when strong models do the downstream work, which is
exactly this setup. Units are minimal *subject to* still standing alone.

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

**Injection can't be eliminated, so the architecture absorbs it.** No LLM pass
has tool access and all output is schema-constrained, which means an injected
instruction can at worst corrupt a field value — never take an action.
Untrusted text is datamarked, the single highest-payoff defense measured.

Each of these cites its evidence inline in the [specification](docs/SPECIFICATION.md).

## Tests

```bash
PYTHONPATH=src python -m pytest tests/ -q
```

36 tests, no API key needed. They cover the deterministic half directly
(normalization, locator maps, hashing, citation verification, independence
arithmetic, idempotent enqueueing, resume) and the LLM passes through a scripted
fake client that verifies wiring — including that the audit actually catches a
deliberately overconfident candidate.

## Status

Initial implementation. Passes 0 and 6 and all deterministic checks are
verified end-to-end on real files; passes 1–5 are verified for wiring against a
fake client but have **not** been run against the live API yet.

Open questions the research left unresolved — including whether the fine-grained
relationship vocabulary is reliable enough to trust — are listed in
[specification §23](docs/SPECIFICATION.md#23-open-questions).
