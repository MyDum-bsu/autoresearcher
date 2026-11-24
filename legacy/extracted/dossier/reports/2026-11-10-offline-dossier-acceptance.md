# Offline dossier: coordinator acceptance

Task: `aro-discovery-hg0`. Scope: the bounded offline software slice, not scientific capability or theorem acceptance.

## Result

The coordinator accepts the repaired offline implementation against its written engineering contract. Independent read-only reviewer `3724aa0a-92d5-4ccc-93e9-2252ea40019f` completed on OpenAI Sol high and returned:

> No issues found.
>
> Merge verdict: OK

This wording does not authorize commits, merging, live activation, scientific attestation or a proof claim. No such operations were performed.

## Observed repair history

Initial implementation passed its 17-test suite, but the coordinator reproduced two defects: changing a case's mathematical data and regenerating valid certificates left the claim identity unchanged; a multiline claim ID injected an apparent attestation heading into Markdown. Thus the initial green tests were not sufficient acceptance.

The first reviewer `78ca474b-4a55-4b09-8fce-189573327f66` failed with `Connection error` and supplied no final verdict. After explicit owner authorization to resume, repair worker `0d5a1d26-7ae0-4839-bf8e-10272b7bdffd` produced test-first fixes. Its report retains the red/green results. The new schema binds normalized input identities inside immutable case records and the claim digest; identifiers and references follow a strict ASCII grammar. The coordinator inspected those checks and independently reran the tests below.

## Coordinator verification

From `<workspace>/aro-discovery-dossier`, with `PYTHONDONTWRITEBYTECODE=1` on Python commands:

- `timeout 120 python3 -m unittest discover -s pilot/science/tests -p 'test_*.py'`: **22 tests OK**.
- The same command with `python3 -O`: **22 tests OK**.
- `timeout 60 python3 -m unittest discover -s pilot/baseline -p 'test_finite_*.py'`: **7 tests OK**.
- `timeout 60 python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'`: **16 tests OK**.
- `ruff check --no-cache pilot`: passed.
- `ruff format --no-cache --check pilot/science`: six files already formatted.
- `git diff --check`: passed; files remain untracked, so this alone is not whitespace coverage of new files.

The science suite includes frozen baseline identities, wrong-scope and regenerated-certificate mutations, identifier-injection regressions, normal/-O checks, deterministic fresh-process exports and file-content inventory around export. These are software acceptance checks on public fixtures, not private research-capability evaluations.

## Boundaries and remaining work

The module supports the declared finite state/prefix comparison and offline dossier only. It is not a general hypothesis engine, durable scheduler or authorization service. The separate correspondence statement is proposed and awaits human semantic review; no Lean build or proof attempt occurred. Novelty and usefulness of scientific outcomes were not evaluated. The owner's new evaluation/domain-architecture request is tracked separately as `aro-discovery-i24`.

Actual provider billing is unknown. No global settings, live journal/status, corpus, baseline files or configuration were changed. No commits or pushes. All deliverables remain in the feature worktree.
