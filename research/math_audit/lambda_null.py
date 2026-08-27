"""MATH-AUDIT / roadmap MATH-4 — empirical null distribution of the confirmer statistic Lambda,
and the realized null pass-rate of the "physics decides" gate at the sealed operating point.

WHAT IS OPEN. Roadmap MATH-4 asks for the empirical null of the GP likelihood-ratio with an
ESTIMATED covariance K, against chi^2_1, and for the size of the deviation that the empirical
T_red calibration absorbed. Nothing has been run.

WHAT THIS ADDS. The sealed T_red is 0.0 (`TRED_CALIBRATION_RESULT.md`), and `confirmer.transit_lr_gp`
returns Lambda := 0 whenever delta_hat <= 0. So `Lambda >= T_red` is satisfied by EVERY input, and
the sealed confirmation reduces algebraically to

    confirmed  <=>  (delta_hat > 0)  AND  shape_pass          [odd/even + no-secondary]

i.e. a one-bit SIGN test plus two vetoes. Erratum 2.9 and audit 3.4 state that the timing gate is
the binding arbiter; neither measures what the photometric gate's null pass rate actually is. This
module measures it, and separately measures the Lambda null so the size of the discarded
discrimination can be quantified.

DESIGN (calibration only; no TEST TIC, P-5)
  * ephemeris "seed"   : the sealed route-and-seed ephemeris (detector -> best_period -> argmax-SNR
                         epoch), i.e. exactly what the sealed confirmer is fed on a null star.
  * ephemeris "random" : n_rand ephemerides drawn from the sealed search support
                         (P ~ loguniform[p_min, 0.5*baseline], t0 ~ U[t_min, t_min+P]) -> the null
                         law of Lambda free of the seeding step.
  For each we record Lambda, delta_hat, n_in, n_transits, sign_pass, shape_pass and the two vetoes
  separately, so P(confirm | H0) can be decomposed.

NOTHING SEALED IS TOUCHED. Read-only on cached calibration residuals; no threshold, statistic,
weight, manifest or tag is modified.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "research/m4_evaluation"))
sys.path.insert(0, str(REPO / "research/m4_evaluation/frozen_rerun"))

CACHE = REPO / "data/processed/m1"
OUT = REPO / "data/manifests/math_audit"

DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
Z_STAR = 3.4          # Seal #2 routing threshold (m4_driver uses fr.z_star for detection)
Z_EXTRACT = 2.0       # M3/RES-4/INN-3 null-pool extraction floor
N_MIN = 2
PERIOD_MIN = 0.5
PERIOD_MAX_FRAC_BASELINE = 0.5
OVERSAMPLING = 3
STELLAR = {"u1": 0.4, "u2": 0.25}
SEED = 20260827


def _pin():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = "1"


def _work(a):
    path, n_rand = a
    import confirmer as CF
    from detector import detect_events
    from period_recovery import best_period
    tic = Path(path).stem
    z = np.load(path)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    base = float(t.max() - t.min())
    pmax = PERIOD_MAX_FRAC_BASELINE * base
    if pmax <= PERIOD_MIN:
        return []
    rows = []

    def record(kind, P, t0, T14):
        lam, delta, nin = CF.transit_lr_gp(t, r, P, t0, T14, STELLAR)
        ntr = CF.n_transits(t, P, t0, T14)
        oe = bool(CF.odd_even_consistent(t, r, P, t0, T14, STELLAR)) if ntr >= 2 else True
        ns = bool(CF.no_secondary(t, r, P, t0, T14, STELLAR))
        shape = (oe and ns) if ntr >= 2 else ns
        rows.append(dict(tic=tic, kind=kind, P=float(P), t0=float(t0), T14=float(T14),
                         Lambda=float(lam), delta=float(delta), n_in=int(nin),
                         n_transits=int(ntr), sign_pass=bool(delta > 0),
                         odd_even_pass=oe, no_secondary_pass=ns, shape_pass=bool(shape),
                         confirmed_Tred0=bool(lam >= 0.0 and delta > 0 and shape)))

    # --- the sealed seed ephemeris (what the confirmer is actually fed) ---
    ev = detect_events(t, r, DGRID, 0.5, Z_STAR)
    if ev.shape[0] >= N_MIN:
        km = int(np.argmax(ev[:, 1]))
        P_hat = best_period(ev[:, 0], PERIOD_MIN, pmax, OVERSAMPLING)[0]
        if np.isfinite(P_hat):
            record("seed", P_hat, float(ev[km, 0]), float(ev[km, 2]))

    # --- random ephemerides from the sealed search support ---
    rng = np.random.default_rng(SEED ^ (int(tic) & 0x7FFFFFFF))
    for _ in range(n_rand):
        P = float(np.exp(rng.uniform(np.log(PERIOD_MIN), np.log(pmax))))
        t0 = float(t.min() + rng.uniform(0.0, P))
        T14 = float(rng.choice(DGRID))
        record("random", P, t0, T14)
    return rows


def run(workers, n_rand, limit):
    _pin()
    from multiprocessing import Pool
    import pandas as pd
    paths = sorted(glob.glob(str(CACHE / "*.npz")))
    if limit:
        paths = paths[:limit]
    tasks = [(p, n_rand) for p in paths]
    t0 = time.time()
    out = []
    with Pool(workers) as pool:
        for i, rs in enumerate(pool.imap_unordered(_work, tasks, chunksize=2), 1):
            out.extend(rs)
            if i % 100 == 0:
                print(f"  {i}/{len(tasks)}  {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(out)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "lambda_null.csv", index=False)
    print(f"[lambda] {len(df)} rows from {df.tic.nunique()} stars in {time.time()-t0:.0f}s")
    print(df.groupby("kind").size())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--n-rand", type=int, default=20)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    run(a.workers, a.n_rand, a.limit)
