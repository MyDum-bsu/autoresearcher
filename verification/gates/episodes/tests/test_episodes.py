"""PUBLIC positive/negative controls; no evaluated candidate attempts."""

import copy
import hashlib
import itertools
import json
import subprocess
import sys
import unittest
from unittest.mock import patch

from pilot.episodes import judge
from pilot.episodes.vendor import finite_bellman as finite
from pilot.episodes.vendor import finite_reference as reference

ROOT = judge.ROOT
REPO = ROOT.parents[1]


def load(name):
    return judge.decode((ROOT / "references" / name).read_text())


def reject(test, data):
    with test.assertRaises((judge.Rejected, finite.CheckerError)):
        judge.evaluate(data)


class Episodes(unittest.TestCase):
    def test_all_public_positive_controls(self):
        for family in "MFR":
            for variant in ("reference", "alternative"):
                with self.subTest(family=family, variant=variant):
                    self.assertEqual(
                        judge.evaluate(load(f"{family}-{variant}.json"))["objective_checks"], "pass"
                    )

    def test_distinct_accepted_submissions(self):
        self.assertNotEqual(
            load("M-reference.json")["certificates"]["state"]["first_action"],
            load("M-alternative.json")["certificates"]["state"]["first_action"],
        )
        self.assertNotEqual(
            load("F-reference.json")["witness"], load("F-alternative.json")["witness"]
        )
        self.assertNotEqual(
            load("R-reference.json")["continuation"]["next_action"],
            load("R-alternative.json")["continuation"]["next_action"],
        )

    def test_independent_routes_all_inputs_and_modes(self):
        for name, instance in judge.inputs().items():
            for mode in ("state", "prefix", "open"):
                with self.subTest(name=name, mode=mode):
                    expected = reference.solve(instance, mode)
                    actual = finite.solve(instance, mode)
                    self.assertEqual(expected["value"], actual["value"])
                    finite.check_result(instance, mode, expected)
                    reference.replay(instance, mode, actual)

    def test_finite_input_set_order_invariance(self):
        # Three cases * two path orders * all first-action permutations <= 16.
        for instance in judge.inputs().values():
            for actions in itertools.permutations(instance["first_actions"]):
                for paths in (instance["paths"], list(reversed(instance["paths"]))):
                    changed = dict(instance, first_actions=list(actions), paths=paths)
                    for mode in ("state", "prefix"):
                        self.assertEqual(finite.solve(instance, mode), finite.solve(changed, mode))

    def test_M_information_and_collision_negative_controls(self):
        for field in ("state_implementable", "injective_implementable"):
            data = load("M-reference.json")
            data[field] = not data[field]
            reject(self, data)
        data = load("M-reference.json")
        data["collision"][1] = data["collision"][0]
        reject(self, data)
        data = load("M-reference.json")
        data["certificates"]["state"] = data["certificates"]["prefix"]
        reject(self, data)

    def test_F_preserve_parent_child_scope_and_no_universal_proof(self):
        mutations = [
            ("parent_outcome", "proved"),
            ("parent", "equal-nonzero-v2"),
            ("witness", "injective"),
        ]
        for field, value in mutations:
            data = load("F-reference.json")
            data[field] = value
            reject(self, data)
        for field, value in [
            ("outcome", "proved"),
            ("case", "hidden"),
            ("restriction", "all"),
            ("parent", "missing-parent"),
        ]:
            data = load("F-reference.json")
            data["child"][field] = value
            reject(self, data)

    def test_certificate_tampering_and_valid_wrong_input(self):
        data = load("F-reference.json")
        data["certificates"]["prefix"]["value"] = "7/1"
        reject(self, data)
        data = load("F-reference.json")
        other = dict(judge.inputs()["hidden"], prefix_gain="1/1")
        # Fully valid certificates plus their own correct hashes cannot replace trusted inputs.
        data["certificates"] = {m: reference.solve(other, m) for m in ("state", "prefix")}
        reject(self, data)
        data = load("F-reference.json")
        data["certificates"]["state"]["normalized_input_sha256"] = "0" * 64
        reject(self, data)

    def test_R_stages_continuation_and_alternative_relation(self):
        for field, value in [
            ("parent_outcome", "proved"),
            ("child_outcome", "proved"),
            ("depends_on", []),
            ("human_review", "approved"),
            ("obligation", "source-assumptions"),
        ]:
            data = load("R-reference.json")
            data["continuation"][field] = value
            reject(self, data)
        data = load("R-reference.json")
        data["stages"].reverse()
        reject(self, data)
        data = load("R-reference.json")
        data["stages"][0]["decision"] = "continue-parent-proof"
        reject(self, data)
        data = load("R-reference.json")
        data["continuation"]["consequences"]["negative"] = "prepare-human-review"
        reject(self, data)

    def test_closed_schema_strict_versions_identifiers(self):
        for family in "MFPR":
            base = load(f"{family}-reference.json")
            for key, value in [
                ("schema_version", True),
                ("episode", family + "\n"),
                ("episode", "../M"),
                ("unknown", "x"),
            ]:
                data = copy.deepcopy(base)
                data[key] = value
                reject(self, data)
        with self.assertRaises(judge.Rejected):
            judge.decode('{"episode":"M","episode":"F"}')
        with self.assertRaises(judge.Rejected):
            judge.decode('{"schema_version":1.0}')

    def test_P_reference_compiles_and_axioms_are_allowed(self):
        for variant in ("reference", "alternative"):
            result = judge.evaluate(load(f"P-{variant}.json"))
            self.assertEqual(result["objective_checks"], "pass")
            self.assertLessEqual(
                set(result["axioms"]), {"Classical.choice", "propext", "Quot.sound"}
            )
            self.assertEqual(result["human_review"], "pending")
        self.assertNotEqual(load("P-reference.json")["proof"], load("P-alternative.json")["proof"])

    def test_P_wrong_statement_unsupported_axiom_and_wrong_proof(self):
        data = load("P-reference.json")
        data["target"] = "True"
        reject(self, data)
        for proof in ("  axiom magic : False\n  exact False.elim magic", "  sorry", "  trivial"):
            data = load("P-reference.json")
            data["proof"] = proof
            reject(self, data)

    def test_P_transitive_axiom_and_missing_inventory_controls(self):
        version = subprocess.CompletedProcess([], 0, "Lean (version 4.35.0-rc2, test)", "")
        for report in (
            "'observation_factorization' depends on axioms: [evil]\n",
            "",
            "'other' depends on axioms: []\n",
        ):
            compiled = subprocess.CompletedProcess([], 0, report, "")
            with patch.object(judge.subprocess, "run", side_effect=[version, compiled]):
                reject(self, load("P-reference.json"))

    def test_two_fresh_processes_each_family(self):
        for family in "MFPR":
            command = [
                sys.executable,
                "-B",
                "-m",
                "pilot.episodes.judge",
                "--input",
                str(ROOT / "references" / f"{family}-reference.json"),
            ]
            first = subprocess.run(command, cwd=REPO, capture_output=True, timeout=60, check=True)
            second = subprocess.run(command, cwd=REPO, capture_output=True, timeout=60, check=True)
            self.assertEqual(first.stdout, second.stdout)
            self.assertEqual(first.stderr, b"")
            self.assertEqual(second.stderr, b"")

    def test_negative_cli_has_no_pass_packet(self):
        command = [
            sys.executable,
            "-B",
            "-m",
            "pilot.episodes.judge",
            "--input",
            str(ROOT / "controls" / "M-wrong-information.json"),
        ]
        result = subprocess.run(command, cwd=REPO, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["objective_checks"], "rejected")

    def test_all_stored_negative_controls(self):
        for path in sorted((ROOT / "controls").glob("*.json")):
            with self.subTest(control=path.name):
                reject(self, judge.decode(path.read_text()))

    def test_frozen_inventory_integrity(self):
        judge.integrity()
        identities = json.loads((ROOT / "reference-identities.json").read_text())
        for name, digest in identities.items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
