"""Unit tests for exact_lp, T1-T7 falsification battery, and SymPy counterexample template."""

from __future__ import annotations

import unittest
from fractions import Fraction

import sympy as sp

from verification.falsifiers.battery_t1_t7 import (
    _solve_t2_temporal_network,
    evaluate_conjecture,
    run_battery,
)
from verification.falsifiers.sympy_counterexample_template import (
    EmptyGridError,
    InvalidGridValueError,
    evaluate_sympy_relation_claim,
    load_exact_json,
    run_exact_grid_falsifier,
    sympy_inequality_holds,
    validate_grids,
)
from verification.oracles.exact_lp import ExactLPError, solve_exact_lp


class TestExactLP(unittest.TestCase):
    def test_simple_bounded_lp(self) -> None:
        # min -x - 2y s.t. x + y <= 4, x <= 2, y <= 3, x,y >= 0 -> opt at (1, 3), val = -7
        res = solve_exact_lp(
            [-1, -2],
            A_ub=[[1, 1], [1, 0], [0, 1]],
            b_ub=[4, 2, 3],
        )
        self.assertEqual(res.status, "optimal")
        self.assertEqual(res.objective, Fraction(-7))
        self.assertEqual(res.x, (Fraction(1), Fraction(3)))

    def test_equality_and_free_variables(self) -> None:
        # min t s.t. t >= x, t >= -x, x == -3/2  -> t = 3/2
        res = solve_exact_lp(
            [1, 0],
            A_ub=[[-1, 1], [-1, -1]],
            b_ub=[0, 0],
            A_eq=[[0, 1]],
            b_eq=[Fraction(-3, 2)],
            free_vars=[0, 1],
        )
        self.assertEqual(res.status, "optimal")
        self.assertEqual(res.objective, Fraction(3, 2))
        self.assertEqual(res.x, (Fraction(3, 2), Fraction(-3, 2)))

    def test_infeasible_and_unbounded_lp(self) -> None:
        inf = solve_exact_lp([1], A_ub=[[1], [-1]], b_ub=[1, -2])
        self.assertEqual(inf.status, "infeasible")
        self.assertIsNone(inf.objective)

        unb = solve_exact_lp([-1], A_ub=[[-1]], b_ub=[0])
        self.assertEqual(unb.status, "unbounded")
        self.assertIsNone(unb.objective)

    def test_rejects_float_or_empty_c(self) -> None:
        with self.assertRaises(ExactLPError):
            solve_exact_lp([])
        with self.assertRaises(ExactLPError):
            solve_exact_lp([1.5])  # type: ignore[list-item]


class TestBatteryT1T7(unittest.TestCase):
    def test_all_seven_cases_pass_exact_ground_truth(self) -> None:
        cases = run_battery()
        self.assertEqual(len(cases), 7)
        self.assertEqual([c.case_id for c in cases], ["T1", "T2", "T3", "T4", "T5", "T6", "T7"])
        for case in cases:
            self.assertTrue(case.passed, f"{case.case_id} failed: {case}")
            self.assertEqual(case.observed_verdict, case.expected_verdict)

    def test_evaluate_conjecture_falsifies_naive_rules(self) -> None:
        cases = run_battery()
        # A naive conjecture claiming "all fixed-recourse problems are exact" fails T2-T5
        res_all = evaluate_conjecture(lambda _c: "exact", cases)
        self.assertFalse(res_all["survived"])
        self.assertEqual(
            [m["case_id"] for m in res_all["mismatches"]],
            ["T2", "T3", "T4", "T5"],
        )

        # A perfect classifier matching ground truth survives
        res_ok = evaluate_conjecture(lambda c: c.expected_verdict, cases)
        self.assertTrue(res_ok["survived"])
        self.assertEqual(res_ok["mismatches"], [])

    def test_t2_full_matrix_adr_separation_scales_with_s(self) -> None:
        # Full unrestricted matrix Y in R^{s x s} on Euclidean ball B_2^s:
        # V_ADR = s strictly exceeds V_ARO = (s + sqrt(s)) / 2 for s = 2, 3, 4.
        for s in (2, 3, 4):
            v_aro, v_adr, gap = _solve_t2_temporal_network(s)
            self.assertEqual(v_adr, Fraction(s))
            self.assertEqual(sp.simplify(v_aro - (s + sp.sqrt(s)) / 2), 0)
            self.assertGreater(float(gap.evalf()), 0.0)


class TestSymPyCounterexampleTemplate(unittest.TestCase):
    def test_rejects_empty_and_invalid_grids(self) -> None:
        for bad in ([], [{}], [{"a": []}]):
            with self.assertRaises(EmptyGridError):
                validate_grids(bad)
        for bad_val in (
            [{"x": [None]}],
            [{"x": [True]}],
            [{"x": [False]}],
            [{"x": [""]}],
            [{"x": ["NaN"]}],
            [{"x": ["inf"]}],
            [{"x": [float("nan")]}],
            [{"x": [float("inf")]}],
            [{"x": [{}]}],
        ):
            with self.assertRaises(InvalidGridValueError):
                validate_grids(bad_val)
        with self.assertRaises(EmptyGridError):
            run_exact_grid_falsifier("c-empty", [], lambda _pt: (True, "", "0", "0"))

    def test_evaluate_sympy_relation_claim(self) -> None:
        rep_fail = evaluate_sympy_relation_claim(
            "bad-claim", [{"x": [1, 2], "y": [1, 2]}], "x + y", "x * y", "<="
        )
        self.assertFalse(rep_fail.survived)
        self.assertIsNotNone(rep_fail.counterexample)
        rep_ok = evaluate_sympy_relation_claim(
            "good-claim",
            [{"a": [-2, 0, 3], "b": [-2, 0, 3], "z": [0, "1/2", 1]}],
            "Max((1 - z) * a + z * b, 0)",
            "(1 - z) * Max(a, 0) + z * Max(b, 0)",
            "<=",
        )
        self.assertTrue(rep_ok.survived)
        self.assertEqual(rep_ok.tested_points, 27)

    def test_exact_json_decimal_no_float64_rounding(self) -> None:
        # 9007199254740993.0 == 2^53 + 1; IEEE-754 float64 rounds it down to 9007199254740992.
        # Exact JSON parsing via parse_float=Decimal MUST falsify 9007199254740993.0 <= 2^53.
        raw_json = (
            '{"claim_id": "float64-boundary", "lhs": "x", "rhs": "9007199254740992", '
            '"relation": "<=", "grids": [{"x": [9007199254740993.0]}]}'
        )
        spec = load_exact_json(raw_json)
        rep = evaluate_sympy_relation_claim(
            spec["claim_id"], spec["grids"], spec["lhs"], spec["rhs"], spec["relation"]
        )
        self.assertFalse(rep.survived)
        self.assertIsNotNone(rep.counterexample)
        if rep.counterexample is not None:
            self.assertEqual(rep.counterexample.point, {"x": "9007199254740993"})

        # Also verify exact rationalization for decimal literals inside lhs/rhs expressions
        rep_lit = evaluate_sympy_relation_claim(
            "float64-literal",
            [{"k": [1]}],
            "9007199254740993.0 * k",
            "9007199254740992 * k",
            "<=",
        )
        self.assertFalse(rep_lit.survived)

    def test_finds_counterexample_on_false_claim_and_survives_true_claim(self) -> None:
        x, y = sp.symbols("x y", real=True)
        # False claim: x + y <= x*y on {1, 2} x {1, 2} (fails at (1, 1): 2 > 1)
        rep_fail = run_exact_grid_falsifier(
            "false-claim",
            [{"x": [1, 2], "y": [1, 2]}],
            lambda pt: (
                sympy_inequality_holds(x + y, x * y, {x: pt["x"], y: pt["y"]}),
                "x + y > x*y",
                str(pt["x"] + pt["y"]),
                str(pt["x"] * pt["y"]),
            ),
        )
        self.assertFalse(rep_fail.survived)
        if rep_fail.counterexample is None:
            self.fail("Expected non-None counterexample witness")
        self.assertEqual(rep_fail.counterexample.point, {"x": "1", "y": "1"})

        # True claim: (x - y)^2 >= 0 (i.e. 0 <= (x - y)^2)
        rep_ok = run_exact_grid_falsifier(
            "true-claim",
            [{"x": [-1, 0, "1/2"], "y": [-1, 0, "1/2"]}],
            lambda pt: (
                sympy_inequality_holds(sp.Integer(0), (x - y) ** 2, {x: pt["x"], y: pt["y"]}),
                "",
                "0",
                str((pt["x"] - pt["y"]) ** 2),
            ),
        )
        self.assertTrue(rep_ok.survived)
        self.assertEqual(rep_ok.tested_points, 9)
        self.assertIsNone(rep_ok.counterexample)


if __name__ == "__main__":
    unittest.main()
