# Wave 5 Stage C: independent mathematical and source criticism

The universal certificate is still incomplete under the original goal's checked-proof requirement. The executed checker reproduces exact finite arithmetic, not a theorem about arbitrary continuous-domain state policies. Original A4 reference 14 was located in the existing pool and inspected. Its support/duality construction substantially overlaps the proposed mechanism; a substantive nearest-source delta has not been established. `goalAchieved=false`; coordinator inspection and continuation remain mandatory.

This report is criticism and an evidence inventory, not an LLM mathematical-truth, novelty, approval or attestation verdict. Stage C is **partial**: the targeted standalone monotone-control literature comparison remains unresolved. Static/adjustable equality results and a monotone affine-recourse result were inspected directly, but they do not replace that missing comparison.

## 1. Scope and authority

Verified worktree `<workspace>/aro-discovery-campaign`, branch `task/aro-discovery-k4t-campaign`, before writes. Read the complete wave-5 specification, original first-success goal, FOUNDATION and AGENTS, literature/oracle/session, workflow-worker, logika and technical-style instructions. The coordinator's existing task was not claimed, closed or advanced. No new proof target, scientific instance, solver optimization, nested agent/workflow, provider retry/fallback, install, commit, push, comparator or live scientific write was performed.

All new output is confined to `artifacts/goal/wave-5/independent-review/`. Reviewed Stage A/B material and older scientific artifacts were not edited. The replay itself verifies all 11 Stage B frozen parent hashes; `execution-summary.json` records that result and the observed hashes of 44 reviewed Stage A/B files. Those 44 hashes were captured after replay, not a fabricated before-session snapshot. Previous untracked work was already present on entry.

## 2. Actual mathematical claim

Parents: `goal/wave-5/astra/contract.md`, `derivation.md`, and `goal/wave-5/verification/contract.md`, `proof.md`, `check.py`.

The class is deterministic finite-horizon linear dynamics, independent continuous symmetric disturbance boxes at every time, symmetric control boxes, one scalar terminal strip `L<=X<=H`, scalar terminal reward `Y`, and no intermediate constraints. A fixed prefix is selected before all disturbances. At `r`, one exact current-state measurement selects the whole suffix before future independent disturbances; there is no later observation. The proposed theorem is broader than A4's stationary example, but the checked data are only its two pinned rational coefficient variants.

For arbitrary nonnegative strip multipliers `lambda,mu`, the proposed bound is

`J <= V0 <= Vr <= D0 + Delta`,

`Delta = (lambda+mu)Hx + Hy - Hmix >= 0`.

`J` must come from a feasible open-loop witness satisfying both strip sides. Exact adaptive equality requires BOTH `J=D0` and `Delta=0`. Positive `Delta` supplies no gain lower bound. Neither a necessary cutoff nor monotonicity between two different single-measurement times is claimed.

The written proof tests three possibly different prefix disturbances against the SAME fixed prefix control. This does not require their extrema to coincide. Independent future disturbances remain available after each measurement. Suffix box maxima are upper relaxations, not necessarily feasible suffix choices. The upper strip is retained in the prefix viability inequality; zero upper dual weight never excuses omitting upper-strip feasibility of the lower witness. These qualifications are present in the parents, rather than repairs supplied by this reviewer.

## 3. Executed decisive checks and their limits

Executed from the verified worktree, with scratch local to this review directory:

- `timeout 120 env TMPDIR="$PWD/artifacts/goal/wave-5/independent-review/scratch" python3 -B goal/wave-5/verification/check.py`
- the identical command with `python3 -B -O`.

Both exit 0; raw stdout/stderr and exit files are saved under `replay-normal.*` and `replay-optimized.*`. `cmp` found byte-identical stdout. A separate bounded Python summary recomputed all 11 frozen-parent hashes and recorded `all_11_parents_match=true` in `execution-summary.json`.

| Fixed exact model | Closure | Exact `J=D0` | Exact defect result | Display-only J |
|---|---:|---|---|---:|
| a4_printed | 67 | checked | strictly positive | 1.4957100981243105 |
| a4_printed | 104 | checked | zero | 1.4957100981243105 |
| a4_reconstructed_decimal | 67 | checked | strictly positive | 1.5011019893820279 |
| a4_reconstructed_decimal | 104 | checked | zero | 1.5011019893820279 |

The checker uses exact Fractions, separately propagates B and E, verifies every open-loop control, both robust strip endpoints, full disturbance supports, chronological nominal replay and nonnegative dual weights. Both upper multipliers in these witnesses are zero. No decimal tolerance determines equality. Printed and reconstructed-decimal data remain distinct; neither is confirmed author/trigonometric input.

The reported 16 invalid controls have different meanings. There are **12 malformed-input/certificate mutations actually rejected by `check()`**, two r67 nonzero-defect predicates, and two flipped favorable-corner predicates. The last four are not checker rejection of four separately submitted certificates. A further symbolic wrong-upper-slack-sign predicate is separate. This distinction matters when quoting discrimination coverage.

### Blocking coverage boundary

`goal/wave-5/verification/check.py:100` checks a polynomial slack identity; `:103-110` checks a symbolic decomposition while explicitly excluding the nonnegative premises. `:121-158` evaluates four fixed rows and their controls. It never represents an arbitrary Borel policy or verifies the dynamics-to-necessary-inequalities implication for the general class. `proof.md:23,29-55,57-65` carries those obligations in prose.

Thus a green replay does not by itself certify `Vr=V0` for arbitrary continuous-domain policies, even for r104: that conclusion additionally uses the written universal upper-bound argument. The open-loop primal/dual equalities and exact zero defects themselves are executed evidence. The parents disclose this boundary; this is an unmet acceptance obligation, not a hidden false theorem or a counterexample.

The replay reuses Stage B's implementation and existing M0 witnesses, with newly saved streams. It is an independent execution and code inspection, not an independently implemented second mathematical route. Stage B's forward-power construction is different from M0's backward builder, but Python Fraction, transcription, witness data and the proposed reduction remain shared dependencies.

Stage B's recorded Ruff/format failures were not repaired or rerun here; they are secondary engineering limitations, not a mathematical refutation. No Lean theorem or comparator was run.

## 4. Primary-source comparison

PDF hashes are bound in `source-hashes.txt` and `execution-summary.json`. All page numbers below are one-based physical PDF pages, followed by printed pages where useful. Text extracts were produced directly from the original PDFs with `pdftotext -layout`, not copied from earlier summaries. Rendered A4 p12 and A3 p6 were visually inspected to check formula layout. Other extracts/renderings retained here are evidence availability, not a claim that every extracted page was fully read.

### A4 and its actual reference 14

`research/sources/A4.pdf`, pp2-4 / printed 67-69, equations (1.1)-(1.5) and Assumption 1: stationary linear dynamics, continuous timewise box disturbances, support-based terminal tightening, current-state measurement followed by a whole-block program. These premises agree with the intended information pattern. They do not agree with the earlier campaign's correlated complete-path replacement or the glossary's special `A=I`/discrete-disturbance bridge class; neither replacement is used here.

A4 p12 / printed 77, equation (3.1), explicitly states: “При T1 >= 104 оптимальная стратегия не дает улучшения критерия качества”. The page also reports `J(x0)=1.501102`, the two-sided strip `[2,10]`, and an approximation accuracy `5·10^-4`. It is already a published cutoff observation. Exact rational reconstruction of that observation is not a new source-level phenomenon.

A4 pp16-17 / printed 81-82 identifies [14] as Kastsiukevich and Dmitruk, *A method for constructing an optimal control strategy in a linear terminal problem*, 2021, DOI `10.33581/2520-6508-2021-2-38-50`. This is **the existing `research/sources/A3.pdf`**, not an unavailable new lead and not an author-manuscript substitute. Its journal pages and DOI are visible on physical pp1-2 / printed 38-39. No download was necessary.

### A3: the closest inspected control construction

Read original A3 physical pp2-8 / printed 39-45 for model, strategy and support/dual construction, and p9 / printed 46 for Example 1.

- Pp3-4 / printed 40-41: Definitions 1-4 and (5)-(9) specify robust open-loop control, exact state at T1, a full suffix selected from that state, and the minimax comparison with open loop. Future box availability is preserved.
- P5 / printed 42 explicitly compares the nested strategy value and open-loop value by the minimax inequality. This inclusion/comparison is known background.
- P6 / printed 43, Proposition (12), under its stated rank/normal hypothesis, gives affine support dependence `f(alpha)=f0+lambda alpha`. Equations (13)-(14) retain both terminal sides and dualize the suffix control box.
- P7 / printed 44 derives the positive/negative dual parts, explicit `f0`, and the first-block robust LP (17). The control-bound contribution is the support of a linear combination of terminal rows. This is directly relevant to the proposed `Hmix`, not a remote analogy.
- P8 / printed 45 extends the support construction via lifted terminal coordinates. These are support inequalities/outer approximations; they must not silently be read as an unconditional exact finite-normal closure representation.
- P9 / printed 46 repeats this oscillator example at `T1=80`, the `[2,10]` strip and `J=1.501102`, and reports a larger adaptive value. It does not state the proposed general two-multiplier information-value bound there.

**Consequence for the claimed delta:** box supports, separate strip dual weights, one-closure minimax comparison and control-row support combinations already appear in the closest control source. The packaging `Delta=(lambda+mu)Hx+Hy-Hmix` measures the loss from separate suffix support relaxations relative to the combined row support. The inspected pages do not explicitly state that exact formula as a general information-value certificate. That narrow absence is NOT evidence of a substantive literature gap or a priority claim. A mere reformulation of these support calculations/common-corner equality does not meet the original goal.

### Static versus adjustable robust optimization

`research/sources/BT04.pdf`, pp4-5 / printed 354-355: Theorem 2.1 states static/adjustable equivalence with **constraint-wise uncertainty**, a product of nonoverlapping row uncertainty blocks, plus a compactness condition on feasible recourse. Timewise independence of physical disturbances is not that hypothesis: the same prefix coordinates affect both strip rows and reward. Therefore applying this theorem to the unreduced A4 problem without a verified transformation would be unjustified.

BT04 p5 Theorem 2.2 gives the finite-vertex fixed-recourse formulation. It already accounts for the generic wave-4 finite-recourse mechanism; it does not alone supply the proposed vertex-free support-defect bound.

`corpus/09_Marandi_denHertog_2018.pdf`, physical pp4-6 / printed 558-560: Definitions 1-4, Assumption 1 and Theorem 1 extend static/adjustable equality under constraint-wise uncertainty and explicit convexity/concavity/compactness hypotheses. Again, independent times do not mean independent terminal rows. No direct coverage or novelty exclusion is asserted without a model-preserving mapping.

### Monotone recourse and remaining monotone-control obligation

`research/sources/GTW25.pdf`, physical pp6-9, Theorem 1, is the June 6, 2025 author manuscript *On the Optimality of Affine Decision Rules in Distributionally Robust Optimization*, not a verified final journal version. Its (F), (A), (D), (B) require monotone cost, affine lower technology/RHS, nonnegative upper recourse matrix, and an equivalent invertible lower subsystem with positive inverse at an attained optimum. The conclusion is equality with **affine** rules, not automatically constant/open-loop rules. The source expressly distinguishes optimal from all feasible first-stage decisions.

The candidate's same-sign suffix criterion is a terminal impulse-row condition. It does not establish the above equivalent-subsystem hypothesis or global monotonicity of the oscillator state dynamics. In particular the printed A matrix has a negative off-diagonal entry. A common favorable corner for X/Y is not a source-backed theorem about general monotone control systems; the opposing upper strip also prevents an unconditional “more control is always feasible” argument. These observations delimit the comparison, not a proof that every monotone-control theorem is inapplicable.

A dedicated closest monotone-control original theorem was **not secured**. A targeted web search returned no usable result; one bounded arXiv API request failed with curl exit 22 and no response PDF. No automatic retries or provider/tool fallback were performed. The failure is not evidence of an absent theorem. GTW25's scalar inventory/affine-policy references are secondary leads, not newly inspected primary results. This unresolved source comparison prevents a documented substantive source-delta label.

## 5. Disposition and coordinator decision

| Category | Evidence-based status |
|---|---|
| False claim | No executed counterexample or specific contradictory source statement obtained. This does not certify truth. |
| Known reconstruction | Open-loop robust tightening, suffix support/dual expressions, minimax inclusion, common-corner support equality, and A4's observed cutoff are already source-backed background. |
| Proof gap / incomplete acceptance | Universal policy/support/order argument remains prose; symbolic algebra and four exact applications do not discharge the general checked-proof obligation. |
| Documented plausible substantive source delta | Not established. The explicit defect packaging differs from the displayed statements inspected, but significance and overlap with monotone-control results remain unresolved. |

Recommendation to the coordinator: retain the finite exact arithmetic and source criticism as useful reconstruction, keep the scientific goal unachieved, and do not fund another numerical sweep or a proof of A4's cutoff merely under a new name. Before any continuation on this mechanism, resolve the narrowly missing original monotone-control comparison and decide whether the explicit support-relaxation defect adds substantive content beyond A3's dual support calculus. If it does not, close this mechanism as reconstruction. If the coordinator identifies a genuine, source-backed delta, the unchanged general claim still needs a checked proof covering its policy quantifiers and support inequalities. This review does not invent a replacement target or start either branch.

## 6. Unperformed work and observed limitations

No r103 or other new scientific cases; no time sweep, necessity theorem, source-coefficient repair, full published-policy reproduction, broad novelty survey, general proof formalization or independent fresh checker implementation. No standalone monotone-control original theorem comparison completed. General proof acceptance and substantive novelty remain unresolved. The initial optional PDF extraction through Python failed because `fitz` was not installed; existing Poppler utilities were then used for PDF extraction, with no dependency installation. The failed arXiv request and raw replay streams remain preserved. Native provider retry/billing behavior is unknown; no claim about OS isolation or external billing is made.
