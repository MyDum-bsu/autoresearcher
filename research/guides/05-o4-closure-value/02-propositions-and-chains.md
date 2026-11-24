# O4 (часть 1): Верифицированные теоремы в Lean 4 (`BridgeO4ClosureValue.lean`)

Все 7 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`):

1. `openLoop_subset_aro` и `openLoop_subset_source`: `openLoopLevels D ⊆ D.aroLevels` и `openLoopLevels D ⊆ D.sourceLevels`.
2. `zero_gain_of_unconstrained_terminal`: `D.rows = 0 → D.aroLevels = openLoopLevels D ∧ D.sourceLevels = openLoopLevels D`.
3. `zero_gain_of_prefix_in_terminal_kernel`: `(∀ w, H (A^q (deviation w)) = 0 ∧ c (A^q (deviation w)) = 0) → D.aroLevels = openLoopLevels D ∧ D.sourceLevels = openLoopLevels D`.
4. `openLoop_eq_shared_corner_lp`: точное совпадение `openLoopLevels D` с конечной угловой ЛП с общим суффиксом `b`.
5. `strict_gain_iff_corner_separation`: при фиксированном `η` условие `η ∈ D.aroLevels ∧ η ∉ openLoopLevels D` эквивалентно выполнимости `VertexLPBound` и невыполнимости `SharedCornerLPBound` на некотором угле для любой пары `(a, b)`.
6. `exists_strict_value_of_measurement_gap`: на явном 1D свидетеле (`A=2, B=1, E=1, U=[-1,1], rho=1, H=1, [-2,4], c=1`) доказано `2 ∈ D.sourceLevels`, `2 ∈ D.aroLevels` и `∀ η ∈ openLoopLevels D, 4 ≤ η` (точные оптимумы `2` и `4` подтверждены точным ЛП в `falsify_o4.py`).

## Внешние и машинные опоры

- Литература (PDF): [A4 Дмитрук (2022), стр. 1](../../../corpus/our_papers/A4_Дмитрук_2022.pdf#page=1), [A5 Дмитрук (диссертация 2022), стр. 1](../../../corpus/our_papers/A5_Дмитрук_диссертация_2022.pdf#page=1).
- Формальные модули и фальсификаторы: [BridgeO4ClosureValue.lean](../../../verification/lean/AroProofs/BridgeO4ClosureValue.lean), [falsify_o4.py](../../../verification/falsifiers/run01/falsify_o4.py).
