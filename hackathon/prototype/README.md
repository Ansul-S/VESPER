# PS7 Prototype — smoke test

Proves the end-to-end path **ahead of the 30-h finale**: the reused TRINETRA-X
spine (untrained detector + period-from-spacing) feeding the **new** physics-feature
extractor (classifier design doc §3), run on **real conditioned TESS light curves**.

## Run
```bash
.venv/bin/python hackathon/prototype/smoke_test.py [N]   # N = #light curves (default 60)
```
Inputs: `data/processed/m1/*.npz` (Phase-I conditioned LCs: `time`, `resid`).
Outputs: `out/smoke_features.csv` (feature table) + `figs/folded_<TIC>.png` (example fold).

## Files
- `features.py` — physics-feature extractor: depth, depth_snr, period, fold_R,
  duration, **odd_even_diff**, **secondary_depth/ratio**, **v_over_u** (V-vs-U shape),
  oot_rms, SNRs. These are the physics-branch inputs to the hybrid classifier.
- `smoke_test.py` — batch driver + example folded-LC figure.

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

## Physics-branch classifier (proof of path, injected labels)
Until the organizer's curated labels arrive, `make_labeled_set.py` injects the four
classes onto realistic TESS noise and `train_classifier.py` trains a gradient-boosted
classifier on the extracted features.
```bash
.venv/bin/python hackathon/prototype/make_labeled_set.py 120
.venv/bin/python hackathon/prototype/train_classifier.py     # -> figs/classifier_eval.png
```
Result (2026-06-26): **held-out accuracy 0.84**; eclipse & other near-perfect; the only
confusion is **transit ↔ blend** — the genuinely hard case (a blend is a diluted eclipse
that mimics a shallow planet). Top features: n_events, max_snr, depth_snr, **odd_even_diff**,
**secondary_depth** — confirming the physics tells drive the separation. The transit/blend
gap is what **pixel-level centroid/difference-imaging features** (design §6) are for.

## Status / next (build phase)
- Spine + extractor + physics-branch classifier all run end-to-end on real/realistic data.
- Next: swap injected labels for the organizer's **curated set** (same interface); add the
  CNN folded-view branch + conformal calibration; add pixel-level (TPF) blend features.
  See `../BAH2026_PS7_CLASSIFIER_DESIGN.md`.
