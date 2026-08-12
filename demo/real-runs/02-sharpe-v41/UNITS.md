# 02-sharpe-v41

Rendered from `runs/sharpe-v41/` — the run tree kip wrote. Everything below is in those artifacts; nothing is added here.

- source: 223 words
- units: 7  (one per 31 words)
- omissions flagged: 0

## 1. Sharpe's central result: before costs, the return on the average actively managed dollar equals the return on the average passively managed dollar. It holds by arithmetic rather than by evidence, and it is conditional on 'active' and 'passive' being defined in the senses the paper gives.

**Role in the source.** The paper's headline claim, and the first of two propositions everything else establishes.

- *primary* ✓ (lines 4–5): “before costs, the return on the average actively managed dollar will equal the return on the average passively managed dollar”
- *supporting* ✓ (lines 3–3): “If "active" and "passive" management styles are defined in sensible ways, it must be the”
- *supporting* ✓ (lines 7–8): “they depend only on the laws of addition, subtraction, multiplication and division.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `passive management`, `market arithmetic`

> imported: Imported the definitional precondition and the arithmetic-only character, each cited.

## 2. After costs, the average actively managed dollar must underperform the average passively managed dollar. Since the two pools earn the same return before costs, and active managers trade frequently, the gap is the cost difference. It is a corollary of the before-costs identity rather than an independent finding.

**Role in the source.** The paper's second proposition, and the one with consequences for choosing a manager.

- *primary* ✓ (lines 5–7): “after costs, the return on the average actively managed dollar will be less than the return on the average passively managed dollar”
- *supporting* ✓ (lines 4–5): “before costs, the return on the average actively managed dollar will equal the return on the average passively managed dollar”
- *supporting* ✓ (lines 14–14): “such managers tend to trade fairly frequently”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `costs`

> imported: Imported the before-costs identity and the frequent-trading premise, each cited.

## 3. Both propositions about active and passive returns hold over any time period and depend only on addition, subtraction, multiplication and division; nothing else is required. The result therefore cannot be overturned by better data, only by rejecting the definitions it starts from.

**Role in the source.** States the argument's logical status, which is what separates it from the empirical literature on manager performance.

- *primary* ✓ (lines 7–8): “These assertions will hold for any time period. Moreover, they depend only on the laws of addition, subtraction, multiplication and division. Nothing else is required.”
- *supporting* ✓ (lines 3–3): “If "active" and "passive" management styles are defined in sensible ways, it must be the”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`, `logical status`

> imported: Resolved 'These assertions' to the two propositions; the 'only by rejecting the definitions' clause is licensed by the conditional in the cited supporting excerpt.

## 4. A passive investor holds every security in the market in the same proportion as the market itself; an active investor is anyone who is not passive, whose portfolio differs from the market at some or all times. The two categories are exhaustive and mutually exclusive.

**Role in the source.** The definitional foundation the whole argument is stated as conditional on; disputing these definitions is the standard route to evading the conclusion.

- *primary* ✓ (lines 10–12): “A passive investor always holds every security from the market, with each represented in the same manner as in the market. An active investor is one who is not passive. Her portfolio will differ from that of the passive managers at some or all times.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `definitions`, `active management`, `passive management`

> imported: Merged the two definitions; exhaustiveness follows from 'is one who is not passive' in the primary excerpt, so no import was needed.

## 5. Active managers trade fairly frequently because they act on perceptions of mispricing and those perceptions change often. This frequent trading is the mechanism behind the cost gap that makes active management underperform after costs.

**Role in the source.** Supplies the causal mechanism for the cost difference driving the after-costs result.

- *primary* ✓ (lines 12–14): “Because active managers usually act on perceptions of mispricing, and because such perceptions change relatively frequently, such managers tend to trade fairly frequently”
- *supporting* ✓ (lines 5–7): “after costs, the return on the average actively managed dollar will be less than the return on the average passively managed dollar”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `trading costs`

> imported: Imported the after-costs result the mechanism explains, cited.

## 6. The market return over any period is the weighted average of the returns on every security in the market, weighted by each security's market value at the start of the period. Because a passive investor holds the market in exactly those proportions, each passive manager earns precisely this return before costs.

**Role in the source.** The first premise of the proof: the step connecting the definition of passive holding to a specific return.

- *primary* ✓ (lines 17–19): “Over any specified time period, the market return will be a weighted average of the returns on the securities within the market, using beginning market values as weights. Each passive manager will obtain precisely the market return, before costs.”
- *supporting* ✓ (lines 10–11): “A passive investor always holds every security from the market, with each represented in the same manner as in the market.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`, `passive management`

> imported: Imported the definition of passive holding that explains why the equality follows, cited.

## 7. The proof: the market return is the value-weighted average of all securities, and passive managers earn exactly that return before costs. Because active and passive together exhaust the market, the actively managed dollars are the remainder, so their weighted average return must also equal the market return before costs.

**Role in the source.** The deductive core: the step from which the headline claim follows.

- *primary* ✓ (lines 19–20): “From this it follows that the return on the average actively managed dollar must equal the market return.”
- *supporting* ✓ (lines 17–19): “the market return will be a weighted average of the returns on the securities within the market, using beginning market values as weights. Each passive manager will obtain precisely the market return, before costs.”
- *supporting* ✓ (lines 11–11): “An active investor is one who is not passive.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`, `active management`

> imported: Resolved 'From this it follows' by citing both premises; the exhaustiveness step is licensed by the definition of active as not-passive.
