import Controls.Unified.ControlFixture

/-! Fixed C2 control: uses `Set.ext` instead of removed `Set.eq_empty_iff_forall_not_mem`. -/
namespace UnifiedControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data

example : Nonempty (badD.ControlBlock 1) ∧ Nonempty (badD.NoiseBlock 1) :=
  BridgeFormalV2.Proofs.nonempty_blocks badD 1

theorem c2EmptyLevels : badD.sourceLevels = ∅ := by
  apply Set.ext
  intro eta
  constructor
  · intro h
    obtain ⟨a0, policy, hb⟩ := h
    have h5 := ((hb zeroNoise zeroNoise).1 (1 : Fin 2)).1
    norm_num [Data.sourceTrajectory, Data.prefixState, Data.run, Data.step,
      Data.blockAt, badD, D, B, E, zeroNoise, noise] at h5
  · intro h
    exact False.elim h

#print axioms c2EmptyLevels
end
end UnifiedControls
