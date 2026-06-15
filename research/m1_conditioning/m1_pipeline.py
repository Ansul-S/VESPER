"""M1 Stage-0 conditioning pipeline — Phase I.

Per VAL A.9 / §4.2 and MATH §2,§9.1: download SPOC 2-min PDCSAP for the CALIBRATION
pool (eta-sample first), apply per-sector wotan biweight detrend + masking -> zero-centred
residual r(t), and fit a per-target noise model (sigma, CDPP, tau_GP).

Contract:
  * CALIBRATION rows ONLY; the TEST split is never touched at M1 (sealed until M4).
  * restricted to the FROZEN M0 sectors (lightkurve returns extended-mission sectors too).
  * no detection threshold is set here (those are M3 / Seal #2).
  * the detrend window is eta-provisional; finalized at M2 (eta >= 0.90) before M3.

Run:  python m1_pipeline.py --config config/m1_config.yaml [--limit N]
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

_THRESHOLD_KEYS = {"z_star", "zstar", "theta", "z_mono", "t_threshold", "sde_threshold",
                   "alpha", "alpha_fap", "epsilon", "tau_threshold"}


def load_config(path: str) -> dict[str, Any]:
    import yaml
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if cfg.get("data_scope", {}).get("split") != "calibration":
        raise ValueError("M1 must run on the CALIBRATION split only (TEST is sealed until M4).")
    leaked = (set(_flatten(cfg)) & _THRESHOLD_KEYS)
    if leaked:
        raise ValueError(f"threshold keys not allowed in M1 config (M3/Seal #2): {sorted(leaked)}")
    return cfg


def _flatten(o: Any) -> set[str]:
    ks: set[str] = set()
    if isinstance(o, dict):
        for k, v in o.items():
            ks.add(str(k).lower()); ks |= _flatten(v)
    elif isinstance(o, (list, tuple)):
        for v in o: ks |= _flatten(v)
    return ks


def m1_1_freeze_config(cfg: dict[str, Any]) -> dict[str, Any]:
    d, n = cfg["detrend"], cfg["noise_model"]
    print(f"[M1.1] detrend={d['method']} window={d['window_length_days']}d | "
          f"noise={n['method']}/{n['kernel']} | split=calibration")
    return cfg


def m1_2_select_sample(cfg: dict[str, Any], limit: int | None = None):
    import pandas as pd
    man = Path("data/manifests/m0/m0_manifest.parquet")
    if not man.exists():
        raise FileNotFoundError("M0 manifest not found locally; download release asset m0-manifest-v1.")
    m = pd.read_parquet(man)
    cal = m[m["split"] == "calibration"]
    s = cfg["data_scope"]
    sample = cal.sample(int(s["eta_sample_size"]), random_state=int(s["eta_sample_seed"])).reset_index(drop=True)
    assert (sample["split"] == "calibration").all(), "TEST LEAK in eta-sample"
    if limit:
        sample = sample.iloc[:limit].copy()
    print(f"[M1.2] eta-sample: {len(sample)} calibration targets (of {len(cal)})")
    return sample


def _condition_one(tic: str, frozen_sectors: set[int], cfg: dict[str, Any]):
    """Download frozen-sector SPOC 2-min LCs, per-sector biweight detrend + mask -> r(t)."""
    import lightkurve as lk
    import numpy as np
    from wotan import flatten

    d = cfg["detrend"]
    sr = lk.search_lightcurve(f"TIC {tic}", mission="TESS", author="SPOC", exptime=120)
    keep = [i for i, sec in enumerate(sr.table["sequence_number"]) if int(sec) in frozen_sectors]
    if not keep:
        return None
    times, res = [], []
    used = []
    for i in keep:
        lc = sr[int(i)].download(quality_bitmask=cfg["masking"]["spoc_quality_bitmask"])
        lc = lc.remove_nans()
        t = np.asarray(lc.time.value, float)
        f = np.asarray(lc.flux.value, float)
        good = np.isfinite(t) & np.isfinite(f) & (f > 0)
        t, f = t[good], f[good]
        if t.size < 100:
            continue
        flat, _ = flatten(t, f, window_length=float(d["window_length_days"]), method=d["method"],
                          break_tolerance=float(d["break_tolerance_days"]),
                          edge_cutoff=float(d["edge_cutoff_days"]), cval=float(d["cval"]),
                          return_trend=True)
        ok = np.isfinite(flat)
        times.append(t[ok]); res.append(flat[ok] - 1.0)  # zero-centred: transit = negative
        used.append(int(sr.table["sequence_number"][int(i)]))
    if not times:
        return None
    return np.concatenate(times), np.concatenate(res), sorted(set(used))


def _noise_model(t, r, cfg: dict[str, Any]):
    """sigma (robust), CDPP at reference durations (binned RMS), tau_GP (celerite2 SHOTerm; ACF fallback)."""
    import numpy as np
    sigma = 1.4826 * np.median(np.abs(r - np.median(r)))  # robust MAD
    cadence_days = np.median(np.diff(np.sort(t))) if t.size > 1 else 2.0 / 1440.0
    cdpp = {}
    for hours in cfg["noise_model"]["cdpp_reference_durations_hours"]:
        nbin = max(1, int(round((hours / 24.0) / cadence_days)))
        k = (r.size // nbin) * nbin
        if k >= nbin:
            binned = r[:k].reshape(-1, nbin).mean(axis=1)
            cdpp[f"{hours}h_ppm"] = float(np.std(binned) * 1e6)
    tau_acf, tau_cel = _tau_gp(t, r, sigma)
    return {"sigma_ppm": float(sigma * 1e6), "cdpp_ppm": cdpp,
            "tau_gp_days": tau_acf, "tau_celerite2_days": tau_cel,
            "tau_method": "acf_efolding(primary)+celerite2_SHOTerm(xcheck)"}


def _tau_gp(t, r, sigma):
    """Operational tau_GP = residual ACF e-folding (robust; A.8 permits GP/robust).
    celerite2 SHOTerm is fit as a recorded cross-check (seeded from the ACF estimate)."""
    import numpy as np
    step = max(1, t.size // 4000)
    tt, rr = t[::step], r[::step]
    cad = float(np.median(np.diff(np.sort(tt)))) if tt.size > 1 else step * 2.0 / 1440.0

    # primary: ACF e-folding on the (thinned) residuals
    x = rr - rr.mean()
    ac = np.correlate(x, x, mode="full")[x.size - 1:]
    ac = ac / ac[0] if ac[0] != 0 else ac
    below = np.where(ac < np.exp(-1))[0]
    tau_acf = float((int(below[0]) if below.size else 1) * cad)

    # cross-check: celerite2 SHOTerm MLE, seeded from tau_acf
    tau_cel = float("nan")
    try:
        import celerite2
        from celerite2 import terms
        from scipy.optimize import minimize

        yerr = np.full_like(rr, sigma if sigma > 0 else np.std(rr) + 1e-9)

        def nll(p):
            try:
                term = terms.SHOTerm(sigma=np.exp(p[0]), rho=np.exp(p[1]), tau=np.exp(p[2]))
                gp = celerite2.GaussianProcess(term, mean=0.0)
                gp.compute(tt, yerr=yerr, quiet=True)
                return -gp.log_likelihood(rr)
            except Exception:
                return 1e10
        rho0 = max(tau_acf, 5 * cad)
        res = minimize(nll, [np.log(np.std(rr) + 1e-9), np.log(rho0), np.log(rho0)],
                       method="Nelder-Mead", options={"maxiter": 600, "xatol": 1e-3, "fatol": 1e-3})
        if res.fun < 1e9:
            tau_cel = float(np.exp(res.x[1]))
    except Exception:
        pass
    return tau_acf, tau_cel


def _diagnostics(t, r):
    import numpy as np
    half = t.size // 2
    s1 = 1.4826 * np.median(np.abs(r[:half] - np.median(r[:half])))
    s2 = 1.4826 * np.median(np.abs(r[half:] - np.median(r[half:])))
    x = r - r.mean()
    lag1 = float(np.corrcoef(x[:-1], x[1:])[0, 1]) if x.size > 2 else float("nan")
    return {"scatter_ratio_halves": float(s2 / s1) if s1 > 0 else float("nan"), "acf_lag1": lag1}


def run(config_path: str, limit: int | None = None) -> None:
    import datetime
    import json
    import sys

    import numpy as np
    import pandas as pd

    cfg = load_config(config_path)
    cfg = m1_1_freeze_config(cfg)
    sample = m1_2_select_sample(cfg, limit=limit)
    frozen = set(int(s) for s in cfg["input"]["sectors"])

    outdir = Path(cfg["output"]["summary_dir"]); outdir.mkdir(parents=True, exist_ok=True)
    cond_dir = Path(cfg["output"]["conditioned_dir"]); cond_dir.mkdir(parents=True, exist_ok=True)

    rows, n_ok, n_skip = [], 0, 0
    for j, row in sample.iterrows():
        tic = str(row["tic"])
        try:
            out = _condition_one(tic, frozen, cfg)
        except Exception as e:
            out = None
            print(f"[M1.3] TIC {tic}: download/condition error: {type(e).__name__}")
        if out is None:
            n_skip += 1
            continue
        t, r, used = out
        np.savez_compressed(cond_dir / f"{tic}.npz", time=t, resid=r, sectors=used)  # gitignored
        nm = _noise_model(t, r, cfg)
        dg = _diagnostics(t, r)
        rows.append({"tic": tic, "sectors_used": used, "n_cadences": int(t.size),
                     **{k: v for k, v in nm.items() if k != "cdpp_ppm"},
                     **{f"cdpp_{k}": v for k, v in nm["cdpp_ppm"].items()}, **dg})
        n_ok += 1
        if n_ok % 10 == 0:
            print(f"[M1.3/4] conditioned {n_ok} targets...")

    summary = pd.DataFrame(rows)
    summary.to_parquet(outdir / "m1_noise_summary.parquet")
    summary.to_csv(outdir / "m1_noise_summary.csv", index=False)  # small; tracked
    if len(summary):
        summary.drop(columns=["sectors_used"]).describe().to_csv(outdir / "m1_noise_describe.csv")

    import hashlib
    freeze = __import__("subprocess").run([sys.executable, "-m", "pip", "freeze"],
                                          capture_output=True, text=True).stdout
    (outdir / "pip-freeze.lock").write_text(freeze)
    prov = {
        "milestone": "M1", "stage": "Stage-0 conditioning (eta-sample)",
        "config_path": config_path,
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "manifest_seal1_sha256": cfg["input"]["manifest_seal1_sha256"],
        "frozen_sectors": sorted(frozen), "split": "calibration",
        "eta_sample_requested": int(cfg["data_scope"]["eta_sample_size"]),
        "n_conditioned": n_ok, "n_skipped": n_skip,
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "note": "Window is eta-provisional; finalized at M2 (eta>=0.90). No thresholds set (M3/Seal #2). TEST untouched.",
        "medians": {c: float(np.nanmedian(summary[c])) for c in summary.columns
                    if c.startswith(("sigma", "cdpp", "tau_gp", "acf", "scatter"))} if len(summary) else {},
    }
    (outdir / "m1_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    print(f"\n[M1.5] conditioned {n_ok} targets ({n_skip} skipped). Summary -> {outdir}/m1_noise_summary.parquet")
    if len(summary):
        print(summary[["sigma_ppm", "tau_gp_days", "acf_lag1"]].median().to_string())


def main() -> None:
    p = argparse.ArgumentParser(description="M1 Stage-0 conditioning pipeline (Phase I).")
    p.add_argument("--config", default=str(Path(__file__).parent / "config" / "m1_config.yaml"))
    p.add_argument("--limit", type=int, default=None, help="Cap targets for a smoke test.")
    args = p.parse_args()
    run(args.config, limit=args.limit)


if __name__ == "__main__":
    main()
