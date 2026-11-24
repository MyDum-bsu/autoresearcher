---
title: "When Is an Affine Decision Rule Exact?"
subtitle: "The state of the theory of two-stage adaptive robust optimization, with an inventory of open problems and candidate attack surfaces"
author: "aro-discovery research programme"
date: "2026-10-20"
abstract: |
 Two-stage adaptive robust optimization asks for a here-and-now decision plus a
 recourse policy that survives every realisation of an uncertain parameter. The
 affine decision rule is the standard tractable surrogate, and the central
 theoretical question is when it loses nothing. This essay fixes the question
 precisely, separates four inequivalent notions of exactness that the
 literature conflates, and surveys what is actually established. Five distinct
 mechanisms that produce exactness are identified (constraint-wise
 decomposition, inverse-positive recourse, conic reformulation, polyhedral
 vertex completion, and restriction to a richer rule class), together with the
 sharp negative families that delimit them. Eight open problems are then stated
 in a form that a theorem could settle. The essay closes with a falsification
 battery: seven instances that any proposed necessary-and-sufficient condition
 must classify correctly, including one class from the author's own programme
 whose affine rule is exact while the project's earlier closed form for the same
 value is not.
---

# Scope, sources, and what this essay does not claim

This is a survey essay with an argument, not a survey with a bibliography. Its
purpose is to state where the theory of affine decision rules currently stands,
which of its gaps are real, and where a new theorem could plausibly live. Every
mathematical claim about the literature is anchored to a page of a document in
the project corpus, named by file in the reference list. Claims that
come from the author's own programme are labelled by their exact machine status,
which is never "proved" unless a Lean file compiles without `sorry`.

Two boundaries are worth stating at the outset, because a reader who mistakes
them will over-read everything that follows.

First, the corpus is finite. It contains twenty-four numbered external papers,
five papers of the Dmitruk school, three recently added preprints, and TeX
sources for five of the numbered papers. A scan of 2023--2026 literature produced leads, and those
leads are cited nowhere in this essay as established results. They appear only
in the final section, marked unverified, as orientation for future reading.

Second, the essay is deliberately silent about algorithmic practice. Column-and-
constraint generation, Benders decomposition, cutting-plane certification and
the engineering of solvers are treated only where a theorem about exactness
depends on them. The question here is structural: given a problem class, is the
affine rule optimal, and if not, how far from optimal is it.

# The problem, and four inequivalent notions of exactness

## The two-stage problem

Let $x \in \mathbb{R}^{n_1}$ be the here-and-now decision, $y \in \mathbb{R}^{n_2}$ the
recourse decision, $\xi \in \Xi \subseteq \mathbb{R}^m$ the uncertain parameter, and
consider

$$
\min_{x \in X}\; c^\top x \;+\; \max_{\xi \in \Xi}\; \min_{y}\;\big\{\, d^\top y \;:\; A(\xi)x + B y \ge h(\xi),\ y \ge 0 \,\big\}.
\tag{2.1}
$$

The recourse matrix $B$ is fixed: it does not depend on $\xi$. This is the
*fixed recourse* assumption, and it is the hypothesis without which most of the
results surveyed here fail, because it is what makes the inner problem an LP
whose dual has a decision-independent feasible set. Ben-Tal, Goryashko, Guslitzer and
Nemirovski introduced the terminology and the observation together [BGT04, p. 353].

Write $V_{\mathrm{AR}}$ for the optimal value of (2.1), the *fully adaptive* value:
the recourse decision is an arbitrary measurable function $y : \Xi \to \mathbb{R}^{n_2}$.
Four restrictions of the policy class recur throughout the literature.

- The *static* rule takes $y(\xi) \equiv y$, one decision for all scenarios.
- The *affine* (or linear) decision rule (ADR/LDR) takes
 $y(\xi) = y_0 + Y\xi$ for a matrix $Y$ of appropriate size; write $V_{\mathrm{AP}}$
 for the resulting value.
- The *piecewise affine* rule is affine on each cell of a finite polyhedral
 partition of $\Xi$.
- The *$K$-adaptable* rule selects in the first stage $K$ candidate policies and
 commits to one of them after observing $\xi$.

Two further parameters act as design variables rather than as modelling
constants. The first is the number $K$ of candidate policies. The second,
specific to deterministic guaranteed control, is a *schedule*: a subset $R$ of
time instants at which the state is measured and the control is recomputed.

## Four notions of exactness

The literature uses "exact" for at least four different statements, and
conflating them is the source of several apparent contradictions.

**Value exactness.** $V_{\mathrm{AP}} = V_{\mathrm{AR}}$: the restricted class
attains the adaptive optimum in value. This is what a bound on the price of
adaptivity measures, and it is what an exactness theorem usually asserts.

**Solution exactness.** There is an affine rule that is optimal *pointwise*:
for every $\xi$ in the support, the rule attains the inner minimum itself, not
the outer worst-case value. This is strictly stronger than value exactness. The
distinction is not academic: Georghiou, Tsoukalas and Wiesemann construct a
problem where the optimal value is attained by an affine rule under a monotone
risk measure, while at a *suboptimal* first-stage decision the unique optimal
policy is nonlinear [GTW25, p. 9]. Solution exactness at the optimal $x$ does not
propagate to nearby $x$.

**Feasibility exactness.** The affine rule achieves the same robust feasible
region for $x$ as the fully adaptive problem. This is the notion in play in the
vertex-reduction results, and it can fail while value exactness holds, because a
different $x$ may compensate for an infeasible policy.

**Reformulation exactness.** A fourth usage is common in the semidefinite and
sum-of-squares literature: "exact reformulation" there means that the SDP has
the same value as the *rule-restricted* problem, with a one-to-one
correspondence between optimal solutions [CJW21b, p. 1; JLLLW22, p. 2]. It does
not mean that the restricted class is lossless relative to the fully adaptive
problem. Since the restricted class is the starting point of those papers, the
two statements are independent: an exact reformulation can be exact of an
approximation. Every claim below distinguishes the two, and the phrase
"reformulation exact" is reserved for the weaker statement.

Unless stated otherwise, "exact" below means value exactness relative to the
adaptive problem. Where a result concerns one of the other notions, the text
says so.

## The reformulation that makes the question tractable

With fixed recourse, LP duality turns the inner minimum into a maximum over the
dual feasible set $\mathcal{W} = \{w \ge 0 : B^\top w = d\}$, which does not
depend on $\xi$ or on $y$. The adversary's problem becomes a bilinear program
over $\Xi \times \mathcal{W}$, and it is NP-hard in general [XB17, arlp line 379--384;
BS18, DDBD line 360]. The affine restriction has a different fate: substituting
$y(\xi) = y_0 + Y\xi$ replaces $n_2$ adjustable variables by $n_2(m+1)$
non-adjustable ones [MDH18, p. 2] and leaves a finite-dimensional LP when $\Xi$
is a polytope [BGT04, Thm. 3.3, p. 360]. The parameter count is itself an object
of study: in the production-inventory class there always exists an optimal rule
with $O(ET)$ non-zero parameters rather than $O(ET^2)$ [LS22, `thm:main`,
main_final line 661].

So the structural question has a sharp form. The affine rule is a *tractable
inner approximation of an intractable exact object*. Exactness asks when the
approximation is tight. Xu and Burer make this literal: the exact object is a
copositive program, and the affine rule is the restriction of that program to an
inner cone [XB17, arlp line 614--683]. Everything else in the literature is, in one way or
another, a sufficient condition for that restriction to be lossless.

# Five mechanisms that produce exactness

The survey literature tends to list exactness results chronologically. That
ordering hides the fact that the results rest on five logically distinct
mechanisms. Separating them is the first contribution of this essay, because a
proposed necessary-and-sufficient condition must explain *which* mechanism it
generalises, and no single mechanism accounts for all the exact cases assembled
here.

## M1: Constraint-wise decomposition

The oldest sufficient condition is separability of the uncertainty across
constraints. Partition $\xi = (\xi^1,\dots,\xi^m)$ so that the $i$-th residual
depends on $\xi^i$ only, and suppose $\Xi = \Xi_1 \times \cdots \times \Xi_m$
with each factor nonempty, convex and compact. Then the static and fully
adaptive problems coincide in value and in feasible here-and-now decisions
[BGT04, Thm. 2.1, p. 354]. Marandi and den Hertog restate the condition in a
form that isolates what it buys: under constraint-wise uncertainty plus modest
regularity, the static rule is exactly optimal [MDH18, p. 561].

The mechanism is decomposition, not geometry. The uncertainty set may be a box,
a ball, or a polytope of any shape, and it may have any number of vertices, as
long as it factors. The condition reappears as a special case in several later
results [MDH18; GTW25], where it serves as the degenerate case in which the
adversary cannot couple constraints, so a single recourse decision suffices.

## M2: Inverse-positive recourse and dominant constraints

The sharpest exactness theorem the corpus contains is due to Georghiou,
Tsoukalas and Wiesemann [GTW25, Thm. 1, p. 8]. Under fixed recourse and four
conditions on an optimal $x$, the affine value equals the adaptive value.

- (F) the second-stage objective $f(x,\cdot;\xi)$ is non-decreasing in $y$;
- (A) the technology matrix $A(\xi)$ and right-hand side $g(\xi)$ are affine in
 $\xi$;
- (D) a dominance condition that lets the remaining constraints be dropped once
 a chosen subset is satisfied;
- (B) there is an index set $I$ of exactly $n_2$ constraints such that $B_I$ is
 invertible with $B_I^{-1} \ge 0$, and the restricted system
 $A_I(\xi)x + B_I y \ge g_I(\xi)$ is equivalent, on $\Xi$, to the full first
 constraint set.

Condition (B) has a transparent reading: the chosen constraints are a
*sufficient* set, and their coefficient matrix is an M-matrix. In that case the
unique candidate
$y^{\ell}(\xi) = B_I^{-1}\,[\,g_I(\xi) - A_I(\xi)x\,]$
is affine, feasible, and pointwise minimal, hence optimal by monotonicity
[GTW25, eq. (17), p. 42]. Proposition 2 makes (B) checkable in practice: if each
variable has a weakly dominant constraint and the coefficient vectors of those
constraints form a partial order, then $B_I$ is a Z-matrix similar to a
strictly triangular matrix with unit diagonal, hence an M-matrix [GTW25, p. 11].
This is the mechanism that covers inventory, lot-sizing and supply-chain models
with serial or arborescent structure.

Two features of this theorem matter for the rest of the essay. It is stated for
the distributionally robust problem, so it covers robust optimization as the
Dirac case, and it imposes *no* structure on the support $\Xi$, which may be
non-convex [GTW25, p. 6]. And it is explicitly one-sided. Each of the four
conditions is *minimal* in the sense that dropping it invalidates the theorem's
conclusion: four single-violation counterexamples are given, with values
$1$ against $1/2$ for (F), $1$ against $1/3$ for (A), $1$ against $1/2$ for
(D), and $3/2$ against $5/4$ for (B) [GTW25, Prop. 1, p. 10]. But none is
*necessary*: the same proposition exhibits an instance that violates all four and
whose optimal policy is nevertheless affine.

One warning about how this theorem is usually cited. The exactness it asserts is
between the affine rule and the fully adaptive problem, which is the strong
notion. That is not true of every "exact" result in the corpus. Ben-Tal et al.'s
Theorem 4.2, for instance, asserts that an explicit SDP equals the AARC for a
single ellipsoid [BGT04, p. 364]; it does not assert that the AARC equals the
ARC. It is reformulation exactness in the sense of §2.2, and it should not be
counted among the sufficient conditions for affine exactness.

## M3: Conic reformulation and cone membership

Xu and Burer show that the fully adaptive two-stage problem with fixed recourse
and right-hand-side uncertainty has an exact copositive reformulation
[XB17, `thm:equivalence`, arlp line 496]. On the same page range they show that the affine rule is the
restriction of that program to the cone of *inverse-nonnegative* matrices
$\mathrm{IA}(Q)$, and that the restricted program reproduces the affine value
exactly [XB17, `theorem:affine-tractable`, arlp line 682]. The sandwich theorem is the conceptual core:

$$
v_{\mathrm{AR}}^* \;\le\; v_{\mathrm{IB}}^* \;\le\; v_{\mathrm{AP}}^*
\tag{3.1}
$$

for every closed convex cone $\mathrm{IB}(Q)$ with
$\mathrm{IA}(Q) \subseteq \mathrm{IB}(Q) \subseteq \mathrm{COP}(Q)$ [XB17, `theorem:approximaterlp`, arlp line 783].
Read as a characterisation, (3.1) says that exactness is a *cone-membership*
statement: $v_{\mathrm{AP}} = v_{\mathrm{AR}}$ holds precisely when an optimal
copositive multiplier for the adversary problem happens to lie in the affine
face.

This is the most conceptually satisfactory formulation available, and it is
also the least algorithmic. Copositive membership is NP-hard, and the paper's
own numerical section reports the typical situation: on 971 of 1000
multi-item-newsvendor instances the intermediate bound and the affine bound
coincide and both sit strictly above the lower bound, while on the remaining 29
the intermediate bound is strictly better than the affine bound [XB17, arlp line 1315--1318].
The paper also exhibits a class, the temporal-network problem of Wiesemann,
Kuhn and Rustem, on which a second-order-cone inner approximation closes the
affine gap exactly [XB17, temporal-network result, arlp line 1045]. That class is important here
because it is the canonical *negative* test for any proposed exactness
condition: the affine gap there is unbounded in general, and the condition must
not certify it.

## M4: Polyhedral vertex structure and barycentric completion

A different mechanism works directly with the geometry of $\Xi$ and makes no
reference to cones. Its starting point is the observation, old and elementary,
that a robust constraint depends on the closed convex hull of the uncertainty
set and on nothing finer [BN99, p. 3]; what changes in the two-stage setting is
that the convexification has to be applied to the *policy graph* rather than to
the uncertainty set.

Ayoub and Poss prove that when $\Xi$ is a polytope and the recourse matrix is
fixed, replacing $\Xi$ by its vertex set is exact for the *fully adaptive*
problem: $x$ extends to an optimal solution of the original problem if and only
if it extends to one of the vertex-restricted problem [AP16, Lemma 1, p. 5].
They also show that the reduction fails as soon as the recourse matrix depends
on $\xi$: a two-point example is feasible at both endpoints and infeasible at
the midpoint [AP16, p. 6]. The pair of results delimits fixed recourse as
exactly the hypothesis under which vertices carry all the information.

Georghiou, Tsoukalas and Wiesemann turn the same fact into a constructive
completion. If the uncertainty set is a bounded polyhedron, $T$ and $h$ are
affine, and $W$ is constant, then for $\xi$ in $\Xi$ one may write $\xi$ as a
barycentric combination of vertices and define the recourse decision as the same
combination of vertex decisions; feasibility transfers because the constraint
map is affine and the recourse matrix is constant [GTW20, Prop. 1, p. 575].
Their Proposition 4 extends the construction: any rule whose graph lies in the
convex hull of the scenario policies is feasible and attains the same value
[GTW20, p. 583], and Proposition 5 identifies the resulting rules as piecewise
affine on a simplicial decomposition, with the barycentric formula as closed form
[GTW20, pp. 583--584].

The mechanism is *convexification of the policy graph*, and it explains why the
exact class in general is piecewise affine rather than affine: the convex hull of
a finite set of scenario decisions generates a piecewise affine rule whenever
the barycentric weights vary with $\xi$. The affine rule is the special case in
which the weights are themselves affine.

Dai and Ho supply the sharp geometric counterpart on the feasibility side. Call
a polyhedron *simple* when every vertex is incident to exactly as many edges as
the ambient dimension. At a simple vertex, every globally feasible recourse
system is locally linearly feasible [DH26, Thm. 2, p. 11], and consequently
simplicity of the support makes the technical condition in their asymptotic
optimality theorem automatic [DH26, Cor. 1, p. 13]. Conversely, for every
non-simple polyhedron there exist data that are globally feasible but not
locally affine at a vertex [DH26, Thm. 4, p. 23]. The authors are careful about
what this does not say: on a non-simple support the condition is no longer
automatic, but it can still hold [DH26, p. 24].

## M5: Restricting to a richer rule class

The fifth mechanism abandons the affine rule and asks for the smallest
superclass that is exact.

Bertsimas and Georghiou build their class around the fact that optimal decision
rules in multistage adaptive optimization are piecewise linear, and they prove
that every continuous piecewise linear function on a compact set is
representable in it [BG14, Thm. 1, p. 5]. The affine rule is the one-piece
case [BG14, p. 5]. Their numerical
section puts the affine gap at more than 20 per cent on average and up to 60 per
cent [BG14, p. 28].

Zhen, den Hertog and Sim obtain exactness for fixed-recourse ARO by Fourier--
Motzkin elimination, with the adjustable variables eliminated one at a time
[ZDS18, p. 24]. The price is explicit: eliminating $N_2$ variables costs
$O(M^{2^{N_2}})$ constraints [ZDS18, p. 8]. Partial elimination gives a monotone
ladder of inner approximations, exact when all adjustable variables are
eliminated [ZDS18, p. 9]. Two results in that paper are especially useful for
the present argument. First, the authors exhibit a fixed-recourse lot-sizing
instance on which imposing linear decision rules is strictly suboptimal while
the elimination reformulation is exact [ZDS18, p. 9]. Second, they prove that a
piecewise affine optimal rule exists with *no* assumption on the uncertainty set
[ZDS18, Thm. 3, p. 11], and that simplex uncertainty is an island where linear
rules suffice [ZDS18, p. 12].

The polynomial-rule line pushes the same idea into semidefinite programming.
Chuong, Jeyakumar and co-authors establish exact sum-of-squares reformulations
for separable quadratic rules over box uncertainty [CJW21b, Thm. 3.1, p. 7],
then for separable polynomial rules of degree $\ell$ [JLLLW22, Thm. 3.1, p. 6],
with a one-to-one correspondence between optimal solutions in addition to
equality of values [CJW21b, p. 1]. Zhang, Sun and Teo extend the pattern to
adjustable robust quadratic programs with a diagonal affine rule [ZST24,
Thm. 3.1, p. 7]. The price is paid in the cone: the reformulations are exact
SDPs, and the general non-affine case remains NP-hard [CJW21a, p. 13].

Chen and Zhang occupy a middle position. They enlarge the affine class by
allowing splitting of the uncertainty vector across several affine pieces and
prove that the enlarged feasible set equals the fully adaptive one [CZ09,
Thm. 1, p. 4]. The mechanism is again graph convexification, and the cost is
the number of extreme points, which is exponential in the number of constraints
[CZ09, p. 4]. Their example makes the stakes concrete: the extended rule attains
value 1 where the plain affine rule attains $N$ [CZ09, p. 6].

# What the negative side establishes

Exactness results are only half the theory. The other half says that the affine
rule cannot be exact in general, and it is considerably sharper than the
positive side.

## Sharp gap families

The corpus contains four explicit gap families. Three are unbounded in a
dimension, and one is a single small instance that can be checked by hand.

Bertsimas, Goyal and Lu give a characterisation for a *fixed* uncertainty set:
either $T(U,h)$ is convex for every $h > 0$, in which case the static value
equals the adaptive value, or $T(U,h)$ is non-convex for some $h$, in which case
there exists an instance with that uncertainty set whose static value is
strictly larger [BGL15, p. 11]. The non-convexity measure $\rho(U)$ bounds the ratio
$z_{\mathrm{AR}} / z_{\mathrm{Rob}}$ tightly and is at most the number of
constraints [BGL15, pp. 15, 17]. Their family $U^\theta$ has
$\kappa(T(U^\theta,h)) = n^{1/\theta}$ for every $h$, so any prescribed gap ratio
is attainable [BGL15, p. 32]. This is a statement about *static* rules, not
affine ones, and the distinction matters: the transformation characterisation
does not transfer to the affine class, and it should not be cited as if it did.

Ben-Tal, El Housni and Goyal give the affine counterpart under a domination
construction. If a simplex scaled by $\beta$ dominates $\Xi$, a piecewise affine
policy built from the threshold map gives a $2\beta$-approximation
[BEG18, `thm:cost`, affine_domination line 389], and the scaling factor is computable in closed form for
permutation-invariant sets. Their separating instance has an affine policy that
is $\Omega(\sqrt{m})$ off the optimum while the piecewise affine policy is
$O(1 + 1/\sqrt{m})$ [BEG18, affine_domination line 661--690]. The construction relies on the dominating set
*containing* the uncertainty set only up to scaling, which is the point the
authors stress.

Haddad-Sisakht and Ryan give the only *checkable* sufficient condition for a
strict gap that the corpus contains. If two constraints are binding at an
optimal static solution for different values of the same uncertain parameter,
and relaxing either strictly improves the static value, then adjustability
strictly lowers the cost [HSR18, Prop. 1, p. 7]. The condition is stated for box
uncertainty and fixed recourse, and it is a certificate rather than a
characterisation. Its converse is false: the authors exhibit three instances
that satisfy none of the published sufficient conditions for static optimality
and yet have equal static and adaptive values [HSR18, p. 18].

Chen and Zhang's $N$-versus-1 example and the (B)-violating instance of
Georghiou, Tsoukalas and Wiesemann, with values $3/2$ and $5/4$
[GTW25, p. 45], complete the set of explicit witnesses. Each is small
enough to be checked by hand, which is what makes them useful as test cases.

## Hardness

Four hardness results limit what an exactness theorem can be expected to
deliver, and one of them concerns certification rather than optimisation.

The adaptive problem with fixed recourse is NP-hard when $\Xi$ is a general
polytope given by linear inequalities, and also when $\Xi$ is a finite convex
hull but the recourse matrix depends on the scenario [BGT04, p. 355]. The
proofs are in a thesis not present in the corpus, which is a genuine gap in our
evidence and is flagged as such. With uncertain recourse, even the affine
problem is NP-hard: its value is the maximum of a quadratic form over the
simplex, which is a copositivity check [BGT04, Example 3.1, p. 360].

Computing the worst case for a fixed here-and-now decision is NP-hard
[BS18, DDBD line 360], so even certifying a candidate solution is hard without structure.
And choosing the minimal number of policies that restores exactness is
NP-complete, even when uncertainty appears only in the objective [Kur25,
Thm. 29, p. 20].

## The insufficiency of vertex reasoning

A tempting shortcut is to reason only about vertices, since the worst case of a
linear program over a polytope is attained at a vertex. The corpus contains
three independent refutations of the shortcut as a route to exactness.

Bertsimas, Goyal and Lu's family shows that a convex, vertex-represented,
down-monotone set can still have an arbitrary static gap [BGL15, p. 32].
Ayoub and Poss show that vertex reduction preserves the fully adaptive optimum
but not the affine one, and that it fails outright under random recourse
[AP16, pp. 5--6]. Dai and Ho show that vertex *incidence structure*, not the
vertex set alone, controls whether local affine feasibility follows from global
feasibility [DH26, pp. 11, 23].

The correct reading is that the vertex set determines the *adaptive* value and
says nothing about the affine value. Any exactness condition must therefore
constrain the interaction between the recourse matrix and the constraint
geometry, as well as the uncertainty set.

# The bridge class: an exact case outside every sufficient condition

The author's programme studies a deterministic guaranteed-control problem that
sits inside the fixed-recourse, right-hand-side-uncertainty setting of §2 but
has enough structure to be solved in closed form. This section states it
precisely and reports what is actually established, with machine status.

## Definition and the rotation

Fix integers $T \ge 1$ and parameters $d_0 \in \mathbb{R}$,
$e = (e_1,e_2) \in \mathbb{R}^2$, $u_b > 0$. The *bridge class*
$\mathcal{B}(T,d_0,e,u_b)$ has state $x_t \in \mathbb{R}^2$, initial condition
$x_0 = (d_0,d_0)$, dynamics

$$
x_{t+1} = x_t + \begin{pmatrix}1\\1\end{pmatrix} u_t + \begin{pmatrix}e_1\\e_2\end{pmatrix} w_t,
\qquad |u_t| \le u_b,\quad w_t \in \{-1,+1\},
\tag{5.1}
$$

and cost $\|x_T\|_1$. A closure set $R \subseteq \{1,\dots,T\}$ specifies the
information structure: at step $t$ the control may depend on $w_1,\dots,w_{r}$
where $r$ is the largest element of $R$ not exceeding $t-1$. Write $V(R)$ for
the minimax value, $V(\varnothing)$ for the blind value and $V(\{1,\dots,T\})$
for the full-information value.

The rotation $s_t = x_{1t} + x_{2t}$, $d_t = x_{1t} - x_{2t}$ is an isometry for
the terminal cost, $\|x_T\|_1 = \max(|s_T|,|d_T|)$, and it diagonalises the
dynamics:

$$
s_T = 2d_0 + 2U + S\,W, \qquad d_T = D\,W,
\qquad U = \sum_{t=1}^{T} u_t,\quad W = \sum_{t=1}^{T} w_t,
\tag{5.2}
$$

with $S = e_1 + e_2$ and $D = e_1 - e_2$. Here $W$ is the accumulated
disturbance; it is not the edge value $g_{\max}$ of S2. The rotation identity
$\|(a,b)\|_1 = \max(|a+b|,|a-b|)$ is P1. The difference coordinate is
uncontrollable, so the worst-case difference is $|D|\,T$ and this term is a
floor under every value in the class.

## What is proved

Three statements in this class compile in the Lean core. P1 is unconditional;
P2 and P3 are axiom-gated, which is a weaker status and is recorded as such
below.

**P1 (rotation).** $\|(a,b)\|_1 = \max(|a+b|,|a-b|)$.

**P2 (information monotonicity).** Extending the set of admissible strategies
cannot increase the infimum, so $R_1 \subseteq R_2$ implies
$V(R_1) \ge V(R_2)$.

**P3 (one-dimensional exactness).** In the one-dimensional bridge the affine
rule attains the exact adaptive optimum. P2 and P3 are axiom-gated in the
current formalisation, which is a weaker status than P1 and is recorded as such.

Two further statements are sorry-free Lean proofs but have not yet been
transferred into the main formalisation: the lower half of the blind-block
composition and the upper half of the full-information value via a centering
strategy [P4, P5].

## What is certified but not proved

Six statements have survived adversarial numerical testing on frozen grids with
exact rational arithmetic. None of them is a theorem. The project's status
ladder is explicit about this: *survived-falsifier* means numerically certified
on a frozen grid, not proved. The list below includes one refutation, S1,
because it is a certified result about the class and bears directly on the
wedge argument later in this section.

**S1 (wedge law).** An earlier project derivation of the full-information value
took the form

$$
V_{\mathrm{old}} \;=\; \max\Big(\max\big(|S|,\,2|d_0| - (2u_b - |S|)T\big),\; |D|\,T\Big)
\tag{5.3}
$$

with no external anchor: it was derived inside the project and implemented in
the project's ladder-forms script (`scripts/ladder_forms.py`, listed under
[S1]--[S6]). It is correct outside the wedge
$\mathcal{W} = \{|S| > 2u_b,\ 2|d_0| < 2u_b,\ T \ge 2\}$ and strictly
underestimates inside it. Inside, the value is the pursuit iteration
$f_1^{T}(2|d_0|)$ with $f_1(x) = \max(x - 2u_b, 0) + |S|$. Evidence: 864 of 864
grid points plus a 576-point regression judge, byte-identical on reruns. This is
an internal refutation, not a correction to a published theorem, and the essay
flags it because the distinction is easy to lose in citation.

**S2 (one-closure scheduling law).** For a single closure at $r$,
$V(\{r\}) = \max(c, g(r))$ with
$c = \max(2|d_0| + (|S|-2u_b)T,\ |D|T)$ and
$g(r) = \max(|S|(T-r),\ |S|T - 2u_b(T-r))$. The minimiser is the plateau
$\{r : g(r) \le c\}$, and the plateau fills the whole domain $[1,T-1]$ if and
only if $c \ge g_{\max}$, where $g_{\max} = \max(g(1), g(T-1))$ is the larger
edge value of the valley. Evidence: 72 instances, 148 exact LP points, zero
violations.

**S3 (block composition).** For an arbitrary closure set $R$, $V(R)$ equals the
fold of the one-closure value over the blind-block lengths. Evidence: 137
pathwise LP points and 5952 DP comparisons.

**S4 (tail sum).** With $L_0,\dots,L_k$ the consecutive differences of
$[0] \cup \mathrm{sorted}(R) \cup [T]$,

$$
V(R) = \max\Big(|D|T,\;\; 2|d_0| + (|S|-2u_b)T,\;\;
\max_{0 \le j \le k}\big[\,|S|\,L_j + (|S|-2u_b)(L_{j+1}+\cdots+L_k)\,\big]\Big).
\tag{5.4}
$$

Evidence: 596 LP points, 54 reductions, 3348 DP cross-checks.

**S5 (full-prefix affine exactness).** In the full-information case the affine
rule over the observed prefix attains the adaptive optimum,
$V_{\mathrm{AP}} = \max(f_1^T(2|d_0|), |D|T) = V(\{1,\dots,T\})$. Evidence: 576
exact LP points, zero gap.

**S6 (maxmin floor).** The path-committed max-min value has the closed form
$V_{\mathrm{mm}} = \max\big(\max(2|d_0| + (|S|-2u_b)T, 0),\ |D|T\big)$ and
$V(R) \ge V_{\mathrm{mm}}$ for every $R$. Evidence: 47 instances, 518 oracle
points over all closure sets.

## Why this class matters for the general theory

Three things follow, and they are the reason the class appears in this essay at
all rather than only in the author's own reports.

First, it is a *positive* affine-exactness instance that none of the five
mechanisms of §3 certifies. The uncertainty set is the vertex set of a cube, so
it is non-simple for $T \ge 2$; the recourse matrix has entries of both signs
and is not inverse-positive in the obvious basis; the constraint system is not
constraint-wise. M1 and M2 therefore do not apply. M4 does apply: $T$ and $h$
are affine and the recourse matrix is constant, so the barycentric completion
produces an exact *piecewise affine* rule. That is precisely the distinction
that matters here, because S5 asserts exactness of the *affine* rule, which M4
does not deliver. M3 addresses the affine class directly but gives no
transparent certificate, and M5 can always be invoked by enlarging the class
until exactness is trivial. So no mechanism in the literature surveyed here
certifies the affine exactness that S5 reports. A proposed necessary-and-
sufficient condition must certify this class, and that gives it a test it would
otherwise not face.

Second, it separates two gaps that the literature usually conflates. In this
class the affine-versus-adaptive gap is zero (S5), while the
*published-formula-versus-truth* gap is strictly positive inside $\mathcal{W}$
(S1). The wedge is therefore a witness that an exactness result about rule
classes does not protect against an incorrect closed form for the value, and
that checking a formula requires a different instrument from checking a policy
class. Both statements are anchored to judge artifacts, so the distinction is
substantive.

Third, the class makes the scheduling question finite and decidable. The tail
sum (5.4) turns "choose the best set of closure moments" into a minimisation of
a maximum of $k+1$ linear forms over compositions of $T$ into $k+1$ parts. That
is a bottleneck-partition problem, and it is the object that §6.4 and §6.5
discuss.

# Eight open problems

The following are stated so that a theorem, a counterexample, or a complexity
result could settle each. For each, the text says what is already known and what
is missing.

## O1. A necessary-and-sufficient condition for affine value exactness

*Statement.* Characterise, in terms of $(A(\cdot), h(\cdot), B, \Xi)$, when
$V_{\mathrm{AP}} = V_{\mathrm{AR}}$ for fixed-recourse right-hand-side
uncertainty.

*Known.* Sufficient: constraint-wise uncertainty [BGT04, Thm. 2.1];
inverse-positive recourse with dominance [GTW25, Thm. 1]; simplex uncertainty
for linear rules [ZDS18, p. 12]; box uncertainty for static rules
[BdR16, p. 12]. A fourth, logically different route is an exact conic dual:
under a closed-cone regularity condition an adjustable Farkas lemma yields an
exact conic program for the two-stage problem [CJ20, p. 3], and for
SOS-convex data the dual is an exact SDP [CJW21a, p. 4]. These are
reformulation-exactness results and say nothing about the size of the affine
class, but they show that the *dual* side admits exactness statements where the
primal side does not. A single ellipsoid with uncertain recourse gives an SDP equal to
the *AARC* [BGT04, Thm. 4.2], which is reformulation exactness only and is not
counted here. Exact reformulation of the question: cone membership
[XB17, `theorem:approximaterlp`, arlp line 783].

*Missing.* Any necessary condition beyond the trivial. Two published statements
of non-necessity exist, and both concern sufficient conditions rather than a
characterisation: the instance in [GTW25, Prop. 1] that violates all four
exactness conditions and is nonetheless exact, and the three instances in
[HSR18, p. 18] that fall outside the known sufficient conditions for static
exactness and yet have equal values. The cone characterisation is exact but not
decidable in polynomial time, and it has not been specialised to yield checkable
conditions on the data. This is the central open problem of the field as
represented in this corpus.

## O2. An exact formula, or a sharp rate, for the affine gap

*Statement.* For fixed recourse and RHS uncertainty, determine
$\sup_{\Xi} \, V_{\mathrm{AP}} / V_{\mathrm{AR}}$ as a function of the geometry
of $\Xi$ and the structure of $B$.

*Known.* Static case: exact characterisation and tight factor
$\rho(U) \le m$ [BGL15]. Affine case: an $O(\sqrt{m})$ upper bound under a
domination construction [BEG18], with a matching $\Omega(\sqrt{m})$ instance,
and an $O(\sqrt{k})$ worst case reported for linear rules [BG14, p. 2]. Empirical:
20 to 60 per cent [BG14, p. 28]. No exact formula exists for any nontrivial
affine class in this corpus.

*Missing.* Everything between the bounds and the instances. A single class with
a provably exact gap formula would be a substantial result. The bridge class of
§5 is a candidate, where the gap is zero by S5, and the wedge shows where the
formula-based reasoning fails.

## O3. The role of vertex count and vertex incidence

*Statement.* Determine the exact relationship between the combinatorial
structure of $\operatorname{vert}(\Xi)$ and affine exactness.

*Known.* If there are only $m$ extreme points, linear policies are optimal
[BdR16, p. 6, citing Bertsimas and Goyal 2012]; the bound is tight when all
extreme points are included [BdR16, p. 7]. Simplicity of the support makes local
linear feasibility automatic [DH26, Thm. 2]. Non-simple supports admit
counterexamples [DH26, Thm. 4]. Vertex representation alone is insufficient
[BGL15, p. 32; AP16, p. 6].

*Missing.* A statement that is both necessary and sufficient in combinatorial
terms. The Dai--Ho dichotomy is the closest thing, and it concerns feasibility
rather than value. Whether the two can be bridged is open.

## O4. The information structure as a decision variable

*Statement.* Given a family of admissible observation schedules, determine the
complexity of choosing a schedule of minimum cardinality that attains the
full-information value, and characterise when such a schedule exists.

*Known.* The number of $K$-adaptable policies needed for exactness is bounded
by $n_\xi + 1$ under objective uncertainty [Kur25, Thm. 2, p. 5] and by
$\min\{R(n_\xi+1), |Y|\}$ under constraint uncertainty via recourse-stable
regions [Kur25, Thm. 11, p. 10]. Minimal $K$ is NP-complete [Kur25, Thm. 29].
In the Dmitruk school the schedule is an input throughout the line: A1 states
the guaranteed-control problem in a form whose Bellman recursion is not
tabulable [A1], A2 formulates the one-closure problem and fixes the closing
instant in advance [A2], A3 keeps the closing instant fixed a priori [A3], A4
fixes the moments in advance and never optimises them [A4, p. 69], and A5
declares the optimal placement out of scope [A5, p. 75].

*Missing.* Any complexity result for schedules, as opposed to policy counts. The
two problems are not the same: a schedule determines the *information* available
at each decision, while $K$ counts the *policies* committed in advance. No paper
in the corpus relates them. This is the largest structural gap in the corpus,
and the bridge class makes it concrete: the tail sum (5.4) gives the value of
every schedule in closed form, so the optimisation over schedules is a finite
combinatorial problem with a known objective.

## O5. Necessary conditions for a strict gap

*Statement.* Give checkable conditions on $(A,h,B,\Xi)$ that imply
$V_{\mathrm{AP}} > V_{\mathrm{AR}}$.

*Known.* One checkable sufficient condition, for box uncertainty and fixed
recourse, via two binding constraints at different values of a shared parameter
[HSR18, Prop. 1]. Two explicit witnesses [CZ09, p. 6; GTW25, p. 45]. The
observation that vertex reduction fails under random recourse [AP16, p. 6].

*Missing.* Generality. The HSR condition is box-only and instance-level. No
condition in the corpus covers a general polytope, and none is proved necessary.
Necessary conditions for a gap are logically equivalent to sufficient conditions
for exactness, so O5 is the contrapositive face of O1; the literature has
developed the positive face far more than the negative one.

## O6. A price of adaptivity for two-stage robust optimization

*Statement.* Define and compute a quantity, analogous to the price of
anarchy, that measures the worst-case ratio between the adaptive optimum and the
best static solution, as a function of the problem data.

*Known.* The ratio is characterised exactly for the static class
[BGL15, Thm. 3.2], bounded by $\rho(U) \le m$, and computed for specific
families. For the affine class only bounds exist. The term "price of
adaptivity" is not used in this sense anywhere in the corpus; a scan of recent
literature found it only in adjacent literatures, and that lead is unverified.

*Missing.* A definition that is stable across problem classes, and any exact
computation. The obstacle is that the natural ratio is unbounded when the
adaptive value is zero, so a normalisation is needed. The bridge class offers a
clean testbed, since both ends of the ladder are known in closed form there.

## O7. A bridge theorem between guaranteeing-program control and two-stage ARO

*Statement.* Establish an equivalence, or a sharp two-sided bound, between the
guaranteed value of a terminal control problem with scheduled closures and the
value of a two-stage adaptive robust program with a correspondingly structured
uncertainty set.

*Known.* The ladder OC $\ge$ RO$(k) \ge$ DP is formalised as monotonicity in the
author's Lean core [P2]. The Dmitruk school articulates the ladder
qualitatively in one page [A5, p. 39] and computes exact values for fixed
schedules [A4; A5, Thm. 2.1]. A5's Theorem 2.2 gives an exact polyhedral
parametric representation of the closing sets, and A5's Lemma 2.5 gives
piecewise-affine support values via parametric LP basis stability.

*Missing.* No paper in the corpus that we have read states both sides in a
common formalism and proves an equivalence. The author's rotation (5.2) is a candidate dictionary:
it maps the control problem to two scalar coordinates, one controllable and one
not, and the resulting value has the same max-of-two-terms shape as the
robust-optimization bounds. Whether the dictionary extends beyond the bridge
class is open.

## O8. The quantifier-order gap

*Statement.* Quantify the difference between $\min\max$ and $\max\min$ in the
two-stage problem, and determine when it vanishes.

*Known.* Dmitruk observes that the max-min form may be easier to solve than the
min-max form [A4], and the author's S6 gives a closed form for the
path-committed max-min value in the bridge class, with
$V(R) \ge V_{\mathrm{mm}}$ for all $R$ and an explicit gap formula in the pure
regime. No general treatment exists in the corpus.

*Missing.* A general inequality, and a characterisation of the classes where the
gap is zero. The max-min value is a relaxation of the min-max value obtained by
reversing the order of choice, so the gap is a measure of the value of
commitment; the literature on information design would call it the value of
commitment power. Nothing in the corpus connects the two vocabularies.

# A falsification battery for exactness conditions

The eight problems above are hard individually. There is, however, a cheap
instrument that the literature has not assembled and that this essay proposes:
a battery of seven instances any necessary-and-sufficient condition must
classify correctly. Its value is asymmetric. Passing the battery does not
confirm a condition; failing one instance refutes it outright.

| # | Instance | Required verdict | Anchor |
|---|---|---|---|
| T1 | Bridge class of §5 | exact: affine attains adaptive | S5; P3 in 1D |
| T2 | SOC temporal network | **not** exact in general (gap unbounded) | [XB17, temporal-network result, arlp line 1045] |
| T3 | Chen--Zhang $N$-vs-1 | not exact for affine, exact for extended | [CZ09, p. 6] |
| T4 | GTW (B)-violating instance | not exact ($3/2$ vs $5/4$) | [GTW25, p. 45] |
| T5 | BEG separating instance | not exact for affine ($\Omega(\sqrt m)$) | [BEG18, affine_domination line 661--690] |
| T6 | Box uncertainty, static | exact | [BdR16, p. 12] |
| T7 | Simplex uncertainty | exact for linear rules | [ZDS18, p. 12] |

The design of the battery follows from three considerations.

T1 is the discriminating entry. The other six can be passed by conditions that
key on the uncertainty set alone, because in each of them the geometry is
decisive. T1 has uncertainty set equal to the vertex set of a cube, which is
non-simple for $T \ge 2$, and a recourse matrix with both signs. A condition
that certifies *affine* exactness there must use the interaction of dynamics and
cost, not the shape of $\Xi$ alone. A condition that fails T1 may still be a
valid sufficient condition; a claimed *characterisation* that fails T1 is
refuted.

T2 is the anti-triviality entry. A condition that certifies every fixed-recourse
problem passes T6 and T7 and looks strong; T2 forces it to distinguish the
temporal-network family, where the affine gap is unbounded.

T4 is the anti-necessity probe. The instance violates all four conditions of the
strongest exactness theorem in the corpus and is nevertheless exact, so any
condition that claims necessity must accept it. A condition that rejects T4 is
at best sufficient.

The battery is not offered as a contribution to the mathematics. It is offered
as a discipline: it makes the difference between a sufficient condition and a
characterisation visible in a single table, and it gives a referee a concrete
objection to raise.

# What this essay does not cover, and what would change the picture

The essay excludes four topics on purpose.

**Unverified recent literature.** A scan of 2023--2026 work produced leads on
affine optimality beyond simplex uncertainty, on a posteriori exactness tests
built from dual extreme points, on complexity classifications of static,
two-stage and $K$-adaptable robust optimization, and on the value of coupling
uncertainty sets. None of these is cited as established here. Two of them, if
confirmed, would bear directly on O1: an a posteriori exactness test would give
an algorithm for the cone-membership question, and an a priori condition beyond
simplex uncertainty would compete with [GTW25]. They are the highest-value
reading targets before the next revision of this essay.

**The Electronic Companion of Zeng and Zhao.** Three propositions in that paper
are stated without proof; the proofs live in a companion document not in the
corpus [ZZ13]. Anything said here about column-and-constraint generation is
therefore statement-level only.

**The random-recourse case.** Except where noted, the essay stays inside fixed
recourse, because that is where the exactness question has content. With random
recourse the affine problem itself can be NP-hard [BGT04, Ex. 3.1], and the
vertex reduction fails [AP16, p. 6].

**Algorithms and numerics.** Column-and-constraint generation [ZZ13], inexact
certified variants with multiplicative error budgets [TSC22, Prop. 2, p. 7], and
the primal-dual lifting scheme [GTW20] appear only as context. Their convergence
theories are a separate subject. The certified-pipeline question, namely how to
carry an error budget through a decomposition without losing the certificate,
is a methods problem rather than a structural one.

Two developments would change the picture more than any amount of further
reading.

A proof of O1 in the cone-membership language would convert the field's central
question from a collection of sufficient conditions into a decision procedure,
even if the procedure were exponential. The bridge class would then be one of
its first test cases, and the wedge would show what such a procedure does not
cover, namely the value formula itself.

A complexity result for O4 would connect the robust-optimization literature to
the guaranteed-control literature on the one axis where they are currently
disjoint. The Dmitruk school treats the schedule as given; the robust-
optimization school treats the policy class as given. Neither treats the
information structure as the object to be optimised, and the bridge class shows
that in at least one setting the resulting problem is finite, closed-form, and
combinatorial.

# References

Reference entries give the corpus file and the page convention used in the
text. Page numbers in citations are PDF pages unless the entry says otherwise.

**[A1]** Balashevich, N. V. (2004). Guaranteed program control. `corpus/our_papers/A1_Балашевич_2004.pdf`.
Cited for the school's prehistory; schedule is an input.

**[A2]** Dmitruk, N. M. (2018). One-closure guaranteed control. `corpus/our_papers/A2_Дмитрук_2018.pdf`.
Cited for the one-closure formulation and for the explicit statement that the
optimal closure moment is open (p. 681).

**[A3]** Kostyukevich and Dmitruk (2021). `corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf`.
Cited for the piecewise-affine structure of the value under a rank condition.

**[A4]** Dmitruk, N. M. (2022). Multiply-closed strategy in a linear terminal
guaranteed-control problem. `corpus/our_papers/A4_Дмитрук_2022.pdf`.
Page convention: PDF page cited with journal page in parentheses; PDF p. 1 is
journal p. 66. Cited for the fixed schedule (p. 69), the non-monotone dependence
of the value on a single closure moment (p. 78), and the parametric-LP duality
machinery (p. 75).

**[A5]** Dmitruk, N. M. (2022). Dissertation. `corpus/our_papers/A5_Дмитрук_диссертация_2022.pdf`.
Cited for Theorem 2.1 (p. 53), Theorem 2.2 (p. 55), Lemma 2.5 (p. 65), the
qualitative ladder (p. 39) and the declared exclusion of optimal placement
(p. 75).

**[AP16]** Ayoub, J. and Poss, M. (2016). Decomposition for adjustable robust
linear optimization subject to uncertainty polytope. *Computational Management
Science* 13(2):219--239. `corpus/06_Ayoub_Poss_2016.pdf`.
HAL preprint pagination; journal pagination not mapped.

**[BdR16]** Bertsimas, D. and de Ruiter, F. J. C. T. (2016). Duality in
two-stage adaptive linear optimization: faster computation and stronger bounds.
*INFORMS Journal on Computing* 28(3):500--511.
`corpus/05_Bertsimas_deRuiter_2016.pdf`.

**[BEG18]** Ben-Tal, A., El Housni, O. and Goyal, V. (2018). A tractable
approach for designing piecewise affine policies in two-stage adjustable robust
optimization. `corpus/tex_src/10_BenTal_ElHousni_Goyal_2018/affine_domination.tex`.
Cited by TeX line number because the source, not a PDF, is the anchor.

**[BG14]** Bertsimas, D. and Georghiou, A. (2014). Design of near optimal
decision rules in multistage adaptive mixed-integer optimization.
`corpus/20_Bertsimas_Georghiou_2014.pdf`.
Pre-journal manuscript; final venue not visible in this copy.

**[BGL15]** Bertsimas, D., Goyal, V. and Lu, B. Y. (2015). A tight
characterization of the performance of static solutions in two-stage adjustable
robust linear optimization. *Mathematical Programming* 150(2):281--319.
`corpus/04_Bertsimas_Goyal_Lu_2015.pdf`.
MIT author manuscript: cited pages are manuscript pages, not journal pages.

**[BGT04]** Ben-Tal, A., Goryashko, A., Guslitzer, E. and Nemirovski, A. (2004).
Adjustable robust solutions of uncertain linear programs. *Mathematical
Programming* 99:351--376. `corpus/02_BenTal_Goryashko_etal_2004.pdf`.
Page convention: PDF page cited with printed journal page.

**[BN99]** Ben-Tal, A. and Nemirovski, A. (1999). Robust solutions of uncertain
linear programs. *Operations Research Letters* 25:1--13.
`corpus/01_BenTal_Nemirovski_1999.pdf`.

**[BS18]** Bertsimas, D. and Shtern, S. (2018). A scalable algorithm for two-stage
adaptive robust linear optimization. `corpus/tex_src/13_Bertsimas_Shtern_2018/DDBD_ver4_forArxiv.tex`.
Cited by TeX line number.

**[CJ20]** Chuong, T. D. and Jeyakumar, V. (2020). Generalized Farkas lemma with
adjustable variables. `corpus/15_Chuong_Jeyakumar_2020.pdf`.

**[CJW21a]** Chuong, T. D., Jeyakumar, V., Li, G. and Woolnough, D. (2021a).
Exact dual semidefinite programs for affinely adjustable robust optimization
under SOS-convexity. `corpus/16_Chuong_Jeyakumar_Li_Woolnough_2021a.pdf`.

**[CJW21b]** Chuong, T. D., Jeyakumar, V., Li, G. and Woolnough, D. (2021b).
Exact SDPs for adjustable robust linear programs with box uncertainty under
separable quadratic decision rules. `corpus/17_Chuong_Jeyakumar_Li_Woolnough_2021b.pdf`.

**[CZ09]** Chen, X. and Zhang, Y. (2009). Uncertain linear programs: extended
affinely adjustable robust counterparts. *Operations Research* 57(6):1469--1482.
`corpus/03_Chen_Zhang_2009.pdf`.
Printed page = PDF page + 1468.

**[DH26]** Dai, L. and Ho, C. P. (2026). When is two-stage sample robust
optimization asymptotically optimal? A simple perspective. arXiv:2608.22999.
`corpus/intake/2608.22999.pdf`.

**[GTW20]** Georghiou, A., Tsoukalas, A. and Wiesemann, W. (2020). Robust
optimal control with a primal-dual lifting scheme. `corpus/23_Georghiou_Tsoukalas_Wiesemann_2020.pdf`.
PDF page cited with printed page.

**[GTW25]** Georghiou, A., Tsoukalas, A. and Wiesemann, W. (2025). On the
optimality of affine decision rules in two-stage distributionally robust
optimization. `corpus/24_Georghiou_Tsoukalas_Wiesemann_2025.pdf`.

**[HSR18]** Haddad-Sisakht, A. and Ryan, S. M. (2018). Conditions under which
adjustability lowers the cost of a robust linear program. *Annals of Operations
Research* 269:185--204. `corpus/08_HaddadSisakht_Ryan_2018.pdf`.
Printed page = PDF page + 184.

**[JLLLW22]** Jeyakumar, V., Lee, G. M., Lee, J. H., Li, G. and Woolnough, D.
(2022). Exact SOS reformulations for adjustable robust optimization with
separable polynomial decision rules. `corpus/18_Jeyakumar_etal_2022.pdf`.
Printed page = PDF page + 1362. Note a discrepancy internal to the paper: the
abstract reports degrees 1 to 15, Section 4 reports 1 to 12.

**[Kur25]** Kurtz, J. (2025). Bounding the optimal number of policies for robust
$K$-adaptability. arXiv:2409.12630v3. `corpus/intake/2409.12630.pdf`.

**[LS22]** Lu, H. and Sturt, B. (2022). On the sparsity of optimal linear decision
rules for a class of robust optimization problems with box uncertainty sets.
`corpus/tex_src/11_Lu_Sturt_2022/main_final.tex`.
Cited by TeX line number. Scope: parameter sparsity inside the LDR class, not
exactness.

**[MDH18]** Marandi, A. and den Hertog, D. (2018). When are static and adjustable
robust optimization problems with constraint-wise uncertainty equivalent?
*Mathematical Programming* 170:555--568. `corpus/09_Marandi_denHertog_2018.pdf`.

**[P1]** Lean theorem `l1_eq_max_sum_diff`, `Aroform.lean`, no `sorry`.

**[P2]** Lean theorem `info_value_monotone`, `Aroform.lean`, axiom-gated.

**[P3]** Lean theorem `one_d_exactness`, `Aroform.lean`, axiom-gated.

**[P4]** Lean theorem `blocks_sum_lower`, `TwoDDraft.lean`, no `sorry`;
transfer to `Aroform.lean` pending.

**[P5]** Lean theorem `full_upper_value` with `clamp_sat` and `sRunN`,
`TwoDDraft.lean`, no `sorry`.

**[S1]--[S6]** Judge artifacts: `artifacts/judge/attack_h-auto-2.txt`,
`attack_h-auto-4.txt`, `attack_h-auto-5.txt`, `attack_h-auto-7.txt`,
`attack_h-auto-8.txt`, `attack_h-auto-1.txt`, `attack_h-auto-3.txt`,
`attack_h-auto-6.txt`, `wedge.txt`, `ladder_exact.txt`. Status:
survived-falsifier, numerically certified, not proved. Details in
`docs/THESES.md` §3.

**[TSC22]** Tsang, M. Y., Shehadeh, K. S. and Curtis, F. E. (2022). An inexact
column-and-constraint generation method to solve two-stage robust optimization
problems. arXiv:2207.03291. `corpus/intake/2207.03291.pdf`. Scope: multiplicative error budgets for an inexact solver; contains no
statement about decision-rule exactness.

**[XB17]** Xu, G. and Burer, S. (2017). A copositive approach for two-stage
adjustable robust optimization with uncertain right-hand sides.
`corpus/tex_src/07_Xu_Burer_2017/arlp.tex`.
Cited by TeX line number; no journal pagination in the source.

**[ZDS18]** Zhen, J., den Hertog, D. and Sim, M. (2018). Adjustable robust
optimization via Fourier--Motzkin elimination. *Operations Research*.
`corpus/21_Zhen_denHertog_Sim_2018.pdf`.

**[ZST24]** Zhang, X., Sun, Y. and Teo, K. L. (2024). Exact semidefinite
programming reformulations for adjustable robust quadratic optimization with
affine decision rules. `corpus/19_Zhang_2024.pdf`.

**[ZZ13]** Zeng, B. and Zhao, L. (2013). Solving two-stage robust optimization
problems using a column-and-constraint generation method. *Operations Research
Letters* 41:457--461. `corpus/12_Zeng_Zhao_2013.pdf`.
Proofs of the three propositions are in an Electronic Companion not in the
corpus; statement-level anchors only.
