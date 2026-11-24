# Reading proposal: Ben-Tal, El Housni & Goyal 2018 (affine domination)

meta: "A Tractable Approach for designing Piecewise Affine Policies in Two-stage Adjustable Robust Optimization" — Aharon Ben-Tal, Omar El Housni, Vineet Goyal. Year 2018 (per corpus directory); venue and arXiv id are NOT visible in the TeX source [requires verification; published version known to be in Mathematical Programming but not stated in this file]. TeX source: `corpus/tex_src/10_BenTal_ElHousni_Goyal_2018/affine_domination.tex` (1620 lines; .bbl used for reference list only).

Scope note: despite the corpus shorthand "affine domination", the paper's object is *domination of an uncertainty set by a simplex* used to build a piecewise affine policy (PAP). The affine-policy-exactness content relevant to us is: (i) affine policy is optimal over a simplex (used at line 684-685), (ii) the exactness-separating instance where affine is Omega(sqrt(m)) off optimal (Section 3.2).

Model (eqn:ar, lines 118-125): two-stage adjustable robust covering problem
`z_AR(U) = min c^T x + max_{h in U} min_{y(h)} d^T y(h)` s.t. `A x + B y(h) >= h  for all h in U`, `x, y(h) >= 0`,
with `A, c, d` nonnegative, `U ⊆ R^m_+`. Worst case occurs at extreme points of U; AR is generally intractable (Omega(log m) hardness even for budget sets, Feige et al., line 134).

## Theorem blocks

### thm-beg-1: domination gives a beta-approximation (Theorem, label `thm:ineq`)
- statement: Let U satisfy Assumption 1 and Uhat ⊆ R^m_+ dominate U (Def. `Domination`). Let beta be the scaling factor of (U, Uhat), i.e. min{beta > 0 | Uhat ⊆ beta·U}. Then z_AR(U) ≤ z_AR(Uhat) ≤ beta · z_AR(U). Solving the adjustable problem over a dominating set is feasible for U and gives a beta-approximation.
- conditions: U satisfies Assumption 1 (down-monotone, full-dim, e_i ∈ U, ⊆ [0,1]^m); Uhat dominates U; beta exists since U full-dimensional, beta ≥ 1.
- anchor: affine_domination.tex:305 — `\[z_{\sf AR}({\cal U}) \leq z_{\sf AR}(\hat{\cal U}) \leq \beta \cdot z_{\sf AR}({\cal U}).\]`
- our-relevance: this is an approximation sandwich, not exactness, but it is the mechanism by which a policy computed on a *different* (simplex) set certifies quality on U — the same lifting logic our conj-ldr-exactness proofs use when exactness holds on a simpler set.

### thm-beg-2: PAP from a dominating simplex is feasible and 2beta-approximate (Theorem, label `thm:cost`)
- statement: Let U satisfy Assumption 1 and Uhat = beta·conv(e_1,…,e_m, v) dominate U with v ∈ U. The piecewise affine solution x = 2·xhat, y(h) = (1/beta)·Σ_i (h_i − beta·v_i)^+ · yhat(beta·e_i) + yhat(beta·v) (eq. `picewise_sl`, line 380-385) is feasible for Pi_AR(U) and gives a 2beta-approximation.
- conditions: dominating simplex of the fixed form with v ∈ U; PAP has exponentially many pieces but is computed by one compact LP over Uhat (m+1 scenarios, lines 319-326).
- anchor: affine_domination.tex:389 — `The piecewise affine solution in \eqref{picewise_sl} is feasible and gives a $2\beta$-approximation for the adjustable robust problem, $\Pi_{\sf AR}({\cal U})$~\eqref{eqn:ar}.`
- our-relevance: exhibits a *piecewise* affine rule that provably beats the optimal affine rule's worst-case guarantee on concrete sets — direct evidence that affine-exactness fails on ellipsoids/norm-balls, which any exactness condition of ours must exclude or sharpen.

### thm-beg-3: the only certificate needed is the threshold inequality (Theorem, label `thm:addi`)
- statement: Let U satisfy Assumption 1. If beta and v ∈ U satisfy (1/beta)·Σ_{i=1}^m (h_i − beta·v_i)^+ ≤ 1 for all h ∈ U (eq. `ineq:beta-v`), then the PAP `picewise_sl` gives a 2beta-approximation for Pi_AR(U). (No domination of U by Uhat needs to be checked separately — by Lemma `lem:ineq`b the inequality itself implies 2beta·conv(e_1,…,e_m,v) dominates U.)
- conditions: Assumption 1 only; beta, v ∈ U satisfying the scalar threshold inequality.
- anchor: affine_domination.tex:420 — `Let the uncertainty set ${\cal U}$ satisfy Assumption $1$. Consider any $\beta $ and $ \mb v \in {\cal U}$ satisfying~\eqref{ineq:beta-v}. Then, the piecewise affine solution in \eqref{picewise_sl} gives a $2\beta$-approximation for the adjustable robust problem, $\Pi_{\sf AR}({\cal U})$~\eqref{eqn:ar}.`
- our-relevance: the paper reduces policy quality to one verifiable inequality over U — structurally analogous to what a code-judge checker could verify for candidate exactness conditions (a single closed inequality in the geometry of U).

### thm-beg-4: closed-form beta for permutation invariant sets (Lemma, label `thm:beta`)
- statement: For U permutation invariant satisfying Assumption 1, with gamma(k) = (1/k)·max{Σ_{i=1}^k h_i | h ∈ U} and gamma = gamma(m), the minimum beta solving (1/beta)·max_{h∈U} Σ_i (h_i − beta·gamma)^+ ≤ 1 equals beta = max_{k=1..m} gamma(k) / (gamma + 1/k). Computed in closed form; optimizer is an extreme point of the form h* = gamma(k)·Σ_{i=1}^k e_i (Lemma `lem:struct:sol`, lines 493-497).
- conditions: U permutation invariant + Assumption 1 (SPI sets reduce to PI by diagonal rescaling of A, B without changing the policy bound, lines 449).
- anchor: affine_domination.tex:503 — `\beta  = \max _{ k=1,\ldots,m}  \frac{\gamma(k)}{\gamma +\frac{1}{k}}.`
- our-relevance: a computable geometric quantity (gamma-profile) that exactly determines the PAP guarantee — the kind of set-geometry-to-guarantee map our exactness conditions seek for the affine class.

### thm-beg-5: explicit PAP for PI sets (Theorem, label `thm:perm-inv-beta`)
- statement: For U permutation invariant with Assumption 1, take Uhat = beta·conv(e_1,…,e_m, gamma·e) with beta as in thm-beg-4. Then the explicit PAP x = 2·xhat, y(h) = (1/beta)·Σ_i (h_i − beta·gamma)^+ · yhat(beta·e_i) + yhat(beta·gamma·e) gives a 2beta-approximation for Pi_AR(U), and moreover the set 2·Uhat dominates U.
- conditions: permutation invariant U with Assumption 1; v = gamma·e.
- anchor: affine_domination.tex:530 — `gives a $2 \beta$-approximation for $\Pi_{\sf AR}({\cal U})$ \eqref{eqn:ar}. Moreover, the set $2 \cdot \hat{\cal U}$ dominates ${\cal U}$.`
- our-relevance: for symmetric sets the whole policy (and its guarantee) is read off from the gamma-profile — a template for how our exactness conditions should specialize on symmetric uncertainty sets.

### thm-beg-6: general sets via Algorithm 1 give O(sqrt(m)) (Theorem, label `thm:bound:beta`)
- statement: Suppose Algorithm 1 (iterative MIP-based construction, lines 722-738) returns beta, v. Then v ∈ U, and the PAP `picewise_sl` with these parameters gives an O(sqrt(m))-approximation for Pi_AR(U). Proof: beta ≤ (1 + sqrt(1+16m))/2 from Σ_t Σ_i h_i^t > beta(beta−1)/2 and Σ_t h_i^t ≤ 2.
- conditions: arbitrary U with Assumption 1; each iteration solves a nonconvex max of positives reformulated as a MIP (eq. `eqn:IP`, lines 772-781).
- anchor: affine_domination.tex:747 — `Suppose Algorithm~\ref{algo2} returns $\beta$, $\mb v$. Then $\mb v \in {\cal U}$. Furthermore, the piecewise affine policy~\eqref{picewise_sl} with parameters $\beta$ and $\mb v$ gives a $O(\sqrt m)$-approximation for the adjustable problem~\eqref{eqn:ar}.`
- our-relevance: worst-case parity with affine policy (both O(sqrt m)) — so affine-exactness failure in the worst case is not repaired by piecewise rules either; our exactness conditions must be set-relative, not universal.

### thm-beg-7: predecessor projection result, restated from Bertsimas–Goyal (Theorem, label `thm:berti-goyal`)
- statement: [Bertsimas and Goyal 2011] For any U satisfying Assumption 1 there exist beta ≤ sqrt(m) and v ∈ U such that Σ_{j : beta·v_j < 1} h_j ≤ beta for all h ∈ U. This underlies the O(sqrt m) bound for affine policies: static part covers beta·v, linear part covers the "active" coordinates J (restatement of Lemmas 8 and 9 of Bertsimas-Goyal).
- conditions: Assumption 1; existence statement, no efficient construction claimed here (but Algorithm 1 is the constructive analogue).
- anchor: affine_domination.tex:793 — `\[ \sum_{ j : \beta v_j < 1} \; h_j \leq \beta, \; \forall \mb h \in {\cal U}.\]`
- our-relevance: the affine-policy worst-case analysis reduced to a projection inequality on U — the exact style of geometric lemma our conj-ldr-exactness proofs should reuse when proving affine optimality on specific set classes.

### thm-beg-8: sqrt(m) is tight for simplex domination, even beyond simplices (Theorem, label `thm:worstcase`)
- statement: For the budget set U = {h ∈ R^m_+ | Σ h_i = sqrt(m), 0 ≤ h_i ≤ 1} (eq. `set-ones`), given any 0 < ε < 1/2, any k ∈ N, m sufficiently large, and any P(m) ≤ m^k points z_1,…,z_{P(m)} ∈ U, the set Uhat = m^{1/2−ε}·conv(z_1,…,z_{P(m)}) does not dominate U. So no polynomial-size point set scaled below m^{1/2} dominates the budget set: the framework cannot beat Theta(sqrt m) there.
- conditions: budget uncertainty set with budget exactly sqrt(m); polynomial number of generator points; any fixed ε > 0.
- anchor: affine_domination.tex:811 — `Given any $0 < \epsilon < 1/2$, and $k \in {\mathbb N}$, consider the budget of uncertainty set, ${\cal U}$~\eqref{set-ones} with $m$ sufficiently large. Let $P(m) \leq m^k$.`
- our-relevance: a hardness-of-approximation barrier tied to a specific set (budget, sum = sqrt m) — a natural negative test case: on this set neither affine nor this PAP family is near-optimal, sharpening where our exactness conditions can hold at all.

## Fact blocks

### fact-beg-1: Assumption 1 and its WLOG status
- statement: U ⊆ [0,1]^m is convex, full-dimensional with e_i ∈ U for all i, and down-monotone (h ∈ U, 0 ≤ h' ≤ h ⇒ h' ∈ U). The authors state this can be made WLOG by scaling and down-monotone completion without affecting Pi_AR (line 132).
- anchor: affine_domination.tex:129 — `\noindent {\bf Assumption 1}. ${\cal U}\subseteq [0,1]^m$  is convex, full-dimensional with $\mb{e}_i \in {\cal U}$ for all $i =1,\ldots,m$, and  {\em down-monotone}, i.e.,`
- applies: to every result in the paper; also the standing normalization we assume when porting any instance to our pipeline.

### fact-beg-2: definitions of domination and scaling factor
- statement: Uhat dominates U if for all h ∈ U there is hhat ∈ Uhat with hhat ≥ h (componentwise). Scaling factor beta(U, Uhat) = min{beta > 0 | Uhat ⊆ beta·U}; it exists (U full-dim) and is ≥ 1. Crucially, Uhat need NOT contain U (Example lines 280-284: the dominating simplex for the hypersphere is m^{1/4}·conv(e_1,…,e_m, e/sqrt m)).
- anchor: affine_domination.tex:273 — `\[\beta ({\cal U},\hat{{\cal U}})= \min \left\{ \beta >0 \; |\;\hat{\cal U} \subseteq  \beta \cdot {\cal U} \right\} .\]`
- applies: the two set-relations (domination vs containment) are distinct; domination, not containment, preserves feasibility of the covering problem.

### fact-beg-3: structural lemma — threshold inequality ⇔ domination up to factor 2 (Lemma, label `lem:ineq`)
- statement: a) If Uhat = beta·conv(e_1,…,e_m,v) dominates U (v ∈ U), then (1/beta)·Σ_{i=1}^m (h_i − beta·v_i)^+ ≤ 1 for all h ∈ U. b) Conversely, if beta, v ∈ U satisfy that inequality, then 2beta·conv(e_1,…,e_m,v) dominates U.
- anchor: affine_domination.tex:345 — `\frac{1}{\beta} \sum_{i=1}^m \left( h_i -\beta v_i  \right)^{+} \leq 1, \; \forall \mb h \in {\cal U}.`
- applies: the equivalence (up to factor 2) between the scalar certificate and domination; all per-set bounds in the paper are obtained by evaluating it.

### fact-beg-4: the piecewise affine (threshold) map
- statement: hhat(h) = beta·v + (h − beta·v)_+ dominates every h ∈ U and lies in the down-monotone completion of 2·Uhat (Lemma `lem:2U`). The static component covers beta·v, the piecewise-linear component covers the excess — analogous to threshold policies in dynamic optimization (lines 180-181).
- anchor: affine_domination.tex:334 — `\forall \mb h \in {\cal U}, \qquad \mb{ \hat{h}}(\mb h) = \beta \mb v + ( \mb h - \beta \mb v )_+.`
- applies: the concrete shape of the exponentially-many-pieces policy; a candidate family to test when our judges evaluate non-affine rules.

### fact-beg-5: per-set guarantees — hypersphere and p-norm balls (Props `prop:sphere`, `prop:p-ball`)
- statement: Hypersphere U = {h ≥ 0 | ||h||_2 ≤ 1}: gamma(k) = 1/sqrt(k), maximizer k = sqrt(m), beta = m^{1/4}/2, Uhat = m^{1/4}·conv(e_1,…,e_m, e/sqrt m) dominates U, PAP gives O(m^{1/4}) vs affine O(sqrt m) (BB15). p-norm ball: gamma(k) = k^{−1/p}, beta = (1/p)(p−1)^{(p−1)/p}·m^{(p−1)/p²} = O(m^{(p−1)/p²}), vs affine O(m^{1/p}).
- anchor: affine_domination.tex:574 — `\[ \beta = \frac{1}{p}   (p-1)^{\frac{p-1}{p}}             \cdot m^{\frac{p-1}{p^2}} = O (  m^{\frac{p-1}{p^2}} ).\]`
- applies: concrete separation numbers between affine and piecewise affine on the two canonical convex sets; if our exactness conjecture holds on a set class, it must be consistent with affine being strictly suboptimal at O(sqrt m) vs O(m^{1/4}) on the hypersphere.

### fact-beg-6: per-set guarantees — PI ellipsoid and budget set (Props `prop:ellipsoid`, `prop:Budget of uncertainty set`)
- statement: PI ellipsoid U = {h ≥ 0 | h^T Σ h ≤ 1} with Σ = (1−a)I + a·ee^T, 0 ≤ a ≤ 1: gamma = 1/sqrt(a m² + (1−a)m), beta = (a/2 + (1−a)^{1/2}/(a m² + (1−a)m)^{1/4})^{−1} = O(m^{2/5}). Budget set U = {h ∈ [0,1]^m | Σ h_i ≤ k}: beta = min(k, m/k), so PAP guarantee 2·min(k, m/k); worst case k ≈ sqrt(m) gives Theta(sqrt m).
- anchor: affine_domination.tex:653 — `Then, $$ \hat{ \cal U} = \beta \cdot {\sf{conv}} \left( \mb{e_1}, \mb{e_2},\ldots, \mb{e_m}, \frac{k}{m} \mb e \right)$$ where $ \beta = \min \left( k, \frac{m}{k}\right) $.`
- applies: ellipsoid is the set where affine policy is far from optimal (O(sqrt m) affine vs O(m^{2/5}) PAP) — the primary target set for our exactness investigations; budget set is where affine empirically wins (Section 6).

### fact-beg-7: exactness-separating instance — affine (and re-solving) is Omega(sqrt m) off, PAP near-optimal (Lemmas `lem:tight-comp-paff`, `lem:tight-comp-aff`)
- statement: For instance `ex:bad` (n = m, B_ij = 1 if i = j else 1/sqrt m, A = B, c = e/15, d = e, U = conv(0, e_1,…,e_m, all permutations of (1/sqrt m)·[1,…,1,0,…,0] with r = ceil(m − sqrt m) ones); line 661-675): (i) the PAP gives O(1 + 1/sqrt m)-approximation; (ii) affine policy gives Omega(sqrt m)-approximation, and moreover c^T x*_Aff = Omega(sqrt m)·z_AR(U) — the first-stage affine decision itself is far from optimal; the same holds for the practical re-solving variant that re-optimizes y given x*_Aff (lines 694-696).
- anchor: affine_domination.tex:682 — `Affine policy  gives an $ \Omega ({\sqrt{m}})$-approximation for the adjustable robust problem~\eqref{eqn:ar} for instance \eqref{ex:bad}. Moreover, for any optimal affine solution, the cost of the first-stage solution $ \mb x^*_{\sf Aff}$ is $ \Omega ({\sqrt{m}})$ away from the optimal adjustable problem ~\eqref{eqn:ar}, i.e. $ \mb c^T \mb x^*_{\sf Aff} = \Omega(m^{1/2}) \cdot z_{\sf AR}({\cal U})$.`
- applies: the canonical counterexample family for affine (and re-solving affine) exactness; any necessary condition in conj-ldr-exactness must fail on it, and it is small enough to encode as a judge test.

### fact-beg-8: affine policy is optimal over a simplex; domination without containment drives the gap (Section 3.2 discussion)
- statement: Since Uhat is a simplex with m+1 extreme points, the affine policy solves Pi_AR(Uhat) exactly: z_AR(U) ≤ z_AR(Uhat) = z_Aff(Uhat) ≤ O(1 + 1/sqrt m)·z_AR(U) on instance `ex:bad`, while z_Aff(U) = Omega(sqrt m)·z_Aff(Uhat) — "quite surprising since Uhat dominates U"; the authors stress that Uhat only dominates and does not contain U, which is crucial for the improvement (lines 684-690).
- anchor: affine_domination.tex:685 — `\[z_{\sf AR}({\cal U}) \leq z_{\sf AR}(\hat{\cal U}) = z_{\sf Aff}(\hat{\cal U}) \leq O \left(1+\frac{1}{\sqrt{m}}\right) \cdot z_{\sf AR}({\cal U}),\]`
- applies: an exactness statement in our exact sense — affine is optimal among ALL feasible policies over a simplex (consistent with Bertsimas-Goyal); the simplex is therefore the base positive case for conj-ldr-exactness, and the domination-vs-containment distinction warns that set inclusions do not monotonically preserve affine suboptimality gaps.

## Landscape

Cited in this paper (checked against affine_domination.tex citations and .bbl):
- Ben-Tal-Nemirovski 1999 — yes (`BN99`, line 107).
- BGT-2004 (Ben-Tal, Goryashko, Guslitzer, Nemirovski) — yes (`Ben-Tal04`, line 138; origin of the affine policy).
- Chen-Zhang line — yes, as Chen, Sim, Sun, Zhang 2008 (`chen2008linear`, line 144; extended affine decision rules).
- Bertsimas-Goyal-Lu 2015 — NOT found in .bbl/text; the nearby corpus items actually cited are Bertsimas-Goyal-Sun (`BGS10`, static solutions and symmetry) and Bertsimas-Goyal (`BG10`, power/limits of affine policies) [requires verification against corpus MANIFEST for the exact BGL-2015 entry].
- Bertsimas-deRuiter 2016 — not cited.
- Ayoub-Poss 2016 — yes (`ayoub2016decomposition`, line 134, dynamic extreme-point generation).
- Xu-Burer 2017 — not cited.
- HaddadSisakht-Ryan 2018 — not cited.
- Marandi-denHertog 2018 — not cited.
- Lu-Sturt 2022 — not cited.
- Zeng-Zhao 2013 — cited in earlier form: `zeng2011solving` (Zeng, constraint-and-column generation; text writes "Zeng and Zhao", line 134).
- Bertsimas-Shtern 2018 — not cited.
- Tsang-Shehadeh-Curtis 2022 — not cited.
- Chuong-Jeyakumar line — not cited.
- Zhang 2024 — not cited.
- Bertsimas-Georghiou 2014 — yes, as the 2015 OR paper `bertsimas2015design` (binary decision rules, line 144).
- Zhen-denHertog-Sim 2018 — not cited; the related adjustable-partition line is Postek-den Hertog (`postek2016multistage`, line 144).
- deRuiter-Zhen-denHertog 2018 — not cited.
- Georghiou-Tsoukalas-Wiesemann 2020/2025 — not cited.

Other load-bearing citations (outside our corpus list): Bertsimas-Bidkhori 2015 (`BB15`) — the affine-policy bounds this paper beats and corrects; Bertsimas-Caramanis 2010 (NP-hardness of optimal partitions, line 147); El Housni-Goyal (piecewise static policies, `elhousni2015piecewise`; probabilistic analysis, `housni2017beyond`); Feige et al. 2007 (Omega(log m) hardness); Bertsimas-Iancu-Parrilo 2010 and Iancu-Sharma-Sviridenko 2013 (affine optimality in special multistage cases).

- extends: directly extends Bertsimas-Goyal 2012 (`BG10`) — Theorem `thm:berti-goyal` is a restatement of BG10's Lemmas 8-9, and Algorithm 1 is the PAP analogue of BG10's explicit affine construction (lines 789-799). Sharpens BB15's affine bounds for SPI sets and corrects a typo in BB15 Table 2: the affine bound for p-norm balls should be (m^{(p−1)/p} + m)/(m^{(p−1)/p} + m^{1/p}) = O(m^{1/p}), not the expression printed there (footnote, lines 199-202) — flag this if we quote BB15 numbers.
- contradicts-or-refines: contradicts nothing; refines the folk claim "PAP optimal for polytopes but intractable" by computing an exponentially-piece PAP via a compact LP. Explicitly notes its PAP does NOT generalize the affine policy and affine can be better (budget sets, Section 6; line 202). Theorem `thm:worstcase` is a self-imposed negative result: no simplex-based (or any polynomial-point) domination framework beats Theta(sqrt m) on the sqrt(m)-budget set.

## Open threads for our portfolio

1. Base positive case for conj-ldr-exactness: affine is optimal among all feasible policies over a simplex (fact-beg-8, also attributed to BG10 at line 138). Candidate formalization for a judge: exactness certificate for simplex uncertainty sets; check whether our current conjecture statements cover the m+1-extreme-point case.
2. Required negative test: instance `ex:bad` (fact-beg-7) — affine AND re-solving affine are Omega(sqrt m) off, and the suboptimality sits in the first-stage x, not just in the y-rule. Any candidate exactness condition must fail here; worth encoding as a fixture in `judges/` test data.
3. Set-inclusion monotonicity warning: Uhat dominates U (even "almost contains" it) yet z_Aff(U) = Omega(sqrt m)·z_Aff(Uhat) (lines 684-690). Our exactness conditions must not be monotone under domination/containment of uncertainty sets; add this as an explicit sanity check in condition design.
4. Geometry-to-guarantee dictionary: the gamma(k)-profile of a PI set (eq. `eq:gamma(k)`, line 456) yields the PAP bound in closed form (thm-beg-4). Open for us: is there an analogous scalar profile of U that characterizes *affine exactness* (not just affine suboptimality bounds)?
5. Explicit open problem stated by the authors (line 1004): whether a PAP can be designed that significantly improves over affine for budgeted uncertainty sets — directly adjacent to our question of when affine is (near-)exact on polyhedral sets; the budget set with k = c·sqrt m is the boundary instance.
6. Numerical landscape for ellipsoids (fact-beg-6): affine is provably far from optimal on PI ellipsoids, yet affine exactness is our target there — any exactness result of ours must be conditional on structure beyond the set alone (e.g., cost/matrix symmetry), since the set alone permits large affine gaps.
7. Typo propagation risk: BB15's affine bound for p-norm balls is misquoted in BB15's own tables (footnote lines 199-202); if any of our drafts cite affine bounds for norm-balls via BB15, use the corrected O(m^{1/p}) form and cite this paper's footnote.

## Verdict for our reading queue

- processed-recommendation: process. Not an exactness paper per se, but it supplies (a) the base exactness case (simplex ⇒ affine optimal, fact-beg-8), (b) the standard separating instance for affine/re-solving suboptimality with the gap located in the first-stage decision (fact-beg-7), and (c) a corrected source for affine-policy bounds on norm-balls/ellipsoids needed by any conj-ldr-exactness literature table. Route: extract fact-beg-7/8 as boundary fixtures for the exactness conjecture; record the BB15 typo note in the glossary/landscape notes; do not treat as a source of positive exactness conditions beyond the simplex case.
