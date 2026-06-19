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
**M4 — single sealed-TEST run — ⛔ BLOCKED (2026-06-18) pending a protocol amendment (Finding B).** The M4 harness was built (`research/m4_evaluation/`) and the **CALIBRATION/synthetic dry-run completed end-to-end. TEST was NEVER read** (hard-blocked by the guard); Seal #2 unchanged; no sealed value modified.
- **M3 — Threshold calibration → Seal #2 — ✅ DONE (2026-06-16).** z⋆=3.4 · z_mono=5.3 · T=10.74 · α_FAP=1% · ε=0.01 · N_min=2; w_c (92.8% on Rₚ≤2) · π̂=3.17%; Seal #2 `6292c018…`. Cleaned 854-null basis (146 EB/variable exclusions). Sealed pre-reg docs unmodified.
- **Finding A (implementation, fixable):** TLS discards the narrow `[P̂(1±ε)]` window when it holds < 100 periods (returns full grid) → "targeted" search secretly ran full (ratio 0.995). Feeding in-window periods directly → real saving (ratio 0.010).
- **Finding B (methodology, BLOCKING — confirmed):** TLS **SDE is normalized across the searched grid**, so a narrow-grid SDE (3.55) is not comparable to the full-grid SDE (40.36) that calibrated T=10.74. The sealed "targeted TLS, SDE≥T, single common T both arms" rule is internally inconsistent → Arm B would reject planets Arm A accepts → E1 fails by construction.
- **Resolution (CALIBRATION-only diagnostics):** Option 1 (per-arm narrow-SDE T_B) and Option 3 (wider window) **rejected on evidence** (AUC 0.43 and ≤0.72). **Option 2 — epoch-fixed matched-filter S/N** (evidence-first P̂ + t̂₀; no grid) **validated**: AUC 0.877, FAR-controllable, range-invariant.
- **Combined-arm system dry-run (CALIBRATION-only, 2026-06-18):** full recall-safe Option-2 architecture (route→confirm→full-TLS fallback). **E1 PASS** (ΔR̄=−0.39 pp, one-sided 95% lo −0.80 pp) · **E2 FAIL** (ratio 0.799 → ~20% reduction; population estimate ~29%; <30%). E2 shortfall is structural: ρ_d≈12.4% (sealed B=1000 FAP charged on every routed star) + 59% of routed stars fail the FAP gate → full-TLS fallback. T_red degenerate (FAP gate, not MF, does FP rejection). **Ignore E1/E2 for the philosophical question.**
- **Methodology review-board (2026-06-18): Option-2 APPROVED CONDITIONALLY as an AMENDMENT (not a replacement).** MATH §6 admits "transit-fit SNR" as an arbiter form, so Option-2 complies with Non-Negotiable #3 (folded-photometry significance, not timing coherence; repairs the v3 errors). It **amends the fairness keystone** ("same TLS engine both arms" → "common false-alarm rate"). Conditions: (1) arbiter must be a genuine folded-photometry transit LR (the box depth-SNR is borderline); (2) re-register the keystone change transparently; (3) anti-tuning discipline. The evidence-first **principle survives**; the **targeted-TLS realization does not** (Finding B).
- **Governance review-board (2026-06-18): proposed v3 = FINAL permissible amendment + Phase-I stopping rule (P-1…P-9).** Pre-commit the E1/E2/inconclusive outcome mapping before TEST; one evaluation; failure → pre-committed falsification (no v4); new ideas → new pre-registered experiments. `research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md`. **Pending owner adoption.**
- **E2-fix R&D (2026-06-18, EXPLORATORY — CALIBRATION-only, no seal change):** diagnosed *why* E2 fails (ρ_d≈12% from the sealed **B=1000 period-FAP** + 59% FAP-gate fallback). A **margined white-noise pre-filter** was validated on injections: the *bare* "reject if white-FAP > α" loses ~5% of real planets, but rejecting only at **white-FAP > ~5.5·α** clips **ZERO recoverable planets while still skipping the bootstrap on 97.5% of noise** → ρ_d→~0 → projected **E2 ~25%→~40% (PASS)**. **Implication: E2 is *fixable*, not a fundamental falsification.** BUT the fix touches **sealed A.8 (period-FAP) machinery**, so adopting it would **expand the v3 scope beyond the Option-2 confirmer** (a governance call that bumps the v3-as-final rule). Not adopted; informs the pending decisions. Artifacts: `research/m4_evaluation/validate_prefilter{,_injections}.py`, `data/manifests/m4/dry_run/prefilter_*.csv`.

- **OWNER 4-STEP GATE DECIDED + v3 PACKAGE DRAFTED & APPROVED (2026-06-19).** Owner adopted, in order: **(1)** the v3-as-final stopping rule **P-1…P-9** + pre-committed outcome mapping; **(2)** NN#3 condition #1 = **YES** — the arbiter is a genuine **transit-template likelihood-ratio** (Λ/ΔBIC), box depth-SNR **rejected**; **(3)** v3 **SCOPE = Option-2 confirmer + Lever 1b (period-FAP cheapening), equivalence-gated** — Lever 1a subsumed/excluded, Lever 2 (harmonics) deferred to P-8; **(4)** drafting authorized. **DR-002 ADOPTED** (`docs/decisions/DR-002_DECISION_RECORD.md`). v3 re-registration drafted & owner-approved on governance / consistency / anti-tuning / equivalence-gate / T_red logic: **VAL v3, MATH v1.2, SCIENTIFIC_HYPOTHESIS v2.1** (keystone A6 → common-FAR; Arm-B confirm → transit-LR + full-TLS fallback; A.8a equivalence-gated cheap period-FAP; A.11 confirmer + T_red; §7a stopping rule). Plans: `LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md`, `TRED_CALIBRATION_PLAN.md`. **No sealed numeric value changed; TEST unread; nothing committed/tagged/sealed.**

Next Milestone:
**Seal #2b (v3 re-registration), then M4 — executing the owner-approved sequence.** Remaining gate before the seal: **one final implementation-spec review of the transit-LR confirmer** (the genuine Λ, per A.11 / MATH §6). Then, in order: vault sync → **confirmer spec review** → Lever-1b equivalence validation (CALIBRATION) → T_red calibration (CALIBRATION) → assemble v3 threshold manifest → **cut Seal #2b** → **single M4 TEST run** → accept the pre-committed verdict (E1/E2/inconclusive, VAL §7a). Hard checkpoints at Seal #2b and immediately before the irreversible TEST read (P-5).

Next Action:
**Vault sync (in progress), then draft the transit-LR confirmer implementation spec for owner review** — the last gate before Seal #2b. Lever-1b equivalence + T_red calibration runs proceed once the confirmer spec is signed off (both depend on it). **TEST stays unread; Seal #2 unchanged; v3 docs are drafts pending Seal #2b.**

Execution Plan:
`PHASE1_M4_PLAN.md` (M4 execution plan). Dry-run + diagnostics + governance: `research/m4_evaluation/` — reports `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Diagnostic data: `data/manifests/m4/dry_run/`.

Sealed Documents (do not edit without a new re-registration):
- SCIENTIFIC_HYPOTHESIS.md — **v2.1 drafted (pending Seal #2b)**; sealed baseline v2.0 (`phase1-prereg-v2`)
- TRINETRA_X_PHASE1_VALIDATION.md — **v3 drafted (pending Seal #2b)**; sealed baseline v2 (incl. Appendix A)
- TRINETRA_MATHEMATICAL_FOUNDATIONS.md — **v1.2 drafted (pending Seal #2b)**; sealed baseline v1.1
- *The `phase1-prereg-v2` tag preserves the v2 baseline immutably; v3 drafts are owner-approved but not yet sealed.*

Decision Records:
docs/decisions/F1_DECISION_RECORD.md (DR-001) · docs/decisions/DR-002_DECISION_RECORD.md (DR-002 — Finding B, Option-2 v3 amendment, stopping rule)

GitHub:
origin = https://github.com/Ansul-S/TRINETRA-X — main and tag `phase1-prereg-v2` pushed.

Anti-tuning status:
M0 read **catalog metadata only** (no flux). **TEST split remains UNREAD** — the M4 dry-run (2026-06-18) used CALIBRATION/synthetic hosts only and was hard-blocked from TEST. **Seal #2 unchanged**; sealed prereg docs verified byte-identical to `phase1-prereg-v2`. The pending Option-2 amendment will be decided on CALIBRATION and sealed (Seal #2b) **before** the single TEST run — a legitimate pre-TEST amendment.

Non-blocking follow-ons (do not affect sealed hashes):
- Create references.bib (Kunimoto & Matthews 2020 is load-bearing)
- Add the one-line Phase-I scoping note to the charter (docs/TRINETRA-X.md)
