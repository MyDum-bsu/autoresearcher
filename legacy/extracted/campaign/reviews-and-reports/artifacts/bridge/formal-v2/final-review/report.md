# Independent formal-v2 final replay

C2 is incomplete: the control implementation failed at an unknown auxiliary Set lemma. F3/F4 and unrestricted-source-policy comparison remain unproved. Whole-transfer acceptance is false.

All ten exact frozen prerequisite/F1/F2 targets were freshly compiled with exit 0. Expanded goal types and nonempty transitive axiom outputs were inspected; each uses only propext, Classical.choice and Quot.sound. No reviewed mathematical source or proof was changed.

## Evidence and reproduction

- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/replay.py replay`: exit 0; fresh Model, Goals, Dynamics, Policies and exact Inventory compilation.
- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/make_controls.py`: driver exit 0, distinct compiler results below; not an all-controls pass.
- `timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/replay.py identities`: exit 0; identical pre/post frozen inputs.
- Operation IDs are one-shot: existing receipt labels refuse rerun. A future reproduction must use a separately authorized new evidence directory rather than overwrite this history.
- `theorem-audit.json` and `replay-inventory.stdout:3319-3371`: actual printed types and transitive axioms, not author booleans.
- `actual-import-closure.json`: 3318 fresh compiler-reported imports and their source/binary identities; no dependency rebuild/source-binary reproducibility claim.
- `preflight.json` / `postflight.json`: 13286 unique file identities match; both old 3316/3318 closures, candidate/review/proof seals, exact inventory, binaries and tool identities checked.
- Russian owner report: `reports/briefings/2026-11-13-ogu-aro-formal-v2.md`.

## Exact target coverage

All declaration names below have prefix `BridgeFormalV2.Proofs.`; goal names have prefix `BridgeFormalV2.`. Every row has compiler exit 0 and the same permitted foundation set `{propext, Classical.choice, Quot.sound}`. Data assumptions and full per-node claim/remaining-obligation table are in the Russian report.

| Node | Goal | Declaration |
|---|---|---|
| prerequisite | `BridgeFormalV2.NonemptyBlocksGoal` | `BridgeFormalV2.Proofs.nonempty_blocks` |
| F1 | `BridgeFormalV2.ExpansionGoal` | `BridgeFormalV2.Proofs.expansion` |
| F1 | `BridgeFormalV2.PrefixSplitGoal` | `BridgeFormalV2.Proofs.prefix_split` |
| F1 | `BridgeFormalV2.SourceChronologyGoal` | `BridgeFormalV2.Proofs.source_chronology` |
| F1 | `BridgeFormalV2.SuffixExpansionGoal` | `BridgeFormalV2.Proofs.suffix_expansion` |
| F2 | `BridgeFormalV2.ExogenousImageGoal` | `BridgeFormalV2.Proofs.exogenous_image` |
| F2 | `BridgeFormalV2.ObservationFibreGoal` | `BridgeFormalV2.Proofs.observation_fibre` |
| F2 | `BridgeFormalV2.ForwardPolicyGoal` | `BridgeFormalV2.Proofs.forward_policy` |
| F2 | `BridgeFormalV2.ReversePolicyGoal` | `BridgeFormalV2.Proofs.reverse_policy` |
| F2 | `BridgeFormalV2.EpigraphEqualityGoal` | `BridgeFormalV2.Proofs.epigraph_equality` |

F1 derives the recurrence expansion, prefix split and actual source chronology. F2 constructs both measurable reachable-state/deviation translations, preserves actual controls/trajectories/all signed bounds and equates the two Borel epigraph-level sets. This is not equality with arbitrary unrestricted source strategies, extended-value/attainment, support elimination or a finite vertex/selection theorem.

## Semantic controls

| Control | Compiler result | Interpretation |
|---|---|---|
| C1 | 0 | Real continuous fixture, admissible measurable witness, SourceBound and corresponding AROBound at -2 |
| C2 | 1 | Failed at `C2.lean:8`: unknown `Set.eq_empty_iff_forall_not_mem.mpr`; empty sourceLevels not checked, not an intended rejection |
| C3 | 0 | Two cancelling histories, one observation, arbitrary policy suffix equality under independently varied futures |
| C4 | 0 | Rows -2 for all witness terminal states, zero-noise rejection of -3, opposite signed criterion violates -2 |
| C5 | 1 expected | Working imports and printed c4Reject, then -2/-3 SourceBound type mismatch at the deliberately false target |
| C6 | 0; negative 1 expected | Positive impossibility of incompatible future demands; false construction rejected at suffix/minus equality, not import failure |

The first new `ControlData.lean` fixture also failed elaboration. Its file/output remain immutable. The separately compiled `ControlFixture.lean` makes only concrete fixture Data abbreviations transparent and uses numeric index values; no sealed definitions or reviewed proofs were repaired. C2 was not repaired or rerun. All six declared controls were attempted; no not-run outcome is relabelled as a rejection.

## Remaining coverage and authority

- F3: missing sealed proposition/proof for universal future-box support equivalence, including signed criterion and both terminal directions.
- F4: missing finite fixed-recourse reduction and measurable real-state implementation, including relative dimension/degenerate images.
- Unrestricted source policies: missing existence/level comparison with the Borel convention; no arbitrary-policy bijection claimed.
- C2: incomplete semantic nonvacuity/infeasibility control due to the test implementation error; not a counterexample to the ten checked targets.
- No source/proof repair, new scientific theorem, download, global install, full Mathlib build/import, comparator bypass, live journal/blueprint/corpus/glossary/config write, attestation, commit/push, nested worker/workflow or new objective.
- Python -B and explicit task-local TMP/cache variables, MATHLIB_NO_CACHE_ON_UPDATE=1, bounded processes and a 600 MiB disk guard were used. Minimum observed free bytes: 1146224640. Actual billing/native provider retries/full OS containment remain unknown.
- First-scientific-success and whole-transfer acceptance remain unmet. This is a scoped compiler/hash/axiom audit, not a general scientific success flag.
