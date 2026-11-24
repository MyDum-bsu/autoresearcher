# S2 statement fidelity review — blocked before proof

Task: aro-discovery-k4t. `readyForProof=false`. The independent compiler attempts both failed on absent imports, before elaborating the prepared model or goals. The full trusted compiled definition/import closure is unavailable. S3 must not start on this package.

The reviewed local source text retains the requested real linear OGU model and the measured-state/whole-suffix information pattern. No concrete source-text counterexample to the scoped F1/F2 target was identified. This is structural criticism by an LLM, not a mathematical verdict, successful typecheck, nonvacuity proof, or scientific acceptance. F3/F4 are expressly missing. The original operational acceptance remains withdrawn, and the historical exact-instance evidence remains scoped and unchanged.

## 1. Scope and identities

Verified before writes: worktree `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`. New files only under `artifacts/bridge/formal-v1/statement-review/`. No S1 model, goal, package, dependency, setup result or legacy source/checker/result was repaired. No proof was written. No Lake update/build/cache-helper invocation, network retrieval, comparator execution, scientific-state write, attestation, commit, task mutation, nested agent/workflow or automatic retry was performed.

Read the complete formal-repair spec, FOUNDATION, AGENTS, applicable session/literature/oracle/logika/style instructions, transfer-v1 correspondence, S1 model/goals/map/inventory/seal/collector/report, and actual A4 original physical pp2–6. The old glossary's A=I/discrete-sign/L1 description conflicts with A4; it was not used as the mathematical model and was not edited. Novelty is not this milestone's gate.

Candidate SHA256 identities match S1's frozen seal:

- `bridge/formal-v1/lean/BridgeFormal/Model.lean`: `188a55848460b83105cf2eccd8633fc08a2e8f393bbaebb1e26ed05329073323`.
- `bridge/formal-v1/lean/BridgeFormal/Goals.lean`: `ef3a0cbd1bd40b39403675544cce325dc683dd85b93b5b52030a4aa3ba7e7957`.
- `bridge/formal-v1/expected-theorems.json`: `addd28b9e7075a174544803330a7bc4042bd97171d372b0fff50761ab230717e`.

`seal-comparison.json` records all ten candidate file comparisons. `environment.json` records matching eight sealed upstream file identities, exact revisions, package configuration and executable hashes. This confirms candidate identity, not correctness of definitions or a resolved Lake environment.

## 2. Original-source audit

Original PDF: `corpus/our_papers/A4_Дмитрук_2022.pdf`, SHA256 `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`. Fresh direct layout and coordinate extractions are `A4-p2-6.txt` and `A4-p2-6-bbox.html`. Five fresh rendered pages and `A4-pages-contact.png` preserve the visual formula check. `source-extraction.json` records commands and exit 0 for both extractions; rendering also completed in this session.

| Original anchor | Source requirement inspected | Prepared source text |
|---|---|---|
| Physical p2 / printed p67, (1.1) | Stationary x(t+1)=Ax(t)+Bu(t)+Mw(t), real dimensions, specified x0 | Model:18–35,48–54; E renames source M, control dimension m avoids collision with closure r |
| Physical p2 / printed p67 | Componentwise bounded controls; infinity-norm disturbance bound wmax>0 | Model:29–32,39–42; positive rho and full continuous componentwise boxes |
| Physical pp2–3 / printed pp67–68, (1.2)–(1.3) | All disturbances; both terminal directions; signed linear c^T x(T) | Model:112–125, no norm/absolute value/nonnegative cost coercion |
| Physical p3 / printed p68, nominal expansion and (1.5) | State offset A^T x0; omitted optimization constant must not disappear from guarantees | Model:59–64,104–109 retains the initial state and nominal offset; expansion is a proof obligation |
| Physical p4 / printed p69, Assumption 1 | Exact measured state; select the next entire block at closure | Model:69–95, whole q-block rule on reachable states, no future-noise argument |
| Physical p5 / printed p70, (2.1) and sequential systems | Initial open-loop block then state-dependent suffix using same dynamics | Model:52–57,88–101; Goals:17–32 explicitly demands chronology and terminal expansion |
| Physical p6 / printed p71, Assumption 2 and V=+infinity convention | Source later assumes nonempty closure sets; infeasible positions assigned +infinity | No terminal-feasibility/closure-set-nonemptiness field is imposed. Model:122–125 uses feasible epigraph sets, not a real infimum of the empty set. Extended-value theorem is absent, not asserted. |

Specialization is exactly one fixed measurement, r>0, q>0, T=r+q. It does not purport to cover several measurements, intermediate state constraints, time-varying dynamics or correlated uncertainty. These are disclosed scope limits, not a toy replacement.

## 3. Complete local definition expansion and library boundary

Every prepared local definition and structure body was read in full, including both modules and root imports. `Model-numbered.txt`, `Goals-numbered.txt` and `local-definition-closure.json` preserve all 44 local declaration bodies and their lexical local references. The latter's references are navigational, not elaborator-resolved dependency edges. There are no other local trusted model modules behind the root import file.

The expanded local dependency chain is:

1. `Vec`, `Block`, `Data` → real finite products, arbitrary stationary linear maps A/B/E/H/c, positive n/m/p/r/q, ordered control bounds and positive disturbance radius. There are no invertibility, nonzero-rank, reachability, terminal-feasibility, trajectory-expansion, selection or correspondence assumptions.
2. `ControlOK`, `NoiseOK`, `ControlBlock`, `NoiseBlock`, `at` → bounded block subtypes and zero extension outside their executed horizon. `at`'s zero is an explicit mathematical extension, not recovery from missing input. Executed block indices remain inside their block; Goals:17–25 must establish phase boundaries against the actual recurrence.
3. `step`, `run`, `prefix`, `nominal`, `deviation` → chronological recursion on natural time. Prefix and zero-control deviation are separately computed, not defined to satisfy a desired split.
4. `Z`, `S`, `observed`, `observedDeviation` → actual ranges of recurrence maps and their subtype observations. A range membership proof is in Prop, not an extra data-valued observation of disturbance history.
5. `StatePolicy`, `DeviationPolicy`, `sourceSuffix`, `aroSuffix` → separate measurable rules from the appropriate reachable subtype to bounded entire suffix controls. `StatePolicy a` knows the fixed first-stage a via its type/domain; y is selected for that same a before disturbances in the epigraph witness.
6. `sourceTrajectory`, `aroTrajectory`, `chronologicalControl`, `chronologicalNoise` → the two phases, with one rule evaluation at the measurement and two independent noise blocks. No suffix reoptimization after seeing the future is encoded.
7. `expansion`, `aroTerminal` → independently specified finite linear sum, with power exponent k-1-t and the initial-state term. Its equality with run is NOT assumed in Data or any goal premise.
8. `Rows`, `SourceBound`, `AROBound`, `sourceLevels`, `aroLevels` → actual terminal bounds/cost, both robust quantifiers, one initial program and one contingent rule, then every disturbance. No sampled, rational or vertex-only substitution is used in F1/F2.
9. `Related`, `Preserves`, all ten `*Goal` definitions → demanded conclusions, including translation equations, control/trajectory preservation and every signed real epigraph bound. No goal is passed into Data, SourceBound or AROBound as a hypothesis.

The library boundary cannot be declared complete. The new comment-aware bounded source traversal visited 1,557 available modules and 136 bundled core import leaves, preserving source hashes/imports and core olean identities in `source-import-inspection.json`. Dependency sources including Aesop, Batteries, Qq, ProofWidgets, ImportGraph, LeanSearchClient and Plausible are absent. All eight non-mathlib manifest dependency directories are absent. The inventory still treats the `all` modifier in `import all Init.Data.Nat.Bitwise.Basic` as a token/module candidate; that entry is NOT an actually missing dependency (direct source example: Mathlib/Data/Int/Bitwise.lean:12). Core identities are leaves, not recursively parsed kernel dependencies. Thus neither this inventory nor S1's comment-sensitive regex is a complete compiler closure. Missing dependencies and imports are an explicit blocking gap, not silently replaced by trusted hypotheses.

Relevant pinned library definitions were directly inspected: BorelSpace/Basic.lean:51–52 defines the Borel sigma algebra; :113–115 defines BorelSpace; :187–189 supplies inherited subtype Borel structure; :646–649 supplies countable-product Borel structure; :712–716 supplies real Borel instances. MeasurableSpace/Constructions.lean:184–186 uses comap for subtype measurability, and :223–238 provides subtype construction/composition lemmas. These support the intended reading of the source text; instance synthesis for the actual model is NOT compiler-confirmed.

## 4. Fidelity checks and obligations

### Information and first-stage dependence

Model:66 defines Z using only the actual zero-initial/zero-control prefix response; Model:67 separately defines S(a) from the actual prefix trajectory. This avoids assuming S(a)=nominal(a)+Z. Goals:35–37 demands equality of the translated actual image to Z for every a. Until proved, syntactic independence of Z alone is not sufficient bridge evidence.

The rules in Model:69–75 have no future-block input. `SourceBound` fixes pi and then quantifies wm/wp. In sourceLevels, a and pi are existentially chosen outside these universal disturbances. `AROBound` quantifies xi then every wp, with a single previously chosen y. The source rule cannot distinguish equal measured states merely because different prefix paths realize them. Goals:62–65 demands this fibre equality explicitly. The type-level first-stage dependence and stored nominal subtraction are legitimate known information, not future observations.

### Measurability and policy domains

Both policy structures require `Measurable rule`; neither contains a field asserting a desired translation or feasible selection. Domain S(a) versus Z is explicit and reachable-only. Control membership is enforced by the target subtype. Forward and reverse goals demand a policy in the other measurable structure; they cannot be discharged merely by producing an arbitrary nonmeasurable function.

A4 physical pp2–6 does NOT state Borel regularity. The formal target follows the explicitly declared transfer-v1 Borel implementation convention. This is a scope qualification. F1/F2 could establish correspondence between those Borel classes without establishing equivalence to every unqualified source strategy. The latter requires the separately missing F4 existence/selection coverage; no arbitrary-policy theorem or total off-reachable-state extension is present. This qualification blocks any full-source/full-bridge acceptance, but is not itself a discovered contradiction in the deliberately scoped F1/F2 target.

### Domains, nonvacuity and signed cost

Real finite products, positive horizons and radius, and ordered finite control bounds do not syntactically impose contradictory data fields. Degenerate controls and rank-deficient A/E/images remain allowed; disturbance paths are continuous boxes rather than just signs, even if an allowed E annihilates their state effect. NonemptyBlocksGoal explicitly requests nonempty control and noise block types. Its proof and a compiled Data witness are absent: this review does not certify model inhabitation by Lean.

Terminal gmin/gmax need not be ordered, so terminal infeasibility is representable. Even with consistent target bounds, robust dynamics can be infeasible. Empty sourceLevels/aroLevels are meaningful. `Rows` keeps lower and upper H rows and `D.c x <= eta` with eta:ℝ and unrestricted c. No ENNReal, |c|, L1 terminal objective, sInf, attainment or value claim occurs. The intended nonvacuity and signed-polarity controls C1–C6 were frozen in statement-map.md; none was executed here. An import failure is not a successful negative control.

### Dynamics obligations

F1 uses actual run with stationary real maps. The expansion goal quantifies over every finite k and unrestricted real control/noise blocks, retaining x. Prefix split, sequential chronology including the t=r boundary, and suffix expansion have separate goals. F2 preservation includes the same actual suffix controls, all times t<=r+q and SourceBound iff AROBound for every eta using the same policy witness. These are more than a bare abstract factorization lemma, but remain unproved proposition definitions. No induction or library recurrence proof was supplied in S2.

## 5. Exact target and coverage inventory

All names below have namespace `BridgeFormal`; future proof declarations would have namespace `BridgeFormal.Proofs`. Exact proposition bodies and all Data assumptions are preserved in `Goals-numbered.txt`, `Model-numbered.txt` and `local-definition-closure.json`; the listed SHA256 identities fix those bodies. Each is `def ... : Prop`, not an existing theorem. All ten expected type names occur in the reviewed source; there are zero proof files/declarations.

| Node | Exact proposition / source line in Goals.lean | Expected future proof name | Current dependency obligation |
|---|---|---|---|
| prerequisite | NonemptyBlocksGoal:39 | nonempty_blocks | Construct admissible block witnesses from ordered bounds and rho>0 |
| F1 | ExpansionGoal:8 | expansion | Derive the finite expansion from run for all k,x,u,w |
| F1 | PrefixSplitGoal:13 | prefix_split | Actual prefix = nominal + deviation |
| F1 | SourceChronologyGoal:17 | source_chronology | Initial state and every chronological step, including phase transition |
| F1 | SuffixExpansionGoal:27 | suffix_expansion | Actual terminal source trajectory = suffix expansion with the prefix split |
| F2 | ExogenousImageGoal:35 | exogenous_image | Both inclusions of translated actual reachable image = Z |
| F2 | ObservationFibreGoal:62 | observation_fibre | Same measured state implies same whole suffix |
| F2 | ForwardPolicyGoal:50, using Preserves:42 | forward_policy | Measurable Z-rule, Related, equal controls/trajectories and all robust bounds |
| F2 | ReversePolicyGoal:54, using Preserves:42 | reverse_policy | Measurable S(a)-rule with the same preservation conditions |
| F2 | EpigraphEqualityGoal:58 | epigraph_equality | Equality of feasible real epigraph-level sets via both witness directions |
| F3 | NO PROPOSITION | none | Universal exact future-box support elimination for signed cost and both terminal directions, with whole-block timing |
| F4 | NO PROPOSITION | none | Fixed-recourse finite formulation and measurable real-state implementation, including relative dimension/degenerate images; distinguish state/terminal images from a policy bijection |

For every F1/F2 row: current proof is absent; the shared model import and goals import failed; printed theorem types and axiom audit are NOT RUN; C1–C6 are NOT RUN. For F3/F4: statements, proofs, compiler results, axiom inventories and node-specific controls are absent. This table does not relabel F1/F2 or a factorization lemma as the whole bridge.

## 6. Observed environment and raw checks

Executed once: `timeout 150 python3 -B artifacts/bridge/formal-v1/statement-review/audit.py` -> collector exit 0. Collector success means evidence collection completed, NOT that Lean succeeded. The script never invokes Lake's resolver or downloads. Each Lean subprocess has a 45-second timeout and task-local TMPDIR/cache/explicit LEAN_PATH; output destinations are inside this review directory, never the prepared project.

Exact command arrays, cwd, environment overrides, stdout/stderr and exits are in `typechecks.json`. From `bridge/formal-v1/lean`:

| Actual compiler invocation (installed absolute binary) | Exit | Raw result |
|---|---:|---|
| `lean -o <review>/compiled/BridgeFormal/Model.olean BridgeFormal/Model.lean` | 1 | Model.lean:1:0: missing Mathlib.MeasureTheory.Constructions.BorelSpace.Basic object file |
| `lean -o <review>/compiled/BridgeFormal/Goals.olean BridgeFormal/Goals.lean` | 1 | Goals.lean:1:0: missing BridgeFormal.Model object file |

Separate `model-typecheck.*` and `goals-typecheck.*` preserve raw streams and exits. No statement body was elaborated, no compiled target produced, and no proof checked. `lake build`, `#print` types/axioms, semantic controls and source-policy selection proofs: NOT RUN, for the documented environment/proof absence. No fallback to legacy exact-instance replay was attempted.

Installed binaries remain Lean 4.35.0-rc2 commit `11acb17ec6b07a8f9e9173e6845197929540936b` and Lake 5.0.0-src+11acb17. Mathlib checkout HEAD is exactly `c58b47adb340faa641e363aef2a460dc534bf172`, with empty git porcelain output. Pinned upstream LICENSE/toolchain/config/cache-source hashes match the candidate seal.

The S1 policy blocker is corroborated: pinned Cache/Requests.lean:351–352 returns curl `--retry 5` unconditionally; direct source search finds its use in download paths at :532 and :792. Cache/Cli.lean:22–26 lists supported named options and flags without a retry-disable option. This establishes why the inspected route conflicts with the no-automatic-retry instruction. It does NOT prove all official provisioning routes are impossible. S2 has no authority to repair or reprovision the prepared environment, and did not do so.

## 7. Disposition and boundaries

Evidence-consistency validation checked the 44 local declarations, ten expected target names, two import failures, absent proof/compiled files and unchanged candidate/source identities; see `validation.json`. The technical-style diagnostic (`python3 -B .../lint_technical_style.py report.md --language en --extended`) returned exit 1 for one `passive-result` wording advisory in the scope-prohibition paragraph. `style.stdout`, `style.stderr` and `style.exit` preserve it. The advisory was reviewed and the prohibition wording retained; this style result has no mathematical significance.

Blocking findings:

- **B1 — environment not ready:** actual model and goal compiler attempts fail at imports. Neither type correctness nor measurable-instance elaboration has been observed. Resolve the setup authority/route outside this read-only stage before any proof attempt.
- **B2 — incomplete trusted import closure:** absent pinned dependency sources/compiled imports and lexical-only inventories prevent freezing a compiler-resolved trusted closure. The local model/goal bodies have been expanded and read; the full elaborated library closure has not and cannot be claimed available.

No additional concrete blocking local-text fidelity defect was established. This statement is deliberately weaker than approval: unresolved elaboration, nonvacuity and imported-definition trust remain blockers. The Borel-versus-unqualified-source distinction, F3 and F4 remain visible full-bridge obligations even if F1/F2 later compile and are proved.

Recommendation: keep S3 blocked. Have an authorized setup stage supply the exact pinned dependencies/imports through an approved no-retry route, freeze the resulting resolved identities, then return the unchanged or newly identified statement package to S2. Any statement amendment needs a new identity and review. Do not launch an automatic repair loop from this report.

`readonly-comparison.json` shows zero changed hashes among 44 snapshotted candidate/setup/dictionary/PDF/correction files; upstream sealed file identities also match. This bounded check is not a full host filesystem audit. Newly generated review evidence is standalone and does not restore the withdrawn operational acceptance in `artifacts/bridge/transfer-v1/coordinator/acceptance-correction.json`. Actual billing/native retries inside third-party processes and full OS containment remain unknown. Human semantic/scientific authority remains separate from both this criticism and any future kernel proof.
