"""Exact numerical, mutation and subprocess determinism checks for P2b."""

import copy
import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

import a4_check as checker

ROOT = Path(__file__).resolve().parents[2]
PRODUCER = ROOT / "pilot/baseline/a4_certificate.py"
VERIFIER = ROOT / "pilot/checkers/a4_check.py"
NAMES = ("a4_printed", "a4_reconstructed_decimal")
EXPECTED_DISPLAYS = ("1.495710098124", "1.501101989382")


def run_cli(script, *args, cwd=ROOT):
    flags = ["-O"] if sys.flags.optimize else []
    return subprocess.run(
        [sys.executable, "-B", *flags, str(script), *map(str, args)],
        cwd=cwd,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )


def forward(manifest, controls, disturbances=None):
    """Test-side chronological recurrence, also replaying extremal disturbance paths."""
    model = manifest["dynamics"]
    a = [list(map(F, row)) for row in model["A"]]
    b, e = list(map(F, model["B"])), list(map(F, model["E"]))
    x, y = map(F, model["x0"])
    if disturbances is None:
        disturbances = [F(0)] * model["horizon"]
    for u, w in zip(controls, disturbances, strict=True):
        old_x, old_y = x, y
        x = a[0][0] * old_x + a[0][1] * old_y + b[0] * u + e[0] * w
        y = a[1][0] * old_x + a[1][1] * old_y + b[1] * u + e[1] * w
    return x, y


class A4CheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate once per dataset; reuse these objects only via deepcopy for mutations.
        cls.manifests, cls.certificates, cls.generated_bytes, cls.records = {}, {}, {}, {}
        for name in NAMES:
            path = ROOT / f"pilot/inputs/{name}.json"
            manifest = checker.parse_json(path.read_text(encoding="utf-8"))
            process = run_cli(PRODUCER, "--input", path)
            if process.returncode != 0 or process.stderr:
                raise RuntimeError(f"Certificate generation failed: {process.stderr}")
            certificate = checker.parse_json(process.stdout)
            cls.manifests[name] = manifest
            cls.certificates[name] = certificate
            cls.generated_bytes[name] = process.stdout
            cls.records[name] = checker.check_certificate(manifest, certificate)

    def test_exact_primal_dual_and_decimal_regressions_both_datasets(self):
        for name, display in zip(NAMES, EXPECTED_DISPLAYS, strict=True):
            with self.subTest(dataset=name):
                m, c, r = self.manifests[name], self.certificates[name], self.records[name]
                controls = list(map(F, c["controls"]))
                nominal = forward(m, controls)
                self.assertEqual(tuple(map(F, r["nominal_terminal"])), nominal)
                self.assertEqual(nominal[1] - F(r["support"]["y"]), F(r["exact_reward"]))
                self.assertEqual(F(r["exact_reward"]), F(c["objective"]))
                self.assertEqual(F(r["exact_reward"]), F(r["dual_upper_bound"]))
                self.assertEqual(r["source_page_verification"], "not_performed_by_numeric_checker")
                for multiplier in c["multipliers"].values():
                    self.assertGreaterEqual(F(multiplier), 0)
                with localcontext() as ctx:
                    ctx.prec = 40
                    q = F(r["exact_reward"])
                    self.assertEqual(
                        format(Decimal(q.numerator) / Decimal(q.denominator), ".12f"), display
                    )

    def test_robust_both_bounds_and_reward_attained_by_independent_paths(self):
        for name in NAMES:
            with self.subTest(dataset=name):
                m, c, r = self.manifests[name], self.certificates[name], self.records[name]
                model = m["dynamics"]
                matrix = [list(map(F, row)) for row in model["A"]]
                columns, _ = checker._effects(matrix, list(map(F, model["E"])), (F(0), F(0)), 120)
                controls = list(map(F, c["controls"]))

                # Three separate realizable paths: x min, x max and y min need not coincide.
                def sign(q):
                    return F(1) if q >= 0 else F(-1)

                x_min = forward(m, controls, [-sign(cx) / 2 for cx, _ in columns])[0]
                x_max = forward(m, controls, [sign(cx) / 2 for cx, _ in columns])[0]
                y_min = forward(m, controls, [-sign(cy) / 2 for _, cy in columns])[1]
                self.assertEqual([x_min, x_max], list(map(F, r["robust_terminal_x"])))
                self.assertGreaterEqual(x_min, 2)
                self.assertLessEqual(x_max, 10)
                self.assertEqual(x_min, 2)
                self.assertEqual(y_min, F(r["exact_reward"]))

    def test_chronological_indices_and_reversed_order_rejected(self):
        for name in NAMES:
            m = self.manifests[name]
            controls = list(map(F, self.certificates[name]["controls"]))
            audit = checker.evaluate_dynamics(m["dynamics"], controls, F(1, 2))
            self.assertEqual(audit["columns"][-1], tuple(map(F, m["dynamics"]["B"])))
            self.assertEqual(audit["nominal"], forward(m, controls))
            self.assertNotEqual(forward(m, controls), forward(m, controls[::-1]))
            c = copy.deepcopy(self.certificates[name])
            c["controls"].reverse()
            with self.assertRaises(checker.CheckError):
                checker.check_certificate(m, c)

    def test_terminal_violations_checked_before_objective(self):
        for name in NAMES:
            m = self.manifests[name]
            audit = checker.evaluate_dynamics(m["dynamics"], [F(0)] * 120, F(1, 2))
            for direction, message in ((-1, "lower terminal"), (1, "upper terminal")):
                c = copy.deepcopy(self.certificates[name])
                c["controls"] = [
                    f"{direction if cx >= 0 else -direction}/1" for cx, _ in audit["columns"]
                ]
                with (
                    self.subTest(dataset=name, direction=direction),
                    self.assertRaisesRegex(checker.CheckError, message),
                ):
                    checker.check_certificate(m, c)

    def test_certificate_numeric_and_binding_tampering(self):
        mutations = [
            ("objective", None, "0/1"),
            ("support", "x", "0/1"),
            ("support", "y", "0/1"),
            ("multipliers", "lower", "-1/1"),
            ("multipliers", "upper", "-1/1"),
            ("multipliers", "lower", "0/1"),
            ("multipliers", "upper", "1/1"),
            ("coefficient_set_id", None, "unknown"),
            ("input_sha256", None, "0" * 64),
            ("scope", None, "a4_r80"),
            ("coverage", None, "vertices_only"),
            ("method", None, "unregistered"),
            ("arithmetic", None, "float"),
            ("schema_version", None, True),
            ("certificate_type", None, "project_status"),
            ("controls", 0, "2/1"),
            ("controls", 32, "0/1"),
            ("controls", 0, "0/1"),
        ]
        for name in NAMES:
            for field, key, value in mutations:
                c = copy.deepcopy(self.certificates[name])
                if key is None:
                    c[field] = value
                else:
                    c[field][key] = value
                with (
                    self.subTest(dataset=name, field=field, key=key, value=value),
                    self.assertRaises(checker.CheckError),
                ):
                    checker.check_certificate(self.manifests[name], c)

    def test_feasible_suboptimal_control_with_honest_reward_fails_dual_check(self):
        for name in NAMES:
            m, c = self.manifests[name], copy.deepcopy(self.certificates[name])
            controls = list(map(F, c["controls"]))
            audit = checker.evaluate_dynamics(m["dynamics"], controls, F(1, 2))
            pivot = next(t for t, u in enumerate(controls) if abs(u) < 1)
            cx = audit["columns"][pivot][0]
            step = min(F(1, 10000), (1 - abs(controls[pivot])) / 2)
            controls[pivot] += step if cx > 0 else -step
            changed = checker.evaluate_dynamics(m["dynamics"], controls, F(1, 2))
            self.assertGreaterEqual(changed["nominal"][0] - changed["support"][0], 2)
            self.assertLessEqual(changed["nominal"][0] + changed["support"][0], 10)
            self.assertLess(changed["reward"], audit["reward"])
            c["controls"] = [f"{u.numerator}/{u.denominator}" for u in controls]
            q = changed["reward"]
            c["objective"] = f"{q.numerator}/{q.denominator}"
            with self.assertRaisesRegex(checker.CheckError, "valid dual upper bound"):
                checker.check_certificate(m, c)

    def test_input_data_schema_source_and_identity_tampering(self):
        for name in NAMES:
            for mutation in (
                "A",
                "E",
                "B",
                "x0",
                "horizon",
                "terminal",
                "terminal_lower",
                "identity",
                "source",
                "scope",
                "extra",
                "bool",
            ):
                m = copy.deepcopy(self.manifests[name])
                if mutation == "A":
                    m["dynamics"]["A"][0][0] = "1/1"
                elif mutation in ("E", "B", "x0"):
                    m["dynamics"][mutation][0] = "0/1"
                    if mutation == "x0":
                        m["dynamics"][mutation][1] = "0/1"
                elif mutation == "horizon":
                    m["dynamics"]["horizon"] = 119
                elif mutation == "terminal":
                    m["constraints"]["terminal_x_interval"][1] = "11/1"
                elif mutation == "terminal_lower":
                    m["constraints"]["terminal_x_interval"][0] = "1/1"
                elif mutation == "identity":
                    m["coefficient_set_id"] = "unknown"
                elif mutation == "source":
                    m["source_anchors"][0]["file"] = "other.pdf"
                elif mutation == "scope":
                    m["scope"] = "r80"
                elif mutation == "bool":
                    m["schema_version"] = True
                else:
                    m["unknown"] = "0/1"
                c = copy.deepcopy(self.certificates[name])
                # Even rebinding the supplied digest cannot authorize a changed instance.
                c["input_sha256"] = hashlib.sha256(checker.canonical_json(m).encode()).hexdigest()
                with (
                    self.subTest(dataset=name, mutation=mutation),
                    self.assertRaises(checker.CheckError),
                ):
                    checker.check_certificate(m, c)

    def test_reconstructed_certificate_mislabeled_as_printed(self):
        c = copy.deepcopy(self.certificates[NAMES[1]])
        c["coefficient_set_id"] = NAMES[0]
        c["input_sha256"] = self.certificates[NAMES[0]]["input_sha256"]
        with self.assertRaises(checker.CheckError):
            checker.check_certificate(self.manifests[NAMES[0]], c)
        m = copy.deepcopy(self.manifests[NAMES[1]])
        m["coefficient_set_id"] = NAMES[0]
        with self.assertRaises(checker.CheckError):
            checker.check_certificate(m, c)

    def test_empty_malformed_and_noncanonical_certificates(self):
        m = self.manifests[NAMES[0]]
        for c in (None, {}, [], "", {**self.certificates[NAMES[0]], "extra": 1}):
            with self.assertRaises(checker.CheckError):
                checker.check_certificate(m, c)
        for field, value in (
            ("controls", []),
            ("controls", ["0/1"] * 119),
            ("support", {}),
            ("multipliers", []),
            ("objective", "2/2"),
            ("objective", "01/1"),
            ("objective", "-0/1"),
            ("objective", "1/0"),
            ("objective", "1.5"),
            ("objective", 1),
            ("objective", "Infinity"),
            ("objective", "1/-2"),
        ):
            c = copy.deepcopy(self.certificates[NAMES[0]])
            c[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(checker.CheckError):
                checker.check_certificate(m, c)
        for text in ("", "{", '{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}', '{"x":0.5}'):
            with self.assertRaises(checker.CheckError):
                checker.parse_json(text)

    def test_small_perturbations_recompute_dynamics_not_stored_values(self):
        m, c = self.manifests[NAMES[0]], self.certificates[NAMES[0]]
        controls = list(map(F, c["controls"]))
        baseline = checker.evaluate_dynamics(m["dynamics"], controls, F(1, 2))
        for parameter in ("A", "E"):
            d = copy.deepcopy(m["dynamics"])
            if parameter == "A":
                d["A"][0][0] = "995001/1000000"
            else:
                d["E"][0] = "5001/1000000"
            computed = checker.evaluate_dynamics(d, controls, F(1, 2))
            changed = copy.deepcopy(m)
            changed["dynamics"] = d
            self.assertEqual(computed["nominal"], forward(changed, controls))
            self.assertNotEqual(computed["reward"], baseline["reward"])
            self.assertNotEqual(computed["support"], baseline["support"])

    def test_separate_process_generation_and_checking_are_byte_identical(self):
        # The first producer ran in setUpClass. A second independent process must match.
        with tempfile.TemporaryDirectory(prefix=".p2b-test-", dir=ROOT) as tmp:
            certificate_path = Path(tmp) / "certificate.json"
            for name in NAMES:
                path = ROOT / f"pilot/inputs/{name}.json"
                generated = run_cli(PRODUCER, "--input", path)
                self.assertEqual(generated.returncode, 0, generated.stderr)
                self.assertEqual(generated.stdout, self.generated_bytes[name])
                self.assertEqual(generated.stderr, "")
                certificate_path.write_text(generated.stdout, encoding="utf-8")
                first = run_cli(
                    VERIFIER, "--input", path, "--certificate", certificate_path, cwd=tmp
                )
                second = run_cli(
                    VERIFIER, "--input", path, "--certificate", certificate_path, cwd=tmp
                )
                self.assertEqual(first.returncode, 0, first.stderr)
                self.assertEqual(second.returncode, 0, second.stderr)
                self.assertEqual(first.stderr + second.stderr, "")
                self.assertEqual(first.stdout, second.stdout)
                self.assertEqual(first.stdout, checker.canonical_json(self.records[name]) + "\n")
                self.assertEqual(
                    generated.stdout, checker.canonical_json(self.certificates[name]) + "\n"
                )

    def test_cli_invalid_inputs_have_nonzero_and_no_success_output(self):
        with tempfile.TemporaryDirectory(prefix=".p2b-test-", dir=ROOT) as tmp:
            cert_path, manifest_path = Path(tmp) / "cert.json", Path(tmp) / "input.json"
            path = ROOT / "pilot/inputs/a4_printed.json"
            for text in (
                "",
                "{}",
                "{",
                '{"x":NaN}',
                '{"x":1,"x":2}',
                checker.canonical_json({**self.certificates[NAMES[0]], "objective": "0/1"}),
            ):
                cert_path.write_text(text, encoding="utf-8")
                result = run_cli(VERIFIER, "--input", path, "--certificate", cert_path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr.startswith("a4_check:"))
            cert_path.write_text(self.generated_bytes[NAMES[0]], encoding="utf-8")
            manifest_path.write_text('{"coefficient_set_id":"a4_printed"}', encoding="utf-8")
            for script, args in ((PRODUCER, []), (VERIFIER, ["--certificate", cert_path])):
                result = run_cli(script, "--input", manifest_path, *args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertTrue(result.stderr)

    def test_verifier_has_no_producer_or_legacy_import(self):
        # Numeric independence is structural as well as separate-process execution.
        import ast

        tree = ast.parse(VERIFIER.read_text(encoding="utf-8"))
        roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots.update(alias.name.split(".")[0] for alias in node.names)
            if isinstance(node, ast.ImportFrom):
                roots.add((node.module or "").split(".")[0])
        self.assertEqual(
            roots - {"argparse", "fractions", "hashlib", "json", "pathlib", "re", "sys"}, set()
        )
        self.assertFalse(any(isinstance(node, ast.Assert) for node in ast.walk(tree)))


if __name__ == "__main__":
    unittest.main()
