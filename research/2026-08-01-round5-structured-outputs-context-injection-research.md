# Round 5 — Structured Outputs, Long-Context Batch Sizing, Prompt-Injection Defense

**Date:** 2026-08-01
**Informs:** spec §16 (batching), §18 (model prompting / structured output), §20 (security & trust boundaries).
**Method:** direct primary-source fetching with per-fact citation (NOT the 3-vote adversarial protocol used in rounds 1–4). These three angles were fetched but never verified across four workflow rounds — the claim budget was consumed by earlier angles each time. Facts below are sourced and quoted; treat as **[SOURCED]** tier, one level below rounds 1–4's **[VERIFIED]** tier.
**Companions:** rounds 1–4 verified-claim files + `2026-08-01-production-engineering-brief.md` in this folder.

---

## Topic 1 — Structured outputs / constrained decoding

### The 2024 alarm: "Let Me Speak Freely?" (Tam et al., arXiv 2408.02442, Aug–Oct 2024)

Claimed "a significant decline in LLMs' reasoning abilities under format restrictions." Three modes: JSON-mode (constrained decoding), FRI (format-restricting instructions), NL-to-Format (free text then convert).

Reasoning-task drops (GSM8K, text → JSON-mode):
- GPT-3.5-turbo 76.6% → 49.3%; Claude-3-Haiku 86.5% → 23.4%; LLaMA-3-8B 74.7% → 48.9%; Gemini-1.5-Flash 89.3% → 89.2% (no drop).
- Last Letter Concatenation: GPT-3.5-turbo 56.7% → 25.2%; LLaMA-3-8B 70.1% → 28.0%; **Gemini-1.5-Flash 65.4% → 77.0% (improved)**.

**Classification tasks moved the OTHER way** (this pipeline's actual workload):
- DDXPlus: Gemini 41.6% → 60.3%; Claude-3-Haiku 33.8% → 52.0%; GPT-3.5 44.1% → 55.5%; LLaMA-3-8B 12.0% → 23.4%.
- Sports Understanding: GPT-3.5 67.2% → 80.0%. MultiFin and Task280 near-flat.

The paper's own mitigations: looser schema (drop prescriptive field names), NL-to-Format decoupling, reformat-on-parse-error (+2–3% in high-error cases). (https://arxiv.org/html/2408.02442v3)

### The rebuttal: ".txt — Say What You Mean" (blog.dottxt.ai)

Five methodological critiques: (1) different prompts for structured vs unstructured arms; (2) the JSON-mode prompt **omitted the task description**; (3) an LLM used as "Perfect Text Parser" underperformed hand-written flexible regex; (4) the paper's own classification results contradict its headline; (5) JSON-mode (no guarantees) conflated with true constrained decoding.

Replication on Llama-3-8B-instruct — structured ≥ unstructured on all three: GSM8K 0.78 vs 0.77; Last Letter 0.77 vs 0.73; Shuffle Object 0.44 vs 0.41. Parser choice alone moved Last Letter 0.35 (strict regex) → 0.57 (AI parser) → 0.61 (flexible regex): **the reported degradation is partly a measurement artifact**. Matched prompts + proper Pydantic schema: NL structured 0.68, JSON unstructured 0.73, **JSON structured 0.77**. (https://blog.dottxt.ai/say-what-you-mean.html)

### 2026 arbitration: "The Format Tax" (Lee, D'Antoni, Berg-Kirkpatrick; arXiv 2604.03616, 2026-04-04)

10 models (6 open-weight + GPT-5-Nano, GPT-5.4-Nano, Claude-Haiku-4.5, Grok-4.1-Fast), 4 formats, math/science/logic/writing.

- Average drops: MATH-500 JSON −6.8 pp, XML −6.5, Markdown −4.2, LaTeX −4.0; GPQA JSON −5.7; ZebraLogic JSON −7.1; WritingBench LaTeX −6.8 to −18.6 pp.
- **Key decomposition:** the format-*requesting prompt* alone costs −3.9 pp; adding grammar-constrained decoding costs only **−1.6 pp more**. 92% of significant effects were prompt-level. Answer-flip rates: 25.9% with GCD vs 24.1% without.
- Measured mitigations: 2-turn (freeform → reformat) recovered accuracy in 42/72 comparisons, avg **+6.8 pp**, only 2 worsened. Extended thinking before formatted output recovered 43/72, avg **+9.2 pp**, but **11 (15%) worsened**.
- **Recent closed-weight models showed "near-zero or positive deltas"** — the tax is a current open-weight gap, not inherent. (https://arxiv.org/html/2604.03616v1)

### Supporting 2025–2026 work

- **Schema key wording is an instruction channel**: "changing only schema-key wording can substantially affect accuracy"; a CoT-style key helps only when its semantic gain exceeds grammar-projection distortion; schema-level and prompt-level channels interact non-additively (Le, arXiv 2604.14862). Per-benchmark deltas not in abstract [UNVERIFIED].
- **Small models pay a latency tax**: constrained decoding imposed 3.6×–8.2× latency and degenerate output (Gemma: 52.4% exact-duplicate outputs). Critically: **unconstrained naive prompting produced 0% JSON validity** across all models/datasets despite 77–85% task accuracy (Galeone et al., arXiv 2605.02363).
- **Constrained-only decoding fabricates near-miss entities in 9% of samples** in closed information extraction (vs 0% for a boosted hybrid) — a real, specific failure mode when constraining to enumerations (BoostCD, arXiv 2506.14901).
- JSONSchemaBench: 10K real-world schemas across six frameworks (arXiv 2501.10868). Per-framework compliance rates [UNVERIFIED].
- **PARSE reports up to 64.7% extraction-accuracy improvement** on SWDE by treating schemas as optimizable rather than static (arXiv 2510.08623).

### Bottom line — Topic 1

The 2024 "constrained decoding hurts" claim **has not survived**. 2026 consensus: the cost lives in the *format instruction*, not the decoder mask (−3.9 vs −1.6 pp); the original result was inflated by mismatched prompts and lossy parsing; and **for classification and extraction — this pipeline's workload — schema constraint is neutral-to-positive** (DDXPlus +11 to +18 pp). Evidence-backed mitigations: (a) a thinking/reasoning field before answer fields (+9.2 pp avg, 15% regression rate — measure per pass), (b) loose schemas over prescriptive ones, (c) treat field names as prompt text and tune them, (d) guard against near-miss fabricated enum values.

---

## Topic 2 — Long-context degradation and batch sizing

### Position effects — Lost in the Middle (Liu et al., arXiv 2307.03172, TACL 2024)

Performance "often highest when relevant information occurs at the beginning or end … significantly degrades when models must access relevant information in the middle." 20-document multi-doc QA, GPT-3.5-Turbo: **75.8% at position 1, 53.8% mid-context, 63.2% at position 20 — a 22 pp primacy-to-middle drop.** Mid-context performance fell **below its own 56.1% closed-book baseline** (worse than being given no documents). Explicitly long-context models show the same pattern.

### Effective vs claimed length — RULER (arXiv 2404.06654)

17 long-context models, 13 tasks: "almost all models exhibit large performance drops as the context length increases" despite near-perfect vanilla needle-in-haystack scores; **only half maintain satisfactory performance at 32K**.

### Remove lexical shortcuts — NoLiMa (arXiv 2502.05167)

13 models claiming ≥128K support. At 32K, **11 of 13 fell below 50% of their short-context baseline**. GPT-4o: 99.3% → 69.7% at 32K. Directly relevant: cross-document claim comparison is exactly the low-lexical-overlap case.

### Degradation on trivially simple tasks — Chroma "Context Rot" (2025-07-14)

18 models across Anthropic, OpenAI, Google, Alibaba. "Model performance varies significantly as input length changes, even on simple tasks." A single distractor measurably reduces accuracy; four compound it. **Shuffled haystacks outperform logically coherent ones.** LongMemEval focused prompts (~300 tokens) vastly outperform full ~113K-token prompts on the same question. On pure replication (repeat N words with one substitution): accuracy declined monotonically with length; GPT-4.1 refused 2.55% from ~2,500 words; Claude Opus 4 refused 2.89%; Gemini 2.5 Pro emitted random words from 500–750 words. (https://www.trychroma.com/research/context-rot)

### Direct evidence on items-per-prompt — the spec's actual question

- **Multi-instance processing** (Chen, Pilehvar, Camacho-Collados; arXiv 2603.22608, Apr 2026): "all LLMs follow a pattern of slight performance degradation for small numbers of instances (**approximately 20-100**), followed by a **performance collapse** on larger instance counts. Crucially … while context length is associated with this degradation, **the number of instances has a stronger effect**."
- **Batch classification at scale** (Pipal, Vogel, Wack, Esser; arXiv 2604.03684, 2026-04-07): 3,962 expert-labeled texts, 9 batch sizes {1…1000}, 8 models across 4 providers. **Six of eight models stayed within 2 pp of the single-item baseline through batch size 100.** Claude Haiku 4.5 most robust (max drop 1.1 pp). At b≥250 degradation became model-specific; at b=1000 two OpenAI reasoning models lost **27–36 points** with substantial parse failures. Recommended safe range **25–100**, with >80% token cost savings at b=25.

### Bottom line — Topic 2

The evidence **supports the spec's cap**, and 20–50 sits conservatively inside the empirically safe band. The most on-point finding — degradation starts ~20–100 instances and collapses beyond, with **instance count mattering more than token count** — confirms the spec is right to cap on *unit count* rather than context fraction alone. The 30–50% context reservation is separately justified: degradation is continuous rather than cliff-shaped and appears even on trivial copy tasks, effective length is ~half of claimed at 32K, and 11/13 models fall under half-baseline at 32K without lexical anchors.

**New design implication the spec must absorb:** with a 22 pp positional spread, items in the middle of a batch are systematically disadvantaged — **rotate or randomize item ordering across passes** rather than trusting a fixed order.

---

## Topic 3 — Indirect prompt-injection defense for document ingestion

### Spotlighting (Hines et al., arXiv 2403.14720)

Provenance-marking transformations of untrusted input. Aggregate: **baseline ASR >50% → <2%** with minimal task-efficacy loss.

Per-technique, document summarization on GPT-3.5-Turbo: baseline ~60%, **delimiting ~30%, datamarking 3.1%, encoding 0%**. Document Q&A datamarking: 8% (GPT-3.5-Turbo), 1% (GPT-4), 0% (text-davinci-003). Task impact (SQuAD, IMDB, SuperGLUE WiC/BoolQ): datamarking showed no detrimental effect; encoding was fine on GPT-4 but degraded GPT-3.5-Turbo. Authors recommend **datamarking as default, encoding only for high-capacity models**.

Note the shape: **delimiting alone only halves ASR — delimiters are the weakest layer.**

### Instruction Hierarchy (Wallace et al., arXiv 2404.13208)

Training models to selectively ignore lower-privileged instructions "drastically increases robustness — even for attack types not seen during training." System-prompt-extraction defense **+63%**; jailbreak robustness **+30%** on held-out attacks. Acknowledged limits: over-refusal regressions. Indirect injection via tool use claimed to generalize but **not separately quantified [UNVERIFIED]**.

### CaMeL (Debenedetti et al., arXiv 2503.18813)

A system layer around the LLM: control and data flow extracted from the *trusted query only*, so untrusted data cannot influence program execution; capability-based policies gate tool calls. AgentDojo: **77% of tasks solved with provable security guarantees vs 84% undefended** — a 7 pp utility cost. (The widely-cited 67% figure is from an earlier version [UNVERIFIED].)

**The design principle transfers even without tools: separate the trusted control path from untrusted content, and never let untrusted content determine what the system does.**

### Benchmarks and their limits

- **BIPIA** (arXiv 2312.14197, KDD 2025): LLMs "universally vulnerable"; root cause is that models cannot distinguish informational context from executable instruction. Black-box prompt defenses give "substantial mitigation"; fine-tuning drives ASR "near-zero" without quality loss. Per-model ASRs [UNVERIFIED].
- **AgentDojo** (arXiv 2406.13352): 97 tasks, 629 security test cases; existing attacks "break some security properties but not all."
- **InjecAgent** (arXiv 2403.02691): 1,054 test cases, 17 user tools, 62 attacker tools.
- **Benchmarks are saturating AND flawed** (arXiv 2510.05244, Oct 2025): a simple sanitizer firewall hit 0.02% ASR on AgentDojo with GPT-4o (67.68% benign utility) vs CaMeL's 0% ASR at 53.6% utility; ASB 68.75% → 16.33%; InjecAgent 8.30% → 0.30%. But the authors show ASB **inflates ASR ~8×** via forced tool injection (73.58% → 9.25% with free tool selection), AgentDojo's injections often render tasks unsolvable, and InjecAgent has **no utility metric at all**. Braille-encoded attacks still bypassed the firewall. Conclusion: "firewalls saturate current benchmarks, but this reflects weak evaluation frameworks rather than solved security."
- **Adaptive-attacker reality check (2026):** 464 participants, **272,000 attacks**, 41 real-world agent scenarios, 13 frontier models. Claude Opus 4.5 **0.5% ASR** (61 breaks / 12,000 attempts), Sonnet 4.5 1.0%, Haiku 4.5 1.3%, Kimi K2 4.8%, SecAlign 70B 5.5%, Gemini 2.5 Pro 8.5%. Meta's SecAlign scored 0.5% on InjecAgent and 1.9% on AgentDojo but **5.5% against live humans: static benchmarks understate real vulnerability by ~3–10×. No model was immune.** (https://theweatherreport.ai/posts/ipi-arena-benchmark/)

### Bottom line — Topic 3

**No — ingested text cannot be reliably prevented from steering an extractor.** The best frontier model under adaptive human attack still broke 0.5% of the time across 12,000 attempts; the best-defended open model broke 5.5%. **Plan for a nonzero, persistent injection rate rather than elimination.**

The pipeline's saving grace is architectural, and it is exactly the CaMeL principle: **LLM passes with no tool access and schema-constrained output have no action channel.** The only reachable harm is corrupted field values (wrong extraction, poisoned classification, injected text landing in a downstream record) — not exfiltration or execution. That collapses the threat from "agent hijack" to "data integrity."

Defense layering in order of measured payoff:
1. **Datamark the untrusted span** — highest-yield, lowest-cost layer (60% → 3.1% ASR, no measured task cost).
2. **Do not rely on delimiters alone** — they only halve ASR (~60% → ~30%).
3. **Keep the trusted instruction in the system/control path**; never let document text define the task (instruction hierarchy +63%; CaMeL principle).
4. **Constrain the output schema tightly** — enumerations and typed fields are themselves an injection sink; watch for near-miss fabricated values (9% rate in constrained closed-IE).
5. **Validate outputs downstream** — residual ASR is nonzero regardless.
6. **Do not trust a benchmark score as assurance** — static evals understate adaptive attacks by up to ~10× and have documented structural flaws.

Reserve encoding-based spotlighting for high-capability models only.
