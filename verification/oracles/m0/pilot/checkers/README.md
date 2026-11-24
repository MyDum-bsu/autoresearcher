# Independent finite Bellman check (P2a)

This offline, standard-library checker uses exact `fractions.Fraction` arithmetic
for the two-period finite game documented in `../baseline/README.md`:

```
x1 = a + k*p
x2 = x1 + b + q
cost = abs(x2)
```

It reads the supplied complete paths `(p,q)` without adding missing pairs.
An optional closed terminal interval is a hard constraint on every path.
First and second actions belong to the supplied finite sets `A0` and `A1`.

## Independent mathematical route

For each fixed first action `a`, group complete paths by the information
available when choosing `b`:

- `open`: a single cell, key `open`;
- `state`: the exact measured `x1`, pooling all paths with that state;
- `prefix`: the exact prefix `p`.

For a reachable cell `C`, retain only second actions satisfying the terminal
interval for **all** paths in `C`, and compute

```
v(a,C) = min_b max_(p,q in C) abs(a + k*p + b + q).
V(a)   = max_C v(a,C).
V      = min_a V(a).
```

The cell choices are independent once `a` is fixed. Every full feasible policy
has cell cost at least `v(a,C)` in each cell, hence worst cost at least `V(a)`.
Choosing a minimizing action in each cell attains `V(a)`. A first action is
infeasible if any reachable cell has no action covering every path. The game is
infeasible only if every first action is infeasible. No numerical infinity or
zero represents infeasibility.

In particular, `k=0` pools all prefixes into one state cell. The state route
cannot use a separate second action for each hidden prefix. Correlated suffixes
remain attached to their original complete paths even within pooled cells.

P1 enumerates complete policies. P2a minimizes each cell separately and never
enumerates the Cartesian product of cell actions. P2a selects the smallest
minimizing cell action and the smallest minimizing first action. Its optimal
policy can differ from P1's full-policy lexicographic tie witness at non-binding
cells. Tests compare exact values and replay each feasible P1 witness, allowing
different optimal policies. `nonbinding_ties` explicitly tests this difference.

## Independence boundary

`finite_bellman.py` does not import or read P1 code. This module independently
implements input validation, normalization, observation grouping, Bellman
optimization and witness replay. No P1 numerical, transition, solve, replay, cell or outcome
helper is shared. Only the documented schema and canonical JSON/hash contract
are common. The tests import P1's public `solve` to compare routes.

The public witness checker directly propagates every complete path and derives
its observable key separately from Bellman grouping. It checks one allowed
second action per reachable cell, no missing/extra/duplicate/unsorted cells,
allowed first actions, the hard terminal interval and exact ordered per-path
`path`, `x1`, `x2`, `cost` fields. It also checks schema, instance ID, information
mode, normalized-input hash, claimed worst cost and result shape. Relabeling a
prefix certificate as state does not authorize hidden-prefix actions.

This is implementation-route independence, not an independent specification,
formal proof, external scientific reference or approved scientific judge.
Both routes implement the same small finite game in Python using Fraction.
Shared schema misunderstandings and common language/arithmetic defects remain
possible. SHA-256 binds the normalized input; it is not a signature or proof.

## API and encoding

- `validate_instance(dictionary)`: independent validation and normalization;
  does not mutate the input.
- `parse_instance(json_text)`: also rejects duplicate JSON keys, noninteger JSON
  numbers and nonfinite constants. Use this at a JSON boundary; dictionaries
  cannot preserve duplicate keys.
- `solve(dictionary, information)`: returns a P1-schema record with `optimal`
  and an exact value/policy/outcomes, or typed `infeasible` with null value and
  first action and empty policy/outcomes arrays.
- `check_witness(dictionary, information, witness)`: returns the recomputed
  feasible record or raises `CheckerError`. It checks the `optimal` label as
  syntax only; **replay does not prove optimality**. It rejects infeasibility
  records because they have no feasible witness to replay.
- `check_result(dictionary, information, result)`: also computes the independent
  Bellman optimum and checks the value or the entire typed infeasibility record.
  This is the API for checking an optimality/infeasibility claim.

The exact input fields, rational encoding and output fields match P1's README.
Canonical rationals are reduced ASCII `n/d`, with positive denominator, zero
`0/1`, no plus sign, whitespace or leading zeroes. Arrays encode nonempty sets;
duplicates are errors, and normalization sorts numerically. `schema_version`
must be integer `1`, not a boolean. Missing or unknown fields are rejected.

Scope limits: at most 5 first actions, 5 second actions, 8 complete paths; input
rational absolute numerators and denominators are at most 1000. Computed
rationals are not clipped to those input limits. Python integer parsing limits
can reject exceptionally long forged output numbers explicitly.
`CheckerError.code` distinguishes `invalid_input`, `unsupported_scope` and
`invalid_witness`. Out-of-scope input is an error, never infeasibility. Checks
use explicit exceptions and remain active under Python `-O`.

The normalized input hash is SHA-256 over UTF-8 bytes of
`json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
allow_nan=False)`, without a newline. Instance ID participates; information mode
is bound separately by result metadata. CLI output uses this canonical encoding
and exactly one trailing newline, with no paths, timestamps or timing fields.

## Commands and frozen regression coverage

Run from `<workspace>/aro-discovery-baseline`:

```sh
python3 pilot/checkers/finite_bellman.py --input FILE --information state
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -O -m unittest discover -s pilot/checkers -p 'test_finite_*.py'
```

CLI exit 0 includes typed infeasibility. Invalid/unsupported input and file or
encoding errors produce stderr diagnostics and exit 2 with empty stdout.
Unexpected internal errors propagate; there are no retries or fallback results.
Importing the checker performs no computation or file writes.

The four public fixtures test the following exact triples `(open,state,prefix)`:

| Fixture | Values |
| --- | --- |
| `strict_gain` | `(1,0,0)` |
| `correlated_hidden` | `(1,1,0)` |
| `independent_hidden` | `(1,1,1)` |
| `terminal_feasibility` | `(infeasible,0,0)` |

Before the first test run, `test_finite_bellman.py` freezes a Cartesian product
of 3 gains, 3 first-action menus, 4 complete-path families and 4 terminal-interval
choices: **144 generated instances, 432 mode cases**, beyond the public 4
instances/12 mode cases. The gain set is `{-1/2,0,2/3}`. The first-action menus
include nonzero and noninteger actions; the paths include correlated,
anticorrelated, independent and branching suffixes. Terminal choices include
no interval, `[0,0]`, `[-1/2,5/6]` and `[1/3,4/3]`. Every feasible P1 result is
independently replayed, and every claimed value/infeasibility is compared with
Bellman. No adaptive search or parameter changes occur during testing.

Additional tests cover exact noninteger results, computed values above input
limits, set-order normalization, first-action and non-binding cell ties,
malformed inputs, metadata/outcome/policy tampering and false infeasibility.
Mutation certificates exercise lost prefix correlation, prefix substituted for
state and a missing terminal constraint without editing P1. A feasible but
suboptimal certificate demonstrates the difference between `check_witness`
and `check_result`.

CLI tests compare bytes across two ordinary processes and one `-O` process for
all 12 public mode cases, including infeasibility, and check canonical encoding
and one newline. They use Linux `/dev/stdin` as the input file, write no fixture
artifacts, and bound each subprocess to 5 seconds. The suite commands have a
60-second timeout at this frozen scale. This is a software regression set, not
a general scientific evidence grid, held-out scientific benchmark or claim of
coverage of all finite inputs.

## Limits

With `F` first actions, `S` second actions and `P` paths, Bellman numerical work
is `O(F*S*P)` plus sorting/validation and exact-integer arithmetic costs. Storage
is linear in paths and cells. The comparison suite also runs P1's exponential
full-policy enumerator on deliberately small cases; no worst-cap P1 runtime
bound is asserted.

There is no persistent runtime, continuous A4 solver, discretization error
bound, literature claim, theorem proof or scientific status transition here.
Nothing updates the journal, tracker, configuration or corpus. Continuous
controls, continuous disturbances, extra observations and the continuous A4
one-measurement optimum are outside this check.
