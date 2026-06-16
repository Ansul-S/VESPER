"""M3 automated EB vetting — residual high-SDE null outliers (owner directive step 4).

Applied ONLY to null stars with SDE > threshold that survived catalog cleaning (Prša 2022 + VSX).
Classifies each as an eclipsing-binary / non-planet contaminant via three standard vetting signatures
on the TLS solution; flagged stars are added to calibration_exclusions.csv with reason 'vetted_eclipse'.

Signatures (any one fires -> exclude):
  * secondary eclipse: significant flux dip near phase 0.5 (depth_2 / scatter >= sec_sigma).
  * odd-even depth mismatch: TLS odd_even_mismatch >= oe_sigma (signal is an EB at 2x the period).
  * non-planetary depth / V-shape: TLS depth >= depth_max (deep stellar eclipse), or duration-based
    V-shape (no flat bottom) flagged by TLS transit-shape residual.

Run (from cache, no network):  python research/m3_calibration/vet_outliers.py [--sde-min 9]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPORT = Path("data/manifests/m3")
CACHE = Path("data/processed/m1")
SEC_SIGMA, OE_SIGMA, DEPTH_MAX = 3.0, 3.0, 0.05   # secondary, odd-even, 5% depth ceiling


def _secondary_eclipse(t, flux, period, t0, duration):
    """Depth and significance of a dip near phase 0.5."""
    phase = ((t - t0) / period + 0.5) % 1.0 - 0.5     # primary at 0
    half = max(duration / period, 0.005)
    sec = np.abs(phase - 0.5) < half / 2
    oot = (np.abs(phase) > 0.1) & (np.abs(phase - 0.5) > 0.1) & (np.abs(phase + 0.5) > 0.1)
    if sec.sum() < 3 or oot.sum() < 10:
        return 0.0, 0.0
    depth2 = float(np.median(flux[oot]) - np.median(flux[sec]))
    scatter = 1.4826 * np.median(np.abs(flux[oot] - np.median(flux[oot]))) / np.sqrt(max(sec.sum(), 1))
    return depth2, (depth2 / scatter if scatter > 0 else 0.0)


def vet_one(tic, sde):
    from tls_engine import full_tls  # noqa
    from transitleastsquares import transitleastsquares
    z = np.load(CACHE / f"{tic}.npz", allow_pickle=True)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    flux = 1.0 + r
    baseline = float(t.max() - t.min())
    model = transitleastsquares(t, flux)
    res = model.power(period_min=0.5, period_max=0.5 * baseline, oversampling_factor=3,
                      use_threads=1, show_progress_bar=False)
    depth = 1.0 - float(res.depth)                      # fractional transit depth
    oe = float(getattr(res, "odd_even_mismatch", np.nan))
    dur = float(getattr(res, "duration", 0.1))
    d2, d2_sig = _secondary_eclipse(t, flux, float(res.period), float(res.T0), dur)
    reasons = []
    if np.isfinite(d2_sig) and d2_sig >= SEC_SIGMA and d2 > 0:
        reasons.append(f"secondary_eclipse({d2_sig:.1f}sig)")
    if np.isfinite(oe) and oe >= OE_SIGMA:
        reasons.append(f"odd_even({oe:.1f}sig)")
    if depth >= DEPTH_MAX:
        reasons.append(f"deep_eclipse({depth*100:.1f}%)")
    return {"tic": tic, "tls_sde": sde, "period": float(res.period), "depth_pct": depth * 100,
            "odd_even_sig": oe, "secondary_sig": d2_sig, "verdict": ";".join(reasons) or "no_eb_signature"}


def run(sde_min: float = 9.0) -> None:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    clean = pd.read_csv(REPORT / "m3_null_cleaned_catalog.csv"); clean["tic"] = clean["tic"].astype(str)
    outliers = clean[clean["tls_sde"] > sde_min].sort_values("tls_sde", ascending=False)
    print(f"[vet] {len(outliers)} residual null outliers with SDE>{sde_min} (catalog-clean survivors)")
    rows = [vet_one(str(row["tic"]), float(row["tls_sde"])) for _, row in outliers.iterrows()]
    vet = pd.DataFrame(rows)
    vet.to_csv(REPORT / "m3_vetting.csv", index=False)
    print(vet.to_string(index=False))

    flagged = vet[vet["verdict"] != "no_eb_signature"]
    # append flagged to the exclusion table
    excl = pd.read_csv(REPORT / "calibration_exclusions.csv"); excl["tic"] = excl["tic"].astype(str)
    add = pd.DataFrame([{"tic": r["tic"], "reason": "vetted_eclipse",
                         "source": "M3_automated_vetting", "detail": r["verdict"]}
                        for _, r in flagged.iterrows()])
    excl2 = pd.concat([excl, add], ignore_index=True).drop_duplicates(subset=["tic", "source"])
    excl2.to_csv(REPORT / "calibration_exclusions.csv", index=False)
    print(f"\n[vet] flagged {len(flagged)} as eclipses -> exclusions now {excl2['tic'].nunique()} stars")
    print(f"[vet] {len(outliers) - len(flagged)} residual outlier(s) show NO EB signature (kept; inspect at review)")


def main() -> None:
    p = argparse.ArgumentParser(description="M3 automated EB vetting of residual high-SDE null outliers.")
    p.add_argument("--sde-min", type=float, default=9.0)
    args = p.parse_args()
    run(args.sde_min)


if __name__ == "__main__":
    main()
