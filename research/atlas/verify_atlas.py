#!/usr/bin/env python3
"""Deterministic verifier for the Fundamental Mathematical Atlas & Lean 4 Blueprint (R10 #1271).

Enforces (zero `assert` — works identically under `-B` and `-B -O`):
  1. Strict schema validation of `research/atlas/atlas.json` (kinds, statuses, domains, edges);
  2. Strict DAG acyclicity (Kahn's algorithm), zero self-loops, zero duplicate edges, zero
     isolated/dangling nodes;
  3. 100% file & corpus reference integrity (no path traversal; every referenced corpus file
     must exist and be registered in `corpus/MANIFEST.md` or `corpus/extra/`);
  4. Strict `lean_proved` binding to R2 live Lean 4 kernel `#print axioms` audit:
       - Every `lean_proved` node must declare non-empty `lean_decls`;
       - Static check (comments/strings stripped) confirms zero `sorry`/`admit`/`axiom` and
         declaration presence in the referenced `.lean` file;
       - Live Lean 4 kernel execution of `AroProofs/Inventory.lean` confirms every `lean_proved`
         declaration is kernel-compiled with axioms strictly subset of
         `{propext, Classical.choice, Quot.sound}`;
       - Complete 19/19 coverage of `verify_claim.EXPECTED_UNIFIED_DECLS`;
  5. Operational `falsification_criteria` required on every open conjecture / generalization;
  6. Byte-for-byte freshness of generated `ATLAS.md`, `blueprint.json`, and `BLUEPRINT.md`;
  7. Negative `--self-test` proving guaranteed rejection of fake `lean_proved` nodes, cycles,
     dangling nodes, broken links, missing falsification criteria, and stale artifacts.
"""

from __future__ import annotations

import argparse
import collections
import copy
import json
import pathlib
import re
import sys
import tempfile
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.atlas import (  # noqa: E402
    ALLOWED_DOMAINS,
    ALLOWED_EDGE_RELATIONS,
    ALLOWED_NODE_KINDS,
    ALLOWED_NODE_STATUSES,
)
from research.atlas.build_atlas import (  # noqa: E402
    ATLAS_JSON_REL,
    ATLAS_MD_REL,
    BLUEPRINT_JSON_REL,
    BLUEPRINT_MD_REL,
    build_blueprint_dict,
    render_atlas_md,
    render_blueprint_md,
)

ALLOWED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
_MANIFEST_ENTRY_RE = re.compile(r"^[0-9a-f]{64}\s+(corpus/.+)$")


class AtlasVerificationError(RuntimeError):
    """Raised when an Atlas or Lean 4 Blueprint invariant fails."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise AtlasVerificationError(msg)


def _load_manifest_corpus_paths(repo_root: pathlib.Path) -> set[str]:
    manifest = repo_root / "corpus/MANIFEST.md"
    if not manifest.is_file():
        return set()
    known: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        m = _MANIFEST_ENTRY_RE.match(line.strip())
        if m:
            known.add(m.group(1).strip())
    return known


def _resolve_repo_path(repo_root: pathlib.Path, rel: str, label: str) -> pathlib.Path:
    if not isinstance(rel, str) or not rel.strip():
        raise AtlasVerificationError(f"{label}: empty or non-string path")
    raw = pathlib.Path(rel)
    if raw.is_absolute():
        raise AtlasVerificationError(f"{label}: absolute path forbidden: {rel!r}")
    root_res = repo_root.resolve()
    target = (root_res / raw).resolve()
    if not target.is_relative_to(root_res):
        raise AtlasVerificationError(f"{label}: path escapes repository root: {rel!r}")
    if not target.is_file():
        raise AtlasVerificationError(f"{label}: referenced file does not exist: {rel!r}")
    return target


def _extract_lean_signature(cleaned_source: str, short_name: str) -> str | None:
    """Extract normalized `theorem|lemma|def <short_name> ... :=` header from cleaned Lean code."""
    pat = (
        rf"\b(?:private\s+)?(?:theorem|lemma|def|abbrev)\s+{re.escape(short_name)}\b"
        r".*?(?::=|\bwhere\b)"
    )
    m = re.search(pat, cleaned_source, flags=re.S)
    if not m:
        return None
    return " ".join(m.group(0).split())


def _check_lean_decl_in_source(
    lean_file: pathlib.Path,
    decl_full: str,
    expected_signature: str | None = None,
) -> list[str]:
    """Static check: zero sorry/admit/axiom, declaration presence, and exact signature match."""
    gates_dir = REPO_ROOT / "verification/gates"
    if str(gates_dir) not in sys.path:
        sys.path.insert(0, str(gates_dir))
    import verify_lean as vl  # type: ignore[import-not-found]

    errors: list[str] = []
    cleaned = vl.strip_lean_comments_and_strings(lean_file.read_text(encoding="utf-8"))
    for bad in ("sorry", "admit", "axiom"):
        if re.search(rf"\b{bad}\b", cleaned):
            errors.append(f"Forbidden token '{bad}' in Lean source {lean_file.name}")
    short_name = decl_full.rsplit(".", 1)[-1]
    actual_sig = _extract_lean_signature(cleaned, short_name)
    if actual_sig is None:
        errors.append(f"Declaration '{decl_full}' not found in {lean_file.name}")
    elif expected_signature is not None:
        norm_expected = " ".join(expected_signature.split())
        if actual_sig != norm_expected:
            errors.append(
                f"lean_signature mismatch for '{decl_full}' in {lean_file.name}: "
                f"atlas has {norm_expected!r}, Lean file has {actual_sig!r}"
            )
    return errors


def _audit_live_lean_axioms(repo_root: pathlib.Path) -> dict[str, set[str]]:
    """Verify `.olean` freshness via native `lake --offline build` + live `Inventory.lean` audit."""
    import concurrent.futures

    gates_dir = repo_root / "verification/gates"
    if str(gates_dir) not in sys.path:
        sys.path.insert(0, str(gates_dir))
    import verify_claim as vc  # type: ignore[import-not-found]

    lean_root = repo_root / "verification/lean"
    lake_lib = (lean_root / ".lake").resolve() / "build/lib/lean"
    pre_snap = vc._snapshot_project_oleans(lake_lib) if lake_lib.is_dir() else {}
    targets = ("BridgeFormalV2.Proofs.Inventory", "AroProofs.Inventory")
    can_overlap = all(
        k in pre_snap
        for k in (
            "AroProofs/BridgeF1F2.olean",
            "AroProofs/Aroform.olean",
            "AroProofs/BridgeF3Draft.olean",
        )
    )
    try:
        if can_overlap:
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
                f_lake = pool.submit(vc._run_lake_build, lean_root, targets)
                f_inv = pool.submit(
                    vc._run_live_lean_file, lean_root, "AroProofs/Inventory.lean"
                )
                f_lake.result()
                proc = f_inv.result()
        else:
            vc._run_lake_build(lean_root, targets)
            proc = vc._run_live_lean_file(lean_root, "AroProofs/Inventory.lean")
        post_snap = vc._snapshot_project_oleans(lake_lib) if lake_lib.is_dir() else {}
        if can_overlap and post_snap != pre_snap:
            proc = vc._run_live_lean_file(lean_root, "AroProofs/Inventory.lean")
        vc._audit_live_inventory(lean_root, "AroProofs/Inventory.lean", proc=proc)
    except vc.GateError as exc:
        raise AtlasVerificationError(f"Live Lean 4 verification failed: {exc}") from exc
    return vc.parse_print_axioms(proc.stdout)


def validate_atlas_data(
    atlas: dict[str, Any],
    repo_root: pathlib.Path = REPO_ROOT,
    *,
    audited_axioms: dict[str, set[str]] | None = None,
    expected_unified_decls: tuple[str, ...] | None = None,
    check_generated_sync: bool = True,
) -> dict[str, Any]:
    """Validate Atlas JSON, DAG invariants, file/corpus refs, Lean proof bindings, & artifacts."""
    errors: list[str] = []

    if not isinstance(atlas, dict):
        raise AtlasVerificationError("Atlas root must be a JSON object")
    if atlas.get("schema_version") != 1:
        errors.append(f"Unsupported schema_version: {atlas.get('schema_version')!r}")

    nodes = atlas.get("nodes")
    edges = atlas.get("edges")
    if not isinstance(nodes, list) or not nodes:
        raise AtlasVerificationError("Atlas 'nodes' must be a non-empty list")
    if not isinstance(edges, list) or not edges:
        raise AtlasVerificationError("Atlas 'edges' must be a non-empty list")

    known_corpus = _load_manifest_corpus_paths(repo_root)
    node_by_id: dict[str, dict[str, Any]] = {}
    covered_lean_decls: set[str] = set()

    for idx, node in enumerate(nodes):
        if not isinstance(node, dict):
            errors.append(f"Node #{idx} is not an object")
            continue
        nid = node.get("id")
        if not isinstance(nid, str) or not re.match(r"^[a-z0-9][a-z0-9-]*$", nid):
            errors.append(f"Node #{idx} has invalid id: {nid!r}")
            continue
        if nid in node_by_id:
            errors.append(f"Duplicate node id: {nid!r}")
            continue
        node_by_id[nid] = node

        kind = node.get("kind")
        status = node.get("status")
        domain = node.get("domain")
        if kind not in ALLOWED_NODE_KINDS:
            errors.append(f"Node '{nid}': invalid kind {kind!r}")
        if status not in ALLOWED_NODE_STATUSES:
            errors.append(f"Node '{nid}': invalid status {status!r}")
        if domain not in ALLOWED_DOMAINS:
            errors.append(f"Node '{nid}': invalid domain {domain!r}")

        for req_txt in ("title_en", "title_ru", "statement_en", "statement_ru"):
            val = node.get(req_txt)
            if not isinstance(val, str) or not val.strip():
                errors.append(f"Node '{nid}': missing non-empty '{req_txt}'")

        lean_decls = node.get("lean_decls", [])
        oracles = node.get("oracles", [])
        guides = node.get("guides", [])
        sources = node.get("sources", [])
        for field_name, seq in (
            ("lean_decls", lean_decls),
            ("oracles", oracles),
            ("guides", guides),
            ("sources", sources),
        ):
            if not isinstance(seq, list):
                errors.append(f"Node '{nid}': '{field_name}' must be a list")

        # Validate file & corpus references
        for rel in oracles if isinstance(oracles, list) else []:
            try:
                _resolve_repo_path(repo_root, rel, f"Node '{nid}' oracle")
            except AtlasVerificationError as exc:
                errors.append(str(exc))

        for rel in guides if isinstance(guides, list) else []:
            try:
                _resolve_repo_path(repo_root, rel, f"Node '{nid}' guide")
            except AtlasVerificationError as exc:
                errors.append(str(exc))

        for rel in sources if isinstance(sources, list) else []:
            try:
                _resolve_repo_path(repo_root, rel, f"Node '{nid}' source")
            except AtlasVerificationError as exc:
                errors.append(str(exc))
                continue
            if (
                rel.startswith("corpus/")
                and not rel.startswith("corpus/extra/")
                and known_corpus
                and rel not in known_corpus
            ):
                errors.append(
                    f"Node '{nid}': corpus source not in corpus/MANIFEST.md: {rel!r}"
                )

        # Validate lean_decls file paths on ALL nodes (preventing broken refs in any status)
        for item in lean_decls if isinstance(lean_decls, list) else []:
            if not isinstance(item, dict):
                errors.append(f"Node '{nid}': lean_decls entry must be an object")
                continue
            lean_rel = item.get("file")
            try:
                _resolve_repo_path(repo_root, str(lean_rel or ""), f"Node '{nid}' lean_decl")
            except AtlasVerificationError as exc:
                errors.append(str(exc))

        # Status-specific invariants
        if status == "lean_proved":
            fscope = node.get("formalized_scope")
            if not isinstance(fscope, dict):
                errors.append(
                    f"Node '{nid}' with status 'lean_proved' must declare 'formalized_scope'"
                )
            else:
                for skey in ("proved_in_lean", "not_proved_in_lean"):
                    sv = fscope.get(skey)
                    if not isinstance(sv, str) or not sv.strip():
                        errors.append(
                            f"Node '{nid}': formalized_scope missing non-empty '{skey}'"
                        )
            if not isinstance(lean_decls, list) or not lean_decls:
                errors.append(
                    f"Node '{nid}' has status 'lean_proved' but declares no 'lean_decls'"
                )
            else:
                for item in lean_decls:
                    if not isinstance(item, dict):
                        errors.append(f"Node '{nid}': lean_decls entry must be an object")
                        continue
                    decl_name = item.get("decl")
                    lean_rel = item.get("file")
                    lean_sig = item.get("lean_signature")
                    if not isinstance(decl_name, str) or not decl_name.strip():
                        errors.append(f"Node '{nid}': lean_decls entry missing 'decl'")
                        continue
                    if not isinstance(lean_sig, str) or not lean_sig.strip():
                        errors.append(
                            f"Node '{nid}': lean_decls entry '{decl_name}' "
                            "missing required 'lean_signature'"
                        )
                        continue
                    try:
                        lean_path = _resolve_repo_path(
                            repo_root, str(lean_rel or ""), f"Node '{nid}' lean_decl"
                        )
                    except AtlasVerificationError as exc:
                        errors.append(str(exc))
                        continue
                    if not str(lean_rel).startswith("verification/lean/"):
                        errors.append(
                            f"Node '{nid}': lean_decl file must live under verification/lean/: "
                            f"{lean_rel!r}"
                        )
                    errors.extend(_check_lean_decl_in_source(lean_path, decl_name, lean_sig))
                    covered_lean_decls.add(decl_name)

                    if audited_axioms is not None:
                        if decl_name not in audited_axioms:
                            errors.append(
                                f"Node '{nid}': lean_proved declaration '{decl_name}' "
                                "is missing from live Lean 4 `#print axioms` audit"
                            )
                        else:
                            disallowed = audited_axioms[decl_name] - ALLOWED_AXIOMS
                            if disallowed:
                                errors.append(
                                    f"Node '{nid}': declaration '{decl_name}' depends on "
                                    f"disallowed axioms {sorted(disallowed)}"
                                )
        elif status in ("oracle_verified", "falsified") and (
            not isinstance(oracles, list) or not oracles
        ):
            errors.append(
                f"Node '{nid}' has status '{status}' but declares no executable 'oracles'"
            )

        if kind in ("open_conjecture", "generalization_target") or status == "open":
            fc = node.get("falsification_criteria")
            if not isinstance(fc, dict):
                errors.append(
                    f"Open node '{nid}' must declare operational 'falsification_criteria'"
                )
            else:
                for fc_key in ("method", "oracle_or_battery", "refutation_condition"):
                    v = fc.get(fc_key)
                    if not isinstance(v, str) or not v.strip():
                        errors.append(
                            f"Open node '{nid}': falsification_criteria missing '{fc_key}'"
                        )

    # Check full coverage of expected unified Lean 4 declarations when supplied
    if expected_unified_decls is not None:
        missing_decls = sorted(set(expected_unified_decls) - covered_lean_decls)
        if missing_decls:
            errors.append(
                f"Atlas omits audited Lean 4 declarations: {missing_decls}"
            )

    # Validate edges, degree (no dangling/isolated nodes), and strict DAG acyclicity
    in_deg: dict[str, int] = dict.fromkeys(node_by_id, 0)
    total_deg: dict[str, int] = dict.fromkeys(node_by_id, 0)
    adj: dict[str, list[str]] = collections.defaultdict(list)
    seen_edges: set[tuple[str, str, str]] = set()

    for idx, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"Edge #{idx} is not an object")
            continue
        src = edge.get("source")
        dst = edge.get("target")
        rel = edge.get("relation")
        if rel not in ALLOWED_EDGE_RELATIONS:
            errors.append(f"Edge #{idx}: invalid relation {rel!r}")
        if src not in node_by_id:
            errors.append(f"Edge #{idx}: unknown source node {src!r}")
            continue
        if dst not in node_by_id:
            errors.append(f"Edge #{idx}: unknown target node {dst!r}")
            continue
        if src == dst:
            errors.append(f"Edge #{idx}: self-loop forbidden on {src!r}")
            continue
        key = (src, dst, str(rel))
        if key in seen_edges:
            errors.append(f"Edge #{idx}: duplicate edge {key}")
            continue
        seen_edges.add(key)
        adj[src].append(dst)
        in_deg[dst] += 1
        total_deg[src] += 1
        total_deg[dst] += 1

    isolated = sorted(nid for nid, deg in total_deg.items() if deg == 0)
    if isolated:
        errors.append(f"Dangling/isolated nodes with zero edges: {isolated}")

    # Kahn's topological sort over ALL directed edges to guarantee strict DAG acyclicity
    queue = collections.deque(nid for nid, deg in in_deg.items() if deg == 0)
    visited = 0
    while queue:
        cur = queue.popleft()
        visited += 1
        for nxt in adj.get(cur, ()):
            in_deg[nxt] -= 1
            if in_deg[nxt] == 0:
                queue.append(nxt)
    if visited != len(node_by_id):
        cycle_nodes = sorted(nid for nid, deg in in_deg.items() if deg > 0)
        errors.append(f"Atlas graph is NOT a DAG (cycle involving nodes: {cycle_nodes})")

    # Verify generated ATLAS.md & Lean 4 Blueprint artifacts match atlas.json byte-for-byte
    if check_generated_sync and not errors:
        expected_atlas_md = render_atlas_md(atlas)
        expected_bp = build_blueprint_dict(atlas)
        expected_bp_json = json.dumps(expected_bp, ensure_ascii=False, indent=2) + "\n"
        expected_bp_md = render_blueprint_md(expected_bp)
        for rel_path, expected_content in (
            (ATLAS_MD_REL, expected_atlas_md),
            (BLUEPRINT_JSON_REL, expected_bp_json),
            (BLUEPRINT_MD_REL, expected_bp_md),
        ):
            fpath = repo_root / rel_path
            if not fpath.is_file():
                errors.append(f"Missing generated artifact: {rel_path}")
            elif fpath.read_text(encoding="utf-8") != expected_content:
                errors.append(
                    f"Generated artifact out of sync with atlas.json: {rel_path} "
                    "(run `python3 -B research/atlas/build_atlas.py`)"
                )

    if errors:
        raise AtlasVerificationError(
            "Atlas verification failed:\n  - " + "\n  - ".join(errors)
        )

    status_counts = dict(sorted(collections.Counter(n["status"] for n in nodes).items()))
    kind_counts = dict(sorted(collections.Counter(n["kind"] for n in nodes).items()))
    return {
        "nodes": len(nodes),
        "edges": len(edges),
        "lean_decls_audited": len(covered_lean_decls),
        "status_counts": status_counts,
        "kind_counts": kind_counts,
    }


def run_self_test() -> int:
    """Negative self-tests (zero `assert`, works identically under `-B` and `-B -O`)."""
    base_atlas = json.loads((REPO_ROOT / ATLAS_JSON_REL).read_text(encoding="utf-8"))
    gates_dir = REPO_ROOT / "verification/gates"
    if str(gates_dir) not in sys.path:
        sys.path.insert(0, str(gates_dir))
    import verify_claim as vc  # type: ignore[import-not-found]

    clean_axioms = {d: set(ALLOWED_AXIOMS) for d in vc.EXPECTED_UNIFIED_DECLS}

    def _expect_reject(mutated: dict[str, Any], expected_substr: str, label: str, *,
                       axioms: dict[str, set[str]] | None = None,
                       repo_override: pathlib.Path | None = None,
                       check_sync: bool = False) -> None:
        rejected = False
        err_msg = ""
        try:
            validate_atlas_data(
                mutated,
                repo_root=repo_override or REPO_ROOT,
                audited_axioms=clean_axioms if axioms is None else axioms,
                expected_unified_decls=None,
                check_generated_sync=check_sync,
            )
        except AtlasVerificationError as exc:
            err_msg = str(exc)
            rejected = expected_substr.lower() in err_msg.lower()
        _expect(rejected, f"Self-test '{label}' NOT rejected as expected ({expected_substr!r}): "
                          f"{err_msg}")

    # 1. Fake `lean_proved` node with nonexistent declaration MUST fail
    m1 = copy.deepcopy(base_atlas)
    m1["nodes"][0]["lean_decls"].append(
        {
            "decl": "BridgeFormalV2.Proofs.nonexistent_fake_thm",
            "file": "verification/lean/BridgeFormalV2/Proofs/Dynamics.lean",
            "lean_signature": "theorem nonexistent_fake_thm : True :=",
        }
    )
    _expect_reject(m1, "missing from live Lean 4", "fake-lean-nonexistent")

    # 1b. Mismatched `lean_signature` on a real `lean_proved` declaration MUST fail
    m1b = copy.deepcopy(base_atlas)
    for n in m1b["nodes"]:
        if n["id"] == "lem-p2-info-monotone":
            n["lean_decls"][0]["lean_signature"] = (
                "theorem info_value_monotone (R1 R2 : Nat) : R1 <= R2 :="
            )
    _expect_reject(m1b, "lean_signature mismatch", "lean-signature-mismatch")

    # 2. Fake `lean_proved` node whose declaration depends on `sorryAx` MUST fail
    bad_axioms = copy.deepcopy(clean_axioms)
    bad_axioms["BridgeFormalV2.Proofs.epigraph_equality"].add("sorryAx")
    _expect_reject(copy.deepcopy(base_atlas), "sorryAx", "fake-lean-sorryAx", axioms=bad_axioms)

    # 3. Fake `lean_proved` node with empty `lean_decls` MUST fail
    m3 = copy.deepcopy(base_atlas)
    for n in m3["nodes"]:
        if n["id"] == "thm-f2-epigraph-equality":
            n["lean_decls"] = []
    _expect_reject(m3, "declares no 'lean_decls'", "fake-lean-empty-decls")

    # 4. Cyclic dependency DAG MUST fail
    m4 = copy.deepcopy(base_atlas)
    m4["edges"].append(
        {"source": "def-ogu-system", "target": "thm-f2-epigraph-equality", "relation": "depends_on"}
    )
    _expect_reject(m4, "NOT a DAG", "cycle-detection")

    # 5. Dangling / isolated node MUST fail
    m5 = copy.deepcopy(base_atlas)
    m5["nodes"].append(
        {
            "id": "orphan-node",
            "kind": "lemma",
            "status": "sketch",
            "domain": "foundations",
            "title_en": "Orphan",
            "title_ru": "Сирота",
            "statement_en": "Isolated node.",
            "statement_ru": "Изолированный узел.",
            "lean_decls": [],
            "oracles": [],
            "guides": [],
            "sources": [],
        }
    )
    _expect_reject(m5, "Dangling/isolated", "dangling-node")

    # 6. Broken file reference MUST fail
    m6 = copy.deepcopy(base_atlas)
    m6["nodes"][1]["oracles"] = ["verification/does_not_exist.py"]
    _expect_reject(m6, "does not exist", "broken-file-ref")

    # 7. Open conjecture without `falsification_criteria` MUST fail
    m7 = copy.deepcopy(base_atlas)
    for n in m7["nodes"]:
        if n["id"] == "conj-f4-vertex-lp-selector":
            del n["falsification_criteria"]
    _expect_reject(m7, "falsification_criteria", "missing-falsification-criteria")

    # 8. Stale / drifted generated `ATLAS.md` MUST fail sync check
    with tempfile.TemporaryDirectory(prefix="aro-atlas-sync-") as tmp:
        fake_root = pathlib.Path(tmp)
        (fake_root / ATLAS_MD_REL).parent.mkdir(parents=True, exist_ok=True)
        (fake_root / ATLAS_MD_REL).write_text("# stale\n", encoding="utf-8")
        (fake_root / BLUEPRINT_JSON_REL).parent.mkdir(parents=True, exist_ok=True)
        (fake_root / BLUEPRINT_JSON_REL).write_text("{}\n", encoding="utf-8")
        (fake_root / BLUEPRINT_MD_REL).write_text("# stale\n", encoding="utf-8")
        # Minimal valid 2-node atlas without external file refs
        mini_atlas = {
            "schema_version": 1,
            "title_en": "Mini",
            "title_ru": "Мини",
            "nodes": [
                {
                    "id": "n-a",
                    "kind": "definition",
                    "status": "sketch",
                    "domain": "foundations",
                    "title_en": "A",
                    "title_ru": "А",
                    "statement_en": "A",
                    "statement_ru": "А",
                    "lean_decls": [],
                    "oracles": [],
                    "guides": [],
                    "sources": [],
                },
                {
                    "id": "n-b",
                    "kind": "lemma",
                    "status": "sketch",
                    "domain": "foundations",
                    "title_en": "B",
                    "title_ru": "Б",
                    "statement_en": "B",
                    "statement_ru": "Б",
                    "lean_decls": [],
                    "oracles": [],
                    "guides": [],
                    "sources": [],
                },
            ],
            "edges": [{"source": "n-b", "target": "n-a", "relation": "depends_on"}],
        }
        _expect_reject(
            mini_atlas,
            "out of sync",
            "stale-generated-artifacts",
            axioms={},
            repo_override=fake_root,
            check_sync=True,
        )

    print(
        "ATLAS & BLUEPRINT SELF-TEST OK: 9/9 negative controls rejected "
        "(fake lean_proved decl / lean_signature mismatch / sorryAx / empty lean_decls / "
        "DAG cycle / dangling node / broken file ref / missing falsification_criteria / "
        "stale artifacts)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify Mathematical Atlas and Lean 4 Blueprint integrity (R10 #1271)."
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument(
        "--skip-live-lean",
        action="store_true",
        help="Skip live Lean 4 kernel audit (for quick local schema checks only)",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return run_self_test()

        atlas = json.loads((REPO_ROOT / ATLAS_JSON_REL).read_text(encoding="utf-8"))
        gates_dir = REPO_ROOT / "verification/gates"
        if str(gates_dir) not in sys.path:
            sys.path.insert(0, str(gates_dir))
        import verify_claim as vc  # type: ignore[import-not-found]

        audited_axioms = None if args.skip_live_lean else _audit_live_lean_axioms(REPO_ROOT)
        summary = validate_atlas_data(
            atlas,
            repo_root=REPO_ROOT,
            audited_axioms=audited_axioms,
            expected_unified_decls=vc.EXPECTED_UNIFIED_DECLS,
            check_generated_sync=True,
        )
    except (AtlasVerificationError, OSError, json.JSONDecodeError) as exc:
        print(f"ATLAS VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"status": "ok", "live_lean": not args.skip_live_lean, **summary},
                         ensure_ascii=False, indent=2))
    else:
        sc = summary["status_counts"]
        mode = "live Lean 4 kernel" if not args.skip_live_lean else "static"
        print(
            f"ATLAS & BLUEPRINT OK ({mode}): {summary['nodes']} nodes, {summary['edges']} edges, "
            f"{summary['lean_decls_audited']}/{len(vc.EXPECTED_UNIFIED_DECLS)} Lean decls audited "
            f"(lean_proved={sc.get('lean_proved', 0)}, "
            f"oracle_verified={sc.get('oracle_verified', 0)}, "
            f"falsified={sc.get('falsified', 0)}, open={sc.get('open', 0)})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
