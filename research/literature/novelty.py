#!/usr/bin/env python3
"""Novelty & Proof-Technique Checker for open Atlas conjectures (R11 #1273).

CLI:
  python3 -m research.literature.novelty --conjecture <atlas_node_id> [--live] [--json]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections.abc import Callable, Sequence
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.literature.radar import (  # noqa: E402
    ATLAS_JSON_REL,
    FetchFn,
    RadarFetchError,
    deduplicate_records,
    load_catalog,
    normalize_arxiv_id,
    normalize_doi,
    normalize_title,
    search_all,
)

_STOPWORDS = frozenset(
    {
        "the",
        "and",
        "for",
        "with",
        "from",
        "that",
        "this",
        "into",
        "over",
        "under",
        "when",
        "where",
        "which",
        "their",
        "there",
        "such",
        "every",
        "each",
        "both",
        "some",
        "more",
        "than",
        "only",
        "also",
        "between",
        "through",
        "using",
        "via",
        "beyond",
    }
)


class NoveltyCheckError(RuntimeError):
    """Raised when an invalid conjecture node ID or corrupted catalog/atlas is encountered."""


def _tokenize(text: str) -> set[str]:
    return {
        tok
        for tok in re.findall(r"[a-z0-9_]{3,}", text.lower())
        if tok not in _STOPWORDS and not tok.isdigit()
    }


def _matches_catalog_paper(rec: Any, paper: dict[str, Any]) -> bool:
    """Match a live record against a catalog entry without conflating differing strong IDs."""
    rec_arx = normalize_arxiv_id(rec.arxiv_id)
    rec_doi = normalize_doi(rec.doi)
    cat_arx = normalize_arxiv_id(paper.get("arxiv_id"))
    cat_doi = normalize_doi(paper.get("doi"))

    if rec_arx and cat_arx and rec_arx == cat_arx:
        return True
    if rec_doi and cat_doi and rec_doi == cat_doi:
        return True

    rec_title = normalize_title(rec.title)
    cat_title = normalize_title(paper.get("title"))
    if rec_title and cat_title and rec_title == cat_title:
        if rec_doi and cat_doi and rec_doi != cat_doi:
            return False
        return not (rec_arx and cat_arx and rec_arx != cat_arx)
    return False


def _derive_live_query(node: dict[str, Any]) -> str:
    title = str(node.get("title_en", ""))
    cleaned = re.sub(r"^[A-Z]\d+[a-z]?:\s*", "", title)
    cleaned = re.sub(r"[^A-Za-z0-9\s-]", " ", cleaned)
    words = [w for w in cleaned.split() if len(w) >= 3][:8]
    return " ".join(words) or "adjustable robust optimization affine decision rules"


def check_conjecture(
    conjecture_id: str,
    *,
    repo_root: pathlib.Path = REPO_ROOT,
    top_k: int = 5,
    live: bool = False,
    live_sources: Sequence[str] = ("arxiv", "openalex"),
    live_max_results: int = 5,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] | None = None,
) -> dict[str, Any]:
    """Assess literature novelty, counterexamples, and proof techniques for an Atlas node."""
    atlas = json.loads((repo_root / ATLAS_JSON_REL).read_text(encoding="utf-8"))
    catalog = load_catalog(repo_root)

    node_by_id = {n["id"]: n for n in atlas["nodes"]}
    if conjecture_id not in node_by_id:
        known = ", ".join(sorted(node_by_id)[:10])
        raise NoveltyCheckError(
            f"Unknown Atlas node id {conjecture_id!r} (examples: {known}, ...)"
        )
    node = node_by_id[conjecture_id]

    # Collect 1-hop Atlas neighborhood (dependencies + boundary counterexamples)
    neighbor_ids: set[str] = set()
    boundary_counterexamples: list[dict[str, str]] = []
    for edge in atlas["edges"]:
        src, dst, rel = edge["source"], edge["target"], edge["relation"]
        if src == conjecture_id:
            neighbor_ids.add(dst)
        elif dst == conjecture_id:
            neighbor_ids.add(src)
            if rel in ("refutes", "constrains_adr"):
                other = node_by_id[src]
                boundary_counterexamples.append(
                    {
                        "node_id": src,
                        "relation": rel,
                        "title_en": other["title_en"],
                        "status": other["status"],
                    }
                )

    node_tokens = _tokenize(
        f"{node.get('title_en', '')} {node.get('statement_en', '')} "
        f"{node.get('domain', '')}"
    )

    direct_links: list[dict[str, Any]] = []
    neighbor_links: list[dict[str, Any]] = []
    scored_papers: list[tuple[float, dict[str, Any]]] = []
    techniques: dict[str, list[str]] = {}

    for paper in catalog["papers"]:
        pid = paper["id"]
        direct_rels = [
            lk for lk in paper.get("atlas_links", []) if lk["node_id"] == conjecture_id
        ]
        neigh_rels = [
            lk for lk in paper.get("atlas_links", []) if lk["node_id"] in neighbor_ids
        ]

        if direct_rels:
            for lk in direct_rels:
                direct_links.append(
                    {
                        "paper_id": pid,
                        "title": paper["title"],
                        "year": paper["year"],
                        "relation": lk["relation"],
                        "note": lk.get("note", ""),
                    }
                )
            for tech in paper.get("techniques", []):
                techniques.setdefault(tech, []).append(pid)
        elif neigh_rels:
            for lk in neigh_rels:
                neighbor_links.append(
                    {
                        "paper_id": pid,
                        "title": paper["title"],
                        "year": paper["year"],
                        "via_node": lk["node_id"],
                        "relation": lk["relation"],
                    }
                )

        p_tokens = _tokenize(
            " ".join(
                [
                    paper.get("title", ""),
                    paper.get("abstract", ""),
                    " ".join(paper.get("key_results", [])),
                    " ".join(paper.get("techniques", [])),
                ]
            )
        )
        overlap = len(node_tokens & p_tokens)
        union = len(node_tokens | p_tokens) or 1
        jaccard = overlap / union
        bonus = (0.5 if direct_rels else 0.0) + (0.15 if neigh_rels else 0.0)
        score = round(jaccard + bonus, 4)
        scored_papers.append((score, paper))

    scored_papers.sort(key=lambda item: (-item[0], item[1]["year"], item[1]["id"]))
    closest = [
        {
            "paper_id": p["id"],
            "title": p["title"],
            "authors": p["authors"],
            "year": p["year"],
            "score": sc,
            "techniques": p.get("techniques", []),
            "corpus_path": p.get("corpus_path"),
        }
        for sc, p in scored_papers[:top_k]
    ]
    for item in closest[:3]:
        for tech in item["techniques"]:
            if item["paper_id"] not in techniques.setdefault(tech, []):
                techniques[tech].append(item["paper_id"])

    live_candidates: list[dict[str, Any]] = []
    live_query: str | None = None
    if live:
        live_query = _derive_live_query(node)
        kwargs: dict[str, Any] = {
            "sources": live_sources,
            "max_results": live_max_results,
            "fetch_fn": fetch_fn,
        }
        if sleep_fn is not None:
            kwargs["sleep_fn"] = sleep_fn
        fetched = deduplicate_records(search_all(live_query, **kwargs))
        for rec in fetched:
            in_catalog = any(_matches_catalog_paper(rec, p) for p in catalog["papers"])
            live_candidates.append(
                {
                    **rec.to_dict(),
                    "already_in_catalog": bool(in_catalog),
                }
            )

    if node["status"] == "lean_proved":
        assessment = "already_proved_in_lean"
    elif node["status"] == "falsified":
        assessment = "known_counterexample_in_atlas"
    elif boundary_counterexamples:
        assessment = "open_with_explicit_counterexample_boundaries"
    elif direct_links:
        assessment = "open_with_related_literature_baselines"
    else:
        assessment = "open_unmapped_frontier"

    return {
        "conjecture_id": conjecture_id,
        "title_en": node["title_en"],
        "title_ru": node["title_ru"],
        "kind": node["kind"],
        "status": node["status"],
        "novelty_assessment": assessment,
        "direct_literature_links": direct_links,
        "neighbor_literature_links": neighbor_links,
        "boundary_counterexamples": boundary_counterexamples,
        "closest_papers": closest,
        "applicable_techniques": [
            {"technique": t, "papers": sorted(set(ps))} for t, ps in sorted(techniques.items())
        ],
        "live_query": live_query,
        "live_candidates": live_candidates,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check literature novelty, boundaries, and techniques for an Atlas node."
    )
    parser.add_argument(
        "--conjecture",
        required=True,
        help="Atlas node ID (e.g. conj-o1-adr-exactness-char, conj-o4-closure-scheduling)",
    )
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--live", action="store_true", help="Also query live arXiv/OpenAlex APIs")
    parser.add_argument("--sources", default="arxiv,openalex")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    srcs = [s.strip() for s in args.sources.split(",") if s.strip()]
    try:
        report = check_conjecture(
            args.conjecture,
            top_k=args.top_k,
            live=args.live,
            live_sources=srcs,
        )
    except (NoveltyCheckError, RadarFetchError, OSError, json.JSONDecodeError) as exc:
        print(f"NOVELTY CHECK FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"=== Novelty Report: {report['conjecture_id']} ({report['status']}) ===")
        print(f"Title: {report['title_en']}")
        print(f"Assessment: {report['novelty_assessment']}")
        print(f"Direct links ({len(report['direct_literature_links'])}):")
        for lk in report["direct_literature_links"]:
            print(f"  - [{lk['relation']}] {lk['paper_id']} ({lk['year']}): {lk['title']}")
        print(f"Boundary counterexamples ({len(report['boundary_counterexamples'])}):")
        for ce in report["boundary_counterexamples"]:
            print(f"  - [{ce['relation']}] {ce['node_id']}: {ce['title_en']}")
        print("Closest papers:")
        for cp in report["closest_papers"]:
            print(f"  - ({cp['score']:.3f}) {cp['paper_id']} ({cp['year']}): {cp['title']}")
        print("Applicable techniques:")
        for t in report["applicable_techniques"]:
            print(f"  - {t['technique']} (from {', '.join(t['papers'])})")
        if report["live_query"] is not None:
            print(f"Live candidates for {report['live_query']!r}: {len(report['live_candidates'])}")
            for lc in report["live_candidates"]:
                tag = "known" if lc["already_in_catalog"] else "NEW"
                print(f"  - [{tag}] ({lc.get('year') or '?'}) {lc['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
