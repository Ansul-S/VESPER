"""M4 orchestrator — the single sealed-TEST run (E1 + E2). EXECUTION-ONLY.

Dry-run (mode=dry_run): validates the entire code path end-to-end on CALIBRATION cached
residuals with NO network and NO TEST access. Production (mode=test) reuses the identical
code on the TEST split exactly once, gated by the owner §10 confirmation token.

All thresholds/weights/grid come from Seal #2 (seal_loader). This file sets no science.

Run (dry-run): .venv/bin/python research/m4_evaluation/m4_run.py --config research/m4_evaluation/config/m4_config.yaml
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import seal_loader as SL          # noqa: E402
import injection as INJ           # noqa: E402
import arms as ARMS               # noqa: E402
import recovery as REC            # noqa: E402
import endpoints as EP            # noqa: E402


def _select_hosts(cfg, mode, split):
    """Return [(tic, t, r, srow, tau_gp)] hosts. Dry-run: cached calibration residuals (offline)."""
    man = pd.read_parquet(cfg["input"]["m0_manifest"]); man["tic"] = man["tic"].astype(str)
    nm = pd.read_csv(cfg["input"]["m1_noise_summary"]); nm["tic"] = nm["tic"].astype(str)
    tau_by_tic = dict(zip(nm["tic"], nm["tau_gp_days"]))
    sub = man[man["split"] == split].copy()
    assert (sub["split"] == split).all(), "SPLIT GUARD VIOLATION"

    cache_dir = Path(cfg["input"]["cached_resid_dir"])
    hosts = []
    if cfg["run"]["host_mode"] == "cached_residual":
        avail = {p.stem for p in cache_dir.glob("*.npz")}
        cand = sub[sub["tic"].isin(avail)]
        cand = cand[(cand["rad"] > 0) & np.isfinite(cand["logg"]) & np.isfinite(cand["Teff"])]
        cand = cand.sample(min(int(cfg["campaign"]["max_hosts"]), len(cand)),
                           random_state=int(cfg["output"]["seed"])).reset_index(drop=True)
        for _, row in cand.iterrows():
            tic = row["tic"]
            z = np.load(cache_dir / f"{tic}.npz")
            t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
            if r.size < 1000:
                continue
            hosts.append((tic, t, r, row, float(tau_by_tic.get(tic, 0.005))))
    else:
        raise SystemExit("[M4] host_mode 'raw' (production) requires the network path; not used in dry-run.")
    return hosts


def _build_injection_set(hosts, cfg, ld, rng):
    cells = [(P, R) for P in INJ.GRID_P for R in INJ.GRID_R]
    if cfg["campaign"].get("limit_cells"):
        cells = cells[: int(cfg["campaign"]["limit_cells"])]
    K = int(cfg["campaign"]["injections_per_cell"])
    injections = []
    for (P, R) in cells:
        for _ in range(K):
            tic, t, r, srow, tau = hosts[rng.integers(len(hosts))]
            b = INJ.GRID_B[rng.integers(len(INJ.GRID_B))]
            built = INJ.build_injection(t, P, R, b, srow, ld, rng,
                                        host_mode="cached_residual", r_host=r)
            if built is None:
                continue
            ti, ri, truth = built
            injections.append({"tic": tic, "t": ti, "r": ri, "tau": tau, **truth})
    return injections


def run(config_path: str) -> None:
    cfg = yaml.safe_load(Path(config_path).read_text())
    mode, split = cfg["run"]["mode"], cfg["run"]["split"]

    # --- guards (fail closed) ---
    SL.reject_frozen_overrides(cfg)
    SL.assert_split_allowed(mode, split, cfg["run"].get("confirm_token"))
    fr = SL.load_frozen()
    print(f"[M4] mode={mode} split={split} | Seal #2 {fr.seal2_sha256[:12]} verified | "
          f"z*={fr.z_star} T={fr.T_sde:.3f} eps={fr.epsilon} N_min={fr.n_min}")

    seed = int(cfg["output"]["seed"]); rng = np.random.default_rng(seed)
    ld = INJ.constant_ld() if cfg["run"]["host_mode"] == "cached_residual" else None
    if cfg["run"]["host_mode"] == "raw":
        from m2_pipeline import build_ld_interpolator
        ld = build_ld_interpolator()

    hosts = _select_hosts(cfg, mode, split)
    print(f"[M4] hosts: {len(hosts)} ({split}, {cfg['run']['host_mode']})")
    injset = _build_injection_set(hosts, cfg, ld, rng)
    print(f"[M4] injection set: {len(injset)} injections over the sealed grid")

    # --- dual-arm run + recovery (recall: single pass, no repeats) ---
    rows = []
    for k, inj in enumerate(injset, 1):
        t, r = inj["t"], inj["r"]
        arng = np.random.default_rng(seed ^ (hash(inj["tic"]) & 0x7FFFFFFF) ^ k)
        a = ARMS.arm_a_full(t, r, fr)
        bb = ARMS.arm_b_combined(t, r, fr, inj["tau"], arng)
        truth = {kk: inj[kk] for kk in ("P_true", "t0_true", "t14_true", "Rp", "b", "depth_true", "n_transits")}
        rec_a = REC.recovered(a, truth, fr.T_sde)
        rec_b = REC.recovered(bb, truth, fr.T_sde)
        rows.append({"tic": inj["tic"], "period_days": inj["P_true"], "radius_rearth": int(inj["Rp"]),
                     "b": inj["b"], "n_transits": inj["n_transits"], "depth_true": inj["depth_true"],
                     "rec_tls": rec_a["recovered"], "rec_comb": rec_b["recovered"],
                     "harm_tls": rec_a["harmonic"], "harm_comb": rec_b["harmonic"],
                     "sde_tls": rec_a["sde"], "sde_comb": rec_b["sde"],
                     "fast_path_eligible": bb["fast_path_eligible"], "tls_mode": bb["tls_mode"],
                     "n_events": bb["n_events"], "monotransit": bb["monotransit"], "fap": bb["fap"]})
        if k % 25 == 0:
            print(f"[M4] dual-arm {k}/{len(injset)} ...", flush=True)
    df = pd.DataFrame(rows)

    # --- E1 ---
    e1 = EP.e1_recall(df, dict(fr.w_c), seed=seed, B=int(fr.B))
    print(f"[M4] E1: Delta_R_bar={e1['delta_R_bar']*100:+.2f}pp  one-sided95-lo={e1['ci95_one_sided_lower']*100:+.2f}pp "
          f"-> {'PASS' if e1['pass'] else 'FAIL'} (margin {e1['margin']*100:.0f}pp)")

    # --- E2 timing (subset, >=5 warm-cache repeats) ---
    elig = df[df["fast_path_eligible"]].copy()
    ledger = None
    if not elig.empty:
        sub_idx = EP.timing_subset(elig, int(cfg["timing"]["per_cell_min"]), int(cfg["timing"]["cap"]), seed)
        reps = int(cfg["timing"]["repeats"])
        led = []
        for ii in sub_idx:
            inj = injset[ii]
            t, r = inj["t"], inj["r"]
            arng = np.random.default_rng(seed ^ 7 ^ ii)
            # warm cache: one untimed pass, then >=5 timed repeats (median)
            ARMS.arm_a_full(t, r, fr); ARMS.arm_b_combined(t, r, fr, inj["tau"], arng)
            cf, cdet, cper, ctls = [], [], [], []
            for _ in range(reps):
                t0 = time.perf_counter(); ARMS.arm_a_full(t, r, fr); cf.append(time.perf_counter() - t0)
                td = time.perf_counter(); ev, dec = ARMS.route(t, r, fr, inj["tau"]); cdet.append(time.perf_counter() - td)
                tp = time.perf_counter()
                if dec["multi_event"] and dec["p_hat"]:
                    from period_recovery import period_fap
                    period_fap(t, r, dec["obs_R"], inj["tau"], float(np.median(fr.duration_grid)),
                               fr.duration_grid, fr.period_min_days,
                               fr.period_max_frac_baseline * (t.max() - t.min()),
                               fr.z_star, fr.block_len_multiple, fr.B, np.random.default_rng(seed ^ ii))
                cper.append(time.perf_counter() - tp)
                tt = time.perf_counter(); ARMS.arm_b_combined(t, r, fr, inj["tau"], arng); ctls.append(time.perf_counter() - tt)
            led.append({"idx": int(ii), "fast_path_eligible": True,
                        "cost_full": float(np.median(cf)), "cost_detector": float(np.median(cdet)),
                        "cost_period": float(np.median(cper)),
                        "cost_tls": float(np.median(ctls)),
                        "cost_comb": float(np.median(cdet) + np.median(cper) + np.median(ctls)),
                        "cost_full_sd": float(np.std(cf)), "cost_comb_sd": float(np.std(ctls))})
        ledger = pd.DataFrame(led)
    e2 = EP.e2_compute(ledger, e1["pass"]) if ledger is not None else {"pass": False, "reason": "no eligible stars"}
    if "compute_ratio" in e2:
        print(f"[M4] E2: reduction={e2['reduction']*100:.1f}% (ratio {e2['compute_ratio']:.3f}) rho_d={e2['rho_d']:.3f} "
              f"n_elig={e2['n_eligible']} -> {'PASS' if e2['pass'] else 'FAIL'}")

    # --- artifacts ---
    base = Path(cfg["output"]["report_dir"]) / ("dry_run" if mode == "dry_run" else "")
    base.mkdir(parents=True, exist_ok=True)
    df.to_csv(base / "m4_per_injection.csv", index=False)
    pd.DataFrame(e1["per_cell"]).to_csv(base / "m4_e1_per_cell.csv", index=False)
    if ledger is not None:
        ledger.to_csv(base / "m4_e2_ledger.csv", index=False)
    prov = {
        "milestone": "M4", "mode": mode, "split": split, "host_mode": cfg["run"]["host_mode"],
        "stage": "DRY-RUN (plumbing validation; offline; NO TEST access)" if mode == "dry_run"
                 else "single sealed-TEST run",
        "seal2_sha256": fr.seal2_sha256, "m3_config_sha256": fr.m3_config_sha256,
        "seal1_sha256": SL.SEAL1_SHA256,
        "n_hosts": len(hosts), "n_injections": int(len(df)),
        "frozen_used": {"z_star": fr.z_star, "z_mono": fr.z_mono, "n_min": fr.n_min, "T_sde": fr.T_sde,
                        "epsilon": fr.epsilon, "alpha_fap": fr.alpha_fap, "B": fr.B,
                        "duration_grid": list(fr.duration_grid)},
        "E1": {k: v for k, v in e1.items() if k != "per_cell"},
        "E2": e2,
        "machine": {"platform": platform.platform(), "python": sys.version.split()[0]},
        "seed": seed, "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "anti_tuning": {"test_accessed": split == "test",
                        "note": "DRY-RUN: TEST NOT accessed; thresholds loaded read-only from Seal #2; "
                                "no sealed value set in this run." if mode == "dry_run" else
                                "single TEST read under owner §10 token."},
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
    }
    (base / "m4_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    print(f"[M4] artifacts -> {base}/  (m4_per_injection.csv, m4_e1_per_cell.csv, "
          f"{'m4_e2_ledger.csv, ' if ledger is not None else ''}m4_provenance.json)")


def main() -> None:
    p = argparse.ArgumentParser(description="M4 evaluation orchestrator (dry-run / sealed-TEST).")
    p.add_argument("--config", default=str(HERE / "config" / "m4_config.yaml"))
    args = p.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
