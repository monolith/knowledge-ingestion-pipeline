---
title: Classifier design — cross-model consistency and chat statements (Run C)
date: 2026-08-10
status: COMPLETE — 3-vote adversarially verified
run: wf_d873c0e9-e59
---

# Classifier Design Research — Run C (complete)

106 agents, 24 sources, 118 claims extracted, 25 verified 3-vote → **17 confirmed, 8 refuted**, 12 findings after synthesis.

Every claim below survived 3-vote adversarial verification. Refuted claims are named
inline where they qualify a finding — those must never be cited as support.

## Executive summary

Cross-model label consistency is overwhelmingly a property of the label set and the prompt, not
of the models. Agreement between model families applying the same codebook ranges from mean
Cohen's kappa 0.23 (121 fine-grained, largely interpretive/multiclass features) up to 0.53-0.75
and Krippendorff's alpha 0.80-0.95 (small binary or concrete label sets) — a design effect
roughly an order of magnitude larger than model choice, and one that flips the human-vs-LLM
comparison in both directions across studies. Two levers carry most of it: binary
presence/absence probes instead of one multiclass call (multiclass features had 90% lower odds
of correct detection, OR 0.10, 95% CI 0.03-0.35) and label definitions anchored in surface-
observable criteria rather than judgment calls (F1 above 0.60 vs below 0.30). For chat
statements the literature is thin and does not yet answer the question: the two conversational
studies that survived verification measure LLM-versus-human agreement (weighted kappa median
0.60 on support conversations; 0.38-0.58 on classroom utterances against a human ceiling above
0.90) and neither reports cross-model agreement on conversational text, while
decontextualization, utterance segmentation, and context-window sizing produced no confirmed
evidence at all. Finally, agreement is not correctness: four frontier models agreed on 96.1% of
sarcasm labels with chance-corrected Fleiss kappa of -0.001 while missing 75% of sarcastic
instances, so any design must be validated against human labels rather than against inter-model
consensus.

## Findings

### F1. [HIGH] Cross-family agreement on a fixed label set is dominated by label-set design, not by which models you use — the same measurement (chance-corrected inter-model agreement) spans kappa 0.23 to 0.75 across studies, and whether LLMs beat or lose to human coders flips with the label design.

*Vote: merged 3-0 / 3-0 / 3-0*

Three primary sources, all unanimously confirmed, point in incompatible directions until you
condition on label design. (a) 2601.12099 (Goodall/Shilton/Mullins/Whitehouse, Jan 2026): 7 LLMs
x 121 ritual features x 567 ethnographic excerpts, mean LLM-LLM Cohen's kappa 0.233 vs human-
human 0.573 (matched on the 6 double-coded features; LLM figure is the mean over all 21 model
pairs spanning Qwen 3 4B, Llama 3.2 3B, GPT-OSS 120B, DeepSeek V3.1, GPT-5 Nano, Claude Sonnet
4.5, Perplexity Sonar). (b) 2602.11962 (Wang et al., Feb 2026, ~100k election X posts): 6 LLMs
across 3 families on 5 per-category binary labels — LLM-LLM kappa EXCEEDED human-human on every
category (Conspiracy 0.75 vs 0.43; Hate Speech 0.62 vs 0.32; Sensationalism 0.60 vs 0.23;
Speculation 0.58 vs 0.21; Satire 0.53 vs 0.16). (c) 2501.02532 (Bojic et al., Jan 2025): 8 LLM
variants across 4 families treated as a rater group, Krippendorff's alpha 0.95 sentiment (humans
0.95), 0.80 political leaning (humans 0.55), 0.85 emotional intensity (humans 0.65), 0.25
sarcasm (humans 0.25). The variable that separates the 0.23 case from the 0.53-0.95 cases is the
label design — 121 fine-grained, largely interpretive, often multiclass features versus small
sets of binary or concrete labels — not the models, which overlap heavily across the three
studies. Design implication: the classifier's achievable ceiling is set when the taxonomy is
written, before any model is chosen.

- <https://arxiv.org/abs/2601.12099>
- <https://arxiv.org/abs/2602.11962>
- <https://arxiv.org/abs/2501.02532>

### F2. [HIGH] Binary presence/absence framing substantially outperforms multiclass framing: multiclass features had 90% lower odds of correct detection than binary features (OR 0.10, 95% CI 0.03-0.35, p<.001) in a mixed-effects model over 1.1M+ annotations.

*Vote: 3-0 (supporting binary-decomposition claim from 2602.11962 refuted 1-2)*

Verified verbatim in 2601.12099 results and reproduced in its appendix Table 14 (positive
stratum: OR 0.10 [0.03, 0.35]). The paper's own discussion states 'LLMs perform best when the
annotation task reduces to presence-versus-absence judgments.' Consistent with 2602.11962, whose
5 per-category BINARY labels are the design that produced the highest cross-family kappas in the
whole confirmed set (0.53-0.75). IMPORTANT LIMIT: no confirmed source directly tests decomposing
one multiclass label set into N binary probes — 2601.12099 compares features that were natively
binary against features that were natively multiclass, and the one claim that asserted a tested
binary-decomposition design (2602.11962, mean Krippendorff alpha 0.70 for optimized model
combinations) FAILED verification 1-2. So the direction is well-evidenced; the specific
decomposition tactic is an untested inference, and it multiplies API calls by the number of
labels.

- <https://arxiv.org/abs/2601.12099>
- <https://arxiv.org/abs/2602.11962>

### F3. [HIGH] Label definitions must be anchored in surface-observable criteria rather than interpretive judgment: concrete features reached F1 above 0.60 for the best models while features requiring inference fell below F1 0.30 — and LLM difficulty tracks human difficulty (r=0.61), so human inter-coder reliability is the practical ceiling.

*Vote: merged 3-0 / 3-0 (two related claims refuted 0-3)*

2601.12099, verbatim: ritual function (funerary, initiation, newborn ceremonies) and movement
(dancing, singing) 'annotated with relatively higher accuracy (F1 >> 0.60 for the best models)';
'features requiring interpretive inference, such as psychological discomfort, arousal levels,
and ritual form, proved considerably more difficult (F1 << 0.30)'; LLM performance correlated
with human IRR at r=0.61. Corroborated at the boundary by 2501.02532: sarcasm alpha 0.25 for
BOTH the 33 human annotators and the 7 LLMs, versus sentiment 0.95/0.95 — labels humans cannot
agree on, LLMs cannot either. CAUTION on strength: two other claims that would have replicated
the concrete-vs-interpretive split (from 2506.10150 empathy sub-components and 2603.29141
arithmetic-vs-conceptual grading) were REFUTED 0-3, so this rests on 2601.12099 plus the sarcasm
corroboration, not on a broad replication base. The prescriptive wording ('anchor labels in
observable criteria') is inference, not a sentence in either paper. Design implication: for each
of the ~6 coarse knowledge types, write the definition as a surface test a reader can apply
without inferring intent; if two humans would disagree on a label, expect models to disagree
too.

- <https://arxiv.org/abs/2601.12099>
- <https://arxiv.org/abs/2501.02532>

### F4. [MEDIUM] A named fallback label plus an instruction to use it under uncertainty produces surface consensus that masks minority-class collapse — four frontier models reached a 0.9612 full-agreement ratio on sarcasm 'No' while Fleiss kappa was -0.0011, and missed 79% of hateful and 75% of sarcastic instances against a human reference.

*Vote: merged 3-0 / 3-0 (causal-mechanism version refuted 0-3)*

MultiSoc-4D (Pramanik et al., 7 May 2026; 58k+ Bengali social-media comments; ChatGPT, Gemini,
Claude, Grok). Numbers exact: Table 3 full-agreement ratio 0.9612 on sarcasm 'No', Fleiss kappa
-0.0011; full agreement on sarcasm 'Yes' was 0.00 — the four models never once jointly
identified sarcasm; models found on average 13.5 sarcasm instances vs 35 by humans. The kappa
figure is a genuine within-study outlier (same pipeline gave sentiment kappa 0.56, category
0.41, hateful <0.39), so it is not a whole-pipeline artifact, and the under-detection is
established independently of kappa (which is deflated under extreme skew per the Feinstein/Byrt
prevalence paradox). The prompt explicitly contained 'Assign No for unknown cases of hatefulness
and sarcasm' plus 'Other' for unclear category and 'Neutral' for unclear sentiment — this is the
exact escape-hatch shape proposed for a 'general' bucket. WHY MEDIUM, NOT HIGH: single
unreplicated preprint, 3 months old, zero citations; Bengali social media; the 79%/75% come from
a 500-item human-annotated subset pooled across four models with no per-model breakdown and no
reported human-human IRR; and critically, the CAUSAL version of this claim ('the instruction
caused the collapse') was REFUTED 0-3 — the authors name 'instruction-induced label collapse' in
their title and blame the 'Default Assignment (Confusion Rule)', but they ran no ablation
without the fallback instruction. Design implication (strong despite the caveat): do not write
'if unsure, label general'. Measure the general-bucket rate against human labels before trusting
it.

- <https://arxiv.org/abs/2605.06940>

### F5. [HIGH] Inter-model agreement is not evidence of correctness — high LLM-LLM agreement coexists with systematic divergence from human judgment, in both the collapse case and the calibrated case.

*Vote: merged 3-0 / 3-0 / 3-0*

Two independent demonstrations. (a) 2501.02532, emotional intensity: LLM inter-model
Krippendorff alpha 0.85 vs human-human 0.65, yet humans rated intensity significantly higher —
human mean 3.44 (SD 0.34) vs LLM mean 3.19 (SD 0.17), t(49.42)=3.615, p<.001, Cohen's d=0.88
(large); ANOVA F(8,48)=2.256, p=.039; GPT-4 alone nearly matched humans at 3.43, so the
divergence is model-specific but real at group level. (b) 2605.06940: 96.1% surface agreement
with kappa -0.001 and 75% of sarcastic content missed. Design implication: a cross-model
agreement metric is a useful stability check but is NOT an acceptance test. The classifier needs
a human-labeled gold set, including deliberate oversampling of the rarest knowledge types, or
the general bucket will absorb them invisibly.

- <https://arxiv.org/abs/2501.02532>
- <https://arxiv.org/abs/2605.06940>

### F6. [MEDIUM] Prompt wording alone swings classification accuracy by 26-36 points on an interpretive 6-class task, and interpretive tasks are far more prompt-sensitive than knowledge-anchored ones ('Knowledge Anchoring Effect').

*Vote: 3-0*

Jingyuan Liu, 'What Is Actually Being Annotated?', 2 Apr 2026. 20 semantically equivalent
prompts (10 per style x 2 styles), TREC 6-class question classification, 500 test samples,
temperature 0, casing/spacing/formatting held constant. Table 2: GPT-4o mini accuracy
0.546-0.808 (mean 0.718, SD 0.068); LLaMa3.1:8b 0.392-0.756 (mean 0.578, SD 0.097) — spreads of
26.2pp and 36.4pp. Pairwise agreement rate between prompts spread over 40% with SD > 0.1 on
TREC; on knowledge-anchored Politifact scoring the range was 3% with SD 0.02. WHY MEDIUM:
single-author unreviewed preprint; only 2 models; the paper's own intro states an inconsistent
'0.61 to 0.90' range that conflicts with its Table 2; and the headline 40%-vs-3% gap compares
discrete exact-match to continuous-score PAR — the paper's own binarized Politifact check
narrows it to SD 0.051/0.063 vs >0.1, so the direction holds but the gap is roughly 2x, not 13x.
The paper also warns Politifact's stability is 'Stubborn Consistency' — stable but only ~30%
exact-match accurate, so stability must never be read as accuracy. Independent corroboration of
the general effect exists in Sclar et al. FormatSpread (ICLR 2024, up to 76-point spreads from
formatting alone), cited in verification but not itself fetched. Design implication: freeze one
prompt string as part of the classifier's versioned contract; treat any rewording as a change
requiring re-validation on the gold set.

- <https://arxiv.org/abs/2604.16413>

### F7. [HIGH] Presenting a fixed label set as a lettered option list inherits selection bias, and most of the effect comes from the option-ID tokens rather than raw position — so emit label names, not A/B/C/D, and do not expect shuffling to fix it.

*Vote: 3-0 (competing 2308.11483 claim refuted 0-3)*

Zheng et al., 'LLMs Are Not Robust Multiple Choice Selectors' (2309.03882, v2 Feb 2024; 20 LLMs
x MMLU/ARC/CSQA). Answer-moving attack, Table 1 (0-shot MMLU): gpt-3.5-turbo 67.2 -> 60.9 (-6.3)
when all gold answers move to D; llama-30B 53.1 -> 68.2 (+15.2) at position A; every model
swings both ways (vicuna-v1.3-13B 50.2 -> 64.4 at B / 38.8 at D). The construction is an apt
analogy for a fixed label list, where a given true label always occupies the same slot. CRITICAL
REFINEMENT from the same paper's Table 2 ablation: removing A/B/C/D IDs cuts recall-std from 5.5
to 1.0 on MMLU and 2.3 to 0.6 on ARC — 'option numbering is one primary cause of selection
bias'; residual pure-ordering effect is 'quite irregular'. Also: shuffling options does NOT
reduce bias (5.9 vs 5.5 baseline; ARC 4.2 vs 2.3, i.e. worse), a debiasing instruction barely
helps (6.1 vs 5.5), and ID format matters ((A)(B)(C)(D) = 8.1 worse; 1/2/3/4 = 3.8 better).
Mechanism confirmed current: 2605.06672 (Apr 2026) finds 12 of 13 reasoning configurations show
positive partial correlation between reasoning-trajectory length and position-bias score after
controlling for accuracy (r 0.11-0.41, all p<0.05), with a causal truncation probe (16% -> 32%
shift for R1-Qwen-7B) — i.e. more chain-of-thought produced MORE position bias. 2607.20864 (Jul
2026, 24,000 temperature-0 calls across gpt-4o-mini, claude-haiku-4-5, gemini-2.5-flash, grok-3)
finds position bias detectable in a roughly 60-95% base-accuracy band — which is exactly where a
fine-grained 6-type-plus-general classifier will sit. A competing claim of 13-75% reordering
gaps (2308.11483) was REFUTED 0-3; the magnitudes above are 2023-era models and should not be
quoted as current expected sizes.

- <https://arxiv.org/abs/2309.03882>
- <https://arxiv.org/abs/2605.06672>
- <https://arxiv.org/abs/2607.20864>

### F8. [MEDIUM] Majority voting over three models drawn from different families improves agreement with human consensus, but expanding to five slightly reduces it — ensemble gains saturate and can reverse.

*Vote: 3-0 (prompt-variant voting claim refuted 1-2)*

2602.11962, Table 4: 3-LLM majority vote on Conspiracy reached kappa 0.62 +/- 0.01 (range
0.60-0.65) against human consensus vs 0.56-0.62 for individual models, with the best 3-model set
spanning Llama+GPT+Gemini in 4 of 5 categories; paper states 'LLM majority voting generally
improves agreement, particularly when combining models from different LLM families' and that
five-model voting 'did not improve IRR and, in fact, led to slightly lower agreement.' WHY
MEDIUM: one study, one domain (election social-media posts); the five-model result is stated in
prose with no per-category kappas; on Conspiracy the majority vote only MATCHED the best single
model; the Satire best set used two Llama models (same family). A separate and more directly
useful idea — majority voting over k semantically equivalent PROMPT variants (claimed 90% SD
reduction, ~9% accuracy gain, most of it by k=3) — was REFUTED 1-2 and should not be relied on.

- <https://arxiv.org/abs/2602.11962>

### F9. [MEDIUM] Direct evidence on conversational statement classification exists but is thin, measures only LLM-vs-human agreement (never cross-model agreement), and lands in a wide band: weighted kappa median 0.60 on support conversations (matching expert-expert 0.58) versus Cohen's kappa 0.38-0.58 on classroom utterances against a human ceiling above 0.90.

*Vote: merged 3-0 / 3-0 (two related claims from 2506.10150 refuted 0-3 and 1-2; source attribution corrected during verification)*

(a) Kumar et al. 2506.10150 (Stanford/Northwestern, v2 Oct 2025): 200 real-world support
conversations, 21 empathy sub-components across 4 frameworks, Gemini 2.5 Pro / GPT-4o / Claude
3.7 Sonnet. Expert-LLM weighted kappa 0.17-0.86 (median 0.60, IQR 0.49-0.70) vs expert-expert
0.11-0.84 (median 0.58); expert-LLM pairs cleared the study-internal high-agreement threshold in
15 of 21 sub-components (70%); crowdworker-expert median only 0.33. Caveat: ordinal empathy
RATINGS scored with weighted kappa, not nominal single-label classification, and the 'threshold'
is the study's own 0.58 expert median, not an external standard. (b) True primary for the Talk
Moves result is Vanacore & Kizilcec 2512.19903 (Cornell, 22 Dec 2025) — NOT 2603.29141, which
merely cites it in a table and introduced two errors the original claim inherited. TalkMoves
dataset: 63 K-12 MATHEMATICS CLASSROOM transcripts (whole-class, small-group, online), 800
stratified target utterances, 7-way label set = six Accountable Talk moves + 'None'. Cohen's
kappa 0.38-0.58 across all model-prompt combinations; per-model, zero-shot: Gemini 3 Pro .48,
Claude 4.5 Opus .48, Claude 4.5 Sonnet .40, Gemini 2.5 .38, GPT-5 .47, o3 .46; few-shot-all:
.54/.58/.52/.57/.49/.45. Neither endpoint belongs to the models the secondary source named.
Human expert annotators on the SAME data reached kappa > 0.90, so 0.38-0.58 sits far below the
human ceiling. TWO POINTS DIRECTLY ON THE PROPOSED DESIGN: the Talk Moves label set is
structurally identical to the plan here (roughly 6 fine types plus an explicit 'None' escape
hatch) and it produced only moderate agreement; and utterances were submitted in chunks of 20-30
surrounding discourse lines 'to provide sufficient — but not overwhelming — context', the only
concrete context-window datapoint found. CRITICAL GAP: the claim that 2506.10150 showed cross-
family model-model agreement of alpha 0.51-0.75 was REFUTED 0-3, so NO confirmed source reports
LLM-LLM agreement on conversational text at all.

- <https://arxiv.org/abs/2506.10150>
- <https://arxiv.org/abs/2512.19903>
- <https://arxiv.org/abs/2603.29141>

### F10. [MEDIUM] Few-shot exemplars materially improve fine-grained conversational utterance typing for most models but not uniformly — and for two frontier models they helped negligibly or hurt.

*Vote: 3-0 (extracted during verification of the Talk Moves claim)*

Vanacore & Kizilcec Table 2, Cohen's kappa by prompt regime (zero-shot / one-shot / few-shot
3-example / few-shot all-examples): Gemini 3 Pro .48/.48/.53/.54; Claude 4.5 Opus
.48/.49/.54/.58; Claude 4.5 Sonnet .40/.44/.49/.52; Gemini 2.5 .38/.45/.50/.57; GPT-5
.47/.48/.51/.49 (peaks at 3 examples, then DIPS with all examples); o3 .46/.47/.48/.45 (ends
BELOW zero-shot). So the gain is real (up to +19 kappa points for Gemini 2.5) but model-
dependent in both size and sign, and more exemplars is not monotonically better. The paper also
reports higher recall bought at the cost of increased false positives, with performance varying
considerably by individual label. Single study; bootstrap CIs and significance tests vs zero-
shot baseline were run; code released. Design implication: exemplar count is a per-model tuning
parameter, not a fixed prompt constant — which conflicts directly with the goal of one prompt
working identically across families.

- <https://arxiv.org/abs/2512.19903>

### F11. [MEDIUM] Verbalized confidence scores can be well calibrated but their reliability depends strongly on how the model is asked, with no universal best prompt method — and all of this was measured on closed-book QA, never on classification or conversational text.

*Vote: merged 3-0 / 2-1*

Yang, Tsai & Yamada, 'On Verbalized Confidence Scores for LLMs' (v1 Dec 2024, v2 5 May 2026;
code at github.com/danielyxyang/llm-verbalized-uq). Scope confirmed exactly as previously
asserted: 17 prompt methods (10 custom + 7 from Tian 2023 and Xiong 2023), 10 QA datasets
(arc-c, arc-e, commonsense_qa, logi_qa, mmlu, sciq, social_i_qa, trivia_qa, truthful_qa-
mc1/mc2), 11 models (Gemma 1.1 2B/7B, Llama 3 8B/70B, Qwen 1.5 7B/32B/72B/110B, GPT-3.5-turbo,
GPT-4o-mini, GPT-4o). Metrics ECE/smECE. Best 'combo' method: average deviation of 7% from
empirical accuracy on the large LLMs; worst configurations exceed 0.3 calibration error; Gemma
2B's confidence is 'almost independent from its accuracy'. 'Tiny LLMs favor simple prompt
formulations, while large LLMs benefit from more complex prompt methods' — the best method is
model-dependent. WORDING FIX carried from verification: the source says 'strongly
depends'/'greatly influenced', NOT 'depends primarily' — model capacity is a hard co-determinant
and overconfidence persists at every size, improving mainly through accuracy gains rather than
reduced overconfidence. THREE LIMITS: unrefereed preprint with no confirmed venue; the authors
explicitly disclaim generalization ('It is also unknown to us how our results carry over to
other LLM families'); and all 10 datasets are multiple-choice/short-answer QA with no
conversational or dialogue data, so this supports nothing about confidence calibration on chat
statements. Two of the 11 'parameter-range' models (GPT family) have undisclosed sizes, so
'2B-110B' strictly describes the 8 open-weight models.

- <https://arxiv.org/abs/2412.14737>

### F12. [HIGH] Four of the five research angles have material evidence gaps, and one — structured-output reliability across model families — produced ZERO confirmed claims despite being explicitly targeted.

*Vote: n/a — negative finding compiled across all five angles*

Explicit absence-of-evidence report, since the brief asked for it. (1) STRUCTURED OUTPUT (angle
3): none of the 17 surviving claims touches JSON-schema vs forced-tool-call reliability,
constrained-decoding quality cost, or per-model prompt optimization. The targeted source
2605.02363 (asserted: 7-9B models at 85% task accuracy with 0% valid-JSON joint accuracy;
constrained decoding 3.6-8.2x latency; Gemma 2-9B 52.4% duplicate outputs) yielded nothing
verified — treat every one of those numbers as unconfirmed. This is the single largest hole for
a classifier that must return machine-parseable labels across four vendor APIs. (2) BATCH
CLASSIFICATION (angle 5): 2604.03684 (asserted: 6 of 8 models within 2pp of single-item baseline
through batch size 100, collapse beyond) also produced no confirmed claim — do not assume
batching is free. (3) DECONTEXTUALIZATION AND SEGMENTATION (angle 4): nothing confirmed on
resolving pronouns/ellipsis before classification (Choi et al. and follow-ups produced no
surviving claim), nothing on splitting one chat message into multiple statements, nothing on
claim-detection/check-worthiness accuracy comparing conversational to formal text (ClaimBuster,
CheckThat!). The only context-window datapoint anywhere in the confirmed set is the 20-30
discourse lines used in 2512.19903, which was a design choice, never ablated. (4) PROMPT DESIGN
(angle 5): nothing confirmed on definitions-in-prompt vs bare labels, on positive-plus-negative
exemplars, or on abstain-vs-other escape-hatch designs. Chain-of-thought for classification has
only indirect evidence, and it is negative: 2605.06672 found longer reasoning traces correlate
with MORE position bias (r 0.11-0.41 across 12 of 13 configurations) with causal support from a
truncation probe.

- <https://arxiv.org/abs/2605.02363>
- <https://arxiv.org/abs/2604.03684>

## Caveats

SOURCE QUALITY. Almost the entire evidence base is arXiv preprints, several of them under six
months old with zero citations and no replication: 2601.12099 (Jan 2026), 2602.11962 (Feb 2026),
2604.16413 (Apr 2026, single author, and internally inconsistent — its intro reports an accuracy
range that contradicts its own Table 2), 2605.06940 (May 2026, three months old, unreplicated),
2512.19903 (Dec 2025), 2506.10150 (peer-review status unconfirmed). Only 2309.03882 is a
heavily-cited, mature paper. Confidence labels above are calibrated to this, but the whole
synthesis should be read as "best current preprint evidence," not settled science.  DIRECTIONAL
CONFLICT, UNRESOLVED. 2601.12099 (LLM-LLM kappa 0.23 vs human 0.57) and 2602.11962 (LLM-LLM
0.53-0.75, exceeding human on every category) reach opposite conclusions about whether models
agree with each other better than humans do. The reconciliation offered here — that
binary/concrete label sets explain the gap — is an inference from the two studies' designs, not
a result either paper tested. An alternative explanation is baseline quality: 2602.11962's human
baseline came from 34 minimally-trained crowdworkers with large SDs (±0.14-0.18), which may
depress the human side, while 2601.12099 used trained coders. Do not treat the reconciliation as
proven.  DOMAIN TRANSFER IS THE WEAKEST LINK THROUGHOUT. Not one confirmed source studied
knowledge-type classification of statements. The evidence comes from ethnographic ritual coding,
Bengali social-media moderation, US election tweets, empathy in support conversations, K-12 math
classroom talk, and multiple-choice QA. Every design implication drawn here is a transfer, and
the escape-hatch finding in particular (Bengali, sarcasm/hate binary dimensions, n=500 gold
subset pooled over four models) is the furthest stretch relative to how load-bearing it is.
EIGHT CLAIMS WERE REFUTED, AND THREE OF THEM MATTER TO DECISIONS. (a) The only claim asserting
cross-family agreement numbers on conversational text (2506.10150, alpha 0.51-0.75) failed 0-3 —
so there is no confirmed measurement of model-model agreement on chat. (b) The only claim
asserting a TESTED binary-decomposition design (2602.11962, alpha 0.70) failed 1-2 — the binary-
over-multiclass recommendation rests on an odds ratio between natively-binary and natively-
multiclass features, not on a decomposition experiment. (c) The claim that prompt-variant
majority voting stabilizes labels (90% SD reduction, most gains by k=3) failed 1-2 — an
attractive mitigation for prompt sensitivity that cannot currently be relied on. Also refuted:
two replications of the concrete-vs-interpretive split, the causal version of instruction-
induced label collapse, and the 13-75% option-reordering figure.  TWO ATTRIBUTION ERRORS WERE
CAUGHT AND CORRECTED IN VERIFICATION, which suggests others may remain in the upstream claim
set. The Talk Moves kappa range of 0.38-0.58 was credited to 2603.29141 (a position paper that
only cites it in a table) instead of the true primary 2512.19903; the endpoints were attributed
to Gemini 3 Pro and GPT-5 when they actually belong to Gemini 2.5 zero-shot and Claude 4.5 Opus
few-shot; and the data genre was described as "tutoring dialogues" when it is K-12 classroom
transcripts.  TIME SENSITIVITY. The position-bias magnitudes (6.3 / 15.2 points) come from
2023-era models (llama, vicuna, gpt-3.5-turbo); the mechanism is confirmed to persist in 2026
frontier models but the sizes are not current. The verbalized-confidence benchmark spans Gemma
1.1 through GPT-4o — no Claude model was tested at all, which matters given the cross-family
requirement.  VERIFICATION COVERAGE LIMIT. Several verifiers reported exhausting the session's
WebSearch budget (200/200) before running independent contradiction searches, so most claims
were confirmed by direct primary-source fetch rather than by surveying rival findings.
Confirmation that a paper says X is strong; confirmation that no one disputes X is weak or
absent for most items here.

## Open questions

- Does decomposing this taxonomy into per-label binary probes actually beat one multiclass call,
and at what cost? The OR 0.10 finding compares features that were natively binary against
features that were natively multiclass — no confirmed source tested the decomposition itself.
Needs a direct A/B on the real label set, measuring both agreement gain and the N-fold increase
in calls, latency, and spend.
- What should replace 'general', given that a named fallback plus an 'if unsure use it'
instruction is the one design known to collapse minority classes while inflating surface
agreement? Untested alternatives worth a bakeoff: no fallback at all with a confidence threshold
applied post-hoc; abstain-with-reason; or forcing a positive label and routing low-confidence
outputs to review. No confirmed evidence compares abstain-style and other-style designs.
- How much surrounding chat context is needed, and does decontextualizing a statement (resolving
pronouns and ellipsis) before classification change agreement? The only datapoint anywhere is
the 20-30 discourse lines used in the Talk Moves study, which was a design choice and never
ablated. This is the single biggest unknown for the chat half of the classifier and the
literature appears genuinely thin, not merely unsearched.
- Does structured output degrade label quality, and does it degrade it differently across
OpenAI, Anthropic, Google, and open-weight models? Zero confirmed evidence — the targeted source
produced nothing verified. Since the classifier must return parseable labels from four vendor
APIs, this needs measuring in-house: JSON schema vs forced tool call vs plain text-then-parse,
scored on both parse success and label agreement.
- What is the human-human ceiling on this specific taxonomy? Every study where LLMs looked
adequate compared them against a measured human baseline, and the r=0.61 tracking result says
labels humans cannot agree on are labels models cannot agree on either. Without a double-coded
gold set, there is no way to tell a bad classifier from a bad label definition.

## Refuted — never cite as support

- *(vote 1-2)* Majority voting across k semantically equivalent prompt variants substantially stabilizes labels: aggregating 10 prompts reduced the standard deviation of inter-prompt reliability by 90% and raised mean accuracy ~9% vs single-prompt; for GPT-4o mini mean PAR rose from 0.71 (k=1) to ~0.95 (k=10), with most variance reduction already achieved by k=3.
- *(vote 1-2)* The multi-label task was decomposed into independent binary True/False probes per category, each with a detailed in-prompt definition and temperature 0, and this design produced usable cross-family agreement (mean Krippendorff's alpha 0.70 for optimized model combinations vs 0.62 for the best human sets) — consistent with the 2601.12099 finding that binary framing outperforms multiclass.
- *(vote 0-3)* Three frontier model families (Gemini 2.5 Pro, GPT-4o, Claude 3.7 Sonnet) agreed with each other at Krippendorff's alpha 0.51-0.75 (median 0.60) on the same fixed label sets — a much higher cross-model consistency than the mean LLM-LLM Cohen's κ=0.23 reported in arXiv 2601.12099, suggesting cross-family agreement depends heavily on task/label design.
- *(vote 1-2)* LLM reliability tracked human expert inter-rater reliability across sub-components at Pearson r=0.67 (vs r=0.17 for crowdworkers) — corroborating the r=0.61 'LLM performance tracks human IRR' finding in arXiv 2601.12099: labels humans can't agree on, LLMs can't either, so expert IRR is the right ceiling/benchmark for a classifier's label set.
- *(vote 0-3)* Sub-components with clear linguistic/behavioral markers were reliably annotated (e.g., 'Explorations' median κw=0.76, 'Practical Advice' κw=0.77) while interpretive/subjective ones were not ('Interpretations' κw=0.29) — replicating the concrete-vs-interpretive split (F1>0.60 vs F1<0.30) claimed in arXiv 2601.12099 and implying knowledge-type labels should be defined by observable surface markers.
- *(vote 0-3)* LLM annotation reliability splits sharply by construct concreteness: multimodal LLMs matched expert educators on rote arithmetic grading (κ=0.90) but failed on interpretive conceptual illustrations (κ≈0.47) — corroborating the concrete-vs-interpretive gap reported in arXiv 2601.12099.
- *(vote 0-3)* Including default 'when uncertain' rules in the annotation prompt (assign Other / Neutral / No for unclear cases) systematically biased all models toward those fallback escape-hatch labels, producing what the authors call instruction-induced label collapse.
- *(vote 0-3)* Reordering answer options in multiple-choice questions causes LLM performance gaps of approximately 13% to 75% across benchmarks, demonstrating strong positional/order bias relevant to how a fixed label list is presented to a classifier.

