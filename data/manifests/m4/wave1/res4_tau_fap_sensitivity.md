# RES-4 — Per-star tau_GP FAP sensitivity

**Bounds:** M4_ERRATUM_2026-07-19 §2.4 (tau_GP calibration/test inconsistency)

**Scope.** Calibration NULL stars only, from cached 2.5 d residuals. No TEST read, no network, no sealed artifact edited or re-derived.

**Mechanism.** tau enters the FAP only via L_b = 3*max(tau, T14). Both m3_calibrate and m4_driver.py:117 pass T14 = median(duration_grid) = 0.2 d, so the flat arm is pinned at L_b = 0.6 d and per-star tau can matter only when tau > T14.

## Arms

| Arm | Definition |
|---|---|
| A | flat tau = 0.005 d (sealed run behavior) |
| B | as-implemented per-star (post-audit m4_driver._tau_for: lookup, fallback 0.005); derived exactly from A and C |
| C | per-star tau with complete coverage (recorded M1 tau, else frozen ACF estimator recomputed from the cached residual) |

## Sample

- 1163 cached 2.5 d calibration nulls (185 with a recorded M1 tau row, 978 without).
- tau_C: median 0.0056 d, p95 0.1167 d, max 0.5667 d; 3.87% exceed the sealed T14 = 0.2 d.

## Sealed-fidelity check

`m3_calibrate.py:151` used per-star tau **only** for stars carrying an M1 noise-summary row — 22 of the 968 overlapping stars — and flat 0.005 d for the other 946. The faithful comparison is therefore arm-aware.

- Arm-aware (arm C where M3 had a tau row, else arm A): **968/968** reproduced within 1e-12; max |delta| **0.00e+00**; 968 bitwise identical (FAP quantum 9.990e-04).
- Detector event counts match on 968/968 stars.
- Arm A alone vs M3's record differs on **1** star(s) (max |delta| 5.89e-02). Arm A vs M3's record, ignoring which tau M3 actually used. Differences here are NOT fidelity failures: they are exactly the stars where M3's per-star tau exceeded T14 = 0.2 d, i.e. the effect RES-4 measures.

## tau recomputation validation

- On the 185 stars with a recorded M1 tau, the frozen ACF estimator reproduces it to a median relative error of 0.00e+00 (max 0.00e+00); 100.0% within 1%.

## Gate-decision flips by T14 stratum

| T14 (d) | n | tau_C > T14 | L_b differs | arm B flips (rate, Wilson 95%) | arm C flips (rate, Wilson 95%) |
|---|---|---|---|---|---|
| 0.05 | 1126 | 62 | 62 | 3 (0.0027, [0.0009, 0.0078]) | 24 (0.0213, [0.0144, 0.0315]) |
| 0.1 | 1126 | 45 | 45 | 3 (0.0027, [0.0009, 0.0078]) | 7 (0.0062, [0.0030, 0.0128]) |
| 0.2 **(sealed)** | 1126 | 31 | 31 | 0 (0.0000, [0.0000, 0.0034]) | 1 (0.0009, [0.0002, 0.0050]) |

*0.05 d and 0.1 d are COUNTERFACTUAL stress strata — the sealed pipeline always passes T14 = median(duration grid) = 0.2 d (`m4_driver.py:117`, `m3_calibrate._process_star`). They show that the masking is a property of that convention, not of the tau distribution alone.*

## Findings

- **F1_masking_confirmed** — At the sealed T14 = 0.2 d convention the flat-tau choice changes no gate decision as the driver applies it (arm B: 0/1126, Wilson upper bound 0.0034) and one with complete per-star coverage (arm C: 1/1126, upper bound 0.0050). Erratum §2.4's masking argument is empirically upheld.
- **F2_erratum_2_4_premise_is_imprecise** — Erratum §2.4 states that 'M3 calibrated the period-FAP with per-star tau_GP' while M4 hardcoded 0.005. In fact m3_calibrate.py:151 falls back to 0.005 for any star without an M1 noise-summary row, and only 22 of the 968 overlapping stars had one — M3 was itself overwhelmingly flat-tau. The calibration/test inconsistency is therefore much smaller than that section implies, which strengthens rather than weakens its conclusion.
- **F3_flat_tau_is_mildly_anti_conservative** — The single arm-C flip (TIC 80427281, tau = 0.2889 d) runs flat-open -> per-star-shut: the flat block length is shorter, the surrogate null is easier to beat, and the gate opens on a red-noise null that per-star tau would reject. So the sealed run's FAP gate was very slightly MORE permissive on high-tau stars. Given the prime directive's asymmetry (a false positive is acceptable, a missed planet is not), this is the benign direction.
- **F4_masking_is_a_property_of_the_T14_convention** — Under the counterfactual duration-matched strata the effect reappears: arm C flips 24/1126 at T14 = 0.05 d and 7/1126 at 0.1 d. The masking is bought by passing T14 = median(duration grid), not by the tau distribution being harmless. Any future run that duration-matches T14 must use per-star tau.

**Conclusion.** Sealed fidelity: 968/968 of M3's recorded per-star FAPs are reproduced (max |delta| 0.00e+00), comparing arm C on the 22 stars where M3 had an M1 tau row and arm A on the other 946. The frozen snapshot still is the sealed pipeline. At the sealed T14 convention (median duration grid = 0.2 d), per-star tau_GP changes the period-FAP gate decision on 0/1126 null calibration stars as the post-audit driver would actually apply it (arm B, flip rate 0.0000, Wilson 95% [0.0000, 0.0034]), and on 1/1126 with complete per-star coverage (arm C, 0.0009, [0.0002, 0.0050]). The FAP itself differs on 31/1126 stars, because tau enters only through L_b = 3*max(tau, T14) and only 31 stars have tau > 0.2 d. Erratum §2.4's masking argument is therefore MEASURED, not asserted: the calibration/test tau inconsistency is bounded above by these flip rates and does not change the sealed conclusions.
