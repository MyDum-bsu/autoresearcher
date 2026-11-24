"""Fundamental Mathematical Atlas and Lean 4 Blueprint for aro-discovery v2 (R10 #1271)."""

from __future__ import annotations

ALLOWED_NODE_KINDS = frozenset(
    {
        "definition",
        "axiom_assumption",
        "theorem",
        "lemma",
        "counterexample",
        "open_conjecture",
        "generalization_target",
    }
)

ALLOWED_NODE_STATUSES = frozenset(
    {
        "lean_proved",
        "oracle_verified",
        "falsified",
        "open",
        "sketch",
    }
)

ALLOWED_EDGE_RELATIONS = frozenset(
    {
        "depends_on",
        "refutes",
        "generalizes",
        "special_case_of",
        "open_gap",
        "constrains_adr",
        "related_gap",
    }
)

ALLOWED_DOMAINS = frozenset(
    {
        "foundations",
        "bridge_core",
        "aro_exactness",
        "counterexamples",
        "closure_scheduling",
        "generalizations",
    }
)
