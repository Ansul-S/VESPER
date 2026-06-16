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
**M3 — Threshold calibration → Seal #2 — IN PROGRESS (2026-06-16).** Plan `PHASE1_M3_PLAN.md` **SIGNED OFF** (frozen choices A–G). Untrained machinery built (`research/m3_calibration/`): GP-whitened box matched-filter detector; integer-comb period + circular block bootstrap (B=1000, L_b=3·max(τ_GP,T₁₄)); pinned `transitleastsquares` 1.32 (identical both arms).
- **M3 prerequisite DONE:** M1 noise model recomputed at **2.5 d** (188/188, window-only; 0.5 d archived under `data/manifests/m1/superseded_0.5d/`). Medians: σ 1067→1123, CDPP 1 h 222→250 / 2 h 154→191 / 4 h 98→142 ppm; τ_GP unchanged.
- **DISCOVERY — null-pool contamination.** First null-star calibration: **z⋆ robust (~3.4–3.6)**, but **T and z_mono inflated by unlabeled EBs/variables** ("null" = TOI-removed only). Catalog cleaning (**Prša 2022 EB + VSX**) + automated EB vetting → cleaned 153: z⋆ 3.4, z_mono 14.4→**5.3**, T 19.3→**10.1**, α_FAP exceedance 3.9%→2.0%. **Contamination hypothesis confirmed.**
- **Now running:** ~1000-star cleaned-null calibration for the final FAR≤1%/star T. M0 null definition preserved; cleaned set is a documented derived M3 subset. 5 high-SDE survivors retained (review set).
- **NO Seal #2 yet** — thresholds PROVISIONAL pending owner review of the 1000-star distributions; then decide if the full 6,885 pass is needed.

Next Milestone:
**M4 — Single sealed-TEST evaluation** → primary endpoints E1 (recall non-inferiority) / E2 (scoped compute). Requires Seal #2 first. TEST stays sealed until this run.

Next Action:
1000-star cleaned-null calibration executing (background). On completion: clean → vet → recalibrate → report T, z_mono, α_FAP exceedance, tail composition, T-sensitivity to top survivors → **owner review**. Then instantiate w_c/π̂ (Kunimoto & Matthews 2020), assemble the threshold manifest, and **hash-seal (Seal #2)** only after review. Branch `phase1/m3-calibration`; nothing committed yet (commit on request).

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
