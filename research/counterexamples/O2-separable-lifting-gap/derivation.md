# Counterexample O2/O5: Refutation of Coordinate-Separable Lifting Exactness (`H-O2-1`), $\Omega(d)$ Cross-Polytope Scaling, and Single-Feature Diagonal-Hinge Restoration

> **Target Atlas node:** `conj-o1-adr-exactness-char` (`O1 + O2 + O5`)
> **Verdict:** **REFUTED (`H-O2-1`)** — coordinate-wise segregated / $|\cdot|$-lifted ADR (and in fact **every** coordinate-separable nonlinear policy $y(\xi_0, \xi_1) = y_0 + f_0(\xi_0) + f_1(\xi_1)$ with arbitrarily many axis-aligned breakpoints) gives **zero improvement** over standard ADR on the 2D box $[-1, 1]^2$ and on both frozen `BridgeFormalV2.Data` witnesses (`bridgeAdrGapData`: $6 < 8$; `bridgeFullRankShearData`: $5 < 6$). Conversely, on the $d$-dimensional $\ell_1$ cross-polytope $B_1^d$, standard ADR suffers an $\Omega(d)$ multiplicative ratio ($d$ vs $1$) that coordinate-wise $|\cdot|$-lifting collapses to $0$, while on $[-1, 1]^2$ the **single scalar interaction feature** $\phi_{\mathrm{diag}}(\xi) = |\xi_0 - \xi_1|$ makes lifted ADR **100% exact** for every fixed-recourse ARO and every 2D box-deviation bridge system.
> **Executable exact oracle:** `checks/check_o2_lifting_gap.py` (exact `fractions.Fraction` LP + SymPy continuous-box certificate, `-B` and `-B -O` identical).
> **Lean 4 formalization:** `verification/lean/AroProofs/BridgeO2LiftedADR.lean` (zero `sorry`, standard axioms only).

---

## 1. Exact $\Omega(d)$ Cross-Polytope Ratio vs. Segregated $|\cdot|$-Lifting Exactness (`O2`)

On the $d$-dimensional $\ell_1$ cross-polytope $B_1^d = \{\xi \in \mathbb{R}^d : \sum_{i=1}^d |\xi_i| \le 1\}$, consider the $d$-dimensional Chen–Zhang fixed-recourse ARO:
$$\min_{y(\cdot)} \max_{\xi \in B_1^d} \sum_{i=1}^d y_i(\xi) \quad \text{s.t.} \quad y_i(\xi) \ge \xi_i,\;\; y_i(\xi) \ge -\xi_i \quad \forall i \in \{1, \dots, d\}.$$

- **Fully adaptive optimum:** $y_i^*(\xi) = |\xi_i|$ achieves $V_{\mathrm{ARO}}(d) = 1$.
- **Universal ADR lower bound:** By the $d$ origin-centered syzygies $\frac{1}{2} e_i + \frac{1}{2}(-e_i) = 0$, every affine rule satisfies $y_0(i) \ge 1$ for every $i$, hence $V_{\mathrm{ADR}}(d) \ge d$ — an exact **$\Omega(d)$ multiplicative ratio** $V_{\mathrm{ADR}}/V_{\mathrm{ARO}} \ge d$.
- **Segregated $|\cdot|$-lifted ADR exactness:** Because $\xi \mapsto (\xi^+, \xi^-)$ maps $B_1^d$ into the standard $2d$-simplex $\Delta_{2d}$ with vertices $\{0, \pm e_i\}$ mapped to simplex vertices, the coordinate-wise $|\cdot|$-lifted ADR $y(\xi) = y_0 + Y \xi + Z |\xi|$ is **exact for every fixed-recourse ARO problem $P$ in every dimension $d \ge 1$**, collapsing the $\Omega(d)$ ratio to $1$.

---

## 2. Refutation of `H-O2-1`: Why Coordinate-Separable Liftings Fail on $[-1, 1]^2$ (`O5`)

A natural conjecture (`H-O2-1`) is that coordinate-wise $|\cdot|$-lifted ADR (or axis-aligned piecewise-affine liftings with breakpoints along each coordinate $\xi_i$) should likewise close or shrink the ADR gap on the 2D box $[-1, 1]^2$ and on `BridgeFormalV2.Data`.

**Refutation:** For **any** coordinate-separable function $y(v_0, v_1) = y_0 + f_0(v_0) + f_1(v_1)$ (with completely arbitrary univariate functions $f_0, f_1 : \mathbb{R} \to \mathbb{R}^m$, not even continuous or piecewise-affine):
$$y(-1, 1) + y(1, -1) = (y_0 + f_0(-1) + f_1(1)) + (y_0 + f_0(1) + f_1(-1)) = y(-1, -1) + y(1, 1).$$
Thus **every** coordinate-separable policy satisfies the exact same square barycentric syzygy as an affine rule! Consequently, on both frozen `BridgeFormalV2.Data` witnesses:

| Witness (`BridgeFormalV2.Data`) | $V_{\mathrm{ARO}}$ | $V_{\mathrm{ADR}}$ | $V_{\mathrm{SegLADR}}$ ($|\xi_i|$) | $V_{\mathrm{Separable}}$ ($f_0+f_1$) | $V_{\mathrm{DiagLADR}}$ ($|\xi_0-\xi_1|$) |
|---|---:|---:|---:|---:|---:|
| `bridgeAdrGapData` (rank-1 $B$) | **6** | 8 | 8 | 8 | **6** (exact!) |
| `bridgeFullRankShearData` ($\det B = 1$) | **5** | 6 | 6 | 6 | **5** (exact!) |

---

## 3. Single-Feature Diagonal-Hinge Restoration (`O2 / O5`)

Adding the **single scalar cross-coordinate interaction feature** $\phi_{\mathrm{diag}}(v) = |v_0 - v_1|$ breaks the square syzygy ($|(-1)-1| + |1-(-1)| = 4 \ne 0 = |(-1)-(-1)| + |1-1|$). For **any** corner values $y_{--}, y_{-+}, y_{+-}, y_{++}$, setting
$$y_0 = \frac{y_{--} + y_{++}}{2}, \quad Y_0 = \frac{y_{++} - y_{--} + y_{+-} - y_{-+}}{4}, \quad Y_1 = \frac{y_{++} - y_{--} + y_{-+} - y_{+-}}{4}, \quad Z = \frac{y_{-+} + y_{+-} - y_{--} - y_{++}}{4}$$
gives $y(v_0, v_1) = y_0 + Y_0 v_0 + Y_1 v_1 + Z |v_0 - v_1|$, which coincides identically with the exact barycentric interpolation on the Kuhn triangulation $\{v_0 \le v_1\} \cup \{v_1 \le v_0\}$ of $[-1, 1]^2$. Notice that $Z$ is **literally $1/4$ of the square barycentric syzygy defect**. Hence a single diagonal-hinge feature makes lifted ADR **100% exact** for every fixed-recourse ARO on $[-1, 1]^2$ and every 2D rectangular-deviation `BridgeFormalV2.Data` instance.
