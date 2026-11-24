"""Two-stage ARO families + exact ground truth (Judge-Numerical v1, Track A).

Model (fixed recourse, RHS-only uncertainty):

    z* = min_{x >= 0, Ax >= b}  c·x + max_{zeta in Z} phi(h(zeta) - T x),
    phi(r) = min{ q·y : W y >= r, y >= 0 },      h(zeta) = h0 + H zeta.

Z is a polytope carried by an explicit vertex list. Since phi is convex and
h is affine, zeta -> phi(h(zeta) - T x) is convex, so its max over Z is
attained at a vertex, and the exact compact reformulation holds:

    z* = min  c·x + t
         s.t. Ax >= b, x >= 0,
              W y_v >= h(v) - T x,   q·y_v <= t        for every vertex v.

(Relaxation direction: any feasible (x, t) has t >= max_v phi(h(v) - T x);
tightness: evaluate the optimal x and take y_v optimal for each phi.)

Ground truth is certified by an exact cutting-plane over this LP: solve on a
vertex subset S, scan all vertices for a violated one (phi(h(w) - T x) > t),
add it and repeat. The restricted problem relaxes the full one, a solution
violating no vertex is optimal for the full problem, and no vertex is added
twice — so the loop terminates with the exact z* in Fractions.

Generators use the project-owned splitmix64 RNG: instance data depends on
nothing but the frozen constants in this file. Per FOUNDATION §5 grids and
seeds are frozen before any candidate is evaluated; changing them is a human
decision recorded in the journal.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from aro import exactlp  # noqa: E402
from aro.detrng import DetRng  # noqa: E402

F0, F1 = F(0), F(1)


# ---------------------------------------------------------------- vertices


def budget_vertices(nz: int, gamma: F) -> tuple[tuple[F, ...], ...]:
    """Vertices of {0 <= zeta <= 1, sum zeta <= gamma}, sorted canonically.

    A point is a vertex iff at most one coordinate is fractional; integral
    vertices have popcount <= floor(gamma), fractional ones carry exactly
    gamma - floor(gamma) in one coordinate and floor(gamma) ones elsewhere.
    """
    floor_g = int(gamma)
    frac = gamma - floor_g
    out: set[tuple[F, ...]] = set()
    for bits in range(1 << nz):
        if bin(bits).count("1") <= floor_g:
            out.add(tuple(F((bits >> (nz - 1 - j)) & 1) for j in range(nz)))
    if frac > 0:
        for jf in range(nz):
            for bits in range(1 << (nz - 1)):
                if bin(bits).count("1") != floor_g:
                    continue
                row = [F0] * nz
                row[jf] = frac
                k = 0
                for j in range(nz):
                    if j != jf:
                        row[j] = F((bits >> (nz - 2 - k)) & 1)
                        k += 1
                out.add(tuple(row))
    return tuple(sorted(out))


def box_vertices(ups: tuple[F, ...]) -> tuple[tuple[F, ...], ...]:
    """Vertices of the box prod_j [0, ups_j], sorted canonically."""
    verts: list[tuple[F, ...]] = [()]
    for u in ups:
        verts = [v + (lo,) for v in verts for lo in (F0, u)]
    return tuple(sorted(verts))


# ---------------------------------------------------------------- families


@dataclass(frozen=True)
class FamilyCfg:
    fid: str
    title_ru: str
    verts: tuple[tuple[F, ...], ...]
    dims: tuple[int, int, int, int]  # n_x, m1, m_y, n_y
    seed: int
    n_dev: int
    n_heldout: int
    # data ranges (lo, hi) per matrix; attack grids widen them (e.g. negative T)
    t_range: tuple[int, int] = (0, 3)
    h_range: tuple[int, int] = (0, 3)


@dataclass(frozen=True)
class Instance:
    fid: str
    iid: str
    verts: tuple[tuple[F, ...], ...]
    c: tuple[F, ...]
    A: tuple[tuple[F, ...], ...]
    b: tuple[F, ...]
    q: tuple[F, ...]
    W: tuple[tuple[F, ...], ...]
    T: tuple[tuple[F, ...], ...]
    h0: tuple[F, ...]
    H: tuple[tuple[F, ...], ...]

    @property
    def nz(self) -> int:
        return len(self.verts[0])

    @property
    def n_x(self) -> int:
        return len(self.c)

    @property
    def n_y(self) -> int:
        return len(self.q)

    @property
    def m1(self) -> int:
        return len(self.b)

    @property
    def m_y(self) -> int:
        return len(self.W)


def _make_instance(rng: DetRng, cfg: FamilyCfg, iid: str) -> Instance:
    n_x, m1, m_y, n_y = cfg.dims

    def vec(lo: int, hi: int, k: int) -> tuple[F, ...]:
        return tuple(F(rng.next_int(lo, hi)) for _ in range(k))

    # W = [I | d]: identity block guarantees full recourse (phi always
    # feasible); q > 0 and y >= 0 bound phi below by 0.
    W = tuple(tuple(F1 if j == i else F0 for j in range(n_y - 1)) + (F(rng.next_int(0, 2)),)
              for i in range(m_y))
    return Instance(
        fid=cfg.fid, iid=iid, verts=cfg.verts,
        c=vec(1, 5, n_x),
        A=tuple(vec(0, 4, n_x) for _ in range(m1)),
        b=vec(0, 2, m1),
        q=vec(1, 4, n_y),
        W=W,
        T=tuple(vec(*cfg.t_range, n_x) for _ in range(m_y)),
        h0=vec(1, 5, m_y),
        H=tuple(vec(*cfg.h_range, len(cfg.verts[0])) for _ in range(m_y)),
    )


def family_instances(cfg: FamilyCfg) -> list[Instance]:
    rng = DetRng(cfg.seed)
    out = []
    for k in range(cfg.n_dev):
        out.append(_make_instance(rng, cfg, f"dev-{k + 1}"))
    for k in range(cfg.n_heldout):
        out.append(_make_instance(rng, cfg, f"ho-{k + 1}"))
    return out


# Frozen grids. "full" is the benchmark of record; "smoke" is the tiny grid
# that CI diffs for byte-determinism. Seeds/dims change only by human decision.
FULL = (
    FamilyCfg("budget", "бюджетное множество неопределённости",
              budget_vertices(4, F(3, 2)), (4, 2, 3, 4), 20260919, 6, 3),
    FamilyCfg("box", "боксовое множество с разномасштабными границами",
              box_vertices((F(1, 2), F1, F(3, 2), F(2))), (4, 2, 3, 4), 20260920, 6, 3),
)
SMOKE = (
    FamilyCfg("budget", "бюджетное множество неопределённости",
              budget_vertices(3, F(3, 2)), (3, 1, 2, 3), 101, 2, 1),
    FamilyCfg("box", "боксовое множество с разномасштабными границами",
              box_vertices((F1, F(2), F(2))), (3, 1, 2, 3), 102, 2, 1),
)

GRIDS = {"full": FULL, "smoke": SMOKE}

# Candidate budget rule: a construction must certify exactness using at most
# CAP_MULT times the LP work of the certifier, per instance.
CAP_MULT = 4


# ---------------------------------------------------------------- machinery


def h_of(inst: Instance, v: tuple[F, ...]) -> tuple[F, ...]:
    nz = len(v)
    return tuple(inst.h0[i] + sum(inst.H[i][k] * v[k] for k in range(nz))
                 for i in range(inst.m_y))


def recourse_value(inst: Instance, r: list[F]) -> F | None:
    """Exact phi(r); None means recourse infeasible (= +inf demand)."""
    res = exactlp.solve_min(list(inst.q), [list(w) for w in inst.W], r)
    return res.value if res.status == exactlp.OPTIMAL else None


def restricted_solution(inst: Instance, subset: list[tuple[F, ...]]) -> exactlp.LPResult:
    """Compact LP over a vertex subset: vars x | t (free) | y_v per v in subset.

    Objective is c·x + t; the per-vertex recourse vectors y_v carry zero cost —
    their expense enters only through the epigraph rows t >= q·y_v.
    """
    k = len(subset)
    nv = inst.n_x + 1 + k * inst.n_y
    c = list(inst.c) + [F1] + [F0] * (k * inst.n_y)
    rows: list[list[F]] = []
    rhs: list[F] = []
    for i in range(inst.m1):
        rows.append(list(inst.A[i]) + [F0] * (1 + k * inst.n_y))
        rhs.append(inst.b[i])
    for vi, v in enumerate(subset):
        hv = h_of(inst, v)
        base = inst.n_x + 1 + vi * inst.n_y
        for i in range(inst.m_y):
            row = [F0] * nv
            for j in range(inst.n_x):
                row[j] = inst.T[i][j]
            for j in range(inst.n_y):
                row[base + j] = inst.W[i][j]
            rows.append(row)
            rhs.append(hv[i])
        row = [F0] * nv
        row[inst.n_x] = F1
        for j in range(inst.n_y):
            row[base + j] = -inst.q[j]
        rows.append(row)
        rhs.append(F0)
    free = [False] * inst.n_x + [True] + [False] * (k * inst.n_y)
    return exactlp.solve_min(c, rows, rhs, free)


def x_cost_exact(inst: Instance, x: tuple[F, ...]) -> F | None:
    """c·x + max_v phi(h(v) - T x) by exact LP per vertex; None if infeasible.

    Infeasible means: a first-stage row is violated (x is not admissible at
    all) or some recourse LP is infeasible. Either way the construction's
    "cost" does not exist and the judge must refute it, not score it."""
    for i in range(inst.m1):
        if sum(inst.A[i][j] * x[j] for j in range(inst.n_x)) < inst.b[i]:
            return None
    worst: F | None = None
    for v in verts_of(inst):
        r = [a - b for a, b in zip(h_of(inst, v),
                                   (sum((inst.T[i][j] * x[j] for j in range(inst.n_x)),
                                        F(0))
                                    for i in range(inst.m_y)), strict=True)]
        ph = recourse_value(inst, r)
        if ph is None:
            return None
        worst = ph if worst is None else max(worst, ph)
    assert worst is not None, "instance without vertices has no worst case"
    cost_x = sum((inst.c[j] * x[j] for j in range(inst.n_x)), F(0))
    return cost_x + worst


def verts_of(inst: Instance) -> tuple[tuple[F, ...], ...]:
    return inst.verts


ADD_RULES = ("first", "worst", "all")


def certify(inst: Instance, start: list[tuple[F, ...]] | None = None,
            lp_cap: int | None = None, add: str = "first") -> dict[str, Any]:
    """Exact z* by cutting-plane; canonical vertex order makes it deterministic.

    add = scenario-generation rule per iteration (the C&CG axis, Zeng-Zhao
    2013; adding primal recourse blocks for identified scenarios):
      "first" — stop scanning at the first violated vertex, add it
                (fewest phi-LPs per iteration, most iterations);
      "worst" — scan all, add the argmax violation (ties -> canonical);
      "all"   — scan all, add every violated vertex (fewest iterations,
                most phi-LPs per iteration).
    All three certify the same exact z* — they differ only in LP work,
    which is what the judge measures.

    Returns {"zstar", "x", "iters", "lp_count", "subset"} on success or
    {"status": "budget"} if lp_cap LP solves were exhausted.
    """
    if add not in ("first", "worst", "all"):
        raise ValueError(add)
    verts = verts_of(inst)
    S = list(start) if start else [verts[0]]
    lp = 0
    iters = 0
    while True:
        iters += 1
        if lp_cap is not None and lp > lp_cap:
            return {"status": "budget", "lp_count": lp, "iters": iters}
        res = restricted_solution(inst, S)
        lp += 1
        if res.status != exactlp.OPTIMAL:
            raise AssertionError(f"restricted LP {res.status} on {inst.fid}/{inst.iid}")
        assert res.solution is not None, "optimal LP without a solution vector"
        x, t = res.solution[:inst.n_x], res.solution[inst.n_x]
        tx = [sum((inst.T[i][j] * x[j] for j in range(inst.n_x)), F(0))
              for i in range(inst.m_y)]
        if add == "first":
            for w in verts:
                if w in S:
                    continue
                r = [a - b for a, b in zip(h_of(inst, w), tx, strict=True)]
                ph = recourse_value(inst, r)
                lp += 1
                if ph is None or ph > t:
                    S.append(w)
                    break
            else:
                return self_check_and_return(inst, x, t, S, iters, lp)
        else:
            violated: list[tuple[F, tuple[F, ...]]] = []
            for w in verts:
                if w in S:
                    continue
                r = [a - b for a, b in zip(h_of(inst, w), tx, strict=True)]
                ph = recourse_value(inst, r)
                lp += 1
                if ph is None or ph > t:
                    violated.append((F(10) ** 9 if ph is None else ph, w))
            if not violated:
                return self_check_and_return(inst, x, t, S, iters, lp)
            if add == "worst":
                best = sorted(violated, key=lambda pw: (-pw[0], pw[1]))[0][1]
                S.append(best)
            else:  # "all"
                for _, w in violated:
                    S.append(w)


def self_check_and_return(inst: Instance, x: tuple[F, ...], t: F,
                          S: list[tuple[F, ...]], iters: int, lp: int,
                          ) -> dict[str, Any]:
    cost = sum((inst.c[j] * x[j] for j in range(inst.n_x)), F(0)) + t
    # Hard self-check: z* claimed from the restricted LP must equal the
    # independently recomputed worst-case cost of x (per-vertex phi LPs).
    # A mismatch means the LP builder and the verifier disagree — crash
    # loudly instead of emitting a wrong verdict (judge contract).
    indep = x_cost_exact(inst, x)
    if indep is None or indep != cost:
        raise AssertionError(
            f"certification self-check failed on {inst.fid}/{inst.iid}: "
            f"restricted z* {cost} vs independent cost {indep}")
    return {"status": "certified", "zstar": cost, "x": x,
            "iters": iters, "lp_count": lp, "subset": S}


def greedy_start(inst: Instance, k: int) -> list[tuple[F, ...]]:
    """Top-k vertices by adversarial load sum_i (H v)_i, ties -> canonical."""
    verts = verts_of(inst)
    nz = len(verts[0])
    keyed = sorted(
        ((sum(inst.H[i][k] * v[k] for i in range(inst.m_y) for k in range(nz)), v)
         for v in verts),
        key=lambda kv: (-kv[0], kv[1]))
    return [v for _, v in keyed[:k]]
