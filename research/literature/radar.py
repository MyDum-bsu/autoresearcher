#!/usr/bin/env python3
"""Literature Radar client (arXiv / Semantic Scholar / OpenAlex) & catalog overview builder.

Features:
  - Pure-stdlib HTTP clients with explicit timeouts and fail-closed rate-limit backoff
    (HTTP 429 / 502 / 503 / 504 respecting Retry-After, injectable transport & sleep for
    100% offline deterministic unit tests);
  - Canonical deduplication by arXiv ID (version-stripped), DOI, and normalized title with
    metadata merging;
  - Deterministic generator for `research/literature/LITERATURE.md` linking papers to
    `research/atlas/atlas.json` nodes.
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import email.utils
import json
import math
import pathlib
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections.abc import Callable, Sequence
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

CATALOG_JSON_REL = "research/literature/catalog.json"
LITERATURE_MD_REL = "research/literature/LITERATURE.md"
ATLAS_JSON_REL = "research/atlas/atlas.json"

ARXIV_API_URL = "https://export.arxiv.org/api/query"
SEMANTIC_SCHOLAR_API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENALEX_API_URL = "https://api.openalex.org/works"

_ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

_TRANSIENT_HTTP_CODES = frozenset({429, 500, 502, 503, 504})
_USER_AGENT = "aro-discovery-literature-radar/0.2 (+https://local.aro-discovery)"
_ARXIV_ID_RE = re.compile(r"^(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[a-z-]+)?/\d{7})$")


class RadarFetchError(RuntimeError):
    """Raised when an upstream literature API fails after bounded retries/timeouts."""


@dataclasses.dataclass(frozen=True)
class HttpResponse:
    status: int
    body: bytes
    headers: dict[str, str] = dataclasses.field(default_factory=dict)


FetchFn = Callable[[str, dict[str, str], float], HttpResponse]


@dataclasses.dataclass
class PaperRecord:
    title: str
    authors: list[str]
    year: int | None
    arxiv_id: str | None = None
    doi: str | None = None
    venue: str = ""
    abstract: str = ""
    url: str = ""
    sources: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self) -> None:
        if self.arxiv_id is not None:
            norm = normalize_arxiv_id(self.arxiv_id)
            if norm is None:
                raise ValueError(f"Invalid arXiv identifier for PaperRecord: {self.arxiv_id!r}")
            self.arxiv_id = norm

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def normalize_arxiv_id(raw: str | None) -> str | None:
    """Canonical arXiv identifier: lowercase, no `arXiv:` prefix, no URL, no `vN` version.

    Returns `None` if `raw` does not match a valid modern (`YYMM.NNNN[N]`) or classic
    (`archive[.subject]/YYMMNNN`) arXiv identifier.
    """
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip()
    if not s:
        return None
    s = re.sub(r"^https?://arxiv\.org/(?:abs|pdf)/", "", s, flags=re.I)
    s = re.sub(r"^arxiv:\s*", "", s, flags=re.I)
    s = re.sub(r"\.pdf$", "", s, flags=re.I)
    s = re.sub(r"v\d+$", "", s, flags=re.I)
    s = s.strip().lower()
    if not _ARXIV_ID_RE.match(s):
        return None
    return s


def normalize_doi(raw: str | None) -> str | None:
    """Canonical DOI: lowercase, stripped of URL/prefix and trailing punctuation."""
    if not raw or not isinstance(raw, str):
        return None
    s = raw.strip()
    if not s:
        return None
    s = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", s, flags=re.I)
    s = re.sub(r"^doi:\s*", "", s, flags=re.I)
    s = s.rstrip(".,;)")
    s = s.strip().lower()
    return s or None


def normalize_title(raw: str | None) -> str:
    """Canonical title key for deduplication (NFKD lowercase alphanumeric tokens)."""
    if not raw or not isinstance(raw, str):
        return ""
    decomposed = unicodedata.normalize("NFKD", raw)
    ascii_only = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    tokens = re.findall(r"[a-z0-9]+", ascii_only.lower())
    return " ".join(tokens)


def reconstruct_openalex_abstract(inverted_index: dict[str, list[int]] | None) -> str:
    """Reconstruct plain-text abstract from OpenAlex `abstract_inverted_index`."""
    if not isinstance(inverted_index, dict) or not inverted_index:
        return ""
    positions: list[tuple[int, str]] = []
    for word, indices in inverted_index.items():
        if not isinstance(indices, list):
            continue
        for pos in indices:
            if isinstance(pos, int) and pos >= 0:
                positions.append((pos, str(word)))
    positions.sort(key=lambda item: item[0])
    return " ".join(w for _, w in positions)


def _default_http_fetch(url: str, headers: dict[str, str], timeout: float) -> HttpResponse:
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT, **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k.lower(): v for k, v in resp.headers.items()}
            return HttpResponse(status=int(resp.status), body=resp.read(), headers=hdrs)
    except urllib.error.HTTPError as exc:
        hdrs = {k.lower(): v for k, v in (exc.headers.items() if exc.headers else [])}
        body = b""
        try:
            body = exc.read()
        except OSError:
            body = b""
        return HttpResponse(status=int(exc.code), body=body, headers=hdrs)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RadarFetchError(f"Network/timeout error fetching {url}: {exc}") from exc


def _parse_retry_after(value: str | None) -> float | None:
    """Parse HTTP Retry-After header as raw delay in seconds (no silent clamping)."""
    if not value:
        return None
    s = value.strip()
    try:
        secs = float(s)
        if math.isfinite(secs) and secs >= 0:
            return secs
    except ValueError:
        pass
    try:
        dt = email.utils.parsedate_to_datetime(s)
        return max(dt.timestamp() - time.time(), 0.0)
    except (TypeError, ValueError):
        return None


def fetch_with_backoff(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout: float = 15.0,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_backoff: float = 30.0,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> HttpResponse:
    """Fail-closed HTTP GET with bounded backoff on 429/5xx and honest Retry-After enforcement."""
    transport = fetch_fn or _default_http_fetch
    req_headers = dict(headers or {})
    last_error = ""
    for attempt in range(max_retries + 1):
        try:
            resp = transport(url, req_headers, timeout)
        except (RadarFetchError, TimeoutError, OSError) as exc:
            last_error = str(exc)
            if attempt >= max_retries:
                raise RadarFetchError(
                    f"Exhausted {max_retries} retries on {url}: {last_error}"
                ) from exc
            sleep_fn(min(base_delay * (2**attempt), max_backoff))
            continue

        if 200 <= resp.status < 300:
            return resp
        if resp.status in _TRANSIENT_HTTP_CODES:
            last_error = f"HTTP {resp.status}"
            retry_hdr = resp.headers.get("retry-after") or resp.headers.get("Retry-After")
            retry_after = _parse_retry_after(retry_hdr)
            if retry_after is not None and retry_after > max_backoff:
                raise RadarFetchError(
                    f"Rate-limit Retry-After ({retry_after:.1f}s) exceeds max_backoff "
                    f"({max_backoff:.1f}s) on {url}; refusing premature retry"
                )
            if attempt >= max_retries:
                raise RadarFetchError(
                    f"Upstream returned {last_error} on {url} after {max_retries} retries"
                )
            delay = retry_after if retry_after is not None else min(
                base_delay * (2**attempt), max_backoff
            )
            sleep_fn(delay)
            continue
        raise RadarFetchError(f"Non-retryable HTTP {resp.status} fetching {url}")

    raise RadarFetchError(f"Failed fetching {url}: {last_error}")


def parse_arxiv_atom(xml_bytes: bytes) -> list[PaperRecord]:
    """Parse arXiv Atom XML response into normalized PaperRecord list (fail-closed on bad XML)."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise RadarFetchError(f"Invalid arXiv Atom XML: {exc}") from exc

    expected_root = f"{{{_ATOM_NS['atom']}}}feed"
    if root.tag != expected_root:
        raise RadarFetchError(
            f"Unexpected arXiv response root tag {root.tag!r}; expected Atom <feed>"
        )

    records: list[PaperRecord] = []
    for entry in root.findall("atom:entry", _ATOM_NS):
        title_el = entry.find("atom:title", _ATOM_NS)
        title = " ".join((title_el.text or "").split()) if title_el is not None else ""
        id_el = entry.find("atom:id", _ATOM_NS)
        raw_url = (id_el.text or "").strip() if id_el is not None else ""
        summary_el = entry.find("atom:summary", _ATOM_NS)
        abstract = " ".join((summary_el.text or "").split()) if summary_el is not None else ""
        if "/api/errors" in raw_url.lower():
            detail = abstract or title or raw_url
            raise RadarFetchError(f"arXiv API returned error entry: {detail}")
        arxiv_id = normalize_arxiv_id(raw_url)
        if arxiv_id is None:
            detail = abstract or title or raw_url or "<missing id>"
            raise RadarFetchError(
                f"arXiv Atom entry has missing or invalid arXiv identifier {raw_url!r}: {detail}"
            )
        if not title:
            continue
        doi_el = entry.find("arxiv:doi", _ATOM_NS)
        doi = normalize_doi(doi_el.text if doi_el is not None else None)
        pub_el = entry.find("atom:published", _ATOM_NS)
        year: int | None = None
        if pub_el is not None and pub_el.text:
            m = re.match(r"^(\d{4})", pub_el.text.strip())
            if m:
                year = int(m.group(1))
        authors: list[str] = []
        for auth in entry.findall("atom:author", _ATOM_NS):
            name_el = auth.find("atom:name", _ATOM_NS)
            if name_el is not None and name_el.text and name_el.text.strip():
                authors.append(" ".join(name_el.text.split()))
        records.append(
            PaperRecord(
                title=title,
                authors=authors,
                year=year,
                arxiv_id=arxiv_id,
                doi=doi,
                venue="arXiv",
                abstract=abstract,
                url=raw_url,
                sources=["arxiv"],
            )
        )
    return records


def parse_semantic_scholar_json(payload_bytes: bytes) -> list[PaperRecord]:
    """Parse Semantic Scholar `/paper/search` JSON response (fail-closed on bad shape)."""
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RadarFetchError(f"Invalid Semantic Scholar JSON: {exc}") from exc
    if not isinstance(payload, dict) or "data" not in payload:
        raise RadarFetchError(
            "Semantic Scholar response must be a JSON object containing 'data'"
        )
    data = payload["data"]
    if not isinstance(data, list):
        raise RadarFetchError("Semantic Scholar response 'data' is not a list")

    records: list[PaperRecord] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        title = " ".join(str(item.get("title") or "").split())
        if not title:
            continue
        ext = item.get("externalIds") if isinstance(item.get("externalIds"), dict) else {}
        arxiv_id = normalize_arxiv_id(ext.get("ArXiv"))
        doi = normalize_doi(ext.get("DOI"))
        raw_year = item.get("year")
        year = (
            int(raw_year)
            if isinstance(raw_year, int) and not isinstance(raw_year, bool)
            else None
        )
        authors = [
            " ".join(str(a.get("name", "")).split())
            for a in (item.get("authors") or [])
            if isinstance(a, dict) and str(a.get("name", "")).strip()
        ]
        records.append(
            PaperRecord(
                title=title,
                authors=authors,
                year=year,
                arxiv_id=arxiv_id,
                doi=doi,
                venue=str(item.get("venue") or "").strip(),
                abstract=" ".join(str(item.get("abstract") or "").split()),
                url=str(item.get("url") or "").strip(),
                sources=["semantic_scholar"],
            )
        )
    return records


def parse_openalex_json(payload_bytes: bytes) -> list[PaperRecord]:
    """Parse OpenAlex `/works` JSON response (fail-closed on bad shape)."""
    try:
        payload = json.loads(payload_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RadarFetchError(f"Invalid OpenAlex JSON: {exc}") from exc
    if not isinstance(payload, dict) or "results" not in payload:
        raise RadarFetchError("OpenAlex response must be a JSON object containing 'results'")
    results = payload["results"]
    if not isinstance(results, list):
        raise RadarFetchError("OpenAlex response 'results' is not a list")

    records: list[PaperRecord] = []
    for item in results:
        if not isinstance(item, dict):
            continue
        title = " ".join(str(item.get("title") or "").split())
        if not title:
            continue
        ids = item.get("ids") if isinstance(item.get("ids"), dict) else {}
        doi = normalize_doi(item.get("doi") or ids.get("doi"))
        arxiv_id = normalize_arxiv_id(ids.get("arxiv"))
        raw_year = item.get("publication_year")
        year = (
            int(raw_year)
            if isinstance(raw_year, int) and not isinstance(raw_year, bool)
            else None
        )
        authors: list[str] = []
        for authorship in item.get("authorships") or []:
            if not isinstance(authorship, dict):
                continue
            auth = authorship.get("author")
            if isinstance(auth, dict) and str(auth.get("display_name", "")).strip():
                authors.append(" ".join(str(auth["display_name"]).split()))
        primary_loc = item.get("primary_location")
        venue = ""
        if isinstance(primary_loc, dict) and isinstance(primary_loc.get("source"), dict):
            venue = str(primary_loc["source"].get("display_name") or "").strip()
        abstract = reconstruct_openalex_abstract(item.get("abstract_inverted_index"))
        records.append(
            PaperRecord(
                title=title,
                authors=authors,
                year=year,
                arxiv_id=arxiv_id,
                doi=doi,
                venue=venue,
                abstract=abstract,
                url=str(item.get("id") or "").strip(),
                sources=["openalex"],
            )
        )
    return records


def search_arxiv(
    query: str,
    *,
    max_results: int = 10,
    timeout: float = 15.0,
    max_retries: int = 3,
    base_delay: float = 1.0,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> list[PaperRecord]:
    params = urllib.parse.urlencode(
        {"search_query": f"all:{query}", "start": 0, "max_results": max_results}
    )
    resp = fetch_with_backoff(
        f"{ARXIV_API_URL}?{params}",
        timeout=timeout,
        max_retries=max_retries,
        base_delay=base_delay,
        fetch_fn=fetch_fn,
        sleep_fn=sleep_fn,
    )
    return parse_arxiv_atom(resp.body)


def search_semantic_scholar(
    query: str,
    *,
    max_results: int = 10,
    timeout: float = 15.0,
    max_retries: int = 3,
    base_delay: float = 1.0,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> list[PaperRecord]:
    params = urllib.parse.urlencode(
        {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,year,venue,abstract,externalIds,url",
        }
    )
    resp = fetch_with_backoff(
        f"{SEMANTIC_SCHOLAR_API_URL}?{params}",
        timeout=timeout,
        max_retries=max_retries,
        base_delay=base_delay,
        fetch_fn=fetch_fn,
        sleep_fn=sleep_fn,
    )
    return parse_semantic_scholar_json(resp.body)


def search_openalex(
    query: str,
    *,
    max_results: int = 10,
    timeout: float = 15.0,
    max_retries: int = 3,
    base_delay: float = 1.0,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> list[PaperRecord]:
    params = urllib.parse.urlencode({"search": query, "per-page": max_results})
    resp = fetch_with_backoff(
        f"{OPENALEX_API_URL}?{params}",
        timeout=timeout,
        max_retries=max_retries,
        base_delay=base_delay,
        fetch_fn=fetch_fn,
        sleep_fn=sleep_fn,
    )
    return parse_openalex_json(resp.body)


def _merge_paper(dst: PaperRecord, src: PaperRecord) -> None:
    if not dst.arxiv_id and src.arxiv_id:
        dst.arxiv_id = src.arxiv_id
    if not dst.doi and src.doi:
        dst.doi = src.doi
    if not dst.year and src.year:
        dst.year = src.year
    if (not dst.venue or dst.venue == "arXiv") and src.venue and src.venue != "arXiv":
        dst.venue = src.venue
    if len(src.abstract) > len(dst.abstract):
        dst.abstract = src.abstract
    if len(src.authors) > len(dst.authors):
        dst.authors = list(src.authors)
    if not dst.url and src.url:
        dst.url = src.url
    for s in src.sources:
        if s not in dst.sources:
            dst.sources.append(s)


def deduplicate_records(records: Sequence[PaperRecord]) -> list[PaperRecord]:
    """Deduplicate papers via connected components on strong IDs + conflict-safe title merge.

    1. Union-find merges any two records sharing the same canonical arXiv ID or canonical DOI
       transitively (so a bridging record with both IDs collapses all matching groups into one).
    2. Title-only merging joins two components sharing the same normalized title ONLY when they
       do NOT carry conflicting known DOIs or conflicting known arXiv IDs.
    """
    n = len(records)
    if n == 0:
        return []

    norm_rec = [
        PaperRecord(
            title=r.title,
            authors=list(r.authors),
            year=r.year,
            arxiv_id=normalize_arxiv_id(r.arxiv_id),
            doi=normalize_doi(r.doi),
            venue=r.venue,
            abstract=r.abstract,
            url=r.url,
            sources=list(r.sources),
        )
        for r in records
    ]

    parent = list(range(n))

    def _find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def _union(a: int, b: int) -> int:
        ra, rb = _find(a), _find(b)
        if ra == rb:
            return ra
        if ra < rb:
            parent[rb] = ra
            return ra
        parent[ra] = rb
        return rb

    # Pass 1: transitive union over strong identifiers (arXiv ID and DOI)
    first_by_arxiv: dict[str, int] = {}
    first_by_doi: dict[str, int] = {}
    for idx, rec in enumerate(norm_rec):
        if rec.arxiv_id:
            if rec.arxiv_id in first_by_arxiv:
                _union(first_by_arxiv[rec.arxiv_id], idx)
            else:
                first_by_arxiv[rec.arxiv_id] = idx
        if rec.doi:
            if rec.doi in first_by_doi:
                _union(first_by_doi[rec.doi], idx)
            else:
                first_by_doi[rec.doi] = idx

    # Collect per-component strong IDs before title-based merge
    comp_arxivs: dict[int, set[str]] = collections.defaultdict(set)
    comp_dois: dict[int, set[str]] = collections.defaultdict(set)
    for idx, rec in enumerate(norm_rec):
        root = _find(idx)
        if rec.arxiv_id:
            comp_arxivs[root].add(rec.arxiv_id)
        if rec.doi:
            comp_dois[root].add(rec.doi)

    # Pass 2: title-based merge ONLY when components have no conflicting known DOI or arXiv ID
    roots_by_title: dict[str, list[int]] = collections.defaultdict(list)
    for idx, rec in enumerate(norm_rec):
        nt = normalize_title(rec.title)
        if not nt:
            continue
        root = _find(idx)
        merged_into: int | None = None
        for cand_raw in roots_by_title[nt]:
            cand = _find(cand_raw)
            if cand == root:
                merged_into = cand
                break
            combined_arx = comp_arxivs[cand] | comp_arxivs[root]
            combined_doi = comp_dois[cand] | comp_dois[root]
            if len(combined_arx) > 1 or len(combined_doi) > 1:
                continue
            new_root = _union(cand, root)
            comp_arxivs[new_root] = combined_arx
            comp_dois[new_root] = combined_doi
            merged_into = new_root
            break
        if merged_into is None:
            roots_by_title[nt].append(root)

    groups: dict[int, list[int]] = collections.defaultdict(list)
    for idx in range(n):
        groups[_find(idx)].append(idx)

    merged: list[PaperRecord] = []
    for root in sorted(groups.keys()):
        members = groups[root]
        acc = norm_rec[members[0]]
        for m_idx in members[1:]:
            _merge_paper(acc, norm_rec[m_idx])
        merged.append(acc)
    return merged


def search_all(
    query: str,
    *,
    sources: Sequence[str] = ("arxiv", "openalex", "semantic_scholar"),
    max_results: int = 10,
    timeout: float = 15.0,
    max_retries: int = 3,
    base_delay: float = 1.0,
    fetch_fn: FetchFn | None = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> list[PaperRecord]:
    """Query requested upstream APIs and return deduplicated PaperRecords."""
    collected: list[PaperRecord] = []
    dispatch = {
        "arxiv": search_arxiv,
        "semantic_scholar": search_semantic_scholar,
        "openalex": search_openalex,
    }
    for src in sources:
        if src not in dispatch:
            raise ValueError(f"Unsupported radar source: {src!r}")
        collected.extend(
            dispatch[src](
                query,
                max_results=max_results,
                timeout=timeout,
                max_retries=max_retries,
                base_delay=base_delay,
                fetch_fn=fetch_fn,
                sleep_fn=sleep_fn,
            )
        )
    return deduplicate_records(collected)


def load_catalog(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, Any]:
    return json.loads((repo_root / CATALOG_JSON_REL).read_text(encoding="utf-8"))


def build_literature_md(catalog: dict[str, Any], atlas: dict[str, Any]) -> str:
    """Render deterministic Russian literature overview (`research/literature/LITERATURE.md`)."""
    papers = catalog["papers"]
    atlas_by_id = {n["id"]: n for n in atlas["nodes"]}

    rel_counts: collections.Counter[str] = collections.Counter()
    papers_by_node: dict[str, list[tuple[str, str]]] = collections.defaultdict(list)
    for p in papers:
        for link in p.get("atlas_links", []):
            rel_counts[link["relation"]] += 1
            papers_by_node[link["node_id"]].append((p["id"], link["relation"]))

    total_links = sum(rel_counts.values())
    with_doi = sum(1 for p in papers if p.get("doi"))
    with_arxiv = sum(1 for p in papers if p.get("arxiv_id"))
    with_corpus = sum(1 for p in papers if p.get("corpus_path"))

    lines: list[str] = [
        "# Литературный радар и граф знаний — aro-discovery v2",
        "",
        "> Автоматически сгенерировано из [catalog.json](catalog.json) скриптом "
        "[radar.py](radar.py). Проверка целостности и связей с Атласом: "
        "`make verify-literature` ([verify_literature.py](verify_literature.py)).",
        "> Связанный Математический Атлас: [ATLAS.md](../atlas/ATLAS.md) | "
        "Проверка новизны: `python3 -m research.literature.novelty --conjecture <node_id>`.",
        "",
        "## 1. Сводка каталога",
        "",
        "| Метрика | Значение |",
        "|---|---|",
        f"| Всего индексированных работ | **{len(papers)}** |",
        f"| Привязано к физическим PDF в `corpus/` | **{with_corpus}** |",
        f"| С верифицированным DOI / arXiv ID | **{with_doi} DOI / {with_arxiv} arXiv** |",
        f"| Типизированных связей с Атласом | **{total_links}** ("
        + ", ".join(f"`{k}`={v}" for k, v in sorted(rel_counts.items()))
        + ") |",
        f"| Покрыто узлов `atlas.json` | **{len(papers_by_node)} из {len(atlas['nodes'])}** |",
        "",
        "## 2. Граф связей литературы с открытым фронтом Атласа (Mermaid)",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    open_ids = {n["id"] for n in atlas["nodes"] if n["status"] == "open"}
    shown_papers: set[str] = set()
    graph_edges: list[tuple[str, str, str]] = []
    for p in papers:
        for link in p.get("atlas_links", []):
            if link["node_id"] in open_ids:
                shown_papers.add(p["id"])
                graph_edges.append((p["id"], link["node_id"], link["relation"]))

    for pid in sorted(shown_papers):
        pm = "p_" + pid.replace("-", "_")
        lines.append(f'    {pm}["{pid}"]')
    for nid in sorted(open_ids):
        nm = "n_" + nid.replace("-", "_")
        lines.append(f'    {nm}["{nid} (OPEN)"]')
    for pid, nid, rel in graph_edges:
        pm = "p_" + pid.replace("-", "_")
        nm = "n_" + nid.replace("-", "_")
        lines.append(f"    {pm} -->|{rel}| {nm}")

    lines.extend(
        [
            "```",
            "",
            "## 3. Каталог ключевых работ",
            "",
            "| ID | Авторы и год | Название | Идентификаторы | Связи с Атласом |",
            "|---|---|---|---|---|",
        ]
    )
    for p in sorted(papers, key=lambda x: (x["year"], x["id"])):
        auth_short = ", ".join(p["authors"][:2]) + (" et al." if len(p["authors"]) > 2 else "")
        ids_parts: list[str] = []
        if p.get("doi"):
            ids_parts.append(f"DOI `{p['doi']}`")
        if p.get("arxiv_id"):
            ids_parts.append(f"arXiv `{p['arxiv_id']}`")
        if p.get("corpus_path"):
            ids_parts.append(f"`{p['corpus_path']}`")
        ids_str = "; ".join(ids_parts) if ids_parts else "—"
        links_str = ", ".join(
            f"`{lk['relation']}` → `{lk['node_id']}`"
            + (
                f" (p. {','.join(str(pg) for pg in lk['physical_pages'])})"
                if lk.get("physical_pages")
                else ""
            )
            for lk in p.get("atlas_links", [])
        )
        lines.append(
            f"| `{p['id']}` | {auth_short} ({p['year']}) | {p['title']} | "
            f"{ids_str} | {links_str} |"
        )

    lines.extend(["", "## 4. Покрытие открытых гипотез и целей обобщения Атласа", ""])
    for nid in sorted(open_ids):
        node = atlas_by_id[nid]
        linked = papers_by_node.get(nid, [])
        lines.append(f"### `{nid}` — {node['title_ru']}")
        lines.append("")
        if not linked:
            lines.append("- Связанных работ пока нет.")
        else:
            for pid, rel in sorted(linked):
                lines.append(f"- `{pid}` (`{rel}`)")
        lines.append("")

    return "\n".join(lines)


def write_literature_md(repo_root: pathlib.Path = REPO_ROOT) -> pathlib.Path:
    catalog = load_catalog(repo_root)
    atlas = json.loads((repo_root / ATLAS_JSON_REL).read_text(encoding="utf-8"))
    out = repo_root / LITERATURE_MD_REL
    out.write_text(build_literature_md(catalog, atlas), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Literature Radar (arXiv/S2/OpenAlex) and LITERATURE.md generator."
    )
    parser.add_argument("--build-md", action="store_true", help="Regenerate LITERATURE.md")
    parser.add_argument("--query", default=None, help="Run live search across selected APIs")
    parser.add_argument(
        "--sources",
        default="arxiv,openalex",
        help="Comma-separated sources: arxiv,openalex,semantic_scholar",
    )
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.build_md:
        path = write_literature_md(REPO_ROOT)
        print(f"GENERATED literature_md: {path.relative_to(REPO_ROOT)}")
        return 0

    if args.query:
        srcs = [s.strip() for s in args.sources.split(",") if s.strip()]
        try:
            records = search_all(args.query, sources=srcs, max_results=args.max_results)
        except (RadarFetchError, ValueError) as exc:
            print(f"RADAR ERROR: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps([r.to_dict() for r in records], ensure_ascii=False, indent=2))
        else:
            for r in records:
                print(f"- [{r.year or '?'}] {r.title} ({', '.join(r.sources)})")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
