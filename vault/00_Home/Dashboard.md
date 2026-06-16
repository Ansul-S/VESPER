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
- **Current milestone — M4 (single sealed-TEST run → E1/E2)** ▶ NEXT

## Milestone Ladder

- Pre-registration completion + seal — ✅ DONE (2026-06-15)
- M0 execution plan authored + approved — ✅ DONE (2026-06-15)
- **M0 — Freeze sector/target manifest + leakage-safe split** — ✅ DONE — Seal #1 `1f2d49e1…`; 22,723 targets (S1–S3); cal 6,925 / test 15,798 (2026-06-15)
- **M1 — Stage-0 conditioning** (per-sector biweight detrend + masking → r(t); noise model σ/CDPP/τ_GP) — ✅ DONE (η-sample 188/200, 2026-06-15)
- **M2 — Injection + η ≥ 0.90 transit-preservation** — ✅ DONE — window finalized 2.5 d; gate PASS (Rₚ≥2); Rₚ=1 row noise-limited, 0.5/2 borderline (2026-06-16)
- **M3 — Threshold calibration (calibration only) → Seal #2** — ✅ DONE — untrained machinery built (whitened MF detector · integer-comb period + block bootstrap · pinned TLS 1.32); M1 noise model recomputed at 2.5 d; null-pool contamination found + cleaned (Prša 2022 + VSX + vetting → 854 of 1000); thresholds bootstrap-stable; w_c/π̂ instantiated; **Seal #2 `6292c018…`** (2026-06-16)
- **M4 — Sealed-test evaluation (single run) → E1/E2** — ▶ NEXT (against Seal #2; TEST read once)
- M5/M6 — Parameter coverage, reality check, ablation
- M7 — Write-up

## Sealed Documents (pre-registration set, hash-verified)

- SCIENTIFIC_HYPOTHESIS.md — v2.0
- TRINETRA_X_PHASE1_VALIDATION.md — v2 (incl. Appendix A)
- TRINETRA_MATHEMATICAL_FOUNDATIONS.md — v1.1

## Other Repository Documents

- TRINETRA-X.md (charter) · TRINETRA_X_ARCHITECTURE.md · TRINETRA_CONCEPT_RECONSTRUCTION.md
- REPOSITORY_GAP_ANALYSIS.md (F1–F12) · PHASE1_REMEDIATION.md
- PHASE1_READINESS_REPORT.md · decisions/F1_DECISION_RECORD.md (DR-001)
- PAPER_NOTES.md · references.bib · **SESSION_HANDOFF_2026-06-16.md** (latest)
- **Execution plans / choices:** PHASE1_EXECUTION_PLAN.md (M0) · PHASE1_M0_CHOICES.md · PHASE1_M1_PLAN.md · PHASE1_M2_PLAN.md · **PHASE1_M3_PLAN.md (signed)**
- **Tooling:** research/m0_manifest/ · research/m1_conditioning/ · research/m2_injection/ · **research/m3_calibration/**
- **Artifacts/provenance:** data/manifests/m0 (Seal #1) · m1 (noise summary, 2.5 d + superseded_0.5d) · m2 (η table) · **m3 (provisional thresholds + exclusions; diagnostic_185/)**

## Findings Status

- Critical/Must-fix: F1, F2, F6, F8 — ✅ resolved and sealed
- Should-fix: R-4, R-5, R-6, R-7 — ✅ folded into v2 seal
- F7 (charter scoping note) — ✅ done; references.bib — ✅ created
- Remaining: Low hygiene only (F9 BLS wording) — non-blocking
- **M3 finding — null-pool contamination (R0-3/H4):** TOI-removed "null" pool retains unlabeled EBs/variables that inflate T and z_mono; resolved by Prša 2022 + VSX cross-match + automated EB vetting (derived M3 calibration subset; M0 null definition preserved). z⋆ unaffected.

## M3 SEALED thresholds (Seal #2 `6292c018…`, cleaned 854-star null basis)

- **z⋆ = 3.4** (95% CI [3.30, 3.40]) · **z_mono = 5.3** ([5.0, 5.8]) · **T(SDE) = 10.74** ([9.74, 11.34]) · **α_FAP = 1%** (null exceedance 1.08%) · ε = 0.01 · N_min = 2.
- **w_c** (A.5): log-uniform period × K&M-2020 radius prior → 92.8% weight on Rₚ≤2 R⊕. **π̂ = 3.17%** (A.6). A.7 machine: Apple M4 (10 cores).
- Cleaning: 146 excluded (16 EB + 128 variable [overlap] + 14 vetted); **31 high-SDE survivors retained + audited**. M0 null definition preserved.
- **Seal #2 = `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** (owner-approved 2026-06-16). Verify `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.

## Next Action

**M4 — the single sealed-TEST run** against Seal #2: apply frozen machinery + thresholds to the TEST split exactly once → E1 (recall non-inferiority) / E2 (scoped compute). TEST read for the first time at M4; no threshold/config change permitted. Sealed pre-reg docs unmodified; TEST untouched to date.

## Notes

Repository is authoritative. Obsidian stores research memory. GitHub: github.com/Ansul-S/TRINETRA-X.
