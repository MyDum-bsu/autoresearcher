Reading proposal for the essay; blocks NOT yet registered in the science graph.

# Reading proposal: two-stage ARO exactness and information structures

meta: intake batch of 2026-10-20; three PDFs, none in `corpus/MANIFEST.md`; hashes computed
with `sha256sum` on the intake copies. These are proposal blocks, not evidence and not graph
entities. No block below has been registered, encoded, or judged.

- Kurtz, Jannis. "Bounding the Optimal Number of Policies for Robust K-Adaptability."
  arXiv:2409.12630v3 [math.OC], 3 Sep 2025, 25 pp.
  `file: corpus/intake/2409.12630.pdf`
  `sha256: 839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- Dai, Ling; Ho, Chin Pang. "When Is Two-Stage Sample Robust Optimization Asymptotically
  Optimal? A Simple Perspective." arXiv:2608.22999v1 [math.OC], 24 Aug 2026, 39 pp.
  `file: corpus/intake/2608.22999.pdf`
  `sha256: b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- Tsang, Man Yiu; Shehadeh, Karmel S.; Curtis, Frank E. "An inexact column-and-constraint
  generation method to solve two-stage robust optimization problems." arXiv:2207.03291v2
  [math.OC], 5 Nov 2022, 27 pp.
  `file: corpus/intake/2207.03291.pdf`
  `sha256: cff68fa585627e330cea15838408aca67d0b7fe87f80a621e680f243620930ec`

Conventions used in every block:

- `pdf_page` is the physical page of the intake PDF; `printed_page` is the footer numeral.
  On every anchored page of all three files a footer numeral is visible and equals `pdf_page`;
  the one page without a numeral (Tsang p. 1, footer "Preprint submitted to arXiv") is not used
  as an anchor.
- `quote` is contiguous text from the PDF, with line-break hyphenation and line wrapping
  removed. Mathematical symbols are transcribed in Unicode/ASCII (`nξ` for n_ξ, `R^m_+`,
  `ε̃` for epsilon-tilde). A separate `formula` line gives the typeset formula when the PDF
  splits it across lines; the quote itself remains verbatim.
- `gloss` is one plain sentence, not a paraphrase of the theorem's proof.
- `relevance` answers the three essay questions explicitly: (a) closure-moment count;
  (b) simplicity geometry vs vertex lists and affine exactness; (c) information structure
  as a design variable.

---

## 1. Kurtz (2024/2025): how many policies suffice

The paper's object is the general non-linear two-stage problem
`inf_{x∈X} sup_{ξ∈U} inf_{y∈Y(x)} f(x,y,ξ)` with `Y(x) ⊆ Y ⊂ Z^{n_y}` (integer
wait-and-see decisions, bounded `Y`), and the k-adaptability relaxation
`opt(k) = inf_{x∈X, y_1..y_k∈Y(x)} sup_{ξ∈U} inf_{i=1..k} f(x,y_i,ξ)`.
Two regimes are separated: objective uncertainty with convex `U`, and constraint
uncertainty with convex `U` (recourse-stability), plus finite `U` (complexity).
Scope note: the exact bound is stated for integer wait-and-see decisions; it is a policy-count
bound, not a closure-moment bound, and it does not directly apply to continuous affine policies.

### thm-kurtz-2 — objective-uncertainty bound

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 5
- printed_page: 5
- label: Theorem 2
- quote: `f (x, y, ξ) is concave in ξ for every x ∈ X , y ∈ Y and let k ≥ nξ +1. Then, a solution x ∈ X is optimal for (k-ARO) if and only if it is optimal for (2RO).`
- formula: `k ≥ n_ξ + 1`, where `n_ξ = dim(U)`; `U` convex; `f` continuous and concave in `ξ` for each fixed `(x,y)`; `Y` bounded and integer-valued; no convexity in `x` or `y` is assumed.
- gloss: For convex uncertainty and an objective concave in the scenario, `n_ξ+1` pre-committed integer recourse policies already attain the exact two-stage optimum.
- relevance:
  - (a) This is a bound on the number of distinct second-stage policies, not on the number of measurement or closure times. Its dimension is the uncertainty dimension `n_ξ`, not the horizon `T`; the transfer to closure moments is an analogy, not a corollary.
  - (b) The mechanism is a support-constraint count on the epigraph problem in `(ξ,z)`; it uses convexity of `U` but no vertex-degeneracy or simplicity property. It therefore says nothing about vertex-list `Z` beyond the convex-hull case.
  - (c) `k` is the design variable: a budget of pre-committed policies. The paper's DDID example (Example 5, p. 6) makes information acquisition itself a first-stage binary decision and applies Theorem 2 to get `k = n_ξ+1`; this is the closest formal precedent in the batch for treating an information structure as a decision.

### fact-kurtz-2-dim — dimension dependence

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 5
- printed_page: 5
- label: prose immediately after Theorem 2 (p. 5)
- quote: `The latter bound on k does only depends on the dimension of the uncertainty set and not on the dimension of the decision variables x and y.`
- gloss: The bound is independent of `n_x` and `n_y`; only `dim(U)` enters.
- relevance:
  - (a) Confirms that the count is governed by uncertainty dimension, not by the number of decision stages or the number of state variables; no direct closure-moment reading.
  - (b) A vertex-list `Z` in `R^d` enters only through `d = dim(Z)`; the paper does not refine the bound by the number of vertices or by edge incidences.
  - (c) The design variable `k` is separated from the dimension of the decision problem, which is useful if the essay wants a policy-count axis independent of the controller dimension.

### rem-kurtz-3 — relation to the linear bound

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 5
- printed_page: 5
- label: Remark 3
- quote: `If nξ ≤ ny , Theorem 2 coincides with the bound derived in [HKW15] for the case that f is a linear function.`
- formula: classical linear bound `min{n_y, n_ξ} + 1` (stated on p. 5 before Theorem 2); Theorem 2's bound is `n_ξ + 1`, coinciding when `n_ξ ≤ n_y`.
- gloss: For linear objectives the sharper known bound is `min{n_y,n_ξ}+1`; Theorem 2 matches it when the uncertainty dimension does not exceed the recourse dimension, and for nonlinear concave objectives it uses `n_ξ+1` even when `n_y < n_ξ`.
- relevance:
  - (a) The dimension governing the count is the smaller of uncertainty and recourse dimensions in the linear case; the nonlinear theorem trades that for a uniform `n_ξ+1`. Either way, the count is a policy count, not a closure-moment count.
  - (b) No geometric condition on `Z`; only dimensions.
  - (c) The design budget `k` can be reduced when `n_y < n_ξ` and the objective is linear, which matters if the essay's controller has low-dimensional recourse.

### thm-kurtz-7 — approximation below the bound

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 6
- printed_page: 6
- label: Theorem 7
- quote: `Then, for any s, k ∈ N with s ≤ k it holds opt(s) − opt(k) ≤ Ldiam(Y)ln ( k s ) .`
- formula: `opt(s) - opt(k) ≤ L · diam(Y) · ln(k/s)`, under `f` continuous, concave in `ξ`, and Lipschitz in `y` with constant `L > 0`.
- gloss: If `k` policies are allowed and only `s ≤ k` are used, the objective loss is at most `L·diam(Y)·ln(k/s)`; with `k = n_ξ+1` this bounds the loss of any `s`-policy approximation.
- relevance:
  - (a) Gives a quantitative penalty for using fewer policies than the exact bound, but the variable is still policy count, not closure count. It is the natural template for a "fewer information cells" penalty in the finite-horizon problem, with `s` read as cells rather than moments.
  - (b) No geometric condition on `Z` appears; the bound depends on `diam(Y)`, i.e., on the recourse action set, not on the support's vertices.
  - (c) The design question becomes continuous: choose `k` (or `s`) to trade policy budget against additive objective loss.

### cor-kurtz-8 — additive guarantee threshold

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 8
- printed_page: 8
- label: Corollary 8
- quote: `Then it holds opt(k) ≤ opt(2RO) + α, where opt(2RO) is the optimal value of (2RO).`
- formula: `k ≥ n_ξ + 1 − [(n_ξ+1)(e^{α/(L·diam(Y))} − 1)] / e^{α/(L·diam(Y))}` and `α ≥ 0`.
- gloss: An additive error `α` is guaranteed once `k` is within a specific exponential fraction of `n_ξ+1`.
- relevance:
  - (a) Supplies the exact "how far below the exact count can we go" threshold; if the essay proposes a closure-count bound, this is the shape of the corresponding guarantee.
  - (b) Still support-geometry-free; no vertex/simplicity input.
  - (c) Turns the policy budget into a tunable design parameter with a certified error, which is the closest quantitative analogue to choosing a coarser closure set.

### thm-kurtz-11 — constraint-uncertainty bound via recourse stability

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 10
- printed_page: 10
- label: Theorem 11
- quote: `Then, if k ≥ min {R(nξ + 1), |Y|} , a solution x ∈ X is optimal for (k-ARO-C) if and only if it is optimal for (2RO-C).`
- formula: `k ≥ min{R(n_ξ+1), |Y|}`, where `R` is the number of convex recourse-stable regions whose closures cover `U`, for every feasible `x`.
- gloss: For constraint uncertainty, the count is the number of convex recourse-stable regions times `(n_ξ+1)`, capped by the total number of integer recourse actions.
- relevance:
  - (a) This is the structural bridge from a geometric partition of the uncertainty set to a policy count. In a finite-horizon problem, the analogue of a recourse-stable region is a cell of the measurement-history partition on which the feasible control set is constant; the bound would be `(#cells)(dim+1)`, but the paper proves it only for static integer recourse, so the transfer is a conjecture.
  - (b) The partition is induced by constraint hyperplanes, not by vertex simplicity; it is a complementary geometric decomposition to Dai-Ho's tangent-cone condition. For a vertex-list `Z`, the regions are cells of the arrangement of hyperplanes generated by all recourse actions.
  - (c) The design variable becomes the region cover: a coarser information structure means fewer stable regions, hence a smaller `k`; this is the most direct formal analogue of designing the closure set.

### def-kurtz-9 — recourse-stable region

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 9
- printed_page: 9
- label: Definition 9
- quote: `For a given x ∈ X a convex set D ⊂ U is called recourse-stable, if {y ∈ Y(x) : ∃ξ ∈ D s.t. A(ξ)x + B(ξ)y ≥ h(ξ)} = {y ∈ Y(x) : ∀ξ ∈ D, A(ξ)x + B(ξ)y ≥ h(ξ)} .`
- gloss: A region is recourse-stable when every recourse action is either feasible on the entire region or infeasible somewhere in it; feasibility cannot switch inside the region.
- relevance:
  - (a) Defines the finite combinatorial object that replaces a continuum of scenarios; a closure-moment analogue would need an analogous "control-feasible-stable cell" definition.
  - (b) Gives a region-based alternative to vertex-based exactness; it does not require `Z` to be simple, only that the cover size `R` be finite.
  - (c) The partition is a property of the chosen first-stage `x` and the constraint system, so the information structure and the decision are coupled; this coupling is exactly the design problem the essay wants to isolate.

### thm-kurtz-17 — explicit cover-size bounds

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 14
- printed_page: 14
- label: Theorem 17
- quote: `• k ∈ O (η min{m,nξ } (nξ + 1)) if fixed recourse holds • k ∈ O (η nξ (nξ + 1)) if random recourse holds.`
- formula: fixed recourse `k ∈ O(η^{min{m,n_ξ}}(n_ξ+1))`; random recourse `k ∈ O(η^{n_ξ}(n_ξ+1))`; `η = max{1, max_{x feasible} |H(x)|}` is the maximum number of distinct constraint hyperplanes crossing `U`.
- gloss: With `η` the maximum number of distinct constraint hyperplanes crossing `U`, the cover size is `O(η^{min{m,n_ξ}})` under fixed recourse and `O(η^{n_ξ})` under random recourse, so `k` can grow exponentially in uncertainty dimension.
- relevance:
  - (a) This is the only place in the batch where the bound is explicitly exponential in a dimension; it shows that a "regions × (dim+1)" bound can be much larger than a linear policy count. For closure moments, the analogous exponential would be in the number of measurable cells, not in `T` per se.
  - (b) `η` is computed from hyperplanes generated by all recourse actions; for a vertex-list `Z`, this is an arrangement count, not a simplicity count. A simple polytope can still have a large `η`.
  - (c) The design lever is the number of distinct constraint patterns, i.e., how much information the recourse action is allowed to depend on.

### rem-kurtz-19 — rank refinement

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 14
- printed_page: 14
- label: Remark 19
- quote: `ω := max x∈X rank (A(x)) ≤ min{m, nξ }, leading to the bound k ∈ O (ηω (nξ + 1)) in case of fixed recourse`
- formula: `k ∈ O(η^{ω}(n_ξ+1))`, `ω = max_{x∈X} rank(A(x)) ≤ min{m,n_ξ}`.
- gloss: The fixed-recourse exponent can be tightened from `min{m,n_ξ}` to the actual maximum rank `ω` of the coefficient matrix.
- relevance:
  - (a) A rank-based refinement, not a moment count; it suggests that effective dimension, not nominal dimension, controls the policy count.
  - (b) For vertex-list `Z`, the relevant rank is that of the constraint-coefficient matrix, which is independent of vertex count; this is a useful separation between geometry and dimension.
  - (c) The design variable is now the effective rank of the information-dependent constraint system.

### thm-kurtz-26 — approximation under constraint uncertainty

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 18
- printed_page: 18
- label: Theorem 26
- quote: `Then, for any s ∈ N with s ≤ nξ + 1 it holds opt(Rs) − opt(2RO) ≤ Ldiam(Y)ln ( nξ + 1 s ) .`
- formula: `opt(Rs) - opt(2RO) ≤ L·diam(Y)·ln((n_ξ+1)/s)`, for `1 ≤ s ≤ n_ξ+1`; the same bound extends to `k ∈ {Rs+1, ..., Rs+R−1}` by monotonicity.
- gloss: Below the constraint-uncertainty bound, using `s` policies per stable region yields the same logarithmic loss in `(n_ξ+1)/s`.
- relevance:
  - (a) A per-region analogue of Theorem 7; if closure cells replace stable regions, the loss would be logarithmic in the per-cell policy deficit, not in the number of moments.
  - (b) No simplicity condition; the geometry enters only through `R`.
  - (c) The design trade-off is per-cell resolution versus total policy budget `Rs`.

### thm-kurtz-29 — NP-completeness of k-equivalence

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 20
- printed_page: 20
- label: Theorem 29
- quote: `The k-equivalence problem is NP-complete, even if the uncertainty only appears in the objective function.`
- gloss: Deciding whether `k` policies suffice for exact equivalence is NP-complete even with objective-only uncertainty, via reduction from set cover.
- relevance:
  - (a) Warns that any exact "minimal number of information cells" computation is likely intractable in general; the essay should target bounds and approximations, not exact minima.
  - (b) The reduction uses a finite uncertainty set and a set-cover structure, not a vertex-simplicity condition.
  - (c) The design problem "choose the smallest information structure achieving exactness" inherits set-cover hardness in this encoding.

### fact-kurtz-abstract-np — optimization form is NP-hard

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 1
- printed_page: 1
- label: Abstract (p. 1)
- quote: `for finite uncertainty sets we show that calculating the minimal k for which k-adaptable and two-stage problems are equivalent is NP-hard`
- gloss: The optimization form — finding the minimal exact `k` — is NP-hard for finite uncertainty sets, not merely the decision form.
- relevance:
  - (a) Same hardness warning as Theorem 29, stated for the optimization version.
  - (b) Finite `U`; no geometric simplicity hypothesis.
  - (c) The minimal information-structure design problem is hard in the same encoding.

### thm-kurtz-30 — greedy approximation of minimal k

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 21
- printed_page: 21
- label: Theorem 30
- quote: `Algorithm 1 calculates a value kub with kub ≤ (1 + ln (t)) kopt where kopt is the minimum value for k for which (2RO-C) and (k-ARO-C) have the same optimal value.`
- formula: `k^{ub} ≤ (1 + ln t) k^{opt}`; lower bound `k^{lb} = ceil(t / opt(U)) ≤ k^{opt}` (Remark 31, pp. 21-22).
- gloss: A greedy set-cover procedure returns a policy count within a factor `1+ln(t)` of the minimal exact count when there are no first-stage decisions.
- relevance:
  - (a) An approximation algorithm for the *count*, not for the objective; the same set-cover shape would apply to a minimum-cell selection problem.
  - (b) No vertex geometry; the universe is the finite scenario set.
  - (c) The design variable is a selected set of policies covering the scenarios, which is structurally close to selecting closure cells covering a path set.

### ex-kurtz-4 — tightness of the objective bound

- file: `corpus/intake/2409.12630.pdf`
- sha256: `839e69a9e241e5a15acf141398530b0dbf4bae5fcf6ac64737988731e73433c1`
- pdf_page: 6
- printed_page: 6
- label: Example 4 (and sentence before it)
- quote: `This shows that we need at least k = nξ solutions for optimality.`
- gloss: A simplex-like instance needs `n_ξ` policies, so the `n_ξ+1` bound is tight up to an additive one.
- relevance:
  - (a) Shows the linear-in-dimension count cannot be improved in general; a closure-moment analogue would need a comparable lower-bound example.
  - (b) The instance uses a simplex `U` and unit-vector recourse, i.e., a very simple polytope; the lower bound is not driven by non-simplicity.
  - (c) The design budget `k` is forced by the geometry of the scenario simplex.

---

## 2. Dai & Ho (2026): simplicity as the exact geometric condition

The paper resolves an open question in Bertsimas, Shtern & Sturt (2022): whether the technical
condition A4b (local affine feasibility at every vertex) follows from the mild global feasibility
condition A4a. It reformulates the question as: for a globally feasible recourse system
`W y + H ξ ≥ b` on a polyhedron `Ξ`, when is it also locally linear feasible at every vertex?
The answer is a dichotomy governed by whether `Ξ` is a simple polyhedron.
Scope note: every result below is a feasibility/existence statement about affine policies; none
states that an affine policy attains the optimal value of a two-stage robust objective, and none
gives a policy or moment count.

### def-daiho-simple — definition of simple

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 3
- printed_page: 3
- label: prose definition in the Introduction (p. 3); term used in Corollary 1 and throughout
- quote: `A polyhedron is called simple when every vertex meets exactly as many edges as the ambient dimension, which coincides with vertex non-degeneracy in the sense of linear programming.`
- gloss: A polyhedron is simple if every vertex has exactly `dim(Ξ)` incident edges — the linear-programming non-degeneracy condition (the printed definition says "ambient dimension"; Theorem 2 uses `dim(Ξ)` and reduces the lower-dimensional case by an affine map, so `dim(Ξ)` is the operative count).
- relevance:
  - (a) A purely geometric vertex condition; it counts edges, not policies, moments, or scenarios.
  - (b) This is the exact condition the essay needs for vertex-represented `Z`: simplicity is checkable from vertex/edge incidence, and it is the necessary-and-sufficient geometric obstruction for the local-to-global affine feasibility implication.
  - (c) Geometry is the design lever: choosing a simple support makes the technical condition automatic; choosing a non-simple support requires a per-vertex certificate.

### thm-daiho-dichotomy — the exact dichotomy

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 1
- printed_page: 1
- label: Abstract (p. 1); proved as Theorem 2 (sufficient direction) and Theorem 4 (necessary direction)
- quote: `When the support set is simple, the technical condition is automatic, and asymptotic optimality holds under the remaining standard assumptions. When the support set is not simple, there exists a problem instance on which the technical condition fails, and asymptotic optimality breaks down.`
- formula: simple `Ξ` ⇒ `A4b` follows from `A4a` for every recourse system; non-simple `Ξ` ⇒ some `(W,H,b)` with `A4a` true and `A4b` false at that vertex.
- gloss: The dichotomy is exact: simplicity is both sufficient for the technical condition to be automatic and necessary for it to be automatic uniformly over all recourse systems on the support.
- relevance:
  - (a) No policy or moment count; the dichotomy is about feasibility and asymptotic optimality in sample size, not about a finite information budget.
  - (b) This is the exact geometric criterion for vertex-represented supports: check simplicity of `Ξ`; if simple, affine feasibility is automatic, if not, a counterexample exists but must be constructed. It still does not assert objective-optimality of the affine rule.
  - (c) The support geometry is the design variable; the information structure (affine policy after observing `ξ`) is fixed.

### fact-daiho-a4b — the technical condition

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 8
- printed_page: 8
- label: condition A4b in Theorem 1 (restating Bertsimas et al. 2022)
- quote: `For the same x ∈ Rn as in A4a and for some ϵ > 0, at every vertex ζ0 of Ξ there exists an affine policy yζ0 (·) ∈ L such that T x + W yζ0 (ζ) ≥ h(ζ) ∀ ζ ∈ Ξ ∩ B(ζ0 , ϵ).`
- gloss: A4b demands one common first-stage `x` and, at every vertex, an affine policy feasible on a support neighborhood.
- relevance:
  - (a) A local affine-feasibility condition, not a count of moments or policies.
  - (b) It is exactly the property that a vertex-list affine rule must satisfy near each vertex; the paper's dichotomy says when this is automatic.
  - (c) The information structure is fixed (observe all of `ξ`); the design question is whether the support geometry makes the fixed affine information structure sufficient.

### def-daiho-2 — global vs local linear feasibility

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 9
- printed_page: 9
- label: Definition 2
- quote: `Moreover, the recourse system is called locally linear feasible at the vertex ζ0 if the above policy can be selected as y(·) ∈ L.`
- gloss: Local linear feasibility means an affine policy works on a small neighborhood of the vertex, not merely a pointwise feasible recourse action.
- relevance:
  - (a) Distinguishes pointwise feasibility from affine representability; no moment count.
  - (b) This is the precise local notion that a vertex-list LDR must satisfy; it is weaker than global affine feasibility and stronger than global feasibility.
  - (c) The information structure is the affine map `y(ξ)=y0+Yξ`; the question is where it is valid.

### thm-daiho-2 — sufficient direction: p = dim(Ξ)

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 11
- printed_page: 11
- label: Theorem 2
- quote: `Let ζ0 be any vertex of Ξ, and suppose there are p edges incident to the vertex ζ0 on Ξ. If p = dim(Ξ), then any globally feasible system (4) on Ξ is also locally linear feasible at ζ0.`
- formula: `p = dim(Ξ)` at the vertex `ζ0`.
- gloss: At any vertex with exactly `dim(Ξ)` incident edges, global recourse feasibility forces an affine policy that is feasible in a neighborhood of that vertex.
- relevance:
  - (a) No policy or moment count; the local edge count is the only combinatorial input.
  - (b) This is the core positive result for affine exactness on vertex lists: at a non-degenerate vertex, global feasibility already yields a local affine certificate. It is a feasibility result, not an optimal-value result.
  - (c) The design lever is local support geometry: a vertex with the right number of incident edges makes the affine information structure locally sufficient.

### cor-daiho-1 — simple support gives asymptotic optimality

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 13
- printed_page: 13
- label: Corollary 1
- quote: `A direct consequence of Theorem 2 is that, if Ξ is a simple polyhedron, then the technical assumption A4b in Theorem 1 is satisfied when the milder assumption A4a is imposed.`
- formula: `lim_{N→∞} v̂_N^{SRO} = lim_{N→∞} v̂_N^{MP} = v*` a.s., plus accumulation-point optimality, under A1-A3 and A4a.
- gloss: If the support is simple, A4b follows from the mild global-feasibility condition A4a, so the Bertsimas-Shtern-Sturt asymptotic optimality theorem applies without extra checks.
- relevance:
  - (a) The conclusion is asymptotic in sample size `N`, not a finite policy count.
  - (b) This is the strongest positive statement for vertex-represented supports: simplicity of `Ξ` removes the technical condition entirely. It is about existence of affine policies, not about their objective optimality at finite `N`.
  - (c) The support geometry is the design variable that makes the fixed affine information structure asymptotically sufficient.

### prop-daiho-1 — translated simplicial cone yields a global LDR

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 10
- printed_page: 10
- label: Proposition 1
- quote: `Moreover, the locally linear feasible policy can be selected globally, which serves as a feasible linear decision rule y(·) on Ξ.`
- gloss: On a translated simplicial cone, global feasibility yields a single affine rule feasible on the whole support — an exact LDR feasibility result, not an objective-optimality result.
- relevance:
  - (a) No count; the result is about one affine rule on an unbounded cone.
  - (b) The strongest affine-feasibility statement in the batch: a simplicial-cone support admits a globally feasible LDR. It still does not claim that the LDR attains the optimal value of a two-stage robust objective.
  - (c) The information structure is a single affine map on the whole support; the geometry (simplicial cone) is what makes it sufficient.

### thm-daiho-3 — explicit 3-D counterexample

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 15
- printed_page: 15
- label: Theorem 3
- quote: `Then (4) is globally feasible on Ξ, but not locally linear feasible at the vertex ζ0 = 0.`
- formula: `m=4`, `r=1`, `d=3`; `W = [1, 1, -1, -1]^T`; `H` as printed on p. 15; `b = 0`; `Ξ = conv{0,p_1,...,p_7}`, `p_j = [cos θ_j, sin θ_j, 1]^T`, `θ_j = 2π(j-1)/7`; the origin is the unique non-simple vertex with seven incident edges.
- gloss: An explicit 3-D support with one non-simple vertex and a 4-by-1 recourse system that is globally feasible but admits no affine policy near that vertex.
- relevance:
  - (a) No count; the failure is local and geometric.
  - (b) This is a concrete negative instance for affine feasibility on a vertex list: a single non-simple vertex can destroy local affine representability even when every scenario is pointwise feasible.
  - (c) The support geometry is fixed; the failure is a property of the recourse system, not of an information-design choice.

### thm-daiho-4 — every non-simple support admits such a system

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 23
- printed_page: 23
- label: Theorem 4 (Structural impossibility theorem)
- quote: `For any polyhedron Ξ satisfies Assumption 1, there exists W , H and b such that (4) is globally feasible on Ξ but not locally linear feasible at ζ0 .`
- gloss: Every full-dimensional polyhedron with a vertex of degree greater than `dim(Ξ)` admits some recourse system with the same global-but-not-local-affine failure.
- relevance:
  - (a) No count; it is a structural existence theorem.
  - (b) This is the necessary direction of the dichotomy: non-simplicity is not merely sufficient to allow failure, it is unavoidable for some recourse system. It gives a sharp geometric obstruction for vertex-list affine exactness.
  - (c) The design lever is again the support geometry; the recourse system is constructed after the geometry is fixed.

### cor-daiho-2 — embedding into a two-stage stochastic LP

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 20
- printed_page: 20
- label: Corollary 2
- quote: `Then problem (9) satisfies assumptions A2, A3, and A4a of Theorem 1 but violates A4b.`
- gloss: The counterexample embeds in a two-stage stochastic LP satisfying A2, A3, A4a but violating A4b, so the technical condition is not redundant.
- relevance:
  - (a) An existence counterexample, not a count.
  - (b) It shows that the geometric obstruction survives the embedding into the full stochastic program; for vertex-list `Z`, this is a direct warning that global feasibility does not imply affine representability.
  - (c) The information structure remains fixed; the failure is in the support geometry and the recourse system.

### fact-daiho-caveat — non-simple does not mean always false

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 24
- printed_page: 24
- label: prose after Theorem 4 (p. 24)
- quote: `However, this dichotomy does not mean that A4b always fails on non-simple supports. It only shows that A4b is no longer automatic from A4a.`
- gloss: Non-simple supports make A4b non-automatic, but not necessarily false; a given recourse system may still admit local affine policies.
- relevance:
  - (a) A scope limitation: non-simplicity does not by itself force a policy-count blow-up.
  - (b) Crucial for the essay: a non-simple vertex list does not refute LDR exactness for every problem; it only removes the automatic implication. Any counterexample must construct the recourse system as well as the geometry.
  - (c) The design question becomes per-instance verification, which is exactly what the algorithm addresses.

### lemma-daiho-1 — Farkas certificate on vertices and extreme rays

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 9
- printed_page: 9
- label: Lemma 1
- quote: `The recourse system (4) is globally feasible if and only if every μ ∈ Rm + with W ⊤μ = 0 satisfies μ⊤Hvℓ ≥ 0 and μ⊤(b − Hζs) ≤ 0 ∀ℓ ∈ [L], s ∈ [S],`
- gloss: Global feasibility has an exact Farkas certificate involving only the vertices `ζ_s` and extreme rays `v_ℓ` of the support's recession cone.
- relevance:
  - (a) A finite certificate, but no count of policies or moments.
  - (b) Directly usable for vertex-represented `Z`: it reduces a continuum feasibility check to finitely many inequalities at vertices and extreme rays. This is the cleanest "vertex list is enough" result in the batch.
  - (c) The information structure is not designed here; the certificate is a verification tool for a fixed support.

### lemma-daiho-3 — Riesz interpolation holds exactly for simplicial cones

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 22
- printed_page: 22
- label: Lemma 3(c)
- quote: `The cone C is a simplicial cone; that is, there are exactly d linearly independent edges of C incident to 0, or d linearly independent extreme rays of C.`
- gloss: The Riesz interpolation property — two lower bounds below two upper bounds always admit an intermediate vector — holds exactly for simplicial cones.
- relevance:
  - (a) A purely order-theoretic/geometric characterization; no count.
  - (b) This is the engine of the dichotomy: the tangent cone at a non-simple vertex is not simplicial, so the dual order lacks interpolation, which is exactly what constructs the recourse system that is globally feasible but not locally affine.
  - (c) The design lever is the local cone geometry; no information-structure design is involved.

### thm-daiho-5 — polynomial-time certification

- file: `corpus/intake/2608.22999.pdf`
- sha256: `b483a459aa26c27d86d82f4855ffd45b1098f2acaaa28685f4026c70f101383f`
- pdf_page: 28
- printed_page: 28
- label: Theorem 5 (parts (a)-(c); the quoted sentence is part (b))
- quote: `The algorithm solves at most (m + 2)(m + 1)/2 linear programs, each with at most rd + r + 1 decision variables and mL + m + 1 constraints, hence of size polynomial in (m, r, d, L).`
- formula: at most `(m+2)(m+1)/2` LPs; `rd+r+1` variables; `mL+m+1` constraints; at most `m` iterations; input = `W, H, b`, vertex `ζ0`, and the `L` incident edge directions; part (c) is correctness.
- gloss: Given the local edge directions, at most `(m+2)(m+1)/2` LPs of polynomial size decide local linear feasibility, so certification is polynomial in `(m,r,d,L)`.
- relevance:
  - (a) A complexity result for verifying affine feasibility, not for counting moments.
  - (b) For vertex-list `Z`, this gives a per-vertex certificate of local affine representability; total cost over all vertices is dominated by the number of vertices, not by the per-vertex LP.
  - (c) The verification uses only local geometric information, so the support geometry is the input to the design/verification loop.

---

## 3. Tsang, Shehadeh & Curtis (2022): delta against the processed report

The paper is already processed in
`reports/reading/2026-10-11-tsang-shehadeh-curtis-2022.md` (hereafter "the processed report").
This section deliberately does **not** re-register its eight blocks. It adds only the two items
requested by the essay task: the exact multiplicative certificate and the scope limit regarding
decision-rule exactness. All four numbered claims below were independently re-read in the intake
PDF and matched against the processed report.

### thm-tsang-prop2 — multiplicative error budget

- file: `corpus/intake/2207.03291.pdf`
- sha256: `cff68fa585627e330cea15838408aca67d0b7fe87f80a621e680f243620930ec`
- pdf_page: 7
- printed_page: 7
- label: Proposition 2
- quote: `then the actual relative gap is at most (1 − ε̃)−1 ∏j k=`(1 − εk M P )−1 − 1.`
- formula: `(U - L^ℓ)/U ≤ (1-ε̃)^{-1} ∏_{k=ℓ}^{j} (1-ε_{MP}^k)^{-1} - 1`, under the exploitation-step conditions `(U-L^ℓ)/U ≥ ε` and `(U-U^j)/U < ε̃`.
- gloss: The true relative gap is bounded by the product of per-master inexactness factors and the backtracking threshold — a multiplicative error budget.
- relevance:
  - (a) The budget is over solver tolerances, not over the number of scenarios or moments; it gives no closure-count bound.
  - (b) No affine-rule or vertex-geometry content.
  - (c) The design variable is the tolerance schedule `{ε_{MP}^k}` and the backtracking threshold `ε̃`, i.e., how much information about the master's true optimum is allowed to be lost.

### thm-tsang-cor3 — one-step budget

- file: `corpus/intake/2207.03291.pdf`
- sha256: `cff68fa585627e330cea15838408aca67d0b7fe87f80a621e680f243620930ec`
- pdf_page: 8
- printed_page: 8
- label: Corollary 3
- quote: `then the actual relative gap is at most (1 − ε̃)−1(1 − εj M P )−1 − 1.`
- formula: `(1-ε̃)^{-1}(1-ε_{MP}^j)^{-1} - 1`, when step 1.3 updates `L` to `L^j` instead of `U^j`.
- gloss: If the lower bound is updated conservatively, the budget collapses to two factors: the backtracking threshold and the current master tolerance.
- relevance:
  - (a) A two-factor special case; still no count of scenarios or moments.
  - (b) No geometric content.
  - (c) The design choice is the lower-bound update rule, which determines how many factors enter the budget.

### thm-tsang-thm4 — finite convergence threshold

- file: `corpus/intake/2207.03291.pdf`
- sha256: `cff68fa585627e330cea15838408aca67d0b7fe87f80a621e680f243620930ec`
- pdf_page: 8
- printed_page: 8
- label: Theorem 4
- quote: `If ε̃ < ε/(1 + ε), then Algorithm 2 terminates in a finite number of iterations.`
- formula: `ε̃ < ε/(1+ε)`; the subproblem oracle is exact, only master solves are inexact; `Ξ` finite or a polytope.
- gloss: Choosing the inexact-gap threshold below `ε/(1+ε)` guarantees finite termination.
- relevance:
  - (a) Finiteness, not a quantitative bound: the number of exploration steps is finite because `ext(Ξ)` is finite, but no formula in `|ext(Ξ)|` is given.
  - (b) No affine-rule or vertex-simplicity content.
  - (c) The design variable is the tolerance schedule; the scenario set is grown by the adversary, not chosen by the designer.

### scope-tsang-1 — what the exactness claim does not cover

- file: `corpus/intake/2207.03291.pdf`
- sha256: `cff68fa585627e330cea15838408aca67d0b7fe87f80a621e680f243620930ec`
- pdf_page: 9
- printed_page: 9
- label: Remark 4
- quote: `By setting the actual relative gap tolerance to ε = 0, our i-C&CG method converges to the exact optimal solution to (1).`
- related quote (p. 3): `Adding a new scenario in the master problem is equivalent to adding new second-stage variables and constraints.`
- gloss: Exactness here is exactness of the column-generation solution over full per-scenario recourse variables; it is not a statement that an affine or any other parametric decision rule is exact.
- relevance:
  - (a) The paper never bounds the number of columns/scenarios needed for exactness; it only proves finiteness under a finite-extreme-point assumption (p. 9: "the number of exploration steps is finite"). Therefore it cannot supply a closure-moment count.
  - (b) The paper has no affine-rule exactness theorem. The only occurrence of "decision rule" is a citation of prior work that used linear decision rules as an approximation (p. 11: `developed linear decision rules to approximate solutions to problem instances`). No vertex-list or simple-polytope geometry appears.
  - (c) The information structure is the scenario set `S`: exploration adds a worst-case scenario, exploitation re-solves with tighter tolerance. The design variable is which scenarios enter the master, not when the controller observes the state.

---

## 4. Verification against the processed Tsang report

- Mapping of labels (verified against the intake PDF):
  - processed `thm-prop-1` = printed **Theorem 4** (finite convergence, `ε̃ < ε/(1+ε)`).
  - processed `thm-prop-2` = printed **Proposition 1** (valid lower bound `L^ℓ ≤ υ*`).
  - processed `thm-prop-3` = printed **Proposition 2** (multiplicative budget).
  - processed `thm-prop-4` = printed **Corollary 3** (one-step budget).
- The processed report's formulas for `thm-prop-3` and `thm-prop-4` match the PDF exactly; its
  finite-convergence threshold matches Theorem 4; its valid-lower-bound statement matches
  Proposition 1. No mathematical contradiction found.
- Label correction: the processed report cites "their Prop. B.1" for the pinned-value lemma.
  In the PDF, Appendix B is titled "Proof of Proposition 1", and the lemma itself is printed as
  **Proposition 5** (p. 15). The printed label is Proposition 5; "B.1" does not match the printed
  numbering. This is a citation-label correction, not a change in the statement.
- The processed report's meta says no arXiv id is visible in the LaTeX source. The intake PDF's
  first-page footer gives `arXiv:2207.03291v2 [math.OC] 5 Nov 2022`; this is an addition, not a
  contradiction.
- Not duplicated here: the problem class and standing assumptions, the C&CG generalization
  relation, the exactness-at-ε=0 fact, the finite-extreme-point inheritance, the exploration-step
  monotonicity, the DRO reductions, the three-point DRORSP structure, the MILP reformulations,
  and the landscape. The essay does not need them for the certificate/no-rule point.

---

## Marginal notes

- **Attack the policy-count-to-closure-count transfer directly.** Kurtz Theorem 2 gives the
  exact shape `k ≥ n_ξ+1` for integer recourse under convex uncertainty, while Theorem 11 gives
  `k ≥ min{R(n_ξ+1), |Y|}` for constraint uncertainty. Neither variable is a moment count. The
  cleanest attack is to instantiate the bridge with a small horizon, enumerate all optimal
  contingent controls, and test whether the number of distinct controls needed per
  measurement-history cell behaves like `dim(state)+1`; if it does, the essay has a genuine
  k-adaptability-type analogue, and if it does not, the analogy is dead and should be stated as
  such.

- **Separate feasibility from objective exactness using Dai-Ho.** Dai-Ho proves exact affine
  *feasibility* results: Proposition 1 (simplicial cone, global LDR), Theorem 2 (simple vertex,
  local affine), Corollary 1 (simple support, asymptotic optimality). None of them says an
  affine rule attains the optimal value of a two-stage robust objective. For the essay this is a
  precise separation: Dai-Ho closes the feasibility half of the LDR question on vertex lists,
  leaving the objective half open. That is a publishable sharpening of `conj-ldr-exactness`.

- **Use non-simplicity as a targeted counterexample generator, not as a blanket impossibility.**
  Theorem 4 guarantees a bad recourse system at every non-simple vertex, but the page-24 caveat
  says A4b may still hold for a given system; their Table 1 shows exactly this, with non-simple
  budgeted instances on which A4b still holds. The attack is therefore two-stage: first check
  simplicity of `Z` (boxes are simple; generic budgeted sets may not be), then, only at
  non-simple vertices, run the `(m+2)(m+1)/2`-LP certificate. A failure there is a real
  counterexample; a success is a positive instance, not a refutation of the geometry.

- **Compose the two quantitative budgets.** Tsang's `(1-ε̃)^{-1} ∏(1-ε_{MP}^k)^{-1} - 1` is
  multiplicative in solver tolerances; Kurtz's `L·diam(Y)·ln(k/s)` is additive in objective value.
  A two-part error ledger for the ladder — policy/closure truncation (log) plus solver
  inexactness (product) — is attackable as a lemma with explicit constants, and the bridge
  judge can test whether the product bound is tight on the existing grids.

- **Target bounds, not exact minimal designs, because the exact problem is hard.** Kurtz
  Theorem 29 (NP-complete `k`-equivalence, even objective-only) and the abstract's NP-hardness
  statement rule out a general exact algorithm for the minimal policy count. The essay should
  therefore frame the closure-set design problem as a bounds/approximation problem (Theorem 7,
  Corollary 8, Theorem 26, Theorem 30) and, if it wants a hardness result of its own, reduce
  set cover to "minimum closure set achieving the full-information bridge value" rather than
  attempting an exact characterization.
