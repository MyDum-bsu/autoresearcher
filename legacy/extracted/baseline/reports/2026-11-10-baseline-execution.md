# M0 baseline execution

Status: M0 complete and checked locally; no scientific attestation or runtime release. Owner authorized baseline-first, the entire M0 chain, Pi OpenAI Sol workers through the current connection, isolated work inside the project, and coordinator management of local tasks. This report records execution decisions; it is not scientific attestation or a replacement for the scientific journal.

## Scope and authority

Bead: `aro-discovery-3sd`, claimed by `research-lead` on the owner's instruction and closed after final M0 acceptance; closure is an implementation-task result, not scientific attestation. Worktree: `<workspace>/aro-discovery-baseline`; branch `task/aro-discovery-3sd-baseline`; base `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`.

Implement P1, P2a and P2b from `<workspace>/aro-discovery-restart-plan/docs/specs/2026-11-10-research-pilot-packets.md`. No persistent runtime, Q-A4-R80 solution, live scientific journal/status/config/corpus changes, commits or pushes. Existing source inputs remain read-only. Baseline fixtures are the four owner-approved public cases. The research question's future epsilon and runtime profile are not activated.

## Execution choices

- Verified available Pi model: `openai/gpt-6.1-sol` via `pi --list-models sol`. P1 uses medium reasoning; independent mathematical checks/review use high. One active worker, no fan-out.
- Per-run timeout: 5,400,000 ms, zero retries. The installed standalone Pi agent interface supports timeout enforcement but exposes no native total-tool-call limit. The 60-call limit is an explicit worker stopping instruction and is audited from the run record; it is not represented as a hard SDK limit. Do not add an unverified option or change harness infrastructure merely to simulate enforcement.
- On timeout/tool-budget exhaustion: stop the chain, preserve work and investigate the cause before any new attempt. No automatic retry or escalation.
- Current Pi connection only. No new API keys, model gateway or spending integration. Dollar accounting remains unknown unless reliable usage is supplied; model-reported/catalog costs are not automatically a paid invoice.
- SHA-256 is internal provenance/change detection. Owner summaries use source names, pages and outcomes, not hash inventories.
- Independent checking means different mathematical routes and direct witness replay. Another model session alone is not a scientific verifier.

## Progress

- Prepared isolated worktree and owner-directed Bead. Source checkout remains untouched apart from the authorized local task tracking operation.
- P1 completed with strict finite schema, exhaustive policy search, deterministic witnesses, replay and CLI. Coordinator independently reran the 7 tests.
- P2a added a separate state-cell Bellman route and independent witness/result validation. The frozen regression generator contains 144 instances / 432 information-mode cases: 184 feasible and 248 infeasible, plus 12 public mode cases. No numerical disagreement with P1 was observed.
- P2b produced separate exact input manifests, a chronological control certificate generator and a verifier using backward adjoints plus forward simulation. Both pinned datasets have exact primal/dual gap zero.
- Read-only independent review found no mathematical blocker. It found that oversized JSON integers escaped the Bellman parser as an untyped ValueError; a test-first fix now handles that decoder boundary and excessive nesting with preserved causes. Original failing probes were observed before repair.
- Coordinator's targeted repository Ruff check initially FAILED with 69 findings. A dedicated lint-conformance pass fixed the seven new Python files without changing config/expectations; all 57 recorded output comparisons before/after were byte-identical. This gate was absent from the original worker completion checks: future packet acceptance must include the repository's targeted lint command before handoff.
- Saved six deterministic checked outputs and a provenance manifest in `artifacts/research-pilot-m0/`. Generated and checked both A4 certificates twice; compared output bytes. Independently checked every finite reference result before saving the second route's results.

## Validation and result

Coordinator observed:

```
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pilot/baseline -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s pilot/checkers -p 'test_*.py'
```

7 reference tests and 29 checker tests pass. Repeat both with `python3 -O` for validation independent of removable assertions. Before final lint formatting, coordinator measured 0.389 s / 9.920 s normal and 0.329 s / 11.576 s optimized. Final post-format coordinator runs also passed: normal 0.381 s / 9.538 s; optimized 0.400 s / 11.566 s. `ruff check --no-cache pilot` passed and `ruff format --no-cache --check pilot/baseline/*.py pilot/checkers/*.py` reported all seven Python files already formatted. The lint worker additionally observed `36 passed, 684 subtests passed` in pytest, both normal and optimized; the coordinator's acceptance is the unittest interface above.

| Instance | Open | State | Prefix |
|---|---:|---:|---:|
| strict_gain | 1 | 0 | 0 |
| correlated_hidden_disturbance | 1 | 1 | 0 |
| independent_hidden_disturbance | 1 | 1 | 1 |
| terminal_feasibility | infeasible | 0 | 0 |

A4 printed reward: **1.495710098124**. Reconstructed-decimal reward: **1.501101989382**. Both have exact gap zero, a robust lower terminal endpoint of exactly 2, and an upper endpoint no larger than 10. Values above are rounded displays; retained certificates/check records carry full rational values. Reconstructed decimals remain inferred inputs, not author-confirmed data or exact sin/cos.

## Pi execution and cost

All six runs completed without timeout, automatic retry or model fallback. They ran sequentially. The first three implement baseline packets; the fourth is independent review; the final two repair a review finding and satisfy existing repository lint. No worker was stopped by its time/tool budget. One run's total tool count is not available in its final snapshot, so full mechanical tool-budget compliance is not claimed.

| Run | Pi ID | Reasoning | Duration s | Tool count | Pi reported cost, USD |
|---|---|---|---:|---|---:|
| P1 | `585846f2-3660-4a66-bf7c-bf221501b102` | medium | 565.194 | not retained in final snapshot; worker did not report exact count | 0.4994512 |
| P2a | `f85920ab-5b6c-422a-b37a-f8b5b57d1e05` | high | 567.768 | 27, worker-reported including nested calls/handoff | 0.3925828 |
| P2b | `90ba96a8-0588-4198-8aed-79ea07c37aba` | high | 799.237 | 36, worker-reported | 0.4906528 |
| Review | `61404ff9-6bc5-452e-9ea3-cfbdeaf33968` | high | 496.622 | 33, reviewer-reported | 0.5166436 |
| Decoder repair | `bd74bdab-c530-4491-a87e-516396e557c2` | medium | 181.695 | 14, worker-reported | 0.1372876 |
| Lint conformance | `776d7717-0488-462b-b690-8ee0067a8686` | medium | 330.612 | 37, worker-reported | 0.3757384 |

Sum of these Pi accounting values: **USD 2.4123564**; summed agent duration approximately 49 minutes. This is harness-reported model accounting, not a verified invoice or total project/session spend. Coordinator/planning work is excluded. Actual bill/quota consumption under the current login remains unknown. No new API account/key or external metered runtime was introduced.

The installed API accepts `timeoutMs` and enforces a run timeout; it exposes no hard total-tool-call budget. Limits on calls were instructions, with worker-reported counts for five runs. The final `progress.toolCalls` snapshot does not retain completed calls in the observed API response. This observability limitation is recorded here rather than treating an empty list as zero calls. Before claiming a hard 60-call guarantee in an automated runtime, add/test a native per-call enforcement mechanism; that harness change is outside M0.

## Review and remaining scope

Read-only reviewer inspected all numerical modules/manifests and source anchors, ran the original test suites and 108 additional public software probe cases using pairwise nonanticipativity on complete-path actions. No false acceptance was observed in those checks. Those probes are not a private holdout and were not promoted to a scientific grid. The decoder fix is covered by new API/CLI regressions. Lint changes preserved recorded outputs and only tightened equal-length zip invariants.

P2a and P2b source/test size exceeded the plan's small-diff aspiration; final code is readable and split by module, but no claim of a sub-300-line PR is made. No commits were requested. An integration review can stage these as separate packets; do not compress code to satisfy a cosmetic line count.

Not run: evaluator-owned private holdouts; Lean; continuous state-measurement optimum at r=80; general novelty verification; persistent journal/runtime, sandbox, billing or recovery acceptance. Numeric checkers do not verify PDF page content automatically and have no authority to attest. Existing scientific status and live journal remain untouched.

First owner check: `pilot/README.md`, then its two unittest commands. Suggested next research step: owner review of M0 and a bounded, separately approved r=80 certificate attempt, or runtime construction if durable automated execution is now the priority. Neither is started by this delivery.
