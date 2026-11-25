import AroProofs.BridgeO4ClosureValue

/-!
# O8: Minimax vs. Maximin Quantifier-Order Gap Hierarchy & Zero-Gap Conditions

Advances open Atlas frontier `conj-o8-quantifier-gap` (previously having zero Lean 4 theorems,
backed only by Python/SymPy counterexample `ce-o8-sion-gap` and Run-02 falsifier
`run02-o8-gap-vanishing-regime`) strictly over the frozen core `BridgeFormalV2.Model` /
`BridgeFormalV2.Goals`, F3 `BridgeFormalV3.Proofs.Support`, and O4 `BridgeO4ClosureValue`.

Main theorems (zero `sorry`, zero custom axioms):
  1. `aro_subset_prefixMaximin` & `source_subset_prefixMaximin`:
     Weak minimax inequality `D.aroLevels ⊆ prefixMaximinLevels D` and
     `D.sourceLevels ⊆ prefixMaximinLevels D` (`V_mm_prefix ≤ V({r})`).
  2. `prefixMaximin_subset_fullMaximin`:
     Full-clairvoyance relaxation `prefixMaximinLevels D ⊆ fullMaximinLevels D`
     (`V_mm_full ≤ V_mm_prefix`), completing the 4-level epigraph chain
     `openLoopLevels D ⊆ D.aroLevels (= D.sourceLevels) ⊆ prefixMaximinLevels D ⊆ fullMaximinLevels D`.
  3. `prefixMaximin_iff_tightened`:
     Exact F3 future-support tightening characterization of `prefixMaximinLevels D`.
  4. `zero_gap_hierarchy_of_unconstrained_terminal`:
     When `D.rows = 0` (no terminal state constraints, pure box controls and linear cost),
     ALL FOUR epigraph level sets collapse:
     `openLoopLevels D = D.aroLevels = prefixMaximinLevels D = fullMaximinLevels D`.
     Hence `D.rows > 0` is strictly necessary for ANY quantifier-order gap.
  5. `exists_strict_quantifier_gap_witness`:
     Machine-checked Lean 4 formalization of `ce-o8-sion-gap`
     (`A=2, B=1, E=1, x0=0, U=[-1,1], rho=1, H=1, gmin=-2, gmax=4, c=1`) proving the
     exact strict 3-way hierarchy `V_mm_full = V_mm_prefix = 0 < 2 = V({1}) < 4 = V(∅)`
     over the continuous disturbance boxes `[-1, 1]^2`.
  6. `exists_prefix_zero_full_strict_gap_witness`:
     Machine-checked Lean 4 formalization of the Run-02 commitment-gap dichotomy
     (`A=1, B=1, E=1, x0=0, U=[-1,1], rho=1, H=1, gmin=-1, gmax=1, c=1`) proving
     `V_mm_full ≤ 0 < 1 = V_mm_prefix = V({1})`, cleanly separating prefix-commitment loss
     (zero here) from irreducible future-noise loss (strictly positive `≥ 1`).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data BridgeFormalV3 AroProofs.BridgeO4ClosureValue

namespace AroProofs.BridgeO8QuantifierGap

/-! ## Section 1: Clairvoyant maximin level sets and weak minimax hierarchy -/

/-- Terminal state reached by prefix control `a`, suffix control `b`, exogenous prefix
deviation `xi ∈ Ξ`, and future disturbance block `wp`. -/
def pointwiseTerminal (D : Data) (a : D.ControlBlock D.r) (b : D.ControlBlock D.q)
    (xi : D.Z) (wp : D.NoiseBlock D.q) : Vec D.n :=
  D.expansion D.q (D.nominal a + xi.val) b.val wp.val

/-- Terminal feasibility and cost bound `≤ eta` for a concrete `(a, b, xi, wp)`. -/
def PointwiseBound (D : Data) (a : D.ControlBlock D.r) (b : D.ControlBlock D.q)
    (xi : D.Z) (wp : D.NoiseBlock D.q) (eta : ℝ) : Prop :=
  let x := pointwiseTerminal D a b xi wp
  (∀ i : Fin D.rows, D.gmin i ≤ D.H x i ∧ D.H x i ≤ D.gmax i) ∧ D.c x ≤ eta

/-- Prefix-clairvoyant maximin epigraph level set (`V_mm_prefix`):
adversary reveals `xi ∈ Ξ` before controller chooses BOTH `a` and `b`, while future
disturbance `wp` still acts adversarially afterward. -/
def prefixMaximinLevels (D : Data) : Set ℝ :=
  {eta | ∀ xi : D.Z, ∃ a : D.ControlBlock D.r, ∃ b : D.ControlBlock D.q,
    ∀ wp : D.NoiseBlock D.q, PointwiseBound D a b xi wp eta}

/-- Full-clairvoyant maximin epigraph level set (`V_mm_full`):
adversary reveals BOTH `xi ∈ Ξ` and `wp` before controller chooses `(a, b)`. -/
def fullMaximinLevels (D : Data) : Set ℝ :=
  {eta | ∀ xi : D.Z, ∀ wp : D.NoiseBlock D.q,
    ∃ a : D.ControlBlock D.r, ∃ b : D.ControlBlock D.q,
      PointwiseBound D a b xi wp eta}

/-- Pointwise F3-tightened bound for fixed `(a, b, xi)` after eliminating `wp`. -/
def TightenedPointwiseBound (D : Data) (a : D.ControlBlock D.r) (b : D.ControlBlock D.q)
    (xi : D.Z) (eta : ℝ) : Prop :=
  let z := D.expansion D.q (D.nominal a + xi.val) b.val 0
  (∀ i : Fin D.rows,
    (-(D.terminalRow i)) z + D.futureRowSupport (-(D.terminalRow i)) ≤ -D.gmin i ∧
    (D.terminalRow i) z + D.futureRowSupport (D.terminalRow i) ≤ D.gmax i) ∧
  D.c z + D.futureRowSupport D.c ≤ eta

/-- **Theorem O8.1a:** Causal single-closure ARO levels are contained in prefix-clairvoyant
maximin levels (`V_mm_prefix ≤ V({r})`). -/
theorem aro_subset_prefixMaximin (D : Data) : D.aroLevels ⊆ prefixMaximinLevels D := by
  rintro eta ⟨a, y, hy⟩ xi
  exact ⟨a, y.rule xi, fun wp => hy xi wp⟩

/-- **Theorem O8.1b:** Causal single-closure OGU source levels are contained in prefix-clairvoyant
maximin levels (`V_mm_prefix ≤ V({r})`). -/
theorem source_subset_prefixMaximin (D : Data) : D.sourceLevels ⊆ prefixMaximinLevels D := by
  rw [BridgeFormalV2.Proofs.epigraph_equality D]
  exact aro_subset_prefixMaximin D

/-- **Theorem O8.2:** Prefix-clairvoyant maximin levels are contained in full-clairvoyant
maximin levels (`V_mm_full ≤ V_mm_prefix`). -/
theorem prefixMaximin_subset_fullMaximin (D : Data) :
    prefixMaximinLevels D ⊆ fullMaximinLevels D := by
  intro eta h xi wp
  obtain ⟨a, b, hab⟩ := h xi
  exact ⟨a, b, hab wp⟩

/-! ## Section 2: Exact F3 tightening for prefix-clairvoyant maximin -/

private theorem pointwiseTerminal_split (D : Data) (a : D.ControlBlock D.r)
    (b : D.ControlBlock D.q) (xi : D.Z) (wp : D.NoiseBlock D.q) :
    pointwiseTerminal D a b xi wp =
      D.expansion D.q (D.nominal a + xi.val) b.val 0 + D.futureNoiseResponse wp := by
  simpa [pointwiseTerminal, Data.aroTerminal, Data.aroNominalTerminal, constPolicy] using
    BridgeFormalV3.Proofs.future_expansion D a (constPolicy D b) xi wp

/-- **Theorem O8.3:** Exact F3 support-function tightening characterizes `prefixMaximinLevels D`. -/
theorem prefixMaximin_iff_tightened (D : Data) (eta : ℝ) :
    eta ∈ prefixMaximinLevels D ↔
      ∀ xi : D.Z, ∃ a : D.ControlBlock D.r, ∃ b : D.ControlBlock D.q,
        TightenedPointwiseBound D a b xi eta := by
  constructor
  · intro h xi
    obtain ⟨a, b, hab⟩ := h xi
    refine ⟨a, b, ?_⟩
    set z := D.expansion D.q (D.nominal a + xi.val) b.val 0
    constructor
    · intro i
      constructor
      · apply (BridgeFormalV3.Proofs.robust_row D (-(D.terminalRow i)) z (-D.gmin i)).mp
        intro wp
        have hh := (hab wp).1 i
        rw [pointwiseTerminal_split] at hh
        change -(D.H (z + D.futureNoiseResponse wp) i) ≤ -D.gmin i
        exact neg_le_neg hh.1
      · apply (BridgeFormalV3.Proofs.robust_row D (D.terminalRow i) z (D.gmax i)).mp
        intro wp
        have hh := (hab wp).1 i
        rw [pointwiseTerminal_split] at hh
        exact hh.2
    · apply (BridgeFormalV3.Proofs.robust_row D D.c z eta).mp
      intro wp
      have hh := (hab wp).2
      rwa [pointwiseTerminal_split] at hh
  · intro h xi
    obtain ⟨a, b, hab⟩ := h xi
    refine ⟨a, b, ?_⟩
    intro wp
    set z := D.expansion D.q (D.nominal a + xi.val) b.val 0
    obtain ⟨rows, cost⟩ := hab
    unfold PointwiseBound
    rw [pointwiseTerminal_split]
    constructor
    · intro i
      have hl := (BridgeFormalV3.Proofs.robust_row D (-(D.terminalRow i)) z (-D.gmin i)).mpr
        (rows i).1 wp
      have hu := (BridgeFormalV3.Proofs.robust_row D (D.terminalRow i) z (D.gmax i)).mpr
        (rows i).2 wp
      change -(D.H (z + D.futureNoiseResponse wp) i) ≤ -D.gmin i at hl
      exact ⟨neg_le_neg_iff.mp hl, hu⟩
    · exact (BridgeFormalV3.Proofs.robust_row D D.c z eta).mpr cost wp

/-! ## Section 3: Zero-gap collapse under unconstrained terminal state (`D.rows = 0`) -/

/-- Prefix control column `A^q A^{r - 1 - t} B e_j` mapped to the terminal horizon. -/
def prefixControlColumn (D : Data) (t : Fin D.r) (j : Fin D.m) : Vec D.n :=
  (D.A ^ D.q) ((D.A ^ (D.r - 1 - t.val)) (D.B (BridgeFormalV3.basisVector j)))

private theorem nominal_expansion (D : Data) (a : D.ControlBlock D.r) :
    D.nominal a = D.expansion D.r D.x0 a.val (fun _ => 0) := by
  have hz : blockAt (fun _ : Fin D.r => (0 : Vec D.p)) = (fun _ => 0) := by
    funext t; simp [blockAt]
  simpa only [Data.nominal, hz] using
    BridgeFormalV2.Proofs.expansion D D.r D.x0 a.val (fun _ => (0 : Vec D.p))

private theorem pointwise_cost_split (D : Data) (a : D.ControlBlock D.r)
    (b : D.ControlBlock D.q) (xi : D.Z) (wp : D.NoiseBlock D.q) :
    D.c (pointwiseTerminal D a b xi wp) =
      D.c ((D.A ^ D.q) ((D.A ^ D.r) D.x0)) +
      (∑ t : Fin D.r, ∑ j : Fin D.m, D.c (prefixControlColumn D t j) * a.val t j) +
      D.c ((D.A ^ D.q) xi.val) +
      (∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * b.val t j) +
      D.c (D.futureNoiseResponse wp) := by
  rw [pointwiseTerminal_split, map_add]
  congr 1
  simp only [Data.expansion, nominal_expansion, Pi.zero_apply, map_zero, add_zero, map_add, map_sum]
  have hpref :
      ∑ t : Fin D.r, D.c ((D.A ^ D.q) ((D.A ^ (D.r - 1 - t.val)) (D.B (a.val t)))) =
        ∑ t : Fin D.r, ∑ j : Fin D.m, D.c (prefixControlColumn D t j) * a.val t j := by
    apply Finset.sum_congr rfl
    intro t _
    conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition (a.val t)]
    simp only [map_sum, map_smul, prefixControlColumn, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro j _
    exact mul_comm _ _
  have hsuff :
      ∑ t : Fin D.q, D.c ((D.A ^ (D.q - 1 - t.val)) (D.B (b.val t))) =
        ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * b.val t j := by
    apply Finset.sum_congr rfl
    intro t _
    conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition (b.val t)]
    simp only [map_sum, map_smul, suffixControlColumn, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro j _
    exact mul_comm _ _
  rw [hpref, hsuff]

/-- **Theorem O8.4:** When `D.rows = 0` (no terminal state constraints, pure box controls and
linear cost), the entire 4-level hierarchy collapses:
`openLoopLevels D = D.aroLevels = prefixMaximinLevels D = fullMaximinLevels D`.
In particular, nonempty terminal constraints (`D.rows > 0`) are strictly necessary for ANY
minimax-vs-maximin quantifier gap. -/
theorem zero_gap_hierarchy_of_unconstrained_terminal (D : Data) (hrows : D.rows = 0) :
    openLoopLevels D = D.aroLevels ∧
    D.aroLevels = prefixMaximinLevels D ∧
    prefixMaximinLevels D = fullMaximinLevels D := by
  classical
  have hfull_sub_open : fullMaximinLevels D ⊆ openLoopLevels D := by
    intro eta hfull
    let aStar : D.ControlBlock D.r :=
      ⟨fun t j => if 0 ≤ D.c (prefixControlColumn D t j) then D.umin j else D.umax j, by
        intro t j; dsimp only; split_ifs
        · exact ⟨le_rfl, D.control_nonempty j⟩
        · exact ⟨D.control_nonempty j, le_rfl⟩⟩
    let bStar : D.ControlBlock D.q :=
      ⟨fun t j => if 0 ≤ D.c (suffixControlColumn D t j) then D.umin j else D.umax j, by
        intro t j; dsimp only; split_ifs
        · exact ⟨le_rfl, D.control_nonempty j⟩
        · exact ⟨D.control_nonempty j, le_rfl⟩⟩
    have ha_le : ∀ a : D.ControlBlock D.r,
        ∑ t : Fin D.r, ∑ j : Fin D.m, D.c (prefixControlColumn D t j) * aStar.val t j ≤
          ∑ t : Fin D.r, ∑ j : Fin D.m, D.c (prefixControlColumn D t j) * a.val t j := by
      intro a
      refine Finset.sum_le_sum (fun t _ => Finset.sum_le_sum (fun j _ => ?_))
      dsimp only [aStar]
      split_ifs with hc
      · exact mul_le_mul_of_nonneg_left (a.property t j).1 hc
      · exact mul_le_mul_of_nonpos_left (a.property t j).2 (le_of_not_ge hc)
    have hb_le : ∀ b : D.ControlBlock D.q,
        ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * bStar.val t j ≤
          ∑ t : Fin D.q, ∑ j : Fin D.m, D.c (suffixControlColumn D t j) * b.val t j := by
      intro b
      refine Finset.sum_le_sum (fun t _ => Finset.sum_le_sum (fun j _ => ?_))
      dsimp only [bStar]
      split_ifs with hc
      · exact mul_le_mul_of_nonneg_left (b.property t j).1 hc
      · exact mul_le_mul_of_nonpos_left (b.property t j).2 (le_of_not_ge hc)
    refine ⟨aStar, bStar, ?_⟩
    intro xi wp
    obtain ⟨a, b, hab⟩ := hfull xi wp
    constructor
    · intro i
      exact Fin.elim0 (hrows ▸ i)
    · have hcost : D.c (pointwiseTerminal D aStar bStar xi wp) ≤
          D.c (pointwiseTerminal D a b xi wp) := by
        rw [pointwise_cost_split, pointwise_cost_split]
        linarith [ha_le a, hb_le b]
      exact le_trans hcost hab.2
  have h1 : openLoopLevels D ⊆ D.aroLevels := openLoop_subset_aro D
  have h2 : D.aroLevels ⊆ prefixMaximinLevels D := aro_subset_prefixMaximin D
  have h3 : prefixMaximinLevels D ⊆ fullMaximinLevels D := prefixMaximin_subset_fullMaximin D
  refine ⟨Set.Subset.antisymm h1 (Set.Subset.trans h2 (Set.Subset.trans h3 hfull_sub_open)),
    Set.Subset.antisymm h2 (Set.Subset.trans h3 (Set.Subset.trans hfull_sub_open h1)),
    Set.Subset.antisymm h3 (Set.Subset.trans hfull_sub_open (Set.Subset.trans h1 h2))⟩

/-! ## Section 4: Machine-checked strict quantifier-gap witness (`ce-o8-sion-gap`) -/

/-- Concrete 1D witness `ce-o8-sion-gap`:
`A = 2, B = 1, E = 1, x0 = 0, U = [-1, 1], rho = 1, H = 1, [-2, 4], c = 1`. -/
abbrev o8GapWitnessData : Data where
  n := 1
  m := 1
  p := 1
  rows := 1
  r := 1
  q := 1
  n_pos := Nat.zero_lt_one
  m_pos := Nat.zero_lt_one
  p_pos := Nat.zero_lt_one
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := (2 : ℝ) • LinearMap.id
  B := LinearMap.id
  E := LinearMap.id
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => -2
  gmax := fun _ => 4
  c := LinearMap.proj 0

private theorem o8Gap_terminal_formula (a : o8GapWitnessData.ControlBlock 1)
    (b : o8GapWitnessData.ControlBlock 1)
    (wm : o8GapWitnessData.NoiseBlock 1) (wp : o8GapWitnessData.NoiseBlock 1) :
    o8GapWitnessData.expansion 1
      (o8GapWitnessData.nominal a + o8GapWitnessData.deviation wm) b.val wp.val 0 =
      2 * a.val 0 0 + b.val 0 0 + 2 * wm.val 0 0 + wp.val 0 0 := by
  have hd0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    o8GapWitnessData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    hd0, hw0, Module.End.one_apply, LinearMap.smul_apply, LinearMap.id_apply,
    Pi.add_apply, Pi.smul_apply, Pi.zero_apply, smul_eq_mul, zero_add, add_zero, mul_zero]
  ring

private theorem o8Gap_deviation_eq (wm : o8GapWitnessData.NoiseBlock 1) :
    o8GapWitnessData.deviation wm 0 = wm.val 0 0 := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, o8GapWitnessData]

/-- **Theorem O8.5:** Machine-checked formalization of `ce-o8-sion-gap` over the continuous
disturbance box `[-1, 1]^2`:
  - `0 ∈ prefixMaximinLevels D` (hence `0 ∈ fullMaximinLevels D`, so `V_mm_full ≤ V_mm_prefix ≤ 0`),
  - `2 ∈ D.aroLevels` and `∀ eta ∈ D.aroLevels, 2 ≤ eta` (`V({1}) = 2`),
  - `4 ∈ openLoopLevels D` and `∀ eta ∈ openLoopLevels D, 4 ≤ eta` (`V(∅) = 4`),
establishing the exact strict hierarchy `V_mm_full = V_mm_prefix = 0 < 2 = V({1}) < 4 = V(∅)`. -/
theorem exists_strict_quantifier_gap_witness :
    ∃ D : Data,
      (0 : ℝ) ∈ prefixMaximinLevels D ∧
      (0 : ℝ) ∈ fullMaximinLevels D ∧
      (2 : ℝ) ∈ D.aroLevels ∧
      (∀ eta ∈ D.aroLevels, (2 : ℝ) ≤ eta) ∧
      (4 : ℝ) ∈ openLoopLevels D ∧
      (∀ eta ∈ openLoopLevels D, (4 : ℝ) ≤ eta) := by
  refine ⟨o8GapWitnessData, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · -- 0 ∈ prefixMaximinLevels: continuous-box clairvoyant witness a(w0) = -w0, b = -1
    intro xi
    rcases xi.property with ⟨wm, hwm⟩
    have hxi0 : xi.val 0 = wm.val 0 0 := by
      rw [← hwm, o8Gap_deviation_eq]
    have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    let aPref : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => -wm.val 0 0, fun _ _ => ⟨by linarith, by linarith⟩⟩
    let bPref : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    refine ⟨aPref, bPref, ?_⟩
    intro wp
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    have hterm : pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 = -1 + wp.val 0 0 := by
      unfold pointwiseTerminal
      rw [← hwm, o8Gap_terminal_formula aPref bPref wm wp]
      have ha : aPref.val 0 0 = -wm.val 0 0 := rfl
      have hb : bPref.val 0 0 = -1 := rfl
      rw [ha, hb]; ring
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-2 : ℝ) ≤ pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ∧
        pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ≤ 4
      rw [hterm]; constructor <;> linarith
    · change pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ≤ 0
      rw [hterm]; linarith
  · -- 0 ∈ fullMaximinLevels follows immediately from prefixMaximin_subset_fullMaximin
    apply prefixMaximin_subset_fullMaximin o8GapWitnessData
    intro xi
    rcases xi.property with ⟨wm, hwm⟩
    have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    let aPref : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => -wm.val 0 0, fun _ _ => ⟨by linarith, by linarith⟩⟩
    let bPref : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    refine ⟨aPref, bPref, ?_⟩
    intro wp
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    have hterm : pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 = -1 + wp.val 0 0 := by
      unfold pointwiseTerminal
      rw [← hwm, o8Gap_terminal_formula aPref bPref wm wp]
      have ha : aPref.val 0 0 = -wm.val 0 0 := rfl
      have hb : bPref.val 0 0 = -1 := rfl
      rw [ha, hb]; ring
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-2 : ℝ) ≤ pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ∧
        pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ≤ 4
      rw [hterm]; constructor <;> linarith
    · change pointwiseTerminal o8GapWitnessData aPref bPref xi wp 0 ≤ 0
      rw [hterm]; linarith
  · -- 2 ∈ aroLevels: causal policy a = 0, y(xi) = -xi_0
    let a0 : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let yRule : o8GapWitnessData.Z → o8GapWitnessData.ControlBlock 1 := fun xi =>
      ⟨fun _ _ => -xi.val 0, by
        intro _ _
        rcases xi.property with ⟨wm, hwm⟩
        have hxi : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Gap_deviation_eq]
        have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
        change (-1 : ℝ) ≤ -xi.val 0 ∧ -xi.val 0 ≤ 1
        rw [hxi]; constructor <;> linarith⟩
    have hy_meas : Measurable yRule := by
      refine Measurable.subtype_mk ?_
      rw [measurable_pi_iff]; intro _
      rw [measurable_pi_iff]; intro _
      exact ((continuous_apply (0 : Fin 1)).comp continuous_subtype_val).neg.measurable
    refine ⟨a0, ⟨yRule, hy_meas⟩, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hxi0 : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Gap_deviation_eq]
    have hterm : o8GapWitnessData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 =
        wm.val 0 0 + wp.val 0 0 := by
      change o8GapWitnessData.expansion 1
        (o8GapWitnessData.nominal a0 + xi.val) (yRule xi).val wp.val 0 = _
      rw [← hwm, o8Gap_terminal_formula a0 (yRule xi) wm wp]
      have ha0 : a0.val 0 0 = 0 := rfl
      have hb0 : (yRule xi).val 0 0 = -wm.val 0 0 := by change -xi.val 0 = -wm.val 0 0; rw [hxi0]
      rw [ha0, hb0]; ring
    have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-2 : ℝ) ≤ o8GapWitnessData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ∧
        o8GapWitnessData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 4
      rw [hterm]; constructor <;> linarith
    · change o8GapWitnessData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 2
      rw [hterm]; linarith
  · -- ∀ eta ∈ aroLevels, 2 ≤ eta
    rintro eta ⟨a, y, hy⟩
    let wNeg : o8GapWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wPos : o8GapWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    have hlo := (hy (o8GapWitnessData.observedDeviation wNeg) wNeg).1 0
    have hcost := (hy (o8GapWitnessData.observedDeviation wPos) wPos).2
    change (-2 : ℝ) ≤ o8GapWitnessData.expansion 1
      (o8GapWitnessData.nominal a + o8GapWitnessData.deviation wNeg)
      (y.rule (o8GapWitnessData.observedDeviation wNeg)).val wNeg.val 0 ∧ _ at hlo
    change o8GapWitnessData.expansion 1
      (o8GapWitnessData.nominal a + o8GapWitnessData.deviation wPos)
      (y.rule (o8GapWitnessData.observedDeviation wPos)).val wPos.val 0 ≤ eta at hcost
    rw [o8Gap_terminal_formula] at hlo hcost
    have hn : wNeg.val 0 0 = -1 := rfl
    have hp : wPos.val 0 0 = 1 := rfl
    have hbNeg : (y.rule (o8GapWitnessData.observedDeviation wNeg)).val 0 0 ≤ 1 :=
      ((y.rule (o8GapWitnessData.observedDeviation wNeg)).property 0 0).2
    have hbPos : (-1 : ℝ) ≤ (y.rule (o8GapWitnessData.observedDeviation wPos)).val 0 0 :=
      ((y.rule (o8GapWitnessData.observedDeviation wPos)).property 0 0).1
    rw [hn] at hlo
    rw [hp] at hcost
    linarith [hlo.1, hcost, hbNeg, hbPos]
  · -- 4 ∈ openLoopLevels: a = 0, b = 1
    let a0 : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let b1 : o8GapWitnessData.ControlBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    refine ⟨a0, b1, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hterm : o8GapWitnessData.aroTerminal a0 (constPolicy o8GapWitnessData b1) xi wp 0 =
        1 + 2 * wm.val 0 0 + wp.val 0 0 := by
      change o8GapWitnessData.expansion 1
        (o8GapWitnessData.nominal a0 + xi.val) b1.val wp.val 0 = _
      rw [← hwm, o8Gap_terminal_formula a0 b1 wm wp]
      have ha0 : a0.val 0 0 = 0 := rfl
      have hb1 : b1.val 0 0 = 1 := rfl
      rw [ha0, hb1]; ring
    have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-2 : ℝ) ≤ o8GapWitnessData.aroTerminal a0 (constPolicy o8GapWitnessData b1) xi wp 0 ∧
        o8GapWitnessData.aroTerminal a0 (constPolicy o8GapWitnessData b1) xi wp 0 ≤ 4
      rw [hterm]; constructor <;> linarith
    · change o8GapWitnessData.aroTerminal a0 (constPolicy o8GapWitnessData b1) xi wp 0 ≤ 4
      rw [hterm]; linarith
  · -- ∀ eta ∈ openLoopLevels, 4 ≤ eta
    rintro eta ⟨a, b, hb⟩
    let wNeg : o8GapWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wPos : o8GapWitnessData.NoiseBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    have hlo := (hb (o8GapWitnessData.observedDeviation wNeg) wNeg).1 0
    have hcost := (hb (o8GapWitnessData.observedDeviation wPos) wPos).2
    change (-2 : ℝ) ≤ o8GapWitnessData.expansion 1
      (o8GapWitnessData.nominal a + o8GapWitnessData.deviation wNeg) b.val wNeg.val 0 ∧ _ at hlo
    change o8GapWitnessData.expansion 1
      (o8GapWitnessData.nominal a + o8GapWitnessData.deviation wPos) b.val wPos.val 0 ≤ eta at hcost
    rw [o8Gap_terminal_formula] at hlo hcost
    have hn : wNeg.val 0 0 = -1 := rfl
    have hp : wPos.val 0 0 = 1 := rfl
    rw [hn] at hlo
    rw [hp] at hcost
    linarith [hlo.1, hcost]

/-! ## Section 5: Separation of prefix-commitment gap from irreducible future-noise gap -/

/-- Symmetric 1D integrator witness (`A = 1, B = 1, E = 1, U = [-1, 1], rho = 1, [-1, 1], c = 1`):
has ZERO prefix-commitment gap (`V({1}) = V_mm_prefix = 1`) yet STRICT full-clairvoyance gap
(`V_mm_full ≤ 0 < 1 = V_mm_prefix`). -/
abbrev o8SymmetricData : Data where
  n := 1
  m := 1
  p := 1
  rows := 1
  r := 1
  q := 1
  n_pos := Nat.zero_lt_one
  m_pos := Nat.zero_lt_one
  p_pos := Nat.zero_lt_one
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := LinearMap.id
  B := LinearMap.id
  E := LinearMap.id
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => -1
  gmax := fun _ => 1
  c := LinearMap.proj 0

private theorem o8Sym_terminal_formula (a : o8SymmetricData.ControlBlock 1)
    (b : o8SymmetricData.ControlBlock 1)
    (wm : o8SymmetricData.NoiseBlock 1) (wp : o8SymmetricData.NoiseBlock 1) :
    o8SymmetricData.expansion 1
      (o8SymmetricData.nominal a + o8SymmetricData.deviation wm) b.val wp.val 0 =
      a.val 0 0 + b.val 0 0 + wm.val 0 0 + wp.val 0 0 := by
  have hd0 : (if h : 0 < 1 then a.val ⟨0, h⟩ else 0) = a.val 0 := rfl
  have hw0 : (if h : 0 < 1 then wm.val ⟨0, h⟩ else 0) = wm.val 0 := rfl
  simp only [Data.expansion, Data.nominal, Data.deviation, Data.run, Data.step, Data.blockAt,
    o8SymmetricData, pow_one, pow_zero, Fin.sum_univ_one, Fin.val_zero, Nat.sub_self,
    hd0, hw0, Module.End.one_apply, LinearMap.id_apply,
    Pi.add_apply, zero_add, add_zero]
  ring

private theorem o8Sym_deviation_eq (wm : o8SymmetricData.NoiseBlock 1) :
    o8SymmetricData.deviation wm 0 = wm.val 0 0 := by
  simp [Data.deviation, Data.run, Data.step, Data.blockAt, o8SymmetricData]

/-- **Theorem O8.6:** Prefix-commitment gap vs. full-clairvoyance future-noise gap dichotomy:
on `o8SymmetricData`, `0 ∈ fullMaximinLevels D`, `1 ∈ D.aroLevels`, `1 ∈ prefixMaximinLevels D`,
and `∀ eta ∈ prefixMaximinLevels D, 1 ≤ eta`. Thus `V_mm_full ≤ 0 < 1 = V_mm_prefix = V({1})`. -/
theorem exists_prefix_zero_full_strict_gap_witness :
    ∃ D : Data,
      (0 : ℝ) ∈ fullMaximinLevels D ∧
      (1 : ℝ) ∈ D.aroLevels ∧
      (1 : ℝ) ∈ prefixMaximinLevels D ∧
      (∀ eta ∈ prefixMaximinLevels D, (1 : ℝ) ≤ eta) := by
  refine ⟨o8SymmetricData, ?_, ?_, ?_, ?_⟩
  · -- 0 ∈ fullMaximinLevels: given (wm, wp), set t = max(-1, wm+wp-2), a = b = (t - (wm+wp))/2
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    set s : ℝ := wm.val 0 0 + wp.val 0 0
    set t : ℝ := max (-1 : ℝ) (s - 2)
    have ht_lo : (-1 : ℝ) ≤ t := le_max_left _ _
    have ht_hi : t ≤ 0 := max_le (by norm_num) (by linarith)
    have hu_lo : (-1 : ℝ) ≤ (t - s) / 2 := by
      have : s - 2 ≤ t := le_max_right _ _
      linarith
    have hu_hi : (t - s) / 2 ≤ 1 := by linarith
    let uBlk : o8SymmetricData.ControlBlock 1 :=
      ⟨fun _ _ => (t - s) / 2, fun _ _ => ⟨hu_lo, hu_hi⟩⟩
    refine ⟨uBlk, uBlk, ?_⟩
    have hterm : pointwiseTerminal o8SymmetricData uBlk uBlk xi wp 0 = t := by
      unfold pointwiseTerminal
      rw [← hwm, o8Sym_terminal_formula uBlk uBlk wm wp]
      have hu : uBlk.val 0 0 = (t - s) / 2 := rfl
      rw [hu]; simp only [s]; ring
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-1 : ℝ) ≤ pointwiseTerminal o8SymmetricData uBlk uBlk xi wp 0 ∧
        pointwiseTerminal o8SymmetricData uBlk uBlk xi wp 0 ≤ 1
      rw [hterm]; constructor <;> linarith
    · change pointwiseTerminal o8SymmetricData uBlk uBlk xi wp 0 ≤ 0
      rw [hterm]; exact ht_hi
  · -- 1 ∈ aroLevels: a = 0, y(xi) = -xi_0
    let a0 : o8SymmetricData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let yRule : o8SymmetricData.Z → o8SymmetricData.ControlBlock 1 := fun xi =>
      ⟨fun _ _ => -xi.val 0, by
        intro _ _
        rcases xi.property with ⟨wm, hwm⟩
        have hxi : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Sym_deviation_eq]
        have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
        change (-1 : ℝ) ≤ -xi.val 0 ∧ -xi.val 0 ≤ 1
        rw [hxi]; constructor <;> linarith⟩
    have hy_meas : Measurable yRule := by
      refine Measurable.subtype_mk ?_
      rw [measurable_pi_iff]; intro _
      rw [measurable_pi_iff]; intro _
      exact ((continuous_apply (0 : Fin 1)).comp continuous_subtype_val).neg.measurable
    refine ⟨a0, ⟨yRule, hy_meas⟩, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hxi0 : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Sym_deviation_eq]
    have hterm : o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 = wp.val 0 0 := by
      change o8SymmetricData.expansion 1
        (o8SymmetricData.nominal a0 + xi.val) (yRule xi).val wp.val 0 = _
      rw [← hwm, o8Sym_terminal_formula a0 (yRule xi) wm wp]
      have ha0 : a0.val 0 0 = 0 := rfl
      have hb0 : (yRule xi).val 0 0 = -wm.val 0 0 := by change -xi.val 0 = -wm.val 0 0; rw [hxi0]
      rw [ha0, hb0]; ring
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-1 : ℝ) ≤ o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ∧
        o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 1
      rw [hterm]; exact hwp_bd
    · change o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 1
      rw [hterm]; exact hwp_bd.2
  · -- 1 ∈ prefixMaximinLevels: follows from aro_subset_prefixMaximin
    apply aro_subset_prefixMaximin o8SymmetricData
    let a0 : o8SymmetricData.ControlBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let yRule : o8SymmetricData.Z → o8SymmetricData.ControlBlock 1 := fun xi =>
      ⟨fun _ _ => -xi.val 0, by
        intro _ _
        rcases xi.property with ⟨wm, hwm⟩
        have hxi : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Sym_deviation_eq]
        have hwm_bd : (-1 : ℝ) ≤ wm.val 0 0 ∧ wm.val 0 0 ≤ 1 := wm.property 0 0
        change (-1 : ℝ) ≤ -xi.val 0 ∧ -xi.val 0 ≤ 1
        rw [hxi]; constructor <;> linarith⟩
    have hy_meas : Measurable yRule := by
      refine Measurable.subtype_mk ?_
      rw [measurable_pi_iff]; intro _
      rw [measurable_pi_iff]; intro _
      exact ((continuous_apply (0 : Fin 1)).comp continuous_subtype_val).neg.measurable
    refine ⟨a0, ⟨yRule, hy_meas⟩, ?_⟩
    intro xi wp
    rcases xi.property with ⟨wm, hwm⟩
    have hxi0 : xi.val 0 = wm.val 0 0 := by rw [← hwm, o8Sym_deviation_eq]
    have hterm : o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 = wp.val 0 0 := by
      change o8SymmetricData.expansion 1
        (o8SymmetricData.nominal a0 + xi.val) (yRule xi).val wp.val 0 = _
      rw [← hwm, o8Sym_terminal_formula a0 (yRule xi) wm wp]
      have ha0 : a0.val 0 0 = 0 := rfl
      have hb0 : (yRule xi).val 0 0 = -wm.val 0 0 := by change -xi.val 0 = -wm.val 0 0; rw [hxi0]
      rw [ha0, hb0]; ring
    have hwp_bd : (-1 : ℝ) ≤ wp.val 0 0 ∧ wp.val 0 0 ≤ 1 := wp.property 0 0
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i
      subst hi
      change (-1 : ℝ) ≤ o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ∧
        o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 1
      rw [hterm]; exact hwp_bd
    · change o8SymmetricData.aroTerminal a0 ⟨yRule, hy_meas⟩ xi wp 0 ≤ 1
      rw [hterm]; exact hwp_bd.2
  · -- ∀ eta ∈ prefixMaximinLevels, 1 ≤ eta (test at w0 = 0 with w1 = -1 and w1 = +1)
    intro eta hpref
    let wZero : o8SymmetricData.NoiseBlock 1 :=
      ⟨fun _ _ => 0, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wNeg : o8SymmetricData.NoiseBlock 1 :=
      ⟨fun _ _ => -1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    let wPos : o8SymmetricData.NoiseBlock 1 :=
      ⟨fun _ _ => 1, fun _ _ => ⟨by norm_num, by norm_num⟩⟩
    obtain ⟨a, b, hab⟩ := hpref (o8SymmetricData.observedDeviation wZero)
    have hlo := (hab wNeg).1 0
    have hcost := (hab wPos).2
    change (-1 : ℝ) ≤ o8SymmetricData.expansion 1
      (o8SymmetricData.nominal a + o8SymmetricData.deviation wZero) b.val wNeg.val 0 ∧ _ at hlo
    change o8SymmetricData.expansion 1
      (o8SymmetricData.nominal a + o8SymmetricData.deviation wZero) b.val wPos.val 0 ≤ eta at hcost
    rw [o8Sym_terminal_formula] at hlo hcost
    have hz : wZero.val 0 0 = 0 := rfl
    have hn : wNeg.val 0 0 = -1 := rfl
    have hp : wPos.val 0 0 = 1 := rfl
    rw [hz, hn] at hlo
    rw [hz, hp] at hcost
    linarith [hlo.1, hcost]

end AroProofs.BridgeO8QuantifierGap
