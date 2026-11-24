# Reading proposal: Dmitruk A5 (dissertation 2022)

meta: Н. М. Дмитрук, «Оптимальное управление динамическими системами и их группами
в условиях неопределенности», диссертация (corpus label: 2022). The PDF is an
EXCERPT: 41 pages, printed pp. 37–77, no title page / TOC / publication list; it
contains Chapter 2 «Оптимальное гарантированное управление линейными системами с
возмущениями» (printed p. 37) and the first page of §2.3 (printed p. 77, cut off).
SHA256 verified: 94d6b70331a4682b05b0e828e3fd346e4045f8b659075fd950a4c81471c71a66.
Anchor convention: PDF page k = printed page k+36; below I give PDF page with
printed page in parentheses.

Structure map of the excerpt:
- §2.1 Общая схема построения стратегий — printed 37–40 (task family: linear
  terminal Mayer-criterion problem §2.2; minimum-impulse problems §2.3 one-closure
  continuous / §2.4 multiclosure discrete; state-delay problem §2.5; real-time §2.6;
  theorems 2.5, 2.7, 2.8, 2.12 announced but NOT in this excerpt).
- §2.2.1 Оптимальная гарантирующая программа — printed 41–44 (Lemma 2.1, LP (2.10)).
- §2.2.2 Многократно замыкаемая стратегия управления — printed 44–47 (Defs 2.3–2.8).
- §2.2.3 Допустимая и оптимальная стратегии — printed 47–51 (closing sets (2.17),
  Bellman function (2.21), Bellman equation (2.24), inequality (2.26)).
- §2.2.4 Оптимальные начальные программы как задачи ЛП — printed 51–54 (Thm 2.1).
- §2.2.5 Полиэдральные параметрические представления множеств замыкания —
  printed 54–58 (Lemma 2.4 Farkas, Thm 2.2 exact representation).
- §2.2.6 Алгоритм 2.1 (optimal strategy, exact) — printed 58–60 (Thm 2.3).
- §2.2.7 Вычислительные аспекты (suboptimal strategies) — printed 60–75
  (parametric LP, Lemma 2.5, Algorithm 2.2, Thm 2.4, Algorithms 2.3–2.4,
  Утверждение 2.1, certification problem (2.65)–(2.67)).
- §2.2.8 Анализ улучшения оптимального значения при увеличении числа моментов
  замыкания — printed 75–77 (THE scheduling-adjacent section).
- §2.3 (минимизация полного импульса) — starts printed 77, not in excerpt.

Relation to A4: this is the same construction as A4 (journal paper), but with the
EXACT polyhedral pipeline (§2.2.5–2.2.6) before the approximating one (§2.2.7 ≈ A4),
plus material absent from A4: Theorem 2.3 (along-trajectory monotonicity),
Утверждение 2.1 (two-sided a posteriori certificate), §2.2.8 (value-improvement
bounds under adding closure moments). Pink/magenta editorial notes in the PDF show
it is a working draft (e.g., Замечание 2.10).

## Theorem blocks

### thm-a5-1: Theorem 2.1 — existence of the optimal multiclosure strategy + one-LP-per-closure reduction
- statement: For the linear terminal guaranteed-control problem (2.1)–(2.4)
  `x(t+1) = Ax(t) + Bu(t) + Mw(t)`, box `U`, `W = {‖w‖_∞ ≤ w_max}`, polyhedral
  `X_T`, closure moments `T_1 < … < T_N`, under Assumption 2.2 (first closing set
  nonempty; `x_0` can be driven into `X_1`), the optimal strategy `π^0_N(0, x_0)`
  exists and its optimal initial program `u^0_0(·|x_0)` is the solution of ONE LP
  (2.32) at `j = 0`: `V_j(x_j) = min_{u_j,α} α` s.t.
  `Σ_{t∈Δ_j} G_j D_j(t) u_j(t) − λ_{j+1} α ≤ g_{j+1} − γ_j − G_j x_j`,
  `u_min ≤ u_j(t) ≤ u_max`, with `G_j = P_{j+1} A^{T_{j+1}−T_j}` (2.33) and the
  worst-case row estimates `γ_{ji} = w_max Σ_{t∈Δ_j} ‖p^⊤_{j+1,i} A^{T_{j+1}−t−1} M‖_1`
  (2.34); the optimal value is `V_0(x_0) = α^0`. Same LP re-solved at each realized
  closure state (Thm 2.3 part 1).
- conditions: linear stationary discrete system, polyhedral data, fixed schedule,
  Assumption 2.2 (initial feasibility).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 17 (printed 53) — «Тогда существует
  оптимальная стратегия π^0_N(0, x_0), для которой оптимальная начальная программа
  u^0_0(·|x_0) находится как решение задачи линейного программирования (2.32) при
  j = 0. При этом оптимальное значение задачи (2.1)–(2.4) равно V_0(x_0) = α^0.»
- our-relevance: the value oracle `V(R)` for our bridge class is exactly this LP;
  A5 states it for the exact (non-approximated) closing sets, so `V(R)` is
  LP-exact, not approximation-limited — the cleanest possible oracle for our
  scheduling law to consume.

### thm-a5-2: Theorem 2.2 — EXACT polyhedral parametric representation of closing sets, affine in α, λ_j ≥ 0
- statement: Under condition 1) of Assumption 2.2, for every `j = 1,…,N` the
  closing level set is the polyhedron `X_j(α) = {x ∈ R^n : P_j x ≤ g_j + λ_j α}`,
  `α ∈ R` (2.36), where `P_j = Y_j G_j`, `λ_j = Y_j λ_{j+1} ≥ 0`,
  `g_j = Y_j (g_{j+1} − γ_j) − Σ_t P_j D_j(t) u_min + Σ_t V_j(t)(u_max − u_min)`
  (2.37), base case `P_{N+1} = (−H; H; c^⊤)`, `λ_{N+1} = (0; 0; 1)` (2.38), and the
  rows of `Y_j`, `V_j(t)` form a fundamental system of solutions of the cone
  `(G_j D_j(t))^⊤ y_j + v_j(t) ≥ 0`, `y_j ≥ 0`, `v_j(t) ≥ 0` (2.39) (Farkas
  extremal rays, Lemma 2.4). Hence `λ_j ≥ 0` and `X_j(α_1) ⊆ X_j(α_2) ⊆ X_j` for
  `α_1 < α_2`: level sets are nested, monotone in the information/value parameter.
  Feasibility threshold: LP (2.47) `α_{j,min} = min α` s.t.
  `P_{j+1}x − λ_{j+1}α ≤ g_{j+1} − γ_j` decides whether closing sets are empty
  (infeasible), never empty (unbounded), or empty exactly for `α < α_{j,min}`.
- conditions: exact scheme; the fundamental solutions are finite in number but the
  step suffers the "curse of dimensionality" (Замечание 2.3).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 19 (printed 55) — «множество
  замыкания X_j(α) является выпуклым многогранником вида X_j(α) = {x ∈ R^n :
  P_j x ≤ g_j + λ_j α}, α ∈ R»; p. 21 (printed 57) — «Поскольку Y_j содержит
  только положительные элементы, рекуррентно установим, что λ_j = Y_j λ_{j+1} ≥ 0.»;
  threshold (2.47): p. 22 (printed 58) — «При α < α_{j,min} имеем X_j(α) = ∅.»
- our-relevance: A4's Утверждение 1 gave this only for OUTER APPROXIMATIONS; the
  dissertation proves it EXACTLY, by extremal rays. The affine-in-α right-hand
  sides with `λ_j ≥ 0` are the structural basis of our wedge/plateau claims; the
  α-threshold `α_{j,min}` is a first, trivial case of a "kink/plateau" in the
  information parameter. For `A = I, B = (1,1)^⊤` the recursion (2.37)–(2.39) is a
  concrete route to closed-form `P_j, g_j, λ_j` — hence closed-form `V(R)`.

### thm-a5-3: Theorem 2.3 — monotone non-increase of the guaranteed value along the realized trajectory
- statement: Under Assumption 2.2, along ANY control process realized under the
  optimal strategy, all LPs (2.32) at the realized states `x_j = x*(T_j)` are
  solvable, deliver `V_j(x*(T_j)) = α^0_j(x*(T_j))`, and
  `V_0(x_0) ≥ V_1(x*(T_1)) ≥ … ≥ V_N(x*(T_N))`: the guarantee never deteriorates
  as measurements arrive; moreover each realized Bellman value is not worse than
  the previous one because `x*(T_j) ∈ X_j(α^0_{j−1}(x*(T_{j−1})))` implies
  `V_j(x*(T_j)) ≤ α^0_{j−1}(x*(T_{j−1})) = V_{j−1}(x*(T_{j−1}))`.
- conditions: optimal strategy, Assumption 2.2, realized states stay in closing
  sets by admissibility.
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 23 (printed 59) — «При этом
  V_0(x_0) ≥ V_1(x*(T_1)) ≥ … ≥ V_N(x*(T_N)).»; p. 24 (printed 60) — «по ходу
  процесса управления стратегией гарантированное значение критерия качества задачи
  не возрастает.»
- our-relevance: a monotonicity theorem EXISTS in the school, but in the
  time/state direction (value improves as scheduled measurements arrive), not in
  the schedule-refinement direction. Distinct from our OC → RO(k) → DP ladder
  claim; useful supporting lemma: the value we promise at `t = 0` is conservative
  for all later decisions — relevant to how our law prices future closure options.

### thm-a5-4: Lemma 2.5 + derivative formula — parametric-LP basis stability: piecewise-affine support values with explicit breakpoints
- statement: For the canonical parametric LP `f(α) = min_y (b + λα)^⊤ y`,
  `G^⊤y = p, y ≥ 0` (2.55), if the optimal basic solution at `ᾱ` is doubly
  nondegenerate, then on an interval `]α_*, α*[` the basis (and solution) is
  constant, with endpoints given explicitly by ratio formulas (2.57)
  `α_* = max_i (b_i − g_i^⊤ G_b^{−1} b)/(g_i^⊤ G_b^{−1} λ_b − λ_i)`,
  `α* = min_i …` over the signed index sets `I^∓`. On the interval,
  `df(α)/dα ≡ λ^⊤ y^0(α)` and `f(α) = f(ᾱ) + λ^⊤ y^0(α)(α − ᾱ)`. Since the number
  of bases is finite, `f` is piecewise linear with finitely many linearity
  intervals; Algorithm 2.2 walks the breakpoints `α_max = α^1 > … > α^{K+1} = α_min`
  and detects degenerate kinks (`λ^⊤y^0(α^k) = λ^{k−1}` ⇒ interval extends).
- conditions: LP duality framework; degenerate cases routed: unbounded below ⇒
  correct `α_min` (closing set empty below), infeasible ⇒ direction `p̄_{ji}`
  violates Assumption 2.3 and is deleted (unbounded closing set along it).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 29 (printed 65) — «существует
  интервал ]α_*, α*[ значений параметра α, ᾱ ∈ ]α_*, α*[, для которого базисное
  решение y^0(α) с базисом I^0_b(ᾱ) остается оптимальным: y^0(α) ≡ y^0(ᾱ)»;
  p. 30 (printed 66) — «df(α)/dα ≡ λ^⊤y^0(α), α ∈ ]α_*, α*[.» and «Поскольку число
  базисов в задачах линейного программирования конечно, число указанных интервалов
  также конечно.»
- our-relevance: the full analytic machinery for "value is piecewise-affine in a
  scalar parameter, constant on certifiable intervals" — the template our plateau
  theorem needs. A5 goes beyond A4 by handling degeneracy explicitly and by giving
  closed-form interval endpoints (2.57). Remaining gap for us: our schedule
  parameter `R` is discrete/integer and enters data combinatorially, not only the
  RHS — the transfer still has to be built.

### thm-a5-5: Theorem 2.4 — approximating polyhedra keep the affine-in-α representation with piecewise-linear supports
- statement: Given normals `p̄_{ji}, i = 1,…,l_j` (unit vectors satisfying dual
  feasibility, Assumption 2.3), the outer approximations `X̄_j(α)` (2.48) admit
  `X̄_j(α) = {x ∈ R^n : P̄_j x ≤ ḡ_j + λ̄_j α}, α ∈ [ᾱ_{j,min}, α_max]` (2.61),
  where each row `i` is repeated `K_{ji}` times with
  `ḡ^k_{ji} = f^k_{ji} + c_{ji}`, `λ̄^k_{ji} = λ^k_{ji}` — the pieces of the
  piecewise-linear support functions `f_{ji}(α) = min_{k} {λ^k_{ji} α + f^k_{ji} +
  c_{ji}}` (2.60) produced by Algorithm 2.2 on the dual (2.54). Recommended
  normals: previous-level rows `p̄_{j+1,i} A^{T_{j+1}−T_j}` plus Sobol
  quasi-random points on the unit sphere.
- conditions: condition 1) of Assumption 2.2; Assumption 2.3 (dual feasibility of
  every kept normal); `X_{N+1}(α)` not approximated (`V̄_N = V_N`).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 33 (printed 69) — «при условии
  выбора векторов p̄_{ji}, i = 1, …, l_j, удовлетворяющих предположению 2.3, для
  аппроксимации X̄_j(α) множества замыкания X_j(α) имеет место представление
  X̄_j(α) = {x ∈ R^n : P̄_j x ≤ ḡ_j + λ̄_j α}, α ∈ [ᾱ_{j,min}, α_max]»; Sobol:
  p. 32 (printed 68) — «сгенерировать остальные векторы на основе квазислучайных
  последовательностей Собола [112] для обеспечения равномерного покрытия в
  единичной гиперсфере.»
- our-relevance: this is A4's Утверждение 1 + thm-a4-5 in their fuller form —
  confirms the approximation layer sits ON TOP of the exact representation, and
  every approximating object remains affine in α. Nothing here restricts which
  schedules may be used: the construction is uniform in `T_1 < … < T_N`.

### thm-a5-6: Утверждение 2.1 — two-sided a posteriori certificate for the suboptimal strategy
- statement: With outer approximations, the suboptimal value satisfies
  `V̄_0(x_0) ≤ V_0(x_0)` (2.64) (outer approximation relaxes the problem). Let
  `ᾱ = max_{w∈W} V_{N+1}(x(T|0, x_0, π̄_N, w))` (2.65) be the actual guaranteed
  cost of the suboptimal strategy along trajectories. If `ᾱ < +∞`, then:
  1) the gap of the computed value is bounded by `ᾱ − V̄_0(x_0)`
  (`V̄_0(x_0) ≤ V_0(x_0) ≤ ᾱ`); 2) the online LPs (2.63) remain solvable at every
  realized `x*(T_j)`, i.e., the suboptimal strategy is guaranteed to run to
  completion. If `ᾱ = +∞` (some disturbance drives the trajectory out of a closing
  set), the fallback is to rebuild approximations for the inflated disturbance set
  `W_δ = {w : ‖w‖ ≤ w_max + δ}` with small `δ > 0`.
- conditions: suboptimal strategy from Algorithm 2.4; (2.65) solvable with
  finite value. (2.65) is a convex maximization over a polytope — solved via
  accumulated-disturbance variables and NLP (trust-region in Приложение А).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 37 (printed 73) — «1) оптимальное
  значение V̄_0(x_0) задачи (2.63) при j = 0 отклоняется от оптимального значения
  V_0(x_0) на величину не более чем ᾱ − V̄_0(x_0)»; (2.64): p. 36 (printed 72);
  fallback: p. 37 (printed 73) — «Задачу построения оптимальной стратегии решать
  для "возмущенного" множества W_δ = {w ∈ R^p : ‖w‖ ≤ w_max + δ}»
- our-relevance: the school's own certification pattern = lower bound (LP
  relaxation) + upper bound (worst-case simulation) + gap — exactly the shape our
  judges could certify a schedule `R` with: `V̄(R) ≤ V(R) ≤ ᾱ(R)`. The `W_δ`
  inflation is their infeasibility fallback (matches A4 fact-a4-4).

### thm-a5-7: §2.2.8 — value-improvement bound when ADDING one closure moment (refinement monotonicity, informally)
- statement: Compare the optimal `N`-closure strategy `π^0_N` (closures
  `T_1 < T_2 < … < T_N`) with the optimal `(N−1)`-closure strategy `π^0_{N−1}`
  (closures `T_2 > 1, …, T_N`), i.e., ADD one closure `T_1 ∈ (0, T_2)` "in front".
  Build the feasible `N`-closure strategy (2.69)
  `π_N(0, x_0) = {ũ^0_0(·|x_0); π^0_{N−1}(T_1, x_1), x_1 ∈ X(T_1|0, x_0, ũ^0_0)}`
  by restricting the `(N−1)`-optimal initial program to `Δ_1`. Its guaranteed
  quality is `V_0(x_0|π_N) = max_{w_0} V_1(x(T_1|0, x_0, ũ^0_0, w_0)) =
  max_{x∈X(T_1|0,x_0,ũ^0_0)} V_1(x)`. Then
  `V_0(x_0|π^0_N) ≤ V_0(x_0|π_N) ≤ V_0(x_0|π^0_{N−1})`, so with
  `δ_min := V_0(x_0|π^0_{N−1}) − V_0(x_0|π_N) ≥ 0` one has the improvement bound
  `V_0(x_0|π^0_{N−1}) − V_0(x_0|π^0_N) ≥ δ_min`: the gain of adding the closure is
  at least the (computable) quality of the glued strategy's deficit. The same
  reasoning covers the OC → RO(1) rung (program vs one-closure strategy). Cases
  `δ_max = 0` (upper bound from [43-А]) certify that more closures give NO gain.
  Status: stated as "obvious", no formal proof environment, prepend-direction
  scheme only.
- conditions: fixed `T_2,…,T_N` with `T_2 > 1`; the `(N−1)`-strategy already
  constructed (representations (2.36) known for `j ≥ 2`); only `V_1` for the new
  schedule needs computing by the general rule (2.24).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 41 (printed 77) — «Очевидно,
  выполняются неравенства V_0(x_0|π^0_N) ≤ V_0(x_0|π_N) ≤ V_0(x_0|π^0_{N−1}).» and
  «Положим δ_min := V_0(x_0|π^0_{N−1}) − V_0(x_0|π_N) ≥ 0. Тогда имеет место
  следующая оценка улучшения оптимального значения задачи (2.1)–(2.4) при
  добавлении (слева) одного момента замыкания: V_0(x_0|π^0_{N−1}) − V_0(x_0|π^0_N)
  ≥ δ_min.»; OC→RO(1) extension: p. 40 (printed 76) — «Все последующие рассуждения
  справедливы и для сравнения качества управления оптимальной программой u^0(·) и
  оптимальной однократно замыкаемой стратегией π^0_1(0, x_0)»; quality formula:
  p. 40 (printed 76) — «V_0(x_0|π_N) = max_{w_0∈W_0} V_1(x(T_1|0, x_0, ũ^0_0,
  w_0)) = max_{x∈X(T_1|0,x_0,ũ^0_0)} V_1(x).»
- our-relevance: THE closest prior art to our ladder monotonicity. The adjacent-rung
  inequality RO(N) ≤ RO(N−1) for schedules differing by one prepended closure is
  already claimed here (and its two-step instance is (2.26)); what is NOT done:
  no formal proof, no induction to arbitrary refinements, no DP endpoint, no
  closed forms, no plateau/zero-gain theory beyond referring to [43-А] `δ_max = 0`,
  and nothing for specific instances. Our formalization + closed forms + scheduling
  law remain new; the bare monotonicity statement does not.

## Fact blocks

### fact-a5-1: The full ladder OC — N-closures — DP is articulated, qualitatively, on one page
- statement: If every time instant is a closure moment, the multiclosure strategy
  coincides with the DP (optimal feedback) strategy; the optimal guaranteeing
  program is the limit case with NO closure moments; an `N`-closure strategy,
  `0 < N < T − 1`, is a compromise between quality of the process and effort of
  constructing the solution. The multiclosure value is the nested alternating
  min–max `V_0(x_0) = min_{u_0} max_{w_0} … min_{u_N} max_{w_N} c^⊤x(T)` versus
  the program value `J(x_0) = min … min max … max c^⊤x(T)`; the minimax inequality
  gives the endpoint two-step bound `V_0(x_0) ≤ J(x_0)` (2.26) — so far the ONLY
  quantifier-order result. Closing sets are exactly the domains of the Bellman
  function: `X_j = {x : V_j(x) < +∞}` (Замечание 2.2).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 3 (printed 39) — «Если принять, что
  все моменты времени из промежутка управления являются моментами замыкания, то
  многократно замыкаемая стратегия, очевидно, совпадает со стратегией
  динамического программирования (оптимальной обратной связью). В свою очередь,
  можно считать, что оптимальная гарантирующая программа является предельным
  случаем при отсутствии моментов замыкания.»; (2.26): p. 15 (printed 51) —
  «Принимая во внимание неравенство max min f ≤ min max f … можно заключить, что
  V_0(x_0) ≤ J(x_0).»; Замечание 2.2: p. 14 (printed 50).
- our-relevance: the school already NAMES all three ladder endpoints but only
  quantifies two adjacent pairs ((2.26) and thm-a5-7); the DP rung has no value
  computation anywhere in the excerpt — our measured DP endpoint stays new.

### fact-a5-2: Optimal placement of closure moments is EXPLICITLY declared out of scope; position-dependence is delegated to [43-А]
- statement: §2.2.8 opens: improvement is possible both by the NUMBER and by the
  POSITION of closure moments; [43-А] obtained upper and lower bounds for
  `J(x_0) − V_0(x_0|π^0_1)` (one closure) and showed the value and bounds depend
  on the position `T_1`. Then: «Вопрос об оптимальном положении моментов замыкания
  в диссертации не исследуется.» — the dissertation stops at improvement
  ESTIMATES for increasing the number of closures. Interest is declared in
  `δ_max = 0` cases proving NO improvement from extra closures.
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 39 (printed 75) — «Таким образом,
  улучшение значения критерия качества возможно как за счет выбора числа моментов
  замыкания, так и за счет выбора их положения на Δ. Вопрос об оптимальном
  положении моментов замыкания в диссертации не исследуется.»; δ_max = 0:
  p. 41 (printed 77) — «Представляют интерес случаи, когда δ_max = 0, что
  позволяет установить отсутствие улучшения при увеличении числа моментов
  замыкания.» [Note: which of A1–A4 corresponds to [43-А] cannot be verified from
  this excerpt — the publication list is not included; topically it matches a
  one-closure value-bounds paper (cf. A2). Requires verification.]
- our-relevance: explicit written license for our scheduling law — the school's
  fullest text declines the very question our law answers; and their own
  `δ_max = 0` case is exactly our plateau/zero-gain phenomenon, flagged but not
  developed.

### fact-a5-3: Feasibility depends on the schedule; ε-inflation fallback exists
- statement: The choice of the SET of closure moments (their number and position)
  can decide EXISTENCE of a solution in the strategy class: «выбор другого набора
  моментов замыкания (изменение их количества и расположения) может привести к
  существованию решения в классе стратегий управления» — examples are relegated to
  Приложение А (not in this excerpt). When approximations make continuation
  impossible (`ᾱ = +∞`), rebuild with inflated `W_δ`.
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 18 (printed 54) — quote above;
  fallback: p. 37 (printed 73).
- our-relevance: schedule-dependent feasibility (not only value) is acknowledged
  in one sentence, no theory. Supports our treatment of the law as selecting among
  genuinely different feasible strategy classes; our infeasibility fallback should
  cite/compare `W_δ` (same as A4 fact-a4-4).

### fact-a5-4: Computational economics: exact scheme is exponential (DP curse), approximated scheme is offline-once — a deliberate contrast with the Gabasov school [11]
- statement: The exact algorithm's cost concentrates in building fundamental
  solutions of the cone system (2.39) at step 2 — «проклятие размерности» — and
  can be untenable already at `N > 1`; hence the approximating track. In [11]
  (iterative approach) approximations are recomputed for unknown α-values,
  including DURING the process; in the dissertation all closure-set computations
  are done BEFORE the process and characterize the sets for ALL α at once, so
  online only one LP per closure is solved. The comparison is stated as the
  dissertation's advantage over [11; 33; 34] (real-time suitability).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 23 (printed 59) — «Основная
  вычислительная сложность алгоритма 2.1 приходится на шаг 2, где проявляется
  "проклятие размерности", связанное с применением динамического программирования.»;
  p. 39 (printed 75) — «Однако в диссертации все вычисления, связанные с
  аппроксимациями множеств замыкания, проводятся до начала процесса управления и
  позволяют полностью охарактеризовать эти множества при всех значениях параметра
  α.» (contrast with [11]: p. 38, printed 74).
- our-relevance: the offline/online split and "pay once, query all α" economics
  are the school's design invariants; our judges/gates inherit the same shape.
  Also explains WHY they never search over schedules: each schedule `R` costs one
  offline pass, and no parametric theory in `R` exists — precisely the opening our
  law fills.

### fact-a5-5: The adversary/certification side is the computationally hard side (convex maximization); dimension cut via accumulated disturbances
- statement: Computing the actual guaranteed cost `ᾱ` of a fixed suboptimal
  strategy, `ᾱ = max_w V_{N+1}(x(T|0, x_0, π̄_N, w))` (2.65), is convex-function
  maximization over a polytope — nonconvex, dimension `T·p`; reduced by
  accumulating effective disturbances per segment, `ξ_j = Σ_{t∈Δ_{j−1}}
  A^{T_j−t−1} M w(t)`, `ξ_j ∈ Ξ_j` (2.67), with `Ξ_j` approximated by outer
  polytopes/ellipsoids (upper bound on ᾱ) or penalized via the LP
  `ε(ξ_j) = min_{w,ε} {ε : Σ A^{T_j−t−1} M w(t) = ξ_j, ‖w‖_∞ ≤ w_max + ε}`;
  trust-region NLP used in the experiments. The min side, by contrast, is a
  polynomial LP.
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 37 (printed 73) — «Задача (2.65)
  является задачей максимизации выпуклой функции на выпуклом множестве.»;
  reduction: pp. 37–38 (printed 73–74) — «еще более существенное снижение
  размерности можно получить, если ввести переменные ξ_j ∈ R^n, которые
  аккумулируют действенные возмущения на интервалах Δ_{j−1}»; trust-region:
  p. 38 (printed 74).
- our-relevance: quantifies the max–min/min–max asymmetry computationally: in this
  school the min side is always LP-easy, the max side (certifying a guarantee) is
  convex maximization. Any analytic proof of our scheduling law faces the same
  asymmetry when verifying the worst case for a candidate `R`; their `ξ_j`
  accumulation is the standard dimension cut we should reuse in judges.

### fact-a5-6: A draft note attempts to approximate the JOINT (x, α) epigraph sets — the wedge object — and reports failure (editorial pink text)
- statement: Замечание 2.10 (pink/magenta working note in the PDF): one can
  approximate the sets `X_{jα} = {(x, α) ∈ R^{n+1} : P_j x − λ_j α ≤ g_j}` (2.68)
  — the epigraph/joint representation of closing level sets in (state, value)
  space; the note says: «Пока под вопросом, потому что в примере 1 дает всего
  3 вектора в матрицу P_1, в остальных случаях решаемая задача неограничена (не
  удалась λ)» — in Example 1 it yields only 3 normals for `P_1`, and otherwise the
  underlying problem is unbounded (λ extraction failed).
- anchor: A5_Дмитрук_диссертация_2022.pdf, p. 39 (printed 75), verbatim pink text
  as quoted above.
- our-relevance: the school itself tried to work with the polyhedral wedge in
  (x, α)-space — the exact object our wedge/plateau analysis targets — and stalled
  numerically. Direct evidence that a theory of these joint sets (our line) fills
  a hole the school personally ran into; also a calibration point: naive normal
  enumeration of `X_{jα}` degenerates.

## Landscape

- Relation to A4: A5(excerpt) ⊇ A4 in content. Identical model, definitions, and
  inequality (2.26) = A4's two-step result; §2.2.7 reproduces A4's approximating
  machinery (parametric LP, basis sensitivity, representation (2.61) ≈ A4's
  (2.13)). A5 adds: (i) the EXACT polyhedral pipeline (Thm 2.2 + Algorithm 2.1)
  absent from A4; (ii) Theorem 2.3 (along-trajectory monotonicity `V_0 ≥ V_1 ≥ …
  ≥ V_N`); (iii) Утверждение 2.1 two-sided certificates; (iv) §2.2.8 refinement
  improvement bounds `δ_min` — none of which A4 contains. Our A4 reading flagged
  «no refinement-monotonicity theorem in this school»: A5 §2.2.8 partially
  retracts that — an informal adjacent-rung monotonicity claim EXISTS here.
- Scheduling law (our line): no collision — the dissertation explicitly refuses
  schedule optimization (fact-a5-2), fixes `T_1 < … < T_N` a priori (p. 44,
  printed), and offers only one-step improvement estimates with computable
  `δ_min`. Our law (when to close, plateau filling) is the declared-open problem;
  `δ_min`/`δ_max` are the school's own prototype of the certificate our law
  should generalize from one prepended closure to arbitrary refinements and to
  closed forms.
- Ladder (OC → RO(k) → DP): endpoints named (fact-a5-1), two adjacent-rung
  inequalities present ((2.26) exact endpoint pair; thm-a5-7 for RO(N) ≤ RO(N−1)
  with prepend), full monotonicity never stated as a theorem, DP endpoint never
  computed. Our formal monotonicity + measured DP rung remain new; but our thesis
  must cite §2.2.8 and claim formalization/closed forms, NOT the bare inequality.
- Max–min asymmetry (our maxmin line): everything is one-sided min-max
  (guaranteeing); the only quantifier-order result is the minimax inequality
  behind (2.26); no Sion/von-Neumann gap analysis, no adversary-first formulation.
  The practical asymmetry is computational: min side = LP, max side = convex
  maximization cut down by `ξ_j` (fact-a5-5).
- Wedge: thm-a5-2/thm-a5-4 give level sets affine in α with `λ_j ≥ 0` and
  piecewise-affine support values with certified constancy intervals — the
  α-slice of our wedge language is fully built here; the joint (x, α) wedge
  (2.68) was attempted and abandoned (fact-a5-6). Our wedge/plateau results would
  complete a construction this school started and could not finish.
- Model match: same transfer conditions as A4 (L∞ ball vs `w ∈ {−1,+1}`;
  linear `c^⊤x(T)` vs our `‖x_T‖₁` via terminal ℓ₁-ball level sets (2.29) — the
  dissertation's `X_{N+1}(α) = {x : g_min ≤ Hx ≤ g_max, c^⊤x ≤ α}` takes any
  polyhedral terminal level body, so the pipeline transfers). The excerpt covers
  only §2.2; §2.3–2.6 (impulse minimization, delay, real-time) and Приложение А
  (numerics, incl. the examples A4 reports) are NOT in this PDF — page anchors
  above are all verified against pages present in the file.

## Open threads for our portfolio

1. Formalize thm-a5-7: turn the "Очевидно" chain `V_0(π^0_N) ≤ V_0(π_N) ≤
   V_0(π^0_{N−1})` into a theorem (and Lean candidate) for the bridge class,
   extending prepend-one-closure to arbitrary refinement by induction; cite A5
   §2.2.8 as the informal predecessor.
2. Closed-form `δ_min(R, T_1)` for the bridge class: `δ_min` is computable via
   one max over the reachable set of `V_1` — for `A = I, B = (1,1)^⊤` both
   objects should collapse to explicit piecewise-affine formulas; this is the
   analytic engine for our scheduling law (close at `T_1` iff `δ_min > 0`).
3. Zero-gain/plateau: develop the `δ_max = 0` case the school flags as
   "interesting" but does not analyze (fact-a5-2); identify the plateau intervals
   of the schedule-to-value map and certify them via Lemma 2.5's stability
   intervals transplanted from α to schedule data.
4. DP endpoint: compute `V(DP)` for a small bridge instance to close the ladder
   (fact-a5-1 names but never quantifies the top rung).
5. Wedge theory: the stalled (2.68) joint-set approximation (fact-a5-6) is a
   direct invitation — provide the structure theorem for
   `{(x, α) : P_j x − λ_j α ≤ g_j}` that their normal enumeration could not.
6. Certification pattern: adopt Утверждение 2.1's two-sided certificate
   (`LP lower bound` + `worst-case simulation upper bound` + gap) as the judge
   template for `V(R)` claims; reuse `ξ_j` accumulation (fact-a5-5) and, if
   needed, the `W_δ` fallback (fact-a5-3).
7. Obtain and read the missing parts: [43-А] (one-closure upper/lower bounds for
   `J − V_0(π^0_1)`, position dependence — the school's scheduling-adjacent paper)
   and the dissertation's Приложение А (numerics; identify whether it equals A4's
   Example 1 table). Also §2.3–2.6 if the full text becomes available — theorems
   2.5–2.12 announced on printed p. 39 are not in this excerpt. [requires
   verification: mapping of [43-А] to our A1–A4 labels]

## Verdict for our reading queue

Deep-read complete for the excerpt (Chapter 2, §2.2 — the fullest available text
of the multiclosure LP line). Answers to the four questions: (a) schedule
optimization — NO, explicitly out of scope with a quotable license sentence, only
one-step improvement estimates via `δ_min`; (b) refinement monotonicity —
PARTIALLY YES at "obvious" level: adjacent-rung inequality `RO(N) ≤ RO(N−1)` for a
prepended closure plus the two-step (2.26), no formal proof, no induction, no DP
endpoint — our ladder claim must be positioned as formalization + quantitative
closed forms; (c) max–min vs min–max — only the endpoint minimax inequality; the
asymmetry is computational (LP vs convex maximization, cut by `ξ_j`); (d)
closed-form values — none anywhere; only explicit γ-formulas, the recursion
(2.37), and stability intervals (2.57). Collision risk: LOW for the scheduling
law (the school declined that question in print); MODERATE for bare ladder
monotonicity (cite §2.2.8). Fuel: `δ_min`, Lemma 2.5 intervals, recursion (2.37),
the (2.68) wedge attempt, and the two-sided certification pattern. Priority:
high — pair with obtaining [43-А] and Приложение А.
