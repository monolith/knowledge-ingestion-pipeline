# Round 3 Design-Verification Research — LLM-as-Judge Reliability & Auditor Architecture

**Date:** 2026-08-01
**Pipeline spec:** `/home/anatoly/knowledge_ingestion_pipeline_demo/docs/SPECIFICATION.md` (Pass 5 adversarial audit, §12; batching strategy §16)
**Method:** multi-agent fan-out research, 3-vote adversarial verification per claim. 25 claims survived.
**Prior rounds:** Round 1 — atomic extraction, routing/retrieval ([2026-07-31-pipeline-design-verification-research.md](2026-07-31-pipeline-design-verification-research.md)); Round 2 — claim-relationship classification, evidence aggregation, temporal knowledge ([2026-07-31-round2-audit-classification-engineering-research.md](2026-07-31-round2-audit-classification-engineering-research.md)).

---

## SCOPE WARNING — what this round actually verified

Round 3 was tasked with five angles. **All 25 surviving claims fall under angles (1) LLM-as-judge reliability/biases and (2) self-correction/auditor architecture.** The other three angles produced **zero claims surviving 3-vote verification** in this round:

- **(3) Grounding / hallucination / citation-accuracy metrics** (RAGAS, AlignScore, MiniCheck, ALCE, AttributionBench, LongCite) — UNVERIFIED
- **(4) Structured outputs, long-context degradation, prompt-injection defense** ("Let Me Speak Freely" debate, Lost in the Middle, NoLiMa, spotlighting/CaMeL) — UNVERIFIED
- **(5) Pipeline production engineering** (durable execution, batch-API economics, multi-agent division of labor, Docling/marker/unstructured benchmarks) — UNVERIFIED

Spec decisions resting on angles 3–5 (checker tooling for Pass 5 checks 1/9, §16's 20–50-unit batches and 30–50% context reservation, Pass 0 parser choice, Pass 6/§17 engineering) remain **unaudited by this research program**. Do not cite this file as support for them.

---

## Synthesis — 8 findings

### F1. Preference agreement ≠ correctness auditing; non-reasoning judges are near chance on hard correctness (HIGH)

Strong LLM judges match human *preference* at >80% (MT-Bench/Chatbot Arena, Zheng et al. NeurIPS 2023 — same level as human-human agreement, non-tied votes). But JudgeBench (Tan et al., ICLR 2025) shows that on objectively-labeled hard correctness pairs, many strong judges are barely above random: GPT-4o 56.57%, GPT-4o-mini 50.00%, Claude-3.5-Sonnet 64.29%, Claude-3-Haiku 33.14% (below random), while reasoning models do markedly better: o1-preview 75.43%, o3-mini(high) 80.86%. Crowdsourced-preference benchmarks are explicitly a poor indicator of factual/logical correctness.

**Spec implication:** Pass 5 is a correctness-discrimination task, not a preference task. The auditor must be a reasoning-class model, and even then should be modeled at ~75–85% pairwise accuracy on hard cases — audit reduces error, it does not eliminate it. High `auditor_confidence` values (spec example: 0.99) should not be treated as calibrated.

### F2. Judge biases are systematic, taxonomized, and persist in frontier models (HIGH)

Zheng et al. 2023 documented position, verbosity, and self-enhancement biases plus limited reasoning-grading ability. The CALM framework (Ye et al., arXiv 2410.02736) identifies and automatically quantifies 12 bias types (Position, Verbosity, Compassion-Fade, Bandwagon, Distraction, Fallacy-Oversight, Authority, Sentiment, Diversity, Chain-of-Thought, Self-Enhancement, Refinement-Aware) and concludes reliability is not sufficient for uncritical use even in frontier judges.

**Spec implication:** the Pass 5 audit prompt should be hardened against at least bandwagon/authority framing in candidate text (a candidate asserting "well-established" is itself a bias vector against the auditor).

### F3. Position bias is the dominant judge bias; mitigation is both-orders aggregation (HIGH)

Order-swap flips ~17–22% of pairwise verdicts even for the best 2024-era judges (CALM robustness rates: Claude-3.5 0.832, GPT-4-Turbo 0.818, GPT-4o 0.776 on position vs 0.92–0.98 on verbosity). Wang et al. 2023: order manipulation alone made Vicuna-13B "beat" ChatGPT on 66/80 queries with ChatGPT as judge. Shi et al. (arXiv 2406.07791, 150k+ instances, 15 judges, 22 tasks): position bias is systematic not random, varies significantly by judge and task, is strongly driven by the quality gap (worst on near-ties), and is only weakly influenced by length. Mitigation: Balanced Position Calibration — run both orderings, aggregate (2x judge cost).

**Spec implication:** any pairwise or comparative judgment in the pipeline (Pass 3 relationship judgment between competing readings; Pass 5 comparing candidate versions or candidate-vs-evidence framings) must run both orderings and aggregate, especially for near-tie cases — which are exactly the contested/nuance cases the pipeline cares most about. The spec currently does not mandate this.

### F4. Self-preference bias makes same-model generator+judge unsound; it survives anonymization and is tied to self-recognition (HIGH)

LLM evaluators score their own outputs higher even when humans judge them equal (Panickssery, Bowman & Feng, NeurIPS 2024). Fine-tuning shows a linear, confounder-resistant correlation between self-recognition ability and self-preference strength. GPT-4 recognizes its own generations at 73.5% pairwise accuracy out of the box (weaker models near chance). CALM: self-preference persists under source anonymization (error rates 1.16–16.1 across six judges; ChatGPT 8.91). 2025 nuance (arXiv 2504.03846): some self-preference in strong models tracks genuine quality — but harmful self-preference persists precisely when the evaluator errs as generator, i.e., in exactly the failure cases an auditor exists to catch.

**Spec implication:** the Pass 5 auditor should be a *different model* from the Pass 4 proposer, or at strict minimum a fresh context with the candidate treated as third-party text. Anonymizing authorship is not sufficient — models implicitly recognize their own prose.

### F5. Intrinsic self-correction fails and often degrades accuracy; models cannot judge their own reasoning (HIGH)

Huang et al. (ICLR 2024): with no external feedback, self-correction dropped accuracy on every benchmark tested — GPT-4 GSM8K 95.5→89.0 over two rounds; GPT-3.5 CommonSenseQA 75.8→38.1 after one round; GPT-4-Turbo GSM8K 91.5→88.0. Root cause: LLMs cannot reliably evaluate the correctness of their own reasoning. Their recommendation: ground verification in external feedback (execution, retrieval) rather than intrinsic self-critique. Corroborated by DeepMind SCoRe (2409.12917: prompted self-correction "largely ineffective"; fixed only via multi-turn RL training).

**Spec implication:** validates the spec's core Pass 5 architecture — an audit that checks candidates *against source documents* (external evidence), not a "review your own answer" loop. Never add a cheap intrinsic-self-critique pass as a substitute.

### F6. Self-correction works only with reliable external feedback; the prompted-self-critique literature over-reports (HIGH)

Kamoi et al. (TACL 2024 critical survey): no prior work demonstrates successful self-correction from prompted (unfine-tuned) LLM feedback except in tasks exceptionally suited for it; it works well where reliable external feedback exists; prior positive results used oracle feedback or weak baselines that over-evaluate self-correction.

**Spec implication:** push Pass 5 checks toward mechanical/external verification wherever possible: check 9 (citation accuracy — quoted excerpts and line ranges) should be deterministic string/offset matching, not LLM judgment; check 6 (provenance integrity — IDs/paths resolve) should be code; the LLM auditor spends its unreliable judgment only on the irreducibly semantic checks (coverage, scope fidelity, abstraction drift), grounded in retrieved source text (check 10).

### F7. Fresh-context, atomic, factored verification measurably beats in-context self-critique (HIGH)

Chain-of-Verification (Dhuliawala et al., Meta AI 2023, ACL Findings 2024): answering verification questions in a fresh context that cannot see the original draft (factored) beats joint verification, because models re-copy their own hallucinations when visible. Llama 65B FactScore 55.9→71.4 (factor+revise, ~28% relative); MultiSpanQA F1 0.39→0.48; Wikidata list precision 0.17→0.36. Same model answers atomic verification questions ~70% correctly vs ~17% precision for the same facts in open-ended generation.

**Spec implication:** direct evidence for the spec's per-assertion audit design. Concretely: the auditor should verify each candidate assertion as an isolated question against retrieved units/normalized text *without the candidate's summary prose in the verification context*, then compare answers to the candidate. Atomicity of Pass 1 units pays off again here.

### F8. Trained dedicated critics outperform unaided review, with caveats (MEDIUM)

CriticGPT (OpenAI, arXiv 2407.00215): RLHF-trained critic's critiques preferred over human critiques 63% of the time on naturally occurring LLM code errors; models caught more bugs than paid human reviewers; Human+CriticGPT teams hallucinated less than the model alone. Caveats: vendor self-report, not peer-reviewed; human baseline was the contractor pool, not expert reviewers; even untrained ChatGPT critiques beat human critiques, so the 63% is not solely from critic training; critics nitpick and hallucinate bugs at higher rates than humans.

**Spec implication:** supports investing in a dedicated auditor role with its own tuned prompt (adversarial framing per spec principle 8); expect false-positive findings (nitpick/hallucinated issues) — the `fix`-produces-new-version-never-overwrites rule (§12.3) is the right containment, and `defer` verdicts should route to human review rather than forced resolution.

---

## Spec decisions: contradicted / improved / validated

| Spec element | Verdict | Evidence |
|---|---|---|
| Pass 5 adversarial audit grounded in source chain (principle 8, §12.1, check 10) | **VALIDATED** | F5, F6, F7 — external grounding is the only regime where correction reliably works |
| Auditor identity unspecified (same model as proposer permitted) | **IMPROVE** | F4 — require different model, or minimum fresh context; anonymization insufficient |
| No order-swap mandate for comparative judgments | **IMPROVE** | F3 — mandate both-orders aggregation for pairwise judgments, worst on near-ties |
| `auditor_confidence` field treated as meaningful (example 0.99) | **CAUTION** | F1 — judge calibration unverified this round; JudgeBench: even best reasoning judges ~19% pairwise error on hard cases |
| Check 9 (citation accuracy) via LLM audit | **IMPROVE** | F6 — make it deterministic string/line-range matching; reserve LLM judgment for semantic checks |
| Per-assertion structure of candidates + atomic units | **VALIDATED** | F7 — atomic verification questions: ~70% vs ~17% accuracy |
| Auditor model class unspecified | **IMPROVE** | F1 — must be reasoning-class; GPT-4o-class non-reasoning judges near chance on hard correctness |
| §16 batching (20–50 units, 30–50% context reservation) | **UNVERIFIED** | angle 4 produced no surviving claims — still resting on Round 1/2 evidence and assumption |

---

## Full verified claim set (25 claims)

Legend: vote = adversarial verifier votes (for-against). All confidence labels are the verifiers' own.

### Angle 1 — LLM-as-judge reliability and biases

#### C0. MT-Bench: strong judges match human preference at >80% — 3-0, HIGH
**Claim:** Strong LLM judges like GPT-4 achieve over 80% agreement with both controlled (expert) and crowdsourced human preferences — the same level as human-human agreement.
**Source:** Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," NeurIPS 2023 D&B — https://arxiv.org/abs/2306.05685 (primary)
**Quote:** "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans."
**Evidence:** Verbatim abstract quote confirmed. MT-Bench controlled setting (58 expert-level labelers): GPT-4-human agreement 85% on non-tied votes vs 81% human-human; Chatbot Arena crowdsourced also >80%.
**Caveats:** (a) figures are for non-tied votes; (b) scoped to chat-response *preference* judging — does not generalize to correctness auditing (see C2/C3); (c) same paper documents position/verbosity/self-enhancement biases despite high aggregate agreement.

#### C1. MT-Bench bias taxonomy: position, verbosity, self-enhancement, limited reasoning — 3-0, HIGH
**Claim:** LLM judges exhibit documented systematic biases — position, verbosity, self-enhancement — plus limited reasoning ability; the paper proposes partial mitigations.
**Source:** https://arxiv.org/abs/2306.05685 (primary)
**Evidence:** Position bias: judge consistency under order swap GPT-4 65.0%, GPT-3.5 46.2%, Claude-v1 23.8%. Verbosity: repetitive-list attack failure 91.3% (Claude-v1, GPT-3.5) vs 8.7% (GPT-4). Self-enhancement indications: GPT-4 +10% win rate on own outputs, Claude-v1 +25%. Mitigations: position swapping, few-shot judging (GPT-4 consistency 65.0→77.5%), CoT, reference-guided grading (math grading failure 70%→15%).
**Caveats:** For self-enhancement the paper hedges ("our study cannot determine whether…") — that leg rests on suggestive in-paper data plus later confirmation (Panickssery et al., C10–C12). Position/verbosity independently replicated (Wang et al. 2305.17926).

#### C2. JudgeBench: strong non-reasoning judges near random on hard correctness — 3-0, HIGH
**Claim:** On JudgeBench's objectively-labeled challenging pairs, many strong judges including GPT-4o perform only slightly better than random — frontier judges cannot be assumed reliable for hard correctness discrimination (Pass 5's task).
**Source:** Tan et al., "JudgeBench," ICLR 2025 — https://arxiv.org/abs/2410.12784 (primary, verified against camera-ready PDF)
**Evidence:** Random baseline 50%. GPT-4o 56.57% (vanilla), GPT-4o-mini 50.00%, Llama-3.1-405B 56.86%, Claude-3.5-Sonnet 64.29%, Claude-3-Haiku 33.14% (below random); all fine-tuned judges except Skywork significantly below random. Reasoning judges: o1-preview 75.43%, o1-mini 65.71%, o3-mini(high) 80.86%.
**Caveats:** Not "all frontier judges near random" — reasoning models markedly better; but even the best makes ~19% pairwise errors on hard cases. Model a 2026 reasoning-model auditor at ~75–85% pairwise accuracy on hard cases. Verification used primary PDF directly (search budget exhausted — stronger evidence anyway).

#### C3. Preference-alignment benchmarks don't validate correctness judging — 3-0, HIGH
**Claim:** Human-preference-agreement benchmarks (MT-Bench-style) are a poor indicator of factual/logical correctness on challenging tasks; high human-agreement scores do not validate a judge for correctness auditing.
**Source:** https://arxiv.org/abs/2410.12784 (primary)
**Quote:** "Existing benchmarks primarily focus on a judge's alignment with human preferences, but often fail to account for more challenging tasks where crowdsourced human preference is a poor indicator of factual and logical correctness."
**Evidence:** Judges scoring >80% human agreement on MT-Bench are near-chance on JudgeBench's objective pairs — a direct empirical demonstration. Corroborated by Hosking et al. ICLR 2024 ("Human Feedback is not Gold Standard": preference under-weights factuality).
**Caveats:** "Existing benchmarks" is time-indexed pre-Oct-2024 — JudgeBench and successors now test correctness. Mild author self-interest (motivates their benchmark), offset by reproducible near-chance result. Contradiction sweep limited by search budget; no contradicting source known.

#### C4. CALM: 12 bias types, automatically quantified — 3-0, HIGH
**Claim:** The CALM framework identifies 12 distinct LLM-judge biases (Position, Verbosity, Compassion-Fade, Bandwagon, Distraction, Fallacy-Oversight, Authority, Sentiment, Diversity, Chain-of-Thought, Self-Enhancement, Refinement-Aware), quantified via automated principle-guided perturbation, not human annotation.
**Source:** Ye et al., "Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge" — https://arxiv.org/abs/2410.02736 (primary)
**Evidence:** Table 1/§2.2 enumerates exactly the 12 named biases — perfect match. Methodology is automated LLM-driven modification.
**Caveats:** Paper says "modification" not "perturbation"; 2–3 biases (CoT, Self-Enhancement, Refinement-Aware) quantified by varying the judging setup rather than perturbing answer text — still automated.

#### C5. Frontier judges retain significant task-specific biases; not fit for uncritical use — 3-0, HIGH
**Claim:** Even frontier judge models retain significant biases on specific tasks despite good overall performance; LLM-as-judge reliability is not yet sufficient for uncritical use.
**Source:** https://arxiv.org/abs/2410.02736 (primary)
**Quote:** "while advanced models have achieved commendable overall performance, significant biases persist in certain specific tasks… there remains room for improvement in the reliability of LLM-as-a-Judge." Abstract additionally warns to "exercise caution in LLM-as-a-Judge applications."
**Evidence:** Field consensus corroborated by Zheng et al. 2023, Wang et al. 2023, Panickssery et al. 2024, JudgeBench. 2025 follow-ups confirm biases persist in newer frontier judges.

#### C6. Position bias >> verbosity bias by robustness rate; ~17–22% verdict flips — 3-0, HIGH
**Claim:** By robustness rate (fraction of judgments unchanged after bias injection): position RR Claude-3.5 0.832, GPT-4-Turbo 0.818 (pairwise task) vs verbosity RR Claude-3.5 0.952, GPT-4o 0.977 (scoring task) — roughly 17–18% of pairwise verdicts flip on order swap for the best 2024-era judges.
**Source:** https://arxiv.org/abs/2410.02736 (primary, tables fetched)
**Evidence:** All numbers confirmed; GPT-4o position RR 0.776 (22.4% flips) — the claim understates rather than cherry-picks. Direction agrees with Wang et al. 2023 and MT-Bench.
**Caveats:** Position RR from pairwise task, verbosity RR from scoring task — cross-bias comparison spans two task formats (paper presents them side by side this way). Scoped to 2024-era judges.

#### C7. Self-enhancement persists under source anonymization — 2-1, HIGH (verifier)
**Claim:** Judge models rated their own outputs more favorably even when answer sources were anonymized; self-enhancement error rates 1.16–16.1 across six judges (ChatGPT 8.91).
**Source:** https://arxiv.org/abs/2410.02736 (primary)
**Evidence:** Table 5 reproduced via neutral transcription: ChatGPT 8.91, GPT-4-Turbo 1.16, GPT-4o 1.74, GLM-4 1.18, Claude-3.5 7.48, Qwen2 16.1; metric |1 − y_self/y_other| (%). Anonymization condition confirmed in paper's words. Corroborated by Zheng et al. 2023 and Panickssery et al. NeurIPS 2024 (implicit self-recognition under blind conditions).
**Caveats:** **2-1 vote — one verifier dissented.** Three of six judges near 1–2% (heterogeneous effect). arXiv 2504.03846 (2025): some strong-model self-preference reflects genuine quality differences — qualifies interpretation, not the measurement. "Anonymized" = labels removed, not immunity to implicit self-recognition.

#### C8. Order swap alone flips rankings: Vicuna-13B "beats" ChatGPT 66/80 — 3-0, HIGH
**Claim:** Swapping response order can flip LLM-judge verdicts wholesale — Vicuna-13B beat ChatGPT on 66 of 80 Vicuna Benchmark queries with ChatGPT as evaluator, purely via order manipulation.
**Source:** Wang et al., "Large Language Models are not Fair Evaluators" — https://arxiv.org/abs/2305.17926 (primary, verbatim verified)
**Caveats:** GPT-4-class judges show weaker but still-present position bias (same paper) — the 66/80 magnitude doesn't generalize to modern judges; existence does.

#### C9. Balanced Position Calibration mitigates position bias — 3-0, HIGH
**Claim:** Running the judge over both response orderings and aggregating (Balanced Position Calibration) is an effective mitigation for position bias.
**Source:** https://arxiv.org/abs/2305.17926 (primary)
**Evidence:** One of three calibration strategies proposed; order-swapping became standard practice post-publication (MT-Bench swap-consistency, Arena-Hard pipelines).
**Caveats:** 2x judge cost; residual bias on near-tie pairs; claim says "mitigation," not elimination.

#### C10. Self-preference bias: models score own outputs higher despite equal human-judged quality — 3-0, HIGH
**Claim:** LLM evaluators score their own outputs higher than others' even when human annotators judge them equal — undermining same-model generator+judge designs.
**Source:** Panickssery, Bowman & Feng, "LLM Evaluators Recognize and Favor Their Own Generations," NeurIPS 2024 — https://arxiv.org/abs/2404.13076 (primary). Corroborating: https://arxiv.org/abs/2410.21819 (perplexity/familiarity mechanism — maximal when generator == judge); https://arxiv.org/abs/2504.03846.
**Caveats:** 2025 nuance (2504.03846): self-preference in stronger models often tracks objectively better outputs on verifiable tasks, BUT "harmful self-preference persists when evaluator models err as generators" — worst precisely in the failure cases an auditor exists to catch. "Directly undermines" marginally stronger than the 2025 nuance warrants; qualification, not refutation.

#### C11. Self-preference causally linked to self-recognition — 3-0, HIGH
**Claim:** Fine-tuning experiments show a linear correlation between self-recognition capability and self-preference strength; controlled experiments rule out straightforward confounders — the bias is not coincidental quality difference.
**Source:** https://arxiv.org/abs/2404.13076 (primary, verbatim verified)
**Caveats:** "Resists straightforward confounders" ≠ proof of causation. 2504.03846 addresses a different question and doesn't challenge the fine-tuning experiments. Models are GPT-3.5/Llama-2-era; magnitude on 2026 frontier models unverified, mechanism unrefuted.

#### C12. GPT-4 recognizes its own generations at 73.5% out of the box — 3-0, HIGH
**Claim:** GPT-4 achieved 73.5% pairwise accuracy distinguishing its own summaries from two other LLMs and humans (GPT-3.5 53.5%, Llama 2 51.4% — near chance); same-model self-audit cannot be assumed blind to authorship.
**Source:** https://arxiv.org/abs/2404.13076 (primary; Table 7: GPT-4 0.672 XSUM / 0.747 CNN-DM pairwise, no fine-tuning)
**Correction applied by verifier:** the 53.5/51.4 figures are XSUM values, not CNN/DailyMail (CNN-DM: 0.481/0.505) — substance unchanged: weaker models near chance on both.
**Caveats:** Davidson et al. (arXiv 2407.06946, EMNLP 2024 Findings) found no consistent self-recognition across 10 LLMs in a *security-question* paradigm — self-recognition is task/paradigm-dependent; a null elsewhere doesn't license assuming an auditor is authorship-blind. 2023-24-era models.

#### C13. Position bias is systematic, not random; varies by judge and task — 3-0, HIGH
**Claim:** Position bias is systematic rather than random and varies significantly across judge models and task types — a Pass-5 judge cannot be assumed order-neutral without per-model measurement.
**Source:** Shi et al., "Judging the Judges" — https://arxiv.org/abs/2406.07791 (primary; 15 judges, 22 tasks, ~40 solution models, 150k+ instances on MTBench and DevBench)
**Caveats:** Contradiction sweep limited by search budget; corroborated by Wang et al. 2023 and MT-Bench; no source known claiming position bias is random or eliminated.

#### C14. Position bias driven by quality gap (worst on near-ties), weakly by length — 3-0, HIGH
**Claim:** Position bias is strongly driven by candidate quality gap (dominates when candidates are close in quality); prompt-component length has only weak influence — order-swap countermeasures matter most for near-tie comparisons.
**Source:** https://arxiv.org/abs/2406.07791 (primary; revised 2025-11-11 — current)
**Evidence:** Regression: prompt/input lengths statistically insignificant predictors; quality gap a strong predictor. "Answer pairs… of similar quality are difficult to judge."
**Caveats:** Verbosity bias (preferring longer *answers*) is a distinct bias from length driving *position* bias — no conflict.

### Angle 2 — Self-correction and auditor architecture

#### C15. Intrinsic self-correction fails to improve reasoning and sometimes degrades it — 3-0, HIGH
**Claim:** LLM self-revision with no external feedback fails to improve reasoning accuracy and sometimes actively degrades it, across GSM8K, CommonSenseQA, HotpotQA.
**Source:** Huang et al., "Large Language Models Cannot Self-Correct Reasoning Yet," ICLR 2024 — https://arxiv.org/abs/2310.01798 (primary). Corroborating: DeepMind SCoRe https://arxiv.org/abs/2409.12917 (NeurIPS 2024); Kamoi et al. TACL 2024.
**Evidence:** GPT-4 GSM8K 95.5→91.5→89.0 over two rounds; GPT-3.5 CommonSenseQA 75.8→38.1; GPT-3.5 GSM8K 75.9→74.7; GPT-4 HotpotQA 49.0→43.0. No benchmark improved. Prior positive results (Reflexion, RCI) depended on oracle labels.
**Caveats:** RL-trained reasoning models (o1, R1) self-correct *within* CoT — a trained in-generation capability, not prompted answer revision; bounds applicability without contradicting the claim.

#### C16. Degradation magnitudes, exact — 3-0, HIGH
**Claim:** GPT-3.5 GSM8K 75.9%→75.1% (round 1)→74.7% (round 2); CommonSenseQA 75.8%→38.1%; GPT-4-Turbo GSM8K 91.5%→88.0%.
**Source:** https://arxiv.org/abs/2310.01798 (Tables 3–4, exact match verified)
**Caveats:** GPT-4-Turbo partially recovers to 90.0% at round 2 (omitted, not misstated); CommonSenseQA round 2 recovers to 41.8% (still a collapse). Trained self-correction (SCoRe) qualifies the generalization, not these prompted-intrinsic numbers.

#### C17. Root cause: models can't judge own reasoning; remedy: external feedback — 3-0, HIGH
**Claim:** LLMs cannot reliably evaluate the correctness of their own reasoning; the authors recommend grounding verification in external feedback (execution, search/retrieval) — supporting a Pass-5 auditor that checks claims against source documents rather than asking the extractor to re-examine itself.
**Source:** https://arxiv.org/abs/2310.01798 (§1, §5, §6 verified)
**Evidence sharpener:** the same paper shows multi-agent debate (separate LLM critic, no ground truth) "significantly underperforms simple self-consistency" — a separate auditor is supported *only because* it grounds checks in source documents. External grounding, not merely separateness, does the work.
**Caveats:** The one-line supporting quote is a close paraphrase, not verbatim. SCoRe (RL-trained) qualifies field-level generalization, not this paper-description or its implication for prompted pipelines.

#### C18. No successful self-correction from prompted-LLM feedback except exceptionally suited tasks — 3-0, HIGH
**Claim:** No prior work demonstrates successful self-correction using feedback from prompted (unfine-tuned) LLMs, except tasks exceptionally well-suited for it — intrinsic self-critique is not a reliable audit mechanism for a prompting-only Pass-5 auditor.
**Source:** Kamoi et al., "When Can LLMs Actually Correct Their Own Mistakes?" TACL 12:1417–1440 (2024) — https://arxiv.org/abs/2406.01297 (primary, verbatim verified). Corroborating: Huang et al. ICLR 2024; SCoRe.
**Evidence:** Semantic Scholar sweep of citing corpus (100 citations through 2026): zero papers demonstrating successful intrinsic self-correction from prompted feedback on general tasks; multiple 2026 papers extend the negative finding (revision loops degrading correctness; self-authored verification scores decoupling from performance). o1/R1-style in-CoT self-correction is RL-trained — inside the survey's finding (3), not a refutation.
**Caveats:** A Pass-5 auditor CAN work where checks reduce to reliable external/mechanical feedback (quote string-matching, schema validation, retrieval-grounded NLI) or cross-context/cross-model critique.

#### C19. Self-correction works with reliable external feedback — 3-0, HIGH
**Claim:** Self-correction works well specifically where reliable external feedback exists (verifiable checks: code execution, exact quote matching) — supporting an auditor grounded in external verification.
**Source:** https://arxiv.org/abs/2406.01297 (finding 2, verbatim). Corroborating: CRITIC (Gou et al. ICLR 2024), Self-Debugging (Chen et al. 2023).
**Caveats:** "Exact quote matching" is the claim author's example, not the paper's (fits the paper's category as a deterministic check). "Specifically" shouldn't be read as excluding fine-tuned self-correction.

#### C20. Prior self-correction gains over-evaluated (oracle feedback, weak baselines) — 3-0, HIGH
**Claim:** Studies claiming self-correction gains often used impractical frameworks or unfair evaluations (oracle feedback, weak baselines) — headline improvements in the literature should be discounted when designing Pass 5.
**Source:** https://arxiv.org/abs/2406.01297 (verbatim) + https://arxiv.org/abs/2310.01798 (Reflexion-style gains depended on oracle stop-labels).
**Evidence:** Field consensus for prompted (non-RL-trained) self-correction as of 2026.

#### C21. Factored (fresh-context) verification beats joint (same-context) verification — 3-0, HIGH
**Claim:** Answering verification questions in a fresh context that does NOT see the original draft outperforms same-context verification, because models re-copy their own visible hallucinations — direct evidence a separate-context auditor beats in-context self-critique.
**Source:** Dhuliawala et al., "Chain-of-Verification Reduces Hallucination," Meta AI — https://arxiv.org/abs/2309.11495 (primary; ACL 2024 Findings)
**Evidence:** "Models that attend to existing hallucinations in the context from their own generations tend to repeat the hallucinations" (verbatim). FactScore: baseline 55.9, CoVe joint 60.8, factored 63.7, factor+revise 71.4. Factored prompts contain ONLY the questions — a direct ablation of draft visibility.
**Caveats:** Joint→factored gap alone is +2.9 (the 71.4 headline needs the extra factor+revise cross-check). Llama 65B few-shot (Sept 2023) — magnitudes on modern instruction-tuned models unproven. Covers factual hallucination, not reasoning errors. Scoped to same-model fresh-context; doesn't claim cross-model superiority. Contradiction hunt limited by search budget.

#### C22. CoVe effect sizes across tasks — 3-0, HIGH
**Claim:** With Llama 65B: longform biography FactScore 55.9→71.4 (~28% relative, factor+revise); MultiSpanQA F1 0.39→0.48 (~23%); Wikidata list precision 0.17→0.36.
**Source:** https://arxiv.org/abs/2309.11495 (Tables 1–3, verbatim verified)
**Caveats:** Best-variant-per-task, self-reported by method authors; 2023 base model — no transfer assumption to modern models asserted.

#### C23. Atomic verification questions ≫ open-ended generation accuracy — 3-0, HIGH
**Claim:** The same LLM answers targeted short-form verification questions far more accurately than it generates the same facts open-endedly: ~70% of entity verification questions correct vs ~17% precision in list generation — supporting decomposition of audits into atomic per-claim checks.
**Source:** https://arxiv.org/abs/2309.11495 (§4.3, verbatim; Llama 65B, Wikidata list-QA)
**Evidence:** Kamoi et al. TACL 2024 names "verification easier than generation + decomposable task" as exactly the regime where correction works.
**Caveats:** Model- and task-specific figures ("~" approximations); pairs generation precision with verification-question accuracy — related but distinct metrics.

#### C24. CriticGPT: trained critic preferred over human critiques 63% — 3-0, HIGH (verifier); single-source
**Claim:** An RLHF-trained critic (CriticGPT) produces critiques human evaluators prefer over human-written critiques in 63% of cases on naturally occurring LLM code errors — evidence a dedicated trained auditor beats unaided review.
**Source:** McAleese et al. (OpenAI), "LLM Critics Help Catch LLM Bugs" — https://arxiv.org/abs/2407.00215 (primary; not peer-reviewed; vendor self-evaluation)
**Evidence:** Judges blind to critique source; models caught more bugs than paid human reviewers; CriticGPT reduced nitpick/hallucination rates vs prompted ChatGPT; Human+CriticGPT teams hallucinate less than model alone.
**Caveats:** Human baseline = ChatGPT-training contractor pool ("does not represent the best possible human performance"); untrained ChatGPT critiques ALSO beat human critiques, so 63% isn't solely from critic training; critics nitpick and hallucinate bugs at higher rates than humans; short single-file snippets only. No credible refutation known through Jan 2026, but external sweep was limited.

---

## Round-level caveats

- **Angles 3–5 are unverified** — no surviving claims on grounding metrics (RAGAS/MiniCheck/AlignScore/ALCE), structured-output/long-context/injection, or production engineering (durable execution, batch pricing, parsers). Spec elements resting on those remain unaudited.
- **Model-era drift:** nearly all effect sizes measured on 2023–24 models (GPT-3.5/4/4o, Claude 3.x, Llama 2/65B). Direction of findings is corroborated into 2025–26; magnitudes on 2026 frontier reasoning models are extrapolation.
- **Verification completeness:** several verifiers exhausted their web-search budget and relied on primary-PDF verification plus known literature for the contradiction sweep (noted per-claim). Primary-source quote checks were completed in all cases.
- **One split vote:** C7 (self-enhancement under anonymization) passed 2-1; its substance is independently supported by C10–C12.
- **Single-source finding:** F8/C24 (CriticGPT) is an OpenAI self-report — treat as directional, MEDIUM confidence.
- **No judge-calibration claims survived** — the spec's `auditor_confidence` field has no evidential basis for being treated as calibrated.

## Open questions

1. Which groundedness checker (MiniCheck/Bespoke-MiniCheck vs AlignScore vs LLM-judge NLI) gives the best accuracy-per-dollar for Pass 5 checks 1 and 9 at pipeline scale? (Angle 3 — unverified.)
2. Does constrained JSON-schema decoding degrade the auditor's reasoning quality, and does long-context degradation bite at the spec's 20–50-unit batch sizes? (Angle 4 — unverified; §16 rests on assumption.)
3. Is any auditor-confidence signal (verbalized confidence, logprobs, self-consistency vote share) calibrated enough to drive the spec's `defer`/escalation thresholds?
4. Do 2026 reasoning-class models retain the measured magnitudes of position bias and self-recognition/self-preference, or do the 2023–24 effect sizes overstate the residual risk?
