# E handoff: rank-one boundary continuation completed, with a style-check failure

Task `aro-discovery-k4t`, phase E. One engineering check failed: `E-style-reconstruction` exited 1 for the passive phrase “was performed” at `research/continuation/reconstruction.md:46`. Ruff check and format-check passed. The planned `E-style-timing-control` did not run because the verification sequence stopped at that finding. No retry, fallback or silent text repair occurred. Raw outputs and `verification.json` preserve the outcome. This is not a mathematical refutation. Final results/handoff style lint was not run during terminal reporting.

## Recovered obligation and actual new result

Initial mathematical inputs were ONLY `research/question.md`, `research/resource-manifest.json`, `research/structured/handoff.md`. Mandatory authority files were also read. Later the explicitly referenced structured check manifest was read as an evidence-schema example; predecessor derivation, scientific scripts/outputs/results, history, baseline answer and phase payload were not read. Full access log and limitations: `reconstruction.md`; identities: `input-identities.json` and `results.json`.

The handoff left `D2-C1-v1`: if the common residual hard/cost matrix L=D G has rational rank at most one, does pairwise compatibility inside a measured-state cell imply a common continuation?

**New limitation:** under the distinct-index meaning of “pairwise”, a singleton cell has no pair tests. An empty K_p therefore satisfies that premise vacuously. New exact dynamics-realizable examples show this at rank zero, rank one, and with one prefix containing two hidden suffixes. If “pairwise” includes self-pairs, the original wording already includes nonemptiness; do not claim to refute that reading.

**Explicit child `E-R1-child-v1`:** for a finite nonempty family K_p={b in a common nonempty bounded closed rational box V:L b<=d_p}, rank_Q(L)<=1, individual nonemptiness PLUS distinct-pair nonempty intersections imply joint nonempty intersection. Joint nonemptiness implies those premises. For cells with at least two prefixes the individual premise follows from pairs. Prefix feasibility already supplies it in the original comparison.

`derivation.md` supplies an elementary written argument: factor L=v ell, project V to a closed rational interval, convert each row to a lower/upper scalar bound with sign reversal and explicit zero-row rejection, use attained maximum lower/minimum upper to identify a contradictory singleton/pair if the joint interval is empty, then lift a rational scalar using convex interpolation between box extrema. Rank zero and singleton images are handled separately. This is `unproved-sketch`, NOT a Lean theorem or code-issued general mathematical verdict. Independent F review/formalization remains.

## New executed evidence, not D2 replay

`checks/manifest.json` was frozen before two executions of `checks/rank_one_check.py`; `checks/timing-manifest.json` separately froze the extra hidden-suffix control before execution. No original scientific input or code was modified after freezing.

Six fixed dynamics cases share T=2,r=1,n=d=1,m=2, x_1=0, H=-1,h=0,c=1,d0=0 and x_2=B_1 b+s. Standard box is [0,2]^2. Except rank-zero controls, B_1=(1,-1), t=b_1-b_2.

- Suffixes (-1,0,1), q=2: each individual and pair is feasible, joint t=1; rational action (3/2,1/2) yields terminal states (0,1,2).
- Same suffixes, q=1: all singletons feasible, first/third pair and joint infeasible, with actual hard/cost rows summing to 0<=-1. Rank one does not imply unconditional prefix/state losslessness.
- Singleton suffix -3,q=0: rank one, sole system empty from t>=3 versus box t<=2; distinct-pair premise vacuous.
- B_1=0,s=-1,q=0: rank-zero singleton empty; hard row 0<=-1.
- B_1=0,s=0,q=0: rank-zero feasible control.
- Singleton box {(1,0)}, suffixes (-1,0),q=1: singleton-image feasible control, no division by zero.

The script compares constructive scalar sections against independent exact boundary-line/vertex calculations for every singleton/pair/joint subset, replays explicit nonnegative infeasibility certificates, propagates trajectories and rejects false witnesses, a reversed-sign lower bound and negative multipliers. Both routes are in ONE authored script; this is not an independently authored F checker.

Separate `checks/timing_control.py`: W={(0,-1),(0,1)} has one prefix, not two. The SAME action (3/2,1/2) works at q=2; at q=1 two original rows give 0<=-1; illegal suffix-oracle actions producing zero cost are rejected for assigning different actions to the same prefix. This supplies a nontrivial information-timing control.

Observed commands from the campaign root, with campaign-local TMPDIR/TMP/TEMP and PYTHONDONTWRITEBYTECODE=1:

    timeout 30 python3 -B research/continuation/checks/rank_one_check.py
    timeout 30 python3 -O -B research/continuation/checks/rank_one_check.py
    timeout 30 python3 -B research/continuation/checks/timing_control.py

All three exited 0; the first two outputs were byte-identical. No search loop, general solver, source-pool amendment, predecessor checker replay or Lean execution occurred. Raw stdout/stderr, exact argv, runtime and hashes are retained in `checks/run-observation.json`, `checks/timing-observation.json` and their referenced output files. Exact finite labels concern only seven fixed instances, not the general child.

## Remaining obligations and coordinator action

1. Read and independently criticize `derivation.md`, especially the singleton premise, zero rows, rational section and common-box assumption. A general formal claim still needs a fixed Lean statement/proof; comparator remains blocked as inherited, no bypass authorized.
2. Independently replay at least one positive/rejection pair from the NEW checks under new F evidence IDs. Use the commands above, but capture to new campaign-local F paths; do not overwrite E raw outputs. D2 source/results have not been re-certified by E.
3. Preserve the style failure and skipped command in final accounting. Any authorized later repair must be explicit; E has not spent a repair loop. The diagnostic is stylistic and does not negate the exact evidence.
4. Include both E check manifests, both observation records, verification contract/result, all raw streams and the terminal inventory in the final evidence index. Do not run the terminal campaign validator until coordinator persistence of synthesis.

Continuation succeeded in the narrow operational/scientific sense: a real outstanding obligation was reconstructed, its wording was sharpened by an exact counterexample, and a constructive corrected argument plus new boundary controls were produced. No novelty, general capability, scientific promotion, human attestation or privacy claim follows.

## Execution boundaries and resources

All worker-directed changes are under `research/continuation/`. No D2/baseline/shared tool/source/authority files changed, no live/tracker writes, nested workers, installs, model switch, commits/pushes or private trials. Root and branch were checked before writes. The first inventory command exited 2 on absent `.tmp` after successful Git checks, before any scientific execution or write; the actual existing plan-prescribed local scratch was then validated.

A mandatory-document tool response overflow was automatically spooled by the harness to `/tmp/pi-codemode-4d7a2b31f06ebbd6.txt`. It was not read, edited or deleted by the worker. Subsequent reads were bounded. This prevents claiming that all harness-internal temporary storage was campaign-local, although every worker subprocess received the campaign-local TMPDIR/TMP/TEMP policy. Worktree/read restrictions remain instructional, not filesystem isolation.

The first recorded early timestamp was 2026-11-13T01:25:23Z; exact worker start was not instrumented. `results.json` records scientific subprocess wall times and terminal-reporting time. Effective provider/model settings, billing, native retries and usage counters were not audited. The manual tool-invocation count includes codemode wrappers and nested calls and is recorded at final persistence; it is below the instructional 60-call ceiling, not harness-enforced. No new long-lived process remains.
