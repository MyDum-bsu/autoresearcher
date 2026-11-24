#!/usr/bin/env python3
"""Stage 2 (FALSIFY_FIRST) exact rational verification for G1 (gen-multistage-k-closures, k >= 2).

Checks:
  1. Causal state-history <-> exogenous-deviation recovery on 4 exact trajectories of a 2D k=2
     (3-stage, len=[2,1,2]) coupled linear system with non-identity A and piecewise policy.
  2. Exact k=2 correlated separation witness (`A=0, B=1, E=2, U=[-1,1], rho=1, H=1, [0,10], c=1`,
     correlated path set `w_0 = w_2 in {-1/2, +1/2}, w_1 in [-1, 1]`):
       - History policy achieves `x_3 = 0` on 10 tested paths;
       - On a 5x5 grid of 25 Markov signaling pairs `(a_+, a_-) in [-1, 1]^2`, the collision
         `w_1^+ = (a_- - a_+)/4, w_1^- = (a_+ - a_-)/4` stays in `[-1, 1]`, gives
         `x_2(omega^+) == x_2(omega^-)`, and yields exact LP lower bound `2`.
  3. Atlas-linked repo oracles for G1: runs M0 finite-Bellman unittest suite plus D1 and D2
     counterexample checkers (`check_candidate_v2.py`, `certificate_check_v2.py`,
     `trajectory_check_v2.py`) in the current interpreter mode (`-B` / `-B -O`).
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from fractions import Fraction
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from verification.oracles.exact_lp import solve_exact_lp


def check_k2_causal_history_bijection() -> dict[str, Any]:
    """Verify exact state-history <-> exogenous-deviation bijection on 2D k=2 (len=[2,1,2])."""
    A = [[Fraction(1), Fraction(1, 2)], [Fraction(0), Fraction(1)]]
    B = [[Fraction(1)], [Fraction(1, 2)]]
    E = [[Fraction(1)], [Fraction(-1)]]
    x0 = [Fraction(1), Fraction(-1)]

    def step(x: list[Fraction], u: Fraction, w: Fraction) -> list[Fraction]:
        return [
            A[0][0] * x[0] + A[0][1] * x[1] + B[0][0] * u + E[0][0] * w,
            A[1][0] * x[0] + A[1][1] * x[1] + B[1][0] * u + E[1][0] * w,
        ]

    def run_stage(x_init: list[Fraction], us: list[Fraction], ws: list[Fraction]) -> list[Fraction]:
        x = list(x_init)
        for u, w in zip(us, ws, strict=True):
            x = step(x, u, w)
        return x

    # Nonlinear history-state policy pi:
    u0 = [Fraction(1, 2), Fraction(-1, 4)]

    def pi1(x1: list[Fraction]) -> list[Fraction]:
        return [Fraction(1, 2) if x1[0] >= 0 else Fraction(-1, 2)]

    def pi2(x1: list[Fraction], x2: list[Fraction]) -> list[Fraction]:
        val = Fraction(1, 3) if (x1[0] + x2[1]) >= 0 else Fraction(-1, 3)
        return [val, -val]

    # Test across 4 exact rational noise trajectories (w0 len 2, w1 len 1, w2 len 2)
    trajs = [
        ([Fraction(1), Fraction(-1)], [Fraction(1, 2)], [Fraction(-1, 2), Fraction(1)]),
        ([Fraction(-1, 2), Fraction(1, 2)], [Fraction(-1)], [Fraction(1), Fraction(0)]),
        ([Fraction(0), Fraction(0)], [Fraction(0)], [Fraction(0), Fraction(0)]),
        ([Fraction(1, 3), Fraction(-2, 3)], [Fraction(3, 4)], [Fraction(-1, 4), Fraction(1, 2)]),
    ]
    for w0, w1, w2 in trajs:
        # Exogenous stage deviations (zero init, zero control)
        xi0 = run_stage([Fraction(0), Fraction(0)], [Fraction(0), Fraction(0)], w0)
        xi1 = run_stage([Fraction(0), Fraction(0)], [Fraction(0)], w1)

        # Forward history-state rollout
        x1 = run_stage(x0, u0, w0)
        u1 = pi1(x1)
        x2 = run_stage(x1, u1, w1)
        u2 = pi2(x1, x2)
        x3_hist = run_stage(x2, u2, w2)

        # Causal recovery of (xi0, xi1) strictly from (x1, x2) & policy pi
        nom1 = run_stage(x0, u0, [Fraction(0), Fraction(0)])
        rec_xi0 = [x1[i] - nom1[i] for i in range(2)]
        nom2 = run_stage(x1, pi1(x1), [Fraction(0)])
        rec_xi1 = [x2[i] - nom2[i] for i in range(2)]
        if rec_xi0 != xi0 or rec_xi1 != xi1:
            return {"ok": False, "reason": "Causal deviation recovery failed"}

        # Reverse multistage ARO rollout strictly from (xi0, xi1)
        x1_aro = [nom1[i] + xi0[i] for i in range(2)]
        u1_aro = pi1(x1_aro)
        nom2_aro = run_stage(x1_aro, u1_aro, [Fraction(0)])
        x2_aro = [nom2_aro[i] + xi1[i] for i in range(2)]
        u2_aro = pi2(x1_aro, x2_aro)
        x3_aro = run_stage(x2_aro, u2_aro, w2)
        if x1_aro != x1 or x2_aro != x2 or u1_aro != u1 or u2_aro != u2 or x3_aro != x3_hist:
            return {"ok": False, "reason": "Forward/reverse multistage trajectory mismatch"}

    return {"ok": True, "checked_trajectories": len(trajs)}


def check_k2_markov_vs_history_separation() -> dict[str, Any]:
    """Verify exact k=2 separation witness (A=0, B=1, E=2, U=[-1,1], rho=1, [0,10], c=1)."""
    # 1. History policy achieves x_3 = 0 on all tested paths in Omega
    checked_history_paths = 0
    for w1 in (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)):
        for sgn in (Fraction(1, 2), Fraction(-1, 2)):
            x1 = Fraction(0) + 2 * sgn
            u2 = Fraction(-1) if x1 >= 0 else Fraction(1)
            x3 = u2 + 2 * sgn
            if x3 != Fraction(0):
                return {"ok": False, "reason": f"History policy failed at ({sgn}, {w1})"}
            checked_history_paths += 1

    # 2. For every signaling pair (a_+, a_-) on a 5x5 grid in [-1, 1]^2, check collision & exact LP
    grid = [Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)]
    checked_pairs = 0
    for ap in grid:
        for am in grid:
            w1_p = (am - ap) / 4
            w1_m = (ap - am) / 4
            if not (-1 <= w1_p <= 1 and -1 <= w1_m <= 1):
                return {"ok": False, "reason": "Collision noise out of [-1, 1]"}
            x2_p = ap + 2 * w1_p
            x2_m = am + 2 * w1_m
            if x2_p != x2_m:
                return {"ok": False, "reason": "Collision mismatch"}
            # Exact LP for shared b = g_2(x_2^*) in [-1, 1] and eta:
            #   b - 1 >= 0  (-b <= -1), b + 1 <= 10, b + 1 <= eta (b - eta <= -1)
            lp = solve_exact_lp(
                c=[0, 1],
                A_ub=[[1, 0], [-1, 0], [-1, 0], [1, 0], [1, -1]],
                b_ub=[1, 1, -1, 9, -1],
                free_vars=(0, 1),
            )
            if lp.status != "optimal" or lp.objective != Fraction(2):
                return {"ok": False, "reason": f"Unexpected Markov LP bound: {lp.objective}"}
            checked_pairs += 1

    return {
        "ok": True,
        "history_value": "0",
        "markov_lower_bound": "2",
        "checked_history_paths": checked_history_paths,
        "checked_signaling_pairs": checked_pairs,
    }


def check_atlas_g1_oracles() -> dict[str, Any]:
    """Run the repo M0 finite-Bellman tests and D1/D2 counterexample checkers."""
    py_flags = ["-B", "-O"] if not __debug__ else ["-B"]
    checks = [
        (
            "m0_checkers_bellman",
            [sys.executable, *py_flags, "-m", "unittest", "discover", "-s", "pilot/checkers", "-p", "test_*.py"],
            REPO_ROOT / "verification/oracles/m0",
        ),
        (
            "d1_prefix_merge",
            [
                sys.executable,
                *py_flags,
                "research/counterexamples/D1-baseline/checks/check_candidate_v2.py",
                "research/counterexamples/D1-baseline/checks/candidate-v1.json",
            ],
            REPO_ROOT,
        ),
        (
            "d2_certificate",
            [sys.executable, *py_flags, "research/counterexamples/D2-structured/checks/certificate_check_v2.py"],
            REPO_ROOT,
        ),
        (
            "d2_trajectory",
            [sys.executable, *py_flags, "research/counterexamples/D2-structured/checks/trajectory_check_v2.py"],
            REPO_ROOT,
        ),
    ]
    results: dict[str, int] = {}
    for name, cmd, cwd in checks:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        results[name] = proc.returncode
    return {"ok": all(rc == 0 for rc in results.values()), "exit_codes": results}


def main() -> None:
    r_bij = check_k2_causal_history_bijection()
    r_sep = check_k2_markov_vs_history_separation()
    r_ora = check_atlas_g1_oracles()
    all_ok = r_bij["ok"] and r_sep["ok"] and r_ora["ok"]
    oracle_checks = sum(1 for rc in r_ora["exit_codes"].values() if rc == 0)
    out = {
        "survived": all_ok,
        "checked_points": (
            r_bij.get("checked_trajectories", 0)
            + r_sep.get("checked_history_paths", 0)
            + r_sep.get("checked_signaling_pairs", 0)
            + oracle_checks
        ),
        "k2_causal_bijection": r_bij,
        "k2_markov_vs_history_separation": r_sep,
        "atlas_g1_oracles": r_ora,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
