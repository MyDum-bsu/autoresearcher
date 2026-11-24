#!/usr/bin/env python3
"""Deterministic verifier for Literature Radar & Knowledge Graph (R11 #1273).

Enforces (zero `assert` — works identically under `-B` and `-B -O`):
  1. Strict schema validation of `research/literature/catalog.json`;
  2. Zero duplicate canonical DOIs, arXiv IDs (version-stripped), or normalized titles;
  3. Every `corpus_path` exists inside repo root (no path traversal) and is registered in
     `corpus/MANIFEST.md`, `corpus/intake/`, or `corpus/extra/`;
  4. Every `atlas_links[].node_id` exists in `research/atlas/atlas.json` with a valid relation
     in `ALLOWED_LINK_RELATIONS`, and every open Atlas conjecture/generalization has >= 1 link;
  5. Byte-for-byte freshness of generated `research/literature/LITERATURE.md`;
  6. Negative `--self-test` rejecting duplicate DOI/arXiv/title, dangling Atlas node ID,
     invalid link relation, broken `corpus_path`, and stale `LITERATURE.md`.
"""

from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import json
import pathlib
import re
import sys
import tempfile
from typing import Any

import pypdf

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.literature import ALLOWED_LINK_RELATIONS, ALLOWED_RADAR_SOURCES  # noqa: E402
from research.literature.radar import (  # noqa: E402
    ATLAS_JSON_REL,
    CATALOG_JSON_REL,
    LITERATURE_MD_REL,
    build_literature_md,
    normalize_arxiv_id,
    normalize_doi,
    normalize_title,
)

_MANIFEST_ENTRY_RE = re.compile(r"^[0-9a-f]{64}\s+(corpus/.+)$")
_DOI_FORMAT_RE = re.compile(r"^10\.\d{4,9}/\S+$")
_ARXIV_FORMAT_RE = re.compile(r"^(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[a-z-]+)?/\d{7})$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def _file_sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class LiteratureVerificationError(RuntimeError):
    """Raised when a Literature catalog or Atlas link invariant fails."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise LiteratureVerificationError(msg)


def _load_manifest_paths(repo_root: pathlib.Path) -> set[str]:
    manifest = repo_root / "corpus/MANIFEST.md"
    if not manifest.is_file():
        return set()
    out: set[str] = set()
    for line in manifest.read_text(encoding="utf-8").splitlines():
        m = _MANIFEST_ENTRY_RE.match(line.strip())
        if m:
            out.add(m.group(1).strip())
    return out


def validate_catalog_data(
    catalog: dict[str, Any],
    atlas: dict[str, Any],
    repo_root: pathlib.Path = REPO_ROOT,
    *,
    check_generated_sync: bool = True,
) -> dict[str, Any]:
    """Validate catalog.json schema, dedup keys, corpus paths, Atlas links, and LITERATURE.md."""
    errors: list[str] = []

    if not isinstance(catalog, dict):
        raise LiteratureVerificationError("Catalog root must be a JSON object")
    if catalog.get("schema_version") != 1:
        errors.append(f"Unsupported schema_version: {catalog.get('schema_version')!r}")

    papers = catalog.get("papers")
    if not isinstance(papers, list) or not papers:
        raise LiteratureVerificationError("Catalog 'papers' must be a non-empty list")

    atlas_nodes = {n["id"]: n for n in atlas.get("nodes", [])}
    open_atlas_ids = {
        nid for nid, n in atlas_nodes.items() if n.get("status") == "open"
    }
    manifest_paths = _load_manifest_paths(repo_root)
    root_res = repo_root.resolve()
    corpus_res = (root_res / "corpus").resolve()

    seen_ids: set[str] = set()
    seen_dois: dict[str, str] = {}
    seen_arxivs: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    linked_atlas_nodes: set[str] = set()
    rel_counts: collections.Counter[str] = collections.Counter()

    for idx, paper in enumerate(papers):
        if not isinstance(paper, dict):
            errors.append(f"Paper #{idx} is not an object")
            continue
        pid = paper.get("id")
        if not isinstance(pid, str) or not re.match(r"^[a-z0-9][a-z0-9-]*$", pid):
            errors.append(f"Paper #{idx}: invalid id {pid!r}")
            continue
        if pid in seen_ids:
            errors.append(f"Duplicate paper id: {pid!r}")
            continue
        seen_ids.add(pid)

        title = paper.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"Paper '{pid}': missing non-empty 'title'")
        else:
            nt = normalize_title(title)
            if not nt:
                errors.append(f"Paper '{pid}': title normalizes to empty string")
            elif nt in seen_titles:
                errors.append(
                    f"Duplicate normalized title between '{seen_titles[nt]}' and '{pid}': {title!r}"
                )
            else:
                seen_titles[nt] = pid

        authors = paper.get("authors")
        if (
            not isinstance(authors, list)
            or not authors
            or not all(isinstance(a, str) and a.strip() for a in authors)
        ):
            errors.append(f"Paper '{pid}': 'authors' must be a non-empty list of strings")

        year = paper.get("year")
        if not isinstance(year, int) or isinstance(year, bool) or not (1950 <= year <= 2100):
            errors.append(f"Paper '{pid}': invalid publication year {year!r}")

        src = paper.get("source")
        if src not in ALLOWED_RADAR_SOURCES:
            errors.append(f"Paper '{pid}': invalid source {src!r}")

        abstract = paper.get("abstract")
        if not isinstance(abstract, str) or not abstract.strip():
            errors.append(f"Paper '{pid}': missing non-empty 'abstract'")

        for list_field in ("key_results", "techniques"):
            vals = paper.get(list_field)
            if (
                not isinstance(vals, list)
                or not vals
                or not all(isinstance(v, str) and v.strip() for v in vals)
            ):
                errors.append(f"Paper '{pid}': '{list_field}' must be a non-empty list of strings")

        raw_doi = paper.get("doi")
        if raw_doi is not None:
            ndoi = normalize_doi(raw_doi)
            if not ndoi or not _DOI_FORMAT_RE.match(ndoi):
                errors.append(f"Paper '{pid}': malformed DOI {raw_doi!r}")
            elif ndoi in seen_dois:
                errors.append(
                    f"Duplicate DOI '{ndoi}' between '{seen_dois[ndoi]}' and '{pid}'"
                )
            else:
                seen_dois[ndoi] = pid

        raw_arxiv = paper.get("arxiv_id")
        if raw_arxiv is not None:
            narx = normalize_arxiv_id(raw_arxiv)
            if not narx or not _ARXIV_FORMAT_RE.match(narx):
                errors.append(f"Paper '{pid}': malformed arXiv ID {raw_arxiv!r}")
            elif narx in seen_arxivs:
                errors.append(
                    f"Duplicate arXiv ID '{narx}' between '{seen_arxivs[narx]}' and '{pid}'"
                )
            else:
                seen_arxivs[narx] = pid

        links = paper.get("atlas_links")
        has_links = isinstance(links, list) and len(links) > 0

        cpath = paper.get("corpus_path")
        actual_pdf_pages: int | None = None
        if cpath is None:
            if has_links:
                errors.append(
                    f"Paper '{pid}': missing 'corpus_path' PDF inside corpus/ "
                    "(required for Atlas link provenance)"
                )
        elif not isinstance(cpath, str) or not cpath.strip():
            errors.append(f"Paper '{pid}': invalid corpus_path {cpath!r}")
        else:
            raw_p = pathlib.Path(cpath)
            if raw_p.is_absolute() or ".." in raw_p.parts:
                errors.append(
                    f"Paper '{pid}': corpus_path must be relative inside corpus/: {cpath!r}"
                )
            elif not cpath.startswith("corpus/"):
                errors.append(
                    f"Paper '{pid}': corpus_path must be a .pdf file inside corpus/: {cpath!r}"
                )
            else:
                omitted_meta_path = corpus_res / "public-omitted-pdfs.json"
                omitted_pdfs = json.loads(omitted_meta_path.read_text(encoding="utf-8")) if omitted_meta_path.is_file() else {}
                resolved = (root_res / raw_p).resolve()
                is_omitted_pub = (
                    resolved.is_relative_to(corpus_res)
                    and not resolved.is_file()
                    and cpath in omitted_pdfs
                )
                if not resolved.is_relative_to(corpus_res) or (not resolved.is_file() and not is_omitted_pub):
                    errors.append(f"Paper '{pid}': corpus_path not found in corpus/: {cpath!r}")
                elif resolved.suffix.lower() != ".pdf":
                    errors.append(
                        f"Paper '{pid}': corpus_path must be a .pdf file inside corpus/: {cpath!r}"
                    )
                else:
                    if (
                        not cpath.startswith(("corpus/extra/", "corpus/intake/"))
                        and manifest_paths
                        and cpath not in manifest_paths
                    ):
                        errors.append(
                            f"Paper '{pid}': corpus_path not in corpus/MANIFEST.md: {cpath!r}"
                        )
                    decl_sha = paper.get("pdf_sha256")
                    actual_sha = omitted_pdfs[cpath]["sha256"] if is_omitted_pub else _file_sha256(resolved)
                    if not isinstance(decl_sha, str) or not _SHA256_RE.match(decl_sha):
                        errors.append(f"Paper '{pid}': missing or malformed 'pdf_sha256'")
                    elif decl_sha != actual_sha:
                        errors.append(
                            f"Paper '{pid}': pdf_sha256 mismatch for {cpath}: "
                            f"declared {decl_sha[:12]}, actual {actual_sha[:12]}"
                        )
                    try:
                        actual_pdf_pages = int(omitted_pdfs[cpath]["page_count"]) if is_omitted_pub else len(pypdf.PdfReader(str(resolved)).pages)
                    except Exception as exc:
                        errors.append(
                            f"Paper '{pid}': failed to read PDF pages for {cpath}: {exc}"
                        )
                    else:
                        decl_pages = paper.get("page_count")
                        if (
                            not isinstance(decl_pages, int)
                            or isinstance(decl_pages, bool)
                            or decl_pages != actual_pdf_pages
                        ):
                            errors.append(
                                f"Paper '{pid}': page_count mismatch for {cpath}: "
                                f"declared {decl_pages!r}, actual {actual_pdf_pages}"
                            )

        if not isinstance(links, list) or not links:
            errors.append(f"Paper '{pid}': must declare >= 1 entry in 'atlas_links'")
        else:
            seen_pair: set[tuple[str, str]] = set()
            for lidx, lk in enumerate(links):
                if not isinstance(lk, dict):
                    errors.append(f"Paper '{pid}' atlas_links[{lidx}] is not an object")
                    continue
                nid = lk.get("node_id")
                rel = lk.get("relation")
                note = lk.get("note")
                if not isinstance(nid, str) or nid not in atlas_nodes:
                    errors.append(
                        f"Paper '{pid}' atlas_links[{lidx}]: unknown Atlas node_id {nid!r}"
                    )
                if rel not in ALLOWED_LINK_RELATIONS:
                    errors.append(
                        f"Paper '{pid}' atlas_links[{lidx}]: invalid relation {rel!r}"
                    )
                if not isinstance(note, str) or not note.strip():
                    errors.append(
                        f"Paper '{pid}' atlas_links[{lidx}]: missing non-empty 'note'"
                    )
                phys_pages = lk.get("physical_pages")
                if (
                    not isinstance(phys_pages, list)
                    or not phys_pages
                    or not all(
                        isinstance(pg, int) and not isinstance(pg, bool) and pg >= 1
                        for pg in phys_pages
                    )
                ):
                    errors.append(
                        f"Paper '{pid}' atlas_links[{lidx}]: missing valid 'physical_pages'"
                    )
                elif actual_pdf_pages is not None:
                    bad_pgs = [pg for pg in phys_pages if pg > actual_pdf_pages]
                    if bad_pgs:
                        errors.append(
                            f"Paper '{pid}' atlas_links[{lidx}]: physical_pages {bad_pgs} "
                            f"out of range 1..{actual_pdf_pages} for {cpath}"
                        )
                if isinstance(nid, str) and isinstance(rel, str):
                    pair = (nid, rel)
                    if pair in seen_pair:
                        errors.append(f"Paper '{pid}': duplicate atlas link {pair}")
                    seen_pair.add(pair)
                    if nid in atlas_nodes:
                        linked_atlas_nodes.add(nid)
                        rel_counts[rel] += 1

    uncovered_open = sorted(open_atlas_ids - linked_atlas_nodes)
    if uncovered_open:
        errors.append(
            f"Open Atlas conjectures/generalizations with zero literature links: {uncovered_open}"
        )

    if check_generated_sync and not errors:
        expected_md = build_literature_md(catalog, atlas)
        md_path = repo_root / LITERATURE_MD_REL
        if not md_path.is_file():
            errors.append(f"Missing generated overview: {LITERATURE_MD_REL}")
        elif md_path.read_text(encoding="utf-8") != expected_md:
            errors.append(
                f"Generated {LITERATURE_MD_REL} is out of sync with {CATALOG_JSON_REL} "
                "(run `python3 -B -m research.literature.radar --build-md`)"
            )

    if errors:
        raise LiteratureVerificationError(
            "Literature verification failed:\n  - " + "\n  - ".join(errors)
        )

    return {
        "papers": len(papers),
        "dois": len(seen_dois),
        "arxiv_ids": len(seen_arxivs),
        "atlas_links": sum(rel_counts.values()),
        "atlas_nodes_covered": len(linked_atlas_nodes),
        "open_nodes_covered": len(open_atlas_ids),
        "relation_counts": dict(sorted(rel_counts.items())),
    }


def run_self_test() -> int:
    """Negative self-tests (zero `assert`, works identically under `-B` and `-B -O`)."""
    base_cat = json.loads((REPO_ROOT / CATALOG_JSON_REL).read_text(encoding="utf-8"))
    base_atlas = json.loads((REPO_ROOT / ATLAS_JSON_REL).read_text(encoding="utf-8"))

    def _expect_reject(
        mutated: dict[str, Any],
        expected_substr: str,
        label: str,
        *,
        repo_override: pathlib.Path | None = None,
        check_sync: bool = False,
    ) -> None:
        rejected = False
        err_msg = ""
        try:
            validate_catalog_data(
                mutated,
                base_atlas,
                repo_root=repo_override or REPO_ROOT,
                check_generated_sync=check_sync,
            )
        except LiteratureVerificationError as exc:
            err_msg = str(exc)
            rejected = expected_substr.lower() in err_msg.lower()
        _expect(
            rejected,
            f"Self-test '{label}' NOT rejected ({expected_substr!r}): {err_msg}",
        )

    # 1. Duplicate DOI (with https://doi.org/ prefix variation) MUST fail
    m1 = copy.deepcopy(base_cat)
    m1["papers"][0]["doi"] = "https://doi.org/" + m1["papers"][1]["doi"]
    _expect_reject(m1, "Duplicate DOI", "duplicate-doi")

    # 2. Duplicate arXiv ID (with version suffix variation v1 vs v9) MUST fail
    m2 = copy.deepcopy(base_cat)
    arx_paper = next(p for p in m2["papers"] if p.get("arxiv_id"))
    non_arx = next(p for p in m2["papers"] if not p.get("arxiv_id"))
    non_arx["arxiv_id"] = normalize_arxiv_id(arx_paper["arxiv_id"]) + "v9"
    _expect_reject(m2, "Duplicate arXiv ID", "duplicate-arxiv")

    # 3. Duplicate normalized title MUST fail
    m3 = copy.deepcopy(base_cat)
    m3["papers"][0]["title"] = m3["papers"][1]["title"].upper() + "!"
    _expect_reject(m3, "Duplicate normalized title", "duplicate-title")

    # 4. Dangling Atlas node_id MUST fail
    m4 = copy.deepcopy(base_cat)
    m4["papers"][0]["atlas_links"][0]["node_id"] = "conj-nonexistent-999"
    _expect_reject(m4, "unknown Atlas node_id", "dangling-atlas-node")

    # 5. Invalid link relation MUST fail
    m5 = copy.deepcopy(base_cat)
    m5["papers"][0]["atlas_links"][0]["relation"] = "vaguely_mentions"
    _expect_reject(m5, "invalid relation", "invalid-link-relation")

    # 6. Broken corpus_path MUST fail
    m6 = copy.deepcopy(base_cat)
    m6["papers"][0]["corpus_path"] = "corpus/99_Nonexistent_Paper.pdf"
    _expect_reject(m6, "corpus_path not found", "broken-corpus-path")

    # 7. Tampered pdf_sha256 MUST fail
    m7_sha = copy.deepcopy(base_cat)
    m7_sha["papers"][0]["pdf_sha256"] = "0" * 64
    _expect_reject(m7_sha, "pdf_sha256 mismatch", "tampered-pdf-sha256")

    # 8. Out-of-bounds physical_pages MUST fail
    m8_pg = copy.deepcopy(base_cat)
    m8_pg["papers"][0]["atlas_links"][0]["physical_pages"] = [999]
    _expect_reject(m8_pg, "out of range", "out-of-bounds-physical-page")

    # 9. Non-PDF corpus_path (existing README.md) with stripped PDF metadata MUST fail
    m9_nonpdf = copy.deepcopy(base_cat)
    m9_nonpdf["papers"][0]["corpus_path"] = "README.md"
    m9_nonpdf["papers"][0].pop("pdf_sha256", None)
    m9_nonpdf["papers"][0].pop("page_count", None)
    for lk in m9_nonpdf["papers"][0]["atlas_links"]:
        lk.pop("physical_pages", None)
    _expect_reject(m9_nonpdf, "must be a .pdf file inside corpus/", "non-pdf-corpus-path")

    # 10. Stale LITERATURE.md MUST fail sync check (with real corpus symlinked)
    with tempfile.TemporaryDirectory(prefix="aro-lit-sync-") as tmp:
        fake_root = pathlib.Path(tmp)
        (fake_root / "corpus").symlink_to(REPO_ROOT / "corpus")
        (fake_root / LITERATURE_MD_REL).parent.mkdir(parents=True, exist_ok=True)
        (fake_root / LITERATURE_MD_REL).write_text("# stale\n", encoding="utf-8")
        m10 = copy.deepcopy(base_cat)
        _expect_reject(
            m10,
            "out of sync",
            "stale-literature-md",
            repo_override=fake_root,
            check_sync=True,
        )

    print(
        "LITERATURE VERIFIER SELF-TEST OK: 10/10 negative controls rejected "
        "(duplicate DOI / duplicate arXiv / duplicate title / dangling Atlas node / "
        "invalid relation / broken corpus_path / tampered pdf_sha256 / "
        "out-of-bounds physical_pages / non-PDF corpus_path / stale LITERATURE.md)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify Literature Radar catalog & Atlas knowledge links (R11 #1273)."
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return run_self_test()
        catalog = json.loads((REPO_ROOT / CATALOG_JSON_REL).read_text(encoding="utf-8"))
        atlas = json.loads((REPO_ROOT / ATLAS_JSON_REL).read_text(encoding="utf-8"))
        summary = validate_catalog_data(catalog, atlas, REPO_ROOT, check_generated_sync=True)
    except (LiteratureVerificationError, OSError, json.JSONDecodeError) as exc:
        print(f"LITERATURE VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"status": "ok", **summary}, ensure_ascii=False, indent=2))
    else:
        print(
            f"LITERATURE CATALOG OK: {summary['papers']} papers "
            f"({summary['dois']} DOIs, {summary['arxiv_ids']} arXiv IDs), "
            f"{summary['atlas_links']} Atlas links covering "
            f"{summary['atlas_nodes_covered']} Atlas nodes "
            f"(all {summary['open_nodes_covered']} open targets covered)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
