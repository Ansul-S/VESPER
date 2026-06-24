"""Epoch-fixed Arm-B confirmation statistic — CONFIRMATION STUDY (CALIBRATION-ONLY).

Owner-commissioned (2026-06-18): test whether a period-AND-epoch-fixed transit
matched-filter S/N resolves the null false-alarm tail of the crude all-phase depth-SNR,
while staying range-invariant and ~free. NO TEST. NO sealed-value change. NO Seal #2b.

Statistic (operational, evidence-first):
  detector events -> route iff >= N_min events above z_star
                  -> P_hat = integer-comb best period of event epochs
                  -> t0_hat, T14 = strongest event's epoch + duration
  MF S/N at FIXED (P_hat, t0_hat): fold, in-transit = |phase| <= T14/2,
     depth = -mean(r_in), snr = depth / (sigma_out / sqrt(N_in)).
  NO phase search, NO period grid -> range-invariant + O(n) cost.

Candidate score per star = MF S/N if routed else 0  (captures routing + confirmation;
a non-routed star goes to the full-TLS fallback, so it is not an Arm-B candidate).
FAR<=1%/star threshold T_mf = 99th percentile of the candidate score over null stars.

Run (offline): .venv/bin/python research/m4_evaluation/epoch_fixed_diagnostic.py
"""

from __future__ import annotations

import glob
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m3_calibration"))

import injection as INJ                       # noqa: E402
import seal_loader as SL                      # noqa: E402
from detector import detect_events            # noqa: E402
from period_recovery import best_period       # noqa: E402
from finding_b_diagnostic import depth_snr_at_period, _full_tls  # noqa: E402  (reuse crude stat + full TLS)

N_NULL = 300
INJ_CELLS = [(2.0, 4), (4.0, 4), (2.0, 2), (1.0, 4)]   # strong + borderline (calibration injections)
INJ_HOSTS_PER_CELL = 25
ANCHOR_N = 6   # full-TLS anchor subset size per class (strong planet / null)


def evidence_ephemeris(t, r, fr):
    """Operational (P_hat, t0_hat, T14, n_events). None if not routed (< N_min events)."""
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    if ev.shape[0] < fr.n_min:
        return None
    k = int(np.argmax(ev[:, 1]))
    t0, dur = float(ev[k, 0]), float(ev[k, 2])
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    P_hat = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)[0]
    if not np.isfinite(P_hat):
        return None
    return float(P_hat), t0, dur, int(ev.shape[0])


def mf_snr_fixed(t, r, P, t0, T14):
    """WHITE-noise matched-filter S/N at FIXED (P, t0): depth / (sigma_out / sqrt(N_in_cadences)).
    No phase search, no period grid. (Overstates S/N under correlated noise — see red-noise variant.)"""
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    nin = int(intr.sum())
    if nin < 3:
        return 0.0, nin
    sig = 1.4826 * np.median(np.abs(r[~intr] - np.median(r[~intr])))
    if not np.isfinite(sig) or sig <= 0:
        return 0.0, nin
    depth = -float(r[intr].mean())
    return float(depth / (sig / np.sqrt(nin))), nin


def rednoise_snr_fixed(t, r, P, t0, T14):
    """RED-NOISE-aware matched-filter S/N at FIXED (P, t0), detector-consistent.

    Noise unit = the transit-DURATION timescale (not single cadences): sigma_dur = robust
    scatter of the box-averaged (width T14) out-of-transit flux. Effective independent count =
    number of distinct transits with in-transit data (correlated within a transit, ~independent
    across transits for P >> tau). S/N = depth * sqrt(N_transits) / sigma_dur."""
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    nin = int(intr.sum())
    if nin < 3:
        return 0.0, 0
    # box-averaged depth series on the duration timescale -> red-noise-aware scatter
    cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
    nbin = max(1, int(round(max(T14, 1e-3) / cad)))
    if r.size < 2 * nbin:
        return 0.0, 0
    csum = np.concatenate([[0.0], np.cumsum(r)])
    box = (csum[nbin:] - csum[:-nbin]) / nbin                # box-averaged flux, duration timescale
    sig_dur = 1.4826 * np.median(np.abs(box - np.median(box)))
    if not np.isfinite(sig_dur) or sig_dur <= 0:
        return 0.0, 0
    # distinct transits with data
    epochs = np.round((t[intr] - t0) / P)
    n_tr = int(np.unique(epochs).size)
    if n_tr < 1:
        return 0.0, 0
    depth = -float(r[intr].mean())
    return float(depth * np.sqrt(n_tr) / sig_dur), n_tr


def candidate_score(t, r, fr):
    """(white MF S/N, red-noise MF S/N) at the operational ephemeris if routed, else (0,0)."""
    eph = evidence_ephemeris(t, r, fr)
    if eph is None:
        return 0.0, 0.0, 0, None
    P, t0, T14, nev = eph
    white, _ = mf_snr_fixed(t, r, P, t0, T14)
    red, _ = rednoise_snr_fixed(t, r, P, t0, T14)
    return white, red, nev, (P, t0, T14)


def main():
    fr = SL.load_frozen()
    ld = INJ.constant_ld()
    rng = np.random.default_rng(20260618)
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {Path(p).stem for p in glob.glob("data/processed/m1/*.npz")}
    # SEALED cleaned null pool = M3's actual null draw (m3_per_star.csv, 1000) MINUS the 146/158
    # vetted EB/variable exclusions -> the 854-star cleaned set M3 calibrated on. (The
    # m3_null_cleaned_catalog still CONTAINS excluded contaminants, so it must not be used directly.)
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    cleaned = (draw - exc) & avail
    cal = man[(man["split"] == "calibration") & (man["tic"].isin(cleaned))
              & (man["rad"] > 0) & np.isfinite(man["logg"]) & np.isfinite(man["Teff"])].copy()
    assert (cal["split"] == "calibration").all(), "TEST LEAK"
    assert not (set(cal["tic"]) & exc), "contaminant leaked into null pool"
    print(f"[cleaned null pool] {len(cal)} vetted-clean calibration hosts (M3 draw minus {len(exc)} exclusions)")

    def load_resid(tic):
        z = np.load(f"data/processed/m1/{tic}.npz")
        return np.asarray(z["time"], float), np.asarray(z["resid"], float)

    # ---- NULLS (large, cheap): white + red-noise candidate scores ----
    null_tics = cal.sample(min(N_NULL, len(cal)), random_state=1).reset_index(drop=True)
    nrows = []
    for _, row in null_tics.iterrows():
        tic = row["tic"]; t, r = load_resid(tic)
        if r.size < 1000:
            continue
        white, red, nev, eph = candidate_score(t, r, fr)
        nrows.append({"tic": tic, "white": white, "red": red, "n_events": nev, "routed": eph is not None})
    nd = pd.DataFrame(nrows)
    routed_frac = float(nd["routed"].mean())
    T_white = float(np.percentile(nd["white"], 99))     # FAR<=1%/star by construction
    T_red = float(np.percentile(nd["red"], 99))

    # ---- PLANETS (cheap): white + red-noise scores across cells ----
    prows = []
    hosts = cal.sample(min(INJ_HOSTS_PER_CELL * 2, len(cal)), random_state=2).reset_index(drop=True)
    for (P, Rp) in INJ_CELLS:
        for j in range(INJ_HOSTS_PER_CELL):
            row = hosts.iloc[j % len(hosts)]
            tic = row["tic"]; t, r0 = load_resid(tic)
            if r0.size < 1000:
                continue
            built = INJ.build_injection(t, P, Rp, 0.0, row, ld, rng, host_mode="cached_residual", r_host=r0)
            if built is None:
                continue
            _, r, truth = built
            white, red, nev, eph = candidate_score(t, r, fr)
            prows.append({"tic": tic, "P": P, "Rp": Rp, "white": white, "red": red,
                          "routed": eph is not None, "n_transits": truth["n_transits"]})
    pdf = pd.DataFrame(prows)

    def auc(a, b):
        a, b = np.asarray(a), np.asarray(b)
        return float(np.mean([1.0 if x > y else (0.5 if x == y else 0.0) for x in a for y in b]))

    def report_variant(col, T):
        rec_all = float((pdf[col] >= T).mean())
        rec_strong = float((pdf[pdf["Rp"] >= 4][col] >= T).mean())
        return auc(pdf[col], nd[col]), T, rec_all, rec_strong

    # ---- FULL-TLS ANCHOR (small): track Arm-A recovery + cost ratio ----
    anchor_planets = pdf[(pdf["Rp"] == 4) & (pdf["P"] == 2.0)].head(ANCHOR_N)
    anchor, cost_full, cost_mf = [], [], []
    for _, row in anchor_planets.iterrows():
        tic = row["tic"]; t, r0 = load_resid(tic)
        built = INJ.build_injection(t, 2.0, 4, 0.0, man[man.tic == tic].iloc[0], ld, np.random.default_rng(7), "cached_residual", r_host=r0)
        if built is None:
            continue
        _, r, _ = built
        pmax = fr.period_max_frac_baseline * (t.max() - t.min())
        t0 = time.perf_counter(); sde_f, _ = _full_tls(t, 1 + r, fr.period_min_days, pmax, fr.oversampling); cost_full.append(time.perf_counter() - t0)
        eph = evidence_ephemeris(t, r, fr)
        t0 = time.perf_counter()
        red = rednoise_snr_fixed(t, r, *eph[:3])[0] if eph else 0.0
        cost_mf.append(time.perf_counter() - t0)
        anchor.append({"tic": tic, "sde_full": sde_f, "arm_a_recovered": sde_f >= fr.T_sde, "red": red})
    adf = pd.DataFrame(anchor)
    cost_ratio = float(np.median(cost_mf) / np.median(cost_full)) if cost_full else float("nan")

    out = Path("data/manifests/m4/dry_run"); out.mkdir(parents=True, exist_ok=True)
    nd.to_csv(out / "epoch_fixed_nulls.csv", index=False)
    pdf.to_csv(out / "epoch_fixed_planets.csv", index=False)
    adf.to_csv(out / "epoch_fixed_anchor.csv", index=False)

    print("\n================ EPOCH-FIXED CONFIRMATION STUDY (cleaned null pool) ================")
    print(f"nulls={len(nd)} (routed {routed_frac*100:.1f}%)  planets={len(pdf)}  anchor={len(adf)}")
    for name, col, T in [("WHITE  sqrt(N_cad)", "white", T_white), ("RED-NOISE sqrt(N_tr)", "red", T_red)]:
        a, _, rall, rstrong = report_variant(col, T)
        print(f"\n[{name}]")
        print(f"  null: median={nd[col].median():.2f} 95th={np.percentile(nd[col],95):.2f} "
              f"99th(T,FAR1%)={T:.2f} max={nd[col].max():.2f}")
        print(f"  AUC(planet/null)={a:.3f}  recall@FAR1%: all={rall:.2f} strong(Rp>=4)={rstrong:.2f}")
        for (P, Rp), g in pdf.groupby(["P", "Rp"]):
            print(f"     P={P} Rp={Rp}: med={g[col].median():6.2f} recall={float((g[col]>=T).mean()):.2f} routed={g.routed.mean():.2f}")
    if len(adf):
        rec = adf[adf.arm_a_recovered]
        print(f"\n[vs Arm A] of {int(adf.arm_a_recovered.sum())} Arm-A-recovered anchors, RED>=T_red: {int((rec.red>=T_red).sum())}/{len(rec)}")
    print(f"[cost]     epoch-fixed / full TLS = {cost_ratio:.2e}  (median {np.median(cost_mf)*1e3:.2f} ms vs full {np.median(cost_full):.1f} s)")
    print(f"[range-inv] no period grid used -> invariant to TLS search width: True")
    print(f"\nartifacts -> {out}/epoch_fixed_{{nulls,planets,anchor}}.csv")


if __name__ == "__main__":
    main()
