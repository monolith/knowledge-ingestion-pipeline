# 00-full-pipeline

Rendered from `runs/demo-full/` — the run tree kip wrote. Everything below is in those artifacts; nothing is added here.

**Source.** demo/sources/ — a randomized trial and a practitioner review that disagree about the same effect, both written for this repo.

**This is the structural reference, not a model demonstration.** It is the only run here taken through all seven passes, so it is the one whose tree matches [What a run writes](../../../README.md#what-a-run-writes) in full. Its model calls were answered by the canned transcript in `demo/run_demo.py`, driven through the real CLI — so the *structure* is exactly what `kip run` produces, while the *content* is fixture data. For real model output read runs 01-04.

- source: 206 words across 2 documents
- units: 10  (one per 20 words)
- omissions flagged: 1

## 1. Delayed recall is the proportion of learned items a participant reproduces after a retention interval of twelve hours or more.

- *primary* ✓ (lines 5–5): “Delayed recall is the proportion of learned items a participant reproduces after a retention interval of twelve hours or more.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: None needed; the sentence already stands alone.

## 2. Hippocampal replay during slow-wave sleep strengthens cortical traces, so shortening slow-wave sleep reduces next-day recall.

- *primary* ✓ (lines 9–9): “Hippocampal replay during slow-wave sleep strengthens cortical traces, so shortening slow-wave sleep reduces next-day recall.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: None needed; the mechanism is stated in full.

## 3. An independent replication of the sleep-extension protocol found no statistically significant effect on delayed recall.

- *primary* ✓ (lines 13–13): “An independent replication of the sleep-extension protocol found no statistically significant overall effect on delayed recall.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: Named the protocol that was replicated.

## 4. Participants must not consume caffeine within eight hours of a scheduled sleep session.

- *primary* ✓ (lines 17–17): “Participants must not consume caffeine within eight hours of a scheduled sleep session.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: None needed; the actor and the constraint are explicit.

## 5. To score the delayed-recall task, count the correctly reproduced items and divide by the number of items presented at learning.

- *primary* ✓ (lines 18–18): “To score the recall task, count the correctly reproduced items and divide by the number of items presented at learning.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: Named the task being scored.

## 6. A randomized trial assigned 42 healthy adults to a nine-hour sleep opportunity or their habitual schedule for four weeks.

- *primary* ✓ (lines 5–5): “The trial randomized 42 healthy adults to a nine-hour sleep opportunity or to their habitual schedule over four weeks.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: Named the design and the population.

## 7. Delayed word recall improved 8.2% in the sleep-extension group versus 1.1% in controls.

- *primary* ✓ (lines 10–10): “Delayed word recall improved 8.2% in the extension group versus 1.1% in controls.”

grounding: `attributable` · decision: `keep` · quantitative: `True`

> imported: Named the intervention explicitly.

## 8. Total sleep time rose by 47 minutes per night in the sleep-extension group.

- *primary* ✓ (lines 11–11): “Total sleep time rose by 47 minutes per night in the extension group.”

grounding: `attributable` · decision: `keep` · quantitative: `True`

> imported: Named the group the increase applies to.

## 9. The sleep-extension trial was not blinded and followed participants for only four weeks, so durability beyond one month is unknown.

- *primary* ✓ (lines 15–15): “The trial was not blinded, and follow-up lasted only four weeks, so durability beyond one month is unknown.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: Named the trial the limitation applies to.

## 10. Whether sleep extension improves delayed recall in adults over sixty-five is untested.

- *primary* ✓ (lines 19–19): “Whether the same effect holds in adults over sixty-five remains untested.”

grounding: `attributable` · decision: `keep` · quantitative: `False`

> imported: Named the intervention and the untested population.

## What the omission check said was missing

- **missing** — The baseline measurement occasion is not represented as a unit.
