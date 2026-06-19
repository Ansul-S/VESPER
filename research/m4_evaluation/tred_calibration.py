"""T_red calibration (v3) — CALIBRATION-ONLY.

Implements TRED_CALIBRATION_PLAN.md verbatim. Calibrates the Arm-B fast-path confirmer
threshold T_red to FAR <= 1%/star (the common-FAR keystone), on the cleaned null pool,
using the genuine transit-LR confirmer (confirmer.py; box depth-SNR rejected).

End-to-end Arm-B false confirmation requires BOTH gates: FAP_ref <= alpha (period-FAP gate,
sealed B=1000 reference from m3_per_star.csv) AND confirmer (Lambda >= T_red AND shape_pass).
T_red is set SOLELY from the FAR target (P-3): smallest threshold s.t.
  P_null[ FAP<=alpha AND Lambda>=T_red AND shape_pass ] <= alpha (= 1%).
NOT optimized for E1/E2/recall/fallback. Recall preview (sec 5) is REPORTED, non-setting.

NO TEST; 0 TEST TICs asserted; no seal.
Run: .venv/bin/python research/m4_evaluation/tred_calibration.py [--workers N] [--nstars N] [--inj-hosts N]
"""
from __future__ import annotations
import sys, glob, time, argparse, os, json
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
import seal_loader as SL                          # noqa: E402
import injection as INJ                           # noqa: E402
import confirmer as CF                            # noqa: E402
from detector import detect_events                # noqa: E402
from period_recovery import best_period           # noqa: E402

ALPHA = 0.01                                       # sealed alpha_FAP
FAR_TARGET = 0.01                                  # A.2/A.11 common FAR (<=1%/star)
STELLAR = {"u1": 0.4, "u2": 0.25}                  # constant LD (consistent with injection)
INJ_GRID = [(0.5,2),(1.0,2),(2.0,2),(4.0,2),(0.5,4),(1.0,4),(2.0,4),(4.0,4),(8.0,4),(2.0,8),(4.0,8),(2.0,1)]


def _ephemeris(t, r, fr):
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    if ev.shape[0] < fr.n_min:
        return None
    k = int(np.argmax(ev[:, 1])); t0, dur = float(ev[k, 0]), float(ev[k, 2])
    pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
    P_hat = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)[0]
    if not np.isfinite(P_hat):
        return None
    return float(P_hat), t0, dur


def _null_worker(args):
    tic, fap_ref = args
    fr = SL.load_frozen()
    z = np.load(f"data/processed/m1/{tic}.npz")
    t = np.asarray(z["time"], float); r = np.asarray(z["resid"], float)
    if r.size < 1000:
        return None
    eph = _ephemeris(t, r, fr)
    if eph is None:
        return {"tic": tic, "fap_ref": fap_ref, "routed": False, "Lambda": 0.0,
                "shape_pass": False, "n_transits": 0}
    c = CF.confirm(t, r, eph, STELLAR, T_red=np.inf)   # T_red=inf -> just compute Lambda/shape
    return {"tic": tic, "fap_ref": fap_ref, "routed": True, "Lambda": c["Lambda"],
            "shape_pass": c["shape_pass"], "n_transits": c["n_transits"],
            "fap_gate_pass": bool(fap_ref <= ALPHA)}


def _inj_worker(args):
    tic, P, Rp, rowd = args
    fr = SL.load_frozen(); ld = INJ.constant_ld()
    z = np.load(f"data/processed/m1/{tic}.npz")
    t = np.asarray(z["time"], float); r0 = np.asarray(z["resid"], float)
    if r0.size < 1000:
        return None
    row = pd.Series(rowd)
    built = INJ.build_injection(t, P, Rp, 0.0, row, ld, np.random.default_rng(int(tic) & 0x7FFFFFFF),
                                host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    eph = _ephemeris(t, r, fr)
    if eph is None:
        return {"tic": tic, "P": P, "Rp": Rp, "routed": False, "Lambda": 0.0,
                "shape_pass": False, "period_match": False}
    P_hat = eph[0]
    pm = abs(P_hat - P)/P < 0.01 or any(abs(P_hat - P/m)/(P/m) < 0.01 or abs(P_hat - m*P)/(m*P) < 0.01 for m in (2, 3))
    c = CF.confirm(t, r, eph, STELLAR, T_red=np.inf)
    return {"tic": tic, "P": P, "Rp": Rp, "routed": True, "Lambda": c["Lambda"],
            "shape_pass": c["shape_pass"], "period_match": bool(pm), "n_transits": c["n_transits"]}


def _auc(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.size == 0 or b.size == 0:
        return float("nan")
    # rank-based AUC
    allv = np.concatenate([a, b]); order = allv.argsort(); ranks = np.empty_like(order, float)
    ranks[order] = np.arange(1, allv.size + 1)
    ra = ranks[:a.size].sum()
    return float((ra - a.size*(a.size+1)/2) / (a.size*b.size))


def run(workers=None, nstars=None, inj_hosts=12):
    from multiprocessing import Pool
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    per = pd.read_csv("data/manifests/m3/m3_per_star.csv"); per["tic"] = per["tic"].astype(str)
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    avail = {Path(p).stem for p in glob.glob("data/processed/m1/*.npz")}
    cleaned = sorted((set(per["tic"]) - exc) & avail)
    cal_tics = set(man[man.split == "calibration"]["tic"])
    assert set(cleaned) <= cal_tics, "TEST LEAK"
    if nstars:
        cleaned = cleaned[:nstars]
    fap_map = per.set_index("tic")["period_fap"].to_dict()
    print(f"[tred] cleaned null pool: {len(cleaned)} stars (0 TEST TICs)", flush=True)

    nw = workers or max(1, (os.cpu_count() or 2) - 2)
    t0 = time.perf_counter()
    # ---- NULLS ----
    nargs = [(tic, float(fap_map.get(tic, np.nan))) for tic in cleaned]
    nrows = []
    with Pool(nw) as pool:
        for i, res in enumerate(pool.imap_unordered(_null_worker, nargs, chunksize=4), 1):
            if res is not None:
                nrows.append(res)
            if i % 100 == 0:
                print(f"[tred] nulls {i}/{len(nargs)} ({(time.perf_counter()-t0)/60:.1f} min)", flush=True)
    nd = pd.DataFrame(nrows)

    # ---- INJECTIONS (recall preview) ----
    hosts = man[(man.split == "calibration") & (man.tic.isin(cleaned)) & (man.rad > 0)
                & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    cols = ["tic", "rad", "logg", "Teff", "Tmag"]
    iargs = []
    for (P, Rp) in INJ_GRID:
        hh = hosts.sample(min(inj_hosts, len(hosts)), random_state=(hash((P, Rp)) & 0xFFFF))
        for _, row in hh.iterrows():
            iargs.append((row["tic"], P, Rp, {c: row[c] for c in cols if c in row}))
    irows = []
    with Pool(nw) as pool:
        for res in pool.imap_unordered(_inj_worker, iargs, chunksize=4):
            if res is not None:
                irows.append(res)
    idf = pd.DataFrame(irows)

    out = Path("data/manifests/m4/tred"); out.mkdir(parents=True, exist_ok=True)
    nd.to_csv(out / "tred_nulls.csv", index=False)
    idf.to_csv(out / "tred_injections.csv", index=False)

    # ===================== SET T_red BY FAR (P-3) =====================
    N = len(nd)
    fap_pass = nd[nd.fap_ref <= ALPHA].copy()           # candidates reaching the confirmer
    # false-confirmation candidate Lambda among FAP-gate passers that also pass shape vetting
    fc = fap_pass[fap_pass.shape_pass == True]["Lambda"].values
    fc = np.sort(fc)[::-1]                               # descending
    allowed = int(np.floor(FAR_TARGET * N))             # max false confirmations at FAR<=1%
    if fc.size <= allowed:
        T_red = 0.0                                     # FAP gate alone already <= FAR target -> T_red non-binding
        binding = False
    else:
        # smallest T_red admitting at most `allowed` confirmations: just above the (allowed+1)-th largest Lambda
        T_red = float(fc[allowed])                      # threshold drops the top `allowed`? -> set just above fc[allowed]
        T_red = float(np.nextafter(fc[allowed], np.inf))
        binding = True
    # achieved FAR at T_red
    conf_null = fap_pass[(fap_pass.Lambda >= T_red) & (fap_pass.shape_pass == True)]
    far_end2end = float(len(conf_null) / N)
    far_marginal = float((nd.Lambda >= T_red).mean())   # ignoring FAP gate (diagnostic)
    far_fapgate_cond = float((fap_pass.Lambda >= T_red).mean()) if len(fap_pass) else float("nan")

    # ---- recall preview (REPORTED; non-setting) ----
    ir = idf[idf.routed == True].copy()
    if len(ir):
        confd = ir[(ir.Lambda >= T_red) & (ir.shape_pass == True) & (ir.period_match == True)]
        recall_fast = float(len(confd) / len(ir))
        recall_strong = float((ir[ir.Rp >= 4].eval("Lambda >= @T_red and shape_pass and period_match")).mean())
        fallback_frac = float(1.0 - len(confd)/len(ir))
        auc = _auc(ir.Lambda.values, nd[nd.routed == True].Lambda.values)
    else:
        recall_fast = recall_strong = fallback_frac = auc = float("nan")

    summary = {
        "n_null": int(N), "n_null_routed": int(nd.routed.sum()),
        "n_fap_gate_pass": int(len(fap_pass)), "fap_gate_pass_rate": float(len(fap_pass)/N),
        "FAR_target": FAR_TARGET, "allowed_false_confirmations": allowed,
        "T_red": T_red, "T_red_binding": binding,
        "achieved_FAR_end2end": far_end2end,
        "achieved_FAR_fapgate_conditional": far_fapgate_cond,
        "achieved_FAR_marginal_diagnostic": far_marginal,
        "recall_preview": {"n_inj_routed": int(len(ir)), "fast_path_recall": recall_fast,
                           "fast_path_recall_strong_Rp>=4": recall_strong,
                           "fallback_fraction": fallback_frac,
                           "AUC_planet_vs_null_Lambda": auc,
                           "note": "REPORTED only; T_red set by FAR, not recall (P-3)"},
        "degeneracy_note": ("FAP gate already controls FAR<=target -> T_red non-binding; FP control shared, "
                            "confirmer adds recall protection + shape/EB vetting") if not binding else
                           "T_red binding (confirmer tightens FAR beyond the FAP gate)",
    }
    (out / "tred_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n================ T_red CALIBRATION ================")
    print(json.dumps(summary, indent=2))
    print(f"\nartifacts -> {out}/  | elapsed {(time.perf_counter()-t0)/60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--nstars", type=int, default=None)
    ap.add_argument("--inj-hosts", type=int, default=12)
    a = ap.parse_args()
    run(workers=a.workers, nstars=a.nstars, inj_hosts=a.inj_hosts)
