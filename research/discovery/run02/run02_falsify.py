#!/usr/bin/env python3
"""R12 Run-02 Stage-2 Falsify-First Frontier Runner (O4, G1, G2, O1, O8).

Executes:
  1. Journal Editor Significance Gate on all 5 Run-02 manifest candidates.
  2. Exact rational (`fractions.Fraction`) LP probes via `verification.oracles.exact_lp`:
       - O4 (`run02-o4-submodularity`): exact V(empty), V({1}), V({2}), V({1,2}) across
         unconstrained terminal (rows=0) and two tightly constrained terminal box regimes.
       - G1 (`run02-g1-markov-sufficiency`): exact k=2 Markov vs history LP on the SAME
         control objective comparing injective 2D shift-register state x_2=(w_0,w_1)
         against non-injective projection s_2=w_0+w_1.
       - G2 (`run02-g2-l1-vertex-lp`): exact 2D and 3D l1 cross-polytope Minkowski support
         verification and Vertex-LP V_ARO vs V_ADR separation (2D exact vs 3D gap 1/2).
       - O1 (`run02-o1-fullrank-b-2d`): full T1-T7 battery (7/7) plus exact 2D Bridge
         rank-1 B (tight vs relaxed box) vs full-rank B=I_2 (diagonal & coupled H).
       - O8 (`run02-o8-gap-vanishing-regime`): exact parametric sweep over post-closure
         authority u1_max comparing minimax V({1}), prefix-maximin V_prefix_mm, and
         full-trajectory maximin V_full_mm.

Zero `assert` statements — behaves identically under `python3 -B` and `python3 -B -O`.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import pathlib
import sys
from fractions import Fraction
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.atlas.semantic_index import ATLAS_JSON_DEFAULT, SemanticAtlasIndex  # noqa: E402
from research.discovery.significance_gate import (  # noqa: E402
    SignificanceCandidate,
    evaluate_significance,
)
from verification.falsifiers.battery_t1_t7 import run_battery  # noqa: E402
from verification.oracles.exact_lp import solve_exact_lp  # noqa: E402

MANIFEST_DEFAULT = pathlib.Path(__file__).resolve().parent / "manifest.json"


class Run02FalsifyError(RuntimeError):
    """Raised when a Run-02 falsification probe fails an internal consistency check."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise Run02FalsifyError(msg)


def _solve_1d_t3_schedule(
    *,
    closures: frozenset[int],
    umax: Fraction,
    rho: Fraction,
    gmin: Fraction | None,
    gmax: Fraction | None,
    c_sign: Fraction = Fraction(1),
) -> Fraction:
    """Exact rational LP for 1D integrator x_{t+1} = x_t + u_t + w_t on T=3 (closures <= {1, 2}).

    If `gmin` and `gmax` are None, terminal state is unconstrained (`rows = 0`).
    """
    signs = (-rho, rho)
    u1_keys = list(signs) if 1 in closures else [None]
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
        if 2 in closures:
            k2: Any = (w0, w1)
        elif 1 in closures:
            k2 = (w0, None)
        else:
            k2 = (None, None)
        i1 = u1_idx[k1]
        i2 = u2_idx[k2]
        w_sum = w0 + w1 + w2

        if gmax is not None:
            r_hi = [Fraction(0)] * n_vars
            r_hi[0] = Fraction(1)
            r_hi[i1] = Fraction(1)
            r_hi[i2] = Fraction(1)
            A_ub.append(r_hi)
            b_ub.append(gmax - w_sum)

        if gmin is not None:
            r_lo = [Fraction(0)] * n_vars
            r_lo[0] = Fraction(-1)
            r_lo[i1] = Fraction(-1)
            r_lo[i2] = Fraction(-1)
            A_ub.append(r_lo)
            b_ub.append(-gmin + w_sum)

        r_obj = [Fraction(0)] * n_vars
        r_obj[0] = c_sign
        r_obj[i1] = c_sign
        r_obj[i2] = c_sign
        r_obj[eta_idx] = Fraction(-1)
        A_ub.append(r_obj)
        b_ub.append(-c_sign * w_sum)

    c_vec = [Fraction(0)] * n_vars
    c_vec[eta_idx] = Fraction(1)
    res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=set(range(n_vars)))
    _expect(res.status == "optimal" and res.objective is not None, f"LP failed: {res.status}")
    return res.objective  # type: ignore[return-value]


def probe_o4_submodularity() -> dict[str, Any]:
    """Probe O4: test submodularity of G(R) = V(empty) - V(R) on unconstrained & constrained T=3."""

    def _eval_regime(
        umax: Fraction, gmin: Fraction | None, gmax: Fraction | None
    ) -> dict[str, Any]:
        vals = {
            "empty": _solve_1d_t3_schedule(
                closures=frozenset(), umax=umax, rho=Fraction(1), gmin=gmin, gmax=gmax
            ),
            "r1": _solve_1d_t3_schedule(
                closures=frozenset({1}), umax=umax, rho=Fraction(1), gmin=gmin, gmax=gmax
            ),
            "r2": _solve_1d_t3_schedule(
                closures=frozenset({2}), umax=umax, rho=Fraction(1), gmin=gmin, gmax=gmax
            ),
            "r12": _solve_1d_t3_schedule(
                closures=frozenset({1, 2}), umax=umax, rho=Fraction(1), gmin=gmin, gmax=gmax
            ),
        }
        g_vals = {k: vals["empty"] - v for k, v in vals.items()}
        defect = (g_vals["r12"] - g_vals["r1"]) - (g_vals["r2"] - g_vals["empty"])
        return {
            "V": {k: str(v) for k, v in vals.items()},
            "G": {k: str(v) for k, v in g_vals.items()},
            "submodularity_defect": str(defect),
            "_defect_frac": defect,
        }

    reg_uncon = _eval_regime(Fraction(1), None, None)
    reg_a = _eval_regime(Fraction(1), Fraction(-2), Fraction(6))
    reg_b = _eval_regime(Fraction(1, 2), Fraction(-5, 2), Fraction(10))

    submodular_all = (
        reg_uncon["_defect_frac"] <= 0 and reg_a["_defect_frac"] <= 0 and reg_b["_defect_frac"] <= 0
    )
    for reg in (reg_uncon, reg_a, reg_b):
        reg.pop("_defect_frac")

    return {
        "candidate_id": "run02-o4-submodularity",
        "target_open_node_id": "conj-o4-closure-scheduling",
        "verdict": "SURVIVED_STAGE2" if submodular_all else "FALSIFIED_SUPERMODULAR",
        "instance_unconstrained": reg_uncon,
        "instance_a": reg_a,
        "instance_b": reg_b,
    }


def probe_g1_markov_sufficiency() -> dict[str, Any]:
    """Probe G1: exact k=2 Markov vs history LP on the SAME control objective.

    Compares two observation maps at t=2 for identical dynamics/objective `min max |u_2 - w_0|`:
      1. Injective 2D shift-register state `x_2 = (w_0, w_1)` -> `V_markov == V_history == 0`.
      2. Non-injective 1D projection `s_2 = w_0 + w_1` -> `V_markov = 1 > 0 = V_history`.
    """
    signs = (Fraction(-1), Fraction(1))

    def _solve_k2_observation(*, obs_mode: str) -> Fraction:
        # obs_mode in {"history", "markov_2d_injective", "markov_1d_merged"}
        if obs_mode == "history":
            u2_keys: list[Any] = list(itertools.product(signs, signs))
        elif obs_mode == "markov_2d_injective":
            # 2D shift-register state x_2 = (x_{2,0}, x_{2,1}) = (w_0, w_1)
            u2_keys = [(int(w0), int(w1)) for w0, w1 in itertools.product(signs, signs)]
        else:
            # Merged scalar state s_2 = w_0 + w_1 in {-2, 0, 2}
            u2_keys = [-2, 0, 2]

        u2_idx = {k: i for i, k in enumerate(u2_keys)}
        eta_idx = len(u2_keys)
        n_vars = eta_idx + 1
        A_ub: list[list[Fraction]] = []
        b_ub: list[Fraction] = []
        for idx in range(eta_idx):
            ru = [Fraction(0)] * n_vars
            ru[idx] = Fraction(1)
            rl = [Fraction(0)] * n_vars
            rl[idx] = Fraction(-1)
            A_ub.extend([ru, rl])
            b_ub.extend([Fraction(1), Fraction(1)])

        for w0, w1 in itertools.product(signs, repeat=2):
            if obs_mode == "history":
                key: Any = (w0, w1)
            elif obs_mode == "markov_2d_injective":
                key = (int(w0), int(w1))
            else:
                key = int(w0 + w1)
            i2 = u2_idx[key]
            # |u_2(key) - w_0| <= eta
            r1 = [Fraction(0)] * n_vars
            r1[i2] = Fraction(1)
            r1[eta_idx] = Fraction(-1)
            A_ub.append(r1)
            b_ub.append(w0)

            r2 = [Fraction(0)] * n_vars
            r2[i2] = Fraction(-1)
            r2[eta_idx] = Fraction(-1)
            A_ub.append(r2)
            b_ub.append(-w0)

        c_vec = [Fraction(0)] * n_vars
        c_vec[eta_idx] = Fraction(1)
        res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=set(range(n_vars)))
        _expect(
            res.status == "optimal" and res.objective is not None, f"G1 LP failed: {res.status}"
        )
        return res.objective  # type: ignore[return-value]

    v_history = _solve_k2_observation(obs_mode="history")
    v_markov_2d_inj = _solve_k2_observation(obs_mode="markov_2d_injective")
    v_markov_1d_merged = _solve_k2_observation(obs_mode="markov_1d_merged")

    _expect(v_markov_2d_inj == v_history == Fraction(0), "Injective 2D Markov must equal history")
    _expect(
        v_markov_1d_merged > v_history, "Merged 1D state must strictly separate Markov > history"
    )

    return {
        "candidate_id": "run02-g1-markov-sufficiency",
        "target_open_node_id": "gen-multistage-k-closures",
        "verdict": "SURVIVED_STAGE2",
        "injective_regime": {
            "V_markov": str(v_markov_2d_inj),
            "V_history": str(v_history),
            "gap": str(v_markov_2d_inj - v_history),
        },
        "merged_state_regime": {
            "V_markov": str(v_markov_1d_merged),
            "V_history": str(v_history),
            "gap": str(v_markov_1d_merged - v_history),
        },
    }


def probe_g2_l1_vertex_lp() -> dict[str, Any]:
    """Probe G2: 2D & 3D l1 cross-polytope Minkowski support + Vertex-LP V_ARO vs V_ADR."""
    rho = Fraction(1)

    def _l1_vertices(dim: int) -> list[tuple[Fraction, ...]]:
        verts: list[tuple[Fraction, ...]] = []
        for d in range(dim):
            for sgn in (rho, -rho):
                v = [Fraction(0)] * dim
                v[d] = sgn
                verts.append(tuple(v))
        return verts

    # Verify exact support attainment h_{W}(r) = rho * ||r||_inf in BOTH 2D and 3D
    test_rows_2d = [
        (Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(2)),
        (Fraction(-3), Fraction(1)),
        (Fraction(2), Fraction(-2)),
        (Fraction(-1, 2), Fraction(-3, 4)),
    ]
    verts_2d = _l1_vertices(2)
    for row in test_rows_2d:
        v_max = max(sum(r * c for r, c in zip(row, v, strict=True)) for v in verts_2d)
        _expect(v_max == rho * max(abs(x) for x in row), f"2D l1 support mismatch for {row}")

    test_rows_3d = [
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(-2), Fraction(3)),
        (Fraction(-5), Fraction(2), Fraction(-1)),
        (Fraction(1, 3), Fraction(-2, 3), Fraction(1, 2)),
        (Fraction(-2), Fraction(-2), Fraction(2)),
    ]
    verts_3d = _l1_vertices(3)
    for row in test_rows_3d:
        v_max = max(sum(r * c for r, c in zip(row, v, strict=True)) for v in verts_3d)
        _expect(v_max == rho * max(abs(x) for x in row), f"3D l1 support mismatch for {row}")

    def _solve_l1_pos_sum(dim: int) -> tuple[Fraction, Fraction]:
        verts = _l1_vertices(dim)
        n_aro = len(verts) * dim + 1
        eta_a = n_aro - 1
        A_aro: list[list[Fraction]] = []
        b_aro: list[Fraction] = []
        for k, v in enumerate(verts):
            ro = [Fraction(0)] * n_aro
            for i in range(dim):
                yi = k * dim + i
                for rhs in (v[i], Fraction(0)):
                    r = [Fraction(0)] * n_aro
                    r[yi] = Fraction(-1)
                    A_aro.append(r)
                    b_aro.append(-rhs)
                ro[yi] = Fraction(1)
            ro[eta_a] = Fraction(-1)
            A_aro.append(ro)
            b_aro.append(Fraction(0))
        c_aro = [Fraction(0)] * n_aro
        c_aro[eta_a] = Fraction(1)
        res_aro = solve_exact_lp(c_aro, A_ub=A_aro, b_ub=b_aro, free_vars=set(range(n_aro)))
        _expect(res_aro.status == "optimal" and res_aro.objective is not None, "G2 ARO LP failed")

        stride = dim + 1
        n_adr = dim * stride + 1
        eta_d = n_adr - 1
        A_adr: list[list[Fraction]] = []
        b_adr: list[Fraction] = []
        for v in verts:
            ro = [Fraction(0)] * n_adr
            for i in range(dim):
                off = i * stride
                for rhs in (v[i], Fraction(0)):
                    r = [Fraction(0)] * n_adr
                    r[off] = Fraction(-1)
                    for j in range(dim):
                        r[off + 1 + j] = -v[j]
                    A_adr.append(r)
                    b_adr.append(-rhs)
                ro[off] = Fraction(1)
                for j in range(dim):
                    ro[off + 1 + j] = v[j]
            ro[eta_d] = Fraction(-1)
            A_adr.append(ro)
            b_adr.append(Fraction(0))
        c_adr = [Fraction(0)] * n_adr
        c_adr[eta_d] = Fraction(1)
        res_adr = solve_exact_lp(c_adr, A_ub=A_adr, b_ub=b_adr, free_vars=set(range(n_adr)))
        _expect(res_adr.status == "optimal" and res_adr.objective is not None, "G2 ADR LP failed")
        return res_aro.objective, res_adr.objective  # type: ignore[return-value]

    aro_2d, adr_2d = _solve_l1_pos_sum(2)
    aro_3d, adr_3d = _solve_l1_pos_sum(3)
    _expect(adr_3d > aro_3d, "3D l1 cross-polytope must exhibit strict ADR gap")
    return {
        "candidate_id": "run02-g2-l1-vertex-lp",
        "target_open_node_id": "gen-nonbox-conic-uncertainty",
        "verdict": "SURVIVED_STAGE2",
        "l1_support_rows_verified_2d": len(test_rows_2d),
        "l1_support_rows_verified_3d": len(test_rows_3d),
        "dim2_l1_rotated_square": {
            "V_ARO": str(aro_2d),
            "V_ADR": str(adr_2d),
            "gap": str(adr_2d - aro_2d),
        },
        "dim3_l1_octahedron": {
            "V_ARO": str(aro_3d),
            "V_ADR": str(adr_3d),
            "gap": str(adr_3d - aro_3d),
        },
    }


def _solve_2d_bridge_aro_vs_adr(
    *,
    B: list[list[Fraction]],
    H: list[list[Fraction]],
    c: list[Fraction],
    gmin: list[Fraction],
    gmax: list[Fraction],
    umax: Fraction,
    rho: Fraction,
) -> tuple[Fraction, Fraction]:
    """Solve exact 2D single-closure (r=1, q=1, A=I_2, E=I_2, x0=0) V_ARO and V_ADR."""
    m = len(B[0])
    rows = len(H)
    corners = list(itertools.product((-rho, rho), repeat=2))

    def future_support(row_vec: list[Fraction]) -> Fraction:
        return rho * (abs(row_vec[0]) + abs(row_vec[1]))

    def _solve(affine: bool) -> Fraction:
        n_u2 = (3 * m) if affine else (len(corners) * m)
        eta_idx = m + n_u2
        n_vars = eta_idx + 1
        A_ub: list[list[Fraction]] = []
        b_ub: list[Fraction] = []

        for j in range(m):
            for sgn in (Fraction(1), Fraction(-1)):
                r = [Fraction(0)] * n_vars
                r[j] = sgn
                A_ub.append(r)
                b_ub.append(umax)

        for k, (v0, v1) in enumerate(corners):
            for j in range(m):
                for sgn in (Fraction(1), Fraction(-1)):
                    r = [Fraction(0)] * n_vars
                    if affine:
                        off = m + 3 * j
                        r[off] = sgn
                        r[off + 1] = sgn * v0
                        r[off + 2] = sgn * v1
                    else:
                        r[m + k * m + j] = sgn
                    A_ub.append(r)
                    b_ub.append(umax)

            def _add_row_constraint(
                rv: list[Fraction],
                lim: Fraction,
                *,
                is_obj: bool = False,
                k_idx: int = k,
                vv0: Fraction = v0,
                vv1: Fraction = v1,
            ) -> None:
                sup = future_support(rv)
                const = rv[0] * vv0 + rv[1] * vv1 + sup
                r = [Fraction(0)] * n_vars
                for j in range(m):
                    coeff = rv[0] * B[0][j] + rv[1] * B[1][j]
                    r[j] += coeff
                    if affine:
                        off = m + 3 * j
                        r[off] += coeff
                        r[off + 1] += coeff * vv0
                        r[off + 2] += coeff * vv1
                    else:
                        r[m + k_idx * m + j] += coeff
                if is_obj:
                    r[eta_idx] = Fraction(-1)
                    A_ub.append(r)
                    b_ub.append(-const)
                else:
                    A_ub.append(r)
                    b_ub.append(lim - const)

            for i in range(rows):
                _add_row_constraint(H[i], gmax[i], is_obj=False)
                _add_row_constraint([-H[i][0], -H[i][1]], -gmin[i], is_obj=False)
            _add_row_constraint(c, Fraction(0), is_obj=True)

        c_vec = [Fraction(0)] * n_vars
        c_vec[eta_idx] = Fraction(1)
        res = solve_exact_lp(c_vec, A_ub=A_ub, b_ub=b_ub, free_vars=set(range(n_vars)))
        _expect(
            res.status == "optimal" and res.objective is not None,
            f"2D Bridge LP failed: {res.status}",
        )
        return res.objective  # type: ignore[return-value]

    return _solve(affine=False), _solve(affine=True)


def probe_o1_fullrank_b_2d() -> dict[str, Any]:
    """Probe O1: T1-T7 battery + 2D Bridge rank-1 B (tight vs relaxed) vs full-rank B=I_2."""
    battery = run_battery()
    _expect(len(battery) == 7 and all(r.passed for r in battery), "T1-T7 battery failed")

    I2 = [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
    B_rank1 = [[Fraction(1)], [Fraction(1)]]
    c = [Fraction(1), Fraction(1)]
    gmin_tight = [Fraction(0), Fraction(0)]
    gmax_tight = [Fraction(4), Fraction(4)]
    gmin_relaxed = [Fraction(-10), Fraction(-10)]
    gmax_relaxed = [Fraction(10), Fraction(10)]

    aro_r1_tight, adr_r1_tight = _solve_2d_bridge_aro_vs_adr(
        B=B_rank1, H=I2, c=c, gmin=gmin_tight, gmax=gmax_tight, umax=Fraction(1), rho=Fraction(1)
    )
    aro_r1_rel, adr_r1_rel = _solve_2d_bridge_aro_vs_adr(
        B=B_rank1,
        H=I2,
        c=c,
        gmin=gmin_relaxed,
        gmax=gmax_relaxed,
        umax=Fraction(1),
        rho=Fraction(1),
    )
    aro_fr_diag, adr_fr_diag = _solve_2d_bridge_aro_vs_adr(
        B=I2, H=I2, c=c, gmin=gmin_tight, gmax=gmax_tight, umax=Fraction(1), rho=Fraction(1)
    )
    H_coupled = [[Fraction(1), Fraction(1)], [Fraction(1), Fraction(-1)]]
    aro_fr_cpl, adr_fr_cpl = _solve_2d_bridge_aro_vs_adr(
        B=I2,
        H=H_coupled,
        c=[Fraction(1), Fraction(0)],
        gmin=[Fraction(-2), Fraction(-2)],
        gmax=[Fraction(4), Fraction(4)],
        umax=Fraction(1),
        rho=Fraction(1),
    )
    _expect(aro_r1_tight < adr_r1_tight, "Rank-1 B on tight box must show strict ADR gap")
    _expect(aro_r1_rel == adr_r1_rel, "Rank-1 B on relaxed box should restore exactness")
    return {
        "candidate_id": "run02-o1-fullrank-b-2d",
        "target_open_node_id": "conj-o1-adr-exactness-char",
        "verdict": "SURVIVED_STAGE2" if (aro_fr_diag == adr_fr_diag) else "FALSIFIED",
        "t1_t7_battery_passed": len(battery),
        "rank1_B_diag_H": {
            "V_ARO": str(aro_r1_tight),
            "V_ADR": str(adr_r1_tight),
            "gap": str(adr_r1_tight - aro_r1_tight),
        },
        "rank1_B_relaxed_H": {
            "V_ARO": str(aro_r1_rel),
            "V_ADR": str(adr_r1_rel),
            "gap": str(adr_r1_rel - aro_r1_rel),
        },
        "fullrank_B_diag_H": {
            "V_ARO": str(aro_fr_diag),
            "V_ADR": str(adr_fr_diag),
            "gap": str(adr_fr_diag - aro_fr_diag),
        },
        "fullrank_B_coupled_H": {
            "V_ARO": str(aro_fr_cpl),
            "V_ADR": str(adr_fr_cpl),
            "gap": str(adr_fr_cpl - aro_fr_cpl),
        },
    }


def probe_o8_gap_vanishing() -> dict[str, Any]:
    """Probe O8: sweep u1_max comparing minimax V({1}), prefix-maximin, and full maximin."""
    # 1D system r=1, q=1, x_2 = u0 + u1 + w0 + w1, w0,w1 in [-1,1],
    # u0 in [-1,1], u1 in [-u1_max, u1_max], objective: min max |x_2|.
    rho = Fraction(1)
    u0_max = Fraction(1)
    sweep: list[dict[str, str]] = []
    for u1_max in (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3, 2)):
        # 1. Minimax V({1}) = min_{u0} max_{w0} min_{u1} max_{w1} |u0 + u1 + w0 + w1|
        A_ub: list[list[Fraction]] = [
            [Fraction(1), Fraction(0), Fraction(0), Fraction(0)],
            [Fraction(-1), Fraction(0), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(-1), Fraction(0), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(1), Fraction(0)],
            [Fraction(0), Fraction(0), Fraction(-1), Fraction(0)],
        ]
        b_ub: list[Fraction] = [u0_max, u0_max, u1_max, u1_max, u1_max, u1_max]
        for k, w0 in enumerate((-rho, rho)):
            u1_i = 1 + k
            r_pos = [Fraction(1), Fraction(0), Fraction(0), Fraction(-1)]
            r_pos[u1_i] = Fraction(1)
            A_ub.append(r_pos)
            b_ub.append(-(w0 + rho))

            r_neg = [Fraction(-1), Fraction(0), Fraction(0), Fraction(-1)]
            r_neg[u1_i] = Fraction(-1)
            A_ub.append(r_neg)
            b_ub.append(w0 - rho)

        res_mmx = solve_exact_lp(
            [Fraction(0), Fraction(0), Fraction(0), Fraction(1)],
            A_ub=A_ub,
            b_ub=b_ub,
            free_vars={0, 1, 2, 3},
        )
        _expect(
            res_mmx.status == "optimal" and res_mmx.objective is not None,
            "O8 minimax LP failed",
        )
        v_minimax = res_mmx.objective

        # 2. Prefix-maximin V_prefix_mm = max_{w0} min_{u0, u1} max_{w1} |u0 + u1 + w0 + w1|
        prefix_vals: list[Fraction] = []
        for w0 in (-rho, rho):
            A_s = [
                [Fraction(1), Fraction(0), Fraction(0)],
                [Fraction(-1), Fraction(0), Fraction(0)],
                [Fraction(0), Fraction(1), Fraction(0)],
                [Fraction(0), Fraction(-1), Fraction(0)],
                [Fraction(1), Fraction(1), Fraction(-1)],
                [Fraction(-1), Fraction(-1), Fraction(-1)],
            ]
            b_s = [u0_max, u0_max, u1_max, u1_max, -(w0 + rho), w0 - rho]
            res_s = solve_exact_lp(
                [Fraction(0), Fraction(0), Fraction(1)],
                A_ub=A_s,
                b_ub=b_s,
                free_vars={0, 1, 2},
            )
            _expect(
                res_s.status == "optimal" and res_s.objective is not None,
                "O8 prefix-maximin LP failed",
            )
            prefix_vals.append(res_s.objective)
        v_prefix_mm = max(prefix_vals)

        # 3. Full-trajectory maximin V_full_mm = max_{w0, w1} min_{u0, u1} |u0 + u1 + w0 + w1|
        full_vals: list[Fraction] = []
        for w0, w1 in itertools.product((-rho, rho), repeat=2):
            A_f = [
                [Fraction(1), Fraction(0), Fraction(0)],
                [Fraction(-1), Fraction(0), Fraction(0)],
                [Fraction(0), Fraction(1), Fraction(0)],
                [Fraction(0), Fraction(-1), Fraction(0)],
                [Fraction(1), Fraction(1), Fraction(-1)],
                [Fraction(-1), Fraction(-1), Fraction(-1)],
            ]
            b_f = [u0_max, u0_max, u1_max, u1_max, -(w0 + w1), (w0 + w1)]
            res_f = solve_exact_lp(
                [Fraction(0), Fraction(0), Fraction(1)],
                A_ub=A_f,
                b_ub=b_f,
                free_vars={0, 1, 2},
            )
            _expect(
                res_f.status == "optimal" and res_f.objective is not None,
                "O8 full-maximin LP failed",
            )
            full_vals.append(res_f.objective)
        v_full_mm = max(full_vals)

        sweep.append(
            {
                "u1_max": str(u1_max),
                "V_minimax": str(v_minimax),
                "V_prefix_mm": str(v_prefix_mm),
                "prefix_gap": str(v_minimax - v_prefix_mm),
                "V_full_mm": str(v_full_mm),
                "full_gap": str(v_minimax - v_full_mm),
            }
        )

    _expect(
        [r["prefix_gap"] for r in sweep] == ["1", "1/2", "0", "0"]
        and [r["full_gap"] for r in sweep] == ["1", "1", "1", "1"],
        f"Unexpected O8 dichotomy sweep: {sweep}",
    )
    return {
        "candidate_id": "run02-o8-gap-vanishing-regime",
        "target_open_node_id": "conj-o8-quantifier-gap",
        "verdict": "SURVIVED_STAGE2",
        "prefix_gap_law": "V({1}) - V_prefix_mm = max(0, rho - u1_max)",
        "full_gap_law": "V({1}) - V_full_mm = rho = 1 (irreducible post-closure w_1)",
        "u1_max_sweep": sweep,
    }


_PROBE_REGISTRY: dict[str, tuple[str, str, Any]] = {
    "run02-o4-submodularity": (
        "conj-o4-closure-scheduling",
        "97b7c11d5bc0fbe4667109d3470b8d917c868eccabef0be5695798e7ea8e835d",
        probe_o4_submodularity,
    ),
    "run02-g1-markov-sufficiency": (
        "gen-multistage-k-closures",
        "7b3ab673152ac6f760dad4aa48ef3320d1a1ae9856f84bc51f5e4aabc3dd8bf6",
        probe_g1_markov_sufficiency,
    ),
    "run02-g2-l1-vertex-lp": (
        "gen-nonbox-conic-uncertainty",
        "e8ea305ffbdb82284fba274e3be66a88abc32974bd87cea4ce17a03c077e0812",
        probe_g2_l1_vertex_lp,
    ),
    "run02-o1-fullrank-b-2d": (
        "conj-o1-adr-exactness-char",
        "a14f107f2ce3748f662c80379bcafe45f424e60b5213a7aeae38e871e1ca4944",
        probe_o1_fullrank_b_2d,
    ),
    "run02-o8-gap-vanishing-regime": (
        "conj-o8-quantifier-gap",
        "46c5c314e93a3eaa3f738f70ca4cc5017b6262927c2b2b67060754fd69f991d8",
        probe_o8_gap_vanishing,
    ),
}


def _candidate_claim_sha256(raw_c: dict[str, Any]) -> str:
    """Canonical SHA-256 binding manifest claim prose, prediction, and expected_checks to probe."""
    fields = (
        "candidate_id",
        "target_open_node_id",
        "title",
        "statement",
        "falsifiable_prediction",
        "expected_checks",
    )
    payload = {k: raw_c.get(k) for k in fields}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _verify_expected_checks(
    candidate_id: str, result: dict[str, Any], expected: dict[str, Any]
) -> None:
    """Verify exact rational probe output against manifest `expected_checks` (fail closed)."""
    _expect(
        isinstance(expected, dict) and len(expected) > 0,
        f"Candidate {candidate_id!r} missing non-empty 'expected_checks' in manifest",
    )
    if candidate_id == "run02-o4-submodularity":
        actual = {
            "unconstrained_defect": result["instance_unconstrained"]["submodularity_defect"],
            "instance_a_defect": result["instance_a"]["submodularity_defect"],
            "instance_b_defect": result["instance_b"]["submodularity_defect"],
        }
    elif candidate_id == "run02-g1-markov-sufficiency":
        actual = {
            "injective_gap": result["injective_regime"]["gap"],
            "merged_gap": result["merged_state_regime"]["gap"],
        }
    elif candidate_id == "run02-g2-l1-vertex-lp":
        actual = {
            "dim2_gap": result["dim2_l1_rotated_square"]["gap"],
            "dim3_gap": result["dim3_l1_octahedron"]["gap"],
        }
    elif candidate_id == "run02-o1-fullrank-b-2d":
        actual = {
            "rank1_tight_gap": result["rank1_B_diag_H"]["gap"],
            "rank1_relaxed_gap": result["rank1_B_relaxed_H"]["gap"],
            "fullrank_diag_gap": result["fullrank_B_diag_H"]["gap"],
        }
    elif candidate_id == "run02-o8-gap-vanishing-regime":
        actual = {
            "prefix_gaps": [r["prefix_gap"] for r in result["u1_max_sweep"]],
            "full_gaps": [r["full_gap"] for r in result["u1_max_sweep"]],
        }
    else:
        raise Run02FalsifyError(f"Unsupported candidate_id for expected_checks: {candidate_id!r}")

    _expect(
        set(expected.keys()) == set(actual.keys()),
        f"Manifest expected_checks key mismatch for {candidate_id!r}: "
        f"expected keys {sorted(actual.keys())}, got {sorted(expected.keys())}",
    )
    for key, exp_val in expected.items():
        _expect(
            actual[key] == exp_val,
            f"Manifest prediction FALSIFIED for {candidate_id!r}.{key}: "
            f"expected {exp_val!r}, computed {actual[key]!r}",
        )


def run_all(
    manifest_path: pathlib.Path = MANIFEST_DEFAULT,
    atlas_path: pathlib.Path = ATLAS_JSON_DEFAULT,
) -> dict[str, Any]:
    """Run Significance Gate + bound exact rational Stage-2 Falsify-First probes from manifest."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    raw_candidates = manifest.get("candidates")
    _expect(
        isinstance(raw_candidates, list) and len(raw_candidates) > 0,
        "Manifest must contain a non-empty 'candidates' list",
    )
    idx = SemanticAtlasIndex(atlas_path=atlas_path, backend="offline_tfidf")

    seen_ids: set[str] = set()
    parsed_pairs: list[tuple[SignificanceCandidate, dict[str, Any]]] = []
    for raw_c in raw_candidates:
        cand = SignificanceCandidate.from_dict(raw_c)
        _expect(cand.candidate_id not in seen_ids, f"Duplicate candidate_id: {cand.candidate_id}")
        seen_ids.add(cand.candidate_id)
        _expect(
            cand.candidate_id in _PROBE_REGISTRY,
            f"Manifest candidate {cand.candidate_id!r} has no registered Stage-2 probe",
        )
        expected_target, expected_claim_sha, _ = _PROBE_REGISTRY[cand.candidate_id]
        _expect(
            cand.target_open_node_id == expected_target,
            f"Candidate {cand.candidate_id!r} target {cand.target_open_node_id!r} "
            f"!= probe target {expected_target!r}",
        )
        actual_claim_sha = _candidate_claim_sha256(raw_c)
        _expect(
            actual_claim_sha == expected_claim_sha,
            f"Manifest claim/prediction SHA-256 drift for {cand.candidate_id!r}: "
            f"expected {expected_claim_sha[:12]}, actual {actual_claim_sha[:12]}",
        )
        parsed_pairs.append((cand, raw_c.get("expected_checks")))

    gate_verdicts = [
        evaluate_significance(cand, atlas_path=atlas_path, semantic_index=idx).to_dict()
        for cand, _ in parsed_pairs
    ]
    _expect(
        all(v["decision"] == "ACCEPT" for v in gate_verdicts),
        f"Run-02 manifest failed Significance Gate: {gate_verdicts}",
    )

    probes = []
    for cand, exp_checks in parsed_pairs:
        _, _, probe_fn = _PROBE_REGISTRY[cand.candidate_id]
        result = probe_fn()
        _expect(
            result["candidate_id"] == cand.candidate_id
            and result["target_open_node_id"] == cand.target_open_node_id,
            f"Probe result metadata mismatch for {cand.candidate_id!r}",
        )
        _verify_expected_checks(cand.candidate_id, result, exp_checks)
        probes.append(result)

    return {
        "status": "ok",
        "run_name": manifest["run_name"],
        "seed": manifest["seed"],
        "atlas_sha256": idx.atlas_sha256,
        "significance_gate_accepted": len(gate_verdicts),
        "significance_gate_verdicts": gate_verdicts,
        "probes": probes,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R12 Run-02 Stage-2 Falsify-First Runner.")
    parser.add_argument("--manifest", default=str(MANIFEST_DEFAULT))
    parser.add_argument("--atlas", default=str(ATLAS_JSON_DEFAULT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        report = run_all(pathlib.Path(args.manifest), pathlib.Path(args.atlas))
    except (Run02FalsifyError, OSError, ValueError, KeyError) as exc:
        print(f"RUN-02 FALSIFY ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        summary = ", ".join(f"{p['candidate_id']}={p['verdict']}" for p in report["probes"])
        print(
            f"R12 RUN-02 FALSIFY-FIRST OK: {report['significance_gate_accepted']}/5 "
            f"Significance Gate ACCEPTED | {summary}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
