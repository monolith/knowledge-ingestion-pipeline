"""Run configuration — model roles, batch policy, granularity policy.

Every knob here traces to a specification decision. The spec section is cited on
each field so a config change can be checked against the evidence that motivated
the default. See docs/SPECIFICATION.md.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import Any

# 3.1.0 added the knowledge-type taxonomy (kt-v1) and, with it, removed derived
# classification labels from the content hash (see artifacts.DERIVED_FIELDS).
# Content hashes written under 3.0.0 are therefore NOT comparable with 3.1.0
# hashes -- a run sealed by the older code will not re-seal to the same digest.
SCHEMA_VERSION = "3.1.0"

# --- Model roles (spec §19.4) -------------------------------------------------
# Only three assignments are research-mandated:
#   - grounding checker must be a specialized NLI checker, not a frontier LLM
#     (R4 F1: GPT-4 accuracy at ~400x lower cost)
#   - the auditor must be reasoning-class AND distinct from the proposer
#     (R3 F1: non-reasoning judges near chance on hard correctness pairs;
#      R3 F4: self-preference survives anonymization)
#   - the relationship judge must be prompted, never fine-tuned
#     (R2 F5: fine-tuned classifiers collapse OOD, 0.945 -> 0.42 macro-F1)
# The remaining tier choices are cost judgment, flagged [NEW — confirm] in §19.4.

MODEL_EXTRACTOR = os.environ.get("KIP_MODEL_EXTRACTOR", "claude-sonnet-5")
MODEL_OMISSION = os.environ.get("KIP_MODEL_OMISSION", "claude-sonnet-5")
MODEL_ENRICHER = os.environ.get("KIP_MODEL_ENRICHER", "claude-haiku-4-5")
MODEL_JUDGE = os.environ.get("KIP_MODEL_JUDGE", "claude-sonnet-5")
MODEL_PLANNER = os.environ.get("KIP_MODEL_PLANNER", "claude-sonnet-5")
MODEL_AUDITOR = os.environ.get("KIP_MODEL_AUDITOR", "claude-opus-5")


@dataclass(frozen=True)
class BatchPolicy:
    """Multi-item batch sizing (spec §17).

    Evidence (R5 T2): degradation begins around 20-100 instances and *collapses*
    beyond; instance count has a stronger effect than context length. A batch
    classification study across 8 models found 6/8 stayed within 2pp of the
    single-item baseline through batch size 100.

    `rotate_ordering` is not a stylistic choice: mid-batch items are
    systematically disadvantaged by a 22pp primacy-to-middle spread, and
    mid-context performance can fall *below* the model's own closed-book
    baseline (Lost in the Middle, TACL 2024).
    """

    target_size: int = 35          # inside the spec's 20-50 band (§17)
    hard_split_above: int = 75     # spec §10.4 / §17
    rotate_ordering: bool = True   # R5 T2
    context_reservation: float = 0.4  # reserve 30-50% of window (§17)


@dataclass(frozen=True)
class GranularityPolicy:
    """Pass 1 unit granularity (spec §9.2).

    v2.0 asked for maximally atomic units. Research refuted that as an end in
    itself: fully atomic facts lose the context needed to interpret them, and
    decomposition measurably *hurts* strong verifiers (Minicheck on WICE scored
    72.32 undecomposed vs 59.90-68.22 with every decomposition method tested).
    This pipeline runs strong models downstream, so it extracts *molecular*
    units: decontextualized (stands alone) but minimal (least added info).

    `name` is written into every unit record so granularity stays tunable and
    auditable rather than baked in.
    """

    name: str = "molecular-v1"
    soft_target_words: tuple[int, int] = (20, 80)   # spec §9.4
    warn_words: int = 160                            # spec §9.4
    max_evidence_words: int = 200                    # spec §9.4


@dataclass(frozen=True)
class AuditPolicy:
    """Pass 5 auditor conditions (spec §13.3).

    These three flags exist because the audit only works under specific
    conditions; recording them per-run lets any audit record be re-evaluated
    against the conditions that produced it (spec §7).
    """

    require_distinct_auditor: bool = True   # R3 F4
    order_swap: bool = True                 # R3 F3 (17-22% of verdicts flip)
    # Deterministic checks replace LLM judgment wherever possible (R3 F6),
    # because even the best auditors carry ~19% pairwise error on hard cases.
    deterministic_citation_check: bool = True
    # Grounding via specialized NLI checker (R4 F1). Disabled by default because
    # it needs a local model; when off, grounding degrades to LLM judgment and
    # the audit record says so.
    nli_checker_model: str | None = os.environ.get("KIP_NLI_CHECKER")


@dataclass(frozen=True)
class Config:
    batch: BatchPolicy = field(default_factory=BatchPolicy)
    granularity: GranularityPolicy = field(default_factory=GranularityPolicy)
    audit: AuditPolicy = field(default_factory=AuditPolicy)

    # Injection defense (spec §20.4). Datamarking is the highest-payoff layer:
    # document-summarization attack success ~60% -> 3.1% with no measured task
    # cost. Delimiters alone only halve it, so they are never used alone.
    datamark: bool = True
    datamark_char: str = "▁"  # U+2581 LOWER ONE EIGHTH BLOCK

    # Where the retention taxonomy lives. A unit whose statement matches one of
    # its protected kinds must survive synthesis; see retention.py. None means
    # the shipped default, which a deployment overrides with KIP_TAXONOMY.
    taxonomy_path: str | None = os.environ.get("KIP_TAXONOMY")

    # Cost: the Message Batches API is 50% off input AND output, and stacks with
    # prompt caching (PE T4). Pass 1 across many sources is the natural batch.
    use_batch_api: bool = False

    def model_for(self, role: str) -> str:
        return {
            "extractor": MODEL_EXTRACTOR,
            "omission": MODEL_OMISSION,
            "enricher": MODEL_ENRICHER,
            "judge": MODEL_JUDGE,
            "planner": MODEL_PLANNER,
            "auditor": MODEL_AUDITOR,
        }[role]

    def manifest_fragment(self) -> dict[str, Any]:
        """Config snapshot for the run manifest.

        Spec §7 requires recording the evidence-tier configuration in force --
        which checker did grounding, whether the auditor differed from the
        proposer, and the batch size used -- because all three materially change
        the error rate of the output.
        """
        return {
            "schema_version": SCHEMA_VERSION,
            "batch": asdict(self.batch),
            "granularity": asdict(self.granularity),
            "audit": asdict(self.audit),
            "datamark": self.datamark,
            "taxonomy_path": self.taxonomy_path,
            "use_batch_api": self.use_batch_api,
            "models": {
                role: self.model_for(role)
                for role in ("extractor", "omission", "enricher", "judge", "planner", "auditor")
            },
        }


def default_config() -> Config:
    return Config()
