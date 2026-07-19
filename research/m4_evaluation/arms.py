"""M4 Arm-A runner (VAL A.1) — the sealed full-grid TLS baseline.

Arm A (baseline, and the Arm-B full-TLS fallback): full-grid TLS, SDE >= T.
All thresholds come from the Seal #2 FrozenThresholds — nothing here is tunable.

The v2 targeted-TLS Arm B that used to live here was proven non-executable by
DR-002 Finding B (SDE is grid-normalized) and is preserved, for dry-run artifact
provenance only, in superseded_v2/arms_v2.py. The sealed v3 Arm B is
m4_driver._route_and_seed + confirmer.confirm.
"""

from __future__ import annotations

import numpy as np


def _run_tls(t, flux, period_min, period_max, oversampling):
    """Sealed TLS call; also returns T0 + duration for the recovery predicate."""
    from transitleastsquares import transitleastsquares
    model = transitleastsquares(np.asarray(t, float), np.asarray(flux, float))
    res = model.power(period_min=float(period_min), period_max=float(period_max),
                      oversampling_factor=int(oversampling), use_threads=1,
                      show_progress_bar=False)
    return {"sde": float(res.SDE), "period": float(res.period),
            "t0": float(getattr(res, "T0", np.nan)), "duration": float(getattr(res, "duration", np.nan))}


def _pmax(t, fr):
    baseline = float(np.max(t) - np.min(t))
    return max(fr.period_min_days * 1.5, fr.period_max_frac_baseline * baseline)


def arm_a_full(t, r, fr):
    """Arm A: full-grid TLS on the conditioned residual (flux = 1 + r)."""
    out = _run_tls(t, 1.0 + r, fr.period_min_days, _pmax(t, fr), fr.oversampling)
    out["mode"] = "full"
    return out
