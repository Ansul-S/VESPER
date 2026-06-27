"""BAH2026 PS7 prototype — smoke test.

Runs the reused TRINETRA-X spine + the new physics-feature extractor over a
batch of *real conditioned* TESS light curves (data/processed/m1/*.npz) and
writes a feature table. Also renders one folded-light-curve figure for the
strongest-evidence star, to prove the end-to-end path works ahead of the finale.

Usage:  .venv/bin/python hackathon/prototype/smoke_test.py [N]
"""
from __future__ import annotations

import glob
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from features import extract_features, FEATURE_ORDER, _phase  # noqa: E402

HERE = os.path.dirname(__file__)
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "data", "processed", "m1"))
OUT = os.path.join(HERE, "out")
FIGS = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIGS, exist_ok=True)


def load(npz):
    d = np.load(npz, allow_pickle=True)
    return d["time"], d["resid"]


def main(n=60):
    files = sorted(glob.glob(os.path.join(DATA, "*.npz")))[:n]
    if not files:
        print(f"No conditioned light curves found in {DATA}")
        return
    rows = []
    for fp in files:
        tic = os.path.splitext(os.path.basename(fp))[0]
        time, resid = load(fp)
        try:
            feat = extract_features(time, resid)
        except Exception as e:                       # smoke test: keep going
            print(f"  {tic}: ERROR {e}")
            continue
        feat["tic"] = tic
        rows.append(feat)

    df = pd.DataFrame(rows).set_index("tic")
    cols = [c for c in FEATURE_ORDER if c in df.columns]
    df = df[cols]
    csv = os.path.join(OUT, "smoke_features.csv")
    df.to_csv(csv)

    n_ev = int(df["has_evidence"].sum())
    print(f"Processed {len(df)} light curves | {n_ev} with periodic evidence (>=2 events)")
    print(f"Feature table -> {csv}")
    with pd.option_context("display.width", 160, "display.max_columns", 20):
        show = df[df["has_evidence"] == 1].sort_values("total_snr", ascending=False)
        print("\nTop-10 by total SNR:")
        print(show.head(10).round(4).to_string())

    # --- figure for the strongest-evidence star ---
    cand = df[(df["has_evidence"] == 1) & df["period_days"].notna()]
    if not cand.empty:
        tic = cand.sort_values("total_snr", ascending=False).index[0]
        _plot_folded(tic, cand.loc[tic])


def _plot_folded(tic, feat):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    time, resid = load(os.path.join(DATA, f"{tic}.npz"))
    P = float(feat["period_days"])
    # re-derive t0 from the strongest event for a clean fold
    sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "research", "m3_calibration")))
    from detector import detect_events
    from features import DURATION_GRID, Z_EXTRACT
    ev = detect_events(np.asarray(time, float), np.asarray(resid, float),
                       DURATION_GRID, z_for_extraction=Z_EXTRACT)
    t0 = ev[int(np.argmax(ev[:, 1])), 0]
    ph = _phase(np.asarray(time, float), t0, P)
    order = np.argsort(ph)

    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(time, resid, ".", ms=1, alpha=0.4)
    ax[0].set(title=f"TIC {tic} — conditioned LC", xlabel="time (BTJD)", ylabel="resid flux")
    ax[1].plot(ph[order], resid[order], ".", ms=2, alpha=0.4)
    ax[1].axvline(0, color="r", lw=0.7, alpha=0.6)
    ax[1].set(title=f"folded @ P={P:.3f} d  (depth={feat['depth']:.4f}, "
                    f"SNR={feat['depth_snr']:.1f})", xlabel="phase", ylabel="resid flux")
    ax[1].invert_yaxis()
    fig.tight_layout()
    out = os.path.join(FIGS, f"folded_{tic}.png")
    fig.savefig(out, dpi=110)
    print(f"\nExample folded figure -> {out}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 60)
