---
title: "When Is an Affine Decision Rule Exact?"
subtitle: "Two-stage adaptive robust optimization, the guaranteed-control problem of the Dmitruk school, and the bridge between them: an inventory of results and open problems"
author: "aro-discovery research programme"
date: "2026-10-20"
version: "v2"
abstract: |
  This essay has three parts and one purpose: to let a reader who knows linear
  programming but not this literature arrive at the frontier and see what is
  unproved. Part I treats two-stage adaptive robust optimization on its own
  terms: the model, the four inequivalent meanings of "exact" that the
  literature conflates, the mechanisms that produce exactness, the sharp
  negative families, and the hardness results. Part II treats the other
  tradition: the guaranteed-control problem of the Dmitruk school, where a
  linear system is driven by a scalar control against a bounded disturbance and
  the state is measured at scheduled closure moments. Its general theory is
  summarised, including the multiclosure construction, the exact polyhedral
  representation of closing sets, the parametric-LP duality that makes the
  representation computable, and the a posteriori certificates. Part III states
  the bridge precisely and does the mathematics: a rotation of coordinates that
  turns the two-dimensional terminal cost into two scalars, closed forms for the
  ends of the information ladder, a block-composition and tail-sum reduction,
  and an exact treatment of the difference floor. The essay closes with eight
  open problems stated so that a theorem could settle each, a seven-instance
  falsification battery for candidate exactness conditions, and a verification
  ledger that separates what is Lean-verified, what is numerically certified,
  and what was found to be false while writing this version.
---

# How to read this essay

The reader this is written for knows linear programming, duality, and what a
worst case over a polytope is. Nothing else is assumed. Every symbol is defined
at first use and collected again in Appendix A, together with the problem in
which it lives, because the two literatures reuse the same letters for different
objects and that alone accounts for a share of the confusion in the field.

Three conventions hold throughout.

**Status words.** *Proved* means a Lean file compiles without `sorry`, or a
published proof is cited with its page. *Certified* means exact rational
arithmetic on a frozen grid found no counterexample; it is evidence, not proof.
*Claimed* means the source asserts it and we have not checked it. *Refuted*
means a counterexample exists and is recorded.

**Anchors.** A claim about the literature carries a page, a line number, or a
theorem label. Where the corpus holds the TeX source rather than a PDF, the
anchor is a line number, because that is what can be checked. Links to the
publisher appear where a DOI was verified against Crossref; the absence of a
link means only that the identifier was not verified, not that the paper is
unpublished.

**Where this essay is about its own programme.** Part III reports results of the
author's project. They are labelled by the status ladder above, and the section
that reports them also reports a discrepancy found while this version was being
written, because a survey that hides a defect in its own material is worth less
than one that does not.

![The three objects of this essay. Left: two-stage adaptive robust optimization
restricts the recourse policy. Right: guaranteed control schedules measurements.
The bridge class sits between them: a guaranteed-control instance whose
information structure is exactly a policy class, and whose terminal cost is a
worst case over paths.](figs/fig1_map.pdf){width=86%}

# Part I. Two-stage adaptive robust optimization

## I.1 The model, and why the policy class is the whole subject

Let $x \in \mathbb{R}^{n_1}$ be chosen before the uncertainty is observed — the
*here-and-now* decision — and let $y \in \mathbb{R}^{n_2}$ be chosen after
observing a realisation $\xi \in \Xi \subseteq \mathbb{R}^m$ — the *recourse*
decision. The problem is

$$
\min_{x \in X}\; c^\top x \;+\; \max_{\xi \in \Xi}\; \min_{y}\;\big\{\, d^\top y \;:\; A(\xi)x + B y \ge h(\xi),\ y \ge 0 \,\big\}.
\tag{1.1}
$$

Here $X \subseteq \mathbb{R}^{n_1}$ is the first-stage feasible set, $c$ and $d$
are cost vectors, $A(\xi)$ is the technology matrix, $h(\xi)$ the right-hand
side, and $\Xi$ the uncertainty set. Reading the symbols off the two literatures
that share this model: $x$ is what optimises in Part I and is called $x_0$ or
$u_0$ in Part II; $\xi$ is the random parameter in Part I and the disturbance
*path* $w$ in Part II; $y(\cdot)$ is the recourse *policy* in Part I and the
control *program* in Part II.

The matrix $B$ does not depend on $\xi$. This is the *fixed recourse*
assumption. It is what makes the inner minimisation an LP whose dual feasible
set
$\mathcal{W} = \{w \ge 0 : B^\top w = d\}$
does not depend on the decision or on the scenario [XB17, arlp line 379--384].
Every exactness result in Part I rests on it or on its failure being exploited
as a counterexample. Ben-Tal, Goryashko, Guslitzer and Nemirovski introduced
both the term and the observation [BGT04, p. 353].

If $y(\cdot)$ could be any measurable function, (1.1) would be the *fully
adaptive* value $V_{\mathrm{AR}}$. It is intractable in general. So the subject
is not the model; it is the restriction on the policy class. Four restrictions
recur.

| Policy class | Definition | Value notation | Where it is used |
|---|---|---|---|
| Static | $y(\xi) \equiv y$, one decision for all scenarios | $V_{\mathrm{st}}$ | [BGT04] Thm. 2.1; [BGL15]; [MDH18] |
| Affine (linear) | $y(\xi) = y_0 + Y\xi$, $Y$ of size $n_2 \times m$ | $V_{\mathrm{AP}}$ | [BGT04] §3; [XB17]; [GTW25] |
| Piecewise affine | affine on each cell of a finite polyhedral partition of $\Xi$ | — | [BG14]; [GTW20]; [ZDS18]; [BEG18] |
| $K$-adaptable | $K$ candidate policies fixed in advance, one chosen after observing $\xi$ | $V_{K}$ | [Kur25]; [GTW25] Thm. 2 |

Two parameters are design variables rather than modelling constants: the number
$K$ of candidate policies, and — in the guaranteed-control tradition of Part II —
the *schedule* $R$, the set of instants at which the state is measured. Part III
is about the second.

## I.2 Four meanings of "exact", and why the distinction is not pedantry

The literature says "exact" for at least four different statements. Several
apparent contradictions dissolve once they are separated; several real
contradictions are hidden by not separating them.

**Value exactness.** $V_{\mathrm{AP}} = V_{\mathrm{AR}}$. The restricted class
attains the adaptive optimum in value. This is what a bound on the price of
adaptivity measures.

**Solution exactness.** There is an affine rule that is optimal pointwise: for
every $\xi$ in the support it attains the inner minimum itself, not merely the
outer worst-case value. Strictly stronger than value exactness, and it does not
propagate from the optimal $x$ to nearby $x$: Georghiou, Tsoukalas and Wiesemann
exhibit a problem where the optimal value is attained by an affine rule while at
a suboptimal first-stage decision the unique optimal policy is nonlinear
[GTW25, p. 9].

**Feasibility exactness.** The affine rule attains the same robust feasible
region for $x$ as the fully adaptive problem. This is the notion in play in
vertex-reduction results, and it can fail while value exactness holds, because a
different $x$ may compensate for an infeasible policy.

**Reformulation exactness.** In the semidefinite and sum-of-squares literature
"exact reformulation" means that the conic program has the same value as the
*rule-restricted* problem, with a bijection of optimal solutions
[CJW21b, p. 1; JLLLW22, p. 2]. It does not mean the restriction is lossless.
An exact reformulation can be exact of an approximation, and the two statements
are logically independent because the restricted class is the starting point.

Unless stated otherwise, "exact" below means value exactness relative to the
fully adaptive problem.

## I.3 The reformulation that makes the question well posed

Substituting $y(\xi) = y_0 + Y\xi$ replaces $n_2$ adjustable variables by
$n_2(m+1)$ non-adjustable ones [MDH18, p. 2] and leaves a finite-dimensional LP
when $\Xi$ is a polytope [BGT04, Thm. 3.3, p. 360]. The adversary's problem, by
contrast, is a bilinear program over $\Xi \times \mathcal{W}$ and is NP-hard in
general [XB17, arlp line 379--384; BS18, DDBD line 360].

The parameter count is itself an object of study: in the production-inventory
class there always exists an optimal rule with $O(ET)$ non-zero parameters rather
than $O(ET^2)$ [LS22, `thm:main`, main_final line 661], which is why the affine
class is not automatically unattractive in high dimension.

So the affine rule is a *tractable inner approximation of an intractable exact
object*, and exactness asks when the approximation is tight. Xu and Burer make
the statement literal: the exact object is a copositive program over
$\mathrm{COP}(Q)$, and the affine rule is its restriction to the cone
$\mathrm{IA}(Q)$ of inverse-nonnegative matrices [XB17, arlp line 614--683].
The sandwich theorem,

$$
v_{\mathrm{AR}}^* \;\le\; v_{\mathrm{IB}}^* \;\le\; v_{\mathrm{AP}}^*
\tag{1.2}
$$

for every closed convex cone with
$\mathrm{IA}(Q) \subseteq \mathrm{IB}(Q) \subseteq \mathrm{COP}(Q)$
[XB17, `theorem:approximaterlp`, arlp line 783], is the conceptual core: any
improvement of the affine bound is a cone strictly between the two, and
exactness is membership of an optimal copositive multiplier in the affine face.

## I.4 What is established: the exact cases

The results rest on five logically distinct mechanisms. Separating them matters
because a proposed necessary-and-sufficient condition must say which one it
generalises, and no single mechanism accounts for all known exact cases.

**M1 — constraint-wise decomposition.** Partition $\xi = (\xi^1,\dots,\xi^m)$ so
that the $i$-th residual depends on $\xi^i$ only, and suppose
$\Xi = \Xi_1 \times \cdots \times \Xi_m$ with each factor nonempty, convex and
compact. Then static and fully adaptive problems coincide in value and in
feasible here-and-now decisions [BGT04, Thm. 2.1, p. 354]; the restatement in
[MDH18, p. 561] isolates what the condition buys. The mechanism is
decomposition, not geometry: $\Xi$ may be a box, a ball, or a polytope of any
shape and any number of vertices, as long as it factors.

**M2 — inverse-positive recourse with dominance.** Under fixed recourse and four
conditions on an optimal $x$ — (F) the second-stage objective is non-decreasing
in $y$; (A) technology matrix and right-hand side are affine in $\xi$;
(D) a dominance condition that lets the remaining constraints be dropped once a
chosen subset is satisfied; (B) an index set $I$ of exactly $n_2$ constraints
with $B_I$ invertible and $B_I^{-1} \ge 0$ such that
$A_I(\xi)x + B_I y \ge g_I(\xi)$ is equivalent on $\Xi$ to the full first
constraint set — the affine value equals the adaptive value [GTW25, Thm. 1,
p. 8]. The reading is transparent: the unique candidate
$y^{\ell}(\xi) = B_I^{-1}[\,g_I(\xi) - A_I(\xi)x\,]$ is affine, feasible and
pointwise minimal, hence optimal by monotonicity [GTW25, eq. (17), p. 42].
Condition (B) is checkable in practice: if each variable has a weakly dominant
constraint and those constraints' coefficient vectors form a partial order, then
$B_I$ is a Z-matrix similar to a strictly triangular matrix with unit diagonal,
hence an M-matrix [GTW25, p. 11]. No structure on the support is imposed, and
the support may be non-convex [GTW25, p. 6].

**M3 — conic restriction.** The sandwich (1.2) identifies the exact object and
the affine class as two rungs of one hierarchy; the intermediate rungs are the
usable approximations. An inverse-nonnegative relaxation reproduces the affine
value exactly [XB17, `theorem:affine-tractable`, arlp line 682], and a
second-order-cone rung closes the gap exactly on the temporal-network class
[XB17, arlp line 1045]. The price of the formulation is that copositive
membership is NP-hard and the numerical behaviour is typically strict: on 971
of 1000 multi-item-newsvendor instances the intermediate and affine bounds
coincide and both sit strictly above the lower bound, while on the remaining 29
the intermediate bound is strictly better [XB17, arlp line 1315--1318].

**M4 — polyhedral vertex structure and barycentric completion.** The starting
point is the elementary observation that a robust constraint depends on the
closed convex hull of the uncertainty set and on nothing finer [BN99, p. 3];
what changes in the two-stage setting is that the convexification must be
applied to the *policy graph* rather than to the uncertainty set. Ayoub and Poss
prove that for a polytope $\Xi$ and fixed recourse, replacing $\Xi$ by its
vertex set preserves the *fully adaptive* optimum
[AP16, Lemma 1, p. 5], and that the reduction fails as soon as the recourse
matrix depends on $\xi$: a two-point example is feasible at both endpoints and
infeasible at the midpoint [AP16, p. 6]. Georghiou, Tsoukalas and Wiesemann turn
the fact into a construction: write $\xi$ as a barycentric combination of
vertices and define the recourse decision as the same combination of vertex
decisions; feasibility transfers because the constraint map is affine and the
recourse matrix constant [GTW20, Prop. 1, p. 575]. Any rule whose graph lies in
the convex hull of the scenario policies is feasible with the same value
[GTW20, Prop. 4, p. 583], and the resulting rules are piecewise affine on a
simplicial decomposition, with the barycentric formula as closed form
[GTW20, Prop. 5, pp. 583--584].

Dai and Ho supply the geometric counterpart on the feasibility side. A
polyhedron is *simple* when every vertex is incident to exactly as many edges as
the ambient dimension. At a simple vertex every globally feasible recourse
system is locally linearly feasible [DH26, Thm. 2, p. 11]; for every non-simple
polyhedron there exist data that are globally feasible but not locally affine at
a vertex [DH26, Thm. 4, p. 23]. The authors are explicit that on a non-simple
support the condition is no longer automatic but may still hold [DH26, p. 24].

**M5 — a richer rule class.** Bertsimas and Georghiou build a class around the
fact that optimal decision rules in multistage adaptive optimization are
piecewise linear, and prove that every continuous piecewise linear function on a
compact set is representable in it [BG14, Thm. 1, p. 5]; the affine rule is the
one-piece case. Zhen, den Hertog and Sim obtain exactness for fixed-recourse ARO
by Fourier–Motzkin elimination, at the price of $O(M^{2^{N_2}})$ constraints
when eliminating $N_2$ variables [ZDS18, p. 8], with partial elimination giving a
monotone ladder of inner approximations [ZDS18, p. 9]. Their lot-sizing instance
has linear rules strictly suboptimal while elimination is exact [ZDS18, p. 9],
and a piecewise affine optimal rule exists with no assumption on $\Xi$
[ZDS18, Thm. 3, p. 11]. The polynomial line pushes the same idea into
semidefinite programming with exact sum-of-squares reformulations for separable
quadratic rules over boxes [CJW21b, Thm. 3.1, p. 7] and for separable polynomial
rules of degree $\ell$ [JLLLW22, Thm. 3.1, p. 6]. Zhang, Sun and Teo extend the pattern to adjustable robust quadratic programs
with a diagonal affine rule [ZST24, Thm. 3.1, p. 7]. Chen and Zhang enlarge the
affine class by splitting the uncertainty vector across affine pieces and prove
the enlarged feasible set equals the fully adaptive one [CZ09, Thm. 1, p. 4], at
the cost of a vertex count exponential in the number of constraints
[CZ09, p. 4].

## I.5 What is established: the negative side

Four families give explicit gaps. Three are unbounded in a dimension; one is a
single small instance.

| Family | Statement | Size of the gap | Anchor |
|---|---|---|---|
| Bertsimas–Goyal–Lu | static value equals adaptive iff $T(U,h)$ is convex for all $h>0$ | $\rho(U) \le m$, tight; family $U^\theta$ has $\kappa = n^{1/\theta}$ | [BGL15, pp. 11, 15, 17, 32] |
| Ben-Tal–El Housni–Goyal | simplex domination + threshold map gives $2\beta$-approximation | affine $\Omega(\sqrt{m})$ vs piecewise $O(1+1/\sqrt{m})$ on their instance | [BEG18, line 389; lines 661--690] |
| Haddad-Sisakht–Ryan | two constraints binding for different values of one parameter, each strictly improving when relaxed, imply adjustability lowers cost | certificate, not a characterisation; box uncertainty, fixed recourse only | [HSR18, Prop. 1, p. 7] |
| Chen–Zhang | split rule attains 1 where the plain affine rule attains $N$ | unbounded in $N$ | [CZ09, p. 6] |

Two cautions. The Bertsimas–Goyal–Lu characterisation is for the *static* class,
not the affine one, and the transformation argument does not transfer. The
Haddad-Sisakht–Ryan condition is sufficient only; its converse is false, since
three of their instances satisfy none of the published sufficient conditions for
static optimality and still have equal static and adaptive values
[HSR18, p. 18].

Hardness bounds what any theorem can deliver. With fixed recourse the adaptive
problem is NP-hard when $\Xi$ is a general polytope given by linear inequalities,
and also when $\Xi$ is a finite convex hull but the recourse matrix depends on
the scenario [BGT04, p. 355]; the proofs are in a thesis absent from the corpus,
which is a real gap in our evidence. With uncertain recourse even the affine
problem is NP-hard: its value is the maximum of a quadratic form over a simplex,
a copositivity check [BGT04, Example 3.1, p. 360]. Computing the worst case for a
fixed here-and-now decision is NP-hard [BS18, DDBD line 360], so even
certification is hard without structure. Choosing the minimal number of policies
that restores exactness is NP-complete, even with uncertainty only in the
objective [Kur25, Thm. 29, p. 20].

## I.6 The state of the art in one table

The table is organised by the question a reader usually asks: given my problem,
what can I compute, and what guarantee comes with it.

| Method | What it returns | Guarantee | Cost | Limits |
|---|---|---|---|---|
| Static rule | one $y$ | exact under constraint-wise uncertainty [BGT04 Thm. 2.1]; otherwise ratio $\le \rho(U) \le m$ [BGL15] | one LP | gap arbitrary in general [BGL15 p. 32] |
| Affine rule (ADR/LDR) | $y_0 + Y\xi$ | exact under (F),(A),(D),(B) [GTW25 Thm. 1]; box/static exact [BdR16 p. 12]; simplex/linear exact [ZDS18 p. 12] | one LP | $\Omega(\sqrt m)$ gap possible [BEG18]; 20–60 % observed [BG14 p. 28] |
| Copositive / IA hierarchy | nested bounds | exact at the copositive rung, affine at the IA rung [XB17 Thm 4.1] | copositive program (NP-hard) | no polynomial algorithm known |
| Piecewise affine / barycentric | piecewise rule on a partition | exact as a class for fixed recourse, affine data, constant $W$ [GTW20 Prop. 5] | partition-dependent; can be exponential | rule may leave the lifting hierarchy [GTW20, Example 2] |
| Fourier–Motzkin elimination | exact value | exact when all adjustable variables are eliminated [ZDS18 p. 9] | $O(M^{2^{N_2}})$ constraints [ZDS18 p. 8] | blow-up severe beyond small $N_2$ |
| Polynomial / SOS rules | SDP | exact reformulation of the *restricted* problem [CJW21b; JLLLW22] | SDP | reformulation exactness only; general non-affine NP-hard [CJW21a p. 13] |
| $K$-adaptability | $K$ candidate policies | exact for $K \ge n_\xi+1$ (objective uncertainty) [Kur25 Thm. 2]; $K \ge \min\{R(n_\xi+1),|Y|\}$ (constraint uncertainty) [Kur25 Thm. 11] | $K$-fold master | minimal $K$ NP-complete [Kur25 Thm. 29] |
| Column-and-constraint generation | optimal value | finite convergence under relatively complete recourse [BS18 §2; ZZ13] | MILP sequence | breaks down under mere feasibility [BS18] |
| Dual reformulation (nonlinear recourse) | exact dual, affine rules on the dual | equivalence between primal and dualized model [RZDH23, p. 4] | LP | primal recovery is one-sided: the primal LDR value can be lower than the dual value [RZDH23, p. 8] |

# Part II. Guaranteed control: the Dmitruk problem and its theory

Part I restricts the policy class and keeps the uncertainty abstract. The other
tradition reverses the emphasis: the uncertainty is a bounded disturbance acting
on a dynamical system over a finite horizon, the control is a *program* that may
be corrected when the state is measured, and the object is a guaranteed value
with a definite number of measurements. This part states that problem and its
general theory, because Part III's bridge is built on it.

## II.1 The problem

Consider the discrete linear system

$$
x(t+1) = A x(t) + B u(t) + M w(t), \qquad x(0) = x_0,
\tag{2.1}
$$

with control constraint $u(t) \in U$ (a box $u_{\min} \le u(t) \le u_{\max}$),
disturbance $w(t) \in W = \{w : \|w\|_\infty \le w_{\max}\}$, terminal set
$X_T = \{x : g_{\min} \le H x \le g_{\max}\}$, and worst-case linear criterion
$\max_w c^\top x(T)$ [A4, p. 68]. The symbols live in this problem only: $A$ is
the state matrix, $B$ the control matrix, $M$ the disturbance matrix, $T$ the
horizon, $x_0$ the initial state.

Two objects are distinguished from the start, and confusing them is the most
common error in reading this literature.

- The *guaranteeing program* is one control program $u(\cdot)$ chosen before any
  disturbance is known. Its value is written $J(x_0)$.
- A *closed* (or *feedback*) strategy measures the state at prescribed moments
  and recomputes the control. Its value is written $V_0(x_0)$.

The minimax inequality gives $V_0(x_0) \le J(x_0)$ [A4, (2.26); A2, p. 673]:
a strategy that may react cannot do worse than a program that may not. The gap
$J(x_0) - V_0(x_0)$ is the value of the information the closures provide.

The formulation with a single closure and the $\alpha$-level characterisation of the
closing set go back to the earlier work of the same school [A1; A2]. A set of
closure moments $T_1 < \cdots < T_N$ inside $\{1,\dots,T\}$ defines
segments $\Delta_j = \{T_j, \dots, T_{j+1}-1\}$ with $T_0 = 0$, $T_{N+1} = T$.
On $\Delta_j$ the control is one program; at $T_{j+1}$ the realised state is
measured and the next program is chosen. The schedule is an input throughout
this literature: A2 and A3 fix the closing instant in advance
[A2, p. 667; A3, p. 41], A4 fixes the moments before the process starts
[A4, p. 69], and A5 states outright that the optimal placement of closure
moments is not investigated [A5, p. 75].

## II.2 The exact theory: closing sets as polyhedra

Write $V_j(x_j)$ for the guaranteed value from level $j$ at state $x_j$. The
backward recursion

$$
V_j(x_j) = \min_{u_j}\ \max_{w_j}\ V_{j+1}\big(x(T_{j+1}\mid x_j, u_j, w_j)\big),
\qquad j = N-1,\dots,0,
\tag{2.2}
$$

is Dmitruk's analogue of the Bellman equation [A4, (2.8), p. 72]. Two
structural facts make it computable.

**Closing sets are polyhedra.** The level sets
$X_j(\alpha) = \{x \in X_j : V_j(x) \le \alpha\}$ are convex polyhedra and
$V_j$ is piecewise-linear convex, as the optimal value of an LP
[A4, (2.9), p. 72; A3, p. 42]. Their interpretation is the key to everything
downstream: $X_j(\alpha)$ is the set of states from which the remaining
guarantee is at most $\alpha$. The nesting
$X_j(\alpha_{\min}) \subseteq X_j(\bar\alpha) \subseteq X_j$ is monotone in
$\alpha$.

**The representation is affine in the parameter.** Under the first part of
Assumption 2.2, for every $j$ the closing level set is

$$
X_j(\alpha) = \{\, x \in \mathbb{R}^n : P_j x \le g_j + \lambda_j \alpha \,\},
\qquad \alpha \in \mathbb{R},
\tag{2.3}
$$

with $P_j = Y_j G_j$, $\lambda_j = Y_j \lambda_{j+1} \ge 0$ and
$g_j = Y_j(g_{j+1} - \gamma_j) - \sum_t P_j D_j(t) u_{\min}
+ \sum_t V_j(t)(u_{\max} - u_{\min})$, where the rows of $Y_j, V_j(t)$ form a
fundamental system of solutions of the cone
$(G_j D_j(t))^\top y_j + v_j(t) \ge 0$, $y_j \ge 0$, $v_j(t) \ge 0$
[A5, Thm. 2.2, p. 55]. The matrices $P_j$ do not depend on $\alpha$; only the
right-hand side does, and linearly. That single fact is what turns an
infinite family of polyhedra into one parametric object.

Because the matrices are $\alpha$-free, the whole strategy collapses to one LP
per closure. At each level,

$$
V_j(x_j) = \min_{u_j,\alpha}\ \alpha
\quad\text{s.t.}\quad
\sum_{t \in \Delta_j} G_j D_j(t)\, u_j(t) - \lambda_{j+1}\alpha
\le g_{j+1} - \gamma_j - G_j x_j,
\tag{2.4}
$$

with $G_j = P_{j+1} A^{T_{j+1} - T_j}$ and the worst-case row estimates
$\gamma_{ji} = w_{\max} \sum_{t\in\Delta_j} \| p_{j+1,i}^\top A^{T_{j+1}-t-1} M \|_1$
[A5, Thm. 2.1, p. 53]. The optimal value is $V_0(x_0) = \alpha^0$. With the
$j = 0$ program solved and later levels solved at realised states, the online
cost is one LP per closure [A5, Thm. 2.3, p. 59].

**Trajectory monotonicity.** Under Assumption 2.2, along any process realised
under the optimal strategy,
$V_0(x_0) \ge V_1(x^*(T_1)) \ge \cdots \ge V_N(x^*(T_N))$
[A5, Thm. 2.3, p. 59]. The guarantee never deteriorates as measurements arrive.
This is the dynamical counterpart of the information monotonicity that Part III
states abstractly.

**Computing the representation.** In the one-closure case the support functions
$f_j(\alpha) = \max\{p_j^\top x_1 : x_1 \in X_1(\alpha)\}$ are affine,
$f_j(\alpha) = f_{0j} + \lambda_j\alpha$ with $\lambda_j \ge 0$, under the rank
condition $\operatorname{rank}(G_1^\top \mid c_1) = \operatorname{rank}(G_1^\top
\mid c_1 \mid p_j) = m+1$ [A3, p. 43]. When the rank condition fails the support
is piecewise affine concave on $[\alpha_{\min}, \alpha_{\max}]$, and A3 points at
the lifted set $\Xi_1(\alpha) \subseteq \mathbb{R}^{m+1}$ as the way out
[A3, pp. 44--45]. In the multi-closure case the support values are
piecewise-linear convex in $\alpha$, with explicit breakpoints obtained by
parametric-LP basis tracing: on an interval of constant basis
$df(\alpha)/d\alpha \equiv \lambda^\top y^0(\alpha)$ and
$f(\alpha) = f(\bar\alpha) + \lambda^\top y^0(\alpha)(\alpha - \bar\alpha)$
[A5, Lemma 2.5, p. 65].

## II.3 What the Dmitruk theory gives, and what it costs

**Approximating closing sets keep the affine form.** Given unit normals
$\bar p_{ji}$ satisfying dual feasibility, the outer approximations
$\bar X_j(\alpha)$ admit the same representation
$\bar X_j(\alpha) = \{x : \bar P_j x \le \bar g_j + \bar\lambda_j \alpha\}$ on
$[\bar\alpha_{j,\min}, \alpha_{\max}]$, with each row repeated as many times as
the piecewise-linear support has pieces [A5, Thm. 2.4, p. 69]. The practical
recipe is to take the previous level's rows $\bar p_{j+1,i} A^{T_{j+1}-T_j}$
plus quasi-random directions.

**The certificate is a posteriori and two-sided.** With outer approximations the
computed value satisfies $\bar V_0(x_0) \le V_0(x_0)$, and if the actual
guaranteed cost of the computed strategy is
$\bar\alpha = \max_{w\in W} V_{N+1}(x(T \mid 0, x_0, \bar\pi_N, w)) < \infty$,
then $\bar V_0(x_0) \le V_0(x_0) \le \bar\alpha$ and the online LPs remain
solvable at every realised state [A5, Statement 2.1, p. 73]. If
$\bar\alpha = \infty$ the fallback is to rebuild with an inflated disturbance set
$W_\delta$ [A5, p. 73]. Accuracy is therefore certified per instance, not
globally; this is stated as such in A4 as well [A4, p. 73].

**The hard side is the adversary.** Computing $\bar\alpha$ is maximisation of a
convex function over a polytope, nonconvex, in dimension $Tp$; the dimension is
cut by accumulating effective disturbances per segment,
$\xi_j = \sum_{t\in\Delta_{j-1}} A^{T_j-t-1} M w(t)$, and approximating their
reachable sets [A5, p. 73]. The minimisation side is a polynomial LP. The
asymmetry is structural: the controller's problem is convex, the adversary's is
not.

**Adding a closure has a computable lower bound on its gain.** Comparing the
optimal $N$-closure strategy with the optimal $(N-1)$-closure strategy obtained
by gluing the first program to the shorter strategy gives
$V_0(x_0\mid \pi_N^0) \le V_0(x_0\mid \pi_N) \le V_0(x_0\mid \pi_{N-1}^0)$, hence
$V_0(x_0\mid\pi^0_{N-1}) - V_0(x_0\mid\pi^0_N) \ge \delta_{\min}$ with
$\delta_{\min}$ computable [A5, §2.2.8, p. 75]. The same argument covers the
degenerate case of no closures, which is the guaranteeing program
[A4, (2.26), p. 72].

**The cost profile.** The exact scheme's cost concentrates in building the
fundamental system of the cone $(G_jD_j(t))^\top y_j + v_j(t) \ge 0$ at each
level, which is the curse of dimensionality and can be untenable already at
$N > 1$; the approximating track computes all closure sets offline for all
$\alpha$ at once, so that online only one LP per closure is solved
[A5, p. 59]. This is the stated contrast with the iterative approach of the
Gabasov school, which recomputes approximations during the process
[A5, p. 59].

## II.4 What remains open in that theory

The school itself names the gap. Improvement is possible both by the *number* and
by the *position* of closure moments, and after the one-closure bounds the
dissertation states that the question of the optimal position is not
investigated [A5, p. 75]. A2 declares scheduling and multi-closure open
[A2, p. 681]. The choice of the schedule can even decide existence of a solution
in the strategy class, not merely its quality [A5, p. 54].

Three further items are absent from the theory as presented.

- The value is *not* monotone in a single closure moment: it has an interior
  peak in the examples [A4, p. 78; A2, pp. 679--680]. So "more information is
  better" and "an earlier closure is better" are both false as statements about
  position, even though the value is monotone in the *set* of closures.
- The ladder OC → $N$-closures → DP is articulated qualitatively on one page
  [A5, p. 39] and appears as the two-step inequality
  $V_0(x_0) \le J(x_0)$. The refinement-monotonicity statement is informal
  [A5, p. 75].
- The joint $(x,\alpha)$ epigraph representation is attempted in a working note
  and reported as a failure: in the worked example it yields only three normals
  and otherwise the underlying problem is unbounded [A5, Note 2.10, p. 75].
  That note is the closest the school comes to the object Part III uses.

# Part III. The bridge, in detail

This part connects the two. The connection is not an analogy: a specific class of
the guaranteed-control problem is a specific class of the two-stage problem with
fixed recourse, right-hand-side uncertainty, and a policy class determined by the
closure set. The rest of the part does the mathematics of that class and states
what is verified.

## III.1 The dictionary

Take the Dmitruk model (2.1) with $A = I$, a two-row state, scalar control,
$B = (1,1)^\top$, $M = E = (e_1,e_2)^\top$, initial state $x_0 = (d_0,d_0)$,
box control $|u_t| \le u_b$, disturbance $w_t \in \{-1,+1\}$, terminal cost
$\|x_T\|_1$, and a closure set $R \subseteq \{1,\dots,T\}$. Call this the
*bridge class* $\mathcal{B}(T,d_0,e,u_b)$.

| Dmitruk object | Two-stage ARO object | Why they coincide |
|---|---|---|
| control program on $\Delta_j$ | recourse policy $y(\cdot)$ | both are maps from information to action |
| closure set $R$ | information structure of the policy | policy at $t$ knows $w_1..w_r$, $r=\max\{c\in R: c\le t-1\}$ |
| disturbance path $w \in W$ | scenario $\xi \in \Xi$ | $\Xi = \{-1,+1\}^T$ here |
| guaranteeing program value $J(x_0)$ | static-rule value $V_{\mathrm{st}}$ | no measurements, one program |
| multiclosure value $V_0(x_0)$ | $V(R)$, the $R$-informed value | same minimax, different letters |
| feedback/DP value | $V_{\mathrm{AR}}$ with full information | $R = \{1,\dots,T\}$ |

The last row is the one worth pausing on. In Part I the fully adaptive value is
an intractable object that one restricts; here it is attained by a dynamic
program because the horizon is finite and the state is small. The bridge class
is therefore a rare object: an instance of the intractable side that is exactly
solvable, which is what makes it useful as a test case for general theory.

## III.2 The rotation

Write $x_t = (x_{1t}, x_{2t})$ and rotate:

$$
s_t = x_{1t} + x_{2t}, \qquad d_t = x_{1t} - x_{2t}.
\tag{3.1}
$$

For any pair, $\|(a,b)\|_1 = \max(|a+b|, |a-b|)$. The identity is Lean-verified
with no `sorry` (P1 below), and it is the only piece of the apparatus that needs
no hypothesis. The dynamics separate:

$$
s_T = 2d_0 + 2U + S\,W, \qquad d_T = D\,W, \qquad
U = \sum_{t=1}^{T} u_t, \quad W = \sum_{t=1}^{T} w_t,
\tag{3.2}
$$

with $S = e_1 + e_2$ and $D = e_1 - e_2$. The control enters only the sum
coordinate, because $B = (1,1)^\top$ acts identically on both rows and cancels in
the difference; the disturbance enters both. Consequently the difference
coordinate is uncontrollable, $|d_T| = |D|\,|W|$, and since $|W| \le T$ with
equality on the all-plus or all-minus path, the term $|D|\,T$ is a floor under
every value in the class, at every level of information.

This is the point where a subtlety enters, and this version of the essay reports
it rather than hiding it. It is tempting to conclude
$V(R) = \max(\text{sum part}, |D|T)$, because the sum part is controlled and the
difference part is not. That decomposition is valid only when the same
disturbance path maximises both terms, or when one term dominates on every path.
The adversary chooses *one* path, and the objective is
$\max_w \max(|s_T(w)|, |D\,W(w)|)$, not
$\max(\max_w |s_T(w)|, \max_w |D\,W(w)|)$. Section III.6 records what checking
this changed.

## III.3 The ends of the ladder

Two extreme information structures have closed forms, and both are checked
against exact rational LPs on frozen grids.

**No closure ($R=\varnothing$).** The control is one program chosen blind. The
sum part pays a triangle for the initial offset,

$$
V(\varnothing)^{\text{sum}} = |S|\,T + \max\big(2|d_0| - 2u_b T,\ 0\big),
\tag{3.3}
$$

because the adversary can add $|S|$ per step and the controller can remove $2u_b$
per step, and only the residual offset has to be chased.

**Full information ($R=\{1,\dots,T\}$).** The control reacts to the whole
observed prefix, and the sum part follows the pursuit iteration

$$
f_1(x) = \max(x - 2u_b,\, 0) + |S|, \qquad
V(\{1,\dots,T\})^{\text{sum}} = f_1^{T}\big(2|d_0|\big).
\tag{3.4}
$$

The two forms differ exactly inside the wedge

$$
\mathcal{K} = \big\{\, |S| > 2u_b,\ \ 2|d_0| < 2u_b,\ \ T \ge 2 \,\big\},
\tag{3.5}
$$

drawn in Figure 2. Outside $\mathcal{K}$ the pursuit iteration collapses to the
linear expression $\max(|S|, 2|d_0| - (2u_b - |S|)T)$; inside it, it does not.
The linear expression was derived inside this project, not taken from a
publication, and it understates the guarantee inside $\mathcal{K}$; the
correction is (3.4).

![The wedge. Horizontal axis is $|S|$ in units of $2u_b$, vertical axis the
initial offset in the same units. To the left of the vertical line the linear
expression is exact; inside the shaded rectangle the pursuit iteration is
strictly larger.](figs/fig2_wedge.pdf){width=62%}

## III.4 The ladder in between, and why the schedule matters

For an intermediate closure set $R$ the value is neither end. The natural
question — which schedules are good — has two parts, and they behave
differently.

**At fixed cardinality, position matters.** Figure 3 plots, for every $k$, the
best and worst value over all schedules of size $k$ at $T=5$, computed by the
exact per-path LP oracle. The spread at $k=1$ is 7 to 10, at $k=3$ it is 6 to 8:
knowing *how many* measurements you can afford does not determine what they are
worth. This is the quantitative form of the school's statement that position
matters [A4, p. 78].

![Value against the number of closures. The band is the range over all
schedules of that size; the solid line is the best schedule, the dashed line the
worst. Exact rational LP, $T=5$, $e=(3/2,1/2)$, $u_b=1$, $d_0=0$.](figs/fig4_ladder.pdf){width=66%}

**At fixed cardinality, one closure has a valley.** With a single closure at
$r$ the value as a function of $r$ is V-shaped in the examples: closing too early
leaves too much disturbance ahead, closing too late leaves too much initial
offset unaddressed. Figure 4 shows the exact LP values and the closed form that
the project's S2 statement proposes for this case, side by side for the symmetric
and asymmetric row regimes. They agree when $D = 0$ and on classes where the
difference floor dominates, and disagree otherwise; §III.6 says what that
means.

![One closure, two row regimes. Left: $e=(1,1)$, so $D=0$ and the S2 closed form
matches the exact LP at every admissible moment. Right: $e=(3/2,1/2)$, so $D=1$;
the closed form falls below the exact value at three of the four moments. This is
the domain boundary reported in §III.6, drawn from exact rational LP values at
$T=5$, $u_b=1$, $d_0=0$.](figs/fig3_valley.pdf){width=92%}

**The quantifier order separates the two traditions.** Figure 5 draws the
difference between the multiclosure value and the guaranteeing-program value as a
difference in the order of quantifiers: the strategy alternates
$\min,\max,\min,\max,\dots$, one round per segment, while the program minimises
once and then faces every adversary choice at once. The inequality
$V_0 \le J$ is the only general statement the school records about that
difference [A4, (2.26); A5, p. 39], and Part III's contribution to it is a closed
form in one class, reported below.

![Quantifier structure. Above: the alternating minimax of the multiclosure
strategy. Below: one minimisation followed by all adversary choices, which is the
guaranteeing program. The arrow is the minimax inequality.](figs/fig5_quantifier.pdf){width=78%}

## III.5 The block composition, and the tail-sum reduction

The project's central conjecture for this class is that a schedule's value is
obtained by folding a one-block map along the blind blocks. Let
$L_0,\dots,L_k$ be the consecutive differences of $[0] \cup \operatorname{sorted}(R)
\cup [T]$, so that $\sum_j L_j = T$; $L_j$ is the length of the $j$-th interval
during which the control is blind. The proposed law is

$$
V(R) \;=\; \max\Big(|D|T,\;\; 2|d_0| + (|S|-2u_b)T,\;\;
\max_{0\le j\le k}\big[\,|S|\,L_j + (|S|-2u_b)(L_{j+1}+\cdots+L_k)\,\big]\Big).
\tag{3.6}
$$

Read it as follows. The first two terms are the floor and the blind-regime value;
the bracket says that the worst block is the one with the longest *tail* behind
it, because disturbance accumulated before the last closure cannot be corrected.
For a single closure at $r$ this specialises to
$V(\{r\}) = \max(c, g(r))$ with $c = \max(2|d_0| + (|S|-2u_b)T, |D|T)$ and
$g(r) = \max(|S|(T-r), |S|T - 2u_b(T-r))$, whose graph is the valley of
Figure 3.

The reduction's value is that it turns schedule design into a finite
combinatorial problem with a known objective: minimise a maximum of $k+1$
linear forms over compositions of $T$ into $k+1$ parts. That is a bottleneck
partition, and unlike the policy-count question of Part I it has no complexity
classification in the literature.

**Status, stated precisely.** The fold and the tail sum were certified on frozen
grids with exact rational arithmetic: 137 per-path LP points and 5952 DP
comparisons for the fold, 596 LP points, 54 reductions and 3348 DP cross-checks
for the tail sum. They are not theorems, and — this is the part this version
adds — the certification does not extend to the whole class. See §III.6.

## III.6 What checking this version changed

While producing the figures for this version, the closed forms were checked
against the exact per-path LP oracle on classes other than the ones on which they
were certified. Three facts emerged, and all three are reported here because
they bound what the bridge theory currently claims.

**Fact 1. The fold formula is not valid on the whole class.** Take
$T=5$, $u_b=1$, $d_0=0$, $S=3$, $D=1$. For the single closure at $r=1$ the exact
LP gives 13; formula (3.6) gives 12. The discrepancy appears for every $D \neq 0$
tested where the difference floor does not dominate the sum part, and it is
absent when $D = 0$ or when the floor dominates. The mechanism is the one
identified in §III.2: the formula treats the two coordinates separately, while
the adversary picks one path for both.

**Fact 2. The certificates were on a narrower class than the statement
suggests.** The grids on which the fold and the tail sum were certified lie in
the symmetric row regime and in regimes where the floor dominates. The statement
in the project's own status file is phrased for general $e$, which the grid does
not cover. The correct phrasing is the narrower one.

**Fact 3. The wedge law is unaffected.** The wedge (3.5) concerns the *full
information* end, where the value is computed by the pursuit iteration whether
or not the floor dominates; it was certified on a grid that straddles the wedge
boundary in both coordinates. Figure 2 draws it.

What this means for the essay is unflattering and useful: the bridge class
supplies a genuine test case for Part I's theory, but its own closed form is
established on a sub-class, and the general statement is open. The open problem
O2 below is therefore sharper than it looked in the previous version: it is not
only that no exact gap formula exists in the literature, but that the one this
project proposed has a known domain boundary that no theorem yet explains.

## III.7 The bridge as a test case for Part I

Three properties make the class useful to a reader of Part I, independently of
whether the closed forms hold everywhere.

**It is affine-exact, and no mechanism certifies it.** In the full-information
case the affine rule over the observed prefix attains the adaptive optimum
(certified on 576 exact LP points, zero gap). The class defeats M1 (the
constraint system is not constraint-wise), M2 (the recourse matrix has entries of
both signs, so no inverse-positive basis is available), and — for the *affine*
rule — M4, which applies but delivers a piecewise affine rule. M3 addresses the
class directly but gives no transparent certificate, and M5 can always be made
trivial by enlarging the class. So the class is a positive instance that no
sufficient condition in Part I covers.

**It separates two gaps.** Inside the wedge the affine-versus-adaptive gap is
zero while the *formula-versus-truth* gap is positive. An exactness result about
a rule class therefore does not protect against a wrong closed form for the
value: these are two different objects requiring two different instruments.

**It makes the schedule a finite decision problem.** Formula (3.6) — on the
domain where it holds — gives the value of every schedule in closed form, so the
optimisation over schedules is a finite combinatorial problem with a known
objective. That is exactly what the Dmitruk theory lacks and what Part I's
$K$-adaptability literature counts instead of measuring.

# Part IV. Open problems

Each is stated so that a theorem, a counterexample, or a complexity result could
settle it.

## O1. A necessary-and-sufficient condition for affine value exactness

*Statement.* Characterise, in terms of $(A(\cdot), h(\cdot), B, \Xi)$, when
$V_{\mathrm{AP}} = V_{\mathrm{AR}}$ under fixed recourse and right-hand-side
uncertainty.

*Known.* Sufficient: constraint-wise uncertainty [BGT04, Thm. 2.1];
inverse-positive recourse with dominance [GTW25, Thm. 1]; simplex uncertainty for
linear rules [ZDS18, p. 12]; box uncertainty for static rules [BdR16, p. 12].
Exact conic duals give reformulation exactness for adjoint systems [CJ20, p. 3]
and for SOS-convex data [CJW21a, p. 4]. Exact reformulation of the question: cone
membership [XB17, `theorem:approximaterlp`, arlp line 783].

*Missing.* Any necessary condition. Two published statements of non-necessity
exist, both about sufficient conditions rather than a characterisation
[GTW25, Prop. 1; HSR18, p. 18]. The cone characterisation is exact but not
polynomially decidable, and has not been specialised to checkable data
conditions.

## O2. An exact formula, or a sharp rate, for the affine gap

*Statement.* For fixed recourse and RHS uncertainty, determine
$\sup_{\Xi} V_{\mathrm{AP}}/V_{\mathrm{AR}}$ as a function of the geometry of
$\Xi$ and the structure of $B$.

*Known.* Static case: exact characterisation and tight factor $\rho(U) \le m$
[BGL15]. Affine case: $O(\sqrt m)$ under domination with a matching instance
[BEG18], and an $O(\sqrt k)$ worst case for linear rules [BG14, p. 2].
Empirically 20–60 per cent [BG14, p. 28]. In the bridge class the gap is zero in
the full-information case and the closed forms cover a sub-class only (§III.6).

*Missing.* Everything between the bounds and the instances, and — newly — an
explanation of the domain boundary found in §III.6.

## O3. The role of vertex count and vertex incidence

*Statement.* Determine the exact relationship between the combinatorial
structure of $\operatorname{vert}(\Xi)$ and affine exactness.

*Known.* With $m$ extreme points linear policies are optimal [BdR16, p. 6,
citing Bertsimas and Goyal 2012], tight when all are included [BdR16, p. 7].
Simplicity makes local linear feasibility automatic [DH26, Thm. 2]; non-simple
supports admit counterexamples [DH26, Thm. 4]; vertex representation alone is
insufficient [BGL15, p. 32; AP16, p. 6].

*Missing.* A combinatorial statement that is necessary and sufficient. The
Dai–Ho dichotomy is the closest, and it concerns feasibility rather than value.

## O4. The information structure as a decision variable

*Statement.* Given a family of admissible schedules, determine the complexity of
choosing a schedule of minimum cardinality that attains the full-information
value, and characterise when it exists.

*Known.* The number of $K$-adaptable policies needed for exactness is
$n_\xi+1$ under objective uncertainty [Kur25, Thm. 2, p. 5] and
$\min\{R(n_\xi+1),|Y|\}$ under constraint uncertainty [Kur25, Thm. 11, p. 10];
minimal $K$ is NP-complete [Kur25, Thm. 29]. In the Dmitruk line the schedule is
an input: fixed in A2, A3, A4 [A2, p. 667; A3, p. 41; A4, p. 69], declared out of
scope in A5 [A5, p. 75]. The value is non-monotone in the position of a single
closure [A4, p. 78].

*Missing.* Any complexity result for schedules, as opposed to policy counts. A
schedule determines the information available at each decision; $K$ counts
policies committed in advance. No paper in the corpus relates the two. The bridge
class makes it concrete: on the sub-class where (3.6) holds, the objective of
every schedule is closed-form and the optimisation is finite combinatorial.

## O5. Necessary conditions for a strict gap

*Statement.* Give checkable conditions on $(A,h,B,\Xi)$ implying
$V_{\mathrm{AP}} > V_{\mathrm{AR}}$.

*Known.* One checkable sufficient condition, box uncertainty and fixed recourse,
via two binding constraints at different values of a shared parameter
[HSR18, Prop. 1]. Explicit witnesses [CZ09, p. 6; GTW25, p. 45]. Vertex reduction
fails under random recourse [AP16, p. 6]. A defect of the same kind inside the
bridge class is recorded in §III.6.

*Missing.* Generality: no condition covers a general polytope, and none is proved
necessary. Necessary conditions for a gap are the contrapositive of sufficient
conditions for exactness, so O5 is the negative face of O1.

## O6. A price of adaptivity

*Statement.* Define and compute a quantity, analogous to the price of anarchy,
measuring the worst-case ratio between the adaptive optimum and the best static
solution as a function of the data.

*Known.* Characterised exactly for the static class [BGL15, Thm. 3.2], bounded by
$\rho(U) \le m$. For the affine class only bounds exist. The term is not used in
this sense in the corpus; a scan found it only in adjacent literatures, and that
lead is unverified.

*Missing.* A definition stable across classes, and any exact computation. The
natural ratio is unbounded when the adaptive value is zero, so a normalisation is
required; the bridge class is a clean testbed because both ends of the ladder are
known there.

## O7. A bridge theorem between guaranteeing-program control and two-stage ARO

*Statement.* Establish an equivalence, or a sharp two-sided bound, between the
guaranteed value of a terminal control problem with scheduled closures and the
value of a two-stage adaptive robust program with correspondingly structured
uncertainty.

*Known.* The ladder $OC \ge RO(k) \ge DP$ is formalised as monotonicity in the
project's Lean core (P2). The school articulates it qualitatively [A5, p. 39] and
computes exact values for fixed schedules [A4; A5, Thm. 2.1]. A5's Theorem 2.2
gives the exact parametric representation of closing sets, and Lemma 2.5 the
piecewise-linear supports. The rotation (3.1)–(3.2) maps the bridge class to two
scalars, and the value has the same max-of-two-terms shape as the robust bounds.

*Missing.* A statement of both sides in one formalism with a proof. No paper in
the corpus we have read does this. The domain boundary of §III.6 is evidence that
the two-sided statement is not superficial: the naive decomposition of the
difference floor fails, and the correct one must respect the path coupling.

## O8. The quantifier-order gap

*Statement.* Quantify the difference between $\min\max$ and $\max\min$ in the
two-stage problem and determine when it vanishes.

*Known.* Dmitruk records that the max-min form may be easier than the min-max
form [A4], and the school has the one-step inequality $V_0 \le J$ [A4, (2.26)].
In the bridge class the path-committed max-min value has a closed form and
$V(R) \ge V_{\mathrm{mm}}$ for every $R$ (certified, 47 instances, 518 oracle
points), with an explicit gap in the pure regime.

*Missing.* A general inequality, and a characterisation of the classes where the
gap is zero. The max-min value is a relaxation obtained by reversing the order of
choice, so the gap measures the value of commitment; the information-design
literature has vocabulary for this and the robust literature does not.

# A falsification battery for exactness conditions

Any proposed necessary-and-sufficient condition must classify the following seven
instances correctly. The value of the battery is asymmetric: passing it does not
confirm a condition, failing one instance refutes it.

| # | Instance | Required verdict | Anchor |
|---|---|---|---|
| T1 | Bridge class, full information | exact: affine attains adaptive | verified, §III.7 |
| T2 | SOC temporal network | not exact in general (gap unbounded) | [XB17, arlp line 1045] |
| T3 | Chen–Zhang $N$-vs-1 | not exact for affine, exact for extended | [CZ09, p. 6] |
| T4 | GTW (B)-violating instance | not exact ($3/2$ vs $5/4$) | [GTW25, p. 45] |
| T5 | BEG separating instance | not exact for affine ($\Omega(\sqrt m)$) | [BEG18, lines 661--690] |
| T6 | Box uncertainty, static | exact | [BdR16, p. 12] |
| T7 | Simplex uncertainty | exact for linear rules | [ZDS18, p. 12] |

T1 discriminates, because the other six can be passed by conditions keying on
$\Xi$ alone while T1 has $\Xi$ equal to the vertex set of a cube, non-simple for
$T \ge 2$, and a recourse matrix with both signs. A condition certifying
*affine* exactness there must use the interaction of dynamics and cost. T2 guards
against triviality: a condition that certifies every fixed-recourse problem looks
strong until it must separate the temporal-network family. T4 is the
anti-necessity probe: the instance violates all four conditions of the strongest
exactness theorem in the corpus and is exact, so a claimed characterisation must
accept it.

# What this essay does not cover

**Unverified recent literature.** A scan of 2023–2026 work produced leads on
affine optimality beyond simplex uncertainty, on a posteriori exactness tests
from dual extreme points, on complexity classifications of static, two-stage and
$K$-adaptable robust optimization, and on the value of coupling uncertainty sets.
None is cited as established. Two would bear directly on O1 if confirmed.

**The Electronic Companion of Zeng and Zhao.** Three propositions are stated
without proof there; the proofs are in a companion not in the corpus [ZZ13].
Column-and-constraint statements here are therefore statement-level only.

**Random recourse.** Except where noted the essay stays inside fixed recourse.
With random recourse the affine problem can be NP-hard [BGT04, Ex. 3.1] and the
vertex reduction fails [AP16, p. 6].

**Algorithms and numerics.** Cutting planes, Benders, C&CG and solver
engineering appear only where a theorem depends on them. The certified-pipeline
question — how to carry an error budget through a decomposition without losing
the certificate — is a methods problem, treated in [TSC22, Prop. 2, p. 7].

Two developments would change the picture. A proof of O1 in the cone-membership
language would turn a collection of sufficient conditions into a decision
procedure, even an exponential one. A complexity result for O4 would connect the
two literatures on the one axis where they are currently disjoint: neither
treats the information structure as the object to be optimised.

# Appendix A. Symbols, and the problem each belongs to

| Symbol | Meaning | Lives in |
|---|---|---|
| $x$, $X$ | here-and-now decision, its feasible set | Part I, (1.1) |
| $y$, $y(\cdot)$ | recourse decision, recourse policy | Part I, (1.1) |
| $c$, $d$ | first-stage and second-stage cost vectors | Part I, (1.1) |
| $A(\xi)$, $h(\xi)$ | technology matrix and right-hand side | Part I, (1.1) |
| $B$ | recourse matrix (constant under fixed recourse) | Part I, (1.1) |
| $\xi$, $\Xi$ | uncertain parameter, uncertainty set | Part I, (1.1) |
| $V_{\mathrm{AR}}$, $V_{\mathrm{AP}}$, $V_{\mathrm{st}}$, $V_K$ | adaptive, affine, static, $K$-adaptable values | Part I, §I.1 |
| $\mathcal{W}$ | dual feasible set $\{w\ge0: B^\top w=d\}$ | Part I, §I.3 |
| $\mathrm{IA}(Q)$, $\mathrm{COP}(Q)$, $\mathrm{IB}(Q)$ | inverse-nonnegative, copositive, in-between cones | Part I, §I.3 |
| $A$, $B$, $M$ | state, control, disturbance matrices | Part II, (2.1) |
| $u(t)$, $U$ | control, control constraint set | Part II, (2.1) |
| $w(t)$, $W$, $w_{\max}$ | disturbance, its set, its bound | Part II, (2.1) |
| $x_0$, $x(t)$, $T$ | initial state, state, horizon | Part II, (2.1) |
| $T_1<\dots<T_N$ | closure moments | Part II, §II.1 |
| $\Delta_j$ | $j$-th segment between closures | Part II, §II.1 |
| $J(x_0)$ | guaranteeing-program value | Part II, §II.1 |
| $V_j(x_j)$, $V_0(x_0)$ | guaranteed value from level $j$; multiclosure value | Part II, (2.2) |
| $X_j(\alpha)$ | closing level set at level $j$ | Part II, §II.2 |
| $P_j$, $g_j$, $\lambda_j$ | $\alpha$-free matrices, vector, parameter of $X_j(\alpha)$ | Part II, (2.3) |
| $\gamma_{ji}$ | worst-case row estimate | Part II, (2.4) |
| $R$ | closure set (schedule) in the bridge class | Part III, §III.1 |
| $s_t$, $d_t$ | sum and difference coordinates | Part III, (3.1) |
| $S$, $D$ | $e_1+e_2$ and $e_1-e_2$ | Part III, (3.2) |
| $U$, $W$ | accumulated control and accumulated disturbance | Part III, (3.2) |
| $u_b$, $d_0$, $e$ | control bound, initial offset, row amplitudes | Part III, §III.1 |
| $L_j$ | blind-block lengths | Part III, §III.5 |
| $\mathcal{K}$ | the wedge (3.5) | Part III, §III.3 |
| $f_1$ | pursuit map $x \mapsto \max(x-2u_b,0)+|S|$ | Part III, (3.4) |

# Appendix B. Verification ledger

| Item | Status | Evidence |
|---|---|---|
| Rotation $\|(a,b)\|_1 = \max(\|a+b\|,\|a-b\|)$ | Lean, no `sorry` | P1, `Aroform.lean` |
| Information monotonicity $R_1\subseteq R_2 \Rightarrow V(R_1)\ge V(R_2)$ | Lean, axiom-gated | P2, `Aroform.lean` |
| One-dimensional affine exactness | Lean, axiom-gated | P3, `Aroform.lean` |
| Blind-block lower half | Lean, no `sorry`, transfer pending | P4, `TwoDDraft.lean` |
| Upper half via centering | Lean, no `sorry` | P5, `TwoDDraft.lean` |
| Wedge law (3.5) | certified, 864/864 + 576-point regression | `artifacts/judge/wedge.txt` |
| Full-information affine exactness (T1) | certified, 576 exact LP points, zero gap | `artifacts/judge/attack_h-auto-3.txt` |
| Max-min floor | certified, 47 instances, 518 oracle points | `artifacts/judge/attack_h-auto-6.txt` |
| One-closure valley law (symmetric class) | certified on its grid; fails outside (§III.6) | `attack_h-auto-5.txt`, `h-sched-argmin-3.yaml` |
| Block fold and tail sum | certified on their grid; fails outside (§III.6) | `attack_h-auto-1.txt`, `attack_h-auto-8.txt` |
| All literature claims | anchored to page or line | reference list below |

# References

Entries give the corpus file and the page convention used above. DOI links were
verified against Crossref where a link appears; no link means the identifier was
not verified, not that the work is unpublished.

**[A1]** Balashevich, N. V. (2004). Guaranteed program control. `corpus/our_papers/A1_Балашевич_2004.pdf`. Cited for the school's prehistory; the schedule is an input.

**[A2]** Dmitruk, N. M. (2018). One-closure guaranteed control. `corpus/our_papers/A2_Дмитрук_2018.pdf`. Cited for the one-closure formulation (p. 667), the one-LP reduction (p. 672), the program-versus-strategy inequality (p. 673), the two-sided gap (p. 674), and the declaration that scheduling is open (p. 681).

**[A3]** Kostyukevich and Dmitruk (2021). `corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf`. Cited for the affine-in-$\alpha$ support result under the rank condition (p. 43), the piecewise-affine regime (pp. 44–45), and the one-LP solution (p. 45).

**[A4]** Dmitruk, N. M. (2022). Multiply-closed strategy in a linear terminal guaranteed-control problem. `corpus/our_papers/A4_Дмитрук_2022.pdf`. [DOI](https://doi.org/10.21538/0134-4889-2022-28-3-66-82). Page convention: PDF page with journal page in parentheses; PDF p. 1 is journal p. 66. Cited for the model (p. 68), the fixed schedule (p. 69), the DP recursion and the inequality $V_0\le J$ (p. 72), the polyhedral closing sets (p. 72), the non-monotone dependence on the closure moment (p. 78), and the a posteriori certification (p. 73).

**[A5]** Dmitruk, N. M. (2022). Dissertation. `corpus/our_papers/A5_Дмитрук_диссертация_2022.pdf`. Cited for the qualitative ladder (p. 39), Theorem 2.1 (p. 53), Theorem 2.2 (p. 55), Theorem 2.3 (p. 59), Lemma 2.5 (p. 65), Theorem 2.4 (p. 69), Statement 2.1 (p. 73), and the declared exclusion of optimal placement (p. 75).

**[AP16]** Ayoub, J. and Poss, M. (2016). Decomposition for adjustable robust linear optimization subject to uncertainty polytope. *Computational Management Science* 13(2):219–239. [DOI](https://doi.org/10.1007/s10287-016-0249-2). `corpus/06_Ayoub_Poss_2016.pdf`. HAL preprint pagination; journal pagination not mapped.

**[BdR16]** Bertsimas, D. and de Ruiter, F. J. C. T. (2016). Duality in two-stage adaptive linear optimization: faster computation and stronger bounds. *INFORMS Journal on Computing* 28(3):500–511. [DOI](https://doi.org/10.1287/ijoc.2016.0689). `corpus/05_Bertsimas_deRuiter_2016.pdf`.

**[BEG18]** Ben-Tal, A., El Housni, O. and Goyal, V. (2018). A tractable approach for designing piecewise affine policies in two-stage adjustable robust optimization. *Mathematical Programming*. [DOI](https://doi.org/10.1007/s10107-019-01385-0). `corpus/tex_src/10_BenTal_ElHousni_Goyal_2018/affine_domination.tex`. Cited by TeX line number.

**[BG14]** Bertsimas, D. and Georghiou, A. (2014). Design of near optimal decision rules in multistage adaptive mixed-integer optimization. *Operations Research*. [DOI](https://doi.org/10.1287/opre.2015.1365). `corpus/20_Bertsimas_Georghiou_2014.pdf`. Pre-journal manuscript; final pagination not visible in this copy.

**[BGL15]** Bertsimas, D., Goyal, V. and Lu, B. Y. (2015). A tight characterization of the performance of static solutions in two-stage adjustable robust linear optimization. *Mathematical Programming* 150(2):281–319. [DOI](https://doi.org/10.1007/s10107-014-0768-y). `corpus/04_Bertsimas_Goyal_Lu_2015.pdf`. MIT author manuscript: cited pages are manuscript pages.

**[BGT04]** Ben-Tal, A., Goryashko, A., Guslitzer, E. and Nemirovski, A. (2004). Adjustable robust solutions of uncertain linear programs. *Mathematical Programming* 99:351–376. [DOI](https://doi.org/10.1007/s10107-003-0454-y). `corpus/02_BenTal_Goryashko_etal_2004.pdf`. Page convention: PDF page with printed journal page.

**[BN99]** Ben-Tal, A. and Nemirovski, A. (1999). Robust solutions of uncertain linear programs. *Operations Research Letters* 25:1–13. [DOI](https://doi.org/10.1016/S0167-6377(99)00016-4). `corpus/01_BenTal_Nemirovski_1999.pdf`.

**[BS18]** Bertsimas, D. and Shtern, S. (2018). A scalable algorithm for two-stage adaptive robust linear optimization. `corpus/tex_src/13_Bertsimas_Shtern_2018/DDBD_ver4_forArxiv.tex`. Cited by TeX line number.

**[CJ20]** Chuong, T. D. and Jeyakumar, V. (2020). Generalized Farkas lemma with adjustable variables and two-stage robust linear programs. *Journal of Optimization Theory and Applications*. [DOI](https://doi.org/10.1007/s10957-020-01753-3). `corpus/15_Chuong_Jeyakumar_2020.pdf`.

**[CJW21a]** Chuong, T. D., Jeyakumar, V., Li, G. and Woolnough, D. (2021a). Exact dual semi-definite programs for affinely adjustable robust SOS-convex polynomial optimization problems. *Optimization*. [DOI](https://doi.org/10.1080/02331934.2021.1902521). `corpus/16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf`.

**[CJW21b]** Chuong, T. D., Jeyakumar, V., Li, G. and Woolnough, D. (2021b). Exact SDP reformulations of adjustable robust linear programs with box uncertainties under separable quadratic decision rules. *Journal of Global Optimization*. [DOI](https://doi.org/10.1007/s10898-021-01050-x). `corpus/17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf`.

**[CZ09]** Chen, X. and Zhang, Y. (2009). Uncertain linear programs: extended affinely adjustable robust counterparts. *Operations Research* 57(6):1469–1482. [DOI](https://doi.org/10.1287/opre.1080.0605). `corpus/03_Chen_Zhang_2009.pdf`. Printed page = PDF page + 1468.

**[DH26]** Dai, L. and Ho, C. P. (2026). When is two-stage sample robust optimization asymptotically optimal? A simple perspective. [arXiv:2608.22999](https://arxiv.org/abs/2608.22999). `corpus/intake/2608.22999.pdf`.

**[GTW20]** Georghiou, A., Tsoukalas, A. and Wiesemann, W. (2020). A primal–dual lifting scheme for two-stage robust optimization. *Operations Research*. [DOI](https://doi.org/10.1287/opre.2019.1873). `corpus/23_Georghiou_Tsoukalas_Wiesemann_2020.pdf`. PDF page cited with printed page.

**[GTW25]** Georghiou, A., Tsoukalas, A. and Wiesemann, W. (2025). On the optimality of affine decision rules in distributionally robust optimization. *Management Science*. [DOI](https://doi.org/10.1287/mnsc.2023.00053). `corpus/24_Georghiou_Tsoukalas_Wiesemann_2025.pdf`.

**[HSR18]** Haddad-Sisakht, A. and Ryan, S. M. (2018). Conditions under which adjustability lowers the cost of a robust linear program. *Annals of Operations Research* 269:185–204. [DOI](https://doi.org/10.1007/s10479-018-2954-4). `corpus/08_HaddadSisakht_Ryan_2018.pdf`. Printed page = PDF page + 184.

**[JLLLW22]** Jeyakumar, V., Lee, G. M., Lee, J. H., Li, G. and Woolnough, D. (2022). Sums of squares polynomial program reformulations for adjustable robust linear optimization with separable polynomial decision rules. *Set-Valued and Variational Analysis*. [DOI](https://doi.org/10.1007/s11228-022-00648-x). `corpus/18_Jeyakumar_etal_2022.pdf`. Printed page = PDF page + 1362. Internal discrepancy: the abstract reports degrees 1–15, Section 4 reports 1–12.

**[Kur25]** Kurtz, J. (2025). Bounding the optimal number of policies for robust $K$-adaptability. [arXiv:2409.12630](https://arxiv.org/abs/2409.12630). `corpus/intake/2409.12630.pdf`.

**[LS22]** Lu, H. and Sturt, B. (2022). On the sparsity of optimal linear decision rules for a class of robust optimization problems with box uncertainty sets. *Operations Research*. [DOI](https://doi.org/10.1287/opre.2023.0603). `corpus/tex_src/11_Lu_Sturt_2022/main_final.tex`. Cited by TeX line number. Scope: parameter sparsity inside the LDR class, not exactness.

**[MDH18]** Marandi, A. and den Hertog, D. (2018). When are static and adjustable robust optimization problems with constraint-wise uncertainty equivalent? *Mathematical Programming* 170:555–568. [DOI](https://doi.org/10.1007/s10107-017-1166-z). `corpus/09_Marandi_denHertog_2018.pdf`.

**[RZDH23]** de Ruiter, F. J. C. T., Zhen, J. and den Hertog, D. (2023). Dual approach for two-stage robust nonlinear optimization. *Operations Research*. [DOI](https://doi.org/10.1287/opre.2022.2289). `corpus/22_deRuiter_Zhen_denHertog_2018.pdf`. Cited for the exact dualized reformulation and its one-sided primal recovery (p. 4, p. 8 of the corpus copy).

**[TSC22]** Tsang, M. Y., Shehadeh, K. S. and Curtis, F. E. (2022). An inexact column-and-constraint generation method to solve two-stage robust optimization problems. *Operations Research Letters*. [DOI](https://doi.org/10.1016/j.orl.2022.12.002). `corpus/intake/2207.03291.pdf`. Scope: multiplicative error budgets; no statement about decision-rule exactness.

**[XB17]** Xu, G. and Burer, S. (2017). A copositive approach for two-stage adjustable robust optimization with uncertain right-hand sides. *Computational Optimization and Applications*. [DOI](https://doi.org/10.1007/s10589-017-9974-x). `corpus/tex_src/07_Xu_Burer_2017/arlp.tex`. Cited by TeX line number.

**[ZDS18]** Zhen, J., den Hertog, D. and Sim, M. (2018). Adjustable robust optimization via Fourier–Motzkin elimination. *Operations Research*. [DOI](https://doi.org/10.1287/opre.2017.1714). `corpus/21_Zhen_denHertog_Sim_2018.pdf`.

**[ZST24]** Zhang, X., Sun, Y. and Teo, K. L. (2024). Exact SDP reformulations for adjustable robust quadratic optimization with affine decision rules. *Journal of Optimization Theory and Applications*. [DOI](https://doi.org/10.1007/s10957-023-02371-5). `corpus/19_Zhang_2024.pdf`.

**[ZZ13]** Zeng, B. and Zhao, L. (2013). Solving two-stage robust optimization problems using a column-and-constraint generation method. *Operations Research Letters* 41:457–461. [DOI](https://doi.org/10.1016/j.orl.2013.05.003). `corpus/12_Zeng_Zhao_2013.pdf`. Proofs of the three propositions are in an Electronic Companion not in the corpus.

**[P1]–[P5]** Lean declarations `l1_eq_max_sum_diff`, `info_value_monotone`, `one_d_exactness`, `blocks_sum_lower`, `full_upper_value`, in `Aroform.lean` and `TwoDDraft.lean`.

**[S1]–[S6]** Judge artifacts under `artifacts/judge/`: `attack_h-auto-1.txt`, `attack_h-auto-3.txt`, `attack_h-auto-4.txt`, `attack_h-auto-5.txt`, `attack_h-auto-6.txt`, `attack_h-auto-7.txt`, `attack_h-auto-8.txt`, `wedge.txt`, `ladder_exact.txt`. Status: survived-falsifier where applicable, numerically certified, not proved. Details in `docs/THESES.md` §3.