"""Retention guard — protect content a synthesis step is known to drop.

**This is not classification, and it must not become it.** `vocab.py` records
that typing a unit is a separate job done after digestion, and that rule stands.
Nothing here decides what kind of knowledge a statement is. It answers one
narrower question: *does this unit resemble a kind that Pass 4 loses?* The
answer is a retention flag, not a label, and nothing downstream may read it as
one.

The motivation is measured rather than theoretical. Digesting a 12,311-word
specification produced 93 units; 34 of them reached no approved candidate, and
all fifteen of its label definitions were among the losses. The shape of the
loss was not random: a candidate is `title / summary / assertions`, which is a
shape for *propositions*. A definition asserts nothing to argue with, so a
planner describes it -- "the codebook defines fifteen labels" -- instead of
carrying it across, and the content a consumer actually needs never arrives.

Detection is by the taxonomy's own surface cues, applied in code. That is not a
shortcut: the taxonomy this ships with requires its definitions be written as
surface tests rather than judgment calls, having measured that
concretely-described features reach F1 > 0.60 where interpretive ones fall below
0.30. A cue match is cheap, has no error rate of its own to argue about, and is
auditable -- `protected_by` records which pattern fired.

A match is deliberately generous. A false positive costs one unit carried
forward that need not have been; a false negative costs a definition nobody can
find. Those are not symmetric.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Shipped default. A deployment points `KIP_TAXONOMY` at its own file to change
# which kinds are protected and which cues detect them.
DEFAULT_TAXONOMY = Path(__file__).with_name("taxonomies") / "statement-classifier-v1.json"


@dataclass(frozen=True)
class ProtectedKind:
    label: str
    why: str
    patterns: tuple[re.Pattern[str], ...]

    def matches(self, statement: str) -> str | None:
        for pattern in self.patterns:
            if pattern.search(statement):
                return pattern.pattern
        return None


@dataclass(frozen=True)
class Taxonomy:
    version: str
    source: str
    kinds: tuple[ProtectedKind, ...]

    def protections_for(self, statement: str) -> list[dict[str, str]]:
        """Every protected kind this statement resembles, with the cue that fired."""
        hits: list[dict[str, str]] = []
        for kind in self.kinds:
            cue = kind.matches(statement)
            if cue is not None:
                hits.append({"label": kind.label, "cue": cue})
        return hits


def load_taxonomy(path: str | os.PathLike[str] | None = None) -> Taxonomy | None:
    """Load the retention taxonomy, or None when none is configured.

    Returning None rather than raising is deliberate: the guard is an
    enhancement, and a deployment with no taxonomy must still digest documents.
    A configured-but-unreadable path is a different thing and does raise, because
    silently running unprotected is exactly the failure this module exists to
    stop.
    """
    configured = path or os.environ.get("KIP_TAXONOMY")
    target = Path(configured) if configured else DEFAULT_TAXONOMY
    if not target.exists():
        if configured:
            raise FileNotFoundError(f"KIP_TAXONOMY points at a file that does not exist: {target}")
        return None

    data = json.loads(target.read_text(encoding="utf-8"))
    kinds = tuple(
        ProtectedKind(
            label=entry["label"],
            why=entry.get("why", ""),
            patterns=tuple(re.compile(p, re.IGNORECASE) for p in entry.get("cues", [])),
        )
        for entry in data.get("protected", [])
    )
    return Taxonomy(
        version=data.get("taxonomy_version", "unknown"),
        source=data.get("source", str(target)),
        kinds=kinds,
    )


def annotate(units: list[dict[str, Any]], taxonomy: Taxonomy | None) -> int:
    """Stamp `protected_by` on every unit whose statement matches a protected kind.

    Returns how many units were protected. Mutates in place, before sealing, so
    the flag is part of the record rather than something recomputed later and
    liable to drift from what the planner was told.
    """
    if taxonomy is None:
        return 0
    protected = 0
    for unit in units:
        hits = taxonomy.protections_for(unit.get("canonical_statement", ""))
        if hits:
            unit["protected_by"] = hits
            protected += 1
    return protected


def protected_ids(units: list[dict[str, Any]]) -> set[str]:
    return {u.get("unit_id") for u in units if u.get("protected_by")} - {None}
