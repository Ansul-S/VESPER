"""BAH2026 PS7 prototype — build a SYNTHETIC labeled training set by injection.

Until the organizer's curated labels arrive, we generate physically-motivated
examples of the four classes by injecting signals onto realistic TESS noise
(real cadence/gaps from cached conditioned LCs, noise at each LC's measured rms),
then run the SAME feature extractor used at inference. This validates the
trained-classifier path end-to-end.

Class designs (the discriminators the classifier must learn):
  transit : shallow batman transit, U-shape, NO secondary, NO odd-even
  eclipse : DEEP batman transit + secondary eclipse + odd-even depth alternation
  blend   : DILUTED eclipse — shallow depth BUT retains secondary / odd-even tells
  other   : sinusoidal (spot/pulsation) variability, no box-shaped dip

Usage: .venv/bin/python hackathon/prototype/make_labeled_set.py [N_per_class]
Out:   out/labeled_features.csv
"""
from __future__ import annotations
import glob
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from features import extract_features, FEATURE_ORDER  # noqa: E402

HERE = os.path.dirname(__file__)
M1 = os.path.abspath(os.path.join(HERE, "..", "..", "data", "processed", "m1"))
OUT = os.path.join(HERE, "out"); os.makedirs(OUT, exist_ok=True)
CLASSES = ["transit", "eclipse", "blend", "other"]


def _time_grids(n):
    """Borrow real time arrays (cadence + gaps) from cached conditioned LCs.

    Returns (host_id, time, rms) so downstream evaluation can do leakage-safe,
    group-aware CV (no host LC shared between train and test folds)."""
    grids = []
    for fp in sorted(glob.glob(os.path.join(M1, "*.npz")))[: max(n, 40)]:
        d = np.load(fp)
        t = np.asarray(d["time"], float)
        rms = float(1.4826 * np.median(np.abs(d["resid"] - np.median(d["resid"]))))
        if t.size > 2000 and np.isfinite(rms) and rms > 0:
            host = os.path.splitext(os.path.basename(fp))[0]
            grids.append((host, t, min(max(rms, 1e-4), 0.01)))
    return grids


def _transit(t, t0, P, depth, dur):
    """U-shaped (flat-bottomed, box-like) transit — planet. depth>0 = dip; dur in days."""
    ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
    x = np.abs(ph) * P / (dur / 2)          # 0 at center, 1 at contact
    u = np.clip(1 - x, 0, 1)
    return -depth * np.sqrt(np.clip(1 - (1 - u) ** 2, 0, 1))   # rounded flat-bottom (U)


def _vshape(t, t0, P, depth, dur):
    """V-shaped (pointed, short flat bottom) dip — eclipsing binary / diluted blend."""
    ph = ((t - t0) / P + 0.5) % 1.0 - 0.5
    x = np.abs(ph) * P / (dur / 2)          # 0 at center, 1 at contact
    return -depth * np.clip(1 - x, 0, 1)    # linear -> V


def _inject(kind, t, rms, rng):
    P = rng.uniform(1.5, 9.0)
    t0 = t.min() + rng.uniform(0, P)
    dur = rng.uniform(0.06, 0.20)
    sig = np.zeros_like(t)
    if kind == "transit":
        depth = rng.uniform(0.0008, 0.01)
        sig = _transit(t, t0, P, depth, dur)
    elif kind == "eclipse":
        depth = rng.uniform(0.03, 0.20)
        sig = _vshape(t, t0, P, depth, dur)          # deep V
        # odd-even alternation
        cyc = np.round((t - t0) / P).astype(int)
        sig[cyc % 2 == 1] *= rng.uniform(0.6, 0.85)
        # secondary eclipse at phase 0.5
        ph = ((t - t0) / P) % 1.0
        sec = np.abs(ph - 0.5) < (dur / 2 / P)
        sig[sec] += -depth * rng.uniform(0.2, 0.5)
    elif kind == "blend":
        depth = rng.uniform(0.0008, 0.008)           # shallow like a planet...
        sig = _vshape(t, t0, P, depth, dur)          # ...but V-shaped (diluted EB)
        cyc = np.round((t - t0) / P).astype(int)
        sig[cyc % 2 == 1] *= rng.uniform(0.5, 0.8)   # ...with odd-even tell
        ph = ((t - t0) / P) % 1.0
        sec = np.abs(ph - 0.5) < (dur / 2 / P)
        sig[sec] += -depth * rng.uniform(0.3, 0.6)   # ...and a secondary tell
    elif kind == "other":
        amp = rng.uniform(2, 6) * rms
        sig = amp * np.sin(2 * np.pi * t / P + rng.uniform(0, 2 * np.pi))
    noise = rng.normal(0, rms, t.size)
    return sig + noise


def main(n_per=120):
    grids = _time_grids(n_per)
    if not grids:
        print("No cached LCs to borrow time grids from."); return
    rng = np.random.default_rng(7)
    rows = []
    for kind in CLASSES:
        made = 0
        while made < n_per:
            host, t, rms = grids[rng.integers(len(grids))]
            r = _inject(kind, t, rms, rng)
            try:
                feat = extract_features(t, r)
            except Exception:
                continue
            feat["host"] = host
            feat["label"] = kind
            rows.append(feat); made += 1
        print(f"  {kind:8} {made} examples")
    df = pd.DataFrame(rows)
    cols = [c for c in FEATURE_ORDER if c in df.columns] + ["host", "label"]
    df = df[cols]
    out = os.path.join(OUT, "labeled_features.csv")
    df.to_csv(out, index=False)
    print(f"Labeled set ({len(df)} rows) -> {out}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 120)
