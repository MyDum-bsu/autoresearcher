#!/usr/bin/env python3
"""Exact rational LP + SymPy continuous-box checker for Counterexample O2/O5 (lifted / separable ADR).

Certifies THREE sharp O2/O5 lifting & uncertainty-geometry phenomena with zero floating-point error:

  1. O2 Linear Multiplicative Scaling & Segregated-Lifting Exactness on the d-D l1 Cross-Polytope B_1^d:
     For d = 2, 3, 4, 5 on the Chen-Zhang fixed-recourse ARO over B_1^d = {sum |xi_i| <= 1}:
       - V_ARO(d)     = 1
       - V_ADR(d)     = d   (exact multiplicative ratio = d = Omega(d))
       - V_SegLADR(d) = 1   (coordinate-wise |xi_i|-lifted ADR collapses the gap to 0)

  2. Refutation of H-O2-1 (Coordinate-Separable / Axis-Aligned Liftings Fail on 2D Box & Bridge):
     On BOTH frozen BridgeFormalV2.Data witnesses (`bridgeAdrGapData` rank-1 and
     `bridgeFullRankShearData` full-rank unimodular B = [[1,1],[0,1]]):
       - Even ARBITRARY coordinate-separable policies y(v0, v1) = f0(v0) + f1(v1) (subsuming all
         coordinate-wise |v_i|-lifted, spline, and axis-aligned piecewise-affine rules) satisfy
         the exact square barycentric syzygy y(-1,1) + y(1,-1) = y(-1,-1) + y(1,1), giving
         ZERO improvement over standard ADR:
           * bridgeAdrGapData:        V_ARO = 6 < 8 = V_ADR = V_SegLADR = V_Separable
           * bridgeFullRankShearData: V_ARO = 5 < 6 = V_ADR = V_SegLADR = V_Separable

  3. O2/O5 Positive Resolution (Single-Feature Diagonal-Hinge Lifting Restores Exactness on [-1, 1]^2):
     Adding the SINGLE scalar interaction feature phi_diag(v) = |v0 - v1| yields exactness:
       * bridgeAdrGapData:        V_DiagLADR = 6 = V_ARO (gap = 0)
       * bridgeFullRankShearData: V_DiagLADR = 5 = V_ARO (gap = 0)
     Certified symbolically on the full continuous box [-1, 1]^2 via SymPy Kuhn-triangulation
     identity (zero residual on both triangles v0 <= v1 and v1 <= v0).

Zero `assert` statements — behaves identically under `python3 -B` and `python3 -B -O`.
"""
from __future__ import annotations

import itertools
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
        raise RuntimeError(f"O2 separable-lifting counterexample check failed: {msg}")


def _solve_l1_cross_polytope(d: int) -> dict[str, Any]:
    """Exact rational LP on d-D l1 cross-polytope B_1^d: ARO vs ADR vs Segregated (|xi|) LADR."""
    # Vertices of B_1^d: 0 and +/- e_i (total 2d + 1 points)
    pts: list[tuple[Fraction, ...]] = [tuple(Fraction(0) for _ in range(d))]
    for i in range(d):
        for sgn in (Fraction(1), Fraction(-1)):
            v = [Fraction(0)] * d
            v[i] = sgn
            pts.append(tuple(v))

    def _solve(mode: str) -> Fraction:
        # mode in {"aro", "adr", "seg_ladr"}
        # For each coordinate i in 0..d-1, y_i(xi) is parameterized by:
        #   aro:      one var per point -> len(pts) * d vars
        #   adr:      y0_i + sum_j Y_{ij} xi_j -> (1 + d) * d vars
        #   seg_ladr: y0_i + sum_j Y_{ij} xi_j + sum_j Z_{ij} |xi_j| -> (1 + 2d) * d vars
        if mode == "aro":
            stride = len(pts)
        elif mode == "adr":
            stride = 1 + d
        elif mode == "seg_ladr":
            stride = 1 + 2 * d
        else:
            raise ValueError(mode)
        eta_idx = d * stride
        n_vars = eta_idx + 1
        A_ub: list[list[Fraction]] = []
        b_ub: list[Fraction] = []

        def _add_y_coeff(row: list[Fraction], i: int, k_pt: int, xi: tuple[Fraction, ...], mult: Fraction) -> None:
            off = i * stride
            if mode == "aro":
                row[off + k_pt] += mult
            elif mode == "adr":
                row[off] += mult
                for j in range(d):
                    row[off + 1 + j] += mult * xi[j]
            else:
                row[off] += mult
                for j in range(d):
                    row[off + 1 + j] += mult * xi[j]
                    row[off + 1 + d + j] += mult * abs(xi[j])

        for k_pt, xi in enumerate(pts):
            # Constraints: -y_i(xi) <= -xi_i and -y_i(xi) <= xi_i
            for i in range(d):
                for rhs in (-xi[i], xi[i]):
                    row = [Fraction(0)] * n_vars
                    _add_y_coeff(row, i, k_pt, xi, Fraction(-1))
                    A_ub.append(row)
                    b_ub.append(rhs)
            # Cost: sum_i y_i(xi) - eta <= 0
            row = [Fraction(0)] * n_vars
            for i in range(d):
                _add_y_coeff(row, i, k_pt, xi, Fraction(1))
            row[eta_idx] = Fraction(-1)
            A_ub.append(row)
            b_ub.append(Fraction(0))

        c_vec = [Fraction(0)] * n_vars
        c_vec[eta_idx] = Fraction(1)
        res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=list(range(n_vars)))
        _require(res.status == "optimal" and res.objective is not None, f"B_1^{d} {mode} failed: {res.status}")
        return res.objective

    v_aro = _solve("aro")
    v_adr = _solve("adr")
    v_seg = _solve("seg_ladr")
    _require(v_aro == Fraction(1), f"Expected V_ARO=1 on B_1^{d}, got {v_aro}")
    _require(v_adr == Fraction(d), f"Expected V_ADR={d} on B_1^{d}, got {v_adr}")
    _require(v_seg == Fraction(1), f"Expected V_SegLADR=1 on B_1^{d}, got {v_seg}")
    return {
        "d": d,
        "V_ARO": str(v_aro),
        "V_ADR": str(v_adr),
        "V_SegLADR": str(v_seg),
        "adr_ratio": str(v_adr / v_aro),
        "seg_ladr_gap": str(v_seg - v_aro),
    }


def _solve_2d_bridge_modes(
    *,
    B: list[list[Fraction]],
    H: list[list[Fraction]],
    c: list[Fraction],
    gmin: list[Fraction],
    gmax: list[Fraction],
    umax: Fraction,
    rho: Fraction,
) -> dict[str, Fraction]:
    """Exact rational LP for 2D single-closure bridge across 5 policy classes:
    aro, adr, seg_ladr (affine in v0,v1,|v0|,|v1|), separable (f0(v0)+f1(v1)), diag_ladr (affine in v0,v1,|v0-v1|).
    """
    m = len(B[0])
    rows = len(H)
    corners = list(itertools.product((-rho, rho), repeat=2))

    def future_support(rv: list[Fraction]) -> Fraction:
        return rho * (abs(rv[0]) + abs(rv[1]))

    def _features(mode: str, v0: Fraction, v1: Fraction) -> list[Fraction]:
        if mode == "adr":
            return [Fraction(1), v0, v1]
        if mode == "seg_ladr":
            return [Fraction(1), v0, v1, abs(v0), abs(v1)]
        if mode == "separable":
            # f0(-rho), f0(+rho), f1(-rho), f1(+rho)
            return [
                Fraction(1) if v0 == -rho else Fraction(0),
                Fraction(1) if v0 == rho else Fraction(0),
                Fraction(1) if v1 == -rho else Fraction(0),
                Fraction(1) if v1 == rho else Fraction(0),
            ]
        if mode == "diag_ladr":
            return [Fraction(1), v0, v1, abs(v0 - v1)]
        raise ValueError(mode)

    def _solve(mode: str) -> Fraction:
        if mode == "aro":
            stride = len(corners)
        else:
            stride = len(_features(mode, rho, rho))
        eta_idx = m + m * stride
        n_vars = eta_idx + 1
        A_ub: list[list[Fraction]] = []
        b_ub: list[Fraction] = []

        # Stage-1 box bounds: |u1_j| <= umax
        for j in range(m):
            for sgn in (Fraction(1), Fraction(-1)):
                r = [Fraction(0)] * n_vars
                r[j] = sgn
                A_ub.append(r)
                b_ub.append(umax)

        for k_idx, (v0, v1) in enumerate(corners):
            feats = None if mode == "aro" else _features(mode, v0, v1)
            # Stage-2 box bounds: |u2_j(v)| <= umax
            for j in range(m):
                for sgn in (Fraction(1), Fraction(-1)):
                    r = [Fraction(0)] * n_vars
                    if mode == "aro":
                        r[m + j * stride + k_idx] = sgn
                    else:
                        if feats is None:
                            raise RuntimeError("missing feature vector")
                        for f_i, f_val in enumerate(feats):
                            r[m + j * stride + f_i] = sgn * f_val
                    A_ub.append(r)
                    b_ub.append(umax)

            def _add_row(rv: list[Fraction], lim: Fraction, *, is_obj: bool) -> None:
                const = rv[0] * v0 + rv[1] * v1 + future_support(rv)
                r = [Fraction(0)] * n_vars
                for j in range(m):
                    coeff = rv[0] * B[0][j] + rv[1] * B[1][j]
                    r[j] += coeff
                    if mode == "aro":
                        r[m + j * stride + k_idx] += coeff
                    else:
                        if feats is None:
                            raise RuntimeError("missing feature vector")
                        for f_i, f_val in enumerate(feats):
                            r[m + j * stride + f_i] += coeff * f_val
                if is_obj:
                    r[eta_idx] = Fraction(-1)
                    A_ub.append(r)
                    b_ub.append(-const)
                else:
                    A_ub.append(r)
                    b_ub.append(lim - const)

            for i in range(rows):
                _add_row([H[i][0], H[i][1]], gmax[i], is_obj=False)
                _add_row([-H[i][0], -H[i][1]], -gmin[i], is_obj=False)
            _add_row(c, Fraction(0), is_obj=True)

        c_vec = [Fraction(0)] * n_vars
        c_vec[eta_idx] = Fraction(1)
        res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=list(range(n_vars)))
        _require(res.status == "optimal" and res.objective is not None, f"2D bridge {mode} failed: {res.status}")
        return res.objective

    return {mode: _solve(mode) for mode in ("aro", "adr", "seg_ladr", "separable", "diag_ladr")}


def _verify_sympy_certificates() -> dict[str, Any]:
    """Symbolically certify (1) separable square syzygy and (2) diagonal-hinge Kuhn triangulation."""
    v0, v1 = sp.symbols("v0 v1", real=True)
    y_mm, y_mp, y_pm, y_pp = sp.symbols("y_mm y_mp y_pm y_pp", real=True)
    f0_m, f0_p, f1_m, f1_p, y0_s = sp.symbols("f0_m f0_p f1_m f1_p y0_s", real=True)

    # 1. Arbitrary separable rule y(v0, v1) = y0 + f0(v0) + f1(v1) obeys square syzygy identically
    sep_mp = y0_s + f0_m + f1_p
    sep_pm = y0_s + f0_p + f1_m
    sep_mm = y0_s + f0_m + f1_m
    sep_pp = y0_s + f0_p + f1_p
    sep_syzygy = sp.simplify((sep_mp + sep_pm) - (sep_mm + sep_pp))
    _require(sep_syzygy == 0, f"Separable square syzygy residual nonzero: {sep_syzygy}")

    # 2. Single-feature diagonal-hinge lifting reproduces exact Kuhn triangulation on BOTH triangles
    y0 = (y_mm + y_pp) / 2
    Y0 = (y_pp - y_mm + y_pm - y_mp) / 4
    Y1 = (y_pp - y_mm + y_mp - y_pm) / 4
    Z = (y_mp + y_pm - y_mm - y_pp) / 4

    # Triangle 1: v0 <= v1 => |v0 - v1| = v1 - v0
    diag_t1 = sp.simplify(y0 + Y0 * v0 + Y1 * v1 + Z * (v1 - v0))
    kuhn_t1 = sp.simplify(((1 - v1) / 2) * y_mm + ((v1 - v0) / 2) * y_mp + ((1 + v0) / 2) * y_pp)
    res_t1 = sp.simplify(diag_t1 - kuhn_t1)
    _require(res_t1 == 0, f"Triangle 1 (v0 <= v1) residual nonzero: {res_t1}")

    # Triangle 2: v1 <= v0 => |v0 - v1| = v0 - v1
    diag_t2 = sp.simplify(y0 + Y0 * v0 + Y1 * v1 + Z * (v0 - v1))
    kuhn_t2 = sp.simplify(((1 - v0) / 2) * y_mm + ((v0 - v1) / 2) * y_pm + ((1 + v1) / 2) * y_pp)
    res_t2 = sp.simplify(diag_t2 - kuhn_t2)
    _require(res_t2 == 0, f"Triangle 2 (v1 <= v0) residual nonzero: {res_t2}")

    return {
        "separable_square_syzygy_residual": str(sep_syzygy),
        "kuhn_triangle1_residual": str(res_t1),
        "kuhn_triangle2_residual": str(res_t2),
        "syzygy_defect_coefficient_Z": "(y_mp + y_pm - y_mm - y_pp)/4",
    }


def main() -> None:
    cross_polytope_results = [_solve_l1_cross_polytope(d) for d in (2, 3, 4, 5)]

    rank1_vals = _solve_2d_bridge_modes(
        B=[[Fraction(1)], [Fraction(1)]],
        H=[[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]],
        c=[Fraction(1), Fraction(1)],
        gmin=[Fraction(0), Fraction(0)],
        gmax=[Fraction(4), Fraction(4)],
        umax=Fraction(1),
        rho=Fraction(1),
    )
    _require(rank1_vals["aro"] == Fraction(6), f"rank1 aro: {rank1_vals}")
    _require(rank1_vals["adr"] == Fraction(8), f"rank1 adr: {rank1_vals}")
    _require(rank1_vals["seg_ladr"] == Fraction(8), f"rank1 seg_ladr: {rank1_vals}")
    _require(rank1_vals["separable"] == Fraction(8), f"rank1 separable: {rank1_vals}")
    _require(rank1_vals["diag_ladr"] == Fraction(6), f"rank1 diag_ladr: {rank1_vals}")

    shear_vals = _solve_2d_bridge_modes(
        B=[[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]],
        H=[[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]],
        c=[Fraction(1), Fraction(1)],
        gmin=[Fraction(0), Fraction(-1)],
        gmax=[Fraction(4), Fraction(3)],
        umax=Fraction(1, 2),
        rho=Fraction(1),
    )
    _require(shear_vals["aro"] == Fraction(5), f"shear aro: {shear_vals}")
    _require(shear_vals["adr"] == Fraction(6), f"shear adr: {shear_vals}")
    _require(shear_vals["seg_ladr"] == Fraction(6), f"shear seg_ladr: {shear_vals}")
    _require(shear_vals["separable"] == Fraction(6), f"shear separable: {shear_vals}")
    _require(shear_vals["diag_ladr"] == Fraction(5), f"shear diag_ladr: {shear_vals}")

    sympy_cert = _verify_sympy_certificates()

    out = {
        "counterexample_id": "O2-separable-lifting-gap",
        "target_open_node_id": "conj-o1-adr-exactness-char",
        "hypothesis_refuted": "H-O2-1",
        "verdict": "REFUTED",
        "l1_cross_polytope_scaling": cross_polytope_results,
        "bridge_rank1_lifting_comparison": {k: str(v) for k, v in rank1_vals.items()},
        "bridge_shear_lifting_comparison": {k: str(v) for k, v in shear_vals.items()},
        "sympy_continuous_box_certificate": sympy_cert,
    }
    results_path = pathlib.Path(__file__).resolve().parents[1] / "results.json"
    results_path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
