# TL;DR и Дорожная карта исследований `autoresearcher` (`aro-discovery` v2)

> **Статус документа:** актуальный снимок состояния проекта и исследовательская дорожная карта (Decision D-23, 2026-11-25, ветка `research/autonomous-cycle-03`).
> **Устав и канонические источники:** [`CHARTER.md`](../CHARTER.md), [`AGENTS.md`](../AGENTS.md), [`README.md`](../README.md), [`research/atlas/ATLAS.md`](../research/atlas/ATLAS.md), [`research/problem-map.md`](../research/problem-map.md).

---

## English Abstract

`autoresearcher` (`aro-discovery` v2) is a verifier-gated mathematical research program investigating the exact bridge between **Optimal Guaranteed Control (OGU, Dmitruk school)** and **Two-Stage / Multi-Stage Adaptive Robust Optimization (ARO)** with fixed recourse, the **value of information under closure scheduling** (`O4`, `O7`), the **sharp exactness boundaries of Affine Decision Rules (ADR/LDR)** (`O1`, `O2`, `O5`), and **minimax-vs-maximin quantifier-order commitment gaps** (`O8`).

Every scientific claim follows a strict **Falsify-First** and **Dual-Lock** discipline: conjectures must survive exact rational (`fractions.Fraction`) LP / Bellman / SymPy falsifiers and the executable `T1–T7` battery before proof synthesis; Lean 4 formalizations compile against an immutable `frozen_core` (`BridgeFormalV2.Model` / `Goals`) with **0 `sorry`** and standard axioms strictly `⊆ {propext, Classical.choice, Quot.sound}`; and every formalized track is paired with a 4-file Russian study pack in `research/guides/` for **LearnHarness v0.7.0** (human-only attestation).

As of `research/autonomous-cycle-03`, the formal Lean 4 kernel contains **78 machine-checked declarations (0 `sorry`)** across 11 proof modules — **F1/F2** (10), **P1–P3** (5), **F3** (4), **F4** (9), **G2** (7), **O4 single-closure** (7), **G1** (6), **O1 part 1** (7), **O8 quantifier-gap** (7, Cycle 01), **O4/O7 multi-closure scheduling & supermodular synergy** (8, Cycle 02), and the newly formalized **O1/O2/O5 & F3 full-rank recourse refutation (`H-O1-1`), arbitrary-dimension diagonal ADR exactness, F3 support subadditivity & linear `Ω(n)` gap scaling** track (`BridgeO1FullRankRecourse.lean`, 8 declarations, Cycle 03) — complemented by exact rational oracles (`M0`, `A4 r=67,104`), exact counterexamples (`D1`, `D2`, `E-rank1`, `A-S1`, `O8-sion-gap`, `O4-supermodular-synergy`, `O1-fullrank-shear-gap`, `T2–T5`), and 5 Stage-2 **Run-02** frontier falsifiers. This document summarizes what is rigorously proved vs. oracle-verified vs. honestly open, prioritizes the immediate research queue, and outlines the deeper mathematical theory this program is building toward.

---

## 1. TL;DR: Что делает проект прямо сейчас

`autoresearcher` решает единую связную математическую задачу (Устав [`CHARTER.md §1`](../CHARTER.md)):

1. **Несущая линия (мост ОГУ ↔ ARO и ценность информации):** построить формально доказанный мост между линейным дискретным оптимальным гарантированным управлением с замыканиями в моменты $R = \{r_1 < \dots < r_k\}$ и двухэтапной/многоэтапной адаптивной робастной оптимизацией с фиксированным рекурсом; охарактеризовать **ценность измерения** $G(R) = V(\emptyset) - V(R)$, **оптимальное расписание замыканий $R$** (`O4 + O7`) и **зазор порядка квантификаторов** $V(R) - V_{\mathrm{mm}}$ (`O8`).
2. **Прикладная ветвь внутри моста (границы точности ADR/LDR):** найти проверяемые геометрические и алгебраические границы точности аффинных решающих правил ($V_{\mathrm{ADR}} = V_{\mathrm{ARO}}$, задачи `O1/O2/O5`) за пределами классических достаточных условий (симплекс, покомпонентный бокс, обратно-положительный рекурс) при обязательной проверке на исполнимой батарее фальсификации `T1–T7`.

Принцип научной дисциплины: **LLM не судит истинность**. Любая гипотеза проходит:
- **Stage 2 (Falsify-First):** точный рациональный ЛП (`fractions.Fraction`), Беллман (`M0`), SymPy и батарея `T1–T7` в обоих режимах `-B` и `-B -O`;
- **Stage 3 (Lean 4 Dual-Lock):** формализация поверх замороженного ядра `BridgeFormalV2.Model` / `Goals`, `0 sorry`, аксиомы строго `⊆ {propext, Classical.choice, Quot.sound}`;
- **Stage 4 (No Black-Box Theorems):** 4-файловый русский конспект в `research/guides/` (гейт **G5**), статус `attested` ставит **только человек**.

---

## 2. Что уже строго доказано в Lean 4 vs. проверено точными оракулами и контрпримерами

### 2.1. Формальное ядро Lean 4 (`v4.35.0-rc2`, 78 деклараций, 0 `sorry`)

Все 78 деклараций проходят аудит в [`verification/lean/AroProofs/Inventory.lean`](../verification/lean/AroProofs/Inventory.lean) с разрешённым списком аксиом `{propext, Classical.choice, Quot.sound}`:

| Трек | Модуль Lean 4 | Кол-во | Что строго доказано | Статус |
|---|---|---:|---|---|
| **F1** | `BridgeFormalV2/Proofs/Dynamics.lean` | 5 | Точное хронологическое раскрытие линейной дискретной динамики $x_r = s_0(a) + L w^-$ и суффикса для произвольных $A, B, E, H, c$ (без $A=I$ и обратимости) | `formalized` (baseline) |
| **F2** | `BridgeFormalV2/Proofs/Policies.lean` | 5 | Экзогенность $\Xi = L(W^r)$, сохранение волокон наблюдения, взаимный перевод Borel-политик ОГУ ↔ 2-этапная ARO, равенство эпиграфов `sourceLevels = aroLevels` | `formalized` (baseline) |
| **P1–P3** | `AroProofs/Aroform.lean` (`V1Aroform`) | 5 | Поворот $\ell_1$-нормы, 2-путевые тождества L2a, антимонотонность инфимума `info_value_monotone`, точность 1D хордового ADR | `formalized` (v1 baseline) |
| **F3** | `BridgeFormalV3/Proofs/Support.lean` | 4 | Точное исключение будущих возмущений $w^+$ через опорную функцию бокса: `future_expansion`, `attained_support`, `robust_row`, `exact_tightening` | `formalized` (0 `sorry`, завершено!) |
| **F4** | `AroProofs/BridgeF4CornerLP.lean`, `BridgeF4ExtremeLP.lean` | 9 | Измеримый Borel-селектор на зонотопе $\Xi = L(W^r)$, конечность вершин, точная эквивалентность конечной угловой и экстремальной вершиннной ЛП с `aroLevels` и `sourceLevels` | `formalized` (Run-01) |
| **G2** | `AroProofs/BridgeG2ConicSupport.lean` | 7 | Общее сужение Минковского на произвольных компактах $W_t$, специализации на бокс, $\ell_1$-кросс-политоп и $\ell_2$-шар (SOC), доказательство неполиэдральности 2D $\ell_2$-шара | `formalized` (Run-01, частичное) |
| **O4 (ч.1)** | `AroProofs/BridgeO4ClosureValue.lean` | 7 | Монотонность $V(\{r\}) \le V(\emptyset)$, обнуление выигрыша при `D.rows = 0` или в ядре $\ker(HA^q) \cap \ker(cA^q)$, критерий разделения угловых ЛП, машинный свидетель разрыва $4 > 2$ | `formalized` (Run-01, частичное) |
| **G1** | `AroProofs/BridgeG1Multistage.lean` | 6 | Произвольное число замыканий $k \ge 2$: расщепление стадий, перевод политик по истории, равенство эпиграфов `History = Multistage ARO`, строгое разделение Markov vs History при $k=2$ | `formalized` (Run-01, частичное) |
| **O1** | `AroProofs/BridgeO1ADRExactness.lean` | 7 | Цепочка `Static ⊆ ADR ⊆ ARO`, точность ADR на симплексе, барицентрические сизигии и разрыв Чэня–Чжана T3, 1D-точность и 2D-строгий разрыв ADR внутри `BridgeFormalV2` | `formalized` (Run-01, частичное) |
| **O8** | `AroProofs/BridgeO8QuantifierGap.lean` | 7 | 4-уровневая иерархия `OpenLoop ⊆ ARO = Source ⊆ PrefixMM ⊆ FullMM`, F3-сужение для `PrefixMM`, схлопывание всей иерархии при `D.rows = 0`, точный тройной разрыв $0 < 2 < 4$ (`ce-o8-sion-gap`) и дихотомия $V_{\mathrm{mm}}^{\mathrm{full}} \le 0 < 1 = V_{\mathrm{mm}}^{\mathrm{prefix}} = V(\{1\})$ | `formalized` (Cycle-01) |
| **O4 / O7 (ч.2)** | `AroProofs/BridgeO4Scheduling.lean` | 8 | Полная решётка монотонности расписаний на $T=3$ (`∅ ⊆ {1}, {2} ⊆ {1,2}`), схлопывание всех 4 расписаний при `D.rows = 0`, строгое опровержение субмодулярности $G(R)$ (4D сдвиговый регистр: $G(\{1\})=G(\{2\})=0, G(\{1,2\})=1$, дефект $+1$), строгая субмодулярность (дефект $-1$) и двустороннее доминирование одиночных замыканий ($V(\{1\}) < V(\{2\})$ и $V(\{2\}) < V(\{1\})$) | `formalized` (Cycle-02) |
| **O1 / O2 / O5 + F3 (ч.2)** | `AroProofs/BridgeO1FullRankRecourse.lean` | 8 | Неотрицательность, симметрия и субаддитивность опорного функционала F3; схлопывание ADR при `D.rows = 0` (`O5`); **произвольно-мерная диагональная точность ADR** (`bridge_adr_exact_diagonal`, любое $n, r, q, c$); **опровержение `H-O1-1`** на биективном унимодулярном сдвиге $B = [[1,1],[0,1]] \in \mathrm{SL}_2(\mathbb{Z})$ с $H = I_2$ ($5 < 6$); **линейный рост зазора $\Omega(n)$** (`6k` vs `8k`, отношение $\ge 4/3$, `O2`) | `formalized` (Cycle-03, **NEW**) |

> **Важное уточнение про статус F3 (`Support.lean`):** в ранней карте [`research/problem-map.md`](../research/problem-map.md) файл `BridgeFormalV3/Proofs/Support.lean` числился как WIP. Фактически все 4 цели F3 (`future_expansion`, `attained_support`, `robust_row`, `exact_tightening`) **полностью доказаны без `sorry`**, проходят аудит в `Inventory.lean` и активно используются как фундамент в F4, G2, O4 и O8.

### 2.2. Точные рациональные оракулы, контрпримеры и Stage-2 фальсификаторы

| Артефакт | Расположение | Что установлено (детерминированно, `-B` и `-B -O`) |
|---|---|---|
| **M0 Oracle** | `verification/oracles/m0/` | Конечный эталон и независимый Беллман по ячейкам состояний (36 тестов) |
| **Wave-4 A4 Closures** | `verification/oracles/wave4-a4-closures/`, `research/claims/bridge-transfer-v1/` | Точные рациональные интервалы A4 Дмитрук для одного замыкания при $r=67$ и $r=104$ (32 контроля переноса, байт-идентично в `-B` и `-B -O`) |
| **Wave-5 Support Bound** | `research/claims/wave5-support-bound/` | Двойственная верхняя оценка ценности информации $J \le V_0 \le V_r \le D_0 + \Delta$ |
| **D1 & D2** | `research/counterexamples/D1-baseline/`, `D2-structured/` | Потеря предсказательной информации при слиянии префиксов (D1) и неэквивалентность попарной и совместной совместимости (D2) |
| **E-rank1 & A-S1** | `research/counterexamples/E-rank1/`, `astra-probe-AS1/` | Singleton-контрпример при $\mathrm{rank}(L) \le 1$ (E) и положительный покоординатно-разделимый подкласс при $\mathrm{rank}(L) = 2$ (A-S1, 38 проверок) |
| **O8-sion-gap** | `research/counterexamples/O8-sion-gap/` | Точный ЛП + SymPy непрерывный сертификат строгого разрыва $V(\{1\}) = 2 > 0 = V_{\mathrm{mm}}^{\mathrm{prefix}} = V_{\mathrm{mm}}^{\mathrm{full}}$ (доказан в Lean 4, Cycle 01) |
| **O4-supermodular-synergy** | `research/counterexamples/O4-supermodular-synergy/` | Точный ЛП + SymPy непрерывный сертификат строгого опровержения субмодулярности $G(R)$ (4D сдвиговый регистр: $G(\{1\})=G(\{2\})=0, G(\{1,2\})=1$, дефект $+1$) и двустороннего доминирования одиночных замыканий ($V(\{1\}) < V(\{2\})$ и $V(\{2\}) < V(\{1\})$); полностью доказан в Lean 4 (Cycle 02) |
| **O1-fullrank-shear-gap** | `research/counterexamples/O1-fullrank-shear-gap/` | Точный ЛП + SymPy непрерывный сертификат **опровержения `H-O1-1`** (биективный унимодулярный сдвиг $B = [[1,1],[0,1]], \det B = 1, H = I_2, U = [-1/2, 1/2]^2$: $V_{\mathrm{ARO}} = 5 < 6 = V_{\mathrm{ADR}}$), диагонального контраста ($B_{\mathrm{diag}} = \mathrm{diag}(2, 1) \implies$ зазор $0$) и линейного роста зазора $6k$ vs $8k$ (`O2`); полностью доказан в Lean 4 (Cycle 03, **NEW**) |
| **Батарея T1–T7** | `verification/falsifiers/battery_t1_t7.py` | Исполнимая 7-тестовая батарея точности ADR: положительные (`T1` мост-класс, `T6` покомпонентный бокс, `T7` симплекс) и отрицательные (`T2` SOC Сюй–Бюрер, `T3` Чэнь–Чжан, `T4` GTW25, `T5` BEG18 $\Omega(\sqrt{m})$) |
| **Run-02 Falsifiers** | `research/discovery/run02/run02_falsify.py` | 5 Stage-2 точных рациональных ЛП-зондов (прошли Significance Gate 5/5): O4 субмодулярность на 1D-интеграторе (`defect = -1 ≤ 0`, субмодулярность выжила на 1D, но опровергнута в Cycle 02 на 4D сдвиговом регистре!), G1 марковская достаточность при инъективном сдвиговом регистре, G2 $\ell_1$-вершинная ЛП (2D exact vs 3D gap $1/2$), O1 ранг рекурса $B$ и активные ограничения в 2D, O8 параметрическая дихотомия по $u_{1,\max}$ |

---

## 3. Приоритетные направления исследований прямо сейчас

Исходя из текущего состояния Атласа (5 открытых узлов, из которых все 5 теперь имеют частичное покрытие в Lean 4 и Stage-2 зонды в Run-02), приоритеты выстроены по научной отдаче для диссертации и публикабельности:

### Приоритет 1 — **O4 / O7: Комбинаторика и алгоритмика расписания замыканий $R$ (`conj-o4-closure-scheduling`)**
- **Что уже сделано (обновлено в Cycle 02!):**
  - В `BridgeO4ClosureValue.lean` (7 теорем): необходимые условия строгого выигрыша для $k=1$, критерий разделения угловых ЛП, свидетель разрыва $4 > 2$.
  - В `BridgeO4Scheduling.lean` (8 теорем, Cycle 02) + контрпример `O4-supermodular-synergy`: полная решётка монотонности на $T=3$, схлопывание при `D.rows = 0`, **строгое опровержение субмодулярности $G(R)$** на 4D сдвиговом регистре ($G(\{1\})=G(\{2\})=0, G(\{1,2\})=1$, дефект $+1$, нулевой коэффициент аппроксимации жадного алгоритма), строгая субмодулярность на 1D-интеграторе (дефект $-1$) и **двустороннее доминирование одиночных замыканий** ($V(\{1\}) < V(\{2\})$ и $V(\{2\}) < V(\{1\})$).
- **Ближайшая цель:** найти структурный подкласс динамики (например, скалярные 1D-системы с одним односторонним ограничением $x_T \ge g_{\min}$, где ни один из 23+ рациональных зондов не дал супермодулярности), в котором $G(R)$ гарантированно субмодулярна (что возвращает $(1 - 1/e)$-гарантию жадного выбора $R$) либо где $V(\{r\})$ квазивыпукла по $r$.

### Приоритет 2 — **G1: Инъективность наблюдения и граница Маркова в многоэтапном мосте (`gen-multistage-k-closures`)**
- **Что уже сделано:** мост `HistoryState = Multistage ARO` для любого $k$ и строгое разделение `Markov < History` при $k=2$ (`BridgeG1Multistage.lean`), плюс зонд `run02-g1-markov-sufficiency` (инъективный 2D сдвиговый регистр $x_2 = (w_0, w_1)$ даёт нулевой зазор, а слитая проекция $s_2 = w_0 + w_1$ даёт зазор $1$ на той же задаче).
- **Ближайшая цель:** формализовать в Lean 4 **теорему достаточности марковских политик** при инъективности отображения истории в состояние $x_{r_j}$ (наблюдаемость префикса), а также **многоэтапную конечную вершинную ЛП** для независимых боксовых возмущений (обобщение F4 на $k \ge 2$).

### Приоритет 3 — **O1 / O2 / O5: Геометрическая граница точности ADR/LDR (`conj-o1-adr-exactness-char`)**
- **Что уже сделано (обновлено в Cycle 03!):**
  - В `BridgeO1ADRExactness.lean` (7 теорем): симплекс, барицентрические сизигии, T3 Чэнь–Чжан, 1D-точность и 2D-строгий зазор.
  - В `BridgeO1FullRankRecourse.lean` (8 теорем, Cycle 03) + контрпример `O1-fullrank-shear-gap`: субаддитивность/симметрия/неотрицательность опорной функции F3; схлопывание ADR при `D.rows = 0` (`O5`); **произвольно-мерная диагональная точность ADR** (`bridge_adr_exact_diagonal`, любое $n, r, q, c$); **строгое опровержение `H-O1-1`** на биективном унимодулярном сдвиге $B = [[1,1],[0,1]] \in \mathrm{SL}_2(\mathbb{Z})$ с $H = I_2$ ($V_{\mathrm{ARO}} = 5 < 6 = V_{\mathrm{ADR}}$); и **линейный рост зазора $\Omega(n)$** ($6k$ против $8k$, отношение $\ge 4/3$, `O2`).
- **Ближайшая цель:** атаковать полную геометрическую характеризацию недиагональных $(A, B, E, H)$ через согласованность конуса активных ограничений с пространством сизигий зонотопа $\Xi$, а также проверить достижимость сверхконстантного мультипликативного роста $\Omega(\sqrt{n})$ внутри замороженного `BridgeFormalV2.Data` (`O2`).

### Приоритет 4 — **G2: Коническая двойственность и полиэдральная граница (`gen-nonbox-conic-uncertainty`)**
- **Что уже сделано:** общее сужение Минковского на компактах, $\ell_1/\ell_2$ опорные функции и неполиэдральность 2D $\ell_2$-шара (`BridgeG2ConicSupport.lean`); зонд `run02-g2-l1-vertex-lp` отделил конечную вершинную ЛП на $\ell_1$-кросс-политопе (точную в любой размерности) от провала ADR в 3D (зазор $1/2$).
- **Ближайшая цель:** формализовать конечную $2p$-вершинную ЛП для $\ell_1$-кросс-политопа в Lean 4 и исследовать точную коническую двойственность (SOCP / SDP-лифтинг, регулярность Слейтера) для неполиэдральных $W_t$.

### Приоритет 5 — **O8: Количественная теория зазора квантификаторов (`conj-o8-quantifier-gap`)**
- **Что уже сделано (в этом цикле!):** 7 теорем в `BridgeO8QuantifierGap.lean` (иерархия, F3-сужение, обнуление при `D.rows = 0`, строгий тройной разрыв $0 < 2 < 4$ и дихотомия префиксного и полного зазоров).
- **Ближайшая цель:** формализовать параметрическую формулу `run02-o8-gap-vanishing-regime` ($V(\{1\}) - V_{\mathrm{mm}}^{\mathrm{prefix}} = \max(0, \rho - u_{1,\max})$) и найти многомерное достаточное условие обнуления префиксного зазора через суффиксную управляемость (авторитет $B$-рекурса покрывает зонотоп $\Xi$).

---

## 4. В какую более глубокую математическую теорию это может вырасти

Текущие результаты уже складываются не в разрозненный набор лемм, а в контур **единой геометрической теории информации и адаптивности в линейных робастных системах**:

1. **Двойственная геометрия зонотопов в двухэтапной и многоэтапной ОГУ/ARO.**
   Вся динамика с фиксированным рекурсом проектирует гиперкуб прошлых возмущений $W^r$ в зонотоп $\Xi = L(W^r)$, а будущее $W^q$ свёртывает в опорный сдвиг $h_{W^q}(r)$. Из этой единой картины одновременно вытекают:
   - конечность вершинной редукции (F4) и её обрыв на неполиэдральных конусах (G2);
   - измеримость оптимального управления через Borel-селектор на барицентрической триангуляции;
   - многоэтапная фильтрация зонотопов и расщепление «память vs состояние» (G1 + D1/D2).
2. **Теория ценности информации и комбинаторная оптимизация расписаний замыканий (`O4 + O7`).**
   Функция $G(R) = V(\emptyset) - V(R)$ задаёт нелинейную функцию множеств на моментах времени $\{1, \dots, T-1\}$. Открытие её не-субмодулярности (синергии измерений) связывает ОГУ с теорией субоптимальных сенсорных расписаний, оценками кривизны/субмодулярного отношения и двойственными сертификатами Фаркаша ценности измерения.
3. **Острые геометрические пороги точности аффинных правил (сизигии + ранг рекурса, `O1/O2/O5`).**
   Аффинное правило на многограннике $\Xi$ с $K$ вершинами обязано удовлетворять всем линейным барицентрическим сизигиям между вершинами $\Xi$ (для симплекса их $0 \Rightarrow$ ADR всегда точен; для квадрата — $1$; для $d$-октаэдра — экспоненциально много). Точность ADR определяется тем, согласуется ли конус активных ограничений рекурса (и ранг $B$) с пространством сизигий $\Xi$. Это даёт прямой путь к необходимому и достаточному геометрическому критерию точности ADR.
4. **Декомпозиция потерь обязательства в робастных минимаксных играх (`O8`).**
   Разложение полного зазора $V(R) - V_{\mathrm{mm}}^{\mathrm{full}} = \underbrace{(V(R) - V_{\mathrm{mm}}^{\mathrm{prefix}})}_{\text{потеря раннего обязательства}} + \underbrace{(V_{\mathrm{mm}}^{\mathrm{prefix}} - V_{\mathrm{mm}}^{\mathrm{full}})}_{\text{неустранимый будущий шум}}$ позволяет отделить «цену каузальности» (которую можно обнулить достаточным суффиксным авторитетом рекурса) от «фундаментальной энтропии будущего» (определяемой опорной функцией $h_{W^q}$).

---

## 5. Конкретные открытые задачи и фальсифицируемые гипотезы для следующих циклов

| ID | Гипотеза / Открытая задача | Критерий фальсификации (Stage 2) | Цель формализации (Stage 3, Lean 4) |
|---|---|---|---|
| **H-O4-1** | Не-субмодулярность $G(R)$: существуют LTI-системы ($T=3$), где $G(\{1,2\}) - G(\{1\}) > G(\{2\}) - G(\emptyset)$ (строгая супермодулярная синергия) | **ЗАКРЫТО (Cycle 02):** 4D сдвиговый регистр `O4-supermodular-synergy` (`defect = +1`) + 1D интегратор (`defect = -1`) | **ДОКАЗАНО В LEAN 4:** `BridgeO4Scheduling.lean` (8 теорем, 0 `sorry`) + конспект `09-o4-scheduling-synergy` |
| **H-O4-2** | Субмодулярный подкласс $G(R)$: при каком условии на $(A, B, E, H, g)$ функция $G(R)$ субмодулярна (или $V(\{r\})$ квазивыпукла по $r$)? | Точная рациональная сетка по $(A, B, E, H, g_{\min}, g_{\max})$ на $T \in \{3, 4, 5\}$ в `exact_lp.py` | Достаточное условие квазивыпуклости $V(\{r\})$ или субмодулярности $G(R)$ |
| **H-G1-1** | Инъективность наблюдения $\implies V_{\mathrm{Markov}}(R) = V_{\mathrm{History}}(R)$ для произвольного $k \ge 2$ | Прошёл на $k=2$ в `run02_falsify.py` (`injective_gap = 0`, `merged_gap = 1`) | `BridgeG1MarkovSufficiency.lean`: общая теорема для любого $k$ при левой обратимости карты истории |
| **H-G2-1** | Точная конечная $2p$-вершинная ЛП для $\ell_1$-кросс-политопа при строгом провале ADR в размерности $p \ge 3$ | Прошёл в `run02_falsify.py` (`dim2_gap = 0`, `dim3_gap = 1/2`) | `BridgeG2L1VertexLP.lean`: эквивалентность $2p$-вершинной ЛП и 3D-разрыв ADR |
| **H-O1-1** | В 2D-мосте с полным рангом рекурса ($B$ обратим) и покоординатным терминальным боксом ($H = I_2$) ADR точен ($V_{\mathrm{ADR}} = V_{\mathrm{ARO}}$), тогда как $\mathrm{rank}(B) = 1$ даёт строгий зазор | **ОПРОВЕРГНУТО (Cycle 03):** унимодулярный сдвиг `O1-fullrank-shear-gap` ($B = [[1,1],[0,1]], \det B = 1, H = I_2 \implies 5 < 6$); зато диагональные $(A, B, E, H)$ точны в любой размерности $n$ | **ДОКАЗАНО В LEAN 4:** `BridgeO1FullRankRecourse.lean` (8 теорем, 0 `sorry`) + конспект `10-o1-fullrank-diagonal-boundary` |
| **H-O8-1** | Параметрическая формула зазора $V(\{1\}) - V_{\mathrm{mm}}^{\mathrm{prefix}} = \max(0, \rho - u_{1,\max})$ и многомерное условие суффиксного покрытия $\Xi \subseteq \mathrm{Reach}_q(U)$ для обнуления префиксного зазора | Прошёл 1D-свип в `run02_falsify.py`; проверить 2D-гипотезу суффиксного покрытия точным ЛП | Расширение `BridgeO8QuantifierGap.lean` параметрической и многомерной теоремами |

---

## 6. Как воспроизвести все проверки локально

```bash
# Python-гейты, точные оракулы, контрпримеры, батарея T1-T7 и Run-02 фальсификаторы (-B и -B -O):
make verify-public-hygiene verify-migration verify-corpus verify-m0 verify-transfer \
     verify-counterexamples verify-falsifiers verify-lean verify-literature \
     verify-discovery verify-remote verify-run02 verify-learn

# Проверка всех 10 русских учебных пакетов (Gate G5, включая 08-o8-quantifier-gap, 09-o4-scheduling-synergy и 10-o1-fullrank-diagonal-boundary):
python3 -B verification/gates/verify_guides.py --no-style

# Сборка ядра Lean 4 (78 деклараций, 0 sorry) и живые Lean-гейты:
cd verification/lean && LEAN_NUM_THREADS=2 lake build AroProofs.Inventory && cd ../..
LEAN_NUM_THREADS=1 make verify-lean-compile verify-atlas verify-claim
```
