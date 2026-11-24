# Environment v2: imports provisioned; amended model and goals elaborate

The missing-import environment blocker is resolved in a NEW task-local project. `typed-model-elaboration.json` and `typed-goals-elaboration.json` record actual exit 0. No theorem has been proved. Original formal-v1 sources, unelaborated seal, failed runs and reviews remain unchanged.

## Dependency acquisition and resource limits

All nine package source revisions match the existing pinned manifest. The mathlib acquisition helper in this environment is explicitly modified: curlRetryArgs returns `--retry 0` and never `--retry-all-errors`. The original helper copy, exact diff and original/new hashes are saved. No mathematical Mathlib source, cache hash inputs, compiler, cache origin or integrity mechanism was changed. This is not a pristine upstream helper and is not reported as one. No network request/provider retry was requested.

The small cache helper was built successfully. Its build made a task-local Batteries release build available, including an unused 247 MB linter executable; that disposable new executable was removed with its identity recorded. Only the two actual import roots were requested. The official cache returned 1811 archives successfully from the master origin, without extraction at download time.

A small engineering adapter used upstream hash and extraction-plan APIs. Its first version omitted the placeholder command expected by `parseArgs`, thereby ignoring the first requested root. That error produced an incomplete 1280-archive extraction and a preserved missing-import compiler failure. `UnpackPlanV2.lean` supplies the command argument and extracted 457 additional archives already downloaded; no network retry was needed. Some dependency artifacts were already decompressed by the local helper build. Both adapter versions and their outputs remain saved.

Extraction ran in batches of 32 using the bundled leantar. Source, `.olean` families, Lean IR and integrity traces were kept. New disposable generated C/object artifacts and successfully extracted download archives were removed with hashes/byte counts recorded. A child-process watchdog retained a 600 MiB free-space reserve. At completion around 0.8 GB remained available; do not download full Mathlib or import all Mathlib in the next stage. Other projects, old scientific evidence and system/user caches were not cleaned.

## Actual compiler findings and versioned amendment

Once imports were available, Lean found actual source errors in the original candidate: grouped structure fields were parsed as field parameters, `at` and `prefix` were reserved identifiers, Data-dependent methods were not in their expected namespace, recursive `run` needed an explicit Data parameter, and control/noise subtype abbreviations needed reducibility for measurable-space instance synthesis.

The amended candidate is in `bridge/formal-env-v2/lean/BridgeFormalV2/{Model,Goals}.lean`, a new namespace and identity. Its fixes split fields, rename `at` to `blockAt` and `prefix` to `prefixState`, place model methods under Data, make recursive Data explicit and use type abbreviations for the same subtypes. No information/control/cost hypothesis was relaxed. The source-to-source delta still needs independent semantic inspection before proof. Intermediate failed compiler outputs remain saved; not every intermediate edit had a frozen source snapshot, so they are not advertised as sealed proof versions.

Observed successful commands, from the new project with task-local environment, executed via the recorded provisioner:

- `lake env lean -o .lake/build/lib/lean/BridgeFormalV2/Model.olean BridgeFormalV2/Model.lean`: exit 0.
- `lake env lean -o .lake/build/lib/lean/BridgeFormalV2/Goals.olean BridgeFormalV2/Goals.lean`: exit 0.

These establish elaboration of definitions and ten goal propositions, NOT proof of those propositions, nonvacuity, source fidelity or F1/F2. F3/F4 remain absent. Next gate: independently inspect/seal the amended model and exact targets, then conditional proof development. No further review should rerun the old missing-import environment.
