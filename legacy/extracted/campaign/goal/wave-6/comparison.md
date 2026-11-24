# Wave 6: primary-source comparison of the actual support-defect bound

## Disposition and limits

**Recommended workflow disposition: source-closure (elementary reconstruction).** Close this support-defect mechanism as a route to the original first-success goal. The missing named originals are now accessible and their relevant statements have been read. None of the three DOI leads has been shown to cover the entire wave-5 class by a model-preserving reduction. That does not establish novelty: the actual bound is the ordinary dual upper estimate of a rowwise suffix-support relaxation, with its loss written relative to the open-loop dual expression. A3 already supplies the matching one-measurement control model and coupled support/dual machinery.

This is a source-comparison recommendation for coordinator inspection, not a mathematical-truth or priority verdict. `goalAchieved=false`; `proof_authorized=false`. No new theorem proof, numerical case, optimization, checker replay or formalization was performed. The pre-existing universal proof gap remains; it is not a reason to fund proof of a reconstruction.

## 1. Fixed object being compared

Read in full: `goal/wave-5/astra/derivation.md`, `goal/wave-5/verification/proof.md`, and `artifacts/goal/wave-5/independent-review/report.md`. The latter explicitly calls its standalone monotone-control comparison partial. Its finite checks were not rerun here.

The actual model has deterministic finite-horizon linear dynamics, bounded symmetric continuous control and independent timewise disturbance boxes, no intermediate constraints, terminal strip `L<=X<=H`, and signed linear terminal reward `Y`. A fixed prefix `a` is chosen before disturbance. At `r` the exact current state selects an entire suffix `b`, before every future disturbance. Policies are Borel state maps; neither full prefix history nor future disturbance is supplied. A feasible open-loop witness with guarantee `J` is a separate mandatory input.

Use the parent's terminal decomposition `X=dx+px(a)+cx(b)+zx+ex`, `Y=dy+py(a)+cy(b)+zy+ey`. Its full disturbance row supports are `Sx,Sy`; suffix control supports are `Hx,Hy` and `Hm=sum_suffix beta_t |Cyt+(lambda-mu)Cxt|`; `Hp` is the same mixed-row support over the prefix. For any `lambda,mu>=0`:

```
D0 = dy-Sy + lambda(dx-L-Sx) + mu(H-Sx-dx) + Hp + Hm
Delta = (lambda+mu)Hx + Hy - Hm
J <= V0 <= Vr <= D0+Delta
0 <= Vr-V0 <= D0+Delta-J.
```

Equality requires the feasible witness, `J=D0`, and `Delta=0`. Positive defect is not positive information value; zero defect is not necessary for equality. Neither an exact cutoff necessity nor ordering between different single observation times is asserted. The special same-weak-sign characterization requires `mu=0`, `lambda>0`, positive coordinate weight; the general two-multiplier expression remains authoritative.

## 2. Primary sources, versions and physical anchors

Hashes, acquisition routes and exact physical pages are in `source-manifest.json`. Page numbers below are one-based physical PDF pages, not viewer labels. Extracts were generated directly from the PDFs with Poppler, not taken as mathematical facts from historical Markdown. AS03 pp2,4 and A3 p6 were also rendered and visually read because mathematical glyphs are incomplete in AS03 text extraction.

### AS03: Angeli and Sontag, DOI 10.1109/TAC.2003.817920

`goal/wave-6/sources/AS03.pdf` is the IEEE-formatted article hosted by Sontag's own publication site: TAC 48(10), 2003, 1684–1698; DOI visible on physical p1. Read pp1–6, particularly Definition II.1 on p2/1685, Theorems 1–2 on p3/1686, Proposition III.2 and Corollary III.3 on p4/1687, and Definition V.1 on p6/1689. Retrieved and read the linked author errata; its corrections concern antisymmetry, a difference of states and strict positive time, not an optimization theorem.

Definition II.1 requires `u1>=u2, x1>=x2 => phi(t,x1,u1)>=phi(t,x2,u2)` for all nonnegative times in specified partial orders. On p4 the cooperative differentiable-system test requires nonnegative off-diagonal state partial derivatives and nonnegative input partial derivatives; Corollary III.3 gives the signed-orthant versions. The underlying model there is a forward-complete continuous-time differential system on a forward-invariant state space. The general definition first describes ordered controlled flows.

The word **static** in p6's “static input–state characteristic” means the globally asymptotically stable equilibrium associated with each constant input. It is not optimality of a static robust optimization solution or absence of information value. No such inference is made here.

**Comparison:** favorable signs of terminal impulse columns for two terminal rows at one horizon establish neither order preservation of every state trajectory nor the differentiable flow hypotheses. A coordinate change would have to preserve dynamics, observation and constraints and exhibit the required state/input/output orders; no such reduction is supplied by the parent's terminal signs. A negative matrix entry alone would not exclude every cone order, so that shortcut is also rejected. Even a verified monotone input/output map would not make its jointly maximizing input feasible for the opposing upper strip. AS03 therefore supplies terminology and precise order hypotheses, not a directly applicable equality or the additive defect bound.

### BGL15: Bertsimas, Goyal and Lu, DOI 10.1007/s10107-014-0768-y

Existing `corpus/04_Bertsimas_Goyal_Lu_2015.pdf`: MIT repository cover p1 identifies the DOI, handle `1721.1/103403`, and **author's final manuscript**, without publisher formatting/copy editing. Physical p2 is manuscript p1. Do not assign journal page labels 281–319 to this manuscript's internal pages. Read physical pp1–12,14–17,21–27 for the relevant models/statements and extensions.

Physical p4/manuscript p3, model (1.1): `max_x c'x + min_B max_y d'y`, `Ax+By<=h`, `y>=0`, with `B,d` nonnegative; `x,c,h` initially need not be nonnegative. The source expressly says it cannot handle “covering constraints involving second-stage variables, or lower bounds on second-stage decision variables.” The second-stage rule observes `B`. P9 defines `T(U,h)={B' mu: h'mu=1,B in U,mu>=0}`. P11, Theorem 1: static equality if `T(U,h)` is convex for **all** `h>0`; nonconvexity for some `h` yields **an instance** with strict gap, not a strict gap for every instance.

P15/manuscript p14 adds `x>=0,c>=0` for performance bounds and states Theorem 2, `zAR<=rho(U) zRob`, with `rho(U)=max_{h>0} kappa(T(U,h))`. P21 Theorem 5 extends the multiplicative bound to independent constraint/objective uncertainty `U=U^B x U^d`. P25 Theorem 6 handles uncertain RHS as well but requires **constraint-wise** `U^{B,h}` and retains the nonnegative recourse structure; pp26–27 explain the reduction and explicitly do not extend the approximation bound to arbitrary RHS uncertainty.

**Comparison:** wave 5 has fixed signed suffix coefficients, uncertainty in the terminal RHS, bounded symmetric recourse, and a two-sided strip. Shifting `b` to nonnegative coordinates does not fix the opposed strip rows: their recourse coefficient rows are `cx` and `-cx`; in general they cannot both become nonnegative by coordinate sign flips. Splitting signed variables likewise leaves signed coefficients/equality or coupling constraints, not the source's monotone packing model. Appending a fixed coordinate to homogenize an uncertain RHS requires enforcing that coordinate's value and preserving the same uncertainty; it is not a free nonnegative packing variable. No model-preserving transformation to the theorem hypotheses has been exhibited.

Timewise independence is not constraint-wise independence: one prefix disturbance changes lower-strip, upper-strip and reward rows together. The RHS extension does not erase that dependence. Full observation of uncertain data is not automatically exact current-state observation either. A more informed model can supply an upper bound, but equality for it does not identify the actual policy class without a valid mapping and lower comparison.

### BG10: Bertsimas and Goyal, DOI 10.1287/moor.1090.0440

`goal/wave-6/sources/BG10-author.pdf` was obtained from the link in Bertsimas's MIT publication list. Despite that list's old “submitted … 2009” description and our conservative filename, the downloaded bytes are the **published journal-formatted author courtesy copy**, MOR 35(2), May 2010, pp284–305; DOI and publication history visible on p1. This is not an inferred version match from its abstract. Read physical pp1–5,15–21, particularly models (1)–(6), Theorems 4.1,5.1,5.3 and the proof of 5.3.

Pp2–4/285–287 impose nonnegative decisions, costs and (in the initial covering models) RHS. Constraint matrices may be signed. P4 explicitly explains that nonnegative RHS prevents packing constraints such as `sum x_j<=1` and nonnegative objectives prevent maximization models. P16/299, Theorem 4.1: `zRob(b)<=2 zAdapt(b)` for positive RHS uncertainty. P19/302, Theorem 5.1: factor four for positive joint RHS/cost uncertainty. These are multiplicative optimal-value comparisons, not the parent's instance-dependent additive certificate.

The potentially strongest apparent overlap is p20/303, Theorem 5.3, **exact static/adaptive equality for a hypercube of all entries of `(A,B,b,d)`**, models (56)–(57). Unlike the earlier covering model, here `b` and matrices may be signed; nonnegative decisions and recourse costs remain. On p21/304 the proof explicitly selects the jointly worst scenario: entrywise minimum `A,B`, maximum `b,d`. The sentence “Because the uncertainty set is a hypercube” is the justification that this combined scenario exists. This assumption must not be replaced with “primitive disturbances form a box.”

**Concrete comparison:** after eliminating future disturbance rowwise, a prefix disturbance `w` enters the two strip RHS components through opposite copies of the same scalar `zx(w)`. The set of resulting RHS vectors is a correlated affine image of a box, not in general the Cartesian product of its coordinate intervals. Their separate worst RHS coordinates need not be jointly attainable. Adding a reward epigraph row retains the shared disturbance, rather than creating independently selectable entries. Replacing this image by its Cartesian hull is a relaxation, not a model-preserving reduction to Theorem 5.3. This is exactly the row-independence distinction the parent's proof carefully avoids: it adds scalar necessary inequalities about the common fixed prefix, without claiming a joint worst disturbance. Nonnegative-cost conversion of a signed reward also needs additional constraints/constants; it is not authorized merely by renaming maximization as minimization.

## 3. Closest control source A3: concrete preservation and its boundary

`research/sources/A3.pdf` is byte-identical to its corpus original and to the frozen resource manifest: Kastsiukevich and Dmitruk (2021), DOI 10.33581/2520-6508-2021-2-38-50, journal pp38–50. Read original physical pp1–8; p6/43 visually checked. No additional original beyond the mandated A3 and three DOI leads is used.

For the stationary subclass, the model-preserving dictionary is explicit:

| Wave 5 | A3 original |
|---|---|
| `r`, fixed prefix `a`, state-dependent full suffix `b` | p4/41: `T1`, `u0`, `u1(.|x1)` and Definitions 3–4 |
| exact state observation before future disturbances | p4 numbered measurement/choice assumptions and (5)–(7) |
| disturbance matrix `E`, timewise box | p2/39: `M`, and `W0,W1` on p4 |
| scalar `X` and `[L,H]` | p3/40: one row of `H`, `gmin=L,gmax=H` |
| maximize guaranteed `Y` | minimize worst terminal cost using `c=-lY`; negate the value |
| symmetric control box | set `umin=-beta`, `umax=beta` in A3 |
| full disturbance row supports `Sx,Sy` | p3's `gamma_i,gamma_0` and tightened nominal problem (4) |

This dictionary keeps the two strip sides, future disturbances and information timing. It does not import A3's rank hypothesis without checking it or turn its finite-normal outer approximation into an exact description. A3's model is time invariant; the wave-5 statement allows deterministic time variation and coordinate-specific radii. The latter are not literally an application of A3's stationary proposition. The parent's existing terminal coefficient decomposition shows that its subsequent bound only uses finite rows and boxes; a change to coefficient bookkeeping is not an established substantive contribution.

A3 p6 (11)–(14) computes support bounds of the suffix-feasible cost-level sets and dualizes both terminal sides and the suffix box. P7/44 gives the positive/negative parts and the prefix robust LP (17). P8/45, (18)–(19), uses lifted terminal coordinates, retaining combined constraint/reward row supports. The source explicitly calls these outer approximations. A3 does not state the exact displayed `Delta` formula on these inspected pages, and no claim is made that its rank-restricted proposition verbatim proves the full wave-5 theorem. It does contain the substantive control/support ingredients that the candidate repackages.

## 4. What the candidate actually adds: relaxation bookkeeping

This is an identification of the inequalities and algebra already written in the parent's proof, not a new proof attempt.

The parent takes the suffix reachable pair `{(cx(b),cy(b)): b in suffix box}` and uses only its coordinate supports `Hx,Hy`, ignoring their joint coupling for necessary conditions. Its three rows are exactly the following relaxed prefix problem:

```
R = max_a [dy + py(a) + Hy - Sy]
    a in prefix box
    L + Sx - Hx <= dx + px(a) <= H - Sx + Hx.
```

Every feasible policy's fixed prefix must meet these necessary rows; the relaxation does not construct a suffix policy. For the parent's weights its ordinary Lagrangian box upper estimate is

```
U(lambda,mu) = dy-Sy + lambda(dx-L-Sx) + mu(H-Sx-dx)
               + Hp + (lambda+mu)Hx + Hy.
```

The parent's own formulas identify `U=D0+Delta`. Thus optimizing over the nonnegative weights is the dual of this relaxed finite prefix LP, not a new policy optimization method. With the already assumed feasible open-loop witness this LP has a nonempty compact prefix domain. No dual optimization was executed here. Relative to the combined-row open-loop estimate `D0`, the displayed defect simply records the replacement of the joint mixed suffix support by separate supports. Its sign and common-corner specialization are exactly the parent's elementary support-subadditivity/triangle-inequality step.

A3's support construction retains joint directions before choosing outer normals; wave 5 deliberately discards that information. The discard is not a model-preserving equivalence to the exact adaptive problem, and this comparison does not label it one. It explains why the candidate can upper-bound every policy, including a more informative prefix policy class, while its lower witness stays admissible under the actual sensor. It also explains the lack of a necessity or strict-gain conclusion. The opposite strip remains mandatory for the lower witness even at zero upper multiplier.

The additive certificate is translation invariant in reward: adding a constant to `Y` shifts `J,D0,V0,Vr` equally and leaves the gap and `Delta` unchanged. The multiplicative source bounds depend on their nonnegative/normalized objective setting; an arbitrary shift cannot transfer their factor into this additive formula. This distinction prevents false source coverage. It does not turn the residual elementary calculation into substantive novelty.

The certificate may be practically convenient as a cheap screening explanation that avoids recourse enumeration when it closes exactly. No new complexity guarantee, sharpness characterization, necessity result, new information effect or source-backed non-elementary step has been supplied. The assignment expressly excludes a new formula arrangement or elementary triangle inequality as first success. On the actual unchanged claim, no bounded substantive remaining obligation has been identified that justifies more proof expenditure.

## 5. Logic audit and operational decision

The relevant thesis is whether this actual mechanism contains substantive content beyond its sources and elementary reconstruction, not whether the sources print identical notation. Required qualifications:

- “AS03 has monotone systems” does not imply the terminal-sign certificate is an AS03 optimization theorem (equivocation/false analogy).
- “The primitive set is a box” does not imply its correlated terminal-row image satisfies BG10's entrywise hypercube condition (dropping qualifications).
- “BGL15 has a tight bound” does not establish its nonnegative packing hypotheses, independent uncertainty or observation class for this problem.
- Failure of those three direct reductions does not establish novelty. That inference would omit the elementary-reconstruction alternative.
- Four exact examples do not establish the universal policy claim; a written identity does not supply its missing formal quantifier verification.

**Decision:** source-closure, specifically elementary reconstruction with closest-source support machinery, not a claim of verbatim coverage by any one DOI theorem. No decisive source/access gap remains among the assigned leads. Publisher BG10 and Goyal's publication route returned HTTP 403; the legitimate MIT author route resolved the same article, with its journal identity visible on original pages. Search tool silence was not used as evidence. No extra source was needed.

Stop this mechanism as a first-success route. Preserve wave-5 arithmetic and its published-example interpretation as reconstruction. Do not start another numerical sweep, renamed proof, replacement claim class or fresh research direction. The coordinator may inspect this recommendation; scientific attestation and any future proof authorization remain outside this worker's authority.
