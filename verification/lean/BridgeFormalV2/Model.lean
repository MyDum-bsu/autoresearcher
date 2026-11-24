import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.LinearAlgebra.Matrix.ToLin

/-!
Candidate trusted definitions for S1. No general theorem is proved here.
Source: corpus/our_papers/A4_Дмитрук_2022.pdf, physical pp2-6.
Borel regularity on reachable subtypes is an explicit implementation convention.
-/
namespace BridgeFormalV2

noncomputable section
open scoped BigOperators
open MeasureTheory

abbrev Vec (n : ℕ) := Fin n → ℝ
abbrev Block (k n : ℕ) := Fin k → Vec n

structure Data where
  n : ℕ
  m : ℕ
  p : ℕ
  rows : ℕ
  r : ℕ
  q : ℕ
  n_pos : 0 < n
  m_pos : 0 < m
  p_pos : 0 < p
  r_pos : 0 < r
  q_pos : 0 < q
  A : Vec n →ₗ[ℝ] Vec n
  B : Vec m →ₗ[ℝ] Vec n
  E : Vec p →ₗ[ℝ] Vec n
  x0 : Vec n
  umin : Vec m
  umax : Vec m
  control_nonempty : ∀ i, umin i ≤ umax i
  rho : ℝ
  rho_pos : 0 < rho
  H : Vec n →ₗ[ℝ] Vec rows
  gmin : Vec rows
  gmax : Vec rows
  c : Vec n →ₗ[ℝ] ℝ

namespace Data
variable (D : Data)

def ControlOK (u : Vec D.m) : Prop := ∀ i, D.umin i ≤ u i ∧ u i ≤ D.umax i
def NoiseOK (w : Vec D.p) : Prop := ∀ i, -D.rho ≤ w i ∧ w i ≤ D.rho
abbrev ControlBlock (k : ℕ) := {u : Block k D.m // ∀ t, D.ControlOK (u t)}
abbrev NoiseBlock (k : ℕ) := {w : Block k D.p // ∀ t, D.NoiseOK (w t)}

/-- Zero extension is used only outside the executed finite block. -/
def blockAt {k n : ℕ} (v : Block k n) (t : ℕ) : Vec n :=
  if h : t < k then v ⟨t, h⟩ else 0

def step (x : Vec D.n) (u : Vec D.m) (w : Vec D.p) : Vec D.n :=
  D.A x + D.B u + D.E w

/-- Actual chronological recurrence, not an assumed terminal formula. -/
def run (D : Data) (x : Vec D.n) (u : ℕ → Vec D.m) (w : ℕ → Vec D.p) : ℕ → Vec D.n
  | 0 => x
  | t + 1 => D.step (D.run x u w t) (u t) (w t)

def prefixState (a : D.ControlBlock D.r) (w : D.NoiseBlock D.r) : Vec D.n :=
  D.run D.x0 (blockAt a.val) (blockAt w.val) D.r

def nominal (a : D.ControlBlock D.r) : Vec D.n :=
  D.run D.x0 (blockAt a.val) (fun _ => 0) D.r

/-- Exogenous prefix response; no first-stage control argument occurs. -/
def deviation (w : D.NoiseBlock D.r) : Vec D.n :=
  D.run 0 (fun _ => 0) (blockAt w.val) D.r

def Z : Set (Vec D.n) := Set.range D.deviation
def S (a : D.ControlBlock D.r) : Set (Vec D.n) := Set.range (D.prefixState a)

structure StatePolicy (a : D.ControlBlock D.r) where
  rule : D.S a → D.ControlBlock D.q
  borel : Measurable rule

structure DeviationPolicy where
  rule : D.Z → D.ControlBlock D.q
  borel : Measurable rule

def observed (a : D.ControlBlock D.r) (w : D.NoiseBlock D.r) : D.S a :=
  ⟨D.prefixState a w, ⟨w, rfl⟩⟩
def observedDeviation (w : D.NoiseBlock D.r) : D.Z :=
  ⟨D.deviation w, ⟨w, rfl⟩⟩

def sourceSuffix (a : D.ControlBlock D.r) (pi : D.StatePolicy a)
    (w : D.NoiseBlock D.r) : D.ControlBlock D.q := pi.rule (D.observed a w)
def aroSuffix (y : D.DeviationPolicy) (w : D.NoiseBlock D.r) : D.ControlBlock D.q :=
  y.rule (D.observedDeviation w)

/-- Selected once at the measurement; neither suffix rule takes a future argument. -/
def sourceTrajectory (a : D.ControlBlock D.r) (pi : D.StatePolicy a)
    (wm : D.NoiseBlock D.r) (wp : D.NoiseBlock D.q) (t : ℕ) : Vec D.n :=
  if t ≤ D.r then D.run D.x0 (blockAt a.val) (blockAt wm.val) t
  else D.run (D.prefixState a wm) (blockAt (D.sourceSuffix a pi wm).val) (blockAt wp.val) (t - D.r)

def aroTrajectory (a : D.ControlBlock D.r) (y : D.DeviationPolicy)
    (wm : D.NoiseBlock D.r) (wp : D.NoiseBlock D.q) (t : ℕ) : Vec D.n :=
  if t ≤ D.r then D.run D.x0 (blockAt a.val) (blockAt wm.val) t
  else D.run (D.prefixState a wm) (blockAt (D.aroSuffix y wm).val) (blockAt wp.val) (t - D.r)

def chronologicalControl (a : D.ControlBlock D.r) (b : D.ControlBlock D.q)
    (t : ℕ) : Vec D.m := if t < D.r then blockAt a.val t else blockAt b.val (t - D.r)
def chronologicalNoise (wm : D.NoiseBlock D.r) (wp : D.NoiseBlock D.q)
    (t : ℕ) : Vec D.p := if t < D.r then blockAt wm.val t else blockAt wp.val (t - D.r)

/-- Independently defined finite linear expansion: F1 must connect it to run. -/
def expansion (k : ℕ) (x : Vec D.n) (u : Block k D.m) (w : Block k D.p) : Vec D.n :=
  (D.A ^ k) x + ∑ t : Fin k, (D.A ^ (k - 1 - t.val)) (D.B (u t) + D.E (w t))

def aroTerminal (a : D.ControlBlock D.r) (y : D.DeviationPolicy)
    (xi : D.Z) (wp : D.NoiseBlock D.q) : Vec D.n :=
  D.expansion D.q (D.nominal a + xi.val) (y.rule xi).val wp.val

/-- Every upper and lower terminal row, followed by the signed cost row. -/
def Rows (eta : ℝ) (x : Vec D.n) : Prop :=
  (∀ i, D.gmin i ≤ D.H x i ∧ D.H x i ≤ D.gmax i) ∧ D.c x ≤ eta

def SourceBound (a : D.ControlBlock D.r) (pi : D.StatePolicy a) (eta : ℝ) : Prop :=
  ∀ wm : D.NoiseBlock D.r, ∀ wp : D.NoiseBlock D.q,
    D.Rows eta (D.sourceTrajectory a pi wm wp (D.r + D.q))

def AROBound (a : D.ControlBlock D.r) (y : D.DeviationPolicy) (eta : ℝ) : Prop :=
  ∀ xi : D.Z, ∀ wp : D.NoiseBlock D.q, D.Rows eta (D.aroTerminal a y xi wp)

def sourceLevels : Set ℝ := {eta | ∃ a : D.ControlBlock D.r, ∃ pi : D.StatePolicy a,
  D.SourceBound a pi eta}
def aroLevels : Set ℝ := {eta | ∃ a : D.ControlBlock D.r, ∃ y : D.DeviationPolicy,
  D.AROBound a y eta}

/-- Translation equations are conclusions in F2, never model assumptions. -/
def Related (a : D.ControlBlock D.r) (pi : D.StatePolicy a) (y : D.DeviationPolicy) : Prop :=
  (∀ xi : D.Z, ∀ s : D.S a, s.val = D.nominal a + xi.val → pi.rule s = y.rule xi) ∧
  (∀ s : D.S a, ∀ xi : D.Z, xi.val = s.val - D.nominal a → y.rule xi = pi.rule s)

end Data
end
end BridgeFormalV2
