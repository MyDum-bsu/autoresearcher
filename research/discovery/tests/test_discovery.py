"""100% offline unit & CLI integration tests for R12 Long-Horizon Discovery Loop (#1275)."""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

from research.discovery import PIPELINE_STAGES
from research.discovery.loop import (
    REPO_ROOT,
    DiscoveryLoop,
    OfflineMockExecutor,
)
from research.discovery.routing import (
    MODEL_GEMINI_4_NEON,
    MODEL_OPENCODE_DEEPSEEK_R1,
    MODEL_OPUS_5_5_SURGICAL,
    MODEL_PI_SOL,
    MODEL_SWE_2_HIGH,
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
from research.discovery.state import (
    STATE_FILENAME,
    DiscoveryStateError,
    StateStore,
    compute_state_checksum,
    write_kill_switch,
)


class TestRoutingPolicy(unittest.TestCase):
    def test_default_routing_matrix_is_complete_and_valid(self) -> None:
        summary = validate_routing_matrix(STAGE_ROUTING_MATRIX)
        self.assertEqual(summary["stages"], len(PIPELINE_STAGES))
        self.assertEqual(summary["creative_math_primary"], "google/gemini-4-neon")
        self.assertEqual(summary["engineering_primary"], "pi/sol")
        self.assertEqual(summary["alignment_primary"], "pi/sol")

    def test_engineering_allowed_models_and_bans(self) -> None:
        for spec in (MODEL_PI_SOL, MODEL_OPENCODE_DEEPSEEK_R1, MODEL_SWE_2_HIGH):
            validate_model_spec(spec, role="engineering")

        # zcode banned everywhere
        for bad_prov, bad_mod, bad_fam in (
            ("zcode", "zcode-1", "zcode"),
            ("opencode-go", "deepseek-zcode", "deepseek"),
        ):
            with self.assertRaises(RoutingPolicyError):
                validate_model_spec(
                    ModelSpec(
                        provider=bad_prov,
                        model=bad_mod,
                        reasoning_level="medium",
                        family=bad_fam,
                    ),
                    role="engineering",
                )

        # opencode-go strictly DeepSeek-only
        with self.assertRaises(RoutingPolicyError):
            validate_model_spec(
                ModelSpec(
                    provider="opencode-go",
                    model="glm-4.5",
                    reasoning_level="medium",
                    family="deepseek",
                ),
                role="engineering",
            )

    def test_cross_family_review_and_surgical_opus_guard(self) -> None:
        # Neon author -> pi/sol reviewer by default
        rev_default = select_reviewer_route(MODEL_GEMINI_4_NEON)
        self.assertEqual(rev_default.canonical_id, "pi/sol")
        self.assertNotEqual(rev_default.family, MODEL_GEMINI_4_NEON.family)

        # Non-Neon author -> Neon (high) reviewer
        rev_for_pi = select_reviewer_route(MODEL_PI_SOL)
        self.assertEqual(rev_for_pi.canonical_id, "google/gemini-4-neon")

        # Surgical opus-5.5 permitted ONLY when explicitly triggered AND quota > 0
        rev_opus = select_reviewer_route(
            MODEL_GEMINI_4_NEON, surgical_trigger=True, opus_quota_remaining=2
        )
        self.assertEqual(rev_opus.canonical_id, "anthropic/opus-5.5")

        with self.assertRaises(RoutingPolicyError):
            select_reviewer_route(
                MODEL_GEMINI_4_NEON,
                surgical_trigger=True,
                opus_quota_remaining=0,
                prefer_surgical_opus=True,
            )
        with self.assertRaises(RoutingPolicyError):
            select_reviewer_route(
                MODEL_GEMINI_4_NEON,
                surgical_trigger=False,
                opus_quota_remaining=5,
                prefer_surgical_opus=True,
            )

        # Rogue / low-reasoning model forbidden for semantic alignment audit
        with self.assertRaises(RoutingPolicyError):
            validate_model_spec(
                ModelSpec(
                    provider="openai",
                    model="gpt-4o-mini",
                    reasoning_level="low",
                    family="openai",
                ),
                role="semantic_alignment_audit",
            )

        # Self-acceptance forbidden
        with self.assertRaises(RoutingPolicyError):
            validate_review_separation(MODEL_GEMINI_4_NEON, MODEL_GEMINI_4_NEON)
        with self.assertRaises(RoutingPolicyError):
            validate_review_separation(
                MODEL_OPUS_5_5_SURGICAL,
                MODEL_OPUS_5_5_SURGICAL,
                surgical_trigger=True,
                opus_quota_remaining=1,
            )

    def test_formal_kernel_gate_cannot_be_bypassed_by_llm(self) -> None:
        with self.assertRaises(FormalGateViolationError):
            validate_formal_kernel_verdict(None)
        with self.assertRaises(FormalGateViolationError):
            validate_formal_kernel_verdict(
                {
                    "lean_verified": True,
                    "sorry_count": 1,
                    "frozen_core_intact": True,
                    "custom_axioms": [],
                    "used_axioms": ["propext"],
                    "verified_decls": ["AroProofs.Discovery.a"],
                }
            )
        with self.assertRaises(FormalGateViolationError):
            validate_formal_kernel_verdict(
                {
                    "lean_verified": True,
                    "sorry_count": 0,
                    "frozen_core_intact": False,
                    "custom_axioms": [],
                    "used_axioms": ["propext"],
                    "verified_decls": ["AroProofs.Discovery.a"],
                }
            )


class TestDiscoveryLoopWorkflows(unittest.TestCase):
    def test_falsify_first_terminates_early_with_counterexample_and_zero_lean(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-falsify-") as tmp:
            sdir = pathlib.Path(tmp)
            loop = DiscoveryLoop(
                sdir,
                scenario="falsify",
                requested_node_id="conj-o1-adr-exactness-char",
            )
            st = loop.run()
            self.assertEqual(st.status, "FALSIFIED")
            self.assertIsNone(st.current_stage)
            self.assertIsNotNone(st.counterexample)
            self.assertEqual(st.counterexample["battery_case"], "T2")
            self.assertEqual(
                st.falsification_result["engine"],
                "verification.falsifiers.battery_t1_t7.run_t2",
            )
            self.assertEqual(st.stage_executions.get("LEAN4_BLUEPRINT_VERIFY", 0), 0)
            self.assertEqual(st.stage_executions.get("SUBGOAL_DECOMPOSITION", 0), 0)
            ce_path = pathlib.Path(str(st.counterexample["artifact_path"]))
            self.assertTrue(ce_path.is_file())
            # Calling step() after terminal state is a strict no-op
            st2 = loop.step()
            self.assertEqual(st2.status, "FALSIFIED")
            self.assertEqual(st2.stage_executions, st.stage_executions)

    def test_prove_cycle_with_pause_stop_signal_and_idempotent_resume(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-prove-") as tmp:
            sdir = pathlib.Path(tmp)
            loop = DiscoveryLoop(
                sdir,
                scenario="prove",
                requested_node_id="conj-o4-closure-scheduling",
            )
            # Run first 4 stages up to FALSIFY_FIRST
            st_mid = loop.run(max_steps=4)
            self.assertEqual(st_mid.status, "RUNNING")
            self.assertEqual(st_mid.current_stage, "SUBGOAL_DECOMPOSITION")

            # Drop STOP kill-switch file directly on disk (simulating external CTO/owner stop)
            write_kill_switch(sdir, reason="owner_overnight_stop", hard_stop=True)
            st_stopped = loop.step()
            self.assertEqual(st_stopped.status, "PAUSED")
            self.assertEqual(st_stopped.current_stage, "SUBGOAL_DECOMPOSITION")
            self.assertIn("STOP:owner_overnight_stop", str(st_stopped.pause_reason))

            # Resume and complete all remaining stages
            loop.resume()
            st_final = loop.run()
            self.assertEqual(st_final.status, "PROVED")
            self.assertEqual(st_final.completed_stages, list(PIPELINE_STAGES))
            for stage in PIPELINE_STAGES:
                self.assertEqual(st_final.stage_executions[stage], 1)
            self.assertEqual(st_final.learn_pack["attestation_status"], "unattested_draft")

    def test_mid_subgoal_pause_preserves_partial_lemmas_and_resumes_cleanly(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-mid-pause-") as tmp:
            sdir = pathlib.Path(tmp)
            exec_pause = OfflineMockExecutor(scenario="prove", inject_mid_subgoal_pause_dir=sdir)
            loop = DiscoveryLoop(
                sdir,
                executor=exec_pause,
                requested_node_id="conj-o4-closure-scheduling",
            )
            st_paused = loop.run()
            self.assertEqual(st_paused.status, "PAUSED")
            self.assertEqual(st_paused.current_stage, "SUBGOAL_DECOMPOSITION")
            # Subgoal 1 & lemma 1 already persisted before pause triggered before subgoal 2
            self.assertEqual(len(st_paused.subgoals), 1)
            self.assertEqual(len(st_paused.lemmas), 1)

            # Resume in new DiscoveryLoop instance: preserves lemma 1 and finishes lemmas 2 & 3
            loop2 = DiscoveryLoop(
                sdir,
                executor=OfflineMockExecutor(scenario="prove"),
                requested_node_id="conj-o4-closure-scheduling",
            )
            loop2.resume()
            st_done = loop2.run()
            self.assertEqual(st_done.status, "PROVED")
            self.assertEqual(len(st_done.subgoals), 3)
            self.assertEqual(len(st_done.lemmas), 3)
            self.assertTrue(all(lm["sorry_free"] for lm in st_done.lemmas))

    def test_surgical_opus_consumes_quota_during_alignment_audit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-opus-") as tmp:
            sdir = pathlib.Path(tmp)
            loop = DiscoveryLoop(
                sdir,
                scenario="prove",
                requested_node_id="conj-o4-closure-scheduling",
                surgical_opus=True,
                opus_quota=1,
            )
            st = loop.run()
            self.assertEqual(st.status, "PROVED")
            self.assertEqual(st.opus_quota_remaining, 0)
            self.assertEqual(
                st.alignment_verdict["reviewer_route"]["provider"],
                "anthropic",
            )
            self.assertEqual(
                st.alignment_verdict["reviewer_route"]["model"],
                "opus-5.5",
            )

    def test_state_store_rejects_tampered_and_stale_files(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-state-") as tmp:
            sdir = pathlib.Path(tmp)
            loop = DiscoveryLoop(sdir, requested_node_id="conj-o4-closure-scheduling")
            loop.step()
            store = StateStore(sdir)
            sfile = sdir / STATE_FILENAME

            # Tampered state field without re-signing checksum
            raw = json.loads(sfile.read_text(encoding="utf-8"))
            raw["status"] = "PROVED"
            sfile.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(DiscoveryStateError):
                store.load()

            # Valid checksum but stale updated_at exceeding max_age_seconds
            raw["status"] = "RUNNING"
            raw["updated_at"] = "2020-01-01T00:00:00+00:00"
            raw["state_checksum"] = compute_state_checksum(raw)
            sfile.write_text(json.dumps(raw), encoding="utf-8")
            with self.assertRaises(DiscoveryStateError):
                store.load(max_age_seconds=60)

            # Active status (RUNNING / PAUSED) with current_stage=None MUST fail closed
            for active_status in ("RUNNING", "PAUSED"):
                raw_null = json.loads(sfile.read_text(encoding="utf-8"))
                raw_null["status"] = active_status
                raw_null["current_stage"] = None
                raw_null["updated_at"] = "2026-11-23T00:00:00+00:00"
                raw_null["state_checksum"] = compute_state_checksum(raw_null)
                sfile.write_text(json.dumps(raw_null), encoding="utf-8")
                with self.assertRaises(DiscoveryStateError):
                    store.load()

    def test_loop_blocks_opus_smuggle_at_zero_quota_and_deduplicates_subgoals(self) -> None:
        class RogueOpusExecutor(OfflineMockExecutor):
            def audit_semantic_alignment(
                self,
                conjecture: dict,
                lean_verdict: dict,
                author_route: ModelSpec,
                reviewer_route: ModelSpec,
                should_stop: object,
            ) -> dict:
                res = super().audit_semantic_alignment(
                    conjecture, lean_verdict, author_route, reviewer_route, should_stop  # type: ignore[arg-type]
                )
                # Attempt to smuggle opus-5.5 despite opus_quota=0
                res["reviewer_route"] = MODEL_OPUS_5_5_SURGICAL.to_dict()
                return res

        with tempfile.TemporaryDirectory(prefix="aro-test-smuggle-") as tmp:
            loop = DiscoveryLoop(
                pathlib.Path(tmp),
                executor=RogueOpusExecutor(scenario="prove"),
                requested_node_id="conj-o4-closure-scheduling",
                surgical_opus=True,
                opus_quota=0,
            )
            with self.assertRaises(RoutingPolicyError):
                loop.run()
            st = StateStore(pathlib.Path(tmp)).load()
            self.assertEqual(st.status, "FAILED")
            self.assertEqual(st.opus_quota_used, 0)

        # Deduplication in loop._execute_stage protects any naive executor returning duplicates
        class DuplicateSubgoalExecutor(OfflineMockExecutor):
            def decompose_subgoals(
                self,
                conjecture: dict,
                state: object,
                route: ModelSpec,
                should_stop: object,
            ) -> tuple[list[dict], list[dict]]:
                sgs, lms = super().decompose_subgoals(
                    conjecture, state, route, should_stop  # type: ignore[arg-type]
                )
                return sgs + sgs[:2], lms + lms[:2]

        with tempfile.TemporaryDirectory(prefix="aro-test-dedup-") as tmp:
            loop_dup = DiscoveryLoop(
                pathlib.Path(tmp),
                executor=DuplicateSubgoalExecutor(scenario="prove"),
                requested_node_id="conj-o4-closure-scheduling",
            )
            st_done = loop_dup.run()
            self.assertEqual(st_done.status, "PROVED")
            self.assertEqual(len(st_done.subgoals), 3)
            self.assertEqual(len(st_done.lemmas), 3)

    def test_cli_step_pause_status_resume_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aro-test-cli-") as tmp:
            base = [
                sys.executable,
                "-B",
                "-m",
                "research.discovery.loop",
                "--state-dir",
                tmp,
                "--node-id",
                "conj-o4-closure-scheduling",
                "--json",
            ]
            r_step = subprocess.run(
                [*base, "step"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
            )
            self.assertEqual(json.loads(r_step.stdout)["completed_stages"], ["SELECT_OPEN_NODE"])

            r_pause = subprocess.run(
                [*base, "--reason", "cli_pause_test", "pause"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(json.loads(r_pause.stdout)["status"], "PAUSED")

            r_status = subprocess.run(
                [*base, "status"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
            )
            st_data = json.loads(r_status.stdout)
            self.assertEqual(st_data["status"], "PAUSED")
            self.assertTrue(st_data["kill_switch_active"])

            r_resume = subprocess.run(
                [*base, "resume"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
            )
            self.assertEqual(json.loads(r_resume.stdout)["status"], "RUNNING")

            r_run = subprocess.run(
                [*base, "run"], cwd=REPO_ROOT, capture_output=True, text=True, check=True
            )
            done_data = json.loads(r_run.stdout)
            self.assertEqual(done_data["status"], "PROVED")
            self.assertEqual(done_data["completed_stages"], list(PIPELINE_STAGES))


if __name__ == "__main__":
    unittest.main()
