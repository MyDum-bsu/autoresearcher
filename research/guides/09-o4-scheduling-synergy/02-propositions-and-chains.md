# O4 / O7 (часть 2): Верифицированные теоремы в Lean 4 (`BridgeO4Scheduling.lean`)

Все 8 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`, замороженное ядро `BridgeFormalV2.Model` / `Goals` не изменено):

1. `schedEmpty_subset_schedR1` и `schedEmpty_subset_schedR2`: для любой системы `D : Data` на горизонте $T = 3$ над полным непрерывным боксом возмущений $[-\rho, \rho]^3$ выполняются включения `schedEmptyLevels D ⊆ schedR1Levels D` и `schedEmptyLevels D ⊆ schedR2Levels D` ($V(\{1\}) \le V(\emptyset)$ и $V(\{2\}) \le V(\emptyset)$).
2. `schedR1_subset_schedR12` и `schedR2_subset_schedR12`: для любой `D : Data` выполняются `schedR1Levels D ⊆ schedR12Levels D` и `schedR2Levels D ⊆ schedR12Levels D` ($V(\{1,2\}) \le V(\{1\})$ и $V(\{1,2\}) \le V(\{2\})$).
3. `sched_collapse_of_unconstrained_terminal`: при `D.rows = 0` все четыре множества уровней совпадают (`schedEmptyLevels D = schedR1Levels D = schedR2Levels D = schedR12Levels D`).
4. `exists_strict_supermodular_synergy`: на 4D стационарной системе `synergyWitnessData` доказано $V(\emptyset) = V(\{1\}) = V(\{2\}) = 1$ и $V(\{1,2\}) = 0$, откуда $G(\emptyset) = G(\{1\}) = G(\{2\}) = 0$, $G(\{1,2\}) = 1$ (дефект субмодулярности $+1 > 0$).
5. `exists_strict_submodular_and_early_dominance`: на 1D-интеграторе `earlyDomWitnessData` ($A = 1$, $U = [-1/2, 1/2]$, $g \in [-2, 10]$) доказано $V(\emptyset) = 4$, $V(\{1\}) = 2$, $V(\{2\}) = 3$, $V(\{1,2\}) = 2$ (строгая субмодулярность с дефектом $-1$ и строгое раннее доминирование $V(\{1\}) < V(\{2\})$).
6. `exists_strict_late_dominance`: на 1D-сжимающей системе `lateDomWitnessData` ($A = 1/2$, $U = [-1, 1]$, $g \in [-2, 10]$) доказано $V(\emptyset) = 3/2$, $V(\{1\}) = 1$, $V(\{2\}) = 0$, $V(\{1,2\}) = 0$ (строгое позднее доминирование $V(\{2\}) < V(\{1\})$).

## Внешние и машинные опоры

- Литература (PDF): [A4 Дмитрук (2022), стр. 1](../../../corpus/our_papers/A4_Дмитрук_2022.pdf#page=1).
- Формальные модули и точные оракулы: [BridgeO4Scheduling.lean](../../../verification/lean/AroProofs/BridgeO4Scheduling.lean), [check_o4_synergy.py](../../../research/counterexamples/O4-supermodular-synergy/checks/check_o4_synergy.py), [derivation.md](../../../research/counterexamples/O4-supermodular-synergy/derivation.md).
