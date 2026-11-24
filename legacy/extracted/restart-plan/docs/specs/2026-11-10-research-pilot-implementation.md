# Research pilot: implementation specification

Status: proposed for owner review; no runtime, scientific status, corpus admission, configuration change or paid execution is authorized by this document.
Date: 2026-11-10. Design base: `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac` plus the explicitly fingerprinted working-copy inputs in the companion review record.

## 1. Decision and boundaries

Build an independent, manually started research runtime for one sealed question and one worker slot. First implement an exact finite observation reference in isolation. Next establish the durable protocol, independent checking and owner view. Only then connect a mathematical submission to internal publication. Paid automation is a later release, not a prerequisite for a useful baseline.

The research decision is whether a fixed-measurement method can be used as a trustworthy comparator on the literal A4 example, with a realizable policy and certified bounds. The first milestone is the reproducibility package, not a new theorem. The factory is a research instrument, not the proposed dissertation contribution.

This specification supersedes the **design recommendations** of `docs/specs/2026-11-10-research-harness-pilot.md` for review. It does not supersede FOUNDATION, human decisions, frozen grids or existing gates. Work packets and the paste-ready first assignment are in `2026-11-10-research-pilot-packets.md`. Fresh checks and source fingerprints are in `../../reports/2026-11-10-restart-plan-review.md`.

### Consequential changes from the proposal

| Gap | Decision now | Evidence that would change the decision |
|---|---|---|
| An LP, a Bellman computation and a prefix policy can describe different games | Seal dynamics, information fibres, timing, feasible controls and terminal conditions before choosing a solver; test policy realization separately from value equality | A checked realization/equivalence theorem for an enlarged scope |
| A3 can be read as an unconditional exact finite LP | Record rank conditions, directions and approximation error explicitly. Reproduce its route; do not call an outer approximation the exact source problem | Exact set representation or certified two-sided error bounds |
| The proposed journal conflicts with the established write authority | Use `aro.journal` behind a narrow, serialized adapter and eventually a `ro pilot` entry point. No direct JSONL writer and no writes to the live legacy journal during the pilot | Owner-approved charter change or a tested compatible journal API |
| TLC logs only terminal publication, not all recoverable control state | Journal all accepted control transitions; rebuild leases, reservations and checkpoints too. Extend the model before enabling a live writer | Trace refinement and crash-injection evidence, not another TLC success on the original model |
| Single terminal publication can discard negative or intermediate work | Preserve every accepted submission/check/checkpoint in the journal; one terminal bundle per question version selects references to them. A negative result can be terminal | Multiple active questions or incremental publications become necessary; revise uniqueness/model first |
| Baselines share some code and do not emit portable certificates | New finite route independent of legacy code; exact certificate checker separate from optimizer; normalize scientific output bytes | Mutations survive both checks: add a genuinely different route before trust |
| Runtime status, scientific status and usefulness can be conflated | Separate state machines and authorities (§5); `committed` does not mean `attested` or novel | No relaxation planned |
| Draft dollar ceilings are not a validated execution profile | Local-only initially; explicit binding, tariff and maximum-charge proof before any automated paid request | Measured calibration under approved ceilings |
| New worktree omits dirty/untracked pilot inputs | Bind an input inventory before code; never infer that HEAD contains these files | Owner integrates the reviewed input snapshot |

Stigmergy contributes durable signals, readiness derived from dependencies, a fenced lease, a narrow submission proxy and replayable handoffs. Its runtime, task lifecycle, auto-merge rules and budget counter are not dependencies. Local `../stigmergy/docs/spec.md` §§7–8 was inspected. Beads remains the human-maintained implementation tracker; no scheduler creates Beads. Packet IDs below are specification references, not a second task tracker.

Non-goals: migration of the legacy graph, general autonomous research, schedule optimization, noisy outputs, multi-worker exploration, embeddings, automatic thesis writing, automatic corpus promotion, unattended premium escalation, and repairing all legacy claims. Do not copy old verdicts into the new blueprint. Keep old history read-only and visibly separate.

## 2. Source review and epistemic boundary

Primary anchors directly reviewed in this session:

| Source | Anchor and closest result | Consequence |
|---|---|---|
| A2, Dmitruk 2018 | `corpus/our_papers/A2_Дмитрук_2018.pdf`, PDF p.16, Example 2: numerical minimum at 6.8; Example 3: no gain example | Comparing closing instants numerically and finding no gain are not new contributions |
| A3, Kastsiukevich–Dmitruk 2021 | `corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf`, PDF pp.7–9, (16)–(20): LP and rank-dependent construction, approximation directions, h=0.1, fixed instant 80 | Direct method comparator. State the approximation and its bound; do not relabel LP agreement as a new reformulation theorem |
| A4, Dmitruk 2022 | `corpus/our_papers/A4_Дмитрук_2022.pdf`, PDF pp.3–6, (1.2)–(2.8), and rendered p.12, Example 1 | Terminal constraints, scheduled exact state measurement, block Bellman construction and printed benchmark |
| Dmitruk 2023 | Math-Net `into1170`, PDF pp.4–5, §3, digest in review record | Distinguishes scheduled block strategies from feedback obtained by repeated replanning at intermediate times. Do not give the pilot those extra measurements |

A2 p.16, A3 p.7, A4 p.12 and Dmitruk 2023 p.5 were rendered and visually inspected; PDF text was read for adjacent definitions. Before implementation seals formula inputs, record page regions and independent transcription checks for every used coefficient and hypothesis. The 2023 PDF remains an external review input, not a newly admitted corpus item.

The existing reading report identifies Vayanos–Georghiou–Yu (decision-dependent information), exact convex ARO methods, Dmitruk 2025 and costly observation scheduling. Their detailed theorem comparison was **not repeated here**. In particular the 2025 full text remains a missing check. These are discovery leads only in this plan. A finite baseline and runtime can proceed without them. Any novel claim about general measurement timing, output information or affine-rule exactness must stop at that missing comparison. No global novelty claim follows from this screen.

Historical code, Lean drafts and S1–S5 are `origin: legacy-archaeology`. They may suggest tests; their former status has no force in this episode. A new scientific dependency needs a fresh source anchor or a fresh checked artifact. Legacy warning cases include shared coordinate epigraphs, ignored A, a proof over a fixed control list instead of adaptive policies, and a prefix-indexed LP described as measured-state control.

## 3. One scientific episode

### 3.1 Sealed question Q-A4-R80-v1

**Question:** On the literal printed A4 Example 1 with one exact state measurement at r=80, can we certify a positive guaranteed-reward gain over open loop and a state-realizable policy whose reward is within epsilon=1/10000 of the optimal one-measurement reward?

Epsilon is a proposed acceptance tolerance, not an approved grid/config change. It is included in the owner-approved question digest before execution. The reconstructed-coefficient instance is a separately labeled sensitivity/reproduction comparator, not a substitute when the literal instance fails. One question remains active; baseline fixtures are its prerequisites, not additional research questions.

Positive: an admissible measured-state policy has certified lower reward L, a valid upper bound U satisfies U-L ≤ epsilon, and L-J_open > 0. This establishes a usable fixed-r baseline and justifies comparing a later restricted policy or algorithm against it. It does not establish novelty.

Negative: a certified bound proves no positive gain (U ≤ J_open; feasibility of open loop supplies the opposite bound). Retain the no-benefit baseline, and do not use this instance to motivate measurement benefits. A certificate for a different proposed method's infeasibility rejects that method only, not Q. A failed solver is never a negative mathematical answer.

Inconclusive: missing anchors, unavailable exact projection, L ≤ J_open < U, U-L > epsilon, checker disagreement or resource exhaustion. Preserve feasible witnesses and intervals, stop, and recommend the next discriminating check. Do not widen the grid or switch coefficients to obtain success. A positive gain with a wide optimality gap is a useful partial result but does not resolve Q.

The affordable first milestone is **M0: four finite fixtures plus freshly checked A4 open-loop certificates**. Q may remain inconclusive at M0. Completion of M0 is accepted as a baseline milestone, not silently reported as answering Q. A bounded follow-on attempt at the continuous r=80 calculation needs the same approved episode scope and an additional compute envelope; it is not a prerequisite for building the local reference or protocol.

### 3.2 Exact source instance and timing

For t=0,...,119:

- x(t+1)=A x(t)+B u(t)+E w(t), x(0)=(0,1).
- A=((0.9950,0.0998),(-0.0998,0.9950)); B=E=(0.0050,0.0998)^T.
- Every decimal above is an exact rational. u(t) in [-1,1], w(t) in [-1/2,1/2]. Disturbances form the full rectangular product; no distribution or correlation assumption is substituted.
- Terminal set X_T={x: 2 ≤ x_1 ≤ 10}; maximize inf_w x_2(120), subject to terminal feasibility for every path.
- Before w(0), choose the entire program a=(u(0),...,u(79)). No intermediate observations or replanning.
- At r=80, after w(79) has affected x(80) and before w(80), observe exactly y=x(80). Choose all b(y)=(u(80),...,u(119)). No subsequent observations. The controller knows a and the instance, but not the prefix disturbances themselves.

Let F_r(a,p) be state propagation for p=(w(0),...,w(79)). Prefixes are equivalent iff F_r(a,p)=F_r(a,p'). A permissible suffix policy is constant on each such fibre. For this additive linear model,

F_r(a,p)=A^r x_0 + sum_{t<r} A^{r-1-t} B a_t + sum_{t<r} A^{r-1-t} E p_t.

Thus equality of observations cancels the common initial/control terms. The equivalence relation is independent of a **in this stated model**. Do not generalize this to control-dependent observation maps, disturbance sets or uncertain dynamics. Continuous fibres are not the same as equality of enumerated vertex states.

For an arbitrary finite path relation Omega, define Q_a(y)={q: there exists p with (p,q) in Omega and F_r(a,p)=y}. With terminal cost extended by +infinity outside X_T, the finite reference is

V_state(r)=min_a max_{y reachable under a} min_b max_{q in Q_a(y)} g_bar(F_suffix(y,b,q)).

Q_a(y) is the **union** of continuations across indistinguishable prefixes. Using the continuations of a single hidden prefix gives the controller extra information. Rectangularity permits a common suffix set; the correlated fixture does not. This formula is the proposed executable definition for finite instances, independently checked by enumeration of complete policies.

Comparators:

1. Open loop: one (a,b) chosen before any disturbance.
2. State measurement: b depends on y only.
3. Prefix information: b may depend on p; a relaxation used to detect leakage, not the source policy class.
4. Full state feedback: actions can depend on successive state observations; excluded from Q's solver, useful only as a labeled bound when justified.

Use minimization internally with c=(0,-1) for A4, so V=-J for feasible policies and infeasibility is +infinity. Display A4 results as guaranteed reward J; never negate infeasibility into a finite value. In minimization, V_full ≤ V_state ≤ V_open and V_prefix ≤ V_state. No ordering of prefix-at-one-instant and full state feedback is asserted without further information assumptions.

### 3.3 Finite public fixtures (M0 semantics, not a discretization proof)

All use T=2, r=1, x0=0, scalar state, suffix controls {-1,0,1}, cost |x2|. Controls are chosen before their corresponding disturbances. Paths are complete admissible disturbance pairs, not a probability distribution.

| ID | Model | Expected (open,state,prefix) |
|---|---|---|
| strict_gain | u0 in {-1,0,1}; x1=u0+w0; x2=x1+u1; paths (-1,0),(1,0) | (1,0,0) |
| correlated_hidden_disturbance | u0=0; x1=0; x2=u1+w1; paths (-1,-1),(1,1) | (1,1,0) |
| independent_hidden_disturbance | Same dynamics; all four sign pairs | (1,1,1) |
| terminal_feasibility | strict_gain with x2=0 required | (infeasible,0,0) |

First use exact integers/rationals and complete finite policy enumeration; use a separately implemented state-fibre Bellman check later. The two routes must not import each other's dynamics or partition helpers. They may share a checked schema and arithmetic library. Tests compare witnesses, every terminal outcome and the optimal values. Empty inputs, incorrect observation names and malformed rational values are errors with no scientific verdict.

### 3.4 A4 coefficient provenance and independent routes

Keep two manifests:

- `a4_printed`: c=0.9950, s=0.0998, B_x=0.0050, B_y=s. Fresh run of the historical rational script returned J_open=1.495710098124 (rounded display).
- `a4_reconstructed_decimal`: c=0.9950041652780258, s=0.09983341664682815, B_x=1-c, B_y=s. Fresh run returned 1.501101989382, rounding to the printed result 1.501102. These decimals are exact rational inputs; they are not exact cos(0.1)/sin(0.1) and not confirmed author inputs.

For portable evidence, export the actual rational objective, control vector in chronological time order, support terms and dual multiplier. The existing script stores columns by powers of A; reverse indexing explicitly when exporting a policy. A separate checker propagates nominal controls chronologically, verifies the robust terminal slab by exact support bounds, evaluates guaranteed reward, and checks the independent dual upper bound. Decimal agreement alone is insufficient.

For Q after M0, choose a polyhedral value/feasibility-set route in measured state, compared to the A3 fixed-instant construction. The suffix epigraph consists of (y,z) for which a bounded suffix program robustly meets X_T and has worst cost at most z. Eliminate controls with certified rational projection or a complete dual representation, and test containment of the prefix reachable set. Keep projection certificates and all retained inequalities. A3 directional approximations must supply a direction of bound and a certified residual gap. Vertex scenario recourse is not a continuous-state policy until a checked extension/realization argument is supplied. A sampled Bellman grid cannot certify Q. If exact projection grows beyond the sealed compute cap, return the available bounds and `inconclusive`; do not implement a general solver as an unbudgeted prerequisite.

Lean is reserved for a central general equivalence/realization claim if the owner selects it. Its statement must quantify admissible policies, observations, controls, disturbances and terminal constraints. Require a pinned toolchain, `lake build`, no `sorry`, an axiom audit and independent intended-statement correspondence. An abstract monotonicity theorem or a bound for an unrestricted strategy type does not certify Q. M0 requires no new general theorem and confers no `formalized` status.

## 4. Implementation architecture and authority

Use a new package boundary `pilot/src/aro_pilot/`, local Python 3.12 initially (observed 3.12.3). Standard-library JSON, Fraction, unittest and SQLite suffice for the first slices. No legacy numerical imports. No Stigmergy/Pi/workflow runtime dependency. Revisit the runtime only if one-worker throughput or evidence volume becomes a measured limitation.

```
Owner-approved seal -> deterministic readiness -> dispatcher lease
  -> isolated worker scratch -> typed submission ingress
  -> pinned deterministic verifier -> publisher -> journal + immutable blobs
                                               -> replay -> blueprint/read views
Owner decision CLI ----------------------------^                 -> local HTML
```

One trusted local writer serializes **all** journal-affecting requests. Dispatcher, verifier and publisher are separate capabilities even if deployed in one supervisor. Worker code and verifier code run in separate processes. Untrusted submissions are data, never module names, shell commands or import paths. Registered checker IDs resolve only through an owner-approved digest registry.

| Actor | Authority | Enforced denial |
|---|---|---|
| Worker | Read sealed inputs, write its scratch, submit data/checkpoints with lease token | No journal, corpus, registry, configuration, blueprint, holdout or provider-key access |
| Dispatcher | Grant/renew/expire leases and reserve capacity via serialized command handler | Cannot issue scientific verdicts, approve scope or attest |
| Verifier | Read immutable inputs/submissions; execute pinned checker; issue typed checked result | Cannot install its own generated checker, change a claim, attest, or bypass publication gates |
| Publisher | Verify command identity, checker result, gates and cancellation; append authorized events | Cannot fabricate verification or infer human approval from a text field |
| Owner | Approve seals/budgets/checkers/grids, decide research role, attest through existing authority route | No automatic impersonation of actor `human` by agents |
| Evaluator | Own private tests and release verdict, inspect traces/read views | No scientific attestation; no secret test disclosure to coding worker |

Filesystem permissions/container mounts enforce these boundaries, not prompts. Worker gets a scratch directory and read-only input mount, no home mount or inherited credentials, no default network, bounded CPU/memory/PIDs/wall time. Verifier gets read-only registry and artifacts; no worker-writeable module lookup path. Publisher receives only validated data. A worktree alone is not a sandbox. Process peer identity/capability comes from supervisor channels; payload `actor_id` is not authentication. Local HTML is read-only, escapes all submitted text, exposes only allowlisted content-addressed artifact paths, and has no mutation endpoints.

### Journal authority and adoption gate

The pilot journal is a new lineage in an isolated run root. Before any persistent writer, inspect the installed `aro.journal` API and demonstrate root selection, serialized hash computation and durability on a copy. Wrap every append under one OS lock, including gate/lease/budget events; an external lock is insufficient if another authorized writer bypasses it. Reuse only the minimal journal serialization API; do not import the old runner, graph or judges. If it cannot meet the contract without modification, stop P4 and propose a narrowly scoped journal-library change for owner review. Do not invent a second writer to work around the restriction.

All live state-changing user operations must be exposed through `ro pilot` under FOUNDATION §11; internal services call the authorized journal library. Offline pure computations and temporary test journals do not authorize live integration. Existing global reading/theory-first gates remain in force until the owner explicitly scopes them for the new lineage. The service rechecks current gate policy at commit. Unknown/stale gate evidence means closed. No edits to live `events.jsonl`, `state/science.db`, `blueprint/`, `config/` or `corpus/MANIFEST.md` in implementation packets without an explicit packet and owner authority.

Fresh blueprint YAML records are generated from authorized judge/owner events and evidence in the new lineage, never imported from legacy statuses. SQLite and HTML are rebuildable indexes, not alternate scientific truth stores. No field may exist only in SQLite. Checkpoint drafts are operational artifacts, not approved claims. No batch ingestion of historical claims.

## 5. Records, transitions and recovery

### 5.1 Canonical contracts

Canonical data: UTF-8 JSON, sorted keys, compact separators, newline-terminated journal record; integers and reduced rational strings `n/d` with positive denominator; no floats, NaN or Infinity. Encode infeasibility as a typed value. Reject duplicate JSON keys, unknown enum values and missing required fields. Operational timestamps/usage are excluded from deterministic scientific payload hashes. Version schemas explicitly; unknown schema version blocks replay instead of skipping an event.

| Record | Required content |
|---|---|
| Question seal | question ID/version, full scope and statement digests, objective polarity, dynamics/data digest, timing/information model, constraints, comparators, falsifier, success/negative/inconclusive rules, checker/acceptance/glossary digests, dependency IDs, profile and owner approval reference |
| Event envelope | lineage ID, schema version, event ID, strictly increasing seq, previous hash, event hash, command ID and request digest, trusted actor/role, UTC timestamp, question/version, episode ID, optional attempt/fence, causal event ID, typed payload |
| Lease | episode ID, attempt ID, monotone fence, worker principal, question/seal digest, granted time/deadline, maximum attempt deadline, worker boot/session ID, budget reservation references |
| Submission | submission ID, command ID, exact seal/attempt/fence, input digest, immutable manifest digest, artifact references and sizes, checkpoint reference; no executable paths |
| Evidence item | ID/digest/path, media type, statement/scope/input/checker/environment digests, origin, source anchors, method, explicit coverage, arithmetic, result, witness/certificate refs, dependencies |
| Source anchor | original PDF digest, file identity, one-based page, region, exact excerpt, transcription reviewer/check record; quotation mismatch stays unverified |
| Check result | checker ID/digest, bound submission/statement/scope, result enum, coverage, witness replay result, duration in operational envelope, deterministic payload hash |
| Checkpoint | seal digest, completed steps with artifact IDs, unresolved blocker, next permitted command, required rights, dependencies, remaining reservations, last observed seq; a checkpoint's claims are not self-certified |
| Terminal bundle | unique (lineage,question,version), manifest hash, exact accepted evidence/check IDs, research outcome and limitations, cancellation/gate/policy refs; no automatic usefulness/attestation |
| Owner disposition | authenticated decision reference, exact statement/evidence version, disposition and reason; historical attestations do not carry to revisions |

Check results: `pass`, `counterexample`, `infeasible`, `scope_mismatch`, `invalid_input`, `checker_error`, `timeout`, `inconclusive`. A witness of infeasibility can be mathematical evidence; absence of a witness or a crashed solver cannot. An operationally rejected submission is not a refuted mathematical statement.

### 5.2 Three state dimensions

Operational phase:

`draft -> ready -> leased -> submitted -> validated -> committed`

Branches: `submitted -> rejected -> ready`; `leased -> ready` through expiration; nonterminal -> `canceled`; ready with exhausted attempts -> `deferred`. Blockers are typed overlays on a phase, not an alternative unknown transition. `blocked` includes cause, responsible actor and unblock condition. `recovering` is a service/view state; it cannot issue work until reconciliation completes.

Scientific status uses FOUNDATION names and scoped evidence: seed/conjectured, survived-falsifier, numerical, dual-verified, formalized, attested, refuted, descoped. Only registered code judges cause numerical transitions; only an authenticated owner attests. A finite check records its domain; it cannot promote a universal statement. New questions and drafts need no imported scientific status. Publication is internal evidence membership, not proof strength.

Positioning fields remain separate: `correctness` (including unverified), `scope_match`, `novelty_review` (known reproduction/unresolved/bounded delta), `usefulness_proposal`, and owner `research_disposition`. A valid proof with wrong scope remains valid evidence for its actual statement and unusable for the requested conclusion. None of these fields is a scalar scientific score.

### 5.3 Transition guards and linearization

- Seal: owner approval references exact bytes; one active version. Any change to assumptions, checker, acceptance tolerance, glossary definitions or data creates a new bound version. An approved version is immutable.
- Claim: ready, dependencies valid, no active worker, approved non-draft profile and sufficient budget/capacity. Append `lease_granted` before returning. Attempt budget is non-refundable; increment fence monotonically even after restart.
- Renewal: current worker/fence only, before deadline, bounded by attempt maximum. Persist `lease_renewed`; heartbeats alone cannot extend authority. Proposed lease 300 s, heartbeat 30 s, total attempt 1800 s; all remain draft until owner approval.
- Expiration: under the same lock, compare trusted time then append expiration/requeue. On service restart expire outstanding unsubmitted leases conservatively before granting new ones; saved scratch survives. Clock rollback or unverifiable time causes recovery block. A stale heartbeat must not make a lease look current.
- Submit: lock; validate identity, seal, active phase/fence/deadline, cancellation, blob availability and request digest. Copy/verify bytes into immutable storage, then append `submission_received`. That durable acceptance transfers ownership to verification; lease expiry afterwards does not invalidate accepted work and does not reopen a worker slot for another competing submission. Only one accepted submission per attempt.
- Verify: consume immutable submission using pinned registry. Append bound result. Rejection/requeue is explicit and spends a new attempt; same content/checker may reuse a prior deterministic result only with exact bindings and an explicit event. Timeout/crash blocks; it does not silently requeue or consume premium calls.
- Commit: lock and replay/validate tip; validated result, exact seal, current policy and all gates, no winning precommit cancellation, no prior conflicting terminal bundle. Append once after durable blobs. Same key and digest returns original receipt; same key/different digest is `PUBLICATION_CONFLICT`. The command handler performs retry lookup before new-transition guards: a duplicate accepted submission after lease expiry returns its old receipt, not a new acceptance or a stale-write error.
- Cancel: append under the same lock, fence off future worker writes, stop worker process and tools. Before commit it prevents publication even if verification completed. After commit it records `stop_requested_after_commit`; evidence remains. Correction needs a new version and superseding reference, never overwrite. Process termination and provider charge reconciliation are reported separately from cancellation acceptance.

All commands have caller-generated idempotency IDs and canonical request digests. Same ID/digest returns the original receipt even after a lost response; same ID/different payload fails `IDEMPOTENCY_CONFLICT`. The journal persists IDs; a response cache is disposable. Different duplicate publication IDs still collide on the terminal uniqueness key. A stale worker may keep scratch, never alter authoritative state. Denied requests go to a bounded security trace, not scientific verdicts.

### 5.4 Durability and unknown outcomes

Commit sequence on a local filesystem: validate -> write temporary blob -> fsync blob -> atomically install content-addressed blob without overwrite -> fsync containing directory -> acquire/retain writer lock -> validate current tip/guards -> authorized library append -> fsync journal -> acknowledge seq/hash. The journal event is the membership commit point. Blob digest validation and size limits precede parsing; reject symlinks, traversal and mutable references. Verify these filesystem assumptions with actual fault injection before activation; network filesystems are out of scope.

| Interruption | Required recovery |
|---|---|
| Before blob completion | No receipt/event; discard only owned temporary data after reconciliation |
| Blob durable, no event | Orphan is not published; retry same command may reuse exact bytes |
| Event durable, response lost | Look up command ID and request digest; return original seq/hash; do not append again |
| Append/fsync outcome unknown | Stop writes, scan/verify journal. Complete valid record is reconciled by ID; invalid/partial tail blocks with verified prefix and forensic bytes preserved. No automatic truncation |
| Projection missing/partial | Replay to a new temporary projection, validate full logical export and blob references, atomically switch view; no scientific event is lost |
| Publisher process restart | Recover command dedup, cancellations, gates, reservations and fences before admitting requests |
| Disk-full/permissions/corrupt blob | Explicit `storage_error`/`evidence_missing`; block affected work, preserve last verified view and exact failure |

Hash chaining detects changes but does not authenticate a principal or guarantee fsync. Access control and physical durability tests are separate obligations. No acknowledgment until the configured durability boundary is crossed. Backup test restores journal, blobs and sealed inputs into an empty root and compares complete logical state; a SQLite-only backup is insufficient. Retain all cited evidence, refutations and journal events; provisional raw telemetry retention is 30 days, subject to owner approval. Keep raw traces redacted and never required for scientific replay.

## 6. Model correspondence and limits

The existing TLC model has one question version, two possible workers, two attempts, one Boolean admissibility flag and one terminal log entry. It assumes trusted verification and atomic durable append. It does **not** persist precommit phase/lease state in `log`, model deadlines, renewal, budget dollars, multiple evidence records, command IDs or torn writes. Its `EventuallyVisible` uses weak fairness of Replay and guarantees eventual visibility, not a recovery SLA or permanently fresh view after arbitrary repeated projection loss.

| TLA+ action/invariant | Implementation mapping | Public test |
|---|---|---|
| Claim / AttemptBudget | claim guard + non-refundable attempt/fence event | third claim refused after two attempts |
| Expire, Requeue | explicit expiration/rejection then new lease | same principal reclaims, old fence denied |
| Submit / SingleCurrentWriter | locked ingestion with identity/fence/seal/time | stale-fence submission leaves accepted state unchanged |
| Verify | registry-bound code judge capability | worker-authored `pass` cannot become validated |
| SetGate | authenticated policy/gate event | close gate between verification and commit |
| Cancel | serialized cancellation before terminal append | races on either side of commit |
| Commit / AuthorizedCommit / OneAuthoritativeCommit | durable terminal bundle, uniqueness and guard recheck | closed gate, duplicate same/different payload |
| LoseProjection, Replay / ProjectionNeverLeads | rebuild disposable indexes from full journal | no view sequence exceeds verified tip |
| EventuallyVisible | fair restart/replay after finite faults | crash then successful replay reaches committed bundle |

Map implementation traces to this abstraction by filtering nonterminal journal entries out of abstract `log`, mapping attempt fence to `attempt`, and mapping operational telemetry/checkpoints to stuttering steps. Compare actual transition traces against the abstract actions. Extend a separate model revision before persistent integration to cover durable control-log replay, renew/restart expiry, accepted submission surviving lease loss, two command identities, duplicate receipt and cancellation-after-commit. Keep one question/version in the release model; revision/next episode happens only after manual closure.

Retain negative model controls `AllowStaleSubmission=TRUE` and `AllowGateBypass=TRUE`, expecting invariant violations rather than a green run. New negative controls should remove dedup or durable lease recovery guards. Exact wall-clock behavior, OS sandbox escapes, symlink/race handling, partial writes/fsync, provider billing, source transcription, mathematical truth, schema validation, projection completeness and Lean statement correspondence require implementation/evaluator tests beyond TLC.

## 7. Memory with a concrete purpose

The memory query answers: **What can this worker safely reuse to execute the next sealed step, and what already rules out a tempting shortcut?**

Retain immutable source anchors, scoped statements and assumptions, code/Lean/checker versions, complete witnesses and counterexamples, original negative results, episode checkpoints, operation outcomes, cost reservations and owner decisions. Keep original provenance when deriving a smaller context packet. A discovery lead is not a theorem record. Legacy items are returned only in an explicitly separate historical/analogy section.

Initial retrieval is deterministic indexed filtering, no embeddings: exact question/version -> valid dependencies -> matching information/timing, objective, constraints, uncertainty domain and arithmetic -> known contradictions/counterexamples -> closest source comparators -> unresolved blockers. Stable sort by relation, evidence ID. Return selection reason and exclusion reason for near matches. Include correlated hidden disturbance when retrieving any prefix-based method, even if positive examples rank higher.

A resume packet contains seal bytes and hashes, glossary IDs, input/corpus/checker inventory, last verified sequence, current phase and authority, accepted artifacts and check outcomes, negative evidence, remaining budget/unknown charges, current blockers and one next permitted action. A fresh worker receives only this packet plus journal/artifacts, never earlier chat. It verifies hashes and queries command receipts before resubmitting. It does not reuse an expired lease.

Invalidation is explicit: changed scope/data/observation or objective -> reuse denied; changed checker/runtime -> `revalidation_required`; changed source transcription -> dependent facts and certificates blocked; changed owner disposition -> positioning changes but old checked bytes remain. Propagate through `depends_on` and `reproduces`; do not automatically treat `analogous_to` as proof dependence. A broader theorem may support a narrower claim only through a reviewed specialization mapping, never substring/similarity matching. All prior states remain inspectable. Test retrieval by seeding a very similar wrong-scope theorem and a less similar decisive counterexample.

## 8. Observability is release behavior

Provide `ro pilot status --root ... --json`, a readable CLI rendering and regenerated localhost HTML. These are **planned interfaces**, not commands available today. All display state comes from the verified journal plus a freshness envelope. Scientific payloads remain deterministic; rendering timestamps are operational data.

Every page shows lineage, source seq/hash, projection seq, generation time/time zone, freshness/telemetry status, episode/attempt, question/scope, worker identity, lease deadline and age, last checkpoint, blocker owner, next permitted action, latest evidence links and usage. Timeline separates generation, checking, publication, owner review and recovery. Each item opens its original certificate/anchor and coverage. No green `Verified` badge collapses validity, scope, novelty and usefulness.

| View fixture | Required labels and next action |
|---|---|
| Empty approved root | `No sealed question`; spent=0 only for known empty ledger; `Await owner-approved question` |
| No readable root/telemetry | `Data unavailable`, never empty success or zero spend; last known seq if available |
| Ready | Why dependencies pass; `Ready — manual start required` |
| Active | `Leased`, current checkpoint, deadline, reserved/settled spend; expected next artifact |
| Stale heartbeat | `Telemetry stale — process state unknown`; no claim that computation stopped; lease authority displayed separately |
| Expired | `Lease expired`; prior scratch/checkpoint; reclaim only after expiration/reconciliation |
| Failed verification | `Checker error` or `Scope mismatch` with distinct consequence; no scientific refutation on crash |
| Gate blocked | Which reading/policy approval is absent, responsible owner, exact unblock requirement |
| Unknown spend | Known settled + locked reservation + unknown amount/status; `Paid route blocked — reconcile request ...` |
| Recovering | Last verified view, its age and prefix, `Recovery in progress`; all writes disabled |
| Recovered | Replayed seq/hash, original publication receipt, no duplicate result; explicit recovered marker |
| Committed negative/partial | Counterexample/interval and coverage, not a generic failed run; next owner decision |
| Canceled after commit | Publication remains; future work stopped; outstanding provider reconciliation still visible |

Acceptance: an evaluator unfamiliar with the implementation can locate current activity, blocker, evidence, next action and cost uncertainty within 60 seconds per fixture and without chat. This is a usability target to measure, not a measured result. Structural assertions check required labels/links and state, then a real browser test checks rendering, escaping, stale behavior and artifact navigation. Cost per accepted packet is `not available — no accepted packets` at zero denominator. Research outcomes and engineering release results have different counters. No notification service/background watcher is needed for the manually started pilot.

## 9. Affordable routing and stopping

Initial profile: one question, one worker slot, local deterministic checks, zero automatic API calls. Proposed worker packet estimates are agent-effort estimates, not provider prices or billing guarantees. The current planning session's usage was not measured by this plan and must not be recorded as zero.

Later API activation requires an explicit owner-bound model ID from the one-provider policy, verified current tariff, context/output/reasoning/tool charge caps, and tested gateway enforcement. Candidate model names in the old YAML are unverified suggestions, not supported routing identifiers. Do not edit `config/` or activate the draft YAML. The 500-cent pilot / 150-cent run / three-run proposal remains a ceiling proposal, not an instruction to spend or a claim of affordability. The sum of three 150-cent runs is at most 450 cents; remaining capacity is not a fourth run. Premium subcaps and manual review accounting must be separate, explicit constraints.

Routing: code handles readiness, retrieval, validation, replay and rendering; one lower-cost coding worker implements a bounded packet. There is no economy-to-premium automatic fallback. Escalate only a packet containing competing explanations, failed checks, remaining alternatives, a precise decision and projected cap. Reserve one manual Astra review, proposed 30 minutes and one dossier; do not assume subscription/manual use is monetarily free. Record manual time and `unmetered` cost when no bill is available. Further review requires owner approval.

Before a paid request, reserve a conservative **maximum charge** against both run and pilot in integer cents, rounding upward. Include all billable input/output/reasoning/tool charges using a pinned tariff. Available = approved cap - settled - outstanding reservations. If a maximum cannot be enforced or computed, refuse the request. Persist reservation and provider request ID before dispatch. On known success settle actual usage, release unused reservation; assert actual ≤ reserved. On timeout/lost response retain reservation, mark usage unknown, reconcile by request ID. Do not dispatch a replacement request until absence/nonexecution is established. A missing receipt is not zero. A cost exceeding the reservation is an accounting breach: stop, preserve full actual charge and alert; never clamp the ledger to cap.

Local verifier work may proceed after unknown API usage only if already authorized in its own compute cap; all automatic paid work blocks. An unknown manual charge outside a metered ledger must remain separately visible and blocks any claim about total pilot cost. No silent retries: at most one explicit retry of a documented transient transport failure after reconciliation, charged to existing attempt/call caps. New mathematical guesses are new attempts, not retries.

Proposed stop conditions to seal: two research attempts per version, at most two unexplained discrepancies before the FOUNDATION dossier route, two consecutive runs with no usable new evidence or resolved decision, one active paid request, 1800 s worker attempt and 300 s checker pass. Stop immediately for stale authority, checksum mismatch, empty coverage, unknown source required by a claim, nondeterministic scientific output, permission breach or corrupt journal. Q's continuous projection has its own preapproved compute cap; never expand it automatically. A checker upgrade, new fixture grid or increased budget requires owner approval and a new binding. No Stigmergy counter is used; if one is later reported, its units are заклёпки, distinct from tokens and USD.

## 10. Obligations traced to acceptance

| Obligation | Enforcing mechanism | Observable failure | Acceptance ID |
|---|---|---|---|
| H1 sealed scientific contract | immutable schema/digests, timing/polarity/coverage fields | missing/wrong information model | SCI-01, SCI-04 |
| H2 durable handoff | checkpoints and complete replay, no chat dependence | fresh worker cannot identify next authorized action | REC-03 |
| H3 separate authority | sandbox + capabilities + pinned registry + owner route | worker creates verdict/attestation or reads holdout | SEC-01, SCI-04 |
| H4 append-only provenance | journal adapter, lock, immutable blobs, receipts | stale/duplicate/partial write corrupts membership | PRO-01..04, REC-01..03 |
| H5 validity/scope/novelty/usefulness distinct | bound statements, scope registry, separate review fields | correct unrelated proof accepted for Q | SCI-04, MEM-01 |
| H6 bounded execution/spend | gateway reservations, watchdog, no fallback | unknown cost becomes available balance | COST-01..03 |
| H7 owner-visible state | replayed read models and freshness envelope | absent data looks running/successful | OBS-01 |
| H8 language and terms | glossary digest/term-ID validation, English schemas/prompts | observation/prefix meaning silently changes | LANG-01 |
| Source fidelity | PDF digest/page/region and checked transcription | real hash but unrelated page accepted | SCI-03 |
| Independent evidence | separately implemented routes + certificate replay | shared formulation bug passes both | SCI-01..04 |
| FOUNDATION scientific authority | judge event mapping, Lean gate, human-only attestation | finite result promoted to general theorem | SCI-04, SEC-01 |

Acceptance scenarios, ownership and release order are specified in the packet document. All persistent/runtime behavior in this specification is prospective. This design session observed only source inspection, existing baseline checks and the bounded TLC model.
