import BridgeFormalV2.Goals
import Mathlib.Tactic.Abel

namespace BridgeFormalV2.Proofs
noncomputable section
open Data
open scoped BigOperators

 theorem nonempty_blocks : NonemptyBlocksGoal := by
  intro D k
  constructor
  · exact ⟨⟨fun _ => D.umin, fun _ i => ⟨le_rfl, D.control_nonempty i⟩⟩⟩
  · exact ⟨⟨fun _ => 0, fun _ _ => ⟨neg_nonpos.mpr (le_of_lt D.rho_pos),
      le_of_lt D.rho_pos⟩⟩⟩

 theorem run_add (D : Data) (x z : Vec D.n) (u v : ℕ → Vec D.m)
    (w h : ℕ → Vec D.p) (k : ℕ) :
    D.run (x + z) (fun t => u t + v t) (fun t => w t + h t) k =
      D.run x u w k + D.run z v h k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    simp only [Data.run, Data.step, ih, map_add]
    abel

 theorem prefix_split : PrefixSplitGoal := by
  intro D a wm
  simpa only [Data.prefixState, Data.nominal, Data.deviation, add_zero, zero_add]
    using run_add D D.x0 0 (blockAt a.val) (fun _ => 0)
      (fun _ => 0) (blockAt wm.val) D.r

 theorem run_congr (D : Data) (x : Vec D.n) (u v : ℕ → Vec D.m)
    (w h : ℕ → Vec D.p) (k : ℕ)
    (hu : ∀ t < k, u t = v t) (hw : ∀ t < k, w t = h t) :
    D.run x u w k = D.run x v h k := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Data.run, Data.run, ih (fun t ht => hu t (Nat.lt_succ_of_lt ht))
      (fun t ht => hw t (Nat.lt_succ_of_lt ht)), hu k (Nat.lt_succ_self k),
      hw k (Nat.lt_succ_self k)]

 theorem run_formula (D : Data) (x : Vec D.n) (u : ℕ → Vec D.m)
    (w : ℕ → Vec D.p) (k : ℕ) :
    D.run x u w k = (D.A ^ k) x +
      ∑ t : Fin k, (D.A ^ (k - 1 - t.val)) (D.B (u t.val) + D.E (w t.val)) := by
  induction k with
  | zero => simp [Data.run]
  | succ k ih =>
    rw [Data.run, Data.step, ih, map_add, map_sum, Fin.sum_univ_castSucc]
    have terms : ∀ t : Fin k,
        D.A ((D.A ^ (k - 1 - t.val)) (D.B (u t.val) + D.E (w t.val))) =
        (D.A ^ (k + 1 - 1 - (t.castSucc).val))
          (D.B (u (t.castSucc).val) + D.E (w (t.castSucc).val)) := by
      intro t
      have he : k + 1 - 1 - t.val = (k - 1 - t.val) + 1 := by omega
      simp only [Fin.val_castSucc, he, pow_succ', Module.End.mul_apply]
    simp only [terms]
    simp only [Fin.val_last, Nat.add_sub_cancel, Nat.sub_self, pow_zero,
      Module.End.one_apply, pow_succ', Module.End.mul_apply]
    abel

 theorem expansion : ExpansionGoal := by
  intro D k x u w
  rw [run_formula]
  unfold Data.expansion
  congr 1
  apply Finset.sum_congr rfl
  intro t _
  simp [Data.blockAt, t.isLt]

 theorem source_chronology : SourceChronologyGoal := by
  intro D a pi wm wp
  constructor
  · simp [Data.sourceTrajectory, Data.run]
  · intro t ht
    by_cases h : t < D.r
    · have h1 : t + 1 ≤ D.r := h
      simp [Data.sourceTrajectory, Data.chronologicalControl, Data.chronologicalNoise,
        h, h1, Nat.le_of_lt h, Data.run]
    · by_cases he : t = D.r
      · subst t
        simp [Data.sourceTrajectory, Data.chronologicalControl, Data.chronologicalNoise,
          Data.run, Data.prefixState]
      · have hgt : D.r < t := by omega
        have hs : t + 1 - D.r = (t - D.r) + 1 := by omega
        simp [Data.sourceTrajectory, Data.chronologicalControl, Data.chronologicalNoise,
          Nat.not_le.mpr hgt, Nat.not_le.mpr (by omega : D.r < t + 1),
          Nat.not_lt.mpr (Nat.le_of_lt hgt), hs, Data.run]

 theorem suffix_expansion : SuffixExpansionGoal := by
  intro D a pi wm wp
  have h : ¬ D.r + D.q ≤ D.r := by have := D.q_pos; omega
  simp only [Data.sourceTrajectory, ite_eq_right h, Nat.add_sub_cancel_left]
  rw [expansion, prefix_split]

 theorem exogenous_image : ExogenousImageGoal := by
  intro D a
  have h : (fun wm : D.NoiseBlock D.r => D.prefixState a wm - D.nominal a) =
      D.deviation := by
    funext wm
    rw [prefix_split, add_sub_cancel_left]
  rw [h]
  rfl

 theorem observation_fibre : ObservationFibreGoal := by
  intro D a pi w1 w2 h
  apply congrArg pi.rule
  exact Subtype.ext h

end
end BridgeFormalV2.Proofs
