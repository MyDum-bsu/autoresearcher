import BridgeFormalV3.Proofs.Support
import AroProofs.BridgeF4CornerLP
import AroProofs.BridgeO4ClosureValue
import AroProofs.BridgeO1ADRExactness

/-!
# Cycle 03 — O1 / O2 / O5 & F3: Full-Rank Recourse Refutation (`H-O1-1`),
Arbitrary-Dimension Diagonal ADR Exactness, F3 Support Subadditivity, and
Linear `Ω(n)` Affine Gap Scaling on Frozen `BridgeFormalV2.Data`

Built strictly over frozen `BridgeFormalV2.Model` / `BridgeFormalV2.Goals`,
F3 `BridgeFormalV3.Proofs.Support`, F4 `BridgeF4CornerLP`, O4 `BridgeO4ClosureValue`,
and O1 `BridgeO1ADRExactness`. Zero `sorry`, zero custom axioms.

Main theorems (8 declarations):
  A. F3 Support-Function Convexity Properties:
     1. `futureRowSupport_nonneg`: `0 ≤ D.futureRowSupport row`.
     2. `futureRowSupport_neg`: `D.futureRowSupport (-row) = D.futureRowSupport row`.
     3. `futureRowSupport_add_le`: Subadditivity `h(row₁ + row₂) ≤ h(row₁) + h(row₂)`.
  B. O5 Necessary Condition (Unconstrained Terminal Collapse):
     4. `bridge_adr_exact_of_unconstrained_terminal`: `D.rows = 0 → bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`.
  C. O1 Sharp Positive Boundary (Arbitrary-Dimension Coordinatewise Diagonal Exactness):
     5. `bridge_adr_exact_diagonal`: For EVERY frozen `D : BridgeFormalV2.Data` with diagonal
        `(A, B, E, H)` (arbitrary dimension `n ≥ 1`, arbitrary horizons `r, q ≥ 1`, arbitrary
        linear cost `c` and bounds `u_min, u_max, g_min, g_max, rho > 0`),
        `bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`.
  D. O1 / O5 Refutation of `H-O1-1` (Invertible Unimodular Shear Counterexample):
     6. `shearRecourse_bijective`: `Function.Bijective bridgeFullRankShearData.B` (`det B = 1`).
     7. `exists_bridge_2d_fullrank_invertible_strict_adr_gap`: Even with `A = E = H = I_2`
        and bijective unimodular `B = [[1, 1], [0, 1]]`, `5 ∈ D.aroLevels ∩ D.sourceLevels`
        whereas `∀ eta ∈ bridgeAdrLevels D, 6 ≤ eta` (strict gap `≥ 1`, ratio `≥ 6/5`).
  E. O2 Quantitative Scaling (Linear `Ω(n)` Affine Gap Inside Frozen `BridgeFormalV2.Data`):
     8. `exists_bridge_linear_adr_gap_scaling`: For every `k ≥ 1`, there exists `D : Data` with
        `D.n = 2 * k`, `6 * k ∈ D.aroLevels ∩ D.sourceLevels`, and `∀ eta ∈ bridgeAdrLevels D, 8 * k ≤ eta`
        (additive gap `≥ 2k = n`, ratio `≥ 4/3`).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 AroProofs.BridgeF4VertexLP
  AroProofs.BridgeO4ClosureValue AroProofs.BridgeO1ADRExactness MeasureTheory Set

namespace AroProofs.BridgeO1FullRankRecourse

/-! ## Section 1: F3 Support-Function Convexity Properties -/

/-- **Theorem F3.5:** The F3 future-noise support functional is always nonnegative. -/
theorem futureRowSupport_nonneg (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ) :
    0 ≤ D.futureRowSupport row := by
  unfold Data.futureRowSupport
  exact mul_nonneg (le_of_lt D.rho_pos)
    (Finset.sum_nonneg fun _ _ => Finset.sum_nonneg fun _ _ => abs_nonneg _)

/-- **Theorem F3.6:** The F3 future-noise support functional is symmetric: `h(-row) = h(row)`. -/
theorem futureRowSupport_neg (D : Data) (row : Vec D.n →ₗ[ℝ] ℝ) :
    D.futureRowSupport (-row) = D.futureRowSupport row := by
  simp [Data.futureRowSupport, abs_neg]

/-- **Theorem F3.7:** The F3 future-noise support functional is subadditive:
`h(row₁ + row₂) ≤ h(row₁) + h(row₂)`. -/
theorem futureRowSupport_add_le (D : Data) (row₁ row₂ : Vec D.n →ₗ[ℝ] ℝ) :
    D.futureRowSupport (row₁ + row₂) ≤ D.futureRowSupport row₁ + D.futureRowSupport row₂ := by
  simp only [Data.futureRowSupport, LinearMap.add_apply]
  rw [← mul_add, ← Finset.sum_add_distrib]
  apply mul_le_mul_of_nonneg_left _ (le_of_lt D.rho_pos)
  apply Finset.sum_le_sum
  intro t _
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_le_sum
  intro i _
  exact abs_add_le _ _

/-! ## Section 2: O5 Necessary Condition — Unconstrained Terminal Collapse -/

/-- **Theorem O5.1:** When `D.rows = 0` (no terminal state constraints), affine decision rules
are ALWAYS exact on frozen `BridgeFormalV2.Data` (in fact open-loop is already optimal). -/
theorem bridge_adr_exact_of_unconstrained_terminal (D : Data) (hrows : D.rows = 0) :
    bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels := by
  have hol_sub_adr : openLoopLevels D ⊆ bridgeAdrLevels D := by
    rintro eta ⟨a, b, hb⟩
    let P : AffineDeviationPolicy D :=
      { b0 := b.val
        K := fun _ => 0
        in_box := fun _ t j => by simpa only [LinearMap.zero_apply, add_zero] using b.property t j }
    refine ⟨a, P, ?_⟩
    have hpol : P.toDeviationPolicy = constPolicy D b := by
      simp only [AffineDeviationPolicy.toDeviationPolicy, constPolicy, P]
      congr 1
      funext xi
      apply Subtype.ext
      funext t
      simp
    rwa [hpol]
  have hzero := zero_gain_of_unconstrained_terminal D hrows
  have hsub := bridge_adr_subset_aro_and_source D
  have heq_aro : bridgeAdrLevels D = D.aroLevels :=
    Set.Subset.antisymm hsub.1 (by rw [hzero.1]; exact hol_sub_adr)
  refine ⟨heq_aro, ?_⟩
  rw [heq_aro, BridgeFormalV2.Proofs.epigraph_equality D]

/-! ## Section 3: O1 Positive Boundary — Arbitrary-Dimension Diagonal Exactness -/

/-- Structure certifying that a frozen `BridgeFormalV2.Data` instance is coordinatewise
decoupled (`n = m = p = rows` and `A, B, E, H` act diagonally in the standard basis),
with completely arbitrary horizons `r, q`, cost `c`, and box bounds. -/
structure DiagonalBridgeData (D : Data) where
  hm : D.m = D.n
  hp : D.p = D.n
  hrows : D.rows = D.n
  aDiag : Fin D.n → ℝ
  bDiag : Fin D.n → ℝ
  eDiag : Fin D.n → ℝ
  hDiag : Fin D.n → ℝ
  hA : ∀ (x : Vec D.n) (i : Fin D.n), D.A x i = aDiag i * x i
  hB : ∀ (u : Vec D.m) (i : Fin D.n), D.B u i = bDiag i * u (Fin.cast hm.symm i)
  hE : ∀ (w : Vec D.p) (i : Fin D.n), D.E w i = eDiag i * w (Fin.cast hp.symm i)
  hH : ∀ (x : Vec D.n) (r : Fin D.rows), D.H x r = hDiag (Fin.cast hrows r) * x (Fin.cast hrows r)

private theorem diag_pow_apply {D : Data} (diag : DiagonalBridgeData D) :
    ∀ (k : ℕ) (x : Vec D.n) (i : Fin D.n), (D.A ^ k) x i = (diag.aDiag i) ^ k * x i := by
  intro k
  induction k with
  | zero =>
      intro x i
      simp
  | succ k ih =>
      intro x i
      rw [pow_succ', Module.End.mul_apply, diag.hA, ih]
      ring

private theorem diag_expansion_apply {D : Data} (diag : DiagonalBridgeData D)
    (k : ℕ) (x : Vec D.n) (u : Block k D.m) (w : Block k D.p) (i : Fin D.n) :
    D.expansion k x u w i =
      (diag.aDiag i) ^ k * x i +
        ∑ t : Fin k, (diag.aDiag i) ^ (k - 1 - t.val) *
          (diag.bDiag i * u t (Fin.cast diag.hm.symm i) +
            diag.eDiag i * w t (Fin.cast diag.hp.symm i)) := by
  simp only [Data.expansion, Pi.add_apply, Finset.sum_apply, diag_pow_apply diag,
    diag.hB, diag.hE]

private theorem diag_deviation_apply {D : Data} (diag : DiagonalBridgeData D)
    (w : D.NoiseBlock D.r) (i : Fin D.n) :
    D.deviation w i =
      ∑ t : Fin D.r, (diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i *
        w.val t (Fin.cast diag.hp.symm i) := by
  have hdev : D.deviation w = D.expansion D.r 0 (fun _ => 0) w.val := by
    have hz : blockAt (fun _ : Fin D.r => (0 : Vec D.m)) = (fun _ => 0) := by
      funext t; simp [blockAt]
    simpa only [hz, Data.deviation] using BridgeFormalV2.Proofs.expansion D D.r 0 (fun _ => 0) w.val
  rw [hdev, diag_expansion_apply diag]
  simp only [Pi.zero_apply, mul_zero, zero_add]
  apply Finset.sum_congr rfl
  intro t _
  ring

private def diagRadius {D : Data} (diag : DiagonalBridgeData D) (i : Fin D.n) : ℝ :=
  D.rho * ∑ t : Fin D.r, |(diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i|

private theorem diagRadius_nonneg {D : Data} (diag : DiagonalBridgeData D) (i : Fin D.n) :
    0 ≤ diagRadius diag i :=
  mul_nonneg (le_of_lt D.rho_pos) (Finset.sum_nonneg fun _ _ => abs_nonneg _)

private theorem diag_deviation_bounds {D : Data} (diag : DiagonalBridgeData D)
    (w : D.NoiseBlock D.r) (i : Fin D.n) :
    -diagRadius diag i ≤ D.deviation w i ∧ D.deviation w i ≤ diagRadius diag i := by
  rw [diag_deviation_apply diag w i]
  unfold diagRadius
  rw [Finset.mul_sum, ← Finset.sum_neg_distrib]
  constructor
  · apply Finset.sum_le_sum
    intro t _
    have hw := w.property t (Fin.cast diag.hp.symm i)
    have h := BridgeFormalV3.Proofs.coefficient_bound D
      (-((diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i))
      (w.val t (Fin.cast diag.hp.symm i)) hw
    rw [abs_neg] at h
    linarith
  · apply Finset.sum_le_sum
    intro t _
    exact BridgeFormalV3.Proofs.coefficient_bound D
      ((diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i)
      (w.val t (Fin.cast diag.hp.symm i)) (w.property t (Fin.cast diag.hp.symm i))

private def cornerOfSigns {D : Data} (diag : DiagonalBridgeData D) (s : Fin D.n → Bool) :
    Corner D :=
  fun k =>
    let tj := finProdFinEquiv.symm k
    let t : Fin D.r := tj.1
    let j : Fin D.p := tj.2
    let i : Fin D.n := Fin.cast diag.hp j
    let coeff : ℝ := (diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i
    if s i then decide (0 ≤ coeff) else decide (coeff < 0)

private theorem deviation_cornerOfSigns {D : Data} (diag : DiagonalBridgeData D)
    (s : Fin D.n → Bool) (i : Fin D.n) :
    D.deviation (cornerNoise D (cornerOfSigns diag s)) i =
      if s i then diagRadius diag i else -diagRadius diag i := by
  rw [diag_deviation_apply diag]
  unfold diagRadius
  by_cases hs : s i = true
  · simp only [hs, ↓reduceIte, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro t _
    have hcast : Fin.cast diag.hp (Fin.cast diag.hp.symm i) = i := by ext; rfl
    have hval : (cornerNoise D (cornerOfSigns diag s)).val t (Fin.cast diag.hp.symm i) =
        if 0 ≤ (diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i then D.rho else -D.rho := by
      change cornerCoord D.rho (cornerOfSigns diag s (finProdFinEquiv (t, Fin.cast diag.hp.symm i))) = _
      unfold cornerOfSigns
      rw [Equiv.symm_apply_apply]
      dsimp only
      rw [hcast, hs]
      simp only [↓reduceIte, cornerCoord, decide_eq_true_eq]
    rw [hval]
    split_ifs with hc
    · rw [abs_of_nonneg hc, mul_comm]
    · rw [abs_of_neg (lt_of_not_ge hc)]; ring
  · have hsf : s i = false := Bool.eq_false_iff.mpr hs
    simp only [hsf, Bool.false_eq_true, ↓reduceIte, Finset.mul_sum, ← Finset.sum_neg_distrib]
    apply Finset.sum_congr rfl
    intro t _
    have hcast : Fin.cast diag.hp (Fin.cast diag.hp.symm i) = i := by ext; rfl
    have hval : (cornerNoise D (cornerOfSigns diag s)).val t (Fin.cast diag.hp.symm i) =
        if (diag.aDiag i) ^ (D.r - 1 - t.val) * diag.eDiag i < 0 then D.rho else -D.rho := by
      change cornerCoord D.rho (cornerOfSigns diag s (finProdFinEquiv (t, Fin.cast diag.hp.symm i))) = _
      unfold cornerOfSigns
      rw [Equiv.symm_apply_apply]
      dsimp only
      rw [hcast, hsf]
      simp only [Bool.false_eq_true, ↓reduceIte, cornerCoord, decide_eq_true_eq]
    rw [hval]
    split_ifs with hc
    · rw [abs_of_neg hc]; ring
    · rw [abs_of_nonneg (le_of_not_gt hc)]; ring

private theorem linearMap_decompose_coord {n : ℕ} (f : Vec n →ₗ[ℝ] ℝ) (x : Vec n) :
    f x = ∑ i : Fin n, f (Pi.single i (1 : ℝ)) * x i := by
  have hx : x = ∑ i : Fin n, x i • Pi.single i (1 : ℝ) := by
    funext j; simp [Finset.sum_apply, Pi.smul_apply, Pi.single_apply]
  conv_lhs => rw [hx, map_sum]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_smul, smul_eq_mul, mul_comm]

/-- **Theorem O1.8 (Arbitrary-Dimension Diagonal Bridge ADR Exactness):**
For EVERY frozen `D : BridgeFormalV2.Data` that is coordinatewise decoupled (`DiagonalBridgeData D`)
— arbitrary state dimension `n ≥ 1`, arbitrary horizons `r, q ≥ 1`, arbitrary linear cost `c`,
arbitrary bounds `u_min, u_max, g_min, g_max, rho > 0` — affine decision rules are ALWAYS exact:
`bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels`. -/
theorem bridge_adr_exact_diagonal (D : Data) (diag : DiagonalBridgeData D) :
    bridgeAdrLevels D = D.aroLevels ∧ bridgeAdrLevels D = D.sourceLevels := by
  classical
  have hsub := (bridge_adr_subset_aro_and_source D).1
  have heq_aro : bridgeAdrLevels D = D.aroLevels := by
    apply Set.Subset.antisymm hsub
    intro eta haro
    rw [← vertex_lp_epigraph_eq_aro D] at haro
    rcases haro with ⟨a, uVert, hvert⟩
    let cCoord : Fin D.n → ℝ := fun i => D.c (Pi.single i (1 : ℝ))
    let zCorner : Corner D → Fin D.n → ℝ := fun σ i =>
      D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σ)) (uVert σ).val 0 i
    let faceSet : Fin D.n → Bool → Finset (Corner D) := fun i b =>
      Finset.univ.filter (fun σ : Corner D =>
        D.deviation (cornerNoise D σ) i = if b then diagRadius diag i else -diagRadius diag i)
    have hface_ne : ∀ (i : Fin D.n) (b : Bool), (faceSet i b).Nonempty := by
      intro i b
      refine ⟨cornerOfSigns diag (fun _ => b), ?_⟩
      simp [faceSet, deviation_cornerOfSigns diag]
    have hmin_ex : ∀ (i : Fin D.n) (b : Bool),
        ∃ σ ∈ faceSet i b, ∀ τ ∈ faceSet i b, cCoord i * zCorner σ i ≤ cCoord i * zCorner τ i :=
      fun i b => Finset.exists_min_image (faceSet i b) (fun σ => cCoord i * zCorner σ i) (hface_ne i b)
    choose σStar hσStar_mem hσStar_min using hmin_ex
    let bMin : Fin D.n → Fin D.q → ℝ := fun i t => (uVert (σStar i false)).val t (Fin.cast diag.hm.symm i)
    let bMax : Fin D.n → Fin D.q → ℝ := fun i t => (uVert (σStar i true)).val t (Fin.cast diag.hm.symm i)
    let b0Fun : Fin D.q → Vec D.m := fun t j =>
      let i : Fin D.n := Fin.cast diag.hm j
      if diagRadius diag i = 0 then bMin i t else (bMin i t + bMax i t) / 2
    let KFun : Fin D.q → (Vec D.n →ₗ[ℝ] Vec D.m) := fun t =>
      { toFun := fun v j =>
          let i : Fin D.n := Fin.cast diag.hm j
          if diagRadius diag i = 0 then 0 else (v i / (2 * diagRadius diag i)) * (bMax i t - bMin i t)
        map_add' := fun u v => by
          funext j
          dsimp
          split_ifs
          · simp
          · ring
        map_smul' := fun r u => by
          funext j
          dsimp
          split_ifs
          · simp
          · ring }
    let lam : Fin D.n → D.Z → ℝ := fun i xi =>
      if diagRadius diag i = 0 then 0 else (xi.val i + diagRadius diag i) / (2 * diagRadius diag i)
    have hxi_bounds : ∀ (xi : D.Z) (i : Fin D.n),
        -diagRadius diag i ≤ xi.val i ∧ xi.val i ≤ diagRadius diag i := by
      intro xi i
      rcases xi.property with ⟨w, hw⟩
      rw [← hw]
      exact diag_deviation_bounds diag w i
    have hlam_bounds : ∀ (i : Fin D.n) (xi : D.Z), 0 ≤ lam i xi ∧ lam i xi ≤ 1 := by
      intro i xi
      dsimp [lam]
      split_ifs with h0
      · norm_num
      · have hpos : 0 < diagRadius diag i := lt_of_le_of_ne (diagRadius_nonneg diag i) (Ne.symm h0)
        have h2pos : 0 < 2 * diagRadius diag i := by linarith
        have hb := hxi_bounds xi i
        constructor
        · exact div_nonneg (by linarith) (le_of_lt h2pos)
        · exact (div_le_one h2pos).mpr (by linarith)
    have heval_conv : ∀ (xi : D.Z) (t : Fin D.q) (j : Fin D.m),
        (b0Fun t + KFun t xi.val) j =
          (1 - lam (Fin.cast diag.hm j) xi) * bMin (Fin.cast diag.hm j) t +
            lam (Fin.cast diag.hm j) xi * bMax (Fin.cast diag.hm j) t := by
      intro xi t j
      let i : Fin D.n := Fin.cast diag.hm j
      change b0Fun t j + KFun t xi.val j = (1 - lam i xi) * bMin i t + lam i xi * bMax i t
      dsimp [b0Fun, KFun, lam, i]
      split_ifs with h0
      · ring
      · have h2ne : 2 * diagRadius diag (Fin.cast diag.hm j) ≠ 0 := mul_ne_zero (by norm_num) h0
        field_simp [h2ne]
        ring
    let P : AffineDeviationPolicy D :=
      { b0 := b0Fun
        K := KFun
        in_box := fun xi t j => by
          rw [heval_conv xi t j]
          let i : Fin D.n := Fin.cast diag.hm j
          have hlam := hlam_bounds i xi
          have h1m : 0 ≤ 1 - lam i xi := sub_nonneg.mpr hlam.2
          have hmin := (uVert (σStar i false)).property t j
          have hmax := (uVert (σStar i true)).property t j
          dsimp [bMin, bMax]
          constructor <;> nlinarith }
    refine ⟨a, P, (BridgeFormalV3.Proofs.exact_tightening D a P.toDeviationPolicy eta).mpr ?_⟩
    intro xi
    have hxi_conv : ∀ i : Fin D.n,
        xi.val i = (1 - lam i xi) * D.deviation (cornerNoise D (σStar i false)) i +
          lam i xi * D.deviation (cornerNoise D (σStar i true)) i := by
      intro i
      have hfm : D.deviation (cornerNoise D (σStar i false)) i = -diagRadius diag i := by
        simpa [faceSet] using (Finset.mem_filter.mp (hσStar_mem i false)).2
      have hfp : D.deviation (cornerNoise D (σStar i true)) i = diagRadius diag i := by
        simpa [faceSet] using (Finset.mem_filter.mp (hσStar_mem i true)).2
      rw [hfm, hfp]
      dsimp [lam]
      split_ifs with h0
      · have hb := hxi_bounds xi i
        rw [h0] at hb
        linarith
      · have h2ne : 2 * diagRadius diag i ≠ 0 := mul_ne_zero (by norm_num) h0
        field_simp [h2ne]
        ring
    have hz_conv : ∀ i : Fin D.n,
        D.aroNominalTerminal a P.toDeviationPolicy xi i =
          (1 - lam i xi) * zCorner (σStar i false) i + lam i xi * zCorner (σStar i true) i := by
      intro i
      change D.expansion D.q (D.nominal a + xi.val) (P.toDeviationPolicy.rule xi).val 0 i = _
      rw [diag_expansion_apply diag]
      simp only [zCorner, diag_expansion_apply diag, Pi.add_apply, Pi.zero_apply, mul_zero, add_zero]
      have hctrl : ∀ t : Fin D.q,
          (P.toDeviationPolicy.rule xi).val t (Fin.cast diag.hm.symm i) =
            (1 - lam i xi) * (uVert (σStar i false)).val t (Fin.cast diag.hm.symm i) +
              lam i xi * (uVert (σStar i true)).val t (Fin.cast diag.hm.symm i) := by
        intro t
        have hc := heval_conv xi t (Fin.cast diag.hm.symm i)
        have hcast : Fin.cast diag.hm (Fin.cast diag.hm.symm i) = i := by ext; rfl
        simpa only [AffineDeviationPolicy.toDeviationPolicy, bMin, bMax, hcast] using hc
      simp_rw [hctrl, hxi_conv i]
      have hsum_split :
          ∑ t : Fin D.q, (diag.aDiag i) ^ (D.q - 1 - t.val) *
            (diag.bDiag i * ((1 - lam i xi) * (uVert (σStar i false)).val t (Fin.cast diag.hm.symm i) +
              lam i xi * (uVert (σStar i true)).val t (Fin.cast diag.hm.symm i))) =
            (1 - lam i xi) * (∑ t : Fin D.q, (diag.aDiag i) ^ (D.q - 1 - t.val) *
              (diag.bDiag i * (uVert (σStar i false)).val t (Fin.cast diag.hm.symm i))) +
            lam i xi * (∑ t : Fin D.q, (diag.aDiag i) ^ (D.q - 1 - t.val) *
              (diag.bDiag i * (uVert (σStar i true)).val t (Fin.cast diag.hm.symm i))) := by
        rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
        apply Finset.sum_congr rfl
        intro t _; ring
      rw [hsum_split]
      ring
    constructor
    · intro r
      let i : Fin D.n := Fin.cast diag.hrows r
      have hlam := hlam_bounds i xi
      have h1m : 0 ≤ 1 - lam i xi := sub_nonneg.mpr hlam.2
      have hrow_eq : ∀ x : Vec D.n, D.terminalRow r x = diag.hDiag i * x i := fun x => diag.hH x r
      constructor
      · change -(D.terminalRow r (D.aroNominalTerminal a P.toDeviationPolicy xi)) +
          D.futureRowSupport (-(D.terminalRow r)) ≤ -D.gmin r
        rw [hrow_eq, hz_conv i]
        have hmin_r := ((hvert (σStar i false)).1 r).1
        have hmax_r := ((hvert (σStar i true)).1 r).1
        change -(D.terminalRow r _) + D.futureRowSupport (-(D.terminalRow r)) ≤ -D.gmin r at hmin_r hmax_r
        rw [hrow_eq] at hmin_r hmax_r
        change -(diag.hDiag i * zCorner (σStar i false) i) + D.futureRowSupport (-(D.terminalRow r)) ≤ -D.gmin r at hmin_r
        change -(diag.hDiag i * zCorner (σStar i true) i) + D.futureRowSupport (-(D.terminalRow r)) ≤ -D.gmin r at hmax_r
        nlinarith
      · rw [hrow_eq, hz_conv i]
        have hmin_r := ((hvert (σStar i false)).1 r).2
        have hmax_r := ((hvert (σStar i true)).1 r).2
        change D.terminalRow r _ + D.futureRowSupport (D.terminalRow r) ≤ D.gmax r at hmin_r hmax_r
        rw [hrow_eq] at hmin_r hmax_r
        change diag.hDiag i * zCorner (σStar i false) i + D.futureRowSupport (D.terminalRow r) ≤ D.gmax r at hmin_r
        change diag.hDiag i * zCorner (σStar i true) i + D.futureRowSupport (D.terminalRow r) ≤ D.gmax r at hmax_r
        nlinarith
    · -- Cost row: choose worst sign per coordinate, realize jointly via cornerOfSigns!
      let sBest : Fin D.n → Bool := fun i =>
        decide (cCoord i * zCorner (σStar i false) i ≤ cCoord i * zCorner (σStar i true) i)
      let σJoint : Corner D := cornerOfSigns diag sBest
      have hcost_le : D.c (D.aroNominalTerminal a P.toDeviationPolicy xi) ≤
          D.c (D.expansion D.q (D.nominal a + D.deviation (cornerNoise D σJoint)) (uVert σJoint).val 0) := by
        rw [linearMap_decompose_coord D.c, linearMap_decompose_coord D.c]
        apply Finset.sum_le_sum
        intro i _
        change cCoord i * D.aroNominalTerminal a P.toDeviationPolicy xi i ≤ cCoord i * zCorner σJoint i
        rw [hz_conv i]
        have hlam := hlam_bounds i xi
        have h1m : 0 ≤ 1 - lam i xi := sub_nonneg.mpr hlam.2
        have hstep1 : cCoord i * ((1 - lam i xi) * zCorner (σStar i false) i +
            lam i xi * zCorner (σStar i true) i) ≤ cCoord i * zCorner (σStar i (sBest i)) i := by
          by_cases hcmp : cCoord i * zCorner (σStar i false) i ≤ cCoord i * zCorner (σStar i true) i
          · have hsb : sBest i = true := decide_eq_true hcmp
            rw [hsb]; nlinarith
          · have hsb : sBest i = false := decide_eq_false hcmp
            have hlt : cCoord i * zCorner (σStar i true) i < cCoord i * zCorner (σStar i false) i :=
              lt_of_not_ge hcmp
            rw [hsb]; nlinarith
        have hmem_joint : σJoint ∈ faceSet i (sBest i) := by
          simp [faceSet, σJoint, deviation_cornerOfSigns diag]
        have hstep2 := hσStar_min i (sBest i) σJoint hmem_joint
        exact le_trans hstep1 hstep2
      have hjoint_cost := (hvert σJoint).2
      linarith
  refine ⟨heq_aro, ?_⟩
  rw [heq_aro, BridgeFormalV2.Proofs.epigraph_equality D]

/-! ## Section 4: O1 / O5 Refutation of `H-O1-1` — Invertible Unimodular Shear Witness -/

/-- 2D unimodular shear witness (`det B = 1`, `A = E = H = I_2`, `U = [-1/2, 1/2]^2`, `rho = 1`,
`g_min = (0, -1)`, `g_max = (4, 3)`, `c = (1, 1)^T`) refuting `H-O1-1`. -/
abbrev bridgeFullRankShearData : Data where
  n := 2
  m := 2
  p := 2
  rows := 2
  r := 1
  q := 1
  n_pos := by omega
  m_pos := by omega
  p_pos := by omega
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := LinearMap.id
  B :=
    { toFun := fun u i => if i = 0 then u 0 + u 1 else u 1
      map_add' := fun u v => by funext i; fin_cases i <;> simp [add_assoc, add_left_comm, add_comm]
      map_smul' := fun r u => by funext i; fin_cases i <;> simp [mul_add] }
  E := LinearMap.id
  x0 := 0
  umin := fun _ => -(1 / 2 : ℝ)
  umax := fun _ => (1 / 2 : ℝ)
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun i => if i = 0 then 0 else -1
  gmax := fun i => if i = 0 then 4 else 3
  c :=
    { toFun := fun x => x 0 + x 1
      map_add' := fun x y => by simp; ring
      map_smul' := fun r x => by simp; ring }

/-- **Theorem O1.9:** The shear recourse matrix `B = [[1, 1], [0, 1]]` of
`bridgeFullRankShearData` is bijective (full-rank / invertible in `GL_2(ℝ)`). -/
theorem shearRecourse_bijective : Function.Bijective bridgeFullRankShearData.B := by
  constructor
  · intro u v huv
    have h0 := congrFun huv 0
    have h1 := congrFun huv 1
    simp [bridgeFullRankShearData] at h0 h1
    funext i
    fin_cases i
    · change u 0 = v 0; linarith
    · change u 1 = v 1; linarith
  · intro y
    refine ⟨fun i => if i = 0 then y 0 - y 1 else y 1, ?_⟩
    funext i
    fin_cases i <;> simp [bridgeFullRankShearData]

private theorem shear_deviation_eq (wm : bridgeFullRankShearData.NoiseBlock 1) (i : Fin 2) :
    bridgeFullRankShearData.deviation wm i = wm.val 0 i := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, bridgeFullRankShearData]

private theorem shear_terminal_eq0 (a b : bridgeFullRankShearData.ControlBlock 1)
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

private theorem shear_terminal_eq1 (a b : bridgeFullRankShearData.ControlBlock 1)
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

private def mkShearNoise (v0 v1 : ℝ) (h0 : -1 ≤ v0 ∧ v0 ≤ 1) (h1 : -1 ≤ v1 ∧ v1 ≤ 1) :
    bridgeFullRankShearData.NoiseBlock 1 :=
  ⟨fun _ i => if i = 0 then v0 else v1, by
    intro t i
    fin_cases i
    · simpa [bridgeFullRankShearData] using h0
    · simpa [bridgeFullRankShearData] using h1⟩

/-- **Theorem O1.10 (Refutation of `H-O1-1` — Full-Rank Invertible Recourse Still Fails ADR):**
Even with `A = E = H = I_2` (coordinatewise terminal box) and bijective unimodular recourse
`B = [[1, 1], [0, 1]]`, `5 ∈ D.aroLevels ∩ D.sourceLevels` (attained by the continuous piecewise-affine
rule `u_1 = (1/2, 1/2)`, `u_{2,0}(v) = -v_0 / 2`, `u_{2,1}(v) = max(-v_0 / 2, -v_1 / 2, 0)`),
whereas EVERY affine decision rule satisfies `6 ≤ eta` via the square barycentric syzygy on `u_{2,1}`. -/
theorem exists_bridge_2d_fullrank_invertible_strict_adr_gap :
    ∃ D : Data, D.n = 2 ∧ D.m = 2 ∧ D.rows = 2 ∧ Function.Bijective D.B ∧
      (5 : ℝ) ∈ D.aroLevels ∧ (5 : ℝ) ∈ D.sourceLevels ∧
      ∀ eta ∈ bridgeAdrLevels D, (6 : ℝ) ≤ eta := by
  have h5_aro : (5 : ℝ) ∈ bridgeFullRankShearData.aroLevels := by
    let a1 : bridgeFullRankShearData.ControlBlock 1 :=
      ⟨fun _ _ => (1 / 2 : ℝ), fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let u2RuleFun : bridgeFullRankShearData.Z → Fin 1 → Vec 2 := fun xi _ j =>
      if j = 0 then -(xi.val 0) / 2 else max (-(xi.val 0) / 2) (max (-(xi.val 1) / 2) 0)
    have hy_box : ∀ (xi : bridgeFullRankShearData.Z) (t : Fin 1) (j : Fin 2),
        bridgeFullRankShearData.umin j ≤ u2RuleFun xi t j ∧
        u2RuleFun xi t j ≤ bridgeFullRankShearData.umax j := by
      intro xi t j
      rcases xi.property with ⟨wm, hwm⟩
      have h0 : -1 ≤ xi.val 0 ∧ xi.val 0 ≤ 1 := by
        rw [← hwm, shear_deviation_eq]; exact wm.property 0 0
      have h1 : -1 ≤ xi.val 1 ∧ xi.val 1 ≤ 1 := by
        rw [← hwm, shear_deviation_eq]; exact wm.property 0 1
      fin_cases j
      · change -(1 / 2 : ℝ) ≤ -(xi.val 0) / 2 ∧ -(xi.val 0) / 2 ≤ (1 / 2 : ℝ)
        constructor <;> linarith
      · change -(1 / 2 : ℝ) ≤ max (-(xi.val 0) / 2) (max (-(xi.val 1) / 2) 0) ∧
          max (-(xi.val 0) / 2) (max (-(xi.val 1) / 2) 0) ≤ (1 / 2 : ℝ)
        constructor
        · exact le_trans (by norm_num) (le_trans (le_max_right _ _) (le_max_right _ _))
        · exact max_le (by linarith) (max_le (by linarith) (by norm_num))
    let yRule : bridgeFullRankShearData.Z → bridgeFullRankShearData.ControlBlock 1 :=
      fun xi => ⟨u2RuleFun xi, hy_box xi⟩
    have hy_meas : Measurable yRule := by
      refine Continuous.measurable ?_
      refine Continuous.subtype_mk (continuous_pi fun _ => continuous_pi fun j => ?_) _
      fin_cases j
      · exact (((continuous_apply (0 : Fin 2)).comp continuous_subtype_val).neg).div_const 2
      · exact ((((continuous_apply (0 : Fin 2)).comp continuous_subtype_val).neg).div_const 2).max
          (((((continuous_apply (1 : Fin 2)).comp continuous_subtype_val).neg).div_const 2).max
            continuous_const)
    let yPol : bridgeFullRankShearData.DeviationPolicy := ⟨yRule, hy_meas⟩
    refine ⟨a1, yPol, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hw0 : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    have hw1 : (-1 : ℝ) ≤ wm.val 0 1 ∧ wm.val 0 1 ≤ 1 := wm.property 0 1
    have hq0 : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    have hq1 : (-1 : ℝ) ≤ wp.val 0 1 ∧ wp.val 0 1 ≤ 1 := wp.property 0 1
    have hxi0 : xi.val 0 = wm.val 0 0 := by rw [← hwm, shear_deviation_eq]
    have hxi1 : xi.val 1 = wm.val 0 1 := by rw [← hwm, shear_deviation_eq]
    let mval : ℝ := max (-(wm.val 0 0) / 2) (max (-(wm.val 0 1) / 2) 0)
    have hb0 : (yPol.rule xi).val 0 0 = -(wm.val 0 0) / 2 := by
      simp [yPol, yRule, u2RuleFun, hxi0]
    have hb1 : (yPol.rule xi).val 0 1 = mval := by
      simp [yPol, yRule, u2RuleFun, hxi0, hxi1, mval]
    have hx0 : bridgeFullRankShearData.aroTerminal a1 yPol xi wp 0 =
        1 + wm.val 0 0 / 2 + mval + wp.val 0 0 := by
      change bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a1 + xi.val) (yPol.rule xi).val wp.val 0 = _
      rw [← hwm, shear_terminal_eq0, hb0, hb1]
      change (1 / 2 : ℝ) + (1 / 2 : ℝ) + -(wm.val 0 0) / 2 + mval + wm.val 0 0 + wp.val 0 0 = _
      ring
    have hx1 : bridgeFullRankShearData.aroTerminal a1 yPol xi wp 1 =
        (1 / 2 : ℝ) + mval + wm.val 0 1 + wp.val 0 1 := by
      change bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a1 + xi.val) (yPol.rule xi).val wp.val 1 = _
      rw [← hwm, shear_terminal_eq1, hb1]
    have hm_ge0 : -(wm.val 0 0) / 2 ≤ mval := le_max_left _ _
    have hm_ge1 : -(wm.val 0 1) / 2 ≤ mval := le_trans (le_max_left _ _) (le_max_right _ _)
    have hm_ge_z : 0 ≤ mval := le_trans (le_max_right _ _) (le_max_right _ _)
    have hm_le : mval ≤ (1 / 2 : ℝ) := max_le (by linarith) (max_le (by linarith) (by norm_num))
    constructor
    · intro i
      fin_cases i
      · change (0 : ℝ) ≤ bridgeFullRankShearData.aroTerminal a1 yPol xi wp 0 ∧
          bridgeFullRankShearData.aroTerminal a1 yPol xi wp 0 ≤ 4
        rw [hx0]; constructor <;> linarith
      · change (-1 : ℝ) ≤ bridgeFullRankShearData.aroTerminal a1 yPol xi wp 1 ∧
          bridgeFullRankShearData.aroTerminal a1 yPol xi wp 1 ≤ 3
        rw [hx1]; constructor <;> linarith
    · change bridgeFullRankShearData.aroTerminal a1 yPol xi wp 0 +
        bridgeFullRankShearData.aroTerminal a1 yPol xi wp 1 ≤ 5
      rw [hx0, hx1]
      rcases max_choice (-(wm.val 0 0) / 2) (max (-(wm.val 0 1) / 2) 0) with hcase | hcase
      · have hmv : mval = -(wm.val 0 0) / 2 := hcase
        linarith
      · rcases max_choice (-(wm.val 0 1) / 2) (0 : ℝ) with hcase2 | hcase2
        · have hmv : mval = -(wm.val 0 1) / 2 := hcase.trans hcase2
          linarith
        · have hmv : mval = 0 := hcase.trans hcase2
          linarith
  refine ⟨bridgeFullRankShearData, rfl, rfl, rfl, shearRecourse_bijective, h5_aro, ?_, ?_⟩
  · rw [BridgeFormalV2.Proofs.epigraph_equality bridgeFullRankShearData]
    exact h5_aro
  · intro eta ⟨a, P, hbound⟩
    let u10 : ℝ := a.val 0 0
    let u11 : ℝ := a.val 0 1
    have hu10_le : u10 ≤ (1 / 2 : ℝ) := (a.property 0 0).2
    have hu11_le : u11 ≤ (1 / 2 : ℝ) := (a.property 0 1).2
    let w_mp := mkShearNoise (-1) 1 (by norm_num) (by norm_num)
    let w_pm := mkShearNoise 1 (-1) (by norm_num) (by norm_num)
    let w_mm := mkShearNoise (-1) (-1) (by norm_num) (by norm_num)
    let w_pp := mkShearNoise 1 1 (by norm_num) (by norm_num)
    let u2At : bridgeFullRankShearData.NoiseBlock 1 → Fin 2 → ℝ := fun wm j =>
      (P.toDeviationPolicy.rule (bridgeFullRankShearData.observedDeviation wm)).val 0 j
    -- Square barycentric syzygy on the affine rule u_{2,1}
    have hdev_syz :
        bridgeFullRankShearData.deviation w_mp + bridgeFullRankShearData.deviation w_pm =
        bridgeFullRankShearData.deviation w_mm + bridgeFullRankShearData.deviation w_pp := by
      funext i
      simp only [Pi.add_apply, shear_deviation_eq]
      fin_cases i <;> norm_num [w_mp, w_pm, w_mm, w_pp, mkShearNoise]
    have hsyz_u21 : u2At w_mp 1 + u2At w_pm 1 = u2At w_mm 1 + u2At w_pp 1 := by
      have hK := congrFun (congrArg (P.K 0) hdev_syz) 1
      simp only [map_add, Pi.add_apply] at hK
      change (P.b0 0 1 + P.K 0 (bridgeFullRankShearData.deviation w_mp) 1) +
          (P.b0 0 1 + P.K 0 (bridgeFullRankShearData.deviation w_pm) 1) =
        (P.b0 0 1 + P.K 0 (bridgeFullRankShearData.deviation w_mm) 1) +
          (P.b0 0 1 + P.K 0 (bridgeFullRankShearData.deviation w_pp) 1)
      linarith
    -- Box bounds at corners
    have hub_mp0 : u2At w_mp 0 ≤ (1 / 2 : ℝ) :=
      (P.in_box (bridgeFullRankShearData.observedDeviation w_mp) 0 0).2
    have hub_mp1 : u2At w_mp 1 ≤ (1 / 2 : ℝ) :=
      (P.in_box (bridgeFullRankShearData.observedDeviation w_mp) 0 1).2
    have hub_pm1 : u2At w_pm 1 ≤ (1 / 2 : ℝ) :=
      (P.in_box (bridgeFullRankShearData.observedDeviation w_pm) 0 1).2
    have hub_mm1 : u2At w_mm 1 ≤ (1 / 2 : ℝ) :=
      (P.in_box (bridgeFullRankShearData.observedDeviation w_mm) 0 1).2
    have hlb_pp0 : -(1 / 2 : ℝ) ≤ u2At w_pp 0 :=
      (P.in_box (bridgeFullRankShearData.observedDeviation w_pp) 0 0).1
    -- Terminal lower bound on coordinate 0 at w_mp = (-1, 1) with wp = (-1, -1)
    have hlo_mp0 : (0 : ℝ) ≤ u10 + u11 + u2At w_mp 0 + u2At w_mp 1 - 2 := by
      have h := ((hbound (bridgeFullRankShearData.observedDeviation w_mp) w_mm).1 0).1
      change (0 : ℝ) ≤ bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_mp)
        (P.toDeviationPolicy.rule (bridgeFullRankShearData.observedDeviation w_mp)).val w_mm.val 0 at h
      rw [shear_terminal_eq0] at h
      have h0 : w_mp.val 0 0 = -1 := rfl
      have h1 : w_mm.val 0 0 = -1 := rfl
      rw [h0, h1] at h
      linarith
    -- Terminal lower bound on coordinate 1 at w_pm = (1, -1) with wp = (-1, -1)
    have hlo_pm1 : (-1 : ℝ) ≤ u11 + u2At w_pm 1 - 2 := by
      have h := ((hbound (bridgeFullRankShearData.observedDeviation w_pm) w_mm).1 1).1
      change (-1 : ℝ) ≤ bridgeFullRankShearData.expansion 1
        (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pm)
        (P.toDeviationPolicy.rule (bridgeFullRankShearData.observedDeviation w_pm)).val w_mm.val 1 at h
      rw [shear_terminal_eq1] at h
      have h0 : w_pm.val 0 1 = -1 := rfl
      have h1 : w_mm.val 0 1 = -1 := rfl
      rw [h0, h1] at h
      linarith
    -- Cost bound at w_pp = (1, 1) with wp = (1, 1)
    have hcost_pp : u10 + 2 * u11 + u2At w_pp 0 + 2 * u2At w_pp 1 + 4 ≤ eta := by
      have h := (hbound (bridgeFullRankShearData.observedDeviation w_pp) w_pp).2
      change bridgeFullRankShearData.expansion 1
          (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pp)
          (P.toDeviationPolicy.rule (bridgeFullRankShearData.observedDeviation w_pp)).val w_pp.val 0 +
        bridgeFullRankShearData.expansion 1
          (bridgeFullRankShearData.nominal a + bridgeFullRankShearData.deviation w_pp)
          (P.toDeviationPolicy.rule (bridgeFullRankShearData.observedDeviation w_pp)).val w_pp.val 1 ≤ eta at h
      rw [shear_terminal_eq0, shear_terminal_eq1] at h
      have h0 : w_pp.val 0 0 = 1 := rfl
      have h1 : w_pp.val 0 1 = 1 := rfl
      rw [h0, h1] at h
      linarith
    linarith

/-! ## Section 5: O2 Quantitative Scaling — Linear `Ω(n)` Affine Gap in Frozen `Data` -/

/-- `k`-block decoupled copies of the 2D rank-1 bridge witness (`n = 2*k, m = k, p = 2*k, rows = 2*k`). -/
abbrev bridgeLinearGapData (k : ℕ) (hk : 0 < k) : Data where
  n := 2 * k
  m := k
  p := 2 * k
  rows := 2 * k
  r := 1
  q := 1
  n_pos := by omega
  m_pos := hk
  p_pos := by omega
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := LinearMap.id
  B :=
    { toFun := fun u i => u ⟨i.val / 2, by omega⟩
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
    { toFun := fun x => ∑ i : Fin (2 * k), x i
      map_add' := fun x y => by simp [Finset.sum_add_distrib]
      map_smul' := fun r x => by simp [Finset.mul_sum] }

private theorem linearGap_deviation_eq (k : ℕ) (hk : 0 < k)
    (wm : (bridgeLinearGapData k hk).NoiseBlock 1) (i : Fin (2 * k)) :
    (bridgeLinearGapData k hk).deviation wm i = wm.val 0 i := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, bridgeLinearGapData]

private theorem linearGap_terminal_eq (k : ℕ) (hk : 0 < k)
    (a b : (bridgeLinearGapData k hk).ControlBlock 1)
    (wm wp : (bridgeLinearGapData k hk).NoiseBlock 1) (i : Fin (2 * k)) :
    (bridgeLinearGapData k hk).expansion 1
      ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wm) b.val wp.val i =
      a.val 0 (⟨i.val / 2, by omega⟩ : Fin k) + b.val 0 (⟨i.val / 2, by omega⟩ : Fin k) +
        wm.val 0 i + wp.val 0 i := by
  have ha0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    bridgeLinearGapData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    ha0, hw0, Module.End.one_apply, LinearMap.id_apply, LinearMap.coe_mk, AddHom.coe_mk,
    Pi.add_apply, Pi.zero_apply, zero_add, add_zero]
  ring

private theorem sum_fin_two_mul (k : ℕ) (f : Fin (2 * k) → ℝ) :
    ∑ i : Fin (2 * k), f i =
      ∑ j : Fin k, (f ⟨2 * j.val, by omega⟩ + f ⟨2 * j.val + 1, by omega⟩) := by
  let e : Fin (2 * k) ≃ Fin k × Fin 2 :=
    { toFun := fun i => (⟨i.val / 2, by omega⟩, ⟨i.val % 2, by omega⟩)
      invFun := fun p => ⟨2 * p.1.val + p.2.val, by omega⟩
      left_inv := fun i => Fin.ext (by dsimp; omega)
      right_inv := fun p => Prod.ext (Fin.ext (by dsimp; omega)) (Fin.ext (by dsimp; omega)) }
  have heq : (∑ i : Fin (2 * k), f i) =
      ∑ p : Fin k × Fin 2, f ⟨2 * p.1.val + p.2.val, by omega⟩ :=
    Fintype.sum_equiv e f (fun p => f ⟨2 * p.1.val + p.2.val, by omega⟩)
      (fun i => congrArg f (Fin.ext (by dsimp [e]; omega)))
  rw [heq, Fintype.sum_prod_type]
  apply Finset.sum_congr rfl
  intro j _
  rw [Fin.sum_univ_two]
  simp

/-- **Theorem O2.1 (Linear `Ω(n)` Affine Gap Scaling Inside Frozen `BridgeFormalV2.Data`):**
For every `k ≥ 1`, there exists a frozen `BridgeFormalV2.Data` instance of state dimension
`D.n = 2 * k` such that `6 * k ∈ D.aroLevels ∩ D.sourceLevels`, whereas EVERY affine decision
rule (even with arbitrary cross-block feedback `K : ℝ^{2k} → ℝ^k`) satisfies `8 * k ≤ eta`.
Hence the additive ADR gap grows at least linearly (`≥ 2k = n`) with ratio `≥ 4/3`. -/
theorem exists_bridge_linear_adr_gap_scaling (k : ℕ) (hk : 0 < k) :
    ∃ D : Data, D.n = 2 * k ∧
      (6 * (k : ℝ)) ∈ D.aroLevels ∧ (6 * (k : ℝ)) ∈ D.sourceLevels ∧
      ∀ eta ∈ bridgeAdrLevels D, (8 * (k : ℝ)) ≤ eta := by
  have h6k_aro : (6 * (k : ℝ)) ∈ (bridgeLinearGapData k hk).aroLevels := by
    let a1 : (bridgeLinearGapData k hk).ControlBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let u2Fun : (bridgeLinearGapData k hk).Z → Fin 1 → Vec k := fun xi _ j =>
      max (-xi.val (⟨2 * j.val, by omega⟩ : Fin (2 * k)))
        (-xi.val (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)))
    have hy_box : ∀ (xi : (bridgeLinearGapData k hk).Z) (t : Fin 1) (j : Fin k),
        (bridgeLinearGapData k hk).umin j ≤ u2Fun xi t j ∧
        u2Fun xi t j ≤ (bridgeLinearGapData k hk).umax j := by
      intro xi t j
      rcases xi.property with ⟨wm, hwm⟩
      have h0 : -1 ≤ xi.val (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ∧
          xi.val (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ≤ 1 := by
        rw [← hwm, linearGap_deviation_eq]; exact wm.property 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k))
      have h1 : -1 ≤ xi.val (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ∧
          xi.val (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ≤ 1 := by
        rw [← hwm, linearGap_deviation_eq]; exact wm.property 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k))
      change (-1 : ℝ) ≤ u2Fun xi t j ∧ u2Fun xi t j ≤ 1
      dsimp [u2Fun]
      exact ⟨le_trans (by linarith) (le_max_left _ _), max_le (by linarith) (by linarith)⟩
    let yRule : (bridgeLinearGapData k hk).Z → (bridgeLinearGapData k hk).ControlBlock 1 :=
      fun xi => ⟨u2Fun xi, hy_box xi⟩
    have hy_meas : Measurable yRule := by
      refine Continuous.measurable ?_
      refine Continuous.subtype_mk (continuous_pi fun _ => continuous_pi fun (j : Fin k) => ?_) _
      exact (((continuous_apply (⟨2 * j.val, by omega⟩ : Fin (2 * k))).comp continuous_subtype_val).neg).max
        (((continuous_apply (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k))).comp continuous_subtype_val).neg)
    let yPol : (bridgeLinearGapData k hk).DeviationPolicy := ⟨yRule, hy_meas⟩
    refine ⟨a1, yPol, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hterm : ∀ i : Fin (2 * k),
        (bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp i =
          1 + max (-wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)))
                (-wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k))) +
            wm.val 0 i + wp.val 0 i := by
      intro i
      change (bridgeLinearGapData k hk).expansion 1
        ((bridgeLinearGapData k hk).nominal a1 + xi.val) (yPol.rule xi).val wp.val i = _
      rw [← hwm, linearGap_terminal_eq]
      have hxi0 : xi.val (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)) =
          wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)) := by
        rw [← hwm, linearGap_deviation_eq]
      have hxi1 : xi.val (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k)) =
          wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k)) := by
        rw [← hwm, linearGap_deviation_eq]
      simp only [a1, yPol, yRule, u2Fun, hxi0, hxi1]
    constructor
    · intro (i : Fin (2 * k))
      have hwi : (-1 : ℝ) ≤ wm.val 0 i ∧ wm.val 0 i ≤ 1 := wm.property 0 i
      have hqi : (-1 : ℝ) ≤ wp.val 0 i ∧ wp.val 0 i ≤ 1 := wp.property 0 i
      have h0 : (-1 : ℝ) ≤ wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)) ∧
          wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)) ≤ 1 :=
        wm.property 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k))
      have h1 : (-1 : ℝ) ≤ wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k)) ∧
          wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k)) ≤ 1 :=
        wm.property 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k))
      have hm_le : max (-wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)))
          (-wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k))) ≤ 1 :=
        max_le (by linarith) (by linarith)
      have hm_ge : -wm.val 0 i ≤
          max (-wm.val 0 (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)))
            (-wm.val 0 (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k))) := by
        by_cases heven : i.val % 2 = 0
        · have hi : i = (⟨2 * (i.val / 2), by omega⟩ : Fin (2 * k)) := by ext; dsimp; omega
          conv_lhs => rw [hi]
          exact le_max_left _ _
        · have hi : i = (⟨2 * (i.val / 2) + 1, by omega⟩ : Fin (2 * k)) := by ext; dsimp; omega
          conv_lhs => rw [hi]
          exact le_max_right _ _
      change (0 : ℝ) ≤ (bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp i ∧
        (bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp i ≤ 4
      rw [hterm i]
      constructor <;> linarith
    · change ∑ i : Fin (2 * k), (bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp i ≤ 6 * (k : ℝ)
      rw [sum_fin_two_mul k]
      calc ∑ j : Fin k, ((bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp
              (⟨2 * j.val, by omega⟩ : Fin (2 * k)) +
              (bridgeLinearGapData k hk).aroTerminal a1 yPol xi wp
              (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)))
          ≤ ∑ _j : Fin k, (6 : ℝ) := by
            apply Finset.sum_le_sum
            intro j _
            rw [hterm ⟨2 * j.val, by omega⟩, hterm ⟨2 * j.val + 1, by omega⟩]
            have hd0 : (2 * j.val) / 2 = j.val := by omega
            have hd1 : (2 * j.val + 1) / 2 = j.val := by omega
            have h0 : (-1 : ℝ) ≤ wm.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ∧
                wm.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ≤ 1 :=
              wm.property 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k))
            have h1 : (-1 : ℝ) ≤ wm.val 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ∧
                wm.val 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ≤ 1 :=
              wm.property 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k))
            have hq0 : (-1 : ℝ) ≤ wp.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ∧
                wp.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)) ≤ 1 :=
              wp.property 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k))
            have hq1 : (-1 : ℝ) ≤ wp.val 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ∧
                wp.val 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)) ≤ 1 :=
              wp.property 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k))
            simp only [hd0, hd1]
            rcases max_choice (-wm.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)))
                (-wm.val 0 (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k)))
              with hcase | hcase <;> linarith
        _ = 6 * (k : ℝ) := by simp [mul_comm]
  refine ⟨bridgeLinearGapData k hk, rfl, h6k_aro, ?_, ?_⟩
  · rw [BridgeFormalV2.Proofs.epigraph_equality (bridgeLinearGapData k hk)]
    exact h6k_aro
  · intro eta ⟨a, P, hbound⟩
    let wAllP : (bridgeLinearGapData k hk).NoiseBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wAllM : (bridgeLinearGapData k hk).NoiseBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let u2At : (bridgeLinearGapData k hk).NoiseBlock 1 → Fin k → ℝ := fun wm j =>
      (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wm)).val 0 j
    -- For each block j, pin a_j = 1 and u2_j(wAllP) = 1 via the 2D face square syzygy!
    have hblock_pin : ∀ j : Fin k, (2 : ℝ) ≤ a.val 0 j + u2At wAllP j := by
      intro j
      let i0 : Fin (2 * k) := ⟨2 * j.val, by omega⟩
      let i1 : Fin (2 * k) := ⟨2 * j.val + 1, by omega⟩
      let wMP : (bridgeLinearGapData k hk).NoiseBlock 1 :=
        ⟨fun _ i => if i = i0 then -1 else 1, fun _ i => by
          dsimp only; split_ifs <;> norm_num [bridgeLinearGapData]⟩
      let wPM : (bridgeLinearGapData k hk).NoiseBlock 1 :=
        ⟨fun _ i => if i = i1 then -1 else 1, fun _ i => by
          dsimp only; split_ifs <;> norm_num [bridgeLinearGapData]⟩
      let wMM : (bridgeLinearGapData k hk).NoiseBlock 1 :=
        ⟨fun _ i => if i = i0 ∨ i = i1 then -1 else 1, fun _ i => by
          dsimp only; split_ifs <;> norm_num [bridgeLinearGapData]⟩
      have hdev_syz : (bridgeLinearGapData k hk).deviation wMP + (bridgeLinearGapData k hk).deviation wPM =
          (bridgeLinearGapData k hk).deviation wMM + (bridgeLinearGapData k hk).deviation wAllP := by
        funext i
        simp only [Pi.add_apply, linearGap_deviation_eq]
        dsimp [wMP, wPM, wMM, wAllP]
        have hi01 : i0 ≠ i1 := by intro h; have := congrArg Fin.val h; dsimp [i0, i1] at this; omega
        by_cases h0 : i = i0
        · subst h0; simp [hi01]
        · by_cases h1 : i = i1
          · subst h1; simp [h0]
          · simp [h0, h1]
      have hsyz_j : u2At wMP j + u2At wPM j = u2At wMM j + u2At wAllP j := by
        have hK := congrFun (congrArg (P.K 0) hdev_syz) j
        simp only [map_add, Pi.add_apply] at hK
        change (P.b0 0 j + P.K 0 ((bridgeLinearGapData k hk).deviation wMP) j) +
            (P.b0 0 j + P.K 0 ((bridgeLinearGapData k hk).deviation wPM) j) =
          (P.b0 0 j + P.K 0 ((bridgeLinearGapData k hk).deviation wMM) j) +
            (P.b0 0 j + P.K 0 ((bridgeLinearGapData k hk).deviation wAllP) j)
        linarith
      have ha_le : a.val 0 j ≤ 1 := (a.property 0 j).2
      have hub_mp : u2At wMP j ≤ 1 := (P.in_box ((bridgeLinearGapData k hk).observedDeviation wMP) 0 j).2
      have hub_pm : u2At wPM j ≤ 1 := (P.in_box ((bridgeLinearGapData k hk).observedDeviation wPM) 0 j).2
      have hub_mm : u2At wMM j ≤ 1 := (P.in_box ((bridgeLinearGapData k hk).observedDeviation wMM) 0 j).2
      have hlo_mp : (0 : ℝ) ≤ a.val 0 j + u2At wMP j - 2 := by
        have h := ((hbound ((bridgeLinearGapData k hk).observedDeviation wMP) wAllM).1 i0).1
        change (0 : ℝ) ≤ (bridgeLinearGapData k hk).expansion 1
          ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wMP)
          (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wMP)).val wAllM.val i0 at h
        rw [linearGap_terminal_eq] at h
        have hd : (⟨i0.val / 2, by omega⟩ : Fin k) = j := by ext; dsimp [i0]; omega
        have hw0 : wMP.val 0 i0 = -1 := by simp [wMP]
        have hwp : wAllM.val 0 i0 = -1 := rfl
        rw [hd, hw0, hwp] at h
        linarith
      have hlo_pm : (0 : ℝ) ≤ a.val 0 j + u2At wPM j - 2 := by
        have h := ((hbound ((bridgeLinearGapData k hk).observedDeviation wPM) wAllM).1 i1).1
        change (0 : ℝ) ≤ (bridgeLinearGapData k hk).expansion 1
          ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wPM)
          (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wPM)).val wAllM.val i1 at h
        rw [linearGap_terminal_eq] at h
        have hd : (⟨i1.val / 2, by omega⟩ : Fin k) = j := by ext; dsimp [i1]; omega
        have hw1 : wPM.val 0 i1 = -1 := by simp [wPM]
        have hwp : wAllM.val 0 i1 = -1 := rfl
        rw [hd, hw1, hwp] at h
        linarith
      linarith
    -- Cost bound at wAllP with wp = wAllP
    have hcost := (hbound ((bridgeLinearGapData k hk).observedDeviation wAllP) wAllP).2
    change ∑ i : Fin (2 * k), (bridgeLinearGapData k hk).expansion 1
      ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wAllP)
      (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wAllP)).val wAllP.val i ≤ eta at hcost
    rw [sum_fin_two_mul k] at hcost
    have hsum_ge : (8 * (k : ℝ)) ≤
        ∑ j : Fin k,
          ((bridgeLinearGapData k hk).expansion 1
            ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wAllP)
            (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wAllP)).val wAllP.val
            (⟨2 * j.val, by omega⟩ : Fin (2 * k)) +
           (bridgeLinearGapData k hk).expansion 1
            ((bridgeLinearGapData k hk).nominal a + (bridgeLinearGapData k hk).deviation wAllP)
            (P.toDeviationPolicy.rule ((bridgeLinearGapData k hk).observedDeviation wAllP)).val wAllP.val
            (⟨2 * j.val + 1, by omega⟩ : Fin (2 * k))) := by
      calc (8 * (k : ℝ)) = ∑ _j : Fin k, (8 : ℝ) := by simp [mul_comm]
        _ ≤ _ := by
          apply Finset.sum_le_sum
          intro j _
          rw [linearGap_terminal_eq, linearGap_terminal_eq]
          have hd0 : (⟨(2 * j.val) / 2, by omega⟩ : Fin k) = j := by ext; dsimp; omega
          have hd1 : (⟨(2 * j.val + 1) / 2, by omega⟩ : Fin k) = j := by ext; dsimp; omega
          have hwp0 : wAllP.val 0 (⟨2 * j.val, by omega⟩ : Fin (2 * k)) = 1 := rfl
          rw [hd0, hd1, hwp0]
          have hpin := hblock_pin j
          linarith
    linarith

end AroProofs.BridgeO1FullRankRecourse
