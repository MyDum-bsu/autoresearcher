import Controls.Unified.C1
namespace UnifiedControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data

example (wm wp : D.NoiseBlock 1) :
    D.Rows (-2) (D.sourceTrajectory a pi wm wp 2) := c1Source wm wp

def c4Reject : ¬ D.SourceBound a pi (-3) := by
  intro h
  have hc := (h zeroNoise zeroNoise).2
  rw [show D.r + D.q = 2 from rfl, c1Terminal] at hc
  norm_num [D] at hc

example : ¬ D.Rows (-3) (D.sourceTrajectory a pi zeroNoise zeroNoise 2) := by
  intro h
  have hc := h.2
  rw [c1Terminal] at hc
  norm_num [D] at hc

example : ¬ positiveD.SourceBound positiveA positivePi (-2) := by
  intro h
  have hc := (h zeroNoise zeroNoise).2
  norm_num [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step,
    Data.blockAt, Data.sourceSuffix, positiveD, positiveA, positivePi, D, B, E,
    a, zeroNoise, noise] at hc

#print axioms c4Reject
end
end UnifiedControls
