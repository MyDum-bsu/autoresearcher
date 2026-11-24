# Domain packet: correlated continuations after one state measurement

Task aro-discovery-k4t, phase C. Read this file with `question.md`, `closest-results.md` and `resource-manifest.json`. This packet supports a bounded boundary investigation; it does not certify a new theorem. No scientific status, corpus entry or human attestation is created.

## 1. Reading scope and provenance

Six original PDFs were copied byte-for-byte from this worktree's corpus into `research/sources/`: A2 (2018), A3 (2021), A4 (2022), BT04 (2004), GTW20 (2020), GTW25 (June 6, 2025 version). `copy-provenance.json` records absolute original paths, relative copy paths, byte sizes and SHA-256. The resource manifest additionally binds these identities, selected extracts and page renderings. The originals remain unchanged; these local copies are not admission of new literature to the live corpus.

PDF pages throughout are ONE-BASED physical PDF pages. Printed page labels differ: A4 PDF 2 is printed 67; A3 PDF 4 is printed 41; BT04 PDF 5 is printed 355; GTW20 PDF 4 is printed 575. Source statements below are attributed to the printed authors, not independently re-proved in C.

Read scope:

| Source | Original pages actually inspected as layout text | Rendered pages actually inspected | Purpose |
| --- | --- | --- | --- |
| A4 | 2–6, 12 | 2, 4, 12 | dynamics, boxes, signed terminal objective, blockwise disturbances, closure recursion, printed Example 1 |
| A2 | 2–4 | none | continuous-time/sampled-control model, single-measurement signature, terminal feasibility; no numerical example imported |
| A3 | 2–4, 7–9 | 4 | discrete analogue, exact timing, approximation/rank context, Example 1 polarity |
| BT04 | 3–6 | 5 | information basis, ARC versus RC quantifiers, constraint-wise equivalence assumptions, fixed-recourse vertex theorem |
| GTW20 | 1–4 | 4 | fully observed second-stage parameter, fixed recourse, extreme-point interpolation, random-recourse failure |
| GTW25 | 1–9 | 7 | DRO model, monotonic risk, affine-rule conditions, attained-optimum versus feasible-set scope |

Whole-PDF text extraction is preparation, not a claim of whole-PDF reading. Full copies are in the common pool so either following attempt can inspect other pages of these SAME sources. No web discovery pass or additional primary source was used. Consequently, a comprehensive novelty assessment has NOT occurred. A5 and the 2023 temporary-cache lead were not needed to define this narrower objective and are not silently available as extra research sources during the paired attempts.

A2's layout extraction visibly loses some absolute-value bars and a negation in the paragraph surrounding J1 outside its feasible domain. This packet does not use those corrupted expressions as mathematical premises. Use A2 only for the explicit measurement/continuation signature and model mismatch listed below; consult the original PDF before any stronger transfer. A3's extracted mathematical symbols also contain font substitutions. The selected A3 p4 rendering resolves the continuation timing; no rank theorem is imported into our argument.

## 2. Source-premise map with literal anchors

The following short excerpts are literal layout-text fragments; selected-page files retain their context. `resource-manifest.json` binds each anchor to its source hash and page. Line wrapping is part of the extract, not a new mathematical notation.

### A4: discrete robust terminal control, not a finite correlated-path theorem

- `A4-model`, `sources/A4.pdf`, PDF p2, Eq. (1.1): `x(t + 1) = Ax(t) + Bu(t) + M w(t)`. The displayed U is a control box and W is an infinity-norm disturbance box, available at every t. It is NOT a finite set of complete paths. State/control/disturbance dimensions are unrestricted in this source model; A=I and an L1 terminal cost are not its general assumptions.
- `A4-polarity`, PDF p3, Eqs. (1.2)–(1.3): `при минимуме гарантированного значения линейного терминального критерия качества`, followed by `max c⊤ x(T |x0 , u, w)`. This supports minimization of worst signed terminal linear cost subject to robust terminal constraints, not a universal nonnegative absolute-cost convention.
- `A4-timing`, PDF p4, Assumption 1: `измерить текущее состояние`, then choose a new program on the block starting at the measurement time. Rendering p4 shows Delta_j starts at T_j and ends at T_(j+1)-1. Hence x_(T_j) is measured before applying the control at T_j and the disturbance driving the next transition. There is no new measurement inside that block.
- `A4-blocks`, PDF p4: `wj (·) ∈ Wj`, with Wj defined by wj(t) in the same W at every block time. These are all admissible block functions, with no supplied cross-block correlation restriction. This is the decisive premise that cannot silently be carried to an arbitrary finite correlated W.
- `A4-recursion`, PDF pp5–6, Eqs. (2.4)–(2.8): closure sets contain states from which some open-loop block robustly reaches the next closure set; the source expressly assumes these sets nonempty. PDF p6 has `Vj (xj ) = min max` and separately defines +infinity when a subproblem has no solution. Neither that existence assumption nor extended-value encoding is imposed on this campaign's Boolean bound predicate.
- `A4-example`, PDF p12, Example 1: `x2 (T ) → max`. The rendered printed matrix is [0.9950,0.0998;-0.0998,0.9950] and B=M=[0.0050,0.0998]^T, with x0=[0,1]^T. T=120, the displayed terminal strip uses lower 2 and upper 10. These are printed decimals, not a claim of unrounded continuous-time coefficients. The table includes T1=80 and 2.754215; this is a reported value for that source's construction, not a reproduced exact optimum here. No r=80 computation or transfer is proposed.

### A2/A3: which details survive the bridge

- `A2-timing`, `sources/A2.pdf`, PDF p2, end of model section: `с учетом полученного измерения состояния`. PDF p3 defines pi1 by an initial program and a program indexed by reachable x1; it requires robust terminal inclusion for each reachable x1. This confirms the signature, not equality to prefix-observing ARO. The source is continuous-time, time-varying, scalar-control and sampled-control, with a total-control-impulse objective, unlike our rational discrete terminal-linear model.
- `A2-feasibility`, PDF p3: `Стратегия π1 называется допустимой стратегией управления с моментом замыкания t1, если`; see (1.4) immediately below. Its later closure-set assumptions must not be mistaken for automatic feasibility of arbitrary data.
- `A3-timing`, `sources/A3.pdf`, PDF p4: `measure exactly the current state`, followed by choice of u1 on D1. Eq. (7) is min over the whole second-block program, max over a block disturbance. Its disturbance block is not conditioned on an observed hidden prefix from a correlated finite-path set.
- `A3-geometry`, PDF pp7–8: `piecewise affine and concave`; the text changes the approximation representation in a different rank regime and explicitly discusses increased dimension. This is motivation for changing representations, not evidence for exactness of our row/signature proposal.
- `A3-example`, PDF p9: `closing instant T1 = 80`. The example maximizes x2(T), despite the general minimization convention earlier. Keep this sign change explicit. Do not replace the printed decimals with reconstructed coefficients or infer the campaign's answer from the example.

### BT04: information classes and quantifier order are already known

- `BT04-information`, `sources/BT04.pdf`, PDF p3: `every variable` and, on the following line, `may have its own information basis`. The paper explicitly allows dependence on a prescribed portion of true data. Generic adjustability is not a new idea here.
- `BT04-ARC-RC`, PDF p3, (5)–(6): ARC fixes the first-stage vector and uses forall uncertain data, exists recourse; RC uses exists recourse, forall uncertain data. Objective normalization introduces a first-stage epigraph variable. Neither displayed formula by itself permits observation of an unobserved suffix in our model.
- `BT04-equivalence`, PDF pp4–5, Thm 2.1: `The uncertainty is constraint-wise`, a product of nonempty convex compact row-uncertainty sets, plus a compact set containing all feasible recourse for each feasible first-stage decision. This is a genuine existing sufficient condition for static/adjustable equivalence. Cross-row/cross-time correlated uncertainty and a restricted observation map do not meet it merely by being finite or bounded.
- `BT04-vertices`, PDF p5, Thm 2.2: `V1 = ... = VN of fixed recourse`. A convex-hull uncertainty description permits one recourse block per listed vertex in the stated fully adjustable model. Equal-state coupling between those blocks is not one of the displayed LP constraints. Dropping that coupling changes the information class.

### GTW20/GTW25: precise nearest reformulations, different information promises

- `GTW20-model`, `sources/GTW20.pdf`, PDF p1: `second-stage policy`, with y:Xi->R^n2 adapting to the realization of xi; Xi is a nonempty bounded polyhedron and recourse matrix W is fixed. Cost epigraph normalization is allowed. Our W denotes a path set; it is not that paper's recourse matrix W.
- `GTW20-vertices`, PDF pp3–4, Prop. 1: `Problems` and `are equivalent in the following sense`, followed by feasible-solution transformation with the same objective. Its proof interpolates vertex recourse using convex-combination coefficients depending on the FULL xi. This proves an exact reformulation in its model, not implementability under our smaller state information. A finite-path model and a polyhedral hull are also distinct uncertainty domains.
- `GTW20-random`, PDF p4: `does not hold if problem` and the following line's `random recourse`. The displayed xi*y(xi)>=1 on [-1,1] fails at xi=0. Our proposed matrix model retains fixed recourse; this existing counterexample cannot be passed off as its separating example.
- `GTW25-model`, `sources/GTW25.pdf`, PDF p6, (1): fixed recourse B,D; distributionally robust risk over a support; Q is optimized separately at xi. PDF p7 expressly assumes monotonic risk before an interchange of supremum and policy minimization. We have no probability model or risk interchange.
- `GTW25-condition`, PDF pp7–8: conditions F (monotone recourse objective), A (affine A,g), D (nonnegative upper-bound matrix), B (equivalent subset of n2 lower inequalities with invertible matrix having a positive inverse), at an optimal first-stage choice.
- `GTW25-theorem`, PDF p8, Thm 1: `Assume that problem (1) attains its optimal value`. It concludes optimal-value equality with affine rules under the listed conditions. The next paragraph limits the conclusion to optimal decisions rather than all feasible solutions; PDF p9 notes the nonattainment limitation. This does not identify the full xi with an observed x_r, or prove equality of all bound-feasibility sets.

## 3. Campaign definitions and dependency closure

`question.md` is authoritative for the selected model. Its new symbols (P, S(p), O_a, K_p(a,q)) are local packet definitions, not changes to the live glossary. Use closure moment and fixed recourse in their established senses. Use explicit `F_pre`/`F_state` rather than the live glossary's V(R), whose L1-specialized notation would conceal the signed objective here.

Dependency chain for a valid construction:

1. rational data and complete W -> exact first-block trajectories -> prefix-to-state cells;
2. each ORIGINAL prefix and its attached suffix set -> terminal trajectories under one common block program;
3. actual control box, H/h and signed bound -> residual inequalities for that prefix;
4. actual state cell -> joint constraints on a SINGLE continuation, not independent path decisions;
5. explicit rational witnesses/certificates -> a finite claim, with its q and fixed a;
6. only a separate quantified argument can extend this to other a, other bounds or a general statement.

The suggested directional residual representation must be DERIVED from these steps. It is not a new theorem cited from a PDF. A contradiction certificate is sound if its checked nonnegative combination produces 0<=a strictly negative rational; this is an elementary arithmetic check the following attempts can implement, not an assertion of a complete general LP duality theorem without proof.

## 4. Existing exact evidence and its limits

Read B's `artifacts/campaign/tool-spike/finite-controls.json`: campaign-positive has state/prefix value 0 and open value 1; campaign-infeasible is typed infeasible in all modes; a tampered value was rejected. Those are HISTORICAL B observations in the scalar finite-action absolute-cost schema. C has not re-executed them. The imported README contracts and B import-provenance file are included in the common pool with hashes. P1 full policy enumeration and P2 Bellman `check_result` are two implementations of that schema; replay alone does not establish optimality or infeasibility.

This model's equality/loss boundary is not settled by those numbers. Neither module accepts arbitrary matrix dynamics, continuous rational boxes or signed terminal linear objectives. Their test-only finite menus cannot establish impossibility over all rationals in a box.

B recorded Lean toy compilation and exact finite controls, but the native comparator stopped at `bwrap: setting up uid map: Permission denied`. Wrong-target, dependent-definition and forbidden-axiom native controls did not run. Never bypass the sandbox or call the current scientific question formally verified because an unrelated Lean fixture compiled. B's reproduced TLC checks are protocol-model evidence only; TLC is not a mathematical evaluator for this question.

The upstream proposed single-measurement statement, copied with provenance into `sources/single-measurement-statement.md`, asserts equivalence to scenario assignments ALREADY constant on observation cells. It does not assert equality with the genuinely richer prefix class selected here. It remains proposed, not human approved. This distinction prevents proving the elementary statement and reporting it as the requested boundary result.

## 5. Negative knowledge and stop conditions

- Injectivity of p->x_r lets every prefix assignment be implemented, but is not the desired endpoint or a claimed open problem.
- Correlated paths cannot be replaced by prefix/suffix marginal products. Pooling a state cell unions the suffix possibilities attached to its prefixes; it does not grant the controller knowledge of the realized suffix.
- Lossless for one bound/task, lossless for all q for fixed a, lossless after optimizing a, and implementability of every policy are different quantifier patterns.
- A claim that pairwise continuation compatibility implies whole-cell compatibility needs proof in the ACTUAL shared-matrix geometry. A generic picture of unrelated convex sets is not a dynamics-realizable example.
- The scalar finite-action model and continuous rational boxes have different feasible sets. B's green regressions cannot validate a matrix claim by relabeling fields.
- Printed A4 coefficients, reconstructed decimals and an exact discretization are distinct inputs. No literature-optimum reproduction is attempted.
- The glossary's description of its narrow bridge class as A4 model (1.1) conflicts with the general equation and terminal-linear source pages read here. Report this legacy/source mismatch; do not edit the glossary or silently use its specialized L1 model.

Stop a candidate on a decisive counterexample or source closure. If a needed theorem is absent from this common pool, either supply a self-contained mathematical derivation with honest proof status or stop that inference; no memory citation. No novelty claim follows from the absence of a matching statement in these selected pages. The chosen reconstruction remains useful without novelty because it tests precisely which information assumption an OGU/ARO transfer needs.

## 6. Handoff use

Both attempts may inspect the same six PDFs and frozen local artifacts. Follow `question.md` for expected outputs, certificate checks and limits. Preserve failed constructions. A successor needs one exact remaining obligation and evidence locations, not this packet retold as a successful derivation. No answer from either attempt is present in this common pool.
