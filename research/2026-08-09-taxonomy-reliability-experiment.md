---
title: Taxonomy classification-reliability experiment (2x2 + gates)
date: 2026-08-09
status: RAN — result is INCONCLUSIVE, and that is the finding
---

# Classification Reliability — 5 arms x 3 blind raters x 35 items

Ran to answer one question: **is the kt-v1 taxonomy applied reproducibly, and is
it more reproducible than the 20-label ontology it replaced?**

**Headline: the experiment does not settle it.** Every arm scored high (α 0.88–1.00)
and every between-arm difference falls inside its bootstrap confidence interval.
The point estimates lean *against* the redesign. None of them is resolvable at this
sample size, so they cannot be cited in either direction.

## Design

- **Items**: 35 — 24 boundary cases from `docs/KNOWLEDGE-TYPE-TAXONOMY.md` §6
  (adversarially selected to sit on type edges) + 11 routine sentences taken from
  the shipped demo fixtures rather than written for this test.
- **Raters**: 3 per arm, blind — no repository access, no answer key, no knowledge
  of the other arms. Item order rotated per rater to neutralize position bias.
- **Primary metric**: Krippendorff's α (nominal) between raters. NOT agreement with
  the author's key: that key was written by whoever designed the scheme, so scoring
  against it measures self-consistency. It is reported as a labelled secondary.
- **Projection**: 20-label answers are mapped through `LEGACY_MAP` onto the six
  types, so arms with different vocabulary sizes are compared on where they *land*.
- α implementation validated against hand-computed arithmetic and both extremes
  (perfect = +1.000, independent random = −0.000, systematic disagreement < 0).

## Arms

| arm | vocabulary | definitions | mechanism |
|---|---|---|---|
| A | 20 legacy labels | none (bare enum — the shipped v2 condition) | one choice |
| B | 20 legacy labels | one line each | one choice |
| C | 6 types | none | one choice |
| D | 6 types | the shipped kt-v1 cue/negative/exemplar block | one choice |
| E | 6 types | same shipped block | 6 independent booleans → code priority |

## Results

| arm | α native | α→6 types | α family | unanimity | coverage |
|---|---|---|---|---|---|
| A_legacy20_bare | 0.959 | 0.974 | 0.969 | 0.971 | 1.000 |
| B_legacy20_taught | 0.979 | 1.000 | 1.000 | 1.000 | 1.000 |
| C_six_bare | 0.882 | 0.882 | 0.896 | 0.857 | 1.000 |
| D_six_taught | 0.954 | 0.954 | 0.970 | 0.943 | 1.000 |
| E_six_gates_taught | 0.908 | 0.908 | 0.944 | 0.886 | 1.000 |

| arm | α boundary (hard) | α routine |
|---|---|---|
| A_legacy20_bare | 1.000 | 0.920 |
| B_legacy20_taught | 1.000 | 1.000 |
| C_six_bare | 0.865 | 0.918 |
| D_six_taught | 0.967 | 0.922 |
| E_six_gates_taught | 0.901 | 0.912 |

## Comparisons — with bootstrap CIs (4000 item resamples)

| comparison | Δα | 95% CI | resolvable? |
|---|---|---|---|
| gates vs 6-way choice (E−D) | −0.068 | [−0.175, +0.024] | **no** — CI spans 0 |
| 6 types vs 20 labels, taught (D−B) | −0.048 | [−0.121, +0.000] | **no** — CI touches 0 |
| 6 types vs 20 labels, bare (C−A) | −0.094 | [−0.213, +0.020] | **no** — CI spans 0 |
| definitions on 6 types (D−C) | +0.074 | [−0.047, +0.201] | **no** — CI spans 0 |
| definitions on 20 labels (B−A) | +0.027 | [+0.000, +0.089] | **no** — CI touches 0 |

## What this does and does not establish

**Establishes:**

1. On this item set, *every* condition — including the bare 20-label enum the
   pipeline already shipped — reaches α ≥ 0.88. The premise that the legacy
   ontology needed replacing *for reliability* is not supported.
2. Raters differ on only 0–5 of 35 items. Behaviour is near-deterministic, which
   is a **ceiling effect**: the instrument cannot discriminate designs when all
   arms sit at the top of its range.
3. Gate behaviour is well-calibrated in absolute terms: multi-fire 1.9%,
   abstain 5.7%, mean 0.96 gates fired.

**Does not establish:**

1. That six independent gates beat one six-way choice. Point estimate runs the
   *wrong way* (−0.068, P(Δ>0) = 0.09) — this was the single most load-bearing
   design decision in the taxonomy document and it is now unsupported at best.
2. That six types beat twenty. Point estimate again runs the wrong way in both
   the taught and bare conditions.
3. Anything cross-model. All 15 raters are one model family. The Tier-2 finding
   that motivated the design — LLM–LLM κ 0.23 vs human–human κ 0.57 — is a
   *cross-family* result this experiment structurally cannot reproduce.

## Secondary — agreement with the author's key (boundary items only)

Self-consistency, not reliability. The 20-label arms score low here mostly because
`LEGACY_MAP` projection is lossy, not because the raters were wrong.

| arm | agreement |
|---|---|
| A_legacy20_bare | 0.458 |
| B_legacy20_taught | 0.458 |
| C_six_bare | 0.889 |
| D_six_taught | 0.847 |
| E_six_gates_taught | 0.806 |

## What would actually settle it

Not a bigger version of this. Reliability of a label that changes no answer is
irrelevant, and `unit_type` still has zero branches in the codebase. The measurement
with decision value is the one both review panels ranked first and this experiment
was **not**: the downstream answer-change ablation — typed-filtered retrieval vs
plain hybrid over a real corpus, graded blind, against an untyped long-context
baseline. If labels change no answer, their α does not matter.

If reliability is measured again, it needs: n ≈ 300 items, ≥5 raters, and
**multiple model families** — without which it measures determinism, not agreement.
