import C6
open FinalReviewControls
#check c6Impossible
example : ∃ policy : D.StatePolicy a, FutureDemand policy := by
  refine ⟨pi, ?_⟩
  intro wp
  constructor
  · intro _; rfl
  · intro _; rfl
