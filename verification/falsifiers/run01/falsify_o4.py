#!/usr/bin/env python3
"""Stage 2 (FALSIFY_FIRST) exact rational LP verifier on 7 concrete instances for O4 (conj-o4-closure-scheduling).

Executes `solve_exact_lp` (exact Fraction simplex) on 7 concrete rational instances:
  1. Zero-gain Theorem O4.2 (`rows = 0`, unconstrained terminal): checks `V({r}) == V(empty)`
     on 2 concrete instances (`1D A=2` -> `(3, 3)`; `2D coupled` -> `(-31, -31)`).
  2. Zero-gain Theorem O4.3 (`ker(H A^q) cap ker(c A^q)`): checks `V({r}) == V(empty)` (`(-2, -2)`).
  3. Strict-gain witness O4.6 (`strictGainWitnessData`): checks exact optima `V(empty) = 4 > V({1}) = 2`.
  4. Schedule non-monotonicity across `r in {1, 2, 3}` for `T = 4` (`gmin=-2, gmax=6`): checks exact
     `V(empty) = 6` for all three splits and `V({1}) = 4 > V({2}) = 2 < V({3}) = 4`, refuting
     universal monotone-in-`r` placement.
"""
from __future__ import annotations

import itertools
import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from verification.oracles.exact_lp import solve_exact_lp


def mat_pow(A: list[list[Fraction]], k: int) -> list[list[Fraction]]:
    n = len(A)
    res = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for _ in range(k):
        res = [[sum(res[i][t] * A[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
    return res


def mat_vec(M: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def solve_open_and_single_closure(inst: dict[str, Any]) -> dict[str, Any]:
    """Solve BOTH exact open-loop V(empty) AND exact single-closure V({r}) via Vertex-LP."""
    n, m, p, rows, r, q = inst["n"], inst["m"], inst["p"], inst["rows"], inst["r"], inst["q"]
    A = [[Fraction(v) for v in row] for row in inst["A"]]
    B = [[Fraction(v) for v in row] for row in inst["B"]]
    E = [[Fraction(v) for v in row] for row in inst["E"]]
    H = [[Fraction(v) for v in row] for row in inst["H"]]
    c = [Fraction(v) for v in inst["c"]]
    x0 = [Fraction(v) for v in inst["x0"]]
    umin = [Fraction(v) for v in inst["umin"]]
    umax = [Fraction(v) for v in inst["umax"]]
    gmin = [Fraction(v) for v in inst["gmin"]]
    gmax = [Fraction(v) for v in inst["gmax"]]
    rho = Fraction(inst["rho"])

    def future_support(row_vec: list[Fraction]) -> Fraction:
        tot = Fraction(0)
        for t in range(q):
            At = mat_pow(A, q - 1 - t)
            for j in range(p):
                col = [sum(At[i][k] * E[k][j] for k in range(n)) for i in range(n)]
                tot += abs(sum(row_vec[i] * col[i] for i in range(n)))
        return rho * tot

    Aq = mat_pow(A, q)
    Ar = mat_pow(A, r)
    base_x = mat_vec(Ar, x0)

    L_cols: list[list[Fraction]] = []
    for t in range(r):
        At = mat_pow(A, r - 1 - t)
        for j in range(p):
            L_cols.append([sum(At[i][k] * E[k][j] for k in range(n)) for i in range(n)])
    N = r * p
    corners = list(itertools.product([False, True], repeat=N))
    corner_xi = [
        [sum(L_cols[k][i] * (rho if sig[k] else -rho) for k in range(N)) for i in range(n)]
        for sig in corners
    ]

    Ga_cols: list[list[Fraction]] = []
    for t in range(r):
        At = mat_pow(A, r - 1 - t)
        for j in range(m):
            Ga_cols.append([sum(At[i][k] * B[k][j] for k in range(n)) for i in range(n)])
    Gu_cols: list[list[Fraction]] = []
    for t in range(q):
        At = mat_pow(A, q - 1 - t)
        for j in range(m):
            Gu_cols.append([sum(At[i][k] * B[k][j] for k in range(n)) for i in range(n)])

    n_a, n_b, n_c = r * m, q * m, len(corners)

    def _solve_mode(shared_b: bool) -> Any:
        n_blocks = 1 if shared_b else n_c
        n_vars = n_a + n_blocks * n_b + 1
        eta_idx = n_vars - 1
        A_ub: list[list[Fraction]] = []
        b_ub: list[Fraction] = []
        for t in range(r):
            for j in range(m):
                idx = t * m + j
                ru = [Fraction(0)] * n_vars; ru[idx] = Fraction(1)
                rl = [Fraction(0)] * n_vars; rl[idx] = Fraction(-1)
                A_ub.extend([ru, rl]); b_ub.extend([umax[j], -umin[j]])
        for blk in range(n_blocks):
            off = n_a + blk * n_b
            for t in range(q):
                for j in range(m):
                    idx = off + t * m + j
                    ru = [Fraction(0)] * n_vars; ru[idx] = Fraction(1)
                    rl = [Fraction(0)] * n_vars; rl[idx] = Fraction(-1)
                    A_ub.extend([ru, rl]); b_ub.extend([umax[j], -umin[j]])
        for s, xi in enumerate(corner_xi):
            off = n_a if shared_b else (n_a + s * n_b)
            for i in range(rows):
                hi = H[i]
                for rv, lim in ((hi, gmax[i]), ([-v for v in hi], -gmin[i])):
                    const_p = (
                        sum(rv[d] * mat_vec(Aq, base_x)[d] for d in range(n))
                        + sum(rv[d] * mat_vec(Aq, xi)[d] for d in range(n))
                        + future_support(rv)
                    )
                    row_c = [Fraction(0)] * n_vars
                    for k in range(n_a):
                        aq_ga = mat_vec(Aq, Ga_cols[k])
                        row_c[k] = sum(rv[d] * aq_ga[d] for d in range(n))
                    for l in range(n_b):
                        row_c[off + l] = sum(rv[d] * Gu_cols[l][d] for d in range(n))
                    A_ub.append(row_c); b_ub.append(lim - const_p)
            const_c = (
                sum(c[d] * mat_vec(Aq, base_x)[d] for d in range(n))
                + sum(c[d] * mat_vec(Aq, xi)[d] for d in range(n))
                + future_support(c)
            )
            row_cc = [Fraction(0)] * n_vars
            for k in range(n_a):
                aq_ga = mat_vec(Aq, Ga_cols[k])
                row_cc[k] = sum(c[d] * aq_ga[d] for d in range(n))
            for l in range(n_b):
                row_cc[off + l] = sum(c[d] * Gu_cols[l][d] for d in range(n))
            row_cc[eta_idx] = Fraction(-1)
            A_ub.append(row_cc); b_ub.append(-const_c)
        obj = [Fraction(0)] * n_vars
        obj[eta_idx] = Fraction(1)
        return solve_exact_lp(obj, A_ub=A_ub, b_ub=b_ub, free_vars=tuple(range(n_vars)))

    r_open = _solve_mode(shared_b=True)
    r_clos = _solve_mode(shared_b=False)
    return {
        "name": inst["name"],
        "open_status": r_open.status,
        "V_empty": str(r_open.objective) if r_open.objective is not None else None,
        "closure_status": r_clos.status,
        "V_r": str(r_clos.objective) if r_clos.objective is not None else None,
        "strict_gain": (
            str(r_open.objective - r_clos.objective)
            if (r_open.objective is not None and r_clos.objective is not None)
            else None
        ),
    }


def main() -> None:
    # 1. Unconstrained terminal (rows=0) -> MUST have V({r}) == V(empty)
    zero_gain_rows0 = [
        {
            "name": "rows0_1d_A2",
            "n": 1, "m": 1, "p": 1, "rows": 0, "r": 2, "q": 1,
            "A": [[2]], "B": [[1]], "E": [[1]], "H": [], "c": [3],
            "x0": [1], "umin": [-2], "umax": [3], "gmin": [], "gmax": [], "rho": 1,
        },
        {
            "name": "rows0_2d_coupled",
            "n": 2, "m": 2, "p": 1, "rows": 0, "r": 2, "q": 2,
            "A": [[1, 2], [0, -1]], "B": [[1, 0], [1, 1]], "E": [[1], [2]],
            "H": [], "c": [2, -3], "x0": [1, -1],
            "umin": [-1, -2], "umax": [2, 1], "gmin": [], "gmax": [], "rho": "1/2",
        },
    ]
    res_rows0 = [solve_open_and_single_closure(inst) for inst in zero_gain_rows0]
    rows0_ok = all(r["strict_gain"] == "0" for r in res_rows0)

    # 2. Prefix deviation in ker(H A^q) cap ker(c A^q) -> MUST have V({r}) == V(empty)
    # 2D system where E = [[0], [1]], A = [[1, 0], [0, 0]] (nilpotent on coord 2), H = [[1, 0]], c = [1, 0]
    ker_inst = {
        "name": "prefix_in_terminal_kernel_2d",
        "n": 2, "m": 1, "p": 1, "rows": 1, "r": 1, "q": 1,
        "A": [[1, 0], [0, 0]], "B": [[1], [1]], "E": [[0], [1]],
        "H": [[1, 0]], "c": [1, 0], "x0": [0, 0],
        "umin": [-1], "umax": [1], "gmin": [-2], "gmax": [2], "rho": 1,
    }
    res_ker = solve_open_and_single_closure(ker_inst)
    ker_ok = res_ker["strict_gain"] == "0"

    # 3. Strict gain witness (O4.6): V(empty)=4 > V({1})=2 (gap=2)
    strict_inst = {
        "name": "strict_gain_1d_witness",
        "n": 1, "m": 1, "p": 1, "rows": 1, "r": 1, "q": 1,
        "A": [[2]], "B": [[1]], "E": [[1]], "H": [[1]], "c": [1],
        "x0": [0], "umin": [-1], "umax": [1], "gmin": [-2], "gmax": [4], "rho": 1,
    }
    res_strict = solve_open_and_single_closure(strict_inst)
    strict_ok = res_strict["V_empty"] == "4" and res_strict["V_r"] == "2"

    # 4. Schedule non-monotonicity across r in {1, 2, 3} for T=4 (refutes monotone-in-r!)
    # A = 1, B = 1, E = 1, U = [-1, 1], rho = 1, gmin = -2, gmax = 6, c = 1
    sched_results = []
    for r_val in (1, 2, 3):
        q_val = 4 - r_val
        inst_r = {
            "name": f"T4_schedule_r{r_val}",
            "n": 1, "m": 1, "p": 1, "rows": 1, "r": r_val, "q": q_val,
            "A": [[1]], "B": [[1]], "E": [[1]], "H": [[1]], "c": [1],
            "x0": [0], "umin": [-1], "umax": [1], "gmin": [-2], "gmax": [6], "rho": 1,
        }
        sched_results.append(solve_open_and_single_closure(inst_r))

    v1 = Fraction(sched_results[0]["V_r"])
    v2 = Fraction(sched_results[1]["V_r"])
    v3 = Fraction(sched_results[2]["V_r"])
    all_open_6 = all(r["V_empty"] == "6" for r in sched_results)
    exact_t4_vals = (v1, v2, v3) == (Fraction(4), Fraction(2), Fraction(4))
    non_monotone_ok = all_open_6 and exact_t4_vals and (v2 < v1) and (v2 < v3)

    all_ok = rows0_ok and ker_ok and strict_ok and non_monotone_ok
    out = {
        "survived": all_ok,
        "checked_points": len(res_rows0) + 1 + 1 + len(sched_results),
        "zero_gain_rows0": res_rows0,
        "zero_gain_kernel": res_ker,
        "strict_gain_witness": res_strict,
        "schedule_T4_r1_r2_r3": sched_results,
        "non_monotone_valley_at_r2": non_monotone_ok,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
