# REPOSITORY GAP ANALYSIS — TRINETRA-X

| Field | Value |
|-------|-------|
| **Document** | Critical cross-document review |
| **Version** | 1.0 |
| **Reviewer stance** | Adversarial internal referee — find what is wrong, missing, or unprovable |
| **Scope** | All repository documents (see §0) |
| **Date** | 2026-06-15 |

> This is a deliberately critical audit of the TRINETRA-X document set, written before Phase I executes so that defects are cheap to fix. It hunts for contradictions, missing assumptions, undefined terms, missing benchmark requirements, and reviewer-facing weaknesses. Findings are severity-ranked and cross-referenced. Nothing here changes the science; it identifies where the science is not yet pinned down.

---

## 0. Documents Reviewed

| Path | Lines | Role |
|------|-------|------|
| `docs/TRINETRA-X.md` | 340 | Master charter (author: Vesper) |
| `docs/TRINETRA_CONCEPT_RECONSTRUCTION.md` | 154 | Concept lineage / v3 post-mortem |
| `docs/TRINETRA_X_ARCHITECTURE.md` | 196 | 7-stage system design |
| `docs/TRINETRA_X_PHASE1_VALIDATION.md` | 122 | Pre-registered Phase I protocol |
| `docs/SCIENTIFIC_HYPOTHESIS.md` | 146 | Formal hypotheses |
| `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` | 255 | Canonical theory |
| `docs/PAPER_NOTES.md` | 167 | Publication notebook |
| `archive/PROJECT_AUDIT.md`, `archive/TRACK_B_SCIENTIFIC_REVIEW.md` | — | Historical (Revival-era) |
| `TRINETRA-X.md`, `README.md`, `CLAUDE.md` (root) | 0 | **Empty** |

---

## SEVERITY-RANKED SUMMARY (read this first)

| ID | Finding | Severity | Category |
|----|---------|----------|----------|
| **F1** | Compute saving is defined on a planet-enriched injection sample; at survey scale the planetless majority makes the fast path *overhead*, not saving | **Critical** | Contradiction / Assumption / Benchmark |
| **F2** | Recovery ("recall") success predicate is never operationally defined | **Critical** | Definition |
| **F3** | Period recovery assumes strict periodicity, contradicting the advertised TTV/exomoon "model-agnostic" advantage | **High** | Contradiction / Assumption |
| **F4** | Multi-planet systems break event-spacing period recovery — unaddressed | **High** | Assumption / Benchmark |
| **F5** | Monotransit (N_tr=1) claim collides with the "repeatability is required" gate — a lone event cannot be period-confirmed | **High** | Contradiction / Reviewer |
| **F6** | Multiple-testing across completeness cells has no correction or pre-specified aggregate endpoint | **High** | Benchmark / Definition |
| **F7** | The full system is branded "AI" and Stage-1 is a learned detector, but Phase I uses a simple untrained detector — reconciled in two docs, not in the charter | **Medium** | Contradiction |
| **F8** | Routing rule (z⋆, θ, N_min, "strong") and TLS baseline config are not numerically pinned | **Medium** | Definition / Benchmark |
| **F9** | "vs BLS/TLS" is claimed in title/charter, but only TLS is benchmarked in Phase I | **Medium** | Benchmark |
| **F10** | Bootstrap-FAP exchangeability under red noise is flagged but no resampling scheme is committed | **Medium** | Assumption |
| **F11** | Detrending-induced transit distortion and transit-preservation are not stated/quantified | **Medium** | Assumption / Benchmark |
| **F12** | Repo hygiene: empty root `TRINETRA-X.md` duplicate, empty `README.md`/`CLAUDE.md`, no bibliography, no data-version pinning | **Low** | Hygiene |

---

## 1. CONTRADICTIONS

**F1 — Compute saving: enriched sample vs. survey reality. [Critical]**
`SCIENTIFIC_HYPOTHESIS.md` H1b and `TRINETRA_X_PHASE1_VALIDATION.md` §4 require ≥30 % *total* compute reduction. `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §8.3 derives saving ≈ *f* (fast-path routing fraction). But the primary truth is **injection into real light curves** — i.e. every test star carries a planet. On a planet-bearing star with strong evidence, the fast path saves. On a **planetless** star (the ~99 % of a real survey), the cheap detector finds no events → routes to the full-TLS fallback → cost = detector + full TLS > full TLS. **The fast path is net overhead on the planetless majority.** Therefore: (a) compute measured on the all-injected sample *overstates* survey-scale saving; (b) to save compute on planetless stars you must *skip* full TLS on "no-evidence" stars — but that is exactly where small planets hide, so it trades recall (the v3 "Q4 CDPP-skip" idea, **absent** from Phase I). As written, H1b is only attainable/measurable on a planet-enriched population, and no document states this scoping. *Fix:* explicitly define the compute-measurement population; report compute on both a planet-enriched and a survey-representative sample; either scope H1b to "fast-path-eligible population" or add a calibrated clean-skip tier and fold its recall cost into the non-inferiority test.

**F3 — Strict periodicity vs. model-agnostic generality. [High]**
`TRINETRA_CONCEPT_RECONSTRUCTION.md` §D (Innovation 5) and the charter's spirit advertise catching TTVs, exomoons, and non-box signals "that BLS/TLS reject by construction." But `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §4 recovers the period from *integer-multiple spacing* — which **assumes constant P**. Significant TTVs smear the phase concentration and defeat the very recovery step. The advertised advantage and the implemented method point in opposite directions. *Fix:* state the strict-periodicity assumption explicitly, scope the "model-agnostic" claim to the *event-detection* stage only (not period recovery), and note TTV tolerance as a bounded quantity to be measured, not an unqualified advantage.

**F5 — Monotransit advantage vs. "repeatability required." [High]**
`SCIENTIFIC_HYPOTHESIS.md` H3 and `TRINETRA_X_ARCHITECTURE.md` champion monotransit (N_tr=1) recovery as a TESS strength. But Principle 2 (`TRINETRA-X.md`) and the gate (`TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §6) require **repeatability** as a confirmation criterion. A single event has no repetition; the photometric gate can confirm a transit *shape* but not periodicity, and cannot distinguish a lone transit from a flare/systematic by repetition. The two claims are in tension. *Fix:* define a separate monotransit confirmation criterion (shape + ingress/egress + secondary-eclipse + centroid, explicitly *without* repetition) and state that monotransit FP control is weaker by construction.

**F7 — "AI framework" / learned detector vs. untrained Phase I. [Medium]**
`TRINETRA-X.md` brands the project an "AI-assisted framework" and Stage 1 lists "1D U-Net, Temporal CNN, self-supervised learning"; `TRINETRA_X_ARCHITECTURE.md` Stage 1 is likewise learned. `SCIENTIFIC_HYPOTHESIS.md` §10 and `TRINETRA_X_PHASE1_VALIDATION.md` §8 correctly state Phase I uses a **simple untrained** detector. The reconciliation exists in two documents but **not in the charter**, so a charter-first reader perceives a contradiction (and may expect the first result to contain AI, when it deliberately contains none). *Fix:* add one line to the charter's Stage 1 noting that Phase I validates the *routing principle* with an untrained detector; the learned detector is Phase II.

**F9 — "BLS/TLS" claimed, only TLS tested. [Medium]** Title/charter and `PAPER_NOTES.md` framing say "standard BLS/TLS pipelines," but Phase I benchmarks **TLS only**. Defensible (TLS dominates BLS) but the claim scope and the experiment scope disagree. *Fix:* either add a BLS arm or narrow the comparative claim to TLS and justify the omission.

*(Minor, non-blocking:* the charter's qualitative "match or exceed TLS recall on large planets" vs. the quantitative 2-pp non-inferiority are compatible but stated in different languages; unify the wording.)*

---

## 2. MISSING ASSUMPTIONS

These are load-bearing premises stated nowhere with a check.

- **F1-assumption — Searched-population composition.** The fraction of searched stars hosting a *detectable* transiting planet, and whether the compute claim is made on a planet-enriched or survey-representative sample. (Drives F1.) **Most important missing assumption.**
- **F4 — Single transiting planet per star. [High]** Event→period→confirm assumes one period. Multi-planet systems interleave events of different periods; phase-coherence/Hough on the mixed set aliases or fails. Kepler/TESS multiplicity is common. No document states the single-planet assumption or a method for multiplicity (iterative event masking).
- **F11 — Transit preservation under detrending.** Conditioning must remove variability *without* attenuating transits. `SCIENTIFIC_HYPOTHESIS.md` A2 asserts stationarity but not transit-preservation; over-aggressive detrending is a known recall sink.
- **Shape/limb-darkening adequacy & impact-parameter range.** The matched-filter template and Mandel–Agol fit assume an approximately box/limb-darkened shape; grazing (high-b, V-shaped) transits violate it. The injection grid uses b≤0.6 — so high-b transits are *neither assumed-out nor tested*.
- **Stellar-variability contaminants.** No population-level assumption about pulsators, fast rotators, and EBs that generate coherent quasi-periodic events (the dominant real false-event source). `A4` covers noise scale, not coherent astrophysical mimics.
- **Exchangeability for the bootstrap null (F10).** `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §9 notes red noise breaks strict exchangeability and "motivates block resampling" but commits to nothing — leaving the FAP's validity assumption open.
- **Stellar-parameter reliability.** SNR₁, duration, and depth→radius all depend on TIC stellar radii/density; their uncertainty propagation is assumed negligible but never stated.

---

## 3. MISSING SCIENTIFIC DEFINITIONS

Terms used as if defined but never pinned. Each blocks reproducibility.

- **F2 — "Recall / completeness / recovery." [Critical]** *What counts as a recovered planet?* Period within a stated tolerance (e.g. |P̂−P|/P < 0.01, harmonics allowed?), correct epoch, gate SDE ≥ T? Used pervasively; defined nowhere. Without this predicate, *no recall number is reproducible.*
- **z⋆, θ, N_min, "strong event."** The detection threshold and routing-rule parameters are symbolic throughout (`TRINETRA_X_PHASE1_VALIDATION.md` §2 lists the rule structure but no values, no target false-alarm rate they are set to on the calibration set).
- **CDPP for TESS.** SNR₁ = δ/CDPP(T₁₄) is foundational, but how CDPP is measured operationally on TESS (rolling RMS at duration scale? GP σ?) is undefined.
- **"Transit significance" T (SDE/Λ).** The gate/baseline threshold and its mapping to a false-alarm rate are symbolic.
- **Non-inferiority decision granularity.** Per-cell vs. aggregate: if 1 of N cells fails, does H1a fail? `SCIENTIFIC_HYPOTHESIS.md` §6 says "overall and per cell" but the *decision rule over cells* is unspecified (see F6).
- **"Compute / total cost" aggregation.** `TRINETRA_X_PHASE1_VALIDATION.md` §4 defines the unit (CPU-core-seconds) but not the aggregation (sum vs. median per star) nor whether the shared conditioning cost is included (it should be excluded or charged equally to both arms).
- **"Candidate" vs. "detection" vs. "planet."** Used interchangeably; needs a controlled vocabulary.

---

## 4. MISSING BENCHMARK REQUIREMENTS

- **F6 — Multiple-comparison control. [High]** Non-inferiority is tested across many (P, Rp) cells; with no correction or pre-specified aggregate primary endpoint, the decision is statistically ill-posed (one can pass overall while failing where it matters, or fail a cell by chance). *Require:* a single pre-registered primary estimand (e.g. marginal completeness over the grid weighted by an occurrence prior) plus cell-level reporting as secondary, with an explicit multiplicity rule.
- **TLS baseline configuration.** Implementation (e.g. `transitleastsquares`), period grid, oversampling, duration grid, and SDE threshold must be pinned and reported — they set both arms' recall and the baseline cost.
- **Hardware & runtime protocol.** "Fixed hardware" must be specified (cores, wall-clock vs. CPU-time, parallelism, warm/cold cache, single-thread normalization). A compute claim is only as credible as this protocol.
- **Power analysis shown.** `TRINETRA_X_PHASE1_VALIDATION.md` §6 asserts ≥500 injections/cell "from a power analysis"; the analysis (assumed baseline recall, α, power, resulting N) must be exhibited.
- **Required ablation.** The gate-on/off and calibrated/uncalibrated-score ablation (`PAPER_NOTES.md` T8) substantiates the *core contribution* (photometric gate, calibrated FAP) and should be a **required** Phase I benchmark, not optional.
- **Null-star false-alarm target.** H4 calibration needs a *quantitative* pass target (e.g. FP rate ≤ α per null star), not only "calibrated."
- **External pipeline benchmark.** Recovery of confirmed TOIs and agreement with SPOC/QLP detections should be a quantified benchmark, not only a "reality check."
- **Data & catalog version pinning.** TESS data-release/sector versions, TIC/TOI/EB catalog versions and access dates must be fixed for reproducibility.
- **BLS arm (see F9).**

---

## 5. POTENTIAL REVIEWER CRITICISMS (new — beyond PAPER_NOTES §7)

`PAPER_NOTES.md` already pre-empts R1–R8. The following are **not yet** rebutted anywhere:

- **PR-A (decisive) — "Your compute win is an artifact of an all-planet sample."** (F1.) At survey scale the planetless majority dominates and your prefilter adds cost. *Needed:* survey-representative compute accounting or a scoped claim.
- **PR-B — "Multi-planet systems defeat event-spacing period recovery."** (F4.) *Needed:* iterative masking method + a multi-planet recovery benchmark.
- **PR-C — "Pick one: TTV-robust *or* period-from-spacing."** (F3.) *Needed:* scope the generality claim to detection only.
- **PR-D — "Monotransits can't be period-confirmed; what stops a flare from being your headline detection?"** (F5.) *Needed:* a dedicated single-event vetting criterion.
- **PR-E — "Your non-inferiority test multiplicities aren't controlled."** (F6.)
- **PR-F — "Modern TLS/BLS are fast (vectorized/GPU); is your baseline a straw man?"** *Needed:* an optimized, clearly-specified baseline and a fair runtime protocol.
- **PR-G — "Idealized Mandel–Agol injections are easier than real transits (spot crossings, TTVs, real systematics in-transit)."** Partially A3, but reviewers will push; *consider* injecting non-ideal transits and report the gap vs. TOIs.
- **PR-H — "How much recall does conditioning destroy before detection?"** (F11.) Cancels in the *comparison* (shared), but caps absolute recall and must be reported.
- **PR-I — "Show robustness to z⋆/θ/T."** A sensitivity analysis (not on the sealed test) should be promised.

---

## 6. REPOSITORY HYGIENE (Low severity, quick wins)

- **Empty duplicate `TRINETRA-X.md` at repo root** (the real one is `docs/TRINETRA-X.md`) — delete or make it a pointer to avoid an authoritative-source ambiguity.
- **Empty `README.md`** — should carry a one-screen project overview + doc map + "current phase."
- **Empty `CLAUDE.md`** — should carry agent operating context (non-negotiables, doc map, "don't build prematurely," current phase) so any agent session inherits the rules.
- **Empty `archive/legacy/`** — remove or populate.
- **No bibliography** (`references.bib`) despite `PAPER_NOTES.md` §11 listing the citation set.
- **LaTeX-in-Markdown** renders only in math-aware viewers (noted previously) — acceptable, but state the rendering assumption in `README.md`.
- **No data-availability statement / version manifest** file yet (ties to §4 pinning).

---

## 7. PRIORITIZED REMEDIATION (before Phase I executes)

**Must-fix (blocks a credible Phase I result):**
1. **F1** — define the compute-measurement population and either scope H1b or add a clean-skip tier (decide explicitly). *Update `TRINETRA_X_PHASE1_VALIDATION.md` §4 + `SCIENTIFIC_HYPOTHESIS.md` H1b + `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §8.*
2. **F2** — write the operational recovery/recall predicate (period tolerance, harmonics, epoch, SDE). *Add to `TRINETRA_X_PHASE1_VALIDATION.md` §4.*
3. **F6** — specify a single primary estimand + multiplicity rule for non-inferiority. *`SCIENTIFIC_HYPOTHESIS.md` §6.*
4. **F8 + §4 baseline config** — pin z⋆/θ/T, the TLS configuration, and the runtime protocol. *`TRINETRA_X_PHASE1_VALIDATION.md` §2–§4.*

**Should-fix (before publication, ideally before run):**
5. **F4/F5/F3** — state single-planet & strict-periodicity assumptions; add a monotransit vetting criterion; scope the model-agnostic claim. *`SCIENTIFIC_HYPOTHESIS.md` §5, `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` §4/§6.*
6. **Required ablation + null-star FP target + power analysis shown.** *`TRINETRA_X_PHASE1_VALIDATION.md` §5–§6.*

**Nice-to-fix:** F7, F9, F10, F11 wording/assumptions; §6 hygiene.

---

## 8. WHAT IS *NOT* BROKEN (for balance)

The core logic is sound and unusually well-guarded: the fairness keystone (identical TLS engine/threshold in both arms), the photometric-significance gate replacing timing coincidence, the bootstrap-FAP calibration, the recall-first non-inferiority framing, the master equation reducing the claim to one inequality, and the honest pre-registration with a falsifiable null. The gaps above are about **pinning down and externally validating** that logic — not about a flaw in the idea. None require redesigning the architecture; all are specification or scoping fixes.

---

*Gap analysis v1.0. Findings are cross-referenced to source documents by section. Recommend resolving the four Must-fix items as document edits under the existing pre-registration discipline (a substantive change to frozen parameters requires a re-dated pre-registration).*
