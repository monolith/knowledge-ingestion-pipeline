# ge-aerospace-10k-fy2025

A complete run of the `kip` ingestion pipeline over `ge 10k fy2025`.

**116 knowledge units** · **242 citations** (242 verified) · **31 entries handed off** · run `ge` · schema `3.1.0`

---

## Reading this folder

**If you are a person:** the [entries](#the-knowledge-handed-off) below are the output — what a knowledge base would receive. The [assets](#assets) are the tables, formulas and page images recovered from the source, shown as they are stored.

**If you are a model asked to ingest this run, do not work from this file.** It is a rendering and it is lossy. Read, in order:

1. [`runs/ge/07_enqueue/enqueue.jsonl`](runs/ge/07_enqueue/enqueue.jsonl) — **the handoff.** One JSON event per approved entry, each with `payload.title`, `payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This is the only file you need in order to ingest; everything below is for checking what it says.
2. [`runs/ge/02_units/units.jsonl`](runs/ge/02_units/units.jsonl) — the evidence. Each unit carries verbatim excerpts with character offsets into `normalized.txt`, and `asset_ref` where the evidence is a table cell or a formula. Follow `payload.source_unit_ids` from an entry to get here.
3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. **Check `fidelity` before you trust a comparison:** `exact` came from the source's own markup and can be compared as a string; `transcribed` was read off an image and must not be.
4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset citation resolves against, by character offset.
5. [`runs/ge/00_original_sources/`](runs/ge/00_original_sources) — the raw source, unmodified. Go here when you need to check the pipeline itself.

Everything else records how the output was arrived at: the routing, the judgments, the candidates before audit, and the audit findings.

## What is in each folder

| folder | contents |
|---|---|
| [`00_original_sources`](runs/ge/00_original_sources) | The source documents exactly as ingested, byte for byte. |
| [`01_normalized`](runs/ge/01_normalized) | One directory per source: `normalized.txt` (the flat text every citation resolves against), `assets.jsonl` (tables, formulas and figures the flat text could not hold), `manifest.json`, and `assets/` for any rendered page images. |
| [`02_units`](runs/ge/02_units) | `units.jsonl` — every extracted knowledge unit with its verbatim evidence and character offsets. `omissions.jsonl` — what the completeness check found missing. `rejects.jsonl` if any record failed materialization. |
| [`03_clusters`](runs/ge/03_clusters) | Which units were routed together for comparison, and why. |
| [`04_assessments`](runs/ge/04_assessments) | One judgment per claim: does the evidence support it, contradict it, or settle nothing, and how many INDEPENDENT sources it rests on. |
| [`05_candidates`](runs/ge/05_candidates) | Proposed knowledge-base entries, before audit. |
| [`06_audit`](runs/ge/06_audit) | `audits.jsonl` — the adversarial review of each candidate, with deterministic check results. `corpus_coverage.json` — whether the output fairly represents the whole corpus. |
| [`07_enqueue`](runs/ge/07_enqueue) | **`enqueue.jsonl` is the handoff.** One idempotent event per approved entry. This is the file a consuming knowledge base reads. |
| [`_handoff`](runs/ge/_handoff) | The complete record of every model call: `pending.jsonl` holds the requests, `responses.jsonl` the answers. Copying `responses.jsonl` into a fresh workspace replays the entire run from cache. |

## Does the output represent the corpus?

The run's own corpus-coverage audit returned **`gaps`**, with 2 gap(s) named.

- **The Statement of Operations, the Statement of Financial Position and the Statement of Comprehensive Income sit in regions that produced no units. Total revenue, total assets, total shareholders' equity and comprehensive income each have no representation in the output.** A consumer asking what GE Aerospace earned or is worth in 2025 finds net income and operating cash flow -- recovered this round -- and nothing else from the primary statements. The tables are in the record and anchored, so the material is not lost; nothing points at it, because nothing was read from around it.

- **Thirty-eight substantive financial tables in total carry four or more money figures and relate to no unit: remaining performance obligations, adjusted non-GAAP revenue and margin, the pension plan funded status, accumulated other comprehensive income, and segment revenue and operating profit among them.** The extraction reads this filing's narrative and does not read its tables. That is a property of the reading, not of the asset layer: the tables were all recovered, all but one anchored, and thirty-nine of them travel with the text that was read. The remaining sixty-one mark where the reading did not go.

> This is the first run where the gap is measurable. Before assets were anchored, the same hole showed only as an unexplained count of uncited tables, which could equally have meant the extractor had no reason to quote them. An anchored table in a passage that produced no units is a different and sharper claim: nothing was read there.

> Thirty-nine tables now relate to units, against eight cited before. Twenty-eight of those relate because they sit in text that was read, with no unit quoting them -- which is the behaviour the anchoring was built for.

> Not a gap: twenty-nine of the sixty-one unrelated tables are the cover page, the filer-status checkboxes, the securities-registered list and similar. They should produce no units and their absence misrepresents nothing.

> The density figure and this count are the same finding seen twice: 116 units for 56,836 words is one per 490 words, the sparsest of the six demo runs, and the sparsity is concentrated exactly where the tables are.

Full judgment: [`06_audit/corpus_coverage.json`](runs/ge/06_audit/corpus_coverage.json).

## What the checks found

- The completeness check reported **3 finding(s)** against the first extraction: [`02_units/omissions.jsonl`](runs/ge/02_units/omissions.jsonl).
- The adversarial audit reviewed **31 candidate(s)** and passed 31 without requiring a correction: [`06_audit/audits.jsonl`](runs/ge/06_audit/audits.jsonl).

## Assets

**100 assets** — 100 table. 11 cited by at least one unit, 89 not cited.

An uncited asset is not a failure. A source carries structure that is not content -- a navigation box marked up as a table, a page rendered to check one equation on it -- and capturing it losslessly while citing nothing from it is the correct outcome.

Fidelity is part of the record, because the kinds are not equally trustworthy:

- **exact** (100) — structure recovered from markup the source itself carried — citable as a quote

Evidence cites an asset with `asset_ref {asset_id, row, col}` for a table cell, or `{asset_id}` for a formula. A cell reference resolves to the value **and** the headers governing it, which is what makes a figure checkable rather than merely quoted.

### `src-ge-10k-fy2025-a73b722f`

[`normalized.txt`](runs/ge/01_normalized/src-ge-10k-fy2025-a73b722f/normalized.txt) · [`assets.jsonl`](runs/ge/01_normalized/src-ge-10k-fy2025-a73b722f/assets.jsonl) · [`manifest.json`](runs/ge/01_normalized/src-ge-10k-fy2025-a73b722f/manifest.json)

#### `tbl-src-ge-10k-fy2025-a73b722f-0001`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| New York |   |   | 14-0689340 |
|---|---|---|---|
| (State or other jurisdiction of incorporation or organization) |   |   | (I.R.S. Employer Identification No.) |
| 1 Neumann Way | Evendale | OH | 45215 |
| (Address of principal executive offices) |   |   | (Zip Code) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0002`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Title of each class | Trading Symbol(s) | Name of each exchange on which registered |
|---|---|---|
| Common stock, par value $0.01 per share | GE | New York Stock Exchange |
| 1.875% Notes due 2027 | GE 27E | New York Stock Exchange |
| 1.500% Notes due 2029 | GE 29 | New York Stock Exchange |
| 7 1/2% Guaranteed Subordinated Notes due 2035 | GE /35 | New York Stock Exchange |
| 2.125% Notes due 2037 | GE 37 | New York Stock Exchange |

#### `tbl-src-ge-10k-fy2025-a73b722f-0003`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Large accelerated filer | ☑ | Accelerated filer | ☐ |
|---|---|---|---|
| Non-accelerated filer | ☐ | Smaller reporting company | ☐ |
| Emerging growth company | ☐ |   |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0004`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**Page**

| Page |   |
|---|---|
| Forward-Looking Statements | 3 |
| About GE Aerospace | 4 |
| Management’s Discussion and Analysis of Financial Condition and Results of Operations (MD&A) | 7 |
| Consolidated Results | 8 |
| Segment Operations | 9 |
| Corporate & Other | 10 |
| Other Consolidated Information | 11 |
| Capital Resources and Liquidity | 12 |
| Critical Accounting Estimates | 14 |
| Other Items | 16 |
| Non-GAAP Financial Measures | 19 |

*(41 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0005`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| (In millions) | 2025 | 2024 | 2023 |
|---|---|---|---|
| GE Aerospace funded | $1,580 | $1,286 | $1,011 |
| Customer and partner funded(a) | 1,409 | 1,413 | 1,465 |
| Total Research and development | $2,989 | $2,699 | $2,476 |

Related units: `u-src-ge-10k-fy2025-a73b722f-0008`

#### `tbl-src-ge-10k-fy2025-a73b722f-0006`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| REVENUE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Equipment revenue | $12,159 | $10,274 | $9,318 |
| Services revenue | 30,163 | 24,847 | 22,641 |
| Insurance revenue | 3,533 | 3,581 | 3,389 |
| Total revenue | $45,855 | $38,702 | $35,348 |

Related units: `u-src-ge-10k-fy2025-a73b722f-0020`

#### `tbl-src-ge-10k-fy2025-a73b722f-0007`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**NET INCOME (LOSS) AND EARNINGS (LOSS) PER SHARE (EPS)**

| NET INCOME (LOSS) AND EARNINGS (LOSS) PER SHARE (EPS) |   |   |   |
|---|---|---|---|
| (Per-share in dollars and diluted) | 2025 | 2024 | 2023 |
| Net income (loss) from continuing operations attributable to common shareholders | $8,601 | $6,670 | $9,154 |
| Continuing EPS | $8.05 | $6.09 | $8.33 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0008`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $27,534 | $22,509 | $16,247 |
| Services | 163,029 | 149,127 | 137,756 |
| Total RPO | $190,564 | $171,635 | $154,003 |

Related units: `u-src-ge-10k-fy2025-a73b722f-0024`

#### `tbl-src-ge-10k-fy2025-a73b722f-0009`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| Sales in units, except where noted | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines | 2,386 | 1,911 | 2,075 |
| LEAP Engines(a) | 1,802 | 1,407 | 1,570 |
| Internal shop visit revenue growth % | 24% | 19% | 27% |
| (a) LEAP engines, which are in a significant production ramp, are a subset of Commercial Engines. |   |   |   |

Related units: `u-src-ge-10k-fy2025-a73b722f-0025`

#### `tbl-src-ge-10k-fy2025-a73b722f-0010`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| SEGMENT REVENUE AND PROFIT | 2025 | 2024 | 2023 |
|---|---|---|---|
| Equipment | $8,304 | $7,106 | $6,169 |
| Services | 25,010 | 19,775 | 17,686 |
| Total segment revenue | $33,314 | $26,881 | $23,855 |
| Segment profit | $8,861 | $7,055 | $5,643 |
| Segment profit margin | 26.6% | 26.2% | 23.7% |

Related units: `u-src-ge-10k-fy2025-a73b722f-0026`

#### `tbl-src-ge-10k-fy2025-a73b722f-0011`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $13,754 | $11,462 | $6,508 |
| Services | 156,068 | 142,182 | 131,028 |
| Total RPO | $169,822 | $153,644 | $137,535 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0012`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Sales in units | 2025 | 2024 | 2023 |
|---|---|---|---|
| Defense engines | 635 | 490 | 556 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0013`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| SEGMENT REVENUE AND PROFIT | 2025 | 2024 | 2023 |
|---|---|---|---|
| Defense & Systems (D&S) | $6,574 | $6,109 | $5,927 |
| Propulsion & Additive Technologies (P&AT) | 3,980 | 3,370 | 3,034 |
| Total segment revenue | $10,554 | $9,478 | $8,961 |
| Equipment | $5,128 | $4,208 | $4,000 |
| Services | 5,426 | 5,270 | 4,961 |
| Total segment revenue | $10,554 | $9,478 | $8,961 |
| Segment profit | $1,296 | $1,061 | $908 |
| Segment profit margin | 12.3% | 11.2% | 10.1% |

Related units: `u-src-ge-10k-fy2025-a73b722f-0028`

#### `tbl-src-ge-10k-fy2025-a73b722f-0014`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $13,780 | $11,046 | $9,739 |
| Services | 6,962 | 6,944 | 6,729 |
| Total RPO | $20,742 | $17,991 | $16,468 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0015`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| REVENUE AND OPERATING PROFIT (COST) | 2025 | 2024 | 2023 |
|---|---|---|---|
| Insurance revenue (Note 12) | $3,533 | $3,581 | $3,389 |
| Eliminations and other | (1,546) | (1,239) | (857) |
| Corporate & Other revenue | $1,987 | $2,343 | $2,532 |
| Gains (losses) on purchases and sales of business interests | 5 | 398 | (104) |
| Gains (losses) on retained and sold ownership interests and other equity securities (Note 19) | 312 | 532 | 5,776 |
| Restructuring and other charges (Note 20)(a) | 87 | (525) | (246) |
| Separation costs (Note 20) | (202) | (492) | (692) |
| Insurance profit (loss) (Note 12) | 992 | 1,022 | 332 |
| U.S. tax equity profit (loss) | (189) | (160) | (132) |
| Goodwill impairments (Note 7) | — | (251) | — |
| Adjusted Corporate & Other operating costs (Non-GAAP) | (1,102) | (864) | (990) |

*(7 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0016`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Effective tax rate (ETR) | 14.1% | 12.6% | 9.5% |
| Provision (benefit) for income taxes | $1,405 | $962 | $994 |
| Cash income taxes paid(a) | 585 | 852 | 994 |

Related units: `u-src-ge-10k-fy2025-a73b722f-0033`

#### `tbl-src-ge-10k-fy2025-a73b722f-0017`

table · **exact** · extractor `html_tables_v1` · anchored by `none` · not cited by any unit

|   | Moody's | S&P |
|---|---|---|
| Outlook | Positive | Stable |
| Short term | P-2 | A-2 |
| Long term | A3 | A- |

#### `tbl-src-ge-10k-fy2025-a73b722f-0018`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Years ended December 31 | 2025 | 2024 |
|---|---|---|
| Increase (decrease) in employee benefit liabilities | $746 | $356 |
| Net restructuring and other charges/(cash expenditures) | (144) | (112) |
| (Gains) Losses on purchases and sales of business interests | (6) | (399) |
| Net interest and other financial charges/(cash paid) | (39) | 31 |
| Other deferred assets | (88) | (84) |
| Other | (334) | (118) |
| All other operating activities | $136 | $(326) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0019`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 1 unit

| December 31, 2025 | ERAC | UFLIC | Total |
|---|---|---|---|
| GAAP: Ending balance of reserves at locked-in rate | $18,887 | $4,950 | $23,837 |
| Gross statutory reserves(a) | 23,943 | 5,900 | 29,843 |
| Number of policies in force | 161,300 | 40,400 | 201,700 |
| Number of covered lives in force | 212,600 | 40,400 | 253,000 |
| Average policyholder attained age | 79 | 85 | 80 |
| GAAP: Ending balance of reserves at locked-in rate per policy (in actual dollars) | $117,107 | $122,670 | $118,220 |
| GAAP: Ending balance of reserves at locked-in rate per covered life (in actual dollars) | 88,854 | 122,670 | 94,249 |
| Statutory: Gross reserves per policy (in actual dollars)(a) | 148,441 | 146,050 | 147,962 |
| Statutory: Gross reserves per covered life (in actual dollars)(a) | 112,622 | 146,050 | 117,960 |
| Percentage of policies with: |   |   |   |
| Lifetime benefit period | 69% | 31% | 63% |

*(4 further rows in the stored grid.)*

Related units: `u-src-ge-10k-fy2025-a73b722f-0049`

#### `tbl-src-ge-10k-fy2025-a73b722f-0020`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Assumption | Hypothetical change in 2025 assumption | Estimated adverse impact to projected present value of future cash flows (In millions, pre-tax) |
|---|---|---|
| Morbidity: |   |   |
| Long-term care insurance incidence rates | 5% increase in incidence rates | $600 |
| Long-term care insurance claim continuance | 5% reduction in disabled life deaths | $1,200 |
| Long-term care insurance utilization | 5% increase in utilization | $1,200 |
| Long-term care insurance morbidity improvement | 25 basis point reduction by age with 0% floorNo morbidity improvement | $300$1,200 |
| Active life terminations: |   |   |
| Long-term care insurance mortality | 5% reduction in mortality | $300 |
| Long-term care insurance future premium rate increases | 25% adverse change in success rate on premium rate increase actions not yet approved | $200 |
| Long-term care inflation | 0.25% increase to long-term care inflation rate | $100 |
| Life insurance mortality | 5% increase in mortality | $100 |
| Structured settlement annuity mortality | Impaired life mortality grades to standard ten years earlier | $300 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0021`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ADJUSTED REVENUE, OPERATING PROFIT AND PROFIT MARGIN (NON-GAAP) | 2025 | 2024 |
|---|---|---|
| Total revenue (GAAP) | $45,855 | $38,702 |
| Less: Insurance revenue (Note 12) | 3,533 | 3,581 |
| Adjusted revenue (Non-GAAP) | $42,322 | $35,121 |
| Total costs and expenses (GAAP) | $37,342 | $33,346 |
| Less: Insurance cost and expenses (Note 12) | 2,541 | 2,560 |
| Less: U.S. tax equity cost and expenses | 20 | 14 |
| Less: interest and other financial charges(a) | 843 | 986 |
| Less: non-operating benefit cost (income) | (788) | (842) |
| Less: restructuring & other(a) | (87) | 525 |
| Less: goodwill impairments(a) | — | 251 |
| Less: separation costs(a) | 202 | 492 |

*(13 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0022`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ADJUSTED NET INCOME (LOSS) AND ADJUSTED EFFECTIVE INCOME TAX RATE (NON-GAAP) | 2025 |   |   | 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
| (Diluted, per-share amounts in dollars) |   | Income |   | EPS |   | Income |   | EPS |   |
| Net income (loss) from continuing operations (GAAP) (Note 18) |   |   | $8,598 |   | $8.05 |   | $6,670 |   | $6.09 |
| Insurance net income (loss) (pre-tax) |   | 1,002 |   | 0.94 |   | 1,025 |   | 0.94 |   |
| Tax effect on Insurance net income (loss)(a) |   | (125) |   | (0.12) |   | (219) |   | (0.20) |   |
| Less: Insurance net income (loss) (net of tax) (Note 12) |   | 877 |   | 0.82 |   | 806 |   | 0.74 |   |
| U.S. tax equity net income (loss) (pre-tax) |   | (220) |   | (0.21) |   | (191) |   | (0.17) |   |
| Tax effect on U.S. tax equity net income (loss) |   | 259 |   | 0.24 |   | 235 |   | 0.21 |   |
| Less: U.S. tax equity net income (loss) (net of tax) |   | 38 |   | 0.04 |   | 44 |   | 0.04 |   |
| Non-operating benefit (cost) income (pre-tax) (GAAP) |   | 788 |   | 0.74 |   | 842 |   | 0.77 |   |
| Tax effect on non-operating benefit (cost) income |   | (166) |   | (0.15) |   | (177) |   | (0.16) |   |
| Less: Non-operating benefit (cost) income (net of tax) |   | 623 |   | 0.58 |   | 665 |   | 0.61 |   |

*(29 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0023`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| FREE CASH FLOW (FCF) (NON-GAAP) | 2025 | 2024 |
|---|---|---|
| Cash flows from operating activities (CFOA) (GAAP) | $8,543 | $5,817 |
| Add: gross additions to property, plant and equipment and internal-use software | (1,273) | (1,032) |
| Add: dispositions of property, plant and equipment | 123 | 114 |
| Less: separation cash expenditures | (245) | (800) |
| Less: Corporate & Other restructuring cash expenditures | (56) | (504) |
| Free cash flow (FCF) (Non-GAAP) | $7,694 | $6,203 |
| We believe investors may find it useful to compare free cash flow* performance without the effects of separation cash expenditures and Corporate & Other restructuring cash expenditures (associated with the separation-related program announced in the fourth quarter of 2022). In addition, beginning in the third quarter of 2025, we now include dispositions of property, plant and equipment. We believe this measure will better allow management and investors to evaluate the capacity of our operations to generate free cash flow*. We also use FCF* as a performance metric at the company level for our annual executive incentive plan and performance stock units granted in 2025. |   |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0024`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Period | Total number of shares purchased | Average price paid per share |   | Total number of shares purchased as part of our share repurchase authorization | Approximate dollar value of shares that may yet be purchased under our share repurchase authorization |   |
|---|---|---|---|---|---|---|
| (Shares in thousands) |   |   |   |   |   |   |
| 2025 |   |   |   |   |   |   |
| October | 306 |   | $313.34 | 306 |   |   |
| November | 5,389 | 316.09 |   | 5,389 |   |   |
| December | 710 | 291.98 |   | 710 |   |   |
| Total | 6,404 |   | $313.29 | 6,404 |   | $2,698 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0025`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| /s/ H. Lawrence Culp, Jr. | /s/ Rahul Ghai |
|---|---|
| H. Lawrence Culp, Jr. | Rahul Ghai |
| Chairman and Chief Executive Officer | Chief Financial Officer |
| January 29, 2026 |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0026`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**STATEMENT OF OPERATIONS**

| STATEMENT OF OPERATIONS |   |   |   |
|---|---|---|---|
| (In millions; per-share amounts in dollars) | 2025 | 2024 | 2023 |
| Sales of equipment | $12,159 | $10,274 | $9,318 |
| Sales of services | 30,163 | 24,847 | 22,641 |
| Insurance revenue (Note 12) | 3,533 | 3,581 | 3,389 |
| Total revenue | 45,855 | 38,702 | 35,348 |
| Cost of equipment sold | 12,382 | 10,341 | 9,900 |
| Cost of services sold | 16,586 | 13,967 | 13,039 |
| Selling, general and administrative expenses | 4,088 | 4,437 | 4,045 |
| Separation costs | 202 | 492 | 692 |
| Research and development | 1,580 | 1,286 | 1,011 |
| Interest and other financial charges | 843 | 986 | 1,029 |

*(31 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0027`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**STATEMENT OF FINANCIAL POSITION**

| STATEMENT OF FINANCIAL POSITION |   |   |
|---|---|---|
| December 31 (In millions) | 2025 | 2024 |
| Cash, cash equivalents and restricted cash | $12,392 | $13,619 |
| Investment securities (Note 3) | — | 982 |
| Current receivables (Note 4) | 11,773 | 9,327 |
| Inventories, including deferred inventory costs (Note 5) | 11,868 | 9,763 |
| Current contract assets (Note 8) | 3,511 | 2,982 |
| All other current assets (Note 9) | 1,052 | 962 |
| Current assets | 40,596 | 37,635 |
| Investment securities (Note 3) | 38,788 | 37,741 |
| Property, plant and equipment – net (Note 6) | 7,987 | 7,277 |
| Goodwill (Note 7) | 9,060 | 8,538 |

*(29 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0028`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 6 units

**STATEMENT OF CASH FLOWS**

| STATEMENT OF CASH FLOWS |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Net income (loss) | $8,698 | $6,566 | $9,445 |
| Net (income) loss from discontinued operations activities | (103) | 91 | 3 |
| Adjustments to reconcile net income (loss) to cash from (used for) operating activities: |   |   |   |
| Depreciation and amortization of property, plant and equipment (Note 6) | 863 | 834 | 797 |
| Amortization of intangible assets (Note 7) | 357 | 350 | 382 |
| Goodwill impairments (Note 7) | — | 251 | — |
| (Gains) losses on equity securities (Note 19) | (508) | (719) | (5,846) |
| Principal pension plans (benefit) cost (Note 13) | (655) | (653) | (755) |
| Principal pension plans employer contributions | (211) | (210) | (184) |
| Other postretirement benefit plans (net) | (230) | (299) | (348) |

*(42 further rows in the stored grid.)*

Related units: `u-src-ge-10k-fy2025-a73b722f-0113`, `u-src-ge-10k-fy2025-a73b722f-0113`, `u-src-ge-10k-fy2025-a73b722f-0113`, `u-src-ge-10k-fy2025-a73b722f-0114`, `u-src-ge-10k-fy2025-a73b722f-0114`, `u-src-ge-10k-fy2025-a73b722f-0114`

#### `tbl-src-ge-10k-fy2025-a73b722f-0029`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**STATEMENT OF COMPREHENSIVE INCOME (LOSS)**

| STATEMENT OF COMPREHENSIVE INCOME (LOSS) |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Net income (loss) | $8,698 | $6,566 | $9,445 |
| Less: net income (loss) attributable to noncontrolling interests | (6) | 11 | (37) |
| Net income (loss) attributable to the Company | $8,704 | $6,556 | $9,482 |
| Currency translation adjustments | (43) | 2,131 | 2,274 |
| Benefit plans | (882) | (1,128) | (4,747) |
| Investment securities and cash flow hedges | 749 | (1,016) | 968 |
| Long-duration insurance contracts | (761) | 2,284 | (2,371) |
| L Less: other comprehensive income (loss) attributable to noncontrolling interests | — | (17) | 2 |
| Other comprehensive income (loss) attributable to the Company | $(937) | $2,289 | $(3,878) |
| Comprehensive income (loss) | $7,761 | $8,838 | $5,569 |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0030`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**STATEMENT OF CHANGES IN SHAREHOLDERS' EQUITY**

| STATEMENT OF CHANGES IN SHAREHOLDERS' EQUITY |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Common stock issued | $15 | $15 | $15 |
| Beginning balance | (3,861) | (6,150) | (2,272) |
| Currency translation adjustments | (43) | 2,151 | 2,270 |
| Benefit plans | (882) | (1,120) | (4,745) |
| Investment securities and cash flow hedges | 749 | (1,026) | 968 |
| Long-duration insurance contracts | (761) | 2,284 | (2,371) |
| Accumulated other comprehensive income (loss) | $(4,798) | $(3,861) | $(6,150) |
| Beginning balance | 24,266 | 26,962 | 34,173 |
| Gains (losses) on treasury stock dispositions | (1,048) | (3,028) | (1,845) |
| Stock-based compensation | 371 | 361 | 355 |

*(14 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0031`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| RESULTS OF DISCONTINUED OPERATIONSFor the year ended December 31, 2025 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $— | $— | $— |
| Cost of equipment and services sold | — | — | — |
| Other income, costs and expenses | — | (47) | (47) |
| Net Income (loss) of discontinued operations before income taxes | — | (47) | (47) |
| Benefit (provision) for income taxes | 125 | 9 | 134 |
| Net Income (loss) of discontinued operations, net of taxes | 125 | (38) | 87 |
| Gain (loss) on disposal before income taxes | — | 16 | 16 |
| Benefit (provision) for income taxes | — | — | — |
| Gain (loss) on disposal, net of taxes | — | 16 | 16 |
| Net Income (loss) from discontinued operations, net of taxes | $125 | $(22) | $103 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0032`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| For the year ended December 31, 2024 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $7,244 | $— | $7,244 |
| Cost of equipment and services sold | (6,074) | — | (6,074) |
| Other income, costs and expenses | (1,299) | (21) | (1,320) |
| Net Income (loss) of discontinued operations before income taxes | (129) | (21) | (150) |
| Benefit (provision) for income taxes | 27 | 13 | 40 |
| Net Income (loss) of discontinued operations, net of taxes | (102) | (8) | (110) |
| Gain (loss) on disposal before income taxes | — | 21 | 21 |
| Benefit (provision) for income taxes | — | (1) | (1) |
| Gain (loss) on disposal, net of taxes | — | 19 | 19 |
| Net Income (loss) from discontinued operations, net of taxes | $(102) | $12 | $(91) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0033`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| For the year ended December 31, 2023 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $33,265 | $— | $33,265 |
| Cost of equipment and services sold | (28,205) | — | (28,205) |
| Other income, costs and expenses | (5,306) | (1,301) | (6,607) |
| Net Income (loss) of discontinued operations before income taxes | (246) | (1,301) | (1,547) |
| Benefit (provision) for income taxes(a) | (171) | 1,710 | 1,539 |
| Net Income (loss) of discontinued operations, net of taxes | (417) | 409 | (8) |
| Gain (loss) on disposal before income taxes | — | 6 | 6 |
| Benefit (provision) for income taxes | — | — | — |
| Gain (loss) on disposal, net of taxes | — | 6 | 6 |
| Net Income (loss) from discontinued operations, net of taxes | $(417) | $414 | $(3) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0034`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ASSETS AND LIABILITIES OF DISCONTINUED OPERATIONS | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Cash, cash equivalents and restricted cash(a) | $1,126 | $1,327 |
| Current receivables | 35 | 13 |
| Property, plant, and equipment - net | 26 | 40 |
| All other assets | 648 | 438 |
| Deferred income taxes | 21 | 24 |
| Assets of discontinued operations(b) | $1,855 | $1,841 |
| Accounts payable | $35 | $30 |
| Non-current compensation and benefits | 32 | 33 |
| All other liabilities | 1,347 | 1,254 |
| Liabilities of discontinued operations(b) | $1,413 | $1,317 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0035`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | December 31, 2025 |   |   |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Amortizedcost |   | Grossunrealizedgains |   | Grossunrealizedlosses |   | Estimatedfair value |   | Amortizedcost |   | Grossunrealizedgains |   | Grossunrealizedlosses |   | Estimatedfair value |   |
| Debt |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| U.S. corporate |   | $27,658 |   | $825 |   | $(1,969) |   | $26,513 |   | $28,456 |   | $546 |   | $(2,309) |   | $26,692 |
| Non-U.S. corporate | 2,909 |   | 41 |   | (242) |   | 2,707 |   | 2,970 |   | 23 |   | (302) |   | 2,691 |   |
| State and municipal | 2,751 |   | 46 |   | (192) |   | 2,605 |   | 2,409 |   | 22 |   | (235) |   | 2,196 |   |
| Mortgage and asset-backed | 5,202 |   | 69 |   | (121) |   | 5,151 |   | 5,007 |   | 47 |   | (183) |   | 4,870 |   |
| Government and agencies | 1,015 |   | 4 |   | (95) |   | 924 |   | 1,180 |   | 4 |   | (118) |   | 1,066 |   |
| Equity | 887 |   | — |   | — |   | 887 |   | 225 |   | — |   | — |   | 225 |   |
| Non-current investment securities |   | $40,422 |   | $985 |   | $(2,619) |   | $38,788 |   | $40,248 |   | $641 |   | $(3,148) |   | $37,741 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0036`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| For the years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Net unrealized gains (losses) for equity securities with readily determinable fair value (RDFV) | $313 | $320 | $6,413 |
| Proceeds from debt/equity securities sales and redemptions | 4,922 | 9,099 | 12,595 |
| Gross realized gains on debt securities | 35 | 75 | 52 |
| Gross realized losses and impairments on debt securities | (76) | (66) | (66) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0037`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| For the years ended December 31 | 2025 | 2024 |
|---|---|---|
| Purchases of investment securities | $(4,050) | $(7,132) |
| Dispositions and maturities of investment securities | 4,475 | 6,168 |
| Net (purchases) dispositions of insurance investment securities | $425 | $(963) |

#### `tbl-src-ge-10k-fy2025-a73b722f-0038`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Amortized cost |   | Estimated fair value |   |
|---|---|---|---|---|
| Within one year |   | $843 |   | $847 |
| After one year through five years | 3,460 |   | 3,561 |   |
| After five years through ten years | 5,269 |   | 5,498 |   |
| After ten years | 24,762 |   | 22,845 |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0039`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**CURRENT RECEIVABLES**

| CURRENT RECEIVABLES |   |   |
|---|---|---|
| December 31 | 2025 | 2024 |
| Customer receivables | $9,269 | $7,385 |
| Revenue sharing and other partner receivables(a) | 1,322 | 1,113 |
| Non-income based tax receivables | 165 | 128 |
| Supplier advances | 867 | 546 |
| Receivables from disposed businesses | 34 | 99 |
| Other sundry receivables | 209 | 162 |
| Allowance for credit losses | (94) | (106) |
| Total current receivables | $11,773 | $9,327 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0040`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**LONG-TERM RECEIVABLES**

| LONG-TERM RECEIVABLES |   |   |
|---|---|---|
| December 31 | 2025 | 2024 |
| Long-term customer receivables | $173 | $122 |
| Supplier advances | 94 | 50 |
| Sundry receivables | 105 | 106 |
| Allowance for credit losses | (96) | (85) |
| Total long-term receivables | $276 | $194 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0041`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31 | 2025 | 2024 |
|---|---|---|
| Raw materials and work in process | $9,354 | $7,372 |
| Finished goods | 1,542 | 1,459 |
| Deferred inventory costs(a) | 972 | 932 |
| Inventories, including deferred inventory costs | $11,868 | $9,763 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0042`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Depreciable lives | Original Cost |   |   |   | Net Carrying Value |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|
| December 31 | (in years) | 2025 |   | 2024 |   |   | 2025 |   | 2024 |   |
| Land and improvements | 8 |   | $139 |   | $131 |   |   | $137 |   | $129 |
| Buildings, structures and related equipment | 8 - 40 | 3,295 |   | 3,146 |   |   | 1,411 |   | 1,369 |   |
| Machinery and equipment | 4 - 20 | 12,757 |   | 11,533 |   |   | 4,432 |   | 3,851 |   |
| Leasehold costs and manufacturing plant under construction | 1 - 10 | 1,197 |   | 1,084 |   |   | 989 |   | 872 |   |
| ROU operating lease assets |   |   |   |   |   |   | 1,018 |   | 1,057 |   |
| Property, plant and equipment - net |   |   | $17,388 |   | $15,894 |   |   | $7,987 |   | $7,277 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0043`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Property, plant andequipment additions |   |   |   |   |   | Depreciation and amortization |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| December 31 | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $498 |   | $431 |   | $343 |   | $402 |   | $370 |   | $356 |
| Defense & Propulsion Technologies | 184 |   | 135 |   | 145 |   | 153 |   | 150 |   | 147 |   |
| Corporate and Other(a) | 471 |   | 353 |   | 278 |   | 307 |   | 314 |   | 294 |   |
| Total |   | $1,153 |   | $920 |   | $766 |   | $863 |   | $834 |   | $797 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0044`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| OPERATING LEASE EXPENSE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Long-term (fixed) | $309 | $326 | $364 |
| Long-term (variable) | 30 | 111 | 26 |
| Short-term | 47 | 45 | 115 |
| Total operating lease expense | $385 | $482 | $506 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0045`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| MATURITY OF LEASE LIABILITIES | 2026 |   | 2027 |   | 2028 |   | 2029 |   | 2030 |   | Thereafter |   | Total |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Undiscounted lease payments |   | $278 |   | $221 |   | $176 |   | $154 |   | $117 |   | $377 |   | $1,323 |
| Less: imputed interest |   |   |   |   |   |   |   |   |   |   |   |   | (260) |   |
| Total lease liability as of December 31, 2025 |   |   |   |   |   |   |   |   |   |   |   |   |   | $1,063 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0046`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| SUPPLEMENTAL INFORMATION RELATED TO OPERATING LEASES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Operating cash flows used for operating leases | $329 | $352 | $427 |
| Right-of-use assets obtained in exchange for new lease liabilities | 238 | 196 | 275 |
| Weighted-average remaining lease term | 7.6 years | 7.8 years | 7.7 years |
| Weighted-average discount rate | 4.7% | 4.6% | 4.5% |

#### `tbl-src-ge-10k-fy2025-a73b722f-0047`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Commercial Engines & Services |   | Defense & Propulsion Technologies |   | Total |   |
|---|---|---|---|---|---|---|
| Balance at December 31, 2023 |   | $6,472 |   | $2,476 |   | $8,948 |
| Goodwill impairment | — |   | (251) |   | (251) |   |
| Goodwill adjustments(a) | (131) |   | (28) |   | (159) |   |
| Balance at December 31, 2024 |   | $6,341 |   | $2,197 |   | $8,538 |
| Goodwill acquisition | — |   | 148 |   | 148 |   |
| Goodwill adjustments(a) | 303 |   | 72 |   | 374 |   |
| Balance at December 31, 2025 |   | $6,644 |   | $2,417 |   | $9,060 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0048`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   |   | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INTANGIBLE ASSETS SUBJECT TO AMORTIZATION December 31 | Useful lives (in years) | Gross carryingamount |   | Accumulatedamortization |   | Net |   | Gross carryingamount |   | Accumulatedamortization |   | Net |   |
| Customer-related(a) | 5-20 |   | $3,992 |   | $(2,313) |   | $1,679 |   | $3,850 |   | $(2,083) |   | $1,767 |
| Patents and technology | 5-15 | 2,946 |   | (916) |   | 2,031 |   | 2,744 |   | (759) |   | 1,985 |   |
| Capitalized software | 5-10 | 1,366 |   | (859) |   | 507 |   | 1,296 |   | (803) |   | 493 |   |
| Trademarks & other | 13 | 77 |   | (67) |   | 9 |   | 70 |   | (58) |   | 13 |   |
| Total |   |   | $8,380 |   | $(4,155) |   | $4,225 |   | $7,960 |   | $(3,703) |   | $4,257 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0049`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ESTIMATED 5 YEAR CONSOLIDATED AMORTIZATION | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| Estimated annual pre-tax amortization | 351 | 356 | 357 | 376 | 371 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0050`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| CONTRACT ASSETS, LIABILITIES AND OTHER DEFERRED ASSETS AND INCOME | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Long-term service agreements | $2,792 | $2,374 |
| Equipment and other service agreements | 719 | 609 |
| Current contract assets | $3,511 | $2,982 |
| Nonrecurring engineering costs(a) | $2,423 | $2,438 |
| Customer advances and other(b) | 2,497 | 2,393 |
| Contract and other deferred assets | 4,920 | 4,831 |
| Total contract and other deferred assets | $8,431 | $7,814 |
| Long-term service agreement liabilities | $10,016 | $8,994 |
| Current deferred income | 317 | 359 |
| Contract liabilities and current deferred income | $10,333 | $9,353 |
| Non-current deferred income | 1,065 | 1,013 |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0051`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31 |   | 2025 |   |   | 2024 |   |   |
|---|---|---|---|---|---|---|---|
|   | Maturities | Amount |   | Average Rate | Amount |   | Average Rate |
| Current portion of long-term borrowings |   |   |   |   |   |   |   |
| Senior notes | 2026 |   | $1,504 | 4.00% | $1,952 |   | 4.03% |
| Subordinated notes and other | 2026 | 157 |   |   | 87 |   |   |
| Other short-term |   | 25 |   |   | — |   |   |
| Total short-term borrowings |   |   | $1,686 |   |   | $2,039 |   |
|   | Maturities | Amount |   | Average Rate | Amount |   | Average Rate |
| Senior notes(a) | 2027 - 2050 |   | $16,773 | 4.00% |   | $15,467 | 4.03% |
| Subordinated notes | 2035 - 2037 | 1,456 |   | 4.40% | 1,330 |   | 4.43% |
| Other |   | 580 |   |   | 437 |   |   |
| Total long-term borrowings |   |   | $18,808 |   |   | $17,234 |   |

*(1 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0052`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2026 |   | 2027 | 2028 | 2029 | 2030 | Thereafter | Total |
|---|---|---|---|---|---|---|---|---|
| Long-term debt maturities | 1,661 | (a) | 1,693 | 480 | 1,639 | 1,700 | 13,296 | 20,469 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0053`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31 | 2025 | 2024 |
|---|---|---|
| Trade payables | $5,734 | $4,565 |
| Supply chain finance programs | 1,247 | 1,259 |
| Revenue sharing and other partner payables(a) | 2,553 | 1,689 |
| Sundry payables | 544 | 397 |
| Accounts payable | $10,078 | $7,909 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0054`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31, 2025 | Long-term care | Structured settlement annuities | Life | Other contracts | Total |
|---|---|---|---|---|---|
| Future policy benefit reserves | $25,792 | $8,383 | $906 | $357 | $35,438 |
| Investment contracts | — | 647 | — | 493 | 1,140 |
| Other | — | — | 113 | 203 | 316 |
| Total | $25,792 | $9,031 | $1,019 | $1,053 | $36,894 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0055`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|
| Future policy benefit reserves | $24,675 | $8,426 | $1,018 | $357 | $34,476 |
| Investment contracts | — | 719 | — | 621 | 1,340 |
| Other | — | — | 116 | 277 | 394 |
| Total | $24,675 | $9,145 | $1,134 | $1,254 | $36,209 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0056`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | December 31, 2025 |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Present value of expected net premiums | Long-term care |   | Structured settlement annuities |   | Life |   | Long-term care |   | Structured settlement annuities |   | Life |   |
| Balance, beginning of year |   | $4,144 |   | $— |   | $4,318 |   | $4,063 |   | $— |   | $4,803 |
| Beginning balance at locked-in discount rate | 3,991 |   | — |   | 4,415 |   | 3,745 |   | — |   | 4,773 |   |
| Effect of changes in cash flow assumptions | 355 |   | — |   | 4 |   | 465 |   | — |   | (1) |   |
| Effect of actual variances from expected experience(a) | (19) |   | — |   | (2,681) |   | (26) |   | — |   | 8 |   |
| Adjusted beginning of year balance | 4,327 |   | — |   | 1,738 |   | 4,184 |   | — |   | 4,780 |   |
| Interest accrual | 221 |   | — |   | 164 |   | 209 |   | — |   | 177 |   |
| Net premiums collected | (408) |   | — |   | (292) |   | (403) |   | — |   | (309) |   |
| Effect of foreign currency | — |   | — |   | 103 |   | — |   | — |   | (234) |   |
| Ending balance at locked-in discount rate | 4,140 |   | — |   | 1,714 |   | 3,991 |   | — |   | 4,415 |   |
| Effect of changes in discount rate assumptions | 287 |   | — |   | 119 |   | 154 |   | — |   | (97) |   |

*(24 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0057`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**DESCRIPTION OF OUR PLANS**

| DESCRIPTION OF OUR PLANS |   |   |   |   |
|---|---|---|---|---|
| Plan Category |   | Participants | Funding | Comments |
| Principal Pension Plans | GE Aerospace Pension Plan | Covers U.S. GE Aerospace participants: ~79,000 retirees and beneficiaries, ~33,000 vested former employees and ~9,000 active employees | Our funding policy is to contribute amounts sufficient to meet minimum funding requirements under employee benefit and tax laws. We may decide to contribute additional amounts beyond this level. | Closed to new participants since 2012. Benefits for employees with salaried benefits were frozen effective January 1, 2021, and thereafter these employees receive increased company contributions in the company sponsored defined contribution plan in lieu of participation in a defined benefit plan (announced October 2019). |
|   | GE Aerospace Supplementary Pension Plan | Provides supplementary benefits to higher-level, longer-service U.S. employees | Unfunded. We pay benefits on a pay-as-you-go basis from company cash. | The annuity benefit has been closed to new participants since 2011 and has been replaced by an installment benefit (which was closed to new executives after 2020). Benefits for employees who became executives before 2011 were frozen effective January 1, 2021, and thereafter these employees accrue the installment benefit. |
| Other Pension Plans(a) | 6 U.S. and non-U.S. pension plans with pension assets or obligations that have reached $50 million | Covers ~11,100 retirees and beneficiaries, ~10,300 vested former employees and ~800 active employees | Our funding policy is to contribute amounts sufficient to meet minimum funding requirements under employee benefit and tax laws in each country. We may decide to contribute additional amounts beyond this level. We pay benefits for some plans from company cash. | In certain countries, benefit accruals have ceased and/or have been closed to new hires as of various dates. |
| Principal Retiree Benefit Plans | Provides health and life insurance benefits to certain eligible participants | Covers U.S. GE Aerospace participants: ~40,000 retirees and dependents and ~10,000 active employees | We fund retiree benefit plans on a pay-as-you-go basis and the retiree benefit insurance trust at our discretion. | Participants share in the cost of the healthcare benefits. |

#### `tbl-src-ge-10k-fy2025-a73b722f-0058`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| FUNDING STATUS BY PLAN TYPE | Benefit Obligation |   |   |   | Fair Value of Assets |   |   |   | Deficit/(Surplus) |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Principal Pension Plans: |   |   |   |   |   |   |   |   |   |   |   |   |
| GE Aerospace Pension Plan (subject to regulatory funding) |   | $21,053 |   | $21,010 |   | $19,216 |   | $19,020 |   | $1,837 |   | $1,990 |
| GE Aerospace Supplementary Pension Plan | 2,872 |   | 2,814 |   | — |   | — |   | 2,872 |   | 2,814 |   |
|   | 23,925 |   | 23,824 |   | 19,216 |   | 19,020 |   | 4,709 |   | 4,804 |   |
| Other Pension Plans: |   |   |   |   |   |   |   |   |   |   |   |   |
| Subject to regulatory funding | 3,027 |   | 2,736 |   | 3,831 |   | 3,592 |   | (804) |   | (856) |   |
| Not subject to regulatory funding | 397 |   | 404 |   | — |   | — |   | 397 |   | 404 |   |
| Principal retiree benefit plans for GE Aerospace (not subject to regulatory funding) | 1,135 |   | 1,202 |   | 5 |   | 6 |   | 1,130 |   | 1,196 |   |
| Total plans subject to regulatory funding | 24,080 |   | 23,746 |   | 23,047 |   | 22,612 |   | 1,033 |   | 1,134 |   |
| Total plans not subject to regulatory funding | 4,404 |   | 4,420 |   | 5 |   | 6 |   | 4,399 |   | 4,414 |   |

*(1 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0059`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| COST OF OUR BENEFITS PLANS AND ASSUMPTIONS | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Components of expense (income) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Service cost - operating |   | $59 |   | $2 |   | $13 |   | $71 |   | $22 |   | $13 |   | $94 |   | $37 |   | $17 |
| Interest cost | 1,301 |   | 173 |   | 62 |   | 1,401 |   | 227 |   | 71 |   | 1,892 |   | 422 |   | 111 |   |
| Expected return on plan assets | (1,500) |   | (207) |   | — |   | (1,751) |   | (310) |   | — |   | (2,376) |   | (587) |   | — |   |
| Amortization of net loss (gain) | (506) |   | 30 |   | (60) |   | (468) |   | 41 |   | (82) |   | (723) |   | 20 |   | (124) |   |
| Amortization of prior service cost (credit) | (9) |   | — |   | (81) |   | 6 |   | (1) |   | (103) |   | 5 |   | (4) |   | (148) |   |
| Curtailment / settlement loss (gain) | — |   |   |   | — |   | — |   |   |   | — |   | — |   | (6) |   | — |   |
| Non-operating |   | $(714) |   | $(4) |   | $(79) |   | $(812) |   | $(43) |   | $(114) |   | $(1,202) |   | $(155) |   | $(161) |
| Net periodic expense (income) |   | $(655) |   | $(2) |   | $(66) |   | $(741) |   | $(21) |   | $(101) |   | $(1,108) |   | $(118) |   | $(144) |
| Less: discontinued operations | — |   | — |   | — |   | (88) |   | (12) |   | (15) |   | (377) |   | (78) |   | (57) |   |

*(8 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0060`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 3 units

**PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME)**

| PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   |   |   |   |   |   |   | 2024 |   |   |   |   |   |
|   | Principal pension |   |   | Other pension |   | Principal retiree benefit |   |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Change in benefit obligations |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Balance at January 1 |   | $23,824 |   |   | $3,140 |   | $1,202 |   |   | $36,217 |   | $10,377 |   | $2,055 |
| Service cost | 59 |   |   | 2 |   | 13 |   |   | 71 |   | 22 |   | 13 |   |
| Interest cost | 1,301 |   |   | 173 |   | 62 |   |   | 1,401 |   | 227 |   | 71 |   |
| Participant contributions | 7 |   |   | — |   | 18 |   |   | 8 |   | 4 |   | 21 |   |
| Plan amendments | 36 |   |   | 135 |   | (5) |   |   | — |   | — |   | — |   |
| Actuarial loss (gain) - net (a) | 472 |   |   | (4) |   | (12) |   |   | (1,049) |   | (435) |   | (15) |   |
| Benefits paid | (1,774) |   |   | (185) |   | (143) |   |   | (1,957) |   | (305) |   | (192) |   |
| Dispositions/acquisitions/other - net | — |   |   | (24) |   | — |   |   | (10,867) |   | (6,548) |   | (751) |   |

*(22 further rows in the stored grid.)*

Related units: `u-src-ge-10k-fy2025-a73b722f-0116`, `u-src-ge-10k-fy2025-a73b722f-0116`, `u-src-ge-10k-fy2025-a73b722f-0116`

#### `tbl-src-ge-10k-fy2025-a73b722f-0061`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Level 1 |   |   |   | Level 2 |   |   |   | Level 3 |   |   |   | Assets measured at NAV |   |   |   | Total |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Asset Category |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Global equity |   | $1,200 |   | $1,156 |   | $230 |   | $203 |   |   |   |   |   | $2,410 |   | $1,912 |   | $3,840 |   | $3,271 |
| Fixed income and cash investment funds | 952 |   | 1,299 |   | 1,617 |   | 1,448 |   |   |   |   |   |   |   |   |   | 2,569 |   | 2,747 |   |
| U.S. corporate(a) |   |   |   |   | 2,496 |   | 3,125 |   |   |   |   |   |   |   |   |   | 2,496 |   | 3,125 |   |
| Other debt securities(b) |   |   |   |   | 2,957 |   | 3,152 |   |   |   |   |   | 2,263 |   | 1,851 |   | 5,220 |   | 5,003 |   |
| Real estate |   |   |   |   |   |   |   |   | 449 |   | 541 |   | 934 |   | 995 |   | 1,383 |   | 1,536 |   |
| Private equities and other investments |   |   |   |   |   |   |   |   | 246 |   | 312 |   | 7,079 |   | 6,385 |   | 7,325 |   | 6,697 |   |
| Derivatives, net(c) | (67) |   | (139) |   | 12 |   | 20 |   |   |   |   |   |   |   |   |   | (55) |   | (119) |   |
| Cash |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 284 |   | 297 |   |
| Payables |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | (400) |   | (440) |   |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0062`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ASSET ALLOCATION OF PENSION PLANS | 2025 Target allocation |   | 2025 Actual allocation |   |
|---|---|---|---|---|
|   | Principal Pension | Other Pension (weighted average) | Principal Pension | Other Pension (weighted average) |
| Global equities | 10.0 - 30.0% | 14% | 18% | 12% |
| Debt securities (including cash equivalents) | 19.0 - 87.5 | 65 | 41 | 65 |
| Real estate | 1.0 - 10.0 | 6 | 6 | 7 |
| Private equities & other investments | 12.0 - 44.0 | 15 | 35 | 16 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0063`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| EXPECTED FUTURE BENEFIT PAYMENTS OF OUR BENEFIT PLANS(a) | Principal pension | Other pension | Principal retiree benefit |
|---|---|---|---|
| 2026 | $1,815 | $190 | $120 |
| 2027 | 1,820 | 190 | 115 |
| 2028 | 1,825 | 200 | 115 |
| 2029 | 1,825 | 205 | 110 |
| 2030 | 1,820 | 210 | 110 |
| 2031-2035 | 8,825 | 1,115 | 465 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0064`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**COST OF POSTRETIREMENT BENEFIT PLANS AND CHANGES IN OTHER COMPREHENSIVE INCOME**

| COST OF POSTRETIREMENT BENEFIT PLANS AND CHANGES IN OTHER COMPREHENSIVE INCOME |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| For the years ended December 31 | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
| (Pre-tax) | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Cost (income) of postretirement benefit plans |   | $(655) |   | $(2) |   | $(66) |   | $(741) |   | $(21) |   | $(101) |   | $(1,108) |   | $(118) |   | $(144) |
| Changes in other comprehensive loss (income) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Prior service cost (credit) - current year | 36 |   | 135 |   | (5) |   | — |   | — |   | — |   | 49 |   | — |   | — |   |
| Net loss (gain) - current year (a) | 221 |   | 132 |   | (11) |   | 262 |   | (52) |   | (15) |   | 1,588 |   | 721 |   | (5) |   |
| Reclassifications out of AOCI |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Curtailment/settlement gain (loss) | — |   | — |   | — |   | — |   | — |   | — |   | — |   | 6 |   | — |   |
| Dispositions | — |   | — |   | — |   | 185 |   | (761) |   | 715 |   | 1,989 |   | (792) |   | 1,216 |   |
| Amortization of net gain (loss) | 506 |   | (30) |   | 60 |   | 468 |   | (41) |   | 82 |   | 723 |   | (20) |   | 124 |   |
| Amortization of prior service credit (cost) | 9 |   | — |   | 81 |   | (6) |   | 1 |   | 103 |   | (5) |   | 4 |   | 148 |   |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0065`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| U.S. income (loss) | $6,659 | $4,809 | $7,195 |
| Non-U.S. income (loss) | 3,341 | 2,811 | 3,246 |
| Total | $10,000 | $7,620 | $10,441 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0066`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| INCOME TAX PAYMENTS | 2025 |
|---|---|
| U.S. Federal(a) | $150 |
| U.S. State(a) | 7 |
| Non-U.S: |   |
| Singapore | 178 |
| United Kingdom | 78 |
| Ireland | 60 |
| Hungary | 52 |
| Italy | 46 |
| India | 36 |
| Other Non-U.S. | 132 |
| Total income taxes paid (received), continuing operations | $739 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0067`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| PROVISION (BENEFIT) FOR INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Current |   |   |   |
| U.S. Federal | $671 | $310 | $(588) |
| Non-U.S. | 709 | 423 | 314 |
| U.S. State | (72) | 48 | 134 |
| Deferred |   |   |   |
| U.S. Federal | (35) | 250 | 622 |
| Non-U.S. | 32 | 59 | 453 |
| U.S. State | 100 | (128) | 59 |
| Total | $1,405 | $962 | $994 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0068`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · cited by 3 units

| RECONCILIATION OF U.S. FEDERAL STATUTORY INCOME TAX RATE TO EFFECTIVE INCOME TAX RATE | 2025 |   |   |
|---|---|---|---|
|   | Amount |   | Rate |
| U.S. federal statutory income tax rate |   | $2,100 | 21.0% |
| State and local income taxes, net of federal income tax effect(a) | 74 |   | 0.7% |
| Foreign tax effects: |   |   |   |
| Singapore |   |   |   |
| Statutory rate difference between foreign and U.S. | (70) |   | (0.7)% |
| Local taxes at a rate different than the statutory rate(b) | (37) |   | (0.4)% |
| Other | 53 |   | 0.5% |
| Other foreign jurisdictions | 68 |   | 0.7% |
| Effect of cross-border tax laws |   |   |   |
| Foreign-derived intangible income | (338) |   | (3.4)% |

*(9 further rows in the stored grid.)*

Related units: `u-src-ge-10k-fy2025-a73b722f-0115`, `u-src-ge-10k-fy2025-a73b722f-0115`, `u-src-ge-10k-fy2025-a73b722f-0115`

#### `tbl-src-ge-10k-fy2025-a73b722f-0069`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| RECONCILIATION OF U.S. FEDERAL STATUTORY INCOME TAX RATE TO EFFECTIVE INCOME TAX RATE | 2024 |   |   |   | 2023 |   |   |   |
|---|---|---|---|---|---|---|---|---|
|   |   | Amount |   | Rate |   | Amount |   | Rate |
| U.S. federal statutory income tax rate |   |   | $1,600 | 21.0% |   |   | $2,193 | 21.0% |
| State Taxes, net of federal benefit |   | 123 |   | 1.6 |   | 152 |   | 1.5 |
| Tax on global activities including exports(a) |   | (92) |   | (1.2) |   | 78 |   | 0.7 |
| U.S. business credits(b) |   | (242) |   | (3.2) |   | (254) |   | (2.4) |
| Retained and sold ownership interests |   | (110) |   | (1.4) |   | (1,215) |   | (11.6) |
| All other – net(c) |   | (317) |   | (4.2) |   | 40 |   | 0.3 |
|   |   | (638) |   | (8.4) |   | (1,199) |   | (11.5) |
| Effective income tax rate |   |   | $962 | 12.6% |   |   | $994 | 9.5% |

#### `tbl-src-ge-10k-fy2025-a73b722f-0070`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| UNRECOGNIZED TAX BENEFITS December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Unrecognized tax benefits | $3,056 | $2,824 | $3,399 |
| Portion that, if recognized, would reduce tax expense and effective tax rate(a) | 2,381 | 2,110 | 2,708 |
| Accrued interest on unrecognized tax benefits | 656 | 609 | 635 |
| Accrued penalties on unrecognized tax benefits | 11 | 14 | 111 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0071`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| UNRECOGNIZED TAX BENEFITS RECONCILIATION | 2025 | 2024 | 2023 |
|---|---|---|---|
| Balance at January 1 | $2,824 | $3,399 | $3,951 |
| Additions for tax positions of the current year | 347 | 68 | 109 |
| Additions for tax positions of prior years | 93 | 77 | 156 |
| Reductions for tax positions of prior years(a) | (168) | (649) | (710) |
| Settlements with tax authorities | (30) | (14) | (56) |
| Expiration of the statute of limitations | (10) | (57) | (51) |
| Balance at December 31 | $3,056 | $2,824 | $3,399 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0072`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| DEFERRED INCOME TAXES December 31 | 2025 | 2024 |
|---|---|---|
| Total assets | $7,883 | $7,479 |
| Total liabilities | (424) | (368) |
| Net deferred income tax asset (liability) | $7,459 | $7,111 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0073`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| COMPONENTS OF THE NET DEFERRED INCOME TAX ASSET (LIABILITY) December 31 | 2025 | 2024 |
|---|---|---|
| Deferred tax assets |   |   |
| Insurance company loss reserves | $2,398 | $2,349 |
| Progress collections, Contract assets, Contract liabilities and deferred items | 1,764 | 1,435 |
| Accrued expenses and reserves | 1,278 | 1,231 |
| Deferred expenses | 1,231 | 1,398 |
| Other compensation and benefits | 580 | 510 |
| Principal pension plans | 989 | 1,009 |
| Non-U.S. loss carryforwards(a) | 2,133 | 1,891 |
| Capital losses carryforward | 881 | 849 |
| State deferred tax assets(b) | 684 | 762 |
| Other | 1,522 | 1,514 |

*(10 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0074`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**DEFERRED TAX ASSETS VALUATION ALLOWANCE**

| DEFERRED TAX ASSETS VALUATION ALLOWANCE |   |
|---|---|
| Balance at December 31, 2022 | $(5,164) |
| Additions charged to income tax expense | — |
| Reductions credited to income tax expense | 102 |
| Other adjustments(a) | 1,646 |
| Balance at December 31, 2023 | $(3,416) |
| Additions charged to income tax expense | (2) |
| Reductions credited to income tax expense | 184 |
| Other adjustments | 18 |
| Balance at December 31, 2024 | $(3,216) |
| Additions charged to income tax expense | (2) |
| Reductions credited to income tax expense | 71 |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0075`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| ACCUMULATED OTHER COMPREHENSIVE INCOME (LOSS) (Dividends per share in dollars) | 2025 | 2024 | 2023 |
|---|---|---|---|
| Beginning balance | $(1,472) | $(3,623) | $(5,893) |
| AOCI before reclasses – net of taxes of $(157), $5 and $74 | (43) | 36 | 12 |
| Reclasses from AOCI – net of taxes of $—, $103 and $(626)(a) | — | 2,093 | 2,262 |
| AOCI | (43) | 2,129 | 2,274 |
| Less AOCI attributable to noncontrolling interests | — | (22) | 4 |
| Currency translation adjustments AOCI | $(1,515) | $(1,472) | $(3,623) |
| Beginning balance | $665 | $1,786 | $6,531 |
| AOCI before reclasses – net of taxes of $(117), $22 and $(497) | (393) | (8) | (1,874) |
| Reclasses from AOCI – net of taxes of $(137), $(269) and $(778)(a) | (489) | (1,119) | (2,873) |
| AOCI | (882) | (1,127) | (4,747) |
| Less AOCI attributable to noncontrolling interests | — | (7) | (2) |

*(13 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0076`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| WEIGHTED AVERAGE GRANT DATE FAIR VALUE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Stock options | $79.55 | $65.16 | $36.10 |
| RSUs | 212.45 | 160.70 | 89.6 |
| PSUs | 221.46 | 150.05 | 89.44 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0077`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| STOCK-BASED COMPENSATION ACTIVITY | Stock options |   |   |   |   |   | RSUs |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Shares (in thousands) | Weighted average exercise price |   | Weighted average contractual term (in years) | Intrinsic value (in millions) |   | Shares (in thousands) | Weighted average grant date fair value |   | Weighted average contractual term (in years) | Intrinsic value (in millions) |   |
| Outstanding at January 1, 2025 | 10,917 |   | $91.78 |   |   |   | 3,607 |   | $103.70 |   |   |   |
| Granted | 569 | 202.16 |   |   |   |   | 380 | 212.45 |   |   |   |   |
| Exercised | (4,102) | 104.40 |   |   |   |   | (1,459) | 67.10 |   |   |   |   |
| Forfeited | (83) | 172.13 |   |   |   |   | (137) | 135.42 |   |   |   |   |
| Expired | (37) | 122.58 |   |   |   |   | N/A | N/A |   |   |   |   |
| Outstanding at December 31, 2025 | 7,264 |   | $92.22 | 3.8 |   | $1,568 | 2,391 |   | $141.49 | 1.2 |   | $736 |
| Exercisable at December 31, 2025 | 5,829 |   | $72.33 | 2.6 |   | $1,374 | N/A | N/A |   | N/A | N/A |   |
| Expected to vest | 1,265 |   | $172.50 | 8.6 |   | $171 | 2,194 |   | $139.74 | 1.2 |   | $676 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0078`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Compensation expense (after-tax)(a) |   | $325 |   | $286 |   | $192 |
| Cash received from stock options exercised | 428 |   | 1,492 |   | 565 |   |
| Intrinsic value of stock options exercised and RSU/PSU/Performance shares vested | 853 |   | 1,754 |   | 561 |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0079`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2025 |   |   |   | 2024 |   |   |   | 2023 |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (Earnings for per-share calculation, shares in millions, per-share amounts in dollars) | Diluted |   | Basic |   | Diluted |   | Basic |   | Diluted |   | Basic |   |
| Net income (loss) from continuing operations(a) |   | $8,598 |   | $8,601 |   | $6,670 |   | $6,670 |   | $9,446 |   | $9,449 |
| Preferred stock dividends and other and accretion of preferred share repurchase(b) | — |   | — |   | — |   | — |   | (295) |   | (295) |   |
| Net income (loss) from continuing operations attributable to common shareholders(a) | 8,598 |   | 8,601 |   | 6,670 |   | 6,670 |   | 9,151 |   | 9,154 |   |
| Net income (loss) from discontinued operations | 103 |   | 103 |   | (114) |   | (114) |   | 33 |   | 33 |   |
| Net income (loss) attributable to common shareholders(a) | 8,701 |   | 8,704 |   | 6,556 |   | 6,556 |   | 9,184 |   | 9,187 |   |
| Shares of common stock outstanding | 1,061 |   | 1,061 |   | 1,085 |   | 1,085 |   | 1,089 |   | 1,089 |   |
| Employee compensation-related shares (including stock options) | 8 |   | — |   | 10 |   | — |   | 10 |   | — |   |
| Total average equivalent shares | 1,068 |   | 1,061 |   | 1,094 |   | 1,085 |   | 1,099 |   | 1,089 |   |
| EPS from continuing operations |   | $8.05 |   | $8.11 |   | $6.09 |   | $6.15 |   | $8.33 |   | $8.41 |
| EPS from discontinued operations | 0.10 |   | 0.10 |   | (0.10) |   | (0.11) |   | 0.03 |   | 0.03 |   |

*(2 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0080`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Investment in GE HealthCare realized and unrealized gain (loss) |   | $— |   | $480 |   | $5,639 |
| Investment in and note with AerCap realized and unrealized gain (loss) | 21 |   | 38 |   | 129 |   |
| Investment in Baker Hughes realized and unrealized gain (loss) | — |   | — |   | 10 |   |
| Gains (losses) on retained and sold ownership interests |   | $21 |   | $518 |   | $5,778 |
| Other net interest and investment income (loss)(a)(b) | 946 |   | 813 |   | 637 |   |
| Licensing and royalty income | 175 |   | 210 |   | 148 |   |
| Equity method income | 216 |   | 173 |   | 169 |   |
| Purchases and sales of business interests(c) | 6 |   | 399 |   | (105) |   |
| Other items | 123 |   | 151 |   | 92 |   |
| Total other income (loss) |   | $1,487 |   | $2,264 |   | $6,718 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0081`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| RESTRUCTURING AND OTHER CHARGES | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Workforce reductions |   | $(33) |   | $107 |   | $166 |
| Plant closures & associated costs and other asset write-downs | (51) |   | 74 |   | 84 |   |
| Acquisition/disposition net charges and other | — |   | 366 |   | 10 |   |
|   |   | $(84) |   | $546 |   | $260 |
| Cost of equipment/services |   | $6 |   | $27 |   | $10 |
| Selling, general and administrative expenses | (90) |   | 519 |   | 250 |   |
| Total restructuring and other charges(a) |   | $(84) |   | $546 |   | $260 |
| Restructuring and other cash expenditures(b) |   | $69 |   | $507 |   | $204 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0082`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**ASSETS AND LIABILITIES MEASURED AT FAIR VALUE ON A RECURRING BASIS**

| ASSETS AND LIABILITIES MEASURED AT FAIR VALUE ON A RECURRING BASIS |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Level 1 |   |   |   | Level 2 |   |   |   | Level 3(a) |   |   |   | Nettingadjustment(b) |   |   |   | Net balance(c) |   |   |   |
| December 31 | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Investment securities |   | $655 |   | $14 |   | $34,911 |   | $33,635 |   | $3,222 |   | $5,074 |   | $— |   | $— |   | $38,788 |   | $38,723 |
| Derivatives | — |   | — |   | 247 |   | 243 |   | — |   | — |   | (60) |   | (55) |   | 187 |   | 188 |   |
| Total assets |   | $655 |   | $14 |   | $35,158 |   | $33,878 |   | $3,222 |   | $5,074 |   | $(60) |   | $(55) |   | $38,975 |   | $38,911 |
| Derivatives |   | $— |   | $— |   | $129 |   | $131 |   | $— |   | $— |   | $(58) |   | $(54) |   | $71 |   | $77 |
| Other(d) | — |   | — |   | 400 |   | 367 |   | — |   | — |   | — |   | — |   | 400 |   | 367 |   |
| Total liabilities |   | $— |   | $— |   | $530 |   | $498 |   | $— |   | $— |   | $(58) |   | $(54) |   | $472 |   | $444 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0083`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Balance atJanuary 1 |   | Net realized/unrealized gains(losses)(a) |   | Purchases(b) |   | Sales & Settlements(c) |   | TransfersintoLevel 3 |   | Transfersout ofLevel 3(d) |   | Balance atDecember 31 |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Investment securities |   | $5,074 |   | $27 |   | $2,155 |   | $(2,753) |   | $13 |   | $(1,293) |   | $3,222 |
| 2024 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Investment securities |   | $6,841 |   | $20 |   | $1,505 |   | $(768) |   | $12 |   | $(2,536) |   | $5,074 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0084`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   |   | December 31, 2025 |   |   |   | December 31, 2024 |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
|   |   | Carryingamount(net) |   | Estimatedfair value |   | Carryingamount(net) |   | Estimatedfair value |   |
| Assets | Loans and other receivables(a) |   | $2,197 |   | $2,153 |   | $2,261 |   | $1,981 |
| Liabilities | Borrowings (Note 10) | 20,494 |   | 20,558 |   | 19,273 |   | 18,805 |   |
|   | Investment contracts(a) | 1,140 |   | 1,199 |   | 1,375 |   | 1,432 |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0085`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| FAIR VALUE OF DERIVATIVES |   | December 31, 2025 |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Classification(a) | Gross Notional |   | Fair Value - Assets |   | Fair Value - Liabilities |   | Gross Notional |   | Fair Value - Assets |   | Fair Value - Liabilities |   |
| Qualifying currency exchange contracts | Current |   | $2,125 |   | $38 |   | $17 |   | $1,873 |   | $36 |   | $40 |
| Qualifying cross currency interest rate swaps | Non-Current | 3,079 |   | 20 |   | 62 |   | 416 |   | 8 |   | — |   |
|   | Current | 471 |   | 17 |   | 39 |   | — |   | — |   | — |   |
| Non-qualifying currency exchange contracts and other(b) | Current | 4,983 |   | 172 |   | 12 |   | 6,759 |   | 199 |   | 91 |   |
| Gross derivatives |   |   | $10,659 |   | $247 |   | $129 |   | $9,047 |   | $243 |   | $131 |
| Netting and credit adjustments |   |   |   |   | $(60) |   | $(58) |   |   |   | $(55) |   | $(54) |
| Net derivatives recognized in statement of financial position |   |   |   |   | $187 |   | $71 |   |   |   | $188 |   | $77 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0086`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Amount of Gain (Loss) Recognized in Other Comprehensive Income (Loss) on Derivatives |   |   |   | Amount of Gain (Loss) Reclassified from AOCI into Net Income |   |   |   |
|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Cash flow hedges(a) |   | $133 |   | $(64) |   | $45 |   | $16 |
| Net investment hedges | (798) |   | 348 |   | — |   | — |   |

#### `tbl-src-ge-10k-fy2025-a73b722f-0087`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Balance at January 1 |   | $592 |   | $639 |   | $528 |
| Current-year provisions | 242 |   | 275 |   | 277 |   |
| Expenditures | (242) |   | (321) |   | (167) |   |
| Other changes | 3 |   | (1) |   | — |   |
| Balance at December 31 | 595 |   |   | $592 |   | $639 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0088`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| REVENUE | Total revenue |   |   |   |   |   | Intersegment revenue |   |   |   |   |   | External revenue |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Years ended December 31 | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $33,314 |   | $26,881 |   | $23,855 |   | $62 |   | $216 |   | $559 |   | $33,252 |   | $26,666 |   | $23,296 |
| Defense & Propulsion Technologies | 10,554 |   | 9,478 |   | 8,961 |   | 1,686 |   | 1,453 |   | 1,253 |   | 8,868 |   | 8,025 |   | 7,708 |   |
| Corporate & Other | 1,987 |   | 2,343 |   | 2,532 |   | (1,748) |   | (1,669) |   | (1,812) |   | 3,735 |   | 4,011 |   | 4,344 |   |
| Total revenue |   | $45,855 |   | $38,702 |   | $35,348 |   | $— |   | $— |   | $— |   | $45,855 |   | $38,702 |   | $35,348 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0089`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Years ended December 31 | Equipment |   | Services |   | Total |   | Equipment |   | Services |   | Total |   | Equipment |   | Services |   | Total |   |
| Commercial Engines & Services |   | $8,304 |   | $25,010 |   | $33,314 |   | $7,106 |   | $19,775 |   | $26,881 |   | $6,169 |   | $17,686 |   | $23,855 |
| Defense & Propulsion Technologies | 5,128 |   | 5,426 |   | 10,554 |   | 4,208 |   | 5,270 |   | 9,478 |   | 4,000 |   | 4,961 |   | 8,961 |   |
| Total segment revenue |   | $13,433 |   | $30,436 |   | $43,868 |   | $11,315 |   | $25,045 |   | $36,360 |   | $10,170 |   | $22,647 |   | $32,816 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0090`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| EXPENSES, PROFIT AND INCOME For the years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines & Services |   |   |   |
| Cost of revenue | $21,998 | $17,703 | $16,575 |
| Selling, general and administrative expenses | 1,845 | 1,678 | 1,386 |
| Research and development | 1,287 | 993 | 736 |
| Other segment expenses (income)(a) | (677) | (548) | (484) |
| Total Commercial Engines & Services expenses | 24,453 | 19,826 | 18,213 |
| Defense & Propulsion Technologies |   |   |   |
| Cost of revenue | 7,910 | 7,237 | 6,929 |
| Selling, general and administrative expenses | 1,088 | 954 | 893 |
| Research and development | 308 | 301 | 277 |
| Other segment expenses (income)(a) | (48) | (75) | (46) |

*(13 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0091`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| Years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| U.S. | $18,194 | $17,340 | $17,105 |
| Non-U.S. |   |   |   |
| Europe | 8,603 | 7,800 | 7,248 |
| Asia | 10,819 | 7,237 | 5,734 |
| Americas | 3,664 | 2,593 | 1,862 |
| Middle East and Africa | 4,575 | 3,734 | 3,399 |
| Total Non-U.S. | $27,661 | $21,363 | $18,243 |
| Total geographic revenue | $45,855 | $38,702 | $35,348 |
| Non-U.S. revenue as a % of total revenue | 60% | 55% | 52% |

#### `tbl-src-ge-10k-fy2025-a73b722f-0092`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31 | 2025 | 2024 |
|---|---|---|
| U.S. | $5,736 | $5,166 |
| Non-U.S. |   |   |
| Europe | 1,257 | 1,171 |
| Asia | 505 | 497 |
| Americas | 479 | 431 |
| Other Global | 11 | 12 |
| Total Non-U.S. | $2,252 | $2,111 |
| Property, plant and equipment – net (Note 6) | $7,987 | $7,277 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0093`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**Equity method investment**

|   | Equity method investment |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|
|   | balance |   |   |   | Income (loss) from equity method investments |   |   |   |   |   |
| December 31 | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $1,682 |   | $1,610 |   | $376 |   | $301 |   | $276 |
| Defense & Propulsion Technologies | 189 |   | 186 |   | (2) |   | 8 |   | 8 |   |
| Corporate & Other(a) | 5,244 |   | 4,451 |   | 518 |   | 147 |   | 61 |   |
| Total |   | $7,115 |   | $6,247 |   | $892 |   | $456 |   | $345 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0094`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| For the years ended December 31 | 2025 | 2024 | 2023(a) |
|---|---|---|---|
| Revenue | $48,024 | $35,342 | $41,403 |
| Gross profit (loss) | 1,239 | 1,229 | 4,093 |
| Net income (loss) | 3,538 | 3,243 | 4,768 |
| Net income (loss) attributable to the entity | 3,525 | 3,199 | 4,731 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0095`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| December 31 | 2025 | 2024 |
|---|---|---|
| Current assets | $26,213 | $19,688 |
| Total assets | $67,218 | $54,116 |
| Current liabilities | $23,159 | $17,437 |
| Total liabilities | $32,513 | $23,868 |
| Noncontrolling interests | $336 | $200 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0096`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**Date assumed**

| Date assumed |   |   |   |
|---|---|---|---|
| Executive |   |   |   |
| Name | Position | Age | Officer Position |
| H. Lawrence Culp, Jr. | Chairman of the Board & Chief Executive Officer | 62 | October 2018 |
| Rahul Ghai | Senior Vice President & Chief Financial Officer | 54 | September 2023 |
| Mohamed Ali | Senior Vice President & Chief Technology & Operations Officer(a) | 56 | January 2025 |
| Christian Meisner | Senior Vice President & Chief Human Resources Officer | 56 | April 2024 |
| John R. Phillips III | Senior Vice President, General Counsel & Secretary | 48 | April 2024 |
| Russell Stokes | Senior Vice President & CEO, Commercial Engines & Services(a) | 54 | September 2018 |
| Amy Gowder | Senior Vice President & CEO, Defense & Systems | 50 | April 2024 |
| Ricardo Procacci | Senior Vice President & CEO, Propulsion & Additive Technologies | 58 | April 2024 |
| Robert Giglietti | Vice President, Chief Accounting Officer, Controller and Treasurer | 55 | April 2024 |

#### `tbl-src-ge-10k-fy2025-a73b722f-0097`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**4(j) Second Global Supplemental Indenture dated as of December 2, 2015, among General Electric Capital Corporation, General Electric Company and The Bank of New York Mellon, as successor trustee (incorporated by reference to Exhibit 4.2 to the Company’s Current Report on Form 8-K dated December 3, 2015).**

| 4(j) Second Global Supplemental Indenture dated as of December 2, 2015, among General Electric Capital Corporation, General Electric Company and The Bank of New York Mellon, as successor trustee (incorporated by reference to Exhibit 4.2 to the Company’s Current Report on Form 8-K dated December 3, 2015). |   |
|---|---|
| 4(k) Agreement to furnish to the Securities and Exchange Commission upon request a copy of instruments defining the rights of holders of certain long-term debt of the registrant and consolidated subsidiaries.* |   |
| 4(l) Description of the Registrant’s Securities Registered Pursuant to Section 12 of the Securities Exchange Act of 1934.* |   |
| (10) Except for 10(ll), (mm), (nn), and (oo) below, all of the following exhibits consist of Executive Compensation Plans or Arrangements: |   |
|   | (a) GE Aerospace Executive Life Insurance Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(a) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (b) GE Leadership Life Insurance Plan, effective January 1, 2020 and all amendments to date, including its most recent amendment January 3, 2023 (incorporated by reference to Exhibit 10(b) to the Company’s Annual Report on Form 10-K for the fiscal year ended December 31, 2022). |
|   | (c) GE Aerospace Supplementary Pension Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(d) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (d) GE Aerospace Restoration Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(e) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (e) General Electric 2003 Non-Employee Director Compensation Plan, Amended and Restated as of December 7, 2018 (incorporated by reference to Exhibit 10(g) to the Company’s Annual Report on Form 10-K for the fiscal year ended December 31, 2018). |
|   | (f) Amendment, dated May 7, 2024, to General Electric 2003 Non-Employee Director Compensation Plan, Amended and Restated as of December 7, 2018 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended September 30, 2024). |
|   | (g) GE Aerospace 2024 Non-Employee Director Compensation Plan, effective May 7, 2024 (incorporated by reference to Exhibit 10(b) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2024). |
|   | (h) Form of Director Indemnification Agreement.* |

*(14 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0098`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

**(w) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2025 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2025).**

|   | (w) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2025 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2025). |
|---|---|
|   | (x) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(c) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2024). |
|   | (y) Form of Agreement for Restricted Stock Unit Grants to Executive Offices under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2025 (incorporated by reference to Exhibit 10(f) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (z) Form of Agreement for Restricted Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(e) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (aa) Form of Agreement for Restricted Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2023 (incorporated by reference to Exhibit 10(b) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 31, 2023). |
|   | (bb) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2025 (incorporated by reference to Exhibit 10(h) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (cc) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(g) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (dd) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2023 (incorporated by reference to Exhibit 10(c) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 31, 2023). |
|   | (ee) GE Aerospace Incentive Compensation Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(ee) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (ff) GE Aerospace Annual Executive Incentive Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(ff) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (gg) Employment Agreement between H. Lawrence Culp Jr. and General Electric Company, effective July 1, 2024 (incorporated by reference to Exhibit 10.1 to the Company’s Current Report on Form 8-K dated July 1, 2024). |
|   | (hh) Form of Performance Stock Unit Grant Agreement by and between H. Lawrence Culp, Jr. and General Electric Company, dated July 1, 2024 (incorporated by reference to Exhibit 10.2 to the Company’s Current Report on Form 8-K dated July 1, 2024). |

*(18 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0099`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

| FORM 10-K CROSS REFERENCE INDEX |   | Page(s) |
|---|---|---|
| Part I |   |   |
| Item 1. | Business | 4-7, 9-10, 71-73 |
| Item 1A. | Risk Factors | 24-31 |
| Item 1B. | Unresolved Staff Comments | Not applicable |
| Item 1C. | Cybersecurity | 23 |
| Item 2. | Properties | 4 |
| Item 3. | Legal Proceedings | 70-71 |
| Item 4. | Mine Safety Disclosures | Not applicable |
| Part II |   |   |
| Item 5. | Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities | 22 |
| Item 6. | [Reserved] | Not applicable |

*(17 further rows in the stored grid.)*

#### `tbl-src-ge-10k-fy2025-a73b722f-0100`

table · **exact** · extractor `html_tables_v1` · anchored by `own_text` · not cited by any unit

|   | Signer | Title | Date |
|---|---|---|---|
|   | /s/ Rahul Ghai | Principal Financial Officer | January 29, 2026 |
|   | Rahul GhaiSenior Vice President and Chief Financial Officer |   |   |
|   | /s/ Robert Giglietti | Principal Accounting Officer | January 29, 2026 |
|   | Robert GigliettiVice President, Chief Accounting Officer, Controller and Treasurer |   |   |
|   | /s/ H. Lawrence Culp, Jr. | Principal Executive Officer | January 29, 2026 |
|   | H. Lawrence Culp, Jr.*Chairman of the Board of Directors |   |   |
|   | Sébastien M. Bazin* | Director |   |
|   | Margaret Billson* | Director |   |
|   | Wesley G. Bush* | Director |   |
|   | Thomas Enders* | Director |   |
|   | Edward P. Garden* | Director |   |

*(8 further rows in the stored grid.)*

## Assets in text nobody read

61 asset(s) sit in a region of the source from which no unit was extracted, so nothing in the output points at them. This is a hole in the reading rather than a judgment about evidence: no unit was dropped here, none was ever made. They are shown because they are still the source's content.

### `tbl-src-ge-10k-fy2025-a73b722f-0001`

table · **exact** · anchored by `own_text`

| New York |   |   | 14-0689340 |
|---|---|---|---|
| (State or other jurisdiction of incorporation or organization) |   |   | (I.R.S. Employer Identification No.) |
| 1 Neumann Way | Evendale | OH | 45215 |
| (Address of principal executive offices) |   |   | (Zip Code) |

### `tbl-src-ge-10k-fy2025-a73b722f-0002`

table · **exact** · anchored by `own_text`

| Title of each class | Trading Symbol(s) | Name of each exchange on which registered |
|---|---|---|
| Common stock, par value $0.01 per share | GE | New York Stock Exchange |
| 1.875% Notes due 2027 | GE 27E | New York Stock Exchange |
| 1.500% Notes due 2029 | GE 29 | New York Stock Exchange |
| 7 1/2% Guaranteed Subordinated Notes due 2035 | GE /35 | New York Stock Exchange |
| 2.125% Notes due 2037 | GE 37 | New York Stock Exchange |

### `tbl-src-ge-10k-fy2025-a73b722f-0003`

table · **exact** · anchored by `own_text`

| Large accelerated filer | ☑ | Accelerated filer | ☐ |
|---|---|---|---|
| Non-accelerated filer | ☐ | Smaller reporting company | ☐ |
| Emerging growth company | ☐ |   |   |

### `tbl-src-ge-10k-fy2025-a73b722f-0004`

table · **exact** · anchored by `own_text`

**Page**

| Page |   |
|---|---|
| Forward-Looking Statements | 3 |
| About GE Aerospace | 4 |
| Management’s Discussion and Analysis of Financial Condition and Results of Operations (MD&A) | 7 |
| Consolidated Results | 8 |
| Segment Operations | 9 |
| Corporate & Other | 10 |
| Other Consolidated Information | 11 |
| Capital Resources and Liquidity | 12 |
| Critical Accounting Estimates | 14 |
| Other Items | 16 |
| Non-GAAP Financial Measures | 19 |

*(41 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0011`

table · **exact** · anchored by `own_text`

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $13,754 | $11,462 | $6,508 |
| Services | 156,068 | 142,182 | 131,028 |
| Total RPO | $169,822 | $153,644 | $137,535 |

### `tbl-src-ge-10k-fy2025-a73b722f-0014`

table · **exact** · anchored by `own_text`

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $13,780 | $11,046 | $9,739 |
| Services | 6,962 | 6,944 | 6,729 |
| Total RPO | $20,742 | $17,991 | $16,468 |

### `tbl-src-ge-10k-fy2025-a73b722f-0017`

table · **exact** · anchored by `none`

|   | Moody's | S&P |
|---|---|---|
| Outlook | Positive | Stable |
| Short term | P-2 | A-2 |
| Long term | A3 | A- |

### `tbl-src-ge-10k-fy2025-a73b722f-0018`

table · **exact** · anchored by `own_text`

| Years ended December 31 | 2025 | 2024 |
|---|---|---|
| Increase (decrease) in employee benefit liabilities | $746 | $356 |
| Net restructuring and other charges/(cash expenditures) | (144) | (112) |
| (Gains) Losses on purchases and sales of business interests | (6) | (399) |
| Net interest and other financial charges/(cash paid) | (39) | 31 |
| Other deferred assets | (88) | (84) |
| Other | (334) | (118) |
| All other operating activities | $136 | $(326) |

### `tbl-src-ge-10k-fy2025-a73b722f-0021`

table · **exact** · anchored by `own_text`

| ADJUSTED REVENUE, OPERATING PROFIT AND PROFIT MARGIN (NON-GAAP) | 2025 | 2024 |
|---|---|---|
| Total revenue (GAAP) | $45,855 | $38,702 |
| Less: Insurance revenue (Note 12) | 3,533 | 3,581 |
| Adjusted revenue (Non-GAAP) | $42,322 | $35,121 |
| Total costs and expenses (GAAP) | $37,342 | $33,346 |
| Less: Insurance cost and expenses (Note 12) | 2,541 | 2,560 |
| Less: U.S. tax equity cost and expenses | 20 | 14 |
| Less: interest and other financial charges(a) | 843 | 986 |
| Less: non-operating benefit cost (income) | (788) | (842) |
| Less: restructuring & other(a) | (87) | 525 |
| Less: goodwill impairments(a) | — | 251 |
| Less: separation costs(a) | 202 | 492 |

*(13 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0026`

table · **exact** · anchored by `own_text`

**STATEMENT OF OPERATIONS**

| STATEMENT OF OPERATIONS |   |   |   |
|---|---|---|---|
| (In millions; per-share amounts in dollars) | 2025 | 2024 | 2023 |
| Sales of equipment | $12,159 | $10,274 | $9,318 |
| Sales of services | 30,163 | 24,847 | 22,641 |
| Insurance revenue (Note 12) | 3,533 | 3,581 | 3,389 |
| Total revenue | 45,855 | 38,702 | 35,348 |
| Cost of equipment sold | 12,382 | 10,341 | 9,900 |
| Cost of services sold | 16,586 | 13,967 | 13,039 |
| Selling, general and administrative expenses | 4,088 | 4,437 | 4,045 |
| Separation costs | 202 | 492 | 692 |
| Research and development | 1,580 | 1,286 | 1,011 |
| Interest and other financial charges | 843 | 986 | 1,029 |

*(31 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0027`

table · **exact** · anchored by `own_text`

**STATEMENT OF FINANCIAL POSITION**

| STATEMENT OF FINANCIAL POSITION |   |   |
|---|---|---|
| December 31 (In millions) | 2025 | 2024 |
| Cash, cash equivalents and restricted cash | $12,392 | $13,619 |
| Investment securities (Note 3) | — | 982 |
| Current receivables (Note 4) | 11,773 | 9,327 |
| Inventories, including deferred inventory costs (Note 5) | 11,868 | 9,763 |
| Current contract assets (Note 8) | 3,511 | 2,982 |
| All other current assets (Note 9) | 1,052 | 962 |
| Current assets | 40,596 | 37,635 |
| Investment securities (Note 3) | 38,788 | 37,741 |
| Property, plant and equipment – net (Note 6) | 7,987 | 7,277 |
| Goodwill (Note 7) | 9,060 | 8,538 |

*(29 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0029`

table · **exact** · anchored by `own_text`

**STATEMENT OF COMPREHENSIVE INCOME (LOSS)**

| STATEMENT OF COMPREHENSIVE INCOME (LOSS) |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Net income (loss) | $8,698 | $6,566 | $9,445 |
| Less: net income (loss) attributable to noncontrolling interests | (6) | 11 | (37) |
| Net income (loss) attributable to the Company | $8,704 | $6,556 | $9,482 |
| Currency translation adjustments | (43) | 2,131 | 2,274 |
| Benefit plans | (882) | (1,128) | (4,747) |
| Investment securities and cash flow hedges | 749 | (1,016) | 968 |
| Long-duration insurance contracts | (761) | 2,284 | (2,371) |
| L Less: other comprehensive income (loss) attributable to noncontrolling interests | — | (17) | 2 |
| Other comprehensive income (loss) attributable to the Company | $(937) | $2,289 | $(3,878) |
| Comprehensive income (loss) | $7,761 | $8,838 | $5,569 |

*(2 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0034`

table · **exact** · anchored by `own_text`

| ASSETS AND LIABILITIES OF DISCONTINUED OPERATIONS | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Cash, cash equivalents and restricted cash(a) | $1,126 | $1,327 |
| Current receivables | 35 | 13 |
| Property, plant, and equipment - net | 26 | 40 |
| All other assets | 648 | 438 |
| Deferred income taxes | 21 | 24 |
| Assets of discontinued operations(b) | $1,855 | $1,841 |
| Accounts payable | $35 | $30 |
| Non-current compensation and benefits | 32 | 33 |
| All other liabilities | 1,347 | 1,254 |
| Liabilities of discontinued operations(b) | $1,413 | $1,317 |

### `tbl-src-ge-10k-fy2025-a73b722f-0035`

table · **exact** · anchored by `own_text`

|   | December 31, 2025 |   |   |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Amortizedcost |   | Grossunrealizedgains |   | Grossunrealizedlosses |   | Estimatedfair value |   | Amortizedcost |   | Grossunrealizedgains |   | Grossunrealizedlosses |   | Estimatedfair value |   |
| Debt |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| U.S. corporate |   | $27,658 |   | $825 |   | $(1,969) |   | $26,513 |   | $28,456 |   | $546 |   | $(2,309) |   | $26,692 |
| Non-U.S. corporate | 2,909 |   | 41 |   | (242) |   | 2,707 |   | 2,970 |   | 23 |   | (302) |   | 2,691 |   |
| State and municipal | 2,751 |   | 46 |   | (192) |   | 2,605 |   | 2,409 |   | 22 |   | (235) |   | 2,196 |   |
| Mortgage and asset-backed | 5,202 |   | 69 |   | (121) |   | 5,151 |   | 5,007 |   | 47 |   | (183) |   | 4,870 |   |
| Government and agencies | 1,015 |   | 4 |   | (95) |   | 924 |   | 1,180 |   | 4 |   | (118) |   | 1,066 |   |
| Equity | 887 |   | — |   | — |   | 887 |   | 225 |   | — |   | — |   | 225 |   |
| Non-current investment securities |   | $40,422 |   | $985 |   | $(2,619) |   | $38,788 |   | $40,248 |   | $641 |   | $(3,148) |   | $37,741 |

### `tbl-src-ge-10k-fy2025-a73b722f-0036`

table · **exact** · anchored by `own_text`

| For the years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Net unrealized gains (losses) for equity securities with readily determinable fair value (RDFV) | $313 | $320 | $6,413 |
| Proceeds from debt/equity securities sales and redemptions | 4,922 | 9,099 | 12,595 |
| Gross realized gains on debt securities | 35 | 75 | 52 |
| Gross realized losses and impairments on debt securities | (76) | (66) | (66) |

### `tbl-src-ge-10k-fy2025-a73b722f-0037`

table · **exact** · anchored by `own_text`

| For the years ended December 31 | 2025 | 2024 |
|---|---|---|
| Purchases of investment securities | $(4,050) | $(7,132) |
| Dispositions and maturities of investment securities | 4,475 | 6,168 |
| Net (purchases) dispositions of insurance investment securities | $425 | $(963) |

### `tbl-src-ge-10k-fy2025-a73b722f-0038`

table · **exact** · anchored by `own_text`

|   | Amortized cost |   | Estimated fair value |   |
|---|---|---|---|---|
| Within one year |   | $843 |   | $847 |
| After one year through five years | 3,460 |   | 3,561 |   |
| After five years through ten years | 5,269 |   | 5,498 |   |
| After ten years | 24,762 |   | 22,845 |   |

### `tbl-src-ge-10k-fy2025-a73b722f-0039`

table · **exact** · anchored by `own_text`

**CURRENT RECEIVABLES**

| CURRENT RECEIVABLES |   |   |
|---|---|---|
| December 31 | 2025 | 2024 |
| Customer receivables | $9,269 | $7,385 |
| Revenue sharing and other partner receivables(a) | 1,322 | 1,113 |
| Non-income based tax receivables | 165 | 128 |
| Supplier advances | 867 | 546 |
| Receivables from disposed businesses | 34 | 99 |
| Other sundry receivables | 209 | 162 |
| Allowance for credit losses | (94) | (106) |
| Total current receivables | $11,773 | $9,327 |

### `tbl-src-ge-10k-fy2025-a73b722f-0040`

table · **exact** · anchored by `own_text`

**LONG-TERM RECEIVABLES**

| LONG-TERM RECEIVABLES |   |   |
|---|---|---|
| December 31 | 2025 | 2024 |
| Long-term customer receivables | $173 | $122 |
| Supplier advances | 94 | 50 |
| Sundry receivables | 105 | 106 |
| Allowance for credit losses | (96) | (85) |
| Total long-term receivables | $276 | $194 |

### `tbl-src-ge-10k-fy2025-a73b722f-0041`

table · **exact** · anchored by `own_text`

| December 31 | 2025 | 2024 |
|---|---|---|
| Raw materials and work in process | $9,354 | $7,372 |
| Finished goods | 1,542 | 1,459 |
| Deferred inventory costs(a) | 972 | 932 |
| Inventories, including deferred inventory costs | $11,868 | $9,763 |

### `tbl-src-ge-10k-fy2025-a73b722f-0042`

table · **exact** · anchored by `own_text`

|   | Depreciable lives | Original Cost |   |   |   | Net Carrying Value |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|
| December 31 | (in years) | 2025 |   | 2024 |   |   | 2025 |   | 2024 |   |
| Land and improvements | 8 |   | $139 |   | $131 |   |   | $137 |   | $129 |
| Buildings, structures and related equipment | 8 - 40 | 3,295 |   | 3,146 |   |   | 1,411 |   | 1,369 |   |
| Machinery and equipment | 4 - 20 | 12,757 |   | 11,533 |   |   | 4,432 |   | 3,851 |   |
| Leasehold costs and manufacturing plant under construction | 1 - 10 | 1,197 |   | 1,084 |   |   | 989 |   | 872 |   |
| ROU operating lease assets |   |   |   |   |   |   | 1,018 |   | 1,057 |   |
| Property, plant and equipment - net |   |   | $17,388 |   | $15,894 |   |   | $7,987 |   | $7,277 |

### `tbl-src-ge-10k-fy2025-a73b722f-0044`

table · **exact** · anchored by `own_text`

| OPERATING LEASE EXPENSE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Long-term (fixed) | $309 | $326 | $364 |
| Long-term (variable) | 30 | 111 | 26 |
| Short-term | 47 | 45 | 115 |
| Total operating lease expense | $385 | $482 | $506 |

### `tbl-src-ge-10k-fy2025-a73b722f-0045`

table · **exact** · anchored by `own_text`

| MATURITY OF LEASE LIABILITIES | 2026 |   | 2027 |   | 2028 |   | 2029 |   | 2030 |   | Thereafter |   | Total |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Undiscounted lease payments |   | $278 |   | $221 |   | $176 |   | $154 |   | $117 |   | $377 |   | $1,323 |
| Less: imputed interest |   |   |   |   |   |   |   |   |   |   |   |   | (260) |   |
| Total lease liability as of December 31, 2025 |   |   |   |   |   |   |   |   |   |   |   |   |   | $1,063 |

### `tbl-src-ge-10k-fy2025-a73b722f-0046`

table · **exact** · anchored by `own_text`

| SUPPLEMENTAL INFORMATION RELATED TO OPERATING LEASES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Operating cash flows used for operating leases | $329 | $352 | $427 |
| Right-of-use assets obtained in exchange for new lease liabilities | 238 | 196 | 275 |
| Weighted-average remaining lease term | 7.6 years | 7.8 years | 7.7 years |
| Weighted-average discount rate | 4.7% | 4.6% | 4.5% |

### `tbl-src-ge-10k-fy2025-a73b722f-0048`

table · **exact** · anchored by `own_text`

|   |   | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| INTANGIBLE ASSETS SUBJECT TO AMORTIZATION December 31 | Useful lives (in years) | Gross carryingamount |   | Accumulatedamortization |   | Net |   | Gross carryingamount |   | Accumulatedamortization |   | Net |   |
| Customer-related(a) | 5-20 |   | $3,992 |   | $(2,313) |   | $1,679 |   | $3,850 |   | $(2,083) |   | $1,767 |
| Patents and technology | 5-15 | 2,946 |   | (916) |   | 2,031 |   | 2,744 |   | (759) |   | 1,985 |   |
| Capitalized software | 5-10 | 1,366 |   | (859) |   | 507 |   | 1,296 |   | (803) |   | 493 |   |
| Trademarks & other | 13 | 77 |   | (67) |   | 9 |   | 70 |   | (58) |   | 13 |   |
| Total |   |   | $8,380 |   | $(4,155) |   | $4,225 |   | $7,960 |   | $(3,703) |   | $4,257 |

### `tbl-src-ge-10k-fy2025-a73b722f-0049`

table · **exact** · anchored by `own_text`

| ESTIMATED 5 YEAR CONSOLIDATED AMORTIZATION | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| Estimated annual pre-tax amortization | 351 | 356 | 357 | 376 | 371 |

### `tbl-src-ge-10k-fy2025-a73b722f-0050`

table · **exact** · anchored by `own_text`

| CONTRACT ASSETS, LIABILITIES AND OTHER DEFERRED ASSETS AND INCOME | December 31, 2025 | December 31, 2024 |
|---|---|---|
| Long-term service agreements | $2,792 | $2,374 |
| Equipment and other service agreements | 719 | 609 |
| Current contract assets | $3,511 | $2,982 |
| Nonrecurring engineering costs(a) | $2,423 | $2,438 |
| Customer advances and other(b) | 2,497 | 2,393 |
| Contract and other deferred assets | 4,920 | 4,831 |
| Total contract and other deferred assets | $8,431 | $7,814 |
| Long-term service agreement liabilities | $10,016 | $8,994 |
| Current deferred income | 317 | 359 |
| Contract liabilities and current deferred income | $10,333 | $9,353 |
| Non-current deferred income | 1,065 | 1,013 |

*(2 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0051`

table · **exact** · anchored by `own_text`

| December 31 |   | 2025 |   |   | 2024 |   |   |
|---|---|---|---|---|---|---|---|
|   | Maturities | Amount |   | Average Rate | Amount |   | Average Rate |
| Current portion of long-term borrowings |   |   |   |   |   |   |   |
| Senior notes | 2026 |   | $1,504 | 4.00% | $1,952 |   | 4.03% |
| Subordinated notes and other | 2026 | 157 |   |   | 87 |   |   |
| Other short-term |   | 25 |   |   | — |   |   |
| Total short-term borrowings |   |   | $1,686 |   |   | $2,039 |   |
|   | Maturities | Amount |   | Average Rate | Amount |   | Average Rate |
| Senior notes(a) | 2027 - 2050 |   | $16,773 | 4.00% |   | $15,467 | 4.03% |
| Subordinated notes | 2035 - 2037 | 1,456 |   | 4.40% | 1,330 |   | 4.43% |
| Other |   | 580 |   |   | 437 |   |   |
| Total long-term borrowings |   |   | $18,808 |   |   | $17,234 |   |

*(1 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0052`

table · **exact** · anchored by `own_text`

|   | 2026 |   | 2027 | 2028 | 2029 | 2030 | Thereafter | Total |
|---|---|---|---|---|---|---|---|---|
| Long-term debt maturities | 1,661 | (a) | 1,693 | 480 | 1,639 | 1,700 | 13,296 | 20,469 |

### `tbl-src-ge-10k-fy2025-a73b722f-0053`

table · **exact** · anchored by `own_text`

| December 31 | 2025 | 2024 |
|---|---|---|
| Trade payables | $5,734 | $4,565 |
| Supply chain finance programs | 1,247 | 1,259 |
| Revenue sharing and other partner payables(a) | 2,553 | 1,689 |
| Sundry payables | 544 | 397 |
| Accounts payable | $10,078 | $7,909 |

### `tbl-src-ge-10k-fy2025-a73b722f-0056`

table · **exact** · anchored by `own_text`

|   | December 31, 2025 |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Present value of expected net premiums | Long-term care |   | Structured settlement annuities |   | Life |   | Long-term care |   | Structured settlement annuities |   | Life |   |
| Balance, beginning of year |   | $4,144 |   | $— |   | $4,318 |   | $4,063 |   | $— |   | $4,803 |
| Beginning balance at locked-in discount rate | 3,991 |   | — |   | 4,415 |   | 3,745 |   | — |   | 4,773 |   |
| Effect of changes in cash flow assumptions | 355 |   | — |   | 4 |   | 465 |   | — |   | (1) |   |
| Effect of actual variances from expected experience(a) | (19) |   | — |   | (2,681) |   | (26) |   | — |   | 8 |   |
| Adjusted beginning of year balance | 4,327 |   | — |   | 1,738 |   | 4,184 |   | — |   | 4,780 |   |
| Interest accrual | 221 |   | — |   | 164 |   | 209 |   | — |   | 177 |   |
| Net premiums collected | (408) |   | — |   | (292) |   | (403) |   | — |   | (309) |   |
| Effect of foreign currency | — |   | — |   | 103 |   | — |   | — |   | (234) |   |
| Ending balance at locked-in discount rate | 4,140 |   | — |   | 1,714 |   | 3,991 |   | — |   | 4,415 |   |
| Effect of changes in discount rate assumptions | 287 |   | — |   | 119 |   | 154 |   | — |   | (97) |   |

*(24 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0061`

table · **exact** · anchored by `own_text`

|   | Level 1 |   |   |   | Level 2 |   |   |   | Level 3 |   |   |   | Assets measured at NAV |   |   |   | Total |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Asset Category |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Global equity |   | $1,200 |   | $1,156 |   | $230 |   | $203 |   |   |   |   |   | $2,410 |   | $1,912 |   | $3,840 |   | $3,271 |
| Fixed income and cash investment funds | 952 |   | 1,299 |   | 1,617 |   | 1,448 |   |   |   |   |   |   |   |   |   | 2,569 |   | 2,747 |   |
| U.S. corporate(a) |   |   |   |   | 2,496 |   | 3,125 |   |   |   |   |   |   |   |   |   | 2,496 |   | 3,125 |   |
| Other debt securities(b) |   |   |   |   | 2,957 |   | 3,152 |   |   |   |   |   | 2,263 |   | 1,851 |   | 5,220 |   | 5,003 |   |
| Real estate |   |   |   |   |   |   |   |   | 449 |   | 541 |   | 934 |   | 995 |   | 1,383 |   | 1,536 |   |
| Private equities and other investments |   |   |   |   |   |   |   |   | 246 |   | 312 |   | 7,079 |   | 6,385 |   | 7,325 |   | 6,697 |   |
| Derivatives, net(c) | (67) |   | (139) |   | 12 |   | 20 |   |   |   |   |   |   |   |   |   | (55) |   | (119) |   |
| Cash |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | 284 |   | 297 |   |
| Payables |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   | (400) |   | (440) |   |

*(2 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0062`

table · **exact** · anchored by `own_text`

| ASSET ALLOCATION OF PENSION PLANS | 2025 Target allocation |   | 2025 Actual allocation |   |
|---|---|---|---|---|
|   | Principal Pension | Other Pension (weighted average) | Principal Pension | Other Pension (weighted average) |
| Global equities | 10.0 - 30.0% | 14% | 18% | 12% |
| Debt securities (including cash equivalents) | 19.0 - 87.5 | 65 | 41 | 65 |
| Real estate | 1.0 - 10.0 | 6 | 6 | 7 |
| Private equities & other investments | 12.0 - 44.0 | 15 | 35 | 16 |

### `tbl-src-ge-10k-fy2025-a73b722f-0063`

table · **exact** · anchored by `own_text`

| EXPECTED FUTURE BENEFIT PAYMENTS OF OUR BENEFIT PLANS(a) | Principal pension | Other pension | Principal retiree benefit |
|---|---|---|---|
| 2026 | $1,815 | $190 | $120 |
| 2027 | 1,820 | 190 | 115 |
| 2028 | 1,825 | 200 | 115 |
| 2029 | 1,825 | 205 | 110 |
| 2030 | 1,820 | 210 | 110 |
| 2031-2035 | 8,825 | 1,115 | 465 |

### `tbl-src-ge-10k-fy2025-a73b722f-0065`

table · **exact** · anchored by `own_text`

| INCOME (LOSS) FROM CONTINUING OPERATIONS BEFORE INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| U.S. income (loss) | $6,659 | $4,809 | $7,195 |
| Non-U.S. income (loss) | 3,341 | 2,811 | 3,246 |
| Total | $10,000 | $7,620 | $10,441 |

### `tbl-src-ge-10k-fy2025-a73b722f-0066`

table · **exact** · anchored by `own_text`

| INCOME TAX PAYMENTS | 2025 |
|---|---|
| U.S. Federal(a) | $150 |
| U.S. State(a) | 7 |
| Non-U.S: |   |
| Singapore | 178 |
| United Kingdom | 78 |
| Ireland | 60 |
| Hungary | 52 |
| Italy | 46 |
| India | 36 |
| Other Non-U.S. | 132 |
| Total income taxes paid (received), continuing operations | $739 |

### `tbl-src-ge-10k-fy2025-a73b722f-0069`

table · **exact** · anchored by `own_text`

| RECONCILIATION OF U.S. FEDERAL STATUTORY INCOME TAX RATE TO EFFECTIVE INCOME TAX RATE | 2024 |   |   |   | 2023 |   |   |   |
|---|---|---|---|---|---|---|---|---|
|   |   | Amount |   | Rate |   | Amount |   | Rate |
| U.S. federal statutory income tax rate |   |   | $1,600 | 21.0% |   |   | $2,193 | 21.0% |
| State Taxes, net of federal benefit |   | 123 |   | 1.6 |   | 152 |   | 1.5 |
| Tax on global activities including exports(a) |   | (92) |   | (1.2) |   | 78 |   | 0.7 |
| U.S. business credits(b) |   | (242) |   | (3.2) |   | (254) |   | (2.4) |
| Retained and sold ownership interests |   | (110) |   | (1.4) |   | (1,215) |   | (11.6) |
| All other – net(c) |   | (317) |   | (4.2) |   | 40 |   | 0.3 |
|   |   | (638) |   | (8.4) |   | (1,199) |   | (11.5) |
| Effective income tax rate |   |   | $962 | 12.6% |   |   | $994 | 9.5% |

### `tbl-src-ge-10k-fy2025-a73b722f-0070`

table · **exact** · anchored by `own_text`

| UNRECOGNIZED TAX BENEFITS December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Unrecognized tax benefits | $3,056 | $2,824 | $3,399 |
| Portion that, if recognized, would reduce tax expense and effective tax rate(a) | 2,381 | 2,110 | 2,708 |
| Accrued interest on unrecognized tax benefits | 656 | 609 | 635 |
| Accrued penalties on unrecognized tax benefits | 11 | 14 | 111 |

### `tbl-src-ge-10k-fy2025-a73b722f-0071`

table · **exact** · anchored by `own_text`

| UNRECOGNIZED TAX BENEFITS RECONCILIATION | 2025 | 2024 | 2023 |
|---|---|---|---|
| Balance at January 1 | $2,824 | $3,399 | $3,951 |
| Additions for tax positions of the current year | 347 | 68 | 109 |
| Additions for tax positions of prior years | 93 | 77 | 156 |
| Reductions for tax positions of prior years(a) | (168) | (649) | (710) |
| Settlements with tax authorities | (30) | (14) | (56) |
| Expiration of the statute of limitations | (10) | (57) | (51) |
| Balance at December 31 | $3,056 | $2,824 | $3,399 |

### `tbl-src-ge-10k-fy2025-a73b722f-0072`

table · **exact** · anchored by `own_text`

| DEFERRED INCOME TAXES December 31 | 2025 | 2024 |
|---|---|---|
| Total assets | $7,883 | $7,479 |
| Total liabilities | (424) | (368) |
| Net deferred income tax asset (liability) | $7,459 | $7,111 |

### `tbl-src-ge-10k-fy2025-a73b722f-0073`

table · **exact** · anchored by `own_text`

| COMPONENTS OF THE NET DEFERRED INCOME TAX ASSET (LIABILITY) December 31 | 2025 | 2024 |
|---|---|---|
| Deferred tax assets |   |   |
| Insurance company loss reserves | $2,398 | $2,349 |
| Progress collections, Contract assets, Contract liabilities and deferred items | 1,764 | 1,435 |
| Accrued expenses and reserves | 1,278 | 1,231 |
| Deferred expenses | 1,231 | 1,398 |
| Other compensation and benefits | 580 | 510 |
| Principal pension plans | 989 | 1,009 |
| Non-U.S. loss carryforwards(a) | 2,133 | 1,891 |
| Capital losses carryforward | 881 | 849 |
| State deferred tax assets(b) | 684 | 762 |
| Other | 1,522 | 1,514 |

*(10 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0074`

table · **exact** · anchored by `own_text`

**DEFERRED TAX ASSETS VALUATION ALLOWANCE**

| DEFERRED TAX ASSETS VALUATION ALLOWANCE |   |
|---|---|
| Balance at December 31, 2022 | $(5,164) |
| Additions charged to income tax expense | — |
| Reductions credited to income tax expense | 102 |
| Other adjustments(a) | 1,646 |
| Balance at December 31, 2023 | $(3,416) |
| Additions charged to income tax expense | (2) |
| Reductions credited to income tax expense | 184 |
| Other adjustments | 18 |
| Balance at December 31, 2024 | $(3,216) |
| Additions charged to income tax expense | (2) |
| Reductions credited to income tax expense | 71 |

*(2 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0075`

table · **exact** · anchored by `own_text`

| ACCUMULATED OTHER COMPREHENSIVE INCOME (LOSS) (Dividends per share in dollars) | 2025 | 2024 | 2023 |
|---|---|---|---|
| Beginning balance | $(1,472) | $(3,623) | $(5,893) |
| AOCI before reclasses – net of taxes of $(157), $5 and $74 | (43) | 36 | 12 |
| Reclasses from AOCI – net of taxes of $—, $103 and $(626)(a) | — | 2,093 | 2,262 |
| AOCI | (43) | 2,129 | 2,274 |
| Less AOCI attributable to noncontrolling interests | — | (22) | 4 |
| Currency translation adjustments AOCI | $(1,515) | $(1,472) | $(3,623) |
| Beginning balance | $665 | $1,786 | $6,531 |
| AOCI before reclasses – net of taxes of $(117), $22 and $(497) | (393) | (8) | (1,874) |
| Reclasses from AOCI – net of taxes of $(137), $(269) and $(778)(a) | (489) | (1,119) | (2,873) |
| AOCI | (882) | (1,127) | (4,747) |
| Less AOCI attributable to noncontrolling interests | — | (7) | (2) |

*(13 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0076`

table · **exact** · anchored by `own_text`

| WEIGHTED AVERAGE GRANT DATE FAIR VALUE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Stock options | $79.55 | $65.16 | $36.10 |
| RSUs | 212.45 | 160.70 | 89.6 |
| PSUs | 221.46 | 150.05 | 89.44 |

### `tbl-src-ge-10k-fy2025-a73b722f-0077`

table · **exact** · anchored by `own_text`

| STOCK-BASED COMPENSATION ACTIVITY | Stock options |   |   |   |   |   | RSUs |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Shares (in thousands) | Weighted average exercise price |   | Weighted average contractual term (in years) | Intrinsic value (in millions) |   | Shares (in thousands) | Weighted average grant date fair value |   | Weighted average contractual term (in years) | Intrinsic value (in millions) |   |
| Outstanding at January 1, 2025 | 10,917 |   | $91.78 |   |   |   | 3,607 |   | $103.70 |   |   |   |
| Granted | 569 | 202.16 |   |   |   |   | 380 | 212.45 |   |   |   |   |
| Exercised | (4,102) | 104.40 |   |   |   |   | (1,459) | 67.10 |   |   |   |   |
| Forfeited | (83) | 172.13 |   |   |   |   | (137) | 135.42 |   |   |   |   |
| Expired | (37) | 122.58 |   |   |   |   | N/A | N/A |   |   |   |   |
| Outstanding at December 31, 2025 | 7,264 |   | $92.22 | 3.8 |   | $1,568 | 2,391 |   | $141.49 | 1.2 |   | $736 |
| Exercisable at December 31, 2025 | 5,829 |   | $72.33 | 2.6 |   | $1,374 | N/A | N/A |   | N/A | N/A |   |
| Expected to vest | 1,265 |   | $172.50 | 8.6 |   | $171 | 2,194 |   | $139.74 | 1.2 |   | $676 |

### `tbl-src-ge-10k-fy2025-a73b722f-0078`

table · **exact** · anchored by `own_text`

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Compensation expense (after-tax)(a) |   | $325 |   | $286 |   | $192 |
| Cash received from stock options exercised | 428 |   | 1,492 |   | 565 |   |
| Intrinsic value of stock options exercised and RSU/PSU/Performance shares vested | 853 |   | 1,754 |   | 561 |   |

### `tbl-src-ge-10k-fy2025-a73b722f-0079`

table · **exact** · anchored by `own_text`

|   | 2025 |   |   |   | 2024 |   |   |   | 2023 |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (Earnings for per-share calculation, shares in millions, per-share amounts in dollars) | Diluted |   | Basic |   | Diluted |   | Basic |   | Diluted |   | Basic |   |
| Net income (loss) from continuing operations(a) |   | $8,598 |   | $8,601 |   | $6,670 |   | $6,670 |   | $9,446 |   | $9,449 |
| Preferred stock dividends and other and accretion of preferred share repurchase(b) | — |   | — |   | — |   | — |   | (295) |   | (295) |   |
| Net income (loss) from continuing operations attributable to common shareholders(a) | 8,598 |   | 8,601 |   | 6,670 |   | 6,670 |   | 9,151 |   | 9,154 |   |
| Net income (loss) from discontinued operations | 103 |   | 103 |   | (114) |   | (114) |   | 33 |   | 33 |   |
| Net income (loss) attributable to common shareholders(a) | 8,701 |   | 8,704 |   | 6,556 |   | 6,556 |   | 9,184 |   | 9,187 |   |
| Shares of common stock outstanding | 1,061 |   | 1,061 |   | 1,085 |   | 1,085 |   | 1,089 |   | 1,089 |   |
| Employee compensation-related shares (including stock options) | 8 |   | — |   | 10 |   | — |   | 10 |   | — |   |
| Total average equivalent shares | 1,068 |   | 1,061 |   | 1,094 |   | 1,085 |   | 1,099 |   | 1,089 |   |
| EPS from continuing operations |   | $8.05 |   | $8.11 |   | $6.09 |   | $6.15 |   | $8.33 |   | $8.41 |
| EPS from discontinued operations | 0.10 |   | 0.10 |   | (0.10) |   | (0.11) |   | 0.03 |   | 0.03 |   |

*(2 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0080`

table · **exact** · anchored by `own_text`

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Investment in GE HealthCare realized and unrealized gain (loss) |   | $— |   | $480 |   | $5,639 |
| Investment in and note with AerCap realized and unrealized gain (loss) | 21 |   | 38 |   | 129 |   |
| Investment in Baker Hughes realized and unrealized gain (loss) | — |   | — |   | 10 |   |
| Gains (losses) on retained and sold ownership interests |   | $21 |   | $518 |   | $5,778 |
| Other net interest and investment income (loss)(a)(b) | 946 |   | 813 |   | 637 |   |
| Licensing and royalty income | 175 |   | 210 |   | 148 |   |
| Equity method income | 216 |   | 173 |   | 169 |   |
| Purchases and sales of business interests(c) | 6 |   | 399 |   | (105) |   |
| Other items | 123 |   | 151 |   | 92 |   |
| Total other income (loss) |   | $1,487 |   | $2,264 |   | $6,718 |

### `tbl-src-ge-10k-fy2025-a73b722f-0081`

table · **exact** · anchored by `own_text`

| RESTRUCTURING AND OTHER CHARGES | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Workforce reductions |   | $(33) |   | $107 |   | $166 |
| Plant closures & associated costs and other asset write-downs | (51) |   | 74 |   | 84 |   |
| Acquisition/disposition net charges and other | — |   | 366 |   | 10 |   |
|   |   | $(84) |   | $546 |   | $260 |
| Cost of equipment/services |   | $6 |   | $27 |   | $10 |
| Selling, general and administrative expenses | (90) |   | 519 |   | 250 |   |
| Total restructuring and other charges(a) |   | $(84) |   | $546 |   | $260 |
| Restructuring and other cash expenditures(b) |   | $69 |   | $507 |   | $204 |

### `tbl-src-ge-10k-fy2025-a73b722f-0082`

table · **exact** · anchored by `own_text`

**ASSETS AND LIABILITIES MEASURED AT FAIR VALUE ON A RECURRING BASIS**

| ASSETS AND LIABILITIES MEASURED AT FAIR VALUE ON A RECURRING BASIS |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Level 1 |   |   |   | Level 2 |   |   |   | Level 3(a) |   |   |   | Nettingadjustment(b) |   |   |   | Net balance(c) |   |   |   |
| December 31 | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Investment securities |   | $655 |   | $14 |   | $34,911 |   | $33,635 |   | $3,222 |   | $5,074 |   | $— |   | $— |   | $38,788 |   | $38,723 |
| Derivatives | — |   | — |   | 247 |   | 243 |   | — |   | — |   | (60) |   | (55) |   | 187 |   | 188 |   |
| Total assets |   | $655 |   | $14 |   | $35,158 |   | $33,878 |   | $3,222 |   | $5,074 |   | $(60) |   | $(55) |   | $38,975 |   | $38,911 |
| Derivatives |   | $— |   | $— |   | $129 |   | $131 |   | $— |   | $— |   | $(58) |   | $(54) |   | $71 |   | $77 |
| Other(d) | — |   | — |   | 400 |   | 367 |   | — |   | — |   | — |   | — |   | 400 |   | 367 |   |
| Total liabilities |   | $— |   | $— |   | $530 |   | $498 |   | $— |   | $— |   | $(58) |   | $(54) |   | $472 |   | $444 |

### `tbl-src-ge-10k-fy2025-a73b722f-0083`

table · **exact** · anchored by `own_text`

|   | Balance atJanuary 1 |   | Net realized/unrealized gains(losses)(a) |   | Purchases(b) |   | Sales & Settlements(c) |   | TransfersintoLevel 3 |   | Transfersout ofLevel 3(d) |   | Balance atDecember 31 |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Investment securities |   | $5,074 |   | $27 |   | $2,155 |   | $(2,753) |   | $13 |   | $(1,293) |   | $3,222 |
| 2024 |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Investment securities |   | $6,841 |   | $20 |   | $1,505 |   | $(768) |   | $12 |   | $(2,536) |   | $5,074 |

### `tbl-src-ge-10k-fy2025-a73b722f-0084`

table · **exact** · anchored by `own_text`

|   |   | December 31, 2025 |   |   |   | December 31, 2024 |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
|   |   | Carryingamount(net) |   | Estimatedfair value |   | Carryingamount(net) |   | Estimatedfair value |   |
| Assets | Loans and other receivables(a) |   | $2,197 |   | $2,153 |   | $2,261 |   | $1,981 |
| Liabilities | Borrowings (Note 10) | 20,494 |   | 20,558 |   | 19,273 |   | 18,805 |   |
|   | Investment contracts(a) | 1,140 |   | 1,199 |   | 1,375 |   | 1,432 |   |

### `tbl-src-ge-10k-fy2025-a73b722f-0085`

table · **exact** · anchored by `own_text`

| FAIR VALUE OF DERIVATIVES |   | December 31, 2025 |   |   |   |   |   | December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Classification(a) | Gross Notional |   | Fair Value - Assets |   | Fair Value - Liabilities |   | Gross Notional |   | Fair Value - Assets |   | Fair Value - Liabilities |   |
| Qualifying currency exchange contracts | Current |   | $2,125 |   | $38 |   | $17 |   | $1,873 |   | $36 |   | $40 |
| Qualifying cross currency interest rate swaps | Non-Current | 3,079 |   | 20 |   | 62 |   | 416 |   | 8 |   | — |   |
|   | Current | 471 |   | 17 |   | 39 |   | — |   | — |   | — |   |
| Non-qualifying currency exchange contracts and other(b) | Current | 4,983 |   | 172 |   | 12 |   | 6,759 |   | 199 |   | 91 |   |
| Gross derivatives |   |   | $10,659 |   | $247 |   | $129 |   | $9,047 |   | $243 |   | $131 |
| Netting and credit adjustments |   |   |   |   | $(60) |   | $(58) |   |   |   | $(55) |   | $(54) |
| Net derivatives recognized in statement of financial position |   |   |   |   | $187 |   | $71 |   |   |   | $188 |   | $77 |

### `tbl-src-ge-10k-fy2025-a73b722f-0086`

table · **exact** · anchored by `own_text`

|   | Amount of Gain (Loss) Recognized in Other Comprehensive Income (Loss) on Derivatives |   |   |   | Amount of Gain (Loss) Reclassified from AOCI into Net Income |   |   |   |
|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Cash flow hedges(a) |   | $133 |   | $(64) |   | $45 |   | $16 |
| Net investment hedges | (798) |   | 348 |   | — |   | — |   |

### `tbl-src-ge-10k-fy2025-a73b722f-0087`

table · **exact** · anchored by `own_text`

|   | 2025 |   | 2024 |   | 2023 |   |
|---|---|---|---|---|---|---|
| Balance at January 1 |   | $592 |   | $639 |   | $528 |
| Current-year provisions | 242 |   | 275 |   | 277 |   |
| Expenditures | (242) |   | (321) |   | (167) |   |
| Other changes | 3 |   | (1) |   | — |   |
| Balance at December 31 | 595 |   |   | $592 |   | $639 |

### `tbl-src-ge-10k-fy2025-a73b722f-0088`

table · **exact** · anchored by `own_text`

| REVENUE | Total revenue |   |   |   |   |   | Intersegment revenue |   |   |   |   |   | External revenue |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Years ended December 31 | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $33,314 |   | $26,881 |   | $23,855 |   | $62 |   | $216 |   | $559 |   | $33,252 |   | $26,666 |   | $23,296 |
| Defense & Propulsion Technologies | 10,554 |   | 9,478 |   | 8,961 |   | 1,686 |   | 1,453 |   | 1,253 |   | 8,868 |   | 8,025 |   | 7,708 |   |
| Corporate & Other | 1,987 |   | 2,343 |   | 2,532 |   | (1,748) |   | (1,669) |   | (1,812) |   | 3,735 |   | 4,011 |   | 4,344 |   |
| Total revenue |   | $45,855 |   | $38,702 |   | $35,348 |   | $— |   | $— |   | $— |   | $45,855 |   | $38,702 |   | $35,348 |

### `tbl-src-ge-10k-fy2025-a73b722f-0091`

table · **exact** · anchored by `own_text`

| Years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| U.S. | $18,194 | $17,340 | $17,105 |
| Non-U.S. |   |   |   |
| Europe | 8,603 | 7,800 | 7,248 |
| Asia | 10,819 | 7,237 | 5,734 |
| Americas | 3,664 | 2,593 | 1,862 |
| Middle East and Africa | 4,575 | 3,734 | 3,399 |
| Total Non-U.S. | $27,661 | $21,363 | $18,243 |
| Total geographic revenue | $45,855 | $38,702 | $35,348 |
| Non-U.S. revenue as a % of total revenue | 60% | 55% | 52% |

### `tbl-src-ge-10k-fy2025-a73b722f-0095`

table · **exact** · anchored by `own_text`

| December 31 | 2025 | 2024 |
|---|---|---|
| Current assets | $26,213 | $19,688 |
| Total assets | $67,218 | $54,116 |
| Current liabilities | $23,159 | $17,437 |
| Total liabilities | $32,513 | $23,868 |
| Noncontrolling interests | $336 | $200 |

### `tbl-src-ge-10k-fy2025-a73b722f-0097`

table · **exact** · anchored by `own_text`

**4(j) Second Global Supplemental Indenture dated as of December 2, 2015, among General Electric Capital Corporation, General Electric Company and The Bank of New York Mellon, as successor trustee (incorporated by reference to Exhibit 4.2 to the Company’s Current Report on Form 8-K dated December 3, 2015).**

| 4(j) Second Global Supplemental Indenture dated as of December 2, 2015, among General Electric Capital Corporation, General Electric Company and The Bank of New York Mellon, as successor trustee (incorporated by reference to Exhibit 4.2 to the Company’s Current Report on Form 8-K dated December 3, 2015). |   |
|---|---|
| 4(k) Agreement to furnish to the Securities and Exchange Commission upon request a copy of instruments defining the rights of holders of certain long-term debt of the registrant and consolidated subsidiaries.* |   |
| 4(l) Description of the Registrant’s Securities Registered Pursuant to Section 12 of the Securities Exchange Act of 1934.* |   |
| (10) Except for 10(ll), (mm), (nn), and (oo) below, all of the following exhibits consist of Executive Compensation Plans or Arrangements: |   |
|   | (a) GE Aerospace Executive Life Insurance Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(a) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (b) GE Leadership Life Insurance Plan, effective January 1, 2020 and all amendments to date, including its most recent amendment January 3, 2023 (incorporated by reference to Exhibit 10(b) to the Company’s Annual Report on Form 10-K for the fiscal year ended December 31, 2022). |
|   | (c) GE Aerospace Supplementary Pension Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(d) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (d) GE Aerospace Restoration Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(e) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (e) General Electric 2003 Non-Employee Director Compensation Plan, Amended and Restated as of December 7, 2018 (incorporated by reference to Exhibit 10(g) to the Company’s Annual Report on Form 10-K for the fiscal year ended December 31, 2018). |
|   | (f) Amendment, dated May 7, 2024, to General Electric 2003 Non-Employee Director Compensation Plan, Amended and Restated as of December 7, 2018 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended September 30, 2024). |
|   | (g) GE Aerospace 2024 Non-Employee Director Compensation Plan, effective May 7, 2024 (incorporated by reference to Exhibit 10(b) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2024). |
|   | (h) Form of Director Indemnification Agreement.* |

*(14 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0098`

table · **exact** · anchored by `own_text`

**(w) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2025 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2025).**

|   | (w) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2025 (incorporated by reference to Exhibit 10(a) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2025). |
|---|---|
|   | (x) Form of Agreement for Restricted Stock Unit Grants to Directors under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(c) to the Company’s Quarterly Report on Form 10-Q for the quarter ended June 30, 2024). |
|   | (y) Form of Agreement for Restricted Stock Unit Grants to Executive Offices under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2025 (incorporated by reference to Exhibit 10(f) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (z) Form of Agreement for Restricted Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(e) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (aa) Form of Agreement for Restricted Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2023 (incorporated by reference to Exhibit 10(b) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 31, 2023). |
|   | (bb) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2025 (incorporated by reference to Exhibit 10(h) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (cc) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of May 2024 (incorporated by reference to Exhibit 10(g) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 30, 2025). |
|   | (dd) Form of Agreement for Performance Stock Unit Grants to Executive Officers under the General Electric Company 2022 Long-Term Incentive Plan, as of March 2023 (incorporated by reference to Exhibit 10(c) to the Company’s Quarterly Report on Form 10-Q for the quarter ended March 31, 2023). |
|   | (ee) GE Aerospace Incentive Compensation Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(ee) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (ff) GE Aerospace Annual Executive Incentive Plan, as amended and restated, effective January 1, 2025 (incorporated by reference to Exhibit 10(ff) to the Company's Annual Report on Form 10-K for the fiscal year ended December 31, 2024). |
|   | (gg) Employment Agreement between H. Lawrence Culp Jr. and General Electric Company, effective July 1, 2024 (incorporated by reference to Exhibit 10.1 to the Company’s Current Report on Form 8-K dated July 1, 2024). |
|   | (hh) Form of Performance Stock Unit Grant Agreement by and between H. Lawrence Culp, Jr. and General Electric Company, dated July 1, 2024 (incorporated by reference to Exhibit 10.2 to the Company’s Current Report on Form 8-K dated July 1, 2024). |

*(18 further rows in the stored grid.)*

### `tbl-src-ge-10k-fy2025-a73b722f-0099`

table · **exact** · anchored by `own_text`

| FORM 10-K CROSS REFERENCE INDEX |   | Page(s) |
|---|---|---|
| Part I |   |   |
| Item 1. | Business | 4-7, 9-10, 71-73 |
| Item 1A. | Risk Factors | 24-31 |
| Item 1B. | Unresolved Staff Comments | Not applicable |
| Item 1C. | Cybersecurity | 23 |
| Item 2. | Properties | 4 |
| Item 3. | Legal Proceedings | 70-71 |
| Item 4. | Mine Safety Disclosures | Not applicable |
| Part II |   |   |
| Item 5. | Market for Registrant’s Common Equity, Related Stockholder Matters and Issuer Purchases of Equity Securities | 22 |
| Item 6. | [Reserved] | Not applicable |

*(17 further rows in the stored grid.)*

## The knowledge handed off

Rendered from [`07_enqueue/enqueue.jsonl`](runs/ge/07_enqueue/enqueue.jsonl) — 31 event(s), target `existing-leaf-engine`.

---

### 1. GE Aerospace: what the business is and how it is regulated

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-001-r1` v2

**Slug** `ge-aerospace-what-the-business-is-and-how-it-is-regulated`

The company, its two segments, its customers and the certification regime it operates under. Commercial Engines & Services is roughly three quarters of revenue and three quarters of that is services, so this is an installed-base business; engines run for decades after sale.

**Assertions (8)**

1. Commercial Engines & Services designs, develops, manufactures and services jet engines for commercial airframes and for business aviation and aeroderivative applications, with services including maintenance, repair and overhaul and the sale of spare parts under long-term service agreements, spare parts agreements or time and material contracts. CES was approximately 73% of total GE Aerospace revenue for 2025, with services representing 75% of total CES revenue.

   *backed by* `asmt-0002`

2. Commercial and financial dynamics for major engine platforms play out over many years: new product development cycles are long and, after initial sale, commercial engines can operate for decades with service needs across that life.

   *backed by* `asmt-0003`

3. Defense & Propulsion Technologies is a provider of defense engines and critical aircraft systems, consisting of the Defense & Systems and Propulsion & Additive Technologies businesses. Defense & Systems designs, develops, manufactures and services jet engines and avionics and power systems for governments, militaries and commercial airframers.

   *backed by* `asmt-0004`

4. Some suppliers or their sub-suppliers are limited- or sole-source, so GE's ability to meet customer obligations depends on the product quality, performance, continued availability and stability of those suppliers. In some cases GE must also comply with procurement requirements that limit which suppliers and subcontractors it may use.

   *backed by* `asmt-0007`

5. GE Aerospace reports through two segments: Commercial Engines & Services, and Defense & Propulsion Technologies.

   *backed by* `asmt-0001`

6. GE Aerospace employed approximately 57,000 people at December 31, 2025, of whom approximately 30,000 were in the United States, including approximately 3,800 union-represented manufacturing and service employees. In 2025 the company negotiated collective bargaining agreements with the majority of its US unions, including the IUE-CWA, UAW and IAM.

   *backed by* `asmt-0005`

7. Total research and development was $2,989 million in 2025, $2,699 million in 2024 and $2,476 million in 2023, of which GE Aerospace funded $1,580 million in 2025 and customers and partners funded $1,409 million. Customer funding is primarily from the US Government.

   *backed by* `asmt-0006`

8. Customer selections for aircraft engines, components and systems can significantly affect future sales of parts and services over the life of an engine platform -- so a competitive loss at selection compounds across decades of aftermarket revenue.

   *backed by* `asmt-0008`

**Related topics** `GE Aerospace`, `segments`, `FAA certification`, `aftermarket`

**Assets carried with this entry (6)** — 6 table. 5 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0005</code> — table, exact</summary>

| (In millions) | 2025 | 2024 | 2023 |
|---|---|---|---|
| GE Aerospace funded | $1,580 | $1,286 | $1,011 |
| Customer and partner funded(a) | 1,409 | 1,413 | 1,465 |
| Total Research and development | $2,989 | $2,699 | $2,476 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0043</code> — table, exact, not cited</summary>

|   | Property, plant andequipment additions |   |   |   |   |   | Depreciation and amortization |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| December 31 | 2025 |   | 2024 |   | 2023 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $498 |   | $431 |   | $343 |   | $402 |   | $370 |   | $356 |
| Defense & Propulsion Technologies | 184 |   | 135 |   | 145 |   | 153 |   | 150 |   | 147 |   |
| Corporate and Other(a) | 471 |   | 353 |   | 278 |   | 307 |   | 314 |   | 294 |   |
| Total |   | $1,153 |   | $920 |   | $766 |   | $863 |   | $834 |   | $797 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0047</code> — table, exact, not cited</summary>

|   | Commercial Engines & Services |   | Defense & Propulsion Technologies |   | Total |   |
|---|---|---|---|---|---|---|
| Balance at December 31, 2023 |   | $6,472 |   | $2,476 |   | $8,948 |
| Goodwill impairment | — |   | (251) |   | (251) |   |
| Goodwill adjustments(a) | (131) |   | (28) |   | (159) |   |
| Balance at December 31, 2024 |   | $6,341 |   | $2,197 |   | $8,538 |
| Goodwill acquisition | — |   | 148 |   | 148 |   |

*(2 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0089</code> — table, exact, not cited</summary>

|   | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Years ended December 31 | Equipment |   | Services |   | Total |   | Equipment |   | Services |   | Total |   | Equipment |   | Services |   | Total |   |
| Commercial Engines & Services |   | $8,304 |   | $25,010 |   | $33,314 |   | $7,106 |   | $19,775 |   | $26,881 |   | $6,169 |   | $17,686 |   | $23,855 |
| Defense & Propulsion Technologies | 5,128 |   | 5,426 |   | 10,554 |   | 4,208 |   | 5,270 |   | 9,478 |   | 4,000 |   | 4,961 |   | 8,961 |   |
| Total segment revenue |   | $13,433 |   | $30,436 |   | $43,868 |   | $11,315 |   | $25,045 |   | $36,360 |   | $10,170 |   | $22,647 |   | $32,816 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0090</code> — table, exact, not cited</summary>

| EXPENSES, PROFIT AND INCOME For the years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines & Services |   |   |   |
| Cost of revenue | $21,998 | $17,703 | $16,575 |
| Selling, general and administrative expenses | 1,845 | 1,678 | 1,386 |
| Research and development | 1,287 | 993 | 736 |
| Other segment expenses (income)(a) | (677) | (548) | (484) |

*(19 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0093</code> — table, exact, not cited</summary>

**Equity method investment**

|   | Equity method investment |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|
|   | balance |   |   |   | Income (loss) from equity method investments |   |   |   |   |   |
| December 31 | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2023 |   |
| Commercial Engines & Services |   | $1,682 |   | $1,610 |   | $376 |   | $301 |   | $276 |
| Defense & Propulsion Technologies | 189 |   | 186 |   | (2) |   | 8 |   | 8 |   |
| Corporate & Other(a) | 5,244 |   | 4,451 |   | 518 |   | 147 |   | 61 |   |

*(1 further rows in the stored grid.)*

</details>

**Source units (8)** `u-src-ge-10k-fy2025-a73b722f-0003`, `u-src-ge-10k-fy2025-a73b722f-0005`, `u-src-ge-10k-fy2025-a73b722f-0006`, `u-src-ge-10k-fy2025-a73b722f-0010`, `u-src-ge-10k-fy2025-a73b722f-0002`, `u-src-ge-10k-fy2025-a73b722f-0007`, `u-src-ge-10k-fy2025-a73b722f-0008`, `u-src-ge-10k-fy2025-a73b722f-0011`

**Traceability** — idempotency key `79e62bfcd5ddfa31023cda6482bceee97af28e2a7b42f02ff663a5465bc48e10` · queue event `q-79e62bfcd5ddfa31` · audits `audit-cand-001`

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

### 2. GE Aerospace 2025 results: revenue, profit and backlog

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-002-r1` v2

**Slug** `ge-aerospace-2025-results-revenue-profit-and-backlog`

The year's figures with the drivers the filing states for them, including the backlog's service-heavy composition and the one-off gain that makes 2023 look better than 2024.

**Assertions (11)**

1. Total revenue for 2025 was $45,855 million, against $38,702 million in 2024 and $35,348 million in 2023 -- an increase of $7.2 billion, or 18%, over 2024. Equipment revenue was $12,159 million, services revenue $30,163 million and insurance revenue $3,533 million.

   *backed by* `asmt-0011`

2. Net income from continuing operations attributable to common shareholders was $8,601 million in 2025 against $6,670 million in 2024 and $9,154 million in 2023, with continuing EPS of $8.05, $6.09 and $8.33 respectively. The 2025 increase of $1.9 billion was driven by an increase in segment profit of $2.0 billion.

   *backed by* `asmt-0012`

3. Profit was $10.0 billion in 2025, an increase of $2.4 billion, with profit margin of 21.8%, up 210 basis points. Operating profit, a non-GAAP measure, was $9.1 billion, an increase of $1.8 billion.

   *backed by* `asmt-0013`

4. Remaining performance obligation is defined in the filing as unfilled customer orders for products and product services -- expected life-of-contract sales for product services -- excluding any purchase order that provides the customer the right to cancel.

   *backed by* `asmt-0014`

5. Total RPO was $190,564 million at December 31, 2025, against $171,635 million a year earlier and $154,003 million in 2023 -- an increase of $18.9 billion, or 11%, primarily at Commercial Engines & Services. Services RPO of $163,029 million is roughly six times equipment RPO of $27,534 million.

   *backed by* `asmt-0015`

6. Commercial Engines & Services delivered 2,386 commercial engines in 2025 against 1,911 in 2024, of which 1,802 were LEAP engines against 1,407. Internal shop visit revenue growth was 24% in 2025, 19% in 2024 and 27% in 2023.

   *backed by* `asmt-0016`

7. CES segment revenue was $33,314 million in 2025 with segment profit of $8,861 million and a margin of 26.6%, against 26.2% in 2024 and 23.7% in 2023. Revenue was up $6.4 billion, or 24%, and profit up $1.8 billion, or 26%.

   *backed by* `asmt-0017`

8. Defense & Propulsion Technologies segment revenue was $10,554 million in 2025 with segment profit of $1,296 million and a margin of 12.3%, against 11.2% in 2024 and 10.1% in 2023 -- revenue up 11% and profit up 22%. Defense engine deliveries were 635 units against 490.

   *backed by* `asmt-0001`

9. Corporate & Other revenue includes run-off insurance operations revenue and the elimination of intersegment activity. Corporate & Other operating profit was a cost of $96 million in 2025 against a cost of $339 million in 2024 and a profit of $3,943 million in 2023, the 2023 figure reflecting gains on retained and sold ownership interests of $5,776 million.

   *backed by* `asmt-0019`

10. CES revenue and profit increases were attributed to increased spare parts volume, internal shop visit volume and workscopes, increased engine deliveries and pricing -- with profit increases partially offset by the impact of higher install engine volume.

   *backed by* `asmt-0018`

11. Insurance profit within Corporate & Other was $992 million in 2025, $1,022 million in 2024 and $332 million in 2023, on insurance revenue of $3,533 million, $3,581 million and $3,389 million.

   *backed by* `asmt-0020`

**Related topics** `revenue`, `segment profit`, `remaining performance obligation`

**Assets carried with this entry (12)** — 12 table. 7 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0006</code> — table, exact</summary>

| REVENUE | 2025 | 2024 | 2023 |
|---|---|---|---|
| Equipment revenue | $12,159 | $10,274 | $9,318 |
| Services revenue | 30,163 | 24,847 | 22,641 |
| Insurance revenue | 3,533 | 3,581 | 3,389 |
| Total revenue | $45,855 | $38,702 | $35,348 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0007</code> — table, exact, not cited</summary>

**NET INCOME (LOSS) AND EARNINGS (LOSS) PER SHARE (EPS)**

| NET INCOME (LOSS) AND EARNINGS (LOSS) PER SHARE (EPS) |   |   |   |
|---|---|---|---|
| (Per-share in dollars and diluted) | 2025 | 2024 | 2023 |
| Net income (loss) from continuing operations attributable to common shareholders | $8,601 | $6,670 | $9,154 |
| Continuing EPS | $8.05 | $6.09 | $8.33 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0008</code> — table, exact</summary>

| RPO | December 31, 2025 | December 31, 2024 | December 31, 2023 |
|---|---|---|---|
| Equipment | $27,534 | $22,509 | $16,247 |
| Services | 163,029 | 149,127 | 137,756 |
| Total RPO | $190,564 | $171,635 | $154,003 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0009</code> — table, exact</summary>

| Sales in units, except where noted | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines | 2,386 | 1,911 | 2,075 |
| LEAP Engines(a) | 1,802 | 1,407 | 1,570 |
| Internal shop visit revenue growth % | 24% | 19% | 27% |
| (a) LEAP engines, which are in a significant production ramp, are a subset of Commercial Engines. |   |   |   |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0010</code> — table, exact</summary>

| SEGMENT REVENUE AND PROFIT | 2025 | 2024 | 2023 |
|---|---|---|---|
| Equipment | $8,304 | $7,106 | $6,169 |
| Services | 25,010 | 19,775 | 17,686 |
| Total segment revenue | $33,314 | $26,881 | $23,855 |
| Segment profit | $8,861 | $7,055 | $5,643 |
| Segment profit margin | 26.6% | 26.2% | 23.7% |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0012</code> — table, exact, not cited</summary>

| Sales in units | 2025 | 2024 | 2023 |
|---|---|---|---|
| Defense engines | 635 | 490 | 556 |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0013</code> — table, exact</summary>

| SEGMENT REVENUE AND PROFIT | 2025 | 2024 | 2023 |
|---|---|---|---|
| Defense & Systems (D&S) | $6,574 | $6,109 | $5,927 |
| Propulsion & Additive Technologies (P&AT) | 3,980 | 3,370 | 3,034 |
| Total segment revenue | $10,554 | $9,478 | $8,961 |
| Equipment | $5,128 | $4,208 | $4,000 |
| Services | 5,426 | 5,270 | 4,961 |

*(3 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0015</code> — table, exact, not cited</summary>

| REVENUE AND OPERATING PROFIT (COST) | 2025 | 2024 | 2023 |
|---|---|---|---|
| Insurance revenue (Note 12) | $3,533 | $3,581 | $3,389 |
| Eliminations and other | (1,546) | (1,239) | (857) |
| Corporate & Other revenue | $1,987 | $2,343 | $2,532 |
| Gains (losses) on purchases and sales of business interests | 5 | 398 | (104) |
| Gains (losses) on retained and sold ownership interests and other equity securities (Note 19) | 312 | 532 | 5,776 |

*(13 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0031</code> — table, exact, not cited</summary>

| RESULTS OF DISCONTINUED OPERATIONSFor the year ended December 31, 2025 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $— | $— | $— |
| Cost of equipment and services sold | — | — | — |
| Other income, costs and expenses | — | (47) | (47) |
| Net Income (loss) of discontinued operations before income taxes | — | (47) | (47) |
| Benefit (provision) for income taxes | 125 | 9 | 134 |

*(5 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0032</code> — table, exact, not cited</summary>

| For the year ended December 31, 2024 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $7,244 | $— | $7,244 |
| Cost of equipment and services sold | (6,074) | — | (6,074) |
| Other income, costs and expenses | (1,299) | (21) | (1,320) |
| Net Income (loss) of discontinued operations before income taxes | (129) | (21) | (150) |
| Benefit (provision) for income taxes | 27 | 13 | 40 |

*(5 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0033</code> — table, exact, not cited</summary>

| For the year ended December 31, 2023 | GE Vernova | Bank BPH & Other | Total |
|---|---|---|---|
| Total revenue | $33,265 | $— | $33,265 |
| Cost of equipment and services sold | (28,205) | — | (28,205) |
| Other income, costs and expenses | (5,306) | (1,301) | (6,607) |
| Net Income (loss) of discontinued operations before income taxes | (246) | (1,301) | (1,547) |
| Benefit (provision) for income taxes(a) | (171) | 1,710 | 1,539 |

*(5 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0094</code> — table, exact, not cited</summary>

| For the years ended December 31 | 2025 | 2024 | 2023(a) |
|---|---|---|---|
| Revenue | $48,024 | $35,342 | $41,403 |
| Gross profit (loss) | 1,239 | 1,229 | 4,093 |
| Net income (loss) | 3,538 | 3,243 | 4,768 |
| Net income (loss) attributable to the entity | 3,525 | 3,199 | 4,731 |

</details>

**Source units (11)** `u-src-ge-10k-fy2025-a73b722f-0020`, `u-src-ge-10k-fy2025-a73b722f-0021`, `u-src-ge-10k-fy2025-a73b722f-0022`, `u-src-ge-10k-fy2025-a73b722f-0023`, `u-src-ge-10k-fy2025-a73b722f-0024`, `u-src-ge-10k-fy2025-a73b722f-0025`, `u-src-ge-10k-fy2025-a73b722f-0026`, `u-src-ge-10k-fy2025-a73b722f-0028`, `u-src-ge-10k-fy2025-a73b722f-0030`, `u-src-ge-10k-fy2025-a73b722f-0027`, `u-src-ge-10k-fy2025-a73b722f-0031`

**Traceability** — idempotency key `79e72633f90d593f47b296595bf92c9c7d40e6e885bbb8c85411ec483e4ca835` · queue event `q-79e72633f90d593f` · audits `audit-cand-002`

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

### 3. GE's tax rate, and the businesses it no longer runs

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-003-r1` v2

**Slug** `ge-s-tax-rate-and-the-businesses-it-no-longer-runs`

Why the effective rate sits far below the US statutory rate, what was actually paid in cash, and the exposures retained through discontinued operations.

**Assertions (6)**

1. The effective tax rate was 14.1% in 2025, 12.6% in 2024 and 9.5% in 2023, with a provision for income taxes of $1,405 million, $962 million and $994 million. Cash income taxes paid were $585 million in 2025.

   *backed by* `asmt-0021`

2. The adjusted effective income tax rate, a non-GAAP measure, was 17.3% in 2025 against 20.1% in 2024 -- higher than the GAAP rate in both years.

   *backed by* `asmt-0022`

3. GE states that the rate of tax on its profitable non-US earnings is below the US statutory rate because it has significant business operations subject to tax in countries where the rate on that income is lower, and that the US has enacted a minimum tax on foreign earnings as part of the Tax Cuts and Jobs Act of 2017.

   *backed by* `asmt-0023`

4. The former GE Vernova and GE HealthCare businesses, the Bank BPH mortgage portfolio in Poland, and other trailing assets and liabilities from prior dispositions are reported as discontinued operations.

   *backed by* `asmt-0024`

5. The GE Vernova separation was completed on April 2, 2024 and was structured as a tax-free spin-off. The GE HealthCare separation was completed on January 3, 2023.

   *backed by* `asmt-0025`

6. Bank BPH, along with other Polish banks, has been subject to ongoing litigation in Poland related to its portfolio of floating rate residential mortgage loans, and the Bank BPH financing receivable portfolio is recorded at the lower of cost or fair value less cost to sell.

   *backed by* `asmt-0001`

**Related topics** `effective tax rate`, `discontinued operations`, `Bank BPH`

**Assets carried with this entry (1)** — 1 table.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0016</code> — table, exact</summary>

| INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Effective tax rate (ETR) | 14.1% | 12.6% | 9.5% |
| Provision (benefit) for income taxes | $1,405 | $962 | $994 |
| Cash income taxes paid(a) | 585 | 852 | 994 |

</details>

**Source units (6)** `u-src-ge-10k-fy2025-a73b722f-0033`, `u-src-ge-10k-fy2025-a73b722f-0034`, `u-src-ge-10k-fy2025-a73b722f-0035`, `u-src-ge-10k-fy2025-a73b722f-0037`, `u-src-ge-10k-fy2025-a73b722f-0038`, `u-src-ge-10k-fy2025-a73b722f-0039`

**Traceability** — idempotency key `46b7bb78a100e9369253fd3d4eecf2b761b72fffccb47b618f7897cc3fa70294` · queue event `q-46b7bb78a100e936` · audits `audit-cand-003`

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

### 4. GE's capital structure, liquidity and its stated financial policy

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-004-r1` v2

**Slug** `ge-s-capital-structure-liquidity-and-its-stated-financial-policy`

Borrowings, ratings, the buyback authorization and two qualifications that are easy to miss: no material credit rating covenants, and cash that cannot readily leave the country it sits in.

**Assertions (4)**

1. Consolidated total borrowings were $20.5 billion at December 31, 2025 against $19.3 billion a year earlier, an increase of $1.2 billion primarily due to new debt issued. In July 2025 GE issued $2.0 billion of senior unsecured debt: $1.0 billion of 4.3% senior notes due 2030 and $1.0 billion of 4.9% senior notes.

   *backed by* `asmt-0027`

2. Cash held outside the US has generally been reinvested in active foreign business operations, and substantially all unrepatriated income is subject to US federal tax. Cash at December 31, 2025 included $0.4 billion held in countries with currency control restrictions, which may restrict transfer of funds to the US.

   *backed by* `asmt-0001`

3. Cash from operating activities was $8.5 billion in 2025, an increase of $2.7 billion compared to 2024, primarily due to an increase in net income after adjusting for depreciation of property, plant and equipment.

   *backed by* `asmt-0030`

4. Exchange rate and interest rate risks are managed with a variety of techniques including selective use of derivatives, under policies that include prohibitions on speculative activity. GE states it generates and incurs a small portion of revenue and expenses in currencies other than the US dollar.

   *backed by* `asmt-0031`

**Related topics** `borrowings`, `credit ratings`, `share repurchase`, `liquidity`

**Assets carried with this entry (1)** — 1 table.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0028</code> — table, exact</summary>

**STATEMENT OF CASH FLOWS**

| STATEMENT OF CASH FLOWS |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Net income (loss) | $8,698 | $6,566 | $9,445 |
| Net (income) loss from discontinued operations activities | (103) | 91 | 3 |
| Adjustments to reconcile net income (loss) to cash from (used for) operating activities: |   |   |   |
| Depreciation and amortization of property, plant and equipment (Note 6) | 863 | 834 | 797 |

*(48 further rows in the stored grid.)*

</details>

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0043`, `u-src-ge-10k-fy2025-a73b722f-0045`, `u-src-ge-10k-fy2025-a73b722f-0046`, `u-src-ge-10k-fy2025-a73b722f-0047`

**Traceability** — idempotency key `3c158fb23b74bcffbc9c3ba84fd0be0d7d832e39a9d35f6f408e21337b282f36` · queue event `q-3c158fb23b74bcff` · audits `audit-cand-004`

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

### 5. GE's run-off insurance book and what its assumptions are worth

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-005-r1` v2

**Slug** `ge-s-run-off-insurance-book-and-what-its-assumptions-are-worth`

The long-term care reserves, the policy characteristics that make the tail long, and the quantified sensitivities -- the only place in the filing that states what an assumption change costs in dollars.

**Assertions (9)**

1. GE's run-off insurance operations comprise Employers Reassurance Corporation and Union Fidelity Life Insurance Company. ERAC primarily assumed long-term care insurance.

   *backed by* `asmt-0032`

2. At December 31, 2025 the run-off insurance operations held 201,700 policies in force covering 253,000 lives, with GAAP reserves at the locked-in rate of $23,837 million and gross statutory reserves of $29,843 million. The average policyholder attained age was 80.

   *backed by* `asmt-0033`

3. Among the long-term care policies, 63% have a lifetime benefit period, 77% have an inflation protection option, 25% are joint lives and 64% are premium paying. 19,300 policies were on claim.

   *backed by* `asmt-0034`

4. GE discloses sensitivities on its future policy benefit reserves. A 5% increase in long-term care incidence rates would have an estimated adverse impact of $600 million on the projected present value of future cash flows; a 5% reduction in disabled life deaths, $1,200 million; a 5% increase in utilization, $1,200 million; and no morbidity improvement, $1,200 million.

   *backed by* `asmt-0037`

5. Further disclosed sensitivities: a 5% reduction in long-term care mortality would have an estimated adverse impact of $300 million; a 25% adverse change in the success rate on premium rate increase actions not yet approved, $200 million; a 0.25% increase in the long-term care inflation rate, $100 million; a 5% increase in life insurance mortality, $100 million; and impaired-life structured settlement mortality grading to standard ten years earlier, $300 million.

   *backed by* `asmt-0038`

6. GE reviews its run-off insurance cash flow assumptions at least annually and regularly monitors emerging experience and industry developments to identify trends that may help refine reserve assumptions.

   *backed by* `asmt-0040`

7. GE reinsures approximately 23,000 structured settlement annuities with an average attained age of 58, and its life reinsurance business covers mortality risk on policies reinsured from approximately 135 companies.

   *backed by* `asmt-0035`

8. Future policy benefit reserves represent the present value of future benefits to be paid to or on behalf of policyholders and related expenses, less the present value of future net premiums.

   *backed by* `asmt-0036`

9. Substantially all long-term care insurance policies that are currently premium paying allow the issuing insurance entity to increase premiums, subject to regulatory approval -- so future premium rate increases are an assumption in the reserve, not a certainty.

   *backed by* `asmt-0039`

**Related topics** `long-term care insurance`, `sensitivity analysis`, `reserves`

**Assets carried with this entry (3)** — 3 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0019</code> — table, exact</summary>

| December 31, 2025 | ERAC | UFLIC | Total |
|---|---|---|---|
| GAAP: Ending balance of reserves at locked-in rate | $18,887 | $4,950 | $23,837 |
| Gross statutory reserves(a) | 23,943 | 5,900 | 29,843 |
| Number of policies in force | 161,300 | 40,400 | 201,700 |
| Number of covered lives in force | 212,600 | 40,400 | 253,000 |
| Average policyholder attained age | 79 | 85 | 80 |

*(10 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0020</code> — table, exact, not cited</summary>

| Assumption | Hypothetical change in 2025 assumption | Estimated adverse impact to projected present value of future cash flows (In millions, pre-tax) |
|---|---|---|
| Morbidity: |   |   |
| Long-term care insurance incidence rates | 5% increase in incidence rates | $600 |
| Long-term care insurance claim continuance | 5% reduction in disabled life deaths | $1,200 |
| Long-term care insurance utilization | 5% increase in utilization | $1,200 |
| Long-term care insurance morbidity improvement | 25 basis point reduction by age with 0% floorNo morbidity improvement | $300$1,200 |

*(6 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0054</code> — table, exact, not cited</summary>

| December 31, 2025 | Long-term care | Structured settlement annuities | Life | Other contracts | Total |
|---|---|---|---|---|---|
| Future policy benefit reserves | $25,792 | $8,383 | $906 | $357 | $35,438 |
| Investment contracts | — | 647 | — | 493 | 1,140 |
| Other | — | — | 113 | 203 | 316 |
| Total | $25,792 | $9,031 | $1,019 | $1,053 | $36,894 |

</details>

**Source units (9)** `u-src-ge-10k-fy2025-a73b722f-0048`, `u-src-ge-10k-fy2025-a73b722f-0049`, `u-src-ge-10k-fy2025-a73b722f-0050`, `u-src-ge-10k-fy2025-a73b722f-0053`, `u-src-ge-10k-fy2025-a73b722f-0054`, `u-src-ge-10k-fy2025-a73b722f-0056`, `u-src-ge-10k-fy2025-a73b722f-0051`, `u-src-ge-10k-fy2025-a73b722f-0052`, `u-src-ge-10k-fy2025-a73b722f-0055`

**Traceability** — idempotency key `6c669caaaf25ee76d9283ff468c398385f75bf0805e275b0f41d1acee4c34875` · queue event `q-6c669caaaf25ee76` · audits `audit-cand-005`

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

### 6. Risks GE discloses that carry a mechanism

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-006-r1` v2

**Slug** `risks-ge-discloses-that-carry-a-mechanism`

The risk factors reduced to the ones stating something checkable: sector concentration, product quality costs already incurred, supplier qualification time, and the possibility that a completed tax-free separation is later determined taxable.

**Assertions (4)**

1. GE identifies product safety and quality as an operational risk, stating that its products and services are highly sophisticated and specialized and that a major failure or quality issue affecting its products, or third-party products with which they are used, is a risk. It states it has incurred, and may incur, increased costs, delayed payments or lost equipment or services revenue in connection with a significant issue.

   *backed by* `asmt-0001`

2. GE states it continues to have exposure to its run-off insurance operations and the Bank BPH mortgage portfolio in Poland.

   *backed by* `asmt-0001`

3. GE states that significant input shortages, supplier capacity constraints, supplier or customer production disruptions, supplier quality and sourcing issues or price increases have increased its costs, and that replacing a supplier can require identifying and qualifying a new one or developing manufacturing alternatives, which can take substantial time to implement.

   *backed by* `asmt-0001`

4. GE states that the completed GE HealthCare and GE Vernova separations entail certain risks and potential liabilities, including the risk that one or both is determined to be a taxable transaction.

   *backed by* `asmt-0001`

**Related topics** `risk factors`, `product safety`, `supply chain`, `spin-offs`

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0064`, `u-src-ge-10k-fy2025-a73b722f-0067`, `u-src-ge-10k-fy2025-a73b722f-0065`, `u-src-ge-10k-fy2025-a73b722f-0066`

**Traceability** — idempotency key `0a855f2a3d794f14569673a4899033063b91e53a4bd6c0c5dd85995b4362f4f5` · queue event `q-0a855f2a3d794f14` · audits `audit-cand-006`

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

### 7. Internal control, the auditor, and the two critical audit matters

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-007-r1` v2

**Slug** `internal-control-the-auditor-and-the-two-critical-audit-matters`

Management's Section 404 conclusion and the auditor's own account of where the estimates are hardest -- which lands on the same two areas the filing discloses the most sensitivity about.

**Assertions (3)**

1. The auditor identified two critical audit matters: revenue recognition on certain Aerospace long-term service agreements, and future policy benefits in the run-off insurance operations.

   *backed by* `asmt-0045`

2. On the long-term service agreements the auditor states that the agreements require GE to provide maintenance services over the contract term, and that given the complexity of evaluating the estimates -- including significant judgment necessary to estimate future costs -- auditing the key assumptions required a high degree of auditor judgment.

   *backed by* `asmt-0042`

3. On future policy benefits the auditor states that the liability is based on current assumptions applied to underlying policy cash flows, that significant uncertainties exist in evaluating future cash flow projections over the life of the insurance contracts, and that auditing it required a high degree of auditor judgment and an increased extent of effort, including the use of actuarial specialists.

   *backed by* `asmt-0047`

**Related topics** `internal control`, `Deloitte`, `critical audit matters`

**Source units (3)** `u-src-ge-10k-fy2025-a73b722f-0073`, `u-src-ge-10k-fy2025-a73b722f-0074`, `u-src-ge-10k-fy2025-a73b722f-0075`

**Traceability** — idempotency key `a13834d759c182f06b79f867df5686d30bf02e8912c7a6146cf88492c01414c1` · queue event `q-a13834d759c182f0` · audits `audit-cand-007`

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

### 8. GE's accounting policies: how the numbers are made

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-008-r1` v2

**Slug** `ge-s-accounting-policies-how-the-numbers-are-made`

The definition-shaped part of the filing. Service revenue is recognized against an estimate of total costs, so the estimate is the revenue; CFM International sits outside the consolidated statements; fair values divide between quoted price and internal model.

**Assertions (10)**

1. GE uses derivatives to manage risks including interest rates, foreign exchange, certain equity investments and commodities, and states that accounting for derivatives as hedges requires that at inception and over the term of the arrangement the hedged item and related derivative meet the requirements for hedge accounting.

   *backed by* `asmt-0052`

2. Deferred income tax balances reflect the effects of temporary differences between the carrying amounts of assets and liabilities and their tax bases, as well as net operating losses. GE states that significant judgment is required when assessing its income tax positions and determining tax expense and benefits.

   *backed by* `asmt-0053`

3. For long-term service agreements GE recognizes revenue using the percentage of completion method, based on costs incurred to date relative to its estimate of total costs. Rights to consideration are generally based on utilization of the asset, such as per hour of usage.

   *backed by* `asmt-0048`

4. Contracts are often modified to account for changes in specifications or requirements, and contract modifications in GE's long-term service agreements are predominantly accounted for in a stated manner set out in the policy.

   *backed by* `asmt-0049`

5. GE recognizes revenue on spare parts sold through its services businesses, and enters into long-term development agreements primarily within Defense & Propulsion Technologies, the majority of which are with government customers.

   *backed by* `asmt-0050`

6. GE tests goodwill at least annually for impairment at the reporting unit level, and recognizes an impairment charge if the carrying amount of a reporting unit exceeds its fair value.

   *backed by* `asmt-0051`

7. For fair value measurement GE uses quoted market prices for debt securities where available (Level 1), values publicly traded equity securities using quoted prices (Level 1), and values the majority of its derivatives using internal models that maximize the use of market observable inputs including interest rate curves. It annually reviews its primary pricing vendors to validate that inputs used in their pricing processes are market observable.

   *backed by* `asmt-0054`

8. GE receives grants and incentives from federal, state, local and foreign governments in exchange for compliance with certain conditions, and in December 2025 the FASB issued ASU No. 2025-10 establishing a framework for accounting for government grants received by business entities.

   *backed by* `asmt-0055`

9. In 2025 GE adopted ASU No. 2023-09, Income Taxes (Topic 740): Improvements to Income Tax Disclosures. In November 2024 the FASB issued ASU No. 2024-03 on income statement expense disaggregation.

   *backed by* `asmt-0056`

10. Beginning in the first quarter of 2025 GE changed the terminology used to report GAAP earnings from 'Earnings' to 'Net income', and non-GAAP earnings from 'Adjusted earnings' to 'Adjusted net income'.

   *backed by* `asmt-0057`

**Related topics** `revenue recognition`, `equity method`, `fair value`, `hedge accounting`

**Source units (10)** `u-src-ge-10k-fy2025-a73b722f-0082`, `u-src-ge-10k-fy2025-a73b722f-0083`, `u-src-ge-10k-fy2025-a73b722f-0076`, `u-src-ge-10k-fy2025-a73b722f-0077`, `u-src-ge-10k-fy2025-a73b722f-0078`, `u-src-ge-10k-fy2025-a73b722f-0080`, `u-src-ge-10k-fy2025-a73b722f-0085`, `u-src-ge-10k-fy2025-a73b722f-0087`, `u-src-ge-10k-fy2025-a73b722f-0088`, `u-src-ge-10k-fy2025-a73b722f-0089`

**Traceability** — idempotency key `1c3cd4d1edd0762bbe6bf98d3b863bc72579fbf55642db2989e077743914efa1` · queue event `q-1c3cd4d1edd0762b` · audits `audit-cand-008`

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

### 9. Legal, environmental and indemnification exposures GE retains

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-009-r1` v2

**Slug** `legal-environmental-and-indemnification-exposures-ge-retains`

Obligations that outlived the businesses that created them: shareholder litigation running since 2018, roughly $190 million a year of remediation, indemnities to separated companies, and the warranty provision.

**Assertions (3)**

1. At December 31, 2025 GE had total investment commitments of $4,115 million, of which $3,984 million related to investments by its run-off insurance operations.

   *backed by* `asmt-0044`

2. Following the GE Vernova separation GE retains performance and bank guarantees, and it has remaining obligations under the tax matters agreement to indemnify GE HealthCare for certain tax costs -- $52 million relating to continuing operations and $39 million relating to discontinued operations, both fully reserved.

   *backed by* `asmt-0064`

3. GE provides for estimated product warranty expenses when it sells the related products. The warranty balance was $595 million at December 31, 2025 against $592 million a year earlier, with current-year provisions of $242 million and expenditures of $242 million.

   *backed by* `asmt-0041`

**Related topics** `shareholder litigation`, `environmental remediation`, `indemnification`

**Source units (3)** `u-src-ge-10k-fy2025-a73b722f-0105`, `u-src-ge-10k-fy2025-a73b722f-0106`, `u-src-ge-10k-fy2025-a73b722f-0107`

**Traceability** — idempotency key `3401f716e0eb178a4a4d8c0b80442d98d702cc1cb0feef7fe8bda1a9a6d398b1` · queue event `q-3401f716e0eb178a` · audits `audit-cand-009`

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

### 10. Operating conditions GE reports as fact, not contingency

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-010-r1` v2

**Slug** `operating-conditions-ge-reports-as-fact-not-contingency`

Supply disruption and tariff cost are stated in the indicative -- have impacted, will result -- and the investments made against them are quantified.

**Assertions (2)**

1. Global material availability and supplier delivery performance continued to cause disruptions in 2025 and affected GE's production and delivery of equipment and services to customers.

   *backed by* `asmt-0009`

2. On January 15, 2026 -- after the fiscal year end but before the filing -- GE announced that the Commercial Engines & Services segment will expand to include the entire commercial engine lifecycle, including safety and quality, product management, engineering, supply chain and manufacturing.

   *backed by* `asmt-0001`

**Related topics** `supply chain`, `tariffs`, `capital investment`

**Source units (2)** `u-src-ge-10k-fy2025-a73b722f-0016`, `u-src-ge-10k-fy2025-a73b722f-0019`

**Traceability** — idempotency key `be6ceed11e197bbfef4c76a0c45c476ef16f03b9516c1cce05f53da68ea64a97` · queue event `q-be6ceed11e197bbf` · audits `audit-cand-010`

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

### 11. GE's pension obligations and the deficit behind them

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-011-r1` v2

**Slug** `ge-s-pension-obligations-and-the-deficit-behind-them`

A $5.4 billion deficit that appears nowhere in the results discussion, including a $2.9 billion supplementary plan with no assets against it.

**Assertions (5)**

1. GE sponsors pension and retiree health and life insurance benefit plans presented in three categories. Effective January 1, 2023 certain postretirement benefit plans and liabilities were legally split or allocated between GE HealthCare, GE Vernova and GE Aerospace.

   *backed by* `asmt-0043`

2. Total plan benefit obligations were $28,484 million at December 31, 2025 against plan assets of $23,052 million, a deficit of $5,432 million, compared with a deficit of $5,548 million a year earlier. The GE Aerospace Pension Plan alone had an obligation of $21,053 million against assets of $19,216 million.

   *backed by* `asmt-0059`

3. The GE Aerospace Supplementary Pension Plan is unfunded, with benefits paid on a pay-as-you-go basis, and had an obligation of $2,872 million at December 31, 2025 against no plan assets. Retiree benefit plans are likewise funded on a pay-as-you-go basis.

   *backed by* `asmt-0060`

4. GE's pension funding policy is to contribute amounts sufficient to meet minimum funding requirements under employee benefit and tax laws, with additional contributions at its discretion. ERISA determines minimum funding requirements in the US, and in 2026 GE expects to make payments of approximately $220 million for Supplementary Pension Plan benefits and remaining principal pension plans.

   *backed by* `asmt-0061`

5. The principal pension plans cover approximately 79,000 retirees and beneficiaries and approximately 33,000 vested former employees among US GE Aerospace participants, and the principal retiree benefit plans cover approximately 40,000 retirees. Other pension plans comprise six US and non-US plans with assets or obligations that have reached $50 million.

   *backed by* `asmt-0062`

**Related topics** `pension deficit`, `ERISA`, `unfunded obligations`

**Assets carried with this entry (4)** — 4 table. 3 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0057</code> — table, exact, not cited</summary>

**DESCRIPTION OF OUR PLANS**

| DESCRIPTION OF OUR PLANS |   |   |   |   |
|---|---|---|---|---|
| Plan Category |   | Participants | Funding | Comments |
| Principal Pension Plans | GE Aerospace Pension Plan | Covers U.S. GE Aerospace participants: ~79,000 retirees and beneficiaries, ~33,000 vested former employees and ~9,000 active employees | Our funding policy is to contribute amounts sufficient to meet minimum funding requirements under employee benefit and tax laws. We may decide to contribute additional amounts beyond this level. | Closed to new participants since 2012. Benefits for employees with salaried benefits were frozen effective January 1, 2021, and thereafter these employees receive increased company contributions in the company sponsored defined contribution plan in lieu of participation in a defined benefit plan (announced October 2019). |
|   | GE Aerospace Supplementary Pension Plan | Provides supplementary benefits to higher-level, longer-service U.S. employees | Unfunded. We pay benefits on a pay-as-you-go basis from company cash. | The annuity benefit has been closed to new participants since 2011 and has been replaced by an installment benefit (which was closed to new executives after 2020). Benefits for employees who became executives before 2011 were frozen effective January 1, 2021, and thereafter these employees accrue the installment benefit. |
| Other Pension Plans(a) | 6 U.S. and non-U.S. pension plans with pension assets or obligations that have reached $50 million | Covers ~11,100 retirees and beneficiaries, ~10,300 vested former employees and ~800 active employees | Our funding policy is to contribute amounts sufficient to meet minimum funding requirements under employee benefit and tax laws in each country. We may decide to contribute additional amounts beyond this level. We pay benefits for some plans from company cash. | In certain countries, benefit accruals have ceased and/or have been closed to new hires as of various dates. |
| Principal Retiree Benefit Plans | Provides health and life insurance benefits to certain eligible participants | Covers U.S. GE Aerospace participants: ~40,000 retirees and dependents and ~10,000 active employees | We fund retiree benefit plans on a pay-as-you-go basis and the retiree benefit insurance trust at our discretion. | Participants share in the cost of the healthcare benefits. |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0058</code> — table, exact, not cited</summary>

| FUNDING STATUS BY PLAN TYPE | Benefit Obligation |   |   |   | Fair Value of Assets |   |   |   | Deficit/(Surplus) |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   | 2024 |   | 2025 |   | 2024 |   | 2025 |   | 2024 |   |
| Principal Pension Plans: |   |   |   |   |   |   |   |   |   |   |   |   |
| GE Aerospace Pension Plan (subject to regulatory funding) |   | $21,053 |   | $21,010 |   | $19,216 |   | $19,020 |   | $1,837 |   | $1,990 |
| GE Aerospace Supplementary Pension Plan | 2,872 |   | 2,814 |   | — |   | — |   | 2,872 |   | 2,814 |   |
|   | 23,925 |   | 23,824 |   | 19,216 |   | 19,020 |   | 4,709 |   | 4,804 |   |

*(7 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0059</code> — table, exact, not cited</summary>

| COST OF OUR BENEFITS PLANS AND ASSUMPTIONS | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Components of expense (income) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Service cost - operating |   | $59 |   | $2 |   | $13 |   | $71 |   | $22 |   | $13 |   | $94 |   | $37 |   | $17 |
| Interest cost | 1,301 |   | 173 |   | 62 |   | 1,401 |   | 227 |   | 71 |   | 1,892 |   | 422 |   | 111 |   |
| Expected return on plan assets | (1,500) |   | (207) |   | — |   | (1,751) |   | (310) |   | — |   | (2,376) |   | (587) |   | — |   |

*(14 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0060</code> — table, exact</summary>

**PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME)**

| PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   |   |   |   |   |   |   | 2024 |   |   |   |   |   |
|   | Principal pension |   |   | Other pension |   | Principal retiree benefit |   |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Change in benefit obligations |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Balance at January 1 |   | $23,824 |   |   | $3,140 |   | $1,202 |   |   | $36,217 |   | $10,377 |   | $2,055 |
| Service cost | 59 |   |   | 2 |   | 13 |   |   | 71 |   | 22 |   | 13 |   |

*(28 further rows in the stored grid.)*

</details>

**Source units (5)** `u-src-ge-10k-fy2025-a73b722f-0097`, `u-src-ge-10k-fy2025-a73b722f-0098`, `u-src-ge-10k-fy2025-a73b722f-0099`, `u-src-ge-10k-fy2025-a73b722f-0100`, `u-src-ge-10k-fy2025-a73b722f-0101`

**Traceability** — idempotency key `91dad981a0040e7d303b7ae0682c95063f616d120e41e8ec588a359288a3f6d9` · queue event `q-91dad981a0040e7d` · audits `audit-cand-011`

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

### 12. Free cash flow, geography, and what GE does not report by segment

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-012-r1` v2

**Slug** `free-cash-flow-geography-and-what-ge-does-not-report-by-segment`

The non-GAAP reconciliation, the fact that most revenue is earned outside the US, and the stated absence of segment assets.

**Assertions (4)**

1. Non-US revenue exceeded US revenue in every year presented: $27,661 million against $18,194 million in 2025. Within non-US revenue, Asia was $10,819 million, Europe $8,603 million, Middle East and Africa $4,575 million and the Americas $3,664 million. Asia grew from $5,734 million in 2023, the fastest-growing region shown.

   *backed by* `asmt-0065`

2. GE has two reportable segments and three operating segments, with operating segments aggregated into a reportable segment where they meet the aggregation criteria. The company does not report total assets by segment for internal or external purposes, because its chief operating decision maker does not use segment assets to assess performance or make strategic decisions.

   *backed by* `asmt-0001`

3. Intersegment revenue is material within Defense & Propulsion Technologies: of $10,554 million total segment revenue in 2025, $1,686 million was intersegment, leaving $8,868 million external. Commercial Engines & Services was almost entirely external at $33,252 million of $33,314 million.

   *backed by* `asmt-0066`

4. Free cash flow, a non-GAAP measure, was $7,694 million in 2025 against $6,203 million in 2024. It is reconciled from GAAP cash flows from operating activities of $8,543 million by deducting gross additions to property, plant and equipment and internal-use software of $1,273 million, adding dispositions of $123 million, and excluding separation cash expenditures of $245 million and Corporate & Other restructuring cash expenditures of $56 million.

   *backed by* `asmt-0068`

**Related topics** `free cash flow`, `geographic revenue`, `segment reporting`

**Assets carried with this entry (2)** — 2 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0022</code> — table, exact, not cited</summary>

| ADJUSTED NET INCOME (LOSS) AND ADJUSTED EFFECTIVE INCOME TAX RATE (NON-GAAP) | 2025 |   |   | 2024 |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|
| (Diluted, per-share amounts in dollars) |   | Income |   | EPS |   | Income |   | EPS |   |
| Net income (loss) from continuing operations (GAAP) (Note 18) |   |   | $8,598 |   | $8.05 |   | $6,670 |   | $6.09 |
| Insurance net income (loss) (pre-tax) |   | 1,002 |   | 0.94 |   | 1,025 |   | 0.94 |   |
| Tax effect on Insurance net income (loss)(a) |   | (125) |   | (0.12) |   | (219) |   | (0.20) |   |
| Less: Insurance net income (loss) (net of tax) (Note 12) |   | 877 |   | 0.82 |   | 806 |   | 0.74 |   |

*(35 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0023</code> — table, exact, not cited</summary>

| FREE CASH FLOW (FCF) (NON-GAAP) | 2025 | 2024 |
|---|---|---|
| Cash flows from operating activities (CFOA) (GAAP) | $8,543 | $5,817 |
| Add: gross additions to property, plant and equipment and internal-use software | (1,273) | (1,032) |
| Add: dispositions of property, plant and equipment | 123 | 114 |
| Less: separation cash expenditures | (245) | (800) |
| Less: Corporate & Other restructuring cash expenditures | (56) | (504) |

*(2 further rows in the stored grid.)*

</details>

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0108`, `u-src-ge-10k-fy2025-a73b722f-0109`, `u-src-ge-10k-fy2025-a73b722f-0110`, `u-src-ge-10k-fy2025-a73b722f-0111`

**Traceability** — idempotency key `0f75b6c8b39c003f7a8d6aa7da8c02707b1b501f1c76aa217a8737c0e5977d12` · queue event `q-0f75b6c8b39c003f` · audits `audit-cand-012`

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

### 13. GE's capital structure, liquidity and its stated financial policy

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-013-r1` v2

**Slug** `ge-s-capital-structure-liquidity-and-its-stated-financial-policy`

Borrowings, ratings, the buyback authorization and two qualifications that are easy to miss: no material credit rating covenants, and cash that cannot readily leave the country it sits in.

**Assertions (1)**

1. In March 2024 the Board authorized the repurchase of up to $15.0 billion of common stock, under which shares may be repurchased on the open market.

   *backed by* `asmt-0028`

**Related topics** `borrowings`, `credit ratings`, `share repurchase`, `liquidity`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0044`

**Traceability** — idempotency key `dd7eb250f5ac8cb3b7b1c273c46dfc6079fecfa600a7ec0537226cef10ee578b` · queue event `q-dd7eb250f5ac8cb3` · audits `audit-cand-013`

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

### 14. Free cash flow, geography, and what GE does not report by segment

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-014-r1` v2

**Slug** `free-cash-flow-geography-and-what-ge-does-not-report-by-segment`

The non-GAAP reconciliation, the fact that most revenue is earned outside the US, and the stated absence of segment assets.

**Assertions (1)**

1. In the fourth quarter of 2025 GE repurchased 6,404 thousand shares at an average price of $313.29, all as part of the announced programme, with approximately $2,698 million remaining available. GE Aerospace common stock is listed on the New York Stock Exchange, and as of January 15, 2026 there were approximately 215,000 shareholder accounts of record.

   *backed by* `asmt-0069`

**Related topics** `free cash flow`, `geographic revenue`, `segment reporting`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0024</code> — table, exact, not cited</summary>

| Period | Total number of shares purchased | Average price paid per share |   | Total number of shares purchased as part of our share repurchase authorization | Approximate dollar value of shares that may yet be purchased under our share repurchase authorization |   |
|---|---|---|---|---|---|---|
| (Shares in thousands) |   |   |   |   |   |   |
| 2025 |   |   |   |   |   |   |
| October | 306 |   | $313.34 | 306 |   |   |
| November | 5,389 | 316.09 |   | 5,389 |   |   |
| December | 710 | 291.98 |   | 710 |   |   |

*(1 further rows in the stored grid.)*

</details>

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0112`

**Traceability** — idempotency key `8f0f79b49d486f51670724fb2c3f536c8c5ff7e859d476a99f4286abc8249f17` · queue event `q-8f0f79b49d486f51` · audits `audit-cand-014`

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

### 15. GE Aerospace FY2025: the primary financial statements

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-015-r1` v2

**Slug** `ge-aerospace-fy2025-the-primary-financial-statements`

The headline figures of the filing, each cited to a CELL of the statement it comes from rather than to a quoted row. A 10-K prints three years side by side, so quoting `$8,698 $6,566 $9,445` proves the digits were copied and not that they were assigned to the right year; a cell reference resolves to the value and the year governing it.

**Assertions (4)**

1. GE Aerospace reported net income of $8,698 million for 2025, against $6,566 million in 2024 and $9,445 million in 2023 -- a 32% rise year on year and still below the 2023 figure.

   *backed by* `asmt-0001`

2. Cash from operating activities was $8,537 million in 2025, against $4,710 million in 2024 and $5,189 million in 2023 -- an 81% increase over the prior year and the highest of the three years reported.

   *backed by* `asmt-0001`

3. GE Aerospace's effective income tax rate for 2025 was 14.1%, on tax of $1,405 million, against a U.S. federal statutory rate of 21.0% -- a gap of 6.9 percentage points reconciled line by line in the filing.

   *backed by* `asmt-0001`

4. The principal pension plan's benefit obligation stood at $23,925 million at December 31, 2025, with other pension plans at $3,424 million and principal retiree benefit plans at $1,135 million.

   *backed by* `asmt-0001`

**Related topics** `GE Aerospace 2025 results: revenue, profit and backlog`, `GE's tax rate, and the businesses it no longer runs`

**Labels**

- Attach the label(s) named in the findings.

**Assets carried with this entry (7)** — 7 table. 3 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0009</code> — table, exact</summary>

| Sales in units, except where noted | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines | 2,386 | 1,911 | 2,075 |
| LEAP Engines(a) | 1,802 | 1,407 | 1,570 |
| Internal shop visit revenue growth % | 24% | 19% | 27% |
| (a) LEAP engines, which are in a significant production ramp, are a subset of Commercial Engines. |   |   |   |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0028</code> — table, exact</summary>

**STATEMENT OF CASH FLOWS**

| STATEMENT OF CASH FLOWS |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Net income (loss) | $8,698 | $6,566 | $9,445 |
| Net (income) loss from discontinued operations activities | (103) | 91 | 3 |
| Adjustments to reconcile net income (loss) to cash from (used for) operating activities: |   |   |   |
| Depreciation and amortization of property, plant and equipment (Note 6) | 863 | 834 | 797 |

*(48 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0030</code> — table, exact, not cited</summary>

**STATEMENT OF CHANGES IN SHAREHOLDERS' EQUITY**

| STATEMENT OF CHANGES IN SHAREHOLDERS' EQUITY |   |   |   |
|---|---|---|---|
| For the years ended December 31 (In millions) | 2025 | 2024 | 2023 |
| Common stock issued | $15 | $15 | $15 |
| Beginning balance | (3,861) | (6,150) | (2,272) |
| Currency translation adjustments | (43) | 2,151 | 2,270 |
| Benefit plans | (882) | (1,120) | (4,745) |

*(20 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0060</code> — table, exact</summary>

**PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME)**

| PLAN FUNDED STATUS AND AMOUNTS RECORDED IN ACCUMULATED OTHER COMPREHENSIVE LOSS (INCOME) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|   | 2025 |   |   |   |   |   |   |   | 2024 |   |   |   |   |   |
|   | Principal pension |   |   | Other pension |   | Principal retiree benefit |   |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Change in benefit obligations |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Balance at January 1 |   | $23,824 |   |   | $3,140 |   | $1,202 |   |   | $36,217 |   | $10,377 |   | $2,055 |
| Service cost | 59 |   |   | 2 |   | 13 |   |   | 71 |   | 22 |   | 13 |   |

*(28 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0064</code> — table, exact, not cited</summary>

**COST OF POSTRETIREMENT BENEFIT PLANS AND CHANGES IN OTHER COMPREHENSIVE INCOME**

| COST OF POSTRETIREMENT BENEFIT PLANS AND CHANGES IN OTHER COMPREHENSIVE INCOME |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| For the years ended December 31 | 2025 |   |   |   |   |   | 2024 |   |   |   |   |   | 2023 |   |   |   |   |   |
| (Pre-tax) | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   | Principal pension |   | Other pension |   | Principal retiree benefit |   |
| Cost (income) of postretirement benefit plans |   | $(655) |   | $(2) |   | $(66) |   | $(741) |   | $(21) |   | $(101) |   | $(1,108) |   | $(118) |   | $(144) |
| Changes in other comprehensive loss (income) |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |   |
| Prior service cost (credit) - current year | 36 |   | 135 |   | (5) |   | — |   | — |   | — |   | 49 |   | — |   | — |   |

*(8 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0068</code> — table, exact</summary>

| RECONCILIATION OF U.S. FEDERAL STATUTORY INCOME TAX RATE TO EFFECTIVE INCOME TAX RATE | 2025 |   |   |
|---|---|---|---|
|   | Amount |   | Rate |
| U.S. federal statutory income tax rate |   | $2,100 | 21.0% |
| State and local income taxes, net of federal income tax effect(a) | 74 |   | 0.7% |
| Foreign tax effects: |   |   |   |
| Singapore |   |   |   |

*(15 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0092</code> — table, exact, not cited</summary>

| December 31 | 2025 | 2024 |
|---|---|---|
| U.S. | $5,736 | $5,166 |
| Non-U.S. |   |   |
| Europe | 1,257 | 1,171 |
| Asia | 505 | 497 |
| Americas | 479 | 431 |

*(3 further rows in the stored grid.)*

</details>

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0113`, `u-src-ge-10k-fy2025-a73b722f-0114`, `u-src-ge-10k-fy2025-a73b722f-0115`, `u-src-ge-10k-fy2025-a73b722f-0116`

**Traceability** — idempotency key `01d567bfc6d72b9171ee7630bd9e00b7cbf39bcab77b482b1f6a534e1a1211a4` · queue event `q-01d567bfc6d72b91` · audits `audit-cand-015`

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

### 16. GE Aerospace 2025 results: revenue, profit and backlog

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-016-r1` v2

**Slug** `ge-aerospace-2025-results-revenue-profit-and-backlog`

The year's figures with the drivers the filing states for them, including the backlog's service-heavy composition and the one-off gain that makes 2023 look better than 2024.

**Assertions (1)**

1. Separation costs were $202 million in 2025 against $492 million in 2024 and $692 million in 2023, and during the fourth quarter of 2025 GE substantially completed separation-related restructuring activity.

   *backed by* `asmt-0079`

**Related topics** `revenue`, `segment profit`, `remaining performance obligation`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0015</code> — table, exact, not cited</summary>

| REVENUE AND OPERATING PROFIT (COST) | 2025 | 2024 | 2023 |
|---|---|---|---|
| Insurance revenue (Note 12) | $3,533 | $3,581 | $3,389 |
| Eliminations and other | (1,546) | (1,239) | (857) |
| Corporate & Other revenue | $1,987 | $2,343 | $2,532 |
| Gains (losses) on purchases and sales of business interests | 5 | 398 | (104) |
| Gains (losses) on retained and sold ownership interests and other equity securities (Note 19) | 312 | 532 | 5,776 |

*(13 further rows in the stored grid.)*

</details>

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0032`

**Traceability** — idempotency key `20a8662003b80f7556430532786e5bcbbaaec3b626d8c21af819506a4e201145` · queue event `q-20a8662003b80f75` · audits `audit-cand-016`

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

### 17. GE's run-off insurance book and what its assumptions are worth

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-017-r1` v2

**Slug** `ge-s-run-off-insurance-book-and-what-its-assumptions-are-worth`

The long-term care reserves, the policy characteristics that make the tail long, and the quantified sensitivities -- the only place in the filing that states what an assumption change costs in dollars.

**Assertions (1)**

1. The run-off insurance subsidiaries are required to prepare statutory financial statements in accordance with statutory accounting practices, which differ from the GAAP basis used in the consolidated financial statements.

   *backed by* `asmt-0084`

**Related topics** `long-term care insurance`, `sensitivity analysis`, `reserves`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0057`

**Traceability** — idempotency key `8a1ac68b80e3f19d1cc6069a716b92aac500c461dccecb9f6f97d37145f9ec9c` · queue event `q-8a1ac68b80e3f19d` · audits `audit-cand-017`

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

### 18. Risks GE discloses that carry a mechanism

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-018-r1` v2

**Slug** `risks-ge-discloses-that-carry-a-mechanism`

The risk factors reduced to the ones stating something checkable: sector concentration, product quality costs already incurred, supplier qualification time, and the possibility that a completed tax-free separation is later determined taxable.

**Assertions (1)**

1. GE organizes its risk factors into four categories: strategic, operational, financial, and legal and compliance.

   *backed by* `asmt-0089`

**Related topics** `risk factors`, `product safety`, `supply chain`, `spin-offs`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0062`

**Traceability** — idempotency key `a66c4a552a17d1f9cdc3d93fcda988fac128ef900a197607aee692f43802a1bc` · queue event `q-a66c4a552a17d1f9` · audits `audit-cand-018`

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

### 19. GE's accounting policies: how the numbers are made

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-019-r1` v2

**Slug** `ge-s-accounting-policies-how-the-numbers-are-made`

The definition-shaped part of the filing. Service revenue is recognized against an estimate of total costs, so the estimate is the revenue; CFM International sits outside the consolidated statements; fair values divide between quoted price and internal model.

**Assertions (2)**

1. GE states it believes presenting non-GAAP financial measures provides management and investors useful measures to evaluate performance and trends of the total company, and that in its analysis it sometimes uses information derived from consolidated financial data but not presented in its GAAP financial statements.

   *backed by* `asmt-0100`

2. The consolidated financial statements of GE Aerospace are prepared in conformity with US generally accepted accounting principles.

   *backed by* `asmt-0101`

**Related topics** `revenue recognition`, `equity method`, `fair value`, `hedge accounting`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0055</code> — table, exact, not cited</summary>

| December 31, 2024 |   |   |   |   |   |
|---|---|---|---|---|---|
| Future policy benefit reserves | $24,675 | $8,426 | $1,018 | $357 | $34,476 |
| Investment contracts | — | 719 | — | 621 | 1,340 |
| Other | — | — | 116 | 277 | 394 |
| Total | $24,675 | $9,145 | $1,134 | $1,254 | $36,209 |

</details>

**Source units (2)** `u-src-ge-10k-fy2025-a73b722f-0090`, `u-src-ge-10k-fy2025-a73b722f-0091`

**Traceability** — idempotency key `ed178df0c54cca4d7a7aaef7e65d1feea3efb07e840ebeaa5358d68975e13db0` · queue event `q-ed178df0c54cca4d` · audits `audit-cand-019`

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

### 20. Legal, environmental and indemnification exposures GE retains

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-020-r1` v2

**Slug** `legal-environmental-and-indemnification-exposures-ge-retains`

Obligations that outlived the businesses that created them: shareholder litigation running since 2018, roughly $190 million a year of remediation, indemnities to separated companies, and the warranty provision.

**Assertions (1)**

1. GE states that in the normal course of business it is involved from time to time in various arbitrations, class actions, commercial litigation and investigations.

   *backed by* `asmt-0106`

**Related topics** `shareholder litigation`, `environmental remediation`, `indemnification`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0102`

**Traceability** — idempotency key `ebdf3d4c81f904eef80be2169fac51706f0d13dbc8b4cf9bd435817747d3fb54` · queue event `q-ebdf3d4c81f904ee` · audits `audit-cand-020`

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

### 21. GE Aerospace: what the business is and how it is regulated

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-021-r1` v2

**Slug** `ge-aerospace-what-the-business-is-and-how-it-is-regulated`

The company, its two segments, its customers and the certification regime it operates under. Commercial Engines & Services is roughly three quarters of revenue and three quarters of that is services, so this is an installed-base business; engines run for decades after sale.

**Assertions (7)**

1. Commercial aircraft engine design and production are regulated by the FAA and EASA. To obtain and maintain design approvals -- type certificates -- GE must meet stringent certification requirements and maintain ongoing responsibility for the continued operational safety and airworthiness of its engines. It also holds an FAA production certificate, under which engines produced must meet the approved type design, and its MRO facilities hold repair station certificates from multiple aviation regulators.

   *backed by* `asmt-0072`

2. General Electric Company operates as GE Aerospace. It serves customers in approximately 120 countries, with manufacturing and service operations at 70 facilities in 23 US states and Puerto Rico (24 owned) and 62 facilities in 23 other countries (30 owned).

   *backed by* `asmt-0001`

3. CES customers consist primarily of airframers and airlines, including both Boeing and Airbus, and third-party MRO shops to whom GE sells spare parts and licenses MRO technology.

   *backed by* `asmt-0070`

4. GE Aerospace states that while its intellectual property rights in the aggregate are important, it does not believe its business is materially dependent on any single patent or licence. It licenses IP to commercial customers to support maintenance and repair of its products, and government customers may hold licences to IP developed or used under government contracts.

   *backed by* `asmt-0071`

5. The US government and other government customers often have the ability to modify, curtail or terminate their contracts and subcontracts with GE either at their convenience or for default based on performance.

   *backed by* `asmt-0001`

6. GE Aerospace is subject to international trade controls and sanctions regulations from governments and regulatory bodies around the world, including export controls.

   *backed by* `asmt-0074`

7. GE retains legacy business operations from its history across many industries, including operations related to its former financial services business.

   *backed by* `asmt-0075`

**Related topics** `GE Aerospace`, `segments`, `FAA certification`, `aftermarket`

**Assets carried with this entry (2)** — 2 table. 2 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0067</code> — table, exact, not cited</summary>

| PROVISION (BENEFIT) FOR INCOME TAXES | 2025 | 2024 | 2023 |
|---|---|---|---|
| Current |   |   |   |
| U.S. Federal | $671 | $310 | $(588) |
| Non-U.S. | 709 | 423 | 314 |
| U.S. State | (72) | 48 | 134 |
| Deferred |   |   |   |

*(4 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0090</code> — table, exact, not cited</summary>

| EXPENSES, PROFIT AND INCOME For the years ended December 31 | 2025 | 2024 | 2023 |
|---|---|---|---|
| Commercial Engines & Services |   |   |   |
| Cost of revenue | $21,998 | $17,703 | $16,575 |
| Selling, general and administrative expenses | 1,845 | 1,678 | 1,386 |
| Research and development | 1,287 | 993 | 736 |
| Other segment expenses (income)(a) | (677) | (548) | (484) |

*(19 further rows in the stored grid.)*

</details>

**Source units (7)** `u-src-ge-10k-fy2025-a73b722f-0012`, `u-src-ge-10k-fy2025-a73b722f-0001`, `u-src-ge-10k-fy2025-a73b722f-0004`, `u-src-ge-10k-fy2025-a73b722f-0009`, `u-src-ge-10k-fy2025-a73b722f-0013`, `u-src-ge-10k-fy2025-a73b722f-0014`, `u-src-ge-10k-fy2025-a73b722f-0015`

**Traceability** — idempotency key `09c58d8ede381000e1f17168e5c199ba41685d04a6f82cf06ba74b5deec6d030` · queue event `q-09c58d8ede381000` · audits `audit-cand-021`

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

### 22. GE's tax rate, and the businesses it no longer runs

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-022-r1` v2

**Slug** `ge-s-tax-rate-and-the-businesses-it-no-longer-runs`

Why the effective rate sits far below the US statutory rate, what was actually paid in cash, and the exposures retained through discontinued operations.

**Assertions (1)**

1. Interest and other financial charges were $0.8 billion in 2025 against $1.0 billion in each of 2024 and 2023.

   *backed by* `asmt-0080`

**Related topics** `effective tax rate`, `discontinued operations`, `Bank BPH`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0036`

**Traceability** — idempotency key `f42237fab207007b4db9db416948fcf75556c8bc1abd26827ac5be51a53538ef` · queue event `q-f42237fab207007b` · audits `audit-cand-022`

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

### 23. GE's capital structure, liquidity and its stated financial policy

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-023-r1` v2

**Slug** `ge-s-capital-structure-liquidity-and-its-stated-financial-policy`

Borrowings, ratings, the buyback authorization and two qualifications that are easy to miss: no material credit rating covenants, and cash that cannot readily leave the country it sits in.

**Assertions (3)**

1. Substantially all of the company's debt agreements in place at December 31, 2025 do not contain material credit rating covenants, and the unused back-up revolving syndicated credit facility contains a customary covenant.

   *backed by* `asmt-0083`

2. GE Aerospace states a commitment to maintaining strong investment grade ratings with a disciplined capital allocation strategy.

   *backed by* `asmt-0081`

3. GE's credit ratings at the time of filing were A3 long-term and P-2 short-term from Moody's with a positive outlook, and A- long-term and A-2 short-term from S&P with a stable outlook.

   *backed by* `asmt-0082`

**Related topics** `borrowings`, `credit ratings`, `share repurchase`, `liquidity`

**Source units (3)** `u-src-ge-10k-fy2025-a73b722f-0042`, `u-src-ge-10k-fy2025-a73b722f-0040`, `u-src-ge-10k-fy2025-a73b722f-0041`

**Traceability** — idempotency key `4621be0a42fe9194ea8f08c58f4bcad08df798a3a240b5847555cc25386b1f52` · queue event `q-4621be0a42fe9194` · audits `audit-cand-023`

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

### 24. GE's accounting policies: how the numbers are made

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-024-r1` v2

**Slug** `ge-s-accounting-policies-how-the-numbers-are-made`

The definition-shaped part of the filing. Service revenue is recognized against an estimate of total costs, so the estimate is the revenue; CFM International sits outside the consolidated statements; fair values divide between quoted price and internal model.

**Assertions (4)**

1. Loss contingencies are defined as existing conditions, situations or circumstances involving uncertainty as to possible loss that will ultimately be resolved when future events occur.

   *backed by* `asmt-0098`

2. GE enters into collaborative arrangements with manufacturers and suppliers of components used to build and maintain certain engines, and holds equity method investments in entities where it does not have a controlling financial interest but has significant influence -- the most significant related-party transactions being with CFM International, a non-consolidated company jointly owned.

   *backed by* `asmt-0096`

3. Inventories are stated at the lower of cost or realizable values, with cost primarily determined using the average cost method. Property, plant and equipment is generally depreciated on a straight-line basis over its estimated economic life.

   *backed by* `asmt-0097`

4. GE evaluates supply chain finance programs to ensure that where a third-party intermediary is used to settle trade payables, the intermediary's involvement does not change the nature of the payable.

   *backed by* `asmt-0099`

**Related topics** `revenue recognition`, `equity method`, `fair value`, `hedge accounting`

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0084`, `u-src-ge-10k-fy2025-a73b722f-0079`, `u-src-ge-10k-fy2025-a73b722f-0081`, `u-src-ge-10k-fy2025-a73b722f-0086`

**Traceability** — idempotency key `ef17c0e277cac053f335812f7c9bd8210aa83c7fbb56ebc6f1f87eb58377cf45` · queue event `q-ef17c0e277cac053` · audits `audit-cand-024`

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

### 25. Operating conditions GE reports as fact, not contingency

`create_or_update` · knowledge state **internal-observation** · status `ready` · candidate `cand-025-r1` v2

**Slug** `operating-conditions-ge-reports-as-fact-not-contingency`

Supply disruption and tariff cost are stated in the indicative -- have impacted, will result -- and the investments made against them are quantified.

**Assertions (2)**

1. GE invested $1 billion in US manufacturing and hired 5,000 US workers in 2025, and is separately investing $1 billion to increase MRO capacity, including $500 million to increase capacity in one named facility.

   *backed by* `asmt-0076`

2. GE states it operates in a highly dynamic tariff environment and that, given its global business, tariffs will result in additional cost for GE and its suppliers.

   *backed by* `asmt-0077`

**Related topics** `supply chain`, `tariffs`, `capital investment`

**Source units (2)** `u-src-ge-10k-fy2025-a73b722f-0017`, `u-src-ge-10k-fy2025-a73b722f-0018`

**Traceability** — idempotency key `6b229840466b7888dbbbcf72f3928aed2518fe87154fd846c7e6325d70243ca9` · queue event `q-6b229840466b7888` · audits `audit-cand-025`

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

### 26. GE Aerospace 2025 results: revenue, profit and backlog

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-026-r1` v2

**Slug** `ge-aerospace-2025-results-revenue-profit-and-backlog`

The year's figures with the drivers the filing states for them, including the backlog's service-heavy composition and the one-off gain that makes 2023 look better than 2024.

**Assertions (1)**

1. In 2025 GE announced an Indefinite Delivery/Indefinite Quantity contract from the US Air Force valued up to $5 billion to support foreign military sales for F110-GE-129 engines.

   *backed by* `asmt-0078`

**Related topics** `revenue`, `segment profit`, `remaining performance obligation`

**Source units (1)** `u-src-ge-10k-fy2025-a73b722f-0029`

**Traceability** — idempotency key `901253b8d3874a38bd9564168efbb92f2d108189408dc179972f2cb6ec38caea` · queue event `q-901253b8d3874a38` · audits `audit-cand-026`

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

### 27. GE's cybersecurity framework, governance and disclosed incidents

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-027-r1` v2

**Slug** `ge-s-cybersecurity-framework-governance-and-disclosed-incidents`

The Item 1C disclosure: named processes, Audit Committee oversight, and the admission that attacks have occurred and are expected to continue.

**Assertions (4)**

1. GE Aerospace has developed and implemented a cybersecurity framework intended to assess, identify and manage risks from threats to the security of its information and systems.

   *backed by* `asmt-0085`

2. GE's stated cybersecurity processes include risk-based controls for information systems, a cybersecurity incident response plan with dedicated response teams and testing, security awareness training with additional role-based training, third-party risk assessments of suppliers, and engagement of external cybersecurity companies to periodically assess its posture.

   *backed by* `asmt-0086`

3. The Audit Committee of the GE Aerospace Board is responsible for board-level oversight of cybersecurity risk and reports back to the Board, while management is ultimately responsible for assessing and managing cybersecurity risk, with the CIO leading the company's overall cybersecurity effort.

   *backed by* `asmt-0087`

4. GE states it has experienced, and expects to continue to experience, cyberattacks of varying degrees of sophistication and various cybersecurity incidents, such as distributed denial of service attacks.

   *backed by* `asmt-0001`

**Related topics** `cybersecurity`, `governance`, `incidents`

**Assets carried with this entry (1)** — 1 table. 1 of them travels because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0024</code> — table, exact, not cited</summary>

| Period | Total number of shares purchased | Average price paid per share |   | Total number of shares purchased as part of our share repurchase authorization | Approximate dollar value of shares that may yet be purchased under our share repurchase authorization |   |
|---|---|---|---|---|---|---|
| (Shares in thousands) |   |   |   |   |   |   |
| 2025 |   |   |   |   |   |   |
| October | 306 |   | $313.34 | 306 |   |   |
| November | 5,389 | 316.09 |   | 5,389 |   |   |
| December | 710 | 291.98 |   | 710 |   |   |

*(1 further rows in the stored grid.)*

</details>

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0058`, `u-src-ge-10k-fy2025-a73b722f-0059`, `u-src-ge-10k-fy2025-a73b722f-0060`, `u-src-ge-10k-fy2025-a73b722f-0061`

**Traceability** — idempotency key `4e78f48d6872300ccbb3b3a5cf01b09b817cf1bcb4b19ebf423fcf86eb8a6a39` · queue event `q-4e78f48d6872300c` · audits `audit-cand-027`

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

### 28. Risks GE discloses that carry a mechanism

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-028-r1` v2

**Slug** `risks-ge-discloses-that-carry-a-mechanism`

The risk factors reduced to the ones stating something checkable: sector concentration, product quality costs already incurred, supplier qualification time, and the possibility that a completed tax-free separation is later determined taxable.

**Assertions (4)**

1. GE states that its financial performance is dependent on the condition of the commercial aviation sector and on its partners, suppliers and customers in that sector.

   *backed by* `asmt-0001`

2. GE states it may face risks related to refinancing its debt, particularly in severely adverse market conditions, and that future credit rating downgrades could adversely affect it.

   *backed by* `asmt-0001`

3. GE states that cybersecurity and data privacy laws are rapidly evolving, vary significantly by country and present increasing compliance challenges, and that it periodically receives regulatory inquiries.

   *backed by* `asmt-0001`

4. GE states its business and financial performance may be adversely affected by climate and environmental factors, including changes in regulations and customer demand, and that it faces increasing demand for transitioning to lower emission technologies.

   *backed by* `asmt-0001`

**Related topics** `risk factors`, `product safety`, `supply chain`, `spin-offs`

**Source units (4)** `u-src-ge-10k-fy2025-a73b722f-0063`, `u-src-ge-10k-fy2025-a73b722f-0068`, `u-src-ge-10k-fy2025-a73b722f-0069`, `u-src-ge-10k-fy2025-a73b722f-0070`

**Traceability** — idempotency key `d392c07749deb1f8e3149a6d1ad49c0908105087dee6d56e11b7b25906af3ff1` · queue event `q-d392c07749deb1f8` · audits `audit-cand-028`

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

### 29. Internal control, the auditor, and the two critical audit matters

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-029-r1` v2

**Slug** `internal-control-the-auditor-and-the-two-critical-audit-matters`

Management's Section 404 conclusion and the auditor's own account of where the estimates are hardest -- which lands on the same two areas the filing discloses the most sensitivity about.

**Assertions (2)**

1. Management concluded that GE's internal control over financial reporting was effective as of December 31, 2025, and the independent registered public accounting firm issued an audit report on internal control over financial reporting.

   *backed by* `asmt-0094`

2. GE engaged Deloitte & Touche LLP as its independent registered public accounting firm, which has served as the company's auditor since 2020. Its reports are dated January 29, 2026 and issued from Cincinnati, Ohio.

   *backed by* `asmt-0095`

**Related topics** `internal control`, `Deloitte`, `critical audit matters`

**Source units (2)** `u-src-ge-10k-fy2025-a73b722f-0071`, `u-src-ge-10k-fy2025-a73b722f-0072`

**Traceability** — idempotency key `08cf53b375a25f7675914ec9f1a80fb64644bdb19897b94dd3e15992184fdf52` · queue event `q-08cf53b375a25f76` · audits `audit-cand-029`

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

### 30. Forward-looking qualifications and who signs the filing

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-030-r1` v2

**Slug** `forward-looking-qualifications-and-who-signs-the-filing`

The safe-harbour statement, including an explicit refusal to update, and the officers and committee that certify the accounts.

**Assertions (5)**

1. GE states that the uncertainties it lists may cause actual future results to be materially different from those expressed in its forward-looking statements, that it does not undertake to update those statements, and that the document includes forward-looking projected financial information based on current estimates and forecasts whose actual results could differ materially.

   *backed by* `asmt-0001`

2. Among the uncertainties GE lists for its forward-looking statements are changes in law, regulation or policy such as trade policy and tariffs, government defense priorities or budgets, environmental or climate regulation, and the effects of tax law changes or audits.

   *backed by* `asmt-0001`

3. GE also lists as uncertainties the impact of regulation, government investigations, regulatory, commercial and legal proceedings or disputes, environmental, health and safety matters, and the impact related to information technology, cybersecurity or data security breaches at GE Aerospace or third parties.

   *backed by* `asmt-0001`

4. H. Lawrence Culp, Jr. is Chairman and Chief Executive Officer and Rahul Ghai is Chief Financial Officer; both signed the management report dated January 29, 2026. Christian Meisner is Senior Vice President & Chief Human Resources Officer.

   *backed by* `asmt-0105`

5. The Board of Directors, through its Audit Committee, which consists entirely of independent directors, meets periodically with management, internal auditors and the independent registered public accounting firm.

   *backed by* `asmt-0001`

**Related topics** `forward-looking statements`, `governance`, `Audit Committee`

**Assets carried with this entry (3)** — 3 table. 3 of them travel because it sits in this entry's text, not because a unit quoted it.

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0025</code> — table, exact, not cited</summary>

| /s/ H. Lawrence Culp, Jr. | /s/ Rahul Ghai |
|---|---|
| H. Lawrence Culp, Jr. | Rahul Ghai |
| Chairman and Chief Executive Officer | Chief Financial Officer |
| January 29, 2026 |   |

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0096</code> — table, exact, not cited</summary>

**Date assumed**

| Date assumed |   |   |   |
|---|---|---|---|
| Executive |   |   |   |
| Name | Position | Age | Officer Position |
| H. Lawrence Culp, Jr. | Chairman of the Board & Chief Executive Officer | 62 | October 2018 |
| Rahul Ghai | Senior Vice President & Chief Financial Officer | 54 | September 2023 |
| Mohamed Ali | Senior Vice President & Chief Technology & Operations Officer(a) | 56 | January 2025 |

*(6 further rows in the stored grid.)*

</details>

<details><summary><code>tbl-src-ge-10k-fy2025-a73b722f-0100</code> — table, exact, not cited</summary>

|   | Signer | Title | Date |
|---|---|---|---|
|   | /s/ Rahul Ghai | Principal Financial Officer | January 29, 2026 |
|   | Rahul GhaiSenior Vice President and Chief Financial Officer |   |   |
|   | /s/ Robert Giglietti | Principal Accounting Officer | January 29, 2026 |
|   | Robert GigliettiVice President, Chief Accounting Officer, Controller and Treasurer |   |   |
|   | /s/ H. Lawrence Culp, Jr. | Principal Executive Officer | January 29, 2026 |

*(14 further rows in the stored grid.)*

</details>

**Source units (5)** `u-src-ge-10k-fy2025-a73b722f-0092`, `u-src-ge-10k-fy2025-a73b722f-0093`, `u-src-ge-10k-fy2025-a73b722f-0094`, `u-src-ge-10k-fy2025-a73b722f-0095`, `u-src-ge-10k-fy2025-a73b722f-0096`

**Traceability** — idempotency key `fab4d0bd38690c9d2896b2ee4e764e65946f2be68b69a36f7c60e7658f17fa9e` · queue event `q-fab4d0bd38690c9d` · audits `audit-cand-030`

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

### 31. Legal, environmental and indemnification exposures GE retains

`create_or_update` · knowledge state **authoritative** · status `ready` · candidate `cand-031-r1` v2

**Slug** `legal-environmental-and-indemnification-exposures-ge-retains`

Obligations that outlived the businesses that created them: shareholder litigation running since 2018, roughly $190 million a year of remediation, indemnities to separated companies, and the warranty provision.

**Assertions (2)**

1. Since February 2018 multiple shareholder derivative lawsuits have been filed against current and former GE executive officers and board members, and in July 2018 a putative class action -- the Mahar case -- was filed in New York state court naming GE, former GE executive officers and a former board member among the defendants.

   *backed by* `asmt-0001`

2. GE's operations involve or have involved the use, disposal and cleanup of substances regulated under environmental protection laws. Expenditures for site remediation and worker exposure claims were approximately $190 million in 2025, $175 million in 2024 and $246 million in 2023.

   *backed by* `asmt-0001`

**Related topics** `shareholder litigation`, `environmental remediation`, `indemnification`

**Source units (2)** `u-src-ge-10k-fy2025-a73b722f-0103`, `u-src-ge-10k-fy2025-a73b722f-0104`

**Traceability** — idempotency key `4b7758fcb36009dce31888d33d1d4d6c515e58dfbd5a78700dbb6bdbc8f04796` · queue event `q-4b7758fcb36009dc` · audits `audit-cand-031`

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
