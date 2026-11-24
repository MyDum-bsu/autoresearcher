# Exact finite observation reference (P1)

This offline Python 3.12 standard-library reference enumerates finite policies.
It is not an approved scientific judge and does not write project state.

## Model and scope

The scalar two-period game starts at `x0=0` and has
`x1=a+k*p`, `x2=x1+b+q`, with terminal cost `abs(x2)`.
The first action `a` is selected before `p`; the second action `b` is selected
before `q`. The controller minimizes the maximum cost over the supplied complete
paths `(p,q)`. Paths may be correlated; the reference never adds missing pairs.

Information modes determine the second-action cells:

- `open`: one common action, observation key `open`.
- `state`: one action per exact rational `x1`, pooling every path with that state.
- `prefix`: one action per exact rational `p`; this may reveal information absent
  from a state measurement.

An optional closed terminal interval must hold on every path. No feasible policy
produces the typed result `infeasible`, with null value/first action and empty
policy/outcomes arrays. It never produces a numerical zero or infinity instead.

For each first action, the reference enumerates every assignment of second
actions to reachable cells, propagates every complete path, rejects policies
violating the interval, and compares worst costs using `fractions.Fraction`.
Ties retain the smallest rational first action, then the lexicographically
smallest rational action tuple on numerically sorted cells. The single open
cell precedes no other cells.

This is a finite reference, not a continuous A4 result, an LP solver, a Bellman
implementation, a discretization error bound, or a theorem proof. Finite
optimality says nothing about continuous controls, continuous disturbances,
additional measurements, or the A4 one-measurement optimum.

## Input and pure API

An instance has exactly these fields:

```json
{"schema_version":1,"instance_id":"example","first_actions":["-1/1","0/1","1/1"],"second_actions":["-1/1","0/1","1/1"],"paths":[["-1/1","0/1"],["1/1","0/1"]],"prefix_gain":"1/1","terminal_interval":null}
```

`terminal_interval` may instead be `["lower_n/lower_d","upper_n/upper_d"]`.
Every rational is reduced `n/d`, denominator positive, no whitespace or plus
sign, zero exactly `0/1`. Numerators/denominators use ASCII decimal integers
without leading zeroes. Instance IDs are nonempty strings. Arrays represent
sets: duplicates are errors, and valid arrays normalize to numeric rational
order (paths lexicographically by `(p,q)`).

Limits: at most 5 first actions, 5 second actions, 8 paths, and every input
rational has absolute numerator at most 1000 and denominator at most 1000.
Overflow raises `ReferenceError` with `code="unsupported_scope"`, not mathematical
infeasibility. These are implementation limits, not mathematical assumptions.
Other schema, rational, information-mode and duplicate-key errors have
`code="invalid_input"`. Floats and booleans cannot stand in for rational strings
or the integer schema version. Missing/unknown fields are errors.

- `parse_instance(json_text)` rejects duplicate JSON keys/noninteger numbers and
  returns a normalized validated JSON-shaped dictionary.
- `validate_instance(dictionary)` validates and normalizes without mutating it.
  A dictionary cannot preserve duplicate JSON keys; use `parse_instance` at the
  JSON boundary.
- `solve(dictionary, information)` validates again and exhaustively minimizes.
- `replay(dictionary, information, witness)` checks a feasible, full result-shaped
  witness and returns its recomputed record. It rejects mode mismatch, incomplete
  or extra cells, duplicate/unsorted cells, disallowed actions, violated terminal
  constraints, and altered metadata, hash, exact value or outcomes. It does not
  enumerate alternatives and therefore certifies feasibility/value only. The
  supplied `optimal` label is checked as record syntax, not endorsed by replay.
  Infeasibility cannot be certified by replaying a feasible witness.

All computational functions are pure; importing the module runs no CLI and
performs no file writes.

## Output schema

A result contains `schema_version=1`, `instance_id`, `information`,
`normalized_input_sha256`, `result` (`optimal` or `infeasible`), `value`,
`first_action`, `policy`, and `outcomes`.
`policy` is an ordered array of `[observation_key, action]` pairs.
`outcomes` is an array of objects with `path`, `x1`, `x2`, `cost`, one per
normalized complete path. All numbers except the schema version are canonical
rational strings. Computed rationals are not clipped to the input limits.
`x1` is an additional diagnostic field exposing the measured state; it does not
change the witness's mathematical meaning.

The normalized hash is SHA-256 over UTF-8 JSON from
`json.dumps(normalized, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
allow_nan=False)`, with no newline. Instance ID participates; information mode
is a result field, not part of the input hash. CLI payloads use the same JSON
encoding followed by exactly one newline. They contain no paths or timestamps.
`--public-fixtures` emits `{"schema_version":1,"cases":{...}}`, mapping each public
case ID to all three mode results. It computes each result from the fixture
input; expected values exist only in the tests.

## Commands and verification

From the feature worktree root:

```sh
python3 -m unittest discover -s pilot/baseline -p 'test_*.py'
python3 -O -m unittest discover -s pilot/baseline -p 'test_*.py'
python3 pilot/baseline/finite_reference.py --public-fixtures
python3 pilot/baseline/finite_reference.py --input /path/to/instance.json --information state
```

CLI exit 0 means a valid finite computation, including infeasibility; exit 2
means invalid/unsupported input or an unreadable input file. Diagnostics go to
stderr, with no success artifact. Unexpected internal errors propagate to a
nonzero process exit rather than becoming mathematical results.

For deterministic comparison, use a newly created private temporary directory:

```sh
tmp=$(mktemp -d /tmp/p1-compare.XXXXXXXX)
python3 pilot/baseline/finite_reference.py --public-fixtures > "$tmp/first.json"
python3 pilot/baseline/finite_reference.py --public-fixtures > "$tmp/second.json"
cmp "$tmp/first.json" "$tmp/second.json"
sha256sum "$tmp/first.json"
rm "$tmp/first.json" "$tmp/second.json"
rmdir "$tmp"
```

Tests cover the four public triples, witness replay/tampering, state-versus-prefix
separation, exact noninteger arithmetic, terminal feasibility changes, bounded
scaling examples, set permutations, malformed inputs, CLI failures and repeatable
bytes. Generated checks use bounded standard-library enumeration, not Hypothesis.
Independent P2 checking and evaluator-owned holdouts are outside this slice.

With `F` first actions, `S` second actions, `C_a` reachable cells and `P` paths,
work is proportional to `sum_a S**C_a * P`; policy storage is linear in paths
and cells rather than in the number of policies. At the caps there can be
`5 * 5**8 = 1,953,125` candidate policies and `15,625,000` path evaluations.
Rational arithmetic adds integer-size costs. Worst-cap wall time has not been
benchmarked; no runtime SLA or timeout result is encoded as infeasibility.
No network requests or dependency installation are needed.
