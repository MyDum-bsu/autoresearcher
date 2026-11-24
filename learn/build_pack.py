#!/usr/bin/env python3
"""Build and validate a LearnHarness v0.7.0 export study pack from research/guides/<topic>/.

Preserves relative folder hierarchy `ARO/<track>/<topic>/<file>.md` compatible with
LearnHarness POST /api/graph/import (`files` + `paths`) and validNotesPath().
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import os
import pathlib
import re
import shutil
import sys
from typing import Any

from learn import (
    DEFAULT_ROOT_PREFIX,
    DEFAULT_TRACK,
    IMPORT_EXTENSIONS,
    MAX_IMPORT_BYTES,
    REQUIRED_GUIDE_FILES,
    RESERVED_GUIDE_DIRS,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
_UNSAFE_PATH_CHARS_RE = re.compile(r"[\\:\x00-\x1f\x7f]")


class PackBuildError(ValueError):
    """Raised when a guide topic cannot produce a valid LearnHarness import pack."""


@dataclasses.dataclass(frozen=True)
class PackEntry:
    source_path: pathlib.Path
    relative_path: str
    filename: str
    size_bytes: int
    sha256: str
    source_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_path": str(self.source_path),
            "relative_path": self.relative_path,
            "filename": self.filename,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
            "source_id": self.source_id,
        }


@dataclasses.dataclass(frozen=True)
class StudyPack:
    topic: str
    track: str
    root_prefix: str
    source_dir: pathlib.Path
    entries: tuple[PackEntry, ...]
    total_bytes: int

    @property
    def folder_prefix(self) -> str:
        return f"{self.root_prefix}/{self.track}/{self.topic}/"

    @property
    def source_ids(self) -> frozenset[str]:
        return frozenset(e.source_id for e in self.entries)

    def to_manifest(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "topic": self.topic,
            "track": self.track,
            "root_prefix": self.root_prefix,
            "folder_prefix": self.folder_prefix,
            "source_dir": str(self.source_dir),
            "total_bytes": self.total_bytes,
            "file_count": len(self.entries),
            "entries": [e.to_dict() for e in self.entries],
        }


def compute_lh_source_id(relative_path: str) -> str:
    """Match LearnHarness v0.7.0 sourceDirectory.registerImport(filePath) id hash."""
    digest = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:12]
    return f"src_{digest}"


def valid_notes_path(rel_path: str, filename: str) -> bool:
    """Exact Python mirror of LearnHarness v0.7.0 lib/notes-import-limits.ts validNotesPath."""
    if not rel_path or len(rel_path) > 1024:
        return False
    if _UNSAFE_PATH_CHARS_RE.search(rel_path):
        return False
    parts = rel_path.split("/")
    if any(not part or part in (".", "..") for part in parts):
        return False
    return parts[-1] == filename or rel_path == filename


def _validate_segment(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if (
        not cleaned
        or "/" in cleaned
        or "\\" in cleaned
        or cleaned in (".", "..")
        or _UNSAFE_PATH_CHARS_RE.search(cleaned)
    ):
        raise PackBuildError(f"Invalid {field_name} segment: {value!r}")
    return cleaned


def _run_gate_g5_for_pack(
    pack_dir: pathlib.Path,
    repo_root: pathlib.Path,
    *,
    require_style: bool,
) -> None:
    gates_dir = repo_root / "verification/gates"
    gate_script = gates_dir / "verify_guides.py"
    if not gate_script.is_file():
        raise PackBuildError(f"Gate G5 validator not found: {gate_script}")
    if str(gates_dir) not in sys.path:
        sys.path.insert(0, str(gates_dir))
    import verify_guides as vg  # type: ignore[import-not-found]

    known_corpus = vg.load_known_corpus_files(repo_root)
    known_lean = vg.load_known_lean_decls(repo_root)
    try:
        style_linter = (
            vg.resolve_style_linter(None, require_style=True) if require_style else None
        )
    except FileNotFoundError as exc:
        raise PackBuildError(str(exc)) from exc
    errors = vg.check_pack(pack_dir, repo_root, known_corpus, known_lean, style_linter)
    if errors:
        joined = "\n  - ".join(errors)
        raise PackBuildError(f"Guide pack failed Gate G5 validation:\n  - {joined}")


def resolve_repo_and_guides_root(
    *,
    repo_root: pathlib.Path | None = None,
    guides_root: pathlib.Path | None = None,
) -> tuple[pathlib.Path, pathlib.Path]:
    """Resolve (repo_root, guides_root) robustly for both checkout and wheel installs.

    Precedence:
      1. Explicit `guides_root`
      2. Environment variable `ARO_GUIDES_ROOT`
      3. Explicit `repo_root / "research/guides"`
      4. Walk upward from `Path.cwd()` for `research/guides`
      5. Fallback `REPO_ROOT / "research/guides"`
    """
    if guides_root is not None:
        resolved_guides = guides_root.expanduser().resolve()
        if repo_root is not None:
            return repo_root.expanduser().resolve(), resolved_guides
        if len(resolved_guides.parents) >= 2:
            return resolved_guides.parents[1], resolved_guides
        return REPO_ROOT, resolved_guides

    env_guides = os.environ.get("ARO_GUIDES_ROOT")
    if env_guides:
        resolved_guides = pathlib.Path(env_guides).expanduser().resolve()
        resolved_repo = (
            repo_root.expanduser().resolve()
            if repo_root is not None
            else (resolved_guides.parents[1] if len(resolved_guides.parents) >= 2 else REPO_ROOT)
        )
        return resolved_repo, resolved_guides

    if repo_root is not None:
        resolved_repo = repo_root.expanduser().resolve()
        return resolved_repo, (resolved_repo / "research/guides").resolve()

    cwd = pathlib.Path.cwd().resolve()
    for candidate in (cwd, *cwd.parents):
        cand_guides = candidate / "research/guides"
        if cand_guides.is_dir():
            return candidate, cand_guides.resolve()

    return REPO_ROOT, (REPO_ROOT / "research/guides").resolve()


def build_study_pack(
    topic: str,
    *,
    track: str = DEFAULT_TRACK,
    root_prefix: str = DEFAULT_ROOT_PREFIX,
    repo_root: pathlib.Path | None = None,
    guides_root: pathlib.Path | None = None,
    validate_gate: bool = False,
    require_style: bool = True,
    max_bytes: int = MAX_IMPORT_BYTES,
) -> StudyPack:
    """Assemble and validate a LearnHarness export pack from research/guides/<topic>/."""
    safe_root = _validate_segment(root_prefix, "root_prefix")
    safe_track = _validate_segment(track, "track")
    safe_topic = _validate_segment(topic, "topic")
    if safe_topic in RESERVED_GUIDE_DIRS:
        raise PackBuildError(f"Topic {safe_topic!r} is a reserved non-export directory")

    resolved_repo, base_guides = resolve_repo_and_guides_root(
        repo_root=repo_root, guides_root=guides_root
    )
    topic_dir = (base_guides / safe_topic).resolve()
    if not topic_dir.is_relative_to(base_guides):
        raise PackBuildError(f"Topic path escapes guides root: {topic!r}")
    if not topic_dir.is_dir():
        raise PackBuildError(f"Guide topic directory not found: {topic_dir}")

    if validate_gate:
        _run_gate_g5_for_pack(topic_dir, resolved_repo, require_style=require_style)

    entries: list[PackEntry] = []
    total_bytes = 0
    for fname in REQUIRED_GUIDE_FILES:
        fpath = (topic_dir / fname).resolve()
        if not fpath.is_relative_to(topic_dir) or not fpath.is_file():
            raise PackBuildError(f"Missing required guide file: {safe_topic}/{fname}")
        if fpath.suffix.lower() not in IMPORT_EXTENSIONS:
            raise PackBuildError(f"Unsupported import extension for {fname}")

        raw = fpath.read_bytes()
        if not raw.strip():
            raise PackBuildError(f"Guide file is empty: {safe_topic}/{fname}")
        # Mirror LearnHarness readNotesFile binary heuristic (first 8 KiB NUL byte check)
        if b"\x00" in raw[:8192]:
            raise PackBuildError(f"Guide file contains NUL byte (not plain text): {fname}")
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PackBuildError(f"Guide file is not valid UTF-8: {fname}: {exc}") from exc

        rel_path = f"{safe_root}/{safe_track}/{safe_topic}/{fname}"
        if not valid_notes_path(rel_path, fname):
            raise PackBuildError(f"Invalid LearnHarness relative path: {rel_path!r}")

        size = len(raw)
        total_bytes += size
        if total_bytes > max_bytes:
            raise PackBuildError(
                f"Pack exceeds LearnHarness MAX_IMPORT_BYTES ({max_bytes} bytes)"
            )

        entries.append(
            PackEntry(
                source_path=fpath,
                relative_path=rel_path,
                filename=fname,
                size_bytes=size,
                sha256=hashlib.sha256(raw).hexdigest(),
                source_id=compute_lh_source_id(rel_path),
            )
        )

    return StudyPack(
        topic=safe_topic,
        track=safe_track,
        root_prefix=safe_root,
        source_dir=topic_dir,
        entries=tuple(entries),
        total_bytes=total_bytes,
    )


def materialize_pack(pack: StudyPack, out_dir: pathlib.Path) -> pathlib.Path:
    """Copy pack files into out_dir preserving ARO/<track>/<topic>/<file>.md + manifest."""
    dest_root = out_dir.resolve()
    dest_root.mkdir(parents=True, exist_ok=True)
    for entry in pack.entries:
        target = (dest_root / entry.relative_path).resolve()
        if not target.is_relative_to(dest_root):
            raise PackBuildError(f"Materialized path escapes output root: {entry.relative_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(entry.source_path, target)
    manifest_path = dest_root / "pack-manifest.json"
    manifest_path.write_text(
        json.dumps(pack.to_manifest(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build and validate a LearnHarness v0.7.0 export pack from research/guides/."
    )
    parser.add_argument(
        "topic",
        help="Guide directory name under research/guides/ (e.g. 01-bridge-packet-01)",
    )
    parser.add_argument(
        "--track",
        default=DEFAULT_TRACK,
        help=f"Track folder (default: {DEFAULT_TRACK})",
    )
    parser.add_argument(
        "--root-prefix",
        default=DEFAULT_ROOT_PREFIX,
        help=f"Top folder (default: {DEFAULT_ROOT_PREFIX})",
    )
    parser.add_argument(
        "--guides-root",
        type=pathlib.Path,
        default=None,
        help="Override research/guides/ path",
    )
    parser.add_argument(
        "--out-dir",
        type=pathlib.Path,
        default=None,
        help="Materialize folder tree + pack-manifest.json",
    )
    parser.add_argument(
        "--validate-gate",
        action="store_true",
        help="Also run Gate G5 guide validation",
    )
    parser.add_argument(
        "--no-style",
        action="store_true",
        help="Skip RU style linter when --validate-gate is set",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON manifest to stdout")
    args = parser.parse_args(argv)

    try:
        pack = build_study_pack(
            args.topic,
            track=args.track,
            root_prefix=args.root_prefix,
            guides_root=args.guides_root,
            validate_gate=args.validate_gate,
            require_style=not args.no_style,
        )
        manifest_path = materialize_pack(pack, args.out_dir) if args.out_dir else None
    except PackBuildError as exc:
        print(f"build_pack error: {exc}", file=sys.stderr)
        return 1

    payload = pack.to_manifest()
    if manifest_path is not None:
        payload["manifest_path"] = str(manifest_path)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"PACK OK: {pack.folder_prefix} ({len(pack.entries)} files, {pack.total_bytes} bytes)"
        )
        for e in pack.entries:
            print(f"  - {e.relative_path} [{e.source_id}] ({e.size_bytes} B)")
        if manifest_path is not None:
            print(f"  manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
