"""RES-3 (Wave 1): epoch-tolerance sensitivity of E1.

Quantifies how much of E1's recall structure is the choice of the +/-0.5 T14 epoch
predicate (VAL §4.1 / recovery.py). 80% of the combined arm's losses are
right-period/wrong-epoch (paper §3.2), so the predicate tolerance is a lever.

DATA LIMITATION (honest scope): the sealed recovery.csv stores the COMBINED arm's
seed epoch error (`epoch_err_t14`, from the detector-seeded ephemeris) but NOT Arm A's
(TLS) per-injection epoch error — only the boolean `rec_tls`. So this script varies the
epoch tolerance on the COMBINED side only (rec_comb), holding rec_tls fixed. That makes
the resulting ΔR̄(tol) an UPPER BOUND on the true *symmetric* improvement: a fair
loosening would also let TLS recover its own wrong-epoch cases (e.g. the P=0.5 d gains,
which the edge control showed are TLS epoch failures — erratum §6), lowering rec_tls's
disadvantage. The symmetric sweep requires re-running to capture TLS epoch errors
(a compute task; queued alongside RES-4/RES-6). What is fully answered here from stored
data: the loss reclassification (how many losses the combined predicate creates at each
tolerance) and the combined-side ΔR̄ curve.

rec_comb recomputation (matches m4_driver):
  confirmed-cheap rows: rec_comb(tol) = period_match AND (epoch_err_t14 <= tol)
  fallback rows:        rec_comb       = rec_tls (TLS epoch not stored; unchanged)

Analysis only on the sealed recovery.csv; no new TEST read; no sealed artifact edited.

Run:  .venv/bin/python research/m4_evaluation/res3_epoch_tolerance_sensitivity.py
Out:  data/manifests/m4/wave1/res3_epoch_tolerance_sensitivity.{json,md}
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
SEALED_TOL = 0.5
TOLS = [0.5, 0.625, 0.75, 0.875, 1.0]


def _wkey(P, R):
    pk = f"P{P:g}" if float(P) != 0.5 else "P0.5"
    return f"{pk}_R{int(R)}"


def _wc():
    return json.load(open(SEALED_CORE))["A5_occurrence_weights_wc"]["w_c"]


def rec_comb_at(df, tol):
    """Recompute rec_comb at combined-arm epoch tolerance `tol` (TLS held fixed)."""
    cheap = df["confirmed_cheap"].astype(bool)
    ep_ok = np.isfinite(df["epoch_err_t14"]) & (df["epoch_err_t14"] <= tol)
    rc_cheap = df["period_match"].astype(bool) & ep_ok
    return np.where(cheap, rc_cheap, df["rec_tls"].astype(bool))


def weighted_dR(df, rec_comb, w):
    tmp = df.assign(_rc=np.asarray(rec_comb, bool))
    val = 0.0
    for (P, R), sub in tmp.groupby(["period_days", "radius_rearth"]):
        val += w[_wkey(P, R)] * (sub._rc.mean() - sub.rec_tls.mean())
    return float(val)


def cluster_lo95(df, tol, w, B=2000, seed=20260616):
    rng = np.random.default_rng(seed)
    d = df.assign(_rc=rec_comb_at(df, tol).astype(bool))
    d["tic"] = d["tic"].astype(str)
    hosts = d.tic.unique()
    by_host = {h: d[d.tic == h] for h in hosts}
    boots = np.empty(B)
    for b in range(B):
        s = pd.concat([by_host[h] for h in rng.choice(hosts, hosts.size, replace=True)])
        v = 0.0
        for (P, R), sub in s.groupby(["period_days", "radius_rearth"]):
            v += w[_wkey(P, R)] * (sub._rc.mean() - sub.rec_tls.mean())
        boots[b] = v
    return float(np.percentile(boots, 5))


def main():
    df = pd.read_csv(RECOVERY)
    df["tic"] = df["tic"].astype(str)
    w = _wc()

    # validation: rec_comb at the sealed 0.5 T14 must reproduce the stored column
    repro = rec_comb_at(df, SEALED_TOL)
    assert (repro == df["rec_comb"].astype(bool)).all(), \
        "rec_comb recomputation at 0.5 T14 does not match the sealed column"

    # loss reclassification (losses = rec_tls=1, rec_comb=0 at the sealed tolerance)
    loss = df[df.outcome_vs_armA == "loss"]
    reclass = {"n_losses": int(len(loss)),
               "right_period": int(loss.period_match.sum()),
               "wrong_period": int((~loss.period_match.astype(bool)).sum())}
    for tol in TOLS:
        rp = loss[loss.period_match.astype(bool)]
        reclass[f"losses_recovered_at_{tol}"] = int(
            (np.isfinite(rp.epoch_err_t14) & (rp.epoch_err_t14 <= tol)).sum())

    # ΔR̄(tolerance) curve — occurrence-weighted, combined-side
    curve = {}
    for tol in TOLS:
        rc = rec_comb_at(df, tol)
        curve[str(tol)] = {
            "delta_R_bar_pp": weighted_dR(df, rc, w) * 100,
            "cluster_lo95_pp": cluster_lo95(df, tol, w) * 100,
            "rec_comb_unweighted": float(np.mean(rc)),
            "n_recovered_combined": int(np.sum(rc)),
        }

    summary = {
        "task": "RES-3 epoch-tolerance sensitivity (Wave 1)",
        "scope": "COMBINED-side only (TLS per-injection epoch not stored); ΔR̄ curve is an "
                 "upper bound on the symmetric improvement. Symmetric sweep = compute task.",
        "margin_pp": MARGIN * 100,
        "sealed_tolerance_T14": SEALED_TOL,
        "gains_total": int((df.outcome_vs_armA == "gain").sum()),
        "gains_at_P0.5": int(((df.outcome_vs_armA == "gain") & (df.period_days == 0.5)).sum()),
        "loss_reclassification": reclass,
        "delta_R_bar_curve": curve,
        "conclusion": (
            f"E1's loss structure is dominated by the +/-0.5 T14 epoch predicate: all "
            f"{reclass['n_losses']} losses are confirmed-cheap seeds, {reclass['right_period']} "
            f"right-period; loosening the combined epoch tolerance to 0.75/1.0 T14 recovers "
            f"{reclass['losses_recovered_at_0.75']}/{reclass['losses_recovered_at_1.0']} of them, "
            f"lifting the combined-side ΔR̄ from {curve['0.5']['delta_R_bar_pp']:+.2f} pp to "
            f"{curve['1.0']['delta_R_bar_pp']:+.2f} pp. The losses are a predicate/epoch-precision "
            f"artifact, not a detection-power gap — motivating an epoch-refit confirmer (INN-4). "
            f"A fair symmetric sweep (needs stored TLS epochs) would recover TLS's own wrong-epoch "
            f"cases too (the P=0.5 d gains), so these are upper bounds."),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "res3_epoch_tolerance_sensitivity.json").write_text(json.dumps(summary, indent=2))

    rows = ["# RES-3 — Epoch-tolerance sensitivity of E1", "",
            f"**Scope:** {summary['scope']}", "",
            "## ΔR̄ vs combined-arm epoch tolerance (occurrence-weighted, sealed w_c)", "",
            "| tolerance (T14) | ΔR̄ (pp) | host-cluster lo95 (pp) | combined recall (unwtd) |",
            "|---|---|---|---|"]
    for tol in TOLS:
        c = curve[str(tol)]
        rows.append(f"| ±{tol} | {c['delta_R_bar_pp']:+.2f} | {c['cluster_lo95_pp']:+.2f} | "
                    f"{c['rec_comb_unweighted']:.4f} |")
    rows += ["", "## Loss reclassification (losses = TLS-recovered, combined-missed at ±0.5)", "",
             f"- Total losses: **{reclass['n_losses']}** — {reclass['right_period']} right-period, "
             f"{reclass['wrong_period']} wrong-period (epoch tolerance cannot recover wrong-period).",
             "", "| loosen tolerance to | right-period losses recovered |", "|---|---|"]
    for tol in TOLS:
        rows.append(f"| ±{tol} T14 | {reclass[f'losses_recovered_at_{tol}']} |")
    rows += ["", f"Gains: {summary['gains_total']} total, {summary['gains_at_P0.5']} at P=0.5 d "
             "(TLS epoch failures per the edge control, erratum §6).",
             "", f"**Conclusion.** {summary['conclusion']}"]
    (OUT / "res3_epoch_tolerance_sensitivity.md").write_text("\n".join(rows) + "\n")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
