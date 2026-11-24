namespace Campaign
def Model (n : Nat) : Nat := n + 1
theorem expected : Model 0 = 1 := by rfl
end Campaign
