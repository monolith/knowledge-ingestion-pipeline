# Verifying this run without the source document

Runs 01–03 ship their `source.md`, so you can search it for any quote in
`UNITS.md` and confirm the ✓ yourself. This run does not ship its source, so
that check is not available here — and a ✓ you cannot check is worth very
little. This file is how you check it anyway.

## Why the text is absent

Two of the files a complete run would carry hold the entire article:

- `source.md` — the normalized full text, 6,284 words.
- `handoff-requests.jsonl` — each model request embeds the whole document in its
  user message. (Compare `03-spec-long/handoff-requests.jsonl`, 260 KB for a
  document whose `source.md` is 78 KB.)

De Bondt & Thaler (1985) is a copyrighted journal article. The 82 excerpts in
`units.jsonl` are short, non-contiguous, and each is attached to commentary
about its role in the argument — ordinary quotation. Reproducing the article in
full in a public repository is a different act, so neither file is here.

## What is here instead

`manifest.json` carries the two digests Pass 0 recorded:

| field | value |
|---|---|
| `original_sha256` | `d07fdf649a652f21723eff6f37559d7481eea6fee4e661fa614d1663a0faeb67` |
| `normalized_sha256` | `fb2f88dc5352f7d18838610ce0885054c6f948c3ef29a577743b018f7333e694` |
| `normalizer` | `rich_v1` 1.0.0 |
| `normalized_line_count` | 592 |

Every excerpt in `units.jsonl` additionally records `normalized_char_start`,
`normalized_char_end`, `normalized_line_start` and `normalized_line_end` against
that exact normalized text. The 82 spans run from character 2,993 to 35,559.

## Reproducing it

Obtain the article yourself — the run used the JSTOR scan of
*The Journal of Finance* 40(3), pp. 793–805, [stable URL
2327804](http://www.jstor.org/stable/2327804) — then:

```bash
# 1. Confirm you have byte-identical input.
sha256sum your-copy.pdf     # must equal original_sha256 above

# 2. Re-normalize. No model call, no API key: Pass 0 is deterministic.
kip --workspace /tmp/dt run --sources <dir-with-the-pdf> \
    --run-id dt1 --stop-after normalize

# 3. Confirm the normalized text matches.
sha256sum /tmp/dt/runs/dt1/01_normalized/*/normalized.txt   # == normalized_sha256

# 4. Check every excerpt lands where the unit says it does.
python - <<'EOF'
import json, pathlib
txt = next(pathlib.Path("/tmp/dt/runs/dt1/01_normalized").rglob("normalized.txt")).read_text()
bad = 0
for line in pathlib.Path("units.jsonl").read_text().splitlines():
    for e in json.loads(line)["evidence"]:
        if txt[e["normalized_char_start"]:e["normalized_char_end"]] != e["excerpt"]:
            bad += 1
            print("MISMATCH", e["excerpt"][:60])
print("all excerpts verified" if not bad else f"{bad} mismatches")
EOF
```

If step 1 fails your scan differs from the one used here, and steps 3–4 will not
match — that is the check working, not a bug.

## Replaying the model calls

`handoff-answers.jsonl` holds both answers keyed by content-addressed `call_id`
(`3444e75241f9eda8` for extraction, `dd2a5b7e71731ba9` for the omission check).
Copy it to `_handoff/responses.jsonl` in a workspace whose Pass 0 output matches
the digest above, re-run with `--mode handoff`, and the call ids will match and
the answers will be served as cache hits — reproducing `units.jsonl` and
`omissions.jsonl` exactly, with no model and no API key.

If the call ids do *not* match, the request changed: a different source, a
different prompt version, or a different schema. That is the protocol working as
designed.
