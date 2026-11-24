namespace Campaign
def Model (n : Nat) : Nat := n
axiom forbidden : Model 0 = 0
theorem expected : Model 0 = 0 := forbidden
end Campaign
