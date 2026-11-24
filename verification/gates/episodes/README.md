# PUBLIC M/F/P/R development episodes

All tasks, references, controls and judges in this directory are PUBLIC. These
are evaluator-authoring fixtures, not a benchmark run, a private capability test,
a novelty result or an authorization to publish science. Objective checks do not
award scientific status. Human semantic and usefulness review remains pending.

## Reproduce offline

Run from the repository root, with Python bytecode disabled:

```sh
PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 -m pilot.episodes.author
PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -B -m unittest discover -s pilot/episodes/tests -v
PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -m pilot.episodes.validate
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m pilot.episodes.judge --input pilot/episodes/references/P-reference.json
```

The author command regenerates frozen public finite fixtures and negative controls;
it is an evaluator-maintenance command, NOT a candidate tool. A candidate receives
only an input submission path for `judge`, not replacement instances, target files,
checker paths or expected hashes. A real evaluation would need filesystem isolation;
this package does not enforce it. No arbitrary submitted Python is executed.
The trusted inputs, target and vendor identities must be frozen before attempts.
Candidate-supplied certificate hashes are recomputed against those trusted inputs.
`reference-identities.json` detects drift; it does not authenticate mathematical
meaning. `provenance.json` records two byte-identical imported finite modules;
no sibling path is imported at runtime, and no dossier schema was copied or changed.

Standalone `validate` requires the evaluator-owned exact eight-reference and
five-control inventory in `validate.py`, with filename-to-family bindings for
both sets. Missing or unexpected entries, absent/empty directories, nonfiles and
family substitutions fail before any success summary. Trusted integrity runs
independently before inventory checks; candidate contents cannot reduce coverage.

## Layout and minimal resources

| Family | Task-facing problem | Public reference | Minimal resources |
|---|---|---|---|
| M | `tasks/M.md` | `references/M-{reference,alternative}.json` | `trusted/inputs.json`, exact rational arithmetic, finite checker |
| F | `tasks/F.md` | `references/F-{reference,alternative}.json` | same finite inputs, enumerator and independent checker |
| P | `tasks/P.md` | `references/P-{reference,alternative}.json` | `trusted/target.lean.txt`, Lean 4.35.0-rc2 core/Lean standard library only |
| R | `tasks/R.md` | `references/R-{reference,alternative}.json` | finite inputs and F certificates, stage/continuation rules; source comparison remains an unexecuted obligation |

The advisory `logika` and `technical-style-editor` procedures inform authoring;
they are not judges. No literature fact is asserted by these constructed fixtures.
The checked artifact manifest in `artifacts/public-episodes-tu3/identities.json`
anchors their local evidence identities after validation. Independently authored
reference code (full policy enumeration) and checker code (cellwise Bellman
optimization plus replay) agree on these finite inputs. They are different
arithmetic routes, not independent human approval of the scientific model.

## Common finite model and quantifiers

This is a bounded M0-derived two-period model, NOT the continuous-control bridge.
For each complete path `(p,q)` from the frozen finite path set, set
`x1 = a + k*p`, `x2 = x1 + b + q`. Choose `a` once before either disturbance;
choose `b` after observation and before `q`. Minimize `max_path abs(x2)`, subject
to the frozen finite action sets and any hard terminal interval on every path.
A policy must assign one permitted second action to each reachable observation
cell. Thus the order is `min_a min_policy max_(p,q)` with policy nonanticipativity,
not `max_path min_b`. Complete paths may be correlated.

`state` observes only exact `x1`, `prefix` observes only `p`, and `open` observes
neither. Knowing `a` and `k` does not recover `p` when `k=0`.
A prefix assignment is state-implementable iff it agrees on every pair of paths
with equal `x1`. The finite input grammar is the unchanged vendor closed schema:
integer `schema_version=1`, nonempty finite rational action arrays (<=5 each),
1..8 unique rational path pairs, rational `prefix_gain`, optional terminal
interval; canonical reduced `n/d`, absolute numerator and denominator <=1000.
These limits do not define a general uncertainty-set solver.

Episode submissions are closed objects with integer (not bool) `schema_version=1`
and exact ASCII episode ID `M`, `F`, `P` or `R`. Duplicate keys, unknown fields,
noninteger numbers and unknown IDs reject. Claim IDs are fixed enumerated strings;
this deliberately avoids accepting user-defined scope prose as executable authority.
Full certificates use the vendor result schema (including exact outcomes and
normalized-input hash). The judge accepts ANY replayed optimal policy certificate,
not only the reference solver's canonical tie-break. Certificate policy cells
must use canonical sorted observation keys. JSON object key order is irrelevant.

## Feedback and review

The public judge returns `objective_checks=pass`, `human_review=pending` and
`scientific_status_change=false`, or exits 2 with `objective_checks=rejected` and
a reason. P includes its parsed transitive axiom list. Compiler diagnostics for
P are public feedback. No attempt limit is enforced: these are development tools,
not a hidden grading oracle. No capability rate or trial denominator is computed.

M/F finite relation checks are mechanically ready for independent acceptance.
P has a compiler-checked narrow reference but human statement correspondence is
pending. R checks only the explicit finite decision relations and durable packet;
its research relevance, adequacy of plans and source-comparison quality need human
review. Distinct actions are admitted, not ranked by similarity to a preferred plan.
Human rejection/uncertainty is not silently converted into machine acceptance.

R is static two-stage packet/evidence relation validation. The child evidence
shown at stage 2 is already present inside the complete F evidence at stage 1.
A fresh checker replays the prepared public packet; it is not a successor worker
performing a new research step. No adaptation to newly arriving evidence or
actual continuation is measured. Stronger R evaluation requires a separately
authorized scenario and a checkable successor outcome; this package does not
implement that workflow.

Lean uses a fixed trusted theorem template and restricted proof-body syntax,
not candidate Lean modules or imports. Version mismatch, compile failure, warning,
missing theorem report or nonallowlisted transitive axioms rejects. The positive
allowlist is `propext`, `Classical.choice`, `Quot.sound`. Temporary Lean files stay
inside this directory and are removed. This is not an OS sandbox for hostile
metaprogramming, nor the project's release/formalized-status gate. No mathlib,
legacy formalization, toolchain installation or full correspondence proof is used.
