"""M4 injection — Mandel-Agol transits on the sealed grid (VAL §3).

Reuses the M2 geometry + batman model verbatim (the injection physics is frozen).
Two host modes:
  * raw            (PRODUCTION) — inject into raw PDCSAP flux, then re-condition at the
                   frozen 2.5 d window (M2 path; network). eta attenuation is real.
  * cached_residual (DRY-RUN, offline) — add the (model-1) transit signal to a cached
                   conditioned residual. Validates the detector->TLS->recovery plumbing
                   with NO network; eta is not re-measured (flagged in provenance).

The Claret-2017 LD interpolator (M2) needs VizieR; the dry-run uses a constant
quadratic LD fallback so it runs fully offline. The PRODUCTION run uses Claret-2017.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m2_injection"))

from m2_pipeline import _geometry, _model  # noqa: E402  (frozen injection physics)

GRID_P = [0.5, 1, 2, 4, 8, 16]      # days   (sealed, VAL §3)
GRID_R = [1, 2, 4, 8, 12]           # R_earth
GRID_B = [0.0, 0.3, 0.6]            # impact parameter


def constant_ld(u1: float = 0.4, u2: float = 0.3):
    """Offline LD fallback (dry-run only). PRODUCTION uses m2.build_ld_interpolator (Claret 2017)."""
    def ld(_teff, _logg):
        return u1, u2
    return ld


def n_transits(baseline_days: float, period_days: float) -> int:
    """Coarse transit count over the baseline (E1 restricts to cells with n_tr >= 2)."""
    if period_days <= 0:
        return 0
    return int(np.floor(baseline_days / period_days)) + 1


def inject_into_residual(t, r, t0, P, geom, u1, u2):
    """DRY-RUN offline host mode: r_inj = r + (model - 1). model-1 < 0 in transit."""
    model = _model(t, t0, P, geom, u1, u2)            # depth = geom['depth']
    return r + (model - 1.0)


def build_injection(t_host, P, Rp, b, srow, ld, rng, host_mode="cached_residual", r_host=None, d=None):
    """Return (t, r_injected, truth_dict) for one injection, or None if it cannot be built.

    host_mode='cached_residual' uses r_host (offline). host_mode='raw' reconditions
    via the M2 path (production; needs t_host=raw flux + detrend params d).
    """
    geom = _geometry(P, Rp, b, float(srow["rad"]), float(srow["logg"]), ld)
    u1, u2 = ld(float(srow["Teff"]), float(srow["logg"]))
    span = (float(t_host.min()), float(t_host.max()))
    if span[1] - span[0] < 1.0:
        return None
    t0 = rng.uniform(span[0] + 0.5, span[1] - 0.5)
    truth = {"P_true": float(P), "t0_true": float(t0), "Rp": float(Rp), "b": float(b),
             "depth_true": float(geom["depth"]), "t14_true": float(geom["t14_days"]),
             "n_transits": n_transits(span[1] - span[0], P)}
    if host_mode == "cached_residual":
        if r_host is None:
            return None
        r_inj = inject_into_residual(t_host, r_host, t0, P, geom, u1, u2)
        return np.asarray(t_host, float), np.asarray(r_inj, float), truth
    elif host_mode == "raw":
        from m2_pipeline import inject_measure  # noqa
        # production: inject into raw flux then re-condition (M2 path). Returns conditioned residual.
        from wotan import flatten
        f_inj = np.asarray(r_host, float) * _model(t_host, t0, P, geom, u1, u2)  # r_host = raw flux here
        flat, _ = flatten(t_host, f_inj, window_length=float(d["window_length_days"]), method=d["method"],
                          break_tolerance=float(d["break_tolerance_days"]),
                          edge_cutoff=float(d["edge_cutoff_days"]), cval=float(d["cval"]), return_trend=True)
        ok = np.isfinite(flat)
        if ok.sum() < 50:
            return None
        return np.asarray(t_host[ok], float), np.asarray(flat[ok] - 1.0, float), truth
    raise ValueError(f"unknown host_mode {host_mode}")
