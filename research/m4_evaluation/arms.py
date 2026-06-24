"""M4 dual-arm runner (VAL §2, §4) — shared sealed TLS engine, identical config both arms.

Arm A (baseline): full-grid TLS, SDE >= T.
Arm B (combined): detector -> routing (>= N_min events, or monotransit SNR1 >= z_mono)
                  -> period-from-spacing + block-bootstrap FAP -> targeted TLS on
                  [P_hat(1-eps), P_hat(1+eps)]; full-TLS fallback otherwise. SDE >= T.

The fairness keystone (A.1): both arms call the SAME TLS with the SAME oversampling and
period bounds; only the period *range* differs (full vs narrow). All thresholds come from
the Seal #2 FrozenThresholds — nothing here is tunable.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m3_calibration"))

from detector import detect_events                  # noqa: E402  (frozen detector)
from period_recovery import best_period, period_fap  # noqa: E402


def _run_tls(t, flux, period_min, period_max, oversampling):
    """Identical TLS call for both arms; also returns T0 + duration for the recovery predicate."""
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


def route(t, r, fr, tau_gp):
    """Detector + routing decision. Returns (events, decision_dict)."""
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    snrs = ev[:, 1] if ev.size else np.empty(0)
    n_ev = int(snrs.size)
    max_snr = float(snrs.max()) if n_ev else float("nan")
    multi = n_ev >= fr.n_min
    monotransit = (not multi) and n_ev >= 1 and max_snr >= fr.z_mono
    p_hat, obs_R, fap = np.nan, np.nan, np.nan
    if multi:
        baseline = float(np.max(t) - np.min(t))
        p_min, p_max = fr.period_min_days, fr.period_max_frac_baseline * baseline
        p_hat, _, obs_R = best_period(ev[:, 0], p_min, p_max, fr.oversampling)
    dec = {"n_events": n_ev, "max_event_snr": max_snr, "multi_event": multi,
           "monotransit": monotransit, "fast_path_eligible": bool(multi or monotransit),
           "p_hat": float(p_hat) if np.isfinite(p_hat) else None, "obs_R": float(obs_R) if np.isfinite(obs_R) else None}
    return ev, dec


def arm_b_combined(t, r, fr, tau_gp, rng):
    """Arm B: route -> targeted TLS (multi-event, period FAP ok) else full-TLS fallback."""
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
            tls = _run_tls(t, 1.0 + r, max(p_min, p_hat * (1 - fr.epsilon)), p_hat * (1 + fr.epsilon), fr.oversampling)
            out.update({k: tls[k] for k in ("sde", "period", "t0", "duration")})
            out["tls_mode"] = "targeted"
            return out
    # fallback: full TLS (monotransit, weak period evidence, or no evidence)
    tls = _run_tls(t, 1.0 + r, p_min, _pmax(t, fr), fr.oversampling)
    out.update({k: tls[k] for k in ("sde", "period", "t0", "duration")})
    out["tls_mode"] = "monotransit_fallback" if dec["monotransit"] else (
        "fallback_full" if not dec["fast_path_eligible"] else "fallback_weak_fap")
    return out
