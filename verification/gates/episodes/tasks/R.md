# PUBLIC R: staged evidence and continuation

## Problem, stages and scope

Use the common exact model and fixed claims from M/F. You receive two PUBLIC
stages; their order is part of the task, not a claim that future evidence is hidden.

1. `contradiction`: checked state/prefix certificates on hidden or shift refute
   `equal-all-v1`. Choose the required response `stop-parent-proof`. Preserve this
   evidence; do not continue proving the contradicted parent.
2. `restricted-check`: state/prefix certificates on injective agree. This is one
   finite survival record for `equal-nonzero-v2`, not evidence about all `k != 0`.
   Select a discriminating next action and export a continuation packet usable
   without this conversation. Do not repeat the unchanged parent proof or infer
   novelty from absent literature.

The fixture supplies exact finite premises and quantifiers in F. It does not
supply an inspected source anchor for a universal child theorem. Neither source
reading nor proof search is executed by this episode. The task is to preserve
scientific decision boundaries, not to pretend the next investigation occurred.

This is static two-stage packet/evidence relation validation. Stage 1 contains
a complete F submission, including its child certificates: the child evidence
repeated at stage 2 is already present at stage 1. No newly arriving evidence is
withheld or introduced between decisions. A fresh checker is not a successor
worker; replaying the prepared packet measures neither adaptation nor actual
continuation. A stronger R scenario with a checkable successor outcome is outside
this package and would need separate authorization.

## Closed submission contract

Exactly `episode=R`, integer `schema_version=1`, `stages`, `continuation`.
`stages` is the ordered two-element list above; each element has exactly `stage`,
`evidence`, `decision`. First evidence is a complete valid F submission; second
is state/prefix injective certificates. First decision is `stop-parent-proof`;
second is one of the two alternatives below.

The continuation object has exactly:

- `parent=equal-all-v1`, `parent_outcome=refuted`;
- `child=equal-nonzero-v2`, `child_outcome=finite-survival`;
- `next_action` and its matching `obligation`;
- `depends_on=[contradiction,restricted-check]`, in that order;
- `consequences={positive:prepare-human-review,negative:revise-child,inconclusive:park-child}`;
- `excluded=[universal-proof,novelty,attestation]`;
- `human_review=pending`.

Strings in those arrays/objects are literal JSON strings. Full public packets
are `../references/R-reference.json` and `R-alternative.json`. The packet includes
both staged certificates; combined with the trusted inputs and these task rules,
a fresh checker reconstructs the outcome without session memory or sibling files.

## Substantively different admissible decisions

| Next action | Obligation | What would change the next decision |
|---|---|---|
| `prove-injectivity` | `fiber-injectivity` | Attempt to derive equality of observation partitions for nonzero gain, then feasible-policy correspondence. Success prepares human semantic review, an obstruction revises the child, exhaustion parks it. This spends proof effort and commits to an explicit model-specific route. |
| `compare-source-and-park` | `source-assumptions` | Park numerical/proof work while locating and inspecting an admissible closest primary result and comparing information/feasibility assumptions. A matching supported route prepares review, a contrary premise revises the child, missing evidence leaves it parked. This spends source-review effort and makes no premature novelty claim. |

Both actions address an unresolved uncertainty and preserve the contradiction.
The judge checks the action/obligation/consequence relations, not one preferred
sentence or proof plan. These are frozen admissible options for this bounded
fixture, not an exhaustive list of worthwhile research actions in general.

## Rubric, controls and readiness

Objective code checks: stage order, actual certificate replay, claim lineage,
retention of parent refutation, child finite scope, dependencies and distinct
outcome consequences. Fresh-process tests replay static continuation packets. Minimal
resources are the finite inputs/checker, fixed claim rules and the packet itself.
No source statement may be invented to discharge `source-assumptions`.

Human rubric (pending, no automated score): is the selected action relevant to
the question; can its possible outcomes change a decision; are effort and stop
conditions justified; are proof/source obligations adequate; is the packet useful
to a successor? Record objections and unresolved disagreement explicitly. An LLM
critique cannot discharge this review or award scientific truth.

Negative controls ignore the contradiction, reverse stages, omit dependencies,
claim a universal child proof, mismap the action obligation, remove pending human
review, or give the same positive and negative consequence. Public feedback is
as in the README. Readiness: finite staged relation checks available; research
quality and usefulness acceptance remain human-pending.
