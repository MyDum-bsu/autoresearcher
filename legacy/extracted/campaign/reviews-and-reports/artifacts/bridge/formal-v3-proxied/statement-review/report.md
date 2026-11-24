# F3 sealed-statement review

Task: aro-discovery-k4t. Scope: structural source/statement review before proof, not mathematical acceptance.

The first new inspection command failed on the review-only formatting option `pp.width`. The failure is preserved in `inspection.json` and `inspection.stdout`; it is not a mathematical negative control. A separate `InspectionV2.lean` omits only that option and compiled with exit 0. No candidate, parent definition, proof, or old evidence was edited.

**readyForProof: true.** No concrete scoped F3 semantic blocker was found. All four sealed F3 targets remain unproved. The whole bridge is not accepted: F4 and Borel-versus-unrestricted source-policy existence remain separate missing obligations. This readiness decision authorizes a conditional proof attempt against unchanged targets; it is not a Lean verdict or scientific promotion.

## Authority, identities, and execution

The worktree is `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`. The active project is `bridge/formal-env-v2/lean`. The proxy recovery specification overrides the older recovery evidence paths; all new files for this worker are under this report's directory. The original interrupted review remains partial work, not an accepted review.

Read in full: FOUNDATION, AGENTS, the F3/proxy/offline specifications, relevant formal-v1 repair and formal-v2 continuation specifications, the V3 candidate, parent Model/Goals, and Dynamics/Policies/Inventory. Applied session, worker, oracle, logic, style, and Beads guidance. `bd prime` and `bd show aro-discovery-k4t` were read; the parent epic was not claimed, closed, or changed by this bounded worker. Repository-wide bootstrap gates and scientific CLI writes were intentionally not run: this task permits only scoped evidence writes and local compiler checks.

`identity-before.json` and `identity-after.json` each check 13,399 protected identities with zero mismatches. They cover the inherited source/import/compiler identities, candidate/inventory and parent seals, previous proof files/builds, preserved controls, the original PDF, and all 55 interrupted-review files against the recovery manifest. `protected-identities.json` contains the exact path/hash map. Before/after comparison does not establish upstream provenance beyond the inherited seals.

Authoritative identities:

| File | SHA-256 |
|---|---|
| `bridge/formal-env-v2/lean/BridgeFormalV3/Goals.lean` | `e447ec1e273de169b49bea44b10566581db68bbe951c3576eed13ca42e570f42` |
| `bridge/formal-v3/expected-theorems.json` | `59490a3364441e3d2beae834f6b7db3cc5993de0e60a261cf2968d70f2710775` |
| `artifacts/bridge/formal-v2/proof/proof-seal.json` | `75a63a78a7ad1c8bbe9daa3f41eb6957f709b546d63df17f61e8452af08e1d1c` |
| `corpus/our_papers/A4_Дмитрук_2022.pdf` | `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420` |

Fresh raw `lean -o <this-review>/build/<module>.olean <module>.lean` checks returned exit 0 for Model, Goals, Dynamics, Policies, Inventory, and the exact V3 Goals source. Dependency resolution uses the isolated new build followed by pinned dependency/compiler paths, excluding the mutable project build. The default Lake library target was not substituted for V3. The compiler version and every command/exit/output hash are recorded in the adjacent JSON/stdout/stderr files.

The successful inspection printed actual expanded definitions and all four propositions, enumerated 3,319 imports, and reported all four expected F3 proof declarations absent. Fresh Inventory compilation checked all ten parent target types and printed transitive axioms. Each uses only `Classical.choice`, `Quot.sound`, and `propext`. These are parent F1/F2/prerequisite results, not F3 proofs. No full Mathlib import, dependency acquisition, installation, model request, comparator, nested agent, or workflow was run.

The corrected proxy launch was not repeated here. `worker-transport-scope.json` records that inherited `NODE_OPTIONS` contains `--use-env-proxy` and existing HTTP/HTTPS proxy variables are present, without values. This local worker made no transport probe; physical routing and model authorization are not independently certified by this review.

## Primary source and mapping

Independently rendered and read original A4 physical page 3, printed page 68 (`A4-p3.png`), not merely its earlier review's conclusion. Fresh `pdftotext -f 3 -l 3 -layout` agrees byte-for-byte with the page in the preserved pp2–6 extract. The latter was read for the wider recurrence, boxes, one-measurement/block timing, and feasibility context. Original page coordinates from the preserved `A4-p3-bbox.html` and `source-evidence.json` remain available; they were not regenerated unnecessarily.

Physical p3 displays

- `gamma_0 = wmax sum_{s=0}^{T-1} ||c^T A^s M||_1` and the corresponding `gamma_i` for each signed H row;
- the tightened set `gmin + gamma <= H x <= gmax - gamma`;
- equation (1.4), the signed nominal criterion `c^T x^0(T) + gamma_0`;
- equation (1.5), the terminal expansion with powers `A^(T-t-1)` and both terminal inequalities.

For this suffix, `T` becomes `D.q`, `M` becomes `D.E`, and `wmax` becomes `D.rho`. A4's source sums powers in ascending order; the candidate associates each chronological noise coordinate at time `t` with power `q-1-t`. This is the reversed ordering of the same finite powers for support, not a change to dynamics. Source p2 supplies the stationary real recurrence and continuous infinity-norm box; pp4–6 supply the selection of a whole control block at a measured state. The source does not give this candidate a formal proof automatically.

## Full definition and quantifier audit

Paths below are relative to `bridge/formal-env-v2/lean/`.

### Actual recurrence and finite coefficients

`BridgeFormalV2/Model.lean:56–62` defines `step x u w = A x + B u + E w` and chronological recursion. `Model.lean:112–118` defines expansion and the actual sealed ARO terminal. Parent `Proofs/Dynamics.lean:43–70` connects this finite expansion to the recursion, by induction and finite-sum identities, for arbitrary real states and blocks. The newly compiled parent is not a hypothesis asserting the desired support identity.

`BridgeFormalV3/Goals.lean:18–19` defines the future response by that actual recursion with zero initial state and algebraic zero input. `Goals.lean:26–27` uses columns `A^(q-1-t) (E e_i)` for every `t : Fin q` and `i : Fin p`. For `t < q`, natural subtraction represents the intended nonnegative exponent; the last noise has power zero. The short recurrences have noise terms `E w0`, then `A E w0 + E w1`, then `A^2 E w0 + A E w1 + E w2`, matching these columns. This is a structural index audit, not sampled evidence for a universal theorem.

The coordinate expansion needed by the prover is the finite coefficient representation of the actual response using those columns and real `wp.val t i`. Each coordinate is present; no replacement by noise vertices is built into the type. `basisVector` at `Goals.lean:10–11` has exactly one unit coordinate. E and A are real linear maps, so no affine drift or time-varying matrix was silently introduced.

**Zero input is algebraic decomposition only.** `run` accepts arbitrary vector sequences, not `ControlBlock`. Neither `futureNoiseResponse` nor F3.1 asserts `ControlOK 0`. Physical controls remain `(y.rule xi).val`, with the sealed subtype bounds, in the nominal term. Control boxes may exclude zero; no extra zero-feasibility hypothesis is required or allowed.

### Continuous box, support, and attainment

`Model.lean:18–44` has positive state/control/noise dimensions, positive prefix/suffix horizons, and `rho > 0`; no assumption restricts rows, E, or A to nonnegative values. `NoiseOK` and `NoiseBlock` at lines 48–50 quantify over all real coordinates in `[-rho,rho]`, independently at every time. Future `NoiseBlock q` is not conditioned on prefix noise, control, state, or policy. Prefix `Z` is an actual range at line 74 and does not depend on `a`.

`Goals.lean:30–31` defines the proposed support directly as `rho * sum_t sum_i |row(column t i)|`; it does not define it to be an unknown supremum, or assume equality to one. F3.2 must establish both a bound for **every** valid real noise block and an attaining valid block. Its existential witness comes after `D,row`, so it may depend on the direction. The coefficient sign witness required by this target can choose `+rho` when that real coefficient is nonnegative and `-rho` otherwise; zero coefficients cause no domain problem. The prover must establish membership and equality in Lean, not infer them from a few samples.

Zero row, zero E, rank-deficient response, and zero coefficients are permitted and do not force a positive support claim. Parent `nonempty_blocks` supplies actual nonempty noise/control block types; its fresh type/axiom check passed. Control endpoints also give constant measurable policy candidates, so requiring Borel rules is not by itself an empty-domain device. No feasibility of terminal rows is assumed. `rows = 0` is allowed, but the signed cost remains; the target is not restricted to that case. Inconsistent terminal bounds remain representable and must be handled by the equivalence.

### Signed rows, both terminal sides, and eta

`terminalRow` at `Goals.lean:33–34` is `(proj i).comp H`. The lower side at lines 41–42 is exactly `(-H_i) z + support(-H_i) <= -gmin_i`; the upper side is `H_i z + support(H_i) <= gmax_i`. Symmetry of the real box accounts for the equal magnitudes in the source gamma notation. The candidate need not assume that equality as a hypothesis: F3.2/F3.3 quantify over all linear rows, including negatives.

The criterion at line 43 is `c z + support(c) <= eta`. The original signed linear row c is retained; only its directional noise coefficients are inside absolute values. Neither `|c z|`, an L1 terminal objective, a nonnegative epigraph type, nor a changed bound occurs. F3.3 allows every real `bound`; F3.4 allows every real `eta`. Infeasibility and negative criterion values are not discarded.

### One fixed suffix before universal future noise

`Model.lean:77–83` defines separate state and deviation policies, including measurability. `y.rule : Z -> ControlBlock q` has no future-noise argument. `aroTerminal` uses the same `y.rule xi` for every `wp`. F3.4 quantifies `D,a,y,eta` before the equivalence; `AROBound` then quantifies `xi` and `wp`. `TightenedAROBound` uses the same D, a, y, eta and all xi; it does not select a different suffix per row or per future disturbance.

Each row may have its own attaining disturbance in F3.2. The terminal/cost conjunction does not demand a common jointly extremizing disturbance. Rowwise reasoning preserves universal conjunctions; it does not exchange `exists control` with `forall future noise`. A future-aware rule `Z -> NoiseBlock q -> ControlBlock q` is not the sealed `DeviationPolicy.rule` type. This is a static type observation, not an executed negative control.

Parent `Policies.lean:26–52` connects sealed ARO bounds to actual source trajectories; lines 54–100 provide the bidirectional Borel policy correspondence. Those results preserve the same fixed whole suffix. Their fresh kernel checks do not establish unrestricted source-policy correspondence.

## Exact target inventory and remaining proof work

All entries below are definitions of propositions, not theorem declarations. The namespace prefix is `BridgeFormalV3`; source is `BridgeFormalV3/Goals.lean`.

| Proposition | Source | Required content | Expected declaration | Current evidence |
|---|---|---|---|---|
| `FutureExpansionGoal` | 50–53 | Actual sealed ARO terminal equals nominal terminal plus actual recursive future response | `Proofs.future_expansion` | Proposition elaborated; declaration absent |
| `AttainedSupportGoal` | 56–59 | Bound on all continuous box noise plus a valid attaining witness for every real linear row | `Proofs.attained_support` | Proposition elaborated; declaration absent |
| `RobustRowGoal` | 62–65 | Universal translated row bound iff nominal signed row plus exact proposed support is within the same real bound | `Proofs.robust_row` | Proposition elaborated; declaration absent |
| `ExactTighteningGoal` | 68–70 | Actual `Data.AROBound` iff both nominal terminal sides and signed cost are tightened, for the same a,y,eta | `Proofs.exact_tightening` | Proposition elaborated; declaration absent |

No conclusion-as-assumption, support equality premise, empty-noise restriction, finite-sampling quantifier, weakened criterion, or future-dependent action was found in these statements. A proof developer still has to discharge all four exact inventory types, with the actual coefficient expansion and sign-witness box membership established in the kernel. This report does not supply those proofs.

## Commands, failure classification, and coverage boundary

Executed from the verified feature worktree:

1. `timeout 300 python3 -B artifacts/bridge/formal-v3-proxied/statement-review/replay.py`: six exact source module checks passed; then exit 1 at the unsupported inspection formatting option. Original evidence retained.
2. `timeout 300 python3 -B artifacts/bridge/formal-v3-proxied/statement-review/finish-inspection.py`: explicit review-evidence-only correction, exit 0. Successful actual type/import inspection, direct original-page extraction/render, ten parent axiom checks, four missing F3 declaration checks, and post-run identities.
3. Scoped source scan for `sorry`, custom `axiom`, `unsafe`, `native_decide`, and a full `import Mathlib`: no matches in candidate/parent definition and proof sources. The parsed transitive parent axiom audit is the stronger parent foundation check.

No semantic negative controls or new proof files were created in this statement-review stage. The old fixture-root error and failed C2 are preserved and are not counted as successful controls. The F3 final-review stage must separately predeclare and execute positive support, negative signed row, both terminal sides, too-small support/bound witness rejection, and fixed-block versus future-aware action controls, without disguising import/API errors as mathematical rejection.

No scientific journal, blueprint, glossary, configuration, status, attestation, commit, or Beads update was made. The glossary's legacy A=I/binary-disturbance/L1 bridge-class description does not describe the actual source-native sealed Data; it was not used to weaken the reviewed model and was left unchanged. All new compiler/cache/render products stay in the assigned review directory. The post-run free space was 1,461,170,176 bytes, above the 629,145,600-byte reserve.

**Recommendation:** proceed only to the authorized conditional F3 proof stage against the unchanged candidate and four-entry inventory. Keep whole-transfer acceptance false even if that later stage succeeds; F4 finite/measurable implementation and Borel/unrestricted-source comparison remain outside this readiness decision.
