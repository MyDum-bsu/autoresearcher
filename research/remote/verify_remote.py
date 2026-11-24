#!/usr/bin/env python3
"""Deterministic verifier & negative self-tests for Remote Compute Adapter (#1714).

Zero `assert` statements — behaves identically under `python3 -B` and `python3 -B -O`.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import tempfile
import types
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.remote.colab_runner import (  # noqa: E402
    GRID_PRESETS,
    RemoteComputeBudgetError,
    RemoteComputeError,
    RemoteRunConfig,
    execute_remote_run,
    resolve_grid_preset,
)


class RemoteVerifyError(RuntimeError):
    """Raised when remote compute adapter verification fails."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise RemoteVerifyError(msg)


def verify_remote_adapter(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, Any]:
    """Run deterministic offline checks across presets, dry-run telemetry, and mocked live sync."""
    checked_presets: list[str] = []
    for preset in sorted(GRID_PRESETS):
        script_path, params = resolve_grid_preset(preset, repo_root=repo_root)
        cfg = RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=180.0,
            max_cu=0.5,
            seed=20261124,
            params={**params, "grid_preset": preset},
            live=False,
            repo_root=repo_root,
        )
        rep1 = execute_remote_run(cfg)
        rep2 = execute_remote_run(cfg)
        _expect(rep1.mode == "dry_run", f"Expected dry_run for {preset}")
        _expect(rep1.run_id == rep2.run_id, f"Non-deterministic run_id for {preset}")
        _expect(rep1.script_sha256 == rep2.script_sha256, f"SHA mismatch for {preset}")
        _expect(rep1.estimated_cu <= rep1.max_cu, f"CU exceeded max_cu for {preset}")
        _expect(rep1.reported_cu == 0.0, f"dry_run reported non-zero CU for {preset}")
        _expect(
            "/home/" not in json.dumps(rep1.to_dict())
            and "/media/" not in json.dumps(rep1.to_dict()),
            f"Host path leaked in report for {preset}",
        )
        checked_presets.append(preset)

    # Mocked live lifecycle test (upload + exec + download + stop + rclone copy)
    with tempfile.TemporaryDirectory(prefix="aro-remote-verify-") as tmp:
        tmp_dir = pathlib.Path(tmp)
        out_dir = tmp_dir / "out"
        upload_file = tmp_dir / "grid_spec.json"
        upload_file.write_text('{"grid": [1, 2]}\n', encoding="utf-8")
        commands_seen: list[list[str]] = []

        def fake_runner(cmd: list[str], **_kwargs: Any) -> Any:
            commands_seen.append(list(cmd))
            if "download" in cmd:
                target = pathlib.Path(cmd[-1])
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('{"status": "ok"}\n', encoding="utf-8")
            return types.SimpleNamespace(
                returncode=0,
                stdout="Compute Units: 0.04\nARO_REMOTE_EXIT_CODE=0\nDONE\n",
                stderr="",
            )

        script_path, params = resolve_grid_preset("t1-t7", repo_root=repo_root)
        cfg_live = RemoteRunConfig(
            script=script_path,
            accelerator="L4",
            timeout_sec=120.0,
            max_cu=0.5,
            uploads=(f"{upload_file}:/content/grid_spec.json",),
            artifacts=("/content/result.json",),
            out_dir=out_dir,
            rclone_remote="gdrive:aro-discovery/test-artifacts",
            params=params,
            live=True,
            repo_root=repo_root,
        )
        rep_live = execute_remote_run(
            cfg_live,
            subprocess_runner=fake_runner,
            colab_bin_override="colab",
            rclone_bin_override="rclone",
        )
        _expect(rep_live.mode == "live", "Expected live mode")
        _expect(rep_live.exit_code == 0, f"Expected exit_code 0, got {rep_live.exit_code}")
        _expect(
            rep_live.reported_cu == 0.04, f"Expected parsed CU 0.04, got {rep_live.reported_cu}"
        )
        _expect(
            any("stop" in c for c in commands_seen),
            "Lifecycle run MUST auto-stop Colab VM",
        )
        _expect(
            rep_live.rclone_sync is not None
            and rep_live.rclone_sync["executed"] is True
            and rep_live.rclone_sync["exit_code"] == 0,
            f"Expected rclone sync success, got {rep_live.rclone_sync}",
        )
        _expect(
            len(rep_live.artifacts) == 1 and rep_live.artifacts[0]["present"] is True,
            f"Downloaded artifact missing in report: {rep_live.artifacts}",
        )

    return {
        "presets_verified": checked_presets,
        "mocked_live_lifecycle": "OK",
    }


def run_self_test() -> int:
    """Negative controls (5/5): CU budget, missing script, bad upload, rclone, auto-stop."""
    script_path, _ = resolve_grid_preset("t1-t7")

    # 1. CU budget overflow MUST raise RemoteComputeBudgetError
    try:
        execute_remote_run(
            RemoteRunConfig(
                script=script_path,
                accelerator="H100",
                timeout_sec=3600.0,
                max_cu=0.5,
                live=False,
            )
        )
    except RemoteComputeBudgetError:
        pass
    else:
        raise RemoteVerifyError("CU budget overflow was NOT rejected")

    # 2. Missing script MUST raise RemoteComputeError
    try:
        execute_remote_run(RemoteRunConfig(script=pathlib.Path("nonexistent_script_xyz.py")))
    except RemoteComputeError:
        pass
    else:
        raise RemoteVerifyError("Missing script was NOT rejected")

    # 3. Malformed upload spec MUST raise RemoteComputeError
    try:
        execute_remote_run(RemoteRunConfig(script=script_path, uploads=("missing_colon_spec",)))
    except RemoteComputeError:
        pass
    else:
        raise RemoteVerifyError("Malformed upload spec was NOT rejected")

    # 4. Unsafe rclone remote MUST raise RemoteComputeError
    try:
        execute_remote_run(RemoteRunConfig(script=script_path, rclone_remote="gdrive:bad;rm -rf /"))
    except RemoteComputeError:
        pass
    else:
        raise RemoteVerifyError("Unsafe rclone remote was NOT rejected")

    # 5. Failed remote exec MUST still call `colab stop` in finally block
    with tempfile.TemporaryDirectory(prefix="aro-remote-fail-") as tmp:
        seen: list[list[str]] = []

        def failing_runner(cmd: list[str], **_kwargs: Any) -> Any:
            seen.append(list(cmd))
            rc = 7 if "exec" in cmd else 0
            return types.SimpleNamespace(returncode=rc, stdout="", stderr="boom")

        rep = execute_remote_run(
            RemoteRunConfig(
                script=script_path,
                accelerator="CPU",
                timeout_sec=60.0,
                max_cu=0.5,
                artifacts=("/content/out.json",),
                out_dir=pathlib.Path(tmp) / "out",
                live=True,
            ),
            subprocess_runner=failing_runner,
            colab_bin_override="colab",
        )
        _expect(rep.exit_code == 7, f"Expected exit_code 7, got {rep.exit_code}")
        _expect(any("stop" in c for c in seen), "VM stop was NOT called after exec failure")

    # 6. NaN/zero timeout MUST be rejected, and `stop` failure MUST surface in exit_code
    for bad_timeout in (0.0, float("nan")):
        try:
            execute_remote_run(
                RemoteRunConfig(script=script_path, timeout_sec=bad_timeout, max_cu=0.5)
            )
        except RemoteComputeError:
            pass
        else:
            raise RemoteVerifyError(f"Bad timeout {bad_timeout} was NOT rejected")

    rep_stop_fail = execute_remote_run(
        RemoteRunConfig(
            script=script_path, accelerator="CPU", timeout_sec=60.0, max_cu=0.5, live=True
        ),
        subprocess_runner=lambda cmd, **_kw: types.SimpleNamespace(
            returncode=9 if "stop" in cmd else 0,
            stdout="ARO_REMOTE_EXIT_CODE=0\n" if "exec" in cmd else "",
            stderr="",
        ),
        colab_bin_override="colab",
    )
    _expect(
        rep_stop_fail.stop_failed is True and rep_stop_fail.exit_code == 9,
        f"Failed stop was NOT surfaced: {rep_stop_fail}",
    )

    print(
        "REMOTE COMPUTE VERIFIER SELF-TEST OK: 6/6 negative controls rejected "
        "(CU budget / missing script / bad upload / unsafe rclone / auto-stop / NaN+stop-fail)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Remote Compute Adapter (#1714).")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return run_self_test()
        summary = verify_remote_adapter(REPO_ROOT)
    except (RemoteVerifyError, RemoteComputeError, OSError) as exc:
        print(f"REMOTE COMPUTE VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"status": "ok", **summary}, indent=2, ensure_ascii=False))
    else:
        print(
            f"REMOTE COMPUTE VERIFY OK: {len(summary['presets_verified'])} presets verified, "
            "portable reports (0 host paths), mocked live lifecycle + auto-stop + rclone OK"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
