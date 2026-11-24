# Single-measurement correspondence — proposed statement package v1

Disposition: proposed, unreviewed statement; no completed proof, novelty assessment,
formal release or human semantic attestation. Implementation approval is not approval
of this precise formulation. This file is a review target, not an authorized seal.

Identifiers: question `single-measurement-correspondence`; model
`rational-linear-finite-paths-v1`; proposed claim `bound-witness-equivalence-v1`.
This model is distinct from the scalar M0 finite-action/absolute-cost test model.
The offline dossier's finite tests do not validate this general statement.

## Definitions and timing

Fix integers T >= 2, n,m,d >= 1 and r with 0 < r < T. Let Q denote the
rationals. Fix x_initial in Q^n and rational matrices A_t in Q^(n x n),
B_t in Q^(n x m), E_t in Q^(n x d), for 0 <= t < T. Fix a finite,
nonempty set W of complete disturbance paths w=(w_0,...,w_(T-1)) in
(Q^d)^T. Correlations are retained: W is not replaced by a Cartesian product
of marginal sets, a convex hull or a vertex enumeration of a different model.

For each t fix rational vectors l_t <= h_t coordinatewise, defining the
nonempty bounded control box U_t={u in Q^m : l_t <= u <= h_t}. Fix a
rational matrix H in Q^(k x n) and h in Q^k for k >= 0; hard terminal
feasibility is H x_T <= h, componentwise. It is not assumed attainable.
Fix c in Q^n and d0 in Q; the signed terminal cost is C(x)=c^T x+d0.
Neither c nor C is assumed nonnegative. The polarity is minimization of the
worst path cost; meeting bound q in Q means C(x_T(w)) <= q for every w in W.
There is no absolute value, coordinatewise worst-case substitution or extended
nonnegative codomain in this statement.

The transition is exactly

    x_0 = x_initial
    x_(t+1) = A_t x_t + B_t u_t + E_t w_t.

Timing at each t: the current state exists; at t=r only, exact x_r is
measured; the controller chooses the prescribed control; then disturbance w_t
is applied in the transition. There are no other measurements. In particular,
w_r and future disturbances are unavailable when the second program is chosen.
A policy is selected before the adverse complete path. No stochastic averaging
or probability measure is involved.

## Two witness spaces

A first-block program a belongs to product_(t<r) U_t. For each such a and w,
propagate the first r transitions and define z_a(w)=x_r(a,w).
Define the reachable observation domain O_a={z_a(w):w in W}, a nonempty finite
subset of Q^n. Equal observations depend on a and the specified dynamics, not
on a label for disturbance prefixes.

An implementable witness is (a,g), where

    g : O_a -> product_(r<=t<T) U_t.

For path w, set u_t=a_t for t<r and u_t=g(z_a(w))_t for r<=t<T, then propagate
the complete trajectory. The second program is open loop after the single
measurement: it cannot depend on subsequent states or disturbances. No value
of g outside O_a is required, chosen or silently defaulted.

A scenario witness is (a,v), where

    v : W -> product_(r<=t<T) U_t

and for all w,w' in W,

    z_a(w)=z_a(w') implies v(w)=v(w').

This is equality of the entire second-block program, not just the terminal
state or first second-block action. Use u_t=a_t for t<r and u_t=v(w)_t for
t>=r. Scenario assignments without this consistency condition are a different,
possibly anticipative information class and are excluded.

For either representation, admissibility at bound q means every complete path
trajectory obeys the transition, all control bounds, H x_T(w)<=h, and
C(x_T(w))<=q. The bound and robust feasibility are conjoined; infeasibility
is not encoded as zero, infinity or a successful witness.

## Proposed quantified assertion

For every T,n,m,d,r, every rational data tuple and every nonempty finite W
satisfying the definitions above, and for every q in Q:

    (there exist a and g forming an admissible implementable witness at q)
      if and only if
    (there exist a and v forming an admissible consistent scenario witness at q).

The outer data and q are fixed before either existential witness. The
universal path quantifier is inside each witness's admissibility predicate.
This is bound-feasibility correspondence, not an assertion that a minimum
exists, a particular numeric value is optimal, or the result is new.

## Required witness transformations (proof obligations, not proofs)

1. Forward obligation: use the same a and define v(w)=g(z_a(w)). Establish
   observation consistency, membership in every U_t, and equality of all
   controls and complete trajectories at every t, not only equality of costs.
2. Reverse obligation: use the same a; for each z in O_a define g(z) from
   v(w) for a path satisfying z_a(w)=z. Establish existence of a representative
   and independence from its choice using consistency. Do not select different
   continuations for equal observations or extend g to unreachable states.
3. For both directions, prove that complete-trajectory equality preserves
   each control bound, terminal inequality and signed cost bound, for every
   admissible complete path. Prove that transformations do not enlarge W.
4. Expand definitions when reviewing quantifier order; neither transformation
   may assume the desired existence equivalence as an auxiliary hypothesis.

## Nonemptiness, vacuity and proposed negative fixtures

W and every U_t are explicitly nonempty. The admissible witness set can be
empty because of terminal constraints or q; both existential statements may
then legitimately be false. Positive and infeasible fixtures must both appear
in a future formal acceptance suite so that a universally impossible model is
not mistaken for correspondence evidence. These are specifications, not
executed Lean tests or newly checked numerical results:

- Positive: zero initial state/dynamics/disturbances, singleton W and zero
  controls, terminal constraint x_T=0 and cost 0, q=0; require concrete witnesses
  on both sides.
- Infeasible: the same dynamics with terminal constraint x_T>=1; require no
  witness on either side, not a numeric optimum of zero.
- Wrong observations: two paths with identical x_r but different prefixes;
  unequal assigned continuations must fail the scenario consistency predicate.
  The M0 hidden-disturbance regression illustrates this obstruction only in M0.
- Anticipation: an a_t selected from a future w_t, or a continuation selected
  after w_r, must fail the witness signature/admissibility contract.
- Lost constraints: deleting U_t, terminal inequalities or a transition changes
  the sealed model identity and must be rejected, even if a simpler theorem compiles.
- Wrong polarity: signed negative c and a nonzero q must distinguish <=q from
  >=q, and signed cost from abs(C); removing signs is a statement mutation.
- Empty W: reject the input assumptions rather than accepting a vacuous robust
  claim. An accidentally empty theorem inventory must also fail release.

## Exclusions and unresolved review

Excluded: continuous uncertainty or time, real-valued extensions, vertex
reduction, noisy/output measurements, multiple closings, path constraints not
listed above, optimal closing-time selection, affine decision-rule exactness,
optimal-value attainment, A4 coefficients/results and general OGU-to-ARO source
correspondence. No external source theorem or novelty is claimed. Applicable
PDF anchors and closest-literature comparisons remain required before using
this package as an interpretation of a source problem.

Human review must approve the dynamics/timing, rational domains, disturbance
correlations, reachable-domain policy signature, control and terminal
constraints, objective signs and quantifier mapping. Only after that review
should trusted model/declaration hashes be sealed for a separate proof task.
Any change requires a new package version, not a changed proof target under
an old identity.

A future formal release must pin Lean 4.35.0-rc2, resolved mathlib
`c58b47adb340faa641e363aef2a460dc534bf172` and the complete dependency manifest;
freeze imports, definitions and exact declaration; require a nonempty expected
declaration inventory and transitive parsed axiom records, allowing only
`propext`, `Classical.choice`, `Quot.sound`. Reject missing modules/results,
`sorryAx`, custom/unknown/native-evaluation axioms and statement mismatch.
Independent replay/comparison compatibility and execution isolation are still
unverified. No Lean file, proof attempt or toolchain change is part of this slice.
