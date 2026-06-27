"""BAH2026 PS7 prototype — fetch + condition raw TESS light curves from MAST.

Satisfies the PS7 data requirement: download a sector's HIGH-CADENCE (SPOC 2-min)
light curves from MAST and condition them, rather than reusing any cache.

Recipe mirrors the sealed Phase-I M1 conditioning (research/m1_conditioning):
SPOC 2-min PDCSAP -> per-sector wotan biweight detrend (2.5 d) -> zero-centred
residual r(t). Output npz matches data/processed/m1 format
({time, resid, sectors, window}) so it flows straight into features.py / smoke_test.py.

Usage:
  # sample by TIC id(s), optional --sector filter:
  .venv/bin/python hackathon/prototype/fetch_tess.py --tics 100029948 261136679 --sector 2
  # by a TIC-list file (one id per line) -- for scaling toward a full sector:
  .venv/bin/python hackathon/prototype/fetch_tess.py --tic-file tics.txt --sector 1

For the full ~20-30k-star sector, the scalable path is the MAST bulk-download
wget scripts (one per sector) + this conditioning step in batch; this utility is
the per-target building block and the smoke-test of the ingestion path.
"""
from __future__ import annotations

import argparse
import os

import numpy as np

HERE = os.path.dirname(__file__)
CACHE = os.path.join(HERE, "cache")
os.makedirs(CACHE, exist_ok=True)

WINDOW_DAYS = 2.5          # finalized Phase-I detrend window
QUALITY_BITMASK = "default"


def fetch_condition(tic: int, sector: int | None = None):
    """Download SPOC 2-min PDCSAP for one TIC, biweight-detrend -> (time, resid, sectors)."""
    import lightkurve as lk
    from wotan import flatten

    sr = lk.search_lightcurve(f"TIC {tic}", mission="TESS", author="SPOC", exptime=120)
    if len(sr) == 0:
        raise RuntimeError("no SPOC 2-min products")
    if sector is not None:
        keep = [i for i, m in enumerate(sr.table["mission"]) if f"Sector {sector:02d}" in str(m)]
        if not keep:
            raise RuntimeError(f"no SPOC 2-min in sector {sector}")
        sr = sr[keep]

    times, resids, sectors = [], [], []
    for i in range(len(sr)):
        lc = sr[int(i)].download(quality_bitmask=QUALITY_BITMASK)
        if lc is None:
            continue
        t = np.asarray(lc.time.value, float)
        f = np.asarray(lc.flux.value, float)
        good = np.isfinite(t) & np.isfinite(f)
        t, f = t[good], f[good]
        if t.size < 100:
            continue
        f = f / np.median(f)                       # normalize to ~1
        flat, _ = flatten(t, f, window_length=WINDOW_DAYS, method="biweight", return_trend=True)
        r = flat - 1.0                             # zero-centred residual
        good = np.isfinite(r)
        times.append(t[good]); resids.append(r[good])
        sec = int(str(lc.meta.get("SECTOR", sector or -1)))
        sectors.append(sec)

    if not times:
        raise RuntimeError("nothing downloaded/conditioned")
    order = np.argsort(np.concatenate(times))
    time = np.concatenate(times)[order]
    resid = np.concatenate(resids)[order]
    return time, resid, np.array(sorted(set(sectors)), dtype=int)


def save(tic, time, resid, sectors):
    out = os.path.join(CACHE, f"{tic}.npz")
    np.savez(out, time=time, resid=resid, sectors=sectors, window=np.float64(WINDOW_DAYS))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tics", nargs="*", type=int, default=[])
    ap.add_argument("--tic-file")
    ap.add_argument("--sector", type=int, default=None)
    args = ap.parse_args()

    tics = list(args.tics)
    if args.tic_file:
        with open(args.tic_file) as fh:
            tics += [int(x) for x in fh.read().split() if x.strip().isdigit()]
    if not tics:
        ap.error("provide --tics or --tic-file")

    ok = 0
    for tic in tics:
        try:
            time, resid, sectors = fetch_condition(tic, args.sector)
            out = save(tic, time, resid, sectors)
            print(f"  TIC {tic}: {time.size:6d} cadences, sectors {list(sectors)} -> {out}")
            ok += 1
        except Exception as e:
            print(f"  TIC {tic}: FAILED ({type(e).__name__}: {e})")
    print(f"Done: {ok}/{len(tics)} conditioned into {CACHE}")


if __name__ == "__main__":
    main()
