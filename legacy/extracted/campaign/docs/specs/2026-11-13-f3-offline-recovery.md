# F3 offline recovery: remove accidental MCP and UI-tool-context dependencies

Task aro-discovery-k4t. Owner explicitly requested fixing resume failure. Original run `8d7a9e60-882c-4e89-8a58-429e7f62771f` was observed interrupted and then stopped through workflow_stop, not by editing state. Its 55 partial-review files are preserved and hashed in `artifacts/workflow-recovery/f3-mcp/interrupted-review-identities.json`. No original proof/model/goal or review outcome is overwritten.

## Confirmed diagnosis

Installed pi-extensible-workflows 6.3.0 stores every root-reachable tool in snapshot.tools and requires every one on cold resume. F3 froze 234 tools including unused MCP services. Current supported MCP discovery restored availability; one real search call returned without error, and all 234 frozen tools are now represented. The missing-tool condition was reproduced with installed reachableTools and an MCP-pending inventory, then passed with a ready inventory. Startup connection ordering is a plausible timing explanation, not an instrumented reconstruction of the exact past startup.

A second confirmed limitation prevents simply recommending UI Resume: `scriptToolContext` is absent for commands/session events/headless hosts, so a newly reached tools.write after UI resume would fail even when MCP tools are ready. The old script has such writes. Do not patch snapshots, globally expose tools, install stubs or execute a doomed resume solely to turn the run into failed.

## Supported, tested correction

Use the already installed official @piewf/cli 6.3.0 via its absolute node entrypoint (not in PATH). It is still Pi, not a platform migration. Two no-agent canaries completed. The second exercised real evidence() plus shell() and inspected its own persisted snapshot: eleven root tools, ZERO MCP tools. This corrects the local formal workflow's dependency graph rather than relying on a startup delay. Installed extension code and MCP configuration are unchanged; the general TUI startup issue remains an upstream concern, but the new formal run has no MCP dependency.

New versioned continuation source keeps exact F3 mathematical targets, models, seals, provider/models, statement-before-proof gate and proof/axiom/control acceptance. It uses only supported durable evidence/shell host operations, no session tools.* calls. Child tool selectors are an explicit read/bash/edit/write allowlist; workflow_result remains the runtime result tool. The actual persisted new root snapshot must be checked for zero MCP BEFORE any mathematical agent.

## Bounded continuation and paths

The original statement reviewer was interrupted before delivering a report/readyForProof result. A new bounded reviewer may finish from saved primary extracts and observations, but cannot count the old partial review as accepted. New review/proof/final evidence is ONLY `artifacts/bridge/formal-v3-offline/`; old `artifacts/bridge/formal-v3/` remains readonly. The original `artifacts/bridge/formal-v3/candidate-seal.json` and `bridge/formal-v3/expected-theorems.json` stay authoritative for unchanged targets. New proof source may still use the prescribed `BridgeFormalV3/Proofs/` directory, which had no completed proof when the interruption occurred.

At most three sequential agents: completion review (high), conditional prover (medium), independent replay (high), same 90min/60 instructional envelope as F3. The interrupted reviewer counts as spent effort; no claim of a free retry. No provider retry/fallback, scientific scope change, target amendment, installations/downloads, comparator or private benchmark. Original F1/F2 evidence and missing F4/source-policy obligations unchanged.

The CLI host runs in its own managed session with task-local temp/cache and PI_OFFLINE=1 for startup network operations (not a promise that inference is offline). A supervising wrapper records PID, CLI run ID, raw streams and terminal exit/result. It enforces the existing 600 MiB disk reserve and a bounded host lifetime. A passive no-agent monitor may deliver completion to the current Pi session; interruption of that monitor must not kill the independent proof host. Do not promise uptime or treat monitor completion as mathematical acceptance.

Before launch verify the feature worktree branch. Beads and operational state record the supersession, actual IDs and zero-MCP validation. Old run remains stopped with original journal/snapshot; new run is an explicit continuation, not a resumed original or a claimed replay of an accepted reviewer.
