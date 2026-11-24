# General support bound: proof audit and mechanization boundary

Parent: Astra v1; no statement amendment. The argument below is general written mathematics. `check.py` checks its polynomial slack identities symbolically and its four declared instances exactly. It does NOT formally verify the dynamics-to-inequalities reduction or the general support lemmas. Accordingly the full universal theorem remains a proposal under the original goal's checker-backed-proof standard. No finite result is promoted to a general formal proof.

## Precise statement and information pattern

Let T be finite and 0<=r<=T. For deterministic compatible real matrices, let x(t+1)=A_t x(t)+B_t u_t+E_t w_t, with fixed x(0). Scalar disturbance coordinates range independently over [-rho_t,rho_t], rho_t>=0; scalar control coordinates satisfy |u_t|<=beta_t, beta_t>=0. Multiple coordinates may be flattened into time-labelled coordinates. The only state constraints are L<=X<=H at T, where X and Y are fixed linear terminal functionals, L<=H finite, and the guaranteed reward is Y. The data are deterministic and finite.

An admissible policy consists of one fixed prefix a and one Borel map from the exact current state x(r) to an entire suffix b in its box, chosen before the suffix disturbances. Feasibility and a guarantee q mean: for every prefix disturbance and every independently chosen suffix disturbance, the resulting trajectory satisfies L<=X<=H and Y>=q. There are no intermediate observations or constraints. Define V_r as the supremum of all feasible q; define V_0 similarly with one constant full block. Assume at least one feasible open-loop block with guarantee J. This ensures nonempty feasible classes. Bounded terminal effects and bounded controls make the values finite even for arbitrary Borel policies.

Repeated substitution of the dynamics gives

X=dx+px(a)+cx(b)+zx(wpre)+ex(wpost),
Y=dy+py(a)+cy(b)+zy(wpre)+ey(wpost).

The identity follows inductively by multiplying the previous expansion by A_t and appending B_t u_t+E_t w_t. Coefficients of w and u are computed independently; neither E=B nor invertibility of any A_t is required. Define Sx_pre=sum_pre rho_t |Dxt| and Sx_post analogously, Sx=Sx_pre+Sx_post; define Sy likewise. Let Hx=sum_suffix beta_t|Cxt|, Hy=sum_suffix beta_t|Cyt|. For lambda,mu>=0 put

Hp=sum_prefix beta_t|Cyt+(lambda-mu)Cxt|,
Hm=sum_suffix beta_t|Cyt+(lambda-mu)Cxt|,
D0=dy-Sy+lambda(dx-L-Sx)+mu(H-Sx-dx)+Hp+Hm,
Delta=(lambda+mu)Hx+Hy-Hm.

Claim: J<=V0<=Vr<=D0+Delta and 0<=Vr-V0<=D0+Delta-J. If J=D0 and Delta=0 exactly, then Vr=V0=J. This is a sufficient certificate, not a necessary criterion and not an ordering of values for two different observation times.

## All required bound directions

For a scalar row v and a box |h_i|<=gamma_i, gamma_i>=0, each v_i h_i <= |v_i||h_i| <= gamma_i|v_i|. Summation gives v.h<=sum gamma_i|v_i|. Taking h_i=gamma_i when v_i>=0 and -gamma_i otherwise attains the bound, including zero coefficients; reversing all signs attains its negative. Thus these supports are exact for all continuous disturbances, not sampled approximations. The same argument bounds controls, and maxima for distinct rows need not be attained at one point.

Fix any feasible (a,pi,q). At a prefix disturbance attaining zx=-Sx_pre the measured state is fixed, and pi selects one fixed suffix b. For this b, cx(b)<=Hx. Choose a future disturbance attaining ex=-Sx_post, which is allowed independently of that measured state and b. Robust lower-strip feasibility gives

L <= dx+px(a)+cx(b)-Sx <= dx+px(a)+Hx-Sx.

Therefore gL=dx+px(a)-L-Sx+Hx>=0. This is only a necessary condition. The chosen b is never claimed to be the support-maximizing box corner.

At a possibly different prefix attaining zx=+Sx_pre, the policy selects another suffix b. Now cx(b)>=-Hx. Choose a future disturbance attaining ex=+Sx_post. Robust upper-strip feasibility gives

dx+px(a)-Hx+Sx <= dx+px(a)+cx(b)+Sx <= H.

Therefore gU=H-Sx+Hx-dx-px(a)>=0. This proves the upper side with the correct direction; zero upper dual weight does not remove the original feasibility condition.

At a third possibly different prefix attaining zy=-Sy_pre, its suffix b satisfies cy(b)<=Hy. Choose a future disturbance attaining ey=-Sy_post. The guaranteed reward gives

q <= dy+py(a)+cy(b)-Sy <= dy+py(a)+Hy-Sy.

Hence gR=dy+py(a)+Hy-Sy-q>=0. The suffix is selected before the future disturbance, so future support minimization is legitimate. This step would not apply to a later-reacting suffix control class without new reasoning.

Finally the prefix box implies py(a)+(lambda-mu)px(a)<=Hp. Hence gP=Hp-py(a)-(lambda-mu)px(a)>=0. Crucially the same fixed a appears in all four scalar inequalities. They hold separately because the policy must work for every prefix. No jointly extremizing disturbance, history measurement, correlation restriction, or additional sensor has been introduced.

The following exact identity is checked by SymPy over arbitrary real scalar symbols:

D0+Delta-q = gR + lambda*gL + mu*gU + gP.

Every term on the right is nonnegative. Thus q<=D0+Delta for every feasible q; taking the supremum proves the proposed adaptive upper bound. The bound is finite. Constant maps b(x)=b0 are Borel and implement every feasible open-loop block, so J<=V0<=Vr. Consequently Vr-V0<=D0+Delta-V0<=D0+Delta-J; both inequality directions matter.

For completeness D0 is an open-loop upper bound: a robust open-loop block satisfies dx+px(a)+cx(b)-L-Sx>=0 and H-Sx-dx-px(a)-cx(b)>=0 and q<=dy+py(a)+cy(b)-Sy. Add the two nonnegative weighted slacks and maximize the remaining linear full-block control expression over its box, obtaining D0. A feasible witness with J=D0 therefore certifies the open-loop optimum. The adaptive sandwich with Delta=0 then gives exact equality; overlapping decimals are irrelevant.

## Defect sign and zero condition

Put k=lambda-mu. For every suffix coordinate, triangle inequality yields

|Cy+k Cx| <= |Cy|+|k||Cx| <= |Cy|+(lambda+mu)|Cx|,

since |lambda-mu|<=lambda+mu for nonnegative multipliers (split lambda>=mu and its complement). Multiply by beta>=0 and sum: Delta>=0. The symbolic checker verifies the decomposition into these two nonnegative triangle defects, not the general absolute-value inequalities themselves.

When mu=0 and lambda>0 and beta>0, coordinate defect is zero exactly when Cx and Cy have the same weak sign. To see this, if their signs agree then the absolute value of the sum is the sum of absolute values; if they are strictly opposite, |Cy+lambda Cx|=abs(|Cy|-lambda|Cx|), strictly below their sum because both are positive. Zero coefficients contribute zero. Lambda=0 makes the defect zero regardless of signs. This characterization is not used when both multipliers are positive. Positive Delta provides only an upper bound on information value, never a lower bound.

## Exact instance-to-model bridge

The pinned files specify T=120, x0=(0,1), |u_t|<=1, |w_t|<=1/2, [L,H]=[2,10]. For each model, the checker forms A^k B and A^k E by separate forward recurrences for k=0,...,119, reverses them into chronological terminal columns, and forms A^120 x0 independently. It evaluates the full 120-step nominal trajectory and the expanded sum exactly. Scalar box supports bound every independent disturbance sequence. The open-loop witness is admissible regardless of observation, and its robust lower and upper strip endpoints are checked separately, as are every control bound and the reward. The checker also recomputes D0 and tests J=D0 by rational equality. At r104 Delta is tested as a rational zero, not via float conversion. The printed and reconstructed-decimal manifests remain separate models; neither equals confirmed author/trigonometric data by assumption.

Read directly: research/sources/A4-p4.png, physical p4 / printed p69, Assumption 1 (current state and whole next block); A4-p12.png, physical p12 / printed p77, equation (3.1), strip, horizon, and reported cutoff. PDF parent SHA256 is frozen in parents.json. The published J=1.501102 is not the exact printed-coefficient witness value. This known discrepancy is preserved; no coefficient repair is performed.

## Limits of this stage

Astra's reversed-corner control at r67 starts from a corner already failing its joint favorable-sign predicate. Such a rejection does not discriminate the particular sign reversal. Stage B instead verifies a favorable r104 corner first and then flips a nonzero final coordinate. R67 serves only as a positive-defect/invalid-zero discriminator.

No closest-source novelty audit is performed here: Stage C owns original A4 reference [14]. No necessity of r104, r103 gain, all-model cutoff, published-policy reproduction, or universal formalized theorem is asserted. Installed Lean is present but compiled mathlib dependencies were absent at the inspected project paths; no build, download or comparator was attempted. The general proof bridge above remains written mathematics, and the scientific goal remains unachieved pending coordinator inspection.
