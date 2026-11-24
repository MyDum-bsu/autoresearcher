import BridgeFormalV3.Proofs.Support

set_option pp.fullNames true

example : BridgeFormalV3.FutureExpansionGoal := BridgeFormalV3.Proofs.future_expansion
example : BridgeFormalV3.AttainedSupportGoal := BridgeFormalV3.Proofs.attained_support
example : BridgeFormalV3.RobustRowGoal := BridgeFormalV3.Proofs.robust_row
example : BridgeFormalV3.ExactTighteningGoal := BridgeFormalV3.Proofs.exact_tightening

#print BridgeFormalV3.FutureExpansionGoal
#print BridgeFormalV3.AttainedSupportGoal
#print BridgeFormalV3.RobustRowGoal
#print BridgeFormalV3.ExactTighteningGoal

#print BridgeFormalV3.Proofs.future_expansion
#print axioms BridgeFormalV3.Proofs.future_expansion
#print BridgeFormalV3.Proofs.attained_support
#print axioms BridgeFormalV3.Proofs.attained_support
#print BridgeFormalV3.Proofs.robust_row
#print axioms BridgeFormalV3.Proofs.robust_row
#print BridgeFormalV3.Proofs.exact_tightening
#print axioms BridgeFormalV3.Proofs.exact_tightening

run_cmd do
  let env ← Lean.getEnv
  for name in env.allImportedModuleNames do
    Lean.logInfo m!"IMPORT|{name}"
