# Round 4 Design Verification — Grounding, Citation, (Structured Outputs / Long-Context / Prompt-Injection)

Research date: 2026-08-01
Pipeline spec: `/home/anatoly/knowledge_ingestion_pipeline_demo/docs/SPECIFICATION.md`
Method: multi-agent fan-out → 3-vote adversarial verification → synthesis.
Scope note: Round 4 was scoped to five angles — (1) groundedness/hallucination checkers, (2) citation/attribution verification, (3) structured outputs / constrained decoding, (4) long-context degradation & batch sizing, (5) indirect prompt-injection defense.

**IMPORTANT COVERAGE GAP:** Of the five angles, only (1) grounding checkers and (2) citation/attribution produced claims that survived 3-vote adversarial verification. Angles (3) structured outputs, (4) long-context/batch-sizing, and (5) prompt-injection produced **no surviving verified claims in this batch** and are therefore **unverified** here. The spec's §16 batch numbers (20–50 units, split >75; 30–50% context reservation) and §20 prompt-injection posture are **neither confirmed nor refuted** by this round. See Open Questions.

---

## Executive summary

For the spec's Pass 5 grounding check (§12.2 #1), the evidence is strong and actionable: a small specialized fact-checking model matches frontier-LLM grounding accuracy at roughly 400x lower cost and runs at ingestion-pipeline throughput (>500 checks/min on one mid-range GPU) — so the grounding pass should use a MiniCheck-class checker, not a frontier LLM-as-judge. For the Pass 5 citation-accuracy check (§12.2 #9), NLI-based entailment is the established automated method (ALCE), and it is worth having because LLM-generated citations fail verification at high rates without it (~50% of sentences fully supported in 2023 systems). But every automated attribution checker measured — NLI metrics, fine-tuned GPT-3.5, and even zero-shot GPT-4 — tops out at roughly 80–85% agreement with humans, i.e. about 1 in 5 individual citation judgments is wrong; the spec must treat citation-accuracy verdicts as probabilistic and lean on its raw-source-escalation step (§12.2 #10) for uncertain or high-impact claims rather than assuming near-perfect checking. Angles (3)–(5) remain unverified in this batch.

---

## Findings (synthesized)

### F1 — A small specialized checker matches frontier-LLM grounding accuracy at ~400x lower cost. [HIGH]
Merges claims [0][1][2][3][4][5]. Sources: arXiv:2404.10774 (MiniCheck, EMNLP 2024); https://llm-aggrefact.github.io/ (LLM-AggreFact leaderboard); https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B.

MiniCheck-FT5 (770M) "outperforms all systems of comparable size and reaches GPT-4 accuracy" at "400x lower cost" (paper body: 74.7 vs GPT-4 75.3 balanced accuracy; $0.24 vs $107 to check the 13K test set, ~445x). On the public leaderboard the ordering is confirmed and has strengthened under third-party evaluation: Bespoke-MiniCheck-7B 77.4 (rank 1) > Claude-3.5 Sonnet 77.2 > Granite Guardian 3.3 8B 76.5 > Mistral-Large-2 123B 76.5 > GPT-4o-2024-05-13 75.9. Even sub-1B checkers stay competitive: FactCG-DeBERTa-L 0.4B = 75.6 and MiniCheck-Flan-T5-L 0.8B = 75.0, both above Llama-3.1-405B-Instruct 74.4 (≈500–1000x larger). FactCG (arXiv:2501.17144, NAACL 2025 Findings) independently reports the same directional result from a different group.
Caveats: "GPT-4" = 2024-era model; leaderboard appears frozen ~late-2024/early-2025 and excludes 2025–2026 frontier models, so "beats frontier" is scoped to the models the benchmark evaluated; the 400x multiplier is pinned to April-2024 GPT-4 pricing and shrinks against cheaper current models; margins over the largest models are ~0.6–1.5 points (near noise). Leaderboard maintained by the MiniCheck authors, but built from 10–11 pre-existing third-party datasets with a public board, limiting cherry-pick risk.

### F2 — These checkers run at production ingestion volume cheaply. [HIGH]
Merges claim [6] + throughput portion of [10]. Sources: https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B; MiniCheck GitHub (Liyan06/MiniCheck); arXiv:2502.17125 (LettuceDetect).

Bespoke-MiniCheck-7B with vLLM and MiniCheck-Flan-T5-L both report ">500 docs/min" on a single A6000 (48GB). The MiniCheck repo corroborates: 29K-example test set in 30 min with prefix caching (~967/min) / 55 min without (~527/min). LettuceDetect reports 30–60 examples/sec on a single GPU. "docs/min" counts document–claim PAIR checks, so per-sentence grounding of an N-sentence output costs N checks — feasibility holds at tens of thousands of checks/hour on one mid-range GPU.
Caveats: Bespoke-MiniCheck is licensed CC BY-NC 4.0 (non-commercial; separate commercial licensing) — relevant if the pipeline is commercial. MiniCheck-Flan-T5 variants are the friendlier-license fallback.

### F3 — Per-claim (sentence/clause) entailment decomposition is the standard grounding architecture, and trained NLI checkers generalize out-of-distribution — but AlignScore specifically does NOT reach GPT-4. [HIGH]
Merges claims [7][8] + refuted-AlignScore nuance. Sources: arXiv:2305.16739 (AlignScore, ACL 2023); arXiv:2408.08067 (RAGChecker); amazon-science/RAGChecker + RefChecker.

AlignScore was evaluated on 22 datasets, 19 unseen in training, with "substantial improvement over a wide range of previous metrics" — real OOD generalization for a trained checker (the competing MiniCheck paper calls AlignScore "the existing SOTA specialized fact-checking model" and measures it at 70.4% on LLM-AggreFact). RAGChecker computes faithfulness by claim-level decomposition + per-claim entailment (Llama3-70B as extractor and checker via the open RefChecker framework) — fine-grained claim entailment, not holistic response scoring, is the chosen architecture; the official repo confirms "claim-level entailment operations for fine-grained evaluation."
Contradiction to note: the stronger claim that AlignScore (355M) *matches or outperforms GPT-4* factual-consistency was **REFUTED 0-3**. The small-checker-matches-GPT-4 result holds for MiniCheck/Bespoke-MiniCheck, not for AlignScore. AlignScore is a historical SOTA that has since been surpassed (MiniCheck-FT5 +~4.3%).

### F4 — Encoder token-classification detectors are a cheap alternative for grounding checks, but validated in-domain only and trail the best LLM detector. [MEDIUM]
Merges claims [9][10]. Source: arXiv:2502.17125 (LettuceDetect, Kovács & Recski, Feb 2025) + KRLabsOrg HF card.

LettuceDetect (ModernBERT token-classification) reaches 79.22% example-level F1 on RAGTruth, beating the prior encoder SOTA Luna (65.4) and most prompt-based LLM detectors (gpt-4-turbo prompt 63.4, SelfCheckGPT 58.8), while being ~30x smaller than the best models (396M vs 8–13B). It does NOT beat RAG-HAT (a DPO-tuned Llama-3-8B) at 83.9 — the "most prompt-based models" hedge is accurate.
Caveats: MEDIUM because (a) claim [9] was a 2-1 (split) vote — the paper's own "14.8% improvement over Luna" is an arithmetic error (true gap is 13.82 pts absolute / 21.1% relative), though the load-bearing 79.22 F1 and "beats prior encoder SOTA" verify; (b) evaluation is **in-domain only** (trained and tested on RAGTruth; no LLM-AggreFact-style OOD test), so cross-domain generalization is unproven; (c) self-reported tool-author preprint. Directionally corroborated by MiniCheck's small-model-matches-GPT-4-at-400x thesis.

### F5 — NLI entailment is the established automated method for citation/attribution verification. [HIGH]
Claim [11]. Source: arXiv:2305.14627 (ALCE, Gao et al., EMNLP 2023).

ALCE computes citation recall and precision automatically with the TRUE NLI model (T5-based entailment checker, Honovich et al. 2022). Citation recall = 1 iff at least one citation whose concatenation entails the statement; a citation is "irrelevant" for precision iff it alone does not entail the statement AND removing it still leaves the remaining citations entailing it. ALCE remains the standard citation-quality evaluation. Definitional fact, verified verbatim against the primary source.
Mechanism note for abstraction drift (spec §12.2 #8): citation *recall* is exactly the overclaiming detector — if a generated statement says more than its sources support, the source text fails to entail it and recall < 1.

### F6 — Automated attribution checkers cap at ~80–85% agreement with humans (~1 in 5 judgments wrong). Budget for a meaningful error rate. [HIGH]
Merges claims [12][14][15][16][20]. Sources: arXiv:2305.14627 (ALCE); arXiv:2402.15089 (AttributionBench, ACL 2024 Findings); arXiv:2305.06311 (AttrEval, EMNLP 2023 Findings).

Three independent primary sources converge on the same ceiling:
- ALCE's NLI metrics vs human gold: Cohen's kappa 0.698 (recall) / 0.525 (precision); accuracy 85.1% (recall) / 77.6% (precision) → mislabels ~15–22% of individual citation judgments.
- AttributionBench: even a **fine-tuned GPT-3.5** reaches only ~80% macro-F1 on binary "is every claim fully supported by cited evidence?"; error analysis of 300+ cases blames the model's inability to process nuanced information and the gap between what the model vs human annotators can access; the paper's thesis is that automatic attribution evaluation is an open, hard problem.
- AttrEval-GenSearch (242 human-annotated New Bing examples, 12 domains): the best evaluator, zero-shot GPT-4, reaches only 81–83% overall accuracy (micro-F1 85.1), i.e. ~1 in 5 wrong; weak on the Contradictory class (~45%).
Direct spec implication: the Pass 5 citation-accuracy verdict (§12.2 #9) cannot be assumed near-perfect; treat it as probabilistic and route uncertain/high-impact judgments to raw-source escalation (§12.2 #10). The spec already has that escalation step — the evidence validates it as necessary, not optional.
Caveats: figures are 2023–2024-era models; newer models may improve; the ~80% is per specific formulation/domain. Also note two abstraction-drift-specific claims were **REFUTED** (see below), so there is no surviving clean measurement of abstraction-drift detector accuracy on its own.

### F7 — LLM-generated citations fail verification at high rates without a dedicated pass — which is why the Pass 5 citation check exists. [HIGH]
Merges claims [13][18][19]. Sources: arXiv:2305.14627 (ALCE); arXiv:2409.02897 (LongCite); arXiv:2304.09848 (Liu et al., EMNLP 2023 Findings).

- ALCE: even the best 2023 systems "lack complete citation support 50% of the time" on ELI5 (ChatGPT vanilla 5-passage: 51.1% recall / 50.0% precision; ASQA ChatGPT 73.6% / 72.5%).
- Commercial generative search engines (Bing Chat, NeevaAI, perplexity.ai, YouChat), human eval: only 51.5% of sentences fully supported by citations; only 74.5% of citations support their sentence.
- Off-the-shelf LLMs are poor at long-context citation: GPT-4o citation recall 46.7 on the LongBench-Chat subset.
Caveats: snapshots of 2023 systems (NeevaAI now defunct; modern engines likely score higher) — demonstrates the failure mode, not current 2026 production numbers. "Perform poorly" for GPT-4o is subset-specific (it is much stronger on structured QA: MultiFieldQA recall 79.0). The conservative principle — inline citation cannot be assumed reliable by default — still holds.

### F8 — Dedicated training enables fine-grained sentence-level citation of long documents, beyond off-the-shelf GPT-4o. [MEDIUM]
Merges claims [17][18]. Source: arXiv:2409.02897 (LongCite, Zhang et al., THUDM/Zhipu, EMNLP 2024).

LongCite-8B/9B (SFT on LongCite-45k, built by the CoF coarse-to-fine pipeline) achieve SOTA fine-grained citation on LongBench-Cite, surpassing GPT-4o: LongCite-8B overall citation F1 72.0 vs GPT-4o 65.6 (6.4-pt margin), with ~2x finer granularity.
Caveats: MEDIUM because self-reported by the model's own creators on a benchmark they introduced (LongBench-Cite), and the citation-quality metric uses GPT-4o as the automatic judge (mild circularity); comparison is vs GPT-4o as of Sept 2024. Exact numbers verified verbatim against the primary source; human-eval validation of the GPT-4o judge mitigates the CoI.

---

## Spec decisions: verdicts and recommendations

| Spec item | Evidence verdict | Recommendation |
|---|---|---|
| §12.2 #1 Grounding (every factual clause has supporting units) | **Supported and improvable** | Use a MiniCheck-class specialized checker (MiniCheck-Flan-T5-L or Bespoke-MiniCheck-7B) for the grounding pass rather than a frontier LLM-as-judge — GPT-4-class accuracy at ~400x lower cost, >500 checks/min on one GPU. Check the license: Bespoke-MiniCheck is CC BY-NC; use MiniCheck-Flan-T5 if commercial. |
| §12.2 #8 Abstraction drift (candidate does not say more than the evidence) | **Partially supported; no clean detector** | Use NLI citation *recall* as the mechanism (statement not entailed by source ⇒ overclaim). No surviving evidence of a high-accuracy standalone abstraction-drift detector; budget for error and escalate. |
| §12.2 #9 Citation accuracy (quoted excerpts/line ranges match) | **Supported but capped ~80–85%** | Keep NLI-based verification (ALCE method), but treat verdicts as probabilistic — ~1 in 5 individual judgments is wrong even for GPT-4. Do not gate hard on a single checker verdict. |
| §12.2 #10 Raw-source escalation | **Validated as necessary** | The ~20% attribution-check error rate is exactly why escalation for uncertain/high-impact claims is required, not optional. Good design; keep it. |
| §16 Batch sizing (20–50 units, split >75; 30–50% context reservation) | **UNVERIFIED this round** | No surviving claim. Do not treat as evidence-backed; re-run angle (4) against Lost-in-the-Middle / Chroma context-rot / NoLiMa / RULER. |
| §18 Structured JSON output on every pass | **UNVERIFIED this round** | No surviving claim on constrained-decoding quality degradation. Re-run angle (3) (Tam et al. vs dottxt rebuttal). |
| §20 Prompt-injection / untrusted source text | **UNVERIFIED this round** | No surviving claim. Re-run angle (5) (spotlighting, instruction hierarchy, CaMeL, InjecAgent/BIPIA). |

---

## Full verified claim set (all 21, as-verified)

Format: claim — vote — primary source — evidence & caveats (condensed from verifier notes).

**[0]** MiniCheck-FT5 (770M) outperforms all comparable-size systems and reaches GPT-4 accuracy on LLM-AggreFact — a small specialized checker can match a frontier LLM at grounding verification. — **3-0** — arXiv:2404.10774 — Abstract verbatim; leaderboard shows MiniCheck-Flan-T5-L 75.0 vs GPT-4o 75.9 (~1pt). Caveats: GPT-4 = 2024 model; Bespoke-MiniCheck-7B (77.4) now tops it; benchmark assembled by paper authors from 10–11 third-party datasets.

**[1]** MiniCheck reaches GPT-4-level grounding accuracy at 400x lower cost — per-claim faithfulness checking economically viable at scale. — **3-0** — arXiv:2404.10774 — Abstract verbatim "400x lower cost"; 74.7 vs 75.3 balanced accuracy, $0.24 vs $107 on 13K set (~445x). Caveats: 400x pinned to April-2024 GPT-4 pricing; English-only training.

**[2]** On LLM-AggreFact, Bespoke-MiniCheck-7B ranks #1 at 77.4 avg (11 datasets), edging Claude-3.5 Sonnet (77.2) and beating much larger general models. — **3-0** — https://llm-aggrefact.github.io/ — Direct fetch 2026-08-01 confirms ranks 1–4 and 11-dataset average; Mistral-Large-2 123B/GPT-4o/Qwen2.5-72B/Llama-405B all below. Caveat: pool stops ~2025; "#1" = first among evaluated models.

**[3]** GPT-4o-2024-05-13 as a checker scores 75.9 on LLM-AggreFact — below the 7B Bespoke-MiniCheck (77.4), at far lower cost for the small model. — **3-0** — https://llm-aggrefact.github.io/ — Numbers verified. Caveats: margin 1.5pts; Claude-3.5 Sonnet (77.2) ~ties Bespoke-MiniCheck, so "specialized beats frontier" is specific to GPT-4o; leaderboard frozen; cost clause is inference (7B open-weights vs frontier API).

**[4]** Sub-1B checkers stay competitive: MiniCheck-Flan-T5-L (0.8B) 75.0 and FactCG-DeBERTa-L (0.4B) 75.6 both beat Llama-3.1-405B-Instruct (74.4), ~500–1000x larger. — **3-0** — https://llm-aggrefact.github.io/ — Numbers + arithmetic verified; FactCG paper (arXiv:2501.17144, NAACL 2025) makes same cross-group claim. Caveat: 0.6–1.2-pt margins over 405B likely within noise — "competitive" is the defensible framing.

**[5]** Bespoke-MiniCheck-7B (finetuned from internlm2_5-7b-chat) is claimed by its developers as SOTA fact-checking on LLM-AggreFact (29K test samples) — small dedicated checker beats larger models. Self-reported; card shows a chart but no numeric accuracy in text and no explicit GPT-4 comparison. — **3-0** — https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B — Verbatim SOTA self-claim; leaderboard corroborates #1 at 77.4; MiniCheck paper independently supports the thesis.

**[6]** With vLLM, throughput >500 docs/min on a single A6000 — per-sentence grounding checks feasible at ingestion volume without frontier API costs. — **3-0** — https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B — Card verbatim; MiniCheck repo corroborates (~527–967/min). Caveats: "docs/min" = doc–claim pairs (N sentences = N checks); card names the earlier Llama-3.1 variant; CC BY-NC 4.0 license.

**[7]** AlignScore evaluated on 22 datasets (19 unseen), substantial improvement over prior metrics — OOD generalization for a trained groundedness checker. — **3-0** — arXiv:2305.16739 — Abstract verbatim; MiniCheck paper calls it "existing SOTA specialized fact-checking model" (70.4% on LLM-AggreFact). Caveats: "unseen dataset" ≠ "unseen domain" (shared CNN/DM, XSum corpora); surpassed since 2024; historical-strength claim (correct past tense).

**[8]** RAGChecker implements groundedness via claim-level decomposition + per-claim entailment, using Llama3-70B as extractor and checker via RefChecker — fine-grained claim entailment, not holistic scoring. — **3-0** — arXiv:2408.08067 — Full-text quote verbatim; official amazon-science/RAGChecker repo corroborates. Caveat: model is configurable; Llama3-70B is the paper's/ repo's default, not hard-coded.

**[9]** LettuceDetect (ModernBERT token-classification) achieves 79.22% example-level F1 on RAGTruth, "a 14.8% improvement over Luna," the prior encoder SOTA. — **2-1** — arXiv:2502.17125 — 79.22 F1 verified (Table 2 + HF card); baselines match originals. CAVEAT (must ship): Luna's RAGTruth F1 = 65.4 in both papers, so true gap is 13.82 pts absolute / 21.1% relative — the abstract's "14.8%" is an arithmetic error. Substantive content verifies; self-reported preprint.

**[10]** A small encoder grounding checker outperforms all prior encoder models and most prompt-based LLM methods while ~30x smaller — cheap non-LLM grounding at scale. — **3-0** — arXiv:2502.17125 — Quote verbatim; beats Luna 65.4, prompt gpt-4-turbo 63.4, SelfCheckGPT 58.8, but NOT RAG-HAT 83.9 (DPO-tuned Llama-3-8B) — "most" hedge accurate; 396M vs 8–13B; 30–60 ex/sec. Caveat: **in-domain only** (RAGTruth), no OOD test; best overall detector remains an LLM (RAG-HAT, +4.7 F1).

**[11]** ALCE citation recall/precision computed automatically with the TRUE NLI model (T5-based, Honovich 2022): recall requires ≥1 citation whose concatenation entails the statement; a citation is "irrelevant" if it alone does not entail AND removing it still leaves the rest entailing. — **3-0** — arXiv:2305.14627 — All three components verbatim (ar5iv full text); ALCE is the standard citation-quality eval. Definitional; cannot go stale.

**[12]** ALCE's NLI metrics vs humans: Cohen's kappa 0.698 (recall) / 0.525 (precision); accuracy 85.1% / 77.6% — usable but mislabels ~15–22% of individual citation judgments. — **3-0** — arXiv:2305.14627 — All figures verbatim (§6 + Appendix G.5). Caveat: treating all disagreement as "mislabels" assumes human gold is perfect; claim's hedging keeps it honest.

**[13]** 2023-generation LLMs frequently generated statements without complete citation support: on ELI5 the best systems lacked complete support 50% of the time (ChatGPT vanilla 5-passage 51.1% recall / 50.0% precision; ASQA 73.6% / 72.5%). — **3-0** — arXiv:2305.14627 — Abstract + Tables 4/6 verified across three fetches. Caveat: scoped to 2023 LLMs (not outdated by LongCite 2024); normative "cannot be trusted without verification" is fair inference.

**[14]** On AttributionBench binary classification, even fine-tuned GPT-3.5 reaches only ~80% macro-F1 — a ceiling on automated attribution checkers circa early 2024. — **3-0** — arXiv:2402.15089 — Abstract verbatim (ACL 2024 Findings, Li et al.). Caveat: 80% is fine-tuned GPT-3.5 specifically; OOD performance drops lower; date-scoped.

**[15]** Error analysis of 300+ failure cases: most automated attribution-eval errors come from (a) failing to process nuanced info and (b) mismatch between info available to model vs human annotators. — **3-0** — arXiv:2402.15089 — Abstract sentence verbatim. Caveat: scoped to AttributionBench models/datasets, not a universal law.

**[16]** Automatic attribution evaluation remains unsolved even for SOTA LLMs — a citation-accuracy pass cannot be assumed near-perfect and must budget for a meaningful error rate. — **3-0** — arXiv:2402.15089 — Paper title/thesis; ~80% F1 (~20% error) supports the budgeting inference; adjacent 2024–25 checkers sit ~74–78%. Caveat: ~80% is one formulation; varies by domain.

**[17]** LongCite-8B/9B (SFT on LongCite-45k via CoF) achieve SOTA fine-grained sentence-level citation on LongBench-Cite, surpassing GPT-4o — LongCite-8B F1 72.0 vs GPT-4o 65.6. — **3-0** — arXiv:2409.02897 — Table 2 exact (72.0 vs 65.6, 6.4-pt margin). Caveats: self-reported by creators on their own benchmark; GPT-4o used as the automatic judge (circularity); vs GPT-4o Sept 2024.

**[18]** Off-the-shelf LLMs perform poorly at long-context QA with citations without dedicated training — GPT-4o citation recall 46.7 on LongBench-Chat — inline citation of long sources not reliable by default. — **3-0** — arXiv:2409.02897 — Table 2 recall 46.7 verified. Caveat: LongBench-Chat is the hardest open-ended subset; GPT-4o much stronger on structured QA (MultiFieldQA R=79.0). Conservative principle holds.

**[19]** Human eval of 4 commercial generative search engines (Bing Chat, NeevaAI, perplexity.ai, YouChat): on average only 51.5% of sentences fully supported by citations; only 74.5% of citations support their sentence. — **3-0** — arXiv:2304.09848 — Abstract verbatim; engines match. Caveat: early-2023 snapshot (NeevaAI defunct); demonstrates failure mode, not 2026 numbers.

**[20]** Best automatic attribution evaluator — zero-shot GPT-4 — reaches only 81–83% overall accuracy on AttrEval-GenSearch (242 New Bing examples, 12 domains) — ~1 in 5 citation-support judgments by a strong LLM checker is wrong. — **3-0** — arXiv:2305.06311 — 242-example set + 81–83% verbatim (micro-F1 85.1, so claim uses the conservative number); weak on Contradictory (~45%). Caveats: 2023 GPT-4; best only on GenSearch (fine-tuned models win on the Simulation set).

---

## Refuted claims (0-3 or majority-against; kept for transparency)

- **AlignScore (355M) matches or outperforms GPT-4/ChatGPT factual-consistency metrics.** (arXiv:2305.16739, 0-3) — The small-checker-matches-GPT-4 result holds for MiniCheck, NOT AlignScore. AlignScore is historical SOTA, since surpassed.
- **RAGChecker's claim-entailment metrics correlate substantially better with humans than RAGAS's best metric (Pearson 61.93 vs 41.07) and TruLens.** (arXiv:2408.08067, 0-3) — Did not survive verification; do not cite the RAGAS-is-weaker comparison as established.
- **NLI citation-precision has a documented blind spot: it cannot detect "partial support."** (arXiv:2305.14627, 0-3) — Refuted; ALCE's precision definition accounts for the multi-citation case, so the clean "blind spot" framing is false.
- **Citation precision inversely correlated with perceived utility (r = -0.96), evidence of systematic overclaiming in more useful-sounding systems.** (arXiv:2304.09848, 0-3) — Refuted; the abstraction-drift-via-utility-tradeoff evidence did not hold. There is no surviving clean measurement of abstraction-drift detection accuracy.

---

## Caveats (cross-cutting)

- **Coverage:** Only angles (1) grounding and (2) citation survived verification. Angles (3) structured outputs, (4) long-context/batch-sizing, (5) prompt-injection are **unverified** here despite being named in the round scope and this file's title.
- **Time-sensitivity:** The LLM-AggreFact leaderboard and most cost/accuracy comparisons are 2023–2025-era; they exclude 2025–2026 frontier models. The "400x cheaper" multiplier shrinks against cheaper current frontier pricing. The specialized-beats-frontier conclusion is scoped to models these benchmarks evaluated.
- **Source mix:** F1/F5/F6/F7 rest on multiple peer-reviewed primary sources. F4 (LettuceDetect) and F8 (LongCite) are self-reported preprints on partly author-designed benchmarks — MEDIUM confidence. Claim [9] carried a documented arithmetic error in its own source's abstract.
- **Benchmark conflicts of interest:** LLM-AggreFact is maintained by the MiniCheck authors; LongBench-Cite was introduced by the LongCite authors and judged by GPT-4o. Mitigated by public datasets, cross-group corroboration (FactCG), and human-eval validation, but not eliminated.
- **Attribution-check ceiling is the load-bearing risk:** ~80–85% agreement means ~1 in 5 citation judgments wrong even for GPT-4; this is a hard finding across three independent sources and directly shapes how much the spec can trust Pass 5 citation verdicts.

---

## Open questions

1. **Long-context / batch sizing (spec §16):** Do the 20–50-unit batch and 30–50% context-reservation numbers hold under 2025–2026 long-context degradation evidence (Lost in the Middle, Chroma context-rot July 2025, NoLiMa, RULER)? No surviving claim — needs its own round.
2. **Structured outputs (spec §18):** Does JSON-schema-constrained decoding measurably degrade extraction/classification quality (Tam et al. 2024 "Let Me Speak Freely" vs the dottxt "Say What You Mean" rebuttal and 2025–26 replications)? Unverified.
3. **Prompt-injection defense (spec §20):** Can ingested document text be reliably prevented from steering the extractor, and what layering does current evidence support (spotlighting/Hines 2024, instruction hierarchy/Wallace 2024, CaMeL/Debenedetti 2025, InjecAgent/BIPIA benchmarks)? Unverified.
4. **Abstraction-drift detection specifically:** With both supporting claims refuted, what is the standalone accuracy of an automated "says more than the evidence" detector, distinct from general grounding/recall? Unmeasured here.
5. **Current-frontier re-baseline:** How do 2024-era specialized checkers (MiniCheck/Bespoke-MiniCheck) compare to 2025–2026 frontier models as checkers, given the leaderboard appears frozen? The cost advantage is clear; the accuracy gap may have moved.
