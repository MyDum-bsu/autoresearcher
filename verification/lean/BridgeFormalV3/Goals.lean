import BridgeFormalV2.Proofs.Policies

/-! F3 candidate definitions and propositions; this file supplies no target proof. -/
noncomputable section
open scoped BigOperators
open BridgeFormalV2

namespace BridgeFormalV3

def basisVector {p : ℕ} (i : Fin p) : Vec p :=
  fun j => if j = i then 1 else 0

end BridgeFormalV3

namespace BridgeFormalV2.Data

/-- Actual suffix response, defined by the chronological recurrence. -/
def futureNoiseResponse (D : Data) (wp : D.NoiseBlock D.q) : Vec D.n :=
  D.run 0 (fun _ => 0) (blockAt wp.val) D.q

/-- No future disturbance enters this nominal terminal state. -/
def aroNominalTerminal (D : Data) (a : D.ControlBlock D.r)
    (y : D.DeviationPolicy) (xi : D.Z) : Vec D.n :=
  D.expansion D.q (D.nominal a + xi.val) (y.rule xi).val 0

def futureNoiseColumn (D : Data) (t : Fin D.q) (i : Fin D.p) : Vec D.n :=
  (D.A ^ (D.q - 1 - t.val)) (D.E (BridgeFormalV3.basisVector i))

/-- Proposed exact directional support, not an assumed support axiom. -/
def futureRowSupport (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ) : ℝ :=
  D.rho * ∑ t : Fin D.q, ∑ i : Fin D.p, |row (D.futureNoiseColumn t i)|

def terminalRow (D : Data) (i : Fin D.rows) : Vec D.n →ₗ[ℝ] ℝ :=
  (LinearMap.proj i).comp D.H

def TightenedAROBound (D : Data) (a : D.ControlBlock D.r)
    (y : D.DeviationPolicy) (eta : ℝ) : Prop :=
  ∀ xi : D.Z,
    let z := D.aroNominalTerminal a y xi
    (∀ i : Fin D.rows,
      (-(D.terminalRow i)) z + D.futureRowSupport (-(D.terminalRow i)) ≤ -D.gmin i ∧
      (D.terminalRow i) z + D.futureRowSupport (D.terminalRow i) ≤ D.gmax i) ∧
    D.c z + D.futureRowSupport D.c ≤ eta

end BridgeFormalV2.Data

namespace BridgeFormalV3

/-- F3.1: connect the new row formulation to the actual sealed ARO terminal. -/
def FutureExpansionGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ y : D.DeviationPolicy,
    ∀ xi : D.Z, ∀ wp : D.NoiseBlock D.q,
      D.aroTerminal a y xi wp = D.aroNominalTerminal a y xi + D.futureNoiseResponse wp

/-- F3.2: a general support bound and a witness attaining it on the real box. -/
def AttainedSupportGoal : Prop :=
  ∀ D : Data, ∀ row : Vec D.n →ₗ[ℝ] ℝ,
    (∀ wp : D.NoiseBlock D.q, row (D.futureNoiseResponse wp) ≤ D.futureRowSupport row) ∧
    (∃ wp : D.NoiseBlock D.q, row (D.futureNoiseResponse wp) = D.futureRowSupport row)

/-- F3.3: the future disturbance remains universal after the action is fixed. -/
def RobustRowGoal : Prop :=
  ∀ D : Data, ∀ row : Vec D.n →ₗ[ℝ] ℝ, ∀ z : Vec D.n, ∀ bound : ℝ,
    (∀ wp : D.NoiseBlock D.q, row (z + D.futureNoiseResponse wp) ≤ bound) ↔
      row z + D.futureRowSupport row ≤ bound

/-- F3.4: retain both terminal sides and the signed cost row of the sealed model. -/
def ExactTighteningGoal : Prop :=
  ∀ D : Data, ∀ a : D.ControlBlock D.r, ∀ y : D.DeviationPolicy, ∀ eta : ℝ,
    D.AROBound a y eta ↔ D.TightenedAROBound a y eta

end BridgeFormalV3
