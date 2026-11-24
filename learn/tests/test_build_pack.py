"""Unit tests for learn/build_pack.py."""

from __future__ import annotations

import io
import json
import os
import pathlib
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

from learn import REQUIRED_GUIDE_FILES
from learn.build_pack import (
    PackBuildError,
    build_study_pack,
    compute_lh_source_id,
    materialize_pack,
    valid_notes_path,
)
from learn.push_to_lh import aro_cli

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


class TestBuildPack(unittest.TestCase):
    def test_real_packet_01_builds_with_hierarchy_and_gate_g5(self) -> None:
        pack = build_study_pack(
            "01-bridge-packet-01",
            repo_root=REPO_ROOT,
            validate_gate=True,
            require_style=False,
        )
        self.assertEqual(pack.topic, "01-bridge-packet-01")
        self.assertEqual(pack.folder_prefix, "ARO/01-Bridge-OGU-ARO/01-bridge-packet-01/")
        self.assertEqual(len(pack.entries), 4)
        self.assertGreater(pack.total_bytes, 0)
        for entry, expected_name in zip(pack.entries, REQUIRED_GUIDE_FILES, strict=True):
            expected_rel = f"ARO/01-Bridge-OGU-ARO/01-bridge-packet-01/{expected_name}"
            self.assertEqual(entry.filename, expected_name)
            self.assertEqual(entry.relative_path, expected_rel)
            self.assertTrue(valid_notes_path(entry.relative_path, entry.filename))
            self.assertEqual(entry.source_id, compute_lh_source_id(expected_rel))
            self.assertTrue(entry.source_id.startswith("src_"))
            self.assertEqual(len(entry.source_id), 16)

    def test_materialize_pack_preserves_hierarchy_and_manifest(self) -> None:
        pack = build_study_pack("01-bridge-packet-01", repo_root=REPO_ROOT)
        with tempfile.TemporaryDirectory(prefix="aro-r5-pack-") as tmp:
            out_dir = pathlib.Path(tmp) / "export"
            manifest_path = materialize_pack(pack, out_dir)
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["file_count"], 4)
            self.assertEqual(manifest["folder_prefix"], pack.folder_prefix)
            for entry in pack.entries:
                copied = out_dir / entry.relative_path
                self.assertTrue(copied.is_file())
                self.assertEqual(copied.read_bytes(), entry.source_path.read_bytes())

    def test_rejects_reserved_dirs_and_traversal(self) -> None:
        for bad in ("TEMPLATE", "00-source-packet-01", "../corpus", "a/b", "..", "a:b"):
            with self.assertRaises(PackBuildError):
                build_study_pack(bad, repo_root=REPO_ROOT)

    def test_rejects_missing_file_empty_file_and_nul_byte(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-r5-badpack-") as tmp:
            guides = pathlib.Path(tmp)
            topic = guides / "99-broken"
            topic.mkdir()
            for fname in REQUIRED_GUIDE_FILES[:-1]:
                (topic / fname).write_text("# Ok\n", encoding="utf-8")
            with self.assertRaises(PackBuildError):
                build_study_pack("99-broken", guides_root=guides)

            # Empty file rejected
            (topic / REQUIRED_GUIDE_FILES[-1]).write_text("   \n", encoding="utf-8")
            with self.assertRaises(PackBuildError):
                build_study_pack("99-broken", guides_root=guides)

            # Binary NUL byte rejected (mirrors LearnHarness readNotesFile)
            (topic / REQUIRED_GUIDE_FILES[-1]).write_bytes(b"# Ok\x00binary")
            with self.assertRaises(PackBuildError):
                build_study_pack("99-broken", guides_root=guides)

            # Exceeding max_bytes rejected
            (topic / REQUIRED_GUIDE_FILES[-1]).write_text("# Valid\n", encoding="utf-8")
            with self.assertRaises(PackBuildError):
                build_study_pack("99-broken", guides_root=guides, max_bytes=10)

    def test_valid_notes_path_contract(self) -> None:
        self.assertTrue(valid_notes_path("ARO/Track/Topic/01.md", "01.md"))
        self.assertTrue(valid_notes_path("01.md", "01.md"))
        self.assertFalse(valid_notes_path("../01.md", "01.md"))
        self.assertFalse(valid_notes_path("ARO/./01.md", "01.md"))
        self.assertFalse(valid_notes_path("ARO/Track/other.md", "01.md"))
        self.assertFalse(valid_notes_path("ARO\\Track\\01.md", "01.md"))
        self.assertFalse(valid_notes_path("C:/ARO/01.md", "01.md"))
        self.assertFalse(valid_notes_path("", "01.md"))

    def test_wheel_install_resolves_guides_from_cwd_and_subdirectories(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-fake-sitepkg-") as fake_site:
            old_cwd = pathlib.Path.cwd()
            clean_env = {k: v for k, v in os.environ.items() if k != "ARO_GUIDES_ROOT"}
            try:
                os.chdir(REPO_ROOT / "learn")
                with (
                    mock.patch.dict(os.environ, clean_env, clear=True),
                    mock.patch("learn.build_pack.REPO_ROOT", pathlib.Path(fake_site)),
                ):
                    out = io.StringIO()
                    with redirect_stdout(out):
                        rc = aro_cli(
                            [
                                "study",
                                "01-bridge-packet-01",
                                "--mode",
                                "practice",
                                "--dry-run",
                                "--json",
                            ]
                        )
                    self.assertEqual(rc, 0)
                    parsed = json.loads(out.getvalue())
                    self.assertEqual(parsed["session"]["mode"], "practice")
                    self.assertTrue(parsed["session"]["dry_run"])
            finally:
                os.chdir(old_cwd)


if __name__ == "__main__":
    unittest.main()
