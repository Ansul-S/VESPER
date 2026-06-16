"""M1 noise-model recompute at the FINALIZED 2.5 d detrend window (M3 prerequisite).

Isolated window-length comparison (0.5 d -> 2.5 d). The eta-sample membership is held
FIXED at the original 188 conditioned targets (research/m1_conditioning/eta_sample_188.txt);
the 12 originally-skipped targets are NOT retried. This is a window-only re-measurement of
the per-target noise model (sigma, CDPP, tau_GP) on identical stars.

Determinism guards (abort-on-drift, never silently continue):
  * seed (20260615) + frozen M0 manifest must reproduce the 200-target selection;
  * the pinned 188 must be a subset of that selection;
  * every pinned TIC must still condition at the frozen sectors. If any fails, STOP and
    report (sample drift) without writing final outputs.

No detection threshold is set here (those are M3 / Seal #2). TEST is never touched.

Run:  python recompute_noise_window.py --config config/m1_config.yaml
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

# reuse the signed M1 tooling verbatim (same conditioning + noise model, new window via config)
from m1_pipeline import _condition_one, _diagnostics, _noise_model, load_config

PINNED = Path(__file__).parent / "eta_sample_188.txt"


def _read_pinned() -> list[str]:
    tics = [ln.strip() for ln in PINNED.read_text().splitlines()
            if ln.strip() and not ln.startswith("#")]
    return sorted(set(tics))


def _reproduce_selection(cfg) -> set[str]:
    m = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    cal = m[m["split"] == "calibration"]
    s = cfg["data_scope"]
    sample = cal.sample(int(s["eta_sample_size"]), random_state=int(s["eta_sample_seed"]))
    return set(str(t) for t in sample["tic"].tolist())


def run(config_path: str) -> None:
    cfg = load_config(config_path)
    d = cfg["detrend"]
    if float(d["window_length_days"]) != 2.5:
        raise SystemExit(f"expected finalized 2.5 d window, got {d['window_length_days']} d")
    print(f"[recompute] window={d['window_length_days']}d  method={d['method']}  split=calibration")

    pinned = _read_pinned()
    sel = _reproduce_selection(cfg)
    print(f"[determinism] pinned={len(pinned)}  seed-200 reselected={len(sel)}  "
          f"subset={set(pinned).issubset(sel)}")
    if not set(pinned).issubset(sel):
        raise SystemExit("DRIFT: pinned 188 not a subset of the reproduced seed-200 selection. STOP.")

    frozen = set(int(s) for s in cfg["input"]["sectors"])
    rows, drift = [], []
    for k, tic in enumerate(pinned, 1):
        try:
            out = _condition_one(tic, frozen, cfg)
        except Exception as e:  # network/IO/condition error -> treat as drift, do not skip silently
            out = None
            drift.append((tic, f"{type(e).__name__}: {e}"))
            continue
        if out is None:
            drift.append((tic, "no frozen-sector product / <100 cadences"))
            continue
        t, r, used = out
        nm, dg = _noise_model(t, r, cfg), _diagnostics(t, r)
        rows.append({"tic": tic, "sectors_used": used, "n_cadences": int(t.size),
                     **{kk: vv for kk, vv in nm.items() if kk != "cdpp_ppm"},
                     **{f"cdpp_{kk}": vv for kk, vv in nm["cdpp_ppm"].items()}, **dg})
        if k % 20 == 0:
            print(f"[recompute] conditioned {len(rows)}/{len(pinned)} ...")

    if drift:
        print(f"\n[ABORT] {len(drift)} pinned target(s) drifted — NOT writing final outputs:")
        for tic, why in drift:
            print(f"   TIC {tic}: {why}")
        raise SystemExit("Sample drift detected. Membership must stay at 188/188. Resolve before M3.")

    if len(rows) != len(pinned):
        raise SystemExit(f"membership mismatch: {len(rows)} != {len(pinned)}")

    summary = pd.DataFrame(rows)
    outdir = Path(cfg["output"]["summary_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    summary.to_parquet(outdir / "m1_noise_summary.parquet")
    summary.to_csv(outdir / "m1_noise_summary.csv", index=False)
    summary.drop(columns=["sectors_used"]).describe().to_csv(outdir / "m1_noise_describe.csv")

    freeze = subprocess.run([sys.executable, "-m", "pip", "freeze"],
                            capture_output=True, text=True).stdout
    (outdir / "pip-freeze.lock").write_text(freeze)
    prov = {
        "milestone": "M1", "stage": "Stage-0 conditioning noise model — RECOMPUTE at finalized window",
        "recompute": {"reason": "window finalized at M2 (eta>=0.90); 0.5 d model superseded",
                      "window_days": float(d["window_length_days"]), "prior_window_days": 0.5,
                      "membership": "pinned-188 (window-only comparison; 12 skipped NOT retried)",
                      "supersedes": "data/manifests/m1/superseded_0.5d/"},
        "config_path": config_path,
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "manifest_seal1_sha256": cfg["input"]["manifest_seal1_sha256"],
        "frozen_sectors": sorted(frozen), "split": "calibration",
        "eta_sample_pinned": len(pinned), "n_conditioned": len(summary), "n_drift": 0,
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "note": "Window FINALIZED at 2.5 d (M2). No thresholds set (M3/Seal #2). TEST untouched.",
        "medians": {c: float(np.nanmedian(summary[c])) for c in summary.columns
                    if c.startswith(("sigma", "cdpp", "tau_gp", "acf", "scatter"))},
    }
    (outdir / "m1_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    print(f"\n[done] recomputed {len(summary)}/{len(pinned)} at 2.5 d -> {outdir}")


def main() -> None:
    p = argparse.ArgumentParser(description="M1 noise-model recompute at 2.5 d (pinned 188).")
    p.add_argument("--config", default=str(Path(__file__).parent / "config" / "m1_config.yaml"))
    args = p.parse_args()
    run(args.config)


if __name__ == "__main__":
    main()
