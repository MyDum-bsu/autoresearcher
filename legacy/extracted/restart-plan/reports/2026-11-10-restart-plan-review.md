# Restart implementation plan: review and evidence record

Date: 2026-11-10. This is a planning-session record, not a code-judge verdict or owner approval.

## Delivery and repository state

Delivered a revised English implementation specification and dependency-ordered packets with a complete P1 worker prompt:

- `docs/specs/2026-11-10-research-pilot-implementation.md`
- `docs/specs/2026-11-10-research-pilot-packets.md`

Location: `<workspace>/aro-discovery-restart-plan`, feature branch `plan/research-pilot-restart`, base `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`. No code implementation, commit, push, remote synchronization, live journal append, scientific status transition, Bead creation/update, configuration change or corpus admission was performed. One read-only independent reviewer was used; no implementation worker or automatic paid research route was launched. Session/reviewer provider cost was not measured and is unknown, not zero.

The input checkout `<workspace>/aro-discovery` was on `research/autonomous` at the same HEAD. Its existing modified files were `docs/GLOSSARY.md`, `events.jsonl`, `state/science.db`; it also contained untracked pilot inputs and essay/report files. Those remain outside this change. No upstream was configured; unpushed commits cannot be determined. Open PRs were not checked because no GitHub remote was established. The repository-state skill script and `bd prime`/`bd list --status=open` were read-only context operations. No new task was manufactured for this planning session.

## Fresh checks observed

Commands executed in the source checkout:

```
python3 specs/research-pilot/check_observation_fixtures.py
python3 specs/research-pilot/check_dmitruk_open_loop.py
```

Both exited 0. Observed output:

```
strict_gain: open=1, state=0, prefix=0, state_bellman=0
correlated_hidden_disturbance: open=1, state=1, prefix=0, state_bellman=1
independent_hidden_disturbance: open=1, state=1, prefix=1, state_bellman=1
terminal_feasibility: open=inf, state=0, prefix=0, state_bellman=0
Printed coefficient value: 1.495710098124
Reconstructed coefficient value: 1.501101989382
```

These are fresh executions of historical/design-input scripts. Their agreement is useful baseline evidence, not independent reimplementation and not verification of a continuous one-measurement optimum. The first script uses a Python infinity sentinel internally; the proposed portable schema deliberately uses typed infeasibility instead.

TLC ran on copies in a private temporary directory, with:

```
java -cp "$HOME/.local/share/tlaplus/tla2tools.jar" tlc2.TLC -workers 1 PilotPublication
```

Base configuration exited 0: 163 states generated, 94 distinct states, depth 9, no configured invariant violation. In separate copied configs:

- `AllowStaleSubmission = TRUE`: exit 12, `Invariant SingleCurrentWriter is violated`.
- `AllowGateBypass = TRUE`: exit 12, `Invariant AuthorizedCommit is violated`.

Only the named flag changed per negative run. No model file in the source checkout changed. The plan explains the abstraction limits, especially the absence of durable precommit operational state from the model's log. Implementation conformance, all private holdouts, sandboxing, actual journal crash durability, provider tariffs and paid economics are **not run**, because there is no new runtime yet. No Lean build was run and no formalized claim is made. Broad legacy `make check` was deliberately not run for a documentation-only design; it is neither targeted acceptance nor safe evidence for the new boundary.

The technical-style diagnostic ran on both English documents. Its initial implementation-spec findings were reviewed; four wording changes were made. The word `unique` in the terminal-bundle contract is a uniqueness constraint, not a promotional claim. Packet text had no findings.

Independent read-only reviewer run `38e68fe5-c0e2-44ce-9b54-b7cb447cf0d5` found one planning inconsistency: P9's dependency graph required P6 while the release text allowed offline work after R0. Fixed the graph to `P0 + P2 -> P9`; publication still requires R1 and gates. Reviewer reported no other confirmed blocking issue. This is design review, not scientific certification or release acceptance.

## Primary-source checks

PDF page numbers below are one-based, independent of printed journal page numbering. Used `pdftotext -layout` on the PDFs themselves for definitions and rendered pages with `pdftoppm` for formula/layout checks. This was targeted reading, not a complete literature review.

| File / source | SHA-256 | Read/checked relevance |
|---|---|---|
| `corpus/our_papers/A2_Дмитрук_2018.pdf` | `fca596196bdfe1f8740a767427fe1fd761a8c0712f6b3b314bf0832fe9d29dc9` | Rendered PDF p.16: Example 2 compares closing instants and reports 6.8; Example 3 demonstrates no gain |
| `corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf` | `2330f4ac22dd57b924b17f130a7937769ea6f6f56f825f1779102a038a347288` | Rendered p.7, read pp.8–9: rank-specific LP, approximation, discretization h=0.1, fixed instant 80 |
| `corpus/our_papers/A4_Дмитрук_2022.pdf` | `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420` | Read pp.3–6, rendered p.12: terminal constraints and scheduled state measurements; literal A/B/E coefficients and open-loop printed reward |
| Dmitruk 2023, Math-Net `into1170` | `e79d399aca932f40efa1dd9bf330385498bdf66f05b78d16a74c16381ac43435` | Read pp.4–5, rendered p.5: block Bellman and distinction from repeated feedback replanning |

The 2023 file was found in the existing review cache `/tmp/aro-pilot.nq2nR4/dmitruk2023.pdf`; it matched the earlier review fingerprint. Stable retrieval reference: `https://m.mathnet.ru/php/getFT.phtml?jrnid=into&option_lang=rus&paperid=1170&what=fullt`. This temporary cache is not durable corpus admission. P0 must bind an available source copy before any dependent scientific use. No new download or corpus manifest mutation was performed.

Important missing checks:

- Full-text 2025 successor comparison; full theorem/assumption review of adjacent information-discovery and exact ARO sources. Required before novelty claims, not before the local baseline/reference protocol.
- Source-page transcription region records and independently reconstructed portable A4 certificates. Fresh existing-script runs do not replace P2.
- Certified continuous-state policy and bounds at r=80; no new numerical value for that question was obtained.
- `aro.journal` isolated-root/durability capability test; P4 stops if unavailable instead of bypassing authority.
- Owner approval of episode tolerance, frozen fixture inventory, journal/gate scope, implementation task/base and any paid binding. Draft profile remains draft.

## Working-copy input fingerprints

Paths in this table are relative to the source checkout, not assumed present in the new feature worktree. They pin what the design actually reviewed. Before implementation, verify them or record an explicitly reviewed new input version.

| Path | SHA-256 |
|---|---|
| `FOUNDATION.md` | `41cccffdf929c34e9a3b0d8866fc842ad026f5b046b09b34e62a58b897e3fe12` |
| `docs/GLOSSARY.md` | `bff1e3e1b2588a202ecfb9228fa213601c2f38c95eaf8aa4c6f8bfa9116fad8c` |
| `reports/briefings/2026-11-10-astra-restart.md` | `f2d5bbd42d61b6a106cf78b2968db15e61f724818434433053a98a9c13a703eb` |
| `docs/specs/2026-11-10-research-harness-pilot.md` | `f752eda4b426c6bac947768da32316fd545152fa2618990cd79b43c1ab40e714` |
| `reports/2026-11-10-restart-audit.md` | `4f8e664c80cab0eabe072e86b166b23a750ce965f55c8e28c326ef8ac0296870` |
| `reports/reading/2026-11-10-research-harness-and-optimization.md` | `667cbe43c662a72e88f2608f56c6a6c2e9eee1d7fcfeb367842e0d8efecb0036` |
| `specs/research-pilot/PilotPublication.cfg` | `ce6420d3b7991d59bc9bcae9ad177c54abf9de76676a1c438968c2ea00f63c34` |
| `specs/research-pilot/PilotPublication.tla` | `a8a792449acf2f6908c9c1043722412471253ad99ce63b1f2f7a3b23037fc9bc` |
| `specs/research-pilot/check_dmitruk_open_loop.py` | `20a09d95ed54ddcea8f6963993c790bc08988a989c1eb952dfbcf0f788592be4` |
| `specs/research-pilot/check_observation_fixtures.py` | `237ba5947d61fbbc7f85a31d25e6d7d3b1b628624bd7f8b78c088d7c4ba12558` |
| `specs/research-pilot/pilot.example.yaml` | `f8b7634225c89e64c0e99e2fe5d0843a079f92942f98af23c7bb67b27d44d6c3` |
| `artifacts/research-pilot/2026-11-10-pilot-checks.txt` | `aa6be8719fcd2ba8bf850c1858adca2a0fb6833810a0ba0709b7bb395b6a5189` |
| `../stigmergy/docs/spec.md` | `d3e5c59dc60c96ca501942b3756d2f9d477f6ddd406aabb522b974d6565c9c1f` |

## Handoff

Recommended first move: owner binds P0 inputs and a Bead, then assigns P1's complete prompt to one lower-cost worker in a feature worktree. P1 is a pure finite reference with no new dependencies, paid automation or journal writes. Its outcome is independently checkable without approving the persistent runtime. Do not start a whole-system implementation from this report.

The material choices are M0-first versus an immediate general theorem, the implementation/input base and isolated journal/gate authority, and later spending activation. English term IDs are used internally; Russian equivalents for lease/publication/scope/evidence bundle/research disposition remain editorial proposals and do not block the local reference.
