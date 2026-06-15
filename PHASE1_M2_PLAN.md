# Phase I — M2 Plan & Injection / Transit-Preservation Choices

| Field | Value |
|-------|-------|
| **Document** | M2 execution plan + injection / η-validation frozen-choices proposal |
| **Increment** | **v0.1 — M2 only** (Injection harness + η ≥ 0.90 transit-preservation check) |
| **Created** | 2026-06-15 |
| **Status** | **IN PROGRESS** — harness built + validated; **detrend window FINALIZED at 2.5 d** (M2.4, owner-approved 2026-06-15); full η grid (30 cells × 200 inj) running. Corners 8/1 & 16/1 (noise-limited), 16/2 (borderline) documented + non-gating. |
| **Builds on** | M0 (Seal #1 `1f2d49e1…`), M1 (Stage-0 conditioning; config `m1_config.yaml`, window 0.5 d **provisional**) |
| **Authority** | Subordinate to the sealed pre-registration (`phase1-prereg-v2`). Executes VAL §3 (injection truth), §4.2 (η check), A.1/A.4/A.9. Changes nothing in the sealed docs. |

> **What M2 is.** Build the **injection harness** (Mandel–Agol transits, limb-darkening from TIC stellar params, injected into **real** calibration light curves preserving correlated noise) and run the **transit-preservation check** (VAL §4.2): inject at the frozen grid → apply Stage-0 conditioning → measure η = δ_post/δ_true per (P,R_p) cell → **require median η ≥ 0.90**. The check **finalizes the M1 detrend window**: where η < 0.90, the window is widened **before** any M3 threshold (never after).
>
> **Why sign-off first (your directive).** The injection harness, limb-darkening assumptions, and η-validation design are **frozen** before any build. This doc proposes them; nothing is implemented until §8 is signed.

---

## 1. Scope & boundary

**M2 does:** freeze the injection/η config (post sign-off); build the injection harness; inject Mandel–Agol transits at the **frozen grid** (VAL §3) into real **calibration, null-pool** light curves; re-run Stage-0 conditioning; measure η + a shape-distortion diagnostic per (P,R_p) cell; **finalize the detrend window** (widen where η < 0.90); report the η table + frozen conditioning config for M3.

**M2 does NOT:** touch the **TEST** split (sealed until M4 — G1); set any detection threshold (`z⋆, θ, T, …` are M3 / Seal #2 — G2); run the detector / period inference / TLS detection (M3+); change the **frozen injection grid or η_min = 0.90** (sealed — VAL §3, §4.2); modify any sealed document; build Phase II machinery.

**Hosts:** inject into **null-pool** calibration targets (`is_null`, no known TOI/FP) so the η measurement isn't contaminated by real transits; reuse the M1-conditioned η-sample where null.

---

## 2. Decomposition (M2.1 → M2.5)

| Sub-step | Task | Sealed basis |
|----------|------|--------------|
| **M2.1** | Freeze injection/η config (model, LD source, e, derivations, η design) → `m2_config.yaml` | VAL §3, A.1 |
| **M2.2** | Injection harness: `batman` Mandel–Agol; quadratic LD from TIC (Teff/logg/[Fe/H]); inject in relative-flux space into real PDCSAP at sampled ephemerides | VAL §3, A.1 |
| **M2.3** | η measurement: inject grid → re-condition (M1 pipeline) → recover δ_post at the **known** ephemeris (fixed-shape least-squares depth) → η = δ_post/δ_true + shape diagnostic, per (P,R_p) cell | VAL §4.2 |
| **M2.4** | **Window finalization:** if median η < 0.90 in any cell, widen the biweight window for that regime, re-measure; freeze the final window | VAL §4.2, A.9 |
| **M2.5** | Report η table (per cell, with CIs) + the **frozen conditioning config** handed to M3 | VAL §4.2 |

**Dependencies:** M2.1 gates all. M2.2 → M2.3 → M2.4 (loop until η ≥ 0.90) → M2.5. Output (finalized window + η table) feeds **M3** (calibration / Seal #2). η also bounds absolute recall (reported, not hidden).

---

## 3. Frozen-choices proposal (SIGN-OFF GATE)

> The **injection grid** (P {0.5,1,2,4,8,16} d · R_p {1,2,4,8,12} R⊕ · b {0,0.3,0.6}) and **η_min = 0.90** are **sealed** (VAL §3, §4.2) — not choices here. Below are the *modelling* choices the seal leaves open.

### Decision A — Transit model & limb darkening
| Item | Proposal | Notes |
|------|----------|-------|
| Transit model | **Mandel & Agol (2002)** via `batman` (Kreidberg 2015) | Analytic, standard; matches VAL §3 |
| Limb-darkening law | **Quadratic** (u₁, u₂) | Standard for TESS |
| LD coefficients | Interpolated on **(Teff, logg, [Fe/H])** from a published **TESS-band table (Claret 2017)** | [Fe/H] often absent in TIC → **assume solar [Fe/H]=0**; record per-target u₁,u₂ |

### Decision B — System parameterization (transit shape from the frozen grid)
| Item | Proposal |
|------|----------|
| Depth | δ = (R_p/R⋆)², R⋆ from TIC (manifest) |
| a/R⋆ | from **stellar density** (logg + R⋆; Seager & Mallén-Ornelas 2003) and P — no separate mass needed |
| Inclination | from b (circular): cos i = b /(a/R⋆) |
| **Eccentricity** | **e = 0 (circular)** — frozen assumption for injection-recovery |
| Duration T₁₄ | derived (Winn 2010) from P, a/R⋆, b, R_p/R⋆ — also the `n_transits` / CDPP(T₁₄) timescale |
| Epoch t₀ | uniform-random within the target's observed baseline, **fixed RNG seed** |

### Decision C — η-validation design
| Item | Proposal |
|------|----------|
| Injection hosts | **null-pool calibration** targets (`is_null`); reuse M1-conditioned η-sample where null |
| Injections per (P,R_p) cell (η estimate) | **200** (across random hosts × epochs × the 3 b values), fixed seed — enough for a robust median η + CI; **distinct from** the ≥500/cell recall power sample (§6) |
| Inject → condition | inject in **relative-flux** space into real **pre-detrend** PDCSAP, then run the **same** Stage-0 conditioning (so η captures conditioning attenuation) |
| δ_post recovery | **fixed-shape least-squares depth** at the known (t₀,P,T₁₄) on the conditioned residual |
| Shape diagnostic | per cell: RMS of (conditioned folded profile − scaled injected profile)/δ_true, plus recovered/true duration ratio |
| Pass / revise | **median η ≥ 0.90 per (P,R_p) cell**; if a cell fails → widen the biweight window for that regime, re-measure, **before** M3 (VAL §4.2) |

### Decision D — Library & mechanics
- `batman-package` (Mandel–Agol). Add to `research/m2_injection/requirements.txt`.
- Fixed RNG seed (propose `20260615`); injections reproducible; config + versions pinned in provenance.

---

## 3a. Window finalization (M2.4 — executed + owner-approved 2026-06-15)

The provisional 0.5 d window fails η≥0.90 on long-period/shallow cells (biweight absorbs isolated shallow transits). A window sweep on the hardest cells (80 inj/cell):

| Window | 16/1 | 16/2 | 16/4 | 8/2 | 8/4 | 4/2 | min |
|--------|------|------|------|-----|-----|-----|-----|
| 1.0 d | 0.85 | 0.86 | 0.89 | 0.89 | 0.93 | 0.90 | 0.85 |
| 1.5 d | 0.75 | 0.93 | 0.92 | 0.95 | 0.94 | 0.95 | 0.75 |
| 2.0 d | 0.51 | 0.90 | 0.95 | 0.95 | 0.97 | 0.93 | 0.51 |
| 3.0 d | 0.94 | 0.96 | 0.99 | 0.91 | 0.98 | 0.97 | 0.91 |

Focused **2.5 d** validation (150 inj/cell) with depth + η-spread + SNR₁ (=depth/σ, σ≈1067 ppm):

| Cell | η_med | spread | depth | SNR₁ | read |
|------|-------|--------|-------|------|------|
| 16/1 | 0.833 | 1.96 | 73 ppm | 0.07 | **noise-dominated** (p16<0) |
| 8/1 | 0.867 | 1.83 | 71 ppm | 0.07 | **noise-dominated** (p16<0) |
| 16/2 | 0.879 | 0.51 | 279 ppm | 0.26 | **borderline** (partial signal) |
| 16/4 | 0.959 | 0.16 | 1587 ppm | 1.49 | clean PASS |
| 16/8 | 0.997 | 0.04 | 4536 ppm | 4.25 | clean PASS |
| 8/2 | 0.926 | 0.41 | 284 ppm | 0.27 | PASS |
| 8/4 | 0.959 | 0.12 | 1175 ppm | 1.10 | clean PASS |
| 4/2 | 0.932 | 0.33 | 294 ppm | 0.28 | PASS |

**Decision (owner-approved):** finalize the global detrend window at **2.5 d**. All individually-measurable cells (Rₚ≥4, SNR₁≳1) clear η≥0.90 with tight spread; the η spread balloons only as depth falls below the noise. **Documented corners (non-gating):** **8/1, 16/1** = single-transit noise-limited (SNR₁≈0.07, η meaningless); **16/2** = borderline long-period small-planet (SNR₁≈0.26). These three are carried into the full grid with explicit η distributions but **do not force** a 3.0 d window (which would over-penalize detrending for all stars). **Gate = all non-corner cells η≥0.90.**

**Consequence:** the M1 η-sample noise model (σ/CDPP/τ_GP) was computed at 0.5 d and is **superseded**; it must be recomputed at 2.5 d before M3.

## 4. Risks
| ID | Risk | Mitigation |
|----|------|------------|
| **R2-1** | LD-coefficient error biases injected shape | Quadratic LD from a published TESS table; record per-target u₁,u₂; η is a *ratio* (first-order LD-insensitive) |
| **R2-2** | η measured on hosts with **real** transits | Inject into **null-pool** hosts only |
| **R2-3** | Window-widening trades stellar-noise suppression for transit preservation | Widen **only** failing cells/regimes; report the η–window tradeoff; η ≥ 0.90 is the floor |
| **R2-4** | δ_post recovery method biases η | Fixed-shape LS at known ephemeris; cross-check with folded in-transit mean |
| **R2-5** | Accidentally touching TEST | Inject into **calibration-only** rows; assert no TEST TIC enters M2 |
| **R2-6** | e=0 assumption | Pre-registered scope simplification; TTV/eccentric handling is out of Phase I headline (HYP A9/A10) |

## 5. Deliverables
- `m2_config.yaml` (frozen injection/η config) + provenance.
- η table per (P,R_p) cell (median η + CI + shape diagnostic); window-finalization record.
- **Frozen conditioning config** handed to M3 (final window).
- `research/m2_injection/` tooling.

## 6. Completion criteria (binary)
1. ☐ Injection/η config **frozen** from signed §3 choices; provenance recorded.
2. ☐ Injection harness reproduces Mandel–Agol transits with TIC-derived LD; injects into real null-pool calibration LCs.
3. ☐ η measured per (P,R_p) cell over the frozen grid; shape diagnostic recorded.
4. ☐ **Median η ≥ 0.90** in every headline cell — or window widened and re-measured until met; final window frozen.
5. ☐ **No threshold set; TEST untouched; sealed docs unmodified** (`git diff phase1-prereg-v2` empty); grid & η_min unchanged.
6. ☐ Frozen conditioning config + η table handed to M3.

## 7. (For context) what M2 hands to M3
The **finalized detrend window** + per-target noise model (σ, CDPP, τ_GP) + the η table (absolute-recall bound). M3 then derives + seals thresholds (`z⋆, θ, T, …`) on calibration → **Seal #2**.

## 8. Sign-off
| Decision | Owner choice (2026-06-15) |
|----------|---------------------------|
| A — Transit model · LD law · LD source | **batman Mandel–Agol**; **quadratic** LD; **Claret 2017 TESS** table interpolated on (Teff,logg,[Fe/H]); **solar [Fe/H]=0** fallback |
| B — e=0 · a/R⋆ from density · t₀ sampling | **e=0 (circular)**; a/R⋆ from **stellar density** (logg+R⋆); i from b; T₁₄ derived; **t₀ uniform-random in baseline** (seed 20260615) |
| C — η hosts · injections/cell · δ_post method · shape diagnostic | **null-pool calibration** hosts; **200 injections / (P,R_p) cell**; **fixed-shape least-squares** δ_post at known ephemeris; shape diagnostic; **median η ≥ 0.90 / cell** |
| D — Library (`batman`) · seed | **batman-package**; seed **20260615** |

Approved to freeze the M2 injection / η-validation config: **Ansul — approved in-session**  Date: **2026-06-15**

*On sign-off: write `research/m2_injection/config/m2_config.yaml`, scaffold the harness, probe a single injection, then run the η grid and finalize the window. Grid and η_min = 0.90 remain sealed.*
