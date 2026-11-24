"""Unit tests for Journal Editor Significance Gate & R12 Run-02 Falsify-First Runner (#1714)."""

from __future__ import annotations

import dataclasses
import json
import pathlib
import tempfile
import unittest

from research.discovery.run02.run02_falsify import (
    MANIFEST_DEFAULT,
    Run02FalsifyError,
    run_all,
)
from research.discovery.significance_gate import (
    SignificanceCandidate,
    evaluate_significance,
    run_self_test,
)


class TestSignificanceGateAndRun02(unittest.TestCase):
    def test_significance_gate_self_test_passes(self) -> None:
        self.assertEqual(run_self_test(), 0)

    def test_significance_gate_rejects_goodhart_trivial_lemma(self) -> None:
        trivial = SignificanceCandidate(
            candidate_id="goodhart-bad-1",
            target_open_node_id="conj-o1-adr-exactness-char",
            title="Helper lemma renaming 0-dimensional box bound",
            statement="A trivial lemma proved by reflexivity when rho = 0 only.",
            closes_gap_mechanism="Helper lemma to inflate Lean theorem count.",
            falsifiable_prediction="None needed since trivial.",
            falsifier_method="exact_rational_lp",
            dimension_regime="0-dimensional",
            expected_theorem_class="trivial_helper",
        )
        verdict = evaluate_significance(trivial)
        self.assertEqual(verdict.decision, "REJECT")
        self.assertEqual(verdict.axis_scores["nontriviality"], 0)
        self.assertTrue(any("Goodhart" in r for r in verdict.rejection_reasons))

    def test_significance_gate_rejects_tautology_with_padded_fields(self) -> None:
        manifest = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
        cand = SignificanceCandidate.from_dict(manifest["candidates"][0])
        taut = dataclasses.replace(
            cand,
            candidate_id="goodhart-tautology",
            title="Universal real equality",
            statement="For all x in R, x = x.",
        )
        verdict = evaluate_significance(taut)
        self.assertEqual(verdict.decision, "REJECT")
        self.assertEqual(verdict.axis_scores["nontriviality"], 0)

    def test_significance_gate_rejects_prose_reflexive_tautology(self) -> None:
        manifest = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
        cand = SignificanceCandidate.from_dict(manifest["candidates"][0])
        taut = dataclasses.replace(
            cand,
            candidate_id="goodhart-prose-taut",
            title="Closure schedule matrix rank identity",
            statement=(
                "For every closure schedule R, the exact rank of its matrix M_R "
                "equals the exact rank of that same matrix M_R."
            ),
        )
        verdict = evaluate_significance(taut)
        self.assertEqual(verdict.decision, "REJECT")
        self.assertEqual(verdict.axis_scores["nontriviality"], 0)

    def test_run02_rejects_empty_or_mismatched_manifest(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-run02-bad-") as tmp:
            bad_path = pathlib.Path(tmp) / "empty.json"
            bad_path.write_text(
                json.dumps({"run_name": "BAD", "seed": 1, "candidates": []}), encoding="utf-8"
            )
            with self.assertRaises(Run02FalsifyError):
                run_all(manifest_path=bad_path)

            # Mutated expected_checks (claiming O4 defect = "+1") MUST fail closed
            m = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
            m["candidates"][0]["expected_checks"]["instance_a_defect"] = "1"
            mutated_path = pathlib.Path(tmp) / "mutated.json"
            mutated_path.write_text(json.dumps(m), encoding="utf-8")
            with self.assertRaises(Run02FalsifyError):
                run_all(manifest_path=mutated_path)

            # Mutated statement/prediction prose without updating bound probe MUST fail closed
            m2 = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
            m2["candidates"][0]["statement"] = (
                "Strict supermodularity with defect +1 holds on all T=3 OGU systems."
            )
            mutated_prose = pathlib.Path(tmp) / "mutated_prose.json"
            mutated_prose.write_text(json.dumps(m2), encoding="utf-8")
            with self.assertRaises(Run02FalsifyError):
                run_all(manifest_path=mutated_prose)

            # Omitting constrained keys from expected_checks MUST fail closed
            m3 = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
            m3["candidates"][0]["expected_checks"] = {"unconstrained_defect": "0"}
            mutated_keys = pathlib.Path(tmp) / "mutated_keys.json"
            mutated_keys.write_text(json.dumps(m3), encoding="utf-8")
            with self.assertRaises(Run02FalsifyError):
                run_all(manifest_path=mutated_keys)

    def test_significance_gate_rejects_closed_atlas_target(self) -> None:
        manifest = json.loads(MANIFEST_DEFAULT.read_text(encoding="utf-8"))
        cand = SignificanceCandidate.from_dict(manifest["candidates"][0])
        bad = dataclasses.replace(cand, target_open_node_id="thm-f2-epigraph-equality")
        verdict = evaluate_significance(bad)
        self.assertEqual(verdict.decision, "REJECT")
        self.assertEqual(verdict.axis_scores["frontier_alignment"], 0)

    def test_run02_manifest_and_exact_falsify_first_probes(self) -> None:
        report = run_all()
        self.assertEqual(report["status"], "ok")
        self.assertEqual(report["run_name"], "R12-RUN-02")
        self.assertEqual(report["significance_gate_accepted"], 5)
        probes = {p["candidate_id"]: p for p in report["probes"]}
        self.assertEqual(
            set(probes),
            {
                "run02-o4-submodularity",
                "run02-g1-markov-sufficiency",
                "run02-g2-l1-vertex-lp",
                "run02-o1-fullrank-b-2d",
                "run02-o8-gap-vanishing-regime",
            },
        )
        self.assertEqual(
            probes["run02-o4-submodularity"]["instance_unconstrained"]["submodularity_defect"], "0"
        )
        self.assertEqual(
            probes["run02-o4-submodularity"]["instance_a"]["submodularity_defect"], "0"
        )
        self.assertEqual(
            probes["run02-o4-submodularity"]["instance_b"]["submodularity_defect"], "-1"
        )
        self.assertEqual(probes["run02-g1-markov-sufficiency"]["injective_regime"]["gap"], "0")
        self.assertEqual(probes["run02-g1-markov-sufficiency"]["merged_state_regime"]["gap"], "1")
        self.assertEqual(probes["run02-g2-l1-vertex-lp"]["l1_support_rows_verified_2d"], 5)
        self.assertEqual(probes["run02-g2-l1-vertex-lp"]["l1_support_rows_verified_3d"], 5)
        self.assertEqual(probes["run02-g2-l1-vertex-lp"]["dim2_l1_rotated_square"]["gap"], "0")
        self.assertEqual(probes["run02-g2-l1-vertex-lp"]["dim3_l1_octahedron"]["gap"], "1/2")
        self.assertEqual(probes["run02-o1-fullrank-b-2d"]["t1_t7_battery_passed"], 7)
        self.assertEqual(probes["run02-o1-fullrank-b-2d"]["rank1_B_diag_H"]["gap"], "2")
        self.assertEqual(probes["run02-o1-fullrank-b-2d"]["rank1_B_relaxed_H"]["gap"], "0")
        self.assertEqual(probes["run02-o1-fullrank-b-2d"]["fullrank_B_diag_H"]["gap"], "0")
        self.assertEqual(
            [row["prefix_gap"] for row in probes["run02-o8-gap-vanishing-regime"]["u1_max_sweep"]],
            ["1", "1/2", "0", "0"],
        )
        self.assertEqual(
            [row["full_gap"] for row in probes["run02-o8-gap-vanishing-regime"]["u1_max_sweep"]],
            ["1", "1", "1", "1"],
        )


if __name__ == "__main__":
    unittest.main()
