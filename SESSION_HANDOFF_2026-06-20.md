# SESSION HANDOFF — 2026-06-20 (EOD) — v3 SEALED (#2b) + M4 dress rehearsal; single TEST read authorized, held at scale

| Field | Value |
|-------|-------|
| **Purpose** | Resume TRINETRA-X with **zero reliance on chat history**. |
| **Phase** | Phase I — Scientific Validation |
| **Status** | M0–M3 sealed; **v3 re-registration SEALED (Seal #2b, confirmer-only)**; M4 driver built; **CALIBRATION dress rehearsal complete** (E1 pass / E2 fail → FALSIFIED–compute). **TEST never read.** Single TEST read **authorized by owner**, paused only at the **scale choice**. |
| **Read first** | `CLAUDE.md` → this file → `docs/decisions/DR-002_DECISION_RECORD.md` → `research/m4_evaluation/M4_DRESS_REHEARSAL_READINESS.md` → `research/m4_evaluation/LEVER1B_EQUIVALENCE_RESULT.md` → `TRED_CALIBRATION_RESULT.md`. |

> Authority: repository documents are authoritative; vault mirrors them; this handoff is a pointer. Sealed documents govern on conflict. Supersedes `SESSION_HANDOFF_2026-06-18.md`.

---

## 1. One-paragraph state
The targeted-TLS confirmation was non-executable (Finding B). A v3 re-registration (DR-002) was drafted, owner-approved, and **sealed (Seal #2b)** as **confirmer-only**: Arm-B confirmation is now a folded-photometry **transit likelihood-ratio** (keystone A6 relaxed "same engine" → "common false-alarm rate"). The **Lever-1b** period-FAP cheapening was **dropped** because **both** pre-registered cheap estimators (E-EVT, E-LUT) **failed the numerical-equivalence gate** on calibration → the sealed B=1000 bootstrap stands, ρ_d≈12.4% retained. **T_red=0.0** (FAR-calibrated, non-binding; end-to-end Arm-B FAR 0.12%). The **M4 driver** was built and **dress-rehearsed on CALIBRATION**: **E1 PASS** (ΔR̄=−0.17 pp, lo95=−0.51 pp) / **E2 FAIL** (−5.6%, ρ_d 0.138) → **pre-committed verdict FALSIFIED — compute branch**. The recall-loss mechanism was fully characterized (one sub-margin pathway). The owner **authorized the single irreversible TEST read**; it is **paused only at the scale decision** (≈per-cell 50 under VAL §6's realized-CI rule, ~3–5 h, vs literal ≥500/cell, ~1.5–2 days — same expected verdict).

## 2. Integrity (verify on resume)
- `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` → `6292c018…32692` (Seal #2) ✓
- `shasum -a 256 data/manifests/m4/v3/m4_v3_threshold_manifest.json` → `54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18` (Seal #2b) ✓
- Seal #1 (M0) = `1f2d49e1…`. Tags: `phase1-prereg-v2`, `phase1-prereg-v3` (annotated → seal commit `ff869d4b`). Branch `phase1/m4-v3-seal2b`.
- **TEST split UNREAD; 0 TEST TICs** in all M4 artifacts (substring "leak" flags were false positives in float values; runtime `cleaned ⊆ calibration` assertions passed).

## 3. What was sealed in v3 (Seal #2b, confirmer-only)
- **Carried forward UNCHANGED from Seal #2:** z⋆=3.4, z_mono=5.3, N_min=2, T=10.74, α_FAP=1%, ε=0.01, w_c, π̂=3.17%.
- **Keystone A6:** "same TLS engine" → **"common false-alarm rate"** (Arm A: SDE≥T; Arm B: Λ≥T_red).
- **Arm-B confirmer (A.11):** folded transit **likelihood-ratio** — D-1a depth-only linear GLS (ν=1) · D-2a GP marginal likelihood (per-star Matérn-3/2) · D-3-i no t₀ refinement; sign + odd/even + secondary EB vetting. **Box depth-SNR rejected.**
- **Period-FAP (A.8/A.8a):** sealed B=1000 block bootstrap; **A.8a admits NO cheap estimator** (E-EVT + E-LUT both failed equivalence). ρ_d≈12.4% retained.
- **T_red = 0.0** (non-binding, FAR-calibrated).
- Stopping rule **P-1…P-9** + pre-committed E1/E2/inconclusive outcome mapping (VAL §7a). **v3 is the FINAL amendment (P-2).**

## 4. Lever-1b equivalence — both candidates FAILED (pre-committed fallback)
| Candidate | (i) p95 ΔFAP≤0.005 | (ii) gate-membership | (iii) recall-safety | Verdict |
|---|---|---|---|---|
| E-EVT (GPD, B′=100) | 0.085 (corr 0.99) | discord 9, 7 FP-admit | 2 clipped | **FAIL** |
| E-LUT (uniform-epoch, nsim 4000) | 0.104 (corr 0.82) | discord 11, 9 FP-admit | 2 clipped | **FAIL** |
Cause: GPD can't fit the discrete low-event-count null tail (EVT); the uniform-epoch grid can't capture per-star red-noise event clustering (LUT). The gate worked as designed.

## 5. M4 dress rehearsal (CALIBRATION, 240 injections, per-cell 8)
- **E1 PASS** (ΔR̄=−0.17 pp, lo95=−0.51 pp). The earlier per-cell-5 "fail" (lo −5.19) was **underpowered noise**.
- **E2 FAIL** (reduction −5.6%, ratio 1.056, ρ_d=0.138).
- **Verdict: FALSIFIED — compute branch (E1 pass, E2 fail).**
- **Recall-loss: 14/240, ALL one pathway** (`cheap_confirm` + `fallback_suppressed`): 11 right-period/wrong-epoch (detector t̂₀ < TLS T₀ precision) + 3 wrong-period; sub-margin (9 gains offset) → a v3-confirmer interaction (T_red=0 no recall floor), not a fundamental failure, does not threaten E1.
- **Honest read:** the genuine, robust limitation is **E2** (un-cheapenable B=1000 FAP entry tax) → H1 compute-branch falsification is the expected, legitimate negative Phase I.

## 6. Decisions made this session (all persisted — see Decision Ledger §11)
1. v3-as-final stopping rule P-1…P-9 + outcome mapping → **ADOPTED** (DR-002 §2.1, VAL §7a).
2. NN#3 condition #1 = YES, transit-template LR required; box-SNR rejected (DR-002 §2.2, MATH §6, VAL A.11).
3. v3 scope = Option-2 confirmer + Lever 1b equivalence-gated; 1a subsumed, 2 deferred to P-8 (DR-002 §2.3).
4. Confirmer spec locked: D-1a / D-2a / D-3-i (TRANSIT_LR_CONFIRMER_SPEC.md).
5. Lever 1b DROPPED (both equivalence candidates failed) → confirmer-only v3 (DR-002 §2.3a fallback; LEVER1B_EQUIVALENCE_RESULT.md).
6. T_red=0.0 set by FAR (TRED_CALIBRATION_RESULT.md).
7. Seal #2b cut (manifest `54f06a94…`, tag `phase1-prereg-v3`).
8. Single TEST read **authorized**; scale **unresolved** (the one open decision).

## 7. Active blockers / open decision
1. **TEST scale (the only thing holding the read):** ~per-cell 50 (VAL §6 realized-CI rule, ~3–5 h) vs literal ≥500/cell (~1.5–2 days). Same expected verdict. **Owner to choose.**
2. After the read: accept the pre-committed verdict (VAL §7a). **No v4 (P-2/P-8).**

## 8. Open questions (raised, not blocking the verdict)
- Is running <500/cell a deviation from VAL §6, or within §6's realized-CI decision rule? (My read: within §6 — the realized-CI clause + pre-planned per-cell increase for INCONCLUSIVE cells.) The owner began to raise this before EOD.
- The T_red=0 recall leak is a real (small) cost of the cheap path; a *future, separately pre-registered* experiment (P-8) could add a recall-protective confirmer floor — NOT a v4 of this experiment.

## 9. Risks
- **R-1 (compute) — materialized:** ρ_d≈12–14% (un-cheapenable B=1000 FAP) → E2 fails. This IS the expected falsification.
- **Single-shot multi-day TEST** at ≥500/cell is fragile; incremental checkpoint added; prefer the tractable §6-CI scale.
- **Branch not merged:** all v3 work is on `phase1/m4-v3-seal2b` (+ tag), not on `main`. PR/merge is an owner action.

## 10. Files requiring review on resume
- **Decision/seal:** `docs/decisions/DR-002_DECISION_RECORD.md` (ADOPTED+SEALED); `data/manifests/m4/v3/m4_v3_threshold_manifest.json` (Seal #2b).
- **Sealed specs (read-only; phase1-prereg-v3):** `docs/TRINETRA_X_PHASE1_VALIDATION.md` v3, `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` v1.2, `docs/SCIENTIFIC_HYPOTHESIS.md` v2.1.
- **Plans/results:** `LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md` + `LEVER1B_EQUIVALENCE_RESULT.md`; `TRED_CALIBRATION_PLAN.md` + `TRED_CALIBRATION_RESULT.md`; `TRANSIT_LR_CONFIRMER_SPEC.md`; `M4_DRESS_REHEARSAL_READINESS.md`.
- **Code:** `research/m4_evaluation/` — `m4_driver.py` (TEST runner), `confirmer.py`, `equivalence_validation.py`, `elut_equivalence.py`, `tred_calibration.py`, `assemble_v3_manifest.py`, `seal_loader.py` (TEST guard).
- **Data:** `data/manifests/m4/{equivalence,tred,v3,dress_rehearsal}/`.

## 11. Uncommitted work (post-seal; outside the frozen tag)
`vault/00_Home/{Current_Mission,Dashboard}.md`, `vault/01_Research_log/Daily_Research_Log.md`, `data/manifests/m4/dress_rehearsal/`, `research/m4_evaluation/{m4_driver.py,M4_DRESS_REHEARSAL_READINESS.md}`, this handoff, `NEXT_SESSION_PROMPT.md`. Commit as a post-seal follow-up (does not affect Seal #2b).

## 12. Recommended startup prompt
See `NEXT_SESSION_PROMPT.md` (reproduced in the EOD status report).

---

*Handoff 2026-06-20 (EOD). M0–M3 + v3 sealed; M4 dress rehearsal complete (E1 pass / E2 fail → FALSIFIED–compute); TEST unread; single read authorized, held only at the scale choice; v3 is the final amendment.*
