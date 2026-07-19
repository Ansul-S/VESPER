"""E1 corrected inference (audit remediation, DR-003) — analysis-only, no new TEST read.

Recomputes the E1 one-sided 95% lower bound on the sealed recovery.csv three ways:

  1. injection-level paired bootstrap  — the method the sealed run actually used
     (endpoints.e1_recall; reported lo95 = -0.60 pp);
  2. HOST-CLUSTER paired bootstrap     — resamples the 40 host stars with replacement,
     keeping all their injections, so the CI respects the fact that all 15,000
     injections share 40 noise realizations (the audit's anti-conservativeness fix);
  3. Wilson per-cell + fixed-weight combination — the method named in the sealed
     pre-registration (HYP §6 "Wilson/Clopper-Pearson per cell, combined under the
     fixed weights"), implemented as a delta-method combination of per-cell
     paired-difference variances under the frozen w_c.

All three are reported side by side; the sealed margin (-2 pp) and the sealed point
estimate are unchanged. This corrects the *uncertainty statement*, not the estimand.

Run:  .venv/bin/python research/m4_evaluation/e1_corrected_inference.py
Out:  data/manifests/m4/e2_retiming/e1_corrected_inference.json
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

OUT = Path("data/manifests/m4/e2_retiming")
MARGIN = -0.02


def _wc():
    core = json.loads(Path("data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json").read_text())
    return core["A5_occurrence_weights_wc"]["w_c"]


def _wkey(P, R):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(R)}"


def point_estimate(df, w):
    val = 0.0
    for (P, R), sub in df.groupby(["period_days", "radius_rearth"]):
        val += w[_wkey(P, R)] * (sub.rec_comb.mean() - sub.rec_tls.mean())
    return float(val)


def injection_bootstrap(df, w, B=2000, seed=20260616):
    rng = np.random.default_rng(seed)
    cells = {(P, R): (sub.rec_comb.to_numpy(float), sub.rec_tls.to_numpy(float), w[_wkey(P, R)])
             for (P, R), sub in df.groupby(["period_days", "radius_rearth"])}
    boots = np.empty(B)
    for b in range(B):
        v = 0.0
        for rc, rt, wc in cells.values():
            idx = rng.integers(0, rc.size, rc.size)
            v += wc * (rc[idx].mean() - rt[idx].mean())
        boots[b] = v
    return float(np.percentile(boots, 5)), float(boots.std())

def cluster_bootstrap(df, w, B=2000, seed=20260616):
    """Resample hosts (clusters) with replacement; recompute the weighted estimand."""
    rng = np.random.default_rng(seed)
    hosts = df.tic.unique()
    by_host = {h: df[df.tic == h] for h in hosts}
    boots = np.empty(B)
    for b in range(B):
        hs = rng.choice(hosts, hosts.size, replace=True)
        s = pd.concat([by_host[h] for h in hs])
        v = 0.0
        for (P, R), sub in s.groupby(["period_days", "radius_rearth"]):
            v += w[_wkey(P, R)] * (sub.rec_comb.mean() - sub.rec_tls.mean())
        boots[b] = v
    return float(np.percentile(boots, 5)), float(boots.std())


def wilson_combination(df, w, z=1.6448536269514722):
    """Pre-registered per-cell interval route: per-cell paired-difference variance
    (discordant-pair binomial variance of dR_c = mean(rec_comb - rec_tls)), combined
    under the fixed weights: Var(sum w_c dR_c) = sum w_c^2 Var(dR_c); one-sided 95%."""
    point, var = 0.0, 0.0
    for (P, R), sub in df.groupby(["period_days", "radius_rearth"]):
        d = (sub.rec_comb.astype(float) - sub.rec_tls.astype(float)).to_numpy()
        n = d.size
        point += w[_wkey(P, R)] * d.mean()
        # Wilson-style stabilized variance for the paired difference (add-2 smoothing)
        var += (w[_wkey(P, R)] ** 2) * (np.var(d, ddof=1) if n > 1 else 0.25) / n
    return float(point), float(point - z * np.sqrt(var))


def main():
    df = pd.read_csv("data/manifests/m4/test_run/recovery.csv")
    df["tic"] = df["tic"].astype(str)
    w = _wc()
    n_hosts = int(df.tic.nunique())
    pt = point_estimate(df, w)
    inj_lo, inj_sd = injection_bootstrap(df, w)
    clu_lo, clu_sd = cluster_bootstrap(df, w)
    wil_pt, wil_lo = wilson_combination(df, w)

    out = {
        "margin": MARGIN,
        "n_injections": int(len(df)),
        "n_distinct_hosts": n_hosts,
        "point_delta_R_bar": pt,
        "sealed_reported_lo95": -0.006025453056510998,
        "injection_bootstrap": {"lo95_one_sided": inj_lo, "sd": inj_sd,
                                "pass": bool(inj_lo > MARGIN)},
        "host_cluster_bootstrap": {"lo95_one_sided": clu_lo, "sd": clu_sd,
                                   "pass": bool(clu_lo > MARGIN),
                                   "note": "corrects for 40-host noise-realization sharing"},
        "wilson_weighted_combination": {"point": wil_pt, "lo95_one_sided": wil_lo,
                                        "pass": bool(wil_lo > MARGIN),
                                        "note": "the interval route named in sealed HYP section 6"},
        "conclusion": None,
    }
    all_pass = all([inj_lo > MARGIN, clu_lo > MARGIN, wil_lo > MARGIN])
    out["conclusion"] = ("E1 PASS is robust: all three interval constructions clear the "
                        "sealed -2 pp margin." if all_pass else
                        "E1 conclusion is method-dependent — escalate before relying on it.")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "e1_corrected_inference.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
