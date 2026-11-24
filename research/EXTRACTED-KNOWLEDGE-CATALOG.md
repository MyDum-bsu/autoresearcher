# Каталог извлечённых знаний — R1a (`#1152`, Round 2)

> **Этап:** `R1a` — **ревизия Round 2** (исправлены оба замечания независимого ревью Pi/Sol).
> **Режим:** строго **READ-ONLY** по всем 7 исходным репозиториям (`0` удалений, `0` модификаций — подтверждено живой пофайловой проверкой SHA-256 всех 2 531 dirty/untracked/intake файлов + 83 tracked_core файлов).
> **Staging-каталог:** `<staging>/aro-v2-r1a-staging/` (итоговый манифест перенесён в `legacy/migration-manifest-r1b.json`)
> **Независимая проверка в репозитории:** `make verify-migration` (`verification/gates/verify_baseline.py`)

---

## 0. Что исправлено в Round 2 по замечаниям независимого ревью

1. **Убраны 5 дублирующихся записей из `extraction-manifest.json`:** `build_r1a.py` теперь строит `tracked_core` строго через `git -c core.quotepath=false ls-files` с исключением dirty/untracked путей (`reading-dossiers`: ровно 17 уникальных файлов вместо 22 с 5 дублями). В `verify_r1a.py` добавлена проверка уникальности `(repo, rel_path)` и **биекции 1-в-1** между манифестом и файлами на диске (`423 / 423` уникальных файла).
2. **Извлечены ВСЕ 15 уникальных `.md`-отчётов и планов из `DISCARD-NOISE` в `EXTRACT-REFERENCE`:** в том числе оба указанных ревьюером файла — `artifacts/goal/wave-1/engineering-review/report.md` (независимое ревью G2) и `artifacts/bridge/formal-v1/statement-review/report.md` (постраничная сверка с A4), а также `bridge/formal-v1/statement-map.md`, `artifacts/bridge/formal-v1/setup/report.md`, `goal/engineering/report.md`, `artifacts/bridge/formal-env-v2/outcome.md`, `artifacts/goal/wave-3/style-review.md` и 8 `plan.md`/`recovery-plan.md`. В `verify_r1a.py` добавлен жёсткий инвариант: **0 уникальных `.pdf` И 0 уникальных `.md` файлов в `DISCARD-NOISE`**.
3. **Усилена проверка «0 мутаций» в `verify_r1a.py`:** вместо сравнения только `HEAD` и текста `git status`, теперь сверяется **живой SHA-256 каждого исходного файла** во всех 7 репозиториях (`2 531` dirty/untracked/intake + `83` tracked_core) против `before-git-snapshot.json` и `extraction-manifest.json`.

---

## 1. Сводные показатели (100% покрытие всех 7 директорий)

Все **2 531** dirty/untracked/intake файл во всех 7 каталогах `aro-discovery*` + **83** ключевых `tracked_core` файла основного `aro-discovery` (всего **2 614 уникальных записей**, `0` дублей) классифицированы по трём корзинам:

| Корзина | Файлов | Объём | Назначение |
|---|---:|---:|---|
| **`EXTRACT-CORE`** | **235** | **41,74 МиБ** | Живое ядро для новой базы `v2/clean-base` (корпус, скрытые PDF, Lean 4 F1/F2 + наработка F3 + контроли C1–C6, оракулы M0, сертификаты A4 `r=67/104`, контрпримеры D1/D2/E/Astra, эссе 20.10, негативные контроли гейтов). **100% SHA-256 проверены.** |
| **`EXTRACT-REFERENCE`** | **188** | **2,11 МиБ** | Справочный архив `legacy/extracted/` (17 уникальных досье чтения литературы, **15 независимых ревью/отчётов/statement-map из `campaign`**, 8 планов кампании, 25 отчётов/брифингов, 16 спецификаций, материалы волн 1–7, архитектурные обзоры, план перезапуска, контракты досье, аудит-квитанции Lean, comparator-фикстуры, глоссарий и документы v1). **100% SHA-256 проверены.** |
| **`DISCARD-NOISE`** | **2 191** | **84,07 МиБ** | Однозначный шум: сырые stdout/stderr/exit-потоки, 13 286-файловые хэш-печати, логи git-fetch/прокси, устаревшие Lean/build-артефакты `formal-v1`, 30 одноразовых `.workflow.js`/прокси-скриптов, промежуточные `pdftotext`/`pdftoppm`/`bbox`-срезы, 25 побайтовых дублей (каждый доказан по SHA-256 через `duplicate_of`) и сломанные `events.jsonl`/`science.db` (уйдут в git-тег `archive/v1-pre-clean`). Плюс ~750 МиБ gitignored `.lake/`-пакетов и кэшей. **0 уникальных `.pdf` и 0 уникальных `.md` выброшено.** |

### Разбивка по 7 исходным репозиториям

| Репозиторий / worktree | `EXTRACT-CORE` | `EXTRACT-REFERENCE` | `DISCARD-NOISE` | Статус исходника |
|---|---:|---:|---:|---|
| `aro-discovery` (основной + tracked core + intake) | 80 | 35 | 2 | **Не изменён (live file SHA OK)** |
| `aro-discovery-baseline` | 20 | 1 | 0 | **Не изменён (live file SHA OK)** |
| `aro-discovery-architecture` | 0 | 11 | 0 | **Не изменён (live file SHA OK)** |
| `aro-discovery-restart-plan` | 0 | 3 | 0 | **Не изменён (live file SHA OK)** |
| `aro-discovery-dossier` | 0 | 14 | 8 | **Не изменён (live file SHA OK)** |
| `aro-discovery-episodes` | 27 | 5 | 18 | **Не изменён (live file SHA OK)** |
| `aro-discovery-campaign` | 108 | 119 | 2 163 | **Не изменён (live file SHA OK)** |
| **Итого (уникальных записей)** | **235** | **188** | **2 191** | **0 удалений, 0 правок** |

---

## 2. Что именно спасено в `EXTRACT-CORE` (235 файлов, 41,74 МиБ)

### 2.1. Литература: корпус + скрытые внешние PDF (75 файлов, 35,62 МиБ)
- **Основной корпус (`extracted-core/corpus/`, 64 файла, 27,91 МиБ):** все 24 внешние статьи по ARO + 5 работ школы Дмитрук (`A1`–`A5`) + 5 TeX-исходников + `MANIFEST.md` (все **42 файла из `MANIFEST.md` прошли сверку SHA-256** внутри staging).
- **Препринты из gitignored `corpus/intake/` (3 файла, 1,92 МиБ):** `2207.03291.pdf`, `2409.12630.pdf`, `2608.22999.pdf`.
- **Спасённые внешние первоисточники из волн `campaign` (`extracted-core/literature-extra/`, 8 файлов, 5,79 МиБ):** 7 уникальных PDF + 1 errata, **которых не было в `corpus/`**: `hanner-1956.pdf`, `helly-survey.pdf`, `dvm-2024.pdf`, `iyengar-tr-2002-07.pdf`, `wkr-2013.pdf`, `AS03.pdf`, `AS03-errata.txt`, `BG10-author.pdf`.

### 2.2. Формальное ядро Lean 4 (`extracted-core/lean/`, 28 файлов)
- **`BridgeFormalV2/` (5 файлов):** **10 доказанных без `sorry` деклараций F1/F2** (Lean `v4.35.0-rc2`, аксиомы строго `{propext, Classical.choice, Quot.sound}`).
- **`BridgeFormalV3/` (3 файла — спасённая наработка F3):** `Goals.lean`, `Proofs/Support.lean` (136 строк: `future_expansion`, `attained_support`, `robust_row`, `exact_tightening`), `Proofs/Inventory.lean`.
- **`controls/` (14 файлов `.lean`/`.py`):** позитивные и негативные контроли `ControlFixture.lean`, `C1.lean`..`C6.lean`, `C6Negative.lean`, **исправленный `C2V2.lean`**, `replay.py` и `make_controls.py`.
- **`v1-aroform/Aroform.lean` (1 файл):** 3 базовые доказанные леммы P1–P3 (`l1_eq_max_sum_diff`, `info_value_monotone`, `one_d_exactness`).
- **`config/` (5 файлов):** `lean-toolchain`, `lakefile.toml`, `lake-manifest.json`, `expected-theorems-v2.json`, `expected-theorems.json` (v3).

### 2.3. Точные рациональные оракулы, сертификаты A4 и перенос ОГУ → ARO (`extracted-core/oracles/` & `bridge/`, 51 файл)
- **`oracles/m0/pilot/` + `oracles/m0-artifacts/` (20 файлов):** конечный эталон `finite_reference.py`, независимый Беллман `finite_bellman.py`, сертификатор открытого контура A4, входы и эталоны (**36/36 автотестов OK прямо из staging**).
- **`oracles/wave4-a4-closures/` + `certificates/` (22 файла, 4,40 МиБ):** solver-free верификатор `check.py` (64 контроля) + 10 файлов точных рациональных сертификатов A4 (`r=67` и `r=104`).
- **`bridge/transfer-v1/` (9 файлов):** `correspondence.md`, `methods-and-boundaries.md`, `numeric-ledger.json`, `check.py` (32 контроля), `sources.json`, `claims.json`.

### 2.4. Контрпримеры, аналитические теоремы и эссе (`extracted-core/counterexamples/` & `research/`, 54 файла)
- **`D1-baseline` (6 файлов):** 4-путевой контрпример потери предсказательной информации (`q=3/2`, префикс `1/4` vs состояние `2`).
- **`D2-structured` (11 файлов):** 3-путевой треугольный контрпример (`q=1` пары допустимы, совместно `0 ≤ −1`).
- **`E-rank1` (8 файлов):** singleton-контрпримеры при ранге `≤1` + конструктивный интервальный вывод.
- **`astra-probe-AS1` (6 файлов):** ранг-2 покоординатно-разделимый подкласс `A-S1` + 38-проверочный точный чекер.
- **`wave5-support-bound` (10 файлов):** общая двойственная оценка `J ≤ V₀ ≤ Vᵣ ≤ D₀ + Δ` + SymPy-чекер.
- **`exactness-essay` (12 файлов):** аналитическое эссе `2026-10-20` (4 понятия точности, O1–O8, батарея T1–T7 + 5 векторных графиков).
- **`guides-source/ogu-aro-01-foundation.md` (1 файл):** обзорный пакет 01 для владельца и научрука.

### 2.5. Негативные контроли гейтов (`extracted-core/gates/episodes/`, 27 файлов)
- 4 публичных эпизода `F/M/P/R`, эталоны, негативные контроли (`F-erased-refutation`, `M-wrong-information`, `P-unsupported-axiom`, `P-wrong-statement`, `R-ignore-contradiction`) и 22 теста.

---

## 3. Что сохранено в `EXTRACT-REFERENCE` (188 уникальных файлов, 2,11 МиБ)

| Категория | Файлов | Что внутри |
|---|---:|---|
| `campaign-reports` | 25 | Все отчёты и русскоязычные брифинги кампании 13–14 ноя |
| `campaign-waves-math` + `meta` | 32 | Аналитические отчёты, литературные сравнения, решения и манифесты волн 1–7 |
| `reading-dossiers` | 17 | Все уникальные досье чтения литературы (12 tracked + 5 untracked, 0 дублей) |
| `campaign-specs` | 16 | Спецификации кампании, волн 1–7 и formal-v2/v3 |
| `campaign-independent-reviews` | 15 | **Все 15 уникальных ревью, отчётов и statement-map из `campaign`** (включая `wave-1/engineering-review/report.md`, `formal-v1/statement-review/report.md`, `formal-v1/statement-map.md`, `formal-v1/setup/report.md`, `formal-v2` statement/proof/final, `formal-v3` statement, `transfer-v1/review`, `wave-1/4/5` scientific/independent reviews, `goal/engineering/report.md`, `formal-env-v2/outcome.md`, `wave-3/style-review.md`) |
| `dossier-contracts` + `artifacts` | 14 | Схема офлайн-досье `pilot/science/`, `single-measurement-statement.md`, примеры и отчёты |
| `architecture-research` | 11 | Архитектурные записки и обзоры систем |
| `campaign-plans` | 8 | Все 8 уникальных `plan.md` / `recovery-plan.md` кампании |
| `campaign-research-core` | 8 | `closest-results.md`, `contribution-dossier.md`, `domain-packet.md`, `question.md`, `anchor-catalog.json` |
| `lean-comparator-fixtures` | 7 | Фикстуры Lean-компаратора (`Axiom/Dependent/Semantic/Valid/Wrong.lean`) |
| `pilot-specs` | 7 | Спека `2026-11-10-research-harness-pilot.md`, TLA+ модель `PilotPublication.tla/.cfg` |
| `lean-audit-receipts` | 6 | `theorem-audit.json` (F1/F2), `controls-execution.json`, `formal-v3/state.json` |
| `episodes-docs`, `restart-audit`, `restart-plan`, `baseline-report`, `v1-foundation-docs`, `glossary`, `v1-rational-lp`, `campaign-tests` | 22 | `FOUNDATION.md`, `GLOSSARY.md`, `THESES.md`, `HYPOTHESES.md`, `2026-11-10-restart-audit.md`, проверка первоисточников (вкл. Дмитрук 2023 `into1170`), `exactlp.py`/`aro2s.py`, тесты кампании |

---

## 4. Что отнесено к `DISCARD-NOISE` (2 191 файл, 84,07 МиБ) и почему это безопасно

| Категория шума | Файлов | Объём | Почему безопасно отбросить |
|---|---:|---:|---|
| `campaign-run-artifacts` | 1 228 | 49,76 МиБ | Сырые `*.stdout`/`*.stderr`/`*.exit`, 13 286-файловые `actual-import-closure.json`, `candidate-seal*.json`, `tmp/`-дампы. Все научные выходы, сертификаты, контроли, PDF и `.md`-ревью извлечены. |
| `infra-build-proxy-logs` | 591 | 9,22 МиБ | Логи `git init/fetch/checkout` зависимостей Lean и дампы отладки прокси Pi SDK (все уникальные `.md` извлечены). |
| `pdf-text-png-scratch` | 100 | 9,04 МиБ | Промежуточные `pdftotext`/`pdftoppm`/`bbox`-файлы (исходные PDF сохранены в `corpus/` и `literature-extra/`). |
| `exact-duplicate` | 25 | 7,46 МиБ | **Побайтово идентичные дубли** (каждый доказан по SHA-256 через `duplicate_of` и проверен `verify_r1a.py`). |
| `superseded-formal-v1` + `v1-ns` | 119 | 4,93 МиБ | Устаревшие неудавшиеся `.lean`/build-артефакты `formal-v1` (все `.md`-отчёты и `statement-map.md` извлечены; само доказательство заменено на `BridgeFormalV2`). |
| `v1-legacy-db` | 2 | 2,88 МиБ | Сломанные `events.jsonl` и `state/science.db` (сохранятся в git-теге `archive/v1-pre-clean` в `R1b`). |
| `campaign-check-logs` | 61 | 0,18 МиБ | Сырые stderr/stdout/ruff/style-логи (весь код, выводы, результаты и handoff извлечены в CORE). |
| `one-off-workflow-scripts` | 30 | 0,19 МиБ | Одноразовые `.workflow.js` и прокси-обёртки кампании. |
| `campaign-engineering-harness` | 19 | 0,36 МиБ | Одноразовый harness кампании 13 ноя (`goal/engineering/*.py/*.json`, сломанный на `KeyError: 'id'`; отчёты `.md` извлечены). |
| `episodes-run-logs` | 16 | 0,06 МиБ | Повторно генерируемые логи `ruff`/`tests`/`validation` из `episodes/artifacts/`. |

---

## 5. Выполненные проверки (Round 2)

1. `python3 -B <staging>/verify_r1a.py` → **PASS (round-2)**:
   - `Zero mutations across all 7 repos (HEAD + status + live file-level SHA-256): 2531 dirty/intake + 83 tracked_core OK`
   - `100% coverage & 0 duplicate manifest entries: 2614/2614 unique OK`
   - `1-to-1 bijection manifest <-> staging disk & 100% SHA-256: 423/423 OK`
   - `Zero unique .pdf and zero unique .md files in DISCARD-NOISE: OK`
   - `corpus/MANIFEST.md verified in extracted-core: 42 files OK`
2. `python3 -B -O <staging>/verify_r1a.py` → **PASS (round-2)** (идентично).
3. M0 оракулы в staging (`extracted-core/oracles/m0/`): **36/36 тестов OK**.
