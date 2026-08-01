# Handoff

This repo is a **research-validated design plus a working skeleton**, not a
finished product. The valuable artifact is the specification and the evidence
behind it; the code exists to prove the design is buildable and to give you a
frame to build inside.

Read this file, then [`docs/SPECIFICATION.md`](docs/SPECIFICATION.md) §1 (the
change table). That is enough to start.

---

## What this is

A pipeline that turns heterogeneous documents into audited knowledge-base
entries where every claim traces back to the exact sentence it came from. Seven
passes, append-only JSONL between each, adversarial audit before anything is
queued.

The design started as a v2.0 specification written from experience. Five rounds
of research — four of them with 3-vote adversarial verification per claim —
tested it against published evidence. Ten decisions changed. The specification
now cites the evidence for each one inline.

## What is decided, and don't undo it casually

Each of these overturned an intuitive choice. The evidence is cited in the spec
section named; read that before reversing one.

| Decision | Why it isn't the obvious choice | Spec |
|---|---|---|
| Units are **molecular**, not maximally atomic | Decomposition's value *inverts* with verifier strength — it helps weak verifiers and measurably hurts strong ones (72.3 F1 undecomposed vs 59.9–68.2 decomposed, on a strong verifier). This pipeline runs strong models downstream. | §9.2 |
| Relationship judgment is **coarse first, subtype second** | Only 3-way stance is benchmark-validated (~70–80%). Fine-grained contradiction typing peaked at 0.401 accuracy, and chain-of-thought made it *worse*. | §11.3 |
| Candidate pairs are matched **in code** before any LLM judgment | Open-ended "does this contradict?" runs near chance even for frontier models; the same model given a specific pair succeeds ~77%. Worth ~25 accuracy points. | §11.2 |
| The auditor is a **different, reasoning-class model** | Non-reasoning judges score near chance on hard correctness. Self-preference bias survives anonymization. The code refuses to run if planner == auditor. | §13.3 |
| Citation and provenance checks are **deterministic code** | Automated semantic citation checkers top out at ~80–85% agreement with humans. String and offset comparison has no error rate. | §13.4 |
| **Contextual enrichment before indexing** | The one evidence-backed technique v2.0 lacked outright: 49% reduction in retrieval failures (vendor-measured), 5–15% in independent replications. | §10.2 |
| Batches capped on **unit count**, ~20–50 | Degradation begins around 20–100 instances and then collapses; instance count matters *more* than token count. | §17 |
| Item ordering is **rotated** across passes | Mid-prompt items suffer up to a 22pp accuracy penalty; mid-context can fall below the model's own closed-book baseline. | §11.8 |
| Schema-constrained JSON on every pass | The 2024 "constrained decoding hurts reasoning" alarm did not survive. For classification and extraction the effect is neutral-to-positive, and unconstrained prompting produced **0% JSON validity** in one study. | §19.2 |
| Injection is **absorbed, not prevented** | Best models still break ~0.5% under adaptive attack. No LLM pass gets tool access, so the worst case is a corrupted field value, never an action. | §20 |

## What is open — decide these before or during the build

Full list in [spec §23](docs/SPECIFICATION.md#23-open-questions). The ones that
should change what you build:

1. **The fine-grained relationship vocabulary is unvalidated.** No benchmark
   tests these 15 labels. Before Pass 4 relies on any fine label, build a small
   in-house eval — a few hundred labeled pairs from the real document domain —
   and get per-label confusion data. Until then the 4-bucket grouping is the
   trust boundary.
2. **Can source independence be detected automatically?** The whole
   independence-group mechanism currently rests on operator-supplied metadata.
   Nothing verified says this can be inferred reliably.
3. **Does the thinking-field mitigation help these passes?** It averaged +9.2pp
   across benchmarks but made 15% of cases *worse*. It is on by default and
   trivially switchable (`add_thinking=False`). Measure it per pass; do not
   assume.
4. **Six `[NEW — confirm]` items in the spec** are engineering judgment, not
   evidence — search the spec for that marker. The per-pass model tier table
   (§19.4) is the one most likely to need changing for cost reasons.

## What is verified, and what is not

**Verified against real files:** Pass 0 normalization across PDF/DOCX/PPTX/
email/HTML/Markdown with page and slide provenance; Pass 6 enqueueing; all
deterministic audit checks; `validate`; `trace`. 36 tests, no API key required.

**Wiring-verified only:** Passes 1–5 have **never run against the live API.**
They are exercised end-to-end through a scripted fake client
(`tests/test_pipeline_integration.py`), which proves artifacts flow correctly
and the audit catches a deliberately overconfident candidate — but says nothing
about real model behavior.

**Not built at all:**
- The MiniCheck-class grounding checker (§13.4 check 1). `AuditPolicy.nli_checker_model`
  is the hook; today grounding degrades to LLM judgment and the audit record
  says so.
- The dense half of hybrid retrieval. `route_and_cluster(..., embedder=...)`
  takes a callable; nothing supplies one, so routing is currently lexical +
  metadata only. Anthropic has no embeddings endpoint — bring your own.
- Batch API submission. `Config.use_batch_api` exists and is unused. Pass 1 is
  the natural candidate: 50% off, and it stacks with prompt caching.
- Bi-temporal invalidation (§11.6). The `t_valid`/`t_invalid` fields are carried
  through the schema but nothing consumes them.
- Retraction/source-validity screening (§11.5). `source_validity_flags` is
  populated only by the pipeline's own corrections.

## Suggested build order

1. **Get a live run working.** Set `ANTHROPIC_API_KEY`, then
   `kip --workspace .kip run --sources ./docs --stop-after extract`. Inspect
   the units. This is the cheapest real test and the highest-information one —
   if extraction quality is poor, nothing downstream matters.
2. **Evaluate extraction against the Claimify rubric** (§9.5): entailment,
   element-level coverage, decontextualization. Deliberately *not* atomicity.
3. **Tune granularity.** `GranularityPolicy` is a knob and every unit records
   which policy produced it. This is the parameter the research says matters
   most and cannot be set from first principles.
4. **Run the full pipeline** and diff `05_candidates/candidates.initial.jsonl`
   against `06_audit/candidates.approved.jsonl`. That diff is the audit earning
   its cost. If the audit never changes anything, something is wrong — most
   likely the auditor is not actually a reasoning-class model.
5. **Build the in-house relationship eval** (open question 1). Everything Pass 4
   does downstream inherits Pass 3's error rate.
6. Then the unbuilt pieces above, in whatever order the workload demands.

## Ground rules for extending this

- **Cite evidence or mark it as judgment.** The spec distinguishes verified
  research (`R1`–`R4`), sourced-only material (`R5`, `PE`, `SDK`), carried-forward
  v2.0 decisions, and `[NEW — confirm]` engineering judgment. Keep that
  distinction — its whole purpose is that a reader can tell how much weight a
  decision carries without re-reading the research.
- **Don't cite a refuted claim.** Each research file lists what was refuted and
  why. One trap in particular: Dense X Retrieval is *not* evidence that
  proposition-level indexing beats passage-level — that specific claim was
  refuted 0-3, though the paper's atomicity rubric is still citable.
- **Deterministic beats judged.** If a check can be a string comparison, make it
  one. Every check moved out of the LLM removes a ~20% error rate.
- **Keep the uncertainty in the output.** `subtype_confidence`,
  `excerpt_verified`, `auditor_confidence`, and check `mode` fields all exist so
  consumers can tell what to trust. Flattening them into a clean answer would
  undo the point of the design.

## Repo map

```
docs/SPECIFICATION.md   the deliverable — read §1 first
research/               7 files; rounds 1-4 adversarially verified, rest sourced
src/kip/                skeleton implementation, spec sections cited inline
tests/                  36 tests, no API key needed
skills/, commands/      Claude Code plugin surface
```
