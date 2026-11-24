#!/usr/bin/env python3
"""Figures for the essay v2 (2026-10-20).

Data figures use ONLY the exact per-path LP oracle
(`judges/numerical/bridge.py: ladder_value`, rational arithmetic) at T=5,
where every one of the 32 schedules is affordable. Schematic figures
(1, 2, 5) carry no data. The S2 closed form is checked against the same
LP points and the check is printed, not assumed.
"""
from __future__ import annotations
import itertools, sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "judges" / "numerical"))
sys.path.insert(0, str(ROOT / "src"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = Path(__file__).resolve().parent
plt.rcParams.update({"font.size": 8.6, "axes.titlesize": 9.4, "axes.labelsize": 8.6,
                     "legend.fontsize": 7.6, "figure.dpi": 220,
                     "axes.spines.top": False, "axes.spines.right": False})

from bridge import BridgeInstance, ladder_value

E1, E2, D0, UB, T = F(3, 2), F(1, 2), F(0), F(1), 5
S, D = E1 + E2, E1 - E2

def inst():
    return BridgeInstance(bid="essay", nx=2, A=((F(1), F(0)), (F(0), F(1))),
        B=((F(1),), (F(1),)), E=((E1,), (E2,)), x0=(D0, D0),
        T=T, w_set=(F(-1), F(1)), u_bound=UB)

I = inst()
VAL = {}
for k in range(T + 1):
    for s in itertools.combinations(range(1, T + 1), k):
        R = frozenset(s)
        VAL[R] = ladder_value(I, R)

# ---------------------------------------------------------------- Fig 1: map
fig, ax = plt.subplots(figsize=(6.4, 2.9))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
def box(x, y, w, h, title, body, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.18",
                                fc=fc, ec="#333333", lw=0.8))
    ax.text(x + w/2, y + h - 0.32, title, ha="center", va="top", fontsize=8.8, fontweight="bold")
    ax.text(x + w/2, y + h - 0.95, body, ha="center", va="top", fontsize=7.2, linespacing=1.4)
box(0.15, 2.9, 3.0, 1.85, "Two-stage ARO",
    "min c·x + max$_{\\xi\\in\\Xi}$ min$_y$ d·y\nA(ξ)x + By ≥ h(ξ), y ≥ 0\npolicy class: y(·) restricted", "#e8eef8")
box(0.15, 0.25, 3.0, 1.85, "Guaranteed control (Dmitruk)",
    "x(t+1)=Ax+Bu+Mw, |u|≤u$_b$\ncost: worst-case $\\|x_T\\|_1$\nclosures R ⊆ {1..T}", "#f7ece6")
box(6.55, 1.55, 3.3, 1.95, "Bridge class",
    "A=I, B=(1,1)$^\\top$, E=(e$_1$,e$_2$)\nx$_0$=(d$_0$,d$_0$), w∈{−1,+1}$^T$\nclosed form V(R); 2D rotation", "#eaf3ea")
ax.annotate("", xy=(6.5, 2.5), xytext=(3.2, 1.15),
            arrowprops=dict(arrowstyle="->", lw=1.0, color="#555555", connectionstyle="arc3,rad=-0.25"))
ax.annotate("", xy=(6.5, 2.6), xytext=(3.2, 3.85),
            arrowprops=dict(arrowstyle="->", lw=1.0, color="#555555", connectionstyle="arc3,rad=0.25"))
ax.text(4.85, 0.95, "fixed recourse,\nRHS uncertainty", fontsize=7, ha="center", color="#444444")
ax.text(4.85, 4.4, "information structure\nR = policy information", fontsize=7, ha="center", color="#444444")
fig.tight_layout(); fig.savefig(OUT / "fig1_map.pdf"); plt.close(fig)

# ------------------------------------------------------- Fig 2: the wedge
fig, ax = plt.subplots(figsize=(4.4, 3.2))
ax.fill_between([0, 1], 0, 2.0, color="#e8eef8")
ax.fill_between([1, 4], 0, 1.0, color="#f4d6d0")
ax.axvline(1.0, color="#333333", lw=0.8, ls="--")
ax.axhline(1.0, color="#333333", lw=0.8, ls="--")
ax.set_xlim(0, 4); ax.set_ylim(0, 2.0)
ax.set_xlabel(r"$x=|S|/(2u_b)$"); ax.set_ylabel(r"$y=2|d_0|/(2u_b)$")
ax.set_title(r"Wedge $\mathcal{K}$ where the earlier form fails ($T\geq 2$)")
ax.text(0.45, 1.72, "earlier form\nexact", ha="center", fontsize=8)
ax.text(2.5, 0.45, "pursuit iteration\n$f_1^{\\,T}(2|d_0|)$", ha="center", fontsize=8)
fig.tight_layout(); fig.savefig(OUT / "fig2_wedge.pdf"); plt.close(fig)

# --------------------------------------------- Fig 3: one closure, two regimes
def cval(S): return max(2*abs(D0) + (abs(S)-2*UB)*T, abs(D)*T)
def gg(S, r): return max(abs(S)*(T-r), abs(S)*T - 2*UB*(T-r))

rs = list(range(1, T))
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=False)

# left: D = 0 (symmetric rows) -> law holds
I_sym = BridgeInstance(bid="sym", nx=2, A=((F(1), F(0)), (F(0), F(1))),
    B=((F(1),), (F(1),)), E=((F(1),), (F(1),)), x0=(D0, D0),
    T=T, w_set=(F(-1), F(1)), u_bound=UB)
S_sym, D_sym = F(2), F(0)
lp_s = [float(ladder_value(I_sym, frozenset({r}))) for r in rs]
cf_s = [float(max(cval(S_sym), gg(S_sym, r))) for r in rs]
ax = axes[0]
ax.plot(rs, cf_s, color="#3b5b9a", lw=1.1, label="S2 closed form")
ax.plot(rs, lp_s, "o", ms=3.6, color="#b23a2e", label="exact LP")
plat = [r for r in rs if gg(S_sym, r) <= cval(S_sym)]
if plat: ax.axvspan(min(plat)-0.3, max(plat)+0.3, color="#e8eef8", alpha=0.9)
ax.set_title(r"$e=(1,1)$: $D=0$, law holds")
ax.set_xlabel(r"closure moment $r$"); ax.set_ylabel(r"$V(\{r\})$")
ax.legend(frameon=False, loc="upper center")

# right: D != 0 -> law fails
ax = axes[1]
cf_asym = [float(max(cval(S), gg(S, r))) for r in rs]
lp_asym = [float(VAL[frozenset({r})]) for r in rs]
ax.plot(rs, cf_asym, color="#3b5b9a", lw=1.1, label="S2 closed form")
ax.plot(rs, lp_asym, "o", ms=3.6, color="#b23a2e", label="exact LP")
ax.set_title(r"$e=(3/2,1/2)$: $D=1$, law fails")
ax.set_xlabel(r"closure moment $r$")
ax.legend(frameon=False, loc="upper center")
fig.suptitle(f"One closure, $T={T}$, $u_b=1$, $d_0=0$", fontsize=9.4, y=1.0)
fig.tight_layout(); fig.savefig(OUT / "fig3_valley.pdf"); plt.close(fig)

# ------------------------------- Fig 4: value vs number and position of closures
ks, lo, hi = [], [], []
for k in range(T + 1):
    vs = [float(VAL[R]) for R in VAL if len(R) == k]
    ks.append(k); lo.append(min(vs)); hi.append(max(vs))
fig, ax = plt.subplots(figsize=(4.8, 3.0))
ax.fill_between(ks, lo, hi, color="#e8eef8", label="range over all schedules of size $k$")
ax.plot(ks, lo, "-o", ms=3.2, color="#3b5b9a", label="best schedule")
ax.plot(ks, hi, "--", lw=0.9, color="#777777", label="worst schedule")
ax.set_xlabel(r"number of closures $k=|R|$"); ax.set_ylabel(r"$V(R)$")
ax.set_title(r"Schedule matters at fixed $k$ (exact LP, $T=5$)")
ax.legend(frameon=False, loc="upper right")
fig.tight_layout(); fig.savefig(OUT / "fig4_ladder.pdf"); plt.close(fig)

# ------------------------------------------------------ Fig 5: quantifier order
fig, ax = plt.subplots(figsize=(6.0, 2.3))
ax.set_xlim(0, 10); ax.set_ylim(0, 3.4); ax.axis("off")
def node(x, y, label, fc):
    ax.add_patch(FancyBboxPatch((x-0.44, y-0.24), 0.88, 0.48,
                                boxstyle="round,pad=0.04,rounding_size=0.1", fc=fc, ec="#444", lw=0.7))
    ax.text(x, y, label, ha="center", va="center", fontsize=8.2)
seq_top = [("min u", "#e8eef8"), ("max w", "#f4e2dd"), ("min u", "#e8eef8"), ("max w", "#f4e2dd")]
for i, (lbl, col) in enumerate(seq_top):
    x = 1.0 + i*1.25; node(x, 2.35, lbl, col)
    if i: ax.annotate("", xy=(x-0.60, 2.35), xytext=(x-0.98, 2.35),
                      arrowprops=dict(arrowstyle="->", lw=0.8, color="#555"))
ax.text(0.1, 3.05, r"$V_0(x_0)$: alternating min max (multiclosure, RO ladder)", ha="left", fontsize=7.6)
seq_bot = [("min u", "#e8eef8"), ("max w", "#f4e2dd"), ("max w", "#f4e2dd"), ("max w", "#f4e2dd")]
for i, (lbl, col) in enumerate(seq_bot):
    x = 5.9 + i*1.25; node(x, 0.85, lbl, col)
    if i: ax.annotate("", xy=(x-0.60, 0.85), xytext=(x-0.98, 0.85),
                      arrowprops=dict(arrowstyle="->", lw=0.8, color="#555"))
ax.text(5.0, 0.25, r"$J(x_0)$: one min, then every max (guaranteeing program)", ha="left", fontsize=7.6)
ax.annotate("", xy=(7.8, 1.32), xytext=(7.8, 1.98),
            arrowprops=dict(arrowstyle="->", lw=1.1, color="#b23a2e"))
ax.text(7.95, 1.62, r"$V_0(x_0) \leq J(x_0)$", fontsize=8, color="#b23a2e", ha="left", va="center")
fig.tight_layout(); fig.savefig(OUT / "fig5_quantifier.pdf"); plt.close(fig)

# ----------------------------------------------------------------- checks
print("T =", T, "S =", S, "D =", D, "schedules:", len(VAL))
print("V(empty) =", float(VAL[frozenset()]), " V(full) =", float(VAL[frozenset(range(1, T+1))]))
mism_s = sum(1 for a,b in zip(lp_s,cf_s) if abs(a-b)>1e-9)
mism_a = sum(1 for a,b in zip(lp_asym,cf_asym) if abs(a-b)>1e-9)
print("S2 vs LP one-closure mismatches: symmetric", mism_s, "/", len(rs), "| asymmetric", mism_a, "/", len(rs))
print("k -> (min, max):", [(k, round(a, 2), round(b, 2)) for k, a, b in zip(ks, lo, hi)])
