import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV2.Proofs

def c1Terminal (wm wp : D.NoiseBlock 1) :
    D.sourceTrajectory a pi wm wp 2 =
      fun i => if i = 0 then 2 else wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 := by
  ext i
  fin_cases i <;> simp [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step, Data.blockAt, Data.sourceSuffix, D, B, E, a, pi] <;> ring

def c1Source : D.SourceBound a pi (-2) := by
  intro wm wp
  rw [show D.r + D.q = 2 from rfl, c1Terminal]
  constructor
  · intro i
    fin_cases i
    · norm_num [D]
    · have h00 := wm.property 0 0
      have h01 := wm.property 0 1
      have h10 := wp.property 0 0
      have h11 := wp.property 0 1
      change (-1 ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1) at h00
      change (-1 ≤ wm.val 0 1 ∧ wm.val 0 1 ≤ 1) at h01
      change (-1 ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1) at h10
      change (-1 ≤ wp.val 0 1 ∧ wp.val 0 1 ≤ 1) at h11
      change -4 ≤ wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 ∧
        wm.val 0 0 + wm.val 0 1 + wp.val 0 0 + wp.val 0 1 ≤ 4
      constructor <;> linarith [h00.1,h00.2,h01.1,h01.2,h10.1,h10.2,h11.1,h11.2]
  · norm_num [D]

example : D.AROBound a y (-2) := by
  have hr : D.Related a pi y := ⟨by intros; rfl, by intros; rfl⟩
  exact ((preserves_of_related D a pi y hr).2.2.2 (-2)).mp c1Source

#print axioms c1Terminal
#print axioms c1Source
end
end FinalReviewControls
