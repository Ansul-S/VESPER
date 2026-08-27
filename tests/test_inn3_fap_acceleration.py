"""INN-3 — the accelerated period-FAP must be BIT-IDENTICAL to the sealed one.

These are equivalence tests, not behaviour tests: every assertion below is `==` on
float64, because the whole claim of `fast_period_fap` is that it performs the same
IEEE operations on the same operands in the same order. If any of them ever fails,
the module has stopped being an identity substitution and must not be used as an
estimator of record.

Run:  .venv/bin/python -m pytest tests/test_inn3_fap_acceleration.py -q
"""
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "research" / "m4_evaluation"))
sys.path.insert(0, str(ROOT / "research" / "m4_evaluation" / "frozen_rerun"))

from detector import detect_events                      # noqa: E402  (frozen snapshot)
from period_recovery import best_period, period_fap     # noqa: E402  (frozen snapshot)
from fast_period_fap import FastPeriodFAP, curtail_threshold  # noqa: E402

DGRID = [0.05, 0.1, 0.2, 0.4, 0.8]
Z = 2.0
B = 1000
ALPHA = 0.01


def _fixture(seed=3, n=9000, cad=2.0 / 1440.0, with_transits=True):
    """Synthetic 2-min light curve: red-ish noise plus (optionally) a transit train."""
    rng = np.random.default_rng(seed)
    t = np.arange(n) * cad + 1500.0
    r = rng.normal(0, 1e-3, n)
    r += 3e-4 * np.sin(2 * np.pi * t / 0.7)                       # correlated component
    if with_transits:
        P, t0, dur, depth = 3.1, 1500.6, 0.12, 4e-3
        ph = ((t - t0 + 0.5 * P) % P) - 0.5 * P
        r -= depth * (np.abs(ph) < 0.5 * dur)
    return t, r


def _prep(t, r):
    base = float(t.max() - t.min())
    p_min, p_max = 0.5, 0.5 * base
    F = FastPeriodFAP(t, DGRID, 0.5, Z, p_min, p_max, 3)
    return F, p_min, p_max


def test_rng_vector_draw_matches_scalar_stream():
    """Lever A batches the block-start draws; PCG64 must yield the identical stream."""
    n = 12345
    a = np.random.default_rng(11)
    scalar = np.array([a.integers(0, n) for _ in range(500)])
    b = np.random.default_rng(11)
    assert np.array_equal(scalar, b.integers(0, n, size=500))


def test_curtail_threshold_matches_the_sealed_gate():
    """(ge+1)/(B+1) <= alpha  <=>  ge <= 9  for the sealed alpha=0.01, B=1000."""
    g = curtail_threshold(ALPHA, B)
    assert g == 10
    assert all(((ge + 1) / (B + 1) <= ALPHA) for ge in range(g))
    assert not ((g + 1) / (B + 1) <= ALPHA)


@pytest.mark.parametrize("with_transits", [True, False])
def test_detect_is_bit_identical(with_transits):
    t, r = _fixture(with_transits=with_transits)
    F, _, _ = _prep(t, r)
    a = detect_events(t, r, DGRID, 0.5, Z)
    b = F.detect(r)
    assert a.shape == b.shape
    assert np.array_equal(a, b)


def test_best_R_is_bit_identical():
    t, r = _fixture()
    F, p_min, p_max = _prep(t, r)
    ev = detect_events(t, r, DGRID, 0.5, Z)
    assert ev.shape[0] >= 2
    assert best_period(ev[:, 0], p_min, p_max, 3)[2] == F.best_R(ev[:, 0])


def test_detect_and_comb_bit_identical_on_surrogates():
    """The equivalence must hold on the resampled series, not just the real one."""
    t, r = _fixture()
    F, p_min, p_max = _prep(t, r)
    n = t.size
    blk = max(1, int(round(0.6 / F.cad)))
    nblk = int(np.ceil(n / blk))
    r2 = np.concatenate([r, r])
    offs = np.arange(blk)[None, :]
    rng = np.random.default_rng(5)
    for _ in range(25):
        starts = rng.integers(0, n, size=nblk)
        rs = r2[(starts[:, None] + offs).ravel()[:n]]
        a = detect_events(t, rs, DGRID, 0.5, Z)
        b = F.detect(rs)
        assert a.shape == b.shape and np.array_equal(a, b)
        if a.shape[0] >= 2:
            assert best_period(a[:, 0], p_min, p_max, 3)[2] == F.best_R(b[:, 0])


def test_fap_is_bit_identical_end_to_end():
    t, r = _fixture()
    F, p_min, p_max = _prep(t, r)
    ev = detect_events(t, r, DGRID, 0.5, Z)
    obs_R = best_period(ev[:, 0], p_min, p_max, 3)[2]
    Bsmall = 120                     # keep the test fast; the identity is per-surrogate
    sealed, lb = period_fap(t, r, obs_R, 0.005, 0.2, DGRID, p_min, p_max, Z, 3, Bsmall,
                            np.random.default_rng(77))
    fast, used, curtailed, _ = F.fap(r, obs_R, lb, Bsmall, np.random.default_rng(77))
    assert used == Bsmall and not curtailed
    assert sealed == fast            # float64 equality, deliberately


def test_curtailment_never_changes_the_gate_decision():
    """Exact curtailment is one-sided: it can only stop a run whose gate is already shut."""
    t, r = _fixture()
    F, p_min, p_max = _prep(t, r)
    ev = detect_events(t, r, DGRID, 0.5, Z)
    obs_R = best_period(ev[:, 0], p_min, p_max, 3)[2]
    Bsmall, g = 200, curtail_threshold(ALPHA, 200)
    for seed in (1, 2, 3, 4, 5):
        full, _, _, ge_full = F.fap(r, obs_R, 0.6, Bsmall, np.random.default_rng(seed))
        cur, used, was_cut, ge_cur = F.fap(r, obs_R, 0.6, Bsmall, np.random.default_rng(seed),
                                           curtail_ge=g)
        assert (full <= ALPHA) == (cur <= ALPHA)
        if was_cut:
            assert ge_cur == g and used <= Bsmall and full > ALPHA
        else:
            assert cur == full and ge_cur == ge_full


def test_curtailed_fap_is_a_lower_bound():
    t, r = _fixture(seed=9, with_transits=False)
    F, p_min, p_max = _prep(t, r)
    ev = detect_events(t, r, DGRID, 0.5, Z)
    if ev.shape[0] < 2:
        pytest.skip("fixture produced fewer than N_min events")
    obs_R = best_period(ev[:, 0], p_min, p_max, 3)[2]
    Bsmall, g = 200, curtail_threshold(ALPHA, 200)
    full, _, _, _ = F.fap(r, obs_R, 0.6, Bsmall, np.random.default_rng(42))
    cur, _, _, _ = F.fap(r, obs_R, 0.6, Bsmall, np.random.default_rng(42), curtail_ge=g)
    assert cur <= full
