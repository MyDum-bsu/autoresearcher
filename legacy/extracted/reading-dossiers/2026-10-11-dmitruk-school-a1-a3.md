# Reading proposal: Dmitruk school line A1-A3

meta:
- A1: Н. В. Балашевич, Р. Габасов, Ф. М. Кириллова. «Построение оптимальных обратных связей
  по математическим моделям с неопределенностью». ЖВМиМФ, 2004, т. 44, № 2, с. 265–286.
  sha256(A1_Балашевич_2004.pdf) = 4569a9d9dca6bacb4a2927a1c8c39689e5a3b73dced51ba1d08a290a28d5c9a1 (matches corpus/MANIFEST.md)
- A2: Н. М. Дмитрук. «Оптимальная стратегия с одним моментом замыкания в линейной задаче
  оптимального гарантирующего управления». ЖВМиМФ, 2018, т. 58, № 5, с. 664–681.
  sha256(A2_Дмитрук_2018.pdf) = fca596196bdfe1f8740a767427fe1fd761a8c0712f6b3b314bf0832fe9d29dc9
- A3: Д. А. Костюкевич, Н. М. Дмитрук. «Метод построения оптимальной стратегии управления
  в линейной терминальной задаче». Журнал БГУ. Математика. Информатика. 2021;2:38–50
  (article body in English, Russian title/abstract).
  sha256(A3_Костюкевич_Дмитрук_2021.pdf) = 2330f4ac22dd57b924b17f130a7937769ea6f6f56f825f1779102a038a347288 (matches corpus/MANIFEST.md)
- Anchors: file + printed journal page (with PDF page in parentheses) + verbatim quote.
  Page maps: A1 PDF p. k = journal p. 264+k; A2 PDF p. k = journal p. 663+k; A3 PDF p. k = journal p. 37+k.
- Verbatim quotes below were byte-checked against the PDF text layers (pdftotext); Cyrillic
  OCR of math symbols (α, superscripts) was restored from the page scans, wording unchanged.

## Per-paper findings

### A1 (Балашевич 2004)
Setting: linear nonstationary ОУ problem with set-membership uncertainty,
h_(0)(x(t*)) → max, ẋ = A(t)x + b(t)u + d(t)w, x(t*) ∈ X*, |u| ≤ 1, w(t) ∈ W (journal p. 267, eq. 2.1).
This is a MAX–MIN problem: the controller maximizes the guaranteed (worst-case) payoff
J(u) = min_{x∈X(t*)} h_(0)(x) (p. 267). Controls are discrete (period h); the feedback quality is
the guaranteed criterion value, and feedbacks are classified by how much future information they use.

- Feedback taxonomy and the densification principle — p. 265 (PDF 1): «В зависимости от
  используемой информации вводится несколько типов обратных связей (размыкаемые,
  замыкаемые). По мере усложнения обратной связи (ОС) увеличивается ее эффективность.»
  Types: razмыкаемая (one-shot program recalculated per position), closable (замыкаемая,
  with closure moments), multiply closable, and closed (Bellman) as the p = N limit.
- Bellman recursion and its infeasibility — p. 267–268 (PDF 3–4): Bellman function
  B(τ, z) = max_{|u|≤1} min_{w∈W} min_{x∈[τ,t*]} h_(0)(x(t*)) for the family (2.5), recursion (2.6);
  p. 268 (PDF 4): «Приведенная красивая схема решения задачи (2.1) методом динамического
  программирования не реализуема из-за проклятия размерности (см. [12]), т.е. из-за
  невозможности табулирования функции Беллмана и ОС для задач (2.1) при больших n.»
- Guaranteed program control reduced to a deterministic extremal problem — p. 269 (PDF 5):
  constraints (3.2) split into a nominal part plus worst-case disturbance reserves
  γ_i(τ) = min_w ∫ h_(0)'(t)F(t*)F⁻¹(s)d(s)w(s)ds; the ОПУ becomes a linear extremal problem
  (3.4)–(3.5) with shifted right-hand sides ḡ_i(τ) = g_i − γ_i(τ) − h_(0)'(t*)F(t*)F⁻¹(τ)z,
  solved by the adaptive LP method of [14] (Габасов, Дмитрук, Кириллова, АиТ 2002).
- Two-phase closable OC (feasibility restoration) — p. 270 (PDF 6): if x*₀ admits no guaranteed
  drive to X*, phase 1 solves γ⁰(τ, z) = min γ (minimal γ-neighborhood of X*, eq. 4.1); the
  regulator switches to phase 2 (optimal guaranteed program) at the first τ̄ with γ⁰(τ̄, x*(τ̄)) ≤ 0.
- ONE closure moment machinery (§5) — p. 271 (PDF 7): «Используя момент замыкания t¹,
  определим множество замыкания X¹, включив в него все начальные состояния x в момент t¹,
  которые с гарантией можно перевести в момент t* на терминальное множество X*.»
  The schedule is chosen by the decision maker: p. 271 (PDF 7): «Выберем момент t¹ ∈ T_h
  (t_* < t¹ < t*−h)…». For α ∈ [α_min, α_max] (α_min, α_max = extrema of h_(0) over X*), the
  α-множество замыкания X¹_α collects states guaranteeing entry into
  X*_α = X* ∩ {h_(0) ≥ α}; its worst-case «сужение» X̄¹_α = {h'_(i)(t¹) ≥ g_i − γ_1(t¹),
  h_(0) ≥ α − γ_0(t¹)} accounts for disturbances on [t¹, t*] (p. 272, PDF 8).
- Optimal guaranteed value for a fixed closure moment — p. 272 (PDF 8): «Максимальное
  значение α⁰, для которого существуют множество X¹_{α⁰} и α⁰-допустимое управление
  u^{α⁰}(t|τ, z, 0) (t ∈ T⁰(τ)), является оптимальным гарантированным значением критерия
  качества задачи (2.5) для момента замыкания t¹.»
- Polyhedral approximation algorithm — p. 272–275 (PDF 8–11): X¹_{α_k} approximated from
  outside by M(k)+1 facet half-spaces with normals h¹_(i); Algorithm 1 alternates (a) solving
  M(k)+1 ОУ problems (5.2) (each an LP family parametrized by α), (b) a min-ρ problem (5.3)
  testing α-feasibility, updating α_k monotonically; new facets from active constraints/Lagrange
  multipliers (5.4)–(5.5); ε-stop criterion (5.6) on α_{k−1} − α_k ≤ ε. Output: k-suboptimal
  guaranteed control u^{α_k}.
- MULTI-closure (§7) — p. 279–280 (PDF 15–16): schedule (7.1): «{tⁱ ∈ T_h, i = 1,p},
  t_* < t¹ < … < t^p < t* = t^{p+1}»; closure sets defined recursively — p. 280 (PDF 16):
  «Множества (7.2) определим рекуррентно. Положим X^{p+1} = X*. Множество X^l содержит
  состояния x ∈ Rⁿ, которые с гарантией можно перевести на множество X^{l+1} на промежутке
  T^l = [t^l, t^{l+1}].» p. 280 (PDF 16): «Оптимальная ОС, построенная с помощью p моментов
  замыкания, называется оптимальной многократно замыкаемой ОС. При p = N оптимальная
  многократно замыкаемая ОС называется оптимальной замкнутой ОС.» Algorithm 2 builds
  approximating polyhedra X^{l,k}_α backwards l = p, …, 1 (7.3)–(7.5). α⁰ is still computed for
  the GIVEN moments {tⁱ}; no optimization over the schedule.
- «Effective systems» (quasi-monotonicity of closure sets) — p. 282 (PDF 18), Замечание 2:
  «Систему управления (2.1)… назовем эффективной, если при любых достаточно малых h > 0
  и моментах замыкания t¹ = t⁰ < … < t^k < t* максимальный радиус r шара, который можно
  поместить в множество замыкания X^k, растет с уменьшением индекса k.» For effective
  systems an optimal closable OC drives any x(t⁰) ∈ X⁰ into an ε-neighborhood of X* under all
  w(·) ∈ W. (Also p. 282: «Программная составляющая оптимальной замыкаемой ОС… переводит
  систему управления на терминальное множество вне зависимости от реализующегося в
  дальнейшем возмущения» — the program part of a closable OC is disturbance-independent.)
- Numerics: Example 1 (oscillator ẍ = −x + u + w, maximize x₁(t*)): single closure t¹ = 8 gives
  α⁰ = 2.579865 vs deterministic optimum 7.793629 (p. 278–279, PDF 14–15). Example 2 (p. 284,
  PDF 20): «Таким образом, оптимальное гарантированное значение критерия качества
  α⁰ = 1.175554. Если вместо двух моментов замыкания использовать только один момент
  t¹ = 6, то получим α⁰ = 0.646045, в случае одного момента замыкания t¹ = 9 получаем
  α⁰ = 0.733118.» — closure-count monotonicity demonstrated numerically only; deterministic
  optimum 5.638651 (p. 285). Realized value of the closed-loop run α⁰(t*) = 5.316653.

### A2 (Дмитрук 2018)
Setting: continuous-time linear nonstationary system with unknown bounded disturbance w*,
discrete controls |u(t)| ≤ 1, terminal set X_f = {x: Hx ≤ g} (1.2), cost = total control impulse
J(u) = ∫|u(t)|dt (1.3) minimized under the WORST disturbance — a min–max problem, the
polarity opposite to A1. One closure moment t₁ given a priori: p. 665 (PDF 2): «Предположим,
что задан такой момент времени t₁, что t₁ ∈ Δ, t₀ < t₁ < t_f − h.»; p. 666 (PDF 3): «Следуя [14],
момент t₁ будем называть моментом замыкания системы (1.1).» Motivation — p. 665 (PDF 2):
«Введение промежуточных моментов, названных моментами замыкания, позволяет добиться
компромисса между консерватизмом оптимальных гарантирующих программ и вычислительными
трудностями, связанными с динамическим программированием.»

- Strategy with one closure — p. 666 (PDF 3): π₁ = {u₀(·|x₀); u₁(·|x₁), x₁ ∈ X(t₁|x₀, u₀(·|x₀))};
  feasibility X(t_f|x₁, u₁(·|x₁)) ⊆ X_f for all x₁ in the reachable set at t₁ (1.4); value
  V(π₁) = max_{w⁰∈W₀}{∫_{T₀}|u₀|dt + ∫_{T₁}|u₁|dt}; optimal strategy π₁⁰ = argmin V(π₁).
- Closure set and its α-parametrization — p. 666–667 (PDF 3–4): X₁ = {x₁: ∃ гарантирующая
  программа} («множество замыкания», following [14] = A1); min–max problem (2.4) rewritten
  (2.5)–(2.6) as V(π₁⁰) = min_{u₀,α}{∫_{T₀}|u₀|dt + α} subject to x(t₁) ∈ X₁(α) for all w⁰ ∈ W₀,
  where X₁(α) = {x₁ ∈ X₁: J₁(x₁) ≤ α} and α ∈ [0, α*], α* = max_{u₁∈U₁f}∫|u₁|dt = t_f − t₁.
  Here J₁(x₁) is the optimal guaranteed impulse on T₁ — the inner value function; the
  information parameter α is the allowed post-closure cost budget.
- One-LP solution — p. 668 (PDF 5): «…позволяющая существенно снизить (в сравнении с [14])
  трудоемкость построения оптимальной начальной программы u₀⁰(·|x₀), а именно, свести все
  вычисления к решению одной задачи линейного программирования, без применения описанной
  в замечании 1 итерационной схемы.» This replaces A1's iterative polyhedral refinement.
- Утверждение 1 (support function affine in α) — p. 670 (PDF 7): «Утверждение 1. При любом
  α ∈ [0, α*] значение g_p(α) может быть найдено по формуле g_p(α) = g_p(0) + q'_p ω(α)» (3.7),
  where g_p(α) = max{p'x₁: x₁ ∈ X₁(α)} (3.2); q'_p is the vector |p'd(s)| over the grid sorted
  decreasingly (3.6), and ω_j(α) = 1 for j < N_α, ω_{N_α}(α) = α/h, ω_j = 0 beyond, with
  N_α = ⌊α/h⌋ + 1. Proof purely by LP duality (3.8)–(3.15); Φ(α) piecewise linear, «Полная
  релаксация функции (3.15) происходит после N₁ − ⌊α/h⌋ скачков».
- Closure set is polyhedral and affine in α — p. 671 (PDF 8): X₁(α) = {x₁ ∈ Rⁿ: P₁x₁ ≤
  g₁ + Q₁ω(α)} (3.16); «В (3.16) матрицы P₁, Q₁, вектор g₁ не зависят от параметра α и все
  трудоемкие операции, связанные с их построением, проводятся до начала процесса
  управления.» (If the facet system is too large, outer approximations à la [14] give a
  suboptimal π₁⁻⁰, Замечание 2.)
- Утверждение 2 (single LP yields everything) — p. 672 (PDF 9): the LP (3.18)
  min Σ(u* + u_*) + Σω_j s.t. ΣR₁d(s)(u* − u_*) − Q₁ω ≤ ḡ₁, 0 ≤ u*, u_*, ω ≤ 1 delivers the
  optimal initial program u₀⁰(t|x₀) = u⁰*(s) − u*⁰(s) and the optimal parameter
  α⁰ = h·Σω⁰_j (3.19), with V(π₁⁰) = hφ⁰. Proof: explicit optimal dual solution of (3.20) has
  ω⁰ = ω(α⁰) (complementary slackness + sorted q_j structure).
- Comparison with the optimal guaranteed program — p. 673 (PDF 10): «Нетрудно видеть, что
  V(π₁⁰) ≤ J(u⁰).» (program control = strategy degenerated to closure at t₀).
- Утверждение 3 (two-sided improvement bounds) — p. 674 (PDF 11): «Утверждение 3. Для
  оптимальных значений критериев качества задач (4.1), (2.7) справедливы оценки
  δ_min ≤ J(u⁰) − V(π₁⁰) ≤ δ_max» (4.2), with δ_min = ∫_{T₁}|u⁰(t)|dt − α₁ ≥ 0, α₁ from an LP
  (4.3) using the X₁(α) representation, and δ_max = w*∫_{T₀}φ(t, v⁰)dt where φ(t, v) =
  Σᵢ|lᵢ(t)|vᵢ − |l'(t)|v, v⁰ = optimal Lagrange multipliers of the program problem (4.1).
  Degenerate case — p. 676 (PDF 13): if the program's active set uses one terminal constraint,
  then δ_max = 0 and V(π₁⁰) = J(u⁰): «…при существовании оптимальной гарантирующей
  программы u⁰(t), для которой выполняется указанное свойство, нет смысла выбирать более
  сложную формулировку оптимального управления.»
- Closable feedback — p. 676–678 (PDF 13–15): for every position (τ, z) the strategy problem
  (5.1) min_{u₀,α}∫|u₀| + α s.t. x(t₁) ∈ X₁(α) reduces to an LP (with ḡ₁(τ) updated by the
  measured state); real-time implementation re-solves small LPs each step, warm-started from
  the previous position's solution.
- Numerics — p. 678–680 (PDF 15–17): Example 1 (ẍ = −x + u + w, X_f = {|x_j| ≤ 2}, t_f = 10,
  h = 0.1, x₀ = (5,0), t₁ = 8): J(u⁰) = 5.65361725, V(π₁⁰) = 5.01318650, α⁰ = 1.1, improvement
  0.64313075; P₁ has 166 rows; runtime 0.75 s vs ~3 min for the A1-style iterative algorithm.
  Example 2 (t₁ = 7): V = 4.87967433, improvement 0.77664292, δ_min = 0.31415839;
  p. 679 (PDF 16): «Данный пример демонстрирует улучшение значения V(π₁⁰) в связи с
  выбором момента замыкания t₁. На фиг. 2 представлена зависимость оптимального значения
  критерия качества от момента t₁ ∈ Δ. Минимальное значение V(π₁⁰) достигается при
  t₁⁰ = 6.8 и равно 4.85703231.» — the V(t₁) curve (Fig. 2, p. 680) is NON-monotone with an
  interior minimum, found by grid scan only.
- Feasibility restoration — p. 680 (PDF 17), Example 4: «Учет дополнительной информации о
  состоянии системы управления в будущий момент t₁ позволяет не только улучшить качество
  процесса управления, но и предложить стратегию управления π₁ в том случае, когда
  оптимальная гарантирующая программа u⁰(·) не существует.» With w* = 0.4 the program
  problem (4.1) «не имеет гарантирующих программ из-за пустого множества решений системы
  неравенств Hx ≤ g − γ», yet V(π₁⁰) = 6.20761677 (α⁰ = 1.4). Example 5: realized closable
  feedback 3.40489952 vs razмыкаемая 3.67372354.
- Explicit open problem — p. 681 (PDF 18): «Численные эксперименты (см. пример 2) также
  демонстрируют зависимость значения критерия качества от положения момента замыкания.
  Определение оптимального момента замыкания, а также развитие предложенного подхода на
  случай многократных замыканий — цель дальнейших исследований.»

### A3 (Костюкевич & Дмитрук 2021)
Setting (closest to our bridge class): linear DISCRETE-time system
x(t+1) = Ax(t) + Bu(t) + Mw(t), x(0) = x₀, t = 0,…,T−1 (eq. 1); U = box [u_min, u_max],
W = {‖w‖_∞ ≤ w_max}; terminal box X_T = {g_min ≤ Hx ≤ g_max}; minimax terminal cost
J(u) = max_{w(·)} c'x(T) (eq. 3) — exactly our shape (additive disturbance, box constraints,
worst-case terminal cost) with linear instead of ‖·‖₁ cost. Bilingual paper (English body,
Russian abstract) — Russian quote from abstract, key statements quoted in English.
- Russian abstract — p. 38 (PDF 1): «Определяется оптимальная стратегия управления,
  учитывающая информацию о состоянии системы в один будущий момент времени, и
  предлагается эффективный метод ее вычисления. Результаты численных экспериментов
  демонстрируют улучшение качества управления на основе введенной оптимальной стратегии
  в сопоставлении с оптимальной гарантирующей программой при сравнимой трудоемкости их
  вычисления.»
- Program (open-loop worst-case) layer — p. 40 (PDF 3): deterministic equivalent (4) with
  «tightened» terminal set via γᵢ(t) = w_max Σ‖h'_ᵢA'M‖: J(u) = min c'x₀(T) + γ₀(0) s.t.
  g_min + γ(t) ≤ Hx₀(t) ≤ g_max − γ(t); u⁰(·) is a single LP.
- Strategy and the schedule — p. 41 (PDF 4): «Before the control process starts, we fix a time
  instant T₁ ∈ {1, 2, …, T − 1} that is referred to as the closing instant of system (1)
  (see [6; 8]).» — fixed a priori, never optimized. Strategy π₁ = {u₀(·|x₀), u₁⁰(|x₁),
  x₁ ∈ X(T₁|x₀, u₀⁰(|x₀))}; Definition 4: optimal strategy solves
  V(π₁⁰) = min_{u₀(·)} max_{w₀(·)} J₁(x(T₁)) (eq. 9) with the INNER value
  J₁(x₁) = min_{u₁} max_{w₁} c'x(T|x₁, u₁, w₁) (eq. 7) — a nested min–max.
- Minimax inequality (program vs 1-closure) — p. 42 (PDF 5): «Taking into account the minimax
  inequality we conclude that V(π₁⁰) ≤ J(u⁰).» (same direction as A2, cost version).
- Level sets of the implicit value function — p. 42 (PDF 5): «The function J₁(x₁), x₁ ∈ Rⁿ, as
  the optimal value of a linear program (to which problem (7) is reduced), is a piecewise linear
  convex function (see [10, p. 180]), therefore for any fixed α ∈ [α_min, α_max] the α-level set
  X₁(α) = {x₁ ∈ X₁: J₁(x₁) ≤ α} is a convex polyhedron», with
  α_min = inf c'x + γ₀(T₁), α_max = sup c'x − γ₀(T₁) (bounds on the information parameter).
- Proposition (affinity under a rank condition) — p. 43 (PDF 6): Assumption 1:
  rank(G₁'|c₁) = rank(G₁'|c₁|p_j) = m+1 for all facet normals p_j, where
  G₁ = HA^{T−T₁}, c₁ = c'A^{T₁−T}. Then (12): f_j(α) = f₀ⱼ + λⱼα with
  «f₀ = f(0), λ = {λ_j, j = 1, …, m₁}, λ_j satisfies the conditions G₁'y + c₁λ_j = p_j, λ_j ≥ 0»;
  λ_j and f₀ⱼ come from the explicit dual of LP (13)–(14) WITHOUT solving it (formulae (15));
  if the rank condition fails for p_j, then f_j(α) ≡ +∞ (that direction inadmissible). This is the
  exact-affinity result for closure-set supports — the discrete/terminal-cost twin of A2's
  Утверждение 1.
- One-LP reduction — p. 44–45 (PDF 7–8): with f_j affine, problem (10) [V(π₁⁰) = min_α α s.t.
  J₁(x(T₁)) ≤ α ∀w₀] becomes (16): min α s.t. P₁x(T₁) ≤ f₀ + λα, and reduces to LP (17) with
  T₁ + 1 variables; p. 45 (PDF 8): «problem (17) is solved only once and its solution
  immediately yields the optimal value of the parameter α⁰ = V(π₁⁰) and the optimal initial
  open-loop control u₀⁰(|x₀).»
- Second regime (rank = n < m+1) — p. 44–45 (PDF 7–8): f_j(α) piecewise affine concave on
  [α_min, α_max]; approximate the lifted set Ξ₁(α) = {(ξ₀, ξ) ∈ R^{m+1}: ∃u₁ …} by a polyhedron
  with affine f̄_j(α) = f̄_j(0) + λ̄_jα (formula (18) for f̄₀ⱼ); LP (19) with P̄₁ = q₀c₁' + Q₁G₁.
  Drawback admitted — p. 45 (PDF 8): «To avoid this problem one has to explore the piecewise
  affine structure of the function f_j(α), α ∈ [α_min, α_max]. This will be the focus of a future
  work.»
- Numerics — p. 46–49 (PDF 9–12): Example 1 (discretized Kostyukova–Kostina [6] problem,
  x₂(T) → max, T = 120, T₁ = 80): «…J(u⁰) = 1.501102, while the optimal control strategy (8)
  has the optimal guaranteed value V(π₁⁰) = α⁰ = 2.754 215»; «Calculating the optimal
  open-loop worst-case control takes 0.015 1 s, while to obtain the optimal strategy we needed
  0.018 6 s»; «83 vectors were required, i. e. m₁ = 83»; worst disturbances for program and
  strategy COINCIDE: w*(t) = w_max·sign(c'A^{T−t−1}M), t = 0,…,T−1; geometric identity
  J(u⁰) = min_{x₁∈X(T₁|x₀,u⁰)} J₁(x₁) holds exactly despite the approximation.
  Example 2 (discretized A2 [8] impulse problem, n = 3, T = 100, T₁ = 80): «to J(u⁰) =
  5.722 047. The optimal control strategy has the optimal guaranteed value V(π₁⁰) = α⁰ =
  5.039103»; vs [8] (piecewise-continuous disturbance) J = 5.656 317, V = 5.013186 5 —
  «slightly worse performance is due to discrete disturbance»; «to obtain the optimal strategy
  by solution of problem (19) we needed only 0.081 2 s (0.75 s in [8])»; LP dimension T₁ + 1
  vs T variables in [8].
  Example 3 (indirect control, n = 4, T₁ = 60): «to J(u⁰) = 7.438 263. The optimal strategy
  gives V(π₁⁰) = α⁰ = 6.657 643. The time spent to construct the optimal open-loop worst-case
  control was 0.015 s, while for the optimal control strategy 0.139 s were spent.»
- Self-positioning — p. 49 (PDF 12), Conclusion: «The proposed formulation is a minimax
  optimal control problem with a cost function that is implicitly defined as the optimal value of
  another optimal control problem. We thoroughly elaborated the structure of this problem
  using the duality theory, which allowed us to reduce it to an equivalent linear program and
  significantly simplify the method for optimal strategy construction compared to the
  algorithm introduced in [6].»

## Theorem blocks (cross-paper, prefixed a1-/a2-/a3-)

### thm-a1-1: Bellman recursion for the guaranteed value is untabulable
- statement: B(τ, z) = max_{|u|≤1} min_{w∈W} min_{x∈[τ,t*]} h_(0)(x(t*)) satisfies the backward
  recursion (2.6) with terminal condition B(t*, z) = h_(0)(z) on X*, −∞ off X*; the exact closed
  loop it defines is computationally unrealizable («проклятие размерности»).
- conditions: linear system (2.1), box control |u| ≤ 1, compact disturbance set W, terminal set X*.
- anchor: A1_Балашевич_2004.pdf, p. 268 (PDF 4) — «Приведенная красивая схема решения
  задачи (2.1) методом динамического программирования не реализуема из-за проклятия
  размерности (см. [12])…»
- our-relevance: this is the school's founding negative result; our ladder of N scheduled
  closures is positioned exactly in the gap between program (N=0, trivial) and closed loop
  (N=T, Bellman).

### thm-a1-2: Guaranteed program control = deterministic extremal problem with disturbance reserves
- statement: an admissible discrete control u(t) must satisfy h'_(i)(t*)F(t*)F⁻¹(τ)z +
  ∫h'_(i)(t*)F(t*)F⁻¹(s)b(s)u(s)ds ≥ g_i − γ_i(τ), where the reserve γ_i(τ) = min_w ∫h'_(i)(t*)…·
  d(s)w(s)ds collects the worst-case disturbance contribution along rows of H; hence the ОПУ
  under uncertainty (2.5) equals the deterministic linear extremal problem (3.4)–(3.5) with
  ḡ(τ) = g − γ(τ) − h'_(0)(t*)F(t*)F⁻¹(τ)z.
- conditions: piecewise-continuous w, fundamental matrix F, discrete controls.
- anchor: A1_Балашевич_2004.pdf, p. 269 (PDF 5), eqs. (3.2)–(3.5).
- our-relevance: direct template for our oracle layer: our w ∈ {−1,+1} worst-case reserves are
  the |E|·(row sums) special case; the x(t+1) = x + Bu + Ew dynamics with A = I is exactly
  this with F = I.

### thm-a1-3: One-closure optimal guaranteed value α⁰ via α-множества замыкания
- statement: for fixed t¹, X¹_α = {x: ∃α-admissible control on T¹ transferring x into
  X*_α = X* ∩ {h_(0) ≥ α} under all w}; α⁰ = max{α: x*₀ ∈ X¹_α} is the optimal guaranteed
  criterion value with one closure; computable through the squeezed polyhedron
  X̄¹_α = {h_(i)(t¹) ≥ g_i − γ₁(t¹), h_(0) ≥ α − γ₀(t¹)}.
- conditions: X*_α nonempty; reserves γ₀, γ₁ for intervals [t¹, t*] and [t*, t*] respectively.
- anchor: A1_Балашевич_2004.pdf, p. 271–272 (PDF 7–8) — «Максимальное значение α⁰… является
  оптимальным гарантированным значением критерия качества задачи (2.5) для момента
  замыкания t¹.»
- our-relevance: the ancestor of our one-closure value formula V₁(x₀, R); note their value
  ladder is on the PAYOFF (α from below), so their monotonicity with more closures is upward.

### thm-a1-4: Algorithm 1 — polyhedral outer approximation + parametric LP, k-suboptimality
- statement: starting from m facets, iteratively (a) build X^{1,k}_{α_k} = {h¹_(i)'x ≥ β¹⁽ᵏ⁾_i,
  i = 0..M(k)} by solving M(k)+1 ОУ problems (5.2) parametrized by α, (b) solve min ρ over
  u with x(t¹) ∈ X̄^{1,k}_α (5.3); bisection on α gives α_k with ρ_{α_k} = 1; new facets from
  active sets/Lagrange multipliers (5.4)–(5.5); stop when α_{k−1} − α_k ≤ ε and the iterates
  move ≤ ε (5.6); u^{α_k} is k-suboptimal (guaranteed value within the approximation error).
- conditions: M(k) facet budget, tolerance ε > 0.
- anchor: A1_Балашевич_2004.pdf, p. 273–275 (PDF 9–11), Алгоритм 1.
- our-relevance: the original judge-able deterministic procedure for closure values; our
  LP-judge machinery can reproduce this as a baseline (A1-style iteration vs our one-LP law).

### thm-a1-5: Multi-closure optimal value for a FIXED schedule (7.1)–(7.2)
- statement: for a given schedule t_* < t¹ < … < t^p < t* the closure sets are nested and
  recursive: X^{p+1} = X*, X^l = {x: ∃ control on [t^l, t^{l+1}] driving x into X^{l+1} under all
  w on T^l}; the optimal guaranteed value α⁰ for the schedule is the largest α with
  x*₀ ∈ X¹_α where X^l_α are built with the α-threshold propagated backwards; Algorithm 2
  approximates each X^{l,k}_α by polyhedra in the order l = p, …, 1 (7.3)–(7.5).
- conditions: given schedule (chosen a priori); adaptive LP at each stage.
- anchor: A1_Балашевич_2004.pdf, p. 279–281 (PDF 15–17) — «Множества (7.2) определим
  рекуррентно…»; «При p = N оптимальная многократно замыкаемая ОС называется
  оптимальной замкнутой ОС.»
- our-relevance: this is A4's direct ancestor (multi-closure, fixed schedule, V vs program).
  Crucially, A1 never asks WHICH schedule: our scheduling-law question is orthogonal to the
  whole A1 construction.

### thm-a1-6: Effective systems — nesting of closure sets and ε-guarantee (Замечание 2)
- statement: a system is «эффективная» if the largest inscribed ball radius in the closure set
  X^k grows as the closure index k decreases (earlier closures have larger closure sets);
  for such systems, for any X* and ε > 0 there is an optimal closable OC whose closed loop
  brings any x(t⁰) ∈ X⁰ into the ε-neighborhood of X* for all w(·) ∈ W.
- conditions: sufficiently small h > 0; closure moments t¹ = t⁰ < … < t^k < t*.
- anchor: A1_Балашевич_2004.pdf, p. 282 (PDF 18), Замечание 2.
- our-relevance: the only quasi-monotonicity statement in the line — and it is about SET
  nesting (geometry), not about value monotonicity in the schedule. No pre-emption of our
  ladder monotonicity, but a useful geometric lemma: reachability-style nesting of
  information-actuated sets.

### thm-a2-1: One-closure min–max strategy value as an α-parametrized program
- statement: V(π₁⁰) = min_{u₀∈U₀} max_{w⁰∈W₀} ∫|u₀| + J₁(x(t₁|u₀, w⁰)) (2.4) equals
  min_{u₀,α} ∫_{T₀}|u₀|dt + α subject to x(t₁) ∈ X₁(α) for all w⁰ ∈ W₀ (2.5), where
  X₁(α) = {x₁ ∈ X₁: J₁(x₁) ≤ α} (2.6) and α ∈ [0, α*], α* = t_f − t₁.
- conditions: Предположение 1 (X₁ ≠ ∅), Предположение 2 (∃u₀: X(t₁|x₀,u₀) ⊆ X₁).
- anchor: A2_Дмитрук_2018.pdf, p. 667 (PDF 4), eqs. (2.4)–(2.7).
- our-relevance: the exact one-closure value formula pattern we need; the budget α plays the
  role of the post-closure cost allowance, i.e. the closure set is a sublevel set of the
  continuation value — the same “value function of the future segment” trick our oracle must
  encode for ‖x_T‖₁.

### thm-a2-2: Утверждение 1 — support functions of closure sets are affine in the information parameter
- statement: for every direction p, g_p(α) = g_p(0) + q'_p ω(α) (3.7), where q'_p is built from
  |p'd(s)| sorted decreasingly over the grid (3.6) and ω(α) is the step vector with
  ω_{N_α}(α) = α/h, N_α = ⌊α/h⌋ + 1; proven by explicit LP duality ((3.8)–(3.15)).
- conditions: α ∈ [0, α*], X_f bounded, Предположение 1.
- anchor: A2_Дмитрук_2018.pdf, p. 670 (PDF 7) — «Утверждение 1. При любом α ∈ [0, α*]
  значение g_p(α) может быть найдено по формуле g_p(α) = g_p(0) + q'_p ω(α).»
- our-relevance: ORIGIN of the «closure sets affine in α» machinery we attributed to A4's
  Statement 1; in our {−1,+1} setting the d(s) impulse profile is even simpler, so the same
  formula gives closed-form supports of V's sublevel sets.

### thm-a2-3: Closure set = polyhedron with α-free matrices and α-affine right-hand side
- statement: X₁(α) = {x₁ ∈ Rⁿ: P₁x₁ ≤ g₁ + Q₁ω(α)} (3.16) with P₁, Q₁, g₁ computed entirely
  before the control process starts; ω(α) from thm-a2-2. (Fallback: outer approximations as in
  [14] ⇒ suboptimal π₁⁻⁰, Замечание 2.)
- conditions: finite facet system (P₁ of m₁ rows); Fourier–Mozkin/ESP for its construction.
- anchor: A2_Дмитрук_2018.pdf, p. 671 (PDF 8), eq. (3.16) and the following sentence «В (3.16)
  матрицы P₁, Q₁, вектор g₁ не зависят от параметра α…».
- our-relevance: this is literally the form «P_j x ≤ g_j + λ_j α» that A4 generalizes to N
  closures; for our report to the owner: the affine-in-α statement has its roots HERE (2018),
  not in 2022.

### thm-a2-4: Утверждение 2 — the whole strategy is ONE linear program
- statement: let (u*⁰, u*⁰*, ω⁰) solve LP (3.18): min Σ_{Δ₀}(u* + u_*) + Σ_{j=1}^{N₁} ω_j s.t.
  ΣR₁d(s)(u* − u_*) − Q₁ω ≤ ḡ₁, box constraints; then u₀⁰(t|x₀) = u*⁰(s) − u*⁰*(s),
  α⁰ = h·Σω⁰_j, and V(π₁⁰) = hφ⁰; no iterative α-refinement is needed.
- conditions: Предположения 1–2; facet system of thm-a2-3.
- anchor: A2_Дмитрук_2018.pdf, p. 672 (PDF 9), Утверждение 2 with formulas (3.18)–(3.19).
- our-relevance: the computational heart: closure value + policy in one LP. For our
  N-closure setting with scheduled R, the analogous question (one LP per schedule vs one LP
  over schedules) is exactly where our contribution lives.

### thm-a2-5: Утверждение 3 — computable two-sided gap J(u⁰) − V(π₁⁰), with a zero-improvement certificate
- statement: δ_min ≤ J(u⁰) − V(π₁⁰) ≤ δ_max (4.2), δ_min = ∫_{T₁}|u⁰|dt − α₁ ≥ 0 with α₁ from LP
  (4.3) over the X₁(α) representation, δ_max = w*∫_{T₀}φ(t, v⁰)dt with φ(t, v) = Σᵢ|lᵢ(t)|vᵢ −
  |l'(t)|v from the program's optimal duals v⁰; if the program has a single active terminal
  constraint (v⁰ concentrated), then φ ≡ 0, δ_max = 0 and V(π₁⁰) = J(u⁰): closure cannot help.
- conditions: Предположение 3 (program (4.1) solvable); duality for (4.5)–(4.6).
- anchor: A2_Дмитрук_2018.pdf, p. 674 (PDF 11) for (4.2); p. 676 (PDF 13) for the δ_max = 0 case.
- our-relevance: template for our judge-side bounds V₀(x₀) ≤ J(x₀) refined to computable
  gaps; the degeneracy certificate (one active row ⇒ zero value of information) is a ready
  sanity check for our N-closure bounds: if the program's duals are supported on one row,
  every closure ladder must collapse to the program value.

### thm-a2-6: Closable feedback from the strategy — per-position LP with warm starts
- statement: for every position (τ, z), τ ∈ Δ₀, problem (5.1) min_{u₀,α}∫|u₀| + α s.t.
  x(t₁) ∈ X₁(α) reduces to an LP identical to (3.18) with ḡ₁(τ) = g₁ − γ₀(τ) − R₁F(t₁)F⁻¹(τ)x*(τ);
  the pair built at the previous position is admissible for the new one and serves as the initial
  basis, so the receding re-solve costs little; after t₁ the post-closure guaranteed program
  (5.2) reduces to an LP likewise.
- conditions: measured state at each τ ∈ Δ₀; measured exact state at t₁.
- anchor: A2_Дмитрук_2018.pdf, p. 676–678 (PDF 13–15), eqs. (5.1)–(5.3).
- our-relevance: the implementation layer of the school's OC; our real-time dashboard
  (“measure at R, re-optimize”) is the discrete analog; warm-start admissibility is a lemma we
  can port for free.

### thm-a3-1: Minimax strategy with implicit inner value; V(π₁⁰) ≤ J(u⁰)
- statement: the optimal strategy with closing instant T₁ solves
  V(π₁⁰) = min_{u₀(·)∈U₀} max_{w₀(·)∈W₀} J₁(x(T₁)) (9) where
  J₁(x₁) = min_{u₁} max_{w₁} c'x(T|x₁,u₁,w₁) (7); the minimax inequality gives
  V(π₁⁰) ≤ J(u⁰) against the optimal open-loop worst-case program.
- conditions: discrete-time system (1), box U, W; terminal box X_T.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 41–42 (PDF 4–5) — «Taking into account the
  minimax inequality we conclude that V(π₁⁰) ≤ J(u⁰).»
- our-relevance: our exact problem class (only c'x(T) → ‖x_T‖₁ differs). The nested
  min–max/value-function formulation is the pattern our maxmin judge must verify; the
  inequality direction (cost) is the mirror of A1's payoff version — see Landscape.

### thm-a3-2: α-level sets of the inner value are polyhedra
- statement: J₁(·) is piecewise linear convex (optimal value of an LP parametrized by x₁),
  hence X₁(α) = {x₁ ∈ X₁: J₁(x₁) ≤ α} is a convex polyhedron for every
  α ∈ [α_min, α_max], with α_min = inf c'x + γ₀(T₁), α_max = sup c'x − γ₀(T₁).
- conditions: LP reducibility of (7) (guaranteed program on Δ₁), bounded X_T.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 42 (PDF 5).
- our-relevance: licenses discretization-free handling of the closure ladder for polyhedral
  costs; for ‖x_T‖₁ the same holds after standard epigraph lifting (J₁ remains PL convex) —
  a fact our Lean core can state directly.

### thm-a3-3: Proposition — exact affinity f_j(α) = f₀ⱼ + λ_jα under a rank condition
- statement: under Assumption 1 (rank(G₁'|c₁) = rank(G₁'|c₁|p_j) = m+1 for all j,
  G₁ = HA^{T−T₁}, c₁ = c'A^{T₁−T}), each support f_j(α) = max{p_j'x₁: x₁ ∈ X₁(α)} is affine:
  f_j(α) = f₀ⱼ + λ_jα (12) with λ_j ≥ 0 satisfying G₁'y + c₁λ_j = p_j read off the dual (14)–(15);
  f₀ⱼ likewise explicit; if the rank condition fails for p_j then f_j ≡ +∞ (the direction is
  infeasible at every α).
- conditions: single-terminal-cost direction c, box controls; T₁ fixed.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 43 (PDF 6) — «Proposition. Let assumption 1
  hold. Then f(α) = f₀ + λα…» with the λ_j conditions quoted above.
- our-relevance: the sharpest published form of “closure sets affine in the information
  parameter”; gives us, for our bridge class, closed-form λ_j = (dual norm of the tube under
  row p_j) and hence candidate scheduling statistics (support growth rates per direction) at
  zero computational cost.

### thm-a3-4: One LP (T₁+1 variables) computes α⁰ = V(π₁⁰) and the initial control simultaneously
- statement: under thm-a3-3 the problem (10)/(16) collapses to LP (17):
  min α s.t. Σ_{Δ₀}P₁A^{T₁−t−1}Bu₀(t) − λα ≤ f₀ − γ̄ − P₁A^{T₁−T}x₀, box u₀;
  solved ONCE, yielding α⁰ and u₀⁰(|x₀) at once (u₁⁰(|x₁) only at closure from the LP (7)).
- conditions: rank Assumption 1; facet normals p_j fixed offline.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 45 (PDF 8) — «problem (17) is solved only once
  and its solution immediately yields the optimal value of the parameter α⁰ = V(π₁⁰)…»
- our-relevance: complexity baseline for the per-schedule evaluation oracle our scheduling
  search will call; the schedule length enters only through T₁+1 variables and the f₀/λ data.

### thm-a3-5: Piecewise-affine regime — lifting to R^{m+1} and an explicit future-work pointer
- statement: when rank(G₁'|c₁) = n < m+1, f_j(α) is piecewise affine concave on
  [α_min, α_max]; one then approximates the lifted set Ξ₁(α) = {(ξ₀, ξ) ∈ R^{m+1}: ∃u₁, g_min +
  γ(T₁) ≤ ξ + ΣG₁D(t)u₁(t) ≤ g_max − γ(T₁), ξ₀ + Σc₁'D(t)u₁(t) ≤ α − γ₀(T₁)} by a polyhedron
  {q₀ξ₀ + Q₁ξ ≤ f̄(α)}, f̄_j(α) = f̄_j(0) + λ̄_jα affine, and solves LP (19) with P̄₁ = q₀c₁' + Q₁G₁.
- conditions: n < m+1 terminal-constraint deficit; approximation accuracy budget.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 44–45 (PDF 7–8) — «…f(α), α ∈ [α_min, α_max],
  is piecewise affine and concave…»; «To avoid this problem one has to explore the piecewise
  affine structure of the function f_j(α)… This will be the focus of a future work.»
- our-relevance: the piecewise-affine structure of f_j is EXACTLY what a scheduling law needs
  (knots of f_j vs candidate R); the 2021 authors parked it as future work and A4 did not pick
  it up — a documented, unclaimed thread adjacent to ours.

## Fact blocks

### fact-a1-1: In A1 the closure schedule is an input, chosen by hand
- «Выберем момент t¹ ∈ T_h (t_* < t¹ < t*−h)…» (§5) and the schedule (7.1) «{tⁱ ∈ T_h, i = 1,p},
  t_* < t¹ < … < t^p < t* = t^{p+1}» are fixed before running Algorithm 1/2; no criterion for
  choosing {tⁱ} is given anywhere in the paper.
- anchor: A1_Балашевич_2004.pdf, p. 271 (PDF 7) and p. 279 (PDF 15).

### fact-a1-2: Closure-count monotonicity shown numerically, not proved
- Example 2, same problem, same t-grid: one closure at t¹ = 6 → α⁰ = 0.646045; one at t¹ = 9 →
  α⁰ = 0.733118; two closures (6, 9) → α⁰ = 1.175554; deterministic optimum 5.638651.
  Realized closed-loop run: 5.316653 (Fig. 8 plots α⁰(τ) along the trajectory).
- anchor: A1_Балашевич_2004.pdf, p. 284–285 (PDF 20–21) — «Если вместо двух моментов
  замыкания использовать только один момент t¹ = 6, то получим α⁰ = 0.646045…».

### fact-a1-3: Lineage and tooling of A1
- A1 generalizes [15] (Габасов, Кириллова, Костина, АиТ 1996, № 7 — «Замыкаемые обратные
  связи по состоянию для оптимизации систем управления при неопределенности») and runs on
  the adaptive LP method with parallel constraints of [14] (Габасов, Дмитрук Н.М., Кириллова,
  АиТ 2002, № 3); Witsenhausen's sampled minimax problem is cited as [9].
- anchor: A1_Балашевич_2004.pdf, p. 285–286 (PDF 21–22), список литературы; p. 268 (PDF 4)
  for [15] as the predecessor construction.

### fact-a2-1: Direction of the program-vs-closure inequality in the cost setting
- V(π₁⁰) ≤ J(u⁰): one closure never worsens the guaranteed cost; same direction retained by
  A3 and (per our A4 reading) by A4's V₀(x₀) ≤ J(x₀).
- anchor: A2_Дмитрук_2018.pdf, p. 673 (PDF 10) — «Нетрудно видеть, что V(π₁⁰) ≤ J(u⁰).»

### fact-a2-2: The guaranteed value as a function of the closure moment is non-monotone with an interior optimum (numerics)
- Fig. 2 (p. 680): V(π₁⁰)(t₁) on t₁ ∈ Δ has plateaus and a unique interior minimum
  t₁⁰ = 6.8, V = 4.85703231 (vs 5.01318650 at t₁ = 8, 4.87967433 at t₁ = 7); located by grid
  scan; no analytic scheduling result.
- anchor: A2_Дмитрук_2018.pdf, p. 679–680 (PDF 16–17) — «Минимальное значение V(π₁⁰)
  достигается при t₁⁰ = 6.8 и равно 4.85703231.»
- our-relevance: kills any “close as late as possible” heuristic on our class and supplies a
  ready benchmark: a correct scheduling law must (a) reproduce interior optima of this shape,
  (b) beat or explain them without scanning.

### fact-a2-3: Closure restores feasibility, not only value
- Example 4 (w* = 0.4): the guaranteed program problem has an empty solution set
  (Hx ≤ g − γ infeasible), while the one-closure strategy exists with V(π₁⁰) = 6.20761677,
  α⁰ = 1.4. Same pattern in A1 §4 (two-phase closable OC, minimal γ-neighborhood).
- anchor: A2_Дмитрук_2018.pdf, p. 680 (PDF 17), Пример 4; A1_Балашевич_2004.pdf,
  p. 270 (PDF 6), eq. (4.1).
- our-relevance: for our V(x₀) definitions: with N = 0 (program) the value may be +∞ where
  N ≥ 1 is finite — the ladder must be stated on the extended reals, and the judge for
  V₀ ≤ V₁ must handle feasibility restoration, not only value improvement.

### fact-a2-4: Scheduling and multi-closure are declared open by the school itself
- Заключение + final page: «Определение оптимального момента замыкания, а также развитие
  предложенного подхода на случай многократных замыканий — цель дальнейших
  исследований.» A4 (2022) delivered the multi-closure part with a FIXED schedule; the
  OPTIMAL closure moment remained open after A2 and is not claimed by A4 either.
- anchor: A2_Дмитрук_2018.pdf, p. 681 (PDF 18).

### fact-a3-1: Quantified one-closure gains and runtimes (three examples)
- Ex.1 (from [6], max x₂(T), T=120, T₁=80): J(u⁰) = 1.501102 vs V = 2.754 215 (payoff gain
  ≈ +1.25); 0.015 1 s + 0.018 6 s; m₁ = 83 facet normals; worst-case disturbance identical for
  program and strategy: w*(t) = w_max·sign(c'A^{T−t−1}M).
- Ex.2 (from [8], min impulse, T=100, T₁=80): J = 5.722 047 vs V = 5.039103; 0.081 2 s vs
  0.75 s in [8]; LP has T₁+1 vs T variables.
- Ex.3 (indirect control, n=4, T₁=60): J = 7.438 263 vs V = 6.657 643; 0.015 s vs 0.139 s.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 46–49 (PDF 9–12).

### fact-a3-2: The closing instant is fixed a priori, schedule never optimized
- «Before the control process starts, we fix a time instant T₁ ∈ {1, 2, …, T − 1} that is referred
  to as the closing instant of system (1) (see [6; 8]).» — T₁ = 80, 80, 60 in Examples 1–3;
  no criterion, no sensitivity study (unlike A2's Fig. 2).
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 41 (PDF 4).

### fact-a3-3: Discretization price of the discrete model
- Discretizing A2's continuous problem at h = 0.1 with ∞-norm-bounded discrete disturbance
  degrades both values slightly: J: 5.656 317 → 5.722 047, V: 5.013186 5 → 5.039103; «slightly
  worse performance is due to discrete disturbance»; the trade-off: f_j(α) affine here
  (vs piecewise linear in A2's continuous-in-time case), hence smaller LP and faster solve.
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 47 (PDF 10) — «Compared to [8], where J(u⁰) =
  5.656 317 and V(π₁⁰) = 5.013186 5, slightly worse performance is due to discrete
  disturbance…».
- our-relevance: our {−1,+1} lattice is the fully discrete end of this trade-off; A3's numbers
  quantify what we pay/gain vs a continuous w model.

### fact-a3-4: Explicit unclaimed thread — piecewise-affine structure of f_j(α)
- «To avoid this problem one has to explore the piecewise affine structure of the function
  f_j(α), α ∈ [α_min, α_max]. This will be the focus of a future work.» — no follow-up in A4's
  machinery (A4 uses affine closure sets with a priori schedule and does not exploit knots of
  f_j for scheduling).
- anchor: A3_Костюкевич_Дмитрук_2021.pdf, p. 45 (PDF 8).

## Landscape

Line of construction:
- A1 (2004, Габасов school: Балашевич–Габасов–Кириллова) is the ARCHITECTURE paper: it
  fixes the vocabulary used ever since — moment of closure, closure set, razмыкаемая /
  замыкаемая / многократно замыкаемая / замкнутая OC — and the recursive nested-closure-sets
  construction (X^{p+1} = X*) that A4 later calls the «analog of the Bellman equation». Its
  engine is the Габасов-school adaptive parametric LP: closure sets are approximated
  iteratively by growing polyhedra, and α (the payoff threshold) is found by bisection.
  Schedule: given a priori (fact-a1-1). Polarity: max–min payoff (guaranteed α from below).
- A2 (2018, Н. М. Дмитрук) changes the ENGINE and the POLARITY: cost min–max with
  impulse cost; instead of iterating polyhedral approximations in x-space, it applies LP
  DUALITY directly to the closure-set supports and discovers that they are AFFINE in the
  information parameter α (thm-a2-2/thm-a2-3) — this collapses the whole iteration into ONE
  LP (thm-a2-4) and yields computable improvement bounds with a zero-information
  certificate (thm-a2-5). It also contributes the only scheduling-sensitive evidence in the
  line: the non-monotone V(t₁) curve with an interior optimum (fact-a2-2) — and explicitly
  defers optimal scheduling and multi-closure (fact-a2-4).
- A3 (2021, Костюкевич–Дмитрук) ports the A2 machinery to the DISCRETE-TIME TERMINAL-COST
  minimax problem (our exact class) and sharpens the math: exact affinity of f_j(α) under an
  explicit rank condition with dual formulas for λ_j (thm-a3-3), a rank-based case split
  (affine vs piecewise-affine concave), and a complexity accounting (T₁+1 variables). It
  candidly parks the piecewise-affine structure of f_j — the analytic object a scheduling law
  would consume — as future work (fact-a3-4).
- A4 (2022, already processed) generalizes A2's one-closure LP machinery to N closures with
  the SAME a priori schedule discipline as A1 (Statement 1: P_j x ≤ g_j + λ_j α affine in α —
  the direct descendant of A2's (3.16) and A3's Proposition), proves V₀(x₀) ≤ J(x₀), and never
  optimizes the schedule. So: A4 = A1's multi-closure architecture + A2/A3's duality engine;
  the missing piece across the whole 2004→2022 line is exactly our scheduling question.
- Corpus crossover (by filename and reference lists): Witsenhausen 1968 «A minimax control
  problem for sampled linear systems» is cited by all three (A1 ref [9], A2 ref [1], A3 ref [1])
  — the school self-identifies with the sampled-data minimax tradition (also Красовский 1985,
  Kurzweil A.B. 1977 in A2/A3). A2's list contains the closest external relatives: Kostyukova–
  Kostina 2006 (robust optimal feedback, terminal LQ) [6], Kostina–Kurina 2006 (гарантирующие
  стратегии с промежуточными моментами коррекции) [7], Kostina–Kostyukova 2009 [15],
  Chong–Kostyukova–Kurina 2010 «Guaranteed control policy with arbitrary set of correction
  points… with delay» [17] — note [17]'s title says “arbitrary set of correction points”, i.e.
  even the closest external line treats the correction/closure set as GIVEN, not optimized.
  On the two-stage adaptive-RO side of our bridge: A3's formulation — «a minimax optimal
  control problem with a cost function that is implicitly defined as the optimal value of
  another optimal control problem» — is structurally the same pattern as BGT-2004-style
  adjustable robust LP (corpus/02_BenTal_Goryashko_etal_2004.pdf) with a recourse value in
  the objective, and Zeng–Zhao 2013 (corpus/12) decision rules are the RO-side surrogate for
  the same inner max–min; GTW (corpus/23–24) constrain adjustable recourse similarly.
  A1–A3 differ from the RO line by EXACT polyhedral solvability (no decision-rule relaxation)
  and by the explicit measurement-at-closure semantics.

Max–min vs min–max asymmetry (cross-cutting):
- A1: guaranteed PAYOFF, α⁰ = max α, value ladder goes UP with more closures (0.646 →
  0.733 → 1.176); the program-vs-closure statement is implicit (α⁰ ≥ program guaranteed
  value through X*_α nesting).
- A2/A3 (and A4): guaranteed COST, V = min α, value ladder goes DOWN; V(π₁⁰) ≤ J(u⁰)
  stated explicitly (fact-a2-1).
- The inequality direction flips with polarity; our Foundational V_0(x₀) ≤ J(x₀) (A4, cost
  side) must not be transplanted to payoff statements without flipping. None of A1–A3 proves
  a monotonicity of the value in the schedule — the closest are A1's numerics (fact-a1-2) and
  the geometric nesting of thm-a1-6.

## Open threads for our portfolio

1. Scheduling law is NOT pre-empted — it is explicitly open at both ends of the line: A2
   (p. 681) names «определение оптимального момента замыкания» and multi-closure as
   «цель дальнейших исследований»; A3 (p. 45) parks the piecewise-affine structure of f_j(α)
   as «future work»; A4 fixed multi-closure schedules a priori. No paper in A1–A4 poses, let
   alone answers, “which R and in what order”.
2. The interior optimum in V(t₁) (fact-a2-2) is the strongest prior evidence that closure
   scheduling is a genuinely nontrivial decision — not a monotone “close late” rule. Our
   scheduling law should be validated against this example (t_f = 10, h = 0.1, x₀ = (5,0),
   w* = 0.3): reproduce t₁* = 6.8 analytically from the affine-support data, or explain the
   plateau structure.
3. Candidate scheduling statistics are already computable for free from A3's dual formulas:
   λ_j (support growth rates of closure sets per direction, thm-a3-3), the knots of f_j
   (fact-a3-4), and α_min/α_max endpoints (thm-a3-2). A scheduling law ranking candidate R
   by aggregate λ_j over ‖x_T‖₁'s subgradient directions is a concrete, defensible first
   proposal — and it uses machinery the school published but did not connect to scheduling.
4. Zero-information certificate (thm-a2-5): if the N = 0 program's optimal duals concentrate
   on a single terminal row, every closure has zero value on that instance. This is a ready
   judge-able theorem for our ladder: it bounds the ladder's usefulness and gives a negative
   control for experiments.
5. Feasibility restoration (fact-a2-3, A1 §4) forces our value ladder onto ℝ ∪ {+∞} with
   V₀ possibly infeasible where V₁ is finite; the monotonicity judge must compare values on
   the extended reals, and the Foundational inequality V₀ ≤ J must be re-examined at
   infeasible x₀ (A2's Example 4 shows V is defined where the program value is +∞).
6. Polarity discipline: our bridge class is cost min–max (A2/A3/A4 side). Any port of A1's
   α-множество construction (convenient for ‖·‖₊ thresholds) must flip inequality directions;
   worth a glossary entry (docs/GLOSSARY.md) distinguishing payoff-guarantee (A1) from
   cost-guarantee (A2/A3/A4).
7. Complexity bookkeeping for the scheduling search: per-schedule evaluation is one LP with
   T₁+1 variables (thm-a3-4; A4 analog per closure j); A3's runtimes (0.015–0.14 s) suggest a
   brute-force scan over candidate R is feasible at our scale — useful as the trivial baseline
   our law must beat in wall-clock, not only in value.

## Verdict for our reading queue

Processed and anchored: A1 (22 pp.), A2 (18 pp.), A3 (13 pp.); all sha256 verified (A1, A3 also
match corpus/MANIFEST.md). Keep all three as CORE of the Dmitruk-school branch.
- A1 = architecture and vocabulary (multi-closure, fixed schedule, iterative polyhedra +
  adaptive LP); value mainly historical/structural + numeric monotonicity evidence.
- A2 = the origin of the affine-in-α closure-set machinery (predecessor of A4's Statement 1),
  the one-LP engine, computable improvement bounds, and the only published evidence that
  closure scheduling is nontrivial (interior optimum) — with scheduling explicitly declared open.
- A3 = the discrete terminal-cost twin of our exact problem class; sharpest theorems (rank
  condition, exact affinity, T₁+1 LP) and an explicit unclaimed thread (piecewise-affine f_j)
  adjacent to our scheduling law.
No pre-emption found of our scheduling law, our maxmin answer, or ladder monotonicity:
the line optimizes CONTROL given a schedule, never the schedule. Recommended immediate
actions: (a) file thm-a2-5's zero-information certificate and fact-a2-2's benchmark instance
as candidate judge targets; (b) cross-link A2 (3.16)/A3 Proposition (12) → A4 Statement 1 in
the provenance of the «closure sets affine in α» claim; (c) add the payoff-vs-cost polarity
distinction to docs/GLOSSARY.md at the next session review.

## Registration table

Quotes are copied verbatim from the page text layers (pdftotext); soft-hyphen line breaks are
joined; OCR-lost sub/superscripts and math symbols in the A1 scan layer are restored as displayed
on the page; A3's body is in English, so its quotes are verbatim English (marked «англ.»).
Page numbers are printed journal pages (PDF page = journal page − 264 for A1, − 663 for A2, − 37 for A3).

| block | pdf file | page | verbatim quote |
|---|---|---|---|
| thm-a1-1 | A1_Балашевич_2004.pdf | 268 | `Приведенная красивая схема решения задачи (2.1) методом динамического программирования не реализуема из-за проклятия размерности (см. [12])…` |
| thm-a1-2 | A1_Балашевич_2004.pdf | 269 | `Отсюда следует, что ОПУ задачи (2.5) в условиях неопределенности является решением экстремальной детерминированной задачи` |
| thm-a1-3 | A1_Балашевич_2004.pdf | 271 | `Используя момент замыкания t¹, определим множество замыкания X¹, включив в него все начальные состояния x в момент t¹, которые с гарантией можно перевести в момент t* на терминальное множество X*.` |
| thm-a1-4 | A1_Балашевич_2004.pdf | 273 | `Таким образом, алгоритм построения k-субоптимального управления задачи (2.5) состоит в следующем.` |
| thm-a1-5 | A1_Балашевич_2004.pdf | 280 | `Оптимальная ОС, построенная с помощью p моментов замыкания, называется оптимальной многократно замыкаемой ОС. При p = N оптимальная многократно замыкаемая ОС называется оптимальной замкнутой ОС.` |
| thm-a1-6 | A1_Балашевич_2004.pdf | 282 | `Систему управления (2.1) с заданными ограничениями на управление и возмущение назовем эффективной, если при любых достаточно малых h > 0 и моментах замыкания… максимальный радиус r шара, который можно поместить в множество замыкания X^k, растет с уменьшением индекса k.` |
| fact-a1-1 | A1_Балашевич_2004.pdf | 271 | `Выберем момент t¹ ∈ T_h (t_* < t¹ < t*−h) и будем считать, что τ ∈ T¹_h = {t_*, …, t¹ − h} в задаче (2.5).` |
| fact-a1-2 | A1_Балашевич_2004.pdf | 284 | `Если вместо двух моментов замыкания использовать только один момент t¹ = 6, то получим α⁰ = 0.646045, в случае одного момента замыкания t¹ = 9 получаем α⁰ = 0.733118.` |
| fact-a1-3 | A1_Балашевич_2004.pdf | 286 | `Габасов Р., Кириллова Ф.М., Костина Е.А. Замыкаемые обратные связи по состоянию для оптимизации неопределенных систем управления // Автоматика и телемехан. 1996. № 7. С. 121-130; № 8. С. 90-99.` |
| thm-a2-1 | A2_Дмитрук_2018.pdf | 667 | `Заметим, что α ∈ [0, α*], где α* = max ∫\|u₁(t)\|dt = t_f − t₁.` |
| thm-a2-2 | A2_Дмитрук_2018.pdf | 670 | `Утверждение 1. При любом α ∈ [0, α*] значение g_p(α) может быть найдено по формуле g_p(α) = g_p(0) + q′_p ω(α).` |
| thm-a2-3 | A2_Дмитрук_2018.pdf | 671 | `В (3.16) матрицы P₁, Q₁, вектор g₁ не зависят от параметра α и все трудоемкие операции, связанные с их построением, проводятся до начала процесса управления.` |
| thm-a2-4 | A2_Дмитрук_2018.pdf | 672 | `Утверждение 2. Пусть u*⁰(s), u*⁰*(s), s ∈ Δ₀, ω⁰ = (ω⁰_j, j = 1, N₁) – решение задачи линейного программирования (3.18)…` |
| thm-a2-5 | A2_Дмитрук_2018.pdf | 674 | `Утверждение 3. Для оптимальных значений критериев качества задач (4.1), (2.7) справедливы оценки δ_min ≤ J(u⁰) − V(π₁⁰) ≤ δ_max` |
| thm-a2-6 | A2_Дмитрук_2018.pdf | 676 | `В разд. 2, 3 описан метод построения оптимальной стратегии управления π₁⁰ с одним моментом замыкания t₁ для начального состояния x₀ в момент t₀, т.е. для начальной позиции (t₀, x₀).` |
| fact-a2-1 | A2_Дмитрук_2018.pdf | 673 | `Нетрудно видеть, что V(π₁⁰) ≤ J(u⁰).` |
| fact-a2-2 | A2_Дмитрук_2018.pdf | 679 | `Минимальное значение V(π₁⁰) достигается при t₁⁰ = 6.8 и равно 4.85703231.` |
| fact-a2-3 | A2_Дмитрук_2018.pdf | 680 | `Учет дополнительной информации о состоянии системы управления в будущий момент t₁ позволяет не только улучшить качество процесса управления, но и предложить стратегию управления π₁ в том случае, когда оптимальная гарантирующая программа u⁰(·) не существует.` |
| fact-a2-4 | A2_Дмитрук_2018.pdf | 681 | `Определение оптимального момента замыкания, а также развитие предложенного подхода на случай многократных замыканий – цель дальнейших исследований.` |
| thm-a3-1 | A3_Костюкевич_Дмитрук_2021.pdf | 42 | (англ.) `Taking into account the minimax inequality we conclude that V(π₁⁰) ≤ J(u⁰).` |
| thm-a3-2 | A3_Костюкевич_Дмитрук_2021.pdf | 42 | (англ.) `…therefore for any fixed α ∈ [α_min, α_max] the α-level set X₁(α) = {x₁ ∈ X₁: J₁(x₁) ≤ α} is a convex polyhedron.` |
| thm-a3-3 | A3_Костюкевич_Дмитрук_2021.pdf | 43 | (англ.) `Proposition. Let assumption 1 hold. Then f(α) = f₀ + λα` |
| thm-a3-4 | A3_Костюкевич_Дмитрук_2021.pdf | 45 | (англ.) `problem (17) is solved only once and its solution immediately yields the optimal value of the parameter α⁰ = V(π₁⁰)` |
| thm-a3-5 | A3_Костюкевич_Дмитрук_2021.pdf | 44 | (англ.) `…we propose to replace the approximation of the set X₁(α) with the approximation of the set Ξ₁(α)` |
| fact-a3-1 | A3_Костюкевич_Дмитрук_2021.pdf | 46 | (англ.) `…achieves the optimal guaranteed value equal to J(u⁰) = 1.501102, while the optimal control strategy (8) has the optimal guaranteed value V(π₁⁰) = α⁰ = 2.754 215.` |
| fact-a3-2 | A3_Костюкевич_Дмитрук_2021.pdf | 41 | (англ.) `Before the control process starts, we fix a time instant T₁ ∈ {1, 2, …, T − 1} that is referred to as the closing instant of system (1) (see [6; 8]).` |
| fact-a3-3 | A3_Костюкевич_Дмитрук_2021.pdf | 47 | (англ.) `…slightly worse performance is due to discrete disturbance, while in [8] disturbance was assumed piecewise continuous.` |
| fact-a3-4 | A3_Костюкевич_Дмитрук_2021.pdf | 45 | (англ.) `…one has to explore the piecewise affine structure of the function f_j(α), α ∈ [α_min, α_max]. This will be the focus of a future work.` |
