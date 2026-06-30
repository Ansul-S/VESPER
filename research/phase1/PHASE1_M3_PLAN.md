# Phase I — M3 Plan & Threshold-Calibration Frozen Choices

| Field | Value |
|-------|-------|
| **Document** | M3 execution plan + threshold-calibration frozen-choices proposal |
| **Increment** | **v0.1 — M3 only** (build untrained search machinery → calibrate thresholds on CALIBRATION → **Seal #2**) |
| **Created** | 2026-06-16 |
| **Status** | **✅ DONE — Seal #2 recorded (2026-06-16).** §4 choices A–G signed; machinery built; calibrated on cleaned CALIBRATION-null (854); null-pool contamination found + cleaned (owner-directed); thresholds bootstrap-stable; w_c/π̂ instantiated; **Seal #2 `6292c018…`** (owner-approved). TEST untouched. Next: **M4** single sealed-TEST run. |
| **Builds on** | M0 (Seal #1 `1f2d49e1…`), M1 (Stage-0 conditioning), **M1 noise model recomputed at the finalized 2.5 d window** (`data/manifests/m1/m1_noise_summary.csv`, 188/188; 0.5 d archived under `superseded_0.5d/`), M2 (η gate PASS; window 2.5 d) |
| **Authority** | Subordinate to the sealed pre-registration (`phase1-prereg-v2`). Executes VAL Appendix A.1–A.10. Changes nothing in the sealed docs. |

> **What M3 is.** Build the **simple, untrained** search machinery the protocol assumes — the GP-whitened matched-filter **detector** (MATH §2), **period-from-spacing** inference (MATH §4), the **shared TLS confirmation engine** (Arm A *and* Arm B; VAL A.1), and the **block-bootstrap FAP** (MATH §9.1) — then **derive and freeze on the CALIBRATION set** every `[sealed at M3]` value: $z_\star,\ \theta,\ z_{\rm mono},\ T,\ \alpha_{\rm FAP},\ \varepsilon$ (with $N_{\min}=2$ fixed), plus the calibration-derived per-target $\tau_{\rm GP}$/block lengths, and instantiate the frozen occurrence weights $w_c$ (A.5) and prevalence $\hat\pi$ (A.6). Hash all of it → **Seal #2** (A.10), recorded before the single M4 test run.
>
> **Why sign-off first.** The untrained-detector definition, TLS baseline config, and every calibration *target/procedure* are frozen **before** any threshold is computed (non-negotiable #2). This document proposes them; **nothing is calibrated or sealed until §10 is signed.**

---

## 1. Scope reconciliation (read first)

The forward map in `PHASE1_EXECUTION_PLAN.md` §2 bundled "the simple untrained detector; period-from-spacing; shared TLS engine" into M2's one-line scope. **M2 as executed delivered only the injection harness + η transit-preservation check** (its sealed deliverable). Therefore the detector, period-from-spacing, TLS engine, and bootstrap are **built in M3**, immediately before the calibration that needs them. This is a reading of *where the work lands*, not a change to the sealed protocol: all components remain **untrained** (no learned models — Working Agreement), and thresholds are still derived on CALIBRATION only and sealed before M4.

---

## 2. Scope & boundary

**M3 does:** build the untrained detector, period-from-spacing, shared TLS engine, and block-bootstrap (frozen configs); run them on **null-pool CALIBRATION** stars only; derive each `[sealed at M3]` threshold to its sealed target; instantiate $w_c$, $\hat\pi$; record the A.7 runtime machine; assemble the **threshold manifest** and compute its content hash (**Seal #2**); verify anti-tuning invariants.

**M3 does NOT:** touch the **TEST** split (sealed until M4 — G1); run any recovery/recall/compute *measurement* (that is M4/M5); change the **frozen grid, $\eta_{\min}=0.90$, $N_{\min}=2$, the F6 weight formula, or the A.8 block-length formula** (sealed); build any learned model, classifier, or Phase II clean-skip; modify any sealed document.

**Data scope:** CALIBRATION rows only. Thresholds are set on the **null (planetless) calibration pool** (`is_null`, 22,458-derived calibration subset); injection-recovery measurement is M4. The η-sample's 188 conditioned residuals are reused where applicable; full-pool calibration conditioning is run on demand (open question carried from M2).

---

## 3. Decomposition (M3.1 → M3.7)

| Sub-step | Task | Sealed basis |
|----------|------|--------------|
| **M3.1** | Freeze the M3 config (§4 choices, post sign-off) → `m3_config.yaml`; pin TLS engine + version | VAL A.1–A.9 |
| **M3.2** | **Detector** — GP-whitened matched filter $s(t)=g^{\mathsf T}\Sigma^{-1}r/\sqrt{g^{\mathsf T}\Sigma^{-1}g}$; event extraction; $\Sigma$ from the M1 (2.5 d) noise model | MATH §2; A.3, A.9 |
| **M3.3** | **Period-from-spacing** (MATH §4) + **block-bootstrap FAP** (MATH §9.1); block length $L_b=3\max(\tau_{\rm GP},T_{14})$ | MATH §4, §9.1; A.8 |
| **M3.4** | **Shared TLS engine** (A.1) — identical config for both arms; targeted (Arm B, window $\varepsilon$) and full (Arm A) modes | VAL A.1, §4 |
| **M3.5** | **Calibrate on null CALIBRATION stars** → $T$ (FAR ≤ 1 %/star), $z_\star$ (≤ 1 false event/LC), $z_{\rm mono}$, $\theta$, $\alpha_{\rm FAP}$, $\varepsilon$ | VAL A.2, A.3, A.8 |
| **M3.6** | Instantiate frozen $w_c$ (A.5) + $\hat\pi$ (A.6) from Kunimoto & Matthews (2020) over the grid; record A.7 machine | VAL A.5, A.6, A.7 |
| **M3.7** | Assemble threshold manifest; compute content hash → **Seal #2**; anti-tuning audit | VAL A.10; non-neg. #2 |

**Dependencies:** M3.1 gates all. M3.2 → M3.3 (period FAP consumes detector events) and M3.4 are parallel; M3.5 needs M3.2–M3.4. M3.6 is independent (metadata + literature). M3.7 last. Calibration (M3.5) runs only after §10 sign-off.

---

## 4. Frozen-choices proposal (SIGN-OFF GATE)

> **Sealed, not choices here:** injection grid; $\eta_{\min}=0.90$; $N_{\min}=2$; the F6 weight *formula* (A.5); the $\hat\pi$ *formula* (A.6); the block-length *formula* $L_b=3\max(\tau_{\rm GP},T_{14})$ (A.8); FAR/false-event *targets* (A.2/A.3). Below are the *method + value* choices the seal leaves open. Targets are sealed; the **numeric thresholds achieving them** are derived on calibration *after* sign-off.

### Decision A — Detector (untrained matched filter, MATH §2)
| Item | Proposal | Notes |
|------|----------|-------|
| Statistic | **GP-whitened matched filter** $s=g^{\mathsf T}\Sigma^{-1}r/\sqrt{g^{\mathsf T}\Sigma^{-1}g}$ | Neyman–Pearson optimal; MATH §2 red-noise form |
| Whitening $\Sigma$ | **celerite2 SHOTerm** from the M1 **2.5 d** noise model ($\sigma$, $\tau_{\rm GP}$ per target) | reuses the recomputed model; no per-LC refit of the kernel |
| Template $g$ | **box** of width $T_{14}$ over a frozen **duration grid** (propose $T_{14}\in\{0.05,0.1,0.2,0.4,0.8\}$ d) | untrained; limb-darkened template deferred (box is the conservative Phase I choice) |
| Event declaration | $s(t)<-z_\star$ (noise-normalized); cluster contiguous crossings; one event per local minimum | MATH §2 eq. (event extraction) |
| $z_\star$ target | **≤ 1 expected false event per null LC** (A.3) — derived on null calibration LCs | sealed target; value `[derive at M3.5]` |

### Decision B — Routing & monotransit ($\theta$, $N_{\min}$, $z_{\rm mono}$)
| Item | Proposal |
|------|----------|
| Multi-event fast path | iff $\ge N_{\min}$ events with $N_{\min}=2$ (**sealed**) above $z_\star$ |
| Monotransit branch | single event with $\mathrm{SNR}_1\ge z_{\rm mono}$, $z_{\rm mono}>z_\star$; **weaker FP control**, reported separately (MATH §6) |
| $z_{\rm mono}$ target | propose set so monotransit false-event yield on null LCs ≤ a stated small rate (e.g. ≤ 0.1/LC); value `[derive at M3.5]` |
| $\theta$ | the operational routing predicate = (B multi-event rule) ∨ (monotransit rule); recorded, not a free scalar |

### Decision C — Period-from-spacing + bootstrap FAP (MATH §4, §9.1; A.8)
| Item | Proposal |
|------|----------|
| Inference | from event spacings $\hat t_j-\hat t_i=m_{ij}P$; integer-comb / GCD-style $\hat P$ over the frozen period grid |
| FAP null | **noise-model-aware circular block bootstrap**; $L_b=3\max(\tau_{\rm GP},T_{14})$ (**sealed formula**); **$B=1000$** surrogates (propose; A.8 requires ≥1000) |
| $\alpha_{\rm FAP}$ target | propose a null-exceedance target (e.g. **1 %**) verified on null stars (H4); value `[derive at M3.5]` |

### Decision D — Shared TLS engine (A.1, the fairness keystone)
| Item | Proposal |
|------|----------|
| Engine | **`transitleastsquares`** (Hippke & Heller 2019), pinned version; **identical config in both arms** |
| Period grid | $P\in[0.5,\ \le\!\tfrac12 T_{\rm base}]$ d, default TLS optimal-frequency sampling (oversampling factor frozen, propose 3) |
| Duration / LD | TLS default transit-shape model with TESS quadratic LD (Claret 2017, as M2) |
| SDE definition | TLS Signal Detection Efficiency, as published; **single common threshold $T$** both arms |
| Arm A (full) vs Arm B (targeted) | A = full grid; B = narrow window $[\hat P(1-\varepsilon),\hat P(1+\varepsilon)]$ around the inferred period |

### Decision E — Fast-path window $\varepsilon$ + common threshold $T$
| Item | Proposal |
|------|----------|
| $\varepsilon$ | half-width of Arm B's targeted period window; propose **$\varepsilon=0.01$** (±1 % of $\hat P$, matched to the A.4 recovery tolerance), value confirmed at M3.5 against null-star period scatter |
| $T$ target | TLS SDE threshold s.t. empirical **FAR ≤ 1 %/star** on null calibration stars (A.2); value `[derive at M3.5]` |

### Decision F — Occurrence weights & prevalence ($w_c$, $\hat\pi$)
| Item | Proposal |
|------|----------|
| Source | **Kunimoto & Matthews (2020)** occurrence framework (sealed A.5/A.6); pin in `references.bib` |
| $w_c$ | $w_c\propto w_P(P)w_R(R_p)$ over eligible cells, normalized $\sum w_c=1$ — computed from the frozen formula |
| $\hat\pi$ | (occurrence over grid support) × (geometric $\langle R_\star/a\rangle$), single frozen scalar; used for E3 only (secondary) |

### Decision G — Runtime machine (A.7) & mechanics
- One specified machine: record **CPU model, cores, clock**; single-thread **CPU-core-seconds**; ≥5 repeats, warm cache (compute is measured at M4/M5, but the machine is fixed and recorded now).
- Detector overhead $\rho_d$ harness defined now, measured at M4/M5.
- Fixed RNG seed (propose `20260616`); configs + library versions pinned in provenance.

---

## 5. Calibration procedure (executed only after sign-off; CALIBRATION-only)
1. Condition the null-pool calibration stars at the frozen 2.5 d window (reuse 188 η-sample; extend on demand).
2. Run the detector on each null LC → empirical false-event distribution → set **$z_\star$** at the ≤1-false-event/LC target; set **$z_{\rm mono}$** at its target.
3. Run period-from-spacing + block bootstrap on null LCs → set **$\alpha_{\rm FAP}$** at its null-exceedance target; verify empirical FAR ≤ target (H4).
4. Run TLS on null calibration stars → SDE null distribution → set **$T$** at FAR ≤ 1 %/star.
5. Fix **$\varepsilon$** from the inferred-period scatter on injected calibration hosts (recovery within ±$\varepsilon$).
6. Record every value, the null-star empirical rates achieved, and reliability diagrams (ECE).

> **No TEST row is read. No injection-recall or compute number is produced.** Those are M4/M5.

---

## 6. Risks
| ID | Risk | Mitigation |
|----|------|------------|
| **R3-1** | Calibrating a threshold against a statistic that "by construction exceeds $z_\star$" (the v3 circularity, MATH §9 ¶3) | Significance arbiter is **TLS SDE ≥ T** (physics), never the detector/coherence score; FAP from block bootstrap, not phase-scramble |
| **R3-2** | Wider 2.5 d window inflates CDPP → $z_\star$/$T$ set against noisier residuals, depressing small-planet recall | Documented tradeoff (η ≥ 0.90 floor already paid); thresholds set to **honest** noise; small-planet bound reported, not hidden (M2 Rₚ=1 finding) |
| **R3-3** | TLS engine/version drift breaks the both-arms fairness keystone | Pin engine + version + config hash; identical engine object both arms; recorded in Seal #2 |
| **R3-4** | Accidental TEST access during null-star calibration | Assert `split==calibration` and `is_null` on every row; reuse the M1 guard (`load_config` rejects TEST + threshold keys) |
| **R3-5** | Block bootstrap under-rejects/over-rejects under red noise | $L_b=3\max(\tau_{\rm GP},T_{14})$ sealed; verify empirical FAR on null stars (H4) before trusting $\alpha_{\rm FAP}$ |
| **R3-6** | Premature sealing before sign-off | §10 gate; no `m3_config.yaml` written, no calibration run, until signed |

## 7. Deliverables
- `research/m3_calibration/` tooling (detector, period-from-spacing, TLS wrapper, bootstrap, calibration driver) + `requirements.txt` (pin `transitleastsquares`).
- `m3_config.yaml` (frozen, post sign-off) + provenance.
- Null-calibration threshold report: $z_\star, z_{\rm mono}, \theta, T, \alpha_{\rm FAP}, \varepsilon$ + achieved null rates + reliability diagrams.
- $w_c$ table + $\hat\pi$ scalar (A.5/A.6) + A.7 machine record.
- **Threshold manifest + content hash (Seal #2)** recorded before M4.

## 8. Completion criteria (binary; all must hold) — ✅ M3 DONE (2026-06-16)
1. ☑ Untrained detector, period-from-spacing, shared TLS engine, block bootstrap built to the frozen §4 configs (`research/m3_calibration/`).
2. ☑ $z_\star, z_{\rm mono}, T, \alpha_{\rm FAP}, \varepsilon$ derived on **null CALIBRATION** stars (cleaned 854) to their sealed targets; achieved null rates + bootstrap CIs recorded.
3. ☑ $w_c$, $\hat\pi$ instantiated from the frozen K&M (2020) formulae; A.7 machine recorded (Apple M4, 10 cores).
4. ☑ **Seal #2** (threshold manifest hash) computed + recorded **before** any M4 access.
5. ☑ TEST untouched (0 TEST TICs in any M3 artifact); sealed docs unmodified (`git diff phase1-prereg-v2` empty); grid/$\eta_{\min}$/$N_{\min}$/formulae unchanged.

### 8a. Null-pool cleaning (executed; owner-directed) — derived M3 calibration subset
First null calibration surfaced **EB/variable contamination** inflating $T$ and $z_{\rm mono}$ ($z_\star$ robust). Resolved by **Prša et al. 2022 (TESS EB) + VSX** cross-match (132 excluded) + automated EB vetting — secondary-eclipse / odd-even / depth (14 excluded) → **146 excluded → cleaned 854** of 1000. M0 null definition **preserved**; exclusions in `data/manifests/m3/calibration_exclusions.csv`; **31 retained high-SDE survivors audited** (`retained_high_sde_audit.csv`). Bootstrap (B=1000) CIs: $z_\star$ 3.4 [3.30,3.40], $z_{\rm mono}$ 5.3 [5.0,5.8], $T$ 10.74 [9.74,11.34].

### 8b. Seal #2 record (owner-approved 2026-06-16)
- **Seal #2 (threshold manifest content hash, SHA-256): `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** — distinct from Seal #1 (`1f2d49e1…`). Verify: `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.
- **Sealed values:** $z_\star=3.4$ · $z_{\rm mono}=5.3$ · $N_{\min}=2$ · $T=10.74$ · $\alpha_{\rm FAP}=1\%$ (null exceedance 1.08%) · $\varepsilon=0.01$; A.5 $w_c$ (92.8% on $R_p\le2$); A.6 $\hat\pi=3.17\%$; A.1 TLS 1.32; A.7 machine; A.8 bootstrap; A.9 conditioning (2.5 d).
- **A.10 reference:** this is the VAL Appendix A.10 manifest hash for M3, recorded before M4. The sealed pre-registration docs (`phase1-prereg-v2`) are **not** modified.
- **Expected-evaluation note (non-parametric):** the occurrence-weighted E1 evaluation is expected to be **dominated by the $R_p\le2\,R_\oplus$ population** — the K&M (2020) weighting puts ~92.8% of $w_c$ on $R_p\le2$ ($R_p=1$ alone ~36.3%), combined with the empirically observed M2 detectability limit of Earth-radius single-transit signals (noise-limited $R_p=1$ row); recovery of that population relies on the full-TLS fallback (folding), not single-transit conditioning. Recorded in `SEAL2_RECORD.json` **outside** the hashed core (no sealed value altered).
- **Sign-off:** Ansul — explicit in-session approval, 2026-06-16.

## 9. (For context) what M3 hands to M4
The frozen, hashed threshold manifest (**Seal #2 `6292c018…`**) + the built untrained machinery. M4 runs the **single sealed TEST evaluation** → primary endpoints E1 (recall non-inferiority) and E2 (scoped compute). TEST stays sealed until that run.

## 10. Sign-off
| Decision | Owner choice (2026-06-16) |
|----------|---------------------------|
| A — Detector statistic · whitening · template · $z_\star$ target | **GP-whitened matched filter; box template; duration grid {0.05,0.1,0.2,0.4,0.8} d; $z_\star$ → ≤1 false event/LC** |
| B — Routing · $N_{\min}=2$ · $z_{\rm mono}$ | **$N_{\min}=2$; calibrate $z_{\rm mono}$ to ≤0.1 false alarms/LC** |
| C — Period-from-spacing · bootstrap $B$ · $\alpha_{\rm FAP}$ target | **integer-comb; circular block bootstrap; $B=1000$; $\alpha_{\rm FAP}$ target = 1 %** |
| D — TLS engine · period grid · SDE · both-arms config | **pin `transitleastsquares`; full optimal-frequency grid; oversampling = 3; identical both arms; NO BLS substitute** |
| E — $\varepsilon$ · $T$ target (FAR ≤ 1 %/star) | **$\varepsilon=0.01$; calibrate $T$ to FAR ≤ 1 %/star** |
| F — $w_c$ · $\hat\pi$ (Kunimoto & Matthews 2020) | **sealed Kunimoto & Matthews (2020) formulation** |
| G — Runtime machine · seed · version pinning | **record machine spec + versions; seed `20260616`** |

Approved to freeze the M3 config and proceed to calibration: **Ansul — approved in-session**  Date: **2026-06-16**
**Condition:** no threshold derivation is final and **no Seal #2** is created until the calibration outputs are presented and reviewed.

*On sign-off: write `research/m3_calibration/config/m3_config.yaml`, build the untrained machinery, calibrate on null CALIBRATION stars only, then assemble + hash the threshold manifest (Seal #2). Grid, $\eta_{\min}$, $N_{\min}$, and the A.5/A.6/A.8 formulae remain sealed. TEST stays sealed until the single M4 run.*

*References: VAL = `docs/VESPER_PHASE1_VALIDATION.md` v2 (Appendix A); MATH = `docs/VESPER_MATHEMATICAL_FOUNDATIONS.md` v1.1; HYP = `docs/SCIENTIFIC_HYPOTHESIS.md` v2.0.*
