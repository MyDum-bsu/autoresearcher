#!/usr/bin/env python3
"""Executable T1-T7 falsification battery for ADR exactness conditions (R2 #1156).

Every instance is grounded in `research/literature/exactness-essay/` and `corpus/`,
and solved from first principles using exact rational LP (`verification.oracles.exact_lp`)
and exact symbolic arithmetic (`sympy`) — zero floating-point heuristics.

Instances:
  T1  Bridge-class 1D + 2D (§5 of essay; P3 in Aroform)     -> exact (gap = 0)
  T2  SOC temporal network on Euclidean ball ([XB17, §4.1]) -> not_exact
                                                               (full-matrix ADR=s vs (s+sqrt(s))/2)
  T3  Chen-Zhang N-vs-1 cross-polytope ([CZ09, p. 6])       -> not_exact for ADR (3 vs 1),
                                                               exact for EAARC (1 vs 1)
  T4  GTW25 condition-(B) violation ([GTW25, Prop. 1, p.45])-> not_exact (3/2 vs 5/4)
  T5  BEG18 separating instance ([BEG18, Eq. (ex:bad)], m=900)-> not_exact (strict gap > 0)
  T6  Box uncertainty, static ([BdR16, p. 12] / [BGT04])    -> exact (2 vs 2)
  T7  Simplex uncertainty ([ZDS18, p. 12] / [BG12])         -> exact (gap = 0)
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from collections.abc import Callable
from fractions import Fraction
from typing import Any

import sympy as sp

from verification.oracles.exact_lp import solve_exact_lp


@dataclasses.dataclass(frozen=True)
class BatteryCaseResult:
    case_id: str
    title: str
    anchor: str
    expected_verdict: str  # "exact" | "not_exact"
    observed_verdict: str  # "exact" | "not_exact"
    v_aro: str
    v_adr: str
    gap: str
    passed: bool
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def _solve_vertex_adr(
    vertices: list[tuple[Fraction, ...]],
    n_y: int,
    c_y: list[Fraction],
    constraints_fn: Callable[[tuple[Fraction, ...]], list[tuple[list[Fraction], Fraction]]],
) -> Fraction:
    """Solve exact worst-case affine decision rule LP over finite extreme points.

    Variables: t (free), and for each k in 0..n_y-1: y0_k (free), Y_{k,0..d-1} (free).
    Constraints at every vertex v:
      - sum_k c_y[k] * y_k(v) - t <= 0
      - each row (a_y, rhs) from constraints_fn(v): sum_k a_y[k] * y_k(v) <= rhs
    """
    d = len(vertices[0])
    stride = 1 + d
    n_vars = 1 + n_y * stride  # index 0 is epigraph t

    c = [Fraction(0)] * n_vars
    c[0] = Fraction(1)
    A_ub: list[list[Fraction]] = []
    b_ub: list[Fraction] = []

    def _y_coeffs(v: tuple[Fraction, ...], weights: list[Fraction]) -> list[Fraction]:
        row = [Fraction(0)] * n_vars
        for k, wk in enumerate(weights):
            if wk == 0:
                continue
            base = 1 + k * stride
            row[base] = wk
            for j in range(d):
                row[base + 1 + j] = wk * v[j]
        return row

    for v in vertices:
        ep_row = _y_coeffs(v, c_y)
        ep_row[0] = Fraction(-1)
        A_ub.append(ep_row)
        b_ub.append(Fraction(0))
        for a_y, rhs in constraints_fn(v):
            A_ub.append(_y_coeffs(v, a_y))
            b_ub.append(rhs)

    res = solve_exact_lp(c, A_ub=A_ub, b_ub=b_ub, free_vars=list(range(n_vars)))
    if res.status != "optimal" or res.objective is None:
        raise RuntimeError(f"ADR LP did not solve to optimality: {res.status}")
    return res.objective


def _solve_vertex_aro(
    vertices: list[tuple[Fraction, ...]],
    n_y: int,
    c_y: list[Fraction],
    constraints_fn: Callable[[tuple[Fraction, ...]], list[tuple[list[Fraction], Fraction]]],
) -> Fraction:
    """Solve exact worst-case adaptive optimal value max_{v in V} min_y c_y^T y."""
    worst: Fraction | None = None
    for v in vertices:
        rows = constraints_fn(v)
        A_ub = [a for a, _ in rows]
        b_ub = [b for _, b in rows]
        res = solve_exact_lp(c_y, A_ub=A_ub, b_ub=b_ub, free_vars=list(range(n_y)))
        if res.status != "optimal" or res.objective is None:
            raise RuntimeError(f"ARO vertex LP failed at {v}: {res.status}")
        if worst is None or res.objective > worst:
            worst = res.objective
    if worst is None:
        raise RuntimeError("Empty vertex list in _solve_vertex_aro")
    return worst


def run_t1() -> BatteryCaseResult:
    """T1: 1D + 2D bridge-class exactness (Essay §5; P3 in Aroform)."""
    # 1D instance: y(zeta) >= max((1-zeta)*a + zeta*b, 0), y >= 0, zeta in [0, 1]
    a, b = Fraction(-1), Fraction(3)
    verts_1d = [(Fraction(0),), (Fraction(1),)]

    def cons_1d(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        z = v[0]
        demand = (Fraction(1) - z) * a + z * b
        return [([-Fraction(1)], -demand), ([-Fraction(1)], Fraction(0))]

    v_aro_1d = _solve_vertex_aro(verts_1d, 1, [Fraction(1)], cons_1d)
    v_adr_1d = _solve_vertex_adr(verts_1d, 1, [Fraction(1)], cons_1d)

    # 2D bridge-class with e1 = -e2 = 1, T = 2, d0 = 1/2 on vertices {-1, +1}^2
    # Wait: rotation gives |x1|+|x2| = max(|s|, |d|), controlled s=d0+u, uncontrolled d=d0+2*(w0+w1)
    d0 = Fraction(1, 2)
    verts_2d = [(Fraction(w0), Fraction(w1)) for w0 in (-1, 1) for w1 in (-1, 1)]

    def cons_2d(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        # Variables: y = [u, tau]; tau >= |d0 + u| and tau >= |d0 + 2*(w0 + w1)|, |u| <= 1
        d_coord = d0 + Fraction(2) * (v[0] + v[1])
        return [
            ([Fraction(1), Fraction(-1)], -d0),       # d0 + u <= tau
            ([Fraction(-1), Fraction(-1)], d0),       # -(d0 + u) <= tau
            ([Fraction(0), Fraction(-1)], -d_coord),  # d_coord <= tau
            ([Fraction(0), Fraction(-1)], d_coord),   # -d_coord <= tau
            ([Fraction(1), Fraction(0)], Fraction(1)),
            ([Fraction(-1), Fraction(0)], Fraction(1)),
        ]

    v_aro_2d = _solve_vertex_aro(verts_2d, 2, [Fraction(0), Fraction(1)], cons_2d)
    v_adr_2d = _solve_vertex_adr(verts_2d, 2, [Fraction(0), Fraction(1)], cons_2d)

    gap = (v_adr_1d - v_aro_1d) + (v_adr_2d - v_aro_2d)
    observed = "exact" if gap == 0 else "not_exact"
    passed = (
        v_aro_1d == Fraction(3)
        and v_adr_1d == Fraction(3)
        and v_aro_2d == Fraction(9, 2)
        and v_adr_2d == Fraction(9, 2)
        and observed == "exact"
    )
    return BatteryCaseResult(
        case_id="T1",
        title="Bridge-class 1D & 2D (cube vertices)",
        anchor=(
            "research/literature/exactness-essay/"
            "2026-10-20-essay-exactness-and-open-problems.ru.md §5"
        ),
        expected_verdict="exact",
        observed_verdict=observed,
        v_aro=f"1D={v_aro_1d}, 2D={v_aro_2d}",
        v_adr=f"1D={v_adr_1d}, 2D={v_adr_2d}",
        gap=str(gap),
        passed=passed,
    )


def _solve_t2_temporal_network(s: int) -> tuple[sp.Expr, Fraction, sp.Expr]:
    """Solve Xu-Burer (2017) §4.1 SOC temporal network for dimension s >= 2.

    Problem (`arlp.tex` Eq. (equ:temporal_simple), lines 861-899) in shifted
    coordinates z = 2*xi - 1 in the unit Euclidean ball B_2^s = {||z||_2 <= 1}:
        min_{y(.) in R^s} max_{||z||_2 <= 1} y_s(z)
        s.t. y_1(z) >= (1 +- z_1)/2
             y_i(z) - y_{i-1}(z) >= (1 +- z_i)/2   (i = 2..s).

    Full-matrix affine decision rules y(z) = y_0 + Y z (arbitrary dense Y in R^{s x s},
    NO diagonal restriction) satisfy:
      - Lower bound: inscribed subset V_s = {+-e_1, ..., +-e_s, 0} subset B_2^s solved
        by exact rational full-matrix LP (`_solve_vertex_adr`) gives V_ADR(V_s) = s;
        additionally verified symbolically with dense Y in SymPy (cross-terms cancel
        when averaging +e_i and -e_i, forcing a_i - a_{i-1} >= 1 and a_s >= s).
      - Upper bound: explicit affine/static witness y_k(z) = k is feasible on all of
        B_2^s (since |z_i| <= ||z||_2 <= 1) with worst-case cost s.
      Hence V_ADR = s exactly.
    Adaptive optimal value:
      - Telescoping gives y_s(z) >= (s + ||z||_1)/2, attained pointwise by
        y_k*(z) = sum_{i=1}^k (1 + |z_i|)/2; by Cauchy-Schwarz max_{||z||_2<=1} ||z||_1
        = sqrt(s) (attained at z* = (1/sqrt(s)) * 1_s in B_2^s), so V_ARO = (s + sqrt(s))/2.
    """
    if s < 2:
        raise ValueError(f"T2 temporal network requires s >= 2, got {s}")

    # 1. Inscribed finite subset V_s = {+-e_1, ..., +-e_s, 0} subset B_2^s
    vertices: list[tuple[Fraction, ...]] = [tuple(Fraction(0) for _ in range(s))]
    for i in range(s):
        for sign in (Fraction(1), Fraction(-1)):
            v = [Fraction(0)] * s
            v[i] = sign
            vertices.append(tuple(v))
    for v in vertices:
        if sum(c * c for c in v) > Fraction(1):
            raise RuntimeError(f"Test point {v} is outside unit Euclidean ball")

    def cons(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        rows: list[tuple[list[Fraction], Fraction]] = []
        for i in range(s):
            a_row = [Fraction(0)] * s
            a_row[i] = Fraction(-1)
            if i > 0:
                a_row[i - 1] = Fraction(1)
            # y_i - y_{i-1} >= (1 + v_i)/2  <=>  y_{i-1} - y_i <= -(1 + v_i)/2
            rows.append((list(a_row), -(Fraction(1) + v[i]) / Fraction(2)))
            rows.append((list(a_row), -(Fraction(1) - v[i]) / Fraction(2)))
        return rows

    c_y = [Fraction(0)] * (s - 1) + [Fraction(1)]
    # Full unrestricted dense matrix ADR: all s intercepts + s^2 matrix entries free!
    v_adr_lb = _solve_vertex_adr(vertices, s, c_y, cons)

    # 2. Explicit symbolic verification with arbitrary dense Y in R^{s x s}
    a_syms = sp.symbols(f"a0:{s}", real=True)
    y_mat = sp.Matrix(s, s, lambda r, c: sp.Symbol(f"Y_{r}_{c}", real=True))
    z_vec = sp.Matrix(sp.symbols(f"z0:{s}", real=True))
    y_aff = sp.Matrix(a_syms) + y_mat * z_vec
    telescoped = sp.Integer(0)
    for i in range(s):
        delta_i = y_aff[i] if i == 0 else y_aff[i] - y_aff[i - 1]
        sub_plus = {z_vec[j]: (1 if j == i else 0) for j in range(s)}
        sub_minus = {z_vec[j]: (-1 if j == i else 0) for j in range(s)}
        avg_i = sp.simplify((delta_i.subs(sub_plus) + delta_i.subs(sub_minus)) / 2)
        telescoped = sp.simplify(telescoped + avg_i)
    if sp.simplify(telescoped - a_syms[s - 1]) != 0:
        raise RuntimeError(f"Dense-Y cancellation check failed: got {telescoped}")

    # 3. Exact adaptive value V_ARO = (s + sqrt(s)) / 2 at z* = (1/sqrt(s)) * 1_s in B_2^s
    inv_sqrt_s = sp.Integer(1) / sp.sqrt(s)
    z_star = [inv_sqrt_s] * s
    if sp.simplify(sum(zi * zi for zi in z_star) - 1) != 0:
        raise RuntimeError("z* is not on the unit Euclidean sphere")
    v_aro = sp.simplify(sum((1 + sp.Abs(zi)) / 2 for zi in z_star))
    expected_aro = sp.simplify((sp.Integer(s) + sp.sqrt(s)) / 2)
    if sp.simplify(v_aro - expected_aro) != 0:
        raise RuntimeError(f"Unexpected V_ARO for s={s}: {v_aro} vs {expected_aro}")

    # Upper bound witness y_k(z) = k is feasible on all of B_2^s -> V_ADR <= s
    v_adr_ub = Fraction(s)
    if v_adr_lb != v_adr_ub:
        raise RuntimeError(f"T2 full-matrix ADR lower/upper mismatch: {v_adr_lb} vs {v_adr_ub}")
    gap = sp.simplify(sp.Integer(v_adr_ub.numerator) / sp.Integer(v_adr_ub.denominator) - v_aro)
    return v_aro, v_adr_ub, gap


def run_t2() -> BatteryCaseResult:
    """T2: Xu-Burer (2017) §4.1 SOC temporal network on Euclidean ball (full-matrix ADR)."""
    v_aro_2, v_adr_2, gap_2 = _solve_t2_temporal_network(2)
    v_aro_4, v_adr_4, gap_4 = _solve_t2_temporal_network(4)

    is_strict = (
        bool(gap_2.evalf() > 0)
        and bool(sp.simplify(v_aro_2 - (1 + sp.sqrt(2) / 2)) == 0)
        and v_adr_2 == Fraction(2)
        and bool(sp.simplify(v_aro_4 - 3) == 0)
        and v_adr_4 == Fraction(4)
        and bool(sp.simplify(gap_4 - 1) == 0)
    )
    observed = "not_exact" if is_strict else "exact"
    return BatteryCaseResult(
        case_id="T2",
        title="SOC temporal network on Euclidean ball (full-matrix ADR, Omega(s) gap)",
        anchor=(
            "corpus/tex_src/07_Xu_Burer_2017/arlp.tex lines 853-899 "
            "(Eq. (equ:temporal_simple), Lemma calculateVar2)"
        ),
        expected_verdict="not_exact",
        observed_verdict=observed,
        v_aro=f"s=2: {v_aro_2}; s=4: {v_aro_4}",
        v_adr=f"s=2: {v_adr_2}; s=4: {v_adr_4}",
        gap=f"s=2: {gap_2}; s=4: {gap_4}",
        passed=(observed == "not_exact"),
        notes=(
            "Full-matrix ADR (unrestricted dense Y in R^{s x s}) solved by exact rational LP "
            "on inscribed {+-e_i, 0} subset B_2^s + SymPy cancellation; "
            "V_ADR=s, V_ARO=(s+sqrt(s))/2, gap=(s-sqrt(s))/2"
        ),
    )


def run_t3() -> BatteryCaseResult:
    """T3: Chen-Zhang N-vs-1 cross-polytope (N=3; ADR=3, ARO=EAARC=1)."""
    n_dim = 3
    vertices: list[tuple[Fraction, ...]] = []
    for i in range(n_dim):
        for sign in (Fraction(1), Fraction(-1)):
            v = [Fraction(0)] * n_dim
            v[i] = sign
            vertices.append(tuple(v))

    def cons(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        rows: list[tuple[list[Fraction], Fraction]] = []
        for i in range(n_dim):
            # -y_i <= -v_i  and  -y_i <= v_i  (i.e. y_i >= |v_i|)
            a_row = [Fraction(0)] * n_dim
            a_row[i] = Fraction(-1)
            rows.append((list(a_row), -v[i]))
            rows.append((list(a_row), v[i]))
        return rows

    c_y = [Fraction(1)] * n_dim
    v_aro = _solve_vertex_aro(vertices, n_dim, c_y, cons)
    v_adr = _solve_vertex_adr(vertices, n_dim, c_y, cons)

    # EAARC lifts z = v - w (v,w >= 0, ||v+w||_1 <= 1): vertices are e_i in R^{2N}
    lifted_vertices: list[tuple[Fraction, ...]] = []
    for i in range(2 * n_dim):
        lv = [Fraction(0)] * (2 * n_dim)
        lv[i] = Fraction(1)
        lifted_vertices.append(tuple(lv))

    def cons_eaarc(lv: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        z = tuple(lv[i] - lv[n_dim + i] for i in range(n_dim))
        return cons(z)

    v_eaarc = _solve_vertex_adr(lifted_vertices, n_dim, c_y, cons_eaarc)

    gap = v_adr - v_aro
    observed = "exact" if gap == 0 else "not_exact"
    passed = (
        v_aro == Fraction(1)
        and v_eaarc == Fraction(1)
        and v_adr == Fraction(n_dim)
        and observed == "not_exact"
    )
    return BatteryCaseResult(
        case_id="T3",
        title="Chen-Zhang N-vs-1 (N=3): ADR=3, ARO=EAARC=1",
        anchor="corpus/03_Chen_Zhang_2009.pdf p. 6 (Examples 1-2)",
        expected_verdict="not_exact",
        observed_verdict=observed,
        v_aro=str(v_aro),
        v_adr=str(v_adr),
        gap=str(gap),
        passed=passed,
        notes=f"Extended affine EAARC value = {v_eaarc} (exact)",
    )


def run_t4() -> BatteryCaseResult:
    """T4: GTW25 condition-(B) violation (3/2 vs 5/4 on xi ~ U[-1, 1])."""
    # Exact SymPy integral of Q(xi) = min { y1 + 2 y2 : y1 + y2 >= xi + 1, 0 <= y1,y2 <= 1 }
    xi = sp.Symbol("xi", real=True)
    # On [-1, 0]: y1 = xi + 1, y2 = 0 -> Q(xi) = xi + 1
    # On [0, 1]:  y1 = 1, y2 = xi     -> Q(xi) = 1 + 2 xi
    e_q = (sp.integrate(xi + 1, (xi, -1, 0)) + sp.integrate(1 + 2 * xi, (xi, 0, 1))) / 2
    v_aro = Fraction(int(e_q.p), int(e_q.q))

    # Exact Fraction LP for optimal affine rule y1(xi)=a1+b1*xi, y2(xi)=a2+b2*xi on [-1, 1]:
    # Minimize E[y1 + 2 y2] = a1 + 2 a2 (since E[xi]=0)
    # Constraints at endpoints xi = -1 and xi = 1 (sufficient & necessary for linear inequalities):
    #   variables: [a1, b1, a2, b2] (all free)
    A_ub: list[list[Fraction]] = []
    b_ub: list[Fraction] = []
    for xval in (Fraction(-1), Fraction(1)):
        # -y1 - y2 <= -(xval + 1)
        A_ub.append([Fraction(-1), -xval, Fraction(-1), -xval])
        b_ub.append(-(xval + Fraction(1)))
        # 0 <= y1 <= 1
        A_ub.append([Fraction(-1), -xval, Fraction(0), Fraction(0)])
        b_ub.append(Fraction(0))
        A_ub.append([Fraction(1), xval, Fraction(0), Fraction(0)])
        b_ub.append(Fraction(1))
        # 0 <= y2 <= 1
        A_ub.append([Fraction(0), Fraction(0), Fraction(-1), -xval])
        b_ub.append(Fraction(0))
        A_ub.append([Fraction(0), Fraction(0), Fraction(1), xval])
        b_ub.append(Fraction(1))

    res = solve_exact_lp(
        [Fraction(1), Fraction(0), Fraction(2), Fraction(0)],
        A_ub=A_ub,
        b_ub=b_ub,
        free_vars=[0, 1, 2, 3],
    )
    if res.status != "optimal" or res.objective is None:
        raise RuntimeError(f"T4 ADR LP failed: {res.status}")
    v_adr = res.objective
    gap = v_adr - v_aro
    observed = "exact" if gap == 0 else "not_exact"
    passed = v_aro == Fraction(5, 4) and v_adr == Fraction(3, 2) and gap == Fraction(1, 4)
    return BatteryCaseResult(
        case_id="T4",
        title="GTW25 condition-(B) counterexample (3/2 vs 5/4)",
        anchor="corpus/24_Georghiou_Tsoukalas_Wiesemann_2025.pdf pp. 10, 45 (Prop. 1)",
        expected_verdict="not_exact",
        observed_verdict=observed,
        v_aro=str(v_aro),
        v_adr=str(v_adr),
        gap=str(gap),
        passed=passed,
    )


def run_t5() -> BatteryCaseResult:
    """T5: BEG18 verbatim separating instance (Eq. (ex:bad), m=900, sqrt(m)=30).

    Uses BEG18's exact permutation-symmetry reduction (Eq. (matrix:P), BG10 Lemmas 7-8)
    solved with exact rational LP, plus BEG18's explicit adaptive witness certifying
    V_ARO <= 1 (affine_domination.tex lines 661-690 & 1435-1466).
    """
    k = 30
    m = k * k  # 900
    inv_k = Fraction(1, k)
    r = m - k  # ceil(m - sqrt(m)) = 870
    beta = Fraction(1) + Fraction(m - 1, k)  # row sum of B = 1 + (m-1)/sqrt(m)

    # Verify BEG18 explicit adaptive witness: x = 0, y(0) = 0, y(e_i) = e_i, y(nu_j) = (1/m)*e
    # (B y(e_i))_i = 1 >= 1; (B y(e_i))_j = 1/k >= 0; (B y(nu))_i = beta / m >= 1/k; cost = 1
    if beta * Fraction(1, m) < inv_k:
        raise RuntimeError("BEG18 adaptive witness failed feasibility check")
    v_aro_upper = Fraction(1)

    # Exact symmetric optimal affine LP over [t (free), alpha (>=0), lam (>=0), theta, mu (free)]
    c_theta_act = (Fraction(1) + Fraction(r - 1, k)) * inv_k
    c_mu_act = (
        (Fraction(1) + Fraction(r - 1, k)) * Fraction(r - 1, k)
        + Fraction(m - r, k) * Fraction(r, k)
    )
    c_theta_inact = Fraction(r, k) * inv_k
    c_mu_inact = (
        Fraction(r, k) * Fraction(r - 1, k)
        + (Fraction(1) + Fraction(m - r - 1, k)) * Fraction(r, k)
    )
    A_ub = [
        [Fraction(0), Fraction(0), Fraction(-1), Fraction(-1), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(-1), Fraction(0), Fraction(-1)],
        [Fraction(0), Fraction(0), Fraction(-1), -inv_k, -Fraction(r - 1, k)],
        [Fraction(0), Fraction(0), Fraction(-1), Fraction(0), -Fraction(r, k)],
        [Fraction(-1), Fraction(0), Fraction(m), Fraction(0), Fraction(0)],
        [Fraction(-1), Fraction(0), Fraction(m), Fraction(1), Fraction(m - 1)],
        [Fraction(-1), Fraction(0), Fraction(m), Fraction(r, k), Fraction(r * (m - 1), k)],
        [Fraction(0), -beta, -beta, Fraction(-1), -Fraction(m - 1, k)],
        [Fraction(0), -beta, -beta, -inv_k, -(Fraction(1) + Fraction(m - 2, k))],
        [Fraction(0), -beta, -beta, -c_theta_act, -c_mu_act],
        [Fraction(0), -beta, -beta, -c_theta_inact, -c_mu_inact],
    ]
    b_ub = [
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(-1),
        Fraction(0),
        -inv_k,
        Fraction(0),
    ]
    res_adr = solve_exact_lp(
        [Fraction(1), Fraction(m, 15), Fraction(0), Fraction(0), Fraction(0)],
        A_ub=A_ub,
        b_ub=b_ub,
        free_vars=[0, 3, 4],
    )
    if res_adr.status != "optimal" or res_adr.objective is None:
        raise RuntimeError(f"T5 ADR LP failed: {res_adr.status}")
    v_adr = res_adr.objective
    gap_lb = v_adr - v_aro_upper
    observed = "not_exact" if gap_lb > 0 else "exact"
    passed = v_adr == Fraction(1800, 929) and gap_lb > 0 and observed == "not_exact"
    return BatteryCaseResult(
        case_id="T5",
        title="BEG18 verbatim separating instance (m=900, Omega(sqrt(m)) family)",
        anchor="corpus/tex_src/10_BenTal_ElHousni_Goyal_2018/affine_domination.tex lines 661-690",
        expected_verdict="not_exact",
        observed_verdict=observed,
        v_aro=f"<= {v_aro_upper}",
        v_adr=str(v_adr),
        gap=f">= {gap_lb}",
        passed=passed,
    )


def run_t6() -> BatteryCaseResult:
    """T6: Constraint-wise box uncertainty, static exact (BdR16 p. 12 / BGT04)."""
    vertices = [(Fraction(z1), Fraction(z2)) for z1 in (-1, 1) for z2 in (-1, 1)]

    def cons(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        return [
            ([Fraction(-1), Fraction(0)], -v[0]),  # y1 >= z1
            ([Fraction(0), Fraction(-1)], -v[1]),  # y2 >= z2
        ]

    c_y = [Fraction(1), Fraction(1)]
    v_aro = _solve_vertex_aro(vertices, 2, c_y, cons)
    v_adr = _solve_vertex_adr(vertices, 2, c_y, cons)
    # Static rule: y1 >= 1, y2 >= 1 -> min y1 + y2 = 2
    v_static = Fraction(2)
    gap = v_adr - v_aro
    observed = "exact" if gap == 0 else "not_exact"
    passed = v_aro == v_adr == v_static == Fraction(2) and observed == "exact"
    return BatteryCaseResult(
        case_id="T6",
        title="Constraint-wise box uncertainty (static = ADR = ARO)",
        anchor=(
            "corpus/05_Bertsimas_deRuiter_2016.pdf p. 12; "
            "corpus/02_BenTal_Goryashko_etal_2004.pdf"
        ),
        expected_verdict="exact",
        observed_verdict=observed,
        v_aro=str(v_aro),
        v_adr=str(v_adr),
        gap=str(gap),
        passed=passed,
    )


def run_t7() -> BatteryCaseResult:
    """T7: Simplex uncertainty exactness for linear/affine rules (ZDS18 p. 12 / BG12)."""
    vertices = [
        (Fraction(0), Fraction(0)),
        (Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(1)),
    ]

    def cons(v: tuple[Fraction, ...]) -> list[tuple[list[Fraction], Fraction]]:
        z1, z2 = v
        return [
            ([Fraction(-1), Fraction(-1)], -(Fraction(1) + z1 + Fraction(2) * z2)),
            ([Fraction(-1), Fraction(0)], -z1),
            ([Fraction(0), Fraction(-1)], -z2),
            ([Fraction(-1), Fraction(0)], Fraction(0)),
            ([Fraction(0), Fraction(-1)], Fraction(0)),
        ]

    c_y = [Fraction(2), Fraction(3)]
    v_aro = _solve_vertex_aro(vertices, 2, c_y, cons)
    v_adr = _solve_vertex_adr(vertices, 2, c_y, cons)
    gap = v_adr - v_aro
    observed = "exact" if gap == 0 else "not_exact"
    passed = gap == 0 and observed == "exact"
    return BatteryCaseResult(
        case_id="T7",
        title="Simplex uncertainty Delta_2 (linear/affine rules exact)",
        anchor="corpus/21_Zhen_denHertog_Sim_2018.pdf p. 12",
        expected_verdict="exact",
        observed_verdict=observed,
        v_aro=str(v_aro),
        v_adr=str(v_adr),
        gap=str(gap),
        passed=passed,
    )


def run_battery() -> list[BatteryCaseResult]:
    return [run_t1(), run_t2(), run_t3(), run_t4(), run_t5(), run_t6(), run_t7()]


def evaluate_conjecture(
    predicate: Callable[[BatteryCaseResult], str],
    cases: list[BatteryCaseResult] | None = None,
) -> dict[str, Any]:
    """Test a candidate necessary-and-sufficient condition against T1-T7.

    `predicate(case)` must return "exact" or "not_exact". Any mismatch falsifies it.
    """
    battery = cases if cases is not None else run_battery()
    mismatches: list[dict[str, str]] = []
    for case in battery:
        predicted = predicate(case)
        if predicted not in ("exact", "not_exact"):
            raise ValueError(f"Invalid prediction {predicted!r} for {case.case_id}")
        if predicted != case.observed_verdict:
            mismatches.append(
                {
                    "case_id": case.case_id,
                    "predicted": predicted,
                    "actual": case.observed_verdict,
                }
            )
    return {
        "survived": len(mismatches) == 0,
        "tested": len(battery),
        "mismatches": mismatches,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run exact T1-T7 ADR falsification battery.")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    args = parser.parse_args(argv)

    results = run_battery()
    failed = [r for r in results if not r.passed]

    if args.json:
        print(
            json.dumps(
                {
                    "status": "ok" if not failed else "failed",
                    "passed": len(results) - len(failed),
                    "total": len(results),
                    "cases": [r.to_dict() for r in results],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for r in results:
            tag = "OK" if r.passed else "FAIL"
            print(
                f"[{tag}] {r.case_id} ({r.observed_verdict}): "
                f"V_ARO={r.v_aro}, V_ADR={r.v_adr}, gap={r.gap}"
            )
        print(f"FALSIFICATION BATTERY T1-T7: {len(results) - len(failed)}/{len(results)} OK")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
