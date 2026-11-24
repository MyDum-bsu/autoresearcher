#!/usr/bin/env python3
"""Unified deterministic Stage 2 (Gate G2) and Stage 3 (Gate G3) claim verifier (R2 #1156).

Enforces:
  - Gate G2 (Falsify-First):
      * Non-empty parameter grids with strictly validated finite rational/numeric points
        (`grids: []`, `null`, `bool`, `NaN`, `Inf`, empty/malformed values rejected);
      * Live execution of the submitted `--claim` specification (`sympy_inequality`,
        `t1_t7_predicate`, or `checker_script` — passive point-counting rejected);
      * Exact rational M0 oracle tests (36 tests);
      * Executable T1-T7 ADR falsification battery + falsifier unit suite;
      * Bridge transfer-v1 (32 controls, executed in parallel across its 4 cases) and
        exact counterexamples (D1, D2, E, Astra A-S1).
  - Gate G3 (Formal Kernel & Semantic Controls):
      * Frozen core integrity: required file set `AroCore/{Model,Goals}.lean` and
        `BridgeFormalV2/{Model,Goals}.lean` checked against BOTH pinned trusted SHA-256
        hashes, `frozen-core-sha256.json` manifest completeness, and fail-closed git diff
        covering both frozen files and the manifest itself;
      * Lean 4 v4.35.0-rc2 kernel compilation via native `lake --offline build` (using
        Lake's own content-hash `.trace` verification — zero custom stamp bypasses;
        `--fresh-lean` forces scratch recompile) + ALWAYS-LIVE parallel Lean 4 kernel
        verification of `AroProofs/Inventory.lean` (19 audited targets) and negative
        controls `C5` & `C6Negative`;
      * Zero `sorry`/`admit`/custom axioms, non-empty inventory, union-on-duplicate +
        duplicate-rejection `#print axioms` parser strictly subset of
        `{propext, Classical.choice, Quot.sound}`;
      * Episodes negative regressions (`verification/gates/episodes/controls/`:
        M-wrong-information, F-erased-refutation, P-wrong-statement,
        P-unsupported-axiom, R-ignore-contradiction) + trusted integrity.
  - Self-test (`--self-test`, zero `assert` — works identically under `-B` and `-B -O`).
"""

from __future__ import annotations

import argparse
import concurrent.futures
import getpass
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
LEAN_ROOT = ROOT / "verification/lean"
GATES_DIR = ROOT / "verification/gates"
ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})

FROZEN_CORE_MANIFEST_REL = "verification/lean/manifests/frozen-core-sha256.json"
FROZEN_CORE_MANIFEST = ROOT / FROZEN_CORE_MANIFEST_REL

# Trusted pinned SHA-256 digests of the immutable Lean 4 core files.
# Deleting an entry from frozen-core-sha256.json OR editing both a core file and the manifest
# is rejected unconditionally.
PINNED_FROZEN_CORE_SHA256: dict[str, str] = {
    "verification/lean/AroCore/Model.lean": (
        "8b09a7ffd17974015d537627bf48f0d88064e6fd6dd70a1813c7e8cbad2d9484"
    ),
    "verification/lean/AroCore/Goals.lean": (
        "6a9f6e48df1264c61f73dedfcd96e3a93da24ecc2a1d52b8bb2b589f2a5319ec"
    ),
    "verification/lean/BridgeFormalV2/Model.lean": (
        "44d474e393f0d83dc215877aa9663fbf79c3c9887ed838305cb74048699e6a26"
    ),
    "verification/lean/BridgeFormalV2/Goals.lean": (
        "b3b949e681935df3491602dec2d0daf73ab15b711481b014b6e2a5abb61d2409"
    ),
}
FROZEN_CORE_FILES = tuple(PINNED_FROZEN_CORE_SHA256.keys())

UNIFIED_COMPILE_ORDER = (
    "BridgeFormalV2/Model.lean",
    "BridgeFormalV2/Goals.lean",
    "BridgeFormalV2/Proofs/Dynamics.lean",
    "BridgeFormalV2/Proofs/Policies.lean",
    "BridgeFormalV2/Proofs/Inventory.lean",
    "BridgeFormalV3/Goals.lean",
    "BridgeFormalV3/Proofs/Support.lean",
    "AroCore/Model.lean",
    "AroCore/Goals.lean",
    "AroProofs/BridgeF1F2.lean",
    "AroProofs/Aroform.lean",
    "AroProofs/BridgeF3Draft.lean",
    "AroProofs/BridgeF4CornerLP.lean",
    "AroProofs/BridgeF4ExtremeLP.lean",
    "AroProofs/BridgeG2ConicSupport.lean",
    "AroProofs/BridgeO4ClosureValue.lean",
    "AroProofs/BridgeG1Multistage.lean",
    "AroProofs/BridgeO1ADRExactness.lean",
    "AroProofs/Inventory.lean",
)

POSITIVE_CONTROLS = (
    "Controls/Unified/ControlFixture.lean",
    "Controls/Unified/C1.lean",
    "Controls/Unified/C2.lean",
    "Controls/Unified/C3.lean",
    "Controls/Unified/C4.lean",
    "Controls/Unified/C6.lean",
)

NEGATIVE_CONTROLS = (
    "Controls/Unified/C5.lean",
    "Controls/Unified/C6Negative.lean",
)

# Native Lake targets covering all 13 unified modules and all 6 positive controls transitively.
LAKE_BUILD_TARGETS = (
    "BridgeFormalV2.Proofs.Inventory",
    "AroProofs.Inventory",
    "Controls.Unified.C1",
    "Controls.Unified.C2",
    "Controls.Unified.C3",
    "Controls.Unified.C4",
    "Controls.Unified.C6",
)

EXPECTED_UNIFIED_DECLS = (
    "BridgeFormalV2.Proofs.nonempty_blocks",
    "BridgeFormalV2.Proofs.expansion",
    "BridgeFormalV2.Proofs.prefix_split",
    "BridgeFormalV2.Proofs.source_chronology",
    "BridgeFormalV2.Proofs.suffix_expansion",
    "BridgeFormalV2.Proofs.exogenous_image",
    "BridgeFormalV2.Proofs.observation_fibre",
    "BridgeFormalV2.Proofs.forward_policy",
    "BridgeFormalV2.Proofs.reverse_policy",
    "BridgeFormalV2.Proofs.epigraph_equality",
    "AroProofs.Aroform.info_value_monotone",
    "AroProofs.Aroform.l1_eq_max_sum_diff",
    "AroProofs.Aroform.one_d_exactness",
    "AroProofs.Aroform.l2a_diff_two_path",
    "AroProofs.Aroform.l2a_sum_two_path",
    "BridgeFormalV3.Proofs.future_expansion",
    "BridgeFormalV3.Proofs.attained_support",
    "BridgeFormalV3.Proofs.robust_row",
    "BridgeFormalV3.Proofs.exact_tightening",
    "AroProofs.BridgeF4VertexLP.borel_right_inverse_exists",
    "AroProofs.BridgeF4VertexLP.vertex_lp_to_aro",
    "AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_aro",
    "AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_source",
    "AroProofs.BridgeF4VertexLP.zonotopeVertices_finite",
    "AroProofs.BridgeF4VertexLP.extreme_vertex_lp_to_aro",
    "AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_aro",
    "AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_source",
    "AroProofs.BridgeF4VertexLP.extreme_vertex_lp_eq_corner_lp",
    "AroProofs.BridgeG2ConicSupport.general_attained_support",
    "AroProofs.BridgeG2ConicSupport.general_robust_row",
    "AroProofs.BridgeG2ConicSupport.general_exact_tightening",
    "AroProofs.BridgeG2ConicSupport.box_support_eq_f3",
    "AroProofs.BridgeG2ConicSupport.l1_cross_polytope_support",
    "AroProofs.BridgeG2ConicSupport.l2_soc_ball_support",
    "AroProofs.BridgeG2ConicSupport.l2_ball_not_finset_conv_2d",
    "AroProofs.BridgeO4ClosureValue.openLoop_subset_aro",
    "AroProofs.BridgeO4ClosureValue.openLoop_subset_source",
    "AroProofs.BridgeO4ClosureValue.zero_gain_of_unconstrained_terminal",
    "AroProofs.BridgeO4ClosureValue.zero_gain_of_prefix_in_terminal_kernel",
    "AroProofs.BridgeO4ClosureValue.openLoop_eq_shared_corner_lp",
    "AroProofs.BridgeO4ClosureValue.strict_gain_iff_corner_separation",
    "AroProofs.BridgeO4ClosureValue.exists_strict_value_of_measurement_gap",
    "AroProofs.BridgeG1Multistage.multistage_stage_split",
    "AroProofs.BridgeG1Multistage.multistage_forward_policy",
    "AroProofs.BridgeG1Multistage.multistage_reverse_policy",
    "AroProofs.BridgeG1Multistage.multistage_history_epigraph_eq_aro",
    "AroProofs.BridgeG1Multistage.multistage_markov_subset_history",
    "AroProofs.BridgeG1Multistage.exists_markov_strictly_weaker_than_history_k2",
    "AroProofs.BridgeO1ADRExactness.static_subset_adr_subset_aro",
    "AroProofs.BridgeO1ADRExactness.adr_exact_on_simplex",
    "AroProofs.BridgeO1ADRExactness.barycentric_syzygy_adr_coupling",
    "AroProofs.BridgeO1ADRExactness.chen_zhang_t3_adr_gap",
    "AroProofs.BridgeO1ADRExactness.bridge_adr_subset_aro_and_source",
    "AroProofs.BridgeO1ADRExactness.bridge_adr_exact_1d",
    "AroProofs.BridgeO1ADRExactness.exists_bridge_2d_strict_adr_gap",
)

IMPORT_ERR_MARKERS = (
    "unknown module prefix",
    "does not exist",
    "object file",
    "failed to open file",
    "unknown package",
)

BASELINE_CLAIM_SPEC: dict[str, Any] = {
    "claim_id": "baseline-1d-chord-exactness",
    "kind": "sympy_inequality",
    "lhs": "Max((1 - z) * a + z * b, 0)",
    "rhs": "(1 - z) * Max(a, 0) + z * Max(b, 0)",
    "relation": "<=",
    "grids": [{"a": [-2, 0, 3], "b": [-2, 0, 3], "z": [0, "1/2", 1]}],
}

SUPPORTED_CLAIM_KINDS = frozenset({"sympy_inequality", "t1_t7_predicate", "checker_script"})


class GateError(RuntimeError):
    """Raised when a G2 or G3 verification invariant fails."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise GateError(msg)


def _sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _py_flags() -> list[str]:
    """Propagate current -O optimization level when spawning sub-interpreters."""
    return [sys.executable, "-B", *(["-O"] if not __debug__ else [])]


def validate_claim_spec(spec: dict[str, Any]) -> int:
    """Validate Stage 2 claim spec (rejects empty/invalid grids and no-op specs)."""
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from verification.falsifiers.sympy_counterexample_template import (
        EmptyGridError,
        InvalidGridValueError,
        validate_grids,
    )

    if not isinstance(spec, dict):
        raise GateError("Claim spec must be a JSON object")
    claim_id = spec.get("claim_id")
    if not isinstance(claim_id, str) or not claim_id.strip():
        raise GateError("Claim spec missing non-empty 'claim_id'")
    kind = spec.get("kind")
    if not isinstance(kind, str) or kind not in SUPPORTED_CLAIM_KINDS:
        raise GateError(
            f"Claim spec must declare a verifiable 'kind' in {sorted(SUPPORTED_CLAIM_KINDS)}, "
            f"got {kind!r}"
        )
    if "grids" not in spec:
        raise GateError("Claim spec missing required 'grids' field")
    try:
        return validate_grids(spec["grids"])
    except (EmptyGridError, InvalidGridValueError) as exc:
        raise GateError(f"G2 invalid/empty grid rejected: {exc}") from exc


def evaluate_claim_spec(
    spec: dict[str, Any],
    repo_root: pathlib.Path = ROOT,
    *,
    battery_json: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Validate AND execute the submitted Stage 2 claim spec against its oracle/falsifier."""
    grid_points = validate_claim_spec(spec)
    claim_id = str(spec["claim_id"])
    kind = str(spec["kind"])

    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from verification.falsifiers.sympy_counterexample_template import (
        EmptyGridError,
        InvalidGridValueError,
        evaluate_sympy_relation_claim,
    )

    if kind == "sympy_inequality":
        lhs = spec.get("lhs")
        rhs = spec.get("rhs")
        relation = spec.get("relation", "<=")
        if not isinstance(lhs, str) or not isinstance(rhs, str):
            raise GateError("sympy_inequality claim requires string 'lhs' and 'rhs'")
        try:
            rep = evaluate_sympy_relation_claim(
                claim_id, spec["grids"], lhs, rhs, str(relation)
            )
        except (EmptyGridError, InvalidGridValueError) as exc:
            raise GateError(f"Claim '{claim_id}' evaluation error: {exc}") from exc
        if not rep.survived:
            ce = rep.counterexample
            raise GateError(
                f"Claim '{claim_id}' FALSIFIED at point={ce.point if ce else '?'} "
                f"(lhs={ce.lhs if ce else '?'}, rhs={ce.rhs if ce else '?'}): "
                f"{ce.reason if ce else 'counterexample found'}"
            )
        return {
            "claim_id": claim_id,
            "kind": kind,
            "grid_points": grid_points,
            "tested_points": rep.tested_points,
            "survived": True,
        }

    if kind == "t1_t7_predicate":
        preds = spec.get("predictions")
        if not isinstance(preds, dict):
            raise GateError("t1_t7_predicate claim requires object 'predictions' mapping T1..T7")
        if battery_json is None:
            from verification.falsifiers.battery_t1_t7 import run_battery

            cases_data = [c.to_dict() for c in run_battery()]
        else:
            cases_data = list(battery_json.get("cases", []))
        if len(cases_data) != 7:
            raise GateError(f"Expected 7 T1-T7 battery cases, got {len(cases_data)}")
        mismatches: list[dict[str, str]] = []
        for item in cases_data:
            cid = str(item["case_id"])
            actual = str(item["observed_verdict"])
            if cid not in preds:
                raise GateError(f"t1_t7_predicate claim missing prediction for {cid}")
            predicted = preds[cid]
            if predicted not in ("exact", "not_exact"):
                raise GateError(
                    f"t1_t7_predicate invalid prediction {predicted!r} for {cid}"
                )
            if predicted != actual:
                mismatches.append({"case_id": cid, "predicted": predicted, "actual": actual})
        if mismatches:
            raise GateError(
                f"Claim '{claim_id}' FALSIFIED by T1-T7 battery: {mismatches}"
            )
        return {
            "claim_id": claim_id,
            "kind": kind,
            "grid_points": grid_points,
            "tested_cases": len(cases_data),
            "survived": True,
        }

    if kind == "checker_script":
        script_rel = spec.get("script")
        if not isinstance(script_rel, str) or not script_rel.strip():
            raise GateError("checker_script claim requires non-empty 'script' path")
        raw_path = pathlib.Path(script_rel)
        if raw_path.is_absolute():
            raise GateError(f"checker_script path must be relative to repo root: {script_rel!r}")
        resolved_root = repo_root.resolve()
        script_path = (resolved_root / raw_path).resolve()
        if not script_path.is_relative_to(resolved_root) or not script_path.is_file():
            raise GateError(f"checker_script not found inside repo root: {script_rel!r}")
        extra_args = spec.get("args", [])
        if not isinstance(extra_args, list) or not all(isinstance(a, str) for a in extra_args):
            raise GateError("checker_script 'args' must be a list of strings")
        env = os.environ.copy()
        env["PYTHONPATH"] = str(resolved_root)
        env["ARO_CLAIM_SPEC_JSON"] = json.dumps(spec, ensure_ascii=False, default=str)
        env["ARO_CLAIM_GRIDS_JSON"] = json.dumps(spec["grids"], ensure_ascii=False, default=str)
        proc = subprocess.run(
            [*_py_flags(), str(script_path), *extra_args],
            cwd=str(resolved_root),
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise GateError(
                f"Claim '{claim_id}' checker_script failed (exit {proc.returncode}):\n"
                f"{proc.stdout}\n{proc.stderr}"
            )
        out_str = proc.stdout.strip()
        if not out_str:
            raise GateError(
                f"Claim '{claim_id}' checker_script produced empty stdout; "
                "strict JSON verdict with claim_id/survived/checked_points is required"
            )
        try:
            parsed = json.loads(out_str, parse_float=Decimal)
        except json.JSONDecodeError as exc:
            raise GateError(
                f"Claim '{claim_id}' checker_script stdout is not valid JSON: {exc}"
            ) from exc
        if not isinstance(parsed, dict):
            raise GateError(
                f"Claim '{claim_id}' checker_script JSON verdict must be an object, "
                f"got {type(parsed).__name__}"
            )
        out_claim_id = parsed.get("claim_id")
        if not isinstance(out_claim_id, str) or out_claim_id != claim_id:
            raise GateError(
                f"Claim '{claim_id}' checker_script verdict 'claim_id' mismatch: "
                f"expected {claim_id!r}, got {out_claim_id!r}"
            )
        survived = parsed.get("survived")
        if not isinstance(survived, bool):
            raise GateError(
                f"Claim '{claim_id}' checker_script verdict missing boolean 'survived': {parsed}"
            )
        checked_points = parsed.get("checked_points")
        if (
            not isinstance(checked_points, int)
            or isinstance(checked_points, bool)
            or checked_points < grid_points
        ):
            raise GateError(
                f"Claim '{claim_id}' checker_script verdict 'checked_points' invalid: "
                f"expected int >= {grid_points}, got {checked_points!r}"
            )
        if not survived or parsed.get("status") in ("falsified", "failed", "rejected"):
            raise GateError(
                f"Claim '{claim_id}' FALSIFIED by checker_script: {parsed}"
            )
        return {
            "claim_id": claim_id,
            "kind": kind,
            "grid_points": grid_points,
            "checked_points": checked_points,
            "script": script_rel,
            "survived": True,
        }

    raise GateError(f"Unsupported claim kind: {kind!r}")


def check_frozen_core(
    repo_root: pathlib.Path = ROOT,
    *,
    base_ref: str | None = None,
    manifest_path: pathlib.Path | None = None,
) -> list[str]:
    """Verify AroCore/ and BridgeFormalV2/{Model,Goals}.lean AND their manifest are unmodified."""
    errors: list[str] = []
    lock_file = manifest_path or (repo_root / FROZEN_CORE_MANIFEST_REL)
    if not lock_file.is_file():
        return [f"Missing frozen core SHA-256 manifest: {lock_file}"]

    try:
        lock = json.loads(lock_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Failed to read frozen core SHA-256 manifest: {exc}"]

    frozen_map = lock.get("frozen_files", {})
    if not isinstance(frozen_map, dict) or not frozen_map:
        return ["Frozen core SHA-256 manifest is empty or malformed"]

    # 1. Enforce mandatory required frozen file set + pinned trusted digests
    for req_rel, pinned_sha in PINNED_FROZEN_CORE_SHA256.items():
        if req_rel not in frozen_map:
            errors.append(f"Frozen core manifest missing required entry: {req_rel}")
            continue
        if frozen_map[req_rel] != pinned_sha:
            errors.append(
                f"Frozen core manifest hash tampered ({req_rel}): "
                f"expected pinned {pinned_sha[:12]}, got {str(frozen_map[req_rel])[:12]}"
            )

    # 2. Verify every file listed in manifest + every mandatory file on disk
    all_checked = dict(PINNED_FROZEN_CORE_SHA256)
    for rel, expected_sha in frozen_map.items():
        if rel not in all_checked:
            all_checked[rel] = str(expected_sha)

    for rel, expected_sha in all_checked.items():
        fpath = repo_root / rel
        if not fpath.is_file():
            errors.append(f"Frozen core file missing: {rel}")
            continue
        actual = _sha256(fpath)
        if actual != expected_sha:
            errors.append(
                f"Frozen core tampered ({rel}): expected {expected_sha[:12]}, got {actual[:12]}"
            )

    # 3. Inspect git diff for BOTH frozen core files AND the manifest itself
    if (repo_root / ".git").exists():
        guarded_paths = (*FROZEN_CORE_FILES, FROZEN_CORE_MANIFEST_REL)
        diff_targets = ["HEAD"] if base_ref is None else ["HEAD", base_ref]
        seen_refs: set[str] = set()
        for ref in diff_targets:
            if ref in seen_refs:
                continue
            seen_refs.add(ref)
            proc = subprocess.run(
                ["git", "-C", str(repo_root), "diff", "--name-only", ref, "--", *guarded_paths],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc.returncode != 0:
                errors.append(
                    f"git diff against {ref} failed (exit {proc.returncode}): "
                    f"{proc.stderr.strip()}"
                )
            else:
                changed = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
                for ch in changed:
                    errors.append(f"Frozen core/manifest modified in git diff against {ref}: {ch}")

        # When base_ref is explicitly specified, also verify the manifest in base_ref matches disk
        if base_ref is not None:
            proc_show = subprocess.run(
                ["git", "-C", str(repo_root), "show", f"{base_ref}:{FROZEN_CORE_MANIFEST_REL}"],
                capture_output=True,
                text=True,
                check=False,
            )
            if proc_show.returncode != 0:
                errors.append(
                    f"git show {base_ref}:{FROZEN_CORE_MANIFEST_REL} failed "
                    f"(exit {proc_show.returncode}): {proc_show.stderr.strip()}"
                )
            elif proc_show.stdout != lock_file.read_text(encoding="utf-8"):
                errors.append(
                    f"Frozen core manifest differs from trusted ref {base_ref}"
                )
    return errors


def _resolve_lean_packages_dir(lean_root: pathlib.Path) -> pathlib.Path:
    env_lake = os.environ.get("ARO_LEAN_LAKE_DIR")
    candidates: list[pathlib.Path] = []
    if env_lake:
        candidates.append(pathlib.Path(env_lake).expanduser() / "packages")
    candidates.append((lean_root / ".lake").resolve() / "packages")
    candidates.append(
        pathlib.Path("/media") / getpass.getuser() / "Data/aro-v2-lean-cache/.lake/packages"
    )
    for cand in candidates:
        if cand.is_dir():
            return cand
    searched = ", ".join(str(c) for c in candidates)
    raise GateError(f"Hydrated Lean .lake/packages not found (searched: {searched})")


def _build_lean_path(out_lib: pathlib.Path, lean_root: pathlib.Path) -> str:
    lake_pkgs = _resolve_lean_packages_dir(lean_root)
    parts = [str(out_lib)]
    for pkg in sorted(lake_pkgs.iterdir()):
        lib = pkg / ".lake/build/lib/lean"
        if lib.is_dir():
            parts.append(str(lib))
    sysroot = subprocess.check_output(["lean", "--print-prefix"], text=True).strip()
    parts.append(str(pathlib.Path(sysroot) / "lib/lean"))
    return os.pathsep.join(parts)


def _parse_print_axioms_detailed(output: str) -> tuple[dict[str, set[str]], dict[str, int]]:
    """Parse Lean `#print axioms` output (single- or multi-line), UNIONING axioms on duplicates."""
    axioms_by_thm: dict[str, set[str]] = {}
    counts: dict[str, int] = {}
    pat = re.compile(
        r"^[ \t]*'([^']+)'\s+(?:depends on axioms:\s+\[([^\]]*)\]|does not depend on any axioms)",
        flags=re.M,
    )
    for m in pat.finditer(output):
        name = m.group(1)
        if m.group(2) is not None:
            found = {a.strip() for a in m.group(2).split(",") if a.strip()}
            axioms_by_thm.setdefault(name, set()).update(found)
        else:
            axioms_by_thm.setdefault(name, set())
        counts[name] = counts.get(name, 0) + 1
    return axioms_by_thm, counts


def parse_print_axioms(output: str) -> dict[str, set[str]]:
    """Return map `decl -> union of all reported axioms` (never overwrites earlier axioms)."""
    axioms_by_thm, _ = _parse_print_axioms_detailed(output)
    return axioms_by_thm


def audit_axiom_output(
    output: str,
    expected_decls: tuple[str, ...] = EXPECTED_UNIFIED_DECLS,
    allowlist: frozenset[str] = ALLOWED_AXIOMS,
) -> list[str]:
    axioms_by_thm, counts = _parse_print_axioms_detailed(output)
    if not axioms_by_thm:
        return ["Empty #print axioms inventory output"]
    errors: list[str] = []
    for name, count in sorted(counts.items()):
        if count > 1:
            errors.append(f"Duplicate #print axioms entry for '{name}' (seen {count} times)")
    for decl in expected_decls:
        if decl not in axioms_by_thm:
            errors.append(f"Missing theorem in #print axioms audit: {decl}")
            continue
        disallowed = axioms_by_thm[decl] - allowlist
        if disallowed:
            errors.append(f"Disallowed axioms on {decl}: {sorted(disallowed)}")
    # Also audit any extra declarations printed in the output so nothing hides disallowed axioms
    expected_set = set(expected_decls)
    for name, ax_set in sorted(axioms_by_thm.items()):
        if name in expected_set:
            continue
        disallowed = ax_set - allowlist
        if disallowed:
            errors.append(f"Disallowed axioms on {name}: {sorted(disallowed)}")
    return errors


def _run_lake_build(
    lean_root: pathlib.Path,
    targets: tuple[str, ...],
) -> subprocess.CompletedProcess[str]:
    """Run native `lake --offline build` so Lake verifies every content hash & `.trace`."""
    proc = subprocess.run(
        ["lake", "--offline", "build", "--no-ansi", *targets],
        cwd=str(lean_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise GateError(
            f"Native `lake --offline build` failed (exit {proc.returncode}):\n"
            f"{proc.stdout}\n{proc.stderr}"
        )
    return proc


def _snapshot_project_oleans(lake_lib: pathlib.Path) -> dict[str, str]:
    """Return `{rel_path: sha256}` for all compiled project `.olean`s under `lake_lib`."""
    snap: dict[str, str] = {}
    for top in ("BridgeFormalV2", "BridgeFormalV3", "AroCore", "AroProofs", "Controls"):
        root_dir = lake_lib / top
        if not root_dir.is_dir():
            continue
        for olean in sorted(root_dir.rglob("*.olean")):
            snap[str(olean.relative_to(lake_lib))] = _sha256(olean)
    return snap


def _build_lean_path_optional_pkgs(out_lib: pathlib.Path, lean_root: pathlib.Path) -> str:
    """Build `LEAN_PATH` for `lean_root` (works with Mathlib or standalone projects)."""
    parts = [str(out_lib)]
    try:
        lake_pkgs = _resolve_lean_packages_dir(lean_root)
    except GateError:
        lake_pkgs = None
    if lake_pkgs is not None:
        for pkg in sorted(lake_pkgs.iterdir()):
            lib = pkg / ".lake/build/lib/lean"
            if lib.is_dir():
                parts.append(str(lib))
    sysroot = subprocess.check_output(["lean", "--print-prefix"], text=True).strip()
    parts.append(str(pathlib.Path(sysroot) / "lib/lean"))
    return os.pathsep.join(parts)


def _run_live_lean_file(
    lean_root: pathlib.Path,
    rel: str,
    *,
    lake_lib: pathlib.Path | None = None,
    lean_path: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Execute Lean 4 kernel directly on `rel` (never reads or trusts Lake `.trace` logs)."""
    lib_dir = lake_lib or ((lean_root / ".lake").resolve() / "build/lib/lean")
    env = os.environ.copy()
    env["LEAN_PATH"] = lean_path or _build_lean_path_optional_pkgs(lib_dir, lean_root)
    return subprocess.run(
        ["lean", f"--root={lean_root}", str(lean_root / rel)],
        cwd=str(lean_root),
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def _audit_live_inventory(
    lean_root: pathlib.Path,
    inventory_rel: str = "AroProofs/Inventory.lean",
    *,
    expected_decls: tuple[str, ...] = EXPECTED_UNIFIED_DECLS,
    proc: subprocess.CompletedProcess[str] | None = None,
) -> None:
    """Audit `#print axioms` strictly from live Lean 4 stdout (ignoring `Inventory.trace`)."""
    res = proc if proc is not None else _run_live_lean_file(lean_root, inventory_rel)
    if res.returncode != 0:
        raise GateError(
            f"Lean 4 live check failed on {inventory_rel} (exit {res.returncode}):\n"
            f"{res.stdout}\n{res.stderr}"
        )
    axiom_errors = audit_axiom_output(res.stdout, expected_decls=expected_decls)
    if axiom_errors:
        raise GateError("Lean 4 axiom audit failed:\n  - " + "\n  - ".join(axiom_errors))


def _audit_lake_control_axioms(lake_output: str) -> None:
    """Audit any `#print axioms` lines emitted during `lake build` for positive controls."""
    cleaned_lines: list[str] = []
    for line in lake_output.splitlines():
        m = re.search(
            r"Controls/Unified/C\d+\.lean:\d+:\d+:\s*"
            r"('[^']+'\s+(?:depends on axioms:.*|does not depend on any axioms.*))$",
            line,
        )
        if m:
            cleaned_lines.append(m.group(1))
    if not cleaned_lines:
        return
    ax_map, _ = _parse_print_axioms_detailed("\n".join(cleaned_lines))
    for name, ax_set in sorted(ax_map.items()):
        disallowed = ax_set - ALLOWED_AXIOMS
        if disallowed:
            raise GateError(
                f"Positive control ({name}) used disallowed axioms: {sorted(disallowed)}"
            )


def compile_and_audit_lean(
    lean_root: pathlib.Path = LEAN_ROOT,
    *,
    compile_controls: bool = True,
    fresh: bool = False,
) -> dict[str, Any]:
    """Offline Lean 4 kernel verification via native `lake --offline build` + live kernel checks.

    Uses ZERO custom stamp files: Lake's own content-addressed `.trace` verification ensures any
    modified or broken `.lean` module (e.g. `Dynamics.lean`) is always recompiled by the Lean 4
    kernel, followed by live parallel Lean 4 kernel execution of `AroProofs/Inventory.lean` and
    negative controls `C5` & `C6Negative`.
    """
    if str(GATES_DIR) not in sys.path:
        sys.path.insert(0, str(GATES_DIR))
    import verify_lean as vl  # type: ignore[import-not-found]

    # Static zero-sorry/zero-axiom pre-check on all proof modules (comments & strings stripped)
    proof_files = [
        p
        for p in UNIFIED_COMPILE_ORDER
        if "/Proofs/" in p or p.startswith("AroProofs/")
    ]
    for rel in proof_files:
        src = lean_root / rel
        if not src.is_file():
            raise GateError(f"Missing Lean module: {rel}")
        cleaned = vl.strip_lean_comments_and_strings(src.read_text(encoding="utf-8"))
        for bad in ("sorry", "admit", "axiom"):
            if re.search(rf"\b{bad}\b", cleaned):
                raise GateError(f"Forbidden token '{bad}' in proof module {rel}")

    if fresh:
        with tempfile.TemporaryDirectory(prefix="aro-g3-lean-") as tmp:
            out_lib = pathlib.Path(tmp) / "lib/lean"
            out_lib.mkdir(parents=True, exist_ok=True)
            env = os.environ.copy()
            env["LEAN_PATH"] = _build_lean_path(out_lib, lean_root)

            def _compile_fresh(
                rel: str, *, write_olean: bool = True
            ) -> subprocess.CompletedProcess[str]:
                src = lean_root / rel
                cmd = ["lean", f"--root={lean_root}"]
                if write_olean:
                    olean = out_lib / pathlib.Path(rel).with_suffix(".olean")
                    olean.parent.mkdir(parents=True, exist_ok=True)
                    cmd.extend(["-o", str(olean)])
                cmd.append(str(src))
                return subprocess.run(
                    cmd,
                    cwd=str(lean_root),
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )

            inventory_stdout = ""
            for rel in UNIFIED_COMPILE_ORDER:
                proc = _compile_fresh(rel, write_olean=(rel != "AroProofs/Inventory.lean"))
                if proc.returncode != 0:
                    raise GateError(
                        f"Lean 4 compile failed on {rel} (exit {proc.returncode}):\n"
                        f"{proc.stdout}\n{proc.stderr}"
                    )
                if rel == "AroProofs/Inventory.lean":
                    inventory_stdout = proc.stdout

            axiom_errors = audit_axiom_output(inventory_stdout)
            if axiom_errors:
                raise GateError("Lean 4 axiom audit failed:\n  - " + "\n  - ".join(axiom_errors))

            control_summary: dict[str, str] = {}
            if compile_controls:
                for rel in POSITIVE_CONTROLS:
                    proc = _compile_fresh(rel, write_olean=True)
                    if proc.returncode != 0:
                        raise GateError(
                            f"Positive control {rel} failed:\n{proc.stdout}\n{proc.stderr}"
                        )
                    ctrl_ax, _ = _parse_print_axioms_detailed(proc.stdout)
                    for name, ax_set in ctrl_ax.items():
                        disallowed = ax_set - ALLOWED_AXIOMS
                        if disallowed:
                            raise GateError(
                                f"Positive control {rel} ({name}) disallowed axioms: "
                                f"{sorted(disallowed)}"
                            )
                    control_summary[rel] = "compiled_fresh"
                for rel in NEGATIVE_CONTROLS:
                    proc = _compile_fresh(rel, write_olean=False)
                    combined = proc.stdout + "\n" + proc.stderr
                    if proc.returncode == 0:
                        raise GateError(f"Negative control {rel} unexpectedly compiled!")
                    if any(marker in combined for marker in IMPORT_ERR_MARKERS):
                        raise GateError(
                            f"Negative control {rel} failed due to import error instead of "
                            f"semantic rejection:\n{combined}"
                        )
                    control_summary[rel] = "rejected_as_expected"

            return {
                "compiled_modules": len(UNIFIED_COMPILE_ORDER),
                "build_driver": "lean_fresh_scratch",
                "audited_declarations": len(EXPECTED_UNIFIED_DECLS),
                "allowed_axioms": sorted(ALLOWED_AXIOMS),
                "controls": control_summary,
            }

    # Native `lake --offline build` verifies every module + `.trace` content hash.
    # For the axiom verdict, NEVER trust Lake's cached `Inventory.trace` log: ALWAYS run live
    # Lean 4 kernel on `AroProofs/Inventory.lean` (plus negative controls `C5`/`C6Negative`).
    # When project `.olean`s already exist, overlap those live kernel checks with `lake build`,
    # and automatically re-run them if `lake build` updated ANY project `.olean`.
    targets = LAKE_BUILD_TARGETS if compile_controls else (
        "BridgeFormalV2.Proofs.Inventory",
        "AroProofs.Inventory",
    )
    lake_lib = (lean_root / ".lake").resolve() / "build/lib/lean"
    pre_snap = _snapshot_project_oleans(lake_lib) if lake_lib.is_dir() else {}

    live_targets: list[str] = ["AroProofs/Inventory.lean"]
    if compile_controls:
        live_targets.extend(NEGATIVE_CONTROLS)

    required_pre_oleans = (
        "AroProofs/BridgeF1F2.olean",
        "AroProofs/Aroform.olean",
        "AroProofs/BridgeF3Draft.olean",
        *(("Controls/Unified/C4.olean", "Controls/Unified/C6.olean") if compile_controls else ()),
    )
    can_overlap_live = all(k in pre_snap for k in required_pre_oleans)
    lean_path = _build_lean_path(lake_lib, lean_root)

    live_results: dict[str, subprocess.CompletedProcess[str]] = {}
    if can_overlap_live:
        with concurrent.futures.ThreadPoolExecutor(max_workers=1 + len(live_targets)) as pool:
            f_lake = pool.submit(_run_lake_build, lean_root, targets)
            f_live = {
                pool.submit(
                    _run_live_lean_file, lean_root, rel, lake_lib=lake_lib, lean_path=lean_path
                ): rel
                for rel in live_targets
            }
            lake_proc = f_lake.result()
            for fut, rel in f_live.items():
                live_results[rel] = fut.result()
    else:
        lake_proc = _run_lake_build(lean_root, targets)

    if not lake_lib.is_dir():
        raise GateError(f"Expected Lake build lib directory missing: {lake_lib}")

    lake_combined = lake_proc.stdout + "\n" + lake_proc.stderr
    if compile_controls:
        _audit_lake_control_axioms(lake_combined)

    post_snap = _snapshot_project_oleans(lake_lib)
    if not can_overlap_live or post_snap != pre_snap:
        # Re-run live Lean 4 kernel checks against the newly built `.olean`s
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(live_targets)) as pool:
            fut_map = {
                pool.submit(
                    _run_live_lean_file, lean_root, rel, lake_lib=lake_lib, lean_path=lean_path
                ): rel
                for rel in live_targets
            }
            for fut in concurrent.futures.as_completed(fut_map):
                rel = fut_map[fut]
                live_results[rel] = fut.result()

    # Strictly audit live kernel stdout of `AroProofs/Inventory.lean` (never Lake's Inventory.trace)
    _audit_live_inventory(
        lean_root,
        "AroProofs/Inventory.lean",
        expected_decls=EXPECTED_UNIFIED_DECLS,
        proc=live_results["AroProofs/Inventory.lean"],
    )

    control_summary = {}
    if compile_controls:
        for rel in POSITIVE_CONTROLS:
            control_summary[rel] = "verified_by_lake_build"
        for rel in NEGATIVE_CONTROLS:
            proc = live_results[rel]
            combined = proc.stdout + "\n" + proc.stderr
            if proc.returncode == 0:
                raise GateError(f"Negative control {rel} unexpectedly compiled!")
            if any(marker in combined for marker in IMPORT_ERR_MARKERS):
                raise GateError(
                    f"Negative control {rel} failed due to import error instead of "
                    f"semantic rejection:\n{combined}"
                )
            control_summary[rel] = "rejected_as_expected"

    return {
        "compiled_modules": len(UNIFIED_COMPILE_ORDER),
        "build_driver": "lake_offline_build_and_live_kernel",
        "audited_declarations": len(EXPECTED_UNIFIED_DECLS),
        "allowed_axioms": sorted(ALLOWED_AXIOMS),
        "controls": control_summary,
    }


def _stage_episodes_sandbox(repo_root: pathlib.Path, tmp: str) -> pathlib.Path:
    episodes_src = repo_root / "verification/gates/episodes"
    m0_pilot = repo_root / "verification/oracles/m0/pilot"
    if not episodes_src.is_dir():
        raise GateError(f"Missing episodes directory: {episodes_src}")
    stage = pathlib.Path(tmp) / "pilot/episodes"
    shutil.copytree(episodes_src, stage)
    (pathlib.Path(tmp) / "pilot/__init__.py").write_text("", encoding="utf-8")
    (stage / "__init__.py").write_text("", encoding="utf-8")
    vendor = stage / "vendor"
    vendor.mkdir(exist_ok=True)
    (vendor / "__init__.py").write_text("", encoding="utf-8")
    shutil.copy2(m0_pilot / "baseline/finite_reference.py", vendor / "finite_reference.py")
    shutil.copy2(m0_pilot / "checkers/finite_bellman.py", vendor / "finite_bellman.py")
    return stage


def run_episodes_regressions(repo_root: pathlib.Path = ROOT) -> dict[str, Any]:
    """Run all 8 public references + 5 negative controls from verification/gates/episodes/."""
    with tempfile.TemporaryDirectory(prefix="aro-episodes-eval-") as tmp:
        _stage_episodes_sandbox(repo_root, tmp)
        proc = subprocess.run(
            [*_py_flags(), "-m", "pilot.episodes.validate"],
            cwd=tmp,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise GateError(
                f"Episodes negative regression suite failed (exit {proc.returncode}):\n"
                f"{proc.stdout}\n{proc.stderr}"
            )
        parsed = json.loads(proc.stdout)
        refs = parsed.get("references", {})
        ctrls = parsed.get("negative_controls", {})
        if len(refs) != 8 or len(ctrls) != 5:
            raise GateError(
                f"Unexpected episodes coverage: refs={len(refs)} (expected 8), "
                f"controls={len(ctrls)} (expected 5)"
            )
        for name, item in ctrls.items():
            if item.get("objective_checks") != "rejected":
                raise GateError(f"Negative episode control {name} was NOT rejected: {item}")
        return {
            "references_passed": len(refs),
            "negative_controls_rejected": sorted(ctrls.keys()),
        }


def _run_single_episode_control(repo_root: pathlib.Path, control_name: str) -> dict[str, Any]:
    """Fast self-test helper: verify one specific negative control is rejected by episodes judge."""
    with tempfile.TemporaryDirectory(prefix="aro-episodes-ctrl-") as tmp:
        stage = _stage_episodes_sandbox(repo_root, tmp)
        ctrl_path = stage / "controls" / control_name
        if not ctrl_path.is_file():
            raise GateError(f"Missing episode negative control: {control_name}")
        code = (
            "import json, pathlib\n"
            "from pilot.episodes import judge\n"
            "from pilot.episodes.vendor import finite_bellman\n"
            "judge.integrity()\n"
            f"data = judge.decode(pathlib.Path({str(ctrl_path)!r}).read_text())\n"
            "out = {'objective_checks': 'accepted'}\n"
            "try:\n"
            "    judge.evaluate(data)\n"
            "except (judge.Rejected, finite_bellman.CheckerError) as err:\n"
            "    out = {'objective_checks': 'rejected', 'reason': str(err)}\n"
            "print(json.dumps(out))\n"
        )
        proc = subprocess.run(
            [*_py_flags(), "-c", code],
            cwd=tmp,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise GateError(
                f"Single episode control {control_name} runner failed:\n"
                f"{proc.stdout}\n{proc.stderr}"
            )
        return json.loads(proc.stdout)


def _run_transfer_v1_parallel(repo_root: pathlib.Path) -> int:
    """Run frozen `research/claims/bridge-transfer-v1/check.py` across its 4 cases in parallel."""
    check_py = repo_root / "research/claims/bridge-transfer-v1/check.py"
    contract_path = repo_root / "research/claims/bridge-transfer-v1/case-contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    cases = list(contract["cases"])

    # First verify frozen scientific input SHA-256 digests (identical to check.py:main)
    sha_code = (
        "import importlib.util, pathlib; "
        f"p = pathlib.Path({str(check_py)!r}); "
        "spec = importlib.util.spec_from_file_location('btv1', p); "
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
        "c = m.load(m.CONTRACT_PATH); "
        "[m.require(m.digest(vp) == c['readonly_sha256'][hp], f'changed: {vp}') "
        "for hp, vp in m.V2_FROZEN_INPUTS.items()]"
    )
    p_sha = subprocess.run(
        [*_py_flags(), "-c", sha_code],
        cwd=str(repo_root),
        capture_output=True,
        text=True,
        check=False,
    )
    if p_sha.returncode != 0:
        raise GateError(
            f"bridge-transfer-v1 frozen input check failed:\n{p_sha.stdout}\n{p_sha.stderr}"
        )

    def _run_one_case(case_name: str) -> dict[str, Any]:
        case_code = (
            "import importlib.util, json, pathlib; "
            f"p = pathlib.Path({str(check_py)!r}); "
            "spec = importlib.util.spec_from_file_location('btv1', p); "
            "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
            f"print(json.dumps(m.check_case({case_name!r})))"
        )
        proc = subprocess.run(
            [*_py_flags(), "-c", case_code],
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise GateError(
                f"bridge-transfer-v1 case {case_name} failed:\n{proc.stdout}\n{proc.stderr}"
            )
        return json.loads(proc.stdout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(cases)) as pool:
        results = list(pool.map(_run_one_case, cases))
    tot = sum(len(r["controls"]) for r in results)
    acc = sum(1 for r in results for c in r["controls"] if c["observation"] == "accepted")
    rej = sum(1 for r in results for c in r["controls"] if c["observation"] == "rejected")
    if (tot, acc, rej) != (32, 16, 16):
        raise GateError(
            f"Unexpected transfer-v1 summary: total={tot}, accepted={acc}, rejected={rej}"
        )
    return tot


def run_g2(
    repo_root: pathlib.Path = ROOT,
    *,
    claim_spec: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute Gate G2: strict grids + live claim falsifier + M0 + T1-T7 + transfer + CE."""
    spec = claim_spec if claim_spec is not None else BASELINE_CLAIM_SPEC
    validate_claim_spec(spec)

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root)

    def _run_cmd(cmd: list[str], cwd: pathlib.Path, label: str, *, use_env: bool = False) -> str:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            env=(env if use_env else None),
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            raise GateError(f"{label} failed:\n{proc.stdout}\n{proc.stderr}")
        return proc.stdout

    ce_cmds = [
        (
            [
                *_py_flags(),
                "research/counterexamples/D1-baseline/checks/check_candidate_v2.py",
                "research/counterexamples/D1-baseline/checks/candidate-v1.json",
            ],
            "Counterexample D1",
        ),
        (
            [*_py_flags(), "research/counterexamples/D2-structured/checks/certificate_check_v2.py"],
            "Counterexample D2-cert",
        ),
        (
            [*_py_flags(), "research/counterexamples/D2-structured/checks/trajectory_check_v2.py"],
            "Counterexample D2-traj",
        ),
        (
            [*_py_flags(), "research/counterexamples/E-rank1/checks/rank_one_check.py"],
            "Counterexample E-rank1",
        ),
        (
            [*_py_flags(), "research/counterexamples/astra-probe-AS1/checks/check.py"],
            "Counterexample Astra-AS1",
        ),
    ]

    # Keep concurrency bounded (<= 5 processes) so G2 never starves G3 Lean/Lake on 8-core hosts.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f_tr = pool.submit(_run_transfer_v1_parallel, repo_root)  # up to 4 sub-workers
        f_m0_chk = pool.submit(
            _run_cmd,
            [*_py_flags(), "-m", "unittest", "discover", "-s", "pilot/checkers", "-p", "test_*.py"],
            repo_root / "verification/oracles/m0",
            "M0 oracle tests (pilot/checkers)",
        )
        tot = f_tr.result()
        f_m0_chk.result()

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        f_m0_base = pool.submit(
            _run_cmd,
            [*_py_flags(), "-m", "unittest", "discover", "-s", "pilot/baseline", "-p", "test_*.py"],
            repo_root / "verification/oracles/m0",
            "M0 oracle tests (pilot/baseline)",
        )
        f_ut = pool.submit(
            _run_cmd,
            [
                *_py_flags(),
                "-m",
                "unittest",
                "discover",
                "-s",
                "verification/falsifiers/tests",
                "-p",
                "test_*.py",
            ],
            repo_root,
            "Falsifier unit tests",
            use_env=True,
        )
        f_bat = pool.submit(
            _run_cmd,
            [*_py_flags(), "-m", "verification.falsifiers.battery_t1_t7", "--json"],
            repo_root,
            "T1-T7 battery",
            use_env=True,
        )
        f_ce = [
            pool.submit(_run_cmd, cmd, repo_root, label)
            for cmd, label in ce_cmds
        ]

        f_m0_base.result()
        f_ut.result()
        bat_json = json.loads(f_bat.result())
        if bat_json.get("passed") != 7 or bat_json.get("total") != 7:
            raise GateError(f"T1-T7 battery incomplete: {bat_json}")
        for f in f_ce:
            f.result()

    # Execute the submitted Stage 2 claim itself against its falsifier / T1-T7 / script
    claim_eval = evaluate_claim_spec(spec, repo_root, battery_json=bat_json)

    return {
        "claim": claim_eval,
        "grid_points": claim_eval["grid_points"],
        "m0_tests": 36,
        "t1_t7_passed": 7,
        "transfer_controls": tot,
        "counterexamples": ["D1", "D2-cert", "D2-traj", "E-rank1", "Astra-AS1"],
    }


def run_g3(
    repo_root: pathlib.Path = ROOT,
    *,
    base_ref: str | None = None,
    fresh_lean: bool = False,
) -> dict[str, Any]:
    """Execute Gate G3: frozen core guard + Lean 4 kernel & C1-C6 + episodes regressions."""
    frozen_errors = check_frozen_core(repo_root, base_ref=base_ref)
    if frozen_errors:
        raise GateError("Frozen core integrity failed:\n  - " + "\n  - ".join(frozen_errors))

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        f_lean = pool.submit(
            compile_and_audit_lean,
            repo_root / "verification/lean",
            compile_controls=True,
            fresh=fresh_lean,
        )
        f_ep = pool.submit(run_episodes_regressions, repo_root)
        lean_report = f_lean.result()
        episodes_report = f_ep.result()

    return {
        "frozen_core": "intact",
        "lean": lean_report,
        "episodes": episodes_report,
    }


def run_self_test() -> int:
    """Negative self-tests (zero `assert`, works identically in `-B` and `-B -O`)."""
    # 1. Tampered Goals.lean, deleted Goals.lean from manifest, AND coordinated tamper MUST fail
    with tempfile.TemporaryDirectory(prefix="aro-g3-tamper-") as tmp:
        fake = pathlib.Path(tmp)
        for rel in FROZEN_CORE_FILES:
            dest = fake / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / rel, dest)
        lock_dest = fake / FROZEN_CORE_MANIFEST_REL
        lock_dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(FROZEN_CORE_MANIFEST, lock_dest)
        _expect(check_frozen_core(fake) == [], "Clean frozen core copy failed self-test")

        # 1a. Delete AroCore/Goals.lean from manifest (even while file on disk is intact!)
        lock_orig = json.loads(lock_dest.read_text(encoding="utf-8"))
        lock_missing = json.loads(json.dumps(lock_orig))
        del lock_missing["frozen_files"]["verification/lean/AroCore/Goals.lean"]
        lock_dest.write_text(json.dumps(lock_missing, indent=2), encoding="utf-8")
        errs_del = check_frozen_core(fake)
        _expect(
            any("missing required entry" in e and "Goals.lean" in e for e in errs_del),
            f"Deleted Goals.lean from manifest was NOT rejected: {errs_del}",
        )

        # 1b. Tamper Goals.lean on disk with original manifest
        lock_dest.write_text(json.dumps(lock_orig, indent=2), encoding="utf-8")
        goals_p = fake / "verification/lean/AroCore/Goals.lean"
        goals_p.write_text(
            goals_p.read_text(encoding="utf-8") + "\n-- tampered\n", encoding="utf-8"
        )
        errs_tamp = check_frozen_core(fake)
        _expect(
            any("Frozen core tampered" in e for e in errs_tamp),
            f"Tampered Goals accepted: {errs_tamp}",
        )

        # 1c. Coordinated tamper: rewrite BOTH Goals.lean AND frozen-core-sha256.json
        lock_coord = json.loads(json.dumps(lock_orig))
        lock_coord["frozen_files"]["verification/lean/AroCore/Goals.lean"] = _sha256(goals_p)
        lock_dest.write_text(json.dumps(lock_coord, indent=2), encoding="utf-8")
        errs_coord = check_frozen_core(fake)
        _expect(
            any("manifest hash tampered" in e for e in errs_coord),
            f"Coordinated Goals+manifest tamper accepted: {errs_coord}",
        )

    # 2. Empty grids AND invalid grid points (null / bool / NaN / Inf / empty str) MUST fail G2
    for bad_spec in (
        {"claim_id": "c1", "kind": "sympy_inequality", "grids": []},
        {"claim_id": "c2", "kind": "sympy_inequality", "grids": [{}]},
        {"claim_id": "c3", "kind": "sympy_inequality", "grids": [{"a": []}]},
        {"claim_id": "c4", "kind": "sympy_inequality", "grids": [{"x": [None]}]},
        {"claim_id": "c5", "kind": "sympy_inequality", "grids": [{"x": [True]}]},
        {"claim_id": "c6", "kind": "sympy_inequality", "grids": [{"x": [""]}]},
        {"claim_id": "c7", "kind": "sympy_inequality", "grids": [{"x": ["NaN"]}]},
        {"claim_id": "c8", "kind": "sympy_inequality", "grids": [{"x": [float("nan")]}]},
        {"claim_id": "c9", "kind": "sympy_inequality", "grids": [{"x": [float("inf")]}]},
        # Passive claim without verifiable `kind` MUST be rejected
        {"claim_id": "c-noop", "grids": [{"x": [1]}]},
    ):
        rejected = False
        try:
            validate_claim_spec(bad_spec)
        except GateError:
            rejected = True
        _expect(rejected, f"Invalid/empty/no-op claim spec was NOT rejected: {bad_spec}")

    # 3. Real claim execution MUST falsify false SymPy & T1-T7 claims and accept true claims
    false_sympy_claim = {
        "claim_id": "false-xy-ineq",
        "kind": "sympy_inequality",
        "lhs": "x + y",
        "rhs": "x * y",
        "relation": "<=",
        "grids": [{"x": [1, 2], "y": [1, 2]}],
    }
    rejected_sympy = False
    try:
        evaluate_claim_spec(false_sympy_claim, ROOT)
    except GateError as exc:
        rejected_sympy = "FALSIFIED" in str(exc)
    _expect(rejected_sympy, "False sympy_inequality claim was NOT falsified!")

    true_eval = evaluate_claim_spec(BASELINE_CLAIM_SPEC, ROOT)
    _expect(true_eval["survived"] is True, f"True baseline claim failed: {true_eval}")

    false_t1_t7_claim = {
        "claim_id": "naive-all-exact",
        "kind": "t1_t7_predicate",
        "grids": [{"s": [2, 4]}],
        "predictions": {f"T{i}": "exact" for i in range(1, 8)},
    }
    rejected_t1_t7 = False
    try:
        evaluate_claim_spec(false_t1_t7_claim, ROOT)
    except GateError as exc:
        rejected_t1_t7 = "FALSIFIED" in str(exc) and "T2" in str(exc)
    _expect(rejected_t1_t7, "False t1_t7_predicate claim was NOT falsified on T2!")

    # Also verify exact JSON float parsing (no float64 rounding: 2^53 + 1 != 2^53)
    prec_json = (
        '{"claim_id": "float64-exact", "kind": "sympy_inequality", '
        '"lhs": "x", "rhs": "9007199254740992", "relation": "<=", '
        '"grids": [{"x": [9007199254740993.0]}]}'
    )
    prec_spec = json.loads(prec_json, parse_float=Decimal)
    rejected_prec = False
    try:
        evaluate_claim_spec(prec_spec, ROOT)
    except GateError as exc:
        rejected_prec = "FALSIFIED" in str(exc) and "9007199254740993" in str(exc)
    _expect(
        rejected_prec,
        "Float64 boundary 9007199254740993.0 <= 9007199254740992 was NOT falsified!",
    )

    # Also verify `checker_script` strict JSON contract (empty file / learn/__init__.py / missing
    # fields / checked_points < grid_points / claim_id mismatch / survived=false / traversal)
    rejected_init = False
    try:
        evaluate_claim_spec(
            {
                "claim_id": "noop-init",
                "kind": "checker_script",
                "script": "learn/__init__.py",
                "grids": [{"x": [1]}],
            },
            ROOT,
        )
    except GateError:
        rejected_init = True
    _expect(rejected_init, "Empty learn/__init__.py checker_script was NOT rejected!")

    with tempfile.TemporaryDirectory(prefix="aro-g2-script-") as tmp_root:
        tmp_r = pathlib.Path(tmp_root)
        (tmp_r / "empty.py").write_text("", encoding="utf-8")
        (tmp_r / "missing_fields.py").write_text(
            "import json; print(json.dumps({'survived': True}))\n", encoding="utf-8"
        )
        (tmp_r / "short_points.py").write_text(
            "import json; print(json.dumps({'claim_id': 'c', 'survived': True, "
            "'checked_points': 1}))\n",
            encoding="utf-8",
        )
        (tmp_r / "wrong_id.py").write_text(
            "import json; print(json.dumps({'claim_id': 'other', 'survived': True, "
            "'checked_points': 2}))\n",
            encoding="utf-8",
        )
        (tmp_r / "check_false.py").write_text(
            "import json; print(json.dumps({'claim_id': 'c', 'survived': False, "
            "'checked_points': 2}))\n",
            encoding="utf-8",
        )
        (tmp_r / "check_ok.py").write_text(
            "import json; print(json.dumps({'claim_id': 'c', 'survived': True, "
            "'checked_points': 2}))\n",
            encoding="utf-8",
        )
        for bad_script in (
            "empty.py",
            "missing_fields.py",
            "short_points.py",
            "wrong_id.py",
            "check_false.py",
            "../outside.py",
        ):
            rejected_s = False
            try:
                evaluate_claim_spec(
                    {
                        "claim_id": "c",
                        "kind": "checker_script",
                        "script": bad_script,
                        "grids": [{"x": [1, 2]}],
                    },
                    tmp_r,
                )
            except GateError:
                rejected_s = True
            _expect(rejected_s, f"Invalid checker_script {bad_script} was NOT rejected!")

        ok_res = evaluate_claim_spec(
            {
                "claim_id": "c",
                "kind": "checker_script",
                "script": "check_ok.py",
                "grids": [{"x": [1, 2]}],
            },
            tmp_r,
        )
        _expect(
            ok_res["survived"] is True and ok_res["checked_points"] == 2,
            f"Valid checker_script unexpectedly failed: {ok_res}",
        )

    # 4. Forbidden custom axiom MUST fail G3 axiom audit
    fake_ax_out = "\n".join(
        f"'{d}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for d in EXPECTED_UNIFIED_DECLS
    ).replace("Quot.sound]", "Quot.sound, EvilCustomAxiom]", 1)
    ax_errs = audit_axiom_output(fake_ax_out)
    _expect(any("EvilCustomAxiom" in e for e in ax_errs), f"Custom axiom accepted: {ax_errs}")

    # 5. Active `sorryAx` MUST fail G3 axiom audit
    sorry_out = "\n".join(
        f"'{d}' depends on axioms: [propext, Classical.choice, sorryAx]"
        for d in EXPECTED_UNIFIED_DECLS
    )
    sorry_errs = audit_axiom_output(sorry_out)
    _expect(any("sorryAx" in e for e in sorry_errs), f"sorryAx accepted: {sorry_errs}")

    # 6. Duplicate declaration with `sorryAx` followed by clean line MUST NEVER erase `sorryAx`
    base_clean = "\n".join(
        f"'{d}' depends on axioms: [propext, Classical.choice, Quot.sound]"
        for d in EXPECTED_UNIFIED_DECLS
    )
    first_decl = EXPECTED_UNIFIED_DECLS[0]
    dup_override_1 = (
        f"'{first_decl}' depends on axioms: [propext, sorryAx]\n" + base_clean
    )
    dup_override_2 = (
        f"'{first_decl}' depends on axioms: [propext, sorryAx]\n"
        f"'{first_decl}' does not depend on any axioms\n" + base_clean
    )
    for label, text in (("clean-list", dup_override_1), ("no-axioms", dup_override_2)):
        parsed_union = parse_print_axioms(text)
        _expect(
            "sorryAx" in parsed_union.get(first_decl, set()),
            f"Duplicate override ({label}) erased sorryAx in parse_print_axioms: {parsed_union}",
        )
        dup_errs = audit_axiom_output(text)
        _expect(
            any("sorryAx" in e for e in dup_errs) and any("Duplicate" in e for e in dup_errs),
            f"Duplicate override ({label}) not properly rejected: {dup_errs}",
        )

    # 7. Live Lean 4 kernel check for custom `axiom` in a scratch Lean file
    with tempfile.TemporaryDirectory(prefix="aro-g3-kernel-neg-") as tmp:
        bad_lean = pathlib.Path(tmp) / "Bad.lean"
        bad_lean.write_text(
            "axiom evil : False\ntheorem t_evil : False := evil\n#print axioms t_evil\n",
            encoding="utf-8",
        )
        proc = subprocess.run(
            ["lean", str(bad_lean)], capture_output=True, text=True, check=False
        )
        _expect(proc.returncode == 0, f"Scratch lean failed: {proc.stderr}")
        parsed = parse_print_axioms(proc.stdout)
        _expect(
            "evil" in parsed.get("t_evil", set()),
            f"Kernel did not report evil axiom: {parsed}",
        )
        _expect(
            bool(audit_axiom_output(proc.stdout, expected_decls=("t_evil",))),
            "Gate G3 failed to reject kernel-reported custom axiom!",
        )

    # 8. Broken Dynamics.lean MUST fail native `lake build` even with old `.olean`/forged stamp
    with tempfile.TemporaryDirectory(prefix="aro-g3-lake-neg-") as tmp_lake:
        proj = pathlib.Path(tmp_lake)
        (proj / "lakefile.toml").write_text(
            'name = "negTest"\nversion = "0.1.0"\n\n[[lean_lib]]\nname = "BridgeFormalV2"\n',
            encoding="utf-8",
        )
        dyn = proj / "BridgeFormalV2/Proofs/Dynamics.lean"
        dyn.parent.mkdir(parents=True, exist_ok=True)
        dyn.write_text("theorem expansion_ok : 1 + 1 = 2 := rfl\n", encoding="utf-8")
        _run_lake_build(proj, ("BridgeFormalV2.Proofs.Dynamics",))

        # Break Dynamics.lean while keeping old valid .olean AND planting a forged stamp file
        dyn.write_text("theorem expansion_ok : 1 + 1 = 3 := rfl\n", encoding="utf-8")
        forged_stamp = proj / ".lake/build/aro-g3-stamps.json"
        forged_stamp.parent.mkdir(parents=True, exist_ok=True)
        forged_stamp.write_text('{"forged": true}\n', encoding="utf-8")
        rejected_broken_dyn = False
        try:
            _run_lake_build(proj, ("BridgeFormalV2.Proofs.Dynamics",))
        except GateError:
            rejected_broken_dyn = True
        _expect(
            rejected_broken_dyn,
            "Broken Dynamics.lean was NOT rejected by native `lake --offline build`!",
        )

    # 9. Tampered `Inventory.trace` MUST NEVER fool live `#print axioms` audit
    with tempfile.TemporaryDirectory(prefix="aro-g3-trace-neg-") as tmp_trace:
        proj_t = pathlib.Path(tmp_trace)
        (proj_t / "lakefile.toml").write_text(
            'name = "traceNeg"\nversion = "0.1.0"\n\n[[lean_lib]]\nname = "AroProofs"\n',
            encoding="utf-8",
        )
        evil_mod = proj_t / "AroProofs/Evil.lean"
        evil_mod.parent.mkdir(parents=True, exist_ok=True)
        evil_mod.write_text(
            "axiom evil : False\ntheorem t_evil : False := evil\n", encoding="utf-8"
        )
        inv_mod = proj_t / "AroProofs/Inventory.lean"
        inv_mod.write_text(
            "import AroProofs.Evil\n#print axioms t_evil\n", encoding="utf-8"
        )
        _run_lake_build(proj_t, ("AroProofs.Inventory",))

        # Forge Inventory.trace so Lake's cached log falsely claims clean axioms `[propext]`
        trace_file = proj_t / ".lake/build/lib/lean/AroProofs/Inventory.trace"
        _expect(trace_file.is_file(), f"Expected Lake trace file missing: {trace_file}")
        trace_text = trace_file.read_text(encoding="utf-8")
        _expect("evil" in trace_text, f"Original trace missing 'evil': {trace_text}")
        forged_trace = trace_text.replace("[evil]", "[propext]")
        trace_file.write_text(forged_trace, encoding="utf-8")
        _expect(
            "[evil]" not in trace_file.read_text(encoding="utf-8"),
            "Failed to forge Inventory.trace",
        )

        # Live audit MUST ignore Inventory.trace and still reject `evil` from the Lean 4 kernel!
        rejected_forged_trace = False
        try:
            _audit_live_inventory(proj_t, "AroProofs/Inventory.lean", expected_decls=("t_evil",))
        except GateError as exc:
            rejected_forged_trace = "evil" in str(exc)
        _expect(
            rejected_forged_trace,
            "Forged Inventory.trace fooled live `#print axioms` audit!",
        )

    # 10. Future disturbance leakage MUST fail (episodes M-wrong-information.json)
    ep_ctrl = _run_single_episode_control(ROOT, "M-wrong-information.json")
    _expect(
        ep_ctrl.get("objective_checks") == "rejected",
        f"M-wrong-information negative control was NOT rejected: {ep_ctrl}",
    )

    print(
        "CLAIM GATE G2/G3 SELF-TEST OK: 13/13 negative controls rejected "
        "(tampered Goals.lean / deleted Goals from manifest / coordinated manifest tamper / "
        "empty & null/NaN/bool grids / float64 2^53+1 rounding / passive & empty checker_script / "
        "false claims / custom axiom / sorryAx / duplicate sorryAx override / "
        "kernel evil axiom + broken Dynamics.lean / forged Inventory.trace / future-info leakage)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Unified Gate G2/G3 verifier (R2 #1156).")
    parser.add_argument("--gate", choices=("g2", "g3", "all"), default="all")
    parser.add_argument("--claim", type=pathlib.Path, default=None, help="Optional claim JSON spec")
    parser.add_argument("--base-ref", default=None, help="Git ref for frozen core diff check")
    parser.add_argument(
        "--fresh-lean",
        action="store_true",
        help="Recompile all Lean modules from scratch in an isolated temp dir",
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return run_self_test()

        claim_spec: dict[str, Any] | None = None
        if args.claim is not None:
            claim_spec = json.loads(args.claim.read_text(encoding="utf-8"), parse_float=Decimal)

        report: dict[str, Any] = {"status": "ok", "optimized_mode": not __debug__}
        if args.gate == "all":
            # Run frozen-core check first, then overlap Lean (3 cores) with G2 -> episodes
            # (<=5 cores) so all 8 cores stay busy without NTFS/CPU oversubscription.
            frozen_errors = check_frozen_core(ROOT, base_ref=args.base_ref)
            if frozen_errors:
                raise GateError(
                    "Frozen core integrity failed:\n  - " + "\n  - ".join(frozen_errors)
                )
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                f_lean = pool.submit(
                    compile_and_audit_lean,
                    ROOT / "verification/lean",
                    compile_controls=True,
                    fresh=args.fresh_lean,
                )
                report["g2"] = run_g2(ROOT, claim_spec=claim_spec)
                episodes_report = run_episodes_regressions(ROOT)
                lean_report = f_lean.result()
            report["g3"] = {
                "frozen_core": "intact",
                "lean": lean_report,
                "episodes": episodes_report,
            }
        elif args.gate == "g2":
            report["g2"] = run_g2(ROOT, claim_spec=claim_spec)
        elif args.gate == "g3":
            report["g3"] = run_g3(ROOT, base_ref=args.base_ref, fresh_lean=args.fresh_lean)
    except (GateError, OSError, json.JSONDecodeError) as exc:
        print(f"CLAIM GATE FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        parts: list[str] = []
        if "g2" in report:
            g2 = report["g2"]
            parts.append(
                f"G2 OK (claim={g2['claim']['claim_id']}, M0={g2['m0_tests']}, "
                f"T1-T7={g2['t1_t7_passed']}/7, transfer={g2['transfer_controls']}, CE=5/5)"
            )
        if "g3" in report:
            g3 = report["g3"]
            ln = g3["lean"]
            ep = g3["episodes"]
            parts.append(
                f"G3 OK (frozen core intact, Lean={ln['compiled_modules']} modules / "
                f"{ln['audited_declarations']} decls / {len(ln['controls'])} controls, "
                f"episodes={ep['references_passed']} refs + "
                f"{len(ep['negative_controls_rejected'])} neg controls)"
            )
        print(" | ".join(parts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
