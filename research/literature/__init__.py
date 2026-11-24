"""Literature Radar & Knowledge Graph for aro-discovery v2 (R11 #1273)."""

from __future__ import annotations

ALLOWED_LINK_RELATIONS = frozenset(
    {
        "supports",
        "refutes",
        "generalizes",
        "technique_for",
        "baseline_for",
    }
)

ALLOWED_RADAR_SOURCES = frozenset(
    {
        "corpus",
        "arxiv",
        "semantic_scholar",
        "openalex",
    }
)
