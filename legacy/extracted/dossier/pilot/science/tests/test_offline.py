"""Public bounded regression/mutation checks; no scientific search or holdout claim."""

import copy
import hashlib
import itertools
import json
import os
import subprocess
import sys
import unittest
from dataclasses import FrozenInstanceError, asdict
from unittest.mock import patch

from pilot.checkers.finite_bellman import CheckerError
from pilot.science.contracts import ContractError, canonical, digest, parse
from pilot.science.finite import ROOT, snapshot_integrity
from pilot.science.packet import build, markdown

FIXTURE = ROOT / "pilot/examples/offline-dossier-v1.json"


def example():
    return json.loads(FIXTURE.read_text())


def packet(data):
    return build(parse(canonical(data)))


def rebind(data, index):
    claim = data["claims"][index]
    identity = digest(claim)
    for section in ("evidence", "actions"):
        for item in data[section]:
            if item["claim"] == claim["id"]:
                item["claim_sha256"] = identity


class OfflineTests(unittest.TestCase):
    def reject(self, data):
        with self.assertRaises((ContractError, CheckerError)):
            packet(data)

    def test_example_outcomes(self):
        result = packet(example())
        self.assertEqual(
            [item["scientific_outcome"] for item in result["attempt_results"]],
            ["checked-counterexample", "survived-finite-inventory"] + ["none"] * 4,
        )
        self.assertEqual(result["checked_evidence"][0]["values"], ("1/1", "0/1"))
        self.assertEqual(result["checked_evidence"][1]["values"], ("0/1", "0/1"))
        self.assertFalse(result["scientific_status_change"])
        self.assertEqual(result["human_attestation"], "absent")
        self.assertIn("Finite survival is not universal proof", markdown(result))

    def test_recomputed_certificates_cannot_change_frozen_case(self):
        from pilot.checkers.finite_bellman import solve

        data = example()
        instance = data["instances"][1]
        instance["prefix_gain"] = "2/1"
        data["evidence"][1]["certificates"] = [
            solve(instance, mode) for mode in ("state", "prefix")
        ]
        self.assertEqual(
            [item["value"] for item in data["evidence"][1]["certificates"]],
            ["1/1", "1/1"],
        )
        with self.assertRaisesRegex(ContractError, "inventory input identity"):
            packet(data)

    def test_claim_identifier_cannot_inject_attestation_heading(self):
        data = example()
        old = data["claims"][1]["id"]
        injected = old + "\n\n# Human attestation: approved"
        data["claims"][1]["id"] = injected
        for section in ("evidence", "actions"):
            for item in data[section]:
                if item["claim"] == old:
                    item["claim"] = injected
        rebind(data, 1)
        with self.assertRaisesRegex(ContractError, "identifier"):
            packet(data)

    def test_inventory_hash_changes_identity_and_requires_fresh_references(self):
        from pilot.checkers.finite_bellman import solve

        original = example()
        old_identity = parse(canonical(original)).claims[1].identity
        tampered = copy.deepcopy(original)
        tampered["claims"][1]["cases"][0]["normalized_input_sha256"] = "0" * 64
        rebind(tampered, 1)
        with self.assertRaisesRegex(ContractError, "inventory input identity"):
            packet(tampered)
        data = copy.deepcopy(original)
        instance = data["instances"][1]
        instance["prefix_gain"] = "2/1"
        data["claims"][1]["version"] = 3
        data["claims"][1]["cases"][0]["normalized_input_sha256"] = digest(instance)
        data["evidence"][1]["certificates"] = [
            solve(instance, mode) for mode in ("state", "prefix")
        ]
        self.assertNotEqual(parse(canonical(data)).claims[1].identity, old_identity)
        for stale_section in ("evidence", "actions"):
            stale = copy.deepcopy(data)
            rebind(stale, 1)
            stale[stale_section][1]["claim_sha256"] = old_identity
            with (
                self.subTest(stale=stale_section),
                self.assertRaisesRegex(ContractError, "stale.*claim identity"),
            ):
                packet(stale)
        rebind(data, 1)
        result = packet(data)
        self.assertEqual(result["checked_evidence"][1]["values"], ("1/1", "1/1"))
        self.assertEqual(result["human_attestation"], "absent")
        old_list = example()
        old_list["claims"][1]["cases"] = ["strict_gain"]
        self.reject(old_list)
        duplicate = example()
        duplicate["claims"][1]["cases"] *= 2
        self.reject(duplicate)

    def test_identifier_boundaries_and_narrative_data(self):
        locations = [
            ("claims", 1, "id"),
            ("claims", 1, "parent"),
            ("claims", 1, "cases", 0, "id"),
            ("instances", 1, "instance_id"),
            ("evidence", 1, "id"),
            ("evidence", 1, "claim"),
            ("evidence", 1, "instance"),
            ("evidence", 1, "certificates", 0, "instance_id"),
            ("actions", 1, "id"),
            ("actions", 1, "claim"),
            ("actions", 1, "prerequisites", 0),
            ("attempts", 1, "id"),
            ("attempts", 1, "action"),
            ("attempts", 1, "evidence", 0),
        ]
        invalid = [
            "x\n\n# Human attestation: approved",
            "x\rheading",
            "x`code`",
            "x[link](url)",
            "x*bold*",
            "x<h1>",
            "x|cell",
            "x\\escape",
            "x\tdata",
            " x",
            "x ",
            "",
            "x" * 129,
            "é",
        ]
        for location, value in itertools.product(locations, invalid):
            data = example()
            target = data
            for key in location[:-1]:
                target = target[key]
            target[location[-1]] = value
            with (
                self.subTest(location=location, value=value),
                self.assertRaisesRegex(ContractError, "identifier|nonempty text"),
            ):
                parse(canonical(data))
        data = example()
        old = data["claims"][1]["id"]
        valid = "Claim.v3:case_1-OK"
        data["claims"][1]["id"] = valid
        for section in ("evidence", "actions"):
            data[section][1]["claim"] = valid
        narrative = "Explanation\n\n# Human attestation: approved\n``` * [text](url)"
        data["claims"][1]["statement"] = narrative
        data["attempts"][1]["reason"] = narrative
        rebind(data, 1)
        result = packet(data)
        rendered = markdown(result)
        self.assertNotIn("\n# Human attestation: approved", rendered)
        self.assertIn(valid, rendered)
        self.assertEqual(result["input"]["claims"][1]["statement"], narrative)
        self.assertEqual(result["human_attestation"], "absent")
        self.assertNotEqual(old, valid)

    def test_all_finite_set_orderings_preserve_inventory_identity(self):
        data = example()
        expected = packet(data)
        instance = data["instances"][1]
        # Exhaust all 2! * 3! * 3! = 72 permutations, without new dependencies.
        for paths, first, second in itertools.product(
            itertools.permutations(instance["paths"]),
            itertools.permutations(instance["first_actions"]),
            itertools.permutations(instance["second_actions"]),
        ):
            variant = copy.deepcopy(data)
            variant["instances"][1].update(
                paths=list(paths), first_actions=list(first), second_actions=list(second)
            )
            self.assertEqual(packet(variant), expected)
        submission = parse(canonical(data))
        with self.assertRaises(FrozenInstanceError):
            submission.claims[1].cases[0].normalized_input_sha256 = "0" * 64
        self.assertIsInstance(submission.claims[1].cases, tuple)

    def test_snapshot_all_files(self):
        snapshot_integrity()
        snapshot = json.loads(
            (ROOT / "artifacts/research-pilot-m0/finite-snapshot.json").read_text()
        )
        self.assertEqual(len(snapshot["files"]), 8)
        for name, entry in snapshot["files"].items():
            self.assertEqual(
                hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), entry["sha256"]
            )

    def test_immutable_and_defensive_parse(self):
        data = example()
        submission = parse(canonical(data))
        before = asdict(submission)
        data["claims"][0]["scope"]["modes"][0] = "open"
        data["instances"][0]["paths"][0][0] = "3/1"
        self.assertEqual(asdict(submission), before)
        with self.assertRaises(FrozenInstanceError):
            submission.claims[0].version = 4
        self.assertIsInstance(submission.claims[0].scope.modes, tuple)
        self.assertIsInstance(submission.evidence[0].certificates, tuple)
        self.assertIsInstance(submission.actions[0].prerequisites, tuple)

    def test_closed_records_missing_and_unknown_fields(self):
        base = example()
        locations = [
            (),
            ("claims", 0),
            ("claims", 0, "scope"),
            ("claims", 0, "cases", 0),
            ("instances", 0),
            ("evidence", 0),
            ("actions", 0),
            ("attempts", 0),
            ("evidence", 0, "certificates", 0),
        ]
        for location in locations:
            original = base
            for key in location:
                original = original[key]
            for field in original:
                data = copy.deepcopy(base)
                target = data
                for key in location:
                    target = target[key]
                del target[field]
                with self.subTest(location=location, missing=field):
                    self.reject(data)
            data = copy.deepcopy(base)
            target = data
            for key in location:
                target = target[key]
            target["unknown"] = "PASS"
            with self.subTest(location=location, unknown=True):
                self.reject(data)

    def test_invalid_json_channel(self):
        for raw in (
            '{"x":1,"x":2}',
            '{"x":NaN}',
            '{"x":Infinity}',
            '{"x":1.2}',
            "null",
            "[1]",
            "{",
        ):
            with self.subTest(raw=raw), self.assertRaises(ContractError):
                parse(raw)

    def test_boolean_versions_and_unknown_enums(self):
        changes = [("schema_version", True), ("schema_version", 1), ("schema_version", 3)]
        for field, value in changes:
            data = example()
            data[field] = value
            self.reject(data)
        for section, field, values in [
            ("claims", "version", [True, False, 0, "1"]),
            ("actions", "operation", ["prove", "PASS", None]),
            ("actions", "max_cases", [True, 0, 9]),
            ("actions", "wall_seconds", [True, 0, 121]),
            ("attempts", "outcome", ["proved", "attested", "formalized", None]),
        ]:
            for value in values:
                data = example()
                data[section][0][field] = value
                with self.subTest(section=section, field=field, value=value):
                    self.reject(data)

    def test_rational_boundaries(self):
        for value in ("0", "1/0", "2/2", "-0/1", "01/1", "1/-1", "1.0/1", "1001/1", True, None):
            data = example()
            data["instances"][0]["prefix_gain"] = value
            with self.subTest(value=value):
                self.reject(data)

    def test_numeric_certificate_mutations(self):
        # Every mutated exact value must fail, even if a worker labels it optimal.
        for numerator in range(-3, 4):
            data = example()
            data["evidence"][0]["certificates"][0]["value"] = f"{numerator}/1"
            if numerator != 1:
                self.reject(data)
        for field, value in [
            ("first_action", "1/1"),
            ("result", "PASS"),
            ("normalized_input_sha256", "0" * 64),
            ("information", "prefix"),
        ]:
            data = example()
            data["evidence"][0]["certificates"][0][field] = value
            self.reject(data)
        data = example()
        data["evidence"][0]["certificates"][0]["outcomes"][0]["x2"] = "9/1"
        self.reject(data)

    def test_nonoptimal_feasible_certificate_rejected(self):
        from pilot.checkers.finite_bellman import check_witness

        data = example()
        certificate = copy.deepcopy(data["evidence"][0]["certificates"][1])
        certificate["policy"] = [["-1/1", "0/1"], ["1/1", "0/1"]]
        certificate["value"] = "1/1"
        for outcome in certificate["outcomes"]:
            outcome["x2"] = outcome["path"][1]
            outcome["cost"] = "1/1"
        check_witness(data["instances"][0], "prefix", certificate)
        data["evidence"][0]["certificates"][1] = certificate
        self.reject(data)

    def test_binding_mutations(self):
        for section, field, value in [
            ("evidence", "checker_sha256", "0" * 64),
            ("evidence", "claim_sha256", "0" * 64),
            ("evidence", "instance", "strict_gain"),
            ("evidence", "claim", "prefix-state-equality-v2"),
            ("actions", "claim_sha256", "0" * 64),
            ("actions", "claim", "absent"),
            ("actions", "prerequisites", ["absent"]),
            ("attempts", "action", "absent"),
            ("attempts", "evidence", ["absent"]),
        ]:
            data = example()
            data[section][0][field] = value
            self.reject(data)
        data = example()
        data["claims"][0]["version"] = 3
        self.reject(data)
        for field, value in [("prefix_gain", "1/1"), ("terminal_interval", ["0/1", "0/1"])]:
            data = example()
            data["instances"][0][field] = value
            self.reject(data)
        for field, value in [
            ("modes", ["prefix", "state"]),
            ("model", "linear-general"),
            ("relation", "less-than"),
            ("restriction", "prose predicate"),
        ]:
            data = example()
            data["claims"][0]["scope"][field] = value
            self.reject(data)

    def test_outside_premise_counterexample(self):
        data = example()
        evidence = data["evidence"][1]
        evidence["instance"] = "correlated_hidden_disturbance"
        evidence["certificates"] = data["evidence"][0]["certificates"]
        data["claims"][1]["cases"] = copy.deepcopy(data["claims"][0]["cases"])
        rebind(data, 1)
        with self.assertRaisesRegex(ContractError, "outside claim premises"):
            packet(data)

    def test_lineage_and_duplicate_ids(self):
        for parent in ("absent", "prefix-state-equality-v2"):
            data = example()
            data["claims"][1]["parent"] = parent
            self.reject(data)
        data = example()
        data["claims"][0]["parent"] = data["claims"][1]["id"]
        self.reject(data)
        for section in ("claims", "instances", "evidence", "actions", "attempts"):
            data = example()
            data[section].append(copy.deepcopy(data[section][0]))
            self.reject(data)
        data = example()
        data["claims"][1]["scope"]["restriction"] = "all"
        rebind(data, 1)
        self.reject(data)

    def test_inventory_and_action_eligibility(self):
        for section in ("evidence", "instances"):
            data = example()
            data[section].pop()
            self.reject(data)
        data = example()
        data["attempts"][0]["evidence"] = []
        self.reject(data)
        data = example()
        data["claims"][0]["cases"].append(copy.deepcopy(data["claims"][1]["cases"][0]))
        rebind(data, 0)
        data["actions"][0]["max_cases"] = 2
        self.reject(data)
        data = example()
        data["actions"][1]["prerequisites"] = ["child-finite-test"]
        self.reject(data)
        data = example()
        for key in ("positive", "negative", "inconclusive"):
            data["actions"][0][key] = "Do more tests"
        self.reject(data)

    def test_typed_infeasibility_is_not_numeric(self):
        from pilot.checkers.finite_bellman import solve

        data = example()
        instance = data["instances"][0]
        instance["terminal_interval"] = ["10/1", "10/1"]
        data["evidence"][0]["certificates"] = [
            solve(instance, mode) for mode in ("state", "prefix")
        ]
        data["claims"][0]["cases"][0]["normalized_input_sha256"] = digest(instance)
        rebind(data, 0)
        with self.assertRaisesRegex(ContractError, "typed infeasibility"):
            packet(data)

    def test_each_noncompleted_outcome_has_no_promotion(self):
        for outcome in ("inconclusive", "failed", "cancelled", "budget-exhausted"):
            data = example()
            data["attempts"][0]["outcome"] = outcome
            data["attempts"][0]["evidence"] = []
            result = packet(data)["attempt_results"][0]
            self.assertEqual(result["scientific_outcome"], "none")
            self.assertNotIn("coverage", result)

    def test_bounded_normalization_property_and_planted_mutation(self):
        data = example()
        expected = packet(data)["checked_evidence"]
        # 2! * 3! = 12 order variants of one unchanged public instance.
        instance = data["instances"][0]
        for paths, actions in itertools.product(
            itertools.permutations(instance["paths"]),
            itertools.permutations(instance["second_actions"]),
        ):
            variant = copy.deepcopy(data)
            variant["instances"][0]["paths"] = list(paths)
            variant["instances"][0]["second_actions"] = list(actions)
            self.assertEqual(packet(variant)["checked_evidence"], expected)
        # A planted lost-path normalization defect must kill this acceptance property.
        from pilot.checkers.finite_bellman import validate_instance
        from pilot.science import contracts

        mutated = False

        def lost_path(value):
            nonlocal mutated
            normalized = validate_instance(value)
            if not mutated:
                normalized["paths"] = normalized["paths"][:-1]
                mutated = True
            return normalized

        with (
            patch("pilot.checkers.finite_bellman.validate_instance", side_effect=lost_path),
            self.assertRaisesRegex(ContractError, "inventory input identity"),
        ):
            build(contracts.parse(canonical(data)))

    def test_fresh_process_exports_and_no_writes(self):
        def identities():
            return {
                str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                for path in ROOT.rglob("*")
                if path.is_file() and ".git" not in path.parts
            }

        before = identities()
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
        for form, suffix in (("json", "packet.json"), ("markdown", "dossier.md")):
            command = [
                sys.executable,
                "-m",
                "pilot.science",
                "--input",
                str(FIXTURE),
                "--format",
                form,
            ]
            first = subprocess.run(
                command, cwd=ROOT, env=env, capture_output=True, timeout=30, check=True
            )
            second = subprocess.run(
                command, cwd=ROOT, env=env, capture_output=True, timeout=30, check=True
            )
            self.assertEqual(first.stdout, second.stdout)
            expected = (
                canonical(packet(example())) + "\n"
                if form == "json"
                else markdown(packet(example()))
            )
            self.assertEqual(first.stdout.decode(), expected)
            self.assertEqual(
                first.stdout, (ROOT / f"pilot/examples/offline-dossier-v1.{suffix}").read_bytes()
            )
        self.assertEqual(before, identities())
        failure = subprocess.run(
            [
                sys.executable,
                "-m",
                "pilot.science",
                "--input",
                str(ROOT / "missing.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            env=env,
            capture_output=True,
            timeout=30,
        )
        self.assertEqual(failure.returncode, 2)
        self.assertEqual(failure.stdout, b"")
        self.assertIn(b"rejected", failure.stderr)


if __name__ == "__main__":
    unittest.main()
