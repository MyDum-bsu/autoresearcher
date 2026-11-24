import AroProofs.BridgeF4CornerLP

/-!
# O4: Value of Measurement, Zero-Gain Necessary Conditions, and Strict Separation Criterion

Live Scientific Discovery Run-01 (`conj-o4-closure-scheduling`) built strictly over the frozen
core `BridgeFormalV2.Model` / `BridgeFormalV2.Goals`, F3 `BridgeFormalV3.Proofs.Support`, and
F4 `BridgeF4CornerLP`.

Main theorems (zero `sorry`, zero custom axioms):
  1. `openLoop_subset_aro` & `openLoop_subset_source`: Epigraph monotonicity (`V({r}) ≤ V(∅)`).
  2. `zero_gain_of_unconstrained_terminal`: When `D.rows = 0` (no terminal state constraints),
     `D.aroLevels = openLoopLevels D` and `D.sourceLevels = openLoopLevels D` for EVERY `D : Data`
     (nonempty terminal constraints `D.rows > 0` are necessary for positive value of measurement).
  3. `zero_gain_of_prefix_in_terminal_kernel`: When `D.H (D.A^q (D.deviation w)) = 0` and
     `D.c (D.A^q (D.deviation w)) = 0` for all `w`, `D.aroLevels = openLoopLevels D`
     and `D.sourceLevels = openLoopLevels D`.
  4. `openLoop_eq_shared_corner_lp`: Exact characterization of open-loop feasibility as the
     shared-control restriction of the finite `2^(r*p)` corner LP.
  5. `strict_gain_iff_corner_separation`: Exact finite-dimensional necessary-and-sufficient
     criterion for strict epigraph separation `eta ∈ D.aroLevels \ openLoopLevels D`.
  6. `exists_strict_value_of_measurement_gap`: Concrete `BridgeFormalV2.Data` witness proving
     `2 ∈ D.sourceLevels`, `2 ∈ D.aroLevels`, and `∀ eta ∈ openLoopLevels D, 4 ≤ eta`
     (machine-checked strict measurement gain `V(∅) - V({1}) ≥ 2`).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 AroProofs.BridgeF4VertexLP

namespace AroProofs.BridgeO4ClosureValue

/-! ## Section 1: Open-loop levels and epigraph monotonicity -/

/-- Constant (non-adaptive / open-loop) deviation policy choosing fixed suffix block `b`. -/
def constPolicy (D : Data) (b : D.ControlBlock D.q) : D.DeviationPolicy :=
  ⟨fun _ => b, measurable_const⟩

/-- Open-loop feasibility at epigraph level `eta`: fixed prefix `a` and fixed suffix `b`. -/
def OpenLoopBound (D : Data) (a : D.ControlBlock D.r) (b : D.ControlBlock D.q) (eta : ℝ) : Prop :=
  D.AROBound a (constPolicy D b) eta

/-- Epigraph level set of open-loop (`R = ∅`) guaranteed control. -/
def openLoopLevels (D : Data) : Set ℝ :=
  {eta | ∃ a : D.ControlBlock D.r, ∃ b : D.ControlBlock D.q, OpenLoopBound D a b eta}

/-- **Theorem O4.1a:** Single-closure ARO epigraph contains all open-loop levels (`V({r}) ≤ V(∅)`). -/
theorem openLoop_subset_aro (D : Data) : openLoopLevels D ⊆ D.aroLevels := by
  rintro eta ⟨a, b, hb⟩
  exact ⟨a, constPolicy D b, hb⟩

/-- **Theorem O4.1b:** Single-closure OGU epigraph contains all open-loop levels (`V({r}) ≤ V(∅)`). -/
theorem openLoop_subset_source (D : Data) : openLoopLevels D ⊆ D.sourceLevels := by
  rw [BridgeFormalV2.Proofs.epigraph_equality D]
  exact openLoop_subset_aro D

/-! ## Section 2: Zero-gain necessary conditions for strict value of measurement -/

/-- Suffix control column `A^{q - 1 - t} B e_j`. -/
def suffixControlColumn (D : Data) (t : Fin D.q) (j : Fin D.m) : Vec D.n :=
  (D.A ^ (D.q - 1 - t.val)) (D.B (BridgeFormalV3.basisVector j))

private theorem nominal_terminal_cost_split (D : Data) (a : D.ControlBlock D.r)
    (xi : Vec D.n) (b : D.ControlBlock D.q) :
    D.c (D.expansion D.q (D.nominal a + xi) b.val 0) =
      D.c ((D.A ^ D.q) (D.nominal a + xi)) +
        ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * b.val t j := by
  simp only [Data.expansion, Pi.zero_apply, map_zero, add_zero, map_add, map_sum]
  congr 1
  apply Finset.sum_congr rfl
  intro t _
  conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition (b.val t)]
  simp only [map_sum, map_smul, suffixControlColumn, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro j _
  exact mul_comm _ _

/-- **Theorem O4.2:** When `D.rows = 0` (unconstrained terminal state, pure box controls and
linear cost), adding a closure at `r` gives ZERO value of measurement:
`D.aroLevels = openLoopLevels D` and `D.sourceLevels = openLoopLevels D`. -/
theorem zero_gain_of_unconstrained_terminal (D : Data) (hrows : D.rows = 0) :
    D.aroLevels = openLoopLevels D ∧ D.sourceLevels = openLoopLevels D := by
  classical
  have haro : D.aroLevels = openLoopLevels D := by
    apply Set.Subset.antisymm _ (openLoop_subset_aro D)
    rintro eta ⟨a, y, haro⟩
    have htight := (BridgeFormalV3.Proofs.exact_tightening D a y eta).mp haro
    let bStar : D.ControlBlock D.q :=
      ⟨fun t j => if 0 ≤ D.c (suffixControlColumn D t j) then D.umin j else D.umax j, by
        intro t j
        dsimp only
        split_ifs
        · exact ⟨le_rfl, D.control_nonempty j⟩
        · exact ⟨D.control_nonempty j, le_rfl⟩⟩
    have hcost_le : ∀ (b : D.ControlBlock D.q),
        ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * bStar.val t j ≤
          ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * b.val t j := by
      intro b
      refine Finset.sum_le_sum (fun t _ => Finset.sum_le_sum (fun j _ => ?_))
      dsimp only [bStar]
      split_ifs with hpos
      · exact mul_le_mul_of_nonneg_left (b.property t j).1 hpos
      · exact mul_le_mul_of_nonpos_left (b.property t j).2 (le_of_not_ge hpos)
    refine ⟨a, bStar, (BridgeFormalV3.Proofs.exact_tightening D a (constPolicy D bStar) eta).mpr ?_⟩
    intro xi
    constructor
    · intro i
      exact absurd i.isLt (by omega)
    · have hy_cost := (htight xi).2
      change D.c (D.expansion D.q (D.nominal a + xi.val) bStar.val 0) + D.futureRowSupport D.c ≤ eta
      change D.c (D.expansion D.q (D.nominal a + xi.val) (y.rule xi).val 0) +
        D.futureRowSupport D.c ≤ eta at hy_cost
      rw [nominal_terminal_cost_split] at hy_cost ⊢
      have hcmp := hcost_le (y.rule xi)
      linarith
  exact ⟨haro, by rw [BridgeFormalV2.Proofs.epigraph_equality D]; exact haro⟩

/-- **Theorem O4.3:** If every prefix deviation lies in `ker(H A^q) ∩ ker(c A^q)`, then
a closure at `r` gives ZERO value of measurement (`D.aroLevels = openLoopLevels D` and
`D.sourceLevels = openLoopLevels D`). -/
theorem zero_gain_of_prefix_in_terminal_kernel (D : Data)
    (hH : ∀ w : D.NoiseBlock D.r, D.H ((D.A ^ D.q) (D.deviation w)) = 0)
    (hc : ∀ w : D.NoiseBlock D.r, D.c ((D.A ^ D.q) (D.deviation w)) = 0) :
    D.aroLevels = openLoopLevels D ∧ D.sourceLevels = openLoopLevels D := by
  have haro : D.aroLevels = openLoopLevels D := by
    apply Set.Subset.antisymm _ (openLoop_subset_aro D)
    rintro eta ⟨a, y, haro⟩
    have htight := (BridgeFormalV3.Proofs.exact_tightening D a y eta).mp haro
    let w0 : D.NoiseBlock D.r :=
      ⟨fun _ => 0, fun _ _ => ⟨neg_nonpos.mpr (le_of_lt D.rho_pos), le_of_lt D.rho_pos⟩⟩
    let xi0 : D.Z := D.observedDeviation w0
    let b0 : D.ControlBlock D.q := y.rule xi0
    have hH_xi : ∀ xi : D.Z, D.H ((D.A ^ D.q) xi.val) = 0 := by
      intro xi
      rcases xi.property with ⟨w, hw⟩
      rw [← hw]
      exact hH w
    have hc_xi : ∀ xi : D.Z, D.c ((D.A ^ D.q) xi.val) = 0 := by
      intro xi
      rcases xi.property with ⟨w, hw⟩
      rw [← hw]
      exact hc w
    have hH_indep : ∀ xi : D.Z,
        D.H (D.expansion D.q (D.nominal a + xi.val) b0.val 0) =
          D.H (D.expansion D.q (D.nominal a + xi0.val) b0.val 0) := by
      intro xi
      simp only [Data.expansion, map_add, hH_xi xi, hH_xi xi0, add_zero]
    have hc_indep : ∀ xi : D.Z,
        D.c (D.expansion D.q (D.nominal a + xi.val) b0.val 0) =
          D.c (D.expansion D.q (D.nominal a + xi0.val) b0.val 0) := by
      intro xi
      simp only [Data.expansion, map_add, hc_xi xi, hc_xi xi0, add_zero]
    refine ⟨a, b0, (BridgeFormalV3.Proofs.exact_tightening D a (constPolicy D b0) eta).mpr ?_⟩
    intro xi
    have h0 := htight xi0
    constructor
    · intro i
      have h0i := h0.1 i
      have hHi : D.H (D.expansion D.q (D.nominal a + xi.val) b0.val 0) i =
          D.H (D.expansion D.q (D.nominal a + xi0.val) b0.val 0) i :=
        congrFun (hH_indep xi) i
      change (-(D.H (D.expansion D.q (D.nominal a + xi.val) b0.val 0) i) +
          D.futureRowSupport (-(D.terminalRow i)) ≤ -D.gmin i) ∧
        (D.H (D.expansion D.q (D.nominal a + xi.val) b0.val 0) i +
          D.futureRowSupport (D.terminalRow i) ≤ D.gmax i)
      rw [hHi]
      exact h0i
    · have h0c := h0.2
      change D.c (D.expansion D.q (D.nominal a + xi.val) b0.val 0) + D.futureRowSupport D.c ≤ eta
      rw [hc_indep xi]
      exact h0c
  exact ⟨haro, by rw [BridgeFormalV2.Proofs.epigraph_equality D]; exact haro⟩

/-! ## Section 3: Exact finite corner-LP characterization of open-loop & strict separation -/

/-- Shared-control finite corner LP: a single suffix block `b` must satisfy all `2^(r*p)` corners. -/
def SharedCornerLPBound (D : Data) (a : D.ControlBlock D.r)
    (b : D.ControlBlock D.q) (eta : ℝ) : Prop :=
  ∀ σ : Corner D, TightenedAt D a (D.deviation (cornerNoise D σ)) b eta

/-- **Theorem O4.4:** Open-loop feasibility is equivalent to the shared-control finite corner LP. -/
theorem openLoop_eq_shared_corner_lp (D : Data) :
    openLoopLevels D = {eta | ∃ a : D.ControlBlock D.r, ∃ b : D.ControlBlock D.q,
      SharedCornerLPBound D a b eta} := by
  apply Set.ext
  intro eta
  constructor
  · rintro ⟨a, b, hb⟩
    have htight := (BridgeFormalV3.Proofs.exact_tightening D a (constPolicy D b) eta).mp hb
    refine ⟨a, b, ?_⟩
    intro σ
    exact htight (D.observedDeviation (cornerNoise D σ))
  · rintro ⟨a, b, hshared⟩
    refine ⟨a, b, (BridgeFormalV3.Proofs.exact_tightening D a (constPolicy D b) eta).mpr ?_⟩
    intro xi
    rcases xi.property with ⟨w, hw⟩
    have hw_flat : ∀ k, -D.rho ≤ blockToFlat w.val k ∧ blockToFlat w.val k ≤ D.rho := by
      intro k
      exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
    have hα : ∀ σ : Corner D, 0 ≤ baryWeight D.rho σ (blockToFlat w.val) :=
      fun σ => baryWeight_nonneg D.rho_pos σ _ hw_flat
    have hsum1 : ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) = 1 :=
      sum_baryWeight D.rho_pos (blockToFlat w.val)
    have hz : D.aroNominalTerminal a (constPolicy D b) xi =
        ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) •
          D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σ)) b.val 0 := by
      change D.expansion D.q (D.nominal a + xi.val) b.val 0 = _
      rw [← hw]
      have hsum_nom : D.nominal a =
          ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) • D.nominal a := by
        rw [← Finset.sum_smul, hsum1, one_smul]
      have hdev : D.deviation w =
          ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) •
            D.deviation (cornerNoise D σ) := (deviation_barycentric D w).symm
      have hsum_b : ∑ t : Fin D.q, (D.A ^ (D.q - 1 - t.val)) (D.B (b.val t)) =
          ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) •
            ∑ t : Fin D.q, (D.A ^ (D.q - 1 - t.val)) (D.B (b.val t)) := by
        rw [← Finset.sum_smul, hsum1, one_smul]
      simp only [Data.expansion, Pi.zero_apply, map_zero, add_zero]
      conv_lhs => rw [hsum_nom, hdev, hsum_b]
      simp only [← Finset.sum_add_distrib, ← smul_add, map_sum, map_smul]
    rw [hz]
    constructor
    · intro i
      constructor
      · exact linear_ineq_convex_comb _ hα hsum1 (-(D.terminalRow i)) _ _ _
          (fun σ => ((hshared σ).1 i).1)
      · exact linear_ineq_convex_comb _ hα hsum1 (D.terminalRow i) _ _ _
          (fun σ => ((hshared σ).1 i).2)
    · exact linear_ineq_convex_comb _ hα hsum1 D.c _ _ _ (fun σ => (hshared σ).2)

/-- **Theorem O4.5:** Exact finite-dimensional necessary-and-sufficient criterion for strict
value of measurement at epigraph level `eta`: `eta ∈ D.aroLevels \ openLoopLevels D` iff
the adaptive corner LP is feasible at `eta` while every shared open-loop pair `(a, b)` fails
at some corner `σ : Corner D`. -/
theorem strict_gain_iff_corner_separation (D : Data) (eta : ℝ) :
    (eta ∈ D.aroLevels ∧ eta ∉ openLoopLevels D) ↔
      (∃ a : D.ControlBlock D.r, ∃ uVert : Corner D → D.ControlBlock D.q,
        VertexLPBound D a uVert eta) ∧
      (∀ a : D.ControlBlock D.r, ∀ b : D.ControlBlock D.q,
        ∃ σ : Corner D, ¬ TightenedAt D a (D.deviation (cornerNoise D σ)) b eta) := by
  rw [← vertex_lp_epigraph_eq_aro D, openLoop_eq_shared_corner_lp D]
  simp only [vertexLPLevels, Set.mem_ofPred_eq, SharedCornerLPBound, not_exists, not_forall]

/-! ## Section 4: Concrete formal witness of strict value of measurement (`V(∅) ≥ 4 > 2 ≥ V({1})`) -/

/-- Concrete 1D `BridgeFormalV2.Data` witness (`A=2, B=1, E=1, U=[-1,1], rho=1, H=1, [-2,4], c=1`). -/
abbrev strictGainWitnessData : Data where
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
  A := (2 : ℝ) • LinearMap.id
  B := LinearMap.id
  E := LinearMap.id
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => -2
  gmax := fun _ => 4
  c := LinearMap.proj 0

private theorem witness_terminal_formula (a : strictGainWitnessData.ControlBlock 1)
    (b : strictGainWitnessData.ControlBlock 1)
    (wm : strictGainWitnessData.NoiseBlock 1) (wp : strictGainWitnessData.NoiseBlock 1) :
    strictGainWitnessData.expansion 1
      (strictGainWitnessData.nominal a + strictGainWitnessData.deviation wm) b.val wp.val 0 =
      2 * a.val 0 0 + b.val 0 0 + 2 * wm.val 0 0 + wp.val 0 0 := by
  have hd0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    strictGainWitnessData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    hd0, hw0, Module.End.one_apply, LinearMap.smul_apply, LinearMap.id_apply,
    Pi.add_apply, Pi.smul_apply, Pi.zero_apply, smul_eq_mul, zero_add, add_zero, mul_zero]
  ring

/-- **Theorem O4.6:** Strict value of measurement exists within frozen `BridgeFormalV2.Data`:
on `strictGainWitnessData`, level `2` is achievable with a single closure (`2 ∈ D.sourceLevels`
and `2 ∈ D.aroLevels`), whereas EVERY open-loop level satisfies `4 ≤ eta` (exact gap `≥ 2`). -/
theorem exists_strict_value_of_measurement_gap :
    ∃ D : Data, (2 : ℝ) ∈ D.sourceLevels ∧ (2 : ℝ) ∈ D.aroLevels ∧
      ∀ eta ∈ openLoopLevels D, (4 : ℝ) ≤ eta := by
  refine ⟨strictGainWitnessData, ?_, ?_, ?_⟩
  · -- First prove 2 ∈ aroLevels, then transport to sourceLevels via F2 epigraph_equality
    have h2_aro : (2 : ℝ) ∈ strictGainWitnessData.aroLevels := by
      let a0 : strictGainWitnessData.ControlBlock 1 :=
        ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
      let yRule : strictGainWitnessData.Z → strictGainWitnessData.ControlBlock 1 := fun xi =>
        ⟨fun _ _ => -xi.val 0, by
          intro t i
          rcases xi.property with ⟨wm, hwm⟩
          have hxi : xi.val 0 = wm.val 0 0 := by
            rw [← hwm]
            simp [Data.deviation, Data.run, Data.step, Data.blockAt, strictGainWitnessData]
          have hwm_bd := wm.property 0 0
          change (-1 : ℝ) ≤ -xi.val 0 ∧ -xi.val 0 ≤ 1
          rw [hxi]
          have h1 : (-1 : ℝ) ≤ wm.val 0 0 := hwm_bd.1
          have h2 : wm.val 0 0 ≤ 1 := hwm_bd.2
          constructor <;> linarith⟩
      have hy_meas : Measurable yRule := by
        refine Measurable.subtype_mk ?_
        rw [measurable_pi_iff]; intro _
        rw [measurable_pi_iff]; intro _
        exact ((continuous_apply (0 : Fin 1)).comp continuous_subtype_val).neg.measurable
      let y0 : strictGainWitnessData.DeviationPolicy := ⟨yRule, hy_meas⟩
      refine ⟨a0, y0, ?_⟩
      intro xi wp
      rcases xi.property with ⟨wm, hwm⟩
      have hterm : strictGainWitnessData.aroTerminal a0 y0 xi wp 0 =
          wm.val 0 0 + wp.val 0 0 := by
        have hxi_val : xi.val = strictGainWitnessData.deviation wm := hwm.symm
        have hxi0 : xi.val 0 = wm.val 0 0 := by
          rw [hxi_val]
          simp [Data.deviation, Data.run, Data.step, Data.blockAt, strictGainWitnessData]
        change strictGainWitnessData.expansion 1
          (strictGainWitnessData.nominal a0 + xi.val) (y0.rule xi).val wp.val 0 = _
        rw [hxi_val, witness_terminal_formula a0 (y0.rule xi) wm wp]
        have ha0 : a0.val 0 0 = 0 := rfl
        have hb0 : (y0.rule xi).val 0 0 = -wm.val 0 0 := by
          change -xi.val 0 = -wm.val 0 0; rw [hxi0]
        rw [ha0, hb0]; ring
      have hwm_bd := wm.property 0 0
      have hwp_bd := wp.property 0 0
      have hw1 : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := hwm_bd
      have hw2 : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := hwp_bd
      constructor
      · intro i
        have hi : i = 0 := Fin.eq_zero i
        subst hi
        change (-2 : ℝ) ≤ strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ∧
          strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ≤ 4
        rw [hterm]; constructor <;> linarith
      · change strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ≤ 2
        rw [hterm]; linarith
    rw [BridgeFormalV2.Proofs.epigraph_equality strictGainWitnessData]
    exact h2_aro
  · -- 2 ∈ aroLevels (same witness)
    let a0 : strictGainWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let yRule : strictGainWitnessData.Z → strictGainWitnessData.ControlBlock 1 := fun xi =>
      ⟨fun _ _ => -xi.val 0, by
        intro t i
        rcases xi.property with ⟨wm, hwm⟩
        have hxi : xi.val 0 = wm.val 0 0 := by
          rw [← hwm]
          simp [Data.deviation, Data.run, Data.step, Data.blockAt, strictGainWitnessData]
        have hwm_bd := wm.property 0 0
        change (-1 : ℝ) ≤ -xi.val 0 ∧ -xi.val 0 ≤ 1
        rw [hxi]
        have h1 : (-1 : ℝ) ≤ wm.val 0 0 := hwm_bd.1
        have h2 : wm.val 0 0 ≤ 1 := hwm_bd.2
        constructor <;> linarith⟩
    have hy_meas : Measurable yRule := by
      refine Measurable.subtype_mk ?_
      rw [measurable_pi_iff]; intro _
      rw [measurable_pi_iff]; intro _
      exact ((continuous_apply (0 : Fin 1)).comp continuous_subtype_val).neg.measurable
    let y0 : strictGainWitnessData.DeviationPolicy := ⟨yRule, hy_meas⟩
    refine ⟨a0, y0, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hterm : strictGainWitnessData.aroTerminal a0 y0 xi wp 0 =
        wm.val 0 0 + wp.val 0 0 := by
      have hxi_val : xi.val = strictGainWitnessData.deviation wm := hwm.symm
      have hxi0 : xi.val 0 = wm.val 0 0 := by
        rw [hxi_val]
        simp [Data.deviation, Data.run, Data.step, Data.blockAt, strictGainWitnessData]
      change strictGainWitnessData.expansion 1
        (strictGainWitnessData.nominal a0 + xi.val) (y0.rule xi).val wp.val 0 = _
      rw [hxi_val, witness_terminal_formula a0 (y0.rule xi) wm wp]
      have ha0 : a0.val 0 0 = 0 := rfl
      have hb0 : (y0.rule xi).val 0 0 = -wm.val 0 0 := by
        change -xi.val 0 = -wm.val 0 0; rw [hxi0]
      rw [ha0, hb0]; ring
    have hwm_bd := wm.property 0 0
    have hwp_bd := wp.property 0 0
    have hw1 : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := hwm_bd
    have hw2 : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := hwp_bd
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-2 : ℝ) ≤ strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ∧
        strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ≤ 4
      rw [hterm]; constructor <;> linarith
    · change strictGainWitnessData.aroTerminal a0 y0 xi wp 0 ≤ 2
      rw [hterm]; linarith
  · -- Every open-loop level eta satisfies 4 ≤ eta
    rintro eta ⟨a, b, hb⟩
    let wNeg : strictGainWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wPos : strictGainWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    have hlo := (hb (strictGainWitnessData.observedDeviation wNeg) wNeg).1 0
    have hcost := (hb (strictGainWitnessData.observedDeviation wPos) wPos).2
    change (-2 : ℝ) ≤ strictGainWitnessData.expansion 1
      (strictGainWitnessData.nominal a + strictGainWitnessData.deviation wNeg) b.val wNeg.val 0 ∧
      _ at hlo
    change strictGainWitnessData.expansion 1
      (strictGainWitnessData.nominal a + strictGainWitnessData.deviation wPos) b.val wPos.val 0 ≤
      eta at hcost
    rw [witness_terminal_formula a b wNeg wNeg] at hlo
    rw [witness_terminal_formula a b wPos wPos] at hcost
    have hn : wNeg.val 0 0 = -1 := rfl
    have hp : wPos.val 0 0 = 1 := rfl
    rw [hn] at hlo
    rw [hp] at hcost
    linarith [hlo.1, hcost]

end AroProofs.BridgeO4ClosureValue
