---
description: Trace a knowledge-base claim back to its original source text
argument-hint: <run-id> <candidate-id | queue-event-id | unit-id>
allowed-tools: Bash, Read
---

Trace the provenance chain for `$ARGUMENTS`.

```bash
kip --workspace .kip trace <run-id> <target>
```

Then explain the chain in plain language: what the claim says, which
assessment(s) it rests on, how many *independent* evidence groups support it
(not how many documents — two files describing one study are one piece of
evidence), what the audit changed, and the exact quoted excerpt in the original
file.

Flag these if present:
- any evidence marked `UNVERIFIED` — the excerpt was not matched verbatim to the
  source at extraction time
- a candidate whose `supersedes` field is set — the audit rewrote it, and the
  original is still on disk for comparison
- an assessment with low `subtype_confidence` being relied on for a strong claim
