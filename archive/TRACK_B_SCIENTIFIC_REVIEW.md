# TRINETRA Track B (v3) — SCIENTIFIC REVIEW

**Reviewer role:** Independent scientific referee
**Subject:** The "evidence-first" detection pipeline (TRINETRA v3) — matched-filter dip detection → Hough period recovery → (intended) targeted TLS
**Evidence base:** Source code (`q2_false_positive.py`, `q3_period_recovery.py`, `Unknown star search/unknown_star_search.py`), the recorded search outputs (`search_iter1_candidates.csv`, `search_iter2_candidates.csv`), and the MASTER report.
**Date:** 2026-06-13

---

## VERDICT (up front)

> **The detection *concept* is scientifically sound. The detection *architecture as built* is not — but its flaws are in ordering and statistical calibration, not in the founding idea, so they are fixable without abandoning the approach.**

The pipeline reduces every candidate dip to a single **timestamp** and then makes its accept/reject decision on the **phase-coherence of those timestamps** — a statistic that is *trivially satisfied by noise* and is never calibrated against a null hypothesis. The photometric evidence that actually distinguishes a transit (depth, shape, repeatability) is computed *after* grading, in a "vetting" stage that runs too late to stop anything, and one of whose checks (even/odd) is a silent no-op. The confirmation stage that was supposed to be the real detector (targeted TLS) **was never implemented**. The result is a system that manufactures periodic signals out of stellar and instrumental noise — which is exactly what the recorded data shows: **0 of ~50 candidates across two iterations passed vetting, and every single one failed the phase-folded dip-shape test.**

This is a *correctable* architecture, not a dead end. §7 gives the minimal redesign.

---

## 1. CURRENT DETECTION METHODOLOGY (what the code actually does)

Tracing `get_star()` → `run_trinetra_search()` → `vet_candidate()`:

1. **Acquire & condition** — download/stitch ≤400 d of Kepler long-cadence flux; require baseline ≥ 300 d; 5σ clip; normalize to unit median; Savitzky–Golay detrend (2-day window, polyorder 2, `mode="mirror"`); zero-center: `flux_detr = flux/trend − 1`.
2. **Matched filter (the trigger)** — convolve with a box kernel of ~6 points (3 h); robust noise `σ_mad = 1.4826 · MAD`; flag `response < −3σ_mad`; cluster adjacent flags, keep the deepest point per cluster → **a list of dip *times*** (`unknown_star_search.py:264–296`). Depth is retained only as a transient local variable; it is **not** carried into the period stage.
3. **Hough period recovery** — scan 1000 trial periods in [0.5, min(baseline/2, 200)] d; phase-fold the dip times; `score = (max bin occupancy) / n_dips` (`:308–324`).
4. **"SNR estimate"** — `mean(|response_at_dip|) · √n_dips / σ_mad` (`:329–335`).
5. **Grade A/B/C** — thresholds on `hough_score`, `fp_per_window`, `snr_est`, `n_dips` (`:337–367`).
6. **Vetting (post-hoc)** — period-spacing consistency, phase-folded dip shape, even/odd depth ratio (`:374–467`).
7. **Targeted TLS confirmation** — **absent.** The fast path terminates at step 5/6. The MASTER report (§3.1 Step 4, §8.3) confirms this step "NOT IMPLEMENTED."

**Structural diagnosis:** the evidence hierarchy is inverted. A transit search should decide *"is there a significant, repeating, transit-shaped flux decrement?"* and only then *"at what period?"*. This pipeline decides period first (on timestamps alone) and asks about photometric significance last — and never lets that significance veto the grade.

---

## 2. MATHEMATICAL ASSUMPTIONS — and where they break

**(a) White-Gaussian-noise threshold.** The −3σ_mad cut assumes white Gaussian residuals, giving P(cross) ≈ 1.35×10⁻³ per point. With ~18,900 points and a 6-point kernel (≈3,150 quasi-independent windows), **pure white noise alone yields ≈4 false dips per star**; the red noise and stellar-variability residuals that survive a 2-day SG filter push this higher. The project's own Q2 result (≈20 FP events per baseline at the median operating point) is itself a statement that a *planet-free* star routinely produces ~20 dips. So "≥3 dips" (`MIN_DIPS`) is a threshold that **noise clears by construction.**

**(b) The Hough score is uncalibrated against a null.** `score = max_bin/n_dips` has no associated false-alarm probability, and the scan over 1000 trial periods is an uncorrected multiple-comparisons (look-elsewhere) search. With few dips this is fatal: for `n_dips = 3` and `n_bins = max(10, ⌊√3·3⌋) = 10`, scanning 1000 periods will *almost surely* find a period at which all three phases share one bin → **score = 1.0 from pure noise.** The recorded candidates confirm this exactly:

| KIC | n_dips | best_period | hough_score |
|-----|:------:|:-----------:|:-----------:|
| 10005147 | 3 | 16.88 d | **1.00** |
| 10033388 | 3 | **0.50 d** (grid edge) | **1.00** |
| 10032968 | 3 | 1.70 d | **1.00** |
| 10088111 | 4 | 30.26 d | **1.00** |
| 10018778 | 4 | 34.45 d | **1.00** |

These are not detections; they are the score metric's degenerate limit. A correct method must compare the observed score to the score distribution of *scrambled* dip times and require, e.g., a <1% false-alarm probability.

**(c) The Monte-Carlo validation models the wrong noise.** Q3 draws false-positive times from `np.random.uniform` (`q3_period_recovery.py:266`) — i.i.d. uniform. Real Kepler false dips are **correlated and clustered** (red noise, quarter systematics, rotation). Uniform FPs scatter in phase and are the *easy* case for Hough; clustered FPs conspire to produce coherence. Hence Q3's headline ~83% recovery does **not** transfer to real stars — and indeed the live search shows a 9–26% "candidate" rate with **0% surviving vetting.** The simulation validated the method against a noise model its targets do not obey.

**(d) The "SNR estimate" is circular and therefore inert.** Dips are *selected* for `|response| ≥ 3σ_mad`; therefore `mean(|response|)/σ_mad ≥ 3` automatically, and `× √n_dips` gives `≥ 3√n`. For 14 dips that is ≥11 *before any signal exists*. The data show `snr_estimate` of 15–41 **on stars whose phase-folds are flat** (KIC 10019358: 38.7; KIC 10079998: 41.3). This quantity measures "how many threshold crossings, and how far past threshold," not transit significance. The Grade-A gate `snr_est ≥ 8` is consequently **vacuous** — nothing a candidate could do would fail it.

**(e) Grid-edge pile-up.** `PERIOD_MIN = 0.5` produces candidates sitting exactly on the boundary (KIC 10033388 and KIC 10063028 both at P = 0.5000 d) — a classic grid artifact, not a population of half-day planets.

---

## 3. SOURCES OF FALSE POSITIVES (ranked, from the data)

The recorded candidates carry a uniform fingerprint: **`vet_shape_ok = False` for 100% of them**, and `vet_period_ok = False` for the large majority. The system's own later checks already say "not a transit" — they simply run after grading.

1. **Sparse-dip Hough coherence (dominant).** 3–4 noise dips → score up to 1.00 (§2b). This is the principal false-positive engine.
2. **Stellar variability / rotation residuals.** A 2-day SG window does not remove all quasi-periodic stellar signal; surviving wiggles produce repeatable-looking dips. Notes like "period inconsistent: rms=0.15 d" at P≈1.3 d (KIC 10064921) are rotation/pulsation leakage.
3. **Kepler instrumental ≈30 d harmonics.** A conspicuous period pile-up at **30.2–30.9 d** (KIC 10088111, 10028156, 10063468, 10032516, 10080239, 10079998, …) — the quarter/momentum-dump timescale and its aliases (see §4).
4. **Single deep events seeding long periods (§6).** KIC 10023062 → P≈185–189 d, unstable across iterations.
5. **Period-grid boundary pile-up at 0.5 d (§2e).**

---

## 4. QUARTER-BOUNDARY ARTIFACTS

**Mechanism.** Detrending is applied to the **already-stitched** multi-quarter series with a single 2-day SG window (`get_star()` `:222–230`). Kepler quarters carry per-quarter flux offsets and gaps; an SG filter run *across* a discontinuity (with `mode="mirror"`) rings at the seam, depositing spurious negative excursions localized at the ~90-day quarter joins and their harmonics (~45 d, ~30 d, ~15 d).

**Evidence.** The 30-day clustering in §3.3 is the signature. A genuine planet population would not pile up at the dominant instrumental cadence.

**Assessment of the proposed fix.** The MASTER report's remedy — mask ±1 d around quarter boundaries — treats the symptom. The **root cause** is detrending across segment boundaries. Correct order: detrend **per quarter before stitching** (so each segment's filter never sees a seam), then mask known boundary/momentum-dump times, then concatenate. This removes the source rather than censoring its output.

---

## 5. EVEN/ODD VETTING BUG (precise root cause)

`vet_candidate()` `:433–458`. The check is meant to catch background eclipsing binaries (alternating transits with unequal depth). It is broken in four compounding ways:

1. **Unsorted `np.interp` (the silent failure).** It evaluates `np.interp(p, phases[phases>0], flux_detr[phases>0])`. `np.interp` **requires its `xp` array to be monotonically increasing**; `phases` here is in folded-time order, *not* sorted. NumPy does not error — it returns numerically meaningless values. This is precisely the "fails silently" behaviour the report flagged.
2. **Phase-convention mismatch.** The interpolation grid `phases` was remapped to **[−P/2, +P/2]** at `:419` (`phases[phases > period/2] -= period`), but `even_phases`/`odd_phases` are computed as `(dip − t0) % period` in **[0, P]**. The query coordinate and the grid coordinate are in different conventions, so even a *correct* interpolation would sample the wrong location.
3. **`abs()` erases the sign.** Depth proxy is `abs(np.interp(...))` of zero-centered flux — conflating dips (negative) with brightenings (positive). A real secondary eclipse — the very thing even/odd exists to expose — would be hidden by the absolute value.
4. **Single-sample "depth."** It interpolates one flux value at the dip phase rather than an averaged in-transit depth — i.e. a single noise sample.

**Net effect:** `even_odd_ok` is **True for essentially every candidate** (it flipped once across both iterations — KIC 10064019, ratio 2.7). So the bug is **not** that it rejects real planets; it is that the check is an **inert no-op** that contributes false reassurance and can never catch the EB case it was written for. Note this is *not* why 0/68 pass — the blockers are the shape test (always fails) and period-consistency. Even/odd silently passing everything is a **latent reliability hole**, not the current gate.

---

## 6. SINGLE-EVENT ARTIFACT CONTAMINATION

**Mechanism.** The matched filter smears one sharp event (flare, cosmic ray, momentum-dump residual) across ~6 kernel points; clustering keeps a single dip, but one anomalously deep event then anchors the Hough accumulator when little real structure is present. Combined with a handful of noise dips, it manufactures a coherent-looking long period.

**Diagnostic signature — period instability on identical data.** A real planet's period is invariant under re-analysis. An artifact's is not:

| Star | Iter 1 | Iter 2 | Report history |
|------|--------|--------|----------------|
| KIC 10023062 | P=185.4 d, score 0.53, 32 dips | P=188.8 d, score 0.86, 21 dips | 59 d → 188 d → 128 d |

Same light curve, different period each pass → unambiguously not astrophysical.

**Missing guards.** Nothing rejects a single `|dip| > 10σ` as an artifact; nothing tests **jackknife stability** (does the recovered period survive deleting any one dip?); nothing requires ≥3 **independent** transits of **consistent depth**. Any of these would have removed KIC 10023062 automatically.

---

## 7. IS THE CONCEPT SOUND, OR IS THE ARCHITECTURE FLAWED?

**The concept is sound.** "Detect individual transit-like decrements in O(N), infer period from their spacing in O(k²), then confirm with a *targeted* TLS over a narrow grid" is a legitimate, published-in-spirit strategy (single-transit / monotransit searches; BLS-seed-then-refine). For Jupiter/Neptune-class planets — where individual transits clear the noise — the complexity argument is real and the bimodality insight from Q1 is genuinely good science.

**The architecture as built is flawed,** for three structural reasons (plus two broken statistics):

1. **Inverted evidence hierarchy.** Accept/reject is decided on dip-*time* coherence; photometric depth/shape/repeatability is discarded before the decision and only revisited in non-blocking "vetting."
2. **No null calibration.** The Hough score carries no false-alarm probability and the 1000-period look-elsewhere effect is uncorrected; thresholds (0.40–0.60) are arbitrary and, at low `n_dips`, meaningless.
3. **No confirmation stage.** The targeted-TLS step that was meant to be the actual detector was never built, so the pipeline stops exactly where false positives live.
   - plus the **SNR statistic is circular** (§2d) and the **even/odd check is inert** (§5).

These are defects of **ordering and calibration**, not of the founding idea. They are fixable.

### Minimal redesign to make it sound (highest-leverage first)
1. **Move significance before grading.** Require, as the *gate*, a phase-folded transit that is depth-significant (in-transit mean below out-of-transit by ≥ a calibrated SNR) and U/V-shaped — using **binned/averaged** depth, **sorted** phase, and **sign-aware** (dips are negative) statistics. (This also rewrites the even/odd check correctly.)
2. **Calibrate the Hough score.** Bootstrap against scrambled/scrambled-in-time dip sets; require false-alarm probability < ~1%; apply a look-elsewhere correction for the 1000-period scan. Down-weight or veto `n_dips < ~5`.
3. **Build the targeted-TLS confirmation** and make **its** SDE (e.g. ≥ 9) the accept criterion — Hough only seeds the grid.
4. **Replace the circular SNR** with a true phase-folded transit SNR.
5. **Add artifact guards:** reject single `|dip| > 10σ`; require jackknife-stable period; require ≥3 independent, consistent-depth transits.
6. **Fix detrending order:** per-quarter detrend *before* stitch; then mask boundary/momentum-dump times.

**Salvageable as-is:** the matched-filter + MAD trigger (as a *trigger* only), the Q1 routing philosophy, the speed argument, the zero-centering and MAD fixes (both correct), and the honest bug-logging culture.
**Must be rebuilt:** everything downstream of the dip list.

---

## 8. CREDIT WHERE DUE

The MAD-vs-rolling-std fix and the zero-centering fix are correct and well-reasoned. The Q1 detectability-bimodality result is real, useful science. The "recall over precision" principle is the right call for a discovery instrument. And the project documents its own failures candidly — the report already names the vetting bug, the quarter-boundary problem, and the single-event problem. This review sharpens *why* each occurs and shows that, taken together, they reflect one root cause: **decisions are made on the wrong evidence, in the wrong order, without a null.** Fix the order and add the null, and the concept can stand.

---

*End of review. No source files were modified.*
