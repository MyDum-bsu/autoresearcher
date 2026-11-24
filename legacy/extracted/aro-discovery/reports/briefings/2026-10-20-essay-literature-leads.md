UNVERIFIED LEADS — not in corpus, not anchored; for orientation only.

# Essay literature leads, 2023–2026 (five-question scan)

Date: 2026-10-20
Scope: recent primary papers bearing on Q1–Q5 of the survey essay.
Status rule: every item below is a *lead*. Nothing here is anchored (no file+page,
no gate artifact, no sha256). Result statements are paraphrases of what the
abstract claims, not independent verification. Items marked `[metadata only]`
were identified by title/venue metadata; their abstracts could not be retrieved
and no result is asserted.

Sources used: arXiv Atom API (`export.arxiv.org/api/query`), OpenAlex works API,
individual arXiv abstract pages. Semantic Scholar Graph API was attempted six
times and returned HTTP 429 on every call; no Semantic Scholar data appears below.
SSRN (403), ResearchGate (403), INFORMS PubsOnline (403) and Elsevier/ScienceDirect
(redirect to a JS shell) blocked abstract retrieval.

## Ranking logic

Ranked by closeness to Q1 (necessary/sufficient conditions for exact affine rules)
and Q2 (complexity of choosing information structure / k / observation times),
then by Q3–Q5 relevance. Rank is not a quality judgement.

## Coverage matrix

| Q | Lead numbers |
|---|---|
| Q1 exactness conditions | L01, L02, L03, L07, L12, L16 |
| Q2 information structure / k / schedules | L04, L05, L06, L08, L09, L10, L11, L14, L17 |
| Q3 polyhedral geometry / simplicity / dual bases | L02, L03, L06, L07, L09, L15 |
| Q4 price of adaptivity / conic characterizations | L12, L13, L15, L16, L18, L19 |
| Q5 robust control ↔ two-stage RO bridge | L19, L20, L21, L22, L23, L24 |

---

## L01. On the Optimality of Affine Decision Rules in Distributionally Robust Optimization

- Authors: Angelos Georghiou, Angelos Tsoukalas, Wolfram Wiesemann
- Year: 2025 (Management Science 72(2):1456–1471)
- DOI: 10.1287/mnsc.2023.00053
- URL: https://doi.org/10.1287/mnsc.2023.00053
- Status: abstract read (OpenAlex work record, full abstract text)
- Abstract claims: the paper "propose[s] conditions under which two-stage
  distributionally robust optimization problems are optimally solved in affine or
  K-adaptable decision rules." Unlike prior work the conditions "do not impose any
  structure on the support of the uncertain parameters," and they ensure
  "pointwise (as opposed to worst case) optimality." Pointwise optimality plus
  support-free liftings is claimed to keep the rules optimal for broad DRO classes,
  including phi-divergence and Wasserstein ambiguity sets.
- Bears on: Q1 (sufficient conditions for exact affine/K-adaptable rules), Q4
  (optimality class), Q2 (K-adaptable variant).
- Caveat: setting is two-stage *distributionally robust*, not the fixed-recourse
  RHS-uncertainty ARO of Q1. No necessity claim appears in the abstract.

## L02. Connecting Extreme-Point Generation and Decision Rules in Two-Stage Distributionally Robust Optimization

- Authors: Jin Qi, Chen Yang
- Year: 2026 (arXiv preprint)
- arXiv: 2608.06821
- URL: https://arxiv.org/abs/2608.06821
- Status: abstract read (arXiv abstract page + OpenAlex record)
- Abstract claims: each extreme point of the second-stage dual "defines an affine
  value piece," and a compatible primal basis can define an affine policy piece.
  A separate LP procedure adds pieces "until it recovers the recourse value over
  the uncertainty set," and the authors "develop a posteriori exactness test[s] for
  conventional decision rules," with extensions to degeneracy, rank-deficient
  recourse and structured random recourse. They report that fully characterizing
  the second-stage value "requires more extreme points than solving the first-stage
  problem alone."
- Bears on: Q1 (exactness certification), Q3 (extreme points, primal bases,
  partitions of the dual).
- Caveat: exactness test is a posteriori/computational, not an a priori
  necessary-and-sufficient characterization. Two-stage DRO, not fixed-recourse
  RHS ARO.

## L03. When Is Two-Stage Sample Robust Optimization Asymptotically Optimal? A Simple Perspective

- Authors: Ling Dai, Chin Pang Ho
- Year: 2026 (arXiv preprint)
- arXiv: 2608.22999
- URL: https://arxiv.org/abs/2608.22999
- Status: abstract read (arXiv abstract page)
- Abstract claims: settles an open technical condition behind the asymptotic
  optimality of two-stage sample robust optimization with linear decision rules,
  using a geometric property of the support set called "simpleness": every vertex
  is incident to exactly as many edges as the ambient dimension. If the support is
  simple the technical condition holds automatically and asymptotic optimality
  follows; if not, a counterexample breaks asymptotic optimality, giving a "sharp
  dichotomy." A polynomial-time algorithm certifies the condition at any vertex
  from its incident edge directions.
- Bears on: Q1 (exactness in the limit for linear decision rules), Q3 (vertex
  incidence / simplicity of polyhedra).
- Caveat: asymptotic in the sample-size limit, not finite-sample exactness; the
  object is a support set, not a general uncertainty set.

## L04. Bounding the Optimal Number of Policies for Robust K-Adaptability

- Author: Jannis Kurtz
- Year: 2024 (arXiv v1; v3 2025; Mathematical Programming version reported 2026)
- arXiv: 2409.12630
- URL: https://arxiv.org/abs/2409.12630
- Status: abstract read (arXiv abstract page)
- Abstract claims: derives bounds on k that guarantee optimality of k-adaptability
  for general nonlinear problems with integer decisions, under objective or
  constraint uncertainty. For convex uncertainty sets with objective uncertainty
  the bound grows "linearly on the dimension of the uncertainty"; for constraint
  uncertainty the dependence "can be exponential," which the author calls "the
  first generic bound for a wide class of problems." Approximation guarantees are
  given below the bounds; determining the minimal k that makes k-adaptable and
  two-stage problems equivalent is NP-hard for finite uncertainty sets, with a
  greedy approximation when no first-stage decisions exist.
- Bears on: Q2 (number of wait-and-see policies), Q4 (approximation for small k).
- Caveat: bounds, not exact characterizations; exponential in the constraint-
  uncertainty case.

## L05. The complexity landscape of robust (integer) linear programming

- Authors: Michael Poss, Jannis Kurtz, Marc Goerigk, Dorothee Henke
- Year: 2026 (arXiv preprint)
- arXiv: 2608.21574
- URL: https://arxiv.org/abs/2608.21574
- Status: abstract read (arXiv abstract page)
- Abstract claims: classifies decision problems for static RO, two-stage
  (adjustable) RO and K-adaptability across P, NP, coNP and the polynomial
  hierarchy (Sigma_2^p, Sigma_3^p); with decision-dependent uncertainty and
  quadratic constraints the problems move to the existential theory of the reals
  (exists-R, Sigma_2^R, Sigma_3^R) or become undecidable. Emphasizes polynomial-size
  membership certificates despite exponentially long vector encodings, and gives an
  alternative proof that bilevel linear optimization is in NP. For K-adaptability
  it shows hardness "grows monotonically with K," and that for fully discrete
  decision-dependent instances K-adaptability "reduces back to the static problem."
- Bears on: Q2 (complexity of choosing k / information structure).
- Caveat: classification exercise; the abstract does not claim a complete map for
  every set class.

## L06. Finite adaptability in two-stage robust optimization: asymptotic optimality and tractability

- Authors: Safia Kedad-Sidhoum, Anton Medvedev, Frédéric Meunier
- Year: 2023 (v1; v5 2025)
- arXiv: 2305.05399
- URL: https://arxiv.org/abs/2305.05399
- Status: abstract read (arXiv abstract page)
- Abstract claims: the continuity assumption used by Bertsimas and Caramanis to
  prove convergence of finite adaptability as k grows "is flawed"; the authors
  propose a different assumption and prove convergence under it. They show the
  k=2 case with continuous variables and uncertainty in specific parameters
  becomes polynomial when the uncertainty set is a polytope with a bounded number
  of vertices, extend this to k=3, and derive new geometric results on covering
  polytopes with convex sets.
- Bears on: Q2 (fixed set of k policies; convergence and complexity), Q3 (covering
  polytopes).
- Caveat: the abstract reports a corrected convergence claim, i.e. an earlier
  asymptotic-optimality statement in the literature needed repair. Polynomial
  tractability is restricted (bounded vertex count; k in {2,3}).

## L07. On The Optimality of Affine Decision Rules in Two-Stage Adaptive Robust Optimization Beyond Simplex Uncertainty Sets

- Author: Yanfei Chen
- Year: 2026 (SSRN preprint, not peer reviewed as far as the record shows)
- DOI: 10.2139/ssrn.7416838
- URL: https://doi.org/10.2139/ssrn.7416838
- Status: `[metadata only]` — abstract field empty in OpenAlex; SSRN returned 403.
- Metadata: keywords include "affine decision rules," "uncertainty sets,"
  "right-hand side uncertainty," "optimality gap," "linear programming duality,"
  "robust linear programming."
- Bears on: Q1, Q3 — the title is the closest single match to Q1 found in this scan.
- Caveat: no result may be attributed. Obtain and read before citing. Treat as a
  pointer only; provenance/peer-review status unknown.

## L08. Affine Decision Rules for Robust Optimization with Decision-Dependent Information Discovery

- Authors: Uğur Karabaş, Henri Lefebvre, Michael Poss
- Year: 2026 (HAL preprint, submitted 7 October 2026)
- HAL: hal-05784143
- URL: https://hal.science/hal-05784143
- Status: abstract read (HAL record)
- Abstract claims: derives "structural properties of the resulting min-max-min
  problem, including existence of solutions," and identifies "a condition under
  which information discovery has no value." Proposes a heuristic combining affine
  decision rules with scenario generation, shows "its adversarial separation
  problem is NP-hard," and gives a sampling procedure to estimate solution quality
  without solving to global optimality. On knapsack and facility-location cases it
  "outperforms a K-adaptability approach recently proposed in the literature in
  terms of computation time" at comparable quality.
- Bears on: Q2 (when to acquire information; value of information discovery),
  Q4 (affine-rule heuristic quality).
- Caveat: heuristic; the no-value condition is existence-level, not a full
  characterization of optimal information structure.

## L09. Hitting and Covering Affine Families of Convex Polyhedra, with Applications to Robust Optimization

- Authors: Jean Cardinal, Xavier Goaoc, Sarah Wajsbrot
- Year: 2025 (arXiv preprint)
- arXiv: 2504.16642
- URL: https://arxiv.org/abs/2504.16642
- Status: abstract read (arXiv abstract page)
- Abstract claims: introduces hitting-set variants for continuous families of
  convex polyhedra, and shows these capture decision versions of two-level finite
  adaptability in robust optimization. The problems are solvable in strongly
  polynomial time when the hitting-set size and the dimensions of the polyhedra
  and parameter space are constant; the hitting-set problem is solvable in strongly
  quadratic time for one-parameter families in constant dimension. These give "new
  tractability results for finite adaptability that are the first ones with
  so-called left-hand-side uncertainty, where the underlying problem is non-linear."
- Bears on: Q2 (complexity of partitioning/covering for adaptability), Q3
  (polyhedral geometry).
- Caveat: fixed-dimension, fixed-size regime only.

## L10. Scalable Finite Adaptability via Polyhedral Partition and Learning

- Authors: Zolykha Rezaei, Ningji Wei, Eojin Han
- Year: 2026 (arXiv preprint)
- arXiv: 2606.06927
- URL: https://arxiv.org/abs/2606.06927
- Status: abstract read (arXiv abstract page)
- Abstract claims: makes the uncertainty-set partition explicit and builds policies
  on polyhedral partitions; under mild regularity and general risk measures, "such
  policies converge to the optimal fully adjustable policy as the number of
  regions increases." Gives a parametric partition framework with tractable
  formulations for robust and stochastic finite adaptability, plus an
  "approximate-learn-parallel framework" that preserves solution robustness.
- Bears on: Q2 (policy count vs. partition complexity), Q3 (polyhedral partitions).
- Caveat: convergence in the number of regions; learning component has no
  optimality guarantee beyond robustness preservation as described.

## L11. Distributionally Robust Optimization with Decision-Dependent Information Discovery

- Authors: Qing Jin, Angelos Georghiou, Phebe Vayanos, Grani A. Hanasusanto
- Year: 2024 (v1; revised 2025)
- arXiv: 2404.05900
- URL: https://arxiv.org/abs/2404.05900
- Status: abstract read (arXiv abstract page)
- Abstract claims: studies two-stage DRO where uncertain parameters become known
  only after a costly first-stage investment; formulates a min-max-min-max problem
  and applies K-adaptability, fixing K candidate recourse actions in advance and
  selecting the best after the chosen parameters are observed. Gives an exact
  cutting-plane decomposition, with the evaluation subproblem solved by a
  branch-and-cut algorithm that converges to an optimal solution; tested on R&D
  portfolio and best-box problems.
- Bears on: Q2 (K fixed in advance; information discovery).
- Caveat: the abstract gives no complexity result and no condition on optimal K.

## L12. The Benefit of Uncertainty Coupling in Robust and Adaptive Robust Optimization

- Authors: Dimitris Bertsimas, Liangyuan Na, Bartolomeo Stellato, Irina Wang
- Year: 2023 (v1; v2 2024)
- arXiv: 2302.10369
- URL: https://arxiv.org/abs/2302.10369
- Status: abstract read (arXiv abstract page)
- Abstract claims: defines a coupled uncertainty set as "the intersection between a
  constraint-wise uncertainty set and a coupling set," and derives "theoretical
  tight and computable upper and lower bounds on the objective value improvement"
  from coupling, for both RO and ARO. Explicitly "relate[s] the power of
  adaptability over static solutions with the coupling of uncertainty set," and
  reports computational evidence for the benefit of coupling.
- Bears on: Q4 (quantifying the value of adaptivity, albeit relative to coupling),
  Q1 (conservatism of constraint-wise treatments).
- Caveat: improvement is measured against constraint-wise uncertainty, not against
  the fully adaptive optimum; no affine-rule exactness claim.

## L13. LP-based Approximations for Disjoint Bilinear and Two-Stage Adjustable Robust Optimization

- Authors: Omar El Housni, Ayoub Foussoul, Vineet Goyal
- Year: 2023 (Mathematical Programming 206(1–2):239–281; arXiv v4 2023)
- arXiv: 2112.00868
- DOI: 10.1007/s10107-023-02004-9
- URL: https://arxiv.org/abs/2112.00868
- Status: abstract read (arXiv abstract page)
- Abstract claims: for disjoint bilinear programs over packing polytopes, gives an
  O((log log m1 / log m1)(log log m2 / log m2)) approximation via an LP relaxation
  and randomized rounding. Applied to two-stage ARO with covering constraints and
  RHS uncertainty, the LP restriction achieves an
  O((log n / log log n)(log L / log log L)) approximation, with L the number of
  uncertainty-set constraints; because the restriction yields a feasible affine
  policy, "affine policies give" the same guarantee.
- Bears on: Q4 (approximation guarantee for affine rules in general set classes).
- Caveat: logarithmic factors are not removed; approximation, not exactness.

## L14. Completeness in the Polynomial Hierarchy for many natural Problems in Bilevel and Robust Optimization

- Authors: Christoph Grüne, Lasse Wulf
- Year: 2023 (v1; revised 2025)
- arXiv: 2311.10540
- URL: https://arxiv.org/abs/2311.10540
- Status: abstract read (arXiv listing summary)
- Abstract claims: a meta-theorem yielding over 70 new Sigma_2^p- and Sigma_3^p-
  complete problems for interdiction, regret and two-stage robust variants;
  min-max variants are Sigma_2^p-complete and min-max-min two-stage variants are
  Sigma_3^p-complete for a broad problem list.
- Bears on: Q2 (complexity of two-stage/adaptive variants).
- Caveat: completeness for problem families, not for the schedule-selection
  question specifically.

## L15. General Polyhedral Approximation of two-stage robust linear programming for budgeted uncertainty

- Authors: Lukas Grunau, Tim Niemann, Sebastian Stiller
- Year: 2025 (Computers & Operations Research 179:107014)
- DOI: 10.1016/j.cor.2025.107014
- URL: https://doi.org/10.1016/j.cor.2025.107014
- Status: abstract read (OpenAlex record; publisher page did not render)
- Abstract claims: replaces the uncertainty set by a finite collection of polytopes
  built from vertex subsets of a dominating polytope, where the union "need not
  contain U." For budgeted uncertainty with m rows, the authors note affine
  policies are "known to be best possible approximations" when second-stage
  constraint coefficients are nonnegative, but computing them is usually too slow;
  a single-simplex approach reaches a threshold at Gamma > m after which it "is not
  better than the quasi nominal solution," and the new method improves quality by a
  constant factor before that threshold while staying faster after it.
- Bears on: Q3 (simplex-based polyhedral approximation), Q4 (limits of affine
  policies under budgeted uncertainty).
- Caveat: "best possible" is conditioned on nonnegative recourse coefficients; the
  threshold result is empirical/algorithmic.

## L16. Exact worst-case performance of affine decision rules in two-stage adaptive robust optimization under budgeted uncertainty

- Author: Yanfei Chen
- Year: 2026 (ResearchGate preprint record)
- DOI: 10.13140/RG.2.2.12333.86244
- URL: https://doi.org/10.13140/RG.2.2.12333.86244
- Status: `[metadata only]` — abstract empty in OpenAlex; ResearchGate returned 403.
- Metadata keywords: affine decision rules, budgeted uncertainty, worst-case
  performance, robust optimization.
- Bears on: Q1/Q4 — title suggests an exact worst-case performance characterization
  for affine rules under budgeted uncertainty.
- Caveat: no result asserted. Obtain before citing; provenance unknown.

## L17. The Complexity Landscape of Two-Stage Robust Selection Problems with Budgeted Uncertainty

- Authors: Marc Goerigk, Dorothee Henke, Lasse Wulf
- Year: 2026 (arXiv preprint)
- arXiv: 2602.16465
- URL: https://arxiv.org/abs/2602.16465
- Status: abstract read (arXiv listing summary)
- Abstract claims: separates discrete from continuous budgeted uncertainty;
  "the two-stage selection problem with continuous budgeted uncertainty is
  NP-hard," while the representative-selection variant "is solvable in polynomial
  time," and the hardness extends to two-stage assignment under the same
  uncertainty type.
- Bears on: Q2 (complexity of two-stage adaptivity under budgeted sets), Q3
  (budgeted uncertainty structure).
- Caveat: selection/assignment problem classes only.

## L18. Optimality of Affine Policies in Distributionally Robust Linear-Quadratic Control with Temporally Correlated Noise

- Authors: Jakob Nylöf, Daniel Kuhn, John Lygeros, Giancarlo Ferrari-Trecate
- Year: 2026 (arXiv preprint)
- arXiv: 2609.27653
- URL: https://arxiv.org/abs/2609.27653
- Status: abstract read (arXiv listing summary)
- Abstract claims: for finite-horizon distributionally robust LQ control with
  arbitrarily time-correlated disturbances and a 2-Wasserstein ball around an
  elliptically contoured nominal distribution, proves that "the optimal policy is
  affine" and that the worst case is an affine push-forward of the nominal
  distribution, despite infinite-dimensional policy and ambiguity spaces. Maps are
  computed with a Frank–Wolfe best-response algorithm.
- Bears on: Q4 (exact optimality of affine policies, conic/OT structure), Q5
  (control-side exactness).
- Caveat: LQ control with Wasserstein ambiguity, not fixed-recourse RHS ARO; the
  transfer to Q1 is not claimed in the abstract.

## L19. Regret-Optimal Linear-Quadratic Control under Distributional Drift

- Authors: Lukas-Benedikt Fiechtner, Jose Blanchet
- Year: 2026 (arXiv preprint; submitted to ACC 2027)
- arXiv: 2610.09220
- URL: https://arxiv.org/abs/2610.09220
- Status: abstract read (arXiv listing summary)
- Abstract claims: introduces ex-ante distributionally robust regret optimization
  for finite-horizon LQR with drifting disturbance distributions and a temporally
  coupled moment ambiguity set; affine disturbance-feedback synthesis "reduces
  exactly to a semidefinite program," while the analogous standard DRO relaxation
  "may exhibit a duality gap."
- Bears on: Q4 (exact conic reformulation for affine feedback), Q5 (affine
  disturbance feedback as the bridge object).
- Caveat: regret objective, not worst-case cost; LQR structure.

## L20. Optimal Closed-Loop Measurement Feedback in a Linear Optimal Control Problem

- Author: N. M. Dmitruk
- Year: 2025 (Proceedings of the Steklov Institute of Mathematics 329(S1):S77–S92)
- DOI: 10.1134/s0081543825600966
- URL: https://doi.org/10.1134/s0081543825600966
- Status: abstract read (OpenAlex record)
- Abstract claims: treats a terminal problem of "optimal guaranteed control for a
  linear continuous system" with disturbances whose measured output signals have
  bounded error; constructs a multi-closed control strategy, derives closed-loop
  measurement feedback from it, and proposes algorithms for computing strategies
  and implementing the feedback in real time.
- Bears on: Q5 (guaranteed control / minimax with a fixed disturbance path and
  successive closure instants), Q2 (number and placement of closure instants as a
  scheduling choice — though see caveat).
- Caveat: the abstract describes algorithms for a given multi-closure structure;
  it does not claim optimization over the closure instants. (The 2022 companion is
  already corpus item A4; see cross-reference note.)

## L21. A Transformation-Proximal Bundle Algorithm for Multistage Adaptive Robust Optimization and Application to Constrained Robust Optimal Control

- Authors: Chao Ning, Fengqi You
- Year: 2020 (Automatica 113; arXiv 2018, v2 2019)
- arXiv: 1810.05931
- URL: https://arxiv.org/abs/1810.05931
- Status: abstract read (arXiv listing summary)
- Abstract claims: splits recourse decisions into state and control decisions,
  applies the affine policy only to state decisions while control decisions remain
  fully adaptive, and converts the multistage ARO into an equivalent two-stage ARO
  problem solvable by any two-stage ARO solver. In an inventory-control case the
  affine disturbance-feedback policy "shows severe suboptimality (average gap
  34.88%)," versus 1.68% for the proposed method.
- Bears on: Q5 (explicit ARO ↔ robust optimal control transformation), Q4
  (quantified suboptimality of affine feedback).
- Caveat: published 2020 (outside the 2023–2026 window); included because it is
  the most explicit algorithmic bridge found and is still cited by the recent
  control-side literature.

## L22. System Level Synthesis for Affine Control Policies: Model Based and Data-Driven Settings

- Authors: Lukas Schüepp, Giulia De Pasquale, Florian Dörfler, Carmen Amo Alonso
- Year: 2025 (CDC 2025; arXiv preprint)
- arXiv: 2504.01677
- DOI: 10.1109/CDC57313.2025.11312162
- URL: https://arxiv.org/abs/2504.01677
- Status: abstract read (arXiv listing summary)
- Abstract claims: extends System Level Synthesis to a closed-loop parameterization
  for time-varying affine control policies; shows closed-loop behavior under
  affine policies "can be equivalently characterized using past system
  trajectories," enabling a fully data-driven formulation and integration into MPC
  with closed-loop maps.
- Bears on: Q5 (affine policies as closed-loop maps; bridge vocabulary).
- Caveat: no claim about two-stage RO exactness.

## L23. Distributionally Robust System Level Synthesis With Output Feedback Affine Control Policy

- Authors: Yun Li, Jicheng Shi, Colin N. Jones, Neil Yorke-Smith, Tamas Keviczky
- Year: 2025 (arXiv preprint)
- arXiv: 2508.05466
- URL: https://arxiv.org/abs/2508.05466
- Status: abstract read (arXiv listing summary)
- Abstract claims: finite-horizon robust control of constrained linear systems with
  model mismatch and stochastic disturbances; uses SLS with an output-feedback
  affine policy, extends to a distributionally robust form with a 1-norm mismatch
  bound and a Wasserstein ambiguity set, and derives a tractable reformulation.
- Bears on: Q5 (affine output-feedback policy + DRO), Q4 (tractability).
- Caveat: reformulation/tractability, not exactness of the affine class.

## L24. Robust Data-Enabled Predictive Control: Tractable Formulations and Performance Guarantees

- Authors: Linbin Huang, Jianzhe Zhen, John Lygeros, Florian Dörfler
- Year: 2023 (IEEE Transactions on Automatic Control 68(5):3163–3170)
- DOI: 10.1109/TAC.2023.3241282
- Status: abstract read (OpenAlex record)
- Abstract claims: robust DeePC for LTI systems from inexact input/output data;
  "solves a min–max optimization problem" over a prescribed uncertainty set, gives
  tractable reformulations for several uncertainty sets, and proves performance
  guarantees for the realized input-output cost despite inexact data.
- Bears on: Q5 (min-max robust control as a robust optimization problem).
- Caveat: data-driven predictive control; no decision-rule exactness claim.

---

## Pre-2023 anchors (context only, not leads)

These are not 2023–2026 leads and several are likely already known to the project.
Listed because the recent abstracts above repeatedly point back to them.

1. A. Ben-Tal, O. El Housni, V. Goyal, "A Tractable Approach for designing
   Piecewise Affine Policies in Two-stage Adjustable Robust Optimization,"
   arXiv:1801.06751 (2018). Dominating-simplex construction; exponentially many
   pieces computable by a compact LP; O(m^{1/4}) for hypersphere vs O(sqrt m) for
   affine. Direct Q3 ancestor.
2. O. El Housni, V. Goyal, "On the Optimality of Affine Policies for Budgeted
   Uncertainty Sets," Mathematics of Operations Research 46(2):674–711 (2021),
   DOI 10.1287/moor.2020.1082. Affine policies attain O(log n / log log n), matching
   hardness, for nonnegative fixed recourse under budgeted RHS uncertainty.
3. G. Xu, S. Burer, "A Copositive Approach for Two-Stage Adjustable Robust
   Optimization with Uncertain Right-Hand Sides," arXiv:1609.07402 (2017).
   Copositive reformulation; SDP approximations at least as strong as affine
   policies; polynomial-time exact on a family where affine has arbitrarily large
   gap. Key Q4 conic anchor.
4. G. Xu, G. A. Hanasusanto, "Improved Decision Rule Approximations for Multi-Stage
   Robust Optimization via Copositive Programming," arXiv:1808.06231 (2021).
   Linear rules for uncertain objective/recourse/RHS; quadratic rules for RHS only;
   copositive reformulations, tight conservative approximations.
5. A. Marandi, D. den Hertog, "When are Static and Adjustable Robust Optimization
   with Constraint-Wise Uncertainty Equivalent?", SSRN 2665046 (2015).
   `[metadata only]` — no abstract retrieved. Title is a direct Q1 ancestor.
6. M. E. Villanueva, R. Quirynen, M. Diehl, B. Chachuat, B. Houska, "Robust MPC via
   Min-Max Differential Inequalities," arXiv:1611.03924 (2016). Tube MPC via
   support-function differential inequalities; no discretization of the control
   policy. Q5 anchor.

---

## What is still open according to these abstracts

1. **A priori necessary-and-sufficient exactness conditions for Q1 are not
   supplied by any retrieved abstract.** L01 gives sufficient conditions, in a DRO
   setting, for pointwise optimality of affine/K-adaptable rules. L02 gives only an
   a posteriori test. L03 gives asymptotic exactness under a geometric condition on
   the support set. No abstract claims necessity, and none is stated for the
   fixed-recourse / RHS-uncertainty ARO class named in Q1. L07 and L16 have exactly
   the right titles but their abstracts were unavailable, so this gap may be
   narrower than it appears — they are the first items to obtain.

2. **Finite-k / finite-sample exactness remains open.** L03 is asymptotic in the
   sample size; L04's bounds on k are exponential for constraint uncertainty; L06
   shows polynomial tractability only for bounded-vertex polytopes and k in {2,3}.
   No abstract claims a finite, checkable exactness criterion for general convex
   uncertainty sets.

3. **The earlier convergence claim for finite adaptability needed repair.**
   L06 states that the continuity assumption used by Bertsimas and Caramanis is
   flawed and supplies a replacement. Any essay sentence relying on the older
   convergence argument should be checked against L06 rather than repeated.

4. **Complexity of choosing the information structure itself is not classified.**
   L04, L05, L06, L09, L14, L17 classify fixed-k adaptability or fixed two-stage
   structures. L08 identifies only a condition under which information discovery
   has no value, and shows the adversarial separation problem is NP-hard; it does
   not give a complexity class for optimizing when/what to observe. No retrieved
   abstract gives a complexity result for optimizing observation times or the
   number of wait-and-see policies as a design variable.

5. **No "price of adaptivity" for affine rules in two-stage RO was found.** The
   term appears in this scan only in adjacent literatures: Y. Carmon, O. Hinder,
   "The Price of Adaptivity in Stochastic Convex Optimization," arXiv:2402.10898
   (2024) — at least logarithmic / double-logarithmic / polynomial penalties
   depending on what is unknown, "no parameter-free lunch"; and Z. Barak,
   I. Talgam-Cohen, "Stochastic Knapsack: Semi-Adaptivity Gaps and Improved
   Approximation," arXiv:2602.24042 (2026) — improved adaptivity-gap bounds for
   risky stochastic knapsack and semi-adaptivity gaps. Neither is two-stage ARO;
   they are framing material only. Any "price of adaptivity" definition for ARO
   would have to be constructed, not cited.

6. **Conic/copositive characterizations of affine-rule exactness are largely older
   than the scan window.** The 2023–2026 arXiv hits for copositive + robust
   optimization are about attainment/escape in conic optimization, not decision
   rules; the copositive decision-rule literature retrieved is 2016–2021. L19's
   exact SDP for affine disturbance feedback and L18's affine-optimality theorem
   are control-side conic exactness results, not fixed-recourse RHS ARO.

7. **No equivalence theorem between guaranteeing-program minimax control and
   two-stage ARO was retrieved.** L21 is the closest: it converts multistage ARO
   into an equivalent two-stage ARO by restricting affine policies to state
   decisions, and quantifies the affine-feedback gap (34.88% vs 1.68%). L20 gives
   guaranteed control with measurement error but assumes the multi-closure
   structure. No abstract claims that the two literatures' optimal values coincide,
   nor that a guaranteeing program is a special case of a two-stage adjustable
   robust counterpart.

8. **The k-selection question stays hard even where exactness is achievable.**
   L04: minimal k is NP-hard for finite uncertainty sets; greedy only without
   first-stage decisions. L05: hardness grows monotonically with K. L11: K is fixed
   in advance, with no optimality result for K.

9. **Computational certification is separated from structural characterization.**
   L02 reports that fully characterizing the second-stage value needs more extreme
   points than solving the first-stage problem alone; L03's certification is
   per-vertex; L09's tractability is fixed-dimension. A practical, general
   exactness certificate is not claimed.

10. **The control-side exactness results are conditional on LQ/Wasserstein
    structure.** L18 proves affine optimality under a 2-Wasserstein ball around an
    elliptically contoured nominal distribution; L19 under temporally coupled
    moment ambiguity. Neither abstract claims transfer to polyhedral RHS
    uncertainty or fixed recourse.

---

## Terminology gaps observed (null and near-null searches)

These null results are themselves useful for the essay: the two literatures use
different vocabularies for the same objects.

- arXiv exact phrase `"scheduled recourse"`: 0 results.
- arXiv `"simplex uncertainty"`: 0 results.
- arXiv `"fixed disturbance"` AND `minimax`: 0 results.
- arXiv `"adjustable robust"` AND `"model predictive control"`: 0 results.
- arXiv `"robust MPC"` AND `"two-stage robust optimization"`: 0 results.
- arXiv `"guaranteed feasibility"` AND `"adjustable robust"`: 0 results.
- arXiv `"value of information"` AND `"two-stage robust"`: 0 results.
- arXiv `"vertex solutions"` AND robust AND optimization: 0 results.
- arXiv `"simple polytope"` AND `optimi*`: 0 results.
- arXiv `"affine decision rules"` AND `simplex`: 0 results.
- arXiv `"right-hand side uncertainty"` AND `"decision rules"`: 0 results
  (the hyphenated form `"right-hand-side"` is used inside papers, which is why
  phrase search misses them).

Control-side vocabulary that does retrieve the bridge: "guaranteed control,"
"multi-closed strategy," "closure instants," "measurement feedback," "affine
disturbance feedback," "system level synthesis," "tube MPC." RO-side vocabulary:
"decision rules," "finite adaptability," "K-adaptability," "information discovery,"
"non-anticipativity." An essay mapping these terms pairwise would be doing real
work, because the abstracts do not do it for us.

---

## In-corpus cross-reference (no files added)

- `corpus/our_papers/A4_Дмитрук_2022.pdf` is N. M. Dmitruk, "Multiply closed
  control strategy in a linear terminal problem of optimal guaranteed control"
  (Trudy IMM UrO RAN 28(3), 2022); a Steklov Institute version with the same title
  is indexed as Proc. Steklov Inst. Math. 319(S1):S112–S128 (2022). L20 is the
  2025 successor (measurement feedback, bounded observation error) and is *not*
  the corpus item.
- L21 (Ning & You) is not in the corpus as far as the manifest shows, but the
  project's reading notes already discuss affine disturbance feedback; check before
  treating it as new.
- No file was downloaded and nothing was written to `corpus/`.

## Retrieval log

- arXiv Atom API: ~30 queries; several feeds were truncated by the fetch tool
  (noted where relevant). Queries that returned zero results are listed above.
- OpenAlex works API: ~20 queries; several pages truncated; abstracts often null
  for journal records.
- Semantic Scholar Graph API: 6 attempts, all HTTP 429. No data used.
- Blocked: SSRN 403, ResearchGate 403, INFORMS PubsOnline 403, Elsevier/
  ScienceDirect redirect to JS shell.
- Individual arXiv abstract pages read successfully: 2608.22999, 2608.21574,
  2608.06821, 2409.12630, 2404.05900, 2409.10295, 2504.16642, 2606.06927,
  2302.10369, 2305.05399, 2112.00868, 2409.12630.
