# Astra probe: a coordinate-separable rank-two subclass

Task aro-discovery-k4t. One approach: coordinate-separable residual rows. This is a supplementary exposed attempt, not blind or matched benchmarking. Parent E-R1-child-v1 remains unchanged. General claims below are authored mathematical arguments (campaign category `unproved-sketch`), not machine-proved theorems or scientific attestation.

## A-S1: quantified subclass statement

Fix the exact rational dynamics, fixed first program a, rational bound q and one finite nonempty measured-state cell I of research/question.md. Let N=m(T-r), V=[l,u] intersect Q^N be the SAME nonempty box for every prefix. Expand the dynamics by substitution:

    x_T = Phi(T,r) z_a(p) + G b + eta(s),
    G = [Phi(T,r+1) B_r | ... | B_(T-1)],
    eta(s) = sum_(t=r)^(T-1) Phi(T,t+1) E_t w_t,
    Phi(t,s)=A_(t-1)...A_s, Phi(s,s)=Id.

With D=[H;c^T], beta=(h,q-d0), define L=DG and

    d_(p,j) = beta_j - D_j Phi(T,r)z_a(p)
                        - max_(s in S(p)) D_j eta(s).

Each maximum exists and is rational because S(p) is finite and nonempty. A row holds for every actual suffix iff it holds with that maximum. Different rows may attain their maxima at different suffixes: this is conjunction of inequalities, not Cartesian completion of paths. Therefore exactly

    K_p = {b in V: Lb <= d_p}.

Subclass hypothesis: every nonzero row of L has support in ONE continuation coordinate, and across all rows exactly TWO distinct coordinates occur with nonzero coefficients. Thus rank_Q(L)=2. No condition requires equal right sides, equal suffix sets, nested K_p or a prescribed common witness. All family sizes and all rational right sides admitted by these dynamics are allowed. Extra action coordinates, if present, remain free within V. For a physically nondegenerate member require positive box widths in both used coordinates; the proof also covers boundary/empty residual cases.

**Claim A-S1.** In this subclass, individual nonemptiness of every K_p and nonemptiness of every distinct-pair intersection are equivalent to nonemptiness of their full intersection over Q. This is a structural sufficiency condition at rank two; it disproves necessity of rank at most one for such subclass guarantees. It does NOT make rank two alone sufficient. In particular it does not negate a claim about a guarantee based solely on rank, with all rank-two matrices admitted.

## Direct proof, without an imported intersection theorem

A zero row with negative right side makes K_p empty. Individual nonemptiness excludes it; a zero row with nonnegative right side adds nothing. For a row alpha e_i with alpha>0 the constraint is b_i<=d_(p,j)/alpha. For alpha<0 it is b_i>=d_(p,j)/alpha, with the inequality reversed. Let a_(p,i) be the maximum of l_i and all these lower bounds, and b_(p,i) the minimum of u_i and all upper bounds. Empty lists of row bounds leave the box endpoint. All endpoints are rational and finite. We have the exact product representation

    K_p = product_i [a_(p,i), b_(p,i)] intersect Q^N.

For each coordinate put A_i=max_p a_(p,i), B_i=min_p b_(p,i). Choose attaining indices p_i,s_i. If A_i>B_i and p_i=s_i, that individual K_p is empty. If they differ, their two coordinate intervals are disjoint, so the two sets cannot intersect. Both contradict the hypotheses. Hence A_i<=B_i for every coordinate. The SINGLE vector with coordinates A_i is rational, lies in V and satisfies every row of every K_p. Conversely any joint point witnesses every singleton and pair. Finite I and individual nonemptiness are essential to this stated proof, including singleton cells.

Coordinatewise assembly is legitimate because the common box and every residual row separate in the SAME coordinates. Rank-one projection in E is replaced by a two-dimensional product. Arbitrarily rotating the row axes while keeping V unchanged is not justified: the image of V might couple the two coordinates. No such extension is claimed here.

## A-E1: faithful nondegenerate dynamics realization

Take T=2,r=1,n=m=d=2,x_0=(0,0). A_0=B_0=E_0=A_1=0, B_1=E_1=Id_2. U_0={(0,0)}, U_1=[0,5]^2 intersect Q^2. Thus x_1=0 and x_2=b+w_1. Let

    H=[(-1,0),(0,-1),(1,0),(0,1)], h=(0,0,4,4),
    c=(-1,0), d0=0, q=-1.

Keep exactly these four complete paths:

| prefix w_0 | suffix w_1 |
|---|---|
| (0,0) | (-1,0) |
| (1,0) | (0,-1) |
| (0,1) | (0,0) |
| (0,1) | (1,1) |

The third prefix has two genuinely hidden suffixes. All three states measured at r coincide. Neither policy knows w_1 when choosing b. Every trajectory must satisfy 0<=x_(2,i)<=4 and signed cost -x_(2,1)<=-1; the cost cannot be replaced by its absolute value. L has rows -e1,-e2,e1,e2,-e1 and rank two, witnessed by its first two rows' determinant 1. The residual sets are

    K1=[2,5] x [0,4],
    K2=[1,4] x [1,5],
    K3=[1,3] x [0,3],
    intersection=[2,3] x [1,3], all over Q.

Each has positive area and none of the three contains another. Both continuation coordinates affect hard feasibility. The nonzero signed cost cuts off actions that satisfy all hard constraints, e.g. b=(0,0) for suffix (0,0); its lower bound is active at b_1=2 for prefix 1. The hard upper bounds also restrict the joint set. Hence this is not a rank-one feasible image disguised by unused rows, a singleton action set, a common residual signature, or a one-instance-only family assertion.

The common b=(2,1) yields terminal states (1,1),(2,0),(2,1),(3,2), signed costs -1,-2,-2,-3. It witnesses all singletons, all three pairs and the joint intersection, including both suffixes of prefix 3. b=(5/2,2) is an interior common point. V, H, h, c and q are identical for every prefix. E_0=0 intentionally erases the prefix's state imprint, as allowed in the frozen model; it does not reduce the rank of continuation response G=Id. The singleton first-block box removes any first-stage optimization ambiguity.

## Falsifiers and scope controls

A-E2 keeps the same data and paths but sets q=-3. The sets become [4,5]x[0,4], [3,4]x[1,5], [3,3]x[0,3]. They are individually nonempty, but K1 and K3 are disjoint: prefix 1's cost row -b_1<=-4 and prefix 3's suffix (1,1) upper row b_1<=3 sum to 0<=-1. Thus the subclass does not imply unconditional prefix/state losslessness.

A-E3 retains the same dynamics/terminal rows and q=-1 but uses two paths with the SAME prefix (0,0), suffixes (-1,0) and (3,0). Legal continuation requires b_1>=2 and b_1<=1; the actual cost and hard rows sum to 0<=-1. Separate suffix-aware actions (2,0) and (0,0) satisfy their respective trajectories, but differ at the same prefix and measured state. The checker must reject that policy. This tests timing, not merely set geometry.

The inherited D2 triangle is a serious falsifier of the broader parent: its rows -e1,-e2,e1+e2 have rank two but violate the new support hypothesis. At q=1 with suffixes (-1,0),(0,-1),(0,0), the pair witnesses (1,1),(1,0),(0,1) work while -b_1<=-1, -b_2<=-1 and b_1+b_2<=1 sum to 0<=-1. The new check replays this small certificate from explicit data, without invoking or changing the original checker. The mixed cost direction couples the two individually worst coordinates; that direction is absent in A-S1. Rank alone misses this distinction.

## Evidence, sources and logical boundary

The finite script checks original transitions, row bounds, exact rational witnesses, pair witnesses, empty-set certificates, false actions, a false certificate sign, and illegal suffix-aware policies. It does not prove A-S1 or completeness of a general LP algorithm. No action-grid search is used. One code author supplies both routes, so this is not independent verification.

The authoritative source for this attempt's model is the frozen research/question.md, with the inherited source comparison in research/domain-packet.md and identities in research/resource-manifest.json. E derivation/handoff and D2 derivation were read openly. Their source claims remain inherited: no original PDF page was newly inspected and no literature attribution is used to support the new elementary proof. The packet reports that full block availability makes suffix sets prefix-independent; that stronger source premise is not required here. Correlation and unequal conditional suffix sets remain in A-E1. No novelty, priority, comprehensive literature coverage, general research capability or external theorem attribution follows.

Logical audit: quantifiers range over every finite admitted family, not just checked examples; singleton feasibility is explicit; pair feasibility is not confused with individual feasibility; rank refers to DG excluding box rows; one common action must handle every hidden suffix. The conclusion concerns existence of a state continuation under the pair premise, not implementability of every prefix policy or equality of optimized values. Remaining obligation: independent review/formalization of A-S1 together with its exact dynamics-to-residual correspondence. Comparator remains blocked; no formal release or status promotion is requested.
