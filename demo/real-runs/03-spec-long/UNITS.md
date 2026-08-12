# 03-spec-long

Rendered from `runs/spec/` — the run tree kip wrote. Everything below is in those artifacts; nothing is added here.

- source: 12,311 words
- units: 12  (one per 1,025 words)
- omissions flagged: 5

## 1. The statement classifier assigns a knowledge type to one short statement and returns one classification record, working on statements extracted from documents and statements taken from conversation. Its contract is deliberately narrow: one statement in, one record out.

**Role in the source.** The scope statement the whole specification is built on; everything downstream assumes this unit of work.

- *primary* ✓ (lines 3–4): “Assigns a knowledge type to a short statement. One statement in, one classification record out.”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `contract`, `scope`

## 2. Measured with eight blind raters and no answer key in existence, the taxonomy reaches inter-rater Krippendorff alpha of 0.934 on 160 statements from eight generated sources and 0.894 on 85 statements drawn from three published documents. Real published prose costs roughly 0.05 against generated statements.

**Role in the source.** The headline reliability result, and the number every design decision in the document is ultimately judged against.

- *primary* ✓ (lines 12–12): “| 160 statements from eight generated sources | **0.934** |”
- *primary* ✓ (lines 13–13): “| 85 statements from three published documents | **0.894** |”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `reliability`, `evaluation`

## 3. For scale, the argumentative-zoning scheme reached kappa 0.71 with seven categories and a 111-page codebook, and CoreSC reached 0.50 to 0.57 with eleven categories. This taxonomy has fifteen labels, so its 0.934 is high relative to published schemes of comparable or smaller size.

**Role in the source.** Supplies the external yardstick without which the headline number is uninterpretable.

- *primary* ✓ (lines 18–19): “For scale: the argumentative-zoning scheme reached κ 0.71 with seven categories and a 111-page codebook; CoreSC reached 0.50–0.57 with eleven.”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `reliability`, `prior art`

## 4. The specification labels every claim by its evidential status: VERIFIED means it survived three-vote adversarial verification against a named primary source, MEASURED means it comes from the in-house runs that measured this codebook rather than a published one, and DESIGN means an engineering decision with no supporting measurement.

**Role in the source.** The document's own epistemic convention, which is what lets a reader tell its evidence from its opinions.

- *primary* ✓ (lines 23–24): “**Evidence convention.** Every claim marked `[VERIFIED]` survived three-vote adversarial verification against a primary source”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `evidence`, `methodology`

## 5. A classification is a pure function of the statement, the prompt version and the classifier model. Re-running with a different triple appends a new record rather than replacing the old one, so consumers pick the record whose stamps they trust.

**Role in the source.** The immutability rule that makes the output auditable over time.

- *primary* ✓ (lines 74–75): “**Append, never overwrite.** A classification is a pure function of `(statement, prompt_version, classifier_model)`.”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `contract`, `provenance`

## 6. The classifier answers what kind of statement something is and never whether it is correct. Epistemic maturity is produced separately as `status`, but truth is not, and neither are relationships between statements.

**Role in the source.** The boundary that separates this component from the judgment work done elsewhere in the pipeline.

- *primary* ✓ (lines 79–80): “**The classifier does not judge truth.** It answers "what kind of statement is this", never "is this correct".”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `contract`, `scope`

## 7. The taxonomy is five coarse types over fifteen fine labels, with each fine label mapping to exactly one coarse type by lookup table rather than by judgment. The coarse types are case, method, concept, model and system, plus `general` assigned by code.

**Role in the source.** The structure of the taxonomy itself, as it stands after the dissolution of `rule` and the creation of `system`.

- *primary* ✓ (lines 86–87): “Five coarse types. Fifteen fine labels, each mapping to exactly one coarse type. The mapping is a lookup table, not a judgment.”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `taxonomy`, `structure`

## 8. Within a single annotation scheme, per-category reliability varies by a factor of two and the abstract categories are systematically worst: CoreSC measured Conclusion at 0.89 and Method at 0.74, against Hypothesis 0.46, Motivation 0.46 and Model 0.43. Any category that cannot be written as a surface test should be expected to land near 0.45 regardless of codebook quality.

**Role in the source.** The verified finding that governs how every definition in the document is written, and the reason surface cues are preferred to judgments throughout.

- *primary* ✓ (lines 133–135): “CoreSC measured `Conclusion` 0.89, `Background` 0.87, `Object` 0.81, `Observation` 0.79, `Result` 0.78, `Method` 0.74 — against `Hypothesis` 0.46, `Motivation` 0.46, `Model` 0.43.”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `reliability`, `definitions`

## 9. A named fallback offered to the model is measurably catastrophic: four frontier models given one plus the instruction to assign it for unknown cases recorded 96.1% full agreement with Fleiss kappa of -0.001 and identified the minority class zero times. `general` is therefore assigned by code and never shown to the model.

**Role in the source.** The verified evidence behind the single most counter-intuitive design rule in the document.

- *primary* ✓ (lines 158–160): “A **named** fallback given to the model is catastrophic: four frontier models given one plus "assign it for unknown cases" recorded 96.1% agreement with Fleiss κ **−0.001**”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `general`, `evidence`

## 10. Self-reported confidence cannot drive the `general` assignment. Asked to score all fifteen labels 0-100, an absolute threshold of 90 sends 86% of assignments to `general` and collapses alpha to 0.605, while taking the highest-scoring label with no threshold reaches 0.930 — statistically level with simply asking for one label.

**Role in the source.** A measured rejection of an obvious design, retained in the document so it is not re-attempted.

- *primary* ✓ (lines 176–176): “| **absolute threshold 90** | **0.605** | **86%** |”
- *primary* ✓ (lines 172–172): “| score all fifteen, take the highest | 0.930 | 0% |”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `general`, `evaluation`

## 11. The reason abstention fails is that raters disagree about their own uncertainty more than they disagree about the label: eight raters can all pick `procedure` and score it 95, 88, 72, 91, 60, 85, 78 and 93, so under any threshold some abstain and some do not, turning a unanimous agreement into a disagreement.

**Role in the source.** The mechanism behind the abstention result, and the reason it generalizes beyond the specific threshold tried.

- *primary* ✓ (lines 182–183): “**Raters disagree about their own uncertainty more than they disagree about the label.**”

grounding: `attributable` · decision: `keep` · quantitative: `False` · topics: `general`, `evaluation`

## 12. Three separate measurements show the same pattern: independent booleans plus priority resolution cost 0.092, interior tiers cost 0.11, and confidence plus a threshold collapses to 0.605. Anything that turns one classification decision into two costs more in the second step than it gains in the first.

**Role in the source.** The generalization drawn across three independent negative results, and the strongest design constraint in the document.

- *primary* ✓ (lines 192–194): “**Anything that turns one classification decision into two costs more in the second step than it gains in the first.**”

grounding: `attributable` · decision: `keep` · quantitative: `True` · topics: `design principle`, `evaluation`

## What the omission check said was missing

- **missing** — All fifteen fine-label definitions (section 3.2) are absent. Each is a self-contained definition with cues, exclusions and exemplars -- the densest retrievable content in the document.
- **missing** — All twenty-two pairwise separation rules (section 3.3) are absent. Each states a decidable test between two labels and several carry MEASURED collision counts.
- **missing** — The status ladder, the scope field and the form field are each defined with measured reliability figures and none is represented.
- **missing** — Section 6 on conversational statements carries three VERIFIED findings about classifying chat, including that six frontier models reached only kappa 0.38-0.58 where human annotators exceeded 0.90.
- **missing** — The evidence register in section 9 enumerates every claim in the document by evidential status. Not one of its rows is represented.
