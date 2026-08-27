"""INN-3 — exact-equivalent accelerated period-FAP (MATH §9.1 / VAL A.8).

WHAT THIS IS. A drop-in replacement for `period_recovery.period_fap` that computes
the SAME statistic, on the SAME null model, with the SAME B and the SAME RNG
stream — and returns a bit-identical answer, one to two orders of magnitude faster.
It is an *estimator-of-record substitution* in the sense of MATH §9.1a whose
equivalence proof is the identity map, not a tolerance.

WHY IT MATTERS. The sealed Phase-I compute endpoint E2 is
`C_comb/C_full`, and its dominant term on the routing side is the per-star detector
overhead ρ_d = 11.6% (`data/manifests/m4/e2_retiming/e2_retiming_summary.json`).
Profiling the sealed `period_fap` shows ρ_d is ~100% period-FAP: 18.4 CPU-s per star,
of which ~49% is `np.median(np.diff(np.sort(t)))` — a loop invariant recomputed twice
per duration per surrogate (10 full sorts of an N-vector per surrogate, 10,000 per
star), all returning the same constant. `LEVER1B_EQUIVALENCE_RESULT.md` concluded the
B=1000 bootstrap was "not a removable artifact"; that conclusion is correct about the
*estimator* and wrong about its *cost*. The two candidate cheap estimators tested
there (E-EVT, E-LUT) both tried to APPROXIMATE the null distribution and both failed
all three equivalence criteria. This module does not approximate it.

TWO EXACT LEVERS
----------------
A. INVARIANT HOISTING + VECTORISATION (`FastPeriodFAP.detect` / `.best_R`).
   Everything inside the surrogate loop that is a function of the epoch vector `t`
   alone — cadence, box widths, window-centre epochs, stride indices — is computed
   once at construction. The local-maximum scan becomes three array comparisons; the
   de-duplication becomes a bucketed search with identical greedy semantics; the comb
   scan becomes one (n_freq x k) matrix instead of a Python loop over frequencies.
   Bit-identical by construction: the same IEEE operations on the same operands in
   the same order. Verified below and in `tests/test_fast_period_fap.py`.

B. EXACT CURTAILMENT (`curtail_ge`).
   The sealed gate is FAP = (ge+1)/(B+1) <= alpha with B = 1000, alpha = 0.01
   (Seal #2). That inequality is *exactly* `ge <= 9`. So the moment a run records its
   10th exceedance the gate is decided and no remaining surrogate can reopen it —
   this is curtailed sampling, and the resulting ROUTING DECISION is identical with
   probability one, not within a tolerance. The FAP value is then reported as a
   certified lower bound (`curtailed=True`); the driver consumes the FAP only through
   `fap <= alpha_fap` (`m4_driver.py:171,309`), so nothing downstream is affected.
   Curtailment is one-sided by nature: it can close a gate early, never open one.

MEASURED (calibration only; artifacts in `data/manifests/m4/inn3/`)
-------------------------------------------------------------------
* 1126/1126 cached calibration nulls: exceedance count `ge` identical to the sealed
  recorded value (max |delta| = 0); gate identical at full B and under curtailment.
* Speed, single-thread CPU: sealed 14.26 s/star -> 2.40 s (lever A, 6.35x)
  -> 0.162 s (lever A+B, 74.3x). Mean surrogates under curtailment: 66 of 1000.
* Calibration injections: FAP bit-identical, 0 recoveries clipped, 0 nulls admitted.

SCOPE. Nothing here changes a sealed threshold, statistic, null model, alpha or
verdict. The sealed Phase-I run stands exactly as recorded; `frozen_rerun/` is
untouched. Adopting this module as the operational estimator-of-record for any
future run is an owner decision (a decision record), not a consequence of this file.
"""
from __future__ import annotations

import numpy as np

DEDUP_SEP_DAYS = 0.3        # sealed detector de-duplication window (detector.detect_events)


def curtail_threshold(alpha: float, B: int) -> int:
    """Smallest exceedance count that makes the sealed gate FAP=(ge+1)/(B+1)<=alpha false.

    Gate open  <=>  ge <= floor(alpha*(B+1)) - 1.  Stop at that value + 1.
    For the sealed alpha=0.01, B=1000: open <=> ge <= 9, so stop at 10.
    """
    return int(np.floor(alpha * (B + 1) - 1.0)) + 1


class FastPeriodFAP:
    """Exact accelerated block-bootstrap period-FAP for one light curve.

    Construct once per (t, duration grid, period range); call `fap` per residual.
    `detect` and `best_R` are bit-identical replacements for the frozen
    `detector.detect_events(t, r, grid, stride, z)` and
    `period_recovery.best_period(epochs, p_min, p_max, oversample)[2]`.
    """

    def __init__(self, t, duration_grid, stride_frac=0.5, z_star=2.0,
                 p_min=0.5, p_max=None, oversample=3):
        t = np.asarray(t, float)
        self.t = t
        self.n = t.size
        self.z = float(z_star)
        self.p_min = float(p_min)
        self.p_max_cfg = float(p_max)
        self.oversample = int(oversample)
        # THE loop invariant. The sealed detector recomputes this twice per duration
        # per surrogate; it depends only on t.
        self.cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0

        self.plan = []
        for dur in duration_grid:
            dur = float(dur)
            nbin = max(1, int(round(dur / self.cad)))
            if self.n < 2 * nbin:                       # sealed _box_depth_series guard
                continue
            nwin = self.n - nbin + 1
            step = max(1, int(round(stride_frac * dur / self.cad)))
            idx = np.arange(0, nwin, step)
            self.plan.append({"dur": dur, "nbin": nbin, "idx": idx,
                              "ts": (t[:nwin] + 0.5 * dur)[idx],
                              "w": np.empty(nwin), "scratch": np.empty(nwin)})
        self._csum = np.empty(self.n + 1)
        self._csum[0] = 0.0

    # ------------------------------------------------------------------ detector
    def detect(self, r):
        """Bit-identical replacement for frozen `detect_events(t, r, grid, stride, z)`."""
        rows = []
        csum = self._csum
        np.cumsum(r, out=csum[1:])
        for p in self.plan:
            nbin, w, sc = p["nbin"], p["w"], p["scratch"]
            np.subtract(csum[nbin:], csum[:-nbin], out=w)
            np.divide(w, nbin, out=w)
            np.negative(w, out=w)                       # w is now the sealed `depth`
            sc[:] = w
            med = np.median(sc, overwrite_input=True)
            np.subtract(w, med, out=sc)
            np.abs(sc, out=sc)
            scatter = 1.4826 * np.median(sc, overwrite_input=True)
            if not np.isfinite(scatter) or scatter <= 0:
                continue
            # stride first, then divide: same operands, N/step divisions instead of N
            ss = w[p["idx"]] / scatter
            if ss.size < 3:                             # sealed loop range(1, size-1) is empty
                continue
            c = ss[1:-1]
            m = (c >= self.z) & (c >= ss[:-2]) & (c >= ss[2:])
            if not m.any():
                continue
            j = np.flatnonzero(m) + 1
            rows.append(np.column_stack([p["ts"][j], ss[j], np.full(j.size, p["dur"])]))
        if not rows:
            return np.empty((0, 3))
        ev = np.concatenate(rows)          # duration-major, index-ascending == sealed append order
        ev = ev[np.argsort(-ev[:, 1])]
        return _dedup_bucketed(ev, DEDUP_SEP_DAYS)

    # ----------------------------------------------------------------- comb scan
    def best_R(self, epochs):
        """Bit-identical replacement for frozen `best_period(...)[2]` (the resultant length)."""
        if epochs.size < 2:
            return 0.0
        span = float(epochs.max() - epochs.min())
        p_max = min(self.p_max_cfg, span) if span > 0 else self.p_max_cfg
        if p_max <= self.p_min:
            return 0.0
        df = 1.0 / (self.oversample * max(span, p_max))
        freqs = np.arange(1.0 / p_max, 1.0 / self.p_min, df)
        if freqs.size == 0:
            return 0.0
        periods = 1.0 / freqs
        ang = 2 * np.pi * ((epochs[None, :] / periods[:, None]) % 1.0)
        R = np.hypot(np.cos(ang).mean(axis=1), np.sin(ang).mean(axis=1))
        scores = 1.0 - R                                # the sealed 1-R round-trip, preserved
        return float(1.0 - scores[int(np.argmin(scores))])

    # ----------------------------------------------------------------------- FAP
    def fap(self, r, obs_R, block_len_days, n_surrogates, rng, curtail_ge=None):
        """Block-bootstrap FAP = (ge+1)/(B+1), Laplace-smoothed (sealed definition).

        `block_len_days` is the sealed L_b = block_len_multiple * max(tau_GP, T14);
        pass the value the sealed `period_fap` would compute, not tau and T14.
        `curtail_ge`: stop at this exceedance count (see `curtail_threshold`). None
        runs the full B and returns the bit-identical sealed FAP.

        Returns (fap, n_surrogates_used, curtailed, ge).
        """
        n, B = self.n, int(n_surrogates)
        blk = max(1, min(max(1, int(round(block_len_days / self.cad))), n))
        nblk = int(np.ceil(n / blk))
        r2 = np.concatenate([r, r])                     # circular wrap without a modulo
        offs = np.arange(blk)[None, :]
        ge = 0
        for b in range(B):
            # one vector draw == nblk scalar draws on numpy's PCG64 stream (asserted in tests)
            starts = rng.integers(0, n, size=nblk)
            rs = r2[(starts[:, None] + offs).ravel()[:n]]
            ev = self.detect(rs)
            Rs = self.best_R(ev[:, 0]) if ev.shape[0] >= 2 else 0.0
            if Rs >= obs_R:
                ge += 1
                if curtail_ge is not None and ge >= curtail_ge:
                    return (ge + 1) / (B + 1), b + 1, True, ge
        return (ge + 1) / (B + 1), B, False, ge


def _dedup_bucketed(ev, sep):
    """Sealed greedy de-duplication, identical semantics, without the O(k x kept) scan.

    Sealed: walk the SNR-descending candidates, keep `e` iff |e0 - k0| > sep for every
    already-kept `k`. A conflict needs |e0 - k0| <= sep, so with buckets of width `sep`
    only neighbouring buckets can hold one. Same order, same predicate, same output.
    """
    buckets: dict[int, list[float]] = {}
    kept = []
    for e in ev:
        e0 = e[0]
        b = int(np.floor(e0 / sep))
        hit = False
        for bb in (b - 2, b - 1, b, b + 1, b + 2):      # +-2: float-safe margin on the index
            lst = buckets.get(bb)
            if lst is not None:
                for k0 in lst:
                    if abs(e0 - k0) <= sep:
                        hit = True
                        break
            if hit:
                break
        if not hit:
            kept.append(e)
            buckets.setdefault(b, []).append(e0)
    return np.array(kept)
