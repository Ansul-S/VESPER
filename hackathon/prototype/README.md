# PS7 Prototype — smoke test

Proves the end-to-end path **ahead of the 30-h finale**: the reused VESPER
spine (untrained detector + period-from-spacing) feeding the **new** physics-feature
extractor (classifier design doc §3), run on **real conditioned TESS light curves**.

## Run
```bash
.venv/bin/python hackathon/prototype/smoke_test.py [N]   # N = #light curves (default 60)
```
Inputs: `data/processed/m1/*.npz` (Phase-I conditioned LCs: `time`, `resid`).
Outputs: `out/smoke_features.csv` (feature table) + `figs/folded_<TIC>.png` (example fold).

## Files
- `features.py` — physics-feature extractor (21 features: depth, depth_snr, period, fold_R,
  duration, **odd_even_diff**, **secondary_depth/ratio**, **v_over_u**, trapezoid **flat_frac /
  ingress_frac**, SNRs). Physics-branch inputs to the hybrid classifier.
- `shape_fit.py` — symmetric trapezoid transit-shape fit (committee step 03).
- `smoke_test.py` — batch driver + example folded-LC figure.
- `make_labeled_set.py` — synthetic 4-class injection on real TESS noise; records the injection
  **host** per row (enables leakage-safe group CV). → `out/labeled_features.csv`.
- `train_classifier.py` — **leakage-safe** classifier evaluation (StratifiedGroupKFold out-of-fold
  confusion matrix + per-class P/R/F1 + bootstrap 95% CI + fold-averaged permutation importance).
- `ablation.py` — feature-family ablation (group-CV macro-F1). → `figs/ablation.png` + `out/ablation.csv`.
- `failure_analysis.py` — the transit↔blend hard case. → `figs/failure_case.png`.
- `make_poc_fig.py` — proof-of-concept figure (EB vs planet, fresh MAST). → `figs/eb_vs_planet.png`.
- `characterization_demo.py` — trapezoid shape fit on real data. → `figs/characterization.png`.
- `validate_known.py` — real-label validation on 12 known objects. → `figs/validation_known.png`.
- `_deckstyle.py` — shared publication styling for the figures.

## What the first runs showed (2026-06-26)
- 60/60 cached conditioned LCs processed without error; full feature table produced.
- **Fresh-from-MAST** end-to-end (`fetch_tess.py`): downloaded + conditioned
  **TIC 100029948** (45,232 cadences, sectors 2/3/69) → auto-flagged as an
  **eclipsing binary**: depth ~25%, V-shape, **odd-even diff 0.23**, fold_R 0.99
  — the exact transit-vs-eclipse discrimination PS7 grades, from physics features.
- **Planet contrast:** downloaded **Pi Mensae** (TIC 261136679, sector 1); the
  full-search arm (**TLS**) blindly recovered planet **c** at **P=6.262 d**
  (lit. 6.268 ✓), **depth 289 ppm** (lit. ~315 ✓), dur 3.0 h, **SDE 12.3**.
- Figure `figs/eb_vs_planet.png`: deep-V stellar eclipse vs shallow-U planet,
  both from fresh MAST data — the headline visual for the proposal/report.

## Data scale note (PS7 full-sector)
SPOC 2-min LC FITS ≈ 1.9 MB each → a full sector (~20-30k stars) is ~40-55 GB raw.
Strategy: download → condition → keep only the slim npz (~10 GB/sector, less as
float32) and delete raw FITS per target; or batch. AWS us-east-1 (MAST Open Data)
avoids local storage entirely. Not needed for the proposal.

## Physics-branch classifier (proof of path — SYNTHETIC labels)
Until the organizer's curated labels arrive, `make_labeled_set.py` injects the four classes onto
realistic TESS noise (real cadence/gaps + each LC's measured rms) and the classifier is evaluated
**leakage-safe** (no injection host shared train/test).
```bash
.venv/bin/python hackathon/prototype/make_labeled_set.py 120   # -> out/labeled_features.csv (480 rows, 116 hosts)
.venv/bin/python hackathon/prototype/train_classifier.py       # -> figs/classifier_eval.png (+ out/classifier_metrics.json)
.venv/bin/python hackathon/prototype/ablation.py               # -> figs/ablation.png
.venv/bin/python hackathon/prototype/failure_analysis.py       # -> figs/failure_case.png
```
Verified result (leakage-safe StratifiedGroupKFold, out-of-fold n=480): **accuracy 0.83, macro-F1
0.83 (95% CI 0.80–0.86)**. Eclipse & other are near-perfect (F1 0.99 / 1.00); the only confusion is
**transit ↔ blend** (F1 ≈ 0.66) — the genuinely hard case (a blend is a diluted eclipse that mimics a
shallow planet). **Ablation** (group-CV macro-F1): depth-only 0.62, shape-only 0.53, detection 0.72 —
no single family exceeds 0.72; the **full physics set reaches 0.83**, so depth alone does not
discriminate. Top features: n_events, max_snr, oot_rms. The transit/blend gap is what **pixel-level
centroid/difference-imaging features** (design §6) address in round 2.
> These numbers are on **synthetic labels** — they validate the pipeline + feature design, not
> real-world accuracy. Round-2 uses the organizer's curated set (same interface).

## Characterization — trapezoid shape fit (committee step 03)
`shape_fit.py` fits the symmetric trapezoid and returns the committee's slide-5/6 parameters
(baseline, depth, total duration, ingress/egress, flat-bottom, flat-fraction → U-vs-V verdict).
```bash
.venv/bin/python hackathon/prototype/characterization_demo.py   # -> figs/characterization.png
```
Result on **real** data: EB (TIC 100029948) depth 26% but **flat-fraction 0.26 → V-shape /
false-positive**; Pi Men c depth 279 ppm, **flat-fraction 0.67 → U-shape / planet**. This is the
committee's central point — *depth does not separate planet from false positive; shape does* — and
the shape params are now fed to the classifier (`features.py`). The shape fit cleanly handles the
deep EB-vs-planet case (eclipse F1=1.00); the shallow **transit↔blend** case stays hard (noise-limited
shape at low SNR) and is what pixel-level **centroid/difference-imaging** features address in round 2.

## Validation on KNOWN objects (real labels)
`validate_known.py` runs conditioning → TLS period recovery → trapezoid shape-fit on
confirmed planets (by name, fresh from MAST) and known EBs (RZ Cas + physically
unambiguous deep eclipses scanned from the cache), then checks shape verdict vs truth.
```bash
.venv/bin/python hackathon/prototype/validate_known.py   # -> figs/validation_known.png + out/validation_known.csv
```
Findings (12 objects): **clean transiters recovered with literature-matching periods**
(Pi Men, WASP-121, WASP-100 → U; RZ Cas + 3 deep EBs → V). The **single-feature** shape verdict
scores only **0.58** — no single feature separates the classes (deep total-eclipse EBs have flat
bottoms; phase-curve/short-period planets fold V-ish), which is exactly why the **multi-feature**
classifier is needed (cross-check: the synthetic ablation above — depth-only 0.62, shape-only 0.53
→ full physics set 0.83). The remaining misses are **period-recovery** failures on pathological
stars (AU Mic active; LHS 3844 alias; WASP-18 phase curve) — concrete round-2 targets.

## Status / next (build phase)
- Spine + extractor + physics-branch classifier all run end-to-end on real/realistic data.
- Next: swap injected labels for the organizer's **curated set** (same interface); add the
  CNN folded-view branch + conformal calibration; add pixel-level (TPF) blend features.
  See `../BAH2026_PS7_CLASSIFIER_DESIGN.md`.
