import ControlFixture

namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data

example : Nonempty (badD.ControlBlock 1) ∧ Nonempty (badD.NoiseBlock 1) :=
  BridgeFormalV2.Proofs.nonempty_blocks badD 1

/-- Same unreachable terminal target as C2; use set extensionality directly. -/
example : badD.sourceLevels = ∅ := by
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

end
end FinalReviewControls
