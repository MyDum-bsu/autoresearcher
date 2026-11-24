# Security & Integrity Policy

## Scope

`aro-discovery` is a formal mathematics and verification repository. Security and scientific integrity concerns include:

1. **Verification soundness bypasses** — any flaw that allows `sorry`, custom axioms, weakened `frozen_core` goals, or vacuous Python `assert`-only checks (`python3 -O`) to pass `make verify-all` or `make verify-lean-compile`.
2. **Accidental leakage of sensitive data** — credentials, API keys, private keys, personal identifiers, or host-specific paths committed to tracked files.
3. **Supply-chain or CI workflow issues** — unsafe script execution in `verification/` or `.github/workflows/ci.yml`.

## Automated Safeguards

- `make verify-public-hygiene` deterministically scans all git-tracked files for host paths, secrets, private keys, internal orchestration IDs, and forbidden artifacts (with negative self-tests in both `-B` and `-B -O` modes).
- `make verify-discovery` enforces SHA-256 immutability of the frozen Lean 4 core (`verification/lean/manifests/frozen-core-sha256.json`).
- `make verify-corpus` and `make verify-migration` verify SHA-256 integrity of primary literature and migrated reference assets.

## Reporting a Vulnerability or Integrity Issue

If you discover a security vulnerability, leaked secret, or verification soundness bypass:

1. **Do not** disclose sensitive credentials in a public issue.
2. Open a GitHub Security Advisory (private vulnerability report) on the repository, or contact the maintainers through the repository's security tab with:
   - affected file(s) and commit SHA;
   - minimal reproduction steps (`python3 -B` / `python3 -B -O` / `lake build`);
   - expected vs. observed verifier verdict.

We aim to acknowledge reports promptly and publish a verified fix with a regression negative control.
