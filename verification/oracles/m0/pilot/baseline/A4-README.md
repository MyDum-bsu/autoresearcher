# P2b: exact A4 open-loop certificates

This offline, standard-library implementation produces and independently checks
portable certificates for two pinned decimal instances of A4 Example 1. It has
no journal, tracking, corpus, configuration or scientific-status write authority.
It does not solve the continuous one-measurement problem at r=80.

## Inputs and provenance

Both full manifests have horizon 120, x0=(0,1), dynamics
`x(t+1)=A*x(t)+B*u(t)+E*w(t)`, continuous controls |u(t)|<=1 and independent
continuous disturbances |w(t)|<=1/2. Every disturbance sequence in the full
rectangular product is admissible. The terminal slab is 2<=x1(120)<=10 for
every disturbance path; the objective is to maximize the guaranteed x2(120).
All 120 controls are selected before any disturbance, with no observation.

| Manifest | Exact decimal interpretation | Rounded reward regression (12 places) |
|---|---|---|
| `pilot/inputs/a4_printed.json` | A=((0.9950,0.0998),(-0.0998,0.9950)), B=E=(0.0050,0.0998) | 1.495710098124 |
| `pilot/inputs/a4_reconstructed_decimal.json` | c=0.9950041652780258, s=0.09983341664682815, A=((c,s),(-s,c)), B=E=(1-c,s) | 1.501101989382 |

The manifests store reduced rational strings, not floating-point numbers.
Reconstructed decimals are explicit sensitivity inputs: they are neither exact
cos(0.1)/sin(0.1) nor confirmed author data. Their identities must never be
normalized into the printed instance. Neither program uses the rounded reward
regressions to generate or accept certificates.

Source anchors, retained with their PDF SHA-256 fingerprints in the manifests:

- A4, `corpus/our_papers/A4_Дмитрук_2022.pdf`, PDF p.12, printed p.77,
  Section 3, Example 1, (3.1) and its following paragraph: printed dynamics,
  bounds, initial state and horizon. That paragraph reports 1.501102, which
  differs from the exact rational result for its four-place printed coefficients.
  The reconstructed result rounds to that reported number; this is not proof
  that the authors used the reconstructed decimals.
- A3, `corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf`, PDF p.8,
  printed p.45, last paragraph of Examples: sampling period h=0.1; PDF p.9,
  printed p.46, Example 1, (20) and following paragraph: discrete comparator.
- A2, `corpus/our_papers/A2_Дмитрук_2018.pdf`, PDF p.15, printed p.678,
  Section 6, (6.1): continuous oscillator motivating reconstruction only.
  This is not the same terminal problem and does not confirm decimal precision.
  The implementation plan's separate p.16 comparison of Examples 2/3 is not
  the anchor used here for the oscillator equation.

During this implementation, the three source-file fingerprints were compared
with the preceding review, and the indicated page text was extracted directly.
This was not a new visual/layout review or an independent author-data confirmation.
Historical `specs/research-pilot/check_dmitruk_open_loop.py` was inspected only
for provenance and indexing risks; neither program imports or wraps it.

Numerical input validity is separate from source-page verification. Both programs
pin the SHA-256 of the **entire canonical manifest**, including source identities,
page/region labels, origin, scope, schema and all coefficients. This rejects
unknown coefficients even if a supplied certificate solves that changed instance.
Pinning metadata does not verify a quotation or a PDF page. The numeric checker
needs no PDFs and returns `source_page_verification=not_performed_by_numeric_checker`.
It does not admit sources into the corpus.

## Certificate construction and independent checking

The producer `pilot/baseline/a4_certificate.py` applies A repeatedly to B, E and
x0 using exact fractions. Its columns initially have increasing powers of A;
it reverses them explicitly to chronological order before constructing controls.
For each dataset it starts with the box optimum u_t=sign(C_ty). These pinned
instances violate the tightened lower slab bound at that starting point. It
increases nominal x in ascending y-loss/x-gain cost, exhausting cheap control
flips before taking a fractional final adjustment. It exports the final marginal
cost as the lower multiplier and zero as the upper multiplier. No solution values
are hardcoded. Unsupported assumptions, insufficient capacity, either feasibility
failure or a nonzero exact primal/dual gap cause explicit failure.

The verifier `pilot/checkers/a4_check.py` has independent parsing, manifest pins,
arithmetic and checking code. It imports no producer or legacy numerical helpers
and accepts only JSON data, never executable names or command/import strings.
It computes effects with backward row-adjoint recursions, separately using E
for disturbance support, and propagates the actual proposed controls forward
from x0 in chronological order. It checks that the forward terminal state equals
the backward-adjoint expansion as an additional indexing/dynamics invariant.

Write C_t=A^(T-1-t)B, D_t=A^(T-1-t)E and d=A^T*x0. Independent box disturbances give
`sx=(1/2)*sum(abs(D_tx))`, `sy=(1/2)*sum(abs(D_ty))`. A nominal terminal state
(x,y) is robustly feasible precisely when `x-sx>=2` and `x+sx<=10`; its guaranteed
reward is `y-sy`. The checker tests both inequalities separately.

For L=2+sx and H=10-sx, any feasible control satisfies x-L>=0 and H-x>=0.
For lambda,mu>=0, adding `lambda*(x-L)+mu*(H-x)` to its reward cannot decrease
that reward. Expanding x=d_x+sum(C_tx*u_t), y=d_y+sum(C_ty*u_t) gives the
following upper bound after maximizing each affine term on [-1,1]:

```text
U = d_y - sy + lambda*(d_x-L) + mu*(H-d_x)
    + sum(abs(C_ty + (lambda-mu)*C_tx)).
```

This argument does not assume the two terminal constraints have the same
worst disturbance path. A valid primal control attaining U proves open-loop
optimality for this exact input. The checker requires nonnegative multipliers,
exact feasibility, independently recomputed support, exact claimed reward and
**exact equality** of primal reward and dual upper bound. There are no tolerances
and no validation asserts; Python `-O` does not disable checking.

## JSON contract and pure APIs

All emitted numbers except schema versions are canonical reduced `n/d` strings,
with positive denominators and zero `0/1`. Floats, NaN, Infinity, duplicate JSON
keys, unknown fields, wrong versions and noncanonical rational strings fail.
Canonical JSON is UTF-8 from `json.dumps(data, sort_keys=True,
separators=(",", ":"), ensure_ascii=True, allow_nan=False)`. A digest hashes
these bytes **without a newline**; CLI output appends exactly one newline.
Input whitespace/key order may differ, but numeric/provenance values do not
normalize. There are no timestamps or output-directory-dependent fields.

Manifest identities and canonical digests:

```text
a4_printed
154b1a0181c5a9f29bcc20d64bc111220cbb4193b3560387b543d2c31fe32602
a4_reconstructed_decimal
77dca22ff207f2d7176fe103c2f38552c7a40e1d60cd39d10f1958bc06f1a869
```

A certificate has exactly `schema_version=1`,
`certificate_type=a4_open_loop_primal_dual`, `coefficient_set_id`, `input_sha256`,
`scope=a4_example_1_open_loop_rectangular_disturbances_exact_rational`,
`method=forward_power_columns_fractional_cost_adjustment_v1`,
`coverage=all_120_controls_and_all_independent_continuous_box_disturbances`,
`arithmetic=exact_rational`, `controls` (120 chronological rational strings),
`objective` (guaranteed reward), `support` (`x`,`y`) and `multipliers`
(`lower`,`upper`). Labels and identity are checked, not trusted as evidence.

The compact validation record returns the bound input identity/digest, scope,
coverage, arithmetic, `certificate_validity=valid`, independently computed
`exact_reward`, `dual_upper_bound`, `nominal_terminal`, `robust_terminal_x`,
`support`, `numerical_input_validity=pinned_manifest_match`, and the explicit
source-page limitation. Long exact rational strings are intentional. This is a
numerical certificate-validity record, not a project/scientific status change,
attestation, novelty result or answer to Q-A4-R80-v1.

- Producer: `parse_input(text)`, `validate_input(manifest)` and
  `make_certificate(manifest)`; validation failures raise `ValueError`.
- Verifier: `parse_json(text)`, `validate_input(manifest)` and
  `check_certificate(manifest, certificate)`; ordinary validation failures raise
  `CheckError`, a `ValueError` subclass. The checker has no producer import.
- Verifier's `evaluate_dynamics(dynamics, controls, disturbance_radius)` is an
  **unpinned arithmetic helper**, used for perturbation tests, not a certificate
  validator or an alternate way to approve an unrecognized input. It receives
  Fraction controls and canonical rational strings in the dynamics dictionary.

## Commands and acceptance

From the feature worktree root, caller-owned certificate storage can be used as
follows (substitute either input name). These programs write only stdout/stderr;
they do not retain artifacts themselves.

```sh
python3 -B pilot/baseline/a4_certificate.py \
  --input pilot/inputs/a4_printed.json > /caller/chosen/printed-certificate.json
python3 -B pilot/checkers/a4_check.py \
  --input pilot/inputs/a4_printed.json \
  --certificate /caller/chosen/printed-certificate.json

PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pilot/checkers -p 'test_a4_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -O -m unittest discover -s pilot/checkers -p 'test_a4_*.py'
```

CLI exit 0 means a generated certificate or a valid exact numeric check. Exit 2
means malformed/unsupported input, an invalid certificate or an I/O error, with
an explicit stderr diagnostic and **no stdout success record**. Unexpected
internal failures remain nonzero failures rather than mathematical outcomes.

The tests reuse one immutable generated certificate per input for mutations.
They check exact primal/dual equality for both datasets, chronological replay,
separate realizable extremal paths for both terminal bounds and reward,
nonnegative multipliers, tampered A/B/E/initial state/horizon, controls and their
order, objective, support, multipliers, terminal constraints, schema/source IDs,
identity/hash/scope/method/coverage, empty/malformed certificates and CLI errors.
A reconstructed certificate rebound to the printed identity still fails.
Small direct A/E perturbations change recomputed dynamics/support/reward,
rather than looking up regression values; the pinned certificate boundary
continues to reject such altered inputs.

For each dataset, a second generation and two checker runs in separate processes
must be byte-identical. Checker runs use a temporary working directory without
PDFs, producer modules or source-relative files; only explicit manifest and
certificate paths are used. Tests remove their temporary certificates. No large
permanent certificate artifact is included in this slice. The suite target is
under 60 seconds; measured execution times are reported in the handoff.

P1/P2a code and READMEs remain unchanged. No continuous r80 solution, author-data
confirmation, visual source re-review, general LP optimizer, symbolic theorem,
Lean proof, external judge registration or live-state integration is included.
