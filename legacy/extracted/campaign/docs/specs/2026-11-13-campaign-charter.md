# Evidence-grounded scientific pilot: execution charter

Task: `aro-discovery-k4t`. Owner explicitly requested a detailed plan AND execution, durable tracking, consideration and testing of the useful mechanisms discussed, and confirmation of results. The purpose is to investigate whether this system can do substantive theoretical work in the approved OGU/ARO direction without merely generating activity. No scientific breakthrough is promised.

## Authority and non-negotiable boundaries

FOUNDATION.md and AGENTS.md govern. Internal artifacts are English; owner-facing briefings are Russian. All new work stays in `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`, created from `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`. Verify root/branch before edits. Main and all other worktrees are read-only inputs; main is dirty. Worktree separation is NOT a filesystem sandbox.

The owner authorizes planning, bounded local implementation, public development probes, literature research, and bounded mathematical investigation. This does NOT authorize human attestation, scientific status promotion, changing FOUNDATION or thresholds, live runtime/journal/state/corpus/glossary writes, private-panel execution, deployments, commits, pushes, PRs, purchases, new providers, global installations or contacting authors. New literature can be inspected in campaign-local research artifacts, but not admitted to the live corpus. Never manufacture an actor-human journal event. The coordinator alone owns Beads tracking. No nested agents or workflows inside workers.

A fixed Lean statement can be investigated and compiled as an experimental artifact without claiming human-approved semantic correspondence or project formalized status. Distinguish proof of the actual statement, correspondence to the intended problem, and scientific novelty/usefulness. Only code judges/Lean issue mathematical machine verdicts; an LLM reviewer supplies criticism, not scientific acceptance.

## Execution platform and resource policy

Use current Pi connection and `openai/gpt-6.1-sol`, medium reasoning for implementation/repair/synthesis and high for research/independent review. One active worker at a time. Each worker has a 90-minute timeout and an INSTRUCTIONAL ceiling of 60 tool invocations INCLUDING nested calls. Reserve calls for verification and writing the handoff. There are no orchestrator retries or model/provider fallbacks. A provider failure terminates the workflow; inspect persisted state before any explicit recovery. Native agent/provider internal retry settings are not yet audited and must not be described as disabled merely because `retries: 0` was passed.

The workflow is a finite first campaign, not an indefinite goal loop: at most 14 agent calls including one plan repair/re-review, one final repair/re-review, and synthesis. No automatically expanding population. Budget ceilings are bounds, not targets. Record observed runtime/usage and preparation/helper costs where accessible; unknown provider billing is unknown, not zero. Do not read or print secrets to obtain accounting or settings.

Owner suggested `omp` as an optional execution platform and explicitly allowed staying here. Decision: use existing Pi for this campaign to avoid confounding scientific work with a runtime migration. Record this in the mechanism matrix. Investigate omp only if a concrete observed Pi limitation blocks a required operation; no installation/migration by default. Do not infer omp's capabilities from its name.

## Prior deliverables (read-only; untracked files exist)

- Architecture worktree `<workspace>/aro-discovery-architecture`: `docs/specs/2026-11-10-scientific-operating-model.md`, `docs/specs/2026-11-10-research-capability-and-domain.md`, `reports/reading/2026-11-10-research-systems-architecture.md`, companion formal-evidence review and Russian briefings. Review examined mechanisms, NOT reproduced external discoveries or comparative research productivity.
- Baseline worktree `<workspace>/aro-discovery-baseline`: exact finite policy enumerator/Bellman checker; A4 rational primal-dual certificates. See `pilot/README.md`, report and `artifacts/research-pilot-m0/manifest.json`.
- Dossier worktree `<workspace>/aro-discovery-dossier`: `pilot/science`, finite snapshot and `docs/specs/2026-11-10-single-measurement-statement.md`. The full correspondence statement remains proposed, not human approved or proved.
- Episodes worktree `<workspace>/aro-discovery-episodes`: four PUBLIC M/F/P/R fixtures; `reports/2026-11-13-public-episodes-acceptance.md`. Repaired inventory, 22 tests normal/-O, Ruff/format, eight references/five negatives. R is only static packet validation: stage 1 already includes child evidence, fresh checker is not successor-worker continuation. P is elementary observation factorization, not the full dynamics correspondence theorem.
- Restart-plan worktree `<workspace>/aro-discovery-restart-plan`; main has public TLA model/checks under `specs/research-pilot` and pilot reports. Prior TLC result concerns the bounded model only.

If importing existing code or evidence, copy only the required files, verify source identities and keep a provenance manifest. Do not silently import executable modules from absolute sibling paths. Preserve imported bytes. Add regression coverage for any adapted local interface.

## Mechanisms to examine explicitly

Produce a matrix with source anchor, intended scientific benefit, smallest test, observed result, adoption decision and limitations for every item. Allowed dispositions are tested/adapted, failed, blocked, or deferred-with-a-concrete-reason; a document alone is not a successful test. Do not implement everything just to fill the matrix.

1. ZIB-style question/assumption/method/result dossiers and stop conditions.
2. Co-scientist hypothesis operators: weaken a premise, strengthen a conclusion, change representation, construct a separating example, split a failed conjecture into distinct children. LLM rankings are proposals, never truth or novelty scores.
3. AlphaEvolve/FunSearch candidate/evaluator separation and preservation of failed constructions; try only a small search where a valid independent objective exists. No arbitrary evolutionary engine if this question has no suitable objective.
4. Station-style durable mathematical explanations and a REAL fresh-worker continuation using a bounded packet, not replay of the same checker.
5. Scope-aware domain memory: exact definitions, source-premise maps, dependency closure, counterexamples and negative knowledge. Retrieval relevance is not theorem applicability.
6. Double-route exact checks and adversarial certificates; positive controls as well as rejection tests; fail-closed complete inventories.
7. Lean statement fidelity, dependency/axiom checks and AlphaProof Code's specification-strength testing, vacuity tests, semantic mutation controls and separately reviewed amendments.
8. TLA+/TLC for protocol invariants; clearly distinguish model evidence from implementation correctness and mathematical proof.
9. Pi execution boundaries: current cwd, tool exposure, budgets/retries/cancellation, accounting and context continuity; observe what is feasible without changing global harness configuration or live project state. Do not fabricate isolation or hard call-count enforcement.
10. A simple strong session versus structured domain-assisted work on the same source-grounded question. This is at most two PUBLIC exploratory attempts, not the private 48-trial panel, not a statistically valid efficacy claim, and not blind if file access is not isolated.
11. Independent source/novelty comparison and an honest contribution dossier. Source silence is not novelty. Identify known lemma/reconstruction, project-new example, unresolved claim and plausible literature delta separately.
12. Runtime choice including omp: use existing execution unless a demonstrated limitation warrants another route; do not confuse platform richness with scientific power.

## AlphaProof Code primary sources and verified local observation

Blog: https://deepmind.google/blog/introducing-alphaproof-code/
Paper: https://deepmind.google/documents/36/Formal_Verification_of_Signal_4.pdf
Artifacts: https://github.com/google-deepmind/code-verification/tree/808b4b7ffef198e6a91f71ed776d641a1c236882
Comparator upstream: https://github.com/leanprover/comparator

Coordinator read paper sections 2.1–2.4 (PDF pp.3–6), target boundaries, sections 5.3 and 6 (p.24 onward), artifact README and comparator README. Mechanisms: human-reviewed trusted specifications/dependency closure; prover cannot mutate the specification; skeptical reviews, satisfiable-premise witnesses and mutation disproofs; independent amendment critic; kernel/comparator checks. Signal result is scoped to a particular AArch64 CLI binary with hooked contracts and assumptions, not all Signal apps or all vulnerabilities. The artifacts pin Lean 4.34.0; do not import that toolchain into this project.

Locally `lean --version` showed 4.35.0-rc2. `lake --help` and `lake comparator --help` expose comparator/check, explicit permitted_axioms and bubblewrap isolation. Actual comparator execution has NOT yet been tested. The local comparator differs from the old standalone landrun path; inspect installed help/docs. Never disable sandbox to manufacture a passing validation. If required system support is absent, record the exact blocker and continue independent scientific work using only previously established evidence labels. No global installs or toolchain changes.

## Finite execution phases and required outputs

### A. Detailed plan and independent feasibility review

Create `docs/specs/2026-11-13-scientific-campaign-plan.md` and `reports/briefings/2026-11-13-campaign-plan.md`. Include exact stage inputs/outputs/files, risks, decisions, acceptance commands, evidence inventory schema, dependencies, scientific versus engineering gates, resource estimates, recovery and terminal dispositions. This is a detailed execution specification, not a second task tracker. A reviewer checks scope and feasibility read-only; one bounded plan repair/re-review is permitted. Unresolved unsafe execution blocks dependent stages but not independent source reading.

### B. Minimum verification/tool spike

Implement only campaign-local tools required for the approved plan. Exercise installed comparator with a valid proof and wrong-target/dependent-definition/axiom/inventory controls if feasible; verify nonvacuity explicitly. Reproduce relevant existing TLA checks using existing tools if available, without changing the model to force success. Check resource availability and execution limits honestly. Build a small machine-readable `artifacts/campaign/tool-readiness.json`, evidence outputs and `reports/2026-11-13-tool-spike.md`. Unsupported tools remain blocked, not silently emulated. Do not let this turn into a general runtime project.

### C. Domain immersion and question selection

Read original sources and local exact evidence. Produce `research/domain-packet.md`, `research/question.md`, `research/resource-manifest.json`, and a closest-result comparison. Choose one nontrivial but bounded theoretical question in the approved OGU/ARO information/policy bridge. Do NOT assume the obvious scalar injectivity example or finite factorization lemma is a new open problem. Establish known results/premises and the actual unresolved gap before expensive search. If the candidate is already solved, document the closure and choose at most one alternative. If no defensible open question is found, explicitly investigate a source-grounded boundary/reconstruction without pretending novelty. Persist original-source anchors and local copies/hashes outside the live corpus.

The question packet must be usable by another worker: exact models, timing, quantifiers, domains, objective polarity, constraints, observed examples, forbidden conflations, nearest results and a finite acceptance boundary. Distinguish printed versus reconstructed A4 data; do not start r=80 grinding. Missing decisive source => mark unresolved and stop that inference.

### D. Two bounded public research approaches

One simple strong Pi research session and one structured domain-assisted session receive the SAME question/source pool and per-worker envelope. Run sequentially. Each records a genuine mathematical derivation, explicit conjecture alternatives, at least one serious falsification attempt and checkable results or precise proof gaps. Structured approach uses premise/representation operators and persistent negative knowledge. It must not read the other attempt's answer directory; this is an instructional separation, NOT demonstrated privacy. Do not call it a controlled benchmark or attribute all differences to architecture.

Write `research/baseline/` and `research/structured/`, each with derivation, executable checks where applicable, results and a standalone `handoff.md`. No raw hidden chain-of-thought is requested: retain mathematical arguments, observable actions, evidence and decisions. Limit speculative branches to three, abandon branches on decisive counterevidence, and report exhaustion as exhaustion. A human-readable unproved proof sketch remains a proposal.

### E. Actual successor continuation

A fresh worker receives the question/resource manifest and the structured handoff, not the predecessor conversation. It reconstructs the exact outstanding obligation and performs one NEW check/derivation/source comparison that changes or sharpens the research state. Write `research/continuation/`. Record which required information was missing and whether the next step actually succeeded. Do not confuse a fresh validator with researcher continuation. All context-access limitations remain declared.

### F. Independent review, bounded repair and final acceptance

Reviewer is read-only. Inspect scientific arguments for scope errors and compare sources; run independent exact/formal checks where possible; review code/tests and evidence completeness. This review does not itself confer mathematical correctness or novelty. One repair pass may fix concrete findings and must add regression evidence; no endless new research branch. One final independent verification checks repaired findings, then a synthesis agent writes the English contribution dossier and Russian owner report.

Final paths: `reports/2026-11-13-campaign-acceptance.md`, `reports/briefings/2026-11-13-campaign-outcome.md`, `research/contribution-dossier.md`, `artifacts/campaign/mechanism-results.json`, `artifacts/campaign/evidence-index.json`. Final index must bind observed outputs, source provenance, scope and actual commands; completeness needs a frozen expected inventory, not a vacuous glob. Scientific and engineering results stay separate.

## Success, failure and stopping

Success of the campaign means every planned operation has an honest observed disposition and the scientific attempt was actually made where inputs permitted it. It does not mean a breakthrough occurred. Report the strongest CHECKED statement, all unresolved obligations, closest-source delta, useful negative results, actual continuation outcome and observed effort. Green tests alone do not establish research competence.

Stop a branch when a source already resolves it, a counterexample invalidates it, a required premise/source is unavailable, budget is exhausted, or another attempt would repeat the same question without new evidence. Preserve artifacts on failure. The workflow stops on provider/tool execution failures; no automatic retries. Recovery must inspect workflow_status and source files and use explicit workflow_retry/resume with expectedState. Completed phases are replayed rather than silently rerun. No claim of an always-on watchdog or guaranteed machine uptime.

The coordinator closes the Beads epic only after the actual final result is inspected. A blocked or partial campaign is reported and retained as such; do not close it as full scientific success. No worker may award attested/formalized/new-to-literature status.
