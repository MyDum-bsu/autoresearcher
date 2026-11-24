# G1 engineering repair v1

G1 engineering integrity checks pass. Historical campaign delivery still fails, as it did before this work; its failure is preserved and freshly reproduced under a new ID. This is not a scientific success, a G2 independent review, a general mathematical proof or human attestation.

## Delivered and observed

- Root and branch verified before editing and again after verification: `<workspace>/aro-discovery-campaign`, `task/aro-discovery-k4t-campaign`.
- `checker_v1.py` reuses the immutable original validator and retains its complete contract, adding comparison of actual bytes, file-table hashes and normalized check output hashes with original B `outputs[].sha256`. No historical checker, manifest, output, contract or outcome was rewritten.
- `test_integrity_v1.py` reconstructs a full disposable B bundle with the actual original B specs and frozen inputs. The original validator accepts the positive bundle and a deliberately altered shared stdout after all four consuming checks are consistently rehashed. The new validator accepts the positive bundle and rejects that same mutation. Additional controls reject missing output, un-rehashed tampering and normalized check hash drift. The mutation occurs only in cleaned-up local fixtures.
- `historical-inventory-v1.json` binds 389 historical files; its SHA-256 is pinned in the goal checker. `evidence-index-v1.json` contains 413 file entries, 56 check records, all 13 real phase records, 8 stages, 6 source records, 3 scoped claims and 4 review records. All original producer obligations and historical failures remain present. Existing Astra files and its coordinator quality-failure evidence are included in the file inventory; Astra code was not adapted or relinted as new code.
- The original validator forbids hashing its own index path. The new index therefore binds the immutable historical index indirectly through the pinned historical inventory, not by violating or weakening that rule. The NEW index has no self-hash dependency.
- Missing original F per-process raw streams are explicitly unavailable history. Ten genuinely NEW G1 process executions have new IDs and saved raw stdout/stderr. These replay existing checking algorithms; they are independent executions from their authors, not a separate mathematical derivation, a new reviewer worker, historical observations or G2 review. General rank-one results remain `unproved-sketch`; finite evidence and source-derived reasoning retain their distinct scopes.

## Exact replay and verification

From the specified worktree:

```sh
cd <workspace>/aro-discovery-campaign
timeout 300 python3 -B goal/engineering/replay.py
timeout 30 python3 -O -B goal/engineering/checker_v1.py
git diff --check
```

Observed final replay: exit 0, `passed: true`, `errors: []`; optimized standalone checker: exit 0, `errors: []`; `git diff --check`: exit 0. The coordinator entrypoint resets the gate to incomplete before execution, verifies pinned historical identities, executes subprocesses and checks real exit codes/raw bytes, assembles the index, and executes all original validator obligations plus the new hash binding. It does not merely trust declared pass booleans. Commands, source identities, index identity and counts are saved in `gate.json`; individual commands and outcomes are in `executed-checks-v1.json`.

The final replay ran 21 subprocess checks:

- In EACH of normal and `-O` modes: 34 unchanged campaign tests, 7 baseline tests, 16 finite-checker tests and 4 new G1 regressions; 61 tests per mode, all successful.
- Ten scientific subprocesses: D1 exact construction, D2 trajectory and certificate routes, E rank-one boundary and hidden-suffix controls, each normal and optimized. All exited 0, stderr was empty and stdout matched the original frozen scientific output byte-for-byte. Positive and invalid controls belong to these existing fixed-instance checking programs; these executions do not establish general statements.
- Ruff check and format check on all four new Python files: exit 0.
- NEW `G1-historical-delivery-rejection`: actual original terminal validator exits 1 with `unbound present file: artifacts/campaign/phases/01-plan.json`. Expected rejection is positively checked, not relabeled as a historical successful delivery.

Final raw streams: `artifacts/goal/wave-1/engineering-v1/`. All 389 historical identities remained unchanged. No `delivery-*` scratch directories remained after tests.

## Development findings retained

The first local replay reached all subprocess checks but index assembly failed with `KeyError: 'E-hidden-suffix-control'`: timing-observation uses a distinct schema without `id`/`check_id`. It is now matched by its original `stdout_path`, without inventing an observation. An intermediate index then exposed the original self-index prohibition, a required report missing from the initial snapshot selection, and the missing causal evidence link for historical partial synthesis. The narrow correction preserves the historical index through the snapshot, includes the actual missing report, and uses the NEW observed historical terminal rejection as current delivery blocker evidence. It does not fabricate raw evidence for the historical synthesis KeyError.

A later replay passed index integrity but failed one new Ruff `SIM102` diagnostic. That new-code issue was corrected before final verification. Three development raw-stream sets remain under `artifacts/goal/wave-1/engineering-development-01/`, `engineering-development-02/` and `engineering-development-03/`; these are development executions, not accepted final evidence or provider retries. `development-findings-v1.json` records failures not captured as subprocess streams. No provider retry/fallback was requested; native retry behavior and actual provider billing remain unknown.

## Decisions and limits

Used a thin goal-local extension and schema-specific assembler rather than a new platform or a copy of the full validator. No Astra adaptation was necessary to repair B binding and deliver the campaign inventory. Its historical 20 Ruff findings and formatting failure remain historical failures.

For inherited unit tests, `TMPDIR/TMP/TEMP` points to the existing campaign-local `artifacts/campaign/tmp` because the unchanged fixture requires that exact location. Fixtures are disposable and cleaned up; all persistent new outputs are goal-specific. Python runs use `-B`; no global installs, commits/pushes, live scientific writes, attestation, nested workers, comparator calls, isolation bypasses or OS changes occurred. This worktree is not an OS sandbox. Oversized early documentation batches caused harness-managed `/tmp` spills, which were neither read nor removed; full host-write containment is not claimed.

Not done: G2 independent engineering review, source novelty audit, new mathematical development, general Lean proof, comparator recovery, scientific status promotion and human attestation. They are outside G1. Legitimately unavailable historical reviewer streams cannot be recovered by this repair. The old campaign's negative outcome and blocked comparator remain unchanged. Recommended next step: G2 read-only replay of the positive/shared-rehash regression and complete index, with its own newly saved review streams.
