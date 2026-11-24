# Reading proposal: Tsang, Shehadeh & Curtis 2022

meta: "An inexact column-and-constraint generation method to solve two-stage robust optimization problems" / Man Yiu Tsang, Karmel S. Shehadeh, Frank E. Curtis (Lehigh University) / year 2022 / venue not stated in source beyond the footer "Preprint submitted to arXiv" (ms.tex:35) and the abstract comment `% ORL: 80 words` (ms.tex:243, suggesting an Operations Research Letters submission); no arXiv id visible in the source.

## Theorem blocks

### thm-prop-1: Finite convergence of i-C&CG
- statement: If the backtracking parameter satisfies ε̃ < ε/(1+ε), then the inexact column-and-constraint generation algorithm (i-C&CG) terminates in a finite number of iterations. Combined with the closing remark: setting the actual relative gap tolerance ε = 0 makes the method converge to the exact optimal solution υ* of the two-stage RO problem.
- conditions: Two-stage robust problem (2) with uncertainty set Ξ either finite or a polytope (finitely many extreme points), relatively complete recourse, finite optimum, and the subproblem solved exactly by an optimality oracle at each iteration; master problems solved only to relative gap ε_MP^j ∈ (0,1) with the backtracking routine (exploitation: j←ℓ, L̄←L^ℓ, ε_MP^k ← α ε_MP^k for k ≥ ℓ, α ∈ (0,1)).
- anchor: ms.tex:483-485 — `If $\epst<\varepsilon/(1+\varepsilon)$, then Algorithm \ref{algo:inexact_C&CG} terminates in a finite number of iterations.`
- our-relevance: This is exactness-by-finite-column-generation, not structural exactness of a decision rule: it delimits conj-ldr-exactness (an affine rule being exact is a different mechanism, independent of how many scenarios the master has seen), and its ε̃ < ε/(1+ε) threshold is a certificate-style condition germane to our LP budget/certificates line.

### thm-prop-2: Validity of the best tracked lower bound L^ℓ
- statement: At any iteration of i-C&CG, the value L^ℓ (the most recent solver lower bound that strictly exceeded L̄) is a valid lower bound on the optimal value υ* of the two-stage RO problem, i.e., L^ℓ ≤ υ*.
- conditions: Same problem class as thm-prop-1; crucially the master carries the extra constraint c^T x + δ ≥ L̄ (their eq. Inexact_C&CG_Master_con2); relies on the auxiliary lemma that if L̄ > υ* then the inexact master's optimal value is exactly L̄ (their Prop. B.1), so an invalid bound cannot be certified upward.
- anchor: ms.tex:407-409 — `At any iteration, the value $L^\ell$ is a valid lower bound on the optimal value $\upsilon^\star$ to problem \eqref{prob:2S_robust}, i.e., $L^\ell \leq \upsilon^\star$.`
- our-relevance: A lower-bound certificate that survives inexact master solves — directly analogous to the certificate hygiene we need when our LDR/AARC master programs are solved inexactly (LP budget/certificates line).

### thm-prop-3: Worst-case bound on the actual gap at an exploitation step
- statement: If i-C&CG reaches the exploitation step at iteration j, i.e., the actual relative gap satisfies (Ū − L^ℓ)/Ū ≥ ε while the inexact relative gap satisfies (Ū − U^j)/Ū < ε̃, then the actual relative gap is at most (1−ε̃)^{-1} ∏_{k=ℓ}^{j} (1−ε_MP^k)^{-1} − 1.
- conditions: i-C&CG with master solved to within relative gap ε_MP^k at each iteration since the last valid-bound iteration ℓ; no distributional or recourse assumptions beyond the standing ones; the proof chains U^{k+1} ≤ U^k/(1−ε_MP^{k+1}) with U^j ≤ L^ℓ ∏(1−ε_MP^k)^{-1}.
- anchor: ms.tex:414-416 — `then the actual relative gap is at most $(1-\epst)^{-1} \prod_{k=\ell}^j (1-\varepsilon_{MP}^k)^{-1}-1$.`
- our-relevance: A multiplicative error-budget certificate: total solution error is bounded by the product of per-solve inexactness factors, a template for budgeting inexact sub-solves inside our own certified pipelines (LP budget/certificates).

### thm-prop-4: Gap bound for the L̄←L^j variant (one-step version)
- statement: If in step 1.3 the algorithm updates L̄ ← L^j (instead of U^j), then whenever the exploitation conditions hold at iteration j — (Ū − L^ℓ)/Ū ≥ ε but (Ū − U^j)/Ū < ε̃ — the actual relative gap is at most (1−ε̃)^{-1}(1−ε_MP^j)^{-1} − 1.
- conditions: Same as thm-prop-3 but with the conservative update L̄ ← L^j, which makes L̄ always a valid lower bound and ℓ = j at every iteration; the paper notes this case is "equivalent to the C&CG method with inexact solves of master problems only", covering the tolerance scheme of Tonissen et al. 2021 which lacked any guarantee.
- anchor: ms.tex:476-478 — `then the actual relative gap is at most $(1-\epst)^{-1}(1-\varepsilon_{MP}^j)^{-1}-1$.`
- our-relevance: Shows the general certificate collapses to a single-factor (1−ε̃)^{-1}(1−ε_MP^j)^{-1} bound when the bound-validity constraint is kept conservative — the minimal certificate we would need if our condition-(B)-style optimality checks were run on inexactly solved masters.

### thm-prop-5: Inexact master value pinned at L̄ when L̄ exceeds υ*
- statement: If the value L̄ in the constraint c^T x + δ ≥ L̄ is greater than the optimal value υ* of the two-stage RO problem at some iteration j (i.e., L̄ > υ*), then the optimal value υ*_j of the inexact master problem equals L̄.
- conditions: Same master problem (with the lower-bound constraint and a scenario subset S ⊆ Ξ); uses x* optimal for the full problem and feasibility of (x*, L̄ − c^T x*) via max_{ξ∈S} Q(x*,ξ) ≤ max_{ξ∈Ξ} Q(x*,ξ) < L̄ − c^T x*.
- anchor: ms.tex:654-656 — `If the value $\Lbar$ in \eqref{eqn:Inexact_C&CG_Master_con2} is greater than the optimal value $\upsilon^*$ of problem \eqref{prob:2S_robust} at some iteration $j$ (i.e., $\Lbar>\upsilon^*$), the optimal value $\upsilon^\star_j$ of \eqref{prob:Inexact_C&CG_Master} is $\Lbar$.`
- our-relevance: A safety-lemma pattern: an overly aggressive bound does not corrupt the certificate, it merely pins the relaxed problem at the bound — reusable in any of our schemes that clamp relaxations with provisional valid bounds.

### thm-prop-6: Dual reformulation of the worst-case expectation (MAD/mean-support ambiguity)
- statement: For the DRORSP with ambiguity set P = {Q ∈ D(Ξ) | E_Q[d_i] = μ_i, E_Q[|d_i − μ_i|] ≤ ν_i, i ∈ I} (mean and mean-absolute-deviation information), the inner supremum sup_{Q∈P} E_Q[Q(y,d)] is equivalent to the minimization of Σ_{i∈I}(μ_i η_i + σ_i φ_i) + sup_{d∈Ξ}{ Q(y,d) − Σ_{i∈I}(d_i η_i + |d_i − μ_i| φ_i) } over (η, φ) with φ ≥ 0; under Slater-type conditions the same reduction holds for the mean-support ambiguity set, giving a problem of the form of the two-stage RO problem (2).
- conditions: Compact support Ξ, continuous Q(y,d) and moment functions; strong duality of moment problems (Shapiro et al.); for the mean-support case, the Slater-type condition of Xu et al. 2018 (weaker than classical Slater).
- anchor: ms.tex:791-792 — `The problem $\sup_{\Q\in\calP} \E_\Q[Q(\yb,\db)]$ with $\calP$ defined in \eqref{eqn:MAD_ambiguity_set} is equivalent to`
- our-relevance: This is the same reduction shape as our full-information/guaranteed-control reformulation (sup over disturbance → sup over a support, with dual variables entering the first stage) — a wedge-W-adjacent instance where the "robustified" problem is exactly equivalent to a finite-support-style RO problem under an explicit duality condition.

### thm-prop-7: MILP reformulation of the DRORSP subproblem (three-point property)
- statement: With Δ^lb_i = μ_i − d^lb_i and Δ^ub_i = d^ub_i − μ_i, the DRORSP subproblem sup_{d∈Ξ}{ Q(y,d) − Σ_{i∈I}(d_i η_i + |d_i − μ_i| φ_i) } is equivalent to a MILP: maximize over duals π, binaries b^1, b^2 and z^1 = b^1π, z^2 = b^2π (enforced by McCormick inequalities) the expression −T Σ_r π_r + Σ_i[ μ_i(Σ_r z-free term) − Δ^lb_i(...) + Δ^ub_i(...) − φ_i(b^1_i Δ^lb_i + b^2_i Δ^ub_i) ], subject to 0 ≤ π_r ≤ 1, McCormick bounds on z^1, z^2, and b^1_i + b^2_i ≤ 1 with b^1_i, b^2_i ∈ {0,1}.
- conditions: Recourse Q(y,d) = Σ_r (Σ_i y_{ir} d_i − T)^+ (an LP whose dual is max 0 ≤ π_r ≤ 1 of Σ_r π_r(Σ_i y_{ir} d_i − T)); box support Ξ = {d | d^lb_i ≤ d_i ≤ d^ub_i}; relies on the piecewise-linearity of the objective in each d_i.
- anchor: ms.tex:858-860 — `Let $\Deltalb_i = \mu_i-\dlb_i$ and $\Deltaub_i=\dub_i-\mu_i$ for all $i\in I$. The subproblem $\sup_{\db\in\Xi}\Big\{ Q(\yb,\db)- \sum_{i\in I}\big( d_i\eta_i + |d_i-\mu_i| \varphi_i \big) \Big\}$ is equivalent to`
- our-relevance: The proof turns on an exactness-at-finitely-many-points argument — the inner minimizer d_i* ∈ {d^lb_i, μ_i, d^ub_i} (ms.tex:901) — the same "optimal response lives at finitely many structural points" intuition that underlies our affine-rule exactness conjecture conj-ldr-exactness (vertex-list uncertainty, RHS-only uncertainty).

### thm-prop-8: MILP reformulation of the ROCPCP subproblem (budgeted uncertainty)
- statement: For the robust capacitated p-center problem with budget uncertainty set D = {d | d_i = μ_i + b_i Δ_i, Σ_i b_i ≤ τ, b_i ∈ {0,1}}, the subproblem sup_{d∈D} Q(x,d) is equivalent to the MILP: minimize Σ_i Σ_j c_{ij} x_{ij} μ_i π_i + Σ_i Σ_j c_{ij} x_{ij} Δ_i ζ_i subject to Σ_i π_i = 1, Σ_i b_i ≤ τ, McCormick constraints ζ_i ≥ 0, ζ_i ≥ π_i + b_i − 1, ζ_i ≤ π_i, ζ_i ≤ b_i, π_i ≥ 0, b_i ∈ {0,1}.
- conditions: Recourse Q(x,d) = min_z { z | z ≥ Σ_j c_{ij} d_i x_{ij}, ∀i }, whose dual has a simplex-type constraint Σ_i π_i = 1, π ≥ 0; budget (cardinality-constrained) uncertainty; McCormick linearization of the bilinear b_i π_i.
- anchor: ms.tex:1039-1041 — `The subproblem $\sup_{\db\in\calD} Q(\xb,\db)$ with $\calD$ defined in \eqref{eqn:budget_uncertainty_set} is equivalent to`
- our-relevance: A worked LP-duality-plus-McCormick certificate for a budget uncertainty set — the same budget-set machinery appears in our trackA-ldr-aarc-budget line, here on the adversary side rather than the decision-rule side.

## Fact blocks

### fact-prop-1: Problem class and standing assumptions
- statement: The object of study is the two-stage robust linear optimization problem υ* = min_{x∈X} { c^T x + max_{ξ∈Ξ} min_{y∈Y(x,ξ)} q^T y } with Y(x,ξ) = { y ∈ R^m_+ | Tx + Wy + Cξ ≥ h }; assumptions: (i) Ξ is a finite set or a bounded polyhedron (polytope); (ii) relatively complete recourse (Y(x,ξ) ≠ ∅ for all x ∈ X, ξ ∈ Ξ); (iii) an optimal solution with finite value exists; (iv) c^T x + Q(x,ξ) ≥ K for some K > 0 for all x ∈ X, ξ ∈ Ξ.
- anchor: ms.tex:279 — `where $\Xi\subseteq\R^l$ is an uncertainty set and $\calY(\xb,\xib)=\{\yb\in\R^m_+ \mid \Tb\xb +  \Wb\yb + \Cb\xib \geq \hb\}$ is the second-stage feasibility set.`
- applies: Two-stage RO with fixed technology matrix W (uncertainty enters only through Cξ in the RHS-like term), continuous or integer first- and second-stage variables; strictly positive objective values.

### fact-prop-2: i-C&CG generalizes C&CG
- statement: If the master problems are solved exactly (ε_MP^j = 0) and ε̃ < ε, then L^j = U^j, L̄ is a valid lower bound, ℓ is always set to j, and the backtracking routine reduces to the plain termination check; hence i-C&CG is a generalization of the C&CG method of Zeng & Zhao 2013 with one additional valid lower bound constraint (c^T x + δ ≥ L̄).
- anchor: ms.tex:357 — `Hence, our i-C\&CG method is a generalization of the C\&CG method with an additional valid lower bound constraint \eqref{eqn:Inexact_C\&CG_Master_con2}.`
- applies: The same two-stage RO class as fact-prop-1; note the added constraint is what restores lower-bound validity under inexactness.

### fact-prop-3: Exactness at ε = 0
- statement: By setting the actual relative gap tolerance to ε = 0, the i-C&CG method converges to the exact optimal solution of the two-stage RO problem (not merely an ε-optimal one).
- anchor: ms.tex:503 — `By setting the actual relative gap tolerance to $\varepsilon=0$, our i-C\&CG method converges to the exact optimal solution to \eqref{prob:2S_robust}.`
- applies: All problems satisfying the standing assumptions; exactness here means exactness of the (non-adaptive, full scenario-generation) solution, not of any parametric decision rule.

### fact-prop-4: Finite convergence of exact C&CG (inherited)
- statement: Assuming the maximin subproblem is solved by an optimality oracle that, for polytope Ξ, returns an extreme point of Ξ, and that Ξ is either finite or a polytope, the (exact) C&CG method terminates in a finite number of iterations — credited to Zeng & Zhao 2013 and Bertsimas & Shtern 2018.
- anchor: ms.tex:295 — `Under the assumption that $\Xi$ is either a finite set or a polytope, the C\&CG method terminates in a finite number of iterations \citep{Bertsimas_Shtern:2018,Zeng_Zhao:2013}.`
- applies: Two-stage RO with finite or polyhedral uncertainty; the extreme-point-oracle detail is the exactness mechanism on the adversary side.

### fact-prop-5: Exploration steps always add genuinely new scenarios
- statement: In the finite-convergence proof: if the worst-case scenario ξ* returned by the subproblem already belongs to the current scenario set S, then Ū − U^j ≤ 0, so the algorithm never takes an exploration step on a repeated scenario; every visit to step 4 enlarges S.
- anchor: ms.tex:488 — `We first show that every visit to step 4 (via the exploration step) enlarges the scenario set~$\calS$. Equivalently, we want to prove that if $\xib^\star$ in step 2 belongs to the current scenario set $\calS$ (i.e., $\xib^\star\in\calS$), then we will not proceed to the exploration step.`
- applies: i-C&CG with an exact subproblem oracle; this monotonicity is what reduces finiteness to finiteness of ext(Ξ) plus termination of exploitation phases.

### fact-prop-6: DRO problems reformulate into the two-stage RO form
- statement: Two-stage distributionally robust problems over mean-support or MAD ambiguity sets can be reformulated exactly in the form of the two-stage RO problem (2) via conjugate duality (under the Slater-type condition of Xu et al. 2018 for the mean-support case), with the dual variables appended to the first-stage decisions; therefore both C&CG and i-C&CG apply to such DRO problems.
- anchor: ms.tex:633 — `Hence, problem \eqref{eg_eqn:mean_support_dual} reduces to the form of problem \eqref{prob:2S_robust} with $(\xb,\lambdab)$ as the first-stage decision.`
- applies: Two-stage DRO with moment-type (mean / mean-absolute-deviation) ambiguity sets on a compact support.

### fact-prop-7: Three-point structure of the DRORSP adversary
- statement: Because the DRORSP subproblem objective is piecewise linear in each d_i with two pieces on [d^lb_i, μ_i] and [μ_i, d^ub_i], an optimal demand realization satisfies d_i* ∈ {d^lb_i, μ_i, d^ub_i} for every surgery i; this is what allows the two-binary encoding d_i = μ_i − b^1_i Δ^lb_i + b^2_i Δ^ub_i and the McCormick MILP.
- anchor: ms.tex:901 — `Since the objective function of \eqref{pf_prob:DRORSP_subproblem} is piecewise linear in $d_i$ with two pieces on $[\dlb_i,\mu_i]$ and $[\mu_i,\dub_i]$, we have that the optimal solution $d_i^\star\in\{\dlb_i,\mu_i,\dub_i\}$.`
- applies: The DRORSP recourse structure (sum of positive parts of assignment-minus-threshold) with box support; a special case of adversary optimality at finitely many structural points.

## Landscape
- cites: From the corpus list, the paper cites exactly three: **Zeng-Zhao 2013** (the C&CG method itself — problem assumptions ms.tex:281, algorithm ms.tex:293, convergence ms.tex:295, and ROCPCP instance generation ms.tex:975, ms.tex:1090), **Ayoub-Poss 2016** (ms.tex:260 — relaxing relatively complete recourse via MIP reformulation under 0-1 polytope uncertainty), and **Bertsimas-Shtern 2018** (ms.tex:260, ms.tex:295 — feasibility oracle and extension of C&CG convergence to general compact uncertainty sets). Additionally cited, not on our corpus list: Bertsimas-Sim 2004 (budgeted uncertainty), Tonissen et al. 2021 (adaptive relative tolerance for masters, no guarantees), Wang et al. 2019 (DRORSP), plus application/stochastic-programming references. NOT cited: Ben-Tal-Nemirovski 1999 (the bib has only the Ben-Tal-El Ghaoui-Nemirovski 2009 book, and it is never cited in the text), Ben-Tal-Goryashko 2004, Chen-Zhang 2009, Bertsimas-Goyal-Lu 2015, Bertsimas-deRuiter 2016, Xu-Burer 2017, HaddadSisakht-Ryan 2018, Marandi-denHertog 2018, Ben-Tal-ElHousni-Goyal 2018, Lu-Sturt 2022, Zhen-denHertog-Sim 2018, deRuiter-Zhen-denHertog 2018, Georghiou-Tsoukalas-Wiesemann 2020/2025, Bertsimas-Georghiou 2014, Zhang 2024, and the Chuong-Jeyakumar line.
- extends: Zeng-Zhao 2013 — the core contribution: Zeng-Zhao's C&CG requires masters solved to optimality; this paper shows finiteness survives inexact master solves if (a) a valid-lower-bound constraint c^T x + δ ≥ L̄ is added and (b) a backtracking routine shrinks ε_MP^j by α at exploitation steps, with the threshold ε̃ < ε/(1+ε). It also retroactively supplies the missing theoretical guarantee for Tonissen et al. 2021's adaptive-tolerance scheme (via thm-prop-4).
- contradicts-or-refines: Contradicts nothing in the corpus. Refines the Zeng-Zhao 2013 / Bertsimas-Shtern 2018 convergence framework: finite convergence is shown to be robust to master-side inexactness but is still shown to depend on exact subproblem oracles and on finiteness of ext(Ξ) — the subproblem side is left untouched, and no decision-rule approximation enters anywhere (the paper is orthogonal to the LDR/AARC line rather than competing with it).

## Open threads for our portfolio
- Exactness mechanism mismatch: the paper's only route to "exact optimal solution" (ms.tex:503) is ε = 0 + finite scenario generation with a full (non-adaptive) second-stage policy per scenario. It says nothing about whether a single affine decision rule y(ξ) = Y0 + Y1 ξ can be exact — conj-ldr-exactness remains fully open here, and this paper is a clean foil: exactness via column generation vs. exactness via structure of the rule.
- No subproblem-side inexactness: the optimality oracle for the maximin subproblem must be exact (ms.tex:295); whether a backtracking-style certificate exists when the adversary oracle itself is inexact (as it would be inside an LDR master where the inner max over ξ is solved inexactly) is not addressed — an analog of thm-prop-3 for inexact inner maxes would be a genuine gap we could fill in the AARC setting.
- The K > 0 strict positivity assumption (ms.tex:281) is load-bearing for master feasibility with the L̄ constraint (proof of Prop. 3.1/Prop. B.1 constructs the feasible point (x*, L̄ − c^T x*)); how the certificate machinery behaves with objectives allowed to be negative or zero is not discussed — relevant if we port the L̄-constraint trick to our LP budget/certificates line, where objectives are typically signed.
- Worst-case-only gap accounting: thm-prop-3's bound (1−ε̃)^{-1} ∏(1−ε_MP^k)^{-1} − 1 degrades multiplicatively in the number of exploitation steps and no iteration-complexity (number of oracle calls) bound is given; a quantitative bound relating |ext(Ξ)|, α, and ε̃ is absent (ms.tex:483-500) — the same quantitative-certificate gap we face in our own certified pipelines.
- The DRO reductions (ms.tex:627, ms.tex:633) require the Slater-type condition for strong duality of the moment problem; the paper does not check the condition for its own DRORSP instances, and the interaction of such duality conditions with exactness of affine rules (our full-information/wedge-W line) — i.e., whether the reduced RO problem inherits LDR exactness from the original DRO — is unexplored.

## Verdict for our reading queue
- processed-recommendation: Register thm-prop-1 through thm-prop-4 (the convergence-and-certificate core) as algorithmic-exactness context for conj-ldr-exactness — as contrast, not evidence: this paper establishes that exact solutions to (2) are computable without any decision-rule restriction, which sharpens why structural LDR exactness is a distinct claim. Register fact-prop-1 and fact-prop-2 (problem class + generalization relation) since our trackA blocks quote the same problem class. Register thm-prop-6/7/8 only at fact level (they are application-specific reformulations; their load-bearing content — the three-point property at ms.tex:901 and the McCormick/budget pattern at ms.tex:1044-1051 — is already captured in fact-prop-7 and thm-prop-8 and can serve as pattern precedents for the budget-set line). Skip: the DRORSP/ROCPCP experimental sections, the symmetry-breaking appendix (Denton et al. material), and the two algorithmic variants (Algorithm 3/4, exploitation frequency and time limit — engineering, no new theory, ms.tex:695-765). No edges into wedge-W or condition-(B) literature are possible from this paper: it cites none of that corpus.
