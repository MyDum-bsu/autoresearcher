"""Frozen bounded software regression set; no adaptive generation or search."""

import hashlib
import json
import os
import subprocess
import sys
import unittest
from copy import deepcopy
from fractions import Fraction
from itertools import product
from pathlib import Path

from pilot.baseline.finite_reference import solve as reference_solve
from pilot.checkers import finite_bellman as checker

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "pilot/checkers/finite_bellman.py"
MODES = ("open", "state", "prefix")


def rational(value):
    number = Fraction(value)
    return f"{number.numerator}/{number.denominator}"


def instance(name, first=(0,), second=(-1, 0, 1), gain=0, paths=((-1, -1), (1, 1)), interval=None):
    return {
        "schema_version": 1,
        "instance_id": name,
        "first_actions": [rational(a) for a in first],
        "second_actions": [rational(b) for b in second],
        "prefix_gain": rational(gain),
        "paths": [[rational(p), rational(q)] for p, q in paths],
        "terminal_interval": None if interval is None else [rational(x) for x in interval],
    }


# Frozen before any execution: 3 * 3 * 4 * 4 = 144 instances, 432 mode cases.
# This is a software regression set, not a scientific evidence grid.
FROZEN_GAINS = ("-1/2", "0/1", "2/3")
FROZEN_FIRST_ACTIONS = (("0/1",), ("-1/3", "2/3"), ("1/2", "1/1"))
FROZEN_PATHS = (
    (("-1/2", "-2/3"), ("1/3", "1/2")),
    (("-1/2", "1/2"), ("1/3", "-2/3")),
    (("-1/2", "-2/3"), ("-1/2", "1/2"), ("1/3", "-2/3"), ("1/3", "1/2")),
    (("-1/2", "-2/3"), ("-1/2", "1/2"), ("1/3", "0/1")),
)
FROZEN_INTERVALS = (None, ("0/1", "0/1"), ("-1/2", "5/6"), ("1/3", "4/3"))
GENERATED = tuple(
    instance(f"frozen-{index:03d}", first=first, gain=gain, paths=paths, interval=interval)
    for index, (gain, first, paths, interval) in enumerate(
        product(FROZEN_GAINS, FROZEN_FIRST_ACTIONS, FROZEN_PATHS, FROZEN_INTERVALS)
    )
)
STRICT = instance("strict_gain", first=(-1, 0, 1), gain=1, paths=((-1, 0), (1, 0)))
CORRELATED = instance("correlated_hidden")
INDEPENDENT = instance("independent_hidden", paths=((-1, -1), (-1, 1), (1, -1), (1, 1)))
TERMINAL = instance(
    "terminal_feasibility", first=(-1, 0, 1), gain=1, paths=((-1, 0), (1, 0)), interval=(0, 0)
)
PUBLIC = (
    (STRICT, ("1/1", "0/1", "0/1")),
    (CORRELATED, ("1/1", "1/1", "0/1")),
    (INDEPENDENT, ("1/1", "1/1", "1/1")),
    (TERMINAL, (None, "0/1", "0/1")),
)
TIED = instance("nonbinding_ties", gain=1, paths=((-1, 0), (2, 0)))


def rebind(record, data, mode):
    """Forge metadata deliberately; a replay must still check the actual paths."""
    forged = deepcopy(record)
    forged["instance_id"] = data["instance_id"]
    forged["information"] = mode
    normalized = checker.validate_instance(data)
    forged["normalized_input_sha256"] = hashlib.sha256(
        checker.canonical_json(normalized).encode("utf-8")
    ).hexdigest()
    return forged


class BellmanRegression(unittest.TestCase):
    def compare(self, data, mode, expected_value="unspecified"):
        before = deepcopy(data)
        actual = checker.solve(data, mode)
        reference = reference_solve(data, mode)
        self.assertEqual(data, before)
        self.assertEqual(actual["result"], reference["result"])
        self.assertEqual(actual["value"], reference["value"])
        if expected_value != "unspecified":
            self.assertEqual(actual["value"], expected_value)
            self.assertEqual(
                actual["result"], "infeasible" if expected_value is None else "optimal"
            )
        self.assertEqual(checker.check_result(data, mode, reference), reference)
        if actual["result"] == "optimal":
            self.assertEqual(checker.check_witness(data, mode, reference), reference)
            self.assertEqual(checker.check_witness(data, mode, actual), actual)
        else:
            self.assertIsNone(actual["first_action"])
            self.assertEqual(actual["policy"], [])
            self.assertEqual(actual["outcomes"], [])
            with self.assertRaises(checker.CheckerError):
                checker.check_witness(data, mode, actual)
        return actual, reference

    def test_four_public_fixtures(self):
        for data, values in PUBLIC:
            for mode, expected in zip(MODES, values, strict=True):
                with self.subTest(case=data["instance_id"], mode=mode):
                    self.compare(data, mode, expected)

    def test_frozen_generated_regressions(self):
        self.assertEqual(len(GENERATED), 144)
        feasible = infeasible = 0
        for data in GENERATED:
            for mode in MODES:
                with self.subTest(case=data["instance_id"], mode=mode):
                    actual, _ = self.compare(data, mode)
                    if actual["result"] == "optimal":
                        feasible += 1
                    else:
                        infeasible += 1
        self.assertGreater(feasible, 0)
        self.assertGreater(infeasible, 0)

    def test_tied_witnesses_need_not_match(self):
        actual, reference = self.compare(TIED, "state", "1/1")
        self.assertNotEqual(actual["policy"], reference["policy"])
        self.assertEqual(actual["policy"], [["-1/1", "1/1"], ["2/1", "-1/1"]])
        self.assertEqual(reference["policy"], [["-1/1", "0/1"], ["2/1", "-1/1"]])
        first_tie = instance("first_tie", first=(-1, 1), second=(0,), paths=((0, 0),))
        for mode in MODES:
            with self.subTest(mode=mode):
                actual, _ = self.compare(first_tie, mode, "1/1")
                self.assertEqual(actual["first_action"], "-1/1")

    def test_normalization_and_large_computed_rationals(self):
        data = deepcopy(STRICT)
        for field in ("first_actions", "second_actions", "paths"):
            data[field].reverse()
        for mode in MODES:
            self.assertEqual(checker.solve(data, mode), checker.solve(STRICT, mode))
        edge = instance(
            "computed_unbounded", first=(1000,), second=(1000,), gain=1000, paths=((1000, 1000),)
        )
        self.compare(edge, "state", "1003000/1")

    def test_exact_noninteger_result(self):
        data = instance(
            "rational", first=("1/3",), second=("-1/2",), gain="2/3", paths=(("1/4", "2/7"),)
        )
        for mode in MODES:
            self.compare(data, mode, "2/7")

    def test_lost_prefix_correlation_mutation(self):
        # Rectangularization loses the prefix/suffix relation and raises the value.
        bad = reference_solve(INDEPENDENT, "prefix")
        self.assertEqual(bad["value"], "1/1")
        self.assertEqual(checker.solve(CORRELATED, "prefix")["value"], "0/1")
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(CORRELATED, "prefix", rebind(bad, CORRELATED, "prefix"))
        # Even a feasible replay of the resulting constant policy is not optimal.
        feasible_bad = reference_solve(CORRELATED, "open")
        feasible_bad = rebind(feasible_bad, CORRELATED, "prefix")
        feasible_bad["policy"] = [["-1/1", "0/1"], ["1/1", "0/1"]]
        self.assertEqual(checker.check_witness(CORRELATED, "prefix", feasible_bad)["value"], "1/1")
        with self.assertRaises(checker.CheckerError):
            checker.check_result(CORRELATED, "prefix", feasible_bad)

    def test_prefix_disguised_as_state_mutation(self):
        forged = rebind(reference_solve(CORRELATED, "prefix"), CORRELATED, "state")
        self.assertEqual(forged["value"], "0/1")
        self.assertEqual(checker.solve(CORRELATED, "state")["value"], "1/1")
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(CORRELATED, "state", forged)
        # Renaming both prefix cells to the sole state cannot evade nonanticipativity.
        forged["policy"] = [["0/1", "1/1"], ["0/1", "-1/1"]]
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(CORRELATED, "state", forged)
        forged["policy"] = [["0/1", "1/1"]]
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(CORRELATED, "state", forged)

    def test_missing_terminal_constraint_mutation(self):
        unconstrained = deepcopy(TERMINAL)
        unconstrained["terminal_interval"] = None
        forged = rebind(reference_solve(unconstrained, "open"), TERMINAL, "open")
        self.assertEqual(checker.solve(TERMINAL, "open")["result"], "infeasible")
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(TERMINAL, "open", forged)
        # A different first action can cover all cells even if another cannot.
        data = instance(
            "skip_infeasible_first",
            first=(-1, 0),
            second=(0,),
            gain=1,
            paths=((1, 0),),
            interval=(1, 1),
        )
        actual, _ = self.compare(data, "state", "1/1")
        self.assertEqual(actual["first_action"], "0/1")

    def test_witness_tampering(self):
        good = reference_solve(STRICT, "state")
        mutations = []
        for field, value in (
            ("schema_version", True),
            ("schema_version", 2),
            ("instance_id", "other"),
            ("information", "prefix"),
            ("normalized_input_sha256", "0" * 64),
            ("first_action", "9/1"),
            ("first_action", "0/2"),
            ("value", 0.0),
            ("value", "1/1"),
            ("result", "infeasible"),
            ("policy", {}),
            ("outcomes", []),
        ):
            bad = deepcopy(good)
            bad[field] = value
            mutations.append(bad)
        bad = deepcopy(good)
        del bad["value"]
        mutations.append(bad)
        bad = deepcopy(good)
        bad["extra"] = 0
        mutations.append(bad)
        for policy in (
            good["policy"][:-1],
            list(reversed(good["policy"])),
            good["policy"] + [good["policy"][0]],
            good["policy"] + [["99/1", "0/1"]],
            [["-1/1", "2/1"], ["1/1", "-1/1"]],
            [["-1/1", "1/1", "extra"]],
            [[[], "0/1"]],
        ):
            bad = deepcopy(good)
            bad["policy"] = policy
            mutations.append(bad)
        for field in ("path", "x1", "x2", "cost"):
            bad = deepcopy(good)
            bad["outcomes"][0][field] = ["0/1", "0/1"] if field == "path" else "99/1"
            mutations.append(bad)
        bad = deepcopy(good)
        bad["outcomes"].reverse()
        mutations.append(bad)
        bad = deepcopy(good)
        bad["outcomes"][0]["extra"] = "0/1"
        mutations.append(bad)
        for index, bad in enumerate(mutations):
            with self.subTest(mutation=index), self.assertRaises(checker.CheckerError):
                checker.check_witness(STRICT, "state", bad)
        # Binding includes inputs even when instance_id stays fixed.
        changed = deepcopy(STRICT)
        changed["prefix_gain"] = "0/1"
        with self.assertRaises(checker.CheckerError):
            checker.check_witness(changed, "state", good)

    def test_false_and_malformed_infeasibility(self):
        good = checker.solve(TERMINAL, "open")
        self.assertEqual(checker.check_result(TERMINAL, "open", good), good)
        with self.assertRaises(checker.CheckerError):
            checker.check_result(STRICT, "open", rebind(good, STRICT, "open"))
        for field, value in (
            ("value", "0/1"),
            ("first_action", "0/1"),
            ("policy", [["open", "0/1"]]),
            ("outcomes", [{}]),
            ("schema_version", True),
            ("information", "state"),
        ):
            bad = deepcopy(good)
            bad[field] = value
            with self.subTest(field=field), self.assertRaises(checker.CheckerError):
                checker.check_result(TERMINAL, "open", bad)


class ValidationAndCLI(unittest.TestCase):
    def test_input_validation(self):
        bad_inputs = [None, [], {}]
        for field, value in (
            ("schema_version", True),
            ("schema_version", 1.0),
            ("schema_version", 2),
            ("instance_id", ""),
            ("instance_id", 3),
            ("first_actions", []),
            ("second_actions", "0/1"),
            ("paths", []),
            ("paths", [["0/1"]]),
            ("paths", [["0/1", "0/1", "0/1"]]),
            ("terminal_interval", ["1/1", "-1/1"]),
            ("terminal_interval", []),
            ("terminal_interval", "0/1"),
        ):
            bad = deepcopy(STRICT)
            bad[field] = value
            bad_inputs.append(bad)
        for rational_value in (
            True,
            0,
            0.5,
            "0",
            "1/2 ",
            "+1/2",
            "01/2",
            "1/02",
            "-0/1",
            "0/2",
            "2/4",
            "1/-2",
            "1/0",
            "١/2",
            "1/1\n",
        ):
            bad = deepcopy(STRICT)
            bad["prefix_gain"] = rational_value
            bad_inputs.append(bad)
        for field in ("paths", "first_actions", "second_actions"):
            bad = deepcopy(STRICT)
            bad[field].append(deepcopy(bad[field][0]))
            bad_inputs.append(bad)
        missing = deepcopy(STRICT)
        del missing["terminal_interval"]
        bad_inputs.extend((missing, dict(STRICT, extra=0)))
        for index, bad in enumerate(bad_inputs):
            with self.subTest(index=index), self.assertRaises(checker.CheckerError) as caught:
                checker.solve(bad, "state")
            self.assertEqual(caught.exception.code, "invalid_input")
        for mode in (None, "STATE", "history", [], 1):
            with self.subTest(mode=mode), self.assertRaises(checker.CheckerError):
                checker.solve(STRICT, mode)
        for text in (
            '{"schema_version":1,"schema_version":1}',
            '{"a":NaN}',
            '{"a":Infinity}',
            '{"a":1.0}',
            '{"a":1e0}',
            "{",
        ):
            with self.subTest(text=text), self.assertRaises(checker.CheckerError):
                checker.parse_instance(text)
        self.assertEqual(
            checker.parse_instance(json.dumps(STRICT)), checker.validate_instance(STRICT)
        )

    def test_json_decoder_errors_are_invalid_input(self):
        cases = (
            ('{"schema_version":' + "9" * 5000 + "}", ValueError),
            ("[" * 10000 + "0" + "]" * 10000, RecursionError),
        )
        for text, cause_type in cases:
            with self.subTest(cause=cause_type.__name__):
                with self.assertRaises(checker.CheckerError) as caught:
                    checker.parse_instance(text)
                self.assertEqual(caught.exception.code, "invalid_input")
                self.assertIsInstance(caught.exception.__cause__, cause_type)
                self.assertNotIsInstance(caught.exception.__cause__, checker.CheckerError)

    def test_json_hook_errors_are_not_wrapped(self):
        for text, message in (
            ('{"a":1,"a":2}', "Duplicate JSON key"),
            ('{"a":1.0}', "Noninteger JSON number is forbidden"),
            ('{"a":NaN}', "Noninteger JSON number is forbidden"),
        ):
            with self.subTest(text=text):
                with self.assertRaises(checker.CheckerError) as caught:
                    checker.parse_instance(text)
                self.assertEqual(caught.exception.code, "invalid_input")
                self.assertEqual(str(caught.exception), message)
                self.assertIsNone(caught.exception.__cause__)

    def test_cli_json_decoder_errors_are_invalid_input(self):
        for text in ('{"schema_version":' + "9" * 5000 + "}", "[" * 10000 + "0" + "]" * 10000):
            for optimized in (False, True):
                with self.subTest(nesting=text.startswith("["), optimized=optimized):
                    run = self.run_cli(text.encode(), optimized=optimized)
                    self.assertEqual(run.returncode, 2)
                    self.assertEqual(run.stdout, b"")
                    self.assertIn(b"invalid_input", run.stderr)
                    self.assertNotIn(b"Traceback", run.stderr)

    def test_scope_limits_are_not_infeasibility(self):
        cases = (
            dict(STRICT, first_actions=[rational(x) for x in range(6)]),
            dict(STRICT, second_actions=[rational(x) for x in range(6)]),
            dict(STRICT, paths=[[rational(x), "0/1"] for x in range(9)]),
            dict(STRICT, prefix_gain="1001/1"),
            dict(STRICT, prefix_gain="1/1001"),
            dict(STRICT, terminal_interval=["-1001/1", "0/1"]),
        )
        for data in cases:
            with self.subTest(data=data), self.assertRaises(checker.CheckerError) as caught:
                checker.solve(data, "state")
            self.assertEqual(caught.exception.code, "unsupported_scope")
            with self.assertRaises(checker.CheckerError):
                checker.check_witness(data, "state", reference_solve(STRICT, "state"))

    def run_cli(self, payload, mode="state", optimized=False, path="/dev/stdin"):
        command = [sys.executable] + (["-O"] if optimized else [])
        command += [str(CLI), "--input", str(path), "--information", mode]
        return subprocess.run(
            command,
            cwd=ROOT,
            input=payload,
            capture_output=True,
            timeout=5,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )

    def test_cli_and_byte_determinism(self):
        # Linux /dev/stdin exercises the file CLI without writing input artifacts.
        for data, _ in PUBLIC:
            payload = json.dumps(data).encode("utf-8")
            for mode in MODES:
                with self.subTest(case=data["instance_id"], mode=mode):
                    first = self.run_cli(payload, mode)
                    second = self.run_cli(payload, mode)
                    optimized = self.run_cli(payload, mode, optimized=True)
                    for run in (first, second, optimized):
                        self.assertEqual(run.returncode, 0, run.stderr)
                        self.assertEqual(run.stderr, b"")
                    self.assertEqual(first.stdout, second.stdout)
                    self.assertEqual(first.stdout, optimized.stdout)
                    expected = (checker.canonical_json(checker.solve(data, mode)) + "\n").encode(
                        "utf-8"
                    )
                    self.assertEqual(first.stdout, expected)
                    self.assertEqual(first.stdout.count(b"\n"), 1)
        for payload, code in (
            (b"{", "invalid_input"),
            (json.dumps(dict(STRICT, prefix_gain="1001/1")).encode(), "unsupported_scope"),
        ):
            for optimized in (False, True):
                run = self.run_cli(payload, optimized=optimized)
                self.assertEqual(run.returncode, 2)
                self.assertEqual(run.stdout, b"")
                self.assertIn(code.encode(), run.stderr)
        run = self.run_cli(b"\xff")
        self.assertEqual(run.returncode, 2)
        self.assertIn(b"input_io_error", run.stderr)
        run = self.run_cli(b"", path=CLI.parent / "missing-input.json")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b"")
        self.assertIn(b"input_io_error", run.stderr)
        run = self.run_cli(b"", mode="history")
        self.assertEqual(run.returncode, 2)
        self.assertEqual(run.stdout, b"")


if __name__ == "__main__":
    unittest.main()
