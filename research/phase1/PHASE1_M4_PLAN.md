# Phase I — M4 Plan: The Single Sealed-TEST Run (E1 + E2)

| Field | Value |
|-------|-------|
| **Document** | M4 execution plan — the one allowed read of the TEST split |
| **Increment** | **v0.1 — M4 only** (apply frozen machinery + Seal #2 thresholds to TEST exactly once → primary endpoints E1, E2; collect raw E3/π⋆ inputs for M5) |
| **Created** | 2026-06-18 |
| **Status** | **DRAFT — awaiting sign-off (§10) to execute.** Scope confirmed with owner 2026-06-18 (run scope, conditioning breadth, E2 timing). No TEST row read until §10 is signed. |
| **Builds on** | M0 (Seal #1 `1f2d49e1…`), M1 (Stage-0 conditioning, 2.5 d noise model), M2 (η gate PASS, window 2.5 d), **M3 (Seal #2 `6292c018…`)** |
| **Authority** | **Execution-only.** Subordinate to the sealed pre-registration (`phase1-prereg-v2`) and Seal #2. **Introduces no new frozen parameter.** Reuses `research/m3_calibration/` machinery and the Seal #2 manifest verbatim. Changes nothing in any sealed document. |

> **What M4 is.** Apply the **already-frozen** untrained machinery (detector → routing → period-from-spacing + block-bootstrap → shared TLS) and the **Seal #2 thresholds** to the **TEST split**, **exactly once**, to compute the two **primary** endpoints — **E1** (occurrence-weighted recall non-inferiority vs full TLS) and **E2** (scoped compute on the fast-path-eligible population, ρ_d included) — and to collect, in the same sealed execution, the raw per-star artifacts M5 needs for **E3/π⋆**. **E3 is not computed or interpreted at M4** (M5 is the analysis stage).
>
> **Why this is not tuning.** Every threshold, weight, prevalence, conditioning, bootstrap, and detector-config value is loaded **read-only** from the Seal #2 manifest. M4 sets nothing. The single TEST read is irreversible, so the entire pipeline is validated end-to-end on CALIBRATION/synthetic data **before** TEST is touched (§7). Non-negotiable #2 (no tuning on test data) and #4 (benchmark everything) govern.

---

## 1. Scope & boundary

**M4 does:**
- Build the **TEST injection set** on the sealed grid (§3), injecting Mandel–Agol transits into **raw** TEST PDCSAP flux, then conditioning at the frozen **2.5 d** window (η paid identically in both arms).
- Run the **dual-arm** comparison with the **shared, pinned `transitleastsquares` 1.32** engine (A.1 fairness keystone): **Arm A** = full-grid TLS (baseline); **Arm B** = combined evidence-first system (detector → routing → period seed → targeted TLS, full-TLS fallback when not fast-path-eligible).
- Apply the **operational recovery predicate** (VAL §4.1) identically to both arms.
- Compute **E1** (w_c-weighted $\overline{\Delta R}$ + one-sided 95% CI) and **E2** (compute ratio on the fast-path-eligible population, ρ_d included).
- Process a **survey-representative** set of non-injected, TOI-removed real TEST LCs to capture the **per-star compute + routing ledger** required for E3/π⋆ — **collected only**, not interpreted (M5).
- Freeze all M4 outputs into a content-hashed **M4 results artifact** (`data/manifests/m4/`).

**M4 does NOT:**
- Change any Seal #2 value, the injection grid, η_min, N_min, w_c, π̂, the block-length formula, ε, T, z⋆, z_mono, α_FAP, the TLS config, or the conditioning window. **Any such change requires a new pre-registration, not an edit.**
- Compute or interpret **E3/π⋆** (M5), the reality-check on real TOIs/EBs (M6), or the final verdict (M7).
- Build any learned model, classifier, dashboard, or Phase II clean-skip.
- Read TEST more than once. The single execution produces every artifact downstream milestones need.

**Data scope (owner-confirmed 2026-06-18):**
- **Run scope:** the single TEST read captures **(a)** injection-set outputs for E1, **(b)** compute ledgers for E2, and **(c)** survey-sample ledgers required for E3/π⋆ — all from the same sealed execution. E3 is *not* computed during M4.
- **Conditioning breadth:** condition **only what the run consumes** (injection hosts + survey-sample stars), not all 15,798 TEST targets.

---

## 2. Frozen inputs (loaded read-only from Seal #2 — not re-derived)

| Symbol | Value | Source |
|--------|-------|--------|
| z⋆ (detector event threshold) | **3.4** | Seal #2 |
| z_mono (monotransit) | **5.3** | Seal #2 |
| N_min (multi-event routing) | **2** | sealed pre-reg |
| T (common TLS SDE threshold, both arms) | **10.74** | Seal #2 |
| α_FAP (block-bootstrap period FAP) | **1%** | Seal #2 |
| ε (Arm B targeted half-window) | **0.01** | Seal #2 |
| w_c (occurrence weights; 92.8% on Rₚ≤2 R⊕) | A.5 table | `m3_occurrence_weights.json` |
| π̂ (survey prevalence; E3 only) | **3.17%** | Seal #2 / A.6 |
| Block length L_b = 3·max(τ_GP, T₁₄); B = 1000 | formula | A.8 |
| Conditioning | wotan biweight, **2.5 d** window; celerite2 SHOTerm Σ from M1 | A.9 |
| TLS engine | `transitleastsquares` **1.32**, oversampling 3, identical both arms | A.1 |
| Machine (A.7) | Apple M4, 10 cores, 16 GB, macOS 26.5.1, Python 3.11.9 | A.7 |
| RNG seed | **20260616** | M3 config |

> All values are read from `data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` (hash verified == `6292c018…` at load). The loader **rejects** any attempt to override a sealed key (reuse the M1/M3 `load_config` guard).

---

## 3. TEST injection set (sealed grid — VAL §3)

- **Period P (d):** {0.5, 1, 2, 4, 8, 16}
- **Planet radius Rₚ (R⊕):** {1, 2, 4, 8, 12} → depth via stellar radius
- **Impact parameter b:** {0.0, 0.3, 0.6}
- **≥ 500 injections per (P, Rₚ) cell** (30 cells → ≥ 15,000 injections), b drawn from {0,0.3,0.6}; fixed RNG seed `20260616`.
- **n_transits** recorded as an explicit axis (derived from P × per-target baseline); **E1 estimand restricted to cells with n_transits ≥ 2** (§4).
- **Injection physics:** Mandel–Agol + TESS quadratic limb darkening (Claret 2017, as M2). Inject into **raw** PDCSAP, **then** condition (2.5 d) so conditioning attenuation η is paid in both arms and cancels in the paired ΔR (VAL §4.2).
- **Hosts:** drawn from the **TEST** split (15,798 targets); host-sampling RNG seed `20260616`; hosts may recur across cells. Distinct host list recorded in the M4 artifact.

---

## 4. Endpoints (exactly as sealed — VAL §4)

### E1 — recall non-inferiority (PRIMARY)
- **Recovery predicate (§4.1, both arms identically):** (i) |P̂−P_true|/P_true < 0.01 **or** harmonic {P_true/m, m·P_true}, m∈{2,3} within 1% (harmonics flagged + reported separately); (ii) epoch within ±0.5·T₁₄; (iii) arm's TLS **SDE ≥ T = 10.74**.
- **Estimand:** $\overline{\Delta R} = \sum_{c:\,N_{\rm tr}\ge 2} w_c\,(R_{\text{comb},c} - R_{\text{TLS},c})$, weights w_c frozen (A.5).
- **Decision:** **PASS iff the lower bound of the one-sided 95% CI on $\overline{\Delta R}$ is > −2 pp.** CI by bootstrap over injections (paired by injection, B = 1000, seed `20260616`).
- **Reporting:** per-cell ΔR_c as secondary (Holm-corrected if screened; never gating). **Rₚ=1 (noise-limited) and the Rₚ≤2 R⊕ dominance (92.8% of w_c) reported honestly** — that population is recovered by the full-TLS fallback (folding), not single-transit conditioning (Seal #2 note).

### E2 — compute, fast-path-eligible (PRIMARY)
- **Population:** fast-path-eligible stars (detector evidence meets θ: ≥ N_min events, or monotransit SNR₁ ≥ z_mono). Eligibility is operational, fixed by Seal #2 — not defined on the test outcome.
- **Metric:** single-thread **CPU-core-seconds**, combined (Arm B) / full-TLS (Arm A), on the A.7 machine, **ρ_d (detector cost / full-grid cost) included**, charged on every routed star.
- **Decision:** **PASS iff reduction ≥ 30%** (combined ≤ 0.70 × full) **at non-inferior recall (E1 passes).**
- **Ledger:** per-stage (detector ρ_d, period inference, targeted/fallback TLS for Arm B; full TLS for Arm A). Shared Stage-0 conditioning **excluded** (charged equally to both arms) so the comparison isolates search cost. Report break-even π⋆ = ρ_d / f_p.

### E3 / π⋆ — survey-representative compute (SECONDARY — data collected at M4, analysed at M5)
- Collect per-star routing + compute ledgers over the survey-representative mix (planets in a π̂=3.17% fraction; remainder real TOI-removed TEST LCs). **No E3 number is produced or interpreted at M4.**

---

## 5. Execution sequence

1. **Verify seals** (must pass before anything): `git diff phase1-prereg-v2` on the three sealed docs empty; `shasum -a 256 …SEALED_CORE.json == 6292c018…`. Load Seal #2 read-only.
2. **Assemble injection-host + survey-sample lists** from the TEST split (seed `20260616`); record distinct host list. Assert every selected row has `split == 'test'`.
3. **Download + condition** only those LCs (2.5 d window) — sandbox-disabled (host network); MAST retry on transient drops; multiprocessing `imap_unordered` chunksize=1 (M3 pattern).
4. **Inject** Mandel–Agol signals into raw flux per the grid; condition each injected LC.
5. **Arm A (baseline):** full-grid TLS on every injected + survey LC → SDE, P̂, t₀.
6. **Arm B (combined):** detector (GP-whitened matched filter, box duration grid) → event extraction (z⋆) → routing (N_min / z_mono → θ) → period-from-spacing + block-bootstrap FAP (α_FAP) → **targeted** TLS on [P̂(1−ε), P̂(1+ε)]; **full-TLS fallback** where not fast-path-eligible → SDE, P̂, t₀.
7. **Recovery** (§4.1) applied identically to both arms; harmonic & monotransit flags recorded.
8. **E1:** per-cell completeness → w_c-weighted $\overline{\Delta R}$ + one-sided 95% CI → PASS/FAIL.
9. **E2 ledger + timing** (§6) → reduction % on the fast-path-eligible population → PASS/FAIL (conditioned on E1).
10. **Freeze** all outputs → `data/manifests/m4/` + content hash (the M4 results artifact). Anti-tuning audit (TEST read once; no sealed value changed).

---

## 6. Compute-ledger timing rule (E2 — owner-confirmed 2026-06-18)

- **Recall (E1):** run the full sealed injection campaign **once**. Recovery is deterministic given seeds — **no repeats**.
- **Timing (E2):** measure CPU-core-seconds on a **pre-defined representative subset** of the fast-path-eligible population, with **≥ 5 warm-cache repeats**, single-thread.
- **Subset-selection rule (frozen here, before execution):** from the fast-path-eligible injected LCs, take a **stratified sample of ≥ 10 LCs per occupied (P, Rₚ) cell** (all of them if a cell has fewer), capped at **300 LCs total**, drawn with RNG seed `20260616`. Time **both arms on the identical subset stars** (paired). The subset list is recorded in the M4 artifact before timing.
- **Reported:** mean, median, variance across repeats, ρ_d, per-stage ledger, and the resulting combined-vs-full compute-ratio estimate (point + spread). Purpose is a stable compute estimate, not multiplying the sealed run by 5.

---

## 7. Single-shot discipline & dry-run validation gate (MANDATORY before TEST)

- The complete M4 pipeline (steps 5–10) is **validated end-to-end on the CALIBRATION split (and/or synthetic LCs)** until outputs are sane and the code path is frozen. **Only then** is the TEST execution launched.
- **No peeking:** no TEST-derived quantity is inspected before the full run completes; no threshold/config/seed/grid change after any TEST row is read.
- **Boundary assertions:** every loaded row asserted `split=='test'` during the run (and `split=='calibration'` during the dry run). Seal #2 loader rejects sealed-key overrides.
- **Provenance:** library versions, seeds, machine, and the Seal #2 hash carried into the M4 artifact.

---

## 8. Deliverables (M4 results artifact → `data/manifests/m4/`)

- Per-injection recovery table (both arms; period/epoch/SDE; harmonic + monotransit flags).
- Per-cell completeness R_comb,c / R_TLS,c (n_transits axis).
- E1: $\overline{\Delta R}$ + one-sided 95% CI + PASS/FAIL.
- Per-star compute ledger (both arms, per stage) + ρ_d; E2 timing-subset table (mean/median/variance, ≥5 repeats); E2 reduction % + PASS/FAIL.
- Survey-sample per-star routing + compute ledgers (raw E3/π⋆ inputs; uninterpreted).
- Distinct TEST host list; injection seed log; anti-tuning audit (read-once attestation).
- `research/m4_evaluation/` tooling + `requirements.txt` (pins identical to M3).
- **M4 results content hash** recorded before any downstream (M5) analysis.

---

## 9. Risks

| ID | Risk | Mitigation |
|----|------|------------|
| **R4-1** | Accidental TEST peek / config change after read → invalidates the single-shot | §7 dry-run gate on CALIBRATION; boundary assertions; frozen code path; no edits post-read |
| **R4-2** | R-3 seed-accuracy collapse under red noise (the v3 failure mode) | First true test here; Arm B falls back to full TLS when evidence/period seed is weak — recall protected by the fallback, surfaced in the ledger |
| **R4-3** | Small-planet (Rₚ=1) recall noise-limited drags $\overline{\Delta R}$ | Pre-registered, reported honestly; recovered via TLS fallback; w_c is sealed (no re-weighting to flatter the result) |
| **R4-4** | TLS engine/version drift breaks both-arms fairness | Pin 1.32, identical engine object + config both arms; hash in M4 artifact |
| **R4-5** | ρ_d large enough that E2 fails despite E1 pass (R-1, top risk) | This is a legitimate falsification outcome, reported as-is — not engineered away |
| **R4-6** | TEST conditioning is a large network-heavy overnight job | Condition only what the run consumes; batched `imap_unordered` + MAST retry; sandbox-disabled |

---

## 10. Sign-off gate (must be signed before TEST is read)

| Item | Owner choice (2026-06-18) |
|------|---------------------------|
| Run scope | _capture E1 + E2 + raw E3/π⋆ ledgers in one TEST read; E3 not interpreted at M4_ ✅ confirmed |
| Conditioning breadth | _only what the run consumes (injection hosts + survey sample)_ ✅ confirmed |
| E2 timing | _full recall run once; E2 timing on stratified fast-path-eligible subset (≥10/cell, cap 300), ≥5 warm-cache repeats_ ✅ confirmed |
| Dry-run gate on CALIBRATION before TEST | **pending sign-off** |
| **Approve to read TEST exactly once under Seal #2 (no new frozen parameters)** | **pending sign-off** |

**Approved to execute M4 (read TEST once):** ____________  Date: __________

> On sign-off: dry-run the full pipeline on CALIBRATION/synthetic, freeze the code path, then execute the single TEST run and freeze the M4 results artifact. No Seal #2 value, grid, weight, or config changes under any circumstance — a change requires a new pre-registration.

*References: VAL = `docs/VESPER_PHASE1_VALIDATION.md` v2 (§2–§5, Appendix A); MATH = `docs/VESPER_MATHEMATICAL_FOUNDATIONS.md` v1.1; HYP = `docs/SCIENTIFIC_HYPOTHESIS.md` v2.0; Seal #2 = `PHASE1_M3_PLAN.md` §8b + `data/manifests/m3/SEAL2_RECORD.json`.*
