# Architecture research: review and validation record

Date: 2026-11-10. Task: `aro-discovery-dub`.
Scope: documentation and architecture research, not implementation or scientific verification.

## Deliverables

- `docs/specs/2026-11-10-scientific-operating-model.md`
- `reports/reading/2026-11-10-research-systems-architecture.md`
- `reports/reading/2026-11-10-formal-evidence-architecture.md`
- `reports/briefings/2026-11-10-scientific-architecture.md`

All are new files in `<workspace>/aro-discovery-architecture`, branch `task/aro-discovery-dub-architecture`, base `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`. The source checkout's existing changes are not part of this task.

## Worker execution

Only one worker ran at a time, using the current Pi connection and `openai/gpt-6.1-sol:high`.

1. Formal-evidence researcher `97d7d79c-7d99-4e70-bf75-3b8120241605` completed and returned a report. Its role was read-only; the coordinator persisted the terminal text, then made minor editorial/whitespace corrections. The researcher reported 52 tool invocations; that is self-accounting, not an independently enforced ceiling.
2. Initial independent reviewer `a7f0213f-ec2a-4da4-8f41-ea82ce462acc` ended `failed`, with `INTERNAL_ERROR: Subagent run was interrupted before completion`. Inspection returned no final review. Its output is not counted as acceptance. The persisted state does not identify the underlying interruption cause; absence of timeout errors is not evidence of verified timeout enforcement.
3. After inspecting the failure, the coordinator explicitly launched focused replacement `a0cecb01-0a8b-42dc-9b41-4d99f658340b`: document-only review, 10-minute timeout, at most 12 reads, same model, no retries. It does not repeat external research or scientific runs.

No fallback model or automatic orchestrator retry was requested. Internal Pi/provider retry settings were not audited for these historical sessions, so no stronger absence-of-retry claim is made. Actual provider billing is unknown; tool-reported accounting is not an invoice.

## Coordinator validation

Executed for the four deliverables:

```sh
python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py --language ru reports/briefings/2026-11-10-scientific-architecture.md
python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py --language en docs/specs/2026-11-10-scientific-operating-model.md
python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py --language en reports/reading/2026-11-10-research-systems-architecture.md
python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py --language en reports/reading/2026-11-10-formal-evidence-architecture.md
```

The actual invocations used absolute paths into the architecture worktree. Initial style findings were corrected; the second pass returned no findings for all four files. A separate Python check confirmed UTF-8 decoding, final newlines, absence of trailing whitespace/NUL/replacement characters, and existence of four core cross-document references. It initially caught a whitespace-only line in the formal report; after correction the check passed. `git diff --check` also passed, but does not cover these untracked files; the explicit whitespace check supplies that coverage.

Source identities for seven inspected PDF/repository inputs are retained in `artifacts/architecture-research/source-identities.json`; temporary coordinator-owned downloads were removed after capture. This register is provenance metadata, not corpus admission or a scientific gate artifact.

No mathematical test, Lean build, benchmark, runtime implementation, integration/sandbox experiment or package installation was run. These remain proposed acceptance activities, not observed successes. No FOUNDATION, scientific journal/status, corpus or configuration changes, commits or pushes were made by this task.

## Independent review

The focused reviewer completed. It found no mandatory architecture repair and assessed that the documents answer the owner's request at design level. The coordinator accepts that review as a design check only. The reviewer's final wording “Merge verdict: OK” does not authorize commits, merging, runtime activation or scientific attestation.

The result below is preserved verbatim. Its claims are confined to document consistency; primary-source observations remain supported by the companion research reports.

# Independent architecture review — aro-discovery-dub

**Scope:** Read-only design review of the three requested documents. No prior-run logs, implementation files, experiments, builds, or external sources were consulted. This is not mathematical verification or implementation acceptance.

References below use **Spec** for `<workspace>/aro-discovery-architecture/docs/specs/2026-11-10-scientific-operating-model.md` and **Briefing** for `<workspace>/aro-discovery-architecture/reports/briefings/2026-11-10-scientific-architecture.md`.

## Blockers and required repairs

No issues found.

No evidence-backed P0, P1, or P2 defect qualifies for reporting in the reviewed design. No mandatory architecture repair is identified.

## Does the architecture answer the owner's request?

**Yes, at the requested design level.** It replaces numerical activity as the default objective with a decision-relevant scientific cycle: specify the question, compare sources, attack a scoped hypothesis, interpret the evidence, and justify the next action. It provides hypothesis-generation operators, reasoned selection, evidence requirements, proof-release rules, adoption/defer decisions, and a changed implementation sequence—not merely another runner proposal.

It does **not** claim to have proved the proposed correspondence theorem, established novelty, validated the sandbox, or accepted an implementation. Those limitations are explicit and appropriate to this review (Spec:328–330).

## Assessment

### Scientific scope and hypothesis discipline

The claim package includes the model, observations, policy class, quantifier order, objective polarity, premises, source comparisons, falsifiers, evidence route, and lineage (Spec:65–79). This directly addresses the risk of optimizing or proving a different problem from the intended one.

Generation is constrained to identifiable mathematical moves rather than an unstructured list of ideas. Selection asks what decisions would follow from positive, negative, and inconclusive outcomes, and whether cheaper evidence suffices (Spec:83–108). Acceptance is consequently scope-dependent rather than a universal numerical score. This is a substantive operating philosophy, not just administrative metadata.

### Human authority and no LLM judges

Campaign direction, attestation, autonomy, source admission, budgets, and threshold changes remain human-controlled. Level 3 and one active worker are retained; sequential role changes are not presented as independent verification (Spec:37–43).

The role table keeps proposal, checking, publication, and attestation separate. In particular, the publisher is deterministic and cannot accept a worker-supplied PASS; an actor label is explicitly insufficient authorization (Spec:47–59). Model-based criticism remains advisory. This is consistent with `<workspace>/aro-discovery/FOUNDATION.md`, especially §§5–7 and §9.

### Finite state-policy correspondence

The proposed first theorem is appropriately bounded: finite nonempty disturbance paths, finite-horizon rational linear dynamics, one exact state measurement, and a fixed closing time. The condition equates continuation programs for indistinguishable measured states—not merely equal disturbance prefixes (Spec:154–160).

Crucially, the design recognizes that the equivalence classes depend on the first-block choice and dynamics. It requires transformations in both directions, preservation of trajectories and constraints, and a bound-feasibility formulation rather than assuming an attained optimum. Continuous uncertainty, noisy observations, multiple closings, affine-rule exactness, and `r=80` improvements are expressly excluded.

That is a useful semantic infrastructure target even if already known. Whether its eventual definitions and proof actually establish the correspondence remains a later acceptance question.

### Proof meaning, validity, and evidence status

The separation of semantic correspondence, sealed-statement validity, and scientific interpretation is sound (Spec:146–150). The release contract goes beyond successful compilation: immutable targets and dependencies, a nonempty declaration inventory, complete checking, trusted-statement matching, and a positive axiom allowlist (Spec:164–170).

Scientific status is also separated from correctness evidence, scope, provenance, novelty, usefulness, operational outcome, and human attestation. A worker timeout cannot become a refutation or automatically overwrite a claim; campaign-level timebox/descoping policy is retained (Spec:128–140). This avoids both a generic “verified” flag and an unauthorized replacement of FOUNDATION statuses.

### Adoption decisions and next slice

The adoption policy is selective: retain Pi as the execution substrate, begin with direct Lean feedback, defer additional proof-search interfaces until needed, and avoid a replacement agent framework. The Briefing explains what is borrowed and what is deliberately rejected from the surveyed systems; these are design choices, not claims that published success rates will transfer.

The next slice is bounded and useful: one claim version, one eligible action, one scoped outcome, and one reconstructible handoff, without a daemon or live journal writes (Spec:299–310). Its acceptance checks cover wrong-scope evidence, incomplete outcomes, preserved refutation lineage, inconclusive attempts, deterministic export, and fresh-session reconstruction. Its stop rule prevents inability to articulate a real decision from becoming justification for more runs (Spec:312–314).

## Nonblocking observations and handoff conditions

These are existing design obligations, not additional defects:

- Before proof development, seal timing, observation domain, objective sign, constraints, and both witness transformations; preserve the positive/negative and vacuity fixtures already required.
- Keep the offline dossier demonstrably illustrative. Reusing M0 evidence must not migrate legacy scientific status or imply novelty.
- Treat isolation, retry suppression, budget enforcement, and publication recovery as unverified until the specified boundary and crash tests pass.
- The reordered plan correctly places the dossier and semantic contract ahead of more A4 runs, then separates proof acceptance, the Pi boundary spike, durability, and an authorized scientific campaign (Spec:318–322). The Briefing communicates the same sequence (Briefing:77–81).

The architecture is suitable to accept as a proposed direction and bounded next-step specification, not as authorization for live activation or scientific attestation.

Merge verdict: OK
