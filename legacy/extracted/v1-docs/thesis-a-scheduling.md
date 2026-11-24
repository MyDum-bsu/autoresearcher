# Paper skeleton A — Value of information under scheduled closures

> Status: DRAFT SKELETON (2026-10-11). Gated on: (G1) the A4 collision
> check (reading agent in flight — does the Dmitruk school already
> optimize the closure schedule?); (G2) corpus reading completion for
> the bridge-line papers; (G3) an analytic proof route for the argmin
> law (S2). No submission intent until G1-G3 close.

## One-sentence thesis

For the 2D guaranteed-control bridge class, the value of information
under an arbitrary schedule of closure moments has a closed form; the
optimal single-closure schedule obeys a plateau law with an explicit
whole-domain criterion; and the maxmin value is a universal floor of
the whole ladder — together giving a computable, exactly certified
theory of when measurement is worth its cost.

## Result structure (what we would actually claim)

1. **Closed form for any schedule R** (S3, survived): V(R) = the
   blind-block fold. Lower half: Lean-proven sorry-free
   (`blocks_sum_lower`). Upper half: certified on 137 LP + 5952 DP
   points; the induction is sketched in the S4 reduction.
2. **Tail-sum / bottleneck-partition reduction** (S4, survived):
   scheduling = minimizing a maximum of <= k+2 linear forms over
   compositions — connects to bottleneck optimization; 596 LP points,
   54 reductions, 3348 DP cross-checks.
3. **One-closure argmin law** (S2, survived the fresh 72-instance
   attack): V({r}) = max(c, g(r)); argmin = the plateau; whole-domain
   iff W <= V_min. Proof route (identified, not yet written): the lower
   bound is the k=1 case of the Lean-proven fold; the upper bound is
   the pursuit-strategy argument already formalized for the upper half;
   (ii)/(iii) are then finite interval-arithmetic lemmas on a
   V-shaped function — Lean-able.
4. **Maxmin floor** (S6, survived): V(R) >= V_mm for every R with the
   explicit closed form — the quantitative answer to the max-min
   asymmetry question (Dmitruk consultation material, bd 34k).
5. **Monotonicity spine** (P2, Lean-proven): the ladder
   OC >= RO(k) >= DP is already formalized.

## What is missing before this is a paper

- M1: written proof of S2 items (ii)/(iii) (finite arithmetic) and the
  S2 upper bound (pursuit argument formalization) — the only genuinely
  new mathematics; everything else assembles proven pieces.
- M2: G1 A4 collision check + the related-work delta vs the Dmitruk
  school (A1-A5) and vs BGT-2004/GTW lines.
- M3: the writing (EN preprint; RU dissertation chapters from the same
  results).

## Related-work delta (from the reading program so far)

- BGT-2004: AARC gives feasibility/quality bounds, no exactness claim
  for affine rules in general — our 1D exactness theorem (P3) and the
  scheduling law are outside their frame (they do not schedule
  information).
- Bertsimas-Shtern 2018: dual wedge basis-partition gives piecewise
  linear x-independent dual policies (dual-side exactness per basis
  region) — adjacent mechanism, primal scheduling side untouched; their
  CS-oracle failure mode (31-34% infeasible CCG runs) motivates our
  exact-certification discipline.
- Tsang-Shehadeh-Curtis 2022: i-C&CG error-budget certificates —
  methods template for our certified pipelines; orthogonal to the
  scheduling question.
- A4 (Dmitruk 2022): collision check in flight (G1).
