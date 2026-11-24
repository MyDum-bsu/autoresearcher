# Stage A plan — source-native continuous A4 single closure

Task aro-discovery-k4t. Verified worktree <workspace>/aro-discovery-campaign and branch task/aro-discovery-k4t-campaign before this first write. Existing artifacts and baseline are readonly. GoalAchieved remains false; coordinator inspection is required. No novelty or paper-error claim is planned.

## Scope frozen before implementation

Exactly four scientific cases, in priority order: a4_printed/T1=67; a4_reconstructed_decimal/T1=67; a4_printed/T1=104; a4_reconstructed_decimal/T1=104. T=120, x0=(0,1), |u|<=1, independent continuous |w_t|<=1/2, terminal 2<=x1(T)<=10, maximize guaranteed x2(T). First block fixed in advance; exact current state at T1 selects the entire remaining open-loop block. No suffix observation, prefix oracle, correlated-path substitution, closure-time sweep or sampled disturbance grid.

## Derivation and implementation sequence

1. Preserve fresh original A4 page extractions with source hash, inspect assumptions on physical pp2–6, support approximation pp9–12, benchmark pp12–13 and conclusion/references pp15–17. Inspect M0 generator/checker, README and controls. Copy only necessary pinned inputs and arithmetic/checking modules, preserving origin hashes.
2. Derive exact reachable planar zonotope at T1. Use exact orientation to enumerate its actual vertices, not a direction grid. Propose a finite LP with common first block and one independent suffix per reachable vertex. Explain necessity and convex interpolation sufficiency, including a deterministic every-state triangulated policy that observes state only. Treat this familiar fixed-recourse reduction as reconstruction, not contribution.
3. Freeze binding/control contract before numerical runs. Numerical LP output is a proposal. Seek an exact lower certificate by rationalizing controls with robust slack and checking all vertex terminal/reward rows exactly. Seek an exact upper certificate through nonnegative rationalized LP row multipliers with explicit residual box-support correction; no solver flag or tolerance is a certificate. Report a nonzero rigorous gap honestly. Reuse M0 exact primitives where adequate; no installation.
4. Execute first printed T1=67 end to end, then other frozen cases. Preserve actual raw solver/checker stdout/stderr, commands, input/source/code identities. Bound each process; use Python3 -B and wave-local scratch. If exact certificates fail, preserve proposals and the precise failed inequality rather than retrying automatically.
5. Validate normal and optimized Python; invalid controls frozen below. Save model/source comparison, formulation/policy semantics, contracts, runnable code, certificates/raw outputs, result.json, outcome.md and Russian briefing. Leave all four case dispositions explicit.

## Frozen scoped verification inventory

No extra scientific cases or tiny synthetic fixtures. Per available produced scientific certificate: positive exact verification; incorrect information field (suffix-dependent policy); terminal violation (replace first suffix by all -1); false reward (raise claimed lower to upper+1); negative multiplier; input-binding mutation; closure-time mutation; vertex-list deletion. Run all mutations without asserting which first error must occur. Normal/-O results must agree. These are scoped arithmetic/evidence checks, not a formal proof of the general vertex theorem and not novelty judgments.

## Resource/stop policy

90 minutes / 60 total instructional tool calls including nested; reserve calls for evidence and reporting. No nested agents/workflows/objectives, automatic retry/fallback, commits/pushes, installs/system changes, comparator, live scientific writes or attestation. Skip bootstrap commands that may write live state. Billing and provider-native retry accounting unknown. Independent Stage B belongs to the coordinator, not this worker.
