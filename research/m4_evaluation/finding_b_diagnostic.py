"""Finding-B methodology diagnostic — CALIBRATION-ONLY. No TEST. No seal change.

Characterizes, on a modest calibration sample, the candidate Arm-B confirmation
statistics so the owner can choose how to resolve the SDE-comparability blocker:

  * SDE_full      — full-grid TLS SDE (the M3-calibrated arbiter; Arm A)
  * SDE_targeted  — narrow-window TLS SDE at several half-widths eps (Option 1 / Option 3)
  * depth_snr     — period-fixed folded box depth-SNR at P_hat (Option 2; range-invariant)

For each host we record the statistic for an INJECTED planet (recoverable + borderline
cells) and for the BARE null residual, plus per-statistic cost. Separation between the
planet and null populations is what determines whether a given statistic preserves E1.

Run (offline): .venv/bin/python research/m4_evaluation/finding_b_diagnostic.py [--hosts N]
"""

from __future__ import annotations

import argparse
import glob
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m3_calibration"))

import injection as INJ                  # noqa: E402
import seal_loader as SL                 # noqa: E402
from detector import detect_events       # noqa: E402
from period_recovery import best_period  # noqa: E402

import transitleastsquares.main as _tmain                       # noqa: E402
from transitleastsquares.grid import period_grid as _real_grid  # noqa: E402
from transitleastsquares import transitleastsquares             # noqa: E402

EPS_LIST = [0.01, 0.05, 0.10, 0.20]      # targeted half-widths to sweep (Option 3)


def _full_tls(t, flux, pmin, pmax, ovs):
    _tmain.period_grid = _real_grid       # ensure default grid
    m = transitleastsquares(np.asarray(t, float), np.asarray(flux, float))
    res = m.power(period_min=pmin, period_max=pmax, oversampling_factor=ovs,
                  use_threads=1, show_progress_bar=False)
    return float(res.SDE), float(res.period)


def _targeted_tls(t, flux, p_hat, eps, pmin, pmax, ovs):
    """TLS over the in-window optimal-frequency subset (Finding-A fix); SDE on that grid."""
    full = _real_grid(1, 1, float(np.max(t) - np.min(t)), pmin, pmax, ovs)
    win = full[(full > p_hat * (1 - eps)) & (full <= p_hat * (1 + eps))]
    if win.size == 0:
        win = np.array([p_hat])

    def _patched(R_star, M_star, time_span, period_min=0, period_max=float("inf"),
                 oversampling_factor=3, n_transits_min=2):
        return win
    _tmain.period_grid = _patched
    try:
        m = transitleastsquares(np.asarray(t, float), np.asarray(flux, float))
        res = m.power(oversampling_factor=ovs, use_threads=1, show_progress_bar=False)
        return float(res.SDE), int(win.size)
    finally:
        _tmain.period_grid = _real_grid


def depth_snr_at_period(t, r, P, durations):
    """Period-fixed folded box depth-SNR (Option 2). Fold at P, slide a box of each
    duration over phase, return max (mean in-box decrement) / (sigma/sqrt(n_in)).
    Range-invariant: depends only on P, not on any period grid."""
    t = np.asarray(t, float); r = np.asarray(r, float)
    phase = (t % P)
    order = np.argsort(phase)
    ph, rr = phase[order], r[order]
    sigma = 1.4826 * np.median(np.abs(rr - np.median(rr)))
    if sigma <= 0:
        return 0.0
    best = 0.0
    for dur in durations:
        w = float(dur)
        # slide box start across the folded phase [0, P)
        nstep = 50
        for s in np.linspace(0, P - w, nstep):
            inbox = (ph >= s) & (ph < s + w)
            n_in = int(inbox.sum())
            if n_in < 3:
                continue
            depth = -float(rr[inbox].mean())            # positive = transit-like
            snr = depth / (sigma / np.sqrt(n_in))
            if snr > best:
                best = snr
    return float(best)


def run(n_hosts=16):
    fr = SL.load_frozen()
    ovs = fr.oversampling
    dgrid = fr.duration_grid
    ld = INJ.constant_ld()
    rng = np.random.default_rng(20260618)

    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {Path(p).stem for p in glob.glob("data/processed/m1/*.npz")}
    cal = man[(man["split"] == "calibration") & (man["tic"].isin(avail))
              & (man["rad"] > 0) & np.isfinite(man["logg"]) & np.isfinite(man["Teff"])]
    cal = cal.sample(min(n_hosts, len(cal)), random_state=20260618).reset_index(drop=True)
    assert (cal["split"] == "calibration").all(), "TEST LEAK"

    # case plan: ~40% strong planet (P2,R4), ~30% borderline (P2,R2), ~30% null
    plan = ["planet_R4"] * (len(cal) * 4 // 10) + ["planet_R2"] * (len(cal) * 3 // 10)
    plan += ["null"] * (len(cal) - len(plan))
    rows = []
    for i, row in cal.iterrows():
        tic = row["tic"]
        z = np.load(f"data/processed/m1/{tic}.npz")
        t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
        if r0.size < 1000:
            continue
        case = plan[i]
        if case == "null":
            r, P_true, label = r0, None, "null"
        else:
            Rp = 4 if case == "planet_R4" else 2
            built = INJ.build_injection(t, 2.0, Rp, 0.0, row, ld, rng, host_mode="cached_residual", r_host=r0)
            if built is None:
                continue
            _, r, truth = built
            P_true, label = truth["P_true"], f"planet_R{Rp}"
        # operational P_hat: detector events -> best_period; else full-TLS period
        ev = detect_events(t, r, dgrid, stride_frac=0.5, z_for_extraction=fr.z_star)
        pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
        n_ev = ev.shape[0]
        t0 = time.perf_counter(); sde_full, p_full = _full_tls(t, 1 + r, fr.period_min_days, pmax, ovs)
        c_full = time.perf_counter() - t0
        if n_ev >= 2:
            p_hat = best_period(ev[:, 0], fr.period_min_days, pmax, ovs)[0]
            if not np.isfinite(p_hat):
                p_hat = p_full
        else:
            p_hat = p_full
        rec = {"tic": tic, "label": label, "P_true": P_true, "n_events": n_ev,
               "p_hat": float(p_hat), "p_full": p_full, "sde_full": sde_full, "cost_full": c_full}
        for eps in EPS_LIST:
            t0 = time.perf_counter(); sde_t, npd = _targeted_tls(t, 1 + r, p_hat, eps, fr.period_min_days, pmax, ovs)
            rec[f"sde_eps{eps}"] = sde_t; rec[f"npd_eps{eps}"] = npd; rec[f"cost_eps{eps}"] = time.perf_counter() - t0
        t0 = time.perf_counter(); rec["depth_snr"] = depth_snr_at_period(t, r, p_hat, dgrid)
        rec["cost_depth_snr"] = time.perf_counter() - t0
        rows.append(rec)
        print(f"[{i+1}/{len(cal)}] {label:>10} sde_full={sde_full:5.2f} "
              f"sde_eps.01={rec['sde_eps0.01']:5.2f} sde_eps.2={rec['sde_eps0.2']:5.2f} "
              f"dsnr={rec['depth_snr']:5.2f} cfull={c_full:5.1f}s", flush=True)

    df = pd.DataFrame(rows)
    out = Path("data/manifests/m4/dry_run"); out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "finding_b_diagnostic.csv", index=False)

    # --- summary: separation (planet vs null) per statistic + cost ---
    def summ(col):
        pl = df[df["label"].str.startswith("planet")][col].dropna()
        nu = df[df["label"] == "null"][col].dropna()
        return (f"planet med={pl.median():.2f}[{pl.min():.2f},{pl.max():.2f}] "
                f"null med={nu.median():.2f}[{nu.min():.2f},{nu.max():.2f}]")
    print("\n=== STATISTIC SEPARATION (planet vs null) ===")
    print(f" SDE_full        : {summ('sde_full')}  (T_A=10.74)")
    for eps in EPS_LIST:
        cr = df[f"cost_eps{eps}"].median() / df["cost_full"].median()
        print(f" SDE_targeted e={eps:<4}: {summ(f'sde_eps{eps}')}  cost/full={cr:.3f}  "
              f"npd~{int(df[f'npd_eps{eps}'].median())}")
    print(f" depth_snr (P-fix): {summ('depth_snr')}  cost/full={df['cost_depth_snr'].median()/df['cost_full'].median():.4f}")
    print(f"\n[diag] wrote {out}/finding_b_diagnostic.csv  (n={len(df)})")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--hosts", type=int, default=16)
    run(p.parse_args().hosts)


if __name__ == "__main__":
    main()
