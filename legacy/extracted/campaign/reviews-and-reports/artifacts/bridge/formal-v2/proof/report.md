# Formal v2 proof-stage report — aro-discovery-k4t

The whole OGU→ARO transfer remains incomplete: F3, F4 and comparison with unrestricted source policies are unproved. This stage completes the exact ten reviewed F1/F2/prerequisite targets, including genuine recurrence expansion and both measurable policy transformations. Fresh offline Lean compilation and the exact-inventory axiom check passed. Independent final replay and semantic controls C1–C6 were not run in this proof stage.

## Fixed authority and identities

Workspace: `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`. Active project: `bridge/formal-env-v2/lean`. Original formal-v1 is historical and was not compiled or edited.

`preflight.json` records verification of the reviewed seal, six sealed file identities, installed tool identities, and all 3316 reviewed transitive import source/artifact identities. `proof-seal.json` freezes the new proof files, fresh local compilation products, reviewed target identity, exact inventory, validation and actual proof-import closure. All sealed Model/Goals/inventory identities were checked again after compilation and remain unchanged. No statement amendment was needed.

The compiler-reported proof import closure contains 3318 modules: the 3316 reviewed modules plus Dynamics and Policies. The only explicit proof-only external import is the already-present `Mathlib.Tactic.Abel`; no absent import, download, dependency installation or dependency rebuild was needed. Source anchor: `corpus/our_papers/A4_Дмитрук_2022.pdf`, physical pp2–6; its existing page-layout evidence was read. Source correspondence remains bounded by the separately reviewed Borel-rule convention.

## Exact completed inventory

All names below have namespace `BridgeFormalV2.Proofs`; goal types have namespace `BridgeFormalV2`. Each is a closed theorem of the exact corresponding sealed proposition, with no added assumption. The full printed goal propositions and actual theorem types/axioms are in `fresh-proofs-inventory-02.stdout`.

| Node | Declaration | Exact type | Source location |
|---|---|---|---|
| prerequisite | `nonempty_blocks` | `NonemptyBlocksGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:9` |
| F1 | `expansion` | `ExpansionGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:63` |
| F1 | `prefix_split` | `PrefixSplitGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:26` |
| F1 | `source_chronology` | `SourceChronologyGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:72` |
| F1 | `suffix_expansion` | `SuffixExpansionGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:91` |
| F2 | `exogenous_image` | `ExogenousImageGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:97` |
| F2 | `observation_fibre` | `ObservationFibreGoal` | `BridgeFormalV2/Proofs/Dynamics.lean:106` |
| F2 | `forward_policy` | `ForwardPolicyGoal` | `BridgeFormalV2/Proofs/Policies.lean:54` |
| F2 | `reverse_policy` | `ReversePolicyGoal` | `BridgeFormalV2/Proofs/Policies.lean:72` |
| F2 | `epigraph_equality` | `EpigraphEqualityGoal` | `BridgeFormalV2/Proofs/Policies.lean:89` |

Every target's actual transitive axiom list is exactly `[propext, Classical.choice, Quot.sound]`. The validator requires all ten printed theorem types and all ten actual axiom outputs, rejecting an absent output or an axiom outside the allowlist. There is no `sorry`, custom axiom, native evaluation or unsafe proof escape in the proof sources.

## Proof dependencies and scope

`run_formula` proves the finite expansion by induction on the actual chronological recurrence, splitting the last finite-sum term and using linear-map powers. `expansion` specializes it to the finite blocks. `run_add` proves superposition by a separate recurrence induction; `prefix_split` follows with zero controls/noise in the respective summands. `source_chronology` treats the prefix, measurement boundary and suffix separately. `suffix_expansion` combines the actual suffix execution with the proved expansion and prefix split.

`toState` and `toDeviation` are translation maps on the actual reachable range subtypes, with membership derived from `prefix_split`. Their Borel measurability follows from continuous addition/subtraction and subtype measurability. The transformations compose the original measurable policy with these maps. `preserves_of_related` then derives actual bounded suffix-control equality, full trajectory equality and every robust signed epigraph-bound equivalence from the explicitly proved relation. Every reachable deviation is represented by an actual prefix-noise witness; future disturbances remain universally and independently quantified. The same transformed policy serves all real bounds eta. The epigraph theorem transports witnesses without taking an infimum or assuming feasibility/attainment.

This does not prove equivalence with unqualified source strategies, off-reachable extensions, a value/attainment theorem, future-box support elimination or finite vertex/selection reduction.

## Observed checks and preserved failures

Commands ran from the feature worktree, using Python `-B`. `run.py` sets explicit proof-local TMPDIR/TMP/TEMP/XDG_CACHE_HOME/MATHLIB_CACHE_DIR/LAKE_CACHE_DIR, disables update caching, bounds each subprocess, and monitors the 600 MiB reserve.

- `timeout 180 python3 -B artifacts/bridge/formal-v2/proof/run.py preflight`: exit 0; reviewed identities matched.
- `timeout 300 python3 -B artifacts/bridge/formal-v2/proof/validate.py`: exit 1 at the inventory printer only. Its fresh Model, Goals, Dynamics and Policies compilations all exited 0. The printer used unsupported option `pp.width`; all ten type/axiom outputs were already present, but that failed compilation is not counted as a pass.
- After removing only that print-layout option, `timeout 300 python3 -B artifacts/bridge/formal-v2/proof/finish_validation.py`: exit 0, output `{"status": "pass", "completed": 10, "imports": 3318, "axioms": ["Classical.choice", "Quot.sound", "propext"]}`. The corrected exact inventory compiled with exit 0.
- Earlier development failures remain in `dynamics-01` (incorrect library identifier namespace) and `dynamics-02` (output directory absent). `dynamics-03` and `policies-01` exited 0. Corrections were explicit local source/output-path changes, not automatic retries or dependency repairs.

Fresh final compilation used `lean -o <proof-evidence>/build/BridgeFormalV2/<module>.olean BridgeFormalV2/<module>.lean` in order Model, Goals, Proofs/Dynamics, Proofs/Policies, Proofs/Inventory, with LEAN_PATH prefixed by the new proof-local build directory. This avoids trusting stale local Model/Goals artifacts and never invokes a dependency build. Exact arguments, environment, source hashes, exits and disk minima are in the matching `fresh-*.json` receipts. These operation-labelled evidence scripts deliberately refuse implicit reruns; independent replay must use new output locations/labels.

Lake's existing warnings about its copied mathlib checkout/manifest and local helper changes remain preserved in early stderr. The proof worker did not run `lake update` or change the helper or manifest. Reviewed mathematical import identities matched. This is standalone Lean evidence, not comparator acceptance or a full dependency-source rebuild.

The initial report-style diagnostic exited 1 for one passive-voice phrase. The report now names the actor explicitly; `report-style.stdout` preserves the original finding. This editorial diagnostic is separate from the successful kernel and axiom checks.

## Remaining work and operational boundaries

Missing targets in the reviewed inventory: none. Missing coverage nodes: F3 and F4. Unrestricted-source-policy comparison: unproved. C1–C6 and independent final kernel replay: not run, assigned to the final-review stage. Whole-transfer acceptance: false. No novelty or scientific-status claim follows.

The disk monitor's lowest recorded free space during compiler operations was 1031925760 bytes, above the required 629145600-byte reserve. Final observed free space was 1157517312 bytes; concurrent system activity can change this independently. No others' files were removed. No journal/blueprint/corpus/glossary/config/status writes, attestation, commits, network requests, global installs, nested agents/workflows, fallback or comparator bypass occurred. Actual billing, provider-native retries and full OS containment remain unknown.
