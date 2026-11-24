# G2 independent engineering review

The selected engineering checks found no remaining instance of the original P1 shared-output rehash bypass in G1. The actual complete G1 index passes the checker in normal and optimized Python. The immutable historical terminal validator still rejects its original index. These observations provide engineering evidence only; they do not establish scientific correctness, novelty, a general Lean proof, goal completion or human attestation.

The first reviewer-created shadow omitted the historical index and caused four G1 test setup errors in each mode. Those failures remain in the raw evidence. A separate follow-up supplied the missing historical file without changing G1 code; all four regressions then passed in each mode.

## Scope and inspected implementation

Worktree: `<workspace>/aro-discovery-campaign`; branch: `task/aro-discovery-k4t-campaign`. Root and branch were checked before writes. All persistent G2 files are under `artifacts/goal/wave-1/engineering-review/`. No source, author output, original campaign artifact, G1 gate or G1 index was changed.

Read the complete first-success goal specification, FOUNDATION and AGENTS, the required historical handoff/outcome material, G1 plan/report and all four G1 Python files. Inspected the original P1 description in `artifacts/campaign/phases/12-final-review.json` and the corresponding parent validator and test fixture.

Relevant implementation boundaries:

- `scripts/campaign_acceptance.py:232-247` binds expected output paths but does not compare each original B `outputs[].sha256` with actual output bytes. Its `:473-480` check compares normalized hashes with current bytes. This is why consistent rehashing can evade the parent.
- `goal/engineering/checker_v1.py:35-63` adds actual-byte, file-table and normalized-check binding to the original B output references. `:17-32` pins and checks the historical inventory and its index membership. `:75-79` combines these checks in the actual entrypoint.
- `goal/engineering/assemble_v1.py:51-57` retains historical file identities and excludes the immutable parent index from the new file table to respect the parent's self-hash rule. That historical index remains indirectly bound by the pinned inventory. The new index contains all 13 existing campaign phase records.
- `goal/engineering/replay.py:35-39`, `:58-64`, and `:148-174` reset the gate, check historical identities, execute validation and derive the final gate. Running this author entrypoint would write G1 artifacts. G2 therefore did not invoke it or the writing assembler.

## Independently executed checks

Commands used to produce the new observations:

```sh
cd <workspace>/aro-discovery-campaign
timeout 300 python3 -B artifacts/goal/wave-1/engineering-review/replay_review.py
timeout 180 python3 -B artifacts/goal/wave-1/engineering-review/followup_complete_fixture.py
timeout 20 python3 -B artifacts/goal/wave-1/engineering-review/assess_observations.py
```

`executed-checks.json` records the initial 15 subprocesses, including the two reviewer fixture failures. `followup-executed-checks.json` records six separately identified executions with the corrected fixture. Every recorded process has new stdout/stderr files and their SHA-256 identities. Timeouts are bounded; no process was left running.

The unit tests ran on byte-identical copies of the relevant sources in disposable shadows inside the G2 directory. This preserves the unchanged fixture's required `artifacts/campaign/tmp` layout while keeping its writes inside G2. `TMPDIR`, `TMP`, `TEMP` and explicit Python/Ruff caches pointed inside those shadows; Python used `-B`. Both shadow directories were removed after execution.

Observed results:

- In each of normal and `-O`: 34 campaign tests, 7 baseline tests and 16 finite-checker tests passed in the initial shadow. In the corrected shadow, the 4 G1 frozen-output regressions passed. Total successful suite coverage is 61 tests per mode; the initial eight setup errors remain separately recorded and are not relabeled as successful executions.
- Actual worktree `python3 [-O] -B goal/engineering/checker_v1.py`: exit 0, `errors: []`. The corrected shadow's complete checker also returned exit 0 in both modes.
- Ruff check and format check on exactly the four G1 Python files: exit 0; `All checks passed!` and `4 files already formatted`. Their full argv and raw streams are recorded.
- Actual `python3 -B scripts/campaign_acceptance.py`: exit 1 with `unbound present file: artifacts/campaign/phases/01-plan.json`. This expected historical failure was preserved.
- `assessment.json`: `all_observed_conditions_hold: true`. This evaluates the recorded positive/negative observations, test counts, actual checker output, phase count, cleanup and source identity checks. It does not hide the initial fixture errors or issue a scientific verdict.

The actual new index has 413 file records, 56 checks, 8 stages, 6 sources, 3 claims and 4 review records. All 13 original phase paths are listed in `assessment.json`. The historical inventory still covers 389 files. The 424 source/input identities snapshotted by G2 are unchanged before/after, including G1 source and author outputs. The indirectly bound historical index was checked separately in the corrected fixture and remained unchanged in the actual worktree.

## Decisive original P1 reproduction

The independent probes use the COMPLETE repaired index and active original contract, not a reduced synthetic positive bundle. The mutation occurs only in the G2 shadow.

Positive baseline: parent validation, G1 validation and historical inventory checks all return empty error lists in the corrected fixture. The restored positive bundle does so again after controls.

Mutation: append `G2 independently fabricated shared-output mutation` to `artifacts/campaign/tool-spike/lean-precontrol-build.stdout`; update its size/hash in the file table and its normalized output hashes in all four consuming checks:

- `lean-precontrol-build`
- `sem-satisfiable-premises`
- `sem-false-conclusion`
- `sem-infeasible-instance`

Original stdout SHA-256: `5527355068512c8187bd0cb3d5d9a3d81b517be20edac170461acb522a7da939`.
Mutated stdout SHA-256: `9d5bfb6e4802e0e75f94bd3aa2e5abc586b2a9db7b6a07044a9c8eba5d96bb10`.
The original `tool-readiness.json` bytes remain unchanged.

In both normal and `-O`, the parent returns `[]` on this mutated complete bundle. G1 returns `EvidenceError: original frozen B output drift: lean-precontrol-build: artifacts/campaign/tool-spike/lean-precontrol-build.stdout`. Its pinned historical checks also report the tampering. This directly reproduces the parent bypass and demonstrates rejection by the new binding.

## Missing/invalid evidence controls

Each mode records 13 probe observations: two complete positive observations, the consistent-rehash exploit, and ten additional controls. G1 rejects all ten:

1. Missing shared raw-output file.
2. Un-rehashed corruption of that file.
3. Removed `01-plan.json` file-table entry.
4. Removed frozen B manifest entry.
5. Removed D1 exact-output entry.
6. Removed original `sem-false-conclusion` check.
7. Invalid normalized output hash.
8. Invalid claim statement hash.
9. Forbidden scientific attestation flag.
10. Missing mandatory D1 stage.

Exact diagnostics, changed check IDs and original/mutated hashes are in `G2-followup-normal-independent-full-bundle-complete-fixture.stdout` and its optimized counterpart. This is a focused fault matrix, not an exhaustive security proof.

## Reviewer fixture failure and correction

`replay_review.py:109-116` initially copied the repaired file table plus G1 files and configuration. Because the parent forbids its own index in that table, this copy omitted `artifacts/campaign/evidence-index.json`. G1 regressions read that historical index explicitly and failed with `FileNotFoundError` in setup. The initial independent probes also reported historical drift for that missing file. These are G2 setup failures, not evidence of a G1 product defect.

`followup_complete_fixture.py:20-21` explicitly includes that indirectly bound historical file. Its new execution IDs preserve rather than overwrite all initial observations. The corrected full positive bundle has no historical errors. No author source change, provider retry, provider fallback or unchanged failed scientific attempt was performed.

## Findings, limits and next action

No remaining engineering blocker was reproduced within this review's declared checks. The historical terminal failure, unavailable historical F raw streams, comparator uid-map blocker, Astra quality failures and unproved general claims remain historical facts. G1's new executions must not be presented as the missing historical F streams, an independent mathematical algorithm or G2 scientific verification.

Two oversized documentation-read batches in this G2 session caused harness-managed spills at `/tmp/pi-codemode-18d61d28d2345c2f.txt` and `/tmp/pi-codemode-afb2dda418a35537.txt`. Those paths were not read or removed. G2 subprocess scratch stayed local; full host-write containment is not established.

Not run: the writing G1 replay/assembler, comparator, TLC, Lean, new literature research, new scientific derivations, attestation or live scientific updates. No commits, pushes, installs, system changes, nested agents/workflows or tracker writes occurred. Ripwire indexing/merge gates were not run: this task reviews untracked G1 files and permits writes only in G2 evidence, rather than a tracked merge diff or repository-index update. Focused executable tests and lint provide the stated engineering observations. Native provider retry behavior and actual billing remain unknown.

Recommendation: the coordinator can use these persisted observations for the engineering checkpoint and proceed to the separately scoped source audit. The overall goal remains unachieved; no scientific verdict is supplied.
