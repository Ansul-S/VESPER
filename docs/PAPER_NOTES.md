# PAPER NOTES — TRINETRA-X

| Field | Value |
|-------|-------|
| **Document** | Publication notebook (living) |
| **Version** | 1.0 |
| **Purpose** | Transform future TRINETRA-X results into a peer-reviewed paper |
| **Project** | [`TRINETRA-X.md`](./TRINETRA-X.md) |
| **Companions** | [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) · [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) · [`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md) · [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) |

> A working notebook, not a manuscript. It accumulates the framing, figures, tables, and rebuttals that a publication will need, so that when results exist they can be written up quickly and defensibly. **Honesty clause:** a negative Phase I result is publishable and is planned for here on equal footing with a positive one ([`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md), §9).

---

## 1. Target Venues

| Tier | Venue | Fit |
|------|-------|-----|
| Primary (methods) | *The Astronomical Journal* (AJ) / *MNRAS* | Transit-detection methodology + TESS application |
| Primary (alt) | *PASP* | Instrumentation/algorithms emphasis |
| ML cross-over | *NeurIPS/ICML* ML4Science, or *RAS Techniques & Instruments* | If the learned detector (Phase II) is the headline |
| Preprint | arXiv `astro-ph.EP` + `astro-ph.IM` | On submission |

Most likely first paper: a **methods + validation** paper in AJ/MNRAS reporting the Phase I result.

---

## 2. Candidate Paper Titles

**Phase I (validation) paper — front-runners:**
1. *TRINETRA-X: Evidence-First Triage for Scalable Transit Detection in TESS Light Curves*
2. *Detect Before You Search: Recall-Preserving Computational Triage for Exoplanet Transit Surveys*
3. *Spend Computation Where the Evidence Is: A Non-Inferiority Test of Evidence-First Transit Detection on TESS*

**Mechanism-forward alternatives:**
4. *From Events to Orbits: Period Recovery by Calibrated Voting and Photometric Confirmation*
5. *When Is a Period Search Unnecessary? Single-Transit Detectability and the Compute–Recall Frontier in TESS*

**If negative result:**
6. *The Limits of Evidence-First Transit Detection: A Pre-Registered Null Result on TESS*

*(Working favourite: #1 for a positive result, #6 for a null.)*

---

## 3. Potential Abstracts

### 3a. Positive-result abstract (draft)
> Transit surveys fold every light curve at thousands of trial periods, an exhaustive search whose cost scales poorly to the $\sim10^5$–$10^6$ stars of missions like TESS. We test, in a pre-registered experiment, whether detection cost can be reduced by **routing on evidence**: detecting individual transit-like events directly, inferring the period from their spacing, confirming with a physics-based transit fit, and reserving a full Transit Least Squares (TLS) search only for stars lacking local evidence. Using injection–recovery into real TESS light curves — preserving genuine correlated noise — and an identical TLS engine in both arms, we find that evidence-first routing reduces total compute by [X]% while remaining recall non-inferior to full TLS within a 2-percentage-point margin (recall difference [Δ ± CI]). The advantage is concentrated, as predicted, on the high single-transit-SNR (large-planet) population and on single-transit (monotransit) events that a periodogram cannot fold. Crucially, detection is adjudicated by calibrated photometric significance rather than timing coincidence, and every significance statistic is validated against a bootstrap null. We discuss the compute–recall frontier and its extrapolation to full-survey scale.

### 3b. Null-result abstract (draft)
> We report a pre-registered test of evidence-first transit detection on TESS and find that, under realistic correlated noise, [it fails to preserve recall within the 2-pp margin / the routing fraction is too small to yield meaningful compute savings]. We trace the outcome to [seed-accuracy collapse under red noise / low single-transit detectability of the TESS planet population], quantify the boundary at which the approach would become viable, and release the benchmark to support future work.

---

## 4. Novel Contributions (claims the paper will defend)

1. **A pre-registered non-inferiority framework for detection algorithms.** Importing clinical-trial non-inferiority logic to transit search; recall as the protected endpoint, compute as the superiority endpoint ([`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md), §6).
2. **The compute–recall master equation.** Closed-form $\Delta R=-f(1-r_{\rm seed}g)$ and saving $\approx f$, reducing the entire claim to one testable inequality ([`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md), §8).
3. **Calibrated period recovery.** A bootstrap, look-elsewhere-correct false-alarm probability for sparse-event period inference — the rigorous replacement for uncalibrated coherence scores (§9).
4. **Photometric-significance gating.** Demonstrating that making the folded-transit likelihood ratio the arbiter (not timing coincidence) is what makes evidence-first detection sound — with an explicit before/after against the prior design's failure modes (§10–§11).
5. **A fair, leakage-safe benchmark** of evidence-first routing vs. full TLS on identical real-noise data with an identical detection engine (the fairness keystone).
6. *(Phase II+)* A learned, self-supervised single-transit detector and ExoMiner-style classifier with conformal confidence — if it materially raises $f$ or $r_{\rm seed}$.

---

## 5. Key Figures to Generate

| # | Figure | Purpose / claim it supports |
|---|--------|------------------------------|
| F1 | **Single-transit SNR distribution** of the TESS planet population, with the $z_\star$ threshold and critical radius $R_{p,\rm crit}$ | Establishes the bimodality (A1); motivates triage |
| F2 | **Architecture / data-flow schematic** (Stages 0–3 for Phase I) | Orients the reader; mirrors [`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md) |
| F3 | **Completeness maps** $(P, R_p)$ for full-TLS vs. combined system, plus their difference $\Delta R$ | The H1a result — the headline |
| F4 | **Compute–recall frontier**: saving vs. recall loss as the routing threshold varies (calibration set) | Visualizes the master equation; shows the operating point |
| F5 | **Recovered-vs-true parameter** scatter + residuals for $P$, depth, $T_{14}$, with interval-coverage inset | H5 (parameter recovery / calibration) |
| F6 | **Bootstrap-FAP calibration**: empirical vs. nominal false-alarm rate on null stars; reliability diagram | H4 (calibration); rebuts "uncalibrated like v3" |
| F7 | **Monotransit case studies / recovery rate** vs. TLS in the $N_{\rm tr}=1$ regime | H3 (TESS-specific advantage) |
| F8 | **Throughput / runtime per star** distribution, both arms, same hardware | H1b (compute) |
| F9 *(optional)* | **Before/after on a v3 failure star**: timing-coherence "detection" vs. photometric-gate rejection | Dramatizes contribution #4 |

---

## 6. Required Benchmark Tables

| # | Table | Contents |
|---|-------|----------|
| T1 | **Dataset manifest** | Sectors, target counts, calibration/test split, injection grid $(P, R_p, b)$, $N$ per cell, RNG seed |
| T2 | **Headline result** | $R_{\rm TLS}$, $R_{\rm comb}$, $\Delta R$ with CI; $C_{\rm comb}/C_{\rm TLS}$; routing fraction $f$ — pass/fail vs. pre-registered criteria |
| T3 | **Recall by population** | Completeness split by planet class (Jupiter/Neptune/sub-Neptune/Earth) and by $N_{\rm tr}$ — locates where parity holds/breaks (H2) |
| T4 | **Calibration metrics** | Bootstrap-FAP coverage, gate-significance ECE, conformal coverage (where applicable) |
| T5 | **Parameter accuracy** | Median fractional error and interval coverage for $P$, depth, $T_{14}$ |
| T6 | **Reality-check** | Recall on confirmed TOIs; false-positive rejection rate on known EBs/BEBs/variables |
| T7 | **Compute ledger** | Per-stage time, fast-path vs. fallback counts, total CPU-core-seconds per arm |
| T8 *(method)* | **Ablation** | Effect of removing the photometric gate / using uncalibrated score — quantifies contributions #3–#4 |

---

## 7. Anticipated Reviewer Concerns (and prepared responses)

| # | Likely objection | Prepared response |
|---|------------------|-------------------|
| R1 | "This is just a single-transit / monotransit search — not novel." | We claim novelty in the *recall-preserving triage synthesis* and the *pre-registered non-inferiority test*, not in single-transit detection per se ([`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §D). We cite and position against monotransit literature explicitly. |
| R2 | "How is this different from BLS/TLS prefilters or known triage?" | Both arms use the *same* TLS engine/threshold; the only variable is evidence-routing. The benchmark isolates the routing contribution by construction (§2 of [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md)). |
| R3 | "Your false positives are noise artifacts" (the v3 critique). | Detection is gated on **calibrated photometric significance**, with a bootstrap-FAP null (F6, §9 of math doc). We show the explicit ablation (T8, F9) of what the gate prevents. |
| R4 | "Injection recovery overstates real performance." | Injections are into **real** light curves (real $\Sigma$); we cross-validate against confirmed TOIs at matched parameters (T6, A3). |
| R5 | "Red noise / systematics will break the local detector." | Red-noise-aware (GP-whitened) statistic; per-sector conditioning; calibration measured on null stars (F6). We report where it breaks rather than hiding it. |
| R6 | "Compute comparison is unfair (GPU vs CPU, tuned thresholds)." | Phase I uses a CPU detector (clean CPU-vs-CPU); thresholds frozen on a disjoint calibration set; one sealed-test evaluation (anti-tuning safeguards, §7 of validation doc). |
| R7 | "Recall margin of 2% is arbitrary / too lenient." | Pre-registered, justified, and reported with full per-cell CIs so readers can apply their own margin; superiority not claimed. |
| R8 | "Generalization beyond the chosen sectors." | Splits are leakage-safe by sky region; we discuss extrapolation and release the benchmark for replication. |

---

## 8. Experimental Milestones (paper-bearing)

| Milestone | Produces | Figures/Tables |
|-----------|----------|----------------|
| M0 — Frozen manifest + splits | Reproducible dataset | T1 |
| M1 — Detectability census | TESS $\mathrm{SNR}_1$ distribution | F1 |
| M2 — Conditioning + injection campaign | Real-noise injection set | T1 |
| M3 — Threshold calibration (calibration set) | Frozen $z_\star, \theta, T, \alpha$; frontier | F4, F6 |
| M4 — Sealed-test evaluation (single run) | Headline recall + compute | F3, F8, T2, T3, T7 |
| M5 — Parameter + calibration analysis | Posterior coverage | F5, T4, T5 |
| M6 — Reality check + ablation | TOI/EB performance; gate ablation | F7, F9, T6, T8 |
| **M7 — Write-up** | Phase I manuscript | all |

(Phase II–IV milestones — learned detector, classifier, habitability — feed subsequent papers; see [`TRINETRA-X.md`](./TRINETRA-X.md), Milestones.)

---

## 9. Publication Roadmap

```
Paper I  (Phase I)   "Evidence-First Triage for TESS"            ← validation / methods   [next]
   │   gated on: H1 pass OR a clean, well-characterized null
   ▼
Paper II (Phase II)  "A Self-Supervised Single-Transit Detector" ← if learned detector raises f / r_seed
   │
   ▼
Paper III(Phase III) "Calibrated Astrophysical Vetting w/ Conformal Confidence"  ← classifier + FP rejection
   │
   ▼
Paper IV (Phase IV)  "TRINETRA-X: A Scalable Evidence-First Pipeline & Candidate Catalog"  ← full system + any new candidates
```

**Sequencing principle:** publish the *validated unit* at each phase; never bundle an unvalidated stage into a results claim (the v3 lesson — an open confirmation loop must never be reported as detection).

---

## 10. Reproducibility & Open-Science Commitments

- Pre-registration (`SCIENTIFIC_HYPOTHESIS.md` + `TRINETRA_X_PHASE1_VALIDATION.md`) timestamped before results; cited in the paper.
- Release: frozen manifest, injection grid, seeds, calibrated thresholds, and evaluation code; benchmark made public for replication (addresses R8).
- Every numerical claim traceable to a table; every table to a milestone; every figure to a frozen dataset.
- Negative results reported with the same rigor as positive ones.

---

## 11. Open Writing Questions (to resolve as results arrive)

- Headline framing: lead with **compute saving** (systems audience) or **recall preservation** (astro audience)? — likely recall-first for AJ/MNRAS.
- Whether to fold Phase II's learned detector into Paper I if Phase I passes quickly, or keep the simple-detector validation clean and separate (current lean: **keep separate** — preserves attribution of the routing principle).
- Author/affiliation line (charter author: *Vesper*); acknowledge ISRO exoplanet-challenge context.
- Exact citation set: TLS (Hippke & Heller), BLS (Kovács et al.), AstroNet (Shallue & Vanderburg), ExoMiner (Valizadegan et al.), TESS mission + SPOC/QLP, monotransit searches, conformal prediction.

---

## 12. Empirical Findings Log (as milestones complete)

> Results recorded as milestones run, to feed the manuscript. **Each entry is a dataset-scoped *validation* result, not a final scientific conclusion.** Keep figure/table indices stable (§5–§6).

### EF-1 — Detectability bimodality (M2 injection-recovery; 2026-06-16)

**Finding.** Injection-recovery validation demonstrates a detectability bimodality in TESS 2-minute data: conditioning preserves transit depth (η ≥ 0.90) across the individually measurable population (Rₚ ≥ 2 R⊕ under the finalized 2.5 d detrending window), while the Earth-radius regime is dominated by single-transit noise limitations and is not recoverable through conditioning alone. Recovery of that regime is expected to depend on phase-folding and population-level signal accumulation rather than single-transit preservation.

**Scope / caveats (do not overstate).** This is an **M2 transit-preservation validation result on the S1–S3 southern calibration sample at the finalized 2.5 d biweight window** — *not* a universal statement about all TESS Earth-sized planets. The Rₚ=1 η medians are noise-dominated (depth ~70–85 ppm, single-transit SNR₁ ~0.07–0.08; broad, non-physical η with negative lower quartiles); the boundary depends on stellar noise (σ), sector baseline, and the detrending configuration. The 0.5/2 cell is a documented low-SNR borderline (η = 0.892).

**Connects to.** F1 (single-transit SNR bimodality), the §1 rationale / HYP A1, and the fallback's role (small planets recovered by folding, not single-transit conditioning). Source: `data/manifests/m2/m2_eta_table.csv`; `PHASE1_M2_PLAN.md` §3b. Candidate figure: η map over $(P, R_p)$ as a supplement to F1.

---

*Living document v1.0. Update as milestones complete; keep figure/table indices stable so drafts can reference them early.*
