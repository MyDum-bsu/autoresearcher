# Reading proposal for the essay; blocks NOT yet registered in the science graph.

Status: proposal only. No blocks registered, no judge run, no graph mutation.

Method: `pdftotext -layout` on the six corpus PDFs; printed page numbers checked
against the running heads and footers of each copy. Quotes are reproduced from
the PDF text layer with line wrapping collapsed and are otherwise verbatim.
Glyph caveat: several of these scans have a text layer that renders `,` as `;`,
`≥`/`≤` as `¿`/`6`, drops ligatures (`first` prints as ` rst`, `definition` as
`de nition`, `efficient` as `e cient`), and mangles `ξ` as `Æ`. Two conventions
are used consistently below: **dropped ligatures are restored to standard
spelling** (a pure extraction artifact, no wording is changed), while
**punctuation substitutions are left exactly as in the text layer and flagged in
the gloss**, so a reader can tell what the PDF actually prints. Superscripts and
Greek letters are otherwise flattened to ASCII. Where a quote joins two numbered
items of a theorem list, the numbering is dropped and the gloss says so. Hashes
are the 64 hex characters of the corresponding lines in `corpus/MANIFEST.md`.

Corpus copies used and page arithmetic:

- `01_BenTal_Nemirovski_1999.pdf` — journal typeset copy, Operations Research
  Letters 25 (1999) 1–13. PDF page = printed page.
- `04_Bertsimas_Goyal_Lu_2015.pdf` — MIT Open Access author's final manuscript
  (Math. Program. 150(2):281–319). PDF page 1 is the MIT cover sheet, so PDF
  page = manuscript page + 1. Anchors below use the manuscript numbers printed
  in this copy, **not** the journal's 281–319.
- `05_Bertsimas_deRuiter_2016.pdf` — journal typeset copy, INFORMS Journal on
  Computing 28(3):500–511. PDF page 1 is the INFORMS download cover, so PDF
  page = printed page − 498.
- `06_Ayoub_Poss_2016.pdf` — HAL preprint `hal-01301374v1` of the Computational
  Management Science 13(2):219–239 article. PDF page = manuscript page + 1.
  Anchors use the preprint's own page numbers; the published pagination
  219–239 is **not** mapped here (`page: uncertain` for the journal copy).
- `08_HaddadSisakht_Ryan_2018.pdf` — journal typeset copy, Annals of Operations
  Research 269:185–204. PDF page = printed page − 184.
- `20_Bertsimas_Georghiou_2014.pdf` — pre-journal manuscript dated
  September 2, 2014, printed pages 1–35. PDF page = printed page. Venue and
  final pagination are not visible in this copy (`page: uncertain` outside it).

One scope warning that governs the whole note: **only 04, 05, 06 and 08
actually contain an affine (or static) decision rule.** Paper 01 has no
recourse at all, and paper 20 is about piecewise-linear rules with affine rules
as the P = 1 baseline. Claims below are labelled accordingly; do not let a
later citation of "Bertsimas–Goyal–Lu gives an iff" drift into "affine rules are
exact iff T(U,h) is convex", because their theorem is stated for the **static**
class only.

---

## 1. Ben-Tal & Nemirovski 1999 — geometry-to-tractability dictionary

Paper: "Robust solutions of uncertain linear programs". Static robust
counterpart only; no second stage, no decision rule. Its role in this essay is
ancestral: it fixes the vocabulary (constraint-wise, convex hull, ellipsoidal
representation) that every later exactness condition reuses.

### 01-c1 — only the closed convex hull of the uncertainty set matters
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 3
- `printed_page:` 3
- `quote:` "Evidently, the robust counterpart (PU ) of an uncertain LP program remains unchanged when we replace the uncertainty set U by its closed convex hull. Consequently, from now on we always assume that U is convex and closed."
- `gloss:` Worst-case feasibility depends on U only through its closed convex hull, so a finite vertex list and its convex hull are interchangeable at the robust-counterpart level.
- `relevance:` (i) This is the primitive sufficient condition behind every later vertex-representation argument: convexification is free. (ii) It also bounds what vertex enumeration can buy — it cannot distinguish a polytope from any convex set with the same hull. (iii) Directly relevant: for a vertex-represented U the hull is exactly the polytope, so the "replace U by conv(vertices)" step needs no further hypothesis here.

### 01-c2 — any uncertainty set can be extended to a constraint-wise one
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 4
- `printed_page:` 4
- `quote:` "Thus, given an arbitrary uncertainty set U, we can always extend it to a constraint-wise uncertainty set resulting in the same robust counterpart."
- `gloss:` Constraint-wise structure can be imposed by enlarging U without changing the robust problem, so the robust counterpart "feels" only per-row projections, never cross-row dependence.
- `relevance:` (i) Supplies the canonical exactness condition inherited by 04 and 08: constraint-wise uncertainty guarantees that row couplings cannot hurt. (ii) It is an enlargement, not an equivalence of the original data — it shows that *only* cross-row dependence can create a gap. (iii) A box or a vertex-set that is a Cartesian product of per-row sets is exactly the covered case; a budget set that couples rows is not.

### 01-c3 — robust counterpart value equals the worst single instance
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 4
- `printed_page:` 4
- `quote:` "Proposition 2.1. If the uncertainty U is constraint-wise and the boundedness assumption holds; then (i) (PU ) is infeasible if and only if there exists an infeasible instance (P) ∈ P. (ii) If (PU ) is feasible and c∗ is the optimal value of the problem; then c∗ = sup{c∗ (P) | (P) ∈ P}:"
- `gloss:` Under constraint-wise uncertainty plus boundedness, robust feasibility and robust value coincide exactly with the worst realization; the text layer prints semicolons where the PDF has commas.
- `relevance:` (i) The earliest exactness theorem in this batch: a structural condition on U turns an infinite family into its worst element. (ii) Without constraint-wise structure the equality can fail, which is the static ancestor of every impossibility example in 04 and 08. (iii) This is static, so it says nothing about recourse; it is the template, not the result, for a fixed-recourse RHS-only vertex problem.

### 01-c4 — an explicit robust-vs-instance gap
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 3
- `printed_page:` 3
- `quote:` "A “gap” between the solvability properties of the instances of an uncertain LP and those of its robust counterpart may indeed exist, as is demonstrated by the following simple example:"
- `gloss:` The paper's two-variable example has every instance solvable at value 1 while the robust counterpart is infeasible; the uncertainty set is the segment a11 + a22 = 2 with a11 in [1/2, 3/2].
- `relevance:` (i) None — this is a negative result about exactness of the robust counterpart itself. (ii) It is the minimal witness that a convex, low-dimensional, non-constraint-wise U destroys the "worst instance" identity. (iii) Important semantic caution for the essay: this is a gap between RC and the instance family, **not** an adaptivity gap between affine and fully adaptive recourse. It should not be cited as an affine counterexample.

### 01-c5 — tractability is a property of U's separation oracle
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 5
- `printed_page:` 5
- `quote:` "Tractability principle. An efficient Separation oracle for U implies an efficient Inclusion oracle and; consequently; implies an efficient separation oracle for GU (and thus implies computational tractability of (PU ))."
- `gloss:` If the uncertainty set is separable then the robust feasible set is separable and the robust program is tractable; the text layer prints semicolons for commas.
- `relevance:` (i) Separates the two questions the essay must keep apart: "is affine exact?" is a value question, "is the affine reformulation solvable?" is an oracle question. (ii) It gives no exactness guarantee, so tractability must never be read as optimality. (iii) For a vertex-represented U the separation oracle is trivial (enumerate vertices), so this paper already explains why vertex uncertainty is computationally harmless while remaining silent on whether it is representationally exact.

### 01-c6 — ellipsoidal uncertainty is exactly a conic quadratic program
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 7
- `printed_page:` 7
- `quote:` "Theorem 3.1. The robust counterpart (PU ) of an uncertain LP problem with general ellipsoidal uncertainty can be converted to a conic quadratic program."
- `gloss:` An intersection of finitely many ellipsoids yields a CQP robust counterpart, hence a polynomial-time solvable reformulation.
- `relevance:` (i) The first "geometry determines the exact reformulation class" result in the corpus. (ii) It is a tractability, not an exactness, theorem: it says nothing about whether a static solution is optimal. (iii) For the essay's vertex question this is the contrast case — ellipsoids are not vertex-represented and yet need no vertex enumeration, which is why vertex count is a sufficient, not necessary, route to exactness.

### 01-c7 — polytopes are a case of ellipsoidal uncertainty
- `file:` corpus/01_BenTal_Nemirovski_1999.pdf
- `sha256:` 17034b3d6b9775e2cd144a2200b669598a186050d737006fddc678ad9b5ce105
- `pdf_page:` 8
- `printed_page:` 8
- `quote:` "Thus; a polytopic uncertainty is indeed ellipsoidal."
- `gloss:` A bounded polytope is an intersection of "stripes", each a degenerate ellipsoidal cylinder, so the CQP machinery covers polytopes; the text layer prints a semicolon for the comma.
- `relevance:` (i) Shows that polyhedral and ellipsoidal uncertainty are not disjoint tractability classes, so "box vs ellipsoid" is the wrong axis for an exactness taxonomy. (ii) It undercuts any argument that infers exactness from the *name* of the set geometry. (iii) A vertex-represented polytope therefore sits inside the CQP-covered family, but this yields only computability of the robust counterpart, not exactness of a recourse rule.

---

## 2. Bertsimas, Goyal & Lu 2015 — the iff characterization for static solutions

Paper: "A Tight Characterization of the Performance of Static Solutions in Two-stage Adjustable Robust Linear Optimization". This is the most directly load-bearing paper for the essay. It contains (a) a necessary-and-sufficient geometric criterion, (b) a tight approximation factor, (c) an explicit family attaining any prescribable gap, and (d) an extension to uncertain right-hand sides.

Model caveat to state in the essay: the base model (1.1) is a **packing** problem,
`max c'x + min_B max_{y(B)} d'y` s.t. `Ax + By(B) ≤ h`, with `B ∈ U ⊆ R_+^{m×n2}`
and `y ≥ 0`, so the recourse matrix is the uncertain object. RHS uncertainty
appears only in §4.1. The exactness object is the **static** solution, i.e. the
zero-slope affine rule; the theorem is not stated for general affine rules.

### 04-c1 — static exactness iff the transformation T(U,h) is convex
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 11
- `printed_page:` 10
- `quote:` "Then, zAR = zRob if T (U, h) is convex for all h > 0. Furthermore, if T (U, h) is not convex for some h > 0, then there exist an instance such that zAR > zRob."
- `gloss:` Theorem 1 ("Optimality of Static Solutions"), quoted from its conclusion: convexity of the transformed uncertainty set for every positive right-hand side is exactly equivalent to the static solution attaining the fully adjustable value, and failure of convexity at a single h yields an instance with a strict gap.
- `relevance:` (i) The sharpest sufficient condition in the batch, and the only one with a matching converse. (ii) The converse is constructive, so non-convexity is not merely a missing proof but a certified impossibility. (iii) Caveat: the criterion is for the static class. It is sufficient for affine exactness (static ⊂ affine) but the converse direction is not claimed for nonzero slopes, so the essay must not promote it to an iff for affine rules.

### 04-c2 — the transformation is the dual-feasible scaling of rows
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 9
- `printed_page:` 8
- `quote:` "For instance, if h = e, then T (U , e) is the set of all convex combinations of rows of B ∈ U for all B ∈ U . Note that T (U , e) is not necessarily convex in general."
- `gloss:` T(U,h) collects B'μ over B in U and nonnegative μ normalized by h'μ = 1, i.e. the set of h-weighted convex combinations of rows; it can fail to be convex even when U is convex.
- `relevance:` (i) Names the precise geometric object whose convexity is the exactness criterion, so the essay can state the condition in one line. (ii) It explains why convex U is not enough: the quantifier "for all B in U" is inside the convex combination, and that is what can break convexity. (iii) For a vertex-represented U the set T is generated by vertices alone, making the convexity test finite — a direct hook for the vertex case.

### 04-c3 — constraint-wise U is the inherited sufficient family
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 10
- `printed_page:` 9
- `quote:` "In later discussion, we show that a static solution is optimal if T (U, h) is convex for all h > 0; thereby extending the result in [4] for the case where U is contained in the non-negative orthant."
- `gloss:` Lemma 1 proves that constraint-wise U makes T(U,h) convex for every h, recovering and generalizing Ben-Tal–Nemirovski 1999 beyond nonnegative data.
- `relevance:` (i) The direct inheritance chain 01-c2 → 04-c3 should be drawn explicitly in the essay. (ii) It shows the sufficient conditions form a nested family (constraint-wise ⊂ convex-T), so the interesting question is what lies strictly between. (iii) Constraint-wise sets are products of per-row sets; a budget set with a global cardinality constraint is not of this form, so this condition does not cover the essay's coupled vertex sets.

### 04-c4 — scaled projections: a second sufficient family
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 10
- `printed_page:` 9
- `quote:` "A compact convex set U ∈ Rm×n + is said to satisfy the scaled projections property if the projections of U onto each of its m row sets are scalar multiples of each other."
- `gloss:` Lemma 2 proves that if all row projections of U are positive scalar multiples of one another, then T(U,h) is convex for all h; permutation-invariant sets such as {B ≥ 0 : Σ B_ij ≤ 1} are the canonical example.
- `relevance:` (i) A genuinely new sufficient condition beyond constraint-wise, and one that covers a coupled simplex-type set. (ii) It shows the exactness boundary is not "independence across rows" but a weaker proportionality of row projections. (iii) This is the closest the paper comes to a vertex-set condition: a simplex {B ≥ 0 : Σ B_ij ≤ 1} has a vertex representation and is exact, which the essay can use as a positive vertex example.

### 04-c5 — tight approximation factor equals the non-convexity measure
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 15
- `printed_page:` 14
- `quote:` "Then, zAR ≤ ρ(U ) · zRob . Furthermore, we can show that the bound is tight."
- `gloss:` With ρ(U) = max over h > 0 of κ(T(U,h)), where κ(S) = min{α : conv(S) ⊆ αS}, the adjustable value is at most ρ(U) times the static value, and no smaller factor works in general; the theorem requires the added assumptions x ≥ 0 and c ≥ 0.
- `relevance:` (i) Gives a quantitative distance-to-exactness: ρ(U) = 1 is exactly the exact regime. (ii) Tightness means the measure is not an artifact of the proof, so it is a genuine impossibility certificate. (iii) The factor is a function of U and h only, not of the cost data, so for a vertex-represented U it is in principle computable from vertices — the natural place to attach a vertex-count condition.

### 04-c6 — the factor is at most the number of constraints
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 17
- `printed_page:` 16
- `quote:` "Theorem 3 For any down-monotone convex compact set U ∈ Rm×n + and h > 0, κ(T (U, h)) ≤ m."
- `gloss:` The non-convexity of T and hence the static-vs-adjustable factor is bounded by m, the number of constraints (rows of B), independently of the number of uncertain entries mn.
- `relevance:` (i) A dimension-dependence statement of the good kind: the guarantee degrades in the number of rows, not in the number of uncertain parameters. (ii) It is an upper bound only; the diagonal family in 04-c7 shows it is attained, so m cannot be improved in general. (iii) For a fixed-recourse problem with m rows this pins the worst-case factor to m even under vertex-represented U, which is a useful ceiling for the essay's negative section.

### 04-c7 — the sharp negative family: gap exactly n^(1/θ)
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 32
- `printed_page:` 31
- `quote:` "T (U θ , h) is non-convex for all h > 0. κ(T (U θ , h)) = n 1/θ for all h > 0."
- `gloss:` For the diagonal set U^θ = {B ∈ [0,1]^{n×n} : B_ij = 0 for i ≠ j, Σ_j B_jj^θ ≤ 1} with θ > 1, the non-convexity measure is n^{1/θ}; the quote joins items 3 and 4 of Theorem 7 and drops their numbering. The proof in §3.1 chooses θ = log_μ n to obtain z_AR / z_Rob = n^{1/θ} = μ for any prescribed μ > 1 and any n.
- `relevance:` (i) None for exactness — it is a pure non-exactness family. (ii) It is the essay's best impossibility witness: the gap is exactly the geometric measure, not merely bounded by it, and μ is an input to the construction, so the gap is unbounded. (iii) The set is a vertex-represented, down-monotone, convex polytope in the nonnegative orthant, so it lands squarely inside the "vertex-represented" class and proves that vertex representation alone cannot buy exactness.

### 04-c8 — RHS uncertainty: constraint-wise U^{B,h} restores static optimality
- `file:` corpus/04_Bertsimas_Goyal_Lu_2015.pdf
- `sha256:` 91fe2751d14113006a1e9213ad2ed05d159a0aa9545a3f933148794b7309cb2f
- `pdf_page:` 25
- `printed_page:` 24
- `quote:` "Now, we study the performance of static solution and show that it is optimal if U B,h is constraint-wise."
- `gloss:` In the model where the constraint matrix, the right-hand side and the second-stage objective are all uncertain with U^{B,h,d} = U^{B,h} × U^d, constraint-wise U^{B,h} makes the static solution optimal (Theorem 6).
- `relevance:` (i) This is the paper's only right-hand-side result, and it is a sufficient condition of exactly the constraint-wise type. (ii) The paper states explicitly that the non-convexity bound does not extend here because U^{B,h} is not down-monotone, so exactness survives where the quantitative bound does not. (iii) Partially covers the essay's target, and one step is inference rather than quotation: if the B-block of U^{B,h} is held at a singleton so that only h is uncertain, then U^{B,h} is constraint-wise automatically and Theorem 6 would give static optimality for a pure RHS-only problem. The paper does not spell out this specialization; it should be cited as a corollary of Theorem 6, not as a stated result. It does **not** cover a coupled vertex set over h.

---

## 3. Bertsimas & de Ruiter 2016 — duality, not exactness

Paper: "Duality in Two-Stage Adaptive Linear Optimization: Faster Computation and Stronger Bounds". Contribution is a dualized reformulation and an affine-policy transfer, plus a strengthened lower bound. It is the cleanest statement in the batch of the **fixed-recourse, RHS-only, polyhedral** setting, but it proves no exactness characterization.

### 05-c1 — fixed recourse and RHS-only uncertainty are the working hypotheses
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 3-4
- `printed_page:` 501-502
- `quote:` "For our dual derivation to work, we must have the matrix B to be fixed independent of Æ. Hence, we only consider the case of fixed recourse."
- `gloss:` The paper's dualization requires a recourse matrix B that does not depend on the uncertain parameter; the text layer prints Æ for ξ. The sentence spans the page break (second clause begins PDF page 4 / printed 502), which is why both page fields carry a range. The uncertainty appears only on the right-hand side, Rξ + r, over a polyhedral set U = {ξ ≥ 0 : Dξ ≤ d}.
- `relevance:` (i) Establishes that "fixed recourse + RHS-only" is a genuine modelling class, not a toy assumption. (ii) It also flags that dropping fixed recourse invalidates the derivation, which is the same boundary that 06 tests with a counterexample. (iii) This is exactly the essay's target class, so this block can anchor the definition section.

### 05-c2 — the dualized model preserves the here-and-now decisions exactly
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 3
- `printed_page:` 501
- `quote:` "The new dualized formulations have the same set of feasible (and optimal) here-and-now decisions as the original two-stage models."
- `gloss:` Dualizing over the wait-and-see variables and then over the uncertain parameters yields a two-stage adaptive model whose first-stage feasible and optimal set is identical to the primal's.
- `relevance:` (i) An exactness result of a different kind: exactness of a reformulation, not of a policy class. (ii) It implies the fully adaptive value is invariant under this dualization, so any affine gap computed in the dual is the same gap as in the primal. (iii) Fully covers the fixed-recourse RHS-only polyhedral setting, and is the natural computational vehicle for the essay's target class.

### 05-c3 — affine policies correspond across primal and dual
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 7
- `printed_page:` 505
- `quote:` "Theorem 2 is not only useful because it proves equivalence of the primal and dual formulation with affine policies. It also allows us to solve the dual formulation (16) with affine policies and directly obtain the optimal affine policy of the original formulation (or vice versa)."
- `gloss:` Affine-in-ξ policies in the primal and linear-in-w policies in the dual are in explicit bijection (u = θ + μd, V = λ − μD, π = μ'B' + Q), so the affine value is the same in both formulations.
- `relevance:` (i) Gives a second, dual route to the affine value, which is useful for certifying that a computed gap is not a formulation artifact. (ii) It does not say when the affine value equals the adaptive value — only that both formulations agree on whatever that value is. (iii) Covers the target class technically, and the bijection is a candidate certificate format for the essay's exactness test.

### 05-c4 — vertex count as an exactness driver
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 6
- `printed_page:` 504
- `quote:` "As shown in Bertsimas and Goyal (2012, Lemma 1), linear policies are optimal if there are only m extreme points, where m is the size of the uncertainty set."
- `gloss:` In the static case B = 0 the dual uncertainty set has exactly m extreme points (the unit vectors), and m extreme points suffice for linear policies to be optimal; this is a cited result, not proved here.
- `relevance:` (i) A genuine vertex-count sufficient condition: small vertex count ⇒ affine/linear is exact. (ii) It is a sufficient condition on the *dual* set, so the essay must be careful about which set's vertex count is being counted. (iii) Directly relevant to a vertex-represented problem, but with the caveat that the count that matters may be the dual's, and that m here is the number of constraints, so this is a very restrictive sufficient condition.

### 05-c5 — the lower bound is tight only when all vertices are included
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 7
- `printed_page:` 505
- `quote:` "It is shown by Bertsimas and Goyal (2012) that the lower bound is tight if we include all extreme points of the uncertainty set."
- `gloss:` Solving the fully adjustable model on a finite scenario subset gives a lower bound, and that bound equals the true adaptive value exactly when the subset is the full vertex set.
- `relevance:` (i) Confirms that "full vertex enumeration = exact fully adaptive value", which is the representational fact the essay needs. (ii) The contrapositive is the useful part: any strict subset leaves a possibly strict gap, so vertex completeness is necessary for this particular certificate, if not for exactness in general. (iii) Covers the vertex-represented case directly, and also flags the practical obstruction (vertex counts explode).

### 05-c6 — box uncertainty is a proven exact regime
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 12
- `printed_page:` 510
- `quote:` "This is surprising, because for this case (box uncertainty) we know that affine (in fact, static) policies are provably optimal (Ben-Tal et al. 2009, Theorem 14.2.4)."
- `gloss:` The facility-location experiments use budget uncertainty; at 100% budget the set becomes a box, and in that limit affine — indeed static — policies are provably optimal by a cited theorem.
- `relevance:` (i) A concrete exact geometry: the full box. (ii) It is exactness of the *static* rule at 100% budget, so it is the boundary case of the budget family where the coupling parameter saturates. (iii) Covers a vertex-represented box (2^L vertices) and is the cleanest positive vertex example in the batch alongside 04-c4.

### 05-c7 — affine is empirically near-exact but not proven so
- `file:` corpus/05_Bertsimas_deRuiter_2016.pdf
- `sha256:` 2f6f7ddbd5fd082603ebf2533c0ef86f6c37c74a54bd7c108f223467c3cd636e
- `pdf_page:` 11
- `printed_page:` 509
- `quote:` "If we take a look at the bounds we see they are very close to the objective value, which shows that the use of affine policies is nearly optimal."
- `gloss:` In the facility-location experiments the authors report that the affine-policy lower bounds sit close to the objective value and read this as near-optimality, while noting that at â = 100% (the box limit) the bound is *furthest* from the objective. The visible Table 6 rows span roughly 0.5% to 28.4%, so "nearly optimal" is the authors' summary, not a uniform property of the table.
- `relevance:` (i) Supplies an empirical prior for the essay's "affine usually near-exact" claim, but it is evidence, not a theorem. (ii) It cannot establish a nonzero gap and cannot establish exactness; the numbers are instance-specific. (iii) Covers a fixed-recourse RHS-only problem with budget uncertainty (a vertex-represented polytope when the budget is integral), so it is a useful data point for the target class — but only a data point.

---

## 4. Ayoub & Poss 2016 — exact vertex reduction and its failure

Paper: "Decomposition for adjustable robust linear optimization subject to uncertainty polytope". This is the only paper in the batch that states the vertex-representation theorem for the **fully adjustable** problem outright, and the only one that gives a sharp structural counterexample to it. It does not study affine rules as an object; affine routing is used as a computational baseline.

Model: `min c'x` s.t. `T(ξ)x + W y(ξ) ≥ h` for all `ξ ∈ Ξ`, `x ∈ S`, with `T(ξ) = T^0 + Σ_k T^{1k} ξ_k` and `Ξ` a polytope. Fixed recourse means `W` independent of ξ.

### 06-c1 — affine rules are the tractability response to an intractable ARC
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 3
- `printed_page:` 2
- `quote:` "Ben-Tal et al (2004) prove that adjustable robust optimization is untractable in general, so that they focus on approximations that restrict the adjustable variables to affine functions of the uncertainty, yielding the so-called affine decision rules."
- `gloss:` Affine rules are introduced explicitly as an approximation to an intractable exact problem, not as an exact class.
- `relevance:` (i) Frames the essay's question correctly: affine exactness is an exceptional property, and the burden of proof is on the exactness claim. (ii) It supplies the baseline impossibility (general ARC intractable), which is why exactness results must be structural. (iii) It is the setting in which a vertex-represented U becomes attractive: exactness is recovered by finiteness rather than by policy restriction.

### 06-c2 — polytope ⇒ the vertex set is a faithful replacement
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 4
- `printed_page:` 3
- `quote:` "Indeed, when the robust constraints are linear and the uncertainty set is a polytope, we know that the latter can be replaced by the finite set of its extreme points. This reformulation as such is not very useful because the number of extreme points is usually prohibitive."
- `gloss:` For linear constraints and polyhedral U, imposing the constraint only at extreme points is exactly equivalent to imposing it everywhere; the obstacle is combinatorial size, not correctness.
- `relevance:` (i) The exact vertex-representation statement the essay needs, at the level of the fully adaptive problem. (ii) It is exact only because the constraint is linear in y and the quantifier is over a polytope; it says nothing about the affine class. (iii) This is the clearest positive answer in the batch to the fixed-recourse, RHS-only, vertex-represented question — with the important refinement that it is about full adjustability, so it makes the affine question moot rather than answering it.

### 06-c3 — Lemma 1: vertex restriction preserves the optimal first stage
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 5
- `printed_page:` 4
- `quote:` "Let vert(Ξ) be the set of extreme points of Ξ and x ∈ R|I| a given vector. Vector x can be extended to an optimal solution (x, y) to (P ) if and only if it can be extended to an optimal solution (x, y 0 ) to …"
- `gloss:` The ellipsis replaces the displayed program (P'), which is (P) with ξ restricted to vert(Ξ); the "if and only if" is the exactness claim for fixed recourse.
- `relevance:` (i) The strongest exactness result in the batch for the essay's target structure: with fixed W, the vertex restriction is value-preserving in both directions. (ii) It is a reduction of the *fully adaptive* problem, so it establishes that the adaptive optimum is attained on vertices; it does not claim the optimal policy is affine. (iii) Fully covers fixed-recourse, RHS-only, vertex-represented uncertainty. This block should be the essay's anchor for "vertex representation is enough if recourse is fixed".

### 06-c4 — the vertex reduction fails under random recourse
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 6
- `printed_page:` 5
- `quote:` "Hence, x∗ is feasible for the constraints induced by each ξ ∈ vert([0, 1]) but infeasible for ξ = 0.5, providing a counter-example to Lemma 1 when W is an affine function of ξ."
- `gloss:` With W(ξ) = −1 + 2ξ, T(ξ) = −2 + 3ξ, h = 0 and Ξ = [0,1], the point x* = 1 satisfies the constraints at both endpoints but violates the constraint at the interior point ξ = 0.5.
- `relevance:` (i) None — a pure impossibility witness. (ii) It is the sharpest necessity result in the batch: fixed recourse is not a technical convenience but the exact hypothesis under which vertex reduction is valid. (iii) It closes the vertex-represented case negatively for random recourse, so the essay can state a clean dichotomy: vertex representation + fixed W ⇒ exact (06-c3); vertex representation + W(ξ) ⇒ can fail at a single interior point.

### 06-c5 — bilinear maxima over a polytope are attained at vertices
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 7
- `printed_page:` 6
- `quote:` "Lemma 2 Let P be a polytope, Q a closed and bounded set, and f (p, q) a bilinear function. It holds that {max f (p, q) s.t. p ∈ P, q ∈ Q} = {max f (p, q) s.t. p ∈ vert(P), q ∈ Q}."
- `gloss:` A bilinear objective over a polytope attains its maximum at an extreme point of that polytope, regardless of the other variable's set.
- `relevance:` (i) The technical engine behind the vertex reduction in the separation problem. (ii) Because it is bilinear, it does not generalize to the fully adaptive constraint system without the recourse assumption — that is exactly what 06-c4 exploits. (iii) Directly supports treating a vertex-represented set as a finite scenario list inside a separation oracle.

### 06-c6 — 0-1 affine images make the separation an MILP
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 9
- `printed_page:` 8
- `quote:` "Theorem 2 Let x∗ ∈ R|I| be given and suppose that we know a 0 − 1 polytope Ω ⊂ R|K0| and an affine mapping a(ω) = Aω + b such that Ξ = a(Ω)."
- `gloss:` If the uncertainty polytope is an affine image of a 0-1 polytope, the Farkas separation problem linearizes to a mixed-integer program; the budgeted set {ξ ∈ [0,1]^K : Σ ξ_k ≤ Γ} satisfies this.
- `relevance:` (i) A representational sufficient condition on U for tractable exact solution (not for affine exactness). (ii) It restricts which vertex-represented sets are computationally usable, which matters for any vertex-count exactness claim. (iii) Covers the budget set (vertex-represented), so a budget uncertainty set is simultaneously vertex-represented and MILP-separable — a useful conjunction for the essay.

### 06-c7 — budget integrality changes which exact method wins
- `file:` corpus/06_Ayoub_Poss_2016.pdf
- `sha256:` f7dd561ed79a7caedbccdf41e72fa6097613f21416a573ac2de1cd210fd4c8d6
- `pdf_page:` 15
- `printed_page:` 14
- `quote:` "when Γ is integer, RCG clearly outperforms RG, and the performance of RCG is close to the one of affine routing. In contrast, when Γ is fractional, RCG is outperformed by RG and both algorithms behave much worse than affine routing."
- `gloss:` For the budgeted polytope, integral Γ keeps the vertex structure sparse enough that row-and-column generation tracks affine routing; fractional Γ inflates the vertex count and the exact method loses badly.
- `relevance:` (i) An empirical statement about exact-solver cost, not about exactness of affine. (ii) It shows the vertex count is the operative quantity: fractional Γ increases generated extreme points and destroys the exact method's advantage. (iii) Directly relevant to the target class: the budget set's integrality is a vertex-complexity parameter, and the essay can use this as evidence that "vertex-represented" is not a single difficulty class. Note also that in Table 1 several rows have gap_dyn = gap_aff exactly (e.g. janos-us K=20, Γ=1.0: 7.2% and 7.2%), i.e. affine captures the whole observed adaptivity gain on those instances.

---

## 5. Bertsimas & Georghiou 2014 — affine is generically not the exact class

Paper: "Design of Near Optimal Decision Rules in Multistage Adaptive Mixed-Integer Optimization". Its value for the essay is negative and classificatory: the exact optimal rule class is piecewise linear, affine is the P = 1 special case, and the gap is quantified both worst-case and empirically.

### 20-c1 — worst-case O(√k) suboptimality of linear decision rules
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 2
- `printed_page:` 2
- `quote:` "decision rules generically sacrifice a significant amount of optimality in return for scalability. Indeed, Bertsimas and Goyal [11] have shown that the worst-case cost associated with linear decision rules can be O(√k) suboptimal when applied to two-stage robust optimization problems with k uncertain parameters."
- `gloss:` Linear/affine rules can be a factor of order √k worse than fully adaptive in the worst case, where k is the number of uncertain parameters.
- `relevance:` (i) None — a dimension-dependent lower bound on the gap. (ii) It is the batch's clearest statement that affine exactness cannot hold in general and that the failure rate grows with the ambient uncertainty dimension. (iii) It does not restrict U's geometry, so it applies a fortiori to vertex-represented sets: growing k means growing vertex count, and the √k bound is compatible with a polytope.

### 20-c2 — the exact optimal rule is piecewise linear
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 2
- `printed_page:` 2
- `quote:` "The aforementioned work also shows that the optimal decision rule for adaptive optimization problems is piecewise linear."
- `gloss:` The exact adaptive policy is piecewise linear in the uncertain parameter, so any claim that affine is exact requires the piecewise structure to collapse to a single piece.
- `relevance:` (i) Identifies the exact class, which makes the affine question a question about when a single affine piece suffices. (ii) Any counterexample can be read as a case needing at least two pieces; this is a useful diagnostic for the essay's negative section. (iii) It applies to polyhedral Ξ with vertex structure, so a vertex-represented set is exactly the regime where piecewise-linear rules are the natural exact object.

### 20-c3 — optimal rules are piecewise linear continuous, hence in PC
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 5
- `printed_page:` 5
- `quote:` "Since the optimal decision rules for Problem (3) are piecewise linear continuous functions, see [4, Theorem 2], the optimal solution of Problem (3) is an element of PC."
- `gloss:` The optimal continuous recourse rule lies in the paper's PC space of differences of two max-of-P-linear functions; the citation is to Bemporad–Borrelli–Morari.
- `relevance:` (i) A representation theorem for the exact class, not for affine. (ii) It shows affine (P = 1, single piece, no max) is a strict sub-class of the exact class whenever more than one piece is needed. (iii) For a vertex-represented polyhedral Ξ this is the relevant exact benchmark against which affine must be compared.

### 20-c4 — every piecewise linear continuous function is representable
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 5
- `printed_page:` 5
- `quote:` "Theorem 1 Every piecewise linear continuous function defined over a compact set Ξ is an element of PC."
- `gloss:` The PC representation (max of P linear functions minus max of P linear functions) is lossless for all continuous piecewise-linear functions on a compact Ξ.
- `relevance:` (i) Establishes that the restricted class used to search for rules is not itself a source of error — the error comes from fixing P, not from the representation. (ii) With P = 1 the class is exactly affine, so the paper gives a clean nested hierarchy affine ⊂ PC(P) ⊂ exact. (iii) Applies to any compact Ξ, including vertex-represented polytopes, so the hierarchy is available in the essay's target setting.

### 20-c5 — empirical gap of affine rules: 20% to 60%
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 28
- `printed_page:` 28
- `quote:` "In general, the linear decision rules produce suboptimal solutions. The average relative gap is more than 20% and can reach 60%."
- `gloss:` In the two multistage inventory experiments, the affine (linear decision rule) gap averages above 20% and peaks near 60%, while the piecewise-linear rules stay under 5%.
- `relevance:` (i) None — quantitative evidence of non-exactness. (ii) It gives the essay a concrete magnitude for "the gap can be large in practice", complementing the worst-case √k rate. (iii) These are multistage inventory problems with polyhedral uncertainty; they are vertex-represented in principle, so the numbers are a warning that vertex representation does not imply affine exactness.

### 20-c6 — the affine gap is tied to the geometry of the uncertainty set
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 20
- `printed_page:` 20
- `quote:` "Bertsimas and Bidkhori [9] show that the quality of linear decision rules is directly linked with the geometric properties of the uncertainty set."
- `gloss:` The paper adopts, by citation, the thesis that the size of the affine gap is a geometric property of U rather than a property of the cost data.
- `relevance:` (i) Direct support for the essay's organizing claim that exactness is a geometry question. (ii) It is a citation, not a theorem in this paper, so the essay must attribute it correctly and not present it as proved here. (iii) It is geometry-agnostic, hence consistent with the vertex-count hypothesis, but supplies no vertex-specific criterion.

### 20-c7 — polyhedral Ξ with an explicit vertex-compatible parametrization
- `file:` corpus/20_Bertsimas_Georghiou_2014.pdf
- `sha256:` 616e78f2a90571ce3a4d2f562d9dc63809c91f3f96101da6936d2561421c5469
- `pdf_page:` 4
- `printed_page:` 4
- `quote:` "Here, we assume that Problem (1) has a non-empty and bounded feasible region and the uncertainty set Ξ is a nonempty, convex and compact polyhedron"
- `gloss:` The uncertainty set is the polyhedron Ξ = {ξ ∈ R^k : Wξ ≥ g, ξ1 = 1}, with ξ1 = 1 fixing the affine constant term; the quoted clause is followed immediately by that displayed definition, which is why it ends without a period. The paper works entirely in this polyhedral class.
- `relevance:` (i) Confirms that the paper's negative results live in the polyhedral, hence vertex-representable, class. (ii) It means the 20–60% gaps are not artifacts of a non-polyhedral set. (iii) Directly covers the essay's vertex-represented setting on the negative side: polyhedral U does not rescue affine exactness.

---

## 6. Haddad-Sisakht & Ryan 2018 — checkable conditions for a provably nonzero gap

Paper: "Conditions under which adjustability lowers the cost of a robust linear program". This is the most surgical paper in the batch on the *negative* side: it gives a numerical, checkable sufficient condition for `Z^AARC < Z^RC` in exactly the fixed-recourse + box setting, plus a same-vertex exactness remark, plus the observation that published exactness conditions are not necessary.

Model: fixed recourse, uncertain A and b, box uncertainty χ = {ξ : |ξ_l| ≤ ρ_l}, x, y ≥ 0. Table 1 records the scope: "This paper — A and b — Box uncertainty set and x, y ≥ 0".

### 08-c1 — the value sandwich that makes an AARC gap sufficient
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 4
- `printed_page:` 188
- `quote:` "Because Z A RC ≤ Z A A RC ≤ Z RC , conditions under which Z A A RC < Z RC are sufficient for Z A RC < Z RC as well."
- `gloss:` Since affine rules sit between fully adaptive and static, any instance where the affine value beats the static value also certifies that full adjustability beats static.
- `relevance:` (i) None — it is the logical scaffolding for a negative result. (ii) It converts a computable affine gap into a certified adaptivity gap, which is the essay's "gap provably nonzero" target. (iii) It applies verbatim to fixed-recourse RHS-only box uncertainty, which is the target class with U a box (2^L vertices).

### 08-c2 — the structural mechanism behind a gap
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 4
- `printed_page:` 188
- `quote:` "As detailed below, adjustability may lower the cost if there are at least two constraints that are binding at an optimal RC solution for different values of the same uncertain parameter."
- `gloss:` A gap needs the same uncertain parameter to bind two different constraints at two different worst-case values, with a shared adjustable variable that is bounded above in one and below in the other.
- `relevance:` (i) Gives an interpretable sufficient pattern, and thereby indicates what must be *absent* for exactness. (ii) It is a structural necessary-ish signature: without cross-constraint sharing of a perturbation there is no gap (see 08-c4). (iii) Directly relevant to a vertex-represented box: the two different worst-case values are two distinct vertices of the box, so the mechanism is explicitly a two-vertex phenomenon.

### 08-c3 — Proposition 1: an explicit numerical gap certificate
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 7
- `printed_page:` 191
- `quote:` "There exist two binding constraints indexed by j, k ∈ {1, . . . , m}, j = k, where relaxing either of these constraints strictly improves Z RC , and ξ̂ j = ξ̂k , where ξ̂ j and ξ̂k are defined in Definition 2."
- `gloss:` Condition 1 of Proposition 1 (the "j = k" is the text layer's rendering of j ≠ k): two constraints are binding at the RC optimum at the same worst-case value of a shared perturbation; conditions 2-3 add that a shared perturbation appears in both constraints and that a basic adjustable variable has opposite-signed coefficients d_jr·d_kr < 0 in them, after which inequality (14) certifies Z^RC > Z^AARC.
- `relevance:` (i) A sufficient condition, checkable from one RC primal-dual solve, for a strict affine gap. (ii) It is numerical rather than structural: it needs the RC optimum, so it certifies instances but does not characterize the class. (iii) Fully covers fixed-recourse box uncertainty with RHS/coefficient uncertainty; this is the closest result in the batch to a test for the essay's exact question, but it tests non-exactness, not exactness.

### 08-c4 — same worst-case vertex ⇒ no gap from that variable
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 11
- `printed_page:` 195
- `quote:` "Note also that if condition 2 does not hold, then the uncertainty is constraint-wise, and Z A RC equals Z RC (Ben-Tal et al. 2004; Marandi and den Hertog 2017)."
- `gloss:` Failure of cross-constraint sharing of a perturbation is exactly constraint-wise uncertainty, which is a known exact regime; and Remark 2 shows that even with sharing, equal worst-case values at the two binding constraints make the affine coefficient vanish and restore equality.
- `relevance:` (i) Identifies two distinct exact regimes: constraint-wise structure, and a shared perturbation whose two binding constraints are worst-case at the same value. (ii) The second is a "same-vertex" condition, i.e. a genuine necessary condition inside this two-constraint family. (iii) Directly addresses vertex geometry: if the adversarial solution uses one vertex for both constraints, affine cannot help there.

### 08-c5 — a fully worked strict gap
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 13
- `printed_page:` 197
- `quote:` "This example illustrates the case in which all conditions of the proposition are satisfied along with (14) so that Z RC > Z A A RC ."
- `gloss:` Example 3 is a two-constraint, one-parameter box instance (ξ ∈ [−1,1]) satisfying all three conditions, with the two constraints binding at opposite endpoints ξ = −1 and ξ = +1; the optimal affine recourse rule is explicitly nonconstant and the affine value is strictly below the static value. Exact numeric values are not reproduced here because the stacked fractions in the text layer are ambiguous in this copy (`page: uncertain` for the fractions only).
- `relevance:` (i) None — an existence witness. (ii) It is a minimal, hand-checkable strict gap in the fixed-recourse box setting, so it can serve as a regression test for any proposed exactness criterion: the criterion must declare this instance non-exact. (iii) Covers a two-vertex box exactly, which makes it the smallest possible vertex-represented counterexample to affine exactness in this model class.

### 08-c6 — published sufficient conditions are not necessary
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 18
- `printed_page:` 202
- `quote:` "Three contrived instances illustrate that, although the models are not covered by conditions previously established for Z A RC = Z RC , nevertheless Z A A RC is equal to Z RC ."
- `gloss:` Instances outside the known sufficient exactness conditions can still be affine-exact, so the existing sufficient conditions (constraint-wise, symmetry, nonnegative packing) are strictly not necessary.
- `relevance:` (i) Directly warns against treating the known sufficient conditions as a characterization. (ii) It is the cleanest published statement in the batch that the exactness frontier is not yet mapped. (iii) Applies to fixed-recourse box problems, so the gap in the literature exists inside the essay's target class.

### 08-c7 — stated scope: fixed recourse and box only
- `file:` corpus/08_HaddadSisakht_Ryan_2018.pdf
- `sha256:` 0fc0e659a6003b9705c3f253a6ce0d2ededc6df9e0b0cc063eb926b523685f0f
- `pdf_page:` 18
- `printed_page:` 202
- `quote:` "In this paper we considered the fixed recourse case only. For uncertainty-affected recourse a similar approach would introduce more computational complexity that is a subject for future research. Another extension could be including more sophisticated uncertainty sets beyond box uncertainty."
- `gloss:` The results are restricted to fixed recourse and box uncertainty, and the authors name random recourse and richer U as open extensions.
- `relevance:` (i) Confirms the positive scope is exactly one half of the essay's target class. (ii) It flags the two open directions the essay can position against: random recourse and non-box sets. (iii) Half-covers the target: fixed recourse yes, RHS-only yes (b uncertainty is allowed), box is vertex-represented yes — but coupled vertex sets such as budget are explicitly out of scope.

---

## Marginal notes

#### Ranking: how directly each paper answers "when is the affine rule exact, and when is the gap provably nonzero"

**1. Bertsimas, Goyal & Lu 2015 (04).** The only paper here with a
necessary-and-sufficient geometric criterion for a policy class (convexity of
T(U,h) for all h, for the **static** class), a tight approximation factor equal
to the non-convexity measure, and a parameterized family that attains the factor
exactly. It answers both halves of the question in one framework. Two limits
must be stated in the essay: the theorem is about **static** solutions, so it is
a sufficient condition for affine exactness and a converse only within the
static class; and the base model is a nonnegative packing problem, with RHS
uncertainty relegated to §4.1. It is still first by a wide margin.

**2. Ayoub & Poss 2016 (06).** It answers a *different* question exactly: for
the fully adjustable problem with fixed recourse and polyhedral U, the vertex
restriction is value-preserving in both directions, and with random recourse it
fails at a single interior point. If the essay's real object is "fixed-recourse,
RHS-only, vertex-represented", this paper gives the cleanest true statement
about it — but it says nothing about affine exactness, because it does not need
affine at all. Rank it second for coverage of the target structure, not for
coverage of the affine question.

**3. Haddad-Sisakht & Ryan 2018 (08).** The only paper that gives a
*checkable* certificate of a strictly nonzero affine gap in the fixed-recourse
box setting, plus the same-vertex exactness condition (08-c4), plus the explicit
warning that known sufficient conditions are not necessary (08-c6). It is the
most useful paper for building the essay's negative test suite. It ranks below
06 because its conditions are instance-level numerics rather than a structural
characterization, and it is box-only.

**4. Bertsimas & de Ruiter 2016 (05).** Supplies the cleanest definition of the
target class (fixed recourse, RHS-only, polyhedral), an exact dual
reformulation, and one genuine vertex-count exactness sentence. It does not
attempt a characterization: the paper's exactness content is reformulation
equivalence, not policy exactness. Rank it fourth: indispensable for the
setup, weak for the verdict.

**5. Bertsimas & Georghiou 2014 (20).** Answers "is affine generically exact?"
with a clear no: O(√k) worst case, 20–60% observed, and the exact class is
piecewise linear. It does not answer "when is it exact". Its structural value is
the nested hierarchy affine ⊂ PC(P) ⊂ exact and the demonstration that the
negative results live inside the polyhedral (vertex-representable) class.

**6. Ben-Tal & Nemirovski 1999 (01).** No recourse, therefore no affine rule.
Its contribution is the geometry-to-tractability dictionary and the
constraint-wise worst-instance theorem, both of which are the ancestors of the
later exactness conditions. Cite it for lineage and for the constraint-wise
criterion; do not cite it for anything about affine rules.

#### Which paper supplies the sharpest negative family

**04, Theorem 7.** The family
`U^θ = {B ∈ [0,1]^{n×n} : B_ij = 0 ∀ i ≠ j, Σ_j B_jj^θ ≤ 1}`, θ > 1, gives
`κ(T(U^θ,h)) = n^{1/θ}` for every h > 0 and hence `z_AR / z_Rob = n^{1/θ}`.
Choosing `θ = log_μ n` produces a ratio exactly equal to any prescribed
`μ > 1`, for any `n`. Three properties make it the sharpest: the gap is
*attained* by the geometric measure rather than merely bounded by it; the target
gap is an input to the construction, so it is unbounded; and `U^θ` is a convex,
down-monotone, vertex-represented polytope in the nonnegative orthant, so it
cannot be dismissed as an artifact of a pathological set. It is a static-vs-adaptive
family, so it proves that affine cannot be exact here a fortiori.

Runner-up, for a different purpose: **06's random-recourse counterexample**
(`W(ξ) = −1 + 2ξ`, `T(ξ) = −2 + 3ξ`, `Ξ = [0,1]`, infeasible at `ξ = 0.5`
while feasible at both vertices). It is the sharpest *structural necessity*
witness in the batch — one constraint, one parameter, exact midpoint failure —
and it is what a proof of the vertex-reduction theorem has to exclude. It is not
an affine-gap family, so it belongs in the "necessary conditions" section, not
the "affine suboptimality" section.

#### Coverage of the essay's target configuration

Target: fixed recourse, RHS-only uncertainty, uncertainty set given by its
vertices.

| Paper | Fixed recourse | RHS-only | Vertex-represented U | Verdict for the target |
|---|---|---|---|---|
| 01 | n/a (no recourse) | n/a | polytope ⊂ ellipsoidal (01-c7) | No affine content; supplies constraint-wise criterion only |
| 04 | no (B uncertain) | only §4.1 | convex compact; vertices used in proofs | Partial; static exactness criterion, plus RHS-only sufficient condition 04-c8 |
| 05 | yes (05-c1) | yes | polyhedral; vertex-count remark 05-c4 | Full setting, no exactness characterization |
| 06 | yes (needed for 06-c3) | RHS via h, plus T(ξ)x | yes (Lemma 1) | Full and exact — for the fully adaptive problem, not for affine |
| 20 | yes for B, but recourse is mixed continuous/binary | yes in the data (Cξ) | polyhedral (20-c7) | Full geometry, negative verdict only |
| 08 | yes (08-c7) | yes (A and b) | box = 2^L vertices | Full setting; checkable non-exactness conditions, no characterization |

#### Three claims the essay must not make

1. Do not write "affine rules are exact iff T(U,h) is convex". That is 04's
   theorem for **static** rules. For general affine rules the convexity of
   T(U,h) is sufficient (since static ⊂ affine) but the converse is not proved
   there.
2. Do not write "vertex representation implies exactness". 04-c7 is a
   vertex-represented polytope with an arbitrarily large static/affine gap, and
   06-c4 shows the vertex reduction itself can fail once recourse is random.
3. Do not write "the gap bound fails for RHS uncertainty". 04 states that the
   *non-convexity bound* does not extend to U^{B,h} because that set is not
   down-monotone, while the *exactness* statement (Theorem 6) does hold under
   constraint-wise U^{B,h}. These are two different failures and the essay
   should keep them apart.
