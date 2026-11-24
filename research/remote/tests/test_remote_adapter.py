"""Offline unit tests for research.remote.colab_runner (#1714)."""

from __future__ import annotations

import json
import pathlib
import types

import pytest

from research.remote.colab_runner import (
    GRID_PRESETS,
    RemoteComputeBudgetError,
    RemoteComputeError,
    RemoteRunConfig,
    build_colab_bootstrap_source,
    estimate_cu_cost,
    execute_remote_run,
    main,
    resolve_grid_preset,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def test_dry_run_default_is_deterministic_and_redacts_env_and_paths() -> None:
    script_path, params = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)
    fake_home = "/" + "home" + "/someone/secret.key"
    fake_media = "/" + "media" + "/someone/private/data.csv"
    cfg = RemoteRunConfig(
        script=script_path,
        accelerator="CPU",
        timeout_sec=120.0,
        max_cu=0.5,
        seed=42,
        env=(f"SECRET_TOKEN={fake_home}",),
        params={**params, "debug_path": fake_media},
        live=False,
        repo_root=REPO_ROOT,
    )
    r1 = execute_remote_run(cfg)
    r2 = execute_remote_run(cfg)
    assert r1.mode == "dry_run"
    assert r1.run_id == r2.run_id
    assert r1.script_sha256 == r2.script_sha256
    assert r1.reported_cu == 0.0
    assert r1.exit_code == 0
    assert r1.stop_failed is False
    raw = json.dumps(r1.to_dict())
    assert "/home/" not in raw
    assert "/media/" not in raw
    assert "secret.key" not in raw


def test_cu_budget_guard_rejects_expensive_nan_inf_and_zero_timeout() -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)
    assert estimate_cu_cost("H100", 3600.0) == 25.0
    with pytest.raises(RemoteComputeBudgetError):
        execute_remote_run(
            RemoteRunConfig(script=script_path, accelerator="H100", timeout_sec=1800.0, max_cu=0.5)
        )
    for bad_timeout in (0.0, -5.0, float("nan"), float("inf")):
        with pytest.raises(RemoteComputeError):
            execute_remote_run(
                RemoteRunConfig(script=script_path, timeout_sec=bad_timeout, max_cu=0.5)
            )
    for bad_cu in (0.0, -1.0, float("nan"), float("inf")):
        with pytest.raises(RemoteComputeError):
            execute_remote_run(RemoteRunConfig(script=script_path, timeout_sec=60.0, max_cu=bad_cu))


def test_bootstrap_source_has_no_future_import_and_no_inline_env_secrets() -> None:
    src = build_colab_bootstrap_source(
        script_rel_or_remote="research/discovery/run02/run02_falsify.py",
        script_args=("--json",),
        has_env_file=True,
        unpack_repo_tarball=True,
    )
    assert "from __future__" not in src
    assert "/content/.aro_env.json" in src
    assert "ARO_REMOTE_EXIT_CODE=" in src
    # Simulate colab 0.8.0 prologue injection before script body
    injected = "import os as _colab_os\n" + src
    compile(injected, "<colab_bootstrap>", "exec")


def test_mocked_live_lifecycle_downloads_artifacts_stops_vm_and_syncs_rclone(
    tmp_path: pathlib.Path,
) -> None:
    script_path, params = resolve_grid_preset("run02-all", repo_root=REPO_ROOT)
    upload_src = tmp_path / "params.json"
    upload_src.write_text('{"seed": 1}\n', encoding="utf-8")
    out_dir = tmp_path / "artifacts"
    calls: list[tuple[list[str], float | None]] = []

    def fake_run(cmd: list[str], **kwargs: object) -> object:
        calls.append((list(cmd), kwargs.get("timeout")))  # type: ignore[arg-type]
        if "download" in cmd:
            target = pathlib.Path(cmd[-1])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('{"ok": true}\n', encoding="utf-8")
        return types.SimpleNamespace(
            returncode=0,
            stdout="CU: 0.03\nARO_REMOTE_EXIT_CODE=0\n",
            stderr="",
        )

    cfg = RemoteRunConfig(
        script=script_path,
        accelerator="T4",
        timeout_sec=120.0,
        max_cu=0.5,
        uploads=(f"{upload_src}:/content/params.json",),
        artifacts=("/content/run02_report.json",),
        out_dir=out_dir,
        rclone_remote="gdrive:aro-discovery/run02",
        params=params,
        live=True,
        repo_root=REPO_ROOT,
    )
    rep = execute_remote_run(
        cfg,
        subprocess_runner=fake_run,
        colab_bin_override="colab",
        rclone_bin_override="rclone",
    )
    assert rep.mode == "live"
    assert rep.exit_code == 0
    assert rep.stop_failed is False
    assert rep.reported_cu == 0.03
    assert len(rep.artifacts) == 1 and rep.artifacts[0]["present"] is True
    assert any("stop" in c for c, _ in calls)
    assert any("/content/aro_repo.tar.gz" in c for c, _ in calls)
    assert all(t is not None and t > 0 for _, t in calls)
    assert rep.rclone_sync is not None and rep.rclone_sync["executed"] is True


def test_stop_failure_is_surfaced_in_exit_code() -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)

    def stop_fail_runner(cmd: list[str], **_kwargs: object) -> object:
        rc = 7 if "stop" in cmd else 0
        out = "ARO_REMOTE_EXIT_CODE=0\n" if "exec" in cmd else ""
        return types.SimpleNamespace(returncode=rc, stdout=out, stderr="")

    rep = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=60.0,
            max_cu=0.5,
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=stop_fail_runner,
        colab_bin_override="colab",
    )
    assert rep.stop_failed is True
    assert rep.exit_code == 7


def test_cli_dry_run_preset_writes_report(tmp_path: pathlib.Path) -> None:
    report_path = tmp_path / "report.json"
    rc = main(
        [
            "--grid-preset",
            "o4-schedule",
            "--cpu",
            "--max-cu",
            "0.2",
            "--report-out",
            str(report_path),
        ]
    )
    assert rc == 0
    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["mode"] == "dry_run"
    assert data["params"]["grid_preset"] == "o4-schedule"
    assert set(GRID_PRESETS) >= {
        "t1-t7",
        "o4-schedule",
        "o1-adr",
        "g1-multistage",
        "g2-conic",
        "run02-all",
    }


def test_invalid_rclone_remote_rejected() -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)
    with pytest.raises(RemoteComputeError):
        execute_remote_run(
            RemoteRunConfig(
                script=script_path,
                rclone_remote="gdrive:foo;echo pwned",
                live=False,
            )
        )


def test_colab_exec_sentinel_propagates_remote_failure_and_redacts_tmp() -> None:
    script_path, _ = resolve_grid_preset("g1-multistage", repo_root=REPO_ROOT)

    def sentinel_fail_runner(cmd: list[str], **_kwargs: object) -> object:
        # Simulate colab 0.8.0 returning 0 even when remote script exited 7
        out = "ARO_REMOTE_EXIT_CODE=7\n" if "exec" in cmd else ""
        return types.SimpleNamespace(returncode=0, stdout=out, stderr="")

    fake_secret_dir = "/" + "home" + "/secret"
    rep = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=60.0,
            max_cu=0.5,
            params={f"{fake_secret_dir}/key": "val"},
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=sentinel_fail_runner,
        colab_bin_override="colab",
    )
    assert rep.exit_code == 7
    raw = json.dumps(rep.to_dict())
    assert "/tmp/" not in raw
    assert fake_secret_dir not in raw


def test_expired_wall_clock_deadline_aborts_remaining_steps(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)
    ticks = iter([0.0, 0.0, 5.0, 5.0, 5.0])
    monkeypatch.setattr("research.remote.colab_runner.time.monotonic", lambda: next(ticks))
    seen: list[list[str]] = []

    def runner(cmd: list[str], **_kwargs: object) -> object:
        seen.append(list(cmd))
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")

    rep = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=1.0,
            max_cu=0.5,
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=runner,
        colab_bin_override="colab",
    )
    assert rep.exit_code == 124
    assert not any("exec" in c for c in seen)
    assert any("stop" in c for c in seen)


def test_missing_sentinel_or_negative_signal_rc_fails_closed() -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)

    # Case 1: bootstrap crashes before printing sentinel
    rep_missing = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=60.0,
            max_cu=0.5,
            artifacts=("/content/out.json",),
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=lambda _cmd, **_kw: types.SimpleNamespace(
            returncode=0, stdout="Traceback...\n", stderr=""
        ),
        colab_bin_override="colab",
    )
    assert rep_missing.exit_code == 1

    # Case 2: child killed by SIGKILL (-9)
    rep_sig = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=60.0,
            max_cu=0.5,
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=lambda cmd, **_kw: types.SimpleNamespace(
            returncode=0,
            stdout="ARO_REMOTE_EXIT_CODE=-9\n" if "exec" in cmd else "",
            stderr="",
        ),
        colab_bin_override="colab",
    )
    assert rep_sig.exit_code == -9


def test_keep_session_with_env_always_cleans_up_env_file_after_deadline(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)
    # Expire deadline right after upload_env (before exec_bootstrap)
    ticks = iter([0.0, 0.0, 0.1, 0.2, 5.0, 5.0, 5.0])
    monkeypatch.setattr("research.remote.colab_runner.time.monotonic", lambda: next(ticks))
    seen: list[list[str]] = []
    cleanup_sources: list[str] = []

    def runner(cmd: list[str], **_kwargs: object) -> object:
        seen.append(list(cmd))
        if "exec" in cmd and "-f" in cmd:
            fpath = pathlib.Path(cmd[cmd.index("-f") + 1])
            if fpath.name == "cleanup_env.py" and fpath.is_file():
                cleanup_sources.append(fpath.read_text(encoding="utf-8"))
                return types.SimpleNamespace(
                    returncode=0, stdout="ARO_REMOTE_CLEANUP_OK=1\n", stderr=""
                )
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")

    rep = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=1.0,
            max_cu=0.5,
            keep_session=True,
            env=("API_SECRET=topsecret",),
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=runner,
        colab_bin_override="colab",
    )
    assert rep.exit_code == 124
    assert rep.stop_failed is False
    assert any("exec" in c and "-f" in c and "-c" not in c for c in seen)
    assert len(cleanup_sources) == 1
    assert "os.remove(p)" in cleanup_sources[0]
    assert "ARO_REMOTE_CLEANUP_OK=1" in cleanup_sources[0]
    compile(cleanup_sources[0], "<cleanup_env>", "exec")


def test_cleanup_env_missing_sentinel_fails_closed() -> None:
    script_path, _ = resolve_grid_preset("t1-t7", repo_root=REPO_ROOT)

    def cleanup_perm_err_runner(cmd: list[str], **_kwargs: object) -> object:
        if "exec" in cmd and "-f" in cmd:
            fname = pathlib.Path(cmd[cmd.index("-f") + 1]).name
            if fname == "colab_bootstrap.py":
                return types.SimpleNamespace(
                    returncode=0, stdout="ARO_REMOTE_EXIT_CODE=0\n", stderr=""
                )
            # Simulate PermissionError inside cleanup_env.py while colab 0.8.0 CLI returns 0
            return types.SimpleNamespace(returncode=0, stdout="PermissionError\n", stderr="")
        return types.SimpleNamespace(returncode=0, stdout="", stderr="")

    rep = execute_remote_run(
        RemoteRunConfig(
            script=script_path,
            accelerator="CPU",
            timeout_sec=60.0,
            max_cu=0.5,
            keep_session=True,
            env=("API_SECRET=topsecret",),
            live=True,
            repo_root=REPO_ROOT,
        ),
        subprocess_runner=cleanup_perm_err_runner,
        colab_bin_override="colab",
    )
    assert rep.stop_failed is True
    assert rep.exit_code == 1
