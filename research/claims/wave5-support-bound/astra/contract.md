# Proposed support-defect certificate v1

Frozen before new arithmetic. This is a proposal, not a general checked theorem.

Class: finite-horizon linear deterministic-coefficient dynamics, terminal scalar strip L<=X<=H and scalar reward Y to maximize, independent continuous symmetric disturbance boxes at every time, no intermediate constraints, independent symmetric control boxes. A fixed prefix a is chosen before disturbances. One exact current-state measurement at r selects a whole suffix b before all future disturbances; no later observation. Feasible open-loop witness required. No assumption E=B or rotation coefficients.

Terminal impulse rows are C_x,C_y for controls, D_x,D_y for disturbances, drift d. Define S_x,S_y as full disturbance supports, Hx=sum_suffix beta_t|C_xt|, Hy=sum_suffix beta_t|C_yt| and Hmix=sum_suffix beta_t|C_yt+(lambda-mu)C_xt|. For any lambda,mu>=0 let D0 be the usual open-loop box dual expression, retaining both strip sides. Proposed adaptive bound: V_r<=D0+Delta, Delta=(lambda+mu)Hx+Hy-Hmix>=0. A feasible open-loop reward J gives 0<=V_r-V_0<=D0+Delta-J. If J=D0 and Delta=0, equality follows conditional on the general argument.

Finite obligation: use the exact existing M0 optimal certificate multipliers and witnesses, both input variants, r67 and r104 only. Recompute Delta exactly; check both terminal strip sides through the unmodified M0 checker. Summarize actual wave-4 certificate bindings without modifying them. No r103 experiment. Positive controls: existing M0 certificate accepted and nonnegative support defect; invalid controls: corrupted M0 objective rejected and reversed nonzero suffix corner fails the favorable-sign predicate. Do not claim this predicate necessary for zero information value.

General falsification attacks: independent prefix extremes used for viability and reward must be legitimate separate necessary tests, not a fictitious joint disturbance. Upper-strip omission is allowed only as an explicitly relaxed bound, never as feasibility. Here both viability inequalities are retained. General verification and nearest-source comparison remain external obligations.
