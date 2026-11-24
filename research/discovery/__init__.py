"""Long-Horizon Discovery Loop with Kill-Switch and Differentiated Model Routing (R12 #1275)."""

from __future__ import annotations

PIPELINE_STAGES: tuple[str, ...] = (
    "SELECT_OPEN_NODE",
    "NOVELTY_CHECK",
    "CONJECTURE_PROPOSAL",
    "FALSIFY_FIRST",
    "SUBGOAL_DECOMPOSITION",
    "LEAN4_BLUEPRINT_VERIFY",
    "SEMANTIC_ALIGNMENT_AUDIT",
    "PACK_FOR_LEARNHARNESS",
)

TERMINAL_STATUSES: frozenset[str] = frozenset({"FALSIFIED", "PROVED", "FAILED"})
ALLOWED_STATUSES: frozenset[str] = frozenset({"IDLE", "RUNNING", "PAUSED"}) | TERMINAL_STATUSES
ALLOWED_REASONING_LEVELS: frozenset[str] = frozenset({"low", "medium", "high"})
ALLOWED_ROLES: frozenset[str] = frozenset(
    {"engineering", "creative_math", "hard_math_review", "semantic_alignment_audit"}
)
ALLOWED_LEAN_AXIOMS: frozenset[str] = frozenset({"propext", "Classical.choice", "Quot.sound"})
STATE_SCHEMA_VERSION = 1
