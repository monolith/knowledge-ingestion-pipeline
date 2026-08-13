---
description: Ingest a folder of documents into audited, traceable knowledge units
argument-hint: <source-directory> [--stop-after <pass>]
allowed-tools: Bash, Read
---

Ingest documents from `$ARGUMENTS` using the knowledge-ingestion pipeline.

Steps:

1. Confirm the source directory exists and list what is in it, so the user knows
   what is about to be processed and roughly what it will cost.
2. Run `kip --workspace .kip auth` and report which credential tier resolved.
   It makes no API call, so this is free. An unset `ANTHROPIC_API_KEY` is NOT a
   failure — the pipeline also uses the Claude Code login, which is the normal
   case when running as a plugin. Stop only if that command exits non-zero
   (meaning no concrete credential resolved); do not go hunting for credentials
   anywhere else.

   If it resolved to `claude_code_oauth`, tell the user the run will draw on
   their Claude Code subscription rate limit and so competes with interactive
   sessions — that is the one surprise worth naming before a long run.
3. Run the pipeline:
   ```bash
   kip --workspace .kip run --sources <source-directory>
   ```
   If the user did not specify otherwise and the folder holds more than ~20
   files, run with `--stop-after extract` first and report the unit count before
   continuing — Pass 1 is the expensive pass.
4. Run `kip --workspace .kip validate <run-id>` and report any errors verbatim.
5. Summarize: sources processed, any quarantined, units extracted, clusters,
   assessments by bucket, audit verdicts, and queue events.
6. Report the ASSETS separately, because they are the part a text-shaped summary
   drops: how many tables, formulas and figures were recovered, at what
   fidelity, and how many are **orphaned** — sitting in a passage that produced
   no units. An orphaned asset is not a filing error; it is a hole in the
   reading, and on a dense document it is the most informative number in the
   run. `06_audit/corpus_coverage.json` carries the judgment on whether their
   absence misrepresents the corpus.

If the user has no API credential, or wants to answer the calls themselves, run
with `--mode handoff` instead: the pipeline writes each request to
`_handoff/pending.jsonl` and exits 10, and you answer by appending
`{"call_id": ..., "response": {...}}` to `_handoff/responses.jsonl` and
re-running. Answers are schema-checked on the way in.

When reporting results, carry the pipeline's own uncertainty through rather than
flattening it: coarse relationship buckets are reliable, fine subtypes are
advisory, and a missing contradiction flag is not evidence of consistency.
Report what the audit changed — the diff between initial and approved candidates
is the most informative part of a run.
