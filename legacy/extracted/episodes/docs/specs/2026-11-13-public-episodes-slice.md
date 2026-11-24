# Public research episode authoring slice

Task: `aro-discovery-tu3`. Owner explicitly requested work on the four public M/F/P/R episodes. This is offline evaluator authoring and reference validation, not candidate-system evaluation or scientific attestation.

## Inputs and authority

Read FOUNDATION.md and AGENTS.md in this worktree. Upstream design is in the sibling architecture worktree: `docs/specs/2026-11-10-research-capability-and-domain.md`, especially sections 3–7, and `docs/specs/2026-11-10-scientific-operating-model.md`. Accepted finite infrastructure and scoped example are in the sibling dossier worktree (`pilot/science`, `pilot/baseline`, `pilot/checkers`, and `artifacts/research-pilot-m0/finite-snapshot.json`). These siblings are read-only inputs. No source checkout or sibling may be edited. Any reused files must be copied explicitly with provenance and checked identities, never silently imported from an absolute developer path.

## Deliverable boundary

Prepare one public development episode each for model/scope (M), falsification/repair (F), proof/construction (P), and staged research decisions/continuation (R). Each needs its own task-facing problem, exact model and quantifiers, submission contract, reference outcome, accepted alternatives, known invalid submissions, minimal resource map, feedback policy and readiness limitations. Separate task-facing material from reference material for usability, but label ALL material public. No claim of secrecy or unseen ability follows.

Add only the minimal offline validators and regression tests needed to validate these reference outcomes and positive/negative controls. These validators are code judges; LLM reviews are engineering criticism, not scientific verdicts. Avoid building a general evaluation platform. The R rubric must accept substantively different valid next actions, explicitly represent staged evidence and continuation, and distinguish objective checks from unresolved human judgment. M must distinguish measured-state from disturbance-prefix information. F must retain the original refuted claim separately from any restricted child and never call finite survival a universal proof. P must fix a precise target, keep statement fidelity separate from compilation, and include wrong-statement and unsupported-axiom controls. An elementary observation-factorization lemma can be suitable as a bounded domain proof diagnostic; it must not be presented as the unapproved full single-measurement correspondence theorem, a novelty result, or general research competence.

Lean 4.35.0-rc2 is available through `lean` in PATH (coordinator observed `lean --version`). Installed mathlib/dependency availability has NOT been established. Prefer a minimal self-contained target if scientifically appropriate. Do not download or install toolchains/packages, alter pinned versions, rebuild legacy formalization, or relax proof requirements. If a necessary check is unavailable, preserve the episode specification and mark scored readiness blocked. Human semantic approval is not supplied by this task or by hashes. A compiler-checked reference may still have pending human correspondence review.

## Implementation and validation sequence

First inspect the upstream contracts and existing finite APIs. Refine the bounded episode design here before implementation. Then author specifications and references, add focused offline judges/tests, and run positive AND negative controls. Record exact commands, results, evidence identity and limitations in a report. Verify deterministic outputs in fresh processes. A hash proves byte identity, not scientific authority. Do not call construction/solution lookup a substantive research evaluation.

Independent read-only review follows authoring. Repair concrete findings with regression tests before acceptance. Acceptance concerns episode/evaluator engineering only; no status promotion, competence score or novelty judgment follows.

## Operational restrictions

One worker at a time, current Pi connection, `openai/gpt-6.1-sol`; medium reasoning for implementation, high for independent review. Maximum 90 minutes and 60 tool invocations including nested calls per worker; no nested agents, hidden retries or model fallback. Tool-call cap is instructional, not demonstrated hard enforcement. Keep partial files and an honest handoff on failure/exhaustion.

No benchmark candidate runs, 48-trial panel, private data, r=80 experiments, persistent runtime, corpus admissions, live events/blueprint/state/config/threshold/glossary changes, commits, pushes or installations. No automatic new Beads tasks. The coordinator owns task tracking. Python tests should disable bytecode/cache writes outside the worktree; evidence goes under a new task-specific artifact directory. Main checkout is dirty and must remain untouched.

## Bounded design after reconnaissance (worker, 2026-11-13)

Use `pilot/episodes/` as a standalone public authoring package, without importing
or changing the dossier schemas. Copy only the unchanged finite enumerator and
independent Bellman checker into `vendor/`; verify their bytes against the dossier
snapshot before copying and record source paths, source commit and SHA-256 locally.
Freeze episode inputs in a separate trusted JSON file; candidates cannot supply
instances, claim definitions, expected hashes or evaluator paths.

- M: compare a prefix assignment with measured-state implementability on a
  zero-gain correlated-path input and a nonzero-gain paired input. Check equality
  on observation fibers and replay submitted optimal certificates. Accept all
  optimal certificates, not only the enumerator's tie-break.
- F: preserve the fixed universal parent equality, refute it on either of two
  frozen zero-gain inputs, and create a separate nonzero-gain child with finite
  survival only. Replay certificates and check child premises before conclusions.
- P: prove the core-only observation-factorization equivalence over an inhabited
  action type. A total observation policy exists iff a path assignment is constant
  on observation fibers. The target is a necessary policy representation lemma,
  not the full dynamics/cost correspondence theorem. Keep a trusted declaration
  template separate from proof-body submissions; permit a deliberately small
  proof grammar, compile the fixed target, and inspect its transitive axioms.
  Wrong target and unsupported-axiom controls must fail. Human semantic approval
  remains pending even if the reference compiles.
- R: two explicit public evidence stages, a verified contradiction and a
  premise-restricted finite child check, followed by a self-contained continuation
  packet. Permit either an injectivity-proof plan or a source-comparison/park plan;
  both retain parent refutation and child uncertainty. Code checks identities,
  certificates, dependencies and consequence relations; human review assesses
  relevance, quality and usefulness. No prose similarity score.

Each task has a public problem, closed submission shape, reference/alternative,
negative controls and minimal resources. Standard-library unittest exercises
positive/negative cases and fresh-process deterministic JSON. Lean executes only
fixed templates with restricted proof text; this is a narrow diagnostic, not a
safe executor for arbitrary hostile Lean. No general evaluator platform is built.

## Required handoff

Report produced paths; per-episode reference and readiness; exact executed checks and counts; negative-control behavior; source versus generated evidence boundaries; known blockers and human-review needs; and any failed commands. English internal artifacts, Russian owner briefing. No fabricated success or provider billing claims.
