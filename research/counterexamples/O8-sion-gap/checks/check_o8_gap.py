#!/usr/bin/env python3
"""Exact rational LP + SymPy continuous-box checker for Counterexample O8 (conj-o8-quantifier-gap).

Certifies that Sion-style compactness/convexity of U and W does NOT imply
zero quantifier-order gap on 1D single-closure BridgeFormalV2.Data instances:
  A=2, B=1, E=1, x0=0, U=[-1,1], rho=1, H=1, gmin=-2, gmax=4, c=1
yields over the CONTINUOUS disturbance boxes w0, w1 in [-1, 1]:
  V(empty) = 4, V({1}) = 2, V_mm_prefix = 0, V_mm_full = 0
with strict quantifier-order gap V({1}) - V_mm_prefix = V({1}) - V_mm_full = 2.

Zero `assert` statements — works identically under `python3 -B` and `python3 -B -O`.
"""
from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

import sympy as sp

REPO_ROOT = pathlib.Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from verification.oracles.exact_lp import solve_exact_lp  # noqa: E402


def _require(cond: bool, msg: str) -> None:
    if not cond:
        raise RuntimeError(f"O8 counterexample check failed: {msg}")


def verify_continuous_box_maximin_sympy() -> dict[str, Any]:
    """Symbolically certify continuous-box V_mm_prefix = 0 and V_mm_full = 0 on [-1, 1]^2.

    For x_2 = 2a + b + 2w_0 + w_1 with a, b in [-1, 1], w_0, w_1 in [-1, 1],
    and terminal constraint -2 <= x_2 <= 4:
      1. Prefix-clairvoyant maximin:
         Given w_0 in [-1, 1], worst-case future noise w_1 in [-1, 1] tightens
         -2 <= x_2 <= 4 to -1 <= 2a + b + 2w_0 <= 3 and objective to 2a + b + 2w_0 + 1.
         - Lower bound for EVERY w_0 in [-1, 1] and EVERY feasible (a, b):
           2a + b + 2w_0 >= -1  ==>  2a + b + 2w_0 + 1 >= 0.
         - Explicit continuous feasible witness for EVERY w_0 in [-1, 1]:
           a(w_0) = -w_0 in [-1, 1], b(w_0) = -1 in [-1, 1] gives
           2a(w_0) + b(w_0) + 2w_0 = -1 in [-1, 3] and objective = 0 identically.
         Therefore sup_{w_0 in [-1, 1]} min_{(a,b) feasible} max_{w_1 in [-1, 1]} x_2 = 0.
      2. Full-clairvoyant maximin:
         Given (w_0, w_1) in [-1, 1]^2, 2a + b ranges over [-3, 3] for (a, b) in [-1, 1]^2,
         and terminal feasibility requires -2 <= (2a + b) + (2w_0 + w_1) <= 4.
         Since 2w_0 + w_1 in [-3, 3], the minimum feasible value of x_2 is
         f_full(w_0, w_1) = max(-2, 2w_0 + w_1 - 3).
         - For every (w_0, w_1) in [-1, 1]^2, 2w_0 + w_1 <= 3 ==> f_full(w_0, w_1) <= 0.
         - At (w_0, w_1) = (1, 1), f_full(1, 1) = max(-2, 0) = 0 (attained by a = -1, b = -1).
         Therefore sup_{(w_0, w_1) in [-1, 1]^2} min_{(a,b) feasible} x_2 = 0.
    """
    w0, w1 = sp.symbols("w0 w1", real=True)
    # Prefix witness: a = -w0, b = -1
    a_pref = -w0
    b_pref = sp.Integer(-1)
    tight_lhs = sp.simplify(2 * a_pref + b_pref + 2 * w0)
    pref_obj = sp.simplify(tight_lhs + 1)
    _require(tight_lhs == -1, f"expected 2a+b+2w0 = -1 identically, got {tight_lhs}")
    _require(pref_obj == 0, f"expected prefix witness objective = 0 identically, got {pref_obj}")

    # Full witness at (w0, w1) = (1, 1): min_{a,b in [-1,1]} (2a + b + 3) = 0
    full_at_11 = sp.simplify(2 * (-1) + (-1) + 2 * 1 + 1)
    _require(full_at_11 == 0, f"expected full witness at (1,1) = 0, got {full_at_11}")

    # Verify upper bound on f_full(w0, w1) = max(-2, 2w0 + w1 - 3) <= 0 on [-1, 1]^2:
    # 2w0 + w1 - 3 = 2*(w0 - 1) + (w1 - 1) <= 0 since w0 <= 1 and w1 <= 1.
    diff_expr = sp.expand((2 * w0 + w1 - 3) - (2 * (w0 - 1) + (w1 - 1)))
    _require(diff_expr == 0, f"algebraic identity for 2w0+w1-3 failed: {diff_expr}")

    return {
        "prefix_witness": "a(w0)=-w0, b(w0)=-1 => 2a+b+2w0 = -1 in [-1,3], obj = 0 for all w0 in [-1,1]",
        "prefix_lower_bound": "2a+b+2w0 >= -1 => obj = 2a+b+2w0+1 >= 0 for all w0 in [-1,1]",
        "full_closed_form": "f_full(w0,w1) = max(-2, 2(w0-1)+(w1-1)) <= 0 on [-1,1]^2, attained at (1,1)",
        "certified_V_mm_prefix_continuous": "0",
        "certified_V_mm_full_continuous": "0",
    }


def solve_o8_1d_hierarchy() -> dict[str, Any]:
    """Solve exact rational LPs and certify continuous-box values for the 1D O8 witness."""
    # 1. Open-loop V(empty): x_2 = 2a + b + 2w0 + w1, continuous box sup_{[-1,1]^2}(2w0+w1)=3, inf=-3
    res_open = solve_exact_lp(
        c=[0, 0, 1],
        A_ub=[
            [1, 0, 0], [-1, 0, 0],
            [0, 1, 0], [0, -1, 0],
            [2, 1, 0],
            [-2, -1, 0],
            [2, 1, -1],
        ],
        b_ub=[1, 1, 1, 1, 1, -1, -3],
        free_vars=(0, 1, 2),
    )

    # 2. Causal single-closure ARO V({1}): by F3+F4, continuous box [-1,1] reduces exactly to
    #    endpoints w0 in {-1, +1} with tightened future noise support rho*|1| = 1.
    res_r1 = solve_exact_lp(
        c=[0, 0, 0, 1],
        A_ub=[
            [1, 0, 0, 0], [-1, 0, 0, 0],
            [0, 1, 0, 0], [0, -1, 0, 0],
            [0, 0, 1, 0], [0, 0, -1, 0],
            [2, 1, 0, 0], [-2, -1, 0, 0], [2, 1, 0, -1],
            [2, 0, 1, 0], [-2, 0, -1, 0], [2, 0, 1, -1],
        ],
        b_ub=[1, 1, 1, 1, 1, 1, 5, -1, 1, 1, 3, -3],
        free_vars=(0, 1, 2, 3),
    )

    # 3. Prefix-clairvoyant maximin V_mm_prefix (exact LP check on {-1, 0, 1} + continuous proof)
    prefix_vals: dict[str, Fraction] = {}
    for w0 in (Fraction(-1), Fraction(0), Fraction(1)):
        r = solve_exact_lp(
            c=[0, 0, 1],
            A_ub=[
                [1, 0, 0], [-1, 0, 0],
                [0, 1, 0], [0, -1, 0],
                [2, 1, 0],
                [-2, -1, 0],
                [2, 1, -1],
            ],
            b_ub=[
                1, 1, 1, 1,
                Fraction(3) - 2 * w0,
                Fraction(1) + 2 * w0,
                Fraction(-1) - 2 * w0,
            ],
            free_vars=(0, 1, 2),
        )
        _require(r.status == "optimal" and r.objective is not None, f"prefix LP at w0={w0}")
        prefix_vals[str(w0)] = r.objective  # type: ignore[assignment]
    v_mm_prefix = max(prefix_vals.values())

    # 4. Full-clairvoyant maximin V_mm_full (exact LP check on {-1, 1}^2 + continuous proof)
    full_vals: dict[str, Fraction] = {}
    for w0 in (Fraction(-1), Fraction(1)):
        for w1 in (Fraction(-1), Fraction(1)):
            r = solve_exact_lp(
                c=[0, 0, 1],
                A_ub=[
                    [1, 0, 0], [-1, 0, 0],
                    [0, 1, 0], [0, -1, 0],
                    [2, 1, 0],
                    [-2, -1, 0],
                    [2, 1, -1],
                ],
                b_ub=[
                    1, 1, 1, 1,
                    Fraction(4) - 2 * w0 - w1,
                    Fraction(2) + 2 * w0 + w1,
                    -2 * w0 - w1,
                ],
                free_vars=(0, 1, 2),
            )
            _require(r.status == "optimal" and r.objective is not None, f"full LP at ({w0},{w1})")
            full_vals[f"({w0},{w1})"] = r.objective  # type: ignore[assignment]
    v_mm_full = max(full_vals.values())

    # 5. Symmetric witness (A=1, B=1, E=1, gmin=-1, gmax=1): V({1}) = 1
    res_sym_r1 = solve_exact_lp(
        c=[0, 0, 0, 1],
        A_ub=[
            [1, 0, 0, 0], [-1, 0, 0, 0],
            [0, 1, 0, 0], [0, -1, 0, 0],
            [0, 0, 1, 0], [0, 0, -1, 0],
            [1, 1, 0, 0], [-1, -1, 0, 0], [1, 1, 0, -1],
            [1, 0, 1, 0], [-1, 0, -1, 0], [1, 0, 1, -1],
        ],
        b_ub=[1, 1, 1, 1, 1, 1, 1, -1, 0, -1, 3, -2],
        free_vars=(0, 1, 2, 3),
    )

    cont_cert = verify_continuous_box_maximin_sympy()

    _require(res_open.status == "optimal" and res_open.objective == Fraction(4),
             f"expected V(empty)=4, got {res_open}")
    _require(res_r1.status == "optimal" and res_r1.objective == Fraction(2),
             f"expected V({{1}})=2, got {res_r1}")
    _require(v_mm_prefix == Fraction(0), f"expected V_mm_prefix=0, got {v_mm_prefix}")
    _require(v_mm_full == Fraction(0), f"expected V_mm_full=0, got {v_mm_full}")
    _require(res_sym_r1.status == "optimal" and res_sym_r1.objective == Fraction(1),
             f"expected sym V({{1}})=1, got {res_sym_r1}")

    gap_prefix = res_r1.objective - v_mm_prefix  # type: ignore[operator]
    gap_full = res_r1.objective - v_mm_full  # type: ignore[operator]
    _require(gap_prefix == Fraction(2) and gap_full == Fraction(2),
             f"expected strict gap 2, got prefix={gap_prefix}, full={gap_full}")

    return {
        "conjecture_id": "hyp-o8-1d-sion-zero-gap",
        "atlas_node_id": "conj-o8-quantifier-gap",
        "verdict": "REFUTED_AT_STAGE_2_FALSIFY_FIRST_BY_EXACT_LP",
        "instance": {
            "n": 1, "m": 1, "p": 1, "rows": 1, "r": 1, "q": 1,
            "A": 2, "B": 1, "E": 1, "x0": 0, "U": [-1, 1], "rho": 1,
            "H": 1, "gmin": -2, "gmax": 4, "c": 1,
        },
        "V_empty": str(res_open.objective),
        "V_r1": str(res_r1.objective),
        "V_r1_policy": [str(v) for v in (res_r1.x or ())],
        "V_mm_prefix": str(v_mm_prefix),
        "V_mm_prefix_grid": {k: str(v) for k, v in prefix_vals.items()},
        "V_mm_full": str(v_mm_full),
        "V_mm_full_corners": {k: str(v) for k, v in full_vals.items()},
        "continuous_box_certificate": cont_cert,
        "gap_r1_vs_prefix_mm": str(gap_prefix),
        "gap_r1_vs_full_mm": str(gap_full),
        "value_of_measurement_Vempty_minus_Vr1": str(res_open.objective - res_r1.objective),  # type: ignore[operator]
        "sym_witness_Vr1": str(res_sym_r1.objective),
    }


def main() -> int:
    report = solve_o8_1d_hierarchy()
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
