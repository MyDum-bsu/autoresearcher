# F3 proxy recovery: initialize the intended Node transport before SDK load

Task aro-discovery-k4t. Owner explicitly confirmed all requests must use the existing proxy and requested continued work. Previous CLI403 must not be treated as an established account/region blocker until actual routing is checked.

## Confirmed transport fault

Node22.23.2 supports --use-env-proxy. Ordinary Pi CLI startup calls configureHttpDispatcher; @piewf/cli's direct SDK initialization does not. The latter resolves an installed SDK package reporting1.0.0 and OpenAI7.19.0, while the interactive Pi release is1.5.2. No SDK/package upgrade is part of this repair.

Actual OpenAI SDK loopback regression passed:
- Same HTTP_PROXY/HTTPS_PROXY values without native flag: one direct local-origin request, zero proxy connections.
- With --use-env-proxy: one origin request through one proxy connection.
- Rejecting local proxy with native flag: request fails, origin not reached; no direct fallback.
No external request or real API key was used in the regression.

One unauthenticated connectivity probe with the existing configured proxy returned HTTP401, not the earlier403. A net.client.socket observation confirmed its only physical connection went to the configured proxy. No API key or inference request was used. This validates proxy routing/connectivity, not model authorization by itself.

## Corrected launch

Use the same official CLI, provider/models and sealed mathematics. New task-local supervisor enables --use-env-proxy and inherits it through NODE_OPTIONS for Node children. A task-local preload verifies the flag and that the required provider destinations resolve to the EXISTING proxy, and records redacted physical-connection counts. No proxy URL, endpoint, credentials, global config, system setting or certificate policy changes. Do not print raw proxy credentials or auth headers. Observe any unexpected nonlocal peer separately; transport observation is not an OS firewall guarantee.

New workflow source is a path-scoped copy of the already tested offline continuation: no MCP root dependency, no tools.* calls, explicit read/bash/edit/write child tools and durable evidence/shell storage. New evidence only artifacts/bridge/formal-v3-proxied/ and the corresponding proxied briefing; the candidate seal remains artifacts/bridge/formal-v3/candidate-seal.json. Old interrupted and failed jobs, partial review and artifacts remain immutable. Proof source still uses prescribed BridgeFormalV3/Proofs/. This note overrides evidence paths in earlier recovery specifications; mathematical targets/gates do not change.

One recorded corrected launch is authorized following the demonstrated configuration repair, not a retry loop for an unchanged403. At most three sequential original F3 stages, same model/time/call envelopes. Native proxy configuration is now explicit; if a provider rejection persists under confirmed routing, preserve it and stop rather than change regions/endpoints/providers. F1/F2 remain checked; F3/F4 and whole-bridge acceptance remain pending. No fresh goal scheduler, scientific promotion or attestation.

## Verification and record

Regression: `python3 -B artifacts/workflow-recovery/f3-proxy/test_sdk_proxy.py`.
Configured route probe: `node --use-env-proxy artifacts/workflow-recovery/f3-proxy/probe-configured-proxy.mjs` (one observed request only; do not rerun as an automatic probe loop).
Task launcher: scripts/run-f3-proxied-host.py; native preloader scripts/require-proxied-node.mjs. Evidence artifacts/workflow-recovery/f3-proxy/, including per-process transport counts and supervisor completion. The old conclusion that matching proxy env hashes implied no routing issue was insufficient and is superseded by this actual transport evidence.

No independent worker/API call is required to diagnose local proxy routing. The local candidate-proof plan was prepared but no proof source was written before the owner's proxy correction; do not run a concurrent local prover while the repaired supervised F3 workflow is active. Preserve 600 MiB disk reserve and bounded process lifetime. No global installs/updates, source theorem changes, hidden provider retries/fallback, commits/pushes or live scientific writes.
