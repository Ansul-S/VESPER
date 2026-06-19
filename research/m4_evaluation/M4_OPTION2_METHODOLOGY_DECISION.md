# Methodology Review-Board Decision — Option-2 vs. Original Phase-I Purpose

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Question** | Does the proposed Option-2 amendment remain scientifically consistent with the original purpose of TRINETRA Phase I? (Methodological legitimacy only — E1/E2 performance deliberately ignored.) |
| **Sources reconstructed** | CLAUDE.md; SCIENTIFIC_HYPOTHESIS v2.0; VAL v2 §2/§4/App A; MATH v1.1 §6/§9/§10; TRINETRA-X.md (charter); TRINETRA_CONCEPT_RECONSTRUCTION §C–§E; M1/M2/M3 plans; M4 dry-run + Finding-B + epoch-fixed + combined-arm reports; vault. |
| **VERDICT** | **APPROVE (conditional).** Option-2 is an *amendment* of the same experiment, not a different one — provided three conditions hold. It complies with Non-Negotiable #3; it amends the fairness keystone (an assumption, A6), which must be re-registered transparently. |

## 1. What was Phase I originally trying to prove
That **evidence-first routing** — *detect transit-like events cheaply → infer period from spacing → confirm with physics → run full TLS only where no evidence exists* — **preserves detection recall (non-inferior, δ=2 pp) while cutting compute ≥30% on the fast-path-eligible population** (H1; charter Objective; SCIENTIFIC_HYPOTHESIS §2). It validates a *principle*, not a product (CLAUDE.md). Governing tenets: recall is sacred (Prin. 3 / NN#1); photometry, not timing coincidence, is the judge (Prin. 2 / NN#3); route by evidence, not planet type (Prin. 4). The pre-registered realization fixed the confirmation gate as **narrow-grid TLS, same engine + threshold as the baseline** (the *fairness keystone*, VAL §2, A6), so "the only manipulated variable is whether the detector pre-screens and seeds the search" (H1).

## 2. What Non-Negotiable #3 requires
CLAUDE.md NN#3: *"Physics decides detection. The confirmation gate (transit-model significance), not a coherence score, is the arbiter."* The canonical content (MATH §6): the arbiter is **a likelihood-ratio test on the folded photometry at the seeded period — Λ, equivalently ΔBIC or the transit-fit SNR — requiring significant, shape-consistent, sign-aware folded depth** (i.e. depth + shape + repetition). The v3 failure NN#3 exists to prevent (§E; MATH §10): (i) **timing coherence used as the verdict**; (ii) a **circular statistic** built from quantities the detector threshold forces large (SNR ≳ z⋆√k by construction); (iii) **uncalibrated** score (no null FAP); (iv) **uncorrected look-elsewhere**. NN#3 mandates the *kind* of evidence (calibrated folded photometry) — it does **not**, by itself, mandate the *specific engine* (TLS). "Same engine both arms" is the **fairness keystone (A6)**, a separate assumption whose stated purpose is *equal false-alarm rate* ("equalize thresholds to a common false-alarm rate on the calibration set", A6 check).

## 3. Strongest case that Option-2 remains faithful
- The epoch-fixed confirmer is a **folded-photometry transit significance** (depth via folded depth, shape via transit template, repetition via √N_transits), calibrated against a null (FAR≤1%), with look-elsewhere handled by the period-FAP block bootstrap. This is precisely the §6 arbiter — MATH §6 **explicitly lists "the transit-fit SNR" as an equivalent arbiter form.** It is *not* timing coherence and *not* the v3 circular event-amplitude statistic (empirically corr(n_events, MF)=0.086).
- It therefore **satisfies NN#3 and Principle 2** and repairs, rather than repeats, every v3 error.
- The architecture is otherwise unchanged: cheap detect → period-from-spacing → **physics confirm** → **full-TLS fallback** (recall sacred, NN#1; route by evidence, Prin. 4). The core hypothesis (recall non-inferiority + scoped compute) is intact.
- Crucially, the pre-registered realization is **provably non-executable** (Finding B: narrow-grid SDE is not comparable to the full-grid threshold T; SDE is not invariant to search-grid extent). Insisting on "same TLS engine, same threshold, cheap fast path" is *internally contradictory*. Option-2 is the **nearest faithful realization** that keeps a working physics gate.

## 4. Strongest case that Option-2 violates the original philosophy
- The fairness keystone is not incidental: H1 asserts *"the only manipulated variable is whether the detector pre-screens and seeds the search."* Option-2 manipulates **two** variables — routing **and** the confirmation statistic (TLS-SDE → MF). A recall/compute difference can then no longer be attributed to routing *alone*; it confounds routing with the **intrinsic power gap** between two different statistics.
- Charter Stage 3 names the physics gate as **Mandel–Agol model fitting / Bayesian inference**; a matched-filter SNR is a *lighter* object than a transit *fit*, arguably a reduction in physics rigor.
- "Common FAR" is weaker than "same engine": equal false-alarm rate does **not** imply equal ROC/power. So the experiment shifts from *"does seeding the **same** search preserve recall?"* to *"does seeding a **cheaper, different** confirmer preserve recall?"* — a related but weaker claim.
- There is a real **anti-tuning hazard**: the arbiter is being redefined *after* the pre-registered one was found wanting; without strict discipline this drifts toward "amend until it passes" (review-board F-5).

## 5. Comparison of the three confirmations
| | Full TLS (Arm A baseline) | Targeted TLS (pre-registered fast path) | Fixed-ephemeris LR / MF (Option-2) |
|---|---|---|---|
| NN#3 (physics arbiter) | ✔ transit-model fit | ✔ transit-model fit (same engine) | ✔ §6 folded-transit SNR/Λ (admitted form) |
| Fairness keystone (same engine) | reference | ✔ identical engine + threshold | ✘ different statistic (common-FAR instead) |
| Charter Stage-3 fidelity | highest | highest | lower (matched filter, not a Bayesian fit) |
| Executable / self-consistent | ✔ | ✘ **broken (Finding B)** — narrow-grid SDE ≠ full-grid T | ✔ range-invariant by construction |
| Attribution cleanliness | n/a | cleanest (routing-only) IF it worked | confounds routing with statistic power (mitigated by full-TLS fallback) |
| Role | the benchmark | the *intended* gate, now infeasible | the *nearest faithful* working gate |

The decisive fact: the only confirmation that satisfies **both** NN#3 **and** the same-engine keystone (targeted TLS) is **not realizable**. One must relax something. Full-TLS-everywhere abandons the fast path (no evidence-first). Option-2 keeps the physics gate (NN#3) and the architecture, and relaxes the keystone.

## 6. Preserve / amend / replace
**Amend.** Option-2 **preserves** the core hypothesis (recall non-inferiority + scoped compute), NN#1 (recall sacred), NN#3 (physics arbiter), and the evidence-first architecture; it **amends** assumption A6/the fairness keystone ("same engine both arms" → "common false-alarm rate both arms") and therefore H1's mechanism clause ("seeds the same search" → "seeds a calibrated folded-photometry confirmer"). It does **not replace** the hypothesis.

## 7. If accepted, what Phase I would actually be testing
*"Does evidence-first routing — cheap event detection → period-from-spacing → a **calibrated folded-photometry transit-significance gate at the seeded ephemeris** → full-TLS fallback — achieve recall non-inferior to full TLS at ≥30% lower compute on the fast-path-eligible population, with both arms held to a **common false-alarm rate**?"* The arbiter remains photometric significance (NN#3 intact); the relaxation is keystone-level (equal FAR, not identical engine). The principle under test is unchanged.

## 8. If rejected, what the project currently supports
A **methodological negative result, narrow in scope**: the pre-registered Phase-I realization is **internally inconsistent** — a narrow-grid TLS confirmation cannot share the full-grid SDE threshold, because SDE is not invariant to search-grid extent (Finding B), so the "same TLS engine + same threshold, both arms, cheap fast path" design is **unrealizable**. This **falsifies the specific realization, not the evidence-first principle.** The principle would remain **untested**; the honest conclusion is "the targeted-TLS confirmation as specified is infeasible; a corrected re-registration (or the Phase-II tier) is required" — **not** "evidence-first fails."

## 9. Stronger for v3 amendment, or for a negative-result conclusion? (philosophical)
**Stronger for one disciplined v3 amendment.** Reasoning, independent of E1/E2: (a) Option-2 is methodologically legitimate — a §6-admissible photometric arbiter that repairs all four v3 errors and preserves NN#1/NN#3 and the core hypothesis; (b) the only clean negative result available *now* is narrow (it indicts the TLS *realization*, not the principle); concluding "Phase I negative" from it would **over-claim** — it would report the principle as falsified when only one realization was. Phase I's purpose is to test the *principle*; testing it requires a working arbiter, which the pre-registered one is not and Option-2 is. (A negative-result writeup remains the correct outcome *if* the executed v3 then fails on the sealed TEST — that is the legitimate falsification.)

## 10. Final verdict
**APPROVE — conditional.** Option-2 is a legitimate **amendment of the same experiment**, not a different one, conditional on:
1. **Arbiter integrity (NN#3):** the confirmer is a genuine folded-photometry transit significance (likelihood-ratio / ΔBIC / transit-fit SNR per §6) — sign-aware, shape-consistent, calibrated to a null FAR, look-elsewhere handled by the period-FAP. (The box depth-SNR used in the dry-run is borderline; the faithful form is a transit-template LR. NN#3 stands or falls here.)
2. **Keystone transparency:** the change from "same engine" to "common FAR" is re-registered explicitly, H1's mechanism clause is restated, and the attribution caveat (recall/compute difference now also reflects the statistic gap, mitigated by the full-TLS fallback) is documented.
3. **Anti-tuning discipline (NN#2):** one consolidated re-registration, decided on calibration, justified on first principles, sealed before the single TEST run, with a pre-committed stopping rule (if the executed v3 fails on TEST, that is the falsification — no further amendment).

> **It is the same scientific experiment** — same principle, same physics-arbiter requirement, same recall-sacred routing — **realized through a different, §6-admissible confirmation statistic, because the pre-registered realization was proven internally inconsistent before any TEST data was read.** That is precisely the situation the pre-registration amendment rule was written for.
