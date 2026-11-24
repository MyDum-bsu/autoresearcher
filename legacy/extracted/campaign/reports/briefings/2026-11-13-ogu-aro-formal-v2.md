# ОГУ → ARO: независимый финальный replay formal-v2

C2 не завершён: новый контрольный файл не скомпилирован из-за неверного имени вспомогательной Lean-леммы. F3, F4 и сравнение Borel-политик с unrestricted source policies остаются недоказанными. Весь перенос не принят; научные статусы не изменялись.

Все десять точных prerequisite/F1/F2 targets независимо скомпилированы из неизменённых исходников. Фактические типы совпали с frozen inventory; для каждого получен непустой вывод транзитивных аксиом, содержащий только `propext`, `Classical.choice`, `Quot.sound`. C1/C3/C4 и положительная часть C6 скомпилированы; ложные C5/C6 отклонены по заявленным причинам после успешных импортов.

## Что именно проверено

Рабочий feature-worktree: `<workspace>/aro-discovery-campaign`, ветка `task/aro-discovery-k4t-campaign`. Активная среда — `bridge/formal-env-v2/lean`; failed formal-v1 не запускался. Проверены `FOUNDATION.md`, `AGENTS.md`, полный continuation spec и parent formal-repair spec, процедуры worker/session/Beads, литературы/оракула, логического и технического редактирования. Epic `aro-discovery-k4t` прочитан; его статус не менялся.

Команда независимого replay:

```sh
timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/replay.py replay
```

Наблюдение: exit 0. Свежая отдельная компиляция `Model`, `Goals`, `Proofs/Dynamics`, `Proofs/Policies`, `Proofs/Inventory` — пять exit 0. Использован прямой `lean -o` в task-local evidence build, а не старые proof `.olean` и не сборка одной библиотеки определений. `lake env printenv LEAN_PATH` также завершился с exit 0; зависимости не обновлялись и не скачивались.

Точные команды, окружение, длительности и минимальное свободное место записаны в `artifacts/bridge/formal-v2/final-review/replay-*.json`. Полные типы, определения goal predicates и `#print axioms` находятся в `replay-inventory.stdout:3319–3371`; машинный разбор — `theorem-audit.json`. Пустой inventory, отсутствующий/пустой axiom output, несовпадение типа и неизвестные аксиомы останавливают этот gate.

До компиляции сверены 13286 уникальных file identities из seals, source/config/proof/build файлов, tool binaries и обеих замороженных import closures. Statement closure содержит 3316 модулей, proof closure — 3318. Свежий compiler-reported import closure содержит те же 3318 имён; новые Model/Goals/Proofs загружены из отдельного replay build. Source и доступные `.olean`/`.private`/`.server` hashes записаны в `actual-import-closure.json`. Это не повторная сборка всех зависимостей и не доказательство воспроизводимости dependency binaries из исходников.

Seal кандидата: `artifacts/bridge/formal-env-v2/candidate-seal-v2.json`, SHA256 `fac539e502bd70340f885c9cbbe777065744cd4fd7c4dc0d438ff253d548215c`. Model SHA256 `44d474e393f0d83dc215877aa9663fbf79c3c9887ed838305cb74048699e6a26`; Goals SHA256 `b3b949e681935df3491602dec2d0daf73ab15b711481b014b6e2a5abb61d2409`; expected inventory SHA256 `d62c8eb1d54f30f2e5533771b91ddaa1dfa816dc48b842899de7412e47bf2fe4`. Проверены также reviewed-target identity и отдельный proof seal; их исторические поля `unproved`/`proofsPresent=false` не переписывались и не использовались как итоговый результат.

## Теоремы и границы утверждений

Общие условия `BridgeFormalV2.Data` (`Model.lean:19–42`): положительные n,m,p,r,q; конечномерные вещественные пространства; произвольные стационарные линейные A/B/E/H/c; упорядоченные componentwise control bounds; rho>0; все независимые prefix/future disturbance blocks. Ограничений ранга и достижимости terminal target нет. `Rows` сохраняет обе стороны terminal bounds и signed cost `c x ≤ eta`. Обе policy classes требуют Borel measurability на реальных reachable subtypes. Никакое равенство переноса не включено в Data как предпосылка.

В таблице namespace целей — `BridgeFormalV2`, доказательств — `BridgeFormalV2.Proofs`. Каждая строка имеет compiler exit 0 и ровно допустимые аксиомы `{propext, Classical.choice, Quot.sound}`.

| Узел | Точная цель → proof declaration | Связь с заявлением / зависимости | Controls и оставшаяся граница |
|---|---|---|---|
| prerequisite | `NonemptyBlocksGoal` → `nonempty_blocks`, `Dynamics.lean:9` | Непустые bounded controls и real noise для любого k; свидетели umin и нулевой noise | C1 содержит полный конкретный Data и admissible witnesses; C2 не завершён |
| F1 | `ExpansionGoal` → `expansion`, `Dynamics.lean:63` | Конечная линейная формула выведена из `run`, через индукцию `run_formula`, не предположена | C1 проверяет actual trajectory на положительном горизонте и ненулевом E |
| F1 | `PrefixSplitGoal` → `prefix_split`, `Dynamics.lean:26` | Actual prefix state = nominal + disturbance response; `run_add` | C1/C3 используют continuous disturbances и неинъективный observation image |
| F1 | `SourceChronologyGoal` → `source_chronology`, `Dynamics.lean:72` | Начальное состояние и каждый шаг до r+q, включая границу t=r | C1 actual recurrence; общая теорема не ограничена тестовым A=I |
| F1 | `SuffixExpansionGoal` → `suffix_expansion`, `Dynamics.lean:91` | Actual terminal state = suffix expansion после prefix split; использует q>0 | C1/C4 сохраняют все terminal rows и signed cost |
| F2 | `ExogenousImageGoal` → `exogenous_image`, `Dynamics.lean:97` | Равенство реального range(prefix−nominal) и Z для любого a | Не только отсутствие a в обозначении Z |
| F2 | `ObservationFibreGoal` → `observation_fibre`, `Dynamics.lean:106` | Равные actual observed states дают один suffix block для произвольной state policy | C3 и C6; future не является аргументом policy |
| F2 | `ForwardPolicyGoal` → `forward_policy`, `Policies.lean:54` | Для любой Borel state rule строится Borel deviation rule; `toState_measurable` и `preserves_of_related` | Сохраняются controls, trajectories и все signed epigraph bounds одним witness |
| F2 | `ReversePolicyGoal` → `reverse_policy`, `Policies.lean:72` | Обратный Borel witness через `toDeviation_measurable` | Те же компоненты `Preserves`; не unrestricted source-policy correspondence |
| F2 | `EpigraphEqualityGoal` → `epigraph_equality`, `Policies.lean:89` | `sourceLevels = aroLevels` по двум witness maps | Множества реальных bounds; не утверждение attainment или extended-real infimum |
| F3 | Нет sealed proposition/proof | Universal support equivalence для независимого future box, signed cost и обеих terminal directions | Не закрывается вычислением supports на отдельных примерах |
| F4 | Нет sealed proposition/proof | Точная finite fixed-recourse reduction и measurable real-state selection, включая relative dimension/degenerate images | Не доказано, не включено как гипотеза |
| unrestricted source comparison | Нет proof declaration | Равенство achievable levels Borel-class и unrestricted source strategies | Отдельное selection/comparison обязательство; не исчезает из-за F2 |

`Preserves` (`Goals.lean:43–49`) включает Related в обе стороны, равенство фактических suffix controls, траекторий для всех t≤r+q и SourceBound↔AROBound для каждого real eta. Трансляции меняют только известный nominal offset; future noise не передаётся rule. Реальное доказательство F2 относится к двум явно выбранным Borel-классам. Source fidelity на A4 physical pp2–6 была предметом отдельного statement review; kernel сам не подтверждает интерпретацию PDF. Историческое расхождение glossary с общим source-native A/continuous noise не исправлялось и не использовалось как основание теоремы.

## C1–C6: фактические исходы

Команда:

```sh
timeout 300 python3 -B artifacts/bridge/formal-v2/final-review/make_controls.py
```

Этот driver сохраняет отдельный exit каждого Lean-вызова. Его собственный exit 0 означает завершение записи результатов, а не прохождение всех controls. Фактические исходы находятся в `controls-execution.json`; критерии были записаны в `controls-plan.json` до компиляции контрольных модулей.

Общий `ControlFixture.lean` elaborated с exit 0. Он задаёт ровно C1: n=2,m=1,p=2,r=q=1, A=I, B(u)=(u,0), E(w)=(0,w0+w1), U=[−1,1], rho=1, terminal [−4,4]^2, c(x)=−x0. Все control/noise membership и measurable constant-rule поля заполнены Lean-доказательствами. Область disturbance остаётся непрерывной; проверка robust bound универсальна по её элементам.

| Control | Файл / exit | Наблюдение |
|---|---|---|
| C1 | `C1.lean`, 0 | SourceBound(−2), соответствующий constant-rule AROBound(−2), actual terminal coordinate formula; отрицательный достижимый cost level |
| C2 | `C2.lean`, 1 | Ошибка `Unknown constant Set.eq_empty_iff_forall_not_mem.mpr` в строке 8. Пустота sourceLevels для terminal coordinate [5,5] не проверена. Это ошибка вспомогательного теста, не ожидаемая mathematical rejection и не контрпример модели |
| C3 | `C3.lean`, 0 | Prefix (1,−1) и (−1,1) имеют один observed state; произвольная StatePolicy выбирает один suffix; future +1/−1 не даёт другого выбора |
| C4 | `C4.lean`, 0 | Rows(−2) для всех terminal states witness; Rows(−3) опровергнут при нулевом noise; замена c на +x0 нарушает bound −2 |
| C5 | `C5.lean`, 1, ожидаемый reject | После успешного импорта `c4Reject` Lean отверг использование SourceBound(−2) как SourceBound(−3), `control-c5.stdout:2–7`. Положительная zero-noise contradiction находится в C4; import failure не засчитывался |
| C6 positive | `C6.lean`, 0 | Доказана невозможность одного StatePolicy, требующего +1/−1 control по двум различным future noises при одном prefix observation |
| C6 negative | `C6Negative.lean`, 1, ожидаемый reject | После импорта `c6Impossible` ложная constant-policy конструкция остановлена на несовместимом equality с `minus`, `control-c6negative.stdout:2–12` |

До этих контролей первый новый `ControlData.lean` завершился с exit 1: dependent numeral/typeclass и раскрытие concrete Data в тестовом fixture. Исходный файл и полный output сохранены. Новый fixture делает только его конкретные Data-константы прозрачными и сравнивает `i.val`; sealed Model/Goals и proofs не менялись. Никакая его ошибка не засчитана как intentional rejection. C2 после наблюдаемой ошибки не исправлялся и повторно не запускался. Отсутствующих импортов в фактических C1–C6 запусках не было.

## Что не выполнено и почему

Полный положительный контроль C2 не завершён из-за описанной ошибки тестового API. Нет дополнительной repair-итерации, новой научной теоремы или изменения reviewed proof inventory. F3/F4 и unrestricted-source comparison не входили в этот replay и остаются отдельными пробелами. Comparator не запускался и его isolation failure не обходился; эти standalone compiler/hash/axiom проверки имеют более узкую силу.

Не выполнены downloads, dependency rebuild, global install, hidden network retry/fallback, nested agents/workflows, pi-goal objective, commit/push, journal/blueprint/corpus/glossary/config edits, attestation или live `formalized` transition. Task-local TMPDIR/TMP/TEMP и XDG/Mathlib/Lake cache directories заданы явно, Python запускался с `-B`, `MATHLIB_NO_CACHE_ON_UPDATE=1`; каждый compiler process ограничен timeout и 600 MiB disk watchdog. Actual billing, provider-native retries и полная OS containment неизвестны.

Рекомендация: использовать этот пакет как независимо проверенное покрытие десяти sealed F1/F2/prerequisite targets с незавершённым C2, не как принятие всего переноса. Последующие C2/F3/F4/source-policy работы требуют отдельного явно ограниченного поручения; этот worker их не запускал.
