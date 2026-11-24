# Independent public-episode review

Task: `aro-discovery-tu3`. Reviewer run `655368af-54b5-482d-8e1a-a53781796290` completed read-only, following owner-authorized retry of run `02627054-35e6-45b2-a230-0a71660474aa`, which failed at the provider usage limit without a verdict. This persisted report summarizes the returned review; mathematical/scientific attestation is not granted.

## Mandatory finding: P2, fail-open validation inventory

Original locations: `pilot/episodes/validate.py:10–18`, `pilot/episodes/tests/test_episodes.py:145–148`.

Reference and control discovery uses `glob('*.json')` without checking the expected inventory. Missing files silently reduce checks. The reviewer reproduced these cases by mocking discovery in memory, without changing files:

| Missing material | Observed result |
|---|---|
| All references and controls | Successful summary, zero references and zero controls |
| `P-reference.json` only | Successful summary, seven references and five controls |
| All controls | Successful summary, eight references and zero controls |

Reproduction from the task worktree:

```python
from pathlib import Path
from unittest.mock import patch
from pilot.episodes import validate
with patch.object(Path, 'glob', return_value=()):
    validate.main()
```

Empty reference discovery also bypasses the `judge.integrity()` calls made through individual evaluations. This is a package-completeness defect, not an observed false acceptance of a submitted invalid proof.

Required repair: validate the exact eight-reference/five-control inventory before judging; bind reference contents to the expected family; run integrity independently. Regressions must cover missing files in either inventory, empty/missing directories, and the wrong family under an expected filename. Incomplete packages must fail rather than print a reduced successful summary.

## Other reviewed behavior

No other mandatory substantive defect was established in the inspected scope.

M/F: independently checked enumeration/Bellman agreement and cross-replay on three cases in three modes. State/prefix values: hidden 1/0, shift 1/0, injective 0/0; open-loop is 1 in all cases. Actual observation fibers, immutable parent refutation and finite-only child scope are checked. Valid alternative first actions and a distinct fixed counterexample are accepted.

P: both fixed-target proof bodies compiled; transitive axioms were `Classical.choice`, `Quot.sound`, `propext`. `trivial`, self-reference, `sorry`, wrong target and unsupported-axiom declaration rejected. The reviewer found no accepted target substitution, circular dependency or candidate-controlled authority. The restricted grammar is not a hostile-execution sandbox or project release gate.

R: exact action/consequence tokens are explicitly declared by the public contract; two different action/obligation relations are accepted. This is a narrow interface, not an implicit preferred-prose matcher. However, the first stage already contains the child evidence repeated in the second stage. Fresh processes replay a prepared packet; no successor worker performs a new step. Public packets can be copied. Therefore these checks establish static decision/continuation relations only, NOT adaptation to newly arriving evidence, autonomous research choice, or successful continuation by another worker. Stronger R evaluation needs a separately authorized scenario and checkable successor outcome.

The reviewer ran 2,513 one-field structural mutations of M/F/R submissions, all rejected through `Rejected` or `CheckerError`, with no unexpected acceptance or unhandled exception in that bounded set. This is not exhaustive fuzzing. Vendored modules and source-snapshot identity matched provenance. No source or tracker edits were performed; temporary Lean scratch was cleaned.

Full unittest normal/optimized runs, Ruff and separate fresh-process comparison were not repeated by the reviewer; coordinator results are recorded separately. The coordinator's observed 76 Ruff findings also require repair but are not represented as independent reviewer findings.

## Disposition

Request changes for inventory validation and regression coverage. Preserve the R scope limitation explicitly. After repair, rerun focused acceptance. Human correspondence, scientific statuses, capability scores and benchmark trials remain unawarded.
