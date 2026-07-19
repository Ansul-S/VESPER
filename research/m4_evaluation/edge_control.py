"""P=0.5 d grid-edge control experiment (audit remediation, DR-003) — CALIBRATION-only.

Audit finding: 99.6% of Arm B's 563 sealed-TEST "gains" sit at P = 0.5 d, which is
exactly the sealed TLS grid's period_min. The sealed interpretation ("the confirmer
recovers planets whose full-grid SDE fell just below T") did not test the more
parsimonious explanation: TLS recall is degraded when the true period lies ON the
search-grid boundary (edge effects in grid coverage / SDE normalization).

Control design (CALIBRATION null-pool hosts only; TEST untouched; sealed T=10.74):
  A. inject P=0.50 d, run full TLS with sealed period_min=0.50  (edge condition)
  B. same injections,  run full TLS with period_min=0.30        (period interior)
  C. inject P=0.62 d,  run full TLS with sealed period_min=0.50 (interior control,
     still ultra-short-period -> excludes "short periods generally" as the cause)

If recall(B) >> recall(A) and recall(C) >> recall(A), the edge artifact is confirmed
and the sealed "gain region" interpretation must carry that caveat.

Run:  .venv/bin/python research/m4_evaluation/edge_control.py [--n 60] [--rp 8] [--workers 7]
Out:  data/manifests/m4/e2_retiming/edge_control.{csv,json}
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "frozen_rerun"))       # frozen injection physics + seal loader
sys.path.insert(0, str(HERE.parent / "m2_injection"))
sys.path.insert(0, str(HERE))

import injection as INJ        # noqa: E402 (frozen)
import seal_loader as SL       # noqa: E402 (frozen)
import recovery as REC         # noqa: E402

CACHE = Path("data/processed/m1")
OUT = Path("data/manifests/m4/e2_retiming")
_FR = _MAN = _LD = None


def _run_tls(t, flux, period_min, period_max, oversampling):
    from transitleastsquares import transitleastsquares
    model = transitleastsquares(np.asarray(t, float), np.asarray(flux, float))
    res = model.power(period_min=float(period_min), period_max=float(period_max),
                      oversampling_factor=int(oversampling), use_threads=1,
                      show_progress_bar=False)
    return {"sde": float(res.SDE), "period": float(res.period),
            "t0": float(getattr(res, "T0", np.nan)),
            "duration": float(getattr(res, "duration", np.nan))}


def _init(man_idx):
    global _FR, _MAN, _LD
    _FR, _MAN, _LD = SL.load_frozen(), man_idx, INJ.constant_ld()


def _worker(job):
    tic, P_true, b, seed, pmin_label, pmin = (job["tic"], job["P_true"], job["b"],
                                              job["seed"], job["arm"], job["period_min"])
    fr = _FR
    z = np.load(CACHE / f"{tic}.npz")
    t, r0 = np.asarray(z["time"], float), np.asarray(z["resid"], float)
    rng = np.random.default_rng(int(seed))
    built = INJ.build_injection(t, P_true, job["Rp"], b, _MAN.loc[tic], _LD, rng,
                                host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    pmax = max(pmin * 1.5, fr.period_max_frac_baseline * float(t.max() - t.min()))
    res = _run_tls(t, 1.0 + r, pmin, pmax, fr.oversampling)
    rec = REC.recovered(res, truth, fr.T_sde)
    return {"tic": tic, "arm": pmin_label, "P_true": P_true, "Rp": job["Rp"], "b": b,
            "period_min": pmin, "sde": res["sde"], "period_hat": res["period"],
            "recovered": rec["recovered"], "period_ok": rec["period_ok"],
            "sde_ok": rec["sde_ok"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=60, help="injections per condition")
    ap.add_argument("--rp", type=int, default=8)
    ap.add_argument("--workers", type=int, default=7)
    a = ap.parse_args()
    from multiprocessing import Pool

    fr = SL.load_frozen()
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    # cleaned calibration null hosts with cached residuals (M3 pool; TEST untouched)
    pool_tics = pd.read_csv("data/manifests/m3/m3_null_cleaned_catalog.csv")["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    cal = man[(man.split == "calibration") & man.tic.isin(set(pool_tics) & avail)
              & (man.rad > 0) & np.isfinite(man.logg) & np.isfinite(man.Teff)]
    assert (cal.split == "calibration").all()
    man_idx = cal.set_index("tic")
    rng = np.random.default_rng(20260719)
    hosts = rng.choice(cal.tic.to_numpy(), size=a.n, replace=True)
    bs = [INJ.GRID_B[i % 3] for i in range(a.n)]

    jobs = []
    for i, (tic, b) in enumerate(zip(hosts, bs)):
        seed_e = 900000 + i
        # A + B share the SAME injection (paired): edge grid vs extended grid
        jobs.append({"tic": tic, "P_true": 0.5, "Rp": a.rp, "b": b, "seed": seed_e,
                     "arm": "A_edge_pmin0.5", "period_min": 0.5})
        jobs.append({"tic": tic, "P_true": 0.5, "Rp": a.rp, "b": b, "seed": seed_e,
                     "arm": "B_extended_pmin0.3", "period_min": 0.3})
        # C: off-node short-period control on the sealed grid
        jobs.append({"tic": tic, "P_true": 0.62, "Rp": a.rp, "b": b, "seed": 910000 + i,
                     "arm": "C_offnode_P0.62_pmin0.5", "period_min": 0.5})
    print(f"[edge] {len(jobs)} TLS runs ({a.n}/condition, Rp={a.rp}) on "
          f"{len(set(hosts))} cleaned calibration null hosts")

    rows = []
    with Pool(a.workers, initializer=_init, initargs=(man_idx,)) as pool:
        for i, x in enumerate(pool.imap_unordered(_worker, jobs, chunksize=1), 1):
            if x is not None:
                rows.append(x)
            if i % 20 == 0:
                print(f"[edge] {i}/{len(jobs)} ...", flush=True)
    df = pd.DataFrame(rows)
    OUT.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT / "edge_control.csv", index=False)

    summ = {}
    for arm, grp in df.groupby("arm"):
        summ[arm] = {"n": int(len(grp)), "recall": float(grp.recovered.mean()),
                     "period_ok": float(grp.period_ok.mean()),
                     "sde_ok": float(grp.sde_ok.mean()),
                     "median_sde": float(grp.sde.median())}
    rA = summ.get("A_edge_pmin0.5", {}).get("recall", np.nan)
    rB = summ.get("B_extended_pmin0.3", {}).get("recall", np.nan)
    rC = summ.get("C_offnode_P0.62_pmin0.5", {}).get("recall", np.nan)
    verdict = ("EDGE ARTIFACT CONFIRMED: moving the injected period off the grid edge "
               "(B and C) recovers what the edge condition (A) loses."
               if (rB - rA > 0.15 and rC - rA > 0.15) else
               "Edge artifact NOT confirmed at this sample size — the sealed "
               "interpretation stands unless a larger control says otherwise.")
    out = {"design": "A: P=0.5 on edge grid | B: same injections, pmin=0.3 | C: P=0.62 on sealed grid",
           "n_per_condition": a.n, "Rp": a.rp, "sealed_T": fr.T_sde,
           "recall_by_condition": summ, "verdict": verdict}
    (OUT / "edge_control.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
