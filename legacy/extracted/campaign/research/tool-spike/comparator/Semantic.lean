namespace Campaign
theorem witness : ∃ n : Nat, n = 0 := ⟨0, rfl⟩
theorem falseConclusion : ¬ (∀ n : Nat, n = 0 → n = 1) := by
  intro h
  have bad := h 0 rfl
  cases bad
theorem infeasible : (∃ n : Nat, n = 0) ∧ ¬ (∃ n : Nat, n = 0 ∧ n = 1) := by
  constructor
  · exact witness
  · intro ⟨n, h0, h1⟩
    have bad : (0 : Nat) = 1 := h0.symm.trans h1
    cases bad
#print axioms witness
#print axioms falseConclusion
#print axioms infeasible
end Campaign
