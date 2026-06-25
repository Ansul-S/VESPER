# Daily Research Log

---

## 2026-06-20 — M4 driver built + CALIBRATION dress rehearsal; TEST authorized (held at scale)

Worked On:
- Built `m4_driver.py` (v3 confirmer-only): one driver for the CALIBRATION dress rehearsal (`--mode dry_run`) and the token-gated single TEST run (`--mode test --confirm-token READ-TEST-ONCE-SEAL2-APPROVED`). Wired the transit-LR confirmer + sealed T_red=0 + B=1000 FAP gate + full-TLS fallback; E1 (occurrence-weighted ΔR̄ + one-sided 95% CI) + E2 (compute ledger); dual hash-verification + TEST guard; incremental recovery checkpoint.

Discoveries / Decisions:
- **Dress rehearsal verdict: FALSIFIED — compute branch (E1 PASS, E2 FAIL).** E1 ΔR̄=−0.17 pp, lo95=−0.51 pp (per-cell 8, 240 inj) — comfortably non-inferior. E2 reduction −5.6%, ρ_d=0.138 → fail.
- **Power lesson:** the first rehearsal (per-cell 5) showed E1 "FAIL" (lo95 −5.19 pp). That was **underpowered noise**, not a real recall failure — per-cell 8 tightened it to −0.51 pp (PASS). The driver's binary `pass=lo>−2pp` over-reads underpowered CIs; VAL §5's three-way rule calls that INCONCLUSIVE.
- **Recall-loss mechanism fully characterized (owner-requested):** 14/240 losses, **ALL one pathway** — `cheap_confirm` with `fallback_suppressed=True` (the confirmer confirms at the seeded ephemeris → suppresses fallback → seed fails the recovery predicate → miss; Arm A's full TLS recovers them). **11/14 = right period, wrong epoch** (detector t̂₀ less precise than TLS's fitted T₀); 3/14 wrong period. Net −0.17 pp (sub-margin; 9 gains offset). → a **v3-confirmer interaction** (T_red=0 has no recall-protective floor), NOT a fundamental evidence-first failure; does not threaten E1.
- **The genuine, robust limitation is E2 (compute):** the sealed B=1000 period-FAP (un-cheapenable — both Lever-1b candidates failed equivalence) charges ρ_d≈0.12–0.14 on every routed star → no ≥30% saving. This is the honest falsification.
- **Owner AUTHORIZED the single irreversible TEST read.** Held at one decision only: TEST scale — ~per-cell 50 (§6 realized-CI rule, ~3–5 h) vs literal ≥500/cell (~1.5–2 days). Same expected verdict.

Artifacts created/updated:
- `research/m4_evaluation/m4_driver.py`, `M4_DRESS_REHEARSAL_READINESS.md`; `data/manifests/m4/dress_rehearsal/` (recovery, timing_ledger, e1_per_cell, summary). Logs: `m4_dress_rehearsal{,2}.log`, `m4_smoke.log`.
- All CALIBRATION-only; 0 TEST TICs; Seal #1/#2/#2b intact; nothing of the seal changed.

Problems / Risks carried forward:
- **Single TEST read is the next, irreversible action** (P-5). Multi-day at ≥500/cell — incremental checkpoint added for crash-robustness. **No v4 (P-2/P-8).**
- T_red=0 recall leak is understood + sub-margin, but is a real (small) cost of the cheap path that would persist on TEST.

Next Action:
- Resolve the TEST-scale choice; fire the token-gated read once; accept the pre-committed verdict (VAL §7a).

---

## 2026-06-19 (PM) — Seal #2b CUT: v3 = confirmer-only (Lever-1b equivalence failed)

Worked On:
- Implemented the transit-LR confirmer (`confirmer.py`; spec-locked D-1a/D-2a/D-3-i) and ran the two pre-registered CALIBRATION campaigns; assembled + sealed the v3 manifest.

Discoveries / Decisions:
- **Lever-1b equivalence gate — BOTH candidates FAILED** (854 nulls + injections, B=1000 reference). **E-EVT** (GPD, B′=100): p95 |ΔFAP|=0.085 (17× tol), 7 FP-admit, 2 recoveries clipped — GPD can't fit the discrete low-event-count null. **E-LUT** (uniform-epoch grid, nsim=4000): 0.104, corr 0.82, 9 FP-admit, 2 clipped — can't capture per-star red-noise event clustering. → **pre-committed confirmer-only fallback** (DR-002 §2.3a): period-FAP stays the sealed B=1000 bootstrap, **ρ_d≈12.4% retained**. The equivalence gate worked exactly as designed — the cheap estimator was *required* to be numerically equivalent and isn't.
- **T_red = 0.0 (non-binding), FAR-calibrated** (P-3): end-to-end Arm-B FAR 0.12%. The genuine transit-LR confirmer **rejects 8/9 FAP-gate-passing nulls** (real FP rejection, unlike the dry-run box-S/N; AUC 0.894). Fast-path recall 46% (54% fallback is period-seed error, not the confirmer → combined recall protected).
- **Honest projection:** confirmer-only v3 keeps ρ_d≈12.4% → **E2 expected <30% → H1 compute-branch FALSIFIED** on the single TEST run (E1 recall pass). A legitimate negative Phase I; the recall principle + confirmer upgrade stand.

Artifacts created/updated:
- **Seal #2b cut:** tag `phase1-prereg-v3` (annotated → commit `ff869d4b`), branch `phase1/m4-v3-seal2b`; manifest `data/manifests/m4/v3/m4_v3_threshold_manifest.json` SHA-256 `54f06a94…`.
- Code: `confirmer.py`, `equivalence_validation.py`, `elut_equivalence.py`, `tred_calibration.py`, `assemble_v3_manifest.py`. Memos: `LEVER1B_EQUIVALENCE_RESULT.md`, `TRED_CALIBRATION_RESULT.md`, `TRANSIT_LR_CONFIRMER_SPEC.md`. Data: `data/manifests/m4/{equivalence,tred,v3}/`.
- Integrity: 0 TEST TICs (verified vs parquet split; substring flags were false positives in float values); Seal #1/#2 intact; no sealed numeric changed.

Problems / Risks carried forward:
- **M4 single TEST run is the next, irreversible action** (P-5): wire transit-LR into the M4 driver + CALIBRATION dress rehearsal first; then one read; accept pre-committed verdict. **No v4 (P-2/P-8).**

Next Action:
- Owner go for the M4 TEST path (driver + dress rehearsal → single TEST read).

---

## 2026-06-19 (AM) — v3 re-registration drafted + owner-approved (DR-002); Seal #2b prep begun

Worked On:
- Resumed from the 2026-06-18 handoff. Verified integrity before any work: `git diff phase1-prereg-v2` on the three sealed docs empty (pre-edit); Seal #2 hash `6292c018…` matches; 0 TEST TICs across all `data/manifests/m4/dry_run/*.csv` (re-verified against the M0 parquet split: 15,798 test / 6,925 calibration). TEST untouched.
- Owner walked a 4-step sign-off gate; then drafted the full v3 re-registration package.

Discoveries / Decisions:
- **4-step owner gate (all CALIBRATION-only, TEST unread):** (1) **adopted** the v3-as-final stopping rule **P-1…P-9** + pre-committed E1/E2/inconclusive outcome mapping; (2) **NN#3 condition #1 = YES** — arbiter must be a genuine **transit-template likelihood-ratio** (Λ/ΔBIC), the dry-run box depth-SNR **rejected**; (3) **v3 scope = Option-2 confirmer + Lever 1b (period-FAP cheapening), equivalence-gated** — Lever 1a subsumed/excluded, Lever 2 (harmonics) deferred to P-8, Lever 3/4 narrative-only; (4) drafting authorized.
- **Key reasoning locked in DR-002:** Lever 1b's admissibility warrant is the **numerical-equivalence gate** (compute the *same* sealed FAP via a cheaper EVT/precomputed estimator), **not** the Finding-A precedent (demoted to supporting illustration per owner revision). Confirmer-only v3 is the fallback if the gate fails. The "same TLS engine" keystone (A6) is relaxed to "**common false-alarm rate**" — the principle survives, the targeted-TLS realization does not (Finding B).
- **Consistency catch:** SCIENTIFIC_HYPOTHESIS.md also carried the v2 "identical TLS engine" keystone (mechanism clause + A6) → amended to **v2.1** so the sealed set stays internally consistent (was not in the owner's explicit list; flagged + closed).
- Owner **approved** the package on governance / internal-consistency / anti-tuning / equivalence-gate / T_red-logic. One remaining gate before Seal #2b: a final **implementation-spec review of the transit-LR confirmer**.

Artifacts created/updated:
- Created: `docs/decisions/DR-002_DECISION_RECORD.md` (ADOPTED), `research/m4_evaluation/LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md`, `research/m4_evaluation/TRED_CALIBRATION_PLAN.md`.
- Amended (drafts, pending Seal #2b): `TRINETRA_X_PHASE1_VALIDATION.md` → v3 (§2 keystone, §4.1(iii), §7a stopping rule, A.1/A.2/A.4/A.8a/A.11); `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` → v1.2 (§6, §9.1a); `SCIENTIFIC_HYPOTHESIS.md` → v2.1 (mechanism clause, A6).
- No sealed numeric value changed; nothing committed/tagged/sealed; TEST unread.

Problems / Risks carried forward:
- **Single-shot M4** is the irreversible read — must follow a verified-correct Seal #2b (P-5). Hard checkpoints set at Seal #2b and immediately before the TEST read.
- **Equivalence gate may fail** → confirmer-only v3 → likely E2-fail/negative result, reported as-is (the honest fallback).
- The transit-LR confirmer must be implemented as a genuine shape LR (NN#3), not the dry-run box-SNR — the pending implementation-spec review.

Next Action:
- Draft the transit-LR confirmer **implementation spec** for owner review (last gate before Seal #2b). Then, on sign-off: Lever-1b equivalence validation → T_red calibration → assemble v3 manifest → Seal #2b → single M4 TEST run → pre-committed verdict.

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

## 2026-06-18 — M4 dry-run: protocol blocker found (Finding B), resolution path validated

Worked On:
- Built the M4 evaluation harness (`research/m4_evaluation/`): Seal #2 read-only loader + TEST-access guard, injection, dual-arm runner, recovery predicate, E1/E2 endpoints, orchestrator.
- Ran the full **CALIBRATION/synthetic dry-run** end-to-end (offline; cached calibration residuals as hosts). **TEST never read** (hard-blocked by the guard).
- Investigated two findings on the targeted (Arm B) search; ran CALIBRATION-only methodology diagnostics; validated an epoch-fixed confirmation statistic.

Discoveries / Decisions:
- **Dry-run validated the machinery.** All TEST-access guards pass (dry-run cannot read TEST; the TEST run needs an explicit token; sealed keys cannot be overridden). Injection→conditioning→detection→routing→recovery→E1-weighting→E2-ledger all execute and behave sensibly (w_c loads from Seal #2: 92.83% on Rₚ≤2; recovery physically correct).
- **Finding A (implementation, fixable):** `transitleastsquares.grid.period_grid` discards the `[P̂(1±ε)]` restriction when the window holds < `MINIMUM_PERIOD_GRID_SIZE=100` periods and silently returns the full default grid. At sealed ε=0.01 the window holds only ~20–35 periods → "targeted" TLS secretly ran a full search (cost ratio 0.995). Feeding TLS the in-window periods directly → real saving (1.7 s vs 164 s, ratio 0.010). M3 never hit this (calibration used `full_tls` only).
- **Finding B (methodology, blocking — CONFIRMED):** TLS **SDE is normalized across the searched grid**, so it is not comparable across grid widths. At the identical period on the same LC: full-grid SDE=40.36 (PASS T) vs narrow-grid SDE=3.55 (FAIL T=10.74). The sealed rule "targeted TLS on [P̂(1±ε)], SDE≥T, single common T both arms" (VAL §2/§4.1, A.1/A.4) is internally inconsistent → Arm B would reject planets Arm A accepts → E1 fails by construction.
- **Methodology review (CALIBRATION-only, 16 hosts):** **Option 1** (per-arm narrow-SDE threshold T_B) **rejected** — narrow-grid SDE AUC=0.43 (chance), no separation. **Option 3** (wider window, single T) **rejected** — AUC only 0.72 at ε=0.2 where 84% of saving is already gone; comparability and savings mutually exclusive. **Option 2** (period-fixed statistic) recommended.
- **Epoch-fixed confirmation statistic VALIDATED (CALIBRATION-only, cleaned 854-null pool):** evidence-first supplies P̂ **and** t̂₀ → matched-filter S/N at fixed (P̂,t̂₀), no phase search, no period grid. Red-noise-aware variant (per-transit-timescale scatter, effective N=N_transits): **AUC=0.877**, FAR-controllable (**T_red≈5.5** at FAR≤1%/star), **range-invariant by construction**, **cost 3.3e-5× full TLS** (~0.9 ms vs 28 s). The earlier T=199/recall-0 collapse was an artifact of a null sample that wrongly included M3-excluded EBs (folded depths 5–22%, acf≈0.999) — resolved on the sealed cleaned pool.
- **Recall accounting:** fast-path confirmation recall tracks transit count (P=1→0.92, P=4→0.56). The fast-path gap vs Arm A is **not lost recall** — non-routed / unconfirmed planets fall back to full TLS, so combined recall (E1) is protected; E2 saving accrues on the cheaply-confirmed fraction (ρ_d dominant → R-1 the live risk).

Project state:
- **M4 is BLOCKED pending a protocol amendment** (Finding B). **TEST remains unread; Seal #2 unchanged; no sealed value modified.**
- Recommended next milestone: **Option-2 re-registration / Seal #2b preparation** (red-noise-aware epoch-fixed Arm-B arbiter). Owner to review amendment scope before any re-registration begins.

Artifacts created:
- `PHASE1_M4_PLAN.md` (M4 execution plan, drafted before dry-run).
- `research/m4_evaluation/`: `seal_loader.py`, `injection.py`, `arms.py`, `recovery.py`, `endpoints.py`, `m4_run.py`, `finding_b_diagnostic.py`, `epoch_fixed_diagnostic.py`, `config/m4_config.yaml`, `requirements.txt`.
- Reports: `research/m4_evaluation/M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`.
- Diagnostic data: `data/manifests/m4/dry_run/` (per-injection, E1 per-cell, E2 ledger, finding-B + epoch-fixed CSVs).

Problems / Risks carried forward:
- Finding B requires a re-registration (redefines A.1/A.4 Arm-B arbiter + adds T_red); legitimate as a **pre-TEST** amendment decided on CALIBRATION, sealed before the single TEST run.
- R-1 (detector/period-FAP overhead ρ_d dominates Arm-B cost) is now the live E2 risk; R-3 (red-noise false alarms) is real but controlled by the red-noise-aware normalization on the cleaned pool.
- Compute logistics: full TLS is 30–160 s/LC; the full ≥15k-injection campaign is a multi-day parallel job — plan the M3 `Pool`/`imap_unordered` pattern.

Next Action:
- Present the **proposed Option-2 amendment scope + Appendix-A changes** for owner review (next decision point). Do **not** begin re-registration or create Seal #2b until approved. TEST stays unread.

---

## 2026-06-18 (cont.) — Option-2 system result + methodology & governance boards

Worked On:
- Built + ran the **combined-arm system dry-run** (recall-safe Option-2: route → epoch-fixed confirm → full-TLS fallback) on CALIBRATION. Convened a **methodology review board** (is Option-2 the same experiment?) and a **governance review board** (amendment policy / stopping rule). **TEST never read; Seal #2 unchanged; 0 TEST TICs in any artifact (verified).**

Discoveries / Decisions:
- **System-level endpoints (CALIBRATION, 150 injections + 200 nulls + 12-star timing):** **E1 PASS** (ΔR̄ = −0.39 pp, one-sided 95% lower bound −0.80 pp; fallback + occurrence weighting protect recall). **E2 FAIL** (combined/full = 0.799 → ~20% reduction; population estimate ~29%; both < 30%). E2 shortfall is **structural**: ρ_d ≈ 12.4% (sealed B=1000 block-bootstrap FAP charged on every routed star) + **59% of routed stars fail the FAP gate** → full-TLS fallback. **T_red = 0 (degenerate)** — the FAP gate, not the MF threshold, does the FP rejection on the cleaned pool.
- **Methodology board verdict: Option-2 APPROVED CONDITIONALLY as an AMENDMENT (not a replacement).** Key reconstruction: **MATH §6 defines the arbiter as a likelihood-ratio on folded photometry — "Λ, equivalently ΔBIC or the transit-fit SNR"** — so the epoch-fixed folded-photometry significance is an admitted arbiter form and **satisfies Non-Negotiable #3** (photometry, not timing coherence; repairs the four v3 errors of §E). Option-2 **amends the fairness keystone** (A6: "same TLS engine both arms" → "common false-alarm rate"). The **evidence-first principle survives; the targeted-TLS realization does not** (Finding B). Conditions: (1) arbiter must be a genuine transit-LR (box depth-SNR borderline); (2) re-register the keystone change transparently; (3) anti-tuning discipline. If condition (1) cannot be met as true physics, verdict flips to REJECT.
- **Governance board: proposed v3 = the FINAL permissible amendment + a Phase-I stopping rule (P-1…P-9).** Core distinction: *amendment* (pre-TEST defect fix, e.g. Finding B) vs *tuning* (outcome-motivated change, forbidden by NN#2 on TEST **and** calibration). After v3 no *known defect* compels change, so any v4 would be outcome-driven → unfalsifiability/creep. Pre-commit the E1/E2/inconclusive outcome mapping before TEST; one evaluation; a TEST failure → the pre-committed falsification (no v4); new ideas → new pre-registered experiments. **Pending owner adoption.**
- **If v3 fails on the sealed TEST:** E1 fail → recall falsification (H1 falsified); E2 fail → compute falsification (H1 falsified); inconclusive → pre-planned injection-count increase only. A v3 failure means *both* faithful cheap-confirmer realizations fail on TESS — a strong honest verdict, not a prompt to keep amending.

Artifacts created:
- `research/m4_evaluation/`: `combined_arm_dryrun.py`; reports `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`.
- `data/manifests/m4/dry_run/`: `combined_arm_recovery.csv`, `combined_arm_timing.csv`, `combined_arm_e1_per_cell.csv`, `combined_arm_summary.json`, `epoch_fixed_*.csv`.
- Vault synchronized; `SESSION_HANDOFF_2026-06-18.md` updated; `NEXT_SESSION_PROMPT.md` regenerated.

Problems / Risks carried forward:
- **R-1 (compute external validity) is now the live, measured risk:** ρ_d (B=1000 FAP) ≈ 12% + 59% FAP-gate fallback drive E2 below 30%. The E2 shortfall sits in *sealed* machinery (A.8 B=1000, α_FAP=0.01) — the Arm-B confirmer swap alone cannot fix it.
- **Anti-tuning / amendment creep** — governed by the proposed stopping rule (v3 final; pre-committed outcomes).
- **E2 timing subset = 12 stars** (noisy Σ-cost); a larger timing pass would tighten ~20% vs ~29% (both < 30%).
- The methodology APPROVE is **conditional** on the arbiter being a true transit-LR; the box depth-SNR used in the dry-run does not yet clear that bar.

Next Action:
- **Owner decisions (in order): (1) adopt the v3-as-final stopping rule (P-1…P-9); (2) rule on NN#3 condition — is a folded-photometry transit likelihood-ratio an acceptable physics arbiter; (3) if yes, authorize DR-002 + VAL v3 + T_red calibration plan.** No re-registration / VAL v3 / Seal #2b until adopted. TEST stays unread.

---

## 2026-06-18 (cont. 2) — E2-fix R&D: margined white-noise pre-filter (exploratory)

Worked On:
- Exploratory investigation (CALIBRATION-only, no seal change) into *why* E2 fails and whether it is fixable. Built + ran two validation experiments on existing/cached calibration data. **TEST never read; Seal #2 unchanged; 0 TEST TICs across all m4 artifacts (re-verified).**

Discoveries:
- **Root cause of E2 failure is the sealed B=1000 period-FAP** (ρ_d≈12%, charged on every routed star) + the FAP gate bouncing 59% of routed stars to full-TLS fallback. So E2 is dominated by a *configuration* cost, not a property of the evidence-first principle.
- **Pre-filter premise check** (`validate_prefilter.py`, 120 M3 null stars): the clean per-star inequality "white-FAP ≤ red-FAP" holds only **18.3%** of the time — so the "provably safe, mathematically impossible to pass red if it fails white" justification is **false as stated**. BUT the white FAP is a strong proxy (corr 0.868 with red) and the bare pre-filter rejects 98.3% of null candidates. The null-only safety check was under-powered (nulls rarely pass red).
- **Injection recall-safety test** (`validate_prefilter_injections.py`, 100 injected planets, B=1000): the **bare** pre-filter (reject if white-FAP > α) **loses ~5% of real planets** (4/46 red-pass, 2/39 true recoveries clipped) — confirming the danger. **A safety margin fixes it:** rejecting only at **white-FAP > 5.5·α clips ZERO red-pass planets** (3.2·α for period-matched true recoveries), while null rejection only drops **98.3% → 97.5%**. → ρ_d→~0 with recall preserved → projected **E2 ~25%→~40% (PASS)**.
- **Net:** a *margined* white-noise pre-filter (+ O(1) lookup/EVT FAP for the ~2.5% survivors + multi-period harmonic confirm) is a viable, recall-safe fix for the E2 compute shortfall. **E2 is fixable, not a fundamental falsification.**

Decisions / status:
- This is **exploratory R&D, NOT an adopted decision and NOT a seal change.** It informs the still-pending owner decisions (stopping-rule adoption, NN#3 ruling, v3 scope).
- **Governance implication:** the fix touches **sealed A.8 (period-FAP) machinery** — adopting it would *expand* the v3 re-registration scope beyond the Option-2 confirmer swap, and bumps against the proposed "v3-as-final" stopping rule. Owner must decide v3 scope (confirmer-only vs confirmer + FAP-cheapening).

Artifacts created:
- `research/m4_evaluation/validate_prefilter.py`, `validate_prefilter_injections.py`.
- `data/manifests/m4/dry_run/prefilter_validation.csv`, `prefilter_injection_safety.csv`.

Risks / caveats:
- Margin (5.5·α) is from ~40 red-passers (n small) on strong/recoverable cells (P≤4 d, R≥2) — **deploy with a buffer (~6–8·α) and re-validate on a larger, full-grid injection set** before trusting operationally.
- The pre-filter premise (white as a *bound*) is false per-star; it works only as a *margined heuristic*, validated empirically — not a proof. Margin is statistic-specific (uniform-redraw white tested; analytic-formula white would need its own calibration).

Next Action:
- **Owner: decide v3 SCOPE** — confirmer-only, or confirmer + period-FAP cheapening (the E2-fix). Then (if approved) DR-002 + VAL v3 + T_red calibration + (optional) margined-pre-filter plan, sealed before the single TEST run. TEST stays unread.

---

## 2026-06-24 — M4 single sealed-TEST read EXECUTED → H1 FALSIFIED (compute branch)

Worked On:
- **TEST conditioning (sanctioned first-touch).** The TEST split had never been conditioned (Stage-0); the M1 pipeline is calibration-locked by design and the M4 driver only consumes a residual cache. Built `research/m1_conditioning/condition_test_hosts.py` — reuses `m1_pipeline._condition_one`/`_noise_model` verbatim, frozen-param + threshold-key guards, conditions **exactly** the driver's `test_pool.sample(80, random_state=22)` draw. Verified the conditioned set == the driver's host selection (set-identical). Conditioned **80/80** through frozen Stage-0 (2.5 d biweight, sectors 1–3); 5 transient network failures recovered via an idempotent retry. Provenance: `data/manifests/m4/test_conditioning/`.
- **Fired the single irreversible TEST read once (P-5):** `m4_driver.py --mode test --split test --confirm-token … --per-cell 500 --workers 8`, `caffeinate -i -s`, ~65 h. 15,000 injections (30 cells × 500, literal ≥500/cell — the scale locked after correcting the prior session's "<500 is within §6" read; §6 fixes ≥500 as the floor).

Discoveries (the result):
- **VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** Pre-committed mapping VAL §7a applied.
- **E1 PASS:** occurrence-weighted ΔR̄ = **−0.48 pp**, one-sided 95 % lo **−0.60 pp** (margin −2 pp). Combined recall 0.488 vs full-TLS 0.509. ΔR̄ small because weight (K&M-2020) sits on Rₚ≤2 where arms agree; larger per-cell losses (Rₚ=4–12, ΔR −0.10..−0.26) are low-weight. Cheap path **beats** full TLS at P=0.5 d, Rₚ≥4 (+0.24..+0.39). No INCONCLUSIVE cells.
- **E2 FAIL:** reduction **24.4 %** (ratio 0.756), **ρ_d = 14.4 %** (un-cheapenable B=1000 period-FAP entry tax). Target ≥30 %. Cause structural + pre-identified (dress rehearsal + the failed Lever-1b equivalence gate).
- **Reading:** recall principle holds; compute claim is the falsified branch. A **successful negative Phase I** (prime directive: negative results are results).

Integrity:
- Both seals hash-verified in-run (fail-closed) + intact post-run; `git diff phase1-prereg-v3` over sealed docs + manifests **empty** (NN#2); `test_accessed:true`; TEST read **exactly once**; verdict pre-committed before the read.

Problems / operational:
- Two power cuts during the 3-day run (battery carried it; no work lost; throughput unaffected). MacBook Air M4 health: Condition Normal, no thermal alarms — sustained load is in-spec.

Artifacts:
- `research/m4_evaluation/M4_TEST_RESULT.md` (authoritative result record); `data/manifests/m4/test_run/{summary.json,recovery.csv,e1_per_cell.csv,timing_ledger.csv}`; `data/manifests/m4/test_conditioning/`; `research/m1_conditioning/condition_test_hosts.py`.

Next Action:
- **M7 Phase-I write-up** from the result record + PAPER_NOTES. Optional PR `phase1/m4-v3-seal2b` → `main` (owner). Future ideas → **P-8** (new pre-registered experiments): equivalence-proven cheaper period-FAP, harmonics, recall-protective confirmer floor, clean-skip tier. **No v4 (P-2); TEST will not be read again.**

---

## 2026-06-25 — M7 write-up + M5/M6 characterization (post-result; test-blind)

Worked On:
- **M7 write-up:** manuscript draft v0.1 (`papers/phase1_evidence_first_triage.md`); tables T2/T3/T7 + figures F3/F8 (M4); `docs/references.bib` compiled (ADS-verify pending). PRs #9/#10/#11 merged to `main`.
- **M5 (from existing data, no compute):** F5/F6 + T4/T5 — period match 45.9% (median |ΔP/P| 0.0022 matched), epoch-ok 54.2% (median offset 0.40 T14); period-FAP FAR **1.08% on the cleaned null pool** (reproduces sealed M3; raw 2.07% shows the EB/variable cleaning effect).
- **M6 (gated ~2 h run, test-blind characterization):** built `research/m6_reality_check/` (reality_check, depth_recovery, ablation); restricted TOIs to the **30 calibration-split CP/KP** (excluded 67 test-split TOIs in code → TEST never touched).

Discoveries (M6):
- **T6 reality check:** TOI recall **86.7%, Arm B = Arm A** on 30 real confirmed planets (corroborates E1 recall non-inferiority on real planets). 16 known EBs: 12/16 rejected (8 FAP gate, 4 shape vetting); **4/16 (~25%) slip through** as FPs — genuine confirmer limitation.
- **T8 ablation:** the **bootstrap period-FAP gate controls false alarms** (null FP 0→12.3% if removed); **shape/sign vetting trims recall** (0.133→0.189) with its FP value on astrophysical contaminants (4/8 EBs), not clean nulls.
- **T5-depth:** fitted depth biased **−20%**, seed duration **−31%** (coarse detector grid) → part of the wrong-epoch loss pathway.

Integrity / constraints:
- All M5/M6 work is **characterization, not a re-test**: TEST never touched (M6 used calibration injections + real TOI/EB objects), sealed thresholds unchanged, both seals verified in-run. The H1-falsified (compute branch) verdict is final; v3 remains terminal (P-2, no v4).

Artifacts:
- `papers/phase1_evidence_first_triage.md`; `research/m4_evaluation/{M4_TABLES.md,M5_TABLES.md,make_paper_artifacts.py,m5_recovery_calibration.py,figures/,tables/}`; `research/m6_reality_check/{reality_check,depth_recovery,ablation}.py + M6_TABLES.md`; `data/manifests/m6/`; `docs/references.bib`; `PHASE1_M6_PLAN.md`.

Next Action:
- Finish M7 (compile/verify references; optional F1/F4/F7/F9/T1; venue). Bundle the M6 PR. **No v4 (P-2); TEST read once, not again.**

---

## 2026-06-25 (EOD) — Phase I COMPLETE + Phase II direction set (Kepler scaling)

Worked On:
- **M7 finalized + merged (PRs #9–#13):** manuscript v0.1; T1 dataset manifest; `references.bib` (8 core refs verified exact vs NASA ADS); consistency read-through (fixed 4 stale spots). **Author corrected Vesper → Ansul Suryawanshi** across all docs.
- **Strategic discussion → Phase II direction.** Diagnosed why E2 failed on TESS and what generalizes.

Decisions / discoveries:
- **Phase I is COMPLETE** (M4 verdict + M5/M6 characterization + M7 write-up, all on `main`). The result: H1 falsified on the **compute** branch; recall non-inferiority **supported** (and corroborated on real planets, T6: Arm B = Arm A = 86.7%).
- **Scaling thesis (corrected & adopted as the Phase-II hypothesis):** the compute advantage scales with search-space size because the fast lane folds **k events** vs TLS folds **N points** per trial period (k≪N). Verified the loose "fixed overhead" framing is WRONG — the bootstrap re-runs `best_period` over a baseline-scaled grid; the advantage comes from k≪N, not constant overhead.
- **Real survey-scale bottleneck = the fallback (full TLS on no-evidence stars) = Lever 3**, not the bootstrap. Deferred to its own experiment.
- **LSST ruled OUT** as a showcase (sparse/irregular cadence — different problem). **Kepler** (dense, 4-yr, large period grid, available now) is the proving ground; PLATO/Roman the future analogues.
- **Cross-domain generalization:** real transferable kernel (calibrated local-evidence detection in red noise) BUT the compute thesis only beats *exhaustive periodic search* — most proposed domains (flash-crash, server-outage, ECG) are *aperiodic* anomaly detection where "TLS/Fourier fail" is a strawman vs the real incumbents. Honest version: one experiment in a genuinely periodic domain (predictive maintenance) vs correct baselines. NOT a four-domain victory lap.
- **Phase II experiment chosen + designed:** Kepler scaling experiment; D1–D5 locked (LC; ~2000 FGK / 30-70 split / ~150 hosts; baselines {27d,0.25,1,2,4 yr}; PASS = monotone-↑ reduction AND ≥30% at 4 yr; compute not local). New pre-registration (P-8); Phase I sealed/final, no v4.
- **Compute:** can't run on the MacBook → AWS `us-east-1` spot (Kepler in MAST Open Data, no egress) or national/university HPC; pilot-first on free credits. Condition-once-then-truncate; cloud-portable tooling.

Risks:
- Phase-II compute access undecided (HPC allocation vs AWS spend) — gates the build packaging.
- Kepler red noise/systematics differ → thresholds must be re-calibrated (not reused from TESS).
- Scaling is a hypothesis, not a result (NN#4) — a flat curve would falsify it; that's a valid outcome.

Artifacts:
- `docs/PHASE2_KEPLER_SCALING_PREREG.md` (sketch, D1–D5 + compute plan); `papers/phase1_evidence_first_triage.md` (final v0.1); `docs/references.bib` (verified); `research/m4_evaluation/tables/T1.csv`.

Next Action:
- **Owner:** choose compute path (HPC vs AWS) + venue (AJ/MNRAS). Then promote the Kepler sketch to a full Phase-II pre-registration, build cloud-portable M0-analogue tooling, smoke-test on a few Kepler stars locally, pilot, then full run. Nothing sealed/run until the pre-reg is signed.

---

## Template for future entries

Date:

Worked On:

Discoveries:

Questions:

Problems:

Next Action:
