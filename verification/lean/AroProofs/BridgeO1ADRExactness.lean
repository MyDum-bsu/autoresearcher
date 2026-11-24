import BridgeFormalV3.Proofs.Support
import AroProofs.BridgeF4CornerLP

/-!
# O1 (Partial Coverage): ADR Exactness Mechanisms, Barycentric-Syzygy Obstruction,
and Exact 1D-vs-2D Dimension Dichotomy on Frozen `BridgeFormalV2.Data`

Live Scientific Discovery Run-01 (`conj-o1-adr-exactness-char`, partial) built strictly
over frozen `BridgeFormalV2.Model` / `BridgeFormalV2.Goals`, F3 `BridgeFormalV3.Proofs.Support`,
and F4 `BridgeF4CornerLP`.

Main theorems (zero `sorry`, zero custom axioms):
  A. General fixed-recourse 2-stage linear ARO (`FixedRecourseARO d m k`):
     1. `static_subset_adr_subset_aro`: `staticLevels P Ξ ⊆ adrLevels P Ξ ⊆ aroLevels P Ξ`.
     2. `adr_exact_on_simplex`: For every `d : ℕ` and every fixed-recourse `P`, ADR is exact on
        the standard `d`-simplex `Δ_d`: `adrLevels P Δ_d = aroLevels P Δ_d` (Mechanism M4 / T7).
     3. `barycentric_syzygy_adr_coupling`: Any two finite discrete probability distributions on `Ξ`
        sharing the same barycenter force identical barycentric averages under every affine rule.
     4. `chen_zhang_t3_adr_gap`: Concrete T3 cross-polytope witness (`d = 3`) proving
        `1 ∈ aroLevels` and `∀ eta ∈ adrLevels, 3 ≤ eta`.
  B. Frozen `BridgeFormalV2.Data` ADR dimension dichotomy:
     5. `bridge_adr_subset_aro_and_source`: Borel-measurable affine deviation policies satisfy
        `bridgeAdrLevels D ⊆ D.aroLevels` and `bridgeAdrLevels D ⊆ D.sourceLevels`.
     6. `bridge_adr_exact_1d`: For EVERY frozen `D : BridgeFormalV2.Data` with `D.n = 1`,
        `bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`.
     7. `exists_bridge_2d_strict_adr_gap`: Explicit `D.n = 2` witness (`A=I_2, B=(1,1)^T, E=I_2,
        H=I_2, c=(1,1)^T, g_min=(0,0), g_max=(4,4), u_max=1, rho=1`) proving `6 ∈ D.aroLevels`,
        `6 ∈ D.sourceLevels`, and `∀ eta ∈ bridgeAdrLevels D, 8 ≤ eta`.
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 AroProofs.BridgeF4VertexLP MeasureTheory Set

namespace AroProofs.BridgeO1ADRExactness

/-! ## Section 1: General fixed-recourse 2-stage linear ARO & simplex exactness -/

/-- General 2-stage fixed-recourse linear ARO with affine right-hand side `h_0 + H ξ`. -/
structure FixedRecourseARO (d m k : ℕ) where
  B : (Fin m → ℝ) →ₗ[ℝ] (Fin k → ℝ)
  h0 : Fin k → ℝ
  H : (Fin d → ℝ) →ₗ[ℝ] (Fin k → ℝ)
  c : (Fin m → ℝ) →ₗ[ℝ] ℝ

/-- Fully adaptive epigraph level set on an uncertainty set `Ξ`. -/
def aroLevels {d m k : ℕ} (P : FixedRecourseARO d m k) (Ξ : Set (Fin d → ℝ)) : Set ℝ :=
  {eta | ∀ ξ ∈ Ξ, ∃ y : Fin m → ℝ, (∀ i, P.B y i ≤ P.h0 i + P.H ξ i) ∧ P.c y ≤ eta}

/-- Affine decision rule (ADR) epigraph level set on `Ξ`. -/
def adrLevels {d m k : ℕ} (P : FixedRecourseARO d m k) (Ξ : Set (Fin d → ℝ)) : Set ℝ :=
  {eta | ∃ (y0 : Fin m → ℝ) (Y : (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ)),
    ∀ ξ ∈ Ξ, (∀ i, P.B (y0 + Y ξ) i ≤ P.h0 i + P.H ξ i) ∧ P.c (y0 + Y ξ) ≤ eta}

/-- Static (constant) decision rule epigraph level set on `Ξ`. -/
def staticLevels {d m k : ℕ} (P : FixedRecourseARO d m k) (Ξ : Set (Fin d → ℝ)) : Set ℝ :=
  {eta | ∃ y0 : Fin m → ℝ, ∀ ξ ∈ Ξ, (∀ i, P.B y0 i ≤ P.h0 i + P.H ξ i) ∧ P.c y0 ≤ eta}

/-- **Theorem O1.1:** Epigraph hierarchy `staticLevels ⊆ adrLevels ⊆ aroLevels` for any `P, Ξ`. -/
theorem static_subset_adr_subset_aro {d m k : ℕ} (P : FixedRecourseARO d m k)
    (Ξ : Set (Fin d → ℝ)) :
    staticLevels P Ξ ⊆ adrLevels P Ξ ∧ adrLevels P Ξ ⊆ aroLevels P Ξ := by
  constructor
  · intro eta hst
    rcases hst with ⟨y0, hy0⟩
    refine ⟨y0, 0, ?_⟩
    intro ξ hξ
    simpa only [LinearMap.zero_apply, add_zero] using hy0 ξ hξ
  · intro eta hadr
    rcases hadr with ⟨y0, Y, hY⟩
    intro ξ hξ
    exact ⟨y0 + Y ξ, hY ξ hξ⟩

/-- Standard `d`-simplex `Δ_d = {ξ ∈ ℝ^d | ∀ j, 0 ≤ ξ_j ∧ ∑ j, ξ_j ≤ 1}`. -/
def stdSimplex (d : ℕ) : Set (Fin d → ℝ) :=
  {ξ | (∀ j : Fin d, 0 ≤ ξ j) ∧ ∑ j : Fin d, ξ j ≤ 1}

private def simplexLinearMap {d m : ℕ} (y0 : Fin m → ℝ) (yj : Fin d → (Fin m → ℝ)) :
    (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun ξ := ∑ j : Fin d, ξ j • (yj j - y0)
  map_add' ξ₁ ξ₂ := by
    simp only [Pi.add_apply, add_smul, Finset.sum_add_distrib]
  map_smul' r ξ := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.smul_sum, mul_smul]

private theorem vec_eq_sum_single {d : ℕ} (ξ : Fin d → ℝ) :
    ξ = ∑ j : Fin d, ξ j • Pi.single j (1 : ℝ) := by
  funext i
  simp [Finset.sum_apply, Pi.smul_apply, Pi.single_apply]

/-- **Theorem O1.2 (Simplex ADR Exactness — Mechanism M4 / T7):**
For every dimension `d : ℕ` and every fixed-recourse problem `P`, ADR is exact on `Δ_d`. -/
theorem adr_exact_on_simplex {d m k : ℕ} (P : FixedRecourseARO d m k) :
    adrLevels P (stdSimplex d) = aroLevels P (stdSimplex d) := by
  apply Set.Subset.antisymm (static_subset_adr_subset_aro P (stdSimplex d)).2
  intro eta haro
  have h0_mem : (0 : Fin d → ℝ) ∈ stdSimplex d := by
    constructor
    · intro j; simp
    · simp
  obtain ⟨y0, hy0_feas, hy0_cost⟩ := haro 0 h0_mem
  have he_mem : ∀ j : Fin d, Pi.single j (1 : ℝ) ∈ stdSimplex d := by
    intro j
    constructor
    · intro l
      by_cases h : l = j
      · subst h; simp
      · simp [Pi.single_eq_of_ne h]
    · simp [Pi.single_apply]
  have hyj_ex : ∀ j : Fin d, ∃ y : Fin m → ℝ,
      (∀ i, P.B y i ≤ P.h0 i + P.H (Pi.single j (1 : ℝ)) i) ∧ P.c y ≤ eta :=
    fun j => haro (Pi.single j (1 : ℝ)) (he_mem j)
  choose yj hyj_feas hyj_cost using hyj_ex
  let Y := simplexLinearMap y0 yj
  refine ⟨y0, Y, ?_⟩
  intro ξ hξ
  rcases hξ with ⟨hξ_nonneg, hξ_sum⟩
  let w0 : ℝ := 1 - ∑ j : Fin d, ξ j
  have hw0_nonneg : 0 ≤ w0 := sub_nonneg.mpr hξ_sum
  have hw_total : w0 + ∑ j : Fin d, ξ j = 1 := by simp [w0]
  have hy_conv : y0 + Y ξ = w0 • y0 + ∑ j : Fin d, ξ j • yj j := by
    funext r
    simp only [Y, simplexLinearMap, LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply,
      Finset.sum_apply, Pi.smul_apply, Pi.sub_apply, smul_eq_mul, w0]
    have hsplit : ∑ j : Fin d, ξ j * (yj j r - y0 r) =
        (∑ j : Fin d, ξ j * yj j r) - (∑ j : Fin d, ξ j) * y0 r := by
      rw [Finset.sum_mul, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro j _; ring
    rw [hsplit]
    ring
  constructor
  · intro i
    have hB : P.B (y0 + Y ξ) i = w0 * P.B y0 i + ∑ j : Fin d, ξ j * P.B (yj j) i := by
      rw [hy_conv, map_add, map_smul, map_sum]
      simp [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
    have hH : P.H ξ i = ∑ j : Fin d, ξ j * P.H (Pi.single j (1 : ℝ)) i := by
      conv_lhs => rw [vec_eq_sum_single ξ]
      rw [map_sum]
      simp [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
    rw [hB]
    have h0_zero : P.H 0 i = 0 := by simp
    have h1 : w0 * P.B y0 i ≤ w0 * P.h0 i := by
      have hy0_i := hy0_feas i
      rw [h0_zero, add_zero] at hy0_i
      exact mul_le_mul_of_nonneg_left hy0_i hw0_nonneg
    have h2 : ∑ j : Fin d, ξ j * P.B (yj j) i ≤
        ∑ j : Fin d, ξ j * (P.h0 i + P.H (Pi.single j (1 : ℝ)) i) :=
      Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_left (hyj_feas j i) (hξ_nonneg j))
    calc w0 * P.B y0 i + ∑ j : Fin d, ξ j * P.B (yj j) i
        ≤ w0 * P.h0 i + ∑ j : Fin d, ξ j * (P.h0 i + P.H (Pi.single j (1 : ℝ)) i) :=
          add_le_add h1 h2
      _ = (w0 + ∑ j : Fin d, ξ j) * P.h0 i + ∑ j : Fin d, ξ j * P.H (Pi.single j (1 : ℝ)) i := by
          simp_rw [mul_add, Finset.sum_add_distrib, ← Finset.sum_mul]
          ring
      _ = P.h0 i + P.H ξ i := by rw [hw_total, one_mul, hH]
  · have hc : P.c (y0 + Y ξ) = w0 * P.c y0 + ∑ j : Fin d, ξ j * P.c (yj j) := by
      rw [hy_conv, map_add, map_smul, map_sum]
      simp [smul_eq_mul]
    rw [hc]
    calc w0 * P.c y0 + ∑ j : Fin d, ξ j * P.c (yj j)
        ≤ w0 * eta + ∑ j : Fin d, ξ j * eta :=
          add_le_add (mul_le_mul_of_nonneg_left hy0_cost hw0_nonneg)
            (Finset.sum_le_sum (fun j _ => mul_le_mul_of_nonneg_left (hyj_cost j) (hξ_nonneg j)))
      _ = (w0 + ∑ j : Fin d, ξ j) * eta := by rw [← Finset.sum_mul]; ring
      _ = eta := by rw [hw_total, one_mul]

/-! ## Section 2: Universal barycentric-syzygy obstruction & Chen-Zhang T3 separation -/

/-- **Theorem O1.3 (Universal Barycentric-Syzygy Obstruction Principle):**
Whenever two finite discrete probability distributions `(α, ξ)` and `(β, ζ)` share the same
barycenter `∑ a, α a • ξ a = ∑ b, β b • ζ b`, EVERY affine rule `x ↦ y0 + Y x` produces
identical barycentric averages `∑ a, α a • (y0 + Y (ξ a)) = ∑ b, β b • (y0 + Y (ζ b))`. -/
theorem barycentric_syzygy_adr_coupling {d m : ℕ} {ι₁ ι₂ : Type*} [Fintype ι₁] [Fintype ι₂]
    (α : ι₁ → ℝ) (β : ι₂ → ℝ) (hα : ∑ a, α a = 1) (hβ : ∑ b, β b = 1)
    (ξ : ι₁ → Fin d → ℝ) (ζ : ι₂ → Fin d → ℝ)
    (hbary : ∑ a, α a • ξ a = ∑ b, β b • ζ b)
    (y0 : Fin m → ℝ) (Y : (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ)) :
    ∑ a, α a • (y0 + Y (ξ a)) = ∑ b, β b • (y0 + Y (ζ b)) := by
  have lhs_eq : ∑ a, α a • (y0 + Y (ξ a)) = y0 + Y (∑ a, α a • ξ a) := by
    simp_rw [smul_add, Finset.sum_add_distrib, ← Finset.sum_smul, hα, one_smul]
    congr 1
    rw [map_sum]
    simp_rw [map_smul]
  have rhs_eq : ∑ b, β b • (y0 + Y (ζ b)) = y0 + Y (∑ b, β b • ζ b) := by
    simp_rw [smul_add, Finset.sum_add_distrib, ← Finset.sum_smul, hβ, one_smul]
    congr 1
    rw [map_sum]
    simp_rw [map_smul]
  rw [lhs_eq, rhs_eq, hbary]

/-- Chen-Zhang (2009) T3 instance (`N = 3`): `y_i ≥ ±ξ_i`, minimize `y_0 + y_1 + y_2`
over the `ℓ_1` cross-polytope `|ξ_0| + |ξ_1| + |ξ_2| ≤ 1`. -/
abbrev chenZhangT3 : FixedRecourseARO 3 3 6 where
  B :=
    { toFun := fun y idx => -y ⟨idx.val % 3, Nat.mod_lt _ (by omega)⟩
      map_add' := fun u v => by funext idx; simp; ring
      map_smul' := fun r u => by funext idx; simp }
  h0 := 0
  H :=
    { toFun := fun ξ idx =>
        if idx.val < 3 then -ξ ⟨idx.val % 3, Nat.mod_lt _ (by omega)⟩
        else ξ ⟨idx.val % 3, Nat.mod_lt _ (by omega)⟩
      map_add' := fun u v => by
        funext idx
        by_cases h : idx.val < 3
        · simp [h]; ring
        · simp [h]
      map_smul' := fun r u => by
        funext idx
        by_cases h : idx.val < 3 <;> simp [h] }
  c :=
    { toFun := fun y => y 0 + y 1 + y 2
      map_add' := fun u v => by simp; ring
      map_smul' := fun r u => by simp; ring }

/-- Unit `ℓ_1` cross-polytope in `ℝ^3`. -/
def l1CrossPolytope3 : Set (Fin 3 → ℝ) :=
  {ξ | |ξ 0| + |ξ 1| + |ξ 2| ≤ 1}

/-- **Theorem O1.4 (Chen-Zhang T3 Formal Separation):**
On the 3D `ℓ_1` cross-polytope, `1 ∈ aroLevels` (attained by `y_i(ξ) = |ξ_i|`),
whereas EVERY affine decision rule satisfies `3 ≤ eta` via the three origin-centered syzygies. -/
theorem chen_zhang_t3_adr_gap :
    (1 : ℝ) ∈ aroLevels chenZhangT3 l1CrossPolytope3 ∧
      ∀ eta ∈ adrLevels chenZhangT3 l1CrossPolytope3, (3 : ℝ) ≤ eta := by
  constructor
  · intro ξ hξ
    refine ⟨fun i => |ξ i|, ?_, ?_⟩
    · intro idx
      fin_cases idx <;> simp [neg_abs_le, le_abs_self]
    · exact hξ
  · intro eta hadr
    rcases hadr with ⟨y0, Y, hY⟩
    have h0_mem : (0 : Fin 3 → ℝ) ∈ l1CrossPolytope3 := by
      simp [l1CrossPolytope3]
    have hcost0 : y0 0 + y0 1 + y0 2 ≤ eta := by
      have h0 := (hY 0 h0_mem).2
      simpa [chenZhangT3] using h0
    have hy0_ge1 : ∀ i : Fin 3, (1 : ℝ) ≤ y0 i := by
      intro i
      let ep : Fin 3 → ℝ := Pi.single i (1 : ℝ)
      let em : Fin 3 → ℝ := -ep
      have hep_mem : ep ∈ l1CrossPolytope3 := by
        fin_cases i <;> simp [l1CrossPolytope3, ep]
      have hem_mem : em ∈ l1CrossPolytope3 := by
        fin_cases i <;> simp [l1CrossPolytope3, em, ep]
      have hsyz : ((1 / 2 : ℝ) • (y0 + Y ep) + (1 / 2 : ℝ) • (y0 + Y em)) i = y0 i := by
        have hsum := barycentric_syzygy_adr_coupling
          (α := fun _ : Fin 2 => (1 / 2 : ℝ))
          (β := fun _ : Fin 1 => (1 : ℝ))
          (by norm_num) (by simp)
          (ξ := ![ep, em]) (ζ := ![0])
          (by
            funext r
            simp [Fin.sum_univ_two, em])
          y0 Y
        have hpt := congrFun hsum i
        simpa [Fin.sum_univ_two, Fin.sum_univ_one] using hpt
      have hp_ineq : -(y0 i + Y ep i) ≤ -1 := by
        have h := (hY ep hep_mem).1 ⟨i.val, by omega⟩
        fin_cases i <;> simpa [chenZhangT3, ep] using h
      have hm_ineq : -(y0 i + Y em i) ≤ -1 := by
        have h := (hY em hem_mem).1 ⟨i.val + 3, by omega⟩
        fin_cases i <;> simpa [chenZhangT3, em, ep] using h
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul] at hsyz
      linarith
    linarith [hy0_ge1 0, hy0_ge1 1, hy0_ge1 2]

/-! ## Section 3: Affine decision rules on frozen `BridgeFormalV2.Data` & 1D exactness -/

/-- Borel-measurable affine state-deviation feedback policy `ξ ↦ b0 + K ξ` on frozen `Data`. -/
structure AffineDeviationPolicy (D : Data) where
  b0 : Fin D.q → Vec D.m
  K : Fin D.q → (Vec D.n →ₗ[ℝ] Vec D.m)
  in_box : ∀ (xi : D.Z) (t : Fin D.q) (j : Fin D.m),
    D.umin j ≤ (b0 t + K t xi.val) j ∧ (b0 t + K t xi.val) j ≤ D.umax j

private theorem linearMap_vec_continuous {n m : ℕ} (L : Vec n →ₗ[ℝ] Vec m) :
    Continuous L := by
  refine continuous_pi (fun j => ?_)
  have hformula : (fun v : Vec n => L v j) =
      fun v => ∑ i : Fin n, v i * L (Pi.single i (1 : ℝ)) j := by
    funext v
    conv_lhs => rw [vec_eq_sum_single v, map_sum]
    simp [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [hformula]
  exact continuous_finsetSum _ (fun i _ => (continuous_apply i).mul continuous_const)

/-- Every `AffineDeviationPolicy` is continuous, hence a valid Borel-measurable `D.DeviationPolicy`. -/
def AffineDeviationPolicy.toDeviationPolicy {D : Data} (P : AffineDeviationPolicy D) :
    D.DeviationPolicy where
  rule xi := ⟨fun t => P.b0 t + P.K t xi.val, P.in_box xi⟩
  borel := by
    have hcont : Continuous (fun xi : D.Z => (⟨fun t => P.b0 t + P.K t xi.val, P.in_box xi⟩ :
        D.ControlBlock D.q)) := by
      refine Continuous.subtype_mk ?_ _
      refine continuous_pi (fun t => ?_)
      exact continuous_const.add ((linearMap_vec_continuous (P.K t)).comp continuous_subtype_val)
    exact hcont.measurable

/-- Epigraph level set achievable by affine state-deviation policies on frozen `Data`. -/
def bridgeAdrLevels (D : Data) : Set ℝ :=
  {eta | ∃ (a : D.ControlBlock D.r) (P : AffineDeviationPolicy D),
    D.AROBound a P.toDeviationPolicy eta}

/-- **Theorem O1.5:** On every frozen `BridgeFormalV2.Data`, affine decision rules form a
Borel-measurable subclass of both two-stage ARO and single-closure OGU. -/
theorem bridge_adr_subset_aro_and_source (D : Data) :
    bridgeAdrLevels D ⊆ D.aroLevels ∧ bridgeAdrLevels D ⊆ D.sourceLevels := by
  have hsub : bridgeAdrLevels D ⊆ D.aroLevels := by
    intro eta ⟨a, P, hbound⟩
    exact ⟨a, P.toDeviationPolicy, hbound⟩
  refine ⟨hsub, ?_⟩
  rw [BridgeFormalV2.Proofs.epigraph_equality D]
  exact hsub

private theorem convex_comb_two_ineq {n : ℕ} (lam : ℝ) (h0 : 0 ≤ lam) (h1 : lam ≤ 1)
    (row : Vec n →ₗ[ℝ] ℝ) (zMin zMax : Vec n) (s bound : ℝ)
    (hmin : row zMin + s ≤ bound) (hmax : row zMax + s ≤ bound) :
    row ((1 - lam) • zMin + lam • zMax) + s ≤ bound := by
  rw [map_add, map_smul, map_smul, smul_eq_mul, smul_eq_mul]
  have h1m : 0 ≤ 1 - lam := sub_nonneg.mpr h1
  nlinarith

/-- **Theorem O1.6 (1D Bridge ADR Exactness):**
For EVERY frozen `D : BridgeFormalV2.Data` with `D.n = 1` (arbitrary horizons `r, q`,
dimensions `m, p, rows`, dynamics `A, B, E`, constraints `H, g_min, g_max`, cost `c`),
affine decision rules are ALWAYS exact: `bridgeAdrLevels D = D.aroLevels = D.sourceLevels`. -/
theorem bridge_adr_exact_1d (D : Data) (hn : D.n = 1) :
    bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels := by
  have hsub := (bridge_adr_subset_aro_and_source D).1
  have heq_aro : bridgeAdrLevels D = D.aroLevels := by
    apply Set.Subset.antisymm hsub
    intro eta haro
    rw [← vertex_lp_epigraph_eq_aro D] at haro
    rcases haro with ⟨a, uVert, hvert⟩
    let idx0 : Fin D.n := ⟨0, by omega⟩
    have hidx_unique : ∀ i : Fin D.n, i = idx0 := by
      intro i; ext; omega
    let valAt : Corner D → ℝ := fun σ => D.deviation (cornerNoise D σ) idx0
    have hne : (Finset.univ.image valAt).Nonempty :=
      ⟨valAt (fun _ => false), Finset.mem_image_of_mem _ (Finset.mem_univ _)⟩
    obtain ⟨σMin, _, hσMin_eq⟩ := Finset.mem_image.mp (Finset.min'_mem _ hne)
    obtain ⟨σMax, _, hσMax_eq⟩ := Finset.mem_image.mp (Finset.max'_mem _ hne)
    let ξMin : ℝ := valAt σMin
    let ξMax : ℝ := valAt σMax
    have hle_all : ∀ σ : Corner D, ξMin ≤ valAt σ ∧ valAt σ ≤ ξMax := by
      intro σ
      have hmem : valAt σ ∈ Finset.univ.image valAt :=
        Finset.mem_image_of_mem _ (Finset.mem_univ σ)
      exact ⟨by simpa [ξMin, hσMin_eq] using Finset.min'_le _ _ hmem,
             by simpa [ξMax, hσMax_eq] using Finset.le_max' _ _ hmem⟩
    have hxi_bounds : ∀ xi : D.Z, ξMin ≤ xi.val idx0 ∧ xi.val idx0 ≤ ξMax := by
      intro xi
      rcases xi.property with ⟨w, hw⟩
      have hw_flat : ∀ k, -D.rho ≤ blockToFlat w.val k ∧ blockToFlat w.val k ≤ D.rho := by
        intro k
        exact w.property (finProdFinEquiv.symm k).1 (finProdFinEquiv.symm k).2
      have hα : ∀ σ : Corner D, 0 ≤ baryWeight D.rho σ (blockToFlat w.val) :=
        fun σ => baryWeight_nonneg D.rho_pos σ _ hw_flat
      have hsum1 : ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) = 1 :=
        sum_baryWeight D.rho_pos (blockToFlat w.val)
      have hcoord : xi.val idx0 =
          ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * valAt σ := by
        rw [← hw]
        have hb := congrFun (deviation_barycentric D w).symm idx0
        simpa [valAt, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] using hb
      rw [hcoord]
      constructor
      · calc ξMin = (∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val)) * ξMin := by
              rw [hsum1, one_mul]
          _ = ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * ξMin := Finset.sum_mul ..
          _ ≤ ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * valAt σ :=
              Finset.sum_le_sum (fun σ _ => mul_le_mul_of_nonneg_left (hle_all σ).1 (hα σ))
      · calc ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * valAt σ
            ≤ ∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val) * ξMax :=
              Finset.sum_le_sum (fun σ _ => mul_le_mul_of_nonneg_left (hle_all σ).2 (hα σ))
          _ = (∑ σ : Corner D, baryWeight D.rho σ (blockToFlat w.val)) * ξMax :=
              (Finset.sum_mul ..).symm
          _ = ξMax := by rw [hsum1, one_mul]
    let bMin := uVert σMin
    let bMax := uVert σMax
    by_cases hdeg : ξMin = ξMax
    · -- Degenerate singleton `Z`: constant (affine with `K = 0`) rule `bMin` is exact
      let P : AffineDeviationPolicy D :=
        { b0 := bMin.val
          K := fun _ => 0
          in_box := fun xi t j => by
            simpa only [LinearMap.zero_apply, add_zero] using bMin.property t j }
      refine ⟨a, P, (BridgeFormalV3.Proofs.exact_tightening D a P.toDeviationPolicy eta).mpr ?_⟩
      intro xi
      have hxi_eq : xi.val = D.deviation (cornerNoise D σMin) := by
        funext i
        rw [hidx_unique i]
        have hb := hxi_bounds xi
        linarith
      have hnom_eq : D.aroNominalTerminal a P.toDeviationPolicy xi =
          D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σMin)) bMin.val 0 := by
        change D.expansion D.q (D.nominal a + xi.val) (fun t => bMin.val t + 0) 0 = _
        simp only [add_zero, hxi_eq]
      rw [hnom_eq]
      exact hvert σMin
    · -- Non-degenerate interval `[ξMin, ξMax]`: explicit 1D affine interpolation
      have hlt : ξMin < ξMax := lt_of_le_of_ne (hle_all σMax).1 hdeg
      let δ : ℝ := ξMax - ξMin
      have hδ_pos : 0 < δ := sub_pos.mpr hlt
      have hδ_ne : δ ≠ 0 := ne_of_gt hδ_pos
      let b0Fun : Fin D.q → Vec D.m := fun t j =>
        bMin.val t j - (ξMin / δ) * (bMax.val t j - bMin.val t j)
      let KFun : Fin D.q → (Vec D.n →ₗ[ℝ] Vec D.m) := fun t =>
        { toFun := fun v j => (v idx0 / δ) * (bMax.val t j - bMin.val t j)
          map_add' := fun u v => by funext j; simp only [Pi.add_apply]; ring
          map_smul' := fun r u => by funext j; simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]; ring }
      have heval_conv : ∀ (xi : D.Z) (t : Fin D.q) (j : Fin D.m),
          (b0Fun t + KFun t xi.val) j =
            (1 - (xi.val idx0 - ξMin) / δ) * bMin.val t j +
              ((xi.val idx0 - ξMin) / δ) * bMax.val t j := by
        intro xi t j
        simp only [Pi.add_apply, b0Fun, KFun, LinearMap.coe_mk, AddHom.coe_mk]
        field_simp [hδ_ne]
        ring
      let P : AffineDeviationPolicy D :=
        { b0 := b0Fun
          K := KFun
          in_box := fun xi t j => by
            let lam : ℝ := (xi.val idx0 - ξMin) / δ
            have hlam0 : 0 ≤ lam := div_nonneg (sub_nonneg.mpr (hxi_bounds xi).1) (le_of_lt hδ_pos)
            have hlam1 : lam ≤ 1 := (div_le_one hδ_pos).mpr (sub_le_sub_right (hxi_bounds xi).2 ξMin)
            have h1m : 0 ≤ 1 - lam := sub_nonneg.mpr hlam1
            rw [heval_conv xi t j]
            have hmin := bMin.property t j
            have hmax := bMax.property t j
            constructor <;> nlinarith }
      refine ⟨a, P, (BridgeFormalV3.Proofs.exact_tightening D a P.toDeviationPolicy eta).mpr ?_⟩
      intro xi
      let lam : ℝ := (xi.val idx0 - ξMin) / δ
      have hlam0 : 0 ≤ lam := div_nonneg (sub_nonneg.mpr (hxi_bounds xi).1) (le_of_lt hδ_pos)
      have hlam1 : lam ≤ 1 := (div_le_one hδ_pos).mpr (sub_le_sub_right (hxi_bounds xi).2 ξMin)
      have hxi_conv : xi.val =
          (1 - lam) • D.deviation (cornerNoise D σMin) +
            lam • D.deviation (cornerNoise D σMax) := by
        funext i
        rw [hidx_unique i]
        simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, lam]
        change xi.val idx0 = (1 - (xi.val idx0 - ξMin) / δ) * ξMin +
          ((xi.val idx0 - ξMin) / δ) * ξMax
        field_simp [hδ_ne]
        simp only [δ]
        ring
      have hctrl_conv : ∀ t : Fin D.q,
          (P.toDeviationPolicy.rule xi).val t = (1 - lam) • bMin.val t + lam • bMax.val t := by
        intro t
        funext j
        simpa only [AffineDeviationPolicy.toDeviationPolicy, Pi.add_apply, Pi.smul_apply,
          smul_eq_mul, lam] using heval_conv xi t j
      have hnom_conv : D.aroNominalTerminal a P.toDeviationPolicy xi =
          (1 - lam) • D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σMin)) bMin.val 0 +
            lam • D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σMax)) bMax.val 0 := by
        change D.expansion D.q (D.nominal a + xi.val) (P.toDeviationPolicy.rule xi).val 0 = _
        have ha_split : D.nominal a = (1 - lam) • D.nominal a + lam • D.nominal a := by
          rw [← add_smul]; norm_num
        simp only [Data.expansion, Pi.zero_apply, map_zero, add_zero]
        conv_lhs => rw [ha_split, hxi_conv]
        simp_rw [hctrl_conv, map_add, map_smul, Finset.sum_add_distrib, ← Finset.smul_sum, smul_add]
        abel
      rw [hnom_conv]
      constructor
      · intro i
        constructor
        · exact convex_comb_two_ineq lam hlam0 hlam1 (-(D.terminalRow i)) _ _ _ _
            ((hvert σMin).1 i).1 ((hvert σMax).1 i).1
        · exact convex_comb_two_ineq lam hlam0 hlam1 (D.terminalRow i) _ _ _ _
            ((hvert σMin).1 i).2 ((hvert σMax).1 i).2
      · exact convex_comb_two_ineq lam hlam0 hlam1 D.c _ _ _ _ (hvert σMin).2 (hvert σMax).2
  refine ⟨heq_aro, ?_⟩
  rw [heq_aro, BridgeFormalV2.Proofs.epigraph_equality D]

/-! ## Section 4: Minimal 2D strict ADR gap inside frozen `BridgeFormalV2.Data` -/

/-- Minimal 2D `BridgeFormalV2.Data` witness (`n=2, m=1, p=2, rows=2, r=1, q=1`):
`A=I_2, B=(1,1)^T, E=I_2, H=I_2, c=(1,1)^T, g_min=(0,0), g_max=(4,4), x_0=0, u_max=1, rho=1`. -/
abbrev bridgeAdrGapData : Data where
  n := 2
  m := 1
  p := 2
  rows := 2
  r := 1
  q := 1
  n_pos := by omega
  m_pos := Nat.zero_lt_one
  p_pos := by omega
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := LinearMap.id
  B :=
    { toFun := fun u _ => u 0
      map_add' := fun u v => by funext i; simp
      map_smul' := fun r u => by funext i; simp }
  E := LinearMap.id
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => 0
  gmax := fun _ => 4
  c :=
    { toFun := fun x => x 0 + x 1
      map_add' := fun x y => by simp; ring
      map_smul' := fun r x => by simp; ring }

private theorem gap_deviation_eq (wm : bridgeAdrGapData.NoiseBlock 1) (i : Fin 2) :
    bridgeAdrGapData.deviation wm i = wm.val 0 i := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, bridgeAdrGapData]

private theorem gap_terminal_eq (a : bridgeAdrGapData.ControlBlock 1)
    (b : bridgeAdrGapData.ControlBlock 1)
    (wm wp : bridgeAdrGapData.NoiseBlock 1) (i : Fin 2) :
    bridgeAdrGapData.expansion 1
      (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation wm) b.val wp.val i =
      a.val 0 0 + b.val 0 0 + wm.val 0 i + wp.val 0 i := by
  have ha0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    bridgeAdrGapData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    ha0, hw0, Module.End.one_apply, LinearMap.id_apply, LinearMap.coe_mk, AddHom.coe_mk,
    Pi.add_apply, Pi.zero_apply, zero_add, add_zero]
  ring

private def mkNoise2 (v0 v1 : ℝ) (h0 : -1 ≤ v0 ∧ v0 ≤ 1) (h1 : -1 ≤ v1 ∧ v1 ≤ 1) :
    bridgeAdrGapData.NoiseBlock 1 :=
  ⟨fun _ i => if i = 0 then v0 else v1, by
    intro t i
    fin_cases i
    · simpa [bridgeAdrGapData] using h0
    · simpa [bridgeAdrGapData] using h1⟩

/-- **Theorem O1.7 (2D Bridge Strict ADR Gap):**
Already at `D.n = 2`, ADR exactness fails strictly inside frozen `BridgeFormalV2.Data`:
on `bridgeAdrGapData`, level `6` is achievable by the continuous piecewise-affine adaptive rule
`u_1 = 1, u_2*(v_0, v_1) = max (-v_0) (-v_1)` (`6 ∈ D.aroLevels ∧ 6 ∈ D.sourceLevels`),
whereas EVERY affine decision rule satisfies `8 ≤ eta` (uniquely pinned to static `u_1 = 1, u_2 ≡ 1`). -/
theorem exists_bridge_2d_strict_adr_gap :
    ∃ D : Data, D.n = 2 ∧ (6 : ℝ) ∈ D.aroLevels ∧ (6 : ℝ) ∈ D.sourceLevels ∧
      ∀ eta ∈ bridgeAdrLevels D, (8 : ℝ) ≤ eta := by
  have h6_aro : (6 : ℝ) ∈ bridgeAdrGapData.aroLevels := by
    let a1 : bridgeAdrGapData.ControlBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    have hy_box : ∀ (xi : bridgeAdrGapData.Z) (t : Fin 1) (j : Fin 1),
        bridgeAdrGapData.umin j ≤ max (-xi.val 0) (-xi.val 1) ∧
        max (-xi.val 0) (-xi.val 1) ≤ bridgeAdrGapData.umax j := by
      intro xi t j
      rcases xi.property with ⟨wm, hwm⟩
      have h0 : -1 ≤ xi.val 0 ∧ xi.val 0 ≤ 1 := by
        rw [← hwm, gap_deviation_eq]; exact wm.property 0 0
      have h1 : -1 ≤ xi.val 1 ∧ xi.val 1 ≤ 1 := by
        rw [← hwm, gap_deviation_eq]; exact wm.property 0 1
      change (-1 : ℝ) ≤ max (-xi.val 0) (-xi.val 1) ∧ max (-xi.val 0) (-xi.val 1) ≤ 1
      exact ⟨le_trans (by linarith) (le_max_left _ _), max_le (by linarith) (by linarith)⟩
    let yRule : bridgeAdrGapData.Z → bridgeAdrGapData.ControlBlock 1 :=
      fun xi => ⟨fun _ _ => max (-xi.val 0) (-xi.val 1), hy_box xi⟩
    have hy_meas : Measurable yRule := by
      refine Continuous.measurable ?_
      refine Continuous.subtype_mk (continuous_pi fun _ => continuous_pi fun _ => ?_) _
      exact (((continuous_apply (0 : Fin 2)).comp continuous_subtype_val).neg).max
        (((continuous_apply (1 : Fin 2)).comp continuous_subtype_val).neg)
    let yPol : bridgeAdrGapData.DeviationPolicy := ⟨yRule, hy_meas⟩
    refine ⟨a1, yPol, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hw0 : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    have hw1 : (-1 : ℝ) ≤ wm.val 0 1 ∧ wm.val 0 1 ≤ 1 := wm.property 0 1
    have hq0 : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    have hq1 : (-1 : ℝ) ≤ wp.val 0 1 ∧ wp.val 0 1 ≤ 1 := wp.property 0 1
    have hxi0 : xi.val 0 = wm.val 0 0 := by rw [← hwm, gap_deviation_eq]
    have hxi1 : xi.val 1 = wm.val 0 1 := by rw [← hwm, gap_deviation_eq]
    have hb_eq : (yPol.rule xi).val 0 0 = max (-wm.val 0 0) (-wm.val 0 1) := by
      simp [yPol, yRule, hxi0, hxi1]
    have hx0 : bridgeAdrGapData.aroTerminal a1 yPol xi wp 0 =
        1 + max (-wm.val 0 0) (-wm.val 0 1) + wm.val 0 0 + wp.val 0 0 := by
      change bridgeAdrGapData.expansion 1
        (bridgeAdrGapData.nominal a1 + xi.val) (yPol.rule xi).val wp.val 0 = _
      rw [← hwm, gap_terminal_eq, hb_eq]
    have hx1 : bridgeAdrGapData.aroTerminal a1 yPol xi wp 1 =
        1 + max (-wm.val 0 0) (-wm.val 0 1) + wm.val 0 1 + wp.val 0 1 := by
      change bridgeAdrGapData.expansion 1
        (bridgeAdrGapData.nominal a1 + xi.val) (yPol.rule xi).val wp.val 1 = _
      rw [← hwm, gap_terminal_eq, hb_eq]
    have hm_ge0 : -wm.val 0 0 ≤ max (-wm.val 0 0) (-wm.val 0 1) := le_max_left _ _
    have hm_ge1 : -wm.val 0 1 ≤ max (-wm.val 0 0) (-wm.val 0 1) := le_max_right _ _
    have hm_le1 : max (-wm.val 0 0) (-wm.val 0 1) ≤ 1 := max_le (by linarith) (by linarith)
    constructor
    · intro i
      fin_cases i
      · change (0 : ℝ) ≤ bridgeAdrGapData.aroTerminal a1 yPol xi wp 0 ∧
          bridgeAdrGapData.aroTerminal a1 yPol xi wp 0 ≤ 4
        rw [hx0]; constructor <;> linarith
      · change (0 : ℝ) ≤ bridgeAdrGapData.aroTerminal a1 yPol xi wp 1 ∧
          bridgeAdrGapData.aroTerminal a1 yPol xi wp 1 ≤ 4
        rw [hx1]; constructor <;> linarith
    · change bridgeAdrGapData.aroTerminal a1 yPol xi wp 0 +
        bridgeAdrGapData.aroTerminal a1 yPol xi wp 1 ≤ 6
      rw [hx0, hx1]
      rcases max_choice (-wm.val 0 0) (-wm.val 0 1) with hcase | hcase <;> linarith
  refine ⟨bridgeAdrGapData, rfl, h6_aro, ?_, ?_⟩
  · rw [BridgeFormalV2.Proofs.epigraph_equality bridgeAdrGapData]
    exact h6_aro
  · intro eta ⟨a, P, hbound⟩
    let u1 : ℝ := a.val 0 0
    have hu1_le : u1 ≤ 1 := (a.property 0 0).2
    let b0 : ℝ := P.b0 0 0
    let k0 : ℝ := P.K 0 (Pi.single 0 (1 : ℝ)) 0
    let k1 : ℝ := P.K 0 (Pi.single 1 (1 : ℝ)) 0
    have hK_eval : ∀ v : Vec 2, P.K 0 v 0 = v 0 * k0 + v 1 * k1 := by
      intro v
      have hv : v = v 0 • Pi.single 0 (1 : ℝ) + v 1 • Pi.single 1 (1 : ℝ) := by
        funext i; fin_cases i <;> simp
      conv_lhs => rw [hv]
      rw [map_add, map_smul, map_smul]
      simp [k0, k1, smul_eq_mul]
    let w_mp := mkNoise2 (-1) 1 (by norm_num) (by norm_num)
    let w_pm := mkNoise2 1 (-1) (by norm_num) (by norm_num)
    let w_mm := mkNoise2 (-1) (-1) (by norm_num) (by norm_num)
    let w_pp := mkNoise2 1 1 (by norm_num) (by norm_num)
    have hval_at : ∀ wm : bridgeAdrGapData.NoiseBlock 1,
        (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation wm)).val 0 0 =
          b0 + wm.val 0 0 * k0 + wm.val 0 1 * k1 := by
      intro wm
      change P.b0 0 0 + P.K 0 (bridgeAdrGapData.deviation wm) 0 = _
      rw [hK_eval, gap_deviation_eq wm 0, gap_deviation_eq wm 1]
      ring
    -- Box upper bounds u2(v) <= 1 at all 4 corners
    have hub_mp : b0 - k0 + k1 ≤ 1 := by
      have h := (P.in_box (bridgeAdrGapData.observedDeviation w_mp) 0 0).2
      change (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_mp)).val 0 0 ≤ 1 at h
      rw [hval_at w_mp] at h
      have h0 : w_mp.val 0 0 = -1 := rfl
      have h1 : w_mp.val 0 1 = 1 := rfl
      rw [h0, h1] at h; linarith
    have hub_pm : b0 + k0 - k1 ≤ 1 := by
      have h := (P.in_box (bridgeAdrGapData.observedDeviation w_pm) 0 0).2
      change (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_pm)).val 0 0 ≤ 1 at h
      rw [hval_at w_pm] at h
      have h0 : w_pm.val 0 0 = 1 := rfl
      have h1 : w_pm.val 0 1 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hub_mm : b0 - k0 - k1 ≤ 1 := by
      have h := (P.in_box (bridgeAdrGapData.observedDeviation w_mm) 0 0).2
      change (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_mm)).val 0 0 ≤ 1 at h
      rw [hval_at w_mm] at h
      have h0 : w_mm.val 0 0 = -1 := rfl
      have h1 : w_mm.val 0 1 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hub_pp : b0 + k0 + k1 ≤ 1 := by
      have h := (P.in_box (bridgeAdrGapData.observedDeviation w_pp) 0 0).2
      change (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_pp)).val 0 0 ≤ 1 at h
      rw [hval_at w_pp] at h
      have h0 : w_pp.val 0 0 = 1 := rfl
      have h1 : w_pp.val 0 1 = 1 := rfl
      rw [h0, h1] at h; linarith
    -- Terminal lower bounds x_T >= 0 at w_mp and w_pm with worst-case w_2 = (-1, -1)
    have hlo_mp : (0 : ℝ) ≤ u1 + (b0 - k0 + k1) - 2 := by
      have h := ((hbound (bridgeAdrGapData.observedDeviation w_mp) w_mm).1 0).1
      change (0 : ℝ) ≤ bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
        (bridgeAdrGapData.observedDeviation w_mp) w_mm 0 at h
      have ht : bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_mp) w_mm 0 =
          u1 + (b0 - k0 + k1) - 2 := by
        change bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_mp)
          (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_mp)).val w_mm.val 0 = _
        rw [gap_terminal_eq, hval_at w_mp]
        have h0 : w_mp.val 0 0 = -1 := rfl
        have h1 : w_mp.val 0 1 = 1 := rfl
        have hp : w_mm.val 0 0 = -1 := rfl
        rw [h0, h1, hp]; ring
      linarith
    have hlo_pm : (0 : ℝ) ≤ u1 + (b0 + k0 - k1) - 2 := by
      have h := ((hbound (bridgeAdrGapData.observedDeviation w_pm) w_mm).1 1).1
      change (0 : ℝ) ≤ bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
        (bridgeAdrGapData.observedDeviation w_pm) w_mm 1 at h
      have ht : bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_pm) w_mm 1 =
          u1 + (b0 + k0 - k1) - 2 := by
        change bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pm)
          (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_pm)).val w_mm.val 1 = _
        rw [gap_terminal_eq, hval_at w_pm]
        have h0 : w_pm.val 0 0 = 1 := rfl
        have h1 : w_pm.val 0 1 = -1 := rfl
        have hp : w_mm.val 0 1 = -1 := rfl
        rw [h0, h1, hp]; ring
      linarith
    -- Cost bound at w_pp with worst-case w_2 = (+1, +1)
    have hcost_pp : 2 * u1 + 2 * (b0 + k0 + k1) + 4 ≤ eta := by
      have h := (hbound (bridgeAdrGapData.observedDeviation w_pp) w_pp).2
      change bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_pp) w_pp 0 +
        bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_pp) w_pp 1 ≤ eta at h
      have ht0 : bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_pp) w_pp 0 =
          u1 + (b0 + k0 + k1) + 2 := by
        change bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pp)
          (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_pp)).val w_pp.val 0 = _
        rw [gap_terminal_eq, hval_at w_pp]
        have h0 : w_pp.val 0 0 = 1 := rfl
        have h1 : w_pp.val 0 1 = 1 := rfl
        rw [h0, h1]; ring
      have ht1 : bridgeAdrGapData.aroTerminal a P.toDeviationPolicy
          (bridgeAdrGapData.observedDeviation w_pp) w_pp 1 =
          u1 + (b0 + k0 + k1) + 2 := by
        change bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pp)
          (P.toDeviationPolicy.rule (bridgeAdrGapData.observedDeviation w_pp)).val w_pp.val 1 = _
        rw [gap_terminal_eq, hval_at w_pp]
        have h0 : w_pp.val 0 0 = 1 := rfl
        have h1 : w_pp.val 0 1 = 1 := rfl
        rw [h0, h1]; ring
      linarith
    -- Square barycentric syzygy pins u1 = 1, b0 = 1, k0 = k1 = 0 -> eta >= 8!
    linarith


end AroProofs.BridgeO1ADRExactness
