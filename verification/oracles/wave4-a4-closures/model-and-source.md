# A4 continuous single-closure formulation and certificate semantics

## Source and identity

Original research/sources/A4.pdf SHA256 4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420. Fresh physical-page layout extractions are in artifacts/goal/wave-4/pilot/source/. Physical pp2–4 define the linear dynamics, independent per-time disturbance box, terminal feasibility for every sequence and exact current-state observation followed by a whole-block control choice. Pp5–6 define blockwise strategies and closure sets. Pp9–11 derive support-based outer approximations and (2.20). Pp11–12 explicitly warn that outer containment need not imply true closure containment, permitting degraded reward or infeasible continuation (p11: “вообще говоря, не гарантирует”; p12: “продолжить процесс управления после момента Tj невозможно”). Pp12–13 give Example 1 and report 203 initial normals, 103 retained inequalities, approximate reward 2.913110 at 67 and trajectory reward 2.912640. The trajectory-based difference is not assumed to be a separately certified universal bound. Pp15–17 identify earlier exact feedback methods and the prior single-closure paper [14]. No source-error allegation is made.

M0 input scope labels say open_loop: those labels remain immutable provenance of the coefficient manifests, NOT the policy class in this wave. New certificates bind a separately named single-closure contract. Printed decimal coefficients define an exact rational instance; reconstructed decimal coefficients are a different inferred instance, not verified author/trigonometric data. This wave is not the earlier correlated finite-path model. No novelty conclusion is drawn from numerical agreement, discrepancy, or the following familiar convex construction.

## Finite reduction (written reconstruction; not a formally checked general theorem)

For each pinned coefficient variant and r, the exact claim is a bound on
sup {q : there exist a in [-1,1]^r and a Borel state policy pi:R^2 -> [-1,1]^(120-r), such that for every w_pre in [-1/2,1/2]^r and every w_suffix in [-1/2,1/2]^(120-r), the full chronological dynamics starting at (0,1), using a then pi(x(r)), satisfy 2<=x1(120)<=10 and x2(120)>=q}.
Only reachable states need a certified continuation; the implementation reports an error on off-domain measurements. It can be extended mathematically by the fixed zero block off that closed polygon to obtain a total Borel function without changing any reachable trajectory. That off-domain extension is not asserted robustly feasible. No intermediate state constraints are present in Example 1.

Let r=T1, n=120-r, C_t=A^(119-t)B, D_t=A^(119-t)E and d=A^120 x0. The first block a lies in [-1,1]^r. The terminally propagated prefix disturbance is
Z=sum_{t<r} [-D_t/2,D_t/2].
The remaining disturbance support is s_j=(1/2)sum_{t>=r}|(D_t)_j|. Because the suffix disturbance is independent of all prefix disturbances, the same full suffix box applies at every measured state.

Let v_i enumerate the ACTUAL planar vertices of Z. The finite program maximizes q, with common first-block a and suffix b_i in [-1,1]^n per vertex. For every i put h_i=d+sum_{t<r} C_t a_t+v_i+sum_{t>=r} C_t b_it. Require
h_i1>=2+s_1, h_i1<=10-s_1, h_i2>=q+s_2.
These are three robust rows per vertex. Continuous boxes have not been replaced by sampled disturbances: suffix support is exact, and prefix polytope convexity is used explicitly.

Necessity: every vertex is an attainable prefix disturbance image. An admissible state policy evaluated at those measured states supplies the b_i, so its guarantee cannot exceed the finite optimum. Distinctness follows from invertible A^n (the pinned A has nonzero determinant). No vertex index or disturbance history is supplied to the controller.

Sufficiency/every-state implementation: store a and b_i. At r measure z and compute v=A^n z-d-sum C_t a_t. It lies in Z. Use the ordered fan triangles (v_0,v_i,v_(i+1)), i=1,...,m-2, in ascending index; choose the first triangle containing v and compute exact barycentric weights. Select the entire suffix as the weighted sum of its three stored b's. Triangle boundaries are resolved by that fixed index rule. Box feasibility and all three terminal inequalities follow by affine combination, then exact suffix support covers every future disturbance. The policy is piecewise affine, Borel measurable, and uses current state only; it never measures future state. Outside the reachable polygon it raises an explicit domain error, rather than pretending a continuation is certified. A runnable exact state-to-block routine accompanies the arithmetic checker. The triangulation argument is written mathematics, not a Lean theorem; coordinator/reviewer must inspect it.

## Exact lower and upper certificates

A numerical LP proposes controls and dual weights only. The producer rounds controls to rational numbers, then repairs each suffix nominal x into the exact robust slab using its remaining control capacity. The checker evaluates every vertex row with Fraction arithmetic; lower=min_i(h_i2-s_2). This proves a universal policy lower bound conditional on the reconstruction above, not just selected trajectories.

Write finite rows M u+e q<=b, all control variables u in [-1,1]. Let lambda>=0 and e^T lambda=1 exactly. Then for every feasible point
q<=b^T lambda-(M^T lambda)^T u<=b^T lambda+||M^T lambda||_1.
Thus U=b^T lambda+||M^T lambda||_1 is a rigorous upper bound, even if rounded numerical multipliers leave stationarity residual. The checker recomputes every coefficient and residual exactly. Equality L=U alone would establish finite optimum and, with model/policy reasoning, continuous-policy optimum. Nonzero gaps are reported as intervals, not exact optima. Negative weights, changed bindings, missing vertices or incorrect row semantics must fail.

## Independence and limitations

M0 generator/checker were inspected before implementation. Their open-loop certificate format is inadequate for a state policy. M0's pinned input parser/checker and backward-adjoint column builder are reused readonly through wave-local copies; the producer uses forward powers. The new checker does not invoke the numerical solver or trust its status. The arithmetic route is independent of floating optimization, but both new files were authored in one worker, and M0 arithmetic is shared; Stage B is still required. Vertex identities include explicit prefix sign realizations; edge supports and reachable vertices are checked exactly. General convex interpolation/policy equivalence remains a written argument. No claim of new generic vertex reduction, published-policy reproduction, time-optimal closure or first scientific success is authorized.
