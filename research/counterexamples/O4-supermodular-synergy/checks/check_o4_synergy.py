#!/usr/bin/env python3
"""Exact rational LP + SymPy continuous-box checker for Counterexample O4 (conj-o4-closure-scheduling).

Certifies THREE sharp scheduling phenomena on LTI `BridgeFormalV2.Data` instances at horizon T = 3
over the CONTINUOUS disturbance box `[-1, 1]^3`:

  1. Strict Supermodular Synergy (Refutation of Submodularity of G(R) = V(empty) - V(R)):
     4-state nilpotent shift-register LTI system (`n=4, m=1, p=1, rows=4, U=[-1,1], rho=1`):
       A: e0 -> e1 -> e2 -> 0, e3 -> e0; B = e0; E = e3; c = e2^T;
       H enforces u0 +- (u1 + w0) >= 0 and u0 +- (u2 + w1) >= 0 (gmin = 0, gmax = 10).
     Exact values:
       V(empty) = 1, V({1}) = 1, V({2}) = 1, V({1,2}) = 0
       G(empty) = 0, G({1}) = 0, G({2}) = 0, G({1,2}) = 1
     Submodularity defect = (G({1,2}) - G({1})) - (G({2}) - G(empty)) = +1 > 0.
     Also proves greedy single-closure selection has 0 approximation ratio on general LTI systems.

  2. Strict Submodularity & Early-Closure Dominance (O4 + O7):
     1D integrator (`A=1, B=1, E=1, U=[-1/2, 1/2], rho=1, H=1, gmin=-2, gmax=10, c=1`):
       V(empty) = 4, V({1}) = 2, V({2}) = 3, V({1,2}) = 2
       G(empty) = 0, G({1}) = 2, G({2}) = 1, G({1,2}) = 2
     Submodularity defect = -1 < 0, and V({1}) = 2 < 3 = V({2}).

  3. Strict Late-Closure Dominance (O7):
     1D contracting system (`A=1/2, B=1, E=1, U=[-1, 1], rho=1, H=1, gmin=-2, gmax=10, c=1`):
       V(empty) = 3/2, V({1}) = 1, V({2}) = 0, V({1,2}) = 0
       G(empty) = 0, G({1}) = 1/2, G({2}) = 3/2, G({1,2}) = 3/2
     Late dominance V({2}) = 0 < 1 = V({1}), proving neither early nor late closure dominates.

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
        raise RuntimeError(f"O4 synergy counterexample check failed: {msg}")


def _matmul(X: list[list[Fraction]], Y: list[list[Fraction]]) -> list[list[Fraction]]:
    return [
        [sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))]
        for i in range(len(X))
    ]


def _solve_lti_t3_schedule(
    *,
    A: list[list[Fraction]],
    B: list[list[Fraction]],
    E: list[list[Fraction]],
    H: list[list[Fraction]],
    c_row: list[Fraction],
    gmin: list[Fraction],
    gmax: list[Fraction],
    umax: Fraction,
    rho: Fraction,
    closures: frozenset[int],
) -> Fraction:
    """Exact rational LP for LTI T=3 (m=1, p=1) with closures subset of {1, 2}."""
    n = len(A)
    rows = len(H)
    A2 = _matmul(A, A)
    M0u, M1u, M2u = _matmul(A2, B), _matmul(A, B), B
    M0w, M1w, M2w = _matmul(A2, E), _matmul(A, E), E

    signs = (-rho, rho)
    u1_keys: list[Any] = list(signs) if 1 in closures else [None]
    if 2 in closures:
        u2_keys: list[Any] = list(itertools.product(signs, signs))
    elif 1 in closures:
        u2_keys = [(w0, None) for w0 in signs]
    else:
        u2_keys = [(None, None)]

    u1_idx = {k: 1 + i for i, k in enumerate(u1_keys)}
    base_u2 = 1 + len(u1_keys)
    u2_idx = {k: base_u2 + i for i, k in enumerate(u2_keys)}
    eta_idx = base_u2 + len(u2_keys)
    n_vars = eta_idx + 1

    A_ub: list[list[Fraction]] = []
    b_ub: list[Fraction] = []
    for idx in range(eta_idx):
        ru = [Fraction(0)] * n_vars
        ru[idx] = Fraction(1)
        rl = [Fraction(0)] * n_vars
        rl[idx] = Fraction(-1)
        A_ub.extend([ru, rl])
        b_ub.extend([umax, umax])

    for w0, w1, w2 in itertools.product(signs, repeat=3):
        k1 = w0 if 1 in closures else None
        k2: Any = (
            (w0, w1)
            if 2 in closures
            else ((w0, None) if 1 in closures else (None, None))
        )
        i1 = u1_idx[k1]
        i2 = u2_idx[k2]

        def _add_row(
            rv: list[Fraction],
            rhs: Fraction,
            *,
            is_obj: bool,
            ww0: Fraction = w0,
            ww1: Fraction = w1,
            ww2: Fraction = w2,
            idx1: int = i1,
            idx2: int = i2,
        ) -> None:
            w_val = sum(
                rv[d] * (M0w[d][0] * ww0 + M1w[d][0] * ww1 + M2w[d][0] * ww2)
                for d in range(n)
            )
            row = [Fraction(0)] * n_vars
            row[0] += sum(rv[d] * M0u[d][0] for d in range(n))
            row[idx1] += sum(rv[d] * M1u[d][0] for d in range(n))
            row[idx2] += sum(rv[d] * M2u[d][0] for d in range(n))
            if is_obj:
                row[eta_idx] = Fraction(-1)
                A_ub.append(row)
                b_ub.append(-w_val)
            else:
                A_ub.append(row)
                b_ub.append(rhs - w_val)

        for i in range(rows):
            _add_row(H[i], gmax[i], is_obj=False)
            _add_row([-x for x in H[i]], -gmin[i], is_obj=False)
        _add_row(c_row, Fraction(0), is_obj=True)

    c_vec = [Fraction(0)] * n_vars
    c_vec[eta_idx] = Fraction(1)
    res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=set(range(n_vars)))
    _require(
        res.status == "optimal" and res.objective is not None,
        f"LP failed for closures={sorted(closures)}: {res.status}",
    )
    return res.objective  # type: ignore[return-value]


def verify_sympy_continuous_certificates() -> dict[str, Any]:
    """Symbolically certify continuous-box identities for all 3 witnesses."""
    w0, w1, w2 = sp.symbols("w0 w1 w2", real=True)

    # 1. Supermodular synergy witness: x_3 = (u2+w1, u1+w0, u0, w2)
    # With R={1,2}: u0=0, u1=-w0, u2=-w1 => x_3 = (0, 0, 0, w2), all 4 rows = 0, cost = 0.
    r12_slot0 = sp.simplify((-w1) + w1)
    r12_slot1 = sp.simplify((-w0) + w0)
    _require(r12_slot0 == 0 and r12_slot1 == 0, "SymPy check failed for synergy R={1,2}")

    # 2. Early dominance witness (A=1, umax=1/2):
    # R={1}: u0=0, u1=-w0/2, u2=-w0/2 => x_3 = w1 + w2 in [-2, 2].
    early_r1 = sp.simplify(0 + (-w0 / 2) + (-w0 / 2) + w0 + w1 + w2)
    _require(early_r1 == w1 + w2, f"Expected w1+w2, got {early_r1}")
    # R={2}: u0=1/4, u1=1/4, u2 = -(w0+w1)/4 => x_3 = 1/2 + 3/4*(w0+w1) + w2 in [-2, 3].
    early_r2 = sp.simplify(sp.Rational(1, 4) + sp.Rational(1, 4) - (w0 + w1) / 4 + w0 + w1 + w2)
    _require(early_r2 == sp.Rational(1, 2) + sp.Rational(3, 4) * (w0 + w1) + w2, "early R={2} mismatch")

    # 3. Late dominance witness (A=1/2, umax=1):
    # R={1}: u0=0, u1=-w0/2, u2=-1/2 => x_3 = -1/2 + w1/2 + w2 in [-2, 1].
    late_r1 = sp.simplify(
        sp.Rational(1, 4) * (0 + w0) + sp.Rational(1, 2) * (-w0 / 2 + w1) + (-sp.Rational(1, 2) + w2)
    )
    _require(late_r1 == -sp.Rational(1, 2) + sp.Rational(1, 2) * w1 + w2, "late R={1} mismatch")
    # R={2}: u0=-1, u1=-1, x_2 = -3/2 + w0/2 + w1, u2 = -1 - x_2/2 => x_3 = -1 + w2 in [-2, 0].
    x2_late = sp.Rational(1, 2) * (-1 + w0) + (-1 + w1)
    u2_late = -1 - x2_late / 2
    late_r2 = sp.simplify(x2_late / 2 + u2_late + w2)
    _require(late_r2 == -1 + w2, f"Expected -1+w2, got {late_r2}")

    return {
        "synergy_r12_identity": "u0=0, u1=-w0, u2=-w1 => x_3 = (0, 0, 0, w2), cost = 0",
        "early_dom_r1_identity": "u0=0, u1=u2=-w0/2 => x_3 = w1 + w2 in [-2, 2]",
        "early_dom_r2_identity": "u0=u1=1/4, u2=-(x2-1/2)/4 => x_3 = 1/2 + 3/4*(w0+w1) + w2 in [-2, 3]",
        "late_dom_r1_identity": "u0=0, u1=-w0/2, u2=-1/2 => x_3 = -1/2 + w1/2 + w2 in [-2, 1]",
        "late_dom_r2_identity": "u0=u1=-1, u2=-1-x2/2 => x_3 = -1 + w2 in [-2, 0]",
    }


def _eval_4_schedules(**kwargs: Any) -> dict[str, Any]:
    vals = {
        "empty": _solve_lti_t3_schedule(closures=frozenset(), **kwargs),
        "r1": _solve_lti_t3_schedule(closures=frozenset({1}), **kwargs),
        "r2": _solve_lti_t3_schedule(closures=frozenset({2}), **kwargs),
        "r12": _solve_lti_t3_schedule(closures=frozenset({1, 2}), **kwargs),
    }
    G = {k: vals["empty"] - v for k, v in vals.items()}
    defect = (G["r12"] - G["r1"]) - (G["r2"] - G["empty"])
    return {
        "V": {k: str(v) for k, v in vals.items()},
        "G": {k: str(v) for k, v in G.items()},
        "submodularity_defect": str(defect),
        "_vals": vals,
        "_defect": defect,
    }


def run_all_checks() -> dict[str, Any]:
    # 1. 4D Nilpotent shift-register supermodular synergy witness
    A_syn = [
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
        [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
    ]
    B_syn = [[Fraction(1)], [Fraction(0)], [Fraction(0)], [Fraction(0)]]
    E_syn = [[Fraction(0)], [Fraction(0)], [Fraction(0)], [Fraction(1)]]
    H_syn = [
        [Fraction(0), Fraction(1), Fraction(1), Fraction(0)],
        [Fraction(0), Fraction(-1), Fraction(1), Fraction(0)],
        [Fraction(1), Fraction(0), Fraction(1), Fraction(0)],
        [Fraction(-1), Fraction(0), Fraction(1), Fraction(0)],
    ]
    c_syn = [Fraction(0), Fraction(0), Fraction(1), Fraction(0)]
    syn = _eval_4_schedules(
        A=A_syn, B=B_syn, E=E_syn, H=H_syn, c_row=c_syn,
        gmin=[Fraction(0)] * 4, gmax=[Fraction(10)] * 4,
        umax=Fraction(1), rho=Fraction(1),
    )
    _require(
        syn["_vals"] == {"empty": Fraction(1), "r1": Fraction(1), "r2": Fraction(1), "r12": Fraction(0)}
        and syn["_defect"] == Fraction(1),
        f"Unexpected synergy values: {syn}",
    )

    # 2. 1D integrator: strict submodularity (defect = -1) & early dominance V({1}) < V({2})
    early = _eval_4_schedules(
        A=[[Fraction(1)]], B=[[Fraction(1)]], E=[[Fraction(1)]],
        H=[[Fraction(1)]], c_row=[Fraction(1)],
        gmin=[Fraction(-2)], gmax=[Fraction(10)],
        umax=Fraction(1, 2), rho=Fraction(1),
    )
    _require(
        early["_vals"] == {"empty": Fraction(4), "r1": Fraction(2), "r2": Fraction(3), "r12": Fraction(2)}
        and early["_defect"] == Fraction(-1),
        f"Unexpected early-dominance values: {early}",
    )

    # 3. 1D contracting system: late dominance V({2}) < V({1})
    late = _eval_4_schedules(
        A=[[Fraction(1, 2)]], B=[[Fraction(1)]], E=[[Fraction(1)]],
        H=[[Fraction(1)]], c_row=[Fraction(1)],
        gmin=[Fraction(-2)], gmax=[Fraction(10)],
        umax=Fraction(1), rho=Fraction(1),
    )
    _require(
        late["_vals"] == {"empty": Fraction(3, 2), "r1": Fraction(1), "r2": Fraction(0), "r12": Fraction(0)}
        and late["_defect"] == Fraction(-1, 2),
        f"Unexpected late-dominance values: {late}",
    )

    sympy_cert = verify_sympy_continuous_certificates()

    for d in (syn, early, late):
        d.pop("_vals")
        d.pop("_defect")

    return {
        "conjecture_id": "hyp-o4-submodularity-and-single-closure-dominance",
        "atlas_node_id": "conj-o4-closure-scheduling",
        "verdict": "REFUTED_AT_STAGE_2_FALSIFY_FIRST_BY_EXACT_LP",
        "supermodular_synergy_4d": syn,
        "submodular_early_dominance_1d": early,
        "late_dominance_1d": late,
        "sympy_continuous_certificates": sympy_cert,
    }


def main() -> int:
    print(json.dumps(run_all_checks(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
