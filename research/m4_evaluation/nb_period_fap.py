"""INN-3 parity probe — period-FAP with the surrogate loop numba-compiled.

WHY THIS EXISTS. Arm A's baseline is `transitleastsquares`, a numba-JIT-compiled
package. Arm B's detector + period-FAP was interpreted numpy. A compute-ratio
endpoint measured in CPU seconds between a compiled baseline and an interpreted
challenger measures the two implementations, not the two algorithms. This module puts Arm B's inner loop at the same compilation standard as Arm A's, so the
residual ratio is attributable to the algorithms.

Statistically identical to the sealed estimator (same statistic, same null, same
B, same block bootstrap); NOT claimed bit-identical -- numba's median selection,
argsort tie order and libm cos/sin may differ from numpy's in the last ULP. The
agreement is therefore MEASURED against the sealed Lever-1b criteria, not asserted.

RESULT (see INN3_FAP_ACCELERATION.md §7.2): it reproduces the exceedance count g_e
exactly on the stars tested and is only 1.4-1.7x faster than the pure-numpy
`fast_period_fap`. That BOUNDS the implementation-fairness objection: after the
invariant hoisting of lever A, at most ~2x of Arm B's routing cost is attributable
to language choice. This module is a measurement instrument, NOT the recommended
estimator -- `fast_period_fap` is, because it is bit-identical.
"""
from __future__ import annotations
import numpy as np
from numba import njit


@njit(cache=True, fastmath=False)
def _surrogate_R(r2, n, starts, blk, csum, work, work2, nbins, idx_flat, idx_off, ts_flat, durs,
                 z, p_min, p_max_cfg, oversample, dedup_sep, obs_R):
    """One surrogate: block-bootstrap -> detect -> comb. Returns max comb R."""
    # --- circular block bootstrap (starts already drawn from the SAME rng stream) ---
    csum[0] = 0.0
    filled = 0
    b = 0
    acc = 0.0
    while filled < n:
        s = starts[b]
        take = blk
        if n - filled < blk:
            take = n - filled
        for j in range(take):
            acc += r2[s + j]
            csum[filled + j + 1] = acc
        filled += take
        b += 1

    D = nbins.shape[0]
    cap = idx_flat.shape[0]
    ep = np.empty(cap); sn = np.empty(cap); nev = 0

    for d in range(D):
        nbin = nbins[d]
        nwin = n - nbin + 1
        for i in range(nwin):
            work[i] = -(csum[i + nbin] - csum[i]) / nbin
        med = np.median(work[:nwin])
        for i in range(nwin):
            work2[i] = abs(work[i] - med)
        scatter = 1.4826 * np.median(work2[:nwin])
        if not np.isfinite(scatter) or scatter <= 0.0:
            continue
        lo = idx_off[d]; hi = idx_off[d + 1]
        m = hi - lo
        if m < 3:
            continue
        prev = work[idx_flat[lo]] / scatter
        cur = work[idx_flat[lo + 1]] / scatter
        for q in range(1, m - 1):
            nxt = work[idx_flat[lo + q + 1]] / scatter
            if cur >= z and cur >= prev and cur >= nxt:
                ep[nev] = ts_flat[lo + q]; sn[nev] = cur; nev += 1
            prev = cur; cur = nxt

    if nev < 2:
        return 0.0
    order = np.argsort(-sn[:nev])
    kept = np.empty(nev); nk = 0
    for oi in range(nev):
        e0 = ep[order[oi]]
        ok = True
        for kk in range(nk):
            if abs(e0 - kept[kk]) <= dedup_sep:
                ok = False
                break
        if ok:
            kept[nk] = e0; nk += 1
    if nk < 2:
        return 0.0

    emin = kept[0]; emax = kept[0]
    for kk in range(1, nk):
        if kept[kk] < emin: emin = kept[kk]
        if kept[kk] > emax: emax = kept[kk]
    span = emax - emin
    p_max = p_max_cfg
    if span > 0.0 and span < p_max:
        p_max = span
    if p_max <= p_min:
        return 0.0
    denom = span if span > p_max else p_max
    df = 1.0 / (oversample * denom)
    f0 = 1.0 / p_max; f1 = 1.0 / p_min
    nf = int(np.ceil((f1 - f0) / df))
    if nf <= 0:
        return 0.0
    bestscore = np.inf                 # sealed: score = 1 - R, minimised; R = 1 - min(score)
    twopi = 2.0 * np.pi
    for q in range(nf):
        f = f0 + q * df
        if f >= f1:
            break
        per = 1.0 / f
        cs = 0.0; sm = 0.0
        for kk in range(nk):
            ang = twopi * ((kept[kk] / per) % 1.0)
            cs += np.cos(ang); sm += np.sin(ang)
        sco = 1.0 - np.hypot(cs / nk, sm / nk)
        if sco < bestscore:
            bestscore = sco
            if 1.0 - bestscore >= obs_R:      # exact early exit: exceedance already certain
                return 1.0 - bestscore
    if bestscore == np.inf:
        return 0.0
    return 1.0 - bestscore


@njit(cache=True, fastmath=False)
def _run(r2, n, all_starts, nblk, blk, nbins, idx_flat, idx_off, ts_flat, durs,
         z, p_min, p_max_cfg, oversample, dedup_sep, obs_R, B, curtail_ge):
    csum = np.empty(n + 1)
    work = np.empty(n + 1); work2 = np.empty(n + 1)
    ge = 0
    used = B
    for bi in range(B):
        R = _surrogate_R(r2, n, all_starts[bi], blk, csum, work, work2, nbins, idx_flat, idx_off,
                         ts_flat, durs, z, p_min, p_max_cfg, oversample, dedup_sep, obs_R)
        if R >= obs_R:
            ge += 1
            if curtail_ge > 0 and ge >= curtail_ge:
                used = bi + 1
                break
    return ge, used


class NumbaPeriodFAP:
    def __init__(self, t, duration_grid, stride_frac=0.5, z_star=2.0,
                 p_min=0.5, p_max=None, oversample=3, dedup_sep=0.3):
        t = np.asarray(t, float)
        self.t = t; self.n = t.size; self.z = float(z_star)
        self.p_min = float(p_min); self.p_max_cfg = float(p_max)
        self.oversample = int(oversample); self.dedup_sep = float(dedup_sep)
        self.cad = float(np.median(np.diff(np.sort(t)))) if t.size > 1 else 2.0 / 1440.0
        nb, idxs, tss, durs = [], [], [], []
        for dur in duration_grid:
            dur = float(dur)
            nbin = max(1, int(round(dur / self.cad)))
            if self.n < 2 * nbin:
                continue
            nwin = self.n - nbin + 1
            step = max(1, int(round(stride_frac * dur / self.cad)))
            idx = np.arange(0, nwin, step)
            nb.append(nbin); idxs.append(idx); tss.append(t[:nwin][idx] + 0.5 * dur); durs.append(dur)
        self.nbins = np.array(nb, dtype=np.int64)
        self.idx_off = np.concatenate([[0], np.cumsum([len(i) for i in idxs])]).astype(np.int64)
        self.idx_flat = np.concatenate(idxs).astype(np.int64)
        self.ts_flat = np.concatenate(tss)
        self.durs = np.array(durs)

    def fap(self, r, obs_R, block_len_days, n_surrogates, rng, curtail_ge=None):
        n, B = self.n, int(n_surrogates)
        blk = max(1, min(max(1, int(round(block_len_days / self.cad))), n))
        nblk = int(np.ceil(n / blk))
        r2 = np.concatenate([r, r])
        starts = rng.integers(0, n, size=(B, nblk)).astype(np.int64)   # same stream as the sealed loop
        ge, used = _run(r2, n, starts, nblk, blk, self.nbins, self.idx_flat, self.idx_off,
                        self.ts_flat, self.durs, self.z, self.p_min, self.p_max_cfg,
                        float(self.oversample), self.dedup_sep, float(obs_R), B,
                        int(curtail_ge) if curtail_ge else 0)
        return (ge + 1) / (B + 1), int(used), used < B, int(ge)
