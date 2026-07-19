"""M3 TLS engine (VAL A.1) — the sealed full-grid baseline. PINNED transitleastsquares.

Arm A (full): optimal-frequency grid over [P_min, 0.5*T_base], oversampling=3.
Returns the TLS SDE (threshold T calibrated in M3).

The former `targeted_tls` (narrow window [P_hat(1±eps)]) was removed in the
2026-07-19 audit remediation: it was dead code after DR-002 Finding B (narrow-grid
SDE incomparable to full-grid T) and additionally carried Finding A (TLS silently
substitutes the full grid when the window holds < 100 periods). The historical
implementation lives in research/m4_evaluation/superseded_v2/.
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
