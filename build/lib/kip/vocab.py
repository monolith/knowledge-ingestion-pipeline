"""Extraction vocabulary — the closed value sets a digested unit may carry.

These are NOT a classification. Nothing here says what *kind* of knowledge a
statement is; they record properties visible on the face of the sentence, which
is why they survived the removal of the type taxonomy:

- `MODALITIES` is the deontic force of a sentence, read off its modal verb.
- `FLAGS` marks two things embeddings cannot recover on their own. A null result
  and a positive one are near neighbours in vector space — "X does not work" and
  "X works" differ by one token — so without an explicit marker the distinction
  is unrecoverable downstream. `caveat` is the same problem for scope limits.
- `NODE_KINDS` separates a statement from a question. A question asserts
  nothing, and treating one as a claim corrupts anything that reads claims.
- `detect_quantitative` is pure code and never a model call: whether a sentence
  carries a measurement is decidable from its characters.

Typing a unit — deciding whether it is an observation, a principle, a procedure
— is a separate concern handled after digestion, by a classifier that reads the
canonical statement. This package does not do it and must not grow it back.
"""

from __future__ import annotations

import re

#: How far a unit can be traced to the document it came from. The vocabulary
#: follows established retrieval-evaluation practice, where this property is
#: called *grounding* (equivalently *faithfulness*), and where the underlying
#: test is attribution: would a reader affirm "according to this source, X"?
#: A three-value scale rather than a boolean because the middle case is the
#: common one -- a model that expands an acronym or names a standard measure
#: the document assumes has not smuggled in a claim, and collapsing that into
#: "used outside knowledge" would make the flag fire on everything and mean
#: nothing.
GROUNDING: tuple[str, ...] = (
    "attributable",           # every claim traces to a cited excerpt
    "conventions_added",      # claims trace; standard terminology supplied
    "unattributed_content",   # carries substance no cited excerpt supports
)

MODALITIES: tuple[str, ...] = ("required", "permitted", "prohibited")

FLAGS: tuple[str, ...] = ("negative_result", "caveat")

NODE_KINDS: tuple[str, ...] = ("unit", "question")


def normalize_flags(raw: object) -> list[str]:
    """Keep only known flags, order-stable and deduplicated."""
    if not isinstance(raw, (list, tuple)):
        return []
    seen: list[str] = []
    for flag in raw:
        if flag in FLAGS and flag not in seen:
            seen.append(str(flag))
    return seen


def normalize_modality(raw: object) -> str | None:
    return raw if raw in MODALITIES else None  # type: ignore[return-value]


# --- Quantitative detection (code, never a model call) ------------------------
# Deliberately conservative: a false positive costs a wrong retrieval hint, and
# the cheapest way to keep precision high is to require the number to carry
# quantitative force rather than merely to be a digit on the page.

_UNIT_WORDS = (
    r"%|percent|percentage[ -]points?|pp\b|bps?\b|basis points?"
    r"|ms\b|s\b|sec(?:onds?)?\b|min(?:utes?)?\b|hours?\b|days?\b|weeks?\b|months?\b|years?\b"
    r"|[kmgt]?b\b|bytes?\b|[kmg]hz\b|rps\b|qps\b|req/(?:s|min)\b"
    r"|kg\b|lbs?\b|km\b|mi\b|m\b|cm\b|mm\b"
    r"|x\b|fold\b|times\b"
)
_CURRENCY = r"[$€£¥]|\b(?:usd|eur|gbp|jpy|chf)\b"

_QUANTITATIVE_PATTERNS = (
    # A number immediately followed by a unit or percent sign: "8.2%", "10 rps".
    re.compile(r"\d[\d,]*(?:\.\d+)?\s*(?:" + _UNIT_WORDS + r")", re.IGNORECASE),
    # Currency on either side of a number: "$1,200", "1200 USD".
    re.compile(r"(?:" + _CURRENCY + r")\s*\d|\d[\d,]*(?:\.\d+)?\s*(?:" + _CURRENCY + r")",
               re.IGNORECASE),
    # Statistical notation: n=240, p<0.01, r = 0.61, 95% CI, alpha=.05.
    re.compile(r"\b(?:n|p|r|d|f|t|z|k|alpha|beta|kappa|rho)\s*[=<>≤≥]\s*\.?\d", re.IGNORECASE),
    re.compile(r"\b(?:ci|confidence interval|std|sd|stdev|median|mean|average)\b.{0,20}?\d",
               re.IGNORECASE),
    # Ratios and explicit ranges between numbers: "3:1", "5-10", "20 to 50".
    re.compile(r"\b\d[\d,]*(?:\.\d+)?\s*(?::|to|–|—|-)\s*\d[\d,]*(?:\.\d+)?\b", re.IGNORECASE),
    # Comparison operators against a number: "> 100", "at least 2".
    re.compile(r"(?:[<>≤≥]=?|\bat least\b|\bat most\b|\bno more than\b|\bfewer than\b"
               r"|\bmore than\b|\bexceeds?\b|\bunder\b|\bover\b)\s*\d", re.IGNORECASE),
    # Verb cues that give a bare integer quantitative force: "capped at 4",
    # "limited to 100", "a maximum of 3". Without this, thresholds stated as
    # plain counts read as non-quantitative.
    re.compile(r"\b(?:capped|limited|restricted|fixed|set|bounded)\s+(?:at|to)\s+\d"
               r"|\b(?:maximum|minimum|max|min|up to|no more than|at least|at most|only)\s+"
               r"(?:of\s+)?\d", re.IGNORECASE),
    # Magnitude suffixes: 115k, 1.6k, 4M, 2bn.
    re.compile(r"\b\d[\d,]*(?:\.\d+)?\s*(?:k|m|bn|b|t)\b", re.IGNORECASE),
    # Rates spelled out in words: "2000 requests per second". The counted noun
    # must be plural, which is what separates a rate from an incidental "per":
    # "2019 guidance per section 4" is a citation, not a measurement.
    re.compile(r"\b\d[\d,]*(?:\.\d+)?\s+[a-z]+s\s+per\s+[a-z]", re.IGNORECASE),
    # A bare decimal or thousands-separated number is quantitative on its own.
    re.compile(r"\b\d[\d,]*\.\d+\b"),
    re.compile(r"\b\d{1,3}(?:,\d{3})+\b"),
)

# Stripped BEFORE testing, so their digits cannot trigger a match. These are the
# documented false positives: bare years, section and version numbers, dates,
# and identifier-shaped tokens.
#
# ORDER MATTERS. Whole dates must be removed before the bare-year pattern runs:
# stripping the year out of "2026-08-08" first would leave "-08-08", which the
# numeric-range pattern below then happily matches.
#
# Both number-shaped strippers carry a "but not when a unit follows" guard.
# Without it a stripper aimed at one false positive silently created a much
# larger class of false NEGATIVES: "Accuracy 92.5%" reads as a version number
# and "2000 rps" reads as a year, so two of the most ordinary quantitative
# sentences there are came back False. A stripper may only remove a number that
# is carrying no measurement.
# Scoped case-insensitivity, so the guard can be embedded in a case-SENSITIVE
# pattern (the version stripper needs its leading [A-Z] to stay literal).
_MEASURED = r"(?i:" + _UNIT_WORDS + r"|" + _CURRENCY + r"|\w+s\s+per\b)"

_NON_QUANTITATIVE = (
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),                    # 2026-08-08  (before year)
    re.compile(r"\b\d{1,2}/\d{1,2}/\d{2,4}\b"),              # 8/8/2026    (before year)
    re.compile(r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\s+\d{1,2}\b",
               re.IGNORECASE),
    re.compile(r"§\s*\d+(?:\.\d+)*"),                       # §9.3
    re.compile(r"\bv\d+(?:\.\d+)*\b", re.IGNORECASE),        # v3.0
    # A dotted number directly after a capitalized token is a version, not a
    # measurement: "Python 3.12", "Node 22.1". Adjacency alone is NOT enough --
    # a sentence-initial metric name is capitalized too, so "Accuracy 92.5%"
    # matches this shape exactly. The trailing guard is what tells the two
    # apart: a version number is not followed by a unit.
    re.compile(r"\b[A-Z][A-Za-z+#.]*\s+\d+(?:\.\d+)+\b(?!\s*" + _MEASURED + r")"),
    re.compile(r"\bversion\s+\d+(?:\.\d+)*\b", re.IGNORECASE),
    re.compile(r"\b[A-Z]{2,}-\d+\b"),                        # TS-999
    re.compile(r"\bstep\s+\d+\b", re.IGNORECASE),            # step 3
    # A bare year, but not a four-digit measurement that happens to fall in
    # 1900-2099: "$1995 per seat", "2000 rps", "2000 requests per second".
    re.compile(r"(?<![$€£¥])(?<![$€£¥]\s)\b(?:19|20)\d{2}\b(?!\s*" + _MEASURED + r")"),
)


def detect_quantitative(text: str) -> bool:
    """True when the statement carries a number with quantitative force.

    Computed rather than asked. The distinction that matters is force, not
    presence: "the trial ran in 2026" has a number and is not a quantitative
    result; "recall improved 8.2%" is.
    """
    if not text:
        return False
    stripped = text
    for pattern in _NON_QUANTITATIVE:
        stripped = pattern.sub(" ", stripped)
    return any(pattern.search(stripped) for pattern in _QUANTITATIVE_PATTERNS)


# --- Legacy migration ---------------------------------------------------------
# The pre-kt-v1 ontology was a flat list of 20 labels that mixed four different
# questions: what kind of knowledge this is, why it must not be dropped, how it
# relates to another unit, and whether it is knowledge at all. Splitting those
# axes is what makes the mapping below mostly mechanical -- and what makes the
# five leftovers genuinely undecidable from the label alone.
#
# Honest count: 15 of 20 map deterministically. 5 need review. Anyone quoting a
# higher number is counting the unmapped ones.

LEGACY_MAP: dict[str, tuple[str | None, str | None, tuple[str, ...]]] = {
    # legacy label        -> (type, modality, flags)
    "fact": ("claim", None, ()),
    "claim": ("claim", None, ()),
    "definition": ("concept", None, ()),
    "quantitative_result": ("claim", None, ()),   # `quantitative` re-derived by code
    "null_result": ("claim", None, ("negative_result",)),
    "study_design": ("case", None, ()),
    "method": ("method", None, ()),
    "decision": ("case", None, ()),
    "obligation": ("rule", "required", ()),
    "prohibition": ("rule", "prohibited", ()),
    "exception": ("rule", None, ("caveat",)),
    "deadline": ("rule", "required", ()),
    "risk": ("claim", None, ("caveat",)),
    "limitation": ("claim", None, ("caveat",)),
    "open_question": (None, None, ()),            # becomes node_kind="question"
}

LEGACY_UNMAPPED: dict[str, str] = {
    "dependency": "a relationship, not a type; the typed edge is deferred",
    "contradiction": "a relationship, not a type; carried by claim assessments",
    "recommendation": "method vs rule turns on a modality the label does not record",
    "observation": "case vs claim turns on whether it is bound to one instance",
    "metadata": "not knowledge; the unit should be dropped",
}

LEGACY_TYPES: tuple[str, ...] = tuple(LEGACY_MAP) + tuple(LEGACY_UNMAPPED)
