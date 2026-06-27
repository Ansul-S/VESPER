# BAH 2026 · PS7 — Hybrid Classifier & Feature Design

> Design doc for the centerpiece deliverable: a 4-class AI classifier
> (**transit / eclipse / blend / other**) + parameter estimation + calibrated confidence.
> Branch `hackathon/bah2026-ps7`. Created 2026-06-26. This is a **design spec**, not code yet.
> Pairs with [`BAH2026_PS7_CHALLENGE.md`](./BAH2026_PS7_CHALLENGE.md) and [`BAH2026_PS7_PROPOSAL_DRAFT.md`](./BAH2026_PS7_PROPOSAL_DRAFT.md).

---

## 0. Why this doc exists
PS7's hardest-graded ask (evaluation criterion #1: detection + **classification accuracy**) is the one piece TRINETRA-X Phase I deliberately never built — it has no learned classifier. This spec de-risks that net-new centerpiece *before* the 30-hour finale, so we design now and implement fast.

---

## 1. The classification problem

Input: a star's conditioned light curve (+ TIC metadata) with one or more detected periodic dips.
Output per candidate: a **class label**, a **calibrated confidence**, an **SNR/significance**, and (for transits) **fitted parameters with uncertainties**.

### Label taxonomy & physical discriminators
| Class | Physical cause | Tell-tale light-curve / metadata signatures |
|-------|----------------|---------------------------------------------|
| **Transit** (planet) | Planet crosses host disk | Shallow (≲ few %), **U-shaped** (flat-ish bottom w/ limb-darkening), **no significant secondary**, **odd–even depths equal**, flat out-of-transit, radius ⇒ depth consistent with planet |
| **Eclipse** (EB) | Stellar companion eclipses | Often **deep** (can be %–tens %), **V-shaped** or has **secondary eclipse**, **odd–even depth difference**, sometimes out-of-eclipse ellipsoidal/reflection variation |
| **Blend** | Eclipse/transit from a *different* star diluted into the aperture | Depth **diluted/inconsistent** with target params, **centroid shift** in/out of event, high **TIC contamination ratio**, possible odd–even or secondary from the true (blended) source |
| **Other** | Starspots / pulsation / systematics / non-astrophysical | **Quasi-periodic / sinusoidal** rather than box-like, **no consistent transit shape**, correlated with momentum dumps/systematics, variable depth/shape epoch-to-epoch |

> Recall priority (carried from TRINETRA-X): the costly error is **calling a real transit something else**. Tune operating points and the confidence/abstention so transit recall is protected; let precision against blends/EBs be the controllable trade.

---

## 2. Architecture — hybrid two-branch + calibration

```
              ┌─────────────────────────────────────────────┐
 conditioned  │  Front-end (REUSE from TRINETRA-X)           │
 light curve  │  detrend → dip detect → period recovery      │
 + TIC meta   │  → phase-fold (global + local views)         │
              └───────────────┬─────────────────────────────┘
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                          ▼
 ┌───────────────────┐                    ┌────────────────────┐
 │ PHYSICS BRANCH    │                    │ DEEP BRANCH        │
 │ feature vector →  │                    │ CNN on global+local│
 │ GBT/RF            │                    │ folded views       │
 │ (interpretable)   │                    │ (morphology)       │
 └─────────┬─────────┘                    └─────────┬──────────┘
           │  class probs                           │ class probs
           └───────────────┬────────────────────────┘
                           ▼
                 ENSEMBLE (weighted avg / stacking)
                           ▼
              CONFORMAL CALIBRATION → class + confidence (+ abstain)
                           ▼
        if transit → CONFIRMATION gate (LR significance) + PARAM FIT
```

Why hybrid: the **physics branch** is interpretable, robust on small/imbalanced labeled data, and directly defensible to scientist judges; the **deep branch** catches subtle morphology (ingress shape, asymmetries) the hand features miss. Ensemble gets accuracy *with* an explainable backbone — a real differentiator vs a bare CNN entry.

---

## 3. Physics-feature branch (the interpretable core)

Extract per candidate (after folding on recovered period). Each feature tagged with the class(es) it discriminates.

**Shape / depth**
- `depth` (ppm) — magnitude of dip. *(transit small vs EB large)*
- `duration` (hr) and `duration/period` — geometry sanity. *(all)*
- `depth_consistency` — observed depth vs depth predicted from TIC stellar radius + plausible companion radius. *(blend/EB vs transit)*
- `V_vs_U_shape` — ratio of ingress/egress slope to flat-bottom length; box-likeness (e.g. fit trapezoid). *(EB V-shape vs transit U-shape)*
- `ingress_egress_ratio` & asymmetry. *(other/systematics)*

**Repetition / phase**
- `odd_even_depth_diff` & its significance — alternating-eclipse test. *(EB/blend tell)*
- `secondary_eclipse_depth` & SNR at phase 0.5 (and scanned phases for eccentric). *(EB/blend tell)*
- `period`, `epoch`, `num_transits`, `SNR_per_transit`, `total_SNR`. *(all)*
- `phase_coverage`, `transit_consistency` (depth scatter across epochs). *(other vs transit)*

**Out-of-transit / variability**
- `oot_rms`, `oot_trend`, autocorrelation/periodogram peak away from transit. *(starspots/pulsation → other)*
- `ellipsoidal/reflection` modulation amplitude at P and P/2. *(EB)*

**Crowding / blend (metadata + pixel proxies)**
- `tic_contamratio` (from TIC) — flux contamination in aperture. *(blend)*
- `centroid_shift` in vs out of event — **if Target Pixel Files available** (see §6). *(blend — strongest single discriminator)*
- `crowdsap`/`flfrcsap`-style dilution if available from the LC product. *(blend)*

→ Feed to **XGBoost/LightGBM** (handles mixed scales, missing values, gives feature importances for the report). Class-imbalance handled with class weights / focal-style weighting; **transit recall weighted up**.

---

## 4. Deep branch (morphology)

- **Representation (AstroNet/ExoNet-style):** two 1-D inputs — a **global view** (whole folded light curve, fixed length, e.g. 2001 bins) and a **local view** (zoom on the transit window, e.g. 201 bins). Median-normalized, depth-normalized.
- **Model:** small 1-D CNN per view (conv blocks → pool) → concat → dense → 4-way softmax. Keep it light (trainable in the finale on a single GPU/Colab).
- **Regularization:** dropout, augmentation by jitter/time-shift/noise injection; mixup optional.
- Output: per-class probabilities, fused with the physics branch.

---

## 5. Ensemble + calibration

- **Ensemble:** start with probability averaging (robust); upgrade to **stacking** (logistic meta-learner on the two branches' probs + a few key physics features) if validation supports it.
- **Calibration (the trust deliverable):** **conformal prediction** (e.g. MAPIE) → prediction *sets* with a guaranteed coverage level, giving a principled per-class confidence and an **abstain/"uncertain"** option when classes overlap. This is the PS7 "confidence level" requirement done rigorously, not a raw softmax.

---

## 6. Blend / crowded-field handling — realistic plan

Honest framing for the judges (and for us): **robust blend rejection often needs pixel-level data.** Tiered plan:
1. **Light-curve-only proxies (always available):** depth-inconsistency vs stellar params, odd–even, secondary eclipse, `tic_contamratio`. Gets us a credible first cut.
2. **Pixel-level (if time / TPFs downloaded):** in-/out-of-transit **difference imaging** + **centroid offset** via `lightkurve` Target Pixel Files — the gold-standard blend discriminator. Frame as the strong-version feature; include if the finale time budget allows.
3. **Report limitation explicitly:** state where LC-only blend ID is fundamentally ambiguous. Honest uncertainty reporting *scores* (evaluation criterion #3, methods) and avoids overclaiming.

---

## 7. Parameter estimation (transit class)

- **Period:** recovered period + **bootstrap FAP** error (reuse TRINETRA-X).
- **Depth & duration:** fit a transit model (`batman`) or trapezoid; uncertainties from least-squares covariance, upgraded to **MCMC** posteriors (emcee) for the small science set if time allows.
- Report **value ± uncertainty** for period, depth, duration (PS7 expected outcome).

---

## 8. SNR / significance
- Per-transit and total **SNR** from depth / per-point noise × √N_in-transit.
- **Significance** from the confirmation gate: folded transit-model **likelihood-ratio** vs flat, calibrated to a FAR (reuse TRINETRA-X confirmer).

---

## 9. Training data plan
- **Primary:** the organizer's **curated labeled set** (planets / false positives / EBs / …) — *not yet in hand; obtain ASAP*.
- **Augmentation:** **injection–recovery into real conditioned light curves** (reuse TRINETRA-X M2) to (a) balance classes, (b) generate transits/EBs/blends with known params, (c) validate parameter-fit accuracy and uncertainty calibration on ground truth.
- **Splits:** leakage-safe train / val / **held-out test** by star (never split one star across sets). **No tuning on the science/test data** (carry TRINETRA-X anti-tuning discipline). Thresholds/operating point set on val, then frozen.

---

## 10. Evaluation (aligned to PS7 criteria)
| PS7 criterion | Our metric |
|---|---|
| Detection + classification accuracy | Per-class precision/recall/F1, **confusion matrix**, macro-F1; **transit recall** highlighted |
| Parameter accuracy | Median |Δ|/true for period, depth, duration on injection ground truth; coverage of error bars |
| Methods/approach | Ablation: physics-only vs CNN-only vs hybrid; feature importances; calibration curve |
| Visualization & clarity | §11 |

## 11. Visualization deliverable
Per-candidate **report card**: raw LC (events marked) · phase-folded LC + model fit · predicted **class + confidence bar** · fitted **params table** · **SNR**; plus a global **confusion matrix** and **calibration plot** for the science set.

---

## 12. Reuse map (what comes from TRINETRA-X, what's new)
| Module | Source |
|---|---|
| Conditioning (wotan detrend + noise model) | REUSE `research/m1_conditioning/` |
| Dip detection + period recovery + bootstrap FAP | REUSE `src/detector`, `period_recovery` |
| Confirmation gate (LR significance) | REUSE `src/confirmation` |
| Injection–recovery (labeled augmentation) | REUSE `research/m2_injection/` |
| Parameter fit (depth/period/epoch) | REUSE/EXTEND M5/M6 |
| **Phase-folded global+local views** | **NEW** |
| **Physics-feature extractor (§3)** | **NEW** |
| **GBT + CNN branches + ensemble + conformal** | **NEW** |
| **Blend/centroid features** | **NEW** |
| **Visualization report cards** | **NEW** |

## 13. Risk register
| Risk | Mitigation |
|---|---|
| Labeled set late/small/imbalanced | Injection–recovery augmentation; class weights; conformal abstain |
| Blend ID weak from LC alone | Tiered plan §6; report limitation honestly |
| CNN overfits in finale | Keep small; heavy augmentation; lean on physics branch |
| 30-h time crunch | Physics branch + spine first (works standalone); CNN/ensemble as upgrade; pre-build skeleton now |
| Class confusion EB↔transit | Odd–even + secondary + depth-consistency features explicitly target it |

## 14. 30-hour finale execution sketch (if shortlisted)
1. **H0–4:** data pull (sector + TIC) + conditioning on a star batch (spine reuse).
2. **H4–10:** feature extractor + GBT branch trained on curated set → first working classifier + confusion matrix.
3. **H10–18:** CNN branch (global+local) + ensemble + conformal calibration.
4. **H18–24:** parameter fitting + SNR + (time-permitting) centroid/blend pixel features.
5. **H24–28:** run on the provided science set; visualizations + report cards.
6. **H28–30:** 3-page report + presentation polish.

---

*Design spec only — no code committed yet. Implementation begins if shortlisted (or earlier for a local smoke-test prototype, owner's call).*
