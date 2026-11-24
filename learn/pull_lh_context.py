#!/usr/bin/env python3
"""Read-only context reader over LearnHarness v0.7.0 `skills/learnharness/scripts/graph.py`.

Never opens or writes LearnHarness data files directly — delegates strictly to the
official read-only `graph.py` script (`--data-dir`, `--format json`).
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from typing import Any

from learn import DEFAULT_ROOT_PREFIX, default_lh_repo, fallback_lh_repo


class ContextPullError(RuntimeError):
    """Raised when the read-only LearnHarness graph reader cannot run or returns bad data."""


def resolve_graph_script(explicit: pathlib.Path | None = None) -> pathlib.Path:
    candidates: list[pathlib.Path] = []
    if explicit is not None:
        candidates.append(explicit.expanduser())
    env_script = os.environ.get("ARO_LH_GRAPH_SCRIPT")
    if env_script:
        candidates.append(pathlib.Path(env_script).expanduser())
    candidates.extend(
        [
            default_lh_repo() / "skills/learnharness/scripts/graph.py",
            fallback_lh_repo() / "skills/learnharness/scripts/graph.py",
        ]
    )
    for path in candidates:
        if path.is_file():
            return path.resolve()
    searched = ", ".join(str(p) for p in candidates)
    raise ContextPullError(f"LearnHarness graph.py not found (searched: {searched})")


def _run_graph_py(
    graph_script: pathlib.Path,
    data_dir: pathlib.Path | None,
    sub_args: list[str],
    *,
    timeout: float = 30.0,
) -> dict[str, Any]:
    cmd = [sys.executable, "-B", str(graph_script)]
    if data_dir is not None:
        cmd.extend(["--data-dir", str(data_dir)])
    cmd.extend(["--format", "json", *sub_args])

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise ContextPullError(
            f"graph.py {' '.join(sub_args)} timed out after {timeout}s"
        ) from exc
    except OSError as exc:
        raise ContextPullError(f"Failed to execute graph.py: {exc}") from exc

    if proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip() or f"exit {proc.returncode}"
        raise ContextPullError(f"graph.py {' '.join(sub_args)} failed: {detail}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise ContextPullError(f"Invalid JSON from graph.py: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("records"), list):
        raise ContextPullError(f"Unexpected graph.py payload shape: {payload!r}")
    return payload


def pull_aro_context(
    data_dir: pathlib.Path | None = None,
    *,
    graph_script: pathlib.Path | None = None,
    prefix: str = f"{DEFAULT_ROOT_PREFIX}/",
    topic: str | None = None,
    query: str | None = None,
    timeout: float = 30.0,
) -> dict[str, Any]:
    """Pull ARO/OGU sessions, propositions, and reasoning chains via read-only graph.py."""
    script = resolve_graph_script(graph_script)
    effective_data_dir = data_dir
    if effective_data_dir is None:
        env_dir = os.environ.get("LH_DATA_DIR")
        if env_dir:
            effective_data_dir = pathlib.Path(env_dir).expanduser()

    sessions_resp = _run_graph_py(script, effective_data_dir, ["sessions"], timeout=timeout)
    resolved_data_dir = str(sessions_resp.get("data_dir", effective_data_dir or ""))
    all_sessions = sessions_resp["records"]

    clean_topic = topic.strip("/") if topic else None

    def _session_matches(sess: dict[str, Any]) -> bool:
        name = str(sess.get("name", ""))
        if prefix and not name.startswith(prefix):
            return False
        if clean_topic:
            return f"/{clean_topic}/" in name or name.endswith(f"/{clean_topic}")
        return True

    matched_sessions = [
        s for s in all_sessions if isinstance(s, dict) and _session_matches(s)
    ]
    matched_session_ids = {str(s["id"]) for s in matched_sessions if isinstance(s.get("id"), str)}

    propositions_by_id: dict[str, dict[str, Any]] = {}
    has_scope_filter = bool(prefix or clean_topic)
    if query:
        if has_scope_filter and not matched_session_ids:
            found: list[Any] = []
        else:
            found = _run_graph_py(
                script, effective_data_dir, ["find", query], timeout=timeout
            )["records"]
        for node in found:
            if not isinstance(node, dict) or not isinstance(node.get("id"), str):
                continue
            if has_scope_filter:
                prov = node.get("provenance", [])
                in_scope = any(
                    isinstance(pt, dict) and pt.get("chatId") in matched_session_ids
                    for pt in prov
                )
                if not in_scope:
                    continue
            propositions_by_id[node["id"]] = node
    else:
        for sid in sorted(matched_session_ids):
            recs = _run_graph_py(
                script,
                effective_data_dir,
                ["propositions", "--session", sid],
                timeout=timeout,
            )["records"]
            for node in recs:
                if isinstance(node, dict) and isinstance(node.get("id"), str):
                    propositions_by_id[node["id"]] = node

    propositions = sorted(propositions_by_id.values(), key=lambda n: str(n.get("id", "")))
    prop_ids = set(propositions_by_id)

    all_chains = _run_graph_py(script, effective_data_dir, ["chains"], timeout=timeout)["records"]
    matched_chains: list[dict[str, Any]] = []
    for chain in all_chains:
        if not isinstance(chain, dict):
            continue
        premises = chain.get("premises", [])
        conclusion = chain.get("conclusion")
        prov = chain.get("provenance", [])
        touches_prop = conclusion in prop_ids or any(p in prop_ids for p in premises)
        touches_session = any(
            isinstance(pt, dict) and pt.get("chatId") in matched_session_ids for pt in prov
        )
        if touches_prop or (not query and touches_session):
            matched_chains.append(chain)

    matched_chains.sort(key=lambda c: str(c.get("id", "")))

    return {
        "data_dir": resolved_data_dir,
        "graph_script": str(script),
        "filter": {"prefix": prefix, "topic": clean_topic, "query": query},
        "sessions": matched_sessions,
        "propositions": propositions,
        "chains": matched_chains,
        "summary": {
            "session_count": len(matched_sessions),
            "proposition_count": len(propositions),
            "chain_count": len(matched_chains),
        },
    }


def format_markdown(context: dict[str, Any]) -> str:
    s = context["summary"]
    lines = [
        "# LearnHarness ARO Context (Read-Only)",
        "",
        f"- Data dir: `{context['data_dir']}`",
        f"- Filter: prefix=`{context['filter']['prefix']}`, "
        f"topic=`{context['filter']['topic']}`, query=`{context['filter']['query']}`",
        f"- Summary: {s['session_count']} source(s), "
        f"{s['proposition_count']} proposition(s), {s['chain_count']} chain(s)",
        "",
        "## Propositions",
    ]
    if not context["propositions"]:
        lines.append("- None found.")
    else:
        for node in context["propositions"]:
            lines.append(f"- **{node['name']}** (`{node['id']}`): {node['statement']}")
    lines.append("")
    lines.append("## Chains")
    if not context["chains"]:
        lines.append("- None found.")
    else:
        for ch in context["chains"]:
            prems = " + ".join(ch["premises"])
            lines.append(f"- `{ch['id']}`: `{prems}` => `{ch['conclusion']}`")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Read-only ARO/OGU context adapter over LearnHarness graph.py."
    )
    parser.add_argument("--data-dir", type=pathlib.Path, default=None, help="LearnHarness data dir")
    parser.add_argument("--graph-script", type=pathlib.Path, default=None, help="Path to graph.py")
    parser.add_argument(
        "--prefix",
        default=f"{DEFAULT_ROOT_PREFIX}/",
        help="Source path prefix filter",
    )
    parser.add_argument(
        "--topic",
        default=None,
        help="Filter by topic folder (e.g. 01-bridge-packet-01)",
    )
    parser.add_argument("--query", default=None, help="Optional wildcard query via graph.py find")
    parser.add_argument("--timeout", type=float, default=30.0, help="Subprocess timeout in seconds")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    try:
        ctx = pull_aro_context(
            args.data_dir,
            graph_script=args.graph_script,
            prefix=args.prefix,
            topic=args.topic,
            query=args.query,
            timeout=args.timeout,
        )
    except ContextPullError as exc:
        print(f"pull_lh_context error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(ctx))
    return 0


if __name__ == "__main__":
    sys.exit(main())
