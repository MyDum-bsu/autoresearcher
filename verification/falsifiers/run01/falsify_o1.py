#!/usr/bin/env python3
"""Stage 2 (FALSIFY_FIRST) exact rational verification for O1 (conj-o1-adr-exactness-char, partial).

Checks:
  1. Full T1-T7 falsification battery (`verification.falsifiers.battery_t1_t7.run_battery`):
     verifies all 7 cases pass (T1, T6, T7 exact; T2, T3, T4, T5 not_exact).
  2. Falsification of 4 naive structural O1 candidate predicates on T1-T7 via `evaluate_conjecture`,
     evaluated strictly from explicit geometric/structural descriptors of each T1-T7 instance
     (vertex sets with exact rational affine-independence rank test for simplex detection,
     polytope/ball flag, box/cube geometry check, and constraint-wise decoupling flag — no
     branching on `case_id` inside the candidate predicates):
       - simplex_only (falsified by T1, T4, T6)
       - constraint_wise_m1 (falsified by T1, T7)
       - fixed_recourse_polytope (falsified by T3, T4, T5)
       - box_or_cube_uncertainty (falsified by T4, T7, and also by the 2D Bridge box gap below)
  3. Exact rational LP verification of d-simplex ADR exactness on 6 randomized fixed-recourse
     instances across Delta_1, Delta_2, and Delta_3 (all V_ADR == V_ARO).
  4. Exact rational LP verification of 1D `BridgeFormalV2.Data` ADR exactness (jointly optimizing
     first-stage u_1 and second-stage u_2 with full F3 post-closure tightening) on 8 diverse
     1D instances (r in {1,2,3}, q in {1,2}, rows in {1,2,3}; all V_ADR == V_ARO).
  5. Exact rational LP + 5x5 grid witness verification for the minimal 2D `BridgeFormalV2.Data`
     strict ADR gap (`A=I_2, B=(1,1)^T, E=I_2, H=I_2, c=(1,1)^T, gmin=(0,0), gmax=(4,4),
     umax=1, rho=1`): V_ARO = 6 < V_ADR = 8 (strict gap 2), with nonlinear adaptive witness
     `u_1 = 1, u_2*(v_0, v_1) = max(-v_0, -v_1)` verified feasible with cost <= 6 at all 25 grid points.
"""
from __future__ import annotations

import dataclasses
import itertools
import json
import pathlib
import random
import sys
from fractions import Fraction
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from verification.falsifiers.battery_t1_t7 import (
    BatteryCaseResult,
    _solve_vertex_adr,
    _solve_vertex_aro,
    evaluate_conjecture,
    run_battery,
)
from verification.oracles.exact_lp import solve_exact_lp


@dataclasses.dataclass(frozen=True)
class StructuralFeatures:
    """Explicit structural data for a T1-T7 instance (matching `battery_t1_t7.py`)."""
    dim: int
    polytopal: bool
    fixed_recourse: bool
    constraint_wise_separable: bool
    vertices: tuple[tuple[Fraction, ...], ...] | None  # None for non-polytopal ball T2
    vertices_complete: bool = True
    # Optional separating-inequality certificate proving `not is_axis_aligned_box` when
    # `vertices_complete` is False: `(coord_i, coord_j, max_generator_sum)` such that
    # `max_v v[i] + max_v v[j] > max_generator_sum` while every generator of Xi satisfies
    # `x[i] + x[j] <= max_generator_sum` (checked over `vertices` and generator-family bound).
    non_box_sum_cert: tuple[int, int, Fraction] | None = None


def _exact_rank(rows: list[list[Fraction]]) -> int:
    """Exact Gaussian elimination rank over Q."""
    if not rows:
        return 0
    mat = [list(r) for r in rows]
    n_rows, n_cols = len(mat), len(mat[0])
    rank = 0
    for col in range(n_cols):
        pivot = None
        for r in range(rank, n_rows):
            if mat[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        piv_val = mat[rank][col]
        mat[rank] = [v / piv_val for v in mat[rank]]
        for r in range(n_rows):
            if r != rank and mat[r][col] != 0:
                factor = mat[r][col]
                mat[r] = [mat[r][c] - factor * mat[rank][c] for c in range(n_cols)]
        rank += 1
    return rank


def _is_simplex(feat: StructuralFeatures) -> bool:
    """Check whether vertices form an affinely independent d-simplex.

    When `vertices_complete` is False, only a certified lower bound `len(distinct vertices) > dim + 1`
    is accepted to return False (since a d-simplex has at most d + 1 distinct vertices).
    """
    if not feat.polytopal or feat.vertices is None:
        return False
    unique_verts = set(feat.vertices)
    if len(unique_verts) > feat.dim + 1:
        return False
    if not feat.vertices_complete:
        raise ValueError("Cannot decide simplex property from an incomplete vertex subset with <= d+1 points")
    if len(unique_verts) != feat.dim + 1:
        return False
    v0 = feat.vertices[0]
    diffs = [[v[j] - v0[j] for j in range(feat.dim)] for v in feat.vertices[1:]]
    return _exact_rank(diffs) == feat.dim


def _is_axis_aligned_box(feat: StructuralFeatures) -> bool:
    """Check whether a polytope is an axis-aligned box.

    When `vertices_complete` is True, checks exact equality with the 2^d Cartesian product of
    non-degenerate coordinate intervals. When `vertices_complete` is False, requires a verified
    separating-sum certificate `non_box_sum_cert = (i, j, ub)` proving that the coordinate-wise
    bounding box corner `(max v[i], max v[j])` violates `x[i] + x[j] <= ub` satisfied by all generators.
    """
    if not feat.polytopal or feat.vertices is None:
        return False
    if not feat.vertices_complete:
        if feat.non_box_sum_cert is None:
            raise ValueError("Cannot decide box property from an incomplete vertex subset without a certificate")
        ci, cj, max_gen_sum = feat.non_box_sum_cert
        max_i = max(v[ci] for v in feat.vertices)
        max_j = max(v[cj] for v in feat.vertices)
        if any(v[ci] + v[cj] > max_gen_sum for v in feat.vertices):
            raise ValueError("non_box_sum_cert upper bound violated on listed vertices")
        if max_i + max_j > max_gen_sum:
            return False
        raise ValueError("non_box_sum_cert does not separate the bounding-box corner")
    if len(feat.vertices) != (1 << feat.dim):
        return False
    coord_sets = [sorted({v[j] for v in feat.vertices}) for j in range(feat.dim)]
    if any(len(cs) != 2 for cs in coord_sets):
        return False
    expected = set(itertools.product(*coord_sets))
    return set(feat.vertices) == expected


def _build_t1_t7_features() -> dict[str, StructuralFeatures]:
    """Construct exact geometric descriptors matching the 7 instances in `battery_t1_t7.py`."""
    # T1 (2D bridge-class subinstance: square {-1, +1}^2, coupled recourse constraints)
    t1_verts = tuple((Fraction(w0), Fraction(w1)) for w0 in (-1, 1) for w1 in (-1, 1))
    # T3 (3D cross-polytope {+-e_1, +-e_2, +-e_3})
    t3_verts = tuple(
        tuple(Fraction(sgn) if j == i else Fraction(0) for j in range(3))
        for i in range(3)
        for sgn in (1, -1)
    )
    # T4 (1D interval [-1, 1] under expectation objective, coupled y1 + y2 >= xi + 1)
    t4_verts = ((Fraction(-1),), (Fraction(1),))
    t6_verts = tuple((Fraction(z1), Fraction(z2)) for z1 in (-1, 1) for z2 in (-1, 1))
    t7_verts = ((Fraction(0), Fraction(0)), (Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)))

    # Verbatim T5 (m=900, k=30, r=870): generator set is {0} U {e_0..e_899} U {nu_S : |S|=870}.
    # 1) Non-simplex certificate: the explicit 902-point subset {0, e_0..e_899, nu_first} already has
    #    902 > 900 + 1 distinct vertices (every vertex of Xi_T5 is extreme since ||e_i||_1=1,
    #    sum(nu_S)=870/30=29 > 1, and 0 is minimal).
    # 2) Non-box certificate: on ALL generators of Xi_T5, x_0 + x_1 <= max(0, 1, 2/30) = 1
    #    (0 gives 0, every e_i gives <= 1, every nu_S has entries in {0, 1/30} so nu_S[0]+nu_S[1] <= 2/30 = 1/15 <= 1),
    #    whereas the bounding box of {0, e_0, e_1} must contain e_0 + e_1 with x_0 + x_1 = 2 > 1.
    m_t5, k_t5, r_t5 = 900, 30, 870
    if Fraction(2, k_t5) > Fraction(1):
        raise RuntimeError("T5 nu_S generator bound 2/sqrt(m) <= 1 unexpectedly failed")
    nu_first = tuple(Fraction(1, k_t5) if j < r_t5 else Fraction(0) for j in range(m_t5))
    t5_subset_verts: list[tuple[Fraction, ...]] = [tuple(Fraction(0) for _ in range(m_t5)), nu_first]
    for i in range(m_t5):
        ei = [Fraction(0)] * m_t5
        ei[i] = Fraction(1)
        t5_subset_verts.append(tuple(ei))

    return {
        "T1": StructuralFeatures(dim=2, polytopal=True, fixed_recourse=True, constraint_wise_separable=False, vertices=t1_verts),
        "T2": StructuralFeatures(dim=2, polytopal=False, fixed_recourse=True, constraint_wise_separable=False, vertices=None),
        "T3": StructuralFeatures(dim=3, polytopal=True, fixed_recourse=True, constraint_wise_separable=False, vertices=t3_verts),
        "T4": StructuralFeatures(dim=1, polytopal=True, fixed_recourse=True, constraint_wise_separable=False, vertices=t4_verts),
        "T5": StructuralFeatures(
            dim=m_t5,
            polytopal=True,
            fixed_recourse=True,
            constraint_wise_separable=False,
            vertices=tuple(t5_subset_verts),
            vertices_complete=False,
            non_box_sum_cert=(0, 1, Fraction(1)),
        ),
        "T6": StructuralFeatures(dim=2, polytopal=True, fixed_recourse=True, constraint_wise_separable=True, vertices=t6_verts),
        "T7": StructuralFeatures(dim=2, polytopal=True, fixed_recourse=True, constraint_wise_separable=False, vertices=t7_verts),
    }


def check_t1_t7_and_naive_candidates() -> dict[str, Any]:
    battery = run_battery()
    battery_ok = len(battery) == 7 and all(c.passed for c in battery)
    features = _build_t1_t7_features()

    # Pure structural predicates operating ONLY on `StructuralFeatures` (zero branching on `case_id`)
    def pred_simplex_only(f: StructuralFeatures) -> str:
        return "exact" if _is_simplex(f) else "not_exact"

    def pred_constraint_wise_m1(f: StructuralFeatures) -> str:
        return "exact" if f.constraint_wise_separable else "not_exact"

    def pred_fixed_recourse_polytope(f: StructuralFeatures) -> str:
        return "exact" if (f.polytopal and f.fixed_recourse) else "not_exact"

    def pred_box_or_cube(f: StructuralFeatures) -> str:
        return "exact" if _is_axis_aligned_box(f) else "not_exact"

    candidates = {
        "simplex_only": pred_simplex_only,
        "constraint_wise_m1": pred_constraint_wise_m1,
        "fixed_recourse_polytope": pred_fixed_recourse_polytope,
        "box_or_cube_uncertainty": pred_box_or_cube,
    }
    evals: dict[str, Any] = {}
    all_falsified = True
    for name, fn in candidates.items():
        res = evaluate_conjecture(lambda case, _fn=fn: _fn(features[case.case_id]), cases=battery)
        evals[name] = {
            "survived": res["survived"],
            "mismatched_cases": [m["case_id"] for m in res["mismatches"]],
        }
        if res["survived"]:
            all_falsified = False

    # Note: T4 is a 1D interval [-1, 1] (both a 1-simplex and a 1-box), so `simplex_only` also
    # misclassifies T4 (expectation objective, not worst-case minimax) in addition to T1 and T6!
    return {
        "ok": battery_ok and all_falsified,
        "battery_passed": sum(1 for c in battery if c.passed),
        "battery_total": len(battery),
        "structural_checks": {
            cid: {
                "is_simplex": _is_simplex(f),
                "is_box": _is_axis_aligned_box(f),
                "polytopal_fixed_recourse": f.polytopal and f.fixed_recourse,
                "constraint_wise": f.constraint_wise_separable,
            }
            for cid, f in features.items()
        },
        "naive_candidates_falsified": evals,
    }


def check_simplex_exactness() -> dict[str, Any]:
    """Verify V_ADR == V_ARO on 6 fixed-recourse LP instances over Delta_1, Delta_2, Delta_3."""
    rng = random.Random(20261124)
    checked = 0
    for d in (1, 2, 3):
        verts = [tuple(Fraction(0) for _ in range(d))]
        for j in range(d):
            e = [Fraction(0)] * d
            e[j] = Fraction(1)
            verts.append(tuple(e))
        for _ in range(2):
            c_y = [Fraction(rng.randint(1, 4)), Fraction(rng.randint(1, 4))]
            B_rows = [[Fraction(-1), Fraction(-rng.randint(0, 2))],
                      [Fraction(-rng.randint(0, 2)), Fraction(-1)],
                      [Fraction(-1), Fraction(-1)]]
            h0 = [Fraction(rng.randint(1, 3)) for _ in range(3)]
            H_mat = [[Fraction(rng.randint(-1, 2)) for _ in range(d)] for _ in range(3)]

            def cons(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
                rows: list[tuple[list[Fraction], Fraction]] = [
                    ([Fraction(-1), Fraction(0)], Fraction(0)),
                    ([Fraction(0), Fraction(-1)], Fraction(0)),
                    ([Fraction(1), Fraction(0)], Fraction(20)),
                    ([Fraction(0), Fraction(1)], Fraction(20)),
                ]
                for i in range(3):
                    rhs_val = h0[i] + sum(H_mat[i][j] * v[j] for j in range(d))
                    rows.append((list(B_rows[i]), -rhs_val))
                return rows

            v_aro = _solve_vertex_aro(verts, 2, c_y, cons)
            v_adr = _solve_vertex_adr(verts, 2, c_y, cons)
            if v_aro != v_adr:
                return {"ok": False, "reason": f"Simplex gap at d={d}: {v_aro} vs {v_adr}"}
            checked += 1
    return {"ok": True, "checked_simplices": checked}


def _solve_1d_bridge_aro_adr(
    A: Fraction,
    B: Fraction,
    E: Fraction,
    x0: Fraction,
    umax: Fraction,
    rho: Fraction,
    r: int,
    q: int,
    H: list[Fraction],
    gmin: list[Fraction],
    gmax: list[Fraction],
    c: Fraction,
) -> tuple[Fraction, Fraction] | None:
    """Solve exact 1D BridgeFormalV2.Data corner ARO LP vs affine ADR LP (jointly over u_1 and u_2)."""
    r_pre = sum(abs((A ** (r - 1 - t)) * E) * rho for t in range(r))
    r_post = sum(abs((A ** (q - 1 - t)) * E) * rho for t in range(q))
    b_pre = [(A ** (r - 1 - t)) * B for t in range(r)]
    b_post = [(A ** (q - 1 - t)) * B for t in range(q)]
    aq = A ** q
    ar_x0 = (A ** r) * x0
    xi_corners = [-r_pre, r_pre] if r_pre > 0 else [Fraction(0)]

    n_c = len(xi_corners)
    n_vars = 1 + r + n_c * q
    A_ub, b_ub = [], []
    for t in range(r):
        for sgn in (Fraction(1), Fraction(-1)):
            row = [Fraction(0)] * n_vars
            row[1 + t] = sgn
            A_ub.append(row)
            b_ub.append(umax)
    for ci, xi in enumerate(xi_corners):
        off = 1 + r + ci * q
        for t in range(q):
            for sgn in (Fraction(1), Fraction(-1)):
                row = [Fraction(0)] * n_vars
                row[off + t] = sgn
                A_ub.append(row)
                b_ub.append(umax)
        base_x = aq * (ar_x0 + xi)
        for h_i, lo_i, hi_i in zip(H, gmin, gmax, strict=True):
            rad = abs(h_i) * r_post
            row_hi = [Fraction(0)] * n_vars
            for t in range(r):
                row_hi[1 + t] = h_i * aq * b_pre[t]
            for t in range(q):
                row_hi[off + t] = h_i * b_post[t]
            A_ub.append(row_hi)
            b_ub.append(hi_i - rad - h_i * base_x)
            A_ub.append([-v for v in row_hi])
            b_ub.append(-(lo_i + rad) + h_i * base_x)
        row_c = [Fraction(0)] * n_vars
        row_c[0] = Fraction(-1)
        for t in range(r):
            row_c[1 + t] = c * aq * b_pre[t]
        for t in range(q):
            row_c[off + t] = c * b_post[t]
        A_ub.append(row_c)
        b_ub.append(-(c * base_x + abs(c) * r_post))

    res_aro = solve_exact_lp([Fraction(1)] + [Fraction(0)] * (n_vars - 1), A_ub=A_ub, b_ub=b_ub, free_vars=list(range(n_vars)))
    if res_aro.status != "optimal" or res_aro.objective is None:
        return None

    n_vars2 = 1 + r + 2 * q
    A_ub2, b_ub2 = [], []
    for t in range(r):
        for sgn in (Fraction(1), Fraction(-1)):
            row = [Fraction(0)] * n_vars2
            row[1 + t] = sgn
            A_ub2.append(row)
            b_ub2.append(umax)
    for xi in xi_corners:
        for t in range(q):
            for sgn in (Fraction(1), Fraction(-1)):
                row = [Fraction(0)] * n_vars2
                row[1 + r + t] = sgn
                row[1 + r + q + t] = sgn * xi
                A_ub2.append(row)
                b_ub2.append(umax)
        base_x = aq * (ar_x0 + xi)
        for h_i, lo_i, hi_i in zip(H, gmin, gmax, strict=True):
            rad = abs(h_i) * r_post
            row_hi = [Fraction(0)] * n_vars2
            for t in range(r):
                row_hi[1 + t] = h_i * aq * b_pre[t]
            for t in range(q):
                row_hi[1 + r + t] = h_i * b_post[t]
                row_hi[1 + r + q + t] = h_i * b_post[t] * xi
            A_ub2.append(row_hi)
            b_ub2.append(hi_i - rad - h_i * base_x)
            A_ub2.append([-v for v in row_hi])
            b_ub2.append(-(lo_i + rad) + h_i * base_x)
        row_c = [Fraction(0)] * n_vars2
        row_c[0] = Fraction(-1)
        for t in range(r):
            row_c[1 + t] = c * aq * b_pre[t]
        for t in range(q):
            row_c[1 + r + t] = c * b_post[t]
            row_c[1 + r + q + t] = c * b_post[t] * xi
        A_ub2.append(row_c)
        b_ub2.append(-(c * base_x + abs(c) * r_post))

    res_adr = solve_exact_lp([Fraction(1)] + [Fraction(0)] * (n_vars2 - 1), A_ub=A_ub2, b_ub=b_ub2, free_vars=list(range(n_vars2)))
    if res_adr.status != "optimal" or res_adr.objective is None:
        return None
    return (res_aro.objective, res_adr.objective)


def check_bridge_1d_exactness() -> dict[str, Any]:
    """Verify V_ADR == V_ARO across 8 diverse 1D BridgeFormalV2.Data instances."""
    specs = [
        (Fraction(2), Fraction(1), Fraction(1), Fraction(0), Fraction(1), Fraction(1), 1, 1, [Fraction(1)], [Fraction(-2)], [Fraction(4)], Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(1), Fraction(0), Fraction(1), Fraction(1), 2, 2, [Fraction(1)], [Fraction(-2)], [Fraction(6)], Fraction(1)),
        (Fraction(1), Fraction(2), Fraction(1), Fraction(1), Fraction(1), Fraction(1), 3, 1, [Fraction(1), Fraction(-1)], [Fraction(-4), Fraction(-4)], [Fraction(6), Fraction(5)], Fraction(2)),
        (Fraction(1, 2), Fraction(1), Fraction(1), Fraction(-1), Fraction(2), Fraction(1), 2, 1, [Fraction(1), Fraction(2)], [Fraction(-5), Fraction(-10)], [Fraction(5), Fraction(10)], Fraction(-1)),
        (Fraction(-1), Fraction(1), Fraction(1), Fraction(1, 2), Fraction(2), Fraction(1), 2, 2, [Fraction(1), Fraction(1), Fraction(-2)], [Fraction(-6), Fraction(-4), Fraction(-12)], [Fraction(6), Fraction(8), Fraction(12)], Fraction(3)),
        (Fraction(3, 2), Fraction(2), Fraction(1, 2), Fraction(0), Fraction(2), Fraction(1), 1, 2, [Fraction(1)], [Fraction(-3)], [Fraction(7)], Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(1), Fraction(5), Fraction(1), Fraction(1), 2, 1, [Fraction(1)], [Fraction(-2)], [Fraction(2)], Fraction(1)),
        (Fraction(1), Fraction(1), Fraction(0), Fraction(1), Fraction(1), Fraction(1), 1, 1, [Fraction(1)], [Fraction(-1)], [Fraction(5)], Fraction(1)),
    ]
    values = []
    for idx, sp_args in enumerate(specs):
        ans = _solve_1d_bridge_aro_adr(*sp_args)
        if ans is None or ans[0] != ans[1]:
            return {"ok": False, "reason": f"1D Bridge mismatch on instance {idx}: {ans}"}
        values.append(str(ans[0]))
    return {"ok": True, "checked_1d_instances": len(specs), "exact_values": values}


def check_bridge_2d_strict_adr_gap() -> dict[str, Any]:
    """Verify minimal 2D BridgeFormalV2.Data strict ADR gap: V_ARO = 6 < V_ADR = 8."""
    verts = [(Fraction(a), Fraction(b)) for a in (-1, 1) for b in (-1, 1)]
    H = [(Fraction(1), Fraction(0)), (Fraction(0), Fraction(1))]
    t_gmin, t_gmax = [Fraction(1), Fraction(1)], [Fraction(3), Fraction(3)]
    c_vec = (Fraction(1), Fraction(1))
    cost_tight = Fraction(2)

    A_ub, b_ub = [], []
    A_ub.append([Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]); b_ub.append(Fraction(1))
    A_ub.append([Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)]); b_ub.append(Fraction(1))
    for idx, v in enumerate(verts):
        r1 = [Fraction(0)] * 6; r1[2 + idx] = Fraction(1); A_ub.append(r1); b_ub.append(Fraction(1))
        r2 = [Fraction(0)] * 6; r2[2 + idx] = Fraction(-1); A_ub.append(r2); b_ub.append(Fraction(1))
        for row, lo, hi in zip(H, t_gmin, t_gmax, strict=True):
            hv = row[0] * v[0] + row[1] * v[1]
            hb = row[0] + row[1]
            r_hi = [Fraction(0)] * 6; r_hi[1] = hb; r_hi[2 + idx] = hb
            A_ub.append(r_hi); b_ub.append(hi - hv)
            r_lo = [Fraction(0)] * 6; r_lo[1] = -hb; r_lo[2 + idx] = -hb
            A_ub.append(r_lo); b_ub.append(hv - lo)
        cv = c_vec[0] * v[0] + c_vec[1] * v[1]
        cb = c_vec[0] + c_vec[1]
        ep = [Fraction(-1), cb, Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
        ep[2 + idx] = cb
        A_ub.append(ep); b_ub.append(-(cv + cost_tight))
    res_aro = solve_exact_lp([Fraction(1)] + [Fraction(0)] * 5, A_ub=A_ub, b_ub=b_ub, free_vars=list(range(6)))

    A_ub2, b_ub2 = [], []
    A_ub2.append([Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(0)]); b_ub2.append(Fraction(1))
    A_ub2.append([Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0)]); b_ub2.append(Fraction(1))
    for v in verts:
        A_ub2.append([Fraction(0), Fraction(0), Fraction(1), v[0], v[1]]); b_ub2.append(Fraction(1))
        A_ub2.append([Fraction(0), Fraction(0), Fraction(-1), -v[0], -v[1]]); b_ub2.append(Fraction(1))
        for row, lo, hi in zip(H, t_gmin, t_gmax, strict=True):
            hv = row[0] * v[0] + row[1] * v[1]
            hb = row[0] + row[1]
            A_ub2.append([Fraction(0), hb, hb, hb * v[0], hb * v[1]]); b_ub2.append(hi - hv)
            A_ub2.append([Fraction(0), -hb, -hb, -hb * v[0], -hb * v[1]]); b_ub2.append(hv - lo)
        cv = c_vec[0] * v[0] + c_vec[1] * v[1]
        cb = c_vec[0] + c_vec[1]
        A_ub2.append([Fraction(-1), cb, cb, cb * v[0], cb * v[1]]); b_ub2.append(-(cv + cost_tight))
    res_adr = solve_exact_lp([Fraction(1)] + [Fraction(0)] * 4, A_ub=A_ub2, b_ub=b_ub2, free_vars=list(range(5)))

    grid = [Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)]
    grid_ok = True
    max_cost = Fraction(-100)
    for v0, v1 in itertools.product(grid, grid):
        u2 = max(-v0, -v1)
        x0_post = v0 + 1 + u2
        x1_post = v1 + 1 + u2
        cost = v0 + v1 + 2 * (1 + u2) + cost_tight
        if not (-1 <= u2 <= 1 and 1 <= x0_post <= 3 and 1 <= x1_post <= 3 and cost <= 6):
            grid_ok = False
        if cost > max_cost:
            max_cost = cost

    ok = (
        res_aro.status == "optimal"
        and res_adr.status == "optimal"
        and res_aro.objective == Fraction(6)
        and res_adr.objective == Fraction(8)
        and grid_ok
        and max_cost == Fraction(6)
    )
    return {
        "ok": ok,
        "v_aro": str(res_aro.objective),
        "v_adr": str(res_adr.objective),
        "strict_gap": str(res_adr.objective - res_aro.objective) if res_aro.objective and res_adr.objective else None,
        "witness_grid_points": len(grid) * len(grid),
        "witness_max_cost": str(max_cost),
    }


def main() -> None:
    r_bat = check_t1_t7_and_naive_candidates()
    r_sim = check_simplex_exactness()
    r_1d = check_bridge_1d_exactness()
    r_2d = check_bridge_2d_strict_adr_gap()
    all_ok = r_bat["ok"] and r_sim["ok"] and r_1d["ok"] and r_2d["ok"]
    out = {
        "survived": all_ok,
        "checked_points": (
            r_bat["battery_total"]
            + len(r_bat["naive_candidates_falsified"])
            + r_sim.get("checked_simplices", 0)
            + r_1d.get("checked_1d_instances", 0)
            + r_2d.get("witness_grid_points", 0)
        ),
        "t1_t7_and_naive_falsification": r_bat,
        "simplex_exactness_probe": r_sim,
        "bridge_1d_exactness_probe": r_1d,
        "bridge_2d_strict_adr_gap": r_2d,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
