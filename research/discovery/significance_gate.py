#!/usr/bin/env python3
"""Journal Editor Significance Gate (anti-Goodhart scientific value filter, #1714).

Enforces before spending Lean 4 or remote Colab GPU compute that every candidate
hypothesis:
  1. Targets a genuine `status == "open"` frontier node in `research/atlas/atlas.json`
     (especially primary open questions O4, G1, G2, O1, O8).
  2. Is non-trivial and non-degenerate (rejects Goodhart traps: trivial helper lemmas,
     pure renamings, tautologies, 0D/degenerate-only claims).
  3. Provides a concrete Stage-2 Falsify-First prediction verifiable by exact rational LP,
     SymPy, or the T1-T7 battery.
  4. Is distinct from already-proved / falsified Atlas results (checked via
     `SemanticAtlasIndex` cosine similarity).

Zero `assert` statements — behaves identically under `python3 -B` and `python3 -B -O`.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import sys
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.atlas.semantic_index import ATLAS_JSON_DEFAULT, SemanticAtlasIndex  # noqa: E402

PRIMARY_FRONTIER_NODE_IDS: frozenset[str] = frozenset(
    {
        "conj-o4-closure-scheduling",
        "gen-multistage-k-closures",
        "gen-nonbox-conic-uncertainty",
        "conj-o1-adr-exactness-char",
        "conj-o8-quantifier-gap",
    }
)

APPROVED_FALSIFIER_METHODS: frozenset[str] = frozenset(
    {
        "exact_rational_lp",
        "sympy_symbolic",
        "battery_t1_t7",
        "exact_rational_lp+sympy",
        "exact_rational_lp+battery_t1_t7",
    }
)

TRIVIAL_THEOREM_CLASSES: frozenset[str] = frozenset(
    {
        "trivial_helper",
        "renaming",
        "boilerplate",
        "algebraic_identity",
        "tautology",
    }
)

APPROVED_THEOREM_CLASSES: frozenset[str] = frozenset(
    {
        "characterization",
        "separation_counterexample",
        "sharp_bound",
        "reduction_theorem",
        "structural_property",
        "dichotomy",
    }
)

_TRIVIAL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\btrivial\s+lemma\b", re.IGNORECASE),
    re.compile(r"\bhelper\s+lemma\b", re.IGNORECASE),
    re.compile(r"\bpure\s+renam(?:ing|e)\b", re.IGNORECASE),
    re.compile(r"\bby\s+reflexivity\b", re.IGNORECASE),
    re.compile(r"\bimmediate\s+corollary\s+of\s+f1\b", re.IGNORECASE),
    re.compile(r"\b0-?dimensional\b", re.IGNORECASE),
    re.compile(r"\brho\s*=\s*0\s+only\b", re.IGNORECASE),
    re.compile(r"\b([a-zA-Z])\s*=\s*\1\b"),
    re.compile(r"\b0\s*=\s*0\b"),
    re.compile(r"\b1\s*=\s*1\b"),
    re.compile(r"\bequals?\s+(?:itself|that\s+same\b|the\s+same\b)", re.IGNORECASE),
    re.compile(
        r"\b([a-zA-Z0-9_ ]{4,60}?)\s+(?:equals|is\s+equal\s+to)\s+"
        r"(?:that\s+same\s+|the\s+same\s+)?\1\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bof\s+(?:its|the|a)\s+([a-zA-Z0-9_ ]{3,40}?)\s+equals\b.*"
        r"\bof\s+(?:that|the)\s+same\s+\1\b",
        re.IGNORECASE,
    ),
)

_SUBSTANTIVE_MATH_RE = re.compile(
    r"\b(?:exact|gap|strict|submodular|supermodular|markov|history|conic|polytope|"
    r"simplex|zonotope|support|minimax|maximin|rank|dichotomy|criterion|necessary|"
    r"sufficient|counterexample|separation|vertex|lp|adr|aro|closure|schedule)\b",
    re.IGNORECASE,
)

MIN_PASS_SCORE = 8
MAX_SCORE = 12


class SignificanceGateError(RuntimeError):
    """Raised on malformed significance candidate payloads or self-test failure."""


@dataclasses.dataclass(frozen=True)
class SignificanceCandidate:
    candidate_id: str
    target_open_node_id: str
    title: str
    statement: str
    closes_gap_mechanism: str
    falsifiable_prediction: str
    falsifier_method: str
    dimension_regime: str
    expected_theorem_class: str
    extends_beyond_nodes: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SignificanceCandidate:
        if not isinstance(data, dict):
            raise SignificanceGateError("Candidate payload must be a JSON object")
        req = (
            "candidate_id",
            "target_open_node_id",
            "title",
            "statement",
            "closes_gap_mechanism",
            "falsifiable_prediction",
            "falsifier_method",
            "dimension_regime",
            "expected_theorem_class",
        )
        for key in req:
            val = data.get(key)
            if not isinstance(val, str) or not val.strip():
                raise SignificanceGateError(f"Missing or empty string field {key!r}")
        ext = data.get("extends_beyond_nodes", ())
        if not isinstance(ext, (list, tuple)) or not all(isinstance(x, str) for x in ext):
            raise SignificanceGateError("extends_beyond_nodes must be a list of strings")
        return cls(
            candidate_id=data["candidate_id"].strip(),
            target_open_node_id=data["target_open_node_id"].strip(),
            title=data["title"].strip(),
            statement=data["statement"].strip(),
            closes_gap_mechanism=data["closes_gap_mechanism"].strip(),
            falsifiable_prediction=data["falsifiable_prediction"].strip(),
            falsifier_method=data["falsifier_method"].strip(),
            dimension_regime=data["dimension_regime"].strip(),
            expected_theorem_class=data["expected_theorem_class"].strip(),
            extends_beyond_nodes=tuple(x.strip() for x in ext if x.strip()),
        )


@dataclasses.dataclass(frozen=True)
class SignificanceVerdict:
    candidate_id: str
    target_open_node_id: str
    decision: str  # "ACCEPT" | "REJECT"
    score: int
    max_score: int
    min_pass_score: int
    axis_scores: dict[str, int]
    rejection_reasons: list[str]
    similar_closed_nodes: list[dict[str, Any]]
    atlas_sha256: str

    def to_dict(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


def evaluate_significance(
    candidate: SignificanceCandidate,
    *,
    atlas_path: pathlib.Path = ATLAS_JSON_DEFAULT,
    semantic_index: SemanticAtlasIndex | None = None,
    duplicate_threshold: float = 0.78,
) -> SignificanceVerdict:
    """Evaluate a candidate hypothesis against the Journal Editor Significance Gate."""
    raw_atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
    nodes_by_id: dict[str, dict[str, Any]] = {
        str(n["id"]): n for n in raw_atlas.get("nodes", []) if isinstance(n, dict) and "id" in n
    }
    idx = semantic_index or SemanticAtlasIndex(atlas_path=atlas_path, backend="offline_tfidf")

    rejections: list[str] = []

    # Axis 1: Frontier alignment (0..3)
    target_node = nodes_by_id.get(candidate.target_open_node_id)
    if target_node is None:
        frontier_score = 0
        rejections.append(
            f"target_open_node_id {candidate.target_open_node_id!r} not found in Atlas"
        )
    elif target_node.get("status") != "open":
        frontier_score = 0
        rejections.append(
            f"target_open_node_id {candidate.target_open_node_id!r} has status "
            f"{target_node.get('status')!r}, expected 'open'"
        )
    else:
        is_primary = candidate.target_open_node_id in PRIMARY_FRONTIER_NODE_IDS
        mech_ok = len(candidate.closes_gap_mechanism) >= 40 and bool(
            _SUBSTANTIVE_MATH_RE.search(candidate.closes_gap_mechanism)
        )
        if is_primary and mech_ok:
            frontier_score = 3
        elif is_primary or mech_ok:
            frontier_score = 2
        else:
            frontier_score = 1

    # Axis 2: Non-triviality / Anti-Goodhart (0..3)
    combined_text = (
        f"{candidate.title}\n{candidate.statement}\n"
        f"{candidate.closes_gap_mechanism}\n{candidate.dimension_regime}"
    )
    trivial_hits = [p.pattern for p in _TRIVIAL_PATTERNS if p.search(combined_text)]
    if candidate.expected_theorem_class in TRIVIAL_THEOREM_CLASSES:
        nontrivial_score = 0
        rejections.append(
            f"Anti-Goodhart reject: expected_theorem_class={candidate.expected_theorem_class!r} "
            "is classified as trivial"
        )
    elif trivial_hits:
        nontrivial_score = 0
        rejections.append(
            f"Anti-Goodhart reject: trivial/degenerate phrasing detected ({trivial_hits[0]})"
        )
    elif candidate.expected_theorem_class not in APPROVED_THEOREM_CLASSES:
        nontrivial_score = 0
        rejections.append(
            f"Unrecognized expected_theorem_class={candidate.expected_theorem_class!r}"
        )
    else:
        stmt_math_hits = len(
            {m.group(0).lower() for m in _SUBSTANTIVE_MATH_RE.finditer(candidate.statement)}
        )
        math_hits = len({m.group(0).lower() for m in _SUBSTANTIVE_MATH_RE.finditer(combined_text)})
        if len(candidate.statement) < 40 or stmt_math_hits < 2:
            nontrivial_score = 0
            rejections.append(
                "Anti-Goodhart reject: statement lacks substantive domain mathematical content "
                f"(len={len(candidate.statement)}, domain_terms={stmt_math_hits})"
            )
        elif (
            len(candidate.statement) >= 60
            and stmt_math_hits >= 3
            and math_hits >= 4
            and len(candidate.dimension_regime) >= 8
        ):
            nontrivial_score = 3
        else:
            nontrivial_score = 2

    # Axis 3: Stage-2 Falsifiability (0..3)
    if candidate.falsifier_method not in APPROVED_FALSIFIER_METHODS:
        falsify_score = 0
        rejections.append(
            f"falsifier_method {candidate.falsifier_method!r} not in approved deterministic methods"
        )
    elif len(candidate.falsifiable_prediction) < 30:
        falsify_score = 0
        rejections.append("falsifiable_prediction is too vague (< 30 chars)")
    else:
        has_quant = bool(
            re.search(
                r"(?:<=|>=|<|>|==|!=|\bgap\b|\bexact\b|\bcounterexample\b|\bwitness\b)",
                candidate.falsifiable_prediction,
                re.IGNORECASE,
            )
        )
        falsify_score = 3 if (len(candidate.falsifiable_prediction) >= 50 and has_quant) else 2

    # Axis 4: Novelty vs already-closed Atlas nodes (0..3)
    dup_proved = idx.check_duplicate(
        candidate.title,
        candidate.statement,
        threshold=duplicate_threshold,
        top_k=3,
        status_filter="lean_proved",
    )
    dup_falsified = idx.check_duplicate(
        candidate.title,
        candidate.statement,
        threshold=duplicate_threshold,
        top_k=2,
        status_filter="falsified",
    )
    similar_closed = sorted(
        dup_proved["matches"] + dup_falsified["matches"],
        key=lambda m: (-float(m["score"]), str(m["node_id"])),
    )[:4]
    max_closed_sim = float(similar_closed[0]["score"]) if similar_closed else 0.0

    invalid_extends = [nid for nid in candidate.extends_beyond_nodes if nid not in nodes_by_id]
    if invalid_extends:
        novelty_score = 0
        rejections.append(f"extends_beyond_nodes contains unknown Atlas IDs: {invalid_extends}")
    elif max_closed_sim >= duplicate_threshold:
        novelty_score = 0
        rejections.append(
            f"DUPLICATE_OF_EXISTING_ATLAS_RESULT: cosine={max_closed_sim:.4f} >= "
            f"{duplicate_threshold} with {similar_closed[0]['node_id']!r}"
        )
    elif max_closed_sim < 0.55 and len(candidate.extends_beyond_nodes) >= 1:
        novelty_score = 3
    elif max_closed_sim < 0.65:
        novelty_score = 2
    else:
        novelty_score = 1

    axis_scores = {
        "frontier_alignment": frontier_score,
        "nontriviality": nontrivial_score,
        "falsifiability": falsify_score,
        "novelty_vs_atlas": novelty_score,
    }
    total_score = sum(axis_scores.values())
    if total_score < MIN_PASS_SCORE:
        rejections.append(f"Total significance score {total_score}/{MAX_SCORE} < {MIN_PASS_SCORE}")

    decision = (
        "ACCEPT" if (not rejections and all(v >= 1 for v in axis_scores.values())) else "REJECT"
    )
    return SignificanceVerdict(
        candidate_id=candidate.candidate_id,
        target_open_node_id=candidate.target_open_node_id,
        decision=decision,
        score=total_score,
        max_score=MAX_SCORE,
        min_pass_score=MIN_PASS_SCORE,
        axis_scores=axis_scores,
        rejection_reasons=rejections,
        similar_closed_nodes=similar_closed,
        atlas_sha256=idx.atlas_sha256,
    )


def run_self_test(atlas_path: pathlib.Path = ATLAS_JSON_DEFAULT) -> int:
    """Negative & positive self-tests (5/5 controls, zero `assert`)."""
    idx = SemanticAtlasIndex(atlas_path=atlas_path, backend="offline_tfidf")

    # 1. Valid frontier candidate MUST PASS
    good = SignificanceCandidate(
        candidate_id="test-o4-submod",
        target_open_node_id="conj-o4-closure-scheduling",
        title="O4 Submodularity vs Synergy of Multi-Closure Information Value G(R)",
        statement=(
            "Test whether the measurement value function G(R) = V(empty) - V(R) is submodular "
            "across closure schedules R subset {1,...,T-1} on discrete linear OGU systems with "
            "box controls and disturbances, or exhibits strict supermodular synergy."
        ),
        closes_gap_mechanism=(
            "Advances O4 beyond single-closure separation (thm-o4-single-closure-value) by "
            "determining whether greedy schedule selection has a submodular guarantee."
        ),
        falsifiable_prediction=(
            "Exact rational Vertex-LP over R in {empty, {1}, {2}, {1,2}} checks whether "
            "G({1,2}) - G({1}) <= G({2}) - G(empty) holds or yields a strict counterexample."
        ),
        falsifier_method="exact_rational_lp",
        dimension_regime="1D-2D linear OGU, T>=3, k=2 closures",
        expected_theorem_class="structural_property",
        extends_beyond_nodes=("thm-o4-single-closure-value",),
    )
    v_good = evaluate_significance(good, atlas_path=atlas_path, semantic_index=idx)
    if v_good.decision != "ACCEPT":
        raise SignificanceGateError(f"Valid frontier candidate rejected: {v_good}")

    # 2. Goodhart trivial helper lemma MUST BE REJECTED
    trivial = SignificanceCandidate(
        candidate_id="test-goodhart-trivial",
        target_open_node_id="conj-o4-closure-scheduling",
        title="Trivial lemma renaming F1 prefix expansion",
        statement=(
            "An immediate corollary of F1 by reflexivity showing rho = 0 only gives zero noise."
        ),
        closes_gap_mechanism="Helper lemma for convenience in Lean proofs.",
        falsifiable_prediction="Check rho = 0 gives zero disturbance.",
        falsifier_method="exact_rational_lp",
        dimension_regime="0-dimensional",
        expected_theorem_class="trivial_helper",
    )
    v_triv = evaluate_significance(trivial, atlas_path=atlas_path, semantic_index=idx)
    if v_triv.decision != "REJECT":
        raise SignificanceGateError("Goodhart trivial helper lemma was NOT rejected")

    # 3. Targeting already-proved node MUST BE REJECTED
    already_proved = dataclasses.replace(
        good,
        candidate_id="test-closed-target",
        target_open_node_id="thm-f1-expansion",
    )
    v_closed = evaluate_significance(already_proved, atlas_path=atlas_path, semantic_index=idx)
    if v_closed.decision != "REJECT":
        raise SignificanceGateError("Candidate targeting already-proved node was NOT rejected")

    # 4. Near-verbatim duplicate of an already-proved theorem MUST BE REJECTED
    raw_atlas = json.loads(atlas_path.read_text(encoding="utf-8"))
    f1_node = next(n for n in raw_atlas["nodes"] if n["id"] == "thm-o4-single-closure-value")
    dup_cand = dataclasses.replace(
        good,
        candidate_id="test-dup-o4",
        title=str(f1_node["title_en"]),
        statement=str(f1_node["statement_en"]),
    )
    v_dup = evaluate_significance(
        dup_cand, atlas_path=atlas_path, semantic_index=idx, duplicate_threshold=0.55
    )
    if v_dup.decision != "REJECT":
        raise SignificanceGateError(f"Duplicate of proved Atlas node was NOT rejected: {v_dup}")

    # 5. Unfalsifiable candidate (unapproved method) MUST BE REJECTED
    unfalsifiable = dataclasses.replace(
        good,
        candidate_id="test-no-falsifier",
        falsifier_method="llm_intuition_only",
    )
    v_unf = evaluate_significance(unfalsifiable, atlas_path=atlas_path, semantic_index=idx)
    if v_unf.decision != "REJECT":
        raise SignificanceGateError("Unfalsifiable candidate was NOT rejected")

    # 6. Tautological identity (e.g. `forall x in R, x = x`) with padded rubric fields MUST REJECT
    taut = dataclasses.replace(
        good,
        candidate_id="test-tautology-x-eq-x",
        title="Universal real equality identity",
        statement="For all x in R, x = x.",
    )
    v_taut = evaluate_significance(taut, atlas_path=atlas_path, semantic_index=idx)
    if v_taut.decision != "REJECT":
        raise SignificanceGateError(f"Tautological identity x = x was NOT rejected: {v_taut}")

    # 7. Prose reflexive tautology with domain keywords MUST REJECT
    prose_taut = dataclasses.replace(
        good,
        candidate_id="test-tautology-prose-rank",
        title="Closure schedule matrix rank identity",
        statement=(
            "For every closure schedule R, the exact rank of its matrix M_R "
            "equals the exact rank of that same matrix M_R."
        ),
    )
    v_pt = evaluate_significance(prose_taut, atlas_path=atlas_path, semantic_index=idx)
    if v_pt.decision != "REJECT":
        raise SignificanceGateError(f"Prose reflexive tautology was NOT rejected: {v_pt}")

    print(
        "SIGNIFICANCE GATE SELF-TEST OK: 7/7 controls passed "
        "(valid frontier ACCEPT / Goodhart trivial REJECT / closed target REJECT / "
        "proved duplicate REJECT / non-deterministic falsifier REJECT / "
        "tautology x=x REJECT / prose tautology REJECT)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Journal Editor Significance Gate (#1714).")
    parser.add_argument("--manifest", default=None, help="Path to Run-02 manifest JSON.")
    parser.add_argument("--atlas", default=str(ATLAS_JSON_DEFAULT), help="Path to atlas.json.")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    atlas_path = pathlib.Path(args.atlas)
    try:
        if args.self_test:
            return run_self_test(atlas_path)
        if not args.manifest:
            parser.print_help()
            return 0
        manifest = json.loads(pathlib.Path(args.manifest).read_text(encoding="utf-8"))
        idx = SemanticAtlasIndex(atlas_path=atlas_path, backend="offline_tfidf")
        verdicts = [
            evaluate_significance(
                SignificanceCandidate.from_dict(c),
                atlas_path=atlas_path,
                semantic_index=idx,
            ).to_dict()
            for c in manifest.get("candidates", [])
        ]
        all_ok = all(v["decision"] == "ACCEPT" for v in verdicts)
    except (SignificanceGateError, OSError, ValueError, KeyError) as exc:
        print(f"SIGNIFICANCE GATE ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(
            json.dumps(
                {"status": "ok" if all_ok else "rejected", "verdicts": verdicts},
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        accepted = sum(1 for v in verdicts if v["decision"] == "ACCEPT")
        print(f"SIGNIFICANCE GATE: {accepted}/{len(verdicts)} candidates ACCEPTED")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
