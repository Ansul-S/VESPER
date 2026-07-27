# Changelog

All notable changes to VESPER are recorded here. Phase-I science is sealed and immutable;
entries after v1.0.0 are **corrections and disclosures** layered on top (append-only —
no sealed document, threshold, weight, statistic, or tag is ever edited).

## v1.0.1 — 2026-07-27 — Verdict correction (audit remediation, DR-003)

**Corrects the headline Phase-I compute verdict published in v1.0.0.** No algorithm,
threshold, weight, sealed document, or tag changed; this is a documentation/analysis
correction with full provenance.

### Corrected

- **The v1.0.0 verdict "H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL, 24.4% < 30%)"
  is withdrawn and superseded.** An independent audit (2026-07-19) found the sealed E2
  result was produced by a 12-star, one-repeat timing measurement in deviation from the
  owner-frozen timing rule, and was statistically undecided (ratio CI [0.42, 1.14]).
- **Corrected verdict: E1 PASS (recall non-inferiority, robust) · E2 INCONCLUSIVE.**
  Re-measured under the frozen rule (300 injections × 5 warm-cache repeats, 39 hosts):
  compute ratio **0.727** (27.3% reduction; target ≥ 30%), host-clustered bootstrap 95%
  CI **[0.636, 0.826]** straddling the 0.70 decision boundary — neither confirmed nor
  falsified. ρ_d 11.6%, f_p 23.7%, break-even prevalence π\* ≈ 0.489 ≫ TESS π ≈ 0.03.

### Added (robustness, Wave 1)

- **RES-2:** E1 is robust to the period-weighting scheme — under KM-occurrence period
  weighting ΔR̄ = −0.16 pp (stronger than the sealed log-uniform −0.48 pp).
- **RES-3:** E1's loss channel is epoch-predicate-driven (loosening the combined epoch
  tolerance to ±1.0 T₁₄ nearly zeroes the combined-side ΔR̄).
- **RES-5:** the P = 0.5 d "gain region" is an epoch phenomenon, not a grid-edge artifact
  (paper supplement S-edge + figure S1).
- **RES-7/RES-8:** monotransit campaign design doc; endpoint-disclosure (precision was
  not a pre-registered endpoint).

### Provenance

- Decision record: [`docs/decisions/DR-003_E2_REMEASUREMENT.md`](./docs/decisions/DR-003_E2_REMEASUREMENT.md)
- Corrections/deviations register: [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](./research/m4_evaluation/M4_ERRATUM_2026-07-19.md) §5/§7
- Re-measurement artifacts: `data/manifests/m4/e2_retiming/e2_retiming_summary.json`
- Sealed bytes remain intact at git tags `phase1-prereg-v2` / `phase1-prereg-v3`.

## v1.0.0 — 2026-06-30 — Initial public release

First public release (rebrand TRINETRA-X → VESPER; branding only — no science changed).
Phase-I pre-registered, sealed, single-evaluation experiment on TESS S1–S3.

> ⚠️ The compute-verdict line in the v1.0.0 release notes ("H1 FALSIFIED — compute
> branch") is **superseded by v1.0.1 above** — see DR-003. The recall result (E1 PASS)
> is unchanged.
