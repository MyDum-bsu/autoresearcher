# Counterexample O1: Refutation of Full-Rank Recourse ADR Exactness (`H-O1-1`) & Linear Gap Scaling (`O1 / O2 / O5`)

> **Target Atlas node:** `conj-o1-adr-exactness-char` (`O1 + O2 + O5`)
> **Verdict:** **REFUTED (`H-O1-1`)** — full-rank / invertible recourse $B \in \mathrm{SL}_2(\mathbb{Z})$ ($\det B = 1$) combined with a coordinatewise terminal box ($H = I_2$) is **NOT sufficient** for ADR exactness ($V_{\mathrm{ADR}} = V_{\mathrm{ARO}}$). Off-diagonal coupling in $B$ alone triggers the square barycentric syzygy obstruction. Conversely, **coordinatewise diagonal** $(A, B, E, H)$ restores exactness in **every** dimension $n \ge 1$ and horizon $(r, q)$.
> **Executable exact oracle:** `checks/check_o1_shear_gap.py` (exact `fractions.Fraction` LP + SymPy continuous-box certificate, `-B` and `-B -O` identical).
> **Lean 4 formalization:** `verification/lean/AroProofs/BridgeO1FullRankRecourse.lean` (zero `sorry`, standard axioms only).

---

## 1. Refutation of `H-O1-1`: Unimodular Shear Witness ($B \in \mathrm{SL}_2(\mathbb{Z}), H = I_2$)

Consider the 2D single-closure `BridgeFormalV2.Data` instance ($n = m = p = \mathrm{rows} = 2$, $r = q = 1$, $x_0 = 0$) with $A = E = H = I_2$, control box $U = [-\tfrac{1}{2}, \tfrac{1}{2}]^2$, disturbance radius $\rho = 1$, terminal box $g_{\min} = (0, -1)^\top$, $g_{\max} = (4, 3)^\top$, linear cost $c = (1, 1)^\top$, and **invertible unimodular** recourse matrix:
$$B = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}, \qquad \det(B) = 1.$$

By F3 exact support tightening (`BridgeFormalV3.Proofs.exact_tightening`), eliminating the future disturbance $w^+ \in [-1, 1]^2$ yields the equivalent nominal constraints for all $v = (v_0, v_1) \in [-1, 1]^2$:
1. $(u_{1,0} + u_{1,1}) + (u_{2,0}(v) + u_{2,1}(v)) + v_0 \in [1, 3]$,
2. $u_{1,1} + u_{2,1}(v) + v_1 \in [0, 2]$,
3. $(u_{1,0} + 2u_{1,1}) + (u_{2,0}(v) + 2u_{2,1}(v)) + v_0 + v_1 + 2 \le \eta$.

### Exact Adaptive Optimum: $V_{\mathrm{ARO}} = V_{\mathrm{source}} = 5$

Choose $u_1 = (\tfrac{1}{2}, \tfrac{1}{2})$ and the continuous (hence Borel-measurable) piecewise-affine policy:
$$u_{2,0}(v_0, v_1) = -\tfrac{1}{2} v_0, \qquad u_{2,1}(v_0, v_1) = \max\!\left(-\tfrac{1}{2} v_0,\ -\tfrac{1}{2} v_1,\ 0\right).$$
On the entire continuous box $[-1, 1]^2$:
- $u_{2,0}(v) \in [-\tfrac{1}{2}, \tfrac{1}{2}]$ and $u_{2,1}(v) \in [0, \tfrac{1}{2}] \subseteq [-\tfrac{1}{2}, \tfrac{1}{2}]$;
- $1 + u_{2,0} + u_{2,1} + v_0 = 1 + \tfrac{1}{2} v_0 + u_{2,1} \in [1, 3]$;
- $\tfrac{1}{2} + u_{2,1} + v_1 \in [0, 2]$;
- $\tfrac{7}{2} + \tfrac{1}{2} v_0 + v_1 + 2 \max(-\tfrac{1}{2} v_0, -\tfrac{1}{2} v_1, 0) = \tfrac{7}{2} + \max(-\tfrac{1}{2} v_0 + v_1,\ \tfrac{1}{2} v_0,\ \tfrac{1}{2} v_0 + v_1) \le \tfrac{7}{2} + \tfrac{3}{2} = 5$.

### Universal Affine Lower Bound: $V_{\mathrm{ADR}} \ge 6$

For **any** affine policy $u_2(v) = b_0 + K v$:
1. At $v = (-1, 1)$: $u_{1,0} + u_{1,1} + u_{2,0}(-1,1) + u_{2,1}(-1,1) \ge 2$ with each term $\le \tfrac{1}{2}$ forces $u_{1,0} = u_{1,1} = u_{2,1}(-1, 1) = \tfrac{1}{2}$.
2. At $v = (1, -1)$: $u_{1,1} + u_{2,1}(1,-1) \ge 1$ with each term $\le \tfrac{1}{2}$ forces $u_{2,1}(1, -1) = \tfrac{1}{2}$.
3. By the **square barycentric syzygy** on the affine function $u_{2,1}$:
   $$u_{2,1}(-1, -1) + u_{2,1}(1, 1) = u_{2,1}(-1, 1) + u_{2,1}(1, -1) = 1.$$
   Since $u_{2,1}(-1, -1) \le \tfrac{1}{2}$, we must have $u_{2,1}(1, 1) \ge \tfrac{1}{2}$.
4. Combining with the box lower bound $u_{2,0}(1, 1) \ge -\tfrac{1}{2}$ at $v = (1, 1)$ and $w^+ = (1, 1)$:
   $$\eta \ge u_{1,0} + 2u_{1,1} + u_{2,0}(1,1) + 2u_{2,1}(1,1) + 4 \ge \tfrac{1}{2} + 1 - \tfrac{1}{2} + 1 + 4 = 6.$$

Thus $V_{\mathrm{ARO}} = 5 < 6 = V_{\mathrm{ADR}}$ (gap $= 1$, ratio $= 6/5$), refuting `H-O1-1`.

---

## 2. Sharp Boundary Contrast & O2 Linear Gap Scaling

1. **Diagonal contrast (`O1` positive boundary):** Replacing $B = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ by the diagonal matrix $B_{\mathrm{diag}} = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ (identical per-row $\ell_1$-authority on the exact same data) restores exactness ($V_{\mathrm{ARO}} = V_{\mathrm{ADR}}$, gap $= 0$). In Lean 4 (`bridge_adr_exact_diagonal`), we prove that diagonal $(A, B, E, H)$ guarantees $V_{\mathrm{ADR}} = V_{\mathrm{ARO}} = V_{\mathrm{source}}$ in **every** dimension $n \ge 1$ and horizon $(r, q)$.
2. **Linear $\Omega(n)$ gap scaling (`O2`):** Taking $k \ge 1$ independent 2D rank-1 blocks ($n = 2k$, $m = k$) gives $V_{\mathrm{ARO}}(k) = 6k$ and $V_{\mathrm{ADR}}(k) \ge 8k$ (additive gap $\ge 2k = n$, multiplicative ratio $\ge 4/3$), even when the affine policy is allowed arbitrary cross-block feedback $K \in \mathbb{R}^{k \times 2k}$.
