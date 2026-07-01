"""BAH2026 PS7 — failure analysis: why transit <-> blend is the residual confusion.

The confusion matrix's only error is shallow transit <-> blend. This shows WHY:
injected on the SAME real TESS host + noise, a shallow planet (U, no secondary)
and a diluted blended EB (V + faint secondary/odd-even) are nearly identical from
the light curve alone. The distinguishing tells are sub-noise at this depth ->
motivates pixel-level centroid / difference-imaging features (Round-2).

Run:  .venv/bin/python hackathon/prototype/failure_analysis.py
Out:  figs/failure_case.png
"""
from __future__ import annotations
import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
from make_labeled_set import _transit, _vshape, _time_grids  # reuse the exact injectors
import _deckstyle as ds

HERE = os.path.dirname(__file__)
FIGS = os.path.join(HERE, "figs")


def _fold_bin(t, y, P, t0, win=0.06, nb=45):
    ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
    m = np.abs(ph) <= win
    ph, y = ph[m], y[m]
    b = np.linspace(-win, win, nb + 1)
    idx = np.digitize(ph, b) - 1
    xb, yb = [], []
    for k in range(nb):
        s = idx == k
        if s.sum() >= 3:
            xb.append(0.5 * (b[k] + b[k + 1])); yb.append(np.median(y[s]))
    return ph, y, np.array(xb), np.array(yb)


def main():
    ds.apply()
    grids = _time_grids(60)
    host, t, rms = grids[12]                 # one real host (deterministic)
    rng = np.random.default_rng(42)
    P, dur, depth = 5.3, 0.12, 0.0016        # shallow (~160 ppm) — planet-scale
    t0 = t.min() + 1.7
    noise = rng.normal(0, rms, t.size)       # SAME noise realisation for both

    # planet: U-shape, no secondary, no odd-even
    tr = _transit(t, t0, P, depth, dur) + noise
    # blended EB: diluted V-shape at the SAME depth, with faint odd-even + secondary
    bl = _vshape(t, t0, P, depth, dur)
    cyc = np.round((t - t0) / P).astype(int); bl[cyc % 2 == 1] *= 0.7
    ph_all = ((t - t0) / P) % 1.0
    bl[np.abs(ph_all - 0.5) < (dur / 2 / P)] += -depth * 0.4
    bl = bl + noise

    pht, rawt, xt, yt = _fold_bin(t, tr, P, t0)
    phb, rawb, xb, yb = _fold_bin(t, bl, P, t0)

    fig, ax = plt.subplots(figsize=(9.6, 4.8))
    ax.scatter(pht, rawt * 1e6, s=4, c="0.82", alpha=0.16, zorder=1)
    ax.scatter(phb, rawb * 1e6, s=4, c="0.82", alpha=0.16, zorder=1)
    ax.scatter(xt, yt * 1e6, s=40, c=ds.GREEN, edgecolor="white", lw=0.5, zorder=3,
               label="planet — U-shape, no secondary")
    ax.scatter(xb, yb * 1e6, s=40, c="#7d3c98", marker="s", edgecolor="white", lw=0.5, zorder=3,
               label="blended EB — V-shape, faint secondary/odd-even")
    ax.axhline(0, color="0.75", lw=0.9, zorder=0)
    ax.set_ylim(-depth * 1e6 * 1.7, depth * 1e6 * 1.15)   # dip points DOWN (matches PoC)
    ax.set_xlim(-0.06, 0.06)
    ax.set_xlabel("orbital phase"); ax.set_ylabel("relative flux (ppm)")
    ax.set_title("Why transit ↔ blend is the residual confusion")
    ax.legend(loc="lower right", fontsize=8.5)
    ax.text(0.02, 0.05,
            f"same real host (TIC {host}) + same noise · depth ≈ {depth*1e6:.0f} ppm\n"
            "the distinguishing tells (secondary, odd–even, ingress) are sub-noise\n"
            "at planet depth → needs pixel-level centroid / difference imaging (Round-2)",
            transform=ax.transAxes, fontsize=8.4, va="bottom",
            bbox=dict(boxstyle="round,pad=0.4", fc="#eef4fb", ec=ds.BLUE, lw=1.0))
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    ds.synthetic_banner(fig)
    p = os.path.join(FIGS, "failure_case.png"); fig.savefig(p); plt.close(fig)
    print("saved", p)


if __name__ == "__main__":
    main()
