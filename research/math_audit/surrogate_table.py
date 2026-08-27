"""MATH-AUDIT — record the FULL block-bootstrap surrogate table for the period-FAP.

WHY. The sealed period-FAP (`frozen_rerun/period_recovery.period_fap`) collapses every
surrogate to a single bit: `R_b >= R_obs`. That discards the two quantities needed to
say *what the test is actually testing*: the surrogate's own event multiplicity `k_b`
and its comb resultant `R_b`. This module re-runs the sealed null model once and stores
`(k_b, R_b, span_b, nfreq_b)` for all B surrogates of every star, so that the FAP of ANY
statistic T(k, R) can be recomputed offline without touching a light curve again.

CORRECTNESS. The surrogate stream, the detector, the comb scan and the grid are the
sealed ones (via `fast_period_fap.FastPeriodFAP`, which INN-3 verified bit-identical to
the frozen code on 1126/1126 nulls). `verify` re-derives the sealed exceedance count
`ge = #{b: R_b >= R_obs}` from the stored table and asserts equality with the recorded
sealed value.  Nothing here changes a sealed threshold, statistic, alpha or verdict.

CALIBRATION ONLY. Reads `data/processed/m1/*.npz` (calibration hosts) and the M4
calibration injections. No TEST TIC is touched (P-5).
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
sys.path.insert(0, str(REPO / "research/m2_injection"))
sys.path.insert(0, str(REPO / "research/m4_evaluation"))
sys.path.insert(0, str(REPO / "research/m4_evaluation/frozen_rerun"))

from fast_period_fap import FastPeriodFAP  # noqa: E402

CACHE = REPO / "data/processed/m1"
OUT = REPO / "data/manifests/math_audit"

# --- sealed constants (Seal #2; mirrored from inn3_fap_acceleration.py, not re-derived) ---
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
B_SURROGATES = 1000
ALPHA_FAP = 0.01
Z_EXTRACT = 2.0
N_MIN = 2
BLOCK_LEN_MULTIPLE = 3
TAU_FLAT = 0.005
PERIOD_MIN = 0.5
PERIOD_MAX_FRAC_BASELINE = 0.5
OVERSAMPLING = 3
T14_M3_CONVENTION = 0.2          # m3_calibrate / RES-4 arm A convention for the null pool
SEED = 20260616


def _pin_threads():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = "1"


class InstrumentedFAP(FastPeriodFAP):
    """FastPeriodFAP + per-surrogate (k, R, span, nfreq) recording.

    `best_R_full` is `best_R` with the intermediate quantities returned; the returned R
    is produced by the identical float64 expression, so `R_b >= R_obs` is unchanged.
    """

    def best_R_full(self, epochs):
        if epochs.size < 2:
            return 0.0, 0.0, 0
        span = float(epochs.max() - epochs.min())
        p_max = min(self.p_max_cfg, span) if span > 0 else self.p_max_cfg
        if p_max <= self.p_min:
            return 0.0, span, 0
        df = 1.0 / (self.oversample * max(span, p_max))
        freqs = np.arange(1.0 / p_max, 1.0 / self.p_min, df)
        if freqs.size == 0:
            return 0.0, span, 0
        periods = 1.0 / freqs
        ang = 2 * np.pi * ((epochs[None, :] / periods[:, None]) % 1.0)
        R = np.hypot(np.cos(ang).mean(axis=1), np.sin(ang).mean(axis=1))
        scores = 1.0 - R
        return float(1.0 - scores[int(np.argmin(scores))]), span, int(freqs.size)

    def surrogate_table(self, r, block_len_days, n_surrogates, rng):
        """Run the sealed surrogate loop, recording (k, R, span, nfreq) per surrogate."""
        n, B = self.n, int(n_surrogates)
        blk = max(1, min(max(1, int(round(block_len_days / self.cad))), n))
        nblk = int(np.ceil(n / blk))
        r2 = np.concatenate([r, r])
        offs = np.arange(blk)[None, :]
        kk = np.empty(B, np.int32)
        RR = np.empty(B, np.float64)
        sp = np.empty(B, np.float64)
        nf = np.empty(B, np.int32)
        for b in range(B):
            starts = rng.integers(0, n, size=nblk)
            rs = r2[(starts[:, None] + offs).ravel()[:n]]
            ev = self.detect(rs)
            kk[b] = ev.shape[0]
            if ev.shape[0] >= 2:
                RR[b], sp[b], nf[b] = self.best_R_full(ev[:, 0])
            else:
                RR[b], sp[b], nf[b] = 0.0, 0.0, 0
        return kk, RR, sp, nf


# ============================================================== nulls
def _null_work(path):
    tic = Path(path).stem
    z = np.load(path)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    base = float(t.max() - t.min())
    p_min, p_max = PERIOD_MIN, PERIOD_MAX_FRAC_BASELINE * base
    if p_max <= p_min:
        return None
    F = InstrumentedFAP(t, DGRID, 0.5, Z_EXTRACT, p_min, p_max, OVERSAMPLING)
    ev = F.detect(r)
    if ev.shape[0] < N_MIN:
        return None
    obs_R, obs_span, obs_nf = F.best_R_full(ev[:, 0])
    Lb = BLOCK_LEN_MULTIPLE * max(TAU_FLAT, T14_M3_CONVENTION)
    seed = SEED ^ (int(tic) & 0x7FFFFFFF)
    kk, RR, sp, nf = F.surrogate_table(r, Lb, B_SURROGATES, np.random.default_rng(seed))
    return dict(tic=tic, k=int(ev.shape[0]), obs_R=float(obs_R), obs_span=float(obs_span),
                obs_nfreq=int(obs_nf), n_cadences=int(t.size), baseline=base, Lb=float(Lb),
                sur_k=kk, sur_R=RR, sur_span=sp, sur_nfreq=nf)


def run_nulls(workers, limit=None):
    _pin_threads()
    from multiprocessing import Pool
    paths = sorted(glob.glob(str(CACHE / "*.npz")))
    if limit:
        paths = paths[:limit]
    t0 = time.time()
    rows, K, R, S, NF = [], [], [], [], []
    with Pool(workers) as pool:
        for i, res in enumerate(pool.imap_unordered(_null_work, paths, chunksize=4), 1):
            if res is None:
                continue
            K.append(res.pop("sur_k")); R.append(res.pop("sur_R"))
            S.append(res.pop("sur_span")); NF.append(res.pop("sur_nfreq"))
            rows.append(res)
            if i % 100 == 0:
                print(f"  {i}/{len(paths)}  {time.time()-t0:.0f}s", flush=True)
    import pandas as pd
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "null_obs.csv", index=False)
    np.savez_compressed(OUT / "null_surrogates.npz", tic=np.array(df.tic.values, dtype="U16"),
                        k=np.array(K), R=np.array(R), span=np.array(S), nfreq=np.array(NF))
    print(f"[nulls] {len(df)} stars, {time.time()-t0:.0f}s -> {OUT}")


# ============================================================== injections
def _inj_init():
    _pin_threads()
    global _G
    import pandas as pd
    import seal_loader as SL
    import injection as INJ
    fr = SL.load_frozen()
    man = pd.read_parquet(REPO / "data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    man = man.set_index("tic")
    _G = {"fr": fr, "man": man, "ld": INJ.constant_ld(), "INJ": INJ,
          "stellar": {"u1": 0.4, "u2": 0.25}}


def _inj_work(task):
    tic, P, Rp, b, seed = task
    G = _G
    fr, INJ = G["fr"], G["INJ"]
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    built = INJ.build_injection(t, P, Rp, b, G["man"].loc[tic], G["ld"],
                                np.random.default_rng(seed), host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    F = InstrumentedFAP(t, fr.duration_grid, 0.5, fr.z_star, fr.period_min_days, pmax,
                        fr.oversampling)
    ev = F.detect(r)
    if ev.shape[0] < fr.n_min:
        return None
    kmax = int(np.argmax(ev[:, 1]))
    t0_hat, t14 = float(ev[kmax, 0]), float(ev[kmax, 2])   # m4_driver:120 (duration-matched T14)
    obs_R, obs_span, obs_nf = F.best_R_full(ev[:, 0])
    # sealed period seed + sealed recovery predicate, so recall can be scored per statistic
    from period_recovery import best_period as _bp
    import recovery as REC
    P_hat = _bp(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)[0]
    p_ok = bool(REC._period_match(P_hat, truth["P_true"])[0]) if np.isfinite(P_hat) else False
    e_ok = bool(REC._epoch_match(t0_hat, P_hat, truth["t0_true"], truth["t14_true"])) \
        if np.isfinite(P_hat) else False
    Lb = fr.block_len_multiple * max(TAU_FLAT, t14)
    rng = np.random.default_rng(seed ^ 99)
    kk, RR, sp, nf = F.surrogate_table(r, Lb, fr.B, rng)
    return dict(tic=tic, P=P, Rp=Rp, b=b, seed=int(seed), k=int(ev.shape[0]),
                obs_R=float(obs_R), obs_span=float(obs_span), obs_nfreq=int(obs_nf),
                P_hat=float(P_hat) if np.isfinite(P_hat) else np.nan,
                period_match=p_ok, epoch_match=e_ok, seed_correct=bool(p_ok and e_ok),
                t14_seeded=t14, t0_hat=t0_hat, Lb=float(Lb),
                P_true=float(truth["P_true"]), t0_true=float(truth["t0_true"]),
                t14_true=float(truth["t14_true"]), n_transits=int(truth["n_transits"]),
                sur_k=kk, sur_R=RR, sur_span=sp, sur_nfreq=nf)


def run_injections(workers, per_cell):
    """Task construction MIRRORS inn3_fap_acceleration.run_injections exactly (same host
    draw, same cells, same seeds) so rows are comparable to `inn3_injections.csv`."""
    _pin_threads()
    import pandas as pd
    from multiprocessing import Pool
    import injection as INJ
    man = pd.read_parquet(REPO / "data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv(REPO / "data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv(REPO / "data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    pool = man[(man.split == "calibration") & (man.rad > 0) & np.isfinite(man.logg)
               & np.isfinite(man.Teff)]
    pool = pool[pool.tic.isin((draw - exc) & avail)]
    assert not (set(pool.tic) & set(man[man.split == "test"].tic)), "TEST LEAK"
    hosts = pool.sample(min(80, len(pool)), random_state=22).tic.tolist()
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    tasks, sc = [], 0
    for (P, Rp) in cells:
        for j in range(per_cell):
            tasks.append((hosts[sc % len(hosts)], P, Rp, INJ.GRID_B[j % len(INJ.GRID_B)],
                          20260619 + sc))
            sc += 1
    print(f"[inj] {len(tasks)} injections, {len(cells)} cells, {len(hosts)} calibration hosts")
    t0 = time.time()
    rows, K, R, S, NF = [], [], [], [], []
    with Pool(workers, initializer=_inj_init) as pool:
        for n, res in enumerate(pool.imap_unordered(_inj_work, tasks, chunksize=2), 1):
            if res is None:
                continue
            K.append(res.pop("sur_k")); R.append(res.pop("sur_R"))
            S.append(res.pop("sur_span")); NF.append(res.pop("sur_nfreq"))
            rows.append(res)
            if n % 50 == 0:
                print(f"  {n}/{len(tasks)}  {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "inj_obs.csv", index=False)
    np.savez_compressed(OUT / "inj_surrogates.npz", k=np.array(K), R=np.array(R),
                        span=np.array(S), nfreq=np.array(NF))
    print(f"[inj] {len(df)} injections, {time.time()-t0:.0f}s -> {OUT}")


# ============================================================== verify
def verify():
    """Re-derive the sealed exceedance count from the stored table; must match INN-3."""
    import pandas as pd
    obs = pd.read_csv(OUT / "null_obs.csv")
    z = np.load(OUT / "null_surrogates.npz")
    R = z["R"]
    ge = (R >= obs.obs_R.values[:, None]).sum(axis=1)
    ref = pd.read_csv(REPO / "data/manifests/m4/inn3/inn3_nulls.csv")
    ref["tic"] = ref.tic.astype(str)
    obs["tic"] = obs.tic.astype(str)
    m = obs.assign(ge_new=ge).merge(ref[["tic", "k", "obs_R", "ge_full"]], on="tic",
                                    suffixes=("", "_ref"))
    dk = int((m.k != m.k_ref).sum())
    dR = float(np.abs(m.obs_R - m.obs_R_ref).max())
    dge = int((m.ge_new != m.ge_full).sum())
    print(f"[verify] matched {len(m)} stars vs INN-3")
    print(f"  k mismatches      : {dk}")
    print(f"  max |dR|          : {dR:.3e}")
    print(f"  ge mismatches     : {dge}   (max |d| = {int(np.abs(m.ge_new-m.ge_full).max())})")
    ok = (dk == 0 and dR == 0.0 and dge == 0)
    print(f"  BIT-IDENTICAL     : {ok}")
    json.dump({"n_matched": len(m), "k_mismatch": dk, "max_abs_dR": dR,
               "ge_mismatch": dge, "bit_identical": bool(ok)},
              open(OUT / "verify_surrogate_table.json", "w"), indent=2)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["nulls", "injections", "verify"])
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--per-cell", type=int, default=10)
    a = ap.parse_args()
    if a.cmd == "nulls":
        run_nulls(a.workers, a.limit)
    elif a.cmd == "injections":
        run_injections(a.workers, a.per_cell)
    else:
        verify()


if __name__ == "__main__":
    main()
