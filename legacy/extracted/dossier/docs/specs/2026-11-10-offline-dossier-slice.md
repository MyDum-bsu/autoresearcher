# Offline scientific dossier — implementation contract

Task: `aro-discovery-hg0`. Owner authorized this bounded next slice after the architecture review. Worktree: `<workspace>/aro-discovery-dossier`, branch `task/aro-discovery-hg0-dossier`. Base: `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`.

## Authority and non-goals

Implement an offline claim/action/evidence/dossier microcycle and prepare a proposed statement package. No live journal, blueprint, science database, corpus, configuration or tracker writes from implementation code. No daemon, Pi integration, new scientific campaign, A4 experiments, Lean builds/proof search, dependency installation, commits or pushes. A persisted dossier is illustrative evidence, not an authorized scientific status transition. No human decision or attestation may be fabricated.

Architecture authority: `<workspace>/aro-discovery-architecture/docs/specs/2026-11-10-scientific-operating-model.md`, especially §§3–6,8,10. Formal statement guidance: companion `reports/reading/2026-11-10-formal-evidence-architecture.md`, §§3–4,7. FOUNDATION and current glossary apply. Existing `scripts/reflection.py` writes the live journal: inspected and intentionally not reused or edited.

## Available immutable baseline

Coordinator copied the finite subset of M0 into this worktree without modification:

- `pilot/baseline/finite_reference.py`, its test and README;
- `pilot/checkers/finite_bellman.py`, its test and README;
- `artifacts/research-pilot-m0/finite-reference.json` and `finite-independent.json`.

`artifacts/research-pilot-m0/finite-snapshot.json` records all eight identities. Six code/test/evidence files matched the prior M0 manifest before copying; the two README files were fingerprinted at import. Do not edit these nine files. They are retained here so the deliverable works without another worktree or absolute path. Source hashes detect changed bytes; they do not authenticate a producer, freeze an OS filesystem or establish source/model correspondence.

Use `finite_bellman.check_result` for optimality/infeasibility. `check_witness` alone establishes feasibility/replay, not optimality. Do not reimplement M0 arithmetic. The trusted small adapter must recompute evidence using the unchanged independent checker; a submitted `PASS` or matching user-provided hash is insufficient. Fixed public regression reproduction is allowed; adaptive numerical search is not.

## Narrow scientific example

Use the known M0 distinction between disturbance-prefix and measured-state information. An illustrative parent proposes equality of their values within the declared two-period finite contract; `correlated_hidden_disturbance` gives a counterexample. Preserve the parent and a separately versioned restricted child. A suitable child restricts to nonzero prefix gain; `strict_gain` is an in-scope finite test, while the zero-gain counterexample is outside that child's premises. Do not claim that finite survival proves the child generally.

The implementation must mechanically express the relation, information modes, finite-game scope and child restriction. Free-form prose is explanatory, never executable semantics. Keep the initial schema deliberately narrow rather than implementing arbitrary theorem evaluation or a generic predicate language. Any universal domain is exactly the declared M0 finite input contract, not all control problems. The predicate checker must verify a counterexample satisfies the claim's premises before checking violation. Typed infeasibility is not a number; either define its relation semantics explicitly or reject it for this numeric comparison.

Required scientific distinctions:

- independently checked exact finite value/evidence;
- a checked counterexample to the matched claim version;
- finite survival on an explicit, complete test inventory;
- an inconclusive/failed/cancelled/budget-exhausted attempt with no scientific promotion;
- a proposed child and unreviewed general statement;
- novelty unassessed and human attestation absent.

These are offline record dimensions, not replacements for FOUNDATION statuses. Do not generate `formalized`, `attested` or general `proved` from this module.

## Contracts and interfaces

Choose small standard-library typed immutable records for model/scope, claim version, next action, evidence and attempt. Freeze nested values too, or defensively parse into immutable representations; a frozen dataclass around caller-owned mutable dictionaries is insufficient.

Bind evidence to the exact instance, normalized data, information modes, model/scope and claim version. Bind the next action to its claim and prerequisite records. Unknown/missing fields, duplicate IDs or JSON keys, malformed rationals, boolean-for-integer versions, unknown enum values and unsupported scope fail explicitly. Do not silently default required facts or accept nonfinite numbers. CLI failures have a clear nonzero exit and no apparent successful dossier.

Lineage is immutable and acyclic, has unique IDs, and requires existing parents. A restricted child must retain the declared parent relation/scope rather than modifying the parent in place. Missing evidence, wrong checker identity, altered certificate, altered observation semantics, changed model data, stale claim identity, missing expected cases or mismatched premises cannot support admission. Validate logical content in code instead of trusting prose/labels.

A next-action record includes uncertainty, chosen operation, prerequisites, rationale, positive/negative/inconclusive consequences, exclusions and resource limits. Mechanical eligibility checks presence, binding and known restrictions; it cannot establish the intellectual quality or novelty of the rationale. Reject a trivial record with identical consequences for every outcome. Do not pretend a text-field check proves usefulness.

Provide a documented CLI, preferably `python3 -m pilot.science`, which consumes explicit offline JSON and emits canonical JSON for a handoff and deterministic Markdown for a dossier. Include all required context rather than depending on chat history, current time, cwd-specific absolute paths, SQLite, network, or another checkout. Do not read arbitrary module paths from submitted JSON. Fresh-process export must produce identical bytes and keep parent refutation/child limitations visible.

Suggested new files, with small adjustments allowed inside these boundaries:

- `pilot/science/`: contracts/parser, finite evidence adapter, deterministic packet/dossier rendering and CLI.
- `pilot/science/tests/`: targeted unittest cases and finite bounded property/mutation checks.
- `pilot/examples/`: versioned input fixture and generated example packet/dossier.
- `pilot/science/README.md`: schema, commands, trust boundaries and limitations.
- `docs/specs/2026-11-10-single-measurement-statement.md`: proposed sealed-statement package.
- `reports/2026-11-10-offline-dossier-implementation.md`: actual tests, decisions and gaps.

No edits outside these paths. This plan and the baseline snapshot remain read-only. No changes to root pyproject/config or legacy modules. Do not introduce a second authoritative journal; the JSON files are explicit offline inputs/outputs.

## Statement package, without a proof

Prepare exact English definitions and quantifiers for the proposed correspondence result:

- finite horizon, rational linear dynamics, nonempty finite admissible complete disturbance paths;
- fixed `0 < r < T`, exact state at r, and an explicit measure/choose/disturbance timing convention;
- first open-loop block, second open-loop block depending only on the measured state;
- bounded controls, robust terminal feasibility and a signed linear terminal objective with explicit polarity;
- scenario assignments constant on equal measured states for the fixed first-block decision;
- equivalence of existence of feasible witnesses achieving a given bound;
- transformations in both directions preserving complete trajectories and all constraints;
- policy defined on reachable observations, with no hidden default outside that domain;
- explicit nonemptiness/vacuity conditions, negative fixtures, exclusions and unresolved human correspondence review.

Do not claim optimal-value existence, novelty, a completed proof or human approval of the precise formulation. Generic approval of implementation is not semantic attestation. Do not write Lean placeholder proofs or modify the installed toolchain. This package is input to a later human semantic review and proof task.

## Implementation order and acceptance

Read the baseline contracts and architecture before code. Freeze the example's input/case inventory before tests; write targeted negative tests alongside the first executable vertical path. Implement strict parsing/records, then the M0 adapter, then lineage/action eligibility, then deterministic export and the statement document. Keep individual functions small; no fallback data or hidden retries.

Required acceptance commands from this worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -m unittest discover -s pilot/science/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -O -m unittest discover -s pilot/science/tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest discover -s pilot/baseline -p 'test_finite_*.py'
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'
ruff check --no-cache pilot
ruff format --no-cache --check pilot/science
```

Use `PYTHONDONTWRITEBYTECODE=1` for all Python commands. Test normal/-O parity, two fresh CLI processes, canonical-byte regeneration and both formats. Add integrity verification for all snapshot files, preferably as an acceptance test. Exercise numeric evidence mutation, state/prefix relabeling, tampered model, unknown fields, changed claim version, outside-premise counterexample, missing cases, missing parent, cycles, input mutation, and every inconclusive operational outcome. Verify that output generation does not write any live state.

Run the applicable ripwire quality/change checks if supported; report unavailable/unsupported results honestly, never change gates to obtain a pass. No broad repository build or live `ro` command is required because no production interface changes.

## Worker envelope

One Pi developer worker, `openai/gpt-6.1-sol:medium`, no automatic orchestrator retries/fallback. Maximum 90 minutes and 60 total tool invocations including wrappers/nested calls; count explicitly and stop with retained artifacts before exceeding the ceiling. This old launch path does not yet enforce the call budget or prove filesystem isolation; prompt/worktree boundaries are not presented as a sandbox. If any limit/failure triggers, report what remains and stop, rather than reducing acceptance or silently restarting. Coordinator performs fresh checks and independent review after the implementation worker finishes.
