---
title: Knowledge-type taxonomy for an LLM-maintained wiki
date: 2026-08-08
status: proposal for review
evidence: research/2026-08-08-knowledge-type-taxonomy-research.md
---

# Knowledge-Type Taxonomy for an LLM-Maintained Wiki

A review of the proposed 3-family / 6-type taxonomy, and a recommended revision.

**Evidence tags.** `[T1-n]` = adversarially verified (3-vote) finding *n* in
[the research file](../research/2026-08-08-knowledge-type-taxonomy-research.md).
`[T2:source]` = sourced from a fetched primary text but **not** adversarially
verified — a careful single reading, no more. `[spec §n]` = an already-verified
finding in [`SPECIFICATION.md`](SPECIFICATION.md). Anything with no tag is my
judgment, and is marked as such.

---

## 1. Critique of the proposal

Five things are right, four are wrong, and one is a claim the proposal makes
about itself that the evidence does not support.

### What holds up

**Unit-level classification over page-level.** Correct, and it is the more
important lever than the label set. EMem's authors frame the entire design space
as a granularity tradeoff — coarse chunks retrieve imprecisely, fine units
fragment meaning — and chose a coarser "self-contained event proposition" over
relation triples specifically because triples force retrieval to locate and
recombine several units to answer one question `[T2:EMem]`. Your spec already
landed on the same answer independently: the molecular rule, decontextuality plus
minimality `[spec §9.2]`. Keep it.

**Epistemic status as metadata, not as types.** Correct, and for a sharper reason
than the proposal gives. "Fact," "hypothesis," "insight," and "prediction" are not
different *kinds* of knowledge — they are different *degrees of settledness* about
the same kinds. Making them types would multiply the label set by the status set.
The proposal's own worked example (`insight` → `type: model, status: proposed,
origin: inferred`) is exactly right, and example 20 below shows it working on a
real oracle-style output.

**Separating a knowledge-unit's type from the page it lives on.** Correct, and it
avoids the best-documented failure mode in this whole literature — see below.

**Refusing domain-specific top-level categories.** Correct as a principle,
though it collides with the strongest piece of prior art (see "The domain
problem").

**Six rather than three.** Defensible. Mark Baker's critique of DITA's
concept/task/reference is that a three-way split with a residual bucket makes the
residual too internally diverse to be useful — his analogy is splitting the animal
kingdom into cats, dogs, and everything else `[T2:EveryPageIsPageOne]`. Taxonomies
can be too small. But note this is an argued blog critique, not a measurement, and
**every quantitative claim that label count drives reliability failed
verification** `[T1-9]` — including the tempting "six-to-three doubles accuracy"
figure. You have no external number to design against in either direction.

### What does not hold up

**The three families are mis-leveled.** This is a real error, not a quibble.
In Squire's canonical taxonomy — the source everyone cites — `DECLARATIVE`
branches into exactly two leaves, `FACTS` and `EVENTS`, converging on a single
substrate; `PROCEDURAL` sits under `NONDECLARATIVE`, alongside priming and
classical conditioning `[T1-1]`. So "Declarative" is the *parent* of your
"Episodic," and "Procedural" is on a different branch entirely. Putting the three
side by side mixes two cutting axes. The machine architectures that do use a
co-equal triad — Soar, and CoALA `[T2:CoALA]` — name the third module **semantic**
precisely to dodge this collision. Fix: rename family 1 to **Semantic**. It costs
nothing and removes a defect any careful reader will find.

**"Cognitively grounded" is doing work it hasn't earned.** Squire's boundaries are
carved by lesion dissociation in amnesic patients — impaired declarative memory
alongside intact nondeclarative learning `[T1-4]`. There is no analogue of a
lesion study for a paragraph on a wiki page. Borrowing the vocabulary does not
import the evidence. Worse, the boundaries the proposal leans on are explicitly
continua in their own primary literature: Renoult et al. conclude the
episodic/semantic boundary is "not as distinct" as Tulving implied, anatomically
or functionally; Rubin says he knows of "no convincing evidence" his dimensions
reduce to categories and keeps them only "to simplify communication" `[T1-2]`. And
the explicit/implicit cut — the nearest ancestor of your Declarative/Procedural
split — is the *weakest* of Rubin's three dimensions, lacking a plausible unified
neural basis `[T1-3]`.

This does not mean drop the split. It means **change the justification**. The
honest warrant is computational, not neuroscientific: these categories have
different write rules, different update rules, and different retrieval patterns.
That is exactly how CoALA justifies its triad, and CoALA never cites lesion
evidence `[T1-4]`. Say that in the schema file.

**"Primary + optional secondary + confidence is closer to how knowledge really
works."** Do not make this argument. The specific inference — that because type
membership is graded, a primary+secondary+confidence encoding is closer to the
underlying data — was put to the verifiers as its own claim and **refuted 0–3**
`[T1-2]`. Keep primary+secondary; justify it as retrieval hedging, which is an
engineering reason and a good one.

**"Models" is a dumping ground.** As written it absorbs relationships,
structures, recurring patterns, mechanisms, theories, taxonomies, and
explanations. That is six things. It is also the type most exposed to the
best-documented failure in this literature: in practice, DITA's information types
degenerated from kinds-of-knowledge into *presentation formats* — practitioners
classified by output shape, so a table became "reference," numbered steps became
"task," prose became "concept" `[T2:EveryPageIsPageOne]`. The equivalent failure
here is classifying a page as `Model` because its subject is called a model — a
pricing model, a data model, a risk model. Needs a hard negative definition.

### The claim the proposal makes about itself

The proposal presents itself as descending from Karpathy's LLM Wiki. It does not.
The gist's page taxonomy is document-genre and entity based — summaries, entity
pages, concept pages, comparisons, an overview, a synthesis. It proposes **no**
knowledge-type taxonomy, no sub-page unit granularity, and no status or confidence
metadata `[T2:Karpathy]`. Your six types are an addition, not an inheritance.
That's fine — it's the gap worth filling — but the design doc should say so
rather than borrowing borrowed authority.

### The domain problem

The single most uncomfortable piece of prior art. Robert Horn built the closest
thing to this taxonomy that has ever shipped commercially — Information Mapping's
seven types for "relatively stable subject matter": Procedure, Process, Concept,
Structure, Classification, Principle, Fact. The mapping onto your six is almost
one-to-one (Concept≈Concepts, Procedure≈Methods, Principle≈Rules,
Structure+Process≈Models; he has no Claims and no Cases) `[T2:Horn]`.

Two findings from him you need to sit with:

1. **He concluded the type set is domain-scoped.** Extending the method beyond
   stable subject matter required *new* type sets, not reuse — the memo/report
   extension identified fifteen basic types, and "disputed discourse" is a
   separate domain from stable subject matter `[T2:Horn]`. The practitioner who
   pushed a universal small type set hardest concluded the labels change when the
   author-reader stance changes. Your brief asks for one set spanning trading,
   onboarding, software design, reference, brainstorming, and oracle analysis.
2. **He shipped an explicit escape hatch.** ~40 fine block types under the 7
   coarse types, covering only ~80% of the domain, with writers given criteria to
   invent new block types for the rest, because the residue is idiosyncratic and
   enumerating it is not cost-effective `[T2:Horn]`.

And the harshest result in the set: two controlled reader experiments (n=65 plant
operators, n=76) found texts rewritten to Information Mapping's typed structure
produced **no measurable benefit** on either accuracy or speed. The one advantage
was subjective — readers rated the typed version higher while performing no
better `[T2:Jansen2002]`. Typed structure felt superior without being superior.

That is the risk this whole design runs, and it is why §9's evaluation plan leads
with task outcome and explicitly forbids judging by preference.

---

## 2. Recommended taxonomy

Six types, three families, two trust tiers.

| Family (trusted tier) | Type (advisory tier) | Core question |
|---|---|---|
| **Semantic** — what is so | **Concept** | What does this term mean? |
| | **Claim** | What is asserted to be true? |
| | **Model** | How do these things relate, so we can explain or predict? |
| **Procedural** — what to do | **Method** | How do we bring about a goal? |
| | **Rule** | What must, may, or must not happen? |
| **Episodic** — what happened | **Case** | What occurred in this particular instance? |

Four changes from the proposal:

1. **`Declarative` → `Semantic`.** Removes the parent/child collision `[T1-1]`,
   and matches the only machine-agent precedent that uses a co-equal triad
   `[T2:CoALA]`, `[T2:Zep]`.
2. **Family is trusted; type is advisory.** The 3-way family assignment is what
   retrieval filters and lint may rely on. The 6-way type is used for ranking,
   presentation, and lint heuristics, and never as a hard gate without
   confirmation. This is not a new invention — it is the same trust boundary your
   spec already adopted for relationship classification, where a 15-label flat
   vocabulary tested at 0.401 accuracy while the coarse 3-way stance was the tier
   benchmarks validate `[spec §11.3]`. The same shape should govern here for the
   same reason.
3. **Classification is a sequence of binary gates, not one 6-way choice.** See §4.
   Multiclass "choose one of several" labels had **90% lower odds** of correct
   detection than binary present/absent judgments (OR = 0.10, 95% CI 0.03–0.35, 7
   models × 121 features × 567 excerpts), and the binary-vs-multiclass distinction
   was the dominant task-level predictor of success — raising marginal R² from
   3.8% to 22.5% `[T2:arXiv-2601.12099]`. This is the highest-leverage change in
   the document and it costs nothing but prompt structure.
4. **Questions are not a knowledge type.** See §2.1.

### 2.1 Questions and gaps — a node kind, not a type

Karpathy's `lint` operation explicitly wants knowledge gaps and new questions to
investigate `[T2:Karpathy]`, and your spec already carries `open_question` in its
unit ontology `[spec §9.3]`. Neither fits the six types: a question has no truth
value to check, no procedure to execute, and no instance that occurred.

**Recommendation (my judgment, not evidence-backed):** make `question` a
first-class *node kind* alongside `unit`, outside the type system entirely. A
question is an absence of knowledge; putting it inside the taxonomy pollutes
retrieval, because "what do we know about X?" would start returning "we don't
know." Lint owns questions; retrieval ignores them unless asked.

**Flag for you:** this is a design call, and the alternative — a seventh type — is
defensible. I recommend the node-kind version because it keeps the six clean and
gives lint a home.

### 2.2 What about domain-specific needs?

Horn's finding that type sets are domain-scoped `[T2:Horn]` is real, and the way
to honor it without breaking "no domain-specific top-level categories" is the
escape hatch he actually shipped: **the six types are closed; sub-types beneath
them are open.** A trading unit may be `type: method, subtype: entry-signal`; an
onboarding unit may be `type: rule, subtype: access-policy`. Sub-types are
advisory, never used as a retrieval gate, and pruned when unused. Same two-tier
discipline as everything else here.

---

## 3. Type definitions — positive and negative

Every definition below leads with a **surface cue**, deliberately. Label
*abstractness*, not label count, is what drove classification failure in the one
study that measured both: concretely-described features scored F1 > 0.60 for the
best models while features requiring interpretive inference scored F1 < 0.30 — and
LLM performance tracked human inter-coder reliability at r = 0.61, so categories
humans find hard are hard for models too `[T2:arXiv-2601.12099]`. Definitions that
read like philosophy will not be applied consistently.

---

### Concept — *Semantic*

**Cue:** the unit's grammatical center is "X is / means / refers to / is
distinguished from Y."

**Use this when** the unit's job is to fix what a term means, draw a distinction
between terms, or state what category something belongs to — so that later units
can use the word without re-explaining it.

**Do not use this when:**
- the unit asserts something contingent that could turn out false → **Claim**
- the unit explains *why* or *how* something works → **Model**
- the term happens to appear in the title but the unit is doing something else
  with it — a page titled "Sharpe Ratio" whose content is "how to compute it" is
  a **Method**

**Most common confusion:** Concept vs Model. Test — does the unit define *one*
term, or assert a relation among *two or more* things? One term, Concept.

---

### Claim — *Semantic*

**Cue:** a declarative proposition you could imagine checking, and that could
come out false.

**Use this when** the unit asserts that something is the case — a fact, a finding,
a correlation, a prediction, a hypothesis. Epistemic standing (established,
contested, hypothesis, prediction) is **status metadata**, not a different type.

**Do not use this when:**
- the assertion is about a single dated instance → **Case**
- the assertion is nominal or definitional rather than contingent ("CHF is the
  ISO code for Swiss francs") → **Concept**
- the assertion is deontic — must, may, must not → **Rule**
- the unit is an explanatory apparatus rather than one proposition → **Model**

**Claim is the residual type.** It absorbs whatever the other five gates reject.
That is deliberate, but it must be *monitored*: instructing a model what to do
when uncertain measurably biases output toward that escape hatch — the bias comes
from the instruction wording itself, not the content `[T2:arXiv-2605.06940]`. So
never phrase the fallthrough as "if unsure, use Claim." Phrase it as a positive
test, and watch the Claim share (see §9).

---

### Model — *Semantic*

**Cue:** the unit asserts how two or more things relate such that you could
explain or predict something — "because," "leads to," "is composed of," "trades
off against."

**Use this when** the unit carries a mechanism, a causal story, a structure, a
theory, a recurring pattern, or a taxonomy.

**Do not use this when:**
- **the subject is merely *called* a model.** A pricing model, a data model, a
  risk model — the word in the title is not the classifier. Ask what the unit
  *does*, not what it is named. This is the DITA degeneration failure and it is
  the most likely way this type breaks `[T2:EveryPageIsPageOne]`
- the unit is one proposition rather than an apparatus → **Claim**
- the unit tells you what to do with the mechanism → **Method**
- the unit defines a single term → **Concept**

**Most common confusion:** Model vs Method. Test — could you *execute* it? A
mechanism you can only understand is a Model; a mechanism with an entry point and
steps is a Method.

---

### Method — *Procedural*

**Cue:** steps, a decision procedure, a technique, or an imperative with a goal
attached.

**Use this when** the unit tells you how to bring something about — a procedure, a
heuristic, a strategy, a way to decide.

**Do not use this when:**
- the unit constrains rather than instructs — it says what is permitted, not how
  to proceed → **Rule**
- the unit explains why the technique works → **Model**
- the unit records one occasion on which someone did it → **Case**

**Most common confusion:** Method vs Rule. Test — is compliance evaluable? A Rule
can be *violated*; a Method can only be *ineffective*.

---

### Rule — *Procedural*

**Cue:** a deontic modal — must, shall, may, must not, never, always — with
someone accountable to it.

**Use this when** the unit states a requirement, permission, prohibition,
constraint, standard, policy, limit, or governing principle. Rules carry an
**authority** (who set it) and a **scope** (where it binds); if you cannot name
either, reconsider whether it is really a Rule.

**Do not use this when:**
- the unit describes how a system behaves rather than what an actor must do —
  "the API returns 429 above 100 req/min" is a **Claim**; "clients must not exceed
  100 req/min" is a **Rule**. Same underlying reality, different stance, different
  unit. Both may exist and link
- the unit is a technique presented as advice with no accountability → **Method**
- the unit records a specific enforcement event → **Case**

---

### Case — *Episodic*

**Cue:** a specific time and a specific actor or subject. It happened once.

**Use this when** the unit records an event, an observation, an experiment, a
decision, an outcome, an incident, or a worked example bound to a particular
occasion.

**Do not use this when:**
- the unit generalizes beyond the instance → **Claim**
- the unit merely *has a date* — a policy with an effective date is still a
  **Rule**. Test: is the date part of what happened, or just when it started
  applying?
- the unit is a hypothetical illustration rather than something that occurred; a
  made-up example illustrating a definition belongs to the **Concept** it serves

**Note on study findings.** A published result is usually two units: the **Case**
("on this sample, over this period, this was measured") and the **Claim** it
supports ("this generalizes"). Splitting them is what lets contradiction detection
work later — two studies can disagree as Claims while both remaining true as
Cases.

---

## 4. Decision procedure

**Do not present this as a menu.** Present it as six ordered yes/no questions,
first Yes wins. The reason is measured, not stylistic: multiclass single-choice
labeling had 90% lower odds of correct detection than binary judgments, and that
distinction dominated task-level variance `[T2:arXiv-2601.12099]`.

Order runs most-surface-recognizable first, because abstractness predicts failure
`[T2:arXiv-2601.12099]`.

```
Start: one knowledge unit (a decontextualized, minimal statement — spec §9.2)

G1. Does it report something that happened, at a particular time,
    to a particular actor or subject?                            → YES: CASE
                                                                          ↓ no
G2. Does it state an obligation, permission, or prohibition
    that someone is accountable to?
    (cue: must / shall / may / must not / never / always
     + a nameable authority and scope)                           → YES: RULE
                                                                          ↓ no
G3. Does it tell you how to bring about a goal — steps,
    a technique, or a decision procedure you could execute?      → YES: METHOD
                                                                          ↓ no
G4. Is its main job to fix what a term means, or to draw
    a distinction between terms?                                 → YES: CONCEPT
                                                                          ↓ no
G5. Does it assert how two or more things relate, such that
    you could explain or predict something?                      → YES: MODEL
                                                                          ↓ no
G6. Is it a proposition that could be checked and could
    be wrong?                                                    → YES: CLAIM
                                                                          ↓ no
                                                      UNCLASSIFIED → review queue
```

Four rules on top of the gates:

- **Never silently default.** A unit that fails G6 goes to a review queue, not to
  Claim. Silent defaults hide taxonomy failures; an unclassified rate is a health
  metric.
- **Family is derived, not asked.** Once the type is chosen the family follows
  mechanically. Do not ask the model for both — that is a second multiclass
  decision with nothing to gain.
- **Secondary type is a separate, later, optional question**, asked only as "is
  there a second gate this unit also passes cleanly?" It is never used as a
  retrieval gate.
- **If two gates both fire strongly, the unit is probably two units.** Split it.
  That is the molecular rule doing its job `[spec §9.2]`, and it is a better fix
  than a secondary type.

---

## 5. Metadata schema

The schema is split by **purpose**, and this split is the second-most important
recommendation in the document.

A staged ablation over RAG benchmarks found metadata payoff is task-specific and
**not monotonic**: the entire end-to-end gain on a temporal benchmark came from
one layer — temporal validity windows, +0.220 ± 0.008 — while confidence/conflict
metadata and provenance chains added nothing, and full enrichment was net
*negative* on non-temporal benchmarks (MuSiQue −0.032, HotpotQA −0.063)
`[T2:arXiv-2606.29645]`. Worse, prompting models to use confidence scores raised
confidence-citation rate from 14% to 70% while accuracy **dropped** — the model
dutifully selected high-confidence units that were temporally wrong
`[T2:arXiv-2606.29645]`. Compliance with a schema is not evidence the schema
helps.

So: **audit metadata must not travel into the answer path.**

### 5.1 Retrieval-path fields (may enter model context)

```yaml
family:      semantic | procedural | episodic     # trusted tier
type:        concept | claim | model | method | rule | case
subtype:     <free, domain-scoped, advisory>      # optional
scope:       <where this binds / applies>
authority:   <who set it>                          # rules only
t_valid:     2026-01-01T00:00:00Z                  # bi-temporal — spec §11.6
t_invalid:   null
```

`t_valid` / `t_invalid` are already in your spec, adopted from Graphiti/Zep's
invalidate-don't-delete model `[spec §11.6]`. They are also the one enrichment
layer with a measured payoff `[T2:arXiv-2606.29645]`. They earn their place.

### 5.2 Audit-path fields (lint, review, and humans only — never injected)

```yaml
status:                 established | supported | contested | preliminary
                        | internal-observation | operational | authoritative
                        | superseded
origin:                 sourced | observed | inferred | authored | derived
epistemic_confidence:   0.0–1.0    # how sure are we the content is true
classification_conf:    0.0–1.0    # how sure are we the TYPE is right
secondary_type:         <type> | null
maturity:               seed | developing | stable
source_unit_ids:        [...]
provenance_root:        <...>
```

Three notes:

- **`status` reuses your spec's existing knowledge states** `[spec §12]` rather
  than inventing a parallel vocabulary. Adding `superseded` closes the gap left by
  bi-temporal invalidation.
- **Two confidences, never one.** Conflating "we're unsure this is true" with
  "we're unsure what type this is" makes both unusable. They fail independently
  and get consumed by different processes.
- **Self-reported confidence is weakly trustworthy.** Verbalized confidence is not
  a stable model property — its reliability depends primarily on how the model is
  asked, across 17 prompt methods × 10 datasets × models from 2B to 110B
  `[T2:arXiv-2412.14737]`. Treat `classification_conf` as a triage signal for the
  review queue, not as a calibrated probability.

---

## 6. Twenty-four difficult classifications

Chosen to sit on boundaries, not to be easy. `C` = classification confidence.

### Finance and trading

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 1 | "A *golden cross* is when the 50-day moving average crosses above the 200-day." | Concept | — | Semantic | established / sourced | 0.9 | Fixes a term. The *trade* you make on it is a separate Method unit. G4 fires before G5 because the unit defines one term rather than relating two things. |
| 2 | "Momentum persists at 3–12 month horizons because investors underreact to news." | Model | Claim | Semantic | supported / sourced | 0.7 | A mechanism, not a bare assertion — the "because" clause is the unit's payload. Secondary Claim because the persistence itself is separately checkable. |
| 3 | "Jegadeesh & Titman (1993): 12-month momentum returned ~1%/month, US equities, 1965–1989." | Case | Claim | Episodic | established / sourced | 0.6 | Hard one. Bounded to one sample and period → G1 fires. The generalization "momentum works" is a *different* unit this one supports. Splitting is what lets two studies disagree as Claims while both stay true as Cases. |
| 4 | "Never risk more than 2% of account equity on a single trade." | Rule | Method | Procedural | operational / authored | 0.85 | Deontic modal + accountable actor. Compliance is evaluable, so G2 beats G3. |
| 5 | "March 2026: drawdown hit 12% when the momentum and carry books both de-risked into the same liquidity hole." | Case | Model | Episodic | internal-observation / observed | 0.9 | Dated, specific. Secondary Model because it is evidence for a hidden-correlation mechanism that should exist as its own unit. |

### Employee onboarding and organizational knowledge

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 6 | "New engineers get laptop, SSO, and repo access on day one; the hiring manager files the IT ticket." | Method | Rule | Procedural | operational / authored | 0.6 | Genuinely ambiguous. As written it is a procedure (G3). Rewritten as "the hiring manager **must** file the ticket," G2 fires first and it becomes a Rule. Stance decides, not content. |
| 7 | "The deploy freeze runs 20 Dec – 2 Jan." | Rule | — | Procedural | operational / authored | 0.8 | Has dates but is not a Case — the dates are its *scope*, not what happened. This is the trap G1 must not fall into. |
| 8 | "We say *incident* for anything customer-visible and *defect* for anything caught before release." | Concept | — | Semantic | operational / authored | 0.95 | Pure terminological distinction. Org-specific vocabulary is still Concept — the taxonomy is about cognitive function, not about universality. |

### Software development and system design

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 9 | "The scheduler uses a leaky-bucket limiter with a 10 rps refill." | Model | Claim | Semantic | established / sourced | 0.6 | Structural description of how a system fits together (G5). Secondary Claim because it is also a checkable fact about the codebase that can go stale. |
| 10 | "To add a channel, implement `ChannelAdapter` and register it in `channels/index.ts`." | Method | Rule | Procedural | operational / sourced | 0.85 | Steps with a goal. Secondary Rule because registration is mandatory, not advisory. |
| 11 | "Extension code may import only from `openclaw/plugin-sdk/*` and local `api.ts` barrels." | Rule | Model | Procedural | authoritative / sourced | 0.9 | "May only" + a nameable authority. Secondary Model because the constraint encodes the module-boundary architecture. |
| 12 | "2026-04-11: adopted per-change topic branches after two sessions collided on a shared branch." | Case | Rule | Episodic | internal-observation / observed | 0.7 | An ADR is a dated decision — G1. It *generates* a Rule, which should be a separate linked unit. Do not fuse them: the Rule outlives the incident and must be retrievable without it. |
| 13 | "CAP: a partitioned system must choose between availability and consistency." | Model | Claim | Semantic | established / sourced | 0.55 | Hardest in the set. The word "must" tempts G2, but there is no accountable actor — it is a tradeoff structure, not an obligation. G2's authority-and-scope test is what saves this. |

### Fact-oriented reference material

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 14 | "Python 3.12 removed `distutils`." | Claim | — | Semantic | established / sourced | 0.85 | Contingent, checkable, could have been otherwise. `t_valid` from the 3.12 release date. |
| 15 | "The ISO 4217 code for the Swiss franc is CHF." | Concept | Claim | Semantic | authoritative / sourced | 0.5 | Deliberately contentious. It reads like a fact but functions as a naming convention — it fixes what a symbol means. Expect models to split on this one; it is a good gold-set item precisely because it is a coin flip. |

### Brainstorming and idea development

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 16 | "What if lint emitted a weekly contradiction digest instead of blocking?" | Method | — | Procedural | preliminary / authored | 0.5 | Under §2.1's recommendation this is better stored as `kind: question`. If kept as a unit, it is a proposed procedure — the status carries the tentativeness, not the type. Exactly the proposal's own design principle working. |
| 17 | "Maybe onboarding friction and incident rate are two faces of one undocumented-tribal-knowledge problem." | Model | Claim | Semantic | preliminary / inferred | 0.5 | A proposed mechanism linking two things. `status: preliminary` + `origin: inferred` is what makes it a hunch rather than a finding — no separate "hypothesis" type needed. |
| 18 | "None of the agent-memory papers show typing helping simple lookup." | Claim | Model | Semantic | supported / derived | 0.7 | A checkable proposition *about a literature*. Meta-level content is still ordinary Claim. |

### Oracle-style cross-domain analysis

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 19 | "Firms with public changelogs have lower support load; changelogs pre-answer the top 20% of tickets." | Claim | Model | Semantic | preliminary / inferred | 0.4 | **This is two units fused** — a correlation (Claim) and a mechanism (Model). Low classification confidence is the correct signal. The right action is a split, not a secondary type. |
| 20 | "Across trading drawdowns, incident postmortems, and onboarding churn, the common precursor is an undocumented dependency." | Model | Claim | Semantic | preliminary / inferred | 0.6 | The canonical "insight." Note it needs no `insight` type — `model` + `proposed`/`inferred` + medium confidence captures it exactly, which vindicates the proposal's central design principle. |
| 21 | "Every time we added a governance box, quota draw rose faster than the gate anticipated." | Claim | Model | Semantic | supported / observed | 0.6 | Generalizes over several dated events, so G1 does *not* fire — the individual incidents are the Cases; this is the pattern they support. |

### Cross-cutting hard cases

| # | Unit | Primary | Secondary | Family | Status / Origin | C | Rationale |
|---|---|---|---|---|---|---|---|
| 22 | "Our API returns 429 above 100 req/min." | Claim | Rule | Semantic | established / sourced | 0.5 | Describes behavior → Claim. "Clients must not exceed 100 req/min" is the *same reality* as a Rule. Both units should exist and link. Stance decides. |
| 23 | "Postmortem: the outage was caused by a stale DNS cache." | Case | Claim | Episodic | internal-observation / observed | 0.8 | Dated singular event. The causal attribution is a Claim the Case carries. |
| 24 | "Prefer small reversible steps." | Rule | Method | Procedural | operational / authored | 0.55 | A principle with no modal verb and no explicit authority. G2's cue test fails but its *function* is normative. Borderline by construction — good gold-set item for testing whether models classify by cue or by function. |

Note the confidence distribution: seven items sit at ≤ 0.6. That is the honest
shape. A taxonomy whose hard cases all score 0.9 has not been stress-tested.

---

## 7. Mixed pages and relationships

### 7.1 Mixed pages

Do not fight Karpathy's page model. His pages are topic-shaped — an entity page, a
concept page, a comparison — and that is the right unit for a human reading in
Obsidian `[T2:Karpathy]`. Forcing one type per page recreates precisely the DITA
failure where content gets shredded to fit the type system `[T2:EveryPageIsPageOne]`.

**Type lives on the block, not the page.**

A page on the Kelly criterion legitimately contains four units: a **Concept**
(what it is), a **Model** (why it maximizes log growth), a **Method** (how to size
a position), and a **Rule** (never exceed half-Kelly). One page, four typed units,
four different retrieval behaviors.

Concretely:

```markdown
---
title: Kelly criterion
primary_family: semantic          # for the index only — the page's center of gravity
unit_types: {concept: 1, model: 1, method: 1, rule: 1}
---

## What it is
<!-- unit: concept | c=0.9 -->
...

## Why it maximizes long-run growth
<!-- unit: model | c=0.8 -->
...
```

`primary_family` is for `index.md` navigation and nothing else. Never use it as a
retrieval filter — that reintroduces the whole-page forcing you just avoided.

Baker's second critique applies here too: a typing scheme that only says how to
break content apart, without saying how the pieces reassemble, produces incoherent
fragment collections `[T2:EveryPageIsPageOne]`. The page *is* the reassembly. That
is why the page stays topic-shaped.

**Pages that are pure navigation** — indexes, link lists, MOCs — carry no type.
They are not knowledge units.

### 7.2 Relationships

Same two-tier discipline, for the same measured reason `[spec §11.3]`.

**Trusted coarse set** (safe to act on): `supports`, `contradicts`,
`insufficient_evidence`, `relates`.

**Advisory typed set** (for presentation and lint heuristics; carries its own
confidence, never determinative):

| Link | Typical direction | Meaning |
|---|---|---|
| `defines` | Concept → any | fixes a term the target uses |
| `evidences` | Case → Claim | this instance is evidence for the generalization |
| `instantiates` | Case → Model | this instance is the mechanism playing out |
| `implements` | Method → Model | this procedure operationalizes the mechanism |
| `constrains` | Rule → Method | this rule bounds how the method may be applied |
| `specializes` | any → same type | narrower version of a broader unit |
| `supersedes` | any → same type | replaces, paired with `t_invalid` on the target |

The type pair is a cheap, high-precision way to *generate contradiction
candidates*: Claim × Claim on the same subject, Rule × Rule on the same scope,
Case × Claim where the case cuts against the generalization. That matters because
of the strongest measured result on this question — see §8.

---

## 8. What typing will and will not buy you

Stating this plainly matters, because the failure mode in this literature is a
typed structure that feels better without being better `[T2:Jansen2002]`.

**Where the evidence says typing helps:**

- **Contradiction surfacing, but only if you ask explicitly.** On WikiContradict's
  253 human-annotated contradictory pairs, seven LLMs given two conflicting
  passages surfaced the conflict just 2–10% of the time under a plain prompt
  (Mistral-7B 2.1%, Llama-3-70B 10.4%) — while answering correctly 87.8–97.6% on
  single non-conflicting passages. Explicitly instructing the model to attend to
  contradictions took Llama-3-70B from 10.4% to 43.8% `[T2:WikiContradict]`. Your
  spec reached the same conclusion from a different literature: never ask
  open-endedly whether a cluster contains contradictions; always present retrieved
  candidate pairs `[spec §11.2]`. Typing is how you build those pairs cheaply.
- **Cross-session and temporal synthesis.** Zep's typed graph memory beat flat
  full-context retrieval on LongMemEval by up to 18.5% accuracy while cutting
  latency ~90% and context from ~115k to ~1.6k tokens — with gains concentrated in
  multi-session (44.3% → 57.9%) and temporal reasoning (45.1% → 62.4%), not
  uniform `[T2:Zep]`.
- **Multi-hop composition.** A-MEM's ablation drops Multi-Hop F1 from 27.02 to
  9.65 when link generation and memory evolution are removed `[T2:A-MEM]`.
- **Analytical, comparative and predictive queries.** SRAG's structured metadata
  tagging raised judge scores on predictive (64.5 → 95.6), analytical (65.1 →
  93.8) and comparative (55.9 → 94.1) queries `[T2:SRAG]`. This is your "oracle"
  use case, and it is the strongest positive signal in the set.

**Where the evidence says typing does nothing or hurts:**

- **Simple fact lookup.** SRAG's gain was *absent* there — plain RAG 98.37 vs SRAG
  97.43, p = 0.24, a statistically insignificant slight decrease `[T2:SRAG]`.
- **Structure for its own sake.** Converting retrieved passages into structured
  atomic JSON records with no added metadata content *reduced* accuracy on every
  benchmark tested except FEVER `[T2:arXiv-2606.29645]`.
- **Graph typing on simple retrieval.** Mem0-graph gained only ~2% overall on
  LOCOMO and *hurt* two of four categories — single-hop 67.13 → 65.71, multi-hop
  51.15 → 47.19 `[T2:Mem0]`. A-MEM likewise lost to flat baselines on Open Domain
  and Adversarial questions `[T2:A-MEM]`.
- **Implicit contradictions.** Even with explicit prompting, implicit-conflict
  accuracy moved only 5.9% → 17.6% `[T2:WikiContradict]`. Expect lint to catch
  restated-fact clashes and largely miss reasoning-dependent inconsistencies.

**The honest summary:** this taxonomy buys reasoning-heavy synthesis across many
units. It buys nothing for recall, and it can cost you if you over-structure. Size
the investment accordingly.

---

## 9. Cross-model evaluation plan

Five phases. Phases 0–1 are cheap and should run before any of this ships; phase 4
is the only one that decides whether the taxonomy is worth keeping.

### Phase 0 — Human gold set (the ceiling)

300 units, ~35 per domain across the eight named domains, sampled from real
sources rather than written for the test. Two human coders, independent, then
adjudication. **Report human–human Krippendorff's α first.** Without it the model
numbers mean nothing — Larsen's expert coders reached only Fleiss κ 0.68 on a
4-label knowledge dimension *before* consensus discussion `[T1-6]`, and Bloom's
poor inter-rater reliability survived targeted training and replicated across an
independent cohort `[T1-5]`. If your humans cannot clear ~0.7 at the type level,
fix the definitions before testing any model.

### Phase 1 — Cross-model application

At least five models: three frontier (one each from Anthropic, OpenAI, Google) and
two open-weight in the 7–14B band.

| Metric | Why | Reference point |
|---|---|---|
| Family-level α (3-way) | The trusted tier | must exceed type-level |
| Type-level α (6-way) | The advisory tier | expect materially lower |
| Pairwise LLM–LLM κ | The cross-family question directly | mean 0.23 vs human–human 0.57 `[T2:arXiv-2601.12099]` |
| Per-label confusion | Locates the weak boundaries | expect Model↔Claim, Method↔Rule |
| Residual (Claim) share | Escape-hatch over-absorption | investigate above ~40% `[T2:arXiv-2605.06940]` |
| Unclassified rate | Gate coverage | rising rate = definitions drifting |
| Label-order flip rate | Position bias | your spec expects 17–22% `[spec §21]` |
| JSON validity, **separately** from semantic correctness | They fail independently | 7–9B models hit 85% task accuracy with **0%** valid JSON `[T2:arXiv-2605.02363]` |

Two hard warnings for this phase:

- **Do not validate by cross-model agreement.** Four frontier models once reached
  near-total surface agreement on sarcasm with Fleiss κ ≈ −0.001 — agreement was
  an artifact of shared fallback-label behavior, not shared understanding
  `[T2:arXiv-2605.06940]`. Agreement without a gold set proves nothing.
- **Expect small open models to fail at the type tier.** Llama 3.2 3B and Qwen3 4B
  scored F1 < 0.25 with false-positive rates above 98% and frequent invalid output
  `[T2:arXiv-2601.12099]`. Plan for them to run the family tier only, and to be
  driven by per-model optimized prompts — an iterative prompt optimizer reached
  84–87% structured-output accuracy on 7–9B models where a shared hand-written
  prompt got 0% `[T2:arXiv-2605.02363]`. Constrained decoding is not a free
  substitute: it guarantees syntax but cost 3.6–8.2× latency and, in one case,
  drove Gemma 2-9B to 52.4% duplicate outputs and 15.3% accuracy
  `[T2:arXiv-2605.02363]`.

### Phase 2 — The two structural bets

Same models, same items, three arms:

- **A:** one 6-way multiclass choice
- **B:** six ordered binary gates (§4)
- **C:** family-only (3-way)

B > A is the prediction the OR = 0.10 finding makes `[T2:arXiv-2601.12099]`. C > B
at the family level is the prediction the two-tier trust boundary makes. If B does
not beat A, drop the gates and simplify. If C does not beat B, the family tier is
not buying trust and can be collapsed.

### Phase 3 — Is status really orthogonal to type?

Fisher's exact test on the type × status contingency table over a few hundred
classified units. This is a direct replication of Larsen et al., whose "orthogonal"
second dimension measured as statistically dependent on the first (p < 0.0001),
with items collapsing into three dominant clusters `[T1-6]`.

Expect a few cells to absorb most units. If `hypothesis` collapses onto Claim and
`preliminary` collapses onto Model, the status axis is carrying less information
than the design assumes — which is a reason to shrink the vocabulary, not to drop
the axis. Larsen's own authors kept both dimensions `[T1-6]`.

### Phase 4 — Does it change any answer? (the decisive test)

A held-out query set, ~120 questions, split four ways: **lookup**, **comparative**,
**analytical**, **temporal**. Two arms — type-filtered retrieval vs the plain
hybrid baseline your spec already runs `[spec §10.3]`.

Predicted from the evidence: no gain on lookup, real gain on comparative and
analytical, largest gain on temporal `[T2:SRAG]`, `[T2:Zep]`. If you get that
shape, the taxonomy works. Plus contradiction recall with type-paired candidates
vs untyped pairing, measuring **recall not precision** — missed contradictions are
the dominant failure mode `[spec §11.4]`.

**Kill criterion, agreed in advance.** If Phase 4 shows no gain on any query class,
the taxonomy is decoration. Keep `t_valid`/`t_invalid` — the one metadata layer
with a measured payoff `[T2:arXiv-2606.29645]` — and drop the rest. This clause
exists because of Information Mapping: two controlled experiments, no measurable
benefit, and readers who *preferred* the typed version anyway `[T2:Jansen2002]`.
Judge on task outcome. Never on preference, and never on how coherent the schema
feels.

---

## 10. Changes to the wiki architecture

Mapped onto Karpathy's three layers and three operations `[T2:Karpathy]`.

### Layer 3 — the schema file (`CLAUDE.md` / `AGENTS.md`)

This is where the taxonomy lives, and the format matters more than the content.

- **Pin every definition with its negative definition and two exemplars.** Not
  optional. The same label names carry incompatible content across authors — one
  standard framework defines "procedural knowledge" as knowing how to use
  strategies while another redefines it as task knowledge and moves strategy into
  declarative. Identical three-label sets are not interoperable without pinned
  definitions and examples. Definitions must be surface-recognizable, because
  abstractness predicted classification failure more strongly than count
  `[T2:arXiv-2601.12099]`.
- **State the justification honestly.** "These categories have different write,
  update, and retrieval rules" — not "these are how the brain works." The
  cognitive warrant does not transfer `[T1-4]`.
- **Ship the binary gates verbatim** as the classification procedure, not the
  table of types.

### Layer 2 — the wiki

- **`index.md` gains `family` and `type` columns.** At the scale Karpathy
  describes, the index *is* the type-filtered retrieval mechanism — no embedding
  infrastructure needed. Treat his ~100-source threshold as an untested assumption:
  it is stated as personal experience with no benchmark and no measured retrieval
  accuracy `[T2:Karpathy]`.
- **Units are marked in-page**, page frontmatter carries the aggregate. Dataview
  can then query by type without any custom tooling.
- **`log.md` records classification and reclassification events.** A unit that
  gets reclassified is a signal the definitions are weak at that boundary — that
  log becomes your cheapest ongoing quality metric.

### Operation — Ingest

Classify during extraction, at unit granularity, inside Pass 1 — not as a separate
pass. Granularity is the primary lever on memory quality; the label set is
secondary `[T2:EMem]`. Your spec's molecular rule already governs this
`[spec §9.2]`; the taxonomy rides on top of it.

Replace the flat 20-label unit ontology in `[spec §9.3]` with `family` + `type` +
open `subtype`. The current list mixes levels badly — `fact`, `claim`,
`definition`, `quantitative_result`, `null_result`, `study_design`, `method`,
`decision`, `obligation`, `prohibition`, `exception`, `deadline`, `dependency`,
`risk`, `limitation`, `contradiction`, `recommendation`, `open_question`,
`observation`, `metadata` — several are types, several are statuses, several are
relationships, and one (`metadata`) is not knowledge at all. Most map cleanly:
`obligation`/`prohibition`/`deadline` → Rule; `decision`/`observation`/
`study_design` → Case; `definition` → Concept; `fact`/`quantitative_result`/
`null_result` → Claim; `method`/`recommendation` → Method; `contradiction` →
a relationship, not a type; `open_question` → a question node (§2.1); `metadata`
→ drop.

### Operation — Query

Route by **family**, never by type alone. And set expectations honestly in the
schema file: typing helps analytical, comparative, and temporal questions, and
does nothing for fact lookup `[T2:SRAG]`.

### Operation — Lint

This is where typing pays for itself. Five checks:

1. **Type-paired contradiction candidates** — Claim × Claim on a shared subject,
   Rule × Rule on a shared scope, Case × Claim where the instance cuts against
   the generalization. Always present the *pair* and ask explicitly; never ask
   open-endedly `[T2:WikiContradict]`, `[spec §11.2]`.
2. **Orphan checks** — a Model with no supporting Claims or Cases; a Method with
   no Case showing it was ever used; a Rule with no authority.
3. **Dead-label check** — a type never assigned is a type to prune. Larsen's
   `Metacognitive` category was assigned to **zero** of 940 items; a category can
   be theoretically well-motivated and empirically dead `[T1-6]`.
4. **Residual-share check** — Claim share above ~40% means the upstream gates are
   too narrow, or the escape hatch is over-absorbing `[T2:arXiv-2605.06940]`.
5. **Staleness** — units whose `t_valid` window has closed but that nothing has
   superseded.

---

## 11. Open questions for you

1. **Questions as a node kind, or a seventh type?** §2.1. I recommend node kind;
   the alternative is defensible and it is your call.
2. **Is `Models` the right name**, given it will be applied to pages whose subject
   is literally called a model? I kept it because common words carry better priors
   in small models, and paid for that with a hard negative definition. If it
   confuses in practice, the rename to consider is `Mechanisms`.
3. **How much domain sub-typing to allow** before it becomes the domain-specific
   top-level taxonomy you set out to avoid. Horn's answer was ~40 sub-types
   covering 80%, plus criteria for inventing more `[T2:Horn]`. That is a lot of
   vocabulary.
4. **Does the wiki share the ingestion pipeline's storage**, or is it a separate
   markdown-and-git artifact in Karpathy's sense that the pipeline feeds? This
   changes where classification happens and I do not have enough from you to
   decide it.

---

## 12. Evidence honesty statement

Of the ten questions in the brief, the ones about cognitive-science support are
answered from adversarially verified findings. The ones that actually determine
whether this design *works* — cross-model reliability, retrieval payoff,
contradiction detection, prior-art outcomes — are answered from Tier 2 sources
read once and not challenged.

Nothing in this document should be described to anyone as literature-backed
without that distinction. The parts that are pure engineering judgment —
sub-page granularity, one primary plus optional secondary, classification
confidence, status as metadata — currently rest on **zero verified external
support in either direction** `[T1-8]`. They are reasonable. They are not
findings. The evaluation plan in §9 exists to convert them into one or the other.
