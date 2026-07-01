# VESPER — AI-enabled Detection of Exoplanets from Noisy TESS Light Curves
### BAH 2026 · Problem Statement 7 · Technical Report (≤3 pages)

> **Team VESPER** — Ansul Suryawanshi (lead, IGNOU) · Riddhi Jain (IGNOU) · Samiksha Choudhary (Priyadarshini CoE, Hingna, Nagpur)
> Report skeleton — pre-filled from the round-1 prototype; bracketed `[round-2: …]` items get the final numbers on the organizer's provided dataset. **Keep to 3 pages: trim prose, lean on the figures + tables.**

---

## 1. Objective & approach (½ col)
We detect and classify transit-like dips in noisy TESS light curves and characterize genuine transits. Our pipeline is **evidence-first and physics-grounded**: cheap detection of periodic dips, then a **classifier built on trapezoid transit-shape parameters** (transit / eclipse / blend / other) with **calibrated confidence**, then parameter fitting with uncertainties. It extends a pre-registered exoplanet pipeline whose recall is non-inferior to full Transit Least Squares (TLS).

## 2. Methodology — five steps (mirrors the PS7 brief) (~1 page)
1. **Detrending.** Per-sector **wotan biweight** detrend (2.5-day window) removes detector/systematic ramps → zero-centred residual flux; robust noise model (σ, CDPP). *[Fig. 1: raw vs detrended]*
2. **Identification.** Box matched-filter detection of dips over a duration grid; **period from event spacing** (integer-comb) with a **block-bootstrap false-alarm probability**; for shallow signals, **TLS**. Phase-folding (global + local views). *[Fig. 2: light curve + folded transit]*
3. **Characterization.** Symmetric **trapezoid shape fit** → baseline flux, depth, total duration, **ingress/egress**, **flat-bottom**, and flat-fraction. *Depth alone does not separate a planet from a false positive; the shape (U vs V) does.* *[Fig. 3: characterization — EB vs planet]*
4. **Classification.** Gradient-boosted classifier on physics shape features (depth, duration, **flat-fraction**, **odd–even depth difference**, **secondary-eclipse depth**, ingress fraction, SNR), optionally ensembled with a CNN on folded views; **conformal calibration** gives per-class confidence (with abstention). Trained on the curated/known set, applied to the unknown set. *[Fig. 4: confusion matrix + feature importances]*
5. **Statistical significance.** Per-event **SNR** and a folded transit-model **likelihood-ratio** significance vs a flat baseline; period **FAP** from the bootstrap.

## 3. Assumptions (¼ col)
- Single dominant periodic body per target (no multi-planet de-blending in v1).
- Conditioning preserves transit shape (verified by injection–recovery; transits survive detrending).
- Curated training labels are representative of the unknown-set signal classes.
- Near-white residuals after detrending (low lag-1 autocorrelation); red noise absorbed by the self-calibrated scatter.
- Monotransits and highly grazing/irregular geometries are out of scope for v1.

## 4. Tools & libraries (¼ col)
Python · numpy · scipy · pandas · matplotlib · **lightkurve/astroquery (MAST)** · **wotan** (detrend) · **transitleastsquares**, **batman** (search/modelling) · **scikit-learn** (HistGradientBoosting) · [round-2: PyTorch for CNN view; MAPIE for conformal]. All open-source; data is public (MAST / TESS). TIC catalog supplies the **contamination ratio** (blend feature).

## 5. Uncertainty estimation (¼ col)
- **Period:** bootstrap false-alarm probability + spacing-based error; TLS SDE for significance.
- **Depth / duration / ingress:** trapezoid least-squares **covariance** error bars [round-2: MCMC posteriors for the science set].
- **Classification:** **conformal prediction** → calibrated per-class confidence and an "uncertain/abstain" option when classes overlap.
- **Detection:** per-event SNR and likelihood-ratio significance at a controlled false-alarm rate.

## 6. Results & validation (~½ page)
**Validated on real, labelled objects (round-1).** Conditioning → TLS period recovery → shape-fit on **12 known objects** (6 confirmed planets fresh from MAST + 6 known eclipsing binaries):
- Clean transiters recovered with **literature-matching periods** (e.g. Pi Mensae c: P=6.262 d vs 6.268, depth 289 ppm vs ~315; WASP-121, WASP-100 likewise) and correct **U-shape**; eclipsing binaries flagged **V-shape**. *[Fig. 5: depth × shape — no single feature separates the classes]*
- A single shape feature scores only **0.58** — no single feature separates the classes, which empirically motivates the **multi-feature** classifier.
- **Characterization reproduces the committee's slide-5/6 output on real data** (EB flat-fraction 0.26 = false-positive; planet 0.67).
- **Classifier proof-of-path (SYNTHETIC labels, leakage-safe group CV):** out-of-fold macro-F1 **0.83 (95% CI 0.80–0.86)** on a 4-class injected set; eclipse & systematics near-perfect, the residual is shallow **transit vs blend** (F1 ≈ 0.66). Feature **ablation** confirms no single family exceeds 0.72 (depth-only 0.62, shape-only 0.53) while the full physics set reaches 0.83. *[Fig. 4]* These validate the pipeline + feature design, **not** real-world accuracy — real labels come with the curated set.

[round-2: classification accuracy / confusion matrix on the **provided unknown dataset**; recovered parameter accuracy table (period, depth, duration vs truth); per-event significance levels.]

## 7. Limitations & future work (¼ col)
- **Blends at planet-like depth** are the hard case — light-curve shape alone is ambiguous; we add **pixel-level centroid / difference-imaging** (Target Pixel Files) + the TIC contamination ratio.
- **Period recovery on pathological stars** (active young stars, ultra-short-period aliases, strong phase curves) is the main failure mode found in validation → robust multi-stage period search + phase-curve model.
- **CNN ensemble** on global+local folded views for morphology beyond hand-crafted features.
- Multi-planet systems and monotransits.
- **Scale-out to Kepler / K2** (~200k long-cadence stars): the same condition-then-discard, recall-first pipeline runs as a short cloud burst (≈ **5,000–10,000 CPU-core-hours**; data public on MAST / AWS Open Data, no egress) — a feasibility / order-of-magnitude estimate, not a compute-savings claim.

## Figure list (target ≤6 for 3 pages)
1. Detrending (raw vs flat). 2. Light curve + folded transit. 3. Characterization: EB (V) vs planet (U). 4. Classifier confusion matrix + feature importances. 5. Validation on known objects (depth × shape). 6. Example output "report card" (LC + fit + class + confidence + params).

---
*Prototype artifacts backing this report live in `hackathon/prototype/` (figures in `prototype/figs/`, deck in `deck/`).*
