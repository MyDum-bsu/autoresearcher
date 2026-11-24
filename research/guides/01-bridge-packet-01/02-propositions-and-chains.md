# Пакет 01: Атомарные утверждения и цепочки вывода (F1/F2)

> Файл структурирован под экстрактор графа знаний **LearnHarness v0.7.0** (`POST /api/graph/import` → `nodes.jsonl` + `chains.jsonl`). Каждая пропозиция самодостаточна, а в цепочках перечислены **все совместные посылки**, нужные для вывода.
> **Опоры:** [Model.lean](../../../verification/lean/BridgeFormalV2/Model.lean), [Goals.lean](../../../verification/lean/BridgeFormalV2/Goals.lean), [Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean), [Policies.lean](../../../verification/lean/BridgeFormalV2/Proofs/Policies.lean), [A4_Дмитрук_2022.pdf](../../../corpus/our_papers/A4_Дмитрук_2022.pdf) (физ. с. 2–4), [A3_Костюкевич_Дмитрук_2021.pdf](../../../corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf) (физ. с. 4), [02_BenTal_Goryashko_etal_2004.pdf](../../../corpus/02_BenTal_Goryashko_etal_2004.pdf) (физ. с. 3).

---

## 1. Атомарные пропозиции

- **P0 (Дискретная линейная модель A3/A4 с одним замыканием):** система $x_{t+1} = A x_t + B u_t + E w_t$ на $t = 0, \ldots, T-1$ с $T = r + q$ ($r > 0, q > 0$), фиксированным $x_0 \in \mathbb{R}^n$, произвольными линейными $A, B, E, H, c$, непустым прямоугольником управлений $U = [\underline u, \overline u] \subset \mathbb{R}^m$ и независимыми по времени возмущениями $w \in W^T$, где $W = [-\rho, \rho]^p$, $\rho > 0$. В момент $r$ измеряется точное состояние $x_r$, после чего выбирается весь второй блок $b \in U^q$ без знания $w^+ \in W^q$. Опора: `BridgeFormalV2.Data` ([Model.lean](../../../verification/lean/BridgeFormalV2/Model.lean)), [A4_Дмитрук_2022.pdf](../../../corpus/our_papers/A4_Дмитрук_2022.pdf) (физ. с. 2–4).
- **P1 (Непустота допустимых блоков):** для любых данных $D$ и любой длины $k \in \mathbb{N}$ множества допустимых блоков управления $U^k$ и возмущений $W^k$ непусты (свидетели — нижняя граница $\underline u$ и нулевой шум $0$). Опора: `BridgeFormalV2.Proofs.nonempty_blocks` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P2 (Точное линейное раскрытие рекурсии):** фактическая $k$-шаговая рекурсия `run` совпадает с конечной линейной формулой
  $$
  \mathrm{run}(x, u, w, k) = A^k x + \sum_{t=0}^{k-1} A^{k-1-t}\bigl(B u_t + E w_t\bigr).
  $$
  Опора: `BridgeFormalV2.Proofs.expansion` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P3 (Разложение состояния в момент измерения):** для любого первого блока $a \in U^r$ и любого префикса возмущений $w^- \in W^r$ измеренное состояние равно сумме номинального состояния и чистого отклика на возмущение:
  $$
  x_r(a, w^-) = s_0(a) + \xi(w^-), \qquad s_0(a) = \mathrm{run}(x_0, a, 0, r), \qquad \xi(w^-) = \mathrm{run}(0, 0, w^-, r).
  $$
  Опора: `BridgeFormalV2.Proofs.prefix_split` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P4 (Экзогенность множества отклонений):** образ разности $\mathrm{range}\bigl(w^- \mapsto x_r(a, w^-) - s_0(a)\bigr)$ равен $\Xi = \mathrm{range}(\xi)$ для любого допустимого первого блока $a \in U^r$, то есть область неопределённости второй стадии не зависит от $a$. Опора: `BridgeFormalV2.Proofs.exogenous_image` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P5 (Инвариантность волокон наблюдения):** любая допустимая политика состояния $\pi : S(a) \to U^q$ назначает одинаковый второй блок $b$ для любых двух префиксов $w_1^-, w_2^- \in W^r$ с равным измеренным состоянием $x_r(a, w_1^-) = x_r(a, w_2^-)$ и не зависит от будущего $w^+ \in W^q$. Опора: `BridgeFormalV2.Proofs.observation_fibre` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P6 (Хронологическое и суффиксное совпадение траекторий):** траектория ОГУ удовлетворяет пошаговой рекурсии на каждом $t < r + q$, а её терминальное состояние в момент $r + q$ совпадает с суффиксным раскрытием из точки $s_0(a) + \xi(w^-)$. Опора: `BridgeFormalV2.Proofs.source_chronology`, `BridgeFormalV2.Proofs.suffix_expansion` ([Dynamics.lean](../../../verification/lean/BridgeFormalV2/Proofs/Dynamics.lean)).
- **P7 (Измеримость сдвигов между $S(a)$ и $\Xi$):** взаимно обратные отображения $\tau_a(\xi) = s_0(a) + \xi$ из $\Xi$ в $S(a)$ и $\tau_a^{-1}(s) = s - s_0(a)$ из $S(a)$ в $\Xi$ непрерывны, а значит Borel-измеримы на подпространствах $\mathbb{R}^n$. Опора: `toState_measurable`, `toDeviation_measurable` ([Policies.lean](../../../verification/lean/BridgeFormalV2/Proofs/Policies.lean)).
- **P8 (Сохранение управлений, траекторий и уровней — `Preserves`):** для любого $a \in U^r$:
  1. каждая Borel-политика ОГУ $\pi$ переводится в Borel-правило ARO $y(\xi) = \pi(s_0(a) + \xi)$ с совпадением управлений, траекторий для всех $t \le r + q$ и эквивалентностью $\mathrm{SourceBound}(a, \pi, \eta) \iff \mathrm{AROBound}(a, y, \eta)$ для каждого $\eta \in \mathbb{R}$;
  2. каждое Borel-правило ARO $y$ переводится обратно в Borel-политику ОГУ $\pi(s) = y(s - s_0(a))$ с теми же инвариантами.
  Опора: `BridgeFormalV2.Proofs.forward_policy`, `BridgeFormalV2.Proofs.reverse_policy` ([Policies.lean](../../../verification/lean/BridgeFormalV2/Proofs/Policies.lean)).
- **P9 (Равенство множеств достижимых уровней гарантии):** множества вещественных уровней $\eta$, достижимых в задаче ОГУ и в двухэтапной ARO-переформулировке, совпадают как множества:
  $$
  \mathrm{sourceLevels}(D) = \mathrm{aroLevels}(D).
  $$
  Опора: `BridgeFormalV2.Proofs.epigraph_equality` ([Policies.lean](../../../verification/lean/BridgeFormalV2/Proofs/Policies.lean)).
- **P10 (Явная граница регулярности):** равенство `P9` доказано для пары Borel-измеримых классов (`StatePolicy` и `DeviationPolicy`). На страницах [A3_Костюкевич_Дмитрук_2021.pdf](../../../corpus/our_papers/A3_Костюкевич_Дмитрук_2021.pdf) (физ. с. 4) и [A4_Дмитрук_2022.pdf](../../../corpus/our_papers/A4_Дмитрук_2022.pdf) (физ. с. 3–4) Borel-измеримость явно не оговорена, поэтому сравнение с произвольными неизмеримыми стратегиями остаётся отдельным открытым шагом.

---

## 2. Совместные цепочки рассуждений

- **Цепочка C1 (`P0 + P2 ⇒ P3`):** линейность оператора шага $x_{t+1} = A x_t + B u_t + E w_t$ вместе с формулой раскрытия `expansion` даёт аддитивное разложение $x_r(a, w^-) = s_0(a) + \xi(w^-)$. Без линейности по $(x, u, w)$ разделение на управляемый номинал и экзогенное отклонение рушится.
- **Цепочка C2 (`P0 + P3 ⇒ P4`):** вычитание $s_0(a)$ из $x_r(a, w^-)$ сокращает вклад $x_0$ и $a$, оставляя $\xi(w^-)$, который зависит только от $w^- \in W^r$. Поскольку $W^r$ фиксировано и не зависит от $a$, образ $\Xi$ экзогенен.
- **Цепочка C3 (`P0 + P3 + P6 + P7 ⇒ P8`):** построение прямого и обратного переводов политик $y = \pi \circ \tau_a$ и $\pi = y \circ \tau_a^{-1}$ с сохранением управлений, траекторий и уровней опирается на четыре посылки:
  - `P0 + P3` обеспечивают корректность сдвигов $\tau_a : \Xi \to S(a)$ и $\tau_a^{-1} : S(a) \to \Xi$ (из них же в `C2` вытекает экзогенность `P4`), а сама формула перевода вместе с `P3` напрямую даёт совпадение вторых блоков управления на каждом префиксе $w^-$ и совпадение траекторий для всех $t \le r + q$;
  - `P7` сохраняет Borel-измеримость при композиции;
  - `P6` (`suffix_expansion`) связывает терминальное состояние траектории ОГУ с суффиксной формулой ARO `aroTerminal`, откуда вытекает эквивалентность $\mathrm{SourceBound}(a, \pi, \eta) \iff \mathrm{AROBound}(a, y, \eta)$.
  *(Свойство `P5` служит отдельной проверкой информационной корректности `StatePolicy` в модели `P0` и не входит в посылки вывода `P8`.)*
- **Цепочка C4 (`P8 ⇒ P9`):** взаимное существование сохраняющих уровень партнёров $\pi \leftrightarrow y$ для каждого допустимого первого блока $a$ и каждого $\eta \in \mathbb{R}$ немедленно даёт двустороннее включение $\mathrm{sourceLevels}(D) \subseteq \mathrm{aroLevels}(D)$ и $\mathrm{aroLevels}(D) \subseteq \mathrm{sourceLevels}(D)$.
- **Цепочка C5 (`P9 + P10 ⇒ Граница Пакета 01`):** из `P9` вытекает точная информационная эквивалентность ОГУ и двухэтапной ARO в Borel-классе, но с учётом `P10` и отсутствия `F3/F4` Пакет 01 ещё не утверждает конечную вершинную LP-редукцию и не снимает вопрос неизмеримых стратегий.

---

## 3. Сводная таблица проверенных деклараций Lean 4

| Пропозиция | Декларация Lean 4 (`BridgeFormalV2.Proofs`) | Аксиомы (аудит) |
|---|---|---|
| `P1` | `BridgeFormalV2.Proofs.nonempty_blocks` | `propext`, `Classical.choice`, `Quot.sound` |
| `P2` | `BridgeFormalV2.Proofs.expansion` | `propext`, `Classical.choice`, `Quot.sound` |
| `P3` | `BridgeFormalV2.Proofs.prefix_split` | `propext`, `Classical.choice`, `Quot.sound` |
| `P4` | `BridgeFormalV2.Proofs.exogenous_image` | `propext`, `Classical.choice`, `Quot.sound` |
| `P5` | `BridgeFormalV2.Proofs.observation_fibre` | `propext`, `Classical.choice`, `Quot.sound` |
| `P6` | `BridgeFormalV2.Proofs.source_chronology`, `BridgeFormalV2.Proofs.suffix_expansion` | `propext`, `Classical.choice`, `Quot.sound` |
| `P8` | `BridgeFormalV2.Proofs.forward_policy`, `BridgeFormalV2.Proofs.reverse_policy` | `propext`, `Classical.choice`, `Quot.sound` |
| `P9` | `BridgeFormalV2.Proofs.epigraph_equality` | `propext`, `Classical.choice`, `Quot.sound` |

> Все 10 деклараций проверены статическим аудитом `make verify-lean` (0 `sorry`/`admit`/`axiom`) и историческим независимым replay в [theorem-audit.json](../../../legacy/extracted/campaign/lean-audits/formal-v2/final-review/theorem-audit.json); свежая перекомпиляция ядра запланирована в R2 (`#1156`).
