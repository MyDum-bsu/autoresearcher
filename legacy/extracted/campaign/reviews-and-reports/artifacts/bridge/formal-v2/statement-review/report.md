# Formal v2 independent source and statement review

## Result and boundary

No concrete blocker was found for proof development against the exact sealed ten-target F1/F2 inventory. `readyForProof: true` is a structural review disposition, not a proof, a scientific verdict, attestation, or acceptance of the whole transfer. Current Model and Goals each independently elaborated with exit 0. All ten targets remain unproved.

Two reviewer-tool failures are retained rather than presented as passes. The first preflight used an overbroad dependency-cleanliness assertion and stopped on two pre-existing dereferenced benchmark symlinks. A later diagnostic inspection returned exit 1 solely because this reviewer requested unsupported pretty-printer option `pp.width`; import processing, all ten goal prints, structure prints and four Borel-instance syntheses continued and are present. Neither failure is a current Model/Goals compiler defect. No source/environment repair or compiler retry was performed to hide either result.

The whole bridge remains incomplete: F3 support elimination, F4 finite formulation/selection, and comparison between the chosen Borel policy class and unrestricted source policies have not been proved. Extended-value/attainment claims and total off-reachable policy extensions are also outside these targets.

## Workspace, authority and inputs

Observed root: `<workspace>/aro-discovery-campaign`; branch: `task/aro-discovery-k4t-campaign`. The active project is `bridge/formal-env-v2/lean`, not original formal-v1. Original sources, source artifacts, v1 results, sealed v2 source/configuration, inventory and candidate seal were read only. All new files, including review-only elaboration outputs, are under `artifacts/bridge/formal-v2/statement-review/`.

Read in full: continuation spec, parent formal-repair spec, FOUNDATION, AGENTS, amended Model/Goals, recorded v1-v2 diffs, original statement map/control inventory and transfer dictionary. Applied worker, session-protocol, literature/oracle, logika and technical-style instructions. No project bootstrap/status-writing commands, repository-wide build, task tracking mutation, scientific write, nested agent/workflow/objective, download, installation, commit, comparator bypass or attestation was performed. The bounded worker scope supersedes the generic session bootstrap.

Original A4: `corpus/our_papers/A4_Дмитрук_2022.pdf`, SHA256 `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`. This review freshly extracted physical pp2–6 directly from that PDF with layout and bounding boxes, read all five pages' layout, and visually inspected fresh p2/p4 renders. It did not rely on historical report paraphrases for source equations or information timing. The complete pinned Apache-2.0 license was read.

## Observed compiler and identity evidence

Commands executed from the campaign root:

1. `timeout 180 python3 -B artifacts/bridge/formal-v2/statement-review/inspect.py` -> exit 1 at the clean-worktree assertion, before any compiler invocation. `identity-preflight.json` preserves the matching six sealed hashes, two executable hashes, nine dependency revisions and the unexpected tracked file types. The helper basename also shadowed stdlib `inspect` during apport's exception reporting; this affected only the reviewer exception handler.
2. `timeout 180 python3 -B artifacts/bridge/formal-v2/statement-review/review_current.py` -> exit 0. This explicit diagnostic continuation classified the extra file types without editing dependencies; fresh PDF extraction and separate Model/Goals elaboration each returned exit 0. It did not retry a failed compiler invocation or download.
3. `timeout 180 python3 -B artifacts/bridge/formal-v2/statement-review/audit_imports.py` -> exit 1, solely the review-only `pp.width` diagnostic. See `statement-inspection.json`, `.stdout`, `.stderr` and `inspection-classification.json`. This is not labelled a successful aggregate inspection command.
4. `timeout 240 python3 -B artifacts/bridge/formal-v2/statement-review/freeze_identity.py` -> exit 0; consumed existing diagnostics without rerunning Lean. It hashed 3316 compiler-reported transitive modules with no missing source/binary identity, checked all ten printed target definitions and the four synthesized Borel instances, and froze `reviewed-target-identity.json`.

The actual elaboration invocations, working directory, task-local cache/temp variables, durations, free-space samples and stream hashes are in `model-elaboration.json` and `goals-elaboration.json`. They run the installed `lean -o <review>/build/BridgeFormalV2/{Model,Goals}.olean BridgeFormalV2/{Model,Goals}.lean`. `LEAN_PATH` is the observed Lake workspace path with the review build directory prepended. Thus Goals imports the Model freshly elaborated by this reviewer, not an unverified stale local Model binary. No dependency build is invoked. Explicit `TMPDIR/TMP/TEMP/XDG_CACHE_HOME/MATHLIB_CACHE_DIR/LAKE_CACHE_DIR`, `MATHLIB_NO_CACHE_ON_UPDATE=1`, bounded process timeouts and a 600 MiB reserve monitor are used.

Installed Lean is 4.35.0-rc2, commit `11acb17ec6b07a8f9e9173e6845197929540936b`; Lake is 5.0.0-src+11acb17. Their executable SHA256 identities match the original tool seal. All nine HEADs match the unchanged manifest, including mathlib `c58b47adb340faa641e363aef2a460dc534bf172`. The existing acquisition helper has exactly the recorded modified SHA256 `b0029c2a0725cabd24bb87ac529cf6f97cfb52e9578105d2cc9ea7123efdd2ad`; it was not executed here.

Additional provenance finding: mathlib's `scripts/bench/build/fake-root/bin/lean.py` and `scripts/bench/size/run.py` are regular files where Git records symlinks. Each is byte-identical to its pinned symlink target. The existing provisioning script uses `copytree` without preserving symlinks. These benchmark files are neither imported nor executed in this review; no mathematical source change was found in tracked dependency changes. This narrows, rather than repeats, the earlier broad claim that the cache helper is the only checkout difference. `benchmark-copy-diff.stdout` and `preflight-classification.json` preserve the discrepancy. It is not a mathematical import blocker and no cleanup was authorized or attempted.

`actual-import-closure.json` records actual imported source hashes and `.olean`/available companion hashes, including the review-local Model and Goals. This is an identity inventory of existing dependency cache artifacts, not recompilation or independent kernel replay of all dependency sources, and not a claim of source/binary reproducibility. The importer diagnostics loaded all these modules despite the unrelated unsupported option. The final replay stage must still inspect completed proof types and transitive axioms.

The sealed Lake default target remains named `BridgeFormal` (`lakefile.toml:3,12`), while this amendment is `BridgeFormalV2`. Do not use a bare `lake build` of that historical default as evidence for v2. This review used explicit current module paths successfully; the proof stage must explicitly compile its v2 proof inventory. No configuration change is required for these direct invocations.

## Source correspondence audit

Paths below abbreviate `bridge/formal-env-v2/lean/BridgeFormalV2/` as `V2/`.

| Source anchor | Actual amended definitions | Inspection result |
|---|---|---|
| A4 physical p2, printed p67, (1.1), real state/control/disturbance spaces | `V2/Model.lean:15-42,56-62` | Real finite-dimensional vectors and arbitrary stationary linear maps A/B/E; source M is named E. No A=I, invertibility, rank, scalar-state or rational-grid restriction. Data's m is control dimension; r is prefix length, unlike source notation. |
| A4 p2, bounded control U and positive-radius infinity-norm W | `Model.lean:25-38,47-50` | Componentwise closed control box, ordered bounds, continuous real disturbance box with rho>0. Positive n,m,p,r,q; T=r+q has a genuine interior measurement. Control degeneracy is allowed. E may have deficient rank or vanish, but the disturbance domain is not empty or replaced by finitely many signs. |
| A4 p2, terminal XT; p3 (1.2) | `Model.lean:39-41,120-128` | Every lower and upper H row retained. Terminal feasibility is not a Data hypothesis; inconsistent bounds and unreachable targets remain representable. `rows=0` is permitted, without making terminal constraints disappear for arbitrary positive rows. |
| A4 p3, (1.3), c unrestricted; p4, omitted open-loop constant | `Model.lean:33,42,112-133` | Signed linear cost is `c x ≤ eta`, eta real. Full initial-state offset remains in run/expansion; no norm, absolute value, nonnegative coercion or ENNReal replacement. No unsafe real `sInf` convention. |
| A4 p4, Assumption 1 and Delta-j blocks | `Model.lean:64-104` | Prefix a is fixed before uncertainty. At time r one exact reachable state determines the entire q-block. Neither StatePolicy.rule nor sourceSuffix receives a future-noise argument. Suffix selection is not renewed after each future disturbance. |
| A4 p5, sequential trajectory equations | `Model.lean:53-62,96-113`; `Goals.lean:18-33` | Trajectory is actual two-phase recurrence. SourceChronologyGoal demands consistency across the t=r boundary and all steps t<T. SuffixExpansionGoal still has to derive its terminal formula. |
| A4 p4, W-j product blocks; p5, arbitrary concatenated disturbances | `Model.lean:49-50,123-128` | All component/time combinations occur. Prefix and future blocks are separately universally quantified; future uncertainty has no state/prefix-dependent restriction. This is rectangular set uncertainty, not a probabilistic independence claim. |
| A4 p5–6, terminal feasibility and +infinity convention for no solution | `Model.lean:130-133` | Real feasible epigraph-level sets allow emptiness and avoid asserting attainment. The actual extended-real value convention is not formalized. Assumption 2 of nonempty closure sets on p6 is deliberately not imposed, preserving infeasible cases. |

The live glossary's historical A=I/discrete-sign/L1 description (`docs/GLOSSARY.md`, section 2) disagrees with these actual A4 pages. It is not used as mathematical authority and is not edited. The present sealed model follows the original source's general stationary recurrence, continuous boxes and signed terminal criterion.

## Borel domains, fibres and quantifier order

`S(a)` is the range of the actual disturbed prefix recurrence (`Model.lean:74-75`), not an assumed translated set. `Z` is the range of the actual zero-initial/zero-control response (`:70-74`). The equality of translated reachable sets is a goal (`Goals.lean:36-38`), not a Data field. Data assumes neither terminal expansion nor policy correspondence nor feasible recourse.

The types of both policy rules are concrete reachable-state/deviation subtypes into the bounded full control-block subtype (`Model.lean:77-83`). The diagnostic output synthesized `Pi.borelSpace` for real state vectors and `Subtype.borelSpace` for S(a), Z and the control-block subtype. `Measurable` therefore uses the inherited finite-product/subtype Borel structures, not a silently introduced discrete/trivial sigma algebra. Both directions must construct a policy carrying that measurability field. Translation between S(a) and Z requires the prefix-split/range facts and preservation of Borel measurability; these obligations remain demanded conclusions.

`sourceSuffix` evaluates the one rule only at `observed a wm`; proof components of that subtype do not add physical information. Equal actual measured states therefore cannot license different suffix blocks for different histories. `ObservationFibreGoal` asks for that equality for arbitrary policies, rather than providing a future-dependent policy wrapper. Subtraction of the known `nominal a` is implementable because a is the fixed chosen initial program. A different a may have a different transformed policy; no target asserts a single universal policy independent of a.

Forward/reverse goals quantify a whole input policy, then existentially quantify its counterpart outside all noise, time and eta quantifiers. `Preserves` demands Related translation equations, equality of full suffix controls, equality of entire trajectories for every t≤T, and bound equivalence for every real eta (`Goals.lean:43-57`). Consequently the same witness transformation must preserve all signed levels. The equality of epigraph sets is not only an equality of one sampled optimum. No theorem target assumes `Preserves`, `Related`, the expansion formula, or its desired set equality as an extra hypothesis.

A4 does not explicitly require Borel rules on pp2–6. This is a declared implementation convention (`Model.lean:7`), not an attributed source assumption. The exact F1/F2 target is a correspondence between those two Borel classes. Equality of these classes' achievable levels with the unrestricted source-policy formulation remains a separate missing selection/comparison obligation. It is not required to regard the restricted, explicitly stated ten propositions as a coherent prover target, and it must not disappear from final whole-bridge coverage.

## Exact ten-target audit and frozen identity

All entries have namespace prefix `BridgeFormalV2` for their types and `BridgeFormalV2.Proofs` for expected future declarations. No such proof declaration was supplied in this assignment. The inventory, target definition files and actual import closure are bound by `reviewed-target-identity.json`.

| Node | Closed target type | Expected declaration | Actual obligation, not assumed conclusion |
|---|---|---|---|
| prerequisite | `NonemptyBlocksGoal` | `nonempty_blocks` | For every Data and every k, both bounded block types inhabited. Ordered control bounds and positive rho supply intended witnesses; k=0 does not replace positive r/q. |
| F1 | `ExpansionGoal` | `expansion` | For every k,x,u,w over the reals, actual run equals A^k x plus all chronological impulse terms. Fin-k index ensures k-1-t has the intended nonnegative exponent; k=0 asks for x=x. |
| F1 | `PrefixSplitGoal` | `prefix_split` | Actual prefix equals nominal plus actual zero-control disturbance response, for every bounded a/wm. |
| F1 | `SourceChronologyGoal` | `source_chronology` | Initial state and each actual step to T, including t=r-1 and t=r. Finite execution never uses blockAt's out-of-block zero as an admissible control. |
| F1 | `SuffixExpansionGoal` | `suffix_expansion` | Derive terminal suffix expansion retaining nominal offset and measured deviation, not insert it as a trajectory axiom. |
| F2 | `ExogenousImageGoal` | `exogenous_image` | Equality of actual prefix-minus-nominal image and Z for every a; substantive independence beyond omission of an a argument in the notation Z. |
| F2 | `ObservationFibreGoal` | `observation_fibre` | Same observed state forces the same entire suffix under arbitrary StatePolicy. |
| F2 | `ForwardPolicyGoal` | `forward_policy` | For each bounded prefix and Borel state rule, construct a Borel deviation rule satisfying all of Preserves. |
| F2 | `ReversePolicyGoal` | `reverse_policy` | For each bounded prefix and Borel deviation rule, construct a Borel state rule satisfying the same Preserves. No injective E/A or disturbance-history recovery assumed. |
| F2 | `EpigraphEqualityGoal` | `epigraph_equality` | Equality of full sets of feasible real eta, including infeasible cases. No minimizer, bounded-below proof or extended-real corollary is smuggled into this equality. |

Natural numbers in expansion use zero extension only outside executed block positions. At terminal T, q>0 selects the suffix branch; at t=r the prefix branch supplies exactly prefixState. Chronological control/noise switch with t<r, so the transition after the measurement uses suffix index zero. The chronology goal explicitly makes this interface a proof obligation. No concrete off-by-one mismatch was found.

The v1-to-v2 diffs were independently recomputed from original readonly files and byte-compared with both recorded diffs. Changes are namespace/import relocation, separate structure field binders, reserved identifiers `at`/`prefix` replaced by `blockAt`/`prefixState`, explicit recursive D binder, method namespace and transparent subtype abbreviations, plus `open Data`. The coefficient formula, all quantifiers, positivity/box assumptions, Borel fields, terminal rows, signed criterion and Preserves components were not weakened. The old v1 did not elaborate, so this is a syntactic/intended-statement comparison, not an assertion of equality between two previously kernel-checked models.

## Controls and remaining coverage

C1–C6 remain the frozen specifications in `bridge/formal-v1/statement-map.md`, and must be instantiated with `BridgeFormalV2.Data` and its methods in later independent replay evidence. They have not been executed or discharged here:

- C1: n=2,m=1,p=2,r=q=1; nonzero disturbance, bounded controls, feasible negative signed bound -2 for the explicit constant witness.
- C2: the same nonempty control/noise data, unreachable second-coordinate terminal target [5,5]; expected empty sourceLevels.
- C3: distinct prefix histories with the same measured state and independently varied future; expected identical full suffix under arbitrary policy.
- C4: signed polarity at -2 versus -3 and after flipping c; prevents absolute-value or nonnegative-cost substitution.
- C5: deliberately false SourceBound(-3) must be rejected for its actual zero-disturbance contradiction, not an import/environment error.
- C6: a single observed state cannot choose +1 versus -1 based on unseen future noise; expected logical contradiction, not missing imports.

This review adds no model-control proofs, negative proof candidates, custom axioms or placeholders. NonemptyBlocksGoal itself is unproved; structural inspection of its actual box hypotheses does not count as kernel nonvacuity evidence.

| Coverage | Statement/proof status after this review | Separate remaining obligation |
|---|---|---|
| F1 | Four exact propositions elaborated; zero proofs | Derive recurrence expansion, split and chronological/terminal identities. |
| F2 | Five exact propositions elaborated; zero proofs | Both Borel witness maps, actual-image equality, fibres and full signed-level equality. |
| Prerequisite | One exact proposition elaborated; zero proofs | Block inhabitation in Lean. |
| F3 | No sealed proposition/proof here | Universal support equivalences for actual independent future box and every signed terminal row; preserve whole-block timing. |
| F4 | No sealed proposition/proof here | Exact finite fixed-recourse reduction and Borel state implementation for all reachable real states, including relative dimension and degeneracy. |
| Unrestricted source comparison | Not proved by the ten targets | Existence/level comparison with unqualified source strategies; do not confuse it with arbitrary-policy bijection or assume selection. |
| Extended value/attainment and off-domain rules | Not formalized here | Correct infinity conventions, any attainment theorem, and total policy extensions require separate statements. |
| Proof replay/axioms/C1–C6 | Not run; no proofs in this stage | Execute exact inventory and inspect transitive axioms against only propext/Classical.choice/Quot.sound; run declared controls separately. |

## Handoff

Proceed only with the frozen ten-target F1/F2 package, without editing sealed definitions, goals, inventory or imports silently. Any required amendment must stop proof development and return under a new review identity. Future proof success must be supported by actual proof-file compilation, exact declaration types and axiom output; elaborated `def ... : Prop` is not proof evidence.

No new network activity, full-Mathlib import, cleanup of others' data or background process was used. Every monitored subprocess remained above the 600 MiB reserve; final evidence validation records the minimum observed sample and remaining disk bytes. Changes in global free space are observations, not attributed to this worker. Actual provider billing, native model retries and full OS containment remain unknown. Original scientific-success goal and whole-transfer acceptance remain unmet.
