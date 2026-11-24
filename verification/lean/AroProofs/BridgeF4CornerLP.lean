import BridgeFormalV3.Proofs.Support

/-!
# F4: Finite Vertex-LP Reduction & Explicit Borel-Measurable Selector over Zonotope `Xi = L(W^r)`

Live Scientific Discovery Run-01 (`conj-f4-vertex-lp-selector`) built strictly over the frozen
core `BridgeFormalV2.Model` / `BridgeFormalV2.Goals` and F3 `BridgeFormalV3.Proofs.Support`.

Main theorems (zero `sorry`, zero custom axioms, zero injectivity assumption on `D.deviation`):
  1. `borel_right_inverse_exists`: For EVERY `D : BridgeFormalV2.Data`, constructs an explicit
     Borel-measurable right-inverse `s : D.Z → D.NoiseBlock D.r` (`D.deviation (s xi) = xi.val`)
     by finite lexicographic infimum induction over the compact hypercube `W^r = [-rho, rho]^{r*p}`.
  2. `vertex_lp_to_tightened_aro`: Any finite Vertex-LP solution `uVert : Corner D → D.ControlBlock D.q`
     yields an explicit Borel-measurable `y : D.DeviationPolicy` via multilinear hypercube
     convex interpolation composed with the Borel right-inverse, satisfying `D.TightenedAROBound a y eta`
     and `D.AROBound a y eta`.
  3. `vertex_lp_epigraph_eq_aro` & `vertex_lp_epigraph_eq_source`: Exact epigraph level-set equality
     `vertexLPLevels D = D.aroLevels` and `vertexLPLevels D = D.sourceLevels` for EVERY `D : Data`.
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 MeasureTheory Set

namespace AroProofs.BridgeF4VertexLP

/-! ## Section 1: Elementary Borel measurability from `Iic` preimages (zero extra imports) -/

private theorem measurable_of_Iic_real {α : Type*} [MeasurableSpace α] {f : α → ℝ}
    (hf : ∀ t : ℝ, MeasurableSet (f ⁻¹' Set.Iic t)) : Measurable f := by
  classical
  apply measurable_of_isOpen
  intro U hU
  have hIoi : ∀ a : ℝ, MeasurableSet (f ⁻¹' Set.Ioi a) := by
    intro a
    have hcomp : Set.Ioi a = (Set.Iic a)ᶜ := by
      ext x; simp
    rw [hcomp, Set.preimage_compl]
    exact (hf a).compl
  have hIio : ∀ b : ℝ, MeasurableSet (f ⁻¹' Set.Iio b) := by
    intro b
    have hunion : Set.Iio b = ⋃ n : ℕ, Set.Iic (b - 1 / ((n : ℝ) + 1)) := by
      ext x
      simp only [Set.mem_Iio, Set.mem_iUnion, Set.mem_Iic]
      constructor
      · intro hxb
        obtain ⟨n, hn⟩ := exists_nat_one_div_lt (sub_pos.mpr hxb)
        refine ⟨n, ?_⟩
        linarith
      · rintro ⟨n, hxn⟩
        have hpos : (0 : ℝ) < 1 / ((n : ℝ) + 1) := by positivity
        linarith
    rw [hunion, Set.preimage_iUnion]
    exact MeasurableSet.iUnion (fun n => hf (b - 1 / ((n : ℝ) + 1)))
  have hIoo : ∀ a b : ℝ, MeasurableSet (f ⁻¹' Set.Ioo a b) := by
    intro a b
    have hinter : Set.Ioo a b = Set.Ioi a ∩ Set.Iio b := by
      ext x; simp
    rw [hinter, Set.preimage_inter]
    exact (hIoi a).inter (hIio b)
  have hU_eq :
      U = ⋃ (q : ℚ × ℚ), if Set.Ioo (q.1 : ℝ) (q.2 : ℝ) ⊆ U
        then Set.Ioo (q.1 : ℝ) (q.2 : ℝ) else ∅ := by
    ext x
    constructor
    · intro hxU
      rw [Metric.isOpen_iff] at hU
      obtain ⟨ε, hε, hball⟩ := hU x hxU
      obtain ⟨q1, hq1_lo, hq1_hi⟩ := exists_rat_btwn (show x - ε < x by linarith)
      obtain ⟨q2, hq2_lo, hq2_hi⟩ := exists_rat_btwn (show x < x + ε by linarith)
      refine Set.mem_iUnion.mpr ⟨(q1, q2), ?_⟩
      have hsub : Set.Ioo (q1 : ℝ) (q2 : ℝ) ⊆ U := by
        intro y hy
        apply hball
        rw [Metric.mem_ball, Real.dist_eq, abs_lt]
        constructor <;> linarith [hy.1, hy.2]
      simp only [hsub, ↓reduceIte]
      exact ⟨hq1_hi, hq2_lo⟩
    · intro hx
      rcases Set.mem_iUnion.mp hx with ⟨q, hq⟩
      split_ifs at hq with hsub
      · exact hsub hq
      · exact False.elim hq
  rw [hU_eq, Set.preimage_iUnion]
  refine MeasurableSet.iUnion (fun q => ?_)
  split_ifs
  · exact hIoo (q.1 : ℝ) (q.2 : ℝ)
  · simp

/-! ## Section 2: Multilinear barycentric decomposition of the hypercube `[-rho, rho]^N` -/

def cornerCoord (ρ : ℝ) (b : Bool) : ℝ :=
  if b then ρ else -ρ

def coordWeight (ρ : ℝ) (b : Bool) (x : ℝ) : ℝ :=
  if b then (ρ + x) / (2 * ρ) else (ρ - x) / (2 * ρ)

def baryWeight {N : ℕ} (ρ : ℝ) (σ : Fin N → Bool) (w : Fin N → ℝ) : ℝ :=
  ∏ i : Fin N, coordWeight ρ (σ i) (w i)

private theorem coordWeight_nonneg {ρ x : ℝ} (hρ : 0 < ρ) (hx : -ρ ≤ x ∧ x ≤ ρ) (b : Bool) :
    0 ≤ coordWeight ρ b x := by
  cases b <;> simp only [coordWeight, Bool.false_eq_true, ↓reduceIte]
  · exact div_nonneg (by linarith) (by linarith)
  · exact div_nonneg (by linarith) (by linarith)

private theorem coordWeight_sum {ρ x : ℝ} (hρ : 0 < ρ) :
    coordWeight ρ true x + coordWeight ρ false x = 1 := by
  simp only [coordWeight, ↓reduceIte, Bool.false_eq_true]
  have h2ρ : (2 : ℝ) * ρ ≠ 0 := by linarith
  field_simp [h2ρ]
  ring

private theorem coordWeight_reconstruct {ρ x : ℝ} (hρ : 0 < ρ) :
    coordWeight ρ true x * cornerCoord ρ true +
      coordWeight ρ false x * cornerCoord ρ false = x := by
  simp only [coordWeight, cornerCoord, ↓reduceIte, Bool.false_eq_true]
  have h2ρ : (2 : ℝ) * ρ ≠ 0 := by linarith
  field_simp [h2ρ]
  ring

theorem baryWeight_nonneg {N : ℕ} {ρ : ℝ} (hρ : 0 < ρ)
    (σ : Fin N → Bool) (w : Fin N → ℝ) (hw : ∀ i, -ρ ≤ w i ∧ w i ≤ ρ) :
    0 ≤ baryWeight ρ σ w := by
  unfold baryWeight
  exact Finset.prod_nonneg (fun i _ => coordWeight_nonneg hρ (hw i) (σ i))

private def splitBoolEquiv (N : ℕ) : (Fin (N + 1) → Bool) ≃ Bool × (Fin N → Bool) where
  toFun σ := (σ 0, fun i => σ i.succ)
  invFun p := Fin.cons p.1 p.2
  left_inv σ := by
    funext i
    refine Fin.cases ?_ ?_ i <;> simp
  right_inv p := by
    rcases p with ⟨b, τ⟩
    ext <;> simp

theorem sum_baryWeight {N : ℕ} {ρ : ℝ} (hρ : 0 < ρ) (w : Fin N → ℝ) :
    ∑ σ : Fin N → Bool, baryWeight ρ σ w = 1 := by
  induction N with
  | zero =>
    simp [baryWeight]
  | succ N ih =>
    rw [← Equiv.sum_comp (splitBoolEquiv N).symm]
    rw [Fintype.sum_prod_type]
    have hterm : ∀ (b : Bool) (τ : Fin N → Bool),
        baryWeight ρ ((splitBoolEquiv N).symm (b, τ)) w =
          coordWeight ρ b (w 0) * baryWeight ρ τ (fun i => w i.succ) := by
      intro b τ
      simp only [baryWeight, splitBoolEquiv, Equiv.coe_fn_symm_mk, Fin.prod_univ_succ,
        Fin.cons_zero, Fin.cons_succ]
    simp_rw [hterm, ← Finset.mul_sum, ih (fun i => w i.succ), mul_one]
    simp only [Fintype.sum_bool]
    exact coordWeight_sum hρ

theorem sum_baryWeight_mul_corner {N : ℕ} {ρ : ℝ} (hρ : 0 < ρ)
    (w : Fin N → ℝ) (k : Fin N) :
    ∑ σ : Fin N → Bool, baryWeight ρ σ w * cornerCoord ρ (σ k) = w k := by
  induction N with
  | zero => exact Fin.elim0 k
  | succ N ih =>
    rw [← Equiv.sum_comp (splitBoolEquiv N).symm]
    rw [Fintype.sum_prod_type]
    refine Fin.cases ?_ ?_ k
    · have hterm : ∀ (b : Bool) (τ : Fin N → Bool),
          baryWeight ρ ((splitBoolEquiv N).symm (b, τ)) w *
            cornerCoord ρ (((splitBoolEquiv N).symm (b, τ)) 0) =
            (coordWeight ρ b (w 0) * cornerCoord ρ b) *
              baryWeight ρ τ (fun i => w i.succ) := by
        intro b τ
        simp only [baryWeight, splitBoolEquiv, Equiv.coe_fn_symm_mk, Fin.prod_univ_succ,
          Fin.cons_zero, Fin.cons_succ]
        ring
      simp_rw [hterm, ← Finset.mul_sum, sum_baryWeight hρ (fun i => w i.succ), mul_one]
      simp only [Fintype.sum_bool]
      exact coordWeight_reconstruct hρ
    · intro k'
      have hterm : ∀ (b : Bool) (τ : Fin N → Bool),
          baryWeight ρ ((splitBoolEquiv N).symm (b, τ)) w *
            cornerCoord ρ (((splitBoolEquiv N).symm (b, τ)) k'.succ) =
            coordWeight ρ b (w 0) *
              (baryWeight ρ τ (fun i => w i.succ) * cornerCoord ρ (τ k')) := by
        intro b τ
        simp only [baryWeight, splitBoolEquiv, Equiv.coe_fn_symm_mk, Fin.prod_univ_succ,
          Fin.cons_zero, Fin.cons_succ]
        ring
      simp_rw [hterm, ← Finset.mul_sum, ih (fun i => w i.succ) k']
      rw [← Finset.sum_mul]
      simp only [Fintype.sum_bool, coordWeight_sum hρ, one_mul]

theorem baryWeight_continuous {N : ℕ} (ρ : ℝ) (σ : Fin N → Bool) :
    Continuous (fun w : Fin N → ℝ => baryWeight ρ σ w) := by
  unfold baryWeight
  refine continuous_finsetProd _ (fun i _ => ?_)
  have hi : Continuous (fun w : Fin N → ℝ => w i) := continuous_apply i
  cases h : σ i <;> simp only [coordWeight, Bool.false_eq_true, ↓reduceIte]
  · exact (continuous_const.sub hi).div_const (2 * ρ)
  · exact (continuous_const.add hi).div_const (2 * ρ)

/-! ## Section 3: Lexicographic Borel-measurable right-inverse selector on compact box `[-rho, rho]^N` -/

private def boxSet (N : ℕ) (ρ : ℝ) : Set (Fin N → ℝ) :=
  {w | ∀ i : Fin N, -ρ ≤ w i ∧ w i ≤ ρ}

private theorem isCompact_boxSet (N : ℕ) (ρ : ℝ) : IsCompact (boxSet N ρ) := by
  have h : boxSet N ρ = {w : Fin N → ℝ | ∀ i, w i ∈ Set.Icc (-ρ) ρ} := by
    ext w; simp [boxSet, Set.mem_Icc]
  rw [h]
  exact isCompact_pi_infinite (fun _ => isCompact_Icc)

private theorem lex_borel_prefix_selector {Y : Type*} [TopologicalSpace Y] [T2Space Y]
    [MeasurableSpace Y] [OpensMeasurableSpace Y]
    (N : ℕ) (ρ : ℝ) (L : (Fin N → ℝ) → Y) (hL : Continuous L)
    (Z : Set Y) (hZ : Z = L '' boxSet N ρ) :
    ∀ k : ℕ, (hk : k ≤ N) →
      ∃ f : Z → (Fin k → ℝ),
        Measurable f ∧
        ∀ y : Z, ∃ w ∈ boxSet N ρ, L w = y.val ∧
          ∀ j : Fin k, w ⟨j.val, Nat.lt_of_lt_of_le j.isLt hk⟩ = f y j := by
  intro k
  induction k with
  | zero =>
    intro _
    refine ⟨fun _ => Fin.elim0, measurable_const, ?_⟩
    intro y
    have hy : y.val ∈ L '' boxSet N ρ := hZ ▸ y.property
    rcases hy with ⟨w, hw, hLw⟩
    exact ⟨w, hw, hLw, fun j => Fin.elim0 j⟩
  | succ k ih =>
    intro hk
    obtain ⟨fprev, hfprev_meas, hfprev_wit⟩ := ih (Nat.le_of_succ_le hk)
    let S : Z → Set (Fin N → ℝ) := fun y =>
      {w ∈ boxSet N ρ | L w = y.val ∧
        ∀ j : Fin k, w ⟨j.val, Nat.lt_of_lt_of_le j.isLt (Nat.le_of_succ_le hk)⟩ = fprev y j}
    have hS_compact : ∀ y : Z, IsCompact (S y) := by
      intro y
      have hS_eq : S y = boxSet N ρ ∩
          ({w | L w = y.val} ∩
            ⋂ j : Fin k, {w : Fin N → ℝ |
              w ⟨j.val, Nat.lt_of_lt_of_le j.isLt (Nat.le_of_succ_le hk)⟩ = fprev y j}) := by
        ext w; simp [S]; tauto
      rw [hS_eq]
      refine (isCompact_boxSet N ρ).inter_right ?_
      refine (isClosed_eq hL continuous_const).inter ?_
      exact isClosed_iInter (fun j => isClosed_eq (continuous_apply _) continuous_const)
    have hS_nonempty : ∀ y : Z, (S y).Nonempty := by
      intro y
      rcases hfprev_wit y with ⟨w, hw, hLw, hfj⟩
      exact ⟨w, hw, hLw, hfj⟩
    let coordK : (Fin N → ℝ) → ℝ := fun w => w ⟨k, hk⟩
    let fk : Z → ℝ := fun y => sInf (coordK '' S y)
    have hfk_attained : ∀ y : Z, ∃ w ∈ S y, coordK w = fk y := by
      intro y
      have hc : IsCompact (coordK '' S y) := (hS_compact y).image (continuous_apply _)
      have hne : (coordK '' S y).Nonempty := (hS_nonempty y).image coordK
      exact hc.sInf_mem hne
    have hfk_meas : Measurable fk := by
      apply measurable_of_Iic_real
      intro t
      let Φ : (Fin N → ℝ) → Y × (Fin k → ℝ) :=
        fun w => (L w, fun j : Fin k => w ⟨j.val, Nat.lt_of_lt_of_le j.isLt (Nat.le_of_succ_le hk)⟩)
      have hΦ_cont : Continuous Φ :=
        hL.prodMk (continuous_pi (fun _ => continuous_apply _))
      let K_t : Set (Fin N → ℝ) := boxSet N ρ ∩ {w | coordK w ≤ t}
      have hKt_compact : IsCompact K_t :=
        (isCompact_boxSet N ρ).inter_right (isClosed_le (continuous_apply _) continuous_const)
      have hImg_meas : MeasurableSet (Φ '' K_t) :=
        (hKt_compact.image hΦ_cont).isClosed.measurableSet
      let g : Z → Y × (Fin k → ℝ) := fun y => (y.val, fprev y)
      have hg_meas : Measurable g := measurable_subtype_coe.prodMk hfprev_meas
      have hpre : fk ⁻¹' Set.Iic t = g ⁻¹' (Φ '' K_t) := by
        ext y
        simp only [Set.mem_preimage, Set.mem_Iic, Set.mem_image]
        constructor
        · intro hle
          obtain ⟨w, hwS, hwk⟩ := hfk_attained y
          refine ⟨w, ⟨hwS.1, ?_⟩, ?_⟩
          · change coordK w ≤ t
            linarith
          · apply Prod.ext
            · exact hwS.2.1
            · funext j
              exact hwS.2.2 j
        · rintro ⟨w, ⟨hwbox, hwt⟩, hΦw⟩
          have hLw : L w = y.val := congrArg Prod.fst hΦw
          have hfj : ∀ j : Fin k,
              w ⟨j.val, Nat.lt_of_lt_of_le j.isLt (Nat.le_of_succ_le hk)⟩ = fprev y j := by
            intro j
            exact congrFun (congrArg Prod.snd hΦw) j
          have hwS : w ∈ S y := ⟨hwbox, hLw, hfj⟩
          have hbdd : BddBelow (coordK '' S y) :=
            ((hS_compact y).image (continuous_apply _)).bddBelow
          have hle : fk y ≤ coordK w := csInf_le hbdd ⟨w, hwS, rfl⟩
          exact le_trans hle hwt
      rw [hpre]
      exact hImg_meas.preimage hg_meas
    let fnext : Z → (Fin (k + 1) → ℝ) := fun y j =>
      if h : j.val < k then fprev y ⟨j.val, h⟩ else fk y
    have hfnext_meas : Measurable fnext := by
      rw [measurable_pi_iff]
      intro j
      dsimp only [fnext]
      split_ifs with h
      · exact (measurable_pi_apply ⟨j.val, h⟩).comp hfprev_meas
      · exact hfk_meas
    refine ⟨fnext, hfnext_meas, ?_⟩
    intro y
    obtain ⟨w, hwS, hwk⟩ := hfk_attained y
    refine ⟨w, hwS.1, hwS.2.1, ?_⟩
    intro j
    dsimp only [fnext]
    split_ifs with h
    · exact hwS.2.2 ⟨j.val, h⟩
    · have hjk : j.val = k := by omega
      have hfin : (⟨j.val, Nat.lt_of_lt_of_le j.isLt hk⟩ : Fin N) = ⟨k, hk⟩ :=
        Fin.ext hjk
      rw [hfin]
      exact hwk

/-! ## Section 4: Connecting `BridgeFormalV2.Data` to the Finite Vertex-LP & Borel Selector -/

/-- Index set of the `2^(r*p)` extreme corners of the prefix noise hypercube `W^r`. -/
abbrev Corner (D : Data) := Fin (D.r * D.p) → Bool

/-- Flat-coordinate equivalence `Fin (r * p) ≃ Fin r × Fin p`. -/
def flatToBlock {r p : ℕ} (v : Fin (r * p) → ℝ) : Block r p :=
  fun t i => v (finProdFinEquiv (t, i))

def blockToFlat {r p : ℕ} (w : Block r p) : Fin (r * p) → ℝ :=
  fun k => let ti := finProdFinEquiv.symm k; w ti.1 ti.2

private theorem flatToBlock_blockToFlat {r p : ℕ} (w : Block r p) :
    flatToBlock (blockToFlat w) = w := by
  funext t i
  simp [flatToBlock, blockToFlat]

theorem blockToFlat_flatToBlock {r p : ℕ} (v : Fin (r * p) → ℝ) :
    blockToFlat (flatToBlock v) = v := by
  funext k
  change v (finProdFinEquiv (finProdFinEquiv.symm k)) = v k
  rw [Equiv.apply_symm_apply]

/-- The extreme noise block corresponding to corner `σ : Corner D`. -/
def cornerNoise (D : Data) (σ : Corner D) : D.NoiseBlock D.r :=
  ⟨flatToBlock (fun k => cornerCoord D.rho (σ k)), by
    intro t i
    dsimp only [flatToBlock, cornerCoord]
    split_ifs <;> constructor <;> linarith [D.rho_pos]⟩

/-- The `t, i` prefix disturbance column `A^(r - 1 - t) E e_i`. -/
def prefixNoiseColumn (D : Data) (t : Fin D.r) (i : Fin D.p) : Vec D.n :=
  (D.A ^ (D.r - 1 - t.val)) (D.E (BridgeFormalV3.basisVector i))

/-- Linear expansion of `D.deviation` in flat coordinates (used for linearity & continuity). -/
def flatDeviation (D : Data) (v : Fin (D.r * D.p) → ℝ) : Vec D.n :=
  ∑ t : Fin D.r, ∑ i : Fin D.p, v (finProdFinEquiv (t, i)) • prefixNoiseColumn D t i

theorem deviation_eq_flatDeviation (D : Data) (w : D.NoiseBlock D.r) :
    D.deviation w = flatDeviation D (blockToFlat w.val) := by
  have hz : blockAt (fun _ : Fin D.r => (0 : Vec D.m)) = (fun _ => 0) := by
    funext t; simp [blockAt]
  have hexp : D.deviation w = D.expansion D.r 0 (fun _ => 0) w.val := by
    simpa only [hz, Data.deviation] using
      BridgeFormalV2.Proofs.expansion D D.r (0 : Vec D.n) (fun _ => (0 : Vec D.m)) w.val
  rw [hexp]
  simp only [Data.expansion, map_zero, zero_add, flatDeviation]
  apply Finset.sum_congr rfl
  intro t _
  conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition (w.val t)]
  simp only [map_sum, map_smul, prefixNoiseColumn, blockToFlat, Equiv.symm_apply_apply]

theorem flatDeviation_continuous (D : Data) : Continuous (flatDeviation D) := by
  unfold flatDeviation
  refine continuous_finsetSum _ (fun t _ => continuous_finsetSum _ (fun i _ => ?_))
  exact (continuous_apply _).smul continuous_const

/-- **Theorem F4.1:** For EVERY `D : BridgeFormalV2.Data` (with NO injectivity assumption),
there exists a Borel-measurable right-inverse `s : D.Z → D.NoiseBlock D.r`. -/
theorem borel_right_inverse_exists (D : Data) :
    ∃ s : D.Z → D.NoiseBlock D.r,
      Measurable s ∧ ∀ xi : D.Z, D.deviation (s xi) = xi.val := by
  have hZ_eq : D.Z = flatDeviation D '' boxSet (D.r * D.p) D.rho := by
    ext x
    constructor
    · rintro ⟨w, rfl⟩
      refine ⟨blockToFlat w.val, ?_, (deviation_eq_flatDeviation D w).symm⟩
      intro k
      exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
    · rintro ⟨v, hvbox, rfl⟩
      let w : D.NoiseBlock D.r := ⟨flatToBlock v, fun t i => hvbox (finProdFinEquiv (t, i))⟩
      refine ⟨w, ?_⟩
      rw [deviation_eq_flatDeviation D w, blockToFlat_flatToBlock]
  obtain ⟨f, hf_meas, hf_wit⟩ := lex_borel_prefix_selector
    (D.r * D.p) D.rho (flatDeviation D) (flatDeviation_continuous D) D.Z hZ_eq
    (D.r * D.p) le_rfl
  have hf_eq : ∀ xi : D.Z, f xi ∈ boxSet (D.r * D.p) D.rho ∧ flatDeviation D (f xi) = xi.val := by
    intro xi
    obtain ⟨w, hwbox, hLw, hwf⟩ := hf_wit xi
    have hwf_eq : w = f xi := by
      funext j
      exact hwf j
    rw [← hwf_eq]
    exact ⟨hwbox, hLw⟩
  let s : D.Z → D.NoiseBlock D.r := fun xi =>
    ⟨flatToBlock (f xi), fun t i => (hf_eq xi).1 (finProdFinEquiv (t, i))⟩
  have hs_meas : Measurable s := by
    refine Measurable.subtype_mk ?_
    rw [measurable_pi_iff]
    intro t
    rw [measurable_pi_iff]
    intro i
    exact (measurable_pi_apply (finProdFinEquiv (t, i))).comp hf_meas
  refine ⟨s, hs_meas, ?_⟩
  intro xi
  rw [deviation_eq_flatDeviation D (s xi)]
  change flatDeviation D (blockToFlat (flatToBlock (f xi))) = xi.val
  rw [blockToFlat_flatToBlock]
  exact (hf_eq xi).2

/-! ## Section 5: Finite Vertex-LP Definition, Convex Interpolation & Epigraph Equality -/

/-- Tightened ARO terminal & cost inequalities at a single deviation `xi` and suffix block `b`. -/
def TightenedAt (D : Data) (a : D.ControlBlock D.r) (xi : Vec D.n)
    (b : D.ControlBlock D.q) (eta : ℝ) : Prop :=
  let z := D.expansion D.q (D.nominal a + xi) b.val 0
  (∀ i : Fin D.rows,
    (-(D.terminalRow i)) z + D.futureRowSupport (-(D.terminalRow i)) ≤ -D.gmin i ∧
    (D.terminalRow i) z + D.futureRowSupport (D.terminalRow i) ≤ D.gmax i) ∧
  D.c z + D.futureRowSupport D.c ≤ eta

/-- Finite Vertex-LP feasibility: `2^(r*p)` corner blocks satisfy `TightenedAt` at every corner. -/
def VertexLPBound (D : Data) (a : D.ControlBlock D.r)
    (uVert : Corner D → D.ControlBlock D.q) (eta : ℝ) : Prop :=
  ∀ σ : Corner D, TightenedAt D a (D.deviation (cornerNoise D σ)) (uVert σ) eta

/-- Epigraph level set of the finite Vertex-LP. -/
def vertexLPLevels (D : Data) : Set ℝ :=
  {eta | ∃ a : D.ControlBlock D.r, ∃ uVert : Corner D → D.ControlBlock D.q,
    VertexLPBound D a uVert eta}

/-- Continuous convex-interpolation control map over the `2^(r*p)` hypercube corners. -/
def interpControl (D : Data) (uVert : Corner D → D.ControlBlock D.q)
    (w : D.NoiseBlock D.r) : D.ControlBlock D.q :=
  ⟨fun t j => ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * (uVert σ).val t j, by
    intro t j
    have hw_flat : ∀ k, -D.rho ≤ blockToFlat w.val k ∧ blockToFlat w.val k ≤ D.rho := by
      intro k
      exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
    have hsum1 : ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) = 1 :=
      sum_baryWeight D.rho_pos (blockToFlat w.val)
    constructor
    · calc D.umin j = (∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val)) * D.umin j := by
            rw [hsum1, one_mul]
        _ = ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * D.umin j := Finset.sum_mul ..
        _ ≤ ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * (uVert σ).val t j := by
            refine Finset.sum_le_sum (fun σ _ => ?_)
            exact mul_le_mul_of_nonneg_left ((uVert σ).property t j).1
              (baryWeight_nonneg D.rho_pos σ _ hw_flat)
    · calc ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * (uVert σ).val t j
          ≤ ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * D.umax j := by
            refine Finset.sum_le_sum (fun σ _ => ?_)
            exact mul_le_mul_of_nonneg_left ((uVert σ).property t j).2
              (baryWeight_nonneg D.rho_pos σ _ hw_flat)
        _ = (∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val)) * D.umax j :=
            (Finset.sum_mul ..).symm
        _ = D.umax j := by rw [hsum1, one_mul]⟩

theorem interpControl_continuous (D : Data) (uVert : Corner D → D.ControlBlock D.q) :
    Continuous (interpControl D uVert) := by
  refine Continuous.subtype_mk ?_ _
  refine continuous_pi (fun t => continuous_pi (fun j => ?_))
  refine continuous_finsetSum _ (fun σ _ => ?_)
  have hflat : Continuous (fun w : D.NoiseBlock D.r => blockToFlat w.val) :=
    continuous_pi (fun k =>
      (continuous_apply (finProdFinEquiv.symm k).2).comp
        ((continuous_apply (finProdFinEquiv.symm k).1).comp continuous_subtype_val))
  exact ((baryWeight_continuous D.rho σ).comp hflat).mul continuous_const

theorem deviation_barycentric (D : Data) (w : D.NoiseBlock D.r) :
    ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) • D.deviation (cornerNoise D σ) =
      D.deviation w := by
  rw [deviation_eq_flatDeviation D w]
  have hcorner : ∀ σ : Corner D,
      D.deviation (cornerNoise D σ) =
        flatDeviation D (fun k => cornerCoord D.rho (σ k)) := by
    intro σ
    rw [deviation_eq_flatDeviation D (cornerNoise D σ)]
    congr 1
    exact blockToFlat_flatToBlock (fun k => cornerCoord D.rho (σ k))
  simp_rw [hcorner, flatDeviation, Finset.smul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro t _
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro i _
  simp_rw [smul_smul, ← Finset.sum_smul]
  congr 1
  exact sum_baryWeight_mul_corner D.rho_pos (blockToFlat w.val) (finProdFinEquiv (t, i))

private theorem expansion_barycentric (D : Data) (a : D.ControlBlock D.r)
    (uVert : Corner D → D.ControlBlock D.q) (w : D.NoiseBlock D.r) :
    D.expansion D.q (D.nominal a + D.deviation w) (interpControl D uVert w).val 0 =
      ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) •
        D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σ)) (uVert σ).val 0 := by
  have hsum1 : ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) = 1 :=
    sum_baryWeight D.rho_pos (blockToFlat w.val)
  have hnom : D.nominal a =
      ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) • D.nominal a := by
    rw [← Finset.sum_smul, hsum1, one_smul]
  have hdev : D.deviation w =
      ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) • D.deviation (cornerNoise D σ) :=
    (deviation_barycentric D w).symm
  have hctrl : ∀ t : Fin D.q, (interpControl D uVert w).val t =
      ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) • (uVert σ).val t := by
    intro t
    ext j
    simp [interpControl, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  simp only [Data.expansion, Pi.zero_apply, map_zero, add_zero]
  conv_lhs => rw [hnom, hdev]
  simp only [← Finset.sum_add_distrib, ← smul_add, map_sum, map_smul, hctrl]
  rw [Finset.sum_comm]
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro σ _
  rw [smul_add, Finset.smul_sum]

theorem linear_ineq_convex_comb {ι : Type*} [Fintype ι] {n : ℕ}
    (α : ι → ℝ) (hα : ∀ i, 0 ≤ α i) (hsum : ∑ i, α i = 1)
    (row : Vec n →ₗ[ℝ] ℝ) (z : ι → Vec n) (s bound : ℝ)
    (h : ∀ i, row (z i) + s ≤ bound) :
    row (∑ i, α i • z i) + s ≤ bound := by
  rw [map_sum]
  simp_rw [map_smul, smul_eq_mul]
  calc (∑ i, α i * row (z i)) + s
      = (∑ i, α i * row (z i)) + (∑ i, α i) * s := by rw [hsum, one_mul]
    _ = ∑ i, α i * (row (z i) + s) := by
        rw [Finset.sum_mul, ← Finset.sum_add_distrib]
        apply Finset.sum_congr rfl
        intro i _; ring
    _ ≤ ∑ i, α i * bound := by
        refine Finset.sum_le_sum (fun i _ => mul_le_mul_of_nonneg_left (h i) (hα i))
    _ = (∑ i, α i) * bound := (Finset.sum_mul ..).symm
    _ = bound := by rw [hsum, one_mul]

/-- **Theorem F4.2:** Every feasible finite Vertex-LP solution `uVert` produces an explicit
Borel-measurable `y : D.DeviationPolicy` satisfying both `D.TightenedAROBound a y eta` and
`D.AROBound a y eta` (zero injectivity assumption on `D.deviation`). -/
theorem vertex_lp_to_aro (D : Data) (a : D.ControlBlock D.r)
    (uVert : Corner D → D.ControlBlock D.q) (eta : ℝ)
    (hvert : VertexLPBound D a uVert eta) :
    ∃ y : D.DeviationPolicy, D.TightenedAROBound a y eta ∧ D.AROBound a y eta := by
  obtain ⟨s, hs_meas, hs_inv⟩ := borel_right_inverse_exists D
  let y : D.DeviationPolicy :=
    ⟨fun xi => interpControl D uVert (s xi),
      (interpControl_continuous D uVert).measurable.comp hs_meas⟩
  have htight : D.TightenedAROBound a y eta := by
    intro xi
    let w := s xi
    have hw_flat : ∀ k, -D.rho ≤ blockToFlat w.val k ∧ blockToFlat w.val k ≤ D.rho := by
      intro k
      exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
    have hα : ∀ σ : Corner D, 0 ≤ baryWeight D.rho σ (blockToFlat w.val) :=
      fun σ => baryWeight_nonneg D.rho_pos σ _ hw_flat
    have hsum1 : ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) = 1 :=
      sum_baryWeight D.rho_pos (blockToFlat w.val)
    have hz : D.aroNominalTerminal a y xi =
        ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) •
          D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σ)) (uVert σ).val 0 := by
      change D.expansion D.q (D.nominal a + xi.val) (interpControl D uVert w).val 0 = _
      rw [← hs_inv xi]
      exact expansion_barycentric D a uVert w
    rw [hz]
    constructor
    · intro i
      constructor
      · exact linear_ineq_convex_comb _ hα hsum1 (-(D.terminalRow i)) _ _ _
          (fun σ => ((hvert σ).1 i).1)
      · exact linear_ineq_convex_comb _ hα hsum1 (D.terminalRow i) _ _ _
          (fun σ => ((hvert σ).1 i).2)
    · exact linear_ineq_convex_comb _ hα hsum1 D.c _ _ _ (fun σ => (hvert σ).2)
  exact ⟨y, htight, (BridgeFormalV3.Proofs.exact_tightening D a y eta).mpr htight⟩

/-- **Theorem F4.3a:** Exact epigraph equality between finite Vertex-LP and two-stage ARO. -/
theorem vertex_lp_epigraph_eq_aro (D : Data) :
    vertexLPLevels D = D.aroLevels := by
  apply Set.ext
  intro eta
  constructor
  · rintro ⟨a, uVert, hvert⟩
    obtain ⟨y, _, haro⟩ := vertex_lp_to_aro D a uVert eta hvert
    exact ⟨a, y, haro⟩
  · rintro ⟨a, y, haro⟩
    have htight := (BridgeFormalV3.Proofs.exact_tightening D a y eta).mp haro
    refine ⟨a, fun σ => y.rule (D.observedDeviation (cornerNoise D σ)), ?_⟩
    intro σ
    exact htight (D.observedDeviation (cornerNoise D σ))

/-- **Theorem F4.3b:** Exact epigraph equality between finite corner-indexed LP and single-closure OGU. -/
theorem vertex_lp_epigraph_eq_source (D : Data) :
    vertexLPLevels D = D.sourceLevels := by
  rw [vertex_lp_epigraph_eq_aro D, BridgeFormalV2.Proofs.epigraph_equality D]


end AroProofs.BridgeF4VertexLP
