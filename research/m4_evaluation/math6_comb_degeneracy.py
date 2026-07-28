"""MATH-6 (Wave 2): identifiability of the integer-comb period estimator at N = 2.

CLAIM UNDER TEST. With N_min = 2 sealed (Seal #2), the fast path may seed a period from
exactly two detector events. The roadmap states the degeneracy informally as "any
P = spacing/m gives R = 1, and argmin -> longest-P is the realized convention". This
script (a) proves the tie set analytically-by-construction and verifies it numerically,
(b) MEASURES which harmonic the realized estimator actually returns -- the "longest-P"
part of that statement turns out to be true only ~3/4 of the time -- and (c) characterises
why the block-bootstrap FAP stays valid under the degeneracy.

THE DEGENERACY. For epochs {t_1, t_2} with spacing D = t_2 - t_1, the fold score is
    s(P) = 1 - R(P),   R(P) = |mean_j exp(2*pi*i*t_j/P)|
For N = 2, R(P) = |cos(pi*D/P)|... more usefully: both events share a phase exactly when
D/P is an integer, so
    s(P) = 0  <=>  P = D/m,  m = 1, 2, 3, ...      (subject to P >= p_min)
Every such P is a GLOBAL minimum. The period is therefore NOT identifiable from two
events; only the statistic R is (it equals 1 on the whole tie set).

WHY THE FAP SURVIVES. period_fap compares the OBSERVED R against surrogate R values --
never against P_hat. R is constant (= 1) across the entire tie set, and each surrogate is
scored by the identical degenerate procedure, so observed and null statistics are inflated
in exactly the same way. The degeneracy costs period ACCURACY (a recovery-predicate
matter, absorbed for m in {2,3} by the sealed harmonic tolerance in recovery._period_match)
and NOT false-alarm CONTROL. What the N = 2 FAP actually tests is measured below: with
obs_R saturated at 1, it reduces to the null probability that a surrogate produces so few
events that they too fold perfectly -- a test of event RARITY, not of period coherence.

Frozen (sealed) period_recovery is used throughout. Analysis only; no data read, no
sealed artifact touched.

Run:  .venv/bin/python research/m4_evaluation/math6_comb_degeneracy.py
Out:  data/manifests/m4/wave2/math6_comb_degeneracy.json
"""
from __future__ import annotations

import datetime
import json
import platform
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE / "frozen_rerun"))          # sealed code path FIRST

from period_recovery import best_period, _fold_score    # noqa: E402 (frozen)

OUT = Path("data/manifests/m4/wave2")

# sealed grid parameters (m3_config / m4_driver)
P_MIN = 0.5
P_MAX_FRAC_BASELINE = 0.5
OVERSAMPLING = 3
BASELINES = [24.9, 49.6]        # representative S1-S3 baselines seen in the cached residuals
N_TRIALS = 4000
SEED = 20260616


def tie_set_check() -> dict:
    """Verify s(D/m) = 0 for m = 1..M and s != 0 off the comb."""
    D = 7.0
    ep = np.array([3.0, 3.0 + D])
    on = [float(_fold_score(ep, D / m)) for m in range(1, 11)]
    off = [float(_fold_score(ep, p)) for p in (2.9, 4.1, 5.5, 6.3)]
    return {"spacing_days": D,
            "score_on_comb_m_1_to_10": on,
            "max_score_on_comb": max(on),
            "score_off_comb": off,
            "min_score_off_comb": min(off),
            "tie_set_confirmed": bool(max(on) < 1e-12 and min(off) > 1e-3)}


def _select_once(t1: float, D: float, p_max: float):
    """Return (m_selected_or_None, R) for a two-event draw on the sealed grid."""
    ep = np.array([t1, t1 + D])
    P, _, R = best_period(ep, P_MIN, p_max, OVERSAMPLING)
    if not np.isfinite(P):
        return None, R
    m = D / P
    return (int(round(m)) if abs(m - round(m)) < 1e-3 else "non_integer"), R


def _tally(draws, p_max) -> dict:
    cnt, Rs, unresolvable = Counter(), [], 0
    for t1, D in draws:
        m, R = _select_once(t1, D, p_max)
        if m is None:
            unresolvable += 1
            continue
        cnt[m] += 1
        Rs.append(R)
    n = sum(cnt.values())
    if n == 0:
        return {"n_trials": 0, "n_unresolvable": unresolvable}
    within = sum(v for k, v in cnt.items() if isinstance(k, int) and k in (1, 2, 3))
    ge4 = sum(v for k, v in cnt.items() if isinstance(k, int) and k >= 4)
    noninteger = cnt.get("non_integer", 0)
    return {"n_trials": n, "n_unresolvable": unresolvable,
            "selected_m_distribution": {str(k): {"n": v, "frac": v / n}
                                        for k, v in sorted(cnt.items(), key=lambda kv: str(kv[0]))},
            "frac_m_eq_1_longest_P": cnt[1] / n,
            "frac_m_in_1_2_3_absorbed_by_sealed_tolerance": within / n,
            "frac_m_ge_4_harmonic_miss": ge4 / n,
            "frac_non_integer_not_a_harmonic_of_D": noninteger / n,
            "frac_period_predicate_miss": (ge4 + noninteger) / n,
            "min_R": float(np.min(Rs)) if Rs else None,
            "R_saturated_at_1": bool(Rs and np.min(Rs) > 1 - 1e-9)}


def harmonic_selection(baseline: float, rng) -> dict:
    """Which m does the realized argmin return for N = 2, on the sealed grid?

    STRATIFIED, because two distinct mechanisms are at work and averaging them produces a
    design-dependent number that means nothing:

      IN-RANGE  (D <= p_max): the true spacing IS a grid point, so m=1 is reachable and any
                departure from it is pure floating-point tie-breaking. This isolates the
                estimator's own behaviour.
      OUT-OF-RANGE (D > p_max): P = D lies outside the sealed search range entirely, so m=1
                is structurally unreachable and a sub-harmonic is the only possible answer.
                This is a grid-range property, not a tie-breaking property.

    The aggregate over both strata depends on the (data-dependent) spacing distribution and
    is deliberately NOT reported as a single headline number.
    """
    p_max = P_MAX_FRAC_BASELINE * baseline
    in_draws, out_draws = [], []
    while len(in_draws) < N_TRIALS or len(out_draws) < N_TRIALS:
        t1 = rng.uniform(0.0, baseline * 0.5)
        D = rng.uniform(P_MIN * 1.2, baseline - t1)
        (in_draws if D <= p_max else out_draws).append((t1, D))
    return {"baseline_days": baseline, "p_max_days": p_max,
            "in_range_D_le_pmax": _tally(in_draws[:N_TRIALS], p_max),
            "out_of_range_D_gt_pmax": _tally(out_draws[:N_TRIALS], p_max)}


def multiplicity_curve(baseline: float, rng) -> dict:
    """P(R >= 1 - 1e-3) as a function of the number of events -- what the N=2 FAP tests."""
    p_max = P_MAX_FRAC_BASELINE * baseline
    out = {}
    for k in (2, 3, 4, 5, 6, 8, 10, 15):
        Rs = []
        for _ in range(1500):
            ep = np.sort(rng.uniform(0.0, baseline, k))
            Rs.append(best_period(ep, P_MIN, p_max, OVERSAMPLING)[2])
        Rs = np.asarray(Rs)
        out[str(k)] = {"p_R_ge_0.999": float(np.mean(Rs >= 0.999)),
                       "median_R": float(np.median(Rs))}
    return {"baseline_days": baseline, "curve": out,
            "note": ("With obs_R = 1 (the N=2 case) the FAP is the surrogate probability of "
                     "reaching R >= 1, i.e. essentially the probability the surrogate yields "
                     "only 2-3 events. The N=2 FAP is therefore a test of event RARITY under "
                     "the null, not of period coherence.")}


def main() -> None:
    rng = np.random.default_rng(SEED)
    ties = tie_set_check()
    sel = {f"{b:g}": harmonic_selection(b, rng) for b in BASELINES}
    mult = {f"{b:g}": multiplicity_curve(b, rng) for b in BASELINES}

    ir = [v["in_range_D_le_pmax"] for v in sel.values()]
    orr = [v["out_of_range_D_gt_pmax"] for v in sel.values()]
    fr1 = [v["frac_m_eq_1_longest_P"] for v in ir]
    frm = [v["frac_m_ge_4_harmonic_miss"] for v in ir]
    fr123 = [v["frac_m_in_1_2_3_absorbed_by_sealed_tolerance"] for v in ir]
    frni_out = [v["frac_non_integer_not_a_harmonic_of_D"] for v in orr]
    rsat_out = [v["R_saturated_at_1"] for v in orr]
    summary = {
        "task": "MATH-6 comb-statistic identifiability at N=2 (Wave 2)",
        "roadmap_id": "MATH-6",
        "code_path": "research/m4_evaluation/frozen_rerun/period_recovery.py (sealed snapshot)",
        "sealed_grid": {"p_min_days": P_MIN, "p_max_frac_baseline": P_MAX_FRAC_BASELINE,
                        "oversampling": OVERSAMPLING, "N_min": 2, "seed": SEED},
        "tie_set": ties,
        "harmonic_selection": sel,
        "multiplicity_curve": mult,
        "findings": {
            "F1_degeneracy_exact": ("For N=2 with spacing D, s(P)=0 for every P=D/m (m>=1, "
                                    "D/m>=p_min): an exact global tie. P_hat is unidentifiable; "
                                    "R is identified and saturates at 1."),
            "F2_realized_convention_is_not_strictly_longest_P": (
                f"argmin resolves the tie by floating-point rounding of 1-R at the ~1e-16 level, "
                f"not by a period preference. Even IN RANGE (D <= p_max, where P=D is a grid "
                f"point and m=1 is reachable), m=1 is selected in only "
                f"{min(fr1):.1%}-{max(fr1):.1%} of draws; the rest land on sub-harmonics purely "
                f"through float tie-breaking. The roadmap's 'argmin -> longest-P is the realized "
                f"convention' is therefore approximately, not exactly, true, and is corrected "
                f"here. The two strata are reported separately because their aggregate depends "
                f"on the data-dependent spacing distribution."),
            "F3_in_range_degeneracy_is_absorbed_by_the_sealed_tolerance": (
                f"recovery._period_match accepts m in {{2,3}} (flagged harmonic), which covers "
                f"{min(fr123):.1%}-{max(fr123):.1%} of in-range N=2 seeds; only "
                f"{min(frm):.1%}-{max(frm):.1%} leak to m>=4 and miss the sealed period "
                f"predicate. Every such leak is a RECALL cost, never a false positive."),
            "F3b_out_of_range_is_a_different_failure_entirely": (
                f"When D > p_max the true spacing lies outside the sealed search range, so no "
                f"harmonic of D need fall on the grid: {min(frni_out):.1%}-{max(frni_out):.1%} of "
                f"these draws return a period that is not a harmonic of D at all, and R does NOT "
                f"saturate (R_saturated_at_1 = {rsat_out}). This is a grid-RANGE limitation, not "
                f"the tie-breaking degeneracy, and it presents to the FAP as an ordinary weak "
                f"fold rather than as a perfect one."),
            "F4_fap_validity": ("The FAP compares R, which is invariant on the tie set, and the "
                                "surrogates are scored by the identical degenerate procedure. "
                                "The degeneracy therefore cannot inflate the false-alarm rate; "
                                "it costs period accuracy only."),
            "F5_what_the_N2_fap_actually_tests": (
                "With obs_R saturated at 1, the N=2 FAP reduces to the null probability of a "
                "surrogate producing only 2-3 events -- a rarity test, not a coherence test."),
            "F6_reproducibility_caveat": (
                "Because the tie is broken by IEEE-754 rounding, the selected harmonic is "
                "deterministic for a given input and numpy build but is NOT guaranteed stable "
                "across architectures or numpy versions. Any future re-run should pin the "
                "convention explicitly (e.g. argmin over scores rounded to 1e-12, then longest P) "
                "rather than inherit float noise. Sealed Phase-I results are unaffected: they "
                "were produced once, on one build, and are preserved verbatim."),
        },
        "machine": {"platform": platform.platform(), "python": sys.version.split()[0],
                    "numpy": np.__version__},
        "ran_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "math6_comb_degeneracy.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary["findings"], indent=2))
    print(f"\n[MATH-6] -> {OUT}/math6_comb_degeneracy.json")


if __name__ == "__main__":
    main()
