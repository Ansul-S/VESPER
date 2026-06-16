# Daily Research Log

---

## 2026-06-15 — Phase I pre-registration completed and sealed (v2)

Worked On:
- Full readiness review of the reconstructed repository + vault → produced docs/PHASE1_READINESS_REPORT.md.
- Resolved the four pre-registration blockers and folded in the four should-fix items, then re-registered to v2 and sealed.

Discoveries / Decisions:
- **F1 decision (DR-001):** scope the Phase I compute claim to the fast-path-eligible population; report survey-representative compute as a pre-registered secondary endpoint (with detector overhead ρ_d and break-even prevalence π* = ρ_d/f_p); defer clean-skip routing to Phase II. Adopted with three guardrails (eligibility frozen on calibration; ρ_d measured; π̂ pre-registered + frontier reported).
- Key insight: at TESS-realistic prevalence π ~ 10⁻², survey-scale saving ≈ π·f_p − ρ_d is near zero/negative by construction — so a near-zero E3 is an *expected, honest* result, not a failure. This is what motivates the Phase II clean-skip tier.
- F2: operational recovery predicate pinned (period 1% / harmonics m∈{2,3} flagged · epoch ±0.5 T₁₄ · SDE ≥ T), applied identically to both arms.
- F6: single occurrence-weighted primary estimand ΔR̄ with log-uniform period prior × Kunimoto & Matthews (2020) radius occurrence; per-cell results secondary (Holm) and never gating.
- F8: TLS baseline, thresholds/targets, and runtime protocol pinned in Validation Appendix A; numeric thresholds correctly deferred to M3 (calibration-derived), sealed before M4.
- R-4: committed circular block-bootstrap FAP scheme (L_b = 3·max(τ_GP, T₁₄), B ≥ 1000) — closes the red-noise exchangeability gap.
- R-5: transit-preservation requirement (median η = δ_post/δ_true ≥ 0.90) as a required pre-M3 check.
- R-6: single-planet + strict-periodicity scope stated explicitly; "model-agnostic" claim scoped to event detection only.
- R-7: monotransit single-event vetting criterion (shape, ingress/egress, no secondary, centroid); weaker FP control acknowledged; excluded from headline.

Artifacts created/updated:
- Re-registered: SCIENTIFIC_HYPOTHESIS.md v2.0, TRINETRA_X_PHASE1_VALIDATION.md v2, TRINETRA_MATHEMATICAL_FOUNDATIONS.md v1.1.
- Created: docs/decisions/F1_DECISION_RECORD.md (DR-001), docs/PHASE1_READINESS_REPORT.md.
- Seal: commit 723087e, annotated tag `phase1-prereg-v2`; content hashes verified against the tagged tree.

Problems / Risks carried forward:
- Top residual risk remains F1/PR-A external validity — mitigated but the scoped claim only holds if ρ_d is genuinely small; must be measured at M3/M4.
- Other live risks (tracked in readiness report §6): seed-accuracy collapse under red noise (the v3 failure mode, a real possible null), bootstrap exchangeability under red noise (mitigated by R-4), conditioning recall cost (R-5), straw-man-baseline avoidance (F8), underpowered cells.

Next Action:
- Begin M0: freeze the TESS sector/target manifest + leakage-safe calibration/test split (first data-touching step). Data must not be read before M0 begins under the sealed protocol.
- Non-blocking: create references.bib; add Phase-I scoping note to the charter.

---

## 2026-06-15 (cont.) — Seal, GitHub publication, and project-memory synchronization

Worked On:
- Cut the pre-registration seal, published the repository to GitHub, and synchronized all project memory for clean session handoff.

Summary of the day's major changes (consolidated for handoff):
- **F1 decision** adopted (a+b+c with three guardrails): compute claim scoped to the fast-path-eligible population; survey-representative compute as a pre-registered secondary endpoint (ρ_d, π* = ρ_d/f_p); clean-skip deferred to Phase II.
- **DR-001 created** — docs/decisions/F1_DECISION_RECORD.md (rationale, consequences, guardrails, seal hashes).
- **v2 re-registration** applied across the three frozen documents.
- **F1, F2, F6, F8 resolved**; **R-4, R-5, R-6, R-7 incorporated** into the same v2 seal (no second pre-data re-registration needed).
- **Seal created** — commit `723087e`, annotated tag `phase1-prereg-v2`; frozen-doc SHA-256 hashes verified.
- **GitHub repository created + pushed** — origin = https://github.com/Ansul-S/TRINETRA-X; `main` and tag `phase1-prereg-v2` are on the remote; `.obsidian/workspace.json` now gitignored.
- **Vault synchronized** — Current_Mission, Dashboard, this log; SESSION_HANDOFF_2026-06-15.md created.
- **CLAUDE.md** "Current status" + document map updated; Obsidian-sync operational guidance added.

Status after session:
- Pre-registration SEALED. No Critical/Must-fix/should-fix findings open. No data read. M0 not started.

Next Action:
- Author PHASE1_EXECUTION_PLAN.md, then begin M0 (freeze sector/target manifest + leakage-safe split).

---

## 2026-06-15 (cont.) — M0 execution plan authored and approved

Worked On:
- Authored `PHASE1_EXECUTION_PLAN.md` (v0.1, **M0 increment only**) from the sealed protocol and got in-session owner approval to start M0.

Discoveries / Decisions:
- **Tooling note:** the `/gsd-plan-phase` skill is built for a GSD `.planning/` software project (hard-errors without ROADMAP.md; spawns research/planner agents emitting GSD `PLAN.md` files). TRINETRA-X has no `.planning/` and treats documents as deliverables, so running GSD would have meant unrequested scaffolding + web-searching agents. Decision: apply GSD's *discipline* (milestones → tasks → deps → risks → deliverables → completion criteria) in the project's native research-doc form; no agents spawned. Recorded here so the choice isn't lost to chat.
- **M0 scope clarified:** M0 operates on **catalog metadata only** (TIC, SPOC 2-min availability, coordinates, stellar params, baselines, TOI/EB labels). Bulk light-curve retrieval + conditioning is **M1**. The leakage-safe split needs only TIC IDs + sky coordinates — no photometry — so M0 honors "no data download" cleanly while still being the first archive-touching step.
- **Two seals kept distinct:** **Seal #1** = M0 manifest content-hash (who/what data). **Seal #2** = M3 threshold manifest hash (VAL A.10) — numeric thresholds (z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP) stay deferred to calibration. M0 sets **no** thresholds.
- M0 decomposed into M0.1 sectors → M0.2 metadata target manifest → M0.3 labels/null pool → M0.4 leakage-safe split (TIC-disjoint **and** sky-region/camera-CCD-blocked, no training split) → M0.5 feasibility/power check (≥500 injections/cell at n_tr≥2 vs §6) → M0.6 manifest assembly + Seal #1. Includes a 7-row risk register, deliverables table, 8 binary completion criteria, and a traceability matrix to the sealed clauses.

Artifacts created/updated:
- Created: `PHASE1_EXECUTION_PLAN.md` (status **APPROVED**, M0 not started, no data read; sealed docs verified byte-identical to `phase1-prereg-v2`).
- Vault synchronized: Current_Mission, Dashboard, this log.

Problems / Risks carried forward:
- Same Phase I risk register (readiness report §6). M0-specific risks now tracked in the plan: systematic leakage surviving a TIC-only split (→ sky-region/camera-CCD blocking + audit), selection bias (outcome-independent cuts), null-pool contamination (catalog incompleteness bounds H4), reproducibility (pin versions/seeds + hash), power shortfall (M0.5 gate), premature TEST inspection (Seal #1 + access rule).

Next Action:
- Execute **M0** per `PHASE1_EXECUTION_PLAN.md` §3. Non-blocking: create `references.bib` (Kunimoto & Matthews 2020), add the charter scoping note (F7).

---

## 2026-06-15 (cont.) — M0 executed and sealed (Seal #1)

Worked On:
- Implemented the M0 manifest pipeline (`research/m0_manifest/m0_pipeline.py`) and ran M0 end-to-end against live TESS archives. First data-touching milestone — **catalog metadata only, no flux**.

Discoveries / Decisions:
- **Sectors S1–S3 (south) are feasible — no widening needed.** 32,960 unique SPOC 2-min TICs → **22,723** after cuts. n_sectors: 15,450 (1) / 3,841 (2) / 3,432 (3, CVZ). M0.5: every period node ≥ 500 eligible test hosts at n_tr≥2; binding **P=16 d = 5,794 test hosts**. (Owner rule: widen only if metrics demand — they don't.)
- **Leakage-safe split:** HEALPix nside=8 whole-block, seed 20260615, 30/70 → calibration 6,925 / test 15,798; **leakage audit PASS** (0 shared pixels; TIC-disjoint).
- **Seal #1 (manifest SHA-256): `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`** — deterministic across 3 runs. Provenance + TOI snapshot in `data/manifests/m0/m0_manifest_provenance.json` (tracked); bulk manifest parquet gitignored (regenerable).
- **Three faithful realizations (flagged, reversible pre-seal):**
  1. `CROWDSAP` is a per-LC FITS-header value, not a catalog field → crowding applied via TIC `contratio ≤ 0.25` (CROWDSAP≈1/(1+contratio)); literal CROWDSAP confirmed at M1.
  2. ExoFOP timed out → TOI labels from **NASA Exoplanet Archive TAP** (table `toi`): 97 confirmed-planet hosts, 224 planet/cand, 45 known-FP, 41 multi-planet, null 22,458.
  3. FP labels = TOI FP/FA dispositions (largely EBs); dedicated EB catalog (Prša et al. 2022) deferred to M1+.
- Tooling stack installed in `.venv` (astroquery 0.4.11 etc.); `pip freeze` pinned into provenance.

Artifacts created/updated:
- `research/m0_manifest/m0_pipeline.py` (M0.1–M0.6 implemented); `config/m0_config.yaml` (signed choices).
- `data/manifests/m0/`: provenance JSON + TOI snapshot + pip-freeze lock (tracked); manifest/intermediate parquets (gitignored).
- `PHASE1_EXECUTION_PLAN.md` §3.7–3.8 updated — all completion criteria ☑, Seal #1 recorded, M0 signed DONE.

Problems / Risks carried forward:
- R0-3 null-pool incompleteness (undetected planets in "null" stars) recorded — bounds H4 FAR calibration.
- Manifest table not in git (data-gitignore policy) — seal anchored to hash + provenance + TOI snapshot + pinned versions; decide later whether to archive the frozen table (release asset/DVC).

Next Action:
- Land M0 (PR #2 from `phase1/m0-setup`) and/or begin **M1** (Stage-0 conditioning on the calibration pool). TEST sealed until M4; **Seal #2** (thresholds) at M3.

---

## 2026-06-15 (cont.) — M1 Stage-0 conditioning executed (η-sample)

Worked On:
- Signed off + froze the M1 conditioning config; implemented `research/m1_conditioning/m1_pipeline.py`; conditioned the η-validation sample.

Discoveries / Decisions:
- **Conditioning config (signed):** wotan biweight slider, window 0.5 d (η-finalized at M2); momentum (~2.5 d) + SPOC default quality + scattered-light masks; celerite2 SHOTerm noise model; η-sample 200 (seed 20260615).
- **Fidelity fix #1 — frozen-sector restriction:** lightkurve returns *all* sectors a TIC was ever observed (incl. extended mission 28/29/68); M1 **restricts to frozen M0 sectors {1,2,3}** so conditioning stays inside the seal.
- **Fidelity fix #2 — τ_GP:** the celerite2 SHOTerm point-fit was unreliable (stuck near init). Switched operational **τ_GP to the residual ACF e-folding** (robust; A.8 explicitly permits GP/**robust**); celerite2 retained as a recorded cross-check. After the fix τ_GP tracks correlation (white stars ~8 min; active star ~88 min).
- **η-sample result (188/200 conditioned, 12 skipped):** σ med 1067 ppm [480, 3849]; CDPP(1h) med 222 ppm, CDPP(2h) 154 ppm; τ_GP med ~8 min. **Stationary 187/188 (99 %); white 166/188 (88 %); flagged 12 %** (active-star tail → window-widening candidates at M2). Physically sensible TESS 2-min precision.
- M1 stack installed (lightkurve 2.6.0, wotan 1.10, celerite2 0.3.2).

Artifacts created/updated:
- `research/m1_conditioning/` (pipeline, config, README, requirements).
- `data/manifests/m1/`: noise summary (CSV tracked; parquet gitignored) + describe + provenance JSON + pip-freeze. Conditioned residuals (`data/processed/m1/*.npz`) and LC cache gitignored.
- `PHASE1_M1_PLAN.md` §7 updated — criteria met on the η-sample; results table recorded.

Problems / Risks carried forward:
- 12 % active-star tail not fully whitened at 0.5 d window — expected; handled by the **M2 η ≥ 0.90 check** (per-cell window widening before any M3 threshold). 12 skips (no retrievable frozen-sector SPOC product).
- Full-pool conditioning (6,925) deferred — runs on demand at detection (M3/M4) unless owner wants it pre-computed.

Next Action:
- **M2** — injection harness (Mandel–Agol) + η = δ_post/δ_true per (P,R_p) cell; finalize the detrend window (η ≥ 0.90) before M3. TEST sealed until M4; Seal #2 (thresholds) at M3.

---

## 2026-06-16 — M2 injection + transit-preservation (η) complete; window finalized at 2.5 d

Worked On:
- Built + ran the M2 injection harness and the η ≥ 0.90 transit-preservation check; finalized the detrend window; signed off M2.

Discoveries / Decisions:
- **Harness:** batman Mandel–Agol + quadratic Claret-2017 TESS LD (VizieR J/A+A/600/A30 `tableab`, interpolated on Teff/logg, solar Z); e=0, a/R⋆ from stellar density (logg+R⋆); inject into real **null-pool** calibration PDCSAP (null = no TOI of any disposition) → re-condition → δ_post via fixed-shape LS at the known ephemeris.
- **Two harness bugs fixed during validation:** null pool derived from the tracked TOI snapshot (manifest lacked `is_null`); η sign + unit-depth template (scale actual-geometry model by its depth, not rp=1). After fixes, P=0.5 cells recover η≈0.93–1.0.
- **Window finalization (M2.4):** provisional **0.5 d failed** long-period/shallow cells; swept 1.0/1.5/2.0/3.0 d then a focused 2.5 d (150 inj/cell). **Owner finalized the window at 2.5 d.** All individually-measurable cells (Rₚ≥4) pass cleanly; the η spread balloons only as depth drops below the noise.
- **Full η grid (30 cells × 200 inj, 2.5 d): gate PASS** on the measurable population. Owner gating decision: **the entire Rₚ=1 (Earth) row is excluded as noise-limited** (depth ~70–85 ppm, SNR₁~0.07–0.08, broad/non-physical η, p16<0) — explicit row exclusion, **not** an SNR₁ threshold; widening the window cannot remedy it (the transit is below the noise floor — the detectability bimodality, MATH §2/§7). **0.5/2 retained in the gate as a documented low-SNR borderline** (η=0.892), not reclassified. All gated Rₚ≥2 cells ≥0.90 except 0.5/2.
- **Consequence:** the M1 η-sample noise model (σ/CDPP/τ_GP) was at 0.5 d and is **superseded** — must be recomputed at 2.5 d before M3.

Artifacts created/updated:
- `research/m2_injection/` (pipeline, config, README, requirements); `m1_config.yaml` window 0.5→2.5 d.
- `data/manifests/m2/`: `m2_eta_table.csv` + `m2_provenance.json` (tracked); injected residuals gitignored.
- `PHASE1_M2_PLAN.md` §3a/§3b/§6 — finalization evidence, full η grid, M2 sign-off; vault synced.

Problems / Risks carried forward:
- Earth-radius (Rₚ=1) row is intrinsically noise-limited in TESS 2-min single-transit conditioning — bounds absolute small-planet recall; these are the fallback's job (folding). Documented, not a window failure.
- M1 noise-model recompute at 2.5 d is a hard prerequisite for M3.

Next Action:
- **M3 — threshold calibration** (calibration set only): recompute M1 noise model at 2.5 d, then derive + **hash-seal** `z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP` (**Seal #2**, VAL A.10) before the single M4 test run. Bring the M3 frozen-parameter targets (FAR/FAP, routing rule) for sign-off first.

---

## 2026-06-16 (session 2) — M3 start: M1 recompute, M3 sign-off, null-pool contamination discovery

Worked On:
- **M1 noise-model recompute at the finalized 2.5 d window** (M3 prerequisite). Membership pinned to the original **188** η-sample targets (12 skipped NOT retried; window-only comparison). 188/188, zero MAST drift. 0.5 d artifacts archived under `data/manifests/m1/superseded_0.5d/`.
  - Medians 0.5 d → 2.5 d: σ 1067→**1123** ppm; CDPP 1 h 222→**250**, 2 h 154→**191**, 4 h 98→**142** ppm; τ_GP unchanged; stationarity unchanged. Wider window leaves more low-frequency power (grows with timescale) — the expected transit-preservation tradeoff; thresholds will be set against this (honest, conservative) noise.
- **`PHASE1_M3_PLAN.md` drafted + SIGNED OFF** (decisions A–G). Scope reconciliation accepted: the untrained detector + period-from-spacing + shared TLS engine are **built in M3** (M2 delivered only injection+η). Still no learned models.
- Built `research/m3_calibration/`: GP-whitened **box matched-filter detector**, **integer-comb** period + **circular block bootstrap** (B=1000, L_b=3·max(τ_GP,T₁₄)), **pinned `transitleastsquares` 1.32** (identical both arms), two-phase calibration driver (serial condition → parallel TLS/bootstrap).

Discoveries:
- **NULL-POOL CONTAMINATION (significant).** First calibration on 185 null calibration stars: **z⋆=3.6 is robust**, but **T(SDE)=19.3** and **z_mono=14.4** are **inflated by unlabeled eclipsing binaries / variables** still in the "null" pool (null = TOI-removed only; Prša 2022 EB catalog was deferred at M0). SDE body is clean (median 5.7) but the tail is contaminated (max **27.9 = EI Tuc**, an Algol EB). This is the **R0-3 / H4 null-pool-contamination risk** coming due.
- **Cleaning confirms the hypothesis.** Catalog cross-match (**Prša et al. 2022** TESS EB + **VSX** variables) excluded **30/185**; automated EB vetting (secondary-eclipse / odd-even / V-shape) flagged **+2** → **32 excluded**. Cleaned 153: **z⋆ 3.4, z_mono 5.3 (was 14.4), T 10.1 (was 19.3), α_FAP exceedance 3.9%→2.0%**; body unchanged. Contamination was the cause.

Decisions:
- Clean via **Option 3** (catalog enrichment + vetting); M0 null definition **preserved** — cleaned set is a *derived M3 calibration subset* with a documented exclusion table (`calibration_exclusions.csv`).
- **Scale to ~1000 cleaned null stars** for the final FAR≤1%/star T (153 confirms the hypothesis but the 1% tail is under-sampled; full 6,885 deferred pending the 1000-star read).
- **Keep the 5 catalog+vetting survivors** (no EB signature) — documented "high-SDE survivor review set"; reduce their leverage by scale, not subjective exclusion.

Artifacts created/updated:
- `research/m1_conditioning/recompute_noise_window.py`, `eta_sample_188.txt`; `data/manifests/m1/` (2.5 d summary + provenance; 0.5 d under `superseded_0.5d/`).
- `research/m3_calibration/` (config, detector, period_recovery, tls_engine, m3_calibrate, null_cleaning, vet_outliers, recalibrate, requirements).
- `data/manifests/m3/`: `m3_thresholds_*PROVISIONAL.json`, `calibration_exclusions.csv`, `m3_vetting.csv`, `m3_per_star*.csv`; 185 diagnostic archived under `diagnostic_185/`.
- `PHASE1_M3_PLAN.md` (drafted + §10 signed).

Problems / Risks carried forward:
- **No Seal #2** — thresholds are PROVISIONAL pending owner review of the 1000-star cleaned distributions; then decide if the full 6,885 pass is needed.
- 5 high-SDE survivors (esp. TIC 150102227, SDE 17.8 / 167 ppm) keep T mildly elevated; scale should dilute their p99 leverage.
- Branch `phase1/m3-calibration`; nothing committed yet (commit on owner request).

Next Action:
- 1000-star cleaned-null calibration executing (background). On completion: clean → vet → recalibrate; report T, z_mono, α_FAP exceedance, tail composition, T-sensitivity to top survivors → **owner review before Seal #2**. Then instantiate w_c/π̂ (Kunimoto & Matthews 2020) and assemble the threshold manifest.

---

## 2026-06-16 (session 2, cont.) — M3 1000-star cleaned calibration converged

Worked On:
- **1000-star null calibration** (full pool draw, seed 20260616). Phase A conditioning 1000/1000 at 2.5 d (0 failures, after hardening Phase A with retry/skip — a transient MAST drop had killed the first attempt). Phase B parallel TLS/bootstrap (imap_unordered, chunksize=1).
- **Cleaning at scale:** Prša 2022 + VSX cross-match excluded **132**; automated EB vetting of the 45 residual SDE>9 outliers flagged **+14** (incl. TIC 370324073 at 42.6σ odd-even + 12.9% depth; TIC 207238086 at 60σ secondary) → **146 excluded → cleaned 854**.
- **Bootstrap stability** (B=1000 resamples of the 854) + **retained-high-SDE survivor audit** (31 kept).

Discoveries / Results:
- **Contamination pattern held at scale** (raw 1000: z⋆ 3.5 stable; T 18.7, max SDE 40.4 from EBs). Cleaned 854 thresholds, with bootstrap 95% CIs: **z⋆ = 3.4 [3.30,3.40]** · **z_mono = 5.3 [5.0,5.8]** · **T(SDE) = 10.74 [9.74,11.34]** · **α_FAP = 1%** (null exceedance **1.08%**, at target) · ε = 0.01 · N_min = 2.
- **Tail composition (SDE>9, n=74):** 15 EB + 14 variable + 14 vetted-eclipse = 43 contaminants; **31 survivors retained**.
- **T robust:** drop-top-5 survivors → 9.96 (only −7%); no single survivor dominates the 1% tail. z⋆ unaffected by contamination at every scale.
- **31 survivors** mostly long-period (17/31 P>10 d) few-transit TLS noise + a few shallow (15/31 <500 ppm); top = TIC 150102227 (SDE 17.8, 167 ppm, single-event 3.5σ, period-FAP 0.76 → red-noise latch, not a coherent transit).

Decisions (owner):
- **Accept the cleaned 1000-star basis**; full 6,885 pass **not** required (CIs tight, no new pathology).
- **Keep all 31 survivors** (passed catalog + vetting); document in a retained-high-SDE audit table; no hand-pruning (avoids biasing T downward).

Artifacts:
- `research/m3_calibration/`: + `null_cleaning.py`, `vet_outliers.py`, `recalibrate.py`, `stability_audit.py`.
- `data/manifests/m3/`: `m3_per_star*.csv`, `calibration_exclusions.csv` (146), `m3_vetting.csv`, `m3_null_cleaned_catalog.csv`, `m3_thresholds_cleaned_PROVISIONAL.json`, `m3_stability_audit.json`, `retained_high_sde_audit.csv`; diagnostic 185 under `diagnostic_185/`.

Next Action:
- **Before Seal #2:** instantiate **w_c / π̂** (Kunimoto & Matthews 2020; A.5/A.6) → assemble the threshold manifest → **hash (Seal #2)** on owner go-ahead → M4 single sealed-TEST run. TEST sealed until M4.

---

## 2026-06-16 (session 2, cont.) — M3 Decision F + Seal #2 recorded → M3 DONE

Worked On:
- **Decision F (occurrence weights / prevalence).** Pulled Kunimoto & Matthews (2020) from source (arXiv:2004.05296): Table 5 FGK radius marginals (P<50 d: 1-2 R⊕ 16.2%, 2-4 25.2%, 4-8 1.6%, 8-16 1.6%) + Eqn 25 period power law. Instantiated **w_c** = log-uniform w_P × K&M radius prior w_R, and **π̂** = occurrence over grid × geometric ⟨R⋆/a⟩.
- Recorded **A.7 runtime machine** (Apple M4, 10 cores, 16 GB, macOS 26.5.1, Python 3.11.9).
- Assembled the **complete threshold manifest** (VAL Appendix A.1–A.10), presented for review, then **recorded Seal #2** on owner approval.

Results:
- **w_R (normalized):** R=1 0.363 · R=2 0.565 · R=4 0.036 · R=8 0.0105 · R=12 0.0254. **w_c puts 92.8% of weight on Rₚ≤2 R⊕** (Rₚ=1 alone 36.3%).
- **π̂ = 3.17%** = occurrence 19.74% (P∈[0.78,16] d, R 1–16) × geometric ⟨R⋆/a⟩ 0.160 (n=6925 cal stars).
- **Seal #2 (threshold manifest SHA-256): `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** — owner-approved 2026-06-16; distinct from Seal #1 (`1f2d49e1…`). Independently verifiable: `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.

Decisions (owner):
- Approve the manifest as presented; **create Seal #2 using the candidate hash** (no changes to thresholds/weights/prevalence/conditioning/bootstrap/detector).
- Add an **expected-evaluation note** (E1 dominated by Rₚ≤2 due to K&M weighting + M2 Earth-radius single-transit limit) — recorded **outside** the hashed core (in `SEAL2_RECORD.json`) to preserve the approved hash; no sealed value altered.

Anti-tuning verified:
- `git diff phase1-prereg-v2` on the 3 sealed docs = **empty**; **0 TEST TICs** in any M3 artifact. TEST sealed until the single M4 run.

Artifacts:
- `research/m3_calibration/`: + `occurrence_weights.py`, `assemble_manifest.py`, `finalize_seal2.py`.
- `data/manifests/m3/`: `m3_occurrence_weights.json`, `m3_threshold_manifest_SEALED_CORE.json`, `SEAL2_RECORD.json`, `m3_threshold_manifest_PROVISIONAL.json`.

Next Action:
- **M4 — single sealed-TEST evaluation** against Seal #2 (`6292c018…`): apply frozen machinery + thresholds to the TEST split exactly once → E1 (recall non-inferiority) / E2 (scoped compute). No threshold/config change permitted; TEST read for the first time at M4.

---

## Template for future entries

Date:

Worked On:

Discoveries:

Questions:

Problems:

Next Action:
