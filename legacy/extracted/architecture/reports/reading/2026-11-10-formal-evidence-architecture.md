# Formal-evidence architecture for aro-discovery

**Research date:** 2026-11-10. **Disposition:** architecture recommendation, not implementation or scientific attestation.

## 1. Direct answer

Adopt a **sealed-statement, independently checked proof workflow**. Treat these as separate obligations:

1. **Statement fidelity:** the formal definitions and quantifiers express the approved scientific claim.
2. **Proof validity:** the submitted proof establishes that exact formal statement under an explicit axiom policy.
3. **Scientific interpretation:** applicability, significance, attribution and novelty remain separate review questions.

A successful Lean build addresses neither the first nor the third obligation by itself. The official Lean manual explicitly distinguishes proof validity from statement meaning and describes progressively stronger validation mechanisms. [L1, “Printing Axioms,” “Gold Standard,” “Remaining Issues”]

**Recommended first slice:** formalize the equivalence between a policy using **one exact state measurement at a fixed closing instant** and a scenario formulation whose second-block programs agree whenever the measured states agree. Include the actual discrete dynamics, control bounds, terminal feasibility and objective. This is operating infrastructure, not a novelty claim or a preselected central dissertation theorem.

Use Lean/mathlib directly for this slice. Adopt leanblueprint as a generated explanatory view. If interactive proof repair later needs a Python interface, evaluate pinned LeanInteract first. Defer a search population, learned premise-retrieval pipeline and custom MCP integration until a smaller loop demonstrates a concrete limitation.

## 2. Verified local baseline

### Repository identity and scope

Read-only Git checks established:

- Source checkout: `<workspace>/aro-discovery`, branch `research/autonomous`.
- Intended output worktree: `<workspace>/aro-discovery-architecture`, branch `task/aro-discovery-dub-architecture`.
- Both HEADs: `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`.
- The output worktree was clean at inspection. The source checkout contained pre-existing modifications and untracked research material; these were not treated as committed evidence.

Commands inspected were `git rev-parse --show-toplevel`, `git rev-parse --abbrev-ref HEAD`, `git rev-parse HEAD` and `git status --short` in both trees.

FOUNDATION requires code/Lean judging, human scientific authority and human review sessions. It expressly rejects two LLM products as verification. Its build requirement is necessary but should not be interpreted as sufficient evidence of correspondence. [Local: `FOUNDATION.md:97–112`, §§7 and 9; `AGENTS.md`, “Iron rules,” items 2–4]

### Version baseline

- `lean/aroform/lean-toolchain:1` specifies `leanprover/lean4:v4.35.0-rc2`.
- `lean/aroform/lakefile.toml:3` selects `Aroform` as the default target. Its mathlib requirement does not specify a revision in that file.
- `lean/aroform/lake-manifest.json:4–13` resolves mathlib to `c58b47adb340faa641e363aef2a460dc534bf172`.
- A read-only Git check of the local mathlib dependency returned that same revision; its `lean-toolchain:1` also specifies `v4.35.0-rc2`.

**Decision:** preserve the existing toolchain and complete dependency manifest together. Do not update dependencies as part of proof repair. An upgrade is a separate compatibility decision. No build or installed-tool compatibility was tested here.

### Historical proof labels overstate what can be inferred

The restart audit’s formalization concerns were checked against source rather than accepted from its prose:

| Source observation | Consequence |
|---|---|
| `info_value_monotone` proves `sInf T ≤ sInf S` from `S ⊆ T`. | It is an order-theoretic lemma, not a proof that measured-state policy classes have the required inclusion. `lean/aroform/Aroform.lean:38–39`. |
| `Strategy T := ℕ → (Fin T → Bool) → ℚ`. | The type permits dependence on a complete disturbance path. Causality must be imposed separately; it is not guaranteed by this type. `TwoDDraft.lean:65–68`. |
| `blocks_sum_lower` universally quantifies a fixed list of length/control-sum pairs before existentially choosing signs. | It does not state a lower bound against every adaptive block policy depending on earlier observations. `TwoDDraft.lean:615–623`. |
| `Vtrue` quantifies `Strategy T` without an admissibility predicate or control bound. | `full_upper_value` bounds this defined infimum; it does not establish the intended bounded, information-constrained optimum. `TwoDDraft.lean:803–826`. |
| The manifest explicitly places `TwoDDraft.lean` outside the build. | Its `proven-draft` descriptions are historical metadata, not release verification performed in this session. `lean/formalization.yaml:32–48`. |

The audit’s relevant discussion is `reports/2026-11-10-restart-audit.md:33`; its earlier Lean check was itself not accepted as current verification (`:69`). No historical status was promoted here.

## 3. Statement fidelity: the scientific contract

### Seal definitions as well as the theorem

Before proof search, approve a statement package containing:

- question and claim-scope identifiers;
- informal statement and applicable original-source anchors;
- exact formal declaration and all model definitions on which its meaning depends;
- domains, quantifier order, observation timing and admissibility conditions;
- objective polarity and treatment of infeasibility;
- toolchain, dependency revisions and permitted imports;
- explicit exclusions and unresolved correspondence obligations.

The current glossary defines nonanticipativity through indistinguishability under the prescribed observations and distinguishes a machine-checked statement from finite numerical survival. Use those definitions, not legacy shorthand equating a solution method with a policy class. [Local: `docs/GLOSSARY.md:28–31,40`]

**Proposed enforcement:** proof workers may change proof bodies and approved auxiliary material, but not the sealed statement, model definitions, imports or foundational policy. A required statement change creates a new scope version and returns to correspondence review. Hashing source is useful for identity; it is not a semantic proof.

The release checker should compare the submitted declaration with the trusted statement in a trusted environment. Record its fully qualified name, elaborated type, dependency environment and model-definition identities. Pretty-printed text alone is insufficient protection against misleading notation or instances: Lean’s manual explicitly warns about those remaining interpretation risks. [L1, “Remaining Issues”]

### Formal/informal correspondence is an explicit obligation

Use a mapping table, not a second model’s approval:

| Informal object | Required formal counterpart |
|---|---|
| Available measurement | The actual state/output function produced by the dynamics |
| Policy | A function of available measurement history, or a scenario assignment with proved factorization |
| Feasibility | Control constraints and terminal/path constraints quantified over admissible disturbances |
| Guaranteed cost | Worst cost over the declared scenario set, with minimization/maximization explicit |
| Claimed adaptive lower bound | Quantification over admissible policies before the adverse path is selected |
| Transfer between formulations | Both witness transformations, preserving feasibility and objective |

Human review must approve whether this mapping represents the intended scientific question. Lean can then prove relationships between the formal objects. Two LLMs agreeing about the table does not establish the correspondence. [Local: `FOUNDATION.md`, §7; L1, “Remaining Issues”]

## 4. Concrete first formalization slice

**Proposed scope, not a proved theorem:** finite-horizon discrete linear dynamics with rational data; one fixed closing instant `0 < r < T`; a nonempty finite set of admissible complete disturbance paths; bounded controls; exact state measurement at `r`; hard terminal feasibility; and a declared linear terminal objective.

Choose and document the timing convention: measure `x_t`, choose `u_t`, then apply disturbance `w_t` in the transition. Do not substitute an identity transition matrix or disturbance-prefix observation for the specified model.

Define two representations:

1. **Implementable policy:** a first-block open-loop program `a`, followed by a second-block open-loop program `g(x_r)` selected using the measured state.
2. **Scenario assignment:** the same first-block program `a`, with a second-block program `v(w)` for each admissible path, subject to

   `x_r(a,w) = x_r(a,w′) → v(w) = v(w′)`.

The observation equivalence depends on the first-block controls and dynamics. It must not be silently replaced by equality of disturbance prefixes.

**First release theorem:** for every objective bound `q`, existence of a robustly feasible implementable policy meeting `q` is equivalent to existence of a robustly feasible scenario assignment meeting `q`.

Prove this through:

- evaluation of `g` to obtain the scenario assignment;
- factorization of an observation-consistent scenario assignment through reachable measured states;
- equality of resulting trajectories and terminal costs;
- preservation of every feasibility condition.

Define `g` on reachable measurements first. If a total function is required, specify its extension outside that set and the associated nonemptiness assumptions. Do not hide an arbitrary default inside the model.

This bound-feasibility formulation avoids initially assuming that an optimum is attained or that an infimum of rational values exists in the chosen codomain. Derive value equality only after defining the value and handling infeasibility and boundedness explicitly. In particular, a signed terminal objective should not be silently represented as `ENNReal` without an explicit transformation.

**Excluded:** continuous uncertainty, continuous-time dynamics, noisy/output measurements, multiple closings, affine-rule exactness, optimal schedule selection and the S2–S4 formulas. None follows from the proposed slice. The source papers defining any later target require direct page-level inspection; this research did not independently revalidate A2/A4/A5.

## 5. Proof search and repair

Start with one approved statement and a bounded sequential loop:

`sealed statement → proof attempt → Lean diagnostics → localized repair → independent release validation`.

Retain diagnostics, exact patches, unresolved obligations and stop reasons. A timeout, process failure or exhausted budget is an operational outcome, not a mathematical refutation. No silent retry or model switch is required by this architecture.

AlphaProof Nexus provides primary evidence for the compiler-feedback mechanism and editable-region approach. Its paper also reports two directly relevant failures: moving the central difficulty into a helper lemma containing `sorry`, and presenting unproved, hallucinated helper lemmas as literature results. Its sequence “test lemmas” illustrate semantic smoke tests, not complete correspondence verification. [N1, PDF p. 2, §2; p. 6, “Failure Analysis” and “OEIS”]

**Adopt the mechanism, not its complete orchestration.** Do not permit mutable target parameters or definitions unless parameter search is explicitly part of the approved question. A smaller outstanding goal is not automatically mathematical progress: it may merely restate the target.

Aletheia’s inspected system uses a natural-language Generator, Verifier and Reviser. That is useful as a generation/critique pattern, not as aro-discovery’s proof judge. Its paper separately emphasizes human accountability for attribution beyond formal correctness. [A1, PDF p. 3, §2; p. 7, §3]

Keep draft statements, local `sorry`s and failed sketches in an explicitly non-release area. A promising draft may generate a new candidate lemma; it must not enter the reusable verified library until separately checked under the same policy.

## 6. Trusted kernel and axiom policy

### What the current gate actually checks

`scripts/lean_axioms.py`:

- obtains theorem names from blueprint `\lean{...}` references (`:28–33`);
- returns success when that list is empty (`:37–40`);
- requires matching declarations in `Aroform.lean` (`:41–45`);
- invokes `#print axioms` through an imported module (`:47–55`);
- rejects only a matching occurrence of `sorryAx` (`:59–75`).

It is therefore **not an allowlist for all axioms**, nor a correspondence check. It also does not require a successfully parsed axiom-result record for every requested theorem. Its line-oriented regular expression is an output-format risk; this review did not attempt to exploit it.

### Recommended release policy

Allow only the standard foundational axioms:

`propext`, `Classical.choice`, `Quot.sound`.

Reject `sorryAx`, custom domain axioms, generated native-evaluation axioms and any unknown dependency axiom. Fail closed on an empty expected theorem inventory, missing results, checker errors or an inventory mismatch. A legitimate conditional theorem may quantify a hypothesis, but it must not turn an unproved scientific result into an undocumented premise.

This policy follows the official validation guidance. The manual states that `#print axioms` reports transitive axiom dependencies; it distinguishes standard axioms, `sorryAx`, native evaluation and custom axioms. [L1, “Printing Axioms”; L2, §§8.4–8.5]

**Version caveat:** older advice that checks only `Lean.trustCompiler` is insufficient here. The version-matched manual explains that native evaluation changed from Lean 4.29 and that the old `Lean.trustCompiler` machinery was removed in 4.35. Use a positive allowlist rather than one historical blacklist name. [L1, “On `Lean.trustCompiler`”]

### Independent release validation

Proposed release evidence should include:

1. exact source and dependency identities;
2. successful checking of every named release module;
3. complete transitive axiom results;
4. agreement with the trusted statement and definitions;
5. checker output and artifact digests;
6. separate human correspondence-review disposition.

Lean’s manual recommends `lean4checker` for replaying stored declarations through the kernel and describes comparator’s sandboxed build, exported proof validation and matching against a trusted challenge. Neither removes the obligation to understand the challenge. [L1, “Re-Checking Proofs,” “Gold Standard,” “Remaining Issues”]

**Adoption decision:** design the statement boundary and sandbox boundary now; evaluate version-compatible `lean4checker`/comparator integration before admitting unreviewed generated proofs to release. Their availability and operation in this environment remain untested. Do not run agent-authored elaboration code with production secrets or journal-writing authority: Lean’s manual warns that tactics and meta-code can perform arbitrary actions. [L1, “Re-Checking Proofs”]

Human attestation remains a distinct human action. Generic owner-access delegation must not confer attestation, threshold-changing or journal-publication authority. [Local: `FOUNDATION.md`, §§7,9; `AGENTS.md`, “Iron rules”]

## 7. Acceptance tests for the mapping

These are proposed future acceptance fixtures, **not tests executed during this paused research task**.

| Failure | Required acceptance behavior |
|---|---|
| Vacuity | Reject an accidentally empty scenario set. Include a positive feasibility witness and a deliberately infeasible case so that an equivalence passing only because both sides are impossible is visible. Do not require every legitimate instance to be feasible. |
| Circularity | Reject a helper hypothesis or definition that merely assumes the target bound/equivalence. Inspect expanded definitions, hypotheses and declaration dependency cycles. Unproved scratch helpers must never count as completed proof. |
| Wrong quantifiers | A lower-bound contract ranges over every admissible policy before choosing a path. A mutation replacing an adaptive policy by a fixed list must be identified as a different statement. |
| Anticipation | A policy that changes an earlier action according to a future disturbance must fail admissibility. |
| Wrong observations | Scenario continuations differing after identical measured states must fail the consistency condition, even when disturbance histories differ. |
| Missing dynamics | Removing or replacing the specified transition/observation map must invalidate statement identity or correspondence acceptance. Both witness transformations must preserve the complete trajectory. |
| Missing constraints | Removing control bounds or terminal feasibility must be detected as a scope change. |
| Wrong objective | Exchanging a pathwise aggregate with coordinatewise worst cases, or changing reward/cost polarity, must fail the declared mapping. |
| Hidden dependency gap | A target using an imported `sorry`, custom axiom or native-evaluation axiom must fail release policy. |
| Wrong module/build | A manifest declaration outside the checked release closure, or linked to another declaration, must fail the release inventory. |
| Misleading notation | Changing notation or an instance to alter a model object must not pass trusted-statement/definition comparison. |

These fixtures can falsify a mapping or expose a gate defect. They do not, individually or collectively, replace the general correspondence theorem and human scope review.

## 8. Reuse and adoption decisions

| Tool/family | Decision and trade-off | Evidence that would change the decision |
|---|---|---|
| **Lean + pinned mathlib** | Adopt. Keep project code focused on dynamics, observations, admissibility and witness transformations. Reuse order-theoretic infrastructure rather than rebuilding it. The pinned source contains indexed-supremum monotonicity and corresponding dual declarations. [M1, `Basic.lean:254–279`] | A concrete missing abstraction or a documented incompatibility in the first slice. No broad library migration is justified yet. |
| **leanblueprint** | Adopt as a generated explanatory/dependency view, not a second authority. Its `\leanok` is a claim of formalization; `checkdecls` checks declaration existence, not correspondence or axiom policy. Maintain separate statement/proof readiness. [B1, “Local compilation,” “Editing the blueprint”] | Evidence that generation cannot preserve existing node identities or that maintaining it duplicates scientific state. |
| **LeanInteract** | Preferred candidate for a later Python repair adapter. It exposes command/file execution, proof steps, diagnostics and declaration extraction. Pin the project, REPL revision and package; avoid its latest-version defaults and experimental automatic recovery in the first controlled loop. [I1] | A capped compatibility exercise on this exact toolchain showing missing state operations or unacceptable integration behavior. No such exercise was run. |
| **Pantograph** | Defer until explicit branching/coupled-goal search is needed. Its rationale targets search rather than editor presentation; its protocol exposes goal states and tactics. Internal tactic cancellation is cooperative, so an external process/resource boundary is still needed. [P1, rationale lines 3–15,44–52; protocol §§goal/frontend] | A demonstrated limitation of sequential repair requiring these operations. |
| **LeanDojo** | Do not adopt the original package for new work: its pinned README marks it deprecated and points to LeanDojo-v2. Its tracing/data-extraction scope is unnecessary for the first slice. [D1, README introduction] | An actual requirement for dataset construction or learned retrieval, followed by an independent review of v2. V2 was not inspected here. |
| **Nexus/Aletheia** | Adopt feedback, explicit edit scope and failure-analysis lessons. Do not infer deployable agent availability from a results repository or adopt an LLM verifier as a judge. Nexus’s repository contains successful proof artifacts, not evidence of all attempted outcomes. [N1; N2, README] | A pinned, licensed runnable implementation meeting the local boundaries, plus relevant local evaluation. |

LeanInteract’s source deserves particular caution: `BaseREPLResponse` exposes errors and `sorries`, while its validity-checking code has `allow_sorry=True` by default. “No errors” is not release acceptance. [I2, `interface.py:555–600`]

### License and compatibility caveats

Inspected license declarations were:

- Lean `v4.35.0-rc2`: Apache 2.0. [L3]
- mathlib `c58b47…`: Apache 2.0. [M2]
- leanblueprint `56e066…`: Apache 2.0. [B2]
- LeanInteract `768e18…`: MIT. [I3]
- Pantograph `078969…`: Apache 2.0; its toolchain specifies **4.35.0**, not this project’s **4.35.0-rc2**. [P2]
- Original LeanDojo `7a9f60…`: MIT; inspected toolchain **4.20.0**. [D2]
- Nexus results `064771…`: software Apache 2.0, other materials CC-BY 4.0, with explicit third-party-content caveats. [N2, “License and disclaimer”]

These observations are not a dependency-wide license audit. LeanInteract’s README advertises a compatibility range containing 4.35.0-rc2, but that is upstream documentation, not a local compatibility result. No software was installed. No Aletheia implementation or license was verified. `lean-lsp-mcp` was not inspected; it remains unassessed, not rejected.

## 9. Primary-source register

Six targeted source families were used; snippets were discovery leads only.

**Lean/mathlib**

- **L1:** [Lean 4.35.0-rc2, “Validating a Lean Proof”](https://lean-lang.org/doc/reference/4.35.0-rc2/ValidatingProofs/), sections named above. Version-matched page inspected.
- **L2:** [Lean reference, “Axioms”](https://lean-lang.org/doc/reference/latest/Axioms/), §§8.4–8.5. Rolling page; version-sensitive release recommendations were checked against L1.
- **L3:** [Lean license at v4.35.0-rc2](https://github.com/leanprover/lean4/blob/v4.35.0-rc2/LICENSE).
- **M1:** [mathlib order infrastructure at c58b47adb340faa641e363aef2a460dc534bf172](https://github.com/leanprover-community/mathlib4/blob/c58b47adb340faa641e363aef2a460dc534bf172/Mathlib/Order/CompleteLattice/Basic.lean#L254-L279). Local pinned source inspected.
- **M2:** [mathlib license at the same revision](https://github.com/leanprover-community/mathlib4/blob/c58b47adb340faa641e363aef2a460dc534bf172/LICENSE).

**Blueprint**

- **B1:** [leanblueprint README, revision 56e066d30fb7b608a63f4241fee80982d7eae3ef](https://github.com/PatrickMassot/leanblueprint/blob/56e066d30fb7b608a63f4241fee80982d7eae3ef/README.md).
- **B2:** [License at that revision](https://github.com/PatrickMassot/leanblueprint/blob/56e066d30fb7b608a63f4241fee80982d7eae3ef/LICENSE).

**AlphaProof Nexus**

- **N1:** [Original paper, arXiv:2605.22763v1](https://arxiv.org/pdf/2605.22763v1), PDF p. 2 (§2), p. 6 (failure analysis and semantic test lemmas), p. 10 (§6). Targeted original PDF pages inspected through in-memory text extraction.
- **N2:** [Results README, revision 0647711a71183c1ea492ad60860776617ce1ea88](https://github.com/google-deepmind/alphaproof-nexus-results/blob/0647711a71183c1ea492ad60860776617ce1ea88/README.md).

**Aletheia**

- **A1:** [Original paper, arXiv:2602.10177v1](https://arxiv.org/pdf/2602.10177v1), PDF p. 3 (§2), p. 7 (§3). Targeted original PDF pages inspected through in-memory text extraction.

**LeanDojo/Pantograph**

- **P1:** [Pantograph rationale](https://github.com/leanprover/Pantograph/blob/0789692d65e365c027d171074bf747f1d40328d0/doc/rationale.md) and [REPL protocol](https://github.com/leanprover/Pantograph/blob/0789692d65e365c027d171074bf747f1d40328d0/doc/repl.md), revision `0789692d65e365c027d171074bf747f1d40328d0`.
- **P2:** [Toolchain](https://github.com/leanprover/Pantograph/blob/0789692d65e365c027d171074bf747f1d40328d0/lean-toolchain), [license](https://github.com/leanprover/Pantograph/blob/0789692d65e365c027d171074bf747f1d40328d0/LICENSE).
- **D1:** [LeanDojo README, revision 7a9f600b250a89a62e991c05ffe81ba033018e6e](https://github.com/lean-dojo/LeanDojo/blob/7a9f600b250a89a62e991c05ffe81ba033018e6e/README.md).
- **D2:** [Toolchain](https://github.com/lean-dojo/LeanDojo/blob/7a9f600b250a89a62e991c05ffe81ba033018e6e/lean-toolchain), [license](https://github.com/lean-dojo/LeanDojo/blob/7a9f600b250a89a62e991c05ffe81ba033018e6e/LICENSE).

**LeanInteract**

- **I1:** [README, revision 768e18ebcb5c7ec34d308768a785389eeac37798](https://github.com/augustepoiroux/LeanInteract/blob/768e18ebcb5c7ec34d308768a785389eeac37798/README.md), “Usage,” “Available Queries,” “Advanced options.”
- **I2:** [Response/API source at that revision](https://github.com/augustepoiroux/LeanInteract/blob/768e18ebcb5c7ec34d308768a785389eeac37798/src/lean_interact/interface.py#L555-L600).
- **I3:** [License](https://github.com/augustepoiroux/LeanInteract/blob/768e18ebcb5c7ec34d308768a785389eeac37798/LICENSE).

## 10. Uncertainty, stopping conditions and handoff

**Known:** the current formal definitions omit essential intended policy conditions; the axiom gate is narrower than the recommended policy; version-matched Lean documentation supports separating trusted statements, axiom inspection and stronger proof replay; primary agent papers document relevant repair and misformalization failures.

**Unverified:** correctness of the proposed correspondence theorem, complete feasibility of its Lean implementation, compatibility of candidate adapters/checkers, legacy proof validity under a fresh build, scientific novelty, and any economics or reliability advantage. No benchmark, price or success-rate claim is used to justify adoption.

**What would settle the engineering questions:** after permission to resume implementation, approve the first statement package, complete both witness transformations, demonstrate the negative acceptance fixtures, and replay its release proof with pinned dependencies and the axiom allowlist. Evaluate an adapter only if that workflow exposes a concrete interaction bottleneck. Those are future acceptance activities, not authorization for new runs now.

**Execution limits:** no Lean build, numerical run, new mathematical experiment, journal/config/corpus/tracker change, commit, push, model switch or subagent. Remote PDFs were processed in memory; no corpus downloads or research scratch files were created. The process-capture tool reported cleanup of its owned temporary roots. A guessed blueprint documentation URL and an incorrect Pantograph repository URL returned 404; authoritative repository sources were subsequently located rather than treating those failures as evidence about the projects.

**Call accounting:** 52 tool invocations including this final submission: 16 top-level calls and 36 nested tool calls. Discovery helpers and individual HTTP requests inside a bounded process call are not counted as separate tool invocations. No automatic retry was used.

**Final recommendation:** approve the single-measurement correspondence slice and the sealed-statement/axiom-policy architecture before resuming proof generation. Defer richer proof-search infrastructure until it solves an observed problem in that controlled slice.

---
Coordinator note: the read-only researcher returned this report as its terminal result; the coordinator persisted it and made minor editorial changes after a style-lint pass. No implementation or scientific verdict is implied by persistence.
