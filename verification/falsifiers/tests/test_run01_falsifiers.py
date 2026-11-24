"""Unit tests executing all R12 Run-01 Stage 2 falsifiers and O8 counterexample."""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]


def _py_flags() -> list[str]:
    return [sys.executable, "-B", *(["-O"] if not __debug__ else [])]


class TestRun01Falsifiers(unittest.TestCase):
    def _run_json_script(self, rel_path: str) -> dict:
        script = REPO_ROOT / rel_path
        self.assertTrue(script.is_file(), f"Missing script: {rel_path}")
        proc = subprocess.run(
            [*_py_flags(), str(script)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(
            proc.returncode,
            0,
            f"{rel_path} failed (exit {proc.returncode}):\n{proc.stdout}\n{proc.stderr}",
        )
        return json.loads(proc.stdout)

    def test_o8_counterexample_exact_lp(self) -> None:
        data = self._run_json_script("research/counterexamples/O8-sion-gap/checks/check_o8_gap.py")
        self.assertEqual(data["verdict"], "REFUTED_AT_STAGE_2_FALSIFY_FIRST_BY_EXACT_LP")
        self.assertEqual(data["V_empty"], "4")
        self.assertEqual(data["V_r1"], "2")
        self.assertEqual(data["V_mm_prefix"], "0")
        self.assertEqual(data["V_mm_full"], "0")
        self.assertEqual(data["gap_r1_vs_prefix_mm"], "2")

    def test_f4_vertex_lp_falsifier(self) -> None:
        data = self._run_json_script("verification/falsifiers/run01/falsify_f4.py")
        self.assertTrue(data["survived"])
        self.assertGreaterEqual(data["checked_points"], 13)

    def test_g2_conic_support_falsifier(self) -> None:
        data = self._run_json_script("verification/falsifiers/run01/falsify_g2.py")
        self.assertTrue(data["survived"])
        self.assertGreaterEqual(data["checked_points"], 19)

    def test_o4_closure_value_falsifier(self) -> None:
        data = self._run_json_script("verification/falsifiers/run01/falsify_o4.py")
        self.assertTrue(data["survived"])
        self.assertGreaterEqual(data["checked_points"], 7)

    def test_g1_multistage_falsifier(self) -> None:
        data = self._run_json_script("verification/falsifiers/run01/falsify_g1.py")
        self.assertTrue(data["survived"])
        self.assertGreaterEqual(data["k2_causal_bijection"]["checked_trajectories"], 4)
        self.assertGreaterEqual(data["k2_markov_vs_history_separation"]["checked_history_paths"], 10)
        self.assertGreaterEqual(data["k2_markov_vs_history_separation"]["checked_signaling_pairs"], 25)
        self.assertTrue(data["atlas_g1_oracles"]["ok"])
        self.assertGreaterEqual(data["checked_points"], 43)

    def test_o1_adr_exactness_falsifier(self) -> None:
        data = self._run_json_script("verification/falsifiers/run01/falsify_o1.py")
        self.assertTrue(data["survived"])
        self.assertGreaterEqual(data["checked_points"], 50)


if __name__ == "__main__":
    unittest.main()
