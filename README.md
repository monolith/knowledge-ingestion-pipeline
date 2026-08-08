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
kip --workspace .kip migrate-taxonomy <run-id>           # backfill types on an old run
```

Runs resume: a completed pass is reused rather than recomputed, so an
interrupted or extended run never repeats the expensive extraction step.

`migrate-taxonomy` is also what upgrades a run made before schema 3.1.0 — those
runs hashed the unit's type into its content hash, so `validate` rejects them
until they are migrated.

## Demo — no API key needed

```bash
python demo/run_demo.py                    # scripted client, temp workspace
python demo/run_demo.py --workspace .kip   # keep the artifact tree somewhere
python demo/run_demo.py --live             # same code path, real API (costs money)
```

Ingests the two documents in [`demo/sources/`](demo/sources/) — a randomized
trial and a practitioner review that disagree about the same effect — through
all seven passes, then prints units by type and family, the flags, the
quantitative and multi-fire counts, the entity mentions that reached the
enriched units, and what the audit changed. The artifact tree it writes is real:
`kip show` and `kip trace` work on it.

Every model call is served by a canned transcript, so the run is free,
deterministic, and offline. The test suite executes it.

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

**Six yes/no questions beat one six-way question.** Every unit gets typed —
case, rule, method, concept, model, claim — but the model is never asked to pick
one. It answers six independent booleans in a single call, and the priority
order that resolves them lives in code. Asking a model to choose one label from
a list measured about 90% lower odds of getting it right than asking a yes/no
question. Chaining six separate yes/no calls instead would have been worse
still: six gates at 95% each compounds to roughly 74% end to end.

**Uncertainty is a shape, not a number.** No confidence score is asked for. If
no test fires, the unit is `unclassified` — a visible health metric, not a
silent default. If two fire, it is flagged `multi_fire`, which almost always
means the sentence should have been two units. A confidence number would be one
more thing to calibrate, and a "when unsure, pick X" instruction measurably
biases models toward X.

**A classification is a derivation, so it never touches content identity.**
A unit's content hash covers the assertion — statement, evidence, source
lineage — and deliberately excludes its labels. The earlier version hashed the
type along with everything else, which meant re-classifying a corpus forged new
hashes and the integrity check rejected it. Re-typing is now free; overwriting
is still forbidden.

**Injection can't be eliminated, so the architecture absorbs it.** No LLM pass
has tool access and all output is schema-constrained, which means an injected
instruction can at worst corrupt a field value — never take an action.
Untrusted text is datamarked, the single highest-payoff defense measured.

Each of these cites its evidence inline in the [specification](docs/SPECIFICATION.md).

## Tests

```bash
pytest -q          # or: PYTHONPATH=src python -m pytest tests/ -q
```

273 cases from 195 test functions (the difference is parametrization), no API
key and no network needed. They cover
the deterministic half directly — normalization (including PDF, DOCX, PPTX,
XLSX and multipart email, each built in the test), locator maps, hashing,
citation verification, independence arithmetic, idempotent enqueueing, resume,
the type taxonomy and its legacy migration — and the LLM passes through a
scripted fake client that verifies wiring.

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
unqueueable; a migration is proved not to overwrite a live classification or to
launder an edited statement; and a source added mid-run is proved to stop the
resume rather than to vanish from it. The demo runs as a test too.

## Status

Initial implementation. Passes 0 and 6 and all deterministic checks are
verified end-to-end on real files; passes 1–5 are verified for wiring against a
fake client but have **not** been run against the live API yet.

The type taxonomy is in the same position. Its deterministic half — the
derivations, the quantitative regex, the legacy migration, the content-hash
invariant — is tested directly. Whether a real model answers the six type tests
consistently is **unmeasured**; that is what the retained `unit_type` field is
the control arm for.

Open questions the research left unresolved — including whether the fine-grained
relationship vocabulary is reliable enough to trust — are listed in
[specification §23](docs/SPECIFICATION.md#23-open-questions).
