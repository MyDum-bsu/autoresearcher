#!/usr/bin/env python3
"""HTTP API bridge from aro-discovery v2 to LearnHarness v0.7.0.

Contract:
  - Exports study packs exclusively via POST /api/graph/import (multipart files + paths).
  - Strictly idempotent repeat pushes by default: checks server source presence + content
    SHA-256 sync state and skips unchanged files (`skipped_unchanged`) unless `--force`.
  - Creates Teach/Practice sessions exclusively via POST /api/chats (+ graphContext).
  - Never writes directly to LearnHarness graph ledgers (nodes.jsonl / chains.jsonl).
  - Bypasses system HTTP proxy for loopback URLs without mutating environment variables.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from collections.abc import Sequence
from typing import Any

from learn import (
    DEFAULT_LH_URL,
    DEFAULT_ROOT_PREFIX,
    DEFAULT_TRACK,
    MAX_GRAPH_CONTEXT_PICKS,
    default_push_state_file,
)
from learn.build_pack import PackBuildError, PackEntry, StudyPack, build_study_pack

LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


class LearnHarnessAPIError(RuntimeError):
    """Raised when a LearnHarness HTTP API call fails or returns an invalid payload."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


@dataclasses.dataclass(frozen=True)
class ImportFileOutcome:
    file_path: str
    outcome: str
    ok: bool
    nodes: int
    chains: int
    error: str | None = None
    code: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "filePath": self.file_path,
            "outcome": self.outcome,
            "ok": self.ok,
            "stats": {"nodes": self.nodes, "chains": self.chains},
            **({"error": self.error} if self.error is not None else {}),
            **({"code": self.code} if self.code is not None else {}),
        }


@dataclasses.dataclass(frozen=True)
class PushResult:
    base_url: str
    folder_prefix: str
    dry_run: bool
    results: tuple[ImportFileOutcome, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "base_url": self.base_url,
            "folder_prefix": self.folder_prefix,
            "dry_run": self.dry_run,
            "results": [r.to_dict() for r in self.results],
        }


@dataclasses.dataclass(frozen=True)
class StudySessionResult:
    chat_id: str
    title: str
    mode: str
    url: str
    dry_run: bool
    propositions: tuple[dict[str, str], ...]

    def to_dict(self) -> dict[str, Any]:
        graph_ctx = {"propositions": list(self.propositions)} if self.propositions else None
        return {
            "id": self.chat_id,
            "title": self.title,
            "mode": self.mode,
            "url": self.url,
            "dry_run": self.dry_run,
            "proposition_count": len(self.propositions),
            "graphContext": graph_ctx,
        }


def _normalize_base_url(base_url: str) -> str:
    cleaned = base_url.strip().rstrip("/")
    parsed = urllib.parse.urlparse(cleaned)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise LearnHarnessAPIError(f"Invalid LearnHarness base URL: {base_url!r}")
    return cleaned


def _opener_for_url(url: str) -> urllib.request.OpenerDirector:
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    if host in LOOPBACK_HOSTS:
        return urllib.request.build_opener(urllib.request.ProxyHandler({}))
    return urllib.request.build_opener()


def _http_request_json(
    url: str,
    *,
    method: str = "GET",
    body: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    opener = _opener_for_url(url)
    try:
        with opener.open(req, timeout=timeout) as resp:
            status = resp.status
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except (TimeoutError, OSError):
            detail = str(exc)
        raise LearnHarnessAPIError(
            f"{method} {url} failed with HTTP {exc.code}: {detail}",
            status_code=exc.code,
        ) from exc
    except urllib.error.URLError as exc:
        raise LearnHarnessAPIError(f"{method} {url} connection error: {exc.reason}") from exc
    except (TimeoutError, OSError) as exc:
        raise LearnHarnessAPIError(f"{method} {url} timeout/IO error: {exc}") from exc

    if status < 200 or status >= 300:
        raise LearnHarnessAPIError(
            f"{method} {url} returned unexpected HTTP {status}: {raw}",
            status_code=status,
        )
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise LearnHarnessAPIError(f"{method} {url} returned invalid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise LearnHarnessAPIError(f"{method} {url} returned non-object JSON payload")
    return parsed


def _escape_disposition(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def encode_multipart_import(
    pack: StudyPack,
    boundary: str | None = None,
    *,
    entries: Sequence[PackEntry] | None = None,
) -> tuple[bytes, str]:
    """Build multipart/form-data payload with repeated `files` and `paths` fields."""
    selected = tuple(pack.entries if entries is None else entries)
    bnd = boundary or f"----aro-lh-import-{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    bnd_bytes = bnd.encode("ascii")

    for entry in selected:
        raw = entry.source_path.read_bytes()
        safe_name = _escape_disposition(entry.filename)
        chunks.append(
            b"--" + bnd_bytes + b"\r\n"
            + f'Content-Disposition: form-data; name="files"; filename="{safe_name}"\r\n'.encode()
            + b"Content-Type: text/markdown; charset=utf-8\r\n\r\n"
            + raw
            + b"\r\n"
        )

    for entry in selected:
        chunks.append(
            b"--" + bnd_bytes + b"\r\n"
            + b'Content-Disposition: form-data; name="paths"\r\n\r\n'
            + entry.relative_path.encode("utf-8")
            + b"\r\n"
        )

    chunks.append(b"--" + bnd_bytes + b"--\r\n")
    return b"".join(chunks), f"multipart/form-data; boundary={bnd}"


def _read_push_state(state_file: pathlib.Path) -> dict[str, Any]:
    if not state_file.is_file():
        return {"version": 1, "targets": {}}
    try:
        data = json.loads(state_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "targets": {}}
    if not isinstance(data, dict) or not isinstance(data.get("targets"), dict):
        return {"version": 1, "targets": {}}
    return data


def _write_push_state(state_file: pathlib.Path, state: dict[str, Any]) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_file.with_suffix(f".tmp.{os.getpid()}")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(state_file)


def _fetch_server_notes_sources(
    base_url: str, *, timeout: float = 30.0
) -> dict[str, dict[str, str]]:
    """Query existing imported notes sources from LearnHarness (fail-closed on errors)."""
    existing: dict[str, dict[str, str]] = {}
    try:
        resp = _http_request_json(f"{base_url}/api/graph/sources", method="GET", timeout=timeout)
        for src in resp.get("sources", []):
            if (
                isinstance(src, dict)
                and src.get("kind") == "notes"
                and isinstance(src.get("id"), str)
            ):
                existing[src["id"]] = {
                    "filePath": str(src.get("filePath") or ""),
                    "createdAt": str(src.get("createdAt") or ""),
                }
        return existing
    except LearnHarnessAPIError as exc:
        if exc.status_code != 404:
            raise LearnHarnessAPIError(
                f"Cannot verify existing LearnHarness sources (fail-closed; use --force to "
                f"bypass): {exc}",
                status_code=exc.status_code,
            ) from exc

    # Only fall back to GET /api/graph when /api/graph/sources is 404 (older mock/server)
    graph = _http_request_json(f"{base_url}/api/graph", method="GET", timeout=timeout)
    fmap = graph.get("fileSources")
    if isinstance(fmap, dict):
        for sid, fpath in fmap.items():
            if isinstance(sid, str) and isinstance(fpath, str):
                existing[sid] = {"filePath": fpath, "createdAt": ""}
    return existing


def push_pack(
    pack: StudyPack,
    base_url: str = DEFAULT_LH_URL,
    *,
    dry_run: bool = False,
    force: bool = False,
    state_file: pathlib.Path | None = None,
    timeout: float = 180.0,
) -> PushResult:
    """Import pack files into LearnHarness via POST /api/graph/import.

    Idempotent by default: files already present on the server with matching content
    SHA-256 in the client sync state are skipped (`outcome="skipped_unchanged"`)
    with 0 import POST / LLM calls unless `force=True`.
    """
    base = _normalize_base_url(base_url)
    if dry_run:
        simulated = tuple(
            ImportFileOutcome(
                file_path=e.relative_path,
                outcome="dry-run",
                ok=True,
                nodes=0,
                chains=0,
            )
            for e in pack.entries
        )
        return PushResult(
            base_url=base,
            folder_prefix=pack.folder_prefix,
            dry_run=True,
            results=simulated,
        )

    resolved_state_file = (state_file or default_push_state_file()).expanduser()
    state = _read_push_state(resolved_state_file)
    target_cache = state.setdefault("targets", {}).setdefault(base, {})
    if not isinstance(target_cache, dict):
        target_cache = {}
        state["targets"][base] = target_cache

    to_upload: list[PackEntry] = []
    skipped_by_path: dict[str, ImportFileOutcome] = {}
    if force:
        to_upload = list(pack.entries)
    else:
        server_sources = _fetch_server_notes_sources(base, timeout=min(timeout, 30.0))
        for entry in pack.entries:
            cached = target_cache.get(entry.source_id)
            server_rec = server_sources.get(entry.source_id)
            same_hash = isinstance(cached, dict) and cached.get("sha256") == entry.sha256
            same_stamp = (
                server_rec is not None
                and isinstance(cached, dict)
                and (
                    not cached.get("createdAt")
                    or not server_rec.get("createdAt")
                    or cached.get("createdAt") == server_rec.get("createdAt")
                )
            )
            if server_rec is not None and same_hash and same_stamp:
                skipped_by_path[entry.relative_path] = ImportFileOutcome(
                    file_path=entry.relative_path,
                    outcome="skipped_unchanged",
                    ok=True,
                    nodes=0,
                    chains=0,
                )
            else:
                to_upload.append(entry)

    uploaded_by_path: dict[str, ImportFileOutcome] = {}
    if to_upload:
        body, content_type = encode_multipart_import(pack, entries=to_upload)
        payload = _http_request_json(
            f"{base}/api/graph/import",
            method="POST",
            body=body,
            headers={"Content-Type": content_type},
            timeout=timeout,
        )
        raw_results = payload.get("results")
        if not isinstance(raw_results, list):
            raise LearnHarnessAPIError(
                f"POST /api/graph/import missing 'results' list: {payload}"
            )

        for item in raw_results:
            if not isinstance(item, dict):
                raise LearnHarnessAPIError(f"Malformed import result entry: {item!r}")
            stats = item.get("stats") if isinstance(item.get("stats"), dict) else {}
            rec = ImportFileOutcome(
                file_path=str(item.get("filePath", "")),
                outcome=str(item.get("outcome", "unknown")),
                ok=bool(item.get("ok", False)),
                nodes=int(stats.get("nodes", 0) or 0),
                chains=int(stats.get("chains", 0) or 0),
                error=str(item["error"]) if item.get("error") is not None else None,
                code=str(item["code"]) if item.get("code") is not None else None,
            )
            uploaded_by_path[rec.file_path] = rec

        failures: list[str] = []
        for entry in to_upload:
            rec = uploaded_by_path.get(entry.relative_path)
            if rec is None:
                failures.append(f"{entry.relative_path}: missing from server response")
            elif not rec.ok or rec.outcome != "completed":
                detail = rec.error or rec.code or rec.outcome
                failures.append(f"{entry.relative_path}: outcome={rec.outcome} ({detail})")

        if failures:
            raise LearnHarnessAPIError(
                "POST /api/graph/import did not complete cleanly:\n  - "
                + "\n  - ".join(failures)
            )

        # Record server timestamps + content hashes for idempotent repeat pushes
        post_sources = _fetch_server_notes_sources(base, timeout=min(timeout, 30.0))
        for entry in to_upload:
            srv_rec = post_sources.get(entry.source_id, {})
            target_cache[entry.source_id] = {
                "filePath": entry.relative_path,
                "sha256": entry.sha256,
                "createdAt": srv_rec.get("createdAt", ""),
            }
        _write_push_state(resolved_state_file, state)

    ordered_outcomes = tuple(
        skipped_by_path[e.relative_path]
        if e.relative_path in skipped_by_path
        else uploaded_by_path[e.relative_path]
        for e in pack.entries
    )
    return PushResult(
        base_url=base,
        folder_prefix=pack.folder_prefix,
        dry_run=False,
        results=ordered_outcomes,
    )


def fetch_topic_propositions(
    pack: StudyPack,
    base_url: str = DEFAULT_LH_URL,
    *,
    timeout: float = 30.0,
) -> tuple[dict[str, str], ...]:
    """Read GET /api/graph (+ /api/graph/sources) and select propositions for pack."""
    base = _normalize_base_url(base_url)
    graph = _http_request_json(f"{base}/api/graph", method="GET", timeout=timeout)
    # Prefer `propositions` (stored nodes only, excluding derived `arg_*` implication nodes)
    raw_nodes = graph.get("propositions")
    if not isinstance(raw_nodes, list):
        raw_nodes = graph.get("nodes")
    if not isinstance(raw_nodes, list):
        raise LearnHarnessAPIError(f"GET /api/graph missing 'propositions'/'nodes' list: {graph}")

    matching_source_ids = set(pack.source_ids)
    file_sources = graph.get("fileSources")
    if isinstance(file_sources, dict):
        for sid, fpath in file_sources.items():
            if (
                isinstance(sid, str)
                and isinstance(fpath, str)
                and fpath.startswith(pack.folder_prefix)
            ):
                matching_source_ids.add(sid)

    try:
        sources_resp = _http_request_json(
            f"{base}/api/graph/sources", method="GET", timeout=timeout
        )
        for src in sources_resp.get("sources", []):
            if (
                isinstance(src, dict)
                and isinstance(src.get("id"), str)
                and isinstance(src.get("filePath"), str)
                and src["filePath"].startswith(pack.folder_prefix)
            ):
                matching_source_ids.add(src["id"])
    except LearnHarnessAPIError:
        pass

    picks: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for node in raw_nodes:
        if not isinstance(node, dict):
            continue
        nid = node.get("id")
        name = node.get("name")
        statement = node.get("statement")
        provenance = node.get("provenance")
        if not (
            isinstance(nid, str)
            and not nid.startswith("arg_")
            and isinstance(name, str)
            and isinstance(statement, str)
            and isinstance(provenance, list)
        ):
            continue
        if nid in seen_ids:
            continue
        belongs = any(
            isinstance(pt, dict) and pt.get("chatId") in matching_source_ids
            for pt in provenance
        )
        if belongs:
            seen_ids.add(nid)
            picks.append({"id": nid, "name": name, "statement": statement})

    picks.sort(key=lambda p: p["id"])
    return tuple(picks[:MAX_GRAPH_CONTEXT_PICKS])


def create_study_session(
    pack: StudyPack,
    base_url: str = DEFAULT_LH_URL,
    *,
    mode: str = "teach",
    title: str | None = None,
    propositions: tuple[dict[str, str], ...] | list[dict[str, str]] | None = None,
    allow_empty_context: bool = False,
    dry_run: bool = False,
    timeout: float = 30.0,
) -> StudySessionResult:
    """Create a LearnHarness Teach or Practice session via POST /api/chats."""
    if mode not in ("teach", "practice"):
        raise ValueError(f"Unsupported study mode: {mode!r} (expected 'teach' or 'practice')")

    base = _normalize_base_url(base_url)
    session_title = title or f"ARO {mode.capitalize()}: {pack.topic}"

    selected: tuple[dict[str, str], ...]
    if propositions is not None:
        selected = tuple(
            {
                "id": str(p["id"]),
                "name": str(p["name"]),
                "statement": str(p["statement"]),
            }
            for p in propositions[:MAX_GRAPH_CONTEXT_PICKS]
        )
    elif mode == "practice" and not dry_run:
        selected = fetch_topic_propositions(pack, base, timeout=timeout)
    else:
        selected = ()

    if mode == "practice" and not dry_run and not selected and not allow_empty_context:
        raise LearnHarnessAPIError(
            f"No propositions found in LearnHarness graph for {pack.folder_prefix}. "
            "Run `push` first (or pass --push-first / --allow-empty-context)."
        )

    request_body: dict[str, Any] = {"title": session_title}
    if mode == "practice":
        request_body["kind"] = "practice"
    if selected:
        request_body["graphContext"] = {"propositions": list(selected)}

    if dry_run:
        return StudySessionResult(
            chat_id="dry-run-session",
            title=session_title,
            mode=mode,
            url=f"{base}/chat/dry-run-session",
            dry_run=True,
            propositions=selected,
        )

    resp = _http_request_json(
        f"{base}/api/chats",
        method="POST",
        body=json.dumps(request_body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        timeout=timeout,
    )
    chat_id = resp.get("id")
    if not isinstance(chat_id, str) or not chat_id:
        raise LearnHarnessAPIError(f"POST /api/chats returned invalid id: {resp}")
    returned_title = str(resp.get("title") or session_title)
    encoded_id = urllib.parse.quote(chat_id, safe="")
    return StudySessionResult(
        chat_id=chat_id,
        title=returned_title,
        mode=mode,
        url=f"{base}/chat/{encoded_id}",
        dry_run=False,
        propositions=selected,
    )


def _add_pack_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("topic", help="Guide topic directory under research/guides/")
    parser.add_argument("--track", default=DEFAULT_TRACK)
    parser.add_argument("--root-prefix", default=DEFAULT_ROOT_PREFIX)
    parser.add_argument("--guides-root", type=pathlib.Path, default=None)
    parser.add_argument(
        "--url",
        default=os.environ.get("ARO_LH_URL", DEFAULT_LH_URL),
        help="LearnHarness server URL (default: $ARO_LH_URL or http://127.0.0.1:3000)",
    )
    parser.add_argument(
        "--state-file",
        type=pathlib.Path,
        default=None,
        help="Client-side push SHA-256 sync state file (default: $ARO_LH_STATE_FILE)",
    )
    parser.add_argument("--force", action="store_true", help="Re-import unchanged files")
    parser.add_argument("--timeout", type=float, default=180.0, help="HTTP timeout in seconds")
    parser.add_argument("--validate-gate", action="store_true")
    parser.add_argument("--no-style", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Push study packs and start Teach/Practice sessions in LearnHarness v0.7.0."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_push = sub.add_parser("push", help="Import guide pack via POST /api/graph/import")
    _add_pack_args(p_push)

    p_study = sub.add_parser("study", help="Create Teach or Practice session via POST /api/chats")
    _add_pack_args(p_study)
    p_study.add_argument("--mode", choices=("teach", "practice"), default="teach")
    p_study.add_argument("--title", default=None)
    p_study.add_argument(
        "--push-first",
        action="store_true",
        help="Import pack before creating session",
    )
    p_study.add_argument("--allow-empty-context", action="store_true")

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
        if args.command == "push":
            res = push_pack(
                pack,
                args.url,
                dry_run=args.dry_run,
                force=args.force,
                state_file=args.state_file,
                timeout=args.timeout,
            )
            if args.json:
                print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
            else:
                print(f"PUSH OK ({res.folder_prefix} -> {res.base_url}):")
                for item in res.results:
                    print(
                        f"  - {item.file_path}: {item.outcome} "
                        f"(nodes={item.nodes}, chains={item.chains})"
                    )
            return 0

        push_res: PushResult | None = None
        if args.push_first:
            push_res = push_pack(
                pack,
                args.url,
                dry_run=args.dry_run,
                force=args.force,
                state_file=args.state_file,
                timeout=args.timeout,
            )
        sess = create_study_session(
            pack,
            args.url,
            mode=args.mode,
            title=args.title,
            allow_empty_context=args.allow_empty_context,
            dry_run=args.dry_run,
            timeout=args.timeout,
        )
        if args.json:
            out: dict[str, Any] = {"session": sess.to_dict()}
            if push_res is not None:
                out["push"] = push_res.to_dict()
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"STUDY SESSION READY ({sess.mode}): {sess.title}")
            print(f"  url: {sess.url}")
            print(f"  propositions in graphContext: {len(sess.propositions)}")
        return 0
    except (PackBuildError, LearnHarnessAPIError, ValueError) as exc:
        print(f"push_to_lh error: {exc}", file=sys.stderr)
        return 1


def aro_cli(argv: list[str] | None = None) -> int:
    """Console entrypoint for `aro study <topic> --mode teach|practice` & `aro push <topic>`."""
    return main(argv)


if __name__ == "__main__":
    sys.exit(main())
