# CLAUDE.md — Hackathon Track (BAH 2026 · PS7)

> Operating rules for the **Bharatiya Antariksh Hackathon 2026, Problem Statement 7** track only.
> This file governs work **inside `hackathon/`**. For anything project-wide, defer to the
> **root [`../CLAUDE.md`](../CLAUDE.md)** — it is authoritative on any conflict.

## What this track is

An **applied extension/attachment to VESPER** for ISRO's BAH 2026, **PS7 — AI-enabled
Detection of Exoplanets from Noisy Astronomical Light Curves**. It reuses the validated
VESPER detection spine and adds the PS7-specific pieces: a **trained 4-class classifier**
(transit / eclipse / blend / other), crowded-field/blend handling, parameter estimation,
visualization, and a ≤3-page report. Goal: build a *product/demo* that scores on PS7's
criteria — distinct from VESPER's principle-validation mission.

## Relationship to the main project (read this first)

- **Phase I (TESS) is SEALED and FINAL.** Do **not** edit sealed docs/manifests or the
  `phase1-prereg-v*` git tags. See root `../CLAUDE.md`.
- **Phase II (Kepler scaling) + the compute-path decision are FROZEN** until after the
  hackathon (owner decision, 2026-06-26). Do not resume Phase II here.
- This track is **not** bound by the Phase-I anti-tuning / pre-registration discipline
  (that governs the *research*). Here a **learned classifier is the point**, not a violation.
  Still keep good ML hygiene: leakage-safe train/val/test splits by star, no tuning on the
  final science/test data, calibrated confidence, honest evaluation.
- Now on **`main`** (v1.0.0 shipped); the hackathon deck + prototype live under `hackathon/`.

## Deadlines (absolute)

- **Idea submission CLOSES 2026-07-01** — deliverable is the proposal + PDF deck, *not* a prototype.
- Shortlist 2026-07-20 · Induction 2026-07-21 · **Grand Finale (30 h) 2026-08-06→07** (the build phase).
- Eligibility: students at Indian institutions, **team of 3–4** (confirmed in place).

## Directory map (`hackathon/`)

```
CLAUDE.md                          this file
BAH2026_PS7_CHALLENGE.md           event facts, full PS7 spec, asset-mapping, guardrails (memory)
BAH2026_PS7_PROPOSAL_DRAFT.md      idea submission mapped to official template (web-form + slides)
BAH2026_PS7_CLASSIFIER_DESIGN.md   hybrid classifier design spec (the centerpiece)
deck/                              figures.py + build_pptx.py -> BAH2026_PS7_idea_deck.pptx (+ .pdf)
                                   fills the OFFICIAL ISRO template; build_deck.py is legacy
prototype/                         working pipeline (cache/ + out/ are gitignored)
  fetch_tess.py                    download SPOC 2-min LCs from MAST + condition (reuses M1 recipe)
  features.py                      physics-feature extractor (classifier design §3)
  smoke_test.py                    batch driver over conditioned LCs
  make_labeled_set.py              inject 4 classes (records host) -> labeled feature set
  train_classifier.py              leakage-safe classifier eval (group CV, CI, importance)
  ablation.py · failure_analysis.py   feature ablation + transit/blend hard-case figures
  make_poc_fig.py · characterization_demo.py · validate_known.py   real-data figures
```

## Environment & how to run

- Use the repo venv: **`.venv/bin/python`** (has numpy/scipy/lightkurve/astropy/wotan/
  transitleastsquares/batman/sklearn/matplotlib). **Missing:** `xgboost`, `torch` — the
  physics branch uses sklearn `HistGradientBoostingClassifier`; the CNN branch is deferred
  to the build phase (install torch then).
- Reused spine lives in `../research/m3_calibration/` (`detector.py`, `period_recovery.py`);
  scripts add it to `sys.path`. Conditioned Phase-I LCs are in `../data/processed/m1/*.npz`.
- Filter noisy lightkurve/MAST warnings in shell output when needed.

## Current status (2026-07-01)

- **Official-template deck built + verified:** `deck/BAH2026_PS7_idea_deck.pptx` (14 slides, official
  ISRO template, populated) + `.pdf` (≤5 MB). Team fields filled (Ansul / Riddhi / Samiksha).
- Prototype validated on **fresh MAST data**: TIC 100029948 → EB; Pi Mensae c blindly recovered
  (P=6.262 d, 289 ppm, SDE 12.3).
- Physics-branch classifier (**synthetic** labels, leakage-safe group CV): **macro-F1 0.83
  (95% CI 0.80–0.86)**; eclipse/other near-perfect; only transit↔blend confusion. Ablation: no single
  feature family > 0.72, full set 0.83 → depth alone does not discriminate.
- Claims aligned for defensibility: **recall non-inferior to full TLS** (not a compute claim);
  synthetic results explicitly labelled; blend/CNN scoped to Round-2.

## Conventions / guardrails

- Reuse the VESPER spine; don't reimplement conditioning/detection/period-recovery.
- Keep prototype data artifacts (`cache/`, `out/`) gitignored; commit code + deck + key figures.
- Convert relative dates to absolute. Be honest about limitations (esp. blend ID from
  light curves alone — needs pixel-level/centroid data; report it, don't overclaim).
- Commit/push only when the owner asks (root rule). End commit messages with the
  `Co-Authored-By` trailer (root rule).

## Immediate next steps

1. Owner: **submit before 2026-07-01** — upload `deck/BAH2026_PS7_idea_deck.pdf` (or the PPTX),
   paste Part-A fields from `BAH2026_PS7_PROPOSAL_DRAFT.md`, select PS7.
2. Owner: confirm the optional 4th member (team of 3 is valid).
3. Round-2: swap synthetic labels for the organizer's **curated set** (same interface); add the
   CNN folded-view branch + conformal calibration + pixel-level (TPF) blend features.
   See `BAH2026_PS7_CLASSIFIER_DESIGN.md`.
