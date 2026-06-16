"""M3 recalibration on the CLEANED null subset (owner directive step 5).

Derives z_star, z_mono, T, alpha_FAP on the catalog+vetting-cleaned null calibration subset.
T and period-FAP reuse the per-star values from the full run (independent of which stars are
included); z_star/z_mono recompute detector events from cached residuals (fast, no TLS/network).
Compares BEFORE (185) vs AFTER (cleaned). PROVISIONAL — NO Seal #2 (review gate).

Run (from cache):  python research/m3_calibration/recalibrate.py
"""

from __future__ import annotations

import datetime
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
Z_STAR_TARGET, Z_MONO_TARGET, FAR_TARGET, ALPHA_FAP = 1.0, 0.1, 0.01, 0.01


def _event_snrs(tic):
    z = np.load(CACHE / f"{tic}.npz", allow_pickle=True)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    ev = detect_events(t, r, DGRID, stride_frac=0.5, z_for_extraction=2.0)
    return ev[:, 1].tolist() if ev.size else []


def _derive(per_star: pd.DataFrame, event_map: dict):
    def mean_events(z):
        return float(np.mean([sum(1 for s in event_map[t] if s >= z) for t in per_star["tic"]]))
    zgrid = np.round(np.arange(3.0, 20.01, 0.1), 2)
    z_star = next((float(z) for z in zgrid if mean_events(z) <= Z_STAR_TARGET), float("nan"))
    z_mono = next((float(z) for z in zgrid if mean_events(z) <= Z_MONO_TARGET), float("nan"))
    sde = per_star["tls_sde"].dropna().values
    T = float(np.nanpercentile(sde, 100 * (1 - FAR_TARGET))) if sde.size else float("nan")
    fap = per_star["period_fap"].dropna().values
    return {"n": len(per_star), "z_star": z_star, "z_mono": z_mono, "T_sde": T,
            "false_events_at_z_star": mean_events(z_star) if np.isfinite(z_star) else None,
            "false_events_at_z_mono": mean_events(z_mono) if np.isfinite(z_mono) else None,
            "alpha_fap_null_exceedance": float(np.mean(fap <= ALPHA_FAP)) if fap.size else None,
            "sde_median": float(np.nanmedian(sde)), "sde_max": float(np.nanmax(sde))}


def run() -> None:
    full = pd.read_csv(REPORT / "m3_per_star.csv"); full["tic"] = full["tic"].astype(str)
    excl = pd.read_csv(REPORT / "calibration_exclusions.csv"); excl_tics = set(excl["tic"].astype(str))
    cleaned = full[~full["tic"].isin(excl_tics)].copy()
    print(f"[recal] full={len(full)}  excluded={len(excl_tics)}  cleaned={len(cleaned)}")

    event_map = {t: _event_snrs(t) for t in full["tic"]}     # all, so both derivations share it
    before = _derive(full, event_map)
    after = _derive(cleaned, event_map)

    by_reason = excl.groupby("reason")["tic"].nunique().to_dict()

    # --- high-SDE survivor review set (kept; not excluded) ---
    SDE_HI = 9.0
    excl_reason = excl.assign(tic=excl["tic"].astype(str)).drop_duplicates("tic").set_index("tic")["reason"].to_dict()
    survivors = cleaned[cleaned["tls_sde"] > SDE_HI].sort_values("tls_sde", ascending=False).copy()
    survivors["retention_rationale"] = "no catalog match (Prsa2022/VSX) and no automated EB signature; " \
                                       "retained per owner directive — leverage reduced by sample scale"
    survivors[["tic", "tls_sde", "max_event_snr", "n_events_ge2", "period_fap", "retention_rationale"]] \
        .to_csv(REPORT / "high_sde_survivor_review_set.csv", index=False)

    # --- tail composition: who populates SDE>9 in the FULL sample ---
    hi = full[full["tls_sde"] > SDE_HI].copy()
    hi["category"] = hi["tic"].map(lambda t: excl_reason.get(t, "survivor_kept"))
    tail_comp = hi["category"].value_counts().to_dict()

    # --- T sensitivity to the highest-SDE survivors (report only; nothing removed) ---
    cl_sde = cleaned.dropna(subset=["tls_sde"]).sort_values("tls_sde", ascending=False)
    def T_drop_top(k):
        s = cl_sde["tls_sde"].values[k:]
        return float(np.nanpercentile(s, 100 * (1 - FAR_TARGET))) if s.size else float("nan")
    sensitivity = {"T_cleaned": after["T_sde"], "T_drop_top1": T_drop_top(1),
                   "T_drop_top3": T_drop_top(3), "T_drop_top5": T_drop_top(5),
                   "top5_survivor_sde": cl_sde["tls_sde"].head(5).round(2).tolist()}
    report = {
        "milestone": "M3", "stage": "recalibration on CLEANED null subset (PROVISIONAL — NO Seal #2)",
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "cleaning": {"m0_null_definition": "PRESERVED (TOI-removed); cleaned set is a derived M3 subset",
                     "excluded_stars": len(excl_tics), "by_reason": by_reason,
                     "exclusion_table": "data/manifests/m3/calibration_exclusions.csv"},
        "targets": {"z_star_false_events_per_lc": Z_STAR_TARGET, "z_mono_false_events_per_lc": Z_MONO_TARGET,
                    "far_per_star": FAR_TARGET, "alpha_fap": ALPHA_FAP},
        "before_raw": before, "after_cleaned": after,
        "tail_composition_sde_gt9": tail_comp,
        "T_sensitivity_to_top_survivors": sensitivity,
        "high_sde_survivors_kept": int(len(survivors)),
        "survivor_review_set": "data/manifests/m3/high_sde_survivor_review_set.csv",
        "note": f"{len(full)}-star cleaned null calibration. PROVISIONAL — NO Seal #2 until reviewed. "
                "Survivors retained per owner directive (leverage reduced by scale, not exclusion).",
    }
    (REPORT / "m3_thresholds_cleaned_PROVISIONAL.json").write_text(json.dumps(report, indent=2, default=str))
    print(f"\n=== BEFORE (raw {before['n']}) vs AFTER (cleaned {after['n']}) ===")
    for k in ["n", "z_star", "z_mono", "T_sde", "false_events_at_z_star", "false_events_at_z_mono",
              "alpha_fap_null_exceedance", "sde_median", "sde_max"]:
        print(f"  {k:28s} {before[k]!s:>12}  ->  {after[k]!s:>12}")
    print(f"\n  tail composition (SDE>9): {tail_comp}")
    print(f"  T sensitivity: cleaned={sensitivity['T_cleaned']:.2f}  drop-top1={sensitivity['T_drop_top1']:.2f}  "
          f"drop-top3={sensitivity['T_drop_top3']:.2f}  drop-top5={sensitivity['T_drop_top5']:.2f}")
    print(f"  top-5 survivor SDE: {sensitivity['top5_survivor_sde']}")
    print(f"  high-SDE survivors kept: {len(survivors)} -> high_sde_survivor_review_set.csv")
    print(f"\n[recal] wrote m3_thresholds_cleaned_PROVISIONAL.json")


if __name__ == "__main__":
    run()
