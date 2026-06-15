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
**M1 — Stage-0 conditioning — η-sample done (2026-06-15).** 188/200 calibration targets conditioned (wotan biweight 0.5 d + quality/momentum masks → r(t)); σ med 1067 ppm, CDPP(1h) med 222 ppm, τ_GP med ~8 min; **99 % stationary / 88 % white** (12 % active-star tail flagged). Config frozen (`m1_config.yaml`); calibration-only; TEST untouched. (M0 — DONE; Seal #1 `1f2d49e1…`.)

Next Milestone:
**M2 — injection harness + η ≥ 0.90 transit-preservation check** (finalizes the detrend window; VAL §4.2). Not started.

Next Action:
Owner steer needed: (a) proceed to **M2** (inject Mandel–Agol transits → condition → measure η = δ_post/δ_true per (P,R_p) cell; window widened where η < 0.90 before any M3 threshold), and/or (b) scale conditioning to the full 6,925 calibration pool (otherwise done on demand at detection M3/M4). TEST sealed until M4; Seal #2 (thresholds) at M3.

Execution Plan:
`PHASE1_EXECUTION_PLAN.md` (v0.1, M0 increment — M0 executed). Tooling: `research/m0_manifest/`. Manifest + provenance: `data/manifests/m0/`.

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
