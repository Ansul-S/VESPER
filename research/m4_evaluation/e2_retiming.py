"""E2 re-timing campaign per the FROZEN PHASE1_M4_PLAN §6 rule (audit remediation, DR-003).

The sealed TEST run (2026-06-24) decided E2 on a 12-star subset timed once per star
(driver defaults), in deviation from the owner-signed frozen timing rule:
  "stratified sample of >=10 LCs per occupied (P, Rp) cell, capped at 300, seed
   20260616, >=5 warm-cache repeats, single-thread CPU-core-seconds".
This script executes that frozen rule on the SAME sealed injection set (tasks
reconstructed deterministically by reconstruct_m4_tasks.py — same hosts, same seeds,
same epochs). It reads NO new TEST information: every host/injection was already
read in the single sealed evaluation; only execution cost is re-measured (DR-003).

Measurement: time.process_time() per call (= single-thread CPU-core-seconds, A.7;
robust to worker parallelism with OMP/BLAS pinned to 1 thread), median over
--repeats warm-cache repeats; wall-clock recorded alongside for reference.

SEALED CONFIGURATION is reproduced exactly: FROZEN module snapshot (frozen_rerun/),
tau_GP = 0.005 d flat and confirmer LD u2 = 0.25 (the sealed run's behavior — the
audit's per-star-tau / LD fixes apply to future runs, not to re-measuring this one).

Run:  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
      .venv/bin/python research/m4_evaluation/e2_retiming.py --workers 6 --repeats 5
Out:  data/manifests/m4/e2_retiming/{timing_ledger_full.csv, e2_retiming_summary.json}
"""
from __future__ import annotations

import argparse, json, sys, time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "frozen_rerun"))          # sealed code path FIRST
sys.path.insert(0, str(HERE.parent / "m2_injection"))
sys.path.insert(0, str(HERE))                            # live endpoints/arms (arm_a unchanged)

import injection as INJ                                   # noqa: E402 (frozen)
import seal_loader as SL                                  # noqa: E402 (frozen)
import confirmer as CF                                    # noqa: E402 (frozen)
from detector import detect_events                        # noqa: E402 (frozen)
from period_recovery import best_period, period_fap       # noqa: E402 (frozen)
import endpoints as EP                                    # noqa: E402 (live; CI-based decision)
import arms as ARMS                                       # noqa: E402 (live; arm_a_full identical to sealed)

CACHE = Path("data/processed/m1")
OUT = Path("data/manifests/m4/e2_retiming")
STELLAR_SEALED = {"u1": 0.4, "u2": 0.25}   # sealed run's confirmer LD (kept for fidelity)
TAU_SEALED = 0.005                          # sealed run's flat tau_GP (kept for fidelity)
_FR = _MAN = _LD = None


def _init(man_idx):
    global _FR, _MAN, _LD
    _FR, _MAN, _LD = SL.load_frozen(), man_idx, INJ.constant_ld()


def _route_seed_sealed(t, r, fr, rng):
    """Sealed _route_and_seed logic (m4_driver at tag phase1-prereg-v3), CPU-timed."""
    c = {}
    t0 = time.process_time()
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    c["detector"] = time.process_time() - t0
    n = ev.shape[0]
    out = {"n_events": int(n), "routed": n >= fr.n_min, "p_hat": np.nan, "t0_hat": np.nan,
           "t14": float(np.median(fr.duration_grid)), "fap": np.nan, "cost": c}
    if n >= fr.n_min:
        k = int(np.argmax(ev[:, 1]))
        out["t0_hat"], out["t14"] = float(ev[k, 0]), float(ev[k, 2])
        pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
        t0 = time.process_time()
        P_hat, _, obs_R = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)
        out["p_hat"] = float(P_hat) if np.isfinite(P_hat) else np.nan
        if np.isfinite(P_hat):
            fap, _ = period_fap(t, r, obs_R, TAU_SEALED, out["t14"], fr.duration_grid,
                                fr.period_min_days, pmax, fr.z_star, fr.block_len_multiple,
                                fr.B, rng)
            out["fap"] = float(fap)
        c["period_fap"] = time.process_time() - t0
    else:
        c["period_fap"] = 0.0
    return out


def _worker(row):
    fr = _FR
    tic = str(row["tic"])
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    rng = np.random.default_rng(int(row["seed"]))
    built = INJ.build_injection(t, row["period_days"], row["radius_rearth"], row["b"],
                                _MAN.loc[tic], _LD, rng, host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, _truth = built
    if not getattr(_worker, "_warm", False):        # per-process JIT warm-up (untimed)
        ARMS.arm_a_full(t, r, fr)
        _worker._warm = True
    R = int(row["repeats"])
    cf_cpu, cf_wall, rt_cpu = [], [], []
    s = None
    for _ in range(R):
        w0, c0 = time.perf_counter(), time.process_time()
        ARMS.arm_a_full(t, r, fr)
        cf_cpu.append(time.process_time() - c0); cf_wall.append(time.perf_counter() - w0)
        c0 = time.process_time()
        s = _route_seed_sealed(t, r, fr, np.random.default_rng(int(row["seed"]) ^ 99))
        rt_cpu.append(time.process_time() - c0)
    c_full, c_route = float(np.median(cf_cpu)), float(np.median(rt_cpu))
    c_tls, confirmed = 0.0, False
    if s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]):
        conf = []
        for _ in range(R):
            c0 = time.process_time()
            c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), STELLAR_SEALED, 0.0)
            conf.append(time.process_time() - c0)
        c_tls = float(np.median(conf)); confirmed = bool(c["confirmed"])
    if not confirmed:
        c_tls += c_full
    return {"task": int(row["task"]), "tic": tic, "period_days": row["period_days"],
            "radius_rearth": int(row["radius_rearth"]), "b": row["b"],
            "cost_full": c_full, "cost_full_wall": float(np.median(cf_wall)),
            "cost_full_cpu_spread": float(np.std(cf_cpu)),
            "cost_detector": c_route, "cost_period": 0.0, "cost_tls": c_tls,
            "cost_comb": c_route + c_tls, "fast_path_eligible": True,
            "routed_in_retime": bool(s["routed"]), "confirmed_cheap": confirmed,
            "n_repeats": R}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--per-cell", type=int, default=10)
    ap.add_argument("--cap", type=int, default=300)
    a = ap.parse_args()
    from multiprocessing import Pool

    recon = pd.read_csv(OUT / "task_reconstruction.csv")
    recon["tic"] = recon["tic"].astype(str)
    val = json.loads((OUT / "reconstruction_validation.json").read_text())
    assert val["host_sets_match"] and val["cells_with_host_multiset_mismatch"] == 0, \
        "reconstruction not validated — refuse to time an unverified injection set"
    elig = recon[recon.built & recon.routed].reset_index(drop=True)
    sub_idx = EP.timing_subset(elig, per_cell_min=a.per_cell, cap=a.cap, seed=20260616)
    sub = elig.loc[sub_idx].copy()
    sub["repeats"] = a.repeats
    print(f"[E2-retime] frozen rule subset: {len(sub)} of {len(elig)} eligible "
          f"({sub.tic.nunique()} hosts, {a.repeats} repeats) — sealed config, CPU-time")

    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    man_idx = man[man.split == "test"].set_index("tic")

    led = []
    ledger_path = OUT / "timing_ledger_full.csv"
    with Pool(a.workers, initializer=_init, initargs=(man_idx,)) as pool:
        for i, x in enumerate(pool.imap_unordered(_worker, sub.to_dict("records"), chunksize=1), 1):
            if x is not None:
                led.append(x)
                pd.DataFrame([x]).to_csv(ledger_path, mode="a", header=not ledger_path.exists(),
                                         index=False)
            if i % 15 == 0:
                done = pd.DataFrame(led)
                print(f"[E2-retime] {i}/{len(sub)} | interim ratio "
                      f"{done.cost_comb.sum()/done.cost_full.sum():.3f}", flush=True)
    L = pd.DataFrame(led)
    e2 = EP.e2_compute(L, recall_pass=True)   # E1 pass is sealed + audit-robust
    summary = {"protocol": "PHASE1_M4_PLAN §6 frozen timing rule (audit remediation DR-003)",
               "sealed_run_deviation": "sealed run timed 12 stars x1 repeat (wall-clock)",
               "n_timed": int(len(L)), "n_hosts": int(L.tic.nunique()),
               "repeats": a.repeats, "metric": "single-thread CPU-core-seconds (process_time)",
               "sealed_config_fidelity": {"tau_gp": TAU_SEALED, "confirmer_u2": 0.25,
                                          "modules": "frozen_rerun snapshot"},
               "E2": e2}
    (OUT / "e2_retiming_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(json.dumps({k: v for k, v in e2.items() if k != "per_stage_means_s"}, indent=2))
    print(f"[E2-retime] DECISION: {e2['decision']}  (ratio {e2['compute_ratio']:.3f}, "
          f"CI95 [{e2['ratio_ci95'][0]:.3f}, {e2['ratio_ci95'][1]:.3f}])")


if __name__ == "__main__":
    main()
