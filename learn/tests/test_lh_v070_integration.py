"""End-to-end integration test against the real LearnHarness v0.7.0 standalone server.

Runs strictly on an isolated temporary LH_DATA_DIR and throwaway LH_AUTH_FILE with a local
deterministic mock OpenAI-compatible SSE endpoint (zero external network calls, zero API keys,
zero edits to LearnHarness, and verified zero mutations to ~/.config/LearnHarness/data).
"""

from __future__ import annotations

import http.server
import json
import os
import pathlib
import secrets
import shutil
import socket
import socketserver
import subprocess
import tempfile
import threading
import time
import unittest
import urllib.request
from typing import Any
from unittest import mock

from learn import resolve_lh_standalone
from learn.build_pack import build_study_pack
from learn.pull_lh_context import pull_aro_context, resolve_graph_script
from learn.push_to_lh import create_study_session, push_pack

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
STANDALONE_SERVER = resolve_lh_standalone()
LIVE_LH_DATA = pathlib.Path.home() / ".config/LearnHarness/data"


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _snapshot_dir(root: pathlib.Path) -> dict[str, tuple[int, int]]:
    if not root.is_dir():
        return {}
    snap: dict[str, tuple[int, int]] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            st = p.stat()
            snap[str(p.relative_to(root))] = (st.st_size, st.st_mtime_ns)
    return snap


def _sse_tool_call(call_id: str, tool_name: str, arguments: dict[str, Any]) -> bytes:
    arg_str = json.dumps(arguments, ensure_ascii=False)
    chunks = [
        {
            "id": f"cmpl_{call_id}",
            "object": "chat.completion.chunk",
            "choices": [
                {
                    "index": 0,
                    "delta": {
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "index": 0,
                                "id": call_id,
                                "type": "function",
                                "function": {"name": tool_name, "arguments": arg_str},
                            }
                        ],
                    },
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": f"cmpl_{call_id}",
            "object": "chat.completion.chunk",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "tool_calls"}],
            "usage": {"prompt_tokens": 32, "completion_tokens": 24},
        },
    ]
    body = "".join(f"data: {json.dumps(c, ensure_ascii=False)}\n\n" for c in chunks)
    return (body + "data: [DONE]\n\n").encode("utf-8")


def _sse_stop(text: str = "done") -> bytes:
    chunks = [
        {
            "id": "cmpl_stop",
            "object": "chat.completion.chunk",
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": text},
                    "finish_reason": None,
                }
            ],
        },
        {
            "id": "cmpl_stop",
            "object": "chat.completion.chunk",
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 16, "completion_tokens": 8},
        },
    ]
    body = "".join(f"data: {json.dumps(c, ensure_ascii=False)}\n\n" for c in chunks)
    return (body + "data: [DONE]\n\n").encode("utf-8")


class _MockOpenAIServer:
    """Deterministic keyless OpenAI-compatible SSE mock for LearnHarness extractor/auditor."""

    def __init__(self) -> None:
        self.call_count = 0
        self._lock = threading.Lock()
        parent = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002, ARG002
                return

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", "0"))
                raw = self.rfile.read(length)
                req_json = json.loads(raw.decode("utf-8"))
                messages = req_json.get("messages", [])
                tools = req_json.get("tools", [])
                tool_names = [
                    t.get("function", {}).get("name")
                    for t in tools
                    if isinstance(t, dict)
                ]

                with parent._lock:
                    parent.call_count += 1
                    seq = parent.call_count

                last_role = messages[-1].get("role") if messages else ""
                if last_role == "tool":
                    payload = _sse_stop("submitted")
                elif "submit_findings" in tool_names:
                    payload = _sse_tool_call(
                        f"call_ext_{seq}",
                        "submit_findings",
                        {
                            "propositions": [
                                {
                                    "id": "p1",
                                    "name": f"Linear dynamics split #{seq}",
                                    "statement": (
                                        f"In discrete linear OGU (batch {seq}), "
                                        "x_r(a, w^-) = s_0(a) + xi(w^-)."
                                    ),
                                    "aliases": [],
                                },
                                {
                                    "id": "p2",
                                    "name": f"Exogenous image #{seq}",
                                    "statement": (
                                        f"Deviation set Xi = L(W^r) (batch {seq}) "
                                        "is independent of first-stage control a."
                                    ),
                                    "aliases": [],
                                },
                                {
                                    "id": "p3",
                                    "name": f"Borel policy bijection #{seq}",
                                    "statement": (
                                        f"Translation tau_a (batch {seq}) yields "
                                        "sourceLevels(D) = aroLevels(D)."
                                    ),
                                    "aliases": [],
                                },
                            ],
                            "chains": [
                                {"premises": ["p1", "p2"], "conclusion": "p3"},
                            ],
                        },
                    )
                elif "submit_review" in tool_names:
                    payload = _sse_tool_call(
                        f"call_aud_{seq}",
                        "submit_review",
                        {"links": []},
                    )
                else:
                    payload = _sse_stop("ok")

                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            daemon_threads = True
            allow_reuse_address = True

        self._httpd = ThreadedTCPServer(("127.0.0.1", 0), Handler)
        self.port = self._httpd.server_address[1]
        self.base_url = f"http://127.0.0.1:{self.port}/v1"
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)

    def __enter__(self) -> _MockOpenAIServer:
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)


def _wait_for_server(base_url: str, proc: subprocess.Popen[str], timeout_s: float = 30.0) -> None:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if proc.poll() is not None:
            out = proc.stdout.read() if proc.stdout else ""
            raise RuntimeError(f"LearnHarness standalone exited early ({proc.returncode}): {out}")
        try:
            with opener.open(f"{base_url}/api/graph", timeout=2.0) as resp:
                if resp.status == 200:
                    return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError(f"Timed out waiting for LearnHarness server at {base_url}")


def _get_json_loopback(url: str) -> dict[str, Any]:
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url, timeout=10.0) as resp:
        return json.loads(resp.read().decode("utf-8"))


class TestLearnHarnessV070Integration(unittest.TestCase):
    @unittest.skipUnless(
        STANDALONE_SERVER.is_file() and shutil.which("node"),
        "LearnHarness v0.7.0 standalone build or node binary not available",
    )
    def test_real_lh_v070_import_idempotent_practice_and_pull_isolated(self) -> None:
        live_before = _snapshot_dir(LIVE_LH_DATA)
        clean_env = {
            k: v
            for k, v in os.environ.items()
            if not k.startswith("ARO_LH_") and k != "LH_DATA_DIR"
        }

        with (
            mock.patch.dict(os.environ, clean_env, clear=True),
            tempfile.TemporaryDirectory(prefix="aro-r5-lh-e2e-") as tmp,
            _MockOpenAIServer() as mock_llm,
        ):
            checkout_graph = STANDALONE_SERVER.parents[2] / "skills/learnharness/scripts/graph.py"
            graph_script = (
                checkout_graph if checkout_graph.is_file() else resolve_graph_script()
            )
            tmp_path = pathlib.Path(tmp)
            data_dir = tmp_path / "data"
            data_dir.mkdir()
            auth_file = tmp_path / "auth.json"
            state_file = tmp_path / "push-state.json"
            binding_id = secrets.token_hex(16)

            binding = {
                "version": 1,
                "id": binding_id,
                "baseUrl": mock_llm.base_url,
                "authMode": "keyless",
            }
            auth_file.write_text(
                json.dumps({"__learnharness_custom_provider_binding": json.dumps(binding)}) + "\n",
                encoding="utf-8",
            )
            settings = {
                "version": 1,
                "customProvider": {
                    "baseUrl": mock_llm.base_url,
                    "authMode": "keyless",
                    "credentialBindingId": binding_id,
                    "models": [
                        {
                            "id": "mock-extractor",
                            "context": 32768,
                            "maxTokens": 4096,
                            "reasoning": False,
                        }
                    ],
                },
                "models": {
                    "strong": {"model": {"provider": "custom", "id": "mock-extractor"}},
                    "cheap": {"model": {"provider": "custom", "id": "mock-extractor"}},
                },
            }
            (data_dir / "settings.json").write_text(
                json.dumps(settings, indent=2) + "\n", encoding="utf-8"
            )

            lh_port = _free_port()
            lh_url = f"http://127.0.0.1:{lh_port}"
            env = {
                "PATH": os.environ.get("PATH", ""),
                "HOME": str(tmp_path),
                "NODE_ENV": "production",
                "HOSTNAME": "127.0.0.1",
                "PORT": str(lh_port),
                "LH_DATA_DIR": str(data_dir),
                "LH_AUTH_FILE": str(auth_file),
                "LH_IGNORE_ENV_KEYS": "1",
                "NO_PROXY": "127.0.0.1,localhost,::1",
                "no_proxy": "127.0.0.1,localhost,::1",
            }
            proc = subprocess.Popen(
                ["node", str(STANDALONE_SERVER)],
                cwd=str(STANDALONE_SERVER.parent),
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            try:
                _wait_for_server(lh_url, proc)

                # 1. Build real Packet-01 pack
                pack = build_study_pack(
                    "01-bridge-packet-01",
                    repo_root=REPO_ROOT,
                    validate_gate=True,
                    require_style=False,
                )

                # 2. First push via POST /api/graph/import (multipart files + paths)
                push_res = push_pack(pack, lh_url, state_file=state_file, timeout=120.0)
                self.assertEqual(len(push_res.results), 4)
                for item in push_res.results:
                    self.assertTrue(item.ok, f"Import failed: {item}")
                    self.assertEqual(item.outcome, "completed")
                    self.assertGreaterEqual(item.nodes, 3)
                    self.assertGreaterEqual(item.chains, 1)

                llm_calls_after_first = mock_llm.call_count
                self.assertGreater(llm_calls_after_first, 0)

                pulled_1 = pull_aro_context(
                    data_dir,
                    graph_script=graph_script,
                    prefix="ARO/",
                    topic="01-bridge-packet-01",
                )
                props_after_first = pulled_1["summary"]["proposition_count"]
                chains_after_first = pulled_1["summary"]["chain_count"]
                self.assertEqual(pulled_1["summary"]["session_count"], 4)
                self.assertGreaterEqual(props_after_first, 12)
                self.assertGreaterEqual(chains_after_first, 4)

                # 2b. Repeat push of unchanged pack MUST be strictly idempotent:
                #     0 new LLM calls, 0 duplicate propositions/chains, outcome=skipped_unchanged
                push_res_2 = push_pack(pack, lh_url, state_file=state_file, timeout=120.0)
                self.assertEqual(len(push_res_2.results), 4)
                for item in push_res_2.results:
                    self.assertTrue(item.ok)
                    self.assertEqual(item.outcome, "skipped_unchanged")
                self.assertEqual(
                    mock_llm.call_count,
                    llm_calls_after_first,
                    "Idempotent repeat push must trigger 0 new LLM calls",
                )
                pulled_2 = pull_aro_context(
                    data_dir,
                    graph_script=graph_script,
                    prefix="ARO/",
                    topic="01-bridge-packet-01",
                )
                self.assertEqual(pulled_2["summary"]["proposition_count"], props_after_first)
                self.assertEqual(pulled_2["summary"]["chain_count"], chains_after_first)

                # 3. Verify exact 3-level ARO/... folder hierarchy in LearnHarness
                sources_dir = _get_json_loopback(f"{lh_url}/api/graph/sources")
                raw_folders = sources_dir.get("organization", {}).get("folders", [])
                folders = (
                    list(raw_folders.values())
                    if isinstance(raw_folders, dict)
                    else list(raw_folders)
                )
                by_name = {f.get("name"): f for f in folders if isinstance(f, dict)}
                self.assertIn("ARO", by_name)
                self.assertIn("01-Bridge-OGU-ARO", by_name)
                self.assertIn("01-bridge-packet-01", by_name)
                self.assertIsNone(by_name["ARO"].get("parentId"))
                self.assertEqual(
                    by_name["01-Bridge-OGU-ARO"].get("parentId"),
                    by_name["ARO"].get("id"),
                )
                self.assertEqual(
                    by_name["01-bridge-packet-01"].get("parentId"),
                    by_name["01-Bridge-OGU-ARO"].get("id"),
                )

                # 4. Verify ledgers written by LearnHarness itself (never by our code)
                self.assertTrue((data_dir / "graph/nodes.jsonl").is_file())
                self.assertTrue((data_dir / "graph/chains.jsonl").is_file())

                # 5. Create Practice session with non-empty graphContext via POST /api/chats
                practice = create_study_session(pack, lh_url, mode="practice")
                self.assertEqual(practice.mode, "practice")
                self.assertGreaterEqual(len(practice.propositions), 3)
                self.assertTrue(practice.url.startswith(f"{lh_url}/chat/"))

                chat_record = _get_json_loopback(f"{lh_url}/api/chats/{practice.chat_id}")
                self.assertEqual(chat_record.get("kind"), "practice")
                msgs = chat_record.get("messages", [])
                self.assertGreaterEqual(len(msgs), 1)
                ctx_msg = msgs[0]
                self.assertEqual(ctx_msg.get("customType"), "graph-context")
                ctx_content = str(ctx_msg.get("content", ""))
                self.assertIn("[Session context]", ctx_content)
                self.assertIn("Reasoning chains among them", ctx_content)
                for pick in practice.propositions:
                    self.assertIn(f"[{pick['id']}]", ctx_content)

                # 6. Create Teach session via POST /api/chats
                teach = create_study_session(pack, lh_url, mode="teach")
                teach_record = _get_json_loopback(f"{lh_url}/api/chats/{teach.chat_id}")
                self.assertNotIn("kind", teach_record)
            finally:
                proc.terminate()
                try:
                    proc.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
                if proc.stdout is not None:
                    proc.stdout.close()

        live_after = _snapshot_dir(LIVE_LH_DATA)
        self.assertEqual(
            live_before,
            live_after,
            "Live ~/.config/LearnHarness/data MUST NOT be touched by tests!",
        )


if __name__ == "__main__":
    unittest.main()
