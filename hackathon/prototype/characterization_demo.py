"""Reproduce the committee's step-03 characterization (slides 5/6) on REAL data.

Fits the trapezoid shape to the folded EB (TIC 100029948) and the planet
(Pi Mensae c) and renders a light-curve + best-fit + parameter panel for each,
demonstrating the U-vs-V shape discrimination the committee emphasized.
"""
from __future__ import annotations
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "research", "m3_calibration")))
from shape_fit import fit_trapezoid, trapezoid, fold_to_hours, binned  # noqa: E402
from detector import detect_events  # noqa: E402
from features import DURATION_GRID, Z_EXTRACT  # noqa: E402

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "cache"); FIGS = os.path.join(HERE, "figs")


def load(tic):
    d = np.load(os.path.join(CACHE, f"{tic}.npz")); return d["time"].astype(float), d["resid"].astype(float)


def panel(ax_lc, ax_tx, t_h, flux, fit, title, color, window_h):
    xb, yb = binned(t_h, flux, nb=70)
    ax_lc.plot(t_h, flux, ".", ms=1.5, alpha=0.12, color="0.6")
    ax_lc.plot(xb, yb, "o", ms=3, color=color, label="binned data")
    if fit:
        tt = np.linspace(-window_h, window_h, 600)
        ax_lc.plot(tt, trapezoid(tt, fit["baseline_flux"], fit["depth"], 0.0,
                                 fit["t_total_h"], fit["t_ingress_h"]),
                   "-", color="#c0392b", lw=2, label="best-fit trapezoid")
        for s in (-1, 1):
            ax_lc.axvline(s * fit["t_total_h"] / 2, ls=":", color="#b9770e", lw=1)
            ax_lc.axvline(s * fit["t_flat_h"] / 2, ls=":", color="0.4", lw=1)
    ax_lc.set(title=title, xlabel="time from mid-transit (h)", ylabel="normalized flux",
              xlim=(-window_h, window_h))
    ax_lc.legend(fontsize=7, loc="lower right")

    ax_tx.axis("off")
    if not fit:
        ax_tx.text(0.5, 0.5, "fit failed", ha="center"); return
    lines = [("Estimated Parameters", ""),
             ("Baseline flux", f"{fit['baseline_flux']:.6f}"),
             ("Transit depth", f"{fit['depth']*100:.3f}%  ({fit['depth_ppm']:.0f} ppm)"),
             ("Total duration", f"{fit['t_total_h']:.3f} h"),
             ("Ingress/egress", f"{fit['t_ingress_h']:.3f} h"),
             ("Flat-bottom", f"{fit['t_flat_h']:.3f} h"),
             ("Flat fraction", f"{fit['flat_frac']:.2f}"),
             ("", ""),
             ("Shape verdict", fit["shape_verdict"])]
    y = 0.95
    for k, v in lines:
        if k == "Estimated Parameters":
            ax_tx.text(0.0, y, k, fontsize=12, weight="bold", color="#13294b")
        elif k == "Shape verdict":
            ax_tx.text(0.0, y, f"{k}:", fontsize=10, color="0.3")
            ax_tx.text(0.0, y - 0.06, v, fontsize=11, weight="bold",
                       color="#1e8449" if "planet" in v else "#c0392b")
        elif k:
            ax_tx.text(0.0, y, k, fontsize=10, color="0.3")
            ax_tx.text(0.55, y, v, fontsize=11, weight="bold", color="#111")
        y -= 0.10


def main():
    fig, axs = plt.subplots(2, 2, figsize=(13, 8),
                            gridspec_kw={"width_ratios": [2.4, 1]})

    # EB (real, deep V)
    t, r = load(100029948); P = 1.386633
    ev = detect_events(t, r, DURATION_GRID, z_for_extraction=Z_EXTRACT)
    t0 = ev[int(np.argmax(ev[:, 1])), 0]
    th, fx = fold_to_hours(t, r, P, t0, window_h=6)
    xb, yb = binned(th, fx, 70)
    fit = fit_trapezoid(xb, yb)
    panel(axs[0, 0], axs[0, 1], th, fx, fit, "TIC 100029948 — eclipsing binary (real)", "#c0392b", 6)

    # Pi Men c (real, shallow U)
    t, r = load(261136679); tl = np.load(os.path.join(CACHE, "_pimen_tls.npz"))
    th, fx = fold_to_hours(t, r, float(tl["period"]), float(tl["T0"]), window_h=8)
    xb, yb = binned(th, fx, 60)
    fit = fit_trapezoid(xb, yb)
    panel(axs[1, 0], axs[1, 1], th, fx, fit, "Pi Mensae c — planet (real)", "#2c6fbb", 8)

    fig.suptitle("Step 03 — Characterization by trapezoid shape fit (depth is equal; SHAPE separates planet from EB)",
                 fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = os.path.join(FIGS, "characterization.png"); fig.savefig(out, dpi=120)
    print("saved", out)


if __name__ == "__main__":
    main()
