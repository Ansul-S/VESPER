"""MATH-AUDIT — consolidate every reported number into one JSON + a printed digest.

Run after: surrogate_table.py nulls|injections, lambda_null.py, grid_identity.py,
surrogate_contamination.py.  Emits data/manifests/math_audit/findings.json.

Calibration only.  Nothing sealed is read for decision-making and nothing sealed is written.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).parent.parent.parent
OUT = REPO / "data/manifests/math_audit"
B = 1000
ALPHA = 0.01
P_MIN = 0.5


def fap(so, ss):
    return ((ss >= so[:, None]).sum(1) + 1) / (B + 1)


def stat(k, R, beta):
    return R * np.power(np.maximum(k, 1e-9), beta)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    F: dict = {"generated": pd.Timestamp.utcnow().isoformat(), "alpha_fap": ALPHA, "B": B}

    # ---------------------------------------------------------------- nulls
    nobs = pd.read_csv(OUT / "null_obs.csv")
    nz = np.load(OUT / "null_surrogates.npz")
    NK, NR = nz["k"].astype(float), nz["R"]
    cat = set(pd.read_csv(REPO / "data/manifests/m3/m3_null_cleaned_catalog.csv").tic.astype(int))
    nobs["cleaned"] = nobs.tic.astype(int).isin(cat)
    clean = nobs.cleaned.values
    fR = fap(nobs.obs_R.values, NR)
    nobs["fap"] = fR
    ko = nobs.k.values[:, None]
    Ro = nobs.obs_R.values[:, None]

    F["nulls"] = {
        "n_stars": int(len(nobs)), "n_cleaned": int(clean.sum()),
        "bit_identical_vs_INN3": json.loads((OUT / "verify_surrogate_table.json").read_text()),
    }

    # F1 — tail calibration
    tail = {}
    for pop, m in (("all", np.ones(len(nobs), bool)), ("cleaned", clean), ("excluded", ~clean)):
        row = {}
        for a in (0.01, 0.02, 0.05, 0.10, 0.25, 0.50):
            k = int((fR[m] <= a).sum())
            n = int(m.sum())
            row[str(a)] = {"obs": k, "exp": n * a, "ratio": k / (n * a),
                           "p_greater": float(stats.binomtest(k, n, a, alternative="greater").pvalue)}
        row["ks_vs_uniform"] = {"D": float(stats.kstest(fR[m], "uniform").statistic),
                                "p": float(stats.kstest(fR[m], "uniform").pvalue)}
        row["median_fap"] = float(np.median(fR[m]))
        tail[pop] = row
    F["F1_fap_calibration"] = tail

    # F2 — multiplicity dominance
    exc = NR >= Ro
    ge = exc.sum(1)
    lo = (exc & (NK < ko)).sum(1)
    lk, lr = np.log(NK.ravel()), np.log(np.maximum(NR.ravel(), 1e-12))
    g = (NK.ravel() >= 2) & (NR.ravel() > 0)
    sl, ic = np.polyfit(lk[g], lr[g], 1)
    dfv = pd.DataFrame({"lk": lk[g].round(3), "lr": lr[g]})
    between = dfv.groupby("lk").lr.transform("mean").var() / dfv.lr.var()
    F["F2_multiplicity"] = {
        "share_of_exceedances_from_fewer_event_surrogates": float(lo.sum() / ge.sum()),
        "by_k_obs": {lab: float(lo[m.values].sum() / max(ge[m.values].sum(), 1)) for lab, m in
                     (("k<=4", nobs.k <= 4), ("k5-8", nobs.k.between(5, 8)),
                      ("k9-12", nobs.k.between(9, 12)), ("k>=13", nobs.k >= 13))},
        "surrogate_law_logR_vs_logk": {"slope": float(sl), "intercept": float(ic),
                                       "theory_slope": -0.5,
                                       "corr": float(np.corrcoef(lk[g], lr[g])[0, 1])},
        "var_logR_between_k_frac": float(between),
        "surrogate_k_over_obs_k_median": float(np.median(NK.mean(1) / nobs.k.values)),
        "surrogate_k_rel_sd_median": float(np.median(NK.std(1) / nobs.k.values)),
    }

    # F3 — closed-form gate  W = k R^2 >= ln(N_eff/alpha)
    nobs["W"] = nobs.k * nobs.obs_R ** 2
    pmax = np.minimum(0.5 * nobs.baseline, nobs.obs_span)
    Neff = nobs.obs_span * (1 / P_MIN - 1 / pmax)
    nobs["Wstar"] = np.log(Neff / ALPHA)
    gate = ge <= 9
    pred = (nobs.W >= nobs.Wstar).values
    F["F3_closed_form_gate"] = {
        "Wstar_median": float(nobs.Wstar.median()),
        "Wstar_range": [float(nobs.Wstar.min()), float(nobs.Wstar.max())],
        "confusion": {"TP": int((pred & gate).sum()), "FP": int((pred & ~gate).sum()),
                      "FN": int((~pred & gate).sum()), "TN": int((~pred & ~gate).sum())},
        "accuracy": float((pred == gate).mean()),
        "auc_k": None, "note": "zero free parameters; N_eff = span*(1/p_min - 1/p_max)",
    }

    # ---------------------------------------------------------------- injections
    iobs = pd.read_csv(OUT / "inj_scored.csv")
    iz = np.load(OUT / "inj_surrogates.npz")
    IK, IR = iz["k"].astype(float), iz["R"]
    sc = iobs.seed_correct.values.astype(bool)
    target = float((fR[clean] <= ALPHA).mean())

    def calibrated(beta):
        fn = fap(stat(nobs.k.values.astype(float), nobs.obs_R.values, beta), stat(NK, NR, beta))
        fi = fap(stat(iobs.k.values.astype(float), iobs.obs_R.values, beta), stat(IK, IR, beta))
        s = np.sort(fn[clean])
        q = int(np.floor(target * len(s)))
        a = s[max(q - 1, 0)] if q > 0 else 0.0
        gi = fi <= a
        return {"alpha_star": float(a), "null_FAR": float((fn[clean] <= a).mean()),
                "gate_open": float(gi.mean()), "recall": float((gi & sc).mean())}

    fam = {str(b): calibrated(b) for b in (0.0, 0.2, 0.3, 0.406, 0.5, 0.7, 1.0, 1.5)}

    def cond_fap(ko_, Ro_, K, R):
        o = np.empty(len(ko_))
        for i in range(len(ko_)):
            m = K[i] == ko_[i]
            if m.sum() < 20:
                m = np.abs(K[i] - ko_[i]) <= max(1, 0.2 * ko_[i])
            o[i] = ((R[i][m] >= Ro_[i]).sum() + 1) / (m.sum() + 1) if m.sum() else 1.0
        return o
    fn = cond_fap(nobs.k.values.astype(float), nobs.obs_R.values, NK, NR)
    fi = cond_fap(iobs.k.values.astype(float), iobs.obs_R.values, IK, IR)
    s = np.sort(fn[clean]); q = int(np.floor(target * len(s)))
    a = s[max(q - 1, 0)] if q > 0 else 0.0
    fam["conditional_rank_exactly_pivotal"] = {
        "alpha_star": float(a), "null_FAR": float((fn[clean] <= a).mean()),
        "gate_open": float((fi <= a).mean()), "recall": float(((fi <= a) & sc).mean())}

    base = fam["0.0"]["recall"]
    for v in fam.values():
        v["delta_recall_pp"] = 100 * (v["recall"] - base)
    F["F4_statistic_family"] = {"target_null_FAR": target, "family": fam,
                                "n_injections": int(len(iobs))}

    # F5 — routing ceiling, measured vs predicted, by host baseline
    def ceil_pred(T):
        pm = 0.5 * T
        N = T * (1 / P_MIN - 1 / pm)
        return float(T / np.log(N / ALPHA)), float(N)
    per = {}
    for scl, gdf in iobs.groupby("sector_class"):
        m = gdf.groupby("P").gR.mean()
        lp, v = np.log(m.index.values), m.values
        cross = None
        for i in range(len(v) - 1):
            if v[i] >= 0.5 > v[i + 1]:
                cross = float(np.exp(lp[i] + (v[i] - 0.5) / (v[i] - v[i + 1]) * (lp[i + 1] - lp[i])))
                break
        T = float(gdf.baseline.median())
        pc, N = ceil_pred(T)
        per[scl] = {"T_base_median": T, "N_eff": N, "Wstar": float(np.log(N / ALPHA)),
                    "P_max_predicted": pc, "P50_measured": cross, "n": int(len(gdf)),
                    "gate_open_by_P": {str(k): float(x) for k, x in m.items()}}
    F["F5_routing_ceiling"] = per

    # F6 — subset region (dress rehearsal, calibration)
    dr = pd.read_csv(REPO / "data/manifests/m4/dress_rehearsal/recovery.csv")
    rec_fp = dr.confirmed_cheap.astype(bool) & dr.period_match.astype(bool) & dr.epoch_ok.astype(bool)
    nz_ = dr.period_days > 0.5
    F["F6_subset_region"] = {
        "all_cells": {"fast_path_recoveries": int(rec_fp.sum()),
                      "also_TLS": int((rec_fp & dr.rec_tls.astype(bool)).sum()),
                      "fast_path_only": int((rec_fp & ~dr.rec_tls.astype(bool)).sum())},
        "excluding_P0.5_grid_edge": {
            "fast_path_recoveries": int(rec_fp[nz_].sum()),
            "also_TLS": int((rec_fp[nz_] & dr[nz_].rec_tls.astype(bool)).sum()),
            "fast_path_only": int((rec_fp[nz_] & ~dr[nz_].rec_tls.astype(bool)).sum())},
        "routed_vs_P_corr_logP": float(np.corrcoef(np.log(dr.groupby("period_days").size().index),
                                                   dr.groupby("period_days").routed.mean())[0, 1]),
        "fapgate_vs_P_corr_logP": float(np.corrcoef(np.log(dr.groupby("period_days").size().index),
                                                    dr.groupby("period_days").fap_ok.mean())[0, 1]),
    }

    # F7 — Lambda null / confirmer
    lam = pd.read_csv(OUT / "lambda_null.csv")
    lam["aRs"] = lam.P / (np.pi * lam.T14)
    L = {}
    for kind, s in lam.groupby("kind"):
        L[kind] = {
            "n": int(len(s)), "P_delta_positive": float(s.sign_pass.mean()),
            "P_confirm_given_null_Tred0": float(s.confirmed_Tred0.mean()),
            "odd_even_pass": float(s.odd_even_pass.mean()),
            "no_secondary_pass": float(s.no_secondary_pass.mean()),
            "Lambda_q": {q: float(s.Lambda.quantile(q)) for q in (0.5, 0.9, 0.99)},
            "P_Lambda_ge": {str(t): float((s.Lambda >= t).mean()) for t in (3.84, 6.63, 25.0, 100.0)},
            "template_clamped_frac": float((s.aRs < 2.0).mean()),
        }
    r = lam[lam.kind == "random"]
    L["chi2_1_reference"] = {"q99": 6.63, "P_ge_25_nominal_half": float(0.5 * stats.chi2.sf(25, 1))}
    L["overdispersion_q99_ratio"] = float(r[r.sign_pass].Lambda.quantile(0.99) / 6.63)
    L["p99_by_T14"] = {str(t): float(g.Lambda.quantile(0.99)) for t, g in r.groupby("T14")}
    sd = lam[lam.kind == "seed"]
    L["T_red_for_FAR"] = {str(a): float(sd.Lambda.quantile(1 - a)) for a in (0.10, 0.05, 0.01)}
    F["F7_lambda_null"] = L

    # F8 — red-noise scaling
    rn = pd.read_csv(OUT / "red_noise_scaling.csv")
    F["F8_red_noise"] = {
        "n_stars": int(len(rn)), "acf1_median": float(rn.acf1.median()),
        "acf1_p90": float(rn.acf1.quantile(0.9)),
        "kappa": {c.split("_")[1]: {"median": float(rn[c].median()), "p75": float(rn[c].quantile(.75)),
                                    "p90": float(rn[c].quantile(.9)),
                                    "frac_gt_1.5": float((rn[c] > 1.5).mean())}
                  for c in rn.columns if c.startswith("kappa_")},
        "corr_acf1_kappa0.8": float(np.corrcoef(rn.acf1, rn["kappa_0.8"])[0, 1]),
    }

    # F9 — grid identity
    p = OUT / "grid_identity.csv"
    if p.exists():
        gi = pd.read_csv(p)
        d = gi.ge_fixed - gi.ge_own
        F["F9_grid_identity"] = {
            "n_stars": int(len(gi)),
            "median_abs_delta_ge": float(np.median(np.abs(d))),
            "mean_delta_ge": float(d.mean()),
            "frac_ge_changed": float((d != 0).mean()),
            "gate_flips": int((gi.gate_own != gi.gate_fixed).sum()),
            "gate_open_own": int(gi.gate_own.sum()), "gate_open_fixed": int(gi.gate_fixed.sum()),
        }
    # surrogate grid-size mismatch from the recorded table
    SNF = nz["nfreq"]
    F["F9_grid_identity"] = F.get("F9_grid_identity", {})
    F["F9_grid_identity"].update({
        "frac_surrogates_different_grid_size": float((SNF != nobs.obs_nfreq.values[:, None]).mean()),
        "frac_surrogates_fewer_trials": float((SNF < nobs.obs_nfreq.values[:, None]).mean()),
        "nfreq_ratio_p5_p50_p95": [float(np.percentile(SNF / np.maximum(nobs.obs_nfreq.values[:, None], 1), q))
                                   for q in (5, 50, 95)],
    })

    # F10 — surrogate contamination (MATH-3)
    p = OUT / "surrogate_contamination.csv"
    if p.exists():
        sc2 = pd.read_csv(p)
        r_ = sc2.fap_contaminated / sc2.fap_clean
        F["F10_surrogate_contamination"] = {
            "n": int(len(sc2)),
            "median_fap_contaminated": float(sc2.fap_contaminated.median()),
            "median_fap_clean": float(sc2.fap_clean.median()),
            "median_ratio_contaminated_over_clean": float(r_.median()),
            "frac_contaminated_smaller": float((sc2.fap_contaminated < sc2.fap_clean).mean()),
            "gate_open_contaminated": int(sc2.gate_contaminated.sum()),
            "gate_open_clean": int(sc2.gate_clean.sum()),
            "median_k_inj": float(sc2.k_inj.median()), "median_k_host": float(sc2.k_host.median()),
        }

    (OUT / "findings.json").write_text(json.dumps(F, indent=2, default=str))
    print(json.dumps(F, indent=2, default=str))


if __name__ == "__main__":
    main()
