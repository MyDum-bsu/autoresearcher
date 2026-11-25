# O1 / O2 / O5 (часть 2): Верифицированные теоремы в Lean 4 (`BridgeO1FullRankRecourse.lean`)

Все 8 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`, замороженное ядро `BridgeFormalV2.Model` / `Goals` не изменено):

1. `futureRowSupport_nonneg`, `futureRowSupport_neg` и `futureRowSupport_add_le` (свойства опорного функционала F3): для любой `D : Data` и любых линейных строк `row`, `row₁`, `row₂` выполнены неотрицательность $h(\mathrm{row}) \ge 0$, симметрия $h(-\mathrm{row}) = h(\mathrm{row})$ и субаддитивность $h(\mathrm{row}_1 + \mathrm{row}_2) \le h(\mathrm{row}_1) + h(\mathrm{row}_2)$.
2. `bridge_adr_exact_of_unconstrained_terminal` (`O5`): если `D.rows = 0`, то `bridgeAdrLevels D = D.aroLevels` и `bridgeAdrLevels D = D.sourceLevels` (опирается на `zero_gain_of_unconstrained_terminal` из `BridgeO4ClosureValue.lean` и `BridgeFormalV2.Proofs.epigraph_equality`).
3. `bridge_adr_exact_diagonal` (`O1`, произвольная размерность): для любой системы `D : Data` со структурой `DiagonalBridgeData D` ($n = m = p = \mathrm{rows}$, диагональные $A, B, E, H$, произвольные горизонты $r, q$, критерий $c$ и границы $u_{\min}, u_{\max}, g_{\min}, g_{\max}, \rho > 0$) доказано точное равенство `bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`. Ключевая цепочка: F4 угловая ЛП + минимизация покоординатного вклада по крайним граням $\xi_i = \pm R_i$ + совместная реализация знаков `cornerOfSigns` + F3 точное сужение.
4. `shearRecourse_bijective` (`O1`): доказана биективность матрицы $B = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ системы `bridgeFullRankShearData` (`Function.Bijective bridgeFullRankShearData.B`).
5. `exists_bridge_2d_fullrank_invertible_strict_adr_gap` (опровержение `H-O1-1`): на `bridgeFullRankShearData` ($n = m = \mathrm{rows} = 2$, $A = E = H = I_2$, биективная $B$) доказано $5 \in D.\mathrm{aroLevels} \cap D.\mathrm{sourceLevels}$ и $\forall \eta \in \mathrm{bridgeAdrLevels}\ D,\ 6 \le \eta$.
6. `exists_bridge_linear_adr_gap_scaling` (`O2`): для всякого $k \ge 1$ на $k$-блочной системе `bridgeLinearGapData k hk` размерности $n = 2k$ доказано $6k \in D.\mathrm{aroLevels} \cap D.\mathrm{sourceLevels}$ и $\forall \eta \in \mathrm{bridgeAdrLevels}\ D,\ 8k \le \eta$.

## Внешние и машинные опоры

- Литература (PDF): [Chen & Zhang (2009), стр. 6](../../../corpus/03_Chen_Zhang_2009.pdf#page=6), [Georghiou, Tsoukalas, Wiesemann (2025), стр. 8](../../../corpus/24_Georghiou_Tsoukalas_Wiesemann_2025.pdf#page=8).
- Формальные модули и точные оракулы: [BridgeO1FullRankRecourse.lean](../../../verification/lean/AroProofs/BridgeO1FullRankRecourse.lean), [check_o1_shear_gap.py](../../../research/counterexamples/O1-fullrank-shear-gap/checks/check_o1_shear_gap.py), [derivation.md](../../../research/counterexamples/O1-fullrank-shear-gap/derivation.md).
