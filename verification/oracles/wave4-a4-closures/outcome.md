# Stage A outcome — bounded constructive A4 pilot

**First scientific success remains unachieved.** Concrete formulation, all-state policy construction and exact arithmetic certificates are available for independent Stage B and coordinator inspection. The result is classified as useful certified reproduction, not a contribution, novelty verdict, formal general theorem or attestation.

All four frozen scientific cases were attempted and have exact rational lower/upper certificates checked by the new solver-free checker. Three initial exact extractions failed after floating optimization; their original proposals, stdout/stderr and exit codes remain intact. A separately frozen, explicit prefix-viability correction extracted certificates from the same saved proposals, without rerunning any LP. No scientific case was skipped.

## Checked numerical enclosure

The following decimal intervals are rounded OUTWARD from the exact rational bounds in result.json and each certificate. They enclose the best guaranteed reward, conditional on the written finite-reduction/model correspondence argument in model-and-source.md. Nonzero gaps are not exact-optimum certificates.

| Exact coefficient input | Closure | Outward interval | Exact gap, display only | Vertices / LP rows / variables |
|---|---:|---|---:|---|
| printed | 67 | [2.905827967435, 2.905827967441] | 5.66798e-12 | 134 / 402 / 7170 |
| reconstructed decimal | 67 | [2.912639964467, 2.912639964474] | 5.40118e-12 | 134 / 402 / 7170 |
| printed | 104 | [1.495710098119, 1.495710098125] | 5.32014e-12 | 208 / 624 / 3433 |
| reconstructed decimal | 104 | [1.501101989375, 1.501101989383] | 6.22065e-12 | 208 / 624 / 3433 |

M0 open-loop exact certificates were regenerated and checked from wave-local readonly copies: printed reward displays 1.4957100981243105; reconstructed decimal displays 1.5011019893820279. The r104 intervals contain their respective open-loop optima. This is consistency within tight certified intervals, not an exact proof of equality or a claim about every closure time >=104. No closure-time sweep was performed.

## What is checked and what remains mathematical argument

The checker rebuilds terminal effects using M0 backward adjoints; the producer uses forward powers. For every supplied zonotope vertex it checks an explicit attainable prefix sign sequence. Each consecutive edge must be an exact supporting edge of the full continuous prefix zonotope, with strictly counterclockwise turns and distinct vertices. Every vertex suffix satisfies the exact control box, both robust terminal inequalities and the common reward floor. Exact suffix support covers the entire independent continuous future disturbance box.

The runnable state_to_block function accepts only measured current state and frozen policy. It subtracts the nominal closure state, propagates its offset to terminal coordinates and selects a suffix by deterministic fan-triangle interpolation. At vertices it returns the stored suffix; elsewhere it uses exact barycentric coordinates. Executed in-case tests cover every vertex, the center, one edge midpoint and the zero-prefix-disturbance measured-state interface. The universal interpolation/convexity justification is written out, not inferred from those finite tests. The necessity/sufficiency theorem and every-state argument have NOT been Lean-formalized or independently reviewed.

Upper bounds use nonnegative exact rational row weights normalized to unit reward coefficient. Any residual control stationarity is paid for by the exact control-box support ||M^T lambda||_1. Thus rounding dual weights cannot silently turn a tolerance into a certificate. All rational inequalities are checked without tolerances or assert statements. Float displays and solver success flags have no acceptance role.

## Source-native comparison

A4 physical pp2–6 match the information pattern: exact current-state observation, whole-block action choice, all independent per-time disturbance values. Pp11–12 explicitly allow outer-approximation reward degradation or continuation failure. Pp12–13 report approximate one-closure reward 2.913110 and a trajectory-based value 2.912640, with difference 4.7e-4. Fresh layout extractions, p12–13 coordinate-bearing extraction and original PDF hash are saved under the source directory.

The reconstructed-decimal r67 enclosure rounds to 2.912640 at six decimal places, agreeing with that reported trajectory value. Its difference below 2.913110 is approximately 0.00047003553. This is compatible with the paper's explicit approximation warning. It does not certify the authors' particular initial program, because that program and their computation were not supplied/reproduced, and reconstructed coefficients are inferred, not confirmed author data. The printed/reconstructed discrepancy was already known in M0 and is not a new contribution. Neither the exact polyhedral vertex reduction nor elementary interpolation is claimed as novel.

Nearest inspected primary source A4 already describes optimal blockwise control, closure feasibility and outer-approximation error; its references include earlier exact feedback methods and the prior single-closure article [14]. This wave did not settle a new literature delta. BT04 was not freshly audited here and is not used as an uninspected theorem premise. No generic vertex theorem or published error is claimed.

## Failure record and deliberate extraction change

Initial construct.py runs for printed-r67, reconstructed-r67 and printed-r104 exited 1 after saving successful numerical proposals. Rounded first-block controls placed a continuation-capacity boundary microscopically outside the exact feasible set. For printed-r67, the first diagnosed saturated suffix missed the lower slab by roughly 3.3e-12. No certificate was accepted at that point.

The new extract.py repairs the common first block before suffixes, enforcing exactly

`2+suffix_x_support+prefix_x_support-suffix_control_x_capacity <= d_x+C_pre*a <= 10-suffix_x_support-prefix_x_support+suffix_control_x_capacity`.

This condition is the necessary and sufficient interval for some suffix to meet the robust terminal x slab for every prefix x image, since suffix controls are a continuous symmetric box. It does not certify reward by itself. Subsequent per-vertex exact checking establishes the actual reward lower bound. extraction-contract.json binds the changed extractor and original frozen contract before extraction. Original construct.py and contract.json remain unchanged. Reconstructed-r104's initial extraction succeeded and was not overwritten. This is explicit certificate postprocessing, not an automatic optimization retry, provider fallback or hidden replacement of raw evidence.

## Executed verification and reproducibility

For each case C:

```sh
timeout 240 python3 -B goal/wave-4/check.py C --controls
timeout 240 python3 -B -O goal/wave-4/check.py C --controls
```

Each process exited 0. Each emitted one positive result and seven rejected controls: wrong future information, violated terminal row, false reward, negative multiplier, wrong input binding, wrong closure binding and missing vertex. There are 32 control results per Python mode, 64 total; normal/-O stdout bytes match in all four cases. Raw process streams and command/time/exit records are in artifacts/goal/wave-4/pilot/raw/. The printed-r67 initial shell commands and frozen-contract step are described in plan.md and this report; the later subprocess command arrays are machine-recorded. All calls were sequential, without workers nested inside this worker.

Original input canonical SHA256 identities: printed 154b1a0181c5a9f29bcc20d64bc111220cbb4193b3560387b543d2c31fe32602; reconstructed 77dca22ff207f2d7176fe103c2f38552c7a40e1d60cd39d10f1958bc06f1a869. Raw source/copied-dependency identities are in source/origin-sha256.txt. Source PDF SHA256 is 4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420. Original frozen file identity check found no mismatches. Environment: Python 3.12.3, scipy 1.17.1, numpy 2.5.2; solver HiGHS via installed scipy. The LP time limit was 60 seconds, subprocess limits 240 seconds; actual numerical LP times were about 0.05–0.06 seconds. Native provider retries/billing and exact Pi accounting are unknown; the instructional envelope was tracked manually, not mechanically enforced.

Rechecking existing certificates is readonly and needs only Python stdlib plus the wave-local M0 checker copy. Re-running generation in place is intentionally refused to preserve evidence. To reproduce floating proposals in another permitted destination, a coordinator must explicitly arrange new output paths; do not delete current folders or overwrite certificates. extract.py also refuses to overwrite an existing certificate.

## Additional full-path audit and focused diagnostics

Before execution, full_path_audit.py froze an additional positive diagnostic using only the existing four cases: the first minimum-reward certificate vertex and three full chronological disturbance paths per case (suffix x-min, x-max and y-min). Its source hash was saved first. `timeout 240 python3 -B goal/wave-4/full_path_audit.py` exited 0 for all 12 paths. The original recurrence was replayed from x0 through the nonzero prefix realization, then the actual state_to_block interface selected the certified suffix. Every path met the strip/reward; the y-min path attained the exact certificate lower bound. These executions supplement, rather than replace, the universal support argument. Raw streams are full-path.stdout/stderr; no extra scientific model or fixture was added.

`ruff check --no-cache --select E9,F63,F7,F82 goal/wave-4/construct.py goal/wave-4/extract.py goal/wave-4/check.py` exited 0, All checks passed. This is a focused correctness diagnostic, not a full repository style gate. Technical-style diagnostics exited 1: English report had two passages flagged (passive statement that no time sweep was performed; opening Not done), Russian briefing had one (opening Не выполнены). These passages explicitly disclose scope limitations and are retained after review. No style-linter green claim is made. Full Ruff/format and unrelated repository gates were not run because frozen computational sources must not be reformatted and the change is isolated to wave-local artifacts.

## Scope and handoff

New artifacts are only under goal/wave-4/, artifacts/goal/wave-4/pilot/ and reports/briefings/2026-11-13-goal-wave-4.md. No commits/pushes, live scientific state, task tracker mutation, corpus admission, attestation, installs/system changes, comparator or external-system tests occurred. M0 inputs and dependencies were copied readonly, not modified. Scratch is wave-local and no background process remains.

Not done: independent Stage B, formal universal proof, confirmation of original author coefficients/program, reproduction of the 203-normal approximation, novelty establishment, any additional scientific case or time-optimality claim. These omissions prevent scientific-success promotion. Recommendation: perform the authorized read-only Stage B on these concrete artifacts; if it confirms correspondence and arithmetic, retain this as a useful tightly certified reproduction rather than relabeling it a new contribution.
