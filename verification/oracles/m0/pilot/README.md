# M0: reproducible research baseline

This isolated baseline implements a two-period finite observation game and exact
open-loop certificates for A4 Example 1. It does not run an autonomous research
loop, write the scientific journal, change scientific statuses, or solve the
continuous one-measurement problem at r=80.

Run from the feature worktree root. Python 3.12 standard library is sufficient:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pilot/baseline -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pilot/checkers -p 'test_*.py'
```

The same two commands with `python3 -O` check that validation does not depend on
removable assertions. There are 7 reference tests and 29 checker tests. Finite
cross-checking includes 144 frozen generated instances in three information modes,
in addition to the four public cases. These are software regressions, not a proof
for continuous controls or a general scientific grid.

## Results and their scope

| Finite fixture | Open loop | State measurement | Disturbance prefix |
|---|---:|---:|---:|
| strict_gain | 1 | 0 | 0 |
| correlated_hidden_disturbance | 1 | 1 | 0 |
| independent_hidden_disturbance | 1 | 1 | 1 |
| terminal_feasibility | infeasible | 0 | 0 |

The reference enumerates complete policies. The independent checker minimizes
within observation cells and replays proposed policies without importing the
reference's mathematical functions. A controller observing the state cannot use
a hidden disturbance prefix to select different actions at the same state.

| A4 coefficient set | Guaranteed reward (12 decimal display) | Exact primal/dual gap |
|---|---:|---:|
| Literal printed coefficients | 1.495710098124 | 0 |
| Reconstructed decimal coefficients | 1.501101989382 | 0 |

The second number rounds to the paper's 1.501102, but these reconstructed decimals
are not confirmed author inputs or exact trigonometric coefficients. Both results
apply to open-loop controls and the full independent continuous disturbance box.
They do not establish the value of a policy with a measurement. The generator
uses forward-power columns; the independent checker uses backward adjoints and
chronological forward control replay, robust terminal bounds and a dual bound.

## Inspect and reproduce

Finite output:

```sh
python3 pilot/baseline/finite_reference.py --public-fixtures
```

The output contains rational values and full policy witnesses. Input and API
contracts are in [baseline/README.md](baseline/README.md); independent checks are
in [checkers/README.md](checkers/README.md).

Check the saved A4 certificates without rerunning the optimizer:

```sh
python3 pilot/checkers/a4_check.py --input pilot/inputs/a4_printed.json --certificate artifacts/research-pilot-m0/a4_printed.certificate.json
python3 pilot/checkers/a4_check.py --input pilot/inputs/a4_reconstructed_decimal.json --certificate artifacts/research-pilot-m0/a4_reconstructed_decimal.certificate.json
```

Those commands emit exact, potentially long rational values. A zero process exit
and `certificate_validity: valid` mean the pinned numerical input/certificate
contract passed. The output explicitly says source-page verification is not
performed by the numeric checker. This is not human attestation.

To generate new certificates, send producer stdout to files in your own temporary
directory and pass those files to the checker:

```sh
python3 pilot/baseline/a4_certificate.py --input pilot/inputs/a4_printed.json
python3 pilot/baseline/a4_certificate.py --input pilot/inputs/a4_reconstructed_decimal.json
```

Full provenance, schemas and derivation of the dual bound are in
[baseline/A4-README.md](baseline/A4-README.md). Published source anchor: A4 PDF
page 12, Example 1; reconstruction also uses A2 PDF page 15 and A3 PDF pages 8–9.
No source-corpus registration was changed.

## Retained artifacts

`artifacts/research-pilot-m0/` contains:

- `finite-reference.json`: all public cases, complete-policy route.
- `finite-independent.json`: independent Bellman route; every reference result
  was also checked by independent witness/value verification.
- Two `*.certificate.json` files: chronological controls, exact objectives,
  supports and dual multipliers.
- Two `*.check.json` files: independently checked values and feasibility bounds.
- `manifest.json`: Python version and internal source/input/output fingerprints.

Fingerprints detect changed bytes; they do not prove a mathematical statement.
Repeated certificate generation/checking and finite CLI output were byte-identical.
The artifacts are offline evidence, not entries in the live scientific journal.

## Quality and limits

Repository Ruff checks apply without exemptions:

```sh
ruff check --no-cache pilot
ruff format --no-cache --check pilot/baseline/*.py pilot/checkers/*.py
```

An independent read-only review found a malformed-JSON decoder error; a test-first
fix now returns a typed error for oversized integers and excessive nesting.
The final tests cover tampered policies, wrong information classes, modified
coefficients, wrong dataset labels, invalid controls, false objectives and invalid
dual certificates. Evaluator-private holdouts, Lean and r=80 are not run.

Implementation and review history, Pi agent runs, accounting limitations and next
steps: [execution report](../reports/2026-11-10-baseline-execution.md).
