import ControlFixture
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data
-- Positive impossibility check for the same observation under independent futures.
def c6Impossible : ¬ ∃ policy : D.StatePolicy a, FutureDemand policy := by
  rintro ⟨policy,h⟩
  have hplus := (h futurePlus).1 (show futurePlus.val 0 0 = 1 from rfl)
  have hminus := (h futureMinus).2 (show futureMinus.val 0 0 = -1 from rfl)
  have he : a = minus := hplus.symm.trans hminus
  have hc : (1 : ℝ) = -1 := congrArg (fun b : D.ControlBlock D.q => b.val 0 0) he
  norm_num at hc
#print axioms c6Impossible
end
end FinalReviewControls
