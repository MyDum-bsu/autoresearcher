# A support-defect upper certificate for one late measurement

Status: proposed general derivation, with executed exact arithmetic on four existing cases. No general proof checker or independent new checker has validated this argument. Exact r104 equality is the resulting verification obligation, not an awarded scientific result.

## Source anchors and scope

Directly inspected `research/sources/A4-p12.png`, physical PDF p12 / printed p77, and `A4-p4.png`, physical p4 / printed p69, rendered from `research/sources/A4.pdf`. The PDF hash recomputed in this run is `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`. P4 Assumption 1 specifies exact current-state measurement and selection of an entire next block. P12 equation (3.1) specifies T=120, x0=(0,1), scalar controls |u|<=1, independent disturbances |w|<=0.5, terminal strip [2,10], and terminal second-coordinate reward. Its text says: “При T1 >= 104 оптимальная стратегия не дает улучшения критерия качества”. This is the published numerical observation motivating this work, not an exact certificate for either pinned rational model.

Read `goal/wave-4/model-and-source.md`, the independent review `artifacts/goal/wave-4/independent-review/report.md`, and the actual M0 arithmetic implementation. Existing M0 certificate objects and four wave-4 certificate objects were read by the probe and bound by raw SHA256 in its output. Wave-4 bounds have nonzero rational gaps. No assertion here replaces those historical outputs.

The glossary's special bridge class A=I with discrete disturbances is not the class of this derivation. The source-native continuous-box class in `contract.md` applies. Printed coefficients and reconstructed decimals remain separate exact models; no trigonometric identity is assumed.

## Notation

Write terminal quantities as

X = d_x + p_x a + c_x b + z_x + e_x,
Y = d_y + p_y a + c_y b + z_y + e_y.

Here a is the fixed prefix, b is the whole suffix selected from the measured state, z is the terminally propagated prefix disturbance, and e is the future disturbance contribution. Prefix and suffix disturbance sets are independent compact zonotopes. Each control coordinate has symmetric bound beta_t. Define S_x=S_x^pre+S_x^post and S_y similarly, as exact row supports of the full disturbance box. Define

H_x = sum_suffix beta_t |C_xt|,
H_y = sum_suffix beta_t |C_yt|,
H_m(lambda,mu) = sum_suffix beta_t |C_yt+(lambda-mu)C_xt|.

For prefix controls define H_p(lambda,mu) by the same last expression summed over prefix times. For arbitrary nonnegative lambda,mu, the ordinary open-loop upper bound is

D0 = d_y-S_y + lambda(d_x-L-S_x) + mu(H-S_x-d_x)
     + H_p(lambda,mu) + H_m(lambda,mu).

A fully feasible open-loop witness with guarantee J is required separately. Both strip sides and every independent disturbance must be checked for that witness.

## Proposed general inequality and derivation

For any admissible feasible state policy with prefix a and guaranteed reward q:

(1) d_x+p_x a >= L+S_x-H_x.

Choose a prefix disturbance minimizing z_x. Whatever suffix the measured-state policy chooses there, its nominal contribution c_x b cannot exceed H_x. Future disturbances can independently minimize e_x. Robust lower-strip feasibility therefore implies (1).

(2) d_x+p_x a <= H-S_x+H_x.

Use the prefix maximizing z_x and the future disturbance maximizing e_x. The chosen suffix contribution cannot be less than -H_x. This yields (2). These are necessary viability restrictions, not sufficient conditions for a feasible state policy.

(3) q <= d_y+p_y a+H_y-S_y.

Use a prefix minimizing z_y, bound its chosen suffix reward above by H_y, and minimize future e_y. This is an upper bound even if its maximizing suffix would violate the terminal strip.

The three prefix extremes may be different. No joint attainment is claimed or needed: (1), (2), and (3) constrain the SAME fixed a of a policy that must work for every prefix. This is the key quantifier check. No prefix history is supplied to the controller. These necessary inequalities would even hold under a more informative prefix observation; the lower witness remains open loop and hence admissible with the stipulated sensor.

The nonnegative slacks in (1) and (2) can be added to the right side of (3), with weights lambda and mu. Maximizing the resulting linear expression over the prefix box gives

q <= d_y-S_y + lambda(d_x-L-S_x) + mu(H-S_x-d_x)
     + H_p(lambda,mu) + (lambda+mu)H_x + H_y
   = D0 + Delta,

where

Delta = (lambda+mu)H_x+H_y-H_m(lambda,mu) >= 0.

Nonnegativity follows coordinate by coordinate from the triangle inequality and |lambda-mu|<=lambda+mu. Taking the supremum over policies yields V_r<=D0+Delta. The constant open-loop policy yields J<=V_0<=V_r. Thus

0 <= V_r-V_0 <= D0+Delta-J.

If a verified open-loop primal-dual pair has J=D0 and Delta=0, the proposed argument squeezes V_r=V_0=J exactly. No existence of an optimal adaptive policy is needed. With an inexact open-loop pair the bound includes its actual gap D0-J; it must not be silently dropped.

## Common-corner interpretation and logical attacks

When mu=0 and lambda>0, Delta is a sum of nonnegative coordinate defects lambda|C_xt|+|C_yt|-|C_yt+lambda C_xt|. It vanishes exactly when C_xt C_yt>=0 at each suffix coordinate with positive beta_t. Then one corner simultaneously maximizes suffix X and Y. With lambda=0 the defect vanishes without any X/Y alignment requirement. The general two-multiplier formula, rather than a one-sided sign rule, is authoritative when mu is positive.

Attack 1: a common corner maximizing X and Y may violate X<=H. The proof does not select this corner as a feasible policy. It uses it only for upper bounds; the existing open-loop witness satisfies the full strip. Inferring feasible continuation from (1) alone would be invalid.

Attack 2: separate disturbance extremes may be incompatible. The argument does not sum disturbance vectors or assert simultaneous extrema. It adds scalar necessary inequalities about the common prefix. Replacing the fixed prefix by a prefix chosen after observation would break this step and is excluded.

Attack 3: positive Delta does not imply strict information gain. Delta is an upper bound defect; zero is sufficient, not necessary. At r67 the historical wave-4 lower bounds separately certify a gain over M0. The new defect bound alone cannot do that.

Attack 4: the upper-strip multiplier being zero does not make the upper strip redundant. It only makes that dual weight zero. The M0 feasible witness is checked against both sides. The two exact witness terminal intervals have upper endpoints below 10 in the executed arithmetic.

No new scientific cases or r103 optimization were run. Reversing the last suffix corner coordinate fails the favorable-sign predicate for each frozen case. Corrupting the M0 objective is rejected by the existing checker. These controls test arithmetic/premise handling, not a universal theorem prover or an adversarial policy interpreter.

## Actual fixed-instance observations

The probe uses the unmodified wave-4 copy of M0's exact checker, not an independent implementation. It accepted both M0 primal-dual certificates, including exact objective/dual equality and both strip sides. Its results are identical under normal and optimized Python.

| Exact input | r | Delta (display only) | Exact Delta=0 | Common X/Y suffix corner |
|---|---:|---:|---|---|
| printed | 67 | 1.6272285823887336 | no | no |
| printed | 104 | 0 | yes | yes |
| reconstructed decimal | 67 | 1.6324558241460756 | no | no |
| reconstructed decimal | 104 | 0 | yes | yes |

Exact fractions are in `artifacts/goal/wave-5/astra/probe.stdout.json`, together with input/certificate hashes, multipliers and witness strip intervals. For orientation only, printed J is approximately 1.4957100981243105 and reconstructed J approximately 1.5011019893820279; lower strip endpoints are exactly 2, upper endpoints approximately 9.83535819960487 and 9.84122761611631. Both upper multipliers are exactly zero. No tolerance is used to test Delta=0.

For both variants the r67 suffix has opposing X/Y signs at times 67–72 and 89–103. The r104 suffix has none. This locates a structural explanation of the published cutoff in the exact impulse data, without assuming a rotation angle. It does not prove r103 strict gain, cutoff necessity, or a general comparison between differently timed single measurements. The inclusion of open-loop policies only proves V_r>=V_0; it does not order V_r and V_s for two different single measurements.

## Contribution boundary

This is a viability/support calculation, with the common-corner condition as a zero-defect specialization. Generic box duality and monotonicity are not claimed new. The potential useful deliverable is a small certificate of zero or bounded information value, avoiding recourse-vertex enumeration and retaining the upper-strip feasibility obligation. Whether that constitutes anything beyond known reconstruction remains unresolved.

The wave-4 independent review identifies BT04 Theorem 2.2 (physical p5) as already providing finite fixed-recourse reduction; that is a report-backed comparison, not a freshly consulted primary anchor in this stage. A4 p4 expressly attributes single-closure work to reference [14]. Its original theorem statements have NOT been audited here. The next source obligation is that exact comparison, not a broad search and not a novelty assertion from silence.

General theorem verification, independent exact application checking and closest-source criticism remain necessary. Numerical agreement with A4 and completion of this stage do not meet the first-success goal.
