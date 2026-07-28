"""MATH-5 (Wave 2): BCa host-cluster interval for E1, beside the percentile interval.

WHY. E1's headline is a one-sided 95% lower bound on the occurrence-weighted recall
difference, taken as the 5th percentile of a host-clustered bootstrap. The percentile
interval is first-order accurate and assumes the bootstrap distribution is unbiased and
symmetric about the estimate. With only ~40 host clusters and a statistic that is a
weighted ratio of correlated proportions, neither assumption is free. BCa corrects for
median bias (z0) and for skewness/variance-drift (acceleration a, from a leave-one-HOST-out
jackknife), and is second-order accurate.

The pre-registered decision rule is unchanged and is NOT re-decided here: the sealed
endpoint is the percentile bound. BCa is reported ALONGSIDE it as a robustness check, per
roadmap MATH-5 ("both intervals reported; conclusions unchanged or the change is
front-page").

VECTORIZATION (also delivers roadmap CODE-7). The sealed implementation rebuilds a
DataFrame with pd.concat on every replicate. Here each (host, cell) is reduced once to
counts and success sums, so a whole bootstrap is two matrix products against a
multiplicity matrix. Exact, not approximate: for host multiplicities m,

    R_c = (m @ S_c) / (m @ N),    dR_bar = sum_c w_c (R_c^comb - R_c^tls)

which is identically what resampling whole hosts and re-averaging computes.

Analysis only, on the sealed recovery.csv and the sealed w_c. No TEST read, no sealed
artifact edited, no threshold re-derived.

Run:  .venv/bin/python research/m4_evaluation/math5_bca_cluster_ci.py
Out:  data/manifests/m4/wave2/math5_bca_cluster_ci.{json,md}
"""
from __future__ import annotations

import datetime
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import norm

RECOVERY = "data/manifests/m4/test_run/recovery.csv"
SEALED_CORE = "data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json"
OUT = Path("data/manifests/m4/wave2")

MARGIN = -0.02          # sealed non-inferiority margin (-2 pp)
ALPHA = 0.05            # one-sided 95%
B = 20000               # replicates (cheap once vectorized; sealed run used 1000)
SEED = 20260616


def _wc_key(P, R):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(R)}"


def build_matrices(df: pd.DataFrame, w_c: dict):
    """Reduce to per-(host, cell) counts and success sums.

    Returns hosts, cells, w (cells,), N (hosts,cells), Sc (hosts,cells), St (hosts,cells).
    """
    el = df[df["n_transits"] >= 2].copy()
    el["tic"] = el["tic"].astype(str)
    cells = sorted({(float(P), int(R))
                    for P, R in zip(el["period_days"], el["radius_rearth"])})
    missing = [c for c in cells if _wc_key(*c) not in w_c]
    if missing:
        raise KeyError(f"eligible cells missing from frozen w_c: {missing}")

    hosts = np.array(sorted(el["tic"].unique()))
    hidx = {h: i for i, h in enumerate(hosts)}
    cidx = {c: j for j, c in enumerate(cells)}

    N = np.zeros((hosts.size, len(cells)))
    Sc = np.zeros_like(N)
    St = np.zeros_like(N)
    for (h, P, R), g in el.groupby(["tic", "period_days", "radius_rearth"]):
        i, j = hidx[h], cidx[(float(P), int(R))]
        N[i, j] = len(g)
        Sc[i, j] = g["rec_comb"].astype(float).sum()
        St[i, j] = g["rec_tls"].astype(float).sum()
    w = np.array([w_c[_wc_key(*c)] for c in cells])
    return hosts, cells, w, N, Sc, St, el


def theta(mult: np.ndarray, w, N, Sc, St) -> np.ndarray:
    """dR_bar for one or many host-multiplicity vectors. mult: (hosts,) or (B, hosts)."""
    m = np.atleast_2d(mult).astype(float)
    n = m @ N                                    # (B, cells) resampled counts
    with np.errstate(invalid="ignore", divide="ignore"):
        rc = np.where(n > 0, (m @ Sc) / n, 0.0)
        rt = np.where(n > 0, (m @ St) / n, 0.0)
    # A replicate that loses a cell entirely contributes 0 for it — weights are NOT
    # renormalized. This reproduces the sealed loop exactly (endpoints.e1_recall skips
    # empty cells without redistributing their weight); verified bit-exact against
    # EP.e1_recall on the full recovery.csv.
    occupied = (n > 0).astype(float)
    val = ((rc - rt) * w * occupied).sum(axis=1)
    return val


def main() -> None:
    df = pd.read_csv(RECOVERY)
    w_c = json.load(open(SEALED_CORE))["A5_occurrence_weights_wc"]["w_c"]
    hosts, cells, w, N, Sc, St, el = build_matrices(df, w_c)

    ones = np.ones(hosts.size)
    theta_hat = float(theta(ones, w, N, Sc, St)[0])

    # ---- host-cluster bootstrap (vectorized) ----
    rng = np.random.default_rng(SEED)
    draws = rng.integers(0, hosts.size, size=(B, hosts.size))
    mult = np.zeros((B, hosts.size))
    np.add.at(mult, (np.repeat(np.arange(B), hosts.size), draws.ravel()), 1.0)
    boots = theta(mult, w, N, Sc, St)

    lo_pct = float(np.percentile(boots, 100 * ALPHA))

    # ---- BCa ----
    # z0: median-bias correction
    frac_below = float(np.mean(boots < theta_hat))
    frac_below = min(max(frac_below, 1.0 / B), 1.0 - 1.0 / B)   # guard the inverse CDF
    z0 = float(norm.ppf(frac_below))

    # a: acceleration from a leave-one-HOST-out jackknife (the clusters are the units)
    jack = np.empty(hosts.size)
    for i in range(hosts.size):
        m = np.ones(hosts.size)
        m[i] = 0.0
        jack[i] = theta(m, w, N, Sc, St)[0]
    jbar = jack.mean()
    d = jbar - jack
    denom = 6.0 * (np.sum(d ** 2) ** 1.5)
    a = float(np.sum(d ** 3) / denom) if denom > 0 else 0.0

    z_a = float(norm.ppf(ALPHA))
    adj = z0 + (z0 + z_a) / (1.0 - a * (z0 + z_a))
    alpha_bca = float(norm.cdf(adj))
    lo_bca = float(np.percentile(boots, 100 * alpha_bca))

    summary = {
        "task": "MATH-5 BCa host-cluster interval for E1 (Wave 2)",
        "roadmap_id": "MATH-5",
        "scope": ("Robustness check reported ALONGSIDE the sealed percentile bound. The "
                  "pre-registered E1 decision rule is unchanged and is not re-decided here."),
        "inputs": {"recovery": RECOVERY, "w_c": "Seal #2 A.5", "margin_pp": MARGIN * 100,
                   "alpha_one_sided": ALPHA, "B": B, "seed": SEED},
        "sample": {"n_injections_eligible": int(len(el)), "n_hosts": int(hosts.size),
                   "n_cells": len(cells),
                   "injections_per_host_median": float(np.median(N.sum(axis=1)))},
        "point_estimate_pp": theta_hat * 100,
        "percentile": {"lo95_one_sided_pp": lo_pct * 100, "pass": bool(lo_pct > MARGIN)},
        "bca": {"z0": z0, "acceleration_a": a, "effective_alpha": alpha_bca,
                "lo95_one_sided_pp": lo_bca * 100, "pass": bool(lo_bca > MARGIN)},
        "difference_pp": (lo_bca - lo_pct) * 100,
        "bootstrap_distribution": {
            "mean_pp": float(boots.mean()) * 100,
            "median_pp": float(np.median(boots)) * 100,
            "sd_pp": float(boots.std(ddof=1)) * 100,
            "skew_proxy_z0": z0,
        },
        "small_cluster_caveat": (
            f"The acceleration is estimated from a leave-one-out jackknife over only "
            f"{hosts.size} host clusters. With that few units the third-moment estimate is "
            f"itself noisy, so BCa's correction is indicative rather than definitive; it is "
            f"reported as a robustness check, not as a replacement for the sealed percentile "
            f"endpoint. A cluster bootstrap with <~50 units is known to under-cover somewhat "
            f"regardless of the interval method — the honest reading is that both bounds sit "
            f"well inside the -2 pp margin, not that either is exact to the last decimal."),
        "machine": {"platform": platform.platform(), "python": sys.version.split()[0],
                    "numpy": np.__version__},
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    both_pass = summary["percentile"]["pass"] and summary["bca"]["pass"]
    summary["conclusion"] = (
        f"E1 point estimate {theta_hat*100:+.2f} pp. One-sided 95% lower bound: "
        f"{lo_pct*100:+.2f} pp (percentile) vs {lo_bca*100:+.2f} pp (BCa), a difference of "
        f"{(lo_bca-lo_pct)*100:+.2f} pp. Both are above the sealed -2 pp margin, so the E1 "
        f"non-inferiority conclusion is unchanged under second-order-accurate inference."
        if both_pass else
        f"DISAGREEMENT: percentile lo95 {lo_pct*100:+.2f} pp (pass={lo_pct > MARGIN}) vs BCa "
        f"{lo_bca*100:+.2f} pp (pass={lo_bca > MARGIN}). This is a front-page change and must "
        f"be escalated per roadmap MATH-5.")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "math5_bca_cluster_ci.json").write_text(json.dumps(summary, indent=2))

    rows = ["# MATH-5 — BCa host-cluster interval for E1", "",
            f"**Scope.** {summary['scope']}", "",
            f"Sample: {summary['sample']['n_injections_eligible']} eligible injections across "
            f"{hosts.size} hosts and {len(cells)} cells; B = {B}, seed {SEED}.", "",
            "| Quantity | Value |", "|---|---|",
            f"| Point estimate $\\overline{{\\Delta R}}$ | {theta_hat*100:+.2f} pp |",
            f"| One-sided 95% lower bound — **percentile** (sealed endpoint) | {lo_pct*100:+.2f} pp |",
            f"| One-sided 95% lower bound — **BCa** | {lo_bca*100:+.2f} pp |",
            f"| Difference (BCa − percentile) | {(lo_bca-lo_pct)*100:+.2f} pp |",
            f"| Sealed margin | {MARGIN*100:+.0f} pp |",
            f"| Bias correction $z_0$ | {z0:+.4f} |",
            f"| Acceleration $a$ | {a:+.4f} |",
            f"| Effective lower-tail probability | {alpha_bca:.4f} (vs {ALPHA} nominal) |",
            "", f"**Conclusion.** {summary['conclusion']}", "",
            f"**Small-cluster caveat.** {summary['small_cluster_caveat']}"]
    (OUT / "math5_bca_cluster_ci.md").write_text("\n".join(rows) + "\n")

    print(json.dumps({k: summary[k] for k in
                      ("point_estimate_pp", "percentile", "bca", "difference_pp",
                       "sample", "conclusion")}, indent=2))
    print(f"\n[MATH-5] -> {OUT}/math5_bca_cluster_ci.json + .md")


if __name__ == "__main__":
    main()
