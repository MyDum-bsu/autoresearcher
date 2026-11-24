# G1 (часть 1): Верифицированные теоремы в Lean 4 (`BridgeG1Multistage.lean`)

Все 6 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`):

1. `multistage_stage_split`: для любых замороженных данных `BridgeFormalV2.Data`, любого `k`, вектора длин этапов `len : Fin (k + 1) → Nat` и любого совместного множества `Ω` состояние в конце этапа раскладывается аддитивно на номинальный отклик и экзогенное отклонение `stageDeviation`.
2. `multistage_forward_policy` и `multistage_reverse_policy`: две причинные измеримые по Борелю трансляции между `HistoryStatePolicy` и `HistoryDeviationPolicy` (на полных пространствах историй `Fin j.val → Vec D.n`), сохраняющие состояния на границах этапов, терминальное состояние и эпиграфные оценки на любом `Ω` (без заявления о поточечной взаимной обратности на недостижимых историях).
3. `multistage_history_epigraph_eq_aro`: точное равенство эпиграфов `multistageHistoryLevels D len Ω = multistageAroLevels D len Ω`.
4. `multistage_markov_subset_history`: марковские уровни всегда вложены в уровни с историей и ARO (`multistageMarkovLevels D len Ω ⊆ multistageHistoryLevels D len Ω`).
5. `exists_markov_strictly_weaker_than_history_k2`: на явном 1D-свидетеле с `k = 2` (`len = (1, 1, 1)`, `A = 0, B = 1, E = 2, U = [-1, 1], H = 1, [0, 10], c = 1`, коррелированный путь `w_0 = w_2 ∈ {-1/2, +1/2}, w_1 ∈ [-1, 1]`) доказано: `0 ∈ multistageHistoryLevels`, `0 ∈ multistageAroLevels`, и `∀ η ∈ multistageMarkovLevels, 2 ≤ η` — с разгромом произвольного нелинейного борелевского сигналинга на этапе 1.

## Внешние и машинные опоры

- Литература (PDF): [A4 Дмитрук (2022), стр. 1](../../../corpus/our_papers/A4_Дмитрук_2022.pdf#page=1), [A5 Дмитрук (диссертация 2022), стр. 1](../../../corpus/our_papers/A5_Дмитрук_диссертация_2022.pdf#page=1).
- Формальные модули и фальсификаторы: [BridgeG1Multistage.lean](../../../verification/lean/AroProofs/BridgeG1Multistage.lean), [falsify_g1.py](../../../verification/falsifiers/run01/falsify_g1.py).
