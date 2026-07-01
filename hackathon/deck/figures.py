"""Generate deck figures: architecture diagram + 4-class concept sketch.

The architecture diagram uses clean orthogonal (elbow) connectors on a fixed
grid so every arrow enters its target box squarely on the box edge — no diagonal
or dangling connectors. Run:  .venv/bin/python hackathon/deck/figures.py
"""
from __future__ import annotations
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)

BLUE, RED, GREEN, GREY, PURPLE, GOLD = "#2c6fbb", "#c0392b", "#1e8449", "#566573", "#7d3c98", "#b9770e"
LINE = "#3b4a5a"


def _box(ax, cx, cy, w, h, text, fc, ec="0.25", fs=9, tc="white"):
    """Box centred at (cx, cy). Returns edge anchors for connectors."""
    x, y = cx - w / 2, cy - h / 2
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.06",
                                fc=fc, ec=ec, lw=1.3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, color=tc,
            weight="bold", linespacing=1.25)
    return {"top": (cx, cy + h / 2), "bottom": (cx, cy - h / 2), "cx": cx, "cy": cy}


def _seg(ax, pts, color=LINE, lw=1.7):
    """Plain poly-line through pts (orthogonal elbows)."""
    xs, ys = zip(*pts)
    ax.add_line(plt.Line2D(xs, ys, color=color, lw=lw, solid_capstyle="round",
                           solid_joinstyle="round", zorder=1))


def _arrow(ax, x1, y1, x2, y2, color=LINE, lw=1.7):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=15, lw=lw, color=color, zorder=2,
                                 shrinkA=0, shrinkB=0))


def architecture():
    fig, ax = plt.subplots(figsize=(11.6, 6.5))
    fig.patch.set_facecolor("white")
    ax.set_xlim(0, 12); ax.set_ylim(0, 7.5); ax.axis("off")
    ax.text(6, 7.15, "VESPER — Hybrid Detection & Classification Pipeline",
            ha="center", fontsize=15, weight="bold", color="#13294b")

    # --- boxes (all centred; grid-aligned) ---
    fe = _box(ax, 6.0, 6.35, 11.4, 0.82,
              "Front-end  (reused VESPER spine)\n"
              "conditioning (detrend + noise model)  →  dip detection  →  "
              "period-from-spacing (bootstrap FAP)  →  phase-fold",
              BLUE, fs=8.6)
    phys = _box(ax, 3.0, 4.55, 4.7, 1.25,
                "PHYSICS BRANCH\nfeatures: depth, duration, odd–even,\n"
                "secondary, V/U-shape, centroid/dilution\n→ GBT / Random Forest", GREEN, fs=8.7)
    deep = _box(ax, 9.0, 4.55, 4.7, 1.25,
                "DEEP BRANCH\nCNN on global + local\nphase-folded views\n(morphology)", PURPLE, fs=8.7)
    ens = _box(ax, 6.0, 3.05, 5.0, 0.72, "ENSEMBLE   (stacking / weighted)", GREY, fs=9.4)
    cal = _box(ax, 6.0, 1.95, 6.6, 0.72,
               "CONFORMAL CALIBRATION  →  class + confidence (+ abstain)", GOLD, fs=9.4)
    o1 = _box(ax, 2.1, 0.78, 3.2, 0.74, "transit / eclipse /\nblend / other", RED, fs=8.7)
    o2 = _box(ax, 6.0, 0.78, 3.2, 0.74, "SNR / significance\n(LR confirm gate)", RED, fs=8.7)
    o3 = _box(ax, 9.9, 0.78, 3.2, 0.74, "period · depth · duration\n+ uncertainties", RED, fs=8.7)

    # --- connectors (orthogonal; square box entries) ---
    # front-end -> two branches (fan-out via a horizontal bus)
    yb1 = 5.55
    _seg(ax, [fe["bottom"], (6.0, yb1)])
    _seg(ax, [(phys["cx"], yb1), (deep["cx"], yb1)])
    _arrow(ax, phys["cx"], yb1, *phys["top"])
    _arrow(ax, deep["cx"], yb1, *deep["top"])

    # two branches -> ensemble (fan-in via a horizontal bus)
    yb2 = 3.72
    _seg(ax, [phys["bottom"], (phys["cx"], yb2)])
    _seg(ax, [deep["bottom"], (deep["cx"], yb2)])
    _seg(ax, [(phys["cx"], yb2), (deep["cx"], yb2)])
    _arrow(ax, 6.0, yb2, *ens["top"])

    # ensemble -> calibration
    _arrow(ax, *ens["bottom"], *cal["top"])

    # calibration -> three outputs (fan-out via a horizontal bus)
    yb3 = 1.42
    _seg(ax, [cal["bottom"], (6.0, yb3)])
    _seg(ax, [(o1["cx"], yb3), (o3["cx"], yb3)])
    for o in (o1, o2, o3):
        _arrow(ax, o["cx"], yb3, *o["top"])

    p = os.path.join(OUT, "arch_diagram.png")
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    return p


def process_flow():
    """PS7 five-step methodology as a clean left-to-right flow with square arrows."""
    steps = [("01", "Detrend", "wotan biweight\n→ flat light curve", BLUE),
             ("02", "Identify", "dip detection +\nperiod, phase-fold", BLUE),
             ("03", "Characterize", "trapezoid fit:\ndepth, duration,\ningress, flat-bottom", GREEN),
             ("04", "Classify", "shape params →\ntransit / eclipse /\nblend / other", GOLD),
             ("05", "Significance", "SNR +\nformal significance", GREY)]
    fig, ax = plt.subplots(figsize=(12.6, 3.3)); fig.patch.set_facecolor("white")
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 4); ax.axis("off")
    w, h, y = 2.05, 1.85, 2.5
    xs = [1.28 + i * 2.5 for i in range(5)]
    for i, (num, name, sub, col) in enumerate(steps):
        cx = xs[i]
        ax.add_patch(FancyBboxPatch((cx - w / 2, y - h / 2), w, h,
                                    boxstyle="round,pad=0.02,rounding_size=0.06",
                                    fc=col, ec="0.25", lw=1.3))
        ax.text(cx, y + h / 2 - 0.34, f"{num} · {name}", ha="center", va="center",
                fontsize=11, weight="bold", color="white")
        ax.text(cx, y - 0.18, sub, ha="center", va="center", fontsize=8.7,
                color="white", linespacing=1.3)
        if i < 4:
            _arrow(ax, cx + w / 2, y, xs[i + 1] - w / 2, y)
    ax.text(6.3, 0.72,
            "Steps 01–02 reuse the validated VESPER spine (benchmarked vs full TLS).   "
            "Step 03 shape-fit feeds Step 04 —",
            ha="center", fontsize=9.6, color="#13294b")
    ax.text(6.3, 0.36, "the committee's stated approach: “build the AI classifier on the transit shape parameters.”",
            ha="center", fontsize=9.6, color="#2c6fbb", weight="bold")
    p = os.path.join(OUT, "process_flow.png")
    fig.savefig(p, dpi=200, bbox_inches="tight", facecolor="white"); plt.close(fig)
    return p


def _lc(ax, kind):
    rng = np.random.default_rng(3)
    ph = np.linspace(-0.5, 0.5, 600)
    y = np.zeros_like(ph)
    if kind == "transit":
        m = np.abs(ph) < 0.05
        y[m] = -0.03 * np.sqrt(np.clip(1 - (ph[m] / 0.05) ** 2, 0, 1))  # U-shape (flat-ish bottom)
        title, sub, c = "TRANSIT (planet)", "shallow • U-shape • no secondary", GREEN
    elif kind == "eclipse":
        m = np.abs(ph) < 0.06
        y[m] = -0.13 * (1 - np.abs(ph[m]) / 0.06)                       # V-shape, deep
        ms = (np.abs(ph - 0.5) < 0.035) | (np.abs(ph + 0.5) < 0.035)
        y[ms] = -0.045                                                  # secondary eclipse
        title, sub, c = "ECLIPSE (binary)", "deep • V-shape • secondary • odd–even", RED
    elif kind == "blend":
        m = np.abs(ph) < 0.05
        y[m] = -0.055 * (1 - np.abs(ph[m]) / 0.05)                      # V-ish, diluted
        title, sub, c = "BLEND", "diluted depth • centroid shift • high contam.", PURPLE
    else:
        y = 0.028 * np.sin(2 * np.pi * 2.5 * ph)                        # quasi-sinusoidal
        title, sub, c = "OTHER (spots / sys.)", "quasi-periodic • no transit shape", GREY
    y = y + rng.normal(0, 0.004, ph.size)
    ax.plot(ph, y, ".", ms=1.5, alpha=0.5, color=c)
    ax.set_title(title, fontsize=11, weight="bold", color=c)
    ax.text(0.5, -0.2, sub, transform=ax.transAxes, ha="center", fontsize=8.5, color="0.25")
    ax.set_ylim(-0.17, 0.05); ax.set_xticks([]); ax.set_yticks([])
    ax.set_ylabel("flux", fontsize=8)
    for s in ax.spines.values(): s.set_color("0.7")


def four_class():
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    fig.patch.set_facecolor("white")
    for ax, k in zip(axs.ravel(), ["transit", "eclipse", "blend", "other"]):
        _lc(ax, k)
    fig.suptitle("Four signal classes — distinct physical signatures the classifier separates",
                 fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = os.path.join(OUT, "four_class_concept.png"); fig.savefig(p, dpi=150, facecolor="white"); plt.close(fig)
    return p


if __name__ == "__main__":
    print("saved", architecture())
    print("saved", four_class())
    print("saved", process_flow())
