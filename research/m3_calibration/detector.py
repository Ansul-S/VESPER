"""M3 detector — MAD-normalized box matched filter over a frozen duration grid, untrained.

Box matched filter over the frozen T14 duration grid with a self-calibrated noise
normalization: the box-averaged depth series d(t0) is normalized by its own robust
scatter (1.4826*MAD), which is the duration-timescale CDPP. For the near-white
conditioned residuals of Phase I (M1 2.5 d diagnostics: acf_lag1 ~ 0.01) the
self-calibrated scatter absorbs the residual redness, so no per-epoch GP solve is
needed. NOTE (audit 2026-07-19): this is NOT a GP-whitened filter — the earlier
docstring overstated it. GP whitening (g^T Sigma^-1 r) exists only in the Arm-B
confirmer (confirmer.py); the MATH §11.3 "GP-whitened detection" claim is realized
there, not here.

Gap handling (added 2026-07-19, post-sealed-run): the sliding window is computed
per contiguous segment (split at gaps > gap_break_days), so windows never average
across TESS downlink/momentum-dump gaps and event epochs are not mislabeled near
gap edges. The sealed Phase-I runs used the pre-fix (index-space) version, preserved
verbatim in research/m4_evaluation/frozen_rerun/detector.py; the change affects
future (Phase-II) runs only.

A detected EVENT is a local maximum of SNR = depth/scatter >= z_star.
Returns event epochs + SNRs; no threshold is hard-coded (z_star is calibrated in M3).
"""

from __future__ import annotations

import numpy as np

GAP_BREAK_DAYS = 0.5   # split segments at gaps longer than this


def _segments(t: np.ndarray, gap_break_days: float = GAP_BREAK_DAYS):
    """Index slices of contiguous (gap-free) stretches of the time array."""
    if t.size == 0:
        return []
    brk = np.where(np.diff(t) > gap_break_days)[0]
    starts = np.concatenate([[0], brk + 1])
    ends = np.concatenate([brk + 1, [t.size]])
    return [slice(s, e) for s, e in zip(starts, ends)]


def _box_depth_series_segment(t: np.ndarray, r: np.ndarray, width_days: float):
    """Box-averaged depth d(t0) over one contiguous segment (positive = transit-like)."""
    cad = float(np.median(np.diff(t))) if t.size > 1 else 2.0 / 1440.0
    nbin = max(1, int(round(width_days / cad)))
    if r.size < 2 * nbin:
        return np.empty(0), np.empty(0)
    csum = np.concatenate([[0.0], np.cumsum(r)])
    win_mean = (csum[nbin:] - csum[:-nbin]) / nbin          # aligned to window start
    t0 = t[: win_mean.size] + 0.5 * width_days               # window-centre epoch (gapless segment)
    depth = -win_mean                                        # r is zero-centred, transit negative
    return t0, depth


def _box_depth_series(t: np.ndarray, r: np.ndarray, width_days: float):
    """Concatenate per-segment depth series so windows never span data gaps."""
    ts, ds = [], []
    for sl in _segments(t):
        t0, d = _box_depth_series_segment(t[sl], r[sl], width_days)
        if t0.size:
            ts.append(t0); ds.append(d)
    if not ts:
        return np.empty(0), np.empty(0)
    return np.concatenate(ts), np.concatenate(ds)


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
