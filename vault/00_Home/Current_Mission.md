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
**M4 — single sealed-TEST run — ✅ DONE (2026-06-24). VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** The single irreversible TEST read was executed once (P-5): 15,000 injections (30 cells × 500, literal ≥500/cell), ~65 h on M4. **E1 recall non-inferiority PASS** (ΔR̄=−0.48 pp, one-sided 95% lo −0.60 pp; margin −2 pp). **E2 scoped compute FAIL** (reduction 24.4%, ratio 0.756, ρ_d=14.4%; target ≥30%). Pre-committed verdict (VAL §7a) applied. Recall principle holds; compute claim is the falsified branch (un-cheapenable B=1000 period-FAP entry tax — the Lever-1b gate had already proven it un-cheapenable). A **successful negative Phase I**. Integrity: both seals hash-verified in-run + intact; `git diff phase1-prereg-v3` empty (NN#2); TEST read exactly once. Result record: `research/m4_evaluation/M4_TEST_RESULT.md`; artifacts `data/manifests/m4/test_run/`. **TEST conditioning** (sanctioned first-touch): 80/80 hosts via frozen Stage-0 (`research/m1_conditioning/condition_test_hosts.py`, exactly the driver's `sample(80, random_state=22)` draw).
- **M3 — Threshold calibration → Seal #2 — ✅ DONE (2026-06-16).** z⋆=3.4 · z_mono=5.3 · T=10.74 · α_FAP=1% · ε=0.01 · N_min=2; w_c (92.8% on Rₚ≤2) · π̂=3.17%; Seal #2 `6292c018…`. Cleaned 854-null basis (146 EB/variable exclusions). Sealed pre-reg docs unmodified.
- **Finding A (implementation, fixable):** TLS discards the narrow `[P̂(1±ε)]` window when it holds < 100 periods (returns full grid) → "targeted" search secretly ran full (ratio 0.995). Feeding in-window periods directly → real saving (ratio 0.010).
- **Finding B (methodology, BLOCKING — confirmed):** TLS **SDE is normalized across the searched grid**, so a narrow-grid SDE (3.55) is not comparable to the full-grid SDE (40.36) that calibrated T=10.74. The sealed "targeted TLS, SDE≥T, single common T both arms" rule is internally inconsistent → Arm B would reject planets Arm A accepts → E1 fails by construction.
- **Resolution (CALIBRATION-only diagnostics):** Option 1 (per-arm narrow-SDE T_B) and Option 3 (wider window) **rejected on evidence** (AUC 0.43 and ≤0.72). **Option 2 — epoch-fixed matched-filter S/N** (evidence-first P̂ + t̂₀; no grid) **validated**: AUC 0.877, FAR-controllable, range-invariant.
- **Combined-arm system dry-run (CALIBRATION-only, 2026-06-18):** full recall-safe Option-2 architecture (route→confirm→full-TLS fallback). **E1 PASS** (ΔR̄=−0.39 pp, one-sided 95% lo −0.80 pp) · **E2 FAIL** (ratio 0.799 → ~20% reduction; population estimate ~29%; <30%). E2 shortfall is structural: ρ_d≈12.4% (sealed B=1000 FAP charged on every routed star) + 59% of routed stars fail the FAP gate → full-TLS fallback. T_red degenerate (FAP gate, not MF, does FP rejection). **Ignore E1/E2 for the philosophical question.**
- **Methodology review-board (2026-06-18): Option-2 APPROVED CONDITIONALLY as an AMENDMENT (not a replacement).** MATH §6 admits "transit-fit SNR" as an arbiter form, so Option-2 complies with Non-Negotiable #3 (folded-photometry significance, not timing coherence; repairs the v3 errors). It **amends the fairness keystone** ("same TLS engine both arms" → "common false-alarm rate"). Conditions: (1) arbiter must be a genuine folded-photometry transit LR (the box depth-SNR is borderline); (2) re-register the keystone change transparently; (3) anti-tuning discipline. The evidence-first **principle survives**; the **targeted-TLS realization does not** (Finding B).
- **Governance review-board (2026-06-18): proposed v3 = FINAL permissible amendment + Phase-I stopping rule (P-1…P-9).** Pre-commit the E1/E2/inconclusive outcome mapping before TEST; one evaluation; failure → pre-committed falsification (no v4); new ideas → new pre-registered experiments. `research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md`. **Pending owner adoption.**
- **E2-fix R&D (2026-06-18, EXPLORATORY — CALIBRATION-only, no seal change):** diagnosed *why* E2 fails (ρ_d≈12% from the sealed **B=1000 period-FAP** + 59% FAP-gate fallback). A **margined white-noise pre-filter** was validated on injections: the *bare* "reject if white-FAP > α" loses ~5% of real planets, but rejecting only at **white-FAP > ~5.5·α** clips **ZERO recoverable planets while still skipping the bootstrap on 97.5% of noise** → ρ_d→~0 → projected **E2 ~25%→~40% (PASS)**. **Implication: E2 is *fixable*, not a fundamental falsification.** BUT the fix touches **sealed A.8 (period-FAP) machinery**, so adopting it would **expand the v3 scope beyond the Option-2 confirmer** (a governance call that bumps the v3-as-final rule). Not adopted; informs the pending decisions. Artifacts: `research/m4_evaluation/validate_prefilter{,_injections}.py`, `data/manifests/m4/dry_run/prefilter_*.csv`.

- **OWNER 4-STEP GATE DECIDED + v3 PACKAGE DRAFTED & APPROVED (2026-06-19).** Owner adopted, in order: **(1)** the v3-as-final stopping rule **P-1…P-9** + pre-committed outcome mapping; **(2)** NN#3 condition #1 = **YES** — the arbiter is a genuine **transit-template likelihood-ratio** (Λ/ΔBIC), box depth-SNR **rejected**; **(3)** v3 **SCOPE = Option-2 confirmer + Lever 1b (period-FAP cheapening), equivalence-gated** — Lever 1a subsumed/excluded, Lever 2 (harmonics) deferred to P-8; **(4)** drafting authorized. **DR-002 ADOPTED** (`docs/decisions/DR-002_DECISION_RECORD.md`). v3 re-registration drafted & owner-approved on governance / consistency / anti-tuning / equivalence-gate / T_red logic: **VAL v3, MATH v1.2, SCIENTIFIC_HYPOTHESIS v2.1** (keystone A6 → common-FAR; Arm-B confirm → transit-LR + full-TLS fallback; A.8a equivalence-gated cheap period-FAP; A.11 confirmer + T_red; §7a stopping rule). Plans: `LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md`, `TRED_CALIBRATION_PLAN.md`. **No sealed numeric value changed; TEST unread; nothing committed/tagged/sealed.**

- **SEAL #2b CUT (2026-06-19) — v3 = CONFIRMER-ONLY.** Tag `phase1-prereg-v3` (annotated → commit `ff869d4b`); v3 manifest `54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18`. **Confirmer spec locked** (transit-LR: D-1a depth-only linear GLS · D-2a GP marginal likelihood · D-3-i no t₀ refinement; box depth-SNR rejected). **Lever-1b equivalence FAILED both candidates** (E-EVT: p95 ΔFAP 0.085, 7 FP-admit, 2 clipped; E-LUT: 0.104, 9 FP-admit, 2 clipped) → pre-committed fallback → period-FAP stays sealed B=1000 bootstrap, **ρ_d≈12.4% retained**. **T_red=0.0** (non-binding, FAR-calibrated; end-to-end Arm-B FAR 0.12%; confirmer rejects 8/9 FAP-gate-passing nulls; AUC 0.894). No sealed numeric value changed; TEST unread; Seal #1/#2 intact. Evidence: `research/m4_evaluation/LEVER1B_EQUIVALENCE_RESULT.md`, `TRED_CALIBRATION_RESULT.md`; manifest `data/manifests/m4/v3/`.

- **M4 DRIVER BUILT + DRESS REHEARSAL COMPLETE (2026-06-20, CALIBRATION-only).** `m4_driver.py` (one driver for dry-run + token-gated TEST): Arm A full TLS; Arm B route→B=1000 FAP gate→transit-LR confirmer (sealed T_red=0)→full-TLS fallback; E1 occurrence-weighted ΔR̄+one-sided 95% CI; E2 compute ledger; dual hash-verify + TEST token guard. Instrumented dress rehearsal (240 injections, per-cell 8): **E1 PASS** (ΔR̄=−0.17 pp, lo95=−0.51 pp; the earlier per-cell-5 "fail" lo −5.19 was underpowered noise) · **E2 FAIL** (reduction −5.6%, ρ_d=0.138). **Verdict: FALSIFIED — compute branch (E1 pass, E2 fail).** Recall-loss fully characterized: 14/240 losses, **ALL one pathway** (cheap-confirm suppresses fallback), 11 right-period/wrong-epoch (detector t̂₀ less precise than TLS T₀) + 3 wrong-period; **sub-margin**, does not threaten E1. Genuine limitation = E2 (un-cheapenable B=1000 FAP entry tax), not a confirmer bug. Readiness: `research/m4_evaluation/M4_DRESS_REHEARSAL_READINESS.md`.

Next Milestone:
**M7 — Phase-I write-up** (the result is in; M5/M6 coverage/ablation are optional extensions, not gates on the headline verdict). Report the negative result with equal rigor: recall non-inferiority supported, compute claim falsified, traced to the un-cheapenable sealed period-FAP. Candidate future work is **P-8 territory only** (new, separately pre-registered experiments): equivalence-proven cheaper period-FAP, multi-harmonic testing, recall-protective confirmer floor, clean-skip tier — none a continuation of this experiment (P-2: no v4).

Next Action:
**Phase-I result is final and recorded.** (1) Optional: open a PR to merge `phase1/m4-v3-seal2b` → `main` (owner action). (2) Begin the Phase-I write-up from `research/m4_evaluation/M4_TEST_RESULT.md` + `docs/PAPER_NOTES.md`. No further amendment permitted (P-2/P-8); v3 is final; TEST has been read once and will not be read again.

Execution Plan:
`PHASE1_M4_PLAN.md` (M4 execution plan). Dry-run + diagnostics + governance: `research/m4_evaluation/` — reports `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Diagnostic data: `data/manifests/m4/dry_run/`.

Sealed Documents (SEALED at `phase1-prereg-v3`, 2026-06-19; do not edit without a new re-registration — but P-2 forbids a v4):
- SCIENTIFIC_HYPOTHESIS.md — **v2.1 SEALED**
- TRINETRA_X_PHASE1_VALIDATION.md — **v3 SEALED** (incl. App A: A.8a no cheap estimator, A.11 transit-LR + T_red; §7a stopping rule)
- TRINETRA_MATHEMATICAL_FOUNDATIONS.md — **v1.2 SEALED**
- v3 threshold manifest `data/manifests/m4/v3/m4_v3_threshold_manifest.json` (Seal #2b `54f06a94…`).
- Tags: `phase1-prereg-v2` (v2 baseline) · `phase1-prereg-v3` (v3, → commit `ff869d4b`).

Decision Records:
docs/decisions/F1_DECISION_RECORD.md (DR-001) · docs/decisions/DR-002_DECISION_RECORD.md (DR-002 — Finding B, Option-2 v3 amendment, stopping rule)

GitHub:
origin = https://github.com/Ansul-S/TRINETRA-X — main and tag `phase1-prereg-v2` pushed.

Anti-tuning status:
M0 read **catalog metadata only** (no flux). All calibration/amendment decisions (M1–M3, v3/Seal #2b, dress rehearsal) were made TEST-blind. **TEST was read exactly once (2026-06-24, P-5)** — the single sealed M4 evaluation. The sealed protocol was frozen *before* the read: `git diff phase1-prereg-v3` over sealed docs + manifests is **empty**, both seals hash-verified in-run and intact, no threshold/statistic/weight/config moved. The verdict (E1 pass / E2 fail) was pre-committed (VAL §7a) before the read. Anti-tuning (NN#2) intact end-to-end. **TEST will not be read again** (P-2: v3 is final; no v4).

Non-blocking follow-ons (do not affect sealed hashes):
- Create references.bib (Kunimoto & Matthews 2020 is load-bearing)
- Add the one-line Phase-I scoping note to the charter (docs/TRINETRA-X.md)
