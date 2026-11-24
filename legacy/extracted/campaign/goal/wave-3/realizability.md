# Residual realizability: two scopes and a source closure

Task aro-discovery-k4t, wave 3. Disposition: source-closure of the two selected success routes. All general derivations below are informal reconstruction proposals, not code-judged theorems. No mathematical experiment or new exact certificate was executed. proof_authorized=false; goalAchieved=false.

## 1. Approved model and quantifiers

Use research/question.md, not the glossary's differently specialized L1 bridge entry. Rational data, finite nonempty correlated COMPLETE paths W, rational closed bounded control boxes, fixed first program a and fixed rational q. At time r the controller observes only z=x_r(a,p), selects the ENTIRE continuation b in V, and only then the suffix acts. There are no subsequent observations. Prefix p is an unavailable comparison oracle, not an added sensor. On a measured-state cell all actual suffix constraints must hold for ONE common b. No Cartesian completion of W and no pathwise clairvoyant continuation is permitted.

With D stacking H and c^T, beta(q)=(h,q-d0), repeated substitution yields

    x_T = Phi(T,r) z + G b + eta(s),
    K_p = {b in V : D G b <= beta(q)-D Phi(T,r)z-rho_p},
    rho_p,j = max_{s in S(p)} D_j eta(s).

The max in each row may be attained by a different ACTUAL suffix. This is a conjunction of universal scalar inequalities, not replacement of W by independent coordinate disturbances. The common-cell system uses max_p rho_p componentwise; it does not make individual rho_p observable. A4 original PDF pp2–4 anchors the dynamics, signed cost and measurement ordering, but its stationary real system with timewise box disturbances is NOT the campaign's time-varying finite correlated-path model.

## 2. W3-S1: full-class embedding closes the unrestricted shortcut

Let J>=1 and d>=1. Given ANY finite nonempty list of rational right-hand sides delta_p in Q^J, ANY rational L in Q^(J x d), and one nonempty rational control box V in Q^d, the desired family is

    F_p = {b in V : L b <= delta_p}.

An elementary embedding uses T=2, r=1, state/disturbance dimension J, control dimension d, x0=0, U0={0}, U1=V. Set A0=B0=E0=A1=0, B1=L, E1=I_J. Let H select the first J-1 state coordinates with h=0; let c=e_J, d0=0, q=0. Thus D=I_J, c is nonzero and its last row is the original final inequality, not an additional constraint. For J=1 the hard-row block is empty, as permitted by k>=0.

Choose distinct rational prefix labels ell_p in Q^J and EXACT complete paths (ell_p,-delta_p). Then x1=0 for every prefix and x2=L b-delta_p. Consequently K_p=F_p. A state policy has ONE b on the observed zero cell. Each singleton conditional suffix is fixed by correlation, but the state controller does not observe its label; this construction never supplies a prefix oracle to that controller. Duplicated delta_p cause no problem because the prefixes, hence complete paths, remain distinct. All original paths are retained. The objective is signed terminal cost; c!=0 does not imply the realized cost must be nonconstant on every possible input.

This is a written algebraic reduction, not a new theorem certified by a checker. It shows why general-model dynamics alone cannot justify a stronger universal compatibility shortcut than generic fixed-normal geometry: the class already contains all these finite rational families. The embedding can even keep D,G,V and the other displayed matrices fixed for all RHS lists for a GIVEN L,V,J,d; only W changes. Across different L or dimensions it is a different template. It does not prove universality for an arbitrarily prescribed D or disturbance channel. Its elementary nature disqualifies it as first success.

## 3. What is actually fixed in a template?

Fix horizon, dimensions, ALL A_t,B_t,E_t, initial state, a, control domains, H,h,c,d0,q,r, observation map, and any exogenous disturbance domain/admissibility relation. Only the finite nonempty complete-path set W may vary inside that relation. Freezing W as well would leave no family to classify.

For a prefix p producing z, let Omega_p be the allowed suffix universe under the frozen external relation, and put

    M_p = {D eta(s) : s in Omega_p} subset Q^J.

A vector rho is realizable for this prefix exactly when it is the componentwise maximum of a finite NONEMPTY subset of M_p. Equivalently, for each row j there must be an ACTUAL allowable suffix s_j with

    D eta(s_j) <= rho,   D_j eta(s_j)=rho_j.

Necessity uses an attaining suffix in the original finite conditional set. For sufficiency take the union of these at most J witnesses. Their maximum is rho in all rows. This is direct finite-max reconstruction, not a non-elementary criterion. With a finite rational polyhedral suffix domain each witness condition is a linear feasibility problem; with a non-polyhedral or restricted finite domain it need not be such an LP. No general LP-duality completeness theorem is asserted or needed here.

A finite family must additionally have distinct available prefix labels in the same observed cell, and each pair (p,s_j) must belong to the frozen complete-path admissibility relation. In the unrestricted campaign input and the D2 template below these requirements can be met by erased prefix labels. They cannot be presumed for a different template. Row support constraints on rho describe a PARAMETERIZATION; redundant rows and the shared V can make different rho induce the same residual set. Strict support-vector restriction alone is not proof of strict set-class restriction.

## 4. W3-S2: the inherited D2 template, without changing its matrices

Freeze research/structured/derivation.md section 3: T=2,r=1,n=m=d=2; x0=0; A0=B0=E0=A1=0; B1=E1=I2; U0={0}; V=[0,2]^2 intersect Q^2; H=-I2,h=0,c=(1,1),d0=0. Freeze q=1 for the actual comparison. W alone varies over finite nonempty rational complete paths; the campaign has no additional amplitude bound on these paths. The observed state is always x1=0, independent of prefix labels. This is an existing campaign template, NOT a newly invented A4 template.

For a suffix w=(u,v), D eta(w)=(-u,-v,u+v), so M is the rational plane y1+y2+y3=0. Every realizable rho=(r1,r2,r3) satisfies

    s := r1+r2+r3 >= 0.

Conversely, if s>=0, the three plane points

    (r1,r2,-r1-r2), (r1,-r1-r3,r3), (-r2-r3,r2,r3)

are each <=rho, and together attain all its coordinates. Each is the image of an ACTUAL rational suffix (u,v)=(-y1,-y2); duplicate witnesses can be removed. Give each desired residual a distinct erased prefix label and retain these witnesses as its conditional suffix set. Thus the written characterization is exact at the support-vector level for this template when W varies, without imposing the older experiment's |W|<=4 cap on this general argument.

Before clipping by V, the residual is

    b1>=r1, b2>=r2, b1+b2<=1-r3.

If t=1-s>=0 this is (r1,r2)+t Delta, where Delta={x>=0,y>=0,x+y<=1}. If t<0 it is empty. Hence the nonempty unclipped family consists of translated right triangles of scale 0<=t<=1; a singleton is allowed. A singleton suffix has s=0 and gives a translate of the same scale-1 triangle. The final residuals are these sets intersected with the SAME V. The converse witness construction above realizes every such triangle before clipping.

This is genuinely narrower than arbitrary RHS sets even AFTER clipping: the generic fixed-normal system b1>=0,b2>=0,b1+b2<=4 yields the whole V. If a realizable residual equaled V, containing (0,0) forces r1<=0,r2<=0, and containing (2,2) forces r3<=-3. These imply s<=-3, contradicting s>=0. This argument keeps D,G,V,q and timing fixed throughout. It is a written nonrealizability argument, not an executed finite check or a proposed novel separation.

A strict class restriction does NOT imply an improved compatibility number. The inherited D2 q=1 family has r=(1,0,-1),(0,1,-1),(0,0,0), all with s=0. Its three residuals are pairwise compatible with witnesses (1,1),(1,0),(0,1) for pairs 12,13,23 respectively, yet their actual rows give -b1<=-1, -b2<=-1, b1+b2<=1, summing to 0<=-1. These are the old example's data, read from its immutable derivation; no replay is claimed. The common V contains the listed witnesses, so clipping does not destroy this obstruction. Generic rational planar Helly gives the upper bound three (with individual/small-family feasibility understood). Thus this frozen q=1 template already attains the generic three-prefix obstruction size. This equality is only an informal source-to-model deduction here, not a fresh general proof check. It does not extend Hanner's invariant I(K) to a Helly-number identity.

## 5. Exact nearest-source comparison and no experiment decision

Hanner (1956), original PDF physical pp1–2, printed pp65–66, defines I(K) as the SMALLEST size of a pairwise-intersecting translate family with empty total intersection. His Main Theorem B implies I(Delta)=3 since a triangle is not centrally symmetric. This is not the maximum size of a minimal infeasible subfamily and not a grouped fixed-normal classification. His hypotheses require a compact real convex body with interior; they do not directly cover empty/point residuals or clipping each translate by a fixed box. The explicit inherited D2 witnesses handle this box placement and are rational. Hanner therefore closes the familiar translate obstruction mechanism; it does not certify our support-vector formula or all fixed-template results.

De Loera et al. arXiv:1508.02380v1 physical pp1–3 explicitly state the convex Helly result and its subfield extension. They supply only the generic rational upper bound, not a new sharp dynamics restriction. Zhen–den Hertog–Sim's inspected author manuscript physical pp7–8, Algorithm 1 and Theorem 1, supplies exact elimination and reconstruction of linear adjustable variables. To apply such elimination here one must first stack actual suffix rows on each observed cell with ONE b; applying it separately by path would change information. Neither that translation nor the finite-max witness condition above supplies an established research delta.

No meaningful non-elementary discriminator survived these two selections. Mathematical experiments, frozen test inventory, new exact arithmetic runs, Lean, comparator and proof-agent work were therefore SKIPPED. Test count is zero, not twelve convenient examples. Source/delivery validation is separate and does not test the general derivations. No finite-to-universal inference, novelty verdict or scientific status promotion is made.

## 6. Logical review and what could change the decision

The main potential invalid inferences were: unrestricted embedding => universality for every fixed template; strict support restriction => strict residual-set restriction; strict class inclusion => smaller compatibility number; existence of three pairwise-overlapping translates => a Helly-number formula. None is used. The fixed-template set separation is shown independently; the inherited three-prefix witness addresses the third inference; the generic rational Helly source provides a separate upper bound. No historical proof is treated as a checker of our algebra.

A useful next input would be a scientifically motivated, independently fixed template with channels/domains whose row-image max-closure excludes the known obstruction, plus an original-source comparison showing that the desired consequence is not merely interval/product, translation Helly, exact elimination or a positive-dependence restatement. For example, the actual printed A4 dynamics/terminal data could supply such a motivated restriction only after a specific changed admissibility model and a concrete non-elementary obligation are justified; its original product disturbance model already has common suffix availability. No new target is selected here, and repeating these two source loops without that additional evidence is not recommended.
