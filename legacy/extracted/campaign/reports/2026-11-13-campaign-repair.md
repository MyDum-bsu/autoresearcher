# Campaign repair: bounded response to independent review F

Task: `aro-discovery-k4t`. Workspace: `<workspace>/aro-discovery-campaign`; branch: `task/aro-discovery-k4t-campaign`.

The three reported validator bypasses now have rejection regressions. Versioned D1/D2 checkers pass their frozen examples in normal and optimized Python, with stdout identical to the historical scientific outputs. The final focused Ruff and format observations pass. Final independent review, synthesis and terminal delivery acceptance remain outstanding.

General mathematical statements retain `unproved-sketch` status. This repair supplies no Lean proof, scientific attestation, semantic approval, novelty result, comparator readiness or causal comparison of research approaches.

## Repair boundary and preserved history

This is the single authorized repair pass on four concrete findings. No new research question, source acquisition, search, provider, installation, nested worker, tracker update, live scientific write, commit or push was performed. The root and branch were checked before edits. The active v2 contract, preserved v1, activation, phase records, scientific manifests, original scientific scripts and all original raw outputs were left unchanged.

The new scientific identities are:

- `research/baseline/checks/check_candidate_v2.py`, derived from `check_candidate.py`.
- `research/structured/checks/trajectory_check_v2.py`, derived from `trajectory_check.py`.
- `research/structured/checks/certificate_check_v2.py`, derived from `certificate_check.py`.

`artifacts/campaign/repair/adaptations.json` records the original identities; `artifact-inventory.json` in the same directory binds the repaired files and evidence. Original manifests continue to describe original scripts. Do not redirect an old scientific check ID to v2 bytes. New repair check IDs and separately bound adaptations are required in synthesis.

Pre-repair validator/test source reconstructions are retained as `artifacts/campaign/repair/*-before-repair.py`. They were reconstructed from the inspected original regions after the first edits, not captured by a pre-edit filesystem snapshot. The immutable original research scripts remain directly available. Earlier campaign failure outputs are not replaced by repair outputs.

## P1: original frozen obligations

`scripts/campaign_acceptance.py:frozen_obligations` expands the known B, D1, D2 and E producer schemas from fixed paths. It consumes the active contract's `conditional_inventory.claimed_experiments` policy. It requires every original declared check, candidate, input identity, output and bound execution input/output link. D1 subcases must match the original ordered case mapping. B additionally binds its pre-execution input inventory, its file identities, check IDs and declared targets. The separately frozen E timing control is included when present. Missing normal artifacts require the existing explicit unavailable/failure accounting; no directory glob supplies experimental obligations.

Every declared check's normalized inventory must bind its original producer manifest by SHA-256. B inventories must additionally bind `artifacts/campaign/tool-spike/frozen-inputs.json`. `artifacts/campaign/repair/frozen-delivery-inventory.json` is a schema-only projection containing 29 original check IDs and 98 files. It preserves original hashes and D1 subcases, rather than pretending the projection was frozen before the original experiments.

Regression coverage uses the real preserved manifests. It rejects the review's D1-manifest-only bundle, and analogous D2/E omissions. Adapter tests exercise B/D1/D2/E and the separate E timing manifest: positive original obligations, deleted declared check, deleted declared output, and substituted parent SHA-256. These test fixtures do not constitute scientific evidence.

Synthesis must use the new normalized inventory for the original scientific checks and B checks, preserving the original commands, inputs, raw streams and failures. B records must declare `declared_targets: ["Campaign.expected"]`; this is frozen target accounting, not a native comparator verdict. The normalized inventory does not change any historical disposition.

## P1: causal blocker chains

The validator traverses every unexecuted check's blocker chain and rejects self-reference and cycles. A chain must reach a saved executed observation. Each unexecuted record must carry nonempty `blocker_observations` entries with `check_id`, `stream` (`stdout` or `stderr`) and a literal nonempty `excerpt` occurring in that reachable executed record's bound raw stream. Existing command, stream and identity validation still applies to the executed leaf.

A `tested/adapted` mechanism must cite at least one actually executed passed check. An exclusively blocked/deferred/exhausted support set no longer represents a successful test. Partly tested mechanisms must still state their narrower scope; metadata cannot determine the scientific or causal meaning of a diagnostic.

Regressions cover a self-loop, a two-record cycle, missing causal observation, fabricated diagnostic, an executed failed observation supporting a blocked dependent, and an exclusively not-run mechanism support set. Synthesis must add literal causal diagnostic bindings for the historical comparator namespace failure; it must not describe the blocked controls as successful native rejections.

## P2: stage-to-phase identity

The fixed map is A→01-plan, B→05-tools, C→06-domain, D1→07-baseline, D2→08-structured, E→09-continuation, F-synthesis→13-synthesis. F-review accepts 10-review or 12-final-review, with the phase schema validated and the existing repair/recheck pairing preserved. Under unsafe C, blocked D1/D2/E link to 07-research-not-started. Tests reject cross-stage substitution for every stage, accept the final-review route, and preserve the unsafe-C route.

## P2: checker quality and dimensional rejection

The original D1 and D2 files remain historical frozen evidence, including their lint failures. Their active v2 adaptations use strict zip lengths, a nonambiguous lower-bound variable, sorted imports and formatting. The added `tests/campaign/test_repaired_dimensions.py` rejects dot/add mismatch, mismatched control boxes, inconsistent transition-vector lengths, unequal hard-row/bound counts and a malformed certificate row. The checks execute in both normal and optimized Python; validation does not depend on removable assertions.

The focused quality gate covers eleven active campaign-owned Python files: the nine prior active roles with three v2 replacements, plus the repair verification driver and dimension regressions. It excludes historical original research scripts and imported upstream files. A green active gate does not retroactively make the historical nine-file gate green.

## Executed verification and retained failures

All subprocesses inherited campaign-local TMPDIR/TMP/TEMP, bytecode suppression and campaign-local cache routing. `scripts/campaign_repair_verify.py` records commands, exits, raw stream hashes, byte comparisons and measured subprocess wall times in `artifacts/campaign/repair/verification.json`. It refuses to overwrite that observation file.

Executed commands include:

- `timeout 60 python3 [-O] -B -m unittest discover -s tests/campaign -p 'test_*.py'`: 34 tests pass in each mode.
- `timeout 60 python3 [-O] -B -m unittest discover -s pilot/baseline -p 'test_*.py'`: 7 tests pass in each mode.
- `timeout 60 python3 [-O] -B -m unittest discover -s pilot/checkers -p 'test_finite_*.py'`: 16 tests pass in each mode.
- `timeout 60 python3 [-O] -B research/baseline/checks/check_candidate_v2.py research/baseline/checks/candidate-v1.json`: exit 0; both stdout streams equal `research/baseline/checks/exact.stdout.json` byte for byte.
- `timeout 60 python3 [-O] -B research/structured/checks/trajectory_check_v2.py`: exit 0; both stdout streams equal the historical D2 trajectory output byte for byte.
- `timeout 60 python3 [-O] -B research/structured/checks/certificate_check_v2.py`: exit 0; both stdout streams equal the historical D2 certificate output byte for byte.
- Final `ruff check --no-cache --output-format concise` on the eleven active paths: exit 0, `All checks passed!`, retained as `ruff-final.stdout`/`.stderr`.
- `ruff format --check --no-cache` on the eleven paths: exit 0. A subsequent string-only line split in the certificate adaptation was separately checked by `format-final.*`; its normal/-O executions under `timeout 30` again returned 0 and byte-matched the historical scientific stdout (`certificate-final-{normal,optimized}.*`).
- `timeout 60 ripwire scripts --quality-delta --legend=compact`: exit 0. This is not a clean-code certificate: these untracked campaign files appear as new symbols relative to HEAD; the output reports new-symbol complexity/verbosity/parameter findings.
- `timeout 60 ripwire scripts --edit-check=validate_bundle --legend=compact`: exit 0, `new-symbol`, one caller and zero detected incompatible call sites. Git has no pre-campaign tracked baseline for this file.
- `git diff --check`: exit 0. Explicit UTF-8/newline/trailing-whitespace and JSON checks on repair-owned deliverables are recorded separately; Git alone does not cover untracked files.

The development test observation failed two assertions: the newly constructed failed-leaf fixture omitted its inventory case, and the unsafe-C regression expected the older error ordering. Both fixture defects were corrected without weakening production validation. The development Ruff observation reported twelve issues in the repair code/fixtures. The first full verification's Ruff observation then retained one E501 line-length failure; a string-only split fixed it. All these observations remain in `development-*`, `verification.json`, and `ruff.*`; the final passing quality output has a different path. No operational retry, fallback or scientific input adjustment was used.

## Containment and accounting limits

Subprocess temporary files stayed campaign-local. Two oversized instructional read batches nevertheless caused the harness to create `/tmp/pi-codemode-19227d7d74967444.txt` and `/tmp/pi-codemode-0dd7efc9e142d543.txt`. This violates complete host-write containment. The files were neither read nor deleted; local TMPDIR does not constrain the harness itself. No filesystem sandbox or fully enforced call ceiling is claimed.

Provider usage/billing, internal retries and complete worker wall time are unknown. Recorded subprocess wall times are narrower observations. No new private trial, human attestation or general mathematical proof was attempted. The general rank-one child remains unproved; finite stdout agreement establishes only the declared rational-instance checks.

## Handoff

The coordinator must retain original B/D1/D2/E check identities, attach the normalized frozen-parent links, add concrete blocker diagnostic bindings, and index the v2 repair observations separately. The independent final reviewer must assess the repaired findings, including the larger fail-closed schema surface and the active-versus-historical quality boundary. Only afterward should synthesis produce its five required deliverables. The coordinator alone persists 13-synthesis and then invokes terminal acceptance. This worker did not run that terminal command or mark any review finding independently resolved.
