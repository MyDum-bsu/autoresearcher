# O1 (часть 1): Верифицированные теоремы в Lean 4 (`BridgeO1ADRExactness.lean`)

Все 7 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, 0 предупреждений, аксиомы строго `[propext, Classical.choice, Quot.sound]`):

1. `static_subset_adr_subset_aro`: для любой задачи `FixedRecourseARO d m k` и любого `Ξ`, `staticLevels P Ξ ⊆ adrLevels P Ξ ⊆ aroLevels P Ξ`.
2. `adr_exact_on_simplex`: для любой размерности `d` и любой задачи `P`, `adrLevels P (stdSimplex d) = aroLevels P (stdSimplex d)`.
3. `barycentric_syzygy_adr_coupling`: равенство аффинных комбинаций `∑ α_a • ξ_a = ∑ β_b • ζ_b` (`∑ α_a = ∑ β_b = 1`) влечёт `∑ α_a • (y_0 + Y ξ_a) = ∑ β_b • (y_0 + Y ζ_b)` для любого аффинного правила `(y_0, Y)`.
4. `chen_zhang_t3_adr_gap`: формальное применение `barycentric_syzygy_adr_coupling` к 3D кросс-политопу T3 — `1 ∈ aroLevels` и `∀ η ∈ adrLevels, 3 ≤ η`.
5. `bridge_adr_subset_aro_and_source`: на замороженном `BridgeFormalV2.Data` всякая аффинная политика по отклонению `AffineDeviationPolicy` непрерывна (измерима по Борелю), и `bridgeAdrLevels D ⊆ D.aroLevels`, `bridgeAdrLevels D ⊆ D.sourceLevels`.
6. `bridge_adr_exact_1d`: универсальная 1D-точность — `∀ D : Data, D.n = 1 → bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`.
7. `exists_bridge_2d_strict_adr_gap`: минимальная размерность зазора `n = 2` — конкретный 2D-свидетель `bridgeAdrGapData` с `6 ∈ D.aroLevels`, `6 ∈ D.sourceLevels` и `∀ η ∈ bridgeAdrLevels D, 8 ≤ η` (прямой вывод по угловым неравенствам квадрата).

## Внешние и машинные опоры

- Литература (PDF): [Chen & Zhang (2009), стр. 6](../../../corpus/03_Chen_Zhang_2009.pdf#page=6), [Georghiou, Tsoukalas, Wiesemann (2025), стр. 8](../../../corpus/24_Georghiou_Tsoukalas_Wiesemann_2025.pdf#page=8).
- Формальные модули и фальсификаторы: [BridgeO1ADRExactness.lean](../../../verification/lean/AroProofs/BridgeO1ADRExactness.lean), [falsify_o1.py](../../../verification/falsifiers/run01/falsify_o1.py).
