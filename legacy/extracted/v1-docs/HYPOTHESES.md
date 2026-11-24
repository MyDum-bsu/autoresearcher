# Гипотезы проекта — человеческим языком

> Ответ на критику владельца (2026-09-22): «гипотезы абстрактны, не видно
> связей и того, к чему сходимся». Этот документ — нарративный слой над
> формальными узлами DAG. Каждая карточка: зачем → что утверждаем → что уже
> проверено → чего не хватает → к чему ведёт. Формальные формулировки —
> в узлах DAG (id указаны), машинные доказательства — в артефактах и Lean.

## Лестница доказательства (общий путь каждой гипотезы)

```
seed-вопрос (идея из структуры диссертации)
  → измерения на машинах (LP-оракул, точные дроби)
  → гипотеза (conjectured, statement-lint)
  → атаки (атакующие сетки + исчерпывающие охоты — ДО вывода)
  → survived-falsifier (пережила всё, что мы смогли бросить)
  → доказательство (двойной маршрут) → formalized (Lean, 0 ошибок)
  → глава диссертации (черновик из закрытых узлов, anchor-lint)
```

---

## Карточка 1: «Быстро и точно — совместимы» (conj-ldr-exactness)

**Зачем это нужно.** В робастной оптимизации точный ответ требует перебора
всех сценариев (у нас — всех вершин множества неопределённости), и это
дорого. Аффинная подстройка (решение «по формуле» от сценария) решает
быстро — один LP. Вопрос: теряем ли мы при этом гарантию? Если нет —
задачи нашего класса решаются на порядок быстрее без потери точности.

**Что утверждаем (формально).** В классе: fixed recourse, неопределённость
только в правой части h(ζ) = h0 + Hζ, полиэдральное Z — существует
оптимальное аффинное решающее правило: его гарантированная стоимость
равна точному оптимуму z*.

**Что уже проверено (машиной, точными дробями).**
- Полные перечисления: 20 (1D) + 2025 (2D) + 48 600 (плотный W, рабочая
  первая стадия) инстансов — **0 контрпримеров**.
- Две атакующие сетки (отрицательные T, широкие H) — пережита.
- **1D-случай доказан** и формализован в Lean: хордовая политика точна,
  дешевле не бывает (thm-ldr-1d, formalized).

**Чего не хватает до теоремы.** Доказательства в размерности ≥2. Машина
нашла условие: при «согласованных» знаках отклика задача распадается
на 1D-случаи (следует из 2D-декомпозиции), при разнознаковых — выгода
от информации исчезает. Формулировка 2D-теоремы готова, доказательство —
в работе.

**К чему ведёт.** Глава 2 диссертации: граница применимости быстрых
методов + условия точности. Практически: задачи класса решаются LP за
один проход вместо перебора.

Узел: `conj-ldr-exactness` · статус: survived-falsifier · опирается на:
измерения трека A, BGT-2004 Thm 2.2 (форма совпадает) · атакована:
falsify_attempt × 4+.

---

## Карточка 2: «RO лежит между ОГУ и ДП» (conj-oc-ro-dp-bridge)

**Зачем это нужно.** В школе Дмитрук (ОГУ — оптимальное гарантированное
управление) оценка функционала даётся гарантирующей программой (это
нижняя опора: консервативно, но без информации о состоянии), а полный
учёт информации даёт другую (лучшую) оценку. Вопрос: даёт ли RO
промежуточную оценку, и как она ведёт себя при добавлении информации?
Это мост между двумя школами и — потенциально — новый метод оценки.

**Что утверждаем (формально).** Информационная структура = множество R
моментов «замыкания» (в эти моменты состояние измеряется, управление
корректируется — это в точности рекурсивная часть RO-формулировки).
Тогда гарантированная оценка монотонна по R: больше замыканий — лучше
оценка; любое промежуточное R даёт оценку между OC (R=∅) и DP (R=полное).

**Что уже проверено (машиной).**
- Дискретная игра T=4: 12 инстансов × 8 наборов замыканий (включая
  не-префиксные), инвариант по всем сравнимым парам R1 ⊆ R2 — строгая
  цепь OC > RO(1) > RO(2) > DP.
- **Машина нашла условие содержательности**: при согласованном отклике
  строк состояния цепь строгая; при разнознаковых E — лестница плоская
  (информация бесполезна). Это войдёт в формулировку теоремы.
- Принцип монотонности формализован в Lean (thm-info-monotone).

**Чего не хватает.** Перенос на полную терминальную задачу ОГУ (семантика
соответствия «замыкания ↔ стадии рекурса» — зона человека по §6);
количественное сравнение с методом Дмитрук на их инстансах.

**К чему ведёт.** Новый взгляд на мост ОГУ↔ARO: RO-формулировка как
промежуточная точка семейства методов с управляемой гранулярностью
информации. Для диссертации — глава 2/3 и мост к статьям A2–A5.

Узел: `conj-oc-ro-dp-bridge` · статус: survived-falsifier · опирается на:
rq-ogu-bridge, Дмитрук A2/A4 (якоря) · атакована: лестница 12×8.

---

## Где мы сойдёмся (траектория проекта)

1. **Ближайшая теорема**: 2D-точность аффинных правил при согласованном E
   (декомпозиция s/d уже подтверждена LP до числа; L1-лемма доказана в Lean).
2. **Ближайшее опровержение или расширение**: охота на границе (T≠0,
   плотный W, nz≥3) — либо контрпример к общей гипотезе (первоклассный
   результат), либо расширение класса точности.
3. **Мост**: сравнение RO-лестницы с методом Дмитрук на их инстансах —
   прямой научный результат на стыке школ.
4. **Сходимость диссертации**: из выживших теорем и границ собираются
   главы; карта «что чем доказано» — приложением; всё остальное
   (опровергнутое) — честным Negative Results-разделом.

## Карточки контура (генерат `ro card sync`)

> Первичный письменный слой контура: карточка обязательна до первого прогона атаки (решение владельца 2026-10-10, seq 6068). Пишет агент, ревью — пачкой; аттестация только человеком.

## h-toy-zstar — Toy z* closed form (runner proof card)

status: survived-falsifier
- statement: For all beta >= 0 and Y >= 0: z*(beta, Y) = max(beta - Y, 0) for the toy family min x s.t. x >= 0, (beta - x)^+ <= Y
- falsifier: one exact Fraction mismatch of max(beta - Y, 0) against the hand-derived oracle on the frozen grids
- vocabulary: z* = optimal value; beta = nominal demand; Y = recourse budget
- origin: toy_family ground truth, hand-derived (machinery demo, not science)
- formalization: Aroform.lean toy_z_nonneg

## h-auto-1 — For the bridge class (A=I, B=(1,1)^T, x0=(d0,d0), w in {-1,1}^T, |u_t| <= u_b,…

status: survived-falsifier
- statement: For the bridge class (A=I, B=(1,1)^T, x0=(d0,d0), w in {-1,1}^T, |u_t| <= u_b, cost ||x_T||_1), every closure set R <= {1..T} with chronological blind-block lengths L_0..L_k (the successive differences of [0]+sorted(R)+[T]) satisfies the exact closed form V(R) = max(|D|*T, f_{L_k}(...f_{L_0}(2|d0|)...)) with f_L(x) = max(x - 2*u_b*L, 0) + |S|*L on x >= 0, S = e1+e2, D = e1-e2; e.g. V({1,3}) = 10 at T=4, e=2, u_b=1, d0=0.
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-2 — The published full-information closed form V(full) = max(max(|S|, 2|d0| -…

status: refuted
- statement: The published full-information closed form V(full) = max(max(|S|, 2|d0| - (2*u_b - |S|)*T), |D|*T) is valid only while |S| <= 2*u_b; beyond it the true sum part is the pursuit iterate f_1^T(2|d0|) with f_1(x) = max(x - 2*u_b, 0) + |S| — e.g. at (d0, e, u_b, T) = (0, 2, 1, 2) the exact oracle returns V(full) = 6 while the published form gives 4.
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-3 — In the bridge class under full information (R = {1,...,T}) the best affine…

status: survived-falsifier
- statement: In the bridge class under full information (R = {1,...,T}) the best affine decision rule over the full observed prefix, u_t = alpha_t + sum_{tau<t} b_{t,tau}*w_tau with |u_t| <= u_b on every path, attains exactly the adaptive optimum V_aff = max(f_1^T(2*|d0|), |D|*T) with f_1(x) = max(x - 2*u_b, 0) + |S|, so the affine-to-exact gap is identically zero (e.g. V_aff = 6 = exact at (d0, e, u_b, T) = (0, 2, 1, 2) where the published linear form gives 4), the wedge excess (exact - published, nonzero exactly inside W = {|S| > 2*u_b, 2*|d0| < 2*u_b, T >= 2}) measures the published form's deficit and not an affine restriction cost, and the planned half-identity V_aff = max(max(|S|, 2*|d0| - (2*u_b - |S|)*T), |D|*T) is impossible because the published form lies strictly below the exact optimum inside W while V_aff >= V_exact for any strategy subclass.
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-4 — For the bridge class with a single closure R = {r} the blind-block composition…

status: refuted
- statement: For the bridge class with a single closure R = {r} the blind-block composition (h-auto-1) yields the exact closed form V({r}) = max(2*|d0| + (|S| - 2*u_b)*T, |S|*T - 2*u_b*(T - r), |S|*(T - r), |D|*T), hence the optimal closure moment is an integer r in [1, T-1] nearest the crossing r* = 2*u_b*T/(2*u_b + |S|) of the two r-dependent terms — early-biased when |S| > 2*u_b, late-biased when |S| < 2*u_b, balanced exactly at |S| = 2*u_b, with all-r ties whenever a floor (2*|d0| + (|S| - 2*u_b)*T or |D|*T) dominates the crossing value |S|^2*T/(2*u_b + |S|) — giving the explicit one-closure information gain 2*u_b*|S|*T/(2*u_b + |S|) over V(empty) when the sum part dominates, and refuting bd 8y2's expected balanced-blocks shape (e.g. at (d0, e, u_b, T) = (0, 2, 1, 3): V({1}) = 8 < V({2}) = 10).
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-5 — For the bridge class with a single closure R = {r}, r in [1, T-1], the survived…

status: refuted
- statement: For the bridge class with a single closure R = {r}, r in [1, T-1], the survived one-closure form V({r}) = max(2|d0| + (|S|-2u_b)*T, |S|*T - 2u_b*(T-r), |S|*(T-r), |D|*T) = max(c, g(r)) — with c = max(2|d0| + (|S|-2u_b)*T, |D|*T) r-independent and g(r) = max(|S|*(T-r), |S|*T - 2u_b*(T-r)) a V-shaped valley with kink r* = 2u_b*T/(2u_b+|S|) and bottom X = |S|^2*T/(2u_b+|S|) — yields the corrected argmin law replacing h-auto-4's dead nearest-integer rule: letting Gmin = min over integer r in [1,T-1] of g(r) (equal to X + 2u_b*(1-r*) if r* < 1, X + |S|*(r*-(T-1)) if r* > T-1, X if r* is an integer in [1,T-1], and X + min(|S|*frac(r*), 2u_b*(1-frac(r*))) otherwise), if c >= Gmin the argmin is the plate {r : g(r) <= c} with V_min = c (floor docking — a plate, not all-r ties; the whole domain exactly in the d0-active regime 2|d0| >= 2u_b*T or under a dominating |D|*T), while if c < Gmin the argmin is decided by comparing BOTH valley sides at the integers adjacent to r* — left penalty |S|*frac(r*) vs right penalty 2u_b*(1-frac(r*)), winner = smaller penalty, with r* integer -> {r*}, r* < 1 -> {1}, r* > T-1 -> {T-1} (e.g. at (d0, e, u_b, T) = (0, 7/2, 1, 6): r* = 4/3, penalties 7/3 vs 4/3, argmin {2} with V = 34 < 35 at the nearest r = 1) — and the value of information is V(empty) - V_min = V(empty) - max(c, Gmin), which in the interior sum-dominated regime (2|d0| <= 2u_b*T, c <= X, |D|T <= X, 1 <= r* <= T-1) equals the continuous gain minus the exact rounding loss, 2u_b*|S|*T/(2u_b+|S|) - min(|S|*frac(r*), 2u_b*(1-frac(r*))) (8 = 28/3 - 4/3 at the same point).
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-6 — In the bridge class the path-committed max-min value — the adversary fixes a…

status: survived-falsifier
- statement: In the bridge class the path-committed max-min value — the adversary fixes a full disturbance path W first and the controller then minimizes ||x_T||_1 over control plans knowing W — has the exact closed form V_mm = max(max(2|d0| + (|S|-2u_b)*T, 0), |D|*T), because per path the plan enters only through U = sum u_t (s_T = 2d0 + 2U + S*W and d_T = D*W is control-free), and this quantity equals exactly the r-independent term c of the one-closure form, making it a universal floor of the whole ladder V(R) >= V_mm for every closure set R (from the elementary fold inequality f_a(f_b(x)) <= f_{a+b}(x) per block pair) — so the max-min asymmetry is quantitative on the bridge class: the blind gap V(empty) - V_mm equals min(2u_b*T - 2|d0|, |S|*T) whenever 2|d0| <= 2u_b*T and |D|*T <= max(2|d0| + (|S|-2u_b)*T, 0), and is 0 in the d0-active regime, under a binding |D|*T floor, and identically for mixed E (e.g. at (d0, e, u_b, T) = (0, 1, 1, 4) aligned: V_mm = 0, V(empty) = 8, gap 8 = min(8, 8); mixed-E sweep: V_mm = |D|*T = V(empty), gap 0).
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-7 — On the bridge class (A=I, B=(1,1)^T, x0=(d0,d0), |u_t|<=u_b, cost = worst-case…

status: refuted
- statement: On the bridge class (A=I, B=(1,1)^T, x0=(d0,d0), |u_t|<=u_b, cost = worst-case ||x_T||_1, S=e1+e2, D=e1-e2) with one closure R={r}, the argmin of the fold V({r}) = max(c, g(r)) over r in [1, T-1], with c = max(2|d0| + (|S|-2u_b)*T, |D|*T) and the V-shaped valley g(r) = max(|S|*(T-r), |S|*T - 2u_b*(T-r)), equals exactly the plateau set {r in [1,T-1] : g(r) <= V_min} at level V_min = max(c, Gmin) (Gmin = the four-case integer minimum of g at the kink r* = 2u_b*T/(2u_b+|S|)), and this argmin is the whole domain [1, T-1] if and only if c >= W := max(g(1), g(T-1)) = max(|S|*(T-1), |S|*T - 2u_b), i.e. exactly in one of three regimes: d0-active (2|d0| >= 2u_b*T), floor-dominated (|D|*T >= W), or interior plateau (2|d0| < 2u_b*T AND |D|*T < W AND 2|d0| + (|S|-2u_b)*T >= W) - the third regime replacing the refuted X = |S|^2*T/(2u_b+|S|) threshold of h-auto-5.
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)

## h-auto-8 — For every closure set R subset of {1,...,T} with blind-block lengths…

status: survived-falsifier
- statement: For every closure set R subset of {1,...,T} with blind-block lengths L_0,...,L_k (successive differences of [0]+sorted(R)+[T], sum L_i = T), the survived block composition unfolds exactly into the tail-sum form V(R) = max(|D|*T, 2|d0| + (|S|-2u_b)*T, max_{0<=j<=k} [ |S|*L_j + (|S|-2u_b)*(L_{j+1}+...+L_k) ]), reducing the k-closure scheduling problem (bd 8y2 acceptance a) to minimizing, over all compositions of T into k+1 blocks, a maximum of at most k+2 linear forms.
- falsifier: (see journal verdicts; pre-rebuild hypothesis)
- vocabulary: (see statement)
- origin: run:auto-cycle
- formalization: (open)
## h-sched-argmin-3 — Scheduling argmin law, third repair: plateau iff W <= V_min

status: survived-falsifier
- statement: For the bridge class (A = I, B = (1,1)^T, x0 = (d0, d0), w in {-1,+1}^T, |u_t| <= u_b, cost ||x_T||_1) with one closure R = {r}, r an integer in [1, T-1]: let S = e1+e2, D = e1-e2, c = max(2|d0| + (|S|-2*u_b)*T, |D|*T), g(r) = max(|S|*(T-r), |S|*T - 2*u_b*(T-r)), Gmin = min over integer r in [1, T-1] of g(r), V_min = max(c, Gmin), W = max(g(1), g(T-1)). Then (i) V({r}) = max(c, g(r)) for every integer r; (ii) argmin_r V({r}) = {r : g(r) <= V_min} (the plateau); (iii) the plateau is the whole domain if and only if W <= V_min.
- falsifier: one instance on the frozen grid where the exact per-path LP argmin of V({r}) leaves the plateau, or where plateau-whole-domain and W <= V_min disagree in either direction
- vocabulary: closure moment r; blind block; V({r}) = guaranteed cost with one closure; floor c; valley g(r); plateau; W = valley edge value; Gmin = integer valley bottom
- origin: h-auto-5/7 lineage: body predicates clean twice, iff claims died twice on narrow integer domains (Gmin = W at T = 2, 3); successor per briefing-4 arithmetic check 75/75 on frozen judge data; logical repair = the max of a V-shaped valley over an integer interval sits at an endpoint
- formalization: ROUTE IDENTIFIED (2026-10-11, see "Proof route" below); Step 1 rests on the Lean-proven blocks_sum_lower, Step 2 is the only new formalization (per-block pursuit bound), Steps 3-4 are finite arithmetic

### Proof route for this card (identified 2026-10-11)

- **Step 1 - the lower bound (Lean-proven already):** V({r}) >= max(c, g(r))
  is the k = 1 instance of the blind-block composition lower bound
  (`blocks_sum_lower`, sorry-free in TwoDDraft.lean); the expansion of the
  fold f_{T-r}(f_r(2|d0|)) into the four-term max is finite arithmetic.
- **Step 2 - the upper bound (the only new formalization):** V({r}) <=
  max(c, g(r)) by exhibiting a strategy: the centering (pursuit) control
  applied block-wise on the two blind blocks [0, r] and [r, T]. Lean route:
  extend the existing `clamp_sat`/`sRunN` machinery (proven for the upper
  half of V(full)) to the one-closure information structure. Alternative
  route: the A4-style LP-duality + parametric argument (exhibit a dual
  feasible solution attaining the fold value); pick whichever formalizes
  shorter.
- **Step 3 - the plateau-argmin law (finite arithmetic):** given (i),
  argmin_r max(c, g(r)) = {r : g(r) <= max(c, Gmin)} is interval reasoning
  on a V-shaped function with the four-case integer-bottom formula for
  Gmin; no new heavy mathematics (linarith/nlinarith scale).
- **Step 4 - the whole-domain criterion (one arithmetic lemma):** max of a
  V-shaped function over the integer interval [1, T-1] sits at an endpoint,
  hence max_r g(r) = W; combined with Step 3 this yields the iff.
- **Dependency structure:** Step 2 is the critical path; Steps 3-4 are
  self-contained arithmetic once (i) holds. The A4 collision check passed
  (the school fixes the schedule a priori), so no priority conflict.
