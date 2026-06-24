"""Recall-safety test for the white-noise pre-filter (Lever 1) — on INJECTED planets.

The dangerous case the null-only test could not probe: a REAL planet whose red (bootstrap) FAP
<= alpha (the pipeline would keep it) but whose white FAP > alpha (the pre-filter would clip it
first) -> a lost planet. This can only be seen where red-passes are common: injected planets.

For each injected planet we compute BOTH the red FAP (B=1000 block bootstrap, same as M3) and the
cheap white FAP (uniform event-time redraw), plus whether the recovered period matches truth.
Then we find the smallest safety margin m such that rejecting only when white_FAP > m*alpha clips
NO red-passing (and no period-matched) planet.

CALIBRATION-only. No TEST. No seal change. Parallel; no TLS.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m3_calibration"))

import injection as INJ                          # noqa: E402
from detector import detect_events               # noqa: E402
from period_recovery import best_period, period_fap  # noqa: E402

ALPHA = 0.01
B_RED = 1000
B_WHITE = 400
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
CACHE = Path("data/processed/m1")
# strong/recoverable, multi-transit cells (so they route and have real periodicity)
CELLS = [(1.0, 2), (1.0, 4), (1.0, 8), (2.0, 2), (2.0, 4), (2.0, 8), (4.0, 4), (4.0, 8)]
_MAN = _LD = _TAU = None


def _init(man, tau):
    global _MAN, _LD, _TAU
    _MAN, _LD, _TAU = man, INJ.constant_ld(), tau


def _white_fap(epochs, lo, hi, p_min, p_max, k, rng, b=B_WHITE):
    _, _, obs_R = best_period(epochs, p_min, p_max, 3)
    if not np.isfinite(obs_R):
        return np.nan
    ge = sum(1 for _ in range(b) if best_period(np.sort(rng.uniform(lo, hi, k)), p_min, p_max, 3)[2] >= obs_R)
    return (ge + 1) / (b + 1)


def _pmatch(p_hat, p_true):
    if not np.isfinite(p_hat) or p_hat <= 0:
        return False
    if abs(p_hat - p_true) / p_true < 0.01:
        return True
    return any(abs(p_hat - c) / c < 0.01 for m in (2, 3) for c in (p_true / m, m * p_true))


def _worker(task):
    tic, P, Rp, b, seed = task
    rng = np.random.default_rng(seed)
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    if r0.size < 1000:
        return None
    built = INJ.build_injection(t, P, Rp, b, _MAN.loc[tic], _LD, rng, "cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    ev = detect_events(t, r, DGRID, stride_frac=0.5, z_for_extraction=2.0)
    k = int(ev.shape[0])
    if k < 2:
        return {"tic": tic, "P": P, "Rp": Rp, "routed": False, "k": k}
    baseline = float(t.max() - t.min())
    p_min, p_max = 0.5, 0.5 * baseline
    p_hat, _, obs_R = best_period(ev[:, 0], p_min, p_max, 3)
    t14 = float(np.median(DGRID))
    fap_red, _ = period_fap(t, r, obs_R, float(_TAU.get(tic, 0.005)), t14, DGRID, p_min, p_max,
                            2.0, 3, B_RED, np.random.default_rng(seed ^ 1))
    fap_white = _white_fap(ev[:, 0], float(t.min()), float(t.max()), p_min, p_max, k,
                           np.random.default_rng(seed ^ 2))
    return {"tic": tic, "P": P, "Rp": int(Rp), "routed": True, "k": k, "p_hat": float(p_hat),
            "pmatch": bool(_pmatch(p_hat, P)), "fap_red": float(fap_red), "fap_white": float(fap_white)}


def main():
    import os
    from multiprocessing import Pool
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    cleaned = (draw - exc) & avail
    cal = man[(man.split == "calibration") & (man.tic.isin(cleaned)) & (man.rad > 0)
              & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    nm = pd.read_csv("data/manifests/m1/m1_noise_summary.csv"); nm["tic"] = nm["tic"].astype(str)
    tau = dict(zip(nm["tic"], nm["tau_gp_days"]))
    hosts = cal.sample(min(100, len(cal)), random_state=20260618).tic.tolist()
    tasks = [(hosts[i], CELLS[i % len(CELLS)][0], CELLS[i % len(CELLS)][1], 0.0, 20260618 + i)
             for i in range(len(hosts))]
    nw = max(1, (os.cpu_count() or 4) - 2)
    print(f"[inj-safety] {len(tasks)} injected planets, B_red={B_RED}, {nw} workers ...", flush=True)

    rows = []
    with Pool(nw, initializer=_init, initargs=(cal.set_index("tic"), tau)) as pool:
        for i, x in enumerate(pool.imap_unordered(_worker, tasks, chunksize=1), 1):
            if x:
                rows.append(x)
            if i % 20 == 0:
                print(f"[inj-safety] {i}/{len(tasks)} ...", flush=True)
    d = pd.DataFrame(rows)
    routed = d[d.routed == True].dropna(subset=["fap_red", "fap_white"])

    red_pass = routed[routed.fap_red <= ALPHA]
    pm_pass = red_pass[red_pass.pmatch]
    print("\n================ PRE-FILTER RECALL-SAFETY (injected planets) ================")
    print(f"injected={len(d)}  routed={int((d.routed==True).sum())}  red-pass (fap_red<=a)={len(red_pass)}  "
          f"period-matched red-pass={len(pm_pass)}")
    if len(red_pass):
        clipped = red_pass[red_pass.fap_white > ALPHA]
        m_all = float(red_pass.fap_white.max() / ALPHA)
        print(f"\n[bare pre-filter, reject if white>{ALPHA}]")
        print(f"  red-pass planets CLIPPED: {len(clipped)}/{len(red_pass)} ({len(clipped)/len(red_pass)*100:.0f}%)  <- recall loss if >0")
        print(f"  white FAP among red-pass: median={red_pass.fap_white.median():.3f} max={red_pass.fap_white.max():.3f}")
        print(f"  smallest safe margin (all red-pass): white > {m_all:.1f} * alpha")
    if len(pm_pass):
        clip_pm = pm_pass[pm_pass.fap_white > ALPHA]
        m_pm = float(pm_pass.fap_white.max() / ALPHA)
        print(f"\n[true recoveries: period-matched red-pass]")
        print(f"  CLIPPED by bare pre-filter: {len(clip_pm)}/{len(pm_pass)}")
        print(f"  smallest safe margin (true recoveries): white > {m_pm:.1f} * alpha")
        print(f"  -> reject only when white FAP > {m_pm:.1f}*alpha = {m_pm*ALPHA:.3f} to clip ZERO real planets")
    # what does that margin cost? apply to the null run if present
    nullf = Path("data/manifests/m4/dry_run/prefilter_validation.csv")
    if nullf.exists() and len(pm_pass):
        nd = pd.read_csv(nullf)
        m = float(pm_pass.fap_white.max() / ALPHA)
        bare = (nd.fap_white > ALPHA).mean()
        margined = (nd.fap_white > m * ALPHA).mean()
        print(f"\n[compute retained at the safe margin]  null rejection: bare {bare*100:.1f}% -> margined {margined*100:.1f}%")
    out = Path("data/manifests/m4/dry_run"); out.mkdir(parents=True, exist_ok=True)
    d.to_csv(out / "prefilter_injection_safety.csv", index=False)
    print(f"\n[inj-safety] wrote {out}/prefilter_injection_safety.csv")


if __name__ == "__main__":
    main()
