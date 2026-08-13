# andersen-the-little-mermaid

A complete run of the `kip` ingestion pipeline over `the little mermaid`.

**42 knowledge units** · **108 citations** (108 verified) · **7 entries handed off** · run `mermaid` · schema `3.1.0`

---

## Reading this folder

**If you are a person:** the [entries](#the-knowledge-handed-off) below are the output — what a knowledge base would receive. The [assets](#assets) are the tables, formulas and page images recovered from the source, shown as they are stored.

**If you are a model asked to ingest this run, do not work from this file.** It is a rendering and it is lossy. Read, in order:

1. [`runs/mermaid/07_enqueue/enqueue.jsonl`](runs/mermaid/07_enqueue/enqueue.jsonl) — **the handoff.** One JSON event per approved entry, each with `payload.title`, `payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This is the only file you need in order to ingest; everything below is for checking what it says.
2. [`runs/mermaid/02_units/units.jsonl`](runs/mermaid/02_units/units.jsonl) — the evidence. Each unit carries verbatim excerpts with character offsets into `normalized.txt`, and `asset_ref` where the evidence is a table cell or a formula. Follow `payload.source_unit_ids` from an entry to get here.
3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. **Check `fidelity` before you trust a comparison:** `exact` came from the source's own markup and can be compared as a string; `transcribed` was read off an image and must not be.
4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset citation resolves against, by character offset.
5. [`runs/mermaid/00_original_sources/`](runs/mermaid/00_original_sources) — the raw source, unmodified. Go here when you need to check the pipeline itself.

Everything else records how the output was arrived at: the routing, the judgments, the candidates before audit, and the audit findings.

## What is in each folder

| folder | contents |
|---|---|
| [`00_original_sources`](runs/mermaid/00_original_sources) | The source documents exactly as ingested, byte for byte. |
| [`01_normalized`](runs/mermaid/01_normalized) | One directory per source: `normalized.txt` (the flat text every citation resolves against), `assets.jsonl` (tables, formulas and figures the flat text could not hold), `manifest.json`, and `assets/` for any rendered page images. |
| [`02_units`](runs/mermaid/02_units) | `units.jsonl` — every extracted knowledge unit with its verbatim evidence and character offsets. `omissions.jsonl` — what the completeness check found missing. `rejects.jsonl` if any record failed materialization. |
| [`03_clusters`](runs/mermaid/03_clusters) | Which units were routed together for comparison, and why. |
| [`04_assessments`](runs/mermaid/04_assessments) | One judgment per claim: does the evidence support it, contradict it, or settle nothing, and how many INDEPENDENT sources it rests on. |
| [`05_candidates`](runs/mermaid/05_candidates) | Proposed knowledge-base entries, before audit. |
| [`06_audit`](runs/mermaid/06_audit) | `audits.jsonl` — the adversarial review of each candidate, with deterministic check results. `corpus_coverage.json` — whether the output fairly represents the whole corpus. |
| [`07_enqueue`](runs/mermaid/07_enqueue) | **`enqueue.jsonl` is the handoff.** One idempotent event per approved entry. This is the file a consuming knowledge base reads. |
| [`_handoff`](runs/mermaid/_handoff) | The complete record of every model call: `pending.jsonl` holds the requests, `responses.jsonl` the answers. Copying `responses.jsonl` into a fresh workspace replays the entire run from cache. |

## Does the output represent the corpus?

The run's own corpus-coverage audit returned **`represented`**.

> The conditional and quantitative content is carried rather than paraphrased. A reader can apply the soul conditions and the bargain's failure clause from the output alone, which is what lets them see that the ending follows the rules rather than breaking them.

> The causal chain from rescue to misattribution to marriage survives in order and across two entries. It is the story's mechanism, and a summary would have kept the events and lost the dependency between them.

> The refusal of the knife is presented with the escape's mechanism, price and deadline attached, so it reads as a choice rather than as resignation. That distinction is the story's moral content.

> Six units the first extraction pass missed were recovered by the repair round and all six reached assertions -- the sisters' sequence, the tears rule, the price of rank, the voice's valuation, the family at the surface, and the potion's effect on the polypi. Three of them are setup that pays off in later entries.

Full judgment: [`06_audit/corpus_coverage.json`](runs/mermaid/06_audit/corpus_coverage.json).

## What the checks found

- The completeness check reported **7 finding(s)** against the first extraction: [`02_units/omissions.jsonl`](runs/mermaid/02_units/omissions.jsonl).
- The adversarial audit reviewed **7 candidate(s)** and passed 6 without requiring a correction: [`06_audit/audits.jsonl`](runs/mermaid/06_audit/audits.jsonl).

## Assets

None. This source carried no tables, formulas or figures — the flat text in `01_normalized/` is the whole of it. An empty asset bundle is a result, not a gap.

## The knowledge handed off

Rendered from [`07_enqueue/enqueue.jsonl`](runs/mermaid/07_enqueue/enqueue.jsonl) — 7 event(s), target `existing-leaf-engine`.

---

### 1. The rules of the sea kingdom in 'The Little Mermaid'

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-001-r1` v2

**Slug** `the-rules-of-the-sea-kingdom-in-the-little-mermaid`

The world Andersen states before anything happens in it: who lives there, what they may do and when, what rank costs, and what merpeople cannot do. These are the terms the rest of the story spends, and they are stated as fact by characters who know them.

**Assertions (5)**

1. A mermaid may rise to the surface of the sea only on reaching her fifteenth year, and may then sit on the rocks in the moonlight and see ships, forests and towns. The six sea-princesses are each a year apart, so the youngest waits five years longer than the eldest.

   *backed by* `asmt-0001`

2. Rank is displayed and paid for. The Sea King's mother wears twelve oysters on her tail by right of high birth where others of high rank wear six; the little mermaid is given eight on her fifteenth birthday, and when she says they hurt, the answer is that pride must suffer pain.

   *backed by* `asmt-0001`, `asmt-0009`

3. Merpeople have no tears, and the story states that they therefore suffer more.

   *backed by* `asmt-0001`, `asmt-0009`

4. Each of the five elder sisters surfaces in turn and reports a different sight as the most beautiful. Once grown and free to go whenever they please, all five become indifferent to the surface and prefer home -- which is what makes the youngest's longing a difference in kind rather than degree.

   *backed by* `asmt-0001`

5. The Sea King is a widower; his mother keeps house and raises his six grand-daughters; the youngest is quiet and thoughtful and cares for little but her red flowers and a marble statue of a boy that fell from a wreck.

   *backed by* `asmt-0001`

**Related topics** `fairy tales`, `Hans Christian Andersen`, `world-building`, `rank`

**Labels**

- Mark the assertions as statements within the story rather than about the world.

**Source units (8)** `u-src-the-little-mermaid-df5d02e6-0001`, `u-src-the-little-mermaid-df5d02e6-0002`, `u-src-the-little-mermaid-df5d02e6-0003`, `u-src-the-little-mermaid-df5d02e6-0004`, `u-src-the-little-mermaid-df5d02e6-0005`, `u-src-the-little-mermaid-df5d02e6-0037`, `u-src-the-little-mermaid-df5d02e6-0038`, `u-src-the-little-mermaid-df5d02e6-0039`

**Traceability** — idempotency key `98a2861b042c08348d99214c6f2aaeede417eecd5c734111467961f057660527` · queue event `q-98a2861b042c0834` · audits `audit-cand-001`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 2. Why the prince never knows who saved him

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-002-r1` v2

**Slug** `why-the-prince-never-knows-who-saved-him`

The causal chain that decides the story. Each step is the precondition of the next, and the misattribution at the end of it is a consequence of what the little mermaid is rather than an accident of plot.

**Assertions (4)**

1. On her fifteenth birthday the little mermaid surfaces and sees a three-masted ship where a prince of sixteen is celebrating his birthday.

   *backed by* `asmt-0002`

2. A storm wrecks the ship. Knowing that human beings cannot live in the water, she reaches the prince as he is losing the power of swimming, holds his head above water, and lets the waves carry them.

   *backed by* `asmt-0002`

3. She lays him on a beach near a large white building with his head raised, then hides among the rocks with her face covered in sea-foam so as not to be seen.

   *backed by* `asmt-0002`

4. A young girl from the building finds him and fetches help. Because the mermaid stayed hidden, the prince never learns who saved him -- and the girl who was seen finding him is the one he believes did.

   *backed by* `asmt-0002`

**Related topics** `shipwreck`, `rescue`, `mistaken identity`

**Labels**

- Link to the failure entry, where this chain closes.

**Source units (4)** `u-src-the-little-mermaid-df5d02e6-0006`, `u-src-the-little-mermaid-df5d02e6-0007`, `u-src-the-little-mermaid-df5d02e6-0008`, `u-src-the-little-mermaid-df5d02e6-0009`

**Traceability** — idempotency key `ec2d922dff85a8c850818a128fb6731e40de30ec286274e52d606450f7d1f210` · queue event `q-ec2d922dff85a8c8` · audits `audit-cand-002`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 3. Souls: what a mermaid has, what a human has, and the one way to cross

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-003-r1` v2

**Slug** `souls-what-a-mermaid-has-what-a-human-has-and-the-one-way-to-cross`

The rule system the whole story turns on, set out by the grandmother in answer to a direct question. The conditions are given in operative form, which is what allows the ending to be checked against them rather than merely felt.

**Assertions (5)**

1. Merpeople sometimes live to three hundred years, but when they cease to exist they become foam on the surface of the water and have not even a grave for those they love. They have no immortal souls and will never live again -- like sea-weed once cut off, they can never flourish more.

   *backed by* `asmt-0003`

2. Human beings have a shorter term of life but a soul that lives forever, living on after the body has turned to dust and rising beyond the stars to regions merpeople will never see.

   *backed by* `asmt-0003`

3. There is exactly one way for a mermaid to obtain an immortal soul, and every clause binds: a man must love her so much that she is more to him than his father or mother; all his thoughts and all his love must be fixed upon her; and a priest must place his right hand in hers while he promises to be true to her here and hereafter. Then his soul glides into her body and she gains a share in the future happiness of mankind, and he keeps his own soul as well.

   *backed by* `asmt-0003`

4. The grandmother's own verdict on that route is that it can never happen, and the obstacle she names is specific: a fish's tail is beautiful below and thought ugly on earth, where two stout props called legs are held necessary in order to be handsome.

   *backed by* `asmt-0003`

5. The little mermaid states her valuation as an exchange, not a romance: she would gladly give all the hundreds of years she has to live to be human for one day, for the hope of the happiness of the world above the stars.

   *backed by* `asmt-0003`

**Related topics** `immortal soul`, `mortality`, `afterlife`

**Labels**

- The conditions are conjunctive and the entry preserves that. Any one relaxed and the ending would not follow, so a paraphrase that softened 'more to him than his father or mother' would break the corpus's internal logic.
- Stated by a character, not by the narrator. The grandmother is presented as knowing, but everything here is her account, and the ending revises part of it.
- Same fiction-versus-fact concern as the world entry: 'human beings have a soul which lives forever' is a stipulation of this story.

**Source units (5)** `u-src-the-little-mermaid-df5d02e6-0010`, `u-src-the-little-mermaid-df5d02e6-0011`, `u-src-the-little-mermaid-df5d02e6-0012`, `u-src-the-little-mermaid-df5d02e6-0013`, `u-src-the-little-mermaid-df5d02e6-0014`

**Traceability** — idempotency key `a5f4f9d9d5a80aeeef78193157d2b346a20c39f1f8c7916392fa83e774a9f7da` · queue event `q-a5f4f9d9d5a80aee` · audits `audit-cand-003`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 4. The sea witch's bargain, and everything disclosed before it is struck

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-004-r1` v2

**Slug** `the-sea-witch-s-bargain-and-everything-disclosed-before-it-is-struck`

A contract with fully stated terms. What is unusual, and worth preserving exactly, is that nothing is concealed: the pain, the price, the irreversibility, the failure clause and the witch's own judgment of the deal are all given before the mermaid accepts.

**Assertions (8)**

1. The witch lives beyond crushing whirlpools and a bubbling mire she calls her turfmoor, in a house built with the bones of shipwrecked human beings, in a forest of polypi that seize and hold everything within reach -- including drowned skeletons and a strangled mermaid.

   *backed by* `asmt-0004`

2. The draught must be drunk on shore before sunrise. The tail shrinks into legs with pain as if a sword were passing through her. She keeps her floating gracefulness so that no dancer will tread more lightly, but at every step it will feel as if she were treading on sharp knives, and the blood must flow.

   *backed by* `asmt-0004`

3. The change is irreversible: once her shape is human she can no more be a mermaid, and will never return through the water to her sisters or her father's palace.

   *backed by* `asmt-0004`

4. The failure clause is exact. If she does not win the prince's love -- so that he is willing to forget his father and mother for her sake, love her with his whole soul, and let a priest join their hands in marriage -- she will never have an immortal soul, and on the first morning after he marries another her heart will break and she will become foam on the crest of the waves.

   *backed by* `asmt-0004`

5. The price is her voice, taken by cutting out her tongue, leaving her permanently unable to speak or sing. The witch demands it precisely because it is the best thing she possesses and the thing she was counting on to charm the prince; asked what is left, the witch names her form, her walk and her eyes.

   *backed by* `asmt-0004`, `asmt-0010`

6. The valuation is established before the sale: merpeople have lovelier voices than anyone on earth, the little mermaid sings more sweetly than all of them, and the whole court applauds her at the ball she leaves in order to seek the witch.

   *backed by* `asmt-0004`, `asmt-0010`

7. The witch volunteers her own judgment of the bargain at the outset -- that it is very stupid, that the mermaid shall have her way, and that it will bring her to sorrow.

   *backed by* `asmt-0004`

8. The witch also supplies a defence for the return journey, a few drops of the potion that would tear the polypi's fingers to pieces. It proves unnecessary: they spring back in terror at the sight of the draught.

   *backed by* `asmt-0004`, `asmt-0010`

**Related topics** `bargains`, `sea witch`, `irreversibility`, `voice`

**Labels**

- This is a large entry. It holds together because the clauses are one contract, but a reader wanting only the failure clause has to take the whole bargain.
- The witch's warning that the bargain will bring sorrow is the clause most likely to be cut as flavour. It is load-bearing: it establishes that the mermaid chose with full information.
- The polypi defence is the weakest item here -- it resolves a passage rather than a term of the deal, and sits oddly among clauses.
- One source.

**Source units (8)** `u-src-the-little-mermaid-df5d02e6-0015`, `u-src-the-little-mermaid-df5d02e6-0016`, `u-src-the-little-mermaid-df5d02e6-0017`, `u-src-the-little-mermaid-df5d02e6-0018`, `u-src-the-little-mermaid-df5d02e6-0019`, `u-src-the-little-mermaid-df5d02e6-0020`, `u-src-the-little-mermaid-df5d02e6-0040`, `u-src-the-little-mermaid-df5d02e6-0042`

**Traceability** — idempotency key `dd81bdb1f78902be3c87a34a0e9b316d85e9d791072734ff359401edf2732a8e` · queue event `q-dd81bdb1f78902be` · audits `audit-cand-004`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 5. How the bargain fails, on its own stated terms

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-005-r1` v2

**Slug** `how-the-bargain-fails-on-its-own-stated-terms`

Not misfortune. The mermaid pays the full price continuously, receives affection that is explicitly not marriage, and holds the one fact that would change everything while having sold the means of saying it.

**Assertions (7)**

1. She wakes on the shore with legs and no clothes, wraps herself in her hair, and cannot answer when the prince asks who she is and where she comes from.

   *backed by* `asmt-0005`

2. Every step is as the witch said -- as if treading on needles or sharp knives -- and she bears it willingly, dancing before the court and climbing mountains until her feet bleed and her steps are marked, laughing while she does it.

   *backed by* `asmt-0005`

3. The prince loves her as he would love a little child, says she shall remain with him always, and gives her a cushion at his door and a page's dress -- but it never comes into his head to make her his wife, and unless he marries her she cannot receive an immortal soul.

   *backed by* `asmt-0005`

4. He states the obstacle himself: he was wrecked and cast ashore near a holy temple, the youngest maiden there found him and saved his life, he saw her twice, and she is the only one he could love -- though the little mermaid resembles her closely enough to have almost driven her image from his mind.

   *backed by* `asmt-0005`

5. She knows the correction and cannot make it. She carried him to that wood and watched beneath the foam until people came, and having no voice she can only resolve to stay by him and give up her life for his sake.

   *backed by* `asmt-0005`

6. The bride chosen for him turns out to be that same temple maiden. He recognizes her as the one who saved his life, embraces her, and tells the little mermaid that his fondest hopes are fulfilled and that she will rejoice at his happiness.

   *backed by* `asmt-0005`

7. Her family is not wholly cut off: the sisters come to the surface nightly, and once the grandmother -- who had not surfaced in years -- and the Sea King himself appear, stretching out their hands but not venturing as near the land as the sisters do.

   *backed by* `asmt-0005`, `asmt-0011`

**Related topics** `unrequited love`, `silence`, `mistaken identity`

**Labels**

- Note that the family's visits sit in tension with the witch's stated terms.

**Source units (8)** `u-src-the-little-mermaid-df5d02e6-0021`, `u-src-the-little-mermaid-df5d02e6-0022`, `u-src-the-little-mermaid-df5d02e6-0023`, `u-src-the-little-mermaid-df5d02e6-0024`, `u-src-the-little-mermaid-df5d02e6-0025`, `u-src-the-little-mermaid-df5d02e6-0026`, `u-src-the-little-mermaid-df5d02e6-0027`, `u-src-the-little-mermaid-df5d02e6-0041`

**Traceability** — idempotency key `ac8f72187084121031eda97f072b0f2aa1f95e887a7d88c2439a0c000c08076f` · queue event `q-ac8f721870841210` · audits `audit-cand-005`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 6. The knife: an escape offered and refused

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-006-r1` v2

**Slug** `the-knife-an-escape-offered-and-refused`

The story's decision point, constructed as a clean alternative with a mechanism, a price and a deadline -- which is what makes the refusal an act rather than a fate.

**Assertions (3)**

1. The sisters cut off their hair and give it to the witch in exchange for a knife. If the mermaid plunges it into the prince's heart before sunrise, his warm blood on her feet will grow them together into a tail, and she will return to live out her three hundred years before becoming sea foam.

   *backed by* `asmt-0006`

2. The choice is stated as an exclusive alternative with a deadline: he or she must die before sunrise.

   *backed by* `asmt-0006`

3. She does not use it. She draws back the curtain, sees the bride resting on the prince's breast, kisses his brow, and when he whispers his bride's name in his sleep she flings the knife into the waves and throws herself into the sea.

   *backed by* `asmt-0006`

**Related topics** `sacrifice`, `moral choice`, `sisters`

**Labels**

- The escape's price is a second life, and the entry states it plainly rather than softening it. That is the correct treatment of a fairy tale that is more brutal than its reputation.
- The sisters' own payment -- their hair -- is carried. Without it the knife appears from nowhere.
- One source, one narrative. Nothing here is corroborated by anything.

**Source units (3)** `u-src-the-little-mermaid-df5d02e6-0028`, `u-src-the-little-mermaid-df5d02e6-0029`, `u-src-the-little-mermaid-df5d02e6-0030`

**Traceability** — idempotency key `1ce0f71eedd79b16086ac7f226c8c58ba0d0a8183141aca5bf5f7677e68edb78` · queue event `q-1ce0f71eedd79b16` · audits `audit-cand-006`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 7. The daughters of the air: the rule that revises the ending

`create` · knowledge state **authoritative** · status `ready` · candidate `cand-007-r1` v2

**Slug** `the-daughters-of-the-air-the-rule-that-revises-the-ending`

The story does not overturn its own rules at the end; it adds a third one. A mermaid's eternal destiny hangs on the power of another, and the daughters of the air can earn what she could not be given.

**Assertions (6)**

1. She does not dissolve. She finds herself among the daughters of the air -- transparent beings unseen by mortal eyes, whose speech is too ethereal for mortal ears -- and perceives that she has a body like theirs and is rising out of the foam.

   *backed by* `asmt-0007`, `asmt-0008`

2. The third rule, stated in contrast to the first: a mermaid has no immortal soul and cannot obtain one unless she wins the love of a human being, so her eternal destiny hangs on the power of another. The daughters of the air have no soul either, but can procure one by their own good deeds -- cooling the sultry air that spreads pestilence, carrying the perfume of flowers -- and after striving three hundred years to do all the good in their power they receive one.

   *backed by* `asmt-0007`, `asmt-0008`

3. She is admitted on stated grounds rather than by mercy: she tried with her whole heart to do as they do, suffered and endured, and raised herself to the spirit-world by her good deeds -- so by striving three hundred years in the same way she may obtain an immortal soul.

   *backed by* `asmt-0007`, `asmt-0008`

4. The term is not fixed. For every day the daughters of the air find a good child who is the joy of its parents, their probation shortens by a year; for every naughty or wicked child they weep, and every tear adds a day. This is the only clause addressed past the story to its reader.

   *backed by* `asmt-0007`, `asmt-0008`

5. Two details close: unseen, she kisses the bride's forehead and fans the prince before rising with the children of the air; and she weeps for the first time, having been unable to shed tears as a mermaid.

   *backed by* `asmt-0007`, `asmt-0008`

6. This rule revises rather than supplements the grandmother's account in 'Souls: what a mermaid has, what a human has, and the one way to cross'. She states that a mermaid can obtain a soul only by winning a human's love, and predicts it can never happen. That is not overturned -- the little mermaid does not win it -- but it is shown to be incomplete: a mermaid who has striven as the daughters of the air strive is given the same goal by a second route, earned rather than granted. Read the two entries together.

   *backed by* `asmt-0007`, `asmt-0008`

**Related topics** `daughters of the air`, `good deeds`, `immortal soul`, `moral`

**Source units (6)** `u-src-the-little-mermaid-df5d02e6-0031`, `u-src-the-little-mermaid-df5d02e6-0032`, `u-src-the-little-mermaid-df5d02e6-0033`, `u-src-the-little-mermaid-df5d02e6-0034`, `u-src-the-little-mermaid-df5d02e6-0035`, `u-src-the-little-mermaid-df5d02e6-0036`

**Traceability** — idempotency key `be2e7ef57958fb7d08aa4730e7395ecb87147c81d0202ce19e6f7163cf9cb7a8` · queue event `q-be2e7ef57958fb7d` · audits `audit-cand-007`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>
