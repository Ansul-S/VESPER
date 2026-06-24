"""Combined-arm system dry-run — CALIBRATION-ONLY. Measures actual E1 + E2 for the full
Option-2 architecture: route -> epoch-fixed confirm -> full-TLS fallback. NO TEST. NO seal change.

Architecture under test (recall-safe, per review-board F-2):
  Arm A (baseline): full TLS, SDE >= T_A.
  Arm B (combined): detector -> route (>= N_min events) -> period-from-spacing + block-bootstrap FAP;
     if routed AND FAP <= alpha_fap: red-noise epoch-fixed MF S/N at (P_hat, t0_hat);
        if MF >= T_red -> CONFIRMED cheap (no TLS);
        else            -> full-TLS fallback (SDE >= T_A).
     else (not routed / monotransit / weak FAP) -> full-TLS fallback (SDE >= T_A).
  Recovery (VAL §4.1) applied to both arms: period 1%/harmonic, epoch +/-0.5 T14,
     significance = (Arm A & fallback: SDE>=T_A) / (cheap confirm: MF>=T_red).

T_red is calibrated on the cleaned null pool WITHIN this run (FAR<=1%/star). Recovery is
measured in parallel (deterministic); E2 compute is timed on a serial subset (no contention).

Run (offline): .venv/bin/python research/m4_evaluation/combined_arm_dryrun.py [--per-cell N]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "m3_calibration"))

import injection as INJ                     # noqa: E402
import seal_loader as SL                    # noqa: E402
import arms as ARMS                         # noqa: E402
import recovery as REC                      # noqa: E402
import endpoints as EP                      # noqa: E402
from detector import detect_events          # noqa: E402
from period_recovery import best_period, period_fap  # noqa: E402
from epoch_fixed_diagnostic import rednoise_snr_fixed  # noqa: E402  (validated confirmer)

CACHE = Path("data/processed/m1")
_FR = None  # frozen thresholds, set per-process


def _resid(tic):
    z = np.load(CACHE / f"{tic}.npz")
    return np.asarray(z["time"], float), np.asarray(z["resid"], float)


def _route_and_seed(t, r, fr, rng):
    """detector -> (n_events, P_hat, t0_hat, T14, FAP). Returns dict; routed iff n>=N_min."""
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    n = ev.shape[0]
    out = {"n_events": int(n), "routed": n >= fr.n_min, "p_hat": np.nan, "t0_hat": np.nan,
           "t14": float(np.median(fr.duration_grid)), "fap": np.nan}
    if n >= fr.n_min:
        k = int(np.argmax(ev[:, 1]))
        out["t0_hat"], out["t14"] = float(ev[k, 0]), float(ev[k, 2])
        pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
        P_hat, _, obs_R = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)
        out["p_hat"] = float(P_hat) if np.isfinite(P_hat) else np.nan
        if np.isfinite(P_hat):
            fap, _ = period_fap(t, r, obs_R, 0.005, out["t14"], fr.duration_grid,
                                fr.period_min_days, pmax, fr.z_star, fr.block_len_multiple,
                                fr.B, rng)
            out["fap"] = float(fap)
    return out


def candidate_score(t, r, fr, rng):
    """Null candidate score for T_red calibration: red MF at (P_hat,t0_hat) if routed&FAP-ok, else 0."""
    s = _route_and_seed(t, r, fr, rng)
    if s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]):
        return rednoise_snr_fixed(t, r, s["p_hat"], s["t0_hat"], s["t14"])[0]
    return 0.0


# ---------- parallel recovery worker ----------
def _recover_worker(task):
    tic, P, Rp, b, seed = task
    fr = _FR
    rng = np.random.default_rng(seed)
    t, r0 = _resid(tic)
    srow = _MAN.loc[tic]
    built = INJ.build_injection(t, P, Rp, b, srow, _LD, rng, host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    # Arm A: full TLS
    a = ARMS.arm_a_full(t, r, fr)
    rec_a = REC.recovered(a, truth, fr.T_sde)
    # Arm B: route -> confirm -> fallback
    s = _route_and_seed(t, r, fr, np.random.default_rng(seed ^ 99))
    confirmed_cheap = False
    if s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]):
        mf = rednoise_snr_fixed(t, r, s["p_hat"], s["t0_hat"], s["t14"])[0]
        if mf >= _T_RED:
            confirmed_cheap = True
            armb = {"period": s["p_hat"], "t0": s["t0_hat"], "sde": np.inf}  # significance via MF>=T_red
            recb = REC._period_match(s["p_hat"], truth["P_true"])
            pok, harm = recb
            eok = REC._epoch_match(s["t0_hat"], s["p_hat"], truth["t0_true"], truth["t14_true"])
            rec_b = {"recovered": bool(pok and eok), "harmonic": bool(harm and pok and eok)}
    if not confirmed_cheap:
        rec_b = {"recovered": rec_a["recovered"], "harmonic": rec_a["harmonic"]}  # full-TLS fallback == Arm A
    return {"tic": tic, "period_days": P, "radius_rearth": int(Rp), "b": b,
            "n_transits": truth["n_transits"], "routed": s["routed"],
            "fap_ok": bool(np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap),
            "confirmed_cheap": confirmed_cheap, "rec_tls": rec_a["recovered"], "rec_comb": rec_b["recovered"]}


def _calib_worker(task):
    tic, seed = task
    t, r = _resid(tic)
    if r.size < 1000:
        return 0.0
    return candidate_score(t, r, _FR, np.random.default_rng(seed))


def _init(man, t_red):
    # Reconstruct per-worker: FrozenThresholds (MappingProxyType) and the LD closure are not
    # picklable through Pool initargs, so build them inside each worker (load_frozen re-verifies hashes).
    global _FR, _MAN, _LD, _T_RED
    _FR, _MAN, _LD, _T_RED = SL.load_frozen(), man, INJ.constant_ld(), t_red


def main():
    import os
    from multiprocessing import Pool
    ap = argparse.ArgumentParser()
    ap.add_argument("--per-cell", type=int, default=5)
    ap.add_argument("--n-null", type=int, default=200)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    args = ap.parse_args()

    fr = SL.load_frozen()
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
    exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
    cleaned = (draw - exc) & avail
    cal = man[(man.split == "calibration") & (man.tic.isin(cleaned)) & (man.rad > 0)
              & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    assert not (set(cal.tic) & exc), "contaminant in pool"
    man_idx = cal.set_index("tic")
    ld = INJ.constant_ld()
    print(f"[combined dry-run] cleaned null pool {len(cal)}; workers {args.workers}", flush=True)

    # ---- 1) calibrate T_red on cleaned nulls (FAR<=1%/star) ----
    null_tics = cal.sample(min(args.n_null, len(cal)), random_state=11).tic.tolist()
    print(f"[T_red] calibrating on {len(null_tics)} cleaned nulls ...", flush=True)
    with Pool(args.workers, initializer=_init, initargs=(man_idx, 0.0)) as pool:
        scores = pool.map(_calib_worker, [(tic, 20260618 ^ hash(tic) & 0x7fffffff) for tic in null_tics])
    scores = np.array(scores)
    T_red = float(np.percentile(scores, 99))
    print(f"[T_red] cleaned-null 99th pct (FAR<=1%/star) = {T_red:.2f}  (routed nulls {(scores>0).mean()*100:.0f}%, max {scores.max():.1f})")

    # ---- 2) parallel recovery over the injection grid ----
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    hosts = cal.sample(min(60, len(cal)), random_state=22).tic.tolist()
    tasks, seedc = [], 0
    for (P, Rp) in cells:
        for j in range(args.per_cell):
            tic = hosts[(j + seedc) % len(hosts)]
            b = INJ.GRID_B[j % len(INJ.GRID_B)]
            tasks.append((tic, P, Rp, b, 20260618 + seedc)); seedc += 1
    print(f"[recovery] {len(tasks)} injections over {args.workers} workers ...", flush=True)
    rows = []
    with Pool(args.workers, initializer=_init, initargs=(man_idx, T_red)) as pool:
        for i, x in enumerate(pool.imap_unordered(_recover_worker, tasks, chunksize=1), 1):
            if x is not None:
                rows.append(x)
            if i % 20 == 0:
                print(f"[recovery] {i}/{len(tasks)} done ...", flush=True)
    df = pd.DataFrame(rows)
    print(f"[recovery] {len(df)} injections; routed {df.routed.mean()*100:.0f}%; confirmed-cheap {df.confirmed_cheap.mean()*100:.0f}%", flush=True)

    # ---- 3) E1 (occurrence-weighted) ----
    e1 = EP.e1_recall(df, dict(fr.w_c), seed=20260618, B=2000)
    print(f"[E1] Delta_R_bar = {e1['delta_R_bar']*100:+.2f} pp  one-sided95-lo = {e1['ci95_one_sided_lower']*100:+.2f} pp "
          f"-> {'PASS' if e1['pass'] else 'FAIL'} (margin -2 pp)")

    # ---- 4) E2 compute: serial timing on a routed subset (no contention; warm numba ONCE) ----
    routed = df[df.routed].copy()
    sub = routed.sample(min(12, len(routed)), random_state=33) if len(routed) else routed
    print(f"[E2] timing {len(sub)} routed stars serially (warming JIT once) ...", flush=True)
    led = []
    warmed = False
    for k, (_, rr) in enumerate(sub.iterrows(), 1):
        tic, P, Rp, b = rr.tic, rr.period_days, rr.radius_rearth, rr.b
        t, r0 = _resid(tic)
        built = INJ.build_injection(t, P, Rp, b, man_idx.loc[tic], ld, np.random.default_rng(7), "cached_residual", r_host=r0)
        if built is None:
            continue
        _, r, _ = built
        if not warmed:               # one-time numba JIT warm, not charged
            ARMS.arm_a_full(t, r, fr); warmed = True
        t0 = time.perf_counter(); ARMS.arm_a_full(t, r, fr); c_full = time.perf_counter() - t0
        t0 = time.perf_counter(); s = _route_and_seed(t, r, fr, np.random.default_rng(7)); c_route = time.perf_counter() - t0
        c_mf = 0.0
        confirmed = False
        if s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]):
            t0 = time.perf_counter(); mf = rednoise_snr_fixed(t, r, s["p_hat"], s["t0_hat"], s["t14"])[0]; c_mf = time.perf_counter() - t0
            confirmed = mf >= T_red
        c_b = c_route + c_mf + (0.0 if confirmed else c_full)  # fallback pays full TLS
        led.append({"cost_full": c_full, "cost_route": c_route, "cost_mf": c_mf,
                    "confirmed_cheap": confirmed, "cost_comb": c_b})
        print(f"[E2] timed {k}/{len(sub)}  full={c_full:.1f}s route={c_route:.1f}s confirmed={confirmed}", flush=True)
    L = pd.DataFrame(led)
    if len(L):
        ratio = L.cost_comb.sum() / L.cost_full.sum()
        rho_d = L.cost_route.sum() / L.cost_full.sum()
        print(f"[E2] routed-population timing (n={len(L)}): combined/full = {ratio:.3f} "
              f"-> reduction {100*(1-ratio):.1f}%  {'PASS' if (1-ratio)>=0.30 and e1['pass'] else 'FAIL'} (>=30% + E1)")
        print(f"     rho_d (route incl. B=1000 FAP / full) = {rho_d:.3f}; confirmed-cheap in subset {L.confirmed_cheap.mean()*100:.0f}%; "
              f"median full {L.cost_full.median():.1f}s route {L.cost_route.median():.2f}s")

    out = Path("data/manifests/m4/dry_run"); out.mkdir(parents=True, exist_ok=True)
    df.to_csv(out / "combined_arm_recovery.csv", index=False)
    if len(L): L.to_csv(out / "combined_arm_timing.csv", index=False)
    summary = {"T_red": T_red, "n_injections": len(df), "routed_frac": float(df.routed.mean()),
               "confirmed_cheap_frac": float(df.confirmed_cheap.mean()),
               "E1": {k: v for k, v in e1.items() if k != "per_cell"},
               "E2": ({"compute_ratio": float(L.cost_comb.sum() / L.cost_full.sum()),
                       "reduction": float(1 - L.cost_comb.sum() / L.cost_full.sum()),
                       "rho_d": float(L.cost_route.sum() / L.cost_full.sum()),
                       "n_timed": len(L)} if len(L) else {}),
               "confirmer": "red-noise epoch-fixed MF (R2 LR-upgrade still pending)",
               "seal2_sha256": fr.seal2_sha256, "test_accessed": False}
    (out / "combined_arm_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    pd.DataFrame(e1["per_cell"]).to_csv(out / "combined_arm_e1_per_cell.csv", index=False)
    print(f"[artifacts] -> {out}/combined_arm_{{recovery,timing,e1_per_cell}}.csv + combined_arm_summary.json")


if __name__ == "__main__":
    main()
