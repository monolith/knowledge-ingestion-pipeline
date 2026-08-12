# Real runs

Three complete runs on real documents, produced by the CLI in `--mode handoff`
with **no API key** — the agent running the CLI answered every model call. These
are the pipeline's actual output, not fixtures.

Read `UNITS.md` in each folder. The `.jsonl` files beside it are the artifacts
the pipeline wrote; `render.py` turns them into the markdown.

## What each run shows

| run | source | units | density | what it demonstrates |
|---|---|---|---|---|
| `01-sharpe-v31` | Sharpe excerpt, 223 words | 9 | 1 per 25 words | the original **minimality** prompt |
| `02-sharpe-v41` | same 223 words | 7 | 1 per 31 words | **sufficiency + cited imports** |
| `03-spec-long` | a 12,311-word specification | 12 | **1 per 1,025 words** | **the windowing failure** |

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
SPECIFICATION.md 12,311 words → 12 units   (1 per 1,025 words)
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
works; the coverage does not. Windowing is the fix and it is not built.

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
