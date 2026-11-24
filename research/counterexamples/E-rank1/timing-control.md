# E timing supplement: one prefix with two hidden suffixes

This separately frozen control supplements `derivation.md` §4 without changing the original six inputs, code, manifest or check outputs. It addresses the question packet's explicit timing/correlation obligation. It is part of the same rank-one boundary investigation, not a second research branch.

Use the scalar dynamics of the six-case experiment with B_1=(1,-1), U_1=[0,2]^2, H=-1,h=0,c=1,d0=0. Keep exactly TWO complete disturbance paths (0,-1) and (0,1). There is ONE prefix and one measured state x_1=0. A valid prefix or state policy must choose the SAME b before the suffix is known. Thus t=b_1-b_2 must satisfy t>=1 from the first path's hard constraint and t<=q-1 from the second path's cost constraint.

At q=2 the common b=(3/2,1/2), t=1 gives terminal states (0,2), satisfying both hard and cost bounds. At q=1 the actual rows -t<=-1 and t<=0 sum to 0<=-1. This certificate proves infeasibility over the entire continuous rational box without enumerating action menus. The same contradiction also rules out q=0.

An illegal complete-path oracle chooses b=(1,0) for suffix -1 and b=(0,1) for suffix +1, giving terminal state zero on each path and apparently meeting q=0. `checks/timing_control.py` rejects this assignment because equal prefixes are assigned different actions. It does not treat different complete paths as different observed prefixes or complete the set by marginal products.

This one-prefix residual system is empty at q=1 even though distinct-prefix pair tests have no pairs to reject. The singleton nonemptiness qualification in `E-R1-child-v1` remains necessary. This is a new exact dynamics-realizable control, with result/command/output hashes in `checks/timing-manifest.json` and `checks/timing-observation.json`. It is finite evidence, not a formal proof of the general child or source applicability.
