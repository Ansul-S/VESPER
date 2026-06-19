"""E-LUT equivalence validation (v3, 2nd pre-registered candidate) — CALIBRATION-only.

Implements the LEVER1B plan's second candidate: a precomputed red-noise null distribution
('O(1) lookup'), keyed on (event-count k, baseline). The null R-distribution of k events is
primarily a function of k and the period-search range (p_max = 0.5*baseline); we tabulate the
exceedance of obs_R under UNIFORM-random epochs per (k, baseline-bin), then look it up per star.

Tested against the SAME stored B=1000 bootstrap reference (equiv_nulls.csv / equiv_injections.csv
fap_ref) with the IDENTICAL pre-stated criteria (plan 4) — NOT relaxed. If E-LUT also fails,
the pre-committed confirmer-only fallback stands (now with verdicts on record for BOTH candidates).

NO TEST; reuses CALIBRATION outputs only; no seal.
Run: .venv/bin/python research/m4_evaluation/elut_equivalence.py [--workers N] [--nsim N]
"""
from __future__ import annotations
import sys, argparse, os, json, time
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
from period_recovery import best_period           # noqa: E402

P_MIN = 0.5
PMAX_FRAC = 0.5
OVERSAMPLE = 3
ALPHA = 0.01
TAU_ABS = 0.005
KMAX = 45
BASE_BINS = [20, 28, 36, 46, 60]     # baseline-day bin edges (covers S1-S3 single/double/triple)
NSIM_DEFAULT = 4000
SEED = 20260619


def _null_R_samples(k, baseline, nsim, rng):
    """Null R for k UNIFORM-random epochs over [0, baseline], best-period resultant length."""
    p_max = PMAX_FRAC * baseline
    out = np.empty(nsim, float)
    for i in range(nsim):
        ep = np.sort(rng.uniform(0.0, baseline, size=k))
        out[i] = best_period(ep, P_MIN, p_max, OVERSAMPLE)[2]
    out.sort()
    return out


def _build_cell(args):
    k, bbin_idx, base_mid, nsim, seed = args
    rng = np.random.default_rng(seed)
    return (k, bbin_idx, _null_R_samples(k, base_mid, nsim, rng))


def _bbin(baseline):
    for i in range(len(BASE_BINS) - 1):
        if BASE_BINS[i] <= baseline < BASE_BINS[i + 1]:
            return i
    return 0 if baseline < BASE_BINS[0] else len(BASE_BINS) - 2


def lut_fap(lut, k, bbin_idx, obs_R):
    k = int(min(max(k, 2), KMAX))
    arr = lut.get((k, bbin_idx))
    if arr is None:                       # nearest k in same baseline bin
        ks = [kk for (kk, bb) in lut if bb == bbin_idx]
        if not ks:
            return np.nan
        k = min(ks, key=lambda x: abs(x - k)); arr = lut[(k, bbin_idx)]
    return (int((arr >= obs_R).sum()) + 1) / (arr.size + 1)


def run(workers=None, nsim=NSIM_DEFAULT):
    from multiprocessing import Pool
    eq = Path("data/manifests/m4/equivalence")
    nd = pd.read_csv(eq / "equiv_nulls.csv"); idf = pd.read_csv(eq / "equiv_injections.csv")
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    base = man.set_index("tic")["baseline_days"].to_dict()

    def tic_of(key):
        return str(key).split("_")[0]

    nr = nd[nd.routed == True].copy(); ir = idf[idf.routed == True].copy()
    for df in (nr, ir):
        df["tic"] = df["key"].map(tic_of)
        df["baseline"] = df["tic"].map(lambda t: float(base.get(t, 27.0)))
        df["bbin"] = df["baseline"].map(_bbin)
    base_mids = [(BASE_BINS[i] + BASE_BINS[i+1]) / 2 for i in range(len(BASE_BINS) - 1)]

    # which (k, bbin) cells are actually needed
    need = set()
    for df in (nr, ir):
        for _, row in df.iterrows():
            need.add((int(min(max(row["n_events"], 2), KMAX)), int(row["bbin"])))
    cells = [(k, b, base_mids[b], nsim, SEED ^ (k * 131 + b)) for (k, b) in sorted(need)]
    print(f"[elut] building {len(cells)} (k,baseline) cells x nsim={nsim} (uniform-epoch null)", flush=True)

    nw = workers or max(1, (os.cpu_count() or 2) - 2)
    t0 = time.perf_counter(); lut = {}
    with Pool(nw) as pool:
        for i, (k, b, arr) in enumerate(pool.imap_unordered(_build_cell, cells, chunksize=1), 1):
            lut[(k, b)] = arr
            if i % 25 == 0:
                print(f"[elut] cells {i}/{len(cells)} ({(time.perf_counter()-t0)/60:.1f} min)", flush=True)

    nr["fap_lut"] = nr.apply(lambda r: lut_fap(lut, int(r.n_events), int(r.bbin), r.obs_R), axis=1)
    ir["fap_lut"] = ir.apply(lambda r: lut_fap(lut, int(r.n_events), int(r.bbin), r.obs_R), axis=1)
    out = eq
    nr.to_csv(out / "elut_nulls.csv", index=False); ir.to_csv(out / "elut_injections.csv", index=False)

    # ===== same pre-stated criteria vs fap_ref =====
    near = nr[(nr.fap_ref <= 0.05) | (nr.fap_lut <= 0.05)]
    d = (near.fap_lut - near.fap_ref).abs()
    p95_d = float(d.quantile(0.95)) if len(d) else 0.0
    med_d = float(d.median()) if len(d) else 0.0
    corr = float(np.corrcoef(nr.fap_ref, nr.fap_lut)[0, 1]) if len(nr) > 2 else float("nan")
    crit_i = bool(p95_d <= TAU_ABS)
    ref_pass = nr.fap_ref <= ALPHA; lut_pass = nr.fap_lut <= ALPHA
    discord = int((ref_pass != lut_pass).sum()); admit_extra = int(((~ref_pass) & lut_pass).sum())
    crit_ii = bool(discord <= max(1, int(0.01*len(nr))) and admit_extra == 0)
    keep = ir[(ir.fap_ref <= ALPHA) & (ir.period_match == True)]
    clipped = int((keep.fap_lut > ALPHA).sum())
    crit_iii = bool(clipped == 0)
    verdict = "PASS" if (crit_i and crit_ii and crit_iii) else "FAIL"
    summary = {
        "candidate": "E-LUT (uniform-epoch null, keyed on k + baseline)",
        "n_null_routed": int(len(nr)), "n_inj_routed": int(len(ir)),
        "crit_i_fap_agreement": {"tau_abs": TAU_ABS, "median_abs_dFAP": med_d, "p95_abs_dFAP": p95_d,
                                  "corr_ref_lut": corr, "PASS": crit_i},
        "crit_ii_gate_membership": {"discordant": discord, "limit": max(1, int(0.01*len(nr))),
                                    "admit_extra_FP": admit_extra, "PASS": crit_ii},
        "crit_iii_recall_safety": {"n_ref_pass_periodmatched": int(len(keep)), "clipped_by_lut": clipped,
                                   "PASS": crit_iii},
        "VERDICT": verdict,
    }
    (out / "elut_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n================ E-LUT EQUIVALENCE VALIDATION ================")
    print(json.dumps(summary, indent=2))
    print(f"\nartifacts -> {out}/elut_*  | elapsed {(time.perf_counter()-t0)/60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--nsim", type=int, default=NSIM_DEFAULT)
    a = ap.parse_args()
    run(workers=a.workers, nsim=a.nsim)
