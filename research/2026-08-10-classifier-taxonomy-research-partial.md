---
title: Classifier-taxonomy deep research — PARTIAL (interrupted by spend limit)
date: 2026-08-10
status: three parallel runs; searches + extraction complete, verification interrupted
resume: run IDs inside — completed agents replay from cache, only failed verifiers re-run
---

# Classifier-Taxonomy Research — Partial Results

Three deep-research runs (one per angle group, separate verification budgets —
the fix for the Aug-8 starvation). All three hit the monthly spend limit mid-
verification. Confirmed claims below survived 3-vote adversarial verification
BEFORE the interruption; 'extracted, unverified' claims had verifiers die on
the limit and are recoverable by resuming.

## Run A-annotation-taxonomies  (workflow wf_b804d853-417, task wxdboe2w6)

**5 confirmed / 20 extracted-but-unverified / 0 refuted**

### CONFIRMED (3-0): Expanding Argumentative Zoning from 7 to 15 categories produced three-annotator Fleiss kappa of 0.71 in chemistry (N=3745 sentences) and 0.65 in computational linguistics (N=1629), versus kappa 0.71 for the original 7-category AZ on CL — i.e., roughly doubling the label count cost only about 0.06 kappa within the same discipline and nothing in chemistry.

> The inter-annotator agreement for chemistry was κ = 0.71 (N=3745, n=15, k=3). For CL, the inter-annotator agreement was κ = 0.65 (N=1629, n=15, k=3). For comparison, the inter-annotator agreement for the original, CL-specific AZ with 7 categories was κ = 0.71 (N=3420, n=7, k=3).

Source: <https://aclanthology.org/D09-1155/>

### CONFIRMED (2-1): AZ-II's fine labels were created strictly by splitting the original coarse categories so the coarse labels are deterministically recoverable, and collapsing the 15 fine labels to 6 coarse categories RAISED agreement from 0.71 to kappa 0.75 (chemistry) — directly validating the fine-labels-roll-up-to-~6-coarse-types design, with the caveat that the 0.75 vs 0.71 comparison crosses disciplines.

> The finer grain in AZ-II has been accomplished purely by splitting existing AZ categories; hence, the coarser AZ categories are recoverable (with the exception of the TEXTUAL category). [...] Inter-annotator agreement for the collapsed AZ-II showed κ = 0.75 (N=3745, n=6, k=3). This compares favourably to the collapsed AZ's agreement of κ = 0.71 (N=3420, n=6, k=3); but when comparing the raw numerical results one should consider that different data from different disciplines is used (chemistry in AZ-II, CL in AZ).

Source: <https://aclanthology.org/D09-1155/>

### CONFIRMED (3-0): The agreement was achieved with an extremely heavy codebook: 111 A4 pages of guidelines containing a decision tree, 75 explicit pairwise category-distinction rules, examples from both domains, plus a 10-page domain primer — and this apparatus let expert-trained NON-expert annotators reliably annotate the 15-category scheme, with annotators required to justify every decision from text-based evidence.

> Our annotation guidelines are 111 sides of A4 and contain a decision tree, detailed description of the semantics of the 15 categories, 75 rules for pairwise distinction of the categories and copious examples from both chemistry and computational linguistics.

Source: <https://aclanthology.org/D09-1155/>

### CONFIRMED (3-0): The full Argumentative Zoning scheme has 7 categories (BACKGROUND, OTHER, OWN, AIM, TEXTUAL, CONTRAST, BASIS) and achieved reproducibility K=.71 across 3 trained annotators on 4261 sentences, with per-annotator stability of K=.82, .81, and .76 — confirming the ~0.71 figure the research question asked to verify for the full scheme.

> The full annotation scheme is stable (K=.82, .81, .76; N=1220; k=2 for all three annotators) and reproducible (K=.71, N=4261, k=3).

Source: <https://aclanthology.org/E99-1015/>

### CONFIRMED (3-0): The coarser 3-category 'basic' version of the same scheme (BACKGROUND / OTHER / OWN) achieved measurably higher agreement than the 7-category full scheme: reproducibility K=.78 (N=4031, k=3) vs K=.71, and stability K=.83, .79, .81 — direct evidence that fewer, coarser labels raise inter-annotator agreement on statement-role classification.

> The results show that the basic annotation scheme is stable (K=.83, .79, .81; N=1248; k=2 for all three annotators) and reproducible (K=.78, N=4031, k=3).

Source: <https://aclanthology.org/E99-1015/>

### Extracted but NOT verified (verification died on spend limit — treat as leads)

- Deterministically collapsing hard-to-distinguish fine categories into a coarser grouping raised measured agreement: merging the CONTRAST/OTHER/BACKGROUND distinctions increased reproducibility from K=.71 to K=.75 while preserving the distinctions the authors' application actually needed — an empirical precedent for a two-tier design where fine labels roll up to coarse types. — <https://aclanthology.org/E99-1015/>
- Codebook depth and training had a large measured effect: trained annotators (17-page guidelines for the full scheme, a decision tree, 4 training papers, weekly discussions) reached K=.71, while 18 untrained subjects given only 1 page of instructions plus the decision tree reached only K=.35, .49, and .72 in their three groups on the full scheme. — <https://aclanthology.org/E99-1015/>
- CoreSC is itself a two-tier (layered) label design: 11 first-layer coarse categories (Hypothesis, Motivation, Background, Goal, Object, Method, Experiment, Model, Observation, Result, Conclusion), with a second property layer (New/Old, Advantage/Disadvantage) that expands deterministically into 18 flat fine labels (Table 1) — a working precedent for fine labels that collapse mechanically to coarse types. — <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>
- Measured inter-annotator agreement for CoreSC at the 11-category level, with 16 domain experts over 41 multiply-annotated papers (phase I), was Cohen's kappa = 0.57 for the 9 best annotators on the one paper common to all, and kappa = 0.50 across the remaining papers — i.e., an 11-way knowledge-role scheme annotated by experts landed at only moderate agreement. — <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>
- AZ-II, a 15-category rhetorical scheme annotated by 3 expert-trained non-experts on 30 chemistry papers, reached Fleiss kappa = 0.71 — higher than CoreSC's 0.50-0.57 despite having MORE categories — showing tagset size alone does not determine agreement; but its rare categories were far less reliable (CoDi κ=0.35±0.19, AntiSupp κ=0.36±0.26), and its 7 rarest categories together cover only 6.7% of the corpus. — <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>
- Per-category reliability within CoreSC spans a huge range — Krippendorff-diagnostic Cohen's kappa from 0.89 (Conclusion) and 0.87 (Background) down to 0.46 (Hypothesis, Motivation) and 0.43 (Model), against a category average of 0.55 — meaning abstract/intentional statement types (hypothesis, motivation, model) are systematically the hardest for human annotators, directly relevant since 'model' and claim-like types are among the planned 6 coarse types. — <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>
- The 7-category rhetorical annotation scheme (AIM, TEXTUAL, OWN, BACKGROUND, CONTRAST, BASIS, OTHER) achieved reproducibility of kappa=.71 across 3 trained annotators on 4,261 sentences, and intra-annotator stability of K=.82/.81/.76 — i.e., 'marginally reliable' on Krippendorff's scale for the cross-annotator figure, establishing a concrete agreement ceiling for a ~7-label knowledge-role scheme on statements. — <https://aclanthology.org/J02-4002/>
- Collapsing to a coarser 3-category scheme (OWN/OTHER/BACKGROUND 'intellectual attribution') measurably improved agreement over the full 7-category scheme: reproducibility rose from K=.71 to K=.78 and stability from .82/.81/.76 to .83/.79/.81 — direct empirical evidence that fewer, coarser labels yield higher human agreement, supporting a design where fine labels roll up to a small coarse set. — <https://aclanthology.org/J02-4002/>
- Per-category agreement within one scheme is highly heterogeneous: by Krippendorff's category diagnostics, annotators distinguished AIM (K=.79) and TEXTUAL (K=.79) well but BASIS (K=.49) and CONTRAST (K=.59) poorly — the authors attribute this to explicit metadiscourse cues and fixed location for the reliable categories versus dispersal inside long OWN zones for the unreliable ones. Implication for label-set design: reliability must be checked per label, not just scheme-wide. — <https://aclanthology.org/J02-4002/>
- The CoreSC scheme classifies scientific-article sentences into exactly 11 fine-grained categories: Background, Hypothesis, Motivation, Goal, Object, Method, Model, Experiment, Observation, Result, and Conclusion. — <https://doi.org/10.1093/bioinformatics/bts071>
- Human inter-annotator agreement on the 11-category CoreSC scheme was Cohen's kappa = 0.55 overall (median of the 9 best annotators, 41 papers, annotators working in groups of 3), with per-category kappas in Table 1 ranging from roughly 0.43 (Model) and 0.46 (Motivation) up to 0.87 (Background) and 0.89 (Conclusion) — i.e., moderate overall agreement with large per-label spread at 11-way granularity. — <https://doi.org/10.1093/bioinformatics/bts071>
- Collapsing the 11 fine CoreSC labels deterministically into 4 coarse groups substantially raised automatic F-scores for the merged Approach (72%) and Outcome (81%) groups versus their best fine-label constituents, but the Objective group (merging the four rarest labels) reached only 38% — direct evidence that fine-to-coarse rollup helps unevenly and cannot rescue a coarse group built from rare, confusable fine labels. — <https://doi.org/10.1093/bioinformatics/bts071>
- Teufel, Carletta & Moens (1999) argumentative zoning reached K=0.71 on the full scheme but K=0.81 when collapsed to the three main zones (own, other, background) — direct evidence that a coarse roll-up of a fine rhetorical-role scheme yields measurably higher agreement, and it pins the exact AZ numbers the research question asked to verify (0.71 full, 0.81 coarse, not 0.78). — <https://aclanthology.org/J08-2004/>
- Tagset size alone does not determine achievable agreement: dialogue-act schemes reached K over 0.8 at 13 tags (MapTask, K=0.83), 42 tags (Switchboard-DAMSL, K=0.80), and 20 tags (CSTAR subset, K=0.90) — so a curated 15-20-label fine tier is not inherently below the reliability threshold, but a larger tagset buys no agreement advantage either. — <https://aclanthology.org/J08-2004/>
- Collapsing fine labels into coarse groups measurably raises agreement in word-sense annotation — Palmer, Dang & Fellbaum got 82% agreement with grouped senses vs 71% with fine WordNet senses; Véronis saw noun-sense K rise from ~0.45 to 0.86 after collapsing — but the survey explicitly warns that post-hoc merging is not equivalent to annotating with the coarse set from the start, a caveat for validating a two-tier scheme only at the collapsed level. — <https://aclanthology.org/J08-2004/>
- The prevalence problem: when one category absorbs most of the mass (the risk for a 'general' residual bucket), raw agreement and even accuracy stay high while chance-corrected reliability collapses, and the survey holds that reliability must then be demonstrated on the rare categories — implying a residual-heavy classifier cannot be validated on overall agreement alone. — <https://aclanthology.org/J08-2004/>
- Hierarchical/multi-dimensional dialogue-act schemes with many fine labels only recovered flat-scheme reliability after reduction to roughly a handful of coarse superclasses — ICSI-MRDA matched Switchboard-DAMSL's reliability only when reduced to five 'class-maps' — and hierarchies were explicitly used to let coders back off to a superclass when unsure of the fine label, supporting a design of ~6 coarse types with fine labels beneath them. — <https://aclanthology.org/J08-2004/>
- The Switchboard SWBD-DAMSL project used a fine tag space of 220 distinct dialogue-act tags, of which 130 (59%) occurred fewer than 10 times each in a 205,000-utterance corpus — direct evidence that large fine-grained label sets produce a severe long-tail sparsity problem in practice. — <https://web.stanford.edu/~jurafsky/ws97/manual.august1.html>
- The 220 fine tags were collapsed deterministically into 42 coarse classes by a mechanical rule (dropping the secondary annotation dimensions, with a small number of listed exceptions, plus folding rare variants) — a working precedent for fine labels that roll up deterministically to a coarse tier. — <https://web.stanford.edu/~jurafsky/ws97/manual.august1.html>
- Inter-annotator agreement for the SWBD-DAMSL annotation, measured with Carletta's kappa across the project's human labelers, averaged kappa = 0.80 pairwise — a concrete agreement figure for a clustered ~42-class dialogue-act scheme applied at scale. — <https://web.stanford.edu/~jurafsky/ws97/manual.august1.html>

## Run B-typing-payoff  (workflow wf_376a9a4b-46b, task w5wdw4fkp)

**5 confirmed / 20 extracted-but-unverified / 0 refuted**

### CONFIRMED (3-0): Study 1 (65 operators at the DSM chemical plant in the Netherlands) found no statistically significant difference in task performance — neither correctness nor speed — between the Information Mapping version, the original in-use text, and a rewrite by an experienced non-IMAP writer; mean 78% correct, ~3 minutes for six multiple-choice lookup questions across all conditions.

> The first study showed no effects at all of text format on reader performance (correctness nor speed). ... there were no statistically significant differences between the three text variants, neither concerning the number of correct answers found, nor concerning the time needed to find these answers.

Source: <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>

### CONFIRMED (3-0): The only significant effect of format in Study 1 was subjective preference: the IMAP text scored 7.71 on a ten-point scale versus 6.72 for the expert non-IMAP rewrite, while the original text (7.38) did not differ significantly from either — i.e., readers may merely think an IMAP text is superior.

> The IMAP text (average score 7.71 on a ten-point scale) was assessed as significantly more positive than was the text revised by the lecturer (6.72). The original DSM-text (7.38) was not assessed as significantly more positive or negative than the other texts. ... The outcomes suggest that at best, readers may think that an IMAP text is superior.

Source: <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>

### CONFIRMED (3-0): Study 2 (76 Sony Music employees: 44 of Dutch descent, 32 immigrants, machine-operation instructions with a physical scale model) found no significant effect of text format (IMAP vs traditional) on accuracy, speed, or even subjective judgment, and no interaction with reader origin or education; only subjects' origin and years of education affected performance.

> Regarding the format chosen for the organization and presentation of the text (IMAP or traditional), there were no significant effects on accuracy, speed or evaluation scores at all, neither apart from nor in interaction with the subject variables measured.

Source: <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>

### CONFIRMED (3-0): The journal's Editors' Comments on the article state that the Information Mapping-designed document was compared against a traditionally written version and did NOT prove more effective — directly supporting the 'no task-performance benefit from typed restructuring' claim under verification.

> They compare the efficiency of a document designed using these procedures to that of documents written in a more traditional style. At least for this audience and this goal, employing the design procedure did not yield a more effective document.

Source: <https://www.jbe-platform.com/content/journals/10.1075/dd.4.1.05jan>

### CONFIRMED (2-1): The full text is paywalled with only a one-page preview (the Editors' Comments page), so the specific numbers cited in the design document — n=65 plant operators, n=76 second experiment, and the 'subjective preference only' finding — CANNOT be verified or refuted from this source page; they require the full text or the companion IEEE IPCC 2002 paper.

> Preview this article: Testing an Information Mapping® text: Does the method live up to the expectations?, Page 1 of 1

Source: <https://www.jbe-platform.com/content/journals/10.1075/dd.4.1.05jan>

### Extracted but NOT verified (verification died on spend limit — treat as leads)

- The earlier Jansen et al. (2002/2003, Document Design 4(1)) study — the one the design doc cites as showing no benefit — used only about twenty respondents per text version on a short (three A4 pages) text, and found no significant effectiveness or efficiency differences between the IMAP, conventional, and expert-rewritten versions; the only significant result was a preference rating of IMAP over the expert rewrite (not over the original). The design doc's attribution of 'n=65 plant operators, n=76' to that 2002 study is therefore misattributed — those samples belong to the experiments in this 2007 paper. — <https://www.jbe-platform.com/content/journals/10.1075/idj.15.1.10pai>
- The blanket claim 'typed restructuring produced no task-performance benefit, only subjective preference' is REFUTED for longer texts: in Experiment 1 (n=53 pre-university students, six A4-page brochure), the IMAP version produced significantly higher effectiveness (6.4 vs 5.8 correct answers, p<.05, effect size .09) and much higher efficiency (14.0 vs 20.2 minutes, p<.001, effect size .39) than the conventional version, plus higher appreciation (7.9 vs 6.8, p<.001). — <https://www.jbe-platform.com/content/journals/10.1075/idj.15.1.10pai>
- In Experiment 2a (n=67 staff of a concrete/hydraulic engineering firm and a district water board — almost certainly the 'n=65 plant operators' in the design doc), neither the full IMAP version nor a format-stripped IMAP version improved answer accuracy (78% vs 86% vs 88% correct, F(2,64)=2.45 ns), but BOTH IMAP versions produced significantly faster retrieval than the conventional text (30.4s and 30.9s vs 46.7s, F(2,64)=7.20, p<.01) — so 'no benefit, only preference' is wrong for this experiment: accuracy was flat but time-on-task, a performance measure, improved significantly. — <https://www.jbe-platform.com/content/journals/10.1075/idj.15.1.10pai>
- Experiment 3 (n=76 Sony Music production employees, 44 native / 32 non-native Dutch speakers, one A4-page instructive texts) found NO main effect of text version (IMAP vs conventional) on effectiveness, efficiency, or evaluation, and no interaction with the readers' linguistic origin — this is the true n=76 null result, and it applies to very short texts only. — <https://www.jbe-platform.com/content/journals/10.1075/idj.15.1.10pai>
- Ablating both the link-generation (LG) and memory-evolution (ME) modules drops A-MEM's LoCoMo Multi-Hop F1 from 27.02 to 9.65 (GPT-4o-mini backbone, Table 3) — CONFIRMING the previously collected number, but the ablated components are linking/evolution, not the typed attributes (keywords/tags), so this number does not measure the benefit of typing per se. — <https://arxiv.org/abs/2502.12110>
- The flat LoCoMo baseline clearly beats A-MEM on the Adversarial category (69.23 vs 50.03 F1 with GPT-4o-mini; 52.61 vs 36.35 with GPT-4o), but on Open Domain A-MEM is marginally AHEAD of the LoCoMo baseline (12.14 vs 12.04; 17.10 vs 16.47) — so the previously collected claim 'flat baselines beat A-MEM on Open Domain and Adversarial' is confirmed for Adversarial and only weakly/partially supported for Open Domain (the paper credits LoCoMo and MemGPT as strong there, but A-MEM is not strictly beaten by LoCoMo in these table rows). — <https://arxiv.org/abs/2502.12110>
- Each A-MEM memory note is a typed/structured unit containing LLM-generated keywords, tags, and a contextual description alongside content, timestamp, embedding, and links — i.e., the system does use structured attribute tagging, but the paper's ablation never isolates these attributes' contribution separately from linking and evolution. — <https://arxiv.org/abs/2502.12110>
- The previously collected load-bearing number is MISATTRIBUTED: in A-MEM v6 Table 2 (GPT-4o-mini backbone), 27.02→9.65 is the SINGLE-HOP F1 drop when both link-generation (LG) and memory-evolution (ME) are ablated; the MULTI-HOP F1 drop is 45.85→24.55 (with w/o-ME intermediate at 31.24). The direction (large degradation from ablation) is confirmed, but the category label in the design document is wrong. — <https://arxiv.org/html/2502.12110v6>
- The claim 'flat baselines beat A-MEM on Open Domain and Adversarial' is only PARTIALLY true and backbone-specific: the LoCoMo baseline beats A-MEM on Adversarial only for GPT-4o-mini (69.23 vs 50.03), and LoCoMo (61.56) and MemGPT (60.16) beat A-MEM (48.43) on Open Domain only for GPT-4o; on all four smaller backbones (Qwen 1.5b/3b, Llama 1b/3b) A-MEM wins both categories. — <https://arxiv.org/html/2502.12110v6>
- The ablation does NOT isolate typing itself: Table 2 varies only the link-generation and memory-evolution modules and covers only GPT-4o-mini; no ablation variant removes keywords/tags/contextual descriptions, so A-MEM cannot be cited as direct evidence that TYPE LABELS (as opposed to inter-note linking and note updating) drive the gains. — <https://arxiv.org/html/2502.12110v6>
- Zep achieves up to 18.5% (relative) accuracy improvement on LongMemEval — gpt-4o overall accuracy 60.2% (full-context baseline) to 71.2% (Zep) — while reducing response latency by ~90% (28.9s/115k tokens down to 2.58s/1.6k tokens). Numbers CONFIRMED as stated in the design doc, but they are vendor-reported: all five authors are Zep AI employees, with no independent replication cited. — <https://arxiv.org/abs/2501.13956>
- Zep's LongMemEval gains are concentrated in cross-session and temporal question types: for gpt-4o, multi-session accuracy rises 44.3% to 57.9% and temporal-reasoning 45.1% to 62.4% (Table 3). Both numbers in the design doc VERIFIED against the paper's per-category breakdown. This supports the pattern that typed/temporal graph structure pays off specifically on multi-hop and time-sensitive queries. — <https://arxiv.org/abs/2501.13956>
- Adding graph-based memory structure to Mem0 yields only about a 2% overall improvement on the LOCOMO benchmark (LLM-as-a-Judge metric), despite the added structural machinery. — <https://arxiv.org/abs/2504.19413>
- The graph-structured variant HURTS performance on single-hop and multi-hop question categories: single-hop drops 67.13 to 65.71 and multi-hop drops 51.15 to 47.19 (LLM-as-a-Judge scores) versus base Mem0 — confirming the exact numbers cited in the design document. — <https://arxiv.org/abs/2504.19413>
- Graph structure's gains are concentrated in temporal reasoning (55.51 to 58.13) and open-domain (72.93 to 75.71) categories — the paper attributes this to relational representations aiding temporally grounded, multi-step contextual integration, i.e., structure pays off only for specific query shapes. — <https://arxiv.org/abs/2504.19413>
- EMem's event-proposition memory beats the full-context baseline on both benchmarks with gpt-4o-mini: LoCoMo overall LLM-judge score 0.780 (EMem and EMem-G) vs 0.723 for full context, and LongMemEval_S average accuracy 77.9% (EMem-G) / 76.0% (EMem) vs 55.0% for full context. This confirms the load-bearing claim that EMem beats full-context on LoCoMo/LongMemEval, though evaluation is author-run and the paper is a non-peer-reviewed preprint. — <https://arxiv.org/abs/2511.17208>
- EMem beats flat chunk-based RAG on LoCoMo by a large margin — RAG-4096 (4096-token chunks, dense retrieval) scores 0.302 vs EMem's 0.780 with gpt-4o-mini — but the RAG baseline is absent from the LongMemEval_S table, so the previously collected claim 'beats flat RAG on LoCoMo/LongMemEval' is only verified for LoCoMo. — <https://arxiv.org/abs/2511.17208>
- EMem's memory units are structured event propositions, not knowledge-type-labeled statements: each session is decomposed into enriched elementary discourse units (EDUs) — self-contained statements with normalized entities, temporal cues, and source-turn attributions in a heterogeneous graph. The paper therefore supports fine-grained structured decomposition of memory, but is not direct evidence for assigning knowledge-type labels (claim/rule/preference etc.) to units. — <https://arxiv.org/abs/2511.17208>
- CoALA is a conceptual framework/survey paper that contains no original empirical experiments, benchmarks, or quantitative measurements of its own — it therefore provides NO empirical evidence that typed memory improves agent performance, confirming the research brief's unverified claim. The full text (checked via ar5iv) has no experiment section, no results tables, and no accuracy numbers from the authors' own runs; the memory taxonomy is purely organizational. — <https://arxiv.org/abs/2309.02427>
- CoALA proposes a four-way typed memory scheme for language agents — working, episodic, semantic, and procedural memory — which is the canonical typing taxonomy that later typed-memory systems (A-MEM, Zep, Mem0-graph, etc.) trace back to; the types are defined conceptually, not derived from measured outcomes. — <https://arxiv.org/abs/2309.02427>

## Run C-classifier-design  (workflow wf_d873c0e9-e59, task wq4m9cl1l)

**11 confirmed / 12 extracted-but-unverified / 2 refuted**

### CONFIRMED (3-0): Across 7 LLMs annotating 121 ritual features in 567 ethnographic excerpts, mean pairwise LLM-LLM Cohen's kappa was 0.233, versus 0.573 for human-human agreement — different models applying the same codebook agree far less with each other than trained human coders do.

> LLMs agreed with each other substantially less than human coders agreed with each other. Mean LLM-LLM κ was .233 compared to human-human κ of .573

Source: <https://arxiv.org/abs/2601.12099>

### CONFIRMED (3-0): Multiclass features (multiple ordinal or categorical options) had 90% lower odds of correct detection than binary features (OR=0.10, 95% CI 0.03–0.35) — supporting binary probes per label over one multiclass call for fine-grained typing.

> multiclass features had 90% lower odds of correct detection than binary features (OR=0.10, 95% CI: 0.03–0.35)

Source: <https://arxiv.org/abs/2601.12099>

### CONFIRMED (3-0): Concrete, observable features (ritual function, movement) reached F1 above 0.60 for the best models, while interpretive/inferential features (psychological discomfort, arousal levels, ritual form) fell below F1 0.30 — label sets should be anchored in surface-observable criteria, not judgment calls.

> Features relating to ritual function (e.g., funerary, initiation, newborn ceremonies) and movement (e.g., dancing, singing) were annotated with relatively higher accuracy (F1 >> 0.60 for the best models)...features requiring interpretive inference, such as psychological discomfort, arousal levels, and ritual form, proved considerably more difficult (F1 << 0.30).

Source: <https://arxiv.org/abs/2601.12099>

### CONFIRMED (3-0): On the interpretive TREC question-classification task (6 classes), 20 semantically equivalent prompts differing only in wording produced accuracy spreads of 0.546-0.808 for GPT-4o mini and 0.392-0.756 for LLaMa3.1:8b (temperature=0, formatting held constant) — i.e., prompt wording alone can swing classification accuracy by ~26-36 points per model.

> accuracy varies significantly across semantically equivalent prompts, ranging from 0.808 (prompt: Examine the meaning of the question and identify the type of answer the question is expecting...) to 0.546 (prompt: If someone asks the following question, what kind of answer are they expecting...) for GPT-4o mini, and from 0.756 to 0.392 for LLaMa3.1:8b. This large performance spread in accuracy while no-seemingly difference in prompts indicates that linguistic variation alone can induce significant differences in model outputs.

Source: <https://arxiv.org/abs/2604.16413>

### CONFIRMED (3-0): Prompt sensitivity is strongly task-dependent (a 'Knowledge Anchoring Effect'): on the interpretive TREC task, pairwise agreement rate (PAR) between prompts spread over 40% with SD > 0.1, while on the knowledge-anchored Politifact fact-checking task (ordinal scoring) the fluctuation range was only 3% with SD 0.02 — interpretive classification is far less stable under rewording than knowledge-grounded classification.

> both models show substantial disagreement across semantically equivalent prompts, with PAR spread over 40% ... the PAR heatmap in Figure 2 also reveals a much narrow fluctuation range of only 3% with SD of 0.02, indicating a much high inter-prompt agreement under continuous scoring in Politifact datasets.

Source: <https://arxiv.org/abs/2604.16413>

### CONFIRMED (3-0): With six LLMs (GPT-4o, GPT-4o-mini, Gemini 2.5 Pro, Gemini 2.0 Flash, Llama 3.3-70B, Llama 3.1-8B) annotating 2024 U.S. election posts across five harm categories, LLM-LLM pairwise Cohen's kappa exceeded human-human kappa on every category (Conspiracy 0.75 vs 0.43; Hate Speech 0.62 vs 0.32; Sensationalism 0.60 vs 0.23; Speculation 0.58 vs 0.21; Satire 0.53 vs 0.16) — the opposite direction of the 2601.12099 finding (LLM-LLM 0.23 vs human 0.57).

> Inter-rater reliability analyses show comparable agreement patterns between LLMs and humans, with LLMs exhibiting higher internal consistency and achieving up to 0.90 recall on Speculation. [Reported pairwise Cohen's kappa across 15 LLM pairs: Conspiracy 0.75 ± 0.05, Hate Speech 0.62 ± 0.08, Sensationalism 0.60 ± 0.07, Speculation 0.58 ± 0.09, Satire 0.53 ± 0.09; human-human: 0.43, 0.32, 0.23, 0.21, 0.16 respectively]

Source: <https://arxiv.org/abs/2602.11962>

### CONFIRMED (3-0): Majority voting over the three best-performing LLMs drawn from different model families improved agreement with human consensus versus single models, but expanding the ensemble to five LLMs slightly reduced inter-rater reliability — i.e., ensemble gains saturate and can reverse.

> Five-model voting "did not improve IRR and, in fact, led to slightly lower agreement." [Three-model combinations per category, e.g., Conspiracy: Llama 3.1 + GPT-4o + Gemini 2.5 reached kappa 0.62–0.65 against human consensus]

Source: <https://arxiv.org/abs/2602.11962>

### CONFIRMED (3-0): On concrete/less-interpretive tasks (sentiment, political leaning), LLMs across different model families achieved high inter-rater reliability and higher internal consistency than human annotators — evidence that cross-family label agreement is achievable for concrete label types.

> The results reveal that both humans and LLMs exhibit high reliability in sentiment analysis and political leaning assessments, with LLMs demonstrating higher internal consistency than humans.

Source: <https://arxiv.org/abs/2501.02532>

### CONFIRMED (3-0): Both humans and LLMs showed low agreement on sarcasm detection, corroborating the pattern that interpretive statement types resist consistent classification regardless of annotator type — consistent with the interpretive-vs-concrete divide claimed in arXiv 2601.12099 and the sarcasm Fleiss-kappa≈-0.001 result in arXiv 2605.06940.

> Both groups struggled with sarcasm detection, evidenced by low agreement.

Source: <https://arxiv.org/abs/2501.02532>

### CONFIRMED (3-0): High LLM-LLM agreement can coexist with systematic divergence from human judgment: on emotional intensity, LLMs agreed with each other more than humans did, yet humans rated intensity significantly higher — showing inter-model agreement is not evidence of validity against human ground truth.

> In emotional intensity, LLMs displayed higher agreement compared to humans, though humans rated emotional intensity significantly higher.

Source: <https://arxiv.org/abs/2501.02532>

### CONFIRMED (3-0): On 200 real-world support conversations annotated across four empathy frameworks, LLM-expert agreement (Cohen's weighted kappa median 0.60, range 0.17-0.86) essentially matched expert-expert agreement (median 0.58, range 0.11-0.84), with Expert-LLM pairs exceeding the high-agreement threshold in 15 of 21 sub-components — a counterpoint to studies reporting low LLM annotation reliability, and directly on conversational (chat-like) text.

> Reliability between experts and LLMs closely followed expert reliability with κw between experts and LLMs ranging from 0.17 to 0.86 (median = 0.60), with most values between 0.49 and 0.70 (IQR).

Source: <https://arxiv.org/abs/2506.10150>

### Extracted but NOT verified (verification died on spend limit — treat as leads)

- Three frontier model families (Gemini 2.5 Pro, GPT-4o, Claude 3.7 Sonnet) agreed with each other at Krippendorff's alpha 0.51-0.75 (median 0.60) on the same fixed label sets — a much higher cross-model consistency than the mean LLM-LLM Cohen's κ=0.23 reported in arXiv 2601.12099, suggesting cross-family agreement depends heavily on task/label design. — <https://arxiv.org/abs/2506.10150>
- LLM reliability tracked human expert inter-rater reliability across sub-components at Pearson r=0.67 (vs r=0.17 for crowdworkers) — corroborating the r=0.61 'LLM performance tracks human IRR' finding in arXiv 2601.12099: labels humans can't agree on, LLMs can't either, so expert IRR is the right ceiling/benchmark for a classifier's label set. — <https://arxiv.org/abs/2506.10150>
- Sub-components with clear linguistic/behavioral markers were reliably annotated (e.g., 'Explorations' median κw=0.76, 'Practical Advice' κw=0.77) while interpretive/subjective ones were not ('Interpretations' κw=0.29) — replicating the concrete-vs-interpretive split (F1>0.60 vs F1<0.30) claimed in arXiv 2601.12099 and implying knowledge-type labels should be defined by observable surface markers. — <https://arxiv.org/abs/2506.10150>
- Agreement between human experts and frontier LLMs (Gemini 3 Pro, GPT-5) when coding Talk Moves in tutoring dialogues — a conversational-utterance classification task — is only moderate, with Cohen's kappa between 0.38 and 0.58, well below common ground-truth thresholds. — <https://arxiv.org/abs/2603.29141>
- LLM annotation reliability splits sharply by construct concreteness: multimodal LLMs matched expert educators on rote arithmetic grading (κ=0.90) but failed on interpretive conceptual illustrations (κ≈0.47) — corroborating the concrete-vs-interpretive gap reported in arXiv 2601.12099. — <https://arxiv.org/abs/2603.29141>
- Four LLM annotators (ChatGPT, Gemini, Claude, Grok) showed near-total surface agreement on sarcasm labels (0.9612 full-agreement ratio on 'No') while chance-corrected agreement was essentially zero (Fleiss' kappa ~ -0.001), meaning apparent consensus was an artifact of majority-class collapse rather than shared understanding. — <https://arxiv.org/abs/2605.06940>
- Including default 'when uncertain' rules in the annotation prompt (assign Other / Neutral / No for unclear cases) systematically biased all models toward those fallback escape-hatch labels, producing what the authors call instruction-induced label collapse. — <https://arxiv.org/abs/2605.06940>
- Measured against human labels, the LLM annotators missed 79% of hateful instances and 75% of sarcastic instances (false-negative rates), so high inter-model agreement coexisted with severe failure on minority classes. — <https://arxiv.org/abs/2605.06940>
- The reliability of LLM verbalized confidence scores depends strongly on the prompt method used to elicit them, but well-calibrated confidence scores are achievable with certain prompt methods — this verifies the previously collected claim that 'reliability depends primarily on how the model is asked.' — <https://arxiv.org/abs/2412.14737>
- The benchmark scope matches the unverified numbers: 17 prompt methods (10 custom including basic, advanced, combo variants; 7 from prior work by Tian 2023 and Xiong 2023) were tested across 10 QA datasets (arc-c, arc-e, commonsense_qa, logi_qa, mmlu, sciq, social_i_qa, trivia_qa, truthful_qa-mc1/mc2) and 11 models spanning 2B to 110B parameters (Gemma 1.1 2B/7B, Llama 3 8B/70B, Qwen 1.5 7B/32B/72B/110B, GPT-3.5-turbo, GPT-4o-mini, GPT-4o). — <https://arxiv.org/abs/2412.14737>
- Reordering answer options in multiple-choice questions causes LLM performance gaps of approximately 13% to 75% across benchmarks, demonstrating strong positional/order bias relevant to how a fixed label list is presented to a classifier. — <https://arxiv.org/abs/2308.11483>
- LLM answers to multiple-choice questions are not robust to option position: moving the gold answer to a specific position materially shifts accuracy (gpt-3.5-turbo drops 6.3 points, 67.2 to 60.9, when gold answers are moved to position D; llama-30B gains 15.2 points under a favorable move), so a classifier that presents a fixed label set as an ordered option list inherits position/order bias. — <https://arxiv.org/abs/2309.03882>

