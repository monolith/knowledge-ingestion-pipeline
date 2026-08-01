# Pipeline Design Verification Research — Full Verified Claims

**Date:** 2026-07-30/31
**Subject:** Adversarial verification of the 7-pass knowledge-ingestion pipeline design
(spec: the v2.0 baseline specification)
**Method:** Multi-agent research fan-out across 5 angles → 3-vote adversarial verification per claim.
21 claims confirmed, 4 refuted. Votes shown as confirm-refute.

**Coverage note:** Surviving claims cover angle 1 (atomic extraction) and angle 2
(routing/retrieval) almost exclusively. Angles 3 (relationship classification), 4
(verification/audit), and 5 (production engineering) produced no surviving claims in this
round — those spec passes (3, 5, 6) remain research-unverified.

---

## Theme A — Atomicity & extraction granularity (Pass 1)

### A1. Dense X Retrieval atomicity rubric — CONFIRMED 3-0
**Source:** https://arxiv.org/abs/2312.06648 (Chen et al., EMNLP 2024 main)
Operational proposition criteria: distinct meaning, minimality (cannot be further split),
self-containment/contextualization. Quote verified verbatim in Section 2. A concrete,
citable rubric Pass 1 can align with. Nuance: the paper's own error analysis shows LLM
extractors violate minimality/self-containment in practice.
**Note:** the companion claim that proposition-level *indexing* beats passage-level for
dense retrieval was REFUTED 0-3 — do not cite Dense X as evidence for atomic units as the
pipeline's base retrieval representation.

### A2. Naive decompose-decontextualize-verify loses context — CONFIRMED 3-0
**Source:** https://aclanthology.org/2025.emnlp-main.905/ (VeriFact, Liu et al., EMNLP 2025)
FActScore-style pipelines "often fail to capture essential context and miss key relational
facts." Corroborated: DnDScore (arXiv 2412.13175), Decomposition Dilemmas (arXiv 2411.02400).
Scope caveat: holds for *naive* atomization; decomposition per se can help in some settings.

### A3. Molecular Facts: fully atomic is the wrong representation — CONFIRMED 3-0 (×3 claims)
**Source:** https://aclanthology.org/2024.findings-emnlp.215/ (Gunjal & Durrett, EMNLP Findings 2024)
- Documented granularity tension: atomic facts are easier to check but lack context to
  interpret correctly.
- Explicit position: "fully atomic facts are not the right representation." Criteria for
  molecular facts: decontextuality (stands alone) + minimality (least added info to get there).
- Empirical: molecular facts balance minimality against verification accuracy in ambiguous
  (entity-ambiguous) settings.
Corroborated by DnDScore, Decomposition Dilemmas, ACL 2025 arXiv 2503.15354, 2026 follow-ons
(arXiv 2602.10380). 2026 evidence-extraction work (PrimeFacts arXiv 2605.06006, SEEK
arXiv 2605.26755): decontextualized units give up to 30% relative MRR retrieval gains,
+10-20 Macro-F1 verdict prediction.

### A4. Decomposition Dilemmas: decomposition is not a pure win — CONFIRMED 3-0 (×2 claims)
**Source:** https://arxiv.org/abs/2411.02400 (Hu, Long & Wang, NAACL 2025 main)
- Trade-off: sub-claim accuracy gains offset by decomposition-introduced noise
  (over-fragmentation, context omission, semantic drift).
- Verifier-strength dependence (verified against the paper's tables): weak verifier on FELM
  — decomposition raises F1 48.10 → 67.51-68.12; strong verifier (Minicheck on WICE) — ALL
  decomposition methods underperform no-decomposition (F1 59.90-68.22 vs 72.32); GPT-4o-mini
  verifier degrades with decomposition (71.56 → 54.34-69.39).
- Implication: with strong LLMs in later passes, atomizing in Pass 1 may cost accuracy.
- Qualification: 2025-2026 follow-ups (DyDecomp arXiv 2503.15354; DAD arXiv 2602.21857,
  +6.24 macro-F1 via verifier-aligned GRPO decomposition; CREDENCE arXiv 2606.19819) show
  the trade-off is mitigable via tuned decomposition policies — not eliminated by default.

### A5. Claimify: atomicity deliberately excluded as a quality criterion — CONFIRMED 3-0 (×2 claims)
**Source:** https://arxiv.org/abs/2502.10855 (Metropolitansky & Larson, Microsoft Research, ACL 2025 main)
- Atomicity "lacks a clear endpoint"; prior works (Chen 2023a, Hu 2024a, Tang 2024) suggest
  it does not consistently improve fact-checking. Excluded from their evaluation framework.
- Their validated rubric: **entailment** + **coverage** (element-level; penalizes both
  omitted verifiable content AND included unverifiable content) + **decontextualization**.
  Human validation: 6,490 sentences, 3 annotators, Krippendorff's alpha 0.72 (0.86 high-conf).
- Mapping caveat: this maps onto the spec's 8.7 omission check and loosely onto
  evidence_strength≈entailment; it is NOT a dimension-for-dimension match with the 8.5
  scoring rubric, and must not be cited as validating Pass 1's atomicity rules.

---

## Theme B — Omission/completeness check (Pass 1)

### B1. VeriFact: explicit omission-resolution step measurably helps — CONFIRMED 2-1 + 3-0
**Source:** https://aclanthology.org/2025.emnlp-main.905/ (arXiv 2505.09701; code github.com/launchnlp/VeriFact)
Detect-and-refine (3 LLM judges flag incomplete facts + word-mapping finds missing
relational facts, then LLMs resolve): incomplete facts 22.5% vs 56.7% (SAFE best baseline);
coverage of human reference facts 87.1% vs 77.5% (SAFE) / 78.7% (VERIFY); 24.9% of refined
facts FLIPPED correctness label after incompleteness resolved. 1,168 facts, 4 human annotators.
Caveats: domain is factuality evaluation of LLM long-form output, not document ingestion —
mechanism-level evidence for the spec's omission check, not same-domain proof; multi-pass is
computationally expensive; arXiv 2603.28005 (Mar 2026) finds atomic-decomposition benefits
prompt-dependent in reference-grounded QA judging. Direct-support claim survived 2-1.

### B2. Comprehensiveness metrics: simple end-to-end LLM omission pass wins — CONFIRMED 3-0 (×3 claims)
**Source:** https://arxiv.org/abs/2510.07926 (Dejl et al., Imperial + IBM; ACL 2026 Findings)
- Three metric families compared: NLI atomic-statement decomposition, Q&A-pair extraction,
  end-to-end LLM missing-content detection.
- E2E beat both on WikiContradict (p<0.05); human eval: E2E 88% fully correct vs Q&A 66%,
  NLI 48%. Vs atomic-NLI specifically, E2E won everywhere reported.
- Trade-off (verbatim): "at the cost of reduced robustness, interpretability and result
  granularity" — E2E cross-evaluator-model std-dev 0.044 vs 0.009 (Q&A); E2E returns only
  covered/uncovered sets. On ConflictBank, Q&A beat E2E for some models.
- Corroborated: arXiv 2603.28005 — holistic judge matched/exceeded atomic judge on 2/3
  benchmarks, advantage "particularly pronounced in detecting incomplete answers."
Implication: the spec's LLM omission pass is viable without atomic-decomposition machinery,
but should report structured per-omission findings to recover interpretability.

---

## Theme C — Routing & retrieval (Pass 2)

### C1. Hybrid dense+BM25 beats embeddings alone — CONFIRMED 3-0
**Source:** https://www.anthropic.com/engineering/contextual-retrieval (Anthropic, 2024-09-19)
Embeddings miss exact-match strings (identifiers like "TS-999") that BM25 catches.
Corroborated academically: T2-RAGBench (arXiv 2604.01733, 2026; 23,088 queries — BM25+dense
RRF beats both constituents, +8.1pp Recall@5 on TAT-DQA); Wang et al. 2024 best-practices;
BEIR (Thakur et al. 2021). Qualification: TIFIN India @ SemEval-2025 (arXiv 2504.16627) —
BM25 fusion helped small embedders but REDUCED effectiveness with a top-tier embedder on one
task; treat fusion weighting as tunable.

### C2. Contextual Retrieval — evidence-backed technique ABSENT from spec — CONFIRMED 3-0
**Source:** https://www.anthropic.com/engineering/contextual-retrieval
Prepending LLM-generated chunk context before embedding+BM25 indexing cut top-20 retrieval
failure rate 49% (5.7% → 2.9%; 1-minus-recall@20; codebases/fiction/ArXiv/science).
Spec grep confirms no contextual-enrichment step in Pass 2 (section 9.2 routes on raw
embeddings+BM25). Independent: Merola & Singh, ECIR 2025 (arXiv 2504.19754) — direction
confirmed; AWS replications report smaller 5-15% precision gains. Vendor benchmark caveat.

### C3. LazyGraphRAG: eager LLM graph construction unnecessary — CONFIRMED 3-0, 2-1, 3-0 (×3 claims)
**Source:** https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ (Nov 2024, updated Jun 2025)
- Indexing cost identical to vector RAG, ~0.1% of full GraphRAG (NLP noun-phrase extraction
  + graph statistics; zero index-time LLM use).
- Comparable answer quality to GraphRAG Global Search on global queries at >700x lower query
  cost (Z500 vs C2 config; 5,590 AP articles) — survived 2-1.
- BenchmarkQED follow-up (Jun 2025): LazyGraphRAG won 96/96 LLM-judged comparisons vs
  GraphRAG local/global/DRIFT, vector RAG, LightRAG, RAPTOR, TREX.
Caveats: entirely vendor-internal, LLM-judged (win-rate, not correctness), no independent
replication — code unreleased as of Jul 2026 (graphrag discussion #1490); cost is shifted to
query time, not eliminated. Cite as "Microsoft reports."
**Refuted companion claim** (0-3): "at ~4% of query cost significantly outperforms all
competing methods on both local and global queries" — do not use.

### C4. Flat/dense RAG competitive for general QA; graph wins multi-hop — CONFIRMED 3-0 (×2 claims)
**Sources:** https://arxiv.org/pdf/2604.09666 (RAGSearch benchmark, Apr 2026);
corroborated by Han et al. arXiv 2502.11371 (Feb 2025)
- Agentic (multi-round, esp. RL-trained) search substantially improves dense RAG and narrows
  the gap to GraphRAG — graph structure is partly substitutable by iterative retrieval.
- Given GraphRAG's offline construction + latency overhead, dense RAG "remains a practical
  and competitive alternative for general QA scenarios." Han et al.: GraphRAG's average gain
  over dense RAG +0.47 on general QA vs +27.23 on multi-hop QA.
- Supports the spec's flat hybrid clustering in Pass 2 — UNLESS heavy cross-document
  multi-hop synthesis dominates the workload. Also note: graphs additionally win on global
  sensemaking/summarization, slightly beyond the multi-hop-only escape clause.
**Refuted companion claim** (1-2): the amortization-conditioned narrowing of GraphRAG's
advantage — treat the "only worthwhile when amortized" framing as unverified.

---

## Refuted claims (transparency)
1. Proposition-level indexing significantly beats passage-level for dense retrieval
   (arXiv 2312.06648) — 0-3.
2. Four systematic decomposition error types, three unchecked by the spec
   (arXiv 2411.02400) — 0-3.
3. LazyGraphRAG at ~4% query cost significantly outperforms all methods on local+global
   queries (Microsoft blog) — 0-3.
4. GraphRAG advantage specific to multi-hop + agentic stability, worthwhile only when
   amortized (arXiv 2604.09666) — 1-2.

---

## Design recommendations distilled from confirmed claims
1. **Redefine Pass 1 units as molecular, not maximally atomic**: decontextualized-but-minimal
   (Gunjal & Durrett criteria); drop atomicity as an end in itself (Claimify precedent);
   treat granularity as tunable against downstream verifier strength (Decomposition Dilemmas).
2. **Adopt Claimify's entailment / element-level coverage / decontextualization rubric** for
   Pass 1 extraction quality evaluation — it is human-validated and citable.
3. **Keep the separate omission/completeness check** (VeriFact evidence) and consider the
   simple end-to-end LLM form, but require structured per-omission output to offset the
   documented interpretability/robustness cost.
4. **Add contextual enrichment before Pass 2 indexing** (Anthropic Contextual Retrieval) —
   the one concrete evidence-backed technique the spec lacks.
5. **Keep flat hybrid clustering; skip eager graph construction.** If graph organization is
   ever needed (multi-hop-heavy workloads), prefer the LazyGraphRAG deferred pattern.
6. **Treat dense/sparse fusion weights as tunable** — hybrid gains can shrink or invert with
   top-tier embedding models.
