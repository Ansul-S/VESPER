"""M4 primary endpoints E1 (recall non-inferiority) and E2 (scoped compute).

E1 (VAL §4.1, §5): occurrence-weighted marginal completeness difference
    Delta_R_bar = sum_{c: n_tr>=2} w_c (R_comb,c - R_TLS,c),  w_c frozen (Seal #2 A.5).
    PASS iff lower bound of the one-sided 95% CI on Delta_R_bar > -2 pp.
    CI by paired injection bootstrap (B=1000, seed 20260616).

E2 (VAL §4, A.7): compute ratio (combined / full-TLS) on the FAST-PATH-ELIGIBLE
    population, rho_d (detector cost) included. PASS iff reduction >= 30% at non-inferior
    recall. Timing on a stratified representative subset, >=5 warm-cache repeats.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

DELTA_NI = -0.02            # -2 pp non-inferiority margin (VAL E1)
E2_MIN_REDUCTION = 0.30     # >=30% compute reduction (VAL E2)


def _wc_key(P, Rp):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(Rp)}"


def e1_recall(df: pd.DataFrame, w_c: dict, seed: int = 20260616, B: int = 1000) -> dict:
    """df rows: period_days, radius_rearth, n_transits, rec_comb (bool), rec_tls (bool)."""
    elig = df[df["n_transits"] >= 2].copy()
    cells = sorted({(float(P), int(R)) for P, R in zip(elig["period_days"], elig["radius_rearth"])})

    per_cell, point = [], 0.0
    for (P, R) in cells:
        sub = elig[(elig["period_days"] == P) & (elig["radius_rearth"] == R)]
        w = w_c.get(_wc_key(P, R), 0.0)
        Rc, Rt = float(sub["rec_comb"].mean()), float(sub["rec_tls"].mean())
        point += w * (Rc - Rt)
        per_cell.append({"P": P, "Rp": R, "n": int(len(sub)), "w_c": w,
                         "R_comb": Rc, "R_tls": Rt, "dR": Rc - Rt})

    # paired injection bootstrap within cells -> one-sided 95% lower bound on Delta_R_bar
    rng = np.random.default_rng(seed)
    boots = np.empty(B)
    cell_arrays = {(P, R): (
        elig[(elig["period_days"] == P) & (elig["radius_rearth"] == R)]["rec_comb"].to_numpy(float),
        elig[(elig["period_days"] == P) & (elig["radius_rearth"] == R)]["rec_tls"].to_numpy(float),
        w_c.get(_wc_key(P, R), 0.0)) for (P, R) in cells}
    for b in range(B):
        val = 0.0
        for (P, R), (rc, rt, w) in cell_arrays.items():
            if rc.size == 0:
                continue
            idx = rng.integers(0, rc.size, rc.size)   # paired resample (same idx both arms)
            val += w * (rc[idx].mean() - rt[idx].mean())
        boots[b] = val
    lo95 = float(np.percentile(boots, 5))             # one-sided 95% lower bound
    return {"delta_R_bar": float(point), "ci95_one_sided_lower": lo95,
            "pass": bool(lo95 > DELTA_NI), "margin": DELTA_NI, "n_cells": len(cells),
            "n_injections_eligible": int(len(elig)), "per_cell": per_cell,
            "bootstrap_B": B, "bootstrap_mean": float(boots.mean())}


def e2_compute(ledger: pd.DataFrame, recall_pass: bool) -> dict:
    """ledger rows (fast-path-eligible only): cost_full (Arm A s), cost_comb (Arm B s),
    cost_detector, cost_period, cost_tls. Combined = detector + period + tls."""
    el = ledger[ledger["fast_path_eligible"]].copy()
    if el.empty:
        return {"pass": False, "reason": "no fast-path-eligible stars", "n_eligible": 0}
    C_full = float(el["cost_full"].sum())
    C_comb = float(el["cost_comb"].sum())
    ratio = C_comb / C_full if C_full > 0 else float("nan")
    reduction = 1.0 - ratio
    rho_d = float(el["cost_detector"].sum() / C_full) if C_full > 0 else float("nan")
    f_p = float(el["cost_tls"].sum() / C_full) if C_full > 0 else float("nan")  # narrow/full search-cost frac
    pi_star = rho_d / f_p if f_p > 0 else float("nan")
    return {"n_eligible": int(len(el)), "C_full_s": C_full, "C_comb_s": C_comb,
            "compute_ratio": ratio, "reduction": reduction, "rho_d": rho_d,
            "f_p_search_frac": f_p, "pi_star_breakeven": pi_star,
            "reduction_target": E2_MIN_REDUCTION, "recall_non_inferior": bool(recall_pass),
            "pass": bool(reduction >= E2_MIN_REDUCTION and recall_pass),
            "per_stage_means_s": {"detector": float(el["cost_detector"].mean()),
                                  "period": float(el["cost_period"].mean()),
                                  "tls_comb": float(el["cost_tls"].mean()),
                                  "full_tls": float(el["cost_full"].mean())}}


def timing_subset(df_eligible: pd.DataFrame, per_cell_min: int = 10, cap: int = 300,
                  seed: int = 20260616) -> pd.Index:
    """Frozen subset-selection rule (PHASE1_M4_PLAN §6): stratified >=per_cell_min per
    occupied (P,Rp) cell (all if fewer), capped at `cap`, seed 20260616."""
    rng = np.random.default_rng(seed)
    picks = []
    for (P, R), grp in df_eligible.groupby(["period_days", "radius_rearth"]):
        idx = grp.index.to_numpy()
        take = idx if idx.size <= per_cell_min else rng.choice(idx, per_cell_min, replace=False)
        picks.extend(list(take))
    picks = np.array(picks)
    if picks.size > cap:
        picks = rng.choice(picks, cap, replace=False)
    return pd.Index(sorted(picks))
