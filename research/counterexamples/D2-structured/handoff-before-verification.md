# Self-contained D2 handoff: pairwise compatibility fails in rank two

Task `aro-discovery-k4t`, phase D2. This file is sufficient to reconstruct the outstanding obligation without the predecessor session. Work only in `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`; verify root/branch before writes. Siblings and live scientific state are read-only. No nested agents, tracker writes, installs, commits/pushes, new provider, private trials or human attestation. All scratch/subprocess TMPDIR/TMP/TEMP must be the real in-root directory `artifacts/campaign/tmp`; set PYTHONDONTWRITEBYTECODE=1. The coordinator owns workflow/tracking and final acceptance. Do not read `research/baseline/` or its phase answer to continue this structured line. Instructional separation is not a sandbox or blinding guarantee.

## 1. Exact problem and scope

Read `research/question.md`, `research/resource-manifest.json`, and this handoff first. The common question is `correlated-continuation-compatibility-v1`; its manifest v2 froze sources/tools before both attempts. Only the six PDFs A2/A3/A4/BT04/GTW20/GTW25 were in the paired-attempt pool. E may amend its own continuation source manifest explicitly if a genuinely new decisive source is needed, but must not overwrite this frozen pool. Comparator is blocked by `bwrap: setting up uid map: Permission denied`; no bypass. Lean 4.35.0-rc2 is optional only within inherited authorization; no D2 Lean proof exists.

Model: rational finite-horizon linear dynamics

    x_(t+1)=A_t x_t+B_t u_t+E_t w_t,

finite nonempty set W of COMPLETE correlated paths, nonempty closed bounded rational boxes U_t, fixed first-block program a through t=r-1. At time r measure x_r exactly, select the entire continuation b in V=product_(t>=r)U_t, THEN w_r acts; no further measurement. Prefix policy chooses b(p) for p=w_<r, and must use it for every suffix S(p) attached to that prefix. State policy chooses g(z_a(p)), where z_a(p)=x_r. Every original path must satisfy H x_T<=h and c^T x_T+d0<=q, with nonzero c. Nature selects a path after the policy has been selected. Do not replace W by a marginal product or let a prefix policy see an unobserved suffix.

For fixed a,q define K_p as continuations feasible for every suffix attached to p. Prefix feasibility is all K_p nonempty; state feasibility requires their intersection nonempty within each cell of equal z_a(p). This factorization alone was not the research target. The target was whether common-matrix dynamics can have a genuinely three-prefix incompatibility despite every pair being compatible.

General representation derived in `derivation.md` §2 (NOT formally proved):

    x_T=Phi(T,r)z_a(p)+G b+eta(s),
    G=[Phi(T,r+1)B_r|...|B_(T-1)],
    eta(s)=sum_(t>=r)Phi(T,t+1)E_t w_t.

Stack D=[H;c^T] and beta=(h,q-d0). Put rho_(p,i)=max_(s in S(p))D_i eta(s). Then K_p is the common box plus

    (D G)_i b <= beta_i-D_i Phi(T,r)z_a(p)-rho_(p,i).

On a state cell, only the RHS varies between prefixes. Equality of directional signatures rho suffices for equal residual systems and losslessness; it is not necessary for compatibility at a particular bound.

## 2. Actual checked result: reconstruct it directly

Frozen input: `research/structured/checks/instances.json`.
T=2,r=1,n=m=d=2,x_0=(0,0). A_0=B_0=E_0=A_1=0; B_1=E_1=I. U_0={(0,0)}, U_1=[0,2]^2 intersect Q^2. Thus x_1=0 and x_2=b+w_1. Exactly three paths:

    p1: w_0=(0,0), w_1=(-1,0)
    p2: w_0=(1,0), w_1=(0,-1)
    p3: w_0=(0,1), w_1=(0,0).

H=-I,h=0,c=(1,1),d0=0. All three distinct prefixes give the same measured state. The first stage is a singleton, so no first-stage reoptimization is hidden.

Writing b=(x,y), the residual systems, all with the same box, are

    K1(q): x>=1,y>=0,x+y<=q+1;
    K2(q): x>=0,y>=1,x+y<=q+1;
    K3(q): x>=0,y>=0,x+y<=q.

At q=1 the pair witnesses are K1/K2:(1,1), K1/K3:(1,0), K2/K3:(0,1). Joint infeasibility follows by summing -x<=-1 from p1, -y<=-1 from p2, x+y<=1 from p3, each with multiplier 1: 0<=-1. These are actual terminal/cost rows, not arbitrary unrelated convex sets. The common row matrix has rank two.

Prefix witnesses (1,0),(0,1),(0,0) respectively give zero terminal states and cost zero. Every feasible terminal state is nonnegative, so prefix worst cost cannot be negative. Joint state feasibility implies q>=2 by the same summed rows (0<=q-2), and the common witness (1,1) attains costs (1,1,2). Thus the explained instance bound sets are q>=0 versus q>=2. Executed code checks the exact witness data and affine certificate identities; it is not a general theorem prover. Without the cost bound, hard constraints alone are jointly feasible. This is a bound-sensitive obstruction.

At q=2 the common witness exists although RHS signatures are (-1,0,3),(0,-1,3),(0,0,2). This refutes necessity of signature equality for fixed-bound compatibility, not equality of complete bound sets.

Timing control: use only two paths with the SAME w_0=(0,0) and suffixes (-1,0),(0,-1). There is one prefix. Independent path actions (1,0),(0,1) attain cost zero but fail prefix consistency. One common legal action needs q>=1: sum the two hard rows and the first suffix's cost row to obtain 0<=q-1. At q=0 the exact certificate is 0<=-1; at q=1, (1,1) works. This prevents accidental revelation of w_r.

## 3. Evidence and what has NOT been checked

- `checks/trajectory_check.py`: direct rational propagation through both times, all pairs, prefix witnesses, measured-state equality, q=2 joint witness, false q=1 joint witness rejected exactly on p3, illegal suffix-dependent policy rejected.
- `checks/certificate_check.py`: independent scalar inequality construction bound to the precise matrices; exact joint/timing contradictions; reject missing-row certificate and negative multiplier; q=2 is not falsely refuted. Does not import the trajectory script or generated trajectory outputs.
- `checks/manifest.json`: frozen input/code hashes, four commands, expected controls and output paths. SHA-256 at execution: `14338c2aeb178dc155bfe6001ba0921d74d6e01356bd77bcec3c68344269e907`.
- `checks/run-observation.json`: actual argv, exits, times and output hashes. Both routes exited 0 normally AND under -O; each route's stdout was byte-identical across those modes. Four command observations, no retry.
- `checks/D2-trajectories.stdout.json` and `checks/D2-certificates.stdout.json`: inspect actual data, not only the words passed. Matching stderr files are retained even when empty.
- `results.json`: claim IDs, boundaries, final bindings and resource limitations. `verification.json` records final local checks if present; results.json explicitly lists it as the verification output.

No independently executed F review yet, no Lean theorem, no general rank-one proof, no generic LP-duality completeness result, no literature novelty assessment and no live scientific status. Do not promote a result from same-model criticism. Fresh D2 source reading was A4 PDF physical pp3–5 as layout text and rendered p4; its hash is in results.json and the common manifest. A4 p4's full disturbance-block availability is stronger than arbitrary correlated S(p), so the example does not refute the source. All other nearest-result comparisons are inherited C context, not newly verified in D2.

## 4. Preserved failed parents, children and negative knowledge

`D2-P1-v1`: universal pairwise-to-joint compatibility in the question model — refuted by D2-E1-v1 at q=1. Do not overwrite it with a restricted version.
`D2-P2-v1`: equality of residual signatures necessary for fixed-bound common feasibility — refuted at q=2.
`D2-C2-v1`: equal signatures suffice — general algebraic derivation only.
`D2-C3-v1`: unequal signatures may be compatible — checked instance consequence.
`D2-C1-v1`: rank-at-most-one common residual matrix restores pairwise sufficiency — unresolved child, NEXT OBLIGATION.

Do not infer common minimizers from equal values, joint compatibility from pairs, prefix knowledge from full paths, or all-q losslessness from q=2 compatibility. Do not infer box infeasibility by finite action enumeration. Printed A4 data and r=80 calculations were not used. No novelty follows from six sources not containing this exact example.

## 5. One new successor action, with a discriminating result

Precisely settle D2-C1-v1:

> For every fixed rational a,q in the question model, let L=D G include the hard and signed-cost rows. If rank_Q(L)<=1, then pairwise nonempty K_p intersections inside a state cell imply the entire cell intersection is nonempty over the rational control box.

Suggested proof route: factor nonzero rational L=v ell^T; project the common box to a rational scalar interval t=ell^T b; express each prefix's rows as bounds on t (including zero-row feasibility); prove finite pairwise interval intersection implies joint intersection; supply an explicit rational section t->b using convex interpolation of box endpoint maximizer/minimizer vectors. Handle singleton image/boxes, zero rows and empty residual systems. No external Helly theorem is needed if these steps are actually supplied. Rank-zero needs separate handling. If this fails, preserve the child and give a dynamics-realizable rank-one counterexample rather than substituting another research question.

The new result should be a completed scoped derivation and/or a new candidate-specific rank-one boundary control, not just rerunning the triangle checker. Record actual input paths, missing information and one new claim/check ID under `research/continuation/`; do not modify D2's frozen files. Independent review can later replay the D2 scripts with stdout captured to a NEW campaign-local output path. For replay, after verifying real in-root paths and exporting TMPDIR/TMP/TEMP and PYTHONDONTWRITEBYTECODE, run from the campaign root:

    timeout 30 python3 -B research/structured/checks/trajectory_check.py
    timeout 30 python3 -B research/structured/checks/certificate_check.py

Do not run the full final campaign validator before the coordinator has persisted synthesis. No repeated parameter search or new external source is needed merely to establish the interval implication.
