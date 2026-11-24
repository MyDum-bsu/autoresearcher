"""Unit tests for learn/push_to_lh.py and learn/pull_lh_context.py (mock HTTP + isolated dir)."""

from __future__ import annotations

import http.server
import io
import json
import os
import pathlib
import socketserver
import subprocess
import tempfile
import threading
import unittest
from contextlib import redirect_stderr
from typing import Any
from unittest import mock

from learn.build_pack import build_study_pack, compute_lh_source_id
from learn.pull_lh_context import (
    ContextPullError,
    format_markdown,
    pull_aro_context,
    resolve_graph_script,
)
from learn.pull_lh_context import (
    main as pull_main,
)
from learn.push_to_lh import (
    LearnHarnessAPIError,
    create_study_session,
    encode_multipart_import,
    fetch_topic_propositions,
    push_pack,
)
from learn.push_to_lh import (
    main as push_main,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


class _MockLHServer:
    """In-process HTTP mock implementing LearnHarness v0.7.0 route contracts."""

    def __init__(self) -> None:
        self.requests: list[dict[str, Any]] = []
        self.import_handler: Any = None
        self.graph_payload: dict[str, Any] = {
            "nodes": [],
            "propositions": [],
            "chains": [],
            "fileSources": {},
        }
        self.sources_payload: dict[str, Any] = {"organization": {}, "sources": []}
        self.sources_status = 200
        self.chat_counter = 0

        parent = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002, ARG002
                return

            def _send_json(self, code: int, payload: dict[str, Any]) -> None:
                raw = json.dumps(payload).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            def do_GET(self) -> None:
                parent.requests.append({"method": "GET", "path": self.path})
                if self.path == "/api/graph":
                    self._send_json(200, parent.graph_payload)
                elif self.path == "/api/graph/sources":
                    if parent.sources_status != 200:
                        self._send_json(
                            parent.sources_status, {"error": "temporary sources failure"}
                        )
                    else:
                        self._send_json(200, parent.sources_payload)
                else:
                    self._send_json(404, {"error": "not found"})

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length)
                ctype = self.headers.get("Content-Type", "")
                parent.requests.append(
                    {"method": "POST", "path": self.path, "content_type": ctype, "body": raw}
                )
                if self.path == "/api/graph/import":
                    if parent.import_handler is not None:
                        code, payload = parent.import_handler(raw, ctype)
                        self._send_json(code, payload)
                    else:
                        self._send_json(200, {"results": []})
                elif self.path == "/api/chats":
                    body = json.loads(raw.decode("utf-8"))
                    parent.chat_counter += 1
                    cid = f"chat_mock_{parent.chat_counter}"
                    self._send_json(200, {"id": cid, "title": body.get("title", "Untitled")})
                else:
                    self._send_json(404, {"error": "not found"})

        self._httpd = socketserver.TCPServer(("127.0.0.1", 0), Handler)
        self.port = self._httpd.server_address[1]
        self.url = f"http://127.0.0.1:{self.port}"
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)

    def __enter__(self) -> _MockLHServer:
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)


class TestPushAndPullUnit(unittest.TestCase):
    def setUp(self) -> None:
        self.pack = build_study_pack("01-bridge-packet-01", repo_root=REPO_ROOT)
        self._tmp = tempfile.TemporaryDirectory(prefix="aro-r5-unit-")
        self.tmp_path = pathlib.Path(self._tmp.name)
        self.state_file = self.tmp_path / "push-state.json"

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_multipart_payload_contains_files_and_paths_in_order(self) -> None:
        body, ctype = encode_multipart_import(self.pack, boundary="TESTBND")
        self.assertEqual(ctype, "multipart/form-data; boundary=TESTBND")
        decoded = body.decode("utf-8")
        for entry in self.pack.entries:
            self.assertIn(f'name="files"; filename="{entry.filename}"', decoded)
            self.assertIn(f'name="paths"\r\n\r\n{entry.relative_path}\r\n', decoded)

    def test_dry_run_makes_zero_http_calls_and_writes_no_state(self) -> None:
        res = push_pack(self.pack, "http://127.0.0.1:1", dry_run=True, state_file=self.state_file)
        self.assertTrue(res.dry_run)
        self.assertEqual(len(res.results), 4)
        self.assertTrue(all(r.outcome == "dry-run" for r in res.results))
        self.assertFalse(self.state_file.exists())

        sess = create_study_session(self.pack, "http://127.0.0.1:1", mode="practice", dry_run=True)
        self.assertTrue(sess.dry_run)
        self.assertEqual(sess.mode, "practice")
        self.assertEqual(sess.url, "http://127.0.0.1:1/chat/dry-run-session")

    def test_push_idempotent_repeat_skips_unchanged_and_force_reuploads(self) -> None:
        with _MockLHServer() as srv:

            def _do_import(_raw: bytes, _ct: str) -> tuple[int, dict[str, Any]]:
                srv.sources_payload = {
                    "organization": {},
                    "sources": [
                        {
                            "id": e.source_id,
                            "kind": "notes",
                            "filePath": e.relative_path,
                            "createdAt": "2026-11-23T00:00:00.000Z",
                        }
                        for e in self.pack.entries
                    ],
                }
                return (
                    200,
                    {
                        "results": [
                            {
                                "requestIndex": i,
                                "filePath": e.relative_path,
                                "outcome": "completed",
                                "ok": True,
                                "stats": {"nodes": 2, "chains": 1},
                            }
                            for i, e in enumerate(self.pack.entries)
                        ]
                    },
                )

            srv.import_handler = _do_import

            # Push 1: uploads all 4 files
            r1 = push_pack(self.pack, srv.url, state_file=self.state_file)
            self.assertTrue(all(item.outcome == "completed" for item in r1.results))
            import_posts_1 = [r for r in srv.requests if r["path"] == "/api/graph/import"]
            self.assertEqual(len(import_posts_1), 1)

            # Push 2 (default idempotent): 0 new POST /api/graph/import calls!
            r2 = push_pack(self.pack, srv.url, state_file=self.state_file)
            self.assertTrue(
                all(item.outcome == "skipped_unchanged" and item.ok for item in r2.results)
            )
            import_posts_2 = [r for r in srv.requests if r["path"] == "/api/graph/import"]
            self.assertEqual(len(import_posts_2), 1)

            # Push 3 (--force): forces re-upload
            r3 = push_pack(self.pack, srv.url, force=True, state_file=self.state_file)
            self.assertTrue(all(item.outcome == "completed" for item in r3.results))
            import_posts_3 = [r for r in srv.requests if r["path"] == "/api/graph/import"]
            self.assertEqual(len(import_posts_3), 2)

    def test_push_fails_closed_on_sources_503_with_zero_posts(self) -> None:
        with _MockLHServer() as srv:
            srv.sources_status = 503
            with self.assertRaises(LearnHarnessAPIError) as ctx:
                push_pack(self.pack, srv.url, state_file=self.state_file)
            self.assertEqual(ctx.exception.status_code, 503)
            self.assertIn("fail-closed", str(ctx.exception))
            posts = [r for r in srv.requests if r["method"] == "POST"]
            self.assertEqual(len(posts), 0, "Fail-closed must NOT POST when sources GET fails")

    def test_push_and_study_against_mock_http_server(self) -> None:
        with _MockLHServer() as srv:
            srv.import_handler = lambda _raw, _ct: (
                200,
                {
                    "results": [
                        {
                            "requestIndex": i,
                            "filePath": e.relative_path,
                            "outcome": "completed",
                            "ok": True,
                            "stats": {"nodes": 2, "chains": 1},
                        }
                        for i, e in enumerate(self.pack.entries)
                    ]
                },
            )
            src_id = self.pack.entries[1].source_id
            srv.graph_payload = {
                "propositions": [
                    {
                        "id": "n_aaaaaaaaaaaa",
                        "name": "Exogenous deviation",
                        "statement": "x_r = s_0(a) + xi separates nominal and disturbance",
                        "provenance": [{"chatId": src_id, "messageId": ""}],
                    },
                    {
                        "id": "n_bbbbbbbbbbbb",
                        "name": "Unrelated topic",
                        "statement": "Should be filtered out",
                        "provenance": [{"chatId": "src_other0000000", "messageId": ""}],
                    },
                ],
                "nodes": [
                    {
                        "id": "n_aaaaaaaaaaaa",
                        "name": "Exogenous deviation",
                        "statement": "x_r = s_0(a) + xi separates nominal and disturbance",
                        "provenance": [{"chatId": src_id, "messageId": ""}],
                    },
                    {
                        "id": "arg_cccccccccccc",
                        "name": "⟹",
                        "statement": "Derived implication node",
                        "provenance": [{"chatId": src_id, "messageId": ""}],
                    },
                ],
                "fileSources": {src_id: self.pack.entries[1].relative_path},
            }

            push_res = push_pack(self.pack, srv.url, state_file=self.state_file)
            self.assertFalse(push_res.dry_run)
            self.assertEqual(len(push_res.results), 4)
            self.assertTrue(all(r.outcome == "completed" and r.ok for r in push_res.results))

            picks = fetch_topic_propositions(self.pack, srv.url)
            self.assertEqual(len(picks), 1)
            self.assertEqual(picks[0]["id"], "n_aaaaaaaaaaaa")

            practice = create_study_session(self.pack, srv.url, mode="practice")
            self.assertEqual(practice.mode, "practice")
            self.assertEqual(len(practice.propositions), 1)
            self.assertEqual(practice.url, f"{srv.url}/chat/{practice.chat_id}")

            teach = create_study_session(self.pack, srv.url, mode="teach")
            self.assertEqual(teach.mode, "teach")
            self.assertEqual(len(teach.propositions), 0)

            chat_posts = [
                json.loads(r["body"].decode("utf-8"))
                for r in srv.requests
                if r["method"] == "POST" and r["path"] == "/api/chats"
            ]
            self.assertEqual(len(chat_posts), 2)
            self.assertEqual(chat_posts[0]["kind"], "practice")
            self.assertEqual(len(chat_posts[0]["graphContext"]["propositions"]), 1)
            self.assertNotIn("kind", chat_posts[1])

    def test_push_raises_on_models_not_configured_or_partial_failure(self) -> None:
        with _MockLHServer() as srv:
            srv.import_handler = lambda _raw, _ct: (
                200,
                {
                    "results": [
                        {
                            "requestIndex": 0,
                            "filePath": self.pack.entries[0].relative_path,
                            "outcome": "failed",
                            "ok": False,
                            "code": "models_not_configured",
                            "error": "Configure models first",
                        }
                    ]
                },
            )
            with self.assertRaises(LearnHarnessAPIError) as ctx:
                push_pack(self.pack, srv.url, state_file=self.state_file)
            self.assertIn("Configure models first", str(ctx.exception))

    def test_practice_raises_when_graph_has_no_topic_propositions(self) -> None:
        with _MockLHServer() as srv, self.assertRaises(LearnHarnessAPIError):
            create_study_session(self.pack, srv.url, mode="practice")

    def test_fetch_topic_propositions_caps_at_64_picks(self) -> None:
        src_id = self.pack.entries[0].source_id
        with _MockLHServer() as srv:
            srv.graph_payload = {
                "propositions": [
                    {
                        "id": f"n_{i:012d}",
                        "name": f"Prop {i}",
                        "statement": f"Statement {i}",
                        "provenance": [{"chatId": src_id, "messageId": ""}],
                    }
                    for i in range(80)
                ],
                "fileSources": {src_id: self.pack.entries[0].relative_path},
            }
            picks = fetch_topic_propositions(self.pack, srv.url)
            self.assertEqual(len(picks), 64)
            self.assertEqual(picks[0]["id"], "n_000000000000")
            self.assertEqual(picks[-1]["id"], "n_000000000063")

    def test_resp_read_timeout_error_handled_cleanly_in_api_and_cli(self) -> None:
        class _SlowBodyResp:
            status = 200

            def __enter__(self) -> _SlowBodyResp:
                return self

            def __exit__(self, *args: object) -> None:
                return None

            def read(self) -> bytes:
                raise TimeoutError("timed out while reading response body")

        class _FakeOpener:
            def open(self, _req: Any, timeout: float = 0.0) -> _SlowBodyResp:  # noqa: ARG002
                return _SlowBodyResp()

        with mock.patch("learn.push_to_lh._opener_for_url", return_value=_FakeOpener()):
            with self.assertRaises(LearnHarnessAPIError) as ctx:
                push_pack(
                    self.pack,
                    "http://127.0.0.1:9999",
                    force=True,
                    state_file=self.state_file,
                )
            self.assertIn("timeout/IO error", str(ctx.exception))

            err_buf = io.StringIO()
            with redirect_stderr(err_buf):
                rc = push_main(
                    [
                        "push",
                        "01-bridge-packet-01",
                        "--url",
                        "http://127.0.0.1:9999",
                        "--force",
                        "--state-file",
                        str(self.state_file),
                    ]
                )
            self.assertEqual(rc, 1)
            self.assertIn("timeout/IO error", err_buf.getvalue())

    def test_pull_subprocess_timeout_handled_cleanly(self) -> None:
        fake_script = self.tmp_path / "slow_graph.py"
        fake_script.write_text("import time; time.sleep(5)\n", encoding="utf-8")

        with mock.patch(
            "learn.pull_lh_context.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd=["python3"], timeout=0.1),
        ):
            with self.assertRaises(ContextPullError) as ctx:
                pull_aro_context(
                    self.tmp_path,
                    graph_script=fake_script,
                    timeout=0.1,
                )
            self.assertIn("timed out", str(ctx.exception))

            err_buf = io.StringIO()
            with redirect_stderr(err_buf):
                rc = pull_main(
                    [
                        "--data-dir",
                        str(self.tmp_path),
                        "--graph-script",
                        str(fake_script),
                        "--timeout",
                        "0.1",
                    ]
                )
            self.assertEqual(rc, 1)
            self.assertIn("timed out", err_buf.getvalue())

    def test_pull_lh_context_reads_isolated_data_dir_without_writes(self) -> None:
        clean_env = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith("ARO_LH_") and k != "LH_DATA_DIR"
        }
        with (
            mock.patch.dict(os.environ, clean_env, clear=True),
            tempfile.TemporaryDirectory(prefix="aro-r5-isolated-pull-") as tmp,
        ):
            graph_script = resolve_graph_script()
            data_dir = pathlib.Path(tmp) / "data"
            graph_dir = data_dir / "graph"
            graph_dir.mkdir(parents=True)

            aro_path = "ARO/01-Bridge-OGU-ARO/01-bridge-packet-01/02-propositions-and-chains.md"
            other_path = "Other/course/notes.md"
            aro_sid = compute_lh_source_id(aro_path)
            other_sid = compute_lh_source_id(other_path)

            (graph_dir / "format.json").write_text(json.dumps({"version": 1}), encoding="utf-8")
            (graph_dir / "sources.json").write_text(
                json.dumps(
                    {
                        aro_sid: {
                            "id": aro_sid,
                            "filePath": aro_path,
                            "importedAt": "2026-11-23T00:00:00.000Z",
                        },
                        other_sid: {
                            "id": other_sid,
                            "filePath": other_path,
                            "importedAt": "2026-11-23T00:00:00.000Z",
                        },
                    }
                ),
                encoding="utf-8",
            )
            nodes = [
                {
                    "id": "n_111111111111",
                    "name": "Prefix split",
                    "statement": "x_r(a, w^-) = s_0(a) + xi(w^-)",
                    "aliases": [],
                    "provenance": [{"chatId": aro_sid, "messageId": ""}],
                    "createdAt": "2026-11-23T00:00:01.000Z",
                },
                {
                    "id": "n_222222222222",
                    "name": "Epigraph equality",
                    "statement": "sourceLevels(D) = aroLevels(D)",
                    "aliases": [],
                    "provenance": [{"chatId": aro_sid, "messageId": ""}],
                    "createdAt": "2026-11-23T00:00:02.000Z",
                },
                {
                    "id": "n_999999999999",
                    "name": "Non-ARO note",
                    "statement": "Prefix split mentioned outside ARO",
                    "aliases": [],
                    "provenance": [{"chatId": other_sid, "messageId": ""}],
                    "createdAt": "2026-11-23T00:00:03.000Z",
                },
            ]
            (graph_dir / "nodes.jsonl").write_text(
                "\n".join(json.dumps(n) for n in nodes) + "\n", encoding="utf-8"
            )
            chains = [
                {
                    "id": "arg_111111111111",
                    "premises": ["n_111111111111"],
                    "conclusion": "n_222222222222",
                    "provenance": [{"chatId": aro_sid, "messageId": ""}],
                    "createdAt": "2026-11-23T00:00:04.000Z",
                }
            ]
            (graph_dir / "chains.jsonl").write_text(
                "\n".join(json.dumps(c) for c in chains) + "\n", encoding="utf-8"
            )

            before = {
                str(p.relative_to(data_dir)): (p.stat().st_size, p.stat().st_mtime_ns)
                for p in sorted(data_dir.rglob("*"))
                if p.is_file()
            }

            ctx = pull_aro_context(
                data_dir,
                graph_script=graph_script,
                prefix="ARO/",
                topic="01-bridge-packet-01",
            )
            self.assertEqual(ctx["summary"]["session_count"], 1)
            self.assertEqual(ctx["summary"]["proposition_count"], 2)
            self.assertEqual(ctx["summary"]["chain_count"], 1)
            self.assertEqual(
                [p["id"] for p in ctx["propositions"]],
                ["n_111111111111", "n_222222222222"],
            )
            self.assertIn("Prefix split", format_markdown(ctx))

            qctx = pull_aro_context(
                data_dir, graph_script=graph_script, prefix="ARO/", query="Prefix"
            )
            self.assertEqual([p["id"] for p in qctx["propositions"]], ["n_111111111111"])

            empty_ctx = pull_aro_context(
                data_dir,
                graph_script=graph_script,
                prefix="ARO/NonExistent/",
                query="Prefix",
            )
            self.assertEqual(empty_ctx["summary"]["proposition_count"], 0)

            after = {
                str(p.relative_to(data_dir)): (p.stat().st_size, p.stat().st_mtime_ns)
                for p in sorted(data_dir.rglob("*"))
                if p.is_file()
            }
            self.assertEqual(before, after, "pull_lh_context must be strictly read-only")


if __name__ == "__main__":
    unittest.main()
