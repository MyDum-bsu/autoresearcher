#!/usr/bin/env python3
"""Headless Google Colab GPU/CPU adapter for heavy T1-T7 & parametric falsifier grids.

Design guarantees:
  - Offline / `--dry-run` by default: live cloud execution requires explicit `--live`.
  - Zero hardcoded host paths: locates `colab` via `COLAB_BIN` / PATH / `~/.local/bin/colab`
    and `rclone` via `RCLONE_BIN` / PATH / `~/.local/bin/rclone`.
  - Strict finite positive `--timeout` and `--max-cu` validation (rejects NaN/Inf/<=0) and
    wall-clock subprocess timeout enforcement across all remote steps.
  - Wraps remote script execution in a `__future__`-free bootstrapper (compatible with
    `colab 0.8.0` prologue injection) and optionally bundles minimal repo modules so repo
    presets (`run02-all`, `t1-t7`, etc.) run self-contained on a fresh Colab VM.
  - Automatic VM teardown (`colab stop`) in a `finally` block; any `stop` failure is
    surfaced in `exit_code` and `stop_failed=True` (never silently ignored).
  - Portable JSON report (`RemoteRunReport`) redacts `--env` values and any host paths.
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]

GPU_CHOICES: tuple[str, ...] = ("T4", "L4", "G4", "A100", "H100")
TPU_CHOICES: tuple[str, ...] = ("V5E1", "V6E1")
AUTH_CHOICES: tuple[str, ...] = ("adc", "oauth2")

# Conservative Google Colab Pro+ Compute Unit burn rates (CU per wall-clock hour).
ACCELERATOR_CU_PER_HOUR: dict[str, float] = {
    "CPU": 0.10,
    "T4": 1.96,
    "L4": 4.82,
    "G4": 5.50,
    "A100": 13.08,
    "H100": 25.00,
    "V5E1": 6.00,
    "V6E1": 10.00,
}

# Reproducible preset targets for falsifier & parametric grid workloads in this repo.
GRID_PRESETS: dict[str, dict[str, Any]] = {
    "t1-t7": {
        "script": "verification/falsifiers/battery_t1_t7.py",
        "description": "Full T1-T7 ADR exactness falsification battery",
        "default_params": {"battery": "T1-T7", "exact_rational": True},
    },
    "o4-schedule": {
        "script": "verification/falsifiers/run01/falsify_o4.py",
        "description": "O4 closure scheduling exact rational LP falsifier grid",
        "default_params": {"target": "conj-o4-closure-scheduling", "exact_rational": True},
    },
    "o1-adr": {
        "script": "verification/falsifiers/run01/falsify_o1.py",
        "description": "O1 ADR exactness structural predicate & 1D/2D bridge falsifier",
        "default_params": {"target": "conj-o1-adr-exactness-char", "exact_rational": True},
    },
    "g1-multistage": {
        "script": "verification/falsifiers/run01/falsify_g1.py",
        "description": "G1 multi-closure k>=2 Markov vs history separation falsifier",
        "default_params": {"target": "gen-multistage-k-closures", "exact_rational": True},
    },
    "g2-conic": {
        "script": "verification/falsifiers/run01/falsify_g2.py",
        "description": "G2 non-box conic support tightening falsifier",
        "default_params": {"target": "gen-nonbox-conic-uncertainty", "exact_rational": True},
    },
    "run02-all": {
        "script": "research/discovery/run02/run02_falsify.py",
        "description": "R12 Run-02 falsify-first frontier sweep (O4, G1, G2, O1, O8)",
        "default_params": {"target": "run02-frontier", "exact_rational": True},
    },
}

# Minimal repo subtrees required when executing repo presets on a fresh Colab VM.
_REPO_BUNDLE_INCLUDE: tuple[str, ...] = (
    "verification/oracles",
    "verification/falsifiers",
    "research/counterexamples/D1-baseline",
    "research/counterexamples/D2-structured",
    "research/atlas/atlas.json",
    "research/atlas/__init__.py",
    "research/atlas/semantic_index.py",
    "research/discovery/__init__.py",
    "research/discovery/significance_gate.py",
    "research/discovery/run02",
    "research/remote/__init__.py",
    "research/remote/colab_runner.py",
)

_CU_USAGE_RE = re.compile(r"(?:compute\s+units?|cu)\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
_SENTINEL_RC_RE = re.compile(r"ARO_REMOTE_EXIT_CODE=(-?\d+)")
_REMOTE_SAFE_RE = re.compile(r"^[A-Za-z0-9_.-]+:[A-Za-z0-9_./-]*$")
_ABS_HOST_PATH_RE = re.compile(
    r"(?:^|[\s=:,'\"])(?:/home/|/media/|/Users/|/root/|/mnt/|/tmp/|/var/folders/)[^\s,'\"]*"
)


class RemoteComputeError(RuntimeError):
    """Raised on invalid remote compute configuration or failed remote execution."""


class RemoteComputeBudgetError(RemoteComputeError):
    """Raised when estimated Compute Unit (CU) usage exceeds configured `--max-cu`."""


def _sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _portable_path(path: pathlib.Path, repo_root: pathlib.Path = REPO_ROOT) -> str:
    """Return a repo-relative POSIX path when inside repo_root, otherwise basename."""
    resolved = path.resolve()
    root_resolved = repo_root.resolve()
    try:
        return resolved.relative_to(root_resolved).as_posix()
    except ValueError:
        return resolved.name


def _is_inside_repo(path: pathlib.Path, repo_root: pathlib.Path) -> bool:
    try:
        path.resolve().relative_to(repo_root.resolve())
        return True
    except ValueError:
        return False


def _sanitize_value(value: Any, repo_root: pathlib.Path, out_dir: pathlib.Path) -> Any:
    """Recursively redact host paths inside arbitrary JSON-serializable keys and values."""
    if isinstance(value, dict):
        return {
            str(_sanitize_value(str(k), repo_root, out_dir)): _sanitize_value(v, repo_root, out_dir)
            for k, v in value.items()
        }
    if isinstance(value, list):
        return [_sanitize_value(v, repo_root, out_dir) for v in value]
    if isinstance(value, tuple):
        return [_sanitize_value(v, repo_root, out_dir) for v in value]
    if isinstance(value, str):
        s = value
        root_str = str(repo_root.resolve())
        out_str = str(out_dir.resolve())
        home_str = str(pathlib.Path.home().resolve())
        tmp_str = str(pathlib.Path(tempfile.gettempdir()).resolve())
        s = s.replace(root_str, "<repo>")
        s = s.replace(out_str, "<out_dir>")
        s = s.replace(home_str, "<home>")
        s = s.replace(tmp_str, "<tmp>")
        return _ABS_HOST_PATH_RE.sub(
            lambda m: (
                m.group(0)[0] + "<redacted-path>"
                if m.group(0)[0] in " =:,'\""
                else "<redacted-path>"
            ),
            s,
        )
    return value


def find_colab_bin() -> str | None:
    """Locate `colab` CLI via `COLAB_BIN`, PATH, or `~/.local/bin/colab`."""
    env_bin = os.environ.get("COLAB_BIN", "").strip()
    if env_bin:
        candidate = pathlib.Path(env_bin).expanduser()
        if candidate.is_file():
            return str(candidate)
    found = shutil.which("colab")
    if found:
        return found
    local_bin = pathlib.Path.home() / ".local" / "bin" / "colab"
    if local_bin.is_file():
        return str(local_bin)
    return None


def find_rclone_bin() -> str | None:
    """Locate `rclone` CLI via `RCLONE_BIN`, PATH, or `~/.local/bin/rclone`."""
    env_bin = os.environ.get("RCLONE_BIN", "").strip()
    if env_bin:
        candidate = pathlib.Path(env_bin).expanduser()
        if candidate.is_file():
            return str(candidate)
    found = shutil.which("rclone")
    if found:
        return found
    local_bin = pathlib.Path.home() / ".local" / "bin" / "rclone"
    if local_bin.is_file():
        return str(local_bin)
    return None


def estimate_cu_cost(accelerator: str, timeout_sec: float) -> float:
    """Conservatively estimate Compute Unit cost for an accelerator and positive finite timeout."""
    accel = accelerator.upper()
    if accel not in ACCELERATOR_CU_PER_HOUR:
        raise RemoteComputeError(f"Unknown accelerator: {accelerator!r}")
    if not isinstance(timeout_sec, (int, float)) or isinstance(timeout_sec, bool):
        raise RemoteComputeError(
            f"timeout_sec must be a finite positive number, got {timeout_sec!r}"
        )
    if not math.isfinite(timeout_sec) or timeout_sec <= 0:
        raise RemoteComputeError(
            f"timeout_sec must be finite and > 0 (unbounded timeout=0 forbidden), got {timeout_sec}"
        )
    rate = ACCELERATOR_CU_PER_HOUR[accel]
    return round(rate * (float(timeout_sec) / 3600.0), 4)


def parse_upload_spec(spec: str) -> tuple[pathlib.Path, str]:
    """Parse `LOCAL_PATH:REMOTE_PATH` upload spec and verify local path exists."""
    if ":" not in spec:
        raise RemoteComputeError(f"Invalid upload spec {spec!r}; expected LOCAL_PATH:REMOTE_PATH")
    local_str, remote_path = spec.split(":", 1)
    if not local_str.strip() or not remote_path.strip():
        raise RemoteComputeError(f"Invalid upload spec {spec!r}; empty local or remote path")
    local_path = pathlib.Path(local_str).expanduser().resolve()
    if not local_path.exists():
        raise RemoteComputeError(f"Upload file not found: {local_path.name}")
    return local_path, remote_path


def resolve_grid_preset(
    preset_name: str, repo_root: pathlib.Path = REPO_ROOT
) -> tuple[pathlib.Path, dict[str, Any]]:
    """Resolve a named falsifier grid preset to its script path and default parameters."""
    if preset_name not in GRID_PRESETS:
        raise RemoteComputeError(
            f"Unknown grid preset {preset_name!r}; expected one of {sorted(GRID_PRESETS)}"
        )
    spec = GRID_PRESETS[preset_name]
    script_path = (repo_root / spec["script"]).resolve()
    if not script_path.is_file():
        raise RemoteComputeError(f"Preset script missing: {spec['script']}")
    return script_path, dict(spec["default_params"])


def build_colab_bootstrap_source(
    *,
    script_rel_or_remote: str,
    script_args: tuple[str, ...],
    has_env_file: bool,
    unpack_repo_tarball: bool,
) -> str:
    """Generate a `__future__`-free bootstrap script safe under `colab 0.8.0` prologue injection.

    Never embeds `--env` values in source code (colab 0.8.0 logs executed source to JSONL history);
    when `has_env_file=True`, loads `/content/.aro_env.json` and deletes it immediately.
    """
    lines = [
        "# Auto-generated __future__-free Colab bootstrapper (safe under colab 0.8.0 prologue)",
        "import json, os, subprocess, sys, tarfile",
        f"SCRIPT_TARGET = {script_rel_or_remote!r}",
        f"SCRIPT_ARGS = {list(script_args)!r}",
        "env = dict(os.environ)",
    ]
    if has_env_file:
        lines.extend(
            [
                "try:",
                "    with open('/content/.aro_env.json', 'r', encoding='utf-8') as _ef:",
                "        env.update(json.load(_ef))",
                "finally:",
                "    if os.path.exists('/content/.aro_env.json'):",
                "        os.remove('/content/.aro_env.json')",
            ]
        )
    if unpack_repo_tarball:
        lines.extend(
            [
                "os.makedirs('/content/aro_repo', exist_ok=True)",
                "with tarfile.open('/content/aro_repo.tar.gz', 'r:gz') as tf:",
                "    tf.extractall('/content/aro_repo')",
                "pp = env.get('PYTHONPATH', '')",
                "env['PYTHONPATH'] = '/content/aro_repo' + (':' + pp if pp else '')",
                "cmd = [sys.executable, '-B', SCRIPT_TARGET, *SCRIPT_ARGS]",
                "proc = subprocess.run(cmd, cwd='/content/aro_repo', env=env)",
            ]
        )
    else:
        lines.append(
            "proc = subprocess.run([sys.executable, '-B', SCRIPT_TARGET, *SCRIPT_ARGS], env=env)"
        )
    lines.append("print('ARO_REMOTE_EXIT_CODE=' + str(proc.returncode), flush=True)")
    lines.append("if proc.returncode != 0: raise SystemExit(proc.returncode)")
    return "\n".join(lines) + "\n"


def create_repo_bundle(repo_root: pathlib.Path, target_tar_gz: pathlib.Path) -> pathlib.Path:
    """Create a minimal deterministic tar.gz of repo modules needed for remote falsifier runs."""
    target_tar_gz.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(target_tar_gz, "w:gz") as tf:
        for rel in _REPO_BUNDLE_INCLUDE:
            full = repo_root / rel
            if not full.exists():
                continue
            if full.is_file():
                tf.add(full, arcname=rel)
            else:
                for path in sorted(full.rglob("*")):
                    if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                        continue
                    if path.is_file():
                        tf.add(path, arcname=path.relative_to(repo_root).as_posix())
    return target_tar_gz


@dataclasses.dataclass(frozen=True)
class RemoteRunConfig:
    script: pathlib.Path
    accelerator: str = "CPU"
    high_mem: bool = False
    auth: str = "adc"
    timeout_sec: float = 300.0
    max_cu: float = 0.5
    keep_session: bool = False
    session: str | None = None
    env: tuple[str, ...] = ()
    uploads: tuple[str, ...] = ()
    artifacts: tuple[str, ...] = ()
    out_dir: pathlib.Path = pathlib.Path("tmp/colab-artifacts")
    rclone_remote: str | None = None
    seed: int = 20261124
    params: dict[str, Any] = dataclasses.field(default_factory=dict)
    script_args: tuple[str, ...] = ()
    bundle_repo: bool | None = None
    live: bool = False
    repo_root: pathlib.Path = REPO_ROOT


@dataclasses.dataclass(frozen=True)
class RemoteRunReport:
    schema_version: int
    run_id: str
    mode: str
    script_relpath: str
    script_sha256: str
    accelerator: str
    high_mem: bool
    auth: str
    seed: int
    params: dict[str, Any]
    timeout_sec: float
    max_cu: float
    estimated_cu: float
    reported_cu: float
    duration_sec: float
    exit_code: int
    stop_failed: bool
    colab_installed: bool
    steps: list[dict[str, Any]]
    artifacts: list[dict[str, Any]]
    rclone_sync: dict[str, Any] | None
    timestamp_utc: str

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def _deterministic_run_id(
    script_sha256: str, accelerator: str, seed: int, params: dict[str, Any]
) -> str:
    payload = json.dumps(
        {
            "script_sha256": script_sha256,
            "accelerator": accelerator,
            "seed": seed,
            "params": params,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:12]
    return f"aro-remote-{accelerator.lower()}-{digest}"


def _sanitize_cmd_for_report(cmd: list[str], repo_root: pathlib.Path, out_dir: pathlib.Path) -> str:
    """Format command for portable JSON reports without leaking host/tmp paths or --env values."""
    sanitized: list[str] = []
    root_str = str(repo_root.resolve())
    out_str = str(out_dir.resolve())
    home_str = str(pathlib.Path.home().resolve())
    tmp_str = str(pathlib.Path(tempfile.gettempdir()).resolve())
    redact_next_env = False
    for tok in cmd:
        if redact_next_env:
            key = tok.split("=", 1)[0] if "=" in tok else "VAR"
            sanitized.append(f"{key}=<redacted>")
            redact_next_env = False
            continue
        if tok == "--env":
            sanitized.append(tok)
            redact_next_env = True
            continue
        if tok.startswith("--env="):
            rest = tok[len("--env=") :]
            key = rest.split("=", 1)[0] if "=" in rest else "VAR"
            sanitized.append(f"--env={key}=<redacted>")
            continue
        if tok == root_str or tok.startswith(root_str + os.sep):
            rel = pathlib.Path(tok).resolve().relative_to(repo_root.resolve()).as_posix()
            sanitized.append(rel)
        elif tok == out_str or tok.startswith(out_str + os.sep):
            rel_out = pathlib.Path(tok).resolve().relative_to(out_dir.resolve()).as_posix()
            sanitized.append(f"<out_dir>/{rel_out}" if rel_out != "." else "<out_dir>")
        elif tok.endswith("/colab") or tok == "colab":
            sanitized.append("colab")
        elif tok.endswith("/rclone") or tok == "rclone":
            sanitized.append("rclone")
        elif tok.startswith(tmp_str + os.sep):
            sanitized.append(f"<stage>/{pathlib.Path(tok).name}")
        elif tok.startswith(home_str + os.sep):
            sanitized.append(f"<home>/{tok[len(home_str) + 1 :]}")
        elif _ABS_HOST_PATH_RE.search(tok):
            sanitized.append("<redacted-path>")
        else:
            sanitized.append(tok)
    return shlex.join(sanitized)


def build_rclone_sync_plan(
    out_dir: pathlib.Path,
    rclone_remote: str,
    run_id: str,
    rclone_bin: str = "rclone",
) -> dict[str, Any]:
    """Build deterministic `rclone copy` plan for syncing large remote artifacts."""
    remote_clean = rclone_remote.strip()
    if not _REMOTE_SAFE_RE.match(remote_clean):
        raise RemoteComputeError(
            f"Invalid rclone remote {rclone_remote!r}; expected format like 'gdrive:aro-artifacts'"
        )
    dest = f"{remote_clean.rstrip('/')}/{run_id}"
    cmd = [rclone_bin, "copy", str(out_dir.resolve()), dest, "--checksum"]
    return {
        "remote": dest,
        "cmd": cmd,
        "portable_command": shlex.join(["rclone", "copy", "<out_dir>", dest, "--checksum"]),
        "executed": False,
        "exit_code": None,
    }


def build_execution_plan(
    config: RemoteRunConfig,
    colab_bin: str = "colab",
    rclone_bin: str = "rclone",
    *,
    bootstrap_local_path: pathlib.Path | None = None,
    bundle_local_path: pathlib.Path | None = None,
    env_local_path: pathlib.Path | None = None,
    cleanup_env_local_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    """Validate config, enforce CU budget guard, and build deterministic execution plan."""
    script_path = config.script.expanduser().resolve()
    if not script_path.is_file():
        raise RemoteComputeError(f"Script file not found: {config.script}")

    accel = config.accelerator.upper()
    valid_accels = {"CPU", *GPU_CHOICES, *TPU_CHOICES}
    if accel not in valid_accels:
        raise RemoteComputeError(
            f"Invalid accelerator {config.accelerator!r}; expected one of {sorted(valid_accels)}"
        )
    if config.auth not in AUTH_CHOICES:
        raise RemoteComputeError(f"Invalid auth {config.auth!r}; expected one of {AUTH_CHOICES}")
    if (
        not isinstance(config.max_cu, (int, float))
        or isinstance(config.max_cu, bool)
        or not math.isfinite(config.max_cu)
        or config.max_cu <= 0
    ):
        raise RemoteComputeError(f"max_cu must be finite and > 0, got {config.max_cu!r}")

    for kv in config.env:
        if "=" not in kv or not kv.split("=", 1)[0].strip():
            raise RemoteComputeError(f"Invalid --env entry {kv!r}; expected KEY=VALUE")

    estimated_cu = estimate_cu_cost(accel, config.timeout_sec)
    if estimated_cu > config.max_cu:
        raise RemoteComputeBudgetError(
            f"Estimated CU ({estimated_cu:.4f}) exceeds max_cu budget ({config.max_cu:.4f}) "
            f"for accelerator={accel} timeout={config.timeout_sec}s. "
            "Reduce --timeout, pick a cheaper accelerator, or raise --max-cu explicitly."
        )

    script_sha = _sha256_file(script_path)
    script_rel = _portable_path(script_path, config.repo_root)
    use_repo_bundle = (
        bool(config.bundle_repo)
        if config.bundle_repo is not None
        else _is_inside_repo(script_path, config.repo_root)
    )
    run_id = _deterministic_run_id(script_sha, accel, config.seed, config.params)
    session_name = config.session or run_id[:28]
    out_dir = config.out_dir.expanduser().resolve()

    bootstrap_ref = str(bootstrap_local_path) if bootstrap_local_path else "<bootstrap.py>"
    bundle_ref = str(bundle_local_path) if bundle_local_path else "<aro_repo.tar.gz>"

    base = [colab_bin, "--auth", config.auth]
    steps: list[dict[str, Any]] = []

    # Always use explicit session lifecycle + __future__-free bootstrapper so:
    #  1. `colab 0.8.0` prologue injection never triggers SyntaxError on `from __future__`;
    #  2. Repo scripts have the full minimal repo bundle unpacked at `/content/aro_repo`;
    #  3. Wall-clock timeout and guaranteed `colab stop` apply uniformly.
    new_cmd = [*base, "new", "--session", session_name]
    if accel in TPU_CHOICES:
        new_cmd.extend(["--tpu", accel])
    elif accel in GPU_CHOICES:
        new_cmd.extend(["--gpu", accel])
    if config.high_mem:
        new_cmd.append("--high-mem")
    steps.append({"stage": "create_session", "cmd": new_cmd, "always": False})

    if use_repo_bundle:
        steps.append(
            {
                "stage": "upload_repo_bundle",
                "cmd": [
                    *base,
                    "upload",
                    "-s",
                    session_name,
                    bundle_ref,
                    "/content/aro_repo.tar.gz",
                ],
                "always": False,
            }
        )
    else:
        steps.append(
            {
                "stage": "upload_script",
                "cmd": [
                    *base,
                    "upload",
                    "-s",
                    session_name,
                    str(script_path),
                    f"/content/{script_path.name}",
                ],
                "always": False,
            }
        )

    for spec in config.uploads:
        local_p, remote_p = parse_upload_spec(spec)
        steps.append(
            {
                "stage": "upload",
                "cmd": [*base, "upload", "-s", session_name, str(local_p), remote_p],
                "always": False,
            }
        )

    if config.env:
        env_ref = str(env_local_path) if env_local_path else "<aro_env.json>"
        steps.append(
            {
                "stage": "upload_env",
                "cmd": [*base, "upload", "-s", session_name, env_ref, "/content/.aro_env.json"],
                "always": False,
            }
        )

    steps.append(
        {
            "stage": "exec_bootstrap",
            "cmd": [*base, "exec", "-s", session_name, "-f", bootstrap_ref],
            "always": False,
        }
    )

    for remote_art in config.artifacts:
        local_target = out_dir / pathlib.Path(remote_art).name
        steps.append(
            {
                "stage": "download_artifact",
                "cmd": [*base, "download", "-s", session_name, remote_art, str(local_target)],
                "always": False,
            }
        )

    if not config.keep_session:
        steps.append(
            {
                "stage": "stop_session",
                "cmd": [*base, "stop", "-s", session_name],
                "always": True,
            }
        )
    elif config.env:
        # When keeping VM alive, ALWAYS purge uploaded env file in finally block via
        # `colab exec -s <session> -f <cleanup_env.py>` (colab 0.8.0 uses -f, not -c).
        cleanup_ref = str(cleanup_env_local_path) if cleanup_env_local_path else "<cleanup_env.py>"
        steps.append(
            {
                "stage": "cleanup_env",
                "cmd": [*base, "exec", "-s", session_name, "-f", cleanup_ref],
                "always": True,
            }
        )

    rclone_plan = (
        build_rclone_sync_plan(out_dir, config.rclone_remote, run_id, rclone_bin=rclone_bin)
        if config.rclone_remote
        else None
    )

    return {
        "run_id": run_id,
        "script_path": str(script_path),
        "script_relpath": script_rel,
        "script_sha256": script_sha,
        "use_repo_bundle": use_repo_bundle,
        "accelerator": accel,
        "high_mem": config.high_mem,
        "auth": config.auth,
        "session": session_name,
        "out_dir": str(out_dir),
        "estimated_cu": estimated_cu,
        "max_cu": config.max_cu,
        "steps": [
            {
                "stage": s["stage"],
                "cmd": s["cmd"],
                "portable_command": _sanitize_cmd_for_report(s["cmd"], config.repo_root, out_dir),
                "always": bool(s["always"]),
            }
            for s in steps
        ],
        "rclone_sync": rclone_plan,
    }


def _parse_reported_cu(output_text: str) -> float:
    matches = _CU_USAGE_RE.findall(output_text)
    if not matches:
        return 0.0
    try:
        return round(float(matches[-1]), 4)
    except ValueError:
        return 0.0


def _collect_artifact_hashes(
    out_dir: pathlib.Path, remote_artifacts: tuple[str, ...]
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for remote_art in remote_artifacts:
        local_target = out_dir / pathlib.Path(remote_art).name
        if local_target.is_file():
            records.append(
                {
                    "name": local_target.name,
                    "remote_path": remote_art,
                    "sha256": _sha256_file(local_target),
                    "size_bytes": local_target.stat().st_size,
                    "present": True,
                }
            )
        else:
            records.append(
                {
                    "name": local_target.name,
                    "remote_path": remote_art,
                    "sha256": None,
                    "size_bytes": 0,
                    "present": False,
                }
            )
    return records


def execute_remote_run(
    config: RemoteRunConfig,
    *,
    subprocess_runner: Any = subprocess.run,
    colab_bin_override: str | None = None,
    rclone_bin_override: str | None = None,
) -> RemoteRunReport:
    """Plan and (if `config.live=True`) execute a remote Colab run with full JSON telemetry."""
    colab_bin = colab_bin_override if colab_bin_override is not None else find_colab_bin()
    rclone_bin = rclone_bin_override if rclone_bin_override is not None else find_rclone_bin()

    if config.live and not colab_bin:
        raise RemoteComputeError(
            "`colab` CLI not found; install google-colab-cli or set COLAB_BIN before using --live"
        )
    if config.live and config.rclone_remote and not rclone_bin:
        raise RemoteComputeError(
            "`rclone` CLI not found; install rclone or set RCLONE_BIN before syncing artifacts"
        )

    out_dir_resolved = config.out_dir.expanduser().resolve()
    safe_params = _sanitize_value(dict(config.params), config.repo_root, out_dir_resolved)
    ts_utc = dt.datetime.now(dt.UTC).isoformat(timespec="seconds")

    if not config.live:
        plan = build_execution_plan(
            config,
            colab_bin=colab_bin or "colab",
            rclone_bin=rclone_bin or "rclone",
        )
        rclone_summary = None
        if plan["rclone_sync"] is not None:
            rclone_summary = {
                "remote": plan["rclone_sync"]["remote"],
                "portable_command": plan["rclone_sync"]["portable_command"],
                "executed": False,
                "exit_code": None,
            }
        return RemoteRunReport(
            schema_version=1,
            run_id=plan["run_id"],
            mode="dry_run",
            script_relpath=plan["script_relpath"],
            script_sha256=plan["script_sha256"],
            accelerator=plan["accelerator"],
            high_mem=plan["high_mem"],
            auth=plan["auth"],
            seed=config.seed,
            params=safe_params,
            timeout_sec=config.timeout_sec,
            max_cu=config.max_cu,
            estimated_cu=plan["estimated_cu"],
            reported_cu=0.0,
            duration_sec=0.0,
            exit_code=0,
            stop_failed=False,
            colab_installed=bool(colab_bin),
            steps=[
                {"stage": s["stage"], "command": s["portable_command"], "always": s["always"]}
                for s in plan["steps"]
            ],
            artifacts=[
                {
                    "name": pathlib.Path(a).name,
                    "remote_path": _sanitize_value(a, config.repo_root, out_dir_resolved),
                    "sha256": None,
                    "size_bytes": 0,
                    "present": False,
                }
                for a in config.artifacts
            ],
            rclone_sync=rclone_summary,
            timestamp_utc=ts_utc,
        )

    with tempfile.TemporaryDirectory(prefix="aro-colab-stage-") as stage_tmp:
        stage_dir = pathlib.Path(stage_tmp)
        script_path = config.script.expanduser().resolve()
        use_repo_bundle = (
            bool(config.bundle_repo)
            if config.bundle_repo is not None
            else _is_inside_repo(script_path, config.repo_root)
        )
        bundle_path: pathlib.Path | None = None
        if use_repo_bundle:
            bundle_path = create_repo_bundle(config.repo_root, stage_dir / "aro_repo.tar.gz")
            target_in_vm = _portable_path(script_path, config.repo_root)
        else:
            target_in_vm = f"/content/{script_path.name}"

        env_path: pathlib.Path | None = None
        cleanup_env_path: pathlib.Path | None = None
        if config.env:
            env_dict: dict[str, str] = {}
            for kv in config.env:
                if "=" not in kv or not kv.split("=", 1)[0].strip():
                    raise RemoteComputeError(f"Invalid --env entry {kv!r}; expected KEY=VALUE")
                k, v = kv.split("=", 1)
                env_dict[k] = v
            env_path = stage_dir / "aro_env.json"
            env_path.write_text(json.dumps(env_dict), encoding="utf-8")
            env_path.chmod(0o600)
            if config.keep_session:
                cleanup_env_path = stage_dir / "cleanup_env.py"
                cleanup_env_path.write_text(
                    "import os\n"
                    "p = '/content/.aro_env.json'\n"
                    "if os.path.exists(p):\n"
                    "    os.remove(p)\n"
                    "if not os.path.exists(p):\n"
                    "    print('ARO_REMOTE_CLEANUP_OK=1', flush=True)\n",
                    encoding="utf-8",
                )

        bootstrap_path = stage_dir / "colab_bootstrap.py"
        bootstrap_src = build_colab_bootstrap_source(
            script_rel_or_remote=target_in_vm,
            script_args=config.script_args,
            has_env_file=bool(config.env),
            unpack_repo_tarball=use_repo_bundle,
        )
        bootstrap_path.write_text(bootstrap_src, encoding="utf-8")

        plan = build_execution_plan(
            config,
            colab_bin=colab_bin or "colab",
            rclone_bin=rclone_bin or "rclone",
            bootstrap_local_path=bootstrap_path,
            bundle_local_path=bundle_path,
            env_local_path=env_path,
            cleanup_env_local_path=cleanup_env_path,
        )

        out_dir = pathlib.Path(plan["out_dir"])
        if config.artifacts:
            out_dir.mkdir(parents=True, exist_ok=True)

        normal_steps = [s for s in plan["steps"] if not s["always"]]
        always_steps = [s for s in plan["steps"] if s["always"]]
        collected_output: list[str] = []
        exit_code = 0
        stop_failed = False
        t0 = time.monotonic()
        deadline = t0 + float(config.timeout_sec)

        try:
            for step in normal_steps:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    collected_output.append(
                        f"Wall-clock deadline ({config.timeout_sec}s) expired "
                        f"before {step['stage']}"
                    )
                    exit_code = 124
                    break
                try:
                    proc = subprocess_runner(
                        step["cmd"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=remaining,
                    )
                except subprocess.TimeoutExpired:
                    collected_output.append(
                        f"Wall-clock timeout ({config.timeout_sec}s) exceeded in {step['stage']}"
                    )
                    exit_code = 124
                    break
                if proc.stdout:
                    collected_output.append(proc.stdout)
                if proc.stderr:
                    collected_output.append(proc.stderr)
                if proc.returncode != 0:
                    exit_code = int(proc.returncode)
                    break
                if step["stage"] == "exec_bootstrap":
                    m_rc = _SENTINEL_RC_RE.findall(proc.stdout or "")
                    if not m_rc:
                        collected_output.append(
                            "ERROR: exec_bootstrap exited without ARO_REMOTE_EXIT_CODE sentinel"
                        )
                        exit_code = 1
                        break
                    remote_rc = int(m_rc[-1])
                    if remote_rc != 0:
                        exit_code = remote_rc
                        break
        finally:
            for step in always_steps:
                try:
                    stop_proc = subprocess_runner(
                        step["cmd"],
                        capture_output=True,
                        text=True,
                        check=False,
                        timeout=60.0,
                    )
                    cleanup_missing_ok = step[
                        "stage"
                    ] == "cleanup_env" and "ARO_REMOTE_CLEANUP_OK=1" not in (stop_proc.stdout or "")
                    if stop_proc.returncode != 0 or cleanup_missing_ok:
                        stop_failed = True
                        if exit_code == 0:
                            exit_code = (
                                int(stop_proc.returncode) if stop_proc.returncode != 0 else 1
                            )
                except subprocess.TimeoutExpired:
                    stop_failed = True
                    if exit_code == 0:
                        exit_code = 124

        rclone_summary = None
        if plan["rclone_sync"] is not None:
            rclone_summary = {
                "remote": plan["rclone_sync"]["remote"],
                "portable_command": plan["rclone_sync"]["portable_command"],
                "executed": False,
                "exit_code": None,
            }
            if exit_code == 0 and out_dir.exists():
                rc_proc = subprocess_runner(
                    plan["rclone_sync"]["cmd"],
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=max(30.0, float(config.timeout_sec)),
                )
                rclone_summary["executed"] = True
                rclone_summary["exit_code"] = int(rc_proc.returncode)
                if rc_proc.returncode != 0:
                    exit_code = int(rc_proc.returncode)

        duration_sec = round(time.monotonic() - t0, 3)
        reported_cu = _parse_reported_cu("\n".join(collected_output))
        artifacts = _sanitize_value(
            _collect_artifact_hashes(out_dir, config.artifacts), config.repo_root, out_dir
        )

        return RemoteRunReport(
            schema_version=1,
            run_id=plan["run_id"],
            mode="live",
            script_relpath=plan["script_relpath"],
            script_sha256=plan["script_sha256"],
            accelerator=plan["accelerator"],
            high_mem=plan["high_mem"],
            auth=plan["auth"],
            seed=config.seed,
            params=safe_params,
            timeout_sec=config.timeout_sec,
            max_cu=config.max_cu,
            estimated_cu=plan["estimated_cu"],
            reported_cu=reported_cu,
            duration_sec=duration_sec,
            exit_code=exit_code,
            stop_failed=stop_failed,
            colab_installed=bool(colab_bin),
            steps=[
                {"stage": s["stage"], "command": s["portable_command"], "always": s["always"]}
                for s in plan["steps"]
            ],
            artifacts=artifacts,
            rclone_sync=rclone_summary,
            timestamp_utc=ts_utc,
        )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python3 -m research.remote.colab_runner",
        description=(
            "Headless Google Colab GPU/CPU runner for ARO falsifier grids. "
            "Runs in --dry-run mode by default; pass --live for real cloud execution."
        ),
    )
    p.add_argument("script", nargs="?", help="Local Python script to run on Colab.")
    p.add_argument(
        "--grid-preset",
        choices=sorted(GRID_PRESETS),
        default=None,
        help="Named repo falsifier preset (alternative to positional script).",
    )
    p.add_argument("--gpu", choices=GPU_CHOICES, default=None, help="Colab GPU accelerator.")
    p.add_argument("--tpu", choices=TPU_CHOICES, default=None, help="Colab TPU accelerator.")
    p.add_argument("--cpu", action="store_true", help="Use Colab CPU runtime (default).")
    p.add_argument("--high-mem", action="store_true", help="Request high-RAM machine shape.")
    p.add_argument("--auth", choices=AUTH_CHOICES, default="adc", help="Auth mode (default: adc).")
    p.add_argument(
        "--timeout",
        type=float,
        default=300.0,
        help="Wall-clock timeout in seconds, finite > 0 (default: 300).",
    )
    p.add_argument(
        "--max-cu",
        type=float,
        default=0.5,
        help="Hard Compute Unit (CU) budget ceiling, finite > 0 (default: 0.5).",
    )
    p.add_argument(
        "--seed",
        type=int,
        default=20261124,
        help="Deterministic seed recorded in report.",
    )
    p.add_argument(
        "--params-json",
        default="{}",
        help="JSON object of workload grid parameters recorded in report.",
    )
    p.add_argument("--session", "-s", default=None, help="Optional Colab session name.")
    p.add_argument("--keep", action="store_true", help="Keep VM alive after run.")
    p.add_argument("--env", action="append", default=[], help="Remote env KEY=VALUE.")
    p.add_argument("--upload", action="append", default=[], help="Upload LOCAL:REMOTE.")
    p.add_argument("--artifact", action="append", default=[], help="Remote artifact to download.")
    p.add_argument(
        "--out-dir",
        default="tmp/colab-artifacts",
        help="Local directory for downloaded artifacts (default: tmp/colab-artifacts).",
    )
    p.add_argument(
        "--rclone-remote",
        default=None,
        help="Optional rclone destination (e.g. gdrive:aro-discovery/artifacts).",
    )
    p.add_argument(
        "--report-out",
        default=None,
        help="Optional path to write deterministic JSON report.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Validate inputs, budget, and print execution plan (default).",
    )
    p.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Execute on real Google Colab runtime (overrides --dry-run).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    if "--" in raw_argv:
        sep = raw_argv.index("--")
        cli_argv, script_args = raw_argv[:sep], tuple(raw_argv[sep + 1 :])
    else:
        cli_argv, script_args = raw_argv, ()

    parser = build_parser()
    args = parser.parse_args(cli_argv)

    try:
        user_params = json.loads(args.params_json)
        if not isinstance(user_params, dict):
            raise RemoteComputeError("--params-json must decode to a JSON object")

        if args.grid_preset:
            script_path, preset_params = resolve_grid_preset(args.grid_preset)
            params = {**preset_params, **user_params, "grid_preset": args.grid_preset}
        elif args.script:
            script_path = pathlib.Path(args.script)
            params = dict(user_params)
        else:
            parser.print_help()
            return 0

        if args.tpu:
            accel = args.tpu
        elif args.gpu and not args.cpu:
            accel = args.gpu
        else:
            accel = "CPU"

        cfg = RemoteRunConfig(
            script=script_path,
            accelerator=accel,
            high_mem=bool(args.high_mem),
            auth=args.auth,
            timeout_sec=float(args.timeout),
            max_cu=float(args.max_cu),
            keep_session=bool(args.keep),
            session=args.session,
            env=tuple(args.env),
            uploads=tuple(args.upload),
            artifacts=tuple(args.artifact),
            out_dir=pathlib.Path(args.out_dir),
            rclone_remote=args.rclone_remote,
            seed=int(args.seed),
            params=params,
            script_args=script_args,
            live=bool(args.live),
        )
        report = execute_remote_run(cfg)
    except (RemoteComputeError, ValueError, OSError) as exc:
        print(f"REMOTE COMPUTE ERROR: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps(report.to_dict(), indent=2, ensure_ascii=False)
    if args.report_out:
        out_p = pathlib.Path(args.report_out)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return report.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
