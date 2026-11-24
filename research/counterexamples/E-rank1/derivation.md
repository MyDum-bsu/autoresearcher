# E: the rank-one continuation boundary, with its missing singleton premise

Claim family: `E-R1`, version 1. Parent: `D2-C1-v1` as quoted in `research/structured/handoff.md` §5. This is a new mathematical derivation with finite exact controls, not a replay of the D2 triangle. General statements below have evidence kind `unproved-sketch`: no Lean proof or independent formal verdict is supplied. The argument is given in full for independent criticism. Executed rational checks establish only their frozen instances.

## 1. Statement repair and decision

Interpret “pairwise” as distinct indices. The literal parent is false for a cell containing one prefix: its pairwise premise is vacuous even if that prefix has no feasible continuation. This issue occurs already at rank zero and is realizable in the question's dynamics. It does not refute the substantive rank-one claim when every residual system is nonempty. If “pairwise” includes a prefix paired with itself, the parent already includes this missing premise. The handoff did not specify that convention.

Preserve the parent. Use the following explicit child, `E-R1-child-v1`:

Let I be a finite nonempty state cell, V={b in Q^N: l<=b<=u} a nonempty bounded closed rational box, L in Q^(J x N), and d_p in Q^J for p in I. Define K_p={b in V:L b<=d_p}. Suppose rank_Q(L)<=1, every K_p is nonempty, and K_p intersect K_s is nonempty for every distinct p,s. Then the intersection of all K_p is nonempty over Q. Conversely joint nonemptiness implies these premises.

For |I|>=2, the pairwise premise alone implies each K_p is nonempty. For |I|=1 it does not. This repair preserves the scientific comparison: prefix feasibility in the question already requires every K_p nonempty. Thus, under rank<=1, prefix feasibility plus pairwise compatibility suffices for state feasibility cell by cell. Prefix feasibility ALONE still does not suffice; the new q=1 check gives an incompatible pair at rank one.

The practical consequence is a proposed complete singleton/pair obstruction test for the rank-one residual representation. At rank two the D2 handoff supplies a three-prefix obstruction; that historical result is not independently replayed here. No claim that rank one is necessary for a particular compatible system follows.

## 2. Map from the exact dynamics

Fix a and q from `research/question.md`. Expand each linear transition successively, with Phi(t,s)=A_(t-1)...A_s and Phi(s,s)=I. Then

    x_T = Phi(T,r) z_a(p) + G b + eta(s),
    G = [Phi(T,r+1)B_r | ... | B_(T-1)],
    eta(s) = sum_(t=r)^(T-1) Phi(T,t+1)E_t w_t.

This follows by substitution; no observed suffix is used in choosing b. Put D=[H;c^T], beta=(h,q-d0). A finite nonempty S(p) permits a rowwise maximum rho_(p,j)=max_(s in S(p)) D_j eta(s). Universal hard/cost constraints are exactly

    L b <= d_p,
    L = D G,
    d_p = beta - D Phi(T,r)z_a(p) - rho_p.

The maximum is over each actual conditional suffix set, not a marginal product. Every quantity is rational and each maximum is attained in that finite set. The following argument only needs a common L and V; it does not assume that different prefixes share suffix sets. This is a reconstruction from the declared model, not an attributed external theorem or a formal proof of source correspondence.

## 3. Constructive argument, including degenerate cases

### Rank zero

If L=0 then K_p is V when all entries of d_p are nonnegative, and empty otherwise. Individual nonemptiness therefore makes every K_p equal to V. The rational lower endpoint l belongs to their intersection. Empty residual systems must be rejected before any pair test.

### Rational rank-one factorization

If rank_Q(L)=1, choose a nonzero row ell of L and a coordinate k with ell_k!=0. Define v_j=L_(j,k)/ell_k. Rank one implies every row is proportional to ell, so L_j=v_j ell; the definition fixes the rational proportionality factor. In particular a zero row has v_j=0. All entries of ell and v are rational. This is a row-rank condition on the hard/cost matrix L, not on the dynamics alone and not on L augmented by the box inequalities.

### Exact image of the common box

Let b_minus choose l_i when ell_i>=0 and u_i otherwise; let b_plus choose u_i when ell_i>=0 and l_i otherwise. Set t_minus=ell b_minus and t_plus=ell b_plus. Coordinatewise bounds give t_minus<=ell b<=t_plus for every b in V.

Conversely, for rational t in that closed interval, if t_minus<t_plus put

    alpha=(t-t_minus)/(t_plus-t_minus),
    b(t)=(1-alpha)b_minus+alpha b_plus.

All coordinates are rational, alpha is in [0,1], each coordinate remains in its box, and ell b(t)=t. If t_minus=t_plus the image is a singleton: use b_minus and never divide by zero. This handles singleton boxes and boxes that vary only in coordinates annihilated by ell. Thus the rational image is exactly [t_minus,t_plus] intersect Q, with a common rational section independent of prefix.

### Prefix intervals and zero rows

For each p, first reject any row with v_j=0 and d_(p,j)<0. A zero row with nonnegative right side imposes no scalar restriction. The remaining rows yield

    lower_p = max({t_minus} union {d_(p,j)/v_j : v_j<0}),
    upper_p = min({t_plus} union {d_(p,j)/v_j : v_j>0}).

Division reverses the inequality for negative v_j. The finite sets defining both endpoints are nonempty because box endpoints are included. Hence both endpoints are finite rational numbers. K_p is the inverse image of the closed rational interval [lower_p,upper_p]; it is empty exactly when the zero-row check fails or lower_p>upper_p. In particular nonempty V alone is insufficient.

### Joint intersection without an external intersection theorem

By the explicit individual premise all prefix intervals are nonempty. Let lower_star=max_p lower_p and upper_star=min_p upper_p; both are attained since I is finite. Choose indices p_star,s_star attaining them. If lower_star>upper_star and those indices coincide, their individual interval is empty, contradiction. If they differ, their two intervals are disjoint, contradicting pairwise compatibility. Therefore lower_star<=upper_star. Choose the rational t=lower_star and lift it by the common section b(t). It belongs to every K_p.

The converse follows by taking the same joint point in each singleton and pair. This is a complete written elementary argument, still awaiting machine formalization and independent review. Finite regression evidence is not its proof.

## 4. New dynamics-realizable checks

All six fixed cases use T=2,r=1,n=d=1,m=2, x_0=0, A_0=A_1=0, B_0=(0,0), E_0=0, E_1=1, U_0={(0,0)}, H=(-1), h=0, c=1,d0=0. A complete path has w_0 equal to its prefix index and the specified scalar suffix s. Thus all measured states x_1=0, prefixes are distinct, and x_2=B_1 b+s. Each prefix has one suffix; no suffix-dependent action is allowed. Standard U_1=[0,2]^2.

For B_1=(1,-1), write t=b_1-b_2. Prefix suffix s gives -t<=s and t<=q-s. The common matrix has rows (-1,1),(1,-1), rank one.

- `E-common`: s=(-1,0,1), q=2. Intervals after the box are [1,2],[0,2],[-1,1]. Their joint scalar interval is {1}; b=(3/2,1/2) is the section witness. Terminal states are (0,1,2), with costs <=2 and all hard constraints satisfied.
- `E-separated`: same suffixes, q=1. Every individual interval is nonempty, but the first and third are disjoint. Their actual rows -t<=-1 and t<=0 sum with nonnegative multipliers 1 to 0<=-1. This is a continuous-box infeasibility certificate, not finite action enumeration. It prevents overstating rank one as unconditional losslessness.
- `E-singleton-r1-empty`: s=(-3),q=0. Its sole residual system requires t=3, outside the box image [-2,2]. Distinct-pair compatibility is vacuous; the actual box row t<=2 (from b_1<=2 and -b_2<=0) together with -t<=-3 certifies infeasibility.
- `E-singleton-r0-empty`: B_1=0, s=(-1),q=0. The sole terminal state is -1, so its hard inequality is 0<=-1. This is the literal singleton counterexample already at rank zero. c remains nonzero.
- `E-singleton-r0-feasible`: B_1=0,s=(0),q=0. The whole box works.
- `E-singleton-image`: B_1=(1,-1),s=(-1,0),q=1, U_1={(1,0)}. Both prefixes are feasible at t=1; the singleton-image section must avoid division by zero.

`checks/rank_one_check.py` constructs scalar sections and independently reconstructs all original two-dimensional trajectory inequalities. A second route intersects boundary lines and checks every rational vertex against every inequality for every singleton/pair/joint subset. Boxes are bounded, including degenerate boxes: a nonempty polygon has a vertex, so the fixed feasibility comparisons do not use a finite action menu as a substitute for a continuous box. For every infeasible subset an explicit nonnegative row certificate is checked as well. The routine is candidate-specific and capped at six instances, seven subsets per instance, ten rows per subset and 45 boundary-pair solves per subset (at most 1,890 solves). It is not introduced as a reusable project judge.

Controls reject a false common action, reject the reversed-sign scalar formula, reject negative certificate multipliers, and record that singleton distinct-pair tests are vacuous while the joint problem is infeasible. Exact Fraction arithmetic, not floating point, supplies all observations.

## 5. Remaining gap

The general child is not Lean-checked. The dynamics-to-residual equivalence is a written substitution argument, not a formal semantic correspondence theorem. No new source comparison or novelty search was undertaken, and no external intersection theorem is invoked. The immediate continuation obligation is sharpened to independent review/formalization of this explicit child, rather than searching for a three-prefix rank-one counterexample under individual feasibility. No private-isolation, general research-capability, live scientific-status or human-attestation claim follows.
