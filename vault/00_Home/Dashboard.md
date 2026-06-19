# TRINETRA-X Dashboard

## Current Phase

Phase I — Scientific Validation

## Current Goal

Determine whether evidence-first routing can reduce computational cost while preserving recall.

## Program Status Checklist

- Repository Reconstruction — ✅ Complete
- Scientific Audit (gap analysis, F1–F12) — ✅ Complete
- Remediation (F1, F2, F6, F8 + R-4..R-7) — ✅ Complete
- Pre-registration (v2) — ✅ Complete
- Seal (`phase1-prereg-v2`) — ✅ Complete
- GitHub (push + tag) — ✅ Complete
- PHASE1_EXECUTION_PLAN.md (M0 increment) — ✅ Authored + APPROVED (2026-06-15)
- M0 — Manifest freeze + leakage-safe split — ✅ DONE (Seal #1 `1f2d49e1…`, 2026-06-15)
- M1 — Stage-0 conditioning (η-sample) — ✅ DONE (188/200; 99% stationary / 88% white, 2026-06-15)
- M2 — Injection + η transit-preservation — ✅ DONE (window 2.5 d; gate PASS Rₚ≥2, 2026-06-16)
- M1 noise model recomputed at 2.5 d (M3 prerequisite) — ✅ DONE (188/188; 0.5 d archived, 2026-06-16)
- **M3 — threshold calibration → Seal #2 — ✅ DONE** (cleaned 854 null; Seal #2 `6292c018…`, 2026-06-16)
- **M4 dry-run — ✅ DONE (2026-06-18); TEST UNREAD** — harness built + validated; **Finding B blocks M4**
- **v3 re-registration — ✅ DRAFTED + OWNER-APPROVED (2026-06-19)** — 4-step gate decided; DR-002 adopted; VAL v3 / MATH v1.2 / HYP v2.1 + 2 plans drafted
- **Current milestone — Seal #2b prep** — remaining gate: transit-LR confirmer implementation-spec review → equivalence validation → T_red → manifest → Seal #2b → single M4 TEST run

## Milestone Ladder

- Pre-registration completion + seal — ✅ DONE (2026-06-15)
- M0 execution plan authored + approved — ✅ DONE (2026-06-15)
- **M0 — Freeze sector/target manifest + leakage-safe split** — ✅ DONE — Seal #1 `1f2d49e1…`; 22,723 targets (S1–S3); cal 6,925 / test 15,798 (2026-06-15)
- **M1 — Stage-0 conditioning** (per-sector biweight detrend + masking → r(t); noise model σ/CDPP/τ_GP) — ✅ DONE (η-sample 188/200, 2026-06-15)
- **M2 — Injection + η ≥ 0.90 transit-preservation** — ✅ DONE — window finalized 2.5 d; gate PASS (Rₚ≥2); Rₚ=1 row noise-limited, 0.5/2 borderline (2026-06-16)
- **M3 — Threshold calibration (calibration only) → Seal #2** — ✅ DONE — untrained machinery built (whitened MF detector · integer-comb period + block bootstrap · pinned TLS 1.32); M1 noise model recomputed at 2.5 d; null-pool contamination found + cleaned (Prša 2022 + VSX + vetting → 854 of 1000); thresholds bootstrap-stable; w_c/π̂ instantiated; **Seal #2 `6292c018…`** (2026-06-16)
- **M4 dry-run (CALIBRATION/synthetic; TEST untouched)** — ✅ DONE (2026-06-18) — harness validated; guards block TEST; **Findings A + B surfaced**
- **M4 — Sealed-test evaluation (single run) → E1/E2** — ⛔ BLOCKED by Finding B (SDE not comparable across grid widths) — awaiting protocol amendment
- **Governance: adopt v3-as-final stopping rule (P-1…P-9)** — ✅ ADOPTED (2026-06-19)
- **Option-2 v3 re-registration (DR-002)** — ✅ DRAFTED + OWNER-APPROVED (2026-06-19) — transit-LR Arm-B arbiter (common-FAR keystone) + Lever-1b equivalence-gated period-FAP; VAL v3 / MATH v1.2 / HYP v2.1
- **Seal #2b prep** — ▶ NEXT — confirmer implementation-spec review → Lever-1b equivalence validation (CALIBRATION) → T_red calibration (CALIBRATION) → assemble v3 manifest → cut Seal #2b
- **M4 — single sealed-TEST run → E1/E2** — ⛔ after Seal #2b — one irreversible read; accept pre-committed verdict (VAL §7a). Calibration dry-run: E1 pass, E2 fail (E2 fixable via Lever 1b)
- M5/M6 — Parameter coverage, reality check, ablation
- M7 — Write-up

## Sealed Documents (pre-registration set, hash-verified)

- SCIENTIFIC_HYPOTHESIS.md — sealed v2.0 · **v2.1 drafted (pending Seal #2b)**
- TRINETRA_X_PHASE1_VALIDATION.md — sealed v2 (incl. Appendix A) · **v3 drafted (pending Seal #2b)**
- TRINETRA_MATHEMATICAL_FOUNDATIONS.md — sealed v1.1 · **v1.2 drafted (pending Seal #2b)**
- `phase1-prereg-v2` tag preserves the v2 baseline immutably; v3 drafts owner-approved, not yet sealed.

## Other Repository Documents

- TRINETRA-X.md (charter) · TRINETRA_X_ARCHITECTURE.md · TRINETRA_CONCEPT_RECONSTRUCTION.md
- REPOSITORY_GAP_ANALYSIS.md (F1–F12) · PHASE1_REMEDIATION.md
- PHASE1_READINESS_REPORT.md · decisions/F1_DECISION_RECORD.md (DR-001)
- PAPER_NOTES.md · references.bib · **SESSION_HANDOFF_2026-06-18.md** (latest; supersedes 2026-06-16)
- **Execution plans / choices:** PHASE1_EXECUTION_PLAN.md (M0) · PHASE1_M0_CHOICES.md · PHASE1_M1_PLAN.md · PHASE1_M2_PLAN.md · PHASE1_M3_PLAN.md (signed) · **PHASE1_M4_PLAN.md**
- **Tooling:** research/m0_manifest/ · research/m1_conditioning/ · research/m2_injection/ · research/m3_calibration/ · **research/m4_evaluation/** (harness + Finding-B diagnostics + 3 reports)
- **Artifacts/provenance:** data/manifests/m0 (Seal #1) · m1 (noise summary, 2.5 d + superseded_0.5d) · m2 (η table) · m3 (Seal #2 + exclusions; diagnostic_185/) · **m4/dry_run (dry-run + diagnostic CSVs; TEST untouched)**

## Findings Status

- Critical/Must-fix: F1, F2, F6, F8 — ✅ resolved and sealed
- Should-fix: R-4, R-5, R-6, R-7 — ✅ folded into v2 seal
- F7 (charter scoping note) — ✅ done; references.bib — ✅ created
- Remaining: Low hygiene only (F9 BLS wording) — non-blocking
- **M3 finding — null-pool contamination (R0-3/H4):** TOI-removed "null" pool retains unlabeled EBs/variables that inflate T and z_mono; resolved by Prša 2022 + VSX cross-match + automated EB vetting (derived M3 calibration subset; M0 null definition preserved). z⋆ unaffected.
- **M4 dry-run Finding A (fixable):** TLS narrow-window fallback to full grid (< 100 in-window periods) — implementation fix only; no sealed-value impact.
- **M4 dry-run Finding B (BLOCKING):** TLS SDE not comparable across grid widths → sealed Arm-B "SDE≥T on narrow window, single common T" rule invalid. **Blocks M4.** Resolution = Option-2 epoch-fixed arbiter (validated on CALIBRATION) → requires re-registration + Seal #2b. TEST unread; Seal #2 unchanged.

## M3 SEALED thresholds (Seal #2 `6292c018…`, cleaned 854-star null basis)

- **z⋆ = 3.4** (95% CI [3.30, 3.40]) · **z_mono = 5.3** ([5.0, 5.8]) · **T(SDE) = 10.74** ([9.74, 11.34]) · **α_FAP = 1%** (null exceedance 1.08%) · ε = 0.01 · N_min = 2.
- **w_c** (A.5): log-uniform period × K&M-2020 radius prior → 92.8% weight on Rₚ≤2 R⊕. **π̂ = 3.17%** (A.6). A.7 machine: Apple M4 (10 cores).
- Cleaning: 146 excluded (16 EB + 128 variable [overlap] + 14 vetted); **31 high-SDE survivors retained + audited**. M0 null definition preserved.
- **Seal #2 = `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** (owner-approved 2026-06-16). Verify `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.

## M4 dry-run findings + board decisions (2026-06-18) — TEST UNREAD

- **Finding A (fixable):** TLS discards the narrow `[P̂(1±ε)]` window when it holds < 100 periods → returns the full grid; "targeted" search secretly ran full (cost ratio 0.995). In-window-grid fix → ratio 0.010.
- **Finding B (blocking):** TLS SDE is normalized over the searched grid → narrow-grid SDE (3.55) not comparable to full-grid SDE (40.36) / T=10.74. Sealed "targeted TLS, SDE≥T, single common T both arms" is internally inconsistent → E1 fails by construction.
- **Resolution diagnostics:** Option 1 (per-arm T_B, AUC 0.43) + Option 3 (wider window, AUC ≤0.72) **rejected**; **Option 2 — epoch-fixed matched-filter S/N** validated on the cleaned 854-null pool: **AUC 0.877**, range-invariant.
- **Combined-arm system dry-run:** recall-safe route→confirm→full-TLS-fallback. **E1 PASS** (ΔR̄=−0.39 pp, lo −0.80 pp) · **E2 FAIL** (~20–29% < 30%; ρ_d≈12% from B=1000 FAP + 59% FAP-gate fallback). T_red degenerate.
- **Methodology board:** Option-2 **APPROVED CONDITIONALLY as an AMENDMENT** (MATH §6 admits "transit-fit SNR"; NN#3 satisfied). Amends the fairness keystone ("same engine" → "common FAR"). Principle survives; targeted-TLS realization does not.
- **Governance board:** proposed **v3 = FINAL amendment + stopping rule (P-1…P-9)**; pre-commit outcomes; failure → falsification (no v4); new ideas → new experiments. **Pending owner adoption.**
- **E2-fix R&D (exploratory, CALIBRATION-only, no seal change):** the E2 failure is driven by the sealed **B=1000 period-FAP** (ρ_d≈12%) + 59% FAP-gate fallback. A **margined white-noise pre-filter** (reject only at white-FAP > ~5.5·α) skips the bootstrap on **97.5% of noise while clipping ZERO recoverable planets** (validated on injections; the bare white>α loses ~5%) → ρ_d→~0 → projected **E2 ~40% (PASS)**. **E2 is fixable**, but the fix touches **sealed A.8** → expands v3 scope (governance call). Not adopted.
- Reports: `research/m4_evaluation/` — `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Pre-filter R&D: `validate_prefilter{,_injections}.py` + `data/manifests/m4/dry_run/prefilter_*.csv`.

## Next Action

**Seal #2b prep, owner-approved sequence (2026-06-19):** vault sync (this commit) → **transit-LR confirmer implementation-spec review** (last gate before the seal) → Lever-1b equivalence validation (CALIBRATION) → T_red calibration (CALIBRATION) → assemble v3 threshold manifest → cut **Seal #2b** → **single M4 TEST run** → accept the pre-committed verdict (VAL §7a). Hard checkpoints at Seal #2b and immediately before the TEST read (P-5). **TEST stays unread; Seal #2 unchanged; v3 docs are drafts pending the seal.**

## Notes

Repository is authoritative. Obsidian stores research memory. GitHub: github.com/Ansul-S/TRINETRA-X.
