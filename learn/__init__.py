"""LearnHarness v0.7.0 HTTP API bridge for aro-discovery v2 (R5 #1162).

Strict contract:
  - Zero edits to LearnHarness core.
  - Zero direct writes to LearnHarness data ledgers (nodes.jsonl / chains.jsonl).
  - All writes go through LearnHarness HTTP API (POST /api/graph/import, POST /api/chats).
  - All reads go through HTTP GET or LearnHarness's read-only skills/learnharness/scripts/graph.py.
"""

from __future__ import annotations

import os
import pathlib

DEFAULT_TRACK = "01-Bridge-OGU-ARO"
DEFAULT_ROOT_PREFIX = "ARO"
DEFAULT_LH_URL = "http://127.0.0.1:3000"

# Mirrors LearnHarness v0.7.0 lib/notes-import-limits.ts
MAX_IMPORT_BYTES = 25 * 1024 * 1024
MAX_GRAPH_CONTEXT_PICKS = 64
IMPORT_EXTENSIONS = frozenset({".txt", ".md", ".markdown", ".rst", ".org", ".adoc", ".tex", ".pdf"})
REQUIRED_GUIDE_FILES = (
    "01-intuition-and-map.md",
    "02-propositions-and-chains.md",
    "03-traps-and-counterexamples.md",
    "04-practice-and-attestation.md",
)
RESERVED_GUIDE_DIRS = frozenset({"TEMPLATE", "00-source-packet-01"})


def default_lh_repo() -> pathlib.Path:
    env_repo = os.environ.get("ARO_LH_REPO")
    if env_repo:
        return pathlib.Path(env_repo).expanduser()
    return pathlib.Path.home() / "Desktop/projects/learn-harness-v070"


def fallback_lh_repo() -> pathlib.Path:
    return pathlib.Path.home() / "Desktop/projects/learn-harness"


def resolve_lh_standalone(explicit: pathlib.Path | None = None) -> pathlib.Path:
    if explicit is not None:
        return explicit.expanduser()
    env_server = os.environ.get("ARO_LH_STANDALONE")
    if env_server:
        return pathlib.Path(env_server).expanduser()
    return default_lh_repo() / ".next/standalone/server.js"


def default_push_state_file() -> pathlib.Path:
    env_state = os.environ.get("ARO_LH_STATE_FILE")
    if env_state:
        return pathlib.Path(env_state).expanduser()
    return pathlib.Path.home() / ".cache/aro-discovery/lh-push-state.json"
