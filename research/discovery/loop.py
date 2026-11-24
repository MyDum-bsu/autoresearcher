#!/usr/bin/env python3
"""Managed Long-Horizon Discovery Loop with Pause/Kill-Switch & Model Routing (R12 #1275).

Pipeline stages:
  SELECT_OPEN_NODE -> NOVELTY_CHECK -> CONJECTURE_PROPOSAL -> FALSIFY_FIRST
    --[counterexample found]--> FALSIFIED (0 Lean budget spent)
    --[survived]--> SUBGOAL_DECOMPOSITION -> LEAN4_BLUEPRINT_VERIFY
      -> SEMANTIC_ALIGNMENT_AUDIT -> PACK_FOR_LEARNHARNESS -> PROVED

CLI:
  python3 -m research.discovery.loop --state-dir <dir> {step|run|pause|resume|status}
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import uuid
from collections.abc import Callable
from typing import Any, Protocol

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.discovery import (  # noqa: E402
    PIPELINE_STAGES,
    TERMINAL_STATUSES,
)
from research.discovery.routing import (  # noqa: E402
    STAGE_ROUTING_MATRIX,
    FormalGateViolationError,
    ModelSpec,
    RoutingPolicyError,
    select_reviewer_route,
    validate_formal_kernel_verdict,
    validate_model_spec,
    validate_review_separation,
    validate_routing_matrix,
)
from research.discovery.state import (  # noqa: E402
    DiscoveryState,
    DiscoveryStateError,
    StateStore,
    check_kill_switch,
    clear_kill_switch,
    file_sha256,
    utc_now_iso,
    write_kill_switch,
)
from research.literature.novelty import check_conjecture  # noqa: E402

ATLAS_JSON_REL = "research/atlas/atlas.json"
DEFAULT_STATE_DIR_REL = "tmp/discovery-state"

# Deterministic priority for selecting open Atlas targets
_DEFAULT_NODE_PRIORITY: tuple[str, ...] = (
    "conj-f4-vertex-lp-selector",
    "conj-o4-closure-scheduling",
    "conj-o1-adr-exactness-char",
    "conj-o8-quantifier-gap",
    "gen-multistage-k-closures",
    "gen-nonbox-conic-uncertainty",
)


class DiscoveryPausedSignal(Exception):
    """Raised internally when a PAUSE / STOP kill-switch triggers mid-stage."""

    def __init__(self, signal_kind: str, reason: str) -> None:
        super().__init__(f"{signal_kind}: {reason}")
        self.signal_kind = signal_kind
        self.reason = reason


class StageExecutor(Protocol):
    """Injectable stage executor for offline deterministic tests or live backends."""

    def propose_conjecture(
        self,
        node: dict[str, Any],
        novelty: dict[str, Any],
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]: ...

    def run_falsify_first(
        self,
        conjecture: dict[str, Any],
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]: ...

    def decompose_subgoals(
        self,
        conjecture: dict[str, Any],
        state: DiscoveryState,
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]: ...

    def verify_lean_blueprint(
        self,
        conjecture: dict[str, Any],
        lemmas: list[dict[str, Any]],
        route: ModelSpec,
        repo_root: pathlib.Path,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]: ...

    def audit_semantic_alignment(
        self,
        conjecture: dict[str, Any],
        lean_verdict: dict[str, Any],
        author_route: ModelSpec,
        reviewer_route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]: ...


def check_frozen_core_sha256(repo_root: pathlib.Path) -> tuple[bool, list[str]]:
    """Verify frozen Lean 4 core files against pinned SHA-256 digests from R2 verify_claim."""
    gates_dir = repo_root / "verification/gates"
    if str(gates_dir) not in sys.path:
        sys.path.insert(0, str(gates_dir))
    import verify_claim as vc  # type: ignore[import-not-found]

    errors: list[str] = []
    for rel_path, expected_sha in vc.PINNED_FROZEN_CORE_SHA256.items():
        full = repo_root / rel_path
        if not full.is_file():
            errors.append(f"Missing frozen core file: {rel_path}")
            continue
        actual_sha = file_sha256(full)
        if actual_sha != expected_sha:
            errors.append(
                f"Frozen core SHA-256 mismatch for {rel_path}: "
                f"expected {expected_sha[:12]}, actual {actual_sha[:12]}"
            )
    return (len(errors) == 0), errors


class OfflineMockExecutor:
    """Deterministic 100% offline executor (zero network or LLM calls).

    Supports controlled testing of:
      - `scenario="prove"`: conjecture survives exact rational falsification, decomposes into
        subgoals/lemmas, passes frozen-core + Lean 4 verification (0 sorry, 0 custom axioms),
        passes cross-family Semantic Alignment Audit, and builds an unattested draft study pack.
      - `scenario="falsify"`: conjecture is falsified during `FALSIFY_FIRST` with an exact
        rational counterexample witness; loop terminates in `FALSIFIED` with 0 Lean calls.
      - Fault injection flags (`inject_sorry`, `inject_custom_axiom`, `inject_alignment_fail`,
        `inject_mid_subgoal_pause_dir`) for deterministic negative control verification.
    """

    def __init__(
        self,
        *,
        scenario: str = "prove",
        inject_sorry: bool = False,
        inject_custom_axiom: bool = False,
        inject_alignment_fail: bool = False,
        inject_frozen_core_tamper: bool = False,
        inject_mid_subgoal_pause_dir: pathlib.Path | None = None,
    ) -> None:
        if scenario not in {"prove", "falsify"}:
            raise ValueError(f"Unsupported scenario {scenario!r}; expected 'prove' or 'falsify'")
        self.scenario = scenario
        self.inject_sorry = inject_sorry
        self.inject_custom_axiom = inject_custom_axiom
        self.inject_alignment_fail = inject_alignment_fail
        self.inject_frozen_core_tamper = inject_frozen_core_tamper
        self.inject_mid_subgoal_pause_dir = inject_mid_subgoal_pause_dir
        self._pause_injected_once = False

    def propose_conjecture(
        self,
        node: dict[str, Any],
        novelty: dict[str, Any],
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]:
        if should_stop():
            raise DiscoveryPausedSignal("PAUSE", "interrupted_during_conjecture_proposal")
        nid = str(node["id"])
        slug = re.sub(r"[^a-z0-9]+", "-", nid.lower()).strip("-")
        if self.scenario == "falsify":
            return {
                "conjecture_id": f"hyp-{slug}-overstrong-adr",
                "atlas_node_id": nid,
                "statement": (
                    f"Candidate strengthening of {nid}: naive affine decision rules achieve "
                    "zero suboptimality gap on 2-stage SOC uncertainty B_2(1)."
                ),
                "author_route": route.to_dict(),
                "novelty_assessment": novelty.get("novelty_assessment", "unknown"),
                "falsifier_spec": {
                    "engine": "exact_rational_sympy_t2_probe",
                    "grid_points": 6,
                },
            }
        return {
            "conjecture_id": f"hyp-{slug}-exact-vertex-lemma",
            "atlas_node_id": nid,
            "statement": (
                f"Scoped sub-conjecture for {nid}: finite extreme-point LP reduction over "
                "box/zonotope image Xi = L(W^r) preserves optimal value V(R)."
            ),
            "author_route": route.to_dict(),
            "novelty_assessment": novelty.get("novelty_assessment", "unknown"),
            "falsifier_spec": {
                "engine": "exact_rational_grid_oracle",
                "grid_points": 8,
            },
        }

    def run_falsify_first(
        self,
        conjecture: dict[str, Any],
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]:
        if should_stop():
            raise DiscoveryPausedSignal("PAUSE", "interrupted_during_falsify_first")
        from verification.falsifiers import battery_t1_t7 as battery

        if self.scenario == "falsify":
            # Execute real exact rational LP + SymPy Xu-Burer T2 SOC temporal probe
            res_t2 = battery.run_t2()
            survived = res_t2.observed_verdict == "exact"
            return {
                "survived": survived,
                "checked_points": 2,
                "engine": "verification.falsifiers.battery_t1_t7.run_t2",
                "executor_route": route.to_dict(),
                "counterexample": None
                if survived
                else {
                    "conjecture_id": conjecture["conjecture_id"],
                    "atlas_node_id": conjecture["atlas_node_id"],
                    "battery_case": res_t2.case_id,
                    "anchor": res_t2.anchor,
                    "witness": {
                        "v_aro_exact": res_t2.v_aro,
                        "v_adr_exact": res_t2.v_adr,
                        "strict_gap_exact": res_t2.gap,
                        "observed_verdict": res_t2.observed_verdict,
                    },
                    "verdict": "REFUTED_AT_STAGE_2_FALSIFY_FIRST",
                },
            }
        # Execute real exact rational LP T6 box-static oracle check
        res_t6 = battery.run_t6()
        survived = res_t6.observed_verdict == "exact" and res_t6.passed
        return {
            "survived": survived,
            "checked_points": 4,
            "engine": "verification.falsifiers.battery_t1_t7.run_t6",
            "executor_route": route.to_dict(),
            "v_aro_exact": res_t6.v_aro,
            "v_adr_exact": res_t6.v_adr,
            "max_gap": res_t6.gap,
            "counterexample": None,
        }

    def decompose_subgoals(
        self,
        conjecture: dict[str, Any],
        state: DiscoveryState,
        route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        cid = str(conjecture["conjecture_id"])
        planned_subgoals = [
            {
                "id": f"{cid}-sg1",
                "title": "Compactness and extreme-point representation of zonotope Xi = L(W^r)",
                "target_lemma": "zonotope_extreme_point_attainment",
                "status": "ready_for_lean",
                "author_route": route.canonical_id,
            },
            {
                "id": f"{cid}-sg2",
                "title": "Measurable Borel selector over finite vertex LP optimal face",
                "target_lemma": "borel_vertex_selector_exists",
                "status": "ready_for_lean",
                "author_route": route.canonical_id,
            },
            {
                "id": f"{cid}-sg3",
                "title": "Value equivalence between full policy space and finite vertex LP",
                "target_lemma": "vertex_lp_value_equivalence",
                "status": "ready_for_lean",
                "author_route": route.canonical_id,
            },
        ]

        existing_sg_ids = {sg["id"] for sg in state.subgoals}
        existing_lemma_names = {lm["name"] for lm in state.lemmas}

        for idx, sg in enumerate(planned_subgoals):
            if should_stop():
                raise DiscoveryPausedSignal("PAUSE", f"interrupted_before_subgoal_{idx + 1}")
            if sg["id"] not in existing_sg_ids:
                state.subgoals.append(sg)
                existing_sg_ids.add(sg["id"])
            lemma_name = sg["target_lemma"]
            if lemma_name not in existing_lemma_names:
                state.lemmas.append(
                    {
                        "name": lemma_name,
                        "subgoal_id": sg["id"],
                        "status": "draft_lean_blueprint",
                        "sorry_free": False,
                    }
                )
                existing_lemma_names.add(lemma_name)

            # Optional mid-stage pause hook (after recording first subgoal & lemma)
            if (
                idx == 0
                and self.inject_mid_subgoal_pause_dir is not None
                and not self._pause_injected_once
            ):
                self._pause_injected_once = True
                write_kill_switch(
                    self.inject_mid_subgoal_pause_dir,
                    reason="mid_subgoal_pause_test",
                    hard_stop=False,
                )

        return list(state.subgoals), list(state.lemmas)

    def verify_lean_blueprint(
        self,
        conjecture: dict[str, Any],
        lemmas: list[dict[str, Any]],
        route: ModelSpec,
        repo_root: pathlib.Path,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]:
        if should_stop():
            raise DiscoveryPausedSignal("PAUSE", "interrupted_during_lean_verify")
        frozen_ok, frozen_errors = check_frozen_core_sha256(repo_root)
        if self.inject_frozen_core_tamper:
            frozen_ok = False
            frozen_errors = ["Injected frozen core tampering"]

        sorry_count = 1 if self.inject_sorry else 0
        custom_axioms = ["AroProofs.unsafe_oracle_axiom"] if self.inject_custom_axiom else []
        used_axioms = ["propext", "Classical.choice", "Quot.sound"] + custom_axioms
        verified_decls = [f"AroProofs.Discovery.{lm['name']}" for lm in lemmas]
        lean_ok = frozen_ok and sorry_count == 0 and not custom_axioms and bool(verified_decls)

        return {
            "conjecture_id": conjecture["conjecture_id"],
            "lean_verified": lean_ok,
            "sorry_count": sorry_count,
            "custom_axioms": custom_axioms,
            "used_axioms": used_axioms,
            "frozen_core_intact": frozen_ok,
            "frozen_core_errors": frozen_errors,
            "verified_decls": verified_decls,
            "executor_route": route.to_dict(),
        }

    def audit_semantic_alignment(
        self,
        conjecture: dict[str, Any],
        lean_verdict: dict[str, Any],
        author_route: ModelSpec,
        reviewer_route: ModelSpec,
        should_stop: Callable[[], bool],
    ) -> dict[str, Any]:
        if should_stop():
            raise DiscoveryPausedSignal("PAUSE", "interrupted_during_semantic_alignment")
        passed = not self.inject_alignment_fail
        return {
            "conjecture_id": conjecture["conjecture_id"],
            "alignment_passed": passed,
            "author_route": author_route.to_dict(),
            "reviewer_route": reviewer_route.to_dict(),
            "lean_decls_audited": list(lean_verdict.get("verified_decls", [])),
            "findings": [] if passed else ["Formal Lean statement weakens conjecture premise"],
        }


def _deduplicate_items(
    existing: list[dict[str, Any]],
    incoming: list[dict[str, Any]],
    *,
    key_field: str,
    label: str,
) -> list[dict[str, Any]]:
    """Order-preserving deduplication of subgoals/lemmas by canonical identifier."""
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in [*existing, *incoming]:
        if not isinstance(item, dict):
            raise FormalGateViolationError(f"{label} entries must be JSON objects")
        ident = item.get(key_field)
        if not isinstance(ident, str) or not ident.strip():
            raise FormalGateViolationError(
                f"{label} entry missing non-empty string {key_field!r}: {item!r}"
            )
        if ident not in seen:
            seen.add(ident)
            merged.append(item)
    return merged


def _load_atlas(repo_root: pathlib.Path) -> tuple[dict[str, Any], str]:
    atlas_path = repo_root / ATLAS_JSON_REL
    if not atlas_path.is_file():
        raise DiscoveryStateError(f"Missing Atlas file: {atlas_path}")
    sha = file_sha256(atlas_path)
    data = json.loads(atlas_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("nodes"), list):
        raise DiscoveryStateError(f"Malformed Atlas JSON: {atlas_path}")
    return data, sha


def _select_open_atlas_node(
    atlas: dict[str, Any],
    requested_node_id: str | None = None,
) -> dict[str, Any]:
    open_nodes = {
        str(n["id"]): n
        for n in atlas.get("nodes", [])
        if isinstance(n, dict) and n.get("status") == "open" and n.get("id")
    }
    if not open_nodes:
        raise DiscoveryStateError("No open nodes available in research/atlas/atlas.json")
    if requested_node_id is not None:
        if requested_node_id not in open_nodes:
            raise DiscoveryStateError(
                f"Requested node {requested_node_id!r} is not an open Atlas node "
                f"(open: {sorted(open_nodes)})"
            )
        return open_nodes[requested_node_id]

    for preferred in _DEFAULT_NODE_PRIORITY:
        if preferred in open_nodes:
            return open_nodes[preferred]
    return open_nodes[sorted(open_nodes)[0]]


def _write_unattested_learn_pack(
    state_dir: pathlib.Path,
    state: DiscoveryState,
) -> dict[str, Any]:
    """Generate a 4-file unattested draft LearnHarness pack inside `state_dir/guides/`."""
    assert_node = state.selected_node or {}
    conj = state.active_conjecture or {}
    slug = re.sub(r"[^a-z0-9]+", "-", str(conj.get("conjecture_id", "discovery")).lower()).strip(
        "-"
    )
    pack_dir = state_dir / "guides" / slug
    pack_dir.mkdir(parents=True, exist_ok=True)

    title = str(assert_node.get("title_ru") or assert_node.get("title_en") or slug)
    decls = list((state.lean_verdict or {}).get("verified_decls", []))
    lemmas_md = "\n".join(f"- `{d}`" for d in decls) or "- (нет деклараций)"

    files: dict[str, str] = {
        "01-intuition-and-map.md": (
            f"# {title} — интуиция и карта\n\n"
            f"Черновик конспекта (статус: `unattested_draft`, утверждает только владелец).\n\n"
            f"```mermaid\nflowchart LR\n"
            f"  A[\"Открытый узел Атласа\"] --> B[\"Falsify-First\"]\n"
            f"  B --> C[\"Lean 4 Blueprint\"]\n"
            f"  C --> D[\"Semantic Alignment Audit\"]\n```\n"
        ),
        "02-propositions-and-chains.md": (
            f"# {title} — утверждения и цепочки доказательств\n\n"
            f"Гипотеза: `{conj.get('conjecture_id', '')}`.\n\n"
            f"Проверенные декларации Lean 4 (`0 sorry`, `0` кастомных аксиом):\n{lemmas_md}\n"
        ),
        "03-traps-and-counterexamples.md": (
            f"# {title} — ловушки и границы применимости\n\n"
            f"Узел Атласа: `{state.selected_node_id}`.\n"
            "Проверено прохождение этапа `FALSIFY_FIRST` без опровержения на точной сетке.\n"
        ),
        "04-practice-and-attestation.md": (
            f"# {title} — практика и аттестация владельца\n\n"
            "- Статус аттестации: `unattested_draft` "
            "(перевод в `attested` выполняет только человек).\n"
            "- Импорт в LearnHarness v0.7.0 через `aro push` после проверки Gate G5.\n"
        ),
    }
    written_files: list[str] = []
    for fname, body in files.items():
        fpath = pack_dir / fname
        fpath.write_text(body, encoding="utf-8")
        written_files.append(fname)

    manifest = {
        "pack_slug": slug,
        "pack_dir": str(pack_dir),
        "atlas_node_id": state.selected_node_id,
        "conjecture_id": conj.get("conjecture_id"),
        "attestation_status": "unattested_draft",
        "files": written_files,
        "verified_decls": decls,
        "generated_at": utc_now_iso(),
    }
    (pack_dir / "pack_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest


class DiscoveryLoop:
    """Stateful, resumable, fail-closed Long-Horizon Discovery Loop controller."""

    def __init__(
        self,
        state_dir: pathlib.Path,
        *,
        repo_root: pathlib.Path = REPO_ROOT,
        executor: StageExecutor | None = None,
        scenario: str = "prove",
        requested_node_id: str | None = None,
        surgical_opus: bool = False,
        opus_quota: int = 0,
        max_state_age_seconds: int | None = None,
    ) -> None:
        validate_routing_matrix(STAGE_ROUTING_MATRIX)
        if not isinstance(opus_quota, int) or isinstance(opus_quota, bool) or opus_quota < 0:
            raise RoutingPolicyError(f"opus_quota must be a non-negative int, got {opus_quota!r}")
        self.repo_root = repo_root.resolve()
        self.store = StateStore(state_dir)
        self.executor: StageExecutor = executor or OfflineMockExecutor(scenario=scenario)
        self.scenario = scenario
        self.requested_node_id = requested_node_id
        self.surgical_opus = surgical_opus
        self.opus_quota = opus_quota
        self.max_state_age_seconds = max_state_age_seconds
        self._atlas, self._atlas_sha = _load_atlas(self.repo_root)

    def _should_stop(self) -> bool:
        active, _, _ = check_kill_switch(self.store.state_dir)
        return active

    def load_or_init(self) -> DiscoveryState:
        if self.store.exists():
            return self.store.load(
                expected_atlas_sha256=self._atlas_sha,
                max_age_seconds=self.max_state_age_seconds,
            )
        state = DiscoveryState(
            run_id=f"disc-{uuid.uuid4().hex[:12]}",
            status="IDLE",
            current_stage=PIPELINE_STAGES[0],
            atlas_sha256=self._atlas_sha,
            scenario=self.scenario,
            selected_node_id=self.requested_node_id,
            opus_quota_remaining=self.opus_quota,
            surgical_opus_authorized=self.surgical_opus,
        )
        self.store.save(state)
        self.store.append_event("run_initialized", {"run_id": state.run_id})
        return state

    def status(self) -> dict[str, Any]:
        sig_active, sig_kind, sig_reason = check_kill_switch(self.store.state_dir)
        if not self.store.exists():
            return {
                "initialized": False,
                "status": "UNINITIALIZED",
                "kill_switch_active": sig_active,
                "kill_switch_kind": sig_kind,
                "kill_switch_reason": sig_reason,
            }
        state = self.store.load(
            expected_atlas_sha256=self._atlas_sha,
            max_age_seconds=self.max_state_age_seconds,
        )
        return {
            "initialized": True,
            "run_id": state.run_id,
            "status": state.status,
            "current_stage": state.current_stage,
            "selected_node_id": state.selected_node_id,
            "completed_stages": list(state.completed_stages),
            "stage_executions": dict(state.stage_executions),
            "hypotheses_count": len(state.hypotheses),
            "subgoals_count": len(state.subgoals),
            "lemmas_count": len(state.lemmas),
            "pause_reason": state.pause_reason,
            "failure_reason": state.failure_reason,
            "kill_switch_active": sig_active,
            "kill_switch_kind": sig_kind,
            "kill_switch_reason": sig_reason,
            "has_counterexample": state.counterexample is not None,
            "has_learn_pack": state.learn_pack is not None,
        }

    def pause(self, *, reason: str = "operator_pause", hard_stop: bool = False) -> DiscoveryState:
        write_kill_switch(self.store.state_dir, reason=reason, hard_stop=hard_stop)
        state = self.load_or_init()
        if state.status not in TERMINAL_STATUSES:
            state.status = "PAUSED"
            state.pause_reason = reason
            self.store.save(state)
        self.store.append_event(
            "pause_requested",
            {
                "run_id": state.run_id,
                "hard_stop": hard_stop,
                "reason": reason,
                "current_stage": state.current_stage,
            },
        )
        return state

    def resume(self) -> DiscoveryState:
        state = self.store.load(
            expected_atlas_sha256=self._atlas_sha,
            max_age_seconds=self.max_state_age_seconds,
        )
        removed = clear_kill_switch(self.store.state_dir)
        if state.status == "PAUSED":
            state.status = "RUNNING"
            state.pause_reason = None
            self.store.save(state)
        self.store.append_event(
            "run_resumed",
            {
                "run_id": state.run_id,
                "removed_signals": removed,
                "current_stage": state.current_stage,
                "status": state.status,
            },
        )
        return state

    def _next_stage(self, stage: str) -> str | None:
        idx = PIPELINE_STAGES.index(stage)
        if idx + 1 < len(PIPELINE_STAGES):
            return PIPELINE_STAGES[idx + 1]
        return None

    def _pause_cleanly(self, state: DiscoveryState, kind: str, reason: str) -> DiscoveryState:
        state.status = "PAUSED"
        state.pause_reason = f"{kind}:{reason}"
        self.store.save(state)
        self.store.append_event(
            "pause_honored",
            {
                "run_id": state.run_id,
                "signal": kind,
                "reason": reason,
                "current_stage": state.current_stage,
                "preserved_subgoals": len(state.subgoals),
                "preserved_lemmas": len(state.lemmas),
            },
        )
        return state

    def step(self) -> DiscoveryState:
        """Execute at most one pipeline stage, honoring kill-switch and checkpoint idempotency."""
        state = self.load_or_init()
        if state.status in TERMINAL_STATUSES:
            return state

        sig_active, sig_kind, sig_reason = check_kill_switch(self.store.state_dir)
        if sig_active:
            return self._pause_cleanly(state, sig_kind or "PAUSE", sig_reason or "signal")
        if state.status == "PAUSED":
            return state

        stage = state.current_stage
        if stage is None:
            return state

        # Idempotent resume guard: never re-execute a stage already marked completed
        if stage in state.completed_stages:
            state.current_stage = self._next_stage(stage)
            self.store.save(state)
            return state

        state.status = "RUNNING"
        route_cfg = STAGE_ROUTING_MATRIX[stage]
        validate_model_spec(route_cfg.primary, role=route_cfg.role)

        try:
            self._execute_stage(state, stage, route_cfg.primary)
        except DiscoveryPausedSignal as paused:
            # Checkpoint preserves all partial hypotheses/subgoals/lemmas WITHOUT marking stage done
            return self._pause_cleanly(state, paused.signal_kind, paused.reason)
        except (RoutingPolicyError, FormalGateViolationError) as exc:
            state.status = "FAILED"
            state.failure_reason = str(exc)
            state.attempt_logs.append(
                {
                    "timestamp": utc_now_iso(),
                    "stage": stage,
                    "outcome": "policy_or_formal_violation",
                    "error": str(exc),
                }
            )
            self.store.save(state)
            self.store.append_event(
                "stage_failed",
                {"run_id": state.run_id, "stage": stage, "error": str(exc)},
            )
            raise

        # Post-stage kill-switch check: stage already completed cleanly; pause before next stage
        if state.status not in TERMINAL_STATUSES:
            sig_active, sig_kind, sig_reason = check_kill_switch(self.store.state_dir)
            if sig_active:
                return self._pause_cleanly(state, sig_kind or "PAUSE", sig_reason or "post_stage")

        return state

    def _record_stage_done(
        self,
        state: DiscoveryState,
        stage: str,
        route_used: ModelSpec,
        outcome: str,
        *,
        next_stage: str | None,
        terminal_status: str | None = None,
    ) -> None:
        if stage not in state.completed_stages:
            state.completed_stages.append(stage)
        state.stage_executions[stage] = state.stage_executions.get(stage, 0) + 1
        state.attempt_logs.append(
            {
                "timestamp": utc_now_iso(),
                "stage": stage,
                "route": route_used.canonical_id,
                "reasoning": route_used.reasoning_level,
                "outcome": outcome,
            }
        )
        if terminal_status is not None:
            state.status = terminal_status
            state.current_stage = None
        else:
            state.current_stage = next_stage
        self.store.save(state)
        self.store.append_event(
            "stage_completed",
            {
                "run_id": state.run_id,
                "stage": stage,
                "route": route_used.canonical_id,
                "outcome": outcome,
                "status": state.status,
                "next_stage": state.current_stage,
            },
        )

    def _execute_stage(self, state: DiscoveryState, stage: str, primary_route: ModelSpec) -> None:
        if stage == "SELECT_OPEN_NODE":
            node = _select_open_atlas_node(self._atlas, state.selected_node_id)
            state.selected_node_id = str(node["id"])
            state.selected_node = {
                "id": node["id"],
                "kind": node.get("kind"),
                "title_en": node.get("title_en"),
                "title_ru": node.get("title_ru"),
                "falsification_criteria": node.get("falsification_criteria"),
            }
            self._record_stage_done(
                state, stage, primary_route, "selected", next_stage=self._next_stage(stage)
            )
            return

        if stage == "NOVELTY_CHECK":
            if not state.selected_node_id:
                raise DiscoveryStateError("NOVELTY_CHECK requires selected_node_id")
            report = check_conjecture(
                state.selected_node_id,
                repo_root=self.repo_root,
                live=False,
            )
            state.novelty_report = {
                "conjecture_id": report["conjecture_id"],
                "novelty_assessment": report["novelty_assessment"],
                "direct_links": len(report.get("direct_literature_links", [])),
                "boundary_counterexamples": len(report.get("boundary_counterexamples", [])),
            }
            self._record_stage_done(
                state,
                stage,
                primary_route,
                str(report["novelty_assessment"]),
                next_stage=self._next_stage(stage),
            )
            return

        if stage == "CONJECTURE_PROPOSAL":
            if not state.selected_node or not state.novelty_report:
                raise DiscoveryStateError(
                    "CONJECTURE_PROPOSAL requires selected_node and novelty_report"
                )
            conj = self.executor.propose_conjecture(
                state.selected_node,
                state.novelty_report,
                primary_route,
                self._should_stop,
            )
            author_spec = ModelSpec.from_dict(conj["author_route"])
            validate_model_spec(author_spec, role="creative_math")
            state.active_conjecture = conj
            state.hypotheses.append(conj)
            self._record_stage_done(
                state, stage, author_spec, "proposed", next_stage=self._next_stage(stage)
            )
            return

        if stage == "FALSIFY_FIRST":
            if not state.active_conjecture:
                raise DiscoveryStateError("FALSIFY_FIRST requires active_conjecture")
            res = self.executor.run_falsify_first(
                state.active_conjecture, primary_route, self._should_stop
            )
            survived = res.get("survived")
            checked_pts = res.get("checked_points", 0)
            if (
                not isinstance(survived, bool)
                or not isinstance(checked_pts, int)
                or isinstance(checked_pts, bool)
                or checked_pts < 1
            ):
                raise FormalGateViolationError(
                    f"FALSIFY_FIRST contract violation: invalid result {res!r}"
                )
            state.falsification_result = res
            if not survived:
                ce = res.get("counterexample")
                if not isinstance(ce, dict) or not ce:
                    raise FormalGateViolationError(
                        "FALSIFY_FIRST returned survived=False without counterexample witness"
                    )
                ce_dir = self.store.state_dir / "counterexamples"
                ce_dir.mkdir(parents=True, exist_ok=True)
                cid = str(state.active_conjecture["conjecture_id"])
                ce_file = ce_dir / f"{cid}.json"
                ce_payload = {
                    **ce,
                    "artifact_path": str(ce_file),
                    "recorded_at": utc_now_iso(),
                }
                ce_file.write_text(
                    json.dumps(ce_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                state.counterexample = ce_payload
                self._record_stage_done(
                    state,
                    stage,
                    primary_route,
                    "falsified_early_zero_lean_spent",
                    next_stage=None,
                    terminal_status="FALSIFIED",
                )
                return
            self._record_stage_done(
                state, stage, primary_route, "survived", next_stage=self._next_stage(stage)
            )
            return

        if stage == "SUBGOAL_DECOMPOSITION":
            if not state.active_conjecture:
                raise DiscoveryStateError("SUBGOAL_DECOMPOSITION requires active_conjecture")
            subgoals, lemmas = self.executor.decompose_subgoals(
                state.active_conjecture, state, primary_route, self._should_stop
            )
            dedup_subgoals = _deduplicate_items(
                state.subgoals, subgoals, key_field="id", label="subgoal"
            )
            dedup_lemmas = _deduplicate_items(
                state.lemmas, lemmas, key_field="name", label="lemma"
            )
            if not dedup_subgoals or not dedup_lemmas:
                raise FormalGateViolationError(
                    "SUBGOAL_DECOMPOSITION must produce >= 1 subgoal and >= 1 lemma"
                )
            state.subgoals = dedup_subgoals
            state.lemmas = dedup_lemmas
            self._record_stage_done(
                state, stage, primary_route, "decomposed", next_stage=self._next_stage(stage)
            )
            return

        if stage == "LEAN4_BLUEPRINT_VERIFY":
            if not state.active_conjecture or not state.lemmas:
                raise DiscoveryStateError("LEAN4_BLUEPRINT_VERIFY requires conjecture and lemmas")
            frozen_ok, frozen_errors = check_frozen_core_sha256(self.repo_root)
            if not frozen_ok:
                raise FormalGateViolationError(
                    f"Frozen Lean 4 core integrity failed before verification: {frozen_errors}"
                )
            verdict = self.executor.verify_lean_blueprint(
                state.active_conjecture,
                state.lemmas,
                primary_route,
                self.repo_root,
                self._should_stop,
            )
            state.lean_verdict = verdict
            # Fail closed on sorry, custom axioms, tampered frozen core, or failed kernel check
            validate_formal_kernel_verdict(verdict)
            for lm in state.lemmas:
                lm["status"] = "lean_verified"
                lm["sorry_free"] = True
            self._record_stage_done(
                state, stage, primary_route, "lean_verified", next_stage=self._next_stage(stage)
            )
            return

        if stage == "SEMANTIC_ALIGNMENT_AUDIT":
            if not state.active_conjecture:
                raise DiscoveryStateError("SEMANTIC_ALIGNMENT_AUDIT requires active_conjecture")
            # Defense-in-depth: Lean 4 kernel verdict MUST already be valid before review
            validate_formal_kernel_verdict(state.lean_verdict)
            author_spec = ModelSpec.from_dict(state.active_conjecture["author_route"])
            reviewer_spec = select_reviewer_route(
                author_spec,
                surgical_trigger=state.surgical_opus_authorized,
                opus_quota_remaining=state.opus_quota_remaining,
            )
            validate_review_separation(
                author_spec,
                reviewer_spec,
                surgical_trigger=state.surgical_opus_authorized,
                opus_quota_remaining=state.opus_quota_remaining,
            )

            audit = self.executor.audit_semantic_alignment(
                state.active_conjecture,
                state.lean_verdict or {},
                author_spec,
                reviewer_spec,
                self._should_stop,
            )
            # Re-verify audit payload against router-assigned identities BEFORE debiting quota
            ret_author = ModelSpec.from_dict(audit["author_route"])
            ret_reviewer = ModelSpec.from_dict(audit["reviewer_route"])
            if ret_author.canonical_id != author_spec.canonical_id:
                raise RoutingPolicyError(
                    f"Audit payload author {ret_author.canonical_id!r} does not match "
                    f"conjecture author {author_spec.canonical_id!r}"
                )
            if ret_reviewer.canonical_id != reviewer_spec.canonical_id:
                raise RoutingPolicyError(
                    f"Audit payload reviewer {ret_reviewer.canonical_id!r} does not match "
                    f"router-assigned reviewer {reviewer_spec.canonical_id!r}"
                )
            validate_review_separation(
                ret_author,
                ret_reviewer,
                surgical_trigger=state.surgical_opus_authorized,
                opus_quota_remaining=state.opus_quota_remaining,
            )
            if reviewer_spec.canonical_id == "anthropic/opus-5.5":
                state.opus_quota_remaining -= 1
                state.opus_quota_used += 1

            state.alignment_verdict = {
                **audit,
                "assigned_reviewer_id": reviewer_spec.canonical_id,
            }
            if audit.get("alignment_passed") is not True:
                raise FormalGateViolationError(
                    f"Semantic Alignment Audit rejected promotion: {audit.get('findings')}"
                )
            self._record_stage_done(
                state,
                stage,
                ret_reviewer,
                "alignment_passed",
                next_stage=self._next_stage(stage),
            )
            return

        if stage == "PACK_FOR_LEARNHARNESS":
            # Final promotion gate: live frozen-core SHA-256 + Lean 4 + cross-family alignment
            frozen_ok, frozen_errors = check_frozen_core_sha256(self.repo_root)
            if not frozen_ok:
                raise FormalGateViolationError(
                    f"Frozen Lean 4 core integrity failed before promotion: {frozen_errors}"
                )
            validate_formal_kernel_verdict(state.lean_verdict)
            if (
                not isinstance(state.alignment_verdict, dict)
                or state.alignment_verdict.get("alignment_passed") is not True
            ):
                raise FormalGateViolationError(
                    "Cannot promote to PROVED without passing SEMANTIC_ALIGNMENT_AUDIT"
                )
            ret_author = ModelSpec.from_dict(state.alignment_verdict["author_route"])
            ret_reviewer = ModelSpec.from_dict(state.alignment_verdict["reviewer_route"])
            assigned_id = state.alignment_verdict.get("assigned_reviewer_id")
            if assigned_id != ret_reviewer.canonical_id:
                raise RoutingPolicyError(
                    f"Promotion blocked: alignment reviewer {ret_reviewer.canonical_id!r} "
                    f"does not match assigned reviewer {assigned_id!r}"
                )
            effective_opus_quota = (
                state.opus_quota_used
                if ret_reviewer.canonical_id == "anthropic/opus-5.5"
                else state.opus_quota_remaining
            )
            validate_review_separation(
                ret_author,
                ret_reviewer,
                surgical_trigger=state.surgical_opus_authorized,
                opus_quota_remaining=effective_opus_quota,
            )
            pack = _write_unattested_learn_pack(self.store.state_dir, state)
            state.learn_pack = pack
            self._record_stage_done(
                state,
                stage,
                primary_route,
                "packed_unattested_draft",
                next_stage=None,
                terminal_status="PROVED",
            )
            return

        raise DiscoveryStateError(f"Unknown pipeline stage: {stage!r}")

    def run(self, *, max_steps: int | None = None) -> DiscoveryState:
        """Run stages sequentially until terminal status, pause kill-switch, or `max_steps`."""
        steps_taken = 0
        state = self.load_or_init()
        while state.status not in TERMINAL_STATUSES:
            if max_steps is not None and steps_taken >= max_steps:
                break
            sig_active, sig_kind, sig_reason = check_kill_switch(self.store.state_dir)
            if sig_active:
                return self._pause_cleanly(state, sig_kind or "PAUSE", sig_reason or "signal")
            if state.status == "PAUSED":
                break
            state = self.step()
            steps_taken += 1
            if state.status == "PAUSED":
                break
        return state


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Long-Horizon Discovery Loop with Pause/Kill-Switch & Model Routing (R12 #1275)"
    )
    parser.add_argument(
        "--state-dir",
        type=pathlib.Path,
        default=REPO_ROOT / DEFAULT_STATE_DIR_REL,
        help="Persistent state directory (kept outside Git; default: tmp/discovery-state)",
    )
    parser.add_argument("--node-id", default=None, help="Explicit open Atlas node ID")
    parser.add_argument(
        "--scenario",
        choices=("prove", "falsify"),
        default="prove",
        help="Offline deterministic scenario (default: prove)",
    )
    parser.add_argument("--surgical-opus", action="store_true", help="Authorize surgical opus-5.5")
    parser.add_argument("--opus-quota", type=int, default=0, help="Surgical opus-5.5 call quota")
    parser.add_argument("--max-steps", type=int, default=None, help="Max stages for `run`")
    parser.add_argument("--reason", default="operator_pause", help="Reason for `pause`")
    parser.add_argument("--hard-stop", action="store_true", help="Write STOP instead of PAUSE")
    parser.add_argument("--json", action="store_true", help="Print JSON summary")
    parser.add_argument(
        "command",
        choices=("step", "run", "pause", "resume", "status"),
        help="Discovery loop control command",
    )
    args = parser.parse_args(argv)

    try:
        loop = DiscoveryLoop(
            args.state_dir,
            scenario=args.scenario,
            requested_node_id=args.node_id,
            surgical_opus=args.surgical_opus,
            opus_quota=args.opus_quota,
        )
        if args.command == "status":
            out: dict[str, Any] = loop.status()
        elif args.command == "pause":
            st = loop.pause(reason=args.reason, hard_stop=args.hard_stop)
            out = {"command": "pause", "status": st.status, "current_stage": st.current_stage}
        elif args.command == "resume":
            st = loop.resume()
            out = {"command": "resume", "status": st.status, "current_stage": st.current_stage}
        elif args.command == "step":
            st = loop.step()
            out = {
                "command": "step",
                "run_id": st.run_id,
                "status": st.status,
                "current_stage": st.current_stage,
                "completed_stages": st.completed_stages,
            }
        else:
            st = loop.run(max_steps=args.max_steps)
            out = {
                "command": "run",
                "run_id": st.run_id,
                "status": st.status,
                "current_stage": st.current_stage,
                "completed_stages": st.completed_stages,
            }
    except (
        DiscoveryStateError,
        RoutingPolicyError,
        FormalGateViolationError,
        ValueError,
    ) as exc:
        print(f"DISCOVERY LOOP ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(
            f"DISCOVERY {args.command.upper()}: status={out.get('status')} "
            f"stage={out.get('current_stage')} "
            f"completed={len(out.get('completed_stages', []))}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
