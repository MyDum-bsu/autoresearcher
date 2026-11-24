import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
example : Nonempty (badD.ControlBlock 1) ∧ Nonempty (badD.NoiseBlock 1) :=
  BridgeFormalV2.Proofs.nonempty_blocks badD 1
example : badD.sourceLevels = ∅ := by
  apply Set.eq_empty_iff_forall_not_mem.mpr
  intro eta h
  obtain ⟨a0, policy, hb⟩ := h
  have h5 := ((hb zeroNoise zeroNoise).1 (1 : Fin 2)).1
  norm_num [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step,
    Data.blockAt, badD, D, B, E, zeroNoise, noise] at h5
end
end FinalReviewControls
