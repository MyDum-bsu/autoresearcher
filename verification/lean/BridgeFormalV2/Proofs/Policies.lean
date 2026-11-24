import BridgeFormalV2.Proofs.Dynamics

namespace BridgeFormalV2.Proofs
noncomputable section
open Data MeasureTheory

/-- Translation is defined on the actual reachable images using recurrence superposition. -/
def toState (D : Data) (a : D.ControlBlock D.r) (xi : D.Z) : D.S a :=
  ⟨D.nominal a + xi.val, by
    rcases xi.property with ⟨w, hw⟩
    exact ⟨w, by rw [prefix_split, hw]⟩⟩

def toDeviation (D : Data) (a : D.ControlBlock D.r) (s : D.S a) : D.Z :=
  ⟨s.val - D.nominal a, by
    rcases s.property with ⟨w, hw⟩
    exact ⟨w, by rw [← hw, prefix_split, add_sub_cancel_left]⟩⟩

 theorem toState_measurable (D : Data) (a : D.ControlBlock D.r) :
    Measurable (toState D a) := by
  exact (continuous_const.add continuous_subtype_val).measurable.subtype_mk

 theorem toDeviation_measurable (D : Data) (a : D.ControlBlock D.r) :
    Measurable (toDeviation D a) := by
  exact (continuous_subtype_val.sub continuous_const).measurable.subtype_mk

 theorem preserves_of_related (D : Data) (a : D.ControlBlock D.r)
    (pi : D.StatePolicy a) (y : D.DeviationPolicy) (hr : D.Related a pi y) :
    Preserves D a pi y := by
  have hc : ∀ wm : D.NoiseBlock D.r, D.sourceSuffix a pi wm = D.aroSuffix y wm := by
    intro wm
    exact hr.1 (D.observedDeviation wm) (D.observed a wm) (prefix_split D a wm)
  have ht : ∀ wm : D.NoiseBlock D.r, ∀ wp : D.NoiseBlock D.q,
      D.sourceTrajectory a pi wm wp (D.r + D.q) =
        D.aroTerminal a y (D.observedDeviation wm) wp := by
    intro wm wp
    rw [suffix_expansion]
    unfold Data.aroTerminal
    rw [hc wm]
    rfl
  refine ⟨hr, hc, ?_, ?_⟩
  · intro wm wp t _
    simp only [Data.sourceTrajectory, Data.aroTrajectory, hc wm]
  · intro eta
    constructor
    · intro hb xi wp
      rcases xi.property with ⟨wm, hwm⟩
      have he : D.observedDeviation wm = xi := Subtype.ext hwm
      rw [← he, ← ht wm wp]
      exact hb wm wp
    · intro hb wm wp
      rw [ht wm wp]
      exact hb (D.observedDeviation wm) wp

 theorem forward_policy : ForwardPolicyGoal := by
  intro D a pi
  let y : D.DeviationPolicy :=
    ⟨fun xi => pi.rule (toState D a xi), pi.borel.comp (toState_measurable D a)⟩
  refine ⟨y, preserves_of_related D a pi y ?_⟩
  constructor
  · intro xi s hs
    change pi.rule s = pi.rule (toState D a xi)
    apply congrArg pi.rule
    exact Subtype.ext hs
  · intro s xi hxi
    change pi.rule (toState D a xi) = pi.rule s
    apply congrArg pi.rule
    apply Subtype.ext
    change D.nominal a + xi.val = s.val
    rw [hxi]
    abel

 theorem reverse_policy : ReversePolicyGoal := by
  intro D a y
  let pi : D.StatePolicy a :=
    ⟨fun s => y.rule (toDeviation D a s), y.borel.comp (toDeviation_measurable D a)⟩
  refine ⟨pi, preserves_of_related D a pi y ?_⟩
  constructor
  · intro xi s hs
    change y.rule (toDeviation D a s) = y.rule xi
    apply congrArg y.rule
    apply Subtype.ext
    change s.val - D.nominal a = xi.val
    rw [hs, add_sub_cancel_left]
  · intro s xi hxi
    change y.rule xi = y.rule (toDeviation D a s)
    apply congrArg y.rule
    exact Subtype.ext hxi

 theorem epigraph_equality : EpigraphEqualityGoal := by
  intro D
  apply Set.ext
  intro eta
  constructor
  · rintro ⟨a, pi, hb⟩
    obtain ⟨y, hp⟩ := forward_policy D a pi
    exact ⟨a, y, (hp.2.2.2 eta).mp hb⟩
  · rintro ⟨a, y, hb⟩
    obtain ⟨pi, hp⟩ := reverse_policy D a y
    exact ⟨a, pi, (hp.2.2.2 eta).mpr hb⟩

end
end BridgeFormalV2.Proofs
