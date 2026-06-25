"""M6 W2 — Reality check: TOI recall + EB false-positive rejection (TEST-BLIND).

Runs the sealed pipeline on REAL objects: confirmed/known planets (TOIs) and known
eclipsing binaries (EBs). TEST-BLIND by construction — TOIs are restricted to the
CALIBRATION split (the 67 test-split CP/KP TOIs are EXCLUDED; §1.1 of PHASE1_M6_PLAN).
EBs are the calibration null-pool exclusions (already conditioned). Frozen Stage-0 for
any un-cached TOI; sealed thresholds; NO tuning, NO TEST touch, NO sealed value changed.

Metrics:
  TOI recall   — does the pipeline detect a real confirmed planet?
                 Arm A: full-grid TLS SDE >= T.  Arm B: routed & FAP-gated & confirmer-confirmed,
                 else full-TLS fallback (== Arm A).
  EB rejection — of EBs that reach the confirmer, what fraction does the transit-LR vetting
                 (sign / odd-even / no-secondary) REJECT?  (full TLS cannot tell an EB from a
                 planet by SDE alone; the photometric gate is what should reject it.)

Run: .venv/bin/python research/m6_reality_check/reality_check.py --list-only   # samples, NO network
     .venv/bin/python research/m6_reality_check/reality_check.py --condition   # fetch+condition missing TOIs (network)
     .venv/bin/python research/m6_reality_check/reality_check.py --run         # run pipeline on conditioned samples
"""
from __future__ import annotations
import sys, json, argparse, datetime
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "m4_evaluation"))
sys.path.insert(0, str(HERE.parent / "m3_calibration"))
sys.path.insert(0, str(HERE.parent / "m1_conditioning"))
import seal_loader as SL          # noqa: E402
import arms as ARMS               # noqa: E402
import confirmer as CF            # noqa: E402
import m4_driver as M4            # noqa: E402  (reuse _route_and_seed, _resid, verify_v3_manifest, STELLAR, CACHE)

CACHE = Path("data/processed/m1")
OUT = Path("data/manifests/m6"); OUT.mkdir(parents=True, exist_ok=True)
MANIFEST = "data/manifests/m0/m0_manifest.parquet"


def select_samples():
    man = pd.read_parquet(MANIFEST); man["tic"] = man["tic"].astype(str)
    cal = set(man[man.split == "calibration"].tic)
    toi = pd.read_csv("data/manifests/m0/m0_toi_snapshot.csv"); toi["tic"] = toi["tic"].astype(str)
    cpkp = toi[toi.tfopwg_disp.isin(["CP", "KP"])].drop_duplicates("tic")
    toi_tics = sorted(set(cpkp.tic) & cal)                  # CALIBRATION-split only -> test-blind
    exc = pd.read_csv("data/manifests/m3/calibration_exclusions.csv"); exc["tic"] = exc["tic"].astype(str)
    eb_tics = sorted(set(exc[exc.reason == "eclipsing_binary"].drop_duplicates("tic").tic) & cal)
    return toi_tics, eb_tics


def condition_missing(tics):
    """Frozen Stage-0 for any tic without a cached residual (network)."""
    from condition_test_hosts import load_frozen_cfg
    from m1_pipeline import _condition_one
    cfg = load_frozen_cfg(); frozen = set(int(s) for s in cfg["input"]["sectors"])
    miss = [t for t in tics if not (CACHE / f"{t}.npz").exists()]
    print(f"[reality] conditioning {len(miss)} missing (frozen Stage-0, network)...")
    ok, skip = [], []
    for k, tic in enumerate(miss, 1):
        try:
            res = _condition_one(tic, frozen, cfg)
        except Exception as e:
            res = None; skip.append((tic, f"{type(e).__name__}"))
        if res is None:
            if not skip or skip[-1][0] != tic: skip.append((tic, "no frozen-sector product"))
            continue
        t, r, used = res
        np.savez_compressed(CACHE / f"{tic}.npz", time=t, resid=r, sectors=used); ok.append(tic)
        if k % 5 == 0: print(f"[reality] conditioned {len(ok)}/{len(miss)} ...")
    print(f"[reality] conditioned {len(ok)} ({len(skip)} skipped)")
    return ok, skip


def run_star(tic, fr, t_red, kind):
    t, r = M4._resid(tic)
    a = ARMS.arm_a_full(t, r, fr)
    armA = bool(np.isfinite(a.get("sde", np.nan)) and a["sde"] >= fr.T_sde)
    s = M4._route_and_seed(t, r, fr, 0.005, np.random.default_rng(20260625))
    routed = bool(s["routed"])
    fap_ok = bool(np.isfinite(s["fap"]) and s["fap"] <= fr.alpha_fap and np.isfinite(s["p_hat"]))
    confirmed = sign_pass = shape_pass = np.nan; reached = False
    if fap_ok:
        reached = True
        c = CF.confirm(t, r, (s["p_hat"], s["t0_hat"], s["t14"]), M4.STELLAR, t_red)
        confirmed, sign_pass, shape_pass = bool(c["confirmed"]), bool(c["sign_pass"]), bool(c["shape_pass"])
    armB_detect = bool(confirmed is True) or (not (confirmed is True) and armA)   # confirm OR fallback==ArmA
    return {"tic": tic, "kind": kind, "armA_sde": float(a.get("sde", np.nan)), "armA_detect": armA,
            "routed": routed, "fap_ok": fap_ok, "reached_confirmer": reached,
            "sign_pass": sign_pass, "shape_pass": shape_pass, "confirmed": (confirmed if reached else False),
            "armB_detect": armB_detect}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list-only", action="store_true")
    ap.add_argument("--condition", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()

    toi_tics, eb_tics = select_samples()
    cached = {p.stem for p in CACHE.glob("*.npz")}
    print(f"[reality] CALIBRATION TOIs (CP/KP): {len(toi_tics)} ({sum(t in cached for t in toi_tics)} cached) | "
          f"EBs: {len(eb_tics)} ({sum(t in cached for t in eb_tics)} cached) | TEST-BLIND (test TOIs excluded)")
    if a.list_only:
        print("TOI tics:", ",".join(toi_tics)); print("EB tics:", ",".join(eb_tics))
        print("[reality] --list-only: NO network, NO compute."); return

    skip = []
    if a.condition:
        _, skip = condition_missing(toi_tics)
    if not a.run:
        print("[reality] conditioning done; pass --run to execute the pipeline."); return

    fr = SL.load_frozen(); t_red, v3h = M4.verify_v3_manifest()
    print(f"[reality] Seal#2 {fr.seal2_sha256[:12]} v3 {v3h[:12]} T_sde={fr.T_sde:.3f} alpha_fap={fr.alpha_fap} T_red={t_red}")
    avail = {p.stem for p in CACHE.glob("*.npz")}
    rows = []
    for kind, tics in [("TOI", toi_tics), ("EB", eb_tics)]:
        for i, tic in enumerate((t for t in tics if t in avail), 1):
            try:
                rows.append(run_star(tic, fr, t_red, kind))
            except Exception as e:
                print(f"[reality] {kind} {tic}: {type(e).__name__}: {e}")
            if i % 10 == 0: print(f"[reality] {kind} {i} ...")
    df = pd.DataFrame(rows); df.to_csv(OUT / "reality_check.csv", index=False)

    toi = df[df.kind == "TOI"]; eb = df[df.kind == "EB"]
    ebr = eb[eb.reached_confirmer]
    t6 = {
        "TOI_n": int(len(toi)),
        "TOI_armA_recall": float(toi.armA_detect.mean()) if len(toi) else None,
        "TOI_armB_recall": float(toi.armB_detect.mean()) if len(toi) else None,
        "EB_n": int(len(eb)), "EB_n_reached_confirmer": int(len(ebr)),
        "EB_confirmer_rejection_rate": float((~ebr.confirmed).mean()) if len(ebr) else None,
        "EB_rejected_by_shape": int((~ebr.shape_pass.astype(bool)).sum()) if len(ebr) else 0,
        "EB_rejected_by_sign": int((~ebr.sign_pass.astype(bool)).sum()) if len(ebr) else 0,
        "skipped_conditioning": skip,
        "test_blind": True, "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "seal2_sha256": fr.seal2_sha256, "v3_sha256": v3h,
    }
    (OUT / "T6_reality_check.json").write_text(json.dumps(t6, indent=2, default=str))
    print("\n[T6]", json.dumps({k: v for k, v in t6.items() if k != "skipped_conditioning"}, indent=2, default=str))
    print(f"[reality] -> {OUT}/reality_check.csv + T6_reality_check.json")


if __name__ == "__main__":
    main()
