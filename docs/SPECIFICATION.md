# Knowledge Ingestion Pipeline — Canonical Specification v3.0

**Status:** implementation-ready reference specification, research-grounded
**Supersedes:** specification v2.0 (the pre-research baseline design)
**Primary architectural decision (unchanged from v2 §Header):** every intermediate artifact remains machine-first JSON or JSONL. Human-readable Markdown with YAML front matter is materialized only after the existing leaf engine accepts durable knowledge.

## How to read this document

Every design claim carries a citation:

| Tag | Meaning |
|---|---|
| `v2 §X` | Carried forward from specification v2.0, section X. |
| `R1`–`R4` | Research rounds 1–4 — multi-agent fan-out with **3-vote adversarial verification** per claim. Highest evidence tier. |
| `R5` | Research round 5 — primary sources fetched and quoted, **not** adversarially verified. One tier below R1–R4. |
| `PE` | Production-engineering brief — first-party/vendor documentation, per-fact cited. |
| `SDK` | Claude Code plugin + Anthropic SDK brief. |
| `[NEW — confirm]` | Introduced here, backed by neither v2 nor research. **Requires maintainer confirmation or removal.** |

Research files live in [`../research/`](../research/). Citations point to finding IDs inside them (e.g. `R2 F3` = round 2, finding F3).

Where research **contradicts** v2, the contradiction is stated explicitly rather than silently overwritten.

---

## 1. What changed from v2.0, and why

| # | v2.0 decision | v3.0 decision | Evidence |
|---|---|---|---|
| 1 | Pass 1 extracts **maximally atomic** units (v2 §8.3) | Pass 1 extracts **molecular** units: decontextualized-but-minimal | `R1 A3` — "fully atomic facts are not the right representation" (Gunjal & Durrett, EMNLP Findings 2024) |
| 2 | Atomicity is a quality goal (v2 §8.3) | Atomicity is **not** scored; granularity is a **tunable** calibrated against downstream verifier strength | `R1 A4` (Decomposition Dilemmas, NAACL 2025), `R1 A5` (Claimify, ACL 2025) |
| 3 | 5-dimension 0–3 rubric (v2 §8.5) | Adds Claimify's human-validated **entailment / element-level coverage / decontextualization** evaluation | `R1 A5` — 6,490 sentences, α = 0.72 |
| 4 | Routing on raw embeddings + BM25 (v2 §9.2) | **Contextual enrichment before indexing** — the one evidence-backed technique v2 lacked | `R1 C2` — 49% retrieval-failure reduction (Anthropic 2024); 5–15% in independent replications |
| 5 | 15 relationship labels judged in one step (v2 §10.3) | **Coarse 3-way first, constrained sub-typing second**; the 4-bucket grouping is the trust boundary | `R2 F3` — fine-type classification peaked at 0.401 accuracy; partial/conflicting labels weakest everywhere |
| 6 | Auditor model unspecified (v2 §12) | Auditor **must be reasoning-class**, and a **different model or minimum fresh context** | `R3 F1` (JudgeBench: GPT-4o 56.6% vs o3-mini-high 80.9% on hard correctness), `R3 F4` (self-preference survives anonymization) |
| 7 | Grounding + citation checks by LLM audit (v2 §12.2) | Grounding by **MiniCheck-class specialized checker**; citation accuracy by **deterministic string/line-range matching** | `R4 F1` (GPT-4 accuracy at ~400× lower cost), `R3 F6` |
| 8 | No source-validity screening (v2 §10.4) | Adds **retraction / citation-lineage screening** to evidence weighting | `R2 F8` — 32.2% of paper-mill citations occur post-retraction (JAMA) |
| 9 | `temporal_update` undefined mechanically (v2 §10.3) | Adopts **bi-temporal invalidate-don't-delete** | `R2 F6` — Graphiti/Zep shipped precedent |
| 10 | No ordering discipline for multi-item passes | **Rotate/randomize item order**; both-orders aggregation for pairwise judgments | `R5 T2` (22 pp positional spread), `R3 F3` (17–22% of verdicts flip on swap) |

**Validated without change:** the two-stage match-then-judge structure of Pass 3 (`R2 F1`), the separate omission check (`R1 B1`, `R1 B2`), flat hybrid clustering over eager graph construction (`R1 C3`, `R1 C4`), the adversarial audit as a distinct externally-grounded pass (`R3 F5`–`F7`), raw-source escalation (`R4`), the outbox/idempotency handoff (`PE T3`), and the 20–50-unit batch cap (`R5 T2`).

---

## 2. Purpose

This pipeline ingests heterogeneous files, extracts variable numbers of source-backed knowledge units, routes related units into manageable comparison sets, synthesizes supporting and conflicting evidence, proposes candidate leaves, audits those proposals against the source chain, and hands approved candidates to an existing knowledge-base leaf engine. (v2 §1)

It is designed for generic knowledge domains. Research papers, emails, presentations, contracts, meeting notes, and operational messages use the same pipeline contract even though their unit types and evidence quality differ. (v2 §1)

---

## 3. Core design principles

1. **Raw sources are immutable.** The original file is preserved with a content hash. (v2 §2.1)
2. **Normalization is not summarization.** Pass 0 extracts text and location metadata without deciding what matters. (v2 §2.2)
3. **Knowledge units are molecular and source-backed** — each expresses one proposition that *stands alone* (decontextuality) with the *least added information* needed to do so (minimality). (v2 §2.3 as amended by `R1 A3`)
4. **Variable cardinality is required.** The extractor returns as many units as the source warrants, never a fixed number. (v2 §2.4)
5. **Matching and judgment are separate.** Short canonical statements retrieve likely relationships; context and evidence decide what the relationship is. (v2 §2.5, strongly confirmed by `R2 F1`)
6. **Source independence is explicit.** Multiple artifacts derived from the same underlying study, meeting, or pilot are not counted as independent confirmation. (v2 §2.6)
7. **All intermediate stages are append-only JSONL.** Human readability comes from a trace UI, not from changing storage formats mid-pipeline. (v2 §2.7)
8. **The audit is adversarial and externally grounded.** It attempts to disprove, narrow, or reject the candidate against the source chain — never by asking the proposer to re-read its own output. (v2 §2.8 as sharpened by `R3 F5`)
9. **The existing leaf engine remains the knowledge integrator.** (v2 §2.9)
10. **Every durable assertion is traceable** backward through queue event, audited candidate, assessment, cluster, unit, normalized text location, and original file. (v2 §2.10)
11. **Every automated judgment has a published error rate, and the pipeline is designed to absorb it.** No stage may assume a downstream stage is correct. (`R2 F4`, `R3 F1`, `R4` — see §20)

---

## 4. Terminology

Unchanged from v2 §3, with one amendment:

- **Source / Normalized source / Cluster / Assessment / Candidate leaf / Audit / Queue event / Durable leaf / Source family / Independence group** — as v2 §3.
- **Unit:** one *molecular* knowledge statement and its evidence — minimal, but self-contained enough to be interpreted without its neighbors. (amended per `R1 A3`)

---

## 5. End-to-end flow

```text
Original files
    |
    v
Pass 0 — normalize text and locations                    [code, not LLM]
    |
    v
Pass 1 — extract molecular source-backed units           [LLM, batchable]
    |    + omission/completeness check                   [LLM]
    v
Pass 2 — contextual enrichment, then route and cluster   [LLM enrich + code retrieval]
    |
    v
Pass 3 — match candidates, then judge relationships      [code match + LLM judge]
    |
    v
Pass 4 — generate candidate leaf operations              [LLM]
    |
    v
Pass 5 — adversarial audit and correction                [reasoning LLM + specialized checkers + code]
    |
    v
Step 6 — enqueue approved event to existing leaf engine  [code, not LLM]
    |
    v
Existing leaf engine — merge, bubble, link, update
    |
    v
Durable Markdown + YAML leaf with full provenance
```

(v2 §4, with per-stage execution mode annotated per `R3 F6`, `R4 F1`, `PE T3`.)

---

## 6. Project layout

As v2 §5, with one addition:

```text
project/
  prompts/
  schemas/
  scripts/
  runs/<run_id>/
    00_original_sources/
    01_normalized/<source_id>/
      manifest.json
      normalized.txt
      locator_map.jsonl
      assets/
    02_units/units.jsonl
    02_units/omissions.jsonl          <- NEW: structured omission findings (R1 B2)
    03_clusters/clusters.jsonl
    03_clusters/enriched_units.jsonl  <- NEW: contextualized units for indexing (R1 C2)
    04_assessments/claim_assessments.jsonl
    05_candidates/candidates.initial.jsonl
    06_audit/audits.jsonl
    06_audit/candidates.approved.jsonl
    07_enqueue/enqueue.jsonl
  knowledge_base/
    leaves/<slug>.md
```

---

## 7. Global artifact envelope

Unchanged from v2 §6. Every JSON/JSONL record carries: `schema_version`, `run_id`, `created_at`, `prompt_version`, `model_role`, `artifact_id`, `parent_artifacts`, `content_sha256`, `status`.

Store model/provider metadata in a run manifest: provider, model identifier, decoding settings, SDK version, code commit, prompt hashes, input hashes, token counts, latency, and cost. (v2 §6)

**Addition:** the run manifest must also record, per stage, the **evidence-tier configuration in force** — which checker model performed grounding, whether the auditor differed from the proposer, and the batch size used — because all three materially change the error rate of the output. (`R3 F1`, `R3 F4`, `R5 T2`)

**`content_sha256` covers the assertion, not its labels.** `created_at` and every derived classification field are excluded — the authoritative list is `artifacts.DERIVED_FIELDS`, and the writer and the validator share one copy of it. See §9.3 for why. Schema `3.1.0` introduced this exclusion, so hashes written under `3.0.0` are not comparable with `3.1.0` ones.

---

## 8. Pass 0 — source intake and normalization

### 8.1 Objective

Convert each supported file into deterministic plain text an LLM can consume, preserving enough location information to return to the exact portion of the original. **Code-driven, not LLM-driven.** (v2 §7.1)

### 8.2 Inputs

PDF, DOCX, PPTX, XLSX/CSV, HTML, Markdown, plain text, EML/MSG, exported chat, image, audio transcript, or other connector payload. (v2 §7.2)

### 8.3 Recommended normalizer

**Docling** (IBM Research / LF AI & Data, MIT license) is the recommended default. Its `DoclingDocument` model attaches to every `DocItem` a `prov` list carrying `page_no`, `bbox` (with `coord_origin`), and `charspan` — **precisely the locator-map contract this spec requires** (§8.6). It parses PDF, DOCX, PPTX, XLSX, HTML, EPUB, images, audio, LaTeX, and email. Throughput 0.6–1.34 pages/s on CPU. (`PE T2`)

**Honest tradeoff:** Docling does **not** appear in OmniDocBench's published end-to-end tables (CVPR 2025). Among benchmarked pipeline tools MinerU leads decisively (0.055 text-edit distance vs Marker's 0.157). Docling is selected for its provenance model, format breadth, and license — **not** for demonstrated parsing supremacy, which is `[UNVERIFIED]`. (`PE T2`)

`[NEW — confirm]` **Two-tier normalizer.** Docling is tried first; when unavailable, lightweight pure-Python parsers (pypdf, python-docx, python-pptx, openpyxl) handle the same formats at a few MB instead of a multi-GB ML stack. The price is real and must be recorded: the fallback yields **page/slide/sheet-level provenance only, no bounding boxes**. The `normalizer` field in each manifest records which tier produced the text, so a consumer can tell what fidelity it holds. This dual-path design is not research-backed; it is an engineering hedge, and the reference implementation ships it because installing Docling was not viable on the target host. If parsing fidelity proves inadequate on scanned or complex-layout PDFs, the next escalation is MinerU (which leads OmniDocBench among pipeline tools per `PE T2`), mapped back into this locator-map contract.

### 8.4 Outputs per source

`manifest.json`, `normalized.txt`, `locator_map.jsonl`, optional `assets/`. Manifest fields unchanged from v2 §7.4 (including `source_family_id`, `independence_group`, `lineage_role`, `quality_tier`).

**`source_id` is `src-<slug>-<first 8 of the file's sha256>`.** The readable slug alone is not unique — `notes.md` and `notes.txt` both slugify to `notes`, and discovery is recursive, so `q1/report.md` and `q2/report.md` do too. That collision was silent and total: the two documents shared one `normalized.txt`, one `unit_id` namespace, and one registry entry, so the first was overwritten before Pass 1 read it while `kip validate` still reported a clean run. The digest is content-derived rather than positional so the same file keeps the same id however the directory changes. Two sources that still land on one id are the same bytes under the same name, and Pass 0 refuses them rather than merging.

### 8.5 `normalized.txt` rules

Unchanged from v2 §7.5: UTF-8, stable `\n`; preserve reading order, headings, lists, tables, speaker labels, structural boundaries; deterministic structural markers (`[[PAGE 12]]`, `[[SLIDE 4]]`, `[[SHEET Budget]]`); no paraphrase, summary, inference, or removal of inconvenient content; deterministic-and-logged header/footer stripping only; OCR as fallback with recorded confidence; full email envelope; slide order and title/body/notes distinction; sheet/range references with formulas and displayed values separate.

### 8.6 `locator_map.jsonl`

Unchanged from v2 §7.6. Each record maps a normalized span to the source with `normalized_line_start/end`, `normalized_char_start/end`, `original_locator_start/end`, `text_sha256`, `extraction_confidence`.

Line numbers serve humans; character offsets and hashes serve machines. Keep both. (v2 §7.6)

**This structure is load-bearing for Pass 5:** deterministic citation verification (§13.4) requires exact char offsets and hashes, not line numbers alone. (`R3 F6`)

### 8.7 Acceptance checks

Unchanged from v2 §7.7: unsupported or empty sources are **quarantined with a reason, never silently skipped**, because a skip corrupts every coverage metric downstream.

**Garbage that survives decoding is quarantined too.** Decoding with `errors="replace"` turned an arbitrary binary with a text extension into a page of replacement characters, registered `success` with no warning and sent to the expensive extractor. A NUL byte in the raw bytes, or replacement characters above a small share of the decoded text, is treated exactly like an unsupported format.

---

## 9. Pass 1 — molecular knowledge extraction

### 9.1 Objective

Extract all durable, source-backed knowledge units without imposing a fixed count. (v2 §8.1)

### 9.2 Granularity — the central v3 change

v2 §8.3 instructed maximal atomicity: "split a proposed unit when any of these differ independently." **Research contradicts this as an end in itself.**

- "Fully atomic facts are not the right representation" — atomic facts are easier to verify individually but lose the context needed to interpret them correctly. (`R1 A3`, Gunjal & Durrett, EMNLP Findings 2024)
- Naive decompose-decontextualize-verify pipelines "fail to capture essential context and miss key relational facts." (`R1 A2`, VeriFact, EMNLP 2025)
- **Decomposition helps weak verifiers and hurts strong ones.** On FELM a weak verifier improved F1 48.10 → 67.51–68.12; but Minicheck on WICE scored **72.32 without decomposition vs 59.90–68.22 with every decomposition method tested**. GPT-4o-mini degraded 71.56 → 54.34–69.39. (`R1 A4`, Decomposition Dilemmas, NAACL 2025)
- Claimify (Microsoft, ACL 2025) **deliberately excludes atomicity** from its evaluation framework: it "lacks a clear endpoint" and prior work shows it does not consistently improve fact-checking. (`R1 A5`)

**Since this pipeline uses strong frontier models in Passes 3–5, aggressive Pass 1 atomization is expected to cost downstream accuracy, not gain it.** (`R1 A4`)

**The v3 rule.** A unit is **molecular**:
- **Decontextuality** — it can be interpreted correctly standing alone, without its neighbors or its source's surrounding prose.
- **Minimality** — it adds the *least* information required to achieve decontextuality, and no more.

(Both criteria from `R1 A3`. The operational three-part rubric — distinct meaning, minimality, self-containment — is also citable from Dense X Retrieval, `R1 A1`.)

**Split only when the parts are independently evaluable AND each part remains interpretable alone.** The v2 §8.3 split triggers (truth value, actor, population, intervention, outcome, time horizon, modality, confidence, scope, exception) are retained as *split candidates* — but a split that produces an uninterpretable fragment must be rejected, and the fragment merged back.

**Granularity is a configuration parameter, not a constant.** Record the setting in the run manifest and calibrate against measured downstream accuracy. (`R1 A4`; 2025–2026 follow-ups — DyDecomp, DAD +6.24 macro-F1 via verifier-aligned decomposition — show the trade-off is mitigable with tuned policies, not absent by default.)

> **Do not cite Dense X Retrieval as evidence that proposition-level indexing beats passage-level.** That claim was **refuted 0-3** in verification. (`R1`, refuted-claims list)

### 9.3 Unit ontology — knowledge-type taxonomy `kt-v1`

v2 §8.2 carried a flat list of 20 labels. That list mixed four different questions — what kind of knowledge this is, why it must not be dropped, how it relates to another unit, and whether it is knowledge at all — which is why several of its labels were never separable from each other in practice. v3.1 splits those axes.

**Six types, three families.** The tuple order below **is** the priority order:

| Family (trusted tier) | Type (advisory tier) | Core question |
|---|---|---|
| **Episodic** — what happened | `case` | What occurred in this particular instance? |
| **Procedural** — what to do | `rule` | What must, may, or must not happen? |
| | `method` | How do we bring about a goal? |
| **Semantic** — what is so | `concept` | What does this term mean? |
| | `model` | How do these things relate, so we can explain or predict? |
| | `claim` | What is asserted to be true? |

The family is the **trusted** tier — the coarse judgment reliable enough for a lint rule and for a **ranking prior**. The 6-way type is **advisory**: display and lint pairing only. This is the same trust boundary §11.3 already draws for relationships, adopted here for the same measured reason.

**Neither tier is ever a filter.** The only hard filter anywhere in the system is the **temporal window**; filtering by `family` is deliberately not expressible, because a coarse label that removes documents from consideration silently converts a classification error into a retrieval miss nobody can see. The consuming plugin enforces this in code rather than in prose — `kwg.retrieval` asserts `len(HARD_FILTERS) == 1 and HARD_FILTERS[0] == "temporal_window"`, exposes `rank_prior()`, and offers no `family=` parameter to pass.

`family` is derived mechanically from `type`; it is never asked for separately.

#### How classification is asked

**Six independent booleans in one call, not one six-way choice.** The extractor answers `is_case`, `is_rule`, `is_method`, `is_concept`, `is_model`, `is_claim` — each on its own merits, all in the same schema object. Multiclass "pick one of N" labeling measured **~90% lower odds** of a correct assignment than binary present/absent judgments (OR = 0.10, 95% CI 0.03–0.35), and the binary-vs-multiclass distinction was the dominant task-level predictor of success.

**Resolution happens in code, not in the prompt.** `taxonomy.derive_type()` returns the first test in priority order whose answer is true. An *ordered cascade of six separate LLM gates* was considered and rejected: six gates at 95% each compounds to ~0.74 end to end, worse than the single multiclass call it was meant to beat. Asking all six at once keeps the binary shape without the compounding, and moves the priority order somewhere it can change without a prompt rewrite.

**Uncertainty is structural. No confidence score is asked for or stored.**

| Signal | Meaning |
|---|---|
| `gates_fired == 0` | abstain — `type` is `unclassified`. A real terminal state and a health metric, not an error. |
| `gates_fired == 1` | a clean classification |
| `gates_fired >= 2` | `multi_fire` — the unit is probably **two units**. A split candidate, not a tie to break. |

Consumers that need to abstain check `gates_fired != 1`. There is deliberately no `classification_confidence`: a verbalized confidence number is a second thing to calibrate, and its reliability depends mostly on how it was asked.

`claim` is last in priority because it is the **residual** type — it absorbs whatever the other five reject. That is deliberate and it must be monitored; §9.3's alarm is the unflagged-`claim` share (see `validate.py`, threshold 40%).

#### Secondary vocabulary

- **`modality`** — `required` / `permitted` / `prohibited`, nullable. Populated on any deontic modal. It replaces three legacy labels (`obligation`, `prohibition`, `deadline`), so it is a net *reduction*.
- **`flags`** — multi-select, from exactly two values. `negative_result`: the finding is an absence, a null, or a no-effect result. This is the one flag that survived review unanimously, because "X does not work" retrieves almost identically to "X works", so an unmarked null result is invisible to search and gets summarized out of existence. `caveat`: one merged marker absorbing limitation, exception, and scope restriction.
- **`quantitative`** — **computed by code, never asked.** The distinction is *force*, not presence: "the trial ran in 2026" has a number and is not quantitative; "recall improved 8.2%" is. Stated honestly: this is a **heuristic with a measurable error rate**, not an oracle. Its known misfires are false *positives* — a step range (`steps 1-3`), a section reference, a phone number, a clock time — because the strip list is keyed on singular and symbol forms that real prose often does not use. Those cases are recorded as `xfail` in `tests/test_taxonomy.py` so a future fix flips them deliberately. A wrong answer costs a wrong retrieval hint, which is why paying a model for it is still not worth it; the field is a search aid and **nothing in the pipeline gates on it**, which a test also enforces.
- **`node_kind`** — `unit` or `question`. A question has no truth value to check, no procedure to run, and no instance that occurred. Putting it inside the type system would pollute retrieval, because "what do we know about X?" would start returning "we don't know." Lint owns questions; retrieval ignores them unless asked.
- **`entity_mentions`** — named things exactly as they appear, with line numbers. **Never canonicalized here.** The wiki owns entity resolution and needs the raw surfaces to do it.

#### `unit_type` — the retained control field

The full v2 list is **still asked for and still written to every record**:

`fact`, `claim`, `definition`, `quantitative_result`, `null_result`, `study_design`, `method`, `decision`, `obligation`, `prohibition`, `exception`, `deadline`, `dependency`, `risk`, `limitation`, `contradiction`, `recommendation`, `open_question`, `observation`, `metadata`.

This is a **dual-write**, not a deprecation. `unit_type` is the control arm of the taxonomy evaluation; deleting it would destroy the comparison the change exists to make. It is not used as a gate anywhere downstream.

#### Migrating an existing run

`kip migrate-taxonomy <run-id>` backfills the new fields onto units written before the taxonomy existed. It is idempotent, and it preserves `content_sha256` (see below).

**15 of the 20 legacy labels map deterministically. 5 require review.** Anyone quoting a higher number is counting the unmapped ones. The five, and why the label alone cannot decide them:

| Legacy label | Why it is undecidable from the label |
|---|---|
| `dependency` | a relationship, not a type; the typed edge is deferred |
| `contradiction` | a relationship, not a type; carried by claim assessments |
| `recommendation` | `method` vs `rule` turns on a modality the label does not record |
| `observation` | `case` vs `claim` turns on whether it is bound to one instance |
| `metadata` | not knowledge; the unit should be dropped |

These are set to `type: unclassified` with a `migration_note`, never guessed. Migrated units are stamped `taxonomy_version: "kt-v1-migrated"` so an evaluation can tell a label reconstructed from a coarser one apart from a label a model produced against the type tests.

`migrate-taxonomy` is also the **upgrade path for the hash change**. A run sealed by schema 3.0.0 hashed `unit_type` into `content_sha256`, so `kip validate` reports a content-hash mismatch on every unit until the run is migrated; the migration re-seals under the 3.1.0 rule and validation passes again.

**Two refusals, both required by "no stage may overwrite" below.**

- A unit already stamped `kt-v1` is **left untouched and counted**. Its six independent answers came from a model; the legacy label is one coarse guess, and rebuilding the first from the second is a downgrade that no later check can detect, because every field involved is excluded from the content hash by design. `--reclassify` performs it anyway, and exists so the choice is explicit rather than accidental. (`kt-v1-migrated` is deliberately not protected — re-running the migration over its own output is the idempotence property.)
- A unit whose stored digest matches **neither** the 3.1.0 rule **nor** the 3.0.0 rule had its assertion edited after it was sealed, and the migration refuses it. Re-sealing unconditionally laundered such an edit: `kip validate` failed before the migration and passed after it, because the pass overwrote the only evidence of the change.

#### Classification is a derivation, not a fact

A unit's classification is a pure function of `(canonical_statement, prompt_version, classifier_model)`. Two consequences are binding:

1. **No derived label enters `content_sha256`.** Content identity is the *assertion* — statement, evidence, source lineage — never its labels. Before schema 3.1.0, `seal()` hashed `unit_type` along with everything else, which meant re-deriving a classification forged a new content hash and §22's integrity check rejected the corpus. The exclusion set is `artifacts.DERIVED_FIELDS`, and `validate.py` re-seals through the same function rather than a copy of the rule. **Hashes written under schema 3.0.0 are not comparable with 3.1.0 hashes.**

    Stated so the exclusion list is not over-read: `content_sha256` is a **within-run record digest, not a cross-run content identity.** The envelope — `run_id`, `prompt_version`, `model_role`, `parent_artifacts` — is inside the payload, so the same sentence extracted from the same file by two runs hashes differently. Nothing in this pipeline dedups across runs; `created_at` is excluded because it moves on every recompute of the *same* run, which would make the digest useless for detecting tampering.
2. **Any stage may re-derive; no stage may overwrite.** A differing triple appends a new classification record with its own stamp.

#### What was cut, and why

The taxonomy proposal was larger than this. These parts were reviewed and removed on purpose; re-adding one needs new evidence, not a preference.

| Cut | Why |
|---|---|
| Ordered cascade of six LLM gates | compounds multiplicatively — ~0.74 end to end at 95% per gate, worse than the single call it replaced |
| Status lifecycle enum | duplicates the bi-temporal fields in §11.6, which already carry validity |
| Two confidence scores | nothing to calibrate them against; `gates_fired` carries the same information structurally |
| 10 fine-grained edge labels | the 15-label flat relationship vocabulary tested at 0.401 accuracy (§11.3); no reason to expect better here |
| `risk` flag | maximally interpretive — the label abstractness that predicts classification failure |
| `disputed` flag | unknowable at ingestion; the disputing unit may not be ingested yet. Computed downstream instead |
| `deadline` flag | shadows the temporal fields |
| `limitation` / `exception` flags | merged into `caveat`; three flags for one concept fired on nearly every careful sentence, which flags nothing |
| `decision` flag | that is the `case` type |
| `quantitative` as an LLM question | computed by regex |
| Open sub-types, page-kind enums, review queues | no query was named that they unblock |

A new type, flag, or edge is admitted only by naming the query it unblocks and showing measured gain.

### 9.4 Length guidance

Unchanged from v2 §8.4 — no arbitrary sentence count, no strict character cap. Canonical statement normally one sentence; soft target 20–80 words; hard warning ~160 words; context note under 120 words; evidence one to three excerpts under 200 words total. A long evidence span triggers a split test or raw-source escalation, not automatic invalidation.

> The reference implementation's Pass 1 prompt contradicted v2 here with a "target 450 characters" instruction. v3 prompts must not reintroduce a character cap.

### 9.5 Scoring and quality evaluation

**Retained from v2 §8.5** — anchored 0–3 scores for `specificity`, `retrieval_value`, `connection_value`, `evidence_strength`, `novelty`, with the explicit v2 rule that the decision is not a simple sum and that mandatory obligations, contradictions, critical limitations, and rare exceptions may be retained despite low scores.

**Added — extraction-quality evaluation** (distinct from per-unit scoring; used to evaluate the *extractor*, not to gate individual units). Adopt Claimify's human-validated three-factor rubric (6,490 sentences, 3 annotators, Krippendorff's α = 0.72; 0.86 high-confidence):

| Factor | Question |
|---|---|
| **Entailment** | Is the unit entailed by its cited source span? |
| **Coverage** (element-level) | Does the unit set omit verifiable content, *or* include unverifiable content? Both are penalized. |
| **Decontextualization** | Does the unit stand alone correctly? |

**Atomicity is deliberately not a scored factor.** (`R1 A5`)

> Caveat carried from research: this rubric maps onto v2's §8.7 omission check and loosely onto `evidence_strength ≈ entailment`. It is **not** a dimension-for-dimension match with the v2 §8.5 scoring rubric and must not be cited as validating v2's atomicity rules. (`R1 A5`, mapping caveat)

### 9.6 Omission check — retained and strengthened

v2 §8.7's separate completeness pass is **confirmed by evidence**:

- VeriFact's detect-and-refine step cut incomplete facts to **22.5% vs 56.7%** for the best baseline, and raised coverage of human reference facts to **87.1% vs 77.5%**. Notably, **24.9% of refined facts flipped correctness label** once incompleteness was resolved. (`R1 B1`)
- A simple **end-to-end LLM missing-content pass beat both NLI-atomic-decomposition and Q&A-pair extraction**: 88% fully correct in human eval vs 66% (Q&A) and 48% (NLI). (`R1 B2`, Dejl et al., ACL 2026 Findings)

**Design rule:** use the simple end-to-end LLM omission pass — it does not require atomic-decomposition machinery. **But** it must emit **structured per-omission findings** to `02_units/omissions.jsonl`, because the measured cost of the E2E form is "reduced robustness, interpretability and result granularity" (cross-evaluator std-dev 0.044 vs 0.009 for Q&A). Structured output recovers the interpretability. (`R1 B2`)

Omission questions unchanged from v2 §8.7: which decisions, exceptions, limitations, negative results, dependencies, and numerical findings are unrepresented; which retained unit bundles independently-true-or-false claims; which unit cannot be understood without hidden context.

The omission check may add, split, merge, or downgrade units, but must reference the same normalized text. (v2 §8.7)

> Scope caveat: VeriFact's domain is factuality evaluation of LLM long-form output, not document ingestion — mechanism-level evidence, not same-domain proof. (`R1 B1`)

### 9.7 Unit schema

As v2 §8.6, plus `granularity_policy` / `decontextualization_note` (v3.0) and the `kt-v1` classification block (v3.1):

```json
{
  "unit_id": "u-...",
  "source_id": "src-...",
  "source_family_id": "family-...",
  "independence_group": "study-...",

  "unit_type": "quantitative_result",

  "type_tests": { "is_case": true, "is_rule": false, "is_method": false,
                  "is_concept": false, "is_model": false, "is_claim": true },
  "type": "case",
  "family": "episodic",
  "gates_fired": 2,
  "multi_fire": true,
  "modality": null,
  "suppressed_modality": null,
  "flags": [],
  "quantitative": true,
  "node_kind": "unit",
  "entity_mentions": [ { "surface": "extension group", "line": 12 } ],
  "taxonomy_version": "kt-v1",
  "classifier_model": "<resolved from config>",
  "migration_note": null,

  "canonical_statement": "One decontextualized, minimal statement.",
  "context_note": "Optional interpretive context, not new evidence.",
  "qualifiers": ["exploratory", "not preregistered"],
  "candidate_topics": ["sleep extension", "memory"],
  "evidence": [ { "source_id": "...", "normalized_path": "...",
                  "normalized_line_start": 12, "normalized_line_end": 14,
                  "normalized_char_start": 2301, "normalized_char_end": 2710,
                  "original_locator_start": {"page": 2},
                  "excerpt": "...", "excerpt_sha256": "..." } ],
  "scores": { "specificity": 3, "retrieval_value": 3, "connection_value": 2,
              "evidence_strength": 3, "novelty": 2 },
  "decision": "keep | drop | review",
  "drop_reason": null,
  "extraction_confidence": 0.96,
  "granularity_policy": "molecular-v1",
  "decontextualization_note": "What was added to make this stand alone.",
  "parent_artifacts": [".../normalized.txt"],
  "content_sha256": "..."
}
```

`granularity_policy` and `decontextualization_note` are added per `R1 A3`/`R1 A4` — the first to make granularity tunable and auditable, the second to make the minimality/decontextuality tradeoff inspectable.

**Only `unit_type`, `type_tests`, `modality`, `flags`, `node_kind`, and `entity_mentions` come from the model.** `type`, `family`, `gates_fired`, `multi_fire`, `suppressed_modality`, and `quantitative` are computed from those answers and the statement text. The whole block is excluded from `content_sha256` (§9.3, "classification is a derivation").

**`modality` is scoped to units that resolved to `rule`; `suppressed_modality` holds the rest.** The model is still asked for a modal independently of `is_rule`, and the validator still treats a modality on a non-`rule` type as a fatal error — those two rules collide on a real shape, because a dated decision that states an obligation fires `is_case` and `is_rule` together and `case` wins on priority. Writing the reported modal into `suppressed_modality` keeps the answer (a `multi_fire` unit needs it to split later) while leaving the validated field meaning exactly what the validator checks.

The example above shows a real `multi_fire` case: a measurement on one sample is a `case`, and the generalization it supports is a `claim`. Two gates firing means the source sentence should probably have been split into two units, and the flag is what surfaces that to lint.

**Note the char-offset requirement in `evidence`.** v2 §8.6 showed only line numbers in the unit example while requiring char offsets in §7.6. v3 requires char offsets and `excerpt_sha256` on every evidence record, because Pass 5's deterministic citation check depends on them. (`R3 F6`)

---

## 10. Pass 2 — contextual enrichment, routing, and clustering

### 10.1 Objective

Group likely related units into coherent comparison sets **without deciding whether they agree**. (v2 §9.1)

### 10.2 Contextual enrichment — new in v3

**Before indexing, prepend LLM-generated context to each unit.** This is the one concrete evidence-backed technique v2 lacked entirely (v2 §9.2 routes on raw embeddings + BM25).

Anthropic's Contextual Retrieval cut top-20 retrieval failure rate by **49% (5.7% → 2.9%)** across codebases, fiction, ArXiv, and science content by prepending generated chunk context before both embedding and BM25 indexing. Independent replication (Merola & Singh, ECIR 2025) confirms direction; AWS replications report smaller **5–15%** precision gains. (`R1 C2`)

Write enriched units to `03_clusters/enriched_units.jsonl`. **The enrichment is an index-time artifact only** — it must never replace the unit's `canonical_statement` or leak into evidence.

> Vendor-benchmark caveat: the 49% figure is Anthropic's own measurement; independent replications are smaller but directionally consistent. (`R1 C2`)

### 10.3 Routing signals

Hybrid retrieval, as v2 §9.2: embeddings, lexical/BM25, entities, candidate topics, unit type, population/intervention/outcome tuples, dates, source lineage, existing wiki-topic index.

**Confirmed:** embeddings alone miss exact-match strings (identifiers like `TS-999`) that BM25 catches. Corroborated academically by T2-RAGBench (23,088 queries — BM25+dense RRF beats both constituents, +8.1pp Recall@5), Wang et al. 2024, and BEIR. (`R1 C1`)

**Qualification that must be honored:** fusion weighting is **tunable, not fixed**. TIFIN India @ SemEval-2025 found BM25 fusion helped small embedders but **reduced** effectiveness with a top-tier embedder on one task. (`R1 C1`)

### 10.4 Clustering rules

As v2 §9.3, all retained:
- A unit may belong to multiple clusters when it genuinely affects multiple topics.
- Preserve singleton clusters; unrelated content is not a failure.
- Do not merge clusters merely for shared broad vocabulary.
- Do not classify evidence relationships in this pass.
- Prefer coherent clusters of ~20–50 units; split above ~75.
- Large context windows are headroom, not a target.

**Flat clustering over graph construction is confirmed:**
- LazyGraphRAG shows eager LLM graph construction is unnecessary — indexing cost ~0.1% of full GraphRAG with zero index-time LLM use, at comparable answer quality on global queries. Microsoft reports 96/96 LLM-judged wins in BenchmarkQED follow-up. (`R1 C3`)
- Dense RAG "remains a practical and competitive alternative for general QA scenarios." GraphRAG's average gain over dense RAG is **+0.47 on general QA vs +27.23 on multi-hop QA**. (`R1 C4`, RAGSearch 2026; Han et al. 2025)

**Escape clause:** if the workload becomes dominated by cross-document multi-hop synthesis or global sensemaking, prefer the **LazyGraphRAG deferred pattern** over eager graph construction. (`R1 C4`)

> Cite LazyGraphRAG as "Microsoft reports" — vendor-internal, LLM-judged win-rates, no independent replication, code unreleased as of Jul 2026. The stronger claim ("~4% of query cost significantly outperforms all competing methods") was **refuted 0-3**. (`R1 C3`)

### 10.5 Cluster schema

Unchanged from v2 §9.4.

---

## 11. Pass 3 — claim relationship and evidence synthesis

### 11.1 Objective

Within each cluster, identify canonical claims, classify relationships, assess evidence strength, and preserve disagreement. (v2 §10.1)

### 11.2 Two-stage comparison — strongly validated

v2 §10.2's design (candidate matching, then relationship judgment) is **confirmed by the strongest single evidence chain in this research**:

- **Unguided** whole-document contradiction detection is near-chance: ~50–54% accuracy across four LLMs; GPT-4 at 53.8% accuracy with **8.0% recall**. (`R2 F1`, ContraDoc, NAACL 2024)
- **Localized** judgment works: given the evidence sentence, GPT-4 finds the contradictory counterpart **77.2%** of the time. The gradient — random → 70.2% (told a contradiction exists) → 77.2% (given the sentence) — directly supports localize-before-judge. (`R2 F1`)
- **Not solved by newer models:** a 2026 re-evaluation on 891 documents puts GPT-4o at **0.680 accuracy / 0.697 F1**, with evidence localization 0.54–0.57. (`R2 F1`)

**Rule: never ask the model open-endedly whether a cluster contains contradictions. Always present retrieved candidate pairs.** (`R2 F1`)

### 11.3 Relationship vocabulary — coarse first, then constrained sub-typing

v2 §10.3 listed 15 labels judged in a single step. **Research contradicts this as-is.**

- Established benchmarks (SciFact / HealthVer / COVIDFact) validate only **3-way stance**: Supports / Refutes / Not-Enough-Info. (`R2 F3`)
- Fine-grained contradiction-**type** classification peaked at **0.401 accuracy** in the one study that measured it — and chain-of-thought prompting *degraded* it. (`R2 F3`)
- "Partial / conflicting" labels are the weakest class in **every** study measured: 0.50 F1 zero-shot vs 0.83 for clear False; 0.32 vs 0.73 for the best fine-tuned model at test time. (`R2 F3`)

**The v3 two-step judgment:**

**Step A — coarse stance (trusted).** Classify each candidate pair as `supports` / `contradicts` / `insufficient_evidence`. This is the tier benchmarks validate.

**Step B — constrained sub-typing (labeled lower-confidence).** Only within the coarse class, assign the finer label from v2's vocabulary: `duplicate`, `paraphrase`, `convergent_independent`, `convergent_dependent`, `partially_contradicts`, `scope_difference`, `temporal_update`, `methodological_qualification`, `complementary`, `singleton`, `singleton_hypothesis`, `authoritative_composite`, `operational_composite`.

**The 4-bucket grouping v2 §10.3 already proposed for human presentation — convergent / contested / singleton / complementary-qualifying — is promoted to the system's trust boundary.** Downstream passes and human-facing output may rely on the bucket; they must not rely on the fine label without independent confirmation. (`R2 F3`)

`[NEW — confirm]` Sub-type labels below the bucket level carry a `subtype_confidence` field and are advisory to Pass 4 rather than determinative. The two-step structure is research-mandated; representing it as an explicit advisory field is an implementation choice.

**Do not enable chain-of-thought for Step B by default** — CoT degraded type classification in the one study measuring it. Validate before adopting. (`R2 F3`)

### 11.4 Evidence requirements

**Every `contradicts`-family verdict must carry a quoted evidence span.** When GPT-4 flags a contradiction in the Judge-then-Find setting it is right **88%** of the time and locates correct evidence in **92.7%** of flagged documents — but it flags only 19.6% of truly contradictory documents. (`R2 F2`)

**Corollary the spec must honor: absence of a contradiction flag is weak evidence of consistency.** Missed contradictions, not false alarms, are the dominant failure mode. (`R2 F2`)

### 11.5 Evidence weighting

As v2 §10.4 — weigh independent evidence groups, directness, source authority, study quality, preregistration and sample size, scope match, recency only when time-sensitive, summary-of-another detection, known methodological limitations. **Do not count documents.**

**Added — source validity screening.** Automated retraction and citation-lineage screening enters evidence weighting: **32.2% of citations to paper-mill articles occur *after* retraction**, and retraction does not stop contamination propagating. (`R2 F8`, JAMA-published data)

**Added — expect conclusion instability.** When an automated systematic-review system re-aggregated evidence, **3 of 12 updated Cochrane reviews had their statistical conclusions flip**. Knowledge-state transitions between `established` and `contested` are expected behavior, not anomalies. (`R2 F9`)

> Caveat: the otto-SR source is a non-peer-reviewed preprint, self-evaluated by its creators, and its human-comparator framing structurally favors the tool. (`R2 F9`)

### 11.6 Temporal updates — bi-temporal, invalidate-don't-delete

v2 §10.3 listed `temporal_update` as a label without a mechanism. v3 adopts the **bi-temporal model** shipped by Graphiti/Zep: track *validity time* (`t_valid` / `t_invalid` — when the fact was true in the world) separately from *transaction time* (when the system learned it). When a new fact temporally overlaps and supersedes an existing one, **mark the old edge invalid rather than deleting it**. (`R2 F6`)

This preserves the spec's traceability principle (§3.10): superseded knowledge remains followable.

> Zep's benchmark performance claims are vendor-run; the architectural pattern itself is code-verifiable and is what v3 adopts. (`R2 F6`)

### 11.7 Accuracy expectations — design to absorb them

**Plan for ~70–80% relationship-classification accuracy.** Even a strong fine-tuned system (MultiVerS, Longformer-based) reaches only low-to-mid-70s abstract-level F1 under full supervision: 72.5 on SciFact, 77.6 on HealthVer, 77.3 on COVIDFact. (`R2 F4`)

**Passes 4 and 5 must be designed to absorb 20–30% upstream error.** (`R2 F4`)

**Do not fine-tune the Pass 3 judge.** Fine-tuned claim-relationship classifiers collapse out-of-distribution: 0.945 → 0.42 macro-F1 (LoRA LLaMA, CheckThat! 2025) and 0.88 → 0.44 F1 in a second case. A prompted frontier LLM is the right default. (`R2 F5`)

### 11.8 Ordering discipline

**Rotate or randomize unit ordering across passes.** Items in the middle of a batch are systematically disadvantaged — a 22 pp primacy-to-middle spread, with mid-context performance falling *below* the model's own closed-book baseline. (`R5 T2`, Lost in the Middle / TACL 2024)

### 11.9 Assessment schema

As v2 §10.5, with added fields:

```json
{
  "assessment_id": "asmt-...",
  "cluster_id": "cl-...",
  "canonical_claim": "The proposition being assessed.",
  "coarse_stance": "supports | contradicts | insufficient_evidence",
  "relationship_bucket": "convergent | contested | singleton | complementary",
  "relationship_subtype": "convergent_dependent",
  "subtype_confidence": 0.6,
  "supporting_unit_ids": ["u-001"],
  "opposing_unit_ids": ["u-017"],
  "qualifying_unit_ids": ["u-022"],
  "contradiction_evidence": [ {"unit_id": "u-017", "excerpt": "...", "excerpt_sha256": "..."} ],
  "independent_evidence_groups": ["study-a", "study-b"],
  "source_validity_flags": [],
  "t_valid": "2026-01-01T00:00:00Z",
  "t_invalid": null,
  "support_strength": 1.8,
  "importance_score": 3.0,
  "uncertainty": "high",
  "synthesis": "Balanced source-backed synthesis.",
  "recommended_action": "Create a contested-evidence leaf.",
  "raw_source_escalations": [],
  "parent_artifacts": ["03_clusters/clusters.jsonl", "02_units/units.jsonl"],
  "content_sha256": "..."
}
```

New fields: `coarse_stance` / `relationship_bucket` / `relationship_subtype` / `subtype_confidence` (`R2 F3`), `contradiction_evidence` (`R2 F2`), `source_validity_flags` (`R2 F8`), `t_valid` / `t_invalid` (`R2 F6`).

---

## 12. Pass 4 — candidate leaf generation

Unchanged from v2 §11 in structure. Operations: `create`, `update`, `create_or_update`, `merge`, `split`, `link`, `no_op`, `defer`. Knowledge states: `established`, `supported`, `contested`, `preliminary`, `internal-observation`, `operational`, `authoritative`.

Rules retained from v2 §11.3: state the knowledge state explicitly; each assertion lists assessment IDs; avoid narrow leaves where the ontology favors incorporation; preserve negative and null findings; **do not convert a dependent convergence into independent support**; flag every candidate for audit.

**Amendments:**
- Candidates consume `relationship_bucket` as authoritative and `relationship_subtype` as advisory. (§11.3, `R2 F3`)
- Knowledge-state transitions (`established` ↔ `contested`) are expected on re-ingestion and must be representable as updates, not treated as errors. (`R2 F9`)
- Pass 4 must remain correct when ~20–30% of upstream relationship labels are wrong. (`R2 F4`)

Candidate schema unchanged from v2 §11.4.

---

## 13. Pass 5 — adversarial audit

### 13.1 Objective

Challenge the candidate against assessments, units, normalized sources, and source lineage before queueing. (v2 §12.1)

### 13.2 Why this pass exists — and why it must be external

**Validated:** external grounding is the only regime where LLM self-correction reliably works. Intrinsic self-critique **degrades** accuracy (`R3 F5`, Huang et al. ICLR 2024; Kamoi et al. TACL 2024). Chain-of-Verification — fresh-context, atomic, per-claim verification — is the shape that works: **~70% vs ~17% accuracy on the same facts**. (`R3 F7`)

The v2 §12 design was right. v3 adds the *conditions* under which it actually delivers.

### 13.3 Auditor requirements — new in v3

v2 left the auditor's identity and model class unspecified. Three requirements are now mandatory:

**(a) Reasoning-class model required.** On objectively-labeled hard correctness pairs, non-reasoning judges are near chance — GPT-4o **56.57%**, GPT-4o-mini 50.0%, Claude-3.5-Sonnet 64.29% — while reasoning models reach **75–81%** (o1-preview 75.43%, o3-mini-high 80.86%). Note also that preference agreement does **not** validate correctness auditing: judges scoring >80% human-preference agreement sit near chance on objective correctness. (`R3 F1`, JudgeBench, ICLR 2025)

**(b) Different model, or at minimum fresh context.** Self-preference bias survives anonymization and is causally tied to self-recognition. Anonymizing the proposer's output is *insufficient*. (`R3 F4`)

**(c) Both-orders aggregation for any pairwise judgment.** 17–22% of pairwise verdicts flip on order swap even for the best judges (robustness rates: Claude-3.5 0.832, GPT-4-Turbo 0.818, GPT-4o 0.776). Order manipulation alone made a weaker model beat a stronger one on 66/80 queries. The bias is systematic, not random, and worst for near-ties. (`R3 F3`)

Twelve distinct judge-bias types are taxonomized and quantified (position, verbosity, compassion-fade, bandwagon, distraction, fallacy-oversight, authority, sentiment, diversity, chain-of-thought, self-enhancement, refinement-aware); the literature's explicit conclusion is that LLM-as-judge is **not yet reliable enough for uncritical use**. (`R3 F2`)

### 13.4 Check execution modes — mechanical wherever possible

Because even the best auditors carry **~19% pairwise error on hard cases** (`R3 F1`), every check that *can* be deterministic must be:

| # | Check (v2 §12.2) | v3 execution mode | Evidence |
|---|---|---|---|
| 1 | **Grounding** — every factual clause has supporting units | **Specialized NLI checker**, not frontier LLM | `R4 F1`, `R4 F2` |
| 2 | Coverage — material results, limitations, exceptions represented | LLM (reasoning-class) | v2 §12.2 |
| 3 | Contradiction handling — disagreement not hidden | LLM (reasoning-class) | v2 §12.2 |
| 4 | Scope fidelity — population, time, jurisdiction, modality preserved | LLM (reasoning-class) | v2 §12.2 |
| 5 | Source independence — derivatives not counted as replication | LLM + lineage metadata | v2 §12.2 |
| 6 | **Provenance integrity** — every ID/path resolves | **Deterministic code** | `R3 F6` |
| 7 | Duplication / ontology fit | LLM (reasoning-class) | v2 §12.2 |
| 8 | **Abstraction drift** — candidate says no more than evidence | NLI **citation recall** as mechanism | `R4` |
| 9 | **Citation accuracy** — quoted excerpts and ranges match | **Deterministic string / char-offset / hash matching** | `R3 F6` |
| 10 | **Raw-source escalation** for uncertain or high-impact claims | Required, not optional | `R4` |

**On check 1 (grounding).** Use a MiniCheck-class specialized checker rather than a frontier LLM-as-judge. MiniCheck-FT5 (770M) "reaches GPT-4 accuracy" at **~400× lower cost** ($0.24 vs $107 to check a 13K test set). On the LLM-AggreFact leaderboard: Bespoke-MiniCheck-7B 77.4 > Claude-3.5-Sonnet 77.2 > GPT-4o 75.9; even sub-1B checkers (FactCG-DeBERTa-L 0.4B at 75.6) beat Llama-3.1-405B (74.4). Throughput **>500 checks/min on one A6000**. (`R4 F1`, `R4 F2`)

> **License check:** Bespoke-MiniCheck-7B is CC BY-NC 4.0 (non-commercial). Use MiniCheck-Flan-T5 variants for commercial deployment. (`R4 F2`)
>
> **Scope caveats:** "GPT-4" here is the 2024-era model; the leaderboard appears frozen ~late-2024/early-2025 and excludes 2025–2026 frontier models. Margins over the largest models are ~0.6–1.5 points (near noise). The 400× multiplier is pinned to April-2024 GPT-4 pricing. (`R4 F1`)
>
> **Do not** substitute AlignScore for this role — the claim that AlignScore (355M) matches or outperforms GPT-4 was **refuted 0-3**. AlignScore is a superseded historical SOTA (70.4% on LLM-AggreFact vs MiniCheck-FT5's 74.7%). (`R4 F3`)

**On check 9 (citation accuracy).** Deterministic matching of `excerpt` against `normalized_char_start`/`end` and `excerpt_sha256` is exact and free — this is why §8.6 and §9.7 mandate char offsets and hashes. Where semantic (rather than literal) citation verification is needed, NLI-based entailment is the established method (ALCE), **but every automated attribution checker measured — NLI metrics, fine-tuned GPT-3.5, zero-shot GPT-4 — tops out at ~80–85% agreement with humans.** About 1 in 5 individual citation judgments is wrong. **Do not hard-gate on a single checker verdict.** (`R4`)

**On check 8 (abstraction drift).** Use NLI citation *recall* as the mechanism — a statement not entailed by its source implies overclaim. There is **no verified high-accuracy standalone abstraction-drift detector**; budget for error and escalate. (`R4`)

**On check 10 (raw-source escalation).** The ~20% attribution-check error rate is precisely why escalation for uncertain or high-impact claims is **required, not optional**. (`R4`)

### 13.5 Verdicts

Unchanged from v2 §12.3: `pass`, `pass_with_label`, `fix`, `merge`, `split`, `reject`, `defer`. A `fix`, `merge`, or `split` produces a **new candidate version**; it never overwrites the initial proposal. (v2 §12.3 — this versioning discipline is what makes the audit auditable.)

### 13.6 Confidence reporting

**`auditor_confidence` must not be treated as calibrated.** v2 §12.4's example showed `0.99`. Judge calibration is unverified in this research, and even the best reasoning judges carry ~19% pairwise error on hard cases. Report it, log it, do not gate on it. (`R3 F1`)

### 13.7 Audit schema

As v2 §12.4, with `checks` extended to record **execution mode** per check (`deterministic` / `nli_checker` / `llm_reasoning`) and the auditor's model identity, so that any audit record can be re-evaluated against the conditions in §13.3.

```json
{
  "audit_id": "audit-...",
  "candidate_id": "cand-...",
  "verdict": "fix",
  "auditor_model": "reasoning-class model id",
  "auditor_distinct_from_proposer": true,
  "order_swap_applied": true,
  "checks": {
    "grounding": {"result": "pass", "mode": "nli_checker", "checker": "minicheck-flan-t5-l"},
    "coverage": {"result": "pass", "mode": "llm_reasoning"},
    "contradiction_handling": {"result": "fail", "mode": "llm_reasoning"},
    "scope_fidelity": {"result": "fail", "mode": "llm_reasoning"},
    "source_independence": {"result": "pass", "mode": "llm_reasoning"},
    "provenance_integrity": {"result": "pass", "mode": "deterministic"},
    "citation_accuracy": {"result": "pass", "mode": "deterministic"},
    "abstraction_drift": {"result": "warn", "mode": "nli_checker"},
    "duplication": {"result": "warn", "mode": "llm_reasoning"}
  },
  "findings": ["The title presents contested evidence as established."],
  "required_fixes": ["Use a mixed-evidence title and state."],
  "raw_source_escalation": ["src-001", "src-002"],
  "auditor_confidence": 0.7,
  "parent_artifacts": ["05_candidates/candidates.initial.jsonl", "04_assessments/claim_assessments.jsonl", "02_units/units.jsonl"],
  "content_sha256": "..."
}
```

---

## 14. Step 6 — queue handoff

Unchanged from v2 §13 in contract. Queue event schema as v2 §13.2 with `queue_event_id`, `idempotency_key`, `target_engine`, `operation`, `candidate_id`, `candidate_version`, `audit_ids`, `payload`, `provenance_chain`, `status`.

**The idempotency key is derived from `(target_engine, run_id, candidate_id, candidate_version, sha256(payload))`.** `candidate_id` is a per-run counter, so a key built from it alone made every run's Nth approved candidate identical — and a consumer doing what this section instructs, deduplicating on the key, would have discarded every run after the first. The payload digest is what makes a replay idempotent; the run id is what keeps two runs' proposals distinct.

**Confirmed by engineering evidence:** the **transactional outbox** pattern is the right shape. It solves exactly the dual-write problem this handoff faces (atomically update state + publish), guarantees messages are sent iff the transaction commits and in commit order, and explicitly warns that the relay "might publish a message more than once" — therefore **consumers must be idempotent, tracking IDs of already-processed messages**. This is precisely v2's `idempotency_key` + acknowledge-by-event-ID design. (`PE T3`)

This step is deterministic code, not an LLM reasoning pass. (v2, `prompts/pass_06_enqueue_contract.md`)

---

## 15. Durable leaf materialization

Unchanged from v2 §14. Markdown with YAML front matter written **only after** the existing leaf engine accepts the queue event. Front matter carries `leaf_id`, `title`, `knowledge_state`, `accepted_queue_event_id`, `candidate_id`, `audit_ids`, `source_unit_ids`, `provenance_root`, `created_at`.

`[NEW — confirm]` Where §11.6's bi-temporal model applies, front matter should also carry `t_valid` / `t_invalid`. Adopting bi-temporality is research-backed (`R2 F6`); surfacing it in the durable leaf's front matter is an extension of that decision into the leaf engine's contract, which this spec does not own.

---

## 16. Storage, indexing, and UI

Unchanged from v2 §15. JSONL for intermediate artifacts (streaming, append-only, shardable, isolatable failures, efficient reprocessing, object-store compatible). Trace UI resolves IDs and renders the full chain; **the UI is a projection, JSONL remains the source of truth.**

---

## 17. Context-window and batching strategy

v2 §16's numbers are **validated by direct evidence** — with one addition.

**Cap on unit count, not just tokens.** The most on-point finding: "all LLMs follow a pattern of slight performance degradation for small numbers of instances (**approximately 20-100**), followed by a **performance collapse** on larger instance counts. Crucially … while context length is associated with this degradation, **the number of instances has a stronger effect**." (`R5 T2`, arXiv 2603.22608, Apr 2026)

**The 20–50 batch with a hard split above 75 sits conservatively inside the empirically safe band.** A 3,962-text batch-classification study across 8 models and 9 batch sizes found **6 of 8 models stayed within 2 pp of the single-item baseline through batch size 100** (Claude Haiku 4.5 most robust, max drop 1.1 pp); at b≥250 degradation became model-specific; at b=1000 two reasoning models lost **27–36 points** with substantial parse failures. Recommended safe range 25–100, with >80% token cost savings at b=25. (`R5 T2`, arXiv 2604.03684)

**The 30–50% context reservation is separately justified:** degradation is continuous rather than cliff-shaped and appears even on trivial copy tasks (`R5 T2`, Chroma Context Rot 2025); only half of tested models maintain satisfactory performance at 32K (`R5 T2`, RULER); and **11 of 13 models claiming ≥128K fall below 50% of their short-context baseline at 32K** once lexical shortcuts are removed — which is exactly the cross-document comparison case (`R5 T2`, NoLiMa 2025).

Retained from v2 §16: never optimize for filling the window; normalize and extract long documents section-by-section then run a document-level omission check; cluster globally then synthesize one cluster at a time; retrieve minimal evidence first and expand only for uncertainty, contradiction, or high impact; cache embeddings, normalized text, and pass outputs by hash.

**Added — ordering discipline.** Rotate or randomize item order across passes; do not trust a fixed order. (`R5 T2` — 22 pp positional spread; note also that *shuffled* haystacks outperformed logically coherent ones in Chroma's testing.)

### 17.1 Cost strategy

The **Message Batches API charges 50% of standard prices on both input and output**, holds up to 100,000 requests (or 256 MB) per batch, and most batches complete within an hour (24-hour ceiling). **Prompt-caching discounts stack with batch discounts.** For batches sharing a large system prompt, use the 1-hour cache TTL rather than the 5-minute default. Match results by `custom_id` — order is arbitrary. (`PE T4`)

Pass 1 extraction across many sources is the natural batch candidate. (`SDK`)

---

## 18. Orchestration and resumability

Unchanged from v2 §17: each pass is a durable job with input artifact IDs and hashes, output path, schema validation, completion marker, retry count, deterministic idempotency key, dead-letter status, parent-child lineage, and prompt/model version. A failed pass resumes from the last valid artifact. Do not reprocess unchanged sources unless the normalizer, prompt, schema, model policy, or source hash changes.

**"Unchanged" is checked, not assumed.** Each stage records a fingerprint of the inputs it consumed — for Pass 0 the sorted `(filename, sha256)` of every discovered source, for later passes the content digests of the upstream records. Resuming a run whose fingerprint has moved is refused with the changed stage named, because the alternative is a corpus that is half old and half new with no marker anywhere saying so: the added document is never ingested, never quarantined, and absent from every coverage count, while the registry's `original_sha256` still describes content that no longer exists. `--force` recomputes; a new run id keeps both.

**Pass 1 checkpoints per document.** It is the expensive pass and it accumulates across sources, so a failure on the last document used to discard the paid extraction for all of them. Units and omissions are written to `units.partial.jsonl` / `omissions.partial.jsonl` after each source and removed on success. A malformed unit inside an otherwise good answer is skipped and recorded in `02_units/rejects.jsonl` rather than raised — the same rule `_read_type_tests` already applied to a missing classification, extended to the rest of the record.

**Confirmed by engineering practice:** durable-execution engines implement exactly this contract — recording each step as events and replaying history to restore state after a crash, with completed steps not re-executed. Because execution is at-least-once, **individual activities must be idempotent** (idempotency keys plus destination-side deduplication). (`PE T3`)

**On multi-agent decomposition:** Anthropic reports a multi-agent research system outperforming single-agent by **90.2%** on an internal breadth-first eval — but at **~15× the token cost**, with token usage alone explaining 80% of performance variance. The stated rule: multi-agent pays off for heavy parallelization, information exceeding one context window, and many complex tools; it does **not** pay off when agents must share context or have many inter-dependencies. (`PE T1`)

This pipeline's passes are **sequential and dependency-heavy** (each consumes the prior artifact), so the staged single-pass design is the right shape; parallelism belongs *within* a pass (many sources, many clusters), which is also where the Batch API applies. (`PE T1`, `PE T4`)

---

## 19. Model prompting and structured output

### 19.1 Prompt contract

Each model pass specifies, as v2 §18: role, objective, allowed input fields, explicit ontology, decision rules, output JSON schema, prohibition on invented evidence, source/provenance requirements, uncertainty behavior, and self-check or omission check. **Treat prompts as versioned code.** Validate output structurally before accepting and semantically before advancing. (v2 §18)

### 19.2 Structured output is safe here — and the 2024 alarm did not survive

v2 §18 mandated schema-constrained JSON on every pass without addressing the 2024 claim that format restriction degrades reasoning. The evidence now resolves it:

- The 2024 alarm ("Let Me Speak Freely?") reported large reasoning drops under JSON mode (GPT-3.5 GSM8K 76.6% → 49.3%; Claude-3-Haiku 86.5% → 23.4%). (`R5 T1`)
- **But its own classification results moved the other way** — DDXPlus: Gemini 41.6% → 60.3%, Claude-3-Haiku 33.8% → 52.0%, GPT-3.5 44.1% → 55.5%. (`R5 T1`)
- The dottxt rebuttal identified five methodological flaws — different prompts between arms, a JSON-mode prompt that omitted the task description, and lossy parsing (parser choice alone moved one score 0.35 → 0.61). Matched-prompt replication put **JSON structured (0.77) above JSON unstructured (0.73)**. (`R5 T1`)
- 2026 arbitration ("The Format Tax") decomposed the cost: the format-*requesting prompt* costs **−3.9 pp**, while adding grammar-constrained decoding costs only **−1.6 pp more** — 92% of significant effects were prompt-level. **Recent closed-weight models showed near-zero or positive deltas.** (`R5 T1`)

**Conclusion: for classification and extraction — this pipeline's entire workload — schema constraint is neutral-to-positive.** Keep it. (`R5 T1`)

The alternative is worse: **unconstrained naive prompting produced 0% JSON validity** across all models and datasets in one 2026 study, despite 77–85% task accuracy. (`R5 T1`)

### 19.3 Structured-output design rules

1. **Put a reasoning/thinking field before answer fields.** Measured recovery: 43/72 comparisons, avg **+9.2 pp** — but **11 (15%) worsened**, so measure per pass rather than assuming. (`R5 T1`)
2. **Prefer loose schemas to prescriptive ones.** (`R5 T1`, both the original paper's own mitigation and the 2026 arbitration.)
3. **Treat field names as prompt text.** "Changing only schema-key wording can substantially affect accuracy"; schema-level and prompt-level channels interact non-additively. (`R5 T1`)
4. **Guard against near-miss fabricated enum values.** Constrained-only decoding fabricated near-miss entities in **9%** of samples in closed information extraction. Validate enum outputs against the source ontology rather than trusting the grammar. (`R5 T1`)
5. **Consider two-turn (freeform → reformat) for the hardest reasoning passes.** Recovered accuracy in 42/72 comparisons, avg +6.8 pp, with only 2 regressions — the safer of the two mitigations. (`R5 T1`)

`[NEW — confirm]` Rule 5 is offered as available-when-needed rather than default-on: it doubles call count for the affected pass. The research supports its effectiveness; making it opt-in is a cost judgment.

### 19.4 Model role assignments

| Pass | Role | Model class | Rationale |
|---|---|---|---|
| 0 | Normalizer | none (code) | v2 §7.1 |
| 1 | Extractor | mid-tier frontier, batched | `SDK`; `PE T4` (50% batch discount) |
| 1b | Omission checker | mid-tier frontier | `R1 B2` (E2E form wins) |
| 2 | Contextual enricher | small/cheap frontier | `R1 C2` (per-unit, high volume) |
| 3a | Candidate matcher | none (retrieval code) | `R2 F1` |
| 3b | Relationship judge | frontier, prompted not fine-tuned | `R2 F5` |
| 4 | Candidate planner | frontier | v2 §11 |
| 5a | Grounding checker | specialized NLI (MiniCheck-class) | `R4 F1` |
| 5b | Deterministic checks | none (code) | `R3 F6` |
| 5c | Adversarial auditor | **reasoning-class, different model** | `R3 F1`, `R3 F4` |
| 6 | Enqueue | none (code) | v2 §13 |

`[NEW — confirm]` The specific tier assignments (which pass gets which model size) are engineering judgment informed by `SDK` cost data, not research findings. Only 5a (specialized checker), 5c (reasoning-class, distinct), and 3b (prompted, not fine-tuned) are research-mandated.

---

## 20. Security and trust boundaries

### 20.1 Retained requirements

As v2 §20: treat source text as untrusted **data, not instructions**; strip or quarantine executable content and macros; defend against prompt injection inside documents; enforce file-size, decompression, recursion, and attachment limits; scan uploads and preserve tenant boundaries; redact or classify sensitive data before external model calls; log which text left the trust boundary and which provider processed it; apply access controls consistently across source, normalized, and derived artifacts.

### 20.2 Injection cannot be eliminated — plan for a residual rate

**Ingested text cannot be reliably prevented from steering an LLM.** Under adaptive human attack (464 participants, **272,000 attacks**, 41 scenarios, 13 frontier models), the best model still broke **0.5%** of the time (61 breaks / 12,000 attempts); the best-defended open model broke **5.5%**. **No model was immune.** Static benchmarks understate real vulnerability by **~3–10×**. (`R5 T3`)

**Design for a nonzero, persistent injection rate rather than elimination.** (`R5 T3`)

### 20.3 The architectural defense — this pipeline's strongest asset

**LLM passes with no tool access and schema-constrained output have no action channel.** The only reachable harm is corrupted field values — wrong extraction, poisoned classification, injected text landing in a downstream record — not exfiltration or execution. This collapses the threat from "agent hijack" to "data integrity."

This is the CaMeL principle applied structurally: separate the trusted control path from untrusted content, and never let untrusted content determine what the system *does*. CaMeL's own measurement — 77% of AgentDojo tasks solved *with provable security guarantees* vs 84% undefended, a 7 pp utility cost — quantifies what that separation is worth. (`R5 T3`)

**Corollary requirement:** no pass may grant the model tool access or let document text define the task. Any future change that gives a pass tool access invalidates this section's threat model.

### 20.4 Defense layering, in order of measured payoff

1. **Datamark the untrusted span** — highest-yield, lowest-cost layer: document-summarization ASR **~60% → 3.1%** with no measured task-efficacy cost. (`R5 T3`, Hines et al. 2024)
2. **Do not rely on delimiters alone** — delimiting only halves ASR (~60% → ~30%). It is the weakest layer. (`R5 T3`)
3. **Keep the trusted instruction in the system/control path.** Instruction-hierarchy training improved system-prompt-extraction defense by **63%** and held-out jailbreak robustness by **30%**. (`R5 T3`, Wallace et al. 2024)
4. **Constrain the output schema tightly** — enumerations and typed fields are themselves an injection sink (see §19.3 rule 4 for the near-miss caveat). (`R5 T3`)
5. **Validate outputs downstream** — residual ASR is nonzero regardless. (`R5 T3`)
6. **Do not treat a benchmark score as assurance** — static evals understate adaptive attacks and have documented structural flaws (one benchmark inflates ASR ~8× via forced tool injection; another has no utility metric at all). (`R5 T3`)

Reserve encoding-based spotlighting for high-capability models only — it degraded weaker models in testing. (`R5 T3`)

---

## 21. Quality metrics

As v2 §19, retained in full: normalization coverage; locator-map coverage; units per 1,000 source words; extraction omission rate from sampled audits; atomicity split/merge rate; cluster purity and orphan rate; relationship-class agreement on a gold set; raw-source escalation rate; audit fix/reject rate; provenance resolution success; duplicate-source inflation incidents; queue acceptance/retry rate; leaf correction rate after publication.

**Added metrics, each tied to a documented error rate the pipeline must monitor:**

| Metric | Why | Reference point |
|---|---|---|
| Extraction quality by Claimify factors (entailment / coverage / decontextualization) | Replaces atomicity as the extractor's quality signal | `R1 A5` |
| Coarse-stance vs sub-type agreement | Sub-types are far less reliable than buckets | `R2 F3` (0.401 best fine-type accuracy) |
| Relationship accuracy against a domain gold set | Expect 70–80%; detect drift below | `R2 F4` |
| Contradiction recall (not just precision) | Missed contradictions are the dominant failure mode | `R2 F2` (19.6% flag rate at 88% precision) |
| Auditor order-swap flip rate | Direct measure of position bias in force | `R3 F3` (17–22% expected) |
| Deterministic-check pass rate vs LLM-check pass rate | Divergence indicates LLM check drift | `R3 F6` |
| Batch-size vs accuracy curve | Locate this workload's own degradation point | `R5 T2` |
| Injection-attempt detection rate | Residual rate is nonzero by design | `R5 T3` |

`[NEW — confirm]` This metrics table is assembled from research error rates; v2 §19 did not enumerate these. Each row is research-cited, but the decision to make them standing metrics is an addition.

---

## 22. Acceptance criteria for an implementation

As v2 §21, with amendments:

1. ingest all supported file types without losing structural location; (v2)
2. produce variable-length, schema-valid **molecular** units; (v2, amended per `R1 A3`)
3. trace every retained unit to an exact source excerpt **by character offset and hash**; (v2, sharpened per `R3 F6`)
4. cluster related and unrelated sources without forced merging; (v2)
5. distinguish independent convergence from derivative repetition; (v2)
6. preserve null, contradictory, and qualifying evidence; (v2)
7. correct an overconfident candidate in the audit; (v2)
8. enqueue only approved candidate versions; (v2)
9. resume safely after a failed pass; (v2)
10. reconstruct the full provenance chain from any durable leaf; (v2)
11. **run the audit with a reasoning-class model distinct from the proposer, and record that it did;** (`R3 F1`, `R3 F4`)
12. **verify citations deterministically, not by LLM judgment;** (`R3 F6`)
13. **emit structured per-omission findings, not just a pass/fail completeness verdict;** (`R1 B2`)
14. **survive a prompt-injected source document without the injected instruction changing pipeline behavior** — corrupted field values are in scope for detection, action-channel compromise must be impossible by construction. (`R5 T3`)

---

## 23. Open questions

These were left open by the research and are **not** decided here.

**From round 2:**
1. Do 2026 frontier *reasoning* models close the unguided contradiction-detection gap? No re-evaluation exists in the verified set — GPT-4o (~0.68) is the newest model tested. (`R2` open Q1)
2. What is the empirical reliability of this spec's *specific* relationship vocabulary? No benchmark tests it. A small in-house labeled eval (a few hundred pairs from target document domains) is the only way to get per-label confusion data before trusting fine labels in Pass 4. (`R2` open Q2)
3. Can source independence (`convergent_independent` vs `convergent_dependent`) be detected automatically at acceptable accuracy? The contamination evidence motivates it strongly; no automated method was verified. (`R2` open Q3)

**From round 3:**
4. Is `auditor_confidence` calibratable for this task? Judge calibration was not verified. (`R3`)

**From round 4:**
5. What is the standalone accuracy of an automated abstraction-drift detector, distinct from general grounding/recall? Both supporting claims were refuted; unmeasured. (`R4` open Q4)
6. How do 2024-era specialized checkers (MiniCheck-class) compare against 2025–2026 frontier models as checkers, given the leaderboard appears frozen? The cost advantage is clear; the accuracy gap may have moved. (`R4` open Q5)

**From round 5 / engineering:**
7. Does the thinking-field-before-answer mitigation help or hurt *this* pipeline's passes? It helped 43/72 comparisons but **worsened 15%** — it must be measured per pass, not assumed. (`R5 T1`)
8. Is Docling's parsing fidelity sufficient for this workload's document mix, given it is absent from OmniDocBench's published tables? (`PE T2`)

---

## 24. Research provenance

| File | Tier | Covers |
|---|---|---|
| [`2026-07-31-pipeline-design-verification-research.md`](../research/2026-07-31-pipeline-design-verification-research.md) | Verified (3-vote) | Atomic extraction, routing/retrieval |
| [`2026-07-31-round2-audit-classification-engineering-research.md`](../research/2026-07-31-round2-audit-classification-engineering-research.md) | Verified (3-vote) | Relationship classification, evidence aggregation, temporal knowledge |
| [`2026-08-01-round3-audit-grounding-engineering-research.md`](../research/2026-08-01-round3-audit-grounding-engineering-research.md) | Verified (3-vote) | LLM-as-judge reliability, auditor architecture |
| [`2026-08-01-round4-grounding-structured-context-injection-research.md`](../research/2026-08-01-round4-grounding-structured-context-injection-research.md) | Verified (3-vote) | Grounding checkers, citation/attribution verification |
| [`2026-08-01-round5-structured-outputs-context-injection-research.md`](../research/2026-08-01-round5-structured-outputs-context-injection-research.md) | Sourced | Structured outputs, batch sizing, prompt-injection defense |
| [`2026-08-01-production-engineering-brief.md`](../research/2026-08-01-production-engineering-brief.md) | Sourced | Multi-agent economics, Docling, outbox/durable execution, Batch API |
| [`2026-07-30-claude-plugin-sdk-brief.md`](../research/2026-07-30-claude-plugin-sdk-brief.md) | Sourced | Claude Code plugin anatomy, Anthropic SDK |

Rounds 1–4 ran multi-agent fan-out with 3-vote adversarial verification per claim; refuted claims are listed inside each file for transparency and **must not** be cited as support.
