"""100% offline unit tests for research/literature/{radar,novelty,verify_literature}.py.

Zero live network calls: all arXiv, Semantic Scholar, and OpenAlex HTTP interactions are
exercised through deterministic in-memory mock transports and injectable sleep hooks.
"""

from __future__ import annotations

import json
import unittest

from research.literature.novelty import NoveltyCheckError, check_conjecture
from research.literature.radar import (
    HttpResponse,
    PaperRecord,
    RadarFetchError,
    deduplicate_records,
    fetch_with_backoff,
    normalize_arxiv_id,
    normalize_doi,
    normalize_title,
    parse_arxiv_atom,
    parse_openalex_json,
    parse_semantic_scholar_json,
    reconstruct_openalex_abstract,
    search_all,
)

_SAMPLE_ARXIV_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2409.12630v3</id>
    <published>2025-01-15T12:00:00Z</published>
    <title>Bounding the Optimal Number of Policies for Robust K-Adaptability</title>
    <summary>We prove tight upper bounds on K-adaptability policies.</summary>
    <author><name>Jannis Kurtz</name></author>
    <arxiv:doi>10.1234/kadapt.2025</arxiv:doi>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2501.99999v1</id>
    <published>2025-02-01T00:00:00Z</published>
    <title>Multistage Closure Schedules in Linear Guaranteed Control</title>
    <summary>New closure scheduling bounds via parametric linear programming.</summary>
    <author><name>A. Researcher</name></author>
  </entry>
</feed>
"""

_SAMPLE_OPENALEX_JSON = json.dumps(
    {
        "results": [
            {
                "id": "https://openalex.org/W123456",
                "doi": "https://doi.org/10.1234/KADAPT.2025",
                "title": "Bounding the Optimal Number of Policies for Robust K-Adaptability",
                "publication_year": 2025,
                "authorships": [{"author": {"display_name": "Jannis Kurtz"}}],
                "primary_location": {"source": {"display_name": "Mathematical Programming"}},
                "abstract_inverted_index": {
                    "Exact": [0],
                    "bounds": [1, 4],
                    "on": [2],
                    "K-adaptability": [3],
                    "in": [5],
                    "ARO.": [6],
                },
            }
        ]
    }
).encode("utf-8")

_SAMPLE_S2_JSON = json.dumps(
    {
        "data": [
            {
                "paperId": "s2-abc",
                "title": "Exact Copositive Characterization of Affine Rules in ARO",
                "year": 2025,
                "venue": "Operations Research",
                "abstract": "Copositive and inner conic conditions for ADR exactness.",
                "authors": [{"name": "B. Author"}, {"name": "C. Coauthor"}],
                "externalIds": {"DOI": "10.9999/copositive.2025", "ArXiv": "2502.11111"},
                "url": "https://www.semanticscholar.org/paper/s2-abc",
            }
        ]
    }
).encode("utf-8")


class TestNormalizationAndParsers(unittest.TestCase):
    def test_normalization_helpers(self) -> None:
        self.assertEqual(normalize_arxiv_id("https://arxiv.org/abs/2409.12630v3"), "2409.12630")
        self.assertEqual(normalize_arxiv_id("arXiv:1801.06751v1"), "1801.06751")
        self.assertEqual(normalize_arxiv_id("http://arxiv.org/abs/math/0601234v2"), "math/0601234")
        self.assertEqual(normalize_arxiv_id("math.OC/0601234v1"), "math.oc/0601234")
        self.assertIsNone(normalize_arxiv_id("http://arxiv.org/api/errors#incorrect_id_format"))
        self.assertIsNone(normalize_arxiv_id("not-an-arxiv-id"))
        with self.assertRaises(ValueError):
            PaperRecord(
                title="Bogus",
                authors=["X"],
                year=2025,
                arxiv_id="http://arxiv.org/api/errors#incorrect_id_format",
            )
        self.assertEqual(
            normalize_doi("https://doi.org/10.1007/S10107-003-0454-Y."),
            "10.1007/s10107-003-0454-y",
        )
        self.assertEqual(
            normalize_title("Adjustable Robust Solutions: A Survey!"),
            "adjustable robust solutions a survey",
        )

    def test_parse_arxiv_openalex_and_s2_fixtures(self) -> None:
        arx = parse_arxiv_atom(_SAMPLE_ARXIV_XML)
        self.assertEqual(len(arx), 2)
        self.assertEqual(arx[0].arxiv_id, "2409.12630")
        self.assertEqual(arx[0].doi, "10.1234/kadapt.2025")
        self.assertEqual(arx[0].year, 2025)

        oa = parse_openalex_json(_SAMPLE_OPENALEX_JSON)
        self.assertEqual(len(oa), 1)
        self.assertEqual(oa[0].doi, "10.1234/kadapt.2025")
        self.assertEqual(oa[0].venue, "Mathematical Programming")
        self.assertEqual(oa[0].abstract, "Exact bounds on K-adaptability bounds in ARO.")
        self.assertEqual(reconstruct_openalex_abstract(None), "")

        s2 = parse_semantic_scholar_json(_SAMPLE_S2_JSON)
        self.assertEqual(len(s2), 1)
        self.assertEqual(s2[0].arxiv_id, "2502.11111")
        self.assertEqual(s2[0].authors, ["B. Author", "C. Coauthor"])

    def test_parsers_fail_closed_on_malformed_upstream_payloads(self) -> None:
        # HTML error page instead of Atom XML feed
        with self.assertRaises(RadarFetchError):
            parse_arxiv_atom(b"<html><body>Rate limit exceeded</body></html>")
        # OpenAlex missing `results` key or non-dict JSON list
        with self.assertRaises(RadarFetchError):
            parse_openalex_json(b"{}")
        with self.assertRaises(RadarFetchError):
            parse_openalex_json(b"[]")
        # Semantic Scholar non-dict JSON list or missing `data` key
        with self.assertRaises(RadarFetchError):
            parse_semantic_scholar_json(b"[]")
        with self.assertRaises(RadarFetchError):
            parse_semantic_scholar_json(b"{}")

    def test_arxiv_atom_error_entry_fails_closed_and_empty_feed_ok(self) -> None:
        error_atom = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/api/errors#incorrect_id_format</id>
    <title>Error</title>
    <summary>incorrect id format for bad-id</summary>
  </entry>
</feed>
"""
        with self.assertRaises(RadarFetchError) as ctx:
            parse_arxiv_atom(error_atom)
        self.assertIn("incorrect id format", str(ctx.exception))

        # Entry missing <id> or with empty <id/> MUST fail closed
        missing_id_atom = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry><title>Some title without id</title></entry>
</feed>
"""
        with self.assertRaises(RadarFetchError):
            parse_arxiv_atom(missing_id_atom)

        empty_id_atom = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry><id/><title>Some title with empty id</title></entry>
</feed>
"""
        with self.assertRaises(RadarFetchError):
            parse_arxiv_atom(empty_id_atom)

        # Valid empty Atom feed (zero <entry> elements) MUST still return []
        empty_atom = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>ArXiv Query: no results</title>
</feed>
"""
        self.assertEqual(parse_arxiv_atom(empty_atom), [])


class TestBackoffAndDeduplication(unittest.TestCase):
    def test_429_retry_after_exceeding_max_backoff_fails_closed(self) -> None:
        calls = {"n": 0}
        sleeps: list[float] = []

        def mock_429_120(_url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            calls["n"] += 1
            return HttpResponse(status=429, body=b"slow down", headers={"Retry-After": "120"})

        with self.assertRaises(RadarFetchError) as ctx:
            fetch_with_backoff(
                "https://mock.local/arxiv",
                max_retries=3,
                max_backoff=30.0,
                fetch_fn=mock_429_120,
                sleep_fn=sleeps.append,
            )
        self.assertIn("120.0s", str(ctx.exception))
        # Must fail immediately without premature retry or clamping 120s to 30s
        self.assertEqual(calls["n"], 1)
        self.assertEqual(sleeps, [])
    def test_429_retry_after_backoff_recovers(self) -> None:
        calls = {"n": 0}
        sleeps: list[float] = []

        def mock_fetch(_url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            calls["n"] += 1
            if calls["n"] == 1:
                return HttpResponse(status=429, body=b"rate limited", headers={"retry-after": "2"})
            return HttpResponse(status=200, body=_SAMPLE_S2_JSON, headers={})

        resp = fetch_with_backoff(
            "https://mock.local/s2",
            max_retries=2,
            fetch_fn=mock_fetch,
            sleep_fn=sleeps.append,
        )
        self.assertEqual(resp.status, 200)
        self.assertEqual(calls["n"], 2)
        self.assertEqual(sleeps, [2.0])

    def test_503_exhausts_retries_and_fails_closed(self) -> None:
        sleeps: list[float] = []

        def mock_503(_url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            return HttpResponse(status=503, body=b"service unavailable", headers={})

        with self.assertRaises(RadarFetchError):
            fetch_with_backoff(
                "https://mock.local/oa",
                max_retries=2,
                base_delay=0.5,
                fetch_fn=mock_503,
                sleep_fn=sleeps.append,
            )
        self.assertEqual(sleeps, [0.5, 1.0])

    def test_timeout_exhausts_retries_and_fails_closed(self) -> None:
        sleeps: list[float] = []

        def mock_timeout(_url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            raise TimeoutError("simulated socket read timeout")

        with self.assertRaises(RadarFetchError):
            fetch_with_backoff(
                "https://mock.local/arxiv",
                max_retries=1,
                base_delay=0.25,
                fetch_fn=mock_timeout,
                sleep_fn=sleeps.append,
            )
        self.assertEqual(sleeps, [0.25])

    def test_search_all_deduplicates_and_merges_across_three_apis(self) -> None:
        def mock_router(url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            if "arxiv.org" in url:
                return HttpResponse(status=200, body=_SAMPLE_ARXIV_XML)
            if "openalex.org" in url:
                return HttpResponse(status=200, body=_SAMPLE_OPENALEX_JSON)
            if "semanticscholar.org" in url:
                return HttpResponse(status=200, body=_SAMPLE_S2_JSON)
            return HttpResponse(status=404, body=b"not found")

        recs = search_all(
            "robust k-adaptability",
            sources=("arxiv", "openalex", "semantic_scholar"),
            fetch_fn=mock_router,
            sleep_fn=lambda _: None,
        )
        # 2 arXiv + 1 OpenAlex (dup of Kurtz 2409.12630) + 1 S2 = 3 unique records
        self.assertEqual(len(recs), 3)
        kurtz = next(r for r in recs if r.arxiv_id == "2409.12630")
        self.assertEqual(sorted(kurtz.sources), ["arxiv", "openalex"])
        self.assertEqual(kurtz.venue, "Mathematical Programming")

    def test_deduplicate_by_normalized_title_when_ids_absent(self) -> None:
        r1 = PaperRecord(title="Exact Affine Rules!", authors=["A"], year=2024, sources=["arxiv"])
        r2 = PaperRecord(
            title="exact affine rules",
            authors=["A", "B"],
            year=2024,
            doi="10.1000/test",
            sources=["openalex"],
        )
        deduped = deduplicate_records([r1, r2])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].doi, "10.1000/test")
        self.assertEqual(deduped[0].authors, ["A", "B"])

    def test_deduplicate_transitive_bridge_merges_two_id_groups(self) -> None:
        # r1 has only arXiv ID, r2 has only DOI, r3 carries both -> must collapse to 1 record!
        r1 = PaperRecord(
            title="Preprint Title",
            authors=["A"],
            year=2025,
            arxiv_id="2501.00042",
            sources=["arxiv"],
        )
        r2 = PaperRecord(
            title="Published Journal Title",
            authors=["A", "B"],
            year=2025,
            doi="10.1000/bridge.2025",
            venue="Math. Program.",
            sources=["openalex"],
        )
        r3 = PaperRecord(
            title="Published Journal Title",
            authors=["A", "B"],
            year=2025,
            arxiv_id="2501.00042v2",
            doi="https://doi.org/10.1000/BRIDGE.2025",
            sources=["semantic_scholar"],
        )
        deduped = deduplicate_records([r1, r2, r3])
        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].arxiv_id, "2501.00042")
        self.assertEqual(deduped[0].doi, "10.1000/bridge.2025")
        self.assertEqual(sorted(deduped[0].sources), ["arxiv", "openalex", "semantic_scholar"])

    def test_same_title_with_different_strong_ids_is_not_merged(self) -> None:
        d1 = PaperRecord(
            title="Robust Linear Optimization", authors=["X"], year=2010, doi="10.1000/paper-a"
        )
        d2 = PaperRecord(
            title="Robust Linear Optimization", authors=["Y"], year=2024, doi="10.1000/paper-b"
        )
        res_doi = deduplicate_records([d1, d2])
        self.assertEqual(len(res_doi), 2)
        self.assertEqual({r.doi for r in res_doi}, {"10.1000/paper-a", "10.1000/paper-b"})

        a1 = PaperRecord(
            title="Affine Policies Revisited", authors=["X"], year=2021, arxiv_id="2101.00001"
        )
        a2 = PaperRecord(
            title="Affine Policies Revisited", authors=["Y"], year=2025, arxiv_id="2501.00002"
        )
        res_arx = deduplicate_records([a1, a2])
        self.assertEqual(len(res_arx), 2)
        self.assertEqual({r.arxiv_id for r in res_arx}, {"2101.00001", "2501.00002"})


class TestNoveltyChecker(unittest.TestCase):
    def test_offline_novelty_report_for_open_conjectures(self) -> None:
        rep_o1 = check_conjecture("conj-o1-adr-exactness-char")
        self.assertEqual(
            rep_o1["novelty_assessment"],
            "open_with_explicit_counterexample_boundaries",
        )
        ce_ids = {c["node_id"] for c in rep_o1["boundary_counterexamples"]}
        expected_ces = {
            "ce-t2-soc-temporal",
            "ce-t3-chen-zhang",
            "ce-t4-gtw25-cond-b",
            "ce-t5-beg18-separating",
        }
        self.assertTrue(expected_ces <= ce_ids)
        self.assertGreaterEqual(len(rep_o1["closest_papers"]), 3)
        self.assertTrue(len(rep_o1["applicable_techniques"]) > 0)

        rep_o4 = check_conjecture("conj-o4-closure-scheduling")
        self.assertEqual(rep_o4["status"], "open")
        direct_ids = {d["paper_id"] for d in rep_o4["direct_literature_links"]}
        self.assertIn("a2-dmitruk18", direct_ids)
        self.assertIn("kur25", direct_ids)

    def test_unknown_conjecture_raises_error(self) -> None:
        with self.assertRaises(NoveltyCheckError):
            check_conjecture("conj-does-not-exist")

    def test_live_novelty_mode_with_mock_transport_marks_known_vs_new(self) -> None:
        def mock_router(url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            if "arxiv.org" in url:
                return HttpResponse(status=200, body=_SAMPLE_ARXIV_XML)
            if "openalex.org" in url:
                return HttpResponse(status=200, body=_SAMPLE_OPENALEX_JSON)
            return HttpResponse(status=404, body=b"")

        rep = check_conjecture(
            "conj-o4-closure-scheduling",
            live=True,
            live_sources=("arxiv", "openalex"),
            fetch_fn=mock_router,
            sleep_fn=lambda _: None,
        )
        self.assertIsNotNone(rep["live_query"])
        by_arx = {c["arxiv_id"]: c for c in rep["live_candidates"]}
        # 2409.12630 (Kurtz 2025) is already in catalog.json; 2501.99999 is NEW
        self.assertTrue(by_arx["2409.12630"]["already_in_catalog"])
        self.assertFalse(by_arx["2501.99999"]["already_in_catalog"])

    def test_live_novelty_does_not_conflate_same_title_with_different_doi_or_arxiv(self) -> None:
        # Same exact title as catalog paper bgt04 (DOI 10.1007/s10107-003-0454-y),
        # but with a DIFFERENT DOI -> MUST be marked NEW (already_in_catalog=False)!
        conflicting_s2 = json.dumps(
            {
                "data": [
                    {
                        "paperId": "s2-conflict",
                        "title": "Adjustable robust solutions of uncertain linear programs",
                        "year": 2025,
                        "venue": "Other Journal",
                        "abstract": "Different paper with identical title.",
                        "authors": [{"name": "Different Author"}],
                        "externalIds": {"DOI": "10.9999/different-paper.2025"},
                        "url": "https://example.org/other",
                    }
                ]
            }
        ).encode("utf-8")

        def mock_s2(_url: str, _headers: dict[str, str], _timeout: float) -> HttpResponse:
            return HttpResponse(status=200, body=conflicting_s2)

        rep = check_conjecture(
            "conj-o1-adr-exactness-char",
            live=True,
            live_sources=("semantic_scholar",),
            fetch_fn=mock_s2,
            sleep_fn=lambda _: None,
        )
        self.assertEqual(len(rep["live_candidates"]), 1)
        self.assertFalse(rep["live_candidates"][0]["already_in_catalog"])


if __name__ == "__main__":
    unittest.main()
