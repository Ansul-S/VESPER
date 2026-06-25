"""M6 W1 — depth/T14 recovery on CALIBRATION injections (completes M5 -> T5-full / F5-depth).

The sealed-test recovery did not log the confirmer's fitted depth. Here we re-run route+confirm
on CALIBRATION injections (test-blind) and log the confirmer's fitted depth (delta) vs depth_true,
and the seed duration (T14) vs t14_true. Sealed thresholds; no tuning; calibration only.

Run: .venv/bin/python research/m6_reality_check/depth_recovery.py --per-cell 50 --workers 8
"""
from __future__ import annotations
import sys, argparse
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m4_evaluation")); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
import seal_loader as SL, confirmer as CF, injection as INJ, m4_driver as M4  # noqa: E402
CACHE = Path("data/processed/m1"); OUT = Path("data/manifests/m6"); OUT.mkdir(parents=True, exist_ok=True)
_FR = _MAN = _LD = _TRED = None


def _init(man, t_red):
    global _FR, _MAN, _LD, _TRED
    _FR, _MAN, _LD, _TRED = SL.load_frozen(), man, INJ.constant_ld(), t_red


def _worker(task):
    tic, P, Rp, b, seed = task
    fr, t_red = _FR, _TRED
    t, r0 = M4._resid(tic)
    built = INJ.build_injection(t, P, Rp, b, _MAN.loc[tic], _LD, np.random.default_rng(seed),
                                host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    s = M4._route_and_seed(t, r, fr, 0.005, np.random.default_rng(seed ^ 7))
    if not (s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"])):
        return None
    c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), M4.STELLAR, t_red)
    if not c["confirmed"]:
        return None
    return {"period_days": P, "radius_rearth": int(Rp), "depth_true": truth["depth_true"],
            "depth_fit": float(c["delta"]), "t14_true": truth["t14_true"], "t14_seed": float(s["t14"])}


def main():
    from multiprocessing import Pool
    ap = argparse.ArgumentParser(); ap.add_argument("--per-cell", type=int, default=50)
    ap.add_argument("--workers", type=int, default=8); a = ap.parse_args()
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    pool_df = man[(man.split == "calibration") & (man.rad > 0) & np.isfinite(man.logg) & np.isfinite(man.Teff)]
    pool_df = pool_df[pool_df.tic.isin((draw - exc) & avail)]
    assert (pool_df.split == "calibration").all(), "TEST LEAK"
    hosts = pool_df.sample(min(80, len(pool_df)), random_state=22).tic.tolist()
    man_idx = pool_df.set_index("tic")
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    tasks, sc = [], 0
    for (P, Rp) in cells:
        for j in range(a.per_cell):
            tasks.append((hosts[(j + sc) % len(hosts)], P, Rp, INJ.GRID_B[j % len(INJ.GRID_B)], 70000 + sc)); sc += 1
    fr = SL.load_frozen(); t_red, _ = M4.verify_v3_manifest()
    print(f"[depth] {len(tasks)} calibration injections; T_red={t_red}; workers {a.workers}")
    rows = []
    with Pool(a.workers, initializer=_init, initargs=(man_idx, t_red)) as pool:
        for i, x in enumerate(pool.imap_unordered(_worker, tasks, chunksize=4), 1):
            if x: rows.append(x)
            if i % 200 == 0: print(f"[depth] {i}/{len(tasks)} ...")
    df = pd.DataFrame(rows); df.to_csv(OUT / "depth_recovery.csv", index=False)
    if not len(df):
        print("[depth] no confirmed injections"); return
    df["depth_fracerr"] = (df.depth_fit - df.depth_true) / df.depth_true
    df["t14_fracerr"] = (df.t14_seed - df.t14_true) / df.t14_true
    t5d = pd.DataFrame([
        {"metric": "confirmed injections (depth fitted)", "value": f"{len(df)}"},
        {"metric": "median fractional depth error", "value": f"{df.depth_fracerr.median():+.3f}"},
        {"metric": "depth error IQR", "value": f"{df.depth_fracerr.quantile(.25):+.3f} .. {df.depth_fracerr.quantile(.75):+.3f}"},
        {"metric": "median fractional T14 (seed) error", "value": f"{df.t14_fracerr.median():+.3f}"},
    ])
    t5d.to_csv(Path("research/m4_evaluation/tables") / "T5_depth.csv", index=False)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
    ax1.scatter(df.depth_true * 1e6, df.depth_fit * 1e6, s=6, alpha=0.4, c="#2a9d8f")
    lim = [df.depth_true.min() * 1e6 * 0.8, df.depth_true.max() * 1e6 * 1.2]
    ax1.plot(lim, lim, "k-", lw=1); ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel("true depth (ppm)"); ax1.set_ylabel("fitted depth (ppm)"); ax1.set_title("F5b — depth recovery")
    ax2.scatter(df.t14_true * 24, df.t14_seed * 24, s=6, alpha=0.4, c="#264653")
    lim2 = [df.t14_true.min() * 24 * 0.8, df.t14_true.max() * 24 * 1.2]
    ax2.plot(lim2, lim2, "k-", lw=1); ax2.set_xlabel("true T14 (h)"); ax2.set_ylabel("seed T14 (h)"); ax2.set_title("F5c — duration (seed)")
    fig.tight_layout(); fig.savefig("research/m4_evaluation/figures/F5_depth_t14_recovery.png", dpi=150, bbox_inches="tight"); plt.close(fig)
    print(f"[depth] median depth fracerr {df.depth_fracerr.median():+.3f}; n={len(df)} -> T5_depth.csv, F5_depth_t14_recovery.png")


if __name__ == "__main__":
    main()
