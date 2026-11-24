# ОГУ → ARO: независимый аудит formal-v1, S4

**Статус: blocked. Общее kernel-checked доказательство отсутствует.** Повторные вызовы Lean для Model, Goals и печати ожидаемых теорем завершились exit 1 до elaboration — разбора определений и проверки типов. S3 не запускался; `readyForProof=false`. Ни один из узлов F1–F4 не закрыт.

Проверены 21 identity из candidate seal; расхождений нет. Среди 162 файлов ограниченного read-only снимка изменений нет. Эти результаты устанавливают идентичность проверенных файлов, а не истинность утверждений. C1–C6 не выполнены из-за отсутствующих imports; ложная цель не была отклонена по математической причине. Дополнительно завершился ошибкой XML-разбор PDF-координат; исходная выгрузка и ошибка сохранены.

Предыдущее принятие завершения остаётся отозванным в `artifacts/bridge/transfer-v1/coordinator/acceptance-correction.json`. Историческая квитанция не удалена; проверки четырёх конкретных инстансов сохраняют только прежнее ограниченное покрытие. Этот отчёт не восстанавливает принятие и не меняет научные статусы.

## 1. Предмет и границы аудита

Рабочий корень: `<workspace>/aro-discovery-campaign`; ветка: `task/aro-discovery-k4t-campaign`. Проверены перед первой записью и внутри сборщика свидетельств. Задание: `aro-discovery-k4t`, этап S4 спецификации `docs/specs/2026-11-13-ogu-aro-formal-repair-v1.md`, прочитанной полностью.

Новые файлы находятся только в `artifacts/bridge/formal-v1/final-review/` и в настоящем отчёте. Definitions, statements, legacy checkers/results и свидетельства S1/S2 не правились. Зависимости не устанавливались; cache helper, Lake resolver, comparator, legacy proof project и старые instance-checkers не запускались. Подагенты, workflow и автоматический repair не запускались. Commit, push, журнал, blueprint, конфигурация и аттестация не затронуты.

Обычный bootstrap с live-командами и широкими гейтами проекта сознательно пропущен: дано ограниченное read-only задание без полномочия записывать вне выделенных путей. Обновления Beads не выполнялись. Новизна не является гейтом этого этапа.

## 2. Источник и точность постановки

Прочитаны исходные A4 физические pp2–6 через новую layout-выгрузку оригинального PDF и `bridge/transfer-v1/correspondence.md`, а также реальные Model и Goals. Источник:

- `corpus/our_papers/A4_Дмитрук_2022.pdf`, SHA256 `4f26e650ec6c86e7058e9a2228d8b12bd20fbcd1f8a4ba0c45a3cae8135ec420`;
- физическая p2, печатная p67, (1.1): стационарная рекурсия с произвольными вещественными матрицами, непрерывные control/noise boxes, терминальные двусторонние линейные ограничения;
- физическая p3, печатная p68, (1.2)–(1.3): все возмущения и знаковый линейный терминальный критерий;
- физическая p4, печатная p69, предположение 1: измерение текущего состояния и выбор следующего блока управления по этому измерению;
- физические pp5–6, печатные pp70–71: последовательная динамика, допустимость стратегии и значение `+∞` при невозможности продолжения.

`A4-p2-6.txt` прочитан полностью. `A4-p2-6-bbox.html` сохранён; прямое чтение строк 495–559 показывает координаты непрерывных control/noise boxes. Попытка разобрать весь bbox как XML завершилась `ParseError` на строке 3779, колонке 88. Повтор, очистка XML или замена парсера не выполнялись; `source-anchors.json` не создан. Это дополнительный технический провал извлечения координат, не математический отрицательный контроль. Ошибка записана отдельно в `source-coordinate-parse-failure.json`.

В `docs/GLOSSARY.md`, §2, по-прежнему имеется узкое legacy-описание с `A=I`, дискретными знаками и L1-критерием, атрибутированное A4. Оно не используется как основание данного формального target и не исправлялось вне скоупа. Модель formal-v1 сохраняет фактическую исходную постановку; это наблюдение о тексте, не результат Lean.

### Допущения зафиксированного F1/F2 target

`bridge/formal-v1/lean/BridgeFormal/Model.lean` содержит:

- `Vec n = Fin n → ℝ`; положительные `n,m,p,r,q`; произвольные вещественные линейные отображения `A,B,E,H,c`, начальное состояние `x0`;
- упорядоченные конечные границы управления и `rho>0`; независимость временных блоков означает полный Cartesian product допустимых непрерывных возмущений, не вероятностную независимость;
- `step` и рекурсивный `run`, затем реальные `prefix`, `nominal`, `deviation`; искомая формула `expansion` определена отдельно, её равенство рекурсии не предположено;
- `S(a)` как образ реальной prefix-рекурсии и `Z` как образ zero-control/zero-initial отклика; равенство сдвинутых образов остаётся отдельной целью;
- один `StatePolicy` на достижимом состоянии либо один `DeviationPolicy` на отклонении; результат правила — весь ограниченный suffix block. Будущий блок не является аргументом правила;
- `Rows`: обе стороны каждой терминальной строки и `D.c x ≤ eta`, где `eta : ℝ`; нет замены знакового критерия абсолютной величиной, ENNReal или неоговорённым `sInf` пустого множества;
- возможную терминальную несовместимость; ни feasibility, ни желаемая correspondence, ни selection, ни terminal decomposition не добавлены полями `Data`.

Обе policy-структуры требуют `Measurable rule` на достижимом subtype. На прочитанных страницах A4 Borel-регулярность явно не заявлена. Это ограничение класса formal-v1, а не установленное свойство всех исходных стратегий. Соответствие Borel-свидетелей ещё не доказывает существование равноценного Borel-правила для произвольной исходной стратегии; соответствующая конструкция остаётся в F4. Обобщение на недостижимые состояния и extended-value/attainment corollaries не формализованы.

Текст не заменяет исходный объект рациональной конечной игрушкой и не содержит обнаруженного предположения искомой теоремы. Однако ни inhabitation `Data`, ни синтез measurable instances, ни правильность типов не подтверждены компилятором. Эти структурные замечания LLM не являются математическим вердиктом или разрешением начать S3.

## 3. Реальные identities и окружение

`identities.json` содержит ожидаемые и заново вычисленные SHA256 для десяти локальных sealed файлов, восьми pinned upstream файлов, двух исполняемых файлов Lean/Lake и source-import inventory: всего 21 совпадение. Ключевые identities:

| Объект | SHA256 / revision |
|---|---|
| Model.lean | `188a55848460b83105cf2eccd8633fc08a2e8f393bbaebb1e26ed05329073323` |
| Goals.lean | `ef3a0cbd1bd40b39403675544cce325dc683dd85b93b5b52030a4aa3ba7e7957` |
| expected-theorems.json | `addd28b9e7075a174544803330a7bc4042bd97171d372b0fff50761ab230717e` |
| Mathlib HEAD | `c58b47adb340faa641e363aef2a460dc534bf172` |
| Lean binary | `bf8d54e4714cc4b03d3f6bb34c83b7202b87e49c8bfcbff6895c085bb90ceb38` |
| Lake binary | `8ba83c98f76562d03b8dbc33f1057151ba6cbb121679dde76b2260ccc90495e1` |

Наблюдаемые версии: Lean `4.35.0-rc2`, commit `11acb17ec6b07a8f9e9173e6845197929540936b`; Lake `5.0.0-src+11acb17`. Tracked porcelain Mathlib пуст. Восемь остальных manifest dependency directories отсутствуют. Отсутствие compiled imports непосредственно подтверждено Lean. Полной compiler-resolved import closure нет; lexical inventory и candidate seal её не заменяют.

Pinned `Cache/Requests.lean:351–352` содержит `curl --retry 5` независимо от `supportLegacyCurl`; `Cache/Cli.lean:22–26` перечисляет опции без retry-disable. Это подтверждает причину остановки выбранного в S1 официального cache-маршрута при запрете автоматических повторов. Это не доказательство невозможности всех официальных путей provisioning. S4 не имеет полномочий искать обход или менять setup.

## 4. Что именно запускалось

Сборщик:

```text
timeout 150 python3 -B artifacts/bridge/formal-v1/final-review/audit.py
```

Его exit 0 означает завершение сбора свидетельств. Математический результат сборщика — `blocked`, не PASS. Скрипт прочитан как часть настоящего аудита; положительные поля авторских S1/S2 отчётов не используются вместо вызовов компилятора.

Диагностика технического стиля `python3 -B .../lint_technical_style.py reports/briefings/2026-11-13-ogu-aro-formal-v1.md --language ru --extended` завершилась exit 1 с шестью advisory-замечаниями. Все шесть рассмотрены: они относятся к ограничениям информации, запрету подмены доказательства и явным границам проверки; формулировки сохранены. `style.stdout`, `style.stderr`, `style.exit` удерживают этот результат. Стиль не служит математическим гейтом.

Из `bridge/formal-v1/lean` запускался абсолютный pinned binary Lean. Полные argv, cwd, ограничения времени, environment overrides и сырые stdout/stderr/exit сохранены в `typechecks.json`, `environment.json`, отдельных `*-typecheck.*` и `theorem-print.*`. Каждый compiler subprocess ограничен 45 секундами; `TMPDIR`, cache и выходные `.olean` направлены в final-review.

| Фактическая цель | Команда, сокращён только префикс final-review | Exit | Наблюдение |
|---|---|---:|---|
| реальные definitions | `lean -o <review>/compiled/BridgeFormal/Model.olean BridgeFormal/Model.lean` | 1 | `Model.lean:1:0`: отсутствует `Mathlib.MeasureTheory.Constructions.BorelSpace.Basic.olean` |
| реальные proposition definitions | `lean -o <review>/compiled/BridgeFormal/Goals.olean BridgeFormal/Goals.lean` | 1 | `Goals.lean:1:0`: отсутствует `BridgeFormal.Model.olean` |
| печать точных ожидаемых targets и axioms | `lean <review>/InventoryAudit.lean` | 1 | строка 1: отсутствует `BridgeFormal.Goals.olean`; до `#print` выполнение не дошло |

`InventoryAudit.lean` запрашивает `#print` и `#print axioms` именно для всех десяти ожидаемых proof declarations. Файлов в `BridgeFormal/Proofs/` и самих target proof declarations нет. Поэтому компиляция exact target proofs — **not run: отсутствует входной proof package**; ни Model/Goals, ни файл запросов печати не выданы за proof compilation. `lake build` не запускался: нет proof targets, imports заблокированы, а resolver может начать неразрешённое для S4 provisioning. Другая библиотека и legacy `Aroform.lean` не использовались как замена.

### Axiom allowlist

Допустимы только `propext`, `Classical.choice`, `Quot.sound`. Allowlist прочитан из реального expected inventory и сопоставлен с этими тремя именами. Parsed transitive axiom records: **0**, напечатанных theorem types: **0**. В `axiom-audit.json` стоит `allowlistGateSatisfied=false`; у каждой цели `axioms=null`, не `[]`.

Пустой вывод после import failure не означает «нет запрещённых аксиом». Не подтверждено отсутствие `sorryAx` или иных аксиом в несуществующем доказательстве. Legacy sorry-only scan не применялся. Без реального proof inventory, успешной компиляции и полного вывода `#print axioms` гейт не пройден.

## 5. Proof → claim → assumptions → evidence

В таблице `M` означает `bridge/formal-v1/lean/BridgeFormal/Model.lean`, `G` — `bridge/formal-v1/lean/BridgeFormal/Goals.lean`. Имена propositions имеют префикс `BridgeFormal.`, ожидаемые proof names — `BridgeFormal.Proofs.`. Все G-декларации — **`def ... : Prop`, не теоремы**.

`coverage.json` содержит точные текстовые тела всех десяти propositions, тело `Preserves`, общие допущения и source anchors. `Model-numbered.txt` и `Goals-numbered.txt` сохраняют полный локальный текст со строками; identities выше фиксируют его. Эти тела не названы printed theorem types.

Для каждой строки F1/F2/prerequisite общий наблюдаемый результат: Model/Goals imports exit 1, proof declaration отсутствует, printed type и axioms отсутствуют; C1–C6 not run. Это единая колонка свидетельств, а не десять разных успешных проверок.

| Узел | Source / локальное определение | Точная proposition, строка G | Ожидаемое доказательство — фактически отсутствует | Незакрытая обязанность |
|---|---|---|---|---|
| prerequisite | A4 p2; `ControlBlock`, `NoiseBlock` | `NonemptyBlocksGoal`, G:39 | `nonempty_blocks` | Непустота блоков и compiled admissible witness |
| F1 | A4 (1.1); `run`, `expansion` | `ExpansionGoal`, G:8 | `expansion` | Вывести конечную формулу из рекурсии для всех `k,x,u,w` |
| F1 | A4 (1.1); `prefix`, `nominal`, `deviation` | `PrefixSplitGoal`, G:13 | `prefix_split` | Реальное prefix-состояние равно nominal плюс deviation |
| F1 | A4 pp4–5; `sourceTrajectory`, chronological controls/noise | `SourceChronologyGoal`, G:17 | `source_chronology` | Начальная точка и все шаги, включая границу `t=r` |
| F1 | A4 pp2–5; `sourceTrajectory`, `expansion` | `SuffixExpansionGoal`, G:27 | `suffix_expansion` | Терминальная suffix-формула из реальной динамики, с initial offset |
| F2 | A4 p4; `S(a)`, `Z` | `ExogenousImageGoal`, G:35 | `exogenous_image` | Равенство фактического сдвинутого образа и exogenous Z в обе стороны |
| F2 | A4 предположение 1; `StatePolicy`, `sourceSuffix` | `ObservationFibreGoal`, G:62 | `observation_fibre` | Одинаковое измерение даёт один и тот же весь suffix |
| F2 | A4 pp4–5; `StatePolicy`, `DeviationPolicy`, `Related` | `ForwardPolicyGoal`, G:50, `Preserves` G:42 | `forward_policy` | Measurable forward witness, те же controls/траектории и все знаковые bounds |
| F2 | Те же источник и definitions | `ReversePolicyGoal`, G:54, `Preserves` G:42 | `reverse_policy` | Measurable reverse witness с теми же preservation-условиями |
| F2 | A4 (1.2)–(1.3); `SourceBound`, `AROBound`, levels | `EpigraphEqualityGoal`, G:58 | `epigraph_equality` | Равенство допустимых real epigraph-level sets, включая пустые |
| F3 | A4 p3, support tightening; независимый будущий box | **нет proposition** | **нет proof** | Универсальная support-equivalence для знакового cost и обеих терминальных сторон; whole-block timing |
| F4 | Transfer dictionary §4, письменная реконструкция | **нет proposition** | **нет proof** | Exact fixed-recourse vertex reduction и Borel-правило на всех достижимых real states; relative dimension и вырожденные образы |

F3/F4: compiler/axioms/узловые controls — not run, поскольку нет даже statements. Для F4 дополнительно требуется различать existence-equivalence по terminal image и биекцию произвольных state policies: это разные утверждения. Формальная factorization lemma не закрыла бы всю таблицу даже при успешной проверке.

Предполагаемый путь доказательства F1 — индукция по `run`, затем prefix/suffix и chronology. F2 требует реальных measurable translations между `Z` и `S(a)`, обеих сторон preservation и равенства epigraph sets. Это перечень недостающих доказательств, а не предоставленные доказательства или гипотезы `Data`.

## 6. Семантические контроли: фактический результат каждого

`controls-predeclared.json` записан **до compiler replay** из sealed `statement-map.md`; SHA256 исходного control inventory сохранён. Новые определения игрушечной модели или отдельный Python simulator не создавались.

| Контроль | Предзаданный смысл на реальных definitions | Отдельное свидетельство | Фактический результат |
|---|---|---|---|
| C1 | Двумерные данные, положительные r=q=1, ненулевое disturbance; a=b=1; допустимая отрицательная граница eta=−2 | `C1-result.json` | not run: imports отсутствуют; compiled Data/witness нет |
| C2 | Непустые controls/noise, терминальная вторая координата `[5,5]`; нулевое disturbance опровергает достижимость | `C2-result.json` | not run; пустота sourceLevels не доказана |
| C3 | Prefix paths `(1,−1)` и `(−1,1)` дают одно измерение; один suffix при изменении будущего | `C3-result.json` | not run; только текстовое наблюдение об аргументах rule |
| C4 | Cost −2 допускает eta=−2, но не −3; смена c на +x0 меняет результат | `C4-result.json` | not run; знаковая полярность не проверена Lean |
| C5 | Ложный `SourceBound (-3)` должен быть отвергнут из-за zero-noise contradiction | `C5-result.json` | not run; invalid fixture не предъявлялся и не был отвергнут |
| C6 | Один state rule не может выбирать противоположные suffix controls по ненаблюдаемому будущему | `C6-result.json` | not run; нет compiler-rejected future-dependent fixture |

Во всех шести файлах `negativeControlCredit=false`, математический результат отсутствует. Тип `rule` по исходному тексту не принимает будущее, но type-level exclusion ещё не подтверждён elaboration и не заменяет реально отвергнутый invalid fixture. Import failure C5/C6 не засчитывался как требуемый rejection. Это существенная невыполненная часть приёмки, а не зелёный результат контролей.

Спецификация S4 предписывает при blocked setup/statements аудит блокера и отсутствия proof вместо запуска S3. Именно эта ветка выполнена; фиктивные Lean-файлы с одним import не выдавались за исполнение семантических сценариев.

## 7. Что осталось и рекомендация владельцу

1. **Setup:** получить точные pinned dependencies и compiled imports разрешённым способом без автоматических повторов; существующая проверка одного cache helper не исключает все официальные маршруты. Здесь provisioning не предпринимался.
2. **Statements:** успешно elaborать Model/Goals, построить compiler-resolved dependency closure и вернуть пакет на независимое S2. Любая смена statement требует новой identity и нового ревью.
3. **F1/F2:** предоставить реальные proof files на sealed definitions; собрать именно их, получить printed closed theorem types и transitive axiom inventory по каждой target declaration.
4. **F3/F4:** отдельно зафиксировать и проверить недостающие statements/proofs; не менять смысл узлов ради доступной леммы. Borel/source distinction и terminal/state-image distinction остаются явными.
5. **Controls:** выполнить все C1–C6 на reviewed definitions, включая настоящие отрицательные fixtures с заявленной причиной rejection; после этого повторить независимый финальный аудит по отдельному решению.

**Рекомендация: сохранить `blocked` и не восстанавливать completion acceptance.** Причина — отсутствие proof package и неработающие imports, а не оценка научной новизны или критика другой LLM. Автоматическая доработка и новое принятие этим отчётом не разрешаются.

Не проверено: general proof, compiled theorem types, transitive axioms, nonvacuity/semantic controls, F3/F4, эквивалентность всех исходных стратегий Borel-классу, extended values/attainment и полный compiler import closure. Они отсутствуют либо недоступны при текущем setup. Actual billing и native retries сторонних процессов неизвестны; полного OS containment или исчерпывающего аудита файловой системы не заявлено.

Kernel-проверка будущего доказательства уменьшит риск ошибки вывода относительно проверенных определений. Соответствие этих определений исходнику и применимость к научному утверждению всё равно требуют отдельного рассмотрения и человеческой научной власти. Универсальная безошибочность не заявляется.
