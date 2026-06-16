"""M3 period-from-spacing + block-bootstrap FAP (MATH §4, §9.1; VAL A.8), untrained.

Period recovery: given detector event epochs {t_j}, the spacings satisfy t_j - t_i = m_ij P
for a single strictly-periodic body (MATH §4 scope). We score a period grid by how well the
events phase-fold to a common epoch (integer-comb): for trial P, residual = min phase distance
of all events to the best common phase; the best P minimises folded scatter.

FAP: noise-model-aware CIRCULAR BLOCK BOOTSTRAP (MATH §9.1) — block length L_b = 3*max(tau_GP, T14)
(SEALED multiple). Generate B surrogate residual series, re-run detection + period scoring, and
take the FAP as the fraction of surrogates whose best period score >= the observed score.
"""

from __future__ import annotations

import numpy as np

from detector import detect_events


def _fold_score(epochs: np.ndarray, period: float) -> float:
    """Lower = tighter integer-comb fit. Phase scatter of events at this period."""
    if epochs.size < 2:
        return np.inf
    phase = (epochs / period) % 1.0
    # circular spread around the best common phase
    ang = 2 * np.pi * phase
    R = np.hypot(np.mean(np.cos(ang)), np.mean(np.sin(ang)))   # mean resultant length in [0,1]
    return 1.0 - R                                             # 0 = perfectly aligned


def best_period(epochs: np.ndarray, p_min: float, p_max: float, oversample: int = 3):
    """Integer-comb best period over [p_min, p_max]. Returns (P_hat, score, R)."""
    if epochs.size < 2:
        return np.nan, np.inf, 0.0
    span = float(epochs.max() - epochs.min())
    p_max = min(p_max, span) if span > 0 else p_max
    if p_max <= p_min:
        return np.nan, np.inf, 0.0
    # frequency grid; resolution ~ 1/(oversample*span)
    df = 1.0 / (oversample * max(span, p_max))
    freqs = np.arange(1.0 / p_max, 1.0 / p_min, df)
    if freqs.size == 0:
        return np.nan, np.inf, 0.0
    scores = np.array([_fold_score(epochs, 1.0 / f) for f in freqs])
    k = int(np.argmin(scores))
    return float(1.0 / freqs[k]), float(scores[k]), float(1.0 - scores[k])


def _circular_block_bootstrap(r: np.ndarray, block_len: int, rng) -> np.ndarray:
    n = r.size
    block_len = max(1, min(block_len, n))
    out = np.empty(n)
    filled = 0
    while filled < n:
        start = rng.integers(0, n)
        idx = (start + np.arange(block_len)) % n
        take = min(block_len, n - filled)
        out[filled:filled + take] = r[idx[:take]]
        filled += take
    return out


def period_fap(t, r, obs_R, tau_gp_days, t14_days, duration_grid, p_min, p_max,
               z_star, block_len_multiple, n_surrogates, rng):
    """Block-bootstrap FAP for the observed period alignment R (resultant length).

    Returns (fap, block_len_days). FAP = P(surrogate best-R >= observed R), Laplace-smoothed.
    """
    cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
    L_b_days = block_len_multiple * max(float(tau_gp_days), float(t14_days))
    block_len = max(1, int(round(L_b_days / cad)))
    ge = 0
    for _ in range(int(n_surrogates)):
        rs = _circular_block_bootstrap(r, block_len, rng)
        ev = detect_events(t, rs, duration_grid, z_for_extraction=z_star)
        Rs = best_period(ev[:, 0], p_min, p_max)[2] if ev.shape[0] >= 2 else 0.0
        if Rs >= obs_R:
            ge += 1
    fap = (ge + 1) / (int(n_surrogates) + 1)
    return float(fap), float(L_b_days)
