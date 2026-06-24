"""Lever-1b equivalence validation (v3) — CALIBRATION-ONLY.

Implements LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md verbatim. Decides whether a cheap
per-star EVT (GPD tail-fit) period-FAP estimator is NUMERICALLY EQUIVALENT to the
sealed B=1000 circular-block-bootstrap reference (VAL A.8 / MATH 9.1), on CALIBRATION.

Per star (parallel): detect -> obs_R -> ONE B=1000 surrogate draw {R^(b)} (sealed scheme):
  reference FAP  = (#{R^(b) >= obs_R} + 1)/(B+1)         [matches stored m3 period_fap]
  EVT FAP        = GPD tail-fit to the FIRST B'=100 surrogates, extrapolated to obs_R
Apples-to-apples (same draw); isolates EVT extrapolation from RNG noise.

Pre-stated tolerances (FIXED before results; plan 4 — NOT editable):
  (i)   p95 |FAP_evt - FAP_ref| <= TAU_ABS = 0.005 near the gate; report median/95th/corr.
  (ii)  gate-membership: discordant (FAP<=alpha) <= 1% of nulls; ZERO that ADMIT a null the
        reference rejects (no FP inflation).
  (iii) injections: among reference-PASS (FAP_ref<=alpha) AND period-matched, EVT clips ZERO. (NN#1)
Fallback (plan 6): any fail -> confirmer-only v3 (reference bootstrap stands). No criterion
relaxed after observation (P-1/P-3).  NO TEST; 0 TEST TICs asserted; no seal.

Run: .venv/bin/python research/m4_evaluation/equivalence_validation.py [--workers N] [--nstars N] [--inj-hosts N]
"""
from __future__ import annotations
import sys, glob, time, argparse, os, json, shutil
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
from detector import detect_events                # noqa: E402
from period_recovery import best_period, _circular_block_bootstrap  # noqa: E402
import injection as INJ                           # noqa: E402

# ---- SEALED config (m3_config.yaml; unchanged) ----
DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
T14 = float(np.median(DGRID))           # 0.2
BLOCK_MULT = 3
B_REF = 1000                            # sealed B
B_EVT = 100                             # EVT subsample (first B' of the SAME draw)
OVERSAMPLE = 3
P_MIN = 0.5
PMAX_FRAC = 0.5
Z_BOOT = 2.0
ALPHA = 0.01                            # sealed alpha_FAP
TAU_ABS = 0.005                         # pre-stated tolerance (plan 4i)
SEED = 20260616
INJ_GRID = [(0.5,2),(1.0,2),(2.0,2),(4.0,2),(0.5,4),(1.0,4),(2.0,4),(4.0,4),(8.0,4),(2.0,8),(4.0,8),(2.0,1),(4.0,2)]
TMP = Path("data/manifests/m4/equivalence/_tmp_inj")


def _align(t, r):
    ev = detect_events(t, r, DGRID, stride_frac=0.5, z_for_extraction=Z_BOOT)
    if ev.shape[0] < 2:
        return None, int(ev.shape[0])
    p_max = PMAX_FRAC * float(t.max() - t.min())
    P_hat, _, obs_R = best_period(ev[:, 0], P_MIN, p_max, OVERSAMPLE)
    return (float(P_hat), float(obs_R)), int(ev.shape[0])


def _surrogate_R(t, r, tau, rng):
    cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0/1440.0
    block_len = max(1, int(round(BLOCK_MULT * max(float(tau), T14) / cad)))
    p_max = PMAX_FRAC * float(t.max() - t.min())
    Rs = np.empty(B_REF, float)
    for b in range(B_REF):
        rb = _circular_block_bootstrap(r, block_len, rng)
        ev = detect_events(t, rb, DGRID, z_for_extraction=Z_BOOT)
        Rs[b] = best_period(ev[:, 0], P_MIN, p_max, OVERSAMPLE)[2] if ev.shape[0] >= 2 else 0.0
    return Rs


def _ref_fap(Rs, obs_R):
    return (int((Rs >= obs_R).sum()) + 1) / (Rs.size + 1)


def _evt_fap(Rs, obs_R, Bsub=B_EVT):
    from scipy.stats import genpareto
    s = np.sort(Rs[:Bsub])
    u = float(np.percentile(s, 90.0))
    tail = s[s > u] - u
    if obs_R <= u or tail.size < 8:
        return (int((s >= obs_R).sum()) + 1) / (Bsub + 1)
    p_u = float((s > u).mean())
    try:
        c, _, scale = genpareto.fit(tail, floc=0.0)
        sf = float(genpareto.sf(obs_R - u, c, loc=0.0, scale=scale))
    except Exception:
        return (int((s >= obs_R).sum()) + 1) / (Bsub + 1)
    return max(p_u * sf, 1e-6)


def _worker(args):
    """args = (kind, key, path, tau, seed, P_true). Loads residual file, aligns, bootstraps."""
    kind, key, path, tau, seed, P_true = args
    z = np.load(path)
    t = np.asarray(z["time"], float); r = np.asarray(z["resid"], float)
    if r.size < 1000:
        return None
    al, nev = _align(t, r)
    base = {"key": key, "kind": kind}
    if al is None:
        base["routed"] = False; return base
    P_hat, obs_R = al
    Rs = _surrogate_R(t, r, tau, np.random.default_rng(seed))
    base.update({"routed": True, "P_hat": P_hat, "obs_R": obs_R, "n_events": nev,
                 "fap_ref": _ref_fap(Rs, obs_R), "fap_evt": _evt_fap(Rs, obs_R)})
    if P_true is not None:
        P = float(P_true)
        base["P_true"] = P
        base["period_match"] = bool(abs(P_hat - P)/P < 0.01 or
            any(abs(P_hat - P/m)/(P/m) < 0.01 or abs(P_hat - m*P)/(m*P) < 0.01 for m in (2, 3)))
    return base


def run(workers=None, nstars=None, inj_hosts=12):
    from multiprocessing import Pool
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    nm = pd.read_csv("data/manifests/m1/m1_noise_summary.csv").set_index("tic"); nm.index = nm.index.astype(str)
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    avail = {Path(p).stem for p in glob.glob("data/processed/m1/*.npz")}
    cleaned = sorted((draw - exc) & avail)
    cal_tics = set(man[man.split == "calibration"]["tic"])
    assert set(cleaned) <= cal_tics, "TEST LEAK in null pool"
    assert not (set(cleaned) & exc), "contaminant in null pool"
    if nstars:
        cleaned = cleaned[:nstars]
    print(f"[equiv] cleaned null pool: {len(cleaned)} stars (0 TEST TICs; 0 contaminants)", flush=True)

    def tau_of(tic):
        return float(nm.loc[tic, "tau_gp_days"]) if tic in nm.index else 0.005

    args = [("null", tic, f"data/processed/m1/{tic}.npz", tau_of(tic),
             SEED ^ (int(tic) & 0x7FFFFFFF), None) for tic in cleaned]

    # ---- pre-build injections to temp npz (cheap; no bootstrap here) ----
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir(parents=True, exist_ok=True)
    ld = INJ.constant_ld(); rng = np.random.default_rng(20260619)
    hosts = man[(man.split == "calibration") & (man.tic.isin(cleaned)) & (man.rad > 0)
                & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    n_inj = 0
    for (P, Rp) in INJ_GRID:
        hh = hosts.sample(min(inj_hosts, len(hosts)), random_state=(hash((P, Rp)) & 0xFFFF))
        for _, row in hh.iterrows():
            tic = row["tic"]
            z = np.load(f"data/processed/m1/{tic}.npz")
            t = np.asarray(z["time"], float); r0 = np.asarray(z["resid"], float)
            if r0.size < 1000:
                continue
            built = INJ.build_injection(t, P, Rp, 0.0, row, ld, rng, host_mode="cached_residual", r_host=r0)
            if built is None:
                continue
            _, r, truth = built
            key = f"{tic}_P{P}_R{Rp}_{n_inj}"
            p = TMP / f"{key}.npz"; np.savez_compressed(p, time=t, resid=r)
            args.append(("inj", key, str(p), tau_of(tic),
                         (SEED ^ (int(tic) & 0x7FFFFFFF)) ^ int(P*1000) ^ (Rp*7) ^ n_inj, float(P)))
            n_inj += 1
    print(f"[equiv] pre-built {n_inj} injections across {len(INJ_GRID)} cells", flush=True)

    nw = workers or max(1, (os.cpu_count() or 2) - 2)
    t0 = time.perf_counter(); rows = []
    with Pool(nw) as pool:
        for i, res in enumerate(pool.imap_unordered(_worker, args, chunksize=1), 1):
            if res is not None:
                rows.append(res)
            if i % 50 == 0:
                print(f"[equiv] {i}/{len(args)}  ({(time.perf_counter()-t0)/60:.1f} min)", flush=True)
    df = pd.DataFrame(rows)
    nd = df[df.kind == "null"].copy(); idf = df[df.kind == "inj"].copy()

    out = Path("data/manifests/m4/equivalence")
    nd.to_csv(out / "equiv_nulls.csv", index=False)
    idf.to_csv(out / "equiv_injections.csv", index=False)
    shutil.rmtree(TMP, ignore_errors=True)

    # ===================== EVALUATE PRE-STATED CRITERIA =====================
    nr = nd[nd.routed == True].copy()
    near = nr[(nr.fap_ref <= 0.05) | (nr.fap_evt <= 0.05)]
    d = (near.fap_evt - near.fap_ref).abs()
    med_d = float(d.median()) if len(d) else 0.0
    p95_d = float(d.quantile(0.95)) if len(d) else 0.0
    corr = float(np.corrcoef(nr.fap_ref, nr.fap_evt)[0, 1]) if len(nr) > 2 else float("nan")
    crit_i = bool(p95_d <= TAU_ABS)
    ref_pass = nr.fap_ref <= ALPHA; evt_pass = nr.fap_evt <= ALPHA
    discord = int((ref_pass != evt_pass).sum())
    admit_extra = int(((~ref_pass) & evt_pass).sum())
    crit_ii = bool(discord <= max(1, int(0.01*len(nr))) and admit_extra == 0)
    ir = idf[idf.routed == True].copy() if len(idf) else pd.DataFrame()
    if len(ir):
        keep = ir[(ir.fap_ref <= ALPHA) & (ir.period_match == True)]
        clipped = int((keep.fap_evt > ALPHA).sum())
    else:
        keep = pd.DataFrame(); clipped = -1
    crit_iii = bool(clipped == 0)
    verdict = "PASS" if (crit_i and crit_ii and crit_iii) else "FAIL -> confirmer-only fallback"
    summary = {
        "n_null_routed": int(len(nr)), "n_inj_routed": int(len(ir)),
        "null_fap_gate_pass": int(ref_pass.sum()),
        "crit_i_fap_agreement": {"tau_abs": TAU_ABS, "median_abs_dFAP": med_d, "p95_abs_dFAP": p95_d,
                                  "corr_ref_evt": corr, "PASS": crit_i},
        "crit_ii_gate_membership": {"discordant": discord, "limit": max(1, int(0.01*len(nr))),
                                    "admit_extra_FP": admit_extra, "PASS": crit_ii},
        "crit_iii_recall_safety": {"n_ref_pass_periodmatched": int(len(keep)), "clipped_by_evt": clipped,
                                   "PASS": crit_iii},
        "VERDICT": verdict,
        "estimator_of_record": "E-EVT(GPD,B'=100)" if verdict == "PASS" else "bootstrap (fallback)",
    }
    (out / "equivalence_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n================ LEVER-1b EQUIVALENCE VALIDATION ================")
    print(json.dumps(summary, indent=2))
    print(f"\nartifacts -> {out}/  | elapsed {(time.perf_counter()-t0)/60:.1f} min")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--nstars", type=int, default=None)
    ap.add_argument("--inj-hosts", type=int, default=12)
    a = ap.parse_args()
    run(workers=a.workers, nstars=a.nstars, inj_hosts=a.inj_hosts)
