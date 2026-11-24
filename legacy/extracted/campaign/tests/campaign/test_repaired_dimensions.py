"""Repaired zip sites reject dimensional truncation in normal and optimized Python."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, ROOT / path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class DimensionTests(unittest.TestCase):
    def test_baseline_dimensions(self):
        check = module("research/baseline/checks/check_candidate_v2.py")
        for left, right in (([1], [1, 2]), ([1, 2], [1])):
            with self.subTest(left=left), self.assertRaisesRegex(ValueError, "dimension mismatch"):
                check.dot(left, right)
            with self.subTest(left=left), self.assertRaisesRegex(ValueError, "dimension mismatch"):
                check.add(left, right)
        self.assertEqual(check.dot([1, 2], [3, 4]), 11)

    def test_trajectory_dimensions(self):
        check = module("research/structured/checks/trajectory_check_v2.py")
        data = {
            "x_initial": [0, 0],
            "first_program": [0],
            "boxes": [([0, 0], [1, 1]), ([0, 0], [1, 1])],
        }
        with self.assertRaises(ValueError):
            check.trajectory(data, {"w": []}, [0, 0])
        with self.assertRaises(ValueError):
            check.dot([1], [1, 2])
        with (
            patch.object(check, "trajectory", return_value=[[0, 0]]),
            self.assertRaises(ValueError),
        ):
            check.feasible({"H": [[0, 0], [0, 0]], "h": [1]}, {}, [], 0)
        data["first_program"] = [0, 0]
        data.update(A=[[], []], B=[[], []], E=[[], []])
        with (
            patch.object(check, "mv", side_effect=[[0], [0, 0], [0, 0]]),
            self.assertRaises(ValueError),
        ):
            check.trajectory(data, {"w": [[], []]}, [0, 0])

    def test_certificate_dimensions(self):
        check = module("research/structured/checks/certificate_check_v2.py")
        with (
            patch.object(check, "rows_for", return_value={"cost": ([1], 0)}),
            self.assertRaises(ValueError),
        ):
            check.combine({"p": {}}, [{"lambda": 1, "path": "p", "row": "cost"}], 0)


if __name__ == "__main__":
    unittest.main()
