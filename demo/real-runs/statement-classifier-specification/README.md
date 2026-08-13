# statement-classifier-specification

A complete run of the `kip` ingestion pipeline over `SPECIFICATION`.

**140 knowledge units** · **516 citations** (516 verified) · **53 entries handed off** · run `spec` · schema `3.1.0`

---

## Reading this folder

**If you are a person:** the [entries](#the-knowledge-handed-off) below are the output — what a knowledge base would receive. The [assets](#assets) are the tables, formulas and page images recovered from the source, shown as they are stored.

**If you are a model asked to ingest this run, do not work from this file.** It is a rendering and it is lossy. Read, in order:

1. [`runs/spec/07_enqueue/enqueue.jsonl`](runs/spec/07_enqueue/enqueue.jsonl) — **the handoff.** One JSON event per approved entry, each with `payload.title`, `payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This is the only file you need in order to ingest; everything below is for checking what it says.
2. [`runs/spec/02_units/units.jsonl`](runs/spec/02_units/units.jsonl) — the evidence. Each unit carries verbatim excerpts with character offsets into `normalized.txt`, and `asset_ref` where the evidence is a table cell or a formula. Follow `payload.source_unit_ids` from an entry to get here.
3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. **Check `fidelity` before you trust a comparison:** `exact` came from the source's own markup and can be compared as a string; `transcribed` was read off an image and must not be.
4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset citation resolves against, by character offset.
5. [`runs/spec/00_original_sources/`](runs/spec/00_original_sources) — the raw source, unmodified. Go here when you need to check the pipeline itself.

Everything else records how the output was arrived at: the routing, the judgments, the candidates before audit, and the audit findings.

## What is in each folder

| folder | contents |
|---|---|
| [`00_original_sources`](runs/spec/00_original_sources) | The source documents exactly as ingested, byte for byte. |
| [`01_normalized`](runs/spec/01_normalized) | One directory per source: `normalized.txt` (the flat text every citation resolves against), `assets.jsonl` (tables, formulas and figures the flat text could not hold), `manifest.json`, and `assets/` for any rendered page images. |
| [`02_units`](runs/spec/02_units) | `units.jsonl` — every extracted knowledge unit with its verbatim evidence and character offsets. `omissions.jsonl` — what the completeness check found missing. `rejects.jsonl` if any record failed materialization. |
| [`03_clusters`](runs/spec/03_clusters) | Which units were routed together for comparison, and why. |
| [`04_assessments`](runs/spec/04_assessments) | One judgment per claim: does the evidence support it, contradict it, or settle nothing, and how many INDEPENDENT sources it rests on. |
| [`05_candidates`](runs/spec/05_candidates) | Proposed knowledge-base entries, before audit. |
| [`06_audit`](runs/spec/06_audit) | `audits.jsonl` — the adversarial review of each candidate, with deterministic check results. `corpus_coverage.json` — whether the output fairly represents the whole corpus. |
| [`07_enqueue`](runs/spec/07_enqueue) | **`enqueue.jsonl` is the handoff.** One idempotent event per approved entry. This is the file a consuming knowledge base reads. |
| [`_handoff`](runs/spec/_handoff) | The complete record of every model call: `pending.jsonl` holds the requests, `responses.jsonl` the answers. Copying `responses.jsonl` into a fresh workspace replays the entire run from cache. |

## Does the output represent the corpus?

The run's own corpus-coverage audit returned **`represented`**.

> The two unrelated tables are both from section 2.8, the third collision test. The section's finding IS carried as prose; what no unit points at is the two tables showing the per-pair numbers behind it. A consumer gets the conclusion and not the measurements it rests on, which is a thin gap rather than a hole -- the tables are in the record and the section's claim is stated.

> This is the first pass over this document where its tables exist at all. They were Markdown pipe tables, which had no asset path until now, so the label mapping reached the corpus as flattened rows and the completeness check's own finding -- that a reader 'cannot determine from the output that `distinction` maps to `concept`' -- had no mechanism behind it to fix.

> The reliability figures are this codebook's own in-house measurement: 8 raters, 160 statements, eight sources. The leaf carrying them is `internal-observation` rather than a stronger state, which is the honest label for a document measuring itself.

Full judgment: [`06_audit/corpus_coverage.json`](runs/spec/06_audit/corpus_coverage.json).

## What the checks found

- The completeness check reported **8 finding(s)** against the first extraction: [`02_units/omissions.jsonl`](runs/spec/02_units/omissions.jsonl).
- The adversarial audit reviewed **53 candidate(s)** and passed 41 without requiring a correction: [`06_audit/audits.jsonl`](runs/spec/06_audit/audits.jsonl).

## Assets

**14 assets** — 14 table. 12 related to at least one unit, 2 related to none.

An asset related to no unit sits in a passage the extraction read and drew nothing from -- the same decision it makes about a paragraph it does not extract from, and not tracked as a defect for either. What an asset is worth is settled by whether the text around it reached an approved entry.

Fidelity is part of the record, because the kinds are not equally trustworthy:

- **exact** (14) — structure recovered from markup the source itself carried — citable as a quote

Evidence cites an asset with `asset_ref {asset_id, row, col}` for a table cell, or `{asset_id}` for a formula. A cell reference resolves to the value **and** the headers governing it, which is what makes a figure checkable rather than merely quoted.

### `src-specification-bf9781a3`

[`normalized.txt`](runs/spec/01_normalized/src-specification-bf9781a3/normalized.txt) · [`assets.jsonl`](runs/spec/01_normalized/src-specification-bf9781a3/assets.jsonl) · [`manifest.json`](runs/spec/01_normalized/src-specification-bf9781a3/manifest.json)

| asset | kind · fidelity · anchor | caption | related to |
|---|---|---|---|
| [`tbl-src-specification-bf9781a3-0001`](#tbl-src-specification-bf9781a3-0001) | table · exact · own_text | Statement Classifier — Specification v1.0 | 2 unit(s) |
| [`tbl-src-specification-bf9781a3-0002`](#tbl-src-specification-bf9781a3-0002) | table · exact · own_text | 2.1 Coarse types | 2 unit(s) |
| [`tbl-src-specification-bf9781a3-0003`](#tbl-src-specification-bf9781a3-0003) | table · exact · own_text | 2.2 Fine labels, with measured reliability where it exists | 5 unit(s) |
| [`tbl-src-specification-bf9781a3-0004`](#tbl-src-specification-bf9781a3-0004) | table · exact · own_text | 2.4 `general` | 1 unit(s) |
| [`tbl-src-specification-bf9781a3-0005`](#tbl-src-specification-bf9781a3-0005) | table · exact · own_text | 2.6 `status`, and why `claim` no longer exists | 3 unit(s) |
| [`tbl-src-specification-bf9781a3-0006`](#tbl-src-specification-bf9781a3-0006) | table · exact · own_text | 2.7 What the second collision test changed | 1 unit(s) |
| [`tbl-src-specification-bf9781a3-0007`](#tbl-src-specification-bf9781a3-0007) | table · exact · own_text | 2.8 What the third collision test measured | 1 unit(s) |
| [`tbl-src-specification-bf9781a3-0008`](#tbl-src-specification-bf9781a3-0008) | table · exact · own_text | 2.8 What the third collision test measured | **no units** |
| [`tbl-src-specification-bf9781a3-0009`](#tbl-src-specification-bf9781a3-0009) | table · exact · own_text | 2.9 A change that was tested and rejected | 1 unit(s) |
| [`tbl-src-specification-bf9781a3-0010`](#tbl-src-specification-bf9781a3-0010) | table · exact · own_text | 3.3 Pairwise separations | 13 unit(s) |
| [`tbl-src-specification-bf9781a3-0011`](#tbl-src-specification-bf9781a3-0011) | table · exact · own_text | 4.1 Independent boolean tests, resolved in code | 2 unit(s) |
| [`tbl-src-specification-bf9781a3-0012`](#tbl-src-specification-bf9781a3-0012) | table · exact · own_text | Measured, verified, cited above | **no units** |
| [`tbl-src-specification-bf9781a3-0013`](#tbl-src-specification-bf9781a3-0013) | table · exact · own_text | Headline, measured with 8 raters on 160 statements from eigh | 2 unit(s) |
| [`tbl-src-specification-bf9781a3-0014`](#tbl-src-specification-bf9781a3-0014) | table · exact · own_text | Measured on this codebook, in-house | 5 unit(s) |
Contents of each are at the end, under [Assets in full](#assets-in-full).

## The knowledge handed off

Rendered from [`07_enqueue/enqueue.jsonl`](runs/spec/07_enqueue/enqueue.jsonl) — 53 event(s), target `existing-leaf-engine`.

---

### 1. The statement taxonomy: five coarse types, fifteen fine labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-001-r1` v2

**Slug** `the-statement-taxonomy-five-coarse-types-fifteen-fine-labels`

The structure of the taxonomy and the provenance of its reliability figures. Four labels borrow an anchor category's published agreement; eleven have none.

**Assertions (2)**

1. Each fine label is anchored where possible on a category with a published inter-annotator agreement figure, and the kappa quoted is the agreement for the anchor category in the cited scheme rather than for the label as written here. Four labels carry anchors: observation on CoreSC Observation at 0.79, procedure on CoreSC Method at 0.74, definition on CoreSC Object at 0.81, and background on CoreSC Background at 0.87. The other eleven are marked DESIGN.

   *backed by* `asmt-0005`

2. The CoreSC figures come from Liakata et al., LREC 2010: per-category one-vs-rest Cohen's kappa over 41 chemistry and biochemistry papers with expert annotators. The AZ-II figures come from Teufel et al., EMNLP 2009: fifteen categories, three annotators, N=3745.

   *backed by* `asmt-0001`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0002</code> — table, exact, not cited</summary>

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `method` | What is done, required, forbidden, advised, or settled? |
| `concept` | What does this term mean? |
| `model` | Why does this hold, what does it rest on, and how is it computed? |
| `system` | What is the thing built from, and what does it need to run? |

*(1 further rows in the stored grid.)*

</details>

**Source units (1)** `u-src-specification-bf9781a3-0010`

**Traceability** — idempotency key `ccf5749130ed29484a5b6a72b744b6671da6da2321b082588989d32dc05e287f` · queue event `q-ccf5749130ed2948` · audits `audit-cand-001`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 2. Per-category reliability varies twofold, and abstract categories are worst

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-002-r1` v2

**Slug** `per-category-reliability-varies-twofold-and-abstract-categories-are-worst`

The measured regularity that governs how every definition in this codebook had to be written, and the three rules it imposes.

**Assertions (1)**

1. The first consequence of the reliability spread is that the model coarse type is the known weak point, since its anchor is the lowest measured category in the scheme. Principle is therefore defined primarily as a surface test -- does the statement contain a causal or structural connective linking two named things -- rather than as a judgment about explanatory intent. This was tested directly: a non-surface generality test, asking whether a causal claim outlives the occasion it describes, measured worse than the surface definition it replaced.

   *backed by* `asmt-0007`

**Source units (1)** `u-src-specification-bf9781a3-0014`

**Traceability** — idempotency key `5361edcb333d495a3835e8a75467465025b8fbaac0d2f72e033bd321a71e7fcb` · queue event `q-5361edcb333d495a` · audits `audit-cand-002`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 3. The `general` residual: assign by code, never by confidence

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-003-r1` v2

**Slug** `the-general-residual-assign-by-code-never-by-confidence`

Why the residual label is hidden from the model and why self-reported confidence cannot trigger it, with the threshold experiment that settles it and the generalization that follows.

**Assertions (1)**

1. Four labels were removed after the collision test. Conclusion merged into finding: they were the worst-colliding pair in the set at 11 co-occurrences with alphas of 0.607 and 0.680, and the measured-versus-inferred distinction between them did not survive contact with real statements. Study, permission and tradeoff were dropped as not carrying their weight; all three drew zero assignments in the test, but that was an item-set coverage gap, so the test did not independently show them to be weak and the decision is editorial. Event was retained deliberately for historical recording despite drawing zero assignments for the same reason.

   *backed by* `asmt-0009`

**Source units (1)** `u-src-specification-bf9781a3-0023`

**Traceability** — idempotency key `a98647f29263f313283c08327c62f3b396d5d903726674ac1b5c3f189d1ba598` · queue event `q-a98647f29263f313` · audits `audit-cand-003`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 4. The `status` field: floated, proposed, evidenced, settled

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-004-r1` v2

**Slug** `the-status-field-floated-proposed-evidenced-settled`

The four-rung epistemic-maturity field that replaced a coarse type, its measured reliability, and where it carries information type does not.

**Assertions (2)**

1. A known gap, worse than predicted: a measured result that drives nothing -- 'the signal earned 0.82 Sharpe net of costs over the full sample' -- has no obvious home once claim and finding are gone. This was expected to fall to general and the control run shows it does not. Raters do not reach for the escape hatch, 0 of 288. They split, with 37 disagreeing rater-pairs between observation and principle, the largest collision measured in any run -- and on a research corpus these statements are roughly a quarter of the text. So general's share is not the metric that surfaces this; fine-tier alpha on a results-dense corpus is.

   *backed by* `asmt-0001`

2. The restructure was re-tested on 80 fresh statements with four blind raters and agreement rose on both tiers: fine alpha from 0.778 to 0.858, coarse from 0.866 to 0.927, and unanimity from 0.67 to 0.78. No statement fell outside the taxonomy, 0 of 320.

   *backed by* `asmt-0012`

**Source units (2)** `u-src-specification-bf9781a3-0037`, `u-src-specification-bf9781a3-0038`

**Traceability** — idempotency key `bd18dec0180205ae9df41cc8511d69479c8c4233f5f672e552722467cffb59bc` · queue event `q-bd18dec0180205ae` · audits `audit-cand-004`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 5. The second collision test was confounded by its item set

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-005-r1` v2

**Slug** `the-second-collision-test-was-confounded-by-its-item-set`

A headline improvement, and the control that shows it came from the items rather than the taxonomy. Both are kept.

**Assertions (4)**

1. That comparison was confounded, and a control says the gain was not the taxonomy. The first and second tests used different item sets, so the headline moved for two reasons at once. Re-running the first test's 72 items through the second codebook isolates the taxonomy: the headline v1 to v2 change was +0.080 fine and +0.061 coarse with both taxonomy and items changing; the taxonomy alone moved +0.009 fine and -0.075 coarse; the item set alone moved +0.071 fine and +0.136 coarse. The restructure bought approximately nothing on a fixed item set and lost ground at the coarse tier.

   *backed by* `asmt-0013`

2. The claim that dissolving claim cost nothing was read off the second item set, which happens to contain few of the statements that make it costly. On the first item set the cost is plain: principle and observation disagreed on 37 rater pairs, the largest collision in any test so far, concentrated entirely on empirical research results -- sentences that report a measurement in order to assert a generalization. Claim and finding had absorbed those; with them gone they scatter across two coarse types.

   *backed by* `asmt-0011`

3. The response to the 37-pair collision is a mechanical tie-break rather than a restored label: the strip test assigns a measured result to observation even when the author generalizes from it, and reserves principle for the explanation stated without its measurement. A second contributing cause is established: through v2 the codebook's observation definition still pointed raters at finding, study and conclusion -- labels the restructure had removed. Eleven such dangling pointers were found and repaired, and how much of the 37 was the missing label and how much was the broken codebook is not yet separated.

   *backed by* `asmt-0001`

4. The third collision test measured the renames, the strip test and the eleven repaired pointers on both earlier item sets at once -- 152 statements, four blind raters, two arms differing only in whether the strip test was present. Holding items fixed in both directions: the 72 results-dense items went from fine 0.787 and coarse 0.791 under v2 to 0.883 and 0.874 under v3; the 80 mixed items went from 0.858 and 0.927 to 0.930 and 0.927. That is +0.096 and +0.072 fine alpha with the item set held fixed in each pair -- what §2.7 claimed and could not show.

   *backed by* `asmt-0017`

**Assets carried with this entry (2)** — 2 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0006</code> — table, exact, not cited</summary>

|   | fine α | coarse α |
|---|---|---|
| headline, v1 → v2 (taxonomy **and** items changed) | +0.080 | +0.061 |
| **taxonomy alone** (v1 items, both codebooks) | **+0.009** | **−0.075** |
| item set alone (v2 codebook, both item sets) | +0.071 | +0.136 |

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0007</code> — table, exact, not cited</summary>

|   | fine α | coarse α |
|---|---|---|
| 72 results-dense items, v2 codebook (the control) | 0.787 | 0.791 |
| the same 72, v3 codebook | **0.883** | **0.874** |
| 80 mixed items, v2 codebook | 0.858 | 0.927 |
| the same 80, v3 codebook | **0.930** | 0.927 |

</details>

**Source units (4)** `u-src-specification-bf9781a3-0039`, `u-src-specification-bf9781a3-0040`, `u-src-specification-bf9781a3-0041`, `u-src-specification-bf9781a3-0044`

**Traceability** — idempotency key `19b0445d29224ac22b1f210129829ac90fc41ca973956b7e2a637157e33a4f05` · queue event `q-19b0445d29224ac2` · audits `audit-cand-005`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 6. The third collision test: renames measured, item set held fixed

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-006-r1` v2

**Slug** `the-third-collision-test-renames-measured-item-set-held-fixed`

The experiment run to answer the previous control, with the per-label gains and the confound that limits attributing them.

**Assertions (6)**

1. The strip test does its job locally and disappears in aggregate. On the principle-against-observation boundary it targets, disagreeing rater-pairs went from 37 under the control to 17 once the pointers and names were fixed, and to 11 with the strip test -- a further 35 per cent. On aggregate alpha its effect is plus or minus 0.012, which four raters cannot distinguish from noise. It is retained because the boundary it fixes is cross-coarse, and the coarse tier is the one consumers read.

   *backed by* `asmt-0019`

2. Two collisions the third test surfaced are new, both cross-coarse, and both are one sentence doing two jobs: principle against recommendation at 12 rater-pairs, exemplified by an explanation with an instruction attached; and decision against procedure at 7 rater-pairs, exemplified by a settled choice stated as how the thing is done. §3.3 now carries a rule for each.

   *backed by* `asmt-0020`

3. A generality test for principle was written and rejected. Principle's three remaining collisions were reviewed: two were judged genuine semantic overlap that no wording fixes, and the third, principle against observation, was traced to a specific gap -- the strip test resolves a measurement that also generalizes but says nothing about a causal diagnosis with no measurement in it. The generality test held that being causal is not enough, the claim must still apply to the next case.

   *backed by* `asmt-0022`

4. The generality test was rejected on measurement. It resolved five of the six items it was written for and broke five others that had been unanimous. With the strip test only, principle-observation collisions were 17 and fine alpha across all 152 items was 0.904; adding the generality test made collisions 19 and alpha 0.901, dropped the results-dense subset from 0.871 to 0.848, dropped principle's own alpha from 0.861 to 0.797, and cut principle assignments from 123 to 77.

   *backed by* `asmt-0023`

5. The generality test cut both ways, which is the tell. Two previously unanimous measured results were pulled toward principle, because a measured relation is also a standing one and the two tests point opposite ways on the same sentence; three previously unanimous system-behaviour claims were pulled toward observation, because raters disagreed whether a claim about our own autoscaler generalizes. Fifty-one assignments migrated from principle to observation in total.

   *backed by* `asmt-0024`

6. The event label has not been exercised by three consecutive item sets: 2 of 608 assignments with alpha near zero on those two, while background drew zero across 152 items. Event is retained deliberately for historical recording. It is untested, not disproven -- but three item sets drawn from six source types failing to produce it is itself a statement about how often it will fire.

   *backed by* `asmt-0001`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0009</code> — table, exact, not cited</summary>

|   | with strip test only | + generality test |
|---|---|---|
| `principle`/`observation` collisions | 17 | **19** |
| fine α, all 152 | 0.904 | 0.901 |
| fine α, results-dense subset | 0.871 | **0.848** |
| fine α, mixed subset | 0.930 | 0.943 |
| `principle` α | 0.861 | **0.797** |

*(1 further rows in the stored grid.)*

</details>

**Source units (6)** `u-src-specification-bf9781a3-0046`, `u-src-specification-bf9781a3-0047`, `u-src-specification-bf9781a3-0049`, `u-src-specification-bf9781a3-0050`, `u-src-specification-bf9781a3-0051`, `u-src-specification-bf9781a3-0048`

**Traceability** — idempotency key `003f39b1fa708763383e0cb67ba64040eee5d7e3311b660fd2c75fbc2ead7fac` · queue event `q-003f39b1fa708763` · audits `audit-cand-006`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 7. Codebook depth beats label count, but is not sufficient on its own

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-007-r1` v2

**Slug** `codebook-depth-beats-label-count-but-is-not-sufficient-on-its-own`

The three published findings that justify writing definitions as surface tests and writing them at length.

**Assertions (1)**

1. DEFINITION -- observation (coarse: case, anchor kappa 0.79). Cue: insight extrapolated from multiple events -- a pattern or reading drawn across more than one occasion, not definitive enough to be a rule or a recommendation, anecdotal by nature in that it holds so far, on what has been seen. A single occurrence reported as fact is an event; it becomes an observation when the sentence reads across occasions -- a rate, a repetition, a sample, a trend, a mean. Excludes: the occurrence itself, however quantified (event); an established difference between two options (distinction); reasoning from fundamentals (principle); something definitive enough to be followed (procedure, obligation, prohibition or recommendation).

   *backed by* `asmt-0008`

**Source units (1)** `u-src-specification-bf9781a3-0058`

**Traceability** — idempotency key `ebb7b9ad916df11c253ed7436ffb9f80a4a6ca37621bf67071740b95056e6d10` · queue event `q-ebb7b9ad916df11c` · audits `audit-cand-007`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 8. Required shape of every label definition

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-008-r1` v2

**Slug** `required-shape-of-every-label-definition`

What each of the fifteen definitions must contain, and why boundaries are factored out of them.

**Assertions (2)**

1. RULE -- the strip test, which separates observation from principle. An empirical result is an observation even when the author generalizes from it. Delete the numbers and the sample from the sentence: if nothing of substance survives, it was an observation; if a causal claim survives on its own, it is a principle.

   *backed by* `asmt-0015`

2. DEFINITION -- event (coarse: case). Cue: a single thing that happened, reported as fact. Singular and factual; quantity does not disqualify it, since an incident report full of counts and losses is still one occurrence. An event is one occasion while an observation extrapolates across several. Excludes: a reading drawn from what happened (observation); a settled choice (decision); a generally accepted state of affairs (background).

   *backed by* `asmt-0030`

**Source units (2)** `u-src-specification-bf9781a3-0059`, `u-src-specification-bf9781a3-0060`

**Traceability** — idempotency key `4c1b2182c29ae4e1edf6457cfc2a50a18da5160c4f8b3b04096d939fc79c1332` · queue event `q-4c1b2182c29ae4e1` · audits `audit-cand-008`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 9. The fifteen label definitions

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-009-r1` v2

**Slug** `the-fifteen-label-definitions`

The codebook itself: each label's surface cue and its explicit exclusions, stated so a rater can check a sentence against them without inferring intent. This is the content the specification's own evidence identifies as determining whether the classifier works.

**Assertions (3)**

1. Background was previously written as a positive category -- context a reader needs, presented as generally accepted -- which describes a large share of all expository prose, and it collided with event 11 times, obligation 4 and principle 4 on the first corpus that exercised it. That is why it is now written as a residual.

   *backed by* `asmt-0095`

2. Pairwise distinction rules are the bulk of a working codebook, not a garnish: the scheme that reached kappa 0.71 shipped 75 of them alongside a decision tree, in 111 pages of guidelines. This specification's nineteen rules cover the pairs judged to genuinely collide; that judgment is the author's and is worth challenging, and a pair that turns out to collide in practice should be added to §3.3 rather than patched into a definition.

   *backed by* `asmt-0001`

3. Assumption is judged high value for this corpus specifically: quantitative models fail at their assumptions far more often than at their arithmetic, and assumptions are usually the least recorded part of a model. This is marked DESIGN.

   *backed by* `asmt-0097`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0010</code> — table, exact, not cited</summary>

| Pair | The test that separates them |
|---|---|
| `observation` / `event` | Was anything measured? An observation records a quantity or behaviour; an event records that something occurred. |
| `event` / `decision` | Was a choice made? An event happened to you; a decision was chosen and constrains later action. |
| `decision` / `obligation` | Is there a modal? An obligation states a standing requirement in modal form; a decision states one was established. If both fit, the modal wins. |
| `decision` / `recommendation` | Settled or proposed? A decision is closed; a recommendation is still advice. |
| `obligation` / `prohibition` | **What to do** versus **what not to do.** Judge by the action demanded, not by grammatical polarity — a negatively-phrased requirement that demands an action is an `obligation`. `[MEASURED]` Both items in the 21-pair collision were compound, carrying a requirement and a forbidding in one sentence; under §2.4 both tests score above 90 and the statement resolves to `general` with `multi_fire`. |

*(19 further rows in the stored grid.)*

</details>

**Source units (17)** `u-src-specification-bf9781a3-0061`, `u-src-specification-bf9781a3-0062`, `u-src-specification-bf9781a3-0063`, `u-src-specification-bf9781a3-0064`, `u-src-specification-bf9781a3-0065`, `u-src-specification-bf9781a3-0066`, `u-src-specification-bf9781a3-0067`, `u-src-specification-bf9781a3-0068`, `u-src-specification-bf9781a3-0070`, `u-src-specification-bf9781a3-0072`, `u-src-specification-bf9781a3-0073`, `u-src-specification-bf9781a3-0074`, `u-src-specification-bf9781a3-0076`, `u-src-specification-bf9781a3-0079`, `u-src-specification-bf9781a3-0080`, `u-src-specification-bf9781a3-0078`, `u-src-specification-bf9781a3-0081`

**Traceability** — idempotency key `67524ccf7b27224c46e2d5141b66cf6bca561254daba20b2c387be0f4b026866` · queue event `q-67524ccf7b27224c` · audits `audit-cand-009`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 10. Pairwise separations between colliding labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-010-r1` v2

**Slug** `pairwise-separations-between-colliding-labels`

The rules that bound each label against the ones it collides with, several carrying the measured collision count that prompted them, plus two any-label overrides.

**Assertions (1)**

1. RULE -- the reassurance marker: procedures and principles do not have feelings. Language that soothes, warns off, or manages the reader's reaction -- don't panic, no need to worry, don't stress, ignore me -- marks the sentence as advice from a person, not an operational instruction or a standing relation, and routes to recommendation. This is marked DESIGN.

   *backed by* `asmt-0130`

**Assets carried with this entry (2)** — 2 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0010</code> — table, exact, not cited</summary>

| Pair | The test that separates them |
|---|---|
| `observation` / `event` | Was anything measured? An observation records a quantity or behaviour; an event records that something occurred. |
| `event` / `decision` | Was a choice made? An event happened to you; a decision was chosen and constrains later action. |
| `decision` / `obligation` | Is there a modal? An obligation states a standing requirement in modal form; a decision states one was established. If both fit, the modal wins. |
| `decision` / `recommendation` | Settled or proposed? A decision is closed; a recommendation is still advice. |
| `obligation` / `prohibition` | **What to do** versus **what not to do.** Judge by the action demanded, not by grammatical polarity — a negatively-phrased requirement that demands an action is an `obligation`. `[MEASURED]` Both items in the 21-pair collision were compound, carrying a requirement and a forbidding in one sentence; under §2.4 both tests score above 90 and the statement resolves to `general` with `multi_fire`. |

*(19 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0011</code> — table, exact, not cited</summary>

|   | fine α | coarse α |
|---|---|---|
| single choice of fifteen | **0.877** | **0.896** |
| this mechanism, resolved by the priority order below | 0.785 | 0.805 |

</details>

**Source units (9)** `u-src-specification-bf9781a3-0082`, `u-src-specification-bf9781a3-0083`, `u-src-specification-bf9781a3-0084`, `u-src-specification-bf9781a3-0085`, `u-src-specification-bf9781a3-0086`, `u-src-specification-bf9781a3-0088`, `u-src-specification-bf9781a3-0089`, `u-src-specification-bf9781a3-0095`, `u-src-specification-bf9781a3-0087`

**Traceability** — idempotency key `17d6b2d45fe48580e73d1aca6adfabe13d0c08ea4dc4009bcd8e7c64d1895784` · queue event `q-17d6b2d45fe48580` · audits `audit-cand-010`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 11. How the classifier is asked, and why its mechanism measured worse

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-011-r1` v2

**Slug** `how-the-classifier-is-asked-and-why-its-mechanism-measured-worse`

The boolean-battery mechanism, the published evidence it was inferred from, the in-house test that refuted the inference, and the one property that keeps it in the design anyway.

**Assertions (3)**

1. The priority order is worse than resolving alphabetically -- 0.785 against 0.801. Of six rules tried on the same fired sets, the best was 'the most reliable test wins' at 0.829, still 0.048 below simply asking for one label. The section is retained for its one irreplaceable property, multi-label output: 38 per cent of statements fire two or more tests, and asked separately raters say yes to both. That is information single choice destroys. It is not, on this evidence, a way to raise agreement.

   *backed by* `asmt-0054`

2. Resolution is a fixed priority order over the coarse types, applied by code: case, then method, then concept, then model, then system -- most surface-recognizable first -- with background last of all. Background is exempted from its coarse type's position and resolved below every other fine label: it wins only when nothing else fired at all. Within a coarse type, the fine label whose test fired; if several fired, the first in table order.

   *backed by* `asmt-0055`

3. One consequence of the priority order is named explicitly: a dated decision fires both is_event and is_decision, and because rule outranks case, it resolves to decision. That is intended -- the reason to store a decision is that it governs later action, not that it occurred -- but it means dated decisions leave the case bucket entirely, and multi_fire is the only record that the event reading existed.

   *backed by* `asmt-0001`

**Source units (3)** `u-src-specification-bf9781a3-0096`, `u-src-specification-bf9781a3-0097`, `u-src-specification-bf9781a3-0098`

**Traceability** — idempotency key `2577b41b14b54293211fec7c5f264a9444e32dd01ca4634b29b17d23519cb579` · queue event `q-2577b41b14b54293` · audits `audit-cand-011`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 12. Conversational statements classify materially worse

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-012-r1` v2

**Slug** `conversational-statements-classify-materially-worse`

The evidence that chat is harder, the exemplar finding that conflicts with a frozen prompt, and the three questions on which no evidence was found.

**Assertions (1)**

1. The rollup question is open. The in-house collision test ran exactly the right experiment on this codebook -- same annotations, mapping fixed in advance, agreement measured at both tiers -- and coarse scored 0.866 against fine 0.778, which settles it for this taxonomy on that item set but not in general. It remains unestablished in the literature: the direct experiment does not exist in the reviewed work, and what exists is mixed -- one scheme's collapse from 15 labels to 2 moved kappa 0.65 to 0.65 for zero gain, another moved 0.71 to 0.78, and the canonical survey warns that post-hoc merging is not equivalent to designing the coarse scheme up front, since merges are typically chosen exactly where coders disagreed. Until the gold set is measured at both tiers, the two-tier design is a bet.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0119`

**Traceability** — idempotency key `e0c0d5a06a68ba0b982efef62a6babc71deea00002086bc0c662be7c3f1d5b3e` · queue event `q-e0c0d5a06a68ba0b` · audits `audit-cand-012`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 13. Evaluation, and the pre-registered condition for abandoning the classifier

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-013-r1` v2

**Slug** `evaluation-and-the-pre-registered-condition-for-abandoning-the-classifier`

Why the acceptance test must be human agreement, what must be measured, and the negative evidence that produced a kill criterion written before any results exist.

**Assertions (1)**

1. The in-house measurement base: twenty-two runs, codebook verbatim, no answer key in existence at any point, roughly 10,000 assignments. The measurements that matter are the ones taken with eight raters, because a four-rater run cannot distinguish designs.

   *backed by* `asmt-0063`

**Source units (1)** `u-src-specification-bf9781a3-0124`

**Traceability** — idempotency key `0174a4f2a12a62419e7f3f2e6492af530e1b2437bd8a6111b3478b7cc91dfb05` · queue event `q-0174a4f2a12a6241` · audits `audit-cand-013`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 14. The evidence register: what is measured, what is design, what is contradicted

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-014-r1` v2

**Slug** `the-evidence-register-what-is-measured-what-is-design-what-is-contradicted`

The specification's account of its own confidence, sorted by what backs each claim -- including the decisions with no measurement behind them and the claims the evidence contradicts.

**Assertions (3)**

1. The noise floor: one four-rater run cannot distinguish designs, because the same design run twice scored 0.898 and 0.844. Every effect at the plus-or-minus 0.01 scale -- the strip test's aggregate figure in particular -- is below what four raters can distinguish from noise; only the per-boundary collision counts move far enough to read.

   *backed by* `asmt-0001`

2. Two confounds remain unresolved in the in-house evidence: the renames shipped in the same revision as the eleven repaired pointers, so v3's +0.096 and +0.072 cannot be attributed between them; and the caveats on everything are four raters per arm from one model family, no human gold set, 72 to 152 items per run, no confidence intervals, and item sets that never exercised every label. It measures reproducibility, not correctness.

   *backed by* `asmt-0001`

3. A zero escape-hatch rate was first read as evidence that no label was missing, and it is not: a missing label surfaces as a collision, not an escape. Raters do not reach for the escape hatch even when the right label is absent -- 0 of 320 in v2 and 0 of 288 in the control. The control found the collision the escape rate could not. This is the methodological correction the evidence register exists to record.

   *backed by* `asmt-0066`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0014</code> — table, exact, not cited</summary>

| Claim | Number |
|---|---|
| **The definition pass is the single largest effect measured** | fine α 0.844 → **0.934**, 8 raters, 160 statements, 100% of paired resamples |
| It came from domain judgment, not from the measurements | sixteen structural designs moved ±0.05 or lost; fourteen rewritten definitions moved +0.090 |
| A second round of refinements landed in the noise | nine further rulings: 0.954 → 0.947, beating the prior version in 36% of resamples |
| Real documents cost about 0.05 against generated statements | 0.894 on 85 statements from three published sources |
| Two labels carry three-quarters of real financial writing | `observation` 44%, `principle` 32% |

*(38 further rows in the stored grid.)*

</details>

**Source units (3)** `u-src-specification-bf9781a3-0130`, `u-src-specification-bf9781a3-0131`, `u-src-specification-bf9781a3-0132`

**Traceability** — idempotency key `cdd4ce93185cd382c198ce6ee56d20061bd9e5d9d3d46e56f95a0c6a1bcb1bdb` · queue event `q-cdd4ce93185cd382` · audits `audit-cand-014`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 15. Statement classifier: measured reliability and evidence convention

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-015-r1` v2

**Slug** `statement-classifier-measured-reliability-and-evidence-convention`

What the classifier's agreement figures are, on which corpora and with how many raters, and the three-way labelling scheme the specification uses to mark what backs each of its claims. The figures are reproducibility among model raters on this codebook; no human gold set exists.

**Assertions (1)**

1. For scale, the argumentative-zoning scheme reached kappa 0.71 with seven categories and a 111-page codebook, and CoreSC reached 0.50-0.57 with eleven categories. This taxonomy has fifteen labels.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0003`

**Traceability** — idempotency key `0c6c91a80b7aee46bcc7a19b1d66caa4e303bacd5c9e472bf1872f1267021740` · queue event `q-0c6c91a80b7aee46` · audits `audit-cand-015`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 16. Statement classifier: the contract

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-016-r1` v2

**Slug** `statement-classifier-the-contract`

The interface, the record it returns, and the two things it refuses to do. Stated as the specification states it, so a consumer can build against it.

**Assertions (3)**

1. Classifications are appended, never overwritten. A classification is a pure function of (statement, prompt_version, classifier_model); re-running with a different triple appends a new record rather than replacing the old one, and consumers pick the record whose stamps they trust.

   *backed by* `asmt-0071`

2. The classifier does not judge truth. It answers what kind of statement this is, never whether it is correct; epistemic status lives elsewhere.

   *backed by* `asmt-0072`

3. The output record carries the statement hash, the fine and coarse labels, the per-label boolean tests with a tests_fired count and a multi_fire flag, status, form, modality, flags, provenance, and four stamps: taxonomy_version, prompt_version, classifier_model and classified_at.

   *backed by* `asmt-0070`

**Source units (2)** `u-src-specification-bf9781a3-0005`, `u-src-specification-bf9781a3-0006`

**Traceability** — idempotency key `2ce2675ac56532523f1ccbe6c255c860c9c44a6a78c9eeebec94715427519e90` · queue event `q-2ce2675ac5653252` · audits `audit-cand-016`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 17. The statement taxonomy: five coarse types, fifteen fine labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-017-r1` v2

**Slug** `the-statement-taxonomy-five-coarse-types-fifteen-fine-labels`

The structure of the taxonomy and the provenance of its reliability figures. Four labels borrow an anchor category's published agreement; eleven have none.

**Assertions (2)**

1. Each fine label is anchored where possible on a category with a published inter-annotator agreement figure, and the kappa quoted is the agreement for the anchor category in the cited scheme rather than for the label as written here. Four labels carry anchors: observation on CoreSC Observation at 0.79, procedure on CoreSC Method at 0.74, definition on CoreSC Object at 0.81, and background on CoreSC Background at 0.87. The other eleven are marked DESIGN.

   *backed by* `asmt-0005`

2. The CoreSC figures come from Liakata et al., LREC 2010: per-category one-vs-rest Cohen's kappa over 41 chemistry and biochemistry papers with expert annotators. The AZ-II figures come from Teufel et al., EMNLP 2009: fifteen categories, three annotators, N=3745.

   *backed by* `asmt-0001`

**Assets carried with this entry (2)** — 2 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0003</code> — table, exact</summary>

| Fine label | Coarse | Anchor κ | Anchored on |
|---|---|---|---|
| `observation` | case | **0.79** | CoreSC `Observation` [VERIFIED] |
| `event` | case | — | [DESIGN] — concrete by construction (actor + time) |
| `obligation` | method | — | [DESIGN] — deontic modal is a surface cue |
| `prohibition` | method | — | [DESIGN] — deontic modal is a surface cue |
| `decision` | method | — | [DESIGN] — a settled choice governs what happens next; note it is the one `rule` label with NO deontic modal to key on (§3.3) |

*(10 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0005</code> — table, exact, not cited</summary>

| type | n | bits | reading |
|---|---|---|---|
| `dependency` | 7 | 1.84 | status carries almost everything |
| `procedure` | 48 | 1.74 |   |
| `recommendation` | 94 | 1.73 |   |
| `principle` | 44 | 1.72 |   |
| `architecture` | 18 | 1.53 |   |

*(6 further rows in the stored grid.)*

</details>

**Source units (2)** `u-src-specification-bf9781a3-0011`, `u-src-specification-bf9781a3-0012`

**Traceability** — idempotency key `58f8169b271a8fb5e3e2e63e139cd5420b2a77597d3d51bb9a3bacc19eb97991` · queue event `q-58f8169b271a8fb5` · audits `audit-cand-017`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 18. Per-category reliability varies twofold, and abstract categories are worst

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-018-r1` v2

**Slug** `per-category-reliability-varies-twofold-and-abstract-categories-are-worst`

The measured regularity that governs how every definition in this codebook had to be written, and the three rules it imposes.

**Assertions (1)**

1. Within a single annotation scheme, per-category reliability varies by a factor of two and the abstract categories are systematically the worst: CoreSC measured Conclusion 0.89, Background 0.87, Object 0.81, Observation 0.79, Result 0.78 and Method 0.74, against Hypothesis 0.46, Motivation 0.46 and Model 0.43. This is marked VERIFIED.

   *backed by* `asmt-0006`

**Source units (1)** `u-src-specification-bf9781a3-0013`

**Traceability** — idempotency key `96b4cf90c4433494374c827ac38d9a15f0e8ba1da2bb970aef06c84b668e1e6f` · queue event `q-96b4cf90c4433494` · audits `audit-cand-018`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 19. The `general` residual: assign by code, never by confidence

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-019-r1` v2

**Slug** `the-general-residual-assign-by-code-never-by-confidence`

Why the residual label is hidden from the model and why self-reported confidence cannot trigger it, with the threshold experiment that settles it and the generalization that follows.

**Assertions (1)**

1. General is therefore triggered by disagreement across runs rather than by self-report: classify a statement more than once and, where the runs disagree, assign general. That reads the same signal the confidence rule was after -- nothing fits cleanly -- from a source that is not self-assessment. The number of runs and the disagreement rule are evaluation parameters and are not yet measured. General's share of the corpus is a standing health metric.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0022`

**Traceability** — idempotency key `b090e79c574022c87782122accc8e802630dcd405bef842299eba5c4c59aafdc` · queue event `q-b090e79c574022c8` · audits `audit-cand-019`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 20. Labels cut from the taxonomy, and which cuts the data justified

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-020-r1` v2

**Slug** `labels-cut-from-the-taxonomy-and-which-cuts-the-data-justified`

Four labels were removed. One removal was measured; three were editorial and the specification says so. Two gaps remain.

**Assertions (1)**

1. Merging conclusion into finding cuts against the other change in that revision: finding already took 24 per cent of all assignments and was behaving as a de-facto residual, and widening it increases that risk. The merged definition therefore tightens its exclusions against fact and observation rather than loosening them, and whether that holds is a re-test rather than a claim.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0025`

**Traceability** — idempotency key `b9620c6e8f2e21051ff53747a79abee679cbc51fba3baa0c09b672c8de55fca5` · queue event `q-b9620c6e8f2e2105` · audits `audit-cand-020`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 21. The second collision test was confounded by its item set

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-021-r1` v2

**Slug** `the-second-collision-test-was-confounded-by-its-item-set`

A headline improvement, and the control that shows it came from the items rather than the taxonomy. Both are kept.

**Assertions (2)**

1. Three label changes followed the second collision test. Technique was removed and merged into procedure: it measured alpha 0.588, the weakest label, with six confusions against procedure -- the one change the data made on its own. Driver was renamed principle: driver measured 0.623 and collided with structure seventeen times, the largest collision in that test, and the likely cause is that in engineering a driver is a component, so the label read as machinery rather than as the causal idea. Structure was renamed architecture, which is naming only: architecture is the native word in ML model cards.

   *backed by* `asmt-0016`

2. The two renames account for most of the third test's gain: driver at 0.623 became principle at 0.910, structure at 0.727 became architecture at 0.851, and procedure at 0.760 became 0.834 absorbing technique. The renames are confounded with the pointer repair; both shipped in the same revision and the experiment cannot separate them.

   *backed by* `asmt-0001`

**Source units (2)** `u-src-specification-bf9781a3-0042`, `u-src-specification-bf9781a3-0045`

**Traceability** — idempotency key `680beaf14cc27a71e10ca03ac18d2e231995400190ca0748086be6673ac75dcb` · queue event `q-680beaf14cc27a71` · audits `audit-cand-021`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 22. A scope-judging test for `principle` was measured and rejected

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-022-r1` v2

**Slug** `a-scope-judging-test-for-principle-was-measured-and-rejected`

A design change that was written, tested and reversed, and what its failure confirms about non-surface criteria.

**Assertions (2)**

1. The definitions section, not the label count, determines whether the classifier works. Codebook depth and annotator training moved kappa by 0.15 to 0.36 on identical documents with an identical label set: trained coders with a 17-page codebook, a decision tree and four training papers reached kappa 0.65, 0.85 and 0.87, while untrained coders given one page reached 0.35, 0.49 and 0.72. Growing the label set from 3 to 7 cost only 0.07.

   *backed by* `asmt-0025`

2. Codebook depth is necessary but not sufficient: a 45-page codebook with a decision tree, category semantics, pairwise-distinction rules and worked examples still yielded only kappa 0.50 to 0.57, in CoreSC.

   *backed by* `asmt-0001`

**Source units (2)** `u-src-specification-bf9781a3-0053`, `u-src-specification-bf9781a3-0055`

**Traceability** — idempotency key `b16d4b6deb496d5295c87b0311221de942de2ee42f80496bd9f31b821f57764b` · queue event `q-b16d4b6deb496d52` · audits `audit-cand-022`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 23. Codebook depth beats label count, but is not sufficient on its own

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-023-r1` v2

**Slug** `codebook-depth-beats-label-count-but-is-not-sufficient-on-its-own`

The three published findings that justify writing definitions as surface tests and writing them at length.

**Assertions (1)**

1. Every one of the fifteen fine labels carries three things: a Cue -- the surface pattern, stated so a reader can check it without inferring intent; Excludes -- at least two explicit non-firing conditions; and Exemplars -- one document-style statement and one conversational. Pairwise separations live in §3.3 rather than inside each definition, so that a boundary is stated once rather than twice and cannot drift between two entries.

   *backed by* `asmt-0027`

**Source units (1)** `u-src-specification-bf9781a3-0056`

**Traceability** — idempotency key `f55ca05fe3397af9afc92adeb98e15d3f51814595119fb727de5863ac5c9b845` · queue event `q-f55ca05fe3397af9` · audits `audit-cand-023`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 24. How the classifier is asked, and why its mechanism measured worse

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-024-r1` v2

**Slug** `how-the-classifier-is-asked-and-why-its-mechanism-measured-worse`

The boolean-battery mechanism, the published evidence it was inferred from, the in-house test that refuted the inference, and the one property that keeps it in the design anyway.

**Assertions (3)**

1. The form field takes statement, question or answer. It is orthogonal to type and available under every coarse category: a question about a procedure is type procedure with form question, and the answer that follows is type procedure with form answer. A statement asserts something and is the default; a question asks for something and asserts nothing, defines nothing and instructs nothing; an answer is supplied in response to a question and is only meaningful with one.

   *backed by* `asmt-0057`

2. The type still applies to a question: 'Did the rope theta get bumped to 500k before or after we forked off main?' is a question about a decision. Typing the subject keeps questions retrievable alongside what they are about, which is what makes 'show me the open questions on this topic' a query rather than a scan. The answer value is the one value that implies a relation to another statement; recording it is useful now, but linking it to its question needs the edge layer that is out of scope for v1.

   *backed by* `asmt-0059`

3. The form field closes the largest uncovered source of disagreement. Four questions in the 160-statement corpus produced roughly 50 disagreeing rater-pairs scattered across six different pairs -- background/observation, background/event, background/general, dependency/observation, general/observation and event/general. Raters had no way to record that a statement was a question, so each was filed by its subject matter instead: a question about a data vendor landed near dependency, a question about history landed near event, and no two raters chose alike.

   *backed by* `asmt-0058`

**Source units (3)** `u-src-specification-bf9781a3-0104`, `u-src-specification-bf9781a3-0106`, `u-src-specification-bf9781a3-0105`

**Traceability** — idempotency key `558d8ab5c6bc19982841037bb93a9e7f8e7008371a1a24ce14923b47d93d03e3` · queue event `q-558d8ab5c6bc1998` · audits `audit-cand-024`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 25. Secondary fields: form, provenance, modality and flags

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-025-r1` v2

**Slug** `secondary-fields-form-provenance-modality-and-flags`

Five fields with sharply different evidential standing, and what the classifier deliberately does not emit.

**Assertions (2)**

1. No evidence was found on three questions: resolving pronouns and ellipsis before classification, splitting one message into several statements, and how much surrounding context a conversational statement needs. Three separate research angles returned nothing that survived verification, and the only context datapoint anywhere in the evidence base is a 20-30 line window used as an unablated design choice.

   *backed by* `asmt-0001`

2. Four consequences follow for conversational input, all marked DESIGN: conversational input may carry an optional context window used only for reference resolution; a statement whose references cannot be resolved is classified general rather than guessed; splitting a multi-statement message is out of scope for v1 and the caller supplies one statement; and conversational accuracy is expected to be materially below document accuracy, with the two measured separately.

   *backed by* `asmt-0060`

**Source units (2)** `u-src-specification-bf9781a3-0114`, `u-src-specification-bf9781a3-0115`

**Traceability** — idempotency key `32466ff41ab3655b2762f3cc997725f3a4cf6aeec3ad635b0d18938d6be801e3` · queue event `q-32466ff41ab3655b` · audits `audit-cand-025`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 26. The evidence register: what is measured, what is design, what is contradicted

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-026-r1` v2

**Slug** `the-evidence-register-what-is-measured-what-is-design-what-is-contradicted`

The specification's account of its own confidence, sorted by what backs each claim -- including the decisions with no measurement behind them and the claims the evidence contradicts.

**Assertions (2)**

1. Further in-house findings: all fifteen labels were exercised for the first time, with event going from 2 to 45, background from 0 to 35 and distinction from 7 to 17. Research-results prose is the hardest source, at type alpha 0.642 against 0.899 for an RFC on a fourth independent corpus. And the definitions separate at all -- fine alpha went from 0.778 to 0.934 across twenty-two runs.

   *backed by* `asmt-0067`

2. Four claims are recorded as contradicted or unsupported by the evidence: that typing improves retrieval -- no source isolates it, zero measured evidence; that fine-to-coarse rollup buys reliability -- the direct experiment does not exist and existing evidence is mixed and confounded; that type-matched pairing improves contradiction detection -- zero evidence in either direction; and structured-output reliability across model families -- zero confirmed claims despite being explicitly researched, which is called the largest open risk for a classifier that must return parseable output from several vendors.

   *backed by* `asmt-0001`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0014</code> — table, exact, not cited</summary>

| Claim | Number |
|---|---|
| **The definition pass is the single largest effect measured** | fine α 0.844 → **0.934**, 8 raters, 160 statements, 100% of paired resamples |
| It came from domain judgment, not from the measurements | sixteen structural designs moved ±0.05 or lost; fourteen rewritten definitions moved +0.090 |
| A second round of refinements landed in the noise | nine further rulings: 0.954 → 0.947, beating the prior version in 36% of resamples |
| Real documents cost about 0.05 against generated statements | 0.894 on 85 statements from three published sources |
| Two labels carry three-quarters of real financial writing | `observation` 44%, `principle` 32% |

*(38 further rows in the stored grid.)*

</details>

**Source units (2)** `u-src-specification-bf9781a3-0133`, `u-src-specification-bf9781a3-0135`

**Traceability** — idempotency key `1d7b2ed9f7dd823066a9ec39b5d029bbbca0b076cacd0153c1aca24c760a0307` · queue event `q-1d7b2ed9f7dd8230` · audits `audit-cand-026`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 27. The codebook's measurements, carried from its tables

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-027-r1` v2

**Slug** `the-codebook-s-measurements-carried-from-its-tables`

The label-to-coarse mapping, the per-label anchor kappas and the headline reliability, each cited to a CELL of the table it comes from rather than to a quoted row. The reliability figures are this codebook's own in-house measurement.

**Assertions (3)**

1. The codebook maps fifteen fine labels onto six coarse types: `observation` to case; `event` to case; `obligation` to method; `prohibition` to method; `decision` to method; `procedure` to method; `recommendation` to method; `definition` to concept; `distinction` to concept; `background` to concept; `principle` to model; `architecture` to system; `formula` to model; `assumption` to model; `dependency` to system.

   *backed by* `asmt-0001`

2. Four of the codebook's fine labels carry a measured anchor kappa: `background` 0.87, `definition` 0.81, `observation` 0.79 and `procedure` 0.74. Every other label is marked [DESIGN] and rests on reasoning rather than measurement.

   *backed by* `asmt-0001`

3. The four measured labels are anchored on CoreSC categories and marked [VERIFIED]: `observation` on CoreSC `Observation`, `procedure` on `Method`, `definition` on `Object` and `background` on `Background`. The distinction between [VERIFIED] and [DESIGN] is the specification's own account of how much of the codebook rests on evidence.

   *backed by* `asmt-0001`

**Assets carried with this entry (3)** — 3 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0002</code> — table, exact, not cited</summary>

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `method` | What is done, required, forbidden, advised, or settled? |
| `concept` | What does this term mean? |
| `model` | Why does this hold, what does it rest on, and how is it computed? |
| `system` | What is the thing built from, and what does it need to run? |

*(1 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0003</code> — table, exact</summary>

| Fine label | Coarse | Anchor κ | Anchored on |
|---|---|---|---|
| `observation` | case | **0.79** | CoreSC `Observation` [VERIFIED] |
| `event` | case | — | [DESIGN] — concrete by construction (actor + time) |
| `obligation` | method | — | [DESIGN] — deontic modal is a surface cue |
| `prohibition` | method | — | [DESIGN] — deontic modal is a surface cue |
| `decision` | method | — | [DESIGN] — a settled choice governs what happens next; note it is the one `rule` label with NO deontic modal to key on (§3.3) |

*(10 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0005</code> — table, exact, not cited</summary>

| type | n | bits | reading |
|---|---|---|---|
| `dependency` | 7 | 1.84 | status carries almost everything |
| `procedure` | 48 | 1.74 |   |
| `recommendation` | 94 | 1.73 |   |
| `principle` | 44 | 1.72 |   |
| `architecture` | 18 | 1.53 |   |

*(6 further rows in the stored grid.)*

</details>

**Source units (3)** `u-src-specification-bf9781a3-0137`, `u-src-specification-bf9781a3-0138`, `u-src-specification-bf9781a3-0139`

**Traceability** — idempotency key `bd3a0f96200ee29baef4c04652c770311f734202a876c04d4080dc975d1442fa` · queue event `q-bd3a0f96200ee29b` · audits `audit-cand-027`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 28. Statement classifier: measured reliability and evidence convention

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-028-r1` v2

**Slug** `statement-classifier-measured-reliability-and-evidence-convention`

What the classifier's agreement figures are, on which corpora and with how many raters, and the three-way labelling scheme the specification uses to mark what backs each of its claims. The figures are reproducibility among model raters on this codebook; no human gold set exists.

**Assertions (1)**

1. Current measured reliability, from eight blind raters using the codebook verbatim with no answer key in existence: inter-rater Krippendorff alpha is 0.934 on 160 statements from eight generated sources and 0.894 on 85 statements from three published documents. The form field reaches 1.000, status 0.861-0.906, and scope 0.799-0.940.

   *backed by* `asmt-0068`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0001</code> — table, exact, not cited</summary>

| corpus | α |
|---|---|
| 160 statements from eight generated sources | **0.934** |
| 85 statements from three published documents | **0.894** |
| `form` field | **1.000** |
| `status` field | 0.861–0.906 |
| `scope` field | 0.799–0.940 |

</details>

**Source units (1)** `u-src-specification-bf9781a3-0002`

**Traceability** — idempotency key `607543990d0625e46e8dd8c6666e0035b21152b3e0c2c501807c037b42bced35` · queue event `q-607543990d0625e4` · audits `audit-cand-028`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 29. Per-category reliability varies twofold, and abstract categories are worst

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-029-r1` v2

**Slug** `per-category-reliability-varies-twofold-and-abstract-categories-are-worst`

The measured regularity that governs how every definition in this codebook had to be written, and the three rules it imposes.

**Assertions (1)**

1. The second and third consequences of the reliability spread: any category that cannot be written as a surface test should be expected to land near 0.45 regardless of codebook quality, and per-category agreement must be reported separately in evaluation, because a single aggregate number hides exactly the failure this spread predicts.

   *backed by* `asmt-0073`

**Source units (1)** `u-src-specification-bf9781a3-0015`

**Traceability** — idempotency key `c364e4a8a156d2e2d93fbf4b7a8790e07cfd0513ba923788817ad90a3380f68e` · queue event `q-c364e4a8a156d2e2` · audits `audit-cand-029`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 30. The `general` residual: assign by code, never by confidence

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-030-r1` v2

**Slug** `the-general-residual-assign-by-code-never-by-confidence`

Why the residual label is hidden from the model and why self-reported confidence cannot trigger it, with the threshold experiment that settles it and the generalization that follows.

**Assertions (4)**

1. The general label is assigned by code. It is never offered as a label, never named in the prompt, and has no definition the model can see.

   *backed by* `asmt-0074`

2. Self-reported confidence does not work as the trigger for general, and this was tested directly. Raters scored all fifteen labels 0-100 on the full corpus and code assigned general when no label cleared a bar or when several did: picking one label directly reaches alpha 0.934; argmax over the scores 0.930 with 0 per cent sent to general; margin at least 5 gives 0.893 at 4 per cent; margin at least 20 gives 0.866 at 25 per cent; an absolute threshold of 75 gives 0.892 at 42 per cent; a threshold of 90 gives 0.605 at 86 per cent; and a threshold of 95 gives 0.140 at 99 per cent.

   *backed by* `asmt-0076`

3. Two findings from the abstention experiment: the ordering is sound, since argmax over the scores reaches 0.930, statistically level with asking for one label; and every abstention rule loses.

   *backed by* `asmt-0077`

4. The reason abstention fails is not miscalibration: raters disagree about their own uncertainty more than they disagree about the label. Eight raters can all pick procedure and score it 95, 88, 72, 91, 60, 85, 78 and 93; under any threshold some abstain and some do not, so a statement they unanimously agreed on becomes a disagreement between procedure and general. Abstention does not filter noise, it manufactures it, by adding a second judgement noisier than the first.

   *backed by* `asmt-0078`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0004</code> — table, exact, not cited</summary>

| rule | α | share sent to `general` |
|---|---|---|
| pick one label directly | **0.934** | — |
| score all fifteen, take the highest | 0.930 | 0% |
| margin ≥ 5 between first and second | 0.893 | 4% |
| margin ≥ 20 | 0.866 | 25% |
| absolute threshold 75 | 0.892 | 42% |

*(2 further rows in the stored grid.)*

</details>

**Source units (4)** `u-src-specification-bf9781a3-0016`, `u-src-specification-bf9781a3-0018`, `u-src-specification-bf9781a3-0019`, `u-src-specification-bf9781a3-0020`

**Traceability** — idempotency key `77da4b16bd739da73268ea4e1f867cd73f9712039bca5b15bec456c4ff9dae75` · queue event `q-77da4b16bd739da7` · audits `audit-cand-030`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 31. The `status` field: floated, proposed, evidenced, settled

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-031-r1` v2

**Slug** `the-status-field-floated-proposed-evidenced-settled`

The four-rung epistemic-maturity field that replaced a coarse type, its measured reliability, and where it carries information type does not.

**Assertions (9)**

1. Status is one field carried by every type, taking the values floated, proposed, evidenced and settled. Floated is a point raised without being worked out -- to act on it you would have to invent the details yourself. Proposed is one approach, specified enough to build or test, with nothing validating it. Evidenced means something backs it and the backing is what makes it hold. Settled means indisputable, not the kind of thing the next study overturns.

   *backed by* `asmt-0082`

2. Each rung of the status ladder adds a different thing: floated puts a point on the table, proposed adds specification, evidenced adds evidence, settled adds certainty. The test separating the first two is the one used throughout the codebook -- could you act on this sentence as written, or would you first have to invent the parameters?

   *backed by* `asmt-0001`

3. The status ladder was tested on 160 fresh statements from eight sources with four blind raters and reaches alpha 0.896, higher than the type taxonomy scores on the same items at 0.877. Per rung: floated 0.938, settled 0.914, evidenced 0.906, proposed 0.851.

   *backed by* `asmt-0083`

4. Floated and proposed separate cleanly at 2 disagreeing rater-pairs, the least confused pair in the ladder. This was predicted to be the weak boundary on the reasoning that both are hedged and differ only by degree of specification, and the prediction was wrong. Merging them changes alpha by +0.001, so the fourth rung costs nothing and buys resolution. The real trouble is at the top: evidenced against settled at 21 and evidenced against proposed at 20.

   *backed by* `asmt-0084`

5. The gain from status as a field is that an idea's lifecycle stops being a retyping. A statement begins as floated, becomes proposed once it names its parameters, evidenced when the backtest holds, and may harden to settled. As separate types that path required changing what the statement is; as a status it is an update, which is what actually happens -- and it makes a query like 'show me every principle still at proposed' a query rather than an archaeology exercise.

   *backed by* `asmt-0085`

6. Asking for status does not cost type agreement -- it improves it. On the same 160 items, raters asked for type alone reached fine alpha 0.841 while raters asked for type and status reached 0.877, with coarse moving from 0.840 to 0.896. This was the main risk in the two-field design and it inverted. The likely mechanism is unproven: with nowhere to record how established a statement is, raters were folding that judgment into the type choice. It is the largest effect of its kind measured here, but on four raters with no confidence intervals, so the direction is more solid than the magnitude.

   *backed by* `asmt-0086`

7. Status is not a restatement of type, but its value is concentrated. Cramér's V is 0.595 and mutual information 0.845 of 1.721 bits, so 49 per cent of status is predictable from type and 51 per cent is not -- dependent, not collapsed. The same test was run because the published two-axis design this spec cites failed when its axes turned out statistically dependent and collapsed into a few cells.

   *backed by* `asmt-0087`

8. The independent half of status is concentrated by type, measured as residual entropy of status given type: dependency 1.84 bits on n=7, procedure 1.74 on n=48, recommendation 1.73 on n=94, principle 1.72 on n=44, architecture 1.53, distinction 1.39, decision 1.18, event 0.82, background 0.50, observation 0.19 at 97 per cent evidenced, and definition 0.00 on n=40 at 100 per cent settled. Status earns its place on proposals, approaches and causal claims; on definition it is a constant. That is an argument for scoping the field rather than dropping it, and v1 does not act on it -- it asks for status on every type.

   *backed by* `asmt-0088`

9. The n/a status value is nearly unused: 9 of 640, or 1.4 per cent. Status applies to almost every statement raters saw, including rules and events. The one exception is general, where half the assignments were n/a -- consistent with general being a residual rather than a kind.

   *backed by* `asmt-0089`

**Source units (9)** `u-src-specification-bf9781a3-0027`, `u-src-specification-bf9781a3-0028`, `u-src-specification-bf9781a3-0029`, `u-src-specification-bf9781a3-0030`, `u-src-specification-bf9781a3-0031`, `u-src-specification-bf9781a3-0032`, `u-src-specification-bf9781a3-0033`, `u-src-specification-bf9781a3-0034`, `u-src-specification-bf9781a3-0035`

**Traceability** — idempotency key `192bfced545d3c5eb2c49f3a4a7a2b739e377c01d216191c4612c0f95a00da17` · queue event `q-192bfced545d3c5e` · audits `audit-cand-031`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 32. The fifteen label definitions

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-032-r1` v2

**Slug** `the-fifteen-label-definitions`

The codebook itself: each label's surface cue and its explicit exclusions, stated so a rater can check a sentence against them without inferring intent. This is the content the specification's own evidence identifies as determining whether the classifier works.

**Assertions (3)**

1. Background was previously written as a positive category -- context a reader needs, presented as generally accepted -- which describes a large share of all expository prose, and it collided with event 11 times, obligation 4 and principle 4 on the first corpus that exercised it. That is why it is now written as a residual.

   *backed by* `asmt-0095`

2. Pairwise distinction rules are the bulk of a working codebook, not a garnish: the scheme that reached kappa 0.71 shipped 75 of them alongside a decision tree, in 111 pages of guidelines. This specification's nineteen rules cover the pairs judged to genuinely collide; that judgment is the author's and is worth challenging, and a pair that turns out to collide in practice should be added to §3.3 rather than patched into a definition.

   *backed by* `asmt-0001`

3. Assumption is judged high value for this corpus specifically: quantitative models fail at their assumptions far more often than at their arithmetic, and assumptions are usually the least recorded part of a model. This is marked DESIGN.

   *backed by* `asmt-0097`

**Source units (1)** `u-src-specification-bf9781a3-0071`

**Traceability** — idempotency key `0b470cab19c6e7207702a8d784a864357e8b3c147fb99226d592fe4e7ce0f84f` · queue event `q-0b470cab19c6e720` · audits `audit-cand-032`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 33. Pairwise separations between colliding labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-033-r1` v2

**Slug** `pairwise-separations-between-colliding-labels`

The rules that bound each label against the ones it collides with, several carrying the measured collision count that prompted them, plus two any-label overrides.

**Assertions (1)**

1. RULE -- the reassurance marker: procedures and principles do not have feelings. Language that soothes, warns off, or manages the reader's reaction -- don't panic, no need to worry, don't stress, ignore me -- marks the sentence as advice from a person, not an operational instruction or a standing relation, and routes to recommendation. This is marked DESIGN.

   *backed by* `asmt-0130`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0011</code> — table, exact, not cited</summary>

|   | fine α | coarse α |
|---|---|---|
| single choice of fifteen | **0.877** | **0.896** |
| this mechanism, resolved by the priority order below | 0.785 | 0.805 |

</details>

**Source units (1)** `u-src-specification-bf9781a3-0094`

**Traceability** — idempotency key `beb13ecee109ffb2d80c69a4c91c49ce9779d8b4d459b1a35562f8984e3f03de` · queue event `q-beb13ecee109ffb2` · audits `audit-cand-033`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 34. Evaluation, and the pre-registered condition for abandoning the classifier

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-034-r1` v2

**Slug** `evaluation-and-the-pre-registered-condition-for-abandoning-the-classifier`

Why the acceptance test must be human agreement, what must be measured, and the negative evidence that produced a kill criterion written before any results exist.

**Assertions (3)**

1. The definition pass is the single largest effect measured: with 8 raters on 160 statements from eight sources, the codebook before the definition pass scored fine alpha 0.844 with unanimity 0.72, and after it scored 0.934 with unanimity 0.86, 95 per cent CI [0.905, 0.956], winning in 100 per cent of 400 paired resamples. On a 40-statement subset the same codebook reaches 0.947 to 0.954.

   *backed by* `asmt-0121`

2. The definition-pass gain came from domain judgment, not from the measurements: sixteen structural designs moved plus or minus 0.05 or lost, while fourteen rewritten definitions moved +0.090. A second round of refinements landed in the noise -- nine further rulings took 0.954 to 0.947, beating the prior version in 36 per cent of resamples.

   *backed by* `asmt-0122`

3. On real published documents -- 85 statements extracted from Sharpe's The Arithmetic of Active Management (1991), De Bondt and Thaler's Does the Stock Market Overreact? (1985), and a Goldman Sachs market note -- fine alpha is 0.894 with 95 per cent CI [0.840, 0.942]. Real prose costs roughly 0.05 against generated statements.

   *backed by* `asmt-0123`

**Assets carried with this entry (2)** — 2 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0013</code> — table, exact</summary>

**Headline, measured with 8 raters on 160 statements from eight sources:**

|   | fine α | unanimity |
|---|---|---|
| codebook before the definition pass | 0.844 | 0.72 |
| **codebook after the definition pass** | **0.934** | **0.86** |

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0014</code> — table, exact, not cited</summary>

| Claim | Number |
|---|---|
| **The definition pass is the single largest effect measured** | fine α 0.844 → **0.934**, 8 raters, 160 statements, 100% of paired resamples |
| It came from domain judgment, not from the measurements | sixteen structural designs moved ±0.05 or lost; fourteen rewritten definitions moved +0.090 |
| A second round of refinements landed in the noise | nine further rulings: 0.954 → 0.947, beating the prior version in 36% of resamples |
| Real documents cost about 0.05 against generated statements | 0.894 on 85 statements from three published sources |
| Two labels carry three-quarters of real financial writing | `observation` 44%, `principle` 32% |

*(38 further rows in the stored grid.)*

</details>

**Source units (3)** `u-src-specification-bf9781a3-0125`, `u-src-specification-bf9781a3-0126`, `u-src-specification-bf9781a3-0127`

**Traceability** — idempotency key `31099d6a13db80ef0a2563f8af181c880ada8c90b50997c9a7a405f07d37367a` · queue event `q-31099d6a13db80ef` · audits `audit-cand-034`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 35. The evidence register: what is measured, what is design, what is contradicted

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-035-r1` v2

**Slug** `the-evidence-register-what-is-measured-what-is-design-what-is-contradicted`

The specification's account of its own confidence, sorted by what backs each claim -- including the decisions with no measurement behind them and the claims the evidence contradicts.

**Assertions (1)**

1. Two labels carry three-quarters of real financial writing: observation at 44 per cent and principle at 32 per cent. Their boundary is judged irreducible rather than ill-defined -- it accounts for 42 per cent of all disagreement on real documents, after seven attempts to separate it.

   *backed by* `asmt-0125`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0014</code> — table, exact, not cited</summary>

| Claim | Number |
|---|---|
| **The definition pass is the single largest effect measured** | fine α 0.844 → **0.934**, 8 raters, 160 statements, 100% of paired resamples |
| It came from domain judgment, not from the measurements | sixteen structural designs moved ±0.05 or lost; fourteen rewritten definitions moved +0.090 |
| A second round of refinements landed in the noise | nine further rulings: 0.954 → 0.947, beating the prior version in 36% of resamples |
| Real documents cost about 0.05 against generated statements | 0.894 on 85 statements from three published sources |
| Two labels carry three-quarters of real financial writing | `observation` 44%, `principle` 32% |

*(38 further rows in the stored grid.)*

</details>

**Source units (1)** `u-src-specification-bf9781a3-0129`

**Traceability** — idempotency key `ba2f33580acf7d2625f3c499dc8d0dacc92f300b034f1ea5c5bf20fbd6e120f8` · queue event `q-ba2f33580acf7d26` · audits `audit-cand-035`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 36. Labels cut from the taxonomy, and which cuts the data justified

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-036-r1` v2

**Slug** `labels-cut-from-the-taxonomy-and-which-cuts-the-data-justified`

Four labels were removed. One removal was measured; three were editorial and the specification says so. Two gaps remain.

**Assertions (1)**

1. The claim coarse type was removed because it contradicted the contract. An earlier revision had a claim coarse type whose three labels -- fact, finding and proposition -- differed mainly by how established a statement was, which conflicts with §1's statement that the classifier does not judge truth and that epistemic status lives elsewhere.

   *backed by* `asmt-0081`

**Source units (1)** `u-src-specification-bf9781a3-0026`

**Traceability** — idempotency key `b830c5949bb062ee134a4351b77b44a455664467d8a8970b82db67281871e5ea` · queue event `q-b830c5949bb062ee` · audits `audit-cand-036`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 37. Statement classifier: measured reliability and evidence convention

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-037-r1` v2

**Slug** `statement-classifier-measured-reliability-and-evidence-convention`

What the classifier's agreement figures are, on which corpora and with how many raters, and the three-way labelling scheme the specification uses to mark what backs each of its claims. The figures are reproducibility among model raters on this codebook; no human gold set exists.

**Assertions (2)**

1. The statement classifier assigns a knowledge type to a short statement: one statement in, one classification record out. It works on statements extracted from documents and on statements taken from conversation.

   *backed by* `asmt-0129`

2. The specification uses a three-way evidence convention. A claim marked VERIFIED survived three-vote adversarial verification against a primary source, with the study, the number and the sample named inline. MEASURED means it comes from the in-house runs, which measured this codebook rather than a published one. DESIGN means an engineering decision with no supporting measurement. Nothing is presented as evidence-backed unless a number is attached to it.

   *backed by* `asmt-0069`

**Source units (2)** `u-src-specification-bf9781a3-0001`, `u-src-specification-bf9781a3-0004`

**Traceability** — idempotency key `d6d1bf88d3743f943538796808b0a8cce3130ab8b6ac129535bb577f015b8aab` · queue event `q-d6d1bf88d3743f94` · audits `audit-cand-037`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 38. Statement classifier: the contract

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-038-r1` v2

**Slug** `statement-classifier-the-contract`

The interface, the record it returns, and the two things it refuses to do. Stated as the specification states it, so a consumer can build against it.

**Assertions (3)**

1. Classifications are appended, never overwritten. A classification is a pure function of (statement, prompt_version, classifier_model); re-running with a different triple appends a new record rather than replacing the old one, and consumers pick the record whose stamps they trust.

   *backed by* `asmt-0071`

2. The classifier does not judge truth. It answers what kind of statement this is, never whether it is correct; epistemic status lives elsewhere.

   *backed by* `asmt-0072`

3. The output record carries the statement hash, the fine and coarse labels, the per-label boolean tests with a tests_fired count and a multi_fire flag, status, form, modality, flags, provenance, and four stamps: taxonomy_version, prompt_version, classifier_model and classified_at.

   *backed by* `asmt-0070`

**Source units (3)** `u-src-specification-bf9781a3-0008`, `u-src-specification-bf9781a3-0009`, `u-src-specification-bf9781a3-0007`

**Traceability** — idempotency key `7d133acfa13baa06d6f56ef89cecdd9bc9186b1f87ac744a8fec5bcb74fdb4bd` · queue event `q-7d133acfa13baa06` · audits `audit-cand-038`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 39. The `general` residual: assign by code, never by confidence

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-039-r1` v2

**Slug** `the-general-residual-assign-by-code-never-by-confidence`

Why the residual label is hidden from the model and why self-reported confidence cannot trigger it, with the threshold experiment that settles it and the generalization that follows.

**Assertions (2)**

1. A named fallback given to the model is catastrophic: four frontier models given one plus the instruction to assign it for unknown cases recorded 96.1 per cent agreement with Fleiss kappa -0.001 and identified the minority class zero times, on MultiSoc-4D with over 58,000 comments. Whatever triggers general, the model must not see it. This is marked VERIFIED.

   *backed by* `asmt-0075`

2. This is the third measured instance of one pattern, after booleans plus priority resolution at -0.092 and interior tiers at -0.11: anything that turns one classification decision into two costs more in the second step than it gains in the first.

   *backed by* `asmt-0079`

**Source units (2)** `u-src-specification-bf9781a3-0017`, `u-src-specification-bf9781a3-0021`

**Traceability** — idempotency key `00f6cb8797fefec729a0bf0fbfa5025dbcb2eb1fb4f8a38465108f4abc5870b6` · queue event `q-00f6cb8797fefec7` · audits `audit-cand-039`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 40. Labels cut from the taxonomy, and which cuts the data justified

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-040-r1` v2

**Slug** `labels-cut-from-the-taxonomy-and-which-cuts-the-data-justified`

Four labels were removed. One removal was measured; three were editorial and the specification says so. Two gaps remain.

**Assertions (1)**

1. Two gaps follow from the cuts, both routed to general. First, the model coarse type is left with exactly one fine label, so for that branch the fine and coarse tiers carry identical information -- a degenerate tier, harmless but worth knowing; this is later superseded, as model now carries five labels. Second, permission-shaped statements have no home: a sentence like 'Analysts may exceed the intraday limit provided the book is flat at close' carries a deontic modal but is neither required nor prohibited, so it will land in general or be pulled into obligation by the modal. The spec advises watching general's share for permission-heavy corpora such as policy documents.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0024`

**Traceability** — idempotency key `47fd6e48d09349a4ef38950df3c7813ff28f560422ab8317b0db5a8f2490eace` · queue event `q-47fd6e48d09349a4` · audits `audit-cand-040`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 41. The `status` field: floated, proposed, evidenced, settled

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-041-r1` v2

**Slug** `the-status-field-floated-proposed-evidenced-settled`

The four-rung epistemic-maturity field that replaced a coarse type, its measured reliability, and where it carries information type does not.

**Assertions (1)**

1. Provenance is a separate field and is not classified. Where a record came from -- chat or document, human or model, which thread -- is known at ingestion, so recording it costs no agreement because nobody infers it. It is not status's job: status says how firmly a statement is held now, provenance says where it was born. Both are worth having; only one of them can be got wrong.

   *backed by* `asmt-0090`

**Source units (1)** `u-src-specification-bf9781a3-0036`

**Traceability** — idempotency key `f621e77d8e231cd4e71d7999a3b0fb25b4b330f6e8f025fa2ad1cb5c68e77ada` · queue event `q-f621e77d8e231cd4` · audits `audit-cand-041`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 42. The second collision test was confounded by its item set

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-042-r1` v2

**Slug** `the-second-collision-test-was-confounded-by-its-item-set`

A headline improvement, and the control that shows it came from the items rather than the taxonomy. Both are kept.

**Assertions (1)**

1. One risk the revision introduces: principle can be read normatively. 'Prefer small reversible steps' is a principle in ordinary English but is advice, not an explanation, so §3.3 carries an explicit principle-against-obligation separation for exactly that.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0043`

**Traceability** — idempotency key `9128f76247dec98be205c68b515e3616388909379693284a7a09705247ba0bb2` · queue event `q-9128f76247dec98b` · audits `audit-cand-042`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 43. A scope-judging test for `principle` was measured and rejected

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-043-r1` v2

**Slug** `a-scope-judging-test-for-principle-was-measured-and-rejected`

A design change that was written, tested and reversed, and what its failure confirms about non-surface criteria.

**Assertions (2)**

1. The rejection confirms the §2.3 prediction on this codebook, on the label §2.3 named: a criterion that cannot be checked against the surface of the sentence introduces a judgment, and the judgment does not converge -- even when the criterion is correct in every individual case. The causal-diagnosis gap it was written for is real and remains open; the spec judges it not worth a scope judgment to close.

   *backed by* `asmt-0092`

2. Definitions must be written as surface tests, not judgment calls. Concretely-described features reached F1 above 0.60 while features requiring interpretive inference fell below 0.30, and model difficulty tracked human inter-coder difficulty at r = 0.61, so human disagreement is the practical ceiling. Measured over 7 models, 121 features and 567 excerpts.

   *backed by* `asmt-0093`

**Source units (2)** `u-src-specification-bf9781a3-0052`, `u-src-specification-bf9781a3-0054`

**Traceability** — idempotency key `3a05d0a3a91beac79e282f793b44b55b4c4f245e43dab2a9fd10a40c75f7dd80` · queue event `q-3a05d0a3a91beac7` · audits `audit-cand-043`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 44. Codebook depth beats label count, but is not sufficient on its own

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-044-r1` v2

**Slug** `codebook-depth-beats-label-count-but-is-not-sufficient-on-its-own`

The three published findings that justify writing definitions as surface tests and writing them at length.

**Assertions (1)**

1. The exemplars are drawn from quantitative finance and LLM/ML research because those are the domains the classifier runs on, and the spec notes the drift: the anchor categories were measured on chemistry and computational-linguistics papers, so the kappa figures transfer to these definitions only as far as the category shapes do. §9 records this as a weakness in the evidence base, not as something the exemplars fix.

   *backed by* `asmt-0001`

**Source units (1)** `u-src-specification-bf9781a3-0057`

**Traceability** — idempotency key `c4f46c133b56c061fafb75daf215da228f240a802e343b83e8ee55ecbfcb31b6` · queue event `q-c4f46c133b56c061` · audits `audit-cand-044`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 45. The fifteen label definitions

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-045-r1` v2

**Slug** `the-fifteen-label-definitions`

The codebook itself: each label's surface cue and its explicit exclusions, stated so a rater can check a sentence against them without inferring intent. This is the content the specification's own evidence identifies as determining whether the classifier works.

**Assertions (3)**

1. Background was previously written as a positive category -- context a reader needs, presented as generally accepted -- which describes a large share of all expository prose, and it collided with event 11 times, obligation 4 and principle 4 on the first corpus that exercised it. That is why it is now written as a residual.

   *backed by* `asmt-0095`

2. Pairwise distinction rules are the bulk of a working codebook, not a garnish: the scheme that reached kappa 0.71 shipped 75 of them alongside a decision tree, in 111 pages of guidelines. This specification's nineteen rules cover the pairs judged to genuinely collide; that judgment is the author's and is worth challenging, and a pair that turns out to collide in practice should be added to §3.3 rather than patched into a definition.

   *backed by* `asmt-0001`

3. Assumption is judged high value for this corpus specifically: quantitative models fail at their assumptions far more often than at their arithmetic, and assumptions are usually the least recorded part of a model. This is marked DESIGN.

   *backed by* `asmt-0097`

**Source units (3)** `u-src-specification-bf9781a3-0069`, `u-src-specification-bf9781a3-0077`, `u-src-specification-bf9781a3-0075`

**Traceability** — idempotency key `bc2cce71661203ef819dd966928bc81026eb41cc7bb54b420a3e41b62310df13` · queue event `q-bc2cce71661203ef` · audits `audit-cand-045`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 46. Pairwise separations between colliding labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-046-r1` v2

**Slug** `pairwise-separations-between-colliding-labels`

The rules that bound each label against the ones it collides with, several carrying the measured collision count that prompted them, plus two any-label overrides.

**Assertions (1)**

1. RULE -- the reassurance marker: procedures and principles do not have feelings. Language that soothes, warns off, or manages the reader's reaction -- don't panic, no need to worry, don't stress, ignore me -- marks the sentence as advice from a person, not an operational instruction or a standing relation, and routes to recommendation. This is marked DESIGN.

   *backed by* `asmt-0130`

**Source units (3)** `u-src-specification-bf9781a3-0091`, `u-src-specification-bf9781a3-0092`, `u-src-specification-bf9781a3-0093`

**Traceability** — idempotency key `f7cdfb3315629fa528018d0fc337ebeab1a296eaae66b44680d5ff23a8592251` · queue event `q-f7cdfb3315629fa5` · audits `audit-cand-046`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 47. How the classifier is asked, and why its mechanism measured worse

`create_or_update` · knowledge state **contested** · status `ready` · candidate `cand-047-r1` v2

**Slug** `how-the-classifier-is-asked-and-why-its-mechanism-measured-worse`

The boolean-battery mechanism, the published evidence it was inferred from, the in-house test that refuted the inference, and the one property that keeps it in the design anyway.

**Assertions (7)**

1. Two resolution outcomes are defined: if no test fires the result is general; if two or more coarse types fire, resolve by priority and set multi_fire. A multi-fire statement is a candidate for splitting into two statements.

   *backed by* `asmt-0102`

2. The prompt is a frozen, versioned artifact. Prompt wording alone swung classification accuracy by 26 to 36 points on an interpretive six-class task with temperature 0 and formatting held constant -- 20 semantically equivalent prompts produced 0.546 to 0.808 on one model and 0.392 to 0.756 on another -- and the same study found interpretive tasks far more prompt-sensitive than knowledge-anchored ones. Any change to the prompt string is a prompt_version bump, records carry the version they were produced under, and re-wording without bumping is a defect.

   *backed by* `asmt-0103`

3. Tests are emitted as named boolean fields -- no lettered options and no ordered menu -- because presenting options as A/B/C/D inherits selection bias, and most of the effect comes from the option-ID tokens rather than position: removing the IDs cut recall standard deviation from 5.5 to 1.0 on MMLU. Shuffling does not fix it, at 5.9 against a 5.5 baseline and worse on ARC, and a debiasing instruction barely helps.

   *backed by* `asmt-0104`

4. Majority voting over three models from different families improved agreement with human consensus -- kappa 0.62 plus or minus 0.01 against 0.56 to 0.62 for individual models -- while expanding to five reduced it. Three-model voting is therefore optional and off by default, and when enabled the three must come from different families.

   *backed by* `asmt-0105`

5. The modality field takes required, permitted or prohibited and is populated whenever a deontic modal is present, independent of which type test fired. It is validated only on statements that resolved to rule; otherwise it is retained but not enforced. There is no measured evidence for it: deontic modals are surface cues, which is the property associated with reliable categories, but this specific field has not been evaluated.

   *backed by* `asmt-0106`

6. Provenance is a record of medium, author and source_id: medium is chat, document, transcript or code; author is human or model with the model identifier when known; source_id is the thread, document or file. Nothing here is classified -- every value is known to the ingestion pipeline before the classifier is called, so provenance costs no agreement because it cannot be got wrong by a model that never infers it.

   *backed by* `asmt-0107`

7. Provenance is operationally load-bearing: chat statements classify at fine alpha 0.811 against 0.940 for document statements, on the same codebook and the same run. Without provenance on the record that gap is a fact nobody can act on; with it, a consumer can weight or filter by medium.

   *backed by* `asmt-0108`

**Source units (7)** `u-src-specification-bf9781a3-0099`, `u-src-specification-bf9781a3-0100`, `u-src-specification-bf9781a3-0101`, `u-src-specification-bf9781a3-0102`, `u-src-specification-bf9781a3-0103`, `u-src-specification-bf9781a3-0107`, `u-src-specification-bf9781a3-0108`

**Traceability** — idempotency key `e5720084d1c5b0c20677ff45e39a47216777d1ceda7ba1039ff4c867a8a5d175` · queue event `q-e5720084d1c5b0c2` · audits `audit-cand-047`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 48. Secondary fields: form, provenance, modality and flags

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-048-r1` v2

**Slug** `secondary-fields-form-provenance-modality-and-flags`

Five fields with sharply different evidential standing, and what the classifier deliberately does not emit.

**Assertions (7)**

1. Two flags are defined. negative_result means the statement reports an absence, null or no-effect finding; caveat means the statement limits, scopes or excepts something else. There is no measured evidence for either. negative_result exists because a null finding is not distinguishable from a positive one by embedding similarity -- 'X does not work' and 'X works' are near neighbours -- so without an explicit marker it is unrecoverable downstream. That is a mechanism argument, not a measurement.

   *backed by* `asmt-0109`

2. No confidence score is published. Per-label confidence is elicited internally to drive general assignment but is not part of the output record. Verbalized confidence reliability depends strongly on how the model is asked, with no universal best method across 17 prompt methods, 10 datasets and 11 models spanning 2B to 110B; the best method is model-dependent and small models' confidence is near-independent of their accuracy, and all of it was measured on closed-book QA, never on classification. Uncertainty is expressed structurally instead: tests_fired == 0 is abstention and tests_fired >= 2 is ambiguity.

   *backed by* `asmt-0110`

3. Conversational text is measurably harder. Six frontier models classifying classroom utterances into seven categories reached Cohen's kappa 0.38 to 0.58, where human expert annotators on the same data exceeded 0.90, over 800 stratified utterances. A separate study on support conversations found expert-model weighted kappa median 0.60 against expert-expert 0.58 -- comparable, but on ordinal ratings rather than single-label classification.

   *backed by* `asmt-0112`

4. Few-shot exemplars help, but model-dependently in both size and sign: across six models, kappa gains ranged from +19 points to negative -- one model peaked at three examples then declined with more, another ended below its zero-shot score. Exemplar count is therefore a per-model tuning parameter, which conflicts directly with a single prompt used across families.

   *backed by* `asmt-0001`

5. Inter-model agreement is not evidence of correctness, on two independent demonstrations: four models agreed on 96.1 per cent of labels with Fleiss kappa -0.001 while missing 75 per cent of the minority class; and in a separate study models reached inter-model Krippendorff alpha 0.85 against human-human 0.65 while diverging significantly from human judgment, t(49.42) = 3.615, p below .001, Cohen's d = 0.88. The acceptance test is therefore agreement with human labels, and cross-model agreement is a stability check only.

   *backed by* `asmt-0114`

6. Gold set requirements: both strata sampled separately, document-derived and conversational; rare fine labels deliberately oversampled, otherwise general absorbs them invisibly; and at least two independent human coders, adjudicated, with human-human agreement reported first because it is the ceiling and model numbers are uninterpretable without it.

   *backed by* `asmt-0115`

7. The classifier produces no truth judgment and no relationships between statements. Epistemic maturity is produced -- that is status -- but whether a statement is correct is not, and neither are edges between statements. Relations such as resolved_by and opposes are the natural next layer and are deliberately out of scope for v1.

   *backed by* `asmt-0111`

**Source units (7)** `u-src-specification-bf9781a3-0109`, `u-src-specification-bf9781a3-0110`, `u-src-specification-bf9781a3-0112`, `u-src-specification-bf9781a3-0113`, `u-src-specification-bf9781a3-0116`, `u-src-specification-bf9781a3-0117`, `u-src-specification-bf9781a3-0111`

**Traceability** — idempotency key `74ade3e3022a68781b24b86dbdcec653b16bd764eb9deac392e6e210884f038c` · queue event `q-74ade3e3022a6878` · audits `audit-cand-048`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 49. Conversational statements classify materially worse

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-049-r1` v2

**Slug** `conversational-statements-classify-materially-worse`

The evidence that chat is harder, the exemplar finding that conflicts with a frozen prompt, and the three questions on which no evidence was found.

**Assertions (3)**

1. Metrics required in evaluation: Krippendorff's alpha at the fine tier and the coarse tier reported separately, because raw percentage agreement is biased toward schemes with fewer categories so tiers cannot be compared without chance correction -- and chance-corrected measures are themselves distorted by skew, which a taxonomy with a residual bucket will certainly have. Also required: per-category agreement rather than just aggregate, since a twofold spread is predicted and an aggregate hides it; plus general's share, the multi_fire rate, and per-model divergence.

   *backed by* `asmt-0116`

2. The strongest direct evidence about typed information is negative and human. Two controlled experiments on a shipped information-typing scheme found no effect on task performance: n=65 process operators with effectiveness F(2,62)=1.16 p=.32 and efficiency F(2,62)=2.02 p=.14; and n=76 with no significant effects on accuracy, speed or evaluation scores at all. The only significant effect was subjective preference, and even that did not beat the incumbent text. Scope limit raised by all three verifiers: those studies were powered for large effects only and typing was bundled with six other principles, so this is absence of a large effect, not proof that typing is inert.

   *backed by* `asmt-0117`

3. No source in the reviewed evidence isolates type labels from anything else: every system claiming a typing benefit bundles it with linking, extraction, reranking or temporal invalidation, and the counterfactual -- same corpus, same retriever, labels stripped -- has never been run. The one payoff that replicates across three independent agent-memory systems is temporal validity, not typing.

   *backed by* `asmt-0118`

**Source units (3)** `u-src-specification-bf9781a3-0118`, `u-src-specification-bf9781a3-0120`, `u-src-specification-bf9781a3-0121`

**Traceability** — idempotency key `db4aee3a7bc9041d121c25ce133662a170f53ddbba50d44408a0065a085f5f07` · queue event `q-db4aee3a7bc9041d` · audits `audit-cand-049`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 50. Evaluation, and the pre-registered condition for abandoning the classifier

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-050-r1` v2

**Slug** `evaluation-and-the-pre-registered-condition-for-abandoning-the-classifier`

Why the acceptance test must be human agreement, what must be measured, and the negative evidence that produced a kill criterion written before any results exist.

**Assertions (3)**

1. A kill criterion is pre-registered. Before the classifier is treated as load-bearing: run the ablation -- same corpus, same retriever, same ranking, type labels present versus stripped -- pre-registering the query classes and the minimum effect size; user preference does not count as a gain, written here before results exist because the one scheme that shipped on preference failed on task; and if no query class improves, the classifier is decoration -- keep temporal validity, drop the rest.

   *backed by* `asmt-0119`

2. Batch size does not matter: the same 40 statements rated in batches of 5, 10 and 40 score 0.932, 0.947 and 0.949, so test figures should transfer to one-statement-at-a-time production.

   *backed by* `asmt-0124`

3. Versioning: taxonomy_version changes when labels or their mappings change, prompt_version changes on any prompt edit, and classifier_model records what produced the record. All three are stamped on every record and consumers may filter on them. Changing the taxonomy does not invalidate stored statements, because classifications are appended and a statement may carry several from different versions.

   *backed by* `asmt-0120`

**Source units (3)** `u-src-specification-bf9781a3-0122`, `u-src-specification-bf9781a3-0128`, `u-src-specification-bf9781a3-0123`

**Traceability** — idempotency key `7de90d1c4afeb25cf44e0a8c90b66942dbca131a45613c7e977878abbfd4375d` · queue event `q-7de90d1c4afeb25c` · audits `audit-cand-050`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 51. The evidence register: what is measured, what is design, what is contradicted

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-051-r1` v2

**Slug** `the-evidence-register-what-is-measured-what-is-design-what-is-contradicted`

The specification's account of its own confidence, sorted by what backs each claim -- including the decisions with no measurement behind them and the claims the evidence contradicts.

**Assertions (2)**

1. The register records ten design decisions with no supporting measurement: the five coarse types and their names; the fifteen fine labels, their names and their coarse mappings; the strip test; the principle/recommendation and decision/procedure separations in §3.3; retaining event after three item sets failed to exercise it; the priority order used to resolve multiple firing tests; decomposing this label set into fifteen binary probes specifically; modality, negative_result and caveat; treating general as a code-assigned residual rather than a model-visible label, where the hazard is measured but the mitigation is not; and splitting multi-statement messages being out of scope.

   *backed by* `asmt-0001`

2. Five weaknesses in the evidence itself are recorded: the annotation-reliability figures trace largely to one research lineage rather than to independent replication; all annotation evidence is humans labelling sentences inside full documents while this classifier types short statements shown without their document, and whether agreement transfers up or down is untested -- a claim pointing one way was refuted 0-3; the definitions use quantitative-finance and ML exemplars while every anchor category was measured on chemistry and computational-linguistics papers; the nineteen pairwise separations cover the pairs judged to collide and that judgment is unmeasured, against 75 rules in the scheme that reached kappa 0.71; and the §2.2 reliability numbers are one-vs-rest binary collapses, mechanically higher than the full multi-way agreement of the same scheme at 0.50 to 0.57, so they rank categories reliably but are not absolute targets.

   *backed by* `asmt-0001`

**Source units (2)** `u-src-specification-bf9781a3-0134`, `u-src-specification-bf9781a3-0136`

**Traceability** — idempotency key `19984d5a62e23c44e342b23017356302c201adbdf27b05837f422e977df81b31` · queue event `q-19984d5a62e23c44` · audits `audit-cand-051`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 52. The codebook's measurements, carried from its tables

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-052-r1` v2

**Slug** `the-codebook-s-measurements-carried-from-its-tables`

The label-to-coarse mapping, the per-label anchor kappas and the headline reliability, each cited to a CELL of the table it comes from rather than to a quoted row. The reliability figures are this codebook's own in-house measurement.

**Assertions (1)**

1. The definition pass raised fine-grained inter-rater alpha from 0.844 to 0.934 and unanimity from 0.72 to 0.86, measured with 8 raters on 160 statements drawn from eight sources.

   *backed by* `asmt-0128`

**Assets carried with this entry (2)** — 2 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0001</code> — table, exact, not cited</summary>

| corpus | α |
|---|---|
| 160 statements from eight generated sources | **0.934** |
| 85 statements from three published documents | **0.894** |
| `form` field | **1.000** |
| `status` field | 0.861–0.906 |
| `scope` field | 0.799–0.940 |

</details>

<details><summary><code>tbl-src-specification-bf9781a3-0013</code> — table, exact</summary>

**Headline, measured with 8 raters on 160 statements from eight sources:**

|   | fine α | unanimity |
|---|---|---|
| codebook before the definition pass | 0.844 | 0.72 |
| **codebook after the definition pass** | **0.934** | **0.86** |

</details>

**Source units (1)** `u-src-specification-bf9781a3-0140`

**Traceability** — idempotency key `150bf98e850bccb28d2e947685b59c3e01e3da0504575bf615ad46582c05055e` · queue event `q-150bf98e850bccb2` · audits `audit-cand-052`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 53. Pairwise separations between colliding labels

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-053-r1` v2

**Slug** `pairwise-separations-between-colliding-labels`

The rules that bound each label against the ones it collides with, several carrying the measured collision count that prompted them, plus two any-label overrides.

**Assertions (1)**

1. RULE -- the reassurance marker: procedures and principles do not have feelings. Language that soothes, warns off, or manages the reader's reaction -- don't panic, no need to worry, don't stress, ignore me -- marks the sentence as advice from a person, not an operational instruction or a standing relation, and routes to recommendation. This is marked DESIGN.

   *backed by* `asmt-0130`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-specification-bf9781a3-0010</code> — table, exact, not cited</summary>

| Pair | The test that separates them |
|---|---|
| `observation` / `event` | Was anything measured? An observation records a quantity or behaviour; an event records that something occurred. |
| `event` / `decision` | Was a choice made? An event happened to you; a decision was chosen and constrains later action. |
| `decision` / `obligation` | Is there a modal? An obligation states a standing requirement in modal form; a decision states one was established. If both fit, the modal wins. |
| `decision` / `recommendation` | Settled or proposed? A decision is closed; a recommendation is still advice. |
| `obligation` / `prohibition` | **What to do** versus **what not to do.** Judge by the action demanded, not by grammatical polarity — a negatively-phrased requirement that demands an action is an `obligation`. `[MEASURED]` Both items in the 21-pair collision were compound, carrying a requirement and a forbidding in one sentence; under §2.4 both tests score above 90 and the statement resolves to `general` with `multi_fire`. |

*(19 further rows in the stored grid.)*

</details>

**Source units (1)** `u-src-specification-bf9781a3-0090`

**Traceability** — idempotency key `2ac4cf2265d291ff3c4e9d7d352e0191708367b99e8155103fcfa0de4c810999` · queue event `q-2ac4cf2265d291ff` · audits `audit-cand-053`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

## Assets in full

Every recovered object, shown as it is stored. Indexed at the top under [Assets](#assets); the ones an entry carries are also shown with that entry.

**14 assets** — 14 table. 12 related to at least one unit, 2 related to none.

An asset related to no unit sits in a passage the extraction read and drew nothing from -- the same decision it makes about a paragraph it does not extract from, and not tracked as a defect for either. What an asset is worth is settled by whether the text around it reached an approved entry.

Fidelity is part of the record, because the kinds are not equally trustworthy:

- **exact** (14) — structure recovered from markup the source itself carried — citable as a quote

Evidence cites an asset with `asset_ref {asset_id, row, col}` for a table cell, or `{asset_id}` for a formula. A cell reference resolves to the value **and** the headers governing it, which is what makes a figure checkable rather than merely quoted.

### `src-specification-bf9781a3`

[`normalized.txt`](runs/spec/01_normalized/src-specification-bf9781a3/normalized.txt) · [`assets.jsonl`](runs/spec/01_normalized/src-specification-bf9781a3/assets.jsonl) · [`manifest.json`](runs/spec/01_normalized/src-specification-bf9781a3/manifest.json)

#### `tbl-src-specification-bf9781a3-0001`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 2 units

under *Statement Classifier — Specification v1.0*

| corpus | α |
|---|---|
| 160 statements from eight generated sources | **0.934** |
| 85 statements from three published documents | **0.894** |
| `form` field | **1.000** |
| `status` field | 0.861–0.906 |
| `scope` field | 0.799–0.940 |

Related units: `u-src-specification-bf9781a3-0002`, `u-src-specification-bf9781a3-0140`

#### `tbl-src-specification-bf9781a3-0002`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 2 units

under *2.1 Coarse types*

| Coarse | The question it answers |
|---|---|
| `case` | What happened, on one occasion? |
| `method` | What is done, required, forbidden, advised, or settled? |
| `concept` | What does this term mean? |
| `model` | Why does this hold, what does it rest on, and how is it computed? |
| `system` | What is the thing built from, and what does it need to run? |
| `general` | — assigned by code when no test fires |

Related units: `u-src-specification-bf9781a3-0010`, `u-src-specification-bf9781a3-0137`

#### `tbl-src-specification-bf9781a3-0003`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 5 units

under *2.2 Fine labels, with measured reliability where it exists*

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

*(4 further rows in the stored grid.)*

Related units: `u-src-specification-bf9781a3-0011`, `u-src-specification-bf9781a3-0012`, `u-src-specification-bf9781a3-0137`, `u-src-specification-bf9781a3-0138`, `u-src-specification-bf9781a3-0139`

#### `tbl-src-specification-bf9781a3-0004`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 1 unit

under *2.4 `general`*

| rule | α | share sent to `general` |
|---|---|---|
| pick one label directly | **0.934** | — |
| score all fifteen, take the highest | 0.930 | 0% |
| margin ≥ 5 between first and second | 0.893 | 4% |
| margin ≥ 20 | 0.866 | 25% |
| absolute threshold 75 | 0.892 | 42% |
| **absolute threshold 90** | **0.605** | **86%** |
| absolute threshold 95 | 0.140 | 99% |

Related units: `u-src-specification-bf9781a3-0018`

#### `tbl-src-specification-bf9781a3-0005`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 3 units

under *2.6 `status`, and why `claim` no longer exists*

| type | n | bits | reading |
|---|---|---|---|
| `dependency` | 7 | 1.84 | status carries almost everything |
| `procedure` | 48 | 1.74 |   |
| `recommendation` | 94 | 1.73 |   |
| `principle` | 44 | 1.72 |   |
| `architecture` | 18 | 1.53 |   |
| `distinction` | 9 | 1.39 |   |
| `decision` | 29 | 1.18 |   |
| `event` | 43 | 0.82 |   |
| `background` | 35 | 0.50 |   |
| `observation` | 196 | 0.19 | 97% `evidenced` — near-redundant |
| `definition` | 40 | **0.00** | 100% `settled` — carries nothing |

Related units: `u-src-specification-bf9781a3-0011`, `u-src-specification-bf9781a3-0138`, `u-src-specification-bf9781a3-0139`

#### `tbl-src-specification-bf9781a3-0006`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 1 unit

under *2.7 What the second collision test changed*

|   | fine α | coarse α |
|---|---|---|
| headline, v1 → v2 (taxonomy **and** items changed) | +0.080 | +0.061 |
| **taxonomy alone** (v1 items, both codebooks) | **+0.009** | **−0.075** |
| item set alone (v2 codebook, both item sets) | +0.071 | +0.136 |

Related units: `u-src-specification-bf9781a3-0039`

#### `tbl-src-specification-bf9781a3-0007`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 1 unit

under *2.8 What the third collision test measured*

|   | fine α | coarse α |
|---|---|---|
| 72 results-dense items, v2 codebook (the control) | 0.787 | 0.791 |
| the same 72, v3 codebook | **0.883** | **0.874** |
| 80 mixed items, v2 codebook | 0.858 | 0.927 |
| the same 80, v3 codebook | **0.930** | 0.927 |

Related units: `u-src-specification-bf9781a3-0044`

#### `tbl-src-specification-bf9781a3-0008`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · **related to no unit**

under *2.8 What the third collision test measured*

| v2 | α | v3 | α |
|---|---|---|---|
| `driver` | 0.623 | `principle` | **0.910** |
| `structure` | 0.727 | `architecture` | **0.851** |
| `procedure` | 0.760 | `procedure`, absorbing `technique` | 0.834 |

#### `tbl-src-specification-bf9781a3-0009`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 1 unit

under *2.9 A change that was tested and rejected*

|   | with strip test only | + generality test |
|---|---|---|
| `principle`/`observation` collisions | 17 | **19** |
| fine α, all 152 | 0.904 | 0.901 |
| fine α, results-dense subset | 0.871 | **0.848** |
| fine α, mixed subset | 0.930 | 0.943 |
| `principle` α | 0.861 | **0.797** |
| `principle` assignments | 123 | **77** |

Related units: `u-src-specification-bf9781a3-0050`

#### `tbl-src-specification-bf9781a3-0010`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 13 units

under *3.3 Pairwise separations*

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

*(13 further rows in the stored grid.)*

Related units: `u-src-specification-bf9781a3-0078`, `u-src-specification-bf9781a3-0079`, `u-src-specification-bf9781a3-0080`, `u-src-specification-bf9781a3-0081`, `u-src-specification-bf9781a3-0082`, `u-src-specification-bf9781a3-0083`, `u-src-specification-bf9781a3-0084`, `u-src-specification-bf9781a3-0085` …

#### `tbl-src-specification-bf9781a3-0011`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 2 units

under *4.1 Independent boolean tests, resolved in code*

|   | fine α | coarse α |
|---|---|---|
| single choice of fifteen | **0.877** | **0.896** |
| this mechanism, resolved by the priority order below | 0.785 | 0.805 |

Related units: `u-src-specification-bf9781a3-0094`, `u-src-specification-bf9781a3-0095`

#### `tbl-src-specification-bf9781a3-0012`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · **related to no unit**

under *Measured, verified, cited above*

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

*(4 further rows in the stored grid.)*

#### `tbl-src-specification-bf9781a3-0013`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 2 units

**Headline, measured with 8 raters on 160 statements from eight sources:**  ·  under *Measured on this codebook, in-house*

|   | fine α | unanimity |
|---|---|---|
| codebook before the definition pass | 0.844 | 0.72 |
| **codebook after the definition pass** | **0.934** | **0.86** |

Related units: `u-src-specification-bf9781a3-0125`, `u-src-specification-bf9781a3-0140`

#### `tbl-src-specification-bf9781a3-0014`

table · **exact** · extractor `markdown_tables_v1` · anchored by `own_text` · related to 5 units

under *Measured on this codebook, in-house*

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

*(32 further rows in the stored grid.)*

Related units: `u-src-specification-bf9781a3-0126`, `u-src-specification-bf9781a3-0129`, `u-src-specification-bf9781a3-0130`, `u-src-specification-bf9781a3-0132`, `u-src-specification-bf9781a3-0133`

## Assets not carried by any entry

2 asset(s) sit in a region the extraction read and drew nothing from. That is the same decision it makes about a paragraph it does not extract from, and neither is tracked as a defect. They are shown because they are still the source's content and cost nothing to keep.

### `tbl-src-specification-bf9781a3-0008`

table · **exact** · anchored by `own_text`

under *2.8 What the third collision test measured*

| v2 | α | v3 | α |
|---|---|---|---|
| `driver` | 0.623 | `principle` | **0.910** |
| `structure` | 0.727 | `architecture` | **0.851** |
| `procedure` | 0.760 | `procedure`, absorbing `technique` | 0.834 |

### `tbl-src-specification-bf9781a3-0012`

table · **exact** · anchored by `own_text`

under *Measured, verified, cited above*

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

*(4 further rows in the stored grid.)*
