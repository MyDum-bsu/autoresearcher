# G2: Верифицированные теоремы в Lean 4 (`BridgeG2ConicSupport.lean`)

Все 7 теорем проверены ядром Lean 4 `v4.35.0-rc2` (`0 sorry`, аксиомы строго `[propext, Classical.choice, Quot.sound]`):

1. `general_attained_support`: для любой семьи непустых компактов $W_t$ и любой линейной строки $r$ верхняя оценка $\sum_t h_{W_t}(g_t)$ выполняется для всех $w^+ \in \prod_t W_t$ и **достигается** на конкретном блоке $w^* \in \prod_t W_t$.
2. `general_robust_row`: $\big(\forall w^+ \in \prod_t W_t,\; r(z + R_w w^+) \le b\big) \iff r(z) + \sum_t h_{W_t}(g_t) \le b$.
3. `general_exact_tightening`: `GeneralAROBound D W a y eta ↔ GeneralTightenedAROBound D W a y eta` (сохранены обе стороны всех терминальных ограничений, знаковая стоимость `D.c` и префикс `D.Z`).
4. `box_support_eq_f3`: специализация $W_t = [-\rho, \rho]^p$ совпадает с `D.futureRowSupport` из F3.
5. `l1_cross_polytope_support`: компактность, непустота и точная двойственная норма $h_{B_1(r)}(v) = r \max_i |v_i|$.
6. `l2_soc_ball_support`: компактность, непустота и точная самодвойственная SOC-норма $h_{B_2(r)}(v) = r \sqrt{\sum_i v_i^2}$ (Коши–Буняковский + градиентный свидетель).
7. `l2_ball_not_finset_conv_2d`: при $r > 0$ двумерный шар $B_2(r)$ не представим как конечная выпуклая оболочка `InFinsetConv T` ни для какого конечного $T \subset B_2(r)$ (инъекция $\mathbb{N} \hookrightarrow \text{ext}(B_2(r))$ через стереографические точки $r(\frac{k^2-1}{k^2+1}, \frac{2k}{k^2+1})$).

## Внешние и машинные опоры

- Литература (PDF): [Xu & Burer (2017), стр. 1](../../../corpus/07_Xu_Burer_2017.pdf#page=1), [Chen & Zhang (2009), стр. 6](../../../corpus/03_Chen_Zhang_2009.pdf#page=6).
- Формальные модули и фальсификаторы: [BridgeG2ConicSupport.lean](../../../verification/lean/AroProofs/BridgeG2ConicSupport.lean), [falsify_g2.py](../../../verification/falsifiers/run01/falsify_g2.py).
