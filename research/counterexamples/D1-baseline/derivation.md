# D1: a bound-sensitive three-prefix obstruction

Question: `correlated-continuation-compatibility-v1`. Candidate: `D1-three-prefix-bound-sensitive-v1`. This is the ordinary strong-session attempt. No other attempt or continuation answer was accessed. The result is a source-grounded boundary construction, with no novelty or human-attestation claim.

The exact instance check exited 0 with 11 recorded cases. It establishes a three-prefix state cell whose continuation sets intersect pairwise at q=3/2 but not jointly. The signed objective is essential: hard terminal constraints alone are jointly feasible. Exact witness/certificate bounds give prefix optimum 1/4 and state optimum 2 for this instance. General statements below remain mathematical arguments, not machine-proved general theorems.

## 1. Claims and the three branches

- **D1-G1 v1**, branch 1: derive the fixed-recourse row-envelope representation and sufficient losslessness conditions. Status: self-contained, unformalized argument.
- **D1-P1 v1**, branch 2: proposed shortcut, “pairwise compatibility in a measured-state cell implies whole-cell compatibility.” Status: refuted by the exact instance **D1-E1 v1** below. Stop this parent on the certificate; do not search for more examples of the same failure.
- **D1-S1 v1**, branch 3: identify the role of the source's independently admissible block disturbances and test whether an apparent construction accidentally observes the suffix. The legal prefix program is robust over two suffixes sharing a prefix; an anticipative pathwise assignment is explicitly rejected. The source implication is an unformalized reconstruction, not a reproduction of the source's full closure recursion.

No parameter search was run. The direct construction has one candidate, four complete paths, three prefixes and two continuation coordinates. All branches close with the results and gaps stated here; no fourth branch is opened.

## 2. Expand the dynamics before compressing uncertainty

For t>=s, define Phi(t,s)=A_(t-1)...A_s, with Phi(s,s)=I. For a fixed first program a and prefix p, the measurement is z=z_a(p). Concatenate the second-block controls into b. Expanding one transition at a time gives

    x_T = Phi(T,r) z + L b + e(s),
    L = [Phi(T,r+1)B_r | ... | B_(T-1)],
    e(s) = sum_(t=r)^(T-1) Phi(T,t+1) E_t w_t.

This is a finite algebraic expansion: each step multiplies previous terms by A_t and adds B_t u_t and E_t w_t. No disturbance is observed during the second block. In particular b is the same for every s in S(p), not a function of s.

Let R have rows H followed by c^T. Set t(q)=(h,q-d0), and define the directional residual vector

    sigma_p,j = max_(s in S(p)) R_j e(s).

The maximum exists and is rational because S(p) is finite and nonempty. For a single row, “for all s, R_j L b <= t_j(q)-R_j Phi(T,r)z-R_j e(s)” is equivalent to

    R_j L b <= beta_p,j(a,q)
              = t_j(q)-R_j Phi(T,r)z_a(p)-sigma_p,j.

The maximum sign is important: a worst disturbance subtracts from the allowed right-hand side. Taking maxima separately for different rows does NOT add any complete path; a universal conjunction distributes over the existing path set. It does not justify replacing conditional S(p) by marginal suffixes, nor interchanging the choice of b with the universal suffix quantifier.

Thus **D1-G1** is the explicit common-matrix system

    K_p(a,q) = {b in V : R L b <= beta_p(a,q)}.

For a state cell C_z={p:z_a(p)=z}, define its row envelope

    beta_C,j = min_(p in C_z) beta_p,j
             = t_j(q)-R_j Phi(T,r)z-max_(p in C_z) sigma_p,j.

A state continuation for that cell exists exactly when the SINGLE system `b in V, R L b <= beta_C` is feasible. A prefix continuation exists exactly when every individual prefix system is feasible. There are finitely many prefixes/cells, so independently choosing one rational witness per nonempty system constructs the respective policy on its exact finite domain. This is a finite selection argument, not an assumption that every real solution is rational: the feasible sets are defined over rational b throughout.

This description identifies which residual directions matter for this fixed H and c. Full suffix-set equality is sufficient but stronger than equality of these directional residuals. Equality of residual signatures is not necessary for common feasibility at a given bound: in the checked instance the signatures differ, yet q=2 admits the common b=(1,1).

Two additional consequences, retained as unformalized arguments:

1. If each cell has a representative p* with beta_p* <= beta_p componentwise for every p in that cell, then its envelope equals beta_p*. Prefix feasibility therefore implies state feasibility. Equal signatures are a special case; a nested family can also suffice. If this dominance holds for every q (the q shift is common), it gives equality of bound-feasibility sets for the fixed a.
2. For k terminal rows plus one cost row, each coordinate minimum of beta_C is attained by a prefix. Choosing one such prefix per row gives at most k+1 prefixes whose joint system equals the full cell system, since the control box is common. This is a direct finite row-selection argument, not an invocation of a general convex-intersection theorem. It does not say pairwise testing suffices when k+1=3.

When the continuation has only one scalar coordinate, every nonempty K_p is a closed rational interval: each rational linear inequality is a half-line, all intersected with the bounded rational box. Pairwise compatibility then implies joint compatibility. Indeed choose the largest lower endpoint and smallest upper endpoint; their two intervals intersect, so the largest lower endpoint is at most the smallest upper endpoint. This proves a dimensional boundary in the prose model; it has not been formalized or exhaustively checked. The construction uses two coordinates and three active directional restrictions.

## 3. Frozen, dynamics-realizable construction

All data are exact rational strings in `checks/candidate-v1.json`. Let T=2, r=1, n=m=d=2, x_0=(0,0). Take

    A_0=A_1=I, B_0=E_0=0, B_1=E_1=I,
    U_0={(0,0)}, U_1=[0,2]^2 intersect Q^2,
    H=-I, h=(0,0), c=(1,1), d0=0.

Thus x_1=(0,0) on every path and x_2=b+w_1. The hard terminal constraints are x_2>=0. The cost is the signed sum x_2,1+x_2,2, bounded by q. It is not an absolute norm, even though feasible terminal states in this particular instance are nonnegative.

Keep exactly these four complete paths; no other pairing is admitted:

| Path | w_0 | w_1 | Prefix |
| --- | --- | --- | --- |
| A | (0,0) | (0,0) | p0 |
| B | (1,0) | (-1,0) | p1 |
| C | (1,0) | (-1,-1/4) | p1 |
| D | (0,1) | (0,-1) | p2 |

There are THREE different prefixes, all with measured state (0,0). Paths B and C have the SAME prefix and different suffixes. Consequently the prefix oracle has predictive information from correlations but does not know which of B/C nature selects. The first-stage singleton makes the fixed-a loss also a loss after optimizing over all admissible first programs in this particular instance.

E_0=0 deliberately erases physical prefix influence. It is allowed by the frozen question. The example isolates information about correlated future disturbances, rather than a nondegenerate observability theorem; no robustness under nonzero E_0 is claimed.

Write b=(u,v). Direct terminal substitution yields, with the common box omitted from the display only,

    K_p0(q): u>=0, v>=0, u+v<=q;
    K_p1(q): u>=1, v>=1/4, u+v<=q+1;
    K_p2(q): u>=0, v>=1, u+v<=q+1.

For p1, path C supplies v>=1/4 while path B supplies the tighter cost row u+v<=q+1. Combining their rows is valid because the SAME b must work for both paths. Treating these rows as if they belonged to separately selectable continuations would change the information model.

At q=3/2 every pair has a witness:

| Prefix pair | Common b | Costs on its paths in A,B,C,D order, omitting unrelated paths |
| --- | --- | --- |
| p0,p1 | (1,1/4) | 5/4, 1/4, 0 |
| p0,p2 | (0,1) | 1, 0 |
| p1,p2 | (1,1) | 1, 3/4, 1 |

Every listed terminal vector is nonnegative, and the programs lie in [0,2]^2. All three prefix systems are separately feasible; one legal policy is b_p0=(0,0), b_p1=(1,1/4), b_p2=(0,1), whose path costs are respectively 0,1/4,0,0.

But a state policy uses one b for all paths. The following actual path rows, with coefficient 1 on each, contradict q=3/2:

    B hard row 0:  -u       <= -1,
    D hard row 1:       -v  <= -1,
    A cost row:    u + v    <=  3/2.
    Sum:                   0 <= -1/2.

The multipliers are nonnegative. This establishes infeasibility over ALL rational controls in the continuous box, not just a finite action menu. The same arithmetic also excludes real controls, but the declared model and checked claim remain rational.

## 4. Bound sensitivity and exact optimal values

With the cost bound removed, b=(1,1) satisfies every hard constraint. Thus this is not a permanently hard-infeasible example with an ornamental nonzero objective.

Introduce a common epigraph variable tau for cost. The three rows above sum to `-tau<=-2`, so every state policy has worst cost at least 2. The common witness b=(1,1) has costs (2,1,3/4,1) and attains 2.

For prefix p1, combine path B hard row 0, path C hard row 1, and path B cost:

    -u <= -1, -v <= -1/4, u+v-tau <= 1
    imply -tau <= -1/4.

The legal prefix witness has worst cost 1/4. The other two prefixes attain zero. Therefore the global prefix optimum is 1/4, the state optimum is 2, and (because these witnesses work at any larger bound)

    B_pre(a) = {q in Q:q>=1/4},
    B_state(a) = {q in Q:q>=2}.

Both optima are attained in THIS example by explicit rational witnesses. This says nothing about general-model attainment. The bound q=3/2 is an interior separator, not an endpoint artifact.

## 5. Falsification and information-timing controls

The serious falsification target was **D1-P1**, not a generic picture of convex sets. The common-matrix geometry allows different prefixes to contribute the tightest rows in different directions. Three suffix translations produce the incompatible envelope u>=1, v>=1, u+v<=3/2 while every two-prefix envelope has a witness. The exact contradiction refutes the shortcut for the selected dynamics model; stop this branch.

Additional controls executed by the same candidate-specific code:

- A false common witness b=(1,0) is rejected: path D has negative second terminal coordinate.
- A negative certificate multiplier is rejected explicitly, without relying on Python `assert`.
- Reversing the objective sign changes the summed coefficient vector; the original lower-bound certificate no longer matches. The rejection concerns certificate validity, not the optimum of the mutated problem.
- An anticipative assignment uses b_B=(1,0) and b_C=(1,1/4). Each individual path then has cost zero and feasible terminal state, but B and C share a prefix. It is NOT an admissible prefix policy. The signature check rejects it.
- The legal common p1 program b=(1,1/4) has costs 1/4 and 0 on B/C; it fails q=0 and succeeds at q=1/4. Future w_1 was not observed.
- The legal prefix policy is rejected as a state policy because its three continuations differ at the same measured state.

No rectangular completion of W, convexification, finite action-menu approximation or external solver was used. The two routes are direct trajectory propagation and independently expanded affine rows plus exact nonnegative certificate sums. They are distinct computational routes in one authored script; independent F replay remains required and same-model agreement is not mathematical authority.

## 6. Source premises and nearest-result boundary

Source identities were checked against the frozen resource manifest before execution. Original page renderings actually read in D1: `research/sources/A4-p4.png` (A4 PDF p4, printed 69), and `research/sources/BT04-p5.png` (BT04 PDF p5, printed 355). PDF identities are A4 SHA-256 `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`, BT04 SHA-256 `3ff5e8479fac4326cd4369ac01cefc30fd468681fa4a99af846eb05a4db44f3a`.

A4 p4 defines each block's disturbances as all w_j(t) in W at its block times, with the same unconstrained block admissibility, and Assumption 1 measures x*(T_j) before selecting the program on Delta_j={T_j,...,T_(j+1)-1}. This directly anchors the timing used here. If complete-path admissibility is a product across the first/second blocks, then S(p) is the same suffix set for every p. For equal measured z, all sigma_p and beta_p coincide. Hence prefix bound-feasibility implies state bound-feasibility for each cell by D1-G1, for any fixed a and q. In the finite rational model this is an elementary sufficient condition. The source's continuous disturbance boxes are NOT turned into a finite set or given a new proof of its full dynamic-programming theorem here.

The counterexample deliberately violates blockwise independence. A measured state need not carry the predictive content of a hidden prefix when future disturbance support is conditional on that prefix. This does not refute A4, whose admissible-disturbance premise excludes these correlations.

BT04 p5 Theorem 2.2 displays an ARC LP with independent recourse v_l at the listed vertices under fixed recourse V_1=...=V_N. There is no displayed equality coupling recourse variables whose observations coincide. Our pairwise-versus-joint obstruction is within a specified smaller information class. It does not contradict that theorem, nor establish a new exact reformulation for fully adjustable robust optimization. The preceding text on p5 also warns that common uncertain parameters across constraints can separate ARC and RC. Neither generic adjustability nor correlation-induced differences are claimed as discoveries.

The supplied domain packet and closest-results map are preparation, not a previous solution to this candidate. D1 did not inspect all six PDFs or perform a novelty search. The glossary's specialized L1 bridge description is not used as A4's general model; no live glossary edit was made.

## 7. Remaining proof obligations and stopping

**Checked scope:** one four-path rational construction, complete pair/prefix witnesses, equal measured states, exact optimum and infeasibility certificates, and eleven positive/rejection cases. Inputs, code and command were frozen before the first and only candidate execution. See `checks/manifest.json`, `checks/execution.json` and the raw streams.

**Unproved/formal gaps:** D1-G1, its row-representative consequence and the scalar-interval boundary are prose arguments, not Lean proofs. No general completeness theorem for rational infeasibility certificates was assumed or proved. No statement of necessity for equal directional signatures or independently admissible blocks is claimed. Nondegenerate-prefix perturbations, useful minimal state augmentation for correlated path supports, and multiple later measurements are outside the checked example. Literature novelty remains unresolved.

**One discriminating outstanding obligation:** for the same frozen general model, prove in a fixed formal statement, or find a counterexample to, the following row-representative consequence: each cell's robust continuation system is completely determined by at most k+1 of its prefixes, one attaining the worst residual in each terminal/cost direction; common box rows require no extra prefix. The argument above handles finite maxima and shared response matrices, but a formalization must preserve rational domains, row signs and finite nonempty conditional suffix sets. Do not silently replace this by the weaker observation-factorization lemma.

Stop now: the pairwise shortcut has decisive counterevidence and the requested bound-sensitive consequence is checked. More copies of the same separating example would not sharpen the result. Optional Lean was not attempted; comparator remains blocked by the previously recorded uid-map denial and was not bypassed. No runtime failure occurred in the D1 scientific check.
