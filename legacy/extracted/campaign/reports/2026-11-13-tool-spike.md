# Phase B: observed tool readiness and delivery-integrity spike

Task: `aro-discovery-k4t`. Workspace: `<workspace>/aro-discovery-campaign`; branch: `task/aro-discovery-k4t-campaign`.

**Comparator acceptance is unavailable.** The installed sandboxed comparator was actually invoked once and exited 1 with `bwrap: setting up uid map: Permission denied`. It did not reach target comparison. The three dependent native mismatch/dependency/axiom controls were not run. Sandbox bypass, alternate sandbox executables, detached exports, dependency installation and toolchain changes were not used.

The independent available routes remain usable: the toy Lean package compiled, all three bounded TLC controls produced their expected observations, and the imported exact finite tools passed their scoped tests and explicit positive/infeasible/tampering controls. Delivery validation passed 26 synthetic tests in each Python mode and scoped Ruff/format checks. These are engineering observations, not scientific acceptance, semantic correspondence, novelty or human attestation. Phase C can proceed with source reading and matching-scope exact checks without comparator evidence.

## Authority and preserved inputs

Read the charter and reviewed execution plan in full, FOUNDATION, AGENTS, glossary, all four planning/review phase records, v1/v2 contracts and coordinator activation. The activation selects v2 and repairs the coordinator sequencing conflict without changing the historical planning reviews. No tracker, live scientific state, corpus, glossary, configuration, journal, sibling worktree or workflow source was written. No nested agents/workflows, commits or pushes were used.

Observed and rechecked identities:

| Input | SHA-256 |
| --- | --- |
| Preserved v1 contract | `7fdbb89598f1124b03122ddb9dc9d3855950f9e6fdc79ada272f43f11fdf7ce3` |
| Activated v2 contract | `5327189652994a1f531c91d481cc588e89dff6ec0f093a1198a54c083f30fb0c` |
| Original workflow | `228bda51a9a1e21d90eac2444e992224080f07e175dac08c2d6f409cdd4d87c6` |
| Active continuation workflow | `f67b8a0413a92876440e897952bcbaace87ce6fab4ecd3c64c4f38fdc0ae3114` |

Initial root, branch and dirty/untracked inventory were checked before editing. Existing campaign inputs were preserved. The installed effective environment exposed `PI_PROVIDER=openai`, `PI_MODEL=gpt-6.1-sol`; no alternate provider/model was requested.

## Artifacts and reproducibility boundary

- `artifacts/campaign/tool-readiness.json`: all 20 mandatory B case IDs plus the supporting Lean build; observed or explicitly blocked dispositions, commands, input/output identities, control observations, imports and resource limitations.
- `artifacts/campaign/tool-spike/frozen-inputs.json`: fixtures frozen before initial native/finite executions. Includes immutable Lean source/config bytes, TLA source/config bytes, rational inputs and the single-setting TLA config differences.
- `artifacts/campaign/tool-spike/import-provenance.json`: eight byte-preserved imports and original/copy SHA-256 pairs.
- `artifacts/campaign/tool-spike/commands.json`, `delivery-commands.json`, `delivery-commands-v2.json`, `delivery-commands-v3.json`: retained command observations. Raw stdout/stderr are separate files. `all-command-records.json` consolidates the initial and first delivery wave; later versions remain separate and are listed by readiness.
- `artifacts/campaign/tool-spike/delivery-controls-inventory-v3.json`: active pre-execution snapshot for final delivery regressions, wrapper controls and the final finite adapter observation. Earlier inventories and transcripts remain historical evidence, not silently overwritten current-source identities.
- `research/tool-spike/comparator/`: six independent dependency-free Lean modules, four comparator configs, local package configuration and generated manifest/build outputs.
- `research/tool-spike/tla/`: unchanged copied model/base config and two separately named one-constant mutation configs.

The initial spike helper was formatted and import-cleaned after execution. Its execution-time helper bytes were not independently sealed before that run; do not invent that provenance. Imported finite executable bytes and frozen fixture bytes remained unchanged. Before subsequent validator hardening, source snapshots were archived; the first recovered snapshot was checked against its previously frozen SHA-256. Historical inventory paths describe historical bytes and must not be mistaken for hashes of the now-hardened live script.

Readiness is B evidence, not a ready-made final `evidence-index.json`. Final synthesis must combine phase records, sources, claims, findings and dynamic manifests, preserve historical evidence as historical, and supply the final index schema. It must not claim the future terminal validator has already accepted this campaign.

## Comparator and semantic controls

Installed Lean: `4.35.0-rc2`, commit `11acb17ec6b07a8f9e9173e6845197929540936b`. Installed `lake comparator --help` documents required module names, theorem inventory, explicit axiom allowlist, manifest and bubblewrap. The package has no external dependencies and was built with `lake --no-cache build`, exit 0. This generated its local `lake-manifest.json`; no `lake update`, package fetch or installation was run.

Frozen fixtures use `Campaign.expected`, the dependent definition `Campaign.Model`, and the custom axiom `Campaign.forbidden`. Each solution has its own source module; no Solution bytes were overwritten between controls. Comparator configs explicitly allow only `propext`, `Classical.choice`, `Quot.sound`.

| Case | Observation | Interpretation |
| --- | --- | --- |
| `cmp-valid` | `timeout 120 lake comparator --config cmp-valid.json`: exit 1; saved stderr contains uid-map permission denial | Failed attempted execution; tool readiness blocked before judging |
| `cmp-wrong-target` | Not run; native exit null | Blocked by positive sandbox failure; no statement-mismatch evidence |
| `cmp-dependent-definition` | Not run; native exit null | Native definition-comparison behavior remains unknown |
| `cmp-forbidden-axiom` | Not run; native exit null | No comparator axiom-rejection evidence |
| `cmp-empty-inventory` | Executed campaign preflight exits 1 with `cmp-empty-inventory: empty-target-inventory`; native exit null | Wrapper rejection only |
| `cmp-missing-inventory` | Executed campaign preflight exits 1 with `cmp-missing-inventory: missing-target-coverage`; native exit null | Wrapper coverage rejection only |

The compiled semantic module proves a concrete Nat witness `∃ n, n = 0`, disproves the false strengthening `∀ n, n = 0 → n = 1`, and proves that the nonempty domain/premise can coexist with infeasibility of `n = 0 ∧ n = 1`. `#print axioms` reports no axioms for these three declarations. These satisfy the toy `sem-satisfiable-premises`, `sem-false-conclusion`, `sem-infeasible-instance` controls at isolated-compilation scope. They are not comparator acceptance or an OGU/ARO statement. The custom-axiom fixture intentionally compiles; compilation alone does not reject a forbidden axiom.

No native comparator control was retried. Later wrapper/finite/test waves checked revised local validation code, with separate inventories and outputs; they did not rerun the blocked native comparator.

## Bounded TLC reproduction

Used existing `~/.local/share/tlaplus/tla2tools.jar`, TLC 2.19. Ran sequentially with one worker, `-Xmx256m`, `-Djava.io.tmpdir=<campaign-local tmp>`, and `-metadir` inside campaign-local scratch. The copied model was not edited.

Command form from `research/tool-spike/tla/`:

```sh
timeout 120 java -Xmx256m -Djava.io.tmpdir="$TMPDIR" \
  -cp ~/.local/share/tlaplus/tla2tools.jar tlc2.TLC \
  -workers 1 -metadir "$TMPDIR/<case>" -config <case.cfg> PilotPublication
```

| Case | Sole config change | Exit | Generated / distinct states | Saved observation |
| --- | --- | --- | --- | --- |
| `tlc-base` | None | 0 | 163 / 94 | `Model checking completed. No error has been found.` |
| `tlc-stale-fence` | `AllowStaleSubmission = TRUE` | 12 | 55 / 35 | `Invariant SingleCurrentWriter is violated.` |
| `tlc-gate-bypass` | `AllowGateBypass = TRUE` | 12 | 68 / 48 | `Invariant AuthorizedCommit is violated.` |

Observation JSON was matched against the saved native streams and the unchanged v2 predicates. These are bounded protocol-model results, not implementation correctness, service reliability or mathematical proof.

## Minimum finite imports and exact observations

Imported only the two finite modules, their two test files and their two README contracts from the baseline sibling, plus the model/config from main. Dependencies inspected were standard-library imports and local P1 imports in P2 tests; no absolute sibling module imports are used at runtime. Existing source headers/notices and README bytes were retained. A bounded source-root license-file lookup found no separate license file; no broader licensing conclusion is made.

The shared finite scope is exactly `x1=a+k*p`, `x2=x1+b+q`, terminal cost `abs(x2)`, supplied correlated complete paths, finite rational action sets and an optional hard terminal interval. The independent Bellman solver and `check_result` certify declared finite optimum/infeasibility records, rather than merely replaying a witness. They do not handle general matrix dynamics, continuous uncertainty/controls or the continuous A4 optimum.

Frozen positive: one first action `0/1`, three second actions, paths `(-1,0)` and `(1,0)`, gain 1, no terminal interval. Its state/prefix value is exactly `0/1`, open value `1/1`. Frozen infeasible: same nonempty paths, only second action 0, terminal interval `[0,0]`; both routes return typed infeasibility with null value in all three information modes. Across both instances and all three modes, enumeration and Bellman agree, and `check_result` accepts the enumerator result.

The tamper changes only the positive state certificate value from `0/1` to `1/1`. The actual checker raises `invalid_witness` with `Incorrect exact value or per-path outcomes`; no handwritten validity field substitutes for that call. Empty paths produce `invalid_input`, not infeasibility. Two separately planned public-fixture subprocess runs produced byte-identical stdout. The explicit finite control is tiny: at most `1*3^2=9` policies per mode for its positive instance; imported 144-instance regressions are separate software coverage, not a new scientific search grid.

`scripts/campaign_finite_probe.py` is a campaign-owned observation adapter; it does not modify either imported algorithm. Its raw stdout contains the actual enumerator/Bellman/check_result records and caught checker exception fields.

## Delivery-integrity implementation

`scripts/campaign_acceptance.py` uses only the standard library and no live APIs. The shipped no-argument CLI selects the exact v2 path, checks coordinator activation and preserved v1 identity, and has no contract fallback. Exit 0 denotes structurally consistent accounting, including honest negative/blocked operations; exit 1 denotes delivery inconsistency; exit 2 denotes invalid invocation or unreadable/malformed mandatory contract. No exit establishes mathematical truth.

Implemented checks include mandatory and conditional phase/file/stage/check/mechanism inventories; strict JSON duplicate-key/nonfinite rejection; terminal enums; boolean/integer separation; file sizes/hashes and path/symlink containment; explicit unavailable-file failure links; unsafe-C dependent-stage records; repair/recheck pairing; source-copy and available original-source hashes; dynamic nonempty case/target coverage; command/input/raw-output binding; typed expected-control matching and actual native diagnostic substrings; output-as-input substitution rejection; nonempty required artifacts; checked-claim kind and separately identified independent replay links; and resolved-finding recheck links. The final index is not required to hash itself, and can name itself as a synthesis output.

All 19 frozen regression IDs are represented in `tests/campaign/test_campaign_acceptance.py`. Additional focused tests cover target coverage, native-versus-wrapper exits, no missing-contract fallback, output/input substitution, empty required documents and non-self-hashed index output. The final suite has 26 test methods, including negative-observation subcases. Synthetic bundles are delivery fixtures, not research results.

The validator validates declarations, identities and links. It cannot authenticate arbitrary claimed process execution, decide a prose argument, determine source applicability/novelty, or turn `result_kind` metadata into mathematical truth. Final independent code/Lean execution and the stated scope remain necessary. B did not run the full terminal CLI: mandatory C–F and `13-synthesis.json` do not yet exist. The coordinator must run it only after synthesis returns and is saved.

## Executed verification

All test descendants inherited:

```sh
export TMPDIR=<workspace>/aro-discovery-campaign/artifacts/campaign/tmp
export TMP="$TMPDIR" TEMP="$TMPDIR" PYTHONDONTWRITEBYTECODE=1
```

The directory was created and checked as a real in-root directory before tests. This redirects temporary files; it is not a filesystem sandbox.

| Command from campaign root | Observed result |
| --- | --- |
| `timeout 180 python3 -B -m unittest discover -s tests/campaign -p 'test_*.py'` | Final revision: 26 tests, exit 0 |
| Same command with `python3 -O -B` | Final revision: 26 tests, exit 0 |
| `timeout 120 python3 -B -m unittest discover -s pilot/baseline -p 'test_*.py'` | 7 tests, exit 0 |
| Same baseline command with `python3 -O -B` | 7 tests, exit 0 |
| `timeout 120 python3 -B -m unittest discover -s pilot/checkers -p 'test_finite_*.py'` | 16 tests, exit 0 |
| Same checker command with `python3 -O -B` | 16 tests, exit 0 |
| `ruff check --no-cache scripts/campaign_acceptance.py scripts/campaign_tool_spike.py scripts/campaign_finite_probe.py tests/campaign/test_campaign_acceptance.py` | `All checks passed!`, exit 0 |
| `ruff format --check --no-cache` on the same four files | 4 files already formatted, exit 0 |
| `git diff --check` | Exit 0; tracked-only check does not cover untracked artifacts |

Initial Ruff/format checks did fail; their diagnostic evidence was retained, and campaign-owned formatting/import/style defects were repaired without touching imported bytes. Earlier 23-test passing revisions and final 26-test outputs remain separate. No failed scientific/comparator observation was erased or reclassified into success. Final prose-wide style/whitespace lint was not run; the remaining instructional call budget was reserved for this report and handoff. Broad repository lint/types/build and the final campaign validator were intentionally not run.

## Resources, limits and next action

The initial tool probe took 17.918 seconds of observed local wall time, excluding preparation, implementation, subsequent validation waves and report writing. Command observations retain per-command timings where captured; this is not total agent effort or provider billing. The initial filesystem observation showed approximately 3.0 GiB free on a 98%-used filesystem. The local Lean build directory was about 252 KiB and local temporary artifacts about 3.7 MiB at inspection. Retained build/TLC scratch is small and remains campaign-local for review; no background job was left running.

Safe resource observations found unlimited process CPU/address-space soft limits in the inspected shell. This does not imply unlimited usable memory or safe large jobs. Timeouts bound the local subprocess invocations; forced cancellation and provider cancellation were not tested. The 60-call ceiling is instructional, not a demonstrated hard harness gate. Provider billing, internal retry settings and complete token accounting remain unknown. Worktree/cwd separation does not restrict sibling reads or provide confidentiality. Native executable identities were observed rather than fully pre-execution sealed.

Recommendation: proceed to C with the actual source packet and this narrow finite-checking scope. Keep comparator evidence unavailable unless the owner separately authorizes an environment repair; do not change global namespaces or disable sandboxing. The coordinator should persist `05-tools.json`, preserve these failures/limitations, and later assemble—not assume—the complete final index. No scientific attempt, fresh continuation or human attestation has been performed in B.
