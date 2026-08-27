"""INN-3 — equivalence + speed validation of the exact accelerated period-FAP.

Roadmap INN-3 asks for "the provably-equivalent cheap period-FAP estimator ... the
replacement for the falsified lever, designed with proof obligations stated". This
script supplies the evidence for one, on the sealed Lever-1b criteria
(`LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md` §4, tolerances fixed before results):

    (i)   FAP agreement       p95 |dFAP| <= 0.005
    (ii)  gate membership     discordant <= 8 AND 0 nulls admitted that the reference rejects
    (iii) recall safety       0 reference-pass recoveries clipped

E-EVT and E-LUT failed all three. The estimator validated here returns the SAME
value, so every criterion is met with an exact zero — the equivalence proof is the
identity map. Its speed comes from removing loop invariants and from curtailed
sampling, neither of which is a statistical approximation.

SUBCOMMANDS
  nulls        1126 cached calibration-null residuals: reproduce the sealed recorded
               FAP (exceedance count ge), measure the speed of all three paths.
  injections   sealed M4 routing path replayed on calibration injections across the
               sealed (P, Rp) grid: criteria (i)-(iii) on a planet-bearing sample.
  survey       full-grid TLS cost on calibration nulls -> rho_d and pi* for a
               SURVEY-representative (planetless) star, which is the population pi*
               is actually about.
  project      counterfactual re-analysis of the E2 endpoint from the two recorded
               artifacts (timing ledger + sealed recovery.csv). Arithmetic only:
               TEST light curves are NOT re-read (P-5) and nothing sealed is edited.

SAFETY. Calibration only. No network. No sealed artifact written. The frozen module
snapshot (`frozen_rerun/`) is imported first, exactly as `e2_retiming.py` does, so the
reference is the code that actually ran.

Run:  .venv/bin/python research/m4_evaluation/inn3_fap_acceleration.py nulls --workers 6
Out:  data/manifests/m4/inn3/
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "research/m2_injection"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "frozen_rerun"))          # SEALED CODE PATH FIRST (e2_retiming convention)

from detector import detect_events                       # noqa: E402 (frozen)
from period_recovery import best_period, period_fap      # noqa: E402 (frozen)
from fast_period_fap import FastPeriodFAP, curtail_threshold  # noqa: E402

OUT = REPO / "data/manifests/m4/inn3"
CACHE = REPO / "data/processed/m1"

# --- sealed constants (Seal #2; mirrored, not re-derived) ---
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
T14_M3_CONVENTION = 0.2          # m3_calibrate: median(duration_grid); see the note in `nulls`
SEED = 20260616
CURTAIL = curtail_threshold(ALPHA_FAP, B_SURROGATES)     # == 10

_G: dict = {}


def _machine(workers):
    return {"platform": platform.platform(), "python": sys.version.split()[0],
            "numpy": np.__version__, "workers": workers,
            "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}


def _pin_threads():
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
              "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
        os.environ[v] = "1"


# ============================================================== nulls
def _null_work(a):
    tic, path, fap_ref, lb_ref, do_sealed = a
    z = np.load(path)
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    base = float(t.max() - t.min())
    p_min, p_max = PERIOD_MIN, PERIOD_MAX_FRAC_BASELINE * base
    if p_max <= p_min:
        return None
    F = FastPeriodFAP(t, DGRID, 0.5, Z_EXTRACT, p_min, p_max, OVERSAMPLING)
    ev = F.detect(r)
    if ev.shape[0] < N_MIN:
        return None
    obs_R = F.best_R(ev[:, 0])
    seed = SEED ^ (int(tic) & 0x7FFFFFFF)

    c0 = time.process_time()
    f_full, _, _, ge_full = F.fap(r, obs_R, lb_ref, B_SURROGATES, np.random.default_rng(seed))
    t_full = time.process_time() - c0
    c0 = time.process_time()
    f_cur, n_cur, cur, _ = F.fap(r, obs_R, lb_ref, B_SURROGATES, np.random.default_rng(seed),
                                 curtail_ge=CURTAIL)
    t_cur = time.process_time() - c0

    t_sealed, ge_sealed_live = np.nan, np.nan
    if do_sealed:
        ev_s = detect_events(t, r, DGRID, 0.5, Z_EXTRACT)
        obs_R_s = best_period(ev_s[:, 0], p_min, p_max, OVERSAMPLING)[2]
        c0 = time.process_time()
        fs, _ = period_fap(t, r, obs_R_s, TAU_FLAT, T14_M3_CONVENTION, DGRID, p_min, p_max,
                           Z_EXTRACT, BLOCK_LEN_MULTIPLE, B_SURROGATES,
                           np.random.default_rng(seed))
        t_sealed = time.process_time() - c0
        ge_sealed_live = round(fs * (B_SURROGATES + 1) - 1)

    return dict(tic=tic, k=int(ev.shape[0]), obs_R=float(obs_R),
                ge_ref=int(round(fap_ref * (B_SURROGATES + 1) - 1)),
                ge_full=int(ge_full), gate_ref=bool(fap_ref <= ALPHA_FAP),
                gate_full=bool(f_full <= ALPHA_FAP), gate_cur=bool(f_cur <= ALPHA_FAP),
                n_cur=int(n_cur), curtailed=bool(cur), t_full=float(t_full),
                t_cur=float(t_cur), t_sealed=float(t_sealed),
                ge_sealed_live=float(ge_sealed_live))


def run_nulls(a):
    """Reference = RES-4 arm A at T14 = 0.2 d, itself verified bitwise against the
    sealed M3 per-star FAPs (968/968). Identity is tested on the DISCRETE exceedance
    count ge = FAP*(B+1)-1: the recorded FAPs went through a CSV text round-trip that
    perturbs the last ULP of the float, while ge is the actual sufficient statistic."""
    ref = pd.read_csv(REPO / "data/manifests/m4/wave1/res4_per_star.csv")
    ref["tic"] = ref["tic"].astype(str)
    ref = ref[np.isfinite(ref["fap_A_0.2"])].set_index("tic")
    tasks = []
    for p in sorted(glob.glob(str(CACHE / "*.npz"))):
        tic = Path(p).stem
        if tic not in ref.index:
            continue
        row = ref.loc[tic]
        tasks.append((tic, p, float(row["fap_A_0.2"]), float(row["Lb_A_0.2"]), False))
    if a.limit:
        tasks = tasks[:a.limit]
    for i in range(min(a.sealed_n, len(tasks))):
        tasks[i] = tasks[i][:4] + (True,)
    print(f"[INN-3 nulls] {len(tasks)} calibration nulls (sealed impl re-run on {a.sealed_n})",
          flush=True)

    from multiprocessing import Pool
    res = []
    with Pool(a.workers) as pool:
        for i, x in enumerate(pool.imap_unordered(_null_work, tasks, chunksize=2), 1):
            if x:
                res.append(x)
            if i % 100 == 0:
                print(f"  {i}/{len(tasks)}", flush=True)
    d = pd.DataFrame(res)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "inn3_nulls.csv", index=False)

    sd = d[np.isfinite(d.t_sealed)]
    s = {
        "task": "INN-3 exact accelerated period-FAP — calibration nulls",
        "reference": "data/manifests/m4/wave1/res4_per_star.csv arm A, T14=0.2 d (L_b=0.6 d)",
        "identity_metric": "exceedance count ge = FAP*(B+1)-1 (CSV-roundtrip-safe)",
        "n_stars": len(d),
        "ge_identical_to_sealed_record": int((d.ge_full == d.ge_ref).sum()),
        "ge_max_abs_diff": int((d.ge_full - d.ge_ref).abs().max()),
        "gate_identical_full_B": int((d.gate_full == d.gate_ref).sum()),
        "gate_identical_curtailed": int((d.gate_cur == d.gate_ref).sum()),
        "n_gate_open": int(d.gate_ref.sum()),
        "n_curtailed": int(d.curtailed.sum()),
        "surrogates_used_mean": float(d.n_cur.mean()),
        "surrogates_used_median": float(d.n_cur.median()),
        "cpu_mean_s": {"leverA_full_B": float(d.t_full.mean()),
                       "leverAB_curtailed": float(d.t_cur.mean())},
    }
    if len(sd):
        s["sealed_reference_subset"] = {
            "n": int(len(sd)),
            "ge_identical_live_rerun": int((sd.ge_sealed_live == sd.ge_full).sum()),
            "cpu_mean_s_sealed": float(sd.t_sealed.mean()),
            "speedup_leverA": float(sd.t_sealed.sum() / sd.t_full.sum()),
            "speedup_leverA_plus_B": float(sd.t_sealed.sum() / sd.t_cur.sum()),
        }
    s["machine"] = _machine(a.workers)
    (OUT / "inn3_nulls.json").write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))


# ========================================================= injections
def _inj_init():
    import seal_loader as SL
    import injection as INJ
    _G["fr"] = SL.load_frozen()
    _G["ld"] = INJ.constant_ld()
    _G["INJ"] = INJ
    man = pd.read_parquet(REPO / "data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    _G["man"] = man.set_index("tic")


def _inj_work(task):
    tic, P, Rp, b, seed = task
    fr, INJ = _G["fr"], _G["INJ"]
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    built = INJ.build_injection(t, P, Rp, b, _G["man"].loc[tic], _G["ld"],
                                np.random.default_rng(seed), host_mode="cached_residual",
                                r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    if ev.shape[0] < fr.n_min:
        return None
    # NOTE: m4_driver.py:117 initialises t14 to median(duration_grid) but line 120
    # OVERWRITES it with the seeded event's own duration before the FAP call on line
    # 126. The M4 arm therefore duration-MATCHED T14; replicate that here.
    k = int(np.argmax(ev[:, 1]))
    t14 = float(ev[k, 2])
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    P_hat, _, obs_R = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)
    if not np.isfinite(P_hat):
        return None
    sfap = seed ^ 99

    c0 = time.process_time()
    f_sealed, lb = period_fap(t, r, obs_R, TAU_FLAT, t14, fr.duration_grid, fr.period_min_days,
                              pmax, fr.z_star, fr.block_len_multiple, fr.B,
                              np.random.default_rng(sfap))
    t_sealed = time.process_time() - c0
    F = FastPeriodFAP(t, fr.duration_grid, 0.5, fr.z_star, fr.period_min_days, pmax,
                      fr.oversampling)
    c0 = time.process_time()
    f_full, _, _, _ = F.fap(r, obs_R, lb, fr.B, np.random.default_rng(sfap))
    t_full = time.process_time() - c0
    c0 = time.process_time()
    f_cur, n_cur, cur, _ = F.fap(r, obs_R, lb, fr.B, np.random.default_rng(sfap),
                                 curtail_ge=CURTAIL)
    t_cur = time.process_time() - c0

    al = fr.alpha_fap
    return dict(tic=tic, P=P, Rp=Rp, b=b, k=int(ev.shape[0]), t14_seeded=t14, Lb=float(lb),
                obs_R=float(obs_R), P_hat=float(P_hat), P_true=float(truth["P_true"]),
                fap_sealed=float(f_sealed), fap_full=float(f_full), fap_cur=float(f_cur),
                bitexact=bool(f_sealed == f_full), gate_sealed=bool(f_sealed <= al),
                gate_full=bool(f_full <= al), gate_cur=bool(f_cur <= al),
                n_cur=int(n_cur), curtailed=bool(cur), t_sealed=float(t_sealed),
                t_full=float(t_full), t_cur=float(t_cur))


def run_injections(a):
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
        for j in range(a.per_cell):
            tasks.append((hosts[sc % len(hosts)], P, Rp, INJ.GRID_B[j % len(INJ.GRID_B)],
                          20260619 + sc)); sc += 1
    print(f"[INN-3 injections] {len(tasks)} injections, {len(cells)} cells, "
          f"{len(hosts)} calibration hosts", flush=True)

    from multiprocessing import Pool
    res = []
    with Pool(a.workers, initializer=_inj_init) as pool_:
        for i, x in enumerate(pool_.imap_unordered(_inj_work, tasks, chunksize=1), 1):
            if x:
                res.append(x)
            if i % 25 == 0:
                print(f"  {i}/{len(tasks)} ({len(res)} routed)", flush=True)
    d = pd.DataFrame(res)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "inn3_injections.csv", index=False)

    dfap = np.abs(d.fap_full - d.fap_sealed)
    s = {
        "task": "INN-3 exact accelerated period-FAP — calibration injections",
        "n_routed_injections": len(d),
        "lever1b_criteria": {
            "i_fap_agreement_p95_abs_dFAP": float(np.percentile(dfap, 95)),
            "i_threshold": 0.005,
            "i_pass": bool(np.percentile(dfap, 95) <= 0.005),
            "ii_gate_discordant_full_B": int((d.gate_full != d.gate_sealed).sum()),
            "ii_gate_discordant_curtailed": int((d.gate_cur != d.gate_sealed).sum()),
            "ii_threshold_discordant": 8,
            "ii_fp_admitted_full_B": int((~d.gate_sealed & d.gate_full).sum()),
            "ii_fp_admitted_curtailed": int((~d.gate_sealed & d.gate_cur).sum()),
            "iii_recoveries_clipped_full_B": int((d.gate_sealed & ~d.gate_full).sum()),
            "iii_recoveries_clipped_curtailed": int((d.gate_sealed & ~d.gate_cur).sum()),
        },
        "n_bitexact_fap": int(d.bitexact.sum()),
        "max_abs_dFAP": float(dfap.max()),
        "n_gate_open_sealed": int(d.gate_sealed.sum()),
        "surrogates_used_mean": float(d.n_cur.mean()),
        "surrogates_used_median": float(d.n_cur.median()),
        "cpu_mean_s": {"sealed": float(d.t_sealed.mean()), "leverA": float(d.t_full.mean()),
                       "leverAB": float(d.t_cur.mean())},
        "speedup_leverA": float(d.t_sealed.sum() / d.t_full.sum()),
        "speedup_leverA_plus_B": float(d.t_sealed.sum() / d.t_cur.sum()),
        "t14_seeded_distribution": {str(k): int(v) for k, v in
                                    d.t14_seeded.value_counts().sort_index().items()},
        "machine": _machine(a.workers),
    }
    (OUT / "inn3_injections.json").write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))


# ============================================================= survey
def _survey_init():
    import seal_loader as SL
    _G["fr"] = SL.load_frozen()


def _survey_work(tic):
    import arms as ARMS
    fr = _G["fr"]
    z = np.load(CACHE / f"{tic}.npz")
    t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    ARMS.arm_a_full(t, r, fr)                                   # JIT warm-up, untimed
    ts = []
    for _ in range(3):
        c0 = time.process_time(); ARMS.arm_a_full(t, r, fr); ts.append(time.process_time() - c0)
    c_full = float(np.median(ts))
    c0 = time.process_time()
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    t_det = time.process_time() - c0
    if ev.shape[0] < fr.n_min:
        return dict(tic=tic, c_full=c_full, routed=False, t_det=t_det)
    k = int(np.argmax(ev[:, 1])); t14 = float(ev[k, 2])
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    P_hat, _, obs_R = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)
    if not np.isfinite(P_hat):
        return dict(tic=tic, c_full=c_full, routed=False, t_det=t_det)
    seed = SEED ^ (int(tic) & 0x7FFFFFFF)
    c0 = time.process_time()
    f_s, lb = period_fap(t, r, obs_R, TAU_FLAT, t14, fr.duration_grid, fr.period_min_days, pmax,
                         fr.z_star, fr.block_len_multiple, fr.B, np.random.default_rng(seed))
    t_sealed = time.process_time() - c0
    F = FastPeriodFAP(t, fr.duration_grid, 0.5, fr.z_star, fr.period_min_days, pmax,
                      fr.oversampling)
    c0 = time.process_time()
    f_f, _, _, ge = F.fap(r, obs_R, lb, fr.B, np.random.default_rng(seed))
    t_vec = time.process_time() - c0
    c0 = time.process_time()
    f_c, nc, _, _ = F.fap(r, obs_R, lb, fr.B, np.random.default_rng(seed), curtail_ge=CURTAIL)
    t_cur = time.process_time() - c0
    return dict(tic=tic, c_full=c_full, routed=True, t14=t14, ge=int(ge), t_det=t_det,
                fap_sealed=float(f_s), fap_vec=float(f_f), fap_cur=float(f_c),
                bitexact=bool(f_s == f_f), gate_sealed=bool(f_s <= fr.alpha_fap),
                gate_cur=bool(f_c <= fr.alpha_fap), t_sealed_fap=t_sealed,
                t_vec_fap=t_vec, t_cur_fap=t_cur, n_cur=int(nc))


def run_survey(a):
    """pi* is a survey-scale quantity: rho_d belongs to a survey-REPRESENTATIVE star,
    which is overwhelmingly planetless. The sealed E2 measured rho_d on fast-path-
    eligible injections. Under the sealed (uncurtailed) estimator the distinction was
    immaterial — B=1000 always. Under exact curtailment it is not: nulls curtail far
    harder, because a null's own comb is easy for its surrogates to beat."""
    ref = pd.read_csv(REPO / "data/manifests/m4/wave1/res4_per_star.csv")
    ref["tic"] = ref["tic"].astype(str)
    tics = sorted(ref[np.isfinite(ref["fap_A_0.2"])]["tic"])
    rng = np.random.default_rng(20260817)
    sel = [tics[i] for i in rng.choice(len(tics), size=min(a.limit or 30, len(tics)),
                                       replace=False)]
    print(f"[INN-3 survey] full-grid TLS + FAP on {len(sel)} calibration nulls", flush=True)
    from multiprocessing import Pool
    res = []
    with Pool(a.workers, initializer=_survey_init) as pool:
        for i, x in enumerate(pool.imap_unordered(_survey_work, sel, chunksize=1), 1):
            res.append(x)
            if i % 5 == 0:
                print(f"  {i}/{len(sel)}", flush=True)
    d = pd.DataFrame(res)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "inn3_survey.csv", index=False)
    rt = d[d.routed == True]                                    # noqa: E712
    sp_vec = float(rt.t_sealed_fap.sum() / rt.t_vec_fap.sum())
    routed_frac = float(len(rt) / len(d))
    # per-star routing-stage cost, charged on EVERY star (routed or not: the detector
    # always runs; the FAP only when >= N_min events are found)
    det_all = float(d.t_det.sum())
    s = {
        "task": "INN-3 — survey-representative rho_d and pi*",
        "n_nulls": len(d), "n_routed": int(len(rt)), "routed_fraction": routed_frac,
        "c_full_mean_s": float(d.c_full.mean()), "c_full_median_s": float(d.c_full.median()),
        "fap_bitexact": int(rt.bitexact.sum()),
        "gate_identical_curtailed": int((rt.gate_cur == rt.gate_sealed).sum()),
        "surrogates_used_mean": float(rt.n_cur.mean()),
        "speedup_leverA": sp_vec,
        "speedup_leverA_plus_B": float(rt.t_sealed_fap.sum() / rt.t_cur_fap.sum()),
        "rho_d_null_population": {
            "sealed": float((rt.t_sealed_fap.sum() + det_all) / d.c_full.sum()),
            "leverA": float((rt.t_vec_fap.sum() + det_all / sp_vec) / d.c_full.sum()),
            "leverA_plus_B": float((rt.t_cur_fap.sum() + det_all / sp_vec) / d.c_full.sum()),
        },
        "machine": _machine(a.workers),
    }
    (OUT / "inn3_survey.json").write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))


# ============================================================ project
def _expected_curtailed(p, B=B_SURROGATES, g=CURTAIL):
    """E[min(B, T_g)], T_g = trial of the g-th exceedance. Exact: sum_n P(T_g > n)."""
    from scipy.stats import binom
    if p <= 0:
        return float(B)
    return float(binom.cdf(g - 1, np.arange(B), p).sum())


def _cluster_bootstrap(df, col, nboot=20000, seed=20260727):
    rng = np.random.default_rng(seed)
    uh = np.unique(df["tic"].to_numpy())
    idx = {h: np.flatnonzero(df["tic"].to_numpy() == h) for h in uh}
    comb, full = df[col].to_numpy(), df["cost_full"].to_numpy()
    cs = np.array([comb[idx[h]].sum() for h in uh])
    fs = np.array([full[idx[h]].sum() for h in uh])
    pick = rng.integers(0, uh.size, size=(nboot, uh.size))
    r = cs[pick].sum(axis=1) / fs[pick].sum(axis=1)
    return float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5)), float((r <= 0.70).mean())


def _host_power(d, seed=20260817, nboot=20000):
    """How many host clusters would decide E2 under each cost configuration?

    The frozen §6 rule decides on a host-clustered 95% CI for the ratio. The CI's
    width is set by BETWEEN-HOST variance, so it shrinks as 1/sqrt(H). This asks,
    for each configuration, the H at which the upper limit first falls below 0.70.

    CAVEAT. Resampling H > 39 hosts draws from the 39 observed ones, so it assumes
    they represent the wider host pool. This is a DESIGN calculation, not a
    measurement, and it cannot re-decide the sealed run (P-2). Its purpose is to
    separate "the estimand is out of reach" from "the sample is too small".
    """
    rng = np.random.default_rng(seed)
    cfgs = {"sealed": "cost_comb", "leverA": "cost_comb_leverA",
            "leverA_plus_B": "cost_comb_leverAB",
            "free_detector_limit": "cost_comb_free_detector"}
    out = {"caveat": ("resamples H hosts from the 39 observed; design calculation, "
                      "not a measurement; does not re-decide the sealed run (P-2)"),
           "note": ("m4_driver draws 80 hosts; the erratum §2.1 parity bug used 40, of "
                    "which the E2 timing subset occupied 39. H=79 is therefore the "
                    "counterfactual for the INTENDED design.")}
    for tag, col in cfgs.items():
        g = d.groupby("tic").agg(c=(col, "sum"), f=("cost_full", "sum"))
        c, f, H = g.c.to_numpy(), g.f.to_numpy(), len(g)
        R = float(c.sum() / f.sum())
        se = float(np.sqrt(H / ((H - 1) * f.sum() ** 2) * np.sum((c - R * f) ** 2)))
        need = (0.70 - R) / 1.959963985
        row = {"ratio": R, "cluster_robust_se_at_H": se, "H_observed": H,
               "se_needed_for_hi_le_0.70": need,
               "hosts_needed": int(np.ceil(H * (se / need) ** 2)) if need > 0 else None,
               "by_H": {}}
        for Hp in (H, 49, 60, 79, 100):
            pick = rng.integers(0, H, size=(nboot, Hp))
            r = c[pick].sum(1) / f[pick].sum(1)
            lo, hi = (float(x) for x in np.percentile(r, [2.5, 97.5]))
            row["by_H"][str(Hp)] = {"ci95": [lo, hi],
                                    "decision": ("PASS" if hi <= 0.70 else
                                                 "FAIL" if lo > 0.70 else "INCONCLUSIVE")}
        out[tag] = row
    return out


def run_project(a):
    s_vec = a.s_vec
    led = pd.read_csv(REPO / "data/manifests/m4/e2_retiming/timing_ledger_full.csv")
    rec = pd.read_csv(REPO / "data/manifests/m4/test_run/recovery.csv")
    key = ["tic", "period_days", "radius_rearth", "b"]
    for k in key:
        led[k] = pd.to_numeric(led[k], errors="coerce")
        rec[k] = pd.to_numeric(rec[k], errors="coerce")
    rec["ge"] = np.round(pd.to_numeric(rec["fap"], errors="coerce") * (B_SURROGATES + 1) - 1)
    d = led.merge(rec.groupby(key, as_index=False).agg(ge=("ge", "median")), on=key, how="left")
    ge = pd.to_numeric(d["ge"], errors="coerce").to_numpy(float)
    matched = np.isfinite(ge)
    ge_use = np.where(matched, ge, 0.0)                  # unmatched: charge full B (conservative)
    cache, E = {}, np.empty(len(d))
    for i, g in enumerate(ge_use):
        gi = int(g)
        if gi not in cache:
            cache[gi] = _expected_curtailed(gi / B_SURROGATES)
        E[i] = cache[gi]
    d["E_surrogates"] = E
    d["cost_detector_leverA"] = d["cost_detector"] / s_vec
    d["cost_detector_leverAB"] = d["cost_detector"] / s_vec * (1.0 + E) / (1.0 + B_SURROGATES)
    d["cost_comb_leverA"] = d["cost_detector_leverA"] + d["cost_period"] + d["cost_tls"]
    d["cost_comb_leverAB"] = d["cost_detector_leverAB"] + d["cost_period"] + d["cost_tls"]
    d["cost_comb_free_detector"] = d["cost_period"] + d["cost_tls"]

    C_full = float(d["cost_full"].sum())
    f_p = float(d["confirmed_cheap"].mean())
    ch = d[d["confirmed_cheap"] == True]                 # noqa: E712
    rho = float(ch["cost_tls"].sum() / ch["cost_full"].sum()) if len(ch) else 0.0

    out = {"task": "INN-3 — counterfactual E2 re-analysis (arithmetic on recorded artifacts)",
           "disclaimer": ("NOT a re-measurement. TEST light curves are not re-read (P-5). "
                          "Inputs: e2_retiming/timing_ledger_full.csv and test_run/recovery.csv, "
                          "both already-recorded. The sealed E2 outcome is unchanged."),
           "s_vec_used": s_vec, "n_tasks": len(d), "n_hosts": int(d.tic.nunique()),
           "n_matched_to_recorded_fap": int(matched.sum()),
           "E_surrogates_mean": float(E.mean()), "E_surrogates_median": float(np.median(E)),
           "f_p": f_p, "rho_cheap_path": rho, "C_full_s": C_full}

    for tag, col, dcol in (("sealed", "cost_comb", "cost_detector"),
                           ("leverA", "cost_comb_leverA", "cost_detector_leverA"),
                           ("leverA_plus_B", "cost_comb_leverAB", "cost_detector_leverAB"),
                           ("free_detector_limit", "cost_comb_free_detector", None)):
        C = float(d[col].sum())
        rho_d = float(d[dcol].sum() / C_full) if dcol else 0.0
        ratio = C / C_full
        lo, hi, ple = _cluster_bootstrap(d, col)
        out[tag] = {"compute_ratio": ratio, "reduction": 1 - ratio, "rho_d": rho_d,
                    "pi_star_eligible_population": rho_d / (f_p * (1 - rho)) if f_p else None,
                    "ratio_ci95_host_cluster": [lo, hi], "p_ratio_le_0.70": ple,
                    "meets_30pct_target": bool((1 - ratio) >= 0.30),
                    "frozen_rule_decision": ("PASS" if hi <= 0.70 else
                                             "FAIL" if lo > 0.70 else "INCONCLUSIVE")}
    out["recorded_sealed_for_check"] = {"compute_ratio": 0.7271396884272067,
                                        "ratio_ci95": [0.635873125911904, 0.8257209089276649],
                                        "p_ratio_le_0.70": 0.2698, "rho_d": 0.11564914281767508}
    out["host_power"] = _host_power(d)
    out["machine"] = _machine(1)
    OUT.mkdir(parents=True, exist_ok=True)
    d.to_csv(OUT / "inn3_e2_counterfactual_tasks.csv", index=False)
    (OUT / "inn3_e2_counterfactual.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


def main():
    ap = argparse.ArgumentParser(description="INN-3 exact accelerated period-FAP validation.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("nulls", "injections", "survey", "project"):
        p = sub.add_parser(name)
        p.add_argument("--workers", type=int, default=6)
        p.add_argument("--limit", type=int, default=None)
        if name == "nulls":
            p.add_argument("--sealed-n", type=int, default=60)
        if name == "injections":
            p.add_argument("--per-cell", type=int, default=7)
        if name == "project":
            p.add_argument("--s-vec", type=float, required=True,
                           help="measured lever-A speedup (from the nulls/injections runs)")
    a = ap.parse_args()
    _pin_threads()
    {"nulls": run_nulls, "injections": run_injections,
     "survey": run_survey, "project": run_project}[a.cmd](a)


if __name__ == "__main__":
    main()
