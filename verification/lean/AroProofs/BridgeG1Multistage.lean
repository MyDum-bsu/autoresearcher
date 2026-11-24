import BridgeFormalV3.Proofs.Support

/-!
# G1: Multi-Closure (`k ≥ 2`) Generalization of the OGU ↔ Multistage ARO Bridge

Live Scientific Discovery Run-01 (`gen-multistage-k-closures`) built strictly over the frozen
core `BridgeFormalV2.Model` / `BridgeFormalV2.Goals` and `BridgeFormalV2.Proofs.Dynamics`.

Main theorems (zero `sorry`, zero custom axioms, arbitrary `k : ℕ`, arbitrary stage lengths
`len : Fin (k + 1) → ℕ`, and arbitrary joint disturbance set `Ω` — independent OR correlated):
  1. `multistage_stage_split`: Chronological stage recurrence splits additively into nominal
     control propagation plus purely exogenous stage deviation `stageDeviation`.
  2. `multistage_forward_policy`: Causal Borel-measurable translation from any
     `HistoryStatePolicy` (observing `(x_{r_1}, ..., x_{r_j})`) to a `HistoryDeviationPolicy`
     (observing `(ξ_0, ..., ξ_{j-1})`) preserving controls, states, terminal state, and bounds.
  3. `multistage_reverse_policy`: Causal Borel-measurable translation from any
     `HistoryDeviationPolicy` back to a `HistoryStatePolicy` preserving controls, states,
     terminal state, and bounds.
  4. `multistage_history_epigraph_eq_aro`: Exact epigraph level-set equality
     `multistageHistoryLevels D len Ω = multistageAroLevels D len Ω` for every `k : ℕ`.
  5. `multistage_markov_subset_history`: Memoryless Markov state-feedback levels are always
     contained in full-history OGU / multistage ARO levels.
  6. `exists_markov_strictly_weaker_than_history_k2`: Concrete `k = 2` (3-stage) correlated
     witness proving `0 ∈ multistageHistoryLevels`, `0 ∈ multistageAroLevels`, and
     `∀ eta ∈ multistageMarkovLevels, 2 ≤ eta` (even against nonlinear Borel dual-control
     signaling at stage 1).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data MeasureTheory

namespace AroProofs.BridgeG1Multistage

/-! ## Section 1: Arbitrary `k`-closure multistage dynamics, stage split, and policy classes -/

/-- Joint disturbance trajectory across all `k + 1` inter-closure intervals `len j`. -/
abbrev MultiNoise (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ) :=
  ∀ j : Fin (k + 1), D.NoiseBlock (len j)

/-- Nominal single-stage propagation (zero disturbance). -/
def stageNominal (D : Data) (l : ℕ) (x : Vec D.n) (u : D.ControlBlock l) : Vec D.n :=
  D.run x (blockAt u.val) (fun _ => 0) l

/-- Purely exogenous single-stage disturbance response (zero state, zero control). -/
def stageDeviation (D : Data) (l : ℕ) (w : D.NoiseBlock l) : Vec D.n :=
  D.run 0 (fun _ => 0) (blockAt w.val) l

/-- **Theorem G1.1:** Chronological single-stage recurrence splits additively into nominal
propagation plus purely exogenous stage deviation. -/
theorem multistage_stage_split (D : Data) (l : ℕ) (x : Vec D.n)
    (u : D.ControlBlock l) (w : D.NoiseBlock l) :
    D.run x (blockAt u.val) (blockAt w.val) l =
      stageNominal D l x u + stageDeviation D l w := by
  simpa only [stageNominal, stageDeviation, add_zero, zero_add] using
    BridgeFormalV2.Proofs.run_add D x 0 (blockAt u.val) (fun _ => 0)
      (fun _ => 0) (blockAt w.val) l

private theorem linear_map_continuous {n m : ℕ} (L : Vec n →ₗ[ℝ] Vec m) : Continuous L := by
  have hrep : ∀ x : Vec n, L x = ∑ i : Fin n, x i • L (BridgeFormalV3.basisVector i) := by
    intro x
    conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition x]
    simp only [map_sum, map_smul]
  have hfun : (L : Vec n → Vec m) =
      fun x => ∑ i : Fin n, x i • L (BridgeFormalV3.basisVector i) := funext hrep
  rw [hfun]
  refine continuous_finsetSum _ (fun i _ => (continuous_apply i).smul continuous_const)

private theorem stageNominal_continuous (D : Data) (l : ℕ) :
    Continuous (fun p : Vec D.n × D.ControlBlock l => stageNominal D l p.1 p.2) := by
  have heq : (fun p : Vec D.n × D.ControlBlock l => stageNominal D l p.1 p.2) =
      fun p => D.expansion l p.1 p.2.val (fun _ => (0 : Vec D.p)) := by
    funext ⟨x, u⟩
    have hz : blockAt (fun _ : Fin l => (0 : Vec D.p)) = (fun _ => 0) := by
      funext t; simp [blockAt]
    simpa only [stageNominal, hz] using
      BridgeFormalV2.Proofs.expansion D l x u.val (fun _ => (0 : Vec D.p))
  rw [heq]
  unfold Data.expansion
  refine (linear_map_continuous (D.A ^ l)).comp continuous_fst |>.add ?_
  refine continuous_finsetSum _ (fun t _ => ?_)
  have hlin : Continuous (fun v : Vec D.m => (D.A ^ (l - 1 - t.val)) (D.B v + D.E 0)) := by
    simp only [map_zero, add_zero]
    exact linear_map_continuous ((D.A ^ (l - 1 - t.val)).comp D.B)
  exact hlin.comp ((continuous_apply t).comp (continuous_subtype_val.comp continuous_snd))

/-- Return the last state of a prefix history, or initial state `x0` when the history is empty. -/
def lastOrInit {n : ℕ} (x0 : Vec n) : ∀ {m : ℕ}, (Fin m → Vec n) → Vec n
  | 0, _ => x0
  | _ + 1, hist => hist (Fin.last _)

private theorem lastOrInit_measurable {n m : ℕ} (x0 : Vec n) :
    Measurable (lastOrInit x0 (m := m)) := by
  cases m with
  | zero => exact measurable_const
  | succ m' => exact measurable_pi_apply (Fin.last m')

/-- Non-dependent `Fin.snoc` helper for constant codomain `β`. -/
def snocVec {β : Type*} {m : ℕ} (f : Fin m → β) (b : β) : Fin (m + 1) → β :=
  @Fin.snoc m (fun _ => β) f b

private theorem snocVec_last {β : Type*} {m : ℕ} (f : Fin m → β) (b : β) :
    snocVec f b (Fin.last m) = b :=
  @Fin.snoc_last m (fun _ => β) b f

private theorem snocVec_castSucc {β : Type*} {m : ℕ} (f : Fin m → β) (b : β) (i : Fin m) :
    snocVec f b i.castSucc = f i :=
  @Fin.snoc_castSucc m (fun _ => β) b f i

private theorem measurable_snocVec {α β : Type*} [MeasurableSpace α] [MeasurableSpace β]
    {m : ℕ} {f : α → Fin m → β} {g : α → β} (hf : Measurable f) (hg : Measurable g) :
    Measurable (fun a => snocVec (f a) (g a)) := by
  rw [measurable_pi_iff]
  intro i
  refine Fin.lastCases ?_ ?_ i
  · simpa only [snocVec_last] using hg
  · intro j
    have hfun : (fun a => snocVec (f a) (g a) j.castSucc) = (fun a => f a j) := by
      funext a; exact snocVec_castSucc (f a) (g a) j
    rw [hfun]
    exact (measurable_pi_apply j).comp hf

/-- Borel-measurable history-dependent OGU state policy: at stage `j`, observes `(x_{r_1},...,x_{r_j})`. -/
structure HistoryStatePolicy (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ) where
  rule : ∀ j : Fin (k + 1), (Fin j.val → Vec D.n) → D.ControlBlock (len j)
  borel : ∀ j : Fin (k + 1), Measurable (rule j)

/-- Borel-measurable multistage ARO policy: at stage `j`, observes exogenous `(ξ_0,...,ξ_{j-1})`. -/
structure HistoryDeviationPolicy (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ) where
  rule : ∀ j : Fin (k + 1), (Fin j.val → Vec D.n) → D.ControlBlock (len j)
  borel : ∀ j : Fin (k + 1), Measurable (rule j)

/-- Memoryless Borel-measurable Markov state-feedback policy: at stage `j > 0`, sees ONLY `x_{r_j}`. -/
structure MarkovStatePolicy (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ) where
  initControl : D.ControlBlock (len ⟨0, Nat.zero_lt_succ k⟩)
  stepRule : ∀ j : Fin k, Vec D.n → D.ControlBlock (len j.succ)
  borel : ∀ j : Fin k, Measurable (stepRule j)

/-- Embed any memoryless Markov policy into the history-dependent state policy class. -/
def MarkovStatePolicy.toHistory {D : Data} {k : ℕ} {len : Fin (k + 1) → ℕ}
    (M : MarkovStatePolicy D len) : HistoryStatePolicy D len where
  rule j hist :=
    match j, hist with
    | ⟨0, _⟩, _ => M.initControl
    | ⟨j' + 1, hj⟩, h => M.stepRule ⟨j', Nat.lt_of_succ_lt_succ hj⟩ (h (Fin.last j'))
  borel j := by
    cases j with
    | mk jv hj =>
      cases jv with
      | zero => exact measurable_const
      | succ j' =>
        exact (M.borel ⟨j', Nat.lt_of_succ_lt_succ hj⟩).comp (measurable_pi_apply (Fin.last j'))

/-! ## Section 2: Recursive rollout of states, controls, and terminal state for arbitrary `k` -/

/-- Recursively reconstruct observed state history `(x_{r_1}, ..., x_{r_m})` from exogenous
stage deviations `ξ : Fin m → Vec D.n` under a `HistoryStatePolicy P`. -/
def statesFromDevs (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) :
    ∀ m : ℕ, m ≤ k + 1 → (Fin m → Vec D.n) → (Fin m → Vec D.n)
  | 0, _, _ => Fin.elim0
  | m + 1, hm, ξ =>
    let prevHist : Fin m → Vec D.n :=
      statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc)
    let xPrev : Vec D.n := lastOrInit D.x0 prevHist
    let uCur : D.ControlBlock (len ⟨m, hm⟩) := P.rule ⟨m, hm⟩ prevHist
    let xNext : Vec D.n := stageNominal D (len ⟨m, hm⟩) xPrev uCur + ξ (Fin.last m)
    snocVec prevHist xNext

/-- Recursively recover exogenous stage deviations `(ξ_0, ..., ξ_{m-1})` from observed state
history `xHist : Fin m → Vec D.n` under a `HistoryDeviationPolicy Y`. -/
def devsFromStates (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) :
    ∀ m : ℕ, m ≤ k + 1 → (Fin m → Vec D.n) → (Fin m → Vec D.n)
  | 0, _, _ => Fin.elim0
  | m + 1, hm, xHist =>
    let prevStates : Fin m → Vec D.n := fun i => xHist i.castSucc
    let prevDevs : Fin m → Vec D.n := devsFromStates D Y m (Nat.le_of_succ_le hm) prevStates
    let xPrev : Vec D.n := lastOrInit D.x0 prevStates
    let uCur : D.ControlBlock (len ⟨m, hm⟩) := Y.rule ⟨m, hm⟩ prevDevs
    let ξCur : Vec D.n := xHist (Fin.last m) - stageNominal D (len ⟨m, hm⟩) xPrev uCur
    snocVec prevDevs ξCur

theorem statesFromDevs_measurable (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) → Measurable (statesFromDevs D P m hm)
  | 0, _ => measurable_const
  | m + 1, hm => by
    have hprev_in : Measurable (fun (ξ : Fin (m + 1) → Vec D.n) (i : Fin m) => ξ i.castSucc) := by
      rw [measurable_pi_iff]
      intro i
      exact measurable_pi_apply i.castSucc
    have hprev : Measurable (fun ξ : Fin (m + 1) → Vec D.n =>
        statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc)) :=
      (statesFromDevs_measurable D P m (Nat.le_of_succ_le hm)).comp hprev_in
    have hxPrev : Measurable (fun ξ : Fin (m + 1) → Vec D.n =>
        lastOrInit D.x0 (statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc))) :=
      (lastOrInit_measurable D.x0).comp hprev
    have huCur : Measurable (fun ξ : Fin (m + 1) → Vec D.n =>
        P.rule ⟨m, hm⟩ (statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc))) :=
      (P.borel ⟨m, hm⟩).comp hprev
    have hnom : Measurable (fun ξ : Fin (m + 1) → Vec D.n =>
        stageNominal D (len ⟨m, hm⟩)
          (lastOrInit D.x0 (statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc)))
          (P.rule ⟨m, hm⟩ (statesFromDevs D P m (Nat.le_of_succ_le hm) (fun i => ξ i.castSucc)))) :=
      (stageNominal_continuous D (len ⟨m, hm⟩)).measurable.comp (hxPrev.prodMk huCur)
    exact measurable_snocVec hprev (hnom.add (measurable_pi_apply (Fin.last m)))

theorem devsFromStates_measurable (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) → Measurable (devsFromStates D Y m hm)
  | 0, _ => measurable_const
  | m + 1, hm => by
    have hprev_in : Measurable (fun (xHist : Fin (m + 1) → Vec D.n) (i : Fin m) => xHist i.castSucc) := by
      rw [measurable_pi_iff]
      intro i
      exact measurable_pi_apply i.castSucc
    have hprev : Measurable (fun xHist : Fin (m + 1) → Vec D.n =>
        devsFromStates D Y m (Nat.le_of_succ_le hm) (fun i => xHist i.castSucc)) :=
      (devsFromStates_measurable D Y m (Nat.le_of_succ_le hm)).comp hprev_in
    have hxPrev : Measurable (fun xHist : Fin (m + 1) → Vec D.n =>
        lastOrInit D.x0 (fun i : Fin m => xHist i.castSucc)) :=
      (lastOrInit_measurable D.x0).comp hprev_in
    have huCur : Measurable (fun xHist : Fin (m + 1) → Vec D.n =>
        Y.rule ⟨m, hm⟩ (devsFromStates D Y m (Nat.le_of_succ_le hm) (fun i => xHist i.castSucc))) :=
      (Y.borel ⟨m, hm⟩).comp hprev
    have hnom : Measurable (fun xHist : Fin (m + 1) → Vec D.n =>
        stageNominal D (len ⟨m, hm⟩)
          (lastOrInit D.x0 (fun i : Fin m => xHist i.castSucc))
          (Y.rule ⟨m, hm⟩ (devsFromStates D Y m (Nat.le_of_succ_le hm) (fun i => xHist i.castSucc)))) :=
      (stageNominal_continuous D (len ⟨m, hm⟩)).measurable.comp (hxPrev.prodMk huCur)
    exact measurable_snocVec hprev ((measurable_pi_apply (Fin.last m)).sub hnom)

/-- Chronological state rollout under a `HistoryStatePolicy P` and joint noise `w`. -/
def historyStateRollout (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, m ≤ k + 1 → (Fin m → Vec D.n)
  | 0, _ => Fin.elim0
  | m + 1, hm =>
    let prevHist : Fin m → Vec D.n := historyStateRollout D P w m (Nat.le_of_succ_le hm)
    let xPrev : Vec D.n := lastOrInit D.x0 prevHist
    let uCur : D.ControlBlock (len ⟨m, hm⟩) := P.rule ⟨m, hm⟩ prevHist
    let xNext : Vec D.n := D.run xPrev (blockAt uCur.val) (blockAt (w ⟨m, hm⟩).val) (len ⟨m, hm⟩)
    snocVec prevHist xNext

/-- Chronological state rollout under a `HistoryDeviationPolicy Y` and joint noise `w`. -/
def historyAroRollout (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, m ≤ k + 1 → (Fin m → Vec D.n)
  | 0, _ => Fin.elim0
  | m + 1, hm =>
    let prevHist : Fin m → Vec D.n := historyAroRollout D Y w m (Nat.le_of_succ_le hm)
    let xPrev : Vec D.n := lastOrInit D.x0 prevHist
    let devPrefix : Fin m → Vec D.n :=
      fun i => stageDeviation D (len ⟨i.val, Nat.lt_trans i.isLt hm⟩)
        (w ⟨i.val, Nat.lt_trans i.isLt hm⟩)
    let uCur : D.ControlBlock (len ⟨m, hm⟩) := Y.rule ⟨m, hm⟩ devPrefix
    let xNext : Vec D.n := D.run xPrev (blockAt uCur.val) (blockAt (w ⟨m, hm⟩).val) (len ⟨m, hm⟩)
    snocVec prevHist xNext

/-- Terminal state `x_T` (at index `k` of the `(k+1)`-stage rollout) under `HistoryStatePolicy`. -/
def historyTerminalState (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) (w : MultiNoise D len) : Vec D.n :=
  historyStateRollout D P w (k + 1) le_rfl (Fin.last k)

/-- Terminal state `x_T` under `HistoryDeviationPolicy`. -/
def aroTerminalState (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) (w : MultiNoise D len) : Vec D.n :=
  historyAroRollout D Y w (k + 1) le_rfl (Fin.last k)

/-- Multistage OGU history-policy feasibility over arbitrary joint disturbance set `Ω`. -/
def HistoryStateBound (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) (P : HistoryStatePolicy D len) (eta : ℝ) : Prop :=
  ∀ w ∈ Ω, D.Rows eta (historyTerminalState D P w)

/-- Multistage ARO deviation-policy feasibility over arbitrary joint disturbance set `Ω`. -/
def HistoryAroBound (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) (Y : HistoryDeviationPolicy D len) (eta : ℝ) : Prop :=
  ∀ w ∈ Ω, D.Rows eta (aroTerminalState D Y w)

/-- Multistage Markov state-feedback feasibility over arbitrary joint disturbance set `Ω`. -/
def MarkovStateBound (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) (M : MarkovStatePolicy D len) (eta : ℝ) : Prop :=
  HistoryStateBound D len Ω M.toHistory eta

def multistageHistoryLevels (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) : Set ℝ :=
  {eta | ∃ P : HistoryStatePolicy D len, HistoryStateBound D len Ω P eta}

def multistageAroLevels (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) : Set ℝ :=
  {eta | ∃ Y : HistoryDeviationPolicy D len, HistoryAroBound D len Ω Y eta}

def multistageMarkovLevels (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) : Set ℝ :=
  {eta | ∃ M : MarkovStatePolicy D len, MarkovStateBound D len Ω M eta}

/-! ## Section 3: Exact multistage F2 equivalence for arbitrary `k : ℕ` and arbitrary `Ω` -/

private theorem rollout_eq_statesFromDevs (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) →
      historyStateRollout D P w m hm =
        statesFromDevs D P m hm
          (fun i : Fin m => stageDeviation D (len ⟨i.val, Nat.lt_of_lt_of_le i.isLt hm⟩)
            (w ⟨i.val, Nat.lt_of_lt_of_le i.isLt hm⟩))
  | 0, _ => by funext i; exact Fin.elim0 i
  | m + 1, hm => by
    have ih := rollout_eq_statesFromDevs D P w m (Nat.le_of_succ_le hm)
    simp only [historyStateRollout, statesFromDevs]
    rw [ih, multistage_stage_split]
    rfl

/-- Forward translation: `HistoryStatePolicy` -> `HistoryDeviationPolicy`. -/
def forwardMultiPolicy (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) : HistoryDeviationPolicy D len where
  rule j devs := P.rule j (statesFromDevs D P j.val (Nat.le_of_lt j.isLt) devs)
  borel j := (P.borel j).comp (statesFromDevs_measurable D P j.val (Nat.le_of_lt j.isLt))

private theorem forwardMultiPolicy_rollout (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) →
      historyAroRollout D (forwardMultiPolicy D P) w m hm =
        historyStateRollout D P w m hm
  | 0, _ => by funext i; exact Fin.elim0 i
  | m + 1, hm => by
    have ih := forwardMultiPolicy_rollout D P w m (Nat.le_of_succ_le hm)
    have hst := rollout_eq_statesFromDevs D P w m (Nat.le_of_succ_le hm)
    rw [historyAroRollout, historyStateRollout, ih]
    dsimp only [forwardMultiPolicy]
    rw [← hst]

/-- **Theorem G1.2:** Every Borel `HistoryStatePolicy` translates to a Borel `HistoryDeviationPolicy`
producing identical trajectories, terminal states, and epigraph bounds on ANY `Ω`. -/
theorem multistage_forward_policy (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) (P : HistoryStatePolicy D len) :
    ∃ Y : HistoryDeviationPolicy D len,
      (∀ w : MultiNoise D len, ∀ m : ℕ, (hm : m ≤ k + 1) →
        historyAroRollout D Y w m hm = historyStateRollout D P w m hm) ∧
      (∀ eta : ℝ, HistoryStateBound D len Ω P eta ↔ HistoryAroBound D len Ω Y eta) := by
  refine ⟨forwardMultiPolicy D P, fun w m hm => forwardMultiPolicy_rollout D P w m hm, ?_⟩
  intro eta
  have hterm : ∀ w : MultiNoise D len,
      aroTerminalState D (forwardMultiPolicy D P) w = historyTerminalState D P w := fun w =>
    congrFun (forwardMultiPolicy_rollout D P w (k + 1) le_rfl) (Fin.last k)
  simp only [HistoryStateBound, HistoryAroBound, hterm]

/-- Reverse translation: `HistoryDeviationPolicy` -> `HistoryStatePolicy`. -/
def reverseMultiPolicy (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) : HistoryStatePolicy D len where
  rule j states := Y.rule j (devsFromStates D Y j.val (Nat.le_of_lt j.isLt) states)
  borel j := (Y.borel j).comp (devsFromStates_measurable D Y j.val (Nat.le_of_lt j.isLt))

private theorem devsFromStates_aroRollout (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) →
      devsFromStates D Y m hm (historyAroRollout D Y w m hm) =
        fun i : Fin m => stageDeviation D (len ⟨i.val, Nat.lt_of_lt_of_le i.isLt hm⟩)
          (w ⟨i.val, Nat.lt_of_lt_of_le i.isLt hm⟩)
  | 0, _ => by funext i; exact Fin.elim0 i
  | m + 1, hm => by
    have ih := devsFromStates_aroRollout D Y w m (Nat.le_of_succ_le hm)
    simp only [devsFromStates, historyAroRollout, snocVec_castSucc, snocVec_last]
    funext i
    refine Fin.lastCases ?_ ?_ i
    · rw [snocVec_last, ih, multistage_stage_split, add_sub_cancel_left]
      rfl
    · intro j
      rw [snocVec_castSucc, ih]
      rfl

private theorem reverseMultiPolicy_rollout (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (Y : HistoryDeviationPolicy D len) (w : MultiNoise D len) :
    ∀ m : ℕ, (hm : m ≤ k + 1) →
      historyStateRollout D (reverseMultiPolicy D Y) w m hm =
        historyAroRollout D Y w m hm
  | 0, _ => by funext i; exact Fin.elim0 i
  | m + 1, hm => by
    have ih := reverseMultiPolicy_rollout D Y w m (Nat.le_of_succ_le hm)
    have hdev := devsFromStates_aroRollout D Y w m (Nat.le_of_succ_le hm)
    rw [historyStateRollout, historyAroRollout, ih]
    dsimp only [reverseMultiPolicy]
    rw [hdev]

/-- **Theorem G1.3:** Every Borel `HistoryDeviationPolicy` translates back to a Borel
`HistoryStatePolicy` producing identical trajectories, terminal states, and epigraph bounds on ANY `Ω`. -/
theorem multistage_reverse_policy (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) (Y : HistoryDeviationPolicy D len) :
    ∃ P : HistoryStatePolicy D len,
      (∀ w : MultiNoise D len, ∀ m : ℕ, (hm : m ≤ k + 1) →
        historyStateRollout D P w m hm = historyAroRollout D Y w m hm) ∧
      (∀ eta : ℝ, HistoryStateBound D len Ω P eta ↔ HistoryAroBound D len Ω Y eta) := by
  refine ⟨reverseMultiPolicy D Y, fun w m hm => reverseMultiPolicy_rollout D Y w m hm, ?_⟩
  intro eta
  have hterm : ∀ w : MultiNoise D len,
      historyTerminalState D (reverseMultiPolicy D Y) w = aroTerminalState D Y w := fun w =>
    congrFun (reverseMultiPolicy_rollout D Y w (k + 1) le_rfl) (Fin.last k)
  simp only [HistoryStateBound, HistoryAroBound, hterm]

/-- **Theorem G1.4:** Exact epigraph equality between full-history OGU and multistage ARO
for EVERY `D : Data`, EVERY `k : ℕ` (including all `k ≥ 2`), EVERY schedule `len`, and EVERY `Ω`. -/
theorem multistage_history_epigraph_eq_aro (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) :
    multistageHistoryLevels D len Ω = multistageAroLevels D len Ω := by
  apply Set.ext
  intro eta
  constructor
  · rintro ⟨P, hb⟩
    obtain ⟨Y, _, hiff⟩ := multistage_forward_policy D len Ω P
    exact ⟨Y, (hiff eta).mp hb⟩
  · rintro ⟨Y, hb⟩
    obtain ⟨P, _, hiff⟩ := multistage_reverse_policy D len Ω Y
    exact ⟨P, (hiff eta).mpr hb⟩

/-- **Theorem G1.5:** Memoryless Markov state-feedback levels are always a subset of full-history
OGU and multistage ARO levels. -/
theorem multistage_markov_subset_history (D : Data) {k : ℕ} (len : Fin (k + 1) → ℕ)
    (Ω : Set (MultiNoise D len)) :
    multistageMarkovLevels D len Ω ⊆ multistageHistoryLevels D len Ω ∧
    multistageMarkovLevels D len Ω ⊆ multistageAroLevels D len Ω := by
  have hsub : multistageMarkovLevels D len Ω ⊆ multistageHistoryLevels D len Ω := by
    rintro eta ⟨M, hm⟩
    exact ⟨M.toHistory, hm⟩
  exact ⟨hsub, by rw [← multistage_history_epigraph_eq_aro D len Ω]; exact hsub⟩

/-! ## Section 4: Concrete `k = 2` correlated witness separating Markov vs History/ARO -/

/-- 1D `BridgeFormalV2.Data` (`A=0, B=1, E=2, U=[-1,1], rho=1, H=1, [0,10], c=1`) for `k = 2` witness. -/
abbrev k2WitnessData : Data where
  n := 1
  m := 1
  p := 1
  rows := 1
  r := 1
  q := 1
  n_pos := Nat.zero_lt_one
  m_pos := Nat.zero_lt_one
  p_pos := Nat.zero_lt_one
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := 0
  B := LinearMap.id
  E := (2 : ℝ) • LinearMap.id
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => 0
  gmax := fun _ => 10
  c := LinearMap.proj 0

/-- 3-stage (`k = 2` closures) schedule with unit stage lengths `len = (1, 1, 1)`. -/
abbrev k2UnitLen : Fin 3 → ℕ := fun _ => 1

/-- Correlated `k = 2` path set: `(w_0 = 1/2 ∧ w_2 = 1/2) ∨ (w_0 = -1/2 ∧ w_2 = -1/2)`, `w_1 ∈ [-1,1]`. -/
def k2CorrelatedOmega : Set (MultiNoise k2WitnessData k2UnitLen) :=
  {w | ((w 0).val 0 0 = (1 / 2 : ℝ) ∧ (w 2).val 0 0 = (1 / 2 : ℝ)) ∨
       ((w 0).val 0 0 = (-1 / 2 : ℝ) ∧ (w 2).val 0 0 = (-1 / 2 : ℝ))}

private theorem k2_stage_run (x : Vec 1) (u : k2WitnessData.ControlBlock 1)
    (w : k2WitnessData.NoiseBlock 1) :
    k2WitnessData.run x (blockAt u.val) (blockAt w.val) 1 0 = u.val 0 0 + 2 * w.val 0 0 := by
  have hu0 : (if h : 0 < 1 then u.val ⟨0, h⟩ else 0) = u.val 0 := rfl
  have hw0 : (if h : 0 < 1 then w.val ⟨0, h⟩ else 0) = w.val 0 := rfl
  simp only [Data.run, Data.step, Data.blockAt, k2WitnessData, hu0, hw0,
    LinearMap.zero_apply, LinearMap.id_apply, LinearMap.smul_apply,
    Pi.add_apply, Pi.smul_apply, smul_eq_mul, zero_add]

private theorem historyStateRollout_last (D : Data) {k : ℕ} {len : Fin (k + 1) → ℕ}
    (P : HistoryStatePolicy D len) (w : MultiNoise D len) (m : ℕ) (hm : m + 1 ≤ k + 1) :
    historyStateRollout D P w (m + 1) hm (Fin.last m) =
      D.run (lastOrInit D.x0 (historyStateRollout D P w m (Nat.le_of_succ_le hm)))
        (blockAt (P.rule ⟨m, hm⟩ (historyStateRollout D P w m (Nat.le_of_succ_le hm))).val)
        (blockAt (w ⟨m, hm⟩).val) (len ⟨m, hm⟩) := by
  rw [historyStateRollout, snocVec_last]

/-- **Theorem G1.6:** At `k = 2` closures on correlated `k2CorrelatedOmega`, full-history OGU
and multistage ARO achieve epigraph level `0`, whereas EVERY memoryless Markov state-feedback
policy (even with arbitrary nonlinear Borel dual-control signaling at stage 1) satisfies `2 ≤ eta`. -/
theorem exists_markov_strictly_weaker_than_history_k2 :
    (0 : ℝ) ∈ multistageHistoryLevels k2WitnessData k2UnitLen k2CorrelatedOmega ∧
    (0 : ℝ) ∈ multistageAroLevels k2WitnessData k2UnitLen k2CorrelatedOmega ∧
    ∀ eta ∈ multistageMarkovLevels k2WitnessData k2UnitLen k2CorrelatedOmega, (2 : ℝ) ≤ eta := by
  have h0_hist : (0 : ℝ) ∈ multistageHistoryLevels k2WitnessData k2UnitLen k2CorrelatedOmega := by
    classical
    let zeroBlock : k2WitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let negOneBlock : k2WitnessData.ControlBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let posOneBlock : k2WitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let P : HistoryStatePolicy k2WitnessData k2UnitLen :=
      { rule := fun j hist =>
          match j, hist with
          | ⟨0, _⟩, _ => zeroBlock
          | ⟨1, _⟩, _ => zeroBlock
          | ⟨2, _⟩, h => if (0 : ℝ) ≤ h (0 : Fin 2) 0 then negOneBlock else posOneBlock
        borel := fun j => by
          fin_cases j
          · exact measurable_const
          · exact measurable_const
          · have hset : MeasurableSet {hist : Fin 2 → Vec 1 | (0 : ℝ) ≤ hist (0 : Fin 2) 0} := by
              have hcont : Continuous (fun hist : Fin 2 → Vec 1 => hist (0 : Fin 2) 0) :=
                (continuous_apply (0 : Fin 1)).comp (continuous_apply (0 : Fin 2))
              exact (isClosed_le continuous_const hcont).measurableSet
            exact Measurable.ite hset measurable_const measurable_const }
    refine ⟨P, ?_⟩
    intro w hw
    have hx1 : historyStateRollout k2WitnessData P w 1 (by omega) (Fin.last 0) 0 =
        2 * (w 0).val 0 0 := by
      rw [historyStateRollout_last, k2_stage_run]
      change (0 : ℝ) + 2 * (w 0).val 0 0 = 2 * (w 0).val 0 0
      ring
    have hhist2_0 : historyStateRollout k2WitnessData P w 2 (by omega) (0 : Fin 2) 0 =
        2 * (w 0).val 0 0 := by
      have hcast : (0 : Fin 2) = (Fin.last 0).castSucc := rfl
      rw [hcast, historyStateRollout, snocVec_castSucc]
      exact hx1
    have hterm : historyTerminalState k2WitnessData P w 0 =
        (if (0 : ℝ) ≤ 2 * (w 0).val 0 0 then (-1 : ℝ) else 1) + 2 * (w 2).val 0 0 := by
      unfold historyTerminalState
      rw [historyStateRollout_last, k2_stage_run]
      change (if (0 : ℝ) ≤ historyStateRollout k2WitnessData P w 2 (by omega) (0 : Fin 2) 0
        then negOneBlock else posOneBlock).val 0 0 + 2 * (w 2).val 0 0 = _
      rw [hhist2_0]
      split_ifs <;> rfl
    have hval0 : historyTerminalState k2WitnessData P w 0 = 0 := by
      rw [hterm]
      rcases hw with ⟨hw0, hw2⟩ | ⟨hw0, hw2⟩
      · rw [hw0, hw2]; norm_num
      · rw [hw0, hw2]; norm_num
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (0 : ℝ) ≤ historyTerminalState k2WitnessData P w 0 ∧
        historyTerminalState k2WitnessData P w 0 ≤ 10
      rw [hval0]; norm_num
    · change historyTerminalState k2WitnessData P w 0 ≤ 0
      rw [hval0]
  have h0_aro : (0 : ℝ) ∈ multistageAroLevels k2WitnessData k2UnitLen k2CorrelatedOmega := by
    rw [← multistage_history_epigraph_eq_aro]; exact h0_hist
  refine ⟨h0_hist, h0_aro, ?_⟩
  rintro eta ⟨M, hM⟩
  let u0 : ℝ := M.initControl.val 0 0
  let x1p : Vec 1 := fun _ => u0 + 1
  let x1m : Vec 1 := fun _ => u0 - 1
  let ap : ℝ := (M.stepRule 0 x1p).val 0 0
  let am : ℝ := (M.stepRule 0 x1m).val 0 0
  have hap : (-1 : ℝ) ≤ ap ∧ ap ≤ 1 := (M.stepRule 0 x1p).property 0 0
  have ham : (-1 : ℝ) ≤ am ∧ am ≤ 1 := (M.stepRule 0 x1m).property 0 0
  let mkN : ∀ v : ℝ, (-1 : ℝ) ≤ v → v ≤ 1 → k2WitnessData.NoiseBlock 1 :=
    fun v hv1 hv2 => ⟨fun _ _ => v, fun _ _ => ⟨hv1, hv2⟩⟩
  let w1p : k2WitnessData.NoiseBlock 1 :=
    mkN ((am - ap) / 4) (by linarith) (by linarith)
  let w1m : k2WitnessData.NoiseBlock 1 :=
    mkN ((ap - am) / 4) (by linarith) (by linarith)
  let wHalfP : k2WitnessData.NoiseBlock 1 := mkN (1 / 2) (by norm_num) (by norm_num)
  let wHalfM : k2WitnessData.NoiseBlock 1 := mkN (-1 / 2) (by norm_num) (by norm_num)
  let wp : MultiNoise k2WitnessData k2UnitLen := fun j =>
    match j with
    | ⟨0, _⟩ => wHalfP
    | ⟨1, _⟩ => w1p
    | ⟨2, _⟩ => wHalfP
  let wm : MultiNoise k2WitnessData k2UnitLen := fun j =>
    match j with
    | ⟨0, _⟩ => wHalfM
    | ⟨1, _⟩ => w1m
    | ⟨2, _⟩ => wHalfM
  have hwp_mem : wp ∈ k2CorrelatedOmega := Or.inl ⟨rfl, rfl⟩
  have hwm_mem : wm ∈ k2CorrelatedOmega := Or.inr ⟨rfl, rfl⟩
  have hx1_wp : historyStateRollout k2WitnessData M.toHistory wp 1 (by omega) (Fin.last 0) = x1p := by
    ext i; have hi : i = 0 := Fin.eq_zero i; subst hi
    rw [historyStateRollout_last, k2_stage_run]
    change u0 + 2 * (1 / 2 : ℝ) = u0 + 1; ring
  have hx1_wm : historyStateRollout k2WitnessData M.toHistory wm 1 (by omega) (Fin.last 0) = x1m := by
    ext i; have hi : i = 0 := Fin.eq_zero i; subst hi
    rw [historyStateRollout_last, k2_stage_run]
    change u0 + 2 * (-1 / 2 : ℝ) = u0 - 1; ring
  have hx2_eq :
      historyStateRollout k2WitnessData M.toHistory wp 2 (by omega) (Fin.last 1) =
      historyStateRollout k2WitnessData M.toHistory wm 2 (by omega) (Fin.last 1) := by
    ext i; have hi : i = 0 := Fin.eq_zero i; subst hi
    rw [historyStateRollout_last, historyStateRollout_last, k2_stage_run, k2_stage_run]
    have hctrl_p : (M.toHistory.rule ⟨1, by omega⟩
        (historyStateRollout k2WitnessData M.toHistory wp 1 (by omega))).val 0 0 = ap := by
      change (M.stepRule 0 (historyStateRollout k2WitnessData M.toHistory wp 1 (by omega) (Fin.last 0))).val 0 0 = ap
      rw [hx1_wp]
    have hctrl_m : (M.toHistory.rule ⟨1, by omega⟩
        (historyStateRollout k2WitnessData M.toHistory wm 1 (by omega))).val 0 0 = am := by
      change (M.stepRule 0 (historyStateRollout k2WitnessData M.toHistory wm 1 (by omega) (Fin.last 0))).val 0 0 = am
      rw [hx1_wm]
    rw [hctrl_p, hctrl_m]
    change ap + 2 * ((am - ap) / 4) = am + 2 * ((ap - am) / 4)
    ring
  let bColl : ℝ :=
    (M.stepRule 1 (historyStateRollout k2WitnessData M.toHistory wp 2 (by omega) (Fin.last 1))).val 0 0
  have hterm_wp : historyTerminalState k2WitnessData M.toHistory wp 0 = bColl + 1 := by
    unfold historyTerminalState
    rw [historyStateRollout_last, k2_stage_run]
    change bColl + 2 * (1 / 2 : ℝ) = bColl + 1; ring
  have hterm_wm : historyTerminalState k2WitnessData M.toHistory wm 0 = bColl - 1 := by
    unfold historyTerminalState
    rw [historyStateRollout_last, k2_stage_run]
    have hb_eq : (M.toHistory.rule ⟨2, by omega⟩
        (historyStateRollout k2WitnessData M.toHistory wm 2 (by omega))).val 0 0 = bColl := by
      change (M.stepRule 1 (historyStateRollout k2WitnessData M.toHistory wm 2 (by omega) (Fin.last 1))).val 0 0 = bColl
      rw [← hx2_eq]
    rw [hb_eq]
    change bColl + 2 * (-1 / 2 : ℝ) = bColl - 1; ring
  have hlo : (0 : ℝ) ≤ historyTerminalState k2WitnessData M.toHistory wm 0 := ((hM wm hwm_mem).1 0).1
  have hcost : historyTerminalState k2WitnessData M.toHistory wp 0 ≤ eta := (hM wp hwp_mem).2
  rw [hterm_wm] at hlo
  rw [hterm_wp] at hcost
  linarith

end AroProofs.BridgeG1Multistage
