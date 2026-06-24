"""Condition the M4 TEST host draw through the FROZEN Stage-0 (M4 prerequisite).

The sealed M4 driver (research/m4_evaluation/m4_driver.py) consumes residual npz from
data/processed/m1/{tic}.npz, but the TEST split was never conditioned — m1_pipeline.py is
calibration-locked BY DESIGN ("TEST is never touched at M1; sealed until M4"). The single
M4 read therefore requires a sanctioned, one-time Stage-0 first-touch of TEST.

This script conditions EXACTLY the hosts the sealed driver draws — test_pool.sample(80,
random_state=22) over the SAME manifest filter the driver applies (split==test, rad>0,
finite logg & Teff) — using the IDENTICAL frozen Stage-0. It reuses m1_pipeline._condition_one
/ _noise_model VERBATIM; it introduces NO new parameter, NO threshold, NO tuning. The only
relaxation vs m1_pipeline.load_config is the calibration-split lock (the threshold-key guard
and frozen-window assertions are preserved and enforced).

Stage-0 ONLY (download + frozen biweight detrend + noise model) — no detection, no period
recovery, no recovery/endpoint computation. It does not read or set any sealed threshold.

Run (sandbox-disabled / host network required for the download):
  .venv/bin/python research/m1_conditioning/condition_test_hosts.py --list-only  # print the 80 TICs, NO network
  .venv/bin/python research/m1_conditioning/condition_test_hosts.py              # condition (network)
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# reuse the signed M1 tooling VERBATIM (identical conditioning + noise model + guards)
from m1_pipeline import _condition_one, _diagnostics, _noise_model, _flatten, _THRESHOLD_KEYS

CONFIG = Path(__file__).parent / "config" / "m1_config.yaml"
MANIFEST = Path("data/manifests/m0/m0_manifest.parquet")
SEAL1_SHA = "1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f"
N_HOSTS = 80           # the sealed driver caps at min(80, len(pool)); fixed here
HOST_SEED = 22         # the sealed driver's random_state for the host draw


def load_frozen_cfg() -> dict:
    """Load the SIGNED M1 config; enforce no-threshold-leak + the frozen 2.5 d biweight window.

    Unlike m1_pipeline.load_config we do NOT require split==calibration (this is the sanctioned
    TEST first-touch), but every other invariant is enforced so no parameter can silently drift.
    """
    import yaml
    cfg = yaml.safe_load(CONFIG.read_text())
    leaked = set(_flatten(cfg)) & _THRESHOLD_KEYS
    if leaked:
        raise ValueError(f"threshold keys not allowed in conditioning config: {sorted(leaked)}")
    d = cfg["detrend"]
    if not (d["method"] == "biweight" and float(d["window_length_days"]) == 2.5
            and float(d["break_tolerance_days"]) == 2.5 and float(d["edge_cutoff_days"]) == 2.5
            and float(d["cval"]) == 5):
        raise SystemExit(f"FROZEN Stage-0 drift in detrend config: {d}. Refusing to condition.")
    if cfg["input"]["manifest_seal1_sha256"] != SEAL1_SHA:
        raise SystemExit("config manifest_seal1_sha256 != Seal #1. Refusing.")
    if [int(s) for s in cfg["input"]["sectors"]] != [1, 2, 3]:
        raise SystemExit(f"frozen sectors drift: {cfg['input']['sectors']}. Refusing.")
    return cfg


def host_draw() -> list[str]:
    """Reproduce the sealed M4 driver's host draw EXACTLY, under full TEST availability.

    Driver (m4_driver.py): man.tic->str; pool=man[(split==test)&(rad>0)&isfinite(logg)&isfinite(Teff)];
    pool=pool[pool.tic.isin(avail)]; hosts=pool.sample(min(80,len),random_state=22). With every TEST
    host conditioned the .isin(avail) step is a no-op, so the intended draw is the full-pool sample
    below; conditioning exactly this set makes the driver's realized draw identical (avail==this set).
    """
    if not MANIFEST.exists():
        raise FileNotFoundError(f"M0 manifest not found: {MANIFEST}")
    man = pd.read_parquet(MANIFEST)
    man["tic"] = man["tic"].astype(str)
    pool = man[(man.split == "test") & (man.rad > 0)
               & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    if len(pool) == 0:
        raise SystemExit("empty TEST host pool — manifest/filter mismatch.")
    hosts = pool.sample(min(N_HOSTS, len(pool)), random_state=HOST_SEED).tic.tolist()
    return hosts


def run(list_only: bool) -> None:
    cfg = load_frozen_cfg()
    hosts = host_draw()
    d = cfg["detrend"]
    print(f"[cond-test] frozen Stage-0: {d['method']} window={d['window_length_days']}d "
          f"sectors={cfg['input']['sectors']} | TEST host draw n={len(hosts)} (seed {HOST_SEED})")
    if list_only:
        print("\n".join(hosts))
        print(f"\n[cond-test] --list-only: {len(hosts)} TICs above; NO network call made.")
        return

    frozen = set(int(s) for s in cfg["input"]["sectors"])
    cond_dir = Path(cfg["output"]["conditioned_dir"]); cond_dir.mkdir(parents=True, exist_ok=True)
    outdir = Path("data/manifests/m4/test_conditioning"); outdir.mkdir(parents=True, exist_ok=True)

    rows, ok, skip = [], [], []
    for k, tic in enumerate(hosts, 1):
        cached = cond_dir / f"{tic}.npz"
        if cached.exists():                       # idempotent: don't re-download an already-conditioned host
            z = np.load(cached)
            t, r = np.asarray(z["time"], float), np.asarray(z["resid"], float)
            used = [int(s) for s in z["sectors"]] if "sectors" in z else []
            nm, dg = _noise_model(t, r, cfg), _diagnostics(t, r)
            rows.append({"tic": tic, "sectors_used": used, "n_cadences": int(t.size),
                         **{kk: vv for kk, vv in nm.items() if kk != "cdpp_ppm"},
                         **{f"cdpp_{kk}": vv for kk, vv in nm["cdpp_ppm"].items()}, **dg})
            ok.append(tic)
            continue
        try:
            out = _condition_one(tic, frozen, cfg)
        except Exception as e:
            out = None
            skip.append((tic, f"{type(e).__name__}: {e}"))
            print(f"[cond-test] TIC {tic}: error {type(e).__name__}")
        if out is None:
            if not skip or skip[-1][0] != tic:
                skip.append((tic, "no frozen-sector product / <100 cadences"))
            continue
        t, r, used = out
        np.savez_compressed(cond_dir / f"{tic}.npz", time=t, resid=r, sectors=used)  # driver reads this
        nm, dg = _noise_model(t, r, cfg), _diagnostics(t, r)
        rows.append({"tic": tic, "sectors_used": used, "n_cadences": int(t.size),
                     **{kk: vv for kk, vv in nm.items() if kk != "cdpp_ppm"},
                     **{f"cdpp_{kk}": vv for kk, vv in nm["cdpp_ppm"].items()}, **dg})
        ok.append(tic)
        if k % 10 == 0:
            print(f"[cond-test] conditioned {len(ok)}/{len(hosts)} ...")

    summary = pd.DataFrame(rows)
    if len(summary):
        summary.to_parquet(outdir / "test_hosts_noise_summary.parquet")
        summary.to_csv(outdir / "test_hosts_noise_summary.csv", index=False)

    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                            capture_output=True, text=True).stdout
    (outdir / "pip-freeze.lock").write_text(freeze)
    prov = {
        "milestone": "M4-prep", "stage": "Stage-0 conditioning of the TEST host draw (sanctioned first-touch)",
        "split": "test", "host_seed": HOST_SEED, "n_hosts_drawn": len(hosts),
        "n_conditioned": len(ok), "n_skipped": len(skip),
        "hosts_drawn": hosts, "hosts_conditioned": ok, "hosts_skipped": skip,
        "config_path": str(CONFIG), "config_sha256": hashlib.sha256(CONFIG.read_bytes()).hexdigest(),
        "manifest_seal1_sha256": SEAL1_SHA,
        "frozen_detrend": cfg["detrend"], "frozen_sectors": sorted(frozen),
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "note": ("Stage-0 ONLY (download + frozen 2.5d biweight detrend + noise model). No detection, "
                 "no recovery, no threshold set or read. Conditions EXACTLY the sealed M4 driver's "
                 "host draw. NO sealed value changed (NN#2). The M4 read itself is the single evaluation."),
        "medians": {c: float(np.nanmedian(summary[c])) for c in summary.columns
                    if c.startswith(("sigma", "cdpp", "tau_gp", "acf", "scatter"))} if len(summary) else {},
    }
    (outdir / "test_conditioning_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    print(f"\n[cond-test] conditioned {len(ok)}/{len(hosts)} TEST hosts ({len(skip)} skipped) -> {cond_dir}/")
    print(f"[cond-test] provenance -> {outdir}/test_conditioning_provenance.json")
    if skip:
        print(f"[cond-test] {len(skip)} skipped (no frozen-sector data); realized host pool = {len(ok)}.")


def main() -> None:
    p = argparse.ArgumentParser(description="Condition the M4 TEST host draw (frozen Stage-0).")
    p.add_argument("--list-only", action="store_true", help="Print the 80 drawn TICs and exit (no network).")
    args = p.parse_args()
    run(args.list_only)


if __name__ == "__main__":
    main()
