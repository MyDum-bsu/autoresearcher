#!/usr/bin/env python3
"""Semantic Index for the Mathematical Atlas (`research/atlas/atlas.json`) with Vertex Embeddings.

Supports two backends:
  1. `offline_tfidf` (default): 100% offline, deterministic word + character n-gram TF-IDF
     cosine similarity index with zero external dependencies or network calls.
  2. `vertex` (explicit `--live` flag required): calls Google Cloud Vertex AI Embeddings API
     (`text-embedding-005` or `gemini-embedding-001`) using Application Default Credentials
     (`gcloud auth application-default print-access-token` or `VERTEX_ACCESS_TOKEN`), with an
     explicit hard USD budget ceiling (`--max-usd`, default $0.05) and persistent JSON cache
     keyed by `atlas_sha256 + backend + model`.

CLI:
  python3 -m research.atlas.semantic_index build [--live --model text-embedding-005 --max-usd 0.05]
  python3 -m research.atlas.semantic_index search --query "..." --top-k 5
  python3 -m research.atlas.semantic_index check-duplicate --title "..." --statement "..."
"""

from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
ATLAS_JSON_DEFAULT = REPO_ROOT / "research" / "atlas" / "atlas.json"
DEFAULT_CACHE_PATH = REPO_ROOT / "tmp" / "atlas-semantic-index.json"

VERTEX_MODELS: tuple[str, ...] = ("text-embedding-005", "gemini-embedding-001")
# Official Vertex AI Text Embeddings API per-request instance limits.
VERTEX_MAX_BATCH_SIZE: dict[str, int] = {
    "text-embedding-005": 5,
    "gemini-embedding-001": 1,
}
# Conservative USD per 1,000 characters/units estimate for Vertex AI text embeddings.
VERTEX_USD_PER_1K_CHARS: dict[str, float] = {
    "text-embedding-005": 0.000025,
    "gemini-embedding-001": 0.00015,
}

_TOKEN_RE = re.compile(r"[a-z0-9_]+")
_STOPWORDS: frozenset[str] = frozenset(
    {
        "the",
        "and",
        "for",
        "with",
        "that",
        "this",
        "from",
        "into",
        "over",
        "under",
        "are",
        "was",
        "were",
        "been",
        "has",
        "have",
        "not",
        "but",
        "can",
        "all",
        "any",
        "its",
        "their",
        "when",
        "where",
        "which",
        "whose",
        "such",
        "also",
        "only",
        "each",
        "than",
        "then",
        "both",
        "via",
    }
)


class SemanticIndexError(RuntimeError):
    """Raised on semantic index configuration, cache, or backend errors."""


class SemanticBudgetError(SemanticIndexError):
    """Raised when estimated Vertex AI embedding spend exceeds `--max-usd`."""


def _sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _node_document_text(node: dict[str, Any]) -> str:
    """Build canonical English+structural text representation for an Atlas node."""
    parts = [
        str(node.get("id", "")),
        str(node.get("kind", "")),
        str(node.get("domain", "")),
        str(node.get("status", "")),
        str(node.get("title_en", "")),
        str(node.get("statement_en", "")),
    ]
    fscope = node.get("formalized_scope")
    if isinstance(fscope, dict):
        parts.append(str(fscope.get("proved_in_lean", "")))
        parts.append(str(fscope.get("not_proved_in_lean", "")))
    return "\n".join(p.strip() for p in parts if p and p.strip())


def _tokenize(text: str) -> list[str]:
    """Deterministic word + bigram tokenizer for mathematical English text."""
    lower = text.lower()
    raw_tokens = [t for t in _TOKEN_RE.findall(lower) if len(t) >= 2 and t not in _STOPWORDS]
    bigrams = [f"{raw_tokens[i]}_{raw_tokens[i + 1]}" for i in range(len(raw_tokens) - 1)]
    return raw_tokens + bigrams


def estimate_vertex_usd(texts: list[str], model: str) -> float:
    """Estimate exact unrounded Vertex AI Embeddings cost in USD from total character count."""
    if model not in VERTEX_USD_PER_1K_CHARS:
        raise SemanticIndexError(f"Unsupported Vertex embedding model: {model!r}")
    total_chars = sum(len(t) for t in texts)
    rate = VERTEX_USD_PER_1K_CHARS[model]
    return (total_chars / 1000.0) * rate


def _get_adc_access_token() -> str:
    env_tok = os.environ.get("VERTEX_ACCESS_TOKEN", "").strip()
    if env_tok:
        return env_tok
    proc = subprocess.run(
        ["gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        raise SemanticIndexError(
            "Unable to obtain ADC access token via "
            "`gcloud auth application-default print-access-token`"
        )
    return proc.stdout.strip()


def _resolve_gcp_project(explicit_project: str | None = None) -> str:
    if explicit_project and explicit_project.strip():
        return explicit_project.strip()
    for env_key in ("GOOGLE_CLOUD_PROJECT", "GCLOUD_PROJECT", "VERTEX_PROJECT"):
        val = os.environ.get(env_key, "").strip()
        if val:
            return val
    proc = subprocess.run(
        ["gcloud", "config", "get-value", "project"],
        capture_output=True,
        text=True,
        check=False,
    )
    proj = proc.stdout.strip()
    if proc.returncode != 0 or not proj or proj == "(unset)":
        raise SemanticIndexError(
            "Unable to resolve GCP project; pass --project or set GOOGLE_CLOUD_PROJECT"
        )
    return proj


def _call_vertex_embeddings(
    texts: list[str],
    *,
    model: str,
    project: str,
    location: str,
    max_usd: float,
    task_type: str = "RETRIEVAL_DOCUMENT",
    http_requester: Any = None,
) -> list[list[float]]:
    """Call Vertex AI predict endpoint for embeddings with strict USD budget guard."""
    if model not in VERTEX_MODELS:
        raise SemanticIndexError(f"Unsupported Vertex model {model!r}; expected {VERTEX_MODELS}")
    if (
        not isinstance(max_usd, (int, float))
        or isinstance(max_usd, bool)
        or not math.isfinite(max_usd)
        or max_usd <= 0
    ):
        raise SemanticBudgetError(f"max_usd must be finite and > 0, got {max_usd!r}")
    est_usd = estimate_vertex_usd(texts, model)
    if est_usd > max_usd:
        raise SemanticBudgetError(
            f"Estimated Vertex Embeddings cost (${est_usd:.6f}) exceeds --max-usd (${max_usd:.6f})"
        )

    url = (
        f"https://{location}-aiplatform.googleapis.com/v1/projects/{project}"
        f"/locations/{location}/publishers/google/models/{model}:predict"
    )
    vectors: list[list[float]] = []
    batch_size = VERTEX_MAX_BATCH_SIZE[model]

    if http_requester is not None:
        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            body = {
                "instances": [{"content": t, "task_type": task_type} for t in batch],
            }
            resp = http_requester(url, body)
            preds = resp.get("predictions", [])
            if len(preds) != len(batch):
                raise SemanticIndexError(
                    f"Vertex response prediction count mismatch: {len(preds)} != {len(batch)}"
                )
            for p in preds:
                vals = p["embeddings"]["values"]
                vectors.append([float(x) for x in vals])
        return vectors

    token = _get_adc_access_token()
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        payload = json.dumps(
            {"instances": [{"content": t, "task_type": task_type} for t in batch]}
        ).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise SemanticIndexError(f"Vertex AI Embeddings HTTP error: {exc}") from exc

        preds = data.get("predictions", [])
        if len(preds) != len(batch):
            raise SemanticIndexError(
                f"Vertex response prediction count mismatch: {len(preds)} != {len(batch)}"
            )
        for p in preds:
            vals = p["embeddings"]["values"]
            vectors.append([float(x) for x in vals])
    return vectors


def _cosine_dense(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def _cosine_sparse(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    dot = sum(v * b[k] for k, v in a.items() if k in b)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


@dataclasses.dataclass(frozen=True)
class SearchMatch:
    node_id: str
    kind: str
    status: str
    domain: str
    title_en: str
    score: float

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class SemanticAtlasIndex:
    """Offline-first / Vertex-capable semantic index over `research/atlas/atlas.json`."""

    def __init__(
        self,
        *,
        atlas_path: pathlib.Path = ATLAS_JSON_DEFAULT,
        backend: str = "offline_tfidf",
        model: str = "text-embedding-005",
        cache_path: pathlib.Path | None = None,
        project: str | None = None,
        location: str = "us-central1",
        max_usd: float = 0.05,
        http_requester: Any = None,
    ) -> None:
        if backend not in {"offline_tfidf", "vertex"}:
            raise SemanticIndexError(f"Unsupported backend {backend!r}")
        if backend == "vertex" and model not in VERTEX_MODELS:
            raise SemanticIndexError(f"Unsupported Vertex model {model!r}")
        self.atlas_path = atlas_path.resolve()
        if not self.atlas_path.is_file():
            raise SemanticIndexError(f"Atlas JSON not found: {self.atlas_path}")
        self.backend = backend
        self.model = model if backend == "vertex" else "tfidf-word-bigram-v1"
        self.cache_path = cache_path.resolve() if cache_path else None
        self.project = project
        self.location = location
        if (
            not isinstance(max_usd, (int, float))
            or isinstance(max_usd, bool)
            or not math.isfinite(max_usd)
            or max_usd <= 0
        ):
            raise SemanticBudgetError(f"max_usd must be finite and > 0, got {max_usd!r}")
        self.max_usd = float(max_usd)
        self.http_requester = http_requester

        self.atlas_sha256 = _sha256_file(self.atlas_path)
        self.nodes: list[dict[str, Any]] = []
        self.idf: dict[str, float] = {}
        self.sparse_vectors: dict[str, dict[str, float]] = {}
        self.dense_vectors: dict[str, list[float]] = {}
        self.cache_hit: bool = False
        self.estimated_usd: float = 0.0
        self.spent_chars: int = 0
        self.spent_usd: float = 0.0
        self._load_or_build()

    def _load_or_build(self) -> None:
        raw_atlas = json.loads(self.atlas_path.read_text(encoding="utf-8"))
        nodes = raw_atlas.get("nodes", [])
        if not isinstance(nodes, list) or not nodes:
            raise SemanticIndexError("Atlas JSON contains no nodes")
        self.nodes = nodes

        if self.cache_path and self.cache_path.is_file():
            try:
                cached = json.loads(self.cache_path.read_text(encoding="utf-8"))
                if (
                    cached.get("schema_version") == 1
                    and cached.get("atlas_sha256") == self.atlas_sha256
                    and cached.get("backend") == self.backend
                    and cached.get("model") == self.model
                ):
                    if self.backend == "offline_tfidf":
                        self.idf = {str(k): float(v) for k, v in cached["idf"].items()}
                        self.sparse_vectors = {
                            str(nid): {str(k): float(v) for k, v in vec.items()}
                            for nid, vec in cached["sparse_vectors"].items()
                        }
                    else:
                        self.dense_vectors = {
                            str(nid): [float(x) for x in vec]
                            for nid, vec in cached["dense_vectors"].items()
                        }
                    self.cache_hit = True
                    self.estimated_usd = 0.0
                    return
            except (OSError, KeyError, ValueError, TypeError):
                # Corrupt/incompatible cache: rebuild cleanly
                pass

        docs = [_node_document_text(n) for n in self.nodes]
        if self.backend == "offline_tfidf":
            self._build_tfidf(docs)
        else:
            proj = (
                self.project
                if self.http_requester is not None and self.project
                else _resolve_gcp_project(self.project)
            )
            doc_chars = sum(len(d) for d in docs)
            rate = VERTEX_USD_PER_1K_CHARS[self.model]
            projected_total = ((self.spent_chars + doc_chars) / 1000.0) * rate
            if projected_total > self.max_usd:
                raise SemanticBudgetError(
                    f"Cumulative Vertex Embeddings cost (${projected_total:.8f}) "
                    f"exceeds --max-usd (${self.max_usd:.8f})"
                )
            self.estimated_usd = round((doc_chars / 1000.0) * rate, 6)
            remaining = self.max_usd - (self.spent_chars / 1000.0) * rate
            # Charge characters BEFORE the outbound request so failed/malformed responses
            # still count against cumulative budget and cannot bypass --max-usd on retry.
            self.spent_chars += doc_chars
            self.spent_usd = (self.spent_chars / 1000.0) * rate
            vecs = _call_vertex_embeddings(
                docs,
                model=self.model,
                project=proj,
                location=self.location,
                max_usd=remaining,
                task_type="RETRIEVAL_DOCUMENT",
                http_requester=self.http_requester,
            )
            self.dense_vectors = {str(n["id"]): v for n, v in zip(self.nodes, vecs, strict=True)}

        if self.cache_path:
            self._save_cache()

    def _build_tfidf(self, docs: list[str]) -> None:
        n_docs = len(docs)
        tokenized = [_tokenize(d) for d in docs]
        df: collections.Counter[str] = collections.Counter()
        for toks in tokenized:
            for tok in set(toks):
                df[tok] += 1
        self.idf = {tok: math.log((1.0 + n_docs) / (1.0 + freq)) + 1.0 for tok, freq in df.items()}
        self.sparse_vectors = {}
        for node, toks in zip(self.nodes, tokenized, strict=True):
            self.sparse_vectors[str(node["id"])] = self._tfidf_vector(toks)

    def _tfidf_vector(self, tokens: list[str]) -> dict[str, float]:
        if not tokens:
            return {}
        tf = collections.Counter(tokens)
        total = float(len(tokens))
        vec: dict[str, float] = {}
        for tok, cnt in tf.items():
            idf_val = self.idf.get(tok, 1.0)
            vec[tok] = (cnt / total) * idf_val
        return vec

    def _save_cache(self) -> None:
        if not self.cache_path:
            return
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {
            "schema_version": 1,
            "atlas_sha256": self.atlas_sha256,
            "backend": self.backend,
            "model": self.model,
            "node_count": len(self.nodes),
            "built_at_utc": dt.datetime.now(dt.UTC).isoformat(timespec="seconds"),
        }
        if self.backend == "offline_tfidf":
            payload["idf"] = self.idf
            payload["sparse_vectors"] = self.sparse_vectors
        else:
            payload["dense_vectors"] = self.dense_vectors
        self.cache_path.write_text(
            json.dumps(payload, sort_keys=True, ensure_ascii=False), encoding="utf-8"
        )

    def metadata(self) -> dict[str, Any]:
        return {
            "atlas_sha256": self.atlas_sha256,
            "backend": self.backend,
            "model": self.model,
            "node_count": len(self.nodes),
            "cache_hit": self.cache_hit,
            "estimated_usd": self.estimated_usd,
        }

    def search(
        self,
        query: str,
        *,
        top_k: int = 5,
        kind: str | None = None,
        status: str | None = None,
    ) -> list[SearchMatch]:
        """Return top-k Atlas nodes ranked by cosine similarity to `query`."""
        if not query or not query.strip():
            raise SemanticIndexError("Search query must be non-empty")
        if top_k <= 0:
            raise SemanticIndexError(f"top_k must be > 0, got {top_k}")

        if self.backend == "offline_tfidf":
            q_vec_sparse = self._tfidf_vector(_tokenize(query))
            q_vec_dense: list[float] | None = None
        else:
            proj = (
                self.project
                if self.http_requester is not None and self.project
                else _resolve_gcp_project(self.project)
            )
            q_chars = len(query)
            rate = VERTEX_USD_PER_1K_CHARS[self.model]
            projected_total = ((self.spent_chars + q_chars) / 1000.0) * rate
            if projected_total > self.max_usd:
                raise SemanticBudgetError(
                    f"Cumulative Vertex Embeddings cost (${projected_total:.8f}) "
                    f"exceeds --max-usd (${self.max_usd:.8f})"
                )
            remaining = self.max_usd - (self.spent_chars / 1000.0) * rate
            self.spent_chars += q_chars
            self.spent_usd = (self.spent_chars / 1000.0) * rate
            q_vec_dense = _call_vertex_embeddings(
                [query],
                model=self.model,
                project=proj,
                location=self.location,
                max_usd=remaining,
                task_type="RETRIEVAL_QUERY",
                http_requester=self.http_requester,
            )[0]
            q_vec_sparse = {}

        matches: list[SearchMatch] = []
        for node in self.nodes:
            if kind and node.get("kind") != kind:
                continue
            if status and node.get("status") != status:
                continue
            nid = str(node["id"])
            if self.backend == "offline_tfidf":
                score = _cosine_sparse(q_vec_sparse, self.sparse_vectors.get(nid, {}))
            else:
                if q_vec_dense is None:
                    raise SemanticIndexError("Dense query vector missing for vertex backend")
                score = _cosine_dense(q_vec_dense, self.dense_vectors.get(nid, []))
            matches.append(
                SearchMatch(
                    node_id=nid,
                    kind=str(node.get("kind", "")),
                    status=str(node.get("status", "")),
                    domain=str(node.get("domain", "")),
                    title_en=str(node.get("title_en", "")),
                    score=round(float(score), 4),
                )
            )

        matches.sort(key=lambda m: (-m.score, m.node_id))
        return matches[:top_k]

    def check_duplicate(
        self,
        title: str,
        statement: str,
        *,
        threshold: float = 0.78,
        top_k: int = 5,
        status_filter: str | None = None,
    ) -> dict[str, Any]:
        """Classify whether a candidate hypothesis duplicates an existing Atlas node."""
        combined = f"{title.strip()}\n{statement.strip()}".strip()
        matches = self.search(combined, top_k=top_k, status=status_filter)
        top_score = matches[0].score if matches else 0.0
        if top_score >= threshold:
            risk = "HIGH_DUPLICATE_RISK"
            is_dup = True
        elif top_score >= max(0.45, threshold - 0.23):
            risk = "MODERATE_OVERLAP"
            is_dup = False
        else:
            risk = "NOVEL_CANDIDATE"
            is_dup = False
        return {
            "is_duplicate": is_dup,
            "duplicate_risk": risk,
            "threshold": threshold,
            "top_score": top_score,
            "top_match": matches[0].to_dict() if matches else None,
            "matches": [m.to_dict() for m in matches],
            "backend": self.backend,
            "model": self.model,
            "atlas_sha256": self.atlas_sha256,
        }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python3 -m research.atlas.semantic_index",
        description=(
            "Semantic index over research/atlas/atlas.json "
            "(offline TF-IDF default; --live for Vertex Embeddings)."
        ),
    )
    p.add_argument("--atlas", default=str(ATLAS_JSON_DEFAULT), help="Path to atlas.json.")
    p.add_argument("--cache", default=str(DEFAULT_CACHE_PATH), help="Path to index cache JSON.")
    p.add_argument(
        "--live",
        action="store_true",
        default=False,
        help="Use live Vertex AI Embeddings via ADC (default: offline TF-IDF).",
    )
    p.add_argument(
        "--model",
        choices=VERTEX_MODELS,
        default="text-embedding-005",
        help="Vertex AI embedding model when --live is set.",
    )
    p.add_argument("--project", default=None, help="GCP project ID (default: gcloud config).")
    p.add_argument("--location", default="us-central1", help="Vertex AI region.")
    p.add_argument("--max-usd", type=float, default=0.05, help="Hard USD budget cap for --live.")

    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("build", help="Build or load cached Atlas semantic index.")

    p_search = sub.add_parser("search", help="Search similar Atlas nodes.")
    p_search.add_argument("--query", required=True, help="Search query text.")
    p_search.add_argument("--top-k", type=int, default=5, help="Number of results.")
    p_search.add_argument("--kind", default=None, help="Filter by node kind.")
    p_search.add_argument("--status", default=None, help="Filter by node status.")

    p_dup = sub.add_parser(
        "check-duplicate", help="Check candidate hypothesis for Atlas duplication."
    )
    p_dup.add_argument("--title", required=True, help="Candidate title.")
    p_dup.add_argument("--statement", required=True, help="Candidate mathematical statement.")
    p_dup.add_argument("--threshold", type=float, default=0.78, help="Duplicate cosine threshold.")
    p_dup.add_argument("--top-k", type=int, default=5, help="Number of similar nodes to return.")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        idx = SemanticAtlasIndex(
            atlas_path=pathlib.Path(args.atlas),
            backend="vertex" if args.live else "offline_tfidf",
            model=args.model,
            cache_path=pathlib.Path(args.cache) if args.cache else None,
            project=args.project,
            location=args.location,
            max_usd=args.max_usd,
        )
        if args.command == "build":
            out: dict[str, Any] = {"status": "ok", **idx.metadata()}
        elif args.command == "search":
            matches = idx.search(args.query, top_k=args.top_k, kind=args.kind, status=args.status)
            out = {
                "status": "ok",
                **idx.metadata(),
                "query": args.query,
                "results": [m.to_dict() for m in matches],
            }
        else:
            out = idx.check_duplicate(
                args.title,
                args.statement,
                threshold=args.threshold,
                top_k=args.top_k,
            )
    except (SemanticIndexError, OSError, ValueError) as exc:
        print(f"SEMANTIC INDEX ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
