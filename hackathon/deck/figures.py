"""Generate deck figures: architecture diagram + 4-class concept sketch."""
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

BLUE, RED, GREEN, GREY, PURPLE = "#2c6fbb", "#c0392b", "#1e8449", "#566573", "#7d3c98"


def _box(ax, x, y, w, h, text, fc, ec="0.3", fs=9, tc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            color=tc, weight="bold", wrap=True)


def _arrow(ax, x1, y1, x2, y2, color="0.3"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=14, lw=1.4, color=color))


def architecture():
    fig, ax = plt.subplots(figsize=(11, 6.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    ax.text(6, 6.7, "TRINETRA — Hybrid Detection & Classification Pipeline",
            ha="center", fontsize=14, weight="bold")

    # front-end (reused spine)
    _box(ax, 0.3, 5.3, 11.4, 0.8,
         "Front-end (reused TRINETRA-X spine)\n"
         "conditioning (detrend + noise model) → dip detection → period-from-spacing (bootstrap FAP) → phase-fold",
         BLUE, fs=8.2)
    _arrow(ax, 6, 5.3, 6, 4.95)

    # two branches
    _box(ax, 0.8, 3.5, 4.4, 1.25,
         "PHYSICS BRANCH\nfeatures: depth, duration, odd–even,\nsecondary, V/U-shape, centroid/dilution\n→ GBT / Random Forest", GREEN, fs=8.5)
    _box(ax, 6.8, 3.5, 4.4, 1.25,
         "DEEP BRANCH\nCNN on global + local\nphase-folded views\n(morphology)", PURPLE, fs=8.5)
    _arrow(ax, 3.0, 4.95, 3.0, 4.75); _arrow(ax, 9.0, 4.95, 9.0, 4.75)

    # ensemble
    _box(ax, 3.6, 2.35, 4.8, 0.75, "ENSEMBLE  (stacking / weighted)", GREY, fs=9)
    _arrow(ax, 3.0, 3.5, 5.0, 3.1); _arrow(ax, 9.0, 3.5, 7.0, 3.1)
    _arrow(ax, 6, 2.35, 6, 2.05)

    # calibration
    _box(ax, 3.0, 1.25, 6.0, 0.75,
         "CONFORMAL CALIBRATION → class + confidence (+ abstain)", "#b9770e", fs=9)
    _arrow(ax, 6, 1.25, 6, 0.95)

    # outputs
    _box(ax, 0.6, 0.15, 3.3, 0.75, "transit / eclipse /\nblend / other", RED, fs=8.5)
    _box(ax, 4.35, 0.15, 3.3, 0.75, "SNR / significance\n(LR confirm gate)", RED, fs=8.5)
    _box(ax, 8.1, 0.15, 3.3, 0.75, "period · depth · duration\n+ uncertainties", RED, fs=8.5)
    for cx in (2.25, 6.0, 9.75):
        _arrow(ax, cx, 1.25, cx, 0.9)

    fig.tight_layout()
    p = os.path.join(OUT, "arch_diagram.png"); fig.savefig(p, dpi=130); plt.close(fig)
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
    for ax, k in zip(axs.ravel(), ["transit", "eclipse", "blend", "other"]):
        _lc(ax, k)
    fig.suptitle("Four signal classes — distinct physical signatures the classifier separates",
                 fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    p = os.path.join(OUT, "four_class_concept.png"); fig.savefig(p, dpi=130); plt.close(fig)
    return p


if __name__ == "__main__":
    print("saved", architecture())
    print("saved", four_class())
