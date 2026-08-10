---
title: Does typing pay off downstream? (Run B)
date: 2026-08-10
status: COMPLETE — 3-vote adversarially verified
run: wf_376a9a4b-46b
verdict: NO measured evidence that type labels improve retrieval
---

# Typing Payoff Research — Run B (complete)

104 agents, 22 sources, 109 claims, 25 verified → **18 confirmed, 7 refuted**.

## Executive summary

Across everything that survived adversarial verification, knowledge typing has never been
measured in isolation — every system claiming a typing benefit bundles type labels with linking,
extraction, reranking, or temporal invalidation, and not one paper in the set runs a typed-vs-
untyped arm holding retrieval constant. The strongest direct evidence is negative: two
controlled human experiments on Information Mapping (n=65 and n=76, with the treatment texts
validated as correct by the vendor's own managing director) found zero effect on accuracy or
speed, and the sole significant effect was a subjective preference that did not beat the
incumbent text. In agent memory the measured gains are real but narrower than the design
document assumes: after correcting a column-label error in A-MEM's own table — which I resolved
this session against the LoCoMo dataset — A-MEM's advantage is concentrated in TEMPORAL
reasoning (+20 to +22 F1 over the best flat baseline), while its multi-hop margin is +0.37 F1 on
GPT-4o-mini and it LOSES single-hop and adversarial to a plain full-context baseline on GPT-4o.
Mem0's own numbers point the same way: a typed entity-relation graph buys +1.56 J overall while
HURTING single-hop (−1.42) and multi-hop (−3.96), and both variants lose to full-context
(72.90). The practical read: the one replicated payoff from "typed" structure is
temporal/validity handling, multi-hop gains are small or negative, and nothing in the verified
record justifies funding a statement-type classifier as a retrieval-quality lever.

## Findings

### F1. [HIGH] The only controlled human experiments ever run on a shipped information-typing scheme (Horn's Information Mapping) found NO task-performance benefit — no effect on correctness or speed, in either of two studies.

*Vote: unanimous 3-0 across four merged claims (0, 2, 3, 5)*

Study 1 (Jansen, Korzilius, le Pair & Roest; IEEE IPCC 2002 and Document Design 4(1):48-59,
2003): n=65 process operators at DSM, a Dutch chemical plant (64 men/1 woman, mean age 42, mean
12 years service). Between-subjects, three versions of the same 3-page reference text — the in-
use original (n=22), an IMAP rewrite (n=21), and a rewrite by a Business Communication lecturer
unfamiliar with IMAP (n=22). Groups matched on a cloze pretest and tenure. Task: 6 timed
multiple-choice lookup questions, scored incorrect unless the subject also located the answer in
the text. Effectiveness F(2,62)=1.16, p=.32 (original 74%, IMAP 76%, lecturer 67%). Efficiency
F(2,62)=2.02, p=.14 (29.95s / 30.58s / 36.36s per question). Covariates all n.s.: age p=.59,
tenure p=.46, cloze p=.11. Study 2 (IPCC 2002): n=76 CD Assembly workers at Sony Music
Entertainment Haarlem (44 Dutch-descent, 32 immigrants — 23 Turkish, rest Moroccan/Gambian),
mixed between/within design, each subject got the original of one one-page machine instruction
and the IMAP version of the other, counterbalanced; 2 physical scale-model tasks + 4 retrieval
questions. Verbatim: 'Regarding the format chosen for the organization and presentation of the
text (IMAP or traditional), there were no significant effects on accuracy, speed or evaluation
scores at all, neither apart from nor in interaction with the subject variables measured.' What
DID predict performance were reader variables (Dutch descent, years of education) — typing
helped no subgroup, including the immigrant readers hypothesized to benefit most from IMAP's
consistency principle. Independence is strong and runs AGAINST the finding's direction: academic
authors at University of Nijmegen testing a commercial trademarked method, with the IMAP text
certified as a correct application by the managing director of Information Mapping Netherlands —
which forecloses the 'you applied it wrong' rebuttal. IMAP was shipped in 40 countries to
~150,000 users at the time.

- <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>
- <https://www.jbe-platform.com/content/journals/10.1075/dd.4.1.05jan>
- <https://careljansen.nl/wp-content/uploads/2022/12/2003_Jansen_Korzilius_LePair_Roest-Information-Mapping.pdf>
- <https://repository.ubn.ru.nl/bitstream/handle/2066/74368/74368.pdf>

### F2. [HIGH] Information Mapping's only significant effect was subjective preference, and even that was PARTIAL — the typed text beat one alternative but did NOT beat the incumbent original text. The common summary 'no performance gain, only preference' overstates even the preference result.

*Vote: unanimous 3-0 across two merged claims (1, 4)*

Verbatim: 'The only statistically significant effect found of presentation format was on the
evaluative report marks given by the subjects for the three variants. The IMAP text (average
score 7.71 on a ten-point scale) was assessed as significantly more positive than was the text
revised by the lecturer (6.72). The original DSM-text (7.38) was not assessed as significantly
more positive or negative than the other texts.' Wilks' lambda=0.685, F(2,61)=14.02, p<.001. On
four rated text ASPECTS (readability, structure, ease of search, comprehensibility) there was no
difference at all: Wilks' lambda=0.90, F(6,120)=1.13, p=.35. The IPCC paper states it
independently: the IMAP version 'scored higher than ONE OF THE ALTERNATIVES,' not both. Note the
6.72 comparison text was itself a selected-best expert rewrite (two lecturers wrote versions;
the one students judged better was used). Authors' own gloss, twice: 'this study fails to
substantiate the claim that the IMAP method results in texts that lead to improved reader
performance. It only shows that readers may believe that an IMAP text is superior to a more
traditional text.' Study 2 found no format effect on report marks at all.

- <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>
- <https://www.jbe-platform.com/content/journals/10.1075/dd.4.1.05jan>

### F3. [HIGH] The Information Mapping null does NOT license 'type labels are decoration' — the experiments manipulated the whole seven-principle method as one treatment and were powered only to detect LARGE effects. Typing was never isolated, and the authors explicitly call for that isolation as future work.

*Vote: raised unanimously by all three verifiers as a binding scope limit*

Verbatim from Method: 'The number of subjects was based on a statistical power of .80, a large
effect size and an alpha of .05 (see Cohen, 1992).' So the null rules out a large benefit only —
this is absence of evidence at large effect size, not demonstrated equivalence. IMAP bundles
seven PRINCIPLES (chunking, hierarchy of chunking and labeling, relevance, consistency,
labeling, integrated graphics, accessible detail) PLUS seven information TYPES (procedure,
structure, classification, process, concept, fact, principle — Table 1, p.51). All moved
together; the paper notes the IMAP version differed 'especially in structure and layout.'
Authors' closing recommendation: research is needed 'into the specific role played by each of
the seven principles the method is based on.' Two further scope limits: the task was simple
single-fact lookup by domain experts in a 3-page text (mean 78% correct, ~194s total), and the
comparison texts were strong — 'Both the original text and the version by the communication
lecturer may be characterized as reasonably well structured and articulated.' Correct citation
form for the design doc: 'typed restructuring as a whole method showed no measurable task-
performance benefit on short lookup texts,' NOT 'type labels are inert.'

- <https://careljansen.nl/wp-content/uploads/2022/12/2003_Jansen_Korzilius_LePair_Roest-Information-Mapping.pdf>
- <https://careljansen.nl/wp-content/uploads/2022/12/2002_Jansen-Information_Mapping.pdf>

### F4. [HIGH] RESOLVED THIS SESSION — a live contradiction inside the verified set. A-MEM's arXiv table was RELABELED between v1-v9 and v10-v11 with identical numbers, so the same figures carry different category names depending on which version a citation used. The v11 labeling is correct; 27.02 → 9.65 is MULTI-HOP F1, and every secondary citation drawn from v1-v9 (and one of the confirmed claims here) has the categories wrong.

*Vote: claims 6/7 (v11 labels) vs claims 8/9 (v6 labels) directly conflicted, both 'confirmed'; adjudicated by direct primary re-verification*

I fetched both HTML versions and extracted the tables byte-for-byte. Numeric matrices are
IDENTICAL (nothing was re-run); only headers moved. v1 header: Single Hop | Multi Hop | Temporal
| Open Domain | Adversial. v11 header: Multi Hop | Temporal | Open Domain | Single Hop |
Adversial. I then downloaded the LoCoMo dataset (2.8 MB) and counted categories directly: cat1
n=282 multi-hop, cat2 n=321 all 'When did...' (temporal), cat3 n=96 speculative inference
('Would Caroline likely...'), cat4 n=841 single-hop, cat5 n=446 adversarial. A-MEM's evaluator
aggregates by sorted category integer 1..5, which maps to the v11 header exactly. Three
independent plausibility checks agree: (a) a full-context baseline should dominate single-hop
lookup — under v11 GPT-4o LoCoMo single-hop is 61.56, under v1 it would be 28.00 with 'open
domain' at 61.56, which is implausible for a 96-question speculative-inference category; (b) F1
word-overlap on speculative 'would likely' questions should be LOW, and v11 puts open-domain at
12-17 across the board; (c) the authors themselves corrected the order in a later revision.
Verdict: v11 is authoritative, v1-v9 were mislabeled. Consequence for the design doc: any A-MEM
category claim sourced before Oct 2025 must be re-mapped, and the paper's own prose
('particularly in Multi Hop reasoning and Open Domain tasks') is stale text carried over
unchanged from v1 that now contradicts its own corrected table.

- <https://arxiv.org/html/2502.12110v1>
- <https://arxiv.org/html/2502.12110v11>
- <https://raw.githubusercontent.com/snap-research/locomo/main/data/locomo10.json>

### F5. [HIGH] A-MEM's headline ablation is NOT evidence that structure buys reasoning — removing link generation + memory evolution degrades ALL FIVE categories by 36-70%, with the WORST collapse on single-hop, the easiest category. That degradation profile is the signature of a broken retrieval index, not of a reasoning-specific capability being removed.

*Vote: 3-0 (claim 7), corroborated by claims 6 and 9 and re-verified directly*

Table 3 (GPT-4o-mini), full → w/o LG&ME under corrected labels: Multi-Hop 27.02→9.65 (−17.37,
−64.3%), Temporal 45.85→24.55 (−21.30, −46.5%), Open Domain 12.14→7.77 (−4.37, −36.0%), Single
Hop 44.65→13.28 (−31.37, −70.3%), Adversarial 50.03→15.32 (−34.71, −69.4%). Single-hop drops
most on BOTH absolute and relative readings, which closes the obvious rebuttal that large
absolute drops just track large base scores. The ablated variant's 13.28 single-hop sits ~27
points below the strongest flat baselines (LoCoMo 40.36, MemGPT 41.04) — though note it still
beats ReadAgent (9.67) and MemoryBank (6.61), so the phrase 'below every flat baseline' that
appeared in one confirmed claim is an overreach and should be narrowed. Three structural limits:
(1) there is no 'w/o LG' row, so link generation is NEVER isolated from memory evolution; (2)
single run, single base model for the ablation, no seeds, no variance, no significance tests;
(3) not reproducible from the public repo — WujiangXu/A-mem exposes no --no-lg/--no-me flags.
Most important for the design question: A-MEM has NO closed type taxonomy. Its analyze_content()
JSON schema requests only free-form keywords, a one-sentence context, and free-form tags — no
enum, no controlled vocabulary. A 'category' constructor param exists but is never populated
from the LLM analysis and defaults to 'Uncategorized' (dead code).

- <https://arxiv.org/html/2502.12110v11>
- <https://arxiv.org/abs/2502.12110>

### F6. [HIGH] Under corrected labels, A-MEM's real advantage over flat baselines is TEMPORAL reasoning (+20.33 and +22.12 F1), not multi-hop (+0.37 and +2.50). On GPT-4o it LOSES single-hop to a plain full-context baseline (48.43 vs 61.56) and loses adversarial on both backbones. The 'structured memory buys multi-hop' story is largely an artifact of the mislabeled table.

*Vote: claim 10 confirmed 3-0 on the numbers; its category attribution corrected by this session's direct verification*

Table 1 recomputed under v11 labels, A-MEM minus the best flat baseline (LoCoMo full-context or
MemGPT). GPT-4o-mini: Multi-Hop +0.37 (27.02 vs MemGPT 26.65), Temporal +20.33 (45.85 vs 25.52),
Open Domain +0.10, Single Hop +3.61, Adversarial −19.20 (50.03 vs LoCoMo 69.23). GPT-4o: Multi-
Hop +2.50 (32.86 vs 30.36), Temporal +22.12 (39.41 vs 17.29), Open Domain +0.63, Single Hop
−13.13 (48.43 vs 61.56), Adversarial −16.26 (36.35 vs 52.61). The 45.85-vs-18.41 gap that one
confirmed claim described as 'A-MEM's Multi-Hop advantage' is in fact TEMPORAL. The paper
concedes baseline strength verbatim: 'while LoCoMo and MemGPT show strong performance in certain
categories like Open Domain and Adversial tasks due to their robust pre-trained knowledge in
simple fact retrieval...' — a concession against interest, the most credible direction for self-
reported benchmarks. Caveats: single-run author-reported F1, no variance or CIs, so small gaps
(+0.37, +0.10, +0.63) should be read as zero. The LoCoMo baseline is genuinely flat — it stuffs
the complete preceding conversation into the prompt with no retrieval or memory layer.

- <https://arxiv.org/html/2502.12110v11>
- <https://arxiv.org/abs/2502.12110>

### F7. [HIGH] Zep/Graphiti's numbers are accurately cited in the design document but are vendor self-benchmarks with NO ablation, an open-vocabulary predicate scheme rather than a type taxonomy, a headline stated in RELATIVE not percentage-point terms, a latency claim confounded by prompt size, and an unexplained regression the authors concede.

*Vote: unanimous 3-0 across four merged claims (11, 12, 13, 14)*

NUMBERS CONFIRMED VERBATIM (Table 3, single table with a Model column, not two tables): gpt-4o
multi-session 44.3%→57.9% (printed delta 30.7%↑) and temporal-reasoning 45.1%→62.4% (38.4%↑);
gpt-4o-mini multi-session 40.6%→47.4% (16.7%↑) and temporal-reasoning 36.5%→54.1% (48.2%↑ —
LARGER relative gain than gpt-4o's, so 'smaller figures for mini' is true only in absolute
terms). UNITS: the '18.5%' headline is RELATIVE, not points. Overall LongMemEval 60.2%→71.2% for
gpt-4o (+11.0 points, 18.3% relative) and 55.4%→63.8% for gpt-4o-mini (+8.4 points, 15.2%
relative). The 15.2% figure only reconciles under the relative computation (8.4/55.4=15.16%),
which pins the convention; Table 3's printed deltas reproduce it exactly (13.6/44.3=30.7%,
17.3/45.1=38.4%). Anyone reading '30.7%' as points is wrong by more than 2x. LATENCY:
28.9s→2.58s (91.1%) and 31.3s→3.20s (89.8%) — but the baseline stuffs 115k context tokens vs
Zep's 1.6k, so the ~90% cut is largely a prompt-size artifact. NO ABLATION EXISTS: substring
'ablat' occurs 0 times in the full text; omit/disable/remov/isolat/lesion all 0. Every number is
whole-system Zep vs external baselines, so gains are equally attributable to
BM25+cosine+BFS+RRF/MMR/cross-encoder reranking, fact extraction, or temporal edge invalidation.
TYPING IS OPEN-VOCABULARY: the only typing described is 'The relation_type should be a concise,
all-caps description of the fact (e.g., LOVES, IS_FRIENDS_WITH, WORKS_FOR)'; entity extraction
requests no type at all. The authors place closed ontologies in FUTURE work: 'domain-specific
ontologies present significant potential... warrant further exploration.' REGRESSIONS: single-
session-assistant drops on both models (gpt-4o 94.6%→80.4%, gpt-4o-mini 81.8%→75.0%) plus
knowledge-update on mini (76.9%→74.4%); authors call it 'a notable exception to Zep's otherwise
consistent improvements' with no hypothesis. The single LARGEST gain is single-session-
preference 20.0%→56.7% (+184%), a preference-recall category, not multi-hop. PROVENANCE: all
five authors @getzep.com, arXiv v1 only, never revised in 19 months, no venue, no peer review,
and the authors admit they could not get MemGPT working and invite replication that has not
happened.

- <https://arxiv.org/abs/2501.13956>
- <https://arxiv.org/html/2501.13956v1>

### F8. [HIGH] Mem0's own data is the closest thing to a clean typed-layer test, and it is near-null-to-negative: adding a typed entity-relation graph on top of flat natural-language memories buys +1.56 J points overall (~2% relative) while HURTING single-hop (67.13→65.71) and multi-hop (51.15→47.19), with both variants losing to a plain full-context baseline (72.90).

*Vote: unanimous 3-0 across three merged claims (15, 16, 17)*

Table 2 (LLM-as-a-Judge, LOCOMO, 10 runs with ±1 SD): Mem0 66.88±0.15, Mem0^g 68.44±0.17, Full-
context 72.90±0.19. Table 1 per category — Single-Hop 67.13±0.65→65.71±0.45 (−1.42), Multi-Hop
51.15±0.31→47.19±0.67 (−3.96, −7.7% relative), Open-Domain 72.93±0.11→75.71±0.21 (+2.78),
Temporal 55.51±0.34→58.13±0.44 (+2.62, F1 48.93→51.55). Two up, two down. Effects are 4-13x the
reported SD, so small but resolvable, not noise. Authors concede both regressions in text: graph
memory 'does not provide performance gains here, indicating potential inefficiencies or
redundancies in structured graph representations for complex integrative tasks compared to dense
natural language memory alone' (multi-hop) and 'yields marginal performance drop... relational
structure provides limited utility when the retrieval target occupies a single turn' (single-
hop). Mem0^g is genuinely typed: 'a directed labeled graph G=(V,E,L)' where 'Labels L assign
semantic types to nodes (e.g., Alice - Person, San_Francisco - City)', Neo4j-backed, LLM triplet
extraction. Vendor-authored (research@mem0.ai; Singh and Yadav are founders) — but this is an
ADMISSION AGAINST INTEREST: no vendor fabricates a result showing its flagship graph feature is
near-useless and beaten by dumping the transcript into context. A hostile competitor (Zep)
independently reproduces the same reading. Two qualifications: (a) framing the loss categories
as 'the two it is usually justified by' is a selective read — graph memory is conventionally
justified by multi-hop AND temporal, and temporal is where it wins; (b) there is NO typed-graph
vs untyped-graph arm, so this measures graph-layer vs no-graph-layer and cannot by itself argue
against a type classifier. The adversarial category was DROPPED ('ground truth answers were
unavailable'), so 4 of 5 categories.

- <https://arxiv.org/abs/2504.19413>

### F9. [MEDIUM] CONVERGENT PATTERN ACROSS ALL THREE AGENT-MEMORY SYSTEMS: the one category where structured memory reliably beats flat baselines is TEMPORAL reasoning. Multi-hop gains are small (A-MEM +0.37/+2.50 over best baseline) or outright negative (Mem0-graph −3.96), and simple lookup is flat-to-worse in every system.

*Vote: synthesis across three separately-verified sources; no single claim asserted this, no independent replication exists*

A-MEM (corrected labels): Temporal +20.33 F1 over best flat baseline on GPT-4o-mini and +22.12
on GPT-4o — by far its largest margin, and ~8x its multi-hop margin. Zep: temporal-reasoning
+38.4% relative on gpt-4o and +48.2% on gpt-4o-mini, its most consistent category gain across
both models (single-session-preference is larger on gpt-4o but is a preference-recall category,
not a reasoning one). Mem0-graph: temporal +2.62 J is the category the authors single out —
'structured relational representations in addition to natural language memories significantly
aid in temporally grounded judgments' — while the two hop categories regress. Meanwhile single-
hop lookup: A-MEM +3.61 on mini but −13.13 on GPT-4o; Mem0-graph −1.42; Zep's own regression is
on single-session-assistant. MECHANISM CAUTION, and it is decisive for the design decision: the
plausible cause is temporal/validity machinery, not type labels. Zep implements explicit
temporal edge invalidation (t_valid/t_invalid, 'invalidat' appears 7 times); Mem0^g encodes
relationship recency; A-MEM's gain comes from link generation + memory evolution that rewrites
stale notes. None of these is a statement-type taxonomy. Confidence is medium, not high, because
all three are author- or vendor-reported single-run benchmarks on overlapping datasets (LoCoMo
appears in two of the three), none is peer-reviewed except A-MEM, and no independent replication
exists for any of them.

- <https://arxiv.org/html/2502.12110v11>
- <https://arxiv.org/abs/2501.13956>
- <https://arxiv.org/abs/2504.19413>

### F10. [HIGH] NO source in the verified set isolates type labels from anything else. Every 'typed' system confounds typing with linking, extraction, reranking, or temporal invalidation — and two of the three agent-memory systems do not even use a closed type vocabulary. There is currently zero direct measured evidence that a statement-type classifier improves retrieval, and zero measured evidence either way on type-matched contradiction pairing.

*Vote: raised independently by verifiers on claims 0/2/3/5 (IMAP), 6/7/9 (A-MEM), 13/14 (Zep), 16/17 (Mem0)*

IMAP: seven principles + seven types manipulated as a single treatment; authors explicitly flag
they cannot attribute the null to any one principle. A-MEM: ablation arms are 'w/o LG & ME' and
'w/o ME' only — link generation is never ablated alone — and the typing is free-form LLM
keywords/tags with a dead 'category' field, not a taxonomy. Zep: zero ablation sections in the
entire paper; typing is an open-vocabulary all-caps relation_type string; the authors place
formal ontologies in future work. Mem0: the arm is graph-layer vs no-graph-layer, never typed-
graph vs untyped-graph. So for every headline number, the counterfactual 'same pipeline, same
retrieval, type labels stripped' was never run. Additionally, angles 3, 4, and 5 of the research
brief produced NO surviving claims at all — nothing was verified about SRAG's 72.36→94.35
metadata-tagging result, arXiv 2606.29645's finding that structure-alone JSON conversion REDUCED
accuracy while temporal-validity metadata was the only layer with payoff,
GraphRAG/LightRAG/LazyGraphRAG multi-hop concentration, WikiContradict's 2-10%/43.8%
contradiction-surfacing rates, type-matched contradiction pairing, EMem, CoALA, HippoRAG, or any
post-Karpathy LLM-wiki implementation. Those numbers remain exactly as unverified as before this
round.

- <https://careljansen.nl/wp-content/uploads/2022/12/2003_Jansen_Korzilius_LePair_Roest-Information-Mapping.pdf>
- <https://arxiv.org/html/2502.12110v11>
- <https://arxiv.org/abs/2501.13956>
- <https://arxiv.org/abs/2504.19413>

## Caveats

SCOPE GAP — the largest caveat. Only angles 1 and 2 produced surviving claims. Angles 3
(type/metadata-aware retrieval: SRAG 72.36→94.35, arXiv 2606.29645 structure-hurts/temporal-
helps, GraphRAG/LightRAG), 4 (contradiction detection: WikiContradict 2-10%/43.8%, type-matched
pairing), and 5 (LLM-maintained wiki implementations, Letta/Cursor/Claude Code memory typing)
produced ZERO verified claims. Every number in the design document from those angles is still
unverified. Do not treat this synthesis as covering them.  CITATION-INTEGRITY HAZARD, now
resolved but pervasive in the secondary literature. A-MEM's arXiv table was silently relabeled
between v9 and v10-v11 with identical numbers. Any citation of A-MEM categories published
between Feb and Oct 2025 — including two of the claims that passed verification here — carries
wrong category names. The design document must cite v11 explicitly and re-map any inherited
attribution. The consequence is not cosmetic: it flips the headline from 'structure buys multi-
hop' to 'structure buys temporal.'  SOURCE QUALITY IS UNEVEN AND MOSTLY SELF-REPORTED. Zep is
vendor-authored (all five authors @getzep.com), never peer-reviewed, arXiv v1 only in 19 months,
with the authors themselves admitting they could not get the MemGPT comparison working and
inviting replication that has not occurred. Mem0 is vendor-authored and not peer-reviewed. A-MEM
is the only peer-reviewed source (NeurIPS 2025) and its ablation is not reproducible from its
public repo. Where these vendor sources report results ADVERSE to their own product (Mem0's
graph regressions, Zep's single-session-assistant regression, A-MEM conceding flat baselines win
adversarial), credibility is high — admissions against interest. Where they report wins, treat
as unreplicated.  STATISTICAL WEAKNESS THROUGHOUT. A-MEM and Zep report single runs with no
seeds, variance, CIs, or significance tests, so gaps under ~3 points are uninterpretable. Zep
reports no per-category question counts, so its ±3.36% knowledge-update regression may be noise.
Mem0 is the only one reporting SDs (10 runs), but over a fixed question set from 10
conversations — that captures sampling temperature, not question-sampling variance. LoCoMo
itself is small (10 conversations, 16-26k tokens each) and fits inside modern context windows,
which is why a naive full-context baseline beats every memory system on it; Zep's public
critique documents further LoCoMo defects (wrong speaker attribution, underspecified questions,
no knowledge-update tests). A separate public allegation (Sarah Wooders, Letta, Aug 2025) that
Mem0 mis-implemented competitor baselines attacks the CROSS-SYSTEM rows, not the intra-paper
Mem0 vs Mem0^g comparison this synthesis relies on.  IMAP IS UNDERPOWERED AND CONFOUNDED. Both
studies were sized for power .80 at a LARGE effect size — they rule out a large benefit, not a
small or medium one, and no test statistics at all are reported in the IPCC version (0 F-values,
0 p-values). Cell sizes ~20-22. The treatment was the whole seven-principle method, so the null
cannot be attributed to type labels. Transfer validity is also limited: this measured human
skim-retrieval in 1-3 page documents, not machine retrieval ranking, contradiction pairing, or
multi-hop QA.  ONE UNRESOLVED CONTRADICTION INSIDE THE EVIDENCE. Three claims asserting that a
2007 follow-up (Information Design Journal 15(1), le Pair/Jansen et al.) found IMAP gains on
LONGER texts were all REFUTED 0-3 — the source is paywalled and could not be verified. Yet one
verifier working on the 2003 paper independently reported that same follow-up as showing
effectiveness AND efficiency gains on a longer text plus efficiency gains from format features
alone. That would be a direct counterexample making the benefit conditional on document length.
It is currently unresolved in both directions and should not be cited either way. Note also that
several IEEE-sourced claims were marked refuted purely because ieeexplore.ieee.org was
inaccessible, not because their substance failed — the same content was independently confirmed
from the author-hosted PDF.  TIME SENSITIVITY. The IMAP results (2002/2003) are fixed historical
findings and do not decay, but their transfer to LLM pipelines was never established. The agent-
memory papers are 12-18 months old in a field that moves fast; they describe the state of these
three systems in 2025, not current SOTA.

## Open questions

- Does ANY published work run the actual experiment this decision needs — same corpus, same
retriever, same ranking, with type labels present vs stripped? Nothing in the verified set does.
If no such study exists, the cheapest resolution is to run it in-house on the existing pipeline
before funding a classifier: hold retrieval constant and toggle the type field.

- Is the replicated temporal gain (A-MEM +20-22 F1, Zep +38-48% relative, Mem0-graph +2.62)
caused by type labels or by temporal-validity metadata specifically? All three systems that show
it also implement explicit recency/invalidation machinery. The unverified arXiv 2606.29645
result — that temporal-validity metadata was the ONLY metadata layer with measured payoff
(+0.220) while structure-alone conversion REDUCED accuracy — would independently confirm this if
it holds, and it is the single highest-value unverified claim remaining.

- Does the 2007 IDJ follow-up (le Pair/Jansen) really show Information Mapping gains on longer
texts, with format features alone improving efficiency but not effectiveness? Three claims
asserting it were refuted as unverifiable while a separate verifier reported it as real. If
true, the IMAP evidence becomes 'typing pays off only past a length threshold' rather than
'typing does nothing' — a materially different input to the design decision.

- Is there ANY measured evidence that type-matched candidate pairing (claim-vs-claim, rule-vs-
rule) improves contradiction recall or precision over untyped pairing? Angle 4 produced zero
surviving claims, including the WikiContradict baseline numbers. Since contradiction pairing is
one of the two consumers the wiki layer is being built for, this gap is directly load-bearing
and currently has no evidence on either side.

## Refuted — never cite as support

- *(vote 0-3)* The authors' own earlier Information Mapping experiment found NO measurable effects of IMAP restructuring — corroborating the 'typed restructuring showed no task-performance benefit' prior — but the abstract scopes that null result specifically to a RELATIVELY SHORT text, not to IMAP in general.
- *(vote 0-3)* In the follow-up experiments, IMAP restructuring DID produce a measured task-performance benefit when the text was long: readers were both more effective (accuracy) and more efficient (time) with the IMAP version. This is a direct counterexample to a blanket 'information typing is decoration' claim — the benefit is conditional on document length.
- *(vote 0-3)* Surface format features alone (typical IMAP presentation applied to an otherwise unaltered conventional text) improved efficiency and subjective appreciation but did NOT improve effectiveness — separating the presentation layer from the underlying typed decomposition, and matching the 'preference improves, correctness doesn't' pattern.
- *(vote 0-3)* The record is SINGLE-authored by C. (Carel) Jansen, Dept. of Business Communication, University of Nijmegen (Radboud), pp. 307-318, IPCC 2002 Portland OR — so citing it as 'Jansen et al. 2002' misstates the authorship. The two-study design and the sample sizes in the design document (n=65, n=76) are CONFIRMED exactly. Caveat: the abstract says the study-1 text was 'intended for operators working at a Dutch plant' — it does not state the 65 subjects themselves were plant operators, so 'n=65 plant operators' is an inference, not a stated fact.
- *(vote 0-3)* CONFIRMED: study 1 found zero task-performance benefit from Information-Mapping-typed restructuring — no effect on either accuracy or speed. This is the strongest single data point that assigning information-type labels and restructuring content by type does not, by itself, improve downstream task performance.
- *(vote 0-3)* CONFIRMED with a tightening: the only positive result was subjective preference, and even that held against only ONE of the two comparison texts (the original, not the expert-rewritten version). The author's own reading is that readers may merely *believe* a typed text is better. Design-doc claims should say 'preferred over one of two alternatives', not 'preferred'.
- *(vote 1-2)* PARTIALLY CONFIRMED / PARTIALLY REFUTED: flat baselines beat A-MEM on Adversarial with both GPT models by large margins (GPT-4o-mini: LoCoMo 69.23 vs A-Mem 50.03 F1; GPT-4o: 52.61 vs 36.35), and on GPT-4o the flat baseline also beats A-MEM on Single Hop (61.56 vs 48.43). But the 'Open Domain' half of the collected claim is wrong for the GPT models: A-MEM narrowly wins Open Domain there (12.14 vs 12.04 and 17.10 vs 16.47); only MemGPT on Qwen2.5-3b edges it out (7.04 vs 7.12 — actually A-Mem still wins). The paper's own prose nonetheless concedes baseline strength on Open Domain and Adversarial.
