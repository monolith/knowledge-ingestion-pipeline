---
title: Taxonomy design — empirically validated annotation schemes (Run A)
date: 2026-08-10
status: COMPLETE — 3-vote adversarially verified
run: wf_b804d853-417
---

# Annotation-Taxonomy Research — Run A (complete)

105 agents, 23 sources, 108 claims extracted, 25 verified → **12 confirmed, 13 refuted**, 9 findings.

> **Read the caveats section.** Source concentration is this run's biggest weakness, and two
> of the most decision-relevant numbers are explicitly in limbo.

## Executive summary

The usable empirical evidence comes from a narrow family of scientific-discourse annotation
schemes (Teufel's AZ and AZ-II, Liakata's CoreSC) plus the Artstein & Poesio methodology survey,
and it says label count is a second-order variable. Growing the tagset cost little (3→7 labels:
κ .78→.71; 7→15 on the same domain: .71→.65), while codebook depth and annotator training moved
κ by .15–.36 on identical documents, and individual category definitions inside one scheme
ranged from κ .43 to .89. Coarsening sometimes helps (7→3: .71→.78; 15→2 on chemistry: .71→.78)
and sometimes does literally nothing (15→2 on CL: .65→.65), and every reported gain is
confounded by a fresh purpose-written codebook, different documents, or merges chosen precisely
where annotators had disagreed. No source in this set measures a fine tagset and its
deterministic coarse rollup on the same annotations with a mapping fixed in advance — the one
experiment that would directly validate the proposed two-tier design — and the
abstract/epistemic categories that most resemble the proposed "model", "claim" and "concept"
types were the least reliable in every scheme that measured them. Design implication: spend the
effort on per-category definitions and the codebook, not on tuning the label count, and measure
agreement at both tiers rather than assuming the coarse layer inherits the fine layer's
reliability (or vice versa).

## Findings

### F1. [HIGH] The frequently cited "Argumentative Zoning, 7 categories, κ≈0.71–0.78" is a conflation of two different experiments. The 7-category scheme's reproducibility is a single value, κ=.71 (N=4261, k=3, 87% raw agreement), with intra-annotator stability .82/.81/.76 (N=1220, k=2). The .78 belongs to a separate 3-category experiment (BACKGROUND/OTHER/OWN).

*Vote: 3-0 (two independent primary sources, both read in full)*

EACL 1999 §3.1 verbatim: "the basic annotation scheme is stable (K=.83, .79, .81; N=1248; k=2
for all three annotators) and reproducible (K=.78, N=4031, k=3)… The full annotation scheme is
stable (K=.82, .81, .76; N=1220; k=2…) and reproducible (K=.71, N=4261, k=3)." The CL journal
2002 paper restates the same figures with raw-agreement equivalents (87% / 93%, 92%, 90%) and
confirms exactly seven flat categories (AIM, TEXTUAL, OWN, BACKGROUND, CONTRAST, BASIS, OTHER)
over an 80-article, 12,188-sentence CL corpus with 3 annotators, one of whom was the first
author. Robustness: "Leaving the coding developer out of the coder pool for Study II did not
change the results (K=.71, N=4261, k=2)." Practical consequence — any design argument that
quotes "0.78" as the achievable ceiling for a 7-label scheme is quoting a 3-label number.

- <https://aclanthology.org/E99-1015/>
- <https://aclanthology.org/J02-4002/>

### F2. [HIGH] Codebook depth and annotator training dominate achievable agreement — they move kappa several times more than label count does. The same documents and the same label set produced κ=.65/.85/.87 with trained coders (6- and 17-page instructions, 4 training papers, weekly discussion) and κ=.35/.49/.72 with 18 untrained subjects given 1 page — drops of .30, .36 and .15.

*Vote: 2-1 (verifier confirmed every number verbatim; the dissent concerned the phrase "not the label set", which is inference rather than a controlled contrast)*

EACL 1999 §3.2 verbatim: "Subjects were given only minimal instructions (1 page A4), and the
decision tree… randomly chosen from the set of papers for which our trained annotators had
previously achieved good reproducibility in Study II (K=.65,N=205,k=3; K=.85,N=192,k=3;
K=.87,N=144,k=3)… Reproducibility varied considerably between groups (K=.35, N=205, k=6; K=.49,
N=192, k=6; K=.72, N=144, k=6)." The paper pre-empts the k=6-vs-k=3 objection ("Kappa is
designed to abstract over the number of coders") and states the causal reading itself: "our very
short instructions did not provide enough information for consistent annotation." Honest
narrowing: recomputed on the three most-similar annotators per group the gap shrinks to .15/.22,
still below trained. Magnitude comparison within the same paper: training/codebook = .15–.36;
3→7 label growth = .07. Countervailing datapoint from CoreSC: a 45-page codebook with decision
tree, category semantics, 6 pairwise-distinction rules and worked examples still yielded only
κ=0.50–0.57 — so codebook investment is necessary, not sufficient.

- <https://aclanthology.org/E99-1015/>
- <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>

### F3. [HIGH] Adding labels costs agreement, but only a little, and the cost is not reliably attributable to label count alone: 3→7 labels cost .07 (.78→.71); 7→15 within computational linguistics cost .06 (.71→.65). Across schemes the relationship inverts entirely — the 15-category AZ-II reached Fleiss κ=0.71 while the 11-category CoreSC reached only Cohen κ=0.57/0.50.

*Vote: 3-0 on the cross-scheme inversion; 2-1 on the AZ-II within-domain drop (dissent: the 7-category baseline is a different study, corpus and annotator pool)*

EMNLP 2009 §4.2 verbatim: "The inter-annotator agreement for chemistry was κ = 0.71
(N=3745,n=15,k=3). For CL, the inter-annotator agreement was κ = 0.65 (N=1629,n=15,k=3). For
comparison, the inter-annotator agreement for the original, CL-specific AZ with 7 categories was
κ = 0.71 (N=3420,n=7,k=3)." The paper's headline "no loss of agreement despite more
distinctions" rests on the chemistry 0.71 versus the CL 0.71 — a cross-domain comparison the
authors caveat themselves ("when comparing the raw numerical results one should consider that
different data from different disciplines is used"), and they float the alternative explanation
that chemistry discourse may simply be easier to annotate. LREC 2010 supplies the inversion: 15
flat AZ-II labels at 0.71 versus 11 CoreSC coarse labels at 0.57/0.50, with confounds stated in-
paper (different corpora, Cohen vs Fleiss — though the paper adds that Siegel & Castellan's
multi-rater formula gave "very similar" values, weakening that particular confound, and CoreSC
annotators were domain experts whose quality "was determined post-hoc" and varied widely).
Design read: a 15–20 label fine tier is not, by size alone, outside the range where trained
humans reach substantial agreement.

- <https://aclanthology.org/D09-1155/>
- <https://aclanthology.org/E99-1015/>
- <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>

### F4. [HIGH] Coarsening a label set does not automatically buy agreement. Collapsing all 15 AZ-II labels to a single binary distinction lifted chemistry from 0.71 to 0.78 but left computational linguistics unchanged at 0.65 — 15 labels down to 2, zero measurable gain. The reliability ceiling was set by definitional clarity and domain, not by how many labels were on offer.

*Vote: 2-1 (numbers verbatim-verified; dissent noted that a differently-designed 7-label scheme did score .71 on CL, mild counter-pressure on the sweeping half)*

EMNLP 2009 verbatim: "we first consider the binary distinction between zone categories (OWNMTHD,
OWNRES, OWNCONC, OWNFAIL, OTHR, PREVOWN and COGRO) and rhetorical categories (the other 8). This
shows an inter-annotator agreement of κ_binary = 0.78 (N=3745, n=2, k=3) for chemistry and
κ_binary = 0.65 (N=1629, n=2, k=3) for CL, indicating that annotators find it relatively easy
(chemistry) or at least not more difficult than the overall distinction (CL) to distinguish
these two types of categories." Statistical nuance the parent should carry: kappa at n=2 has far
higher chance agreement than at n=15, so an unchanged κ means raw observed agreement rose
substantially while chance-corrected reliability did not — "zero gain" is true in reliability
terms, not in raw-agreement terms. The paper frames this test as a probe of "how well categories
are defined," which is the mechanism the finding names.

- <https://aclanthology.org/D09-1155/>

### F5. [HIGH] Every measured gain from coarsening in this literature is confounded, and the authors of the canonical survey explicitly warn that collapsing labels after the fact is NOT equivalent to having designed the coarser scheme up front. Reported gains span +0.024 to +0.41 kappa depending on how the merge was chosen.

*Vote: 3-0*

Artstein & Poesio (CL 34(4), pp. 586-587) verbatim: "Palmer, Dang, and Fellbaum (2007) achieved
for the English Verb Lexical Sense task of SENSEVAL-2 a percentage agreement among coders of 82%
with grouped senses, as opposed to 71% with the original WordNet senses… Véronis (1998) found
that agreement on noun word sense tagging went up from a K of around 0.45 to a K of 0.86… We
should note, however, that the post hoc merging of categories is not equivalent to running a
study with fewer categories to begin with." Two weaknesses attach to the headline numbers:
Véronis and Bruce & Wiebe used clustering to merge "the two classes found to be harder to
distinguish" — merges selected exactly where coders disagreed, mechanically maximizing the gain
— and the Palmer 71→82 figure is uncorrected raw percentage agreement. The same paragraph
contains a near-null case the optimistic reading omits: Bruce & Wiebe's collapse of "interest"
senses raised K only 0.874→0.898 (+0.024). Independently, Teufel & Moens's 7→3 result (.71→.78)
came from a fresh annotation pass over 22 DIFFERENT articles with "seven pages of new guidelines
describing the semantics of the three categories" — a coarse scheme with its own dedicated
codebook, not a rollup of existing labels; and per-annotator stability did not rise uniformly
there (.82→.83, .76→.81, but .81→.79). Direct design consequence: the coarse tier's reliability
cannot be claimed from a rollup of fine-tier annotations, and vice versa; if coarse-level
reliability is what matters operationally, it must be measured with annotators who saw the
coarse scheme.

- <https://aclanthology.org/J08-4004/>
- <https://aclanthology.org/J02-4002/>

### F6. [HIGH] Within a single scheme, per-category reliability varies by a factor of two, and the abstract/epistemic categories are systematically the worst — precisely the ones that resemble the proposed "model", "claim" and "concept" coarse types. CoreSC Cohen's κ: Conclusion 0.89, Background 0.87, Object 0.81, Observation 0.79, Result 0.78, Method 0.74, Experiment 0.65, Goal 0.60, Hypothesis 0.46, Motivation 0.46, Model 0.43.

*Vote: 3-0 on the measurement; the mapping onto the proposed KB types is the analyst's inference, not a finding*

LREC 2010 §5.1 states the method verbatim (Krippendorff's diagnostic: "collapses all categories
but the one in focus into one category and then measures reproducibility") and the verdict:
"Conclusion, Background, Observation and Object are easier to recognise, whereas Hypothesis,
Motivation and Model are harder to recognise than the average taken at κ=0.55." All 11 Table 3
values were transcription-checked against the PDF and independently corroborated in the authors'
Bioinformatics 28(7) republication (doi:10.1093/bioinformatics/bts071, Table 1). Byrt's adjusted
values are uniformly lower, spanning 0.39–0.79. The same pattern appears in AZ-II: the aggregate
CoreSC-vs-AZ-II gap is driven entirely by the badly-carved categories — CoreSC's best (0.89,
0.87, 0.81) actually beat AZ-II's best (USE 0.82, AIM 0.80, OWNMTHD 0.76). Caveats: these are
one-vs-rest binary collapses and are mechanically inflated relative to the 11-way κ=0.50–0.57;
the 0.55 comparison baseline is the paper's own loose framing (the arithmetic mean of the 11
values is 0.68); and CoreSC's "Model" means a theoretical/mathematical representation of a
studied phenomenon, so transferring it to a knowledge-base "model" type is an assumption. Design
read: a few ill-defined categories sink a whole scheme's aggregate agreement, and the epistemic
ones are the usual culprits.

- <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>

### F7. [HIGH] ABSENCE FINDING — no source in this evidence set reports agreement at the fine level of a two-tier scheme. CoreSC is a genuine two-tier design (18 composed flat labels rolling up to 11 coarse) but reports only the n=11 coarse figure; PDTB 2.0 has a three-level 4/16/23 hierarchy but the surviving claim about it carries no agreement statistic at all. The single most decision-relevant experiment for the proposed design has not been located.

*Vote: 3-0 on PDTB structure; 2-1 on CoreSC, with the absence confirmed by exhaustive table inspection*

LREC 2010 §2.1: "If we combine the layers of annotation so as to give flat labels, we cater for
the categories in table 1" — Table 1 enumerates exactly 18 (Hypothesis, Motivation, Background,
Goal, Object-New, Object-New-Advantage, Object-New-Disadvantage, Method-New, Method-New-
Advantage, Method-New-Disadvantage, Method-Old, Method-Old-Advantage, Method-Old-Disadvantage,
Experiment, Model, Observation, Result, Conclusion). The reported kappas carry n=11 (footnote 1:
"n for the number of categories"), and Table 3's 11 rows use coarse names ("Object", "Method",
not Object-New / Method-Old-Disadvantage). The verifier confirmed by full-table inspection that
the fine labels appear with numbers in exactly one place — a raw co-occurrence contingency
table, not an agreement statistic. Notably, this is the one case where a fine→coarse collapse
did NOT rescue agreement: 18 fine labels collapsed to 11 coarse still only reached 0.50–0.57.
PDTB 2.0 manual §4.2 verbatim: "The tagset of senses is organized hierarchically… The top level,
or class level, has four tags… For each class, a second level of types is defined… A third level
of subtype specifies the semantic contribution of each argument"; counts of 16 types and 23
subtypes were derived by enumerating Figure 1 (the manual never states those totals
numerically). Scope note: PDTB 3.0 (2019) revised the hierarchy, so these counts are version-
locked.

- <http://www.lrec-conf.org/proceedings/lrec2010/pdf/644_Paper.pdf>
- <https://www.cis.upenn.edu/~elenimi/pdtb-manual.pdf>

### F8. [HIGH] METHODOLOGICAL REQUIREMENT — raw percentage agreement is biased toward schemes with fewer categories, so agreement cannot be compared across the fine and coarse tiers (or across schemes) without chance correction. Two coders labelling at random agree on 1/2 of items with 2 categories but only 1/3 with 3.

*Vote: 3-0*

Artstein & Poesio §2.3 verbatim, quoting Scott (1955, p. 322): "[percentage agreement] is biased
in favor of dimensions with a small number of categories… given two coding schemes for the same
phenomenon, the one with fewer categories will result in higher percentage agreement just by
chance… pure chance will cause the coders to agree on half of the items (1/4 + 1/4)… they would
only agree on a third of the items (1/9 + 1/9 + 1/9)." Two scope qualifications the raw claim
omits: (a) the bias holds under uniform marginals — skew matters at least as much, and A&P's Di
Eugenio & Glass example shows a 95%/5% binary scheme has chance agreement 0.905, so "a seemingly
high observed agreement of 90% is actually worse than expected by chance"; (b) chance correction
does not fully restore comparability either — A&P §3 documents that π/κ/α are themselves
distorted by prevalence ("the exceeding difficulty in getting high agreement values when most of
the items fall under one category"). Since a knowledge-base taxonomy with a "general" residual
will almost certainly be skewed, expect kappa to look pessimistic even when the classifier is
behaving. IMPORTANT CITATION CORRECTION: two upstream claims cited
https://aclanthology.org/J08-2004/, which is a different paper entirely (Xue, "Labeling Chinese
Predicates with Semantic Roles"). The correct source is J08-4004.

- <https://aclanthology.org/J08-4004/>

### F9. [MEDIUM] ABSENCE FINDING — three of the five research angles returned nothing that survived verification: residual/"other" category design (angle 4), domain statement-type classification in requirements engineering, legal deontic norms, and clinical guidelines (angle 2), and before/after codebook-design studies from the content-analysis methodology literature (angle 5). There is currently no empirical basis in this evidence set for how to design or size the "general" residual bucket.

*Vote: n/a — inferred from the composition of the surviving claim set*

Both candidate residual-design claims were voted down 0-3: the SWBD-DAMSL claim that residual
space is split by cause (% uninterpretable / x non-verbal / o other-forward-function / no other-
answers) under a mechanical decision rule, and the AZ claim that a forced-choice scheme with no
dustbin still concentrated 67% of sentences in one category. No requirements-engineering, legal-
deontic (LegalRuleML, Waltl, Ashley) or clinical-guideline claim reached the confirmed set at
all, nor did any Krippendorff/Neuendorf/MacQueen codebook-development study. Read this as a
coverage gap in this run rather than proof of absence in the literature — the run's search
budget was exhausted mid-verification and effort concentrated on the AZ/CoreSC lineage. The
nearest usable proxy evidence is finding 2 (codebook depth moved kappa by .15–.36), which
supports investing in residual-bucket definitions but says nothing about their shape.

- <https://web.stanford.edu/~jurafsky/ws97/manual.august1.html>
- <https://aclanthology.org/J02-4002/>

## Caveats

SOURCE CONCENTRATION IS THE BIGGEST WEAKNESS. Nine of the twelve confirmed claims trace to four
papers from essentially one research lineage — Teufel is an author on AZ (1999, 2002), AZ-II
(2009) and CoreSC (2010), and Liakata co-authors the CoreSC work. The apparent breadth of
"multiple primary sources" overstates independence. The one genuinely external source is
Artstein & Poesio's methodology survey, which contributes no new annotation data. Nothing here
is independent replication.  UNRESOLVED INTERNAL INCONSISTENCY. Verifiers for two CONFIRMED
claims independently extracted, from the primary PDFs, numbers showing that collapsing fine
labels on IDENTICAL data raised agreement — AZ-II 15→6 coarse, κ 0.71→0.75 on the same chemistry
corpus (with a stated deterministic union rule: OWN = OWNFAIL ∪ OWNMTHD ∪ OWNRES ∪ OWNCONC ∪ FUT
∪ NOVADV), and AZ 7→5, κ .71→.75 on the same Study II data. Yet the standalone claims asserting
those results were both voted down 0-3. The refutations most likely targeted the interpretive
overreach ("direct evidence that a two-tier rollup buys reliability at no annotation cost")
rather than the arithmetic, but that is my inference. These are the two most decision-relevant
numbers in the entire run and they are currently in limbo — treat them as unverified until re-
checked.  VOTE QUALITY. Four confirmed claims passed 2-1, not unanimously (the AZ-II within-
domain drop, the binary-collapse result, the training-dominance claim, and the CoreSC agreement
figures). In each case the dissent concerned causal framing, not the numbers.  CITATION ERROR.
Two claims cited https://aclanthology.org/J08-2004/ for Artstein & Poesio; that URL is a
different paper. Correct: https://aclanthology.org/J08-4004/. Anyone re-checking should use the
corrected URL.  CoreSC SCOPE OVERSTATED UPSTREAM. The "16 chemistry experts over 265 papers"
framing attaches to corpus scale; the κ=0.50–0.57 figures come from phase I only (41 papers) and
from the 9 best-performing annotators. The error runs conservative — a best-9 subset scores at
least as well as the full pool.  TRANSFER IS AN ASSUMPTION, NOT A FINDING. All evidence is
humans labelling running sentences inside full scientific papers. The design in question types
short, pre-extracted knowledge statements from mixed document and chat sources, with no
surrounding discourse. Whether agreement transfers up or down is untested here — a claim
suggesting it goes UP (κ .84 for typing pre-selected statements out of context, vs .71 for full-
document labelling) was refuted 0-3 and remains open.  VERIFICATION METHOD LIMIT. The session's
WebSearch budget was exhausted (200/200) partway through verification, so most verifiers
substituted full primary-document extraction for external contradiction sweeps. For "what does
paper X report" claims that is the stronger check; for "is this the consensus reading" it leaves
a real gap. Several verifiers also caught the WebFetch summarizer returning fabricated numbers
and wrong titles, and worked around it by decompressing PDF streams directly — treat any figure
in this report that was NOT verbatim-extracted with suspicion.  TIME-SENSITIVITY: none of
practical consequence. These are fixed historical measurements of human annotation behavior
(1999–2010) and do not decay like model benchmarks. The one version-locked item is PDTB: the
4/16/23 counts are PDTB 2.0 only; PDTB 3.0 (2019) revised the hierarchy.  HOUSE-RULE NOTE for
the parent: per the deep-research persistence rule, the full claim set with confidence labels,
named sources, evidence and adversarial verdicts should be written to a *-research.md beside the
artifact it informs (for a plugin skill, skills/<name>/references/ so it ships) and linked from
that artifact. I did not write it — subagent instructions forbid report files.

## Open questions

- Does deterministic fine-to-coarse rollup preserve or improve reliability on the SAME
annotations with the mapping fixed in advance? Two primary texts appear to contain exactly this
result (AZ-II 15→6: κ 0.71→0.75; AZ 7→5: κ .71→.75), extracted verbatim by verifiers of
confirmed claims, but the standalone claims asserting them were refuted 0-3. This is the single
most important unresolved item — it is the direct empirical test of the proposed two-tier design
and it needs a clean re-verification.

- How should the "general" residual be designed and how large should it be expected to grow?
Nothing survived on catch-all category design — not the SWBD-DAMSL split-by-cause precedent, not
the mass-concentration evidence, not any annotation-science guidance on abstain-vs-residual.
Worth a dedicated second pass, since a badly-defined residual is the most likely failure mode
for a scheme whose weakest categories (per finding 6) are the abstract ones.

- Does agreement transfer from full-document sentence labelling to short, pre-extracted
knowledge statements shown without context? The evidence base is entirely the former; the design
is entirely the latter. One refuted claim pointed the opposite way from intuition (κ .84 out of
context vs .71 in running text), so the direction of the effect is genuinely unknown.

- Do the applied domains — requirements engineering (functional vs non-functional), legal
deontic classification (obligation/permission/prohibition), clinical recommendation-strength
typing — report human inter-annotator agreement at all, or only downstream classifier F1? If
they report only F1, that is itself a finding about what the field considers worth measuring,
and it means the AZ/CoreSC lineage is the only agreement evidence available for this design.

## Refuted — never cite as support

- *(vote 0-3)* Collapsing the fine-grained 15-category AZ-II scheme into 6 coarse categories RAISED inter-annotator agreement from Fleiss' kappa = 0.71 (15-way) to kappa = 0.75 (6-way) on the identical chemistry corpus (N=3745 sentences, 3 annotators). This is direct measured evidence that a deterministic fine-to-coarse rollup of a curated label set yields a coarse layer more reliable than the fine layer it derives from.
- *(vote 1-2)* Achieving kappa ~0.71 on a 15-label statement-typing scheme required an extraordinary codebook investment: 111 pages of A4 guidelines containing a decision tree, 75 explicit pairwise category-distinction rules, worked examples from both domains, plus a separate 10-page domain 'primer' — and 3 months of part-time work to author, developed on 70 chemistry + 20 CL papers held out from the evaluation set. This is the measured cost basis for a 15-label scheme reaching substantial agreement.
- *(vote 0-3)* Deterministically collapsing fine labels into coarser ones measurably RAISED agreement on the identical annotated data: merging CONTRAST, OTHER and BACKGROUND lifted reproducibility from K=.71 to K=.75, while retaining the distinctions the authors considered task-critical (AIM, TEXTUAL, BASIS, plus the basic own/other/background split). This is direct primary evidence that a two-tier design — annotate fine, report/consume coarse — buys reliability at no annotation cost.
- *(vote 0-3)* CoreSC is explicitly built as a two-tier scheme of exactly the shape under design: a first layer of 11 coarse core concepts (Hypothesis, Motivation, Background, Goal, Object, Method, Experiment, Model, Observation, Result, Conclusion) plus a second 'property' layer (New/Old, Advantage/Disadvantage) that composes deterministically into ~18 flat fine labels (e.g. Method-Old-Disadvantage, Object-New-Advantage). The fine labels are a cross-product of coarse type x property, not an independently curated list.
- *(vote 0-3)* The scheme is forced-choice with NO residual/'other'/'miscellaneous' catch-all — every sentence must take exactly one of the seven substantive labels ('OTHER' means 'other researchers' work', a contentful category, not a dustbin) — and the resulting label distribution is extremely skewed, with 67% of all sentences falling into the single category OWN. A knowledge-base scheme that adds a 'general' residual should therefore expect mass concentration well beyond what a balanced design assumes; here one substantive category absorbed two thirds of items without any residual bucket existing at all.
- *(vote 0-3)* Classifying only pre-selected 'important' statements into six rhetorical categories — 200 sentences sampled from 1183 already judged relevant, presented WITHOUT surrounding context — yielded reproducibility kappa .84 (N=200, k=3) and stability .90/.86/.83 (N=100, k=2), substantially better than the .71 obtained when labelling every sentence in a document. This is the closest analogue in the paper to a pipeline that types already-extracted knowledge statements, and it suggests such a task is measurably easier than typing raw running text.
- *(vote 0-3)* The CoreSC scheme — 11 fine-grained knowledge-role categories (Background, Hypothesis, Motivation, Goal, Object, Method, Model, Experiment, Observation, Result, Conclusion) applied at sentence level — achieved only Cohen's κ=0.55 overall inter-annotator agreement, measured on 41 papers across the 9 best annotators. This is well below the κ≈0.7 conventionally treated as usable, and below the κ≈0.71-0.78 reported for Teufel's 7-category Argumentative Zoning.
- *(vote 1-2)* Per-category agreement inside a single fine-grained scheme varies by roughly a factor of two: categories anchored to observable text (Conclusion κ=0.89, Background κ=0.87, Observation κ=0.79) are reliably annotated, while categories requiring inference about author intent or abstraction (Model κ=0.43, Motivation κ=0.46, Hypothesis κ=0.46) are not. Aggregate kappa hides this — the label set, not the annotators, is the failure point.
- *(vote 0-3)* Deterministically collapsing the 11 fine CoreSC labels into 4 coarse groups raises automatic-classification F1 for groups built from high-agreement fine labels (Outcome 81%, Approach 72%) above the best single fine-grained label (Experiment 76%, Background 62%), but the coarse group assembled entirely from low-agreement fine labels (Objective = MOT+GOA+HYP+OBJ) stays at 38%. Collapsing fine labels improves measurable performance only when the constituent labels were themselves reliably distinguishable; it does not rescue an intrinsically ill-defined group.
- *(vote 0-3)* Teufel's Argumentative Zoning shows higher inter-coder agreement at coarse granularity than fine: K=0.81 for the three main zones (own, other, background) versus K=0.71 for the full scheme. This is direct empirical evidence that collapsing a fine label set into a small coarse set raises measured agreement within the same annotation study.
- *(vote 1-2)* SWBD-DAMSL used a fine-grained tagset of 220 tags in actual coding, and the project then deterministically clustered those 220 fine tags into 42 coarser classes for downstream use — the collapse was driven by label sparsity (130 of the 220 tags occurred fewer than 10 times each). This is a direct precedent for a two-tier scheme where a curated fine label set rolls up to a small coarse set, with sparsity as the stated criterion for the rollup.
- *(vote 0-3)* Human annotators achieved an average pairwise Kappa of .80 on the SWBD-DAMSL scheme, with 8 trained linguistics graduate-student coders labeling 1,155 Switchboard conversations (March 1 – July 5, 1997). This is the primary-source value behind the frequently cited SWBD-DAMSL agreement figure; the manual states the statistic without specifying whether it was computed at the 220-tag or 42-class granularity, so granularity-specific agreement is NOT established by this source.
- *(vote 0-3)* The residual/catch-all space is deliberately split by CAUSE rather than pooled into one 'other' bucket — % (uninterpretable verbal), x (non-verbal, e.g. [Laughter]), o (other forward function), no (other answers, most commonly 'I don't know') — and the residual assignment is governed by a mechanical decision rule rather than annotator judgment alone.
