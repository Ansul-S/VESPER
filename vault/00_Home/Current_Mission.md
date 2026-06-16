# Current Mission

Project:
TRINETRA-X

Current Phase:
Phase I — Scientific Validation

Current Goal:
Determine whether evidence-first routing can reduce computational cost while preserving recall.

Current Status:
- Pre-registration **v2 SEALED** — git tag `phase1-prereg-v2` (commit `723087e`), pushed to GitHub.
- Decision **DR-001** recorded (F1 compute-scope decision).
- **No remaining Critical, Must-fix, or Should-fix findings.** (F1, F2, F6, F8 resolved; R-4, R-5, R-6, R-7 folded into v2.)
- **M0 EXECUTED (2026-06-15).** Seal #1 (manifest hash) `1f2d49e1…` cut; 22,723 SPOC 2-min targets (S1–S3 south); leakage-safe 30/70 split; TEST set sealed (read once at M4). M0.5 feasibility passed — no sector widening needed.

Current Milestone:
**M3 — Threshold calibration → Seal #2 — ✅ DONE (2026-06-16).** Plan `PHASE1_M3_PLAN.md` signed (A–G); untrained machinery built (`research/m3_calibration/`): GP-whitened box matched-filter detector; integer-comb period + circular block bootstrap (B=1000, L_b=3·max(τ_GP,T₁₄)); pinned `transitleastsquares` 1.32 (identical both arms).
- **Prerequisite:** M1 noise model recomputed at **2.5 d** (188/188; 0.5 d archived).
- **Null-pool contamination found + cleaned (owner-directed).** "Null" = TOI-removed only → unlabeled EBs/variables inflated T and z_mono (z⋆ robust). Resolved via **Prša 2022 EB + VSX** cross-match (132) + automated EB vetting (14) → **146 excluded → cleaned 854** of 1000. M0 null definition preserved; **31 high-SDE survivors retained + audited**.
- **Sealed thresholds (bootstrap B=1000 CIs):** **z⋆ = 3.4** [3.30,3.40] · **z_mono = 5.3** [5.0,5.8] · **T = 10.74** [9.74,11.34] · **α_FAP = 1%** (exceedance 1.08%) · ε = 0.01 · N_min = 2. **w_c** (92.8% on Rₚ≤2; A.5) · **π̂ = 3.17%** (A.6) from Kunimoto & Matthews 2020. A.7 machine = Apple M4 (10 cores).
- **Seal #2 RECORDED (owner-approved 2026-06-16): SHA-256 `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** (distinct from Seal #1 `1f2d49e1…`). Verify: `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`. Sealed pre-reg docs unmodified; TEST untouched (0 TEST TICs in any M3 artifact).
- **Note (sealed record):** occurrence-weighted E1 expected to be **dominated by Rₚ≤2 R⊕** (K&M weighting + M2 noise-limited Rₚ=1); recovered via TLS fallback, not single-transit conditioning.

Next Milestone:
**M4 — Single sealed-TEST evaluation** → primary endpoints E1 (recall non-inferiority) / E2 (scoped compute). Seal #2 now in place. **TEST stays sealed until this single run.**

Next Action:
**Begin M4 — the single sealed-TEST run** against Seal #2 (`6292c018…`): apply the frozen machinery + thresholds to the TEST split exactly once → E1/E2. Anti-tuning: TEST read for the first time at M4; no threshold/config change permitted. Branch `phase1/m3-calibration`; M3 work + Seal #2 to be committed.

Execution Plan:
`PHASE1_EXECUTION_PLAN.md` (v0.1, M0). M3: `PHASE1_M3_PLAN.md` (signed). Tooling: `research/m3_calibration/`. Provisional artifacts: `data/manifests/m3/` (185 diagnostic under `diagnostic_185/`).

Sealed Documents (do not edit without a new re-registration):
- SCIENTIFIC_HYPOTHESIS.md — v2.0
- TRINETRA_X_PHASE1_VALIDATION.md — v2 (incl. Appendix A: frozen parameters)
- TRINETRA_MATHEMATICAL_FOUNDATIONS.md — v1.1

Decision Record:
docs/decisions/F1_DECISION_RECORD.md (DR-001)

GitHub:
origin = https://github.com/Ansul-S/TRINETRA-X — main and tag `phase1-prereg-v2` pushed.

Anti-tuning status:
M0 read **catalog metadata only** (no flux). TEST split **sealed at M0** (read once at M4). **Seal #2** (calibration threshold manifest hash) happens at M3, before the single M4 run. Sealed prereg docs verified byte-identical to `phase1-prereg-v2`.

Non-blocking follow-ons (do not affect sealed hashes):
- Create references.bib (Kunimoto & Matthews 2020 is load-bearing)
- Add the one-line Phase-I scoping note to the charter (docs/TRINETRA-X.md)
