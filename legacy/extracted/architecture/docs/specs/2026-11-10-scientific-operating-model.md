# Scientific operating model and architecture

Date: 2026-11-10. Task: `aro-discovery-dub`.
Status: **proposed architecture; no live activation, policy amendment or scientific attestation**.

Companion decision record: [Research capability, usefulness and domain architecture](2026-11-10-research-capability-and-domain.md). It specifies what the whole research system is for, its domain package, competence/usefulness measures, evaluation material and budget-matched comparisons. Its execution sequence refines §10: software acceptance alone is not evidence of research capability, and private evaluation requires a validated evaluator and access boundary.

This document supplements the earlier research-pilot implementation plan. It changes the recommended order of work, not FOUNDATION. It is the decision record for what to build, reuse and defer after M0. Detailed source support is in:

- `../../reports/reading/2026-11-10-research-systems-architecture.md` (S1–S7).
- `../../reports/reading/2026-11-10-formal-evidence-architecture.md` (L1–I3).
- Prior plan worktree: `<workspace>/aro-discovery-restart-plan/docs/specs/2026-11-10-research-pilot-implementation.md` and its packet companion.
- M0 worktree: `<workspace>/aro-discovery-baseline/pilot/README.md` and `reports/2026-11-10-baseline-execution.md`.

The absolute paths above are local handoff locations, not portable dependencies. Before integration, documents and approved code need one reviewed source tree. This research does not authorize committing or copying the other worktrees into the dirty source checkout.

## 1. The decision

**Build a research decision-and-evidence layer around Pi, not a machine that endlessly runs solvers.**

A useful cycle resolves a named uncertainty or explains why it could not. It may end with a counterexample, a narrower claim, a new proof obligation, a literature dependency, a checked algorithmic improvement, or a reason to stop. It need not end with a positive theorem or a better number.

Keep FOUNDATION's five components: memory, search, code judges, writing and evaluator. The decision layer belongs inside the orchestrator/search component. It does not replace evolutionary algorithm search or weaken adversary-first theorem work. It chooses when a particular method is justified and eligible. Defer the expensive population mechanism until a useful, discriminating evaluator exists.

A scientific contribution has several independent requirements:

1. The question matters to the approved research direction.
2. The model and information structure mean what the question says.
3. The mathematical/numerical claim has the right kind of evidence for its scope.
4. Prior work does not already settle the claimed contribution.
5. The result can be reconstructed and reused with its limitations intact.

A kernel check addresses a formal assertion, not all five. A model's preference addresses none as a final verdict. Agent execution success is a separate operational fact.

## 2. Authority and operating rhythm

### Campaign, shift, operation

- **Campaign:** a human-approved research question, context, exclusions, budget envelope and review point. Its scientific direction is not inferred from whichever program is easy to optimize.
- **Shift:** one bounded investigation authorized within that campaign; initially started by the human. It has a question/scope version, allowed actions, resources, evidence requirements and terminal conditions.
- **Operation:** read a source, propose a claim, search for a counterexample, derive a lemma, attempt a proof, run an approved benchmark, or assemble an evidence-bound explanation.

These are organizational records, not new scientific statuses. Default remains FOUNDATION Level 3. The owner can delegate local organization without delegating scientific attestation, threshold changes, corpus admission or future autonomous campaigns. Research records may contain proposed next work; a runtime does not create Beads tasks. Human-authorized implementation coordination may use Beads, as in the present task.

Use **one active Pi worker**, with sequential role changes. Roles constrain purpose, tools and output; they do not need simultaneous agents. Keep independent code checks even when the same model is used for proposal and critique. The evaluator observes; it does not decide research direction or turn components off except at hard resource limits.

### Role boundaries

| Principal | May do | May not do |
|---|---|---|
| Human | Choose direction, attest, authorize autonomy/budget/source admission and threshold changes | Be impersonated by a worker |
| Orchestrator | Select an eligible next operation within the approved shift; record reasoning; stop and escalate | Declare a theorem true, alter frozen acceptance, turn a timeout into refutation |
| Archivist | Extract anchored source statements and comparison tables | Treat a search snippet or converted formula as source authority |
| Explorer | Propose claims, constructions and lineage-preserving revisions | Raise scientific status based on persuasive text |
| Adversary | Produce attacks, exact counterexample candidates, missing-assumption reports | Treat failed search as proof |
| Deriver | Derive, construct certificates, attempt sealed Lean statements | Approve its own proof or silently modify the target |
| Code judge | Check a specific artifact/claim scope under a frozen procedure | Infer generality, novelty or importance from an instance test |
| Publisher | Mechanically apply an authorized, scope-bound evidence event | Accept a worker-supplied PASS or bypass human attestation |
| Scribe | Assemble explanations and draft text from eligible nodes | Smuggle an unsupported proposition into narrative |

The publisher is a deterministic authority boundary, not another LLM. An actor string or an unforgeable-looking ID in a JSON file does not establish authority.

## 3. Hypotheses: representation, generation and selection

### A claim is more than a sentence

Each proposed claim needs an immutable claim version linked to:

- its research question and intended contribution;
- model version: dynamics, dimensions, data interpretation and domains;
- observations: exact/noisy state/output, timing, number of closings and causality;
- policy class: what is chosen once, what can depend on which observation;
- quantifier order, assumptions, conclusion, objective polarity and feasibility;
- closest checked source statements, with explicit scope differences;
- proposed falsifier and relevant boundary/degenerate cases;
- planned evidence route and its limits;
- parents, including prior refutations, restrictions or generalizations;
- a reason the next operation could change a research decision.

A finite example, a general theorem, an algorithm and a source comparison have different schemas. Do not force all of them into a numerical score card. A claim without a meaningful falsifier may still be a definition or a question; it must not be presented as a testable conjecture.

For A4, printed coefficients and reconstructed decimal coefficients are different model versions. Neither is silently promoted to exact trigonometric data. A prefix-indexed assignment is not automatically an implementable measured-state policy.

### Bounded generation

Generate candidates through explicit operators rather than asking for a large list of interesting ideas:

1. **Assumption boundary:** remove or strengthen one declared premise of a known scoped result; say what would break or become possible.
2. **Counterexample repair:** derive a new, narrower child claim from a checked failure; keep the original refuted claim.
3. **Representation bridge:** ask when two policy/problem formulations describe the same feasible objects and objective values.
4. **Mechanism from instances:** propose a structural explanation of a numerical pattern, with a route to a general result; label the pattern as finite evidence.
5. **Algorithmic obstruction:** identify a concrete cost/exactness bottleneck and propose a method with an external acceptance measure.

For the first campaign, propose at most three alternatives per selection point; this is a proposed workload bound, not a hidden scientific alert threshold. Use the owner's approved budget to choose one. Diversity means different mathematical mechanisms, not different wording of the same guess.

### Selection is reasoned, not pseudo-quantitative

First apply mechanical eligibility: source/model identifiers exist, prerequisites are available, evidence procedure is in scope, no active unaddressed contradiction, budget and permissions fit.

Then the lead recommends an action using a short comparison:

- What uncertainty does it address?
- What different decisions follow from positive, negative and inconclusive outcomes?
- Is a cheaper source read, exact small case or logical argument sufficient?
- Is the likely result a reusable lemma/counterexample or just another isolated number?
- Which assumption or novelty gap prevents a stronger interpretation?

LLM rankings and estimated success probabilities are advisory prose, not numerical scientific evidence. Priority follows owner goals and explicit dependencies. If neither outcome changes anything, do not run the experiment merely to fill the cycle.

## 4. The detailed research cycle

| Stage | Required input | Output | Stop/redirect condition |
|---|---|---|---|
| **Orient** | Approved campaign and versioned working set | One unresolved question and eligible action options | Missing scope or conflicting authority: ask the human, do not guess |
| **Read/compare** | Specific claim or uncertainty | Anchored statement and assumption-by-assumption comparison | Missing original source, unverified formula or unresolved successor paper: block the affected claim |
| **Specify** | Model, policy and question | Immutable claim/model package and evidence plan | Ambiguous quantifiers, dynamics or observations: return to specification |
| **Attack** | Scoped claim and frozen attack contract | Checked counterexample, finite survival record, or inconclusive attempt | A valid counterexample refutes only its matched claim; infrastructure failure proves nothing |
| **Explain/revise** | Evidence and failure analysis | Derived obstruction, revised child claim or proof obligations | No justified change since last attempt: park rather than repeat |
| **Derive** | Surviving claim plus explicit assumptions | Derivation and independent computational/symbolic route where applicable | Disagreement becomes a discrepancy dossier; at most the charter's two authorized explanation attempts |
| **Formalize** | Approved statement package for a suitable lemma | Proof candidate and complete dependency/axiom record | Statement changes, hidden assumptions or exhausted budget: stop this attempt |
| **Judge/reproduce** | Frozen submitted artifacts and trusted checkers | Scoped reproducible verdict; complete coverage inventory | Missing result, checker drift, nondeterminism or mismatch: no publication |
| **Record** | Authorized verdict and checked artifact identities | Event and updated derived scientific view | Stale authorization or incomplete artifact storage: reject |
| **Interpret/communicate** | Eligible scientific nodes | Short result, limitations, relevance and next decision | Unsupported statement: return it to the relevant claim, not the published narrative |
| **Review** | Campaign delta, costs, blocked questions | Human direction/attestation decisions | Budget review or scientific decision required: stop |

The table is not a mandatory straight line. A source theorem can close a question without experiments. A counterexample may lead directly to a narrower formulation. A proof obstruction may require a new lemma. A stopped infrastructure attempt resumes only through an explicit recovery decision. Falsification precedes proof attempts for theorem work as required by FOUNDATION; finite survival does not compel formalization.

`logika` applies to statement/argument review; `technical-style-editor` applies to the dossier and report. Their critique is useful input, never a code-judge verdict.

### Evidence outcomes must remain separate

Retain FOUNDATION's statuses and terminal nodes. Do not add a generic `verified=true` or automatically force every theorem through meaningless numerical stages. The following are descriptive dimensions, not replacement statuses:

- **Correctness evidence:** exact certificate, finite checks, symbolic derivation, formal proof, or none.
- **Scope:** the actual model, parameter range and information structure checked.
- **Source provenance:** anchor inspected or still required; printed versus inferred data.
- **Novelty assessment:** unassessed, known overlap, unresolved comparison, or human-reviewed difference.
- **Usefulness:** relation to a campaign objective, with an explanation, not an LLM-issued verdict.
- **Operation:** completed, failed, cancelled, budget exhausted or evidence incomplete.
- **Attestation:** human decision only.

A formalized supporting lemma need not be novel. A new algorithm may have exact instance certificates without a general optimality theorem. A refuted conjecture may yield a valuable obstruction. A timeout is none of these scientific outcomes. FOUNDATION's eventual theorem timebox/descoping policy still applies to campaign decisions; an individual worker timeout must not mechanically overwrite a claim with a scientific conclusion.

## 5. Formal proofs: validity and meaning

The formal-evidence companion establishes why the current proof labels cannot be reused as intended scientific results. An order lemma is not a theorem about the intended policy class; an unconstrained path-dependent `Strategy` does not enforce control bounds or causality. The current axiom script rejects `sorryAx`, but is not a complete axiom allowlist and succeeds on an empty theorem inventory.

Use three separate obligations:

1. **Meaning:** an approved mapping between informal model and formal definitions, including timing, constraints and quantifier order.
2. **Validity:** the submitted proof establishes the exact sealed statement under the permitted foundations.
3. **Interpretation:** applicability, attribution and novelty are reviewed separately.

### The first mathematical slice

Recommend an infrastructure lemma, not a preordained dissertation theorem:

> For a finite, nonempty disturbance-path set in a finite-horizon rational linear system with one exact measurement at a fixed closing time, an implementable state-measurement policy meets a given robust feasibility/objective bound if and only if a scenario assignment meets the same bound and assigns identical second-block programs to indistinguishable measured states.

This is a **proposed target**, not proved here. Seal the timing convention, signed objective, control/terminal constraints and reachable observation domain. Prove both witness transformations and preservation of trajectories/constraints. Use bound feasibility first rather than silently assuming existence of an optimum. The scenario equivalence classes depend on the first-block decision and actual dynamics.

This slice targets the project's observed information-structure failure. It does not prove continuous-uncertainty vertex reduction, continuous-time results, noisy observations, multiple closings, affine-rule exactness or an r=80 improvement. It is useful even if known, because it binds future numerical claims to implementable policies.

### Release contract

Freeze the declaration, model definitions, imports, Lean toolchain and full dependency manifest. Proof search may edit only allowed proof material. A changed assumption produces a new target, not a repaired proof of the old one. Keep scratch `sorry` material out of the release import closure.

Require a nonempty expected theorem inventory, successful checking of every release module, one parsed transitive axiom result per declaration, and a positive allowlist (`propext`, `Classical.choice`, `Quot.sound`). Reject unknown/custom/native-evaluation axioms and `sorryAx`. A dependency having the same declaration name is not enough: match against trusted statements and model definitions.

Pin the current Lean **4.35.0-rc2** and resolved mathlib revision for the first compatibility assessment. Do not upgrade to repair a proof silently. Evaluate version-compatible independent replay/comparison facilities before accepting unreviewed generated proofs. Compiler success and `#print axioms` alone do not supply a sandbox or establish semantic fidelity. Agent-authored tactics/meta-code are executable untrusted code.

Prefer direct Lean feedback initially. LeanInteract is a candidate only after a measured interface need; its error-free response is not a no-`sorry` guarantee by default. Pantograph is deferred for explicit branching search; the inspected release targets a different toolchain. Do not adopt deprecated original LeanDojo for the first slice. Blueprint is a generated view, not an independent status store.

## 6. Memory: what persists and what the next worker receives

Keep the charter's one scientific state, not a collection of competing databases:

- **Events:** authoritative history of admitted claims, scoped evidence and human decisions, through `aro.journal`/`ro` only.
- **Blueprint and artifacts:** the scientific objects, dependency graph and immutable evidence addressed by those events.
- **SQLite/search/rendered markdown:** replaceable projections or caches, never additional authority.
- **Pi sessions:** operational history and recoverable working context, not scientific truth.
- **Beads:** human-directed implementation tasks, not proof or numerical evidence.

Separate records for question, definition/model, claim version, source anchor, construction/policy, evidence, counterexample and attempt. Relations distinguish `depends_on`, `supports_within_scope`, `refutes`, `restricts`, `generalizes`, `instantiates`, `compares_with` and `supersedes`. Proof dependencies must be acyclic; a source/research navigation graph may contain non-proof cycles. These relation names are a proposed typed domain vocabulary, not new live events.

### A working-set packet is a scientific handoff

A new worker receives the question and scope, applicable definitions, relevant source anchors, checked evidence, nearest counterexamples, open proof obligations, explicit exclusions, current operation contract, budget and write boundary. Include rejected approaches and the exact reason they do not apply. Resolve relevant dependency closure before truncating narrative; if the closure cannot fit, split the task rather than omit a necessary premise.

Retrieve by exact model/claim dependencies and scope compatibility before semantic similarity. A proof for a different observation map must not be retrieved as authority merely because the prose resembles the current claim. A changed definition marks dependent evidence stale for the new version; historical evidence remains intact. Equivalence of two claim formulations is a claim to justify, not embedding deduplication.

Research interpretations and methodological lessons are allowed as prose explicitly labeled as interpretation and linked to evidence. A generated playbook change is a proposal requiring the appropriate review; it cannot silently become a system instruction. Start with deterministic queries and explicit relationships. Add vector search only after measuring concrete retrieval failures, and never use similarity as a validity test.

## 7. Technical architecture and recovery

### Component layout

```text
Human campaign / scope / budget decisions
                  |
        Scientific controller
   eligibility + proposed next action
                  |
        bounded Pi worker session
  sources / scratch / diagnostics / proposals
                  |
       immutable submission snapshot
                  |
     trusted checker in isolated executor
     finite / symbolic / certificate / Lean
                  |
      deterministic authorized publisher
                  |
        aro.journal + artifact store
                  |
    blueprint / working set / owner briefing
```

Use existing Python project conventions for scientific types/checkers/views. Keep Pi's TypeScript integration thin. JSON artifact contracts are the boundary; no second model router, conversation store or home-grown agent loop.

### Pi integration decision

Native Pi **1.5.1** supplies sessions, tools, cancellation and lifecycle hooks. The installed workflow extension is **6.3.0**. A project extension can inspect/block `tool_call`; nested calls carry parent IDs and pass through the same hooks. This is a documented integration surface, **not yet a tested deployment**.

The first integration spike must show that the chosen subagent path loads the required gate, binds the exact worktree cwd, records complete counters and preserves output before cleanup. Prefer the current native subagent path if it passes. If it cannot satisfy these boundaries, use an explicit isolated worker host through the same Pi SDK and existing authentication, not a replacement agent framework. This conditional is a declared integration decision gate, not an automatic runtime fallback.

Budgets must cover elapsed time, compute resources, admitted tool calls and model usage separately. Keep the owner's current worker limits: 90 minutes and 60 tool invocations; no autonomous extension after exhaustion. Define the counting rule before execution. Proposed rule: every admitted Pi tool invocation counts once, including wrapper and nested calls; rejected/invalid calls are additionally audited but never authorize side effects. Reserve capacity durably before dispatch; deduplicate by run plus call ID. A tool invocation is not the number of shell subprocesses or HTTP requests, so OS compute/process limits remain necessary.

Record requested, admitted, started and finalized calls separately. A progress snapshot is not a cumulative log. A concurrent batch cannot spend the same remaining budget twice. `terminate` behavior alone is not a wall-clock kill or proof that sibling calls have stopped.

Disable or explicitly authorize retry behavior at each layer: orchestrator/subagent, Pi agent, provider, tool and proof adapter. Pi documents agent-level retries enabled by default, independently from subagent `retries: 0`. Freeze effective nonsecret settings and report observed retry events. Do not infer historical absence of internal retries from the number of submitted runs. No model fallback is permitted by the current owner decision.

### Isolation is not a prompt

A feature worktree separates files but does not restrict filesystem access. A terminal instruction not to touch `events.jsonl` is not a security boundary. Before live activation, worker execution must lack access to publisher credentials, writable live science state, checker sources and evaluator-private cases. Generated code runs in a process/container boundary with explicit read-only inputs, writable scratch, resource caps and an approved network policy. Do not modify the owner's proxy environment to achieve this.

The Pi host may hold the existing model credential; code execution must not inherit that secret. Treat documents, downloaded repositories and tool output as data, not policy instructions. Tool permission hooks are defense in depth, not a substitute for OS boundaries around arbitrary shell or Lean meta-code. Demonstrate these restrictions with negative tests; until then describe isolation as unverified.

### Persistence and publication

Preserve the prior plan's leases/fencing, idempotent publication, cancellation and staged artifact invariants. There is one writer for scientific admission. Candidate snapshots are stored before a judge starts; checkers cannot read a mutable candidate tree. The result binds the claim/model version, input snapshot, checker version and complete case inventory. Missing mandatory data fails closed.

Source inspection confirms `aro.journal.append_event` currently uses a module-global target and lacks an explicit target/lock/fsync transaction API. Therefore an isolated-root pilot cannot merely call the old append function and assume isolation. Introduce a narrowly reviewed API within `aro.journal`/`ro`, preserving existing consumers; do not build an ad hoc competing journal writer or monkeypatch globals. This implementation is deferred and the live journal remains untouched.

Recovery must distinguish:

- worker died before submission: preserve scratch/trace and propose an explicit new attempt;
- snapshot stored but no verdict: rerun only the pinned deterministic checker when authorized;
- verdict stored but event absent: publish that same evidence once with a valid fence;
- event durable but view missing: rebuild the projection, do not rerun the research;
- cancelled/stale attempt reports late: retain diagnostic output but reject publication;
- accepted source/definition later invalidated: append a corrective event and invalidate dependent current views; never erase historical evidence.

TLA+ remains appropriate for publication/fencing/recovery interleavings. Its prior 94-state pilot check is evidence about that model, not a proof that a future implementation or the scientific claim is correct. Add refinement correspondence and crash-injection tests before claiming implementation coverage.

## 8. Acceptance scenarios

These are specifications for later implementation. None was executed as a new experiment during this architecture task.

| ID | Scenario | Required result |
|---|---|---|
| H1 | Two disturbance histories produce the same measured state but a candidate assigns different continuations | Reject measured-state realizability; do not relabel as state feedback |
| H2 | A counterexample satisfies the exact premises and violates the claim | Judge admits refutation of that claim version; a repaired child remains distinct |
| H3 | Counterexample violates a premise, or a checker finds none on a finite grid | No general refutation/proof respectively; scope retained |
| H4 | The closest source already covers the claimed contribution | Preserve reproduction/supporting value; no novelty claim |
| H5 | Literal printed data is replaced with inferred decimals | New model version; old evidence cannot be relabeled |
| F1 | A proof omits dynamics/control bounds, assumes its conclusion or swaps quantifiers | Trusted statement/model mismatch or correspondence rejection; no formalized claim |
| F2 | Empty theorem inventory, missing result, imported `sorry`, custom or native-evaluation axiom | Formal release fails closed |
| F3 | Both sides of an equivalence are accidentally impossible | Mapping review/fixtures expose vacuity; retain explicit nonempty domains and positive/negative cases |
| M1 | Retrieve a lemma for a different information structure | It may be a lead, but cannot satisfy an evidence dependency |
| M2 | Restart the next worker without previous conversation | It reconstructs the same next-action context from artifacts; no lost contradiction |
| R1 | Crash at each snapshot/verdict/event/view boundary | No fabricated acceptance, no lost admitted event, no duplicate publication |
| R2 | 60 admitted tool calls, then direct/nested/concurrent call attempts | No 61st admitted call; counters and denied attempts auditable |
| R3 | Timeout/cancel while a process is active, followed by a late callback | Owned process group stops; artifacts retained; stale publication rejected |
| R4 | Worker attempts to read private tests/secrets or write live state/checker code | OS/tool boundary denies access; a prompt refusal alone does not pass |
| R5 | Transient provider error with retries disabled | Terminal operational error, no hidden attempt or model fallback |
| E1 | Evaluator sees only easy/duplicate cases, empty result set or missing case | Complete-inventory gate rejects; public and private acceptance remain separate |
| E2 | All candidate programs pass or fail | Monitor flags a possible nondiscriminating gate; never silently adjusts thresholds |
| W1 | A draft claims a general theorem from finite survival | Anchor/scope gate rejects the sentence |

Include positive controls as well as these negative controls. Known-bad mutations are evaluator fixtures, not worker-visible training material. Hashes cannot hide private tests from a worker that can read their files. Holdout separation must be implemented and measured, not asserted.

## 9. What changes in the previous plan

| Previous emphasis | Keep | Change |
|---|---|---|
| M0 finite and A4 baselines | Exact certificates, independent checking, explicit information structures | Treat as regression/comparator infrastructure, not a research agenda |
| Next bounded r=80 attempt | A possible example/application | No longer the recommended immediate next step; first bind claims to policy semantics and review the contribution question |
| Runtime packet series | Fencing, durability, replay and protected publication | Move behind an offline scientific decision/dossier microcycle and a Pi boundary spike |
| Formalization as a later proof phase | Select central theorems from surviving research | Add early model-correspondence infrastructure; do not preselect dissertation theorems |
| P9 offline demonstration | Its corrected independence from full runtime | Extend it to exercise selection, refutation, scoped evidence and handoff |
| Existing Pi tool budget | 90 minutes / 60 calls as owner limits | Implement native-hook accounting, distinguish nesting and retries; previous instruction-only ceiling was not enforced |
| Journal adapter uncertainty | Authorized `aro.journal` write boundary | Explicit root/durability API is now known required work, not assumed available |
| Single provenance manifest | Automated identities and reproducibility | Add semantic model/claim binding; matching hashes cannot prove the right model was used |
| Memory summaries | Source anchors, retained failures | Require typed scope-aware retrieval and proof-obligation closure |

No earlier work is deleted or retroactively upgraded. This document supersedes only the recommended continuation order. The original plan files are not edited in this task.

## 10. Recommended implementation sequence

### Next bounded slice: an offline scientific dossier and decision gate

Implement **one claim version → one eligible action → one scoped evidence outcome → one reconstructible handoff**, without a persistent daemon, new model API or live scientific journal writes.

Suggested implementation boundaries, subject to final repository placement:

- `pilot/science/`: typed immutable model/claim/action/evidence contracts, structural eligibility validation and deterministic dossier/working-set export.
- `pilot/science/tests/`: finite checked fixtures and negative mutations for scope, lineage, missing evidence and wrong observation semantics.
- `pilot/examples/`: one explicitly illustrative claim lifecycle bound to existing M0 evidence; no invented scientific verdict and no unexplained auto-promotion.
- A sealed statement package for the proposed single-measurement correspondence theorem; prose/definitions and proof obligations first, not an unreviewed proof search.

Reuse the existing M0 checkers by exact approved snapshot rather than rewriting their arithmetic. Read-only import of old evidence does not confer authority to migrate legacy scientific status. Source/model correspondence requires the explicit human semantic review described above.

**Acceptance:** a valid finite claim can cite only matching evidence; wrong-scope evidence and incomplete outcomes fail; a checked counterexample retains the parent and restricted child; an inconclusive run has no scientific promotion; regeneration is byte-identical; a fresh session obtains the same scoped packet; the next-action record explains the decisions each possible outcome would change. These checks establish engineering behavior, not the novelty or general correctness of a hypothesis.

**Stop after the slice** if the dossier cannot express a real next scientific decision without fabricating a score, source fact or verdict. Do not solve that problem by launching more workers.

### Subsequent slices, not authorized execution by this document

1. **Formal contract and proof gate:** nonempty target inventory, axiom allowlist, pinned environment, trusted statement matching, negative fixtures, then the approved correspondence proof. Separate proof development from release-checker development and review.
2. **Pi boundary spike:** demonstrate exact cwd, hook inheritance, budget reservation, complete audit, effective retries, cancellation and filesystem isolation. Use a trivial engineering fixture, not a scientific campaign. Choose the thin adapter route from this evidence.
3. **Durable single-worker microcycle:** explicit isolated `aro.journal` root, snapshot/check/publish/replay, crash tests and implementation-to-TLA correspondence. No live-state activation until acceptance.
4. **Scientific campaign:** compare the closest literature including unresolved successors, choose an actual theorem/algorithm question, and authorize bounded experiments/proofs. r=80 remains an optional application, not the default center of the system.
5. **Scale only after evidence:** private holdouts, benchmark diversity, evolutionary niches and stronger search tooling when the small cycle exposes a bottleneck. No autonomy promotion merely because ten processes finished.

## 11. Evaluation, limitations and owner review

Measure decision-relevant scientific outcomes, repeatability, evidence-scope errors, recovered failures, handoff completeness, admitted tool usage and time. Preserve FOUNDATION's code-derived metrics and human-controlled thresholds. No new numeric alarm threshold is activated by this document. Refutations have no quota. Report token usage and cost separately; actual provider billing may be unknown and must not be labeled zero.

Immediate uncertainty: adapter/sandbox compatibility, durability implementation, first theorem proof, and complete literature novelty comparison. None is settled by these design documents. The public papers motivate mechanisms; their success rates and large-scale demonstrations are not guarantees for this project.

The recommendation to the owner is to accept the **offline dossier + sealed-statement slice** before either more A4 numerical runs or a permanent runtime. It directly tests whether the system can keep the intended mathematical question intact across generation, criticism, evidence and a fresh worker, while making the next research decision explicit. Broader automation should follow that result, not substitute for it.
