import AroProofs.BridgeF1F2
import AroProofs.Aroform
import AroProofs.BridgeF3Draft
import AroProofs.BridgeF4CornerLP
import AroProofs.BridgeF4ExtremeLP
import AroProofs.BridgeG2ConicSupport
import AroProofs.BridgeO4ClosureValue
import AroProofs.BridgeG1Multistage
import AroProofs.BridgeO1ADRExactness

-- BridgeFormalV2 F1/F2 (10 targets)
#print axioms BridgeFormalV2.Proofs.nonempty_blocks
#print axioms BridgeFormalV2.Proofs.expansion
#print axioms BridgeFormalV2.Proofs.prefix_split
#print axioms BridgeFormalV2.Proofs.source_chronology
#print axioms BridgeFormalV2.Proofs.suffix_expansion
#print axioms BridgeFormalV2.Proofs.exogenous_image
#print axioms BridgeFormalV2.Proofs.observation_fibre
#print axioms BridgeFormalV2.Proofs.forward_policy
#print axioms BridgeFormalV2.Proofs.reverse_policy
#print axioms BridgeFormalV2.Proofs.epigraph_equality

-- AroProofs.Aroform P1-P3 (5 core targets)
#print axioms AroProofs.Aroform.info_value_monotone
#print axioms AroProofs.Aroform.l1_eq_max_sum_diff
#print axioms AroProofs.Aroform.one_d_exactness
#print axioms AroProofs.Aroform.l2a_diff_two_path
#print axioms AroProofs.Aroform.l2a_sum_two_path

-- BridgeFormalV3 F3 draft (4 targets)
#print axioms BridgeFormalV3.Proofs.future_expansion
#print axioms BridgeFormalV3.Proofs.attained_support
#print axioms BridgeFormalV3.Proofs.robust_row
#print axioms BridgeFormalV3.Proofs.exact_tightening

-- R12 Run-01 F4: Finite Vertex-LP & Borel Selector over Zonotope Xi (9 targets)
#print axioms AroProofs.BridgeF4VertexLP.borel_right_inverse_exists
#print axioms AroProofs.BridgeF4VertexLP.vertex_lp_to_aro
#print axioms AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_aro
#print axioms AroProofs.BridgeF4VertexLP.vertex_lp_epigraph_eq_source
#print axioms AroProofs.BridgeF4VertexLP.zonotopeVertices_finite
#print axioms AroProofs.BridgeF4VertexLP.extreme_vertex_lp_to_aro
#print axioms AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_aro
#print axioms AroProofs.BridgeF4VertexLP.extreme_vertex_lp_epigraph_eq_source
#print axioms AroProofs.BridgeF4VertexLP.extreme_vertex_lp_eq_corner_lp

-- R12 Run-01 G2: General Compact Convex / Conic Support Tightening (7 targets)
#print axioms AroProofs.BridgeG2ConicSupport.general_attained_support
#print axioms AroProofs.BridgeG2ConicSupport.general_robust_row
#print axioms AroProofs.BridgeG2ConicSupport.general_exact_tightening
#print axioms AroProofs.BridgeG2ConicSupport.box_support_eq_f3
#print axioms AroProofs.BridgeG2ConicSupport.l1_cross_polytope_support
#print axioms AroProofs.BridgeG2ConicSupport.l2_soc_ball_support
#print axioms AroProofs.BridgeG2ConicSupport.l2_ball_not_finset_conv_2d

-- R12 Run-01 O4 (partial): Single-Closure Value of Measurement Foundation (7 targets)
#print axioms AroProofs.BridgeO4ClosureValue.openLoop_subset_aro
#print axioms AroProofs.BridgeO4ClosureValue.openLoop_subset_source
#print axioms AroProofs.BridgeO4ClosureValue.zero_gain_of_unconstrained_terminal
#print axioms AroProofs.BridgeO4ClosureValue.zero_gain_of_prefix_in_terminal_kernel
#print axioms AroProofs.BridgeO4ClosureValue.openLoop_eq_shared_corner_lp
#print axioms AroProofs.BridgeO4ClosureValue.strict_gain_iff_corner_separation
#print axioms AroProofs.BridgeO4ClosureValue.exists_strict_value_of_measurement_gap

-- R12 Run-01 G1 (partial): Multi-Closure k >= 2 Bridge & Markov vs History (6 targets)
#print axioms AroProofs.BridgeG1Multistage.multistage_stage_split
#print axioms AroProofs.BridgeG1Multistage.multistage_forward_policy
#print axioms AroProofs.BridgeG1Multistage.multistage_reverse_policy
#print axioms AroProofs.BridgeG1Multistage.multistage_history_epigraph_eq_aro
#print axioms AroProofs.BridgeG1Multistage.multistage_markov_subset_history
#print axioms AroProofs.BridgeG1Multistage.exists_markov_strictly_weaker_than_history_k2

-- R12 Run-01 O1 (partial): ADR Exactness Simplex/Syzygy & 1D-vs-2D Bridge Dichotomy (7 targets)
#print axioms AroProofs.BridgeO1ADRExactness.static_subset_adr_subset_aro
#print axioms AroProofs.BridgeO1ADRExactness.adr_exact_on_simplex
#print axioms AroProofs.BridgeO1ADRExactness.barycentric_syzygy_adr_coupling
#print axioms AroProofs.BridgeO1ADRExactness.chen_zhang_t3_adr_gap
#print axioms AroProofs.BridgeO1ADRExactness.bridge_adr_subset_aro_and_source
#print axioms AroProofs.BridgeO1ADRExactness.bridge_adr_exact_1d
#print axioms AroProofs.BridgeO1ADRExactness.exists_bridge_2d_strict_adr_gap
