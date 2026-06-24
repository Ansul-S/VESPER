"""M4 operational recovery predicate (VAL §4.1) — applied identically to both arms.

An injected planet is RECOVERED by an arm iff ALL hold:
  (i)   Period:  |P_hat - P_true|/P_true < 0.01  OR a harmonic {P_true/m, m*P_true},
        m in {2,3}, within 1% (harmonic matches counted recovered but FLAGGED).
  (ii)  Epoch:   recovered ephemeris aligns to a true transit within +/- 0.5 * T14_true.
  (iii) Significance:  arm's TLS SDE >= T  (the single common Seal #2 threshold).
"""

from __future__ import annotations

import numpy as np

PERIOD_TOL = 0.01
HARMONICS = (2, 3)


def _period_match(p_hat, p_true):
    """Return (matched, is_harmonic). Direct 1% match, else m in {2,3} harmonic within 1%."""
    if not np.isfinite(p_hat) or p_hat <= 0:
        return False, False
    if abs(p_hat - p_true) / p_true < PERIOD_TOL:
        return True, False
    for m in HARMONICS:
        for cand in (p_true / m, m * p_true):
            if abs(p_hat - cand) / cand < PERIOD_TOL:
                return True, True
    return False, False


def _epoch_match(t0_hat, p_hat, t0_true, t14_true):
    """True transit (t0_true) folded on the recovered ephemeris within +/- 0.5 T14."""
    if not np.isfinite(t0_hat) or not np.isfinite(p_hat) or p_hat <= 0:
        return False
    dphi = (t0_true - t0_hat) % p_hat
    dphi = min(dphi, p_hat - dphi)            # fold to [0, P/2]
    return dphi <= 0.5 * max(t14_true, 1e-3)


def recovered(arm_result: dict, truth: dict, T_sde: float) -> dict:
    """Apply the three-part predicate. Returns flags dict (recovered + harmonic + per-criterion)."""
    p_ok, harm = _period_match(arm_result.get("period", np.nan), truth["P_true"])
    e_ok = _epoch_match(arm_result.get("t0", np.nan), arm_result.get("period", np.nan),
                        truth["t0_true"], truth["t14_true"])
    sde = arm_result.get("sde", np.nan)
    s_ok = bool(np.isfinite(sde) and sde >= T_sde)
    rec = bool(p_ok and e_ok and s_ok)
    return {"recovered": rec, "harmonic": bool(harm and rec),
            "period_ok": bool(p_ok), "epoch_ok": bool(e_ok), "sde_ok": s_ok, "sde": float(sde)}
