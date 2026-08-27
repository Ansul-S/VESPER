"""MATH-AUDIT / roadmap MATH-3 — surrogate contamination: the FAP's null is built from a
series that CONTAINS the signal being tested.

ROADMAP MATH-3 (open, never executed) asks for "the argument that this only weakens the null
ordering (conservative direction)" plus a measurement on ~50 calibration injections.

THE ARGUMENT GOES THE OTHER WAY. `period_recovery.period_fap` block-bootstraps the SAME residual
`r` that carries the injected transits. Each surrogate therefore inherits the transit dips, at
scrambled epochs. Two consequences, both pushing the same direction:

  (i)  the dips are supernumerary DETECTIONS -> the surrogate's event multiplicity k_b is
       inflated relative to a signal-free null;
  (ii) the pooled surrogate law measured on 1236 calibration nulls is R_b ~ 1.61 k_b^-0.41
       (`surrogate_table.py`), i.e. R_b DECREASES with k_b.

So contamination lowers the surrogate resultants, lowers the exceedance count, and lowers the
FAP: the sealed test is ANTI-conservative on signal-bearing stars, not conservative. That is
recall-favourable and false-alarm-neutral (nulls carry no signal to leak), but it is the
opposite of the direction the roadmap assumed, and it means the FAP reported for a routed
candidate is not the FAP of the signal-free null.

MEASUREMENT. For each injection, compute the FAP twice on the identical RNG stream:
  fap_contaminated : surrogates drawn from r = host + transit   (SEALED behaviour)
  fap_clean        : surrogates drawn from r0 = host alone      (signal-free null)
both compared against the SAME observed resultant obs_R (computed on r). Calibration only.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "research/m2_injection"))
sys.path.insert(0, str(REPO / "research/m4_evaluation"))
sys.path.insert(0, str(REPO / "research/m4_evaluation/frozen_rerun"))
from fast_period_fap import FastPeriodFAP  # noqa: E402

CACHE = REPO / "data/processed/m1"
OUT = REPO / "data/manifests/math_audit"
TAU_FLAT, SEED = 0.005, 20260619
_G: dict = {}


def _init():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = "1"
    global _G
    import pandas as pd
    import seal_loader as SL
    import injection as INJ
    man = pd.read_parquet(REPO / "data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    _G = {"fr": SL.load_frozen(), "man": man.set_index("tic"), "ld": INJ.constant_ld(), "INJ": INJ}


def _work(task):
    tic, P, Rp, b, seed = task
    fr, INJ = _G["fr"], _G["INJ"]
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    built = INJ.build_injection(t, P, Rp, b, _G["man"].loc[tic], _G["ld"],
                                np.random.default_rng(seed), host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    F = FastPeriodFAP(t, fr.duration_grid, 0.5, fr.z_star, fr.period_min_days, pmax, fr.oversampling)
    ev = F.detect(r)
    if ev.shape[0] < fr.n_min:
        return None
    t14 = float(ev[int(np.argmax(ev[:, 1])), 2])
    obs_R = F.best_R(ev[:, 0])
    Lb = fr.block_len_multiple * max(TAU_FLAT, t14)
    # identical RNG stream for both arms -> the only difference is which series is resampled
    f_dirty, _, _, ge_d = F.fap(r, obs_R, Lb, fr.B, np.random.default_rng(seed ^ 99))
    f_clean, _, _, ge_c = F.fap(r0, obs_R, Lb, fr.B, np.random.default_rng(seed ^ 99))
    k0 = F.detect(r0).shape[0]
    return dict(tic=tic, P=P, Rp=Rp, b=b, k_inj=int(ev.shape[0]), k_host=int(k0), obs_R=float(obs_R),
                fap_contaminated=float(f_dirty), fap_clean=float(f_clean),
                ge_contaminated=int(ge_d), ge_clean=int(ge_c),
                gate_contaminated=bool(f_dirty <= fr.alpha_fap),
                gate_clean=bool(f_clean <= fr.alpha_fap), n_transits=int(truth["n_transits"]))


def run(workers, per_cell):
    import pandas as pd
    from multiprocessing import Pool
    sys.path.insert(0, str(REPO / "research/m2_injection"))
    import injection as INJ
    man = pd.read_parquet(REPO / "data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv(REPO / "data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv(REPO / "data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    pool = man[(man.split == "calibration") & (man.rad > 0) & np.isfinite(man.logg) & np.isfinite(man.Teff)]
    pool = pool[pool.tic.isin((draw - exc) & avail)]
    assert not (set(pool.tic) & set(man[man.split == "test"].tic)), "TEST LEAK"
    hosts = pool.sample(min(80, len(pool)), random_state=22).tic.tolist()
    tasks, sc = [], 0
    for P in INJ.GRID_P:
        for Rp in INJ.GRID_R:
            for j in range(per_cell):
                tasks.append((hosts[sc % len(hosts)], P, Rp, INJ.GRID_B[j % len(INJ.GRID_B)],
                              SEED + sc))
                sc += 1
    print(f"[MATH-3] {len(tasks)} injections")
    t0 = time.time()
    rows = []
    with Pool(workers, initializer=_init) as p:
        for i, x in enumerate(p.imap_unordered(_work, tasks, chunksize=1), 1):
            if x:
                rows.append(x)
            if i % 25 == 0:
                print(f"  {i}/{len(tasks)}  {time.time()-t0:.0f}s", flush=True)
    d = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "surrogate_contamination.csv", index=False)
    print(f"[MATH-3] {len(d)} routed, {time.time()-t0:.0f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--per-cell", type=int, default=4)
    a = ap.parse_args()
    run(a.workers, a.per_cell)
