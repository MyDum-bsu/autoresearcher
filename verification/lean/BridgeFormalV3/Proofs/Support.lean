import BridgeFormalV3.Goals

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data

namespace BridgeFormalV3.Proofs

/-- The zero input is an algebraic sequence, not a bounded physical control. -/
theorem response_expansion (D : Data) (wp : D.NoiseBlock D.q) :
    D.futureNoiseResponse wp = D.expansion D.q 0 (fun _ => 0) wp.val := by
  have hz : blockAt (fun _ : Fin D.q => (0 : Vec D.m)) = (fun _ => 0) := by
    funext t
    simp [blockAt]
  simpa only [hz, Data.futureNoiseResponse] using BridgeFormalV2.Proofs.expansion D D.q (0 : Vec D.n)
    (fun _ => (0 : Vec D.m)) wp.val

 theorem future_expansion : FutureExpansionGoal := by
  intro D a y xi wp
  rw [Data.aroTerminal, Data.aroNominalTerminal, response_expansion]
  simp only [Data.expansion, Pi.zero_apply, map_zero, zero_add, add_zero,
    map_add, Finset.sum_add_distrib]
  abel

 theorem basis_decomposition {p : ℕ} (v : Vec p) :
    v = ∑ i : Fin p, v i • basisVector i := by
  classical
  ext j
  simp [basisVector, Finset.sum_apply, Pi.smul_apply]

 theorem response_row (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ)
    (wp : D.NoiseBlock D.q) :
    row (D.futureNoiseResponse wp) =
      ∑ t : Fin D.q, ∑ i : Fin D.p, row (D.futureNoiseColumn t i) * wp.val t i := by
  rw [response_expansion]
  simp only [Data.expansion, map_zero, zero_add, map_sum]
  apply Finset.sum_congr rfl
  intro t _
  conv_lhs => rw [basis_decomposition (wp.val t)]
  simp only [map_sum, map_smul, Data.futureNoiseColumn, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  exact mul_comm _ _

 theorem coefficient_bound (D : Data) (b w : ℝ)
    (hw : -D.rho ≤ w ∧ w ≤ D.rho) : b * w ≤ D.rho * |b| := by
  by_cases hb : 0 ≤ b
  · rw [abs_of_nonneg hb, mul_comm D.rho]
    exact mul_le_mul_of_nonneg_left hw.2 hb
  · have hn : b ≤ 0 := le_of_not_ge hb
    rw [abs_of_nonpos hn]
    have hh := mul_le_mul_of_nonpos_left hw.1 hn
    nlinarith

 theorem attained_support : AttainedSupportGoal := by
  classical
  intro D row
  constructor
  · intro wp
    rw [response_row, Data.futureRowSupport, Finset.mul_sum]
    apply Finset.sum_le_sum
    intro t _
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    exact coefficient_bound D _ _ (wp.property t i)
  -- Each row chooses its own independent box corner; the suffix control stays fixed.
  · let w : Block D.q D.p := fun t i =>
      if 0 ≤ row (D.futureNoiseColumn t i) then D.rho else -D.rho
    have hw : ∀ t, D.NoiseOK (w t) := by
      intro t i
      dsimp [w]
      split_ifs <;> constructor <;> linarith [D.rho_pos]
    refine ⟨⟨w, hw⟩, ?_⟩
    rw [response_row, Data.futureRowSupport, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    dsimp [w]
    split_ifs with hb
    · rw [abs_of_nonneg hb, mul_comm]
    · rw [abs_of_neg (lt_of_not_ge hb)]
      ring

 theorem robust_row : RobustRowGoal := by
  intro D row z bound
  obtain ⟨upper, wp, attained⟩ := attained_support D row
  constructor
  · intro h
    have hh := h wp
    rwa [map_add, attained] at hh
  · intro h wp
    rw [map_add]
    have hh := upper wp
    linarith

 theorem exact_tightening : ExactTighteningGoal := by
  intro D a y eta
  constructor
  · intro h xi
    constructor
    · intro i
      constructor
      · apply (robust_row D (-(D.terminalRow i)) (D.aroNominalTerminal a y xi)
          (-D.gmin i)).mp
        intro wp
        have hh := (h xi wp).1 i
        rw [future_expansion] at hh
        change -(D.H (D.aroNominalTerminal a y xi + D.futureNoiseResponse wp) i) ≤ -D.gmin i
        exact neg_le_neg hh.1
      · apply (robust_row D (D.terminalRow i) (D.aroNominalTerminal a y xi)
          (D.gmax i)).mp
        intro wp
        have hh := (h xi wp).1 i
        rw [future_expansion] at hh
        exact hh.2
    · apply (robust_row D D.c (D.aroNominalTerminal a y xi) eta).mp
      intro wp
      have hh := (h xi wp).2
      rwa [future_expansion] at hh
  · intro h xi wp
    obtain ⟨rows, cost⟩ := h xi
    rw [future_expansion]
    constructor
    · intro i
      have hl := (robust_row D (-(D.terminalRow i)) (D.aroNominalTerminal a y xi)
        (-D.gmin i)).mpr (rows i).1 wp
      have hu := (robust_row D (D.terminalRow i) (D.aroNominalTerminal a y xi)
        (D.gmax i)).mpr (rows i).2 wp
      change -(D.H (D.aroNominalTerminal a y xi + D.futureNoiseResponse wp) i) ≤ -D.gmin i at hl
      exact ⟨neg_le_neg_iff.mp hl, hu⟩
    · exact (robust_row D D.c (D.aroNominalTerminal a y xi) eta).mpr cost wp

end BridgeFormalV3.Proofs
