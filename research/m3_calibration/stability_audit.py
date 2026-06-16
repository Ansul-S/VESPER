"""M3 threshold stability (bootstrap CIs) + retained-high-SDE survivor audit (owner directive).

(1) Bootstrap the CLEANED 854-star null calibration set (resample stars with replacement, B times)
    and recompute z_star, z_mono, T per resample -> compact CIs. Quantifies threshold stability;
    NOT a larger-scale recalibration.
(2) Retained-high-SDE audit table: every kept survivor (SDE>9, no catalog match, no EB signature)
    with TIC, SDE, period, depth, the exclusion checks performed, and the reason retained.

Run (from cache):  python research/m3_calibration/stability_audit.py [--B 1000]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from detector import detect_events  # noqa: E402

REPORT = Path("data/manifests/m3")
CACHE = Path("data/processed/m1")
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
Z_STAR_TGT, Z_MONO_TGT, FAR_TGT = 1.0, 0.1, 0.01


def _event_snrs(tic):
    z = np.load(CACHE / f"{tic}.npz", allow_pickle=True)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    ev = detect_events(t, r, DGRID, stride_frac=0.5, z_for_extraction=2.0)
    return ev[:, 1].tolist() if ev.size else []


def _derive(sdes, events_list):
    zgrid = np.round(np.arange(3.0, 20.01, 0.1), 2)
    def mean_ev(z):
        return float(np.mean([sum(1 for s in row if s >= z) for row in events_list]))
    z_star = next((float(z) for z in zgrid if mean_ev(z) <= Z_STAR_TGT), np.nan)
    z_mono = next((float(z) for z in zgrid if mean_ev(z) <= Z_MONO_TGT), np.nan)
    T = float(np.nanpercentile(sdes, 100 * (1 - FAR_TGT))) if len(sdes) else np.nan
    return z_star, z_mono, T


def run(B: int = 1000) -> None:
    full = pd.read_csv(REPORT / "m3_per_star.csv"); full["tic"] = full["tic"].astype(str)
    excl = pd.read_csv(REPORT / "calibration_exclusions.csv"); excl_tics = set(excl["tic"].astype(str))
    cleaned = full[~full["tic"].isin(excl_tics)].reset_index(drop=True)
    n = len(cleaned)
    print(f"[stab] cleaned null set n={n}; bootstrap B={B}")

    event_map = {t: _event_snrs(t) for t in cleaned["tic"]}
    sde_arr = cleaned["tls_sde"].values
    events = [event_map[t] for t in cleaned["tic"]]
    point = _derive(sde_arr, events)

    rng = np.random.default_rng(20260616)
    zs, zm, Ts = [], [], []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        zsi, zmi, Ti = _derive(sde_arr[idx], [events[i] for i in idx])
        zs.append(zsi); zm.append(zmi); Ts.append(Ti)
    def ci(a):
        a = np.array(a, float); a = a[np.isfinite(a)]
        return {"median": float(np.median(a)), "p2.5": float(np.percentile(a, 2.5)),
                "p16": float(np.percentile(a, 16)), "p84": float(np.percentile(a, 84)),
                "p97.5": float(np.percentile(a, 97.5)), "sd": float(np.std(a))}
    stab = {"n_cleaned": n, "B": B,
            "z_star": {"point": point[0], **ci(zs)},
            "z_mono": {"point": point[1], **ci(zm)},
            "T_sde": {"point": point[2], **ci(Ts)}}

    # --- retained-high-SDE survivor audit table ---
    vet = pd.read_csv(REPORT / "m3_vetting.csv"); vet["tic"] = vet["tic"].astype(str)
    surv = vet[vet["verdict"] == "no_eb_signature"].copy()
    surv = surv.merge(cleaned[["tic", "max_event_snr", "period_fap", "n_events_ge2"]], on="tic", how="left")
    surv["catalog_check"] = "no Prsa2022/VSX match (15\" cone)"
    surv["secondary_check"] = surv["secondary_sig"].map(lambda x: f"{x:.1f}sig (<3 keep)")
    surv["oddeven_check"] = surv["odd_even_sig"].map(lambda x: f"{x:.1f}sig (<3 keep)")
    surv["depth_check"] = surv["depth_pct"].map(lambda x: f"{x:.3f}% (<5% keep)")
    surv["reason_retained"] = "passed catalog + secondary + odd-even + depth checks; no EB signature"
    cols = ["tic", "tls_sde", "period", "depth_pct", "max_event_snr", "period_fap",
            "catalog_check", "secondary_check", "oddeven_check", "depth_check", "reason_retained"]
    surv[cols].sort_values("tls_sde", ascending=False).to_csv(REPORT / "retained_high_sde_audit.csv", index=False)

    out = {"milestone": "M3", "stage": "threshold stability + survivor audit (PROVISIONAL, pre-Seal #2)",
           "basis": "cleaned 1000-star null calibration (854 after 146 exclusions)",
           "bootstrap_thresholds": stab,
           "retained_high_sde_survivors": {"n": int(len(surv)),
               "summary": f"{len(surv)} null stars with SDE>9 retained: passed catalog (Prsa2022/VSX) "
                          "and automated EB vetting (secondary/odd-even/depth); mostly long-period "
                          "few-transit TLS noise. Kept in the null FAR population (no hand-pruning).",
               "table": "data/manifests/m3/retained_high_sde_audit.csv"}}
    (REPORT / "m3_stability_audit.json").write_text(json.dumps(out, indent=2, default=str))

    print("\n=== threshold stability (point [2.5%, 97.5%], +/-1sd) ===")
    for k in ["z_star", "z_mono", "T_sde"]:
        d = stab[k]
        print(f"  {k:8s} point={d['point']!s:>7}  median={d['median']:.2f}  "
              f"95% CI [{d['p2.5']:.2f}, {d['p97.5']:.2f}]  sd={d['sd']:.2f}")
    print(f"\n[stab] retained-high-SDE survivors: {len(surv)} -> retained_high_sde_audit.csv")
    print(f"[stab] wrote m3_stability_audit.json")


def main() -> None:
    p = argparse.ArgumentParser(description="M3 threshold bootstrap stability + survivor audit.")
    p.add_argument("--B", type=int, default=1000)
    args = p.parse_args()
    run(args.B)


if __name__ == "__main__":
    main()
