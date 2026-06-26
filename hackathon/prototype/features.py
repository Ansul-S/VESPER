"""BAH2026 PS7 prototype — physics-feature extractor (design doc §3).

SMOKE-TEST grade: extracts interpretable, classifier-ready features from a
*conditioned* TESS light curve (time, resid) using the reused TRINETRA-X spine
(detector.detect_events + period_recovery.best_period). These are the physics
branch inputs for the hybrid transit/eclipse/blend/other classifier.

Not the final implementation — this proves the extractor runs on real data and
produces sensible, separable features. No labels, no TPF/centroid here.
"""
from __future__ import annotations

import os
import sys

import numpy as np

# reuse the sealed Phase-I spine (untrained detector + period-from-spacing)
_SPINE = os.path.join(os.path.dirname(__file__), "..", "..", "research", "m3_calibration")
sys.path.insert(0, os.path.abspath(_SPINE))
from detector import detect_events          # noqa: E402
from period_recovery import best_period      # noqa: E402

# default search config (TESS single-sector scale)
DURATION_GRID = np.array([0.05, 0.08, 0.12, 0.18, 0.25])   # days
P_MIN, P_MAX = 0.5, 13.0                                    # days
Z_EXTRACT = 2.0                                             # event extraction floor (SNR)


def _phase(time, t0, period):
    """Phase in [-0.5, 0.5), transit centred at 0."""
    return ((time - t0) / period + 0.5) % 1.0 - 0.5


def _robust_rms(x):
    return float(1.4826 * np.median(np.abs(x - np.median(x)))) if x.size else np.nan


def extract_features(time, resid, *, duration_grid=DURATION_GRID,
                     p_min=P_MIN, p_max=P_MAX, z_extract=Z_EXTRACT):
    """Return a dict of physics features for one conditioned light curve."""
    t = np.asarray(time, float)
    r = np.asarray(resid, float)
    f = {
        "n_points": int(t.size),
        "baseline_days": float(t.max() - t.min()) if t.size else 0.0,
        "oot_rms": _robust_rms(r),
    }

    ev = detect_events(t, r, duration_grid, z_for_extraction=z_extract)
    f["n_events"] = int(ev.shape[0])
    if ev.shape[0] == 0:
        f.update(dict(max_snr=0.0, total_snr=0.0, has_evidence=0))
        return f

    epochs, snrs, durs = ev[:, 0], ev[:, 1], ev[:, 2]
    f["max_snr"] = float(snrs.max())
    f["total_snr"] = float(np.sqrt(np.sum(snrs ** 2)))
    f["has_evidence"] = 1
    f["best_dur_days"] = float(durs[np.argmax(snrs)])

    if ev.shape[0] < 2:
        f.update(dict(period_days=np.nan, fold_R=0.0, depth=np.nan,
                      depth_snr=np.nan, odd_even_diff=np.nan,
                      secondary_depth=np.nan, v_over_u=np.nan,
                      duration_frac=np.nan))
        return f

    # period from event spacing (reused spine)
    P, score, R = best_period(epochs, p_min, p_max)
    f["period_days"] = float(P)
    f["fold_R"] = float(R)               # phase-alignment quality of the comb

    t0 = epochs[int(np.argmax(snrs))]    # reference on the strongest event
    dur = f["best_dur_days"]
    if not np.isfinite(P) or P <= 0:
        return f
    half_w = 0.5 * dur / P               # half transit width in phase units
    ph = _phase(t, t0, P)

    in_tr = np.abs(ph) <= half_w
    oot = np.abs(ph) > 3 * half_w
    f["duration_frac"] = float(dur / P)

    base = np.median(r[oot]) if oot.any() else 0.0
    depth = float(base - np.median(r[in_tr])) if in_tr.any() else np.nan   # +ve = dip
    f["depth"] = depth
    noise = _robust_rms(r[oot]) if oot.any() else np.nan
    n_in = max(int(in_tr.sum()), 1)
    f["depth_snr"] = float(depth / (noise / np.sqrt(n_in))) if noise and noise > 0 else np.nan

    # --- odd/even depth difference (EB / blend tell) ---
    cyc = np.round((t - t0) / P).astype(int)
    odd = in_tr & (cyc % 2 == 1)
    even = in_tr & (cyc % 2 == 0)
    if odd.any() and even.any():
        d_odd = base - np.median(r[odd])
        d_even = base - np.median(r[even])
        denom = abs(d_odd) + abs(d_even)
        f["odd_even_diff"] = float(abs(d_odd - d_even) / denom) if denom > 0 else 0.0
    else:
        f["odd_even_diff"] = np.nan

    # --- secondary eclipse at phase 0.5 (EB / blend tell) ---
    sec = np.abs(np.abs(ph) - 0.5) <= half_w
    if sec.any():
        sec_depth = base - np.median(r[sec])
        f["secondary_depth"] = float(sec_depth)
        f["secondary_ratio"] = float(sec_depth / depth) if depth and depth > 0 else np.nan
    else:
        f["secondary_depth"] = np.nan
        f["secondary_ratio"] = np.nan

    # --- V vs U shape: inner-third depth vs full in-transit depth (U>~1, V<1) ---
    inner = np.abs(ph) <= (half_w / 3)
    if inner.any() and in_tr.any() and depth and depth > 0:
        d_inner = base - np.median(r[inner])
        f["v_over_u"] = float(d_inner / depth)   # ~1 flat-bottom (U/box), <1 pointy (V)
    else:
        f["v_over_u"] = np.nan

    # --- trapezoid shape-fit parameters (committee step 03; THE discriminator) ---
    f.update(_shape_features(t, r, P, t0, dur))
    return f


def _shape_features(t, r, P, t0, dur):
    """Fold + fit trapezoid -> flat_frac, ingress_frac, t_total_h, fit depth (U vs V)."""
    out = {"flat_frac": np.nan, "ingress_frac": np.nan,
           "t_total_h": np.nan, "fit_depth_ppm": np.nan}
    try:
        from shape_fit import fit_trapezoid, fold_to_hours, binned
        win = max(6.0, dur * 24 * 3)
        th, fx = fold_to_hours(t, r, P, t0, window_h=win)
        if th.size < 30:
            return out
        xb, yb = binned(th, fx, 60)
        if xb.size < 8:
            return out
        sf = fit_trapezoid(xb, yb)
        if sf:
            out.update(flat_frac=sf["flat_frac"], ingress_frac=sf["ingress_frac"],
                       t_total_h=sf["t_total_h"], fit_depth_ppm=sf["depth_ppm"])
    except Exception:
        pass
    return out


FEATURE_ORDER = [
    "n_points", "baseline_days", "oot_rms", "n_events", "has_evidence",
    "max_snr", "total_snr", "best_dur_days", "period_days", "fold_R",
    "depth", "depth_snr", "duration_frac", "odd_even_diff",
    "secondary_depth", "secondary_ratio", "v_over_u",
    "flat_frac", "ingress_frac", "t_total_h", "fit_depth_ppm",
]
