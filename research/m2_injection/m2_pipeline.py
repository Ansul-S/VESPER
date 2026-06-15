"""M2 injection + transit-preservation (eta) pipeline — Phase I.

Per VAL §3 / §4.2 / A.1: inject batman Mandel-Agol transits (quadratic Claret-2017 LD from
TIC stellar params) into real null-pool CALIBRATION light curves, re-run Stage-0 conditioning,
recover delta_post at the known ephemeris, and report eta = delta_post/delta_true per (P,R_p)
cell. Requires median eta >= 0.90 (sealed); else the detrend window is widened before M3.

Contract: CALIBRATION null-pool hosts only (TEST sealed until M4); injection grid + eta_min are
sealed and not modified here; no detection threshold is set (M3 / Seal #2).

Run:  python m2_pipeline.py --config config/m2_config.yaml [--cells N] [--per-cell K] [--hosts H]
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

R_EARTH_OVER_R_SUN = 6.371e6 / 6.957e8   # R_earth / R_sun
G_CGS = 6.674e-8
R_SUN_CM = 6.957e10


def load_config(path: str) -> dict[str, Any]:
    import yaml
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if cfg["eta_check"]["hosts"] != "null_pool_calibration":
        raise ValueError("M2 eta hosts must be null_pool_calibration (TEST sealed).")
    if float(cfg["eta_check"]["eta_min"]) != 0.90:
        raise ValueError("eta_min is sealed at 0.90 (VAL §4.2); do not change.")
    return cfg


def build_ld_interpolator():
    """Claret 2017 TESS quadratic LD (VizieR J/A+A/600/A30 tableab): (Teff,logg)->(u1,u2) at solar Z."""
    import numpy as np
    from astroquery.vizier import Vizier
    from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

    v = Vizier(columns=["*"]); v.ROW_LIMIT = -1
    tab = v.get_catalogs("J/A+A/600/A30/tableab")[0].to_pandas()
    tab = tab[np.isclose(tab["Z"], 0.0)]                 # solar metallicity
    if "Mod" in tab and tab["Mod"].nunique() > 1:
        tab = tab[tab["Mod"] == tab["Mod"].mode().iloc[0]]  # single model atmosphere
    tab = tab.dropna(subset=["Teff", "logg", "aLSM", "bLSM"]).drop_duplicates(["Teff", "logg"])
    pts = tab[["Teff", "logg"]].to_numpy(float)
    u1 = LinearNDInterpolator(pts, tab["aLSM"].to_numpy(float))
    u2 = LinearNDInterpolator(pts, tab["bLSM"].to_numpy(float))
    u1n = NearestNDInterpolator(pts, tab["aLSM"].to_numpy(float))
    u2n = NearestNDInterpolator(pts, tab["bLSM"].to_numpy(float))

    def ld(teff, logg):
        a, b = float(u1(teff, logg)), float(u2(teff, logg))
        if not np.isfinite(a):
            a = float(u1n(teff, logg))
        if not np.isfinite(b):
            b = float(u2n(teff, logg))
        return a, b
    print(f"[M2.2] Claret-2017 LD table: {len(tab)} (Teff,logg) nodes at solar Z")
    return ld


def _geometry(P_days, rp_rearth, b, rstar_rsun, logg, ld):
    """Density-based transit geometry (e=0): a/R*, inc, T14, depth, (u1,u2)."""
    import numpy as np
    k = (rp_rearth * R_EARTH_OVER_R_SUN) / rstar_rsun           # Rp/R*
    depth = k * k
    g = 10.0 ** logg                                            # cgs
    P_s = P_days * 86400.0
    a_rs = (g * P_s ** 2 / (4 * np.pi ** 2 * (rstar_rsun * R_SUN_CM))) ** (1.0 / 3.0)
    a_rs = max(a_rs, 1.5)
    cosi = min(b / a_rs, 0.999)
    inc = np.degrees(np.arccos(cosi))
    arg = max(((1 + k) ** 2 - b ** 2), 0.0)
    t14 = (P_days / np.pi) * np.arcsin(min(1.0, (1.0 / a_rs) * np.sqrt(arg) / np.sin(np.radians(inc))))
    teff = None
    return {"k": k, "depth": float(depth), "a_rs": float(a_rs), "inc": float(inc),
            "t14_days": float(t14)}


def _model(time, t0, P_days, geom, u1, u2, unit_depth=False):
    import batman, numpy as np
    p = batman.TransitParams()
    p.t0, p.per = t0, P_days
    p.rp = 1.0 if unit_depth else geom["k"]
    p.a, p.inc, p.ecc, p.w = geom["a_rs"], geom["inc"], 0.0, 90.0
    p.u, p.limb_dark = [u1, u2], "quadratic"
    m = batman.TransitModel(p, np.ascontiguousarray(time)).light_curve(p)
    return m


def _flatten(t, f, d):
    from wotan import flatten
    import numpy as np
    flat, _ = flatten(t, f, window_length=float(d["window_length_days"]), method=d["method"],
                      break_tolerance=float(d["break_tolerance_days"]),
                      edge_cutoff=float(d["edge_cutoff_days"]), cval=float(d["cval"]), return_trend=True)
    ok = np.isfinite(flat)
    return t[ok], flat[ok] - 1.0


def inject_measure(t_raw, f_raw, t0, P_days, geom, u1, u2, d):
    """Inject transit into raw flux, re-condition, recover delta_post via fixed-shape LS."""
    import numpy as np
    model = _model(t_raw, t0, P_days, geom, u1, u2)          # depth = geom['depth']
    f_inj = f_raw * model
    tc, r = _flatten(t_raw, f_inj, d)
    if tc.size < 50:
        return None
    # unit-depth profile with the CORRECT geometry (min ~ -1): actual model normalized by its depth
    shape = (_model(tc, t0, P_days, geom, u1, u2) - 1.0) / geom["depth"]
    denom = float(shape @ shape)
    if denom <= 0:
        return None
    delta_post = float(shape @ r) / denom                   # LS depth at known ephemeris (r ~ delta * shape)
    in_t = shape < -1e-3
    shape_rms = float(np.sqrt(np.mean((r[in_t] - delta_post * shape[in_t]) ** 2)) / geom["depth"]) if in_t.any() else np.nan
    return geom["depth"], delta_post, shape_rms


def run(config_path: str, cells: int | None = None, per_cell: int | None = None, hosts: int | None = None) -> None:
    import datetime, json, hashlib, sys, warnings
    import numpy as np, pandas as pd, lightkurve as lk, yaml
    warnings.filterwarnings("ignore")

    cfg = load_config(config_path)
    d = yaml.safe_load(open(cfg["input"]["m1_config"]))["detrend"]   # frozen M1 detrend params
    grid = cfg["injection_grid_reference"]
    seed = int(cfg["system"]["rng_seed"]); rng = np.random.default_rng(seed)
    K = per_cell or int(cfg["eta_check"]["injections_per_cell"])
    bvals = grid["impact_b"]; frozen = set(int(s) for s in cfg["input"]["sectors"])
    outdir = Path(cfg["output"]["summary_dir"]); outdir.mkdir(parents=True, exist_ok=True)

    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    toi_tics = set(pd.read_csv("data/manifests/m0/m0_toi_snapshot.csv")["tic"].astype(str))
    cal = man[man["split"] == "calibration"].copy()
    null = cal[~cal["tic"].astype(str).isin(toi_tics)].copy()   # null = no TOI of any disposition
    assert (null["split"] == "calibration").all(), "TEST LEAK"
    print(f"[M2.2] null-pool calibration hosts available: {len(null)} (of {len(cal)} calibration)")
    Hn = hosts or min(150, len(null))
    hostdf = null.sample(Hn, random_state=seed).reset_index(drop=True)
    ld = build_ld_interpolator()

    # preload raw (pre-detrend) LCs for the host set, restricted to frozen sectors
    raw = {}
    for _, row in hostdf.iterrows():
        tic = str(row["tic"])
        try:
            sr = lk.search_lightcurve(f"TIC {tic}", mission="TESS", author="SPOC", exptime=120)
            keep = [i for i, s in enumerate(sr.table["sequence_number"]) if int(s) in frozen]
            ts, fs = [], []
            for i in keep:
                lc = sr[int(i)].download(quality_bitmask=cfg.get("_q", "default")).remove_nans()
                tt = np.asarray(lc.time.value, float); ff = np.asarray(lc.flux.value, float)
                ok = np.isfinite(tt) & np.isfinite(ff) & (ff > 0)
                if ok.sum() > 100:
                    ts.append(tt[ok]); fs.append(ff[ok] / np.median(ff[ok]))   # per-sector normalized
            if ts:
                raw[tic] = (np.concatenate(ts), np.concatenate(fs), row)
        except Exception:
            continue
    print(f"[M2.2] preloaded {len(raw)} null-pool host LCs (frozen sectors {sorted(frozen)})")

    periods = grid["period_days"]; radii = grid["radius_rearth"]
    cell_list = [(P, Rp) for P in periods for Rp in radii]
    if cells:
        cell_list = cell_list[:cells]
    keys = list(raw.keys())
    rows = []
    for (P, Rp) in cell_list:
        etas = []
        for _ in range(K):
            tic = keys[rng.integers(len(keys))]
            t_raw, f_raw, srow = raw[tic]
            b = bvals[rng.integers(len(bvals))]
            geom = _geometry(P, Rp, b, float(srow["rad"]), float(srow["logg"]), ld)
            u1, u2 = ld(float(srow["Teff"]), float(srow["logg"]))
            span = (t_raw.min(), t_raw.max())
            t0 = rng.uniform(span[0] + 0.5, span[1] - 0.5)
            res = inject_measure(t_raw, f_raw, t0, P, geom, u1, u2, d)
            if res is None:
                continue
            dt, dp, _sr = res
            etas.append(dp / dt)
        etas = np.array(etas)
        med = float(np.nanmedian(etas)) if etas.size else np.nan
        lo, hi = (float(np.nanpercentile(etas, 16)), float(np.nanpercentile(etas, 84))) if etas.size else (np.nan, np.nan)
        rows.append({"period_days": P, "radius_rearth": Rp, "n": int(etas.size),
                     "eta_median": med, "eta_p16": lo, "eta_p84": hi, "pass": bool(med >= 0.90)})
        print(f"[M2.3] P={P:>4} Rp={Rp:>2}: eta_med={med:.3f} [{lo:.3f},{hi:.3f}] n={etas.size} "
              f"{'PASS' if med>=0.90 else 'FAIL'}")

    eta = pd.DataFrame(rows)
    eta.to_csv(outdir / "m2_eta_table.csv", index=False)
    n_fail = int((~eta["pass"]).sum())
    freeze = __import__("subprocess").run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True).stdout
    (outdir / "pip-freeze.lock").write_text(freeze)
    prov = {
        "milestone": "M2", "stage": "injection + transit-preservation (eta)",
        "config_sha256": hashlib.sha256(Path(config_path).read_bytes()).hexdigest(),
        "manifest_seal1_sha256": cfg["input"]["manifest_seal1_sha256"],
        "detrend_window_days": d["window_length_days"], "eta_min": 0.90,
        "n_hosts": len(raw), "injections_per_cell": K, "seed": seed,
        "n_cells": len(eta), "n_cells_fail": n_fail,
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "eta_overall_median": float(np.nanmedian(eta["eta_median"])) if len(eta) else None,
        "note": "eta>=0.90 required per (P,Rp). Failing cells -> widen window (M2.4) before M3. TEST untouched; no thresholds.",
    }
    (outdir / "m2_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    print(f"\n[M2.5] eta table -> {outdir}/m2_eta_table.csv | cells failing eta>=0.90: {n_fail}/{len(eta)}")


def main() -> None:
    p = argparse.ArgumentParser(description="M2 injection + eta pipeline (Phase I).")
    p.add_argument("--config", default=str(Path(__file__).parent / "config" / "m2_config.yaml"))
    p.add_argument("--cells", type=int, default=None, help="Cap number of (P,Rp) cells (smoke test).")
    p.add_argument("--per-cell", type=int, default=None, help="Override injections per cell.")
    p.add_argument("--hosts", type=int, default=None, help="Override null-host count.")
    a = p.parse_args()
    run(a.config, cells=a.cells, per_cell=a.per_cell, hosts=a.hosts)


if __name__ == "__main__":
    main()
