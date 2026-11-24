# D2: a bound-sensitive three-prefix obstruction with fixed recourse

Question `correlated-continuation-compatibility-v1`; task `aro-discovery-k4t`.
The exact construction below refutes pairwise compatibility as a universal shortcut in the frozen question model. All three prefixes have exactly the same measured state. Every pair admits a common continuation at bound 1, whereas all three together do not. The obstruction disappears at bound 2 and is not hard-constraint infeasibility.

Executed evidence: `checks/D2-trajectories.stdout.json`, `checks/D2-certificates.stdout.json`, their optimized-mode counterparts, and `checks/run-observation.json`. The manifest was frozen before execution. These are author-created, executed exact arithmetic checks, awaiting independent F replay. No Lean theorem, human correspondence approval, live status or literature novelty is claimed.

## 1. Premises, dependencies and source boundary

Use precisely the finite correlated-path model of `../question.md`: rational linear dynamics, nonempty rational control boxes, fixed first-block program a, one exact state measurement x_r, then an entire open-loop continuation selected before w_r. Prefix policies depend on w_<r, not on an arbitrary complete-path ID. Hard terminal constraints and the signed terminal cost bound apply to every original complete path. There is no implicit Cartesian completion.

Fresh source reading in D2: `../sources/A4-selected.txt`, physical PDF pages 3–5 (text), and `../sources/A4-p4.png` (rendered physical PDF page 4, printed 69). A4 PDF SHA-256 is `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`. PDF p3, (1.2)–(1.3), supplies terminal robust constraints and minimization of max c^T x(T). PDF p4 defines each disturbance block as all functions with w_j(t) in the same W, and Assumption 1 measures current state before choosing the block program. In particular the displayed fragment `wj (·) ∈ Wj` is a block-availability condition, not an assertion that any correlated finite path set is permitted. The rendering confirms that Delta_j begins at T_j.

The investigation below is our declared model variant, not an A4 theorem: time-varying rational E_t and a finite correlated complete-path set replace the source's fixed-matrix/timewise-box disturbance setting. The source's state-based continuation uses full block disturbance availability. Our example therefore does not contradict its recursion. The C packet's six-source comparison remains inherited context, not a fresh D2 reproof of those sources. The live glossary's L1-specialized V(R) is not used as the signed objective here; the reported glossary/source mismatch is left untouched.

Dependencies for the separating claim are only: the frozen matrices/paths/boxes; exact propagation and policy timing; terminal row arithmetic; explicit witnesses; soundness of summing valid inequalities with nonnegative coefficients. No general LP-duality completeness, compactness theorem, convex-hull interpolation or unavailable external theorem is needed for the contradiction.

## 2. Representation operator: residual rows rather than raw histories

**D2-R1-v1, general derivation, not machine-proved.** Write Phi(t,s)=A_(t-1)...A_s for t>s and Phi(s,s)=I. For fixed a, prefix p and continuation vector b=(u_r,...,u_(T-1)), repeated substitution gives

    x_T = Phi(T,r) z_a(p) + G b + eta(s),
    G = [Phi(T,r+1) B_r | ... | Phi(T,T) B_(T-1)],
    eta(s) = sum_(t=r)^(T-1) Phi(T,t+1) E_t w_t.

This follows by substituting x_(t+1)=A_t x_t+B_t u_t+E_t w_t into the next transition; the empty product for the final control is I. Thus the coefficient of every continuation control is common across prefixes. Let D be H with the additional final row c^T, and beta(q)=(h,q-d0). For each row i define the finite rational directional signature

    rho_(p,i) = max_(s in S(p)) D_i eta(s).

Because a vector inequality holds for every suffix exactly when each scalar row does, the precise residual system is

    K_p(a,q) = {b in V : (D G)_i b <= beta_i(q)
                                  - D_i Phi(T,r) z_a(p) - rho_(p,i), all i}.

No single suffix must maximize all rows simultaneously. Rowwise maxima here do not replace W by a Cartesian set: they express the conjunction of the original universal inequalities. Conversely, satisfying each displayed maximum dominates each original suffix inequality, proving the reverse implication. This is a direct algebraic argument, not a general proof checked by our two-period scripts.

On a measured-state cell C_z, all z_a(p)=z. Prefix feasibility is nonemptiness of every K_p; state feasibility requires one b satisfying all prefixes in the cell. Pooling those inequalities replaces rho_(p,i) by max_(p in C_z) rho_(p,i), equivalently taking the directional maxima over the union of conditional suffix sets. Equality of suffix sets inside each cell suffices for identical residual systems. Equality of their directional signatures already suffices and is weaker than literal equality of suffix sets. Therefore if these signatures agree on every state cell, prefix and state bound feasibility coincide, for every q at that fixed a. A finite number of cells permits choosing one feasible b for each nonempty common residual system. This proves the sufficient direction as a mathematical derivation only.

This identifies the source premise: rectangular prefix/suffix availability makes S(p) independent of p, so no hidden prefix changes the possible future disturbance block at a fixed measured state. Arbitrary correlated W need not have this property. Neither equality of signatures nor rectangularity is asserted necessary for compatibility in a fixed task.

## 3. Contradiction-first branch: preserve the failed universal parent

**D2-P1-v1, original parent (refuted):** for every admissible data tuple, fixed a, q and state cell, if K_p intersect pairwise, they intersect jointly.

A generic three-convex-set picture would not establish a counterexample in this model. The attack must realize all sets with the SAME continuation matrix, hard constraints, signed cost and control box. The construction uses translates of one triangle, with the cost row providing the third direction.

### 3.1 Exact dynamics and complete paths

**D2-E1-v1.** Take T=2, r=1, n=m=d=2, x_0=(0,0). At time 0 set A_0=B_0=E_0=0 and U_0={(0,0)}. At time 1 set A_1=0, B_1=E_1=I_2 and U_1=[0,2]^2 intersect Q^2. Thus

    x_1=(0,0),    x_2=b+w_1.

There are exactly three complete paths:

| Path/prefix ID | w_0 | w_1 |
| --- | --- | --- |
| p1 | (0,0) | (-1,0) |
| p2 | (1,0) | (0,-1) |
| p3 | (0,1) | (0,0) |

Each prefix is distinct; all measured states coincide. E_0=0 intentionally removes their state imprint. This is permitted by the question and models the prefix oracle as genuinely richer information; it is not a claim that a physical sensor observes these prefixes. Correlation makes each suffix determined by its prefix in THIS instance. That does not license pathwise decisions when several suffixes share a prefix; §5 attacks that mistake separately.

Set H=-I_2, h=(0,0), c=(1,1), d0=0. Hard terminal feasibility means x_2 has nonnegative components. The signed cost is x_(2,1)+x_(2,2), not an absolute norm. The first program is the only member of its box, so there is no unexamined first-stage optimization that might remove the loss.

### 3.2 Shared-row residual geometry

Write b=(x,y), keeping these continuation coordinates distinct from state notation. Direct substitution yields

    K1(q): x>=1, y>=0, x+y<=q+1, b in [0,2]^2;
    K2(q): x>=0, y>=1, x+y<=q+1, b in [0,2]^2;
    K3(q): x>=0, y>=0, x+y<=q,   b in [0,2]^2.

The common non-box row matrix is [(-1,0);(0,-1);(1,1)], of rank two. These are translations of a common triangle before intersection with the common box. In particular the example does not smuggle in prefix-dependent recourse matrices.

At q=1 every pair has a rational witness:

| Prefix set | Common b | Costs on its paths |
| --- | --- | --- |
| {p1,p2} | (1,1) | 1,1 |
| {p1,p3} | (1,0) | 0,1 |
| {p2,p3} | (0,1) | 0,1 |

The trajectory route verifies every row and box for every listed pair. The joint system contains the following ACTUAL path inequalities:

    p1 hard row 0: -x <= -1,
    p2 hard row 1: -y <= -1,
    p3 cost row:    x+y <= 1.

Their nonnegative multipliers (1,1,1) sum to 0<=-1. The certificate route verifies exact zero left coefficients and strictly negative right side. Hence no rational or real continuation can satisfy all three; no action-grid exhaustion is being mistaken for box infeasibility. This is a dynamics-realizable, genuinely three-prefix obstruction at a fixed bound. Stop P1 on this decisive certificate, retaining its original statement.

### 3.3 Bound sensitivity and instance value consequence

Prefix continuations b(p1)=(1,0), b(p2)=(0,1), b(p3)=(0,0) give terminal state zero on each original path, hence worst cost zero. Hard terminal nonnegativity and c=(1,1) imply no feasible path can have negative cost. The prefix bound set is therefore {q in Q:q>=0}.

For a state policy a single b must satisfy x>=1 and y>=1. On p3 its cost is x+y, so q>=2. The same three-row certificate, retaining q symbolically, sums to 0<=q-2. Its constant term and slope are checked through the exact affine row formula; the script does not sample q to infer nonlinearity away. At q=2 the common b=(1,1) satisfies every hard constraint and costs (1,1,2); the same b works for every q>=2. Thus the state bound set is {q in Q:q>=2}, with attained worst cost two. The general logical extension from the checked affine identity and constant witnesses is explained here; the scripts do not certify arbitrary theorems about rational optimization.

Without the cost bound, b=(1,1) satisfies ALL hard constraints. Thus this is a bound-sensitive information gap, not an objective-free terminal feasibility failure. At q=1, comparing only pairwise subproblems misses it.

## 4. Signature branch: refute necessity, retain distinct children

**D2-P2-v1, original strengthened parent (refuted):** if a state cell has a nonempty common continuation at a fixed q, its directional residual signatures must all be equal.

At q=2 the common witness above is feasible, although the three non-box residual RHS vectors are (-1,0,3), (0,-1,3), (0,0,2). Since the state and beta are common, different RHS vectors mean different directional signatures. The certificate route computes the differences and the trajectory route checks the same common witness. This refutes necessity for fixed-bound compatibility. It does NOT show equality of the complete prefix/state bound sets; §3.3 establishes their inequality for this instance.

Preserve separate children:

- **D2-C2-v1:** equal directional signatures inside each state cell suffice for equality of bound feasibility. Derivation in §2; unproved-sketch label because no general formal checker was executed.
- **D2-C3-v1:** unequal signatures may still be compatible at a particular bound. Exact construction at q=2; not a converse or a universal losslessness criterion.

Negative knowledge: signature equality is a sufficient representation criterion, not an equivalence test; unequal raw data do not automatically imply information loss at every bound.

## 5. Timing/correlation falsifier: prefix is not complete-path information

**D2-E2-v1.** Keep the same dynamics, boxes, H,h,c. Replace W by exactly two paths sharing w_0=(0,0), with w_1=(-1,0) and (0,-1). There is only ONE prefix and ONE observed state. Both legal policy classes must choose a SINGLE b before the unknown suffix.

At q=0 independent path decisions (1,0) and (0,1) each attain cost zero, but they are NOT a legal prefix policy. The trajectory checker verifies their local feasibility and explicitly rejects their failure to be constant on the shared prefix. For a legal b, the two hard rows imply x>=1,y>=1 while the first path's cost row gives x+y<=q+1. Their sum is 0<=q-1, so q=0 is impossible. The certificate route verifies 0<=-1. At q=1 the common b=(1,1) is feasible. This control distinguishes genuine correlation information from an illicit observation of w_r and detects a direction of modeling error that would fabricate a better value.

## 6. Weakened-premise child and successor obligation

**D2-C1-v1, unresolved child of P1:** fix a and q in the declared model. If L=D G, with D stacking hard and cost rows, has rank at most one over Q, then pairwise compatibility inside every state cell implies joint compatibility. For rank zero the residual constraints do not depend on b; the rank-one case must be addressed explicitly. This is a changed premise, not a silent repair of the refuted parent.

A plausible route is to factor a nonzero rational L as v ell^T, project the common rational box V to t=ell^T b, express each prefix system as an interval in t, and construct a rational b from a common rational t. The missing obligation is a complete rational interval/section argument covering zero coefficients, singleton boxes, empty intervals and the possibility that an entire prefix system is infeasible. It must not assume a Helly theorem from memory or infer a theorem from our rank-two counterexample. No rank-one checker or formal proof was executed in D2. The triangle establishes that rank two can fail; it does not prove rank one cannot fail.

This is a concrete NEW continuation opportunity: finish the rational projection argument or produce a rank-one counterexample, preferably adding a small independently executed rank-one boundary control. Replaying D2's triangle outputs alone does not resolve it. The more ambitious general bound on how many prefixes can witness incompatibility is not pursued and is not needed by this handoff.

## 7. Logical and evidence audit

- Quantifiers preserved: one b per original prefix versus one per state cell; every original suffix remains universally quantified. In E2 these classes coincide, unlike clairvoyant path assignments.
- No composition inference: compatibility of pairs is the refuted proposition, not a proof step.
- The single first-stage choice prevents fixed-a loss from being overstated as a loss after a different a is optimized.
- Exact certificates prove impossibility over continuous rational boxes, not merely over a sampled menu. No general certificate-completeness assertion is used.
- Checked arithmetic and proposed general arguments have distinct claim IDs and labels. Same-model reasoning is not an additional scientific verdict.
- No search or new literature was needed after the explicit construction. Three branches are recorded in research-plan.md; P1/P2 stop at counterevidence, C1 remains unresolved for the successor. No finite survival or literature priority claim is made.
