# Candidate statement package and proof dependencies

## Status and authority

S1 only. Candidate definitions/statements are not proofs. Setup is blocked by the inspected official cache client's unconditional native retries, which this worker cannot reconcile with the explicit no-automatic-retry constraint. No cache get, dependency update, full source build, proof development or comparator execution was attempted. This is a conservative policy stop, not evidence that official caches are unavailable or that no other supported environment route can exist. The initial unsupported Git clone option failed locally with exit 129; its correction used one exact-SHA fetch, not a network retry. Both raw histories are retained.

The original operational acceptance correction remains authoritative: `artifacts/bridge/transfer-v1/coordinator/acceptance-correction.json`. Old exact-instance observations remain scoped evidence. No novelty gate, live status change, attestation, commit or issue mutation is part of S1.

## Source anchors and definitions

Original `corpus/our_papers/A4_Дмитрук_2022.pdf`, sha256 `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`, physical pp2-6, fresh layout and coordinate extraction in setup/source. Physical p2 (printed p67), (1.1): stationary recurrence, real vector spaces, control box, continuous infinity-norm disturbance box with positive radius, terminal two-sided linear rows. Physical p3 (printed p68), (1.2)-(1.3): all disturbances, signed linear criterion. Physical p4 (printed p69), Assumption 1: exact current-state measurement and selection of the next whole control block. Physical pp5-6 (printed pp70-71): successive trajectory systems, terminal membership and infeasible value +infinity. We specialize to one fixed measurement with positive blocks r and q, T=r+q. No Assumption 2 of nonempty closure sets is imposed: infeasibility must remain representable.

`Data` uses positive n,m,p,r,q and finite terminal row count (possibly zero); arbitrary stationary real linear maps A,B,E,H,c; no invertibility, disturbance rank, terminal feasibility or correspondence assumptions. Control bounds are ordered; disturbance radius is strictly positive. Degenerate control boxes and rank-deficient images remain allowed. Terminal bounds need not be consistent. Arbitrary c is a linear functional, with no nonnegative-cost coercion.

| Source object | Model declaration | Meaning / review boundary |
|---|---|---|
| finite real inputs | Vec, Block, ControlOK, NoiseOK, ControlBlock, NoiseBlock | Full continuous componentwise boxes; NonemptyBlocksGoal still unproved |
| equation (1.1) | step, run | Chronological natural-number recurrence |
| initial program | prefix, nominal | Finite r-block; at extends outside the block by zero, never executed in the finite horizon |
| prefix disturbance response | deviation, Z | Actual zero-initial/zero-control recurrence; no a argument |
| actual measured state | S, observed | Range of actual prefix recurrence, NOT defined by the desired decomposition |
| one state rule | StatePolicy | Measurable map from reachable-state subtype to bounded whole q-block |
| deviation recourse | DeviationPolicy | Separately defined measurable map on Z to bounded whole q-block |
| execution after observation | sourceSuffix, sourceTrajectory | Rule has no future input and is evaluated only at the measured state |
| ARO execution / rows | aroSuffix, aroTrajectory, aroTerminal | Trajectory uses actual recurrence; ARO robust rows use independently defined expansion |
| terminal constraints and cost | Rows | Every lower and upper H row, plus unrestricted signed c(x) <= eta |
| robust quantifiers | SourceBound, AROBound | A single rule, all prefix/observed deviations, then all independent future blocks |
| epigraph levels | sourceLevels, aroLevels | Sets of real bounds; empty sets represent infeasibility; no attainment claim |
| witness translations | Related | Translation equations are demanded conclusions, never Data fields |

`Measurable` uses Mathlib's Borel structures on finite real products and inherited subtype measurable spaces; this must be checked by elaboration and S2. A4 does not explicitly state Borel regularity on these pages. This is the declared implementation convention from transfer-v1, NOT a newly attributed source theorem. Equivalence with arbitrary unqualified source rules would require the missing F4 selection result. Off-reachable-state total extensions are NOT defined or claimed.

## Exact goals and expected future declarations

All goals below are `def ... : Prop`, in `BridgeFormal/Goals.lean`. No proof placeholder is supplied. Expected future declarations (namespace `BridgeFormal.Proofs`) must have exactly the corresponding closed goal type, not a weakened type with a desired conclusion added as a hypothesis. Proof-only path: `bridge/formal-v1/lean/BridgeFormal/Proofs/`; future build must explicitly include its modules, not just the current definition library.

| Node | Goal definition | Expected declaration | Dependency / proof plan |
|---|---|---|---|
| prerequisites | NonemptyBlocksGoal | nonempty_blocks | Constant umin and zero-noise witnesses using bound/radius fields |
| F1 | ExpansionGoal | expansion | Induction on run time; split last finite-sum term, distribute linear maps and powers; all real data, not test cases |
| F1 | PrefixSplitGoal | prefix_split | Induction on actual recurrence for nominal and disturbance responses |
| F1 | SourceChronologyGoal | source_chronology | Unfold the two chronological phases; treat t=r and t<r boundaries exactly |
| F1 | SuffixExpansionGoal | suffix_expansion | Prefix split + positive q + ExpansionGoal, retaining initial-state offset |
| F2 prerequisite | ExogenousImageGoal | exogenous_image | Prefix split in both range inclusions, subtraction cancellation; not merely syntactic independence of Z |
| F2 information | ObservationFibreGoal | observation_fibre | Equality of reachable subtypes from equality of actual state, congruence of one rule |
| F2 | ForwardPolicyGoal | forward_policy | Build translation Z -> S(a), prove continuous/Borel on subtypes, compose rule, prove Related/controls/trajectories/all signed bounds |
| F2 | ReversePolicyGoal | reverse_policy | Build inverse translation S(a) -> Z, prove Borel and inverse equations, preserve all actual trajectories and robust rows |
| F2 | EpigraphEqualityGoal | epigraph_equality | Both witness maps at the same a and every eta; no real infimum of an empty set |
| F3 | NOT FORMALIZED | none | Exact support equivalence for independent continuous future box for each signed row; requires separate statement/review identity |
| F4 | NOT FORMALIZED | none | Finite recourse + Borel real-state selection in relative dimension, rank degeneracy and terminal/state image distinctions; requires separate statement/review identity |

Preserves includes Related, actual suffix control equality, complete trajectory equality up to T, and SourceBound iff AROBound for every real eta. The same measurable witness serves every eta. These are stronger witness requirements than a single numerical value equality. No quantifier permits selecting a new suffix after observing wp.

## Definition closure and missing material

The seal records trusted local source/config SHA256 identities, installed Lean/Lake executable identities, exact mathlib checkout, pinned upstream manifest, and the recursively discovered source import graph. Missing dependency modules and compiled imports are explicit; a source hash is not a compiled-import hash. Resolved Lake manifest is reconstructed from the unchanged existing project pin and renamed only at the root; no dependency revision is upgraded. It is a pinned intended resolution, NOT a successfully loaded Lake workspace.

Not formalized: F3/F4 goals/proofs; extended-real optimal value and any infimum/attainment corollary; compactness/polytope/vertex enumeration; measurable selection/triangulation; equivalence of Borel witnesses to arbitrary source policies; total policy off reachable states; terminal-image reduction; closure-set projection comparison. None is concealed behind a model predicate or proof constant. F1/F2 proofs are also absent.

## Semantic control inventory (frozen before execution)

Controls are specifications for later Lean evidence files under final-review only, not executions in S1. Use the actual Data, run, Rows and policy definitions; no Python simulator can count as their discharge. Each control must typecheck its complete Data and explicit noise/control membership obligations.

- C1 satisfiable witness: n=2,m=1,p=2,r=q=1, A identity, B(u)=(u,0), E(w)=(0,w0+w1), x0=(0,0), U=[-1,1], rho=1, H identity, terminal [-4,4]^2, c(x)=-x0. Prefix a=1 and constant suffix b=1 are measurable. Prove SourceBound at eta=-2 and AROBound for its corresponding constant rule. This uses nonzero disturbance, positive horizon and a negative feasible cost level.
- C2 infeasible terminal: same data, replace second terminal coordinate interval by [5,5]. Prove sourceLevels is empty by the all-zero prefix/future disturbances: second state is zero regardless of controls. Controls/disturbances themselves remain nonempty. Do not merely choose an empty terminal interval.
- C3 information fibres: C1 prefix paths (1,-1) and (-1,1) have the same measured state. For an arbitrary StatePolicy prove their sourceSuffix equality. Vary future independently while retaining that same suffix. This checks history/future information is unavailable.
- C4 signed polarity: C1 witness terminal first coordinate is 2, cost -2. Prove Rows (-2) at all its terminal states; disprove Rows (-3) at zero disturbances. With c changed to +x0 the same witness violates eta=-2. No absolute value substitution.
- C5 deliberate rejected target: request a proof that the C1 witness satisfies SourceBound (-3). Supply zero-disturbance contradiction as the gate's expected reason; a candidate false proof file must be rejected by Lean, not accepted because imports are absent. Any environment/import failure is INVALID CONTROL, not the expected rejection.
- C6 future-dependent forbidden suffix: on C1 with the same prefix observation, request a single StatePolicy whose sourceSuffix equals constant +1 when future first noise component is +1 and constant -1 when it is -1. Prove this specification impossible by equality of the same sourceSuffix. A negative test purporting to construct it must fail for the contradictory control equality after imports are working.

These controls do not replace the general goals. Their execution and an axiom audit are NOT RUN in S1. Allowed future theorem foundations are only propext, Classical.choice, Quot.sound; future gate must reject sorryAx, unknown axioms and native-evaluation trust shortcuts. Definitions/goals need successful elaboration and S2 fidelity review before any S3 proof.
