# Current Mission

> **AUTHORITATIVE CURRENT STATE — updated 2026-06-30 (EOD).** The detailed fields below this block are **Phase-I historical record** (kept for provenance); read this block first.

## ▶ Latest event: identity rebrand + first public release (2026-06-30)

**The project was rebranded from codename `TRINETRA-X` to `VESPER`** (the old name was already in use elsewhere). **Branding only — no science, methodology, equations, thresholds, results, or figures changed.** Acronym locked: **VESPER = Validation Engine for Stellar Photometric Evidence and Recovery** (also the evening star). The root folder is now `~/Desktop/VESPER` and the GitHub repo is **`github.com/Ansul-S/VESPER`**.

- **First public release `v1.0.0` cut** — annotated tag on `main` HEAD `0118548` + GitHub Release "VESPER v1.0.0 — Initial Public Release". `main` == `origin/main`; tree clean.
- **Sealed-artifact hash note:** rebranding the sealed docs/manifests **changed their recorded SHA-256 digests by design** (owner-authorized). See **`docs/decisions/F1_DECISION_RECORD.md` §5a** — any mismatch is from the naming change only; original sealed bytes are intact at tags `phase1-prereg-v2/v3`. ⚠️ `shasum` against the *old* recorded hashes will mismatch — read §5a first.
- **Phase I unchanged:** still COMPLETE / SEALED / FINAL. **Active substantive task is unchanged:** the hackathon block below. See `SESSION_HANDOFF_2026-06-30.md`.

## ▶ Where the project is now (2026-06-29)

**Active track: BAH 2026 — Problem Statement 7 (ISRO Bharatiya Antariksh Hackathon).** A new *applied* track, an **extension/attachment to VESPER** (not a fork). Lives under `hackathon/`, **merged to `main` via PR #14** (merge commit `9d72920`, 2026-06-27).

- **Phase I (TESS) — COMPLETE & SEALED & FINAL.** M0–M7 done and merged (PRs #1–#13). H1 **falsified on the compute branch** (E1 recall non-inferiority PASS; E2 scoped compute FAIL 24.4% < 30%); recall principle **supported**. v3 is terminal — **no v4** (P-2). Seals intact: #2 `6292c018…`, #2b `54f06a94…`.
- **Phase II (Kepler scaling) — FROZEN until after the hackathon** (owner decision 2026-06-26). The compute-path decision (HPC vs AWS) is likewise deferred. Sketch: `docs/PHASE2_KEPLER_SCALING_PREREG.md` (on the unmerged `phase2/kepler-scaling-prereg` branch).

### Hackathon status (BAH 2026 · PS7)
- **Round-1 submission package is COMPLETE** (deadline **2026-07-01**): proposal web-form text + 11-slide PDF deck (`hackathon/deck/BAH2026_PS7_idea_deck.pdf`) + report skeleton. Team **VESPER** (Ansul Suryawanshi lead / IGNOU; Riddhi Jain / IGNOU; Samiksha Choudhary / Priyadarshini CoE Nagpur — 3 members, 4th optional).
- **Working prototype validated on real MAST data** covering all 5 PS7 steps (detrend→identify→characterize→classify→significance). Trapezoid shape-fit reproduces the committee's slide-5/6 output; pipeline validated on 12 known objects (planets U vs EBs V).
- **Owner actions left for round 1:** paste proposal fields + upload PDF before 2026-07-01.
- **Round 2 (if shortlisted, ~Aug):** plug organizer's curated labels into the classifier; add robust period recovery + phase-curve handling + pixel-level centroid (blends) + optional CNN.

**Next action:** submit round 1 before 2026-07-01. See `SESSION_HANDOFF_2026-06-29.md`.

---

*(Phase-I historical record follows — provenance only.)*

Project:
VESPER

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
**M7 — Phase-I write-up (well advanced).** Draft v0.1 in `papers/phase1_evidence_first_triage.md`; tables T2/T3/T7 + figures F3/F8 (M4), T4/T5 + F5/F6 (M5), T6/T8/T5-depth + F5b/c (M6) generated. `docs/references.bib` compiled (ADS-verify pending). PRs #9/#10/#11 merged to `main`; M6 PR pending. **M5 + M6 EXECUTED (2026-06-25, test-blind characterization)** — see Current Milestone history below. Remaining for M7: compile/verify references, optional F1/F4/F7/F9/T1, venue decision. Future architectural ideas are **P-8 only** (new pre-registered experiments); no v4 (P-2).

Next Action:
**Finish the M7 write-up** from the manuscript draft + PAPER_NOTES (M4/M5/M6 results all folded in). Bundle the M6 PR (`phase1/m6-plan` → `main`). No further amendment (P-2/P-8); v3 is final; TEST read once and will not be read again. M6 was characterization only (calibration + real TOI/EB objects; TEST never touched; sealed thresholds unchanged).

Execution Plan:
`PHASE1_M4_PLAN.md` (M4 execution plan). Dry-run + diagnostics + governance: `research/m4_evaluation/` — reports `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Diagnostic data: `data/manifests/m4/dry_run/`.

Sealed Documents (SEALED at `phase1-prereg-v3`, 2026-06-19; do not edit without a new re-registration — but P-2 forbids a v4):
- SCIENTIFIC_HYPOTHESIS.md — **v2.1 SEALED**
- VESPER_PHASE1_VALIDATION.md — **v3 SEALED** (incl. App A: A.8a no cheap estimator, A.11 transit-LR + T_red; §7a stopping rule)
- VESPER_MATHEMATICAL_FOUNDATIONS.md — **v1.2 SEALED**
- v3 threshold manifest `data/manifests/m4/v3/m4_v3_threshold_manifest.json` (Seal #2b `54f06a94…`).
- Tags: `phase1-prereg-v2` (v2 baseline) · `phase1-prereg-v3` (v3, → commit `ff869d4b`).

Decision Records:
docs/decisions/F1_DECISION_RECORD.md (DR-001) · docs/decisions/DR-002_DECISION_RECORD.md (DR-002 — Finding B, Option-2 v3 amendment, stopping rule)

GitHub:
origin = https://github.com/Ansul-S/VESPER — `main` pushed; tags `phase1-prereg-v2`, `phase1-prereg-v3`, `m0-manifest-v1`, and release `v1.0.0` (2026-06-30) on the remote.

Anti-tuning status:
M0 read **catalog metadata only** (no flux). All calibration/amendment decisions (M1–M3, v3/Seal #2b, dress rehearsal) were made TEST-blind. **TEST was read exactly once (2026-06-24, P-5)** — the single sealed M4 evaluation. The sealed protocol was frozen *before* the read: `git diff phase1-prereg-v3` over sealed docs + manifests is **empty**, both seals hash-verified in-run and intact, no threshold/statistic/weight/config moved. The verdict (E1 pass / E2 fail) was pre-committed (VAL §7a) before the read. Anti-tuning (NN#2) intact end-to-end. **TEST will not be read again** (P-2: v3 is final; no v4).

Non-blocking follow-ons (do not affect sealed hashes):
- Create references.bib (Kunimoto & Matthews 2020 is load-bearing)
- Add the one-line Phase-I scoping note to the charter (docs/VESPER.md)
