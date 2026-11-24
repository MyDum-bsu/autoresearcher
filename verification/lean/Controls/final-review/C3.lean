import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
example (policy : D.StatePolicy a) :
    D.sourceSuffix a policy wPlus = D.sourceSuffix a policy wMinus ∧
    (fun (_ : D.NoiseBlock D.q) => D.sourceSuffix a policy wPlus) futurePlus =
      (fun (_ : D.NoiseBlock D.q) => D.sourceSuffix a policy wMinus) futureMinus := by
  have hs : D.prefixState a wPlus = D.prefixState a wMinus := by
    ext i
    fin_cases i <;> norm_num [Data.prefixState, Data.run, Data.step,
      Data.blockAt, D, B, E, a, wPlus, wMinus, noise]
  have he := BridgeFormalV2.Proofs.observation_fibre D a policy wPlus wMinus hs
  exact ⟨he,he⟩
example : futurePlus.val 0 0 = 1 ∧ futureMinus.val 0 0 = -1 := ⟨rfl,rfl⟩
end
end FinalReviewControls
