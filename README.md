# `autoresearcher` — Automated Research Discovery for Adaptive Robust Optimization

**Formal Lean 4 Proofs · Exact Rational Falsifiers · Mathematical Atlas · LearnHarness Study Packs**

[![Repository](https://img.shields.io/badge/GitHub-MyDum--bsu%2Fautoresearcher-blue)](https://github.com/MyDum-bsu/autoresearcher)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

`autoresearcher` (internal Python/Lean workspace `aro-discovery`) is an end-to-end, verifier-gated mathematical research repository investigating the formal bridge between **Optimal Guaranteed Control (OGU / Dmitruk school)** and **Two-Stage Adaptive Robust Optimization (ARO)** with fixed recourse, the **value of information under closure scheduling**, and **exactness boundaries of Affine Decision Rules (ADR/LDR)**.

Every scientific claim in this repository is governed by a strict **Falsify-First** and **Dual-Lock** discipline: conjectures must survive exact rational LP / Bellman / SymPy falsifiers before proof synthesis, Lean 4 proofs are compiled against an immutable `frozen_core` with zero `sorry` and standard axioms only, and human-readable Russian study packs are generated for **LearnHarness v0.7.0** (with human-only attestation).

> **Project Governance & Roadmaps (RU):** [CHARTER.md](CHARTER.md) · [research/problem-map.md](research/problem-map.md) · [research/atlas/ATLAS.md](research/atlas/ATLAS.md)

---

## Verified Results at a Glance

| Pillar | Metric / Artifact | Verification Status |
|---|---|---|
| **Lean 4 Formal Kernel** (`v4.35.0-rc2`) | **55 proved declarations** in [`AroProofs/Inventory.lean`](verification/lean/AroProofs/Inventory.lean) (**36 new** from Run-01 across F4, G2, O4, G1, O1 + 10 `BridgeFormalV2` F1/F2 + 5 `Aroform` P1–P3 + 4 `BridgeFormalV3` F3) | **0 `sorry`**, axioms strictly `⊆ {propext, Classical.choice, Quot.sound}`; `frozen_core` SHA-256 locked |
| **Exact Counterexamples** | **`O8-sion-gap`** (minimax quantifier gap + continuous-box SymPy certificate), **`D1`**, **`D2`**, **`E-rank1`**, **`A-S1`** (38 exact checks) | Deterministic exact-rational & SymPy verifiers (`-B` and `-B -O`) |
| **ADR Falsification Battery** | **`T1–T7`** executable falsification suite (`verification/falsifiers/`) | 7/7 battery checks + unit tests passing in `-B` and `-B -O` |
| **Exact Rational Oracles** | **M0** finite reference & Bellman (36 tests) + **A4** closure certificates (`r=67`, `r=104`, 32 transfer controls) | Byte-identical in `-B` and `-B -O` |
| **Mathematical Atlas & Blueprint** | **37 nodes, 60 edges** (`research/atlas/atlas.json`): `16 lean_proved`, `8 oracle_verified`, `8 falsified`, `5 open` | DAG integrity, live Lean signature audit, 9 negative controls |
| **Russian Study Guides (`LearnHarness v0.7.0`)** | **7 structured 4-file study packs** in [`research/guides/`](research/guides/) (including 5 new Run-01 packs marked `unattested_draft`) + live HTTP API bridge (`learn/`) | Gate G5 (100% anchor-lint, LaTeX, Mermaid, RU style) + isolated E2E tests |

---

## Lean 4 Proof Inventory (55 Declarations, 0 `sorry`)

All 55 declarations are audited in [`verification/lean/AroProofs/Inventory.lean`](verification/lean/AroProofs/Inventory.lean) against the positive axiom allowlist `{propext, Classical.choice, Quot.sound}`:

| Module / Track | Declarations | Mathematical Scope |
|---|---:|---|
| `BridgeFormalV2` (F1/F2) | 10 | Linear discrete dynamics expansion, prefix split, exogenous image `Ξ = L(W^r)`, Borel policy translation OGU ↔ 2-stage ARO, epigraph-level equality |
| `AroProofs.Aroform` (P1–P3) | 5 | L1 rotation identity, monotonicity of infimum under policy inclusion, 1D ADR exactness, 2-path L2a identities |
| `BridgeFormalV3` (F3) | 4 | Future-disturbance expansion, attained support, robust row tightening, exact support equivalence |
| `BridgeF4CornerLP` + `BridgeF4ExtremeLP` (**F4**, Run-01) | 9 | Borel right-inverse selector over zonotope `Ξ`, finite vertex-LP & extreme-vertex-LP equivalence with ARO and source epigraphs |
| `BridgeG2ConicSupport` (**G2**, Run-01) | 7 | General compact convex / conic support tightening, box/L1 cross-polytope/L2 SOC ball support, non-polyhedrality of 2D L2 ball |
| `BridgeO4ClosureValue` (**O4**, Run-01) | 7 | Single-closure value of measurement: open-loop inclusion, zero-gain criteria, shared corner-LP characterization, strict gain iff corner separation |
| `BridgeG1Multistage` (**G1**, Run-01) | 6 | Multi-closure `k ≥ 2` stage split, forward/reverse policies, history-policy epigraph equality, strict separation of Markov vs. history policies at `k = 2` |
| `BridgeO1ADRExactness` (**O1**, Run-01) | 7 | Static ⊆ ADR ⊆ ARO inclusion, simplex ADR exactness, barycentric syzygy coupling, Chen–Zhang T3 gap, 1D exactness vs. 2D strict ADR gap |

---

## Honest Open Frontiers

We explicitly distinguish proved results from open mathematical frontiers (tracked in [`research/atlas/atlas.json`](research/atlas/atlas.json)):

- **O8 (`conj-o8-quantifier-gap`, `open` + `ce-o8-sion-gap` `falsified`):** Exact counterexample establishes a strict minimax quantifier gap (`V_maxmin < V_minmax`) under non-convex/coupled constraints (including a continuous-box SymPy certificate). General sufficient regularity conditions closing the gap remain open.
- **G2 (`gen-nonbox-conic-uncertainty`, `open`, partial coverage):** General compact convex support tightening and L1/L2 conic specializations are formalized in Lean 4; full finite-dimensional conic duality / spectrahedral lifting for arbitrary non-box uncertainty sets remains open.
- **O4 (`conj-o4-closure-scheduling`, `open`, partial coverage):** Single-closure value-of-measurement foundation and strict-gain corner separation are formalized; optimal scheduling of closure time(s) `R` under general dynamics remains open.
- **G1 (`gen-multistage-k-closures`, `open`, partial coverage):** Multi-stage `k ≥ 2` history-policy bridge and strict Markov-vs-history separation are proved; general finite-recourse reduction and optimal multi-closure scheduling remain open.
- **O1 (`conj-o1-adr-exactness-char`, `open`, partial coverage):** Simplex exactness, syzygy coupling, 1D exactness, and 2D strict gap are proved in Lean 4; a complete necessary-and-sufficient geometric characterization of ADR exactness in dimension `≥ 2` remains open.

---

## Russian Study Guides & LearnHarness v0.7.0 Integration

Following the **No Black-Box Theorems** principle ([`CHARTER.md`](CHARTER.md)), every formalized track has a human-readable Russian study pack in [`research/guides/`](research/guides/) formatted to a strict 4-file standard (`01-intuition-and-map.md`, `02-propositions-and-chains.md`, `03-traps-and-counterexamples.md`, `04-practice-and-attestation.md`) and validated by Gate G5 (`make verify-guides`):

- [`01-bridge-packet-01/`](research/guides/01-bridge-packet-01/) — OGU ↔ 2-Stage ARO Bridge Foundation (F1/F2 + D1/D2)
- [`02-math-atlas/`](research/guides/02-math-atlas/) — Fundamental Mathematical Atlas & Lean 4 Blueprint
- [`03-f4-vertex-lp-selector/`](research/guides/03-f4-vertex-lp-selector/) — F4: Finite Vertex-LP & Borel Selector *(Run-01, `unattested_draft`)*
- [`04-g2-conic-support/`](research/guides/04-g2-conic-support/) — G2: Conic & Compact Convex Support Tightening *(Run-01, `unattested_draft`)*
- [`05-o4-closure-value/`](research/guides/05-o4-closure-value/) — O4: Single-Closure Value of Measurement *(Run-01, `unattested_draft`)*
- [`06-g1-multistage-bridge/`](research/guides/06-g1-multistage-bridge/) — G1: Multi-Stage `k ≥ 2` Bridge & Markov vs. History *(Run-01, `unattested_draft`)*
- [`07-o1-adr-exactness/`](research/guides/07-o1-adr-exactness/) — O1: ADR Exactness, Simplex/Syzygy & 1D-vs-2D Dichotomy *(Run-01, `unattested_draft`)*

> **Attestation Policy:** All 5 Run-01 study packs are intentionally marked `unattested_draft`. Promoting any result to `attested` is strictly a human-only action after manual mathematical review.

The [`learn/`](learn/) package provides the `aro` CLI and HTTP API bridge for exporting study packs to **LearnHarness v0.7.0** (`POST /api/graph/import`, `POST /api/chats`).

---

## Repository Layout

| Directory | Purpose |
|---|---|
| `verification/` | Trusted verification core: `lean/` (Lean 4 `v4.35.0-rc2`: `AroCore`, `AroProofs`, `BridgeFormalV2`, `BridgeFormalV3`, `Controls`, `V1Aroform`), `falsifiers/` (`T1–T7` battery + SymPy), `oracles/` (M0 + A4 `r=67,104`), `gates/` (G1–G5, Lean static/compile gates, public hygiene gate) |
| `research/` | Git-native scientific memory: `atlas/` (37 nodes / 60 edges + Blueprint), `claims/`, `counterexamples/` (`D1`, `D2`, `E-rank1`, `A-S1`, `O8-sion-gap`), `discovery/` (managed discovery loop + `frozen_core` guard), `literature/` (radar & knowledge graph), `guides/` (Russian LearnHarness study packs) |
| `corpus/` | Immutable primary literature library (24 ARO papers + A1–A5 Dmitruk school + 5 TeX sources + `MANIFEST.md` SHA-256 + `intake/` + `extra/`) |
| `learn/` | Python package & isolated E2E tests for LearnHarness v0.7.0 HTTP API integration |
| `thesis/` | Russian master's thesis outline & artifacts (`100%` anchor-lint) |
| `pipeline/` | Darkfactory stage profiles and independent review rubrics |
| `legacy/` | Read-only structured v1 reference archive (`extracted/`, `migration-manifest-r1b.json`) |

---

## Quick Start & Reproducible Verification

### Prerequisites

- **Python ≥ 3.12** with `pyyaml` and `sympy`:
  ```bash
  python3 -m pip install pyyaml sympy
  ```
- **Lean 4 (`v4.35.0-rc2`)** via [`elan`](https://github.com/leanprover/elan) *(required for `make verify-atlas`, `make verify-lean-compile`, and `make verify-claim`)*:
  ```bash
  cd verification/lean
  lake exe cache get
  LEAN_NUM_THREADS=1 lake build AroCore AroProofs BridgeFormalV2
  ```
  *(Setting `LEAN_NUM_THREADS=1` keeps peak RAM well within 8–13 GiB.)*
- **Optional RU Technical-Style Linter** *(for full `make verify-guides` style checks)*: set `ARO_STYLE_LINTER=/path/to/lint_technical_style.py`, or run portable schema/anchor/LaTeX/Mermaid verification via `python3 -B verification/gates/verify_guides.py --no-style`.

### Verification Commands

All standalone Python gates (`verify-public-hygiene`, `verify-migration`, `verify-corpus`, `verify-m0`, `verify-transfer`, `verify-falsifiers`, `verify-lean`, `verify-atlas`, `verify-literature`, `verify-discovery`, `verify-guides`, `verify-learn`) execute in both standard (`python3 -B`) and optimized (`python3 -B -O`) modes so no gate relies on stripped `assert` statements; `verify-counterexamples` runs `O8-sion-gap` in both `-B` and `-O` (and legacy counterexamples in `-B`), `verify-claim` runs G2+G3 in `-B` and G2 + self-tests in `-O`, and `verify-lean-compile` invokes the Lean 4 compiler in `-B`:

```bash
make verify-public-hygiene  # Security & hygiene audit across all tracked files (+ self-test)
make verify-migration       # SHA-256 verification of all 423 migrated v1 reference assets (-B and -O)
make verify-corpus          # SHA-256 verification of all 42 corpus/MANIFEST.md primary sources (-B and -O)
make verify-m0              # 36 exact rational M0 finite-reference & Bellman tests (-B and -O)
make verify-transfer        # 32 OGU -> ARO transfer controls (A4 r=67, r=104), -B/-O byte-identical
make verify-counterexamples # Exact counterexamples D1, D2, E-rank1, A-S1 (38 checks), O8-sion-gap
make verify-falsifiers      # Executable T1-T7 ADR falsification battery + exact_lp/SymPy unit tests
make verify-lean            # Static Lean 4 audit (0 sorry/admit/custom axioms + negative self-tests)
make verify-literature      # Literature catalog, pdf_sha256 & physical_pages, Atlas links + unit tests
make verify-discovery       # Discovery loop routing, frozen_core SHA-256 check, offline dry-runs
make verify-learn           # Unit & isolated E2E tests for LearnHarness v0.7.0 HTTP API bridge

# Guide Gate G5 (portable CI mode without external RU style linter, or full mode via `make verify-guides`):
python3 -B verification/gates/verify_guides.py --no-style

# Lean 4 live kernel compilation, Atlas live audit, and Gate G2/G3 (requires hydrated Mathlib cache):
LEAN_NUM_THREADS=1 make verify-lean-compile
LEAN_NUM_THREADS=1 make verify-atlas
LEAN_NUM_THREADS=1 make verify-claim

# Run every deterministic verification target end-to-end (when Lean 4 & ARO_STYLE_LINTER are available):
LEAN_NUM_THREADS=1 make verify-all
```

---

## License & Citation

- Original code, Lean 4 formalizations, verification gates, falsifiers, mathematical atlas, and documentation authored in this repository are released under the [MIT License](LICENSE).
- **Third-Party Corpus Notice:** Academic PDFs and LaTeX source files under `corpus/` are third-party primary literature retained for SHA-256 reproducibility (`corpus/MANIFEST.md`); they remain under their respective authors' and publishers' copyrights/licenses and are **not** relicensed under MIT.
- Machine-readable citation metadata is provided in [CITATION.cff](CITATION.cff).
- See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md) for verification invariants and reporting guidelines.
