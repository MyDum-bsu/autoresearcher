# D1 standalone handoff: three-prefix incompatibility

Task `aro-discovery-k4t`, phase D1. Workspace `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`. This handoff describes only D1. Do not give it to D2 before D2 finishes: the paired attempts have instructional answer separation. The prescribed successor E receives the structured attempt, not this file, unless the coordinator explicitly changes that role.

## What is established, and by what

The single candidate-specific check exited 0; all 11 declared cases passed. It replayed rational matrix trajectories, all pair witnesses, a common-state infeasibility certificate, exact optimal-value bounds, and rejection/timing controls. This is authored exact arithmetic evidence awaiting independent F replay, not an LLM truth verdict, general Lean proof, novelty claim or human attestation.

Core files:

- `research/question.md`: authoritative general-model quantifiers and caps.
- `research/resource-manifest.json`: same frozen source/tool pool for both attempts; SHA-256 `1ff15746b0a2c8c47499cefdeca9dc2fc6b95c92ef536ce2e9259d7b542373d8`.
- `research/baseline/derivation.md`: definitions, three branches, general argument, full construction, source boundaries and gaps.
- `research/baseline/checks/candidate-v1.json`: exact data, witnesses and certificate rows.
- `research/baseline/checks/check_candidate.py`: standard-library exact checker, not an optimizer or shared judge.
- `research/baseline/checks/manifest.json`: immutable pre-execution inputs/expected outcomes/command.
- `research/baseline/checks/execution.json`: actual exit, times and stream/input identities.
- `research/baseline/checks/exact.stdout.json`, `exact.stderr`: retained original streams.
- `research/baseline/results.json`: claim/evidence/limitation accounting.
- `research/baseline/checks/delivery-inventory.json`: post-execution schema projection of the unchanged pre-execution inventory, for the final delivery validator's `case_ids`/`files` shape. It must not be misreported as an additional pre-execution freeze or a new mathematical check.

## Definitions sufficient to reconstruct the result

The policy is selected before nature chooses one of finitely many COMPLETE paths. Measure x_r, choose the entire second-block program b, then w_r acts. Prefix policy b(p) knows w_<r but not the future suffix; state policy b(x_r) only knows the measured state. Both must satisfy hard terminal constraints and the cost bound on every compatible suffix.

For a fixed first program a, expand x_T=Phi(T,r)z_a(p)+L b+e(s). Let R stack H and c^T and t(q) stack h and q-d0. Then K_p={b in V:R L b<=beta_p}, where beta_p=t(q)-R Phi(T,r)z_a(p)-max_(s in S(p))R e(s), with rowwise maxima. State-cell feasibility uses the componentwise minimum of beta_p over its prefixes. These general statements have prose arguments only; do not label them machine-proved from the example.

Exact instance: T=2,r=1,n=m=d=2; x_0=0; A_0=A_1=I; B_0=E_0=0; B_1=E_1=I. First control is fixed at zero; b=(u,v) belongs to [0,2]^2 intersect Q^2. Thus x_1=0, x_2=b+w_1. Hard constraint x_2>=0; cost c^T x_2 with c=(1,1).

The four paths are:

    A: w_0=(0,0), w_1=(0,0), prefix p0;
    B: w_0=(1,0), w_1=(-1,0), prefix p1;
    C: w_0=(1,0), w_1=(-1,-1/4), prefix p1;
    D: w_0=(0,1), w_1=(0,-1), prefix p2.

All three prefixes have the SAME measured state. The continuation systems, including the common box, are

    p0: u>=0, v>=0,   u+v<=q;
    p1: u>=1, v>=1/4, u+v<=q+1;
    p2: u>=0, v>=1,   u+v<=q+1.

At q=3/2 the pair witnesses are (1,1/4), (0,1), (1,1) for pairs 01,02,12. Joint feasibility is impossible: B's -u<=-1 plus D's -v<=-1 plus A's u+v<=3/2 gives 0<=-1/2. Hard constraints alone are jointly feasible at (1,1).

The common witness (1,1) attains state worst cost 2; the same certificate with epigraph tau proves tau>=2. Prefix witnesses (0,0),(1,1/4),(0,1) attain worst cost 1/4. B's -u<=-1, C's -v<=-1/4, and B's u+v-tau<=1 prove tau>=1/4 for p1. Thus B_pre={q>=1/4}, B_state={q>=2}, all over Q. The singleton first-stage box removes any issue about subsequently optimizing a.

## Source premise and negative knowledge

D1 directly read A4 PDF p4 (render `research/sources/A4-p4.png`) and BT04 PDF p5 (`BT04-p5.png`). Their exact PDF hashes are recorded in the resource manifest and derivation. A4's measurement comes before the new block; its disturbance-block sets admit each block independently. With common conditional suffix sets S(p), equal measured state makes beta_p equal, so prefix feasibility can be implemented cellwise. The finite rational reconstruction does not re-prove A4's continuous-box recursion.

BT04 Theorem 2.2 is a fixed-recourse vertex ARC formulation with a separate recourse per vertex; its displayed formulation does not impose equality of recourse across equal observations. The present example is not a refutation of that source. Generic information sensitivity and basic observation factorization are already background, not claimed discoveries.

The tempting pairwise-compatibility parent is refuted; do not repeat it unchanged. B and C share a prefix: pathwise zero-cost controls b_B=(1,0), b_C=(1,1/4) are anticipative and are rejected as a prefix policy. Continuous-box infeasibility comes from a universal linear certificate, not enumerating a finite action menu. E_0=0 is deliberately degenerate and allowed; no claim about a nondegenerate observability class is made. No extra sources, installations, sibling execution, tracker writes or live scientific writes occurred.

## Exact replay and delivery integration

Before independent replay, verify root/branch and input hashes against `checks/manifest.json`. Keep the existing evidence unchanged. Use a new reviewer-owned local stream path and a new check ID, not the author's PASS:

    cd <workspace>/aro-discovery-campaign
    export TMPDIR="$PWD/artifacts/campaign/tmp"
    export TMP="$TMPDIR" TEMP="$TMPDIR" PYTHONDONTWRITEBYTECODE=1
    timeout 120 /usr/bin/python3 -B research/baseline/checks/check_candidate.py research/baseline/checks/candidate-v1.json

Scratch must already be an actual nonsymlink in-root directory; stop on a failed precondition, do not fall back to /tmp. The original D1 command and raw streams are in `execution.json`. Its expected success is exit 0, status `passed`, 11 cases, joint contradiction -1/2, prefix/state optima 1/4 and 2, and rejection of the anticipative path policy. The same execution includes decisive positive and rejection controls, but F must independently inspect/run appropriate ones before synthesizing a checked claim.

For final delivery index integration use check ID `D1-exact-construction-v1`, `inventory_path=research/baseline/checks/delivery-inventory.json`, actual input/output refs from `execution.json`, and its raw stream paths. Normalize the final validator's `command.cwd` to `.` relative to the verified root if required by that schema; preserve the absolute execution cwd in the original record. No source, predicate or result was changed for this packaging projection.

## One outstanding discriminating obligation

Formalize or refute the row-representative consequence in the SAME finite rational model: for fixed a,q and one measured-state cell, at most k+1 prefixes determine its entire robust continuation system, by choosing an attaining prefix in each of the k hard-terminal directions and the cost direction. Common box rows need no extra prefix. The prose argument is finite coordinatewise minimization with a shared control-response matrix. A fixed formal statement must keep the finite nonempty conditional suffix sets, rational domains, signs, common state and shared L explicit. Do not substitute the elementary policy-factorization statement.

Other gaps remain explicit: no general Lean theorem, necessity characterization of directional-signature equality, complete infeasibility-certificate theorem, broad novelty survey, nondegenerate-prefix stability result or multiple-measurement extension. Optional Lean was not run; native comparator remains blocked by the pre-existing uid-map denial and was not bypassed.

Stop reason: decisive separating witness and exact certificates obtained; further unchanged instances would repeat the result. There was no D1 scientific runtime failure. Preparation/tool overhead and unknown provider billing are separate from the observed subprocess time in `execution.json`. The session's tool budget is instructional, not sandboxing or a hard harness limit.
