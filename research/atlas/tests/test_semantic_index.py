"""Offline & mocked-Vertex unit tests for research.atlas.semantic_index (#1714)."""

from __future__ import annotations

import hashlib
import json
import pathlib
from typing import Any

import pytest

from research.atlas.semantic_index import (
    ATLAS_JSON_DEFAULT,
    VERTEX_MAX_BATCH_SIZE,
    SemanticAtlasIndex,
    SemanticBudgetError,
    SemanticIndexError,
    estimate_vertex_usd,
    main,
)


def test_offline_tfidf_search_finds_o4_and_caches(tmp_path: pathlib.Path) -> None:
    cache_file = tmp_path / "atlas-index.json"
    idx1 = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="offline_tfidf",
        cache_path=cache_file,
    )
    assert idx1.cache_hit is False
    assert cache_file.is_file()
    matches = idx1.search("strict value of measurement closure schedule selection R", top_k=3)
    assert matches
    assert matches[0].node_id in {"conj-o4-closure-scheduling", "thm-o4-single-closure-value"}

    idx2 = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="offline_tfidf",
        cache_path=cache_file,
    )
    assert idx2.cache_hit is True


def test_duplicate_detection_flags_exact_atlas_copy() -> None:
    raw = json.loads(ATLAS_JSON_DEFAULT.read_text(encoding="utf-8"))
    node = next(n for n in raw["nodes"] if n["id"] == "thm-f1-expansion")
    idx = SemanticAtlasIndex(atlas_path=ATLAS_JSON_DEFAULT, backend="offline_tfidf")
    res = idx.check_duplicate(node["title_en"], node["statement_en"], threshold=0.5)
    assert res["is_duplicate"] is True
    assert res["duplicate_risk"] == "HIGH_DUPLICATE_RISK"
    assert res["top_match"]["node_id"] == "thm-f1-expansion"


def test_mocked_vertex_backend_respects_batch_limits_and_caches(tmp_path: pathlib.Path) -> None:
    batch_sizes: list[int] = []

    def fake_vertex_http(_url: str, body: dict[str, Any]) -> dict[str, Any]:
        insts = body["instances"]
        batch_sizes.append(len(insts))
        preds = []
        for item in insts:
            h = hashlib.sha256(item["content"].encode("utf-8")).digest()
            vec = [float(b) / 255.0 for b in h[:8]]
            preds.append({"embeddings": {"values": vec}})
        return {"predictions": preds}

    cache_file = tmp_path / "vertex-index.json"
    idx = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        cache_path=cache_file,
        max_usd=0.05,
        http_requester=fake_vertex_http,
    )
    assert idx.cache_hit is False
    assert sum(batch_sizes) == len(idx.nodes)
    assert max(batch_sizes) <= VERTEX_MAX_BATCH_SIZE["text-embedding-005"]
    assert idx.estimated_usd > 0.0 and idx.estimated_usd < 0.01

    # Reload from cache without calling Vertex again
    calls_before = len(batch_sizes)
    idx_cached = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        cache_path=cache_file,
        max_usd=0.05,
        http_requester=fake_vertex_http,
    )
    assert idx_cached.cache_hit is True
    assert len(batch_sizes) == calls_before

    # Search uses 1 query call
    matches = idx_cached.search("conic Minkowski support tightening", top_k=3)
    assert len(matches) == 3
    assert len(batch_sizes) == calls_before + 1


def test_gemini_embedding_model_respects_batch_size_one(tmp_path: pathlib.Path) -> None:
    seen_sizes: list[int] = []

    def fake_http(_url: str, body: dict[str, Any]) -> dict[str, Any]:
        insts = body["instances"]
        seen_sizes.append(len(insts))
        return {"predictions": [{"embeddings": {"values": [0.1, 0.2, 0.3]}} for _ in insts]}

    idx = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="gemini-embedding-001",
        project="test-proj",
        cache_path=tmp_path / "gem-idx.json",
        max_usd=0.05,
        http_requester=fake_http,
    )
    assert len(seen_sizes) == len(idx.nodes)
    assert all(sz == 1 for sz in seen_sizes)


def test_vertex_budget_guard_rejects_nan_inf_and_cumulative_overspend() -> None:
    assert estimate_vertex_usd(["a" * 10000], "text-embedding-005") > 0.0
    for bad_usd in (0.0, -0.01, float("nan"), float("inf")):
        with pytest.raises(SemanticBudgetError):
            SemanticAtlasIndex(
                atlas_path=ATLAS_JSON_DEFAULT,
                backend="vertex",
                model="text-embedding-005",
                project="test-proj",
                max_usd=bad_usd,
                http_requester=lambda _u, _b: {"predictions": []},
            )

    def fake_http(_url: str, body: dict[str, Any]) -> dict[str, Any]:
        return {"predictions": [{"embeddings": {"values": [1.0, 0.0]}} for _ in body["instances"]]}

    # Build uses ~$0.000471; set max_usd to exactly allow build, then a huge query must fail
    idx = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        max_usd=0.0005,
        http_requester=fake_http,
    )
    with pytest.raises(SemanticBudgetError):
        idx.search("closure " * 5000, top_k=3)


def test_short_queries_accumulate_exact_chars_and_cannot_bypass_max_usd(
    tmp_path: pathlib.Path,
) -> None:
    def fake_http(_url: str, body: dict[str, Any]) -> dict[str, Any]:
        return {"predictions": [{"embeddings": {"values": [1.0, 0.0]}} for _ in body["instances"]]}

    cache_file = tmp_path / "cached-short.json"
    # Build cache once with generous budget
    SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        cache_path=cache_file,
        max_usd=0.05,
        http_requester=fake_http,
    )
    # Reload from cache with tiny budget: 1000 * 7 chars = 7000 chars -> $0.000175 > $0.00001
    idx = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        cache_path=cache_file,
        max_usd=0.00001,
        http_requester=fake_http,
    )
    with pytest.raises(SemanticBudgetError):
        for _ in range(100):
            idx.search("closure", top_k=1)


def test_failed_vertex_query_still_charges_budget_and_gemini_rate_is_0_00015(
    tmp_path: pathlib.Path,
) -> None:
    assert estimate_vertex_usd(["a" * 1000], "gemini-embedding-001") == pytest.approx(0.00015)

    calls = 0

    def bad_on_query(_url: str, body: dict[str, Any]) -> dict[str, Any]:
        nonlocal calls
        calls += 1
        # Return valid embeddings for build, malformed empty predictions for query
        if body["instances"][0]["task_type"] == "RETRIEVAL_DOCUMENT":
            return {
                "predictions": [{"embeddings": {"values": [1.0, 0.0]}} for _ in body["instances"]]
            }
        return {"predictions": []}

    idx = SemanticAtlasIndex(
        atlas_path=ATLAS_JSON_DEFAULT,
        backend="vertex",
        model="text-embedding-005",
        project="test-proj",
        cache_path=tmp_path / "fail-charge.json",
        max_usd=0.000491,
        http_requester=bad_on_query,
    )
    # First query fails on response parsing, but its chars MUST already be charged
    with pytest.raises(SemanticIndexError):
        idx.search("a" * 600, top_k=1)
    # Second 600-char query pushes total above $0.000491 -> MUST fail with SemanticBudgetError
    with pytest.raises(SemanticBudgetError):
        idx.search("a" * 600, top_k=1)


def test_cli_offline_build_and_search(tmp_path: pathlib.Path) -> None:
    cache_file = tmp_path / "cli-idx.json"
    assert main(["--cache", str(cache_file), "build"]) == 0
    assert main(["--cache", str(cache_file), "search", "--query", "minimax maximin gap"]) == 0
