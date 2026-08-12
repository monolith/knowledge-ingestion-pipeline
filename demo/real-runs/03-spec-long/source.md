# Statement Classifier — Specification v1.0

Assigns a knowledge type to a short statement. One statement in, one
classification record out. Works on statements extracted from documents and on
statements taken from conversation.

**Current measured reliability.** Inter-rater Krippendorff α, eight blind raters,
codebook verbatim, no answer key in existence:

| corpus | α |
|---|---|
| 160 statements from eight generated sources | **0.934** |
| 85 statements from three published documents | **0.894** |
| `form` field | **1.000** |
| `status` field | 0.861–0.906 |
| `scope` field | 0.799–0.940 |

For scale: the argumentative-zoning scheme reached κ 0.71 with seven categories
and a 111-page codebook; CoreSC reached 0.50–0.57 with eleven. This taxonomy has
fifteen labels. Full method and caveats in §9 and in
`research/2026-08-11-definition-pass.md`.

**Evidence convention.** Every claim marked `[VERIFIED]` survived three-vote
adversarial verification against a primary source; the study, the number, and
the sample are named inline. Claims marked `[MEASURED]` come from the in-house
runs in `research/`, which measured this codebook rather than a published one.
Claims marked `[DESIGN]` are engineering decisions with no supporting
measurement — they are labelled that way deliberately, and §9 lists every one of
them in a single place. Nothing here is presented as evidence-backed unless a
number is attached to it.

The research this cites ships in `research/`.

---

## 1. Contract

```
classify(statement: str, context?: str) -> Classification
```

**Input.** One statement, plus the surrounding context it appeared in. The
context is used to **classify that statement** — a line is often only readable
against what came before it — but never to reclassify the neighbours themselves.
One statement in, one record out.

`[DESIGN]` This reverses an earlier restriction that limited context to pronoun
and ellipsis resolution. Several statements measured as unclassifiable in
isolation are unambiguous in place, and no evidence was found either way on how
much context a conversational statement needs (§6).

**Output.** A classification record:

```json
{
  "statement_sha256": "…",
  "fine": "observation",
  "coarse": "case",
  "tests": {"is_observation": true, "is_result": false, "…": false},
  "tests_fired": 1,
  "multi_fire": false,
  "status": "evidenced",
  "form": "statement",
  "modality": null,
  "flags": ["negative_result"],
  "provenance": {"medium": "chat", "author": "human", "source_id": "…"},
  "taxonomy_version": "sc-v1",
  "prompt_version": "sc-v1-classify-0001",
  "classifier_model": "<model id>",
  "classified_at": "2026-08-10T00:00:00Z"
}
```

**Append, never overwrite.** A classification is a pure function of
`(statement, prompt_version, classifier_model)`. Re-running with a different
triple appends a new record; it does not replace the old one. Consumers pick
the record whose stamps they trust.

**The classifier does not judge truth.** It answers "what kind of statement is
this", never "is this correct". Epistemic status lives elsewhere.

---

## 2. The taxonomy

Five coarse types. Fifteen fine labels, each mapping to exactly one coarse
type. The mapping is a lookup table, not a judgment.

### 2.1 Coarse types

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `method` | What is done, required, forbidden, advised, or settled? |
| `concept` | What does this term mean? |
| `model` | Why does this hold, what does it rest on, and how is it computed? |
| `system` | What is the thing built from, and what does it need to run? |
| `general` | — assigned by code when no test fires |

### 2.2 Fine labels, with measured reliability where it exists

Each fine label is anchored, where possible, on a category that has a published
inter-annotator agreement figure. `κ` below is the measured agreement for the
*anchor* category in the cited scheme — not for this label as written here.

| Fine label | Coarse | Anchor κ | Anchored on |
|---|---|---|---|
| `observation` | case | **0.79** | CoreSC `Observation` [VERIFIED] |
| `event` | case | — | [DESIGN] — concrete by construction (actor + time) |
| `obligation` | method | — | [DESIGN] — deontic modal is a surface cue |
| `prohibition` | method | — | [DESIGN] — deontic modal is a surface cue |
| `decision` | method | — | [DESIGN] — a settled choice governs what happens next; note it is the one `rule` label with NO deontic modal to key on (§3.3) |
| `procedure` | method | **0.74** | CoreSC `Method` [VERIFIED] |
| `recommendation` | method | — | [DESIGN] |
| `definition` | concept | **0.81** | CoreSC `Object` [VERIFIED] |
| `distinction` | concept | — | [DESIGN] |
| `background` | concept | **0.87** | CoreSC `Background` [VERIFIED] |
| `principle` | model | — | [DESIGN] — the causal idea the model runs on; carries `status` (§2.6) |
| `architecture` | system | — | [DESIGN] — compositional cue (*is composed of*) |
| `formula` | model | — | [DESIGN] — an equation is the most surface-detectable cue in the set |
| `assumption` | model | — | [DESIGN] — marker words (*assumes*, *conditional on*) |
| `dependency` | system | — | [DESIGN] — marker words (*requires*, *depends on*) |

Source for all CoreSC figures: Liakata et al., LREC 2010, per-category
one-vs-rest Cohen's κ, 41 chemistry/biochemistry papers, expert annotators.
AZ-II: Teufel et al., EMNLP 2009, 15 categories, three annotators, N=3745.
Both in `research/2026-08-10-annotation-taxonomy-research-runA.md`.

### 2.3 What the reliability spread means for this design

`[VERIFIED]` Within a single annotation scheme, per-category reliability varies
by a factor of two, and the abstract categories are systematically the worst:
CoreSC measured `Conclusion` 0.89, `Background` 0.87, `Object` 0.81,
`Observation` 0.79, `Result` 0.78, `Method` 0.74 — against `Hypothesis` 0.46,
`Motivation` 0.46, `Model` 0.43.

Three consequences, all binding on this spec:

1. The `model` coarse type is the known weak point. Its anchor is the lowest
   measured category in the scheme. §3 therefore defines `principle` primarily as
   a surface test — does the statement contain a causal or structural connective
   linking two named things — rather than as a judgment about explanatory intent.
   `[MEASURED]` This was tested directly. A non-surface criterion — the
   **generality test**, asking whether a causal claim outlives the occasion it
   describes — was written for `principle` and measured *worse* than the surface
   definition it replaced (§2.9). The prediction above held on this codebook,
   on the label the prediction named.
2. Any category that cannot be written as a surface test should be expected to
   land near 0.45 regardless of codebook quality.
3. Per-category agreement must be reported separately in evaluation. A single
   aggregate number hides exactly the failure this spread predicts.

### 2.4 `general`

`general` is assigned **by code**. It is never offered as a label, never named
in the prompt, and has no definition the model can see.

`[VERIFIED]` A **named** fallback given to the model is catastrophic: four
frontier models given one plus "assign it for unknown cases" recorded 96.1%
agreement with Fleiss κ **−0.001** and identified the minority class zero times
(MultiSoc-4D, 58k+ comments). Whatever triggers `general`, the model must not
see it.

`[MEASURED]` **Self-reported confidence does not work as the trigger, and this
was tested directly.** Raters scored all fifteen labels 0–100 on the full
corpus; code then assigned `general` when no label cleared a bar, or when
several did:

| rule | α | share sent to `general` |
|---|---|---|
| pick one label directly | **0.934** | — |
| score all fifteen, take the highest | 0.930 | 0% |
| margin ≥ 5 between first and second | 0.893 | 4% |
| margin ≥ 20 | 0.866 | 25% |
| absolute threshold 75 | 0.892 | 42% |
| **absolute threshold 90** | **0.605** | **86%** |
| absolute threshold 95 | 0.140 | 99% |

Two findings. **The ordering is sound** — argmax over the scores reaches 0.930,
statistically level with asking for one label. **Every abstention rule loses.**

`[MEASURED]` The reason is not miscalibration. **Raters disagree about their own
uncertainty more than they disagree about the label.** Eight raters can all pick
`procedure` and score it 95, 88, 72, 91, 60, 85, 78, 93; under any threshold
some abstain and some do not, so a statement they *unanimously agreed on*
becomes a disagreement between `procedure` and `general`. Abstention does not
filter noise — it manufactures it, by adding a second judgement noisier than the
first.

This is the third measured instance of the same pattern, after booleans plus
priority resolution (−0.092, §4.1) and interior tiers (−0.11,
`research/2026-08-11-instrument-bakeoff.md`). **Anything that turns one
classification decision into two costs more in the second step than it gains in
the first.**

`[DESIGN]` `general` is therefore triggered by **disagreement across runs**, not
by self-report: classify a statement more than once and, where the runs
disagree, assign `general`. That reads the same signal the confidence rule was
after — nothing fits cleanly — from a source that is not self-assessment. The
number of runs and the disagreement rule are evaluation parameters (§7) and are
not yet measured.

`general`'s share of the corpus is a standing health metric (§7).

### 2.5 What was cut, and the two gaps it leaves

`[MEASURED]` Four labels were removed after the collision test
(`research/2026-08-10-codebook-collision-test.md`):

- `conclusion` merged into `finding`. They were the worst-colliding pair in the
  set (11 co-occurrences; α 0.607 and 0.680) and the measured-versus-inferred
  distinction between them did not survive contact with real statements.
- `study`, `permission`, `tradeoff` dropped as not carrying their weight for this
  corpus. Note honestly: all three also drew **zero** assignments in the test, but
  that was an item-set coverage gap, so the test did not independently show them
  to be weak — the decision is editorial.
- `event` retained deliberately, for historical recording, despite also drawing
  zero assignments for the same coverage reason.

Two gaps this leaves, both routed to `general`:

1. **`model` now has exactly one fine label.** For that branch the fine and
   coarse tiers carry identical information — a degenerate tier, harmless but
   worth knowing. (Superseded: `model` now carries five labels — see §2.7.)
2. **Permission-shaped statements have no home.** "Analysts may exceed the
   intraday limit provided the book is flat at close" carries a deontic modal but
   is neither required nor prohibited. It will land in `general`, or be pulled
   into `obligation` by the modal. Watch `general`'s share for permission-heavy
   corpora such as policy documents.

`[DESIGN]` Merging `conclusion` into `finding` cuts against the other change in
this revision — `finding` already took 24% of all assignments and was behaving
as a de-facto residual, and widening it increases that risk. The merged
definition below therefore tightens its exclusions against `fact` and
`observation` rather than loosening them. Whether that holds is a re-test, not a
claim.

### 2.6 `status`, and why `claim` no longer exists

`[DESIGN]` §1 says this classifier does not judge truth and that epistemic
status lives elsewhere. An earlier revision nonetheless had a `claim` coarse type
whose three labels — `fact`, `finding`, `proposition` — differed mainly by *how
established* a statement was. That contradicted the contract.

They are now one field, carried by **every** type:

```
status: floated | proposed | evidenced | settled
```

- `floated` — a point raised without being worked out. To act on it you would
  have to invent the details yourself. *"what if we looked at parking-lot
  traffic for the retail names"*
- `proposed` — one approach, specified enough to build or test. Nothing has
  validated it. *"weight each name by lot occupancy normalised to store
  footprint, rebalanced weekly"*
- `evidenced` — something backs it, and the backing is what makes it hold.
  *"the lot-count signal held up out of sample, 0.41 Sharpe net"*
- `settled` — indisputable. Not the kind of thing the next study overturns.
  *"Sharpe ratio is excess return divided by standard deviation"*

Each rung adds a different thing: `floated` puts a point on the table,
`proposed` adds **specification**, `evidenced` adds **evidence**, `settled` adds
**certainty**. The test that separates the first two is the one used throughout
this codebook — *could you act on this sentence as written, or would you first
have to invent the parameters?*

`[MEASURED]` The ladder was tested on 160 fresh statements from eight sources
with four blind raters
(`research/2026-08-11-status-ladder-test.md`). It reaches **α 0.896**, higher
than the type taxonomy scores on the same items (0.877). Per rung: `floated`
0.938, `settled` 0.914, `evidenced` 0.906, `proposed` 0.851.

`[MEASURED]` **`floated` and `proposed` separate cleanly** — 2 disagreeing
rater-pairs, the *least* confused pair in the ladder. This was predicted to be
the weak boundary, on the reasoning that both are hedged and differ only by
degree of specification. The prediction was wrong. Merging them changes α by
+0.001, so the fourth rung costs nothing and buys resolution. The real trouble
is at the top: `evidenced`/`settled` 21 and `evidenced`/`proposed` 20.

The gain is that an idea's lifecycle stops being a retyping. "More cars in the
lot predicts stronger same-store sales" begins as `floated`, becomes `proposed`
once it names its parameters, `evidenced` when the backtest holds, and may
harden to `settled`. As separate types that path required changing what the
statement *is*; as a status it is an update, which is what actually happens —
and it makes "show me every principle still at `proposed`" a query rather than
an archaeology exercise.

`[MEASURED]` **Asking for status does not cost type agreement — it improves
it.** On the same 160 items, raters asked for type alone reached fine α 0.841;
raters asked for type *and* status reached **0.877** (coarse 0.840 → 0.896).
This was the main risk in the two-field design and it inverted. The likely
mechanism, unproven: with nowhere to record how established a statement is,
raters were folding that judgment into the type choice; given a field for it,
the type decision gets cleaner. It is the largest effect of its kind measured
here, but four raters and no confidence intervals — treat the direction as more
solid than the magnitude.

`[MEASURED]` **Status is not a restatement of type, but its value is
concentrated.** The published two-axis design this spec cites failed because its
axes turned out statistically dependent and collapsed into a few cells, so the
same test was run here: Cramér's V = 0.595, mutual information 0.845 of 1.721
bits — **49% of status is predictable from type, 51% is not**. Dependent, not
collapsed.

Where the independent half lives, measured as residual entropy of status given
type:

| type | n | bits | reading |
|---|---|---|---|
| `dependency` | 7 | 1.84 | status carries almost everything |
| `procedure` | 48 | 1.74 | |
| `recommendation` | 94 | 1.73 | |
| `principle` | 44 | 1.72 | |
| `architecture` | 18 | 1.53 | |
| `distinction` | 9 | 1.39 | |
| `decision` | 29 | 1.18 | |
| `event` | 43 | 0.82 | |
| `background` | 35 | 0.50 | |
| `observation` | 196 | 0.19 | 97% `evidenced` — near-redundant |
| `definition` | 40 | **0.00** | 100% `settled` — carries nothing |

`status` earns its place exactly where you would want it — on proposals,
approaches, and causal claims. On `definition` it is a constant. That is an
argument for scoping the field rather than dropping it, and it is not yet acted
on: v1 asks for status on every type, and the cost of asking is the 0% `n/a`
rate below rather than any measured loss.

`[MEASURED]` **`n/a` is nearly unused: 9 of 640 (1.4%).** Status applies to
almost every statement raters saw, including rules and events. The one exception
is `general`, where half the assignments were `n/a` — consistent with `general`
being a residual rather than a kind.

`[DESIGN]` **Provenance is a separate field and is not classified.** Where a
record came from — chat or document, human or model, which thread — is known at
ingestion. Recording it costs no agreement because nobody infers it. It is *not*
`status`'s job: status says how firmly a statement is held now, provenance says
where it was born. Both are worth having; only one of them can be got wrong.

**`[MEASURED]` Known gap, and it is worse than predicted.** A measured result
that drives nothing — "the signal earned 0.82 Sharpe net of costs over the full
sample" — has no obvious home now. `claim`/`finding` was where it used to go.
This was expected to fall to `general`; the control run shows it does not.
Raters do not reach for the escape hatch (0 of 288). They split, 37 disagreeing
rater-pairs between `observation` and `principle`, the largest collision
measured in any run — and on a research corpus these statements are roughly a
quarter of the text. So `general`'s share is **not** the metric that surfaces
this. Fine-tier α on a results-dense corpus is. See §2.7 and
`research/2026-08-10-codebook-collision-control.md`.

### 2.7 What the second collision test changed

`[MEASURED]` The restructure in §2.5–2.6 was re-tested on 80 fresh statements
with four blind raters
(`research/2026-08-10-codebook-collision-test-v2.md`). Agreement rose on both
tiers: fine α 0.778 → **0.858**, coarse α 0.866 → **0.927**, unanimity 0.67 →
0.78. No statement fell outside the taxonomy (0 of 320).

**`[MEASURED]` That comparison was confounded, and a control says the gain was
not the taxonomy.** The first test and the second used *different item sets*, so
the headline moved for two reasons at once. Re-running the first test's 72 items
through the second codebook holds the items fixed and isolates the taxonomy
(`research/2026-08-10-codebook-collision-control.md`):

| | fine α | coarse α |
|---|---|---|
| headline, v1 → v2 (taxonomy **and** items changed) | +0.080 | +0.061 |
| **taxonomy alone** (v1 items, both codebooks) | **+0.009** | **−0.075** |
| item set alone (v2 codebook, both item sets) | +0.071 | +0.136 |

The restructure bought approximately nothing on a fixed item set, and *lost*
ground at the coarse tier. The claim that dissolving `claim` "cost nothing" was
read off the second item set, which happens to contain few of the statements
that make it costly. On the first item set the cost is plain: `principle` and
`observation` disagreed on **37** rater pairs, the largest collision in any test
so far, concentrated entirely on empirical research results — sentences that
report a measurement *in order to* assert a generalization. `claim`/`finding`
had absorbed those. With it gone they scatter across two coarse types.

`[DESIGN]` The response is a mechanical tie-break rather than a restored label:
the **strip test** in §3.2 assigns a measured result to `observation` even when
the author generalizes from it, and reserves `principle` for the explanation
stated without its measurement. `[DESIGN]` A second contributing cause is
established: through v2 the codebook's `observation` definition still pointed
raters at `finding`, `study`, and `conclusion` — labels the restructure had
removed. Eleven such dangling pointers were found and repaired. How much of the
37 was the missing label and how much was the broken codebook is not yet
separated.

Three changes follow from that test:

- **`technique` removed**, merged into `procedure`. It measured α 0.588, the
  weakest label, with six confusions against `procedure`. This is the one change
  the data made on its own.
- **`driver` → `principle`.** `driver` measured α 0.623 and collided with
  `structure` seventeen times — the largest collision in that test. `[DESIGN]` The
  likely cause is the same ambiguity that sank `mechanism`: in engineering, a
  *driver* is a component, so the label read as machinery rather than as the
  causal idea. `principle` has no such reading. Whether the rename fixes the
  boundary is a re-test, not a claim.
- **`structure` → `architecture`.** `[DESIGN]` Naming only. `architecture` is
  the native word in ML model cards; `structure` was the more neutral term for
  portfolios. The ML reading was judged to carry more weight for this corpus.

`[DESIGN]` One risk this revision introduces: `principle` can be read
normatively. "Prefer small reversible steps" is a principle in ordinary English
but is advice, not an explanation — §3.3 now carries an explicit
`principle`/`obligation` separation for exactly that.

### 2.8 What the third collision test measured

`[MEASURED]` The changes in §2.7, plus the strip test and the eleven repaired
pointers from the control, were tested on **both** earlier item sets at once —
152 statements, four blind raters, two arms differing only in whether the strip
test was present (`research/2026-08-10-codebook-collision-test-v3.md`).

Holding the items fixed, in both directions:

| | fine α | coarse α |
|---|---|---|
| 72 results-dense items, v2 codebook (the control) | 0.787 | 0.791 |
| the same 72, v3 codebook | **0.883** | **0.874** |
| 80 mixed items, v2 codebook | 0.858 | 0.927 |
| the same 80, v3 codebook | **0.930** | 0.927 |

**+0.096 and +0.072 fine α, with the item set held fixed in each pair.** This is
what §2.7 claimed and could not show. The two renames account for most of it:

| v2 | α | v3 | α |
|---|---|---|---|
| `driver` | 0.623 | `principle` | **0.910** |
| `structure` | 0.727 | `architecture` | **0.851** |
| `procedure` | 0.760 | `procedure`, absorbing `technique` | 0.834 |

`[CAVEAT]` The renames are confounded with the pointer repair; both shipped in
the same revision and this experiment cannot separate them.

**The strip test does its job locally and disappears in aggregate.** On the
`principle`/`observation` boundary it targets: 37 disagreeing rater-pairs under
the control, 17 once the pointers and names were fixed, **11** with the strip
test — a further 35%. On aggregate α its effect is ±0.012, which four raters
cannot distinguish from noise. It is retained because the boundary it fixes is
*cross-coarse*, and the coarse tier is the one consumers read.

`[MEASURED]` Two collisions this test surfaced are new, both cross-coarse, and
both are one sentence doing two jobs — the same shape the strip test addresses.
§3.3 now carries a rule for each:

- **`principle` / `recommendation`**, 12 rater-pairs. *"training/serving skew
  here is almost always the tokenizer version, check that before you go looking
  at the data"* — an explanation with an instruction attached.
- **`decision` / `procedure`**, 7 rater-pairs. *"Models are versioned by the
  SHA-256 of the serialized artifact, not by a semantic version string"* — a
  settled choice stated as how the thing is done.

`[MEASURED]` **`event` has not been exercised by three consecutive item sets**
(2 of 608 assignments, α ≈ 0 on those two; `background` drew zero across 152
items). `event` is retained deliberately for historical recording. It is
untested, not disproven — but three item sets drawn from six source types
failing to produce it is itself a statement about how often it will fire.

### 2.9 A change that was tested and rejected

`[MEASURED]` `principle`'s three remaining collisions were reviewed after §2.8.
Two were judged genuine semantic overlap that no wording fixes
(`principle`/`recommendation`, `principle`/`architecture`). The third,
`principle`/`observation`, was traced to a specific gap: the strip test resolves
a *measurement that also generalizes*, but says nothing about a **causal
diagnosis with no measurement in it** — "groupby stopped preserving row order
after the 2.1 upgrade, which is why the ranks shifted" explains one incident and
has no numbers to strip.

A **generality test** was written for `principle` to close it: being causal is
not enough, the claim must still apply to the next case. It was tested as a
fourth arm — same 152 items, same rotation, one paragraph different
(`research/2026-08-10-codebook-collision-test-v3c.md`).

**It was rejected.** It resolved five of the six items it was written for, and
broke five others that had been unanimous:

| | with strip test only | + generality test |
|---|---|---|
| `principle`/`observation` collisions | 17 | **19** |
| fine α, all 152 | 0.904 | 0.901 |
| fine α, results-dense subset | 0.871 | **0.848** |
| fine α, mixed subset | 0.930 | 0.943 |
| `principle` α | 0.861 | **0.797** |
| `principle` assignments | 123 | **77** |

It cut both ways, which is the tell. Two previously-unanimous *measured results*
were pulled toward `principle` ("Factor momentum spans stock-level momentum…"),
because a measured relation is also a standing one — the two tests point
opposite ways on the same sentence. Three previously-unanimous *system-behaviour
claims* were pulled toward `observation` ("the gpu autoscaler scales on queue
depth, not utilization…"), because raters disagreed whether a claim about *our*
autoscaler generalizes. 51 assignments migrated from `principle` to
`observation` in total.

`[MEASURED]` **This is the §2.3 prediction confirmed on this codebook, on the
label §2.3 named.** A criterion that cannot be checked against the surface of
the sentence introduces a judgment, and the judgment does not converge — even
when the criterion is correct in every individual case. The causal-diagnosis gap
identified above is real and remains **open**; it is not worth a scope judgment
to close it.

---

## 3. Definitions

`[VERIFIED]` This section, not the label count, is what determines whether the
classifier works. Codebook depth and annotator training moved κ by **.15–.36**
on identical documents with an identical label set — trained coders with a
17-page codebook, a decision tree and four training papers reached
κ .65/.85/.87; untrained coders given one page reached .35/.49/.72. Growing the
label set from 3 to 7 cost only **.07** (Teufel & Moens, EACL 1999).

`[VERIFIED]` Definitions must be written as surface tests, not judgment calls.
Concretely-described features reached F1 **> 0.60**; features requiring
interpretive inference fell **below 0.30**, and model difficulty tracked human
inter-coder difficulty at **r = 0.61** — so human disagreement is the practical
ceiling (7 models × 121 features × 567 excerpts, arXiv 2601.12099).

`[VERIFIED]` Codebook depth is necessary but not sufficient: a 45-page codebook
with a decision tree, category semantics, pairwise-distinction rules and worked
examples still yielded only κ 0.50–0.57 (CoreSC).

### 3.1 Required shape for every definition

Each of the fifteen fine labels carries:

- **Cue** — the surface pattern, stated so a reader can check it without
  inferring intent.
- **Excludes** — at least two explicit non-firing conditions.
- **Exemplars** — one document-style statement, one conversational.

Exemplars are drawn from quantitative finance and LLM/ML research, because
those are the domains this classifier runs on. `[DESIGN]` Note the drift: the
anchor categories in §2.2 were measured on chemistry and computational-
linguistics *papers*, so the κ figures transfer to these definitions only as far
as the category shapes do. §9 records this as a weakness in the evidence base,
not as something the exemplars fix.

Pairwise separations live in §3.3, not inside each definition, so that a
boundary is stated once rather than twice and cannot drift between two entries.

### 3.2 The fifteen definitions

---

#### `observation` → `case` · anchor κ 0.79

> **Cue.** **Insight extrapolated from multiple events.** A pattern or reading
> drawn across more than one occasion — not definitive enough to be a rule or a
> recommendation. Anecdotal by nature: it holds so far, on what has been seen.
>
> **More than one.** A single occurrence reported as fact is an `event`. It
> becomes an `observation` when the sentence reads across occasions — a rate, a
> repetition, a sample, a trend, a mean.
>
> **Excludes:** the occurrence itself, however quantified (→ `event`); an
> established difference between two options (→ `distinction`); reasoning from
> fundamentals (→ `principle`); something definitive enough to be followed
> (→ `procedure`, `obligation`, `prohibition` or `recommendation`).
>
> **Strip test.** An empirical result is an `observation` *even when the author
> generalizes from it*. Delete the numbers and the sample from the sentence: if
> nothing of substance survives, it was an `observation`; if a causal claim
> survives on its own, it is a `principle`.
>
> **Doc.** "Realized volatility on the book exceeded the model's 99th-percentile
> band on three consecutive sessions in March 2026."
> **Chat.** "loss spiked right after we bumped LR to 3e-4, twice in a row"

#### `event` → `case`

> **Cue.** **A single thing that happened, reported as fact.** Singular and
> factual. Quantity does not disqualify it — an incident report full of counts
> and losses is still one occurrence.
>
> **One versus many.** An `event` is one occasion. An `observation` extrapolates
> across several. *"The kill switch cancelled all 1,912 resting orders in 310 ms
> with zero rejects"* is one occurrence — `event`. *"Third timeout this week,
> same node every time — the nic is cooked"* reads across three — `observation`.
>
> **Excludes:** a reading drawn from what happened (→ `observation`); a settled
> choice (→ `decision`); a generally accepted state of affairs (→ `background`).
>
> **Doc.** "The prime broker raised margin requirements on the fund's short book
> on 14 March 2026."
> **Chat.** "training run 47 OOM'd overnight on node 3"


---

#### `obligation` → `method`

> **Cue.** **What is owed to a third party.** A requirement is an `obligation`
> only when there is someone outside the doing party to whom it is owed — a
> regulator, an exchange, a counterparty, a client, a contract. The positive
> counterpart of `prohibition`.
>
> **Internal requirements are `procedure`.** A rule the organisation imposes on
> itself, however mandatory it sounds, is how the organisation works: it belongs
> in the manual. *"Under Regulation T, initial margin is 50 percent"* is owed to
> a regulator — `obligation`. *"A new signal trades in shadow for sixty sessions
> before the Investment Committee will consider an allocation"* is owed to
> nobody outside — `procedure`.
>
> **Judge the action, not the grammar.** A requirement stated with a negation is
> still an obligation if what it demands is an action.
>
> **Excludes:** what must NOT be done (→ `prohibition`); an internal requirement
> (→ `procedure`); advice with no accountability (→ `recommendation`).
>
> **Doc.** "Positions must be marked to market daily before 17:00 ET."
> **Chat.** "every eval run has to log its seed and commit hash"

#### `prohibition` → `method`

> **Cue.** **The negative case of `procedure`** — where a `procedure` says what
> to do, a `prohibition` says what must not be done. A hard rule, manual-grade:
> it would be printed as an absolute and it can be *violated*.
>
> **Test.** Could someone be in breach of it? A `prohibition` was set by someone
> with standing, and doing it anyway is a breach. A peer pointing away from
> something out of experience — *"dead end, don't redo it"* — creates no breach
> and is a `recommendation`, however imperative it sounds.
>
> **Excludes:** a positively-stated requirement (→ `obligation`); advice against
> an action with no accountability behind it (→ `recommendation`).
>
> **Doc.** "The desk may not carry overnight exposure in names below $50m ADV."
> **Chat.** "never train on anything that overlaps the eval split"


#### `decision` → `method`

> **Cue.** A choice reported as settled, which governs what happens after it.
> Typically past-tense and agentive: *adopted*, *chose*, *approved*,
> *standardised on*, *agreed to*. This is the one `rule` label with no deontic
> modal to key on.
>
> **Excludes:** something that merely occurred, with no choice made (→ `event`);
> a choice still being proposed (→ `recommendation`); a statement carrying an
> explicit modal, which the deontic labels take instead.
>
> **Doc.** "The committee standardised on daily rebalancing after the turnover
> analysis."
> **Chat.** "we went with LoRA instead of a full fine-tune"

---

#### `procedure` → `method` · anchor κ 0.74

> **Cue.** An established operational instruction: **how the system is used.**
> It could be pasted into a user manual unchanged and read as something to be
> followed every time.
>
> **Test.** Is the sentence *reporting practice* or *putting something forward*?
> Reporting is `procedure`: *we use*, *backtests are charged*, *the loader runs
> at 07:00*, *positions are marked daily*.
>
> **Excludes:** anything put forward rather than reported — *we propose*,
> *proposal:*, *we recommend*, *is preferable*, *should*, *worth*, *what if*,
> *try* (→ `recommendation`); anything hedged — *I think*, *probably*,
> *usually*, *not sure* (→ `recommendation`); anything announced as a
> contribution to a discussion — *unpopular take*, *cheapest idea*,
> *counterpoint* (→ `recommendation`); how the system is **built** rather than
> used (→ `architecture`); a settled configuration choice among real
> alternatives (→ `decision`); the arithmetic defining a quantity (→ `formula`);
> a constraint someone is accountable to (→ `obligation`).
>
> `[MEASURED]` These were two labels (`procedure` and `technique`) until the
> second collision test measured `technique` at α 0.588, the weakest in the set.
> Merged.
>
> **Doc.** "To build the factor: winsorize at 1%, z-score cross-sectionally,
> then neutralize by sector and size."
> **Chat.** "we use gradient checkpointing to fit the batch on one node"


#### `recommendation` → `method`

> **Cue.** **Prescribes a course of action** — advice on what ought to be done,
> with no requirement force and nothing settled. Practical and experiential,
> bearing on a choice where more than one valid option exists, and usually
> conversational in register.
>
> **Excludes:** a requirement someone is accountable to (→ `obligation`); a
> choice already made (→ `decision`); a bare description of an approach (→
> `procedure`).
>
> **Doc.** "Practitioners should prefer shrinkage estimators when the sample
> covariance matrix is near-singular."
> **Chat.** "you probably want to warm up the LR over the first 2k steps"

---

#### `definition` → `concept` · anchor κ 0.81

> **Cue.** **Fixes a key topic.** It states what a term means, and the term is
> load-bearing — remove the definition and the reader cannot follow what
> follows. The grammatical centre is *X is / means / refers to / is defined as
> Y*.
>
> **Against `background`.** A `definition` defines the topic. `background` adds
> colour around it without defining anything.
>
> **Excludes:** a contingent statement that could turn out false, which fixes no
> terminology (→ `principle`); a contrast drawn between two terms (→
> `distinction`).
>
> **Doc.** "The Sharpe ratio is excess return divided by the standard deviation
> of excess return."
> **Chat.** "perplexity is just exp of the mean negative log-likelihood"

#### `distinction` → `concept`

> **Cue.** A **qualifier between multiple methods or options**, resting on
> established differences rather than on one occasion's measurement. The
> contrast is the payload: two things are named and what separates them is the
> point.
>
> **Proven, not anecdotal.** A `distinction` cites differences that hold — fee
> schedules, contract terms, published behaviour. If the contrast rests on what
> someone saw once, it is an `observation`.
>
> **Excludes:** a single term being defined (→ `definition`); a theoretical
> claim reasoned from fundamentals (→ `principle`); a one-off comparison
> someone happened to measure (→ `observation`).
>
> **Doc.** "Realized volatility is measured from past returns; implied
> volatility is backed out of option prices."
> **Chat.** "RAG retrieves at query time; fine-tuning bakes it into the weights"

#### `background` → `concept` · anchor κ 0.87

> **Cue.** **Additional colour or history.** It enriches understanding of the
> surround — but **it does not define the topic itself**. Strip it out and the
> topic is still defined; you have only lost context.
>
> **Against `definition`.** A `definition` is key to defining a key topic.
> `background` sits beside the topic and adds shading.
>
> **It is contextual, and usually announced** — *for context*, *historically*,
> *the desk began in*, the opening chapter of a handbook. Decide from the
> surrounding context (§1).
>
> **Against `observation`.** An `observation` extrapolates across events.
> `background` supplies the surround.
>
> **Last resort.** `background` loses every tie. If any other test fires, that
> label wins — a dated change is an `event`, a term being fixed is a
> `definition`, a contrast is a `distinction`, an explanation is a `principle`.
> `background` is what remains when a statement informs but claims nothing,
> instructs nothing, and defines nothing. `[MEASURED]` It was previously written
> as a positive category — "context a reader needs, presented as generally
> accepted" — which describes a large share of all expository prose, and it
> collided with `event` 11 times, `obligation` 4 and `principle` 4 on the first
> corpus that exercised it.
>
> **Excludes:** everything else. That is the point.
>
> **Doc.** "Cross-sectional momentum has been documented in equity markets since
> Jegadeesh and Titman."
> **Chat.** "transformers displaced RNNs for sequence modelling around 2018"

---

#### `principle` → `model`

> **Cue.** **The theory or rule** behind something — reasoning from fundamentals
> about why it holds or why it is built that way. First principles, not
> comparison, not measurement, and not implementation.
>
> **Test.** Would it survive without the specific case in front of you? A
> `principle` is stated at the level of the idea. A statement that compares two
> named options is a `distinction`; one that reports what was seen is an
> `observation`, even when it explains itself.
>
> **Excludes:** how the thing is built or sourced (→ `architecture`); the equation
> that computes it (→ `formula`); what must be true for it to hold (→
> `assumption`); what it needs in order to run (→ `dependency`); a single
> measured occasion (→ `observation`).
>
> **Carries `status`** (§2.6), as every type does: `floated` when raised but not
> worked out, `proposed` when specified but unvalidated, `evidenced` when
> something backs it, `settled` when indisputable. The status is not part of
> choosing this label — a principle is a principle whether or not it is proven.
>
> **Doc.** "Parking-lot vehicle counts predict same-store sales, so changes in
> counts lead reported revenue by roughly one quarter."
> **Chat.** "the whole thesis is more cars means the store is doing better"

#### `architecture` → `system`

> **Cue.** **Implementational design** — the construction of a physical or
> software system: what it is built out of, what components it has, what they
> are. Not a logical scheme and not a configuration.
>
> **Against `principle`.** `architecture` is the implementation; `principle` is
> the theory or rule behind it. The same system has both — how it is built, and
> why it is built that way.
>
> **The elevator test.** What the doors are made of and how the hoist is
> assembled is `architecture`. How to call the car is `procedure`.
>
> **Actual, not proposed.** `architecture` describes a real implementation,
> including a specification of one that has been committed to. A system being
> *put forward* is a `recommendation`, however concrete its detail.
>
> **Excludes:** how the system is *used* (→ `procedure`); a settled setting or
> configuration choice (→ `decision`); why it works (→ `principle`); the
> arithmetic (→ `formula`); something separate the build needs present
> (→ `dependency`).
>
> **Doc.** "Parking-lot counts are derived from daily satellite imagery, matched
> to store locations by geofence and aggregated to ticker level."
> **Chat.** "signal's built from the vendor feed plus our own geofences"

#### `formula` → `model`

> **Cue.** **Mathematical or scientific in nature** — an equation, an arithmetic
> definition in prose, or a statement that defines something in mathematical or
> scientific terms. A `formula` says what a quantity *equals*; it instructs
> nobody.
>
> **No opinions in a formula.** A formula computes and stops. If the sentence
> also evaluates, judges or hedges the result, that part is not formula.
>
> **Against `recommendation`.** A `recommendation` prescribes a course of
> action. A `formula` prescribes nothing — it defines.
>
> **Test.** Is the arithmetic the payload, or machinery inside a policy? "OCC
> divides the strike by four and multiplies contracts by four" defines the
> adjustment — `formula`. "The book targets 10% vol on a 0.94-decay covariance;
> if realized exceeds 13% the scaler cuts gross" uses arithmetic to state what
> is done — `procedure`.
>
> **Excludes:** a term's meaning with no computation given (→ `definition`); a
> reported value rather than the rule producing it (→ `observation`); arithmetic
> in service of an operational instruction (→ `procedure`).
>
> **Doc.** "Signal = z-score of the trailing 30-day change in vehicle count,
> winsorized at 1% and neutralized by sector."
> **Chat.** "it's just zscore(30d delta) then sector demean"

#### `assumption` → `model`

> **Cue.** **A leap of faith.** Something taken on trust for the rest to hold —
> asserted without evidence and without proof, and the sentence knows it. Marker
> words: *assumes*, *presupposes*, *conditional on*, *holds only if*, *provided
> that*, *on the standing assumption that*.
>
> **Against `architecture`.** An `assumption` is believed; an `architecture` is
> built. If it could be inspected in the system, it is not an assumption.
>
> **Excludes:** something needed to run rather than to be true (→ `dependency`);
> a limit on where it applies, stated as a result (→ `observation` or `principle`);
> a rule someone must follow (→ `obligation`).
>
> **Doc.** "The signal assumes foot traffic converts to revenue at a stable rate
> across store formats."
> **Chat.** "this only works if the conversion rate is roughly constant"
>
> `[DESIGN]` High value for this corpus specifically: quantitative models fail
> at their assumptions far more often than at their arithmetic, and assumptions
> are usually the least recorded part of a model.

#### `dependency` → `system`

> **Cue.** **An established requirement** — a hard fact that the thing cannot
> run without. Marker words: *requires*, *depends on*, *needs*, *is a
> prerequisite for*, *without X you cannot*.
>
> **Hard, not casual.** A `dependency` holds as a matter of fact about the
> system. Someone noting that a piece of data would be handy, or that they wish
> a mapping existed, is reporting their situation — `observation`, which is
> anecdotal by nature.
>
> **Excludes:** something taken for granted for a claim to hold (→ `assumption`);
> what the thing is built from (→ `architecture`); an anecdotal note about what
> is missing (→ `observation`).
>
> **Doc.** "Signal construction requires the earnings calendar in order to
> suppress positions into scheduled announcements."
> **Chat.** "needs the earnings cal, otherwise we trade straight into prints"




### 3.3 Pairwise separations

`[VERIFIED]` Pairwise distinction rules are the bulk of a working codebook, not
a garnish: the scheme that reached κ 0.71 shipped **75** of them alongside a
decision tree, in 111 pages of guidelines.

`[DESIGN]` The nineteen rules below cover the pairs judged to genuinely collide.
Pairs not listed were judged non-colliding — that judgment is mine and is worth
challenging; a pair that turns out to collide in practice should be added here
rather than patched into a definition.

| Pair | The test that separates them |
|---|---|
| `observation` / `event` | Was anything measured? An observation records a quantity or behaviour; an event records that something occurred. |
| `event` / `decision` | Was a choice made? An event happened to you; a decision was chosen and constrains later action. |
| `decision` / `obligation` | Is there a modal? An obligation states a standing requirement in modal form; a decision states one was established. If both fit, the modal wins. |
| `decision` / `recommendation` | Settled or proposed? A decision is closed; a recommendation is still advice. |
| `obligation` / `prohibition` | **What to do** versus **what not to do.** Judge by the action demanded, not by grammatical polarity — a negatively-phrased requirement that demands an action is an `obligation`. `[MEASURED]` Both items in the 21-pair collision were compound, carrying a requirement and a forbidding in one sentence; under §2.4 both tests score above 90 and the statement resolves to `general` with `multi_fire`. |
| `background` / `event` | `[MEASURED]` 13 rater-pairs. Both report what happened; the difference is what the sentence is *for*. An `event` records an occurrence in its own right; `background` uses occurrences to explain how things came to be, defines nothing, and is normally signalled or positioned as context. Decide from the surrounding context, not the sentence alone. |
| `recommendation` / `obligation` | Is anyone accountable? Advice can be ignored without violation; an obligation cannot. |
| `principle` / `architecture` | `[MEASURED]` The largest collision in the second test (17 disagreeing rater-pairs, when these were `driver`/`structure`). WHY it works versus HOW it is built. If deleting the sentence would leave you unable to explain the idea, it is a principle; if it would leave you unable to rebuild the thing, it is architecture. |
| `principle` / `obligation` | Explanatory or normative? A principle says why something holds; an obligation says someone must do something. "Prefer small reversible steps" is normative — it is a `recommendation` or `obligation`, not a principle. |
| `principle` / `recommendation` — the theoretical/practical test | `[MEASURED]` 18 rater-pairs. Is it **theoretical or hands-on**? A `principle` is a general, logical guide that would hold for anyone, stated at concept level. A `recommendation` is practical advice drawn from experience, bearing on a choice at hand **where more than one valid option exists**, and it usually sounds conversational. *"Counterpoint on freight — whatever we build there we're third in line behind people with faster feeds"* states a fact but its job is to stop an action, and it is experiential and conversational: `recommendation`. |
| `decision` / `procedure` | `[MEASURED]` 7 disagreeing rater-pairs in the third test, across two coarse types. `[DESIGN]` **Does the sentence name what was chosen *instead of* something else?** Surface cues: *rather than*, *not X but Y*, *instead of*, *we standardised on*. Naming the rejected alternative makes it a `decision`; stating only how the thing is done makes it a `procedure`. "Models are versioned by artifact SHA-256, not by semantic version" names the alternative — `decision`. |
| `principle` / `assumption` | Is it the reason it works, or a precondition for it working? A principle explains; an assumption is what must hold for the explanation to survive. |
| `principle` / `observation` | `[MEASURED]` The largest collision measured in any run (37 rater-pairs in the control, 17 after repair and renaming, 11 with the strip test). Apply the **strip test** from §3.2 `observation`: delete the numbers and the sample from the sentence. If nothing of substance survives, it is an `observation` — *even if the author generalizes from it*. If a causal claim stands on its own without any measurement, it is a `principle`. `[MEASURED]` A second, scope-judging test was written for this boundary and measured worse (§2.9); do not reintroduce one without re-testing. |
| `architecture` / `formula` | Parts or arithmetic? Architecture names components; a formula computes a value. |
| `architecture` / `dependency` | Inside or outside? Architecture is what the thing is made of; a dependency is something separate it needs. |
| `assumption` / `dependency` | Must be TRUE, or must be PRESENT? An assumption is a belief the model rests on; a dependency is an input it consumes. |
| `formula` / `definition` | Does it compute? A formula produces a number; a definition fixes a meaning. |
| `definition` / `background` | Fixing a term or setting the scene? A definition pins meaning; background situates the reader. |
| `definition` / `distinction` | One term or two? A definition fixes one; a distinction separates two. |
| `obligation` / `procedure` | `[MEASURED]` A cross-coarse leak in the first test (6 disagreeing rater-pairs). A procedure tells you the steps; an obligation tells you that doing it is required. A numbered list with a *must* in it is an obligation. |
| `procedure` / `definition` | `[MEASURED]` 15 rater-pairs, all on one naming-convention statement. Does the sentence describe **what a thing is**, or **what to do with it**? A naming scheme, a schema, a set of valid values is a `definition` even when following it requires action. |
| `procedure` / `principle` | Is the payload the instruction or the reason? A `procedure` tells you what is done; a `principle` tells you why it holds. Where a sentence carries both, the instruction wins — unless it is hedged or reassuring, in which case see below. |
| any / `recommendation` — the put-forward rule | `[MEASURED]` 15 rater-pairs on proposed architectures, and the dominant signal in the 72-pair `procedure` collision. **Anything proposed is a `recommendation`**, whatever it proposes. Markers: *we propose*, *proposal:*, *this RFC proposes*, *we recommend*, *is preferable*, *should*, *worth*, *what if*, *try*, *suggest*. Content does not override this — a fully specified system architecture that is being put forward is a `recommendation`, not an `architecture`. |
| any / `recommendation` — the reassurance marker | `[DESIGN]` **Procedures and principles do not have feelings.** Language that soothes, warns off, or manages the reader's reaction — *don't panic*, *no need to worry*, *don't stress*, *ignore me* — marks the sentence as advice from a person, not an operational instruction or a standing relation. Route to `recommendation`. |

---

## 4. Mechanism

### 4.1 Independent boolean tests, resolved in code

The model answers **one independent yes/no question per fine label**, in a
single call. It is never asked to pick one of fifteen.

`[VERIFIED]` Multiclass framing measured **90% lower odds** of correct
detection than binary presence/absence framing (OR 0.10, 95% CI 0.03–0.35,
p<.001, mixed-effects model over 1.1M+ annotations, arXiv 2601.12099).

`[DESIGN]` The specific tactic of decomposing *this* label set into fifteen
binary probes is an inference from that finding, not a tested design. The cited
study compared natively-binary features against natively-multiclass ones; it did
not decompose one set into the other. A claim asserting a tested decomposition
design was refuted 1-2 in verification.

**`[MEASURED]` The inference has now been tested directly, and it does not
hold.** Five coarse families × four blind raters, each agent seeing one family's
definitions and nothing else, on the same 160 items as the single-choice run
(`research/2026-08-11-boolean-battery-test.md`):

| | fine α | coarse α |
|---|---|---|
| single choice of fifteen | **0.877** | **0.896** |
| this mechanism, resolved by the priority order below | 0.785 | 0.805 |

Per-test agreement is *good* — eleven of fifteen tests exceed α 0.87. The loss
is entirely in resolution: raters fire slightly different **sets**, and priority
turns a small difference in the set into a different label. On 27 of 160 items
all four raters fired a label in common and still resolved differently.

`[MEASURED]` **The priority order below is worse than resolving alphabetically**
(0.785 vs 0.801). Of six rules tried on the same fired sets, the best was "the
most reliable test wins", at 0.829 — still 0.048 below simply asking for one
label. Retain this section for its one irreplaceable property, **multi-label
output**: 38% of statements fire two or more tests, and asked separately raters
say yes to both. That is information single choice destroys. It is not, on this
evidence, a way to raise agreement.

Resolution is a fixed priority order over the coarse types, applied by code:

```
case → method → concept → model → system        …and `background` last of all
```

Most surface-recognizable first. `background` is exempted from its coarse type's
position and resolved **last**, below every other fine label in the taxonomy: it
wins only when nothing else fired at all. See §3.2 — it is defined as the
residual of the `concept` family, not as a competitor within it. `[DESIGN]` One consequence worth naming: a
dated decision fires both `is_event` and `is_decision`, and because `rule`
outranks `case`, it resolves to `decision`. That is intended — the reason to
store a decision is that it governs later action, not that it occurred — but it
means dated decisions leave the `case` bucket entirely, and `multi_fire` is the
only record that the event reading existed. Within a coarse type, the fine label whose test
fired; if several fired, the first in the table order.

- **No test fires** → `general`.
- **Two or more coarse types fire** → resolve by priority, set `multi_fire`.
  A multi-fire statement is a candidate for splitting into two statements.

### 4.2 Prompt is a frozen, versioned artifact

`[VERIFIED]` Prompt wording alone swung classification accuracy by **26–36
points** on an interpretive six-class task with temperature 0 and formatting
held constant — 20 semantically equivalent prompts produced 0.546–0.808 on one
model and 0.392–0.756 on another (arXiv 2604.16413). The same study found
interpretive tasks far more prompt-sensitive than knowledge-anchored ones.

Any change to the prompt string is a `prompt_version` bump. Records carry the
version they were produced under. Re-wording without bumping is a defect.

### 4.3 Emit label names, never letters

`[VERIFIED]` Presenting options as A/B/C/D inherits selection bias, and most of
the effect comes from the option-ID tokens rather than position: removing the
IDs cut recall standard deviation from **5.5 to 1.0** on MMLU. Shuffling does
**not** fix it (5.9 vs 5.5 baseline; worse on ARC), and a debiasing instruction
barely helps (Zheng et al., arXiv 2309.03882, 20 models).

Tests are emitted as named boolean fields. No lettered options, no ordered menu.

### 4.4 Ensembling

`[VERIFIED]` Majority voting over three models from *different* families
improved agreement with human consensus (κ 0.62 ± 0.01 vs 0.56–0.62 for
individual models); expanding to five **reduced** it (arXiv 2602.11962).

`[DESIGN]` Three-model voting is optional and off by default. When enabled, the
three must come from different families.

---

## 5. Secondary fields

### 5.1 `modality` — on rules

`required` / `permitted` / `prohibited`, populated whenever a deontic modal is
present, independent of which type test fired. Validated only on statements that
resolved to `rule`; otherwise retained but not enforced.

`[DESIGN]` No measured evidence. Deontic modals are surface cues, which is the
property associated with reliable categories (§3), but this specific field has
not been evaluated.

### 5.2 `form` — statement, question or answer

```
form: statement | question | answer
```

Orthogonal to `type`, and available under **every** coarse category. A question
about a procedure is `type: procedure, form: question`; the answer that follows
is `type: procedure, form: answer`.

- `statement` — asserts something. The default.
- `question` — asks for something. Asserts nothing, defines nothing, instructs
  nothing.
- `answer` — supplied in response to a question, and only meaningful with one.

`[MEASURED]` **This closes the largest uncovered source of disagreement.** Four
questions in the 160-statement corpus produced roughly **50 disagreeing
rater-pairs**, scattered across six different pairs — `background`/`observation`,
`background`/`event`, `background`/`general`, `dependency`/`observation`,
`general`/`observation`, `event`/`general`. Raters had no way to record that a
statement was a question, so each one was filed by its *subject matter* instead:
a question about a data vendor landed near `dependency`, a question about
history landed near `event`, and no two raters chose alike.

`[DESIGN]` **The type still applies.** *"Did the rope theta get bumped to 500k
before or after we forked off main?"* is a `question` about a `decision`. Typing
the subject keeps questions retrievable alongside what they are about, which is
what makes "show me the open questions on this topic" a query rather than a
scan.

`[DESIGN]` `answer` is the one value that implies a relation to another
statement. Recording it is useful now; linking it to its question needs the edge
layer that is out of scope for v1 (§5.4).

### 5.3 `provenance` — where the record came from

```
provenance: { medium, author, source_id }
```

`medium` — `chat` / `document` / `transcript` / `code`. `author` — `human` /
`model`, with the model identifier when known. `source_id` — the thread,
document, or file.

`[DESIGN]` **Nothing here is classified.** Every value is known to the
ingestion pipeline before the classifier is called, so provenance costs no
agreement — it cannot be got wrong by a model that never infers it. This is the
opposite of the provenance that was *removed* from `status` in §2.6: "who
established this claim" is a judgment about the world that the sentence does not
contain; "which Slack thread did this line come from" is a fact the reader
already has.

`[MEASURED]` It is also operationally load-bearing. Chat statements classify at
fine α 0.811 against 0.940 for document statements on the same codebook and the
same run (§6). Without provenance on the record that gap is a fact nobody can
act on; with it, a consumer can weight or filter by medium.

### 5.4 Flags

`negative_result` — the statement reports an absence, null, or no-effect
finding. `caveat` — the statement limits, scopes, or excepts something else.

`[DESIGN]` No measured evidence for either flag. `negative_result` exists
because a null finding is not distinguishable from a positive one by embedding
similarity — "X does not work" and "X works" are near neighbours — so without an
explicit marker it is unrecoverable downstream. That is a mechanism argument,
not a measurement.

### 5.5 What this classifier does not produce

- **No confidence score is published.** Per-label confidence is elicited
  internally to drive `general` assignment (§2.4) but is not part of the output
  record. `[VERIFIED]` Verbalized confidence reliability
  depends strongly on how the model is asked, with no universal best method
  across 17 prompt methods × 10 datasets × 11 models spanning 2B–110B; the best
  method is model-dependent and small models' confidence is near-independent of
  their accuracy (arXiv 2412.14737). All of it was measured on closed-book QA,
  never on classification. Uncertainty is expressed structurally instead:
  `tests_fired == 0` is abstention, `tests_fired >= 2` is ambiguity.
- **No truth judgment and no relationships between statements.** Epistemic
  *maturity* is produced — that is `status` (§2.6) — but whether a statement is
  *correct* is not, and neither are edges between statements. Relations
  (`resolved_by`, `opposes`) are the natural next layer and are deliberately out
  of scope for v1.

---

## 6. Conversational statements

`[VERIFIED]` Conversational text is measurably harder. Six frontier models
classifying classroom utterances into seven categories reached Cohen's κ
**0.38–0.58**, where human expert annotators on the same data exceeded **0.90**
(Vanacore & Kizilcec, arXiv 2512.19903, 800 stratified utterances). A separate
study on support conversations found expert-model weighted κ median 0.60 against
expert-expert 0.58 — comparable, but on ordinal ratings rather than single-label
classification (arXiv 2506.10150).

`[VERIFIED]` Few-shot exemplars help, but model-dependently in both size **and
sign**: across six models, κ gains ranged from +19 points to *negative* — one
model peaked at three examples then declined with more, another ended below its
zero-shot score (Vanacore & Kizilcec, Table 2). Exemplar count is therefore a
per-model tuning parameter, which conflicts directly with a single prompt used
across families.

**No evidence was found** on: resolving pronouns and ellipsis before
classification, splitting one message into several statements, or how much
surrounding context a conversational statement needs. Three separate research
angles returned nothing that survived verification. The only context datapoint
anywhere in the evidence base is a 20–30 line window used as an unablated design
choice.

`[DESIGN]` Consequently:

- Conversational input may carry an optional context window, used only for
  reference resolution.
- A statement whose references cannot be resolved is classified `general` rather
  than guessed.
- Splitting a multi-statement message is **out of scope for v1**. The caller
  supplies one statement.
- Expect conversational accuracy materially below document accuracy, and measure
  the two separately (§7).

---

## 7. Evaluation

### 7.1 Human gold set first

`[VERIFIED]` Inter-model agreement is not evidence of correctness. Two
independent demonstrations: four models agreed on 96.1% of labels with Fleiss κ
−0.001 while missing 75% of the minority class; and in a separate study models
reached inter-model Krippendorff α 0.85 against human-human 0.65 while
diverging significantly from human judgment (t(49.42)=3.615, p<.001,
Cohen's d=0.88).

The acceptance test is agreement with human labels. Cross-model agreement is a
stability check only.

Gold set requirements:

- Both strata sampled separately: document-derived and conversational.
- Rare fine labels deliberately oversampled — otherwise `general` absorbs them
  invisibly.
- At least two independent human coders, adjudicated. **Report human–human
  agreement first**; it is the ceiling, and model numbers are uninterpretable
  without it.

### 7.2 Metrics

- Krippendorff's α at the **fine** tier and the **coarse** tier, reported
  separately. `[VERIFIED]` Raw percentage agreement is biased toward schemes
  with fewer categories, so tiers cannot be compared without chance correction —
  and chance-corrected measures are themselves distorted by skew, which a
  taxonomy with a residual bucket will certainly have (Artstein & Poesio,
  Computational Linguistics 34(4)).
- **Per-category** agreement, not just aggregate. §2.3 predicts a twofold
  spread; an aggregate hides it.
- `general` share, `multi_fire` rate, per-model divergence.

### 7.3 The rollup question is open

`[MEASURED]` The in-house collision test ran exactly this experiment on this
codebook: same annotations, mapping fixed in advance, agreement measured at both
tiers. Coarse scored **0.866** against fine **0.778**. That settles it for this
taxonomy on that item set — not in general.

`[DESIGN]` It remains unestablished in the literature. The direct experiment — one
annotation set, a mapping fixed in advance, agreement measured at both tiers —
does not exist in the reviewed literature. What exists is mixed: one scheme's
collapse from 15 labels to 2 moved κ 0.65 → 0.65 (zero gain), another moved
0.71 → 0.78, and the canonical survey warns that post-hoc merging is not
equivalent to designing the coarse scheme up front, since merges are typically
chosen exactly where coders disagreed.

Measuring both tiers on the gold set answers this for this taxonomy. Until then,
the two-tier design is a bet.

### 7.4 Kill criterion, pre-registered

`[VERIFIED]` The strongest direct evidence about typed information is negative
and human. Two controlled experiments on a shipped information-typing scheme
found **no effect on task performance** — n=65 process operators, effectiveness
F(2,62)=1.16 p=.32, efficiency F(2,62)=2.02 p=.14; and n=76, "no significant
effects on accuracy, speed or evaluation scores at all." The only significant
effect was subjective preference, and even that did not beat the incumbent text
(Jansen, Korzilius, le Pair & Roest, IEEE IPCC 2002 / Document Design 4(1)).

Scope limit, raised by all three verifiers: those studies were powered for large
effects only, and typing was bundled with six other principles — so this is
absence of a large effect, not proof that typing is inert.

`[VERIFIED]` No source in the reviewed evidence isolates type labels from
anything else. Every system claiming a typing benefit bundles it with linking,
extraction, reranking, or temporal invalidation; the counterfactual — same
corpus, same retriever, labels stripped — has never been run. The one payoff
that replicates across three independent agent-memory systems is **temporal
validity**, not typing.

Therefore, before this classifier is treated as load-bearing:

1. Run the ablation. Same corpus, same retriever, same ranking; type labels
   present versus stripped. Pre-register the query classes and the minimum
   effect size.
2. **User preference does not count as a gain.** Written here before results
   exist, because the one scheme that shipped on preference failed on task.
3. If no query class improves, the classifier is decoration. Keep temporal
   validity, drop the rest.

---

## 8. Versioning

`taxonomy_version` changes when labels or their mappings change.
`prompt_version` changes on any prompt edit. `classifier_model` records what
produced the record. All three are stamped on every record, and consumers may
filter on them.

Changing the taxonomy does not invalidate stored statements — classifications
are appended, and a statement may carry several from different versions.

---

## 9. Evidence register

Everything in this spec, sorted by what backs it.

### Measured, verified, cited above

| Claim | Number |
|---|---|
| Definitions dominate label count | κ .15–.36 vs .07 |
| Surface-observable beats interpretive | F1 >0.60 vs <0.30; r=0.61 to human difficulty |
| Binary framing beats multiclass | OR 0.10 (CI 0.03–0.35) |
| Prompt wording swings accuracy | 26–36 points |
| Option-ID letters cause selection bias | SD 5.5 → 1.0 when removed |
| Named escape hatch coincides with minority collapse | 96.1% agreement, κ −0.001, 75% missed |
| Agreement ≠ correctness | two independent demonstrations |
| Three-model vote helps, five does not | κ 0.62 vs 0.56–0.62 |
| Per-category reliability varies twofold; abstract worst | 0.89 … 0.43 |
| Conversational is harder | κ 0.38–0.58 vs human >0.90 |
| Few-shot gain is model-dependent in sign | +19 points to negative |
| Verbalized confidence is prompt-dependent | 17 methods × 10 datasets × 11 models |
| Percentage agreement is biased by category count | Artstein & Poesio |
| Typed documentation showed no task benefit | n=65, n=76, both null |
| Temporal validity is the replicated payoff | across three memory systems |

### Measured on this codebook, in-house

Twenty-two runs, codebook verbatim, no answer key in existence at any point,
roughly 10,000 assignments. The measurements that matter are the ones taken with
**eight raters** — a four-rater run cannot distinguish designs (see *Noise
floor* below).

**Headline, measured with 8 raters on 160 statements from eight sources:**

| | fine α | unanimity |
|---|---|---|
| codebook before the definition pass | 0.844 | 0.72 |
| **codebook after the definition pass** | **0.934** | **0.86** |

95% CI [0.905, 0.956]; the new codebook wins in **100%** of 400 paired
resamples. On a 40-statement subset the same codebook reaches **0.947–0.954**.

**On real published documents** — 85 statements extracted from Sharpe's *The
Arithmetic of Active Management* (1991), De Bondt & Thaler's *Does the Stock
Market Overreact?* (1985), and a Goldman Sachs market note — **fine α 0.894**,
95% CI [0.840, 0.942]. Real prose costs roughly 0.05 against generated
statements.

**Secondary fields:** `form` **1.000**, `scope` 0.799–0.940, `status`
0.861–0.906.

**Batch size does not matter.** The same 40 statements rated in batches of 5, 10
and 40 score 0.932, 0.947 and 0.949. Test figures should transfer to
one-statement-at-a-time production.

| Claim | Number |
|---|---|
| **The definition pass is the single largest effect measured** | fine α 0.844 → **0.934**, 8 raters, 160 statements, 100% of paired resamples |
| It came from domain judgment, not from the measurements | sixteen structural designs moved ±0.05 or lost; fourteen rewritten definitions moved +0.090 |
| A second round of refinements landed in the noise | nine further rulings: 0.954 → 0.947, beating the prior version in 36% of resamples |
| Real documents cost about 0.05 against generated statements | 0.894 on 85 statements from three published sources |
| Two labels carry three-quarters of real financial writing | `observation` 44%, `principle` 32% |
| `observation`/`principle` is irreducible, not ill-defined | 42% of all disagreement on real documents, after seven attempts to separate it |
| `form` is the most reliable field in the system | α **1.000** on the synthetic corpus, 1.000 on real documents |
| Questions were ~50 hidden splits before `form` existed | scattered across six different label pairs |
| Batch size is irrelevant between 5 and 40 statements | 0.932 / 0.947 / 0.949 |
| **Self-reported confidence cannot drive `general`** | 0.605 at threshold 90, with 86% of assignments falling through |
| **Noise floor: one 4-rater run cannot distinguish designs** | the same design run twice scored 0.898 and 0.844 |
| **v3 improves on v2 with the item set held fixed, in both directions** | fine **+0.096** (72 results-dense items), **+0.072** (80 mixed items) |
| `driver` → `principle` fixed the weakest label | α 0.623 → **0.910**, same 80 items |
| `structure` → `architecture` fixed the second-weakest | α 0.727 → **0.851**, same 80 items |
| Merging `technique` into `procedure` helped `procedure` | α 0.760 → 0.834, same 80 items |
| The strip test moves its target boundary | `principle`/`observation` 37 → 17 (repair + renames) → **11** (strip test) |
| The strip test's aggregate effect is within noise | fine −0.005, coarse +0.012, over 152 items |
| **Asking for status IMPROVES type agreement** | fine +0.036, coarse +0.056, same 160 items |
| The status ladder is more reliable than the type taxonomy | status α **0.896** vs type α 0.877, same items |
| `floated`/`proposed` separate cleanly — the predicted weak boundary was not weak | 2 rater-pairs, least confused in the ladder |
| The ladder's real difficulty is at the top | `evidenced`/`settled` 21, `evidenced`/`proposed` 20 |
| Status is dependent on type but does not collapse | Cramér's V 0.595; 49% predictable from type, 51% not |
| Status is worthless on some types and carries everything on others | residual entropy 0.00 on `definition`, 1.84 on `dependency` |
| Raters do not want an `n/a` status | 9 of 640 (1.4%) |
| All fifteen labels exercised, for the first time | `event` 2 → 45, `background` 0 → 35, `distinction` 7 → 17 |
| Research-results prose is the hardest source, on a fourth independent corpus | type α 0.642 vs 0.899 for an RFC |
| Chat classifies materially worse than documents | fine α 0.811 vs 0.940, same codebook, same run |
| Two new collisions only visible once coverage existed | `background`/`event` 11, `distinction`/`principle` 7 |
| Two new cross-coarse collisions surfaced | `principle`/`recommendation` 12, `decision`/`procedure` 7; both now in §3.3 |
| **A scope-judging criterion on `principle` was tested and made things worse** | `principle`/`observation` 17 → **19**; `principle` α 0.861 → **0.797**; rejected (§2.9) |
| Non-surface criteria do not converge, even when individually correct | 5 target items resolved, 5 unanimous items broken |
| `event` is unexercised, not disproven | 2 of 608 assignments across three item sets, α ≈ 0 |
| The definitions separate at all | fine α 0.778 → **0.934**, across twenty-two runs |
| Coarse tier beats fine on the same annotations | +0.088 (v1), +0.069 (v2); mapping fixed in advance |
| **The v2 restructure did NOT improve reliability** | taxonomy alone: fine **+0.009**, coarse **−0.075** |
| **The +0.080 v1→v2 headline was the item set, not the taxonomy** | 89% of the fine-tier gain |
| Dissolving `claim` has a cost, concealed by the v2 item set | `principle`/`observation` 37 rater-pairs on v1 items, 0 on v2 items |
| `technique` was the weakest label and collided with `procedure` | α 0.588, 6 confusions; merged |
| `driver`/`structure` was v2's largest collision | 17 confusions; both since renamed |
| `mechanism` (v1, since removed) was reliable despite its 0.43 anchor | α 0.933 |
| `finding`/`conclusion` were v1's worst pair | 17 confusions; merged, then removed |
| A results-shaped label absorbs a quarter of a research corpus | `finding` 24% (v1), `observation` 23% (v2) |
| Raters do not reach for the escape hatch even when the right label is absent | 0 of 320 (v2), 0 of 288 (control) |

That last row is the methodological correction this register exists to record.
A zero escape-hatch rate was first read as evidence that no label was missing.
It is not: a missing label surfaces as a **collision**, not an escape. The
control found the collision the escape rate could not.

Caveats on all of the above: four raters per arm from one model family, no human
gold set, 72–152 items per run, no confidence intervals, and item sets that
never exercised every label. It measures reproducibility, not correctness.

Two confounds remain unresolved. The renames shipped in the same revision as the
eleven repaired pointers, so v3's +0.096/+0.072 cannot be attributed between
them. And every effect at the ±0.01 scale — the strip test's aggregate figure
in particular — is below what four raters can distinguish from noise; only the
per-boundary collision counts move far enough to read.

### Design decisions with no supporting measurement

- The five coarse types and their names.
- The fifteen fine labels, their names, and which coarse type each maps to. The
  `driver` → `principle` and `structure` → `architecture` renames are motivated
  by a measured collision but are not themselves measured.
- The strip test separating `observation` from `principle`. Its effect on the
  target boundary is measured (37 → 11); its effect on aggregate α is not
  distinguishable from noise. The decision to keep it rests on the boundary
  being cross-coarse, which is a judgment. Its proposed companion, the
  generality test, WAS measured and was rejected (§2.9).
- The `principle`/`recommendation` and `decision`/`procedure` rules in §3.3. The
  collisions are measured; the separators are not.
- Retaining `event` after three item sets failed to exercise it.
- The priority order used to resolve multiple firing tests.
- Decomposing this label set into fifteen binary probes specifically.
- `modality`, `negative_result`, `caveat`.
- Treating `general` as a code-assigned residual rather than a model-visible label
  (the *hazard* is measured; this *mitigation* is not).
- Splitting multi-statement messages being out of scope.

### Contradicted or unsupported by the evidence

- That typing improves retrieval. No source isolates it. Zero measured evidence.
- That fine→coarse rollup buys reliability. Direct experiment does not exist;
  existing evidence is mixed and confounded.
- That type-matched pairing improves contradiction detection. Zero evidence in
  either direction.
- Structured-output reliability across model families. Zero confirmed claims
  despite being explicitly researched — the largest open risk for a classifier
  that must return parseable output from several vendors.

### Known weaknesses in the evidence itself

- The annotation-reliability figures trace largely to one research lineage; this
  is not independent replication.
- All annotation evidence is humans labelling sentences inside full documents.
  This classifier types short statements shown without their document. Whether
  agreement transfers up or down is untested — a claim pointing one way was
  refuted 0-3.
- The definitions in §3.2 use quantitative-finance and LLM/ML exemplars, while
  every anchor category in §2.2 was measured on chemistry and computational-
  linguistics papers. The κ figures transfer only as far as the category
  shapes do; they were not measured on these exemplars or these domains.
- The nineteen pairwise separations in §3.3 cover the pairs judged to collide.
  That judgment is unmeasured. The scheme that reached κ 0.71 shipped 75 rules.
- The reliability numbers in §2.2 are one-vs-rest binary collapses, mechanically
  higher than the full multi-way agreement of the same scheme (κ 0.50–0.57).
  They rank categories against each other reliably; they are not absolute
  targets.
