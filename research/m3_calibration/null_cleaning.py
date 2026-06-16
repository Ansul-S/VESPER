"""M3 null-pool cleaning — catalog enrichment (Prša et al. 2022 TESS EB + VSX variables).

Per owner directive (2026-06-16): the M0 null definition is PRESERVED unchanged; this builds a
DERIVED M3 calibration subset by removing catalog-matched astrophysical contaminants (eclipsing
binaries, variables) that inflate T / z_mono / alpha_FAP. Every exclusion is logged with reason +
source in data/manifests/m3/calibration_exclusions.csv.

Catalogs:
  * Prša et al. (2022), ApJS 258, 16 — TESS EB catalog (Vizier J/ApJS/258/16), matched by TIC.
  * VSX — AAVSO Variable Star Index (Vizier B/vsx/vsx), matched by sky cone.

Run (host network):  python research/m3_calibration/null_cleaning.py [--radius-arcsec 15]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

REPORT = Path("data/manifests/m3")
PRSA_VIZIER = "J/ApJS/258/16"
VSX_VIZIER = "B/vsx/vsx"


def _prsa_eb_tics() -> set[str]:
    from astroquery.vizier import Vizier
    v = Vizier(row_limit=-1)
    cats = v.get_catalogs(PRSA_VIZIER)
    tics: set[str] = set()
    for tab in cats:
        col = next((c for c in tab.colnames if c.upper() in ("TIC", "TIC_ID", "TICID")), None)
        if col:
            for x in tab[col]:
                try:
                    tics.add(str(int(x)))
                except Exception:
                    pass
    return tics


def _vsx_matches(df: pd.DataFrame, radius_arcsec: float) -> dict[str, str]:
    """Cone-match each null star to VSX; return {tic: 'Name|Type'} for hits."""
    from astropy import units as u
    from astropy.coordinates import SkyCoord
    from astroquery.vizier import Vizier
    v = Vizier(row_limit=5, columns=["Name", "Type", "RAJ2000", "DEJ2000"])
    hits: dict[str, str] = {}
    for _, row in df.iterrows():
        c = SkyCoord(float(row["ra"]) * u.deg, float(row["dec"]) * u.deg)
        try:
            res = v.query_region(c, radius=radius_arcsec * u.arcsec, catalog=VSX_VIZIER)
        except Exception:
            res = None
        if res and len(res) and len(res[0]):
            t = res[0][0]
            hits[str(row["tic"])] = f"{t['Name']}|{t['Type']}"
    return hits


def _load_with_coords() -> pd.DataFrame:
    """Build the per-star table with coords from m3_per_star.csv + the M0 manifest (any sample size)."""
    d = pd.read_csv(REPORT / "m3_per_star.csv"); d["tic"] = d["tic"].astype(str)
    m = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); m["tic"] = m["tic"].astype(str)
    out = d.merge(m[["tic", "ra", "dec", "Tmag", "Teff", "rad"]], on="tic", how="left")
    out.to_csv(REPORT / "m3_per_star_coords.csv", index=False)
    return out


def run(radius_arcsec: float = 15.0) -> None:
    df = _load_with_coords()
    df["tic"] = df["tic"].astype(str)
    print(f"[clean] {len(df)} null stars loaded; {int((df['tls_sde']>9).sum())} have SDE>9")

    rows = []
    # --- Prša 2022 EB catalog (by TIC) ---
    try:
        eb = _prsa_eb_tics()
        print(f"[clean] Prša 2022 EB catalog: {len(eb)} TICs fetched")
        for tic in df["tic"]:
            if tic in eb:
                rows.append({"tic": tic, "reason": "eclipsing_binary",
                             "source": "Prsa2022_ApJS258_16", "detail": "TIC match"})
    except Exception as e:
        print(f"[clean] Prša fetch FAILED: {type(e).__name__}: {e}")

    # --- VSX variables (by cone) ---
    try:
        vsx = _vsx_matches(df, radius_arcsec)
        print(f"[clean] VSX variable matches: {len(vsx)} (radius {radius_arcsec}\")")
        for tic, name in vsx.items():
            rows.append({"tic": tic, "reason": "variable_star",
                         "source": "VSX_AAVSO", "detail": name})
    except Exception as e:
        print(f"[clean] VSX query FAILED: {type(e).__name__}: {e}")

    excl = pd.DataFrame(rows).drop_duplicates(subset=["tic", "source"])
    excl.to_csv(REPORT / "calibration_exclusions.csv", index=False)
    excl_tics = set(excl["tic"]) if len(excl) else set()
    cleaned = df[~df["tic"].isin(excl_tics)].copy()
    cleaned.to_csv(REPORT / "m3_null_cleaned_catalog.csv", index=False)

    print(f"\n[clean] catalog exclusions: {len(excl_tics)} stars "
          f"({len(rows)} catalog hits) -> cleaned null = {len(cleaned)}/{len(df)}")
    if len(excl):
        merged = excl.merge(df[["tic", "tls_sde", "max_event_snr"]], on="tic", how="left")
        print(merged.sort_values("tls_sde", ascending=False).to_string(index=False))
    print("\n[clean] residual high-SDE (>9) NOT caught by catalogs (-> automated vetting next):")
    resid = cleaned[cleaned["tls_sde"] > 9].sort_values("tls_sde", ascending=False)
    print(resid[["tic", "tls_sde", "max_event_snr", "n_events_ge2", "period_fap"]].to_string(index=False)
          if len(resid) else "  (none)")
    print(f"\n[clean] wrote calibration_exclusions.csv + m3_null_cleaned_catalog.csv")


def main() -> None:
    p = argparse.ArgumentParser(description="M3 null-pool catalog cleaning (Prsa 2022 + VSX).")
    p.add_argument("--radius-arcsec", type=float, default=15.0)
    args = p.parse_args()
    run(args.radius_arcsec)


if __name__ == "__main__":
    main()
