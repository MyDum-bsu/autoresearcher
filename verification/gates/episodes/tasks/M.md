# PUBLIC M: observation and scope

## Problem

Use the exact finite model in `../README.md` and the trusted `hidden` and
`injective` cases in `../trusted/inputs.json`. Determine whether an optimal prefix
assignment for each case can be implemented using only the measured state.
Supply a conflicting pair of complete paths if not. Compute and certify optimal
state and prefix values on `hidden`. Do not replace state information by a
remembered disturbance prefix. All paths and all reachable cells are quantified;
a policy must choose one action for indistinguishable measurements.

`hidden` has `k=0`, first and second actions `{-1,0,1}`, paths `(-1,-1),(1,1)`.
`injective` has `k=1`, the same action sets, paths `(-1,0),(1,0)`.
There are no terminal constraints. These are constructed public fixtures, not
source-derived theorems.

## Closed submission contract

Exactly `episode`, `schema_version`, `certificates`, `state_implementable`,
`injective_implementable`, `collision`. Set `episode=M`, integer version 1;
`certificates` has exactly `state` and `prefix`, each a full vendor result.
The implementability fields are booleans for the submitted hidden prefix
certificate and a checked injective optimal prefix assignment. `collision` is
a length-two list of distinct trusted hidden complete paths with equal measured
state and unequal assigned prefix actions. The collision order is immaterial.
See `../references/M-reference.json` for the complete public JSON shape.

## Reference and alternatives

The hidden state optimum is 1, prefix optimum 0. The prefix certificate chooses
`a=0`, assigns `b(-1)=1`, `b(1)=-1`. Both paths give `x1=0`, so it is not
state-implementable. Every hidden state policy sees a single cell; two terminal
values differ by 2, so worst absolute terminal value is at least 1. Action `b=-a`
attains 1. Thus state certificates with `a=-1,0,1` are all optimal. The two public
submissions use different first actions in their state certificates, not merely
different prose. The injective prefix assignment has value 0 and factors through
`x1=p`; it is state-implementable. This checks the paired premise change.

Independent finite routes reproduce the values and replay the certificates.
Wrong information labels, a duplicate/nonconflicting collision, an altered input
with a recomputed valid hash, a false implementability boolean and wrong values
are negative controls. Feedback is the common public judge policy; no semantic
status promotion follows. Readiness: finite checks available; independent review
of task/model correspondence still required.
