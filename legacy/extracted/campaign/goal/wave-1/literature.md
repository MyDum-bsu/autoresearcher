# G3 original-source audit: compatibility geometry is not yet a contribution

Task `aro-discovery-k4t`; goal wave 1. Disposition: completed source audit with no actionable research target. `actionableTarget=false`. This is an authorial source comparison, not a scientific or novelty verdict. The first-success goal is not achieved by this audit.

## Scope and preserved history

The workspace root and branch were checked before writes: `<workspace>/aro-discovery-campaign`, `task/aro-discovery-k4t-campaign`. The goal specification, FOUNDATION, AGENTS, glossary, campaign question/resource-source pool, coordinator handoff, campaign/Astra outcome reports, roadmap, E derivation and Astra derivation were read. Existing campaign/Astra outputs and the cancelled parent were not edited or resumed. G2's recovered engineering observations do not establish a scientific result and do not block this reading task.

The four required files were persisted before the final comparison. Their initial selection records remain under `selection-record-*`; the final files do not retroactively authorize a proof attempt. Only one research-target selection was assessed. A second selection was not justified by the inspected sources and was not spent on a renamed elementary variant.

## Exact model being compared

The model is `research/question.md`, not the full-information ARC model. Fix the first program a, rational cost bound q, one exact state observation at r, and finite correlated COMPLETE disturbance paths W. One entire continuation b is chosen after observing x_r and before any suffix disturbance is revealed; there are no subsequent observations. Preserve all actual conditional suffix sets S(p). The common continuation box V is closed, bounded, nonempty and rational. Hard terminal rows and the signed linear cost are fixed across prefixes.

The inherited substitution argument gives K_p={b in V:L b<=d_p}, L=DG, D=[H;c^T], with d_p containing rowwise maxima over the actual S(p). State feasibility requires a common b for all prefixes in each equal-state cell; prefix feasibility requires individual nonemptiness. This substitution is an inherited informal derivation, not a freshly checked general proof. Neither rowwise maximization nor comparison with a convex source licenses Cartesian completion of W or a suffix-dependent policy.

## Original PDF anchors inspected in this assignment

Physical PDF pages are one-indexed. SHA-256 and paths are in `source-manifest.json`. TXT extracts were made directly from the PDFs in this worktree, not treated as independent sources. A4 PDF p4 was also visually inspected from a new render. The other mathematical readings used direct layout-preserving PDF extraction; no visual inspection of those pages is claimed.

### S1. Ben-Tal, Goryashko, Guslitzer, Nemirovski (2004)

Original `research/sources/BT04.pdf`, PDF pp3–5, printed pp353–355.

- PDF p3: “every variable ... may have its own information basis”, and equations (5)/(6) explicitly distinguish forall-data/exists-recourse from exists-recourse/forall-data.
- PDF pp4–5, Theorem 2.1: constraint-wise non-overlapping uncertainty blocks, Z=Z1×...×Zm with convex compact factors; bounded feasible recourse in a compact V_u. Conclusion: RC and ARC equivalent.
- PDF p5, Theorem 2.2: uncertainty is a convex hull of finitely listed data and recourse matrix is common; independent v_l blocks give an exact LP.

Comparison: restricted information and quantifier order are established concepts. The campaign has a finite correlated path list and a common decision within each measured-state cell, not independent recourse after full path revelation. Compact V alone does not establish Theorem 2.1's row-independent product uncertainty. The theorem's product is a product of uncertain DATA blocks, not Astra's product of ACTION intervals. Confusing these two products would change the premise.

### S2. Dmitruk (2022), multiple closure strategies

Original `research/sources/A4.pdf`, PDF pp2–4, printed pp67–69; newly extracted context continues to p6.

- PDF p2, (1.1): x(t+1)=Ax(t)+Bu(t)+Mw(t), box control and pointwise box disturbance.
- PDF p3, (1.2)/(1.3): guaranteed terminal inclusion and worst linear terminal cost. Directional worst-disturbance bounds and tightened terminal rows are already used in (1.4)/(1.5).
- PDF p4: W_j consists of all blockwise disturbances w_j(t) in W. Assumption 1 permits measuring the current state at T_j and choosing the new entire program on that block from that measurement. Literal anchor: “в зависимости от измеренного ... выбрать новое управление”.

Comparison: timing matches the campaign's one-closure specialization. Availability of all blockwise disturbances differs from a prefix-conditioned finite suffix set. The old state-merging examples use correlation that this source's block availability does not model. They therefore do not refute the source. Directional residual bounds are also not, by themselves, a new bridge contribution. The source has real-valued stationary dynamics; the campaign allows rational time-dependent matrices. No theorem covering that extension is asserted here.

### S3. De Loera, La Haye, Oliveros, Roldán-Pensado, *Helly numbers of algebraic subsets of R^d*

Downloaded original research preprint `https://arxiv.org/pdf/1508.02380`; local filename `goal/wave-1/sources/helly-survey.pdf` is retained for identity continuity, but the document is an original research article, NOT a survey. PDF pp1–4 read in bounded extracts; the decisive anchors are pp1–3.

- PDF p1 introduction: finite convex families in R^d have the d+1-subfamily intersection criterion.
- PDF p2, after definition (1.1): “if F is any subfield of R ... the S-Helly number of S=F^d is still d+1.” This includes F=Q, so a claimed new rational-domain d+1 bound would not avoid the classical result.
- PDF p3: for d=1 and any subset S of R the Helly number is at most two. Thus interval pairwise-to-joint behavior is explicitly background here.
- PDF p4, Lemma 2.3, reports Hoffman's general characterization and cites the original. That original was NOT inspected; do not import its detailed statement as a freshly audited fixed-normal theorem.

Comparison: campaign K_p are convex polyhedra restricted to Q^N. The ordinary N+1 upper bound, including individual/small subfamily feasibility when the family has fewer members, is established background. Applying the result to the rational image L(V) in rank(L) coordinates is a natural reconstructed rank-based refinement, not a new contribution or a checked theorem from this worker. Astra's coordinate boxes form a smaller class than arbitrary convex sets: assembling coordinate intervals is elementary and yields pairwise sufficiency even at rank two. It does not contradict the d+1 statement or prove rank-two sufficiency generally. The inherited triangle is precisely the kind of obstruction the general convex criterion allows.

Historical originals Helly/Radon/Hoffman and a dedicated fixed-normal positive-circuit classification were not obtained/read. This limits claims of complete literature coverage. The already explicit subfield and one-dimensional statements suffice to reject these elementary mechanisms as first-success targets; they do not certify all remaining geometry as known.

### S4. Zhen, den Hertog, Sim (2018), *Adjustable Robust Optimization via Fourier–Motzkin Elimination*

Original local author manuscript `corpus/21_Zhen_denHertog_Sim_2018.pdf`, with a ResearchGate cover page. PDF pp6–8 = manuscript pp5–7; context PDF pp2–10 was extracted, and pp4–8 read.

- PDF p6, equations (1)/(2): common recourse B, y(z) chosen after z is revealed, affine technology/RHS.
- PDF p7, Algorithm 1 and Theorem 1: divide rows according to the sign of the eliminated coefficient; keep zero rows and all lower/upper comparisons. Exact conclusion X=X_{\{l}}.
- PDF p8: reconstruct the eliminated variable between the maximum lower and minimum upper bound; repeated elimination gives an equivalent static reformulation. The authors explicitly warn of quadratic growth per elimination.

Comparison: a proposal merely to eliminate a fixed-normal residual LP, or to pair its lower/upper bounds, overlaps an explicit existing exact method. To use it for the campaign, first stack ALL prefix rows sharing one state and retain ONE common continuation variable. Applying the full-information formula separately to complete paths would grant forbidden suffix information. The stacking and subsequent elimination are a model translation, not a demonstrated literature delta. This source does not, in the inspected theorem, give a sharp minimum number of DISTINCT PREFIX GROUPS in an infeasible subsystem for a specified fixed L and shared box. That absence from one theorem is not evidence that the grouped problem is open. No unaudited positive-circuit theorem is attributed to these authors.

### S5. Marandi and den Hertog (2018), *When are static and adjustable robust optimization problems with constraint-wise uncertainty equivalent?*

Original `corpus/09_Marandi_denHertog_2018.pdf`, PDF pp1,4–6, printed pp555,558–560, plus context pp2–3 and p7.

- PDF p4: adjustable/static definitions retain distinct quantifier orders.
- PDF p5, Definitions 3/4 and Assumptions i–vii: separable fixed recourse, product constraint-wise uncertainty, compact/convex uncertainty, compact/convex Y(x), concavity in uncertainty and convexity in recourse, no uncertain equality constraints.
- PDF p6, Theorem 1: Opt(RC)=Opt(ARC) under those assumptions.

Comparison: this is a stronger nonlinear sufficient result than merely citing the 2004 linear theorem. Its conclusion is equality of worst-case objective values, not implementation of every full-information policy. A correlated finite W, or the vector of conditional directional residuals indexed by prefixes in a cell, need not have convex product uncertainty. The campaign cannot infer losslessness from compactness, fixed normals or a shared box. Conversely it cannot claim a new sufficient principle by silently reinstating this source's product/convex premises. Conditional application on each cell would require proving those exact premises for the induced model, rather than treating prefix labels as independent uncertain coordinates.

## Target selection 1: fixed-normal compatibility / Helly refinement

Proposed scope: a finite-family criterion for K_p with common L and box V, improving rank-only pairwise heuristics and covering Astra's box subclass.

Decision: DO NOT SELECT FOR G4. Interval/product compatibility is elementary background. A general dimension/rank Helly bound is background. Generic exact elimination is already available in S4. A sharper grouped obstruction formula might be useful, but this audit has neither an inspected closest fixed-normal classification nor a nontrivial dynamics-restricted delta. Merely naming positive circuits is not an obligation with justified novelty. No theorem attempt, finite search, certificate experiment or Lean run was performed in G3.

This is a source closure of the proposed elementary success route, not a declaration that every possible fixed-normal theorem is known. The rank-one correction's individual-nonemptiness premise remains important for the inherited statements; it does not create novelty.

## Unselected second slot and concrete next discriminating lead

Read the ORIGINAL partial-observation/set-valued-information robust-control results for correlated disturbance histories, not another intersection proof. The exact discrimination is whether the task-specific sufficient statistic (measured x_r plus only terminal-relevant conditional directional support data) is already covered by an information-state/sufficient-statistic theorem. Compare preservation of robust BOUND FEASIBILITY for fixed a and every rational q, not only an optimal value, and distinguish a fixed terminal task from uniformity over all terminal losses.

A useful packet would need an original theorem about correlated uncertainty and restricted information, with a concrete map from its information state to this model. None was acquired here. The next source action is to follow S5 PDF p5's rectangularity references [18,21] into the original robust dynamic-programming papers and inspect what statistic is required when rectangularity fails; retrieve those originals before selecting a claim. Their identities/theorems are not supplied from memory. If they already imply the terminal-support statistic result, close that route as a reconstruction too. If they do not, the next worker must identify the exact extra hypothesis or a dynamics-realizable separation before spending Astra. Arbitrary relabeling of prefixes or generic hypergraph coloring alone would again be elementary.

## Search, evidence and limitations

Two Searcharvester queries returned empty tool results, not evidence of an empty literature. An arXiv API query for “fixed normals” returned noisy matches, including unrelated fixed-normal-load physics; it establishes no absence claim. The useful additional original PDF was fetched once by curl. No provider fallback or retry was used. Original source acquisition and safe local PDF extraction continued despite comparator restrictions; no comparator was rerun or bypassed.

A4's image was checked for observation ordering and blockwise disturbance domains. The source manifest binds source bytes, exact page scopes, extracted context and prior inputs. New artifact validation checks binding/completeness only, not mathematical truth. Inherited exact finite results remain inherited exact finite evidence; E/Astra general arguments remain informal; no general Lean proof exists in this G3 output. Logical audit kept pairwise feasibility separate from singleton feasibility, information products separate from action products, fixed-a bound feasibility separate from optimized values, and a missing source separate from a false theorem.

Not run: new mathematical checks, source theorem reproduction, Lean/comparator, live admission, tracker changes, attestation, commits or push. No scientific-status transition was requested. Pi accounting and actual provider billing/retry behavior were not available to this worker; no numeric effort or billing claim is inferred from subprocess times.
