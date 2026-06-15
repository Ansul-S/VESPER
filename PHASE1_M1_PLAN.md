# Phase I — M1 Plan & Conditioning Choices

| Field | Value |
|-------|-------|
| **Document** | M1 execution plan + conditioning frozen-choices proposal |
| **Increment** | **v0.1 — M1 only** (Stage-0 Conditioning) |
| **Created** | 2026-06-15 |
| **Status** | **SIGNED OFF** (owner, 2026-06-15) — biweight detrend + celerite2 noise model, η-sample first; config frozen in `m1_config.yaml`; executing M1 |
| **Builds on** | M0 (Seal #1 `1f2d49e1…`; manifest = release asset `m0-manifest-v1`) |
| **Authority** | Subordinate to the sealed pre-registration (`phase1-prereg-v2`). Executes VAL A.9 / §4.2; changes nothing in the sealed docs. |

> **What M1 is.** The first **flux-touching** milestone: download SPOC 2-min light curves for the **calibration** pool and apply **Stage-0 conditioning** — per-sector detrend + masking → zero-centred residual `r(t)` — plus a per-target **noise model** (σ, CDPP, τ_GP) that downstream stages require. Conditioning is **shared by both arms**, so it precedes and is independent of routing (the fairness keystone).
>
> **Frozen choice (why sign-off).** VAL A.9 freezes the detrend "kernel and window … exact `wotan`/`celerite2` parameters." The method materially affects recall — **over-aggressive detrending is the known recall sink** (A8 / risk R-5). So M1 proposes the conditioning config for your sign-off (§4); the window is then **finalized by the η ≥ 0.90 transit-preservation check** (VAL §4.2), which is M2 and gates M3. Per non-negotiable #2, the config is frozen **before** thresholds and revised (if η < 0.90) **before** any threshold is set — never after.

---

## 1. Scope & boundary

**M1 does:** freeze the conditioning config (§4, post sign-off); retrieve SPOC 2-min PDCSAP_FLUX for the **calibration** split (or an η-validation sample first); run Stage-0 conditioning (detrend + momentum-dump/quality/scattered-light masking → `r(t)`); fit the per-target noise model (celerite2 GP → σ, CDPP(T₁₄), τ_GP); record residual stationarity/whiteness diagnostics (checks A2, A4).

**M1 does NOT:** touch the **TEST** split (sealed until M4 — G1); set any detection threshold (`z⋆, θ, T, …` are M3 / Seal #2 — G2); run the detector, period inference, or TLS (M2+); run the η check itself (M2, though M1 produces its inputs); modify any sealed document; build Phase II machinery.

**Inputs:** the M0 manifest (calibration rows only), via the release asset or local regeneration. **Data volume note:** the calibration pool is 6,925 targets — full retrieval is large; §4 Decision D proposes conditioning an **η-validation sample first**, then scaling.

---

## 2. Decomposition (M1.1 → M1.5)

| Sub-step | Task | Sealed basis |
|----------|------|--------------|
| **M1.1** | Freeze the conditioning config (method, window, masks, noise model) from the signed §4 choices → `m1_config.yaml` | VAL A.9 |
| **M1.2** | Retrieve SPOC 2-min PDCSAP_FLUX for calibration targets (or the η-sample); cache locally (gitignored) | VAL §3 |
| **M1.3** | Stage-0 conditioning: per-sector detrend + momentum-dump (~2.5 d) + SPOC quality-flag + scattered-light masking → zero-centred `r(t)` | VAL A.9; MATH §0/§2 |
| **M1.4** | Per-target noise model: fit celerite2 GP to `r(t)` → σ, **CDPP(T₁₄)**, **τ_GP** (for A.8 block bootstrap) | MATH §2, §9.1; VAL A.8 |
| **M1.5** | Residual diagnostics: stationarity + whiteness post-conditioning (checks A2, A4); per-target QA table | HYP A2, A4 |

**Dependencies:** M1.1 gates all (config first). M1.2 → M1.3 → M1.4 → M1.5. The **η check (M2)** consumes M1.3/M1.4 and finalizes M1.1's window. M3 calibration consumes M1.4 (σ/τ_GP).

---

## 3. Provisional conditioning recipe (for context; numerics frozen at §4 sign-off)

Zero-centred conditioned residual, transit = **negative** excursion (MATH §0). Single-transit significance uses CDPP(T₁₄) (MATH §2); the GP noise model upgrades white-noise CDPP to Σ on transit timescales (MATH §11) and supplies τ_GP for the block bootstrap (MATH §9.1, VAL A.8).

---

## 4. Conditioning frozen-choices proposal (SIGN-OFF GATE)

All choices are outcome-independent (set before detection); the window is η-finalized on **calibration** data before M3.

### Decision A — Detrending method
| Option | Description | Verdict |
|--------|-------------|---------|
| **A1. `wotan` biweight time-windowed slider** | Robust Tukey-biweight slider; the wotan benchmark's best detrender for planet discovery (recovers 99 %/94 % of the shallowest Kepler/K2 planets). Simple, transit-preserving, no per-star fitting. | ✓ **Recommended** (lowest recall risk; matches Phase I "simple") |
| **A2. GP / `celerite2` detrend** | Fit + subtract a stellar-variability GP. Better on highly active stars, but **risks absorbing transits** (η sink) and is heavier. | ◐ Reserve for active-star subset; default off |

**Recommendation: A1 (biweight)** for the Stage-0 detrend, with the GP used as the **noise model** (Decision C), not the detrender.

### Decision B — Window length & masking
- **Window:** start **0.5 d** (≫ max T₁₄ in the grid, to preserve depth), **η-finalized** per (P,R_p) cell — widened where η < 0.90 (VAL §4.2). `break_tolerance` to avoid bridging gaps.
- **Masks:** momentum dumps (~2.5 d cadence, S1–S3); **SPOC quality-flag** bitmask (default hard bits); scattered-light/anomaly flags.

### Decision C — Noise model (σ, CDPP, τ_GP)
- **`celerite2` GP** (e.g. SHOTerm / Matérn-3/2) fit to the conditioned residuals → per-target σ, CDPP(T₁₄), and **τ_GP** (block-bootstrap block length, VAL A.8). Recommended.

### Decision D — M1 data scope
- **Condition an η-validation sample first** (e.g. a few ×10² calibration targets spanning the grid), confirm the pipeline + η behaviour, **then scale** to the full calibration pool. Recommended (avoids a multi-GB blind download).

---

## 5. Risks

| ID | Risk | Mitigation |
|----|------|------------|
| **R1-1** | Over-aggressive detrend attenuates transits (η < 0.90) — recall sink (A8/R-5) | Wide biweight window; η check (M2) gates + revises **before** M3 |
| **R1-2** | GP noise model **absorbs** transits → biased σ/CDPP | GP is noise-model only (not detrender); fit on transit-masked residuals where applicable |
| **R1-3** | Download volume/time for 6,925 calibration LCs | η-sample first (Decision D); cache; resumable retrieval |
| **R1-4** | Gap/momentum-dump bridging distorts residuals | `break_tolerance` + explicit masks; stationarity diagnostic (M1.5) |
| **R1-5** | Accidentally touching TEST split | Pipeline reads **calibration-only** rows from the manifest; assert no TEST TIC enters M1 |

## 6. Deliverables
- `m1_config.yaml` (frozen conditioning config) + provenance.
- Conditioned residuals `r(t)` + per-target noise model (σ, CDPP, τ_GP) for the η-sample (then full calibration), cached (gitignored); summary table tracked.
- M1.5 diagnostics table (stationarity/whiteness).
- `research/m1_conditioning/` tooling.

## 7. Completion criteria (binary)
1. ☐ Conditioning config **frozen** from signed §4 choices; recorded with provenance.
2. ☐ Calibration LCs retrieved (η-sample ✓, then full pool); **no TEST target touched**.
3. ☐ Stage-0 conditioning produces zero-centred `r(t)` with masks applied.
4. ☐ Per-target noise model yields σ, CDPP(T₁₄), τ_GP.
5. ☐ Stationarity/whiteness diagnostics recorded (A2/A4).
6. ☐ **No threshold set; TEST untouched; sealed docs unmodified** (`git diff phase1-prereg-v2` empty).
7. ☐ (Hands off to M2) η inputs ready; window finalization deferred to the M2 η ≥ 0.90 check.

## 8. Sign-off
| Decision | Owner choice (2026-06-15) |
|----------|---------------------------|
| A — Detrend method | **wotan biweight time-windowed slider** |
| B — Window · masks | window **0.5 d** start (η-finalized at M2); momentum-dump (~2.5 d) + SPOC default quality bitmask + scattered-light masks |
| C — Noise model | **celerite2 GP** (SHOTerm) → σ, CDPP(T₁₄), τ_GP |
| D — M1 data scope | **η-validation sample first** (200 calibration targets, seed 20260615), then scale to the full calibration pool |

Approved to freeze the M1 conditioning config: **Ansul — approved in-session**  Date: **2026-06-15**

*On sign-off: write `research/m1_conditioning/config/m1_config.yaml`, scaffold the pipeline, condition the η-sample, then scale. The window is η-finalized at M2 before any M3 threshold.*
