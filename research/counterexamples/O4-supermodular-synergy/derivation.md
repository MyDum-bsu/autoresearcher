# Counterexample O4: Supermodular Synergy (Refutation of Submodularity of $G(R)$) & Bidirectional Single-Closure Dominance (`O4 / O7`)

> **Target Atlas node:** `conj-o4-closure-scheduling` (`O4 + O7`)
> **Verdict:** **REFUTED** — the value-of-information set function $G(R) = V(\emptyset) - V(R)$ is **neither submodular nor supermodular** on LTI `BridgeFormalV2.Data` systems at $T=3$, and single-closure strict dominance (`O7`) is **bidirectional** ($V(\{1\}) < V(\{2\})$ and $V(\{2\}) < V(\{1\})$ both occur on 1D LTI systems).
> **Executable exact oracle:** `checks/check_o4_synergy.py` (exact `fractions.Fraction` LP + SymPy continuous-box certificate, `-B` and `-B -O` identical).
> **Lean 4 formalization:** `verification/lean/AroProofs/BridgeO4Scheduling.lean` (zero `sorry`, standard axioms only).

---

## 1. Strict Supermodular Synergy Witness (Refuting Submodularity of $G(R)$)

Consider the 4-state, 1-control, 1-disturbance LTI nilpotent shift-register system at horizon $T = 3$ with $x_0 = 0$, $U = [-1, 1]$, $\rho = 1$ ($w_t \in [-1, 1]$):

$$A = \begin{pmatrix} 0 & 0 & 0 & 1 \\ 1 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix}, \quad B = \begin{pmatrix} 1 \\ 0 \\ 0 \\ 0 \end{pmatrix}, \quad E = \begin{pmatrix} 0 \\ 0 \\ 0 \\ 1 \end{pmatrix},$$

so that $A e_3 = e_0 \mapsto e_1 \mapsto e_2 \mapsto 0$. The terminal state after 3 steps is:

$$x_3 = A^2(B u_0 + E w_0) + A(B u_1 + E w_1) + (B u_2 + E w_2) = \begin{pmatrix} u_2 + w_1 \\ u_1 + w_0 \\ u_0 \\ w_2 \end{pmatrix}.$$

Terminal constraints $H x_3 \in [0, 10]^4$ and linear cost $c^T x_3 = x_3^{(2)} = u_0$ encode:
$$u_0 \ge |u_1 + w_0| \quad \text{and} \quad u_0 \ge |u_2 + w_1| \qquad \forall (w_0, w_1, w_2) \in [-1, 1]^3.$$

### Exact Optimal Values Across All Four Schedules $R \subseteq \{1, 2\}$

- **$R = \emptyset$ (open loop):** $u_1, u_2 \in [-1, 1]$ are constant, so $\max_{w_0 \in [-1,1]} |u_1 + w_0| \ge 1 \implies u_0 \ge 1$. Attained by $u_0 = 1, u_1 = 0, u_2 = 0$: **$V(\emptyset) = 1$**.
- **$R = \{1\}$ (closure at $t=1$ only):** $u_1(x_1) = -w_0$ cancels $w_0$, but $u_2$ only sees $x_1 = (u_0, 0, 0, w_0)^T$ (independent of $w_1$), so $\max_{w_1 \in [-1,1]} |u_2 + w_1| \ge 1 \implies u_0 \ge 1$: **$V(\{1\}) = 1$**, **$G(\{1\}) = 0$**.
- **$R = \{2\}$ (closure at $t=2$ only):** $u_2(x_2) = -w_1$ cancels $w_1$, but $u_1$ is chosen before $t=2$ (constant), so $\max_{w_0 \in [-1,1]} |u_1 + w_0| \ge 1 \implies u_0 \ge 1$: **$V(\{2\}) = 1$**, **$G(\{2\}) = 0$**.
- **$R = \{1, 2\}$ (both closures):** $u_0 = 0$, $u_1(x_1) = -x_1^{(3)} = -w_0$, $u_2(x_1, x_2) = -x_2^{(3)} = -w_1$ yields $x_3 = (0, 0, 0, w_2)^T$: **$V(\{1, 2\}) = 0$**, **$G(\{1, 2\}) = 1$**.

**Submodularity defect:**
$$\bigl(G(\{1,2\}) - G(\{1\})\bigr) - \bigl(G(\{2\}) - G(\emptyset)\bigr) = (1 - 0) - (0 - 0) = +1 > 0.$$

**Algorithmic consequence (`O4`):** Every singleton closure has zero marginal gain ($G(\{1\}) = G(\{2\}) = 0$), so greedy closure selection has **zero approximation ratio** on general LTI systems.

---

## 2. Strict Submodularity & Bidirectional Single-Closure Dominance (`O4 + O7`)

1. **Early dominance + strict submodularity** ($A = 1, B = 1, E = 1, U = [-1/2, 1/2], \rho = 1, g \in [-2, 10], c = 1$):
   $$V(\emptyset) = 4, \quad V(\{1\}) = 2, \quad V(\{2\}) = 3, \quad V(\{1,2\}) = 2 \implies \text{defect} = -1 < 0, \; V(\{1\}) < V(\{2\}).$$
2. **Late dominance** ($A = 1/2, B = 1, E = 1, U = [-1, 1], \rho = 1, g \in [-2, 10], c = 1$):
   $$V(\emptyset) = \tfrac{3}{2}, \quad V(\{1\}) = 1, \quad V(\{2\}) = 0, \quad V(\{1,2\}) = 0 \implies \text{defect} = -\tfrac{1}{2} < 0, \; V(\{2\}) < V(\{1\}).$$

Thus on LTI `BridgeFormalV2.Data` systems at $T = 3$:
- $G(R)$ is **neither submodular nor supermodular**;
- Neither earlier nor later single closures universally dominate.
