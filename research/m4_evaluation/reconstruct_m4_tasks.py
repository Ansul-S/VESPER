"""Deterministic reconstruction of the sealed M4 TEST task list (audit remediation, DR-003).

The sealed TEST run (2026-06-24) built its 15,000 injection tasks from pure arithmetic
on frozen seeds (m4_driver.py): host draw = pool.sample(80, random_state=22); task
(cell c, index j) -> tic = hosts[(2j + 500c) % 80], b = GRID_B[j % 3],
injection seed = 20260619 + 500c + j. This script rebuilds that exact task list,
re-derives per-task routing eligibility by re-running the FROZEN detector on the
reconstructed injections, and validates the reconstruction against the sealed
`data/manifests/m4/test_run/recovery.csv` (per-cell host multisets + routed counts).

It also computes the OBSERVED transit count per injection (distinct epochs with >=1
in-transit cadence in the actual time array) to quantify the audit finding that the
sealed n_transits = floor(baseline/P)+1 formula ignores gaps and epoch.

Reads NO new TEST information: the hosts and injections reconstructed here are the
ones already read in the single sealed evaluation (P-5 argument in DR-003).

Run:  .venv/bin/python research/m4_evaluation/reconstruct_m4_tasks.py [--workers 8]
Out:  data/manifests/m4/e2_retiming/task_reconstruction.csv + reconstruction_validation.json
"""
from __future__ import annotations

import argparse, json, sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
# FROZEN module snapshot first on sys.path (sealed code path, immune to later fixes)
sys.path.insert(0, str(HERE / "frozen_rerun"))
sys.path.insert(0, str(HERE.parent / "m2_injection"))

import injection as INJ            # noqa: E402  (frozen copy)
import seal_loader as SL           # noqa: E402  (frozen copy)
from detector import detect_events  # noqa: E402  (frozen copy)

CACHE = Path("data/processed/m1")
OUT = Path("data/manifests/m4/e2_retiming")
_FR = _MAN = _LD = None


def build_task_list():
    """Reproduce m4_driver.main()'s pool, host draw, and task arithmetic exactly."""
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet")
    man["tic"] = man["tic"].astype(str)
    avail = {p.stem for p in CACHE.glob("*.npz")}
    pool_df = man[(man.split == "test") & (man.rad > 0)
                  & np.isfinite(man.logg) & np.isfinite(man.Teff)].copy()
    pool_df = pool_df[pool_df.tic.isin(avail)]
    hosts = pool_df.sample(min(80, len(pool_df)), random_state=22).tic.tolist()
    cells = [(P, Rp) for P in INJ.GRID_P for Rp in INJ.GRID_R]
    tasks, sc = [], 0
    for c, (P, Rp) in enumerate(cells):
        for j in range(500):
            tic = hosts[(j + sc) % len(hosts)]
            bb = INJ.GRID_B[j % len(INJ.GRID_B)]
            tasks.append({"task": sc, "cell": c, "j": j, "tic": tic,
                          "period_days": P, "radius_rearth": Rp, "b": bb,
                          "seed": 20260619 + sc})
            sc += 1
    return pool_df.set_index("tic"), hosts, pd.DataFrame(tasks)


def _observed_n_transits(t, P, t0, t14):
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(t14, 1e-3)
    if not intr.any():
        return 0
    return int(np.unique(np.round((t[intr] - t0) / P)).size)


def _init(man_idx):
    global _FR, _MAN, _LD
    _FR, _MAN, _LD = SL.load_frozen(), man_idx, INJ.constant_ld()


_NPZ = {}


def _resid(tic):
    if tic not in _NPZ:
        z = np.load(CACHE / f"{tic}.npz")
        _NPZ[tic] = (np.asarray(z["time"], float), np.asarray(z["resid"], float))
    return _NPZ[tic]


def _worker(row):
    tic, P, Rp, b, seed = row["tic"], row["period_days"], row["radius_rearth"], row["b"], row["seed"]
    fr = _FR
    rng = np.random.default_rng(int(seed))
    t, r0 = _resid(tic)
    built = INJ.build_injection(t, P, Rp, b, _MAN.loc[tic], _LD, rng,
                                host_mode="cached_residual", r_host=r0)
    if built is None:
        return {**row, "built": False}
    _, r, truth = built
    ev = detect_events(t, r, fr.duration_grid, stride_frac=0.5, z_for_extraction=fr.z_star)
    n_ev = int(ev.shape[0])
    return {**row, "built": True, "n_events": n_ev, "routed": n_ev >= fr.n_min,
            "t0_true": truth["t0_true"], "t14_true": truth["t14_true"],
            "n_transits_formula": truth["n_transits"],
            "n_transits_observed": _observed_n_transits(t, P, truth["t0_true"], truth["t14_true"])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    from multiprocessing import Pool

    man_idx, hosts, tasks = build_task_list()
    OUT.mkdir(parents=True, exist_ok=True)
    used = sorted(tasks.tic.unique())
    print(f"[recon] 15,000 tasks rebuilt; drawn hosts {len(hosts)}; DISTINCT USED {len(used)} "
          f"(parity bug: stride-2 walk)")

    rec = pd.read_csv("data/manifests/m4/test_run/recovery.csv")
    rec["tic"] = rec["tic"].astype(str)
    v = {"hosts_drawn": len(hosts), "hosts_used_reconstructed": len(used),
         "hosts_used_sealed_csv": int(rec.tic.nunique()),
         "host_sets_match": set(used) == set(rec.tic.unique())}
    # per-cell host multiset check
    mism = 0
    for (P, Rp), grp in tasks.groupby(["period_days", "radius_rearth"]):
        s = rec[(rec.period_days == P) & (rec.radius_rearth == Rp)]
        if sorted(grp.tic.tolist()) != sorted(s.tic.tolist()):
            mism += 1
    v["cells_with_host_multiset_mismatch"] = mism
    print(f"[recon] host-set match: {v['host_sets_match']}; cell multiset mismatches: {mism}/30")

    rows = []
    with Pool(a.workers, initializer=_init, initargs=(man_idx,)) as pool:
        for i, x in enumerate(pool.imap_unordered(_worker, tasks.to_dict("records"),
                                                  chunksize=16), 1):
            rows.append(x)
            if i % 1500 == 0:
                print(f"[recon] {i}/15000 ...", flush=True)
    df = pd.DataFrame(rows).sort_values("task").reset_index(drop=True)
    df.to_csv(OUT / "task_reconstruction.csv", index=False)

    v["routed_frac_reconstructed"] = float(df.routed.mean())
    v["routed_frac_sealed_csv"] = float(rec.routed.mean())
    # per-cell routed-count agreement (routing is deterministic given the injection)
    rc = df.groupby(["period_days", "radius_rearth"]).routed.sum()
    rs = rec.groupby(["period_days", "radius_rearth"]).routed.sum()
    v["cells_with_routed_count_mismatch"] = int((rc != rs).sum())
    v["max_routed_count_abs_diff"] = int((rc - rs).abs().max())
    # observed-vs-formula transit count audit
    eligible_formula = df[df.n_transits_formula >= 2]
    v["n_formula_ge2"] = int(len(eligible_formula))
    v["n_formula_ge2_but_observed_le1"] = int((eligible_formula.n_transits_observed <= 1).sum())
    v["n_observed_lt_formula"] = int((df.n_transits_observed < df.n_transits_formula).sum())
    (OUT / "reconstruction_validation.json").write_text(json.dumps(v, indent=2))
    print(json.dumps(v, indent=2))


if __name__ == "__main__":
    main()
