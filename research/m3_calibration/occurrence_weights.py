"""M3 Decision F — instantiate the FROZEN occurrence weights w_c (A.5) and prevalence pi_hat (A.6)
from the sealed Kunimoto & Matthews (2020) framework. NOT calibration-tuned; computed from the
frozen formula + grid + the M0 stellar sample. Feeds E1 weighting (M4) and E3 (M5). Recorded for
the Seal #2 manifest. PROVISIONAL until owner review (NO Seal #2 here).

Sources (Kunimoto & Matthews 2020, AJ 159, 248; arXiv:2004.05296):
  * Table 5 — FGK occurrence marginalized over period, by radius bin (planets per star, %):
      P<50 d : 1-2 R+:16.2  2-4:25.2  4-8:1.6   8-16:1.6
      P<100 d: 1-2:18.1     2-4:35.4  4-8:3.1   8-16:2.6
  * Eqn 25 broken power law df/dlogP ~ P^alpha (P<<P0), P^beta (P>>P0):
      1-2 R+: alpha=1.9, beta=-0.5, P0=5.9 d
      2-4 R+: alpha=2.2, beta=-0.1, P0=13.3 d
      (4-8, 8-16: KM report a gradually-rising, non-cutoff form; we reuse the 2-4 shape as a
       documented approximation — giants carry <4% of the weight, so the effect is negligible.)
  * Table 3 star counts (FGK): F 40,010 / G 39,173 / K 17,097 (used only as provenance).

A.5 w_c = w_P(P) * w_R(R_p), normalized over the N_tr>=2 eligible cells.
  w_P : log-uniform over {0.5,1,2,4,8,16} d (powers of 2 -> equal weight per node).
  w_R : KM radius-occurrence at {1,2,4,8,12} R+ (each node -> its KM bin; 8 & 12 share KM's 8-16,
        split by geometric log sub-bin width -> documented assumption flagged for review).

A.6 pi_hat = (occurrence over grid (P,R) support) x (geometric <R*/a> for the target sample).

Run:  python research/m3_calibration/occurrence_weights.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

REPORT = Path("data/manifests/m3")
GRID_P = [0.5, 1, 2, 4, 8, 16]          # days
GRID_R = [1, 2, 4, 8, 12]               # R_earth

# --- KM 2020 inputs (frozen) ---
KM_RADIUS_BINS = {"1-2": (1, 2), "2-4": (2, 4), "4-8": (4, 8), "8-16": (8, 16)}
KM_OCC_P50 = {"1-2": 16.2, "2-4": 25.2, "4-8": 1.6, "8-16": 1.6}   # % per star, P<50 d (used: grid max 16 d)
KM_POWERLAW = {"1-2": (1.9, -0.5, 5.9), "2-4": (2.2, -0.1, 13.3),
               "4-8": (2.2, -0.1, 13.3), "8-16": (2.2, -0.1, 13.3)}  # (alpha,beta,P0); giants approx
KM_PMIN = 0.78125   # KM grid lower period bound


def _km_bin_for_radius(R):
    """KM coarse bin containing radius node R; returns bin key."""
    for k, (lo, hi) in KM_RADIUS_BINS.items():
        if lo <= R < hi:
            return k
    return "8-16"  # 12 R+ falls in 8-16


def _geom_split_8_16():
    """Split KM's 8-16 occurrence between nodes 8 and 12 by geometric log sub-bins within [8,16]."""
    mid = np.sqrt(8 * 12)                     # 9.80 -> boundary between node-8 and node-12 sub-bins
    w8 = np.log(mid / 8.0)                     # [8, 9.80]
    w12 = np.log(16.0 / mid)                   # [9.80, 16]
    tot = w8 + w12
    return w8 / tot, w12 / tot


def w_R():
    """KM radius-occurrence weight per grid radius node (un-normalized = occurrence in node's bin)."""
    f8, f12 = _geom_split_8_16()
    occ = {}
    for R in GRID_R:
        if R == 8:
            occ[R] = KM_OCC_P50["8-16"] * f8
        elif R == 12:
            occ[R] = KM_OCC_P50["8-16"] * f12
        else:
            occ[R] = KM_OCC_P50[_km_bin_for_radius(R)]
    return occ


def _period_frac(alpha, beta, P0, p_hi, p_lo=KM_PMIN):
    """Fraction of a radius bin's occurrence with period in [p_lo, p_hi], via smooth broken power law
    df/dlogP ∝ (P/P0)^alpha / (1 + (P/P0)^(alpha-beta)). Returns ∫_p_lo^p_hi / ∫_p_lo^50."""
    trapz = getattr(np, "trapezoid", None) or np.trapz
    lg = np.linspace(np.log(p_lo), np.log(50.0), 4000)
    P = np.exp(lg)
    dens = (P / P0) ** alpha / (1.0 + (P / P0) ** (alpha - beta))
    num = trapz(np.where(P <= p_hi, dens, 0.0), lg)
    den = trapz(dens, lg)
    return float(num / den)


def geometric_RstarOverA():
    """<R*/a> over the calibration target sample, averaged over the grid periods (log-uniform, = w_P).
    a/R* from stellar density: M* = g R*^2 / G (g=10^logg cgs); a=(G M* P^2/4pi^2)^(1/3)."""
    G = 6.674e-8                       # cgs
    Rsun, day = 6.957e10, 86400.0
    m = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    cal = m[m["split"] == "calibration"].copy()
    cal = cal[(cal["rad"] > 0) & np.isfinite(cal["logg"])]
    Rstar = cal["rad"].values * Rsun
    g = 10.0 ** cal["logg"].values
    Mstar = g * Rstar ** 2 / G
    vals = []
    for P in GRID_P:                   # log-uniform over periods
        a = (G * Mstar * (P * day) ** 2 / (4 * np.pi ** 2)) ** (1.0 / 3.0)
        vals.append(np.median(Rstar / a))
    return float(np.mean(vals)), int(len(cal))


def run() -> None:
    # --- w_c ---
    wR = w_R()
    sR = sum(wR.values())
    wR_norm = {R: wR[R] / sR for R in GRID_R}          # radius prior (normalized over 5 nodes)
    wP = {P: 1.0 / len(GRID_P) for P in GRID_P}         # log-uniform
    w_c = {}
    for P in GRID_P:
        for R in GRID_R:
            w_c[f"P{P}_R{R}"] = wP[P] * wR_norm[R]
    tot = sum(w_c.values())
    w_c = {k: v / tot for k, v in w_c.items()}          # normalized over 30 eligible cells

    # --- pi_hat ---
    # occurrence over grid (P,R) support: sum over radius bins of [P<50 marginal x frac(P in [0.78,16])]
    occ_grid_pct = 0.0
    fracs = {}
    for k, (a, b, P0) in KM_POWERLAW.items():
        fr = _period_frac(a, b, P0, p_hi=16.0)
        fracs[k] = fr
        occ_grid_pct += KM_OCC_P50[k] * fr
    occ_grid = occ_grid_pct / 100.0                     # planets per star, P in [0.78,16] d, R 1-16
    geom, n_cal = geometric_RstarOverA()
    pi_hat = occ_grid * geom

    out = {
        "milestone": "M3", "decision": "F — occurrence weights w_c (A.5) + prevalence pi_hat (A.6)",
        "status": "PROVISIONAL — owner review pending; NO Seal #2",
        "source": "Kunimoto & Matthews 2020 (AJ 159,248; arXiv:2004.05296): Table 5 (FGK, P<50 d) + Eqn 25 power law",
        "grid": {"P_days": GRID_P, "R_earth": GRID_R},
        "w_P_log_uniform": wP,
        "w_R_radius_prior": {
            "km_occurrence_pct_P50": KM_OCC_P50,
            "node_to_bin": {str(R): _km_bin_for_radius(R) for R in GRID_R},
            "split_8_16_geometric": {"node8_frac": _geom_split_8_16()[0], "node12_frac": _geom_split_8_16()[1],
                                     "assumption": "flat occurrence per log-radius within KM 8-16 bin"},
            "w_R_normalized": wR_norm},
        "w_c": w_c,
        "pi_hat": {"value": pi_hat,
                   "occurrence_over_grid_planets_per_star": occ_grid,
                   "period_fraction_Ple16_over_Plt50": fracs,
                   "geometric_RstarOverA_mean": geom, "n_calibration_stars": n_cal,
                   "integration_bounds": {"P_days": [KM_PMIN, 16.0], "R_earth": [1, 16],
                                          "note": "grid node P=0.5 d is below KM's 0.78 d support; occurrence integrated from 0.78 d"}},
        "assumptions_for_review": [
            "w_R uses KM Table 5 FGK P<50 d marginal (closest to grid max 16 d); P<100 d available as alt.",
            "nodes 8 & 12 R+ share KM's 8-16 bin -> split by geometric log sub-bin (giants <4% of weight).",
            "giant-planet period shape (4-8, 8-16) approximated by the 2-4 R+ power law (negligible effect)."],
    }
    REPORT.mkdir(parents=True, exist_ok=True)
    (REPORT / "m3_occurrence_weights.json").write_text(json.dumps(out, indent=2, default=str))

    print("=== w_R (radius prior, normalized) ===")
    for R in GRID_R:
        print(f"  R={R:>2} R+  ({_km_bin_for_radius(R)}):  w_R={wR_norm[R]:.4f}")
    print("\n=== w_c (30 cells; w_P=1/6 log-uniform x w_R) — by radius (sums over the 6 periods) ===")
    for R in GRID_R:
        s = sum(w_c[f"P{P}_R{R}"] for P in GRID_P)
        print(f"  R={R:>2}: per-cell {w_c[f'P0.5_R{R}']:.4f}  radius-summed {s:.4f}")
    print(f"\n  w_c sums to {sum(w_c.values()):.4f} over 30 cells")
    print(f"\n=== pi_hat ===")
    print(f"  occurrence over grid (P in [0.78,16] d, R 1-16): {occ_grid*100:.2f}% per star")
    print(f"  period fractions (P<=16 / P<50): " + ", ".join(f"{k}:{v:.2f}" for k, v in fracs.items()))
    print(f"  geometric <R*/a> (n={n_cal}): {geom:.4f}")
    print(f"  pi_hat = {pi_hat:.5f}  ({pi_hat*100:.3f}%)")
    print(f"\n[F] wrote m3_occurrence_weights.json")


if __name__ == "__main__":
    run()
