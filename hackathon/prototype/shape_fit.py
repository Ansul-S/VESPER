"""BAH2026 PS7 prototype — trapezoid transit-shape fit (committee step 03).

The committee's own false-positive example proves DEPTH does not separate a
planet from an eclipsing binary/false positive (both ~1.4%); the SHAPE does —
specifically the ingress/egress duration and the flat-bottom fraction (U vs V).
Their "Further Steps" slide says the classifier should be built ON the transit
SHAPE PARAMETERS. This module fits the symmetric trapezoid and returns exactly
the parameters shown on their slides 5/6.

Model (time t in hours from mid-transit), symmetric trapezoid:
  baseline f0                              for |t| >= T_tot/2
  linear ingress/egress                    for T_flat/2 < |t| < T_tot/2
  flat bottom f0 - depth                   for |t| <= T_flat/2
with T_flat = T_tot - 2*T_ing.
"""
from __future__ import annotations
import numpy as np
from scipy.optimize import curve_fit


def trapezoid(t, f0, depth, tc, t_tot, t_ing):
    """Symmetric trapezoid transit. t, durations in hours; depth>0 = dip."""
    t_tot = max(t_tot, 1e-3)
    t_ing = float(np.clip(t_ing, 1e-3, t_tot / 2))
    x = np.abs(t - tc)
    half_tot, half_flat = t_tot / 2, t_tot / 2 - t_ing
    y = np.zeros_like(x)
    # ingress/egress ramp 0..1 between half_flat and half_tot
    ramp = (half_tot - x) / max(t_ing, 1e-6)
    frac = np.where(x <= half_flat, 1.0, np.where(x >= half_tot, 0.0, ramp))
    return f0 - depth * np.clip(frac, 0, 1)


def fit_trapezoid(t_hours, flux):
    """Fit the trapezoid; return param dict + derived shape discriminators."""
    t = np.asarray(t_hours, float); y = np.asarray(flux, float)
    good = np.isfinite(t) & np.isfinite(y)
    t, y = t[good], y[good]
    f0_0 = np.median(y[np.abs(t) > 0.6 * np.ptp(t) / 2]) if t.size else 1.0
    depth0 = max(f0_0 - np.min(y), 1e-4)
    span = np.ptp(t)
    p0 = [f0_0, depth0, 0.0, 0.4 * span, 0.1 * span]
    bounds = ([f0_0 - 0.5, 1e-5, -span / 4, span * 0.02, 1e-3],
              [f0_0 + 0.5, 1.0, span / 4, span, span / 2])
    try:
        popt, pcov = curve_fit(trapezoid, t, y, p0=p0, bounds=bounds, maxfev=20000)
        perr = np.sqrt(np.clip(np.diag(pcov), 0, np.inf))
    except Exception:
        return None
    f0, depth, tc, t_tot, t_ing = popt
    t_flat = max(t_tot - 2 * t_ing, 0.0)
    resid = y - trapezoid(t, *popt)
    noise = 1.4826 * np.median(np.abs(resid - np.median(resid)))
    return {
        "baseline_flux": float(f0),
        "depth": float(depth), "depth_ppm": float(depth * 1e6), "depth_err_ppm": float(perr[1] * 1e6),
        "t_total_h": float(t_tot), "t_ingress_h": float(t_ing), "t_flat_h": float(t_flat),
        "flat_frac": float(t_flat / t_tot) if t_tot > 0 else 0.0,        # U (~1) vs V (~0)
        "ingress_frac": float(t_ing / t_tot) if t_tot > 0 else 0.0,      # V has large ingress_frac
        "fit_noise": float(noise),
        "shape_verdict": "U-shape (planet-like)" if (t_flat / max(t_tot, 1e-9)) > 0.35
                         else "V-shape (EB / false-positive-like)",
    }


def fold_to_hours(time_days, resid, period_days, t0_days, window_h=8.0):
    """Phase-fold and return (time-from-mid-transit [h], flux) within +/- window_h."""
    ph = ((np.asarray(time_days, float) - t0_days) / period_days + 0.5) % 1.0 - 0.5
    th = ph * period_days * 24.0
    flux = 1.0 + np.asarray(resid, float)
    m = np.abs(th) <= window_h
    order = np.argsort(th[m])
    return th[m][order], flux[m][order]


def binned(x, y, nb=80):
    b = np.linspace(x.min(), x.max(), nb + 1)
    idx = np.digitize(x, b) - 1
    xm, ym = [], []
    for k in range(nb):
        s = idx == k
        if s.sum() >= 3:
            xm.append(0.5 * (b[k] + b[k + 1])); ym.append(np.median(y[s]))
    return np.array(xm), np.array(ym)
