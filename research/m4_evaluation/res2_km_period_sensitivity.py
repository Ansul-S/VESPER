"""RES-2 (Wave 1, audit remediation): KM-period-weighted E1 sensitivity.

The audit's #1 missing analysis. The sealed occurrence weight w_c (Seal #2 A.5) uses a
**log-uniform** period dimension w_P (each of {0.5,1,2,4,8,16} d gets 1/6) crossed with
the KM 2020 radius prior w_R. This script re-weights the *period* dimension by the actual
Kunimoto & Matthews (2020) occurrence model (their Eqn 22/25 broken power law, Table 7),
per radius bin, and recomputes the E1 estimand ΔR̄ and all three one-sided 95% lower
bounds (injection bootstrap, host-cluster bootstrap, Wilson-weighted combination) — so
the E1 PASS is tested against the weighting the audit flagged, not only the sealed one.

KM period model (Table 7; df/dlogP ∝ P^α/(1+(P/P0)^γ), α=β+γ):
  1-2 R+ : β=-0.5, γ=2.42, P0=5.9 d   (α=1.92)
  2-4 R+ : β=-0.1, γ=2.30, P0=13.3 d  (α=2.20)
KM's larger bins (4-8, 8-16 R+) are not power-law-cutoff-describable (KM §7); following
the sealed A.5 convention, giant nodes (R4/R8/R12) reuse the 2-4 R+ period shape
(they carry <8% of the radius weight, so the choice is negligible).

P=0.5 d is below KM's 0.78 d support (A.6 note). Handled two ways, both reported:
  - EXTRAPOLATED : evaluate the power law at P=0.5 d anyway (extrapolate below support);
  - EXCL-P0.5    : drop the P=0.5 node (period weights renormalized over {1,2,4,8,16}).

w_R (radius) is held at the sealed KM values; only the period dimension changes. Analysis
only, on the sealed recovery.csv — no new TEST read; no sealed artifact is edited.

Run:  .venv/bin/python research/m4_evaluation/res2_km_period_sensitivity.py
Out:  data/manifests/m4/wave1/res2_km_period_sensitivity.{json,md}
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RECOVERY = "data/manifests/m4/test_run/recovery.csv"
SEALED_CORE = "data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json"
OUT = Path("data/manifests/m4/wave1")
MARGIN = -0.02
PERIODS = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
Z95 = 1.6448536269514722

# KM 2020 Table 7 period-shape parameters, keyed by radius node (giants reuse 2-4 shape).
KM_BETA_GAMMA_P0 = {
    1:  (-0.5, 2.42, 5.9),    # 1-2 R+ bin
    2:  (-0.1, 2.30, 13.3),   # 2-4 R+ bin
    4:  (-0.1, 2.30, 13.3),   # 4-8  -> 2-4 shape (A.5 convention)
    8:  (-0.1, 2.30, 13.3),   # 8-16 -> 2-4 shape
    12: (-0.1, 2.30, 13.3),   # 8-16 -> 2-4 shape
}


def _wkey(P, R):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(R)}"


def km_dfdlogP(P, R):
    """KM 2020 Eqn 22 broken power law df/dlogP ∝ P^α/(1+(P/P0)^γ), α=β+γ."""
    beta, gamma, P0 = KM_BETA_GAMMA_P0[int(R)]
    alpha = beta + gamma
    return P ** alpha / (1.0 + (P / P0) ** gamma)


def build_weights(w_R, mode):
    """Return a w_c dict over all 30 (P,R) cells. mode in {sealed, km_extrap, km_excl}.
    w_R is the sealed radius prior; the period dimension is per-radius KM (or log-uniform)."""
    radii = sorted(int(r.lstrip("R")) for r in w_R)
    wc = {}
    for R in radii:
        if mode == "sealed":
            wP = {P: 1.0 / len(PERIODS) for P in PERIODS}                 # log-uniform
        else:
            nodes = PERIODS if mode == "km_extrap" else PERIODS[1:]       # excl drops 0.5
            raw = {P: km_dfdlogP(P, R) for P in nodes}
            s = sum(raw.values())
            wP = {P: (raw.get(P, 0.0) / s) for P in PERIODS}             # 0 for dropped nodes
        for P in PERIODS:
            wc[_wkey(P, R)] = w_R[f"R{R}"] * wP[P]
    return wc


# ---- estimand + three interval constructions (mirror e1_corrected_inference.py) --------
def point_estimate(df, w):
    return float(sum(w[_wkey(P, R)] * (sub.rec_comb.mean() - sub.rec_tls.mean())
                     for (P, R), sub in df.groupby(["period_days", "radius_rearth"])))


def injection_bootstrap(df, w, B=2000, seed=20260616):
    rng = np.random.default_rng(seed)
    cells = {(P, R): (sub.rec_comb.to_numpy(float), sub.rec_tls.to_numpy(float), w[_wkey(P, R)])
             for (P, R), sub in df.groupby(["period_days", "radius_rearth"])}
    boots = np.empty(B)
    for b in range(B):
        v = 0.0
        for rc, rt, wc in cells.values():
            if wc == 0.0:
                continue
            idx = rng.integers(0, rc.size, rc.size)
            v += wc * (rc[idx].mean() - rt[idx].mean())
        boots[b] = v
    return float(np.percentile(boots, 5))


def cluster_bootstrap(df, w, B=2000, seed=20260616):
    rng = np.random.default_rng(seed)
    hosts = df.tic.unique()
    by_host = {h: df[df.tic == h] for h in hosts}
    boots = np.empty(B)
    for b in range(B):
        s = pd.concat([by_host[h] for h in rng.choice(hosts, hosts.size, replace=True)])
        v = 0.0
        for (P, R), sub in s.groupby(["period_days", "radius_rearth"]):
            wc = w[_wkey(P, R)]
            if wc:
                v += wc * (sub.rec_comb.mean() - sub.rec_tls.mean())
        boots[b] = v
    return float(np.percentile(boots, 5))


def wilson_combination(df, w, z=Z95):
    point, var = 0.0, 0.0
    for (P, R), sub in df.groupby(["period_days", "radius_rearth"]):
        wc = w[_wkey(P, R)]
        if wc == 0.0:
            continue
        d = (sub.rec_comb.astype(float) - sub.rec_tls.astype(float)).to_numpy()
        n = d.size
        point += wc * d.mean()
        var += (wc ** 2) * (np.var(d, ddof=1) if n > 1 else 0.25) / n
    return float(point), float(point - z * np.sqrt(var))


def main():
    df = pd.read_csv(RECOVERY)
    df["tic"] = df["tic"].astype(str)
    core = json.load(open(SEALED_CORE))
    w_R = {f"R{k}": v for k, v in core["A5_occurrence_weights_wc"]["w_R_normalized"].items()}

    modes = {"sealed": "log-uniform w_P (sealed A.5)",
             "km_extrap": "KM Eqn-25 w_P, P=0.5 extrapolated below KM support",
             "km_excl": "KM Eqn-25 w_P, P=0.5 node excluded (renormalized)"}
    results = {}
    for mode, label in modes.items():
        w = build_weights(w_R, mode)
        pt = point_estimate(df, w)
        results[mode] = {
            "label": label,
            "delta_R_bar_pp": pt * 100,
            "injection_lo95_pp": injection_bootstrap(df, w) * 100,
            "cluster_lo95_pp": cluster_bootstrap(df, w) * 100,
            "wilson_lo95_pp": wilson_combination(df, w)[1] * 100,
            "period_weight_by_node": {f"P{P:g}": round(sum(w[_wkey(P, R)] for R in [1, 2, 4, 8, 12]), 5)
                                      for P in PERIODS},
        }
        results[mode]["pass_all_three"] = bool(
            min(results[mode]["injection_lo95_pp"], results[mode]["cluster_lo95_pp"],
                results[mode]["wilson_lo95_pp"]) > MARGIN * 100)

    all_pass = all(r["pass_all_three"] for r in results.values())
    summary = {
        "task": "RES-2 KM-period-weighted E1 sensitivity (Wave 1)",
        "source": "Kunimoto & Matthews 2020, Table 7 / Eqn 22-25 (arXiv:2004.05296)",
        "margin_pp": MARGIN * 100,
        "n_injections": int(len(df)),
        "n_hosts": int(df.tic.nunique()),
        "results": results,
        "conclusion": ("E1 PASS is robust to the period-weighting scheme: all three interval "
                       "constructions clear the -2 pp margin under sealed log-uniform AND KM "
                       "occurrence weighting (both P=0.5 handlings)." if all_pass else
                       "E1 is SENSITIVE to period weighting — the sealed log-uniform w_P flatters "
                       "the result; at least one KM-weighted lower bound breaches -2 pp. ESCALATE."),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "res2_km_period_sensitivity.json").write_text(json.dumps(summary, indent=2))

    # markdown table
    rows = ["# RES-2 — KM-period-weighted E1 sensitivity", "",
            f"Source: {summary['source']}. Margin: **{MARGIN*100:.0f} pp**. "
            f"n={summary['n_injections']} injections, {summary['n_hosts']} hosts. "
            "w_R held at sealed KM values; only the period dimension changes.", "",
            "| Weighting | ΔR̄ (pp) | injection lo95 | host-cluster lo95 | Wilson lo95 | PASS |",
            "|---|---|---|---|---|---|"]
    for mode, r in results.items():
        rows.append(f"| {r['label']} | {r['delta_R_bar_pp']:+.2f} | {r['injection_lo95_pp']:+.2f} | "
                    f"{r['cluster_lo95_pp']:+.2f} | {r['wilson_lo95_pp']:+.2f} | "
                    f"{'✅' if r['pass_all_three'] else '❌'} |")
    rows += ["", "**Period weight by node (summed over radius):**", "",
             "| scheme | " + " | ".join(f"P={P:g}" for P in PERIODS) + " |",
             "|---|" + "---|" * len(PERIODS)]
    for mode, r in results.items():
        rows.append(f"| {mode} | " + " | ".join(f"{r['period_weight_by_node'][f'P{P:g}']:.3f}"
                                                for P in PERIODS) + " |")
    rows += ["", f"**Conclusion.** {summary['conclusion']}"]
    (OUT / "res2_km_period_sensitivity.md").write_text("\n".join(rows) + "\n")

    print(json.dumps({m: {k: v for k, v in r.items() if k != "period_weight_by_node"}
                      for m, r in results.items()}, indent=2))
    print("\nCONCLUSION:", summary["conclusion"])


if __name__ == "__main__":
    main()
