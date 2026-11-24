# Stage A handoff

Disposition: concrete candidate for targeted verification; goalAchieved=false. No scientific success or novelty claim. Coordinator owns continuation.

The proposed certificate bounds the adaptive advantage by an open-loop primal-dual gap plus a suffix support defect. Both exact input variants have zero defect at r104 under their existing M0 multipliers. The reused exact checker accepts the full open-loop witnesses, including the upper strip. This supplies a precise route to exact r104 equality, conditional on checking the general derivation. It does not retroactively remove the wave-4 enclosure gaps.

## Verification obligation

Read `contract.md` and `derivation.md`. Establish the universal bound V_r<=D0+Delta for the stated independent continuous-box model and exact current-state/whole-suffix information pattern. In particular check the three separate necessary prefix inequalities and the sign of each weighted slack. Then independently recompute the two r104 zero defects and M0 witness feasibility/duality from pinned coefficients. Retain r67 as a nonzero-defect discriminator. No new cases or large recourse LP are needed.

The mathematical obligation is substantive enough to inspect because it would turn an overlapping enclosure into an exact statement about all admissible state policies. That does not establish a substantive novel contribution. Stage C must compare original A4 reference [14] and relevant static/adjustable control results; the mechanism may be known or elementary. If source coverage closes it, retain it as reconstruction.

## Delivered files and evidence

- `goal/wave-5/astra/plan.md`: approach and controls frozen before computation.
- `goal/wave-5/astra/contract.md`: class, formula, cases and invalid controls.
- `goal/wave-5/astra/derivation.md`: proposed proof, attacks, source anchors, observed finite scope.
- `goal/wave-5/astra/probe.py`: narrow exact support calculation; imports readonly M0 arithmetic.
- `artifacts/goal/wave-5/astra/probe.stdout.json`: exact fractions, M0 results, invalid-control results and parent SHA256 bindings.
- `artifacts/goal/wave-5/astra/probe-optimized.stdout.json`: byte-identical optimized execution.
- Matching `.stderr` and `.exit` files record actual process output and return codes.

Executed from `<workspace>/aro-discovery-campaign`:

`TMPDIR="$PWD/artifacts/goal/wave-5/astra/scratch" timeout 120 python3 -B goal/wave-5/astra/probe.py`

and the same command with `-O`. Both produced results; `cmp` reported identical stdout. Four rows report Delta>=0, two exact zero defects at r104, and four reversed-corner rejections. The corrupted M0 objective was rejected for each variant. These are finite checks using shared M0 code, not independent general proof evidence. Full commands' stdout/stderr were redirected to the named evidence files and process exit codes saved separately.

## Limits and preserved history

No r103 cases, optimization solver runs, recourse enumeration, Lean proof, comparator, source downloads, nested workers, automatic retries, provider fallback, installs, system changes, commits, live scientific writes or attestation. A broad directory lookup was bounded at 20 seconds and timed out; a subsequent narrower path lookup found the existing wave-4 M0 certificate wrappers. No scientific computation was retried after failure. A read requested offset 110 beyond a 105-line goal document; the final section was then read at offset 75. One batched read produced a harness-managed `/tmp` spill; the truncated required model and final goal section were read separately. Subprocess scratch was task-local; the worktree is not OS isolation.

The stage used one viability/support approach and its dual algebraic expression, within the two-approach limit. No task tracker or old artifact was written. Existing repository-wide untracked files predated this work and were not cleaned. Actual billing and provider-native retry behavior are unknown. No claim is made about source novelty or author coefficient precision.

Recommendation: perform the narrow proof/application check, then the original-source comparison. Stop with reconstruction if the condition is already covered; do not invent a stronger result or infer r103 gain from a failed sign condition.
