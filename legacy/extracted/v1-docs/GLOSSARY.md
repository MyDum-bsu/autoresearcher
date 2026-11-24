# Глоссарий и обозначения — aro-discovery

> Компонент системы (не разовый документ): принятая терминология и
> обозначения для всех этапов — журнал, blueprint, карточки, отчёты,
> сессии. Живёт по правилу: новый термин входит через сессию (сначала
> определение здесь, потом употребление); при расхождении словоупотребления
> с глоссарием правится либо текст, либо глоссарий — «на глаз» нельзя.
> Язык: EN-канон в пайплайне (код, журнал, узлы), RU-эквиваленты здесь —
> для сессий и диссертации. Основание: policy_updated seq 902 (EN),
> plan_approved seq 1236, решения владельца 2026-09-24/25.

## Pilot vocabulary (English)

Use the English terms below in the pilot. The Russian column is an editorial proposal for the owner's reports and thesis. The owner approves the final Russian wording. Original source quotations retain their language.

| Term ID | Canonical English | Definition | Russian editorial candidate |
|---|---|---|---|
| `adjustable_robust_optimization` | adjustable robust optimization (ARO) | Robust optimization with decisions that can depend on observations available at their stage. | адаптивная робастная оптимизация |
| `recourse_decision` | recourse decision | Decision selected after the observation available at a later stage. In a two-stage model it is the second-stage decision. | решение второго этапа |
| `fixed_recourse` | fixed recourse | The recourse coefficient matrix is independent of the uncertain parameters. | фиксированная матрица второго этапа |
| `affine_decision_rule` | affine decision rule (ADR) | A decision rule affine in an explicitly named observable quantity. | аффинное правило принятия решений |
| `optimal_guaranteed_control` | optimal guaranteed control | The problem of optimizing a worst-case control criterion under the prescribed information and constraints. | оптимальное гарантированное управление |
| `guaranteeing_program` | guaranteeing control program | Open-loop sequence selected before the disturbances and required to satisfy the constraints for all admissible realizations. | гарантирующая программа управления |
| `closing_instant` | closing instant | Scheduled instant at which a measurement is made available before recomputing the program for the next block. The source problem specifies what is measured. | момент замыкания |
| `closure_schedule` | closure schedule | Ordered set of closing instants. In the finite discrete model the instants lie strictly between the start and terminal times. | расписание замыканий |
| `measurement_history` | measurement history | Measurements available when a control decision is made. | история измерений |
| `disturbance_prefix` | disturbance prefix | Realized sequence of disturbances up to the stated instant. | префикс реализаций возмущений |
| `nonanticipativity` | nonanticipativity | A decision agrees across scenarios indistinguishable at its decision instant under the prescribed observations. | неупреждаемость |
| `guaranteed_value` | guaranteed value | Best worst-case criterion over feasible policies in the specified information class. Minimize the worst cost or maximize the least reward according to the declared polarity. | оптимальное гарантированное значение критерия |
| `value_of_measurement` | value of measurement | Decrease in optimal guaranteed cost due to a specified measurement on the same instance. | выигрыш от измерения |
| `scope` | claim scope | Assumptions, quantifiers, admissible inputs and conclusion that determine what a claim asserts. | область применимости утверждения |
| `evidence_bundle` | evidence bundle | Versioned collection of source anchors, check results and witnesses bound to a claim or research question. | пакет свидетельств |
| `research_disposition` | research disposition | Owner's decision about the role of a claim in the active research program. | решение о роли результата в работе |
| `episode` | research episode | Work on a sealed question under a declared budget and acceptance contract, possibly across attempts. | исследовательский эпизод |
| `lease` | work lease | Time-bounded authority to submit work for one attempt. | временное право на сдачу результата |
| `stigmergy` | stigmergy | Coordination through durable changes in a shared environment that guide later work. | стигмергия |
| `publication` | internal publication | Committing checked evidence to the research journal. | фиксация результата в журнале |
| `holdout` | holdout episode | Acceptance episode whose specific input and expected evidence remain inaccessible to the worker. | закрытый сценарий приёмки |

In the discrete pilot use `V(R)` for a **fixed** closure schedule, `V_full` for full feedback, and `V_open` for the open-loop optimum. State the minimization convention and the ordering `V_full ≤ V(R) ≤ V_open`. Reserve **dynamic programming** for a solution method. An **exact value** refers to the stated model and arithmetic. **Survived a finite test** states the extent of numerical evidence. **Machine-checked proof** identifies the formal statement and kernel.

For RU prose, prefer «измерение состояния» or «измерение выхода» where applicable. Avoid «наблюдение возмущений» for either unless the model supplies them. Use «оптимизация расписания» only when the closing instants are decision variables. Bind every technical term in a question specification to a term ID. A changed definition is versioned. The Russian editor checks the statement's object, hypotheses, polarity and quantifiers against English before prose enters a chapter. [A2, PDF pp. 2–3](../corpus/our_papers/A2_Дмитрук_2018.pdf#page=2), [A4, PDF pp. 3–5](../corpus/our_papers/A4_Дмитрук_2022.pdf#page=3), [BGT 2004, PDF pp. 1–4](../corpus/02_BenTal_Goryashko_etal_2004.pdf#page=1).

## Earlier vocabulary and notation

The tables below record legacy conventions. Where terms conflict, use the pilot definitions for new work.

## 1. Модель и математика (сторона ARO)

| Термин | Определение |
|---|---|
| Двухэтапная ARO (fixed recourse) | min c·x + max_{ζ∈Z} φ(h(ζ) − T·x): решение первого этапа x, решение второго этапа y(ζ) после наблюдения ζ |
| Fixed recourse | Матрица второго этапа W не зависит от ζ. В данном классе ζ входит в правую часть h(ζ) = h0 + Hζ |
| Z / vertex list | Множество неопределённости как выпуклая оболочка конечного списка вершин (бюджетное/боксовое) |
| φ(r) | Задача второго этапа: min{q·y : W·y ≥ r, y ≥ 0} — точная рациональная величина |
| z* | Точный оптимум двухэтапной задачи (сертифицируется cutting-plane) |
| Compact reformulation | ARC как LP с блоком y_v на вершину (BGT-2004 Thm 2.2) — то, что считает `restricted_solution` |
| AARC / ldr-aarc | Аффинное решающее правило y(ζ) = Y0 + Y1·ζ одной ЛП (BGT Thm 3.3); restriction ⇒ стоимость ≥ z* |
| CAP_MULT / LP budget | Бюджет кандидата: ≤ CAP_MULT × LP-работы сертификатора на инстанс (aro2s,Frozen) |
| Гейт | `make check`: статика + mypy strict + PBT + байт-детерминизм + журнал + чекеры + Lean + алерты |
| Пантеон | Refuted-узлы с машинно проверяемыми контрпримерами; повтор ид = впустую-предложение |

## 2. Мост ОГУ ↔ ARO (сторона Дмитрук)

| Термин | Определение |
|---|---|
| ОГУ | Оптимальное гарантированное управление (школа Дмитрук, якоря A1–A5) |
| Мост-класс | Дискретная система x(t+1) = A·x + B·u + E·w, A = I, w ∈ {−1,+1}, коробочное u, терминальный критерий ‖x_T‖₁ — узкая модель проекта, которую сопоставляют с (1.1) из A4 |
| Замыкание / closure moment | Момент t, в который состояние точно измеряется и управление корректируется; между замыканиями — open loop по истории |
| R / closure set | Множество моментов замыкания; информационная структура стратегии |
| V(R) | Оптимальное гарантированное значение при R. При сравнении с A4 явно указать, доступны ли измерения или префикс возмущений. Старый `bridge.ladder_lp` использует общие координатные эпиграфы и может завышать значение |
| Лестница по информации | При минимизации V_full ≤ V(R) ≤ V_open. Исторические обозначения OC, RO(k), DP смешивали класс стратегий и метод решения |
| BT-1 / conj-ogu-aro-transfer | Мостовой тезис: соответствие V(R) ↔ ARO-гарантия, перенос теорем, E-alignment следствие (iii) |
| 2D-разложение | Целевая теорема: V(R) = max(V_scalar, |d0| + |Δe|·T); V_scalar — скалярная (нулевая настройка), V_diff — разностная компонента |
| E-alignment | Условие на амплитуды строк E: e1 = e2 (вырождается в скалярную) vs e1 = −e2 (лестница плоская в разностной части) |
| Поворот L1 | ‖x‖₁ пары = max(‖s‖, ‖d‖), s = x1+x2, d = x1−x2 (лемма `l1_eq_max_sum_diff`) — доказано |

## 3. Архитектура (хранилища, узлы, роли)

| Термин | Определение |
|---|---|
| Шесть хранилищ | events.jsonl (что ПРОИЗОШЛО) · научный граф/база (что ДОКАЗАНО + состояние цикла; поглощает blueprint, решение 2026-10-10) · reports/ (что ЗНАЧИЛО) · config/ + METRICS.md (что РАЗРЕШЕНО) · beads (что ОТКРЫТО) · decisions-легер (что ЖДЁТ владельца) |
| Журнал | events.jsonl, append-only с hash-цепочкой; писать только через `ro event` / aro.journal |
| Узел / blueprint | Элемент DAG: id, kind (question/conjecture/experiment/citation/theorem/example), status, deps, evidence (sha256), origin, autonomy |
| Семейство (family) | Организующая единица научного графа (образец openai/math, решение 2026-10-10): principal-результат + опровергнутые предшественники (видимы) + преемники + сопутствующие леммы. Родословная читается из графа, не восстанавливается из брифингов. Первые семейства — backfill h-auto-1…8; мутаторные узлы — служебное семейство-реестр; прочие run-узлы — архивный слой без удаления |
| Тезис (thesis statement) | Однострочная формулировка principal-результата семейства (стиль openai/math CONTENTS) — первоклассный узел графа; развёрнутые карточки, статусы и вердикты цепляются к нему. Письменный слой нового контура (решение 2026-10-10): эссе — архивный снапшот старого цикла, главы диссертации собираются владельцем из графа |
| Линейка статусов | seed → conjectured → survived-falsifier → numerical → dual-verified → formalized → attested; терминали refuted/descoped. Численные переходы — только код-судья; attested — только человек |
| Судья | Детерминированный код с вердиктом (aro2s, attack, hunt, bridge, toy, search.dsl); LLM к судейству не допускается никогда |
| Роли (актёры) | explorer/mutator (предлагает) · adversary (атакует) · judge (вердикт) · deriver (формализация) · archivist (литература) · scribe (текст) · orchestrator (такт) · evaluator (наблюдает) · human (власть) |
| Decisions-легер | decision_opened/answered/defaulted события; стол дефолтов (policy seq 1245): SLA 5 активных тактов, defaultable-решения применяются сами; сетки/пороги/статусы/устав — без дефолта |

## 4. Процессные термины

| Термин | Определение |
|---|---|
| Такт (вечерний, 19:30) | decisions --apply-defaults → мутатор → search → циклы → охота → гейт → коммит; при stall ≥ 7 — holiday-режим. **Заморожен 2026-10-10** (решение владельца, перестройка контура); определение будет переписано новой спецификацией |
| Holiday-режим | stall ≥ 7: такт строит досье рефлексии (reflection.py) и вопрос мутатору о расширении словаря; судьи и blueprint не трогаются (v2-holiday-tick, seq 1376) |
| Near-miss | Почти-выживший кандидат: известен инстанс и зазор, прошёл smoke; главная мишень прицельных мутаций (из enriched брифа) |
| Чемпион | Лучший passing-кандидат семейства по (total_lp, id) — вычисляется, не хранится |
| Citation-harvest | Кто цитирует якорные статьи (OpenAlex) — novelty-радар по графу цитирований |
| Proposal card | Карточка-предложение (статья/факт/интейк) — НЕ evidence; якорение и кодирование по политике оракула |
| Falsify-first | Атака ДО продвижения из conjectured и до формализации; promotion без зарегистрированной атаки запрещён |
| Autonomy H/C/A × 0-4 | Атрибуция вклада узла: H человеческий / A агент / C код; уровень — глубина человеческого вклада; код присваивает, человек корректирует при аттестации (seq 1377) |
| Процессные SKILL.md | Загружаемые компетенции агента (lit-review, oracle-encode, session-protocol, attestation) — план П2 (OpenResearch adoption) |
| Манифест формализаций (formalization manifest) | lean/formalization.yaml — носитель тройки «утверждение (blueprint-узел) ↔ Lean-декларация ↔ судья-артефакт» (решение 2026-10-10, spec T8); валидируется `ro manifest` в make check. Статусы записи: verified (в билде, с узлом, связка \lean{}) и proven-draft (sorry-free, вне gate-цели, перенос — bd gmd). Evidence-артефакт опционален: по ADR-0003 чистая Lean-теорема — истина сама по себе |
| Факт-блок (fact block) | Блок знания: утверждение + якорь (PDF-страница или строка TeX + дословная цитата + sha256) + класс задач, к которому применимо + ссылка на работу; сущность графа вида fact (литературная программа 2026-10-11, seq 6554). Вся рабочая продукция — на английском; русский — для готовых текстов диссертации |
| Теорема-блок (theorem block) | Блок знания: точная формулировка + профиль применимости (условия: fixed recourse, структура неопределённости и т.д.) + якорь + связь с формализацией (манифест-тройка, когда появится Lean); сущность графа вида theorem |
| Ландшафт (landscape) | Рёбра между работами (cites/extends/contradicts) и вопросы, висящие на пробелах; «связь теории, областей применимости, направлений поиска» — структура в графе, не текст |
| Портфель (portfolio) | Рабочий стол графа: проблемы и потенциальные результаты с полями problem / potential result / provability confidence (H/M/L + обязательное письменное обоснование агента — суждение оркестровки, НЕ научный вердикт) / refutability path / importance (владелец) / difficulty (история атак + оценка агента) / status / origin. Стоп-кран цикла берёт верхний незаблокированный элемент; утверждение ранжира — владелец пачкой. Существующие нити влиты первыми записями |
| Спека атаки (attack spec) | YAML в specs/attacks/: карточка + замороженные гриды + оракул + claims по import-путям; исполняет единый детерминированный раннер (`ro attack`, решение 2026-10-10). Артефакты байт-идентичны при повторных прогонах; триада exit-кодов: 0 survived-falsifier / 1 refuted / 2 crashed (сбой конвейера — никогда не вердикт, статус карточки не трогается). Без действующей карточки (`cards.card_ok`) спека отказывается работать. Старые одноразовые скрипты атак — замороженные свидетельства, миграции не подлежат |
| Карточка гипотезы (hypothesis card) | Обязательный пред-артефакт любой атаки: утверждение человеческим языком в docs/HYPOTHESES.md + словарь терминов + ожидаемый фальсификатор + происхождение (литература/предшественница); вердикты судей цепляются к id карточки. Не то же, что proposal card (литературное предложение). Пишет агент; ревью владельца пачкой; аттестация и попадание в paper — только после ревью (решение 2026-10-10) |
| Стоп-кран theory-first | Мягкий гейт режима (решение 2026-10-10): LLM-оркестратор сам решает, есть ли новый теоретический вход, и обязан записать решение с аргументацией в состояние цикла; вердикты при этом остаются только кодовыми |
| Очередь чтения (reading queue) | Первоклассный вход состояния цикла: работы/разделы, обязанные быть прочитанными и закодированными до атак; наполняют человек + агент в сессии, скан поставляет предложения. Механический гейт: очередь не пуста → атаки не запускаются. Периметр новизны (novelty-запросы) — конфиг-данные, не код (решение 2026-10-10). Статусы элемента очереди (рабочая лексика, не лестница науки): open → read → encoded; dismissed — отклонено человеком. Гейт держат статусы open/read (элемент ещё без разграничения); encoded/dismissed гейт открывают |
| Рабочий набор (working set) | Ответ состояния цикла на вопрос «с чем работает цикл N+1» (рендер `ro state`): открытые нити (open threads — выжившие гипотезы; опровергнутые остаются видимы внутри семей по дисциплине утверждений), чемпионы (производные от sweep-артефакта, не хранятся), очередь чтения с гейтом, стоп-кран-контекст, своды семей со ступенями |

## 5. Метрики

| Термин | Определение |
|---|---|
| Stall | Такты без научного движения (продвижение/опровержение); ≥ 7 — стоп автокоммитов (METRICS §2); считает ВСЕ завершённые циклы, включая гейт-микроциклы (известное загрязнение — bd обсуждение) |
| Decisive share | Доля циклов с научным движением |
| Weighted science yield (КПД) | Σ весов переходов (formalized/attested ×10, survived ×5, numerical ×2, refuted ×5, conjectured ×1) / judge-hours |
| Generator rank | component-tests → exploration: ранг exploration только при узлах от мутатора |
| Autonomy H/C/A | Сводка атрибуции по узлам (`ro metrics`) |

## 6. Литературный контур (v2-literature-pipeline, seq 1513)

| Стадия | Инструмент | Статус выхода |
|---|---|---|
| scout | lit_scan (OpenAlex + citation-harvest) + alphaXiv MCP discover_papers (семантика, интерактив) | карточки-предложения — НЕ evidence |
| intake | lit_intake.py: PDF → corpus/intake/ (карантин), sha256, digest | карточка с вопросами кодирования |
| propose | агент: карточки фактов с якорями (страница + дословная цитата); логическая проверка формулировок (skill logika) | факт-карточка |
| encode | агент: property/регрессия + цитат-узел с pdf_anchor; владелец выборочно ревьюит (d-oracle-encoding) | факт в гейте |
| gate | make check: расхождение с литературой = красный гейт | refuted-candidate (d-oracle-discrepancy) |
| reproduce | статьи с кодом: клон, воспроизведение, переиспользование (bd 9qv) | enrichment |

Якорь = файл + страница + дословная цитата + sha256 PDF. По памяти — никогда
(правило 1). OpenAlex/alphaXiv-запись — метаданные цитирования, не
математическая истина, пока нет pdf_anchor.

## 7. Правила словоупотребления (частые смешения)

- **survived-falsifier ≠ доказано**: «пережил атаку» — численное свидетельство, ограниченное покрытым пространством.
- **proposal ≠ evidence**: карточка/предложение становится истиной только после якоря + судьи.
- **refuted** — опровергнут конкретный кандидат (конструкция), не гипотеза целиком; гипотеза переживает и рожает следующую.
- **near-miss ≠ new**: почти-выживший известен (дедуп); новые предложения целятся в его окрестность.
- **z\* vs V(R)**: z* — сторона ARO (aro2s); V(R) — сторона ОГУ (bridge). Мост BT-1 связывает их структурно, не численно.
- **Такт vs сессия**: такт — автомат (контракт, holiday-ветка); сессия — человек+агент (может всё, что не запрещено).
- **judge_crash ≠ gate_failed**: упавший судья — проблема конвейера, не идеи.
- **Дисциплина утверждений (2026-10-10)**: гарантированно истинны только факты из статей (pdf-якорь) и Lean-теоремы; собственные численные результаты — свидетельство с явным покрытием сетки, никогда не «истина». Рендеры графа и любые тексты не смазывают эту разницу; утверждение без опоры живёт только в статусе question/conjectured.
- **Эссе ≠ письменный слой**: thesis/essay — архивный снапшот старого контура; новые научные формулировки рождаются только как тезисы/карточки графа.
