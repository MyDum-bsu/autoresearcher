#!/usr/bin/env python3
"""Deterministic verifier & negative self-tests for R12 Long-Horizon Discovery Loop (#1275).

Enforces (zero `assert` — works identically under `python3 -B` and `python3 -B -O`):
  1. Routing matrix completeness & strict policy audit (zero `zcode`, DeepSeek-only in
     `opencode-go`, `gemini-4-neon (high)` for `creative_math`, cross-family review);
  2. Frozen `AroCore/` + `BridgeFormalV2/` SHA-256 integrity;
  3. Full offline `FALSIFY_FIRST` cycle: refutes candidate at Stage 2 with concrete witness,
     terminates in `FALSIFIED`, and spends ZERO Lean 4 budget;
  4. Full offline `PROVE` cycle with mid-flight `pause` -> `status` -> `resume`: preserves
     intermediate subgoals & lemmas across pause, executes every stage strictly once, and
     produces an unattested 4-file LearnHarness draft pack;
  5. Negative `--self-test` (10/10 controls): self-acceptance, family-spoofing, banned `zcode`,
     non-DeepSeek `opencode-go`, unauthorized `opus-5.5`, Lean `sorry`, custom Lean axiom,
     failed Semantic Alignment Audit, corrupted/tampered state, stale schema/Atlas state.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import tempfile
from typing import Any

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from research.discovery import PIPELINE_STAGES  # noqa: E402
from research.discovery.loop import (  # noqa: E402
    DiscoveryLoop,
    OfflineMockExecutor,
    check_frozen_core_sha256,
)
from research.discovery.routing import (  # noqa: E402
    MODEL_GEMINI_4_NEON,
    MODEL_OPUS_5_5_SURGICAL,
    STAGE_ROUTING_MATRIX,
    FormalGateViolationError,
    ModelSpec,
    RoutingPolicyError,
    validate_formal_kernel_verdict,
    validate_model_spec,
    validate_review_separation,
    validate_routing_matrix,
)
from research.discovery.state import (  # noqa: E402
    STATE_FILENAME,
    DiscoveryStateError,
    StateStore,
)


class DiscoveryVerificationError(RuntimeError):
    """Raised when any Discovery Loop verification invariant or self-test fails."""


def _expect(cond: bool, msg: str) -> None:
    if not cond:
        raise DiscoveryVerificationError(msg)


def verify_discovery_pipeline(repo_root: pathlib.Path = REPO_ROOT) -> dict[str, Any]:
    """Run routing audit, frozen-core audit, and both end-to-end offline dry-runs."""
    routing_summary = validate_routing_matrix(STAGE_ROUTING_MATRIX)

    frozen_ok, frozen_errors = check_frozen_core_sha256(repo_root)
    _expect(frozen_ok, f"Frozen Lean 4 core integrity failed: {frozen_errors}")

    # Dry-run 1: FALSIFY_FIRST early termination (0 Lean budget spent)
    with tempfile.TemporaryDirectory(prefix="aro-r12-falsify-") as tmp1:
        dir1 = pathlib.Path(tmp1)
        loop1 = DiscoveryLoop(
            dir1,
            repo_root=repo_root,
            scenario="falsify",
            requested_node_id="conj-o1-adr-exactness-char",
        )
        st1 = loop1.run()
        _expect(st1.status == "FALSIFIED", f"Expected FALSIFIED, got {st1.status!r}")
        _expect(st1.counterexample is not None, "FALSIFIED run must record counterexample")
        ce_path = pathlib.Path(str(st1.counterexample["artifact_path"]))
        _expect(ce_path.is_file(), f"Counterexample artifact missing on disk: {ce_path}")
        _expect(
            "LEAN4_BLUEPRINT_VERIFY" not in st1.completed_stages
            and st1.stage_executions.get("LEAN4_BLUEPRINT_VERIFY", 0) == 0,
            "FALSIFIED run MUST NOT spend Lean 4 verification budget",
        )
        _expect(
            st1.completed_stages
            == ["SELECT_OPEN_NODE", "NOVELTY_CHECK", "CONJECTURE_PROPOSAL", "FALSIFY_FIRST"],
            f"Unexpected FALSIFIED stage trace: {st1.completed_stages}",
        )

    # Dry-run 2: PROVE with mid-subgoal PAUSE -> status -> resume -> PROVED (idempotent)
    with tempfile.TemporaryDirectory(prefix="aro-r12-prove-") as tmp2:
        dir2 = pathlib.Path(tmp2)
        exec2 = OfflineMockExecutor(scenario="prove", inject_mid_subgoal_pause_dir=dir2)
        loop2 = DiscoveryLoop(
            dir2,
            repo_root=repo_root,
            executor=exec2,
            requested_node_id="conj-o4-closure-scheduling",
        )
        st_paused = loop2.run()
        _expect(st_paused.status == "PAUSED", f"Expected PAUSED mid-run, got {st_paused.status!r}")
        _expect(
            st_paused.current_stage == "SUBGOAL_DECOMPOSITION",
            f"Expected pause inside SUBGOAL_DECOMPOSITION, got {st_paused.current_stage!r}",
        )
        _expect(
            len(st_paused.subgoals) >= 1 and len(st_paused.lemmas) >= 1,
            "Mid-stage pause must preserve already-generated subgoals and lemmas",
        )
        status_snap = loop2.status()
        _expect(
            status_snap["status"] == "PAUSED" and status_snap["kill_switch_active"] is True,
            f"Unexpected paused status snapshot: {status_snap}",
        )
        # Stepping while paused MUST be a clean no-op
        st_still_paused = loop2.step()
        _expect(st_still_paused.status == "PAUSED", "step() advanced while PAUSED")

        # Resume in a fresh controller instance (proving persistence across process restarts)
        loop2_resumed = DiscoveryLoop(
            dir2,
            repo_root=repo_root,
            executor=OfflineMockExecutor(scenario="prove"),
            requested_node_id="conj-o4-closure-scheduling",
        )
        loop2_resumed.resume()
        st_done = loop2_resumed.run()
        _expect(st_done.status == "PROVED", f"Expected PROVED after resume, got {st_done.status!r}")
        _expect(
            st_done.completed_stages == list(PIPELINE_STAGES),
            f"Incomplete stages on PROVED: {st_done.completed_stages}",
        )
        _expect(
            all(st_done.stage_executions.get(s) == 1 for s in PIPELINE_STAGES),
            f"Idempotency violation — duplicate stage execution: {st_done.stage_executions}",
        )
        _expect(st_done.learn_pack is not None, "PROVED run must produce LearnHarness draft pack")
        _expect(
            st_done.learn_pack["attestation_status"] == "unattested_draft",
            "Automated pipeline MUST NEVER set status 'attested'",
        )
        pack_dir = pathlib.Path(str(st_done.learn_pack["pack_dir"]))
        for req_file in (
            "01-intuition-and-map.md",
            "02-propositions-and-chains.md",
            "03-traps-and-counterexamples.md",
            "04-practice-and-attestation.md",
            "pack_manifest.json",
        ):
            _expect((pack_dir / req_file).is_file(), f"Missing pack file: {req_file}")

    return {
        "routing": routing_summary,
        "frozen_core_intact": True,
        "falsify_first_dry_run": "FALSIFIED_0_LEAN_SPENT",
        "prove_pause_resume_dry_run": "PROVED_IDEMPOTENT_8_OF_8_STAGES",
    }


def _expect_raises(
    exc_types: type[Exception] | tuple[type[Exception], ...],
    substr: str,
    label: str,
    fn: Any,
) -> None:
    try:
        fn()
    except exc_types as exc:
        msg = str(exc)
        _expect(
            substr.lower() in msg.lower(),
            f"Self-test '{label}' raised {type(exc).__name__} with unexpected message: {msg}",
        )
        return
    raise DiscoveryVerificationError(f"Self-test '{label}' was NOT rejected")


def run_self_test() -> int:
    """Negative self-tests (10/10 controls, zero `assert`, works under `-B` and `-B -O`)."""
    # 1. Self-acceptance (author_family == reviewer_family) MUST fail
    _expect_raises(
        RoutingPolicyError,
        "self-acceptance forbidden",
        "self-acceptance-same-family",
        lambda: validate_review_separation(MODEL_GEMINI_4_NEON, MODEL_GEMINI_4_NEON),
    )

    # 2. Family spoofing to bypass self-acceptance MUST fail
    spoofed = ModelSpec(
        provider="google",
        model="gemini-4-neon",
        reasoning_level="high",
        family="spoofed-independent",
    )
    _expect_raises(
        RoutingPolicyError,
        "family mismatch",
        "family-spoofing-bypass",
        lambda: validate_review_separation(MODEL_GEMINI_4_NEON, spoofed),
    )

    # 3. Banned `zcode` provider/model MUST fail
    zcode_spec = ModelSpec(
        provider="zcode",
        model="zcode-pro",
        reasoning_level="medium",
        family="zcode",
    )
    _expect_raises(
        RoutingPolicyError,
        "zcode",
        "banned-zcode",
        lambda: validate_model_spec(zcode_spec, role="engineering"),
    )

    # 4. Non-DeepSeek model under `opencode-go` MUST fail
    non_ds = ModelSpec(
        provider="opencode-go",
        model="qwen-2.5-coder",
        reasoning_level="medium",
        family="openai",
    )
    _expect_raises(
        RoutingPolicyError,
        "deepseek-only",
        "opencode-go-non-deepseek",
        lambda: validate_model_spec(non_ds, role="engineering"),
    )

    # 5. Surgical `opus-5.5` without trigger/quota AND rogue executor payload smuggle MUST fail
    _expect_raises(
        RoutingPolicyError,
        "surgical_trigger",
        "unauthorized-surgical-opus",
        lambda: validate_review_separation(
            MODEL_GEMINI_4_NEON,
            MODEL_OPUS_5_5_SURGICAL,
            surgical_trigger=False,
            opus_quota_remaining=0,
        ),
    )

    class _RogueOpusSmuggleExecutor(OfflineMockExecutor):
        def audit_semantic_alignment(
            self,
            conjecture: dict[str, Any],
            lean_verdict: dict[str, Any],
            author_route: ModelSpec,
            reviewer_route: ModelSpec,
            should_stop: Any,
        ) -> dict[str, Any]:
            res = super().audit_semantic_alignment(
                conjecture, lean_verdict, author_route, reviewer_route, should_stop
            )
            res["reviewer_route"] = MODEL_OPUS_5_5_SURGICAL.to_dict()
            return res

    with tempfile.TemporaryDirectory(prefix="aro-r12-opus-smuggle-") as tmp:
        loop_smuggle = DiscoveryLoop(
            pathlib.Path(tmp),
            executor=_RogueOpusSmuggleExecutor(scenario="prove"),
            requested_node_id="conj-o4-closure-scheduling",
            surgical_opus=True,
            opus_quota=0,
        )
        _expect_raises(
            RoutingPolicyError,
            "does not match router-assigned reviewer",
            "rogue-executor-opus-quota-bypass",
            loop_smuggle.run,
        )
        st_smuggle = StateStore(pathlib.Path(tmp)).load()
        _expect(
            st_smuggle.status == "FAILED",
            f"Expected FAILED on opus smuggle, got {st_smuggle.status!r}",
        )

    # 6. Promotion blocked when Lean 4 has `sorry` (even with LLM approval)
    with tempfile.TemporaryDirectory(prefix="aro-r12-sorry-") as tmp:
        loop = DiscoveryLoop(
            pathlib.Path(tmp),
            executor=OfflineMockExecutor(scenario="prove", inject_sorry=True),
            requested_node_id="conj-o4-closure-scheduling",
        )
        _expect_raises(
            FormalGateViolationError,
            "lean_verified",
            "lean-sorry-blocks-promotion",
            loop.run,
        )
        st = StateStore(pathlib.Path(tmp)).load()
        _expect(st.status == "FAILED", f"Expected FAILED on sorry, got {st.status!r}")

    # 7. Promotion blocked when Lean 4 uses custom axiom (direct gate + pipeline)
    _expect_raises(
        FormalGateViolationError,
        "custom axioms",
        "lean-custom-axiom-blocks-promotion",
        lambda: validate_formal_kernel_verdict(
            {
                "lean_verified": True,
                "sorry_count": 0,
                "frozen_core_intact": True,
                "custom_axioms": ["MyUnsafeAxiom"],
                "used_axioms": ["propext", "MyUnsafeAxiom"],
                "verified_decls": ["AroProofs.Discovery.fake"],
            }
        ),
    )

    # 8. Promotion blocked when SEMANTIC_ALIGNMENT_AUDIT fails
    with tempfile.TemporaryDirectory(prefix="aro-r12-align-") as tmp:
        loop = DiscoveryLoop(
            pathlib.Path(tmp),
            executor=OfflineMockExecutor(scenario="prove", inject_alignment_fail=True),
            requested_node_id="conj-o4-closure-scheduling",
        )
        _expect_raises(
            FormalGateViolationError,
            "semantic alignment audit rejected",
            "alignment-fail-blocks-promotion",
            loop.run,
        )
        st = StateStore(pathlib.Path(tmp)).load()
        _expect(st.status == "FAILED", f"Expected FAILED on alignment fail, got {st.status!r}")

    # 9. Corrupted / tampered state file MUST fail closed
    with tempfile.TemporaryDirectory(prefix="aro-r12-corrupt-") as tmp:
        sdir = pathlib.Path(tmp)
        loop = DiscoveryLoop(sdir, requested_node_id="conj-o4-closure-scheduling")
        loop.step()
        state_file = sdir / STATE_FILENAME
        raw = json.loads(state_file.read_text(encoding="utf-8"))
        raw["status"] = "PROVED"  # tamper without updating checksum
        state_file.write_text(json.dumps(raw), encoding="utf-8")
        _expect_raises(
            DiscoveryStateError,
            "checksum mismatch",
            "tampered-state-checksum",
            lambda: StateStore(sdir).load(),
        )
        state_file.write_text("{truncated json", encoding="utf-8")
        _expect_raises(
            DiscoveryStateError,
            "corrupted discovery state",
            "truncated-state-json",
            lambda: StateStore(sdir).load(),
        )

    # 10. Stale schema_version and stale atlas_sha256 MUST fail closed
    with tempfile.TemporaryDirectory(prefix="aro-r12-stale-") as tmp:
        sdir = pathlib.Path(tmp)
        loop = DiscoveryLoop(sdir, requested_node_id="conj-o4-closure-scheduling")
        loop.step()
        # Atlas changed underneath in-flight state
        _expect_raises(
            DiscoveryStateError,
            "atlas_sha256 mismatch",
            "stale-atlas-sha256",
            lambda: StateStore(sdir).load(expected_atlas_sha256="0" * 64),
        )
        # Incompatible schema_version
        state_file = sdir / STATE_FILENAME
        raw = json.loads(state_file.read_text(encoding="utf-8"))
        raw["schema_version"] = 99
        state_file.write_text(json.dumps(raw), encoding="utf-8")
        _expect_raises(
            DiscoveryStateError,
            "schema_version",
            "stale-schema-version",
            lambda: StateStore(sdir).load(),
        )

    print(
        "DISCOVERY VERIFIER SELF-TEST OK: 10/10 negative controls rejected "
        "(self-acceptance / family-spoofing / banned zcode / non-DeepSeek opencode-go / "
        "unauthorized opus-5.5 / Lean sorry / custom Lean axiom / failed semantic alignment / "
        "corrupted+tampered state / stale schema+Atlas)"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic verifier for R12 Long-Horizon Discovery Loop (#1275)."
    )
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        if args.self_test:
            return run_self_test()
        summary = verify_discovery_pipeline(REPO_ROOT)
    except (
        DiscoveryVerificationError,
        DiscoveryStateError,
        RoutingPolicyError,
        FormalGateViolationError,
        OSError,
    ) as exc:
        print(f"DISCOVERY VERIFICATION FAILED: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({"status": "ok", **summary}, ensure_ascii=False, indent=2))
    else:
        print(
            f"DISCOVERY LOOP VERIFY OK: {summary['routing']['stages']}/8 stages routed "
            f"(creative={summary['routing']['creative_math_primary']}, "
            f"eng={summary['routing']['engineering_primary']}, "
            f"audit={summary['routing']['alignment_primary']}), "
            "frozen core intact, FALSIFY_FIRST (0 Lean spent) & PROVE pause/resume OK"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
