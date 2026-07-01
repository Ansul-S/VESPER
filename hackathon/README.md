# BAH 2026 · Problem Statement 7 — VESPER

**AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves** — the applied hackathon track of **[VESPER](../README.md)**, built for ISRO's **Bharatiya Antariksh Hackathon 2026** (powered by Hack2skill).

> An **extension/attachment to VESPER**, not a fork. It reuses VESPER's validated TESS detection spine and adds the PS7-specific pieces: a 4-class classifier (transit / eclipse / blend / other), parameter estimation, visualization, and a report. **Phase-I research is sealed/final and untouched here.**

## Status (2026-07-01)

- **Round-1 idea submission: COMPLETE + submitted.** Deck built **inside the official ISRO template** (mandatory), 14 slides → [`deck/BAH2026_PS7_idea_deck.pdf`](deck/BAH2026_PS7_idea_deck.pdf) (+ `.pptx`).
- **Team VESPER** — Ansul Suryawanshi (lead, IGNOU) · Riddhi Jain (IGNOU) · Samiksha Choudhary (Priyadarshini CoE, Hingna, Nagpur).

## The five-step method (mirrors the PS7 brief)

`01 Detrend` (wotan biweight) → `02 Identify` (dip detection + period-from-spacing + phase-fold) → `03 Characterize` (trapezoid shape fit) → `04 Classify` (transit / eclipse / blend / other) → `05 Significance` (SNR + transit-LR).

## Verified results

**Real MAST data (fresh, blind):**
- **Pi Mensae c** blindly recovered by TLS — P = 6.262 d (lit. 6.268), depth 289 ppm (lit. ~315), SDE 12.3.
- **TIC 100029948** flagged as an eclipsing binary — depth ~25%, V-shape, odd–even 0.23.
- Trapezoid shape-fit reproduces the committee's step-03 output: EB flat-fraction 0.26 (V → false positive) vs planet 0.67 (U).

**Classifier proof-of-path — SYNTHETIC labels, leakage-safe** (StratifiedGroupKFold, no injection host shared train/test):
- accuracy **0.83**, macro-F1 **0.83 (95% CI 0.80–0.86)**; eclipse & systematics near-perfect; the only residual is shallow **transit vs blend** (F1 ≈ 0.66).
- **Ablation:** duration 0.50 · shape 0.53 · EB-tells 0.58 · depth 0.62 · detection 0.72 · **all-physics 0.83** → *no single feature family suffices; depth alone does not discriminate.*

> ⚠️ **Scope:** classifier numbers are on **synthetic** labels (injected signals on real TESS noise) — they validate the pipeline + feature design, **not** real-world accuracy. The organizers' curated labels + a CNN branch + pixel-level (TPF) blend features are the **Round-2** build. The reused spine's **recall is non-inferior to full TLS** (this is not a compute-savings claim).

## Layout

```
BAH2026_PS7_CHALLENGE.md        event facts + full PS7 spec + asset-mapping
BAH2026_PS7_PROPOSAL_DRAFT.md   idea submission (Part-A web-form text + Part-B deck outline)
BAH2026_PS7_CLASSIFIER_DESIGN.md hybrid classifier design spec
BAH2026_PS7_REPORT_SKELETON.md  ≤3-page technical report skeleton
CLAUDE.md                       track-scoped operating rules
deck/     build_pptx.py (fills the official template) + figures.py -> idea_deck.pptx (+ .pdf)
prototype/  features.py · shape_fit.py · train_classifier.py (leakage-safe) · ablation.py ·
            failure_analysis.py · make_poc_fig.py · validate_known.py · make_labeled_set.py
```

## Build

```bash
.venv/bin/python hackathon/deck/figures.py               # arch · four-class · process-flow figures
.venv/bin/python hackathon/prototype/make_poc_fig.py     # proof-of-concept figure
.venv/bin/python hackathon/prototype/make_labeled_set.py 120   # synthetic 4-class set (records host)
.venv/bin/python hackathon/prototype/ablation.py         # figs/ablation.png
.venv/bin/python hackathon/prototype/train_classifier.py # figs/classifier_eval.png + metrics.json
.venv/bin/python hackathon/deck/build_pptx.py            # fills the official template -> idea_deck.pptx
```

The official ISRO template (`[Pub] ISRO BAH 2026 _ Idea Submission Template (2).pptx`) is obtained from the organizers and kept locally in `deck/` (gitignored). Export the PDF from PowerPoint / Google Slides, or headless LibreOffice.
