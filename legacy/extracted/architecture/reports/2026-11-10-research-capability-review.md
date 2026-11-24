# Research capability architecture: review and validation

Task: `aro-discovery-i24`. Documentation-only extension of the operating model. No capability benchmark or scientific experiment was run.

## Coordinator disposition

Independent reviewer `e52ae8bc-db2e-4b96-9477-42a8eba6da8a` completed on OpenAI Sol high. It found no architectural blocker, and reported a missing referenced `evaluation-plan.json`. The coordinator created that artifact during the review; its existence, JSON structure and arithmetic are checked before handoff. The report below preserves the reviewer's observation rather than rewriting it retrospectively. The missing-reference finding is resolved, not a waived gate.

The plan counts are proposals: four public development episodes, eight private episodes, two configurations and three attempts per private episode give 48 allocated private attempts. They are not measured capabilities, approved trial budgets or a reliability guarantee. The final execution requires separate authorization and validated privacy/budget boundaries.

Deliverables: `docs/specs/2026-11-10-research-capability-and-domain.md`, Russian brief `reports/briefings/2026-11-10-research-capability.md`, the linked main operating-model document, `artifacts/architecture-research/evaluation-plan.json` and PDF identities in `evaluation-sources.json`. Source PDFs were read outside the corpus; temporary downloads are cleaned after identity capture.

The repaired offline dossier is a different completed engineering task. Coordinator tests observed 22 normal/-O science tests, 7 reference tests and 16 checker tests passing, plus Ruff; its independent review found no issues. Those checks do not evaluate research competence. See the dossier worktree's `reports/2026-11-10-offline-dossier-acceptance.md`.

No live scientific state, corpus, configured thresholds, global glossary or model settings were changed. No commits or pushes. Actual provider billing remains unknown. Terminology and the evaluation protocol are design proposals; the documents do not confer scientific authority.

## Executed documentation checks

`lint_technical_style.py --language en docs/specs/2026-11-10-research-capability-and-domain.md` and the corresponding `--language ru` command on the owner brief returned no findings after three editorial fixes. A Python validation checked four documents for UTF-8/final newlines/trailing whitespace, the main-document reference, evaluation JSON status and counts (`4/8/2/3 -> 48`), and two PDF source identities. The first pass caught a Markdown hard-break space in the copied review; after normalizing that whitespace the rerun passed. `git diff --check` also passed; explicit text checks cover untracked files. The coordinator-owned temporary PDF cache was removed after recording identities. No scientific benchmark or runtime gate is claimed by these checks.

## Independent review (trailing Markdown whitespace normalized)

## Verdict

**No blocking architecture issues found.** The proposal answers the owner’s scientific-capability question rather than replacing it with safety tests. One documentation issue is confirmed below.

Reviewed: `<workspace>/aro-discovery-architecture/docs/specs/2026-11-10-research-capability-and-domain.md`, the companion scientific operating model, and `<workspace>/aro-discovery/FOUNDATION.md` and `docs/GLOSSARY.md`. No files, tasks or journal entries were changed; no network research, builds, experiments or subagents were used.

## Finding

**P2 — Referenced evaluation-plan artifact is missing.**
**Location:** `<workspace>/aro-discovery-architecture/docs/specs/2026-11-10-research-capability-and-domain.md:5`, introductory paragraph.

The document says the proposed pilot counts “are recorded in `artifacts/architecture-research/evaluation-plan.json`.” Reading that path in the architecture worktree returned `ENOENT`. This leaves a broken supporting reference and overstates the delivered evaluation package. It does **not** invalidate the arithmetic or protocol: §7 independently specifies eight private episodes × two configurations × three attempts = 48 allocated attempts.

**Minimal repair:** supply the referenced artifact before handoff, or describe it as proposed and identify §7 as the current record. No benchmark execution or live configuration change is needed.

## Assessment against the owner’s questions

- **Capability and usefulness:** §§2–3 distinguish mechanism integrity, domain research competence and project usefulness. M/F/P/R explicitly test modeling, falsification, proof/construction and research decisions. Algorithmic improvement and prospective novelty/usefulness receive separate evidence requirements. This is materially broader than false-acceptance testing.
- **Metrics and gaming:** §5 freezes denominators, retains agent failures and exhaustion, separates pending review, distinguishes answerable from abstention cases, requires positive controls, and prevents easy-instance pooling and node-splitting credit. Any-success and all-success are direct grouped diagnostics, not interchangeable reliability estimates.
- **Evaluation material and protocol:** §§3–4 and §7 distinguish public development templates from separately curated private episodes. Mechanism/source-family separation, exposure controls, fresh state, no cross-trial feedback and retirement after repair-guiding disclosure are explicit. I found no basis to claim that the public templates are being passed off as private tests.
- **Baseline fairness:** §6 gives B0 the same model, admissible sources, tools, permissions and resource caps, while allowing a genuine tool-using session. B1’s retrieval and helper work are accounted for. The combined comparison tests the package/protocol bundle; later ablations are correctly needed to attribute gains to individual mechanisms.
- **Authority and novelty:** Human source-based significance/novelty review remains distinct from code/Lean mathematical checking. LLM critique cannot award scientific verdicts. Historical reconstruction, project novelty and literature novelty are explicitly separated; failed search is not proof or priority evidence. This is consistent with FOUNDATION’s authority boundaries.
- **Domain architecture and terminology:** §§1 and 8–9 choose domain-specific research with reusable engineering, name the whole undertaking a **research system**, and specify definitions, anchored sources, scoped dependencies, proof/evidence libraries, procedural skills, tool contracts and reviewed memory. Their integration into bounded working sets is described, rather than reduced to a larger system prompt.

## Genuine limitations—not merge blockers

1. **The panel is diagnostic only.** Four public and eight private episodes, with 48 allocated private attempts, cannot establish broad reliability or discovery ability. The document explicitly says so; no sample-size defect is demonstrated merely by these proposed counts.
2. **Operational readiness remains unestablished.** Actual reference tasks, evaluator validity/privacy, enforced budgets, reset/isolation behavior and compatible formal tooling require the separately authorized verification described in the proposal.
3. **Usefulness remains prospective.** Neither improved benchmark acceptance nor successful proof integration alone establishes novelty, human time saved or meaningful contribution to the approved research program. Campaign dossiers and measured human effort are appropriately required.
4. **This was a local design review.** External source assertions and empirical claims about existing tools/dossiers were not independently reproduced. No benchmark performance, domain-package benefit or live readiness is certified here.

**Recommendation:** accept the proposed architecture with the missing-reference correction; keep implementation, diagnostic execution and scientific activation separately authorized.

Merge verdict: OK with notes
