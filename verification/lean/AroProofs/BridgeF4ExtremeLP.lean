import AroProofs.BridgeF4CornerLP

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 MeasureTheory Set

namespace AroProofs.BridgeF4VertexLP

/-! ## Section 6: Exact Reduction to the True Extreme Points `vert(Xi)` of the Zonotope `Xi = D.Z` -/

/-- Standard extreme point of a set `S ⊆ Vec n`:
`v ∈ S` and `v` cannot lie in the open segment between two points of `S` other than `v`. -/
def IsExtremePoint {n : ℕ} (S : Set (Vec n)) (v : Vec n) : Prop :=
  v ∈ S ∧ ∀ x ∈ S, ∀ y ∈ S, ∀ θ : ℝ,
    0 < θ → θ < 1 → v = θ • x + (1 - θ) • y → x = v ∧ y = v

/-- The set of true extreme points (vertices) `vert(Xi)` of the zonotope `Xi = D.Z`. -/
def zonotopeVertices (D : Data) : Set (Vec D.n) :=
  {v | IsExtremePoint D.Z v}

/-- `x` is a finite convex combination of elements of `T : Finset (Vec n)`. -/
def InFinsetConv {n : ℕ} (T : Finset (Vec n)) (x : Vec n) : Prop :=
  ∃ w : Vec n → ℝ, (∀ t ∈ T, 0 ≤ w t) ∧ (∑ t ∈ T, w t = 1) ∧ (∑ t ∈ T, w t • t = x)

/-- Finite image of the `2^(r*p)` hypercube corners under `D.deviation`. -/
def cornerImages (D : Data) : Finset (Vec D.n) :=
  Finset.univ.image (fun σ : Corner D => D.deviation (cornerNoise D σ))

private theorem zonotope_convex (D : Data) :
    ∀ x ∈ D.Z, ∀ y ∈ D.Z, ∀ θ : ℝ, 0 ≤ θ → θ ≤ 1 → θ • x + (1 - θ) • y ∈ D.Z := by
  rintro x ⟨wx, rfl⟩ y ⟨wy, rfl⟩ θ hθ0 hθ1
  let w : D.NoiseBlock D.r :=
    ⟨fun t i => θ * wx.val t i + (1 - θ) * wy.val t i, by
      intro t i
      have hx := wx.property t i
      have hy := wy.property t i
      constructor <;> nlinarith⟩
  refine ⟨w, ?_⟩
  rw [deviation_eq_flatDeviation D w, deviation_eq_flatDeviation D wx,
    deviation_eq_flatDeviation D wy]
  simp only [flatDeviation, blockToFlat, Finset.smul_sum, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro t _
  apply Finset.sum_congr rfl
  intro i _
  rw [smul_smul, smul_smul, ← add_smul]

private theorem finset_conv_mem_of_convex {n : ℕ} {S : Set (Vec n)}
    (hS : ∀ x ∈ S, ∀ y ∈ S, ∀ θ : ℝ, 0 ≤ θ → θ ≤ 1 → θ • x + (1 - θ) • y ∈ S)
    (T : Finset (Vec n)) (hT : ∀ t ∈ T, t ∈ S) :
    ∀ x, InFinsetConv T x → x ∈ S := by
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
        have hsum_vec : ∑ t ∈ T, w t • t = 0 :=
          Finset.sum_eq_zero (fun t ht => by rw [hzero t ht, zero_smul])
        rw [hsum_vec, add_zero]
      rw [hx_eq]
      exact hT a (Finset.mem_insert_self a T)
    · have hwa_lt : w a < 1 := lt_of_le_of_ne (by linarith) h1
      have hden_pos : 0 < 1 - w a := sub_pos.mpr hwa_lt
      have hrest_eq : ∑ t ∈ T, w t = 1 - w a := by linarith
      let y : Vec n := ∑ t ∈ T, (w t / (1 - w a)) • t
      have hyS : y ∈ S := by
        apply ih (fun t ht => hT t (Finset.mem_insert_of_mem ht))
        refine ⟨fun t => w t / (1 - w a), ?_, ?_, rfl⟩
        · intro t ht; exact div_nonneg (hrest_nn t ht) (le_of_lt hden_pos)
        · simp_rw [div_eq_mul_inv]
          rw [← Finset.sum_mul, hrest_eq, mul_inv_cancel₀ (ne_of_gt hden_pos)]
      have hx_comb : x = w a • a + (1 - w a) • y := by
        rw [← hx]
        congr 1
        dsimp only [y]
        rw [Finset.smul_sum]
        apply Finset.sum_congr rfl
        intro t _
        rw [smul_smul, mul_div_cancel₀ _ (ne_of_gt hden_pos)]
      rw [hx_comb]
      exact hS a (hT a (Finset.mem_insert_self a T)) y hyS (w a) hwa_nn (le_of_lt hwa_lt)

private theorem zonotope_in_conv_cornerImages (D : Data) :
    ∀ x ∈ D.Z, InFinsetConv (cornerImages D) x := by
  classical
  rintro x ⟨w, rfl⟩
  let f : Corner D → Vec D.n := fun σ => D.deviation (cornerNoise D σ)
  let α : Corner D → ℝ := fun σ => baryWeight D.rho σ (blockToFlat w.val)
  have hα_nn : ∀ σ : Corner D, 0 ≤ α σ := by
    intro σ
    apply baryWeight_nonneg D.rho_pos
    intro k
    exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
  let wt : Vec D.n → ℝ := fun t => ∑ σ ∈ Finset.univ.filter (fun σ => f σ = t), α σ
  refine ⟨wt, ?_, ?_, ?_⟩
  · intro t _
    exact Finset.sum_nonneg (fun σ _ => hα_nn σ)
  · have hfib := Finset.sum_fiberwise_of_maps_to
      (s := (Finset.univ : Finset (Corner D))) (t := cornerImages D) (g := f) (f := α)
      (fun σ _ => Finset.mem_image_of_mem f (Finset.mem_univ σ))
    rw [hfib]
    exact sum_baryWeight D.rho_pos (blockToFlat w.val)
  · have hterm : ∀ t ∈ cornerImages D,
        wt t • t = ∑ σ ∈ Finset.univ.filter (fun σ => f σ = t), α σ • f σ := by
      intro t _
      dsimp only [wt]
      rw [Finset.sum_smul]
      apply Finset.sum_congr rfl
      intro σ hσ
      rw [(Finset.mem_filter.mp hσ).2]
    rw [Finset.sum_congr rfl hterm]
    have hfib := Finset.sum_fiberwise_of_maps_to
      (s := (Finset.univ : Finset (Corner D))) (t := cornerImages D) (g := f)
      (f := fun σ => α σ • f σ)
      (fun σ _ => Finset.mem_image_of_mem f (Finset.mem_univ σ))
    rw [hfib]
    exact deviation_barycentric D w

private theorem sum_eq_self_of_weight_one {n : ℕ} (T : Finset (Vec n)) (t0 : Vec n) (ht0 : t0 ∈ T)
    (w : Vec n → ℝ) (hw : ∀ t ∈ T, 0 ≤ w t) (hsum : ∑ t ∈ T, w t = 1) (hw1 : w t0 = 1) :
    ∑ t ∈ T, w t • t = t0 := by
  classical
  have hsplit := Finset.add_sum_erase T w ht0
  have hrest_nn : ∀ t ∈ T.erase t0, 0 ≤ w t := fun t ht => hw t (Finset.mem_of_mem_erase ht)
  have hrest0 : ∑ t ∈ T.erase t0, w t = 0 := by linarith
  have hzero : ∀ t ∈ T.erase t0, w t = 0 := fun t ht =>
    (Finset.sum_eq_zero_iff_of_nonneg hrest_nn).mp hrest0 t ht
  rw [← Finset.add_sum_erase T (fun t => w t • t) ht0, hw1, one_smul]
  have hvec0 : ∑ t ∈ T.erase t0, w t • t = 0 :=
    Finset.sum_eq_zero (fun t ht => by rw [hzero t ht, zero_smul])
  rw [hvec0, add_zero]

private theorem extreme_point_mem_generating_finset {n : ℕ} {S : Set (Vec n)}
    (hS : ∀ x ∈ S, ∀ y ∈ S, ∀ θ : ℝ, 0 ≤ θ → θ ≤ 1 → θ • x + (1 - θ) • y ∈ S)
    (T : Finset (Vec n)) (hT : ∀ t ∈ T, t ∈ S) (hgen : ∀ x ∈ S, InFinsetConv T x)
    {v : Vec n} (hv : IsExtremePoint S v) : v ∈ T := by
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
    have hsplit := Finset.add_sum_erase T w ht0
    have hrest_nn : 0 ≤ ∑ t ∈ T.erase t0, w t :=
      Finset.sum_nonneg (fun t ht => hw t (Finset.mem_of_mem_erase ht))
    linarith
  have hwt0_lt : w t0 < 1 := by
    refine lt_of_le_of_ne hwt0_le (fun h1 => ?_)
    have heq := sum_eq_self_of_weight_one T t0 ht0 w hw hsum h1
    exact ht0_ne (heq.symm.trans hvsum)
  have hden_pos : 0 < 1 - w t0 := sub_pos.mpr hwt0_lt
  have hrest_sum : ∑ t ∈ T.erase t0, w t = 1 - w t0 := by
    have hsplit := Finset.add_sum_erase T w ht0
    linarith
  let y : Vec n := ∑ t ∈ T.erase t0, (w t / (1 - w t0)) • t
  have hyS : y ∈ S := by
    apply finset_conv_mem_of_convex hS (T.erase t0) (fun t ht => hT t (Finset.mem_of_mem_erase ht))
    refine ⟨fun t => w t / (1 - w t0), ?_, ?_, rfl⟩
    · intro t ht; exact div_nonneg (hw t (Finset.mem_of_mem_erase ht)) (le_of_lt hden_pos)
    · simp_rw [div_eq_mul_inv]
      rw [← Finset.sum_mul, hrest_sum, mul_inv_cancel₀ (ne_of_gt hden_pos)]
  have hv_eq : v = w t0 • t0 + (1 - w t0) • y := by
    rw [← hvsum, ← Finset.add_sum_erase T (fun t => w t • t) ht0]
    congr 1
    dsimp only [y]
    rw [Finset.smul_sum]
    apply Finset.sum_congr rfl
    intro t _
    rw [smul_smul, mul_div_cancel₀ _ (ne_of_gt hden_pos)]
  have hcontra := (hv.2 t0 (hT t0 ht0) y hyS (w t0) hwt0_pos hwt0_lt hv_eq).1
  exact ht0_ne hcontra

private theorem conv_erase_redundant {n : ℕ} (T : Finset (Vec n)) (t0 : Vec n) (ht0 : t0 ∈ T)
    (ht0_conv : InFinsetConv (T.erase t0) t0) {z : Vec n} (hz : InFinsetConv T z) :
    InFinsetConv (T.erase t0) z := by
  classical
  obtain ⟨u, hu_nn, hu_sum, hu_eq⟩ := ht0_conv
  obtain ⟨w, hw_nn, hw_sum, hw_eq⟩ := hz
  let w' : Vec n → ℝ := fun t => w t + w t0 * u t
  have hwt0_nn : 0 ≤ w t0 := hw_nn t0 ht0
  refine ⟨w', ?_, ?_, ?_⟩
  · intro t ht
    exact add_nonneg (hw_nn t (Finset.mem_of_mem_erase ht)) (mul_nonneg hwt0_nn (hu_nn t ht))
  · dsimp only [w']
    rw [Finset.sum_add_distrib, ← Finset.mul_sum, hu_sum, mul_one, add_comm]
    rw [Finset.add_sum_erase T w ht0]
    exact hw_sum
  · dsimp only [w']
    simp_rw [add_smul, mul_smul]
    rw [Finset.sum_add_distrib, ← Finset.smul_sum, hu_eq, add_comm]
    rw [Finset.add_sum_erase T (fun t => w t • t) ht0]
    exact hw_eq

private theorem finset_conv_reduces_to_extreme_aux {n : ℕ} {S : Set (Vec n)} :
    ∀ k : ℕ, ∀ T : Finset (Vec n), T.card ≤ k →
      (∀ t ∈ T, t ∈ S) → (∀ x ∈ S, InFinsetConv T x) →
      ∃ E : Finset (Vec n), (∀ v ∈ E, IsExtremePoint S v) ∧ (∀ x ∈ S, InFinsetConv E x) := by
  classical
  intro k
  induction k with
  | zero =>
    intro T hcard hT hgen
    have hEmpty : T = ∅ := Finset.card_eq_zero.mp (Nat.eq_zero_of_le_zero hcard)
    subst hEmpty
    exact ⟨∅, fun _ hv => False.elim (Finset.notMem_empty _ hv), hgen⟩
  | succ k ih =>
    intro T hcard hT hgen
    by_cases hall : ∀ t ∈ T, IsExtremePoint S t
    · exact ⟨T, hall, hgen⟩
    · push Not at hall
      obtain ⟨t0, ht0, hnot_ext⟩ := hall
      have ht0S : t0 ∈ S := hT t0 ht0
      have hdecomp : ∃ x ∈ S, ∃ y ∈ S, ∃ θ : ℝ,
          0 < θ ∧ θ < 1 ∧ t0 = θ • x + (1 - θ) • y ∧ ¬ (x = t0 ∧ y = t0) := by
        by_contra hnone
        push Not at hnone
        exact hnot_ext ⟨ht0S, fun x hx y hy θ h0 h1 heq => hnone x hx y hy θ h0 h1 heq⟩
      obtain ⟨x, hxS, y, hyS, θ, hθ0, hθ1, ht0_eq, hne⟩ := hdecomp
      obtain ⟨α, hα_nn, hα_sum, hα_eq⟩ := hgen x hxS
      obtain ⟨β, hβ_nn, hβ_sum, hβ_eq⟩ := hgen y hyS
      let γ : Vec n → ℝ := fun t => θ * α t + (1 - θ) * β t
      have hγ_nn : ∀ t ∈ T, 0 ≤ γ t := fun t ht =>
        add_nonneg (mul_nonneg (le_of_lt hθ0) (hα_nn t ht))
          (mul_nonneg (by linarith) (hβ_nn t ht))
      have hγ_sum : ∑ t ∈ T, γ t = 1 := by
        dsimp only [γ]
        rw [Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.mul_sum, hα_sum, hβ_sum]
        ring
      have hγ_eq : ∑ t ∈ T, γ t • t = t0 := by
        dsimp only [γ]
        simp_rw [add_smul, mul_smul]
        rw [Finset.sum_add_distrib, ← Finset.smul_sum, ← Finset.smul_sum, hα_eq, hβ_eq]
        exact ht0_eq.symm
      have hα_le : α t0 ≤ 1 := by
        have hsp := Finset.add_sum_erase T α ht0
        have hr : 0 ≤ ∑ t ∈ T.erase t0, α t :=
          Finset.sum_nonneg (fun t ht => hα_nn t (Finset.mem_of_mem_erase ht))
        linarith
      have hβ_le : β t0 ≤ 1 := by
        have hsp := Finset.add_sum_erase T β ht0
        have hr : 0 ≤ ∑ t ∈ T.erase t0, β t :=
          Finset.sum_nonneg (fun t ht => hβ_nn t (Finset.mem_of_mem_erase ht))
        linarith
      have hγ_lt : γ t0 < 1 := by
        have hle : γ t0 ≤ 1 := by dsimp only [γ]; nlinarith
        refine lt_of_le_of_ne hle (fun h1 => ?_)
        have hα1 : α t0 = 1 := by dsimp only [γ] at h1; nlinarith
        have hβ1 : β t0 = 1 := by dsimp only [γ] at h1; nlinarith
        have hx0 : x = t0 := hα_eq.symm.trans (sum_eq_self_of_weight_one T t0 ht0 α hα_nn hα_sum hα1)
        have hy0 : y = t0 := hβ_eq.symm.trans (sum_eq_self_of_weight_one T t0 ht0 β hβ_nn hβ_sum hβ1)
        exact hne ⟨hx0, hy0⟩
      have hden_pos : 0 < 1 - γ t0 := sub_pos.mpr hγ_lt
      have hrest_sum : ∑ t ∈ T.erase t0, γ t = 1 - γ t0 := by
        have hsp := Finset.add_sum_erase T γ ht0
        linarith
      have ht0_conv : InFinsetConv (T.erase t0) t0 := by
        refine ⟨fun t => γ t / (1 - γ t0), ?_, ?_, ?_⟩
        · intro t ht; exact div_nonneg (hγ_nn t (Finset.mem_of_mem_erase ht)) (le_of_lt hden_pos)
        · simp_rw [div_eq_mul_inv]
          rw [← Finset.sum_mul, hrest_sum, mul_inv_cancel₀ (ne_of_gt hden_pos)]
        · have hsp : γ t0 • t0 + ∑ t ∈ T.erase t0, γ t • t = t0 := by
            rw [Finset.add_sum_erase T (fun t => γ t • t) ht0]
            exact hγ_eq
          have hsub : ∑ t ∈ T.erase t0, γ t • t = (1 - γ t0) • t0 := by
            rw [sub_smul, one_smul]
            exact eq_sub_of_add_eq' hsp
          have hscale :
              ∑ t ∈ T.erase t0, (γ t / (1 - γ t0)) • t =
                (1 - γ t0)⁻¹ • ∑ t ∈ T.erase t0, γ t • t := by
            rw [Finset.smul_sum]
            apply Finset.sum_congr rfl
            intro t _
            rw [div_eq_inv_mul, mul_smul]
          rw [hscale, hsub, smul_smul, inv_mul_cancel₀ (ne_of_gt hden_pos), one_smul]
      have hcard' : (T.erase t0).card ≤ k := by
        have hlt : (T.erase t0).card < T.card := Finset.card_erase_lt_of_mem ht0
        omega
      exact ih (T.erase t0) hcard'
        (fun t ht => hT t (Finset.mem_of_mem_erase ht))
        (fun z hz => conv_erase_redundant T t0 ht0 ht0_conv (hgen z hz))

/-- **Theorem F4.4a:** The true extreme-point set `vert(Xi) = zonotopeVertices D` is finite
(every extreme point of `Xi = L(W^r)` is the image of a corner of `W^r`). -/
theorem zonotopeVertices_finite (D : Data) : (zonotopeVertices D).Finite := by
  have hsub : zonotopeVertices D ⊆ (cornerImages D : Set (Vec D.n)) := by
    intro v hv
    exact extreme_point_mem_generating_finset (zonotope_convex D) (cornerImages D)
      (fun t ht => by
        rcases Finset.mem_image.mp ht with ⟨σ, _, rfl⟩
        exact ⟨cornerNoise D σ, rfl⟩)
      (zonotope_in_conv_cornerImages D) hv
  exact (cornerImages D).finite_toSet.subset hsub

/-- True Vertex-LP indexed strictly by the distinct extreme points `vert(Xi) = zonotopeVertices D`. -/
def ExtremeVertexLPBound (D : Data) (a : D.ControlBlock D.r)
    (uExt : zonotopeVertices D → D.ControlBlock D.q) (eta : ℝ) : Prop :=
  ∀ v : zonotopeVertices D, TightenedAt D a v.val (uExt v) eta

/-- Epigraph level set of the true `vert(Xi)`-indexed Vertex-LP. -/
def extremeVertexLPLevels (D : Data) : Set ℝ :=
  {eta | ∃ a : D.ControlBlock D.r,
    ∃ uExt : zonotopeVertices D → D.ControlBlock D.q,
      ExtremeVertexLPBound D a uExt eta}

/-- **Theorem F4.4b:** Any feasible true-vertex LP solution `uExt` over `vert(Xi)` lifts to a
feasible corner-indexed LP solution and hence yields an explicit Borel-measurable
`y : D.DeviationPolicy` achieving `D.TightenedAROBound a y eta` and `D.AROBound a y eta`. -/
theorem extreme_vertex_lp_to_aro (D : Data) (a : D.ControlBlock D.r)
    (uExt : zonotopeVertices D → D.ControlBlock D.q) (eta : ℝ)
    (hext : ExtremeVertexLPBound D a uExt eta) :
    ∃ y : D.DeviationPolicy, D.TightenedAROBound a y eta ∧ D.AROBound a y eta := by
  classical
  have hT_sub : ∀ t ∈ cornerImages D, t ∈ D.Z := by
    intro t ht
    rcases Finset.mem_image.mp ht with ⟨σ, _, rfl⟩
    exact ⟨cornerNoise D σ, rfl⟩
  obtain ⟨E, hE_ext, hE_gen⟩ := finset_conv_reduces_to_extreme_aux
    (cornerImages D).card (cornerImages D) le_rfl hT_sub (zonotope_in_conv_cornerImages D)
  have hcorner_lift : ∀ σ : Corner D,
      ∃ b : D.ControlBlock D.q, TightenedAt D a (D.deviation (cornerNoise D σ)) b eta := by
    intro σ
    have hξZ : D.deviation (cornerNoise D σ) ∈ D.Z := ⟨cornerNoise D σ, rfl⟩
    obtain ⟨μ, hμ_nn, hμ_sum, hμ_eq⟩ := hE_gen _ hξZ
    let uAt : Vec D.n → D.ControlBlock D.q := fun v =>
      if hv : v ∈ zonotopeVertices D then uExt ⟨v, hv⟩ else
        ⟨fun _ => D.umin, fun _ j => ⟨le_rfl, D.control_nonempty j⟩⟩
    let b : D.ControlBlock D.q :=
      ⟨fun t j => ∑ v ∈ E, μ v * (uAt v).val t j, by
        intro t j
        constructor
        · calc D.umin j = (∑ v ∈ E, μ v) * D.umin j := by rw [hμ_sum, one_mul]
            _ = ∑ v ∈ E, μ v * D.umin j := Finset.sum_mul ..
            _ ≤ ∑ v ∈ E, μ v * (uAt v).val t j :=
                Finset.sum_le_sum (fun v hv =>
                  mul_le_mul_of_nonneg_left ((uAt v).property t j).1 (hμ_nn v hv))
        · calc ∑ v ∈ E, μ v * (uAt v).val t j
              ≤ ∑ v ∈ E, μ v * D.umax j :=
                Finset.sum_le_sum (fun v hv =>
                  mul_le_mul_of_nonneg_left ((uAt v).property t j).2 (hμ_nn v hv))
            _ = (∑ v ∈ E, μ v) * D.umax j := (Finset.sum_mul ..).symm
            _ = D.umax j := by rw [hμ_sum, one_mul]⟩
    refine ⟨b, ?_⟩
    have hz_eq : D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σ)) b.val 0 =
        ∑ v : E, μ v.val • D.expansion D.q (D.nominal a + v.val) (uAt v.val).val 0 := by
      have hnom : D.nominal a = ∑ v ∈ E, μ v • D.nominal a := by
        rw [← Finset.sum_smul, hμ_sum, one_smul]
      have hctrl : ∀ t : Fin D.q, b.val t = ∑ v ∈ E, μ v • (uAt v).val t := by
        intro t; ext j
        simp [b, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
      simp only [Data.expansion, Pi.zero_apply, map_zero, add_zero]
      conv_lhs => rw [hnom, ← hμ_eq]
      simp only [← Finset.sum_add_distrib, ← smul_add, map_sum, map_smul, hctrl]
      rw [Finset.sum_comm, ← Finset.sum_add_distrib]
      have hfin : ∑ v ∈ E, (μ v • (D.A ^ D.q) (D.nominal a + v) +
          ∑ t : Fin D.q, μ v • (D.A ^ (D.q - 1 - t.val)) (D.B ((uAt v).val t))) =
          ∑ v ∈ E, μ v • ((D.A ^ D.q) (D.nominal a + v) +
          ∑ t : Fin D.q, (D.A ^ (D.q - 1 - t.val)) (D.B ((uAt v).val t))) := by
        apply Finset.sum_congr rfl
        intro v _
        rw [smul_add, Finset.smul_sum]
      rw [hfin, ← Finset.sum_coe_sort E]
    have hμ_nn' : ∀ v : E, 0 ≤ μ v.val := fun v => hμ_nn v.val v.property
    have hμ_sum' : ∑ v : E, μ v.val = 1 := by
      rw [Finset.sum_coe_sort E μ]; exact hμ_sum
    have ht_v : ∀ v : E, TightenedAt D a v.val (uAt v.val) eta := by
      intro v
      have hv_ext : v.val ∈ zonotopeVertices D := hE_ext v.val v.property
      simp only [uAt, hv_ext, ↓reduceDIte]
      exact hext ⟨v.val, hv_ext⟩
    change (∀ i : Fin D.rows, _) ∧ _
    rw [hz_eq]
    constructor
    · intro i
      constructor
      · exact linear_ineq_convex_comb (fun v : E => μ v.val) hμ_nn' hμ_sum'
          (-(D.terminalRow i)) _ _ _ (fun v => ((ht_v v).1 i).1)
      · exact linear_ineq_convex_comb (fun v : E => μ v.val) hμ_nn' hμ_sum'
          (D.terminalRow i) _ _ _ (fun v => ((ht_v v).1 i).2)
    · exact linear_ineq_convex_comb (fun v : E => μ v.val) hμ_nn' hμ_sum'
        D.c _ _ _ (fun v => (ht_v v).2)
  choose uVert huVert using hcorner_lift
  exact vertex_lp_to_aro D a uVert eta huVert

/-- **Theorem F4.4c:** Exact epigraph equality between true `vert(Xi)`-indexed Vertex-LP and ARO. -/
theorem extreme_vertex_lp_epigraph_eq_aro (D : Data) :
    extremeVertexLPLevels D = D.aroLevels := by
  apply Set.ext
  intro eta
  constructor
  · rintro ⟨a, uExt, hext⟩
    obtain ⟨y, _, haro⟩ := extreme_vertex_lp_to_aro D a uExt eta hext
    exact ⟨a, y, haro⟩
  · rintro ⟨a, y, haro⟩
    have htight := (BridgeFormalV3.Proofs.exact_tightening D a y eta).mp haro
    refine ⟨a, fun v => y.rule ⟨v.val, v.property.1⟩, ?_⟩
    intro v
    exact htight ⟨v.val, v.property.1⟩

/-- **Theorem F4.4d:** Exact epigraph equality between true `vert(Xi)`-indexed Vertex-LP and OGU. -/
theorem extreme_vertex_lp_epigraph_eq_source (D : Data) :
    extremeVertexLPLevels D = D.sourceLevels := by
  rw [extreme_vertex_lp_epigraph_eq_aro D, BridgeFormalV2.Proofs.epigraph_equality D]

/-- **Theorem F4.4e:** Equivalence between true `vert(Xi)`-indexed LP and `2^(r*p)` corner LP. -/
theorem extreme_vertex_lp_eq_corner_lp (D : Data) :
    extremeVertexLPLevels D = vertexLPLevels D := by
  rw [extreme_vertex_lp_epigraph_eq_aro D, vertex_lp_epigraph_eq_aro D]

end AroProofs.BridgeF4VertexLP
