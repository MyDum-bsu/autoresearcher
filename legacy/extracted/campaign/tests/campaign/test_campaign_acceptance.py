"""Disposable evidence bundles, not scientific campaign evidence."""

import copy
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "campaign_acceptance", ROOT / "scripts/campaign_acceptance.py"
)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
REAL = json.loads((ROOT / validator.CONTRACT_PATH).read_text())


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        tmp = ROOT / "artifacts/campaign/tmp"
        self.assertEqual(Path(os.environ["TMPDIR"]).resolve(), tmp.resolve())
        self.temp = tempfile.TemporaryDirectory(dir=tmp, prefix="delivery-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.contract = copy.deepcopy(REAL)
        self.contract["required_check_ids"] = ["tlc-stale-fence"]
        self.contract["required_present_or_explicitly_unavailable_files"] = [
            "payload.txt",
            "research/resource-manifest.json",
            "artifacts/campaign/mechanism-results.json",
        ]
        self.contract["must_exist_for_validator_invocation"] = [
            validator.CONTRACT_PATH,
            validator.INDEX_PATH,
        ]
        self.contract["conditional_inventory"]["C_safeToContinue_true"]["files"] = ["attempt.txt"]
        self.index = {
            "schema_version": 1,
            "contract_sha256": "",
            "question_manifest_sha256": "",
            "campaign_disposition": "completed-with-declared-limits",
            "scientific_attestation": False,
            "stages": [],
            "files": [],
            "checks": [],
            "sources": [],
            "claims": [],
            "reviews": [],
            "resources": {"billing": "unknown"},
            "limitations": ["Synthetic delivery test; no mathematical truth claim"],
        }
        self.put(validator.CONTRACT_PATH, json.dumps(self.contract))
        self.index["contract_sha256"] = validator.sha256(self.root / validator.CONTRACT_PATH)
        self.put("payload.txt", "frozen input\n")
        self.put("attempt.txt", "delivered attempt\n")
        self.put("research/resource-manifest.json", "{}\n")
        self.index["question_manifest_sha256"] = validator.sha256(
            self.root / "research/resource-manifest.json"
        )
        names = (
            REAL["required_phase_records"]
            + REAL["conditional_inventory"]["C_safeToContinue_true"]["phase_records"]
        )
        for name in names:
            self.put_phase(name)
        for stage in REAL["required_stage_ids"]:
            phase = {
                "A": "01-plan",
                "B": "05-tools",
                "C": "06-domain",
                "D1": "07-baseline",
                "D2": "08-structured",
                "E": "09-continuation",
                "F-review": "10-review",
                "F-synthesis": "13-synthesis",
            }[stage]
            self.index["stages"].append(
                {
                    "id": stage,
                    "disposition": "completed",
                    "phase_record": self.phase_path(phase),
                    "output_paths": ["payload.txt"],
                    "check_ids": ["tlc-stale-fence"],
                    "reason": "",
                    "blocker_evidence_ids": [],
                }
            )
        self.put("stdout.txt", "Invariant SingleCurrentWriter is violated.\n")
        self.put("stderr.txt", "")
        self.observation = {
            "case_id": "tlc-stale-fence",
            "layer": "native-tlc",
            "native_exit": 12,
            "wrapper_exit": 0,
            "reason_code": "SingleCurrentWriter",
            "diagnostic_stream": "stdout",
            "diagnostic_excerpt": "Invariant SingleCurrentWriter is violated.",
        }
        self.put("observation.json", json.dumps(self.observation))
        self.inventory = {"case_ids": ["tlc-stale-fence"], "files": [self.ref("payload.txt")]}
        self.put("inventory.json", json.dumps(self.inventory))
        self.check = {
            "id": "tlc-stale-fence",
            "stage": "B",
            "disposition": "passed",
            "command": {"cwd": ".", "argv": ["java", "tlc2.TLC"]},
            "inputs": [self.ref("payload.txt")],
            "outputs": [self.ref(p) for p in ("stdout.txt", "stderr.txt", "observation.json")],
            "scope": "bounded synthetic protocol model",
            "expected_observation": "SingleCurrentWriter counterexample",
            "observed_exit": 12,
            "stdout_path": "stdout.txt",
            "stderr_path": "stderr.txt",
            "observed_summary": "expected control",
            "reason": "",
            "blocker_evidence_ids": [],
            "inventory_path": "inventory.json",
            "observation_path": "observation.json",
        }
        self.index["checks"] = [self.check]
        self.index["sources"] = [
            {
                "id": "S1",
                "original_path": "read-only-public-source",
                "original_sha256": validator.sha256(self.root / "payload.txt"),
                "copy_path": "payload.txt",
                "copy_sha256": validator.sha256(self.root / "payload.txt"),
                "import_kind": "verbatim",
                "anchors": ["section 1"],
                "read_scope": "fixture",
            }
        ]
        self.index["claims"] = [
            {
                "id": "Q1",
                "version": 1,
                "statement_path": "payload.txt",
                "statement_sha256": validator.sha256(self.root / "payload.txt"),
                "evidence_kind": "unproved-sketch",
                "source_ids": ["S1"],
                "check_ids": [],
                "dependency_ids": [],
                "scope": "fixture only",
                "limitations": ["unproved"],
            }
        ]
        self.index["reviews"] = [
            {
                "phase_id": "10-review",
                "findings": [],
                "resolution_status": "no-findings",
                "repair_check_ids": [],
                "recheck_check_ids": [],
            }
        ]
        self.mechanisms = [
            {
                "id": name,
                "disposition": "tested/adapted",
                "source_anchor": "S1",
                "intended_benefit": "fixture",
                "smallest_test": "fixture",
                "observed_result": "fixture",
                "adoption_decision": "fixture",
                "limitations": "fixture",
                "check_ids": ["tlc-stale-fence"],
            }
            for name in REAL["required_mechanism_ids"]
        ]
        self.put("artifacts/campaign/mechanism-results.json", json.dumps(self.mechanisms))

    def put(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)
        self.index["files"] = [item for item in self.index["files"] if item["path"] != path]
        self.index["files"].append(
            {
                "path": path,
                "availability": "present",
                "sha256": validator.sha256(target),
                "size_bytes": target.stat().st_size,
            }
        )

    def ref(self, path):
        return {"path": path, "sha256": validator.sha256(self.root / path)}

    def phase_path(self, name):
        return f"artifacts/campaign/phases/{name}.json"

    def put_phase(self, name, safe=True):
        self.put(
            self.phase_path(name),
            json.dumps(
                {
                    "disposition": "done",
                    "summary": "Synthetic phase",
                    "reportPath": "",
                    "evidencePaths": [],
                    "blockers": [],
                    "safeToContinue": safe,
                }
            ),
        )

    def errors(self):
        return validator.validate_bundle(self.root, self.contract, self.index)

    def reject(self, fragment):
        errors = self.errors()
        self.assertTrue(errors, "Malformed bundle was accepted")
        self.assertIn(fragment, errors[0])

    def test_complete_positive_bundle(self):
        self.assertEqual(self.errors(), [])

    def test_honest_negative_and_blocked_bundle(self):
        blocker = {
            "id": "unsupported-tool",
            "stage": "B",
            "disposition": "blocked",
            "scope": "unavailable native tool",
            "expected_observation": "not run",
            "observed_exit": None,
            "reason": "namespace prerequisite unavailable",
            "blocker_evidence_ids": ["tlc-stale-fence"],
            "blocker_observations": [
                {
                    "check_id": "tlc-stale-fence",
                    "stream": "stdout",
                    "excerpt": "Invariant SingleCurrentWriter is violated.",
                }
            ],
        }
        self.index["checks"].append(blocker)
        self.index["claims"][0]["evidence_kind"] = "refuted-candidate"
        self.assertEqual(self.errors(), [])

    def test_missing_stage(self):
        self.index["stages"].pop()
        self.reject("stage")

    def test_missing_file(self):
        self.index["files"] = [f for f in self.index["files"] if f["path"] != "attempt.txt"]
        self.reject("missing required file")

    def test_missing_check(self):
        self.check["id"] = "different"
        self.reject("missing required check")

    def test_missing_mechanism(self):
        self.put("artifacts/campaign/mechanism-results.json", json.dumps(self.mechanisms[:-1]))
        self.reject("mechanism")

    def test_empty_inventory(self):
        for field in ("stages", "files", "checks", "sources", "claims", "reviews"):
            with self.subTest(field=field):
                saved = self.index[field]
                self.index[field] = []
                self.reject("empty inventory")
                self.index[field] = saved
        self.inventory["case_ids"] = []
        self.put("inventory.json", json.dumps(self.inventory))
        self.reject("dynamic cases")

    def test_wrong_output_hash(self):
        (self.root / "stdout.txt").write_text("tampered")
        self.reject("size")

    def test_source_drift(self):
        self.index["sources"][0]["original_sha256"] = "0" * 64
        self.reject("source drift")

    def test_duplicate_id(self):
        self.index["checks"].append(copy.deepcopy(self.check))
        self.reject("duplicate check")

    def test_duplicate_json_key(self):
        self.put("observation.json", '{"case_id":"a","case_id":"b"}')
        self.check["outputs"][-1] = self.ref("observation.json")
        self.reject("duplicate JSON key")
        self.put("observation.json", '{"value":NaN}')
        self.check["outputs"][-1] = self.ref("observation.json")
        self.reject("nonfinite")

    def test_path_escape(self):
        for path in ("../outside", "/etc/passwd", "a/../../outside"):
            with self.subTest(path=path):
                self.index["files"].append({"path": path, "availability": "present"})
                self.reject("path escape")
                self.index["files"].pop()

    def test_symlink_escape(self):
        (self.root / "escape").symlink_to(self.root.parent, target_is_directory=True)
        self.index["files"].append({"path": "escape/outside", "availability": "present"})
        self.reject("symlink escape")

    def test_invalid_enum(self):
        self.index["scientific_attestation"] = True
        self.reject("attestation")
        self.index["scientific_attestation"] = False
        self.index["schema_version"] = True
        self.reject("schema_version")
        self.index["schema_version"] = 1
        self.check["disposition"] = "pending"
        self.reject("invalid check disposition")

    def test_null_exit_claimed_pass(self):
        self.check["observed_exit"] = None
        self.reject("null exit")

    def test_wrong_negative_observation(self):
        variants = [
            ("wrong case", {"case_id": "tlc-base"}),
            ("wrong exit", {"native_exit": 0}),
            ("wrong reason", {"reason_code": "unrelated"}),
            ("unrelated diagnostic", {"diagnostic_stream": "stderr"}),
            ("forged excerpt", {"diagnostic_excerpt": "invented native evidence"}),
            ("wrapper posing as native", {"layer": "campaign-preflight"}),
        ]
        for name, mutation in variants:
            with self.subTest(name=name):
                self.put("observation.json", json.dumps(self.observation | mutation))
                self.check["outputs"][-1] = self.ref("observation.json")
                self.assertTrue(self.errors())
        self.put("observation.json", json.dumps(self.observation))
        self.check["outputs"][-1] = self.ref("observation.json")
        self.check["outputs"][-1]["sha256"] = "0" * 64
        self.reject("identity mismatch")
        self.check["outputs"][-1] = self.ref("observation.json")
        (self.root / "stderr.txt").unlink()
        self.reject("missing file")

    def test_unsupported_checked_claim(self):
        claim = self.index["claims"][0]
        claim.update(
            evidence_kind="exact-finite",
            check_ids=["tlc-stale-fence"],
            independent_check_ids=["tlc-stale-fence"],
        )
        self.reject("author check reused")

    def test_repair_without_recheck(self):
        self.put_phase("11-repair")
        self.reject("unpaired repair")
        self.put_phase("12-final-review")
        self.put("reports/2026-11-13-campaign-repair.md", "repair\n")
        self.index["reviews"][0].update(findings=["concrete defect"], resolution_status="resolved")
        self.reject("missing recheck")

    def test_unsafe_question_conditional_inventory(self):
        self.put_phase("06-domain", safe=False)
        self.reject("07-research-not-started")
        self.put_phase("07-research-not-started", safe=False)
        self.reject("wrong stage phase link")
        for stage in self.index["stages"]:
            if stage["id"] in {"D1", "D2", "E"}:
                stage.update(
                    disposition="blocked",
                    phase_record=self.phase_path("07-research-not-started"),
                    reason="Decisive source premise missing at C",
                    blocker_evidence_ids=["tlc-stale-fence"],
                )
        self.assertEqual(self.errors(), [])

    def test_missing_and_empty_target_inventory(self):
        for expected, reported, reason in (
            ([], [], "empty-target-inventory"),
            (["Campaign.expected"], [], "missing-target-coverage"),
            (["Campaign.expected"], ["wrong"], "missing-target-coverage"),
        ):
            with (
                self.subTest(expected=expected, reported=reported),
                self.assertRaisesRegex(validator.EvidenceError, reason),
            ):
                validator.target_inventory("fixture", expected, reported)
        validator.target_inventory("fixture", ["Campaign.expected"], ["Campaign.expected"])

    def test_wrapper_predicates_require_null_native_exit(self):
        for case, reason in (
            ("cmp-empty-inventory", "empty-target-inventory"),
            ("cmp-missing-inventory", "missing-target-coverage"),
        ):
            predicate = REAL["expected_control_predicates"][case]
            observation = {
                "case_id": case,
                "layer": "campaign-preflight",
                "reason_code": reason,
                "native_exit": None,
                "wrapper_exit": 1,
                "diagnostic_stream": "stderr",
                "diagnostic_excerpt": f"{case}: {reason}",
            }
            check = {"observed_exit": 1, "control_facts": predicate.get("requires", [])}
            validator.check_predicate(
                case, check, observation, predicate, {"stderr": observation["diagnostic_excerpt"]}
            )
            observation["native_exit"] = 0
            with self.assertRaises(validator.EvidenceError):
                validator.check_predicate(
                    case,
                    check,
                    observation,
                    predicate,
                    {"stderr": observation["diagnostic_excerpt"]},
                )

    def test_missing_contract_cannot_fallback(self):
        with self.assertRaises((FileNotFoundError, KeyError, validator.EvidenceError)):
            validator.load_active_contract(self.root)

    def test_output_cannot_replace_input(self):
        self.check["inputs"] = [self.ref("stdout.txt")]
        self.reject("output substituted for input")

    def test_empty_required_artifact(self):
        self.put("payload.txt", "")
        self.reject("empty required artifact")

    def test_index_output_does_not_require_self_hash(self):
        self.index["stages"][-1]["output_paths"].append(validator.INDEX_PATH)
        self.assertEqual(self.errors(), [])

    def test_wrong_stage_phase_link(self):
        for stage in self.index["stages"]:
            saved = stage["phase_record"]
            stage["phase_record"] = self.phase_path("01-plan" if stage["id"] != "A" else "05-tools")
            self.reject("wrong stage phase link")
            stage["phase_record"] = saved

    def test_final_review_phase_link(self):
        self.put_phase("11-repair")
        self.put_phase("12-final-review")
        self.put("reports/2026-11-13-campaign-repair.md", "repair\n")
        next(s for s in self.index["stages"] if s["id"] == "F-review")["phase_record"] = (
            self.phase_path("12-final-review")
        )
        self.assertEqual(self.errors(), [])

    def test_blocker_cycles_and_causal_observation(self):
        blocked = dict(
            self.check,
            disposition="blocked",
            observed_exit=None,
            reason="tool unavailable",
            blocker_evidence_ids=["tlc-stale-fence"],
        )
        self.index["checks"] = [blocked]
        self.reject("cyclic blocker")
        other = dict(blocked, id="other", blocker_evidence_ids=["tlc-stale-fence"])
        blocked["blocker_evidence_ids"] = ["other"]
        self.index["checks"].append(other)
        self.reject("cyclic blocker")
        self.index["checks"] = [self.check, dict(other, blocker_evidence_ids=["tlc-stale-fence"])]
        self.reject("missing causal observation")
        other = self.index["checks"][-1]
        other["blocker_observations"] = [
            {"check_id": "tlc-stale-fence", "stream": "stdout", "excerpt": "invented"}
        ]
        self.reject("unbound causal diagnostic")
        other["blocker_observations"][0]["excerpt"] = "Invariant SingleCurrentWriter is violated."
        failure = dict(
            self.check, id="native-failure", disposition="failed", reason="Observed native failure"
        )
        self.index["checks"].append(failure)
        self.inventory["case_ids"].append("native-failure")
        self.put("inventory.json", json.dumps(self.inventory))
        other["blocker_evidence_ids"] = ["native-failure"]
        other["blocker_observations"][0]["check_id"] = "native-failure"
        self.assertEqual(self.errors(), [])
        self.mechanisms[0]["check_ids"] = ["other"]
        self.put("artifacts/campaign/mechanism-results.json", json.dumps(self.mechanisms))
        self.reject("not-run mechanism")

    def test_real_frozen_manifest_cannot_be_omitted(self):
        for path in (
            "research/baseline/checks/manifest.json",
            "research/structured/checks/manifest.json",
            "research/continuation/checks/manifest.json",
        ):
            with self.subTest(path=path):
                self.put(path, (ROOT / path).read_text())
                self.reject("missing frozen check")
                self.index["files"] = [f for f in self.index["files"] if f["path"] != path]

    def test_actual_frozen_obligations(self):
        paths = [
            "artifacts/campaign/tool-readiness.json",
            "research/baseline/checks/manifest.json",
            "research/structured/checks/manifest.json",
            "research/continuation/checks/manifest.json",
            "research/continuation/checks/timing-manifest.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                original = json.loads((ROOT / path).read_text())
                inputs = original.get("input_files", original.get("inputs", []))
                specs = original.get("checks", [{"id": c} for c in original.get("check_ids", [])])
                ids = [s["id"] for s in specs]
                inv = {
                    "case_ids": ids,
                    "candidate_ids": original.get("candidate_ids", []),
                    "frozen_parents": [{"path": path, "sha256": validator.sha256(ROOT / path)}],
                    "frozen_case_mapping": {c: original.get("cases", []) for c in ids},
                }
                if original["phase"] == "B":
                    frozen_path = original["input_manifest"]
                    frozen = json.loads((ROOT / frozen_path).read_text())
                    inv["frozen_parents"].append(
                        {"path": frozen_path, "sha256": validator.sha256(ROOT / frozen_path)}
                    )
                self.put("normalized.json", json.dumps(inv))
                refs = {path} | {r["path"] for r in inputs}
                if original["phase"] == "B":
                    refs.add(frozen_path)
                    refs.update(r["path"] for r in frozen["files"])
                refs.update(original.get("required_outputs", original.get("output_paths", [])))
                refs.update(original.get("expected_deliverables", []))
                checks = {}
                for spec in specs:
                    ins = spec.get("input_paths", [r["path"] for r in inputs]) + [
                        r["path"] for r in spec.get("inputs", [])
                    ]
                    outs = [spec[k] for k in ("stdout_path", "stderr_path") if k in spec] + [
                        r["path"] for r in spec.get("outputs", [])
                    ]
                    if original["phase"] == "D1":
                        outs = original["output_paths"]
                    refs.update(ins + outs)
                    checks[spec["id"]] = {
                        "stage": original["phase"],
                        "disposition": "passed",
                        "inventory_path": "normalized.json",
                        "inputs": [{"path": p} for p in ins],
                        "outputs": [{"path": p} for p in outs],
                    }
                if original["phase"] == "B":
                    for check in checks.values():
                        check["declared_targets"] = frozen["targets"]
                files = {p: {"availability": "present"} for p in refs}

                def present(p, files=files):
                    validator.require(p in files or p == "normalized.json", "missing bound file")
                    return self.root / p if p == "normalized.json" else ROOT / p

                def validate(path=path, files=files, checks=checks, present=present):
                    validator.frozen_obligations(
                        self.root, self.contract, {path}, files, checks, present
                    )

                validate()
                removed = checks.pop(ids[0])
                with self.assertRaisesRegex(validator.EvidenceError, "missing frozen check"):
                    validate()
                checks[ids[0]] = removed
                output = removed["outputs"][0]["path"]
                del files[output]
                with self.assertRaisesRegex(validator.EvidenceError, "missing frozen"):
                    validate()
                files[output] = {"availability": "present"}
                inv["frozen_parents"][0]["sha256"] = "0" * 64
                self.put("normalized.json", json.dumps(inv))
                with self.assertRaisesRegex(validator.EvidenceError, "unbound frozen parent"):
                    validate()

    def test_dynamic_target_coverage(self):
        self.inventory["targets"] = ["Campaign.expected"]
        self.put("inventory.json", json.dumps(self.inventory))
        self.check["reported_targets"] = []
        self.reject("missing-target-coverage")


if __name__ == "__main__":
    unittest.main()
