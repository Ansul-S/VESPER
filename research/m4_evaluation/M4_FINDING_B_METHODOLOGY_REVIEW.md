# M4 Finding-B Methodology Review — Arm-B Confirmation Statistic

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Status** | **Decision-support for owner.** No re-registration drafted, no seal changed, TEST unread. |
| **Scope** | CALIBRATION-only diagnostics (16 hosts: 10 injected, 6 null) + analysis. No TEST access. |
| **Question (owner)** | Is Finding B best fixed by a **minimal amendment** (Option 1) or does the **targeted-arm statistic need redefinition**? |
| **Answer** | **Redefinition.** Options 1 and 3 are empirically non-viable; the period-fixed statistic (Option 2 family) is the only candidate that preserves recall at low compute — but it is a substantive re-registration, not a minimal edit. |

> **Finding B restated.** TLS **SDE is normalized across the searched period grid**, so it is not comparable across grid widths. The sealed Arm-B rule — *targeted TLS on `[P̂(1±ε)]`, **SDE ≥ T**, single common T both arms* (VAL §2/§4.1, A.1/A.4) — is internally inconsistent: a narrow-grid SDE is on a different scale than the full-grid SDE that calibrated T=10.74. As written, Arm B rejects planets Arm A accepts → E1 fails by construction.

## 1. Evidence (CALIBRATION-only; 16 hosts)

Per-statistic separation between injected planets and null residuals, and cost vs full TLS. "recall @ null-FAR" = fraction of the planets **Arm A actually recovers** (SDE_full ≥ T_A) that also clear a threshold set at the null distribution's max (a stand-in for FAR≤1% in this small sample). AUC = rank probability a planet scores above a null.

| Statistic | AUC (planet/null) | recall @ null-FAR | cost / full | Verdict |
|-----------|-------------------|-------------------|-------------|---------|
| **SDE_full** (Arm A, T_A=10.74) | **0.92** | **1.00** | 1.000 | reference |
| Narrow SDE, ε=0.01 (**Option 1**) | **0.43** | 0.00 | 0.028 | **no discrimination** |
| Narrow SDE, ε=0.05 | 0.48 | 0.00 | 0.060 | non-viable |
| Narrow SDE, ε=0.10 (**Option 3**) | 0.55 | 0.17 | 0.097 | poor |
| Narrow SDE, ε=0.20 (**Option 3**) | 0.72 | 0.67 | 0.158 | insufficient + saving eroding |
| **depth-SNR**, period-fixed (**Option 2**) | **0.85** | 0.67 | 0.0003 | best cheap option; tail to fix |

Source: `data/manifests/m4/dry_run/finding_b_diagnostic.csv`. Even **Arm-A-recovered** planets get narrow-grid SDE of ~2 (ε=.01) to ~7 (ε=.2) — all below T_A=10.74 — confirming the scale shift is fatal, not marginal.

## 2. Option-by-option assessment

### Option 1 — Per-arm threshold T_B at common FAR (the "minimal amendment")
- **E1 impact:** **Fails.** Narrow-grid SDE (ε=0.01) has AUC 0.43 (≈ chance) — planet and null medians coincide (1.86 vs 1.75). **No T_B exists** that separates planets from nulls; recall at any sane FAR ≈ 0. Recall non-inferiority is unachievable.
- **E2 impact:** Best (cost 0.028× → ~97% saving) — but irrelevant given E1 fails.
- **Appendix-A changes:** Small textual: A.4 "single common T" → per-arm {T_A, T_B}; add T_B to A.2.
- **Calibration workload:** Would need the targeted-SDE null distribution from routed null stars — sparse (few nulls route), likely needs the full 6885 null pool. Moot.
- **Interpretability:** Weak — SDE on ~14–25 periods is not a meaningful detection statistic (TLS SDE assumes a broad grid).
- **Anti-tuning risk:** Low in principle (calibrate on CALIBRATION, seal before TEST), but moot — the statistic doesn't work.
- **Verdict: rejected on evidence.**

### Option 3 — Wider targeted window, single common T_A
- **E1 impact:** AUC rises with ε (0.43→0.48→0.55→0.72) but never approaches full's 0.92 until ε approaches the full grid. At ε=0.2, recall of Arm-A-recovered planets is only 0.67 → E1 (−2 pp margin) would fail.
- **E2 impact:** Saving collapses as ε grows: ε=0.1 → 90% saving (AUC 0.55), ε=0.2 → 84% (AUC 0.72). To reach SDE comparability you need ≈ full grid → **no saving**. Comparability and compute saving are mutually exclusive here.
- **Appendix-A changes:** Smallest numerically (only ε), but ε was sealed at 0.01 *matched to the A.4 1% recovery tolerance*; widening to ~0.3–0.5 decouples confirm-window from recovery-tolerance — a semantic change.
- **Calibration workload:** Moderate (sweep ε on injected+null, re-verify T_A FAR).
- **Interpretability:** Clean story IF a workable width existed; it does not.
- **Anti-tuning risk:** Low (one re-derived ε), but moot.
- **Verdict: rejected — cannot satisfy E1 and E2 simultaneously.**

### Option 2 — Period-fixed detection statistic (depth-SNR / likelihood-ratio)
- **E1 impact:** **Most promising.** depth-SNR at the seeded P̂ has AUC 0.85 (vs full 0.92) — and it is **range-invariant by construction** (no grid normalization to collapse). The remaining gap is a null **false-alarm tail** (one null scored 21.7) from my crude statistic searching *all phases × durations*. Evidence-first supplies **both P̂ and t̂₀** from the detector events; fixing the **epoch** (and using a proper transit matched-filter / likelihood-ratio rather than a free-phase box) should suppress that tail and lift AUC toward full. **Needs one confirming diagnostic.**
- **E2 impact:** **Best by far** — period-fixed evaluation is ~free (cost 0.0003×); the fast path becomes detector → P̂,t̂₀ → single-point confirmation. E2 ≫ 30% saving, with ρ_d (detector + period-FAP) now the dominant Arm-B cost (so R-1 is correctly the live risk).
- **Appendix-A changes:** **Largest.** Redefines A.1 (Arm B no longer runs TLS) and A.4 (arbiter = period-fixed statistic ≥ T_dsnr, calibrated to FAR≤1%/star on CALIBRATION). The "same TLS engine both arms" fairness keystone is replaced by a **"same false-alarm rate both arms"** keystone — arguably the more honest statement of evidence-first (and consistent with VAL §2's own phrase "same SDE threshold T, *set to a common false-alarm rate*").
- **Calibration workload:** **Light compute** (depth-SNR is ~free → can calibrate T_dsnr on the full 6885 null pool easily), but **conceptual/spec work is heavy** (define the exact statistic + template + epoch handling, then re-register).
- **Interpretability:** High as a detection statistic; reframes the headline comparison as "full TLS search vs detector-seeded confirmation at equal FAR" — defensible and arguably stronger, but reviewers must accept it is no longer a same-engine comparison.
- **Anti-tuning risk:** **Moderate** — a new statistic + threshold chosen *after* observing the dry-run blocker is real researcher-degrees-of-freedom. Mitigations: (a) decide and calibrate on CALIBRATION only; (b) re-register with explicit rationale that the change was forced by a **pre-TEST implementation discovery** (a legitimate amendment under the pre-reg rules), re-dated as a new version; (c) freeze the statistic/template/threshold and seal **before** the single TEST run; (d) one TEST evaluation only.
- **Verdict: recommended direction**, pending one confirming diagnostic (epoch-fixed statistic) before re-registration.

## 3. Cross-cutting

- **All three require a re-registration + re-seal (Seal #2b) before TEST.** None touches TEST. The dry-run diagnostics inform the choice; they are not the seal.
- **The recall headline was always modest** (Arm A recovers the strong Rₚ=4 cells and one Rₚ=2; Rₚ≤2 mostly noise-limited) — consistent with the Seal #2 expected-evaluation note. E1 is about Arm B *matching* Arm A, not absolute recall.
- **Anti-tuning meta-point:** we are selecting methodology after a dry-run failure. This is legitimate *only* because (i) it is pre-TEST, (ii) it is decided on CALIBRATION, (iii) it is re-registered and sealed before the one TEST run. This must be stated plainly in the re-registration.

## 4. Recommendation
1. **Reject Options 1 and 3** (evidence above).
2. **Adopt the Option 2 direction**, but first run **one more CALIBRATION-only diagnostic**: a period-**and-epoch**-fixed transit matched-filter / likelihood-ratio statistic, to confirm it removes the null false-alarm tail and reaches full-grid-comparable AUC. (Compute is ~free, so this can use a large null sample.)
3. If confirmed, **draft a re-registration** (new pre-reg version + decision record): redefine A.1/A.4 Arm-B arbiter, add the calibrated threshold T_dsnr (FAR≤1%/star on CALIBRATION), restate the fairness keystone as common-FAR, carry forward all other Seal #2 values unchanged → **Seal #2b**. Then resume M4 (single TEST run) against the amended protocol.

**Decision requested:** approve step 2 (the epoch-fixed confirming diagnostic on CALIBRATION) and, in principle, the Option-2 re-registration direction — or redirect.
