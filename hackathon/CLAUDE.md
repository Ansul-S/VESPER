# CLAUDE.md — Hackathon Track (BAH 2026 · PS7)

> Operating rules for the **Bharatiya Antariksh Hackathon 2026, Problem Statement 7** track only.
> This file governs work **inside `hackathon/`**. For anything project-wide, defer to the
> **root [`../CLAUDE.md`](../CLAUDE.md)** — it is authoritative on any conflict.

## What this track is

An **applied extension/attachment to TRINETRA-X** for ISRO's BAH 2026, **PS7 — AI-enabled
Detection of Exoplanets from Noisy Astronomical Light Curves**. It reuses the validated
TRINETRA-X detection spine and adds the PS7-specific pieces: a **trained 4-class classifier**
(transit / eclipse / blend / other), crowded-field/blend handling, parameter estimation,
visualization, and a ≤3-page report. Goal: build a *product/demo* that scores on PS7's
criteria — distinct from TRINETRA-X's principle-validation mission.

## Relationship to the main project (read this first)

- **Phase I (TESS) is SEALED and FINAL.** Do **not** edit sealed docs/manifests or the
  `phase1-prereg-v*` git tags. See root `../CLAUDE.md`.
- **Phase II (Kepler scaling) + the compute-path decision are FROZEN** until after the
  hackathon (owner decision, 2026-06-26). Do not resume Phase II here.
- This track is **not** bound by the Phase-I anti-tuning / pre-registration discipline
  (that governs the *research*). Here a **learned classifier is the point**, not a violation.
  Still keep good ML hygiene: leakage-safe train/val/test splits by star, no tuning on the
  final science/test data, calibrated confidence, honest evaluation.
- Live on branch **`hackathon/bah2026-ps7`** (PR #14 → `main`). Don't mix with research branches.

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
deck/                              figures.py + build_deck.py -> BAH2026_PS7_idea_deck.pdf
prototype/                         working pipeline (cache/ + out/ are gitignored)
  fetch_tess.py                    download SPOC 2-min LCs from MAST + condition (reuses M1 recipe)
  features.py                      physics-feature extractor (classifier design §3)
  smoke_test.py                    batch driver over conditioned LCs
  make_labeled_set.py              inject 4 classes -> labeled feature set
  train_classifier.py             physics-branch GBT + confusion matrix + importances
```

## Environment & how to run

- Use the repo venv: **`.venv/bin/python`** (has numpy/scipy/lightkurve/astropy/wotan/
  transitleastsquares/batman/sklearn/matplotlib). **Missing:** `xgboost`, `torch` — the
  physics branch uses sklearn `HistGradientBoostingClassifier`; the CNN branch is deferred
  to the build phase (install torch then).
- Reused spine lives in `../research/m3_calibration/` (`detector.py`, `period_recovery.py`);
  scripts add it to `sys.path`. Conditioned Phase-I LCs are in `../data/processed/m1/*.npz`.
- Filter noisy lightkurve/MAST warnings in shell output when needed.

## Current status (2026-06-26)

- Proposal v1.0 + 9-slide PDF deck built (team fields are **placeholders** — owner fills).
- Prototype validated on **fresh MAST data**: TIC 100029948 → EB; Pi Mensae c blindly
  recovered (P=6.262 d, 289 ppm, SDE 12.3).
- Physics-branch classifier on injected labels: **0.84 held-out accuracy** (only
  transit↔blend confusion — the genuinely hard case).
- **PR #14** open.

## Conventions / guardrails

- Reuse the TRINETRA-X spine; don't reimplement conditioning/detection/period-recovery.
- Keep prototype data artifacts (`cache/`, `out/`) gitignored; commit code + deck + key figures.
- Convert relative dates to absolute. Be honest about limitations (esp. blend ID from
  light curves alone — needs pixel-level/centroid data; report it, don't overclaim).
- Commit/push only when the owner asks (root rule). End commit messages with the
  `Co-Authored-By` trailer (root rule).

## Immediate next steps

1. Owner: fill team details (deck slides 1–2 + "first hackathon?" field) → re-run `build_deck.py`.
2. Owner: submit before 2026-07-01 (paste Part-A fields + upload PDF, select PS7).
3. Obtain organizer's **curated labeled set** → drop into `train_classifier.py` (same interface).
4. Build phase (if shortlisted): CNN folded-view branch + conformal calibration + pixel-level
   blend features. See `BAH2026_PS7_CLASSIFIER_DESIGN.md`.
