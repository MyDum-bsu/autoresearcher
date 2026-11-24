#!/usr/bin/env python3
"""Stage 2 (FALSIFY_FIRST) exact rational + SymPy verification for G2 (gen-nonbox-conic-uncertainty).

Every single claim below is directly executed and checked (zero unexecuted claims):
  1. `l1` cross-polytope support: exact rational LP (`solve_exact_lp`) vs `r * ||g||_inf` (4 vectors).
  2. `l2` SOC ball support: exact symbolic Cauchy-Schwarz identity
     `(g1^2 + g2^2)*(w1^2 + w2^2) - (g1*w1 + g2*w2)^2 == (g1*w2 - g2*w1)^2 >= 0` + exact
     gradient attainment witnesses across 4 rational vectors (SymPy).
  3. Multi-stage (q=2, p=2, n=2) additivity computed directly from dynamics `(A, E, row)`:
     explicit attaining blocks verified for ALL THREE families (`box` F3, `l1`, `l2` SOC).
  4. Compact 2x2 spectrahedra & Slater-failure dual unattainment check (SymPy):
     - Slater-valid 2x2 PSD set `M(w) = [[1+w1, w2], [w2, 1-w1]] >= 0`: `M(0) = I > 0`
       and `det M(w) = 1 - w1^2 - w2^2`.
     - Slater-failing compact 2x2 PSD set `[[w1, w2], [w2, 0]] >= 0, 0 <= w1 <= 1`:
       primal max of `w2` is `0` (attained), while dual matrix `[[lam, -1/2], [-1/2, mu]] >= 0`
       has `det = 0` at `mu = 1/(4*lam)` for every `lam > 0` (dual inf = `0`), yet `det = -1/4 < 0`
       at `lam = 0` for every finite `mu` (dual infimum unattained without Slater regularity).
  5. Finite sample check on 11 rational stereographic circle points (full non-polyhedrality
     for all `k : Nat` is machine-checked in Lean 4 `l2_ball_not_finset_conv_2d`).
"""
from __future__ import annotations

import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

import sympy as sp

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from verification.oracles.exact_lp import solve_exact_lp


def check_l1_cross_polytope_exact_lp() -> dict[str, Any]:
    """Verify max_{||w||_1 <= r} g^T w == r * ||g||_inf via exact rational LP across 4 vectors."""
    r = Fraction(3, 2)
    test_vectors = [
        [Fraction(2), Fraction(-5)],
        [Fraction(-7, 3), Fraction(4, 3)],
        [Fraction(0), Fraction(0)],
        [Fraction(3), Fraction(3)],
    ]
    checked = 0
    for g in test_vectors:
        c_lp = [-g[0], g[0], -g[1], g[1]]
        res = solve_exact_lp(c_lp, A_ub=[[1, 1, 1, 1]], b_ub=[r])
        if res.status != "optimal" or res.objective is None:
            return {"ok": False, "reason": f"l1 LP failed: {res.status}"}
        lp_max = -res.objective
        closed = r * max(abs(g[0]), abs(g[1]))
        if lp_max != closed:
            return {"ok": False, "reason": f"l1 mismatch {lp_max} != {closed}"}
        checked += 1
    return {"ok": True, "checked": checked, "r": str(r)}


def check_l2_soc_ball_sympy() -> dict[str, Any]:
    """Verify symbolic Cauchy-Schwarz identity + exact attainment witnesses for SOC ball."""
    g1s, g2s, w1s, w2s = sp.symbols("g1 g2 w1 w2", real=True)
    cs_diff = sp.expand(
        (g1s**2 + g2s**2) * (w1s**2 + w2s**2)
        - (g1s * w1s + g2s * w2s) ** 2
        - (g1s * w2s - g2s * w1s) ** 2
    )
    if cs_diff != 0:
        return {"ok": False, "reason": f"Cauchy-Schwarz identity failed: {cs_diff}"}

    r = sp.Rational(5, 2)
    test_vectors = [
        (sp.Rational(3), sp.Rational(-4)),
        (sp.Rational(1), sp.Rational(2)),
        (sp.Rational(0), sp.Rational(0)),
        (sp.Rational(-5), sp.Rational(12)),
    ]
    checked = 0
    for g1, g2 in test_vectors:
        norm_g = sp.sqrt(g1**2 + g2**2)
        expected = sp.simplify(r * norm_g)
        if norm_g == 0:
            w1, w2 = sp.Integer(0), sp.Integer(0)
        else:
            w1, w2 = r * g1 / norm_g, r * g2 / norm_g
        if sp.simplify(w1**2 + w2**2 - r**2) > 0:
            return {"ok": False, "reason": "SOC witness outside ball"}
        if sp.simplify(g1 * w1 + g2 * w2 - expected) != 0:
            return {"ok": False, "reason": "SOC attainment mismatch"}
        checked += 1
    return {"ok": True, "checked": checked, "r": str(r), "symbolic_cs_identity_zero": True}


def check_multistage_additivity_from_dynamics() -> dict[str, Any]:
    """Compute g_t = (row^T A^{q-1-t} E)^T from (A, E, row) and verify box, l1, l2 witnesses."""
    A = sp.Matrix([[1, 1], [0, 1]])
    E = sp.Matrix([[1, 0], [0, 1]])
    row = sp.Matrix([[1, 2]])
    q = 2
    dirs = [(row * (A ** (q - 1 - t)) * E) for t in range(q)]
    g0 = (dirs[0][0], dirs[0][1])
    g1 = (dirs[1][0], dirs[1][1])

    # 1. Box (rho = 1/2): explicit attaining block + feasibility check
    rho = sp.Rational(1, 2)
    w_box = [tuple(rho if v >= 0 else -rho for v in g) for g in (g0, g1)]
    if not all(abs(v) <= rho for w in w_box for v in w):
        return {"ok": False, "reason": "multistage box witness infeasible"}
    box_expected = rho * sum(abs(v) for g in (g0, g1) for v in g)
    box_attained = sum(g[i] * w[i] for g, w in zip((g0, g1), w_box, strict=True) for i in range(2))
    if sp.simplify(box_attained - box_expected) != 0:
        return {"ok": False, "reason": "multistage box attainment mismatch"}

    # 2. l1 cross-polytope (r = 1): explicit attaining block + feasibility check
    w_l1 = []
    for g in (g0, g1):
        idx = 0 if abs(g[0]) >= abs(g[1]) else 1
        sgn = sp.Integer(1) if g[idx] >= 0 else sp.Integer(-1)
        w_l1.append((sgn, sp.Integer(0)) if idx == 0 else (sp.Integer(0), sgn))
    if not all(abs(w[0]) + abs(w[1]) <= 1 for w in w_l1):
        return {"ok": False, "reason": "multistage l1 witness infeasible"}
    l1_expected = sum(max(abs(g[0]), abs(g[1])) for g in (g0, g1))
    l1_attained = sum(g[i] * w[i] for g, w in zip((g0, g1), w_l1, strict=True) for i in range(2))
    if sp.simplify(l1_attained - l1_expected) != 0:
        return {"ok": False, "reason": "multistage l1 attainment mismatch"}

    # 3. l2 SOC ball (r = 1): explicit attaining block + feasibility check
    w_l2 = []
    l2_expected = sp.Integer(0)
    for g in (g0, g1):
        ng = sp.sqrt(g[0] ** 2 + g[1] ** 2)
        l2_expected += ng
        w_l2.append((g[0] / ng, g[1] / ng))
    if not all(sp.simplify(w[0] ** 2 + w[1] ** 2 - 1) <= 0 for w in w_l2):
        return {"ok": False, "reason": "multistage l2 witness infeasible"}
    l2_attained = sp.simplify(
        sum(g[i] * w[i] for g, w in zip((g0, g1), w_l2, strict=True) for i in range(2))
    )
    if sp.simplify(l2_attained - l2_expected) != 0:
        return {"ok": False, "reason": "multistage l2 attainment mismatch"}

    return {
        "ok": True,
        "computed_g0": [str(g0[0]), str(g0[1])],
        "computed_g1": [str(g1[0]), str(g1[1])],
        "box_f3_support": str(box_expected),
        "l1_support": str(l1_expected),
        "l2_soc_support": str(l2_expected),
        "all_three_witnesses_attained": True,
    }


def check_slater_boundary_and_circle_samples() -> dict[str, Any]:
    """Verify Slater-valid 2x2 spectrahedron, Slater-failing unattained dual, and 11 circle pts."""
    w1, w2 = sp.symbols("w1 w2", real=True)
    M_slater = sp.Matrix([[1 + w1, w2], [w2, 1 - w1]])
    M_at_zero = M_slater.subs({w1: 0, w2: 0})
    det_slater = sp.simplify(M_slater.det())
    if M_at_zero != sp.eye(2) or sp.simplify(det_slater - (1 - w1**2 - w2**2)) != 0:
        return {"ok": False, "reason": "Slater spectrahedron check failed"}

    # Primal Slater-failing 2x2 spectrahedron M_fail(w) = [[w1, w2], [w2, 0]] >= 0, 0 <= w1 <= 1
    M_fail = sp.Matrix([[w1, w2], [w2, 0]])
    det_fail = sp.simplify(M_fail.det())
    if sp.simplify(det_fail + w2**2) != 0:
        return {"ok": False, "reason": "Primal Slater-failure determinant check failed"}
    # PSD requires det_fail = -w2^2 >= 0 => w2 = 0; verify primal witness (0, 0) is PSD and gives w2 = 0
    if M_fail.subs({w1: 0, w2: 0}) != sp.zeros(2, 2):
        return {"ok": False, "reason": "Primal witness (0, 0) failed PSD check"}

    lam = sp.Symbol("lam", positive=True)
    mu = sp.Symbol("mu", real=True)
    D_mat = sp.Matrix([[lam, sp.Rational(-1, 2)], [sp.Rational(-1, 2), mu]])
    D_pos = D_mat.subs(mu, 1 / (4 * lam))
    det_pos = sp.simplify(D_pos.det())
    trace_pos_gt0 = bool(sp.simplify(D_pos.trace()).is_positive)
    det_zero = sp.simplify(sp.Matrix([[0, sp.Rational(-1, 2)], [sp.Rational(-1, 2), mu]]).det())
    if det_pos != 0 or not trace_pos_gt0 or det_zero != sp.Rational(-1, 4):
        return {"ok": False, "reason": "Slater-failure dual attainment check failed"}

    pts = [
        (Fraction(k * k - 1, k * k + 1), Fraction(2 * k, k * k + 1))
        for k in range(11)
    ]
    if len(set(pts)) != 11 or not all(x * x + y * y == 1 for x, y in pts):
        return {"ok": False, "reason": "Stereographic sample check failed"}

    return {
        "ok": True,
        "slater_spectrahedron_det": str(det_slater),
        "slater_interior_M0_is_I": True,
        "primal_slater_fail_det": str(det_fail),
        "primal_witness_0_0_psd": True,
        "slater_failure_dual_det_at_pos_lam": str(det_pos),
        "slater_failure_dual_trace_positive": trace_pos_gt0,
        "slater_failure_dual_det_at_lam0": str(det_zero),
        "stereographic_sample_points_checked": len(pts),
    }


def main() -> None:
    r_l1 = check_l1_cross_polytope_exact_lp()
    r_l2 = check_l2_soc_ball_sympy()
    r_ms = check_multistage_additivity_from_dynamics()
    r_sl = check_slater_boundary_and_circle_samples()
    all_ok = all(r["ok"] for r in (r_l1, r_l2, r_ms, r_sl))
    out = {
        "survived": all_ok,
        "checked_points": r_l1.get("checked", 0) + r_l2.get("checked", 0) + 11,
        "l1_cross_polytope": r_l1,
        "l2_soc_ball": r_l2,
        "multistage_additivity": r_ms,
        "slater_and_circle_samples": r_sl,
    }
    print(json.dumps(out, indent=2))
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
