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

A chain does not always end in a sentence. Where the evidence carries an
`asset_ref`, say so and resolve it: a table cell reference gives the value **and
the headers governing it** (`2025` × `Net income (loss)`), which is the point —
quoting a flattened row proves the digits were copied, not that they were
assigned to the right column. Report the asset's `fidelity` alongside: an
`exact` asset came from the source's own markup, a `transcribed` one is a
reading of a page image and must not be compared as a string.

Assets related to the unit but not cited by it are worth a line too. They travel
with the entry because they sit in its text, and a consumer receiving the entry
receives them.

Flag these if present:
- any evidence marked `UNVERIFIED` — the excerpt was not matched verbatim to the
  source at extraction time
- a candidate whose `supersedes` field is set — the audit rewrote it, and the
  original is still on disk for comparison
- an assessment with low `subtype_confidence` being relied on for a strong claim
- an `asset_verified: false` reference — the cited cell or asset does not
  resolve, which means the citation points at nothing
