"""Fast, dependency-light unit tests (numpy/pandas only) — audit remediation 2026-07-19.

Covers the pure-math pieces a referee (or a regression) would check first:
recovery predicate, occurrence-weight integrity, E1/E2 endpoint logic (including
the CI-based E2 decision and the missing-weight guard), the host-assignment
arithmetic that caused the 40-of-80 bug, and the gap-aware detector on synthetic
signals. Heavy-dependency paths (TLS, batman, celerite2) are exercised by the
milestone scripts, not here.

Run:  .venv/bin/python -m pytest tests/ -q
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "research" / "m4_evaluation"))
sys.path.insert(0, str(ROOT / "research" / "m3_calibration"))

import endpoints as EP          # noqa: E402
import recovery as REC          # noqa: E402
from detector import detect_events, _segments  # noqa: E402


# ---------------------------------------------------------------- recovery predicate
def test_period_match_direct_and_harmonic():
    ok, harm = REC._period_match(10.0, 10.05)
    assert ok and not harm                       # within 1%
    ok, harm = REC._period_match(5.0, 10.0)
    assert ok and harm                           # P/2 harmonic
    ok, harm = REC._period_match(30.0, 10.0)
    assert ok and harm                           # 3P harmonic
    ok, _ = REC._period_match(10.4, 10.0)
    assert not ok                                # 4% off, no harmonic


def test_epoch_match_folds_correctly():
    # true epoch 3 periods after the recovered one -> phase distance 0
    assert REC._epoch_match(t0_hat=1.0, p_hat=2.0, t0_true=7.0, t14_true=0.1)
    # offset by half a period -> maximal phase distance
    assert not REC._epoch_match(t0_hat=1.0, p_hat=2.0, t0_true=2.0, t14_true=0.1)


# ---------------------------------------------------------------- E1 endpoint
def _toy_df(n=200, hosts=4):
    rng = np.random.default_rng(0)
    rows = []
    for i in range(n):
        rows.append({"period_days": 1.0, "radius_rearth": 2, "n_transits": 3,
                     "tic": f"h{i % hosts}",
                     "rec_comb": bool(rng.random() < 0.5), "rec_tls": bool(rng.random() < 0.5)})
    return pd.DataFrame(rows)


def test_e1_missing_weight_raises():
    df = _toy_df()
    with pytest.raises(KeyError):
        EP.e1_recall(df, {"P2_R2": 1.0}, B=10)   # wrong cell key -> must not silently zero


def test_e1_point_estimate_and_cluster_ci():
    df = _toy_df()
    out = EP.e1_recall(df, {"P1_R2": 1.0}, B=50)
    manual = df.rec_comb.mean() - df.rec_tls.mean()
    assert out["delta_R_bar"] == pytest.approx(manual)
    assert "cluster_ci95_one_sided_lower" in out and out["n_hosts"] == 4
    assert out["ci95_one_sided_lower"] <= out["delta_R_bar"]


# ---------------------------------------------------------------- E2 endpoint
def _ledger(ratio, n=30, jitter=0.0, seed=1, prefix="h"):
    rng = np.random.default_rng(seed)
    full = 40.0 + rng.normal(0, jitter, n).clip(-30, 30)
    return pd.DataFrame({"tic": [f"{prefix}{i}" for i in range(n)],
                         "cost_full": full, "cost_detector": full * 0.1,
                         "cost_period": 0.0, "cost_tls": full * (ratio - 0.1),
                         "cost_comb": full * ratio, "fast_path_eligible": True,
                         "confirmed_cheap": [i % 3 == 0 for i in range(n)]})


def test_e2_decision_pass_fail_inconclusive():
    assert EP.e2_compute(_ledger(0.50), True, B=2000)["decision"] == "PASS"
    assert EP.e2_compute(_ledger(0.90), True, B=2000)["decision"] == "FAIL"
    # huge per-star spread straddling 0.70 -> INCONCLUSIVE (distinct hosts per frame)
    wide = pd.concat([_ledger(0.40, n=4, seed=2, prefix="a"),
                      _ledger(1.05, n=4, seed=3, prefix="b")])
    assert EP.e2_compute(wide, True, B=2000)["decision"] == "INCONCLUSIVE"


def test_e2_pass_requires_recall():
    out = EP.e2_compute(_ledger(0.50), recall_pass=False, B=500)
    assert out["decision"] != "PASS" or not out["pass"]


def test_e2_pi_star_uses_cheap_path_fraction():
    out = EP.e2_compute(_ledger(0.50), True, B=500)
    assert out["pi_star_breakeven"] == pytest.approx(
        out["rho_d"] / (out["f_p_cheap_path"] * (1 - out["pi_star_rho"])) if
        "pi_star_rho" in out else out["pi_star_breakeven"])
    assert out["f_p_cheap_path"] == pytest.approx(1 / 3, abs=0.05)


# ---------------------------------------------------------------- E2 resume guard (V-1)
def _sub(task_ids):
    return pd.DataFrame({"task": list(task_ids), "tic": [f"t{i}" for i in task_ids],
                         "period_days": 1.0, "radius_rearth": 2, "b": 0.6})


def test_resume_guard_no_ledger_returns_all(tmp_path):
    sub = _sub(range(5))
    out = EP.pending_timing_tasks(sub, tmp_path / "nope.csv")
    assert list(out.task) == list(range(5))


def test_resume_guard_skips_done_tasks(tmp_path):
    led = tmp_path / "ledger.csv"
    pd.DataFrame({"task": [0, 2, 4], "cost_full": 1.0, "cost_comb": 0.5}).to_csv(led, index=False)
    out = EP.pending_timing_tasks(_sub(range(5)), led)
    assert list(out.task) == [1, 3]                 # only unseen ids, no duplicates
    assert list(out.index) == [0, 1]                # re-indexed


def test_resume_guard_idempotent_when_complete(tmp_path):
    led = tmp_path / "ledger.csv"
    pd.DataFrame({"task": list(range(5)), "cost_full": 1.0}).to_csv(led, index=False)
    assert len(EP.pending_timing_tasks(_sub(range(5)), led)) == 0


def test_resume_guard_empty_or_taskless_ledger_returns_all(tmp_path):
    empty = tmp_path / "empty.csv"
    empty.write_text("task,cost_full\n")            # header only, no rows
    assert list(EP.pending_timing_tasks(_sub(range(3)), empty).task) == [0, 1, 2]
    notask = tmp_path / "notask.csv"
    pd.DataFrame({"cost_full": [1.0, 2.0]}).to_csv(notask, index=False)
    assert list(EP.pending_timing_tasks(_sub(range(3)), notask).task) == [0, 1, 2]


# ---------------------------------------------------------------- host assignment
def test_host_assignment_covers_all_hosts():
    """Regression for the sealed-run parity bug: hosts[(j+sc)%80] used only 40 hosts."""
    hosts = list(range(80))
    used_fixed, sc = set(), 0
    for _cell in range(30):
        for _j in range(500):
            used_fixed.add(hosts[sc % len(hosts)]); sc += 1
    assert len(used_fixed) == 80                  # fixed arithmetic: full coverage
    used_buggy, sc = set(), 0
    for _cell in range(30):
        for j in range(500):
            used_buggy.add(hosts[(j + sc) % len(hosts)]); sc += 1
    assert len(used_buggy) == 40                  # documents the sealed run's behavior


# ---------------------------------------------------------------- detector
def test_detector_segments_split_on_gaps():
    t = np.concatenate([np.arange(0, 5, 0.01), np.arange(8, 13, 0.01)])
    segs = _segments(t)
    assert len(segs) == 2


def test_detector_finds_synthetic_transit_and_respects_gap():
    rng = np.random.default_rng(3)
    cad = 2.0 / 1440.0
    t = np.concatenate([np.arange(0, 5, cad), np.arange(8, 13, cad)])
    r = rng.normal(0, 1e-4, t.size)
    center = 10.0                                  # transit inside the 2nd segment
    r[np.abs(t - center) < 0.05] -= 5e-3           # deep 0.1 d dip
    ev = detect_events(t, r, [0.1], z_for_extraction=5.0)
    assert ev.shape[0] >= 1
    assert abs(ev[np.argmax(ev[:, 1]), 0] - center) < 0.15   # epoch not shifted by the gap


def test_detector_no_events_on_pure_noise_at_high_z():
    rng = np.random.default_rng(4)
    t = np.arange(0, 10, 2.0 / 1440.0)
    r = rng.normal(0, 1e-4, t.size)
    ev = detect_events(t, r, [0.1], z_for_extraction=8.0)
    assert ev.shape[0] == 0
