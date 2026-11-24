# PUBLIC episode authoring: aro-discovery-tu3

The scoped reference/control checks pass; scientific and capability acceptance
remain unawarded. Human statement correspondence for P and research-quality
judgment for R are pending. The advisory style linter exits 1 on six reviewed
wording flags; it is not reported as a green gate.

Worktree: `<workspace>/aro-discovery-episodes`.
Branch: `task/aro-discovery-tu3-public-episodes`. No commits, pushes, tracker
writes, installations, candidate trials, model calls, new agents or live scientific
state writes were performed. The inherited main checkout and all siblings were
read-only inputs. This is evaluator authoring, not a benchmark run.

## Changes and design decisions

- Refined `docs/specs/2026-11-13-public-episodes-slice.md` after inspecting upstream
  capability/operating-model contracts and finite APIs, before implementation.
- Added `pilot/episodes/README.md`, four public tasks under `tasks/`, frozen inputs
  and a fixed Lean target under `trusted/`, eight reference submissions and five
  stored invalid controls, plus additional in-test negative mutations.
- Added `judge.py`, `author.py`, `validate.py` and a focused standard-library
  unittest module. The package is standalone: no dossier parser or live API is
  imported, and dossier schemas remain unchanged.
- Copied only `finite_reference.py` and `finite_bellman.py` into `vendor/`, after
  checking their source SHA-256. `provenance.json` identifies the source commit,
  snapshot identity and both imports. No runtime absolute sibling import exists.
- Froze trusted finite instances separately from candidate certificates. The
  checker recomputes metadata, feasibility, per-path costs and optimality against
  these instances; valid certificates with recomputed hashes for changed data
  cannot change the task. Closed schema/version/identifier boundaries are tested.
- M accepts different optimal state certificates, not a preferred first action.
  F accepts different frozen counterexamples. R accepts a proof route or a
  source-comparison/park route with distinct obligation relations. P accepts
  different proofs of the fixed template and checks its transitive axioms.

The hidden instance deliberately admits three tied optimal state first actions.
The shifted counterexample uses second actions `{-2,-1,0}` and first action `{1}`:
these preserve a strict state/prefix gap. During reference construction, the
initial shifted-action idea was checked algebraically and corrected before the
reference/control suite; an untranslated action set would have lost that gap.
No failed reference was retained as accepted evidence.

P is only the observation-factorization equivalence over an inhabited action
type. The construction uses arbitrary representatives on attained observations
and a default action elsewhere. It neither proves nor claims the full proposed
single-measurement dynamics/constraint/cost correspondence theorem. Lean compiles
only the trusted declaration plus a restricted proof body; it does not accept
submitted modules, imports, custom axioms or a target chosen by the candidate.

## Observed validation

Commands below were run with explicit `cd` into the stated worktree. Every script
run had an external timeout. Python runs disabled bytecode writes.

| Exact command after `cd <workspace>/aro-discovery-episodes` | Observed result |
|---|---|
| `git rev-parse --show-toplevel && git rev-parse --abbrev-ref HEAD` | Correct root and task branch, checked at start and again before implementation writes. |
| `timeout 10 lean --version` | Lean 4.35.0-rc2, commit `11acb17ec6b07a8f9e9173e6845197929540936b`. |
| `git -C <workspace>/aro-discovery-dossier rev-parse HEAD` | `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`. Read only. |
| `sha256sum <workspace>/aro-discovery-dossier/pilot/baseline/finite_reference.py <workspace>/aro-discovery-dossier/pilot/checkers/finite_bellman.py` | Both matched the supplied finite snapshot; exact identities in provenance. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 -m pilot.episodes.author` | Completed; independently checked generated certificates and the counterexample gap assertion. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m pilot.episodes.judge --input pilot/episodes/references/P-reference.json` | Fixed target passed; axioms exactly `Classical.choice`, `Quot.sound`, `propext`; human review pending. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 180 python3 -B -m unittest discover -s pilot/episodes/tests -v > artifacts/public-episodes-tu3/tests.txt 2>&1` | Final suite: 16 tests, OK. Earlier intermediate suite: 15 tests, OK; final adds stored-control coverage and the second P reference. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -m pilot.episodes.validate > artifacts/public-episodes-tu3/validation-a.json` | Eight public references pass objective checks; five stored invalid controls reject. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -m pilot.episodes.validate > artifacts/public-episodes-tu3/validation-b.json` | Same results in a second fresh process. |
| `cmp artifacts/public-episodes-tu3/validation-a.json artifacts/public-episodes-tu3/validation-b.json` | Exit 0: identical verdict bytes. |
| `sha256sum artifacts/public-episodes-tu3/validation-a.json` | `3d4500467520403fbb842b116d7df81aaacf32237b0c6b47471891a590de3181`. |
| `PYTHONDONTWRITEBYTECODE=1 timeout 30 python3 ~/.agents/skills/technical-style-editor/scripts/lint_technical_style.py pilot/episodes/README.md --language en > artifacts/public-episodes-tu3/style.txt` | Exit 1; six advisory flags reviewed. Negations retain required model/trust boundaries; `unique rational path pairs` denotes mathematical nonduplication, not promotion. No wording change was needed for those flags. |

`validate.py` emits no timestamp or absolute path. Each family also has a test
comparing two fresh CLI processes; thus deterministic output is checked both per
family and for the complete validation summary. The unittest runner's elapsed-time
line is operational output, not a deterministic judge artifact.

Final inventory verification used a bounded inline `python3 -B` command to hash
all package files, rerun `python3 -B -m pilot.episodes.author`, and assert that the
before/after dictionaries were identical. Observed: author regeneration was
byte-identical across 28 package files; both imported source identities and the
source snapshot SHA-256 matched; no `__pycache__` directory or trailing whitespace
in authored package files was found. The generated evidence inventory contains
32 entries. `git diff --check` exited 0 (tracked diff only); new-file whitespace
was checked by the inline Python assertions. Final `git status --short` lists
only the task's new package, contract, report and artifact directory as untracked.

### Positive and negative control coverage

The finite cross-route test compares independent policy enumeration and Bellman
optimization for three trusted cases in all three information modes (nine
case/mode comparisons), then cross-replays certificates. The bounded set-order
test covers all first-action permutations and both path orders. Valid optimal
certificates are checked relationally rather than by byte equality to one answer.

Stored controls: M wrong information; F erased refutation; P wrong target;
P unsupported axiom declaration; R ignored contradiction. Additional tests cover
observation/certificate mode swaps, nonconflicting collisions, wrong child
premises/lineage, false universal conclusions, valid wrong-input certificates
and their recomputed hashes, hash-only tampering, reversed stages, missing
continuation dependencies, mismatched action/obligation, false human approval,
identical consequences, duplicate JSON keys, bool versions, unknown fields and
identifier injection. P includes a real compiler-rejected `trivial` wrong proof,
`sorry`, and mocked empty/wrong/unsupported transitive-axiom reports to exercise
the release-report parser without introducing a real untrusted axiom.

## Reference outcomes and readiness

| Family | Reproduced reference outcome | Engineering readiness and remaining review |
|---|---|---|
| M | Hidden state 1, prefix 0; prefix is not state-implementable. Injective paired assignment is implementable. Different optimal state first actions accepted. | Finite objective checks available; independent task/model correspondence review pending. |
| F | Hidden and shift each state 1 versus prefix 0; fixed parent refuted in the offline fixture. Nonzero child on injective: state/prefix 0, finite survival only. | Counterexample replay and child-premise checks available; no universal child theorem or scientific promotion. |
| P | Both proof bodies compile against the same fixed observation-factorization target; transitive axioms within the positive allowlist. | Narrow compiler-checked development reference. Human statement correspondence pending; no project release build, `formalized` status or full correspondence theorem. |
| R | Two ordered checked stages; both proof-route and source-review/park continuations accepted under explicit relations. | Finite staged checks and fresh-session reconstruction available. Human relevance, plan quality, effort and usefulness rubric pending. |

All results are public development evidence. No private isolation, unseen ability,
source novelty, scientific significance, campaign usefulness or cost saving is
established. No numerical capability score is computed.

## Evidence identity and provenance boundary

`pilot/episodes/provenance.json` records source bytes; `reference-identities.json`
binds the two trusted author inputs. `artifacts/public-episodes-tu3/identities.json`
is a generated inventory of the authored package and observed evidence, excluding
itself. Byte identity is reproducibility evidence, not source/model authority.
The generated references come from the copied finite enumerator and local proof
construction, then undergo the independent checker/Lean checks. No published
mathematical source fact or literature novelty claim is imported.

Trusted evaluator files must be protected from candidate writes in any later
trial. This authoring worktree is not an OS isolation boundary. Restricted Lean
syntax, timeouts and fixed templates reduce scope but do not establish a hostile
Lean execution sandbox. Native hard call-budget enforcement was not implemented;
the worker's 60-call envelope was tracked manually, including wrapper/nested calls.

## Failed commands and consciously omitted work

An initial reconnaissance command `find pilot -maxdepth 3 -type f` exited 1 because
this worktree had no `pilot/` directory yet; it performed no writes. The style
command above also exited 1 and its output is preserved. No reference compiler
or unittest command failed. The deliberately invalid proof/control failures are
expected rejection results, not successful candidate attempts.

Not run: full-repository lint/types/build, legacy Lean release build, mathlib
availability assessment, benchmark/model trials, private isolation test, live
journal/status changes or source admissions. These are outside this bounded
standalone evaluator-authoring scope. Independent coordinator acceptance and a
separate read-only review have not yet occurred. No blocker prevents reproducing
the included finite/Lean references; scored scientific acceptance remains blocked
on the explicitly pending human/reviewer decisions, not on a hidden fallback.

## Кратко владельцу

Подготовлены четыре публичных эпизода M/F/P/R, воспроизводимые эталоны и
отрицательные контроли. Финальные 16 тестов прошли; два свежих процесса дали
одинаковый JSON. Узкая Lean-лемма проверена компилятором, но её смысловое
соответствие ещё не одобрено человеком. Для R машинно проверяются связи решений
с фактами, а качество исследовательского выбора остаётся на человеческом ревью.
Рекомендация: передать пакет координатору на независимую приёмку; benchmark,
научные статусы и заявления о способностях пока не запускать и не присваивать.
