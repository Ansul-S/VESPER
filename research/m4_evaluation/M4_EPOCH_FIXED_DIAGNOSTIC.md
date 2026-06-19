# M4 Epoch-Fixed Confirmation-Statistic Diagnostic Report

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Scope** | CALIBRATION-only. Cleaned null pool (854) + synthetic injections. **No TEST. No sealed-value change. No Seal #2b.** |
| **Purpose** | Confirmation study: does a period-AND-epoch-fixed transit statistic resolve the Finding-B SDE-comparability blocker with FAR control, separation, range-invariance, and ~zero cost? |
| **Verdict** | **Yes — success criteria met.** Recommend proceeding to the Option-2 re-registration (proper calibration + E1 fallback accounting to be done there). |

## 1. Statistic tested
Evidence-first supplies **both** P̂ (integer-comb of detector event spacings) **and** t̂₀, T14 (strongest detector event). The confirmation evaluates a transit matched filter at the **fixed (P̂, t̂₀)** — no phase search, no period grid:
- **White** `√N_cad`: depth / (σ_out / √N_in_cadences). (Naive; overstates S/N under correlated noise.)
- **Red-noise** `√N_tr` (detector-consistent): depth · √N_transits / σ_dur, where σ_dur = robust scatter of the box-averaged flux on the **transit-duration timescale**, and N_transits = number of distinct transits with data. Treats each transit as one independent unit (correct under red noise for P ≫ τ).

## 2. Results (cleaned null pool: 854; 300 nulls, 100 injections, 6-star full-TLS anchor)

| Statistic | null median | null 99th (T, FAR≤1%) | null max | AUC (planet/null) | recall@FAR1% strong (Rₚ≥4) | cost / full | range-inv |
|-----------|-------------|------------------------|----------|-------------------|-----------------------------|-------------|-----------|
| **White** √N_cad | 0.00 | 6.53 | 38.82 | 0.873 | 0.75 | 3.3e-5 | ✓ |
| **Red-noise** √N_tr | 0.00 | **5.52** | **21.76** | **0.877** | **0.79** | 3.3e-5 | ✓ |

Recall by cell (red-noise), illustrating expected physics (recall rises with transit count):

| Cell | median S/N | recall@FAR1% | routed |
|------|-----------|--------------|--------|
| P=1 Rₚ=4 | 16.07 | 0.92 | 0.92 |
| P=2 Rₚ=4 | 9.31 | 0.88 | 0.92 |
| P=4 Rₚ=4 | 6.46 | 0.56 | 0.88 |
| P=2 Rₚ=2 | 0.47 | 0.08 | 0.52 (noise-limited; mostly not even routed) |

## 3. Answers to the owner's specific questions

1. **Does it eliminate/suppress the 21.7 null outlier?** The 21.7 (and the later 806/713) were **contaminant EBs/variables** wrongly included in an unvetted null draw — they are excluded by the sealed M3 cleaning. On the correct cleaned pool, the null tail is bounded; the **red-noise** normalization further suppresses the white tail (max 38.8 → 21.8). FAR is controllable (T_red ≈ 5.5 at the 99th percentile).
2. **Maintains/improves AUC (~0.85)?** **Yes** — 0.877 (red) / 0.873 (white) vs crude depth-SNR 0.85 (and narrow-grid SDE 0.43).
3. **Can a threshold be calibrated at FAR≤1%/star?** **Yes** — T_red ≈ 5.5 (null 99th pct on the cleaned pool). Final value to be calibrated on the full cleaned null pool at re-registration.
4. **Genuinely range-invariant?** **Yes, by construction** — the statistic uses no period grid, so it is unaffected by TLS search-grid width (the root cause of Finding B). Confirmed `True`.
5. **Preserves the E2 compute advantage?** **Yes** — cost 3.3e-5 × full TLS (~0.9 ms vs ~28 s), even cheaper than narrow-grid TLS.

## 4. The recall gap and the fallback (important)
The fast-path confirmation recovers **3/5** Arm-A-recovered anchors, and recall declines at longer period / fewer transits (P=4 → 0.56). This is **not** lost recall for the combined system: in Arm B, a planet that fails to route or fails the cheap confirm **falls back to full TLS** and is recovered there. So:
- **E1 (combined recall non-inferiority)** is protected by the full-TLS fallback — combined recall ≈ Arm A.
- **E2 (compute saving)** accrues only on the fraction confirmed cheaply by the fast path. The numbers above imply a large saving on short-period / high-transit-count planets, less on long-period ones — which is exactly the evidence-first profile.
- This makes ρ_d (detector + period-FAP) the dominant Arm-B cost and **R-1 the correctly-identified live risk**, to be measured at M4.

## 5. Updated three-option comparison

| Dimension | Opt 1: per-arm narrow-SDE T_B | Opt 2: **epoch-fixed (red-noise)** | Opt 3: wider window, single T |
|-----------|-------------------------------|-------------------------------------|-------------------------------|
| **E1 (recall)** | Fails — AUC 0.43, no separation | **AUC 0.877; combined recall protected by fallback** | AUC ≤0.72 at ε=.2; would fail −2pp |
| **E2 (compute)** | ~97% (moot) | **~100% on confirmed fraction (3e-5×)** | erodes to ~84% at ε=.2 and still poor AUC |
| **Appendix-A changes** | small (add T_B) but moot | **large: redefine A.1/A.4 arbiter + add T_red** | smallest (ε only) but unworkable |
| **Calibration workload** | sparse/moot | light compute (statistic is ~free → full null pool easy); spec work heavy | moderate; moot |
| **Interpretability** | weak (SDE on ~20 periods) | **high (matched-filter S/N at known ephemeris); "common-FAR" fairness keystone** | clean story but no workable width |
| **Anti-tuning risk** | low/moot | moderate — new statistic chosen post-discovery; mitigated by CALIBRATION-only + pre-TEST re-registration + single TEST run | low/moot |
| **Verdict** | **rejected** | **recommended** | **rejected** |

## 6. Recommendation
**Proceed to the Option-2 re-registration**, using the **red-noise-aware** epoch-fixed matched-filter S/N as the Arm-B confirmation statistic. It meets every success criterion at the confirmation-study level: robust planet/null separation (AUC 0.88), FAR-controllable (T_red ≈ 5.5 at FAR≤1%), range-invariant by construction, and ~free (3e-5× full TLS), while the full-TLS fallback protects combined recall (E1).

**Caveats to settle at re-registration (not now):**
- Calibrate T_red precisely on the **full** cleaned null pool (not the 300-star sample) and verify FAR≤1%/star.
- Make the **fast-path-confirmed ∪ full-TLS-fallback** recall accounting explicit in A.4, so E1 measures combined recall and E2 measures saving on the confirmed fraction (with ρ_d).
- Fix the exact statistic + template + epoch/duration handling and freeze it (one statistic, no variants) before sealing.
- State plainly that this amendment is **forced by a pre-TEST implementation discovery**, decided on CALIBRATION, sealed before the single TEST run (anti-tuning preserved).

*Per owner instruction, stopping here: no amendment drafted, no threshold calibrated to seal, no Seal #2b, no M4 execution — awaiting review.*
