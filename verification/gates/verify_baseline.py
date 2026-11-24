#!/usr/bin/env python3
"""Baseline integrity verifier for autoresearcher (supports full local corpus and PDF-free public mirror)."""

from __future__ import annotations

import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _is_omitted_public_pdf(rel: str) -> bool:
    return rel.startswith("corpus/") and rel.lower().endswith(".pdf")


def verify_migration() -> None:
    manifest_path = ROOT / "legacy/migration-manifest-r1b.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assets = manifest["assets"]
    if len(assets) != 423:
        raise AssertionError(f"Expected 423 migrated assets, found {len(assets)}")
    verified = 0
    omitted_pdfs = 0
    for item in assets:
        rel = item["v2_path"]
        expected = item["sha256"]
        if not _HEX64.match(expected):
            raise AssertionError(f"Invalid SHA-256 in manifest for {rel}")
        p = ROOT / rel
        if not p.is_file():
            if _is_omitted_public_pdf(rel):
                omitted_pdfs += 1
                continue
            raise AssertionError(f"Missing migrated asset: {rel}")
        got = sha256_file(p)
        if got != expected:
            raise AssertionError(f"SHA-256 mismatch for {rel}")
        verified += 1
    print(f"MIGRATION SHA-256 OK: {verified} verified + {omitted_pdfs} omitted third-party PDFs (total {verified + omitted_pdfs}/423)")


def verify_corpus() -> None:
    manifest_path = ROOT / "corpus/MANIFEST.md"
    checked = 0
    present = 0
    omitted_pdfs = 0
    for raw in manifest_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if len(line) > 66 and line[64:66] == "  ":
            expected_sha, rel = line[:64], line[66:]
            if not _HEX64.match(expected_sha):
                raise AssertionError(f"Invalid SHA-256 in corpus/MANIFEST.md: {rel}")
            target = ROOT / rel
            if not target.is_file():
                if _is_omitted_public_pdf(rel):
                    omitted_pdfs += 1
                    checked += 1
                    continue
                raise AssertionError(f"Missing corpus file: {rel}")
            if sha256_file(target) != expected_sha:
                raise AssertionError(f"Corpus SHA-256 mismatch: {rel}")
            present += 1
            checked += 1
    if checked != 42:
        raise AssertionError(f"Expected 42 corpus manifest entries, found {checked}")
    intake_pdfs = sorted((ROOT / "corpus/intake").glob("*.pdf")) if (ROOT / "corpus/intake").is_dir() else []
    extra_files = sorted((ROOT / "corpus/extra").glob("*")) if (ROOT / "corpus/extra").is_dir() else []
    print(
        f"CORPUS MANIFEST OK: {checked}/42 manifest entries ({present} verified on disk, "
        f"{omitted_pdfs} third-party PDFs omitted in public mirror) + "
        f"{len(intake_pdfs)} intake PDFs + {len(extra_files)} extra files"
    )


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("migration", "all"):
        verify_migration()
    if mode in ("corpus", "all"):
        verify_corpus()
    if mode not in ("migration", "corpus", "all"):
        print(f"Unknown mode: {mode}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
