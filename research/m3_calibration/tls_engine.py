"""M3 shared TLS engine (VAL A.1) — identical config in both arms. PINNED transitleastsquares.

Arm A (full): optimal-frequency grid over [P_min, 0.5*T_base], oversampling=3.
Arm B (targeted): narrow window [P_hat(1-eps), P_hat(1+eps)] around the inferred period.
Returns the TLS SDE (the single common significance statistic; threshold T calibrated in M3).
"""

from __future__ import annotations

import numpy as np


def _run_tls(t, flux, period_min, period_max, oversampling):
    from transitleastsquares import transitleastsquares
    model = transitleastsquares(t.astype(float), flux.astype(float))
    res = model.power(period_min=float(period_min), period_max=float(period_max),
                      oversampling_factor=int(oversampling), use_threads=1,
                      show_progress_bar=False)
    return float(res.SDE), float(res.period)


def full_tls(t, r, cfg):
    """Arm A: full-grid TLS. r is the zero-centred residual; flux = 1 + r."""
    baseline = float(t.max() - t.min())
    p_max = max(float(cfg["period_min_days"]) * 1.5,
                float(cfg["period_max_frac_baseline"]) * baseline)
    sde, period = _run_tls(t, 1.0 + r, cfg["period_min_days"], p_max, cfg["oversampling_factor"])
    return {"sde": sde, "period": period, "p_min": float(cfg["period_min_days"]), "p_max": p_max,
            "mode": "full"}


def targeted_tls(t, r, p_hat, epsilon, cfg):
    """Arm B: TLS restricted to [p_hat(1-eps), p_hat(1+eps)]."""
    p_min = max(float(cfg["period_min_days"]), p_hat * (1.0 - epsilon))
    p_max = p_hat * (1.0 + epsilon)
    sde, period = _run_tls(t, 1.0 + r, p_min, p_max, cfg["oversampling_factor"])
    return {"sde": sde, "period": period, "p_min": p_min, "p_max": p_max, "mode": "targeted"}
