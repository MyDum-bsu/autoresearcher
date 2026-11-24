# Methods, executable evidence and transfer boundaries

Read `correspondence.md` first. Its dictionary, information-preserving transformations, support rows, vertex extension and closure sets constitute the written general derivation. This file records what the methods do and what the checks actually cover.

## Source method map

| Method | Exactness conditions and role here | Bound direction for cost minimization |
|---|---|---|
| Exact future support | Independent suffix box, fixed whole suffix control, linear terminal rows. Derived row by row in correspondence §3. | Equality, including signed epigraph offset |
| Vertex LP | Given finite hull, affine data, fixed recourse, continuous convex control domain. BT04 Thm 2.2 p5; GTW20 Prop 1 pp3–4. | Equality of feasible epigraph levels and optimum |
| Complete FME | Project suffix controls out of all tightened terminal, cost and box inequalities; keep zero-coefficient rows, pair every lower and upper row. ZHS18 original physical pp6–8, Algorithm 1/Thm 1. | Equality of projection, not an affine-policy restriction |
| Robust LP duality | A remaining row affine in deviation can be maximized exactly over a nonempty bounded polytope. Feasibility and finiteness are checked hypotheses; no uncertain recourse is dualized as though fixed. | Equality for complete exact reformulation |
| Affine decision rule | Constrain y(xi)=b0+B1 xi, require all robust rows. GTW20 p4 explicitly warns these can be suboptimal. | Feasible restriction gives upper cost / lower reward |
| Incomplete vertex/scenario subset | Omits required states unless its hull is the complete image. | Relaxation gives lower cost / upper reward |
| Outer closure approximation | Larger state set than the exact cost-level closure set. | Relaxation only; no policy certificate |

ZHS18's local PDF has a ResearchGate cover: physical p6 is manuscript p5 (model), physical pp7–8 are manuscript pp6–7 (Algorithm 1 and theorem). Its fixed recourse matrix and bounded eliminated-variable hypothesis hold here because suffix control coordinates have explicit box rows. The proof reconstructs an eliminated coordinate between a maximum of lower bounds and a minimum of upper bounds; finite max/min preserve measurability for our affine data. Repeated complete elimination gives a static robust description, but can multiply rows substantially. Partial elimination followed by affine restrictions remains a restriction, not automatically an exact method. No FME run was needed for these saved certificates.

On a simplex uncertainty image, barycentric coordinates are affine on the whole image, so vertex interpolation itself is an affine optimal recourse construction under the same fixed-recourse/convex-domain hypotheses. This is a conditional consequence of the displayed proof, not a newly searched affine-rule theorem. The actual legacy polygons are not simplices. Fixed recourse alone supplies no general affine-rule exactness claim for them. No fresh affine-policy literature search or comparison run was performed.

For an H-representation Z={xi:D xi≤e}, each projected robust affine row `alpha(a,eta)+beta^T xi≤0` has the exact dual support form `exists lambda≥0: D^T lambda=beta, alpha+e^T lambda≤0`. Z must be nonempty and support finite; both follow here from the nonempty compact image, with relative-hull equalities included as two inequalities if needed. This displayed LP duality step is a mathematical reconstruction. The saved certificates instead directly certify the finite primal/dual bounds; no unseen solver output is accepted as a proof.

## Formulation dimensions

Let k=T−r, N=number of vertices of the chosen deviation image, m=control dimension and ell=number of one-sided terminal inequalities. The vertex LP has `rm+1` common variables and `Nkm` adjustable variables; total `rm+1+Nkm`. There are `N(ell+1)` terminal/cost inequalities, `2rm` prefix box rows and `2Nkm` suffix box rows if boxes are explicitly expanded. Equalities/inequalities describing an uncertainty image are not counted as LP decision rows after a vertex list is supplied. No extra initial-state variable is introduced. Degenerate images use their actual vertex count, not a full-dimensional formula.

The four-case numerical ledger is the sole quantitative authority: `numeric-ledger.json`. With the saved scalar-control horizon and terminal-deviation polygons it records:

| Cases (both coefficient variants) | r | k | N | Common variables | Adjustable variables | Total variables | Terminal/cost rows | Box rows |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| r67 | 67 | 53 | 134 | 68 | 7102 | 7170 | 402 | 14338 |
| r104 | 104 | 16 | 208 | 105 | 3328 | 3433 | 624 | 6864 |

These dimensions are an interpretation of existing vectors, not a newly generated LP. They do not demonstrate a scaling or runtime advantage over the source closure algorithm. Enumerating disturbance-coordinate box vertices would count path information and many duplicate/interior images; it is not the observed-state vertex inventory used here.

## Frozen application and command

`case-contract.json` pins all four cases, the checker hash, historical input/output hashes and the accepted/invalid control inventory before execution. The new `check.py` imports only the read-only legacy checker and its arithmetic helper. It calls the original exact certificate check, independently constructs chronological impulse columns for the standard ARO row interpretation, recomputes all terminal/cost residuals using Fraction, and checks the signed reward-to-cost interval transformation. It does not run the generator, optimizer, extractor, private panel or comparator.

Acceptance from the assigned worktree:

```
timeout 300 python3 -B bridge/transfer-v1/check.py
timeout 300 python3 -B -O bridge/transfer-v1/check.py
```

These run actual checks, reject changed frozen files, and fail explicitly on any unexpected accepted invalid control. They do not trust `result.json` or pass declarations. Neither mode uses assert for validation. Process-local integer serialization limit is explicitly fixed to allow the large exact trajectory fractions; it is not a retry or system change. The entrypoint is read-only and reviewable without a disposable writable copy.

Raw streams and exit codes are `artifacts/bridge/transfer-v1/author/{normal,optimized}.{stdout,stderr,exit}`. Normal and optimized stdout are byte-identical and both exit codes are zero. Each case in each mode accepts positive mapping, robust terminal/signed-cost rows, state-only timing and chronological replay; it rejects cost-sign corruption, terminal-row reversal, incorrect information metadata and a semantic future-information table. The table holds the actual zero-prefix-disturbance measured state fixed, varies the future suffix disturbance, and deliberately changes one suffix control. The valid state-to-block function returns the same block; the hostile table is rejected on equal-observation/different-control inconsistency. This distinguishes a metadata gate from a finite semantic timing diagnostic. It is not a static verifier of arbitrary policy code, nor an exhaustive nonanticipativity test over every real state.

The chronological replay uses one existing measured state and two future paths per case, retaining exact terminal coordinates. All vertex residuals are checked with exact box support; finite replay is supplementary. Historical independent review arithmetic remains reused evidence, not a newly independent proof. Existing certificates have nonzero reward gaps. The cost enclosure is obtained by endpoint negation/reversal; acceptance does not imply exact optimality or verification of the authors' own policy.

Printed and reconstructed-decimal coefficients remain distinct exact models. Reconstructed coefficients are inferred sensitivity data, not confirmed author coefficients. No source-data discrepancy is resolved by their numerical similarity. The original M0 `open_loop` input label is coefficient provenance, not the policy semantics; the wave-4 contract binds the single-closure policy class explicitly.

## Historical failures and non-delivery boundaries

All frozen historical files are rehashed by the acceptance command. Producer extraction failures and independent-review v1 face-enumeration/default serialization failures remain intact. Their later explicitly changed runs do not retroactively pass those failures. No old path, contract, checker, certificate or result was replaced.

Not run: new solver optimization, regenerated cases, source closure-algorithm reproduction, affine-policy solver comparison, universal symbolic judge, Lean build, formal transfer theorem, scientific admission, attestation and broad repository gates. None is needed for this narrow read-only row bridge; none is reported passed. Stage B independent correspondence review is coordinator-owned and not launched here. The author's logic pass checks quantifier order, meaning stability, both witness directions, sign polarity and hidden rank assumptions; it is editorial analysis, not a scientific verdict. Code outputs judge only the stated fixed-instance checks.

The first scientific success remains false. A written universal derivation is neither formalized nor admitted to a thesis. The near objective may be useful as an application of known mathematics; novelty is not an acceptance gate for it. Long-term charter obligations remain unchanged.

Next bounded question from this boundary: which exact projected-image/closure representation is preferable for a specified higher-dimensional instance under a frozen memory budget, while retaining recoverable state-only suffix witnesses? This is a representation question for future owner selection, not a reopened closed route or a claimed new theorem. Measurement noise, multiple future closures, correlated disturbances, nonterminal path constraints, integer/nonconvex recourse and uncertain recourse matrices are separate models. They require a new information/selection argument rather than silent transfer of this result.

Instructional calls and subprocesses are bounded manually; no native provider retry/billing telemetry or full host containment is available. No automatic retry, fallback, install, system change, background worker, journal/scientific-state write, commit or push was used.
