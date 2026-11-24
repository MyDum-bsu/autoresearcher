# Wave 4 Stage B — independent read-only review

The first-success goal remains **unachieved**. This review supplies independent fixed-instance arithmetic evidence and source comparisons for coordinator inspection. It does not award scientific significance, novelty, a general theorem, or attestation.

All four pilot certificates passed the producer checker in normal and optimized Python. A separate exact arithmetic implementation also accepted all four and rejected its four invalid mutations in both modes. The additional review implementation initially failed twice for reviewer-side reasons; all failures and subsequent explicitly changed executions are retained. No producer file was repaired or overwritten.

## Scope and identities

Worktree `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`, were checked before the first write. New review files exist only under `artifacts/goal/wave-4/independent-review/`. This directory is abbreviated REVIEW below. All pilot outputs, sources, and wave contracts were treated as read-only.

`summary.json` records that all 104 files under `goal/wave-4/` and `artifacts/goal/wave-4/pilot/` retain their pre-review hashes. The six files frozen by `goal/wave-4/contract.json` match their declared hashes. Both copied inputs equal the authorized readonly baseline inputs byte for byte. Their raw SHA256 values are:

- printed: `4a900a987be67265d2fb43ad0db74188db0e3dccfb12d3212e00f9028504f2ca`;
- reconstructed decimal: `856e00ecc75bf5dc158dda82290bb22f9ea7c30bb5531179d1263747013d3e0d`.

Original A4 PDF SHA256: `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`. Original A4 and BT04 PDF hashes and baseline input hashes are retained in `origins.sha256`. Fresh layout extractions from those actual PDFs, and coordinate-bearing A4 pp12–13 extraction, are in `source/`; their hashes are in `summary.json`. Text extraction, not a new page-image rendering, was performed. The aligned Example 1 matrices were read directly from the fresh PDF layout extraction; the original source is not inferred from the pilot report.

## Arithmetic correctness: executed evidence

For each of the four frozen cases, the following commands exited 0:

```sh
timeout 240 python3 -B goal/wave-4/check.py CASE --controls
timeout 240 python3 -B -O goal/wave-4/check.py CASE --controls
```

Actual absolute command arrays, timings, and exit codes are in `commands.json`; raw streams are `CASE-normal.stdout/stderr` and `CASE-optimized.stdout/stderr`. These eight executions contain eight accepted positive results and 56 rejected invalid controls, not 64 independent positive certificates. The seven producer mutations test information label, terminal row, claimed lower objective, multiplier sign, input identity, closure identity, and missing vertex. Every normal/-O stdout pair is byte-identical. The information mutation alone checks metadata, not a semantic proof that arbitrary hostile policy code cannot read a future disturbance.

`review_checks_v2.py` implements separate chronological impulse propagation, exposed-face endpoint enumeration, primal inequalities, and generic sparse weighted-row accumulation for the upper bound. Its arithmetic does not import the producer's effects builder, polygon generator, rational parser, or bound checker. It does import the reviewed `state_to_block` only for actual policy-interface diagnostics; this reuse is not advertised as an independent policy algorithm. Both versions of review code were hashed before their respective execution.

The final successful independent executions were:

```sh
timeout 300 python3 -B -c 'import sys,runpy; sys.set_int_max_str_digits(20000); sys.argv=["artifacts/goal/wave-4/independent-review/review_checks_v2.py","independent"]; runpy.run_path(sys.argv[0],run_name="__main__")'
timeout 300 python3 -B -O -c 'import sys,runpy; sys.set_int_max_str_digits(20000); sys.argv=["artifacts/goal/wave-4/independent-review/review_checks_v2.py","independent"]; runpy.run_path(sys.argv[0],run_name="__main__")'
```

`independent-v2-wide-normal/optimized.stdout`, `.stderr`, and `.exit` preserve actual output and return codes (both 0). The integer-to-string limit is increased only within these subprocesses to a bounded 20,000 digits, not in system settings. Their stdout bytes match. Each mode accepted four fixed-instance arithmetic certificates and rejected 16 invalid mutations: false lower, false upper, negative multiplier, and missing vertex. Full exact bounds, interior disturbances, measured states, selected suffix blocks, and terminal states are retained in raw JSON, not replaced by floating summaries.

Three interior fan triangles per case were checked using weights `(1/7,2/7,4/7)`. The associated continuous prefix disturbances are convex combinations of their vertex realizations. The actual measured-state routine selected the corresponding convex combination of suffix controls. Original chronological dynamics were then replayed for suffix x-min, x-max, and y-min disturbances: 36 full interior-prefix trajectories per mode. Each met the terminal strip and reward floor. These are diagnostics of the actual interface, not finite sampling promoted to universal validity.

### Recomputed outward intervals

The following endpoints are rounded outward to 12 decimal places from the exact fractions. Nonzero gaps remain nonzero.

| Input | Closure | Enclosure | Gap, floating display only |
|---|---:|---|---:|
| printed | 67 | [2.905827967435, 2.905827967441] | 5.667979057932578e-12 |
| reconstructed decimal | 67 | [2.912639964467, 2.912639964474] | 5.401181872865298e-12 |
| printed | 104 | [1.495710098119, 1.495710098125] | 5.320142433962708e-12 |
| reconstructed decimal | 104 | [1.501101989375, 1.501101989383] | 6.220651786050736e-12 |

The independent arithmetic outputs reproduce these bounds as exact fractions. `summary.json` binds each certificate SHA256. Agreement is fixed-instance evidence, not exact optimality, a theorem proved from examples, or first scientific success.

## Source correspondence and information assumptions

Fresh original A4 physical pp2–6 establish the linear discrete recurrence, terminal constraints for **all** per-time disturbances, exact current-state observation at a preselected closure, and selection of a whole control block after that observation. In particular, p4 Assumption 1 says to measure the current state and choose the next block depending on that measurement. The quantification is rectangular over the continuous disturbance boxes, not a finite correlated path model. No intermediate state constraint is imposed in Example 1.

A4 physical p12, equation (3.1), fixes `T=120`, initial state `(0,1)`, terminal first coordinate in `[2,10]`, `|u|<=1`, `|w|<=0.5`, and terminal second coordinate maximization. The printed coefficient input matches the decimals shown there. General sections use minimization of a worst-case cost, whereas this example maximizes reward. Review bound directions follow the example, not an unmodified cost sign.

The reconstructed-decimal manifest is explicitly labeled inferred sensitivity data, with A3/A2 motivation rather than author precision confirmation. Its equality to the readonly M0 input establishes provenance only. This review does not verify the inference of trigonometric coefficients or substitute it for printed data. The two variants remain different exact rational models. Their numerical closeness to reported source values cannot identify the authors' actual numerical input.

The legacy manifest `scope=open_loop` label is coefficient provenance, while the wave contract and actual certificate explicitly name the new single-closure policy class (`model-and-source.md:7`, `check.py:84–91`). Reusing that input does not itself grant a more informative sensor. The routine `state_to_block` takes the pinned model, frozen certificate, and measured state; it has no future disturbance input and returns the entire suffix. The executed recurrence diagnostics exercise nonzero, non-extreme prefix disturbances. No subsequent measurement is used.

## Continuous coverage, finite reduction, and every-state implementation

The following separates executed finite identities from the written mathematical extension in `goal/wave-4/model-and-source.md:9–25`.

1. **Reachable prefix set.** The terminally propagated disturbance is exactly `Z=sum[-D_t/2,D_t/2]` over prefix times. Independent face enumeration exposes both endpoints of every generator-perpendicular supporting face, including opposite faces. It obtains exactly the supplied 134 vertices for r67 and 208 for r104. There are no parallel nonzero generators in these fixed instances. Every supplied consecutive edge has the exact support of the complete continuous zonotope. This is not a sampled direction grid.
2. **Future disturbance.** For each terminal row, the suffix box contributes exactly `sum |D_t,j|/2`. This is the support of the entire continuous suffix box; independence from prefix history permits the same suffix box at each measured state. Simultaneous attainment of the three coordinate extrema is unnecessary, since each inequality must hold separately for all disturbances.
3. **Necessity.** Given any admissible state policy and its common first block, its controls evaluated at the reachable vertex states satisfy the finite rows. Hence the finite program is a relaxation of the original policy optimization and its verified dual upper bound has the correct direction. The pinned state propagation is invertible, as explicitly checked by the producer checker; distinct propagated vertices identify distinct measured states.
4. **Sufficiency.** For each fixed first block, all reachable states map affinely to Z. Its ordered polygon admits the fan triangulation used by the routine. Independent checks establish positive orientation of every fan triangle, exact area sum, and exact polygon boundary support for these instances. On a triangle, a convex combination of the stored suffix blocks preserves the control box and each robust terminal row because recourse coefficients are fixed and the dependence on the measured disturbance image is affine. This gives the written every-state extension, rather than an inference from the 36 replayed trajectories.
5. **Implementability.** The routine subtracts the nominal closure state, propagates the difference to terminal coordinates, and selects the first containing triangle with exact barycentric weights. A fixed tie rule resolves boundaries; adjacent interpolants agree on their common fan edges. This is a piecewise-affine state rule on the reachable polygon, not a controller supplied with hidden prefix history. `check.py:43–76` and `model-and-source.md:25` contain the actual implementation and explanation.
6. **Off-domain behavior.** The executable rejects unreachable measurements; the review observed the explicit domain error. The zero-block total Borel extension mentioned at `model-and-source.md:13` is a mathematical extension, not implemented by the routine. This is not a reachable-state failure under the exact source model. Noise, numerical state measurement, finite-precision deployment, and robust feasibility off the reachable polygon are not certified.

No general triangulation/finite-reduction theorem was machine-formalized here. The machine checks discharge the concrete polygon, support, box, and rational inequalities. The universal real-state extension relies on the displayed convexity argument and known finite fixed-recourse reasoning. It is not legitimate to claim a formally checked general theorem on the strength of these tests.

## Bound direction and extraction history

For reward maximization, the feasible state-policy construction yields a **lower** guarantee. The row certificate has nonnegative weights, objective-row mass exactly one, and upper value `b^T lambda + ||M^T lambda||_1`. Adding the finite inequalities yields `q <= b^T lambda - (M^T lambda)^T u`; the support of `[-1,1]` controls bounds the final term from above. The independent checker assembles this through generic variable indices, including shared prefix variables and distinct suffix blocks. It does not require rounded solver multipliers to have zero stationarity residual. There is no reversal of lower and upper bounds in the executed certificates.

Three historical producer extraction failures remain present. This review did not rerun the solver, generator, extractor, or alter their proposals. The accepted objects are the final saved certificates, not numerical solver status flags. Their acceptance does not retrospectively make the initial failures pass. `goal/wave-4/outcome.md:36–44` and `extract.py` disclose the explicit prefix-viability correction. Exact checking of its resulting controls, rather than trust in the correction procedure, supports the present bounds.

## Closest-source delta and usefulness: separate from arithmetic

**A4 comparison.** Physical pp11–12 expressly warn that outer approximation containment does not ensure true closure containment: reward can deteriorate or continuation can fail. Physical pp12–13 report 2.913110 and a trajectory value 2.912640 at closure 67, with a 4.7e-4 difference. The reconstructed-decimal enclosure rounds to that trajectory value at six decimals. Since author coefficients and their particular initial program are unconfirmed, this does not certify the paper's policy, its universal guarantee, or an error in the paper. The source's description of an extremal trajectory is preserved; the review does not silently reinterpret it as an independently verified universal guarantee.

**BT04 comparison.** Original `research/sources/BT04.pdf`, physical p5 (printed p355), Theorem 2.2 explicitly states that finite convex-hull uncertainty with fixed recourse has an exact LP with recourse variables per vertex. After exact suffix support elimination, this pilot has fixed suffix coefficients and affine uncertainty in the vertex-dependent right-hand sides; shared first-block variables and reward are the nonadjustable variables. The theorem thus already supplies the central finite-recourse mechanism. The planar zonotope representation and state-based interpolation instantiate that mechanism; the evidence does not identify a new generic vertex theorem. Theorem 2.2 itself points to its reference [12], not a new result of this pilot.

**Unresolved nearest-control-source comparison.** A4 physical pp2 and 16–17 identify its prior single-closure work [14], Kastsiukevich and Dmitruk 2021, and earlier exact feedback methods. This Stage B did not freshly audit all of those originals or compare their complete algorithms/certification methods. No exhaustive novelty or priority claim follows. The producer already disclaims a new literature delta (`outcome.md:32–34`).

The useful deliverable is a small, exact, replayable rational benchmark enclosure with a concrete every-reachable-state policy representation and adversarial controls. It does not reproduce the 203-normal approximation algorithm or certify the authors' computed program. It can help distinguish tight certification from trajectory-only evidence for the pinned inputs. Such usefulness and arithmetic agreement do not meet the original requirement of a substantive contribution with demonstrated closest-source delta.

## Preserved review failures and limits

- `review_checks.py` v1 omitted opposite exposed faces in its independent enumeration. It failed in normal and -O, before reporting results. The initial `execution.exit=1`, `execution.stderr`, and `independent-normal/optimized.stderr` are retained. This was a defect in review code, not a counterexample to the pilot.
- A new filename, `review_checks_v2.py`, adds the opposite faces of this centrally symmetric zonotope. Its default-runtime executions failed while serializing a long exact terminal fraction (`4300`-digit integer string limit). `independent-v2-normal/optimized.*` retain those failures. No mathematical inequality failed there.
- The explicitly changed, process-local 20,000-digit serialization envelope produced the successful `independent-v2-wide-*` runs. There was no automatic retry, solver retry, provider fallback, new worker, or producer repair. All versions and failures remain immutable review evidence.
- This review does not establish global task accounting or native provider billing/retry behavior. The instructional tool-call envelope was tracked manually, not mechanically enforced. Subprocesses were sequential and bounded; no background process was started.
- No live journal, blueprint, task tracker, corpus, glossary, configuration, or scientific status was written. No install, comparator, commit, push, attestation, or system change was performed. No broad repository gate, Lean theorem check, or new scientific case was run. These are outside this read-only assignment.

## Coordinator handoff

Consider the four concrete fixed-input certificates and the source comparison as a **useful certified reproduction dossier**, subject to the explicit universal-extension and source-identity scope above. The arithmetic checks report acceptance; this review does not report scientific success. The missing author numerical data/program, absent new literature delta, and unformalized general extension remain open. Coordinator inspection is still required. No repair allocation or scientific status promotion is requested by this report.
