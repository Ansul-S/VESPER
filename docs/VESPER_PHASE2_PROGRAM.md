# VESPER Phase II — Re-scoped Program (end-to-end definition)

| Field | Value |
|-------|-------|
| **Status** | **DRAFT v0.1 (2026-07-20) — NOT SEALED. NO DATA READ.** Defines the re-scoped Phase II for owner review. Adoption requires **DR-004** sign-off; execution requires the [`ROADMAP_TO_10`](./ROADMAP_TO_10.md) Phase-II gate (all waves complete). Frozen-parameter tables here are **proposals**; every one is sealed only at the track's own pre-registration. |
| **Author** | Drafted for Ansul Suryawanshi (owner); all seal/freeze decisions are owner sign-offs (CLAUDE.md working agreement). |
| **Supersedes** | `docs/PHASE2_KEPLER_SCALING_PREREG.md` (branch `phase2/kepler-scaling-prereg`, 2026-06-25 sketch). §2.3 records what that sketch got right and the measured conditions under which its question revives. |
| **Inputs** | Sealed Phase-I record (M4 + DR-003 erratum chain) · [`docs/audits/PROJECT_AUDIT_2026-07-19.md`](./audits/PROJECT_AUDIT_2026-07-19.md) · the 2026-07-19 deep scientific review (panel review; to be persisted to `docs/reviews/`) |
| **Prime directive (unchanged)** | Find evidence first. Spend computation second. Let physics decide. Recall > precision. No tuning on test data. Negative results are results. |

---

## 0. Executive summary

Phase I validated the **recall half** of evidence-first routing (E1 robust across three interval constructions) and — pending the DR-003 frozen-rule re-measurement — left the **compute half** somewhere between falsified and inconclusive, with the *structural* analysis (§1.2) showing the survey-scale ceiling is ≈ π·f_p ≈ 0.6% regardless. Phase II therefore **does not scale the routing claim to Kepler**. It re-aims the program at the three assets Phase I actually produced:

- **Track A — Theory:** formalize the *triage impossibility bound* with the sealed Phase-I run as its empirical witness.
- **Track B — Infrastructure:** release the sealed injection-recovery machinery as **VESPER-Bench**, the community's first pre-registered, leakage-safe transit-search benchmark (Kepler DR25 enters here).
- **Track C — Science:** an **event-wise monotransit detection pipeline** — the one regime (K=1) where fold-based search provably cannot operate, where the Phase-I entry-tax economics do not exist, and where the charter's "photometry decides" principle is *structurally forced* (there is no timing coherence to lean on).

One **gating experiment (G0)** runs first: the SES/FFA confrontation, which adjudicates both the strongest external attack on the routing premise and the old sketch's scaling hypothesis, with pre-registered decision rules.

**Phase II reads no Kepler or new TESS data until DR-004 is signed and the relevant track's pre-registration is sealed.**

---

## 1. Why re-scope (the evidence ledger)

### 1.1 What Phase I established
- **E1 (recall):** ΔR̄ = −0.48 pp; one-sided 95% lower bound −0.60 pp (injection bootstrap), **−0.82 pp (40-host cluster bootstrap)**, −0.60 pp (Wilson-weighted) vs a −2 pp margin. Robust, with disclosed structural caveats (fallback carries 78.9% of injections; 30.3% of weight in zero-zero cells; P=0.5 d gains/losses are epoch-predicate phenomena per the 2026-07-19 edge control).
- **E2 (compute):** the sealed 12-star measurement is withdrawn (DR-003; ratio CI [0.42, 1.14]); the frozen-rule re-measurement is Wave-0 work. **The re-scoping does not depend on its outcome** (§1.2).
- Measured cost anatomy: entry tax ρ_d ≈ 0.144; confirmed-cheap fraction f_p ≈ 0.211; corrected break-even prevalence **π\* ≈ 0.68** vs TESS-realistic π̂ ≈ 0.032.

### 1.2 The structural ceiling (why the routing claim is not worth a second mission)
For per-transit SNR₁ and K transits, coherent SNR ≈ SNR₁√K. A per-star router of the Phase-I class serves only signals with **SNR₁ ≥ z**; occurrence is dominated by planets in the stacking-required band z/√K ≤ SNR₁ < z (92.8% of the frozen occurrence weight sits at Rₚ ≤ 2 R⊕, where the sealed run measured both arms near zero recall at Rₚ=1 and fallback-driven parity at Rₚ=2). Even at ρ_d → 0, survey-scale saving ≈ π·f_p·(1−ρ) ≈ **0.6%**. This is a property of the *transit-survey signal population*, not of any implementation. Track A turns this argument into a theorem; no Phase-II measurement can outrun it.

### 1.3 The external threat that must be confronted, not assumed away
The Kepler-TPS decomposition (per-cadence single-event statistics computed once; folding as cheap combination) and the fast-folding algorithm (FFA, O(N log N) over all periods) suggest the "expensive coherent search" premise is an artifact of using TLS as the cost baseline. VESPER's detector already computes ~90% of an SES pipeline. If a cheap coherent search matches TLS recall at ≤0.3× cost, the routed-vs-full dichotomy dissolves — **G0 measures this before any Phase-II commitment.**

### 1.4 What the superseded Kepler sketch got right (and its revival condition)
The 2026-06-25 sketch's mechanism is partially sound: per trial period the fast lane folds k events (k ≪ N), so the **per-eligible-star** ratio should improve with baseline (n_P grows for both arms; TLS cost ∝ n_P·N, fast-lane comb cost ∝ n_P·k, though the bootstrap's B·(N·D) detector term still scales with N). Its flaw is scope: the survey-scale ceiling (§1.2) caps the payoff no matter how well the per-star ratio scales, and the FFA threat (§1.3) attacks its baseline. **Revival condition (pre-registered here):** the scaling question returns as optional **Track D** only if G0 lands in Outcome C (§3, G0-R3) *and* the owner accepts the §1.2 scoped-claim limitation in writing. Otherwise the sketch's branch is closed and archived.

---

## 2. Mission, scope, and non-goals

**Phase-II mission.** Convert Phase I's validated machinery and honest negative into (A) citable theory, (B) community infrastructure, and (C) a detection capability in the regime where the evidence-first architecture is *necessary* rather than merely cheaper.

**Non-goals (hard):** no survey-compute-savings headline; no learned models in any sealed loop (Phase-II may *design* ML extensions; sealed tracks remain untrained, attributable machinery); no product/deployment; no reopening of any Phase-I sealed artifact (P-2 stands: v3 terminal, TEST never re-read).

**Inherited non-negotiables NN#1–7** apply verbatim. **New Phase-II non-negotiables:**
- **NN-P2-8:** each track runs under its **own sealed pre-registration**; no cross-track parameter borrowing after any track touches data.
- **NN-P2-9:** G0's decision rules are sealed **before** G0 executes; the G0 verdict binds the program per §3.
- **NN-P2-10:** any Track-C claim rests on a **binding photometric threshold** (Λ_mono > 0 by construction) — the Phase-I charter inversion (timing gate as realized arbiter, T_red = 0) must not recur.

---

## 3. G0 — the gating experiment (SES/FFA confrontation)

**Question.** Does a cheap coherent search (fold over the detector's own per-duration matched-filter series) reproduce full-TLS recall at a small fraction of its cost?

**Design (calibration-only; cached S1–S3 residuals; no new data; no sealed value touched — same legal basis as the M4 dress rehearsals and the 2026-07-19 edge control).**
1. Implement an SES-fold search: the frozen detector's box depth/SNR series per duration → period scan by fast folding (FFA or FFT-accelerated phase-binning) → max folded statistic per star, threshold calibrated on the cleaned M3 null pool to the same 1%/star FAR that produced T = 10.74.
2. Injection-recovery on the M2-style calibration grid (≥ 8 injections/cell × 30 cells, same hosts/seeds discipline as the dress rehearsal), three arms: full TLS (sealed config) · SES-fold · Phase-I combined arm.
3. Cost metric: single-thread CPU-core-seconds, ≥5 warm repeats, the Wave-3 timing harness (A.7 conventions).

**Pre-registered decision rules (sealed at DR-004 before G0 runs):**
- **G0-R1 (dichotomy dissolved):** SES-fold recall ≥ TLS − 2 pp (occurrence-weighted, calibration CI) **and** cost ≤ 0.30 × TLS → the routing/scaling lane is **closed permanently**; Track A gains the empirical clause "a conforming cheap coherent search exists"; Tracks A–C proceed as planned.
- **G0-R2 (partial):** cost ∈ (0.30, 0.70] × TLS **or** recall gap ∈ (2, 5] pp → dichotomy weakened; record quantitatively in Track A; no Track D.
- **G0-R3 (premise survives):** cost > 0.70 × TLS **or** recall gap > 5 pp → optional Track D (Kepler per-star scaling, §1.4) may be proposed to the owner as a *scoped, secondary* question; Tracks A–C still take priority.

**Effort:** ~1–2 weeks (implementation + ~1 day compute). **Timing:** after Wave 0 completes (the E2 verdict must not share a machine or a mind with new experiments); may run pre-gate as a DR-004 *decision input* with owner sign-off of the rules above.

---

## 4. Track A — Theory: the triage impossibility bound

**Claim to formalize (T-1).** For any two-stage detector over a transit survey in which the cheap stage thresholds a per-event statistic at z (calibrated to per-star false-event rate μ) and failures fall back to the full search, the expected survey compute ratio satisfies

  C_comb/C_full ≥ 1 + ρ_d − π·f_p(z)·(1 − ρ + ρ_d),  with  f_p(z) = P(SNR₁ ≥ z′ ∣ detectable planet), z′ the end-to-end cheap-path acceptance level,

so survey saving ≤ π·f_p(z) − ρ_d, and the break-even prevalence is π\* = ρ_d / (f_p(1−ρ+ρ_d)) (exact form; the sealed run's π\* ≈ 0.68 is its empirical instance). Corollary: with occurrence concentrated below single-event visibility (TESS/Kepler-like populations), no router in this class achieves material survey-scale saving; the binding quantity is the occurrence-weighted upper tail of the SNR₁ distribution.

**Work items.**
- **A-1** Precise statement + proof under explicit assumptions (stationary per-star costs; fallback-complete recall; independence of routing errors from cost); document every assumption's realism.
- **A-2** Population curves: f_p(z) and the saving bound vs z for TESS (measured M1 noise + KM occurrence), Kepler DR25 (published noise/occurrence — **literature values only; no data read**), and PLATO (design specs). Uncertainty bands from occurrence-model error.
- **A-3** Place the sealed Phase-I measurement (and the DR-003 re-measurement) on the curve as the witness point; reconcile with the E2 verdict whatever it is.
- **A-4** The G0 clause: if G0-R1, add the stronger statement (the two-stage question is moot because C_full itself collapses).
- **A-5** Scope boundary theorem-side: the bound's failure modes — K=1 (no fold exists: Track C's charter) and non-compute resources (vetting/followup allocation, where the same algebra prices *attention*, not CPU) — stated as the two open lanes.

**Endpoints / done:** theorem + proof reviewed by ≥1 external mathematician/statistician; curves reproducible from a tracked notebook; integrated as a section of the Phase-I paper (or companion note). **No seal needed** (theory reads no protected data). **Effort:** 3–4 weeks, parallel with Wave 5.

---

## 5. Track B — Infrastructure: VESPER-Bench

**Product.** The sealed benchmarking machinery, packaged for third parties: frozen manifest + leakage-safe split; conditioning spec; injection physics; occurrence weights with the **KM-period-weighted variant** included (audit §3.5); sealed-threshold protocol; single-shot evaluation harness with digest-verified configs; metrics (occurrence-weighted recall + CIs incl. host-cluster bootstrap; cost ledger conventions).

**Milestones.**
- **B-1** Extract the harness onto the Wave-3 `vesper_core` + seal-tooling library (dependency: Roadmap ARCH-1/2, INN-2).
- **B-2** TESS benchmark v1: S1–S3 manifest (Seal #1 basis), documented tasks ("closed" = sealed-test protocol; "open" = calibration playground), reference baselines (TLS sealed config; G0's SES-fold; Phase-I combined arm) with published score cards.
- **B-3** **Kepler DR25 extension:** new leakage-safe manifest (quarter-coverage-stratified split; EB/variable cleaning per the M3 recipe; **data version pinned to DR25 file digests** — the audit's reproducibility-rot lesson). This is Phase II's only Kepler data read, and it is *benchmark construction*, not hypothesis testing — sealed as **P2-Seal-B1** before any leaderboard use.
- **B-4** External-user acceptance test: one outside user reproduces the reference card from the public artifacts within stated tolerance, on a clean machine, without author help.
- **B-5** Release: DOI, versioned data cards, contribution policy (new baselines run under the sealed protocol or are labeled "open division").

**Endpoints / done:** B-4 passes; ≥1 non-VESPER pipeline scored on it. **Kill criterion:** if B-4 cannot pass after two iterations, descope to "reproducibility package for the Phase-I paper" and record why. **Effort:** 4–6 weeks (+ bounded cloud compute for Kepler conditioning; the only non-local item in Phase II).

---

## 6. Track C — Science: event-wise monotransit detection (the flagship)

### 6.1 Why this is the right home for evidence-first
For K=1: (i) folding cannot increase SNR — the full search's *only* advantage is void; (ii) there is no timing coherence — the arbiter **must** be photometric shape/significance, structurally realizing NN#3 and repairing the Phase-I inversion; (iii) the entry-tax economics that killed E2 do not apply (there is no expensive alternative being routed around — the cheap path is the *only* path); (iv) the science need is real and growing: single-sector TESS baselines (~27 d) make every P ≳ 27 d planet a monotransit, and long-period detection is where PLATO-era demographics point.

### 6.2 Formal hypotheses
- **H-C1 (detection):** the event-wise pipeline (detector at z_mono → physics LR confirmer with binding Λ_mono → vetoes) achieves monotransit recall ≥ **R_min** on the SNR₁-visible injected population at a calibrated false-alarm rate ≤ **α_mono** per star. (R_min, α_mono sealed at P2C-prereg; drafting anchors: R_min = 0.70 on the z_mono-visible class; α_mono = 1%/star, matching Phase-I FAR discipline.)
- **H-C2 (characterization):** the duration–density period posterior, P ≈ π²Gρ⋆T₁₄³ / [3(1−b²)^{3/2}] marginalized over b (and e where priors exist), achieves nominal frequentist coverage: 68/95% credible intervals contain P_true within ±5 pp coverage error on the sealed test.
- **H-C3 (purity):** ≥ **V_min** of injected eclipsing-binary/systematic contaminants are rejected by the physics gates (odd/even is unavailable at K=1 → the veto set is: sign, shape-template consistency, secondary search at the posterior-implied phases, duration-density consistency itself). Drafting anchor V_min = 0.75, to be set from calibration achievable-region — **never** from test.
- **H0:** any of H-C1..C3 fails its sealed margin → reported as a falsification of the event-wise monotransit realization, with the same finality discipline as Phase I.

### 6.3 The free pre-study (no new data; runs pre-gate)
The sealed grid accidentally contains **892 effective monotransits** (≤1 observed transit; 852 at P=16 d — erratum §4). Re-analysis of the already-recorded `recovery.csv` rows (no light-curve access, hence no new TEST read under the DR-003 boundary) yields: both arms' behavior at K_obs ≤ 1, the fast path's seed quality on single events, and empirical anchors for the §6.2 margins. Deliverable: a short memo that feeds the P2C-prereg numbers. **This is the first Phase-II science act and it is free.**

### 6.4 Milestone ladder (mirrors Phase I discipline)
| Milestone | Content | Data touched | Seal |
|---|---|---|---|
| **P2C-M0** | Manifest: multi-sector S1–S3 overlap targets (baselines 27–82 d) for K=1-regime injections (P > baseline ⇒ K=1 by construction); leakage-safe split reusing the M0 sky-region rule; η-style feasibility | Catalog metadata only | **P2-Seal-C1** (manifest digest) |
| **P2C-M1** | Conditioning via the frozen Stage-0 (2.5 d biweight; per-star noise incl. per-star τ — the audit fix is standard here) | Calibration LCs | — |
| **P2C-M2** | Injection design: P ∈ {1.5×, 3×, 6×, 12×} baseline · Rₚ ∈ {4, 8, 12} R⊕ (+ Rₚ=2 exploratory row, expected noise-limited — pre-labeled as in Phase-I M2) · b ∈ {0, 0.3, 0.6}; **raw-then-recondition mode mandatory** (the η lesson: no residual-space shortcut in a sealed run) | Calibration | — |
| **P2C-M3** | Calibration: z_mono revalidated (sealed 5.3 as prior); **Λ_mono threshold calibrated to α_mono with T_red > 0 binding (NN-P2-10)**; veto suite ROC on the cleaned null pool + injected EB models; duration-density posterior coverage on calibration | Calibration | **P2-Seal-C2** (thresholds) |
| **P2C-M4** | Dress rehearsal on calibration; instrumented loss taxonomy; owner review | Calibration | — |
| **P2C-M5** | **Single sealed TEST read** (pre-committed verdict mapping; token-gated; one read, final) | TEST (once) | verdict |
| **P2C-M6** | Reality check: known long-period/monotransit TESS objects (community-confirmed single-transit candidates); Kepler cross-check *via Track B's sealed benchmark only* | Public confirmed objects | — |
| **P2C-M7** | Write-up + release | — | — |

### 6.5 Draft frozen-parameter table (to seal at P2C-M0/M3; every value owner-signed)
| Parameter | Draft value | Source / rationale |
|---|---|---|
| z_mono | 5.3 (revalidate) | Phase-I Seal #2 (0.1 false events/LC target) |
| α_mono | 1%/star | FAR discipline continuity |
| Λ_mono (T_red analogue) | **> 0, calibrated** | NN-P2-10; χ²₁-anchored, empirically calibrated with the estimated-K correction (audit MATH-4) |
| R_min / V_min | 0.70 / 0.75 (anchor) | To be set from §6.3 pre-study + M3 achievable region, before TEST |
| Injection mode | raw + recondition | η paid honestly (erratum §2.3 lesson) |
| Recovery predicate | epoch within ±0.5 T₁₄ **+ pre-registered tolerance sensitivity at ±0.75/1.0** | Edge-control lesson: never again a single-tolerance estimand |
| Period-posterior spec | ρ⋆ from TIC+spectroscopy where available; b marginalized uniform·transit-probability prior; e fixed 0 with disclosed bias note | Standard single-transit estimator |
| n_transits accounting | **Data-driven observed-epoch count** (not ⌊baseline/P⌋+1) | Erratum §4 lesson |

### 6.6 Baseline for comparison
No fold-based method exists at K=1, so the baseline is the **uncalibrated single-event matched filter** (= the detector alone at z_mono, no physics gates): H-C1/H-C3 measure what the calibrated-FAP + physics-confirmation stack *adds* — FP purity at matched recall — which is precisely the evidence-first value proposition in its native regime.

**Effort:** 10–14 weeks part-time (M3's null calibration is the compute pole; all local-feasible — no fold means cheap everywhere).

---

## 7. Data policy (program-wide)
- **Phase-I TEST:** never re-read (P-5/P-2 eternal). Re-analysis of already-recorded outputs (`recovery.csv` etc.) is legal per the DR-003 boundary; any new light-curve access to those hosts is not.
- **Track C TEST split:** defined at P2C-M0, read exactly once at P2C-M5, then closed forever — the Phase-I single-shot discipline verbatim.
- **Kepler DR25:** touched only inside Track B, only after P2-Seal-B1, with data-file digests pinned in the manifest.
- **Calibration data:** the open playground, as in Phase I; every sealed number derives from calibration + theory only.

## 8. Governance
- **Adoption:** this document v1.0 + G0 rules signed as **DR-004** after the ROADMAP_TO_10 gate (Waves 0–6). Pre-gate exceptions (explicit): §6.3 pre-study and G0, both calibration/recorded-data only, each with owner sign-off first.
- **Amendment policy:** per track, one terminal amendment analogous to Phase-I P-2 (a v2 of a track prereg is final; a failed track is reported, not retried).
- **Stopping rules:** Track A stops at external review + integration; B at B-4 or its kill criterion; C at the pre-committed P2C-M5 verdict either way.
- **Sign-off gates:** every seal, threshold, and margin above is a presented-for-approval item; nothing freezes without the owner's recorded sign-off. All Wave-3 integrity tooling (digest-verified configs, module-identity assertions, frozen-code-as-data) is mandatory infrastructure for every sealed run.

## 9. Timeline & compute (part-time solo, after the Phase-I roadmap completes)
| Item | Duration | Compute |
|---|---|---|
| §6.3 pre-study + G0 | 2–3 wk | ~1 day local |
| Track A | 3–4 wk (parallel) | negligible |
| Track B | 4–6 wk | bounded cloud (Kepler conditioning only) |
| Track C | 10–14 wk | local (M3 null calibration is the pole) |
| **Phase II total** | **≈ 4–6 months** | mostly local |

## 10. Risks & kill criteria
| Risk | Track | Mitigation / kill |
|---|---|---|
| G0 lands R1 and the community reads it as "VESPER refuted itself" | A | That *is* the Track-A story told properly: the bound + the witness; write it first |
| Bound proof assumptions attacked | A | A-1 documents realism per assumption; external review before publication |
| Benchmark unused | B | B-4 acceptance + one external pipeline scored pre-release; else descope honestly |
| Monotransit FP rate uncontrollable at useful recall (the real scientific risk) | C | That outcome is H0 — a publishable falsification under the same discipline; margins set from calibration so the test is fair |
| ρ⋆ errors poison the period posterior | C | Coverage endpoint (H-C2) measures it; spectroscopic-subsample cross-check at M6 |
| Scope creep back toward routing/product | all | NN-P2 set + §2 non-goals; Track D exists only behind G0-R3 + owner writing |

## 11. Deliverables
1. Phase-I paper strengthened with the Track-A bound section (+ companion theory note if the venue splits it).
2. **VESPER-Bench v1** (TESS) + v1.1 (Kepler DR25), DOI'd, with reference score cards.
3. Track-C monotransit paper — detection *or* falsification, sealed either way.
4. DR-004 (adoption) and per-track seal records; §6.3 pre-study memo; G0 report.

## 12. Relationship to ROADMAP_TO_10
Waves 0–5 unchanged. **Wave 6 content is rewritten by this document upon DR-004:** INN-3 (cheap equivalent FAP) is **demoted** (revivable only under G0-R3); INN-4 (epoch-refit confirmer) migrates into Track C's M2/M3 design space; the Phase-II gate checklist's "Phase-II prereg drafted" items now point here. The roadmap edit itself is performed only after DR-004 is signed (no silent rewrites of an adopted plan).

## 13. Open questions for the owner (decision points, not blockers to review)
1. Confirm Track D's status: closed-unless-G0-R3 (recommended) vs. keep as a standing secondary.
2. Publication packaging: bound inside the Phase-I paper (recommended) vs. separate methods note.
3. Track order after G0: C-before-B (science first; recommended — B depends on Wave-3 engineering anyway) vs. B-first.
4. Kepler scope in B-3: full FGK DR25 manifest vs. a curated ~5k-star subset (recommended start).
5. External reviewers to invite for A-1 and B-4.

---

*Draft v0.1, 2026-07-20. Nothing here is sealed; nothing here reads data; every number marked "anchor/draft" is a proposal awaiting owner sign-off at its own gate. The discipline that made Phase I credible — freeze before you look, one look, report either way — is inherited whole.*
