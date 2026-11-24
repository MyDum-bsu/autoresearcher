#!/usr/bin/env python3
"""Reusable Stage 2 Falsify-First SymPy + exact-Fraction counterexample template (R2 #1156).

Enforces non-empty parameter grids with strictly validated finite rational/numeric points
(rejecting `grids: []`, `null`, `bool`, `NaN`, `Inf`, and empty/malformed values) so Stage 2
conjectures can never pass on vacuous or corrupted grids.
"""

from __future__ import annotations

import dataclasses
import itertools
import json
import math
from collections.abc import Callable, Mapping, Sequence
from decimal import Decimal
from fractions import Fraction
from typing import Any

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, rationalize, standard_transformations


class EmptyGridError(ValueError):
    """Raised whenever a falsification grid specification is empty or vacuous."""


class InvalidGridValueError(ValueError):
    """Raised whenever a falsification grid contains a non-finite, null, bool, or invalid point."""


@dataclasses.dataclass(frozen=True)
class CounterexampleWitness:
    point: dict[str, str]
    reason: str
    lhs: str
    rhs: str


@dataclasses.dataclass(frozen=True)
class FalsificationReport:
    claim_id: str
    tested_points: int
    survived: bool
    counterexample: CounterexampleWitness | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "tested_points": self.tested_points,
            "survived": self.survived,
            "counterexample": (
                dataclasses.asdict(self.counterexample)
                if self.counterexample is not None
                else None
            ),
        }


def load_exact_json(text: str) -> Any:
    """Parse JSON preserving exact decimal literals (no IEEE-754 float64 rounding)."""
    return json.loads(text, parse_float=Decimal)


def parse_exact_grid_value(value: Any, *, axis: str = "", grid_idx: int = 0) -> Fraction:
    """Parse a single grid coordinate as an exact finite Fraction.

    Strictly rejects `None` (JSON null), `bool`, `NaN`/`Inf`, empty strings, and
    non-numeric objects. Preserves exact `Decimal` values without float64 rounding.
    """
    loc = f"Grid #{grid_idx} axis {axis!r}" if axis else f"Grid #{grid_idx}"
    if value is None:
        raise InvalidGridValueError(f"{loc} contains null/None point")
    if isinstance(value, bool):
        raise InvalidGridValueError(f"{loc} contains boolean point {value!r}")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, Decimal):
        if not value.is_finite():
            raise InvalidGridValueError(f"{loc} contains non-finite Decimal {value!r}")
        return Fraction(value)
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise InvalidGridValueError(f"{loc} contains non-finite float {value!r}")
        return Fraction(str(value))
    if isinstance(value, str):
        s = value.strip()
        if not s:
            raise InvalidGridValueError(f"{loc} contains empty string point")
        if s.lower() in ("nan", "+nan", "-nan", "inf", "+inf", "-inf", "infinity", "+infinity",
                         "-infinity", "null", "none", "true", "false"):
            raise InvalidGridValueError(f"{loc} contains non-finite/invalid token {value!r}")
        try:
            return Fraction(s)
        except (ValueError, ZeroDivisionError) as exc:
            raise InvalidGridValueError(
                f"{loc} contains invalid rational {value!r}: {exc}"
            ) from exc
    raise InvalidGridValueError(
        f"{loc} contains unsupported point type {type(value).__name__}: {value!r}"
    )


def validate_grids(grids: Sequence[Mapping[str, Sequence[Any]]]) -> int:
    """Validate that grids is non-empty and every coordinate is a finite exact rational."""
    if not isinstance(grids, Sequence) or isinstance(grids, (str, bytes)) or len(grids) == 0:
        raise EmptyGridError("Falsifier grids must be a non-empty list of parameter grids")
    total = 0
    for idx, grid in enumerate(grids):
        if not isinstance(grid, Mapping) or len(grid) == 0:
            raise EmptyGridError(f"Grid #{idx} is empty")
        prod = 1
        for axis, values in grid.items():
            if not isinstance(axis, str) or not axis.strip():
                raise InvalidGridValueError(f"Grid #{idx} has invalid axis name {axis!r}")
            if not isinstance(values, Sequence) or isinstance(values, (str, bytes)) or not values:
                raise EmptyGridError(f"Grid #{idx} axis {axis!r} has empty domain")
            for raw_val in values:
                parse_exact_grid_value(raw_val, axis=axis, grid_idx=idx)
            prod *= len(values)
        total += prod
    if total <= 0:
        raise EmptyGridError("Total grid point count must be positive")
    return total


def run_exact_grid_falsifier(
    claim_id: str,
    grids: Sequence[Mapping[str, Sequence[int | float | Decimal | str | Fraction]]],
    check_point: Callable[[dict[str, Fraction]], tuple[bool, str, str, str]],
) -> FalsificationReport:
    """Exhaustively evaluate exact Fraction points over all grids until a counterexample is found.

    `check_point(pt)` returns `(holds, reason, lhs_str, rhs_str)`.
    """
    validate_grids(grids)
    tested = 0
    for idx, grid in enumerate(grids):
        axes = sorted(grid.keys())
        domains = [
            [parse_exact_grid_value(v, axis=ax, grid_idx=idx) for v in grid[ax]]
            for ax in axes
        ]
        for combo in itertools.product(*domains):
            pt = dict(zip(axes, combo, strict=True))
            tested += 1
            holds, reason, lhs_s, rhs_s = check_point(pt)
            if not holds:
                witness = CounterexampleWitness(
                    point={k: str(v) for k, v in pt.items()},
                    reason=reason,
                    lhs=lhs_s,
                    rhs=rhs_s,
                )
                return FalsificationReport(
                    claim_id=claim_id,
                    tested_points=tested,
                    survived=False,
                    counterexample=witness,
                )
    return FalsificationReport(
        claim_id=claim_id,
        tested_points=tested,
        survived=True,
        counterexample=None,
    )


def sympy_inequality_holds(
    expr_lhs: sp.Expr, expr_rhs: sp.Expr, subs: Mapping[sp.Symbol, Any]
) -> bool:
    """Exact SymPy check for expr_lhs <= expr_rhs at rational substitution `subs`."""
    diff = sp.simplify(expr_lhs.subs(subs) - expr_rhs.subs(subs))
    return bool(diff <= 0)


_SAFE_SYMPY_FUNCS: dict[str, Any] = {
    "Abs": sp.Abs,
    "abs": sp.Abs,
    "Max": sp.Max,
    "max": sp.Max,
    "Min": sp.Min,
    "min": sp.Min,
    "sqrt": sp.sqrt,
    "Rational": sp.Rational,
    "Integer": sp.Integer,
}

_VALID_RELATIONS = frozenset({"<=", "<", ">=", ">", "=="})


def _parse_safe_sympy_expr(expr_str: str, axis_symbols: dict[str, sp.Symbol]) -> sp.Expr:
    if not isinstance(expr_str, str) or not expr_str.strip():
        raise InvalidGridValueError("SymPy expression must be a non-empty string")
    if "__" in expr_str:
        raise InvalidGridValueError(f"Disallowed dunder token in SymPy expression: {expr_str!r}")
    local_dict: dict[str, Any] = {**_SAFE_SYMPY_FUNCS, **axis_symbols}
    try:
        expr = parse_expr(
            expr_str,
            local_dict=local_dict,
            global_dict={},
            transformations=(*standard_transformations, rationalize),
        )
    except Exception as exc:
        raise InvalidGridValueError(
            f"Failed to parse SymPy expression {expr_str!r}: {exc}"
        ) from exc
    if not isinstance(expr, sp.Basic):
        raise InvalidGridValueError(f"Parsed object is not a SymPy expression: {expr!r}")
    unknown = expr.free_symbols - set(axis_symbols.values())
    if unknown:
        names = sorted(str(s) for s in unknown)
        raise InvalidGridValueError(
            f"SymPy expression {expr_str!r} references undeclared symbols: {names}"
        )
    return expr


def evaluate_sympy_relation_claim(
    claim_id: str,
    grids: Sequence[Mapping[str, Sequence[Any]]],
    lhs_str: str,
    rhs_str: str,
    relation: str = "<=",
) -> FalsificationReport:
    """Evaluate a declarative SymPy relation (`lhs <rel> rhs`) over validated exact grids."""
    if relation not in _VALID_RELATIONS:
        raise InvalidGridValueError(
            f"Unsupported relation {relation!r}; expected one of {sorted(_VALID_RELATIONS)}"
        )
    validate_grids(grids)
    all_axes = sorted({ax for grid in grids for ax in grid})
    axis_symbols = {ax: sp.Symbol(ax, real=True) for ax in all_axes}
    lhs_expr = _parse_safe_sympy_expr(lhs_str, axis_symbols)
    rhs_expr = _parse_safe_sympy_expr(rhs_str, axis_symbols)

    def _check_pt(pt: dict[str, Fraction]) -> tuple[bool, str, str, str]:
        subs = {axis_symbols[k]: sp.Rational(v.numerator, v.denominator) for k, v in pt.items()}
        lhs_val = sp.simplify(lhs_expr.subs(subs))
        rhs_val = sp.simplify(rhs_expr.subs(subs))
        diff = sp.simplify(lhs_val - rhs_val)
        if relation == "<=":
            ok = bool(diff <= 0)
        elif relation == "<":
            ok = bool(diff < 0)
        elif relation == ">=":
            ok = bool(diff >= 0)
        elif relation == ">":
            ok = bool(diff > 0)
        else:
            ok = bool(diff == 0)
        reason = "" if ok else f"Violated ({lhs_str}) {relation} ({rhs_str})"
        return ok, reason, str(lhs_val), str(rhs_val)

    return run_exact_grid_falsifier(claim_id, grids, _check_pt)
