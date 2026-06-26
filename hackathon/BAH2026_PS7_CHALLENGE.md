# BAH 2026 — Problem Statement 7: Challenge Record

> Repository memory for the **Bharatiya Antariksh Hackathon 2026 (BAH 2026)** pivot.
> This is a **separate applied track** — an **extension/attachment to TRINETRA-X**, not a fork of it. It does **not** reopen or amend sealed Phase I (TRINETRA-X v3 is terminal). Phase I science stays sealed and final.
> Created 2026-06-26 on branch `hackathon/bah2026-ps7`.
>
> **Project course (owner decision, 2026-06-26):** Phase II (Kepler scaling) and its **compute-path decision are FROZEN** until after the hackathon. The owner will decide the overall project course after BAH 2026.

---

## 1. Event facts

| Field | Value |
|-------|-------|
| Event | Bharatiya Antariksh Hackathon 2026 (BAH 2026) |
| Organizer | ISRO, powered by Hack2skill |
| URL | https://hack2skill.com/event/bah2026/ |
| Eligibility | Students currently enrolled at **Indian institutions**; India-only; no working professionals |
| Team size | **3–4 members** (may span colleges) |
| Format | 30-hour grand finale |
| Fees | None |
| Prizes/benefits | ISRO recognition; potential ISRO internship; II-AC travel reimbursed for finalists; ISRO + domain mentorship |

### Timeline (absolute dates)
| Milestone | Date |
|-----------|------|
| Registration & Idea Submission opens | 2026-06-10 |
| Problem Statement Session 1 / 2 | 2026-06-15 / 2026-06-16 |
| **Registration & Idea Submission CLOSES** | **2026-07-01** |
| Final shortlist announced | 2026-07-20 |
| Induction session | 2026-07-21 |
| Grand Finale | 2026-08-06 → 2026-08-07 |

**Immediate deliverable = concept/idea proposal per provided template (no prototype required for round 1). Due 2026-07-01 (~5 days from creation of this record).**

### Our status (confirmed 2026-06-26)
- Eligibility: **YES** — eligible + team of 3–4 in place.
- Classifier approach decision: **Hybrid** (physics-motivated features + a CNN view on phase-folded light curves, ensembled).
- Venue/template: dashboard submission page is login-gated; **template fields still need to be pasted in** to finalize proposal formatting.

---

## 2. Problem Statement 7 (verbatim objective)

**Title:** AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves

**Objective:** Develop an AI-based data analysis pipeline capable of automatically detecting exoplanet transit signals from noisy astronomical light curve data.

**Context:** Transit photometry requires identifying extremely small brightness variations. In **crowded fields**, contamination arises from **stellar blending** (foreground/background sources in the aperture) and **detector noise**. Brightness dips can be a **transiting planet**, an **eclipsing stellar companion (EB)**, or **starspots** — distinct light-curve features that are hard to disentangle in noisy crowded-field data.

**The algorithm must:**
1. Identify datasets with periodic dips potentially mimicking astrophysical phenomena.
2. Classify dips into **transits, eclipses, blends, and other** astrophysical categories.
3. Apply the classifier on provided science datasets and categorize signals.
4. Provide **SNR / significance** of identified events.
5. For transits, estimate **depth, period, duration**.

**Data:**
- TESS raw light curves from MAST (https://archive.stsci.edu/tess/tic_ctl.html); advised to use a sector's high-cadence data (~20–30k stars).
- A **curated labeled dataset** (known exoplanets, false positives, eclipsing binaries, etc.) will be provided for training.

**Tools:** Any public Python libraries; no specialized software needed.

**Expected outcomes:**
- AI pipeline that robustly identifies + classifies dips into astrophysical signals.
- Parameter estimation by light-curve fitting: orbital period, transit duration, transit depth.
- Visualization of the light curve + detected/classified signal.
- Confidence level of the detected signal.
- **Report (max 3 pages):** methodology, assumptions, tools/libraries, uncertainty estimation.

**Evaluation criteria:**
1. Accuracy of event detection + classification.
2. Accuracy of estimated parameters.
3. Methods / approach.
4. Visualization and clarity.

---

## 3. Mapping to existing TRINETRA-X assets

PS7 ≈ the TRINETRA-X spine **plus a learned multi-class classifier and crowded-field/blend handling**.

| PS7 requirement | Reusable TRINETRA-X asset | Status |
|---|---|---|
| Ingest TESS sector light curves | M0 manifest + Stage-0 conditioning (wotan biweight + noise model) — `research/m1_conditioning/` | ✅ reuse |
| Detect periodic dips | Evidence-first detector + period-from-spacing + bootstrap FAP — `src/detector`, `period_recovery` | ✅ reuse |
| SNR / significance | Confirmation gate (folded transit likelihood-ratio at FAR) — `src/confirmation` | ✅ reuse |
| Fit period / depth / duration | M5 (period/epoch) + M6 (depth recovery) — `research/m5_*`, `research/m6_reality_check/` | ✅ reuse |
| Reject eclipsing binaries | M6 EB rejection (12/16) | ⚠️ extend → full multi-class |
| Calibrated confidence | bootstrap/conformal calibration discipline | ✅ ethos in place |
| Benchmark vs TLS | full-TLS comparison harness | ✅ reuse |

**New build for PS7 (only if shortlisted; the 30-h finale):**
- **Multi-class classifier** (transit / eclipse / blend / other) — Hybrid: physics features (depth, duration, odd–even depth difference, secondary-eclipse search, V-shape vs U-shape, ingress/egress, SNR, period) + a **CNN view** on phase-folded (global + local) light curves, ensembled. Trained on the provided curated set.
- **Crowded-field / blend discriminators** — centroid-shift / difference-image proxy, aperture/contamination ratio, odd–even and secondary-eclipse depth, dilution estimate.
- **Visualization** module + **3-page report**.

---

## 4. Discipline / guardrails for this track

- Separate branch (`hackathon/bah2026-ps7`); **never** touch sealed Phase I docs/manifests or the `phase1-prereg-v*` tags.
- Phase I result is reportable as prior work / credibility (real ISRO-context pipeline, benchmarked vs TLS, calibrated confidence, EB rejection demonstrated).
- Keep the physics-first ethos: classifier features are physics-motivated and interpretable; every confidence is calibrated; benchmark/ablate honestly.

## 5. Open items
- [x] Paste the dashboard proposal template fields → finalize proposal to exact format. *(done — web-form + 9-slide PDF deck built)*
- [x] Team filled: **Team TRINETRA-X** — Ansul Suryawanshi (leader, IGNOU), Riddhi Jain (IGNOU), Samiksha Choudhary (Priyadarshini CoE, Hingna, Nagpur). 3 members (valid; 4th optional).
- [ ] **Submit before 2026-07-01:** select PS7, paste Part-A fields, upload `deck/BAH2026_PS7_idea_deck.pdf`.
- [ ] **Curated labeled training dataset — expected in Round 2** (the build phase), per organizer flow. Plugs into `prototype/train_classifier.py` (same interface). Until then we use injected labels (proof-of-path: 0.84 acc).
- [ ] Confirm target TESS sector for the demo (a high-cadence sector with ~20–30k stars) — Round 2.
- [ ] PR #14 left open as the working branch through the hackathon (not merged yet, owner's call).
