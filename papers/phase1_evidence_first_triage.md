# The Limits of Evidence-First Transit Detection: A Pre-Registered Test on TESS

**DRAFT v0.1 — 2026-06-25.** Phase-I validation/methods paper. Grounded in the sealed M4 result (`research/m4_evaluation/M4_TEST_RESULT.md`); numbers are from the single TEST read (`data/manifests/m4/test_run/`). Citations are name-year placeholders keyed to `docs/PAPER_NOTES.md` §11 / `docs/references.bib`. Author line per charter (Vesper); ISRO exoplanet-challenge context acknowledged.

---

## Abstract

Transit surveys fold every light curve at thousands of trial periods — an exhaustive search whose cost scales poorly to the $\sim10^5$–$10^6$ stars of missions like TESS. We test, in a pre-registered single-evaluation experiment, whether detection cost can be reduced by **routing on evidence**: detecting individual transit-like events directly, inferring the period from their spacing, confirming with a calibrated folded-photometry transit likelihood-ratio held to a common false-alarm rate with the baseline, and reserving a full Transit Least Squares (TLS) search only for stars the cheap gate rejects. Using injection–recovery into real TESS light curves (preserving genuine correlated noise) on a sealed test set of 15,000 trials, we find that evidence-first routing **preserves recall** non-inferiorly to full TLS (occurrence-weighted recall difference $-0.48$ percentage points; one-sided 95% lower bound $-0.60$ pp; pre-registered margin $-2$ pp). **However, the compute saving over the fast-path-eligible population (24.4%) falls short of our pre-registered 30% threshold, falsifying the compute branch of the hypothesis.** We localize the shortfall to a single replaceable component — the per-star bootstrap period false-alarm-probability (FAP) entry tax ($\rho_d\approx14\%$), charged on every routed star — which a numerical-equivalence gate proved cannot be cheapened without altering which stars pass. Recall losses concentrate on large, low-occurrence planets and arise from one mechanism (the cheap confirmer suppressing the full-search fallback on a right-period/wrong-epoch seed); they are partly offset by gains on short-period planets the periodogram misses. We release the sealed benchmark and identify the cheaper-but-equivalent period-FAP as the decisive lever for future work.

---

## 1. Introduction

Box-fitting (BLS; Kovács et al. 2002) and Transit Least Squares (TLS; Hippke & Heller 2019) period searches evaluate a dense grid of trial periods for every star. This exhaustive design is the workhorse of transit detection, but its cost grows with both the target count and the period-grid density, which scales unfavourably for all-sky, high-cadence missions.

An alternative is to **spend computation where the evidence is**. If a light curve contains one or more individually detectable transit-like events, their *spacing* constrains the period directly, and a single folded-photometry significance test at the implied ephemeris can confirm or reject a candidate without a full grid search. Only stars lacking such local evidence need the exhaustive search. The central question of this paper is whether such routing can cut compute **without dropping planets a full search would have found** — recall being the property a detection pipeline cannot sacrifice.

We frame this as a **non-inferiority test**, importing the logic of clinical trials: recall is the *protected* endpoint (the new procedure must be no worse than the baseline within a pre-specified margin), and compute is the *superiority* endpoint (the new procedure must be meaningfully cheaper). Both criteria, the thresholds, the injection grid, and the analysis were **pre-registered and cryptographically sealed before any test data were read**, and the test set was read exactly once. This design directly addresses the credibility problem that dogs "we saved X% compute" claims: here the result is falsifiable and was not tuned.

This is a deliberately **untrained** Phase-I test: the event detector is a simple matched-filter, not a learned model, so a pass or fail is attributable to the *routing principle* rather than to a model's capacity. We report a negative result on the compute claim with the same rigor we would a positive one.

## 2. Methods

### 2.1 Data and frozen manifest (M0)
We use TESS 2-minute SPOC light curves from sectors S1–S3 (southern ecliptic). A frozen manifest of 22,723 targets was split leakage-safe by sky region into a calibration set (6,925) and a test set (15,798); the split and target list were hash-sealed (Seal #1) before any conditioning. All thresholds are calibrated on the calibration set only; the test set is sealed until the single evaluation.

### 2.2 Stage-0 conditioning
Each light curve is detrended per sector with a time-windowed biweight slider (wotan; Hippke et al. 2019) at a window of 2.5 d — finalized on the calibration set by a transit-preservation criterion ($\eta\ge0.90$) — with SPOC quality masking and momentum-dump handling, yielding a zero-centred residual $r(t)$. A per-star noise model ($\sigma$, CDPP, $\tau_{\rm GP}$) is recorded. No detection threshold is set at this stage.

### 2.3 Injection–recovery design
Synthetic transits are injected into **real** conditioned residuals (preserving the true correlated-noise covariance) on a grid of period $P\in\{0.5,1,2,4,8,16\}$ d and radius $R_p\in\{1,2,4,8,12\}\,R_\oplus$ (30 cells), with impact parameter varied per injection. The sealed test campaign uses **500 injections per cell** (15,000 total — the pre-registered floor), drawn over 80 test-set host stars. Recovery is defined operationally (period within tolerance and epoch within $\pm0.5\,T_{14}$), identically for both arms.

### 2.4 The two arms (the fairness keystone)
- **Arm A (baseline):** a full-grid TLS search; a star is recovered if its signal-detection efficiency $\mathrm{SDE}\ge T$.
- **Arm B (combined / evidence-first):** the matched-filter detector extracts events; if $\ge N_{\min}$ events are found the star is *routed* and a period is inferred from event spacing; a block-bootstrap **period-FAP** gates entry; stars passing the gate go to a **folded-photometry transit likelihood-ratio (LR) confirmer** at the seeded ephemeris, and stars that fail the gate or the confirmer fall back to the **identical full TLS** as Arm A.

The fairness keystone is that both arms are held to a **common false-alarm rate**, not the same engine — a relaxation adopted in the sealed v3 amendment (below). The full-TLS fallback guarantees that a routed planet is lost only if the seed is wrong *and* the fallback is suppressed.

### 2.5 Thresholds and the v3 amendment
Thresholds were calibrated on the cleaned calibration null pool and sealed (Seal #2): event threshold $z_\star=3.4$, monotransit $z_{\rm mono}=5.3$, $N_{\min}=2$, TLS threshold $T=10.74$, period-FAP level $\alpha_{\rm FAP}=0.01$, targeted-window $\varepsilon=0.01$, an occurrence weight $w_c$ (Kunimoto & Matthews 2020 radius prior; 92.8% weight on $R_p\le2\,R_\oplus$), and a mean occurrence $\hat\pi=3.17\%$.

A pre-test methodological defect (Finding B: TLS SDE is normalized across the searched grid, so a narrow-grid SDE is not comparable to the full-grid threshold $T$) made the original "targeted-TLS" confirmation non-executable. This forced a final, pre-registered amendment (v3): the fairness keystone was relaxed from "same engine" to "common false-alarm rate," and Arm-B confirmation became the folded transit-LR ($\Lambda$, sign-aware and shape-consistent, with a physical transit template) at confirmer threshold $T_{\rm red}$ (set to the same null FAR; calibration yielded the non-binding $T_{\rm red}=0$). A separately-proposed cheapening of the period-FAP (replacing the $B{=}1000$ block bootstrap with a cheaper estimator) was admitted only under a numerical-equivalence gate, which **both** candidate estimators failed; the sealed bootstrap therefore stands. The amendment is documented in DR-002 and was sealed (Seal #2b, tag `phase1-prereg-v3`) before the test read. **No numeric threshold was changed by v3.**

### 2.6 Endpoints, pre-registration, and anti-tuning
- **E1 (recall non-inferiority):** the occurrence-weighted recall difference $\overline{\Delta R}=R_{\rm comb}-R_{\rm TLS}$; PASS if its one-sided 95% lower bound (bootstrap, $B=2000$) exceeds the $-2$ pp margin.
- **E2 (scoped compute):** the compute reduction over the fast-path-eligible population; PASS if $\ge30\%$ at non-inferior recall. (A survey-representative figure, E3, is expected near-zero by construction and is a secondary endpoint.)

The outcome mapping (E1/E2/inconclusive → conclusions) was pre-committed before the read; a stopping rule (P-1…P-9) declared v3 the terminal amendment and prohibits any post-hoc change. Integrity was verified in-run (both seals hash-checked, fail-closed) and after (`git diff` against the sealed tag empty; test accessed exactly once).

## 3. Results

The single sealed-test evaluation (15,000 injections; read once) returns the headline of Table T2.

### 3.1 E1 — recall is preserved (PASS)
The occurrence-weighted recall difference is $\overline{\Delta R}=-0.48$ pp with a one-sided 95% lower bound of $-0.60$ pp, comfortably inside the $-2$ pp margin: **routing does not sacrifice recall.** On the occurrence-weighted scale (Table T2) recall is 0.218 (full) vs 0.213 (combined); on the unweighted injected grid it is 0.509 vs 0.488. The weighted figures are low in absolute terms because the Kunimoto & Matthews (2020) weight concentrates on small ($R_p\le2$) planets, which are intrinsically hard; E1 concerns the *difference*, which is non-inferior.

The completeness maps (Figure F3) and Table T3 localize the structure. At $R_p=2\,R_\oplus$ — the weight-dominant class — the arms are at near-parity ($-0.37$ pp). The largest per-cell losses are at intermediate periods and larger radii ($R_p=4$: $-5.1$ pp; $R_p=8/12$: $-2.1/-2.7$ pp), which carry little occurrence weight. At $R_p=1$ both arms recover essentially nothing (noise-limited single transits). Notably, at the shortest period ($P=0.5$ d) the combined arm **outperforms** full TLS by $+19$ pp (Table T3, by period; the blue column in F3): the confirmer recovers short-period planets whose full-grid SDE fell just below $T$.

### 3.2 Recall-loss mechanism (one pathway)
Against full TLS the outcomes are: both recover 6,761; neither 6,807; **combined-only (gain) 563; TLS-only (loss) 869.** All 869 losses share a single pathway: the cheap confirmer confirmed at the seeded ephemeris and therefore **suppressed the full-TLS fallback**, but the seed then failed the recovery predicate. Of these, 80% are *right-period/wrong-epoch* — the detector's event epoch is less precise than TLS's fitted $T_0$ — and 20% are wrong-period. They concentrate on large, low-occurrence planets (so the weighted $\overline{\Delta R}$ stays small). The 563 gains, almost all at $P=0.5$ d, partly offset them. This mechanism was anticipated by the calibration dress rehearsal and is a confirmer/fallback interaction (the non-binding $T_{\rm red}=0$ provides no recall floor), not a failure of period recovery.

### 3.3 E2 — compute saving falls short (FAIL)
On the fast-path-eligible timing subset the combined arm costs 0.756× the full search — a **24.4% reduction**, short of the pre-registered 30% (Table T7; Figure F8). The bottleneck is the routing **entry tax** $\rho_d\approx14.4\%$: the detector plus the $B=1000$ block-bootstrap period-FAP are charged on every routed star, including the ~61% that fail the FAP gate and fall back to the full search (routing funnel: 75.2% routed → 38.7% of routed pass the gate → 72.5% of those confirmed). F8 makes this concrete: confirmed-cheap stars save dramatically (~80 s → ~10 s), but fallback stars pay the entry tax *on top of* the full search, so the per-star saving is diluted. The break-even occurrence is $\pi^\star\approx0.236$.

### 3.4 Verdict
By the pre-committed mapping (VAL §7a): **E1 PASS, E2 FAIL → H1 FALSIFIED on the compute branch.** A successful, well-characterized negative result.

### 3.5 Parameter recovery and calibration
Among the 11,036 routed injections with a period seed (Table T5; Figure F5), the inferred period matches truth within tolerance for 45.9%, with a tight median fractional error of 0.0022 for matched cases; 27.1% of matches fall on a 2×/½/3× harmonic of the fundamental rather than the fundamental itself. The seeded epoch lies within the recovery window ($\le0.5\,T_{14}$) for 54.2%, with a median offset of $0.40\,T_{14}$ — the detector-epoch imprecision (relative to TLS's fitted $T_0$) that drives the right-period/wrong-epoch loss pathway of §3.2. The period-FAP is well-calibrated: on the cleaned null pool the empirical false-alarm rate at the sealed $\alpha=0.01$ is **1.08%** (Figure F6, Table T4), reproducing the sealed M3 calibration. F6 also quantifies the value of the null-pool cleaning — before removing EB/variable contaminants (which carry real periodic signals) the raw FAR is inflated to 2.07%. *(Depth/$T_{14}$ recovery were not logged per-injection and are deferred.)*

## 4. Discussion

**What holds.** The recall-safety of evidence-first routing — its hardest and most important claim — is *supported* on a sealed test set: a cheap detector plus a calibrated transit-LR confirmer plus a full-search fallback recovers planets non-inferiorly to exhaustive TLS at a common false-alarm rate. The architecture does what it was designed to do for recall.

**What fails, and why it is informative.** The compute claim is falsified in this realization, and the failure is *localized to one replaceable component*: the bootstrap period-FAP entry tax. We did not merely observe a shortfall — we proved (via the equivalence gate) that this particular estimator cannot be cheapened without changing which stars pass, and we measured exactly how the tax dilutes the saving (Figure F8). The principle is not refuted; a specific, identified configuration is.

**Scope and caveats.** (i) The 24.4% is the *scoped* reduction over fast-path-eligible stars, measured on a 12-star timing subset; the survey-representative figure is expected near-zero by construction and is not claimed. (ii) Relaxing the fairness keystone to common-FAR (v3) means an arm difference also reflects the intrinsic power gap between the LR confirmer and TLS, not routing alone; the full-TLS fallback mitigates this and the caveat is disclosed. (iii) **The test grid contained no monotransit cases** — all 15,000 injections had $\ge2$ transits over the S1–S3 baseline (Table T3, by regime) — so the monotransit regime, a known evidence-first advantage region (full TLS cannot fold single events), is *not exercised here*. It is deferred to a future campaign with longer-period / single-event injections, where the advantage is expected to appear.

**Future work (separately pre-registered).** The decisive lever is a **cheaper-but-provably-equivalent period-FAP** — the direction the equivalence gate closed for the two candidates tried, but which a better-constructed estimator could pass. Other directions (multi-harmonic testing; a recall-protective confirmer floor to remove the right-period/wrong-epoch losses; a clean-skip tier) are deferred to new experiments. None is a continuation of this one: v3 is the terminal amendment.

## 5. Conclusion

Evidence-first routing on TESS preserves recall but, in its sealed realization, does not reach a 30% compute saving — a pre-registered null on the compute branch, traced to the per-star bootstrap period-FAP entry tax. The recall principle survives; the compute claim awaits a cheaper, equivalent gate. We release the sealed benchmark, thresholds, and evaluation code to support replication and the identified next step.

## 6. Reproducibility & data availability

Pre-registration (`SCIENTIFIC_HYPOTHESIS.md` v2.1, `TRINETRA_X_PHASE1_VALIDATION.md` v3, `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` v1.2) was sealed as git tag `phase1-prereg-v3` (Seal #2b manifest `54f06a94…`) before the test read; thresholds as Seal #2 (`6292c018…`); the manifest as Seal #1 (`1f2d49e1…`). The test was read exactly once; `git diff` against the sealed tag is empty. Result record: `research/m4_evaluation/M4_TEST_RESULT.md`. Tables/figures regenerate from `data/manifests/m4/test_run/` via `research/m4_evaluation/make_paper_artifacts.py`. Repository: github.com/Ansul-S/TRINETRA-X.

## Figures & Tables

- **F3** — Completeness maps (full / combined / Δ) over $(P, R_p)$: `research/m4_evaluation/figures/F3_completeness_maps.png`.
- **F8** — Per-star runtime, both arms, with combined-arm stage breakdown: `research/m4_evaluation/figures/F8_runtime.png`.
- **T2/T3/T7** — Headline, recall-by-population, compute ledger: `research/m4_evaluation/M4_TABLES.md`.
- **F5** — Period recovery (recovered vs true; harmonic aliases): `research/m4_evaluation/figures/F5_period_recovery.png`.
- **F6** — Period-FAP calibration on null stars (cleaned vs raw): `research/m4_evaluation/figures/F6_fap_calibration.png`.
- **T4/T5** — FAP calibration; period/epoch accuracy: `research/m4_evaluation/M5_TABLES.md`.
- *To add:* F1 (single-transit SNR census), F4 (compute–recall frontier, calibration), F7 (monotransit — needs a single-event campaign), F9 (gate before/after), T1 (dataset manifest), T6 (reality check: TOIs/EBs — needs M6), T8 (gate ablation — needs M6); depth/$T_{14}$ recovery (needs re-run with logging).

## References

Compiled in `docs/references.bib`. In-text citations map to keys: TLS `HippkeHeller2019_TLS`; BLS `Kovacs2002_BLS`; wotan `Hippke2019_wotan`; lightkurve `Lightkurve2018`; TESS `Ricker2015_TESS`; SPOC `Jenkins2016_SPOC`; occurrence `KunimotoMatthews2020`; EB catalog `Prsa2022_TESSEB`; VSX `Watson2006_VSX`; AstroNet `ShallueVanderburg2018_AstroNet`; ExoMiner `Valizadegan2022_ExoMiner`; non-inferiority `Piaggio2012_NonInferiority`; conformal prediction `ShaferVovk2008_Conformal`. **Bibliographic details require a final NASA ADS verification pass before submission.**

---

*Draft v0.1. Living manuscript; numbers frozen to the sealed M4 read. Next: compile references, add M5/M6 figures/tables, tighten Methods §2.5 against DR-002, and decide venue (AJ/MNRAS).*
