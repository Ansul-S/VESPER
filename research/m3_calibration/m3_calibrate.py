"""M3 threshold calibration driver (Phase I) — CALIBRATION-null only; TEST sealed until M4.

Builds nothing learned. Runs the untrained machinery on null calibration light curves and
DERIVES the sealed-target thresholds:
  * z_star   : smallest detector SNR s.t. mean false events/LC <= 1.0          (VAL A.3)
  * z_mono   : smallest detector SNR s.t. mean false events/LC <= 0.1          (Decision B)
  * T        : 99th-pct of full-TLS peak SDE over null stars (FAR <= 1%/star)  (VAL A.2)
  * alpha_FAP: 1% null-exceedance target; null period-FAP distribution reported (VAL A.8/H4)
  * epsilon  : fixed = 0.01 (Decision E; recovery tolerance, not derived from null noise)

NO Seal #2 here. Outputs are written for OWNER REVIEW (PHASE1_M3_PLAN.md §10 condition).

Run (host network for conditioning):  python research/m3_calibration/m3_calibrate.py [--limit N]
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m1_conditioning"))

from detector import detect_events                      # noqa: E402
from period_recovery import best_period, period_fap     # noqa: E402
from tls_engine import full_tls                         # noqa: E402

_THRESHOLD_KEYS = {"z_star", "zstar", "z_mono"}  # M3 DERIVES these; config must not pin a value


def load_cfg(path: str) -> dict:
    import yaml
    cfg = yaml.safe_load(Path(path).read_text())
    if cfg["data_scope"]["split"] != "calibration":
        raise ValueError("M3 calibration runs on CALIBRATION only (TEST sealed until M4).")
    if not cfg["data_scope"].get("null_only"):
        raise ValueError("M3 threshold calibration must use null stars only.")
    return cfg


def select_null_sample(cfg, limit=None) -> list[str]:
    m = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    m["tic"] = m["tic"].astype(str)
    cal = m[m["split"] == "calibration"].copy()
    cal["is_null"] = (~cal["is_known_planet"].astype(bool)) & (~cal["is_known_fp"].astype(bool))
    cal_null = cal[cal["is_null"]]
    n_target = int(cfg["data_scope"].get("null_random_n", 0))
    if n_target > 0:
        # full-pool draw: random N null calibration stars, seeded; reuse cached residuals where drawn
        rng = np.random.default_rng(int(cfg["runtime"]["seed"]))
        pool = sorted(cal_null["tic"].tolist())
        n = min(n_target, len(pool))
        tics = sorted(rng.choice(pool, size=n, replace=False).tolist())
        print(f"[M3] full-pool null draw: {len(tics)} of {len(pool)} (seed {cfg['runtime']['seed']})")
        return tics[:limit] if limit else tics
    # default: the eta-sample null subset (185)
    eta = set(str(t) for t in pd.read_csv(cfg["input"]["m1_noise_summary"])["tic"].astype(str))
    tics = sorted(cal_null[cal_null["tic"].isin(eta)]["tic"].tolist())
    return tics[:limit] if limit else tics


def condition_or_load(tic, cfg, m1cfg):
    """2.5 d conditioned residual: load cached (window-tagged) or condition fresh (network)."""
    cache = Path(cfg["output"]["resid_cache_dir"]) / f"{tic}.npz"
    win = float(cfg["data_scope"]["detrend_window_days"])
    if cache.exists():
        z = np.load(cache)
        if "window" in z and float(z["window"]) == win:
            return np.asarray(z["time"]), np.asarray(z["resid"])
    from m1_pipeline import _condition_one
    out = _condition_one(tic, set(cfg["input"]["sectors"]), m1cfg)
    if out is None:
        return None, None
    t, r, used = out
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, time=t, resid=r, sectors=used, window=win)
    return t, r


def _process_star(args):
    """Heavy per-star compute from a CACHED 2.5 d residual: detector + period FAP + full TLS.
    Module-level for multiprocessing. Returns the per-LC dict (no network)."""
    tic, cache_path, cfg, tau_gp = args
    z = np.load(cache_path, allow_pickle=True)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    det, tls, pr = cfg["detector"], cfg["tls"], cfg["period_recovery"]
    dgrid = det["duration_grid_days"]
    rng = np.random.default_rng(int(cfg["runtime"]["seed"]) ^ (int(tic) & 0x7FFFFFFF))
    ev = detect_events(t, r, dgrid, stride_frac=det["t0_stride_frac"], z_for_extraction=2.0)
    snrs = ev[:, 1] if ev.size else np.empty(0)
    baseline = float(t.max() - t.min())
    p_min, p_max = float(tls["period_min_days"]), tls["period_max_frac_baseline"] * baseline
    fap = np.nan
    if ev.shape[0] >= 2:
        _, _, obs_R = best_period(ev[:, 0], p_min, p_max, tls["oversampling_factor"])
        t14 = float(np.median(dgrid))
        fap, _ = period_fap(t, r, obs_R, float(tau_gp), t14, dgrid, p_min, p_max,
                            z_star=2.0, block_len_multiple=pr["block_len_multiple"],
                            n_surrogates=pr["n_surrogates"], rng=rng)
    try:
        sde = full_tls(t, r, tls)["sde"]
    except Exception as e:
        sde = np.nan
        print(f"[M3] TIC {tic}: TLS error {type(e).__name__}")
    return {"tic": tic, "n_events_ge2": int((snrs >= 2).sum()),
            "max_event_snr": float(snrs.max()) if snrs.size else np.nan,
            "event_snrs": snrs.tolist(), "period_fap": fap, "tls_sde": sde}


def run(config_path: str, limit=None, workers=None) -> None:
    import os
    from multiprocessing import Pool
    cfg = load_cfg(config_path)
    import yaml
    m1cfg = yaml.safe_load(Path(cfg["input"]["m1_config"]).read_text())
    nm = pd.read_csv(cfg["input"]["m1_noise_summary"]).set_index("tic")
    nm.index = nm.index.astype(str)

    det, tls, pr = cfg["detector"], cfg["tls"], cfg["period_recovery"]
    dgrid = det["duration_grid_days"]
    tics = select_null_sample(cfg, limit)
    print(f"[M3] null calibration sample: {len(tics)} targets  window={cfg['data_scope']['detrend_window_days']}d")

    # --- Phase A: serial conditioning (network) -> cache 2.5 d residuals ---
    # Resilient: cached residuals load offline; transient MAST drops retry then skip (never kill the run).
    import time
    ready, n_fail = [], 0
    for k, tic in enumerate(tics, 1):
        t = r = None
        for attempt in range(3):
            try:
                t, r = condition_or_load(tic, cfg, m1cfg)
                break
            except Exception as e:
                if attempt == 2:
                    n_fail += 1
                    print(f"[M3] TIC {tic}: conditioning failed after retries ({type(e).__name__}); skipped")
                else:
                    time.sleep(3 * (attempt + 1))
        if t is None or r is None or r.size < 1000:
            continue
        tau = float(nm.loc[tic, "tau_gp_days"]) if tic in nm.index else 0.005
        ready.append((tic, str(Path(cfg["output"]["resid_cache_dir"]) / f"{tic}.npz"), cfg, tau))
        if k % 50 == 0:
            print(f"[M3] conditioned {k}/{len(tics)} (ready={len(ready)}, failed={n_fail}) ...", flush=True)
    print(f"[M3] Phase A done: {len(ready)} residuals ready ({n_fail} failed). Phase B (parallel TLS/bootstrap)...", flush=True)

    # --- Phase B: parallel heavy compute from cache (no network) ---
    # imap_unordered + chunksize=1 so long-baseline stars don't bottleneck one worker's chunk.
    nw = workers or max(1, (os.cpu_count() or 2) - 2)
    per_lc = []
    with Pool(nw) as pool:
        for i, res in enumerate(pool.imap_unordered(_process_star, ready, chunksize=1), 1):
            per_lc.append(res)
            if i % 50 == 0:
                print(f"[M3] Phase B: {i}/{len(ready)} done ...", flush=True)
    df = pd.DataFrame(per_lc)
    n = len(df)

    # ---- derive thresholds ----
    all_snrs = [s for row in df["event_snrs"] for s in row]
    def mean_events_per_lc(z):
        return float(np.mean([sum(1 for s in row if s >= z) for row in df["event_snrs"]])) if n else np.nan
    zgrid = np.round(np.arange(3.0, 12.01, 0.1), 2)
    z_star = next((float(z) for z in zgrid if mean_events_per_lc(z) <= det["z_star_target_false_events_per_lc"]), float("nan"))
    z_mono = next((float(z) for z in zgrid if mean_events_per_lc(z) <= det["z_mono_target_false_events_per_lc"]), float("nan"))
    sde_vals = df["tls_sde"].dropna().values
    T = float(np.nanpercentile(sde_vals, 100 * (1 - tls["far_target_per_star"]))) if sde_vals.size else float("nan")
    fap_vals = df["period_fap"].dropna().values
    alpha_fap = float(pr["alpha_fap_target"])
    null_exceed_at_alpha = float(np.mean(fap_vals <= alpha_fap)) if fap_vals.size else float("nan")
    epsilon = float(cfg["fast_path"]["epsilon"])

    thresholds = {
        "z_star": z_star, "z_mono": z_mono, "n_min": int(cfg["routing"]["n_min"]),
        "T_sde": T, "alpha_fap": alpha_fap, "epsilon": epsilon,
        "achieved": {
            "mean_false_events_per_lc_at_z_star": mean_events_per_lc(z_star) if np.isfinite(z_star) else None,
            "mean_false_events_per_lc_at_z_mono": mean_events_per_lc(z_mono) if np.isfinite(z_mono) else None,
            "tls_far_target": tls["far_target_per_star"], "T_is_pct": 100 * (1 - tls["far_target_per_star"]),
            "null_fap_exceedance_at_alpha": null_exceed_at_alpha,
            "n_null_stars": n, "n_with_tls": int(sde_vals.size), "n_with_period_fap": int(fap_vals.size),
            "tls_sde_median": float(np.nanmedian(sde_vals)) if sde_vals.size else None,
            "tls_sde_max": float(np.nanmax(sde_vals)) if sde_vals.size else None,
        },
    }

    outdir = Path(cfg["output"]["report_dir"]); outdir.mkdir(parents=True, exist_ok=True)
    df.drop(columns=["event_snrs"]).to_csv(outdir / "m3_per_star.csv", index=False)
    prov = {
        "milestone": "M3", "stage": "threshold calibration (PROVISIONAL — pre-review, NO Seal #2)",
        "config_path": config_path,
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "manifest_seal1_sha256": cfg["input"]["manifest_seal1_sha256"],
        "split": "calibration", "null_only": True,
        "sample": cfg["data_scope"]["calibration_sample"], "n_null_stars": n,
        "thresholds": thresholds,
        "machine": {"platform": platform.platform(), "processor": platform.processor() or "n/a",
                    "python": sys.version.split()[0]},
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "seed": int(cfg["runtime"]["seed"]),
        "note": "PROVISIONAL thresholds for owner review. No Seal #2. TEST untouched. "
                "Sample = null eta-subset (185); extensible to full 6885 null calibration pool.",
    }
    (outdir / "m3_thresholds_PROVISIONAL.json").write_text(json.dumps(prov, indent=2, default=str))
    print("\n[M3] PROVISIONAL thresholds (pre-review, NO Seal #2):")
    print(json.dumps(thresholds, indent=2, default=str))
    print(f"[M3] report -> {outdir}/m3_thresholds_PROVISIONAL.json + m3_per_star.csv")


def main() -> None:
    p = argparse.ArgumentParser(description="M3 threshold calibration (null calibration only).")
    p.add_argument("--config", default=str(HERE / "config" / "m3_config.yaml"))
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--workers", type=int, default=None)
    args = p.parse_args()
    run(args.config, limit=args.limit, workers=args.workers)


if __name__ == "__main__":
    main()
