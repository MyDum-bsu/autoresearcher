# Physical availability at the single closure

## Frozen information and quantifiers

Authority: `research/question.md`, `goal/wave-1/question.md` and the wave-2 assignment. Fix rational model data, finite nonempty correlated complete-path set W, first program a, terminal hard task H,h and signed cost c,d0 before selecting continuation rules. For each rational q, the comparison is

* prefix oracle: `exists v:P->V, forall (p,s) in W: terminal_bounds(a,v(p),p,s,q)`;
* approved physical policy: `exists g:O_a->V, forall (p,s) in W: terminal_bounds(a,g(z_a(p)),p,s,q)`.

Nature selects a complete path after the policy is selected; the one exact x_r measurement precedes choice of the ENTIRE second block b. No subsequent measurement, correction or suffix knowledge is allowed. The prefix oracle is only a comparator. The actual closure input is `(z; a, model, W, H,h,c,d0,q)`, where only z varies as an observation. Knowing W is model knowledge, not knowing which path was selected. No observation history was supplied.

The task fixes a and compares feasibility for every rational q. Optimizing a, comparing only optimum numbers, implementing every prefix policy and uniformity over arbitrary terminal losses are different assertions. None follows merely from equality for one q. Nonempty boxes/path sets do not imply feasibility.

## Availability test (elementary audit criterion, not a contribution)

For any proposed prefix statistic tau(p), there is an implementation `f(z_a(p))=tau(p)` from the approved observation precisely when tau is constant on every reachable fibre

    C_a(z) = {p in P : z_a(p)=z}.

A varying statistic on one fibre demands hidden prefix information. A constant statistic can be tabulated by evaluating the known finite model over all prefixes; it adds no distinction beyond z. Computation from a SET of compatible prefixes does not identify the realized prefix. This factorization check is elementary specification analysis, not newly proved science.

## Candidate support data

With the inherited terminal propagation `x_T=Phi(T,r)z+Gb+eta(s)`, set `D=[H;c^T]`, `beta(q)=(h,q-d0)`, `L=DG`. For a known prefix, define

    rho_p,j = max_{s in S(p)} D_j eta(s),
    K_p(q) = {b in V : Lb <= beta(q)-D Phi(T,r)z_a(p)-rho_p}.

These are the inherited residual identities, not a new checked general theorem. `rho_p` uses S(p), not the full path realized after closure. Even this prefix-conditioned worst-case summary is not physically available unless it is constant on C_a(z). Availability is separate from correctness of the residual formula. Linear dynamics and exact state measurement do not imply an injective prefix-to-state map.

The physically computable set is instead

    S_a(z) = union_{p in C_a(z)} S(p),
    rho_bar_j(z) = max_{s in S_a(z)} D_j eta(s)
                = max_{p in C_a(z)} rho_p,j.

Every set is finite and nonempty for reachable z. This enumeration uses only a, model, W and z; it does not take independent marginal suffixes or fabricate a complete path. Different rows may attain their maxima on different paths: this is legitimate for separate universal linear inequalities and does not mean that those maxima form one realized path. No additional online observation is involved.

`rho_bar(z)` describes intersection of all K_p(q) in that cell, with a SINGLE common b. It does not implement separate prefix-dependent b choices. Equal rho across a cell is sufficient to make those residual systems equal; that equality is neither a novelty result nor a necessary condition for common feasibility of a particular bound. Different rho values alone do not certify incompatible continuations. The known wave-1 exact construction is diagnostic inherited evidence, not newly executed mathematical evidence in this audit.

A statistic that preserves more prefix distinctions than z cannot be computed from z alone. A statistic `t(z)` coarser than z may preserve this particular task if its cells still admit common actions; establishing useful minimality requires more than declaring equal residual LPs. No new sensor restriction or compressed representation theorem has been selected.

## Source correspondence

| Dimension | Approved model | IY original author report | WKR original author manuscript | DVM extended original |
|---|---|---|---|---|
| Uncertainty | fixed finite correlated COMPLETE paths, no Cartesian completion | sets of probability measures with stage/history product Assumption 1, p4 | fixed unknown transition kernel in parameter ambiguity set; s/(s,a) products, pp5–6 | independent primitives, history-dependent input-output functions, p3; one latent primitive can encode a whole correlated path without exposing it |
| Observation | only x_r at closure; known a/model/W | full current state and policies initially allowed history, pp3–4 | full online state/action history in general, p2; offline training history is separate, p3 | perfect observation/action recall p3; Pi must be sigma(M), p4 |
| Timing/action | choose all b before suffix; no further actions | repeated sequential decisions | repeated sequential decisions, possibly randomized | repeated decisions generally; one-decision specialization does not give more information |
| Domains | rational continuous box; finite rational path list | discrete/countable states and discrete actions, p3 | finite states/actions and real-valued ambiguity parameters, pp2,5–6 | bounded metric sets, nonnegative costs, regularity assumptions, p3 |
| Quantifiers | fixed a; exists physical policy, for all paths; every rational q | optimized worst expected reward over policies, pp4–7 | worst expected reward; stationary optimality under s-rectangularity and history-sensitive counterexample, pp8–10 | pointwise Q/V preservation for every available memory/action if Definition 1 holds, pp4–5 |
| What cannot be transferred | no oracle/history/sensor | Markov sufficiency without its model assumptions | history-dependent optimal action without history access | prefix-defined summary not computable from M; hard-feasibility/rational attainment without additional justification |

DVM's one-decision specialization uses Y_0=z and W_0=the complete latent path, with b as the single action. Constant later primitives do not alter correlations, and hidden W_0 is not an observation. At that decision M_0 contains only Y_0 and known constants. A proposed `sigma(M_0)=rho_p` must pass exactly the fibre test above. The source's standard partially observed STATE example cannot be applied to the physical x_r alone if that state discards predictive path information; a latent model state may be enlarged for analysis, but the measured state may not.

## Logical review and rejected inferences

* `tau is definable from a prefix, therefore observable from x_r` equivocates between model-defined and physically known information. Missing premise: tau factors through z_a. DVM Definition 1 explicitly requires a memory function.
* `the sources assume more/different information, therefore our claim is new` is unsupported; a source mismatch supplies no positive literature delta.
* `each prefix has some b, therefore one b works for its observed cell` changes `forall p exists b` to `exists b forall p`. Keep one common b before elimination.
* `the compressed optimum agrees, therefore every rational bound is feasible` can drop nonattainment and rational witness qualifications. Exact feasibility needs actual witnesses/certificates, not an infimum alone.
* `non-rectangularity can make history useful` is already in WKR Proposition 2.4. Reproducing that qualitative phenomenon with a new elementary example is not a justified substantive target.

These are logical/source criticisms, not mathematical or novelty verdicts. No machine proof, new separating construction or experimental judge was executed. This audit selects no proof target.
