import AroProofs.BridgeG1Multistage

/-!
# O4 / O7: Multi-Closure Scheduling Lattice, Supermodular Synergy, and Bidirectional Dominance

Advances open Atlas frontier `conj-o4-closure-scheduling` (`O4 + O7`) strictly over the frozen
core `BridgeFormalV2.Model` / `BridgeFormalV2.Goals` and `AroProofs.BridgeG1Multistage`.

All 4 closure schedules on horizon `T = 3` (`R ⊆ {1, 2}`) are modeled directly via
`BridgeG1Multistage.multistageHistoryLevels D len Set.univ` over the continuous disturbance box
`[-ρ, ρ]^3` (which equals `multistageAroLevels D len Set.univ` by `multistage_history_epigraph_eq_aro`).

Main theorems (zero `sorry`, zero custom axioms):
  1. `schedEmpty_subset_schedR1`: `V({1}) ≤ V(∅)` for every `D : Data`.
  2. `schedEmpty_subset_schedR2`: `V({2}) ≤ V(∅)` for every `D : Data`.
  3. `schedR1_subset_schedR12`: `V({1, 2}) ≤ V({1})` for every `D : Data`.
  4. `schedR2_subset_schedR12`: `V({1, 2}) ≤ V({2})` for every `D : Data`.
  5. `sched_collapse_of_unconstrained_terminal`: When `D.rows = 0`, all four schedule epigraphs
     collapse (`schedEmptyLevels D = schedR1Levels D = schedR2Levels D = schedR12Levels D`).
  6. `exists_strict_supermodular_synergy`: Concrete 4D LTI nilpotent shift-register witness
     (`synergyWitnessData`) proving `V(∅) = V({1}) = V({2}) = 1` and `V({1, 2}) = 0`, hence
     `G(∅) = G({1}) = G({2}) = 0, G({1, 2}) = 1` (strict supermodular defect `+1 > 0`, refuting
     submodularity of `G(R)` and proving greedy selection has 0 approximation ratio).
  7. `exists_strict_submodular_and_early_dominance`: Concrete 1D integrator witness
     (`earlyDomWitnessData`) proving `V(∅) = 4, V({1}) = 2, V({2}) = 3, V({1, 2}) = 2`
     (strict submodular defect `-1 < 0` AND strict early-closure dominance `V({1}) < V({2})`).
  8. `exists_strict_late_dominance`: Concrete 1D contracting witness (`lateDomWitnessData`)
     proving `V(∅) = 3/2, V({1}) = 1, V({2}) = 0, V({1, 2}) = 0`
     (strict late-closure dominance `V({2}) < V({1})`).
-/

noncomputable section
open scoped BigOperators
open BridgeFormalV2 BridgeFormalV2.Data MeasureTheory AroProofs.BridgeG1Multistage

namespace AroProofs.BridgeO4Scheduling

/-! ## Section 1: Horizon `T = 3` closure schedules and monotonicity lattice -/

/-- Horizon `T = 3` open-loop schedule `R = ∅` (`len = [3]`). -/
abbrev lenEmpty : Fin 1 → ℕ := fun _ => 3

/-- Horizon `T = 3` early single-closure schedule `R = {1}` (`len = [1, 2]`). -/
abbrev lenR1 : Fin 2 → ℕ
  | ⟨0, _⟩ => 1
  | ⟨1, _⟩ => 2

/-- Horizon `T = 3` late single-closure schedule `R = {2}` (`len = [2, 1]`). -/
abbrev lenR2 : Fin 2 → ℕ
  | ⟨0, _⟩ => 2
  | ⟨1, _⟩ => 1

/-- Horizon `T = 3` full two-closure schedule `R = {1, 2}` (`len = [1, 1, 1]`). -/
abbrev lenR12 : Fin 3 → ℕ := fun _ => 1

private theorem snocVec_last {β : Type*} {m : ℕ} (f : Fin m → β) (b : β) :
    snocVec f b (Fin.last m) = b :=
  @Fin.snoc_last m (fun _ => β) b f

private theorem snocVec_castSucc {β : Type*} {m : ℕ} (f : Fin m → β) (b : β) (i : Fin m) :
    snocVec f b i.castSucc = f i :=
  @Fin.snoc_castSucc m (fun _ => β) b f i

/-- Epigraph level set for `R = ∅` on `T = 3` over the full continuous disturbance box. -/
def schedEmptyLevels (D : Data) : Set ℝ :=
  multistageHistoryLevels D lenEmpty Set.univ

/-- Epigraph level set for `R = {1}` on `T = 3` over the full continuous disturbance box. -/
def schedR1Levels (D : Data) : Set ℝ :=
  multistageHistoryLevels D lenR1 Set.univ

/-- Epigraph level set for `R = {2}` on `T = 3` over the full continuous disturbance box. -/
def schedR2Levels (D : Data) : Set ℝ :=
  multistageHistoryLevels D lenR2 Set.univ

/-- Epigraph level set for `R = {1, 2}` on `T = 3` over the full continuous disturbance box. -/
def schedR12Levels (D : Data) : Set ℝ :=
  multistageHistoryLevels D lenR12 Set.univ

/-! ### Helper lemmas for splitting 2-step and 3-step runs -/

private theorem run_three_eq (D : Data) (x : Vec D.n) (u0 u1 u2 : Vec D.m) (w0 w1 w2 : Vec D.p) :
    let u3 : Block 3 D.m := ![u0, u1, u2]
    let w3 : Block 3 D.p := ![w0, w1, w2]
    D.run x (blockAt u3) (blockAt w3) 3 =
      D.step (D.step (D.step x u0 w0) u1 w1) u2 w2 := by
  simp [Data.run, Data.blockAt]

private theorem run_two_eq (D : Data) (x : Vec D.n) (u0 u1 : Vec D.m) (w0 w1 : Vec D.p) :
    let u2 : Block 2 D.m := ![u0, u1]
    let w2 : Block 2 D.p := ![w0, w1]
    D.run x (blockAt u2) (blockAt w2) 2 =
      D.step (D.step x u0 w0) u1 w1 := by
  simp [Data.run, Data.blockAt]

private theorem run_one_eq (D : Data) (x : Vec D.n) (u0 : Vec D.m) (w0 : Vec D.p) :
    let u1 : Block 1 D.m := ![u0]
    let w1 : Block 1 D.p := ![w0]
    D.run x (blockAt u1) (blockAt w1) 1 = D.step x u0 w0 := by
  simp [Data.run, Data.blockAt]

private theorem run_block_three (D : Data) (x : Vec D.n)
    (u : D.ControlBlock 3) (w : D.NoiseBlock 3) :
    D.run x (blockAt u.val) (blockAt w.val) 3 =
      D.step (D.step (D.step x (u.val 0) (w.val 0)) (u.val 1) (w.val 1)) (u.val 2) (w.val 2) := by
  simp [Data.run, Data.blockAt]

private theorem run_block_two (D : Data) (x : Vec D.n)
    (u : D.ControlBlock 2) (w : D.NoiseBlock 2) :
    D.run x (blockAt u.val) (blockAt w.val) 2 =
      D.step (D.step x (u.val 0) (w.val 0)) (u.val 1) (w.val 1) := by
  simp [Data.run, Data.blockAt]

private theorem run_block_one (D : Data) (x : Vec D.n)
    (u : D.ControlBlock 1) (w : D.NoiseBlock 1) :
    D.run x (blockAt u.val) (blockAt w.val) 1 = D.step x (u.val 0) (w.val 0) := by
  simp [Data.run, Data.blockAt]

private abbrev mkNoise1 (D : Data) (v : Vec D.p) (hv : D.NoiseOK v) : D.NoiseBlock 1 :=
  ⟨fun _ => v, fun _ => hv⟩

private abbrev mkNoise2 (D : Data) (v0 v1 : Vec D.p) (h0 : D.NoiseOK v0) (h1 : D.NoiseOK v1) :
    D.NoiseBlock 2 :=
  ⟨![v0, v1], fun t => by fin_cases t <;> assumption⟩

private abbrev mkNoise3 (D : Data) (v0 v1 v2 : Vec D.p)
    (h0 : D.NoiseOK v0) (h1 : D.NoiseOK v1) (h2 : D.NoiseOK v2) : D.NoiseBlock 3 :=
  ⟨![v0, v1, v2], fun t => by fin_cases t <;> assumption⟩

private abbrev mkCtrl1 (D : Data) (u0 : Vec D.m) (h0 : D.ControlOK u0) : D.ControlBlock 1 :=
  ⟨fun _ => u0, fun _ => h0⟩

private abbrev mkCtrl2 (D : Data) (u0 u1 : Vec D.m) (h0 : D.ControlOK u0) (h1 : D.ControlOK u1) :
    D.ControlBlock 2 :=
  ⟨![u0, u1], fun t => by fin_cases t <;> assumption⟩

private abbrev mkCtrl3 (D : Data) (u0 u1 u2 : Vec D.m)
    (h0 : D.ControlOK u0) (h1 : D.ControlOK u1) (h2 : D.ControlOK u2) : D.ControlBlock 3 :=
  ⟨![u0, u1, u2], fun t => by fin_cases t <;> assumption⟩

private theorem term_empty_eq (D : Data) (P : HistoryStatePolicy D lenEmpty)
    (w : MultiNoise D lenEmpty) :
    let u := P.rule 0 Fin.elim0
    historyTerminalState D P w =
      D.step (D.step (D.step D.x0 (u.val 0) ((w 0).val 0)) (u.val 1) ((w 0).val 1))
        (u.val 2) ((w 0).val 2) := by
  dsimp only [historyTerminalState, historyStateRollout, snocVec_last, lastOrInit]
  exact run_block_three D D.x0 (P.rule 0 Fin.elim0) (w 0)

private theorem term_r1_eq (D : Data) (P : HistoryStatePolicy D lenR1)
    (w : MultiNoise D lenR1) :
    let u0 := P.rule 0 Fin.elim0
    let x1 := D.step D.x0 (u0.val 0) ((w 0).val 0)
    let u12 := P.rule 1 (fun _ => x1)
    historyTerminalState D P w =
      D.step (D.step x1 (u12.val 0) ((w 1).val 0)) (u12.val 1) ((w 1).val 1) := by
  have hx1 : historyStateRollout D P w 1 (by omega) =
      fun _ : Fin 1 => D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0) := by
    funext i
    have hi : i = Fin.last 0 := Fin.eq_zero i
    rw [hi, historyStateRollout, snocVec_last]
    exact run_block_one D D.x0 (P.rule 0 Fin.elim0) (w 0)
  dsimp only [historyTerminalState]
  rw [historyStateRollout, snocVec_last, hx1]
  dsimp only [lastOrInit]
  exact run_block_two D _ _ (w 1)

private theorem term_r2_eq (D : Data) (P : HistoryStatePolicy D lenR2)
    (w : MultiNoise D lenR2) :
    let u01 := P.rule 0 Fin.elim0
    let x2 := D.step (D.step D.x0 (u01.val 0) ((w 0).val 0)) (u01.val 1) ((w 0).val 1)
    let u2 := P.rule 1 (fun _ => x2)
    historyTerminalState D P w = D.step x2 (u2.val 0) ((w 1).val 0) := by
  have hx2 : historyStateRollout D P w 1 (by omega) =
      fun _ : Fin 1 =>
        D.step (D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P.rule 0 Fin.elim0).val 1) ((w 0).val 1) := by
    funext i
    have hi : i = Fin.last 0 := Fin.eq_zero i
    rw [hi, historyStateRollout, snocVec_last]
    exact run_block_two D D.x0 (P.rule 0 Fin.elim0) (w 0)
  dsimp only [historyTerminalState]
  rw [historyStateRollout, snocVec_last, hx2]
  dsimp only [lastOrInit]
  exact run_block_one D _ _ (w 1)

private theorem term_r12_eq (D : Data) (P : HistoryStatePolicy D lenR12)
    (w : MultiNoise D lenR12) :
    let u0 := P.rule 0 Fin.elim0
    let x1 := D.step D.x0 (u0.val 0) ((w 0).val 0)
    let u1 := P.rule 1 (fun _ => x1)
    let x2 := D.step x1 (u1.val 0) ((w 1).val 0)
    let u2 := P.rule 2 ![x1, x2]
    historyTerminalState D P w = D.step x2 (u2.val 0) ((w 2).val 0) := by
  have hx1 : historyStateRollout D P w 1 (by omega) =
      fun _ : Fin 1 => D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0) := by
    funext i
    have hi : i = Fin.last 0 := Fin.eq_zero i
    rw [hi, historyStateRollout, snocVec_last]
    exact run_block_one D D.x0 (P.rule 0 Fin.elim0) (w 0)
  have hx2 : historyStateRollout D P w 2 (by omega) =
      ![D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0),
        D.step (D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P.rule 1 (fun _ => D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0)
          ((w 1).val 0)] := by
    funext i
    fin_cases i
    · change historyStateRollout D P w 2 (by omega) (Fin.castSucc 0) = _
      rw [historyStateRollout, snocVec_castSucc, hx1]; rfl
    · change historyStateRollout D P w 2 (by omega) (Fin.last 1) = _
      rw [historyStateRollout, snocVec_last, hx1]
      exact run_block_one D _ _ (w 1)
  dsimp only [historyTerminalState]
  rw [historyStateRollout, snocVec_last, hx2]
  exact run_block_one D _ _ (w 2)

/-- **Theorem O4.7a:** Adding a closure at `r = 1` never degrades the epigraph (`V({1}) ≤ V(∅)`). -/
theorem schedEmpty_subset_schedR1 (D : Data) :
    schedEmptyLevels D ⊆ schedR1Levels D := by
  rintro eta ⟨P, hP⟩
  let u := P.rule 0 Fin.elim0
  let u0 : D.ControlBlock 1 := mkCtrl1 D (u.val 0) (u.property 0)
  let u12 : D.ControlBlock 2 := mkCtrl2 D (u.val 1) (u.val 2) (u.property 1) (u.property 2)
  let P1 : HistoryStatePolicy D lenR1 :=
    { rule := fun j _ =>
        match j with
        | ⟨0, _⟩ => u0
        | ⟨1, _⟩ => u12
      borel := fun j => by fin_cases j <;> exact measurable_const }
  refine ⟨P1, ?_⟩
  intro w _
  let wE : MultiNoise D lenEmpty := fun _ =>
    mkNoise3 D ((w 0).val 0) ((w 1).val 0) ((w 1).val 1)
      ((w 0).property 0) ((w 1).property 0) ((w 1).property 1)
  have hterm : historyTerminalState D P1 w = historyTerminalState D P wE := by
    rw [term_r1_eq, term_empty_eq]
    rfl
  rw [hterm]
  exact hP wE trivial

/-- **Theorem O4.7b:** Adding a closure at `r = 2` never degrades the epigraph (`V({2}) ≤ V(∅)`). -/
theorem schedEmpty_subset_schedR2 (D : Data) :
    schedEmptyLevels D ⊆ schedR2Levels D := by
  rintro eta ⟨P, hP⟩
  let u := P.rule 0 Fin.elim0
  let u01 : D.ControlBlock 2 := mkCtrl2 D (u.val 0) (u.val 1) (u.property 0) (u.property 1)
  let u2 : D.ControlBlock 1 := mkCtrl1 D (u.val 2) (u.property 2)
  let P2 : HistoryStatePolicy D lenR2 :=
    { rule := fun j _ =>
        match j with
        | ⟨0, _⟩ => u01
        | ⟨1, _⟩ => u2
      borel := fun j => by fin_cases j <;> exact measurable_const }
  refine ⟨P2, ?_⟩
  intro w _
  let wE : MultiNoise D lenEmpty := fun _ =>
    mkNoise3 D ((w 0).val 0) ((w 0).val 1) ((w 1).val 0)
      ((w 0).property 0) ((w 0).property 1) ((w 1).property 0)
  have hterm : historyTerminalState D P2 w = historyTerminalState D P wE := by
    rw [term_r2_eq, term_empty_eq]
    rfl
  rw [hterm]
  exact hP wE trivial

/-- **Theorem O4.7c:** Refining `{1}` to `{1, 2}` never degrades the epigraph (`V({1,2}) ≤ V({1})`). -/
theorem schedR1_subset_schedR12 (D : Data) :
    schedR1Levels D ⊆ schedR12Levels D := by
  rintro eta ⟨P, hP⟩
  let P12 : HistoryStatePolicy D lenR12 :=
    { rule := fun j hist =>
        match j, hist with
        | ⟨0, _⟩, _ => P.rule 0 Fin.elim0
        | ⟨1, _⟩, h =>
            let b := P.rule 1 h
            mkCtrl1 D (b.val 0) (b.property 0)
        | ⟨2, _⟩, h =>
            let b := P.rule 1 (fun _ => h (0 : Fin 2))
            mkCtrl1 D (b.val 1) (b.property 1)
      borel := fun j => by
        fin_cases j
        · exact measurable_const
        · refine Measurable.subtype_mk ?_
          rw [measurable_pi_iff]; intro _
          exact (measurable_pi_apply (0 : Fin 2)).comp (measurable_subtype_coe.comp (P.borel 1))
        · refine Measurable.subtype_mk ?_
          rw [measurable_pi_iff]; intro _
          have hproj : Measurable (fun h : Fin 2 → Vec D.n => fun _ : Fin 1 => h (0 : Fin 2)) := by
            rw [measurable_pi_iff]; intro _
            exact measurable_pi_apply (0 : Fin 2)
          exact (measurable_pi_apply (1 : Fin 2)).comp
            (measurable_subtype_coe.comp ((P.borel 1).comp hproj)) }
  refine ⟨P12, ?_⟩
  intro w _
  let w1 : MultiNoise D lenR1 := fun j =>
    match j with
    | ⟨0, _⟩ => w 0
    | ⟨1, _⟩ => mkNoise2 D ((w 1).val 0) ((w 2).val 0) ((w 1).property 0) ((w 2).property 0)
  have hterm : historyTerminalState D P12 w = historyTerminalState D P w1 := by
    rw [term_r12_eq, term_r1_eq]
    rfl
  rw [hterm]
  exact hP w1 trivial

/-- **Theorem O4.7d:** Refining `{2}` to `{1, 2}` never degrades the epigraph (`V({1,2}) ≤ V({2})`). -/
theorem schedR2_subset_schedR12 (D : Data) :
    schedR2Levels D ⊆ schedR12Levels D := by
  rintro eta ⟨P, hP⟩
  let u01 := P.rule 0 Fin.elim0
  let P12 : HistoryStatePolicy D lenR12 :=
    { rule := fun j hist =>
        match j, hist with
        | ⟨0, _⟩, _ => mkCtrl1 D (u01.val 0) (u01.property 0)
        | ⟨1, _⟩, _ => mkCtrl1 D (u01.val 1) (u01.property 1)
        | ⟨2, _⟩, h => P.rule 1 (fun _ => h (1 : Fin 2))
      borel := fun j => by
        fin_cases j
        · exact measurable_const
        · exact measurable_const
        · have hproj : Measurable (fun h : Fin 2 → Vec D.n => fun _ : Fin 1 => h (1 : Fin 2)) := by
            rw [measurable_pi_iff]; intro _
            exact measurable_pi_apply (1 : Fin 2)
          exact (P.borel 1).comp hproj }
  refine ⟨P12, ?_⟩
  intro w _
  let w2 : MultiNoise D lenR2 := fun j =>
    match j with
    | ⟨0, _⟩ => mkNoise2 D ((w 0).val 0) ((w 1).val 0) ((w 0).property 0) ((w 1).property 0)
    | ⟨1, _⟩ => w 2
  have hterm : historyTerminalState D P12 w = historyTerminalState D P w2 := by
    rw [term_r12_eq, term_r2_eq]
    rfl
  rw [hterm]
  exact hP w2 trivial

/-! ## Section 2: Total multi-closure collapse when `D.rows = 0` -/

private theorem step3_cost_split (D : Data) (u0 u1 u2 : Vec D.m) (w0 w1 w2 : Vec D.p) :
    D.c (D.step (D.step (D.step D.x0 u0 w0) u1 w1) u2 w2) =
      D.c ((D.A ^ 3) D.x0) +
        (∑ j : Fin D.m, D.c ((D.A ^ 2) (D.B (BridgeFormalV3.basisVector j))) * u0 j) +
        (∑ j : Fin D.m, D.c (D.A (D.B (BridgeFormalV3.basisVector j))) * u1 j) +
        (∑ j : Fin D.m, D.c (D.B (BridgeFormalV3.basisVector j)) * u2 j) +
        D.c ((D.A ^ 2) (D.E w0)) + D.c (D.A (D.E w1)) + D.c (D.E w2) := by
  have hlin : ∀ (L : Vec D.m →ₗ[ℝ] ℝ) (v : Vec D.m),
      L v = ∑ j : Fin D.m, L (BridgeFormalV3.basisVector j) * v j := by
    intro L v
    conv_lhs => rw [BridgeFormalV3.Proofs.basis_decomposition v]
    simp only [map_sum, map_smul, smul_eq_mul]
    apply Finset.sum_congr rfl
    intro j _
    exact mul_comm _ _
  have h0 := hlin ((D.c.comp (D.A ^ 2)).comp D.B) u0
  have h1 := hlin ((D.c.comp D.A).comp D.B) u1
  have h2 := hlin (D.c.comp D.B) u2
  simp only [LinearMap.comp_apply, pow_succ', pow_zero, Module.End.mul_apply,
    Module.End.one_apply] at h0 h1 h2
  simp only [Data.step, map_add, pow_succ', pow_zero, Module.End.mul_apply, Module.End.one_apply]
  rw [h0, h1, h2]
  ring

/-- **Theorem O4.8:** When `D.rows = 0` (no terminal state constraints, pure box controls and
linear cost), ALL FOUR `T = 3` closure schedules collapse to the open-loop epigraph:
`schedEmptyLevels D = schedR1Levels D = schedR2Levels D = schedR12Levels D`. -/
theorem sched_collapse_of_unconstrained_terminal (D : Data) (hrows : D.rows = 0) :
    schedEmptyLevels D = schedR1Levels D ∧
    schedEmptyLevels D = schedR2Levels D ∧
    schedEmptyLevels D = schedR12Levels D := by
  classical
  have h12_sub_empty : schedR12Levels D ⊆ schedEmptyLevels D := by
    rintro eta ⟨P, hP⟩
    let mkOpt : (Vec D.m →ₗ[ℝ] ℝ) → Vec D.m := fun L j =>
      if 0 ≤ L (BridgeFormalV3.basisVector j) then D.umin j else D.umax j
    have hOpt_ok : ∀ L : Vec D.m →ₗ[ℝ] ℝ, D.ControlOK (mkOpt L) := by
      intro L j
      dsimp only [mkOpt]
      split_ifs
      · exact ⟨le_rfl, D.control_nonempty j⟩
      · exact ⟨D.control_nonempty j, le_rfl⟩
    have hOpt_le : ∀ (L : Vec D.m →ₗ[ℝ] ℝ) (v : Vec D.m), D.ControlOK v →
        ∑ j : Fin D.m, L (BridgeFormalV3.basisVector j) * mkOpt L j ≤
          ∑ j : Fin D.m, L (BridgeFormalV3.basisVector j) * v j := by
      intro L v hv
      refine Finset.sum_le_sum (fun j _ => ?_)
      dsimp only [mkOpt]
      split_ifs with hpos
      · exact mul_le_mul_of_nonneg_left (hv j).1 hpos
      · exact mul_le_mul_of_nonpos_left (hv j).2 (le_of_not_ge hpos)
    let L0 : Vec D.m →ₗ[ℝ] ℝ := (D.c.comp (D.A ^ 2)).comp D.B
    let L1 : Vec D.m →ₗ[ℝ] ℝ := (D.c.comp D.A).comp D.B
    let L2 : Vec D.m →ₗ[ℝ] ℝ := D.c.comp D.B
    let uStar : D.ControlBlock 3 :=
      mkCtrl3 D (mkOpt L0) (mkOpt L1) (mkOpt L2) (hOpt_ok L0) (hOpt_ok L1) (hOpt_ok L2)
    let PE : HistoryStatePolicy D lenEmpty :=
      { rule := fun _ _ => uStar
        borel := fun _ => measurable_const }
    refine ⟨PE, ?_⟩
    intro w _
    let w12 : MultiNoise D lenR12 := fun j =>
      match j with
      | ⟨0, _⟩ => mkNoise1 D ((w 0).val 0) ((w 0).property 0)
      | ⟨1, _⟩ => mkNoise1 D ((w 0).val 1) ((w 0).property 1)
      | ⟨2, _⟩ => mkNoise1 D ((w 0).val 2) ((w 0).property 2)
    have hP_cost : D.c (historyTerminalState D P w12) ≤ eta := (hP w12 trivial).2
    constructor
    · intro i
      exact absurd i.isLt (by omega)
    · rw [term_empty_eq]
      rw [term_r12_eq] at hP_cost
      rw [step3_cost_split] at hP_cost ⊢
      have hu0_ok : D.ControlOK ((P.rule 0 Fin.elim0).val 0) := (P.rule 0 Fin.elim0).property 0
      have hu1_ok : D.ControlOK ((P.rule 1 (fun _ => D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w12 0).val 0))).val 0) :=
        (P.rule 1 _).property 0
      have hu2_ok : D.ControlOK ((P.rule 2 ![D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w12 0).val 0),
          D.step (D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w12 0).val 0))
            ((P.rule 1 (fun _ => D.step D.x0 ((P.rule 0 Fin.elim0).val 0) ((w12 0).val 0))).val 0)
            ((w12 1).val 0)]).val 0) :=
        (P.rule 2 _).property 0
      have hle0 := hOpt_le L0 _ hu0_ok
      have hle1 := hOpt_le L1 _ hu1_ok
      have hle2 := hOpt_le L2 _ hu2_ok
      simp only [L0, L1, L2, LinearMap.comp_apply] at hle0 hle1 hle2
      change D.c ((D.A ^ 3) D.x0) +
          (∑ j : Fin D.m, D.c ((D.A ^ 2) (D.B (BridgeFormalV3.basisVector j))) * mkOpt L0 j) +
          (∑ j : Fin D.m, D.c (D.A (D.B (BridgeFormalV3.basisVector j))) * mkOpt L1 j) +
          (∑ j : Fin D.m, D.c (D.B (BridgeFormalV3.basisVector j)) * mkOpt L2 j) +
          D.c ((D.A ^ 2) (D.E ((w 0).val 0))) + D.c (D.A (D.E ((w 0).val 1))) +
          D.c (D.E ((w 0).val 2)) ≤ eta
      have hw0 : (w12 0).val 0 = (w 0).val 0 := rfl
      have hw1 : (w12 1).val 0 = (w 0).val 1 := rfl
      have hw2 : (w12 2).val 0 = (w 0).val 2 := rfl
      simp only [hw0, hw1, hw2] at hP_cost hle1 hle2
      linarith
  have hE1 : schedEmptyLevels D = schedR1Levels D :=
    Set.Subset.antisymm (schedEmpty_subset_schedR1 D)
      ((schedR1_subset_schedR12 D).trans h12_sub_empty)
  have hE2 : schedEmptyLevels D = schedR2Levels D :=
    Set.Subset.antisymm (schedEmpty_subset_schedR2 D)
      ((schedR2_subset_schedR12 D).trans h12_sub_empty)
  have hE12 : schedEmptyLevels D = schedR12Levels D :=
    Set.Subset.antisymm ((schedEmpty_subset_schedR1 D).trans (schedR1_subset_schedR12 D))
      h12_sub_empty
  exact ⟨hE1, hE2, hE12⟩

/-! ## Section 3: Strict Supermodular Synergy Witness (Refuting Submodularity of `G(R)`) -/

/-- 4D nilpotent shift operator `A : e3 ↦ e0 ↦ e1 ↦ e2 ↦ 0`. -/
def shift4A : Vec 4 →ₗ[ℝ] Vec 4 where
  toFun x := ![x 3, x 0, x 1, 0]
  map_add' x y := by ext i; fin_cases i <;> simp
  map_smul' r x := by ext i; fin_cases i <;> simp

/-- Input map `B : u ↦ u • e0`. -/
def shift4B : Vec 1 →ₗ[ℝ] Vec 4 where
  toFun u := ![u 0, 0, 0, 0]
  map_add' x y := by ext i; fin_cases i <;> simp
  map_smul' r x := by ext i; fin_cases i <;> simp

/-- Disturbance map `E : w ↦ w • e3`. -/
def shift4E : Vec 1 →ₗ[ℝ] Vec 4 where
  toFun w := ![0, 0, 0, w 0]
  map_add' x y := by ext i; fin_cases i <;> simp
  map_smul' r x := by ext i; fin_cases i <;> simp

/-- Terminal constraint map `H x = (x₂ + x₁, x₂ - x₁, x₂ + x₀, x₂ - x₀)`. -/
def shift4H : Vec 4 →ₗ[ℝ] Vec 4 where
  toFun x := ![x 2 + x 1, x 2 - x 1, x 2 + x 0, x 2 - x 0]
  map_add' x y := by ext i; fin_cases i <;> simp <;> ring
  map_smul' r x := by ext i; fin_cases i <;> simp <;> ring

/-- 4D LTI nilpotent shift-register witness for strict supermodular synergy (`defect = +1`). -/
abbrev synergyWitnessData : Data where
  n := 4
  m := 1
  p := 1
  rows := 4
  r := 1
  q := 1
  n_pos := by omega
  m_pos := Nat.zero_lt_one
  p_pos := Nat.zero_lt_one
  r_pos := Nat.zero_lt_one
  q_pos := Nat.zero_lt_one
  A := shift4A
  B := shift4B
  E := shift4E
  x0 := 0
  umin := fun _ => -1
  umax := fun _ => 1
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := shift4H
  gmin := fun _ => 0
  gmax := fun _ => 10
  c := LinearMap.proj 2

private theorem synergy_step1 (u0 w0 : Vec 1) :
    synergyWitnessData.step 0 u0 w0 = ![u0 0, 0, 0, w0 0] := by
  ext i
  fin_cases i <;> simp [Data.step, synergyWitnessData, shift4A, shift4B, shift4E]

private theorem synergy_step2 (u0 u1 w0 w1 : Vec 1) :
    synergyWitnessData.step (synergyWitnessData.step 0 u0 w0) u1 w1 =
      ![w0 0 + u1 0, u0 0, 0, w1 0] := by
  rw [synergy_step1]
  ext i
  fin_cases i <;> simp [Data.step, synergyWitnessData, shift4A, shift4B, shift4E]

private theorem synergy_step3 (u0 u1 u2 w0 w1 w2 : Vec 1) :
    synergyWitnessData.step (synergyWitnessData.step (synergyWitnessData.step 0 u0 w0) u1 w1) u2 w2 =
      ![w1 0 + u2 0, w0 0 + u1 0, u0 0, w2 0] := by
  rw [synergy_step2]
  ext i
  fin_cases i <;> simp [Data.step, synergyWitnessData, shift4A, shift4B, shift4E]

private theorem shift4H_bounds (a b c d : ℝ)
    (h0 : 0 ≤ c + b ∧ c + b ≤ 10) (h1 : 0 ≤ c - b ∧ c - b ≤ 10)
    (h2 : 0 ≤ c + a ∧ c + a ≤ 10) (h3 : 0 ≤ c - a ∧ c - a ≤ 10) :
    ∀ i : Fin 4, (0 : ℝ) ≤ shift4H ![a, b, c, d] i ∧ shift4H ![a, b, c, d] i ≤ 10 := by
  intro i
  fin_cases i
  · exact h0
  · exact h1
  · exact h2
  · exact h3

private abbrev vec1 (v : ℝ) : Vec 1 := fun _ => v

private abbrev noise1Synergy (v : ℝ) (h1 : (-1 : ℝ) ≤ v) (h2 : v ≤ 1) :
    synergyWitnessData.NoiseBlock 1 :=
  ⟨fun _ _ => v, fun _ _ => ⟨h1, h2⟩⟩

/-- **Theorem O4.9 (Refutation of Submodularity of `G(R)`):**
On the 4D LTI nilpotent shift-register system `synergyWitnessData`:
  - `V(∅) = 1`, `V({1}) = 1`, `V({2}) = 1`, `V({1, 2}) = 0`,
hence `G(∅) = G({1}) = G({2}) = 0` and `G({1, 2}) = 1` (strict supermodular defect `+1 > 0`). -/
theorem exists_strict_supermodular_synergy :
    ∃ D : Data,
      ((1 : ℝ) ∈ schedEmptyLevels D ∧ ∀ eta ∈ schedEmptyLevels D, (1 : ℝ) ≤ eta) ∧
      ((1 : ℝ) ∈ schedR1Levels D ∧ ∀ eta ∈ schedR1Levels D, (1 : ℝ) ≤ eta) ∧
      ((1 : ℝ) ∈ schedR2Levels D ∧ ∀ eta ∈ schedR2Levels D, (1 : ℝ) ≤ eta) ∧
      ((0 : ℝ) ∈ schedR12Levels D ∧ ∀ eta ∈ schedR12Levels D, (0 : ℝ) ≤ eta) := by
  have h1_empty : (1 : ℝ) ∈ schedEmptyLevels synergyWitnessData := by
    let uE : synergyWitnessData.ControlBlock 3 :=
      mkCtrl3 synergyWitnessData (vec1 1) (vec1 0) (vec1 0)
        (fun _ => ⟨by norm_num, by norm_num⟩)
        (fun _ => ⟨by norm_num, by norm_num⟩)
        (fun _ => ⟨by norm_num, by norm_num⟩)
    let PE : HistoryStatePolicy synergyWitnessData lenEmpty :=
      { rule := fun _ _ => uE, borel := fun _ => measurable_const }
    refine ⟨PE, ?_⟩
    intro w _
    rw [term_empty_eq, synergy_step3]
    have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
    have hw1 : (-1 : ℝ) ≤ (w 0).val 1 0 ∧ (w 0).val 1 0 ≤ 1 := (w 0).property 1 0
    have hu0 : (PE.rule 0 Fin.elim0).val 0 0 = 1 := rfl
    have hu1 : (PE.rule 0 Fin.elim0).val 1 0 = 0 := rfl
    have hu2 : (PE.rule 0 Fin.elim0).val 2 0 = 0 := rfl
    constructor
    · exact shift4H_bounds _ _ _ _
        (by rw [hu0, hu1]; constructor <;> linarith)
        (by rw [hu0, hu1]; constructor <;> linarith)
        (by rw [hu0, hu2]; constructor <;> linarith)
        (by rw [hu0, hu2]; constructor <;> linarith)
    · change (LinearMap.proj 2 : Vec 4 →ₗ[ℝ] ℝ) _ ≤ (1 : ℝ)
      simp only [LinearMap.proj_apply, Matrix.cons_val, Matrix.head_cons, Matrix.tail_cons]
      rw [hu0]
  have hr1_ge1 : ∀ eta ∈ schedR1Levels synergyWitnessData, (1 : ℝ) ≤ eta := by
    rintro eta ⟨P, hP⟩
    -- Fix w0 = 0, vary w1 ∈ {-1, +1}; u2 cannot see w1!
    let wP : MultiNoise synergyWitnessData lenR1 := fun j =>
      match j with
      | ⟨0, _⟩ => noise1Synergy 0 (by norm_num) (by norm_num)
      | ⟨1, _⟩ => mkNoise2 synergyWitnessData (vec1 1) (vec1 0)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
    let wM : MultiNoise synergyWitnessData lenR1 := fun j =>
      match j with
      | ⟨0, _⟩ => noise1Synergy 0 (by norm_num) (by norm_num)
      | ⟨1, _⟩ => mkNoise2 synergyWitnessData (vec1 (-1)) (vec1 0)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
    have hrow2 := ((hP wM trivial).1 2).1
    have hrow3 := ((hP wP trivial).1 3).1
    have hcost := (hP wP trivial).2
    rw [term_r1_eq, synergy_step3] at hrow2 hrow3 hcost
    simp only [synergyWitnessData, shift4H, wP, wM, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val, LinearMap.coe_mk, AddHom.coe_mk,
      LinearMap.proj_apply] at hrow2 hrow3 hcost
    linarith
  refine ⟨synergyWitnessData, ?_, ?_, ?_, ?_⟩
  · -- V(∅) = 1
    exact ⟨h1_empty, fun eta heta => hr1_ge1 eta (schedEmpty_subset_schedR1 synergyWitnessData heta)⟩
  · -- V({1}) = 1
    exact ⟨schedEmpty_subset_schedR1 synergyWitnessData h1_empty, hr1_ge1⟩
  · -- V({2}) = 1
    refine ⟨schedEmpty_subset_schedR2 synergyWitnessData h1_empty, ?_⟩
    rintro eta ⟨P, hP⟩
    -- Vary w0 ∈ {-1, +1}; u1 is chosen before t = 2 so it cannot see w0!
    let wP : MultiNoise synergyWitnessData lenR2 := fun j =>
      match j with
      | ⟨0, _⟩ => mkNoise2 synergyWitnessData (vec1 1) (vec1 0)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      | ⟨1, _⟩ => noise1Synergy 0 (by norm_num) (by norm_num)
    let wM : MultiNoise synergyWitnessData lenR2 := fun j =>
      match j with
      | ⟨0, _⟩ => mkNoise2 synergyWitnessData (vec1 (-1)) (vec1 0)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      | ⟨1, _⟩ => noise1Synergy 0 (by norm_num) (by norm_num)
    have hrow0 := ((hP wM trivial).1 0).1
    have hrow1 := ((hP wP trivial).1 1).1
    have hcost := (hP wP trivial).2
    rw [term_r2_eq, synergy_step3] at hrow0 hrow1 hcost
    simp only [synergyWitnessData, shift4H, wP, wM, Matrix.cons_val_zero,
      Matrix.cons_val_one, Matrix.cons_val, LinearMap.coe_mk, AddHom.coe_mk,
      LinearMap.proj_apply] at hrow0 hrow1 hcost
    linarith
  · -- V({1, 2}) = 0
    have h0_r12 : (0 : ℝ) ∈ schedR12Levels synergyWitnessData := by
      let clamp : ℝ → ℝ := fun z => max (-1) (min 1 z)
      have hclamp_bd : ∀ z : ℝ, (-1 : ℝ) ≤ clamp z ∧ clamp z ≤ 1 := by
        intro z
        exact ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩
      have hclamp_eq : ∀ z : ℝ, (-1 : ℝ) ≤ z → z ≤ 1 → clamp z = z := by
        intro z h1 h2
        dsimp only [clamp]
        rw [min_eq_right h2, max_eq_right h1]
      have hclamp_cont : Continuous clamp :=
        continuous_const.max (continuous_const.min continuous_id)
      let P12 : HistoryStatePolicy synergyWitnessData lenR12 :=
        { rule := fun j hist =>
            match j, hist with
            | ⟨0, _⟩, _ => mkCtrl1 synergyWitnessData (vec1 0) (fun _ => ⟨by norm_num, by norm_num⟩)
            | ⟨1, _⟩, h =>
                mkCtrl1 synergyWitnessData (vec1 (clamp (-(h 0 3)))) (fun _ => hclamp_bd _)
            | ⟨2, _⟩, h =>
                mkCtrl1 synergyWitnessData (vec1 (clamp (-(h 1 3)))) (fun _ => hclamp_bd _)
          borel := fun j => by
            fin_cases j
            · exact measurable_const
            · refine Measurable.subtype_mk ?_
              rw [measurable_pi_iff]; intro _
              rw [measurable_pi_iff]; intro _
              have h0 : Continuous (fun h : Fin 1 → Vec 4 => h 0 3) :=
                (continuous_apply (3 : Fin 4)).comp (continuous_apply (0 : Fin 1))
              exact (hclamp_cont.comp h0.neg).measurable
            · refine Measurable.subtype_mk ?_
              rw [measurable_pi_iff]; intro _
              rw [measurable_pi_iff]; intro _
              have h1 : Continuous (fun h : Fin 2 → Vec 4 => h 1 3) :=
                (continuous_apply (3 : Fin 4)).comp (continuous_apply (1 : Fin 2))
              exact (hclamp_cont.comp h1.neg).measurable }
      refine ⟨P12, ?_⟩
      intro w _
      rw [term_r12_eq]
      have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
      have hw1 : (-1 : ℝ) ≤ (w 1).val 0 0 ∧ (w 1).val 0 0 ≤ 1 := (w 1).property 0 0
      have hx1_3 : (synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0)) 3 =
          (w 0).val 0 0 := by
        rw [synergy_step1]; rfl
      have hu1_val : (P12.rule 1 (fun _ => synergyWitnessData.step 0
          ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0 0 = -((w 0).val 0 0) := by
        change clamp (-(synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0) 3)) = _
        rw [hx1_3]
        exact hclamp_eq _ (by linarith) (by linarith)
      have hx2_3 : (synergyWitnessData.step (synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P12.rule 1 (fun _ => synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0)
          ((w 1).val 0)) 3 = (w 1).val 0 0 := by
        rw [synergy_step2]; rfl
      have hu2_val : (P12.rule 2 ![synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0),
          synergyWitnessData.step (synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))
            ((P12.rule 1 (fun _ => synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0)
            ((w 1).val 0)]).val 0 0 = -((w 1).val 0 0) := by
        change clamp (-(synergyWitnessData.step (synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P12.rule 1 (fun _ => synergyWitnessData.step 0 ((P12.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0)
          ((w 1).val 0) 3)) = _
        rw [hx2_3]
        exact hclamp_eq _ (by linarith) (by linarith)
      rw [synergy_step3]
      have hu0_val : (P12.rule 0 Fin.elim0).val 0 0 = 0 := rfl
      constructor
      · exact shift4H_bounds _ _ _ _
          (by rw [hu0_val, hu1_val]; constructor <;> linarith)
          (by rw [hu0_val, hu1_val]; constructor <;> linarith)
          (by rw [hu0_val, hu2_val]; constructor <;> linarith)
          (by rw [hu0_val, hu2_val]; constructor <;> linarith)
      · change (LinearMap.proj 2 : Vec 4 →ₗ[ℝ] ℝ) _ ≤ (0 : ℝ)
        simp only [LinearMap.proj_apply, Matrix.cons_val, Matrix.head_cons, Matrix.tail_cons]
        rw [hu0_val]
    refine ⟨h0_r12, ?_⟩
    rintro eta ⟨P, hP⟩
    -- Even with R={1,2}, row 0 + row 1 gives 2*u0 >= 0 => u0 >= 0 => eta >= 0.
    let w0 : MultiNoise synergyWitnessData lenR12 := fun _ =>
      noise1Synergy 0 (by norm_num) (by norm_num)
    have hrow0 := ((hP w0 trivial).1 0).1
    have hrow1 := ((hP w0 trivial).1 1).1
    have hcost := (hP w0 trivial).2
    rw [term_r12_eq, synergy_step3] at hrow0 hrow1 hcost
    simp only [synergyWitnessData, shift4H, Matrix.cons_val_zero, Matrix.cons_val_one,
      Matrix.cons_val, LinearMap.coe_mk, AddHom.coe_mk, LinearMap.proj_apply] at hrow0 hrow1 hcost
    linarith

/-! ## Section 4: Strict Submodularity & Bidirectional Single-Closure Dominance (`O4 + O7`) -/

/-- 1D integrator witness (`A=1, B=1, E=1, U=[-1/2, 1/2], rho=1, H=1, [-2, 10], c=1`)
showing strict submodularity (`defect = -1`) and early-closure dominance (`V({1}) = 2 < 3 = V({2})`). -/
abbrev earlyDomWitnessData : Data where
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
  umin := fun _ => -(1 / 2 : ℝ)
  umax := fun _ => (1 / 2 : ℝ)
  control_nonempty := fun _ => by norm_num
  rho := 1
  rho_pos := zero_lt_one
  H := LinearMap.id
  gmin := fun _ => -2
  gmax := fun _ => 10
  c := LinearMap.proj 0

private theorem early_step3 (u0 u1 u2 w0 w1 w2 : Vec 1) :
    earlyDomWitnessData.step (earlyDomWitnessData.step (earlyDomWitnessData.step 0 u0 w0) u1 w1) u2 w2 0 =
      u0 0 + u1 0 + u2 0 + w0 0 + w1 0 + w2 0 := by
  simp [Data.step, earlyDomWitnessData]; ring

private abbrev noise1Early (v : ℝ) (h1 : (-1 : ℝ) ≤ v) (h2 : v ≤ 1) :
    earlyDomWitnessData.NoiseBlock 1 :=
  ⟨fun _ _ => v, fun _ _ => ⟨h1, h2⟩⟩

/-- **Theorem O4.10 (Strict Submodularity & Early-Closure Dominance):**
On the 1D integrator `earlyDomWitnessData`:
  `V(∅) = 4`, `V({1}) = 2`, `V({2}) = 3`, `V({1, 2}) = 2`,
giving strict submodular defect `-1 < 0` AND strict early dominance `V({1}) < V({2})`. -/
theorem exists_strict_submodular_and_early_dominance :
    ∃ D : Data,
      ((4 : ℝ) ∈ schedEmptyLevels D ∧ ∀ eta ∈ schedEmptyLevels D, (4 : ℝ) ≤ eta) ∧
      ((2 : ℝ) ∈ schedR1Levels D ∧ ∀ eta ∈ schedR1Levels D, (2 : ℝ) ≤ eta) ∧
      ((3 : ℝ) ∈ schedR2Levels D ∧ ∀ eta ∈ schedR2Levels D, (3 : ℝ) ≤ eta) ∧
      ((2 : ℝ) ∈ schedR12Levels D ∧ ∀ eta ∈ schedR12Levels D, (2 : ℝ) ≤ eta) := by
  have h2_r1 : (2 : ℝ) ∈ schedR1Levels earlyDomWitnessData := by
    let clampHalf : ℝ → ℝ := fun z => max (-(1 / 2 : ℝ)) (min (1 / 2 : ℝ) z)
    have hcb : ∀ z : ℝ, (-(1 / 2 : ℝ)) ≤ clampHalf z ∧ clampHalf z ≤ (1 / 2 : ℝ) := fun z =>
      ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩
    have hceq : ∀ z : ℝ, (-(1 / 2 : ℝ)) ≤ z → z ≤ (1 / 2 : ℝ) → clampHalf z = z := by
      intro z h1 h2; dsimp only [clampHalf]; rw [min_eq_right h2, max_eq_right h1]
    have hcc : Continuous clampHalf := continuous_const.max (continuous_const.min continuous_id)
    let P1 : HistoryStatePolicy earlyDomWitnessData lenR1 :=
      { rule := fun j hist =>
          match j, hist with
          | ⟨0, _⟩, _ => mkCtrl1 earlyDomWitnessData (vec1 0) (fun _ => ⟨by norm_num, by norm_num⟩)
          | ⟨1, _⟩, h =>
              let v := clampHalf (-(h 0 0) / 2)
              mkCtrl2 earlyDomWitnessData (vec1 v) (vec1 v) (fun _ => hcb _) (fun _ => hcb _)
        borel := fun j => by
          fin_cases j
          · exact measurable_const
          · refine Measurable.subtype_mk ?_
            rw [measurable_pi_iff]; intro t
            rw [measurable_pi_iff]; intro _
            have h0 : Continuous (fun h : Fin 1 → Vec 1 => h 0 0) :=
              (continuous_apply (0 : Fin 1)).comp (continuous_apply (0 : Fin 1))
            fin_cases t <;>
              exact (hcc.comp (h0.neg.div_const 2)).measurable }
    refine ⟨P1, ?_⟩
    intro w _
    rw [term_r1_eq]
    have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
    have hw1 : (-1 : ℝ) ≤ (w 1).val 0 0 ∧ (w 1).val 0 0 ≤ 1 := (w 1).property 0 0
    have hw2 : (-1 : ℝ) ≤ (w 1).val 1 0 ∧ (w 1).val 1 0 ≤ 1 := (w 1).property 1 0
    have hx1 : (earlyDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0)) 0 = (w 0).val 0 0 := by
      simp [Data.step, earlyDomWitnessData, P1, mkCtrl1, vec1]
    have hu1 : (P1.rule 1 (fun _ => earlyDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0 0 =
        -((w 0).val 0 0) / 2 := by
      change clampHalf (-(earlyDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0) 0) / 2) = _
      rw [hx1]; exact hceq _ (by linarith) (by linarith)
    have hu2 : (P1.rule 1 (fun _ => earlyDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 1 0 =
        -((w 0).val 0 0) / 2 := by
      change clampHalf (-(earlyDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0) 0) / 2) = _
      rw [hx1]; exact hceq _ (by linarith) (by linarith)
    have hu0 : (P1.rule 0 Fin.elim0).val 0 0 = 0 := rfl
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i; subst hi
      change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 ∧ earlyDomWitnessData.step _ _ _ 0 ≤ 10
      rw [early_step3, hu0, hu1, hu2]; constructor <;> linarith
    · change earlyDomWitnessData.step _ _ _ 0 ≤ 2
      rw [early_step3, hu0, hu1, hu2]; linarith
  have h12_ge2 : ∀ eta ∈ schedR12Levels earlyDomWitnessData, (2 : ℝ) ≤ eta := by
    rintro eta ⟨P, hP⟩
    let wM : MultiNoise earlyDomWitnessData lenR12 := fun _ => noise1Early (-1) (by norm_num) (by norm_num)
    let wP : MultiNoise earlyDomWitnessData lenR12 := fun _ => noise1Early 1 (by norm_num) (by norm_num)
    have hlo := ((hP wM trivial).1 0).1
    have hcost := (hP wP trivial).2
    rw [term_r12_eq] at hlo hcost
    change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 at hlo
    change earlyDomWitnessData.step _ _ _ 0 ≤ eta at hcost
    rw [early_step3] at hlo hcost
    let x1M := earlyDomWitnessData.step earlyDomWitnessData.x0 ((P.rule 0 Fin.elim0).val 0) ((wM 0).val 0)
    let x2M := earlyDomWitnessData.step x1M ((P.rule 1 (fun _ => x1M)).val 0) ((wM 1).val 0)
    let x1P := earlyDomWitnessData.step earlyDomWitnessData.x0 ((P.rule 0 Fin.elim0).val 0) ((wP 0).val 0)
    let x2P := earlyDomWitnessData.step x1P ((P.rule 1 (fun _ => x1P)).val 0) ((wP 1).val 0)
    have hu1M := ((P.rule 1 (fun _ => x1M)).property 0 0).2
    have hu2M := ((P.rule 2 ![x1M, x2M]).property 0 0).2
    have hu1P := ((P.rule 1 (fun _ => x1P)).property 0 0).1
    have hu2P := ((P.rule 2 ![x1P, x2P]).property 0 0).1
    change _ ≤ (1 / 2 : ℝ) at hu1M hu2M
    change (-(1 / 2 : ℝ)) ≤ _ at hu1P hu2P
    have hwM0 : (wM 0).val 0 0 = -1 := rfl
    have hwM1 : (wM 1).val 0 0 = -1 := rfl
    have hwM2 : (wM 2).val 0 0 = -1 := rfl
    have hwP0 : (wP 0).val 0 0 = 1 := rfl
    have hwP1 : (wP 1).val 0 0 = 1 := rfl
    have hwP2 : (wP 2).val 0 0 = 1 := rfl
    dsimp only [x1M, x2M, x1P, x2P] at hu1M hu2M hu1P hu2P
    linarith [hlo, hcost, hu1M, hu2M, hu1P, hu2P, hwM0, hwM1, hwM2, hwP0, hwP1, hwP2]
  refine ⟨earlyDomWitnessData, ?_, ?_, ?_, ?_⟩
  · -- V(∅) = 4
    refine ⟨?_, ?_⟩
    · let uE : earlyDomWitnessData.ControlBlock 3 :=
        mkCtrl3 earlyDomWitnessData (vec1 (1 / 3)) (vec1 (1 / 3)) (vec1 (1 / 3))
          (fun _ => ⟨by norm_num, by norm_num⟩)
          (fun _ => ⟨by norm_num, by norm_num⟩)
          (fun _ => ⟨by norm_num, by norm_num⟩)
      refine ⟨{ rule := fun _ _ => uE, borel := fun _ => measurable_const }, ?_⟩
      intro w _
      rw [term_empty_eq]
      have hw0 := (w 0).property 0 0
      have hw1 := (w 0).property 1 0
      have hw2 := (w 0).property 2 0
      have h3 := early_step3 (uE.val 0) (uE.val 1) (uE.val 2) ((w 0).val 0) ((w 0).val 1) ((w 0).val 2)
      have hu0 : uE.val 0 0 = 1 / 3 := rfl
      have hu1 : uE.val 1 0 = 1 / 3 := rfl
      have hu2 : uE.val 2 0 = 1 / 3 := rfl
      constructor
      · intro i
        have hi : i = 0 := Fin.eq_zero i; subst hi
        change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 ∧ earlyDomWitnessData.step _ _ _ 0 ≤ 10
        rw [h3, hu0, hu1, hu2]; constructor <;> linarith [hw0.1, hw0.2, hw1.1, hw1.2, hw2.1, hw2.2]
      · change earlyDomWitnessData.step _ _ _ 0 ≤ 4
        rw [h3, hu0, hu1, hu2]; linarith [hw0.2, hw1.2, hw2.2]
    · rintro eta ⟨P, hP⟩
      let wM : MultiNoise earlyDomWitnessData lenEmpty := fun _ =>
        mkNoise3 earlyDomWitnessData (vec1 (-1)) (vec1 (-1)) (vec1 (-1))
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      let wP : MultiNoise earlyDomWitnessData lenEmpty := fun _ =>
        mkNoise3 earlyDomWitnessData (vec1 1) (vec1 1) (vec1 1)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      have hlo := ((hP wM trivial).1 0).1
      have hcost := (hP wP trivial).2
      rw [term_empty_eq] at hlo hcost
      change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 at hlo
      change earlyDomWitnessData.step _ _ _ 0 ≤ eta at hcost
      rw [early_step3] at hlo hcost
      simp only [wM, wP, mkNoise3, vec1, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val] at hlo hcost
      linarith
  · -- V({1}) = 2
    exact ⟨h2_r1, fun eta heta => h12_ge2 eta (schedR1_subset_schedR12 earlyDomWitnessData heta)⟩
  · -- V({2}) = 3
    refine ⟨?_, ?_⟩
    · let clampHalf : ℝ → ℝ := fun z => max (-(1 / 2 : ℝ)) (min (1 / 2 : ℝ) z)
      have hcb : ∀ z : ℝ, (-(1 / 2 : ℝ)) ≤ clampHalf z ∧ clampHalf z ≤ (1 / 2 : ℝ) := fun z =>
        ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩
      have hceq : ∀ z : ℝ, (-(1 / 2 : ℝ)) ≤ z → z ≤ (1 / 2 : ℝ) → clampHalf z = z := by
        intro z h1 h2; dsimp only [clampHalf]; rw [min_eq_right h2, max_eq_right h1]
      have hcc : Continuous clampHalf := continuous_const.max (continuous_const.min continuous_id)
      let P2 : HistoryStatePolicy earlyDomWitnessData lenR2 :=
        { rule := fun j hist =>
            match j, hist with
            | ⟨0, _⟩, _ =>
                mkCtrl2 earlyDomWitnessData (vec1 (1 / 4)) (vec1 (1 / 4))
                  (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
            | ⟨1, _⟩, h =>
                mkCtrl1 earlyDomWitnessData (vec1 (clampHalf (-((h 0 0) - 1 / 2) / 4))) (fun _ => hcb _)
          borel := fun j => by
            fin_cases j
            · exact measurable_const
            · refine Measurable.subtype_mk ?_
              rw [measurable_pi_iff]; intro _
              rw [measurable_pi_iff]; intro _
              have h0 : Continuous (fun h : Fin 1 → Vec 1 => h 0 0) :=
                (continuous_apply (0 : Fin 1)).comp (continuous_apply (0 : Fin 1))
              exact (hcc.comp ((h0.sub continuous_const).neg.div_const 4)).measurable }
      refine ⟨P2, ?_⟩
      intro w _
      rw [term_r2_eq]
      have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
      have hw1 : (-1 : ℝ) ≤ (w 0).val 1 0 ∧ (w 0).val 1 0 ≤ 1 := (w 0).property 1 0
      have hw2 : (-1 : ℝ) ≤ (w 1).val 0 0 ∧ (w 1).val 0 0 ≤ 1 := (w 1).property 0 0
      have hx2 : (earlyDomWitnessData.step (earlyDomWitnessData.step 0
          ((P2.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P2.rule 0 Fin.elim0).val 1) ((w 0).val 1)) 0 = 1 / 2 + (w 0).val 0 0 + (w 0).val 1 0 := by
        simp [Data.step, earlyDomWitnessData, P2, mkCtrl2, vec1]; ring
      have hu2 : (P2.rule 1 (fun _ => earlyDomWitnessData.step (earlyDomWitnessData.step 0
          ((P2.rule 0 Fin.elim0).val 0) ((w 0).val 0))
          ((P2.rule 0 Fin.elim0).val 1) ((w 0).val 1))).val 0 0 =
          -((w 0).val 0 0 + (w 0).val 1 0) / 4 := by
        change clampHalf (-(earlyDomWitnessData.step _ _ _ 0 - 1 / 2) / 4) = _
        rw [hx2]
        have hsimp : -(1 / 2 + (w 0).val 0 0 + (w 0).val 1 0 - 1 / 2) / 4 =
            -((w 0).val 0 0 + (w 0).val 1 0) / 4 := by ring
        rw [hsimp]
        exact hceq _ (by linarith) (by linarith)
      have hu0 : (P2.rule 0 Fin.elim0).val 0 0 = 1 / 4 := rfl
      have hu1 : (P2.rule 0 Fin.elim0).val 1 0 = 1 / 4 := rfl
      constructor
      · intro i
        have hi : i = 0 := Fin.eq_zero i; subst hi
        change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 ∧ earlyDomWitnessData.step _ _ _ 0 ≤ 10
        rw [early_step3, hu0, hu1, hu2]; constructor <;> linarith
      · change earlyDomWitnessData.step _ _ _ 0 ≤ 3
        rw [early_step3, hu0, hu1, hu2]; linarith
    · rintro eta ⟨P, hP⟩
      let wM : MultiNoise earlyDomWitnessData lenR2 := fun j =>
        match j with
        | ⟨0, _⟩ => mkNoise2 earlyDomWitnessData (vec1 (-1)) (vec1 (-1))
            (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
        | ⟨1, _⟩ => noise1Early (-1) (by norm_num) (by norm_num)
      let wP : MultiNoise earlyDomWitnessData lenR2 := fun j =>
        match j with
        | ⟨0, _⟩ => mkNoise2 earlyDomWitnessData (vec1 1) (vec1 1)
            (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
        | ⟨1, _⟩ => noise1Early 1 (by norm_num) (by norm_num)
      have hlo := ((hP wM trivial).1 0).1
      have hcost := (hP wP trivial).2
      rw [term_r2_eq] at hlo hcost
      change (-2 : ℝ) ≤ earlyDomWitnessData.step _ _ _ 0 at hlo
      change earlyDomWitnessData.step _ _ _ 0 ≤ eta at hcost
      rw [early_step3] at hlo hcost
      let x2M := earlyDomWitnessData.step
        (earlyDomWitnessData.step earlyDomWitnessData.x0 ((P.rule 0 Fin.elim0).val 0) ((wM 0).val 0))
        ((P.rule 0 Fin.elim0).val 1) ((wM 0).val 1)
      let x2P := earlyDomWitnessData.step
        (earlyDomWitnessData.step earlyDomWitnessData.x0 ((P.rule 0 Fin.elim0).val 0) ((wP 0).val 0))
        ((P.rule 0 Fin.elim0).val 1) ((wP 0).val 1)
      have hu2M := ((P.rule 1 (fun _ => x2M)).property 0 0).2
      have hu2P := ((P.rule 1 (fun _ => x2P)).property 0 0).1
      change _ ≤ (1 / 2 : ℝ) at hu2M
      change (-(1 / 2 : ℝ)) ≤ _ at hu2P
      have hwM0 : (wM 0).val 0 0 = -1 := rfl
      have hwM1 : (wM 0).val 1 0 = -1 := rfl
      have hwM2 : (wM 1).val 0 0 = -1 := rfl
      have hwP0 : (wP 0).val 0 0 = 1 := rfl
      have hwP1 : (wP 0).val 1 0 = 1 := rfl
      have hwP2 : (wP 1).val 0 0 = 1 := rfl
      dsimp only [x2M, x2P] at hu2M hu2P
      linarith [hlo, hcost, hu2M, hu2P, hwM0, hwM1, hwM2, hwP0, hwP1, hwP2]
  · -- V({1, 2}) = 2
    exact ⟨schedR1_subset_schedR12 earlyDomWitnessData h2_r1, h12_ge2⟩

/-- 1D contracting witness (`A=1/2, B=1, E=1, U=[-1, 1], rho=1, H=1, [-2, 10], c=1`)
showing strict late-closure dominance (`V({2}) = 0 < 1 = V({1})`). -/
abbrev lateDomWitnessData : Data where
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
  A := (1 / 2 : ℝ) • LinearMap.id
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
  gmax := fun _ => 10
  c := LinearMap.proj 0

private theorem late_step3 (u0 u1 u2 w0 w1 w2 : Vec 1) :
    lateDomWitnessData.step (lateDomWitnessData.step (lateDomWitnessData.step 0 u0 w0) u1 w1) u2 w2 0 =
      (1 / 4 : ℝ) * (u0 0 + w0 0) + (1 / 2 : ℝ) * (u1 0 + w1 0) + (u2 0 + w2 0) := by
  simp [Data.step, lateDomWitnessData]; ring

private abbrev noise1Late (v : ℝ) (h1 : (-1 : ℝ) ≤ v) (h2 : v ≤ 1) :
    lateDomWitnessData.NoiseBlock 1 :=
  ⟨fun _ _ => v, fun _ _ => ⟨h1, h2⟩⟩

/-- **Theorem O4.11 (Strict Late-Closure Dominance):**
On the 1D contracting system `lateDomWitnessData`:
  `V(∅) = 3/2`, `V({1}) = 1`, `V({2}) = 0`, `V({1, 2}) = 0`,
proving strict late-closure dominance `V({2}) < V({1})` (opposite to Theorem O4.10). -/
theorem exists_strict_late_dominance :
    ∃ D : Data,
      ((3 / 2 : ℝ) ∈ schedEmptyLevels D ∧ ∀ eta ∈ schedEmptyLevels D, (3 / 2 : ℝ) ≤ eta) ∧
      ((1 : ℝ) ∈ schedR1Levels D ∧ ∀ eta ∈ schedR1Levels D, (1 : ℝ) ≤ eta) ∧
      ((0 : ℝ) ∈ schedR2Levels D ∧ ∀ eta ∈ schedR2Levels D, (0 : ℝ) ≤ eta) ∧
      ((0 : ℝ) ∈ schedR12Levels D ∧ ∀ eta ∈ schedR12Levels D, (0 : ℝ) ≤ eta) := by
  have h0_r2 : (0 : ℝ) ∈ schedR2Levels lateDomWitnessData := by
    let clamp1 : ℝ → ℝ := fun z => max (-1 : ℝ) (min (1 : ℝ) z)
    have hcb : ∀ z : ℝ, (-1 : ℝ) ≤ clamp1 z ∧ clamp1 z ≤ 1 := fun z =>
      ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩
    have hceq : ∀ z : ℝ, (-1 : ℝ) ≤ z → z ≤ 1 → clamp1 z = z := by
      intro z h1 h2; dsimp only [clamp1]; rw [min_eq_right h2, max_eq_right h1]
    have hcc : Continuous clamp1 := continuous_const.max (continuous_const.min continuous_id)
    let P2 : HistoryStatePolicy lateDomWitnessData lenR2 :=
      { rule := fun j hist =>
          match j, hist with
          | ⟨0, _⟩, _ =>
              mkCtrl2 lateDomWitnessData (vec1 (-1)) (vec1 (-1))
                (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
          | ⟨1, _⟩, h =>
              mkCtrl1 lateDomWitnessData (vec1 (clamp1 (-1 - (h 0 0) / 2))) (fun _ => hcb _)
        borel := fun j => by
          fin_cases j
          · exact measurable_const
          · refine Measurable.subtype_mk ?_
            rw [measurable_pi_iff]; intro _
            rw [measurable_pi_iff]; intro _
            have hc : Continuous (fun h : Fin 1 → Vec 1 => clamp1 (-1 - (h 0 0) / 2)) :=
              hcc.comp (continuous_const.sub (((continuous_apply (0 : Fin 1)).comp (continuous_apply (0 : Fin 1))).div_const 2))
            exact hc.measurable }
    refine ⟨P2, ?_⟩
    intro w _
    rw [term_r2_eq]
    have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
    have hw1 : (-1 : ℝ) ≤ (w 0).val 1 0 ∧ (w 0).val 1 0 ≤ 1 := (w 0).property 1 0
    have hw2 : (-1 : ℝ) ≤ (w 1).val 0 0 ∧ (w 1).val 0 0 ≤ 1 := (w 1).property 0 0
    have hx2 : (lateDomWitnessData.step (lateDomWitnessData.step 0
        ((P2.rule 0 Fin.elim0).val 0) ((w 0).val 0))
        ((P2.rule 0 Fin.elim0).val 1) ((w 0).val 1)) 0 =
        -(3 / 2 : ℝ) + (1 / 2 : ℝ) * (w 0).val 0 0 + (w 0).val 1 0 := by
      simp [Data.step, lateDomWitnessData, P2, mkCtrl2, vec1]; ring
    have hu2 : (P2.rule 1 (fun _ => lateDomWitnessData.step (lateDomWitnessData.step 0
        ((P2.rule 0 Fin.elim0).val 0) ((w 0).val 0))
        ((P2.rule 0 Fin.elim0).val 1) ((w 0).val 1))).val 0 0 =
        -(1 / 4 : ℝ) - (1 / 4 : ℝ) * (w 0).val 0 0 - (1 / 2 : ℝ) * (w 0).val 1 0 := by
      change clamp1 (-1 - (lateDomWitnessData.step _ _ _ 0) / 2) = _
      rw [hx2]
      have hsimp : -1 - (-(3 / 2 : ℝ) + (1 / 2 : ℝ) * (w 0).val 0 0 + (w 0).val 1 0) / 2 =
          -(1 / 4 : ℝ) - (1 / 4 : ℝ) * (w 0).val 0 0 - (1 / 2 : ℝ) * (w 0).val 1 0 := by ring
      rw [hsimp]
      exact hceq _ (by linarith) (by linarith)
    have hu0 : (P2.rule 0 Fin.elim0).val 0 0 = -1 := rfl
    have hu1 : (P2.rule 0 Fin.elim0).val 1 0 = -1 := rfl
    constructor
    · intro i
      have hi : i = 0 := Fin.eq_zero i; subst hi
      change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 ∧ lateDomWitnessData.step _ _ _ 0 ≤ 10
      rw [late_step3, hu0, hu1, hu2]; constructor <;> linarith
    · change lateDomWitnessData.step _ _ _ 0 ≤ 0
      rw [late_step3, hu0, hu1, hu2]; linarith
  have h12_ge0 : ∀ eta ∈ schedR12Levels lateDomWitnessData, (0 : ℝ) ≤ eta := by
    rintro eta ⟨P, hP⟩
    -- Fix w0 = w1 = 0, vary w2 ∈ {-1, +1}
    let wM : MultiNoise lateDomWitnessData lenR12 := fun j =>
      match j with
      | ⟨0, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
      | ⟨1, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
      | ⟨2, _⟩ => noise1Late (-1) (by norm_num) (by norm_num)
    let wP : MultiNoise lateDomWitnessData lenR12 := fun j =>
      match j with
      | ⟨0, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
      | ⟨1, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
      | ⟨2, _⟩ => noise1Late 1 (by norm_num) (by norm_num)
    have hlo := ((hP wM trivial).1 0).1
    have hcost := (hP wP trivial).2
    rw [term_r12_eq] at hlo hcost
    change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 at hlo
    change lateDomWitnessData.step _ _ _ 0 ≤ eta at hcost
    rw [late_step3] at hlo hcost
    simp only [wM, wP, noise1Late] at hlo hcost
    linarith
  refine ⟨lateDomWitnessData, ?_, ?_, ?_, ?_⟩
  · -- V(∅) = 3/2
    refine ⟨?_, ?_⟩
    · let uE : lateDomWitnessData.ControlBlock 3 :=
        mkCtrl3 lateDomWitnessData (vec1 0) (vec1 0) (vec1 (-(1 / 4)))
          (fun _ => ⟨by norm_num, by norm_num⟩)
          (fun _ => ⟨by norm_num, by norm_num⟩)
          (fun _ => ⟨by norm_num, by norm_num⟩)
      refine ⟨{ rule := fun _ _ => uE, borel := fun _ => measurable_const }, ?_⟩
      intro w _
      rw [term_empty_eq]
      have hw0 := (w 0).property 0 0
      have hw1 := (w 0).property 1 0
      have hw2 := (w 0).property 2 0
      have hu0 : uE.val 0 0 = 0 := rfl
      have hu1 : uE.val 1 0 = 0 := rfl
      have hu2 : uE.val 2 0 = -(1 / 4 : ℝ) := rfl
      constructor
      · intro i
        have hi : i = 0 := Fin.eq_zero i; subst hi
        change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 ∧ lateDomWitnessData.step _ _ _ 0 ≤ 10
        rw [late_step3, hu0, hu1, hu2]; constructor <;> linarith [hw0.1, hw0.2, hw1.1, hw1.2, hw2.1, hw2.2]
      · change lateDomWitnessData.step _ _ _ 0 ≤ 3 / 2
        rw [late_step3, hu0, hu1, hu2]; linarith [hw0.2, hw1.2, hw2.2]
    · rintro eta ⟨P, hP⟩
      let wM : MultiNoise lateDomWitnessData lenEmpty := fun _ =>
        mkNoise3 lateDomWitnessData (vec1 (-1)) (vec1 (-1)) (vec1 (-1))
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      let wP : MultiNoise lateDomWitnessData lenEmpty := fun _ =>
        mkNoise3 lateDomWitnessData (vec1 1) (vec1 1) (vec1 1)
          (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      have hlo := ((hP wM trivial).1 0).1
      have hcost := (hP wP trivial).2
      rw [term_empty_eq] at hlo hcost
      change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 at hlo
      change lateDomWitnessData.step _ _ _ 0 ≤ eta at hcost
      rw [late_step3] at hlo hcost
      simp only [wM, wP, mkNoise3, vec1, Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.cons_val] at hlo hcost
      linarith
  · -- V({1}) = 1
    refine ⟨?_, ?_⟩
    · let clamp1 : ℝ → ℝ := fun z => max (-1 : ℝ) (min (1 : ℝ) z)
      have hcb : ∀ z : ℝ, (-1 : ℝ) ≤ clamp1 z ∧ clamp1 z ≤ 1 := fun z =>
        ⟨le_max_left _ _, max_le (by norm_num) (min_le_left _ _)⟩
      have hceq : ∀ z : ℝ, (-1 : ℝ) ≤ z → z ≤ 1 → clamp1 z = z := by
        intro z h1 h2; dsimp only [clamp1]; rw [min_eq_right h2, max_eq_right h1]
      have hcc : Continuous clamp1 := continuous_const.max (continuous_const.min continuous_id)
      let P1 : HistoryStatePolicy lateDomWitnessData lenR1 :=
        { rule := fun j hist =>
            match j, hist with
            | ⟨0, _⟩, _ => mkCtrl1 lateDomWitnessData (vec1 0) (fun _ => ⟨by norm_num, by norm_num⟩)
            | ⟨1, _⟩, h =>
                mkCtrl2 lateDomWitnessData (vec1 (clamp1 (-(h 0 0) / 2))) (vec1 (-(1 / 2)))
                  (fun _ => hcb _) (fun _ => ⟨by norm_num, by norm_num⟩)
          borel := fun j => by
            fin_cases j
            · exact measurable_const
            · refine Measurable.subtype_mk ?_
              rw [measurable_pi_iff]; intro t
              rw [measurable_pi_iff]; intro _
              have h0 : Continuous (fun h : Fin 1 → Vec 1 => h 0 0) :=
                (continuous_apply (0 : Fin 1)).comp (continuous_apply (0 : Fin 1))
              fin_cases t
              · exact (hcc.comp (h0.neg.div_const 2)).measurable
              · exact measurable_const }
      refine ⟨P1, ?_⟩
      intro w _
      rw [term_r1_eq]
      have hw0 : (-1 : ℝ) ≤ (w 0).val 0 0 ∧ (w 0).val 0 0 ≤ 1 := (w 0).property 0 0
      have hw1 : (-1 : ℝ) ≤ (w 1).val 0 0 ∧ (w 1).val 0 0 ≤ 1 := (w 1).property 0 0
      have hw2 : (-1 : ℝ) ≤ (w 1).val 1 0 ∧ (w 1).val 1 0 ≤ 1 := (w 1).property 1 0
      have hx1 : (lateDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0)) 0 = (w 0).val 0 0 := by
        simp [Data.step, lateDomWitnessData, P1, mkCtrl1, vec1]
      have hu1 : (P1.rule 1 (fun _ => lateDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 0 0 =
          -((w 0).val 0 0) / 2 := by
        change clamp1 (-(lateDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0) 0) / 2) = _
        rw [hx1]; exact hceq _ (by linarith) (by linarith)
      have hu0 : (P1.rule 0 Fin.elim0).val 0 0 = 0 := rfl
      have hu2 : (P1.rule 1 (fun _ => lateDomWitnessData.step 0 ((P1.rule 0 Fin.elim0).val 0) ((w 0).val 0))).val 1 0 =
          -(1 / 2 : ℝ) := rfl
      constructor
      · intro i
        have hi : i = 0 := Fin.eq_zero i; subst hi
        change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 ∧ lateDomWitnessData.step _ _ _ 0 ≤ 10
        rw [late_step3, hu0, hu1, hu2]; constructor <;> linarith
      · change lateDomWitnessData.step _ _ _ 0 ≤ 1
        rw [late_step3, hu0, hu1, hu2]; linarith
    · rintro eta ⟨P, hP⟩
      -- Fix w0 = 0, vary (w1, w2) ∈ {(-1,-1), (+1,+1)}
      let wM : MultiNoise lateDomWitnessData lenR1 := fun j =>
        match j with
        | ⟨0, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
        | ⟨1, _⟩ => mkNoise2 lateDomWitnessData (vec1 (-1)) (vec1 (-1))
            (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      let wP : MultiNoise lateDomWitnessData lenR1 := fun j =>
        match j with
        | ⟨0, _⟩ => noise1Late 0 (by norm_num) (by norm_num)
        | ⟨1, _⟩ => mkNoise2 lateDomWitnessData (vec1 1) (vec1 1)
            (fun _ => ⟨by norm_num, by norm_num⟩) (fun _ => ⟨by norm_num, by norm_num⟩)
      have hlo := ((hP wM trivial).1 0).1
      have hcost := (hP wP trivial).2
      rw [term_r1_eq] at hlo hcost
      change (-2 : ℝ) ≤ lateDomWitnessData.step _ _ _ 0 at hlo
      change lateDomWitnessData.step _ _ _ 0 ≤ eta at hcost
      rw [late_step3] at hlo hcost
      simp only [wM, wP, noise1Late, mkNoise2, vec1, Matrix.cons_val_zero, Matrix.cons_val_one] at hlo hcost
      linarith
  · -- V({2}) = 0
    exact ⟨h0_r2, fun eta heta => h12_ge0 eta (schedR2_subset_schedR12 lateDomWitnessData heta)⟩
  · -- V({1, 2}) = 0
    exact ⟨schedR2_subset_schedR12 lateDomWitnessData h0_r2, h12_ge0⟩

end AroProofs.BridgeO4Scheduling
