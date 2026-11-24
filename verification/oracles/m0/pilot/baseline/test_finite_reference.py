"""Public contract tests; generated checks are bounded stdlib enumerations."""

import itertools
import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import finite_reference as ref


def instance(**changes):
    data = {
        "schema_version": 1,
        "instance_id": "test",
        "first_actions": ["-1/1", "0/1", "1/1"],
        "second_actions": ["-1/1", "0/1", "1/1"],
        "paths": [["-1/1", "0/1"], ["1/1", "0/1"]],
        "prefix_gain": "1/1",
        "terminal_interval": None,
    }
    return data | changes


class ReferenceTests(unittest.TestCase):
    def test_public_values_and_replay(self):
        expected = {
            "strict_gain": ["1/1", "0/1", "0/1"],
            "correlated_hidden_disturbance": ["1/1", "1/1", "0/1"],
            "independent_hidden_disturbance": ["1/1"] * 3,
            "terminal_feasibility": [None, "0/1", "0/1"],
        }
        for name, data in ref.public_fixtures().items():
            for mode, value in zip(ref.MODES, expected[name], strict=True):
                with self.subTest(name=name, mode=mode):
                    result = ref.solve(data, mode)
                    self.assertEqual(result["value"], value)
                    self.assertEqual(result["result"], "infeasible" if value is None else "optimal")
                    if value is None:
                        self.assertIsNone(result["first_action"])
                        self.assertEqual(result["policy"], [])
                        self.assertEqual(result["outcomes"], [])
                    else:
                        self.assertEqual(ref.replay(data, mode, result), result)
                        self.assertEqual(len(result["outcomes"]), len(data["paths"]))
                        self.assertEqual(
                            max(Fraction(o["cost"]) for o in result["outcomes"]), Fraction(value)
                        )
                        for o in result["outcomes"]:
                            self.assertEqual(abs(Fraction(o["x2"])), Fraction(o["cost"]))
                            if data["terminal_interval"]:
                                lo, hi = map(Fraction, data["terminal_interval"])
                                self.assertLessEqual(lo, Fraction(o["x2"]))
                                self.assertLessEqual(Fraction(o["x2"]), hi)

    def test_hidden_prefix_and_witness_tampering(self):
        data = ref.public_fixtures()["correlated_hidden_disturbance"]
        prefix = ref.solve(data, "prefix")
        with self.assertRaises(ref.ReferenceError):
            ref.replay(data, "state", prefix)
        prefix["information"] = "state"
        with self.assertRaises(ref.ReferenceError):
            ref.replay(data, "state", prefix)
        for field in ("action", "x2", "value", "extra", "missing"):
            witness = ref.solve(instance(), "state")
            if field == "action":
                witness["policy"][0][1] = "-1/1"
            elif field == "x2":
                witness["outcomes"][0]["x2"] = "99/1"
            elif field == "value":
                witness["value"] = "99/1"
            elif field == "extra":
                witness["policy"].append(["99/1", "0/1"])
            else:
                witness["policy"].pop()
            with self.subTest(field=field), self.assertRaises(ref.ReferenceError):
                ref.replay(instance(), "state", witness)

    def test_exact_arithmetic_bounds_and_input_dependence(self):
        data = instance(
            first_actions=["1/3"],
            second_actions=["-1/2"],
            paths=[["1/2", "1/6"]],
            prefix_gain="2/3",
        )
        result = ref.solve(data, "state")
        self.assertEqual(result["value"], "1/3")
        self.assertEqual(result["policy"], [["2/3", "-1/2"]])
        self.assertEqual(ref.replay(data, "state", result), result)
        for upper in ("0/1", "2/1"):
            data = instance(terminal_interval=["0/1", upper])
            self.assertEqual(
                ref.solve(data, "open")["result"], "infeasible" if upper == "0/1" else "optimal"
            )
        for gain in range(-2, 3):
            for mode in ref.MODES:
                data = instance(prefix_gain=f"{gain}/1")
                value = Fraction(ref.solve(data, mode)["value"])
                scaled = instance(
                    first_actions=["-2/1", "0/1", "2/1"],
                    second_actions=["-2/1", "0/1", "2/1"],
                    prefix_gain=f"{2 * gain}/1",
                )
                self.assertEqual(Fraction(ref.solve(scaled, mode)["value"]), 2 * value)

    def test_replay_constraints_and_tie_order(self):
        data = instance()
        witness = ref.solve(data, "open")
        self.assertEqual((witness["first_action"], witness["policy"]), ("-1/1", [["open", "1/1"]]))
        with self.assertRaises(ref.ReferenceError):
            ref.replay(instance(terminal_interval=["0/1", "0/1"]), "open", witness)
        witness["policy"][0][1] = "2/1"
        with self.assertRaises(ref.ReferenceError):
            ref.replay(data, "open", witness)
        edge = instance(
            first_actions=["1000/1"],
            second_actions=["1000/1"],
            paths=[["1000/1", "1000/1"]],
            prefix_gain="1000/1",
        )
        result = ref.solve(edge, "state")
        self.assertEqual(result["value"], "1003000/1")
        self.assertEqual(ref.replay(edge, "state", result), result)

    def test_set_permutations_preserve_entire_result(self):
        original = instance()
        expected = ref.solve(original, "state")
        self.assertEqual(expected["first_action"], "0/1")
        for first in itertools.permutations(original["first_actions"]):
            for paths in itertools.permutations(original["paths"]):
                data = instance(
                    first_actions=list(first),
                    paths=list(paths),
                    second_actions=list(reversed(original["second_actions"])),
                )
                self.assertEqual(ref.solve(data, "state"), expected)
                normalized = ref.parse_instance(json.dumps(data))
                self.assertEqual(ref.validate_instance(normalized), normalized)

    def test_invalid_inputs_and_scope(self):
        bad = [instance(schema_version=v) for v in (True, 1.0, 2, "1")]
        bad += [instance(extra=1), instance(instance_id=""), [], None]
        bad += [
            instance(first_actions=[x])
            for x in (
                True,
                1,
                1.0,
                "1",
                "2/2",
                "0/2",
                "-0/1",
                "+1/1",
                "01/1",
                "1/-1",
                "1/0",
                " 1/1",
                "1/1 ",
            )
        ]
        bad += [instance(**{key: []}) for key in ("first_actions", "second_actions", "paths")]
        bad += [
            instance(first_actions=["0/1", "0/1"]),
            instance(second_actions=["0/1", "0/1"]),
            instance(paths=[["0/1", "0/1"]] * 2),
            instance(paths=[["0/1"]]),
            instance(paths=[["0/1"] * 3]),
            instance(paths=[True]),
            instance(terminal_interval=["1/1", "0/1"]),
            instance(terminal_interval=["0/1"]),
        ]
        missing = instance()
        del missing["paths"]
        bad.append(missing)
        for data in bad:
            with self.subTest(data=data), self.assertRaises(ref.ReferenceError) as ctx:
                ref.solve(data, "state")
            self.assertEqual(ctx.exception.code, "invalid_input")
        for data in (
            instance(first_actions=[f"{i}/1" for i in range(6)]),
            instance(second_actions=[f"{i}/1" for i in range(6)]),
            instance(paths=[[f"{i}/1", "0/1"] for i in range(9)]),
            instance(prefix_gain="1001/1"),
            instance(prefix_gain="1/1001"),
            instance(prefix_gain="1" + "0" * 5000 + "/1"),
        ):
            with self.assertRaises(ref.ReferenceError) as ctx:
                ref.solve(data, "state")
            self.assertEqual(ctx.exception.code, "unsupported_scope")
        for text in (
            '{"schema_version":1,"schema_version":1}',
            "{",
            "NaN",
            "Infinity",
            '{"x":1e999}',
        ):
            with self.assertRaises(ref.ReferenceError):
                ref.parse_instance(text)
        with self.assertRaises(ref.ReferenceError):
            ref.solve(instance(), "feedback")

    def test_cli_and_side_effect_free_import(self):
        script = Path(ref.__file__).resolve()

        def run(*args, **kw):
            return subprocess.run(
                [sys.executable, "-B", *args], capture_output=True, timeout=20, **kw
            )

        with tempfile.TemporaryDirectory(prefix="p1-test-") as directory:
            probe = run(
                "-c",
                f"import sys; sys.path.insert(0, {str(script.parent)!r}); import finite_reference",
                cwd=directory,
            )
            self.assertEqual((probe.returncode, probe.stdout, probe.stderr), (0, b"", b""))
            self.assertEqual(list(Path(directory).iterdir()), [])
            source = Path(directory) / "input.json"
            source.write_text(json.dumps(instance()))
            result = run(str(script), "--input", str(source), "--information", "state")
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout), ref.solve(instance(), "state"))
            for text in ("{}", '{"x":1,"x":2}', json.dumps(instance(prefix_gain="1001/1"))):
                source.write_text(text)
                invalid = run(str(script), "--input", str(source), "--information", "state")
                self.assertEqual((invalid.returncode, invalid.stdout), (2, b""))
                self.assertTrue(invalid.stderr)
        first = run(str(script), "--public-fixtures")
        second = run(str(script), "--public-fixtures")
        self.assertEqual((first.returncode, second.returncode), (0, 0))
        self.assertEqual(first.stdout, second.stdout)
        self.assertTrue(first.stdout.endswith(b"\n"))
        self.assertEqual(set(json.loads(first.stdout)["cases"]), set(ref.public_fixtures()))
