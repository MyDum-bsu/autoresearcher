import Controls.Unified.C6
open UnifiedControls
#check c6Impossible
-- Negative control: forbidden future-dependent suffix demand (MUST be rejected by Lean kernel).
example : ∃ policy : D.StatePolicy a, FutureDemand policy := by
  refine ⟨pi, ?_⟩
  intro wp
  constructor
  · intro _; rfl
  · intro _; rfl
