"""Remote compute adapter for headless Google Colab GPU/CPU falsifier workloads."""

from __future__ import annotations

from research.remote.colab_runner import (
    ACCELERATOR_CU_PER_HOUR,
    GPU_CHOICES,
    GRID_PRESETS,
    TPU_CHOICES,
    RemoteComputeBudgetError,
    RemoteComputeError,
    RemoteRunConfig,
    RemoteRunReport,
    build_execution_plan,
    build_rclone_sync_plan,
    estimate_cu_cost,
    execute_remote_run,
    find_colab_bin,
    find_rclone_bin,
    resolve_grid_preset,
)

__all__ = [
    "ACCELERATOR_CU_PER_HOUR",
    "GPU_CHOICES",
    "GRID_PRESETS",
    "TPU_CHOICES",
    "RemoteComputeBudgetError",
    "RemoteComputeError",
    "RemoteRunConfig",
    "RemoteRunReport",
    "build_execution_plan",
    "build_rclone_sync_plan",
    "estimate_cu_cost",
    "execute_remote_run",
    "find_colab_bin",
    "find_rclone_bin",
    "resolve_grid_preset",
]
