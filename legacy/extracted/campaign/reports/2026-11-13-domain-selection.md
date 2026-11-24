# Phase C: source-grounded question selection

Task: aro-discovery-k4t. Disposition: completed phase-C packet, safe for the two bounded public investigations. Scientific novelty and correctness of a new result are not established. No new scientific theorem/construction has been evaluated in C.

## Delivered decision

Select ONE question: `correlated-continuation-compatibility-v1`, stated in `research/question.md`. It asks for the residual-constraint boundary between disturbance-prefix policies and policies using one exact state measurement, including a dynamics-realizable test of pairwise versus joint continuation compatibility. This is a boundary/reconstruction objective, not a claim of a newly discovered open problem. Q2 was not opened.

The source-reading result that motivates it is precise: A3/A4 give state-indexed block programs with pointwise block disturbance availability; BT04/GTW20 give adjustable recourse indexed by revealed uncertain data. Neither displayed result automatically supplies equality with the smaller state information class under arbitrary correlated complete paths. The proposed upstream factorization statement ALREADY imposes observation consistency and therefore does not answer this question.

Primary deliverables:

- `research/domain-packet.md`: exact source-premise map, 6-source reading scope, layout limitations, dependency closure, negative knowledge and local-evidence boundary.
- `research/question.md`: rational matrix model, complete-path correlations, timing, policy signatures, hard terminal constraints, signed minimax bound, quantifiers, computational caps, expected result and candidate-specific exact certificate route.
- `research/closest-results.md`: row-by-row comparison with A2/A3/A4, BT04 Thms 2.1/2.2, GTW20 Prop. 1/Example 1, GTW25 Thm 1 and the unapproved proposed statement.
- `research/resource-manifest.json`: final manifest version 2; the same frozen question/source/tool pool, permissions and resource envelope for both attempts.

The common pool contains six byte-identical original PDF copies, selected layout extracts, seven inspected page renderings, bounding-box extracts for those renderings, an anchor catalog and a verbatim copy of the upstream proposed statement. Original sources and all siblings remain read-only. No reference solution from either future attempt exists in this pool.

## Identity and fairness freeze

Question SHA-256: `6e6bbaff0d752c3bfe7e2f9ee78b3135e689e437e012730f4c482c3a31f786dc`.

Final resource-manifest SHA-256: `1ff15746b0a2c8c47499cefdeca9dc2fc6b95c92ef536ce2e9259d7b542373d8`.

Before either attempt, a disclosed metadata-only amendment added executable byte identities. The original manifest is preserved as `research/resource-manifest-v1.json`, SHA-256 `63447143a2b9dc6e9f7b4b08c144ac85be94374c030a6221fa26ba8e2447bb13`. `research/tool-identities.json` binds executable/launcher bytes, SHA-256 `d712d082503770c00e55a50975a980e470dba84eb8606ab111f90b5e2ec109d1`. Question, sources, permissions and limits did not change. These identities do not constitute full dependency or sandbox verification.

Both attempts get 90 minutes, 60 total tool invocations including nested calls, maximum 3 active branches and the same source/tool access. No new sources, shared evaluator changes, installations or reading the other attempt/answer phase. Candidate-specific exact code is permitted only in the author's own attempt directory. Filesystem separation is instructional, not isolation or blinding. The experiment supports descriptive comparison, not a causal/statistical efficacy claim.

## Observed verification

Executed in the absolute campaign worktree, with inherited campaign-local TMPDIR/TMP/TEMP and PYTHONDONTWRITEBYTECODE=1:

1. PDF preparation: `timeout 60 python3 -B` inline copy/extraction driver called `pdftotext -layout` and `pdfinfo` for exactly 6 PDFs. SHA-256 equality of each copy to its original was checked before use. Selected pages were persisted separately. Render preparation used `pdftotext -f PAGE -l PAGE -bbox-layout` and `pdftoppm -f PAGE -l PAGE -singlefile -scale-to 1500 -png` for exactly 7 pages. No scientific solver ran.
2. `timeout 60 python3 -B` inline phase-C integrity check: exit 0, 75 frozen common-file hashes checked, 6 original/copy PDF pairs checked, 21 literal excerpts found on their declared physical PDF pages, root/branch checked, UTF-8/final-newline/trailing-whitespace checks passed for the four main packet artifacts. Persisted result: `research/phase-c-verification.json`.
3. `python3 -B ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py --language en FILE` for each of the three English packet documents: each exit 0, `No findings.` Raw stdout/stderr and argv are in `research/phase-c-style.txt`. Style checks say nothing about mathematical truth.

A first unique-phrase anchor-extraction command exited 1 with `Nonunique anchor BT04-information: [5, 11]`. It had not written its planned catalog; partial excerpt files were preserved. The invocation was not retried. The final catalog was authored as physical PDF/page anchors to already available full page context, without a uniqueness claim. The observation is retained in `research/sources/preparation-observation.json`; the independent packet-integrity check subsequently verified literal membership on declared pages. This was a bookkeeping failure, not a scientific refutation or a reason to substitute architecture prose for research.

The final delivery inventory and terminal file-hygiene observation are written separately after this report; they do not change the frozen question/source/tool pool. They are metadata evidence, not mathematical evaluators.

## Limits, legacy mismatch and omitted work

- No scientific search, exact new separating construction, Lean proof of Q1, matrix optimality result, human correspondence approval, novelty verdict or attestation is claimed. Those are not phase-C deliverables. Existing B finite controls were read, not re-executed, and remain scoped to finite scalar absolute-cost games.
- No comprehensive external novelty search was run. The six read originals support the declared reconstruction target; their silence cannot establish an open problem. No additional source was needed to define this target, and the frozen attempts cannot privately enrich their pool.
- A2 extraction loses some bars/negations. Only its clear measurement/signature comparison is used; detailed algebraic transfer is withheld. Source copies are available for direct inspection.
- The glossary's specialized L1/A=I bridge class is not the general A4 Eq. (1.1) and terminal-linear model actually read. This inherited mismatch is reported, not fixed. The new question explicitly defines its own symbols and source mapping.
- Comparator remains blocked by B's observed bwrap uid-map permission denial; native semantic controls did not run. No bypass or claim that compilation establishes source correspondence. TLC is protocol-model evidence only.
- No broad repository tests, terminal campaign validator or new mathematical check ran: this phase delivered documents/provenance, not changed scientific code. No private trials, tracker/live state/glossary/corpus/config writes, nested agents, provider changes, installs, commits or pushes.

## Resources and next operation

Preparation comprises six source copies/layout extractions, seven page renders, local source/README reading and packet synthesis. This cost belongs to C, not either paired attempt. Python 3.12.3, Lean 4.35.0-rc2 and Poppler 24.02.0 were observed with local version commands; executable/launcher identities are recorded separately. Provider billing, effective reasoning setting and native retry behavior are unknown. Exact dispatch time was not instrumented; source-copy creation and verification timestamps are persisted and are not represented as total worker runtime. The instructional call ceiling includes wrappers/nested calls; final count is to be reported in terminal delivery evidence.

Recommended next step: dispatch D1 and then D2 with the final frozen manifest and question, not merely the task title. A useful first action is to derive the actual prefix-conditioned residual inequalities and freeze one candidate-specific compatibility test with explicit feasible and rejection controls. No success outcome is prescribed. Safe continuation means sufficient anchored material and an available exact route for that bounded investigation; it does not mean LLM approval of science.
