"""Fail-closed persistent state store and Pause / Kill-Switch manager (R12 #1275).

Design guarantees:
  - State lives outside Git by default (`--state-dir` is explicit in tests/CLI; default is
    `<repo>/tmp/discovery-state`, already gitignored).
  - Atomic writes (`tmp` + `fsync` + `os.replace`) prevent partial/corrupted checkpoints.
  - Every saved state carries `schema_version`, `atlas_sha256`, and a canonical SHA-256
    `state_checksum`; any corrupted, truncated, tampered, or stale state fails closed
    with `DiscoveryStateError`.
  - Pause / Kill-Switch operates via both explicit CLI commands (`pause`/`resume`) and
    drop-in filesystem signal files (`PAUSE` / `STOP` inside `state_dir`), preserving all
    open hypotheses, intermediate subgoals, lemmas, and attempt logs with zero data loss.
"""

from __future__ import annotations

import dataclasses
import datetime
import hashlib
import json
import os
import pathlib
import tempfile
from typing import Any

from research.discovery import (
    ALLOWED_STATUSES,
    PIPELINE_STAGES,
    STATE_SCHEMA_VERSION,
)

STATE_FILENAME = "discovery_state.json"
EVENTS_FILENAME = "events.jsonl"
PAUSE_SIGNAL_FILE = "PAUSE"
STOP_SIGNAL_FILE = "STOP"


class DiscoveryStateError(RuntimeError):
    """Raised when the discovery state file is missing, corrupted, tampered, or stale."""


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")


def file_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def compute_state_checksum(payload: dict[str, Any]) -> str:
    """Compute canonical SHA-256 checksum over state payload excluding `state_checksum`."""
    clean = {k: v for k, v in payload.items() if k != "state_checksum"}
    canonical = json.dumps(clean, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def check_kill_switch(state_dir: pathlib.Path) -> tuple[bool, str | None, str | None]:
    """Check for `STOP` (hard) or `PAUSE` (graceful) signal files inside `state_dir`.

    Returns `(active, signal_kind, reason)`.
    """
    for kind, fname in (("STOP", STOP_SIGNAL_FILE), ("PAUSE", PAUSE_SIGNAL_FILE)):
        sig_path = state_dir / fname
        if sig_path.exists():
            reason = ""
            try:
                reason = sig_path.read_text(encoding="utf-8").strip()
            except OSError:
                reason = ""
            return True, kind, reason or f"{kind.lower()}_signal_file"
    return False, None, None


def write_kill_switch(
    state_dir: pathlib.Path,
    *,
    reason: str = "operator_pause",
    hard_stop: bool = False,
) -> pathlib.Path:
    """Create `PAUSE` or `STOP` signal file atomically."""
    state_dir.mkdir(parents=True, exist_ok=True)
    fname = STOP_SIGNAL_FILE if hard_stop else PAUSE_SIGNAL_FILE
    target = state_dir / fname
    _atomic_write_text(target, f"{reason.strip() or fname}\n")
    return target


def clear_kill_switch(state_dir: pathlib.Path) -> list[str]:
    """Remove active `PAUSE` and `STOP` signal files, returning names removed."""
    removed: list[str] = []
    for fname in (PAUSE_SIGNAL_FILE, STOP_SIGNAL_FILE):
        sig_path = state_dir / fname
        if sig_path.exists():
            sig_path.unlink()
            removed.append(fname)
    return removed


def _atomic_write_text(target: pathlib.Path, content: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{target.name}.", suffix=".tmp", dir=target.parent)
    tmp_path = pathlib.Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())
        tmp_path.replace(target)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise


@dataclasses.dataclass
class DiscoveryState:
    run_id: str
    schema_version: int = STATE_SCHEMA_VERSION
    status: str = "IDLE"
    current_stage: str | None = PIPELINE_STAGES[0]
    atlas_sha256: str = ""
    scenario: str = "prove"
    selected_node_id: str | None = None
    selected_node: dict[str, Any] | None = None
    novelty_report: dict[str, Any] | None = None
    hypotheses: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    active_conjecture: dict[str, Any] | None = None
    falsification_result: dict[str, Any] | None = None
    counterexample: dict[str, Any] | None = None
    subgoals: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    lemmas: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    lean_verdict: dict[str, Any] | None = None
    alignment_verdict: dict[str, Any] | None = None
    learn_pack: dict[str, Any] | None = None
    completed_stages: list[str] = dataclasses.field(default_factory=list)
    stage_executions: dict[str, int] = dataclasses.field(default_factory=dict)
    attempt_logs: list[dict[str, Any]] = dataclasses.field(default_factory=list)
    pause_reason: str | None = None
    failure_reason: str | None = None
    opus_quota_remaining: int = 0
    opus_quota_used: int = 0
    surgical_opus_authorized: bool = False
    created_at: str = dataclasses.field(default_factory=utc_now_iso)
    updated_at: str = dataclasses.field(default_factory=utc_now_iso)

    def to_payload(self) -> dict[str, Any]:
        raw = dataclasses.asdict(self)
        raw["state_checksum"] = compute_state_checksum(raw)
        return raw

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any],
        *,
        expected_atlas_sha256: str | None = None,
        max_age_seconds: int | None = None,
    ) -> DiscoveryState:
        """Strictly validate and deserialize a persisted state payload (fail-closed)."""
        if not isinstance(payload, dict):
            raise DiscoveryStateError("Discovery state root must be a JSON object")

        sv = payload.get("schema_version")
        if sv != STATE_SCHEMA_VERSION:
            raise DiscoveryStateError(
                f"Stale or unsupported state schema_version: {sv!r} "
                f"(expected {STATE_SCHEMA_VERSION})"
            )

        decl_cs = payload.get("state_checksum")
        if not isinstance(decl_cs, str) or len(decl_cs) != 64:
            raise DiscoveryStateError("Corrupted state: missing or malformed 'state_checksum'")
        actual_cs = compute_state_checksum(payload)
        if decl_cs != actual_cs:
            raise DiscoveryStateError(
                f"Corrupted/tampered state checksum mismatch: "
                f"declared {decl_cs[:12]}, actual {actual_cs[:12]}"
            )

        run_id = payload.get("run_id")
        if not isinstance(run_id, str) or not run_id.strip():
            raise DiscoveryStateError("Corrupted state: missing non-empty 'run_id'")

        status = payload.get("status")
        if status not in ALLOWED_STATUSES:
            raise DiscoveryStateError(f"Corrupted state: invalid status {status!r}")

        cur_stage = payload.get("current_stage")
        if cur_stage is not None and cur_stage not in PIPELINE_STAGES:
            raise DiscoveryStateError(f"Corrupted state: invalid current_stage {cur_stage!r}")
        if status in {"IDLE", "RUNNING", "PAUSED"} and cur_stage is None:
            raise DiscoveryStateError(
                f"Corrupted state: active status {status!r} requires a non-null current_stage"
            )

        completed = payload.get("completed_stages")
        if not isinstance(completed, list) or not all(s in PIPELINE_STAGES for s in completed):
            raise DiscoveryStateError(
                f"Corrupted state: invalid completed_stages {completed!r}"
            )

        stage_exec = payload.get("stage_executions")
        if not isinstance(stage_exec, dict) or not all(
            k in PIPELINE_STAGES and isinstance(v, int) and not isinstance(v, bool) and v >= 0
            for k, v in stage_exec.items()
        ):
            raise DiscoveryStateError("Corrupted state: invalid stage_executions map")

        for list_field in ("hypotheses", "subgoals", "lemmas", "attempt_logs"):
            if not isinstance(payload.get(list_field), list):
                raise DiscoveryStateError(f"Corrupted state: {list_field!r} must be a list")

        opus_q = payload.get("opus_quota_remaining", 0)
        if not isinstance(opus_q, int) or isinstance(opus_q, bool) or opus_q < 0:
            raise DiscoveryStateError(
                f"Corrupted state: invalid opus_quota_remaining {opus_q!r}"
            )
        opus_used = payload.get("opus_quota_used", 0)
        if not isinstance(opus_used, int) or isinstance(opus_used, bool) or opus_used < 0:
            raise DiscoveryStateError(f"Corrupted state: invalid opus_quota_used {opus_used!r}")
        if not isinstance(payload.get("surgical_opus_authorized", False), bool):
            raise DiscoveryStateError(
                "Corrupted state: 'surgical_opus_authorized' must be a boolean"
            )
        if status == "PROVED" and (
            not isinstance(payload.get("lean_verdict"), dict)
            or not isinstance(payload.get("alignment_verdict"), dict)
        ):
            raise DiscoveryStateError(
                "Corrupted state: PROVED status missing lean_verdict or alignment_verdict"
            )
        if status == "FALSIFIED" and not isinstance(payload.get("counterexample"), dict):
            raise DiscoveryStateError(
                "Corrupted state: FALSIFIED status missing counterexample artifact"
            )

        atlas_sha = payload.get("atlas_sha256")
        if not isinstance(atlas_sha, str) or not atlas_sha.strip():
            raise DiscoveryStateError("Corrupted state: missing 'atlas_sha256'")
        if expected_atlas_sha256 and atlas_sha != expected_atlas_sha256:
            raise DiscoveryStateError(
                f"Stale state: atlas_sha256 mismatch (state={atlas_sha[:12]}, "
                f"current_atlas={expected_atlas_sha256[:12]})"
            )

        updated_at = payload.get("updated_at")
        if not isinstance(updated_at, str) or not updated_at.strip():
            raise DiscoveryStateError("Corrupted state: missing 'updated_at'")
        try:
            updated_dt = datetime.datetime.fromisoformat(updated_at)
        except ValueError as exc:
            raise DiscoveryStateError(f"Corrupted state: invalid 'updated_at': {exc}") from exc

        if max_age_seconds is not None:
            now_dt = datetime.datetime.now(datetime.UTC)
            if updated_dt.tzinfo is None:
                updated_dt = updated_dt.replace(tzinfo=datetime.UTC)
            age = (now_dt - updated_dt).total_seconds()
            if age > max_age_seconds:
                raise DiscoveryStateError(
                    f"Stale state: last updated {age:.0f}s ago (limit {max_age_seconds}s)"
                )

        known_fields = {f.name for f in dataclasses.fields(cls)}
        kwargs = {k: v for k, v in payload.items() if k in known_fields}
        return cls(**kwargs)


class StateStore:
    """Atomic, checksummed state store rooted at `state_dir`."""

    def __init__(self, state_dir: pathlib.Path) -> None:
        self.state_dir = state_dir.resolve()
        self.state_path = self.state_dir / STATE_FILENAME
        self.events_path = self.state_dir / EVENTS_FILENAME

    def exists(self) -> bool:
        return self.state_path.is_file()

    def load(
        self,
        *,
        expected_atlas_sha256: str | None = None,
        max_age_seconds: int | None = None,
    ) -> DiscoveryState:
        if not self.state_path.is_file():
            raise DiscoveryStateError(f"No discovery state found at {self.state_path}")
        try:
            raw_text = self.state_path.read_text(encoding="utf-8")
            payload = json.loads(raw_text)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise DiscoveryStateError(
                f"Corrupted discovery state file {self.state_path}: {exc}"
            ) from exc
        return DiscoveryState.from_payload(
            payload,
            expected_atlas_sha256=expected_atlas_sha256,
            max_age_seconds=max_age_seconds,
        )

    def save(self, state: DiscoveryState) -> None:
        state.updated_at = utc_now_iso()
        payload = state.to_payload()
        rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        _atomic_write_text(self.state_path, rendered)

    def append_event(self, event_type: str, details: dict[str, Any]) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True)
        entry = {
            "timestamp": utc_now_iso(),
            "event": event_type,
            **details,
        }
        line = json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n"
        with self.events_path.open("a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
