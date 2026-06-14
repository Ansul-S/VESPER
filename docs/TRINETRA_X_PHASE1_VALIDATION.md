# TRINETRA-X — Phase I Scientific Validation (PRE-REGISTRATION)

**Version:** 2 (re-dated 2026-06-15; supersedes v1 frozen 2026-06-14). **Status:** PRE-REGISTERED, re-sealed before any results exist.
**v2 changes (no data read).** Critical/Must-fix: F1 — compute scoped to fast-path-eligible population + survey-representative secondary endpoint ($\rho_d$, $\pi^\star$); F2 — operational recovery predicate (§4.1); F6 — single occurrence-weighted primary estimand + multiplicity (§4–§5); F8 — thresholds, TLS baseline, runtime protocol (Appendix A). Should-fix folded into the same seal: R-4 — block-bootstrap FAP scheme (A.8); R-5 — transit-preservation requirement (§4.2, A.9); R-6 — single-planet/strict-periodicity scope; R-7 — monotransit vetting (MATH §6, A.3). See [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) + [`REPOSITORY_GAP_ANALYSIS.md`](./REPOSITORY_GAP_ANALYSIS.md).
**Mission:** Determine whether evidence-first routing provides a *measurable* advantage over BLS/TLS on TESS light curves — lower compute at non-inferior recall.
**Governing non-negotiables:** (1) recall > precision; (2) no tuning on test data; (3) physics decides detection; (4) every metric benchmarked; (5) every confidence calibrated.

> This document fixes the hypotheses, datasets, parameters, and decision rules **in advance**. Any change after results are seen requires a new, dated pre-registration. This is the mechanism that enforces non-negotiable #2.

---

## 1. THE CLAIM, AS A FALSIFIABLE HYPOTHESIS

Evidence-first routing makes two separable claims:

- **H₁ — recall non-inferiority.** The combined system (fast path + fallback) recovers injected planets at a rate no worse than full TLS by more than **δ = 2 percentage points** (absolute).
- **H₂ — compute superiority (primary, scoped).** On the **fast-path-eligible population** (detector evidence ≥ θ; §2, Appendix A), the combined system's compute is at least **30% lower** than full TLS, at non-inferior recall, with detector overhead $\rho_d$ included.
- **H₂-survey — compute, survey-representative (secondary, descriptive).** On a mixed sample at pre-registered prevalence $\hat\pi$, report $C_{\rm comb}/C_{\rm full}$ vs $\pi$ and the break-even $\pi^\star = \rho_d/f_p$. Non-gating (§4–§5).

**Mechanistic identity that makes this clean.** Because the fallback *is* full TLS and the fast-path gate *is* the same TLS engine on a narrow grid, recall can be lost in exactly one place:

```
combined_recall_loss        =  (fraction routed to fast path) × (planets the detector seeds at the WRONG period)
compute_saving (eligible)   ≈  1 − (ρ_d + ρ)        with ρ = narrow-grid cost / full-grid cost,  ρ_d = detector cost / full-grid cost
compute_saving (survey)     ≈  π·f_p − ρ_d           ⇒  break-even prevalence  π* = ρ_d / f_p
```

So Phase I is, precisely: **does a cheap untrained detector route enough stars to a narrow-grid TLS — with the right period seed — to save compute without dropping planets that full TLS would have found?** Detector quality shows up only as *routing fraction* and *seed accuracy*; the detection physics is identical in both arms.

---

## 2. DESIGN PRINCIPLE: ISOLATE THE ROUTING VARIABLE

Both arms share **identical preprocessing** and **identical detection physics (TLS)**. The *only* manipulated variable is whether the detector pre-screens and seeds the search.

| | **Arm A — Baseline** | **Arm B — TRINETRA-X (evidence-first)** |
|---|---|---|
| Preprocess | per-sector detrend + masking (shared) | same |
| Detect | — | simple untrained local detector → events |
| Route | always full search | evidence ≥ θ → fast path; else → fallback |
| Period | full TLS grid | seed from event spacing (+ bootstrap FAP) |
| **Confirm (arbiter)** | **TLS, SDE ≥ T** | **targeted TLS on [P̂(1−ε), P̂(1+ε)], SDE ≥ T** (fallback = full TLS, SDE ≥ T) |
| Decision threshold T | same SDE threshold, set to a common false-alarm rate on the CALIBRATION set | same |

Using the **same TLS engine and the same SDE threshold T** in both arms is the fairness keystone: it compares at equal precision, so any recall difference is attributable to routing/seeding alone, and the compute difference is transparent (narrow grid vs full grid).

**Fast-path-eligible population (defined for H₂; guardrail 1).** A star is *fast-path-eligible* iff its detector evidence meets the pre-registered routing threshold θ (multi-event: ≥ $N_{\min}$ events; monotransit: a single event with $\mathrm{SNR}_1 \ge z_{\rm mono}$). θ, $z_\star$, $z_{\rm mono}$, $N_{\min}$, the common SDE threshold $T$, the TLS baseline configuration, and the runtime protocol are **frozen on the calibration set** and recorded in **Appendix A**. Eligibility is thus an operational, reproducible class fixed *before* the sealed test — not defined on the test outcome — which is what makes the scoped H₂ non-circular.

---

## 3. DATASETS (frozen)

**Source.** TESS SPOC 2-minute PDCSAP_FLUX from a fixed list of sectors (recorded in the frozen manifest). FFI/QLP excluded from Phase I to remove a pipeline confound.

**Splits — disjoint by sky region / TIC to prevent leakage.** Because the detector is *untrained*, there is **no training split** — a deliberate simplification of the "simple, no training" choice.
- **CALIBRATION set** — used *only* to fix thresholds (detector evidence θ, routing rule, TLS SDE T, bootstrap-FAP cutoff, confidence calibration).
- **TEST set** — sealed; evaluated **once**.

**Primary truth — injection-recovery (into real light curves).** Inject physical (Mandel–Agol + limb-darkening from stellar params) transits into real TESS light curves, preserving real correlated noise. Frozen grid:
- Period P (days): {0.5, 1, 2, 4, 8, 16} — chosen so most cells yield ≥2 transits in the available baseline.
- Planet radius Rp (R⊕): {1, 2, 4, 8, 12} → depth via stellar radius.
- Impact parameter b: {0.0, 0.3, 0.6}.
- ≥ **500 injections per (P, Rp) cell** (sample size from the power analysis in §6), fixed RNG seed.
- **n_transits** recorded as an explicit axis (derived from P and per-target baseline).

**Reality check — real labels (secondary).** Confirmed TESS Objects of Interest (planets) + known false positives (EBs/BEBs/variables) in the same sectors. Used to confirm the injection-based conclusions transfer to real signals; **not** part of the headline pass/fail (truth is incomplete and selection-biased).

**Survey-representative compute sample (for H₂-survey; secondary).** A mixed sample at a **pre-registered prevalence** $\hat\pi$, derived as TESS planet occurrence × geometric transit probability using the Kunimoto & Matthews (2020) occurrence framework (source and value frozen in Appendix A.6). Planets are injected into only a $\hat\pi$ fraction of stars; the remainder are **real, known-TOI-removed** light curves carrying genuine correlated noise (no injected planet). Compute is measured over this sample to report $C_{\rm comb}/C_{\rm full}$ as a function of $\pi$ and the break-even $\pi^\star$. This sample is used for the **compute secondary endpoint only** — never for the recall pass/fail.

---

## 4. ENDPOINTS & METRICS

**4.1 Operational recovery predicate (applies identically to both arms).**
An injected planet $(P_{\rm true}, t_{0,\rm true}, \delta_{\rm true})$ is counted **recovered** by an arm iff that arm returns a detection satisfying **all** of:
- **(i) Period.** $|\hat P - P_{\rm true}|/P_{\rm true} < 0.01$, **or** $\hat P$ matches a harmonic $\{P_{\rm true}/m,\, m P_{\rm true}\}$, $m\in\{2,3\}$, within the same 1 % tolerance. Harmonic matches are counted as recovered (the planet was found) but are **flagged and reported separately** so the alias rate is visible.
- **(ii) Epoch.** the recovered ephemeris aligns to a true transit within $\pm 0.5\,T_{14}$.
- **(iii) Significance.** the arm's TLS SDE $\ge T$, the single common threshold of Appendix A.

Completeness $R$ is the fraction of injected planets recovered, computed per $(P, R_p)$ cell and aggregated via the F6 primary estimand (§4.2/§5). Applying one predicate to both arms preserves the fairness keystone (§2).

**4.2 Transit-preservation requirement (required pre-M3 check).** Before thresholds are frozen, measure conditioning-induced transit attenuation: inject Mandel–Agol transits at the grid parameters, apply Stage-0 conditioning, and compare recovered depth $\hat\delta_{\rm post}$ to injected $\delta_{\rm true}$. Report the median depth-attenuation factor $\eta = \hat\delta_{\rm post}/\delta_{\rm true}$ and a shape-distortion diagnostic per $(P, R_p)$ cell; **require median $\eta \ge \eta_{\min} = 0.90$** (Appendix A.9). Because conditioning precedes detection in both arms, $\eta$ cancels in the paired $\Delta R$ comparison but bounds absolute recall — it is reported, not hidden. If $\eta < \eta_{\min}$ in a cell, the conditioning configuration is revised **before** any threshold is set (never after the test).

**Primary**
- **E1 — recall non-inferiority (primary).** The F6 **occurrence-weighted marginal completeness difference** $\overline{\Delta R} = \sum_{c:N_{\rm tr}\ge2} w_c(R_{\text{comb},c} - R_{\text{TLS},c})$ on the TEST injection set, with weights $w_c$ frozen in Appendix A.5. **Pass** iff the lower bound of the one-sided 95 % CI on $\overline{\Delta R}$ is **> −2 pp**. Per-cell $\Delta R_c$ reported as secondary (Holm-corrected if screened; never gating). Recovery per §4.1; cells with **n_transits ≥ 2**.
- **E2 — compute, fast-path-eligible (primary).** Compute ratio (combined / full-TLS) on the **fast-path-eligible population** (§2), on identical hardware, **including detector overhead $\rho_d$**. Pass if reduction **≥ 30 %** at non-inferior recall (E1). Report $\rho_d$ and the per-stage ledger.
- **E3 — compute, survey-representative (secondary, descriptive).** On the survey-representative sample (§3), report $C_{\rm comb}/C_{\rm full}$ as a function of $\pi$ and the break-even $\pi^\star = \rho_d/f_p$. **Not** pass/fail; expected ≈ 0 or negative at TESS-realistic $\hat\pi$ (this is the pre-registered survey-scale limitation, not a failure).

**Secondary (descriptive, reported, not pass/fail)**
- Routing fraction (% to fast path) and **fast-path-conditional recall**.
- **Recall–compute frontier** as a function of routing threshold θ — computed on the **CALIBRATION set only** (showing it on test would be tuning).
- Recovered-parameter accuracy for P, depth, duration, with **interval coverage** (do 1σ intervals contain truth ~68%?).
- **Calibration** of the bootstrap FAP / gate significance: ECE + reliability diagram. The FAP null uses the **frozen block-bootstrap scheme** (MATH §9.1, Appendix A.8); calibration is verified on null stars (empirical FAR $\le \alpha_{\rm FAP}$, H4).
- **Monotransit sub-analysis** (n_transits = 1): reported separately as a known evidence-first advantage region — excluded from the headline because full TLS also cannot fold single events (an unfair cell for the baseline). Monotransit candidates are confirmed by the **single-event vetting criterion** (MATH §6; routing threshold $z_{\rm mono}$, Appendix A.3), with explicitly **weaker FP control** noted; monotransit FP rate on null stars is reported.
- Real-label check: recall on confirmed TOIs; FP-rejection rate on known FPs.

**Compute accounting.** Single-thread **CPU-core-seconds** per star on the fixed machine of Appendix A (median over ≥ 5 repeats, warm cache; full distribution reported, not just the mean). Phase I uses a **CPU** detector, so the comparison is clean CPU-vs-CPU (no GPU-vs-CPU confound). Arm B cost = detector ($\rho_d$, charged on every routed star) + period inference + targeted/fallback TLS; Arm A cost = full TLS. **Shared Stage-0 conditioning is excluded** (or charged equally to both arms) so the comparison isolates search cost. The fast-path-eligible aggregate (E2) and the prevalence-weighted aggregate (E3) are both reported, derived from the identical per-star ledger.

---

## 5. DECISION RULE (stated before results)

- **VALIDATED** iff **E1 passes** (primary estimand $\overline{\Delta R}$ lower bound ≥ −2 pp) AND **E2 passes** (≥ 30 % compute reduction on the fast-path-eligible population, $\rho_d$ included). E3 and $\pi^\star$ are reported but do not gate.
- **FALSIFIED** if $\overline{\Delta R}$ lower bound **< −2 pp** (routing drops real planets) — OR — E2 reduction **< 30 %** at non-inferior recall (no advantage even where evidence exists).
- **INCONCLUSIVE** if the CI on $\overline{\Delta R}$ (or on E2) is too wide to decide (underpowered) → pre-planned sample-size increase, thresholds and truth unchanged.
- **Out of scope (not a verdict):** a near-zero/negative survey-representative figure (E3) at TESS-realistic $\hat\pi$ — expected by construction; motivates the Phase II clean-skip tier (§8).

This is symmetric: the experiment is allowed to **kill** the idea. A pass means routing earns its place on TESS; a fail means it does not, and we report that.

---

## 6. POWER & SAMPLE SIZE (fixed in advance)

To detect a 2 pp non-inferiority margin against an assumed baseline recall around 80–90% with ~90% power at α=0.05, each (P, Rp) completeness cell needs on the order of several hundred injections; we fix **≥500 injections/cell** and **≥ a few ×10³ total**, then confirm the realized CI width supports a decision. If any headline cell's CI half-width exceeds the 2 pp margin, that cell is declared INCONCLUSIVE and re-run with more injections — truth and thresholds unchanged.

---

## 7. ANTI-TUNING SAFEGUARDS (non-negotiable #2)

- TEST set sealed until the single, final evaluation.
- All thresholds (θ, routing rule, T, FAP cutoff, ε window) **frozen from the CALIBRATION set** and hash-recorded before the test run.
- Exactly **one** test evaluation. No threshold edits post-hoc; any change ⇒ new pre-registration with a new date.
- The recall–compute frontier and all operating-point selection happen on CALIBRATION data only.

---

## 8. EXPLICIT NON-GOALS FOR PHASE I

No learned/trained models. No dashboards. No deployment or API. No full-catalog production run (scope = the frozen sample). No hyperparameter search against the test set. No habitability scoring or classification model — Phase I tests **only** the routing-vs-physics-detection claim. **No clean-skip / noise-floor skipping of the full TLS search on no-evidence stars** — this is the only mechanism that could yield *survey-scale* compute saving, it trades recall, and it therefore requires its own non-inferiority test; it is **deferred to Phase II**. Classification, FP-class modeling, learned detectors, and calibrated planet probabilities are Phase II, conditional on a Phase I pass.

---

## 9. WHAT A PASS / FAIL WOULD MEAN

- **Pass:** evidence-first routing is a real, measurable efficiency gain on TESS at protected recall — justifying Phase II (learned detector, classifier, calibrated confidence, the full TRINETRA-X stack).
- **Fail (recall):** the detector cannot seed periods reliably enough; the routing idea does not survive contact with real TESS noise — the same verdict v3 earned, now obtained honestly and early.
- **Fail (compute):** routing fraction is too low to matter; full TLS stays the right tool. Equally publishable, equally valuable to know before building anything larger.

---

---

## Appendix A — Frozen Parameters & Baseline Configuration

> **Two-step freeze (read first).** This appendix freezes the **procedure and targets** now (v2, no data read). The **numeric** values of calibration-derived thresholds ($z_\star, \theta, z_{\rm mono}, T, \alpha, \alpha_{\rm FAP}, \varepsilon$) are set on the CALIBRATION set during milestone **M3**, then **hash-sealed before the single sealed-test run (M4)**. Deriving thresholds from calibration data is not tuning (non-negotiable #2); deriving them from test data would be. Values marked `[sealed at M3]` are filled and hashed at M3.

**A.1 TLS baseline (identical engine in both arms — the fairness keystone).**
- Implementation: `transitleastsquares` (Hippke & Heller 2019); record exact version.
- Period sampling: optimal/Ofir (2014) over $[P_{\min}, P_{\max}]$ matched to the injection grid; record oversampling factor.
- Duration grid: default; limb-darkening from TIC stellar parameters.
- Fast-path confirmation: the **same** TLS engine on the narrow window $[\hat P(1-\varepsilon), \hat P(1+\varepsilon)]$.

**A.2 Common significance threshold $T$.** TLS SDE threshold set so the empirical false-alarm rate on **null (planetless) calibration stars** equals a pre-registered $\alpha$ (target **FAR ≤ 1 % per star**). **Both arms use this identical $T$.** Value: `[sealed at M3]`.

**A.3 Detector threshold & routing ($z_\star$, θ).** $z_\star$ set on the calibration set to a target local false-event yield (**≤ 1 expected false event per null light curve**). Routing rule: multi-event fast path iff $\ge N_{\min}$ events with $N_{\min} = 2$; monotransit branch iff a single event has $\mathrm{SNR}_1 \ge z_{\rm mono}$ for a stated $z_{\rm mono} > z_\star$. Values: `[sealed at M3]`.

**A.4 Recovery predicate.** As §4.1 (period 1 % / harmonics $m\in\{2,3\}$ flagged; epoch $\pm 0.5\,T_{14}$; SDE ≥ $T$).

**A.5 F6 occurrence weight prior $w_c$ (FROZEN).** $w_c \propto w_P(P)\,w_R(R_p)$, normalized to $\sum_c w_c = 1$ over eligible cells, where:
- $w_P(P)$ is **log-uniform** over the period nodes {0.5, 1, 2, 4, 8, 16} d restricted to $N_{\rm tr}\ge 2$ cells (equal weight per node in $\log P$).
- $w_R(R_p)$ is the **radius-occurrence weighting from Kunimoto & Matthews (2020)**, evaluated at the grid radii {1, 2, 4, 8, 12} $R_\oplus$ (occurrence integrated over each radius node's bin).
This is the sole pre-registered weighting and is not revisited post-hoc.

**A.6 Survey-representative prevalence $\hat\pi$ (FROZEN).** $\hat\pi = $ (TESS planet occurrence) × (geometric transit probability), where the occurrence term is integrated over the injection grid's $(P, R_p)$ support using the **same Kunimoto & Matthews (2020) occurrence framework as A.5**, and the geometric term is $\langle R_\star/a\rangle$ for the target sample. The single frozen scalar $\hat\pi$ and its integration bounds are recorded here before any data; used only for E3 (reported as a curve over $\pi$ in addition to the point at $\hat\pi$).

**A.7 Runtime protocol.** One specified machine (record CPU model, cores, clock); single-thread **CPU-core-seconds**; median over ≥ 5 repeats; warm cache; report the full distribution. Shared Stage-0 conditioning excluded (or charged equally to both arms). Detector overhead $\rho_d$ measured and reported separately.

**A.8 Bootstrap-FAP resampling (frozen).** Noise-model-aware **circular block bootstrap** (MATH §9.1). Block length $L_b = 3\times\max(\tau_{\rm GP},\,T_{14})$, where the GP correlation timescale $\tau_{\rm GP}$ is measured per target during conditioning (calibration-derived, like other thresholds); $B \ge 1000$ surrogates over the identical period grid; bootstrap-FAP cutoff $\alpha_{\rm FAP}$ `[sealed at M3]` set to a target null exceedance. Calibration verified on null stars (H4).

**A.9 Conditioning & transit preservation (frozen).** Stage-0 per-sector detrend (GP/biweight kernel and window frozen here; record exact `wotan`/`celerite2` parameters); momentum-dump (~2.5 d) and scattered-light/quality masking. Transit-preservation tolerance: median depth-attenuation factor $\eta = \hat\delta_{\rm post}/\delta_{\rm true} \ge \eta_{\min} = 0.90$ per eligible cell (measured per §4.2 before thresholds are frozen).

**A.10 Manifest hash.** On M3 completion, all `[sealed at M3]` values + this appendix (A.1–A.9) are hashed into the frozen manifest; the hash is recorded before M4. Exactly one sealed-test evaluation follows.

---

*Pre-registration only — no code, no results. Implementation begins with the shared Stage-0 conditioning and the CALIBRATION-set threshold-fixing, on one frozen set of TESS sectors.*
