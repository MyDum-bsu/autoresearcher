import BridgeFormalV3.Proofs.Support
import AroProofs.BridgeF4CornerLP
import AroProofs.BridgeO1ADRExactness
import AroProofs.BridgeO1FullRankRecourse

/-!
# Cycle 04 — O2 / O5: Lifted & Piecewise-Affine Decision Rules, `Ω(d)` Cross-Polytope Scaling,
Refutation of Coordinate-Separable Lifting (`H-O2-1`), and Single-Feature Diagonal-Hinge Restoration

Built strictly over frozen `BridgeFormalV2.Model` / `BridgeFormalV2.Goals`,
F3 `BridgeFormalV3.Proofs.Support`, F4 `BridgeF4CornerLP`, O1 `BridgeO1ADRExactness`,
and Cycle-03 `BridgeO1FullRankRecourse`. Zero `sorry`, zero custom axioms.

Main theorems (8 declarations):
  A. O5 Universal Lifted Hierarchy & Syzygy Obstruction:
     1. `lifted_adr_hierarchy_and_affine_collapse`: For any lifting `φ : ℝ^d → ℝ^L`,
        `adrLevels P Ξ ⊆ liftedAdrLevels P Ξ φ ⊆ aroLevels P Ξ`, and if `φ` is affine then
        `liftedAdrLevels P Ξ φ = adrLevels P Ξ` (nonlinearity is necessary to beat ADR).
     2. `lifted_barycentric_syzygy_coupling`: Universal lifted barycentric-syzygy obstruction:
        equal lifted barycenters force identical averages under every `φ`-lifted ADR.
  B. O2 Sharp `Ω(d)` Multiplicative Ratio vs. Segregated `|·|`-Lifting Exactness on `B_1^d`:
     3. `l1_cross_polytope_adr_ratio_linear`: For every `d ≥ 1`, on the `d`-dimensional `ℓ_1`
        cross-polytope `B_1^d`, `1 ∈ aroLevels` whereas EVERY affine decision rule satisfies
        `d ≤ eta` (exact `Ω(d)` multiplicative ratio `V_ADR / V_ARO ≥ d`).
     4. `segregated_ladr_exact_on_l1_cross_polytope`: For every `d ≥ 1` and EVERY fixed-recourse
        ARO problem `P`, coordinate-wise `|·|`-lifted (segregated) ADR is exact on `B_1^d`:
        `liftedAdrLevels P (l1CrossPolytope d) (absLift d) = aroLevels P (l1CrossPolytope d)`.
  C. O5 Refutation of `H-O2-1` (Coordinate-Separable Liftings Fail on the 2D Box & Bridge):
     5. `separable_rule_square_syzygy`: EVERY coordinate-separable rule
        `v ↦ y0 + f0 (v 0) + f1 (v 1)` (with completely arbitrary nonlinear `f0, f1`) satisfies
        the exact square barycentric syzygy `y(-r0, r1) + y(r0, -r1) = y(-r0, -r1) + y(r0, r1)`.
     6. `exists_bridge_2d_separable_strict_gap`: Inside frozen `BridgeFormalV2.Data`, BOTH
        `bridgeFullRankShearData` (`5 < 6`, invertible `B`) and `bridgeAdrGapData` (`6 < 8`,
        rank-1 `B`) suffer the exact same strict gap under EVERY coordinate-separable policy
        (subsuming all coordinate-wise `|·|`-lifted and axis-aligned piecewise-affine rules).
  D. O2 / O5 Sharp Positive Resolution (Single-Feature Diagonal-Hinge Restoration):
     7. `diagonal_lifted_adr_exact_on_box2d`: Adding the SINGLE scalar interaction feature
        `φ_diag(ξ) = |ξ_0 - ξ_1|` makes lifted ADR exact for EVERY fixed-recourse ARO problem `P`
        on the 2D box `[-1, 1]^2` via the exact Kuhn triangulation (coefficient `Z` = `1/4` of
        the square syzygy defect).
     8. `bridge_diagonal_lifted_adr_exact_2d_box`: Inside frozen `BridgeFormalV2.Data`, for EVERY
        2D instance whose deviation set `D.Z` is a rectangular box `[-r0, r0] × [-r1, r1]`
        (`r0, r1 > 0`), Borel-measurable single-feature diagonal-hinge lifted ADR is exact:
        `bridgeDiagLiftedAdrLevels D hn = D.aroLevels ∧ bridgeDiagLiftedAdrLevels D hn = D.sourceLevels`
        (in particular closing the gap on both `bridgeAdrGapData` and `bridgeFullRankShearData`).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 AroProofs.BridgeF4VertexLP
  AroProofs.BridgeO1ADRExactness AroProofs.BridgeO1FullRankRecourse MeasureTheory Set

namespace AroProofs.BridgeO2LiftedADR

/-! ## Section 1: O5 Universal Lifted ADR Hierarchy & Lifted Syzygy Obstruction -/

/-- `φ`-lifted affine decision rule (LADR) epigraph level set on `Ξ`:
`y(ξ) = y0 + Y ξ + Z (φ ξ)`. -/
def liftedAdrLevels {d m k L : ℕ} (P : FixedRecourseARO d m k) (Ξ : Set (Fin d → ℝ))
    (φ : (Fin d → ℝ) → (Fin L → ℝ)) : Set ℝ :=
  {eta | ∃ (y0 : Fin m → ℝ) (Y : (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ))
    (Z : (Fin L → ℝ) →ₗ[ℝ] (Fin m → ℝ)),
    ∀ ξ ∈ Ξ, (∀ i, P.B (y0 + Y ξ + Z (φ ξ)) i ≤ P.h0 i + P.H ξ i) ∧
      P.c (y0 + Y ξ + Z (φ ξ)) ≤ eta}

/-- **Theorem O5.2 (Lifted ADR Hierarchy & Affine-Lifting Collapse):**
For every fixed-recourse ARO `P`, uncertainty set `Ξ`, and feature map `φ : ℝ^d → ℝ^L`:
1. `adrLevels P Ξ ⊆ liftedAdrLevels P Ξ φ ⊆ aroLevels P Ξ`.
2. If `φ` is affine (`φ(ξ) = a0 + A ξ`), then `liftedAdrLevels P Ξ φ = adrLevels P Ξ`
   (nonlinearity of `φ` is necessary to strictly beat standard ADR). -/
theorem lifted_adr_hierarchy_and_affine_collapse {d m k L : ℕ} (P : FixedRecourseARO d m k)
    (Ξ : Set (Fin d → ℝ)) (φ : (Fin d → ℝ) → (Fin L → ℝ)) :
    (adrLevels P Ξ ⊆ liftedAdrLevels P Ξ φ ∧ liftedAdrLevels P Ξ φ ⊆ aroLevels P Ξ) ∧
      ((∃ (a0 : Fin L → ℝ) (A : (Fin d → ℝ) →ₗ[ℝ] (Fin L → ℝ)), ∀ ξ, φ ξ = a0 + A ξ) →
        liftedAdrLevels P Ξ φ = adrLevels P Ξ) := by
  have hsub1 : adrLevels P Ξ ⊆ liftedAdrLevels P Ξ φ := by
    intro eta ⟨y0, Y, hY⟩
    refine ⟨y0, Y, 0, ?_⟩
    intro ξ hξ
    simpa only [LinearMap.zero_apply, add_zero] using hY ξ hξ
  have hsub2 : liftedAdrLevels P Ξ φ ⊆ aroLevels P Ξ := by
    intro eta ⟨y0, Y, Z, hYZ⟩
    intro ξ hξ
    exact ⟨y0 + Y ξ + Z (φ ξ), hYZ ξ hξ⟩
  refine ⟨⟨hsub1, hsub2⟩, ?_⟩
  rintro ⟨a0, A, hφ⟩
  apply Set.Subset.antisymm _ hsub1
  intro eta ⟨y0, Y, Z, hYZ⟩
  refine ⟨y0 + Z a0, Y + Z.comp A, ?_⟩
  intro ξ hξ
  have heq : y0 + Z a0 + (Y + Z.comp A) ξ = y0 + Y ξ + Z (φ ξ) := by
    rw [hφ ξ, map_add]
    simp only [LinearMap.add_apply, LinearMap.comp_apply]
    abel
  rw [heq]
  exact hYZ ξ hξ

/-- **Theorem O5.3 (Universal Lifted Barycentric-Syzygy Obstruction):**
Whenever two finite discrete probability distributions `(α, ξ)` and `(β, ζ)` share the same
lifted barycenter in `(ξ, φ(ξ))`, EVERY `φ`-lifted affine rule produces identical barycentric
averages. Thus a lifting `φ` can only break an ADR obstruction by separating the lifted
barycenters of its active syzygies. -/
theorem lifted_barycentric_syzygy_coupling {d m L : ℕ} {ι₁ ι₂ : Type*} [Fintype ι₁] [Fintype ι₂]
    (φ : (Fin d → ℝ) → (Fin L → ℝ))
    (α : ι₁ → ℝ) (β : ι₂ → ℝ) (hα : ∑ a, α a = 1) (hβ : ∑ b, β b = 1)
    (ξ : ι₁ → Fin d → ℝ) (ζ : ι₂ → Fin d → ℝ)
    (hbary_x : ∑ a, α a • ξ a = ∑ b, β b • ζ b)
    (hbary_φ : ∑ a, α a • φ (ξ a) = ∑ b, β b • φ (ζ b))
    (y0 : Fin m → ℝ) (Y : (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ)) (Z : (Fin L → ℝ) →ₗ[ℝ] (Fin m → ℝ)) :
    ∑ a, α a • (y0 + Y (ξ a) + Z (φ (ξ a))) = ∑ b, β b • (y0 + Y (ζ b) + Z (φ (ζ b))) := by
  have lhs_eq : ∑ a, α a • (y0 + Y (ξ a) + Z (φ (ξ a))) =
      y0 + Y (∑ a, α a • ξ a) + Z (∑ a, α a • φ (ξ a)) := by
    simp_rw [smul_add, Finset.sum_add_distrib, ← Finset.sum_smul, hα, one_smul]
    congr 1
    · congr 1
      rw [map_sum]
      simp_rw [map_smul]
    · rw [map_sum]
      simp_rw [map_smul]
  have rhs_eq : ∑ b, β b • (y0 + Y (ζ b) + Z (φ (ζ b))) =
      y0 + Y (∑ b, β b • ζ b) + Z (∑ b, β b • φ (ζ b)) := by
    simp_rw [smul_add, Finset.sum_add_distrib, ← Finset.sum_smul, hβ, one_smul]
    congr 1
    · congr 1
      rw [map_sum]
      simp_rw [map_smul]
    · rw [map_sum]
      simp_rw [map_smul]
  rw [lhs_eq, rhs_eq, hbary_x, hbary_φ]

/-! ## Section 2: O2 `Ω(d)` Cross-Polytope Ratio & Arbitrary-`d` Segregated `|·|`-Lifting Exactness -/

/-- Unit `ℓ_1` cross-polytope `B_1^d = {ξ ∈ ℝ^d | ∑ i, |ξ i| ≤ 1}` in arbitrary dimension `d`. -/
def l1CrossPolytope (d : ℕ) : Set (Fin d → ℝ) :=
  {ξ | ∑ i : Fin d, |ξ i| ≤ 1}

/-- Coordinate-wise absolute-value lifting `φ_abs(ξ) = (|ξ_0|, ..., |ξ_{d-1}|)`. -/
def absLift (d : ℕ) : (Fin d → ℝ) → (Fin d → ℝ) :=
  fun ξ i => |ξ i|

/-- `d`-dimensional Chen-Zhang fixed-recourse ARO: `y_i ≥ ±ξ_i`, minimize `∑_i y_i`. -/
abbrev chenZhangND (d : ℕ) (hd : 0 < d) : FixedRecourseARO d d (2 * d) where
  B :=
    { toFun := fun y idx => -y ⟨idx.val % d, Nat.mod_lt _ hd⟩
      map_add' := fun u v => by funext idx; simp; ring
      map_smul' := fun r u => by funext idx; simp }
  h0 := 0
  H :=
    { toFun := fun ξ idx =>
        if idx.val < d then -ξ ⟨idx.val % d, Nat.mod_lt _ hd⟩
        else ξ ⟨idx.val % d, Nat.mod_lt _ hd⟩
      map_add' := fun u v => by
        funext idx
        by_cases h : idx.val < d
        · simp [h]; ring
        · simp [h]
      map_smul' := fun r u => by
        funext idx
        by_cases h : idx.val < d <;> simp [h] }
  c :=
    { toFun := fun y => ∑ i : Fin d, y i
      map_add' := fun u v => by simp [Finset.sum_add_distrib]
      map_smul' := fun r u => by simp [Finset.mul_sum] }

/-- **Theorem O2.2 (Exact `Ω(d)` Multiplicative ADR Ratio on the `d`-D `ℓ_1` Cross-Polytope):**
For every dimension `d ≥ 1`, on `B_1^d`:
- `1 ∈ aroLevels (chenZhangND d hd) (l1CrossPolytope d)` (attained by `y_i(ξ) = |ξ_i|`),
- EVERY affine decision rule satisfies `(d : ℝ) ≤ eta` (exact multiplicative ratio `≥ d`). -/
theorem l1_cross_polytope_adr_ratio_linear (d : ℕ) (hd : 0 < d) :
    (1 : ℝ) ∈ aroLevels (chenZhangND d hd) (l1CrossPolytope d) ∧
      ∀ eta ∈ adrLevels (chenZhangND d hd) (l1CrossPolytope d), (d : ℝ) ≤ eta := by
  constructor
  · intro ξ hξ
    refine ⟨fun i => |ξ i|, ?_, ?_⟩
    · intro idx
      by_cases h : idx.val < d
      · simp [h, neg_le_neg_iff, le_abs_self]
      · simp [h, neg_abs_le]
    · exact hξ
  · intro eta ⟨y0, Y, hY⟩
    have h0_mem : (0 : Fin d → ℝ) ∈ l1CrossPolytope d := by
      simp [l1CrossPolytope]
    have hcost0 : ∑ i : Fin d, y0 i ≤ eta := by
      have h0 := (hY 0 h0_mem).2
      simpa [chenZhangND] using h0
    have hy0_ge1 : ∀ i : Fin d, (1 : ℝ) ≤ y0 i := by
      intro i
      let ep : Fin d → ℝ := Pi.single i (1 : ℝ)
      let em : Fin d → ℝ := -ep
      have hep_mem : ep ∈ l1CrossPolytope d := by
        show ∑ j : Fin d, |Pi.single i (1 : ℝ) j| ≤ 1
        have hsum : ∑ j : Fin d, |Pi.single i (1 : ℝ) j| = 1 := by
          rw [Finset.sum_eq_single i]
          · simp
          · intro j _ hji; simp [Pi.single_eq_of_ne hji]
          · intro hi; exact absurd (Finset.mem_univ i) hi
        linarith
      have hem_mem : em ∈ l1CrossPolytope d := by
        show ∑ j : Fin d, |(-ep) j| ≤ 1
        simpa [l1CrossPolytope, Pi.neg_apply, abs_neg] using hep_mem
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
        have hmod : i.val % d = i.val := Nat.mod_eq_of_lt i.isLt
        have hfin : (⟨i.val % d, Nat.mod_lt _ hd⟩ : Fin d) = i := Fin.ext hmod
        have hlt : i.val < d := i.isLt
        simp only [chenZhangND, LinearMap.coe_mk, AddHom.coe_mk, Pi.zero_apply, zero_add,
          hlt, ↓reduceIte, hfin] at h
        simpa [ep] using h
      have hm_ineq : -(y0 i + Y em i) ≤ -1 := by
        have h := (hY em hem_mem).1 ⟨i.val + d, by omega⟩
        have hmod : (i.val + d) % d = i.val := by
          rw [Nat.add_mod_right]; exact Nat.mod_eq_of_lt i.isLt
        have hfin : (⟨(i.val + d) % d, Nat.mod_lt _ hd⟩ : Fin d) = i := Fin.ext hmod
        have hge : ¬ (i.val + d < d) := by omega
        simp only [chenZhangND, LinearMap.coe_mk, AddHom.coe_mk, Pi.zero_apply, zero_add,
          hge, ↓reduceIte, hfin] at h
        simpa [em, ep] using h
      simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul] at hsyz
      linarith
    have hsum_ge : (d : ℝ) ≤ ∑ i : Fin d, y0 i := by
      calc (d : ℝ) = ∑ _i : Fin d, (1 : ℝ) := by simp
        _ ≤ ∑ i : Fin d, y0 i := Finset.sum_le_sum (fun i _ => hy0_ge1 i)
    linarith

private def segLinY {d m : ℕ} (yp ym : Fin d → (Fin m → ℝ)) :
    (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun ξ := ∑ j : Fin d, ((1 / 2 : ℝ) * ξ j) • (yp j - ym j)
  map_add' ξ₁ ξ₂ := by
    simp only [Pi.add_apply, mul_add, add_smul, Finset.sum_add_distrib]
  map_smul' r ξ := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.smul_sum, mul_smul]
    apply Finset.sum_congr rfl
    intro j _
    exact smul_comm (1 / 2 : ℝ) r _

private def segLinZ {d m : ℕ} (y0 : Fin m → ℝ) (yp ym : Fin d → (Fin m → ℝ)) :
    (Fin d → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun ζ := ∑ j : Fin d, ((1 / 2 : ℝ) * ζ j) • (yp j + ym j - (2 : ℝ) • y0)
  map_add' ζ₁ ζ₂ := by
    simp only [Pi.add_apply, mul_add, add_smul, Finset.sum_add_distrib]
  map_smul' r ζ := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply, Finset.smul_sum, mul_smul]
    apply Finset.sum_congr rfl
    intro j _
    exact smul_comm (1 / 2 : ℝ) r _

/-- **Theorem O2.3 (Arbitrary-Dimension Segregated `|·|`-Lifted ADR Exactness on `B_1^d`):**
For EVERY dimension `d : ℕ` and EVERY fixed-recourse ARO problem `P`, coordinate-wise `|·|`-lifted
(segregated) ADR is exact on the `ℓ_1` cross-polytope `B_1^d`:
`liftedAdrLevels P (l1CrossPolytope d) (absLift d) = aroLevels P (l1CrossPolytope d)`.
This collapses the `Ω(d)` ADR ratio of Theorem O2.2 to `0`. -/
theorem segregated_ladr_exact_on_l1_cross_polytope {d m k : ℕ} (P : FixedRecourseARO d m k) :
    liftedAdrLevels P (l1CrossPolytope d) (absLift d) = aroLevels P (l1CrossPolytope d) := by
  apply Set.Subset.antisymm (lifted_adr_hierarchy_and_affine_collapse P (l1CrossPolytope d) (absLift d)).1.2
  intro eta haro
  have h0_mem : (0 : Fin d → ℝ) ∈ l1CrossPolytope d := by simp [l1CrossPolytope]
  obtain ⟨y0, hy0_feas, hy0_cost⟩ := haro 0 h0_mem
  have hep_mem : ∀ j : Fin d, Pi.single j (1 : ℝ) ∈ l1CrossPolytope d := by
    intro j
    show ∑ l : Fin d, |Pi.single j (1 : ℝ) l| ≤ 1
    have hsum : ∑ l : Fin d, |Pi.single j (1 : ℝ) l| = 1 := by
      rw [Finset.sum_eq_single j]
      · simp
      · intro l _ hlj; simp [Pi.single_eq_of_ne hlj]
      · intro hj; exact absurd (Finset.mem_univ j) hj
    linarith
  have hem_mem : ∀ j : Fin d, -(Pi.single j (1 : ℝ)) ∈ l1CrossPolytope d := by
    intro j
    show ∑ l : Fin d, |(-(Pi.single j (1 : ℝ))) l| ≤ 1
    simpa [l1CrossPolytope, Pi.neg_apply, abs_neg] using hep_mem j
  choose yp hyp_feas hyp_cost using fun j => haro (Pi.single j (1 : ℝ)) (hep_mem j)
  choose ym hym_feas hym_cost using fun j => haro (-(Pi.single j (1 : ℝ))) (hem_mem j)
  refine ⟨y0, segLinY yp ym, segLinZ y0 yp ym, ?_⟩
  intro ξ hξ
  let w0 : ℝ := 1 - ∑ j : Fin d, |ξ j|
  let pj : Fin d → ℝ := fun j => (|ξ j| + ξ j) / 2
  let qj : Fin d → ℝ := fun j => (|ξ j| - ξ j) / 2
  have hw0_nn : 0 ≤ w0 := sub_nonneg.mpr hξ
  have hpj_nn : ∀ j, 0 ≤ pj j := fun j => by
    have h := neg_abs_le (ξ j); dsimp [pj]; linarith
  have hqj_nn : ∀ j, 0 ≤ qj j := fun j => by
    have h := le_abs_self (ξ j); dsimp [qj]; linarith
  have hw_total : w0 + ∑ j : Fin d, (pj j + qj j) = 1 := by
    have hsum : ∑ j : Fin d, (pj j + qj j) = ∑ j : Fin d, |ξ j| := by
      apply Finset.sum_congr rfl; intro j _; dsimp [pj, qj]; ring
    rw [hsum]; dsimp [w0]; ring
  have hy_conv : y0 + segLinY yp ym ξ + segLinZ y0 yp ym (absLift d ξ) =
      w0 • y0 + ∑ j : Fin d, (pj j • yp j + qj j • ym j) := by
    funext r
    simp only [segLinY, segLinZ, absLift, LinearMap.coe_mk, AddHom.coe_mk, Pi.add_apply,
      Pi.sub_apply, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, w0, pj, qj]
    have hcomb :
        (∑ j : Fin d, (1 / 2 : ℝ) * ξ j * (yp j r - ym j r)) +
          (∑ j : Fin d, (1 / 2 : ℝ) * |ξ j| * (yp j r + ym j r - 2 * y0 r)) =
        (∑ j : Fin d, ((|ξ j| + ξ j) / 2 * yp j r + (|ξ j| - ξ j) / 2 * ym j r)) -
          (∑ j : Fin d, |ξ j|) * y0 r := by
      rw [← Finset.sum_add_distrib, Finset.sum_mul, ← Finset.sum_sub_distrib]
      apply Finset.sum_congr rfl
      intro j _; ring
    linarith
  have hξ_conv : ξ = ∑ j : Fin d, (pj j • Pi.single j (1 : ℝ) + qj j • (-(Pi.single j (1 : ℝ)))) := by
    funext r
    simp only [Finset.sum_apply, Pi.add_apply, Pi.smul_apply, Pi.neg_apply, smul_eq_mul]
    rw [Finset.sum_eq_single r]
    · simp only [Pi.single_eq_same, pj, qj]; ring
    · intro j _ hjr; simp [Pi.single_eq_of_ne (Ne.symm hjr)]
    · intro hr; exact absurd (Finset.mem_univ r) hr
  constructor
  · intro i
    have hB : P.B (y0 + segLinY yp ym ξ + segLinZ y0 yp ym (absLift d ξ)) i =
        w0 * P.B y0 i + ∑ j : Fin d, (pj j * P.B (yp j) i + qj j * P.B (ym j) i) := by
      rw [hy_conv, map_add, map_smul, map_sum]
      simp [Finset.sum_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    have hH : P.H ξ i =
        ∑ j : Fin d, (pj j * P.H (Pi.single j (1 : ℝ)) i + qj j * P.H (-(Pi.single j (1 : ℝ))) i) := by
      conv_lhs => rw [hξ_conv]
      rw [map_sum]
      simp [Finset.sum_apply, Pi.add_apply, Pi.smul_apply, smul_eq_mul]
    rw [hB]
    have h1 : w0 * P.B y0 i ≤ w0 * P.h0 i := by
      have h0i := hy0_feas i
      have hz : P.H 0 i = 0 := by simp
      rw [hz, add_zero] at h0i
      exact mul_le_mul_of_nonneg_left h0i hw0_nn
    have h2 : ∑ j : Fin d, (pj j * P.B (yp j) i + qj j * P.B (ym j) i) ≤
        ∑ j : Fin d, (pj j * (P.h0 i + P.H (Pi.single j (1 : ℝ)) i) +
          qj j * (P.h0 i + P.H (-(Pi.single j (1 : ℝ))) i)) := by
      apply Finset.sum_le_sum
      intro j _
      exact add_le_add (mul_le_mul_of_nonneg_left (hyp_feas j i) (hpj_nn j))
        (mul_le_mul_of_nonneg_left (hym_feas j i) (hqj_nn j))
    calc w0 * P.B y0 i + ∑ j : Fin d, (pj j * P.B (yp j) i + qj j * P.B (ym j) i)
        ≤ w0 * P.h0 i + ∑ j : Fin d, (pj j * (P.h0 i + P.H (Pi.single j (1 : ℝ)) i) +
            qj j * (P.h0 i + P.H (-(Pi.single j (1 : ℝ))) i)) := add_le_add h1 h2
      _ = (w0 + ∑ j : Fin d, (pj j + qj j)) * P.h0 i +
            ∑ j : Fin d, (pj j * P.H (Pi.single j (1 : ℝ)) i +
              qj j * P.H (-(Pi.single j (1 : ℝ))) i) := by
          have hrearr :
              ∑ j : Fin d, (pj j * (P.h0 i + P.H (Pi.single j (1 : ℝ)) i) +
                qj j * (P.h0 i + P.H (-(Pi.single j (1 : ℝ))) i)) =
              (∑ j : Fin d, (pj j + qj j)) * P.h0 i +
                ∑ j : Fin d, (pj j * P.H (Pi.single j (1 : ℝ)) i +
                  qj j * P.H (-(Pi.single j (1 : ℝ))) i) := by
            rw [Finset.sum_mul, ← Finset.sum_add_distrib]
            apply Finset.sum_congr rfl; intro j _; ring
          linarith
      _ = P.h0 i + P.H ξ i := by rw [hw_total, one_mul, hH]
  · have hc : P.c (y0 + segLinY yp ym ξ + segLinZ y0 yp ym (absLift d ξ)) =
        w0 * P.c y0 + ∑ j : Fin d, (pj j * P.c (yp j) + qj j * P.c (ym j)) := by
      rw [hy_conv, map_add, map_smul, map_sum]
      simp [smul_eq_mul]
    rw [hc]
    calc w0 * P.c y0 + ∑ j : Fin d, (pj j * P.c (yp j) + qj j * P.c (ym j))
        ≤ w0 * eta + ∑ j : Fin d, (pj j * eta + qj j * eta) :=
          add_le_add (mul_le_mul_of_nonneg_left hy0_cost hw0_nn)
            (Finset.sum_le_sum fun j _ => add_le_add
              (mul_le_mul_of_nonneg_left (hyp_cost j) (hpj_nn j))
              (mul_le_mul_of_nonneg_left (hym_cost j) (hqj_nn j)))
      _ = (w0 + ∑ j : Fin d, (pj j + qj j)) * eta := by
          have hrearr : ∑ j : Fin d, (pj j * eta + qj j * eta) =
              (∑ j : Fin d, (pj j + qj j)) * eta := by
            rw [Finset.sum_mul]; apply Finset.sum_congr rfl; intro j _; ring
          linarith
      _ = eta := by rw [hw_total, one_mul]

/-! ## Section 3: O5 Refutation of `H-O2-1` — Coordinate-Separable Liftings Fail on 2D Box & Bridge -/

/-- **Theorem O5.4 (Universal Square Syzygy for Coordinate-Separable Rules):**
EVERY coordinate-separable decision rule `v ↦ y0 + f0 (v 0) + f1 (v 1)` — with completely
arbitrary nonlinear univariate functions `f0, f1 : ℝ → Vec m` (subsuming all coordinate-wise
`|·|`-lifted, spline, and axis-aligned piecewise-affine rules with arbitrarily many breakpoints) —
still obeys the exact square barycentric syzygy on any axis-aligned rectangle `[-r0, r0] × [-r1, r1]`. -/
theorem separable_rule_square_syzygy {m : ℕ} (y0 : Vec m) (f0 f1 : ℝ → Vec m) (r0 r1 : ℝ) :
    let rule : Vec 2 → Vec m := fun v => y0 + f0 (v 0) + f1 (v 1)
    rule ![-r0, r1] + rule ![r0, -r1] = rule ![-r0, -r1] + rule ![r0, r1] := by
  intro rule
  funext j
  simp only [rule, Pi.add_apply, Matrix.cons_val_zero, Matrix.cons_val_one]
  ring

/-- A Borel-measurable coordinate-separable deviation policy on a 2D frozen `BridgeFormalV2.Data`:
`u_2(ξ)_t = b0_t + f0_t(ξ_0) + f1_t(ξ_1)` for arbitrary univariate `f0, f1`. -/
structure SeparableDeviationPolicy (D : Data) (hn : D.n = 2) where
  pol : D.DeviationPolicy
  b0 : Fin D.q → Vec D.m
  f0 : Fin D.q → ℝ → Vec D.m
  f1 : Fin D.q → ℝ → Vec D.m
  is_separable : ∀ (xi : D.Z) (t : Fin D.q),
    (pol.rule xi).val t = b0 t + f0 t (xi.val ⟨0, by omega⟩) + f1 t (xi.val ⟨1, by omega⟩)

/-- Epigraph level set achievable by arbitrary coordinate-separable policies on 2D frozen `Data`. -/
def bridgeSeparableLevels (D : Data) (hn : D.n = 2) : Set ℝ :=
  {eta | ∃ (a : D.ControlBlock D.r) (P : SeparableDeviationPolicy D hn),
    D.AROBound a P.pol eta}

private def mkNoiseShear (v0 v1 : ℝ) (h0 : -1 ≤ v0 ∧ v0 ≤ 1) (h1 : -1 ≤ v1 ∧ v1 ≤ 1) :
    bridgeFullRankShearData.NoiseBlock 1 :=
  ⟨fun _ i => if i = 0 then v0 else v1, by
    intro t i; fin_cases i
    · simpa [bridgeFullRankShearData] using h0
    · simpa [bridgeFullRankShearData] using h1⟩

private def mkNoiseRank1 (v0 v1 : ℝ) (h0 : -1 ≤ v0 ∧ v0 ≤ 1) (h1 : -1 ≤ v1 ∧ v1 ≤ 1) :
    bridgeAdrGapData.NoiseBlock 1 :=
  ⟨fun _ i => if i = 0 then v0 else v1, by
    intro t i; fin_cases i
    · simpa [bridgeAdrGapData] using h0
    · simpa [bridgeAdrGapData] using h1⟩

private theorem shear_dev_eq (wm : bridgeFullRankShearData.NoiseBlock 1) (i : Fin 2) :
    bridgeFullRankShearData.deviation wm i = wm.val 0 i := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, bridgeFullRankShearData]

private theorem rank1_dev_eq (wm : bridgeAdrGapData.NoiseBlock 1) (i : Fin 2) :
    bridgeAdrGapData.deviation wm i = wm.val 0 i := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, bridgeAdrGapData]

private theorem shear_term_eq0 (a b : bridgeFullRankShearData.ControlBlock 1)
    (wm wp : bridgeFullRankShearData.NoiseBlock 1) :
    bridgeFullRankShearData.expansion 1
      (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation wm) b.val wp.val 0 =
      a.val 0 0 + a.val 0 1 + b.val 0 0 + b.val 0 1 + wm.val 0 0 + wp.val 0 0 := by
  have ha0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    bridgeFullRankShearData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    ha0, hw0, Module.End.one_apply, LinearMap.id_apply, LinearMap.coe_mk, AddHom.coe_mk,
    Pi.add_apply, Pi.zero_apply, zero_add, add_zero, ↓reduceIte]
  ring

private theorem shear_term_eq1 (a b : bridgeFullRankShearData.ControlBlock 1)
    (wm wp : bridgeFullRankShearData.NoiseBlock 1) :
    bridgeFullRankShearData.expansion 1
      (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation wm) b.val wp.val 1 =
      a.val 0 1 + b.val 0 1 + wm.val 0 1 + wp.val 0 1 := by
  have ha0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  have hne : (1 : Fin 2) ≠ 0 := by decide
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    bridgeFullRankShearData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    ha0, hw0, Module.End.one_apply, LinearMap.id_apply, LinearMap.coe_mk, AddHom.coe_mk,
    Pi.add_apply, Pi.zero_apply, zero_add, add_zero, hne, ↓reduceIte]
  ring

private theorem rank1_term_eq (a b : bridgeAdrGapData.ControlBlock 1)
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

/-- **Theorem O5.5 (Refutation of `H-O2-1` Inside Frozen `BridgeFormalV2.Data`):**
Even allowing ARBITRARY coordinate-separable nonlinear policies `u_2(ξ) = b0 + f0(ξ_0) + f1(ξ_1)`
(strictly containing all coordinate-wise `|·|`-lifted and axis-aligned piecewise-affine rules),
BOTH frozen 2D bridge witnesses suffer the exact same strict gap as standard ADR:
1. `bridgeFullRankShearData` (bijective unimodular `B`): `5 ∈ aroLevels ∩ sourceLevels`, yet
   `∀ eta ∈ bridgeSeparableLevels, 6 ≤ eta`;
2. `bridgeAdrGapData` (rank-1 `B`): `6 ∈ aroLevels ∩ sourceLevels`, yet
   `∀ eta ∈ bridgeSeparableLevels, 8 ≤ eta`. -/
theorem exists_bridge_2d_separable_strict_gap :
    (∀ eta ∈ bridgeSeparableLevels bridgeFullRankShearData rfl, (6 : ℝ) ≤ eta) ∧
      (∀ eta ∈ bridgeSeparableLevels bridgeAdrGapData rfl, (8 : ℝ) ≤ eta) := by
  constructor
  · -- Part 1: Full-rank shear witness (every separable policy has eta >= 6)
    intro eta ⟨a, P, hbound⟩
    let u10 : ℝ := a.val 0 0
    let u11 : ℝ := a.val 0 1
    have hu10_le : u10 ≤ (1 / 2 : ℝ) := (a.property 0 0).2
    have hu11_le : u11 ≤ (1 / 2 : ℝ) := (a.property 0 1).2
    let w_mp := mkNoiseShear (-1) 1 (by norm_num) (by norm_num)
    let w_pm := mkNoiseShear 1 (-1) (by norm_num) (by norm_num)
    let w_mm := mkNoiseShear (-1) (-1) (by norm_num) (by norm_num)
    let w_pp := mkNoiseShear 1 1 (by norm_num) (by norm_num)
    let u2At : bridgeFullRankShearData.NoiseBlock 1 → Fin 2 → ℝ := fun wm j =>
      (P.pol.rule (bridgeFullRankShearData.observedDeviation wm)).val 0 j
    have hsyz_u21 : u2At w_mp 1 + u2At w_pm 1 = u2At w_mm 1 + u2At w_pp 1 := by
      have hmp := congrFun (P.is_separable (bridgeFullRankShearData.observedDeviation w_mp) 0) 1
      have hpm := congrFun (P.is_separable (bridgeFullRankShearData.observedDeviation w_pm) 0) 1
      have hmm := congrFun (P.is_separable (bridgeFullRankShearData.observedDeviation w_mm) 0) 1
      have hpp := congrFun (P.is_separable (bridgeFullRankShearData.observedDeviation w_pp) 0) 1
      have hd_mp0 : (bridgeFullRankShearData.observedDeviation w_mp).val ⟨0, by decide⟩ = -1 := by
        change bridgeFullRankShearData.deviation w_mp 0 = -1; rw [shear_dev_eq]; rfl
      have hd_mp1 : (bridgeFullRankShearData.observedDeviation w_mp).val ⟨1, by decide⟩ = 1 := by
        change bridgeFullRankShearData.deviation w_mp 1 = 1; rw [shear_dev_eq]; rfl
      have hd_pm0 : (bridgeFullRankShearData.observedDeviation w_pm).val ⟨0, by decide⟩ = 1 := by
        change bridgeFullRankShearData.deviation w_pm 0 = 1; rw [shear_dev_eq]; rfl
      have hd_pm1 : (bridgeFullRankShearData.observedDeviation w_pm).val ⟨1, by decide⟩ = -1 := by
        change bridgeFullRankShearData.deviation w_pm 1 = -1; rw [shear_dev_eq]; rfl
      have hd_mm0 : (bridgeFullRankShearData.observedDeviation w_mm).val ⟨0, by decide⟩ = -1 := by
        change bridgeFullRankShearData.deviation w_mm 0 = -1; rw [shear_dev_eq]; rfl
      have hd_mm1 : (bridgeFullRankShearData.observedDeviation w_mm).val ⟨1, by decide⟩ = -1 := by
        change bridgeFullRankShearData.deviation w_mm 1 = -1; rw [shear_dev_eq]; rfl
      have hd_pp0 : (bridgeFullRankShearData.observedDeviation w_pp).val ⟨0, by decide⟩ = 1 := by
        change bridgeFullRankShearData.deviation w_pp 0 = 1; rw [shear_dev_eq]; rfl
      have hd_pp1 : (bridgeFullRankShearData.observedDeviation w_pp).val ⟨1, by decide⟩ = 1 := by
        change bridgeFullRankShearData.deviation w_pp 1 = 1; rw [shear_dev_eq]; rfl
      change (P.pol.rule (bridgeFullRankShearData.observedDeviation w_mp)).val 0 1 +
          (P.pol.rule (bridgeFullRankShearData.observedDeviation w_pm)).val 0 1 =
        (P.pol.rule (bridgeFullRankShearData.observedDeviation w_mm)).val 0 1 +
          (P.pol.rule (bridgeFullRankShearData.observedDeviation w_pp)).val 0 1
      rw [hmp, hpm, hmm, hpp]
      simp only [Pi.add_apply, hd_mp0, hd_mp1, hd_pm0, hd_pm1, hd_mm0, hd_mm1, hd_pp0, hd_pp1]
      ring
    have hub_mp0 : u2At w_mp 0 ≤ (1 / 2 : ℝ) :=
      ((P.pol.rule (bridgeFullRankShearData.observedDeviation w_mp)).property 0 0).2
    have hub_mp1 : u2At w_mp 1 ≤ (1 / 2 : ℝ) :=
      ((P.pol.rule (bridgeFullRankShearData.observedDeviation w_mp)).property 0 1).2
    have hub_pm1 : u2At w_pm 1 ≤ (1 / 2 : ℝ) :=
      ((P.pol.rule (bridgeFullRankShearData.observedDeviation w_pm)).property 0 1).2
    have hub_mm1 : u2At w_mm 1 ≤ (1 / 2 : ℝ) :=
      ((P.pol.rule (bridgeFullRankShearData.observedDeviation w_mm)).property 0 1).2
    have hlb_pp0 : -(1 / 2 : ℝ) ≤ u2At w_pp 0 :=
      ((P.pol.rule (bridgeFullRankShearData.observedDeviation w_pp)).property 0 0).1
    have hlo_mp0 : (0 : ℝ) ≤ u10 + u11 + u2At w_mp 0 + u2At w_mp 1 - 2 := by
      have h := ((hbound (bridgeFullRankShearData.observedDeviation w_mp) w_mm).1 0).1
      change (0 : ℝ) ≤ bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_mp)
        (P.pol.rule (bridgeFullRankShearData.observedDeviation w_mp)).val w_mm.val 0 at h
      rw [shear_term_eq0] at h
      have h0 : w_mp.val 0 0 = -1 := rfl
      have h1 : w_mm.val 0 0 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hlo_pm1 : (-1 : ℝ) ≤ u11 + u2At w_pm 1 - 2 := by
      have h := ((hbound (bridgeFullRankShearData.observedDeviation w_pm) w_mm).1 1).1
      change (-1 : ℝ) ≤ bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pm)
        (P.pol.rule (bridgeFullRankShearData.observedDeviation w_pm)).val w_mm.val 1 at h
      rw [shear_term_eq1] at h
      have h0 : w_pm.val 0 1 = -1 := rfl
      have h1 : w_mm.val 0 1 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hcost_pp : u10 + 2 * u11 + u2At w_pp 0 + 2 * u2At w_pp 1 + 4 ≤ eta := by
      have h := (hbound (bridgeFullRankShearData.observedDeviation w_pp) w_pp).2
      change bridgeFullRankShearData.expansion 1
          (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pp)
          (P.pol.rule (bridgeFullRankShearData.observedDeviation w_pp)).val w_pp.val 0 +
        bridgeFullRankShearData.expansion 1
          (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pp)
          (P.pol.rule (bridgeFullRankShearData.observedDeviation w_pp)).val w_pp.val 1 ≤ eta at h
      rw [shear_term_eq0, shear_term_eq1] at h
      have h0 : w_pp.val 0 0 = 1 := rfl
      have h1 : w_pp.val 0 1 = 1 := rfl
      rw [h0, h1] at h; linarith
    linarith
  · -- Part 2: Rank-1 bridge witness (every separable policy has eta >= 8)
    intro eta ⟨a, P, hbound⟩
    let u1 : ℝ := a.val 0 0
    have hu1_le : u1 ≤ 1 := (a.property 0 0).2
    let w_mp := mkNoiseRank1 (-1) 1 (by norm_num) (by norm_num)
    let w_pm := mkNoiseRank1 1 (-1) (by norm_num) (by norm_num)
    let w_mm := mkNoiseRank1 (-1) (-1) (by norm_num) (by norm_num)
    let w_pp := mkNoiseRank1 1 1 (by norm_num) (by norm_num)
    let u2At : bridgeAdrGapData.NoiseBlock 1 → ℝ := fun wm =>
      (P.pol.rule (bridgeAdrGapData.observedDeviation wm)).val 0 0
    have hsyz : u2At w_mp + u2At w_pm = u2At w_mm + u2At w_pp := by
      have hmp := congrFun (P.is_separable (bridgeAdrGapData.observedDeviation w_mp) 0) 0
      have hpm := congrFun (P.is_separable (bridgeAdrGapData.observedDeviation w_pm) 0) 0
      have hmm := congrFun (P.is_separable (bridgeAdrGapData.observedDeviation w_mm) 0) 0
      have hpp := congrFun (P.is_separable (bridgeAdrGapData.observedDeviation w_pp) 0) 0
      have hd_mp0 : (bridgeAdrGapData.observedDeviation w_mp).val ⟨0, by decide⟩ = -1 := by
        change bridgeAdrGapData.deviation w_mp 0 = -1; rw [rank1_dev_eq]; rfl
      have hd_mp1 : (bridgeAdrGapData.observedDeviation w_mp).val ⟨1, by decide⟩ = 1 := by
        change bridgeAdrGapData.deviation w_mp 1 = 1; rw [rank1_dev_eq]; rfl
      have hd_pm0 : (bridgeAdrGapData.observedDeviation w_pm).val ⟨0, by decide⟩ = 1 := by
        change bridgeAdrGapData.deviation w_pm 0 = 1; rw [rank1_dev_eq]; rfl
      have hd_pm1 : (bridgeAdrGapData.observedDeviation w_pm).val ⟨1, by decide⟩ = -1 := by
        change bridgeAdrGapData.deviation w_pm 1 = -1; rw [rank1_dev_eq]; rfl
      have hd_mm0 : (bridgeAdrGapData.observedDeviation w_mm).val ⟨0, by decide⟩ = -1 := by
        change bridgeAdrGapData.deviation w_mm 0 = -1; rw [rank1_dev_eq]; rfl
      have hd_mm1 : (bridgeAdrGapData.observedDeviation w_mm).val ⟨1, by decide⟩ = -1 := by
        change bridgeAdrGapData.deviation w_mm 1 = -1; rw [rank1_dev_eq]; rfl
      have hd_pp0 : (bridgeAdrGapData.observedDeviation w_pp).val ⟨0, by decide⟩ = 1 := by
        change bridgeAdrGapData.deviation w_pp 0 = 1; rw [rank1_dev_eq]; rfl
      have hd_pp1 : (bridgeAdrGapData.observedDeviation w_pp).val ⟨1, by decide⟩ = 1 := by
        change bridgeAdrGapData.deviation w_pp 1 = 1; rw [rank1_dev_eq]; rfl
      change (P.pol.rule (bridgeAdrGapData.observedDeviation w_mp)).val 0 0 +
          (P.pol.rule (bridgeAdrGapData.observedDeviation w_pm)).val 0 0 =
        (P.pol.rule (bridgeAdrGapData.observedDeviation w_mm)).val 0 0 +
          (P.pol.rule (bridgeAdrGapData.observedDeviation w_pp)).val 0 0
      rw [hmp, hpm, hmm, hpp]
      simp only [Pi.add_apply, hd_mp0, hd_mp1, hd_pm0, hd_pm1, hd_mm0, hd_mm1, hd_pp0, hd_pp1]
      ring
    have hub_mm : u2At w_mm ≤ 1 :=
      ((P.pol.rule (bridgeAdrGapData.observedDeviation w_mm)).property 0 0).2
    have hlo_mp : (0 : ℝ) ≤ u1 + u2At w_mp - 2 := by
      have h := ((hbound (bridgeAdrGapData.observedDeviation w_mp) w_mm).1 0).1
      change (0 : ℝ) ≤ bridgeAdrGapData.expansion 1
        (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_mp)
        (P.pol.rule (bridgeAdrGapData.observedDeviation w_mp)).val w_mm.val 0 at h
      rw [rank1_term_eq] at h
      have h0 : w_mp.val 0 0 = -1 := rfl
      have h1 : w_mm.val 0 0 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hlo_pm : (0 : ℝ) ≤ u1 + u2At w_pm - 2 := by
      have h := ((hbound (bridgeAdrGapData.observedDeviation w_pm) w_mm).1 1).1
      change (0 : ℝ) ≤ bridgeAdrGapData.expansion 1
        (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pm)
        (P.pol.rule (bridgeAdrGapData.observedDeviation w_pm)).val w_mm.val 1 at h
      rw [rank1_term_eq] at h
      have h0 : w_pm.val 0 1 = -1 := rfl
      have h1 : w_mm.val 0 1 = -1 := rfl
      rw [h0, h1] at h; linarith
    have hcost_pp : 2 * u1 + 2 * u2At w_pp + 4 ≤ eta := by
      have h := (hbound (bridgeAdrGapData.observedDeviation w_pp) w_pp).2
      change bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pp)
          (P.pol.rule (bridgeAdrGapData.observedDeviation w_pp)).val w_pp.val 0 +
        bridgeAdrGapData.expansion 1
          (bridgeAdrGapData.nominal a + bridgeAdrGapData.deviation w_pp)
          (P.pol.rule (bridgeAdrGapData.observedDeviation w_pp)).val w_pp.val 1 ≤ eta at h
      rw [rank1_term_eq, rank1_term_eq] at h
      have h0 : w_pp.val 0 0 = 1 := rfl
      have h1 : w_pp.val 0 1 = 1 := rfl
      rw [h0, h1] at h; linarith
    linarith

/-! ## Section 4: O2 / O5 Sharp Positive Resolution — Single-Feature Diagonal-Hinge Restoration -/

/-- The 2D unit box `[-1, 1]^2`. -/
def unitBox2 : Set (Fin 2 → ℝ) :=
  {ξ | (-1 ≤ ξ 0 ∧ ξ 0 ≤ 1) ∧ (-1 ≤ ξ 1 ∧ ξ 1 ≤ 1)}

/-- Single scalar diagonal-hinge interaction feature `φ_diag(ξ) = |ξ_0 - ξ_1|`. -/
def diagLift2 : (Fin 2 → ℝ) → (Fin 1 → ℝ) :=
  fun ξ _ => |ξ 0 - ξ 1|

private def diagLinY {m : ℕ} (ymm ymp ypm ypp : Fin m → ℝ) :
    (Fin 2 → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun ξ :=
    ((1 / 4 : ℝ) * ξ 0) • (ypp - ymm + ypm - ymp) +
      ((1 / 4 : ℝ) * ξ 1) • (ypp - ymm + ymp - ypm)
  map_add' ξ₁ ξ₂ := by
    funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; ring
  map_smul' r ξ := by
    funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]; ring

private def diagLinZ {m : ℕ} (ymm ymp ypm ypp : Fin m → ℝ) :
    (Fin 1 → ℝ) →ₗ[ℝ] (Fin m → ℝ) where
  toFun ζ := ((1 / 4 : ℝ) * ζ 0) • (ymp + ypm - ymm - ypp)
  map_add' ζ₁ ζ₂ := by
    funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; ring
  map_smul' r ζ := by
    funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]; ring

/-- **Theorem O2.4 (Single-Feature Diagonal-Hinge Exactness on the 2D Box `[-1, 1]^2`):**
For EVERY fixed-recourse ARO problem `P` on the 2D box `[-1, 1]^2`, adding the SINGLE scalar
cross-coordinate interaction feature `φ_diag(ξ) = |ξ_0 - ξ_1|` restores 100% exactness:
`liftedAdrLevels P unitBox2 diagLift2 = aroLevels P unitBox2`.
The lifting coefficient `Z = (ymp + ypm - ymm - ypp) / 4` is literally `1/4` of the square
barycentric syzygy defect, and the resulting rule coincides with exact barycentric interpolation
on the Kuhn triangulation `{ξ_0 ≤ ξ_1} ∪ {ξ_1 ≤ ξ_0}`. -/
theorem diagonal_lifted_adr_exact_on_box2d {m k : ℕ} (P : FixedRecourseARO 2 m k) :
    liftedAdrLevels P unitBox2 diagLift2 = aroLevels P unitBox2 := by
  apply Set.Subset.antisymm (lifted_adr_hierarchy_and_affine_collapse P unitBox2 diagLift2).1.2
  intro eta haro
  let vmm : Fin 2 → ℝ := ![-1, -1]
  let vmp : Fin 2 → ℝ := ![-1, 1]
  let vpm : Fin 2 → ℝ := ![1, -1]
  let vpp : Fin 2 → ℝ := ![1, 1]
  have hvmm : vmm ∈ unitBox2 := by simp [unitBox2, vmm]
  have hvmp : vmp ∈ unitBox2 := by simp [unitBox2, vmp]
  have hvpm : vpm ∈ unitBox2 := by simp [unitBox2, vpm]
  have hvpp : vpp ∈ unitBox2 := by simp [unitBox2, vpp]
  obtain ⟨ymm, hymm_f, hymm_c⟩ := haro vmm hvmm
  obtain ⟨ymp, hymp_f, hymp_c⟩ := haro vmp hvmp
  obtain ⟨ypm, hypm_f, hypm_c⟩ := haro vpm hvpm
  obtain ⟨ypp, hypp_f, hypp_c⟩ := haro vpp hvpp
  let y0 : Fin m → ℝ := (1 / 2 : ℝ) • (ymm + ypp)
  refine ⟨y0, diagLinY ymm ymp ypm ypp, diagLinZ ymm ymp ypm ypp, ?_⟩
  intro ξ hξ
  rcases hξ with ⟨⟨h0l, h0u⟩, ⟨h1l, h1u⟩⟩
  by_cases hle : ξ 0 ≤ ξ 1
  · -- Triangle 1: ξ 0 ≤ ξ 1 => |ξ 0 - ξ 1| = ξ 1 - ξ 0
    have habs : |ξ 0 - ξ 1| = ξ 1 - ξ 0 := by rw [abs_of_nonpos (by linarith)]; ring
    let l1 : ℝ := (1 - ξ 1) / 2
    let l2 : ℝ := (ξ 1 - ξ 0) / 2
    let l3 : ℝ := (1 + ξ 0) / 2
    have hl1 : 0 ≤ l1 := by dsimp [l1]; linarith
    have hl2 : 0 ≤ l2 := by dsimp [l2]; linarith
    have hl3 : 0 ≤ l3 := by dsimp [l3]; linarith
    have hl_sum : l1 + l2 + l3 = 1 := by dsimp [l1, l2, l3]; ring
    have hy_eq : y0 + diagLinY ymm ymp ypm ypp ξ + diagLinZ ymm ymp ypm ypp (diagLift2 ξ) =
        l1 • ymm + l2 • ymp + l3 • ypp := by
      funext j
      simp only [y0, diagLinY, diagLinZ, diagLift2, LinearMap.coe_mk, AddHom.coe_mk,
        Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, habs, l1, l2, l3]
      ring
    have hξ_eq : ξ = l1 • vmm + l2 • vmp + l3 • vpp := by
      funext i; fin_cases i
      · simp [vmm, vmp, vpp, l1, l2, l3]; ring
      · simp [vmm, vmp, vpp, l1, l2, l3]; ring
    rw [hy_eq]
    constructor
    · intro i
      have hB : P.B (l1 • ymm + l2 • ymp + l3 • ypp) i =
          l1 * P.B ymm i + l2 * P.B ymp i + l3 * P.B ypp i := by
        simp [map_add, map_smul, smul_eq_mul]
      have hH : P.H ξ i = l1 * P.H vmm i + l2 * P.H vmp i + l3 * P.H vpp i := by
        conv_lhs => rw [hξ_eq]
        simp [map_add, map_smul, smul_eq_mul]
      rw [hB, hH]
      have c1 := mul_le_mul_of_nonneg_left (hymm_f i) hl1
      have c2 := mul_le_mul_of_nonneg_left (hymp_f i) hl2
      have c3 := mul_le_mul_of_nonneg_left (hypp_f i) hl3
      have hsum_h0 : (l1 + l2 + l3) * P.h0 i = P.h0 i := by rw [hl_sum, one_mul]
      linarith
    · have hc : P.c (l1 • ymm + l2 • ymp + l3 • ypp) =
          l1 * P.c ymm + l2 * P.c ymp + l3 * P.c ypp := by
        simp [map_add, map_smul, smul_eq_mul]
      rw [hc]
      have c1 := mul_le_mul_of_nonneg_left hymm_c hl1
      have c2 := mul_le_mul_of_nonneg_left hymp_c hl2
      have c3 := mul_le_mul_of_nonneg_left hypp_c hl3
      have hsum_e : (l1 + l2 + l3) * eta = eta := by rw [hl_sum, one_mul]
      linarith
  · -- Triangle 2: ξ 1 < ξ 0 => |ξ 0 - ξ 1| = ξ 0 - ξ 1
    have hgt : ξ 1 ≤ ξ 0 := le_of_not_ge hle
    have habs : |ξ 0 - ξ 1| = ξ 0 - ξ 1 := abs_of_nonneg (by linarith)
    let l1 : ℝ := (1 - ξ 0) / 2
    let l2 : ℝ := (ξ 0 - ξ 1) / 2
    let l3 : ℝ := (1 + ξ 1) / 2
    have hl1 : 0 ≤ l1 := by dsimp [l1]; linarith
    have hl2 : 0 ≤ l2 := by dsimp [l2]; linarith
    have hl3 : 0 ≤ l3 := by dsimp [l3]; linarith
    have hl_sum : l1 + l2 + l3 = 1 := by dsimp [l1, l2, l3]; ring
    have hy_eq : y0 + diagLinY ymm ymp ypm ypp ξ + diagLinZ ymm ymp ypm ypp (diagLift2 ξ) =
        l1 • ymm + l2 • ypm + l3 • ypp := by
      funext j
      simp only [y0, diagLinY, diagLinZ, diagLift2, LinearMap.coe_mk, AddHom.coe_mk,
        Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, habs, l1, l2, l3]
      ring
    have hξ_eq : ξ = l1 • vmm + l2 • vpm + l3 • vpp := by
      funext i; fin_cases i
      · simp [vmm, vpm, vpp, l1, l2, l3]; ring
      · simp [vmm, vpm, vpp, l1, l2, l3]; ring
    rw [hy_eq]
    constructor
    · intro i
      have hB : P.B (l1 • ymm + l2 • ypm + l3 • ypp) i =
          l1 * P.B ymm i + l2 * P.B ypm i + l3 * P.B ypp i := by
        simp [map_add, map_smul, smul_eq_mul]
      have hH : P.H ξ i = l1 * P.H vmm i + l2 * P.H vpm i + l3 * P.H vpp i := by
        conv_lhs => rw [hξ_eq]
        simp [map_add, map_smul, smul_eq_mul]
      rw [hB, hH]
      have c1 := mul_le_mul_of_nonneg_left (hymm_f i) hl1
      have c2 := mul_le_mul_of_nonneg_left (hypm_f i) hl2
      have c3 := mul_le_mul_of_nonneg_left (hypp_f i) hl3
      have hsum_h0 : (l1 + l2 + l3) * P.h0 i = P.h0 i := by rw [hl_sum, one_mul]
      linarith
    · have hc : P.c (l1 • ymm + l2 • ypm + l3 • ypp) =
          l1 * P.c ymm + l2 * P.c ypm + l3 * P.c ypp := by
        simp [map_add, map_smul, smul_eq_mul]
      rw [hc]
      have c1 := mul_le_mul_of_nonneg_left hymm_c hl1
      have c2 := mul_le_mul_of_nonneg_left hypm_c hl2
      have c3 := mul_le_mul_of_nonneg_left hypp_c hl3
      have hsum_e : (l1 + l2 + l3) * eta = eta := by rw [hl_sum, one_mul]
      linarith

/-- Borel-measurable single-feature diagonal-hinge lifted affine deviation policy on 2D frozen `Data`:
`u_2(ξ)_t = b0_t + K_t ξ + |w0 * ξ_0 - w1 * ξ_1| • z_t`. -/
structure DiagLiftedDeviationPolicy (D : Data) (hn : D.n = 2) where
  b0 : Fin D.q → Vec D.m
  K : Fin D.q → (Vec D.n →ₗ[ℝ] Vec D.m)
  z : Fin D.q → Vec D.m
  w0 : ℝ
  w1 : ℝ
  in_box : ∀ (xi : D.Z) (t : Fin D.q) (j : Fin D.m),
    D.umin j ≤ (b0 t + K t xi.val + |w0 * xi.val ⟨0, by omega⟩ - w1 * xi.val ⟨1, by omega⟩| • z t) j ∧
    (b0 t + K t xi.val + |w0 * xi.val ⟨0, by omega⟩ - w1 * xi.val ⟨1, by omega⟩| • z t) j ≤ D.umax j

private theorem lin_vec_cont {n m : ℕ} (L : Vec n →ₗ[ℝ] Vec m) : Continuous L := by
  refine continuous_pi (fun j => ?_)
  have hform : (fun v : Vec n => L v j) =
      fun v => ∑ i : Fin n, v i * L (Pi.single i (1 : ℝ)) j := by
    funext v
    have hv : v = ∑ i : Fin n, v i • Pi.single i (1 : ℝ) := by
      funext r; simp [Finset.sum_apply, Pi.smul_apply, Pi.single_apply]
    conv_lhs => rw [hv, map_sum]
    simp [Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
  rw [hform]
  exact continuous_finsetSum _ (fun i _ => (continuous_apply i).mul continuous_const)

/-- Every `DiagLiftedDeviationPolicy` is continuous, hence a valid Borel-measurable `D.DeviationPolicy`. -/
def DiagLiftedDeviationPolicy.toDeviationPolicy {D : Data} {hn : D.n = 2}
    (P : DiagLiftedDeviationPolicy D hn) : D.DeviationPolicy where
  rule xi := ⟨fun t => P.b0 t + P.K t xi.val +
    |P.w0 * xi.val ⟨0, by omega⟩ - P.w1 * xi.val ⟨1, by omega⟩| • P.z t, P.in_box xi⟩
  borel := by
    have hcont : Continuous (fun xi : D.Z => (⟨fun t => P.b0 t + P.K t xi.val +
        |P.w0 * xi.val ⟨0, by omega⟩ - P.w1 * xi.val ⟨1, by omega⟩| • P.z t, P.in_box xi⟩ :
        D.ControlBlock D.q)) := by
      refine Continuous.subtype_mk (continuous_pi fun t => ?_) _
      have haff : Continuous (fun xi : D.Z => P.b0 t + P.K t xi.val) :=
        continuous_const.add ((lin_vec_cont (P.K t)).comp continuous_subtype_val)
      have hhinge : Continuous (fun xi : D.Z =>
          |P.w0 * xi.val ⟨0, by omega⟩ - P.w1 * xi.val ⟨1, by omega⟩|) :=
        ((continuous_const.mul ((continuous_apply (⟨0, by omega⟩ : Fin D.n)).comp continuous_subtype_val)).sub
          (continuous_const.mul ((continuous_apply (⟨1, by omega⟩ : Fin D.n)).comp continuous_subtype_val))).abs
      exact haff.add (hhinge.smul continuous_const)
    exact hcont.measurable

/-- Epigraph level set achievable by single-feature diagonal-hinge lifted ADR on 2D frozen `Data`. -/
def bridgeDiagLiftedAdrLevels (D : Data) (hn : D.n = 2) : Set ℝ :=
  {eta | ∃ (a : D.ControlBlock D.r) (P : DiagLiftedDeviationPolicy D hn),
    D.AROBound a P.toDeviationPolicy eta}

private theorem convex_comb_three_ineq {n : ℕ} (l1 l2 l3 : ℝ)
    (h1 : 0 ≤ l1) (h2 : 0 ≤ l2) (h3 : 0 ≤ l3) (hsum : l1 + l2 + l3 = 1)
    (row : Vec n →ₗ[ℝ] ℝ) (z1 z2 z3 : Vec n) (s bound : ℝ)
    (hz1 : row z1 + s ≤ bound) (hz2 : row z2 + s ≤ bound) (hz3 : row z3 + s ≤ bound) :
    row (l1 • z1 + l2 • z2 + l3 • z3) + s ≤ bound := by
  simp only [map_add, map_smul, smul_eq_mul]
  have c1 := mul_le_mul_of_nonneg_left hz1 h1
  have c2 := mul_le_mul_of_nonneg_left hz2 h2
  have c3 := mul_le_mul_of_nonneg_left hz3 h3
  have hs : (l1 + l2 + l3) * s = s := by rw [hsum, one_mul]
  have hb : (l1 + l2 + l3) * bound = bound := by rw [hsum, one_mul]
  linarith

/-- **Theorem O2.5 (Single-Feature Diagonal-Hinge Exactness Inside Frozen `BridgeFormalV2.Data`):**
For EVERY 2D frozen `BridgeFormalV2.Data` instance (`hn : D.n = 2`) whose exogenous deviation set
`D.Z` is a rectangular box `[-r0, r0] × [-r1, r1]` (`r0 > 0, r1 > 0`) — with completely arbitrary
horizons `r, q`, recourse `B`, terminal constraints `H, g_min, g_max`, and cost `c` (in particular
covering both `bridgeAdrGapData` and `bridgeFullRankShearData`) — Borel-measurable single-feature
diagonal-hinge lifted ADR is ALWAYS exact:
`bridgeDiagLiftedAdrLevels D hn = D.aroLevels ∧ bridgeDiagLiftedAdrLevels D hn = D.sourceLevels`. -/
theorem bridge_diagonal_lifted_adr_exact_2d_box (D : Data) (hn : D.n = 2)
    (r0 r1 : ℝ) (hr0 : 0 < r0) (hr1 : 0 < r1)
    (hZ : ∀ v : Vec D.n, v ∈ D.Z ↔
      (-r0 ≤ v ⟨0, by omega⟩ ∧ v ⟨0, by omega⟩ ≤ r0) ∧
      (-r1 ≤ v ⟨1, by omega⟩ ∧ v ⟨1, by omega⟩ ≤ r1)) :
    bridgeDiagLiftedAdrLevels D hn = D.aroLevels ∧
      bridgeDiagLiftedAdrLevels D hn = D.sourceLevels := by
  have hsub : bridgeDiagLiftedAdrLevels D hn ⊆ D.aroLevels := by
    intro eta ⟨a, P, hbound⟩
    exact ⟨a, P.toDeviationPolicy, hbound⟩
  have heq_aro : bridgeDiagLiftedAdrLevels D hn = D.aroLevels := by
    apply Set.Subset.antisymm hsub
    intro eta ⟨a, y, hy⟩
    have hy_tight := (BridgeFormalV3.Proofs.exact_tightening D a y eta).mp hy
    let i0 : Fin D.n := ⟨0, by omega⟩
    let i1 : Fin D.n := ⟨1, by omega⟩
    have hfin_cases : ∀ i : Fin D.n, i = i0 ∨ i = i1 := by
      intro i
      have hi : i.val < 2 := hn ▸ i.isLt
      by_cases h0 : i.val = 0
      · left; exact Fin.ext h0
      · right; exact Fin.ext (show i.val = 1 by omega)
    let mkV : ℝ → ℝ → Vec D.n := fun x0 x1 i => if i = i0 then x0 else x1
    have hmk0 : ∀ x0 x1, mkV x0 x1 i0 = x0 := fun _ _ => by simp [mkV]
    have hmk1 : ∀ x0 x1, mkV x0 x1 i1 = x1 := fun _ _ => by
      have hne : i1 ≠ i0 := by intro h; have := congrArg Fin.val h; simp [i0, i1] at this
      simp [mkV, hne]
    let vmm : D.Z := ⟨mkV (-r0) (-r1), (hZ _).mpr ⟨⟨by rw [hmk0], by rw [hmk0]; linarith⟩,
      ⟨by rw [hmk1], by rw [hmk1]; linarith⟩⟩⟩
    let vmp : D.Z := ⟨mkV (-r0) r1, (hZ _).mpr ⟨⟨by rw [hmk0], by rw [hmk0]; linarith⟩,
      ⟨by rw [hmk1]; linarith, by rw [hmk1]⟩⟩⟩
    let vpm : D.Z := ⟨mkV r0 (-r1), (hZ _).mpr ⟨⟨by rw [hmk0]; linarith, by rw [hmk0]⟩,
      ⟨by rw [hmk1], by rw [hmk1]; linarith⟩⟩⟩
    let vpp : D.Z := ⟨mkV r0 r1, (hZ _).mpr ⟨⟨by rw [hmk0]; linarith, by rw [hmk0]⟩,
      ⟨by rw [hmk1]; linarith, by rw [hmk1]⟩⟩⟩
    let bmm := y.rule vmm
    let bmp := y.rule vmp
    let bpm := y.rule vpm
    let bpp := y.rule vpp
    let b0Fun : Fin D.q → Vec D.m := fun t => (1 / 2 : ℝ) • (bmm.val t + bpp.val t)
    let KFun : Fin D.q → (Vec D.n →ₗ[ℝ] Vec D.m) := fun t =>
      { toFun := fun v =>
          ((1 / 4 : ℝ) * (v i0 / r0)) • (bpp.val t - bmm.val t + bpm.val t - bmp.val t) +
            ((1 / 4 : ℝ) * (v i1 / r1)) • (bpp.val t - bmm.val t + bmp.val t - bpm.val t)
        map_add' := fun u v => by
          funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul]; ring
        map_smul' := fun r u => by
          funext j; simp only [Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, RingHom.id_apply]; ring }
    let zFun : Fin D.q → Vec D.m := fun t =>
      (1 / 4 : ℝ) • (bmp.val t + bpm.val t - bmm.val t - bpp.val t)
    have hr0_ne : r0 ≠ 0 := ne_of_gt hr0
    have hr1_ne : r1 ≠ 0 := ne_of_gt hr1
    -- Helper: normalized coordinates u0 = xi 0 / r0, u1 = xi 1 / r1 ∈ [-1, 1]
    have hnorm : ∀ xi : D.Z, (-1 ≤ xi.val i0 / r0 ∧ xi.val i0 / r0 ≤ 1) ∧
        (-1 ≤ xi.val i1 / r1 ∧ xi.val i1 / r1 ≤ 1) := by
      intro xi
      have hb := (hZ xi.val).mp xi.property
      constructor
      · constructor
        · rw [le_div_iff₀ hr0]; linarith
        · rw [div_le_iff₀ hr0]; linarith
      · constructor
        · rw [le_div_iff₀ hr1]; linarith
        · rw [div_le_iff₀ hr1]; linarith
    have heval_tri1 : ∀ (xi : D.Z) (t : Fin D.q), xi.val i0 / r0 ≤ xi.val i1 / r1 →
        b0Fun t + KFun t xi.val + |r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1| • zFun t =
          ((1 - xi.val i1 / r1) / 2) • bmm.val t +
            ((xi.val i1 / r1 - xi.val i0 / r0) / 2) • bmp.val t +
            ((1 + xi.val i0 / r0) / 2) • bpp.val t := by
      intro xi t hle
      have habs : |r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1| = xi.val i1 / r1 - xi.val i0 / r0 := by
        have hrew : r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1 = xi.val i0 / r0 - xi.val i1 / r1 := by
          simp only [div_eq_inv_mul]
        rw [hrew, abs_of_nonpos (by linarith)]; ring
      funext j
      simp only [b0Fun, KFun, zFun, LinearMap.coe_mk, AddHom.coe_mk,
        Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, habs]
      ring
    have heval_tri2 : ∀ (xi : D.Z) (t : Fin D.q), xi.val i1 / r1 ≤ xi.val i0 / r0 →
        b0Fun t + KFun t xi.val + |r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1| • zFun t =
          ((1 - xi.val i0 / r0) / 2) • bmm.val t +
            ((xi.val i0 / r0 - xi.val i1 / r1) / 2) • bpm.val t +
            ((1 + xi.val i1 / r1) / 2) • bpp.val t := by
      intro xi t hge
      have habs : |r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1| = xi.val i0 / r0 - xi.val i1 / r1 := by
        have hrew : r0⁻¹ * xi.val i0 - r1⁻¹ * xi.val i1 = xi.val i0 / r0 - xi.val i1 / r1 := by
          simp only [div_eq_inv_mul]
        rw [hrew, abs_of_nonneg (by linarith)]
      funext j
      simp only [b0Fun, KFun, zFun, LinearMap.coe_mk, AddHom.coe_mk,
        Pi.add_apply, Pi.sub_apply, Pi.smul_apply, smul_eq_mul, habs]
      ring
    let P : DiagLiftedDeviationPolicy D hn :=
      { b0 := b0Fun
        K := KFun
        z := zFun
        w0 := r0⁻¹
        w1 := r1⁻¹
        in_box := fun xi t j => by
          rcases hnorm xi with ⟨⟨h0l, h0u⟩, ⟨h1l, h1u⟩⟩
          by_cases hle : xi.val i0 / r0 ≤ xi.val i1 / r1
          · rw [heval_tri1 xi t hle]
            simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
            have hmm := bmm.property t j
            have hmp := bmp.property t j
            have hpp := bpp.property t j
            constructor <;> nlinarith
          · have hge : xi.val i1 / r1 ≤ xi.val i0 / r0 := le_of_not_ge hle
            rw [heval_tri2 xi t hge]
            simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul]
            have hmm := bmm.property t j
            have hpm := bpm.property t j
            have hpp := bpp.property t j
            constructor <;> nlinarith }
    refine ⟨a, P, (BridgeFormalV3.Proofs.exact_tightening D a P.toDeviationPolicy eta).mpr ?_⟩
    intro xi
    rcases hnorm xi with ⟨⟨h0l, h0u⟩, ⟨h1l, h1u⟩⟩
    by_cases hle : xi.val i0 / r0 ≤ xi.val i1 / r1
    · let l1 : ℝ := (1 - xi.val i1 / r1) / 2
      let l2 : ℝ := (xi.val i1 / r1 - xi.val i0 / r0) / 2
      let l3 : ℝ := (1 + xi.val i0 / r0) / 2
      have hl1 : 0 ≤ l1 := by dsimp [l1]; linarith
      have hl2 : 0 ≤ l2 := by dsimp [l2]; linarith
      have hl3 : 0 ≤ l3 := by dsimp [l3]; linarith
      have hl_sum : l1 + l2 + l3 = 1 := by dsimp [l1, l2, l3]; ring
      have hxi_conv : xi.val = l1 • vmm.val + l2 • vmp.val + l3 • vpp.val := by
        funext i
        rcases hfin_cases i with rfl | rfl
        · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, vmm, vmp, vpp, hmk0, l1, l2, l3]
          field_simp [hr0_ne, hr1_ne]; ring
        · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, vmm, vmp, vpp, hmk1, l1, l2, l3]
          field_simp [hr0_ne, hr1_ne]; ring
      have hnom_conv : D.aroNominalTerminal a P.toDeviationPolicy xi =
          l1 • D.aroNominalTerminal a y vmm +
            l2 • D.aroNominalTerminal a y vmp +
            l3 • D.aroNominalTerminal a y vpp := by
        simp only [Data.aroNominalTerminal, Data.expansion, Pi.zero_apply, map_zero, add_zero]
        have ha_split : D.nominal a = l1 • D.nominal a + l2 • D.nominal a + l3 • D.nominal a := by
          rw [← add_smul, ← add_smul, hl_sum, one_smul]
        have hctrl : ∀ t : Fin D.q, (P.toDeviationPolicy.rule xi).val t =
            l1 • bmm.val t + l2 • bmp.val t + l3 • bpp.val t :=
          fun t => heval_tri1 xi t hle
        conv_lhs => rw [ha_split, hxi_conv]
        simp_rw [hctrl, map_add, map_smul, Finset.sum_add_distrib, ← Finset.smul_sum, smul_add]
        abel
      rw [hnom_conv]
      constructor
      · intro i
        constructor
        · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum (-(D.terminalRow i)) _ _ _ _ _
            ((hy_tight vmm).1 i).1 ((hy_tight vmp).1 i).1 ((hy_tight vpp).1 i).1
        · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum (D.terminalRow i) _ _ _ _ _
            ((hy_tight vmm).1 i).2 ((hy_tight vmp).1 i).2 ((hy_tight vpp).1 i).2
      · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum D.c _ _ _ _ _
          (hy_tight vmm).2 (hy_tight vmp).2 (hy_tight vpp).2
    · have hge : xi.val i1 / r1 ≤ xi.val i0 / r0 := le_of_not_ge hle
      let l1 : ℝ := (1 - xi.val i0 / r0) / 2
      let l2 : ℝ := (xi.val i0 / r0 - xi.val i1 / r1) / 2
      let l3 : ℝ := (1 + xi.val i1 / r1) / 2
      have hl1 : 0 ≤ l1 := by dsimp [l1]; linarith
      have hl2 : 0 ≤ l2 := by dsimp [l2]; linarith
      have hl3 : 0 ≤ l3 := by dsimp [l3]; linarith
      have hl_sum : l1 + l2 + l3 = 1 := by dsimp [l1, l2, l3]; ring
      have hxi_conv : xi.val = l1 • vmm.val + l2 • vpm.val + l3 • vpp.val := by
        funext i
        rcases hfin_cases i with rfl | rfl
        · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, vmm, vpm, vpp, hmk0, l1, l2, l3]
          field_simp [hr0_ne, hr1_ne]; ring
        · simp only [Pi.add_apply, Pi.smul_apply, smul_eq_mul, vmm, vpm, vpp, hmk1, l1, l2, l3]
          field_simp [hr0_ne, hr1_ne]; ring
      have hnom_conv : D.aroNominalTerminal a P.toDeviationPolicy xi =
          l1 • D.aroNominalTerminal a y vmm +
            l2 • D.aroNominalTerminal a y vpm +
            l3 • D.aroNominalTerminal a y vpp := by
        simp only [Data.aroNominalTerminal, Data.expansion, Pi.zero_apply, map_zero, add_zero]
        have ha_split : D.nominal a = l1 • D.nominal a + l2 • D.nominal a + l3 • D.nominal a := by
          rw [← add_smul, ← add_smul, hl_sum, one_smul]
        have hctrl : ∀ t : Fin D.q, (P.toDeviationPolicy.rule xi).val t =
            l1 • bmm.val t + l2 • bpm.val t + l3 • bpp.val t :=
          fun t => heval_tri2 xi t hge
        conv_lhs => rw [ha_split, hxi_conv]
        simp_rw [hctrl, map_add, map_smul, Finset.sum_add_distrib, ← Finset.smul_sum, smul_add]
        abel
      rw [hnom_conv]
      constructor
      · intro i
        constructor
        · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum (-(D.terminalRow i)) _ _ _ _ _
            ((hy_tight vmm).1 i).1 ((hy_tight vpm).1 i).1 ((hy_tight vpp).1 i).1
        · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum (D.terminalRow i) _ _ _ _ _
            ((hy_tight vmm).1 i).2 ((hy_tight vpm).1 i).2 ((hy_tight vpp).1 i).2
      · exact convex_comb_three_ineq l1 l2 l3 hl1 hl2 hl3 hl_sum D.c _ _ _ _ _
          (hy_tight vmm).2 (hy_tight vpm).2 (hy_tight vpp).2
  refine ⟨heq_aro, ?_⟩
  rw [heq_aro, BridgeFormalV2.Proofs.epigraph_equality D]

end AroProofs.BridgeO2LiftedADR
