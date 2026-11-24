# F4: Цепочка теорем и доказательство в Lean 4

## Ключевая конструкция (3 шага без допущения инъективности $L$)

1. **Конечная лексикографическая индукция (`borel_right_inverse_exists`):**
   - Отображение $L : [-\rho, \rho]^N \to \mathbb{R}^n$ ($N = r p$) непрерывно на компакте $K = [-\rho, \rho]^N$.
   - Последовательно минимизируем координаты $w_0, w_1, \dots, w_{N-1}$ на компактном слое $S_k(\xi) = \{w \in K \mid L w = \xi,\; w_{<k} = f_{<k}(\xi)\}$.
   - По компактности инфимум $f_k(\xi) = \inf \{w_k \mid w \in S_k(\xi)\}$ **достигается** (`IsCompact.sInf_mem`), а подмножество уровня:
     $$\{\xi \in \Xi \mid f_k(\xi) \le t\} = (\mathrm{id}, f_{<k})^{-1}\!\Big((L, \pi_{<k})(\{w \in K \mid w_k \le t\})\Big)$$
     является прообразом компактного (значит, замкнутого и борелевского!) множества при уже измеримом отображении $(\mathrm{id}, f_{<k})$.
   - Итоговый селектор $s(\xi) = (f_0(\xi), \dots, f_{N-1}(\xi))$ — **измеримый по Борелю правый обратный**: $s(\xi) \in W^r$ и $L(s(\xi)) = \xi$.
2. **Полилинейная барицентрическая интерполяция (`vertex_lp_to_aro`):**
   - На гиперкубе $[-\rho, \rho]^N$ веса $\alpha_\sigma(w) = \prod_{k=0}^{N-1} \frac{\rho \pm w_k}{2\rho} \ge 0$ непрерывны, дают $\sum_\sigma \alpha_\sigma(w) = 1$ и $\sum_\sigma \alpha_\sigma(w) L(\mathrm{corner}(\sigma)) = L(w)$.
   - Интерполированное управление $b(w) = \sum_\sigma \alpha_\sigma(w) u_\sigma$ непрерывно, лежит в $U^q$ и сохраняет все линейные суженные неравенства `TightenedAt`.
   - Политика $y(\xi) = b(s(\xi))$ борелевски измерима и удовлетворяет `TightenedAROBound` и `AROBound` (через F3 `exact_tightening`).
3. **Редукция к истинным крайним точкам $\operatorname{vert}(\Xi)$ (`zonotopeVertices_finite`, `extreme_vertex_lp_to_aro`, `extreme_vertex_lp_epigraph_eq_aro`, `extreme_vertex_lp_epigraph_eq_source`):**
   - Индукцией по числу элементов конечного порождающего множества образов углов $S = L(\{-\rho, +\rho\}^N)$ доказывается: $\operatorname{vert}(\Xi) \subseteq S$ (множество конечного размера) и $\Xi = \operatorname{conv}(\operatorname{vert}(\Xi))$.
   - Любое решение ЛП на $\operatorname{vert}(\Xi)$ поднимается выпуклыми комбинациями до решения на всех углах $W^r$, откуда:
     $$\mathrm{extremeVertexLPLevels}(D) = \mathrm{vertexLPLevels}(D) = D.\mathrm{aroLevels} = D.\mathrm{sourceLevels}.$$

## Верифицированные декларации Lean 4 (`0 sorry`, только `[propext, Classical.choice, Quot.sound]`)
- `AroProofs.BridgeF4VertexLP.borel_right_inverse_exists`
- `AroProofs.BridgeF4VertexLP.vertex_lp_to_aro`
- `AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_aro`
- `AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_source`
- `AroProofs.BridgeF4VertexLP.zonotopeVertices_finite`
- `AroProofs.BridgeF4VertexLP.extreme_vertex_lp_to_aro`
- `AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_aro`
- `AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_source`
- `AroProofs.BridgeF4VertexLP.extreme_vertex_lp_eq_corner_lp`

## Внешние и машинные опоры

- Литература (PDF): [A4 Дмитрук (2022), стр. 1](../../../corpus/our_papers/A4_Дмитрук_2022.pdf#page=1), [Ayoub & Poss (2016), стр. 4](../../../corpus/06_Ayoub_Poss_2016.pdf#page=4).
- Формальные модули и фальсификаторы: [BridgeF4CornerLP.lean](../../../verification/lean/AroProofs/BridgeF4CornerLP.lean), [BridgeF4ExtremeLP.lean](../../../verification/lean/AroProofs/BridgeF4ExtremeLP.lean), [falsify_f4.py](../../../verification/falsifiers/run01/falsify_f4.py).
