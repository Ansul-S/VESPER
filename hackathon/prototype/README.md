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

## Status / next (build phase)
- This is SMOKE-TEST grade (no labels yet, no TPF/centroid blend features).
- Next: train physics branch (GBT) once the organizer's **curated labeled set** arrives;
  add the CNN folded-view branch + conformal calibration; add pixel-level blend features
  if TPFs are pulled. See `../BAH2026_PS7_CLASSIFIER_DESIGN.md`.
