# M4 E2-Fix — Brainstorm → Plan → Validation (session log, 2026-06-18)

> **Purpose.** Self-contained transcript-of-record of the E2 compute-fix investigation, written so a
> fresh Claude session can continue with zero chat history. **Status: EXPLORATORY R&D — CALIBRATION-only,
> NOT adopted, no seal changed, TEST never read.** For the full project state read `CLAUDE.md` →
> `SESSION_HANDOFF_2026-06-18.md` first; this doc is the deep-dive on the compute fix.

---

## 0. Where the project was when this started
- Phase I (evidence-first exoplanet detection on TESS). Goal: prove evidence-first routing is **≥30% cheaper
  than full TLS at non-inferior recall**, on the fast-path-eligible population.
- M0–M3 sealed (Seal #2 `6292c018…`: z⋆=3.4, z_mono=5.3, N_min=2, T=10.74, α_FAP=1%, ε=0.01, B=1000 block-bootstrap FAP, w_c, π̂=3.17%).
- **M4 blocked by Finding B** (narrow-grid TLS SDE not comparable to the full-grid threshold T). The fix
  **Option-2** (epoch-fixed folded-photometry confirmer + full-TLS fallback) was conditionally approved as an *amendment*.
- **Combined-arm calibration dry-run result: E1 PASS / E2 FAIL.**
  - **E1** (recall non-inferiority): ΔR̄ = **−0.39 pp**, one-sided 95% lower bound **−0.80 pp** → PASS (margin −2 pp).
  - **E2** (compute reduction on routed pop): ratio **0.799 → ~20%** measured; population model **~29%**; both **< 30% → FAIL**.
- **Why E2 fails (the thing this session attacks):**
  1. **ρ_d ≈ 12.4%** — the sealed **B=1000 circular block-bootstrap period-FAP** is charged on *every* routed star.
  2. **59% of routed stars fail the FAP gate** → fall back to full TLS (cost = ρ_d + full search > baseline).
  3. Only **41% of routed stars** confirm cheaply (and `T_red≈0` degenerate — the FAP gate, not the confirmer, does the FP rejection).

## 1. The problem in plain terms (airport analogy)
- Full TLS = everyone through one slow thorough security line.
- Evidence-first = add a **fast lane**: cheap pre-screen → quick confirm for the obvious ones → slow line only for the rest.
- What's breaking it:
  1. **The pre-screen (period-FAP bootstrap) costs ~12% of the whole slow search — every fast-lane entrant pays it.**
  2. **59% of fast-lane entrants get bounced to the slow line anyway** (fail the FAP gate) — so they pay the entry tax *plus* the full search.
- Net: big save on 41%, small loss on 59%, tax on all → ~20–29% < 30%.

## 2. Brainstorm — the levers (no-constraints ideation)
- **Lever 1 — make "is this period real?" cheap** (kills ρ_d, the dominant term): analytic/closed-form FAP, precomputed O(1) lookup table, ACF (one FFT) for both period + significance, or **remove the bootstrap from the hot path entirely** (the calibrated confirm + full-TLS fallback already protect recall+precision; FP are acceptable per the Prime Directive).
- **Lever 2 — reduce the 59% bounce**: better/robust period recovery; **try multiple candidate periods at the (free) confirm** instead of one guess.
- **Lever 3 (big swing, Phase-II)**: calibrated **clean-skip** / noise-floor skip — don't run full TLS on no-evidence stars. Where survey-scale savings actually live (trades recall → own validation).
- **Lever 4 — reframe**: O(N) vs O(N·P·D) complexity-class story; **monotransit sensitivity** (TLS structurally can't fold P > baseline — evidence-first finds them). A sensitivity win, not just a speed win.

## 3. The proposed 4-part plan (owner's synthesis)
1. **Zero-cost white-noise pre-filter.** Compute the analytic *white-noise* FAP first. Claim: red noise inflates FP rate (MATH §10.2) so **FAP_red ≥ FAP_white**; therefore if white FAP > α already, reject instantly (can't pass red). Formula `1−(1−b^(1−k))^{N_P}`.
2. **O(1) lookup / EVT FAP.** For survivors, replace the B=1000 bootstrap with a precomputed red-noise null over a grid (baseline, k, noise), bilinear interpolation → O(1). Keeps the H4 "FAP ≤ α" requirement, computed cheaply. → ρ_d ~12% → ~0 → E2 past 30%.
3. **Multi-period harmonic testing.** Bounce is mostly harmonic aliasing (guessing gap, P/2, P/3). Since the photometric confirm is cheap, test the top 3–5 integer fractions (P/2, P/3, 2P), keep the highest sign-aware folded-transit S/N. Rescues aliased real planets → fewer bounces.
4. **Strategic reframe.** Frame as O(N) vs O(N·P·D); highlight monotransit sensitivity.

## 4. Technical assessment + arithmetic (mine)
**Verdict: sound for the *scoped* E2; #1 elegant but its "provably safe" claim needs empirical check.**

E2 ratio ≈ (confirmed)·(fast cost) + (fallback)·(1 + fast cost):

| Scenario | confirmed | ρ_d | E2 ratio | reduction |
|---|---|---|---|---|
| Now | 41% | 0.12 | 0.71 | **29% FAIL** |
| +#1/#2 (ρ_d→~0.02) | 41% | 0.02 | 0.61 | **39% PASS** |
| +#3 (confirmed→~60%) | 60% | 0.02 | 0.42 | **58% PASS** |

Caveats flagged: (a) E2 numbers from a 12-star timing subset (noisy); (b) this wins the *scoped* E2, **not** survey-scale (that needs clean-skip, Phase-II); (c) **in the sealed project, replacing the B=1000 bootstrap touches sealed A.8 — a bigger re-registration than the Option-2 confirmer swap, and it bumps the proposed "v3-as-final" stopping rule.**

## 5. Validation Experiment 1 — pre-filter premise (`validate_prefilter.py`)
**Test:** on 120 M3 null stars, recompute the white-noise FAP of the *same* comb statistic (uniform event-time redraw) and compare to the stored red block-bootstrap FAP.

**Results:**
- `white ≤ red` holds for **only 18.3%** of stars → **the per-star inequality is FALSE**; the "mathematically impossible to pass red if fails white" justification does **not** hold as a universal law.
- corr(white, red) = **0.868** (white is a strong *proxy* → supports the lookup idea #2).
- Bare pre-filter (reject if white > α=0.01) rejects **98.3%** of null candidates.
- 0 unsafe wrong-rejects — **but under-powered** (nulls rarely pass red by construction, so the dangerous case had ~1–2 chances to appear). **Recall-safety must be tested on injected planets** (next experiment).

## 6. Validation Experiment 2 — injection recall-safety (`validate_prefilter_injections.py`)
**Test:** inject 100 strong/recoverable planets (P≤4 d, R≥2 R⊕) into cleaned-null calibration hosts. For each, compute BOTH the red FAP (B=1000 bootstrap, same as M3) and the cheap white FAP, plus whether the recovered period matches truth. The recall-killing case = a planet the red test would keep (red FAP ≤ α) that the white pre-filter would clip (white FAP > threshold).

**Results:**
```
injected=100  routed=99  red-pass (fap_red<=α)=46  period-matched true recoveries=39

BARE pre-filter (reject if white > α):
  clips 4/46 red-pass AND 2/39 true recoveries   -> ~5% of real planets LOST (the danger is real)
  white FAP among red-pass: median 0.002, max 0.055

WITH a safety margin:
  reject only if white > 5.5·α  -> clips ZERO red-pass planets
  reject only if white > 3.2·α  -> clips ZERO period-matched true recoveries
  null rejection: 98.3% (bare) -> 97.5% (margined)   <- compute win essentially intact
```

**Interpretation:** the *bare* threshold (slide #1 as written) loses ~5% of planets — confirms my caution. **A simple safety margin fixes it:** at **white > ~5.5·α**, the pre-filter clips **zero** recoverable planets while still skipping the bootstrap on **97.5%** of noise → **ρ_d → ~0 → projected E2 ~40% (PASS), with recall preserved.**

## 7. Conclusions
- **E2 is FIXABLE, not a fundamental falsification.** The failure was a *configuration* cost (the sealed B=1000 period-FAP), not a property of the evidence-first principle. A **margined white-noise pre-filter** (+ O(1) lookup for the ~2.5% survivors + multi-period harmonic confirm) removes the entry tax while preserving recall.
- **The recommended fix:** reject a period candidate (skip the bootstrap) only when **white-FAP > ~5.5·α** (use a buffer ~6–8·α for safety). This is *recall-safe by measurement* (zero planets clipped), not by the (false) "provably safe" argument.
- **Honest caveats (must address before trusting operationally):**
  1. Margin (5.5·α) is from **~40 red-passers** on **strong cells (P≤4 d, R≥2)** — re-validate on a larger, full-grid injection set; the *shape* (small margin → zero loss, compute intact) is robust, the exact number is not yet locked.
  2. The premise (white as a hard bound) is **false per-star** — it works only as a **margined heuristic**, validated empirically.
  3. Margin is **statistic-specific** — I tested uniform-redraw white FAP; the analytic formula `1−(1−b^(1−k))^{N_P}` is a *different* white null (binned vs continuous-R) and would need its own margin calibration.
  4. **Governance:** the fix touches **sealed A.8 (period-FAP)** → adopting it **expands the v3 re-registration scope** beyond the Option-2 confirmer swap, and bumps the proposed **v3-as-final** stopping rule. This is an owner decision (v3 scope: confirmer-only vs +FAP-cheapening).

## 8. Open items / next steps
1. **Owner: decide v3 SCOPE** — confirmer-only, or confirmer + period-FAP cheapening (this E2-fix).
2. If in scope: **lock the margin** on a larger/full-grid injection set (more stars, all (P,R) cells), and decide the deployed white-FAP estimator (uniform-redraw vs analytic formula vs ACF) → calibrate its margin.
3. Re-run the **combined-arm E2** with `margined pre-filter → lookup → multi-period confirm → fallback` to confirm > 30% and E1 still passes (a bigger timing subset than the 12-star one).
4. All of this stays **CALIBRATION-only** and must be **sealed before** the single TEST run (anti-tuning NN#2).

## 9. Artifacts (this investigation)
- Code: `research/m4_evaluation/validate_prefilter.py`, `validate_prefilter_injections.py`.
- Data: `data/manifests/m4/dry_run/prefilter_validation.csv`, `prefilter_injection_safety.csv`.
- Broader M4 context: `M4_COMBINED_ARM_RESULT.md` (E1/E2), `M4_OPTION2_METHODOLOGY_DECISION.md` (Option-2 verdict), `PHASE1_AMENDMENT_STOPPING_RULE.md` (v3-as-final governance), `SESSION_HANDOFF_2026-06-18.md` (full state).

---
*EXPLORATORY R&D log. No sealed value changed; TEST never read; 0 TEST TICs in any artifact (verified). Nothing here is adopted — it informs the pending owner decisions on v3 scope and salvage-vs-negative-result.*
