"""Package completeness is evaluator authority, never submission authority."""

import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pilot.episodes import judge, validate

ROOT = judge.ROOT
REPO = ROOT.parents[1]
REFERENCES = {
    f"{family}-{variant}.json": family
    for family in "MFPR"
    for variant in ("reference", "alternative")
}
CONTROLS = {
    "M-wrong-information.json": "M",
    "F-erased-refutation.json": "F",
    "P-wrong-statement.json": "P",
    "P-unsupported-axiom.json": "P",
    "R-ignore-contradiction.json": "R",
}


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory(prefix="inventory-", dir=ROOT)
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name) / "episodes"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns("inventory-*"))

    def rejected_without_summary(self):
        output = io.StringIO()
        with (
            patch.object(judge, "ROOT", self.root),
            contextlib.redirect_stdout(output),
            self.assertRaises((judge.Rejected, OSError)),
        ):
            validate.main()
        self.assertEqual(output.getvalue(), "")

    def test_every_expected_file_is_required(self):
        for directory, inventory in [("references", REFERENCES), ("controls", CONTROLS)]:
            for name in inventory:
                with self.subTest(directory=directory, name=name):
                    path = self.root / directory / name
                    contents = path.read_bytes()
                    path.unlink()
                    try:
                        self.rejected_without_summary()
                    finally:
                        path.write_bytes(contents)

    def test_empty_and_missing_directories(self):
        for directory in ("references", "controls"):
            path = self.root / directory
            with self.subTest(directory=directory, state="empty"):
                shutil.rmtree(path)
                path.mkdir()
                self.rejected_without_summary()
            with self.subTest(directory=directory, state="missing"):
                path.rmdir()
                self.rejected_without_summary()
            shutil.copytree(ROOT / directory, path)
        shutil.rmtree(self.root / "references")
        shutil.rmtree(self.root / "controls")
        self.rejected_without_summary()

    def test_unexpected_entries_and_nonfiles(self):
        for directory in ("references", "controls"):
            for name in ("extra.json", "extra.txt"):
                with self.subTest(directory=directory, name=name):
                    path = self.root / directory / name
                    path.write_text("{}")
                    try:
                        self.rejected_without_summary()
                    finally:
                        path.unlink()
            name = next(iter(REFERENCES if directory == "references" else CONTROLS))
            path = self.root / directory / name
            contents = path.read_bytes()
            path.unlink()
            path.mkdir()
            try:
                self.rejected_without_summary()
            finally:
                path.rmdir()
                path.write_bytes(contents)

    def test_each_filename_is_bound_to_its_family(self):
        for directory, inventory in [("references", REFERENCES), ("controls", CONTROLS)]:
            for name, family in inventory.items():
                with self.subTest(directory=directory, name=name):
                    path = self.root / directory / name
                    contents = path.read_bytes()
                    other = "F" if family == "M" else "M"
                    source = ROOT / "references" / f"{other}-reference.json"
                    if directory == "controls":
                        source = (
                            ROOT
                            / "controls"
                            / next(item for item, kind in CONTROLS.items() if kind == other)
                        )
                    path.write_bytes(source.read_bytes())
                    try:
                        self.rejected_without_summary()
                    finally:
                        path.write_bytes(contents)

    def test_integrity_runs_independently_before_inventory(self):
        shutil.rmtree(self.root / "references")
        with (
            patch.object(judge, "ROOT", self.root),
            patch.object(
                judge, "integrity", side_effect=judge.Rejected("integrity sentinel")
            ) as integrity,
        ):
            with self.assertRaisesRegex(judge.Rejected, "integrity sentinel"):
                validate.main()
            integrity.assert_called_once_with()

    def test_cli_missing_inventory_is_nonzero_without_summary(self):
        for directory, name in [
            ("references", "P-reference.json"),
            ("controls", "M-wrong-information.json"),
        ]:
            path = self.root / directory / name
            contents = path.read_bytes()
            path.unlink()
            script = (
                "from pathlib import Path; from pilot.episodes import judge, validate; "
                f"judge.ROOT = Path({str(self.root)!r}); validate.main()"
            )
            try:
                result = subprocess.run(
                    [sys.executable, "-B", "-c", script],
                    cwd=REPO,
                    capture_output=True,
                    timeout=60,
                    check=False,
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, b"")
            finally:
                path.write_bytes(contents)


if __name__ == "__main__":
    unittest.main()
