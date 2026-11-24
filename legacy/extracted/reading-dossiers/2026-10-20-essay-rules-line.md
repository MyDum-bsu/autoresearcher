# Reading proposal for the essay; blocks NOT yet registered in the science graph.

Status: proposal only. No blocks registered, no judge run, no graph mutation.
Method: `pdftotext -layout` on the three corpus PDFs; printed page numbers checked against the page headers. Superscripts and Greek letters are rendered in ASCII where extraction loses typography. Hashes are the first 64 hex characters of the corresponding lines in `corpus/MANIFEST.md`.

Corpus copies used:
- `09_Marandi_denHertog_2018.pdf` — journal typeset copy, Math. Program. Ser. A (2018) 170:555–568. PDF page = printed page − 554.
- `21_Zhen_denHertog_Sim_2018.pdf` — ResearchGate manuscript copy of "Adjustable Robust Optimization via Fourier–Motzkin Elimination" (Operations Research, July 2018, DOI 10.1287/opre.2017.1714). Its printed page numbers are 1–29, not the journal's 1086–1100; anchors below use the printed numbers in this copy. PDF page = printed page + 1.
- `22_deRuiter_Zhen_denHertog_2018.pdf` — manuscript copy, printed pages 1–11 plus E-Companion. PDF page = printed page.

---

## 1. Marandi & den Hertog 2018 — when are static and adjustable robust problems equivalent?

### 09-c1 — the recourse-matrix boundary of affine tractability
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 2
- `printed_page:` 556
- `quote:` "For linear ARO problems with fixed recourse, using affine decision rules leads to a robust linear problem that is computationally tractable for many types of uncertainty sets. This is not the case for problems with non-fixed recourse."
- `gloss:` Affine decision rules preserve tractability when the recourse matrix is fixed, and fail to do so when the recourse matrix is uncertain.
- `relevance:` (i) Locates the exact boundary of the affine rule class on the recourse side; (ii) tells us which reformulations are certifiable LPs and which are not; (iii) the bridge class with scalar control and fixed state matrix sits on the tractable side of this line, so affine is at least computable there, though not necessarily exact.

### 09-c2 — the variable price of affine rules
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 2
- `printed_page:` 556
- `quote:` "for a problem with n adjustable variables and l uncertain parameters, applying affine decision rules means substituting n adjustable variables with n(l + 1) non-adjustable variables."
- `gloss:` The affine rule class is bought by expanding every adjustable variable into an intercept plus one coefficient per uncertain coordinate.
- `relevance:` (ii) This is the baseline size of the affine relaxation against which any non-affine class must be priced; (iii) for a scalar control n is small, so the multiplier is l + 1 coefficients per stage rather than n(l + 1), which keeps the affine LP compact but does not make it exact.

### 09-c3 — the affine gap is cited, not derived
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 2
- `printed_page:` 556
- `quote:` "In [7], a bound is derived for the gap between the objective value of the problem that results from using affine decision rules and that of the ARO problem."
- `gloss:` The paper only points to an existing error bound for affine rules; it states no formula, constant, or rate of its own.
- `relevance:` (ii) A gap bound is available in the literature but not instantiated here, so a new result specializing it to fixed-recourse vertex uncertainty would be a genuine addition rather than a restatement; (iii) the bridge class needs exactly such an instantiated bound if affine rules are to be used as a certified baseline.

### 09-c4 — no uncertain equalities, and the hidden rule imposed by elimination
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 5
- `printed_page:` 559
- `quote:` "Notice that problem (1) does not contain any equality constraint that depends on ζ . The usual way of dealing with such uncertain equalities in (A RC) is to eliminate adjustable variables [14, Section 7]. This means that we are implicitly forcing the adjustable variables that are eliminated to obey specific decision rules."
- `gloss:` The equivalence theory excludes ζ-dependent equality constraints; eliminating adjustable variables from such equalities silently restricts the admissible decision rules.
- `relevance:` (i) This is a hard boundary on which static/affine exactness theorems may be applied; (ii) it warns that an elimination-based reduction can change the rule class without saying so; (iii) state equations with uncertain right-hand sides are exactly the case excluded here, so this theorem cannot be used directly on a dynamic bridge class.

### 09-c5 — constraint-wise uncertainty makes the static rule exactly optimal
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 6
- `printed_page:` 560
- `quote:` "If problem (1) has constraint-wise uncertainty and Assumptions i–vii hold, then O pt (RC) = O pt (A RC)."
- `gloss:` Under constraint-wise uncertainty plus convexity in the adjustable variables, concavity in the uncertain parameters, and convex compact domains, the static robust solution is exactly optimal for the adjustable problem.
- `relevance:` (i) A non-affine exactness result in the sense that the optimal rule can be constant, a strict sub-class of affine rules; (ii) the adjustable problem collapses to a static robust problem; (iii) it identifies the structural reason a bridge class would lose all value from adaptivity, namely block-separable (constraint-wise) uncertainty.

### 09-c6 — fixed recourse plus constraint-wise uncertainty is enough for static exactness
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 6
- `printed_page:` 560
- `quote:` "For a problem with fixed recourse and constraint-wise uncertainty, Assumption ii implies equality of the objective values of (RC) and (A RC)."
- `gloss:` With fixed recourse and compact constraint-wise uncertainty, static and adjustable worst-case values coincide.
- `relevance:` (i) Exactness of the constant rule under a fixed-recourse hypothesis; (ii) the static counterpart is the computable object; (iii) the bridge class is fixed-recourse, but its uncertainty couples the terminal constraint, so this sufficient condition is not met.

### 09-c7 — exactness does not buy polynomial time
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 6
- `printed_page:` 560
- `quote:` "Even though in this case the resulting (RC) is N P-hard in general, there are cases for which (RC) is tractable, for instance see [3, Section 1.4]."
- `gloss:` Exact reduction to a static robust counterpart can still leave an NP-hard problem; tractability requires additional structure.
- `relevance:` (ii) A caution for any "exact reformulation" claim: exactness and certifiable polynomial computation are separate properties; (iii) the bridge class needs a tractability argument for the static counterpart, not only an equality of optimal values.

### 09-c8 — the rule-class gap ordering
- `file:` corpus/09_Marandi_denHertog_2018.pdf
- `sha256:` 59c56d0aac12d2d6d00a643f14622c3128e06ccc88d6f0580d91748b0d2a8ab7
- `pdf_page:` 11
- `printed_page:` 565
- `quote:` "Then, in general, for problem (H RC), we have O pt (H A RC) ≤ O pt (A A RCζ,α ) ≤ O pt (A A RCα ) ≤ O pt (H RC)."
- `gloss:` Full adjustability is no worse than affine rules in all uncertain parameters, which is no worse than affine rules only in the non-constraint-wise parameters, which is no worse than static rules; the paper states that these inequalities can be strict and gives examples in its supplement.
- `relevance:` (i) A clean ordering of where restricting the rule class costs value; (ii) each intermediate object is a computable affine/static relaxation, so the chain is a certificate ladder; (iii) for the bridge class, this says that dropping dependence on constraint-wise blocks is free only under the corollary conditions, not in general.

---

## 2. Zhen, den Hertog & Sim 2018 — adjustable robust optimization via Fourier–Motzkin elimination

### 21-c1 — exact solution of fixed-recourse ARO is claimed
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 24
- `printed_page:` 23
- `quote:` "We propose a generic FME approach for solving ARO problems with fixed recourse to optimality."
- `gloss:` Fourier–Motzkin elimination is presented as an exact method for fixed-recourse adjustable robust optimization, not merely as an approximation scheme.
- `relevance:` (i) The exact class is the full adjustable class, represented after elimination by piecewise affine rules; (ii) an exact algorithm, subject to the size limits below; (iii) fixed recourse is the same hypothesis as the bridge class, so the method is applicable in principle.

### 21-c2 — the constraint-count price of elimination
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 8
- `printed_page:` 7
- `quote:` "The complexity of eliminating N2 adjustable variables from M constraints via Algorithm 1 is O(M^{2^{N2}}), which is an unfortunate inheritance of FME."
- `gloss:` Eliminating all adjustable variables can blow the constraint count up as a tower exponential in the number of eliminated variables.
- `relevance:` (ii) This is the explicit computational price of exactness; (iii) a scalar control keeps N2 small, which is the favourable regime, but state variables and epigraph variables also count toward N2 in a full dynamic formulation.

### 21-c3 — partial elimination is a monotone inner-approximation ladder
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 9
- `printed_page:` 8
- `quote:` "The following theorem shows that the more adjustable variables are eliminated, the tighter the approximation becomes; if all the adjustable variables are eliminated, the set representation is exact"
- `gloss:` Eliminating a subset and imposing decision rules on the remainder yields nested inner approximations that improve monotonically and become exact at full elimination.
- `relevance:` (ii) A computable, certifiable relaxation hierarchy with a known exact limit; (iii) it gives a principled budgeted algorithm for the bridge class: eliminate as many recourse variables as the constraint budget allows, then use a rule class on the rest.

### 21-c4 — affine rules can be strictly suboptimal in a fixed-recourse instance
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 9
- `printed_page:` 8
- `quote:` "We show in §7.1 that imposing linear decision rules on yij in (P ) can lead to a suboptimal solution, whereas this equivalent reformulation produces the optimal solution."
- `gloss:` In the fixed-recourse lot-sizing network with budget uncertainty, affine rules can be suboptimal while Fourier–Motzkin elimination is exact.
- `relevance:` (i) A concrete counterexample to affine exactness in a fixed-recourse two-stage linear problem; (ii) it supplies an exact benchmark against which affine gaps can be measured; (iii) the lot-sizing network is a flow problem with fixed recourse, structurally close to a scalar-control bridge with conservation constraints.

### 21-c5 — piecewise affine optimal decision rules exist
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 11
- `printed_page:` 10
- `quote:` "There exist ODRs for Problem (1) such that yl , l ∈ [N2 ], is a convex piecewise affine function or a concave piecewise affine function, and the remaining components of y are general piecewise affine functions."
- `gloss:` For any fixed-recourse two-stage linear ARO, one adjustable variable can be chosen convex or concave piecewise affine and all remaining variables general piecewise affine without loss of optimality.
- `relevance:` (i) This is the central non-affine exactness class in the three papers; (ii) piecewise affine rules are finitely parameterized by the elimination data; (iii) an l1 terminal cost is itself piecewise linear, so this rule class matches the kink structure of the objective.

### 21-c6 — the piecewise-affine result needs no geometry on the uncertainty set
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 11
- `printed_page:` 10
- `quote:` "Since we do not impose any assumption on the uncertainty set W in Problem (1), Theorem 3 holds for Problem (1) with general uncertainty sets."
- `gloss:` Piecewise-affine optimality does not require convexity, box structure, or any particular representation of the uncertainty set.
- `relevance:` (i) Directly covers a finite vertex set, which is the essay's vertex-uncertainty setting; (ii) the theorem does not enumerate vertices; (iii) this is the key reason the FME route is a plausible exactness lever for fixed-recourse vertex uncertainty.

### 21-c7 — simplex uncertainty is an affine exactness island
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 12
- `printed_page:` 11
- `quote:` "Suppose the uncertainty set Wpoly is a standard simplex. Then, there exist LDRs that are ODRs for the adjustable variables y in Problem (1)."
- `gloss:` For simplex uncertainty, affine rules are exactly optimal, so the non-affine lever is unnecessary there.
- `relevance:` (i) Delimits one exactness island for affine rules; (ii) the affine model is an LP/SOCP-sized object; (iii) a vertex set that is a simplex falls inside this island, while a box does not, so the bridge class must be classified by the geometry of its vertex set before choosing a rule class.

### 21-c8 — box uncertainty gives two-piecewise affine rules and a sum-of-max form
- `file:` corpus/21_Zhen_denHertog_Sim_2018.pdf
- `sha256:` 4dd3a2459894eefe1267516892cfd4df9d20af133484c886ccc377883b90b6c3
- `pdf_page:` 14
- `printed_page:` 13
- `quote:` "An immediate observation from Theorem 5 is that, if we eliminate all the adjustable variables in (12) via Algorithm 1, it results in a sum-of-max representation"
- `gloss:` For box uncertainty, Theorem 5 (p.12) gives two-piecewise affine hinge rules for the dual adjustable variables, and full dual elimination collapses the feasible set to one sum-of-max constraint; the paper interprets the same operation as lifting the uncertainty set into higher dimensions (p.13).
- `relevance:` (i) The exact non-affine class for box/vertex uncertainty is the two-piecewise affine hinge rule in the dual; (ii) the sum-of-max description is a convex static formulation, and the paper notes it can be solved approximately with existing techniques; (iii) the absolute-value/hinge form is the natural match for an l1 terminal cost, making this the closest template for the bridge class.

---

## 3. de Ruiter, Zhen & den Hertog 2018 — dual approach for two-stage robust nonlinear optimization

### 22-c1 — affine rules produce the wrong curvature in nonlinear recourse
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 1
- `printed_page:` 1
- `quote:` "if we substitute linear decision rules for the adjustable variables, then the model becomes convex in the uncertain parameters, whereas for computational tractability we need concavity in the uncertain parameters."
- `gloss:` In nonlinear ARO with convex adjustable terms, affine rules turn the inner worst-case problem into a convex maximization over the uncertainty set, the wrong curvature for a tractable robust counterpart.
- `relevance:` (i) Explains why affine is not even the computationally natural class when recourse is nonlinear; (ii) motivates dualization rather than direct robustification; (iii) an l1 terminal cost is convex and piecewise linear, so this curvature obstruction is live in the bridge class.

### 22-c2 — fixed recourse excludes ζ·y interaction terms
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 2
- `printed_page:` 2
- `quote:` "Note that Problem (1) has fixed recourse because the functions gi , i = 0, ..., m1 , and the matrix B do not depend on ζ. Therefore, there are no direct interaction terms between ζ and y, such as products ζ > y."
- `gloss:` Fixed recourse means the nonlinear adjustable terms and the recourse matrix are free of ζ, so the model contains no bilinear ζ·y products.
- `relevance:` (i) The class boundary under which the dual reformulation is developed; (ii) it is the structural hypothesis that makes the consecutive dual exact; (iii) state equations with a fixed B and uncertainty only in the right-hand side fit this hypothesis, including an l1 terminal cost on the terminal state.

### 22-c3 — the naive nonlinear affine model is NP-hard
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 2
- `printed_page:` 2
- `quote:` "The inner maximization problem in (5) tries to maximize a convex function over a polyhedron, which is in general NP-hard."
- `gloss:` The affine-rule nonlinear robust counterpart is NP-hard because its inner problem maximizes a convex function over a polytope.
- `relevance:` (ii) The computational price of the direct nonlinear affine route; (iii) this is the obstacle that the dual route is designed to avoid for the bridge class.

### 22-c4 — dualization turns the nonlinear problem linear in the adjustable variables
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 3
- `printed_page:` 3
- `quote:` "However, in this paper we show that the dual of the nonlinear problem is linear in the adjustable variables."
- `gloss:` Consecutive dualization produces a linear adjustable robust problem in the dual variables, so linear ARO machinery becomes applicable.
- `relevance:` (i) The exact reformulation changes the rule class to linear-in-the-dual variables; (ii) all linear ARO tools, including LDRs and FME, can then be applied; (iii) a bridge class with convex l1 terminal cost can be handled if it admits this dual form.

### 22-c5 — dualization is an exact iff reformulation, not a relaxation
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 4
- `printed_page:` 4
- `quote:` "The here-and-now decision x is feasible for (1) if and only if x is feasible for the following dualized model"
- `gloss:` Under a polyhedral uncertainty set and relatively complete recourse, the dualized model has exactly the same feasible here-and-now decisions as the original nonlinear problem.
- `relevance:` (ii) An exact, certifiable reformulation rather than an approximation; (iii) unlike the Marandi–den Hertog theorem, this route explicitly allows linear equalities containing ζ, which matters for state equations in the bridge class.

### 22-c6 — primal affine rule recovery and its one-sided value
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 6
- `printed_page:` 6
- `quote:` "If x, yj , j = 0, . . . , nζ are feasible for (8), then x, y(ζ) = y0 + Σ_{j=1}^{nζ} yj ζj is feasible for the primal linear decision rule model (1) and its objective value is at most the objective value of (8)."
- `gloss:` A primal affine rule is recovered from a feasible dual LDR solution, and the primal LDR value is no worse than the dual LDR value; the proof uses a perspective relaxation (Lemma 1, p.6), an extended Jensen inequality.
- `relevance:` (i) The recovered rule is affine, so this is not an exactness claim beyond affine; (ii) it yields a feasible primal rule plus a dual-side bound; (iii) the perspective step is what keeps l1/piecewise-linear costs conic representable, so the bridge class does not leave the cone class.

### 22-c7 — the dual LDR value can overstate the primal LDR value
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 8
- `printed_page:` 8
- `quote:` "the true objective value of the primal linear decision rule model could be lower than the value obtained of (8)"
- `gloss:` The dual LDR value is only an upper bound on the recovered primal LDR value, so the recovery step is conservative.
- `relevance:` (ii) The gap is one-sided and must be measured, not assumed away; (iii) a certified bridge-class result cannot rest on the dual value alone and needs the lower-bound side.

### 22-c8 — linked scenarios roughly halve the measured gap
- `file:` corpus/22_deRuiter_Zhen_denHertog_2018.pdf
- `sha256:` bb7fc8198f2d12a6d0df9071950e8ddfba12296f8f16ae8fcd6d3d0196d3e87e
- `pdf_page:` 10
- `printed_page:` 10
- `quote:` "For the largest instance the linked primal scenarios reduced the gap from 10.7% to 5.2%."
- `gloss:` Linking dual binding scenarios to primal scenarios roughly halved the observed optimality gap on the largest test instance.
- `relevance:` (ii) A concrete, computable certification of LDR suboptimality; (iii) the guarantee is stated for right-hand-side uncertainty (Theorem 3, pp.9–10), which is the regime a terminal-cost bridge class typically occupies, so this is a directly usable gap-measurement template.

---

## Marginal notes

**Most plausible exactness lever.** For a fixed-recourse two-stage linear ARO with vertex uncertainty, the lever proved exact in these three papers is **piecewise affine decision rules generated by Fourier–Motzkin elimination**, not polynomial or quadratic rules (the latter are only cited as related rule classes, 21 p.3). Zhen et al. prove that one eliminated adjustable variable can be chosen convex or concave piecewise affine and the rest general piecewise affine, with **no assumption on the uncertainty set** (21 p.10, Theorem 3). A finite vertex set is therefore covered without vertex enumeration in the theorem. For box uncertainty the dual specializes to **two-piecewise affine hinge rules** (21 p.12, Theorem 5) and a single **sum-of-max** static constraint (21 p.13), which the authors describe as lifting the uncertainty set into higher dimensions (21 p.13). Affine rules are not a safe substitute: their own fixed-recourse lot-sizing instance has an affine-rule solution that can be suboptimal while FME is exact (21 p.8). The other two papers mark the boundaries. Marandi–den Hertog require constraint-wise uncertainty and exclude ζ-dependent equalities for static exactness (09 pp.559–560), so a dynamic bridge class with uncertain state equations falls outside that theorem. de Ruiter–Zhen–den Hertog show that the dual route does accommodate ζ-dependent linear equalities under relatively complete recourse (22 pp.2–4), which is the right exact reformulation tool for that case.

**Computational price.** Exactness is paid for in constraints, not in a different complexity class of the data. FME constraint growth is O(M^{2^{N2}}) in the number of eliminated adjustable variables (21 p.7), so full elimination is a small-instance method (21 pp.3–4, 8). Redundant-constraint identification is required to keep the reformulation usable; an exact redundancy test can be as hard as solving the ARO itself (21 p.14, Theorem 6), and the tractable sufficient test is a static-RO heuristic (21 pp.14–15, Theorem 7). Partial elimination plus LDR on the remainder gives a monotone family of inner approximations that becomes exact only when all adjustable variables are eliminated (21 p.8, Theorem 2); the appointment-scheduling experiment reports the gap reaching zero as more variables are eliminated (21 p.23). For nonlinear recourse, dualization is exact (22 p.4, Theorem 1), but applying LDRs in the dual and recovering a primal LDR is one-sided: the true primal LDR value can be lower than the dual value (22 pp.6–8), so a certified gap needs the sampled lower-bound machinery (22 pp.9–10; 10.7% to 5.2% on the largest instance, 22 p.10). The perspective/conic step does not raise the complexity class for l1-type costs (22 p.6).

**Bridge class with scalar control and l1 terminal cost.** The scalar control is the favourable case for FME because N2 is small in O(M^{2^{N2}}); the binding dimensions become the number of constraints M and, if the uncertainty set is presented as a finite vertex list, the number of vertices, which re-enters at the final static robust LP (one constraint copy per vertex). The most promising exact route is therefore: write the l1 terminal cost as a hinge/absolute-value epigraph, dualize so that the adjustable variables are linear (22), then either eliminate the scalar control by FME and solve the resulting static robust LP over the vertices exactly (21), or, if the elimination is too large, eliminate a subset and use two-piecewise affine/hinge rules on the rest, reporting the monotone inner-approximation gap (21 p.8, p.12). A new-results target suggested by this reading is an exact hinge-rule description whose size is governed by M and N2 rather than by the number of vertices; in the FME route the vertex count is deferred to the final static constraints, not removed. The affine gap bound cited by Marandi–den Hertog (09 p.556) is not instantiated there, so specializing it to this fixed-recourse vertex-uncertainty bridge class would be a genuine addition rather than a restatement.
