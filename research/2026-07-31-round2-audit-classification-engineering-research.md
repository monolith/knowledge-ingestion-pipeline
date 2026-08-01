# Round 2 Design-Verification Research — Claim Relationships, Evidence Aggregation, Temporal Knowledge

**Date:** 2026-07-31 (persisted 2026-08-01)
**Informs:** [`SPECIFICATION.md`](/home/anatoly/knowledge_ingestion_pipeline_demo/docs/SPECIFICATION.md) — the 7-pass LLM knowledge-ingestion pipeline (Passes 3–5 primarily)
**Companion:** Round 1 research at [`2026-07-31-pipeline-design-verification-research.md`](/home/anatoly/knowledge-ingestion-plugin/research/2026-07-31-pipeline-design-verification-research.md) (atomic extraction, routing/retrieval — not repeated here)
**Method:** multi-agent fan-out research with 3-vote adversarial verification per claim. 23 claims survived; 2 were refuted and are listed at the bottom for transparency.

## Coverage note (important)

Round 2 was scoped to five angles: (1) claim relationship classification, (2) evidence aggregation + temporal knowledge, (3) LLM-as-judge / adversarial audit, (4) grounding / citation verification, (5) production pipeline engineering. **The surviving verified claim set covers only angles 1 and 2.** No claims for angles 3–5 (judge biases, self-correction limits, RAGAS/MiniCheck-style groundedness checkers, structured-output effects, long-context degradation, prompt-injection defenses, durable execution, batch economics) survived into this batch. Those areas remain unverified and need a follow-up round before the corresponding spec passes (Pass 5, Pass 0/6) can claim evidence backing.

---

## Executive summary

The evidence strongly validates the spec's two-stage retrieve-then-judge design for Pass 3: unguided whole-document contradiction detection is near chance (GPT-4 53.8% accuracy, 8% recall on ContraDoc; GPT-4o still only ~0.68 in a 2026 re-evaluation), while localized judgment with a candidate in hand jumps to 77.2% and flagged contradictions carry 88% precision with 92.7% correct evidence localization. The spec's 15-label relationship vocabulary, however, exceeds anything the literature validates — benchmarks only support coarse 3-way stance (Supports/Refutes/NEI), fine-grained contradiction-type classification peaked at 0.401 accuracy in the one study that measured it, and "partial/conflicting" labels are consistently the weakest class everywhere they appear — so the pipeline should judge coarse first and sub-type in a constrained second step, treating the spec's 4-bucket grouping as the reliability boundary. Realistic accuracy expectations for automated claim-relationship classification are ~70–80%, and fine-tuned classifiers collapse out-of-domain (0.945→0.42 macro-F1; 0.88→0.44 F1), supporting the spec's prompted-frontier-LLM approach over fine-tuning. For Passes 3–4, Zep/Graphiti's bi-temporal invalidate-don't-delete pattern is shipped precedent for the spec's temporal_update handling, JAMA-published citation-contamination data (32.2% of paper-mill citations occur post-retraction) argues for adding automated retraction/validity screening to §10.4 evidence weighting, and the otto-SR preprint shows LLM evidence synthesis can match or beat human reviewers — and that re-aggregation materially flips statistical conclusions (3 of 12 Cochrane reviews).

---

## Findings

### F1. Unguided contradiction detection is near-chance; localized judgment works — the spec's two-stage design (§10.2) is validated — HIGH

**Merged claims:** #0, #1, #9

- **ContraDoc (NAACL 2024, Table 2):** open-ended binary judgment of whether a long document self-contradicts is ~50–54% accuracy across GPT-3.5 / GPT-4 / PaLM2 / LLaMA-2 (GPT-4: 53.8% acc, 8.0% recall). Paper: "the models have a near-random performance."
- **Same benchmark, guided condition:** given the evidence sentence, GPT-4 finds the contradictory counterpart 77.2% of the time (GPT-3.5: 51.6%). Intermediate condition (told a contradiction exists): 70.2% evidence-hit-rate vs 16% random. The gradient random → 70.2% → 77.2% directly supports localizing candidates before the LLM judges the relationship.
- **2026 follow-up (arXiv 2601.02627, Jan/Apr 2026, 891-doc ContraDoc):** GPT-4o reaches only 0.680 accuracy / 0.697 F1 on binary inconsistency classification; LLaMA3.2-90B 0.681 / 0.657; GPT-4o evidence localization 0.54–0.57 hit rate. Document-level inconsistency detection is **not solved by newer models**.

**Spec implication:** Pass 3's candidate-matching-then-relationship-judgment structure is the right shape. Never ask the model "does this cluster contain contradictions?" open-endedly; always present retrieved candidate pairs.

Sources: https://aclanthology.org/2024.naacl-long.362.pdf · https://arxiv.org/pdf/2601.02627

### F2. LLM "contradicts" verdicts are high-precision / low-recall — trust flags with quoted evidence, never trust silence — HIGH

**Merged claims:** #2 (plus #9's localization figures)

- **ContraDoc Judge-then-Find (Table 4):** GPT-4 flags only 19.6% of truly contradictory documents (conservative), but with 88% yes/no precision, and it locates the correct evidence in 92.7% of documents it flags. "Even though GPT4 might only be able to find 19.6% of the CONTRADOC-POS, it can provide the correct evidence for 92.7% of them."

**Spec implication:** require every `contradicts`-family verdict in Pass 3 to carry quoted evidence spans (the assessment schema's unit-ID lists should be backed by excerpts); treat *absence* of a contradiction flag as weak evidence of consistency, not proof — recall is the failure mode, not precision.

Source: https://aclanthology.org/2024.naacl-long.362.pdf

### F3. Fine-grained relationship taxonomies are the least reliable part — benchmarks only validate coarse 3-way stance — HIGH

**Merged claims:** #3, #6, #8, #11

- **Task formulation (MultiVerS, Findings of NAACL 2022):** SciFact/HealthVer/COVIDFact define scientific claim verification as 3-way document-level stance (Supports/Refutes/NEI) + rationale selection. No established benchmark validates labels like `partially_contradicts` or `temporal_update`.
- **Contradiction-TYPE classification (arXiv 2504.00180, Amazon, Mar 2025):** best type-detection accuracy was **0.401** (Claude-3 Sonnet, basic prompting; 3-class chance ≈ 0.333) vs 0.710 for binary detection — and chain-of-thought *degraded* type classification ("performance drops ranging from 8% for Claude models up to 25% for Llama 70B").
- **"Conflicting" label (CheckThat! 2025 Task 3, arXiv 2509.11492):** the ambiguous/partially-supportive/contradictory class scored ~0.50 F1 vs 0.83 for clear False (zero-shot validation); best fine-tuned model: 0.32 Conflicting vs 0.73 False at test. Corroborated by DS@GT on the same task (Conflicting 0.36 vs False 0.81).
- **CONTRADICT hardest class (Košprdić et al., KMIS 2024):** highest misclassification rate (22% vs ~8% for other classes); genuine contradictions missed because surface keyword overlap makes contradicting claims look like supporting ones.

**Spec implication (evidence contradicts spec §10.3 as written):** the 15-label vocabulary (`supports`, `contradicts`, `partially_contradicts`, `scope_difference`, `temporal_update`, `methodological_qualification`, …) is far beyond validated reliability. Concrete recommendation: two-step judgment — first coarse (supports / contradicts / neither, ~70–80% achievable), then a *separate constrained* sub-typing prompt for pairs judged contradicts-family; surface the spec's own 4-bucket grouping (convergent / contested / singleton / complementary) as the trust boundary for downstream decisions, treating fine labels as advisory annotations with explicitly lower confidence. Avoid free CoT for the sub-typing step (it hurt type classification in the one study measuring it).

Sources: https://aclanthology.org/2022.findings-naacl.6.pdf · https://arxiv.org/pdf/2504.00180 · https://arxiv.org/pdf/2509.11492 · https://www.scitepress.org/Papers/2024/129000/129000.pdf

### F4. Realistic accuracy band for automated claim-relationship classification: ~70–80%, not 95%+ — HIGH

**Merged claims:** #4, #7, #10

- **MultiVerS (2022 SOTA, fully supervised):** 72.5 abstract-level F1 on SciFact, 77.6 HealthVer, 77.3 COVIDFact. SciFact-Open shows a further ≥15-F1 drop moving to open-domain retrieval — the closed-setting numbers are *optimistic* for deployment.
- **RAG contradiction detection (arXiv 2504.00180):** best configuration (Claude-3 Sonnet + CoT) reached 0.710 accuracy at detecting whether retrieved-document-set contradictions exist; wide variance by contradiction type (self-contradictions 0.006–0.456 vs pair contradictions up to 0.893).
- **Fine-tuned in-domain ceiling (Košprdić et al. 2024):** DeBERTa-Large fine-tuned on SciFact hit 0.88 F1, beating zero-shot GPT-4 (0.81), GPT-4 Turbo/GPT-4o (0.79) on the same 122-example test set — in-domain fine-tuning helps, but see F5.

**Spec implication:** Pass 3 confidence/uncertainty fields should be calibrated to a ~70–80% base-rate expectation; downstream passes (4–5) must be designed to absorb 20–30% relationship-classification error, e.g. by preserving disagreement (which §10.1 already mandates) rather than resolving it.

Sources: https://aclanthology.org/2022.findings-naacl.6.pdf · https://arxiv.org/pdf/2504.00180 · https://www.scitepress.org/Papers/2024/129000/129000.pdf

### F5. Fine-tuned claim classifiers collapse out-of-distribution — the spec's prompted-LLM approach is the right default — HIGH

**Merged claims:** #5, #12 (with #10 as the in-domain counterpoint)

- **CheckThat! 2025 (arXiv 2509.11492):** LoRA-fine-tuned LLaMA hit 0.945 macro-F1 on English validation, then **collapsed to 0.42** on the official test set (True-F1 0.899→0.232); authors attribute it to overfitting and shifted evidence structure. Fine-tuned RoBERTa dropped similarly (0.59→0.35); at test time fine-tuning barely beat zero-shot prompting (0.42 vs 0.40–0.41).
- **Košprdić et al. 2024 cross-domain:** DeBERTa fine-tuned on SciFact fell from 0.88 in-domain to 0.44 weighted F1 (0.50 accuracy) on HealthVer — a halving. Retraining on 90% of SciFact only recovered 0.48.

**Spec implication:** for a general-purpose ingester consuming heterogeneous documents, do not fine-tune the Pass 3 relationship judge; prompted frontier models degrade more gracefully across domains. Fine-tuning is only defensible with a locked, in-domain document distribution plus a held-out OOD eval.

Sources: https://arxiv.org/pdf/2509.11492 · https://www.scitepress.org/Papers/2024/129000/129000.pdf

### F6. Bi-temporal, invalidate-don't-delete knowledge graphs (Zep/Graphiti) are shipped precedent for the spec's temporal handling — HIGH

**Merged claims:** #13, #14

- **Zep (arXiv 2501.13956, Jan 2025) + Graphiti (getzep/graphiti, 29k+ stars, maintained into 2026):** bi-temporal model — event timeline T (t_valid/t_invalid on edges) separate from transactional ingestion timeline T′ (t′_created/t′_expired). On detecting temporally overlapping contradictions, the outdated edge's t_invalid is set to the new edge's t_valid — **invalidated, not deleted**: "old facts are invalidated — not deleted… query what was true at any point in time."

**Spec implication:** Pass 4's `temporal_update` handling and knowledge-state lifecycle should adopt this exact pattern: never destructive updates; superseded leaves get closed validity ranges, keeping the historical record queryable. This is architecture verifiable in open-source code, not a vendor benchmark claim.

Sources: https://arxiv.org/abs/2501.13956 · https://github.com/getzep/graphiti

### F7. Structured temporal retrieval beat full-context stuffing on LongMemEval — supportive, but vendor-run — HIGH (with vendor caveat)

**Merged claims:** #15

- **Zep on LongMemEval-S:** gpt-4o-mini 63.8% vs 55.4% full-context baseline (3.20s vs 31.3s latency, ~90% cut); gpt-4o 71.2% vs 60.2% — up to 18.5% *relative* accuracy improvement. Baseline fairness cross-checked: the independent LongMemEval paper (arXiv 2410.10813, ICLR 2025) reports gpt-4o full-context at 60.6%, matching Zep's 60.2% baseline — not sandbagged.
- Not uniform: Zep *underperformed* the baseline on single-session-assistant questions (−17.7% rel.) and knowledge-update with gpt-4o-mini (−3.36%). Latency excludes graph-ingestion cost. All authors are Zep employees; non-peer-reviewed preprint.

**Spec implication:** supports the spec's bet that a structured knowledge store outperforms re-reading full history, but the per-question-type splits warn that knowledge-*update* queries are exactly where structured memory is weakest — Pass 4's update logic deserves its own eval rather than inherited confidence.

Sources: https://arxiv.org/abs/2501.13956 · https://arxiv.org/abs/2410.10813

### F8. Citation contamination is real and survives retraction — automated source-validity screening belongs in §10.4 evidence weighting — HIGH

**Merged claims:** #16, #17, #18

- **Tang & Cai, JAMA Network Open, June 12 2025 (PMC12163679):** across ~200,000 life-science systematic reviews, 299 (0.15%) cited retracted paper-mill articles in their evidence synthesis; contamination rising over time; one contaminated review fed a US federal WTC-health regulation.
- **Retraction doesn't stop it:** of 385 citations to paper-mill articles, 124 (32.2%) occurred *after* retraction, 13 more than 500 days after — human aggregators do not consistently verify source validity.
- **Authors' recommendation:** citation-screening tools during review; "developing automated detection tools are essential to preserving the credibility of systematic reviews."

**Spec implication (evidence improves on spec):** §10.4's weighting criteria ("whether one source is merely a summary of another," source authority) should gain an explicit machine check: retraction/validity status lookup (Retraction Watch/Crossref) for cited studies, and provenance tracking to distinguish `convergent_independent` from `convergent_dependent` — the contamination data shows dependence and invalidity are common and silently propagate through aggregation.

Source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12163679/

### F9. LLM evidence synthesis can match/exceed human reviewers, and re-aggregation materially flips conclusions — MEDIUM (single vendor preprint)

**Merged claims:** #19, #20, #21, #22

- **otto-SR (medRxiv preprint, June 13 2025, DOI 10.1101/2025.06.13.25329541; authors include Moher, Tricco, Detsky, Church):**
  - Screening, 32,357 citations / 5 reviews: 96.7% sensitivity vs 81.7% human, at equal specificity (97.9% vs 98.1%). [3-0 vote]
  - Data extraction, 4,495 data points / 495 studies / 7 reviews: 93.1% vs 79.7% human accuracy, blinded-adjudication reference. [2-1 vote — finer figures unverifiable behind Cloudflare; headline numbers independently confirmed via Semantic Scholar abstract]
  - Reproducing/updating a full Cochrane issue (12 reviews, 146,276 citations): median 0 incorrectly excluded studies (IQR 0–0.25); found nearly 2× the eligible studies of the original authors (114 vs 64). [3-0]
  - **Conclusion flips:** after dual human review of outputs, updated meta-analyses yielded newly significant effects in 2 reviews and negated significance in 1 — 3 of 12 flipped. [3-0]

**Spec implication:** supports the viability of Passes 3–4's automated synthesis ambition, and the 3/12 flip rate is direct evidence that the spec's knowledge-state lifecycle (established/contested) must expect *material* state transitions on update — knowledge states are not sticky. Weight: preprint, self-evaluation by the tool's creators, human comparator structurally disadvantaged in phase 1 (single graduate-level abstract screener vs full-text-derived gold standard).

Source: https://www.medrxiv.org/content/10.1101/2025.06.13.25329541v1

---

## Full verified claim set (traceability)

Claim numbers are from the round-2 adversarial verification batch. All quotes verified verbatim against primary sources unless noted.

| # | Claim (condensed) | Vote | Conf | Source |
|---|---|---|---|---|
| 0 | Open-ended binary self-contradiction judgment near chance for GPT-3.5/GPT-4/PaLM2/LLaMA-2 (~50–54%; GPT-4 53.8% acc, 8.0% recall) | 3-0 | high | ContraDoc, NAACL 2024 |
| 1 | Given the evidence sentence, GPT-4 finds the contradictory counterpart 77.2% (GPT-3.5 51.6%) — supports retrieve-then-judge | 3-0 | high | ContraDoc, NAACL 2024 |
| 2 | Judge-then-Find: GPT-4 flags 19.6% of contradictory docs, 88% precision, 92.7% evidence hit on flags | 3-0 | high | ContraDoc, NAACL 2024 |
| 3 | SciFact/HealthVer/COVIDFact validate only 3-way stance + rationale; no fine-grained relationship types | 3-0 | high | MultiVerS, Findings NAACL 2022 |
| 4 | MultiVerS fully supervised: 72.5/77.6/77.3 abstract F1 — realistic reliability band ~70–80 | 3-0 | high | MultiVerS, Findings NAACL 2022 |
| 5 | CheckThat! 2025: LoRA-LLaMA 0.945 val → 0.42 test macro-F1 (overfitting/evidence-structure shift) | 3-0 | high | arXiv 2509.11492 |
| 6 | "Conflicting" class much harder than True/False (0.50 vs 0.83 val; 0.32 vs 0.73 test) | 3-0 | high | arXiv 2509.11492 (+ DS@GT 2507.06195) |
| 7 | Contradiction detection over retrieved sets: best 0.710 accuracy (Claude-3 Sonnet + CoT), wide variance by type | 3-0 | high | arXiv 2504.00180 |
| 8 | Contradiction TYPE classification best 0.401; CoT degrades it (−8% Claude, −25% Llama-70B) | 3-0 | high | arXiv 2504.00180 |
| 9 | 2026 ContraDoc re-eval: GPT-4o ~0.68 acc / 0.70 F1; evidence localization 0.54–0.57 — unsolved | 3-0 | high | arXiv 2601.02627 |
| 10 | Fine-tuned DeBERTa-Large 0.88 F1 beats zero-shot GPT-4 0.81 / Turbo & 4o 0.79 on SciFact (n=122) | 3-0 | high | Košprdić et al., KMIS 2024 |
| 11 | CONTRADICT hardest class (22% error); surface keyword overlap masks contradictions as support | 3-0 | medium | Košprdić et al., KMIS 2024 |
| 12 | OOD collapse: DeBERTa 0.88 (SciFact) → 0.44 F1 (HealthVer); 90%-retrain recovers only 0.48 | 3-0 | high | Košprdić et al., KMIS 2024 |
| 13 | Zep/Graphiti bi-temporal model: t_valid/t_invalid separate from transactional timestamps | 3-0 | high | arXiv 2501.13956 + getzep/graphiti |
| 14 | Contradiction → invalidate edge (t_invalid := new t_valid), never delete; history preserved | 3-0 | high | arXiv 2501.13956 + getzep/graphiti |
| 15 | Zep beats full-context on LongMemEval (63.8 vs 55.4 gpt-4o-mini; ~90% latency cut); vendor-run, baseline independently corroborated | 3-0 | high* | arXiv 2501.13956 (+2410.10813) |
| 16 | Paper-mill articles contaminate systematic reviews via evidence synthesis, biasing downstream practice | 3-0 | high | JAMA Netw Open 2025, PMC12163679 |
| 17 | 32.2% of citations to paper-mill articles occurred post-retraction (13 >500 days later) | 3-0 | high | JAMA Netw Open 2025, PMC12163679 |
| 18 | Authors: automated citation-screening/detection tools essential to review credibility | 3-0 | high | JAMA Netw Open 2025, PMC12163679 |
| 19 | otto-SR screening: 96.7% vs 81.7% human sensitivity at ~equal specificity (32,357 citations) | 3-0 | high** | medRxiv 10.1101/2025.06.13.25329541 |
| 20 | otto-SR extraction: 93.1% vs 79.7% human accuracy (4,495 data points) | 2-1 | medium | medRxiv 10.1101/2025.06.13.25329541 |
| 21 | Cochrane reproduction: median 0 wrongly excluded (IQR 0–0.25); 114 vs 64 eligible studies found | 3-0 | high** | medRxiv 10.1101/2025.06.13.25329541 |
| 22 | Updated meta-analyses flipped significance in 3 of 12 Cochrane reviews (2 newly significant, 1 negated) | 3-0 | high** | medRxiv 10.1101/2025.06.13.25329541 |

\* vendor self-report; architecture claims (13–14) code-verifiable, benchmark claim (15) not peer-reviewed.
\** verbatim-verified against the preprint, but the preprint itself is non-peer-reviewed self-evaluation; treat group-level confidence as medium for design decisions.

### Per-claim evidence detail

**#0 — Unguided detection near chance.** ContraDoc (arXiv 2311.09182 / NAACL 2024), Table 2, CONTRADOC-POS+NEG: GPT-4 53.8% acc / 8.0% recall; GPT-3.5 50.1% / 0.2%; PaLM2 52.0% / 13.4%; LLaMA-2 50.5% / 38.3%. GPT models biased to "No" (97–100% precision, tiny recall); LLaMA-2 biased to "Yes." Verbatim: "the models have a near-random performance." Citation scan found no re-evaluation refuting this and no counter-paper. *Caveat:* 2023-era models — read as an argument for guided comparison, not a measured property of 2026 frontier models (see #9 for the 2026 partial update).

**#1 — Localized judgment 77.2%.** Same paper, §5: "GPT3.5 can detect 51.6% of the cases, while GPT4 can detect 77.2% of them… LLMs do reasonably well in document-level contradiction detection if the exact sentence with contradiction is pointed out but not so otherwise." Intermediate Top-k condition: GPT-4 70.2% EHR vs 16% random. *Caveat:* within-document self-contradiction, not a retrieval pipeline — extension to retrieve-then-judge is inferential but direct.

**#2 — High precision on flags.** Same paper, Table 4 (gpt-4-0613): precision 88.0%, TP rate 19.6%, evidence hit 92.7%, best real-accuracy of four models. *Caveats:* 19.6% is TP over the full set (recall over positives ≈39% — imprecision originates in the paper's own prose); 2.7% FP rate means a small share of "yes" verdicts are wrong outright.

**#3 — Only coarse taxonomy validated.** MultiVerS abstract, verbatim: task = "label scientific documents which Support or Refute an input claim, and to select evidentiary sentences." Unified y ∈ {SUPPORTS, REFUTES, NEI}. Nearest counter-evidence (WICE's "partially supported," EMNLP 2023) is Wikipedia entailment, not scientific claims, and partial *support*, not partial contradiction. *Caveats:* COVIDFact natively 2-way (mapped to 3); HealthVer/COVIDFact rationales reconstructed, not natively annotated.

**#4 — ~70s F1 ceiling.** MultiVerS Table 2, fully supervised: SciFact 72.5 (67.2 sentence), HealthVer 77.6 (69.1), COVIDFact 77.3 (43.7). SOTA at publication (vs Vert5Erini 68.2, ParagraphJoint 69.1). SciFact-Open (arXiv 2210.13777): ≥15 F1 drop in open-domain retrieval over 500K abstracts — closed-setting numbers are optimistic. *Caveats:* abstract-level F1 bundles retrieval + labeling; "ceiling" is a 2022-anchored expectation band (~70–80), not a proven cap for 2026 models; GPT-4-class zero-shot label-only results reach high-70s/low-80s.

**#5 — OOD collapse of fine-tuned LLaMA.** ClaimIQ at CheckThat! 2025 (arXiv 2509.11492): Table 2 val macro-F1 0.945; Tables 3–4 official test 0.42; True-F1 0.899→0.232. Authors: "may have overfit… or faced difficulties adapting to shifts in evidence structure and language style." RoBERTa also dropped 0.59→0.35; fine-tuned barely beat zero-shot at test (0.42 vs 0.40–0.41). *Caveats:* "validation" was the team's own 90/10 split (in-distribution); Task 3 is True/False/Conflicting — analogous to, not identical with, a supports/contradicts taxonomy. Note: an initial small-model WebFetch summary hallucinated different numbers (0.62/0.58); direct PDF reading corrected it.

**#6 — Conflicting class hardest.** Same paper: label definition verbatim "the evidence is ambiguous, partially supportive, or contradictory." Val: prompted LLaMA Conflicting F1 0.496 vs False 0.832. Test: LoRA row 0.23 (True) / 0.73 (False) / 0.32 (Conflicting). Independently corroborated by DS@GT (arXiv 2507.06195): Conflicting 0.36 vs False 0.81, attributed to True/Conflicting overlap in embedding space. *Caveats:* at test time True (0.23) was even lower than Conflicting — everything but False collapsed; ClaimIQ was mid-pack (DS@GT 4th at 0.52 test macro).

**#7 — Retrieved-set contradiction detection 0.710.** arXiv 2504.00180 (Amazon, Mar 2025), Table 3: Claude-3 Sonnet + CoT 0.710 (best); Sonnet basic 0.539; Haiku 0.395/0.578; Llama-3.3-70B 0.679/0.497; Llama-3.1-8B 0.380/0.482. Self-contradictions 0.006–0.456 vs pair contradictions up to 0.893. *Caveat:* tested models were not frontier even in Mar 2025 (no Claude 3.5, GPT-4o, o1) — evidence the task is hard, not a current SOTA ceiling.

**#8 — Type classification 0.401, CoT hurts.** Same paper, Table 3: type-detection best Claude-3 Sonnet basic 0.401 acc / 0.216 macro-F1 (chance ~0.333); verbatim "performance drops ranging from 8% for Claude models up to 25% for Llama 70B" for CoT on type detection (Sonnet 0.401→0.368). *Caveats:* CoT degraded most-not-all models (Llama-3.1-8B acc rose while macro-F1 collapsed 0.163→0.056); paper's taxonomy is self/pair/conditional, not the spec's — relevance to §10.3 is inferential; preprint.

**#9 — 2026: still unsolved.** arXiv 2601.02627 (Tan et al., submitted 2026-01-06, rev 2026-04-08), 891 docs (449 inconsistent/442 consistent), Table 5 direct prompting: GPT-4o 0.680 acc / 0.697 F1; LLaMA3.2-90B 0.681 / 0.657. GPT-4o EHR 0.536 (DP) → 0.571 (best method). *Caveats:* quote splices DP accuracy with best-method EHR from different rows; GPT-4o/LLaMA3.2 are not 2026 frontier reasoning models. (The paper's own redact-and-retry method claim was REFUTED 0-3 in verification — only these baseline numbers survived.)

**#10 — Fine-tuned beats zero-shot in-domain.** Košprdić et al. 2024 (KMIS/IC3K, SCITEPRESS, DOI 10.5220/0012900000003838), Table 3 weighted-avg F1: DeBERTa_SF 0.88, GPT-4 0.81, GPT-4 Turbo 0.79, GPT-4o 0.79; same 122-example test set, zero-shot (temp 0). *Caveats:* n=122 (only 27 CONTRADICT), no significance tests; asymmetric comparison by design; minimal GPT prompts (no few-shot/CoT); do NOT generalize to "fine-tuned beats frontier LLMs today."

**#11 — CONTRADICT hardest, surface-overlap mechanism.** Same paper, §6: 6/27 CONTRADICT errors (22%) vs ~8% other classes; verbatim "the model may overlook clear contradictions in the evidence, relying instead on generalizations stemming from the presence of related terms." *Caveats (medium conf):* coarse 3-class task — extrapolation to fine-grained labels is inferred; error analysis on DeBERTa with 14 total errors, though GPT-4 performed worse overall, making the inference conservative for LLM pipelines.

**#12 — Cross-domain halving.** Same paper, Table 2: DeBERTaSF-80 on HealthVer: wa-F1 0.44 / acc 0.50; DeBERTaSF-90: 0.48 / 0.52. Verbatim confirmed. *Caveats:* the paper frames this positively (beats prior SOTA Sarrouti BERT F1 0.36 and GPT-4 zero-shot OOD); single train/test pair — but aligned with established cross-domain NLI degradation literature.

**#13 — Bi-temporal model.** arXiv 2501.13956 §2.1 verbatim: "Zep implements a bi-temporal model, where timeline T represents the chronological ordering of events, and timeline T′ represents the transactional order of Zep's data ingestion." §2.2.3: four timestamps (t′_created, t′_expired, t_valid, t_invalid) on edges. Corroborated by shipped code (getzep/graphiti). *Note:* the known Letta/MemGPT dispute over Zep targets LoCoMo performance claims, not this architecture.

**#14 — Invalidate, don't delete.** Same paper verbatim: "When the system identifies temporally overlapping contradictions, it invalidates the affected edges by setting their t_invalid to the t_valid of the invalidating edge." Graphiti README: "old facts are invalidated — not deleted… Query what's true now, or what was true at any point in time." Mechanism description by the system's authors, verifiable in code.

**#15 — LongMemEval result.** Same paper, LongMemEval-S: gpt-4o-mini 63.8% vs 55.4% (3.20s vs 31.3s); gpt-4o 71.2% vs 60.2% (2.58s vs 28.9s). 15.2%/18.5% are relative improvements; 3.20/31.3 = 89.8% latency cut. Independent cross-check: LongMemEval paper (arXiv 2410.10813, ICLR 2025) reports gpt-4o full-context 60.6% — Zep's baseline was fair. *Caveats:* all-author vendor preprint; Zep LOST on single-session-assistant (−17.7% rel) and knowledge-update w/ gpt-4o-mini (−3.36%); latency excludes ingestion.

**#16–18 — Citation contamination trilogy.** Tang & Cai, JAMA Network Open, 2025-06-12 (PMC12163679), cross-sectional study of ~200,000 life-science systematic reviews: 299 (0.15%) cited retracted paper-mill articles in evidence synthesis; contamination rising; 124/385 citations (32.2%) post-retraction, 13 (3.4%) >500 days after (range: 2773 days before to 1306 after); oncology most affected; one contaminated review cited in a US federal WTC-health regulation. Verbatim: "Correcting contaminated reviews and developing automated detection tools are essential to preserving the credibility of systematic reviews"; recommends "citation-screening tools during the review process." *Caveats:* source hedges "may compromise" where claim #16 states flatly; study concerns human reviewers — application to LLM pipelines is motivational analogy, correctly framed.

**#19–22 — otto-SR.** Cao et al., "Automation of Systematic Reviews with Large Language Models," medRxiv 2025-06-13 (DOI 10.1101/2025.06.13.25329541; authors incl. Moher, Tricco, Detsky, Church). Verified verbatim via Europe PMC (PPR1035179) and medRxiv API after Cloudflare blocked direct fetch. Phase 1 (screening, 32,357 citations/5 reviews, reference = original reviews' post-full-text decisions): otto-SR 96.7% sens / 97.9% spec vs human 81.7% / 98.1%. Phase 2 (extraction): 93.1% vs 79.7% accuracy [2-1 vote: the 4,495-data-points/495-studies/blinded-adjudication specifics could not be independently confirmed beyond the abstract]. Phase 4 (12 Cochrane reviews, 146,276 citations): median 0 incorrectly excluded (IQR 0–0.25); 114 vs 64 eligible studies; whole issue reproduced in ~2 days; after dual human review, 2 reviews newly significant + 1 negated = 3/12 conclusion flips. *Caveats (all four):* non-peer-reviewed preprint; self-evaluation by the tool's creators; phase-1 human comparator structurally disadvantaged (single grad-level abstract screener vs full-text gold standard); "LLM-driven re-aggregation" is shorthand — LLM did screening/extraction, pooling was conventional statistics with human verification of discrepancies; abstract omits specificity-side error detail for the Cochrane phase.

---

## Refuted claims (transparency)

1. **"Joint full-document encoding (MultiVerS-style) outperforms extract-then-label pipelines"** — vote 1-2. The MultiVerS comparison did not cleanly establish this for the spec's setting; do not cite it as justification for single-pass whole-document judgment.
2. **"Redact-and-retry iterative prompting outperforms direct prompting for extracting inconsistency evidence"** (arXiv 2601.02627's method claim) — vote 0-3. Only that paper's *baseline* measurements (claim #9) survived; its proposed method's superiority did not verify. Do not adopt redact-and-retry on this evidence.

---

## Spec decisions: contradicted, improved, or confirmed

| Spec element | Verdict | Evidence |
|---|---|---|
| §10.2 two-stage comparison (candidate matching → relationship judgment) | **Confirmed** | F1: near-chance unguided vs 77.2% localized (ContraDoc); 2026 re-eval unchanged |
| §10.3 15-label relationship vocabulary judged in one step | **Contradicted as-is** | F3: type classification 0.401 best; Conflicting/partial labels weakest everywhere; recommend coarse-first + constrained sub-typing; treat 4-bucket grouping as the trust boundary |
| Pass 3 confidence expectations | **Calibration needed** | F4: plan for ~70–80% relationship accuracy; design Passes 4–5 to absorb 20–30% error |
| Any temptation to fine-tune the Pass 3 judge | **Contradicted** | F5: 0.945→0.42 and 0.88→0.44 OOD collapses; prompted frontier LLM is the right default |
| `contradicts` verdicts + evidence excerpts | **Improved** | F2: require quoted evidence with every contradicts-family verdict; treat non-flags as weak evidence only |
| Pass 4 `temporal_update` / lifecycle | **Confirmed + concrete pattern** | F6: adopt Graphiti's bi-temporal invalidate-don't-delete (t_valid/t_invalid vs transaction time) |
| §10.4 evidence weighting | **Improved** | F8: add automated retraction/validity screening and source-dependence (citation-lineage) checks |
| Knowledge-state lifecycle stickiness | **Improved** | F9: 3/12 Cochrane conclusion flips on update — expect material established↔contested transitions |
| CoT prompting for relationship sub-typing | **Contradicted (weakly)** | F3/#8: CoT degraded type classification in the one study measuring it — validate before defaulting to CoT there |

---

## Caveats

- **Coverage gap is the biggest one:** angles 3 (LLM-as-judge/audit), 4 (grounding/citation verification), and 5 (production engineering) produced **no surviving verified claims** in this round. Pass 5's audit design and Pass 0/6 engineering choices remain evidence-unverified. Round 1 covered extraction and routing; a round 3 is needed for judge-bias, groundedness-checker, and pipeline-engineering evidence.
- **Model vintage:** ContraDoc numbers are 2023-era models; the Amazon RAG study used Claude-3-generation models. The 2026 re-eval (#9) shows GPT-4o still weak, but no surviving claim tests frontier *reasoning* models (o1/o3, Claude 4-class) on these tasks.
- **otto-SR (F9)** is a non-peer-reviewed preprint, self-evaluated by its creators, with one 2-1 vote; its human-comparator framing structurally favors the tool in phase 1.
- **Zep's benchmark claim (F7)** is vendor-run (architecture claims F6 are code-verifiable and safe).
- Several verifications noted **exhausted search budgets** before exhaustive 2026 counter-evidence sweeps — confidence is "high" per protocol, not absolute.
- Two claims were **refuted** in verification (see above); the redact-and-retry refutation means #9's source paper should be cited only for its baseline numbers.

## Open questions

1. Do 2026 frontier *reasoning* models (o1/o3-class, Claude 4-class) close the unguided contradiction-detection gap? No re-evaluation exists in the surviving set — GPT-4o (still ~0.68) is the newest tested model.
2. What is the empirical reliability of the spec's *specific* 15-label vocabulary? No benchmark tests it; a small in-house labeled eval (few hundred pairs from target document domains) is the only way to get per-label confusion data before trusting fine labels in Pass 4 decisions.
3. Can source independence (`convergent_independent` vs `convergent_dependent`) be detected automatically at acceptable accuracy? The contamination evidence motivates it strongly, but no automated method was verified this round.
4. Angles 3–5 wholesale: judge-bias magnitudes (position/verbosity/self-preference), self-correction limits, MiniCheck/AlignScore-class groundedness checkers at production scale, structured-output quality effects, long-context batch-size limits for the spec's 20–50-unit comparisons, and prompt-injection defenses for ingestion — all still unanswered for this spec.
