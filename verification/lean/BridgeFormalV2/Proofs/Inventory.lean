import BridgeFormalV2.Proofs.Policies

set_option pp.fullNames true

run_cmd do
  for n in (← Lean.getEnv).allImportedModuleNames do
    Lean.logInfo m!"IMPORT|{n}"

example : BridgeFormalV2.NonemptyBlocksGoal := BridgeFormalV2.Proofs.nonempty_blocks

#check BridgeFormalV2.Proofs.nonempty_blocks

#print BridgeFormalV2.NonemptyBlocksGoal

#print axioms BridgeFormalV2.Proofs.nonempty_blocks

example : BridgeFormalV2.ExpansionGoal := BridgeFormalV2.Proofs.expansion

#check BridgeFormalV2.Proofs.expansion

#print BridgeFormalV2.ExpansionGoal

#print axioms BridgeFormalV2.Proofs.expansion

example : BridgeFormalV2.PrefixSplitGoal := BridgeFormalV2.Proofs.prefix_split

#check BridgeFormalV2.Proofs.prefix_split

#print BridgeFormalV2.PrefixSplitGoal

#print axioms BridgeFormalV2.Proofs.prefix_split

example : BridgeFormalV2.SourceChronologyGoal := BridgeFormalV2.Proofs.source_chronology

#check BridgeFormalV2.Proofs.source_chronology

#print BridgeFormalV2.SourceChronologyGoal

#print axioms BridgeFormalV2.Proofs.source_chronology

example : BridgeFormalV2.SuffixExpansionGoal := BridgeFormalV2.Proofs.suffix_expansion

#check BridgeFormalV2.Proofs.suffix_expansion

#print BridgeFormalV2.SuffixExpansionGoal

#print axioms BridgeFormalV2.Proofs.suffix_expansion

example : BridgeFormalV2.ExogenousImageGoal := BridgeFormalV2.Proofs.exogenous_image

#check BridgeFormalV2.Proofs.exogenous_image

#print BridgeFormalV2.ExogenousImageGoal

#print axioms BridgeFormalV2.Proofs.exogenous_image

example : BridgeFormalV2.ObservationFibreGoal := BridgeFormalV2.Proofs.observation_fibre

#check BridgeFormalV2.Proofs.observation_fibre

#print BridgeFormalV2.ObservationFibreGoal

#print axioms BridgeFormalV2.Proofs.observation_fibre

example : BridgeFormalV2.ForwardPolicyGoal := BridgeFormalV2.Proofs.forward_policy

#check BridgeFormalV2.Proofs.forward_policy

#print BridgeFormalV2.ForwardPolicyGoal

#print axioms BridgeFormalV2.Proofs.forward_policy

example : BridgeFormalV2.ReversePolicyGoal := BridgeFormalV2.Proofs.reverse_policy

#check BridgeFormalV2.Proofs.reverse_policy

#print BridgeFormalV2.ReversePolicyGoal

#print axioms BridgeFormalV2.Proofs.reverse_policy

example : BridgeFormalV2.EpigraphEqualityGoal := BridgeFormalV2.Proofs.epigraph_equality

#check BridgeFormalV2.Proofs.epigraph_equality

#print BridgeFormalV2.EpigraphEqualityGoal

#print axioms BridgeFormalV2.Proofs.epigraph_equality
