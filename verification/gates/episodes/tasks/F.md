# PUBLIC F: refute and retain a restricted child

## Problem and fixed claims

Parent `equal-all-v1` asserts: for EVERY instance in the finite model/limits of
`../README.md` for which both state and prefix feasible policy sets are nonempty,
the two optimal values are equal. Refute this exact parent with a checked frozen
witness. Retain the parent and its refutation, then propose the distinct child
`equal-nonzero-v2`: the same assertion restricted to `k != 0`. Check the child
only on frozen `injective`; report finite survival, never a universal proof.
The child is not a replacement version that erases the failed parent.

Use `hidden` or `shift` from `../trusted/inputs.json`. `shift` has first action
`{1}`, second actions `{-2,-1,0}`, `k=0`, paths `(-1,-1),(1,1)`. As in M, controls
are finite and second actions must respect the selected observation. A zero-gain
attack is outside the restricted child's premise even if it refutes the parent.
The parent is explicitly about feasible optima: infeasibility is not a numerical
value and cannot be used as a spurious equality or zero.

## Closed submission contract

Exactly `episode=F`, integer `schema_version=1`, `parent=equal-all-v1`,
`parent_outcome=refuted`, `witness` (`hidden` or `shift`), `certificates`, `child`.
Certificates contain full `state` and `prefix` results. The child has exactly
`id=equal-nonzero-v2`, `parent=equal-all-v1`,
`restriction=nonzero-prefix-gain`, `outcome=finite-survival`, `case=injective`,
and `certificates` (state/prefix). Full shape: `../references/F-reference.json`.
No candidate-supplied instance, expected identity or textual predicate is admitted.

## Reference outcomes and accepted alternatives

Both hidden and shift certify state value 1 and prefix value 0. In shift, state
chooses `b=-1`, while prefix chooses `b(-1)=0`, `b(1)=-2`. Both satisfy their
finite action premises; the optimum-zero prefix certificate is a lower-bound
certificate because the objective is nonnegative. A state policy leaves terminal
values separated by 2, proving lower bound 1, attained by its certificate.
The two public references select genuinely different frozen witness inputs.
Any checked optimum certificate on either witness is admissible. Child values
on injective are both 0. The nonzero-gain injectivity argument is a proposed
proof route, not a proof awarded by this finite check.

Negative controls include erasing the parent refutation, relabeling the child
as proved, attaching hidden to the nonzero child, changing the child lineage,
and transplanting valid certificates from altered data with new hashes.
Minimal resources are the trusted finite cases plus independent exact checker;
no literature or external solver is needed. Public feedback and human review
follow the common README. Readiness: finite reference and controls available;
no universal child theorem or scientific attestation is supplied.
