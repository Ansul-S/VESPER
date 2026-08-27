"""MATH-AUDIT — is the surrogate maximised over the SAME period grid as the observation?

MATH v1.2 §9 states the look-elsewhere absorption as a premise:

    "recompute the maximized statistic T^(b) = max_P Z^(b)(P) over the **identical** grid ...
     Because each surrogate is maximized over the same N_P periods, the look-elsewhere effect
     is **automatically** absorbed"

and audit 2026-07-19 §3.3 certifies it: "the max-over-grid selection effect is handled
correctly because the null distribution is built from the same max-over-grid statistic on
surrogates". The implementation does not do this. `period_recovery.best_period` derives the
grid from the epochs it is handed:

    span   = epochs.max() - epochs.min()          # SURROGATE's span
    p_max  = min(p_max, span)
    df     = 1 / (oversample * max(span, p_max))  # SURROGATE's resolution
    freqs  = arange(1/p_max, 1/p_min, df)

so every surrogate is maximised over its own grid, whose size varies with its own event
multiplicity and time span.

THIS SCRIPT re-runs the identical surrogate stream and scores each surrogate BOTH ways:
  R_own   — the sealed value (grid from the surrogate's own epochs)
  R_fixed — the same epochs scored on the OBSERVED star's grid (MATH §9 as written)
and reports the resulting change in the exceedance count and in gate membership.

Calibration only. Nothing sealed is modified; this measures a discrepancy, it does not fix one.
"""
from __future__ import annotations

import argparse
import glob
import os
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "research/m4_evaluation"))
sys.path.insert(0, str(REPO / "research/m4_evaluation/frozen_rerun"))
from fast_period_fap import FastPeriodFAP  # noqa: E402

CACHE = REPO / "data/processed/m1"
OUT = REPO / "data/manifests/math_audit"
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
B_SURROGATES, ALPHA, Z_EXTRACT, N_MIN = 1000, 0.01, 2.0, 2
BLOCK_LEN_MULTIPLE, TAU_FLAT, T14_CONV = 3, 0.005, 0.2
PERIOD_MIN, PERIOD_MAX_FRAC, OVERSAMPLING, SEED = 0.5, 0.5, 3, 20260616


def _pin():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = "1"


class GridFAP(FastPeriodFAP):
    def R_on(self, epochs, freqs):
        """Resultant maximised over a PRESCRIBED frequency grid (sealed float expression)."""
        if epochs.size < 2 or freqs.size == 0:
            return 0.0
        periods = 1.0 / freqs
        ang = 2 * np.pi * ((epochs[None, :] / periods[:, None]) % 1.0)
        R = np.hypot(np.cos(ang).mean(axis=1), np.sin(ang).mean(axis=1))
        scores = 1.0 - R
        return float(1.0 - scores[int(np.argmin(scores))])

    def own_grid(self, epochs):
        span = float(epochs.max() - epochs.min())
        p_max = min(self.p_max_cfg, span) if span > 0 else self.p_max_cfg
        if p_max <= self.p_min:
            return np.empty(0)
        df = 1.0 / (self.oversample * max(span, p_max))
        return np.arange(1.0 / p_max, 1.0 / self.p_min, df)


def _work(path):
    tic = Path(path).stem
    z = np.load(path)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    base = float(t.max() - t.min())
    p_max = PERIOD_MAX_FRAC * base
    if p_max <= PERIOD_MIN:
        return None
    F = GridFAP(t, DGRID, 0.5, Z_EXTRACT, PERIOD_MIN, p_max, OVERSAMPLING)
    ev = F.detect(r)
    if ev.shape[0] < N_MIN:
        return None
    obs_grid = F.own_grid(ev[:, 0])
    obs_R = F.R_on(ev[:, 0], obs_grid)

    Lb = BLOCK_LEN_MULTIPLE * max(TAU_FLAT, T14_CONV)
    n = F.n
    blk = max(1, min(max(1, int(round(Lb / F.cad))), n))
    nblk = int(np.ceil(n / blk))
    r2 = np.concatenate([r, r])
    offs = np.arange(blk)[None, :]
    rng = np.random.default_rng(SEED ^ (int(tic) & 0x7FFFFFFF))
    ge_own = ge_fix = 0
    for _ in range(B_SURROGATES):
        starts = rng.integers(0, n, size=nblk)
        rs = r2[(starts[:, None] + offs).ravel()[:n]]
        e = F.detect(rs)
        if e.shape[0] >= 2:
            Rown = F.R_on(e[:, 0], F.own_grid(e[:, 0]))
            Rfix = F.R_on(e[:, 0], obs_grid)
        else:
            Rown = Rfix = 0.0
        ge_own += Rown >= obs_R
        ge_fix += Rfix >= obs_R
    return dict(tic=tic, k=int(ev.shape[0]), obs_R=float(obs_R), obs_nfreq=int(obs_grid.size),
                ge_own=int(ge_own), ge_fixed=int(ge_fix),
                gate_own=bool((ge_own + 1) / 1001 <= ALPHA),
                gate_fixed=bool((ge_fix + 1) / 1001 <= ALPHA))


def run(workers, limit):
    _pin()
    import pandas as pd
    from multiprocessing import Pool
    paths = sorted(glob.glob(str(CACHE / "*.npz")))
    if limit:
        paths = paths[:limit]
    t0 = time.time()
    rows = []
    with Pool(workers) as pool:
        for i, x in enumerate(pool.imap_unordered(_work, paths, chunksize=4), 1):
            if x:
                rows.append(x)
            if i % 200 == 0:
                print(f"  {i}/{len(paths)}  {time.time()-t0:.0f}s", flush=True)
    d = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "grid_identity.csv", index=False)
    print(f"[grid] {len(d)} stars, {time.time()-t0:.0f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    run(a.workers, a.limit)
