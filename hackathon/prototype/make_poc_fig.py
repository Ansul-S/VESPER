"""Regenerate the headline proof-of-concept figure: eb_vs_planet.png.

Fresh-MAST demonstration that the reused VESPER spine blindly recovers a real
planet (Pi Mensae c) and flags a real eclipsing binary (TIC 100029948) by
physics — the depth-is-equal / SHAPE-separates story (committee step 03).

Rebuilt cleanly so every plotted point stays inside the axes: robust y-limits
from the folded data and marker-only overlays (no cross-gap connecting line that
can shoot outside the frame). Same cached data + same recovered parameters as the
original; nothing scientific changed.

Run:  .venv/bin/python hackathon/prototype/make_poc_fig.py
Out:  hackathon/prototype/figs/eb_vs_planet.png
"""
from __future__ import annotations
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "research", "m3_calibration")))
from detector import detect_events  # noqa: E402
from features import DURATION_GRID, Z_EXTRACT  # noqa: E402

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "cache")
FIGS = os.path.join(HERE, "figs")
os.makedirs(FIGS, exist_ok=True)
WIN = 0.10  # phase half-window shown


def load(tic):
    d = np.load(os.path.join(CACHE, f"{tic}.npz"))
    return d["time"].astype(float), d["resid"].astype(float)


def fold(t, r, P, t0):
    ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
    return ph, r


def bin_phase(ph, y, nb=60, lo=-WIN, hi=WIN):
    b = np.linspace(lo, hi, nb + 1)
    idx = np.digitize(ph, b) - 1
    xm, ym = [], []
    for k in range(nb):
        s = idx == k
        if s.sum() >= 3:
            xm.append(0.5 * (b[k] + b[k + 1]))
            ym.append(np.median(y[s]))
    return np.array(xm), np.array(ym)


def panel(ax, ph, y, color, title, note, ylabel):
    """Robustly bounded phase-folded panel; dip points downward, nothing clips."""
    m = np.abs(ph) <= WIN
    phw, yw = ph[m], y[m]
    xb, yb = bin_phase(phw, yw)

    # y-limits from the binned curve (the signal) with padding; this frames the
    # transit/eclipse and guarantees every marker sits inside the axes.
    ref = yb if yb.size else yw
    lo, hi = np.nanmin(ref), np.nanmax(ref)
    span = max(hi - lo, 1e-9)
    ylo, yhi = lo - 0.30 * span, hi + 0.30 * span

    ax.axhline(0.0, color="0.8", lw=0.8, zorder=0)
    ax.scatter(phw, np.clip(yw, ylo, yhi), s=3, c="0.72", alpha=0.30, zorder=1,
               edgecolor="none", rasterized=True)
    ax.scatter(xb, yb, s=20, c=color, zorder=3, edgecolor="white", linewidth=0.4, clip_on=True)
    ax.set_xlim(-WIN, WIN)
    ax.set_ylim(ylo, yhi)  # dip points downward (intuitive: transit = flux drop)
    ax.set_xlabel("orbital phase", fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.set_title(title, fontsize=11, weight="bold", color="#13294b")
    ax.text(0.03, 0.05, note, transform=ax.transAxes, fontsize=8.6, va="bottom", ha="left",
            bbox=dict(boxstyle="round,pad=0.4", fc="#eaf2ff", ec=color, lw=1.1))
    for s in ax.spines.values():
        s.set_color("0.55")


def main():
    fig, axs = plt.subplots(1, 2, figsize=(12.5, 5.2))
    fig.patch.set_facecolor("white")

    # --- LEFT: eclipsing binary, TIC 100029948 (deep V) ---
    t, r = load(100029948)
    P_eb = 1.386633
    ev = detect_events(t, r, DURATION_GRID, z_for_extraction=Z_EXTRACT)
    t0 = ev[int(np.argmax(ev[:, 1])), 0]
    ph, y = fold(t, r, P_eb, t0)
    panel(axs[0], ph, y * 100.0, "#c0392b",
          "TIC 100029948 — ECLIPSING BINARY\nblindly recovered  P = 1.387 d",
          "depth ~25%  •  V-shape\nodd–even diff 0.23  →  STELLAR",
          "relative flux (%)")

    # --- RIGHT: Pi Mensae c, TIC 261136679 (shallow U) ---
    t, r = load(261136679)
    tl = np.load(os.path.join(CACHE, "_pimen_tls.npz"))
    ph, y = fold(t, r, float(tl["period"]), float(tl["T0"]))
    panel(axs[1], ph, y * 1e6, "#2c6fbb",
          "TIC 261136679 — Pi Mensae c (PLANET)\nblindly recovered by TLS  P = 6.262 d  SDE = 12.3",
          "depth ~289 ppm  •  U-shape\nshallow  →  PLANET-SCALE",
          "relative flux (ppm)")

    fig.suptitle("Transit vs Eclipse — fresh MAST data → conditioning → recovery → physics discrimination (PS7)",
                 fontsize=12.5, weight="bold", color="#13294b")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out = os.path.join(FIGS, "eb_vs_planet.png")
    fig.savefig(out, dpi=150, facecolor="white")
    plt.close(fig)
    print("saved", out)


if __name__ == "__main__":
    main()
