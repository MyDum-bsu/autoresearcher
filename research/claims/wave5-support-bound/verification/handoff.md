# Stage B targeted verification handoff

Disposition: **partial verification; candidate retained for independent criticism**. The universal policy-to-scalar reduction is written, not formally checked. No scientific success, novelty, attestation or status promotion is asserted; goalAchieved=false pending coordinator inspection.

The independent exact implementation reproduced the four declared support calculations, including exact zero defect at r104 for both coefficient variants and exact M0 primal-dual equality with both terminal strip sides satisfied. All 16 frozen invalid numerical controls were rejected. Normal and optimized executions returned 0 with byte-identical stdout. These finite checks do not constitute a checked general theorem.

## Frozen obligation and mathematical audit

`contract.md` freezes Astra's original statement, two models, r67/r104 and positive/invalid control inventory before arithmetic. `artifacts/goal/wave-5/verification/parents.json` freezes 11 parent hashes before computation. No claim amendment, new scientific case, r103 run, recourse optimization, or repair loop was undertaken.

`proof.md:5` onwards states quantifiers and control/information domains. Its bound-direction audit retains both terminal strip sides, independently attainable continuous-box extrema and the same fixed prefix across all tests. The suffix is selected from current state before future independent disturbances. Necessary lower-strip slack is dx+px-L-Sx+Hx; necessary upper-strip slack is H-Sx+Hx-dx-px; reward slack is dy+py+Hy-Sy-q. The independent symbolic identity is

D0+Delta-q = reward_slack + lambda*lower_slack + mu*upper_slack + prefix_support_slack.

All terms are nonnegative under the explicitly written premises. A different prefix disturbance may be used for each necessary condition; the proof neither combines those disturbances into one trajectory nor reveals history. Constant open-loop maps give V0<=Vr, and J<=V0 implies Vr-V0<=D0+Delta-J in the correct direction. The support triangle inequality gives Delta>=0. Exact equality Vr=V0=J follows from the proposed general reduction plus the checked identities J=D0 and Delta=0. It is not inferred from decimal overlap.

SymPy 1.14.0 checked the universal polynomial slack identity and triangle-defect decomposition, and rejected a wrong upper-slack sign. It did not verify the order/support premises or their derivation from arbitrary policies. Installed Lean reports 4.35.0-rc2; compiled mathlib dependencies were absent at the inspected project locations. No build/download/toolchain change or comparator was attempted. Thus the full general theorem remains a proposal under the original goal's checker-backed-proof requirement. This is an explicit coverage limit, not a substitution of finite cases for a proof.

## Exact finite results

`check.py` uses forward repeated matrix-vector powers, independently of M0's backward adjoint builder. It does not import or invoke M0 or Astra code. It derives A^k B and A^k E separately, computes A^120 x0, checks a complete chronological replay, every control bound, all independent-box supports, both terminal strip sides, nonnegative multipliers, claimed reward, and exact primal-dual equality. It then computes suffix supports and Delta. The mathematical reduction, Fraction runtime, input transcription and old witness data are not algorithmically independent in every respect; only the new finite arithmetic route is independent of the old builders/checkers.

| Exact model | r | J display only | Delta display only | Exact Delta=0 |
|---|---:|---:|---:|---|
| printed | 67 | 1.4957100981243105 | 1.6272285823887336 | no |
| printed | 104 | 1.4957100981243105 | 0 | yes |
| reconstructed decimal | 67 | 1.5011019893820279 | 1.6324558241460756 | no |
| reconstructed decimal | 104 | 1.5011019893820279 | 0 | yes |

Every row has exact rational J=D0. The robust lower endpoint is exactly 2; upper slack against 10 is positive, approximately 0.16464180039513004 for printed and 0.15877238388369014 for reconstructed decimal. Exact fractions, multipliers, endpoints and all outputs are in `check.stdout.json`. No floating-point comparison decides a check. Both multipliers on the upper strip are exactly zero; the witnesses still satisfy that strip side.

The invalid inventory comprises eight controls per model: objective +1, an out-of-box control, a negative lower multiplier, changed disturbance radius with stale support, tightened lower strip above the actual robust lower endpoint, tightened upper strip below its actual robust upper endpoint, a false r67 zero-defect assertion, and a reversed final r104 favorable-corner coordinate. Each arithmetic corruption is rejected for its specified reason. The strip/noise mutations deliberately exercise the mathematical predicate on in-memory copies, not a general input parser; frozen parent files remain untouched. A seventeenth invalid observation is the symbolic wrong-upper-slack-sign rejection, reported separately from the 16 finite controls.

Astra's r67 corner-reversal test begins with a corner that already fails the common-favorable predicate. That is not a discriminating reversal control. Stage B checks that the unmodified r104 corner is favorable before reversing its nonzero final component. This finding does not refute the bound or reinterpret positive r67 Delta as strict information gain.

## Actual evidence and commands

Working root and branch were verified as `<workspace>/aro-discovery-campaign`, `task/aro-discovery-k4t-campaign`, initially and before writes. New deliverables are restricted to the assigned two verification directories.

Executed from that root, with subprocess TMPDIR/TMP/TEMP pointing to `artifacts/goal/wave-5/verification/scratch`:

- `timeout 120 python3 -B goal/wave-5/verification/check.py`: exit 0; four exact rows, 16 rejected invalid controls, symbolic identities and wrong-sign control.
- `timeout 120 python3 -B -O goal/wave-5/verification/check.py`: exit 0; same observations.
- `cmp artifacts/goal/wave-5/verification/check.stdout.json artifacts/goal/wave-5/verification/check-optimized.stdout.json`: exit 0. Matching `.stderr` and `.exit` files preserve raw process observations.
- A separate Python -B binding/integrity check produced `binding-and-integrity.json`: all 11 frozen parents unchanged; both canonical input digests equal their certificate input_sha256 and coefficient identities match. It records Python 3.12.3 and code/proof hashes.
- `timeout 15 ruff check --no-cache goal/wave-5/verification/check.py`: exit 1, **18 style findings**. `ruff format --check --no-cache` also exits 1. No formatting repair was attempted after the scientific checks; both failures remain recorded.
- `timeout 20 ripwire goal/wave-5/verification --quality-delta --legend=compact`: exit 1, no local baseline or usable git HEAD for that new directory. This is unavailable quality-delta evidence, not a pass. No artificial baseline was created.
- Technical-style lint on `proof.md`: exit 1, two passive-construction flags at lines 71 and 77. Both describe preserved scope/provenance and were retained after manual review.

Raw stdout/stderr/exit evidence for these tools is in `artifacts/goal/wave-5/verification/`. Lint failures do not change exact arithmetic outputs, but this deliverable is not lint-clean. The new checker is a fixed-input research artifact, not a general validated parser or production judge.

## Source inspection and remaining authority

Read the wave-5 specification and original first-success goal in full, FOUNDATION and AGENTS, applicable session/literature/oracle/logika/style/worker instructions, actual Astra contract/derivation/probe/handoff/output, and wave-4 model/checker/input files. Directly inspected A4 physical pp4 and 12 rendered images. The source-native measurement/whole-block assumptions and the two-sided strip agree with this frozen contract; the reconstructed coefficient precision is still not author-confirmed. The A4 PDF hash is bound in parents.json. Task-local layout extractions of these two pages are preserved as A4-p4.txt and A4-p12.txt.

Not run: a fully mechanized general theorem, comparator, new scientific cases, broad source survey or original reference [14] novelty audit. Stage C owns the closest-source criticism. No necessity/cutoff theorem, r103 gain, source novelty, model consensus success or workflow-based scientific success is claimed. No previous artifact was repaired. No nested workers/workflows/objective, retries, fallback, installs, commits/pushes, tracker/live scientific writes or attestation were performed. One batched read had a missing lean-toolchain path; bounded path inspection established the actual layout. Initial batched reads produced harness-managed /tmp spills; required specification and foundation sections were subsequently read without relying on truncated text. This worktree is not OS isolation, and native provider retries/accounting/billing remain unknown.

Recommendation to coordinator: send the exact candidate and this coverage limitation to Stage C for original-reference comparison. Retain the exact r104 arithmetic as evidence even if the criterion is elementary or known. Do not mark the general theorem formally verified or the first-success goal achieved; any further formal work or continuation belongs to the coordinator.
