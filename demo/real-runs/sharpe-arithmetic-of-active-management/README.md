# sharpe-arithmetic-of-active-management

A complete run of the `kip` ingestion pipeline over `sharpe arithmetic active management`.

**38 knowledge units** · **54 citations** (54 verified) · **7 entries handed off** · run `sharpe` · schema `3.1.0`

---

## Reading this folder

**If you are a person:** the [entries](#the-knowledge-handed-off) below are the output — what a knowledge base would receive. The [assets](#assets) are the tables, formulas and page images recovered from the source, shown as they are stored.

**If you are a model asked to ingest this run, do not work from this file.** It is a rendering and it is lossy. Read, in order:

1. [`runs/sharpe/07_enqueue/enqueue.jsonl`](runs/sharpe/07_enqueue/enqueue.jsonl) — **the handoff.** One JSON event per approved entry, each with `payload.title`, `payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This is the only file you need in order to ingest; everything below is for checking what it says.
2. [`runs/sharpe/02_units/units.jsonl`](runs/sharpe/02_units/units.jsonl) — the evidence. Each unit carries verbatim excerpts with character offsets into `normalized.txt`, and `asset_ref` where the evidence is a table cell or a formula. Follow `payload.source_unit_ids` from an entry to get here.
3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. **Check `fidelity` before you trust a comparison:** `exact` came from the source's own markup and can be compared as a string; `transcribed` was read off an image and must not be.
4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset citation resolves against, by character offset.
5. [`runs/sharpe/00_original_sources/`](runs/sharpe/00_original_sources) — the raw source, unmodified. Go here when you need to check the pipeline itself.

Everything else records how the output was arrived at: the routing, the judgments, the candidates before audit, and the audit findings.

## What is in each folder

| folder | contents |
|---|---|
| [`00_original_sources`](runs/sharpe/00_original_sources) | The source documents exactly as ingested, byte for byte. |
| [`01_normalized`](runs/sharpe/01_normalized) | One directory per source: `normalized.txt` (the flat text every citation resolves against), `assets.jsonl` (tables, formulas and figures the flat text could not hold), `manifest.json`, and `assets/` for any rendered page images. |
| [`02_units`](runs/sharpe/02_units) | `units.jsonl` — every extracted knowledge unit with its verbatim evidence and character offsets. `omissions.jsonl` — what the completeness check found missing. `rejects.jsonl` if any record failed materialization. |
| [`03_clusters`](runs/sharpe/03_clusters) | Which units were routed together for comparison, and why. |
| [`04_assessments`](runs/sharpe/04_assessments) | One judgment per claim: does the evidence support it, contradict it, or settle nothing, and how many INDEPENDENT sources it rests on. |
| [`05_candidates`](runs/sharpe/05_candidates) | Proposed knowledge-base entries, before audit. |
| [`06_audit`](runs/sharpe/06_audit) | `audits.jsonl` — the adversarial review of each candidate, with deterministic check results. `corpus_coverage.json` — whether the output fairly represents the whole corpus. |
| [`07_enqueue`](runs/sharpe/07_enqueue) | **`enqueue.jsonl` is the handoff.** One idempotent event per approved entry. This is the file a consuming knowledge base reads. |
| [`_handoff`](runs/sharpe/_handoff) | The complete record of every model call: `pending.jsonl` holds the requests, `responses.jsonl` the answers. Copying `responses.jsonl` into a fresh workspace replays the entire run from cache. |

## Does the output represent the corpus?

The run's own corpus-coverage audit returned **`represented`**.

> This source has no non-textual content of any kind -- no mathematical notation, no tables, no figures. Pass 0 produced an empty assets.jsonl, which is the correct result and not a gap: the paper's argument is arithmetic stated in words, and Sharpe says so ('they depend only on the laws of addition, subtraction, multiplication and division').

> The footnotes carry more weight in this document than in the others: three of the five state conditions without which a body claim is false. Treating them as content rather than apparatus is what keeps the output honest, and it is worth noting because a pipeline that discarded footnotes would produce an output that still looked complete.

> Not loss: the repair round's five units overlap the first round in subject (both cover the argument's setup) but not in content -- the first round cited one of the four opening quotations and the repair round carried the other three.

Full judgment: [`06_audit/corpus_coverage.json`](runs/sharpe/06_audit/corpus_coverage.json).

## What the checks found

- The completeness check reported **6 finding(s)** against the first extraction: [`02_units/omissions.jsonl`](runs/sharpe/02_units/omissions.jsonl).
- The adversarial audit reviewed **7 candidate(s)** and passed 0 without requiring a correction: [`06_audit/audits.jsonl`](runs/sharpe/06_audit/audits.jsonl).

## Assets

None. This source carried no tables, formulas or figures — the flat text in `01_normalized/` is the whole of it. An empty asset bundle is a result, not a gap.

## The knowledge handed off

Rendered from [`07_enqueue/enqueue.jsonl`](runs/sharpe/07_enqueue/enqueue.jsonl) — 7 event(s), target `existing-leaf-engine`.

---

### 1. Sharpe's arithmetic: the average actively managed dollar must underperform

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-001-r1` v2

**Slug** `sharpe-s-arithmetic-the-average-actively-managed-dollar-must-underperform`

The paper's two assertions and their proofs. Before costs the average actively managed dollar earns exactly the market return; after costs it earns less. Both follow from a weighted-average identity and a cost inequality, and from nothing else -- no model of equilibrium, no assumption about how markets price.

**Assertions (8)**

1. If active and passive management are defined sensibly, then before costs the return on the average actively managed dollar equals the return on the average passively managed dollar; after costs it is less.

   *backed by* `asmt-0001`

2. The two arithmetic assertions about active and passive returns hold for any time period and depend only on the laws of addition, subtraction, multiplication and division -- nothing else is required, no theory of market equilibrium among it.

   *backed by* `asmt-0002`

3. Assertion 1 follows in one step: the market return must equal a weighted average of the returns on the passive and active segments, and the passive segment earns the market return, so the active segment must earn it too -- if the first two returns are the same, the third must be also.

   *backed by* `asmt-0010`

4. Assertion 2 needs only the fact that actively managing a given number of dollars costs more than managing them passively -- active managers must pay for more research and pay more for trading, and security analysts, brokers, traders, specialists and other market-makers all must eat.

   *backed by* `asmt-0011`

5. Because active and passive returns are equal before cost and active managers bear greater costs, the after-cost return from active management must be lower than that from passive management.

   *backed by* `asmt-0012`

6. Both proofs use only simple principles of arithmetic -- the second is described as embarrassingly simple, using the most rudimentary notions -- which is what makes the conclusion hard to escape: there is no model to dispute, only addition, subtraction, multiplication and division.

   *backed by* `asmt-0001`

7. Over any specified period the market return is a weighted average of the returns on the securities in the market, using beginning market values as the weights.

   *backed by* `asmt-0008`

8. Each passive manager obtains precisely the market return before costs, because holding every security in market proportions reproduces the weighted average that defines the market return.

   *backed by* `asmt-0009`

**Related topics** `Defining active and passive management`, `Measuring active management honestly`

**Source units (8)** `u-src-sharpe-arithmetic-active-management-f419bef6-0001`, `u-src-sharpe-arithmetic-active-management-f419bef6-0002`, `u-src-sharpe-arithmetic-active-management-f419bef6-0010`, `u-src-sharpe-arithmetic-active-management-f419bef6-0011`, `u-src-sharpe-arithmetic-active-management-f419bef6-0012`, `u-src-sharpe-arithmetic-active-management-f419bef6-0037`, `u-src-sharpe-arithmetic-active-management-f419bef6-0008`, `u-src-sharpe-arithmetic-active-management-f419bef6-0009`

**Traceability** — idempotency key `c9f8a439ee3fb1e6977b969893e2624a056603d3f48e625a7755512e7e964d85` · queue event `q-c9f8a439ee3fb1e6` · audits `audit-cand-001`

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

### 2. Defining active and passive management, and why the definitions carry the proof

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-002-r1` v2

**Slug** `defining-active-and-passive-management-and-why-the-definitions-carry-the-proof`

The arithmetic is only exact because of how its terms are fixed: a market chosen in advance, a passive investor holding every security in market proportions, and an active investor defined as anyone who is not passive. The last is what makes the two categories exhaustive, and the proof depends on that.

**Assertions (5)**

1. The arithmetic requires that a market be selected first -- the stocks in the S&P 500, for example, or a set of small stocks -- after which every investor holding securities from that market is classified as either active or passive.

   *backed by* `asmt-0004`

2. A passive investor always holds every security in the selected market in market proportions: if security X is 3 per cent of the market's value, a passive portfolio holds 3 per cent of its value in X -- equivalently, the same percentage of the total outstanding amount of every security.

   *backed by* `asmt-0005`

3. An active investor is defined negatively, as one who is not passive: the portfolio differs from the passive portfolio at some or all times, and because active managers act on perceptions of mispricing that change frequently, they tend to trade frequently -- which is where the term comes from.

   *backed by* `asmt-0006`

4. Because active is defined as not-passive, the two categories are exhaustive over the holders of securities in the selected market, which is what makes the weighted-average argument work: there is no third segment for returns to hide in.

   *backed by* `asmt-0007`

5. When computing each security's total outstanding amount for the passive-holding definition, cross-holdings within the market should be netted out.

   *backed by* `asmt-0028`

**Source units (5)** `u-src-sharpe-arithmetic-active-management-f419bef6-0004`, `u-src-sharpe-arithmetic-active-management-f419bef6-0005`, `u-src-sharpe-arithmetic-active-management-f419bef6-0006`, `u-src-sharpe-arithmetic-active-management-f419bef6-0007`, `u-src-sharpe-arithmetic-active-management-f419bef6-0029`

**Traceability** — idempotency key `f9fd7388dc7e75cf9460dcad4493c3d167310582a958703ef6aa01f5371fb990` · queue event `q-f9fd7388dc7e75cf` · audits `audit-cand-002`

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

### 3. Why measured active performance appears to beat the market

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-003-r1` v2

**Slug** `why-measured-active-performance-appears-to-beat-the-market`

Three measurement failures, each of which can make active managers look better than the arithmetic allows: passive managers who are not passive, an active sample that omits part of the non-passive segment, and summary statistics that do not weight by dollars under management. The specific distortions -- survivorship bias, benchmark mismatch, small-cap bias from equal weighting -- sit under them.

**Assertions (11)**

1. Empirical evidence appearing to show active managers beating the market can be explained by three measurement failures rather than by any failure of the arithmetic.

   *backed by* `asmt-0013`

2. The first measurement failure is that the passive managers in a comparison may not be truly passive: some index fund managers sample the market rather than holding all its securities in market proportions, and some charge fees high enough to bring total costs to equal or exceed those of active managers.

   *backed by* `asmt-0001`

3. The second measurement failure is that the active managers in a comparison may not represent the whole non-passive component of the market -- most empirical analyses consider only professional or institutional active managers and exclude active holders such as individual investors.

   *backed by* `asmt-0001`

4. Institutional active managers can beat passive managers after cost as a group, but only if non-institutional individual investors are foolish enough to pay the added costs of institutional active management through inferior performance -- the arithmetic still binds, the losses have merely moved to a group nobody measured.

   *backed by* `asmt-0015`

5. A comparison is also distorted when active managers hold securities from outside the market being used as the benchmark: equity mutual funds holding cash are generally beaten badly by an all-equity index in up markets and sometimes exceed it in down markets.

   *backed by* `asmt-0001`

6. Survivorship bias inflates measured active performance: excluding managers who went out of business during the period removes those likely to have had especially poor returns, so the results look better than what the average actively managed dollar obtained.

   *backed by* `asmt-0001`

7. The third measurement failure, and possibly the most important in practice, is that summary statistics for active managers may not represent the average actively managed DOLLAR: computing that requires weighting each manager's return by the dollars under management at the beginning of the period, whereas comparisons often use a simple average across managers or the median manager.

   *backed by* `asmt-0001`

8. Equal-weighting active manager returns imports a small-capitalization bias, because equity fund managers with smaller amounts of money tend to favor stocks with smaller outstanding values -- so the average active manager is beaten badly when small-cap stocks underperform and may exceed the market when they do well.

   *backed by* `asmt-0017`

9. Whichever way the equal-weighted average moves, the average actively managed dollar underperforms the market net of costs in both cases -- the size bias changes what the statistic shows, not what the arithmetic requires.

   *backed by* `asmt-0018`

10. Properly measured, the average actively managed dollar must underperform the average passively managed dollar net of costs, and empirical analyses that appear to refute this principle are guilty of improper measurement.

   *backed by* `asmt-0001`

11. The three reasons given for apparent refutations are not an exhaustive list: others exist, such as differential treatment of dividend reinvestment and of mergers and acquisitions, but they are typically less important.

   *backed by* `asmt-0001`

**Related topics** `Sharpe's arithmetic: the average actively managed dollar must underperform`

**Source units (11)** `u-src-sharpe-arithmetic-active-management-f419bef6-0013`, `u-src-sharpe-arithmetic-active-management-f419bef6-0014`, `u-src-sharpe-arithmetic-active-management-f419bef6-0015`, `u-src-sharpe-arithmetic-active-management-f419bef6-0016`, `u-src-sharpe-arithmetic-active-management-f419bef6-0017`, `u-src-sharpe-arithmetic-active-management-f419bef6-0018`, `u-src-sharpe-arithmetic-active-management-f419bef6-0019`, `u-src-sharpe-arithmetic-active-management-f419bef6-0020`, `u-src-sharpe-arithmetic-active-management-f419bef6-0021`, `u-src-sharpe-arithmetic-active-management-f419bef6-0022`, `u-src-sharpe-arithmetic-active-management-f419bef6-0032`

**Traceability** — idempotency key `5eedbaf28aadb2d3f9956f2b3505adee5ddb743422dddacafadaeab38d7cb9db` · queue event `q-5eedbaf28aadb2d3` · audits `audit-cand-003`

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

### 4. Measuring a manager against a passive alternative chosen in advance

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-004-r1` v2

**Slug** `measuring-a-manager-against-a-passive-alternative-chosen-in-advance`

What follows for practice: peer-group comparisons are a poor basis for decisions, equal-weighted and median-manager alternatives are not practical, and the only measurement that answers the question is against a feasible passive benchmark identified before the period begins.

**Assertions (4)**

1. Peer-group comparisons are dangerous as a basis for decisions: the capitalization-weighted average performance of active managers is inferior to a passive alternative by the arithmetic, and most peer-group averages are not capitalization-weighted, so they carry additional biases on top of that.

   *backed by* `asmt-0001`

2. Investing equal amounts with many managers is not a practical alternative to capitalization weighting, and investing with the median manager is less practical still, since that manager's identity is not known in advance.

   *backed by* `asmt-0001`

3. The right way to measure a manager's performance is against a comparable passive alternative -- a benchmark or normal portfolio -- which must be a feasible alternative identified IN ADVANCE of the period over which performance is measured.

   *backed by* `asmt-0024`

4. Only with in-advance benchmark measurement in place can an active manager, or someone who hires active managers, know whether he or she is in the minority who have beaten viable passive alternatives.

   *backed by* `asmt-0027`

**Source units (4)** `u-src-sharpe-arithmetic-active-management-f419bef6-0025`, `u-src-sharpe-arithmetic-active-management-f419bef6-0026`, `u-src-sharpe-arithmetic-active-management-f419bef6-0027`, `u-src-sharpe-arithmetic-active-management-f419bef6-0028`

**Traceability** — idempotency key `4e47423d1d27e2cb6fdb8ffc305f53a12907033051d1486e87270232701700b9` · queue event `q-4e47423d1d27e2cb` · audits `audit-cand-004`

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

### 5. What Sharpe's arithmetic still leaves possible

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-005-r1` v2

**Slug** `what-sharpe-s-arithmetic-still-leaves-possible`

The result is not a counsel of despair. Some active managers beat passive after costs, necessarily a minority of actively managed dollars; and an investor can assemble a set of active managers that collectively beats passive if the ones managing a majority of that investor's active funds do.

**Assertions (2)**

1. The arithmetic is not a counsel of despair: some active managers can beat their passive counterparts even after costs, but they must manage a minority share of the actively managed dollars in the market in question.

   *backed by* `asmt-0001`

2. An investor such as a pension fund can choose a set of active managers that collectively beats a passive alternative after costs; not all the managers in the set need beat their passive counterparts, only those managing a majority of that investor's actively managed funds.

   *backed by* `asmt-0014`

**Source units (2)** `u-src-sharpe-arithmetic-active-management-f419bef6-0023`, `u-src-sharpe-arithmetic-active-management-f419bef6-0024`

**Traceability** — idempotency key `e3103c18e7d557cb3865c0669bc8a7dfee638149ccb608a8baaa734e4c059617` · queue event `q-e3103c18e7d557cb` · audits `audit-cand-005`

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

### 6. Scope limits on Sharpe's arithmetic

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-006-r1` v2

**Slug** `scope-limits-on-sharpe-s-arithmetic`

The footnoted conditions the body's claims depend on: cross-holdings netted out, corporate events ignored for simplicity without affecting the principles, and passive managers assumed to hold across the whole period rather than trade within it.

**Assertions (2)**

1. Mergers, new listings and reinvestment of dividends occurring during the period require more complex calculations than the simple weighted average, but do not affect the basic principles; the paper ignores them to keep things simple.

   *backed by* `asmt-0001`

2. The claim that passive managers obtain precisely the market return assumes they buy before the period begins and do not sell until after it ends; when passive managers do trade, they may have to trade with active managers, who are paid for providing that liquidity.

   *backed by* `asmt-0001`

**Related topics** `Sharpe's arithmetic: the average actively managed dollar must underperform`

**Source units (2)** `u-src-sharpe-arithmetic-active-management-f419bef6-0030`, `u-src-sharpe-arithmetic-active-management-f419bef6-0031`

**Traceability** — idempotency key `d2471dbda9949f97b15d361fff55c9cbff64ee9d7c6e8b9c6380c318fa20482a` · queue event `q-d2471dbda9949f97` · audits `audit-cand-006`

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

### 7. The claims Sharpe's arithmetic was written to answer

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-007-r1` v2

**Slug** `the-claims-sharpe-s-arithmetic-was-written-to-answer`

The four practitioner assertions the paper opens with, the specific reply to the small-stocks one, Sharpe's concession that he is belaboring the obvious, and his reason for doing it anyway. Also the paper's own two-part structure and its publication details.

**Assertions (6)**

1. Sharpe's target is the claim that passive management rests on complex and unrealistic theories of capital market equilibrium: the conclusions of investment professionals who say otherwise can usually be justified only by assuming the laws of arithmetic have been suspended for the convenience of those who choose careers as active managers.

   *backed by* `asmt-0003`

2. The claims Sharpe's arithmetic is written against are that index funds tracking the S&P 500 are a fad whose past-decade advantage may prove transitory, that in small stocks especially an investor is probably better off with an active manager than buying the market, and that any graduate of a good business school should beat an index fund over a market cycle.

   *backed by* `asmt-0033`

3. The small-stocks claim is answered by the market-selection step rather than by evidence: because the arithmetic holds for any market defined in advance -- including a set of small stocks -- active managers in small stocks are bound by it exactly as they are in the S&P 500.

   *backed by* `asmt-0034`

4. Sharpe concedes the result is obvious and belabored, and justifies publishing it by the ubiquity of statements denying it -- the paper exists because the arithmetic is widely disregarded, not because it is difficult.

   *backed by* `asmt-0035`

5. The paper divides in two: a formal half proving the two assertions from arithmetic, and a practical half explaining why measured evidence appears to contradict them -- Sharpe marks the boundary himself.

   *backed by* `asmt-0001`

6. The paper was published in the Financial Analysts' Journal, Vol. 47, No. 1, January/February 1991, pages 7-9, and the first two of its opening quotations come from the September 3, 1990 issue of Forbes.

   *backed by* `asmt-0032`

**Source units (6)** `u-src-sharpe-arithmetic-active-management-f419bef6-0003`, `u-src-sharpe-arithmetic-active-management-f419bef6-0034`, `u-src-sharpe-arithmetic-active-management-f419bef6-0035`, `u-src-sharpe-arithmetic-active-management-f419bef6-0036`, `u-src-sharpe-arithmetic-active-management-f419bef6-0038`, `u-src-sharpe-arithmetic-active-management-f419bef6-0033`

**Traceability** — idempotency key `ed5b47a7afffc3d2155f316f71e82dc7e31cd226fe2aa273f74003162f98b7e7` · queue event `q-ed5b47a7afffc3d2` · audits `audit-cand-007`

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
