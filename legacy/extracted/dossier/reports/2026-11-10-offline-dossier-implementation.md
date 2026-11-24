# Offline dossier implementation — aro-discovery-hg0

## Resume: два исправления после воспроизведения координатором

Независимое ревью **не принято**: reviewer `78ca474b` завершился с
`Connection error`, без итогового вердикта. Ни прежние зелёные проверки,
ни текущий ремонт не заменяют независимое ревью. Проверка координатором,
новое независимое ревью и закрытие задачи остаются за координатором.

В owner-authorized resume исправлены только две границы допуска:

- `pilot/science/contracts.py`: обязательный schema 2; `Claim.cases` теперь
  immutable tuple из frozen `Case(id, normalized_input_sha256)`, сортируемый
  по ID, без поддержки старых string-only списков. Binding входит в claim
  identity. ID и ссылки проверяются по грамматике
  `[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}`, SHA-256 — 64 lowercase hex.
  Проверяются также ID инстансов, сертификатов и inventory; пояснения остаются
  свободным текстом и сохраняются как данные.
- `pilot/science/packet.py`: build повторно нормализует каждый ожидаемый
  инстанс штатным unchanged checker и сравнивает вычисленный hash с inventory
  **до** допуска evidence. Evidence вне inventory отклоняется. Полное покрытие,
  premise/model validation и прежние научные ограничения сохранены.
- `pilot/science/tests/test_offline.py`: добавлены пять тестов; всего 22.
  Пересчитанные valid certificates для `strict_gain` с gain `2/1` действительно
  дают `1/1, 1/1`, но прежний binding их не допускает. Подмена ожидаемого hash
  отклоняется и после обновления claim hashes. Легитимная version 3 с новым
  binding и свежими ссылками принимается; stale action/evidence hashes — нет.
  Проверены 14 ID-позиций × 14 недопустимых значений, valid-ID control,
  narrative preservation, immutable case records и отказ старому списку.
  Помимо прежних 12 parent permutations проверены все 72 перестановки
  paths/first_actions/second_actions ребёнка: packet и binding неизменны.
  Premise/infeasibility fixtures обновлены, чтобы проверять именно прежние
  границы, а не останавливаться на новом inventory gate.
- `pilot/science/README.md` описывает schema 2 и грамматику. Перегенерированы
  только три `pilot/examples/offline-dossier-v1.*` файла. Имя illustrative
  example сохранено; submission и packet имеют schema 2, M0 records — schema 1.

### Реальные red/green команды resume

Все команды выполнялись после `cd <workspace>/aro-discovery-dossier`.
Все Python-вызовы использовали `PYTHONDONTWRITEBYTECODE=1`; повторов после
transient-сбоев, переключений модели и fallback не было.

Первым, **до реализации исправлений**, выполнен regression seam parse/build:

```sh
PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest pilot.science.tests.test_offline.OfflineTests.test_recomputed_certificates_cannot_change_frozen_case pilot.science.tests.test_offline.OfflineTests.test_claim_identifier_cannot_inject_attestation_heading
```

Red: `Ran 2 tests`, `FAILED (failures=2)`, оба `ContractError not raised`, exit 1.
После реализации и миграции example та же команда: `Ran 2 tests`, `OK`, exit 0.

| Остальные выполненные команды | Результат resume |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -m unittest discover -s pilot/science/tests -p 'test_*.py'` | 22 tests, OK; заключительный прогон 0.935s |
| `PYTHONDONTWRITEBYTECODE=1 timeout 120 python3 -O -m unittest discover -s pilot/science/tests -p 'test_*.py'` | 22 tests, OK; последний прогон 0.932s |
| `PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest discover -s pilot/baseline -p 'test_finite_*.py'` | 7 tests, OK |
| `PYTHONDONTWRITEBYTECODE=1 timeout 60 python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'` | 16 tests, OK |
| `timeout 30 ruff check --no-cache pilot` | All checks passed! |
| `timeout 30 ruff format --no-cache --check pilot/science` | 6 files already formatted |
| `git diff --check` | exit 0; untracked deliverables не охватываются git diff |

Перегенерация обоих outputs выполнена командами из исторического раздела ниже
с теми же absolute paths, `timeout 30` и bytecode flag. Science suite затем
запустил по два fresh CLI процесса для каждого формата, сравнил байты между
процессами и с generated examples, проверил отсутствие content writes экспортом.
`test_snapshot_all_files` и отдельный вызов `snapshot_integrity()` подтвердили
pinned manifest и все восемь frozen file identities. Не редактировались baseline,
checker, snapshot, specs/plans или исходный checkout.

SHA-256 текущих артефактов:

- input: `c602adb064214df56de210a8c5b20e9d989e04b8268f7dc914039164306f3ab9`;
- packet: `4d779c0f3859989b90a58d30e21c26fe3dad77b35a034a8d3fd3f2c500051b2f`;
- Markdown: `227ef5fb05d791f623cb5207e7deb5f31ef73d5a046ddf1798f116e749e98e9a`.

Структурные проверки resume (обе exit 0):

```sh
timeout 60 ripwire <workspace>/aro-discovery-dossier --quality-delta --no-cache --legend=compact
timeout 60 ripwire <workspace>/aro-discovery-dossier --edit-check=pilot/science/packet.py:build --no-cache --legend=compact
```

На `df8027532+dirty`: quality `gating=0`, `preexisting-worse=0`,
`new-symbol=79`; это **не** отсутствие нового долга. Untracked pilot считается
новым относительно HEAD. Сохранены явные небольшие validation idioms,
сходные certificate fixtures и размер unittest-класса; build имеет verbosity
finding 62 строки, ID regression — 61. Переносить model definition или дробить
узкие проверки ради метрики не стали. Edit-check: `status=new-symbol`,
`callers=3`, `incompatible=0`, `graph_ambiguous=2`, `graph_unresolved=90`,
`graph_unindexed=56`; это ограниченный структурный сигнал, не merge approval.
Никакие baseline/ack ledgers не записывались.

### Пределы и передача

Грамматика защищает текущую presentation от ID-инъекций; это не HTML sanitizer
для будущих renderer-ов. Hash binding фиксирует содержимое относительно claim,
но не удостоверяет автора и не запрещает человеку предложить новую версию.
Проверки перестановок исчерпывают только указанные finite fixtures; это не
доказательство для всего класса моделей. Human attestation остаётся `absent`,
novelty — `unassessed`, scientific status не меняется. OS sandbox,
concurrency/interpreter attacks, новые научные эксперименты и Lean — not run,
вне согласованного скоупа. Live state, tracker, commit/push не затронуты.
Координатору: заново проверить текущие файлы и выполнить независимое ревью;
результаты worker `beede40a` ниже являются историческими.

## Historical implementation by beede40a — retained, not current acceptance

Следующий исходный отчёт сохранён без удаления прежних результатов.
Он относится к реализации до двух воспроизведённых дефектов; прежние 17 tests
и schema 1 не являются текущей приёмкой и не подтверждают исправления resume.

Implemented the bounded offline microcycle on branch
`task/aro-discovery-hg0-dossier` at base `df8027532ebc8f59e37c63aabf9b2d2cd7b843ac`.
The required acceptance commands passed in this environment. No scientific live
state was published, and no theorem, novelty or human attestation is claimed.
Coordinator review and task closure remain outstanding.

## Files and implementation decisions

New files only:

- `pilot/science/contracts.py`: closed JSON parser, immutable typed records,
  defensive nested-value ownership and exact claim identities.
- `pilot/science/finite.py`: pinned eight-file snapshot integrity and independent
  `finite_bellman.check_result` adapter; premises checked before value comparison.
- `pilot/science/packet.py`: lineage, prerequisite/action eligibility, complete
  inventory checking, operational/scientific outcome separation, deterministic
  JSON/Markdown rendering with full M0 definitions and handoff context.
- `pilot/science/__main__.py`: explicit input and format, stdout-only export,
  nonzero rejection without a successful dossier.
- `pilot/science/tests/test_offline.py`: 17 targeted tests, including bounded
  normalization variants, negative mutations, fresh-process reproduction and
  filesystem inventory checks.
- `pilot/science/README.md`: schema, execution commands, scientific interpretation
  and explicit trust boundaries.
- `pilot/examples/offline-dossier-v1.json`: frozen public example input/inventory.
- `pilot/examples/offline-dossier-v1.packet.json`: canonical generated handoff.
- `pilot/examples/offline-dossier-v1.dossier.md`: generated illustrative dossier.
- `docs/specs/2026-11-10-single-measurement-statement.md`: proposed exact
  bound-witness correspondence statement and future proof/review obligations.
- `reports/2026-11-10-offline-dossier-implementation.md`: this report.

The initial inventory was written before tests: the parent's
`correlated_hidden_disturbance` counterexample and the restricted child's
`strict_gain` finite test. Certificates were copied from the unchanged imported
M0 reference artifact, then recomputed through the independent checker. The
production adapter does not import the enumerating reference implementation or
accept a submitted module path. The illustrative failed/cancelled/exhausted
attempts are explicitly labeled input examples, not historical incidents.

The module implements only equality of state/prefix finite optimal costs over
the M0 contract and the nonzero-prefix-gain restriction. Typed infeasibility is
rejected by this numeric relation. Free text never supplies executable theorem
semantics. Resources are checked declarations, not OS-enforced process limits.
No new dependency or root configuration change was required.

## Actual verification

All commands below ran from `<workspace>/aro-discovery-dossier`.
All Python commands used `PYTHONDONTWRITEBYTECODE=1`.

| Command | Observed result |
|---|---|
| `timeout 120 python3 -m unittest discover -s pilot/science/tests -p 'test_*.py'` | 17 tests, OK |
| `timeout 120 python3 -O -m unittest discover -s pilot/science/tests -p 'test_*.py'` | 17 tests, OK |
| `timeout 60 python3 -m unittest discover -s pilot/baseline -p 'test_finite_*.py'` | 7 tests, OK |
| `timeout 60 python3 -m unittest discover -s pilot/checkers -p 'test_finite_*.py'` | 16 tests, OK |
| `ruff check --no-cache pilot` | All checks passed |
| `ruff format --no-cache --check pilot/science` | 6 files already formatted |
| `git diff --check` | exit 0; no tracked baseline diff |

The science suite checks both output formats in two fresh CLI processes each,
compares them with the generated example bytes, and compares every
worktree regular file's content identity before and after those exports. This
checks observed filesystem behavior, not adversarial OS isolation or metadata
writes. The suite checks the pinned snapshot manifest SHA-256 and all eight
listed code/test/README/evidence hashes. The snapshot itself is not edited.

Canonical regeneration commands actually run, each with `timeout 30` and the
bytecode environment flag:

```sh
python3 -m pilot.science --input <workspace>/aro-discovery-dossier/pilot/examples/offline-dossier-v1.json --format json > <workspace>/aro-discovery-dossier/pilot/examples/offline-dossier-v1.packet.json
python3 -m pilot.science --input <workspace>/aro-discovery-dossier/pilot/examples/offline-dossier-v1.json --format markdown > <workspace>/aro-discovery-dossier/pilot/examples/offline-dossier-v1.dossier.md
```

The CLI has no output-file option; these two writes are explicit shell
redirections to allowlisted example outputs. Rejected CLI calls emit no packet
to stdout. The CLI tests also exercise an unreadable input with exit 2.

### Structural checks and observed limitations

`timeout 60 ripwire <workspace>/aro-discovery-dossier --quality-delta --no-cache --legend=compact --max-tokens=1800`
returned exit 0 at `df8027532+dirty`, with `gating=0`,
`preexisting-worse=0`, `new-symbol=70`. Ripwire reported that `--max-tokens`
is ignored for this verb. The findings include imported baseline code treated
as new because it is untracked, unittest discovery/callbacks treated as dead
code, test-class verbosity and short serializer/duplicate-key idioms shared
with the baseline. These are retained and reported, not suppressed or used to
modify baseline gates. This is not a claim of zero new debt or a full type check.

An initial edit-check invocation with the same `--max-tokens` option was
rejected (exit 1). After removing that unsupported option, the explicit command

```sh
timeout 60 ripwire <workspace>/aro-discovery-dossier --edit-check=pilot/science/packet.py:build --no-cache --legend=compact
```

returned exit 0: `status=new-symbol`, three identified callers,
`incompatible=0`, `graph_ambiguous=2`, `graph_unresolved=92`,
`graph_unindexed=56`. These resolver limits prevent treating this as an
exhaustive merge-safety proof. No baseline/ack ledger was written.

An initial science test run exposed a defect in the planted mutation fixture:
it removed another path on every nested checker validation, eventually making
the path set empty. The fixture was corrected to drop a path only once at the
parse boundary; the valid but altered instance is then rejected against the
original certificate. The unchanged production checker was not edited.
Initial Ruff findings (import ordering, unused import, a long literal and
nested context managers) were fixed only in the new implementation/test files.
No acceptance assertion or baseline gate was weakened.

## Scientific and editorial review boundaries

The parent retains independently checked values state=1/1, prefix=0/1 and a
matched-version counterexample. The child retains state=prefix=0/1 only on
`strict_gain`; finite survival is never upgraded to universal proof. A zero-gain
counterexample is rejected against the child's nonzero-gain premise.
Novelty remains unassessed and human attestation absent in both formats.

The proposed statement specifies rational linear dynamics, nonempty complete
paths, fixed measurement timing, reachable-state policies, consistent scenario
assignments, bounded controls, hard terminal feasibility and signed linear
cost bound. Both trajectory-preserving transformations are obligations, not
completed proofs. Logical review separated existential witness feasibility
from optimum attainment and finite induction from universal proof; it retained
explicit nonempty domains and legitimate infeasibility on both sides.

The imported baseline's source hashes establish byte identity only. Source/model
correspondence and producer authority are not established by matching hashes.
No external mathematical source assertion is introduced without an anchor;
closest-literature comparison and human semantic mapping remain unresolved.

The technical-style diagnostic was run separately on the README, statement
package and this report after its initial multiple-path invocation was rejected
with exit 2. The single-path diagnostics returned five README flags and three
statement flags (exit 1), and no report findings (exit 0). The flagged passages
retain necessary scope negations, full-program/full-trajectory distinctions,
and the schema requirement for unique IDs; they are not promotional claims.
These are reviewed style diagnostics, not failing scientific/code gates.

## Not run / not authorized

No Lean build or proof search, A4 numerical experiment, scientific campaign,
live `ro`/bootstrap operation, journal/blueprint/database/corpus/config write,
tracker update, dependency installation, subagent, commit, push, provider retry
or model switch was initiated by this worker. There was no broad repository
build, static type-check campaign, private holdout, concurrency attack,
interpreter sandbox validation or independent scientific review. Tests exercise
public frozen regression cases only. Independent review and task closure belong
to the coordinator; no tracker status was changed.
