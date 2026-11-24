"""Pure-stdlib exact rational LP solver (Two-Phase Simplex with Bland's anti-cycling rule).

All arithmetic uses `fractions.Fraction` — zero floating-point rounding error.
Solves:
    minimize    c^T x
    subject to  A_ub x <= b_ub
                A_eq x == b_eq
                x_j >= 0   (or free variables via `free_vars` index set)

Every returned optimal solution is independently checked for primal feasibility
and exact objective equality before returning.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from fractions import Fraction

Number = int | str | Fraction


class ExactLPError(ValueError):
    """Raised on malformed LP dimensions or invalid inputs."""


@dataclasses.dataclass(frozen=True)
class ExactLPResult:
    status: str  # "optimal" | "infeasible" | "unbounded"
    objective: Fraction | None
    x: tuple[Fraction, ...] | None


def _to_frac(v: Number) -> Fraction:
    if isinstance(v, Fraction):
        return v
    if isinstance(v, bool):
        raise ExactLPError("Boolean value not allowed in exact rational LP")
    if isinstance(v, (int, str)):
        return Fraction(v)
    raise ExactLPError(f"Unsupported non-exact number type: {type(v).__name__}")


def _pivot(tableau: list[list[Fraction]], basis: list[int], row: int, col: int) -> None:
    piv = tableau[row][col]
    inv = Fraction(1) / piv
    t_row = tableau[row]
    for j in range(len(t_row)):
        t_row[j] *= inv
    for i, r in enumerate(tableau):
        if i == row:
            continue
        factor = r[col]
        if factor != 0:
            for j in range(len(r)):
                r[j] -= factor * t_row[j]
    basis[row] = col


def _simplex_phase(
    tableau: list[list[Fraction]],
    basis: list[int],
    n_vars: int,
    max_iters: int = 20000,
) -> str:
    """Run Bland's rule simplex minimizing the last row of tableau."""
    m = len(basis)
    obj_row = tableau[m]
    for _ in range(max_iters):
        # Bland's rule: smallest variable index with negative reduced cost
        enter = -1
        for j in range(n_vars):
            if obj_row[j] < 0:
                enter = j
                break
        if enter == -1:
            return "optimal"

        # Minimum ratio test with Bland's tie-break (smallest leaving basis variable index)
        leave = -1
        best_ratio: Fraction | None = None
        for i in range(m):
            a_ij = tableau[i][enter]
            if a_ij > 0:
                ratio = tableau[i][n_vars] / a_ij
                if (
                    best_ratio is None
                    or ratio < best_ratio
                    or (ratio == best_ratio and basis[i] < basis[leave])
                ):
                    best_ratio = ratio
                    leave = i
        if leave == -1:
            return "unbounded"
        _pivot(tableau, basis, leave, enter)
    raise ExactLPError(f"Simplex exceeded max_iters={max_iters}")


def solve_exact_lp(
    c: Sequence[Number],
    *,
    A_ub: Sequence[Sequence[Number]] = (),
    b_ub: Sequence[Number] = (),
    A_eq: Sequence[Sequence[Number]] = (),
    b_eq: Sequence[Number] = (),
    free_vars: Sequence[int] = (),
) -> ExactLPResult:
    """Solve an exact rational LP in standard/mixed form via Two-Phase Bland Simplex."""
    n_orig = len(c)
    if n_orig == 0:
        raise ExactLPError("Objective vector c must be non-empty")
    if len(A_ub) != len(b_ub):
        raise ExactLPError("A_ub and b_ub row count mismatch")
    if len(A_eq) != len(b_eq):
        raise ExactLPError("A_eq and b_eq row count mismatch")

    c_orig = [_to_frac(v) for v in c]
    free_set = set(free_vars)
    if any(idx < 0 or idx >= n_orig for idx in free_set):
        raise ExactLPError(f"free_vars out of range [0, {n_orig})")

    # Split each free variable x_j = x_j^+ - x_j^- with x_j^+, x_j^- >= 0
    col_map: list[tuple[int, int | None]] = []
    c_std: list[Fraction] = []
    for j in range(n_orig):
        pos_idx = len(c_std)
        c_std.append(c_orig[j])
        if j in free_set:
            neg_idx = len(c_std)
            c_std.append(-c_orig[j])
            col_map.append((pos_idx, neg_idx))
        else:
            col_map.append((pos_idx, None))

    def _expand_row(row: Sequence[Number]) -> list[Fraction]:
        if len(row) != n_orig:
            raise ExactLPError(f"Constraint row length {len(row)} != {n_orig}")
        out = [Fraction(0)] * len(c_std)
        for j, val in enumerate(row):
            fv = _to_frac(val)
            p_idx, n_idx = col_map[j]
            out[p_idx] = fv
            if n_idx is not None:
                out[n_idx] = -fv
        return out

    # Convert inequalities A_ub x <= b_ub into equalities with nonnegative slack variables
    n_slacks = len(A_ub)
    n_base = len(c_std) + n_slacks
    rows: list[list[Fraction]] = []
    rhs: list[Fraction] = []

    for i, (row, b_val) in enumerate(zip(A_ub, b_ub, strict=True)):
        expanded = _expand_row(row) + [Fraction(0)] * n_slacks
        expanded[len(c_std) + i] = Fraction(1)
        b_f = _to_frac(b_val)
        if b_f < 0:
            expanded = [-v for v in expanded]
            b_f = -b_f
        rows.append(expanded)
        rhs.append(b_f)

    for row, b_val in zip(A_eq, b_eq, strict=True):
        expanded = _expand_row(row) + [Fraction(0)] * n_slacks
        b_f = _to_frac(b_val)
        if b_f < 0:
            expanded = [-v for v in expanded]
            b_f = -b_f
        rows.append(expanded)
        rhs.append(b_f)

    m = len(rows)
    if m == 0:
        if any(v < 0 for v in c_std):
            return ExactLPResult(status="unbounded", objective=None, x=None)
        zeros = tuple(Fraction(0) for _ in range(n_orig))
        return ExactLPResult(status="optimal", objective=Fraction(0), x=zeros)

    # Phase I: add artificial variables for every row lacking a trivial unit slack column
    basis: list[int] = [-1] * m
    art_cols: list[int] = []
    n_total = n_base

    # Identify rows that already have a positive unit slack column
    for i in range(m):
        for s_col in range(len(c_std), n_base):
            if rows[i][s_col] == 1 and all(rows[r][s_col] == 0 for r in range(m) if r != i):
                basis[i] = s_col
                break
        if basis[i] == -1:
            art_cols.append(n_total)
            basis[i] = n_total
            n_total += 1

    # Build Phase I tableau
    tableau: list[list[Fraction]] = []
    for i in range(m):
        r = rows[i] + [Fraction(0)] * len(art_cols) + [rhs[i]]
        if basis[i] >= n_base:
            r[basis[i]] = Fraction(1)
        tableau.append(r)

    if art_cols:
        phase1_obj = [Fraction(0)] * (n_total + 1)
        for col in art_cols:
            phase1_obj[col] = Fraction(1)
        # Eliminate basic artificial variables from Phase I objective row
        for i in range(m):
            if basis[i] >= n_base:
                for j in range(n_total + 1):
                    phase1_obj[j] -= tableau[i][j]
        tableau.append(phase1_obj)

        p1_status = _simplex_phase(tableau, basis, n_total)
        if p1_status != "optimal" or tableau[m][n_total] != 0:
            return ExactLPResult(status="infeasible", objective=None, x=None)

        # Drive any remaining degenerate artificial variable out of basis
        for i in range(m):
            if basis[i] >= n_base:
                piv_col = next((j for j in range(n_base) if tableau[i][j] != 0), -1)
                if piv_col != -1:
                    _pivot(tableau, basis, i, piv_col)

        # Drop redundant zero rows with artificial basis and strip artificial columns
        keep_rows = [i for i in range(m) if basis[i] < n_base]
        tableau = [
            tableau[i][:n_base] + [tableau[i][n_total]] for i in keep_rows
        ]
        basis = [basis[i] for i in keep_rows]
        m = len(basis)
    else:
        tableau = [rows[i] + [rhs[i]] for i in range(m)]

    # Build Phase II objective row
    c_full = c_std + [Fraction(0)] * n_slacks
    phase2_obj = list(c_full) + [Fraction(0)]
    for i in range(m):
        cb = c_full[basis[i]]
        if cb != 0:
            for j in range(n_base + 1):
                phase2_obj[j] -= cb * tableau[i][j]
    tableau.append(phase2_obj)

    p2_status = _simplex_phase(tableau, basis, n_base)
    if p2_status != "optimal":
        return ExactLPResult(status=p2_status, objective=None, x=None)

    x_std = [Fraction(0)] * n_base
    for i, col in enumerate(basis):
        x_std[col] = tableau[i][n_base]

    x_orig: list[Fraction] = []
    for p_idx, n_idx in col_map:
        val = x_std[p_idx] - (x_std[n_idx] if n_idx is not None else Fraction(0))
        x_orig.append(val)

    # Independent primal feasibility & objective check
    for j in range(n_orig):
        if j not in free_set and x_orig[j] < 0:
            raise ExactLPError(f"Internal error: negative non-free variable x[{j}]={x_orig[j]}")
    for row, b_val in zip(A_ub, b_ub, strict=True):
        lhs = sum((_to_frac(a) * xv for a, xv in zip(row, x_orig, strict=True)), Fraction(0))
        if lhs > _to_frac(b_val):
            raise ExactLPError(f"Internal error: violated A_ub row ({lhs} > {b_val})")
    for row, b_val in zip(A_eq, b_eq, strict=True):
        lhs = sum((_to_frac(a) * xv for a, xv in zip(row, x_orig, strict=True)), Fraction(0))
        if lhs != _to_frac(b_val):
            raise ExactLPError(f"Internal error: violated A_eq row ({lhs} != {b_val})")

    obj = sum((ci * xi for ci, xi in zip(c_orig, x_orig, strict=True)), Fraction(0))
    return ExactLPResult(status="optimal", objective=obj, x=tuple(x_orig))
