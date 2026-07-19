"""M4 primary endpoints E1 (recall non-inferiority) and E2 (scoped compute).

E1 (VAL §4.1, §5): occurrence-weighted marginal completeness difference
    Delta_R_bar = sum_{c: n_tr>=2} w_c (R_comb,c - R_TLS,c),  w_c frozen (Seal #2 A.5).
    PASS iff lower bound of the one-sided 95% CI on Delta_R_bar > -2 pp.
    CI by paired injection bootstrap; a host-cluster bootstrap is reported alongside
    when a `tic` column is present (audit 2026-07-19: injections share host noise
    realizations, so the injection-level CI alone is anti-conservative).

E2 (VAL §4, A.7, §5): compute ratio (combined / full-TLS) on the FAST-PATH-ELIGIBLE
    population, rho_d (detector + period-FAP cost) included. Decision is taken on the
    CI, not the point estimate (audit 2026-07-19 — the sealed run reported a 12-star
    point estimate with no interval, which VAL §5's own INCONCLUSIVE clause requires):
      PASS         if the CI upper bound on the ratio <= 0.70 (and E1 non-inferior),
      FAIL         if the CI lower bound on the ratio  > 0.70,
      INCONCLUSIVE otherwise (CI straddles the sealed 0.70 threshold).

pi* (break-even prevalence, MATH §8.3a): pi* = rho_d / (f_p (1 - rho)), where f_p is
    the fraction of planet hosts that actually take the cheap path (confirmed-cheap),
    NOT a cost fraction. The sealed run's `pi_star_breakeven` (rho_d / search-cost
    fraction = 0.236) conflated the two; both are now reported under honest names.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

DELTA_NI = -0.02            # -2 pp non-inferiority margin (VAL E1)
E2_MIN_REDUCTION = 0.30     # >=30% compute reduction (VAL E2)
E2_MAX_RATIO = 1.0 - E2_MIN_REDUCTION


def _wc_key(P, Rp):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(Rp)}"


def e1_recall(df: pd.DataFrame, w_c: dict, seed: int = 20260616, B: int = 1000) -> dict:
    """df rows: period_days, radius_rearth, n_transits, rec_comb (bool), rec_tls (bool),
    optionally tic (enables the host-cluster bootstrap)."""
    elig = df[df["n_transits"] >= 2].copy()
    cells = sorted({(float(P), int(R)) for P, R in zip(elig["period_days"], elig["radius_rearth"])})
    missing = [(P, R) for (P, R) in cells if _wc_key(P, R) not in w_c]
    if missing:
        raise KeyError(f"e1_recall: eligible cells missing from frozen w_c "
                       f"(silent zero-weighting is forbidden): {missing}")

    per_cell, point = [], 0.0
    for (P, R) in cells:
        sub = elig[(elig["period_days"] == P) & (elig["radius_rearth"] == R)]
        w = w_c[_wc_key(P, R)]
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
        w_c[_wc_key(P, R)]) for (P, R) in cells}
    for b in range(B):
        val = 0.0
        for (P, R), (rc, rt, w) in cell_arrays.items():
            if rc.size == 0:
                continue
            idx = rng.integers(0, rc.size, rc.size)   # paired resample (same idx both arms)
            val += w * (rc[idx].mean() - rt[idx].mean())
        boots[b] = val
    lo95 = float(np.percentile(boots, 5))             # one-sided 95% lower bound

    out = {"delta_R_bar": float(point), "ci95_one_sided_lower": lo95,
           "pass": bool(lo95 > DELTA_NI), "margin": DELTA_NI, "n_cells": len(cells),
           "n_injections_eligible": int(len(elig)), "per_cell": per_cell,
           "bootstrap_B": B, "bootstrap_mean": float(boots.mean())}

    # host-cluster bootstrap (respects shared noise realizations across injections)
    if "tic" in elig.columns:
        hosts = elig["tic"].astype(str).unique()
        by_host = {h: elig[elig["tic"].astype(str) == h] for h in hosts}
        cboots = np.empty(B)
        for b in range(B):
            hs = rng.choice(hosts, hosts.size, replace=True)
            s = pd.concat([by_host[h] for h in hs])
            v = 0.0
            for (P, R) in cells:
                sub = s[(s["period_days"] == P) & (s["radius_rearth"] == R)]
                if len(sub):
                    v += w_c[_wc_key(P, R)] * (sub["rec_comb"].mean() - sub["rec_tls"].mean())
            cboots[b] = v
        out["cluster_ci95_one_sided_lower"] = float(np.percentile(cboots, 5))
        out["cluster_pass"] = bool(out["cluster_ci95_one_sided_lower"] > DELTA_NI)
        out["n_hosts"] = int(hosts.size)
    return out


def e2_compute(ledger: pd.DataFrame, recall_pass: bool, B: int = 20000,
               seed: int = 20260616) -> dict:
    """ledger rows (fast-path-eligible only): cost_full (Arm A s), cost_comb (Arm B s),
    cost_detector, cost_period, cost_tls; optionally confirmed_cheap and tic.
    Combined = detector + period + tls. Decision on the bootstrap CI (see module doc)."""
    el = ledger[ledger["fast_path_eligible"]].copy()
    if el.empty:
        return {"decision": "INCONCLUSIVE", "pass": False,
                "reason": "no fast-path-eligible stars", "n_eligible": 0}
    C_full = float(el["cost_full"].sum())
    C_comb = float(el["cost_comb"].sum())
    ratio = C_comb / C_full if C_full > 0 else float("nan")
    reduction = 1.0 - ratio
    rho_d = float(el["cost_detector"].sum() / C_full) if C_full > 0 else float("nan")

    # bootstrap CI on the ratio of sums; cluster by host when tic present, else by row
    rng = np.random.default_rng(seed)
    if "tic" in el.columns and el["tic"].nunique() > 1:
        groups = [g for _, g in el.groupby(el["tic"].astype(str))]
        cluster = "host"
    else:
        groups = [el.iloc[[i]] for i in range(len(el))]
        cluster = "row"
    ratios = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, len(groups), len(groups))
        s = pd.concat([groups[i] for i in idx])
        cf = s["cost_full"].sum()
        ratios[b] = s["cost_comb"].sum() / cf if cf > 0 else np.nan
    lo, hi = (float(np.nanpercentile(ratios, 2.5)), float(np.nanpercentile(ratios, 97.5)))

    if hi <= E2_MAX_RATIO and recall_pass:
        decision = "PASS"
    elif lo > E2_MAX_RATIO:
        decision = "FAIL"
    else:
        decision = "INCONCLUSIVE"

    # pi* per MATH §8.3a: f_p = fraction of (planet-host) eligible stars taking the
    # cheap path end-to-end; rho = cheap-confirm cost fraction.
    out = {"n_eligible": int(len(el)), "C_full_s": C_full, "C_comb_s": C_comb,
           "compute_ratio": ratio, "reduction": reduction, "rho_d": rho_d,
           "ratio_ci95": [lo, hi], "ratio_ci_cluster": cluster, "bootstrap_B": B,
           "p_ratio_le_0p70": float(np.nanmean(ratios <= E2_MAX_RATIO)),
           "reduction_target": E2_MIN_REDUCTION, "recall_non_inferior": bool(recall_pass),
           "decision": decision, "pass": decision == "PASS",
           "search_cost_frac_legacy": float(el["cost_tls"].sum() / C_full) if C_full > 0 else float("nan"),
           "per_stage_means_s": {"detector": float(el["cost_detector"].mean()),
                                 "period": float(el["cost_period"].mean()),
                                 "tls_comb": float(el["cost_tls"].mean()),
                                 "full_tls": float(el["cost_full"].mean())}}
    if "confirmed_cheap" in el.columns:
        f_p = float(el["confirmed_cheap"].mean())
        cheap = el[el["confirmed_cheap"]]
        rho = float(cheap["cost_tls"].sum() / C_full) if len(cheap) and C_full > 0 else 0.0
        out["f_p_cheap_path"] = f_p
        out["pi_star_breakeven"] = rho_d / (f_p * (1.0 - rho)) if f_p > 0 else float("inf")
        out["pi_star_note"] = ("MATH §8.3a definition (rho_d / f_p(1-rho)); the sealed run's "
                               "0.236 used a search-cost fraction for f_p and understated pi*.")
    return out


def timing_subset(df_eligible: pd.DataFrame, per_cell_min: int = 10, cap: int = 300,
                  seed: int = 20260616) -> pd.Index:
    """Frozen subset-selection rule (PHASE1_M4_PLAN §6): stratified >=per_cell_min per
    occupied (P,Rp) cell (all if fewer), capped at `cap`, seed 20260616.
    NOTE (audit 2026-07-19): the sealed TEST run invoked this with per_cell_min=2 and
    cap=12 via the driver defaults, in deviation from the frozen rule above; the
    defaults here now match the frozen rule."""
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
