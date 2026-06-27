"""BAH2026 PS7 prototype — validate the full pipeline on KNOWN objects.

Real-label validation: run conditioning -> period recovery (TLS) -> trapezoid
shape-fit on a set of confirmed transiting PLANETS and known ECLIPSING BINARIES,
then check the shape verdict (U vs V) against ground truth. Planets come fresh
from MAST by name; EBs include physically-unambiguous deep eclipses scanned from
the conditioned cache (depth > 5% cannot be a planet -> rock-solid EB label).

Run (slow; downloads): .venv/bin/python hackathon/prototype/validate_known.py
Out: out/validation_known.csv  +  figs/validation_known.png
"""
from __future__ import annotations
import glob
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "research", "m3_calibration")))
from shape_fit import fit_trapezoid, fold_to_hours, binned  # noqa: E402

HERE = os.path.dirname(__file__)
M1 = os.path.abspath(os.path.join(HERE, "..", "..", "data", "processed", "m1"))
OUT = os.path.join(HERE, "out"); FIGS = os.path.join(HERE, "figs")
os.makedirs(OUT, exist_ok=True)
WINDOW = 2.5

# confirmed transiting planets (name, literature period d) — expect U / planet-like
PLANETS = [("Pi Mensae", 6.27), ("WASP-18", 0.941), ("WASP-121", 1.275),
           ("AU Mic", 8.463), ("LHS 3844", 0.463), ("WASP-100", 2.849)]
# known eclipsing binary by name — expect V / EB-like. (Other bright EBs like
# U Cephei / TW Draconis stall on MAST download; we use the reliable cache scan
# for additional, physically-unambiguous deep-eclipse EBs instead.)
EBS_NAMED = [("RZ Cassiopeiae", 1.195)]


def fetch_by_name(name):
    import lightkurve as lk
    from wotan import flatten
    sr = lk.search_lightcurve(name, mission="TESS", author="SPOC", exptime=120)
    if len(sr) == 0:
        raise RuntimeError("no SPOC 2-min")
    lc = sr[0].download(quality_bitmask="default")
    t = np.asarray(lc.time.value, float); f = np.asarray(lc.flux.value, float)
    g = np.isfinite(t) & np.isfinite(f); t, f = t[g], f[g]
    f = f / np.median(f)
    flat, _ = flatten(t, f, window_length=WINDOW, method="biweight", return_trend=True)
    r = flat - 1.0; g = np.isfinite(r)
    return t[g], r[g]


def run_tls(t, r, pmin=0.4, pmax=15.0):
    from transitleastsquares import transitleastsquares
    flux = 1.0 + r
    res = transitleastsquares(t, flux).power(period_min=pmin, period_max=min(pmax, (t.max()-t.min())/2),
                                             use_threads=1, oversampling_factor=2, duration_grid_step=1.2)
    return res


def characterize(t, r):
    res = run_tls(t, r)
    th, fx = fold_to_hours(t, r, res.period, res.T0, window_h=max(6.0, res.duration * 24 * 2.5))
    xb, yb = binned(th, fx, 60)
    fit = fit_trapezoid(xb, yb) if xb.size >= 8 else None
    return res, fit


def characterize_spine(t, r):
    """Fast (no-TLS) period + shape fit using the reused spine — for deep EBs."""
    from detector import detect_events
    from period_recovery import best_period
    from features import DURATION_GRID, Z_EXTRACT
    ev = detect_events(t, r, DURATION_GRID, z_for_extraction=Z_EXTRACT)
    if ev.shape[0] < 2:
        return None, None
    P, _, _ = best_period(ev[:, 0], 0.4, 13.0)
    if not np.isfinite(P) or P <= 0:
        return None, None
    t0 = ev[int(np.argmax(ev[:, 1])), 0]
    dur = ev[int(np.argmax(ev[:, 1])), 2]
    th, fx = fold_to_hours(t, r, P, t0, window_h=max(6.0, dur * 24 * 2.5))
    xb, yb = binned(th, fx, 60)
    fit = fit_trapezoid(xb, yb) if xb.size >= 8 else None
    return P, fit


def cached_deep_ebs(n=4, min_depth=0.05):
    """Scan conditioned cache (fast spine, no TLS) for unambiguous deep eclipses
    (depth > 5% cannot be a planet -> rock-solid EB ground truth)."""
    out = []
    for fp in sorted(glob.glob(os.path.join(M1, "*.npz"))):
        d = np.load(fp); t = d["time"].astype(float); r = d["resid"].astype(float)
        if t.size < 5000:
            continue
        try:
            P, fit = characterize_spine(t, r)
        except Exception:
            continue
        if fit and fit["depth"] > min_depth:
            out.append((os.path.splitext(os.path.basename(fp))[0], P, fit))
            if len(out) >= n:
                break
    return out


class _Res:
    """Lightweight stand-in for a TLS result (cache EBs use the fast spine)."""
    def __init__(self, period, sde):
        self.period = period; self.SDE = sde


def verdict_correct(true_cls, fit):
    if not fit:
        return False
    is_u = fit["flat_frac"] > 0.35
    return (true_cls == "planet" and is_u) or (true_cls == "EB" and not is_u)


def main():
    rows, plotdata = [], []

    for name, plit in PLANETS:
        try:
            t, r = fetch_by_name(name)
            res, fit = characterize(t, r)
        except Exception as e:
            print(f"  [planet] {name}: SKIP ({type(e).__name__})"); continue
        _record(rows, plotdata, name, "planet", plit, res, fit)

    for name, plit in EBS_NAMED:
        try:
            t, r = fetch_by_name(name)
            res, fit = characterize(t, r)
        except Exception as e:
            print(f"  [EB] {name}: SKIP ({type(e).__name__})"); continue
        _record(rows, plotdata, name, "EB", plit, res, fit)

    print("  scanning cache for deep (unambiguous) EBs ...")
    for tic, P, fit in cached_deep_ebs(n=5):
        _record(rows, plotdata, f"TIC {tic}", "EB", np.nan, _Res(P, np.nan), fit)

    df = pd.DataFrame(rows)
    csv = os.path.join(OUT, "validation_known.csv"); df.to_csv(csv, index=False)
    acc = df["verdict_ok"].mean() if len(df) else float("nan")
    print(f"\nValidated {len(df)} known objects | shape-verdict accuracy = {acc:.2f}")
    print(df.to_string(index=False))
    _plot(plotdata, acc)
    print(f"\nCSV -> {csv}")


def _record(rows, plotdata, name, true_cls, plit, res, fit):
    ff = fit["flat_frac"] if fit else np.nan
    depth_ppm = fit["depth_ppm"] if fit else np.nan
    ok = verdict_correct(true_cls, fit)
    rows.append({"target": name, "true_class": true_cls, "P_lit_d": plit,
                 "P_rec_d": round(float(res.period), 4), "SDE": round(float(res.SDE), 1),
                 "depth_ppm": round(float(depth_ppm), 0) if np.isfinite(depth_ppm) else np.nan,
                 "flat_frac": round(float(ff), 3) if np.isfinite(ff) else np.nan,
                 "verdict": fit["shape_verdict"] if fit else "no-fit", "verdict_ok": bool(ok)})
    if fit and np.isfinite(ff) and np.isfinite(depth_ppm):
        plotdata.append((true_cls, depth_ppm, ff, name))
    tag = "OK" if ok else "x"
    print(f"  [{true_cls:6}] {name:16} P_rec={res.period:7.3f}d depth={depth_ppm:7.0f}ppm "
          f"flat_frac={ff:.2f} -> {fit['shape_verdict'] if fit else 'no-fit'} [{tag}]")


def _plot(plotdata, acc):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 6))
    for cls, col, mk in [("planet", "#1e8449", "o"), ("EB", "#c0392b", "s")]:
        xs = [d for c, dp, d, n in plotdata if c == cls]
        ys = [dp for c, dp, d, n in plotdata if c == cls]
        ax.scatter(xs, ys, c=col, marker=mk, s=90, label=cls, edgecolor="k", zorder=3)
    for cls, dp, d, n in plotdata:
        ax.annotate(n, (d, dp), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.axvline(0.35, ls="--", color="0.4", label="U/V boundary (flat_frac=0.35)")
    ax.set(xlabel="flat-bottom fraction  (V-shape ← → U-shape)", ylabel="transit depth (ppm)",
           yscale="log", title=f"Pipeline validation on known objects — shape-verdict accuracy {acc:.0%}")
    ax.legend(); fig.tight_layout()
    p = os.path.join(FIGS, "validation_known.png"); fig.savefig(p, dpi=120)
    print(f"figure -> {p}")


if __name__ == "__main__":
    main()
