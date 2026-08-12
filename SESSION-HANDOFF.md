# Session handoff — 2026-08-12

**If you are an agent resuming this work, everything you need is in this file.
Read it top to bottom, then `demo/real-runs/README.md`. Start on Open work item
A (document windowing) unless told otherwise.**

Written for whoever picks this up next. `HANDOFF.md` describes the project;
this describes **what changed in this session, what is open, and what will bite
you.**

---

## Resuming: the short version

**What kip is.** A knowledge **digestion** pipeline: it breaks documents into
standalone chunks with verified citations and finds relationships between them.
Classification was deliberately removed this session — it happens afterwards, in
a separate classifier that does not exist yet. **Do not add typing back.**

**Where the work is.** Branch `refactor/strip-classification-dual-runtime`, 180
tests passing, pushed but not merged.

**What to do first.** Open work item A below: document windowing. It is the
largest defect and it is quiet — it does not error, it silently returns a
summary instead of a digestion.

**How to run it live.** Not with the scripted client — that is what hid every
real bug for the life of this project. Use the handoff runtime, where you are
the model:

```bash
PYTHONPATH=src /home/sirlunch/workspace/conda/bin/python3 -m kip \
  --workspace /tmp/ws run --sources <dir> --run-id r1 --mode handoff --show-request
```

Each model call is written to `_handoff/pending.jsonl` and the process exits 10.
Answer by appending one line to `_handoff/responses.jsonl`:

```
{"call_id": "<id from the output>", "response": { ...schema-valid object... }}
```

Then re-run the same command. Completed stages resume; answered calls are cache
hits; only the frontier advances. Exit 0 means the run finished.

**Tests.** `/home/sirlunch/workspace/conda/bin/python3 -m pytest -q`
(pytest is not on the default python).

**The bar for a chunk**, in Anatoly's words: clear as a standalone insight *"not
just as a grammatical sentence but as a point in context of the paper"* — good
enough for a high-school comprehension test, a logic test, and to hold ground in
a PhD thesis citing it. Windowing must not lower that.

Two repos are in play:

| repo | what it is | state |
|---|---|---|
| `~/knowledge-ingestion-plugin` (`kip`) | the digestion pipeline | branch `refactor/strip-classification-dual-runtime`, 180 tests pass, **pushed, not merged** |
| `~/statement-classifier` | the taxonomy spec | `master`, public, **spec only — no code exists** |

---

## Start here

1. `demo/real-runs/README.md` — three real runs with rendered output. It is the
   fastest way to see what the pipeline actually produces and where it fails.
2. This file's **Open work** section.
3. `docs/SPECIFICATION.md` only if you need pipeline internals.

---

## What changed this session

### 1. Classification was stripped out (`ff13f52`)

Anatoly's framing, and it is the right one: **this is digestion, not ingestion.**
The pipeline breaks documents into chunks and finds relationships between them.
Typing those chunks is a separate job done afterwards, by something that reads
the canonical statement — and also needed for chat, which never goes through
this pipeline at all.

Deleted: `taxonomy.py`, `migrate.py`, the `migrate-taxonomy` command, the
`type`/`family`/`unit_type`/`type_tests` fields, the type-and-family validation,
and the type rendered into the route, assess, audit and trace prompts.

`vocab.py` is new and holds what was never a classification: `MODALITIES`,
`FLAGS`, `NODE_KINDS`, `GROUNDING`, `detect_quantitative`. Its docstring says
the package must not grow typing back. **Please honour that** — the reason it
was safe to remove is that nothing branched on it; the type was produced in
pass 1 and read as decoration everywhere else.

### 2. Dual runtime (`0955170`, `32daddf`)

`complete_json` is the only seam every pass goes through, so a second client was
all it took.

- `--mode sdk` — calls Anthropic, needs a credential.
- `--mode handoff` — writes each request to `_handoff/pending.jsonl` and stops
  with **exit 10**. The agent answers into `responses.jsonl` and re-runs; stages
  resume from checkpoints and answered calls are cache hits.

This is what finally let kip process a real document. Before it, **every test in
the package drove a scripted client and the pipeline had never seen a real
model.** Two bugs surfaced in the first live run, both of which would bite the
SDK runtime equally:

- `HandoffPending` inherited `Exception`, and several passes wrap their model
  call in `except Exception: report and continue`. Pass 3 caught the pending
  signal, reported a failure, wrote an empty artifact, checkpointed the stage as
  complete, and the answer supplied afterwards was never read. It now inherits
  `BaseException`. **If you add a pass, do not catch `BaseException`.**
- `HandoffClient` returned whatever the agent wrote, unvalidated. Answers are now
  schema-checked where they are supplied.

### 3. The extraction prompt was rewritten twice (`v3.1 → v4.0 → v4.1`)

This came from Anatoly reading the output and saying the chunks were "a little
light". He was right, and the prompt was at fault:

> **MINIMALITY:** adds the LEAST information required to achieve
> decontextuality, and no more.

That is an explicit instruction to strip the context that makes a point a point.
It produced statements that were grammatically standalone and argumentatively
orphaned.

- **v4.0** replaced minimality with **SUFFICIENCY**: a unit must stand alone as
  an *insight* — a reader who never saw the document should be able to answer a
  comprehension question about it, follow its reasoning, or apply its formula.
  `context_note` got a real description (it had none, and came back empty on
  every unit).
- **v4.1** added citation roles. Evidence carries `role: primary | supporting`.
  Sufficiency licenses importing context; it does **not** license asserting it
  uncited. Any claim beyond the primary passage must quote the passage that
  licenses it.

Effect on the same 223-word source: 9 units → 7, median 22 → 58 words,
`context_note` 0/9 → 7/7, citations 1.0 → 2.3 per unit. **Unit count went down**
— two pairs merged, because small pieces of an argument are rubble.

### 4. `grounding` (`d2176ae`)

Anatoly's request: flag whether a unit came from the document or from the
model's own knowledge. Three values, following retrieval-evaluation practice
where this is called grounding or faithfulness:

`attributable` · `conventions_added` · `unattributed_content`

The model is asked a **counterfactual it can answer** — "if this document were
the only thing you had ever read, could you have written this unit?" — not a
question about its training data, which it cannot inspect.

**It is checked, not trusted.** `validate._check_grounding` errors on a unit
claiming `attributable` while resting on an unverified excerpt, warns when a
unit records imported context but cites no supporting excerpt, and counts
unattributed units as a health metric rather than failing the run.

### 5. CCITT decoder (`ffed9d0`)

Scanned PDFs carry pages as CCITT images with no text layer, so every extractor
kip had returned nothing. `ccitt.py` is a dependency-free ITU-T T.4/T.6 decoder
plus a minimal PNG writer (no Pillow, no poppler on this host, and adding an
image library to a text pipeline for one codec is a poor trade).

Verified on the De Bondt & Thaler (1985) scan: 13 pages, all 6,296 rows of page
one, 7.1% ink, fully legible.

**It is decoded but not wired into `normalize`.** See open work.

---

## Open work, most important first

### A. Document windowing — the biggest defect

`extract` sends the **whole document in one call**. There is no chunking
anywhere in the pipeline, and the `context_reservation: 0.4` knob in
`config.py` is never read.

Measured, same extractor and prompt:

```
Sharpe excerpt      223 words →  9 units   (1 per    25 words)
classifier spec  12,311 words → 12 units   (1 per 1,025 words)
```

**A 41× collapse in density.** One pass over 12,000 words with "return as many
units as the source warrants" produces a *summary-shaped* answer. The omission
check diagnosed its own run — fifteen label definitions, twenty-two pairwise
rules, three field vocabularies and an entire evidence register unrepresented.
See `demo/real-runs/03-spec-long/`.

Everything else held at that length: every citation verified, all units
`attributable`, median 45 words. **The quality machinery works; the coverage
does not.**

Suggested shape: split into overlapping sections, extract per section, dedupe
against `independence_group`. Watch out — a supporting citation may live in a
different window from its primary, so evidence resolution has to see the whole
document even when extraction does not.

### B. Wire the CCITT decoder into `normalize`

`ccitt.pdf_page_images` produces PNGs; nothing calls it. The natural design is
an OCR path in `normalize` that, in handoff mode, hands page images to the agent
— same pattern as the LLM calls, since the agent is the vision model.

Note the architecture Anatoly named and which already half-exists:
`00_original_sources/` keeps the raw file, `01_normalized/<id>/normalized.txt`
is the full text digestion works from. OCR output belongs in the second.

### C. Merge the branch

Six commits, 180 tests, not merged. Anatoly wanted to review first.

### D. The classifier does not exist

`~/statement-classifier` is a specification with **zero Python files**. It is
well-specified — 22 runs, ~10,000 assignments, α 0.934 on generated statements
and 0.894 on published documents — but nothing implements it. Digestion now
produces untyped units and there is nothing downstream to type them.

---

## Things that will bite you

**Do not put the workspace inside the sources directory.** `discover_sources`
recurses, so the second run finds its own artifacts as new sources and the
stage-fingerprint check fails the run. Correct behaviour, confusing symptom.

**Answering handoff calls by hand is exacting.** Two shapes bit me: `assertions`
must be objects with `text` and `assessment_ids` (not bare strings), and audit
`findings` must be strings (not objects). The validator now names the exact
path, so read the error rather than guessing.

**`pytest` is not on the default python.** Use
`/home/sirlunch/workspace/conda/bin/python3`, and `PYTHONPATH=src python3 -m kip`
to run the CLI without installing.

**Do not transcribe copyrighted sources into the repo.** I tried to write out
De Bondt & Thaler as a test corpus and hit a content filter — correctly.
Decoding a scan to *read* it is fine; reproducing the paper is not. The demo
uses a document we wrote instead.

**The web-search budget was exhausted** (200/200) in the previous session. The
`grounding` docstrings name established practice but attach no paper citations,
because I could not verify them. If the spec should cite the literature by name,
that needs a fresh session — do not invent references.

---

## Context that is not in the code

Anatoly's standard for a chunk, in his words: it must be clear as a standalone
insight *"not just as a grammatical sentence but as a point in context of the
paper"* — good enough to answer a high-school comprehension test, a philosophy
or logic test, and to explain a formula in depth. And the citations must hold up
well enough to *"hold ground in a PhD thesis that uses the paper in its
argument."* That standard is what v4.0 and v4.1 encode; if you change the
extraction prompt, that is the bar to hold it to.

One finding worth carrying forward, measured repeatedly across both repos:
**changes that make the model reason more tend to lose; changes that tell it
what to look for tend to win.** In the classifier work, sixteen structural
designs moved nothing while rewriting fourteen definitions moved α by 0.090. In
this repo, the same shape: the wins were naming what a unit must carry, not
adding steps to the pipeline.
