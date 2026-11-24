# Research capability, usefulness and domain architecture

Task: `aro-discovery-i24`. Status: proposed design decisions and evaluation protocol; no capability experiment, threshold activation or scientific attestation has occurred.

This addendum fills a gap in `2026-11-10-scientific-operating-model.md`: preventing false acceptance does not demonstrate useful research ability. The owner asked how to measure that ability, what material to use, and how domain knowledge enters the system. Sections 1–10 give decisions; §11 separates observed facts from proposals and sources. The proposed pilot counts are recorded in `artifacts/architecture-research/evaluation-plan.json`, not presented as measurements.

## 1. Name, object and scope

Working term: **research system**, Russian **исследовательская система aro-discovery**; short form **система**. This describes its purpose without implying a factory's interchangeable output or a human scientist's authority. `Agent`, `workflow`, `pipeline`, `runtime` and `harness` remain implementation terms, not the name of the whole undertaking. This is a proposed terminology decision; the dirty live glossary is not edited here.

The system's purpose is to help obtain defensible new mathematical results in the approved optimization direction and explain what those results mean. It must also recognize known results, expose failed claims, and preserve useful partial work. Writing more hypotheses, proving arbitrarily easy lemmas or running more processes is not the goal.

**Decision: domain-specific research, with reusable engineering mechanisms.** Initial domain: two-stage adjustable robust optimization, guaranteed optimal control and the explicit bridge between their information/policy models. Required supporting mathematics includes linear/convex optimization, duality, elimination, polyhedral geometry, nonanticipativity and finite-horizon dynamics. This is narrower than “all optimization,” and much narrower than general scientific intelligence. Reusing storage or a proof adapter in another field does not demonstrate competence in that field.

We do not train a new domain model now. Start with the chosen general LLM plus a versioned domain package, explicit research protocols and checkable tools. A new scientific domain requires its own source/definition package, competence episodes, evaluators and human acceptance. It cannot be activated by changing the system prompt alone.

## 2. Three questions, three kinds of evidence

| Question | Evidence required | What does not answer it |
|---|---|---|
| Is the mechanism safe and faithful? | Software contract tests, false-evidence mutations, recovery/permission tests | A persuasive final answer |
| Can it perform research work in this domain? | Fresh, bounded episodes testing modeling, falsification, construction, proof and transfer | A green unit-test suite or a known answer copied from a paper |
| Is it useful to this research program? | Accepted work on relevant questions, including the human effort needed to inspect/repair it | Number of tool calls, claims, tokens, pages or successful compiler invocations |

No single “intelligence score” combines these. Maintain a capability profile by task family, a separate integrity/reliability profile, and a campaign usefulness dossier. Safety violations are vetoes, never a small penalty offset by good mathematics. FOUNDATION's existing metrics remain; this adds evidence needed to interpret them, without altering configured thresholds.

A successful example establishes that one episode was solved under its exact conditions. Repeated held-out success across different mechanisms supports a bounded competence claim. A fresh validated research contribution supports a claim about that contribution, not general intelligence.

## 3. Capabilities and evaluation material

The **research episode** is the unit: a frozen starting problem/state, permitted resources, budget, acceptance obligations and submitted artifacts. It may span several role changes or sessions. A tool call or a proof tactic is not an episode.

| Family | What the system must do | Material | Acceptance / principal failure |
|---|---|---|---|
| **M — Model and scope** | Translate a problem into dynamics, observations, policy class, quantifiers and constraints; find an invalid transfer | Source problems and independently reviewed premise-changing variants; nearby models with different information | Trusted semantic contract plus structural tests and human correspondence review. A correct proof of the wrong statement fails |
| **F — Falsify and repair** | Produce a valid counterexample or explain why the proposed attack is outside the premises; formulate a distinct restricted child | Known false claims, true controls, explicit insufficient-information cases, planted quantifier/causality errors | Independent witness replay and premise check. Failed search is not proof; modifying the parent does not erase refutation |
| **P — Prove and construct** | Find a construction/lemma and prove a fixed target, using an approved library | Domain lemmas with trusted Lean statements; paired construction-with-answer and construction-without-answer variants; some independent proof sanity tasks | Exact sealed theorem, permitted axioms and checked dependency closure. No weakened statement, circular helper or trivial restatement |
| **R — Research decisions and continuation** | Choose a discriminating next action, respond to a contradiction, stop an uninformative branch, continue from another worker's packet | Masked historical episodes with staged evidence; fresh matched scenarios requiring a different next step; deliberately missing source/assumption | Frozen sets of admissible actions/obligations where objectively known; otherwise explicit human rubric. Not similarity to one preferred plan |
| **A — Algorithmic contribution** | Produce a feasible method or certified bound that improves a declared comparator beyond easy cases | Owner-approved family-disjoint optimization instances, baselines and budget tiers | Independent feasibility/certificate checks; bound/runtime comparison on held-out families. Infeasibility or wrong information cannot buy a better score |
| **N — Novelty and research usefulness** | Explain the relation to closest results; produce a contribution useful to an approved open question | Prospective research campaigns and current primary literature, including contrary/stronger results | Human source-based assessment separate from mathematical checking. Search silence or a new phrasing does not establish novelty |

M/F/P/R are the first capability panel. A needs its own frozen algorithmic benchmark; N is longitudinal campaign evidence, not a quick automatic test.

### Concrete domain episodes

These are **public task templates**, not a claimed private test set:

- A controller receives an exact state but not the disturbance prefix. Ask whether a scenario policy is implementable, and require a witness or counterexample under the actual observation map. M0 is a public calibration seed, not unseen evidence.
- Given a robust linear problem and a proposed dual derivation, identify a removed feasibility/boundedness premise and supply the correct scoped conclusion. The evaluator first establishes the reference claim and accepted alternatives; it does not assume a named duality theorem applies.
- Given a fixed formal correspondence statement, construct both witness transformations while preserving terminal feasibility and cost polarity. This tests proof work; giving the transformations in the prompt changes the task and must be recorded.
- Given numerical agreement on a finite grid, decide whether the next step should be a uniform bound, a missing-source read, a boundary attack or a stop. The scenario supplies enough evidence to distinguish the admissible choices.
- After a checkpoint, present a counterexample that invalidates a premise. Check whether the system revises dependencies and leaves historical evidence intact instead of continuing the obsolete proof.
- Present a theorem already covered by an accessible closest-source result. A useful result is correct attribution and reuse, not a fabricated novelty claim.

Every implemented episode must have a real reference basis: an inspected source anchor, a checked certificate, a trusted formal statement, or an explicitly constructed and independently validated fixture. These templates are not enough by themselves. If a reference cannot be established, the episode stays out of scored acceptance.

## 4. Materials, secrecy and contamination

Use three layers, with distinct labels:

1. **Public development/regression:** M0, known local failures and visible example tasks. Used to develop contracts and checkers; never described as evidence of unseen research ability.
2. **Evaluator-private capability episodes:** new task instances and structural variants, authored/validated separately and withheld from the system being tested. Split by theorem/mechanism/source family; changing coefficients or file names alone does not establish an independent family. Equivalent reformulations and variants of the same source theorem stay together. No claim of freedom from pretraining contamination can be guaranteed.
3. **Prospective campaign:** a question selected before the attempt, with fixed starting knowledge and an accountable budget. Results are checked and compared with literature after submission. This is the place for evidence of new research, including negative/partial contributions.

Masked historical reconstruction is useful but not genuine discovery: the model may already know the published solution. Hiding a proof file does not erase pretraining. Novel-to-the-episode, new-to-the-project and plausibly-new-to-the-literature are separate labels. A human can attest the last only after an explicit comparison dossier; it is not a universal guarantee of priority.

### Public benchmark policy

miniF2F and PutnamBench can test formal-tool integration and some proof skills. They are not the release gate for optimization research. The inspected miniF2F README describes olympiad/course statements and a legacy Lean installation path: do not assume compatibility with our pinned Lean. PutnamBench distinguishes finding a solution from proving a supplied one; adopt that distinction. Its original paper also warns about possible contamination through informal proofs. Do not import an old website claim of “no contamination” as a present guarantee. Pin compatible statements and licenses before any use; no benchmark was installed or run here. [S2–S3]

### Separation requirements

The evaluated worker cannot read hidden solutions, score rubrics, future evidence, evaluation logs from other runs or held-out instance generators. A fresh worktree is insufficient if the worker can read sibling directories. Test the filesystem/tool boundary before calling a set private. No public artifact from the current chat is private.

Use separate authoring, development and final-evaluation contexts. Reviewers or agents exposed to hidden answers must not transfer those answers into candidate skills, memory or prompts. Candidate configurations share the same clean starting memory; trials cannot learn from earlier trial results. A separate transfer experiment may intentionally carry approved memory, with that exposure declared.

Judge diagnostics allowed during an attempt are part of the contract: ordinary Lean compiler feedback may be available; hidden tests cannot become an unlimited optimization oracle. Once a final episode is opened to guide repairs, retire it to regression and replace it for fresh confirmation. Cache outputs and Git history must respect the same separation as files.

## 5. Metrics: precise outcomes rather than activity counts

### Machine-verifiable core

For a family with N eligible episodes and R fresh attempts per episode, define `s[i,r]=1` only when the declared result is accepted within budget and no veto is violated; otherwise 0. The planned denominator is frozen. Agent failures, exhaustion and unsupported answers stay in it. Independently diagnosed evaluator/infrastructure incidents are retained and reported separately; replacements follow the preregistered policy, never silent deletion of inconvenient attempts.

Report by family:

- **Accepted-at-budget rate:** `sum(s)/(N*R)`, with raw counts and budget. For unresolved human review, report pending rather than silently treating it as accepted. This is the primary competence measure.
- **Any-success across R attempts:** fraction of episodes with at least one accepted result; a budgeted capability diagnostic, not deployment reliability.
- **All-success across R attempts:** fraction with all attempts accepted; a stricter repeatability diagnostic. Never estimate it as a power of the aggregate average. The any/all distinction is adapted from pass@k/pass^k; our direct grouped proportions describe the actual R attempts, not a promise of independent future trials. [S1]
- **False-accept count/rate:** invalid submissions accepted by a tested gate, with the invalid-submission denominator. Assess the gate with independently established negative AND positive controls; rejecting everything must fail the useful-acceptance test.
- **Unsupported-result incidence:** attempts that make an unearned scientific claim (including “proved” from finite survival), per evaluated attempt. Evidence comes from anchored claim audits/code where possible and human review where necessary, never an LLM's own confidence.
- **Proper abstention/clarification:** separate success rates on explicitly unanswerable/out-of-scope episodes and on answerable episodes. Blanket refusal cannot yield a high capability score.
- **Proof success:** the P-family accepted rate after exact statement matching and the release gate, not compile rate. Record statement/fidelity failures separately from proof-search failures.

Task families are primary strata. Do not pool hundreds of simple numerical instances with a few proof episodes to inflate one average. Multiple coefficients of one construction do not count as independent research mechanisms. If an overall macro-average is shown, publish its fixed weighting and all family results beside it; it does not replace vetoes.

### Process quality and transfer

Measure what the process achieves, not how elegant its plan sounds:

- proportion of staged episodes where the selected next action can distinguish the remaining alternatives;
- repeated execution after a known contradiction or unchanged failure, with exceptions for an explicitly justified new test;
- continuation success after replacing the worker and supplying only the durable packet;
- adaptation under paired observation/premise changes; the same answer should not be accepted on both sides of a deliberately discriminating pair;
- acceptance on a withheld mechanism family after learning a reusable lemma/procedure on development episodes.

Where a finite hidden scenario makes these events objectively decidable, code computes them. Where multiple research paths may be worthwhile, humans assess a fixed rubric: question relevance, evidential consequence, premise discipline, responsiveness to evidence and usefulness of the resulting artifact. Reviewers see anonymized outputs where practical, may disagree, and record reasons. Disagreement remains unresolved or goes to the owner; it is not averaged into mathematical truth. LLM criticism can propose issues but cannot award scientific verdicts.

Do not score private chain-of-thought. The observable record is submitted plans/decisions, source anchors, tool actions, intermediate artifacts and outcomes.

### Usefulness and cost

For accepted work, report elapsed/compute time, model usage, actual cost when known, and human minutes spent on task preparation, hints, intervention, review and repair. Include unsuccessful attempts and separate one-time episode-authoring cost from recurring work. If no work is accepted, cost-per-accepted-result is undefined, not zero. Token counts and provider billing remain different quantities.

Compare system-assisted and existing work on matched tasks. Without measured human baseline times, report observed effort and acceptance; do not claim time saved. A human can consume a valid negative result, a reusable lemma or a source-based closure of a false novelty claim. Count each predeclared episode objective once; splitting it into many nodes does not multiply credit.

In campaigns, use a **contribution dossier**: exact result and evidence scope, closest-source delta, relevance to an approved question, independent reproduction, limitations, downstream use and human review effort. The owner assesses significance. A threshold in a benchmark can establish an improvement there, not global novelty. Scientific novelty is not reduced to a fully automatic scalar.

## 6. Comparisons that identify the system's contribution

Hold the chosen model/provider/reasoning configuration constant first. Compare:

- **B0 — simple strong baseline:** one Pi session with the same task, allowed sources, tools, permissions and resource caps; no structured domain retrieval or campaign memory. It may reason, use Lean and inspect sources. Do not handicap it to one model response.
- **B1 — research system:** the same resources plus the proposed domain package, retrieval/working-set construction and explicit research protocol. Retrieval, preprocessing, hidden helper calls and all worker calls consume the declared budget/accounting.
- **Ablations, later:** remove one feature at a time—domain skill, structured retrieval, learned memory, explicit adversary phase or formal feedback—while leaving other resources fixed. An ablation is a diagnostic experiment, not permission to remove production integrity gates. Deliberately unsafe variants stay isolated and never publish.

For the B0/B1 comparison, both can access the same admissible source pool and trusted tools. Automatic curation versus self-retrieval is a system advantage being tested; do not give B1 the hidden answer or count its preparation as free. For a knowledge-resource ablation, explicitly label the changed source access and do not confuse it with the orchestration comparison.

If B1 brings no useful gain at comparable resource limits, simplify it. If it succeeds only with more compute, report the quality/cost curve; do not attribute the gain entirely to architecture. Test broader model choices only after establishing the evaluator and within owner-authorized provider rules.

## 7. Run protocol and proposed first panel

### Before scored trials

An evaluator author defines each task and hidden acceptance; another check establishes that the task is valid, not already solved by an admitted dependency, and that at least one reference outcome exists where solvability is claimed. Include valid alternatives, known invalid artifacts and source/statement ambiguities. Prove the gate can reject the wrong model and accept a correct result. Any grader defect blocks scoring until the affected reference and verdicts are repaired.

Register model/provider/reasoning, source/knowledge/skill/tool versions, Lean/dependency versions, evaluator versions, input identities, permission profile, resource ceilings, trial counts, stopping rules, allowed feedback, intervention policy and incidence/retry policy. The evaluation controller is deterministic; Pi executes the candidate sessions. The tested candidate cannot change evaluators, task sets, its own evaluation budget or acceptance policy.

### Small diagnostic panel, proposed, not authorized execution

- Four public development episodes: one each for M/F/P/R, used to debug task validity and evaluation plumbing.
- Eight separately curated private episodes: two per family, split by mechanism rather than numeric seed.
- Two configurations, B0 and B1, with three fresh attempts for every private episode: **48 allocated private attempts**. Counts are design choices, not sample-size guarantees or measurements.
- Establish per-family resource caps on public development episodes, then freeze them before private comparison. The existing 90-minute/60-call worker envelope is an upper bound, not a default entitlement for every trial. Native call-count enforcement and private isolation must be demonstrated first; instruction-only caps cannot support a hard-budget claim.

This panel diagnoses missing abilities and evaluator defects. Eight private episodes do not justify a broad reliability certificate. Report raw paired outcomes, variation by family and pending reviews. Any statistical comparison must treat task/source families as clusters, not regard repeated trials or coefficient variants as unrelated observations. Preregister an uncertainty analysis before a larger panel; do not use max-minus-min from a few runs as a confidence interval. Broader acceptance requires more independent families and a separately frozen confirmation set, with size chosen from pilot variance and the decision at stake.

No arbitrary percentage threshold defines intelligence. Before release, the owner sets the required family-specific competence, review burden and resource limits. Every known critical integrity failure blocks promotion pending repair and fresh confirmation. Zero observed violations is not a guarantee of zero future risk.

### Execute and interpret

Run sessions sequentially with fresh state, counterbalanced configuration order and no cross-trial feedback. Preserve every assigned trial ID and terminal reason. A successful result after a human mathematical hint belongs to an assisted track, not the unassisted success numerator. Always account for the hint and review effort. Controlled checkpoint/restart tests are labeled experiments, not hidden operational incidents.

Use the public set for diagnosis and changes; freeze a candidate before the private set. Open the private results once for the declared decision. Record null results and regressions. Do not repeatedly peek, adjust the prompt and announce the best score as a clean test.

After capability evaluation, authorize one bounded real research shift with a contribution dossier. A held-out proof benchmark shows competence; only work on real approved questions can establish project usefulness. The larger campaign continues to use FOUNDATION's human review and autonomy policy.

## 8. Domain package: what the system knows and can do

The **domain package** is a versioned bundle of admissible sources, exact definitions, proven/reproduced objects, procedural skills, tool contracts and capability tags. It contains no new source of scientific truth: its knowledge entries resolve to blueprint nodes, source anchors and artifacts.

| Resource | Contents | Runtime use / acceptance |
|---|---|---|
| **Model and terminology registry** | Dynamics, domains, observations, timing, admissible policy classes, objectives, quantifiers; alternative formulations remain distinct | Build the task's model/scope contract before retrieval or proof; changes invalidate reuse under the old identity |
| **Primary-source index** | Admitted PDF/TeX, exact anchors, extraction status, assumptions/conclusion, closest-result comparisons | Retrieve on demand; formulas require direct original inspection. A source statement is not automatically a formally proved library theorem |
| **Scientific dependency graph** | Definitions, scoped claims, counterexamples, proof obligations, accepted evidence and explicit human decisions | Construct the working set; include relevant contradictions, exclusions and supporting statements. Similarity cannot authorize a lemma |
| **Proof library** | Pinned Lean/mathlib plus project lemmas with trusted statement mapping and axiom records | Search by actual types/assumptions; exclude scratch and target-equivalent declarations from proof-evaluation access |
| **Construction/evidence library** | Exact certificates, validated witnesses, model transformations and refuted constructions | Reuse as input or comparator with scope binding; new parameters/observations require new checks |
| **Procedural skills** | Literature comparison; model/quantifier audit; duality with premise checks; counterexample design; derivation; Lean repair; discrepancy handling; clear technical exposition | Load the relevant version at the corresponding operation. A skill guides work but never supplies theorem authority |
| **Tool registry** | Narrow source reading, finite checking, exact/symbolic validation, solver/certificate interfaces, Lean checks, graph lookup and artifact inspection | Explicit input/output, domain limits, authority, side effects and failure modes; reject unsupported scope instead of silently approximating |
| **Methodological memory** | Evidence-linked lessons about failed approaches and useful procedures | Reviewed promotion and rollback; no raw failed trace becomes a new global instruction |

### What exists versus what is proposed

Freshly tested M0 supplies a finite reference/checker and A4 open-loop certificate route, not a general optimization research engine. The repaired offline dossier supplies scope binding and export for a narrow finite example. Neither supplies automated scientific question selection or a verified domain proof library.

Existing `skills/` contains source/statement/procedure checkers; its README explicitly labels some components as stubs and statement lint as heuristic. Do not infer new-system readiness from that README or reuse legacy verdicts without revalidation. Existing global `logika` and `technical-style-editor` are advisory review procedures under FOUNDATION, not mathematical judges. General course-oriented optimization skills may suggest terminology or methods, but are not substitutes for research-level source anchors.

Lean/mathlib versions have been inspected, but the proposed correspondence proof and strengthened release gate have not run. General symbolic tooling, solver adapters, a full source-aware retrieval graph and private evaluation service are proposed capabilities, not installed-and-tested claims. Each resource enters the capability manifest only after its own contract checks.

### How this enters the harness

At shift creation, resolve the question's domain/model IDs and permitted action families. Select a small resource manifest: relevant source and graph closure, a versioned skill subset, allowed tools and their capability limits. Pi receives that working set and tool surface, rather than the full global skill catalog. Log what was actually loaded/read/called so an evaluation can reproduce the exposure.

The deterministic boundary validates tool scope and returned evidence. A retrieval result cannot grant a permission or raise a status. Unsupported observations, uncertainty sets or proof environments cause a typed refusal/escalation. Source code or generated Lean tactics execute only in the previously specified isolated boundary. Domain specialization resides in this package and its tests, not in an undocumented paragraph of the coordinator prompt.

Test the package through ablations and transfer: does retrieving the right assumptions reduce wrong-model proofs; does a counterexample skill improve valid refutations without increasing false ones; does reusable memory help a different episode rather than merely repeat a known answer? Keep a resource only if it earns its complexity or is an integrity requirement.

## 9. Learning and generalization

Distinguish three mechanisms:

- **In-context learning:** the current session uses examples; it disappears unless exported.
- **Externalized learning:** reviewed lemmas, counterexamples and procedural lessons persist in versioned knowledge/skills/tools. This is the initial approach.
- **Weight updates:** fine-tuning or reinforcement learning changes the model; deferred until a diagnosed limitation, suitable data and a separate evaluation contract justify it.

A new skill or memory rule is a candidate change. Require provenance, scope, supporting episodes, an ablation/transfer check, independent review and a rollback version. The system cannot rewrite its evaluators, grant itself new scope or train on final-evaluation answers. Increasing memory volume is not a learning metric. Improvement means better accepted work on fresh related tasks at accounted cost, without lost integrity.

## 10. Architectural changes and next work

Add explicit contracts for `ResearchEpisode`, `EvaluationProtocol`, `CapabilityManifest`, `DomainPackage`, `TrialRecord` and `ContributionDossier`. These are proposed names, not implemented schemas. The science graph still stores scientific facts; a separate evaluator record stores trials and scores and cannot promote scientific state. Human-approved changes enter through authorized project interfaces, not ad hoc writes.

The order is now:

1. Finish the bounded offline dossier acceptance; this engineering slice is independently checked, not a capability score.
2. Draft and independently validate the first public M/F/P/R episode specifications, including reference outcomes and negative controls; map each capability to a domain resource. Do not launch a benchmark before its evaluator is trustworthy.
3. Approve semantic statement packages and implement the necessary proof-release checks. Add the minimum domain tools needed by those episodes; avoid an encyclopedic knowledge-ingestion project.
4. Demonstrate Pi budgets, effective settings, isolation and fresh-session reset; establish a genuinely private evaluator boundary.
5. Ask the owner to authorize the frozen diagnostic panel, budgets and interpretation rules; execute B0/B1 comparisons and report limitations.
6. Only then authorize a bounded real scientific shift and assess contribution/usefulness. Further generalization, more workers or stronger autonomy require fresh evidence, not a successful software build.

A source-reading or mathematical design question may be worked on before the full panel when explicitly authorized; the restriction is on claiming evaluated competence or autonomously expanding scientific scope. This plan does not make useful research wait for a large platform. It requires evidence proportional to the claim being made about the system.

## 11. Sources and verification limits

**Observed local authority:** FOUNDATION §§0–10 (optimization direction, source trust, code judges, human authority, metric/threshold policy); current `docs/GLOSSARY.md`, especially the pilot vocabulary; `skills/README.md` (declared heuristic/stub status); architecture and formal-evidence reports in this worktree. The repaired dossier's coordinator acceptance is in `<workspace>/aro-discovery-dossier/reports/2026-11-10-offline-dossier-acceptance.md`.

**S1 — Repeated success versus repeatability:** Yao et al., [τ-bench, arXiv:2406.12045v1](https://arxiv.org/pdf/2406.12045v1#page=4), PDF pp.4–5, “Pass^k metric.” Original PDF text inspected. We adopt the distinction, not its customer-service tasks, success figures or simulated-user setup. Our family-stratified research protocol is a project design.

**S2 — Formal integration diagnostic:** [miniF2F official README](https://github.com/openai/miniF2F), sections Overview, Structure and Versioning, inspected for this task. Describes contest/course statements, optional proofs, validation/test split and a versioned benchmark. Repository page is mutable; pin an appropriate compatible revision before execution. No current score, statement-count or Lean-4 compatibility claim is imported here.

**S3 — Find versus prove:** Tsoukalas et al., [PutnamBench, arXiv:2407.11214v1](https://arxiv.org/pdf/2407.11214v1#page=4), PDF p.4 “Factored Solutions”; p.23 Figure 20 discusses potential indirect contamination from informal proofs. Original PDF text and the [official project page](https://trishullab.github.io/PutnamBench/) inspected. We use these as reasons to separate construction from supplied-answer proof and to retain contamination caveats; no reported benchmark score transfers to aro-discovery.

**S4 — Engineering evaluation guidance, not mathematical authority:** local Polomodov notes `research/01-agent-evals-production-grade.md` (2026-07-18), §§2,4,6–9, and `research/16-agent-autonomy-boundaries.md` (2026-10-02), §§4,7–9, under `<local-docs>/docs/polomodov/`. Paraphrase of the author's guidance: evaluate frozen episodes with an explicit contract, repeated trials, full human effort and separate reliability/ability. Our transfer is the domain research protocol above. The first article's live fetch timed out; local notes were inspected, not represented as a fresh verification of all quoted upstream studies. No external score, cost or reliability number from those notes is used here. URLs: [evaluation](https://polomodov.tech/2026-07-18-agent-evals-production-grade/), [autonomy](https://polomodov.tech/2026-10-02-agent-autonomy-boundaries/).

**Not established:** a measured capability profile, new scientific discovery, benefit from domain skills/retrieval, any benchmark performance, evaluator privacy, current public-benchmark compatibility, safe autonomy or a statistically justified release threshold. No evaluation model calls, mathematical experiment, corpus admission, global glossary/config change, commit or push is authorized by this document. The proposed pilot is a design for later approval, not a run already scheduled.
