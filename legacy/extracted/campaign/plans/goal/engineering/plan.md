# G1 narrow engineering plan (v1)

Root and branch verified before this write: <workspace>/aro-discovery-campaign, task/aro-discovery-k4t-campaign. Existing campaign and Astra files are immutable parents.

Implement only a goal-local adapter of the existing delivery validator, enforcing original per-check output SHA-256 in addition to all existing obligations. Reproduce the shared-output consistent-rehash bypass in a disposable local fixture; the old validator must accept it and the new validator must reject it. Retain old acceptance tests unchanged and execute normal and optimized runs.

Build a new versioned index from the historical partial index, original producer manifests, all phase records, repair records and source/scientific artifacts. Normalize missing fields without changing historical outcomes. Missing historical reviewer raw streams remain explicitly unavailable history. Capture new process replays under new G1 IDs, distinguish same-code replay from independent mathematical development and from G2 review. Preserve original comparator blockage; do not rerun comparator or toolchains.

Provide replay.py to execute actual regression tests, new scientific process controls, lint/format and integrity checks with local scratch, Python -B, timeouts and persisted stdout/stderr. It must not trust stored pass booleans. Bind immutable parent identities and the complete historical inventory. If historical obligations cannot honestly be fulfilled, persist the exact rejection and report partial rather than weakening the old contract. No Astra adaptation is needed merely to include its existing evidence.

Reserve verification/report time after at most 60 minutes implementation. G1 establishes engineering integrity only, never scientific novelty, general proof or human attestation. No tracker mutation, nested workers, commits, global installs, provider retry/fallback or live scientific writes.
