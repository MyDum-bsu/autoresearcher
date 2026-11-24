# Research pilot: work packets, release plan and first-worker assignment

Status: original implementation decomposition, with the M0 execution amendment below. Companion specification: `2026-11-10-research-pilot-implementation.md`. No implementation worker was launched in the initial design session.

Execution amendment: the owner subsequently approved baseline-first through P2b, retained Beads, selected Pi OpenAI Sol through the current login, and authorized the coordinator to organize the local work. The coordinator created/claimed `aro-discovery-3sd` and used `<workspace>/aro-discovery-baseline`, branch `task/aro-discovery-3sd-baseline`. Workers used verified `openai/gpt-6.1-sol` (medium for P1/repairs, high for independent mathematical work/review), sequentially, with 90-minute native timeouts and a 60-call stopping instruction. A native hard call-count limit was not available; this is disclosed in the execution report. On any limit exhaustion the chain must stop for investigation, not retry automatically. The later runtime, r=80 question, spending profile, scientific attestation and live journal remain outside this authorization. See the baseline worktree's `reports/2026-11-10-baseline-execution.md` for results and limitations.

Acceptance amendment from execution: run `ruff check --no-cache pilot` on each new code packet before handoff, without weakening the repository configuration. Final M0 acceptance also repeats the specified unittest commands with `-O`. Scientific artifact fingerprints are internal provenance; owner summaries show source names/pages and results rather than checksum inventories.

## 1. Working-copy and task discipline

The source checkout is `<workspace>/aro-discovery`, branch `research/autonomous`, HEAD `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`. It contains owner/unrelated changes, including `docs/GLOSSARY.md`, `events.jsonl`, `state/science.db`, untracked pilot specifications/checks and essay/report files. Do not stash, reset, move, commit or overwrite them. The design is delivered in `<workspace>/aro-discovery-restart-plan`, branch `plan/research-pilot-restart`, based on the same HEAD. No commit or remote sync was requested.

Before implementation the owner supplies/creates the relevant Bead and approves the input inventory. A worker claims only that owner-created task. Packet IDs P0–P9 identify scope; they do not automatically create tasks, carry task status or supersede existing Beads. Do not claim an old scientific task merely because its title looks related. Existing journal decisions, grids and configuration require their established owner route. This plan contains proposed decision payloads only; it does not forge owner ledger entries.

Feature work occurs in a new worktree from the agreed base; no work in the main checkout. Owner selects the integration base because pilot inputs are not all in HEAD. A fingerprinted read-only input root is sufficient for P1; no need to copy unrelated dirty files. No commits/pushes/PRs without explicit instruction. Plan-sized units target reviewable diffs under 300 lines; P1 and the protocol packet may require two sequential sub-slices (contract/tests, implementation). Preserve a coherent tested interface; if over 400 changed source/test lines, stop and propose the split rather than adding infrastructure.

## 2. Dependency order and work estimates

Estimates are bounded **agent effort**, not human delivery dates or a promise that the draft USD ceiling funds development. API calls below mean additional automatically invoked paid calls; a manually started worker session itself may be billed/unmetered and must be reported honestly. One active worker throughout. Independent source review can be performed sequentially; no fan-out is required.

Dependency graph:

`P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P7 -> P8`

`P0 + P2 -> P9` (optional offline continuous scientific attempt; no runtime required). Publishing P9 evidence additionally requires R1 (P3–P7) and owner-resolved gates.

P8 is paid calibration, not required for M0. P9 is the attempt to resolve Q; it may be deferred after M0. Do not hide this distinction in completion reporting.

| Packet | Scope and write boundary | Expected artifact and acceptance | Stop condition | Agent effort / paid calls |
|---|---|---|---|---|
| **P0 — seal inputs** | Owner/lead review only. `pilot/inputs/review-v1/manifest.json`, `pilot/inputs/review-v1/question.json`, source comparison record; no corpus/config/legacy state writes | Immutable inventory of spec, glossary, sources, fixtures and registry proposals. A second reader checks every used source page and coefficient; validator rejects missing scope, tolerance or approval. Owner-approved fixture freeze required before research runs | Missing input, mismatched source or absent approval; architecture-only work may continue but no live publication | 0.5–1.5 h; 0 API; one proposed bounded owner review |
| **P1 — finite reference** | Only `pilot/baseline/finite_reference.py`, `pilot/baseline/test_finite_reference.py`, `pilot/baseline/README.md`. Pure functions, CLI JSON to stdout; no runtime or scientific journal | Exact exhaustive policy values, canonical policy witnesses, explicit infeasibility, malformed-input errors. `python3 -m unittest discover -s pilot/baseline -p 'test_*.py'`; repeat CLI and byte-compare. See full assignment below | Scope would require a continuous solver, journal integration, new dependencies or >400 source/test lines; disagreement gets a dossier, not changed expectations | 1–2 h; 0 automatic API; one lower-cost worker session |
| **P2a — independent finite verifier** | `pilot/checkers/finite_bellman.py`, its public tests; P1 files read-only. Separate implementation of transitions and information fibres | Bellman values and direct witness replay agree with P1 on all public cases and small frozen generated cases. Mutation: hidden-prefix choice for equal state must fail. `python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'` | Shared numerical helper with P1 becomes necessary, or no independent implementation route | 1–2 h; 0 automatic API |
| **P2b — A4 baseline certificates** | `pilot/baseline/a4_certificate.py`, `pilot/checkers/a4_check.py`, exact input manifests and associated tests. No edits to old reproducer | Export controls chronologically, exact objectives/support sums/multiplier for both datasets. Checker independently propagates A and validates primal/dual equality. `python3 -m unittest discover -s pilot/checkers -p 'test_a4_*.py'`; tampered A/coeff label/control order must fail | Cannot justify upper bound or source transcription; preserve mismatch. No closing-instant solver here | 1.5–3 h; 0 automatic API |
| **P3 — contracts and pure protocol** | `pilot/src/aro_pilot/contracts.py`, `reducer.py`, `pilot/tests/test_protocol.py`; model extension only in `specs/research-pilot-v2/` | Reducer consumes validated events, never touches filesystem. Explicit errors for stale fence, gate closure, cancel/commit race, duplicate/conflicting command IDs. `PYTHONPATH=pilot/src python3 -m unittest discover -s pilot/tests -p 'test_protocol.py'`; TLC extension and both negative controls | Required state is not reconstructible, or a trace cannot be mapped to the model | 2–4 h total, split contracts/model from reducer; 0 API |
| **P4 — durable boundary** | `pilot/src/aro_pilot/journal_adapter.py`, `blobstore.py`, `service.py`, `pilot/tests/test_durability.py`; no existing `src/aro/journal.py` edits in this packet | Temporary isolated roots only. Authorized `aro.journal` adapter with serialization, fsync, command receipts and replay; root cannot resolve to live checkout. `PYTHONPATH=pilot/src:src python3 -m unittest discover -s pilot/tests -p 'test_durability.py'` plus fault matrix below | Journal API cannot guarantee required isolated/durable append; propose separately authorized minimal API change. No fallback writer | 2–4 h; 0 API |
| **P5 — memory and read views** | `pilot/src/aro_pilot/projection.py`, `resume.py`, `view.py`, templates, `pilot/tests/test_views.py` | Rebuild full state; stable evidence retrieval and counterexample selection; CLI/HTML empty/stale/failed/recovered views; resume dossier. `PYTHONPATH=pilot/src python3 -m unittest discover -s pilot/tests -p 'test_views.py'`, browser acceptance OBS-01 | Any primary fact exists only in SQLite; fresh worker needs chat; stale view looks current | 2–3 h; 0 API |
| **P6 — permissions and local integration** | `pilot/runtime/` sandbox definition, `pilot/src/aro_pilot/dispatch.py`, `verify.py`, `publish.py`, public integration tests. Separately reviewed thin `src/aro/cli.py` registration for `ro pilot` only after owner authorization | One local finite episode with genuine checker, journal and board. `PYTHONPATH=pilot/src:src python3 -m unittest discover -s pilot/tests -p 'test_integration.py'`; privilege denial tests and restart resume | Missing actual OS boundary, global gate authority or CLI authorization. Keep isolated dry-run only; never claim production ready | 2–4 h, split permissions from CLI integration; 0 API |
| **P7 — evaluator release** | Evaluator-owned external holdout root (owner supplies path/access). Public additions only `pilot/evaluation/interface.md`, versioned result/report schema | Hidden families below, full trace conformance and fresh-worker test. Evaluator invokes sealed public CLI interface in clean sandbox. All deterministic invariants pass; manifest pins every binary/input | Any invariant failure, holdout exposure, missing required test or nondeterminism; report release blocked | 1–2 h local evaluation + independent review; 0 API needed |
| **P8 — optional paid calibration** | `pilot/src/aro_pilot/meter.py`, gateway adapter and public fake-provider tests; owner alone binds profile/config | Fault-tested reservations before dispatch, request reconciliation, hard caps; only then one approved lower-cost route on same sealed episode as manual baseline. `PYTHONPATH=pilot/src python3 -m unittest discover -s pilot/tests -p 'test_budget.py'`; COST-01..03 | Unknown usage, unavailable tariff/max cap, unbound draft, breach, exhausted attempts; no automatic premium fallback | 1.5–3 h implementation; 0 live calls until owner approval. Then propose ≤2 calls for one worker attempt; measured maximum must fit approved reservation |
| **P9 — bounded Q attempt** | `pilot/science/a4_r80/` and its tests/certificates only; frozen input/checker contracts; separately registered checker | State-realizable policy and rational bounds for r=80; scope/coverage audit, independent replay. If projection unavailable, an inconclusive dossier is the artifact. Acceptance scenario Q in §3 of implementation spec | 2 unexplained discrepancies or sealed compute cap; no schedule search, no coefficient substitution, no new theorem status | 2–4 h exploratory agent work, then stop/re-scope; 0 automatic API. Exact continuous completion is not promised |

No packet can authorize its own newly generated verifier for scientific publication. Independent review and evaluator tests precede registry admission. Authoring a checker and testing it is allowed in scratch; treating its self-reported result as a scientific verdict is not.

## 3. Release plan and acceptance inventory

### Releases

- **R0: offline scientific reference (P0–P2).** No journal writes or paid automation. Four finite semantics cases, two coefficient-specific A4 certificates, independent replay. Owner can reproduce M0. No novelty or source-problem one-measurement optimum claimed.
- **R1: isolated research runtime (P3–P7).** Manual local episode only, actual permissions, durable recovery, board and resume acceptance. No live legacy state migration. Global gates remain closed unless explicitly resolved by owner.
- **R2: metered worker route (P8).** R1 plus tariff/profile approval and spend fault tests. One route before any model comparison. Stochastic observations from one/two runs are case reports, not reliability or savings estimates.
- **Scientific extension (P9).** May follow R0 using offline artifacts. Publication requires R1 and gates; a terminal bundle can state `inconclusive` with useful bounds. A later general claim gets its own question/seal, literature comparison and Lean plan.

Public cases specify behavior and may be used for development. Evaluator owns hidden fixture bytes, expected outputs, injectors and results in a separate filesystem/repository inaccessible to the worker, including git history, shell mounts and logs. The lead specifies families but does not disclose private values. Pin holdout manifest before release; record digest only in public release metadata. A holdout not yet prepared is `not run`, not passing. Exposure retires that holdout and requires a newly sealed one; fixes use a public reproduction, never repeated tuning on secret feedback.

| ID | Public regression | Evaluator-owned holdout variation and oracle |
|---|---|---|
| SCI-01 | Four finite fixtures, exhaustive policies vs independent Bellman, witness replay; infeasible tagged rather than numeric | Different rational coefficients, collisions and correlated suffixes; independently enumerated optimal values and nonanticipativity checks |
| SCI-02 | Printed vs reconstructed A4 inputs; chronological controls and robust support/dual certificate; ignored-A and shared-epigraph tests | Permuted coordinates, modified A and signed reward; exact independent certificate evaluation, not rounded number match |
| SCI-03 | Empty grids rejected; real PDF digest paired with wrong page stays unverified; mutated coefficient label fails | Source/statement swap with plausible text and genuine checksum; anchor comparison prevents admission |
| SCI-04 | Correct Lean theorem or numerical certificate for prefix information submitted as state-measurement result; reject Q scope binding | Valid proof about unrestricted/fixed-list controls lacks adaptive quantifiers/control bounds. Compilation can pass; result must remain wrong-scope. An intentionally false certificate must also fail numeric replay |
| PRO-01 | Same principal claims fence1, expires, reclaims fence2, submits fence1; no accepted submission | Vary expiration/renewal/restart ordering; compare reference reducer and actual state |
| PRO-02 | Verify with gate open, close before commit; publication refused | Missing/changed gate policy, stale gate snapshot, forged actor; no terminal membership |
| PRO-03 | Cancel before/after commit; duplicate same digest, conflicting digest | Schedule race at append boundary; exactly one allowed outcome and no erased publication |
| PRO-04 | Lost submission/publication response; query command ID, resend same request; one receipt/event | Deliver late response after restart and expiry. Old receipt returned; no new attempt or duplicate charge |
| REC-01 | Kill at blob write/install, before append, after append/fsync, before receipt, before projection update | Inject partial writes and disk-full in varied order; either verified old/new state or explicit blocked recovery; never silent truncation |
| REC-02 | Delete projection, replay, compare full logical export including anchors, counterexamples, reservations and owner decisions | Repeated failed replay then successful replay, missing blob and unsupported schema. No dropped fields or false empty success |
| REC-03 | New worker has only journal, blobs and sealed inputs; resumes without earlier chat | Old worker disappears at checkpoint/accepted submission; new worker chooses reclaim vs reconcile correctly; hashes and final evidence preserved |
| COST-01 | Timeout with no usage receipt keeps maximum reservation, available balance cannot increase | Provider accepted call but response lost. No duplicate call, no zero charge and no paid continuation |
| COST-02 | Reservation exceeds run/pilot limit, unbound profile, concurrent paid request denied | Price/tool-charge edge and fractional-cent rounding; fake gateway counts dispatches and tests all caps |
| COST-03 | Late settlement and cancel race; charge over reservation triggers breach | Usage reconciled twice; one settlement; paid route remains blocked until reconciliation. Unknown manual costs stay labeled |
| SEC-01 | Worker cannot write journal/checker/config, read holdout, access network or impersonate owner; injected import path rejected | Symlink/path traversal and untrusted PDF instruction attempts; publisher/checker never execute candidate commands |
| MEM-01 | Exact-scope positive plus correlated negative retrieved; incompatible theorem labeled analogy | Very similar wrong-scope result ranked high lexically must not become evidence; checker-version change blocks dependent reuse |
| OBS-01 | All view fixtures in spec §8, freshness and cost-denominator rendering | Evaluator navigation from state to evidence/blocker/recovery receipt under 60 seconds; real browser check of escaped text and links |
| LANG-01 | English labels/fields/prompts, pinned glossary IDs, explicit polarity | Renamed information field or translation changes meaning; reject schema/scope mismatch rather than guess |

R1 gate: all required deterministic public and private checks pass, both intentional TLC negative cases fail as expected, scientific payloads are byte-identical on two runs, backups/replay restore all logical state, and evaluator can resume without chat. No averaging away a permission or invariant failure. Record omissions as release blockers. Mathematical scope correctness is necessary even when all software tests pass.

R2 compares a manual artifact-producing baseline and one worker route with identical sealed inputs, tool rights and compute caps. Record raw successes/failures/unknown/exhausted counts, accepted evidence, provider usage, reserved/settled/unmetered costs, wall time and owner review minutes. If funding permits two independent runs on the same screened case, report both outcomes and pass^2 with denominator 1 paired case. Do not infer population reliability or cost superiority. Premium escalation is a separate manually approved dossier, not an invisible component of the cheaper route.

Rollback: disable new dispatch/paid gateway, preserve journal/blobs, serve the last verified read view with stale/recovery labels. Do not delete a failed attempt or rewrite scientific history. A release/checker regression invalidates reuse through events and reruns, not overwritten artifacts.

## 4. Complete first-worker prompt

Copy the following assignment as one message into a fresh lower-cost worker session. It intentionally repeats the finite contract so implementation does not depend on this conversation. Owner must attach/select the Bead and authorize starting the packet; this prompt does not authorize a paid API integration.

---

# Assignment P1: exact finite observation reference

You are the bounded implementation worker for P1 of the aro-discovery restart. Implement only the local finite reference described below. Do not build the runtime, inspect holdouts, start subagents or launch paid API calls. End with files, observed test results, limitations and a resume point.

## Project and authority

Source input root: `<workspace>/aro-discovery`.
Design root: `<workspace>/aro-discovery-restart-plan`.
Expected base HEAD: `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`; verify current state, do not assume it is unchanged.
Design files: `docs/specs/2026-11-10-research-pilot-implementation.md` and `docs/specs/2026-11-10-research-pilot-packets.md` under the design root.

Read `AGENTS.md`, `FOUNDATION.md`, current source-root `docs/GLOSSARY.md`, implementation spec §§1–3 and this assignment. Read source-root `specs/research-pilot/check_observation_fixtures.py` only as historical/public input; do not import, wrap or copy its implementation. It returned the four expected triples in the design session, but you must run your own checks.

Run `git rev-parse --show-toplevel`, `git rev-parse --abbrev-ref HEAD`, `git status --short`, `bd prime`, and inspect the owner-selected Bead. If there is no matching owner-created task or no authorized feature-worktree base, stop with `BLOCKED: owner task/worktree binding missing`. Do not create a task automatically or claim an unrelated old task. Work in a new feature worktree from the authorized base, not in either source or design checkout. Claim only the supplied task under the normal Beads workflow. No commit, push, sync, checkout/switch or stash of anyone else's work.

All pre-existing dirty files in the source checkout are other people's work. In particular do not touch `docs/GLOSSARY.md`, `events.jsonl`, `state/science.db`, `specs/research-pilot/`, `artifacts/research-pilot/`, essay/report files, `config/`, `corpus/`, `blueprint/`, existing judges or Lean. No scientific status changes. No `ro attack`, backfill or broad `make check` against the live checkout.

Allowed writes in your worktree only:

- `pilot/baseline/finite_reference.py`
- `pilot/baseline/test_finite_reference.py`
- `pilot/baseline/README.md`

No dependency installation or root configuration changes. Python 3.12 standard library only. Use `fractions.Fraction`, `itertools`, `json`, `unittest` as needed. New functions must use explicit validation, not removable `assert` statements for input checks. No network. This is an offline reference, not an approved scientific judge.

## Exact scope

A two-period scalar finite control game with one exact state measurement at r=1. For each first action a and complete disturbance path (p,q):

- x1 = a + k*p.
- x2 = x1 + b + q.
- x0=0; first actions A0 and second actions A1 are finite nonempty rational sets; k is rational.
- A0 is selected before p. If information=`state`, b depends only on exact x1. If `prefix`, b depends only on p. If `open`, b is one common action for every path. In all cases b is selected before q.
- Path set Omega is a finite nonempty set of rational pairs and may be correlated. Never replace it by a Cartesian product unless those paths are actually present.
- Terminal cost is |x2|. Optional hard terminal interval [lower,upper] must hold on every path. A policy violating it on one path is infeasible. No policy feasible means typed `infeasible`, not zero, NaN, an exception or JSON Infinity.

An instance is a closed JSON object:

`{"schema_version":1,"instance_id":"...","first_actions":["-1/1","0/1","1/1"],"second_actions":["-1/1","0/1","1/1"],"paths":[["-1/1","0/1"],["1/1","0/1"]],"prefix_gain":"1/1","terminal_interval":null}`

`terminal_interval` is null or a two-element rational array. Rational strings must be reduced `n/d`, denominator positive, no whitespace or plus sign; zero is `0/1`. Reject floats/booleans, invalid integers, duplicate JSON keys, unknown fields, unsupported schema versions, empty action/path sets, repeated actions/paths, malformed path lengths, inverted intervals and unknown information modes. Return a clear error, never a success verdict. Arrays are treated as sets and sorted canonically before computation. Pin bounds for this reference: at most 5 first actions, 5 second actions and 8 paths, with |numerator| ≤ 1000 and denominator ≤ 1000. Reject larger inputs as `unsupported_scope`, not `infeasible`; these bounds are reference implementation limits, not the source mathematical domain.

Implement an exhaustive route: for each a, form the observable cells for the requested information class; enumerate every assignment of an A1 action to those cells; propagate each full path and evaluate worst terminal cost/feasibility; minimize over policies and first actions. Use exact rational equality. A `state` cell must pool all suffixes from all paths with that state. Do not optimize separately per hidden prefix. This is finite enumeration, not LP, continuous Bellman, an A4 solver or a theorem proof.

Expose pure functions to parse/validate, solve one information mode, and replay a supplied policy witness. Keep CLI separate. No import-time execution or file writes. A result contains schema version, instance ID, information mode, normalized input SHA-256, result `optimal` or `infeasible`, value (rational string or null), first action (or null), sorted observable-cell/action pairs, and per-path terminal states/costs for a feasible witness. Encode `open` observation key as `open`, state/prefix keys as canonical rational strings. For infeasible results witness fields are null/empty. Result is the reference computation's scoped output, not an authoritative project verdict.

Tie-break deterministically by sorted rational first action, then sorted cells and lexicographically ordered action tuple. Replay validates complete coverage of every reachable cell, no extra keys, actions in allowed sets and information-mode agreement, then checks every terminal constraint and exact value. Replay certifies the witness's feasibility/value, not optimality; only exhaustive search supplies the finite optimality result. Never claim an enumeration is a proof for continuous controls or disturbances.

## Public fixtures and expected answers

1. `strict_gain`: A0=A1={-1,0,1}, k=1, Omega={(-1,0),(1,0)}, no terminal interval. Expected (open,state,prefix)=(1,0,0).
2. `correlated_hidden_disturbance`: A0={0}, A1={-1,0,1}, k=0, Omega={(-1,-1),(1,1)}, no terminal interval. Expected (1,1,0). A prefix policy uses b=-p; that policy is invalid as a state policy because both states are zero.
3. `independent_hidden_disturbance`: same actions/k, all four pairs from {-1,1} squared. Expected (1,1,1).
4. `terminal_feasibility`: fixture 1 with terminal_interval=[0,0]. Expected (infeasible,0,0). State witness a=0,b(y)=-y meets the constraint; no open-loop policy does.

CLI contract:

- `python3 pilot/baseline/finite_reference.py --public-fixtures` emits one canonical JSON object with all four cases and all three information results, then a newline.
- `python3 pilot/baseline/finite_reference.py --input /path/to/instance.json --information state` emits one result using the same schema.
- Exit 0 means a valid computation completed, including mathematical infeasibility. Exit 2 means invalid/unsupported input. Unexpected internal failure exits nonzero and must not emit a fabricated mathematical result. Diagnostics go to stderr. No paths, timestamps or wall time in deterministic payloads.

## Required checks

Use a test-first loop. First tests should fail because the implementation is absent, not because an unrelated environment is broken. Implement only this contract. Required tests:

- Exact values for all four fixtures in all three modes.
- Replay each returned feasible witness and check every path.
- A supplied prefix-dependent action choice on the equal-state correlated fixture is rejected as a state witness, even if it has lower cost.
- Terminal infeasibility is explicit; a changed terminal bound changes feasibility.
- At least one noninteger rational input exercises exact equality/arithmetic.
- Permuting input sets preserves normalized hash, result value and tie-broken policy.
- Tamper with one action or terminal value in a returned witness and replay rejects it.
- Each listed invalid-input category fails without a success artifact; bound overflow is unsupported scope.
- Import module produces no output/writes; repeated CLI output is byte-identical.

Acceptance commands from your worktree:

```
python3 -m unittest discover -s pilot/baseline -p 'test_*.py'
python3 -O -m unittest discover -s pilot/baseline -p 'test_*.py'
python3 pilot/baseline/finite_reference.py --public-fixtures > /tmp/p1-first.json
python3 pilot/baseline/finite_reference.py --public-fixtures > /tmp/p1-second.json
cmp /tmp/p1-first.json /tmp/p1-second.json
```

Use private temporary filenames/directories if the example names exist; remove only your own temporary outputs afterwards. README must explain the exact model, commands, schema, limitations, cost of exhaustive enumeration and the fact that this is not a continuous A4 result. Tests must exercise input-dependent behavior, not simply assert that a hardcoded answer table matches itself. Independent P2 implementation/evaluator checks will later judge this route; do not write or inspect them now.

## Stop and handoff

Stop on a specification contradiction, unavailable authorized worktree/Bead, mathematical disagreement, required dependency, >400 source/test lines without an agreed split, or any need to expand the write boundary. Do not silently change expected values or limits. Preserve a minimal failing case and exact command. If the slice is complete, do not start P2.

Read the `workflow-worker`, `property-testing` and applicable local coding-review skills when available; follow project authority over generic automation advice. Do not initiate parallel agents. Report `DONE` only for the local slice after observed checks, never for the research question or release.

Final handoff in English: status, feature-worktree path/branch/HEAD, Bead ID, allowed files changed, commands and exit outcomes, deterministic output digest, limitations/untested items, cost known/unknown, and the next action for the independent P2 reviewer. No commit or scientific publication.

---

## 5. Material owner decisions before activation

These are proposed review items, not recorded owner decisions. The owner/authorized CLI must bind them through the established decision ledger before live use; no default silently grants scientific or spending authority.

1. Approve M0-first and Q-A4-R80-v1 with literal coefficients and epsilon=1/10000. Alternative: demand a general new theorem immediately, which requires a wider source review and proof budget; do not use this packet unchanged.
2. Select the clean implementation base/input snapshot and create/select the first Bead. Approve a separate pilot lineage with existing journal/CLI authority and decide how current reading/theory-first gates apply. Until then only pure/offline work is safe; journal-library deficiency may need a separate approved fix.
3. Keep automatic paid work disabled initially. Later approve a real model/tariff/cap binding and one bounded manual Astra review. The draft ceilings do not become approved through accepting a design document.

Editorial approvals can wait without changing implementation: Russian equivalents for `lease`, `publication`, `scope`, `evidence_bundle` and `research_disposition` in the current glossary remain proposed wording. Internal IDs/English definitions are fixed by the sealed glossary; translations must not substitute disturbance observation for state measurement.
