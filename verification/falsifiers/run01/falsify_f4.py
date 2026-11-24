#!/usr/bin/env python3
"""Stage 2 (FALSIFY_FIRST) exact rational LP falsifier for F4 (conj-f4-vertex-lp-selector).

Tests F4 across 4 diverse rational BridgeFormalV2.Data instances, INCLUDING strictly
non-injective zonotope projections L: W^r -> R^n (e.g. r*p = 2 -> n = 1 and r*p = 3 -> n = 1
and r*p = 4 -> n = 2 with rank-deficient L), checking:
  1. Exact rational Vertex-LP solution (a*, u_vert*, eta*);
  2. Exact rational lexicographic-minimum right-inverse w*(xi) on interior zonotope points
     (where L^{-1}(xi) cap W^r is a non-singleton segment/polytope!);
  3. Exact multilinear barycentric weights alpha_sigma(w*(xi)) >= 0, sum = 1,
     sum alpha_sigma corner(sigma) == w*(xi), L(w*(xi)) == xi;
  4. Interpolated control b(xi) in [umin, umax]^q and ALL tightened row & cost inequalities
     satisfied with exact Fraction arithmetic (zero floating-point error).
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


def mat_vec(M: list[list[Fraction]], v: list[Fraction]) -> list[Fraction]:
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


def vec_add(u: list[Fraction], v: list[Fraction]) -> list[Fraction]:
    return [u[i] + v[i] for i in range(len(u))]


def mat_pow(A: list[list[Fraction]], k: int) -> list[list[Fraction]]:
    n = len(A)
    res = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
    for _ in range(k):
        res = [
            [sum(res[i][t] * A[t][j] for t in range(n)) for j in range(n)]
            for i in range(n)
        ]
    return res


def check_f4_instance(inst: dict[str, Any]) -> dict[str, Any]:
    n, m, p, rows, r, q = (
        inst["n"], inst["m"], inst["p"], inst["rows"], inst["r"], inst["q"]
    )
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

    # Prefix deviation matrix L: R^(r*p) -> R^n
    # deviation(w) = sum_{t=0}^{r-1} A^{r-1-t} E w_t
    L_cols: list[list[Fraction]] = []
    for t in range(r):
        AtE = [
            [sum(mat_pow(A, r - 1 - t)[i][k] * E[k][j] for k in range(n)) for j in range(p)]
            for i in range(n)
        ]
        for j in range(p):
            L_cols.append([AtE[i][j] for i in range(n)])
    N = r * p

    def deviation(w_flat: list[Fraction]) -> list[Fraction]:
        return [sum(L_cols[k][i] * w_flat[k] for k in range(N)) for i in range(n)]

    # Future noise support for any linear functional row_vec: R^n -> R
    # futureRowSupport(row) = rho * sum_{t=0}^{q-1} sum_{j=0}^{p-1} |row (A^{q-1-t} E e_j)|
    def future_support(row_vec: list[Fraction]) -> Fraction:
        tot = Fraction(0)
        for t in range(q):
            At = mat_pow(A, q - 1 - t)
            for j in range(p):
                col = [sum(At[i][k] * E[k][j] for k in range(n)) for i in range(n)]
                val = sum(row_vec[i] * col[i] for i in range(n))
                tot += abs(val)
        return rho * tot

    # Suffix control effect matrix G_u: R^(q*m) -> R^n, and A^q
    Aq = mat_pow(A, q)
    Gu_cols: list[list[Fraction]] = []
    for t in range(q):
        At = mat_pow(A, q - 1 - t)
        for j in range(m):
            Gu_cols.append([sum(At[i][k] * B[k][j] for k in range(n)) for i in range(n)])

    # Prefix nominal control effect matrix G_a: R^(r*m) -> R^n, plus A^r x0
    Ar = mat_pow(A, r)
    base_x = mat_vec(Ar, x0)
    Ga_cols: list[list[Fraction]] = []
    for t in range(r):
        At = mat_pow(A, r - 1 - t)
        for j in range(m):
            Ga_cols.append([sum(At[i][k] * B[k][j] for k in range(n)) for i in range(n)])

    # Corners of W^r: all 2^N sign tuples in {False, True}^N
    corners = list(itertools.product([False, True], repeat=N))
    corner_w = [[rho if bit else -rho for bit in sig] for sig in corners]
    corner_xi = [deviation(w) for w in corner_w]

    # Build exact Vertex-LP: variables = [a (r*m), b_0 (q*m), ..., b_{2^N-1} (q*m), eta (1)]
    n_a = r * m
    n_b = q * m
    n_c = len(corners)
    n_vars = n_a + n_c * n_b + 1
    eta_idx = n_vars - 1

    A_ub: list[list[Fraction]] = []
    b_ub: list[Fraction] = []

    # Box bounds on a
    for t in range(r):
        for j in range(m):
            idx = t * m + j
            row_u = [Fraction(0)] * n_vars
            row_u[idx] = Fraction(1)
            A_ub.append(row_u); b_ub.append(umax[j])
            row_l = [Fraction(0)] * n_vars
            row_l[idx] = Fraction(-1)
            A_ub.append(row_l); b_ub.append(-umin[j])

    # Box bounds on each corner b_s
    for s in range(n_c):
        off = n_a + s * n_b
        for t in range(q):
            for j in range(m):
                idx = off + t * m + j
                row_u = [Fraction(0)] * n_vars
                row_u[idx] = Fraction(1)
                A_ub.append(row_u); b_ub.append(umax[j])
                row_l = [Fraction(0)] * n_vars
                row_l[idx] = Fraction(-1)
                A_ub.append(row_l); b_ub.append(-umin[j])

    # Tightened terminal rows & cost at every corner s
    # z(a, xi, b) = Aq (base_x + Ga a + xi) + Gu b
    # row(z) = row(Aq base_x) + row(Aq xi) + sum_k row(Aq Ga_k) a_k + sum_l row(Gu_l) b_l
    def add_tightened_rows(s: int, xi: list[Fraction]) -> None:
        off = n_a + s * n_b
        # Terminal rows H_i
        for i in range(rows):
            h_i = H[i]
            neg_h_i = [-v for v in h_i]
            for row_vec, rhs_lim in ((h_i, gmax[i]), (neg_h_i, -gmin[i])):
                supp = future_support(row_vec)
                const_part = (
                    sum(row_vec[d] * mat_vec(Aq, base_x)[d] for d in range(n))
                    + sum(row_vec[d] * mat_vec(Aq, xi)[d] for d in range(n))
                    + supp
                )
                coeffs = [Fraction(0)] * n_vars
                for k in range(n_a):
                    aq_ga = mat_vec(Aq, Ga_cols[k])
                    coeffs[k] = sum(row_vec[d] * aq_ga[d] for d in range(n))
                for l in range(n_b):
                    coeffs[off + l] = sum(row_vec[d] * Gu_cols[l][d] for d in range(n))
                A_ub.append(coeffs)
                b_ub.append(rhs_lim - const_part)
        # Cost row c
        supp_c = future_support(c)
        const_c = (
            sum(c[d] * mat_vec(Aq, base_x)[d] for d in range(n))
            + sum(c[d] * mat_vec(Aq, xi)[d] for d in range(n))
            + supp_c
        )
        coeffs_c = [Fraction(0)] * n_vars
        for k in range(n_a):
            aq_ga = mat_vec(Aq, Ga_cols[k])
            coeffs_c[k] = sum(c[d] * aq_ga[d] for d in range(n))
        for l in range(n_b):
            coeffs_c[off + l] = sum(c[d] * Gu_cols[l][d] for d in range(n))
        coeffs_c[eta_idx] = Fraction(-1)
        A_ub.append(coeffs_c)
        b_ub.append(-const_c)

    for s, xi in enumerate(corner_xi):
        add_tightened_rows(s, xi)

    obj_c = [Fraction(0)] * n_vars
    obj_c[eta_idx] = Fraction(1)
    lp_res = solve_exact_lp(obj_c, A_ub=A_ub, b_ub=b_ub, free_vars=tuple(range(n_vars)))
    if lp_res.status != "optimal" or lp_res.x is None or lp_res.objective is None:
        return {"name": inst["name"], "survived": False, "reason": f"Vertex LP status={lp_res.status}"}

    sol = lp_res.x
    a_star = list(sol[:n_a])
    u_vert = [list(sol[n_a + s * n_b : n_a + (s + 1) * n_b]) for s in range(n_c)]
    eta_star = lp_res.objective

    # Compute exact lexicographic-minimum right-inverse w*(xi) for interior zonotope points
    def lex_min_preimage(xi_target: list[Fraction]) -> list[Fraction]:
        fixed: list[Fraction] = []
        for coord in range(N):
            c_lex = [Fraction(1 if j == coord else 0) for j in range(N)]
            A_ub_lex = []
            b_ub_lex = []
            for j in range(N):
                r1 = [Fraction(1 if k == j else 0) for k in range(N)]
                r2 = [Fraction(-1 if k == j else 0) for k in range(N)]
                A_ub_lex.extend([r1, r2])
                b_ub_lex.extend([rho, rho])
            A_eq_lex = [[L_cols[j][d] for j in range(N)] for d in range(n)]
            b_eq_lex = list(xi_target)
            for prev_j, prev_val in enumerate(fixed):
                A_eq_lex.append([Fraction(1 if k == prev_j else 0) for k in range(N)])
                b_eq_lex.append(prev_val)
            r_lex = solve_exact_lp(
                c_lex, A_ub=A_ub_lex, b_ub=b_ub_lex, A_eq=A_eq_lex, b_eq=b_eq_lex,
                free_vars=tuple(range(N)),
            )
            if r_lex.status != "optimal" or r_lex.objective is None:
                raise RuntimeError(f"Lexicographic preimage failed at coord {coord}: {r_lex.status}")
            fixed.append(r_lex.objective)
        return fixed

    # Test interior probe points generated from interior w_probe in (-rho, rho)^N
    checked = 0
    for w_probe_raw in inst["probe_w"]:
        w_probe = [Fraction(v) for v in w_probe_raw]
        xi_target = deviation(w_probe)
        w_sel = lex_min_preimage(xi_target)

        # Verify exact right-inverse: w_sel in W^r and L(w_sel) == xi_target
        if not all(-rho <= val <= rho for val in w_sel):
            return {"name": inst["name"], "survived": False, "reason": "w_sel out of W^r"}
        if deviation(w_sel) != xi_target:
            return {"name": inst["name"], "survived": False, "reason": "L(w_sel) != xi_target"}

        # Multilinear barycentric weights alpha_sigma(w_sel)
        alphas: list[Fraction] = []
        for sig in corners:
            prod = Fraction(1)
            for k, bit in enumerate(sig):
                wt = (rho + w_sel[k]) / (2 * rho) if bit else (rho - w_sel[k]) / (2 * rho)
                prod *= wt
            alphas.append(prod)

        if any(al < 0 for al in alphas) or sum(alphas) != Fraction(1):
            return {"name": inst["name"], "survived": False, "reason": "invalid barycentric weights"}
        recon_w = [sum(alphas[s] * corner_w[s][k] for s in range(n_c)) for k in range(N)]
        if recon_w != w_sel:
            return {"name": inst["name"], "survived": False, "reason": "barycentric w mismatch"}

        # Interpolated suffix control b(xi) = sum_s alpha_s * u_vert[s]
        b_sel = [sum(alphas[s] * u_vert[s][l] for s in range(n_c)) for l in range(n_b)]
        for t in range(q):
            for j in range(m):
                val = b_sel[t * m + j]
                if not (umin[j] <= val <= umax[j]):
                    return {"name": inst["name"], "survived": False, "reason": "control out of box"}

        # Nominal terminal state z = Aq (base_x + Ga a* + xi_target) + Gu b_sel
        nom_a = vec_add(
            base_x,
            [sum(Ga_cols[k][d] * a_star[k] for k in range(n_a)) for d in range(n)],
        )
        z = vec_add(
            mat_vec(Aq, vec_add(nom_a, xi_target)),
            [sum(Gu_cols[l][d] * b_sel[l] for l in range(n_b)) for d in range(n)],
        )
        # Check EVERY tightened row & cost inequality
        for i in range(rows):
            hz = sum(H[i][d] * z[d] for d in range(n))
            supp_u = future_support(H[i])
            supp_l = future_support([-v for v in H[i]])
            if hz + supp_u > gmax[i] or (-hz) + supp_l > -gmin[i]:
                return {"name": inst["name"], "survived": False, "reason": f"row {i} violated"}
        cz = sum(c[d] * z[d] for d in range(n))
        if cz + future_support(c) > eta_star:
            return {"name": inst["name"], "survived": False, "reason": "cost violated"}
        checked += 1

    # Extract TRUE distinct extreme points vert(Xi) from unique corner images via exact LP!
    unique_pts: list[list[Fraction]] = []
    for xi in corner_xi:
        if xi not in unique_pts:
            unique_pts.append(xi)

    true_vertices: list[list[Fraction]] = []
    for idx_v, v in enumerate(unique_pts):
        others = [u for j, u in enumerate(unique_pts) if j != idx_v]
        if not others:
            true_vertices.append(v)
            continue
        # Test if v lies in conv(others): exists lam >= 0, sum lam = 1, sum lam_j u_j = v
        k_oth = len(others)
        A_eq_v = [[others[j][d] for j in range(k_oth)] for d in range(n)]
        A_eq_v.append([Fraction(1)] * k_oth)
        b_eq_v = list(v) + [Fraction(1)]
        r_conv = solve_exact_lp(
            [Fraction(0)] * k_oth, A_eq=A_eq_v, b_eq=b_eq_v
        )
        if r_conv.status == "infeasible":
            true_vertices.append(v)

    # Solve TRUE vert(Xi)-indexed LP directly and confirm eta_ext == eta_corner!
    n_ext = len(true_vertices)
    n_vars_ext = n_a + n_ext * n_b + 1
    eta_ext_idx = n_vars_ext - 1
    A_ub_ext: list[list[Fraction]] = []
    b_ub_ext: list[Fraction] = []
    for t in range(r):
        for j in range(m):
            idx = t * m + j
            r_u = [Fraction(0)] * n_vars_ext; r_u[idx] = Fraction(1)
            A_ub_ext.append(r_u); b_ub_ext.append(umax[j])
            r_l = [Fraction(0)] * n_vars_ext; r_l[idx] = Fraction(-1)
            A_ub_ext.append(r_l); b_ub_ext.append(-umin[j])
    for s in range(n_ext):
        off = n_a + s * n_b
        for t in range(q):
            for j in range(m):
                idx = off + t * m + j
                r_u = [Fraction(0)] * n_vars_ext; r_u[idx] = Fraction(1)
                A_ub_ext.append(r_u); b_ub_ext.append(umax[j])
                r_l = [Fraction(0)] * n_vars_ext; r_l[idx] = Fraction(-1)
                A_ub_ext.append(r_l); b_ub_ext.append(-umin[j])
        xi = true_vertices[s]
        for i in range(rows):
            h_i = H[i]
            neg_h_i = [-val for val in h_i]
            for row_vec, rhs_lim in ((h_i, gmax[i]), (neg_h_i, -gmin[i])):
                supp = future_support(row_vec)
                const_part = (
                    sum(row_vec[d] * mat_vec(Aq, base_x)[d] for d in range(n))
                    + sum(row_vec[d] * mat_vec(Aq, xi)[d] for d in range(n))
                    + supp
                )
                coeffs = [Fraction(0)] * n_vars_ext
                for k in range(n_a):
                    aq_ga = mat_vec(Aq, Ga_cols[k])
                    coeffs[k] = sum(row_vec[d] * aq_ga[d] for d in range(n))
                for l in range(n_b):
                    coeffs[off + l] = sum(row_vec[d] * Gu_cols[l][d] for d in range(n))
                A_ub_ext.append(coeffs)
                b_ub_ext.append(rhs_lim - const_part)
        supp_c = future_support(c)
        const_c = (
            sum(c[d] * mat_vec(Aq, base_x)[d] for d in range(n))
            + sum(c[d] * mat_vec(Aq, xi)[d] for d in range(n))
            + supp_c
        )
        coeffs_c = [Fraction(0)] * n_vars_ext
        for k in range(n_a):
            aq_ga = mat_vec(Aq, Ga_cols[k])
            coeffs_c[k] = sum(c[d] * aq_ga[d] for d in range(n))
        for l in range(n_b):
            coeffs_c[off + l] = sum(c[d] * Gu_cols[l][d] for d in range(n))
        coeffs_c[eta_ext_idx] = Fraction(-1)
        A_ub_ext.append(coeffs_c)
        b_ub_ext.append(-const_c)
    obj_ext = [Fraction(0)] * n_vars_ext
    obj_ext[eta_ext_idx] = Fraction(1)
    lp_ext = solve_exact_lp(
        obj_ext, A_ub=A_ub_ext, b_ub=b_ub_ext, free_vars=tuple(range(n_vars_ext))
    )
    if lp_ext.status != "optimal" or lp_ext.objective != eta_star:
        return {
            "name": inst["name"],
            "survived": False,
            "reason": f"vert(Xi) LP mismatch: {lp_ext.objective} != {eta_star}",
        }

    return {
        "name": inst["name"],
        "survived": True,
        "corners": n_c,
        "true_vertices_count": n_ext,
        "checked_interior_points": checked,
        "eta_star_exact": str(eta_star),
        "eta_vert_xi_exact": str(lp_ext.objective),
        "non_injective": N > n,
    }


INSTANCES = [
    {
        "name": "1d_non_injective_2to1_zonotope",
        "n": 1, "m": 1, "p": 1, "rows": 1, "r": 2, "q": 1,
        "A": [[2]], "B": [[1]], "E": [[1]], "H": [[1]], "c": [1],
        "x0": [0], "umin": [-3], "umax": [3], "gmin": [-4], "gmax": [6], "rho": 1,
        "probe_w": [["0", "0"], ["1/3", "-1/2"], ["-2/3", "1/4"], ["1/2", "1/2"]],
    },
    {
        "name": "1d_non_injective_3to1_asymmetric",
        "n": 1, "m": 1, "p": 1, "rows": 1, "r": 3, "q": 1,
        "A": [["3/2"]], "B": [[1]], "E": [["1/2"]], "H": [[1]], "c": [1],
        "x0": ["1/2"], "umin": [-4], "umax": [5], "gmin": [-3], "gmax": [7], "rho": "1/2",
        "probe_w": [["0", "0", "0"], ["1/4", "-1/4", "1/3"], ["-1/3", "1/6", "-1/6"]],
    },
    {
        "name": "2d_non_injective_4to2_zonotope",
        "n": 2, "m": 1, "p": 2, "rows": 2, "r": 2, "q": 1,
        "A": [[1, 1], [0, 1]],
        "B": [[1], [1]],
        "E": [[1, -1], [0, 1]],
        "H": [[1, 0], [0, 1]],
        "c": [1, 2],
        "x0": [0, 0], "umin": [-5], "umax": [5],
        "gmin": [-8, -6], "gmax": [8, 6], "rho": "1/2",
        "probe_w": [
            ["0", "0", "0", "0"],
            ["1/4", "-1/4", "1/6", "-1/3"],
            ["-1/3", "1/5", "-1/4", "1/4"],
        ],
    },
    {
        "name": "2d_multi_suffix_q2_injective",
        "n": 2, "m": 2, "p": 1, "rows": 2, "r": 2, "q": 2,
        "A": [[1, "1/2"], [0, 1]],
        "B": [[1, 0], [0, 1]],
        "E": [[1], [1]],
        "H": [[1, 1], [1, -1]],
        "c": [2, -1],
        "x0": [1, -1], "umin": [-3, -2], "umax": [3, 4],
        "gmin": [-10, -10], "gmax": [10, 10], "rho": 1,
        "probe_w": [["0", "0"], ["1/2", "-1/3"], ["-3/4", "2/5"]],
    },
]

results = [check_f4_instance(inst) for inst in INSTANCES]
all_ok = all(r["survived"] for r in results)
tot_pts = sum(r.get("checked_interior_points", 0) for r in results)
print(json.dumps({"survived": all_ok, "checked_points": tot_pts, "instances": results}, indent=2))
sys.exit(0 if all_ok else 1)
