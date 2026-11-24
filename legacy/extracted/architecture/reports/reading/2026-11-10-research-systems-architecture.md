# Research-system architecture: primary-source decision review

Status: research and design input, not runtime implementation or scientific attestation.
Date: 2026-11-10. Task: `aro-discovery-dub`. Scope: the operating model for a mathematical research campaign, hypothesis handling, evidence, memory and Pi integration. Formal evidence has a separate companion review, `2026-11-10-formal-evidence-architecture.md`.

## Decision

Adopt a human-directed research campaign with bounded, artifact-producing investigations. Use Pi as the agent execution platform. Build a small scientific domain layer that decides which operations are eligible, binds claims to evidence and preserves history. Do not build another general agent platform or use a solver score as a research agenda.

This is a design recommendation grounded in the sources below and in the project's observed failures. None of the external systems' reported scientific gains or costs is treated as an estimate for aro-discovery.

## Research method and stopping rule

Questions: which mechanisms help select useful questions, prevent wrong-scope acceptance, preserve counterexamples, support formalization and survive worker replacement? Which existing implementation can be adopted without replacing project authority or Pi?

Inspected targeted primary material rather than collecting a broad catalog: AI co-scientist, ZIB's Agentic Researcher, AlphaEvolve/FunSearch, the Station, local Stigmergy, installed Pi documentation/source, and current project modules. The formal-evidence researcher covers Lean and proof-agent sources separately. Search results were discovery leads only. External PDFs were read from original PDF text extraction, not prior markdown summaries; no mathematical theorem was imported from those PDFs. No package was installed or evaluated as a functioning dependency.

Targeted discovery used paper titles and official repositories; a retained search query was `site.github.com google-deepmind funsearch README evaluator sandbox license`. Retrieval date is above. Stop when the architectural decisions have a primary-source basis and additional products would only duplicate a mechanism. A feature/version not inspected stays unverified. Machine-readable identities for seven inspected input files are retained in `artifacts/architecture-research/source-identities.json`; this does not admit them to the scientific corpus.

## Sources and what they actually support

### S1 — AI co-scientist: hypothesis operators, not scientific authority

Primary source: [Gottweis et al., arXiv:2502.18864v1](https://arxiv.org/pdf/2502.18864v1#page=8), PDF pp.8–13, §§3.2–3.5. Read the entire selected section.

Observed: the scientist's goal becomes a research-plan configuration; generation, reflection, ranking, proximity, evolution and meta-review roles cooperate through a supervisor and persistent context. Generation includes literature-grounded proposals and identification of testable intermediate assumptions (p.10). Ranking uses model-mediated pairwise tournaments (pp.11–12). Evolution creates new hypotheses rather than overwriting earlier ones (p.12). Meta-review appends feedback to later prompts (pp.9–10,12–13). Scientists can refine goals and provide hypotheses/reviews (p.13).

Adopt: explicit proposal operators; distinguish an assumption from a conclusion; parent/child lineage for repaired hypotheses; periodic summaries of recurrent failures; human direction-setting.

Do not adopt: model-based correctness/novelty decisions as verdicts, Elo as a scientific truth or usefulness score, unrestricted asynchronous expansion, or automatic accumulation of critiques in authoritative prompts. The paper's reasoning roles are proposal mechanisms under FOUNDATION, not judges. Its biomedical validation results are outside this comparison.

Design consequence: generate a small set of alternative explanatory claims or methods, each with a falsifier and decision consequence. A revision is a new object. Reflection proposes a change to the playbook; it does not install it.

### S2 — ZIB: research contract and bounded investigation

Primary sources: [Zimmer et al., arXiv:2603.15914v1](https://arxiv.org/pdf/2603.15914v1#page=4), PDF pp.4–9; repository [README](https://github.com/ZIB-IOL/The-Agentic-Researcher/tree/82d1e3fec5f78863c70c015d2090b9823966e97b), [INSTRUCTIONS.md](https://github.com/ZIB-IOL/The-Agentic-Researcher/blob/82d1e3fec5f78863c70c015d2090b9823966e97b/INSTRUCTIONS.md), [MIT license](https://github.com/ZIB-IOL/The-Agentic-Researcher/blob/82d1e3fec5f78863c70c015d2090b9823966e97b/LICENSE). Repository revision obtained from the GitHub commits API, not guessed from a branch label.

Observed: levels distinguish assigning individual tasks from autonomous work within a researcher-provided plan (p.4). Inputs are research question, tools/data and prior work (p.5). CLI agents operate inside a sandbox, and each investigation records goal, hypothesis, method, implementation, results, analysis and next steps (p.6). The loop includes evaluation, analysis and reporting (p.7). It distinguishes failed code from a failed idea and warns against manipulating evaluation (p.8). The current README lists Pi support and a launcher; it also describes copying instruction templates and creating `TODO.md`. Instructions X/M1/M2 require precise notation, derivation before implementation and verification before claims.

Adopt: a bounded research assignment, persistent dossier, source checking, explicit hypotheses/limits and analysis of failures. Use controlled comparisons; when interactions matter, preregister a factorial design rather than imposing one-variable-at-a-time as a universal mathematical rule.

Do not adopt wholesale: its task file, auto-commit loop, broad autonomy, or script-pass label `verified` as a substitute for scoped evidence. It would conflict with Beads, conservative Git and FOUNDATION's proof distinctions. The sandbox launcher's security claims are not penetration-test evidence; the README explicitly disclaims security guarantees.

Design consequence: study its sandbox configuration if our access-boundary spike needs it, but do not install the full launcher or overwrite AGENTS. MIT permits reuse subject to its notice; compatibility and mount/credential isolation remain untested.

### S3 — AlphaEvolve and FunSearch: searchable methods need an external evaluator

Primary sources: [AlphaEvolve, arXiv:2506.13131v1](https://arxiv.org/pdf/2506.13131v1#page=4), PDF pp.4–7, Figure 2 and §§2.1–2.4; [FunSearch repository](https://github.com/google-deepmind/funsearch/tree/cc53f274237d7ab05c19df939edbc1f9616a7c19), [evaluator.py](https://github.com/google-deepmind/funsearch/blob/cc53f274237d7ab05c19df939edbc1f9616a7c19/implementation/evaluator.py).

Observed: AlphaEvolve receives an initial program and external evaluation code, samples existing programs, generates edits, evaluates and stores results. Its abstraction may be a construction, a search procedure or another program representation. FunSearch's published repository states that language models, untrusted-code sandbox and distributed infrastructure are not supplied. The inspected `Sandbox.run` raises `NotImplementedError`. Its evaluator registers a program if some per-test scores are present; that behavior is not our complete-coverage release gate. Software license is Apache-2.0; other repository material uses CC-BY according to its README.

Adopt: an explicit candidate-method boundary, fixed independent evaluation, parentage, diversity among search methods and retaining failures. Mathematical certificates must be evaluated independently from the code that proposes them.

Defer: an evolutionary engine until there is an approved algorithmic question, a reliable objective and a meaningful comparator. Do not optimize number of hypotheses, compiler successes or publication events. Do not import the reference evaluator as a safe general sandbox or as complete scientific acceptance.

Design consequence: search heuristics are replaceable plugins behind a stable candidate/evidence interface. They are not the top-level research controller.

### S4 — Station: accumulated research explanations

Primary source: [Autonomous Mathematical Discovery in an Open-World Multi-Agent Environment, arXiv:2608.23691v1](https://arxiv.org/pdf/2608.23691v1#page=2), PDF pp.2–4, §§2–3.1 and Table 1.

Observed: separate rooms support computation, communication and archival publication; agents are replaced while an archive persists. The archive stores agent-authored papers for later workers. Publication uses automated review. The reported experiments use several model families and long open-world runs.

Adopt: concise reusable research explanations with assumptions, constructions and failed paths; context packets drawn from durable scientific artifacts; successor workers need the reason an approach failed as well as its execution outcome.

Do not adopt: a simulated society, votes/model review as acceptance, self-publication by the author, unrestricted agenda changes or the reported scale. Mathematical claims and comparative discoveries reported in that paper were not reproduced in this study and are not imported as facts about our domain.

Design consequence: preserve a short interpretation with each evidence bundle, explicitly marked as interpretation. Every interpretation links to checkable claims and original evidence; an appealing narrative cannot promote itself.

### S5 — Stigmergy: durable coordination with a guarded writer

Primary source: local `<workspace>/stigmergy/docs/spec.md`, §§7–8, especially readiness guards, worker proxy, lease expiry and idempotent station execution (previously inspected in the pilot design; re-read the cited guard section for this review).

Adopt: a worker's bounded right to submit, durable signals, explicit requeue and restart from artifacts. Beads and research state have different roles. The runtime may propose a follow-up in the research record but must not manufacture human tasks.

Do not adopt: its factory task replacement, merge/commit defaults or runtime dependencies. One worker is enough to test durable sequential handoff. Reusing the principle does not require using its scheduler or counter.

### S6 — Pi: use the installed execution surface instead of rebuilding it

Primary sources installed locally, version **1.5.1**:

- `.../@earendil-works/pi-coding-agent/docs/sdk.md`: Session lifecycle, Prompting, Subscribing to events, Configuring a session; read in full.
- `docs/extensions.md:973–990`: `tool_call` can block; `terminate` has batch semantics.
- `docs/extensions.md:788–813,2790–2800`: execution events and nested calls, with `parentToolCallId`.
- `docs/settings.md:122–136`: agent-level and provider-level retries are separate.
- `examples/extensions/permission-gate.ts`: fail-closed headless permission example, read in full; a regex example is not a complete sandbox.

Primary source for installed `pi-extensible-workflows` **6.3.0**: `subagents/README.md`, lifecycle/retry/worktree behavior; `src/pi-runtime-adapter.ts:203–228` adds running tool calls and removes each after completion.

Consequences verified by documentation/source inspection, not a runtime prototype:

1. `tool_call` permits a native pre-execution budget/permission gate. Nested calls also traverse it. Persist admitted call IDs before allowing side effects; track wrappers and nested calls with an explicitly declared counting rule. A single shell call can still run many commands, so tool counts are not a compute/security boundary.
2. `tool_execution_end` observes finalized calls, including failures. A progress snapshot's empty `toolCalls` is not a total-call counter; the observed removal explains M0's lost final count.
3. `agent_end` is not final idleness: retries/continuations can follow. Use `agent_settled` or the documented lifecycle envelope and test it.
4. SDK `cwd` explicitly binds project discovery and built-in paths. M0's prompt-level `cd` instruction is not a filesystem permission boundary.
5. `retries: 0` at the subagent orchestration layer does not establish that Pi's agent-level retries are off. SDK settings document agent retries enabled by default. Freeze effective per-run settings, disable or explicitly budget/document each layer, and observe retry events. This review did not inspect secret-bearing current account/settings files and cannot infer whether historical M0 requests internally retried.
6. Durable Pi transcripts are useful operational traces. They are not scientific state, full nested-tool audit history, or an authorization ledger. SDK sessions and the subagent extension have different recovery boundaries; do not equate a new run from a stored request with continuation of an old scientific attempt.

Adopt: existing model/session/tool execution, stored login, reasoning levels, cancellation and lifecycle events. Prefer a thin project extension/adapter. If the installed subagent path cannot enforce an explicit cwd, required hooks and safe snapshot capture, use the same Pi SDK for an isolated worker host; do not implement a replacement model loop. Verify this seam before choosing a live launcher. Do not change global Pi settings during research.

### S7 — Project reality: the missing layer is scientific decision-making

Fresh source inspection:

- `src/aro/cycle.py:39–104` journals a plan, soft theory-first reason and reading gate. These functions do not themselves make every independent scientific write depend on the plan's authorization.
- `src/aro/stateview.py:30–120` renders thread/family/queue/portfolio summaries; it is not a claim-scoped packet of applicable theorems, counterexamples and next discriminating action.
- `src/aro/journal.py:16–17,45–57`: read accepts a path; append uses a module-global journal path and does not expose an explicit target/lock/fsync transaction API. The previous plan's possible isolated adapter deficiency is now confirmed by source, though crash behavior has not been tested here.
- `src/aro/blocks.py:59–81` and `src/aro/sciencegraph.py:619–662`, together with the earlier restart audit: direct graph writes and replay omissions require complete event coverage before a fresh projection can be trusted. The earlier destructive backfill experiment was not rerun.
- M0 report in `<workspace>/aro-discovery-baseline/reports/2026-11-10-baseline-execution.md`: independent finite/LP certificate checks work locally, but there is no integrated scientific campaign. Its private holdouts, Lean and live runtime are explicitly not run. The r=80 target was a proposed follow-on, not an established research contribution.

Adopt: terminology, charter authority, useful source anchors, freshly checked M0 regression artifacts, and existing Beads for human-directed implementation tasks. Legacy code is a reference for interfaces and failure cases, not automatically trusted dependency code.

Change before live use: an explicit safe root/append API within the authorized `aro.journal` boundary, total replay of accepted facts, claim-to-model binding, an admissible-next-action decision contract, and scoped memory retrieval. No module-global path monkeypatch as production isolation; no second unauthorized writer.

## Adoption summary

| Capability | Decision now | Cost / condition before adoption |
|---|---|---|
| Pi model/session/tool execution | Reuse installed platform | Prove per-worker hooks, cwd, cancellation and retry settings in an isolated integration spike |
| Scientific controller | Build a small domain state machine plus LLM proposal role | Own the claim/model/evidence contract; do not hardcode a single search strategy |
| Hypothesis operators | Adapt co-scientist-style generation/refinement | All results remain proposals; testable deltas and immutable lineage required |
| Research dossier | Adapt ZIB and Station ideas | Bind narrative to evidence; no new task-file truth store or auto-publication |
| Program evolution | Defer | Needs a discriminating, protected objective and budget-matched baseline |
| Durable coordination | Adapt Stigmergy principles | No Stigmergy scheduler/runtime dependency; one active worker |
| Lean support | Reuse kernel/mathlib and baseline compiler loop; see companion review | Statement fidelity and allowed axioms precede a prover-agent integration |
| Blueprint presentation | Use an export from the scientific graph | No separately editable proof-status store; compatibility checked before installation |
| Memory search | Typed relations and deterministic scope filters first | Embeddings only after measured retrieval failures; similarity never authorizes reuse |
| General research framework | Do not install wholesale | None inspected replaces Pi plus our scientific authority contract without conflicting defaults |

## What this research does not establish

It does not prove any new optimization claim, certify third-party reported discoveries, demonstrate a working sandbox or choose a paid-service tariff. It does not amend FOUNDATION or activate autonomy. External PDF sources remain review inputs outside corpus admission. Source facts, project observations and design proposals are separated above so later evidence can change the decision without rewriting history.
