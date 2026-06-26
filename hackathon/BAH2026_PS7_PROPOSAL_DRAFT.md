# BAH 2026 · PS7 — Idea Submission (v1.0 — mapped to official template, prototype-validated)

> **Problem Statement 7:** AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves
> **Solution name:** TRINETRA · **Approach:** Hybrid (physics features ⊕ CNN) · **Date:** 2026-06-26
> Two deliverables: **(A) web-form fields** + **(B) idea deck (PPTX→PDF ≤5 MB)**. Fill `[...]` placeholders.

> **Proof of concept (validated 2026-06-26, fresh MAST data).** The full spine runs end-to-end today:
> we downloaded raw SPOC 2-min light curves from MAST, conditioned them, and (i) the physics-feature
> extractor confidently flagged **TIC 100029948** as an **eclipsing binary** (depth ≈25%, odd–even
> diff 0.23, V-shape), while (ii) the full-search arm **blindly recovered Pi Mensae c** at
> **P = 6.262 d** (literature 6.268), **depth 289 ppm** (literature ≈315), **SDE 12.3**. See
> `prototype/figs/eb_vs_planet.png`. Only the *trained* 4-class classifier remains to be built
> (it needs the organizer's labeled set), and it is fully specced in `BAH2026_PS7_CLASSIFIER_DESIGN.md`.

---

# PART A — Dashboard web-form (paste-ready, within character limits)

### Challenge (dropdown)
→ **PS7: AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves**

### Brief about your Idea *(≤1024 chars)*
> TRINETRA is an evidence-first, physics-grounded AI pipeline that detects and classifies transit-like dips in noisy TESS light curves from crowded fields. It cheaply finds candidate periodic dips, then routes each through a hybrid classifier — physics-motivated features (depth, duration, odd–even depth, secondary eclipse, V-/U-shape, centroid & dilution proxies) combined with a CNN on the phase-folded light curve — to label it transit / eclipse / blend / other with a calibrated confidence. For genuine transits it fits period, depth, and duration with uncertainties, and visualizes the result. It is built on a working, pre-registered exoplanet pipeline already benchmarked against full Transit Least Squares on TESS, so we extend a validated spine rather than start from scratch. Recall is prioritized: a missed planet is the costly error; physics confirms every detection.

### What problem are you trying to solve? *(≤2000 chars)*
> Detecting exoplanets by transit photometry means finding brightness dips of a few parts per thousand — or less — in stellar light curves. In TESS's crowded fields this is acutely hard for three reasons. (1) Noise & contamination: detector systematics and flux from blended foreground/background stars in the photometric aperture dilute and distort the signal. (2) Confusion of look-alikes: a dip can be a transiting planet, an eclipsing binary, a background/blended eclipse, or starspot variability — each leaves distinct but subtle features that are easily conflated in noisy data, so naive detectors flood the candidate list with false positives. (3) Trust: a raw detection without calibrated confidence, a significance level, or fitted physical parameters is not scientifically actionable.
>
> TRINETRA solves all three. It robustly identifies periodic dips in noisy light curves, then classifies each into transit / eclipse / blend / other using a hybrid AI model that fuses interpretable physics features with a CNN view of the folded signal. It explicitly handles crowded-field blends via centroid-shift and dilution/contamination proxies, odd–even depth differences, and secondary-eclipse checks. Every detection carries an SNR / significance level and a calibrated confidence (bootstrap false-alarm probability for periods, conformal prediction for class probabilities), so confidence is trustworthy rather than an uncalibrated score. For confirmed transits it estimates orbital period, transit depth, and duration with uncertainties by light-curve fitting, and produces clear visualizations of the light curve with the detected, classified signal. The outcome is an end-to-end, interpretable pipeline from raw TESS light curve to a vetted, parameterized, confidence-scored candidate.

### Technology Stack being used *(≤1024 chars)*
> Python scientific stack: numpy, scipy, pandas, matplotlib. Astronomy: lightkurve, astropy, astroquery/MAST (TESS data access), wotan (detrending), transitleastsquares & batman (transit search + modelling). Machine learning: scikit-learn, XGBoost/LightGBM (physics-feature branch), PyTorch (CNN branch on global+local folded views), conformal-prediction calibration (e.g. MAPIE) for trustworthy confidence. Injection–recovery into real conditioned light curves for labeled augmentation and uncertainty validation. All open-source; no specialized or licensed software.

### Is this your first hackathon? If Yes, then please share your experience. *(≤1024 chars)*
> Not for the whole team. Our team leader (Ansul Suryawanshi) has participated in several hackathons before; those earlier attempts — including round-1 exits — taught us to lead with a working, rigorously validated solution rather than a concept deck. For Riddhi Jain and Samiksha Choudhary this is their first hackathon, bringing fresh perspective and energy. What we bring to PS7 is a genuine head start: TRINETRA-X, a pre-registered exoplanet-detection pipeline we developed and benchmarked against full Transit Least Squares on TESS data (ISRO exoplanet context), with calibrated confidence and demonstrated eclipsing-binary rejection. The detection spine already runs end-to-end on real MAST data — we are extending it with the AI classifier this challenge needs, not starting from scratch.

---

# PART B — Idea deck (slide-by-slide; PPTX → PDF ≤5 MB)

### Slide 1 — Title
- **Team Name:** TRINETRA-X
- **Problem Statement:** PS7 — AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves
- **Team Leader Name:** Ansul Suryawanshi
- _(Solution name: **TRINETRA**)_

### Slide 2 — Team Members
- **Team Leader:** Ansul Suryawanshi · Indira Gandhi National Open University (IGNOU)
- **Member-1:** Riddhi Jain · Indira Gandhi National Open University (IGNOU)
- **Member-2:** Samiksha Choudhary · Priyadarshini College of Engineering (Hingna), Nagpur
- **Member-3:** `[optional 4th member — a team of 3 is valid; BAH allows 3–4]`
- _(Optionally note roles: data/conditioning · ML/classifier · physics/parameter-fit · viz/report)_

### Slide 3 — Opportunity (different / solves / USP)
- **How different from existing ideas?** Most pipelines either detect *or* classify, and many output uncalibrated scores. TRINETRA is **evidence-first + physics-grounded**: it routes on cheap evidence, confirms with a transit-model significance gate, and fuses **interpretable physics features with a CNN** — interpretable *and* high-ceiling. Built on a pipeline already **benchmarked vs full TLS** on TESS.
- **How will it solve the problem?** Detect periodic dips → classify (transit/eclipse/blend/other) with explicit **crowded-field/blend discriminators** → attach **SNR + calibrated confidence** → fit **period/depth/duration** with uncertainties → visualize.
- **USP:** (1) Hybrid physics+DL, interpretable & robust on small data. (2) **Calibrated confidence by construction** (bootstrap FAP + conformal). (3) **Physics decides** detection, recall-prioritized. (4) **Explicit blend handling** (centroid/dilution, odd–even, secondary eclipse). (5) Extends a **validated, pre-registered** spine — **already demonstrated on fresh MAST data** (Pi Men c blindly recovered at P=6.262 d / 289 ppm / SDE 12.3; TIC 100029948 flagged as an EB), not a blank slate.

### Slide 4 — Features offered
- Robust periodic-dip detection in noisy crowded-field light curves.
- 4-class AI classification: **transit / eclipse / blend / other**.
- **SNR / significance** per event.
- Transit **parameter fit**: orbital period, depth, duration (+ uncertainties).
- **Calibrated confidence** per detection.
- **Visualization**: annotated raw + phase-folded light curve with class + fit overlay.
- Reproducible, provenance-tracked, benchmarked vs full TLS.
- **Figure:** `prototype/figs/eb_vs_planet.png` (deep-V eclipse vs shallow-U planet, fresh MAST) + `deck/figs/four_class_concept.png`.

### Slide 5 — Process flow / use-case diagram
```
Raw TESS LC (MAST sector) → [1] Conditioning (wotan detrend + noise model)
 → [2] Dip detection (evidence-first) → [3] Period recovery (spacing + bootstrap FAP)
 → [4] Phase-fold (global+local) + feature extraction
 → [5] Hybrid classifier: physics features (GBT) ⊕ CNN(folded) → ensemble
       → {transit, eclipse, blend, other} + conformal confidence
 → [6] Confirmation + SNR (transit-model likelihood-ratio gate)
 → [7] Parameter fit (period, depth, duration + uncertainties)
 → [8] Visualization + report
```

### Slide 6 — Wireframes / mock (optional)
- Mock of the output report card per star: raw LC, folded fit, predicted class + confidence bar, fitted params table, SNR. _(Optional — include if time.)_

### Slide 7 — Architecture diagram
- Two-branch classifier: **Physics branch** (feature extractor → GBT/RF) + **Deep branch** (CNN on global+local folded views) → **ensemble + conformal calibration** → class + confidence; feeding the **confirmation gate** and **parameter-fit** modules. Shared **conditioning + detection + period-recovery** front-end (reused from TRINETRA-X). **Figure:** `deck/figs/arch_diagram.png`.

### Slide 8 — Technologies to be used
- **Core:** Python, numpy, scipy, pandas, matplotlib.
- **Astronomy:** lightkurve, astropy, astroquery/MAST, wotan, transitleastsquares, batman.
- **ML:** scikit-learn, XGBoost/LightGBM, PyTorch, conformal calibration (MAPIE).
- **Method:** injection–recovery into real light curves; bootstrap FAP; conformal prediction; benchmark vs full TLS.

### Slide 9 — Estimated implementation cost (optional)
- **₹0 software** — entirely open-source. Data is public (MAST). Development on standard laptops + free/low-cost cloud or a GPU session for CNN training. _(Negligible cost; emphasize feasibility.)_

---

## Notes / TODO before submitting (deadline 2026-07-01)
- [ ] Fill team name, leader, 3 members (name + college), roles.
- [ ] Fill "first hackathon?" honestly.
- [ ] Build the PPTX from the official template → export **PDF ≤5 MB**; add 2–3 figures (architecture, a folded-transit example, the 4-class concept).
- [ ] Paste Part-A fields into the dashboard form; select PS7 in the Challenge dropdown.
- [ ] (Build-phase, not now) obtain the organizer-provided **curated labeled training set** (separate from the raw TESS data source below).

### Data note (important distinction)
- The link `archive.stsci.edu/tess/tic_ctl.html` is the **TESS Input Catalog (TIC) + Candidate Target List (CTL)** — a *catalog of star properties/targets*, plus the **raw light-curve source** for a sector (downloaded via MAST bulk scripts / `lightkurve` / `astroquery` per sector, ~20–30k stars). This is the **unlabeled science data**.
- The **curated labeled dataset** (known planets, false positives, EBs) the hackathon "will provide" is **separate** and is what trains the classifier. We still need that from the organizers.
