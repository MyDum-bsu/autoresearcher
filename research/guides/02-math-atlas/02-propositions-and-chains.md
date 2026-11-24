# Пакет 02: Атомарные утверждения и цепочки вывода Атласа

> **Опоры:** [atlas.json](../../atlas/atlas.json), [BLUEPRINT.md](../../../verification/lean/blueprint/BLUEPRINT.md), [Model.lean](../../../verification/lean/BridgeFormalV2/Model.lean), [Goals.lean](../../../verification/lean/BridgeFormalV3/Goals.lean), [Aroform.lean](../../../verification/lean/AroProofs/Aroform.lean), [A4_Дмитрук_2022.pdf](../../../corpus/our_papers/A4_Дмитрук_2022.pdf), [02_BenTal_Goryashko_etal_2004.pdf](../../../corpus/02_BenTal_Goryashko_etal_2004.pdf).

---

## 1. Атомарные определения ядра

- **A1 (Модель ОГУ — `def-ogu-system`).** В [Model.lean](../../../verification/lean/BridgeFormalV2/Model.lean) задана дискретная линейная система $x_{t+1} = A x_t + B u_t + E w_t$ на горизонте $T = r + q$, где $u_t \in [u_{\min}, u_{\max}]$, $w_t \in [-\rho, \rho]^p$ с $\rho > 0$. Непустота допустимых блоков управлений и возмущений доказана декларацией `BridgeFormalV2.Proofs.nonempty_blocks`.
- **A2 (Экзогенное отклонение — `def-exogenous-deviation`).** Префиксный отклик на возмущение $\xi = L w^-$ порождает зонотоп $\Xi = L(W^r)$, не зависящий от первого блока управления $a$ (`BridgeFormalV2.Proofs.exogenous_image`).
- **A3 (Политики по Борелю — `def-borel-policies`).** Политика ОГУ $g : S(a) \to U^q$ и правило ARO $y : \Xi \to U^q$ измеримы по Борелю и сохраняют волокна наблюдения (`BridgeFormalV2.Proofs.observation_fibre`).
- **A4 (Направленная опорная функция — `def-future-support`).** Для любой линейной строки $h$ в [Goals.lean](../../../verification/lean/BridgeFormalV3/Goals.lean) определена точная опорная величина будущего возмущения:

$$
\sigma_q(h) \;=\; \rho \sum_{t=0}^{q-1} \sum_{i=1}^{p} \bigl|h(A^{q-1-t} E e_i)\bigr|.
$$

---

## 2. Доказанные в Lean 4 цепочки вывода (`lean_proved`)

### Цепочка C1: Полный мост F1 → F2 → F3 (14 деклараций Lean 4)

- **P1 (`thm-f1-expansion`):** Рекуррентная траектория совпадает с явной линейной суммой и раскладывается в момент $r$ как $x_r = s_0(a) + \xi$ (`BridgeFormalV2.Proofs.expansion`, `BridgeFormalV2.Proofs.prefix_split`, `BridgeFormalV2.Proofs.source_chronology`, `BridgeFormalV2.Proofs.suffix_expansion`).
- **P2 (`thm-f2-policy-bijection`):** Сдвиг аргумента $y(\xi) = g(s_0(a) + \xi)$ и обратный сдвиг $g(s) = y(s - s_0(a))$ переводят допустимые Borel-политики друг в друга с сохранением траекторий (`BridgeFormalV2.Proofs.forward_policy`, `BridgeFormalV2.Proofs.reverse_policy`).
- **P3 (`thm-f2-epigraph-equality`):** Из `P1 + P2` следует равенство множеств гарантированных уровней $\mathrm{sourceLevels}(D) = \mathrm{aroLevels}(D)$ (`BridgeFormalV2.Proofs.epigraph_equality`).
- **P4 (`thm-f3-future-tightening`):** В [Support.lean](../../../verification/lean/BridgeFormalV3/Proofs/Support.lean) доказано аддитивное отделение будущего возмущения, достижимость $\sigma_q(h)$ в вершине бокса и точная эквивалентность универсальной робастной строки и суженной строки:

$$
\forall w^+ \in W^q,\; h(z + R_w w^+) \le b \;\Longleftrightarrow\; h(z) + \sigma_q(h) \le b.
$$

Эта цепочка закрывает 4 декларации F3 (`future_expansion`, `attained_support`, `robust_row`, `exact_tightening`), полностью подтверждённые живым ядром Lean 4 в [Inventory.lean](../../../verification/lean/AroProofs/Inventory.lean).

### Цепочка C2: Информационная монотонность и одномерная точность ADR (5 деклараций Lean 4)

- **P5 (`lem-p1-l1-rotation`):** Тождество поворота $|a| + |b| = \max(|a+b|, |a-b|)$ и двупутевые формулы в [Aroform.lean](../../../verification/lean/AroProofs/Aroform.lean) сводят 2D задачу мост-класса к разделённым координатам суммы и разности.
- **P6 (`lem-p2-info-monotone`):** В [Aroform.lean](../../../verification/lean/AroProofs/Aroform.lean) доказана абстрактная порядковая лемма для подмножеств `Set ENNReal`: из $S \subseteq T$ следует $\inf T \le \inf S$ (`AroProofs.Aroform.info_value_monotone`). Применение этой леммы к расписаниям замыканий $R \subseteq R'$ (опора [A5_Дмитрук_диссертация_2022.pdf](../../../corpus/our_papers/A5_Дмитрук_диссертация_2022.pdf)) требует отдельного — пока не формализованного в Lean 4 — доказательства включения множеств достижимых уровней.
- **P7 (`thm-p3-1d-adr-exactness`):** В одномерной задаче рекурса на $[0, 1]$ хордовое аффинное правило достигает точного адаптивного оптимума (`AroProofs.Aroform.one_d_exactness`), что служит базовым случаем для 1D/2D эталона `T1` в [battery_t1_t7.py](../../../verification/falsifiers/battery_t1_t7.py).

---

## 3. Цепочки оракульной верификации и открытого фронта

- **C3 (Численный перенос на A4 Дмитрук):** `thm-f3-future-tightening` специализируется на 4 замороженных экземплярах A4 (`r=67` и `r=104`), где [check.py](../../claims/bridge-transfer-v1/check.py) проверяет 32 контроля (16 принятых, 16 отвергнутых) в точных дробях `Fraction`.
- **C4 (Двойственная оценка Wave-5 — частичная верификация):** Оценка $J \le V_0 \le V_r \le D_0 + \Delta$ (и следствие $V_r - V_0 \le D_0 + \Delta - J$) **не** выводится только из F3 и абстрактной леммы `P6` о `sInf`. Согласно [handoff.md](../../claims/wave5-support-bound/verification/handoff.md), она опирается на отдельные письменные (не формализованные в Lean 4) посылки: политико-скалярную редукцию с неотрицательными двойственными множителями $\lambda, \mu \ge 0$, независимые экстремумы непрерывного бокса, вложение постоянных программ открытого контура ($V_0 \le V_r$), неравенство треугольника для опорных функций ($\Delta \ge 0$) и символьное тождество остатков $D_0 + \Delta - q$, проверенное в `SymPy`. Конечный скрипт [check.py](../../claims/wave5-support-bound/verification/check.py) независимо воспроизводит 4 замороженных экземпляра A4 (`r=67` и `r=104`, включая точное $J = D_0$ и $\Delta = 0$ при `r=104`) и отвергает 16 искажённых контролей.
- **C5 (Открытый переход к F4 и O4):** `thm-f3-future-tightening` + `thm-transfer-a4-v1` открывают гипотезу **F4** (`conj-f4-vertex-lp-selector`) о конечной вершинной LP-редукции на $\operatorname{vert}(\Xi)$ с измеримым селектором, а `lem-wave5-support-bound` + `thm-m0-finite-bellman` открывают задачу **O4** (`conj-o4-closure-scheduling`) о строгой ценности измерения и выборе оптимального расписания $R$.
- **C6 (Открытая характеризация O1 и обобщения G1–G2):** Положительные ориентиры `T1` (мост-класс), `T6` (боксовая статика, [05_Bertsimas_deRuiter_2016.pdf](../../../corpus/05_Bertsimas_deRuiter_2016.pdf)) и `T7` (симплекс, [21_Zhen_denHertog_Sim_2018.pdf](../../../corpus/21_Zhen_denHertog_Sim_2018.pdf)) задают требования к гипотезе **O1**, а `thm-f3-future-tightening` — точку старта для многоэтапного обобщения **G1** ($k \ge 2$) и обобщения **G2** на произвольные компактные выпуклые множества $W_t$ (как полиэдральные вроде кросс-политопа $\ell_1$, так и неполиэдральные — евклидов шар $\ell_2$, SOC или спектраэдр). При этом исключение шума через опорную функцию Минковского $h_{W_t}$ остаётся точным для любого компакта $W_t$, тогда как точность ADR отдельно ограничена связями `constrains_adr` от `T2` и `T3`.
