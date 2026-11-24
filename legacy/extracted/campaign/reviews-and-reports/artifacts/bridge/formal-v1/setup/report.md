# S1: настройка заблокирована; определения и цели ещё не прошли elaboration

S1 не завершён: оба вызова Lean вернули exit 1 из-за отсутствующих `.olean`. Общего доказательства нет; пакет не готов к S3. Подготовлены реальные определения модели, десять точных F1/F2-целей, план доказательств и шесть семантических контролей. F3/F4 явно отсутствуют.

## Наблюдённый блокер

Получен чистый исходник официального Mathlib на `c58b47adb340faa641e363aef2a460dc534bf172`. Полный Apache-2.0 LICENSE прочитан; скачанный файл побайтово совпал с checkout. Его `lean-toolchain` — `leanprover/lean4:v4.35.0-rc2`, соответствует установленному Lean `11acb17ec6b07a8f9e9173e6845197929540936b`.

В pinned `Cache/Requests.lean:351-352` функция `curlRetryArgs` безусловно добавляет `--retry 5`; `Cache/Cli.lean:23-28` перечисляет поддержанные опции без отключения retries. Читались соответствующие Main/IO/Requests/CLI и Lake-конфигурация. При явном запрете automatic retries этот официальный helper НЕ запускался. Это консервативная остановка по ограничению задачи, а не доказанная недоступность cache и не утверждение, что все другие официальные пути невозможны. Не было попытки обойти запрет, изменить helper, подменить toolchain или собрать Mathlib целиком. Повторное разрешение этого противоречия остаётся координатору; автоматически продолжать нельзя.

Первая команда `git clone --no-checkout --depth 1 --revision=<pin> ...` получила exit 129: Git 2.43.0 не поддерживает эту опцию; сеть ещё не вызывалась. Сохранены stdout/stderr/exit. После чтения help синтаксис был исправлен: `git init`, `git remote add origin https://github.com/leanprover-community/mathlib4.git`, один `timeout 180 git fetch --depth 1 origin <pin>`, затем detached checkout `FETCH_HEAD`. Эта последовательность завершилась exit 0; ревизия и чистота checkout проверены. Никаких повторов сетевого fetch не было.

Официальный LICENSE URL: `https://raw.githubusercontent.com/leanprover-community/mathlib4/c58b47adb340faa641e363aef2a460dc534bf172/LICENSE`; `curl --fail --location --max-time 55 ...` завершился exit 0. Никаких insecure/proxy/credential/system изменений не было. Mathlib checkout занимает наблюдённые 152 MB и остаётся только в новом изолированном проекте.

## Файлы и проверка

- `bridge/formal-v1/plan.md`: локальный план, записанный до остальных новых файлов.
- `bridge/formal-v1/lean/BridgeFormal/Model.lean`: конечномерные реальные состояния, стационарные линейные карты, настоящая хронологическая recurrence, два положительных временных блока, непрерывные непустые disturbance boxes и ограниченные control boxes; измеримое правило на достижимых состояниях выбирает весь suffix без доступа к будущему. Сохранены обе стороны всех терминальных строк и signed cost.
- `bridge/formal-v1/lean/BridgeFormal/Goals.lean`: десять непроверенных целей типа Prop. Ни одна не объявлена доказанной теоремой. Суффиксная terminal expansion не предпосылка модели; её связь с recurrence — отдельная цель.
- `bridge/formal-v1/statement-map.md`: прямые PDF-якоря, словарь source → Lean, предпосылки, граф будущих доказательств, шесть заранее объявленных контролей и полный список пропусков.
- `bridge/formal-v1/expected-theorems.json`: точные ожидаемые будущие имена/типы десяти деклараций, proof-only каталог и allowlist оснований. Он не сообщает о наличии доказательств.
- `artifacts/bridge/formal-v1/setup/trusted-seal.json`: SHA256 доверенных candidate source/config/inventory, исполняемых Lean/Lake и upstream identity до proof development. Это заморозка кандидата, НЕ подтверждение elaboration или semantic fidelity. Любая последующая правка требует новой identity и ревью.
- `lean/lake-manifest.json`: сохранены все прежние mathlib/dependency revisions; переименован только root package. Это зафиксированное предполагаемое разрешение, не успешно загруженная Lake workspace.

Выполнено `timeout 180 python3 -B bridge/formal-v1/seal.py` → exit 0 самого сборщика свидетельств. Его exit 0 НЕ означает успех Lean. В отдельных subprocess с task-local TMPDIR/cache и явным LEAN_PATH:

| Команда из нового Lean-проекта | Exit | Фактический результат |
|---|---:|---|
| `lean BridgeFormal/Model.lean` | 1 | Нет `Mathlib/MeasureTheory/Constructions/BorelSpace/Basic.olean` |
| `lean BridgeFormal/Goals.lean` | 1 | Нет локального `BridgeFormal/Model.olean` |

Оба raw stdout/stderr/exit сохранены. Компилятор остановился на imports; синтаксис, типы, measurable instances и proposition bodies НЕ проверены. Ни ошибки imports, ни отсутствие доказательства не считаются корректным отрицательным semantic control.

Source-import inventory хеширует 1565 доступных source modules и отмечает отсутствующие зависимости; это лексическое приближение, не elaborator import graph: regex может захватывать `import` внутри block comments и давать ложные элементы вроде `A`, `B`, `Z`, `If`, `This`. Полная compiled dependency closure отсутствует. Этот дополнительный дефект инвентаризации явно запрещает считать seal готовым proof target. Core modules привязаны к точным compiler identities, а не к проверенному набору всех импортированных `.olean`.

## Покрытие

| Узел | Что подготовлено | Kernel proof / axioms / controls |
|---|---|---|
| F1 | ExpansionGoal, PrefixSplitGoal, SourceChronologyGoal, SuffixExpansionGoal | нет; imports blocked; axiom audit not run |
| F2 | ExogenousImageGoal, ObservationFibreGoal, ForwardPolicyGoal, ReversePolicyGoal, EpigraphEqualityGoal; prerequisite NonemptyBlocksGoal | нет; imports blocked; axiom audit not run |
| F3 | отдельная обязанность exact future support elimination | proposition и proof отсутствуют |
| F4 | отдельная обязанность finite formulation + Borel real-state selection, включая relative dimension | proposition и proof отсутствуют |
| C1–C6 | зафиксированы в statement-map до исполнения | not run: среда не готова |

Не формализованы extended-value convention/оптимальный value, attainment, Borel-versus-arbitrary-policy existence, полигональная редукция, measurable selection и off-domain extension. Equality epigraph sets не подменена `sInf` пустого множества. Словарь legacy A=I/sign/L1 не изменён и не используется как исходная математическая модель.

## Следующий допустимый шаг

Сначала устранить конфликт setup authority с native retries официального pinned helper либо согласовать другой поддержанный путь с сохранением проверки целостности; затем подготовить полную dependency closure, получить успешный `lake build BridgeFormal` и провести S2. До этого S3 запускать нельзя. Рекомендуемая build-команда после разрешения и завершения setup: из `bridge/formal-v1/lean`, с абсолютными task-local TMPDIR/MATHLIB_CACHE_DIR/XDG_CACHE_HOME, `timeout 300 lake build BridgeFormal`. В S1 она NOT RUN, чтобы Lake не инициировал неразрешённое получение зависимостей. Будущие proof modules должны отдельно попасть в точный build inventory; сборка нынешних definitions proof не проверяет.

Новые записи ограничены `bridge/formal-v1/` и `artifacts/bridge/formal-v1/setup/`; legacy scientific/source/results, correction и исходные receipts не редактировались. Beads просмотрен, но не изменён из-за разрешённого write scope. Нет nested agents/workflows, глобальных установок, commit/push, comparator bypass, private benchmark или scientific attestation. Фактические расходы провайдера, native retries внутри сторонних процессов и полное OS containment неизвестны. Независимое semantic review и человеческая научная власть остаются отдельными от будущей проверки ядром Lean.
