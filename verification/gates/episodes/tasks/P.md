# PUBLIC P: observation factorization, narrow proof diagnostic

## Fixed target

For arbitrary types `Path`, `Obs`, `Action`, with `Action` inhabited, arbitrary
`obs : Path → Obs` and assignment `f : Path → Action`, prove:

```
(∃ g : Obs → Action, ∀ p, g (obs p) = f p) ↔
  (∀ p q, obs p = obs q → f p = f q)
```

Every path is quantified. No surjectivity or injectivity is assumed. Observations
outside the image may receive any action; the inhabited premise supplies it.
Paths/observations may be empty. The exact declaration and imports are frozen in
`../trusted/target.lean.txt`. Fixing the statement is independent of compiling it.
This asks for a proof/construction, not a numerical instance lookup.

The mathematical interpretation is only that a scenario assignment factors
through observation iff it is constant on observation fibers. It does NOT prove
trajectory, control-feasibility, terminal-cost preservation, vertex reduction,
existence of robust optima, novelty, or the full single-measurement correspondence.
No source-paper correspondence or human statement approval is supplied here.

## Closed submission and resources

Submit exactly `episode=P`, integer `schema_version=1`,
`target=observation_factorization`, and a nonempty `proof` string of indented Lean
tactics replacing ONLY the proof placeholder (no outer `by`). Lean 4.35.0-rc2 with
its standard `Lean` import is the complete admitted library. No mathlib or
additional installation is required. The restricted syntax rejects commands,
imports, declarations, comments, strings, metaprogramming and unapproved qualified
names. Read `../judge.py:proof` for the public syntax restriction; it is a bounded
diagnostic, not a universal Lean proof interface or a hostile-code sandbox.

## Reference and alternatives

The reference explicitly constructs `g`: on an attained observation choose a
representative path and use its assigned action; otherwise use `default`. Fiber
constancy makes the chosen representative irrelevant to all attained paths.
The forward implication transports equality through `g`. This logical argument
was authored here; Lean compilation and transitive axiom inspection check the
fixed formal target. The actual public proof is in `../references/P-reference.json`.

Any proof body admitted by the restricted grammar that proves the same fixed
statement under the allowlist is accepted, including different local binders,
equality rewrites and witness constructions. The gate never compares proof bytes
with the reference. The syntax boundary intentionally excludes some legitimate
Lean proofs; extend it only as an explicit evaluator revision, not a hidden fallback.
No target-equivalent helper theorem is supplied as an admitted proof dependency.

Wrong target ID, proof of a trivial wrong statement (`trivial` against the fixed
target), `sorry`, unsupported axiom declarations, an unknown transitive axiom,
and an empty/mismatched theorem report are controls. Compiler success is necessary
but insufficient: exact template, pinned version and parsed positive axiom
allowlist are also required. Public compiler feedback is permitted. Reference
compilation does not grant `formalized` status: the project release build and
human semantic correspondence review remain outside this task. Readiness is
compiler-checked development reference, with human statement fidelity pending.
