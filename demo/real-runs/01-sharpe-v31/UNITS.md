# 01-sharpe-v31

Rendered from `runs/sharpe/` — the run tree kip wrote. Everything below is in those artifacts; nothing is added here.

- source: 223 words
- units: 9  (one per 24 words)
- omissions flagged: 2

## 1. Before costs, the return on the average actively managed dollar will equal the return on the average passively managed dollar.

- *primary* ✓ (lines 4–5): “before costs, the return on the average actively managed dollar will equal the return on the average passively managed dollar”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `passive management`, `market arithmetic`

> imported: Kept as written; already standalone.

## 2. After costs, the return on the average actively managed dollar will be less than the return on the average passively managed dollar.

- *primary* ✓ (lines 5–7): “after costs, the return on the average actively managed dollar will be less than the return on the average passively managed dollar”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `costs`

## 3. The two propositions about active and passive returns hold for any time period and depend only on the laws of addition, subtraction, multiplication and division.

- *primary* ✓ (lines 7–8): “These assertions will hold for any time period. Moreover, they depend only on the laws of addition, subtraction, multiplication and division.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`

> imported: Resolved 'These assertions' to the two propositions about active and passive returns.

## 4. A passive investor always holds every security from the market, with each security represented in the same proportion as in the market.

- *primary* ✓ (lines 10–11): “A passive investor always holds every security from the market, with each represented in the same manner as in the market.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `passive management`, `definitions`

## 5. An active investor is an investor who is not passive, and an active investor's portfolio differs from that of passive managers at some or all times.

- *primary* ✓ (lines 11–12): “An active investor is one who is not passive. Her portfolio will differ from that of the passive managers at some or all times.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `definitions`

> imported: Resolved 'Her portfolio' to an active investor's portfolio.

## 6. Active managers trade fairly frequently because they act on perceptions of mispricing and such perceptions change relatively frequently.

- *primary* ✓ (lines 12–14): “Because active managers usually act on perceptions of mispricing, and because such perceptions change relatively frequently, such managers tend to trade fairly frequently”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `active management`, `trading costs`

## 7. Over any specified time period, the market return is a weighted average of the returns on the securities within the market, using beginning market values as weights.

- *primary* ✓ (lines 17–18): “Over any specified time period, the market return will be a weighted average of the returns on the securities within the market, using beginning market values as weights.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`, `definitions`

## 8. Each passive manager obtains precisely the market return, before costs.

- *primary* ✓ (lines 18–19): “Each passive manager will obtain precisely the market return, before costs.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `passive management`

## 9. Because each passive manager obtains the market return and the market return is a weighted average of all securities, the return on the average actively managed dollar must equal the market return.

- *primary* ✓ (lines 19–20): “From this it follows that the return on the average actively managed dollar must equal the market return.”

grounding: `—` · decision: `keep` · quantitative: `False` · topics: `market arithmetic`, `active management`

> imported: Resolved 'From this it follows' to the two premises it depends on.

## What the omission check said was missing

- **missing** — The argument is stated as conditional on active and passive management being defined in sensible ways. That precondition scopes every subsequent claim and is not represented in any unit.
- **missing** — The claim that nothing beyond elementary arithmetic is required is a distinct strengthening of the dependency claim, asserting sufficiency rather than merely listing what is used.
