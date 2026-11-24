#!/usr/bin/env python3
"""Deterministic builder for the Mathematical Atlas (ATLAS.md) and Lean 4 Blueprint (R10 #1271).

Reads `research/atlas/atlas.json` and emits:
  1. `research/atlas/ATLAS.md` — Russian owner-facing overview with Mermaid DAG and tables;
  2. `verification/lean/blueprint/blueprint.json` — machine-readable Lean 4 Blueprint DAG;
  3. `verification/lean/blueprint/BLUEPRINT.md` — Lean 4 Blueprint dependency roadmap.
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ATLAS_JSON_REL = "research/atlas/atlas.json"
ATLAS_MD_REL = "research/atlas/ATLAS.md"
BLUEPRINT_JSON_REL = "verification/lean/blueprint/blueprint.json"
BLUEPRINT_MD_REL = "verification/lean/blueprint/BLUEPRINT.md"

_STATUS_LABEL_RU: dict[str, str] = {
    "lean_proved": "Доказано в Lean 4",
    "oracle_verified": "Проверено точным оракулом",
    "falsified": "Опровергнуто / контрпример",
    "open": "Открытая гипотеза / цель",
    "sketch": "Черновик / схема",
}

_KIND_LABEL_RU: dict[str, str] = {
    "definition": "Определение",
    "axiom_assumption": "Предпосылка",
    "theorem": "Теорема",
    "lemma": "Лемма",
    "counterexample": "Контрпример",
    "open_conjecture": "Открытая гипотеза",
    "generalization_target": "Цель обобщения",
}

_DOMAIN_LABEL_RU: dict[str, str] = {
    "foundations": "Фундамент и предпосылки",
    "bridge_core": "Ядро моста ОГУ <-> ARO (F1-F4)",
    "aro_exactness": "Точность аффинных правил (ADR / P1-P3 / T1-T7)",
    "counterexamples": "Границы и контрпримеры (D1-D2, E, A-S1, T2-T5)",
    "closure_scheduling": "Ценность информации и выбор расписания R (O4, O8)",
    "generalizations": "Естественные обобщения (G1-G2)",
}

_REL_ARROW: dict[str, str] = {
    "depends_on": "-->|depends_on|",
    "refutes": "-.->|refutes|",
    "generalizes": "==>|generalizes|",
    "special_case_of": "-->|special_case_of|",
    "open_gap": "-.->|open_gap|",
    "constrains_adr": "-.->|constrains_adr|",
    "related_gap": "-.->|related_gap|",
}


def _mermaid_id(node_id: str) -> str:
    return node_id.replace("-", "_")


def _escape_mermaid_label(text: str) -> str:
    return text.replace('"', "'").replace("<", "").replace(">", "")


def load_atlas(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, Any]:
    path = repo_root / ATLAS_JSON_REL
    return json.loads(path.read_text(encoding="utf-8"))


def build_blueprint_dict(atlas: dict[str, Any]) -> dict[str, Any]:
    """Extract the Lean 4 Blueprint DAG linking formal declarations, controls, and open targets."""
    nodes = atlas["nodes"]
    edges = atlas["edges"]
    blueprint_nodes: list[dict[str, Any]] = []
    deps_by_node: dict[str, list[str]] = collections.defaultdict(list)
    refuters_by_node: dict[str, list[str]] = collections.defaultdict(list)
    adr_constraints_by_node: dict[str, list[str]] = collections.defaultdict(list)

    for edge in edges:
        rel = edge["relation"]
        if rel in ("depends_on", "generalizes", "special_case_of", "open_gap"):
            deps_by_node[edge["source"]].append(edge["target"])
        elif rel == "refutes":
            refuters_by_node[edge["target"]].append(edge["source"])
        elif rel == "constrains_adr":
            adr_constraints_by_node[edge["target"]].append(edge["source"])

    lean_decl_count = 0
    for node in nodes:
        nid = node["id"]
        lean_decls = list(node.get("lean_decls", []))
        lean_decl_count += len(lean_decls)
        bp_status = {
            "lean_proved": "proved",
            "oracle_verified": "oracle_verified",
            "falsified": "falsified",
            "open": "open",
            "sketch": "sketch",
        }[node["status"]]
        entry: dict[str, Any] = {
            "id": nid,
            "kind": node["kind"],
            "domain": node["domain"],
            "title": node["title_en"],
            "blueprint_status": bp_status,
            "lean_decls": lean_decls,
            "oracles": list(node.get("oracles", [])),
            "depends_on": sorted(set(deps_by_node.get(nid, []))),
            "bounded_by_counterexamples": sorted(set(refuters_by_node.get(nid, []))),
            "adr_constrained_by": sorted(set(adr_constraints_by_node.get(nid, []))),
        }
        if "formalized_scope" in node:
            entry["formalized_scope"] = node["formalized_scope"]
        if "falsification_criteria" in node:
            entry["falsification_criteria"] = node["falsification_criteria"]
        blueprint_nodes.append(entry)

    status_counts = dict(sorted(collections.Counter(n["status"] for n in nodes).items()))
    return {
        "schema_version": 1,
        "source_atlas": ATLAS_JSON_REL,
        "lean_toolchain": "leanprover/lean4:v4.35.0-rc2",
        "allowed_axioms": ["Classical.choice", "Quot.sound", "propext"],
        "summary": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "lean_proved_nodes": status_counts.get("lean_proved", 0),
            "lean_audited_declarations": lean_decl_count,
            "status_counts": status_counts,
        },
        "nodes": blueprint_nodes,
    }


def render_blueprint_md(blueprint: dict[str, Any]) -> str:
    """Render English Lean 4 Blueprint markdown for formal verification and agent workflows."""
    s = blueprint["summary"]
    lines: list[str] = [
        "# Lean 4 Blueprint — aro-discovery v2",
        "",
        f"> Auto-generated from `{blueprint['source_atlas']}` by `research/atlas/build_atlas.py`.",
        f"> Toolchain: `{blueprint['lean_toolchain']}` | Allowed axioms: "
        + ", ".join(f"`{a}`" for a in blueprint["allowed_axioms"]),
        "",
        "## Summary",
        "",
        f"- **Blueprint nodes:** {s['total_nodes']} ({s['total_edges']} directed edges)",
        f"- **Lean 4 kernel-proved nodes:** {s['lean_proved_nodes']} "
        f"({s['lean_audited_declarations']} live-audited declarations)",
        "- **Status breakdown:** "
        + ", ".join(f"`{k}`={v}" for k, v in sorted(s["status_counts"].items())),
        "",
        "## Formal Dependency Graph (Lean Core + Open Formalization Frontier)",
        "",
        "```mermaid",
        "flowchart LR",
    ]
    focus_domains = (
        "foundations",
        "bridge_core",
        "aro_exactness",
        "closure_scheduling",
        "generalizations",
    )
    focus_nodes = [
        n
        for n in blueprint["nodes"]
        if n["blueprint_status"] in ("proved", "open") and n["domain"] in focus_domains
    ]
    focus_ids = {n["id"] for n in focus_nodes}
    for n in focus_nodes:
        mid = _mermaid_id(n["id"])
        tag = "PROVED" if n["blueprint_status"] == "proved" else "OPEN"
        lbl = _escape_mermaid_label(f"{n['id']} [{tag}]")
        lines.append(f'    {mid}["{lbl}"]')
    for n in focus_nodes:
        src = _mermaid_id(n["id"])
        for dep in n["depends_on"]:
            if dep in focus_ids:
                lines.append(f"    {_mermaid_id(dep)} --> {src}")
    lines.extend(["```", "", "## Lean 4 Proved Declarations & Formalized Scope", ""])
    lines.append("| Blueprint Node | Declaration | Lean Module | Formalized Scope |")
    lines.append("|---|---|---|---|")
    for n in blueprint["nodes"]:
        if n["blueprint_status"] != "proved":
            continue
        scope = n.get("formalized_scope", {}).get("proved_in_lean", "—")
        for d in n["lean_decls"]:
            lines.append(f"| `{n['id']}` | `{d['decl']}` | `{d['file']}` | {scope} |")

    lines.extend(["", "## Open Formalization Targets (Stage 2 -> Stage 3 Queue)", ""])
    lines.append(
        "| Target Node | Kind | Dependencies | Refuting Boundaries | ADR Constraints |"
    )
    lines.append("|---|---|---|---|---|")
    for n in blueprint["nodes"]:
        if n["blueprint_status"] != "open":
            continue
        deps = ", ".join(f"`{x}`" for x in n["depends_on"]) or "—"
        refs = ", ".join(f"`{x}`" for x in n["bounded_by_counterexamples"]) or "—"
        adrs = ", ".join(f"`{x}`" for x in n["adr_constrained_by"]) or "—"
        lines.append(f"| `{n['id']}` | `{n['kind']}` | {deps} | {refs} | {adrs} |")
    lines.append("")
    return "\n".join(lines)


def render_atlas_md(atlas: dict[str, Any]) -> str:
    """Render Russian owner-facing Mathematical Atlas overview (research/atlas/ATLAS.md)."""
    nodes = atlas["nodes"]
    edges = atlas["edges"]
    status_counts = collections.Counter(n["status"] for n in nodes)
    kind_counts = collections.Counter(n["kind"] for n in nodes)
    total_lean_decls = sum(len(n.get("lean_decls", [])) for n in nodes)

    lines: list[str] = [
        f"# {atlas['title_ru']}",
        "",
        "> Автоматически сгенерировано из [atlas.json](atlas.json) скриптом "
        "[build_atlas.py](build_atlas.py). Проверка целостности и живого ядра Lean 4: "
        "`make verify-atlas` ([verify_atlas.py](verify_atlas.py)).",
        "> Связанный Lean 4 Blueprint: "
        "[BLUEPRINT.md](../../verification/lean/blueprint/BLUEPRINT.md) "
        "и учебный пакет для LearnHarness: "
        "[02-math-atlas](../guides/02-math-atlas/01-intuition-and-map.md).",
        "",
        "## 1. Сводка Атласа",
        "",
        "| Метрика | Значение |",
        "|---|---|",
        f"| Всего узлов в графе | **{len(nodes)}** |",
        f"| Направленных связей (DAG) | **{len(edges)}** |",
        f"| Доказано в Lean 4 (`lean_proved`) | **{status_counts['lean_proved']} узлов "
        f"({total_lean_decls} живых деклараций)** |",
        f"| Проверено точными оракулами (`oracle_verified`) | "
        f"**{status_counts['oracle_verified']}** |",
        f"| Контрпримеры / границы (`falsified`) | **{status_counts['falsified']}** |",
        f"| Открытые гипотезы и цели обобщения (`open`) | **{status_counts['open']}** |",
        "",
        "Распределение по типам узлов: "
        + ", ".join(
            f"{_KIND_LABEL_RU.get(k, k)} (`{k}`): **{v}**"
            for k, v in sorted(kind_counts.items())
        )
        + ".",
        "",
        "## 2. Граф зависимостей и исследовательской границы (Mermaid DAG)",
        "",
        "```mermaid",
        "flowchart TD",
    ]

    for node in nodes:
        mid = _mermaid_id(node["id"])
        lbl = _escape_mermaid_label(f"{node['id']} ({node['status']})")
        lines.append(f'    {mid}["{lbl}"]')
    for edge in edges:
        src = _mermaid_id(edge["source"])
        dst = _mermaid_id(edge["target"])
        arrow = _REL_ARROW[edge["relation"]]
        lines.append(f"    {src} {arrow} {dst}")
    lines.extend(["```", "", "## 3. Карта узлов по доменам", ""])

    by_domain: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for node in nodes:
        by_domain[node["domain"]].append(node)

    domain_order = (
        "foundations",
        "bridge_core",
        "aro_exactness",
        "closure_scheduling",
        "counterexamples",
        "generalizations",
    )
    for dom in domain_order:
        dom_nodes = by_domain.get(dom, [])
        if not dom_nodes:
            continue
        lines.append(f"### {_DOMAIN_LABEL_RU.get(dom, dom)}")
        lines.append("")
        lines.append("| Узел | Тип | Статус | Краткое содержание | Машинная опора |")
        lines.append("|---|---|---|---|---|")
        for n in dom_nodes:
            supports: list[str] = []
            if n.get("lean_decls"):
                supports.append(
                    "Lean 4: " + ", ".join(f"`{d['decl']}`" for d in n["lean_decls"])
                )
            if n.get("oracles"):
                supports.append(
                    "Оракул: " + ", ".join(f"`{o}`" for o in n["oracles"])
                )
            sup_str = "; ".join(supports) if supports else "—"
            lines.append(
                f"| `{n['id']}` | {_KIND_LABEL_RU[n['kind']]} | "
                f"{_STATUS_LABEL_RU[n['status']]} | {n['title_ru']} | {sup_str} |"
            )
        lines.append("")

    lines.extend(
        [
            "## 4. Открытые гипотезы и цели обобщения (операционные критерии фальсификации)",
            "",
        ]
    )
    for n in nodes:
        if n["status"] != "open":
            continue
        fc = n.get("falsification_criteria", {})
        lines.extend(
            [
                f"### `{n['id']}` — {n['title_ru']}",
                "",
                f"- **Тип:** {_KIND_LABEL_RU[n['kind']]} (`{n['kind']}`)",
                f"- **Формулировка:** {n['statement_ru']}",
                f"- **Метод фальсификации (Stage 2):** `{fc.get('method', '')}` "
                f"через `{fc.get('oracle_or_battery', '')}`",
                f"- **Условие опровержения:** {fc.get('refutation_condition', '')}",
                "",
            ]
        )

    return "\n".join(lines)


def write_generated_artifacts(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, pathlib.Path]:
    atlas = load_atlas(repo_root)
    blueprint = build_blueprint_dict(atlas)

    atlas_md_path = repo_root / ATLAS_MD_REL
    bp_json_path = repo_root / BLUEPRINT_JSON_REL
    bp_md_path = repo_root / BLUEPRINT_MD_REL

    bp_json_path.parent.mkdir(parents=True, exist_ok=True)
    atlas_md_path.write_text(render_atlas_md(atlas), encoding="utf-8")
    bp_json_path.write_text(
        json.dumps(blueprint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    bp_md_path.write_text(render_blueprint_md(blueprint), encoding="utf-8")
    return {
        "atlas_md": atlas_md_path,
        "blueprint_json": bp_json_path,
        "blueprint_md": bp_md_path,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate ATLAS.md and Lean 4 Blueprint from research/atlas/atlas.json"
    )
    parser.add_argument(
        "--repo-root",
        type=pathlib.Path,
        default=REPO_ROOT,
        help="Repository root directory",
    )
    args = parser.parse_args(argv)
    outputs = write_generated_artifacts(args.repo_root.resolve())
    for key, path in outputs.items():
        print(f"GENERATED {key}: {path.relative_to(args.repo_root.resolve())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
