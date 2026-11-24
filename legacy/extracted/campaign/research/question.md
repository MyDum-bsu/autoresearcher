# Q1 v1: When does a single state measurement lose robust continuation feasibility?

Task: aro-discovery-k4t, phase C. Frozen question ID: `correlated-continuation-compatibility-v1`.
Disposition: source-grounded boundary/reconstruction objective. Novelty is unestablished. This is the only selected question; Q2 was not opened. The elementary equivalence between a state policy and a scenario assignment constant on state cells is background, not the research deliverable.

## 1. Exact model

Let Q be the rationals. Fix integers T >= 2, 0 < r < T, n,m,d >= 1 and k >= 0. All data below are rational: x_initial in Q^n; A_t in Q^(n x n), B_t in Q^(n x m), E_t in Q^(n x d), t=0,...,T-1; H in Q^(k x n), h in Q^k; c in Q^n and d0 in Q. The main construction must have c != 0. Controls belong to nonempty bounded closed boxes U_t = {u in Q^m: l_t <= u <= h_t^u}, with componentwise inequalities and rational endpoints; singleton coordinates are allowed.

W is a finite, nonempty set of distinct COMPLETE paths (w_0,...,w_(T-1)) in (Q^d)^T, chosen independently of controls. Keep correlations exactly: no Cartesian completion, convexification, replacement by marginal vertices or removal of paths. Different paths may have the same length-r prefix. Define P={w_<r : w in W} and S(p)={w_>=r : (p,w_>=r) in W}; each S(p) is nonempty.

Dynamics, with no other constraints implicit:

    x_0 = x_initial
    x_(t+1) = A_t x_t + B_t u_t + E_t w_t.

An entire policy is selected before nature selects a complete path in W. At time r the existing state x_r is measured exactly, the ENTIRE second-block program is chosen, then w_r enters the transition. There are no subsequent measurements or corrections. Thus neither policy below knows which suffix in S(p) occurs. Prefix information is a comparison oracle, not an asserted physical sensor.

A first-block program a is in A=product_(t<r) U_t. Propagation defines z_a(p)=x_r(a,p) and O_a={z_a(p):p in P}. The two policy signatures are:

    prefix: (a,v), v : P -> V, V=product_(r<=t<T) U_t;
    state:  (a,g), g : O_a -> V.

No policy values on unreachable states are required. The prefix policy chooses v(p), not v(w) independently for each COMPLETE path. The state policy chooses g(z_a(p)). Controls are open loop within each block.

Every complete trajectory must satisfy the HARD terminal constraint H x_T <= h. The signed terminal cost is C(x_T)=c^T x_T+d0. For q in Q, bound feasibility means C(x_T)<=q on EVERY w in W. Minimize the worst signed cost, not its absolute value and not a maximum guarantee of a positive reward. A source example maximizing x_2(T) maps, if used at all, to c=-e_2 and a negated guarantee; it is not this campaign's numeric instance.

## 2. Quantifiers and primary question

Define F_pre(a,q) by `exists v:P->V, forall w in W: H x_T(a,v(w_<r),w)<=h and C(x_T)<=q`. Define F_state(a,q) with `exists g:O_a->V` in the same place. All data, a and q are fixed before the existential continuation policy.

**Question:** characterize the boundary between F_pre(a,q) and F_state(a,q) using the geometry of the residual continuation constraints, and determine whether pairwise compatibility of prefixes in each state cell suffices, or whether a genuinely multi-prefix incompatibility can occur in this fixed-recourse model. Supply a dynamics-realizable rational obstruction or a precise structural reason why the attempted obstruction is impossible. Isolate what the source blockwise-disturbance premise contributes.

The intended general argument is for every declared rational data tuple, every admissible FIXED a and every rational q. A construction may freeze a by singleton first-block boxes. Define B_I(a)={q in Q:F_I(a,q)}. Equality of B_pre(a) and B_state(a) is weaker than implementability of every prefix policy. Equality after optimizing the first block means equality of {q:exists a F_I(a,q)}; it is a different statement. A loss at one a alone does not prove a loss after that optimization. Uniform equality over all possible H,h,c,d0 is NOT requested.

Infeasibility is the Boolean false for a given bound, or a typed `infeasible` in check output. It is never a zero optimum. An optimal value may be discussed as an infimum of achieved worst costs; no attainment claim is needed or inherited from the source. Nonempty W/U_t does not imply a feasible policy.

## 3. Starting representation, with obligations left to the attempts

For fixed a and p, let K_p(a,q) be the set of second-block programs b in V satisfying terminal and cost bounds for every suffix in S(p). This is a DEFINITION. A promising route is to expand the dynamics into terminal-state contribution from z_a(p), common linear response to b, and suffix contribution. Derive the inequalities with their signs; do not assume a formula copied from another model. The terminal/control matrix is common across prefixes; right-hand sides may differ because of conditional suffix sets.

Investigate directional worst residuals in the terminal constraint rows and cost row, rather than equality of raw prefixes or full suffix sets. Determine which equalities of such signatures suffice and whether they are necessary for this fixed task. A common feasible continuation can exist even when residual data differ. Equal optimal numbers do not imply common minimizers; pairwise intersections do not by themselves supply a continuation for a larger cell. These are warnings and candidate falsifiers, not conclusions already checked in this phase.

Merely writing `intersection K_p != empty` does not meet the substantive deliverable. Connect that representation to source premises and produce an explicit certificate/construction or a precise failed obligation. The proposed multi-prefix test is a way to attack a tempting shortcut, not a required answer. A negative answer supported by an argument is equally valid. No reference solution or preselected coefficients are supplied.

## 4. Bounded checkable consequence and common permissions

Preferred consequence: an exact small matrix-dynamics instance with a merged state cell of at least three distinct prefixes, and an adjudication of pairwise versus joint bound feasibility. Each feasibility assertion needs an explicit rational continuation satisfying all relevant paths. An infeasibility assertion can be certified by nonnegative rational multipliers on the actual stacked inequalities: verify that their weighted left coefficients vanish and weighted right side is strictly negative. This establishes infeasibility only for that particular rational system; completeness/existence of such certificates in general is a separate proof obligation, not an imported theorem here. The construction must retain the same H,h,c,q and box for all prefixes and show how residual problems arise from the declared dynamics. Prefer a bound-sensitive example with a nonzero signed objective; identify explicitly if the obstruction is entirely in hard constraints.

Both attempts may author direct candidate-specific exact code under their own `checks/`, using Python 3.12.3 standard library (`fractions.Fraction`, `itertools`, `json`, `hashlib`, etc.). Check matrix products and path trajectories directly in one route and independently replay explicit inequality certificates in another route. No new reusable evaluator, shared-code edits, dependency installation or solver infrastructure. Never infer continuous-box infeasibility by enumerating a finite action menu. Existing imported finite tools apply ONLY to their scalar two-period finite-action absolute-cost schema; they are auxiliary controls, not an evaluator for the selected matrix model.

Before execution freeze each candidate/check manifest: exact data, candidate ID/version, expected observation, controls, argv, input hashes, outputs and claimed scope. For constructions cap T<=4, n,m,d<=3, m*(T-r)<=3, k<=6, |W|<=4. Use at most 64 candidates, 3 active branches and 120 seconds TOTAL search time, stopping on a decisive witness; each search subprocess timeout <=120 seconds. Count exact operations before any loop. A direct certificate replay should need no search. General arguments may retain symbolic T/n/m/d but cannot be labeled machine-proved from these instances.

Required controls for a claimed exact construction: a genuine feasible witness; a false witness or sign/constraint mutation that must be rejected; a correlation/timing control that does not grant knowledge of w_r; and verification that claimed equal x_r values really are equal. For multi-prefix incompatibility include a witness for EVERY claimed pair, an all-prefix contradiction certificate, and feasible prefix continuations. If a control fails, preserve it and downgrade the claim. A split on distinct prefixes with different states is not the target obstruction.

Optional Lean: same installed 4.35.0-rc2, at most 25 minutes within the attempt budget, no downloads, own `lean/`, freeze exact statement/dependencies/axioms before proof work. Comparator is blocked by the observed bwrap uid-map denial; no bypass and no semantic-equivalence claim from compilation. No human statement approval or live formalized status.

## 5. Expected result/artifact contract

Each attempt writes `derivation.md`, `results.json`, `handoff.md`, `checks/manifest.json` and every declared check input/code/output. Derivation contains exact statement IDs, source-premise mapping, at least one serious falsifier, a mathematical argument or explicit construction, and unresolved implications. Results distinguish `source-reconstruction`, `exact-finite`, `unproved-sketch`, `refuted-candidate`, `unresolved`; prose approval is not a check. Persist the original parent when weakening a premise or changing a representation.

Progress means at least one of: a replayable dynamics-realizable separating certificate; a justified sufficient condition with its precise unproved/formal boundary plus a discriminating instance; or a decisive refutation/source closure of a proposed shortcut that sharpens the remaining obligation. An exact proof gap after a serious attempt is an honest exhausted result. Scalar injectivity, cell factorization alone, another tool inventory, and architecture prose are not substantive progress on this question.

Both public attempts receive the identical frozen packet/source/tool pool in `resource-manifest.json`, the same 90 minutes/60 total tool invocations and permissions. No new sources or shared tools during D1/D2; no reading the other attempt's directory or phase answer. This is instructional separation, not demonstrated isolation, blinding or an efficacy benchmark. Stop an inference on a decisive missing source, counterexample or budget exhaustion. Novelty cannot be asserted from this six-source inspection.
