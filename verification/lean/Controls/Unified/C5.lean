import Controls.Unified.C4
open UnifiedControls
#check c4Reject
-- Negative control: deliberately false signed-bound target (MUST be rejected by Lean kernel).
example : D.SourceBound a pi (-3) := by
  exact c1Source
