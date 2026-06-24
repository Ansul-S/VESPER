"""Arm-B transit likelihood-ratio confirmer (v3) — CALIBRATION-only.

Implements TRANSIT_LR_CONFIRMER_SPEC.md (owner-locked 2026-06-19):
  D-1a  depth-only LINEAR likelihood-ratio (nu=1): template SHAPE fixed from the
        seed (T14) + stellar density; only depth delta is fitted (analytic GLS).
  D-2a  GP marginal likelihood (per-star Matern-3/2 kernel, correlation length tau)
        as the statistic-of-record; whitened OLS (D-2b) admitted ONLY if validated
        equal to the GP null FAR (transit_lr_whitened, for the equivalence study).
  D-3 i no t0 refinement for the headline statistic (pure fixed-ephemeris LR).

At the FIXED evidence ephemeris (P_hat, t0_hat, T14) on conditioned residuals r(t):
  y := -r        (dimming positive; sign-aware)
  m := unit-depth limb-darkened transit template (batman), shape from (P,T14,stellar)
  GLS:  delta_hat = (m^T K^-1 y) / (m^T K^-1 m),  Lambda = delta_hat^2 * (m^T K^-1 m)
        Lambda := 0 if delta_hat <= 0   (sign-aware rejection)
  K is the per-star covariance (Matern-3/2 red term + white diag) via celerite2.
  No period grid, no phase search -> range-invariant (the Finding-B fix).

Confirm iff Lambda >= T_red AND sign_pass AND shape_pass(odd/even + no secondary).
Look-elsewhere is handled UPSTREAM by the period-FAP gate (A.8/A.8a); this is a
single fixed-ephemeris test -> no additional LEE.  NO TEST. NO seal change.
"""
from __future__ import annotations

import numpy as np

try:
    import batman
    _HAVE_BATMAN = True
except Exception:  # pragma: no cover
    _HAVE_BATMAN = False

import celerite2
from celerite2 import terms


# ----------------------------------------------------------------------------- template
def unit_transit_template(t, P, t0, T14, stellar):
    """Unit-depth limb-darkened transit shape m(t) in [0,1] (1 at mid-transit).

    Shape fixed by (P, T14) + stellar limb-darkening (D-1a): b=0 (central), a/Rs from
    the seed duration  a/Rs = P / (pi * T14).  Depth is NOT in the template (fitted).
    """
    T14 = float(max(T14, 1e-3))
    if not _HAVE_BATMAN:
        # trapezoid fallback (ingress = 10% of T14) if batman unavailable
        phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
        x = np.abs(phase)
        tau = 0.1 * T14
        m = np.clip((0.5 * T14 + tau - x) / max(tau, 1e-6), 0.0, 1.0)
        m[x <= 0.5 * T14 - tau] = 1.0
        m[x >= 0.5 * T14 + tau] = 0.0
        return m
    aRs = max(P / (np.pi * T14), 2.0)
    u1, u2 = stellar.get("u1", 0.4), stellar.get("u2", 0.25)
    pm = batman.TransitParams()
    pm.t0, pm.per, pm.rp, pm.a = t0, P, 0.05, aRs
    pm.inc, pm.ecc, pm.w = 90.0, 0.0, 90.0
    pm.u, pm.limb_dark = [u1, u2], "quadratic"
    flux = batman.TransitModel(pm, np.ascontiguousarray(t)).light_curve(pm)
    dip = 1.0 - flux
    mx = float(dip.max())
    return dip / mx if mx > 0 else dip


# ----------------------------------------------------------------------------- noise model
def estimate_kernel(t, r, intr):
    """Per-star (sigma_white, sigma_red, tau_days) from OUT-of-transit residuals.

    tau = acf e-folding time (M1-consistent); sigma_red from lag-1 autocorrelation,
    sigma_white the remainder.  Robust (MAD) scale.  Returns conservative floors.
    """
    out = r[~intr]
    if out.size < 50:
        out = r
    sig = 1.4826 * np.median(np.abs(out - np.median(out)))
    sig = float(sig) if np.isfinite(sig) and sig > 0 else float(np.std(r) + 1e-9)
    cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
    x = out - np.mean(out)
    denom = float(np.dot(x, x)) + 1e-30
    acf1 = float(np.dot(x[:-1], x[1:]) / denom) if x.size > 2 else 0.0
    acf1 = min(max(acf1, 0.0), 0.95)
    tau = max(cad / max(-np.log(acf1 + 1e-6), 1e-3), 2.0 * cad) if acf1 > 0 else 2.0 * cad
    sig_red = sig * np.sqrt(acf1)
    sig_white = sig * np.sqrt(max(1.0 - acf1, 1e-3))
    return float(sig_white), float(sig_red), float(tau)


def _gp_solve(t, diag, sig_red, tau, *vecs):
    """Return K^-1 @ each vec, with K = Matern32(sigma_red, tau) + diag(white^2)."""
    rho = float(max(tau, 1e-4))
    kernel = terms.Matern32Term(sigma=float(max(sig_red, 1e-9)), rho=rho)
    gp = celerite2.GaussianProcess(kernel, mean=0.0)
    gp.compute(t, diag=diag, quiet=True)
    return [gp.apply_inverse(np.ascontiguousarray(v)) for v in vecs]


# ----------------------------------------------------------------------------- LR statistics
def transit_lr_gp(t, r, P, t0, T14, stellar):
    """D-2a GP marginal-likelihood depth-only LR.  Returns (Lambda, delta, n_in)."""
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    nin = int(intr.sum())
    if nin < 3:
        return 0.0, 0.0, nin
    m = unit_transit_template(t, P, t0, T14, stellar)
    if m.max() <= 0:
        return 0.0, 0.0, nin
    y = -r  # dimming positive
    sw, sr, tau = estimate_kernel(t, r, intr)
    diag = np.full(t.shape, sw * sw, float)
    try:
        Kinv_y, Kinv_m = _gp_solve(t, diag, sr, tau, y, m)
    except Exception:
        return transit_lr_whitened(t, r, P, t0, T14, stellar)[:3]
    mKm = float(np.dot(m, Kinv_m))
    if not np.isfinite(mKm) or mKm <= 0:
        return 0.0, 0.0, nin
    delta = float(np.dot(m, Kinv_y) / mKm)
    if delta <= 0:                       # sign-aware rejection
        return 0.0, delta, nin
    lam = float(delta * delta * mKm)     # = chi^2_1 LR improvement
    return lam, delta, nin


def transit_lr_whitened(t, r, P, t0, T14, stellar):
    """D-2b whitened OLS depth-only LR (validation fallback only).  (Lambda, delta, n_in)."""
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    nin = int(intr.sum())
    if nin < 3:
        return 0.0, 0.0, nin
    m = unit_transit_template(t, P, t0, T14, stellar)
    sw, _, _ = estimate_kernel(t, r, intr)
    if sw <= 0 or m.max() <= 0:
        return 0.0, 0.0, nin
    y = -r
    mm = float(np.dot(m, m))
    if mm <= 0:
        return 0.0, 0.0, nin
    delta = float(np.dot(m, y) / mm)
    if delta <= 0:
        return 0.0, delta, nin
    lam = float((delta * delta * mm) / (sw * sw))
    return lam, delta, nin


# ----------------------------------------------------------------------------- vetting
def odd_even_consistent(t, r, P, t0, T14, stellar, k_sigma=3.0):
    """Odd vs even transit depth consistency (EB rejection).  True if consistent."""
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    if intr.sum() < 6:
        return True  # too few to test -> do not reject on this basis
    epoch = np.round((t - t0) / P)
    depths = {}
    for parity in (0, 1):
        sel = intr & (np.mod(epoch, 2) == parity)
        if sel.sum() >= 3:
            depths[parity] = (-float(r[sel].mean()), float(r[sel].std() / np.sqrt(sel.sum()) + 1e-9))
    if len(depths) < 2:
        return True
    (d0, e0), (d1, e1) = depths[0], depths[1]
    return abs(d0 - d1) <= k_sigma * np.sqrt(e0 * e0 + e1 * e1)


def no_secondary(t, r, P, t0, T14, stellar, k_sigma=3.0):
    """No significant secondary eclipse at phase 0.5 (EB rejection).  True if clean."""
    lam_sec, depth_sec, nin = transit_lr_gp(t, r, P, t0 + 0.5 * P, T14, stellar)
    # a secondary as deep/significant as a primary-scale dimming -> reject
    return not (lam_sec >= 25.0 and depth_sec > 0)   # ~5 sigma secondary


def n_transits(t, P, t0, T14):
    phase = ((t - t0 + 0.5 * P) % P) - 0.5 * P
    intr = np.abs(phase) <= 0.5 * max(T14, 1e-3)
    if intr.sum() == 0:
        return 0
    return int(np.unique(np.round((t[intr] - t0) / P)).size)


# ----------------------------------------------------------------------------- top-level
def confirm(t, r, eph, stellar, T_red):
    """Full Arm-B confirmation at the fixed seed eph=(P,t0,T14).  dict.

    confirmed = (Lambda >= T_red) and sign_pass and shape_pass.
    """
    P, t0, T14 = float(eph[0]), float(eph[1]), float(eph[2])
    lam, delta, nin = transit_lr_gp(t, r, P, t0, T14, stellar)
    ntr = n_transits(t, P, t0, T14)
    sign_pass = delta > 0
    # shape vetting only meaningful with repetition (N_tr >= 2); monotransit -> MATH 6 (weaker, headline-excluded)
    if ntr >= 2:
        shape_pass = odd_even_consistent(t, r, P, t0, T14, stellar) and no_secondary(t, r, P, t0, T14, stellar)
    else:
        shape_pass = no_secondary(t, r, P, t0, T14, stellar)
    confirmed = bool(lam >= float(T_red) and sign_pass and shape_pass)
    return {"Lambda": lam, "delta": delta, "n_in": nin, "n_transits": ntr,
            "sign_pass": bool(sign_pass), "shape_pass": bool(shape_pass), "confirmed": confirmed}


# ----------------------------------------------------------------------------- smoke test
if __name__ == "__main__":
    import sys, glob
    from pathlib import Path
    HERE = Path(__file__).parent
    sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "m3_calibration"))
    import injection as INJ
    import pandas as pd

    rng = np.random.default_rng(20260619)
    man = pd.read_parquet("data/manifests/m0/m0_manifest.parquet"); man["tic"] = man["tic"].astype(str)
    man = man[man.split == "calibration"]
    ld = INJ.constant_ld()
    files = sorted(glob.glob("data/processed/m1/*.npz"))[:6]
    print("=== confirmer.py smoke test (CALIBRATION npz; no TEST) ===")
    for f in files:
        tic = Path(f).stem
        row = man[man.tic == tic]
        if row.empty:
            continue
        row = row.iloc[0]
        z = np.load(f); t = np.asarray(z["time"], float); r0 = np.asarray(z["resid"], float)
        if r0.size < 1000:
            continue
        stellar = {"u1": 0.4, "u2": 0.25}
        # NULL (no injection)
        P, t0 = 3.0, float(t.min() + 1.0); T14 = 0.12
        lam_null, d_null, _ = transit_lr_gp(t, r0, P, t0, T14, stellar)
        # STRONG injection at the same ephemeris
        built = INJ.build_injection(t, P, 4, 0.0, row, ld, rng, host_mode="cached_residual", r_host=r0)
        if built is None:
            print(f"  {tic}: null Lambda={lam_null:7.2f}  (injection build failed)")
            continue
        _, r_inj, truth = built
        eph = (truth["P_true"], truth["t0_true"], truth["t14_true"])
        c = confirm(t, r_inj, eph, stellar, T_red=0.0)
        print(f"  {tic}: NULL Lambda={lam_null:7.2f} (delta={d_null:+.4f})  |  "
              f"R=4 INJ Lambda={c['Lambda']:8.2f} delta={c['delta']:+.4f} "
              f"n_tr={c['n_transits']} sign={c['sign_pass']} shape={c['shape_pass']}")
    print("done.")
