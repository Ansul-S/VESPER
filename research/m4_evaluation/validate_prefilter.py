"""Validate the white-noise pre-filter premise (Lever 1) on EXISTING M3 null data.

Premise: for the SAME period-coherence statistic R, the white-noise FAP is a lower bound on
the red-noise (block-bootstrap) FAP. If true, rejecting candidates whose WHITE FAP already
exceeds alpha is provably safe (it can never wrongly reject a candidate the red test would pass).

Red FAP: already computed in M3 (`data/manifests/m3/m3_per_star.csv`, column `period_fap`,
B=1000 circular block bootstrap on residuals).
White FAP: recomputed here cheaply — the §5/§9 white null = draw k uniform event times over the
same baseline, recompute R, take the exceedance. No detection re-run, no TLS.

CALIBRATION-only. No TEST. No seal change. Read-only diagnostic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m3_calibration"))
from detector import detect_events          # noqa: E402
from period_recovery import best_period      # noqa: E402

ALPHA = 0.01           # M3 sealed alpha_fap
B_WHITE = 400          # white surrogates (cheap)
N_STARS = 120          # sample of M3 null stars
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
CACHE = Path("data/processed/m1")


def white_fap(epochs, span_lo, span_hi, p_min, p_max, k, rng, b_white=B_WHITE):
    """FAP under the white null: k uniform event times over the same span."""
    if k < 2:
        return np.nan
    _, _, obs_R = best_period(epochs, p_min, p_max, 3)
    if not np.isfinite(obs_R):
        return np.nan
    ge = 0
    for _ in range(b_white):
        ts = np.sort(rng.uniform(span_lo, span_hi, k))
        Rs = best_period(ts, p_min, p_max, 3)[2]
        if Rs >= obs_R:
            ge += 1
    return (ge + 1) / (b_white + 1)


def main():
    per = pd.read_csv("data/manifests/m3/m3_per_star.csv")
    per["tic"] = per["tic"].astype(str)
    per = per[per["period_fap"].notna()]                      # stars with a stored red FAP
    avail = {p.stem for p in CACHE.glob("*.npz")}
    per = per[per["tic"].isin(avail)]
    samp = per.sample(min(N_STARS, len(per)), random_state=20260618).reset_index(drop=True)
    print(f"[prefilter] testing {len(samp)} M3 null stars (stored red FAP vs recomputed white FAP)")

    rng = np.random.default_rng(20260618)
    rows = []
    for i, r in samp.iterrows():
        tic = r["tic"]
        z = np.load(CACHE / f"{tic}.npz")
        t, res = np.asarray(z["time"], float), np.asarray(z["resid"], float)
        ev = detect_events(t, res, DGRID, stride_frac=0.5, z_for_extraction=2.0)  # match M3
        k = int(ev.shape[0])
        if k < 2:
            continue
        baseline = float(t.max() - t.min())
        p_min, p_max = 0.5, 0.5 * baseline
        fw = white_fap(ev[:, 0], float(t.min()), float(t.max()), p_min, p_max, k, rng)
        rows.append({"tic": tic, "k": k, "fap_white": fw, "fap_red": float(r["period_fap"])})
        if (i + 1) % 30 == 0:
            print(f"[prefilter] {i+1}/{len(samp)} ...", flush=True)
    d = pd.DataFrame(rows).dropna(subset=["fap_white", "fap_red"])

    # --- core checks ---
    holds = (d["fap_white"] <= d["fap_red"] + 1e-9).mean()
    # safety: stars the pre-filter would reject (white > alpha) that red would PASS (red <= alpha)
    wrong_reject = d[(d["fap_white"] > ALPHA) & (d["fap_red"] <= ALPHA)]
    rejected = (d["fap_white"] > ALPHA).mean()        # fraction the pre-filter rejects for free
    print("\n================ WHITE-NOISE PRE-FILTER VALIDATION ================")
    print(f"n stars (k>=2, both FAPs): {len(d)}   median k={d['k'].median():.0f}")
    print(f"white <= red holds for: {holds*100:.1f}% of stars   (premise: should be ~100%)")
    print(f"pre-filter rejects (white FAP > {ALPHA}): {rejected*100:.1f}% of routed candidates -> bootstrap skipped")
    print(f"UNSAFE wrong-rejects (white>{ALPHA} BUT red<={ALPHA}): {len(wrong_reject)}  (MUST be 0 for safety)")
    if len(wrong_reject):
        print(wrong_reject.to_string(index=False))
    # how many survive the pre-filter and still need a FAP (the lookup-table population)
    print(f"survive pre-filter (white<={ALPHA}) -> need lookup/bootstrap: {(d['fap_white']<=ALPHA).mean()*100:.1f}%")
    print(f"\n[corr] white vs red FAP: rho={np.corrcoef(d['fap_white'],d['fap_red'])[0,1]:.3f}")
    out = Path("data/manifests/m4/dry_run"); out.mkdir(parents=True, exist_ok=True)
    d.to_csv(out / "prefilter_validation.csv", index=False)
    print(f"[prefilter] wrote {out}/prefilter_validation.csv")


if __name__ == "__main__":
    main()
