import BridgeFormalV2.Model

/-! Unproved target propositions. These definitions are not theorem evidence. -/
namespace BridgeFormalV2
noncomputable section
open Data

/-- F1: the formula must follow from the actual chronological recurrence. -/
def ExpansionGoal : Prop :=
  ∀ D : Data, ∀ k : ℕ, ∀ x : Vec D.n,
    ∀ u : Block k D.m, ∀ w : Block k D.p,
      D.run x (blockAt u) (blockAt w) k = D.expansion k x u w

def PrefixSplitGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ wm : D.NoiseBlock D.r,
    D.prefixState a wm = D.nominal a + D.deviation wm

def SourceChronologyGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ pi : D.StatePolicy a,
    ∀ wm : D.NoiseBlock D.r, ∀ wp : D.NoiseBlock D.q,
      D.sourceTrajectory a pi wm wp 0 = D.x0 ∧
      ∀ t < D.r + D.q,
        D.sourceTrajectory a pi wm wp (t + 1) =
          D.step (D.sourceTrajectory a pi wm wp t)
            (D.chronologicalControl a (D.sourceSuffix a pi wm) t)
            (D.chronologicalNoise wm wp t)

def SuffixExpansionGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ pi : D.StatePolicy a,
    ∀ wm : D.NoiseBlock D.r, ∀ wp : D.NoiseBlock D.q,
      D.sourceTrajectory a pi wm wp (D.r + D.q) =
        D.expansion D.q (D.nominal a + D.deviation wm)
          (D.sourceSuffix a pi wm).val wp.val

/-- The reachable deviation image, not merely its notation, is independent of a. -/
def ExogenousImageGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r,
    Set.range (fun wm : D.NoiseBlock D.r => D.prefixState a wm - D.nominal a) = D.Z

def NonemptyBlocksGoal : Prop :=
  ∀ D : Data, ∀ k : ℕ, Nonempty (D.ControlBlock k) ∧ Nonempty (D.NoiseBlock k)

def Preserves (D : Data) (a : D.ControlBlock D.r)
    (pi : D.StatePolicy a) (y : D.DeviationPolicy) : Prop :=
  D.Related a pi y ∧
  (∀ wm : D.NoiseBlock D.r, D.sourceSuffix a pi wm = D.aroSuffix y wm) ∧
  (∀ wm : D.NoiseBlock D.r, ∀ wp : D.NoiseBlock D.q, ∀ t ≤ D.r + D.q,
    D.sourceTrajectory a pi wm wp t = D.aroTrajectory a y wm wp t) ∧
  (∀ eta : ℝ, D.SourceBound a pi eta ↔ D.AROBound a y eta)

def ForwardPolicyGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ pi : D.StatePolicy a,
    ∃ y : D.DeviationPolicy, Preserves D a pi y

def ReversePolicyGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ y : D.DeviationPolicy,
    ∃ pi : D.StatePolicy a, Preserves D a pi y

def EpigraphEqualityGoal : Prop :=
  ∀ D : Data, D.sourceLevels = D.aroLevels

/-- Identical observed states cannot reveal prefix history or future noise. -/
def ObservationFibreGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ pi : D.StatePolicy a,
    ∀ w1 w2 : D.NoiseBlock D.r, D.prefixState a w1 = D.prefixState a w2 →
      D.sourceSuffix a pi w1 = D.sourceSuffix a pi w2

end
end BridgeFormalV2
