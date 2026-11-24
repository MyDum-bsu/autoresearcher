import Mathlib.Data.ENNReal.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum

/-!
Core elementary lemmas P1-P3 migrated cleanly into `AroProofs.Aroform` (Lean 4 v4.35.0-rc2)
with minimal targeted Mathlib imports (zero `import Mathlib` bloat).
-/

namespace AroProofs.Aroform

theorem toy_z_nonneg (β Y : ℚ) : 0 ≤ max (β - Y) 0 :=
  le_max_right _ _

theorem toy_z_zero_of_le (β Y : ℚ) (h : β ≤ Y) : max (β - Y) 0 = 0 :=
  max_eq_right (by linarith)

theorem toy_z_sub_of_gt (β Y : ℚ) (h : Y < β) : max (β - Y) 0 = β - Y :=
  max_eq_left (by linarith)

/-- Information monotonicity: enlarging the feasible policy set cannot increase the infimum. -/
theorem info_value_monotone {S T : Set ENNReal} (hST : S ⊆ T) : sInf T ≤ sInf S :=
  le_sInf fun _ hx => sInf_le (hST hx)

/-- Coordinate rotation identity: |a| + |b| = max(|a + b|, |a - b|). -/
theorem l1_eq_max_sum_diff (a b : ℚ) :
    |a| + |b| = max |a + b| |a - b| := by
  simp only [abs_eq_max_neg, max_def]
  repeat' split
  all_goals linarith

/-- Convexity along [0, 1]: chord of pointwise optima dominates affine demand. -/
theorem chord_dominates (a b ζ : ℚ) (h0 : 0 ≤ ζ) (h1 : ζ ≤ 1) :
    max ((1 - ζ) * a + ζ * b) 0 ≤ (1 - ζ) * max a 0 + ζ * max b 0 := by
  have hz0 : 0 ≤ 1 - ζ := by linarith
  have h2 : 0 ≤ (1 - ζ) * max a 0 + ζ * max b 0 :=
    add_nonneg (mul_nonneg hz0 (le_max_right a 0)) (mul_nonneg h0 (le_max_right b 0))
  have h1a : (1 - ζ) * a ≤ (1 - ζ) * max a 0 :=
    mul_le_mul_of_nonneg_left (le_max_left a 0) hz0
  have h1b : ζ * b ≤ ζ * max b 0 := mul_le_mul_of_nonneg_left (le_max_left b 0) h0
  refine max_le ?_ h2
  linarith

theorem chord_cost_bound (A B ζ : ℚ) (h0 : 0 ≤ ζ) (h1 : ζ ≤ 1) :
    (1 - ζ) * A + ζ * B ≤ max A B := by
  rcases le_or_gt A B with h | h
  · have hle : (1 - ζ) * A ≤ (1 - ζ) * B := mul_le_mul_of_nonneg_left h (by linarith)
    linarith [le_max_right A B]
  · have hle : ζ * B ≤ ζ * A := mul_le_mul_of_nonneg_left (le_of_lt h) h0
    linarith [le_max_left A B]

theorem one_d_policy_lower (a b Y0 Y1 : ℚ)
    (h0 : max a 0 ≤ Y0) (h1 : max b 0 ≤ Y0 + Y1) :
    max (max a 0) (max b 0) ≤ max Y0 (Y0 + Y1) := by
  have hM : 0 ≤ max Y0 (Y0 + Y1) :=
    le_trans (le_trans (le_max_right a 0) h0) (le_max_left _ _)
  exact max_le
    (max_le (le_trans (le_trans (le_max_left a 0) h0) (le_max_left _ _)) hM)
    (le_trans h1 (le_max_right _ _))

/-- 1D ADR exactness theorem (P3): affine chord rule achieves exact adaptive optimum. -/
theorem one_d_exactness (a b : ℚ) :
    (∃ Y0 Y1 : ℚ, ∀ ζ : ℚ, 0 ≤ ζ → ζ ≤ 1 →
        max ((1 - ζ) * a + ζ * b) 0 ≤ Y0 + Y1 * ζ
        ∧ 0 ≤ Y0 + Y1 * ζ
        ∧ Y0 + Y1 * ζ ≤ max (max a 0) (max b 0))
    ∧ ∀ Y0 Y1 : ℚ, (∀ ζ : ℚ, 0 ≤ ζ → ζ ≤ 1 →
        max ((1 - ζ) * a + ζ * b) 0 ≤ Y0 + Y1 * ζ
        ∧ 0 ≤ Y0 + Y1 * ζ) →
      max (max a 0) (max b 0) ≤ max Y0 (Y0 + Y1) := by
  constructor
  · refine ⟨max a 0, max b 0 - max a 0, ?_⟩
    intro ζ h0 h1
    have hrw : max a 0 + (max b 0 - max a 0) * ζ
        = (1 - ζ) * max a 0 + ζ * max b 0 := by ring
    have hcd := chord_dominates a b ζ h0 h1
    have hcb := chord_cost_bound (max a 0) (max b 0) ζ h0 h1
    have hz0 : 0 ≤ 1 - ζ := by linarith
    have hnn : 0 ≤ (1 - ζ) * max a 0 + ζ * max b 0 :=
      add_nonneg (mul_nonneg hz0 (le_max_right a 0)) (mul_nonneg h0 (le_max_right b 0))
    constructor
    · rw [hrw]; exact hcd
    · rw [hrw]; exact ⟨hnn, hcb⟩
  · intro Y0 Y1 hf
    have e0 := hf 0 (by norm_num) (by norm_num)
    have e1 := hf 1 (by norm_num) (by norm_num)
    exact one_d_policy_lower a b Y0 Y1 (by simpa using e0.1) (by simpa using e1.1)

def V_scalar (d0 e1 e2 T : ℚ) : ℚ := |d0| + |e1 + e2| * T

def V_diff (d0 e1 e2 T : ℚ) : ℚ := |d0| + |e1 - e2| * T

theorem V_diff_aligned (d0 e1 e2 T : ℚ) (h : e1 = e2) :
    V_diff d0 e1 e2 T = |d0| := by
  subst h; simp [V_diff]

theorem V_diff_opposite (d0 e1 e2 T : ℚ) (h : e2 = -e1) :
    V_diff d0 e1 e2 T = |d0| + 2 * |e1| * T := by
  subst h
  simp only [V_diff, sub_neg_eq_add]
  have h2 : e1 + e1 = 2 * e1 := by ring
  rw [h2, abs_mul]
  have h2n : |(2 : ℚ)| = 2 := by norm_num
  rw [h2n]

theorem l2a_diff_two_path (d0 v T : ℚ) (hT : 0 ≤ T) :
    max |d0 + v * T| |d0 - v * T| = |d0| + |v| * T := by
  have h1 := l1_eq_max_sum_diff d0 (v * T)
  have h2 : |v| * T = |v * T| := by rw [abs_mul, abs_of_nonneg hT]
  rw [h2]
  exact h1.symm

theorem l2a_sum_two_path (a e T : ℚ) (hT : 0 ≤ T) :
    max |a + 2 * e * T| |a - 2 * e * T| = |a| + 2 * |e| * T := by
  have h2 : |2 * e * T| = 2 * |e| * T := by
    rw [abs_mul, abs_mul, abs_of_nonneg hT]
    norm_num
  rw [← h2]
  exact (l1_eq_max_sum_diff a (2 * e * T)).symm

end AroProofs.Aroform
