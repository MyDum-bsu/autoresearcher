#!/usr/bin/env python3
"""Deterministic public-repository hygiene & security verifier for aro-discovery.

Audits the exact Git index snapshot (`git ls-files -s -z` + `git cat-file --batch`) or
a target directory during --self-test for:
  - host-specific absolute user/volume paths (Unix home/media/Users, Windows Users)
  - leaked secrets, API keys, private keys, and credentials-in-URLs
  - internal orchestration IDs (thread/project/environment IDs)
  - hardcoded local task-board endpoints and internal board ticket references
  - personal email addresses outside SHA-256-verified primary literature under corpus/
  - forbidden tracked build/credential artifacts (.env, *.pem, *.key, *.olean, .lake)
  - tracked symlinks pointing to absolute paths or escaping the repository root

Every blob is scanned without binary-header skipping or size cutoffs across UTF-8
(including NUL bytes), UTF-16 BOM, UTF-16LE, and UTF-16BE, plus tracked pathnames.

Optionally (`--check-history`) audits all commits reachable from HEAD (author/committer
emails, commit messages, and historical blobs), rejects shallow checkouts, and reads
allowlist manifests strictly from each audited commit (never from the uncommitted index).

Diagnostics never echo matched secrets, raw line contents, or sensitive filenames.
Runs identically under `python3 -B` and `python3 -B -O` (no logic relies on `assert`).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]

FORBIDDEN_PATH_RES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("forbidden_env_file", re.compile(r"(?:^|/)\.env(?:\.[^/]+)?$")),
    ("forbidden_key_file", re.compile(r"(?:^|/)(?:id_rsa|id_ed25519|.*\.(?:pem|key|p12|pfx))$")),
    ("forbidden_lean_artifact", re.compile(r"(?:^|/)\.lake(?:/|$)|\.(?:olean|ilean)$")),
)

# Regexes are assembled so this script itself never embeds literal forbidden tokens
# and is audited by the exact same rules with zero self-exemptions.
CONTENT_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "host_unix_path",
        re.compile(
            r"(?<![A-Za-z0-9_.-])(?:/ho" + r"me/[A-Za-z0-9_.-]+"
            r"|/me" + r"dia/[A-Za-z0-9_.-]+"
            r"|/Us" + r"ers/[A-Za-z0-9_.-]+)"
        ),
    ),
    (
        "host_windows_path",
        re.compile(r"[A-Za-z]:\\Us" + r"ers\\[A-Za-z0-9_.-]+"),
    ),
    (
        "file_uri_host",
        re.compile(r"file:///(?:ho" + r"me|me" + r"dia|Us" + r"ers)/"),
    ),
    (
        "secret_token",
        re.compile(
            r"(?:gh" + r"p_[A-Za-z0-9]{20,}"
            r"|github_" + r"pat_[A-Za-z0-9_]{20,}"
            r"|gh" + r"[ousr]_[A-Za-z0-9]{20,}"
            r"|s" + r"k-(?:proj-|ant-)?[A-Za-z0-9_-]{20,}"
            r"|AK" + r"IA[0-9A-Z]{16}"
            r"|AI" + r"za[0-9A-Za-z\-_]{35}"
            r"|xo" + r"x[baprs]-[A-Za-z0-9-]{10,})"
        ),
    ),
    (
        "private_key",
        re.compile(r"-----BEGIN [A-Z0-9 ]*PRI" + r"VATE KEY-----"),
    ),
    (
        "basic_auth_url",
        re.compile(r"https?://[^/\s:@]+:[^/\s:@]+@[^\s]+"),
    ),
    (
        "internal_bb_id",
        re.compile(
            r"\b(?:th" + r"r_[a-z0-9]{8,}"
            r"|pr" + r"oj_[a-z0-9]{8,}"
            r"|en" + r"v_[a-z0-9]*\d[a-z0-9]{5,})\b"
        ),
    ),
    (
        "local_board_ref",
        re.compile(
            r"(?:127\.0\.0\.1:44" + r"100"
            r"|localhost:44" + r"100"
            r"|\bBo" + r"ard\s*#\d+\b)"
        ),
    ),
    (
        "personal_email",
        re.compile(r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ),
)

CORPUS_EMAIL_ALLOW_PREFIX = "corpus/"

COMBINED_ALL_RE = re.compile(
    "|".join(f"(?P<{name}>{pat.pattern})" for name, pat in CONTENT_RULES)
)
COMBINED_NO_EMAIL_RE = re.compile(
    "|".join(
        f"(?P<{name}>{pat.pattern})"
        for name, pat in CONTENT_RULES
        if name != "personal_email"
    )
)


def _decode_candidate_texts(raw: bytes) -> list[str]:
    """Return all text decodings (UTF-8 and UTF-16 variants) with no size or magic-header skip."""
    if not raw:
        return []
    texts: list[str] = []
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        texts.append(raw.decode("utf-16", errors="replace"))
    texts.append(raw.decode("utf-8", errors="replace"))
    if len(raw) >= 2:
        even_len = len(raw) - (len(raw) % 2)
        chunk = raw[:even_len]
        texts.append(chunk.decode("utf-16-le", errors="ignore"))
        texts.append(chunk.decode("utf-16-be", errors="ignore"))
    return texts


def _safe_display_path(rel: str) -> str:
    """Redact any pathname that itself matches a sensitive hygiene rule."""
    for _, pat in CONTENT_RULES:
        if pat.search(rel) is not None:
            return "<redacted-path>"
    return rel


def _parse_corpus_allowlist(manifest_md: str | None, migration_json: str | None) -> dict[str, str]:
    """Build exact (rel_path -> sha256) map for primary literature under corpus/."""
    allowed: dict[str, str] = {}
    if manifest_md:
        for raw_line in manifest_md.splitlines():
            line = raw_line.strip()
            if len(line) > 66 and line[64:66] == "  ":
                digest, rel = line[:64], line[66:]
                if re.fullmatch(r"[0-9a-f]{64}", digest) and rel.startswith(CORPUS_EMAIL_ALLOW_PREFIX):
                    allowed[rel] = digest
    if migration_json:
        try:
            data = json.loads(migration_json)
            for item in data.get("assets", []):
                rel = item.get("v2_path", "")
                digest = item.get("sha256", "")
                if (
                    isinstance(rel, str)
                    and isinstance(digest, str)
                    and rel.startswith(CORPUS_EMAIL_ALLOW_PREFIX)
                    and re.fullmatch(r"[0-9a-f]{64}", digest)
                ):
                    allowed.setdefault(rel, digest)
        except (json.JSONDecodeError, AttributeError):
            pass
    return allowed


def _read_git_blob_optional(repo_root: pathlib.Path, spec: str) -> str | None:
    try:
        raw = subprocess.check_output(
            ["git", "cat-file", "blob", spec],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
        )
        return raw.decode("utf-8", errors="replace")
    except subprocess.CalledProcessError:
        return None


def _load_corpus_email_hashes(
    repo_root: pathlib.Path,
    *,
    git_ref: str | None,
) -> dict[str, str]:
    """Load exact corpus/ SHA-256 allowlist from git_ref (':' for index, '<commit>:' for commit, None for disk)."""
    if git_ref is not None:
        manifest_md = _read_git_blob_optional(repo_root, f"{git_ref}corpus/MANIFEST.md")
        migration_json = _read_git_blob_optional(
            repo_root, f"{git_ref}legacy/migration-manifest-r1b.json"
        )
        return _parse_corpus_allowlist(manifest_md, migration_json)

    manifest_path = repo_root / "corpus/MANIFEST.md"
    migration_path = repo_root / "legacy/migration-manifest-r1b.json"
    manifest_md = (
        manifest_path.read_text(encoding="utf-8", errors="replace")
        if manifest_path.is_file()
        else None
    )
    migration_json = (
        migration_path.read_text(encoding="utf-8", errors="replace")
        if migration_path.is_file()
        else None
    )
    return _parse_corpus_allowlist(manifest_md, migration_json)


def _batch_read_git_blobs(repo_root: pathlib.Path, shas: list[str]) -> dict[str, bytes]:
    """Read multiple Git blobs in a single deadlock-free `git cat-file --batch` call."""
    unique_shas = list(dict.fromkeys(shas))
    if not unique_shas:
        return {}
    payload = ("\n".join(unique_shas) + "\n").encode("ascii")
    res = subprocess.run(
        ["git", "cat-file", "--batch"],
        cwd=repo_root,
        input=payload,
        capture_output=True,
        check=True,
    )
    out = res.stdout
    pos = 0
    total = len(out)
    blobs: dict[str, bytes] = {}
    for sha in unique_shas:
        nl = out.find(b"\n", pos)
        if nl == -1:
            break
        header = out[pos:nl].decode("ascii").strip()
        pos = nl + 1
        parts = header.split(" ")
        if len(parts) >= 3 and parts[1] == "blob":
            size = int(parts[2])
            blobs[sha] = out[pos : pos + size]
            pos += size + 1  # skip trailing newline
        if pos >= total:
            break
    return blobs


def _scan_path_name(rel: str, safe_rel: str, *, context_prefix: str = "") -> list[str]:
    """Scan a tracked pathname against forbidden-artifact and content hygiene rules."""
    violations: list[str] = []
    prefix = f"{context_prefix}:" if context_prefix else ""
    for rule_name, pat in FORBIDDEN_PATH_RES:
        if pat.search(rel):
            violations.append(f"{prefix}{safe_rel}:0: [{rule_name}] forbidden tracked path")
    for rule_name, pat in CONTENT_RULES:
        if pat.search(rel) is not None:
            violations.append(
                f"{prefix}{safe_rel}:0: [{rule_name}] hygiene rule violation in tracked path"
            )
    return violations


def _scan_text_lines(
    display_label: str,
    text: str,
    *,
    allow_email: bool,
) -> list[str]:
    violations: list[str] = []
    seen: set[tuple[int, str]] = set()
    combined = COMBINED_NO_EMAIL_RE if allow_email else COMBINED_ALL_RE
    for match in combined.finditer(text):
        rule_name = match.lastgroup
        if rule_name is None:
            continue
        lineno = text.count("\n", 0, match.start()) + 1
        key = (lineno, rule_name)
        if key not in seen:
            seen.add(key)
            # Never echo matched values or raw snippets (prevents secret leakage in CI logs).
            violations.append(f"{display_label}:{lineno}: [{rule_name}] hygiene rule violation")
    return violations


def _scan_blob(
    rel: str,
    safe_rel: str,
    mode: str,
    raw: bytes,
    repo_root: pathlib.Path,
    corpus_email_hashes: dict[str, str],
    *,
    context_prefix: str = "",
) -> list[str]:
    violations: list[str] = []
    display_label = f"{context_prefix}:{safe_rel}" if context_prefix else safe_rel

    if mode == "120000":
        target = raw.decode("utf-8", errors="replace")
        if os.path.isabs(target):
            violations.append(f"{display_label}:0: [absolute_symlink] tracked symlink has absolute target")
        else:
            resolved = (repo_root / rel).parent.joinpath(target).resolve()
            try:
                resolved.relative_to(repo_root.resolve())
            except ValueError:
                violations.append(
                    f"{display_label}:0: [escaping_symlink] tracked symlink escapes repository root"
                )
        violations.extend(_scan_text_lines(display_label, target, allow_email=False))
        return violations

    allow_email = False
    if rel in corpus_email_hashes:
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha == corpus_email_hashes[rel]:
            allow_email = True

    seen_v: set[str] = set()
    for text in _decode_candidate_texts(raw):
        for v in _scan_text_lines(display_label, text, allow_email=allow_email):
            if v not in seen_v:
                seen_v.add(v)
                violations.append(v)
    return violations


def scan_tree(repo_root: pathlib.Path, *, use_git: bool = True) -> tuple[int, list[str]]:
    """Scan the exact Git index snapshot (when use_git=True) or directory tree (for self-tests)."""
    corpus_email_hashes = _load_corpus_email_hashes(
        repo_root, git_ref=":" if use_git else None
    )
    violations: list[str] = []

    if use_git:
        out = subprocess.check_output(
            ["git", "-c", "core.quotepath=false", "ls-files", "-s", "-z"],
            cwd=repo_root,
        )
        entries: list[tuple[str, str, str]] = []
        for entry in out.split(b"\x00"):
            if not entry:
                continue
            header, rel_b = entry.split(b"\t", 1)
            mode, blob_sha, _stage = header.decode("ascii").split(" ")
            rel = rel_b.decode("utf-8", errors="replace")
            entries.append((mode, blob_sha, rel))

        blobs = _batch_read_git_blobs(
            repo_root, [sha for mode, sha, _ in entries if mode != "160000"]
        )
        scanned = 0
        for mode, blob_sha, rel in entries:
            safe_rel = _safe_display_path(rel)
            violations.extend(_scan_path_name(rel, safe_rel))
            if mode == "160000":
                continue
            scanned += 1
            raw = blobs[blob_sha]
            violations.extend(
                _scan_blob(rel, safe_rel, mode, raw, repo_root, corpus_email_hashes)
            )
        return scanned, violations

    # Non-git directory scan (used by isolated --self-test temp directories)
    rel_list: list[str] = []
    for dirpath, dirnames, filenames in os.walk(repo_root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        base = pathlib.Path(dirpath)
        for d in list(dirnames):
            dp = base / d
            if dp.is_symlink():
                rel_list.append(dp.relative_to(repo_root).as_posix())
                dirnames.remove(d)
        for fname in sorted(filenames):
            rel_list.append((base / fname).relative_to(repo_root).as_posix())

    scanned = 0
    for rel in sorted(rel_list):
        safe_rel = _safe_display_path(rel)
        violations.extend(_scan_path_name(rel, safe_rel))
        full = repo_root / rel
        if full.is_symlink():
            scanned += 1
            raw = os.readlink(full).encode("utf-8", errors="replace")
            violations.extend(
                _scan_blob(rel, safe_rel, "120000", raw, repo_root, corpus_email_hashes)
            )
            continue
        if not full.is_file():
            continue
        scanned += 1
        raw = full.read_bytes()
        violations.extend(
            _scan_blob(rel, safe_rel, "100644", raw, repo_root, corpus_email_hashes)
        )

    return scanned, violations


def scan_history(repo_root: pathlib.Path) -> tuple[int, list[str]]:
    """Scan all commits reachable from HEAD (metadata, messages, and blobs).

    Rejects shallow repositories and reads corpus manifests strictly from each
    audited commit (never from the uncommitted Git index).
    """
    is_shallow = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"],
        cwd=repo_root,
        text=True,
    ).strip()
    if is_shallow == "true":
        return 0, ["repo:0: [shallow_repository] --check-history requires a full non-shallow clone"]

    commits = subprocess.check_output(
        ["git", "rev-list", "HEAD"],
        cwd=repo_root,
        text=True,
    ).splitlines()
    violations: list[str] = []
    seen_blob_checks: set[tuple[str, str, str, str]] = set()
    manifest_cache: dict[tuple[str | None, str | None], dict[str, str]] = {}

    for commit in commits:
        meta = subprocess.check_output(
            ["git", "show", "-s", "--format=%an%n%ae%n%cn%n%ce%n%s%n%b", commit],
            cwd=repo_root,
            text=True,
        )
        short = commit[:12]
        for lineno, line in enumerate(meta.splitlines(), 1):
            seen_meta_rules: set[str] = set()
            for match in COMBINED_ALL_RE.finditer(line):
                rule_name = match.lastgroup
                if rule_name is None or rule_name in seen_meta_rules:
                    continue
                if rule_name == "personal_email" and match.group(0).lower().endswith(
                    "@users.noreply.github.com"
                ):
                    continue
                seen_meta_rules.add(rule_name)
                violations.append(
                    f"commit:{short}:meta:{lineno}: [{rule_name}] history metadata violation"
                )

        tree_out = subprocess.check_output(
            ["git", "ls-tree", "-r", "-z", commit],
            cwd=repo_root,
        )
        entries: list[tuple[str, str, str, str]] = []
        manifest_sha: str | None = None
        migration_sha: str | None = None
        for entry in tree_out.split(b"\x00"):
            if not entry:
                continue
            header, rel_b = entry.split(b"\t", 1)
            mode, obj_type, blob_sha = header.decode("ascii").split(" ")
            rel = rel_b.decode("utf-8", errors="replace")
            entries.append((mode, obj_type, blob_sha, rel))
            if obj_type == "blob" and rel == "corpus/MANIFEST.md":
                manifest_sha = blob_sha
            elif obj_type == "blob" and rel == "legacy/migration-manifest-r1b.json":
                migration_sha = blob_sha

        mkey = (manifest_sha, migration_sha)
        if mkey not in manifest_cache:
            manifest_cache[mkey] = _load_corpus_email_hashes(repo_root, git_ref=f"{commit}:")
        corpus_email_hashes = manifest_cache[mkey]

        to_fetch: list[tuple[str, str, str, str]] = []
        for mode, obj_type, blob_sha, rel in entries:
            safe_rel = _safe_display_path(rel)
            violations.extend(_scan_path_name(rel, safe_rel, context_prefix=f"commit:{short}"))
            if obj_type != "blob":
                continue
            expected_sha = corpus_email_hashes.get(rel, "")
            ckey = (mode, blob_sha, rel, expected_sha)
            if ckey in seen_blob_checks:
                continue
            seen_blob_checks.add(ckey)
            to_fetch.append((mode, blob_sha, rel, safe_rel))

        blobs = _batch_read_git_blobs(repo_root, [sha for _, sha, _, _ in to_fetch])
        for mode, blob_sha, rel, safe_rel in to_fetch:
            violations.extend(
                _scan_blob(
                    rel,
                    safe_rel,
                    mode,
                    blobs[blob_sha],
                    repo_root,
                    corpus_email_hashes,
                    context_prefix=f"commit:{short}",
                )
            )

    return len(commits), violations


def run_self_test() -> None:
    """Negative and positive self-tests proving every hygiene rule triggers accurately."""
    secret_gh = "gh" + "p_" + "A1b2C3d4E5f6G7h8I9j0K1"
    secret_oai = "s" + "k-" + "0123456789abcdefghijklmno"
    synth_email = "alice" + "@example.org"
    negative_cases: list[tuple[str, str, str, str]] = [
        ("host_unix_path", "notes.md", "path /ho" + "me/alice/project\n", "host_unix_path"),
        ("host_media_path", "notes.md", "cache /me" + "dia/bob/disk\n", "host_unix_path"),
        ("host_macos_path", "notes.md", "path /Us" + "ers/carol/repo\n", "host_unix_path"),
        ("host_win_path", "notes.md", "path C:\\Us" + "ers\\dave\\repo\n", "host_windows_path"),
        ("file_uri", "notes.md", "file:///ho" + "me/alice/file.txt\n", "file_uri_host"),
        ("gh_token", "cfg.txt", f"token={secret_gh}\n", "secret_token"),
        ("openai_key", "cfg.txt", f"key={secret_oai}\n", "secret_token"),
        ("priv_key", "key.txt", "-----BEGIN RSA PRI" + "VATE KEY-----\n", "private_key"),
        ("basic_auth", "url.txt", "https://user:pass" + "@example.com/repo.git\n", "basic_auth_url"),
        ("bb_thread_id", "log.md", "ref " + "th" + "r_0000000000\n", "internal_bb_id"),
        ("bb_proj_id", "log.md", "ref " + "pr" + "oj_0000000000\n", "internal_bb_id"),
        ("bb_env_id", "log.md", "ref " + "en" + "v_0000000000\n", "internal_bb_id"),
        ("local_board", "doc.md", "http://127.0.0.1:44" + "100/api/board\n", "local_board_ref"),
        ("board_ticket", "doc.md", "See " + "Bo" + "ard #9999 for details\n", "local_board_ref"),
        ("email_leak", "doc.md", f"contact: {synth_email}\n", "personal_email"),
        ("env_file", ".env", "FOO=bar\n", "forbidden_env_file"),
        ("pem_file", "certs/server.pem", "placeholder\n", "forbidden_key_file"),
        ("olean_file", "build/Foo.olean", "placeholder\n", "forbidden_lean_artifact"),
        (
            "disguised_pdf_with_markers",
            "fake.pdf",
            f"%PDF-1.4\n1 0 obj\nкириллица secret {secret_gh}\nendobj\n%%EOF\n",
            "secret_token",
        ),
        ("unlisted_tex_email", "corpus/tex_src/evil.tex", f"{synth_email}\n", "personal_email"),
        ("secret_in_filename", f"docs/{secret_gh}.txt", "benign body\n", "secret_token"),
        ("email_in_pem_filename", f"certs/{synth_email}.pem", "placeholder\n", "forbidden_key_file"),
        (
            "email_filename_plus_body_secret",
            f"docs/{synth_email}.txt",
            f"token={secret_gh}\n",
            "secret_token",
        ),
    ]

    for label, rel, content, expected_rule in negative_cases:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            target = root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            _, violations = scan_tree(root, use_git=False)
            if not any(f"[{expected_rule}]" in v for v in violations):
                raise RuntimeError(
                    f"Self-test {label!r} FAILED: expected [{expected_rule}], got {violations!r}"
                )
            for v in violations:
                if secret_gh in v or secret_oai in v or synth_email in v:
                    raise RuntimeError(
                        f"Self-test {label!r} FAILED: sensitive value leaked into diagnostic: {v!r}"
                    )

    # Negative encoding tests: UTF-16 BOM, BOM-less UTF-16LE with Cyrillic, >2MiB UTF-16LE, UTF-8 with NUL
    encoding_cases: list[tuple[str, bytes]] = [
        ("utf16_bom", f"token={secret_gh}\n".encode("utf-16")),
        ("utf16_le_cyrillic", f"секретный токен {secret_gh}\n".encode("utf-16-le")),
        ("utf16_le_over_2mib", ("A" * 1_100_000 + f"\ntoken={secret_gh}\n").encode("utf-16-le")),
        ("utf8_with_nul", f"prefix\x00token={secret_gh}\n".encode("utf-8")),
    ]
    for enc_label, raw_bytes in encoding_cases:
        with tempfile.TemporaryDirectory() as td:
            root = pathlib.Path(td)
            (root / "notes.bin").write_bytes(raw_bytes)
            _, violations = scan_tree(root, use_git=False)
            if not any("[secret_token]" in v for v in violations):
                raise RuntimeError(f"Self-test {enc_label} FAILED: missed secret_token: {violations}")
            if any(secret_gh in v for v in violations):
                raise RuntimeError(f"Self-test {enc_label} FAILED: secret leaked into diagnostic!")

    # Negative symlink test: tracked .lake symlink pointing to host path
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        lake_link = root / "verification/lean/.lake"
        lake_link.parent.mkdir(parents=True, exist_ok=True)
        os.symlink("/me" + "dia/bob/lean-cache/.lake", lake_link)
        _, violations = scan_tree(root, use_git=False)
        if not any("[forbidden_lean_artifact]" in v for v in violations):
            raise RuntimeError(f"Symlink self-test missed forbidden_lean_artifact: {violations}")
        if not any("[absolute_symlink]" in v for v in violations):
            raise RuntimeError(f"Symlink self-test missed absolute_symlink: {violations}")
        if not any("[host_unix_path]" in v for v in violations):
            raise RuntimeError(f"Symlink self-test missed host_unix_path: {violations}")

    # Negative Git index snapshot test: staged secret caught even if working-tree file is overwritten or deleted
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        git_env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "ARO Contributor",
            "GIT_AUTHOR_EMAIL": "aro-contributors" + "@users.noreply.github.com",
            "GIT_COMMITTER_NAME": "ARO Contributor",
            "GIT_COMMITTER_EMAIL": "aro-contributors" + "@users.noreply.github.com",
        }
        subprocess.check_call(["git", "init", "-q"], cwd=root, env=git_env)
        staged = root / "staged_secret.txt"
        staged.write_text(f"token={secret_gh}\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "staged_secret.txt"], cwd=root, env=git_env)
        staged.write_text("clean on disk\n", encoding="utf-8")
        _, idx_overwritten = scan_tree(root, use_git=True)
        if not any("[secret_token]" in v for v in idx_overwritten):
            raise RuntimeError(f"Git index overwrite self-test missed staged secret: {idx_overwritten}")
        staged.unlink()
        _, idx_deleted = scan_tree(root, use_git=True)
        if not any("[secret_token]" in v for v in idx_deleted):
            raise RuntimeError(f"Git index delete self-test missed staged secret: {idx_deleted}")

    # Negative & positive --check-history self-test (clean, dirty, shallow clone, uncommitted index manifest)
    with tempfile.TemporaryDirectory() as td:
        base = pathlib.Path(td)
        root = base / "origin"
        root.mkdir()
        git_env = {
            **os.environ,
            "GIT_AUTHOR_NAME": "ARO Contributor",
            "GIT_AUTHOR_EMAIL": "aro-contributors" + "@users.noreply.github.com",
            "GIT_COMMITTER_NAME": "ARO Contributor",
            "GIT_COMMITTER_EMAIL": "aro-contributors" + "@users.noreply.github.com",
        }
        subprocess.check_call(["git", "init", "-q"], cwd=root, env=git_env)
        (root / "clean.txt").write_text("clean content\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "clean.txt"], cwd=root, env=git_env)
        subprocess.check_call(["git", "commit", "-q", "-m", "initial clean"], cwd=root, env=git_env)
        _, clean_hist = scan_history(root)
        if clean_hist:
            raise RuntimeError(f"Clean history self-test failed: {clean_hist}")

        # Commit an unlisted corpus/tex_src email without MANIFEST.md; staging MANIFEST.md in index must NOT bypass history check
        tex = root / "corpus/tex_src/p/paper.tex"
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex_bytes = f"author {synth_email}\n".encode("utf-8")
        tex.write_bytes(tex_bytes)
        subprocess.check_call(["git", "add", "corpus/tex_src/p/paper.tex"], cwd=root, env=git_env)
        subprocess.check_call(["git", "commit", "-q", "-m", "add tex without manifest"], cwd=root, env=git_env)
        tex_sha = hashlib.sha256(tex_bytes).hexdigest()
        (root / "corpus/MANIFEST.md").write_text(
            f"{tex_sha}  corpus/tex_src/p/paper.tex\n", encoding="utf-8"
        )
        subprocess.check_call(["git", "add", "corpus/MANIFEST.md"], cwd=root, env=git_env)
        _, staged_manifest_hist = scan_history(root)
        if not any("[personal_email]" in v for v in staged_manifest_hist):
            raise RuntimeError(
                "Uncommitted index MANIFEST.md improperly suppressed history email violation!"
            )

        # Commit 2: mismatched MANIFEST hash for paper.tex; Commit 3: matching MANIFEST hash.
        # History cache must NOT let Commit 3's match mask Commit 2's mismatch!
        (root / "corpus/MANIFEST.md").write_text(
            f"{'0' * 64}  corpus/tex_src/p/paper.tex\n", encoding="utf-8"
        )
        subprocess.check_call(["git", "add", "corpus/MANIFEST.md"], cwd=root, env=git_env)
        subprocess.check_call(["git", "commit", "-q", "-m", "bad manifest hash"], cwd=root, env=git_env)
        (root / "corpus/MANIFEST.md").write_text(
            f"{tex_sha}  corpus/tex_src/p/paper.tex\n", encoding="utf-8"
        )
        subprocess.check_call(["git", "add", "corpus/MANIFEST.md"], cwd=root, env=git_env)
        subprocess.check_call(["git", "commit", "-q", "-m", "fix manifest hash"], cwd=root, env=git_env)
        _, mismatched_hist = scan_history(root)
        if not any("[personal_email]" in v for v in mismatched_hist):
            raise RuntimeError(
                "History cache improperly masked older commit with mismatched MANIFEST hash!"
            )

        # Commit 4: subject line with BOTH personal email and GitHub noreply email must still flag personal email
        (root / "clean2.txt").write_text("ok\n", encoding="utf-8")
        subprocess.check_call(["git", "add", "clean2.txt"], cwd=root, env=git_env)
        subprocess.check_call(
            [
                "git",
                "commit",
                "-q",
                "-m",
                f"co-authored by {synth_email} and aro-contributors" + "@users.noreply.github.com",
            ],
            cwd=root,
            env=git_env,
        )
        _, noreply_mix_hist = scan_history(root)
        if not any(":meta:" in v and "[personal_email]" in v for v in noreply_mix_hist):
            raise RuntimeError(
                "GitHub noreply suffix improperly masked another email on the same metadata line!"
            )

        shallow = base / "shallow"
        subprocess.check_call(
            ["git", "clone", "-q", "--depth=1", f"file://{root}", str(shallow)],
            env=git_env,
        )
        _, shallow_hist = scan_history(shallow)
        if not any("[shallow_repository]" in v for v in shallow_hist):
            raise RuntimeError(f"Shallow history self-test missed rejection: {shallow_hist}")

    # Positive cases: benign Python variables, portable paths, and SHA-256-verified corpus/tex_src email
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "learn.py").write_text(
            "env_server = os.environ.get('ARO_LH_STANDALONE')\n"
            "env_guides = os.environ.get('ARO_GUIDES_ROOT')\n"
            "cache = '<lean-cache>/.lake'\n",
            encoding="utf-8",
        )
        tex = root / "corpus/tex_src/paper/main.tex"
        tex.parent.mkdir(parents=True, exist_ok=True)
        tex_bytes = ("\\author{Author\\thanks{author" + "@university.edu}}\n").encode("utf-8")
        tex.write_bytes(tex_bytes)
        tex_sha = hashlib.sha256(tex_bytes).hexdigest()
        (root / "corpus/MANIFEST.md").write_text(
            f"{tex_sha}  corpus/tex_src/paper/main.tex\n", encoding="utf-8"
        )
        _, violations = scan_tree(root, use_git=False)
        if violations:
            raise RuntimeError(f"Self-test positive case FAILED with unexpected violations: {violations}")

    print(
        f"PUBLIC HYGIENE SELF-TEST OK: {len(negative_cases)} content/path + {len(encoding_cases)} encoding + "
        "1 symlink + 2 index-snapshot + 3 history (clean/uncommitted-manifest/shallow) + 2 positive controls verified (zero leak echo)"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify public-repository hygiene across the Git index snapshot."
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run negative and positive self-tests in isolated temporary directories.",
    )
    parser.add_argument(
        "--check-history",
        action="store_true",
        help="Audit all commits reachable from HEAD (metadata, messages, and blobs; rejects shallow clones).",
    )
    parser.add_argument(
        "--root",
        type=pathlib.Path,
        default=ROOT,
        help="Repository root to scan (default: auto-detected).",
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    repo_root = args.root.resolve()
    if args.check_history:
        commit_count, violations = scan_history(repo_root)
        if violations:
            print(
                f"PUBLIC HISTORY HYGIENE FAILED ({len(violations)} violation(s) across {commit_count} commits):",
                file=sys.stderr,
            )
            for v in violations[:50]:
                print(f"  - {v}", file=sys.stderr)
            if len(violations) > 50:
                print(f"  ... and {len(violations) - 50} more", file=sys.stderr)
            return 1
        print(f"PUBLIC HISTORY HYGIENE OK: {commit_count} reachable commits verified, 0 violations")
        return 0

    scanned, violations = scan_tree(repo_root, use_git=True)
    if violations:
        print(
            f"PUBLIC HYGIENE FAILED ({len(violations)} violation(s) across {scanned} indexed blobs):",
            file=sys.stderr,
        )
        for v in violations[:50]:
            print(f"  - {v}", file=sys.stderr)
        if len(violations) > 50:
            print(f"  ... and {len(violations) - 50} more", file=sys.stderr)
        return 1

    print(f"PUBLIC HYGIENE OK: {scanned} indexed blobs verified, 0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
