import BridgeFormalV2.Proofs.Policies

/-! Frozen C1-C6 fixture only; no replacement of reviewed definitions. -/
namespace FinalReviewControls
noncomputable section
open BridgeFormalV2 BridgeFormalV2.Data

def B : Vec 1 →ₗ[ℝ] Vec 2 where
  toFun u i := if i = 0 then u 0 else 0
  map_add' u v := by ext i; by_cases h : i = 0 <;> simp [h]
  map_smul' c u := by ext i; by_cases h : i = 0 <;> simp [h]

def E : Vec 2 →ₗ[ℝ] Vec 2 where
  toFun w i := if i = 0 then 0 else w 0 + w 1
  map_add' u v := by ext i; by_cases h : i = 0 <;> simp [h] <;> ring
  map_smul' c u := by ext i; by_cases h : i = 0 <;> simp [h, mul_add]

abbrev D : Data where
  n := 2
  m := 1
  p := 2
  rows := 2
  r := 1
  q := 1
  n_pos := by decide
  m_pos := by decide
  p_pos := by decide
  r_pos := by decide
  q_pos := by decide
  A := LinearMap.id
  B := B
  E := E
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := by intro i; norm_num
  rho := 1
  rho_pos := by norm_num
  H := LinearMap.id
  gmin := fun _ => -4
  gmax := fun _ => 4
  c := -(LinearMap.proj (0 : Fin 2))

abbrev badD : Data := { D with
  gmin := fun i => if i.val = 0 then -4 else 5
  gmax := fun i => if i.val = 0 then 4 else 5 }

abbrev positiveD : Data := { D with c := LinearMap.proj (0 : Fin 2) }

def a : D.ControlBlock D.r := ⟨fun _ _ => 1, by intro t i; constructor <;> norm_num [D]⟩
def minus : D.ControlBlock D.q := ⟨fun _ _ => -1, by intro t i; constructor <;> norm_num [D]⟩
def pi : D.StatePolicy a := ⟨fun _ => a, measurable_const⟩
def y : D.DeviationPolicy := ⟨fun _ => a, measurable_const⟩
def positiveA : positiveD.ControlBlock positiveD.r := a
def positivePi : positiveD.StatePolicy positiveA := ⟨fun _ => a, measurable_const⟩

def noise (x z : ℝ) (hx : -1 ≤ x ∧ x ≤ 1) (hz : -1 ≤ z ∧ z ≤ 1) :
    D.NoiseBlock 1 := ⟨fun _ i => if i = 0 then x else z, by
  intro t i; change -1 ≤ (if i = 0 then x else z) ∧ (if i = 0 then x else z) ≤ 1
  by_cases h : i = 0 <;> simp [h, hx, hz]⟩
def zeroNoise : D.NoiseBlock 1 := noise 0 0 (by norm_num) (by norm_num)
def wPlus : D.NoiseBlock 1 := noise 1 (-1) (by norm_num) (by norm_num)
def wMinus : D.NoiseBlock 1 := noise (-1) 1 (by norm_num) (by norm_num)
def futurePlus : D.NoiseBlock 1 := noise 1 0 (by norm_num) (by norm_num)
def futureMinus : D.NoiseBlock 1 := noise (-1) 0 (by norm_num) (by norm_num)

/-! A forbidden candidate is required to agree with both future demands at one observation. -/
def FutureDemand (policy : D.StatePolicy a) : Prop :=
  ∀ wp : D.NoiseBlock D.q,
    ((wp.val 0) 0 = 1 → D.sourceSuffix a policy zeroNoise = a) ∧
    ((wp.val 0) 0 = -1 → D.sourceSuffix a policy zeroNoise = minus)

end
end FinalReviewControls
