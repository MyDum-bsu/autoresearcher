# Public episodes: bounded engineering repair

Task: `aro-discovery-tu3`. Mandatory inventory repair and the coordinator's Ruff
findings are repaired. Final normal and optimized suites each pass 22 tests;
Ruff and format checks pass. Coordinator acceptance remains pending. No scientific
acceptance, status promotion, capability score or benchmark trial is awarded.

Worktree: `<workspace>/aro-discovery-episodes`.
Branch: `task/aro-discovery-tu3-public-episodes`, verified at entry and immediately
before the first write. All shell commands below ran after explicit
`cd <workspace>/aro-discovery-episodes`.

## Red before green

Added `pilot/episodes/tests/test_inventory.py` before changing the validator.
The exact regression command was:

```sh
PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -B -m unittest pilot.episodes.tests.test_inventory -v > artifacts/public-episodes-tu3/repair/inventory-red.txt 2>&1
```

Observed exit 1: **6 tests, 34 failures**, against the original implementation.
The retained log includes successful partial summaries from the original
fail-open validator. Missing individual files, empty inventories, unexpected
entries and family substitutions failed to raise. The independent integrity
sentinel also showed the original validator treating integrity failures as
negative-control rejections and emitting a partial success summary.

After repair, the same six-test module passes, with its output recorded separately
in `repair/inventory-green.txt`. The red artifact remains unchanged. During final
test review, the nonfile test was corrected to restore each fixture before moving
to the other inventory; the complete normal/optimized and targeted suites were
then rerun on that final test version.

## Decisions and files

- `pilot/episodes/validate.py`: evaluator-owned explicit mappings name exactly
  eight references and five controls and bind every filename to M/F/P/R. The
  validator checks both complete inventories and all family bindings before
  evaluating any submission. It rejects missing/unexpected entries (including
  non-JSON extras), missing/empty directories, nonfile expected entries and
  family-swapped contents. Completeness cannot be reduced by submission content.
- `judge.integrity()` runs first, independently of inventory discovery or
  individual submissions. Integrity and family-validation failures are outside
  the negative-control rejection handler. Errors propagate to a nonzero process
  exit; no summary is printed until every required check finishes.
- `pilot/episodes/tests/test_inventory.py`: every one of the 13 expected files
  is individually removed; both directory inventories are emptied and removed;
  both missing together, unexpected JSON/non-JSON entries, expected-name
  directories, all 13 filename/family substitutions and the independent integrity
  sentinel are covered. Fresh subprocess regressions remove `P-reference.json`
  and `M-wrong-information.json`: both must exit nonzero with empty stdout.
  Tests use disposable copies inside this worktree and remove them afterward.
- `pilot/episodes/author.py`, `judge.py`, `validate.py`,
  `tests/test_episodes.py`, `tests/test_inventory.py`: import ordering, unused
  import/argument, multi-statement lines, line wrapping and formatting repaired.
  `judge.py` only changes layout and the unused JSON callback parameter name;
  submission/CLI formats and existing rejection strings are retained.
- `pilot/episodes/README.md` and `tasks/R.md`: document the inventory boundary and
  precise R limitation. No R workflow or additional research capability was built.
- `artifacts/public-episodes-tu3/repair/`: new repair evidence. Existing author,
  reviewer and coordinator reports were not edited. Historical author evidence
  files were retained rather than overwritten with newer passing results.
- `artifacts/public-episodes-tu3/identities.json`: current evidence inventory;
  its original 32-entry version is preserved as
  `repair/identities-before-repair.json`. The current inventory covers package,
  historical evidence, repair evidence and this report, excluding itself.

No author regeneration was run. Both vendored modules, provenance metadata,
trusted inputs/Lean target, trusted identity file, all eight reference JSON files
and all five control JSON files retain their original identities. Lint policy
was not changed. No source checkout or sibling was edited; no agents, installs,
commits, pushes, tracker writes, provider/model changes, trials or live scientific
writes were performed.

## Exact final checks and observed results

Commands preserve Python's no-bytecode setting. Each script invocation has an
external timeout; subprocess regressions also have explicit subprocess timeouts.
Paths beginning `repair/` below are under `artifacts/public-episodes-tu3/`.

| Exact command | Result |
|---|---|
| `git rev-parse --show-toplevel && git rev-parse --abbrev-ref HEAD` | Expected absolute root and task branch, twice before editing. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -B -m unittest discover -s pilot/episodes/tests -v > artifacts/public-episodes-tu3/repair/tests-normal.txt 2>&1` | Exit 0; 22 tests, OK. Includes real Lean reference checks, stored invalid controls, per-family fresh CLI comparison and new inventory regressions. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -O -B -m unittest discover -s pilot/episodes/tests -v > artifacts/public-episodes-tu3/repair/tests-optimized.txt 2>&1` | Exit 0; 22 tests, OK. Completeness does not depend on Python assertions. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -B -m unittest pilot.episodes.tests.test_inventory -v > artifacts/public-episodes-tu3/repair/inventory-green.txt 2>&1` | Exit 0; 6 tests, OK. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B -m pilot.episodes.validate > artifacts/public-episodes-tu3/repair/validation-a.json` | Exit 0; 8 references pass, 5 negative controls reject. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -B -m pilot.episodes.validate > artifacts/public-episodes-tu3/repair/validation-b.json` | Exit 0; independent fresh process, same counts. |
| `cmp artifacts/public-episodes-tu3/repair/validation-a.json artifacts/public-episodes-tu3/repair/validation-b.json` | Exit 0; identical bytes. |
| `cmp artifacts/public-episodes-tu3/validation-a.json artifacts/public-episodes-tu3/repair/validation-a.json` | Exit 0; repaired valid output is identical to historical output. |
| `sha256sum artifacts/public-episodes-tu3/repair/validation-{a,b}.json` | Both `3d4500467520403fbb842b116d7df81aaacf32237b0c6b47471891a590de3181`. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 -B -c 'from pilot.episodes import judge; judge.integrity(); print("Integrity: PASS")'` | Exit 0; trusted inputs/target and both vendor identities pass. |
| `ruff check --no-cache pilot/episodes > artifacts/public-episodes-tu3/repair/ruff.txt` | Exit 0; All checks passed! No exclusions or policy changes. |
| `ruff format --no-cache --check pilot/episodes/author.py pilot/episodes/judge.py pilot/episodes/validate.py pilot/episodes/tests/test_episodes.py pilot/episodes/tests/test_inventory.py > artifacts/public-episodes-tu3/repair/format.txt` | Exit 0; 5 files already formatted. Vendor files intentionally not formatted. |
| `git diff --check` | Exit 0; tracked-diff check only (package files remain untracked). |
| `find pilot/episodes -type d \( -name '__pycache__' -o -name 'inventory-*' -o -name 'lean-*' \)` | Exit 0, no output: no retained bytecode or test/Lean scratch directories. |

An additional bounded inline `python3 -B` verification checked all 32 original
manifest entries against current bytes and rejected any changed entry outside
the six explicitly authorized pre-existing package files. It also ran integrity
and checked the 8/5 summary counts. Output is `repair/provenance.txt`: six allowed
changes; every historical evidence, reference, control and provenance entry
unchanged. New test/report/evidence identities are in the refreshed manifest.
Hashes establish byte identity, not mathematical or scientific authority.

The advisory prose command
`PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py reports/2026-11-13-public-episodes-repair.md --language en > artifacts/public-episodes-tu3/repair/style.txt`
exited 1 with two reviewed flags: passive wording about prohibited operations and
the required `Not run` boundary. Both preserve operational limits; no wording
change was needed. This advisory result is not reported as a passing gate.

### Historical and intermediate failures

The initial `ruff check --no-cache pilot/episodes` reproduced **76 findings** and
exit 1. A targeted `ruff check --no-cache --fix` fixed three import findings but
still exited 1 with 70 remaining findings after the inventory replacement and
callback rename; its chained format command therefore did not run. Running the
formatter separately left two findings (one long string and one nested context);
manual repairs cleared both. No gate was weakened. One attempted tool-batching
script had a JavaScript syntax error and made no tool calls or file changes.
These failures and the red regression result are history, not rewritten passes.
The coordinator's acceptance/review reports and author's historical checks remain
the coordinator's/author's records.

## Readiness and limits

The package is ready for the coordinator to repeat bounded engineering acceptance;
this worker does not grant acceptance. M/F retain finite certificate replay and
finite-only child semantics. P remains the fixed observation-factorization lemma
with pending human correspondence review, not the full correspondence theorem
or the project's formalized/release gate.

**R is static two-stage packet/evidence relation validation.** Stage 1's complete
F submission already includes the child evidence repeated at stage 2. A fresh
checker replays a prepared public packet; it is not a successor worker performing
a new step. No adaptation to newly arriving evidence, autonomous research choice
or actual continuation is measured. Plan relevance, source comparison, effort and
usefulness remain human-pending. Public packets can be copied. Stronger R evidence
requires a separately authorized scenario and checkable successor outcome.

Not run: full-repository lint/types/build, legacy Lean build, hostile-execution
isolation, private evaluation, scientific attestation, source admissions or
candidate trials. They are outside this bounded repair. No engineering blocker
was observed in the requested gates. Further acceptance and scientific authority
remain with the coordinator and human reviewer respectively.
