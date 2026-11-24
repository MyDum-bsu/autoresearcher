# Exact single-closure OGU → ARO correspondence

## Authority, scope and status

This is a source-faithful application dossier, not a novelty claim. A4 physical pp2–6 and A3 physical pp2–5 define the model and information pattern. BT04 physical pp3–5 supplies information-basis terminology and Theorem 2.2. GTW20 physical pp1,3–4 supplies its fixed-recourse model and Proposition 1 with vertex interpolation. `sources.json` binds original PDFs and fresh page extractions. The derivations below are written reconstructions; no Lean theorem, thesis admission, scientific status promotion or human attestation is supplied. The seven historical routes and failures remain unchanged.

The live glossary §2 attributes A=I, discrete signs and an L1 terminal criterion to A4. Original A4 (1.1) instead allows general A, continuous box disturbances, a polyhedral terminal set and signed linear terminal cost. This dossier uses the latter. The live glossary and legacy Lean strategy are not modified or used to infer a theorem.

## 1. Data and complete bidirectional dictionary

Use state dimension n, control dimension m, disturbance dimension p, horizon T, fixed closure r with 0<r<T. Source notation M is E here, and source control dimension r is m here to avoid collision with closure time. Source stationary recurrence is

`x[t+1]=A x[t]+B u[t]+E w[t], x[0]=x0`.

U=[u_min,u_max] is nonempty bounded closed (hence convex compact), with componentwise bounds; W=[−rho,rho]^p, rho>0. Different times admit every combination in the Cartesian product. This is set-theoretic independence, not a probability assumption. XT={x:g_min≤H x≤g_max}; all its rows remain present. Cost is `c^T x[T]`, c unrestricted in sign. No intermediate state constraints or later measurements are included. A3/A4 do not assert Borel regularity explicitly on these pages; Borel rules are our explicit implementation convention. The vertex construction below shows that adding this convention does not alter feasible epigraph levels for this polyhedral class.

| OGU object | Information-faithful ARO object | Reverse interpretation |
|---|---|---|
| Initial program a=(u[0],…,u[r−1])∈U^r | Common first-stage decision a | Execute it chronologically before measurement |
| Guaranteed cost upper bound eta∈R | Nonadjustable epigraph scalar | Bound worst-case signed terminal cost |
| Exact observation s=x[r] | Information basis s, or deviation xi=s−s0(a) | A known subtraction using stored first-stage a |
| Reachable observation set S(a) | Translated uncertainty image s0(a)+Z | Every element has a feasible prefix disturbance realization |
| Entire suffix b=pi(s)∈U^(T−r) | Adjustable vector y(xi)=pi(s0(a)+xi) | Select all suffix inputs at r, execute without later observation |
| Prefix path w−∈W^r | xi=L w−∈Z=L(W^r) | Path history is not supplied to recourse |
| Independent future w+∈W^(T−r) | Unobserved robust uncertainty, then exact support constants | Still chosen after the whole suffix block is fixed |
| Robust terminal membership | Each terminal robust inequality | Same physical constraints, not a sampled replacement |
| inf over programs and policies, sup signed cost | min eta subject to robust epigraph row | Equal feasible epigraph levels and equal infima |
| No admissible program/policy | ARO infeasible; value +infinity | No synthetic continuation or fallback feasibility |

For fully specified products, define Phi(t,k)=A[t−1]…A[k] for k<t and Phi(k,k)=I. The source is A[t]=A, B[t]=B, E[t]=E. Allowing deterministic time-varying matrices in these products is a separate reconstruction, not a stationary source theorem. With chronological block ordering,

`s0(a)=Phi(r,0)x0+Σ[t<r]Phi(r,t+1)B[t]a[t]`,
`L=[Phi(r,1)E[0] | … | E[r−1]]`, `xi=L w−`, `Z=L(W^r)`,
`P=Phi(T,r)`, `F=[Phi(T,r+1)B[r] | … | B[T−1]]`,
`G=[Phi(T,r+1)E[r] | … | E[T−1]]`.

Thus `s=s0(a)+xi` and exactly

`x[T]=P(s0(a)+xi)+F b+G w+`.

Equivalently `x[T]=d+C−a+P L w−+F b+G w+`, where d=Phi(T,0)x0 and C− has blocks Phi(T,t+1)B[t], t<r. In particular `P s0(a)=d+C−a`. These identities preserve the initial-state objective offset; the source's open-loop LP may omit its constant for optimization but it must be restored for reported guarantees.

## 2. Exact quantifiers and both witness transformations

An OGU epigraph witness is `(a,pi,eta)` with pi Borel on the closed reachable set S(a), taking values in U^(T−r), and

`exists a,pi,eta; forall w− in W^r; [b=pi(s0(a)+Lw−)]; forall w+ in W^(T−r): x[T] in XT and c^T x[T]≤eta`.

The single pi is chosen as a contingent rule, not chosen anew after seeing w+. The trajectory cost uses a supremum (a Borel rule need not attain its worst case). Define the value as the infimum of feasible eta; infeasibility gives +infinity. Compact control boxes bound every terminal cost, so a nonempty feasible class cannot have value −infinity.

The exact ARO witness is `(a,y,eta)` with y:Z→U^(T−r) Borel and

`forall xi in Z; forall w+ in W^(T−r): P(s0(a)+xi)+F y(xi)+G w+ in XT, c^T[P(s0(a)+xi)+F y(xi)+G w+]≤eta`.

Z is fixed independently of a: first-stage dependence is solely in the known translation s0(a). Observing s and storing a determines xi by subtraction. Conversely xi and a determine s. Thus this is exogenous deviation uncertainty with an implementable information basis, not an assertion that the translated state set is itself exogenous.

Forward witness transformation: set y(xi)=pi(s0(a)+xi). Reverse: set pi(s)=y(s−s0(a)) for s∈S(a). Translation preserves Borel measurability. Both transformations use the same a, same b for every actual prefix path, same chronological dynamics and hence the same entire trajectory and exact worst-case cost, not just an inequality between optimal values. Any total rule on R^n can be obtained off the closed reachable set by a fixed member of U^(T−r); this is a mathematical off-domain extension and makes no robust-feasibility promise there. The existing executable instead rejects unreachable measurements explicitly.

If one writes recourse as beta(w−), the necessary information constraint is

`Lw−=Lw−' implies beta(w−)=beta(w−')`.

A fully informed path rule without this equality is not the same witness class. Nevertheless existence at a given epigraph level is unchanged in this rectangular terminal model: for fixed a,eta, define K(xi) as the suffix control box intersected with all support-tightened terminal/cost halfspaces in §3. Its graph is polyhedral and its rows depend on w− only through xi. If a path rule is feasible then K(xi) is nonempty for every xi, since xi has a prefix preimage. Vertex selection and the finite triangulation of §4 construct a Borel fibre-constant selection from K. This replacement can change actual controls and trajectories of the unrestricted path rule; equality of actual trajectories is claimed only for the information-faithful witness transformations above. Neither an arbitrary fibre-constant measurable path rule's quotient measurability nor a hidden measurable selection theorem is assumed. The construction supplies the needed measurable witness directly. Correlated future sets, history-dependent constraints or objectives would invalidate this redundancy argument.

## 3. Eliminate future uncertainty exactly, without observing it

Write terminal inequalities R x≤h with R=[H;−H], h=[g_max;−g_min]. For any row vector v^T, define

`kappa(v)=sigma[W^(T−r)](G^T v)=rho Σ[t=r..T−1] ||E[t]^T Phi(T,t+1)^T v||_1`.

For non-centred independent boxes replace each term with the actual box support, including its centre offset. For the source centred boxes kappa(v)=kappa(−v), but c itself must not be replaced by |c|. For z=P(s0(a)+xi)+F y(xi), the exact rows are

`R_i z≤h_i−kappa(R_i^T)` for every terminal row i,
`c^T z−eta≤−kappa(c)` (a distinct cost row),
`u_min≤y_t(xi)≤u_max`.

Each equivalence follows from `forall w+: v^T(z+Gw+)≤b iff v^T z+sup[w+] v^TGw+≤b`. Suprema exist for these continuous linear functions on compact boxes. Different rows may have different maximizers; no joint extremizer is required. Rectangularity is essential: exactly the same future product set applies at every reachable state and every prefix. Quantifiers are `forall xi exists b forall w+`, not `forall xi forall w+ exists b`.

For reward `e2^T x[T]`, use c=−e2 and eta=−q: `min worst cost = − max guaranteed reward`. A reward certificate L≤V_reward≤U becomes −U≤V_cost≤−L. Negative terminal coordinates are legitimate; no norm, absolute cost or nonnegative truncation is introduced.

## 4. Source-hypothesis-checked finite vertex model

Z is a nonempty compact polytope because it is a linear image of a finite-dimensional box, even when L has deficient rank. Let v_1,…,v_N be its actual vertices. Minimize eta over common `(a,eta)` and b_j∈U^(T−r), imposing at every v_j the rows of §3 with y(v_j)=b_j. This is an LP. The rows are affine in `(a,eta,xi,b)`; their recourse coefficients `[R F; c^T F; I;−I]` are fixed, not uncertain. First-stage box rows may be imposed once. Recourse need not be feasible for every a; the LP tests it, rather than assuming relatively complete recourse.

BT04 Theorem 2.2 (physical p5) requires a given finite convex hull of coefficient tuples and a common recourse matrix. Here the affine map from Z to coefficient tuples maps conv{v_j} to the convex hull of their tuples, with exactly that fixed matrix. It need not preserve extremality or be injective: the theorem permits any finite hull-generating list. GTW20 (physical p1) assumes nonempty bounded polyhedral Xi, affine T and h, fixed W; its Proposition 1 (pp3–4) gives restriction/interpolation. All these hypotheses hold after deviation parametrization and support elimination. No claim invokes BT04 Theorem 2.1's constraint-wise independence: the terminal rows share xi and generally fail that condition. Independence across disturbance times is a different property.

Necessity: each v_j∈Z has a prefix preimage. Evaluate the state rule at s0(a)+v_j. The entire future set is allowed there, hence b_j satisfies all finite rows. Sufficiency and measurability: fix a finite triangulation of Z in its relative affine hull using only its vertices (for example a pulling triangulation with a fixed vertex order). Order its simplices and assign a boundary point to the first containing simplex. Solve its unique barycentric coordinates within that affinely independent simplex, and define y(xi)=Σ_j lambda_j(xi)b_j. All weights are nonnegative and sum to one, so the control box and every affine robust row are preserved. Each region is Borel, its coordinates affine and continuous relative to the simplex; the finite tie rule is Borel. Adjacent simplex interpolants agree on shared faces. This supplies one state-implementable rule for every reachable REAL state, not only rational states or sampled paths. The triangulation construction/regularity details are written reconstruction complementing the inspected source interpolation theorem, not a machine-formal proof.

No inverse dynamics is used. If dim Z=0, there is one deviation and one suffix block. If dim Z=1, use intervals and their endpoints; in higher deficient dimension use relative-affine coordinates. The same finite proof applies when A, P or L is singular. Even uncertainty-coordinate vertices of W^r need not map to distinct states or to vertices of Z: duplicates/interior images must not be mistaken for observed-state vertices.

One may alternatively use terminal deviation Q=PZ with zeta=Pxi. In this terminal-only rectangular model all rows depend on xi only through zeta. A vertex LP and triangulation on Q therefore also give an exact EXISTENCE/optimal-value formulation, with implementation b(s)=g(P(s−s0(a))). When P is singular, distinct observed states may share zeta; using g then restricts witnesses but not achievable epigraph levels, because their feasible suffix sets are identical. This is not a bijection of arbitrary state policies or their trajectories. For the four legacy cases P is invertible and their terminal-deviation polygons have N=2r vertices; their implementation uses those polygons. Its explicit invertibility check is a boundary of that legacy implementation, not a hypothesis of the general transfer here.

The LP is finite and its control variables range over a compact box; if feasible, minimizing eta attains a finite optimum (eta can be tightened to the finite maximum of its vertex rows). The constructed Borel rule attains that same guarantee. This attainment statement is a written consequence, not an observed solver result or an exact-optimality claim for the saved nonzero-gap certificates.

## 5. Closure sets in the same signed-cost model

Define `C_eta={s: exists b∈U^(T−r), R(Ps+Fb)≤h−kappa_R, c^T(Ps+Fb)≤eta−kappa(c)}`. Define feasibility-only C by dropping the last row. Then

`exists state policy with bound eta for a iff S(a)⊆C_eta`.

The forward implication evaluates its suffix at every reachable state; the reverse chooses vertex witnesses and interpolates as above. C_eta is a convex polyhedral projection of the joint (s,b) rows. A3's J1 and A4's last-block value have C_eta as their sublevel set and C as their finite-value domain; +infinity marks infeasible states. For reward q, the same set uses `e2^T(Ps+Fb)≥q+kappa(e2)` and is a reward superlevel set. There is no switch of physical model between ARO and closure sets.

A vertex extended formulation retains b_j at observed deviations; a closure-set H-representation projects out b once and tests containment; a support representation tests all relevant directions. Exact representations agree. Replacing C_eta by an outer set makes containment easier, supplies only a relaxation (lower cost / upper reward bound), and does not certify an admissible policy. An inner set whose points come with actual implementable suffix witnesses supplies a feasible restriction (upper cost / lower reward bound). A finite subset of states alone is only a relaxation unless its convex hull covers S(a) and interpolation hypotheses hold. Closure feasibility alone does not certify a cost level. This distinction preserves the source's warning about approximate continuation sets and the historical failed controls.
