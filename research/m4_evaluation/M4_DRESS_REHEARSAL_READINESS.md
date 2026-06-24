# M4 Dress-Rehearsal Readiness Report (CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-20 |
| **Purpose** | De-risk the single irreversible TEST read: verify the v3 (confirmer-only) M4 driver is correct, and characterize the recall-loss mechanism, before the owner's go. |
| **Scope** | CALIBRATION cleaned null hosts; 240 injections (per-cell 8) instrumented; E2 timing on a 6-star subset. **TEST never read; 0 TEST TICs.** |

## Machinery (all verified)
- Seal #2 `6292c018…` + v3 manifest `54f06a94…` hash-verified in-run (fail-closed). TEST-blind (`test_accessed:false`).
- E1 (occurrence-weighted ΔR̄ + one-sided 95% CI), E2 (compute ledger), per-injection pathway logging — all correct.

## Headline (per-cell 8, 240 injections)
- **E1 — recall non-inferiority: ΔR̄ = −0.17 pp, lo95 = −0.51 pp → PASS** (margin −2 pp; comfortable).
- **E2 — scoped compute: reduction −5.6% (ratio 1.056), ρ_d = 0.138 → FAIL** (entry tax retained; <30%).
- **Pre-committed verdict: FALSIFIED — compute branch (E1 pass, E2 fail).**

> The earlier per-cell-5 run showed E1 "FAIL" (lo95 −5.19 pp). That was **underpowered noise**, not a real recall failure: at per-cell 8 the CI tightens to −0.51 pp and the point estimate (−0.17 pp) is essentially non-inferior. E1 **passes**; recall is protected.

## Recall-loss mechanism (the owner's question) — ONE pathway
- Outcomes vs Arm A: both 115 · neither 102 · **loss 14** · gain 9.
- **All 14 losses share a single pathway: `cheap_confirm` with `fallback_suppressed = True`** (100%). The confirmer confirmed at the seeded ephemeris (huge Λ, shape-consistent) and therefore suppressed the full-TLS fallback; the seed then failed the recovery predicate → miss. Arm A (full TLS) recovers all 14 via its own fitted ephemeris.
- **Failure point within the pathway:**
  - **11 / 14 = right period, wrong EPOCH** (period_err median 0.005 — period is correct; t̂₀ from the detector's strongest-event epoch lands just outside the ±0.5·T₁₄ recovery window). The cheap path trusts the **detector's** event epoch, which is *less precise* than TLS's fitted T₀ — a genuine but marginal cost of the cheap path.
  - **3 / 14 = wrong period** (period_err 0.01–0.30); the confirmer still confirmed (a transit-like fold exists at the alias) and suppressed fallback.
- **Magnitude: −0.17 pp occurrence-weighted (sub-margin).** 9 gains (confirmer recovers planets whose full-TLS SDE fell just below T) partly offset the 14 losses. Net does **not** threaten E1 non-inferiority.

## Interpretation — genuine limitation vs v3-design interaction
The recall leak is a **v3-confirmer interaction**, not a fundamental failure of evidence-first period recovery: it is driven by **T_red=0 (non-binding) confirming on a right-period / marginally-off-epoch seed and suppressing the fallback**, dominated by the detector epoch being less precise than TLS's. It is one clean, well-understood mechanism, and it is **below the non-inferiority margin** — E1 passes. It would *not* be the thing the TEST measures as the verdict.

**The decisive, robust finding is E2 (compute):** with the sealed B=1000 period-FAP that the equivalence gate proved un-cheapenable (both candidates failed), ρ_d ≈ 0.12–0.14 is charged on every routed star and the fast path does not earn ≥30% — here it is even net-negative on the timing subset. This is the **genuine limitation**: evidence-first routing, in its sealed v3 realization, does not beat full TLS on compute. E2 fail is the honest Phase-I falsification (compute branch); E1 (recall) is supported.

## Readiness verdict
- **Machinery: ready.** ✓
- **Expected single-TEST outcome: E1 pass / E2 fail → H1 FALSIFIED (compute branch)** — a legitimate negative Phase I. The recall principle and the transit-LR confirmer stand; the compute claim is the falsifiable casualty, traceable to the un-cheapenable sealed period-FAP (not to a confirmer bug).

Artifacts: `data/manifests/m4/dress_rehearsal/{recovery,timing_ledger,e1_per_cell}.csv`, `summary.json`; log `data/manifests/m4/m4_dress_rehearsal2.log`.
