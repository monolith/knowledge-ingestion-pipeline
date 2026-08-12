# Verifying this run

This run is complete: `source.md` is the normalized text every excerpt was cut
from, so the fastest check is to open it and search for any quote in `UNITS.md`.
The rest of this file is for checking the run mechanically rather than by eye.

The source is the JSTOR scan of De Bondt & Thaler (1985), *The Journal of
Finance* 40(3), pp. 793–805, [stable URL
2327804](http://www.jstor.org/stable/2327804).

## The digests

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

## Reproducing it from the original PDF

`source.md` is Pass 0's output, not the original. To check that Pass 0 itself is
faithful, obtain the article and re-run it:

```bash
# 0. Fastest check, no PDF needed: every excerpt sits at its recorded offsets.
python - <<'EOF'
import json, pathlib
txt = pathlib.Path("source.md").read_text()
bad = [e for l in pathlib.Path("units.jsonl").read_text().splitlines()
       for e in json.loads(l)["evidence"]
       if txt[e["normalized_char_start"]:e["normalized_char_end"]] != e["excerpt"]]
print(f"{len(bad)} mismatches" if bad else "all 82 excerpts verified")
EOF

# 1. Confirm you have byte-identical input.
sha256sum your-copy.pdf     # must equal original_sha256 above

# 2. Re-normalize. No model call, no API key: Pass 0 is deterministic.
kip --workspace /tmp/dt run --sources <dir-with-the-pdf> \
    --run-id dt1 --stop-after normalize

# 3. Confirm the normalized text matches.
sha256sum /tmp/dt/runs/dt1/01_normalized/*/normalized.txt   # == normalized_sha256

# 4. Confirm Pass 0 reproduced this run's source.md byte for byte.
diff /tmp/dt/runs/dt1/01_normalized/*/normalized.txt source.md && echo identical
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
