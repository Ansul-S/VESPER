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
- **M3 — threshold calibration → Seal #2 — ▶ IN PROGRESS** (plan signed; machinery built; null cleaning under way; **no Seal #2 yet**)

## Milestone Ladder

- Pre-registration completion + seal — ✅ DONE (2026-06-15)
- M0 execution plan authored + approved — ✅ DONE (2026-06-15)
- **M0 — Freeze sector/target manifest + leakage-safe split** — ✅ DONE — Seal #1 `1f2d49e1…`; 22,723 targets (S1–S3); cal 6,925 / test 15,798 (2026-06-15)
- **M1 — Stage-0 conditioning** (per-sector biweight detrend + masking → r(t); noise model σ/CDPP/τ_GP) — ✅ DONE (η-sample 188/200, 2026-06-15)
- **M2 — Injection + η ≥ 0.90 transit-preservation** — ✅ DONE — window finalized 2.5 d; gate PASS (Rₚ≥2); Rₚ=1 row noise-limited, 0.5/2 borderline (2026-06-16)
- **M3 — Threshold calibration (calibration only) → Seal #2** — ▶ IN PROGRESS — plan signed (A–G); untrained machinery built (whitened MF detector · integer-comb period + block bootstrap · pinned TLS 1.32); M1 noise model recomputed at 2.5 d; **null-pool contamination found + being cleaned** (Prša 2022 + VSX + vetting); 1000-star cleaned calibration running; PROVISIONAL thresholds, **no Seal #2** (2026-06-16)
- M4 — Sealed-test evaluation (single run)
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

## M3 provisional thresholds (PRE-SEAL, diagnostic 153-star cleaned)

- z⋆ ≈ **3.4** (≤1 false event/LC) · z_mono ≈ **5.3** (≤0.1/LC) · T(SDE) ≈ **10.1** (FAR≤1%/star) · α_FAP exceedance **2.0%** (target 1%) · ε = 0.01 · N_min = 2.
- Being re-derived on ~1000 cleaned null stars; **not sealed**.

## Next Action

M3 in progress: 1000-star cleaned-null calibration running. On completion → clean/vet/recalibrate → report (T, z_mono, α_FAP, tail composition, survivor sensitivity) → **owner review before Seal #2**. Then w_c/π̂ (Kunimoto & Matthews 2020) + threshold-manifest hash. TEST sealed until M4.

## Notes

Repository is authoritative. Obsidian stores research memory. GitHub: github.com/Ansul-S/TRINETRA-X.
