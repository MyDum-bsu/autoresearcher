import BridgeFormalV3.Proofs.Support

/-!
# G2: General Compact Convex / Conic Uncertainty Support Tightening (Beyond Box `W`)

Live Scientific Discovery Run-01 (`gen-nonbox-conic-uncertainty`) built strictly over the frozen
core `BridgeFormalV2.Model` / `BridgeFormalV2.Goals` and F3 `BridgeFormalV3.Proofs.Support`.

Main theorems (zero `sorry`, zero custom axioms):
  1. `general_attained_support`: Exact stage-wise Minkowski support attainment over ANY family
     of nonempty compact disturbance sets `W : Fin D.q → Set (Vec D.p)`.
  2. `general_robust_row`: Exact row-wise elimination of future disturbances `wp ∈ StageNoiseBlock D W`.
  3. `general_exact_tightening`: `GeneralAROBound D W a y eta ↔ GeneralTightenedAROBound D W a y eta`.
  4. `box_support_eq_f3`: Specializing `W t = [-rho, rho]^p` recovers F3 `D.futureRowSupport` exactly.
  5. `l1_cross_polytope_support`: Non-box polyhedral `l1` cross-polytope closed form `r * ‖v‖_∞`.
  6. `l2_soc_ball_support`: Non-polyhedral Euclidean/SOC `l2` ball closed form `r * ‖v‖_2`.
  7. `l2_ball_not_finset_conv_2d`: Non-polyhedrality of the 2D `l2` ball (infinitely many extreme
     points via stereographic rational circle points, so finite vertex-LP reduction cannot apply).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 Set

namespace AroProofs.BridgeG2ConicSupport

/-! ## Section 1: Stage-wise general compact future disturbance sets and Minkowski support -/

/-- General future noise block constrained stage-wise by `wp t ∈ W t`. -/
abbrev StageNoiseBlock (D : Data) (W : Fin D.q → Set (Vec D.p)) :=
  {wp : Block D.q D.p // ∀ t : Fin D.q, wp t ∈ W t}

/-- Chronological future noise response for an arbitrary future block `wp : Block D.q D.p`. -/
def generalFutureNoiseResponse (D : Data) (wp : Block D.q D.p) : Vec D.n :=
  D.run 0 (fun _ => 0) (blockAt wp) D.q

/-- Minkowski support function `h_{Wt}(v) = sup_{w ∈ Wt} ∑ i, v i * w i`. -/
def minkowskiSupport {p : ℕ} (Wt : Set (Vec p)) (v : Vec p) : ℝ :=
  sSup ((fun w : Vec p => ∑ i : Fin p, v i * w i) '' Wt)

/-- Stage-wise Minkowski future row support `∑_t h_{W_t}(row ∘ A^{q-1-t} E)`. -/
def stageFutureRowSupport (D : Data) (W : Fin D.q → Set (Vec D.p))
    (row : Vec D.n →ₗ[ℝ] ℝ) : ℝ :=
  ∑ t : Fin D.q, minkowskiSupport (W t) (fun i => row (D.futureNoiseColumn t i))

/-- General ARO terminal state over arbitrary stage-wise future noise `wp : StageNoiseBlock D W`. -/
def generalAroTerminal (D : Data) (W : Fin D.q → Set (Vec D.p))
    (a : D.ControlBlock D.r) (y : D.DeviationPolicy)
    (xi : D.Z) (wp : StageNoiseBlock D W) : Vec D.n :=
  D.expansion D.q (D.nominal a + xi.val) (y.rule xi).val wp.val

/-- Universal future-noise ARO feasibility over general stage-wise sets `W`. -/
def GeneralAROBound (D : Data) (W : Fin D.q → Set (Vec D.p))
    (a : D.ControlBlock D.r) (y : D.DeviationPolicy) (eta : ℝ) : Prop :=
  ∀ xi : D.Z, ∀ wp : StageNoiseBlock D W,
    D.Rows eta (generalAroTerminal D W a y xi wp)

/-- Tightened ARO bound using the stage-wise Minkowski support function `stageFutureRowSupport`. -/
def GeneralTightenedAROBound (D : Data) (W : Fin D.q → Set (Vec D.p))
    (a : D.ControlBlock D.r) (y : D.DeviationPolicy) (eta : ℝ) : Prop :=
  ∀ xi : D.Z,
    let z := D.aroNominalTerminal a y xi
    (∀ i : Fin D.rows,
      (-(D.terminalRow i)) z + stageFutureRowSupport D W (-(D.terminalRow i)) ≤ -D.gmin i ∧
      (D.terminalRow i) z + stageFutureRowSupport D W (D.terminalRow i) ≤ D.gmax i) ∧
    D.c z + stageFutureRowSupport D W D.c ≤ eta

private theorem general_response_expansion (D : Data) (wp : Block D.q D.p) :
    generalFutureNoiseResponse D wp = D.expansion D.q 0 (fun _ => 0) wp := by
  have hz : blockAt (fun _ : Fin D.q => (0 : Vec D.m)) = (fun _ => 0) := by
    funext t; simp [blockAt]
  simpa only [hz, generalFutureNoiseResponse] using
    BridgeFormalV2.Proofs.expansion D D.q (0 : Vec D.n) (fun _ => (0 : Vec D.m)) wp

private theorem general_future_expansion (D : Data) (W : Fin D.q → Set (Vec D.p))
    (a : D.ControlBlock D.r) (y : D.DeviationPolicy)
    (xi : D.Z) (wp : StageNoiseBlock D W) :
    generalAroTerminal D W a y xi wp =
      D.aroNominalTerminal a y xi + generalFutureNoiseResponse D wp.val := by
  rw [generalAroTerminal, Data.aroNominalTerminal, general_response_expansion]
  simp only [Data.expansion, Pi.zero_apply, map_zero, zero_add, add_zero,
    map_add, Finset.sum_add_distrib]
  abel

private theorem general_response_row (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ)
    (wp : Block D.q D.p) :
    row (generalFutureNoiseResponse D wp) =
      ∑ t : Fin D.q, ∑ i : Fin D.p, row (D.futureNoiseColumn t i) * wp t i := by
  rw [general_response_expansion]
  simp only [Data.expansion, map_zero, zero_add, map_sum]
  apply Finset.sum_congr rfl
  intro t _
  conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition (wp t)]
  simp only [map_sum, map_smul, Data.futureNoiseColumn, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro i _
  exact mul_comm _ _

private theorem dot_continuous {p : ℕ} (v : Vec p) :
    Continuous (fun w : Vec p => ∑ i : Fin p, v i * w i) := by
  refine continuous_finsetSum _ (fun i _ => ?_)
  exact continuous_const.mul (continuous_apply i)

theorem minkowskiSupport_attained {p : ℕ} {Wt : Set (Vec p)}
    (hK : IsCompact Wt) (hne : Wt.Nonempty) (v : Vec p) :
    (∀ w ∈ Wt, ∑ i : Fin p, v i * w i ≤ minkowskiSupport Wt v) ∧
    (∃ w ∈ Wt, ∑ i : Fin p, v i * w i = minkowskiSupport Wt v) := by
  let f : Vec p → ℝ := fun w => ∑ i : Fin p, v i * w i
  have hImgK : IsCompact (f '' Wt) := hK.image (dot_continuous v)
  have hImgNe : (f '' Wt).Nonempty := hne.image f
  have hBdd : BddAbove (f '' Wt) := hImgK.bddAbove
  constructor
  · intro w hw
    exact le_csSup hBdd ⟨w, hw, rfl⟩
  · obtain ⟨w, hw, hfeq⟩ := hImgK.sSup_mem hImgNe
    exact ⟨w, hw, hfeq⟩

/-- **Theorem G2.1:** Exact attainment of the stage-wise Minkowski support function over
any family of nonempty compact disturbance sets `W : Fin D.q → Set (Vec D.p)`. -/
theorem general_attained_support (D : Data) (W : Fin D.q → Set (Vec D.p))
    (hW : ∀ t : Fin D.q, IsCompact (W t) ∧ (W t).Nonempty)
    (row : Vec D.n →ₗ[ℝ] ℝ) :
    (∀ wp : StageNoiseBlock D W,
      row (generalFutureNoiseResponse D wp.val) ≤ stageFutureRowSupport D W row) ∧
    (∃ wp : StageNoiseBlock D W,
      row (generalFutureNoiseResponse D wp.val) = stageFutureRowSupport D W row) := by
  constructor
  · intro wp
    rw [general_response_row, stageFutureRowSupport]
    refine Finset.sum_le_sum (fun t _ => ?_)
    exact (minkowskiSupport_attained (hW t).1 (hW t).2 _).1 (wp.val t) (wp.property t)
  · have hex : ∀ t : Fin D.q, ∃ wt ∈ W t,
        ∑ i : Fin D.p, row (D.futureNoiseColumn t i) * wt i =
          minkowskiSupport (W t) (fun i => row (D.futureNoiseColumn t i)) :=
      fun t => (minkowskiSupport_attained (hW t).1 (hW t).2 _).2
    choose w hw_mem hw_eq using hex
    refine ⟨⟨w, hw_mem⟩, ?_⟩
    rw [general_response_row, stageFutureRowSupport]
    exact Finset.sum_congr rfl (fun t _ => hw_eq t)

/-- **Theorem G2.2:** Exact row-wise elimination of stage-wise compact future disturbances. -/
theorem general_robust_row (D : Data) (W : Fin D.q → Set (Vec D.p))
    (hW : ∀ t : Fin D.q, IsCompact (W t) ∧ (W t).Nonempty)
    (row : Vec D.n →ₗ[ℝ] ℝ) (z : Vec D.n) (bound : ℝ) :
    (∀ wp : StageNoiseBlock D W, row (z + generalFutureNoiseResponse D wp.val) ≤ bound) ↔
      row z + stageFutureRowSupport D W row ≤ bound := by
  obtain ⟨upper, wp, attained⟩ := general_attained_support D W hW row
  constructor
  · intro h
    have hh := h wp
    rwa [map_add, attained] at hh
  · intro h wp
    rw [map_add]
    have hh := upper wp
    linarith

/-- **Theorem G2.3:** Exact F3 support-function tightening generalized to ANY family of
nonempty compact stage-wise disturbance sets `W : Fin D.q → Set (Vec D.p)`. -/
theorem general_exact_tightening (D : Data) (W : Fin D.q → Set (Vec D.p))
    (hW : ∀ t : Fin D.q, IsCompact (W t) ∧ (W t).Nonempty)
    (a : D.ControlBlock D.r) (y : D.DeviationPolicy) (eta : ℝ) :
    GeneralAROBound D W a y eta ↔ GeneralTightenedAROBound D W a y eta := by
  constructor
  · intro h xi
    constructor
    · intro i
      constructor
      · apply (general_robust_row D W hW (-(D.terminalRow i)) (D.aroNominalTerminal a y xi)
          (-D.gmin i)).mp
        intro wp
        have hh := (h xi wp).1 i
        rw [general_future_expansion] at hh
        change -(D.H (D.aroNominalTerminal a y xi + generalFutureNoiseResponse D wp.val) i) ≤ -D.gmin i
        exact neg_le_neg hh.1
      · apply (general_robust_row D W hW (D.terminalRow i) (D.aroNominalTerminal a y xi)
          (D.gmax i)).mp
        intro wp
        have hh := (h xi wp).1 i
        rw [general_future_expansion] at hh
        exact hh.2
    · apply (general_robust_row D W hW D.c (D.aroNominalTerminal a y xi) eta).mp
      intro wp
      have hh := (h xi wp).2
      rwa [general_future_expansion] at hh
  · intro h xi wp
    obtain ⟨rows, cost⟩ := h xi
    rw [general_future_expansion]
    constructor
    · intro i
      have hl := (general_robust_row D W hW (-(D.terminalRow i)) (D.aroNominalTerminal a y xi)
        (-D.gmin i)).mpr (rows i).1 wp
      have hu := (general_robust_row D W hW (D.terminalRow i) (D.aroNominalTerminal a y xi)
        (D.gmax i)).mpr (rows i).2 wp
      change -(D.H (D.aroNominalTerminal a y xi + generalFutureNoiseResponse D wp.val) i) ≤ -D.gmin i at hl
      exact ⟨neg_le_neg_iff.mp hl, hu⟩
    · exact (general_robust_row D W hW D.c (D.aroNominalTerminal a y xi) eta).mpr cost wp

/-! ## Section 2: Exact specializations — Box (F3), `l1` cross-polytope, and `l2` SOC ball -/

private theorem minkowskiSupport_eq_of_upper_and_witness {p : ℕ} {Wt : Set (Vec p)}
    {v : Vec p} {val : ℝ}
    (hupper : ∀ w ∈ Wt, ∑ i : Fin p, v i * w i ≤ val)
    (hwit : ∃ w ∈ Wt, ∑ i : Fin p, v i * w i = val) :
    minkowskiSupport Wt v = val := by
  unfold minkowskiSupport
  rcases hwit with ⟨w0, hw0, hfeq⟩
  apply le_antisymm
  · have hne : ((fun w : Vec p => ∑ i : Fin p, v i * w i) '' Wt).Nonempty := ⟨val, w0, hw0, hfeq⟩
    apply csSup_le hne
    rintro y ⟨w, hw, rfl⟩
    exact hupper w hw
  · have hBdd : BddAbove ((fun w : Vec p => ∑ i : Fin p, v i * w i) '' Wt) :=
      ⟨val, by rintro y ⟨w, hw, rfl⟩; exact hupper w hw⟩
    exact le_csSup hBdd ⟨w0, hw0, hfeq⟩

/-- **Theorem G2.4:** Specializing `W t = [-rho, rho]^p` recovers F3 `D.futureRowSupport` exactly. -/
theorem box_support_eq_f3 (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ) :
    let Wbox : Fin D.q → Set (Vec D.p) := fun _ => {w : Vec D.p | D.NoiseOK w}
    (∀ t : Fin D.q, IsCompact (Wbox t) ∧ (Wbox t).Nonempty) ∧
    stageFutureRowSupport D Wbox row = D.futureRowSupport row := by
  classical
  dsimp only
  constructor
  · intro _
    constructor
    · have heq : {w : Vec D.p | D.NoiseOK w} = {w : Vec D.p | ∀ i, w i ∈ Set.Icc (-D.rho) D.rho} := by
        ext w; simp [Data.NoiseOK, Set.mem_Icc]
      rw [heq]
      exact isCompact_pi_infinite (fun _ => isCompact_Icc)
    · exact ⟨fun _ => 0, fun _ => ⟨neg_nonpos.mpr (le_of_lt D.rho_pos), le_of_lt D.rho_pos⟩⟩
  · rw [stageFutureRowSupport, Data.futureRowSupport, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    rw [Finset.mul_sum]
    apply minkowskiSupport_eq_of_upper_and_witness
    · intro w hw
      refine Finset.sum_le_sum (fun i _ => ?_)
      exact BridgeFormalV3.Proofs.coefficient_bound D _ _ (hw i)
    · let w0 : Vec D.p := fun i => if 0 ≤ row (D.futureNoiseColumn t i) then D.rho else -D.rho
      refine ⟨w0, ?_, ?_⟩
      · intro i; dsimp only [w0]; split_ifs <;> constructor <;> linarith [D.rho_pos]
      · apply Finset.sum_congr rfl
        intro i _
        dsimp only [w0]
        split_ifs with hb
        · rw [abs_of_nonneg hb, mul_comm]
        · rw [abs_of_neg (lt_of_not_ge hb)]; ring

/-- Non-box polyhedral `l1` cross-polytope `{w ∈ ℝ^p | ∑ |w_i| ≤ r}`. -/
def l1Ball (p : ℕ) (r : ℝ) : Set (Vec p) :=
  {w : Vec p | ∑ i : Fin p, |w i| ≤ r}

/-- **Theorem G2.5:** Compactness, nonemptiness, and exact dual `l∞` Minkowski support
`h_{B_1(r)}(v) = r * max_i |v_i|` for the `l1` cross-polytope. -/
theorem l1_cross_polytope_support {p : ℕ} (hp : 0 < p) {r : ℝ} (hr : 0 ≤ r) (v : Vec p) :
    let hne : (Finset.univ : Finset (Fin p)).Nonempty := ⟨⟨0, hp⟩, Finset.mem_univ _⟩
    IsCompact (l1Ball p r) ∧
    (l1Ball p r).Nonempty ∧
    minkowskiSupport (l1Ball p r) v = r * Finset.univ.sup' hne (fun i : Fin p => |v i|) := by
  classical
  dsimp only
  let hne : (Finset.univ : Finset (Fin p)).Nonempty := ⟨⟨0, hp⟩, Finset.mem_univ _⟩
  let M : ℝ := Finset.univ.sup' hne (fun i : Fin p => |v i|)
  have hM_ge : ∀ i : Fin p, |v i| ≤ M := fun i =>
    Finset.le_sup' (f := fun j : Fin p => |v j|) (Finset.mem_univ i)
  have hM_nn : 0 ≤ M := le_trans (abs_nonneg (v ⟨0, hp⟩)) (hM_ge ⟨0, hp⟩)
  refine ⟨?_, ?_, ?_⟩
  · have hsub : l1Ball p r ⊆ {w : Vec p | ∀ i, w i ∈ Set.Icc (-r) r} := by
      intro w hw i
      have hle : |w i| ≤ ∑ j : Fin p, |w j| :=
        Finset.single_le_sum (f := fun j => |w j|) (fun j _ => abs_nonneg _) (Finset.mem_univ i)
      exact abs_le.mp (le_trans hle hw)
    have hbox : IsCompact {w : Vec p | ∀ i, w i ∈ Set.Icc (-r) r} :=
      isCompact_pi_infinite (fun _ => isCompact_Icc)
    have hcl : IsClosed (l1Ball p r) := by
      have hcont : Continuous (fun w : Vec p => ∑ i : Fin p, |w i|) :=
        continuous_finsetSum _ (fun i _ => (continuous_apply i).abs)
      exact isClosed_le hcont continuous_const
    exact hbox.of_isClosed_subset hcl hsub
  · refine ⟨0, ?_⟩
    simp [l1Ball, hr]
  · apply minkowskiSupport_eq_of_upper_and_witness
    · intro w hw
      calc ∑ i : Fin p, v i * w i
          ≤ ∑ i : Fin p, |v i * w i| := Finset.sum_le_sum (fun i _ => le_abs_self _)
        _ = ∑ i : Fin p, |v i| * |w i| := Finset.sum_congr rfl (fun i _ => abs_mul _ _)
        _ ≤ ∑ i : Fin p, M * |w i| :=
            Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_right (hM_ge i) (abs_nonneg _))
        _ = M * ∑ i : Fin p, |w i| := (Finset.mul_sum ..).symm
        _ ≤ M * r := mul_le_mul_of_nonneg_left hw hM_nn
        _ = r * M := mul_comm M r
    · obtain ⟨i0, _, hi0⟩ := Finset.exists_mem_eq_sup' hne (fun i : Fin p => |v i|)
      let sgn : ℝ := if 0 ≤ v i0 then r else -r
      let w0 : Vec p := fun i => if i = i0 then sgn else 0
      refine ⟨w0, ?_, ?_⟩
      · have hsum_abs : ∑ i : Fin p, |w0 i| = |sgn| := by
          rw [Finset.sum_eq_single i0]
          · simp [w0]
          · intro j _ hj; simp [w0, hj]
          · intro h; exact False.elim (h (Finset.mem_univ i0))
        change ∑ i : Fin p, |w0 i| ≤ r
        rw [hsum_abs]
        dsimp only [sgn]
        split_ifs
        · rw [abs_of_nonneg hr]
        · rw [abs_neg, abs_of_nonneg hr]
      · rw [Finset.sum_eq_single i0]
        · simp only [w0, ↓reduceIte, sgn]
          split_ifs with hpos
          · rw [hi0, abs_of_nonneg hpos, mul_comm]
          · rw [hi0, abs_of_neg (lt_of_not_ge hpos)]; ring
        · intro j _ hj; simp [w0, hj]
        · intro h; exact False.elim (h (Finset.mem_univ i0))

/-- Non-negative square root via supremum (zero extra Mathlib imports beyond frozen core). -/
def nonnegSqrt (x : ℝ) : ℝ :=
  sSup {t : ℝ | 0 ≤ t ∧ t ^ 2 ≤ x}

private theorem nonnegSqrt_spec {x : ℝ} (hx : 0 ≤ x) :
    0 ≤ nonnegSqrt x ∧ (nonnegSqrt x) ^ 2 = x := by
  let S : Set ℝ := {t : ℝ | 0 ≤ t ∧ t ^ 2 ≤ x}
  have hS_ne : S.Nonempty := ⟨0, le_rfl, by nlinarith⟩
  have hS_sub : S ⊆ Set.Icc 0 (x + 1) := by
    intro t ht
    refine ⟨ht.1, ?_⟩
    nlinarith [ht.1, ht.2]
  have hS_closed : IsClosed S :=
    (isClosed_le continuous_const continuous_id).inter
      (isClosed_le (continuous_id.pow 2) continuous_const)
  have hS_compact : IsCompact S := isCompact_Icc.of_isClosed_subset hS_closed hS_sub
  have hs_mem : nonnegSqrt x ∈ S := hS_compact.sSup_mem hS_ne
  refine ⟨hs_mem.1, le_antisymm hs_mem.2 ?_⟩
  by_contra hlt
  push Not at hlt
  let s := nonnegSqrt x
  have hgap : 0 < x - s ^ 2 := sub_pos.mpr hlt
  let eps : ℝ := min 1 ((x - s ^ 2) / (2 * s + 2))
  have hden_pos : 0 < 2 * s + 2 := by linarith [hs_mem.1]
  have heps_pos : 0 < eps := lt_min zero_lt_one (div_pos hgap hden_pos)
  have heps_le1 : eps ≤ 1 := min_le_left _ _
  have heps_le2 : eps ≤ (x - s ^ 2) / (2 * s + 2) := min_le_right _ _
  have hmul : eps * (2 * s + 2) ≤ x - s ^ 2 := (le_div_iff₀ hden_pos).mp heps_le2
  have hsq_le : (s + eps) ^ 2 ≤ x := by nlinarith
  have hmem' : s + eps ∈ S := ⟨by linarith [hs_mem.1], hsq_le⟩
  have hle : s + eps ≤ s := le_csSup hS_compact.bddAbove hmem'
  linarith

/-- Non-polyhedral Euclidean / Second-Order Cone (SOC) ball `{w ∈ ℝ^p | ∑ w_i^2 ≤ r^2}`. -/
def l2Ball (p : ℕ) (r : ℝ) : Set (Vec p) :=
  {w : Vec p | ∑ i : Fin p, (w i) ^ 2 ≤ r ^ 2}

private theorem sum_mul_sq_le_cauchy_schwarz {p : ℕ} (v w : Vec p) :
    (∑ i : Fin p, v i * w i) ^ 2 ≤ (∑ i : Fin p, (v i) ^ 2) * (∑ i : Fin p, (w i) ^ 2) := by
  exact Finset.sum_mul_sq_le_sq_mul_sq Finset.univ v w

/-- **Theorem G2.6:** Compactness, nonemptiness, and exact self-dual SOC Minkowski support
`h_{B_2(r)}(v) = r * √(∑ v_i^2)` (with `0 ≤ h` and `h^2 = r^2 * ∑ v_i^2`) for the Euclidean `l2` ball. -/
theorem l2_soc_ball_support {p : ℕ} {r : ℝ} (hr : 0 ≤ r) (v : Vec p) :
    IsCompact (l2Ball p r) ∧
    (l2Ball p r).Nonempty ∧
    minkowskiSupport (l2Ball p r) v = r * nonnegSqrt (∑ i : Fin p, (v i) ^ 2) ∧
    0 ≤ minkowskiSupport (l2Ball p r) v ∧
    (minkowskiSupport (l2Ball p r) v) ^ 2 = r ^ 2 * ∑ i : Fin p, (v i) ^ 2 := by
  have hsum_v_nn : 0 ≤ ∑ i : Fin p, (v i) ^ 2 := Finset.sum_nonneg (fun i _ => sq_nonneg _)
  obtain ⟨hnv_nn, hnv_sq⟩ := nonnegSqrt_spec hsum_v_nn
  let nv : ℝ := nonnegSqrt (∑ i : Fin p, (v i) ^ 2)
  have hsupp_eq : minkowskiSupport (l2Ball p r) v = r * nv := by
    apply minkowskiSupport_eq_of_upper_and_witness
    · intro w hw
      have hcs := sum_mul_sq_le_cauchy_schwarz v w
      have hprod : (∑ i : Fin p, (v i) ^ 2) * (∑ i : Fin p, (w i) ^ 2) ≤ (r * nv) ^ 2 := by
        rw [mul_pow, hnv_sq, mul_comm (r ^ 2)]
        exact mul_le_mul_of_nonneg_left hw hsum_v_nn
      have hsq_le : (∑ i : Fin p, v i * w i) ^ 2 ≤ (r * nv) ^ 2 := le_trans hcs hprod
      have hrhs_nn : 0 ≤ r * nv := mul_nonneg hr hnv_nn
      nlinarith
    · by_cases hv0 : ∑ i : Fin p, (v i) ^ 2 = 0
      · have hnv0 : nv = 0 := by
          have : nv ^ 2 = 0 := hnv_sq.trans hv0
          exact sq_eq_zero_iff.mp this
        refine ⟨0, ?_, ?_⟩
        · change ∑ i : Fin p, ((0 : Vec p) i) ^ 2 ≤ r ^ 2
          simp only [Pi.zero_apply]
          have h0 : ∑ _i : Fin p, (0 : ℝ) ^ 2 = 0 := by simp
          rw [h0]; exact sq_nonneg r
        · simp [hnv0]
      · have hsum_pos : 0 < ∑ i : Fin p, (v i) ^ 2 := lt_of_le_of_ne hsum_v_nn (Ne.symm hv0)
        have hnv_pos : 0 < nv := by
          refine lt_of_le_of_ne hnv_nn (fun h0 => ?_)
          have : (0 : ℝ) ^ 2 = ∑ i : Fin p, (v i) ^ 2 := by rw [h0]; exact hnv_sq
          linarith
        have hnv_ne : nv ≠ 0 := ne_of_gt hnv_pos
        let w0 : Vec p := fun i => r * v i / nv
        refine ⟨w0, ?_, ?_⟩
        · change ∑ i : Fin p, (r * v i / nv) ^ 2 ≤ r ^ 2
          have hrew : ∑ i : Fin p, (r * v i / nv) ^ 2 =
              (r ^ 2 / nv ^ 2) * ∑ i : Fin p, (v i) ^ 2 := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro i _; ring
          rw [hrew, ← hnv_sq, div_mul_cancel₀ _ (pow_ne_zero 2 hnv_ne)]
        · have hrew : ∑ i : Fin p, v i * w0 i =
              (r / nv) * ∑ i : Fin p, (v i) ^ 2 := by
            rw [Finset.mul_sum]
            apply Finset.sum_congr rfl
            intro i _; dsimp only [w0]; ring
          rw [hrew, ← hnv_sq]
          field_simp [hnv_ne]
          rfl
  refine ⟨?_, ?_, hsupp_eq, ?_, ?_⟩
  · have hsub : l2Ball p r ⊆ {w : Vec p | ∀ i, w i ∈ Set.Icc (-r) r} := by
      intro w hw i
      have hsq : (w i) ^ 2 ≤ r ^ 2 :=
        le_trans (Finset.single_le_sum (f := fun j => (w j) ^ 2) (fun j _ => sq_nonneg _)
          (Finset.mem_univ i)) hw
      exact ⟨by nlinarith, by nlinarith⟩
    have hbox : IsCompact {w : Vec p | ∀ i, w i ∈ Set.Icc (-r) r} :=
      isCompact_pi_infinite (fun _ => isCompact_Icc)
    have hcl : IsClosed (l2Ball p r) := by
      have hcont : Continuous (fun w : Vec p => ∑ i : Fin p, (w i) ^ 2) :=
        continuous_finsetSum _ (fun i _ => (continuous_apply i).pow 2)
      exact isClosed_le hcont continuous_const
    exact hbox.of_isClosed_subset hcl hsub
  · refine ⟨0, ?_⟩
    change ∑ i : Fin p, ((0 : Vec p) i) ^ 2 ≤ r ^ 2
    simp only [Pi.zero_apply]
    have h0 : ∑ _i : Fin p, (0 : ℝ) ^ 2 = 0 := by simp
    rw [h0]
    exact sq_nonneg r
  · rw [hsupp_eq]; exact mul_nonneg hr hnv_nn
  · rw [hsupp_eq, mul_pow, hnv_sq]

/-! ## Section 3: Non-polyhedrality of the 2D `l2` SOC ball (no finite vertex-LP reduction) -/

/-- Standard extreme point of a set `S ⊆ Vec n`. -/
def IsExtremePoint {n : ℕ} (S : Set (Vec n)) (v : Vec n) : Prop :=
  v ∈ S ∧ ∀ x ∈ S, ∀ y ∈ S, ∀ θ : ℝ,
    0 < θ → θ < 1 → v = θ • x + (1 - θ) • y → x = v ∧ y = v

/-- Finite convex hull membership in `T : Finset (Vec n)`. -/
def InFinsetConv {n : ℕ} (T : Finset (Vec n)) (x : Vec n) : Prop :=
  ∃ w : Vec n → ℝ, (∀ t ∈ T, 0 ≤ w t) ∧ (∑ t ∈ T, w t = 1) ∧ (∑ t ∈ T, w t • t = x)

private theorem l2Ball_convex (p : ℕ) {r : ℝ} :
    ∀ x ∈ l2Ball p r, ∀ y ∈ l2Ball p r, ∀ θ : ℝ,
      0 ≤ θ → θ ≤ 1 → θ • x + (1 - θ) • y ∈ l2Ball p r := by
  intro x hx y hy θ hθ0 hθ1
  change ∑ i : Fin p, (θ * x i + (1 - θ) * y i) ^ 2 ≤ r ^ 2
  have hpoint : ∀ i : Fin p,
      (θ * x i + (1 - θ) * y i) ^ 2 ≤ θ * (x i) ^ 2 + (1 - θ) * (y i) ^ 2 := by
    intro i
    have hdiff : θ * (x i) ^ 2 + (1 - θ) * (y i) ^ 2 - (θ * x i + (1 - θ) * y i) ^ 2 =
        θ * (1 - θ) * (x i - y i) ^ 2 := by ring
    have hnn : 0 ≤ θ * (1 - θ) * (x i - y i) ^ 2 :=
      mul_nonneg (mul_nonneg hθ0 (by linarith)) (sq_nonneg _)
    linarith
  calc ∑ i : Fin p, (θ * x i + (1 - θ) * y i) ^ 2
      ≤ ∑ i : Fin p, (θ * (x i) ^ 2 + (1 - θ) * (y i) ^ 2) :=
        Finset.sum_le_sum (fun i _ => hpoint i)
    _ = θ * (∑ i : Fin p, (x i) ^ 2) + (1 - θ) * (∑ i : Fin p, (y i) ^ 2) := by
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum]
    _ ≤ θ * r ^ 2 + (1 - θ) * r ^ 2 := by
        have h1 : θ * (∑ i : Fin p, (x i) ^ 2) ≤ θ * r ^ 2 := mul_le_mul_of_nonneg_left hx hθ0
        have h2 : (1 - θ) * (∑ i : Fin p, (y i) ^ 2) ≤ (1 - θ) * r ^ 2 :=
          mul_le_mul_of_nonneg_left hy (by linarith)
        linarith
    _ = r ^ 2 := by ring

private theorem sphere_point_is_extreme (p : ℕ) {r : ℝ} (v : Vec p)
    (hv : ∑ i : Fin p, (v i) ^ 2 = r ^ 2) :
    IsExtremePoint (l2Ball p r) v := by
  refine ⟨by change ∑ i : Fin p, (v i) ^ 2 ≤ r ^ 2; linarith, ?_⟩
  intro x hx y hy θ hθ0 hθ1 hveq
  have hident : ∀ i : Fin p,
      θ * (x i) ^ 2 + (1 - θ) * (y i) ^ 2 - (v i) ^ 2 =
        θ * (1 - θ) * (x i - y i) ^ 2 := by
    intro i
    have hvi : v i = θ * x i + (1 - θ) * y i := by
      have := congrFun hveq i
      simpa [Pi.add_apply, Pi.smul_apply, smul_eq_mul] using this
    rw [hvi]; ring
  have hsum_ident :
      θ * (∑ i : Fin p, (x i) ^ 2) + (1 - θ) * (∑ i : Fin p, (y i) ^ 2) - r ^ 2 =
        θ * (1 - θ) * ∑ i : Fin p, (x i - y i) ^ 2 := by
    rw [← hv, Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib, ← Finset.sum_sub_distrib,
      Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro i _
    exact hident i
  have hle0 : θ * (1 - θ) * ∑ i : Fin p, (x i - y i) ^ 2 ≤ 0 := by
    have h1 : θ * (∑ i : Fin p, (x i) ^ 2) ≤ θ * r ^ 2 :=
      mul_le_mul_of_nonneg_left hx (le_of_lt hθ0)
    have h2 : (1 - θ) * (∑ i : Fin p, (y i) ^ 2) ≤ (1 - θ) * r ^ 2 :=
      mul_le_mul_of_nonneg_left hy (by linarith)
    linarith
  have hprod_pos : 0 < θ * (1 - θ) := mul_pos hθ0 (by linarith)
  have hsum_nn : 0 ≤ ∑ i : Fin p, (x i - y i) ^ 2 := Finset.sum_nonneg (fun i _ => sq_nonneg _)
  have hsum_zero : ∑ i : Fin p, (x i - y i) ^ 2 = 0 := by nlinarith
  have hxy : x = y := by
    funext i
    have hterm := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ => sq_nonneg (x j - y j))).mp
      hsum_zero i (Finset.mem_univ i)
    have hdiff0 : x i - y i = 0 := sq_eq_zero_iff.mp hterm
    linarith
  have hxv : x = v := by
    rw [hveq, hxy, ← add_smul]
    simp
  exact ⟨hxv, hxy.symm.trans hxv⟩

private theorem finset_conv_mem_l2 {p : ℕ} {r : ℝ}
    (T : Finset (Vec p)) (hT : ∀ t ∈ T, t ∈ l2Ball p r) :
    ∀ x, InFinsetConv T x → x ∈ l2Ball p r := by
  classical
  induction T using Finset.induction_on with
  | empty =>
    rintro x ⟨w, _, hsum, _⟩
    simp only [Finset.sum_empty] at hsum
    linarith
  | @insert a T ha ih =>
    rintro x ⟨w, hw, hsum, hx⟩
    rw [Finset.sum_insert ha] at hsum hx
    have hwa_nn : 0 ≤ w a := hw a (Finset.mem_insert_self a T)
    have hrest_nn : ∀ t ∈ T, 0 ≤ w t := fun t ht => hw t (Finset.mem_insert_of_mem ht)
    have hrest_sum_nn : 0 ≤ ∑ t ∈ T, w t := Finset.sum_nonneg hrest_nn
    by_cases h1 : w a = 1
    · have hsum0 : ∑ t ∈ T, w t = 0 := by linarith
      have hzero : ∀ t ∈ T, w t = 0 := fun t ht =>
        (Finset.sum_eq_zero_iff_of_nonneg hrest_nn).mp hsum0 t ht
      have hx_eq : x = a := by
        rw [← hx, h1, one_smul]
        have hvec0 : ∑ t ∈ T, w t • t = 0 :=
          Finset.sum_eq_zero (fun t ht => by rw [hzero t ht, zero_smul])
        rw [hvec0, add_zero]
      rw [hx_eq]; exact hT a (Finset.mem_insert_self a T)
    · have hwa_lt : w a < 1 := lt_of_le_of_ne (by linarith) h1
      have hden_pos : 0 < 1 - w a := sub_pos.mpr hwa_lt
      have hrest_eq : ∑ t ∈ T, w t = 1 - w a := by linarith
      let y : Vec p := ∑ t ∈ T, (w t / (1 - w a)) • t
      have hyB : y ∈ l2Ball p r := by
        apply ih (fun t ht => hT t (Finset.mem_insert_of_mem ht))
        refine ⟨fun t => w t / (1 - w a), ?_, ?_, rfl⟩
        · intro t ht; exact div_nonneg (hrest_nn t ht) (le_of_lt hden_pos)
        · simp_rw [div_eq_mul_inv]
          rw [← Finset.sum_mul, hrest_eq, mul_inv_cancel₀ (ne_of_gt hden_pos)]
      have hx_comb : x = w a • a + (1 - w a) • y := by
        rw [← hx]; congr 1
        dsimp only [y]; rw [Finset.smul_sum]
        apply Finset.sum_congr rfl
        intro t _; rw [smul_smul, mul_div_cancel₀ _ (ne_of_gt hden_pos)]
      rw [hx_comb]
      exact l2Ball_convex p a (hT a (Finset.mem_insert_self a T)) y hyB
        (w a) hwa_nn (le_of_lt hwa_lt)

private theorem extreme_mem_finset_l2 {p : ℕ} {r : ℝ}
    (T : Finset (Vec p)) (hT : ∀ t ∈ T, t ∈ l2Ball p r)
    (hgen : ∀ x ∈ l2Ball p r, InFinsetConv T x)
    {v : Vec p} (hv : IsExtremePoint (l2Ball p r) v) : v ∈ T := by
  classical
  by_contra hvnot
  obtain ⟨w, hw, hsum, hvsum⟩ := hgen v hv.1
  have hpos_ex : ∃ t0 ∈ T, 0 < w t0 := by
    by_contra hall
    push Not at hall
    have hle : ∑ t ∈ T, w t ≤ 0 :=
      le_trans (Finset.sum_le_sum (fun t ht => hall t ht)) (by simp)
    linarith
  obtain ⟨t0, ht0, hwt0_pos⟩ := hpos_ex
  have ht0_ne : t0 ≠ v := fun h => hvnot (h ▸ ht0)
  have hwt0_le : w t0 ≤ 1 := by
    have hsp := Finset.add_sum_erase T w ht0
    have hrest_nn : 0 ≤ ∑ t ∈ T.erase t0, w t :=
      Finset.sum_nonneg (fun t ht => hw t (Finset.mem_of_mem_erase ht))
    linarith
  have hwt0_lt : w t0 < 1 := by
    refine lt_of_le_of_ne hwt0_le (fun h1 => ?_)
    have hsp := Finset.add_sum_erase T w ht0
    have hrest_nn : ∀ t ∈ T.erase t0, 0 ≤ w t := fun t ht => hw t (Finset.mem_of_mem_erase ht)
    have hrest0 : ∑ t ∈ T.erase t0, w t = 0 := by linarith
    have hzero : ∀ t ∈ T.erase t0, w t = 0 := fun t ht =>
      (Finset.sum_eq_zero_iff_of_nonneg hrest_nn).mp hrest0 t ht
    have hv_t0 : v = t0 := by
      rw [← hvsum, ← Finset.add_sum_erase T (fun t => w t • t) ht0, h1, one_smul]
      have hvec0 : ∑ t ∈ T.erase t0, w t • t = 0 :=
        Finset.sum_eq_zero (fun t ht => by rw [hzero t ht, zero_smul])
      rw [hvec0, add_zero]
    exact ht0_ne hv_t0.symm
  have hden_pos : 0 < 1 - w t0 := sub_pos.mpr hwt0_lt
  have hrest_sum : ∑ t ∈ T.erase t0, w t = 1 - w t0 := by
    have hsp := Finset.add_sum_erase T w ht0; linarith
  let y : Vec p := ∑ t ∈ T.erase t0, (w t / (1 - w t0)) • t
  have hyB : y ∈ l2Ball p r := by
    apply finset_conv_mem_l2 (T.erase t0) (fun t ht => hT t (Finset.mem_of_mem_erase ht))
    refine ⟨fun t => w t / (1 - w t0), ?_, ?_, rfl⟩
    · intro t ht; exact div_nonneg (hw t (Finset.mem_of_mem_erase ht)) (le_of_lt hden_pos)
    · simp_rw [div_eq_mul_inv]
      rw [← Finset.sum_mul, hrest_sum, mul_inv_cancel₀ (ne_of_gt hden_pos)]
  have hv_eq : v = w t0 • t0 + (1 - w t0) • y := by
    rw [← hvsum, ← Finset.add_sum_erase T (fun t => w t • t) ht0]; congr 1
    dsimp only [y]; rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro t _; rw [smul_smul, mul_div_cancel₀ _ (ne_of_gt hden_pos)]
  exact ht0_ne (hv.2 t0 (hT t0 ht0) y hyB (w t0) hwt0_pos hwt0_lt hv_eq).1

/-- Rational stereographic parameterization of infinitely many points on the 2D circle of radius `r`. -/
def stereoCirclePoint (r : ℝ) (k : ℕ) : Vec 2 :=
  fun i => if i = 0 then r * (((k : ℝ) ^ 2 - 1) / ((k : ℝ) ^ 2 + 1))
           else r * ((2 * (k : ℝ)) / ((k : ℝ) ^ 2 + 1))

private theorem stereoCirclePoint_norm_sq (r : ℝ) (k : ℕ) :
    ∑ i : Fin 2, (stereoCirclePoint r k i) ^ 2 = r ^ 2 := by
  rw [Fin.sum_univ_two]
  simp only [stereoCirclePoint, ↓reduceIte, Fin.one_eq_zero_iff, Nat.succ_ne_self]
  have hden : ((k : ℝ) ^ 2 + 1) ≠ 0 := by positivity
  field_simp [hden]
  ring

private theorem stereoCirclePoint_injective {r : ℝ} (hr : 0 < r) :
    Function.Injective (stereoCirclePoint r) := by
  intro k1 k2 h
  have h0 : stereoCirclePoint r k1 0 = stereoCirclePoint r k2 0 := congrFun h 0
  simp only [stereoCirclePoint, ↓reduceIte] at h0
  have hfrac : (((k1 : ℝ) ^ 2 - 1) / ((k1 : ℝ) ^ 2 + 1)) =
      (((k2 : ℝ) ^ 2 - 1) / ((k2 : ℝ) ^ 2 + 1)) := mul_left_cancel₀ (ne_of_gt hr) h0
  have hd1 : (0 : ℝ) < (k1 : ℝ) ^ 2 + 1 := by positivity
  have hd2 : (0 : ℝ) < (k2 : ℝ) ^ 2 + 1 := by positivity
  have hcross : ((k1 : ℝ) ^ 2 - 1) * ((k2 : ℝ) ^ 2 + 1) =
      ((k2 : ℝ) ^ 2 - 1) * ((k1 : ℝ) ^ 2 + 1) := (div_eq_div_iff (ne_of_gt hd1) (ne_of_gt hd2)).mp hfrac
  have hsq : (k1 : ℝ) ^ 2 = (k2 : ℝ) ^ 2 := by linarith
  have hk_real : (k1 : ℝ) = (k2 : ℝ) := by
    have hnn1 : (0 : ℝ) ≤ (k1 : ℝ) := Nat.cast_nonneg k1
    have hnn2 : (0 : ℝ) ≤ (k2 : ℝ) := Nat.cast_nonneg k2
    nlinarith
  exact Nat.cast_injective hk_real

/-- **Theorem G2.7:** For `r > 0`, the 2D Euclidean SOC ball `l2Ball 2 r` is NOT the convex
hull of any finite vertex set `T : Finset (Vec 2)` (formalizing the non-polyhedral boundary of G2). -/
theorem l2_ball_not_finset_conv_2d {r : ℝ} (hr : 0 < r) :
    ¬ ∃ T : Finset (Vec 2),
      (∀ t ∈ T, t ∈ l2Ball 2 r) ∧ (∀ x ∈ l2Ball 2 r, InFinsetConv T x) := by
  rintro ⟨T, hT, hgen⟩
  have hmem : ∀ k : ℕ, stereoCirclePoint r k ∈ T := by
    intro k
    exact extreme_mem_finset_l2 T hT hgen
      (sphere_point_is_extreme 2 (stereoCirclePoint r k) (stereoCirclePoint_norm_sq r k))
  let S : Finset (Vec 2) := (Finset.range (T.card + 1)).image (stereoCirclePoint r)
  have hsub : S ⊆ T := by
    intro x hx
    rcases Finset.mem_image.mp hx with ⟨k, _, rfl⟩
    exact hmem k
  have hcard_S : S.card = T.card + 1 := by
    rw [Finset.card_image_of_injective _ (stereoCirclePoint_injective hr), Finset.card_range]
  have hle : S.card ≤ T.card := Finset.card_le_card hsub
  omega

end AroProofs.BridgeG2ConicSupport
