# Contribution dossier: correlated continuation compatibility

Task `aro-discovery-k4t`, finite campaign of 2026-11-13. Scientific attestation: false. Engineering disposition: partial, with an unresolved validator integrity defect and containment violations. Terminal delivery validation is not run by synthesis. The coordinator must first save its returned phase result.

## 1. Strongest checked result

The campaign executed mathematical investigations, not only infrastructure work. The strongest checked package is a dynamics-realizable rational counterexample to the universal pairwise-compatibility shortcut, including exact continuous-box infeasibility and attained instance values. Two public attempts produced related examples; independent reviewers executed their checks. This is not a new-to-literature claim.

D1 fixes T=2, r=1, two-dimensional state/control/disturbance, a singleton first program, continuation box [0,2]^2, hard terminal nonnegativity and signed terminal sum cost. All three distinct disturbance prefixes give measured state (0,0). Four original complete paths include two different hidden suffixes under the same prefix. At q=3/2 every pair of prefix continuation sets has an explicit feasible rational witness, but the common state program would satisfy

    -u <= -1, -v <= -1, u+v <= 3/2,

whose nonnegative sum is 0<=-1/2. Exact trajectory checks and inequality certificates establish prefix optimum 1/4 and state optimum 2, both attained by explicit controls. The singleton first-stage box makes this an instance-level optimized gap as well as a fixed-a gap. Infeasibility concerns every rational control in the continuous box, not a sampled action menu. D1 executes 11 positive/rejection cases, including rejection of suffix-dependent decisions, a false witness, a negative multiplier and a sign-mutated certificate.

D2 uses three complete paths, three distinct prefixes, the same measured zero state and a common two-coordinate recourse matrix. At q=1 its three pair witnesses work, while actual path rows sum to 0<=-1. Prefix value is 0 and state value 2 in that instance. At q=2 a common program works despite unequal directional residual signatures: equality of signatures is not necessary for compatibility at one bound. Hard constraints alone are jointly feasible, so the nonzero signed objective is material. D2 separately rejects a clairvoyant assignment under two suffixes sharing one prefix.

Evidence: `research/baseline/derivation.md`, `checks/candidate-v1.json`, `checks/manifest.json`, `checks/exact.stdout.json`; `research/structured/derivation.md`, `checks/instances.json`, `checks/manifest.json`, `checks/D2-trajectories.stdout.json`, `checks/D2-certificates.stdout.json`. Relative `checks/` paths in this paragraph belong to the immediately preceding attempt directory. Original author check IDs remain distinct from repair and independent review observations in the index.

## 2. Declared model and inference boundary

The frozen question is `correlated-continuation-compatibility-v1` in `research/question.md`. Rational linear dynamics use a supplied finite nonempty set of complete disturbance paths, retaining correlations exactly. A policy is chosen before nature selects a path. At time r, x_r is measured; the whole second-block program is then selected before w_r enters. There are no later measurements. Prefix policies depend on w_<r, never independently on each full path; state policies depend only on reachable x_r. Every original suffix remains universally quantified. The objective minimizes worst signed terminal cost, not an absolute norm or a positive reward guarantee.

The examples intentionally erase prefix influence on the measured state. They expose predictive information in correlations; they are not a nondegenerate observability theorem. They do not establish robustness under nonzero prefix injection, continuous uncertainty, arbitrary first-stage optimization, multiple measurements or a general OGU/ARO correspondence theorem. Imported scalar finite-action tools cannot evaluate this matrix/continuous-box model; their passing tests are auxiliary engineering controls only.

Both attempts derive a common-matrix residual representation K_p={b in V:L b<=d_p(a,q)} using directional maxima over the actual conditional suffix sets. Signature equality and blockwise-independent suffix availability give sufficient losslessness arguments at fixed a. Those general arguments, D1's at-most-k+1 row-attaining-prefix consequence, and scalar/rank-one intersection statements remain `unproved-sketch`. No scientific Lean statement was proved or comparator-certified. Exact arithmetic execution proves only the declared instance consequences and certificate identities, not the complete general argument.

## 3. Actual successor outcome

E started from the question, frozen resources and D2 standalone handoff, without predecessor conversation. It reconstructed D2-C1: rank<=1 might make pairwise compatibility sufficient. It found an omitted singleton convention: distinct-pair compatibility is vacuous for a one-prefix cell even when that residual system is empty. Rank-zero and rank-one singleton instances refute that literal parent.

E retained the parent and wrote a corrected child requiring each K_p nonempty as well as pairwise compatibility. Its constructive rational projection/section argument covers zero rows, negative coefficients, rank zero, degenerate boxes and singleton images. This general child remains unformalized. Six new exact boundary cases and one separate hidden-suffix timing control executed successfully; normal/-O rank-one outputs agree. The new q=1 incompatible pair also prevents overstating rank one as unconditional prefix/state losslessness. This changed the research state rather than merely replaying D2.

Evidence: `research/continuation/reconstruction.md`, `derivation.md`, `timing-control.md`, `results.json`, `checks/manifest.json`, `checks/timing-manifest.json` and their bound stdout/stderr. Input paths and access limits are recorded in `input-identities.json` and results. Freshness is conversational, not demonstrated filesystem privacy or independent mathematical authority.

## 4. Source attribution and possible contribution

The campaign's six-source comparison is `research/closest-results.md`; original PDF identities, read pages and extracted/rendered anchors are in `research/resource-manifest.json` and `research/sources/anchor-catalog.json`. Synthesis relies on that persisted source examination and F's reported page rereads, not a new literature search or fresh reading of all PDFs.

| Source and PDF anchor | Known premise/result used for comparison | Why it does not automatically settle the selected model |
| --- | --- | --- |
| A2 pp2–4; A3 pp2–4 | Single measured-state closure, then a whole control program; source-specific dynamics/objectives | Their block disturbance availability is not the supplied correlated conditional suffix family; no numerical source example is reproduced here. |
| A4 pp2–6, especially p4 Assumption 1 | State measured before selecting the block program; independently available blockwise disturbances and existence assumptions | Our correlated paths and allowed infeasibility deliberately change those premises. The examples do not refute A4's recursion. |
| Ben-Tal et al. 2004 (BT04), p3 and pp4–5, Theorems 2.1–2.2 | Restricted information bases; independent-row assumptions; fixed-recourse vertex programs | Independent full-data recourse does not impose equal-state coupling or preserve prefix nonanticipation. Compactness alone does not supply independence. |
| GTW20 pp3–4, Proposition 1 and Example 1 | Fixed-recourse extreme-point interpolation; known failure when recourse coefficients are uncertain | Interpolation weights may depend on information unavailable to a state policy; the known uncertain-recourse example is not our construction. |
| GTW25 pp6–9, Theorem 1 | Specific sign/inverse/attainment premises for affine-rule optimal-value equality | It does not identify full data with x_r or assert equality of all bound-feasibility sets for every fixed a. |

Contribution categories are therefore distinct:

- Known framework/reconstruction: information restrictions, robust epigraph bounds, common-matrix residual inequalities and elementary interval reasoning.
- Campaign-local concrete contribution: two replayed rational separating constructions, explicit optimum/infeasibility certificates, and preserved timing/sign/correlation negative controls.
- Sharpened unresolved claim: E's corrected rank-one child, including the individual-nonemptiness premise; its general proof is still a written argument.
- Literature delta: none established. These examples may be new to this project but may be known or immediate specializations in the wider literature. The possibility that the campaign produced no novel scientific result is explicit.

## 5. Independent execution and engineering findings

F initially executed five scientific routes, reproducing D1's 11 cases, both D2 routes, E boundary and E timing outputs. Final F recheck executed the three repaired D1/D2 scripts plus the two E scripts in normal/-O: ten exit-0 processes with empty stderr and byte-identical historical stdout, as recorded in `artifacts/campaign/phases/12-final-review.json`. These are reviewer execution observations, not an LLM truth vote. Separate per-process F raw streams were not persisted as campaign files; the phase summaries are the retained independent observation records. The index distinguishes these coordinator-persisted observations from author/repair raw streams rather than fabricating missing F raw files.

The final reviewer also observed 34 campaign, 7 imported baseline and 16 checker unit tests passing in each Python mode, and Ruff/format passing on 11 active campaign-owned files. Historical failures remain: C's six raw TXT files lack final LF; original D1/D2 quality checks failed (35 combined Ruff findings and D1 format failure); E style and repair-report style each failed an advisory diagnostic; repair development tests/lint had intermediate failures. Versioned *_v2.py scripts preserve original frozen scientific bytes and observations. No statement that all tests ever passed is warranted.

One authorized repair closed the three concrete initial validator bypasses: omitted original scientific obligations, self/cyclic blockers and cross-stage phase links. Dimension-rejection regressions and v2 checkers passed. A residual P1 survives: the validator checks current refs but does not fully enforce original B outputs[].sha256. Final review's disposable full-bundle probe consistently rehashed a shared Lean stdout across four referencing checks; validation still accepted it while the original frozen parent stayed unchanged. Real B output bytes were not altered. The original stdout SHA-256 is `5527355068512c8187bd0cb3d5d9a3d81b517be20edac170461acb522a7da939`; the fabricated fixture's replacement was `2b95095c62c3c0866a99606e487e37e3cd6ebb9f30840745e051d3728177333e`. This finding remains unresolved even if later terminal accounting returns 0. No second repair is authorized.

B's sandboxed comparator failed before judging with `bwrap: setting up uid map: Permission denied`; dependent mismatch/definition/axiom controls remain blocked. Wrapper inventory controls and toy Lean semantic compilation are narrower successes, not scientific statement fidelity. TLC reproduced 94 distinct base states and intended invariant violations in two changed configs (exit 12), certifying only the bounded protocol model. Full filesystem containment failed through automatic harness output spills, including synthesis's `/tmp/pi-codemode-44dac734480467e3.txt` and `/tmp/pi-codemode-175b7c38466c790f.txt`; these external files were not read or removed. Subprocess scratch routing is campaign-local, not a host sandbox.

## 6. Descriptive comparison and effort

D1 and D2 each had one sequential public/nonisolated attempt, the same frozen question/source/tool pool and 90-minute/60-invocation instructional envelope. D1 produced the richer four-path hidden-suffix example and exact 1/4 versus 2 values. D2 made the operator/negative-knowledge record explicit, used a smaller three-path obstruction and supplied the rank-one successor obligation. E added singleton counterexamples and a corrected child. These observations do not establish superiority, causation, productivity rates or statistical significance. Access separation was instructional, not blind; internal provider retries are unknown.

D1 records 0.04969696496846154 seconds for its scientific subprocess; D2 records 0.56567595602246 seconds for four scientific processes; E records 0.20811706501990557 seconds for its scientific processes. These quantities exclude reading, derivation, checker development, packet preparation and writing and are not comparable end-to-end costs. D1 records 34 calls at a persistence point (36 in its phase handoff); D2 records 52 at its result amendment, with differing measurement endpoints. Full worker wall time and provider usage/billing are unknown. B's 17.918-second initial probe also excludes implementation/later waves. C's six-PDF copying, extraction, rendering, anchor work and shared packet, plus B tooling and repair/reviews, are preparation/helper costs, not free inputs or D2-only effort.

## 7. Decisions and one next step

The owner must decide whether the source-grounded examples warrant further study, whether to authorize a separate repair of the residual delivery-integrity defect/environment, and whether to approve any exact scientific statement for later formalization. No live status, corpus, threshold or journal changes occurred; private trials and human attestation were not run.

Recommended next step: have the owner review the exact corrected E rank-one statement and its source boundary before authorizing a bounded formalization/novelty follow-up. This tests the most substantive surviving obligation without repeating solved examples or treating infrastructure completion as discovery. The current campaign stops with its unresolved engineering finding and no established literature novelty.
