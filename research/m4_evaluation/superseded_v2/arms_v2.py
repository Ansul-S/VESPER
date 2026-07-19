"""SUPERSEDED v2 Arm-B (targeted TLS) — kept only so m4_run.py / dry_run artifacts
remain reproducible. Non-executable as a fair arm per DR-002 Finding B; the sealed
v3 TEST run used m4_driver.py + confirmer.py instead. Do not import from live code."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent.parent / "m3_calibration"))
sys.path.insert(0, str(HERE.parent))

from detector import detect_events                   # noqa: E402
from period_recovery import best_period, period_fap  # noqa: E402
from arms import _run_tls, _pmax                     # noqa: E402


def route(t, r, fr, tau_gp):
    """Detector + routing decision (v2). Returns (events, decision_dict)."""
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    snrs = ev[:, 1] if ev.size else np.empty(0)
    n_ev = int(snrs.size)
    max_snr = float(snrs.max()) if n_ev else float("nan")
    multi = n_ev >= fr.n_min
    monotransit = (not multi) and n_ev >= 1 and max_snr >= fr.z_mono
    p_hat, obs_R = np.nan, np.nan
    if multi:
        baseline = float(np.max(t) - np.min(t))
        p_min, p_max = fr.period_min_days, fr.period_max_frac_baseline * baseline
        p_hat, _, obs_R = best_period(ev[:, 0], p_min, p_max, fr.oversampling)
    dec = {"n_events": n_ev, "max_event_snr": max_snr, "multi_event": multi,
           "monotransit": monotransit, "fast_path_eligible": bool(multi or monotransit),
           "p_hat": float(p_hat) if np.isfinite(p_hat) else None,
           "obs_R": float(obs_R) if np.isfinite(obs_R) else None}
    return ev, dec


def arm_b_combined(t, r, fr, tau_gp, rng):
    """v2 Arm B: route -> targeted TLS (multi-event, period FAP ok) else full-TLS fallback.

    NON-EXECUTABLE as a fair arm (Finding B: narrow-grid SDE incomparable to full-grid T;
    Finding A: TLS ignores windows < 100 periods). Historical only."""
    ev, dec = route(t, r, fr, tau_gp)
    baseline = float(np.max(t) - np.min(t))
    p_min, p_max = fr.period_min_days, fr.period_max_frac_baseline * baseline
    out = {**dec, "fap": None, "tls_mode": None}

    if dec["multi_event"] and dec["p_hat"]:
        t14 = float(np.median(fr.duration_grid))
        fap, _ = period_fap(t, r, dec["obs_R"], float(tau_gp), t14, fr.duration_grid, p_min, p_max,
                            z_star=fr.z_star, block_len_multiple=fr.block_len_multiple,
                            n_surrogates=fr.B, rng=rng)
        out["fap"] = float(fap)
        if fap <= fr.alpha_fap:
            p_hat = dec["p_hat"]
            tls = _run_tls(t, 1.0 + r, max(p_min, p_hat * (1 - fr.epsilon)),
                           p_hat * (1 + fr.epsilon), fr.oversampling)
            out.update({k: tls[k] for k in ("sde", "period", "t0", "duration")})
            out["tls_mode"] = "targeted"
            return out
    tls = _run_tls(t, 1.0 + r, p_min, _pmax(t, fr), fr.oversampling)
    out.update({k: tls[k] for k in ("sde", "period", "t0", "duration")})
    out["tls_mode"] = "monotransit_fallback" if dec["monotransit"] else (
        "fallback_full" if not dec["fast_path_eligible"] else "fallback_weak_fap")
    return out
