# Reading proposal for the essay; blocks NOT yet registered in the science graph.

Target: exactness of affine/linear decision rules (LDR) in two-stage adaptive robust optimization,
and its copositive/conic characterizations. All six PDFs read with `pdftotext -layout`, page by page.
Every `quote:` below was machine-checked to be a verbatim substring of the extracted page text.
Normalisation applied when checking: whitespace collapsed; ligatures (fi/fl/ffi) expanded;
end-of-line word division silently rejoined (so printed "Unfor-/tunately" is quoted
"Unfortunately"); genuine compound hyphens such as "non-adjustable" are kept. No other edits.
A few quotes end at a colon that introduces a display equation; that display is described in `gloss:`.

## Files and hashes (from `corpus/MANIFEST.md`)

| paper | file | sha256 | type |
|---|---|---|---|
| 03 | `corpus/03_Chen_Zhang_2009.pdf` | `d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a` | journal article, OR 57(6) 1469-1482 |
| 15 | `corpus/15_Chuong_Jeyakumar_2020.pdf` | `a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5` | journal article, JOTA (online first) |
| 16 | `corpus/16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf` | `386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef` | journal article, Optimization (online first) |
| 17 | `corpus/17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf` | `48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65` | journal article, J. Global Optim. |
| 18 | `corpus/18_Jeyakumar_etal_2022.pdf` | `13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd` | journal article, SVVA 30:1363-1380 |
| 19 | `corpus/19_Zhang_2024.pdf` | `8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941` | journal article, JOTA (online first) |

Page convention: `pdf_page` is the physical PDF page (1-based). `printed_page` is the number
actually printed on the page; where the PDF carries no printed folio, this is stated as uncertain.
For `03_Chen_Zhang_2009.pdf` the page has two columns, so text was extracted per column
(left/right halves at x=0/306 pt); the printed folio is PDF page + 1468.
For `16_..._2021a.pdf` the printed folio is PDF page - 1; for `18_..._2022.pdf` it is PDF page + 1362.
Caveat on `03`: that PDF embeds a non-Unicode math font, so several set/vector symbols are dropped
by pdftotext (and the infinity glyph becomes a control character). Quotes below therefore avoid
fragments containing those glyphs, and this is flagged where a result is described but not quoted.

## How to read the `relevance:` field

- **(i)** bearing on a necessary-and-sufficient condition for LDR exactness;
- **(ii)** bearing on the gap between the affine policy and the exact adaptive optimum;
- **(iii)** bearing on whether the deterministic worst-case bridge class
  (`x(t+1)=Ax+Bu+Ew`, `A=I`, `w in {-1,+1}^p`, boxed `u`, terminal `||x_T||_1`, closure set `R`)
  sits inside a known exact class.


## P03 — Chen & Zhang 2009 — Extended affinely adjustable robust counterparts

- `file:` 03_Chen_Zhang_2009.pdf
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a

### cz1 — cz-aarc-restriction

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 2, left column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 2
- `printed_page:` 1470
- `quote:` "Because the general adjustable robust counterpart is intractable, Ben-Tal et al. (2004) proposed a tractable approach for solving fixed-recourse instances using affine decision rules—restricting recourse variables as affine functions of the realization of the primitive uncertainties, referred to as the affinely adjustable robust counterpart (AARC)."
- `gloss:` The fully adaptive two-stage problem is declared intractable; the affine decision rule is introduced only as a tractable restriction of it, not as an exact representation.
- `relevance:` (i) No exactness condition is asserted: the text gives a restriction, so this is the "gap" side of the dichotomy, not a characterization. (ii) It fixes the reference optimum against which any gap must be measured. (iii) The bridge class is a finite-horizon policy over a sign tree; restricting to a single affine function of one w-vector is a strictly smaller class, so this statement does not place the bridge inside an exact class.

### cz2 — cz-aarc-too-restrictive

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 3, right column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 3
- `printed_page:` 1471
- `quote:` "The AARC is motivated by the belief that the change in recourse variables is often linear to small changes in data uncertainty. However, the AARC may be too restrictive, particularly in cases where linear dependency fails to be a good approximation, as illustrated in the following example."
- `gloss:` The paper explicitly states that linear dependence can be a poor approximation, and points to a concrete counterexample rather than to a condition.
- `relevance:` (i) Gives a negative answer for a whole class: no sufficient condition for exactness is offered, only a counterexample. (ii) This is the qualitative gap statement; no bound is given here. (iii) Directly relevant: the bridge objective is a sum of absolute values, whose exact response is piecewise linear, exactly the situation in which affine dependence "fails to be a good approximation".

### cz3 — cz-example-gap-N

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 6, left column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 6
- `printed_page:` 1474
- `quote:` "Hence, the optimal objective value of the EAARC is one. This is exactly the optimal objective value of the ARC, whereas the optimal objective value of the AARC is N ."
- `gloss:` On a norm-ball instance the adaptive optimum equals 1, the plain affine rule gives N, and the positive/negative-split rule recovers 1.
- `relevance:` (i) A sharp non-exactness witness for the plain affine class, with an exact alternative class attaining the optimum; the exact response there is |z|, which is not affine. (ii) The gap is the factor N, i.e., unbounded in the dimension. (iii) This is the closest structural analogue to the bridge in the six papers: L1-type cost, sign-symmetric uncertainty, exact policy equal to an absolute-value response rather than an affine one.

### cz4 — cz-thm1-feasible-set-equality

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 4, right column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 4
- `printed_page:` 1472
- `quote:` "In this following, we show that XEAARC = X0 ."
- `gloss:` Theorem 1 states equality between the extended (vertex-weight reparameterized) affine feasible set and the fully adaptive feasible set X0, when the uncertainty set is a polytope given by its extreme points and the extended set is the same polytope lifted with those weights.
- `relevance:` (i) This is an equality (both inclusions), hence the strongest exactness statement in the six papers, but it concerns the reparameterized class, not the plain affine class. (ii) It says the gap can be closed, without quantifying the cost. (iii) Because a sign box has exactly 2^p vertices, a two-stage collapse of the bridge fits the hypothesis - at the price of 2^p auxiliary blocks; the theorem does not address T-stage ladders.

### cz5 — cz-extreme-points-exponential

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 4, right column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 4
- `printed_page:` 1472
- `quote:` "Unfortunately, in general, for a polyhedral set defined by linear equalities and inequalities, the number of extreme points is exponential in terms of the number of constraints of the polyhedral set, and we may end up with an intractable formulation."
- `gloss:` The vertex-weight construction that guarantees exactness has a cost exponential in the number of constraints of the uncertainty set.
- `relevance:` (i) Turns the exactness result into a hardness statement about the exact class: exact but not tractable. (ii) The gap can be closed only by paying an exponential price. (iii) At bridge scale (p sign coordinates) 2^p blocks is out of reach, so the exact class exists formally but is not a usable certificate.

### cz6 — cz-dual-zero-iff

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 5, right column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 5
- `printed_page:` 1473
- `quote:` "It is clear that the feasibility problem (7) is feasible if and only if its dual has an optimal objective value zero."
- `gloss:` Membership in the affine-rule feasible set is equivalent to a conic dual attaining value zero; this is the paper's only literal iff certificate.
- `relevance:` (i) This is an iff condition, but for feasibility of the rule-restricted system, not for equality with the adaptive optimum; it certifies a point, not exactness of the class. (ii) No gap information. (iii) Supplies the conic-dual shape a bridge-side check would take if the bridge is modeled with vertex weights.

### cz7 — cz-further-splitting-no-gain

- `file:` 03_Chen_Zhang_2009.pdf
- `extract:` `pdftotext -layout`, PDF page 9, left column
- `sha256:` d914cd0f32887706473f189c4dd464eeee982efe397a9084cd5684f10ec3418a
- `pdf_page:` 9
- `printed_page:` 1477
- `quote:` "It is obvious that for any feasible solution of problem (18) for general K, we can construct a feasible solution for problem (15) with the same objective value."
- `gloss:` Refining the positive/negative split into K>1 blocks per coordinate yields no better value than the single split, under the normalization (17).
- `relevance:` (i) A negative structural result: within this family, more auxiliary freedom does not buy exactness. (ii) Rules out a natural route to shrinking the gap. (iii) Important caveat for the bridge: the companion Theorem 5 (PDF p. 7, printed 1475; described here, not quoted, because the infinity and set glyphs are dropped by the embedded font) states that for the infinity norm with finite radii the split extended set yields the same feasible set as the un-split extension, and the paper glosses this as the EAARC not improving on that extension - and a sign box is exactly such an infinity-norm set, so splitting cannot help the bridge; a different reparameterization would be required.


## P15 — Chuong & Jeyakumar 2020 — Generalized Farkas lemma with adjustable variables

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5

### q1 — qj-mapping-intractability

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 2
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "However, even two-stage robust optimization problems with adjustable variables are in general computationally intractable. Indeed, the second-stage adjustable decision is a mapping and so it is generally very difficult to establish numerically verifiable solvability characterizations or approximations of the system with a mapping unless the system is restricted to some special classes of mappings."
- `gloss:` The hardness is located in optimizing over mappings, and it is overcome only by restricting to a special class of mappings.
- `relevance:` (i) Frames exactness as a property of a mapping class, not of the data; no iff is claimed. (ii) The unrestricted adaptive optimum is the object that is hard to even describe, so any gap statement must be against a value that is itself only semialgebraically characterized. (iii) The bridge policy is a non-anticipative mapping on a sign tree, so it is in the same "mapping" category and is not covered by any result here.

### q2 — qj-parameterized-affine-rule

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 4, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 4
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "We now introduce a parameterized affine rule, where the mapping x(·) satisfies the rule:"
- `gloss:` The affine rule is x(u) = rho*y + (1-rho)*W*u with a scale parameter rho in [0,1]; for rho in (0,1) this is the standard affine rule after rescaling.
- `relevance:` (i) Defines the class whose exactness is at issue; the scale parameter does not enlarge the class. (ii) No gap result attached. (iii) The bridge ladder is not of this form: its policy class is indexed by closure sets, not by a scalar rescaling of one affine map.

### q3 — qj-farkas-iff

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 5, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 5
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Suppose that the cone C in (5) is closed. Then, the following statements are equivalent:"
- `gloss:` Under closedness of the cone generated by the data, non-negativity of a linear form over the affine-rule system is equivalent to the existence of finitely many multipliers satisfying linear matrix inequalities.
- `relevance:` (i) This is the only literal iff characterization of the affine-restricted system in the six papers; the "only if" direction is obtained from Hahn-Banach separation plus a variable transformation. (ii) It equates two descriptions of the same rule-restricted object, so it says nothing about the distance to the adaptive optimum. (iii) A conic certificate of this shape is what a bridge-side exactness proof would have to produce, but the bridge would need one cone per closure pattern.

### q4 — qj-strong-duality-sdp

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 15, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 15
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Theorem 3.1 (Strong duality with SDP duals) Let the feasible set of problem (RP) be non-empty and let the following cone C P be closed, where"
- `gloss:` For spectrahedral uncertainty, the infimum of the affinely adjustable two-stage linear program equals the maximum of an explicit semidefinite dual; the only hypothesis beyond non-emptiness is closedness of the cone CP.
- `relevance:` (i) An exact reformulation of the AARC, not an exactness result for the AARC against the ARC; the qualification is a regularity condition, not a condition on when affine rules are optimal. (ii) No gap statement. (iii) This is the "conic characterization" template the essay can cite for the reformulation side, and it is unconditional once CP is closed.

### q5 — qj-socp-ellipsoid

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 20, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 20
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Corollary 3.1 (Strong duality with SOCP duals) Consider the problem (RP) with U in (2) replaced by E in (40), and let the feasible set of problem (RP) be non-empty."
- `gloss:` Under ellipsoidal uncertainty the semidefinite dual collapses to a second-order cone program with the same optimal value.
- `relevance:` (i) A tractable subclass of the reformulation, still not an exactness class for the rule. (ii) Nothing about the gap. (iii) Speaks to tractability, not to the bridge, whose uncertainty set is a polytope of sign vectors rather than an ellipsoid.

### q6 — qj-closedness-sufficiency

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 23, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 23
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Proposition 3.1 (Sufficiency for the closedness of C P ) Assume that one of the following conditions holds: (a) The uncertainty set U of problem (RP) is a polytope; (b) The Slater condition holds for the problem (RP)"
- `gloss:` The closedness hypothesis of the strong duality theorem is automatically satisfied for polytopal uncertainty or under a strict Slater condition.
- `relevance:` (i) Purely sufficient, not necessary; it qualifies the duality theorem, not LDR exactness. (ii) No gap content. (iii) Since the bridge uncertainty is a polytope, this is the condition under which the conic dual of the affine-rule problem is exact for the bridge in its two-stage collapse.

### q7 — qj-exact-conic-program

- `file:` 15_Chuong_Jeyakumar_2020.pdf
- `extract:` `pdftotext -layout`, PDF page 3, single column
- `sha256:` a8f46660154d09ffa89f5b0c6dc54ba3ece4835214871b8eafd31944ed5e82e5
- `pdf_page:` 3
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "We utilize a general closed cone regularity condition, which guarantees that strong duality holds between the primal and dual pairs, and hence obtain an exact conic linear program for the two-stage robust program."
- `gloss:` The authors describe their output as an exact conic program for the two-stage robust program, meaning exact for the affine-restricted program.
- `relevance:` (i) The word "exact" here is about the conic reformulation, and the sentence should not be read as a claim that affine rules are exact; this is the main terminological trap in the paper. (ii) No gap statement. (iii) Useful as a warning for the essay: "exact SDP" in this literature almost never means "affine rule is optimal".


## P16 — Chuong, Jeyakumar, Li & Woolnough 2021a — Exact dual SDPs for affinely adjustable SOS-convex problems

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef

### r2 — cj-affine-rule-circumvention

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 6, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 6
- `printed_page:` 5
- `quote:` "Following Ben-Tal et al. [10], we circumvent the intractability, in this paper, by imposing the second-stage decision variable w(·) to satisfy the affine decision rule (see e.g. [10, Page 356]) given by"
- `gloss:` The affine rule w(u) = y0 + W u with a full matrix W is imposed as a modeling restriction to obtain tractability.
- `relevance:` (i) Restriction, not characterization. (ii) The gap is left entirely open. (iii) The full matrix W is at least the right shape for a policy that couples all uncertain coordinates, unlike the diagonal rule of paper 19.

### rA — cj-assumption-A

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 7, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 7
- `printed_page:` 6
- `quote:` "Assumption A: We assume for (RT) that h0 , hl : Rs × Rν → R and pil :"
- `gloss:` The exact dual SDP requires: objective and constraints separable in first-stage (x,y) and SOS-convex in x, affine in the second-stage variable, and affine data dependence on u.
- `relevance:` (i) This is a sufficient structural condition for exact duality of the rule-restricted problem; it is silent on whether the rule itself is optimal. (ii) No gap. (iii) The bridge has a polyhedral (L1) rather than SOS-convex objective, so Assumption A is not met by the bridge without reformulation.

### rB — cj-thm-exact-dual

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 8, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 8
- `printed_page:` 7
- `quote:` "Theorem 2.1 (Exact dual SDP for (RT)): For the problem (RT), let inf (RT) > −∞ and Assumption A be satisfied."
- `gloss:` Under Assumption A and a strict-feasibility (Slater-type) condition, the infimum of the affinely adjustable problem equals the maximum of an explicit SDP, with dual attainment.
- `relevance:` (i) Exactness of the dual reformulation under a constraint qualification; the qualification is regularity, not optimality of the rule. (ii) No gap. (iii) Confirms the pattern: in this school "exact SDP" is always exactness of the reformulation.

### r3 — cj-cq-exactness

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 4, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 4
- `printed_page:` 3
- `quote:` "More specifically, we show that, under a constraint qualification, the optimal values of the two-stage affinely adjustable robust optimization problem and its associated dual program are equal with the solution attainment of the dual problem."
- `gloss:` The paper's headline exactness is equality between the affine-rule primal and its dual, conditional on a constraint qualification.
- `relevance:` (i) This is the precise thing that is and is not claimed: primal-dual equality, not affine-adaptive equality. (ii) Nothing about the adaptive gap. (iii) The essay should cite this as a conic dual characterization, not as an LDR exactness theorem.

### r4 — cj-np-hard-nonaffine

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 13, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 13
- `printed_page:` 12
- `quote:` "Indeed, it is known that, solving even a single-stage convex quadratic robust optimization with quadratic constraints with an uncertainty set that is the intersection of ellipsoids under a non-affine uncertainty dependency is NP-hard"
- `gloss:` Once the data depend non-affinely on the uncertain parameter, even the single-stage robust quadratic problem with an intersection-of-ellipsoids set is NP-hard.
- `relevance:` (i) An impossibility boundary: it explains why the affine-dependence assumption is not cosmetic. (ii) Hardness, not gap. (iii) The bridge dynamics are affine in w, so the bridge is on the tractable side of this particular boundary - the hardness there would come from the policy class, not from the data map.

### r5 — cj-sos-not-tractable

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 13, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 13
- `printed_page:` 12
- `quote:` "Solving a robust two-stage optimization problem (RT) using the sum of squares problem involving SOS-convex polynomials is in general not numerically tractable."
- `gloss:` The paper concedes that the SOS-based exact dual is not computationally tractable in general; tractability is inherited only in the special cases it lists.
- `relevance:` (i) Even where an exact reformulation exists, it may be intractable, so exactness and tractability must be reported separately. (ii) No gap statement. (iii) Warns against treating any SOS exactness result as a computational certificate for the bridge.

### r7 — cj-optimality-characterization

- `file:` 16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf
- `extract:` `pdftotext -layout`, PDF page 20, single column
- `sha256:` 386dfa3b8fa7df897be45bf17bf32f5d8c54ef08ad840221cd17836d93b193ef
- `pdf_page:` 20
- `printed_page:` 19
- `quote:` "Corollary 2.4 (Characterization of solution for (RT)): For the problem (RT), let inf (RT) > −∞ and Assumption A be satisfied."
- `gloss:` A feasible affine-rule solution is optimal for the affine-rule problem if and only if there exist multipliers satisfying the LMI and SOS conditions (23)-(24).
- `relevance:` (i) This is the closest thing in the six papers to a necessary-and-sufficient optimality certificate, but it certifies optimality inside the affine class only. (ii) It cannot detect a positive gap to the adaptive optimum. (iii) The bridge would need the analogous certificate for its own policy class, which none of the papers supplies.


## P17 — Chuong, Jeyakumar, Li & Woolnough 2021b — Exact SDPs for box uncertainty under separable quadratic rules

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65

### s1 — cjw-box-hard

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 2
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "Unfortunately, no numerically tractable representation exists for a general non-negative non-convex quadratic function over boxes because a non-convex quadratic optimization problem over box constraints is a fundamental NP-hard global optimization problem [13]."
- `gloss:` There is no tractable exact conic representation of nonnegativity of a general nonconvex quadratic over a box, because that would solve an NP-hard problem.
- `relevance:` (i) The hardness boundary that forces the separable restriction. (ii) Not a gap statement. (iii) Crucial for the bridge: sign uncertainty is exactly a box, so any claim that a quadratic rule is exact over the bridge must survive this NP-hardness barrier unless separability is imposed.

### s2 — cjw-separable-qdr

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 6, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 6
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "We assume that the adjustable variable y(·) admits a separable quadratic decision rule of the form:"
- `gloss:` The rule is y(z) = y0 + Pz + (z^T Q_1 z, ..., z^T Q_s z) with each Q_r diagonal, i.e. affine plus a sum of single-coordinate quadratics.
- `relevance:` (i) Defines a strictly larger tractable class than the affine class, but not a characterization of when it is exact. (ii) No gap bound; the paper only reports numerical improvements over the affine rule. (iii) The rule has no cross terms in z, so it cannot represent a piecewise-linear L1 response such as |z|; the bridge value function is not additive in the sign coordinates, so this class does not obviously contain the bridge optimum.

### s3 — cjw-sos-iff

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 4, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 4
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "Theorem 2.1 (Semi-definite and SOS Representations) Let α ∈ R, u := (u 1 , . . . , u q ) ∈ Rq and W := diag(w1 , . . . , wq ) be a diagonal matrix, where w j ∈ R, j = 1, . . . , q. Then, the following statements are equivalent:"
- `gloss:` For a separable quadratic with diagonal quadratic part, nonnegativity over a box, an SOS representation, and an explicit 3x3 PSD feasibility system are pairwise equivalent.
- `relevance:` (i) A genuine iff, and the engine of every exactness claim in papers 17-19; it is a characterization of nonnegativity, not of policy optimality. (ii) No gap. (iii) This is the exact conic (LMI) lemma the bridge would need in a separable surrogate, and it is only valid because the quadratic part is diagonal.

### s4 — cjw-exact-sdp

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 7, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 7
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "Consider the adjustable robust linear program with the separable quadratic decision rule under the box data uncertainty (P) and the semidefinite programming problem (SDP). Then, inf(P) = inf(S D P)."
- `gloss:` The box-uncertain adjustable linear program under a separable quadratic rule has exactly the same optimal value as an explicit SDP.
- `relevance:` (i) Exactness of the rule-restricted problem under a fixed rule class; no condition under which the rule class is optimal is given. (ii) The gap to the adaptive optimum is neither bounded nor discussed. (iii) Applies to a box - the bridge shape - but under a separable rule, which is the wrong symmetry for an L1 value function.

### s5 — cjw-exact-lp

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 11, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 11
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "Corollary 3.3 (Exact LP Reformulation) For the problem (LP), it holds that inf(L P) = inf(S D P L) = inf(L D P),"
- `gloss:` With the affine rule, the SDP collapses to a linear program whose value equals the robust affine-rule value; the reformulation is the usual absolute-value epigraph over the box.
- `relevance:` (i) Identifies the affine rule as a tractable subclass inside the quadratic family; exactness still refers to the reformulation. (ii) No gap. (iii) This is the standard LP that the bridge-side closed-loop ladder would have to beat, since an affine-in-w policy reduces to exactly this epigraph form.

### s6 — cjw-one-to-one

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 1, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 1
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "admit exact semi-definite program (SDP) reformulations in the sense that they share the same optimal values and admit a one-to-one correspondence between the optimal solutions."
- `gloss:` The exactness claim is value equality plus a bijection between optimal solutions of the rule-restricted problem and its SDP.
- `relevance:` (i) This is the strongest form of exactness in the paper, and it is still confined to the rule-restricted problem. (ii) No statement about the adaptive optimum. (iii) Useful as a template for what a bridge-side exactness theorem would have to assert (values plus solution correspondence), but it must be asserted against the adaptive optimum, not against a reformulation.

### s7 — cjw-extension-open

- `file:` 17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf
- `extract:` `pdftotext -layout`, PDF page 20, single column
- `sha256:` 48143323542f3e3cce255c95722c5f6c91490bf4366ec1b38b063a8a2dd00f65
- `pdf_page:` 20
- `printed_page:` uncertain - journal-style PDF with no printed page numbers; headers carry only "Journal of Global Optimization" and the footer "123"
- `quote:` "Our approach may be extended to study adjustable robust linear programs over box data uncertainty sets under a more general separable polynomial decision rule"
- `gloss:` The authors explicitly leave the general separable polynomial rule to future work.
- `relevance:` (i) Confirms the boundary of the result: only separable quadratic is settled here. (ii) No gap content. (iii) For the essay this marks an open direction, since a piecewise-linear bridge policy is not a polynomial at all.


## P18 — Jeyakumar, Lee, Lee, Li & Woolnough 2022 — SOS reformulations for separable polynomial rules

- `file:` 18_Jeyakumar_etal_2022.pdf
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd

### t1 — jel-mapping-object

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 2
- `printed_page:` 1364
- `quote:` "However, even a linear ARO problem with two-stage decision-making is a challenging problem because we optimize a linear function over mappings rather than vectors."
- `gloss:` The difficulty is intrinsic to optimizing over functions; decision rules are the standard response.
- `relevance:` (i) Frames the problem so that exactness must be a property of a rule class. (ii) No gap. (iii) The bridge ladder is exactly an optimization over non-anticipative mappings, so this framing applies verbatim.

### t2 — jel-general-quadratic-hard

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 2
- `printed_page:` 1364
- `quote:` "On the other hand, two-stage ARO with box uncertainty sets under a general quadratic decision rule is numerically an intractable problem, because the resulting transformed single-stage problem is a numerically intractable non-convex quadratic optimization problem over box constraints which is known to be a NP-hard problem [13]."
- `gloss:` A general quadratic rule over a box makes the robust counterpart NP-hard, which is why separability is imposed.
- `relevance:` (i) A hardness boundary, not a characterization. (ii) Hardness rather than gap. (iii) The bridge is a box-uncertain problem, so this is the barrier any non-separable quadratic or piecewise-linear rule for the bridge would hit.

### t3 — jel-sos-representation

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 3, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 3
- `printed_page:` 1365
- `quote:` "Next, we present a sum of squares (SOS) representation for non-negativity of a separable polynomial over a box."
- `gloss:` For separable polynomials, nonnegativity over a box is certified exactly by a univariate SOS representation per coordinate.
- `relevance:` (i) The certificate that makes exactness possible; it certifies constraints, not policy optimality. (ii) No gap. (iii) Separability is the price of admission; the bridge value function is not separable in the sign coordinates, so this certificate does not transfer directly.

### t7 — jel-poly-rule

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 5, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 5
- `printed_page:` 1367
- `quote:` "satisfies more generally a separable polynomial decision rule of the form:"
- `gloss:` The rule is y_r(z) = a_0^r + sum_j sum_{k=1..l} a_{kj}^r z_j^k: additive across coordinates, polynomial of degree l in each.
- `relevance:` (i) Defines a hierarchy of rule classes, not an exactness condition. (ii) The numerical section measures how the gap shrinks with l, not an exactness theorem. (iii) Additivity in z is incompatible with a value function built from sums of absolute values of coupled coordinates, so containment of the bridge is not claimed and is implausible.

### t4 — jel-exact-sos

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 6, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 6
- `printed_page:` 1368
- `quote:` "Theorem 3.1 (Exact SOS Reformulation) Consider the problem (RP) with the separable polynomial decision rule and the box data uncertainty, and the sums of squares programming problem (SOS). Then, inf (RP) = inf (SOS)."
- `gloss:` For a separable polynomial rule over a box, the robust problem and an explicit SOS program have equal optimal values, with a bijection of optimal solutions.
- `relevance:` (i) Exactness of the rule-restricted problem, with no constraint qualification; the hypothesis is the rule class plus box uncertainty. (ii) Still no comparison with the adaptive optimum. (iii) This is the cleanest exact conic reformulation in the group for box uncertainty, which is the bridge geometry.

### t5 — jel-exactness-sense

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 2
- `printed_page:` 1364
- `quote:` "The exactness is characterized in the sense that the problems have the same optimal values and they exhibit a one-to-one correspondence between the optimal solutions."
- `gloss:` The authors define exactness as value equality plus a bijection of optimal solution sets between the robust problem and its reformulation.
- `relevance:` (i) A definitional clarification: "exact" is not "affine rule is optimal". (ii) No gap. (iii) The essay should adopt this definition explicitly, then state separately the (absent) exactness-against-adaptive-optimum notion.

### t8 — jel-degree-ladder

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 1, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 1
- `printed_page:` 1363
- `quote:` "Our results demonstrate that the adjustable robust solutions approach the actual optimal solution as the degree of the polynomial increases from one to fifteen."
- `gloss:` Increasing the polynomial degree is reported to shrink the gap to the fully adaptive optimum, empirically.
- `relevance:` (i) This is the only gap-oriented statement in the six papers, and it is numerical, not a theorem or a bound. (ii) It gives evidence of a vanishing gap along a hierarchy, but no rate and no proof. (iii) Suggests a hierarchy route for the bridge, but with the same caveat: polynomial rules do not represent absolute values without high degree.

### t6 — jel-degree-discrepancy

- `file:` 18_Jeyakumar_etal_2022.pdf
- `extract:` `pdftotext -layout`, PDF page 14, single column
- `sha256:` 13462f14db8e9886b4fde279a62d9d6bd258d0f6a6a5637ebb374059194eedfd
- `pdf_page:` 14
- `printed_page:` 1376
- `quote:` "We show that the adjustable robust solutions approach the true optimal solution as the degree of the polynomial ℓ increases from one to twelve."
- `gloss:` Section 4 states the ladder runs from degree one to twelve, while the abstract and introduction state one to fifteen.
- `relevance:` (i) No logical bearing on exactness, but a citation hazard: the two degree ranges cannot both describe the same experiment. (ii) The gap-closing evidence is therefore reported inconsistently. (iii) Do not cite either endpoint for the bridge without checking the figures in the PDF.


## P19 — Zhang, Sun & Teo 2024 — Exact SDPs for adjustable robust quadratic optimization with affine rules

- `file:` 19_Zhang_2024.pdf
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941

### u1 — z-exact-sdp-quadratic

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 2, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 2
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "In this paper, we deal with exact semidefinite programming (SDP) reformulations for a class of adjustable robust quadratic optimization problems with affine decision rules."
- `gloss:` The paper extends exact SDP reformulations from linear to quadratic adjustable robust problems under an affine rule.
- `relevance:` (i) Exactness of the reformulation class, not of the rule. (ii) No gap statement. (iii) Shows the conic program remains exact when the objective and constraints are quadratic, provided the affine rule and its special structure hold.

### u2 — z-diagonal-W

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 5, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 5
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "where ρ := (ρ1 , . . . , ρm ) ∈ Rm and W := diag(ω1 , . . . , ωm ) ∈ Rm×m are non-adjustable variables."
- `gloss:` The decision rule is y(z) = rho + Wz with W diagonal, so each recourse coordinate depends only on the matching uncertainty coordinate.
- `relevance:` (i) A severe restriction of the affine class; no exactness condition is offered for the full-matrix case. (ii) The gap of the diagonal subclass is not discussed. (iii) The bridge policy must couple coordinates (L1 over a coupled state), so this class cannot be the known exact class containing the bridge.

### u3 — z-lemma-iff

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 6, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 6
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Lemma 2.1 [12] Let α ∈ R, v := (v1 , . . . , vm ) ∈ Rm and W := diag(ω1 , . . . , ωm ), where ω j ∈ R, j = 1, . . . , m. Then, the following statements are equivalent:"
- `gloss:` Nonnegativity of alpha + v.z + sum omega_j z_j^2 over a box is equivalent to an explicit 3x3 PSD system, via a degree-4 SOS representation.
- `relevance:` (i) A genuine iff, but about constraint nonnegativity; it is quoted from paper 17 and is the technical core. (ii) No gap. (iii) The lemma requires diagonal W; it is precisely the conic lemma that fails for coupled L1-type bridge value functions.

### u4 — z-thm-value

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 7, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 7
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Theorem 3.1 Consider the problem (RTP) with U i , i = 1, . . . , l, given by (1) and its reformulation problem (SDP). Then, inf(RTP) = inf(SDP)."
- `gloss:` The affine-rule robust quadratic problem and an explicit SDP share the same optimal value.
- `relevance:` (i) Exactness of the reformulation. (ii) No gap. (iii) Confirms the pattern; note that as displayed in (RTP), the rule is affine in a box variable z, while the constraint-data uncertainty u^i ranges over separate spectrahedral sets U^i, so this is not an affine rule in the uncertainty that enters the constraint data.

### u5 — z-thm-correspondence

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 7, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 7
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "Moreover, (x, ρ, W ) is an optimal solution of the problem (RTP) if and only if there exist τ ∈ R, δ ∈ Rlm , u ∈ R pl , X ∈ R3×3lm , σ ∈ Rm and Y ∈ R3×3 m such that"
- `gloss:` Optimality of a triple in the robust problem is equivalent to extendability to an optimal solution of the SDP by auxiliary multipliers and PSD blocks.
- `relevance:` (i) A necessary-and-sufficient certificate of optimality within the rule class. (ii) It cannot certify absence of a gap. (iii) Provides the certificate shape a bridge-side proof would need, but with the diagonal-W restriction.

### u6 — z-special-sets

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 4, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 4
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "For ellipsoidal, polytopic, and box uncertain sets, we also establish exact SDP reformulations for adjustable robust quadratic optimization problems."
- `gloss:` The exact reformulation specializes to the three standard uncertainty geometries.
- `relevance:` (i) Tractable subclasses of the reformulation. (ii) No gap. (iii) Box is the bridge geometry, but the exactness here is again about the reformulation under a diagonal affine rule.

### u7 — z-extends-linear-to-quadratic

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 10, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 10
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "However, Theorem 3.1 extends these results from linear optimization models to quadratic optimization models."
- `gloss:` The contribution is positioned as a strict extension of the linear exact-SDP results (papers 15 and 16) to quadratic models.
- `relevance:` (i) Confirms that the entire lineage is about exact reformulations, not exactness of the rule. (ii) No gap. (iii) Useful for the essay's lineage claim: 15 -> 16 -> 17 -> 18 -> 19 is one chain of conic reformulations, each widening the model but not the exactness question.

### u8 — z-copositive-citation

- `file:` 19_Zhang_2024.pdf
- `extract:` `pdftotext -layout`, PDF page 3, single column
- `sha256:` 8800140f1b5fe0f82672f5400d3b88b4553a1e88eea4c1611dc6b1ff92138941
- `pdf_page:` 3
- `printed_page:` uncertain - online-first PDF; footers carry only "123" and no printed page number is visible
- `quote:` "In [24], exact copositive optimization reformulations are obtained for robust quadratic optimization problems with uncertain parameters containing both continuous and integer components."
- `gloss:` This is a citation to adjacent literature; the paper does not develop any copositive characterization itself.
- `relevance:` (i) Negative finding for the essay: none of the six papers gives a copositive characterization of LDR exactness. (ii) No gap content. (iii) Signals the missing link the essay would have to build: a copositive or completely-positive description of when the affine class attains the adaptive value.


## Marginal notes

**Which paper is closest to a characterization (iff condition) of LDR exactness?**

Two different senses have to be separated, and no paper in the six merges them.

1. *Closest in logical form to an iff.* `15_Chuong_Jeyakumar_2020`, Theorem 2.1 (Adjustable
   Farkas' Lemma, PDF p. 5; optimization form Theorem 3.1, PDF p. 15). It is the only literal
   set of equivalent statements about the affine-restricted system in the corpus. `q3` is its exact
   shape: closedness of the cone C is assumed, and then "the following statements are equivalent".
   What remains unstated: the equivalence is between two descriptions of the *same*
   affine-restricted problem (a semi-infinite implication and a finite LMI system), so the "only if"
   direction never compares against the fully adaptive value. There is no statement of the form
   "affine value = adaptive value iff condition on A, B, b, U". The cone-closedness hypothesis is a
   regularity condition for strong duality; the paper never claims it is a condition for the affine
   rule to be optimal. Also unstated: any necessity direction for exactness, any gap bound, and any
   statement covering multi-stage (more than two-stage) adaptation.

2. *Closest in content to an exactness statement for a policy class.* `03_Chen_Zhang_2009`,
   Theorem 1 (PDF p. 4, printed 1472; quote `cz4`): the extended feasible set built from the
   extreme points of a polytopal uncertainty set equals the fully adaptive feasible set X0.
   What remains unstated: (a) the theorem is a construction that always works for polytopes, not a
   *criterion* on the data, so it supplies no necessary condition; (b) it is silent on when the plain
   affine class already equals X0; (c) it needs K = M = number of extreme points and the companion
   Theorem 5 (PDF p. 7, printed 1475; described here, not quoted, because the infinity and set glyphs
   are dropped by the embedded font) states that for the infinity norm with finite radii the split
   extended set gives the same feasible set as the un-split extension, so splitting cannot help on a
   box; (d) it gives no bound on the gap when the construction is not used; (e) it never converts the
   negative box result into a condition saying which *other* reparameterization is exact.

3. *Closest to a two-sided condition on when the affine class fails.* Still `03_Chen_Zhang_2009`,
   Theorems 5, 6 and 8 (PDF pp. 7-8, printed 1475-1476). Read together they give: with the infinity
   norm and finite radii the split class does not improve on the un-split extension (Theorem 5);
   with all radii infinite and the extension bounded the same holds (Theorem 6); with a non-infinity
   norm and some finite radius the split class *may* be a strict subset, i.e. may strictly improve
   (Theorem 8; its proof adds the normalisation ||e_i||_(t) = 1). Example 3 (PDF p. 7) shows
   Theorem 6 can fail when the extension is unbounded.
   What remains unstated: the conclusions are one-directional ("does not improve" vs "may provide a
   strict improvement"), the word "may" in Theorem 8 is a construction, not a criterion, and nothing
   is said about the *plain* affine class or about necessity. It is the closest the six papers come to
   a data-dependent condition on non-exactness, and it is still not an iff.

**Secondary observations that bear directly on the essay.**

- **No copositive characterization is present.** The only occurrence of "copositive" in all six
  PDFs is a citation in `19_Zhang_2024` (PDF p. 3; quote `u8`) to Mittal et al. on robust quadratic
  optimization with mixed-integer uncertainty. The conic characterizations actually supplied are
  SDP/SOCP duals (15, 16) and SOS/LMI certificates for separable nonnegativity (17, 18, 19). All of
  them certify the rule-restricted problem exactly; none certifies that the rule class attains the
  adaptive optimum. A copositive description of the gap is the missing piece.

- **"Exact" in this literature never means "the affine rule is optimal".** Papers 16, 17, 18 and 19
  all use "exact" for value equality between the robust problem and a conic reformulation, plus a
  bijection of optimal solutions (`t5`, `s6`, `u5`). Any essay sentence of the form "exact SDP
  reformulation" must be read in that sense, or it will overstate the result.

- **Hardness boundaries.** The tractable side is protected by: affine data dependence (16, p. 12,
  NP-hard otherwise), separability plus box (17, p. 2; 18, p. 2, NP-hard otherwise), and diagonal
  quadratic part (17 Theorem 2.1; 19 Lemma 2.1). For the bridge these three boundaries coincide
  with its geometry only in part: sign uncertainty is a box, but the L1 terminal cost is not additive
  in the sign coordinates, so the separable classes (17, 18, 19) do not visibly contain the bridge
  policy, and the only class that does contain it without separability is the Chen-Zhang
  vertex-weight class, at 2^p auxiliary blocks.

- **Numerical gap evidence is stated inconsistently.** `18_Jeyakumar_etal_2022` reports the degree
  ladder as "one to fifteen" in the abstract and introduction (PDF p. 1, printed 1363, quote `t8`;
  PDF p. 2, printed 1364) but as "one to twelve" in Section 4 (PDF p. 14, printed 1376, quote `t6`).
  The discrepancy is unresolved in the text; do not cite either endpoint without checking the figures.

- **Scope caveat in `19_Zhang_2024`.** Its affine rule adapts to a box variable z while the
  constraint data uncertainty u^i ranges over a spectrahedral set (PDF p. 5), and the coefficient
  matrix W is diagonal (`u2`). It is therefore not a characterization of LDR exactness for the
  classical ARO setting in which the rule adapts to the same uncertainty that enters the data.

