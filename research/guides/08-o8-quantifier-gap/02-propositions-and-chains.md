# O8 (часть 1): Верифицированные теоремы в Lean 4 (`BridgeO8QuantifierGap.lean`)

Все 7 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`, замороженное ядро `BridgeFormalV2.Model` / `Goals` не изменено):

1. `aro_subset_prefixMaximin` и `source_subset_prefixMaximin`: `D.aroLevels ⊆ prefixMaximinLevels D` и `D.sourceLevels ⊆ prefixMaximinLevels D` (слабое минимаксное неравенство $V_{\mathrm{mm}}^{\mathrm{prefix}} \le V(\{r\})$).
2. `prefixMaximin_subset_fullMaximin`: `prefixMaximinLevels D ⊆ fullMaximinLevels D` ($V_{\mathrm{mm}}^{\mathrm{full}} \le V_{\mathrm{mm}}^{\mathrm{prefix}}$).
3. `prefixMaximin_iff_tightened`: точная редукция `prefixMaximinLevels D` через сужение будущих возмущений F3 (`TightenedPointwiseBound` и `D.futureRowSupport`).
4. `zero_gap_hierarchy_of_unconstrained_terminal`: `D.rows = 0 → openLoopLevels D = D.aroLevels ∧ D.aroLevels = prefixMaximinLevels D ∧ prefixMaximinLevels D = fullMaximinLevels D`.
5. `exists_strict_quantifier_gap_witness`: на 1D-свидетеле `o8GapWitnessData` ($A = 2$, $B = E = H = c = \rho = 1$, $U = [-1, 1]$, $g \in [-2, 4]$) доказано: `0 ∈ prefixMaximinLevels D`, `0 ∈ fullMaximinLevels D`, `2 ∈ D.aroLevels`, `∀ η ∈ D.aroLevels, 2 ≤ η`, `4 ∈ openLoopLevels D` и `∀ η ∈ openLoopLevels D, 4 ≤ η` (точный тройной разрыв $0 < 2 < 4$ на непрерывных боксах $[-1, 1]^2$).
6. `exists_prefix_zero_full_strict_gap_witness`: на симметричном 1D-интеграторе `o8SymmetricData` ($A = B = E = H = c = \rho = 1$, $U = [-1, 1]$, $g \in [-1, 1]$) доказано: `0 ∈ fullMaximinLevels D`, `1 ∈ D.aroLevels`, `1 ∈ prefixMaximinLevels D` и `∀ η ∈ prefixMaximinLevels D, 1 ≤ η` (нулевой префиксный зазор при строгом полном зазоре $\ge 1$).

## Внешние и машинные опоры

- Литература (PDF): [A4 Дмитрук (2022), стр. 1](../../../corpus/our_papers/A4_Дмитрук_2022.pdf#page=1).
- Формальные модули и точные оракулы: [BridgeO8QuantifierGap.lean](../../../verification/lean/AroProofs/BridgeO8QuantifierGap.lean), [check_o8_gap.py](../../../research/counterexamples/O8-sion-gap/checks/check_o8_gap.py), [run02_falsify.py](../../../research/discovery/run02/run02_falsify.py).
