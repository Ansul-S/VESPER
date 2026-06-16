"""M3 detector — GP-whitened matched filter (MATH §2), untrained.

Box matched filter over a frozen T14 duration grid with a red-noise-aware noise
normalization: the box-averaged depth series d(t0) is normalized by its own robust
scatter on the transit-duration timescale (1.4826*MAD), which is exactly the
duration-timescale CDPP and the operative effect of the generalized (Sigma-whitened)
matched filter g^T Sigma^-1 r / sqrt(g^T Sigma^-1 g) for the near-white conditioned
residuals (M1 2.5 d diagnostics: acf_lag1 ~ 0.01). For correlated residuals the
self-calibrated scatter absorbs the residual redness, so no per-epoch GP solve is needed.

A detected EVENT is a local minimum of d(t0) whose SNR = -d/scatter >= z_star.
Returns event epochs + SNRs; no threshold is hard-coded (z_star is calibrated in M3).
"""

from __future__ import annotations

import numpy as np


def _box_depth_series(t: np.ndarray, r: np.ndarray, width_days: float):
    """Box-averaged depth d(t0) and trial epochs for a transit of duration width_days.

    d>0 means a flux *decrement* (transit-like), since r is zero-centred with transit negative
    we report depth = -mean(r) over the window so positive depth = transit-like.
    """
    cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
    nbin = max(1, int(round(width_days / cad)))
    if r.size < 2 * nbin:
        return np.empty(0), np.empty(0)
    # cumulative-sum sliding mean over nbin-wide windows (stride = nbin//2 via t0_stride applied by caller)
    csum = np.concatenate([[0.0], np.cumsum(r)])
    win_mean = (csum[nbin:] - csum[:-nbin]) / nbin          # length r.size-nbin+1, aligned to window start
    t0 = t[: win_mean.size] + 0.5 * width_days               # window-centre epoch
    depth = -win_mean                                        # positive = transit-like decrement
    return t0, depth


def detect_events(t: np.ndarray, r: np.ndarray, duration_grid_days, stride_frac: float = 0.5,
                  z_for_extraction: float = 0.0):
    """Run the box matched filter over the duration grid; return events as (epoch, snr, dur).

    z_for_extraction only filters which local minima are *returned* (set 0 to return all
    candidate minima with their SNR so calibration can sweep z_star post hoc).
    """
    events = []
    for dur in duration_grid_days:
        t0, depth = _box_depth_series(t, r, float(dur))
        if t0.size == 0:
            continue
        scatter = 1.4826 * np.median(np.abs(depth - np.median(depth)))
        if not np.isfinite(scatter) or scatter <= 0:
            continue
        snr = depth / scatter                                # positive SNR = transit-like
        # stride: keep one trial per stride_frac*dur to avoid oversampling the same window
        cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
        step = max(1, int(round(stride_frac * float(dur) / cad)))
        idx = np.arange(0, snr.size, step)
        ts, ss = t0[idx], snr[idx]
        # local maxima of SNR (transit-like peaks) above the extraction floor
        for k in range(1, ts.size - 1):
            if ss[k] >= z_for_extraction and ss[k] >= ss[k - 1] and ss[k] >= ss[k + 1]:
                events.append((float(ts[k]), float(ss[k]), float(dur)))
    if not events:
        return np.empty((0, 3))
    ev = np.array(events)
    # de-duplicate events overlapping in time across durations: keep the highest-SNR within 0.3 d
    ev = ev[np.argsort(-ev[:, 1])]
    kept = []
    for e in ev:
        if all(abs(e[0] - k[0]) > 0.3 for k in kept):
            kept.append(e)
    return np.array(kept)


def max_event_snr(t, r, duration_grid_days, stride_frac=0.5) -> float:
    """Highest transit-like SNR anywhere in the light curve (for false-event calibration)."""
    ev = detect_events(t, r, duration_grid_days, stride_frac, z_for_extraction=-np.inf)
    return float(ev[:, 1].max()) if ev.size else float("nan")
