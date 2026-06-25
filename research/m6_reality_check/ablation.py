"""M6 W3 — gate ablation on CALIBRATION (-> T8): what the calibrated photometric gate buys.

Compares the sealed Arm-B confirmer against two ablations, on CALIBRATION injections
(recall) and the cleaned null pool (false positives). Test-blind; sealed thresholds; the
ablations REMOVE/replace a component to measure its contribution — they do not re-tune.

  SEALED      : routed & FAP<=alpha & confirmer(Lambda>=T_red & sign & shape[odd/even,no-secondary])
  no_shape    : drop the sign + shape vetting (confirm on Lambda>=T_red only)  -> what the shape gate rejects
  no_fap_gate : drop the bootstrap period-FAP entry gate (confirm any routed seed) -> what the FAP gate rejects

Run: .venv/bin/python research/m6_reality_check/ablation.py --per-cell 30 --n-null 300 --workers 8
"""
from __future__ import annotations
import sys, argparse, json
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m4_evaluation")); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
import seal_loader as SL, confirmer as CF, injection as INJ, recovery as REC, m4_driver as M4  # noqa: E402
CACHE = Path("data/processed/m1"); OUT = Path("data/manifests/m6"); OUT.mkdir(parents=True, exist_ok=True)
_FR = _MAN = _LD = _TRED = None


def _init(man, t_red):
    global _FR, _MAN, _LD, _TRED
    _FR, _MAN, _LD, _TRED = SL.load_frozen(), man, INJ.constant_ld(), t_red


def _decide(t, r, s, fr, t_red):
    """Return (sealed, no_shape, no_fap_gate) confirm flags for one routed seed."""
    routed = s["routed"] and np.isfinite(s["p_hat"])
    if not routed:
        return False, False, False
    fap_ok = np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap
    c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), M4.STELLAR, t_red)
    lam_ok = bool(c["Lambda"] >= t_red)
    sealed = bool(fap_ok and c["confirmed"])
    no_shape = bool(fap_ok and lam_ok)                 # drop sign+shape vetting
    no_fap_gate = bool(c["confirmed"])                 # drop FAP entry gate
    return sealed, no_shape, no_fap_gate


def _inj_worker(task):
    tic, P, Rp, b, seed = task
    fr, t_red = _FR, _TRED
    t, r0 = M4._resid(tic)
    built = INJ.build_injection(t, P, Rp, b, _MAN.loc[tic], _LD, np.random.default_rng(seed), "cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    s = M4._route_and_seed(t, r, fr, 0.005, np.random.default_rng(seed ^ 7))
    se, ns, nf = _decide(t, r, s, fr, t_red)
    p_ok, _ = REC._period_match(s["p_hat"], truth["P_true"]) if np.isfinite(s["p_hat"]) else (False, False)
    e_ok = REC._epoch_match(s["t0_hat"], s["p_hat"], truth["t0_true"], truth["t14_true"]) if np.isfinite(s["p_hat"]) else False
    seedok = bool(p_ok and e_ok)
    return {"kind": "inj", "sealed": se and seedok, "no_shape": ns and seedok, "no_fap_gate": nf and seedok}


def _null_worker(task):
    tic, seed = task
    fr, t_red = _FR, _TRED
    t, r = M4._resid(tic)
    s = M4._route_and_seed(t, r, fr, 0.005, np.random.default_rng(seed))
    se, ns, nf = _decide(t, r, s, fr, t_red)
    return {"kind": "null", "sealed": se, "no_shape": ns, "no_fap_gate": nf}


def main():
    from multiprocessing import Pool
    ap = argparse.ArgumentParser(); ap.add_argument("--per-cell", type=int, default=30)
    ap.add_argument("--n-null", type=int, default=300); ap.add_argument("--workers", type=int, default=8); a = ap.parse_args()
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    pool_df = man[(man.split == "calibration") & (man.rad > 0) & np.isfinite(man.logg) & np.isfinite(man.Teff)]
    pool_df = pool_df[pool_df.tic.isin((draw - exc) & avail)]
    assert (pool_df.split == "calibration").all(), "TEST LEAK"
    hosts = pool_df.sample(min(80, len(pool_df)), random_state=22).tic.tolist()
    nulls = pool_df.sample(min(a.n_null, len(pool_df)), random_state=33).tic.tolist()
    man_idx = pool_df.set_index("tic")
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    itasks, sc = [], 0
    for (P, Rp) in cells:
        for j in range(a.per_cell):
            itasks.append((hosts[(j + sc) % len(hosts)], P, Rp, INJ.GRID_B[j % len(INJ.GRID_B)], 80000 + sc)); sc += 1
    ntasks = [(tic, 90000 + k) for k, tic in enumerate(nulls)]
    fr = SL.load_frozen(); t_red, _ = M4.verify_v3_manifest()
    print(f"[ablation] {len(itasks)} injections + {len(ntasks)} nulls; T_red={t_red}; workers {a.workers}")
    irows, nrows = [], []
    with Pool(a.workers, initializer=_init, initargs=(man_idx, t_red)) as pool:
        for i, x in enumerate(pool.imap_unordered(_inj_worker, itasks, chunksize=4), 1):
            if x: irows.append(x)
            if i % 200 == 0: print(f"[ablation] inj {i}/{len(itasks)} ...")
        for i, x in enumerate(pool.imap_unordered(_null_worker, ntasks, chunksize=4), 1):
            if x: nrows.append(x)
    di, dn = pd.DataFrame(irows), pd.DataFrame(nrows)
    variants = ["sealed", "no_shape", "no_fap_gate"]
    t8 = pd.DataFrame([{"variant": v, "recall": float(di[v].mean()) if len(di) else None,
                        "null_FP_rate": float(dn[v].mean()) if len(dn) else None} for v in variants])
    t8.to_csv(Path("research/m4_evaluation/tables") / "T8.csv", index=False)
    pd.concat([di, dn]).to_csv(OUT / "ablation.csv", index=False)
    print("\n[T8]\n" + t8.to_string(index=False))
    print(f"[ablation] -> {OUT}/ablation.csv + tables/T8.csv")


if __name__ == "__main__":
    main()
