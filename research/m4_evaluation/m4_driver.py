"""M4 driver (v3, confirmer-only) — E1 (recall non-inferiority) + E2 (scoped compute).

ONE driver for both the CALIBRATION dress rehearsal (--mode dry_run --split calibration)
and the single TEST run (--mode test --split test --confirm-token ...). The TEST path is
hard-gated by seal_loader.assert_split_allowed (token READ-TEST-ONCE-SEAL2-APPROVED).

v3 architecture (sealed phase1-prereg-v3; manifest 54f06a94...):
  Arm A (baseline): full-grid TLS, SDE >= T_sde.
  Arm B (combined): detector -> route (>= N_min events) -> period-from-spacing
     -> B=1000 block-bootstrap period-FAP gate (sealed A.8; Lever-1b DROPPED, equivalence failed)
     -> if FAP <= alpha_fap: TRANSIT-LR confirmer (confirmer.confirm, sealed T_red=0.0,
        sign + odd/even + secondary vetting)  [box depth-SNR REJECTED, DR-002 2.2]
            confirmed -> cheap recovery (period+epoch match; significance = Lambda>=T_red)
            else      -> full-TLS fallback (== Arm A)
     -> not routed / weak FAP -> full-TLS fallback.
Recovery (VAL 4.1) identical both arms; significance arm-specific at COMMON FAR (keystone A6 v3).
T_red is SEALED (=0.0) — NOT recalibrated here (recalibration post-seal would violate the freeze).

NO sealed value changed. Seal #2 + v3 manifest hashes verified fail-closed before any compute.
Run (dress rehearsal):  .venv/bin/python research/m4_evaluation/m4_driver.py --mode dry_run --split calibration --per-cell 8

AUDIT REMEDIATION (2026-07-19; affects FUTURE runs only — the sealed TEST run of
2026-06-24 used the pre-fix behavior, disclosed in M4_ERRATUM_2026-07-19):
  * host assignment: the sealed run's hosts[(j+sc) % 80] walked the host list with
    stride 2 (both j and sc increment), so only the 40 even-indexed of the 80 drawn
    hosts were ever used. Fixed to hosts[sc % len(hosts)] (full coverage).
  * tau_GP: was hardcoded 0.005 d for every star (M3 calibration used per-star tau);
    now looked up per star from the conditioning noise summaries (fallback 0.005).
  * E2 timing: defaults now follow the frozen PHASE1_M4_PLAN §6 rule (>=10/cell,
    cap 300) with >=5 warm-cache repeats and single-thread CPU-core-seconds
    (time.process_time, use_threads=1) per A.7; the sealed run timed 12 stars once
    each with wall-clock. Decision is now taken on a bootstrap CI (endpoints.py).
  * injection seed is carried into recovery rows so E2 re-times the SAME injections
    E1 counted (the sealed run re-drew epochs with a different rng for timing).
"""
from __future__ import annotations
import argparse, json, sys, time, hashlib, os
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
import injection as INJ          # noqa: E402
import seal_loader as SL         # noqa: E402
import arms as ARMS              # noqa: E402
import recovery as REC           # noqa: E402
import endpoints as EP           # noqa: E402
import confirmer as CF           # noqa: E402
from detector import detect_events            # noqa: E402
from period_recovery import best_period, period_fap  # noqa: E402

CACHE = Path("data/processed/m1")
V3_MANIFEST = Path("data/manifests/m4/v3/m4_v3_threshold_manifest.json")
# Both digests accepted (DR-001 §5a rebrand; content-verified vs tag — see seal_loader).
V3_SEAL_SHAS = {
    "54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18",  # sealed (pre-rebrand)
    "0e600b50ec3b3fc40f8adbe810b5d541d71a9da67a9687789a597e60a8698d83",  # post-rebrand, content-verified
}
V3_SEAL_SHA = "54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18"
STELLAR = {"u1": 0.4, "u2": 0.3}   # constant LD, now actually equal to injection.constant_ld()
                                   # (sealed run used u2=0.25 here vs 0.30 in injection — erratum)
_FR = _MAN = _LD = _TRED = None
_TAU = {}                          # per-star tau_GP lookup (audit fix; sealed run used 0.005 flat)


def _load_tau_table():
    """Per-star tau_GP from the conditioning noise summaries (fallback 0.005 d)."""
    tau = {}
    for p in ("data/manifests/m1/m1_noise_summary.csv",
              "data/manifests/m4/test_conditioning/test_hosts_noise_summary.csv"):
        try:
            t = pd.read_csv(p)
            col = "tau_gp_days" if "tau_gp_days" in t.columns else None
            if col:
                tau.update({str(r["tic"]): float(r[col]) for _, r in t.iterrows()
                            if np.isfinite(r[col])})
        except Exception:
            pass
    return tau


def _tau_for(tic) -> float:
    global _TAU
    if not _TAU:                    # lazy-load so direct callers (M6) get real values too
        _TAU = _load_tau_table()
    return _TAU.get(str(tic), 0.005)


def verify_v3_manifest():
    """Fail-closed: v3 manifest hash must match the sealed value; return sealed T_red."""
    if not V3_MANIFEST.exists():
        raise SystemExit(f"[M4] FATAL: v3 manifest missing: {V3_MANIFEST}")
    h = hashlib.sha256(V3_MANIFEST.read_bytes()).hexdigest()
    if h not in V3_SEAL_SHAS:
        raise SystemExit(f"[M4] FATAL: v3 manifest drift. got {h} expected one of {sorted(V3_SEAL_SHAS)}")
    man = json.loads(V3_MANIFEST.read_text())
    t_red = float(man["v3_A11_confirmer"]["T_red"])
    if man["v3_A8_period_FAP"]["A8a_cheap_estimator_admitted"] is not None:
        raise SystemExit("[M4] FATAL: v3 manifest claims a cheap estimator; expected confirmer-only.")
    return t_red, h


def _resid(tic):
    z = np.load(CACHE / f"{tic}.npz")
    return np.asarray(z["time"], float), np.asarray(z["resid"], float)


def _route_and_seed(t, r, fr, tau, rng, time_it=False):
    """detector -> route -> period seed -> B=1000 FAP. Returns dict (+ stage costs if time_it)."""
    c = {}
    t0 = time.perf_counter()
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    c["detector"] = time.perf_counter() - t0
    n = ev.shape[0]
    out = {"n_events": int(n), "routed": n >= fr.n_min, "p_hat": np.nan, "t0_hat": np.nan,
           "t14": float(np.median(fr.duration_grid)), "fap": np.nan, "cost": c}
    if n >= fr.n_min:
        k = int(np.argmax(ev[:, 1]))
        out["t0_hat"], out["t14"] = float(ev[k, 0]), float(ev[k, 2])
        pmax = fr.period_max_frac_baseline * float(t.max() - t.min())
        t0 = time.perf_counter()
        P_hat, _, obs_R = best_period(ev[:, 0], fr.period_min_days, pmax, fr.oversampling)
        out["p_hat"] = float(P_hat) if np.isfinite(P_hat) else np.nan
        if np.isfinite(P_hat):
            fap, _ = period_fap(t, r, obs_R, float(tau), out["t14"], fr.duration_grid,
                                fr.period_min_days, pmax, fr.z_star, fr.block_len_multiple, fr.B, rng)
            out["fap"] = float(fap)
        c["period_fap"] = time.perf_counter() - t0
    else:
        c["period_fap"] = 0.0
    return out


def _period_err(p_hat, p_true):
    """Relative period error to truth OR to the nearest counted harmonic; + is-harmonic flag."""
    if not np.isfinite(p_hat) or p_hat <= 0:
        return np.nan, False
    cands = [(abs(p_hat - p_true) / p_true, False)]
    for m in (2, 3):
        cands.append((abs(p_hat - p_true / m) / (p_true / m), True))
        cands.append((abs(p_hat - m * p_true) / (m * p_true), True))
    err, harm = min(cands, key=lambda x: x[0])
    return float(err), bool(harm)


def _epoch_err_t14(t0_hat, p_hat, t0_true, t14_true):
    """Folded epoch offset in units of T14 (the recovery predicate uses <= 0.5)."""
    if not np.isfinite(t0_hat) or not np.isfinite(p_hat) or p_hat <= 0:
        return np.nan
    dphi = (t0_true - t0_hat) % p_hat
    dphi = min(dphi, p_hat - dphi)
    return float(dphi / max(t14_true, 1e-3))


def _recover_worker(task):
    tic, P, Rp, b, seed = task
    fr, t_red = _FR, _TRED
    rng = np.random.default_rng(seed)
    t, r0 = _resid(tic)
    built = INJ.build_injection(t, P, Rp, b, _MAN.loc[tic], _LD, rng, host_mode="cached_residual", r_host=r0)
    if built is None:
        return None
    _, r, truth = built
    a = ARMS.arm_a_full(t, r, fr)
    rec_a = REC.recovered(a, truth, fr.T_sde)
    s = _route_and_seed(t, r, fr, _tau_for(tic), np.random.default_rng(seed ^ 99))

    # --- Arm B pathway (fully instrumented) ---
    eligible = bool(s["routed"])
    fap_ok = bool(np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]))
    p_err, harm = _period_err(s["p_hat"], truth["P_true"]) if np.isfinite(s["p_hat"]) else (np.nan, False)
    p_ok, _ = REC._period_match(s["p_hat"], truth["P_true"]) if np.isfinite(s["p_hat"]) else (False, False)
    e_err = _epoch_err_t14(s["t0_hat"], s["p_hat"], truth["t0_true"], truth["t14_true"])
    e_ok = REC._epoch_match(s["t0_hat"], s["p_hat"], truth["t0_true"], truth["t14_true"]) if np.isfinite(s["p_hat"]) else False
    lam = shape = sign = np.nan; confirmed = False
    if fap_ok:
        c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), STELLAR, t_red)
        lam, shape, sign, confirmed = c["Lambda"], c["shape_pass"], c["sign_pass"], c["confirmed"]
    # decision path
    if confirmed:                       # cheap-confirm: FALLBACK SUPPRESSED; recovery from the seed
        path = "cheap_confirm"; fallback_suppressed = True
        rec_comb = bool(p_ok and e_ok); confirmed_cheap = True
    else:                               # not eligible / weak FAP / confirmer-rejected -> full-TLS fallback == Arm A
        path = ("fallback_not_eligible" if not eligible else
                "fallback_weak_fap" if not fap_ok else "fallback_confirmer_reject")
        fallback_suppressed = False; rec_comb = rec_a["recovered"]; confirmed_cheap = False
    # loss / gain classification vs Arm A
    outcome = ("loss" if (rec_a["recovered"] and not rec_comb) else
               "gain" if (rec_comb and not rec_a["recovered"]) else
               "both" if rec_comb else "neither")
    return {"tic": tic, "period_days": P, "radius_rearth": int(Rp), "b": b, "seed": int(seed),
            "n_transits": truth["n_transits"], "routed": eligible, "fast_path_eligible": eligible,
            "p_hat": float(s["p_hat"]) if np.isfinite(s["p_hat"]) else np.nan,
            "fap": float(s["fap"]) if np.isfinite(s["fap"]) else np.nan, "fap_ok": fap_ok,
            "period_err": p_err, "period_match": bool(p_ok), "harmonic": bool(harm),
            "epoch_err_t14": e_err, "epoch_ok": bool(e_ok),
            "Lambda": float(lam) if np.isfinite(lam) else np.nan,
            "shape_pass": bool(shape) if shape == shape else False,
            "sign_pass": bool(sign) if sign == sign else False,
            "confirmed_cheap": confirmed_cheap, "fallback_suppressed": fallback_suppressed,
            "decision_path": path, "rec_tls": rec_a["recovered"], "rec_comb": rec_comb,
            "outcome_vs_armA": outcome}


def _init(man, t_red):
    global _FR, _MAN, _LD, _TRED, _TAU
    _FR, _MAN, _LD, _TRED = SL.load_frozen(), man, INJ.constant_ld(), t_red
    _TAU = _load_tau_table()


def main():
    from multiprocessing import Pool
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["dry_run", "test"])
    ap.add_argument("--split", required=True)
    ap.add_argument("--confirm-token", default=None)
    ap.add_argument("--per-cell", type=int, default=8)
    # AUDIT FIX 2026-07-19: defaults now match the frozen PHASE1_M4_PLAN §6 timing
    # rule (>=10/cell, cap 300, >=5 repeats). The sealed run used 12 / 2 / 1.
    ap.add_argument("--e2-cap", type=int, default=300, help="max fast-path-eligible stars timed for E2")
    ap.add_argument("--e2-percell", type=int, default=10, help="min eligible stars per cell in the E2 timing subset")
    ap.add_argument("--e2-repeats", type=int, default=5, help="warm-cache timing repeats per star (median taken)")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 4) - 2))
    a = ap.parse_args()

    # ---- HARD GUARDS (fail closed) ----
    SL.assert_split_allowed(a.mode, a.split, a.confirm_token)
    fr = SL.load_frozen()                                    # verifies Seal #2 + m3_config
    t_red, v3h = verify_v3_manifest()                        # verifies v3 manifest
    print(f"[M4 {a.mode}/{a.split}] Seal#2 {fr.seal2_sha256[:12]} | v3 {v3h[:12]} | T_red={t_red} "
          f"| B={fr.B} alpha_fap={fr.alpha_fap} T_sde={fr.T_sde:.3f}", flush=True)

    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    pool_df = man[(man.split == a.split) & (man.rad > 0) & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    if a.mode == "dry_run":      # dress rehearsal on the cleaned calibration null pool
        draw = set(pd.read_csv("data/manifests/m3/m3_per_star.csv")["tic"].astype(str))
        exc = set(pd.read_csv("data/manifests/m3/calibration_exclusions.csv")["tic"].astype(str))
        pool_df = pool_df[pool_df.tic.isin((draw - exc) & avail)]
    else:
        pool_df = pool_df[pool_df.tic.isin(avail)]
    assert (pool_df.split == a.split).all()
    # TEST-blindness assertion for the dress rehearsal
    if a.mode == "dry_run":
        assert not (set(pool_df.tic) & set(man[man.split == "test"].tic)), "TEST LEAK in dry-run pool"
    man_idx = pool_df.set_index("tic"); ld = INJ.constant_ld()
    print(f"[M4] {a.split} host pool: {len(pool_df)} stars; workers {a.workers}", flush=True)

    # ---- recovery over the sealed injection grid ----
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    hosts = pool_df.sample(min(80, len(pool_df)), random_state=22).tic.tolist()
    tasks, sc = [], 0
    for (P, Rp) in cells:
        for j in range(a.per_cell):
            # AUDIT FIX 2026-07-19: was hosts[(j + sc) % len(hosts)] — with both j and
            # sc incrementing per task this walked the (even-length) host list with
            # stride 2, so only half the drawn hosts were ever used (the sealed TEST
            # run used 40 of its 80 hosts). sc alone increments by 1 -> full coverage.
            tic = hosts[sc % len(hosts)]; bb = INJ.GRID_B[j % len(INJ.GRID_B)]
            tasks.append((tic, P, Rp, bb, 20260619 + sc)); sc += 1
    print(f"[M4] recovery: {len(tasks)} injections ...", flush=True)
    outdir = Path("data/manifests/m4") / ("dress_rehearsal" if a.mode == "dry_run" else "test_run")
    outdir.mkdir(parents=True, exist_ok=True)
    partial = outdir / "recovery_partial.csv"           # incremental checkpoint (crash-robust)
    rows = []
    with Pool(a.workers, initializer=_init, initargs=(man_idx, t_red)) as pool:
        for i, x in enumerate(pool.imap_unordered(_recover_worker, tasks, chunksize=1), 1):
            if x is not None:
                rows.append(x)
                hdr = not partial.exists()
                pd.DataFrame([x]).to_csv(partial, mode="a", header=hdr, index=False)  # append-as-you-go
            if i % 40 == 0:
                print(f"[M4] recovery {i}/{len(tasks)} ...", flush=True)
    df = pd.DataFrame(rows)
    print(f"[M4] {len(df)} injections; routed {df.routed.mean()*100:.0f}%; confirmed-cheap {df.confirmed_cheap.mean()*100:.0f}%", flush=True)

    # ---- E1 (occurrence-weighted DeltaR-bar + one-sided 95% CI) ----
    e1 = EP.e1_recall(df, dict(fr.w_c), seed=20260616, B=2000)
    print(f"[E1] DeltaR_bar={e1['delta_R_bar']*100:+.2f}pp lo95={e1['ci95_one_sided_lower']*100:+.2f}pp "
          f"-> {'PASS' if e1['pass'] else 'FAIL'}", flush=True)

    # ---- E2 (frozen PHASE1_M4_PLAN §6 rule: stratified >=10/cell cap 300, >=5 warm
    #      repeats, single-thread CPU-core-seconds; same injections E1 counted) ----
    elig = df[df.fast_path_eligible].copy()
    sub_idx = EP.timing_subset(elig, per_cell_min=a.e2_percell, cap=a.e2_cap, seed=20260616) if len(elig) else pd.Index([])
    sub = elig.loc[elig.index.intersection(sub_idx)] if len(sub_idx) else elig.head(0)
    print(f"[E2] timing {len(sub)} fast-path-eligible stars ({a.e2_repeats} repeats, CPU-time) ...", flush=True)
    led, warmed = [], False
    for k, (_, rr) in enumerate(sub.iterrows(), 1):
        t, r0 = _resid(rr.tic)
        built = INJ.build_injection(t, rr.period_days, rr.radius_rearth, rr.b, man_idx.loc[rr.tic],
                                    ld, np.random.default_rng(int(rr.seed)), "cached_residual", r_host=r0)
        if built is None:
            continue
        _, r, truth = built
        if not warmed:
            ARMS.arm_a_full(t, r, fr); warmed = True
        cf_rep, route_rep = [], []
        s = None
        for _rep in range(a.e2_repeats):
            t0 = time.process_time(); ARMS.arm_a_full(t, r, fr); cf_rep.append(time.process_time() - t0)
            t0 = time.process_time()
            s = _route_and_seed(t, r, fr, _tau_for(rr.tic),
                                np.random.default_rng(int(rr.seed) ^ 99), time_it=True)
            route_rep.append(time.process_time() - t0)
        c_full = float(np.median(cf_rep)); c_route = float(np.median(route_rep))
        c_tls, confirmed = 0.0, False
        if s["routed"] and np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]):
            conf_rep = []
            for _rep in range(a.e2_repeats):
                t0 = time.process_time()
                c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), STELLAR, t_red)
                conf_rep.append(time.process_time() - t0)
            c_tls = float(np.median(conf_rep)); confirmed = c["confirmed"]
        if not confirmed:
            c_tls += c_full                                            # fallback pays full TLS
        led.append({"tic": rr.tic, "cost_full": c_full, "cost_detector": c_route,
                    "cost_period": 0.0, "cost_tls": c_tls, "cost_comb": c_route + c_tls,
                    "fast_path_eligible": True, "confirmed_cheap": confirmed,
                    "cost_full_spread": float(np.std(cf_rep)), "n_repeats": a.e2_repeats})
        if k % 10 == 0:
            print(f"[E2] timed {k}/{len(sub)} full={c_full:.1f}s route={c_route:.2f}s conf={confirmed}", flush=True)
    L = pd.DataFrame(led)
    e2 = EP.e2_compute(L, e1["pass"]) if len(L) else {"decision": "INCONCLUSIVE", "pass": False, "reason": "no timing"}
    if len(L):
        print(f"[E2] reduction={e2['reduction']*100:.1f}% (ratio {e2['compute_ratio']:.3f} "
              f"CI95 [{e2['ratio_ci95'][0]:.3f},{e2['ratio_ci95'][1]:.3f}]) rho_d={e2['rho_d']:.3f} "
              f"-> {e2['decision']}", flush=True)

    # ---- verdict (pre-committed mapping, VAL 7a; CI-based E2 decision per VAL §5's
    #      INCONCLUSIVE clause — audit fix 2026-07-19) ----
    e2_dec = e2.get("decision", "FAIL" if not e2.get("pass") else "PASS")
    if not e1["pass"]:
        verdict = "FALSIFIED — recall branch (E1 fail)"
    elif e2_dec == "PASS":
        verdict = "VALIDATED (E1 pass + E2 pass)"
    elif e2_dec == "FAIL":
        verdict = "FALSIFIED — compute branch (E1 pass, E2 fail)"
    else:
        verdict = "INCONCLUSIVE — E2 CI straddles the sealed 0.70 threshold (VAL §5)"

    outdir = Path("data/manifests/m4") / ("dress_rehearsal" if a.mode == "dry_run" else "test_run")
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "recovery.csv", index=False)
    if len(L): L.to_csv(outdir / "timing_ledger.csv", index=False)
    pd.DataFrame(e1["per_cell"]).to_csv(outdir / "e1_per_cell.csv", index=False)
    summary = {"mode": a.mode, "split": a.split, "test_accessed": a.split == "test",
               "seal2_sha256": fr.seal2_sha256, "v3_manifest_sha256": v3h, "T_red": t_red,
               "n_injections": int(len(df)), "routed_frac": float(df.routed.mean()),
               "confirmed_cheap_frac": float(df.confirmed_cheap.mean()),
               "E1": {k: v for k, v in e1.items() if k != "per_cell"},
               "E2": e2, "verdict_pre_committed": verdict,
               "confirmer": "transit-LR (D-1a/D-2a/D-3-i); box depth-SNR rejected"}
    (outdir / "summary.json").write_text(json.dumps(summary, indent=2, default=str))
    print(f"\n[M4 {a.mode}] VERDICT: {verdict}")
    print(f"[artifacts] -> {outdir}/")


if __name__ == "__main__":
    main()
