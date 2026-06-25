# M5 Tables — parameter recovery + FAP calibration (from existing artifacts)

> `m5_recovery_calibration.py`; no new compute, no TEST re-read. Period/epoch from the
> sealed-test recovery; FAP calibration from the M3 null pool.

## T5 — Parameter accuracy (period & epoch; depth/T14 deferred — not logged)

| metric | value |
|---|---|
| routed injections with a period seed | 11036 |
| period_match rate (within tolerance) | 45.9 % |
| harmonic among period-matched | 27.1 % |
| median |ΔP/P| (all seeded) | 0.0162 |
| median |ΔP/P| (period-matched) | 0.0022 |
| epoch_ok rate (|Δt0| ≤ 0.5 T14) | 54.2 % |
| median epoch offset (T14 units) | 0.402 |

## T4 — Period-FAP calibration on null stars

| metric | value |
|---|---|
| cleaned null stars with a period-FAP | 833 |
| FAR at nominal α=0.01 (cleaned, sealed basis) | 1.08 % |
| FAR at nominal α=0.01 (raw, pre-cleaning) | 2.07 % |
| nominal α_FAP (sealed) | 1 % |
| matches sealed M3 (1.08%) | YES |
| calibration verdict | well-calibrated |
