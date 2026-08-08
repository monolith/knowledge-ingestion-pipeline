---
title: Knowledge-type taxonomy for an LLM-maintained wiki — research
date: 2026-08-08
tiers: [verified-3-vote, sourced-unverified]
run: wf_756bdaf1-c84
---

# Knowledge-Type Taxonomy for an LLM-Maintained Wiki — Research

Deep-research pass run 2026-08-07/08 to evaluate a proposed knowledge-type taxonomy
(3 cognitive families x 6 types) for an LLM-maintained wiki in the sense of
[Karpathy's *LLM Wiki* gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
It informs, and should be read against, [`docs/SPECIFICATION.md` §9.3 'Unit ontology'](../docs/SPECIFICATION.md)
and [`docs/KNOWLEDGE-TYPE-TAXONOMY.md`](../docs/KNOWLEDGE-TYPE-TAXONOMY.md).

## How to read this document

Two evidence tiers, matching the convention already used by the `R1`–`R5`/`PE` round files in this folder:

- **Tier 1 — Verified.** Ran 3-vote adversarial verification; a claim needed 2 of 3 verifiers to *fail* to
  refute it to survive. Cite freely, honoring each finding's stated corrections.
- **Tier 2 — Sourced, not adversarially verified.** Extracted from a fetched primary source with a quoted
  or paraphrased evidence line, but never put to a refutation vote. **Do not cite as verified.** These are
  leads and design inputs, at roughly the confidence of a careful single reading.

**The `REFUTED` list in §3 is not a list of debunkings.** The synthesizer flagged explicitly that verifiers
repeatedly hit ACM DL 403, lifescied.org 403, pnas.org 403 and ScienceDirect paywalls, and that at least
three exhausted the session WebSearch budget (200/200) before their counter-searches could run. Most
refutations mean *nobody could open the primary text*, not *the claim is false*. Several refuted items
reappear in Tier 2 with their source attached — that is the same claim at its correct, lower confidence,
not a contradiction.

**Tier-1 coverage is skewed.** All 8 surviving source-claims come from cognitive psychology or
education assessment. Nothing from knowledge representation, agent memory, or retrieval evaluation
survived to Tier 1 — those literatures are present in Tier 2 only. The global verification budget was
25 claims out of 140 extracted, ranked by importance and source quality, which systematically favored
the angles searched first. This is a known failure mode of this harness (see
`project_knowledge_ingestion_plugin` memory); it was diagnosed and the un-verified claims recovered from
the run journal rather than by re-running the search.

---

## 1. Executive summary (from the synthesis agent)

The verified evidence supports the taxonomy's *shape* only weakly and does not support its
*cognitive branding* at all. Every canonical source the proposal invokes either mis-levels its three
families (in Squire's taxonomy episodic sits *inside* declarative, and procedural sits under
nondeclarative — they are not co-equal siblings) or explicitly denies that the boundaries are sharp
(Renoult et al. 2019 on episodic/semantic; Rubin 2021/22 on explicit/implicit, which he judges the
weakest of his three dimensions for lack of a unified neural basis). Critically, the empirical
warrant behind those labels comes from lesion dissociation, conscious accessibility, and
representational flexibility — none of which has an analogue in classifying text on a wiki page — so
borrowing the vocabulary does not import the evidence; "cognitively grounded" here is rhetoric, not
warrant. The one directly transferable empirical result is negative-adjacent: applying small,
abstract cognitive taxonomies to text is a task with known poor inter-rater reliability that
survives targeted rater training and replicates across independent cohorts (Bloom's in computing
education), and the closest two-axis precedent (Larsen et al. 2022, n=940) found the "orthogonal"
second dimension statistically dependent on the first (Fisher's exact, p<0.0001) — though those
authors still recommend coding both axes. Nothing survived verification on the three angles that
would most directly justify the design — DITA/Diátaxis/Information-Mapping precedent, typed LLM-
agent memory (CoALA/MemGPT/A-MEM/HippoRAG/Zep) gains, and whether type-filtered retrieval or
contradiction detection actually improves — so the six-type/three-family structure should currently
be defended as an engineering choice validated by your own evals, not as a finding.

---

## 2. Tier 1 — Verified findings (3-vote adversarial)

### T1-1. HIGH confidence

**Claim.** The proposed three families (Declarative / Procedural / Episodic) are mis-leveled against every canonical taxonomy they invoke: in Squire's canonical carving, Facts and Events are sibling leaves *inside* Declarative sharing one substrate, and Procedural sits under Nondeclarative — so the three are not co-equal. The architectures that do use a co-equal triad (Soar, ACT-R-derived CoALA) name the third module 'semantic', not 'declarative', precisely to avoid this parent/child collision.

**Vote.** merged 2-1 (claim 4) with supporting verifier notes from claims 0 and 5; verifier confidence high

**Evidence and required corrections.**

Verifier independently retrieved the full PNAS text via PMC (Squire LR & Zola SM 1996, PMC33639,
PMID 8942965) and read Figure 1 as an image. The tree: LONG-TERM MEMORY → DECLARATIVE (EXPLICIT) and
NONDECLARATIVE (IMPLICIT); DECLARATIVE branches to exactly two leaves, FACTS and EVENTS, converging
on one box, 'MEDIAL TEMPORAL LOBE / DIENCEPHALON'; PROCEDURAL (SKILLS AND HABITS) → STRIATUM sits
under NONDECLARATIVE alongside priming, classical conditioning, nonassociative learning.
Programmatic count over the complete rendered article (~8,630 body words + captions + 66 refs):
'episodic' = 0, 'semantic' = 0. Verbatim: 'The key distinction is between the capacity for conscious
recollection of facts and events (declarative memory) and a heterogeneous collection of nonconscious
learning capacities (nondeclarative memory).' A separate verifier independently flagged the same
defect from the Renoult side: 'Declarative vs Episodic' is not a well-formed contrast in the
source's own terms, since declarative = semantic + episodic. Recommended softening: Squire does not
'directly contradict' a document taxonomy (different level of description) — he provides no support
for it and mis-levels it. Practical implication: rename the family to Semantic or Conceptual, or
drop the cognitive framing.

**Sources.**
- https://www.pnas.org/doi/10.1073/pnas.93.24.13515
- https://neuropsychologylab.psych.utoronto.ca/files/FromKnowingtoRememberingTheSemanticEpisodicDistinction.pdf

### T1-2. HIGH confidence

**Claim.** The boundaries the taxonomy leans on are continua, not categories — and this is the explicit conclusion of the primary literature, not an outside critique. Renoult et al. (2019) conclude the episodic/semantic boundary is 'not as distinct' as Tulving's proposal implied whether defined anatomically or functionally; Rubin (2021/22) states he knows of 'no convincing evidence' his three dimensions can be reduced to categories, and that categories are retained for communicative convenience only.

**Vote.** merged 2-1 (claim 0) + 3-0 (claim 1); both verified verbatim against primary PDFs at high confidence

**Evidence and required corrections.**

Both verifiers extracted PDF text themselves (no pdftotext available; custom FlateDecode/Tj
extractors) rather than trusting snippets. Renoult, Irish, Moscovitch & Rugg (2019), Trends in
Cognitive Sciences 23(12):1041-1057, Concluding Remarks, verbatim: '...although episodic and
semantic memory represent the expression of different memory systems as Tulving proposed, the
boundaries between them, whether anatomically or functionally defined, are not as distinct as
Tulving's proposal may have led one to believe.' Rubin (Memory & Cognition 2022;50(3), DOI
10.3758/s13421-021-01148-3, PMID 33650021), under a section literally headed 'Continua versus
categories': 'I know of no convincing evidence that the three dimensions I use can be reduced to
categories... The three dimensions are continua. Individual memories vary in a continuous fashion
along these dimensions at both the behavioral and neural level,' and 'using the extremes of those
continua as labels for categories simplifies communication and is necessary to maintain contact with
the literature.' Post-2019 field motion runs the same way (De Brigard/Werning 2024 Phil Trans R Soc
B 379:20230407; 'Semanticization Challenges the Episodic-Semantic Distinction' 2022). TWO LIMITS:
(a) both authors still affirm a coarse distinction — Renoult says the systems 'retain a measure of
distinctiveness' — so this argues for fuzzy-edged coarse types, not for abandoning typing; (b) the
tempting inference 'therefore primary+secondary type with a confidence score is closer to the data'
was put to the verifiers as a separate claim and REFUTED 0-3, so that specific design justification
is unsupported even though the continuum finding is solid.

**Sources.**
- https://neuropsychologylab.psych.utoronto.ca/files/FromKnowingtoRememberingTheSemanticEpisodicDistinction.pdf
- https://sites.duke.edu/rubinlab/files/2021/08/2021-online-ConceptualSpace-Dimension-M-C.pdf

### T1-3. MEDIUM confidence

**Claim.** The explicit/implicit cut — the nearest cognitive ancestor of a Declarative-vs-Procedural content split — is the weakest of Rubin's three dimensions: he judges that empirical support for a plausible neural basis is lacking (unlike self-reference and scene construction), and cites Dew & Cabeza (2011) concluding the constructs used to distinguish explicit from implicit memory have not yielded data consistent with a dichotomy.

**Vote.** 2-1; verifier confidence high on the attributive core, with a required scope correction

**Evidence and required corrections.**

Verbatim from the extracted primary PDF: 'Unlike the self-reference and scene construction
dimensions, empirical support for a plausible neural basis for an explicit versus implicit
distinction is lacking'; and 'In a review article on the "porous boundaries" between explicit and
implicit memory, Dew and Cabeza (2011) conclude that the constructs used in the literature to
distinguish between explicit and implicit memory have not yielded data consistent with the
dichotomy... "simple dichotomies between explicit and implicit memory are inadequate given the
current state of the memory literature" (p. 185).' Rubin affirms the contrast for the other two
dimensions in the same paper ('a plausible underlying neural basis for this dimension exists' for
self-reference; 'strong converging evidence' for scene), which is what licenses 'weakest'. The link
to declarative/procedural is source-grounded, not invented: Rubin cites Squire (1987, pp. 167-169)
listing 'declarative versus procedural, knowing that versus knowing how' as divisions 'closely
related to' explicit/implicit. TWO REQUIRED CORRECTIONS: (1) drop the word 'exact' — Rubin's
dimension is about conscious accessibility at retrieval, whereas a wiki's Declarative/Procedural
split is a content-type distinction over text that is explicit by construction; implicit phenomena
(priming, eyeblink conditioning) have no wiki analogue, and the 2024 Multidimensional Model of
Mental Representations (Phil Trans R Soc B 379:20230408) explicitly confines itself to
explicit/declarative representations for the same reason. (2) 'lacks a plausible neural basis' ≠ 'no
neural evidence' — Squire & Dede 2015 marshal lesion and imaging dissociations; Rubin's narrower
point is that implicit memory is a heterogeneous collection of systems, so the single dimension
lacks a *unified* substrate. Net for the design: the Declarative/Procedural cut is defensible as an
information-design distinction but should not be sold as neurally validated.

**Sources.**
- https://sites.duke.edu/rubinlab/files/2021/08/2021-online-ConceptualSpace-Dimension-M-C.pdf

### T1-4. MEDIUM confidence

**Claim.** The cognitive taxonomy's empirical warrant does not transfer to classifying wiki text. Squire's boundaries are carved by lesion dissociation in amnesic patients, plus conscious accessibility and representational flexibility. No equivalent criterion exists for a text unit on a page, so borrowing the labels borrows the vocabulary and not the evidence — this is a design choice presented as a finding.

**Vote.** 3-0; verifier confidence medium (own counter-evidence sweep was budget-limited)

**Evidence and required corrections.**

Verbatim from the PMC full text: 'Some of the best evidence for distinguishing between kinds of
memory has come from the study of amnesic patients who have sustained bilateral damage to medial
temporal lobe or midline diencephalic brain structures,' and 'the kinds of learning and memory that
are intact in amnesia depend on different brain systems than those damaged in amnesia.' The second
half of the claim is a methodological inference needing no source, and is exactly the 'flag where no
evidence exists' the research question asked for; nothing contradicting it was found. Corroborating
pattern: the systems that DO borrow these labels for machines — Soar's episodic/semantic/procedural
modules, ACT-R's declarative/procedural split, CoALA (Sumers, Yao, Narasimhan, Griffiths 2023) —
justify the split on computational grounds (different update and learning rules), never by citing
lesion evidence. TWO PRECISION DEFECTS, both cutting toward the conclusion: (1) Squire actually uses
three criteria, not one — alongside anatomy he invokes conscious access and flexibility
('Declarative knowledge is accessible to multiple response systems. Nondeclarative memory is more
encapsulated'). Those functional criteria arguably DO have information-design analogues (is a unit
consulted by reference or executed as a procedure; how does it update), so the design is not as
criterion-less as the sentence implies — this is the strongest available reconstruction of the
taxonomy. (2) The amnesia evidence warrants only the declarative/nondeclarative cut, not an Episodic
third family, which rests on a separate and more contested literature (Vargha-Khadem et al. 1997
developmental amnesia vs Squire & Zola's rebuttal).

**Sources.**
- https://www.pnas.org/doi/10.1073/pnas.93.24.13515

### T1-5. MEDIUM confidence

**Claim.** Poor inter-rater reliability when applying a small abstract cognitive taxonomy to text is a property of the task, not of one bad rater pool: it is stated as unattributed background fact in the field's own literature, confirmed by a systematic review, and it survived targeted training interventions and replicated across an independent educator cohort.

**Vote.** 2-1 on the framing claim; verifier confidence high, but with a re-sourcing instruction

**Evidence and required corrections.**

ACM DL 403s, so the verifier pulled the abstract via the Semantic Scholar Graph API and confirmed
character-for-character: Zhang, Wong, Giacaman & Luxton-Reilly (2021), ACE '21 — 'the application of
Bloom's taxonomy in computing education is often difficult and the classification often suffers from
poor inter-rater reliability.' Paper identity cross-checked against the DBLP ACE 2021 TOC (Semantic
Scholar mis-normalizes the venue as an IFAC symposium — metadata artifact of the 'ACE'
abbreviation). With WebSearch exhausted the verifier queried OpenAlex and Semantic Scholar directly
and found only corroboration: Masapanta-Carrión & Velázquez-Iturbide (2018, SIGCSE, systematic
review, 81 cites) — 'the most often reported difficulty is determining the level of the taxonomy
where an assessment task can be classified'; same authors (2019, ITiCSE) — 'different instructors
understand Bloom's taxonomy differently'; training raised accuracy for experienced participants but
'variation was increased, and confidence was decreased for non-experienced participants'; same
authors (2022, IEEE EDUCON) — an explicit replication with a different cohort in which 'high
variation and low accuracy in educators' classifications persisted' despite the interventions; Gluga
et al. (2012, SIGCSE) on 'over-confidence and confusion,' n=10. THREE HANDLING NOTES: keep the
source's 'often' hedge (the claim drops it); Zhang et al. is a consensus indicator, not primary
evidence — they measured BERT accuracy against QuestionBank labels and measured no human IRR at all,
so cite Masapanta-Carrión 2022 as the primary; and no kappa/alpha magnitude was located in any
retrievable abstract, so 'poor' is well-attested qualitatively but UNQUANTIFIED. Transfer caveat:
none of these sources involve LLM raters.

**Sources.**
- https://dl.acm.org/doi/10.1145/3441636.3442305
- https://doi.org/10.1145/3159450.3159491
- https://doi.org/10.1145/3304221.3319748
- https://doi.org/10.1109/educon52537.2022.9766707
- https://doi.org/10.1145/2157136.2157181

### T1-6. MEDIUM confidence

**Claim.** A second 'orthogonal' axis is a testable assumption, and in the closest published precedent it failed: RBT's knowledge-type and cognitive-process dimensions were statistically dependent on 940 assessment items (Fisher's exact, p<0.0001), collapsing into three dominant clusters. But the authors' own conclusion was to keep BOTH axes, not to collapse them — dependence argued for redundant coding, not for a single axis.

**Vote.** 2-1; verifier confidence high on the numbers, with four scope qualifications

**Evidence and required corrections.**

lifescied.org 403s; verified verbatim via Europe PMC full text (PMC9727608) plus Crossref metadata.
Larsen, Endo, Yee, Do & Lo (2022), CBE—Life Sciences Education 21(4), DOI 10.1187/cbe.20-08-0170,
PMID 36112622, CC BY-NC-SA, 47 Crossref cites. Abstract: 'Contingency analysis on 940 assessment
items revealed that the knowledge-type and cognitive-process dimensions are related and not
independent.' Body: 'Fisher's exact test between the knowledge types and cognitive processes
revealed a significant relationship between the two dimensions (p < 0.0001)'; 'three predominant
combinations... factual knowledge with remember; conceptual knowledge with understand, analyze,
evaluate, and create; and procedural knowledge with apply'; 'factual knowledge and remember is the
most common (28%), followed by... conceptual knowledge and understand (23%).' The independence
premise is source-supported, not invented: Table 1 lists the revision feature as 'Separate knowledge
into a dimension orthogonal to the cognitive processes.' FOUR QUALIFICATIONS: (1) the original claim
mis-attached 23% to a four-process cluster — it is conceptual+understand alone; conceptual is 49% of
all items. (2) The authors conclude 'both dimensions of the revised Bloom's taxonomy should be used'
— citing this as 'two-axis taxonomies fail' inverts the paper. (3) Fisher's test reads observed
marginals in a non-random corpus: 834/940 items from ONE private doctoral university's biology
courses (12 courses, 16 instructors, 2011-2015), plus 106 AP-Bio/MCAT items deliberately added after
the authors 'discovered that the assessment items skewed'; the authors state 'we do not attempt to
make universal claims.' Dependence may reflect what instructors choose to test, not logical
entanglement. Coding noise was material: initial Fleiss' κ 0.68 (knowledge type) / 0.70 (cognitive
process), only 17% of items triple-coded and 36% single-coded. (4) 'Closest precedent' is our
judgment — RBT's second axis is cognitive PROCESS (what a learner does), the proposal's is epistemic
STATUS/CONFIDENCE/MATURITY of a unit; the analogy is defensible taste, not evidence. Actionable:
treat status-vs-type orthogonality as an empirical question to measure on your own corpus, and
expect a few type×status cells to absorb most units.

**Sources.**
- https://www.lifescied.org/doi/10.1187/cbe.20-08-0170

### T1-7. MEDIUM confidence

**Claim.** Rubin's structural argument is that a hierarchy of memory types only classifies what has already been observed and leaves well-documented phenomena homeless, whereas a small set of conceptually independent dimensions crossed into a factorial space both organizes the literature and re-homes orphans — explicitly analogized to the early periodic table. Relevant to whether the proposal should be a 3-family/6-type hierarchy or a faceted space.

**Vote.** 3-0 on faithfulness to the source; verifier confidence high — but the source is a single-author theoretical paper with no measurement

**Evidence and required corrections.**

Verifier extracted the full PDF (152,199 chars) and located every element. Structural argument
(offset ~10,900): 'the hierarchy did not predict the existence of new life forms with particular
properties — it just classified what was found... In contrast, for dimensional models, the
properties extend across dimensions creating predictions about the properties of new categories.'
Fig. 1 caption confirms the target is the memory hierarchy: 'A hierarchical organization of
categories of memory (based on Squire, 1987, 2004).' Homeless phenomena (offset ~9,862), all four
named with citations: self-reference semantic memory (Kopelman 1990; Prebble 2013), non-self-
reference episodic memories (Larsen 1988), implicit self-reference memory including habits (Hirst
1994), implicit-scene memory including déjà vu (Brown 2003) — 'fall outside the existing categories
of the standard memory taxonomy.' Factorial claim (offset ~93,026): 'the three dimensions combine to
form eight categories in a nonhierarchical organization... much as the early periodic table did for
chemistry.' THREE FIDELITY FLAGS: (a) the 8 cells are a convenience dichotomization Rubin explicitly
does not endorse as crisp types; (b) 'orthogonal' is the summarizer's word — the paper never uses it
(0 occurrences), says 'conceptually independent,' and notes self-reference and scene are
'independent except for scene memory locating the person remembering relative to the contents of the
memory'; (c) the delivered payoff is weaker than 'predicts unoccupied cells' — the abstract says
'Empty locations in the proposed space are filled with existing phenomena that lack a clear place in
current theories,' i.e. re-homing known phenomena. Cite as argument, never as measured evidence that
facets beat hierarchies.

**Sources.**
- https://sites.duke.edu/rubinlab/files/2021/08/2021-online-ConceptualSpace-Dimension-M-C.pdf

### T1-8. HIGH confidence

**Claim.** NO verified evidence survived on the three angles that would most directly justify this design: (a) prior information-typing systems and what broke in them (DITA, Information Mapping, Diátaxis, upper ontologies, argumentation/claim schemas, PROV-O); (b) typed memory for LLM agents and whether typing measurably helps (CoALA, MemGPT/Letta, A-MEM, HippoRAG, Zep/Graphiti, Mem0, GraphRAG); (c) whether type-aware retrieval, contradiction detection, or insight generation actually improves over flat semantic search. Every surviving claim came from cognitive psychology or education-assessment literature.

**Vote.** n/a — observation about the composition of the verified set

**Evidence and required corrections.**

Confirmed claims map to: Renoult 2019 (TiCS), Rubin 2021/22 (Memory & Cognition) x3, Squire & Zola
1996 (PNAS) x2, Larsen 2022 (CBE-LSE), Zhang 2021 (ACE). Zero confirmed claims cite DITA, Diátaxis,
Horn's Information Mapping, BFO/SUMO/DOLCE, IBIS/nanopublications, Schema.org ClaimReview, CoALA,
MemGPT, A-MEM, HippoRAG, Zep, Mem0, GraphRAG, WikiContradict, or the Karpathy LLM-wiki gist.
IMPORTANT DISTINCTION: this is absence of evidence *in this research pass*, not evidence of absence
in the literature — multiple verifiers reported hitting hard walls (ACM DL 403, lifescied.org 403,
ScienceDirect paywall, pnas.org 403, and at least three verifiers reporting the session's 200/200
WebSearch budget exhausted before adversarial sweeps could run). Practical consequence: the parts of
the proposal that are engineering decisions — sub-page knowledge-unit granularity, one primary +
optional secondary type, classification confidence, status/origin/maturity as metadata rather than
types — currently rest on zero verified external support in either direction. They should be
defended as reasonable engineering to be validated by your own eval harness, and the design doc
should say so explicitly rather than implying literature backing.

**Sources.**
- internal: 8 confirmed / 17 refuted claim set, all sourced to neuropsychology and education-assessment venues

### T1-9. HIGH confidence

**Claim.** Every quantitative claim that taxonomy SIZE drives classification reliability failed verification. The 'six labels are too many, three is safer' argument has no verified support in this evidence set — in either direction.

**Vote.** four separate size/reliability claims voted down (three 0-3, one 1-2)

**Evidence and required corrections.**

Refuted: Karpen & Welch 2016 pharmacy-faculty IRR 0.25 / 46.0% accuracy (1-2); 'collapsing six Bloom
levels to three raised accuracy 46.0%→81.8%' (0-3); 'six-to-three roughly doubles automated
accuracy, 59.2%→82.61% on 504 questions' (0-3, and the claimant themselves flagged it as a secondary
restatement they could not open the ACM PDF to verify); Nasstrom 2009 expert-vs-teacher panel kappas
(0-3); Fleiss κ=0.189 across 8 raters on 42 computing questions (0-3); Larsen's Fleiss κ 0.68/0.70
as a standalone ceiling claim (0-3); 'Metacognitive was never assigned to a single item across 940'
(0-3); zero-shot LLM accuracy 0.72-0.73 for GPT-4o-mini and Gemini-1.5-Pro on six Bloom levels
(0-3). Note the asymmetry: the *qualitative* task-difficulty finding survived (finding above), the
*numbers* did not — consistent with paywalled primary sources rather than with the numbers being
wrong. One number does appear inside verified verifier evidence and can be cited with care: Larsen
et al.'s pre-consensus Fleiss κ of 0.68 (knowledge type) and 0.70 (cognitive process) on a 4-label
knowledge dimension, quoted from the Europe PMC full text the verifier read directly — treat as a
rough expert-human reference point on a comparably sized label set, not as a settled ceiling, since
the standalone claim built on it was voted down.

**Sources.**
- https://www.sciencedirect.com/science/article/abs/pii/S1877129715301921
- https://dl.acm.org/doi/10.1145/3441636.3442305
- https://www.cambridgeassessment.org.uk/Images/426171-on-the-reliability-of-applying-educational-taxonomies.pdf
- https://arxiv.org/html/2511.10903

---

## 3. Tier 1 — Claims that did NOT survive verification

Read with the caveat above: for most of these the verifiers could not open the primary text.
The vote is recorded as `refutes-nonrefutes`.

**R-1** *(vote 0-3)* — Type membership is better described as a graded weighting than as discrete category assignment: the same event is represented with episodic and semantic components whose relative weights shift with elapsed time and with the current task. A taxonomy that forces one primary type per unit is therefore imposing a cut the underlying cognitive evidence does not support; a primary+secondary type with a confidence score is closer to the data.

**R-2** *(vote 0-3)* — The neural correlates of the two putative systems overlap almost completely: fMRI meta-analytic comparison shows the episodic 'core recollection network' and the 'general semantic network' share essentially the same parahippocampal, middle temporal, ventral parietal, and midline frontal/posterior regions, with the hippocampus the conspicuous region present in the episodic network but not the semantic one. The measured dissociation reduces to roughly one region, not two separate systems.

**R-3** *(vote 1-2)* — The same content migrates across the declarative/procedural boundary over time — skills start as explicit memories and become implicit with practice, and priming carries an explicit component — so membership is a function of the retrieval episode rather than an intrinsic property of the knowledge. Squire himself argued total neural separation of the two systems is implausible because explicit processes depend on earlier-evolving implicit regions.

**R-4** *(vote 1-2)* — Authoritative metacognition frameworks disagree on whether 'conditional knowledge' is a distinct type at all: Jacobs & Paris (1987) and Schraw & Dennison (1994) keep it separate, Anderson et al. (2001) — the revised Bloom taxonomy — merge it into Procedural, and Flavell (1987) and Henri (1992) omit it entirely. The declarative/procedural/conditional boundary is therefore NOT settled by evidence; it is a modeling choice that expert authors resolve differently.

**R-5** *(vote 0-3)* — The SAME label names carry incompatible content across authors. Schraw & Dennison define Procedural knowledge as 'about how to use strategies', while Murphy explicitly redefines Procedural knowledge to mean task knowledge and moves strategy knowledge into Declarative. Identical three-label sets are thus not interoperable without pinned definitions and examples — a direct warning for any taxonomy expected to be applied consistently across independent classifiers.

**R-6** *(vote 0-3)* — The primary cut in the empirically-grounded taxonomy is consciousness of retrieval (declarative vs nondeclarative), not content type; 'Procedural (skills and habits)' appears only as one branch UNDER nondeclarative, alongside priming, simple classical conditioning, and nonassociative learning. A taxonomy that puts Declarative, Procedural, and Episodic side by side as three families is therefore mixing two different cutting axes and is not the structure this evidence supports.

**R-7** *(vote 1-2)* — Trained domain experts (pharmacy faculty) applying the six-level Bloom's Taxonomy to exam questions achieved poor inter-rater reliability (0.25) and only 46.0% accuracy against a reference key — direct evidence that a six-category abstract cognitive taxonomy is NOT reliably applied even by human subject-matter experts without training.

**R-8** *(vote 0-3)* — Collapsing the six Bloom levels into three raised classification accuracy from 46.0% to 81.8% — i.e., reducing label count on the same stimuli nearly doubled accuracy, evidence that taxonomy SIZE is a primary driver of classification reliability independent of rater expertise.

**R-9** *(vote 0-3)* — Trained expert human raters applying the Revised Bloom's Taxonomy knowledge dimension (Factual/Conceptual/Procedural/Metacognitive) to 940 biology assessment items achieved only Fleiss' κ = 0.68 for knowledge type (and κ = 0.70 for cognitive process) before consensus discussion — i.e. a small, abstract, cognitively-grounded label set with expert raters and iterative norming still leaves roughly a third of the achievable agreement on the table. This is an empirical ceiling reference for what LLM classifiers on a comparable 4-6 label taxonomy can be expected to hit.

**R-10** *(vote 0-3)* — One of the four knowledge-dimension categories — Metacognitive — was never assigned to a single item across the entire 940-item corpus (0%), while Factual/Conceptual/Procedural absorbed 38%/49%/13%. A taxonomy category can be theoretically well-motivated and empirically dead, which argues for pruning label sets against observed usage rather than against cognitive theory alone.

**R-11** *(vote 0-3)* — Human experts applying Bloom's six-level taxonomy to computing questions achieve only "slight" inter-rater agreement — Fleiss's kappa of 0.189 across 8 raters on 42 questions — even after rater training. This is direct empirical evidence that an abstract, cognitively-grounded ~6-category taxonomy is applied inconsistently by trained humans, which sets a pessimistic prior for asking multiple LLM families to apply a 6-type knowledge taxonomy consistently.

**R-12** *(vote 0-3)* — A fine-tuned BERT classifier trained on expert-labeled questions (Canterbury QuestionBank) achieved only moderate accuracy over the six Bloom categories, and performed markedly better on the lower/more concrete levels than the higher/more abstract ones — evidence that abstractness of a category's definition, not just count, drives classification failure.

**R-13** *(vote 0-3)* — Collapsing the label set from six categories to three roughly doubles reliability of automated classification — reported as 59.2% accuracy on all six Bloom classes versus 82.61% on three classes (Knowledge, Comprehension, Analysis) on a 504-question set. NOTE: this figure is a secondary restatement from surveys citing Zhang et al.; I could not open the ACM PDF (HTTP 403) to verify it verbatim in the primary text. Treat as moderate confidence. It is the single most decision-relevant number for the taxonomy-size question.

**R-14** *(vote 0-3)* — Applying a fixed 6-level taxonomy to items that were DESIGNED to sit at specific levels still produced near-chance agreement: Karpen & Welch (2016) had 21 pharmacy faculty classify 6 exam questions with Bloom's taxonomy and got Krippendorff's alpha = 0.25. This is direct evidence that a small, well-known label set with authoritative definitions does not guarantee consistent application even by domain experts.

**R-15** *(vote 0-3)* — Rater expertise, not the taxonomy, dominates agreement: on the same 35 Swedish upper-secondary Mathematics objectives coded with revised Bloom's, Nasstrom (2009) got kappa 0.47/0.41 from a panel of 4 assessment experts versus 0.15/0.24 from a panel of 4 teachers, with intra-rater kappa 0.43 vs 0.18 — no measure exceeded moderate agreement for either panel.

**R-16** *(vote 0-3)* — There is NO empirical evidence in this literature on whether the number of categories in a taxonomy affects rater reliability. The single study cited as showing that more sub-categories increase agreement (Chan et al. 2002, 9-category vs 5-category SOLO) is judged by the reviewer to have misread its own data, and the question is left open for future research.

**R-17** *(vote 0-3)* — On a fixed six-label taxonomy (Bloom's cognitive-process levels) applied to 600 short sentences, zero-shot LLM classification accuracy topped out at only 0.72–0.73 for GPT-4o-mini (0.72 acc / 0.72 macro-F1) and Gemini-1.5-Pro (0.73 acc / 0.73 macro-F1) — i.e. roughly a quarter of items mislabeled even by frontier-tier models on a well-documented, decades-old six-category scheme.

---

## 4. Caveats carried by the synthesis

SOURCE-BASE SKEW: all 8 confirmed claims come from cognitive psychology (Squire & Zola 1996; Renoult
et al. 2019; Rubin 2021/22) or education-assessment research (Larsen et al. 2022; the Bloom's-in-
computing-education thread). None come from knowledge representation, LLM-agent memory, or retrieval
evaluation — the three literatures that would speak most directly to whether this taxonomy will work
in a wiki pipeline.  "REFUTED" OFTEN MEANS "COULD NOT VERIFY", NOT "SHOWN FALSE". Verifiers
repeatedly hit ACM DL 403, lifescied.org 403, pnas.org 403, and ScienceDirect paywalls, and at least
three reported the session's WebSearch budget exhausted (200/200) before adversarial counter-
searches could run. Two of them said outright that their contradiction sweep rested on the primary
text plus prior knowledge rather than a fresh scan. Do not read the 17-item refuted list as 17
debunkings — read it as claims whose primary text nobody could open.  CROSS-DOMAIN TRANSFER IS THE
WEAKEST LINK THROUGHOUT. Cognitive memory taxonomies classify mental representations by conscious
access and neural substrate; this proposal classifies authored text. Bloom's-taxonomy reliability
studies used human educators on exam questions, not LLMs on knowledge units. The Larsen
orthogonality result used cognitive-process as its second axis, not epistemic status. Each transfer
is a reasonable analogy and none is a demonstrated result — the verifiers flagged this on four of
eight findings.  CORPUS NARROWNESS: the Larsen n=940 finding is 834 items from a single private
doctoral university's biology courses (2011-2015), with marginals hand-adjusted mid-study and 36% of
items single-coded; the authors explicitly decline universal claims. Gluga et al. 2012 had n=10
participants.  UNQUANTIFIED CENTRAL FACT: "poor inter-rater reliability" is well-attested
qualitatively across a systematic review and a failed-remediation replication, but no kappa or alpha
magnitude survived verification. You know the direction, not the size.  TIME-SENSITIVITY:
essentially zero for the cognitive-psych findings (slow-moving; 2019-2024 work reinforces rather
than overturns them). Potentially high for anything about LLM classification reliability,
structured-output conformance on small open-weight models, and typed agent memory — but nothing on
those topics survived, so no stale claim is being carried forward.  PERSISTENCE: per the standing
rule, this full verified set (confirmed + refuted + verifier reasoning) should be written to
/home/anatoly/knowledge-ingestion-plugin/research/ alongside the six existing round files, and
linked from /home/anatoly/knowledge-ingestion-plugin/skills/knowledge-ingestion/SKILL.md so it
ships. I did not write it — this subagent was instructed not to create report files, so the parent
needs to do it.

---

## 5. Open questions

**Q1.**
Does typed knowledge actually improve anything downstream? Nothing survived on whether type-filtered
retrieval beats plain semantic search, whether typing helps contradiction detection, or whether it
helps cross-domain insight generation. This is the load-bearing justification for the entire
taxonomy and it is currently unevidenced in this set — it needs either a dedicated research pass
against the KG-RAG / metadata-filtering / WikiContradict literature, or an internal A/B on your own
corpus.

**Q2.**
What label count can a 7B-14B open-weight model apply consistently, and does a two-tier scheme (3
families as a first pass, 6 types as a second) beat flat 6-way? Every quantitative size-vs-
reliability claim failed verification, so there is no external number to design against. A same-
corpus experiment measuring Krippendorff's alpha across model families at 3 vs 6 labels would settle
it cheaply and would be more decision-relevant than any further literature search.

**Q3.**
Is the status/origin/confidence/maturity axis genuinely independent of the type axis in your corpus?
Larsen et al. is the warning shot: the one published two-axis design that was assumed orthogonal
measured as dependent. Run the same contingency test on a few hundred of your own classified units —
if fact/hypothesis/insight collapses onto Claims and brainstorm collapses onto Cases, the metadata
axis is carrying less information than the design assumes.

**Q4.**
Should the structure be a hierarchy or a facet space? Rubin argues dimensions re-home orphan
phenomena that a hierarchy leaves stranded, which maps to the practical worry: where does a trading
playbook that is simultaneously a Model, a Method, and a Rule actually live? Whether
primary+secondary type is sufficient, or whether independent facets (form × epistemic status ×
domain) would fit real units better, is unresolved — and the specific inference that
primary+secondary+confidence is 'closer to the cognitive data' was explicitly voted down.

---

## 6. Tier 2 — Sourced but not adversarially verified

All 140 extracted claims, minus those promoted into Tier 1, grouped by research angle and source.
`[central]` / `[supporting]` / `[tangential]` is the extractor's own importance rating.

### A1. Cognitive-science foundations — is the declarative / procedural / episodic split real and sharp?

**Case & Swanson 1996/97, Academic Medicine / Advances in Medical Education — *'Fact' is in the eye of the beholder***
<https://link.springer.com/chapter/10.1007/978-94-011-4886-3_40>
*Date/edition note:* 1997 (Springer chapter in Advances in Medical Education, pp. 139-142); originally published 1996 in Academic Medicine 71(10):S31-S33, PMID 8940927

- `[central]` When four trained human raters applied a learning taxonomy (factual recall vs. higher cognitive levels) to real high-stakes multiple-choice test items, inter-rater agreement was only MODERATE — i.e., a small, well-known cognitive taxonomy applied by domain experts to concrete content does not produce reproducible labels. This is direct empirical evidence against the assumption that knowledge-type classification is objective; it sets a ceiling expectation for any LLM applying a 6-type taxonomy.

- `[central]` Taxonomic label assignment was systematically biased by the rater's own expertise level: faculty (more expert) were significantly more likely than recent graduates to classify the same items as 'Factual Recall'. The knowledge-type label therefore encodes the classifier's knowledge state, not an intrinsic property of the content — a direct analogue to different model families (or the same model at different capability levels) disagreeing on Concept vs. Claim vs. Model.

- `[central]` The paper's titular finding is that 'fact' is not a stable intrinsic category but an artifact of the observer — what looks like factual recall to an expert is higher-order reasoning to a novice. This undermines treating 'factual/declarative' as a crisp type boundary in any taxonomy that separates Concepts/Claims from Models/Methods.

- `[supporting]` Taxonomic classification of items had little practical/predictive value: no systematic performance differences related to taxonomic level were found between the two student cohorts (McMaster problem-based vs. conventional curriculum), so the labels bought no downstream utility despite the classification effort.

- `[supporting]` The study is empirical, on real operational content: items from the 1993 and 1994 Medical Council of Canada multiple-choice examinations were classified by two recent graduates and two faculty members. Note: the full text is PAYWALLED — only the abstract and metadata are publicly visible, so no kappa/alpha coefficient is available to quantify what 'moderate agreement' means numerically.

**Renoult, Irish, Moscovitch & Rugg 2019, Trends in Cognitive Sciences 23(12) — *From Knowing to Remembering***
<https://neuropsychologylab.psych.utoronto.ca/files/FromKnowingtoRememberingTheSemanticEpisodicDistinction.pdf>
*Date/edition note:* 2019-12 (Trends in Cognitive Sciences Vol. 23, No. 12, pp. 1041-1057; doi 10.1016/j.tics.2019.09.008; available online October 2019)

- `[central]` Renoult et al. conclude that the episodic/semantic boundary is not sharp: after reviewing behavioral, neuropsychological and neuroimaging evidence they state the boundaries are less distinct than Tulving's original proposal implied, whether defined anatomically or functionally. This directly undercuts treating Declarative vs Episodic as crisply separable categories in a knowledge-type taxonomy.

- `[supporting]` Knowledge units migrate between types over time: through 'semanticization or schematization' via repeated re-encoding, episodic memories lose their contextual specificity and become personal facts — i.e., the episodic-to-declarative transition is a documented process, not an edge case. A wiki taxonomy therefore needs re-classification over time (a Case becoming a Claim/Concept) rather than a one-time label.

- `[supporting]` Real recall units are mixtures rather than pure types: content analysis of autobiographical narratives finds a blend spanning well-defined episodes through to decontextualized semantics, which the authors say supports continuum-based accounts of 'personal semantics' — a documented hybrid category sitting between the episodic and semantic poles.

**Rubin 2021/22, Memory & Cognition 50(3) — *A conceptual space for episodic and semantic memory***
<https://sites.duke.edu/rubinlab/files/2021/08/2021-online-ConceptualSpace-Dimension-M-C.pdf>
*Date/edition note:* Accepted 28 January 2021; published online 2021 by The Psychonomic Society / Springer in Memory & Cognition (issue 50(3), 2022). DOI 10.3758/s13421-021-01148-3.

- `[central]` Rubin states outright that there is no convincing evidence the three dimensions underlying the episodic/semantic distinction (explicit-implicit, self-reference, scene) can be reduced to discrete categories — the categories exist for communicative convenience, not because the data support sharp boundaries. Directly answers the research question's 'are the boundaries sharp?': per Rubin, no; individual memories vary continuously along each dimension at both behavioral and neural levels. This is an argued position over existing literature, not a new measurement.

- `[central]` The explicit/implicit (i.e. declarative vs. procedural/nondeclarative) split — the exact boundary a Declarative-vs-Procedural knowledge taxonomy leans on — is the WEAKEST of Rubin's three dimensions: he judges that it lacks a plausible neural basis (unlike self-reference and scene), and cites Dew & Cabeza's (2011) review concluding the constructs used to distinguish explicit from implicit memory have not produced data consistent with a dichotomy.

- `[central]` Rubin's core structural argument is that a HIERARCHY of memory types (Tulving/Squire) only classifies what has already been observed and leaves well-documented phenomena homeless, whereas a small set of orthogonal DIMENSIONS crossed into a factorial space (3 binary dimensions → 8 cells) both organizes the existing literature and predicts unoccupied cells — explicitly analogized to the periodic table. He names four concrete phenomena that fall outside the standard taxonomy: personal/self-reference semantic memory, non-self-reference episodic memories, implicit self-reference memory (habits, personality), and implicit-scene memory (déjà vu).

- `[supporting]` Rubin's model deliberately deconstructs 'episodic memory' from a top-level type into a conjunction of three orthogonal attribute values (explicit + self-referential + scene-based), with Tulving's remaining criteria (autonoetic reliving, voluntary retrieval, single occurrence) treated as ADDITIONAL restrictions layered on top rather than as defining the type — i.e. the properties usually bundled into a type label are better modeled as separable metadata facets.

**Squire & Zola 1996, PNAS 93(24) — *Structure and function of declarative and nondeclarative memory systems***
<https://www.pnas.org/doi/10.1073/pnas.93.24.13515>
*Date/edition note:* 1996-11-26

- `[central]` In Squire's canonical taxonomy, 'facts' and 'events' (the content analogues of semantic and episodic memory) are NOT separate top-level systems — they are sibling subcategories inside a single Declarative system that depends on the same brain substrate (medial temporal lobe / diencephalon). The paper does not use the terms 'episodic' or 'semantic' at all. This directly contradicts the proposal's treatment of Declarative and Episodic as two of three co-equal cognitive families.

- `[central]` The boundaries in this taxonomy are justified by neural dissociation evidence — amnesic patients with bilateral medial temporal or midline diencephalic damage showing impaired declarative memory alongside intact nondeclarative learning — not by intuitive content categories. No equivalent dissociation criterion exists for classifying text on a wiki page, so borrowing the taxonomy's labels does not import its empirical warrant.

- `[supporting]` 'Nondeclarative' — the category containing procedural memory — is explicitly characterized as a grab-bag of dissimilar capacities rather than a single coherent kind, and by 1996 was still being extended to newly studied tasks (classification learning, artificial grammar learning, prototype abstraction). A knowledge taxonomy that treats 'Procedural' as one clean family is smoothing over heterogeneity the source literature deliberately flags.

- `[supporting]` The functional property separating the two systems is accessibility/flexibility: declarative content can be used by multiple downstream response systems, while nondeclarative content is encapsulated and largely usable only by the system that learned it. This is a claim about retrieval reach, which is the one part of the cognitive distinction that plausibly transfers to a retrieval-oriented wiki design.

**Canadian Journal of Learning and Technology 34(2), 2008 — metacognition frameworks / conditional knowledge**
<https://files.eric.ed.gov/fulltext/EJ1073838.pdf>
*Date/edition note:* Spring 2008 (Canadian Journal of Learning and Technology, v34 n2; ERIC EJ1073838)

- `[supporting]` When human coders applied an abstract knowledge-category scheme to real text, the category almost never fired: Gunawardena, Lowe & Anderson (1997) coded only 4 of 206 online-debate postings into the metacognitive category, and reported difficulty telling metacognitive statements apart from others. Abstract cognitive categories can produce near-zero, unreliable hit rates on naturalistic text.

- `[supporting]` Multiple independent research teams found Henri's (1992) metacognitive-knowledge category unusable in practice — scored with poor inter-rater reliability by McKenzie & Murphy (2000), abandoned outright by Hara (2000) for lacking objective criteria, and called 'extremely difficult to reliably score' by Hara, Bonk & Angeli (2000). Category definitions without operational criteria and examples measurably fail at the annotation step.

- `[supporting]` Murphy's own proposed framework reports NO empirical validation — no inter-rater agreement, no kappa, no coding study. The paper is a conceptual synthesis whose indicators and prompts are offered as untested starting points that the author says still need validity testing. Any citation of this paper as evidence that declarative/procedural/conditional works in practice would be unsupported.


### A2. Reliability of applying small cognitive taxonomies to text (education-assessment evidence)

**Karpen & Welch 2016, Currents in Pharmacy Teaching and Learning — faculty IRR on Bloom's**
<https://www.sciencedirect.com/science/article/abs/pii/S1877129715301921>
*Date/edition note:* 2016-11-01

- `[supporting]` The optimal three-tier grouping was derived empirically from observed misclassification patterns rather than chosen a priori (Knowledge; Comprehension/Application; Analysis/Synthesis/Evaluation), supporting a method of merging exactly those category boundaries that raters actually confuse.

- `[supporting]` The evidence base is thin: the study used only six example exam questions rated by faculty at a single college of pharmacy, so the 0.25 / 46.0% / 81.8% figures are a small-sample, single-institution result, not a robust generalizable effect size.

- `[tangential]` The taxonomy tested is the ORIGINAL Bloom cognitive-process hierarchy (Knowledge/Comprehension/Application/Analysis/Synthesis/Evaluation), not the revised Bloom knowledge dimension (Factual/Conceptual/Procedural/Metacognitive); so it bears on how reliably raters apply a 6-label abstract taxonomy in general, and only by analogy on knowledge-TYPE labeling.

**Larsen, Endo, Yee, Do & Lo 2022, CBE—Life Sciences Education 21(4) — RBT two-dimension contingency analysis (n=940)**
<https://www.lifescied.org/doi/10.1187/cbe.20-08-0170>
*Date/edition note:* 2022-12 (CBE—Life Sciences Education 21(4):ar66; DOI 10.1187/cbe.20-08-0170). Note: the search lead labeled this 2021, but the published issue is Winter 2022.

- `[central]` The two dimensions RBT assumes are independent — knowledge type and cognitive process — are in fact statistically dependent (Fisher's exact test, p < 0.0001), with items collapsing into a few dominant type×process clusters (Factual+Remember 28%, Conceptual+Understand/Analyze/Evaluate/Create 23%, Procedural+Apply). Claims that a knowledge-type axis is orthogonal to a status/confidence/maturity axis are therefore testable, and in the closest published precedent the orthogonality assumption failed.

- `[supporting]` Surface lexical cues do not determine the category: 57% of items led with question words rather than action verbs, and the five most common prompt words (which, what, describe, how, explain) had Shannon evenness J′ of 0.58–0.85 — i.e. each word spread near-uniformly across cognitive processes. Question-phrase glosses like "what is it?" / "what can we do?" are mnemonics for humans, not classification signals; keyword or verb heuristics cannot substitute for semantic judgment of the unit.

- `[supporting]` The reported κ figures rest on a partial double-coded subset: only 17% of the 940 items were coded by all three researchers and 36% were coded by a single researcher, so the agreement statistic characterizes 64% of the corpus at best and cannot be read as reliability over the whole data set. Any agreement number quoted from this study should be treated as an optimistic partial estimate.

**Zhang, Wong, Giacaman & Luxton-Reilly 2021, ACE '21 — automated Bloom classification**
<https://dl.acm.org/doi/10.1145/3441636.3442305>
*Date/edition note:* 2021-02-02 (ACE '21, 23rd Australasian Computing Education Conference, Feb 2-4 2021)

- `[central]` The paper's own framing states as established fact that Bloom's taxonomy classification in computing education suffers from poor inter-rater reliability, i.e. the reliability problem is a property of the taxonomy-application task itself, not of one bad rater pool.

- `[supporting]` Classification performance was strongly gated by class imbalance in the labeled data — the model performed best only when each category had a roughly even number of examples. Rare categories (4 Evaluation, 17 Application, 20 Synthesis items) were learned poorly, implying a knowledge-type taxonomy whose types occur at very unequal frequency will be applied unreliably on its rare types.

**arXiv 2511.10903 (Nov 2025) — LLM zero-shot Bloom-level classification across model families**
<https://arxiv.org/html/2511.10903>
*Date/edition note:* 2025-11-14

- `[central]` The same six-label prompt produced large cross-family spread: Claude 3.5 Haiku scored 0.58 accuracy / 0.51 macro-F1 and open-weight LLaMA 3.1 via Ollama scored 0.42 accuracy / 0.35 macro-F1 — a ~31-point accuracy gap between the best and worst model on identical inputs, with the smaller/open-weight models described as more prompt-sensitive.

- `[central]` Classification errors concentrated at adjacent categories in the taxonomy, not randomly — the authors attribute this to genuinely subtle boundaries between neighboring labels rather than to model weakness, implying that taxonomies whose categories sit on a continuum are inherently harder to apply consistently than ones with disjoint definitions.

- `[supporting]` A small supervised classifier (SVM with synonym-replacement/embedding augmentation) trained on the same 600 labeled sentences reached 94% accuracy — roughly 21 points above the best zero-shot LLM — indicating that for a fixed small label set, a few hundred human-labeled exemplars beat prompt-only LLM typing by a wide margin.

- `[supporting]` EVIDENCE GAP: despite being surfaced by a 'knowledge dimensions' search, this study covers only Bloom's cognitive-process dimension (Knowledge/Comprehension/Application/Analysis/Synthesis/Evaluation) and never tests the revised taxonomy's knowledge dimension (Factual/Conceptual/Procedural/Metacognitive); it also reports no inter-rater reliability statistic (no kappa or alpha) for the human labels it treats as ground truth, and rests on a single small dataset.

**Coleman 2017, Cambridge Assessment *Research Matters* 24 — *On the reliability of applying educational taxonomies***
<https://www.cambridgeassessment.org.uk/Images/426171-on-the-reliability-of-applying-educational-taxonomies.pdf>
*Date/edition note:* Autumn 2017 — Research Matters, Issue 24, Cambridge Assessment (PDF re-hosted 2020). NOTE: the cited attribution "Voleman (2020)" is wrong; the author is Victoria Coleman, Research Division, Cambridge Assessment, 2017.

- `[supporting]` Keyword/verb-list heuristics for assigning items to taxonomy levels are unreliable because raters map the same cue word to different levels; the review's recommended remedies are consensus discussion, practice on sample material, and per-level worked examples/rubrics rather than definitions alone.

- `[supporting]` Reliability results cannot be transferred from one taxonomy to another: 17 of the 21 reviewed studies used Bloom's or adaptations of it, and the review explicitly states there is insufficient evidence to support or refute the hypothesis that other taxonomies achieve high reliability given training and materials. Any new label set must have its own agreement measured.


### A3. Information-typing prior art — DITA, Information Mapping, Diátaxis

**Jansen et al. 2002 IPCC / Document Design 4(1) 2003 — controlled reader experiments on Information Mapping**
<https://ieeexplore.ieee.org/document/1049113/>
*Date/edition note:* 2002 (IEEE International Professional Communication Conference proceedings, pp. 307-318; DOI 10.1109/IPCC.2002.1049113; OpenAlex indexes publication year as 2003; journal version published as Document Design 4(1):48-59, January 2003)

- `[central]` Two controlled reader experiments (n=65 and n=76) testing texts rewritten according to the Information Mapping method (Horn's six information types: concept, procedure, process, principle, fact, structure) against non-IMAP versions found essentially no measurable benefit. NOTE ON ATTRIBUTION: Crossref, OpenAlex and Semantic Scholar all list the author as Carel Jansen, not Karreman & Steehouder; the journal version is Jansen, Korzilius, Le Pair & Roest, Document Design 4(1):48-59, 2003.

- `[central]` In study 1 (65 plant operators, chemical-process text), imposing the Information Mapping type/structure scheme produced zero effect on reader task performance on either accuracy or speed — the two measures that would justify the typing overhead.

- `[central]` The only advantage IMAP showed was subjective: readers rated the IMAP version higher than one alternative on overall judgment while performing no better — i.e. typed/structured presentation felt superior without being superior, a perceived-quality effect that would mislead anyone evaluating a taxonomy by user preference rather than task outcome.

- `[supporting]` The IMAP version was benchmarked not only against the untouched original but against a version rewritten by a skilled writer who did not use the method, and the formal typing method did not beat ordinary competent rewriting.

- `[supporting]` In study 2 (76 subjects, half immigrants, machine-operating instructions) reader attributes — origin and education level — dominated performance while text format did not, and IMAP gave no measurable help to readers reading in a non-native language; the variance sat in the audience, not the information typing.

**Information Mapping (vendor blog) — *The DITA topic types: square pegs and round holes***
<https://informationmapping.com/blogs/news/the-dita-topic-types-square-pegs-and-round-holes>
*Date/edition note:* unknown (no date or byline present on the page)

- `[central]` Information Mapping's Theory of Information Types defines exactly six information types — Process (what happens, who does what), Procedure (step-by-step work instructions), Principle (policies, rules, guidelines), Concept (ideas, definitions, abstractions), Structure (parts, functions, components), and Fact (statements, specifications) — offered as a general-purpose typing scheme for business content. This is direct prior art for a small, ~6-slot knowledge-type taxonomy and maps closely onto the proposed Concepts/Claims/Models/Methods/Rules/Cases set (Concept≈Concepts, Procedure≈Methods, Principle≈Rules, Structure≈Models, Fact≈Claims), with Process as an extra type and no episodic/Cases type.

- `[central]` A three-category typing scheme with a residual catch-all (DITA's concept/task/reference) is criticized on the grounds that the residual bucket becomes too internally diverse to be useful — the argument being attributed to Mark Baker's "Everything Else Is Not a Concept" (Every Page Is Page One), using the analogy of splitting the animal kingdom into cats, dogs, and everything else. This is an argument that taxonomies can be too SMALL, not only too large.

- `[supporting]` DITA's topic triad is a single-source publishing/authoring technology that is commonly — and, per this source, incorrectly — treated as an information design methodology; the confusion, not the types themselves, is what causes problems for content developers and managers.

- `[supporting]` The only evidence offered for the six-type scheme is an unquantified appeal to commercial track record — 40+ years of application to "millions of pages" — with no study, inter-rater reliability data, or citation. Falsifiable in the sense that no supporting research is presented anywhere in the piece; this marks the six-type taxonomy as practitioner convention rather than an empirically validated construct.

- `[tangential]` The source's own stated position is that DITA's topic types are not defective but are misused, that misalignment comes from forcing content into rigid categories, and that user purpose (not document genre) should drive structure — an argument that typing schemes should key on the reader's question rather than the artifact's form.

**Horn 1998 — *Structured Writing as a Paradigm* (the Information Mapping method, primary source)**
<https://faculty.washington.edu/farkas/TC510-Fall2011/Horn-StructuredWritingParadigm.pdf>
*Date/edition note:* 1998

- `[central]` Horn's Information Mapping taxonomy for the "relatively stable subject matter" domain is exactly SEVEN information types — Procedure, Process, Concept, Structure, Classification, Principle, Fact — asserted (not empirically derived in this chapter) to be a general account of how people think about stable subject matter. This is the closest prior art to the proposed six-type set (Concepts/Claims/Models/Methods/Rules/Cases): Horn's Concept≈Concepts, Procedure≈Methods, Principle≈Rules, Structure+Process≈Models; he has no Claims or Cases type, and instead has Classification and Fact. Origin of the seven: inspection of textbook/manual sentences (Horn 1965), i.e. corpus intuition, not a cognitive-science result.

- `[central]` The seven types are explicitly DOMAIN-SCOPED, not universal: Horn defines a "domain of discourse" by shared author-reader assumptions and stance, and reports that extending the method to other domains required NEW type sets rather than reuse — the 1977 memo/report extension identified fifteen basic report/memo types, and "disputed discourse" (contested knowledge) is a separate domain from stable subject matter. This is direct prior-art evidence AGAINST one small type set spanning finance/trading, onboarding, software design, factual reference, brainstorming, and cross-domain analysis; the practitioner who tried it hardest concluded the label set changes when the author-reader stance changes.

- `[central]` The taxonomy is deliberately two-level and deliberately INCOMPLETE: ~40 fine-grained block types sit under the 7 coarse information types, and Horn states the 40 cover only about 80% of the stable-subject-matter domain, with the remaining 20% handled by giving writers criteria to invent new block types rather than by enumerating more labels. His stated reason is that the residual types are idiosyncratic to particular subject matters, so enumerating them is not cost-effective. This is a falsifiable design precedent for taxonomy sizing: a small closed set plus an explicit escape hatch, not exhaustive coverage.

- `[supporting]` The empirical base Horn cites is about LEARNING OUTCOMES, not retrieval, and contains NO inter-rater reliability evidence for applying the type labels. Of ten studies summarized in Horn 1992b, seven measured learning (mostly test scores vs "conventional" materials) and only two measured retrieval time; reviewer Ruth Clark (1993) explicitly flagged the gap. The one organizational study cited (Holding 1985, 180 managers at Pacific Telephone) reports a mean 32% decrease in reading time and 83% faster approval — but these are supervisor self-reports from interviews, not instrumented measurement. Nowhere in the chapter is agreement between writers/raters on assigning a block to a type measured or even discussed — a direct absence-of-evidence flag for any claim that a fixed type set is applied consistently by independent annotators (human or model).

- `[supporting]` The classification unit is sub-page and single-purpose by rule — the "information block" replaces the paragraph, is usually ≤ 7±2 (max nine) sentences, must carry a label chosen by systematic criteria, and by the relevance principle may contain only information serving one main point. Its cognitive grounding was later downgraded by Horn himself: he says he originally took Miller (1956) 7±2 literally but subsequent chunking research means it must now be used "on a more metaphorical basis" — i.e. the size rule is heuristic, not a validated cognitive limit.

**Procida, *Diátaxis* — the compass / decision procedure**
<https://diataxis.fr/compass/>
*Date/edition note:* Not stated on page (undated; site carries only \"Copyright © Daniele Procida\", served from ReadTheDocs \"latest\" version — continuously updated. Diátaxis framework itself dates to ~2017.)

- `[central]` Diátaxis — the framework that explicitly positions itself against DITA-style information typing — reduces classification of any documentation unit to exactly two binary questions over orthogonal axes (action/cognition × acquisition/application), producing a 4-cell truth table rather than a flat menu of labels. This is a design assertion by the framework's author; no reliability data is offered on the page.

- `[central]` The framework's own author concedes that trained human authors frequently cannot classify content intuitively even under a 4-type scheme, and that intuition sometimes returns a confidently wrong answer — i.e. a small, well-known information-type taxonomy is NOT self-evidently applicable in practice, which is why a forced decision procedure was added on top of the type map. Asserted from practice; not measured, no inter-rater data.

- `[supporting]` Diátaxis's primary classificatory axis is an explicit procedural-vs-declarative split, glossed by the author as doing versus "theoretical or propositional knowledge" — convergent precedent for the proposal's Declarative/Procedural family boundary, arrived at independently from documentation practice rather than borrowed from Tulving/Anderson. Note the second axis (acquisition vs. application of skill) is about USER NEED, not knowledge kind, and has no analogue in the proposed six-type scheme.

- `[supporting]` Diátaxis explicitly prescribes classification at sub-document granularity, down to the sentence and word level, using the same questions applied at document level — established precedent that an information-type scheme can be applied at "knowledge unit" rather than page granularity.

- `[supporting]` Diátaxis instructs practitioners to hold the label names loosely and interpret the type vocabulary flexibly — treating the underlying distinctions as load-bearing and the names as disposable. This is in direct tension with what the LLM-annotator literature requires for high inter-rater agreement (rigid definitions, boundary cases, negative examples), so it is precedent for the axes but counter-precedent for the label-definition style a cross-model classifier needs.

**Baker 2012, Every Page Is Page One — *The tyranny of the terrible troika***
<https://everypageispageone.com/2012/07/28/the-tyranny-of-the-terrible-troika-rethinking-concept-task-and-reference/>
*Date/edition note:* 2012-07-28

- `[central]` In practice, the three DITA information types degenerated from knowledge/behavior categories into presentation formats: practitioners classify by output shape (table = reference, numbered steps = task, prose = concept) rather than by kind of knowledge — a documented failure mode for any small generic type set.

- `[central]` A taxonomy that only specifies how to break content into typed pieces is incomplete as an information-design theory; it must also specify how typed pieces reassemble into a coherent whole, or it yields incoherent fragment collections ("Frankenbooks").

- `[supporting]` DITA's concept/task/reference is a historical reduction of Information Mapping's six information-block types (Principle, Process, Procedure, Concept, Fact, Structure) — i.e., the field moved from six types to three, and Baker judges the collapse a loss.

- `[supporting]` A three-type vocabulary is too small to express the range of content structures authors need; expressive capacity is limited by the number of available types.

- `[tangential]` The correct unit of typed knowledge is defined by the reader's need at the moment of retrieval, not by document or page boundaries — an argument for sub-page, purpose-complete knowledge units.


### A4. Typed memory for LLM agents — does typing measurably help?

**Sumers, Yao, Narasimhan & Griffiths 2023/24, TMLR — *CoALA: Cognitive Architectures for Language Agents***
<https://arxiv.org/abs/2309.02427>
*Date/edition note:* 2023-09-05 (arXiv v1); v2 2023-09-27; v3 2024-03-15; published in TMLR 2024

- `[central]` CoALA proposes exactly the tripartite long-term memory typing under evaluation — episodic, semantic, procedural — plus a short-term working memory, as the organizing structure for LLM agents. This is direct prior-art support that a cognitive-memory-family split (declarative/semantic, procedural, episodic) is a coherent typing scheme for LLM-maintained knowledge, and it is the scheme a major cognitive-architecture paper chose independently of any wiki use case.

- `[central]` CoALA provides NO empirical measurement that typed memory improves agent performance. It is explicitly a theoretical framework validated by retrospective organization of other people's empirical work — so it cannot be cited as evidence that episodic/semantic/procedural typing produces measured gains over flat memory.

- `[supporting]` In CoALA's survey (Table 2), most surveyed language agents implement only ONE long-term memory type, not all three — SayCan and ReAct have procedural memory only and lack semantic and episodic memory; Voyager has procedural only; Generative Agents is among the few with episodic plus semantic. So as of 2024 the full three-way typing was aspirational rather than standard practice.

- `[supporting]` CoALA asserts an asymmetry in write risk across memory types: writing to procedural memory is significantly riskier than writing to episodic or semantic memory. This bears directly on a wiki design where an LLM maintains typed units — Methods/Rules (procedural-family) writes warrant stricter gating than Concepts/Claims/Cases writes. Note this is asserted, not measured.

- `[supporting]` CoALA identifies type-aware / context-sensitive retrieval from typed memory as an open, understudied problem rather than a solved or demonstrated win — meaning the claim that type-filtered retrieval beats flat semantic search is not established by this source.

**A-MEM: Agentic Memory for LLM Agents (NeurIPS 2025)**
<https://arxiv.org/abs/2502.12110>
*Date/edition note:* 2025-02-17 (arXiv v1; last revised 2025-10-08, v11; published at NeurIPS 2025)

- `[central]` The measured gain in A-MEM comes from the structural machinery (link generation + memory evolution), not merely from storing notes: ablating both modules drops Multi-Hop F1 from 27.02 to 9.65 on LoCoMo with GPT-4o-mini (link generation alone recovers to 21.35). This is direct evidence that imposing structure/relations over stored knowledge units measurably improves multi-hop retrieval versus flat storage.

- `[central]` A-MEM's per-unit metadata schema is fixed in SHAPE but open in VOCABULARY: every memory note carries contextual description, keywords, and tags, all LLM-generated at write time rather than drawn from a predefined type taxonomy. The paper therefore provides no evidence for a fixed closed label set; it is evidence for structured attributes with emergent labels.

- `[central]` Structured/linked memory does not uniformly beat flat baselines — the benefit is question-type dependent. On GPT models, flat baselines (LoCoMo, MemGPT) beat A-MEM on Open Domain and Adversarial categories (e.g., Adversarial F1 69.23 for LoCoMo vs 50.03 for A-MEM), while A-MEM wins on Multi-Hop and Temporal (+149% on Temporal).

- `[supporting]` Small open-weight models (Qwen2.5 1.5B/3B, Llama 3.2 1B/3B) benefited from the structured-note pipeline more consistently than GPT models did — A-MEM beat every baseline in every category on the non-GPT models, suggesting LLM-generated structured attributes are applicable by sub-4B models and that structure compensates for weaker parametric knowledge.

- `[supporting]` Writing structured notes with attributes and links is cheaper at inference time than flat long-context baselines: A-MEM used ~1,200-2,500 tokens per memory operation versus ~16,900 for LoCoMo/MemGPT, an 85-93% token reduction.

**Zep / Graphiti — temporal knowledge-graph agent memory (Jan 2025)**
<https://arxiv.org/abs/2501.13956>
*Date/edition note:* 2025-01-20 (arXiv v1; announced 2025-01-23)

- `[central]` Zep's memory hierarchy is explicitly modeled on the cognitive episodic/semantic distinction: it stores raw episodes and derived semantic entities as separate subgraph tiers, and the authors justify this by appeal to psychological memory models — evidence that the declarative/episodic split is being carried into production agent-memory architectures, not just cognitive-architecture papers.

- `[central]` Structured, typed graph memory measurably beat flat full-context retrieval on LongMemEval: up to 18.5% accuracy improvement while cutting latency ~90% (28.9s -> 2.58s for gpt-4o) and shrinking average context from ~115k tokens to ~1.6k tokens. This is a concrete measured gain of typed/structured memory over undifferentiated chunk stuffing.

- `[central]` The accuracy gains from structured memory are concentrated in cross-session and temporal question types rather than uniform: multi-session 44.3% -> 57.9%, temporal-reasoning 45.1% -> 62.4%, but knowledge-update only 78.2% -> 83.3%. Typing/structuring pays off specifically where information must be synthesized across many separate records — the same regime a multi-page LLM wiki operates in.

- `[supporting]` Structured typed memory is NOT uniformly better — it regressed on one question category, with single-session-assistant accuracy dropping 17.7% for gpt-4o versus the full-context baseline. This is direct counter-evidence that extraction into a typed structure can lose information present in the raw text.

- `[supporting]` Zep handles contradictions by bi-temporal edge invalidation — tracking valid-time and transaction-time separately and marking a fact invalid rather than deleting it — which operationalizes the design principle that truth-status/validity is time-scoped metadata attached to a knowledge unit, distinct from the unit's type.

**Mem0 (Apr 2025) — scalable long-term agent memory, incl. Mem0-graph variant**
<https://arxiv.org/abs/2504.19413>
*Date/edition note:* 2025-04-28

- `[central]` Adding a typed/structured (entity+relation graph) memory layer on top of untyped natural-language memory produced only ~2% overall improvement on the LOCOMO benchmark (Mem0 base 66.88% ± 0.15 vs Mem0-graph 68.44% ± 0.17 LLM-as-a-Judge). This is direct measured evidence that imposing structure/typing on agent memory yields small, not transformative, end-task gains.

- `[central]` Typed graph memory HURT performance on two of four question categories: single-hop J-score fell 67.13 -> 65.71 and multi-hop fell 51.15 -> 47.19 (F1 28.64 -> 24.32) versus flat memory. Structure is not uniformly beneficial and can degrade retrieval on both simple lookups and multi-hop composition.

- `[supporting]` The gain from typed graph memory was concentrated in temporal and open-domain questions — temporal F1 48.93 -> 51.55 and J 55.51 -> 58.13; open-domain J 72.93 -> 75.71. If typing helps, it helps on relational/time-grounded queries, not on lookup or chained reasoning.

- `[supporting]` The structured/typed variant roughly doubled stored memory tokens (~7k -> ~14k per conversation) and roughly tripled search latency (p95 0.200s -> 0.657s; total p95 1.440s -> 2.590s). The ~2% accuracy gain from typing carries a measurable 2x storage and ~3x retrieval-latency cost.

- `[supporting]` Mem0's production baseline memory carries NO knowledge-type taxonomy: memories are stored as salient natural-language text managed by four LLM function-calling operations (ADD, UPDATE, DELETE, NOOP), with typing (entity type classification + relationship triplets) present only in the optional graph variant. A shipped production memory system deliberately made typing optional rather than foundational.

**EMem (Nov 2025) — event-proposition structured conversational memory**
<https://arxiv.org/abs/2511.17208>
*Date/edition note:* 2025-11-21 (v1); v2 2025-12-11

- `[central]` Structuring conversational history into small typed units (event-like propositions organized in a heterogeneous graph of sessions, EDUs, and argument nodes) outperforms both flat-chunk RAG and full-context baselines on two long-term memory benchmarks: on LoCoMo with gpt-4o-mini, EMem scored 0.780 LLM-judge vs 0.723 full-context, 0.613 Mem0, 0.585 Zep, 0.513 LangMem, 0.302 plain RAG; on LongMemEval_S, 76.0-77.9% vs 55.0% full-context and 64.2% Nemori. This is measured, not asserted.

- `[central]` Decomposing knowledge too finely is a documented failure mode: relation-triple representations fragment the source discourse so that retrieval must locate and recombine several units to answer one question. The authors chose a coarser unit (a self-contained event proposition bundling participants, time, and local context) specifically to avoid this. This is an argued design rationale supported by the benchmark win, not an isolated ablation of granularity.

- `[central]` The paper frames the entire design space as a granularity tradeoff — coarse chunks retrieve imprecisely, fine-grained units fragment meaning — implying the choice of 'knowledge unit' size, not the label set, is the primary lever for memory quality.

- `[supporting]` Adding graph-propagation machinery on top of the typed units bought almost nothing: EMem-G tied EMem on LoCoMo (0.780 vs 0.780) and gained only ~1.9 points on LongMemEval_S (77.9% vs 76.0%), while costing more context tokens. Structural elaboration beyond the basic unit typing showed diminishing returns.

- `[supporting]` Typed/structured memory cut retrieval context by roughly 30x on LoCoMo (average 738.2 tokens vs a 23,653-token full-context baseline) and ~40-100x on LongMemEval_S (0.6K-3.6K vs 101K) while raising accuracy, so structuring is a cost win as well as a quality win.


### A5. Cross-model classification reliability and structured-output conformance

**arXiv 2601.12099 (Jan 2026) — 7 LLMs x 121 features x 567 excerpts, LLM-LLM vs human-human agreement**
<https://arxiv.org/pdf/2601.12099>
*Date/edition note:* 2026-01-17 (arXiv v1; PDF stamped 2026-01-21)

- `[central]` Different LLMs applied the SAME fixed codebook far less consistently with each other than human coders did with each other: mean LLM-LLM Cohen's kappa = 0.23 versus human-human kappa = 0.57 (7 models, 121 features, 567 excerpts). The authors explicitly conclude this cross-model divergence limits the value of simple ensembling. This is direct evidence against the assumption that many model families will apply a fixed knowledge-type label set consistently.

- `[central]` Multi-class labels (choose one of several ordinal/categorical options) were dramatically harder than binary present/absent judgments: multiclass features had 90% lower odds of correct detection than binary features (OR = 0.10, 95% CI 0.03-0.35), and feature type was the dominant task-level predictor, raising marginal R-squared from 3.8% to 22.5%. This bears directly on a six-way single-choice primary-type decision versus a set of independent binary tests.

- `[central]` Label ABSTRACTNESS, not label count alone, drove failure: concrete, explicitly-described features scored F1 > 0.60 for the best models, while features requiring interpretive inference scored F1 < 0.30; and LLM performance tracked human inter-coder reliability at r = 0.61, so categories humans find hard to agree on are also hard for LLMs. Implication: knowledge-type definitions must be surface-recognizable, not judgment calls.

- `[central]` Small open-weight models (Llama 3.2 Instruct 3B, Qwen3 Instruct 4B) were the worst performers (F1 < 0.25), over-predicted presence to the point of a false-positive rate above 98%, and Llama frequently emitted invalid outputs that did not comply with the multi-task instruction format. Frontier/large models (DeepSeek V3.1, GPT-OSS 120B, Claude Sonnet 4.5, GPT-5 Nano) clustered at F1 0.37-0.41 — better, but still far below usable.

- `[supporting]` Self-consistency voting bought almost nothing (mode of 10 repetitions added only 0.01-0.02 F1 over single-pass multi-task prompting), but ensemble agreement was a usable — if weak — confidence signal: annotations with 91-100% run agreement were 81% accurate versus 68% at 10-50% agreement (r = 0.12 over 214,529 predictions), with the signal strongest in large models (GPT-OSS 120B r = 0.36) and entirely absent in Llama 3.2 (r = -0.01). Self-reported/derived confidence from small models is therefore uninformative.

**arXiv 2605.06940 (May 2026) — closed-set label instructions and fallback-label dominance**
<https://arxiv.org/pdf/2605.06940>
*Date/edition note:* 2026-05-07

- `[central]` High inter-model agreement on a fixed closed label set can be an artifact of fallback-label dominance rather than real semantic agreement: on sarcasm, four frontier LLM annotators (ChatGPT, Gemini, Claude, Grok) reached near-total surface agreement while Fleiss' Kappa was approximately -0.001, i.e. no better than chance. Directly falsifiable measurement, not assertion — the kappa is computed on a shared 20% validation set against a human-calibrated 500-item gold set.

- `[central]` Instructing a model what to do when it is uncertain ("assign Other for unclear categories; assign Neutral for unclear sentiments; assign No for unknown cases") measurably biases the output distribution toward that escape-hatch label. The bias is caused by the instruction wording itself, not by the underlying content — a direct hazard for any taxonomy that ships an 'Other', low-confidence, or default-type rule.

- `[central]` Cross-family consistency is not evidence of correct classification. Closed-set label instructions produced a common labeling regime across four architecturally unrelated frontier models, suppressing the model-to-model variability that would otherwise expose the error — so 'all model families agree on the label' cannot be used as a validation signal for a taxonomy.

- `[supporting]` The magnitude of collapse on inference-heavy label dimensions is large: measured against a human-calibrated reference, LLM annotators missed 79% of hateful instances and 75% of sarcastic instances, assigning the fallback 'No' instead. Measured on a 500-item human gold set within a 58K+ comment Bengali social-media corpus.

- `[supporting]` Agreement tracked the abstractness of the label dimension, not the number of labels: 3-class sentiment scored Fleiss kappa ~0.5553, 8-class category ~0.4091, binary hate speech <0.3868, and binary sarcasm ~-0.0011. The two binary (smallest) label sets performed worst, which contradicts the assumption that shrinking a taxonomy reliably improves cross-model agreement — what mattered was whether the label required inference about intent rather than surface identification.

**arXiv 2412.14737 (Dec 2024, rev. May 2026) — verbalized-confidence reliability, 17 prompt methods x 10 datasets**
<https://arxiv.org/pdf/2412.14737>
*Date/edition note:* 2024-12-19 (arXiv v1; v2 dated 2026-05-05)

- `[supporting]` Verbalized (self-reported) confidence from LLMs is not a stable model property: across a benchmark of 17 prompt methods x 10 closed-book QA datasets x models from 2B to 110B (Gemma 1.1, Llama 3, Qwen 1.5, GPT family), reliability of the confidence score depends primarily on how the model is asked, though some prompt methods do yield well-calibrated scores.

- `[supporting]` The smallest evaluated open-weight model (gemma1.1-2b) produced confidence scores that were not merely miscalibrated but carried essentially no signal about correctness — i.e. self-reported confidence from very small models is uninformative, not just biased.

- `[supporting]` The prompt method that maximizes confidence reliability does not transfer across model scale: for 7-8B models a simple 'probscore' formulation helped most, while 70B+ models gained more from few-shot prompting or ranking multiple guesses (few-shot degraded the small models).

- `[tangential]` With the best-performing composite prompt ('combo'), large LLMs achieved verbalized confidence within roughly 7 percentage points of empirical accuracy on average — so calibrated self-reported confidence is attainable at frontier scale under a tuned prompt.

- `[supporting]` Overconfidence is systematic across model sizes: confidence stays high even as task accuracy falls, and observed improvements with scale come mostly from higher accuracy rather than from better-calibrated confidence.

**arXiv 2605.02363 (May 2026) — structured-output conformance in 7–9B open-weight models**
<https://arxiv.org/pdf/2605.02363>
*Date/edition note:* 2026-05-04

- `[central]` Small open-weight models (7-9B: Llama 3.1-8B, Gemma 2-9B, Qwen 2.5-7B) can be semantically correct while producing 0% usable structured output: with no system prompt they reached up to 85% task accuracy on GSM8K but 0% joint correct-and-valid-JSON accuracy across all models and datasets. This means content correctness and schema compliance must be measured as separate metrics for any LLM-emitted classification pipeline.

- `[central]` The structured-output failure is a per-model generation default, not a parameter-count limitation: GPT-4o, a frontier proprietary model, also scored 0% output accuracy under both NAIVE and REFERENCE prompting on GSM8K because it systematically wrapped JSON in markdown fences — the identical failure mode seen in Gemma 2-9B. A prompt that produces clean typed JSON on one model family cannot be assumed to work on another.

- `[central]` Constrained decoding (JSON grammar via vLLM) guarantees syntactic validity but is not free: it cost 3.6x-8.2x inference latency versus unconstrained generation, and degraded output quality — under CONSTRAINED, Gemma 2-9B produced 52.4% exact-duplicate outputs and only 15.31% output accuracy on GSM8K, versus 87.41% with an optimized prompt.

- `[central]` Reliable structured output from 7-9B models is achievable without fine-tuning, but requires per-model automated system-prompt optimization rather than one shared hand-written prompt: an iterative optimizer (AloLab, meta-agent Claude Sonnet 4.5) reached 84-87% output accuracy on GSM8K and 34-40% on MATH, with 29/30 paired McNemar comparisons against the best static prompt significant at p < 0.05, at near-unconstrained latency.

- `[supporting]` The paper's evidence does NOT extend to classification or taxonomy-labeling schemas: both benchmarks are mathematical with a fixed two-field contract (reasoning + answer), and the authors explicitly state generalization to other task types and output schemas is unestablished. So no evidence here bears on how schema complexity or label-set size affects compliance.


### A6. Downstream payoff — typed retrieval, contradiction detection, and the Karpathy pattern itself

**arXiv 2606.29645 (Jun 2026) — staged metadata-enrichment ablation over RAG benchmarks**
<https://arxiv.org/pdf/2606.29645>
*Date/edition note:* 2026-06-28

- `[central]` Converting raw retrieved passages into structured, atomic JSON records — with no added metadata content, i.e. structure alone — REDUCED answer accuracy on every benchmark tested except FEVER (e.g. −0.078±0.007 F1 on MuSiQue, −0.040 on HotpotQA, −0.008±0.006 on TempLAMA). This is direct empirical counter-evidence to the assumption that atomizing/typing knowledge into discrete structured units improves downstream LLM use.

- `[central]` Metadata payoff is task-specific rather than general: across five enrichment levels, the entire end-to-end gain on the temporal benchmark came from one metadata layer (temporal validity windows, +0.220±0.008), while the later layers (confidence/conflict metadata, provenance chains) added nothing, and full enrichment was net NEGATIVE on non-temporal benchmarks (MuSiQue −0.032, HotpotQA −0.063, SimpleQA −0.010). Adding more metadata fields is not monotonically beneficial.

- `[central]` There is a measurable gap between a model correctly USING a metadata field and that field improving answers: prompting models to use confidence scores raised confidence-citation rate from 14% to 70% (+56pp) yet accuracy DROPPED (TempLAMA −0.192, MuSiQue −0.032), because the model selected high-confidence units that were temporally wrong. Compliance with a metadata schema is not evidence the schema helps.

- `[supporting]` The benefit of typed/enriched context varies systematically by model family and capability — measured across four models from three families (GPT-4.1-mini +0.273, Llama-3.1-8B +0.227, Qwen3-32B +0.160, GPT-4.1 +0.120 on TempLAMA) — with gains inversely related to model capability. A single metadata scheme therefore does not transfer uniformly across model families; provenance metadata in particular showed 0% unprompted and 0% appropriate utilization ("unprocessable").

- `[supporting]` When metadata type is aligned to the task, a much smaller/cheaper model with enriched context beat a frontier model on raw passages by ~19 F1 points (0.947 vs 0.760, 3-seed mean) — i.e. the design lever that pays is model-context alignment, not the quantity of metadata attached.

**Karpathy, *LLM Wiki* gist (442a6bf5) — the source pattern**
<https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>
*Date/edition note:* 2026-04-04

- `[central]` The gist's page taxonomy is document-genre/entity based (summaries, entity pages, concept pages, comparisons, overview, synthesis) — it proposes NO knowledge-type taxonomy, no sub-page 'knowledge unit' granularity, and no status/confidence metadata. The proposal's six-type Declarative/Procedural/Episodic scheme therefore has no precedent in the source pattern it descends from; it is an addition, not an inherited design.

- `[central]` Karpathy claims a plain markdown index file (page link + one-line summary + optional metadata, organized by category) is sufficient for retrieval at roughly 100 sources and hundreds of pages, making embedding-based RAG unnecessary at that scale. This is a falsifiable scale threshold, but stated as personal experience with no benchmark, no baseline comparison, and no measured retrieval accuracy.

- `[central]` Contradiction detection is proposed as a periodic LLM 'lint' pass over the wiki — an unstructured, prompt-driven review — rather than a typed-metadata or NLI-based mechanism. No detection rate, precision, or recall is reported; the capability is asserted, not measured.

- `[supporting]` Consistency of wiki structure across sessions and model families is delegated entirely to a single natural-language schema file (CLAUDE.md / AGENTS.md) co-evolved by the user — i.e. the pattern's answer to 'can many models apply this consistently?' is a prose instruction document, with no evaluation of cross-model agreement.

- `[supporting]` The pattern's stated value is amortized maintenance, not classification: one ingested source is claimed to touch 10-15 wiki pages, and the argument is that LLMs make bookkeeping cost near zero. No measurement of quality, error rate, or downstream retrieval benefit is offered.

**WikiContradict (Jun 2024) — 253 human-annotated contradictory Wikipedia passage pairs**
<https://arxiv.org/pdf/2406.13805>
*Date/edition note:* 2024-06-19

- `[central]` LLMs given two retrieved passages that contradict each other almost never produce an answer that surfaces the conflict. Across seven LLMs on WikiContradict's 253 human-annotated instances, correct responses under the plain two-passage prompt fell to roughly 2%–10% (e.g. Mistral-7b-instruct 2.1%, Llama-3-70b-instruct 10.4%), while the same models answered correctly 87.8%–97.6% of the time when given a single non-conflicting passage. Conflict-surfacing is therefore a measured failure mode of flat, untyped retrieval — not an assumption.

- `[central]` Explicitly instructing the model to attend to contradictions produces a large measured jump in conflict-aware answers — Llama-3-70b-instruct went from 10.4% to 43.8% correct. This means contradiction detection is a scaffolding/prompt-design property, not an emergent capability of the model reading the corpus; an LLM-maintained wiki that wants contradictions found must ask for them explicitly.

- `[central]` The benefit of explicit conflict prompting concentrates almost entirely on EXPLICIT (surface-level) contradictions and barely moves IMPLICIT ones requiring reasoning: for Llama-3-70b-instruct, explicit-conflict accuracy rose 13.3% -> 60.0% while implicit-conflict accuracy rose only 5.9% -> 17.6%. WikiContradict is 64% explicit / 36% implicit (161 vs 92 instances). Automated contradiction detection over a knowledge base should therefore be expected to catch restated-fact clashes and largely miss reasoning-dependent inconsistencies.

- `[supporting]` A small open-weight model (Mistral-7b-instruct) failed in a distinctive, silently-wrong way: rather than flagging the conflict it reconciled the two contradictory passages by presenting both answers as if compatible, and the LLM judge scored that as valid. Model size/family changes not just the accuracy but the SHAPE of the error, which is direct evidence against assuming cross-family consistency on conflict-related judgements.

- `[supporting]` Even with a small, concrete 3-way label set (correct / partially correct / incorrect) applied by trained human annotators who are the paper's own authors, inter-annotator agreement was only Cohen's kappa 0.58–0.88 across prompt templates, over 1,375 samples double-annotated for 2,750 judgements; the automated LLM judge built on top reached only ~0.8 F-score. This is a concrete ceiling data point for how reliably any fixed label set gets applied to knowledge units.

**SRAG (2026) — structured metadata tagging of chunks and queries, financial-analyst QA**
<https://arxiv.org/pdf/2603.26670>
*Date/edition note:* 2026-03 (arXiv:2603.26670v1; arXiv abstract page lists submission 27 Jan 2026, PDF metadata 31 Mar 2026)

- `[central]` SRAG — which appends structured metadata (topics, sentiment, KNOWLEDGE/QUERY TYPE labels such as informational/quantitative/comparative/analytical/information_lookup, KG triples, semantic tags) to both chunks and queries before embedding — raised GPT-5-as-judge answer scores from 72.36 to 94.35 (on a 0-100 scale, ~30% relative, Welch's t-test p=2e-13) over plain RAG on a financial-analyst QA corpus. This is direct evidence that type-tagging text units improves retrieval-grounded answers, but the metric is an LLM judge on a single domain (Apple equity-research documents), not a ground-truth retrieval metric, and the paper is an unrefereed preprint.

- `[central]` The benefit of type-tagging is concentrated in exactly the reasoning-heavy query classes (predictive 64.46->95.61 p=9e-5; analytical 65.1->93.8 p=2e-5; comparative 55.9->94.1 p=0.0002) and is ABSENT for simple fact lookup, where plain RAG already scored 98.37 and SRAG scored 97.43 (p=0.24, i.e. a statistically insignificant slight decrease). Typed retrieval therefore pays off for cross-cutting 'oracle'-style analysis and not for needle-in-haystack factual recall.

- `[central]` In the marginal ablation, NO single metadata component's removal produced a statistically significant change — removing chunk TYPE cost only -0.3 points (p=0.7), semantic tags -1.1 (p=0.15), topics -0.53 (p=0.55), KG triples +0.01 (p=0.99), sentiment +0.63 (p=0.37). So the paper does not demonstrate that the type label alone carries the gain; the authors attribute the effect to joint/compositional use of tags+topics+type and explicitly did not run the power-set/Shapley attribution that would isolate it.

- `[supporting]` The headline 30% average gain is driven by a minority tail, not a broad uplift: the tail-risk table reports median difference 0.0, P(SRAG better) = 0.441 vs P(SRAG worse) = 0.407, 90th-percentile difference +88.1, 5th-percentile -2.9, max loss -7.9, average gain when better 51.76 vs average harm when worse -1.95. Typed metadata thus helps hugely on a subset of queries and is near-neutral or mildly harmful elsewhere — a favorable but highly skewed payoff profile.

- `[supporting]` The advantage of typed/structured tagging is largest at small retrieval budgets (k=3) and shrinks as k grows to 5 and 10, indicating the mechanism is improved early-rank precision rather than added recall — so typing matters most when the context window forces a small number of retrieved units.


---

## 7. Sources fetched (28)

| # | Quality | Angle | Source |
|---|---|---|---|
| 1 | primary | A2 | [Karpen & Welch 2016, Currents in Pharmacy Teaching and Learning — faculty IRR on Bloom's](https://www.sciencedirect.com/science/article/abs/pii/S1877129715301921) |
| 2 | primary | A2 | [Larsen, Endo, Yee, Do & Lo 2022, CBE—Life Sciences Education 21(4) — RBT two-dimension contingency analysis (n=940)](https://www.lifescied.org/doi/10.1187/cbe.20-08-0170) |
| 3 | primary | A2 | [Zhang, Wong, Giacaman & Luxton-Reilly 2021, ACE '21 — automated Bloom classification](https://dl.acm.org/doi/10.1145/3441636.3442305) |
| 4 | primary | A2 | [arXiv 2511.10903 (Nov 2025) — LLM zero-shot Bloom-level classification across model families](https://arxiv.org/html/2511.10903) |
| 5 | primary | A1 | [Case & Swanson 1996/97, Academic Medicine / Advances in Medical Education — *'Fact' is in the eye of the beholder*](https://link.springer.com/chapter/10.1007/978-94-011-4886-3_40) |
| 6 | primary | A2 | [Coleman 2017, Cambridge Assessment *Research Matters* 24 — *On the reliability of applying educational taxonomies*](https://www.cambridgeassessment.org.uk/Images/426171-on-the-reliability-of-applying-educational-taxonomies.pdf) |
| 7 | primary | A1 | [Renoult, Irish, Moscovitch & Rugg 2019, Trends in Cognitive Sciences 23(12) — *From Knowing to Remembering*](https://neuropsychologylab.psych.utoronto.ca/files/FromKnowingtoRememberingTheSemanticEpisodicDistinction.pdf) |
| 8 | primary | A1 | [Rubin 2021/22, Memory & Cognition 50(3) — *A conceptual space for episodic and semantic memory*](https://sites.duke.edu/rubinlab/files/2021/08/2021-online-ConceptualSpace-Dimension-M-C.pdf) |
| 9 | primary | A1 | [Squire & Zola 1996, PNAS 93(24) — *Structure and function of declarative and nondeclarative memory systems*](https://www.pnas.org/doi/10.1073/pnas.93.24.13515) |
| 10 | primary | A1 | [Canadian Journal of Learning and Technology 34(2), 2008 — metacognition frameworks / conditional knowledge](https://files.eric.ed.gov/fulltext/EJ1073838.pdf) |
| 11 | primary | A3 | [Jansen et al. 2002 IPCC / Document Design 4(1) 2003 — controlled reader experiments on Information Mapping](https://ieeexplore.ieee.org/document/1049113/) |
| 12 | blog | A3 | [Information Mapping (vendor blog) — *The DITA topic types: square pegs and round holes*](https://informationmapping.com/blogs/news/the-dita-topic-types-square-pegs-and-round-holes) |
| 13 | primary | A3 | [Horn 1998 — *Structured Writing as a Paradigm* (the Information Mapping method, primary source)](https://faculty.washington.edu/farkas/TC510-Fall2011/Horn-StructuredWritingParadigm.pdf) |
| 14 | primary | A3 | [Procida, *Diátaxis* — the compass / decision procedure](https://diataxis.fr/compass/) |
| 15 | primary | A4 | [Sumers, Yao, Narasimhan & Griffiths 2023/24, TMLR — *CoALA: Cognitive Architectures for Language Agents*](https://arxiv.org/abs/2309.02427) |
| 16 | primary | A4 | [A-MEM: Agentic Memory for LLM Agents (NeurIPS 2025)](https://arxiv.org/abs/2502.12110) |
| 17 | primary | A4 | [Zep / Graphiti — temporal knowledge-graph agent memory (Jan 2025)](https://arxiv.org/abs/2501.13956) |
| 18 | primary | A4 | [Mem0 (Apr 2025) — scalable long-term agent memory, incl. Mem0-graph variant](https://arxiv.org/abs/2504.19413) |
| 19 | primary | A4 | [EMem (Nov 2025) — event-proposition structured conversational memory](https://arxiv.org/abs/2511.17208) |
| 20 | primary | A6 | [arXiv 2606.29645 (Jun 2026) — staged metadata-enrichment ablation over RAG benchmarks](https://arxiv.org/pdf/2606.29645) |
| 21 | blog | A3 | [Baker 2012, Every Page Is Page One — *The tyranny of the terrible troika*](https://everypageispageone.com/2012/07/28/the-tyranny-of-the-terrible-troika-rethinking-concept-task-and-reference/) |
| 22 | blog | A6 | [Karpathy, *LLM Wiki* gist (442a6bf5) — the source pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
| 23 | primary | A6 | [WikiContradict (Jun 2024) — 253 human-annotated contradictory Wikipedia passage pairs](https://arxiv.org/pdf/2406.13805) |
| 24 | primary | A6 | [SRAG (2026) — structured metadata tagging of chunks and queries, financial-analyst QA](https://arxiv.org/pdf/2603.26670) |
| 25 | primary | A5 | [arXiv 2601.12099 (Jan 2026) — 7 LLMs x 121 features x 567 excerpts, LLM-LLM vs human-human agreement](https://arxiv.org/pdf/2601.12099) |
| 26 | primary | A5 | [arXiv 2605.06940 (May 2026) — closed-set label instructions and fallback-label dominance](https://arxiv.org/pdf/2605.06940) |
| 27 | primary | A5 | [arXiv 2412.14737 (Dec 2024, rev. May 2026) — verbalized-confidence reliability, 17 prompt methods x 10 datasets](https://arxiv.org/pdf/2412.14737) |
| 28 | primary | A5 | [arXiv 2605.02363 (May 2026) — structured-output conformance in 7–9B open-weight models](https://arxiv.org/pdf/2605.02363) |

---

## 8. Run provenance

- Run ID `wf_756bdaf1-c84`, 2026-08-07 22:00 UTC → 2026-08-08 01:09 UTC (3h09m)
- 111 agents, 0 errors, 0 empty results, ~6.26M subagent tokens, 1,798 tool calls
- 6 search angles → 28 sources fetched → 140 claims extracted
- 25 claims verified (3 votes each) → 8 confirmed, 17 refuted, 9 findings after synthesis
- 2 URL duplicates filtered, 6 sources dropped on budget
- Tier 2 recovered from the run journal: 123 claims

