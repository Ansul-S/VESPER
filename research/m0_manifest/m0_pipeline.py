"""M0 manifest pipeline — Phase I (scaffold).

Executes milestone M0 of PHASE1_EXECUTION_PLAN.md: freeze the TESS sector/target
manifest and the leakage-safe calibration/test split, then content-hash it (Seal #1).

SCAFFOLD ONLY. Archive-touching bodies raise NotImplementedError until the M0
frozen-choices proposal (PHASE1_M0_CHOICES.md) is signed off and config/m0_config.yaml
is filled. This module is metadata-only by contract:

  * no light-curve flux is downloaded (that is M1);
  * no detection threshold is set (those are M3 / Seal #2);
  * no statistic is computed on the TEST split (plan G1).

Run order (post sign-off):
  python m0_pipeline.py --config config/m0_config.yaml
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

# NOTE: heavy imports (astroquery, astropy, healpy, pandas, pyarrow) are deferred
# into the step bodies so `--help` and import work before the stack is installed.


# Detection-threshold keys that belong to M3 (Seal #2), NOT to an M0 manifest config.
# Their presence here would violate plan guardrail G2 (no thresholds in M0).
_THRESHOLD_KEYS = {
    "z_star", "zstar", "z*", "theta", "z_mono", "t_threshold", "sde_threshold",
    "alpha", "alpha_fap", "epsilon", "eps", "tau_gp",
}


def _flatten_keys(obj: Any) -> set[str]:
    """Collect every mapping key (recursively) for the threshold-leak guard."""
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            keys.add(str(k).lower())
            keys |= _flatten_keys(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            keys |= _flatten_keys(v)
    return keys


def load_config(config_path: str) -> dict[str, Any]:
    """Load and validate the frozen-choices config.

    Guards (plan G1/G2): rejects a config that sets training_split=true, has an empty
    sector list, or smuggles in any detection-threshold key (z*, theta, T, ...) — those
    belong to M3 / Seal #2, never to an M0 manifest config.
    """
    import yaml  # deferred so `--help` works before the stack is installed

    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    if not cfg.get("sectors", {}).get("list"):
        raise ValueError("config error: sectors.list must be non-empty (M0.1).")
    if cfg.get("split", {}).get("training_split", False):
        raise ValueError(
            "config error: split.training_split must be false — Phase I detector is untrained (VAL §3)."
        )
    leaked = _flatten_keys(cfg) & _THRESHOLD_KEYS
    if leaked:
        raise ValueError(
            f"config error: detection-threshold keys are not allowed in an M0 config "
            f"(those are M3 / Seal #2 — plan G2): {sorted(leaked)}"
        )
    return cfg


def m0_1_freeze_sectors(cfg: dict[str, Any]) -> dict[str, Any]:
    """M0.1 — record the frozen SPOC 2-min sector list + rationale (VAL §3)."""
    s = cfg["sectors"]
    frozen = {
        "sectors": [int(x) for x in s["list"]],
        "hemisphere": str(s.get("hemisphere", "")),
        "rationale": str(s.get("rationale", "")).strip(),
    }
    print(f"[M0.1] frozen SPOC 2-min sectors: {frozen['sectors']} ({frozen['hemisphere']})")
    return frozen


def m0_2_build_target_manifest(
    cfg: dict[str, Any], sectors: dict[str, Any], limit: int | None = None
) -> Any:
    """M0.2 — enumerate SPOC 2-min targets in the frozen sectors and apply the
    outcome-independent inclusion/exclusion cuts; cross-match TIC for coords,
    R_star + limb-darkening inputs (Teff/logg), Tmag, and contamination; derive
    per-target observed baseline. Metadata only — no flux. (VAL §3, A.1).

    `limit` caps the target count for a smoke test (None = full run).

    Crowding note: SPOC CROWDSAP is a per-LC FITS-header value, not a catalog
    field. We apply the crowding cut via the TIC contamination ratio `contratio`
    (CROWDSAP ~= 1/(1+contratio)); literal CROWDSAP is confirmed at M1.
    """
    import warnings
    from pathlib import Path

    import pandas as pd
    from astroquery.mast import Catalogs, Observations

    warnings.filterwarnings("ignore")
    outdir = Path(cfg["output"]["manifest_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    sec_list = sectors["sectors"]

    cache = outdir / "m0_targets.parquet"
    if cache.exists() and not limit and not cfg.get("_refresh", False):
        df = pd.read_parquet(cache)
        print(f"[M0.2] loaded cached target manifest: {len(df)} targets ({cache})")
        return df

    # 1) SPOC 2-min observations per sector (metadata table; no files retrieved)
    frames = []
    for s in sec_list:
        obs = Observations.query_criteria(
            obs_collection="TESS", dataproduct_type="timeseries",
            t_exptime=120, sequence_number=s, provenance_name="SPOC",
        )
        df = obs["target_name", "s_ra", "s_dec", "t_min", "t_max", "sequence_number"].to_pandas()
        df["tic"] = df["target_name"].astype(str)
        frames.append(df)
        print(f"[M0.2] sector {s}: {len(df)} SPOC 2-min observations")
    obs_all = pd.concat(frames, ignore_index=True)
    obs_all.to_parquet(outdir / "m0_observations.parquet")

    # 2) aggregate to one row per TIC (sectors observed + observed span)
    agg = (
        obs_all.groupby("tic")
        .agg(
            n_sectors=("sequence_number", "nunique"),
            sectors=("sequence_number", lambda x: sorted({int(i) for i in x})),
            ra=("s_ra", "first"), dec=("s_dec", "first"),
            t_min=("t_min", "min"), t_max=("t_max", "max"),
        )
        .reset_index()
    )
    agg["baseline_days"] = agg["t_max"] - agg["t_min"]
    print(f"[M0.2] unique TICs across sectors {sec_list}: {len(agg)}")
    if limit:
        agg = agg.iloc[:limit].copy()
        print(f"[M0.2] SMOKE TEST — capped to {len(agg)} targets")

    # 3) TIC stellar params (chunked cross-match)
    ids = agg["tic"].tolist()
    keep = ["ID", "Tmag", "Teff", "logg", "rad", "mass", "contratio"]
    tic_frames, chunk = [], 1000
    for i in range(0, len(ids), chunk):
        c = ids[i : i + chunk]
        cat = Catalogs.query_criteria(catalog="Tic", ID=c)
        tic_frames.append(cat[keep].to_pandas())
        print(f"[M0.2] TIC params {min(i + chunk, len(ids))}/{len(ids)}")
    tic = pd.concat(tic_frames, ignore_index=True)
    tic["tic"] = tic["ID"].astype(str)
    m = agg.merge(tic.drop(columns=["ID"]), on="tic", how="left")

    # 4) outcome-independent inclusion cuts (recorded before application; plan G3)
    inc = cfg["inclusion"]
    n0 = len(m)
    if inc.get("require_tic_stellar_params", True):
        m = m[m["Teff"].notna() & m["logg"].notna() & m["rad"].notna()]
    n_params = len(m)
    if inc.get("tmag_min") is not None:
        m = m[m["Tmag"] >= inc["tmag_min"]]
    if inc.get("tmag_max") is not None:
        m = m[m["Tmag"] <= inc["tmag_max"]]
    n_tmag = len(m)
    n_contratio_unknown = 0
    if inc.get("crowdsap_min") is not None:
        cmin = inc["crowdsap_min"]
        contratio_max = (1.0 - cmin) / cmin
        n_contratio_unknown = int(m["contratio"].isna().sum())
        # keep rows with known contratio <= bound; unknown contratio is kept and flagged
        m = m[(m["contratio"].isna()) | (m["contratio"] <= contratio_max)]
    n_crowd = len(m)
    m = m.reset_index(drop=True)

    print(
        f"[M0.2] cuts: start={n0} -> stellar_params={n_params} -> Tmag={n_tmag} "
        f"-> crowding={n_crowd}  (contratio unknown kept: {n_contratio_unknown})"
    )
    m.to_parquet(outdir / "m0_targets.parquet")
    return m


def m0_3_assemble_labels(cfg: dict[str, Any], targets: Any) -> tuple[Any, dict[str, Any]]:
    """M0.3 — label planets/FPs from the NASA Exoplanet Archive TOI table; define the
    null pool as planet-host-removed; tag multi-planet hosts; record incompleteness
    caveat (VAL §3, A.2; H4). ExoFOP was unreachable; NEA TAP is the reproducible source.

    FP labels = TOI FP/FA dispositions (largely EBs/variables). A dedicated TESS EB
    catalog (Prsa et al. 2022) can enrich the FP set at M1+ (eb_catalog provenance note).
    """
    import datetime
    import warnings

    from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

    warnings.filterwarnings("ignore")
    t = NasaExoplanetArchive.query_criteria(table="toi", select="toi,tid,tfopwg_disp")
    toi = t["toi", "tid", "tfopwg_disp"].to_pandas()
    toi = toi.dropna(subset=["tid"])
    toi["tic"] = toi["tid"].astype("Int64").astype(str)

    targets = targets.copy()
    tset = set(targets["tic"])
    toi_in = toi[toi["tic"].isin(tset)].copy()

    planetish = {"PC", "CP", "KP", "APC"}   # planet or candidate -> removed from null pool
    confirmed = {"CP", "KP"}                # confirmed planets -> reality-check positives
    fp_disp = {"FP", "FA"}                  # known false positives -> reality-check negatives

    by_tic = toi_in.groupby("tic")["tfopwg_disp"].apply(list)
    planet_host = {k for k, v in by_tic.items() if any(d in planetish for d in v)}
    confirmed_host = {k for k, v in by_tic.items() if any(d in confirmed for d in v)}
    fp_host = {k for k, v in by_tic.items() if any(d in fp_disp for d in v)}
    n_planetish = toi_in[toi_in["tfopwg_disp"].isin(planetish)].groupby("tic").size()
    multi = set(n_planetish[n_planetish >= 2].index)

    targets["is_known_planet"] = targets["tic"].isin(confirmed_host)
    targets["is_planet_host_or_candidate"] = targets["tic"].isin(planet_host)
    targets["is_known_fp"] = targets["tic"].isin(fp_host)
    targets["is_multiplanet"] = targets["tic"].isin(multi)
    targets["is_null"] = ~targets["tic"].isin(planet_host | fp_host)

    # Pin the in-sample TOI snapshot so the seal's labels are reproducible (non-negotiable #6).
    import hashlib
    from pathlib import Path

    outdir = Path(cfg["output"]["manifest_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    snap = toi_in.sort_values(["tic", "toi"]).reset_index(drop=True)
    snap_path = outdir / "m0_toi_snapshot.csv"
    snap.to_csv(snap_path, index=False)
    snap_hash = hashlib.sha256(snap_path.read_bytes()).hexdigest()

    prov = {
        "toi_source": "NASA Exoplanet Archive TAP, table 'toi'",
        "toi_snapshot_path": str(snap_path),
        "toi_snapshot_sha256": snap_hash,
        "toi_query_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "toi_total_rows": int(len(toi)),
        "toi_in_sample": int(len(toi_in)),
        "n_known_planet_hosts": int(targets["is_known_planet"].sum()),
        "n_planet_host_or_candidate": int(targets["is_planet_host_or_candidate"].sum()),
        "n_known_fp": int(targets["is_known_fp"].sum()),
        "n_multiplanet": int(targets["is_multiplanet"].sum()),
        "n_null": int(targets["is_null"].sum()),
        "null_pool_caveat": (
            "Null = no TOI of any disposition. Catalog incompleteness leaves some "
            "undetected planets in null stars; bounds H4 FAR calibration; reported (R0-3)."
        ),
        "eb_catalog_note": (
            "FP set = TOI FP/FA dispositions (largely EBs/variables). Dedicated TESS EB "
            "catalog (Prsa et al. 2022) can enrich the FP labels at M1+."
        ),
    }
    print(
        f"[M0.3] labels: known-planet={prov['n_known_planet_hosts']} "
        f"planet/cand={prov['n_planet_host_or_candidate']} fp={prov['n_known_fp']} "
        f"multiplanet={prov['n_multiplanet']} null={prov['n_null']}"
    )
    return targets, prov


def m0_4_leakage_safe_split(cfg: dict[str, Any], targets: Any) -> tuple[Any, dict[str, Any]]:
    """M0.4 — whole-HEALPix-block calibration/test split, TIC-disjoint, seeded, NO
    training split; leakage audit (no pixel shared across splits). TEST sealed (VAL §3, §7)."""
    import astropy.units as u
    import numpy as np
    from astropy_healpix import HEALPix

    sp = cfg["split"]
    if sp.get("scheme") != "healpix":
        raise NotImplementedError(f"split scheme {sp.get('scheme')!r} not implemented; use 'healpix'.")
    if sp.get("training_split", False):
        raise ValueError("training_split must be false (untrained detector).")
    nside = int(sp["healpix_nside"])
    targets = targets.copy()
    hp = HEALPix(nside=nside)
    targets["healpix"] = hp.lonlat_to_healpix(
        targets["ra"].to_numpy() * u.deg, targets["dec"].to_numpy() * u.deg
    )

    # Assign WHOLE pixels to calibration (in seeded-random pixel order) until ~cal_fraction
    # of targets is reached; remaining pixels -> test. Whole-pixel assignment => no sky
    # block, and therefore no shared instrumental systematic, bridges the two splits.
    rng = np.random.default_rng(int(sp["rng_seed"]))
    pix_counts = targets.groupby("healpix").size()
    pixels = pix_counts.index.to_numpy()
    pixels = pixels[rng.permutation(len(pixels))]
    cal_target = float(sp["calibration_fraction"]) * len(targets)
    cal_pix, running = set(), 0
    for p in pixels:
        if running >= cal_target:
            break
        cal_pix.add(int(p))
        running += int(pix_counts[p])
    targets["split"] = np.where(targets["healpix"].isin(cal_pix), "calibration", "test")

    cal_px = set(targets.loc[targets["split"] == "calibration", "healpix"])
    test_px = set(targets.loc[targets["split"] == "test", "healpix"])
    overlap = cal_px & test_px
    if overlap:
        raise AssertionError(f"leakage audit FAILED: {len(overlap)} pixels in both splits.")

    prov = {
        "split_scheme": "healpix", "healpix_nside": nside, "rng_seed": int(sp["rng_seed"]),
        "training_split": False,
        "calibration_n": int((targets["split"] == "calibration").sum()),
        "test_n": int((targets["split"] == "test").sum()),
        "achieved_calibration_fraction": float((targets["split"] == "calibration").mean()),
        "n_pixels_calibration": len(cal_px), "n_pixels_test": len(test_px),
        "pixel_overlap": len(overlap),
    }
    print(
        f"[M0.4] split: calibration={prov['calibration_n']} test={prov['test_n']} "
        f"(cal frac {prov['achieved_calibration_fraction']:.3f}); "
        f"pixel overlap={len(overlap)} (leakage audit PASS)"
    )
    return targets, prov


def m0_5_feasibility_check(cfg: dict[str, Any], targets: Any) -> tuple[Any, Any]:
    """M0.5 — eligible-host coverage per period node. n_transits>=2 eligibility depends
    on P and observed baseline only (R_p sets depth, not transit count), so a host is
    eligible for every (P,R_p) cell at a given P. Uses baselines only — NO detection
    statistic on TEST (plan G1). Span-based estimate (optimistic envelope); M1 refines
    with actual cadence coverage."""
    import numpy as np
    import pandas as pd

    grid = cfg["injection_grid_reference"]
    periods = grid["period_days"]
    min_inj = int(grid["min_injections_per_cell"])
    nmin = int(grid["headline_requires_n_transits_ge"])

    rows = []
    for P in periods:
        ntr = np.floor(targets["baseline_days"] / float(P))
        elig = ntr >= nmin
        for split in ("calibration", "test"):
            hosts = int((elig & (targets["split"] == split)).sum())
            rows.append({"period_days": P, "split": split, "eligible_hosts": hosts})
    feas = pd.DataFrame(rows)

    pivot = feas.pivot(index="period_days", columns="split", values="eligible_hosts")
    test_hosts = pivot["test"]
    at_risk = [P for P in periods if test_hosts[P] < min_inj]
    print("[M0.5] eligible hosts (n_transits>=2) per period node:")
    print(pivot.to_string())
    if at_risk:
        print(
            f"[M0.5] AT-RISK periods (test hosts < {min_inj}/cell): {at_risk} "
            f"-> §6 contingency or widen sector block (R0-5)"
        )
    else:
        print(f"[M0.5] OK — every period has >= {min_inj} eligible test hosts.")
    return targets, feas


def m0_6_seal_manifest(
    cfg: dict[str, Any], sectors: dict[str, Any], targets: Any, feasibility: Any,
    provenance: dict[str, Any],
) -> str:
    """M0.6 — assemble the frozen manifest (Table T1) + provenance, compute the
    deterministic SHA-256 over a canonical manifest serialization (Seal #1), and emit
    the TEST-set access rule. Returns the hash to record in the plan + log (VAL §7, A.10)."""
    import datetime
    import hashlib
    import json
    import subprocess
    import sys
    from pathlib import Path

    outdir = Path(cfg["output"]["manifest_dir"])
    outdir.mkdir(parents=True, exist_ok=True)

    cols = [
        "tic", "sectors", "n_sectors", "ra", "dec", "baseline_days", "Tmag", "Teff",
        "logg", "rad", "contratio", "is_known_planet", "is_known_fp", "is_multiplanet",
        "healpix", "split",
    ]
    cols = [c for c in cols if c in targets.columns]
    man = targets[cols].copy()
    man["sectors"] = man["sectors"].apply(lambda s: ",".join(map(str, s)) if isinstance(s, (list, tuple)) else s)
    man = man.sort_values("tic").reset_index(drop=True)

    # Deterministic content hash = SHA-256 of canonical CSV (sorted, fixed cols/format).
    csv_bytes = man.to_csv(index=False, float_format="%.6f").encode()
    manifest_hash = hashlib.sha256(csv_bytes).hexdigest()

    freeze = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True
    ).stdout
    (outdir / "pip-freeze.lock").write_text(freeze)
    config_bytes = Path(cfg.get("_config_path", "research/m0_manifest/config/m0_config.yaml")).read_bytes()

    prov = {
        "milestone": "M0",
        "seal": "Seal #1 (manifest content hash)",
        "manifest_sha256": manifest_hash,
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "sealed_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sectors": sectors,
        "n_targets": int(len(man)),
        "split_counts": {
            "calibration": int((man["split"] == "calibration").sum()),
            "test": int((man["split"] == "test").sum()),
        },
        "python": sys.version.split()[0],
        "feasibility": feasibility.to_dict(orient="records"),
        "test_set_access_rule": (
            "TEST rows are read for the first and only time at M4 (single sealed run). "
            "No detection statistic is computed on TEST before M4 (plan G1)."
        ),
        "note": (
            "Seal #1 = manifest_sha256 (who/what data). Calibration-derived THRESHOLDS "
            "are sealed separately at M3 (Seal #2; VAL A.10). No thresholds in M0."
        ),
        **provenance,
    }
    (outdir / "m0_manifest_provenance.json").write_text(json.dumps(prov, indent=2, default=str))
    man.to_parquet(outdir / "m0_manifest.parquet")

    print(f"[M0.6] Seal #1 manifest SHA-256: {manifest_hash}")
    print(f"[M0.6] provenance -> {outdir}/m0_manifest_provenance.json (tracked)")
    print(f"[M0.6] manifest   -> {outdir}/m0_manifest.parquet ({len(man)} targets; gitignored)")
    return manifest_hash


def run(config_path: str, limit: int | None = None) -> None:
    cfg = load_config(config_path)
    cfg["_config_path"] = config_path
    sectors = m0_1_freeze_sectors(cfg)
    targets = m0_2_build_target_manifest(cfg, sectors, limit=limit)
    targets, label_prov = m0_3_assemble_labels(cfg, targets)
    targets, split_prov = m0_4_leakage_safe_split(cfg, targets)
    targets, feasibility = m0_5_feasibility_check(cfg, targets)
    seal = m0_6_seal_manifest(cfg, sectors, targets, feasibility, {**label_prov, **split_prov})
    print(f"\nM0 complete. Seal #1 (manifest SHA-256): {seal}")


def main() -> None:
    p = argparse.ArgumentParser(description="M0 manifest pipeline (Phase I).")
    p.add_argument(
        "--config",
        default=str(Path(__file__).parent / "config" / "m0_config.yaml"),
        help="Path to the signed-off frozen-choices config.",
    )
    p.add_argument("--limit", type=int, default=None, help="Cap target count for a smoke test.")
    args = p.parse_args()
    run(args.config, limit=args.limit)


if __name__ == "__main__":
    main()
