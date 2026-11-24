# Contributing to `aro-discovery`

Thank you for your interest in contributing to `aro-discovery`. Because this repository serves as a formally verified scientific workspace, all contributions must preserve its mathematical and verification invariants.

## Core Invariants

1. **Frozen Lean Core (`frozen_core`) is immutable.**
   Do not weaken, edit, or bypass definitions or theorem targets in:
   - `verification/lean/AroCore/Model.lean`
   - `verification/lean/AroCore/Goals.lean`
   - `verification/lean/BridgeFormalV2/Model.lean`
   - `verification/lean/BridgeFormalV2/Goals.lean`
   - `verification/lean/manifests/frozen-core-sha256.json`

   Integrity is enforced programmatically by `check_frozen_core_sha256` inside `make verify-discovery`.

2. **Falsify-First.**
   Every new conjecture must survive exact rational LP / Bellman / SymPy falsification (including the `T1–T7` battery where applicable) before proof synthesis or Lean 4 formalization. Refuted conjectures are preserved as first-class counterexamples under `research/counterexamples/` and are never overwritten.

3. **Zero `sorry` and Standard Axioms Only.**
   All Lean 4 proofs must compile with zero `sorry`/`admit` and depend strictly on the standard Lean 4 axiom allowlist `{propext, Classical.choice, Quot.sound}`.

4. **No Black-Box Theorems & Human-Only Attestation.**
   Closed scientific results must be accompanied by an intelligible Russian study pack in `research/guides/` (validated by Gate G5 `make verify-guides`). Never set a guide's attestation status to `attested` programmatically — human attestation is reserved strictly for the project owner after manual review.

5. **Public Hygiene.**
   Never commit host-specific absolute paths, credentials, private keys, or personal emails outside SHA-256-locked primary literature sources.

## Verification Checklist Before Opening a Pull Request

Run all deterministic verification gates locally:

```bash
make verify-all
```

If you modified Lean 4 files, also run the Lean 4 compiler check with single-threaded memory discipline:

```bash
LEAN_NUM_THREADS=1 make verify-lean-compile
```

Ensure every gate passes in both standard (`python3 -B`) and optimized (`python3 -B -O`) modes, and that `make verify-public-hygiene` reports zero violations.
