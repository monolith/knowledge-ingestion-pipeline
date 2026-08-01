# Production-Engineering Evidence Brief (2026-08-01)

**Informs:** spec §7 (Pass 0 normalization), §13 (queue handoff), §16 (batching), §17 (orchestration).
**Method:** direct fetches of primary sources by a research agent (WebSearch unavailable that session — all facts from primary-URL fetches; absence-of-evidence notes are scoped to fetched sources). NOT adversarially verified, unlike the round 1–4 claim sets; every fact cites its primary source and most are vendor/first-party documentation, i.e. authoritative for what the vendor's own system does.
**Companions:** rounds 1–4 verified-claim files in this folder + `2026-07-30-claude-plugin-sdk-brief.md`.

## Topic 1 — Multi-agent vs single-agent division of labor (§17)

- Anthropic "How we built our multi-agent research system" (2025-06-13,
  anthropic.com/engineering/built-multi-agent-research-system):
  - Multi-agent (Opus 4 lead + Sonnet 4 subagents) beat single-agent Opus 4 by
    **90.2%** on Anthropic's internal breadth-first research eval (relative
    improvement on that eval, not generic accuracy).
  - **Token economics: multi-agent ≈ 15× chat tokens** (agents generally ≈ 4×).
    On BrowseComp, token usage alone explained 80% of performance variance.
  - Worth it when: heavy parallelization, information exceeding one context
    window, many complex tools. NOT worth it when: agents must share context or
    have many inter-dependencies (explicitly "most coding tasks"), or value
    doesn't justify token cost.
  - Orchestrator-worker mechanics: 3–5 parallel subagents on complex queries;
    parallel tool calls cut research time up to 90%; explicit effort-scaling
    heuristics (simple query = 1 agent / 3–10 tool calls).
- "Effective context engineering for AI agents" (2025-09-29): subagents explore
  in isolated contexts and return condensed 1,000–2,000-token summaries;
  compaction + structured note-taking outside the window.
- "Effective harnesses for long-running agents" (2025-11-26): for multi-session
  work compaction isn't sufficient — initializer agent, JSON feature list,
  progress files + git history as durable state, one-feature-at-a-time.
- 2026 follow-ups exist (titles verified from the engineering index, contents
  not fetched): parallel-Claudes C compiler (2026-02-05), harness design
  (2026-03-24), Managed Agents scaling (2026-04-08).
- **Caveat:** the 90.2% figure is mid-2025 models on an internal eval; the
  later harness posts shift emphasis toward single-agent + state artifacts for
  dependency-heavy work. Weigh both.

## Topic 2 — Document parsing tooling for Pass 0 (§7)

**Docling** (IBM Research → LF AI & Data; MIT license; arXiv 2408.09869,
2024-08-19, v5 2024-12-09; docling-project.github.io/docling):
- Formats: PDF, DOCX, PPTX, XLSX, HTML, EPUB, images (PNG/TIFF/JPEG), audio
  (WAV/MP3), video, LaTeX, email (EML/MSG), plain text; OCR for scanned
  input; VLM support (GraniteDocling). (2024 tech report covers PDF path only.)
- Layout: RT-DETR-derived detector trained on DocLayNet+proprietary data (ONNX,
  72 DPI); TableFormer for table structure (2–6 s/table on CPU).
- Speed: 1.27–1.34 pages/s (M3 Max), 0.60–0.92 pages/s (Xeon E5-2690), 225-page
  set. Tech report publishes NO accuracy/F1 metrics.
- **Provenance — the decisive fact for this spec:** every `DocItem` carries
  `prov`: `page_no`, `bbox` (l/t/r/b + coord_origin), `charspan`
  (docling-project.github.io/docling/reference/docling_document/). This is the
  exact per-element provenance the spec's locator_map (§7.6) requires.

**OmniDocBench** (arXiv 2412.07626, CVPR 2025; github.com/opendatalab/OmniDocBench):
- Paper v2 overall edit distance (lower better, EN/ZH): MinerU 0.15/0.357;
  Mathpix 0.191/0.365; **Marker 0.336/0.556**; GPT-4o 0.233/0.399.
- Current leaderboard: MinerU 0.055 text-edit; Marker 0.157; specialist VLMs
  lead (PaddleOCR-VL 0.0326, MinerU2.5-Pro 0.036).
- **Docling and unstructured absent from fetched OmniDocBench tables** — any
  "Docling wins parsing benchmarks" claim is [UNVERIFIED]. Verified picture:
  MinerU decisively beats Marker; Docling's differentiators are the typed
  provenance-preserving document model, format breadth, CPU-feasible speed,
  and MIT/LF governance — not benchmark supremacy.

## Topic 3 — Durable execution & idempotency (§13, §17)

**Transactional outbox** (microservices.io/patterns/data/transactional-outbox.html):
- Solves the dual-write problem (atomically update DB + publish message)
  without 2PC: message written to an outbox table in the same transaction as
  the business update; a relay (log tailing or polling) publishes it.
- Guarantees: sent iff the transaction commits, in commit order; relay "might
  publish a message more than once" ⇒ **at-least-once + consumer-side dedup by
  message ID** — matching the spec's idempotency_key + acknowledge-by-event-ID.

**Temporal** (docs.temporal.io; blog 2024-02-27; temporal.io/solutions/ai):
- Durability via event-history replay: on crash the worker replays history to
  the last successful point; completed activities (`ActivityTaskCompleted`) are
  not re-executed.
- At-least-once activity execution ⇒ activities must be idempotent; recommended:
  idempotency keys/request IDs + destination dedup (unique-constraint table).
- Determinism requirement for workflow code (side effects in activities only) is
  standard Temporal doctrine but [UNVERIFIED from these fetches].
- AI case studies (vendor page, undated): Replit coding agent, Retool Agents,
  Gorgias ("All LLM use cases are workflows"); pitched features: state
  persistence, retries, human-in-the-loop, observability.

## Topic 4 — Anthropic Message Batches economics (§16)

Official doc platform.claude.com/docs/en/build-with-claude/batch-processing.md
(fetched 2026-08-01; pricing.md 404'd — batch doc's own table is the source):
- **50% of standard prices on BOTH input and output** (e.g. Sonnet 4.6 batch
  $1.50/$7.50 per MTok; Opus 4.8 $2.50/$12.50; Haiku 4.5 $0.50/$2.50).
- Limits: 100,000 requests or 256 MB per batch; most complete <1 h; results at
  full completion or 24 h cutoff (unprocessed requests expire unbilled);
  results downloadable 29 days; arbitrary order — match by `custom_id`.
- **Prompt-caching discounts STACK with batch discounts**; cache hits
  best-effort (30–98% observed); use 1-hour TTL for shared-context batches;
  `max_tokens: 0` pre-warm not allowed in batches.
- Rejected in batches: `stream: true`, fast mode, thread params. Server tools
  work. Beta header `output-300k-2026-03-24` raises max_tokens to 300k
  batch-only at batch pricing.
