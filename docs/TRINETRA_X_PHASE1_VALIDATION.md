# TRINETRA-X — Phase I Scientific Validation (PRE-REGISTRATION)

**Version:** 3 (re-dated 2026-06-19; supersedes v2 frozen 2026-06-15). **Status:** PRE-REGISTERED, re-sealed before any TEST results exist. **TEST split never read.** **v3 is the FINAL permissible amendment (stopping rule §7a / DR-002).**
**v3 changes (CALIBRATION-only; TEST not read; authority [`DR-002`](./decisions/DR-002_DECISION_RECORD.md)).** Forced by **Finding B** — the targeted-TLS confirmation realization is internally inconsistent (TLS SDE is normalized across the search grid, so a narrow-grid SDE is not comparable to the full-grid threshold $T$). Two amendments, both decided pre-TEST: **(A)** the **fairness keystone A6** is relaxed from "same TLS engine + threshold both arms" → "**common false-alarm rate both arms**"; Arm B's confirmation becomes an **epoch-fixed folded-photometry transit likelihood-ratio** $\Lambda$ at $(\hat P, \hat t_0)$ with threshold $T_{\rm red}$ set to the same FAR, plus full-TLS fallback (§2, §4.1(iii), A.1, A.2, A.11; MATH §6). **(B)** the period-FAP estimator (A.8) is replaced — under a mandatory **numerical-equivalence gate** (§A.8a) — from the $B=1000$ live block-bootstrap to a cheaper estimator (per-star EVT / precomputed null) computing the **same** sealed FAP at the **same** $\alpha_{\rm FAP}$; it reverts to the bootstrap (confirmer-only v3) if the gate fails. Adds the **amendment policy + stopping rule P-1…P-9** and the **pre-committed outcome mapping** (§7a). **No sealed threshold, grid, occurrence prior, or $\alpha$ value is changed by v3** ($z_\star, z_{\rm mono}, N_{\min}, T{=}10.74, \alpha_{\rm FAP}, \varepsilon, w_c, \hat\pi$ unchanged); $T$ remains the full-grid SDE threshold for Arm A and the fallback.
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

**Mechanistic identity that makes this clean.** Because the fallback *is* full TLS, and the fast-path gate is a calibrated physics confirmer **held to the same false-alarm rate as the baseline** (v3: a folded-photometry transit likelihood-ratio at the seeded ephemeris; v2 specified the same TLS engine on a narrow grid — see §2 and DR-002 Finding B), recall can be lost in exactly one place:

```
combined_recall_loss        =  (fraction routed to fast path) × (planets the detector seeds at the WRONG period AND the confirmer then rejects, net of full-TLS fallback)
compute_saving (eligible)   ≈  1 − (ρ_d + ρ)        with ρ = confirmer cost / full-grid cost,  ρ_d = (detector + cheap period-FAP) cost / full-grid cost
compute_saving (survey)     ≈  π·f_p − ρ_d           ⇒  break-even prevalence  π* = ρ_d / f_p
```

So Phase I is, precisely: **does a cheap untrained detector route enough stars to a cheap, calibrated transit confirmer — with the right period seed — to save compute without dropping planets that full TLS would have found?** Detector quality shows up as *routing fraction* and *seed accuracy*; the confirmation is a §6-admissible transit-significance gate held to a common false-alarm rate with the baseline (v3 keystone), and the full-TLS fallback re-searches any star the cheap gate rejects, so a routed planet is lost only if both the seed is wrong and the fallback misses it.

---

## 2. DESIGN PRINCIPLE: ISOLATE THE ROUTING VARIABLE

Both arms share **identical preprocessing**. The manipulated variable is whether the detector pre-screens and seeds the search and confirms it with a cheap physics gate; **both arms' confirmation is held to a common false-alarm rate** (v3 keystone, below), and any star the cheap gate does not confirm is re-searched by full TLS (the fallback). (v2 used the same TLS engine on a narrow grid for Arm B's confirmation; that realization is non-executable — DR-002 Finding B.)

| | **Arm A — Baseline** | **Arm B — TRINETRA-X (evidence-first)** |
|---|---|---|
| Preprocess | per-sector detrend + masking (shared) | same |
| Detect | — | simple untrained local detector → events |
| Route | always full search | evidence ≥ θ → fast path; else → fallback |
| Period | full TLS grid | seed from event spacing (+ equivalence-gated cheap period-FAP, §A.8) |
| **Confirm (arbiter)** | **TLS, SDE ≥ T** | **epoch-fixed folded-photometry transit likelihood-ratio $\Lambda$ at $(\hat P, \hat t_0)$, $\Lambda \ge T_{\rm red}$** (fallback = full TLS, SDE ≥ T) |
| Decision threshold | TLS SDE threshold $T$, set to a target FAR on CALIBRATION | confirmer threshold $T_{\rm red}$, set to the **same** target FAR on CALIBRATION (A.2, A.11) |

The **fairness keystone (v3, assumption A6)** is that **both arms are held to a common false-alarm rate** — Arm A via TLS SDE $\ge T$, Arm B via $\Lambda \ge T_{\rm red}$, with $T$ and $T_{\rm red}$ each calibrated to the same target FAR (≤ 1 %/star) on null calibration stars. This compares at equal precision, so any recall difference reflects routing/seeding **and** the intrinsic power gap between the two confirmation statistics (the **attribution caveat**, below), the latter bounded by the full-TLS fallback. The compute difference remains transparent (cheap confirmer + equivalence-gated period-FAP vs full grid). *(v2 keystone was the stronger "same TLS engine + same SDE threshold $T$ both arms"; Finding B proved that realization internally inconsistent — see DR-002 §3.)*

**Attribution caveat (v3).** Relaxing A6 from "same engine" to "common FAR" means an E1/E2 difference now also reflects the power gap between the $\Lambda$ confirmer and TLS, not routing alone. This is mitigated by the full-TLS fallback — a routed star failing the cheap gate is still searched at full power — and is reported, not hidden (DR-002 §3).

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
- **(iii) Significance.** the arm clears its calibrated significance gate at the **common false-alarm rate** (v3 keystone, §2): **Arm A** (and any fallback) — TLS SDE $\ge T$ (Appendix A.2); **Arm B fast path** — confirmer $\Lambda \ge T_{\rm red}$ (Appendix A.11), $T_{\rm red}$ calibrated to the same FAR as $T$. *(v2 used a single common TLS-SDE threshold for both arms; amended per DR-002 Finding B.)*

Completeness $R$ is the fraction of injected planets recovered, computed per $(P, R_p)$ cell and aggregated via the F6 primary estimand (§4.2/§5). The period (i) and epoch (ii) clauses apply identically to both arms; the significance clause (iii) is arm-specific but holds both arms to the **same false-alarm rate**, which is what the v3 fairness keystone (§2) preserves.

**4.2 Transit-preservation requirement (required pre-M3 check).** Before thresholds are frozen, measure conditioning-induced transit attenuation: inject Mandel–Agol transits at the grid parameters, apply Stage-0 conditioning, and compare recovered depth $\hat\delta_{\rm post}$ to injected $\delta_{\rm true}$. Report the median depth-attenuation factor $\eta = \hat\delta_{\rm post}/\delta_{\rm true}$ and a shape-distortion diagnostic per $(P, R_p)$ cell; **require median $\eta \ge \eta_{\min} = 0.90$** (Appendix A.9). Because conditioning precedes detection in both arms, $\eta$ cancels in the paired $\Delta R$ comparison but bounds absolute recall — it is reported, not hidden. If $\eta < \eta_{\min}$ in a cell, the conditioning configuration is revised **before** any threshold is set (never after the test).

**Primary**
- **E1 — recall non-inferiority (primary).** The F6 **occurrence-weighted marginal completeness difference** $\overline{\Delta R} = \sum_{c:N_{\rm tr}\ge2} w_c(R_{\text{comb},c} - R_{\text{TLS},c})$ on the TEST injection set, with weights $w_c$ frozen in Appendix A.5. **Pass** iff the lower bound of the one-sided 95 % CI on $\overline{\Delta R}$ is **> −2 pp**. Per-cell $\Delta R_c$ reported as secondary (Holm-corrected if screened; never gating). Recovery per §4.1; cells with **n_transits ≥ 2**.
- **E2 — compute, fast-path-eligible (primary).** Compute ratio (combined / full-TLS) on the **fast-path-eligible population** (§2), on identical hardware, **including detector overhead $\rho_d$**. Pass if reduction **≥ 30 %** at non-inferior recall (E1). Report $\rho_d$ and the per-stage ledger.
- **E3 — compute, survey-representative (secondary, descriptive).** On the survey-representative sample (§3), report $C_{\rm comb}/C_{\rm full}$ as a function of $\pi$ and the break-even $\pi^\star = \rho_d/f_p$. **Not** pass/fail; expected ≈ 0 or negative at TESS-realistic $\hat\pi$ (this is the pre-registered survey-scale limitation, not a failure).

**Secondary (descriptive, reported, not pass/fail)**
- Routing fraction (% to fast path) and **fast-path-conditional recall**.
- **Recall–compute frontier** as a function of routing threshold θ — computed on the **CALIBRATION set only** (showing it on test would be tuning).
- Recovered-parameter accuracy for P, depth, duration, with **interval coverage** (do 1σ intervals contain truth ~68%?).
- **Calibration** of the period-FAP / gate significance: ECE + reliability diagram. The FAP null uses the **frozen block-bootstrap scheme** (MATH §9.1, Appendix A.8) as the reference; the v3 cheap estimator (§A.8a) is held to it under the numerical-equivalence gate. Calibration is verified on null stars (empirical FAR $\le \alpha_{\rm FAP}$, H4). The confirmer threshold $T_{\rm red}$ is likewise calibrated to FAR ≤ 1 %/star on null stars (A.11).
- **Monotransit sub-analysis** (n_transits = 1): reported separately as a known evidence-first advantage region — excluded from the headline because full TLS also cannot fold single events (an unfair cell for the baseline). Monotransit candidates are confirmed by the **single-event vetting criterion** (MATH §6; routing threshold $z_{\rm mono}$, Appendix A.3), with explicitly **weaker FP control** noted; monotransit FP rate on null stars is reported.
- Real-label check: recall on confirmed TOIs; FP-rejection rate on known FPs.

**Compute accounting.** Single-thread **CPU-core-seconds** per star on the fixed machine of Appendix A (median over ≥ 5 repeats, warm cache; full distribution reported, not just the mean). Phase I uses a **CPU** detector, so the comparison is clean CPU-vs-CPU (no GPU-vs-CPU confound). Arm B cost = detector + **equivalence-gated cheap period-FAP** (together $\rho_d$, charged on every routed star) + confirmer ($\Lambda$ at the seeded ephemeris) + full-TLS fallback where the cheap gate does not confirm; Arm A cost = full TLS. *(v3: $\rho_d$'s period-FAP term is the cheap estimator of §A.8, not the $B=1000$ live bootstrap — this is the term whose sealed-v2 cost drove the dry-run E2 shortfall; see DR-002 §1.)* **Shared Stage-0 conditioning is excluded** (or charged equally to both arms) so the comparison isolates search cost. The fast-path-eligible aggregate (E2) and the prevalence-weighted aggregate (E3) are both reported, derived from the identical per-star ledger.

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
- **v3 is the final permissible amendment (§7a).** Both v3 amendments are forced by a pre-TEST defect (Finding B) or admitted only under a numerical-equivalence gate (§A.8a); no further protocol change is permitted before the single TEST run.

---

## 7a. AMENDMENT POLICY & STOPPING RULE (v3; authority DR-002)

> Policy governing protocol amendments. Adopted 2026-06-19 on CALIBRATION evidence, TEST unread. Distinguishes a legitimate *amendment* (a pre-TEST defect fix) from forbidden *tuning* (any change motivated by a measured outcome). This is what keeps v3 a single committed, falsifiable test rather than the first step of amendment creep.

**Amendment vs. tuning.** An *amendment* corrects a logical/implementation defect discovered **before** the TEST read (e.g. Finding B). *Tuning* is any design change motivated by a measured outcome — on TEST **or** CALIBRATION — and is prohibited (non-negotiable #2).

- **P-1.** Only amendments are permitted; tuning is prohibited.
- **P-2.** **v3 is the terminal amendment.** On sealing v3 (Seal #2b), the protocol is frozen.
- **P-3.** Design-by-theory, threshold-by-calibration: v3's confirmation statistic is fixed from first principles (MATH §6) *before* its calibration performance is examined; calibration may only set a threshold to a pre-stated FAR, never select among statistic variants by performance.
- **P-4.** Pre-committed outcomes (below) are sealed before the TEST read; none of them is "amend."
- **P-5.** One evaluation: TEST is read exactly once, against sealed v3.
- **P-6.** Failure is a result: a TEST failure → the pre-committed falsification, reported with equal rigor; it does **not** authorize a v4.
- **P-7.** Narrow defect exception (high bar): only a *new Finding-B-class provable inconsistency* found during v3 calibration can force a stop + explicit owner decision; a performance shortfall never qualifies; a *second* such defect = a feasibility negative result.
- **P-8.** New ideas → new, separately pre-registered experiments (the deferred Lever 1a, multi-period harmonic testing, and the clean-skip tier live here — never as retroactive improvements to this Phase-I result).
- **P-9.** Amendment ledger (below) records every version + justification + seal hash; the count is kept visible.

**Pre-committed TEST-outcome mapping (sealed before TEST; consistent with §5).**
- **E1 fail** — one-sided 95 % lower bound on $\overline{\Delta R} < -2$ pp → recall falsification → **H1 FALSIFIED**; successful negative Phase I; do not proceed to Phase II on the routing-recall claim.
- **E2 fail** — compute reduction < 30 % at non-inferior recall → compute falsification → **H1 FALSIFIED (compute branch)**. A near-zero survey-representative figure (E3) is expected by construction and is **not** a failure.
- **Inconclusive** — CI wider than the margin → **not a pass**; the only permitted response is the pre-planned injection-count increase (§6), truth and thresholds unchanged — not an amendment.

**Amendment ledger (P-9).**

| Version | Date | Justification | Pre-data status | Seal |
|---|---|---|---|---|
| v1 | 2026-06-14 | Initial Phase I pre-registration | pre-data | (superseded) |
| v2 | 2026-06-15 | F1 compute scope (DR-001) + R-4…R-7, one re-registration | pre-data | tag `phase1-prereg-v2`; M3 thresholds Seal #2 `6292c018…` |
| **v3** | **2026-06-19** | Finding B (forced defect) + Option-2 confirmer (A6 → common-FAR) + Lever 1b period-FAP (equivalence-gated) | **pre-TEST (CALIBRATION-only)** | **Seal #2b — pending** |

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

**A.1 TLS baseline (Arm A and the Arm-B fallback).**
- Implementation: `transitleastsquares` (Hippke & Heller 2019); record exact version.
- Period sampling: optimal/Ofir (2014) over $[P_{\min}, P_{\max}]$ matched to the injection grid; record oversampling factor.
- Duration grid: default; limb-darkening from TIC stellar parameters.
- This full-grid TLS is **Arm A's detector and Arm B's full-TLS fallback**. *(v3: Arm B's fast-path confirmation is no longer targeted TLS — Finding B — but the folded-photometry transit-LR confirmer of A.11. The full-grid TLS configuration here is unchanged.)*

**A.2 Arm-A significance threshold $T$.** TLS SDE threshold set so the empirical false-alarm rate on **null (planetless) calibration stars** equals a pre-registered $\alpha$ (target **FAR ≤ 1 % per star**). Used by **Arm A and the Arm-B full-TLS fallback**. Value: $T = 10.74$ (sealed at M3, Seal #2; **unchanged in v3**). *(v3: Arm B's fast-path confirmer uses its own threshold $T_{\rm red}$, A.11, calibrated to the **same** FAR — this is the v3 "common false-alarm rate" keystone, §2, replacing the v2 "single common $T$ both arms".)*

**A.3 Detector threshold & routing ($z_\star$, θ).** $z_\star$ set on the calibration set to a target local false-event yield (**≤ 1 expected false event per null light curve**). Routing rule: multi-event fast path iff $\ge N_{\min}$ events with $N_{\min} = 2$; monotransit branch iff a single event has $\mathrm{SNR}_1 \ge z_{\rm mono}$ for a stated $z_{\rm mono} > z_\star$. Values: `[sealed at M3]`.

**A.4 Recovery predicate.** As §4.1 (period 1 % / harmonics $m\in\{2,3\}$ flagged; epoch $\pm 0.5\,T_{14}$; significance per §4.1(iii) — Arm A / fallback: SDE ≥ $T$; Arm B fast path: $\Lambda \ge T_{\rm red}$, both at the common FAR).

**A.5 F6 occurrence weight prior $w_c$ (FROZEN).** $w_c \propto w_P(P)\,w_R(R_p)$, normalized to $\sum_c w_c = 1$ over eligible cells, where:
- $w_P(P)$ is **log-uniform** over the period nodes {0.5, 1, 2, 4, 8, 16} d restricted to $N_{\rm tr}\ge 2$ cells (equal weight per node in $\log P$).
- $w_R(R_p)$ is the **radius-occurrence weighting from Kunimoto & Matthews (2020)**, evaluated at the grid radii {1, 2, 4, 8, 12} $R_\oplus$ (occurrence integrated over each radius node's bin).
This is the sole pre-registered weighting and is not revisited post-hoc.

**A.6 Survey-representative prevalence $\hat\pi$ (FROZEN).** $\hat\pi = $ (TESS planet occurrence) × (geometric transit probability), where the occurrence term is integrated over the injection grid's $(P, R_p)$ support using the **same Kunimoto & Matthews (2020) occurrence framework as A.5**, and the geometric term is $\langle R_\star/a\rangle$ for the target sample. The single frozen scalar $\hat\pi$ and its integration bounds are recorded here before any data; used only for E3 (reported as a curve over $\pi$ in addition to the point at $\hat\pi$).

**A.7 Runtime protocol.** One specified machine (record CPU model, cores, clock); single-thread **CPU-core-seconds**; median over ≥ 5 repeats; warm cache; report the full distribution. Shared Stage-0 conditioning excluded (or charged equally to both arms). Detector overhead $\rho_d$ measured and reported separately.

**A.8 Period-FAP reference scheme (frozen).** Noise-model-aware **circular block bootstrap** (MATH §9.1). Block length $L_b = 3\times\max(\tau_{\rm GP},\,T_{14})$, where the GP correlation timescale $\tau_{\rm GP}$ is measured per target during conditioning (calibration-derived, like other thresholds); $B \ge 1000$ surrogates over the identical period grid; FAP cutoff $\alpha_{\rm FAP}$ (sealed at M3, Seal #2; **unchanged in v3**) set to a target null exceedance. Calibration verified on null stars (H4). **In v3 this $B=1000$ bootstrap is the reference (ground-truth) estimator** against which the operational cheap estimator (A.8a) is validated, and the **fallback** if the equivalence gate fails.

**A.8a Operational period-FAP estimator (v3; equivalence-gated).** The operational pipeline replaces the live $B=1000$ bootstrap with a **cheaper estimator** of the **same** FAP quantity at the **same** $\alpha_{\rm FAP}$ — per-star **EVT / GPD tail-fit** preferred (preserves each star's red-noise structure), or a precomputed red-noise null grid keyed on (baseline, event count, noise level) with interpolation. **Admissibility (numerical-equivalence gate, validated on CALIBRATION only — full protocol in the Lever-1b equivalence-validation plan):** the estimator is admitted into v3 iff, on the cleaned null pool, **(i)** its FAP matches the A.8 bootstrap FAP within a pre-stated tolerance, **(ii)** it does not change which routed stars pass/fail the $\alpha_{\rm FAP}$ gate beyond that tolerance, and **(iii)** on injections it is recall-safe (clips no recoverable planet the bootstrap keeps). **Fallback:** if any condition fails, A.8a is dropped and v3 reverts to the A.8 bootstrap ("confirmer-only v3"); the resulting compute outcome is reported as-is (DR-002 §2.3a). The estimator choice and its validated tolerance are recorded into the v3 manifest and hashed (Seal #2b).

**A.9 Conditioning & transit preservation (frozen).** Stage-0 per-sector detrend (GP/biweight kernel and window frozen here; record exact `wotan`/`celerite2` parameters); momentum-dump (~2.5 d) and scattered-light/quality masking. Transit-preservation tolerance: median depth-attenuation factor $\eta = \hat\delta_{\rm post}/\delta_{\rm true} \ge \eta_{\min} = 0.90$ per eligible cell (measured per §4.2 before thresholds are frozen).

**A.10 Manifest hash.** The v2 freeze hashed all `[sealed at M3]` values + Appendix A.1–A.9 (Seal #2, `6292c018…`). **v3 (Seal #2b):** the reissued VAL v3 / MATH v1.2 are content-hashed, and the v3-specific calibration outputs — the admitted A.8a estimator + its validated tolerance, and $T_{\rm red}$ (A.11) — are hashed into the v3 threshold manifest, recorded **before** M4. Sealed v2 thresholds carry over unchanged. Exactly one sealed-TEST evaluation follows the seal.

**A.11 Fast-path confirmer & threshold $T_{\rm red}$ (v3; frozen by theory, threshold by calibration).** Arm B's fast-path confirmation is an **epoch-fixed folded-photometry transit likelihood-ratio** at the seeded ephemeris $(\hat P, \hat t_0)$: fold the conditioned light curve at $\hat P$, fit a **physical transit template** (Mandel–Agol / limb-darkened; trapezoid permitted as its degenerate form) against a flat-baseline null, and form $\Lambda$ (equivalently $\Delta\mathrm{BIC}$ or the transit-fit S/N) — **sign-aware** (dimming only) and **shape-consistent** (transit template, not a box). Look-elsewhere is handled by the period-FAP (A.8/A.8a) gating entry to the confirmer. The statistic form is fixed from first principles (MATH §6) **before** examining its calibration performance (stopping rule P-3); the box depth-SNR used in the M4 dry-run is **not** admissible (DR-002 §2.2). **Threshold $T_{\rm red}$** is set so the empirical FAR on **null calibration stars** equals the same target as $T$ (**≤ 1 %/star**) — the common-FAR keystone (§2). Calibration procedure: the **T_red calibration plan** (full cleaned null pool). Value: `[sealed at #2b]`.

---

*Pre-registration only — no code, no results. Implementation begins with the shared Stage-0 conditioning and the CALIBRATION-set threshold-fixing, on one frozen set of TESS sectors.*
