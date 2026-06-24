# SCIENTIFIC HYPOTHESIS — TRINETRA-X

| Field | Value |
|-------|-------|
| **Document** | Formal Scientific Hypothesis & Research Proposal |
| **Version** | 2.1 |
| **Revised** | 2026-06-19 (v2.1: v3 re-registration consistency [DR-002] — assumption **A6** and the H1 mechanism clause relaxed from "same TLS engine + threshold both arms" → "**common false-alarm rate both arms**", per Finding B; arbiter realization = folded-photometry transit likelihood-ratio. CALIBRATION-only; TEST unread.) — 2026-06-15 (v2.0: resolves gap-analysis F1, F2, F6; supersedes v1.0) |
| **Status** | Phase I — Scientific Validation (pre-registration, re-sealed; v3 amendment pending Seal #2b) |
| **Project** | TRINETRA-X (see [`TRINETRA-X.md`](./TRINETRA-X.md)) |
| **Companion documents** | [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md) · [`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md) · [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) · [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) |

> This document states, in research-proposal form, the falsifiable scientific claims of TRINETRA-X. It governs Phase I and binds all downstream phases. It is written to support eventual peer-reviewed publication: every hypothesis is stated so that it can, in principle, be **rejected by observation**.

> **Revision note (v2.0, 2026-06-15).** This version completes the pre-registration before any data is read, per [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) and the gap analysis. **Critical/Must-fix:** F1 (compute rescoped to the fast-path-eligible population + survey-representative secondary endpoint with detector overhead $\rho_d$ and break-even $\pi^\star$); F2 (operational recovery predicate, [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §4.1); F6 (single occurrence-weighted primary estimand + multiplicity rule). **Should-fix, included in the same seal to avoid a second pre-data re-registration:** R-4 (committed block-bootstrap FAP scheme); R-5 (transit-preservation requirement, $\eta_{\min}=0.90$); R-6 (single-planet / strict-periodicity scope); R-7 (monotransit single-event vetting criterion). No results exist; resolving these now is pre-registration completion, not post-hoc tuning (non-negotiable #2).

---

## 0. Abstract

Transit surveys detect exoplanets by folding each star's light curve at thousands of trial periods and testing for a periodic dimming — an exhaustive, hypothesis-driven search whose cost scales poorly to the ~10⁵–10⁶ stars of modern missions. TRINETRA-X proposes an **evidence-first** alternative: detect individual transit-like events directly and cheaply, infer the orbital period from their spacing, and pay the full periodogram search only for the minority of stars where no local evidence exists. We hypothesize that, on TESS light curves, this routing reduces computational cost substantially **on the population that presents exploitable local evidence (the fast-path-eligible population)** — **without** a scientifically meaningful loss of detection recall — because (i) large planets produce single-transit signatures well above the noise, and (ii) any star lacking such evidence is routed to a full Transit Least Squares (TLS) search identical to the baseline. Survey-scale (prevalence-weighted) compute is reported as a pre-registered *secondary* endpoint, with the break-even prevalence $\pi^\star$ made explicit; survey-scale saving requires a clean-skip mechanism deferred to Phase II. This proposal formalizes that claim as a falsifiable, pre-registered experiment with explicit non-inferiority margins, success and failure criteria, and the assumptions on which the claim rests. The unifying principle, inherited and corrected from the project's lineage, is that **photometric significance — not the coincidence of event timing — is the arbiter of detection** (cf. [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §E–§F).

---

## 1. Scientific Rationale

The detectability of a single transit is governed by its signal-to-noise ratio,

$$\mathrm{SNR}_1 \;=\; \frac{\delta}{\mathrm{CDPP}(T_{14})}, \qquad \delta = \left(\frac{R_p}{R_\star}\right)^2,$$

where $\delta$ is the fractional transit depth and $\mathrm{CDPP}(T_{14})$ is the combined differential photometric precision on the transit-duration timescale (derived in [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md), §2). Because $\delta \propto (R_p/R_\star)^2$, the single-transit SNR of a Jupiter-class planet exceeds that of an Earth-class planet by a factor $\sim(R_{\rm Jup}/R_\oplus)^2 \approx 120$. The transiting-planet population is therefore **bimodal in single-transit detectability**: large planets clear any reasonable local-detection threshold in one event; small planets do not, and require the coherent averaging that only phase-folding provides.

This bimodality is the physical foundation of the proposal. It implies that a large fraction of detectable planets can be found **without** a period search, and that the stars for which a period search is genuinely necessary are a well-defined, identifiable minority — identifiable, crucially, by the *evidence the data presents*, not by the planet type (which is the unknown). Routing on evidence strength is thus not a heuristic but the only epistemically valid way to allocate computation under this physics (cf. [`TRINETRA-X.md`](./TRINETRA-X.md), Principle 4).

The prior incarnation of this idea (TRINETRA v3) validated the *efficiency* of evidence-first routing but failed scientifically because it allowed **timing coherence to substitute for photometric significance** and never calibrated its detection statistic against a null ([`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §E). TRINETRA-X retains the philosophy and repairs exactly that defect: a physics-based confirmation gate is the arbiter, and every significance statistic is calibrated. The present hypothesis tests whether, with that repair, evidence-first routing delivers a measurable advantage on real TESS data.

---

## 2. Primary Hypothesis (H1)

> **H1.** On TESS light curves, an evidence-first routing pipeline — a cheap local transit-event detector that *seeds* a narrow, physics-based confirmation search, with a full-TLS fallback for stars lacking local evidence — achieves planet-detection **recall non-inferior to full TLS** (non-inferiority margin $\delta_{\mathrm{NI}} = 2$ percentage points) while reducing **computational cost on the fast-path-eligible population by at least 30 %**. (Survey-representative compute is reported as a pre-registered *secondary* endpoint; see H1b-survey and §10.)

For statistical testing, H1 decomposes into two simultaneous claims, both of which must hold:

- **H1a (recall non-inferiority — primary).** The occurrence-weighted marginal completeness difference satisfies $\overline{\Delta R} > -\delta_{\mathrm{NI}}$, with $\delta_{\mathrm{NI}} = 0.02$ (primary estimand and decision rule defined in §6), evaluated over completeness cells with $N_{\rm tr}\ge 2$. "Recovered" is the operational predicate of [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §4.1, applied identically to both arms.
- **H1b (compute superiority — primary, scoped to fast-path-eligible population).** On the **fast-path-eligible population** — stars whose detector evidence meets the pre-registered routing threshold $\theta$, frozen on the calibration set (definition and freeze in [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §2 and Appendix A) — $C_{\text{comb}}/C_{\text{TLS}} \le 0.70$ on identical hardware. The detector overhead $\rho_d = C_{\rm det}/C_{\rm full}$ is included in $C_{\text{comb}}$ and reported explicitly (guardrail 2). Measurement defined in [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §4.
- **H1b-survey (compute, survey-representative — secondary, descriptive, non-gating).** On a mixed sample built at a pre-registered prevalence $\hat\pi$ (guardrail 3), report $C_{\text{comb}}/C_{\text{full}}$ as a function of $\pi$ together with the break-even prevalence $\pi^\star = \rho_d / f_p$ (theory in [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) §8.3). This endpoint characterizes — and is expected to bound near zero or negative at TESS-realistic $\pi$ — the survey-scale limitation that motivates the Phase II clean-skip tier (§10). It is **not** part of the Phase I pass/fail decision.

Here $R$ denotes completeness (recall) against injected transits in real TESS noise; "comb" is the combined fast-path + fallback system; "TLS" is full-grid TLS on every star. Both arms share identical preprocessing and are held to a **common false-alarm rate** (v3 keystone): the detector pre-screens and seeds the search, and Arm B confirms it with a calibrated folded-photometry transit likelihood-ratio at the seeded ephemeris, while any star the cheap gate does not confirm is re-searched by full TLS (the fallback). *(v2.0 required an identical TLS engine + threshold in both arms; Finding B proved that realization internally inconsistent — see [`decisions/DR-002_DECISION_RECORD.md`](./decisions/DR-002_DECISION_RECORD.md) and [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §2.)* An attribution caveat follows from the relaxation (a recall/compute difference now also reflects the confirmer-vs-TLS power gap, bounded by the fallback); it is reported, not hidden.

---

## 3. Null Hypothesis (H0)

> **H0.** Evidence-first routing confers no measurable advantage on TESS: either its recall is inferior to full TLS by more than the margin, **or** it fails to reduce compute by the required amount (or both).

Formally, the disjunction of the two component nulls:

- **H0a:** $R_{\text{comb}} - R_{\text{TLS}} \le -\delta_{\mathrm{NI}}$  (routing loses real planets), **or**
- **H0b:** $C_{\text{comb}}/C_{\text{TLS}} > 0.70$  (routing fails to save compute at non-inferior recall).

Rejecting H1 requires failing to reject **either** H0a or H0b. The experiment is constructed so that H0 is genuinely defeatable *and* genuinely able to win — the idea can be killed (cf. [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §5).

---

## 4. Secondary Hypotheses

These refine, mechanistically explain, or extend H1. They are reported but are **not** gating for the Phase I pass/fail decision.

- **H2 — Seed accuracy scales with single-transit SNR.** Fast-path recall is an increasing function of $\mathrm{SNR}_1$ and approaches full-TLS recall on the high-$\mathrm{SNR}_1$ (Jupiter/large-planet) population: $r_{\rm seed}(\mathrm{SNR}_1)\!\to\!1$ as $\mathrm{SNR}_1\!\to\!\infty$. This is the mechanism by which H1a can hold (math in [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md), §7).
- **H3 — Monotransit advantage (TESS-specific).** In the single-transit regime (orbital period $P >$ available baseline, $N_{\rm tr}=1$), evidence-first detection achieves **strictly higher** recall than full TLS, because a periodogram cannot fold a lone event. Monotransit candidates are confirmed by a dedicated **single-event vetting criterion** (transit shape, ingress/egress, secondary-eclipse absence, centroid; [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) §6), whose false-positive control is **weaker by construction** than the repeating-transit gate. Reported descriptively; excluded from the headline (an unfair cell for the baseline).
- **H4 — Statistical calibration.** The bootstrap false-alarm probability of period recovery and the confirmation-gate significance are **calibrated**: nominal-$\alpha$ thresholds yield empirical false-alarm rates $\le \alpha$ on planet-free (null) light curves.
- **H5 — Parameter recovery.** Recovered posteriors for period, depth, and duration achieve nominal interval coverage (e.g., 68 % credible intervals contain the injected truth $\approx$ 68 % of the time).
- **H6 — False-positive control.** The physics gate plus astrophysical classifier reject known false positives (eclipsing binaries, background eclipsing binaries, variables, systematics) at a high rate without measurable recall cost on confirmed planets.

---

## 5. Assumptions

The validity of H1 rests on the following assumptions, each stated so it can be checked rather than presumed.

- **A1 — Detectability bimodality holds for TESS.** A scientifically meaningful fraction of transiting planets satisfy $\mathrm{SNR}_1 \ge z_\star$ (the local-detection threshold). *Check:* compute $\mathrm{SNR}_1$ for the confirmed TESS planet population; confirm the bimodal structure observed for Kepler ([`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §D).
- **A2 — Conditioning yields locally stationary residuals.** Per-sector detrending leaves residuals approximately stationary on transit-duration timescales, so a local noise estimate is meaningful. *Check:* residual stationarity diagnostics post-conditioning.
- **A3 — Injection fidelity.** Synthetic transits injected into **real** TESS light curves reproduce the detectability of real transits because the real correlated noise is preserved. *Check:* compare recovery of injected vs. confirmed-TOI transits at matched parameters (H5 / reality-check set).
- **A4 — Characterizable noise.** TESS noise, though red, is locally characterizable (robust scatter / Gaussian-process covariance), enabling a calibrated local detection statistic. *Check:* noise-model residual whiteness after GP/robust modeling.
- **A5 — Reliable external labels.** TOI and eclipsing-binary catalogs provide labels of sufficient reliability for the reality-check set. *Check:* cross-catalog agreement on a held-out subset.
- **A6 — Fair benchmark (v3: common false-alarm rate).** Holding both arms to a **common false-alarm rate** — Arm A via TLS SDE $\ge T$, Arm B via the folded-transit likelihood-ratio $\Lambda \ge T_{\rm red}$, each calibrated to the same null FAR — compares the methods at **equal precision / false-alarm rate**, isolating recall and compute up to the confirmer-vs-TLS power gap (bounded by the full-TLS fallback). *Check:* equalize thresholds to a common false-alarm rate on the calibration set ([`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §2, A.2/A.11). *(v2.0 stated this as "same TLS engine + threshold both arms"; amended per DR-002 Finding B — the targeted-TLS realization is non-executable because the TLS SDE is not comparable across grid widths.)*
- **A7 — Detector overhead is small enough to be earned back on the fast-path-eligible population, and survey-scale saving is prevalence-limited.** The scoped compute claim (H1b) requires $\rho_d + \rho \le 0.70$ on fast-path-eligible stars, where $\rho = C_{\rm fast}/C_{\rm full}$. Survey-scale saving requires $\pi\,f_p > \rho_d$, i.e. prevalence above break-even $\pi^\star = \rho_d/f_p$; at TESS-realistic $\pi \sim 10^{-2}$ this is generally not met without a clean-skip mechanism (deferred to Phase II). *Check:* measure $\rho_d$, $\rho$, and $f_p$ directly on fixed hardware during calibration (M3) and the sealed run (M4); report $\pi^\star$.
- **A8 — Conditioning preserves transits.** Per-sector detrending removes stellar/instrumental variability **without** significantly attenuating transit depth or distorting transit shape on transit-duration timescales. Over-aggressive detrending is a known recall sink. *Check:* inject transits, apply Stage-0 conditioning, and measure the recovered-vs-injected depth-attenuation factor $\eta$ and shape distortion; require median $\eta \ge 0.90$ ([`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §4.2). The attenuation is shared by both arms (it precedes detection) and so cancels in $\Delta R$, but it caps **absolute** recall and is reported (rebuts reviewer concern PR-H).
- **A9 — One detectable transiting planet per star (Phase I scope).** Event→period→confirm assumes a single period; multi-planet systems interleave events of different periods and can alias or defeat phase-coherence recovery. Phase I **scopes the recall claim to single-planet recovery**; multiplicity handling (iterative event masking) is deferred to Phase II. *Check:* flag injected/known multi-planet systems and report their recovery separately, excluded from the headline.
- **A10 — Strict periodicity for period recovery.** Recovering $P$ from event spacing assumes constant $P$ ($\hat t_j - \hat t_i = m_{ij}P$); significant transit-timing variations (TTVs) smear phase concentration and degrade recovery. The **"model-agnostic" generality** of evidence-first detection is therefore scoped to the **event-detection stage only**, not to period recovery. TTV tolerance is a bounded quantity to be *measured*, not a claimed advantage. *Check:* report recovery vs. injected TTV amplitude as a secondary.

Violation of any assumption does not merely weaken H1 — it changes what a pass or fail *means*, and must therefore be reported alongside the result.

---

## 6. Non-Inferiority Definitions

Recall is the **primary endpoint**, and the claim is one of *non-inferiority*, not superiority: TRINETRA-X need not detect more planets than TLS — it must not detect meaningfully fewer, while costing less.

- **Margin.** $\delta_{\mathrm{NI}} = 0.02$ (2 percentage points, absolute completeness). Chosen as a standard, scientifically defensible margin: small enough that a pass protects recall, large enough to be decidable with attainable sample sizes ([`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §6).
- **Primary estimand (single, pre-registered).** The **occurrence-weighted marginal completeness difference**
  $$\overline{\Delta R} = \sum_{c\,:\,N_{\rm tr}\ge 2} w_c\,\bigl(R_{\text{comb},c} - R_{\text{TLS},c}\bigr), \qquad \sum_c w_c = 1,$$
  over the eligible $(P, R_p)$ cells of the **sealed test** injection set, where $R_{\cdot,c}$ is completeness under the operational recovery predicate ([`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §4.1) and the weights $w_c$ are the **pre-registered occurrence prior** frozen in [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) Appendix A.5 (log-uniform in $P$ × Kunimoto & Matthews 2020 radius occurrence). The same paired injections are used in both arms.
- **Primary decision.** Non-inferiority is **declared** iff the lower bound of the one-sided 95 % confidence interval on $\overline{\Delta R}$ exceeds $-\delta_{\mathrm{NI}} = -0.02$ (interval propagated from the per-cell paired-binomial outcomes; Wilson/Clopper–Pearson per cell, combined under the fixed weights).
- **Secondary (descriptive, never gating).** Per-cell $\Delta R_c$ are reported with cell-level CIs; if cell-level screening is used it applies a **pre-specified Holm correction** at family-wise $\alpha = 0.05$ and is reported as secondary only. A single failing cell does **not** by itself falsify H1a; the primary decision is on $\overline{\Delta R}$ alone.
- **Mechanistic bound.** Because the fallback *is* full TLS, recall can be lost only on stars routed to the fast path:
  $$\Delta R \;=\; -\,f\,\bigl(1 - r_{\rm seed}\,g\bigr),$$
  where $f$ is the fast-path routing fraction, $r_{\rm seed}$ the probability of seeding the correct period for a true planet, and $g$ the gate confirmation efficiency. Non-inferiority is therefore the requirement $f\,(1 - r_{\rm seed}\,g) \le \delta_{\mathrm{NI}}$ (derived in [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md), §8).

---

## 7. Falsifiability Criteria

The proposal is falsifiable in the strict sense: pre-specified observations would compel rejection of H1. TRINETRA-X is **falsified** (in Phase I) if, on the sealed test set:

1. **Recall falsification.** The lower 95 % bound of $\Delta R < -\delta_{\mathrm{NI}}$ — the fast path drops real planets that TLS would have found, beyond the margin. *(This is the precise failure mode that ended v3, now testable in advance.)* **Or**
2. **Compute falsification.** $C_{\text{comb}}/C_{\text{TLS}} > 0.70$ at non-inferior recall — the routing fraction is too small for the principle to matter on TESS.

A result that is **inconclusive** (confidence intervals wider than the margin) is *not* a pass; it triggers a pre-planned increase in injection sample size, with thresholds and truth held fixed (no re-tuning; [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §6–§7).

---

## 8. Success Criteria

Aligned with the tiered goals of [`TRINETRA-X.md`](./TRINETRA-X.md) and operationalized here.

| Tier | Criterion (must hold on the sealed test set) |
|------|----------------------------------------------|
| **Phase I pass (Minimum)** | H1a holds (primary estimand $\overline{\Delta R}$ lower bound $> -0.02$, §6) **and** H1b holds ($C_{\text{comb}}/C_{\text{TLS}} \le 0.70$ on the **fast-path-eligible population**, detector overhead $\rho_d$ included and reported) **and** false-alarm control on null stars is calibrated (H4). The survey-representative figure (H1b-survey) and $\pi^\star$ are reported but do **not** gate the pass. |
| **Target** | Minimum **plus**: fast-path recall matches full-TLS recall to within $\delta_{\mathrm{NI}}$ on the Jupiter / large-planet population (H2 confirmed); demonstrable monotransit recovery exceeding TLS (H3); compute reduction materially beyond 30 %. |
| **Stretch** | Target **plus**: calibrated parameter posteriors (H5) and false-positive rejection without recall cost (H6) on the reality-check set — establishing the full evidence → confirm → classify chain end-to-end, the precursor to a paradigm claim. |

Per the non-negotiables ([`TRINETRA-X.md`](./TRINETRA-X.md)): no tuning on test data; every claim benchmarked against TLS on identical data; every confidence calibrated.

---

## 9. Failure Criteria

A failure is a scientific result, not a setback, and is to be reported with equal rigor.

- **Recall failure (H0a not rejected).** Diagnosis: the local detector cannot seed periods reliably enough in real TESS noise; $r_{\rm seed}\,g$ is too low on the routed population. *Implication:* evidence-first routing, as posed, does not preserve recall on TESS — the same verdict v3 earned, obtained honestly and early. Do **not** proceed to Phase II.
- **Compute failure (H0b not rejected).** Diagnosis: even on the fast-path-eligible population, $C_{\text{comb}}/C_{\text{TLS}} > 0.70$ — the per-star fast-path cost (including detector overhead $\rho_d$ = detector + cheap period-FAP) is too high, or the cheap confirmer saves too little, so routing does not earn ≥30 % on the population where it is supposed to be cheapest. *Implication:* evidence-first routing does not deliver a compute advantage even where evidence exists; full TLS remains the correct tool. Equally publishable as a negative result. (Note: a near-zero or negative **survey-representative** figure at TESS-realistic $\pi$ is *expected by construction* — see §10 — and is **not** a Phase I failure; it is the pre-registered motivation for the Phase II clean-skip tier.)
- **Assumption failure.** If a check in §5 fails (e.g., A1 bimodality absent, A3 injection infidelity), the experiment is **inconclusive about the hypothesis**; the assumption violation is the finding, and the protocol is revised under a new pre-registration.

---

## 10. Scope, Limitations, and Relationship to Later Phases

Phase I tests **only** the routing-vs-physics-detection claim (H1) and its mechanistic / calibration corollaries (H2, H4). It deliberately excludes — as Phase II–IV work conditional on a Phase I pass — the learned detector, the astrophysical classifier (H6 at scale), calibrated planet probabilities, and habitability scoring ([`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md), Stages 1, 4, 5; [`TRINETRA-X.md`](./TRINETRA-X.md), Milestones). Phase I uses a **simple, untrained** local detector by design, so that a pass or fail is attributable to the *routing principle* rather than to model quality.

Phase I deliberately **does not** attempt survey-scale compute reduction. On a survey-representative population the planetless majority presents no local evidence and routes to the full-TLS fallback, so the prefilter is net overhead (saving $\approx \pi f_p - \rho_d$; [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) §8.3). Survey-scale saving therefore requires a **calibrated clean-skip tier** that skips the full search on no-evidence stars — which trades recall and so demands its own non-inferiority test. That mechanism is **deferred to Phase II** (out of Phase I scope); Phase I only *quantifies* the survey-scale frontier (H1b-survey, $\pi^\star$) so the Phase II need is established on evidence rather than assertion.

The governing philosophy is preserved throughout and stated once more for the record:

> **Find evidence first. Spend computation second. Let physics decide.** Recall is sacred; a false positive is acceptable, a missed planet is not; and *photometric significance, not timing coincidence, is what makes a candidate a planet.*

---

*Hypothesis document v2.0 (2026-06-15). Pre-registered claims; no results herein. Supersedes v1.0 and any informal hypothesis statements in companion documents where they conflict.*
