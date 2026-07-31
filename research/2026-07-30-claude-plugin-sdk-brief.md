# Claude Code Plugin + Anthropic SDK Brief (2026-07-30)

Implementation-facing research gathered by a claude-code-guide agent, July 30 2026.
Informs the plugin structure and SDK usage in this repo. Companion to the design
research in this folder.

## 1. Claude Code plugin anatomy

`plugin.json` (paths relative to plugin root):

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "...",
  "author": "...",
  "skills": ["./skills"],
  "agents": ["./agents"],
  "hooks": ["./hooks/config.json"],
  "mcpServers": ["./mcp/servers.json"],
  "defaultEnabled": true
}
```

- Required fields: `name`, `version`, `description`, `author`.
- Folder layout: `skills/<skill-name>/SKILL.md` (+ bundled scripts in the skill
  folder), shared code in `lib/`. Skills auto-discovered under `skills/`.
- Install flow: `claude plugin install <url>` or marketplace add; plugins are
  discovered from GitHub repos or local paths.
- `${CLAUDE_PLUGIN_ROOT}` — CONFIRMED locally (2026-07-30) against the official
  `plugin-dev` plugin: environment variable resolving to the plugin's absolute
  directory; always use it for portable paths to bundled scripts/config. The
  research agent had flagged it unconfirmed; local ground truth at
  `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/`
  (includes a `plugin-structure` skill — consult at build time).

## 2. SKILL.md frontmatter

```yaml
---
name: extract-knowledge-units
description: Extract atomic knowledge units from normalized files
command: extract-knowledge
model: claude-sonnet-5
effort: high
permissions:
  - tool: bash
  - tool: read
visibility: private
---
```

Fields: `name`, `description`, `command` (slash command), `model`
(`default|sonnet|opus|haiku|fable` or full IDs), `effort` (`auto|low|high`),
`permissions` (pre-approved tools, optionally with path patterns), `visibility`,
`args` (JSON Schema for command arguments). Substitutions available in scripts:
`{{cwd}}`, `{{selectedFile}}`, `{{clipboard}}`.

## 3. Anthropic Python SDK (July 2026)

Model IDs and fit:

| Model | ID | Pipeline fit |
|---|---|---|
| Opus 5 | `claude-opus-5` | adversarial audit (highest reasoning) |
| Sonnet 5 | `claude-sonnet-5` | extraction / assessment sweet spot |
| Haiku 4.5 | `claude-haiku-4-5` | cheap filtering / routing |
| Fable 5 | `claude-fable-5` | top tier, limited availability |

Structured outputs — native now, two forms:

```python
# Pydantic
response = client.messages.parse(model="claude-sonnet-5", max_tokens=2048,
    messages=[...], response_type=KnowledgeUnit)
parsed = response.parsed

# Raw JSON schema
response = client.messages.create(model="claude-sonnet-5", max_tokens=2048,
    messages=[...],
    output_config={"format": {"type": "json_schema", "schema": {...}}})
```

- Supported schema features: object/array/scalars, `enum`, `const`, `anyOf`,
  `allOf`, local `$ref`, string formats, `required`,
  `additionalProperties: false`, `minItems` (0/1 only).
- NOT supported: recursive schemas, numeric `minimum`/`maximum`, string length
  constraints, external `$ref`.
- `response_format` is a back-compat alias for `output_config.format`.

Prompt caching: `system=[{"type":"text","text":..., "cache_control":{"type":"ephemeral"}}]`
(5-min TTL default; `"ttl": "1h"` variant exists).

Message Batches API: `client.beta.messages.batches.create(requests=[Request(custom_id=..., params=MessageCreateParamsNonStreaming(...))])`,
up to 100k requests/batch, **50% off both input and output tokens**. Fits Pass 1
extraction across many sources.

Retries: SDK auto-retries 408/409/429/5xx with backoff (`max_retries`, default 2).

**[CONFLICTING SOURCES]** Max output tokens: Opus 5 cited as 32k vs 128k;
Sonnet 5 / Haiku 4.5 as 8k vs 64k. Set `max_tokens` conservatively (4k–16k) and
verify empirically.

## 4. Agent SDK vs raw Anthropic SDK

- Raw SDK (`anthropic`): stateless request/response stages — normalization
  assist, extraction, assessment, audit. Simpler, cheaper, batchable.
- Tool Runner (`client.beta.messages.tool_runner()`): agentic loop over your own
  tools without hand-writing the while-loop; good middle ground when a stage
  needs raw-source escalation (fetch more context on demand).
- Claude Agent SDK (`claude-agent-sdk`): full harness (Read/Write/Bash tools,
  sessions, permissions). Only worth it for stages that must autonomously
  explore files.
- Recommendation for this pipeline: raw SDK (+ Batches where async OK) for all
  passes; consider Tool Runner for Pass 3/5 raw-source escalation.

## Sources

- code.claude.com/docs/en/plugins.md (plugin structure)
- platform.claude.com/docs/en/build-with-claude/structured-outputs
- platform.claude.com/docs/en/build-with-claude/prompt-caching
- platform.claude.com/docs/en/about-claude/pricing
- code.claude.com/docs/en/agent-sdk/overview
- github.com/anthropics/anthropic-sdk-python
- aiwiki.ai/wiki/anthropic_batches_api; dev.to (batch API cost); sitepoint.com
  (429 handling); augmentcode.com (Claude Code vs Agent SDK)
