# TRINETRA-X — Architecture for the ISRO Exoplanet Challenge (2026)

**Premise:** all prior code is deleted. We keep only the *scientifically valid concepts* from `TRINETRA_CONCEPT_RECONSTRUCTION.md` and rebuild on a modern (2026) stack for **TESS** light curves.

### What we keep (philosophy) vs. what we discard (implementation)

| TRINETRA concept | Status in TRINETRA-X |
|---|---|
| Evidence-first: find events before assuming a period | **Keep** — but as a *learned* detector, and only as a **trigger** |
| Route by *observed evidence strength*, not by (unknown) planet type | **Keep** — core triage |
| Fast path for the easy majority, full search only for the hard minority | **Keep** |
| Recall is sacred; push precision downstream | **Keep** |
| Period from event spacing | **Keep, but calibrated** (false-alarm probability + look-elsewhere correction) |
| **Photometric significance is the arbiter, not timing coincidence** | **Keep — and promote it to the GATE** (the central fix) |
| Matched filter + MAD threshold | *Discard* → learned local detector |
| Uncalibrated Hough score as verdict | *Discard* → physics-confirmation gate + conformal confidence |
| Circular SNR; even/odd via unsorted interp; detrend across segments | *Discard* → real transit-fit SNR; correct binned vetting; per-sector detrend |
| Validate against uniform-random noise | *Discard* → injection-recovery into **real** TESS light curves |

**Founding principle, corrected:** *start with evidence — but let **photometric significance (depth, shape, repetition)**, not the coincidence of event times, decide what counts as evidence.*

---

## 1. ARCHITECTURE DIAGRAM

```
                          ┌──────────────────────────────────────────────┐
                          │  TIC / stellar catalog (Teff, R*, mag,        │
                          │  contamination ratio, crowding)               │
                          └───────────────┬──────────────────────────────┘
                                          │ (conditioning + features at every stage)
   TESS SPOC 2-min PDCSAP                 │
   (+ QLP/TESS-SPOC FFI)                  ▼
        │            ┌─────────────────────────────────────────────────────────┐
        ▼            │ STAGE 0 — TESS-aware conditioning                         │
 ┌───────────────┐   │  • per-SECTOR detrend (GP/biweight) — never across seams │
 │ raw + quality │──▶│  • mask momentum dumps (~2.5 d), scattered-light, flags  │
 │ flags         │   │  • normalize; keep raw copy for the confirmation fit     │
 └───────────────┘   └───────────────┬─────────────────────────────────────────┘
                                      ▼
                     ┌─────────────────────────────────────────────────────────┐
                     │ STAGE 1 — LEARNED LOCAL DETECTOR  (evidence trigger, GPU) │
                     │  1D U-Net/TCN → per-cadence p(transit-shape)              │
                     │  self-supervised pretrain → fine-tune on injections      │
                     │  OUT: event times {tᵢ} + local confidence  (high recall) │
                     └───────────────┬─────────────────────────────────────────┘
                                     │  evidence strength?
                 ┌───────────────────┼─────────────────────┬───────────────────┐
        strong ≥2 events      single strong event       weak / none            │
                 ▼                   ▼                       ▼                   │
   ┌──────────────────────┐ ┌──────────────────┐  ┌────────────────────────┐   │
   │ STAGE 2 — PERIOD      │ │ MONOTRANSIT path │  │ FALLBACK: full BLS/TLS │   │
   │ INFERENCE (calibrated)│ │ (TESS-critical): │  │ or SPOC-DV on the      │   │
   │  weighted phase       │ │ no period; fit   │  │ HARD MINORITY only     │   │
   │  coherence / BLS-on-  │ │ single event,    │  └───────────┬────────────┘   │
   │  events + bootstrap   │ │ duration, depth  │              │                │
   │  FAP + look-elsewhere │ └────────┬─────────┘              │                │
   └───────────┬──────────┘          │                        │                │
               └──────────┬──────────┴────────────────────────┘                │
                          ▼                                                     │
   ┌───────────────────────────────────────────────────────────────────────┐  │
   │ STAGE 3 — PHYSICS CONFIRMATION  ◀── THE GATE (photometric significance) │  │
   │  differentiable transit model (Mandel-Agol + limb darkening, jaxoplanet)│  │
   │  fit {P, t0, depth, duration, b} → POSTERIORS (NumPyro HMC)             │  │
   │  significance = ΔBIC / transit-fit SNR vs flat;  require shape+repeat   │  │
   │  emit vetting views: odd/even (binned, sign-aware), secondary, centroid │  │
   └───────────────┬───────────────────────────────────────────────────────┘  │
                   │ pass significance gate                                     │
                   ▼                                                            │
   ┌───────────────────────────────────────────────────────────────────────┐  │
   │ STAGE 4 — ML CLASSIFIER / FP REJECTION  (ExoMiner-style multi-branch)   │◀─┘
   │  inputs: global view · local view · odd/even view · secondary view ·    │
   │  centroid/diff-image · scalar features (stellar, contamination, FAP,    │
   │  fit diagnostics, routing-path id)                                      │
   │  OUT: p(planet) and p(EB / BEB / variable / systematic)                 │
   └───────────────┬───────────────────────────────────────────────────────┘
                   ▼
   ┌───────────────────────────────────────────────────────────────────────┐
   │ STAGE 5 — CALIBRATED CONFIDENCE                                         │
   │  deep ensemble + MC-dropout (epistemic) → temperature scaling →         │
   │  CONFORMAL prediction (distribution-free coverage) + abstain zone       │
   └───────────────┬───────────────────────────────────────────────────────┘
                   ▼
   ┌───────────────────────────────────────────────────────────────────────┐
   │ STAGE 6 — RANKED OUTPUT                                                 │
   │  per candidate: P±σ, duration±σ, depth±σ, t0; p(planet)+conf. interval; │
   │  FP-class probs; vetting flags; monotransit flag; completeness context  │
   └───────────────────────────────────────────────────────────────────────┘
```

**Two-speed by design (the triage):** Stages 1→2→3→4 are the *fast path* for stars with local evidence; the full BLS/TLS/DV fallback runs only for the minority with none. Stellar-catalog features and the routing-path id are injected everywhere — directly addressing the genesis-era "domain shift across paths" concern by making the path an explicit feature.

---

## 2. DATA FLOW

```
INGEST        SPOC 2-min PDCSAP_FLUX (primary) + QLP/TESS-SPOC FFI (faint/extra targets)
              + TIC stellar params + data-quality flags                 [per star, per sector]
   │
CONDITION     per-sector GP detrend (celerite2) → mask(momentum dumps, scattered light,
              quality!=0) → normalize → {detrended LC, raw LC, mask, σ-estimate}
   │
DETECT        batched on GPU: LC → 1D U-Net/TCN → p_transit(t) → peak-pick + cluster
              → event list {tᵢ, conf_i, local_depth_i, local_dur_i}
   │
ROUTE         n_events≥2 → PERIOD ; n_events==1 (strong) → MONOTRANSIT ; else → FALLBACK
   │
PERIOD        events → weighted phase-coherence/BLS-on-events → P̂, plus bootstrap null
              (scramble event times) → FAP(P̂) with multi-period (look-elsewhere) correction
   │
CONFIRM       seed P̂ (or single event) → differentiable transit fit on the RAW LC →
              posteriors {P,t0,δ,T14,b,u}; significance Δ; build phase-folded + diagnostic views
              GATE: keep iff significance≥threshold AND shape consistent AND (repeats OR strong mono)
   │
CLASSIFY      views + scalars → multi-branch net → {p_planet, p_EB, p_BEB, p_var, p_sys}
   │
CALIBRATE     ensemble/MC-dropout → temp-scale → conformal set → {p_planet, [lo,hi], decision∈
              {PLANET, FALSE-POSITIVE, REVIEW/ABSTAIN}}
   │
RANK/EMIT     sort by p_planet·significance; attach parameter posteriors + completeness for that
              (P, depth, mag) cell → challenge submission + human-review queue
```

Provenance is carried end-to-end (raw LC, mask, fit posteriors, every view) so any verdict is auditable — a hard lesson from the prior version, where the decision-relevant photometry was discarded before the decision.

---

## 3. MODEL SELECTION

| Stage | Model | Why this choice (2026) |
|---|---|---|
| **0 Conditioning** | `wotan` biweight / `celerite2` Gaussian-process detrend; quality-flag & momentum-dump masking | GP captures stellar variability without eating transits; **per-sector** application avoids the seam artifacts that plagued the old pipeline. |
| **1 Local detector** | 1D **U-Net / Temporal Conv Net (TCN)** doing per-cadence transit-shape segmentation; **self-supervised pretraining** (masked reconstruction / contrastive on unlabeled TESS) | Per-cadence segmentation is the right primitive for "where are the events?"; pretraining exploits the huge unlabeled TESS corpus; GPU-batched O(N) gives the scaling. Naturally emits **single-transit** events (TESS monotransits) that BLS/TLS underperform on. |
| **2 Period inference** | Weighted phase-coherence / **BLS-restricted-to-event-times** + **bootstrap false-alarm probability** | Cheap (sparse events), and — unlike the old Hough score — it ships a **calibrated FAP** with look-elsewhere correction, so coincidence can't masquerade as detection. |
| **3 Confirmation (GATE)** | **Differentiable transit model** (Mandel–Agol + limb darkening) via `jaxoplanet`; posteriors with **NumPyro HMC** | Produces **period/duration/depth *with uncertainties*** (a hard requirement) and a *physical* significance — the arbiter the prior design lacked. |
| **4 Classifier / FP rejection** | **ExoMiner-style multi-branch DNN** (global + local + odd/even + secondary + centroid/diff-image branches, fused with scalar stellar/diagnostic features) | NASA-validated template for transit vetting; the multi-view inputs are exactly the discriminants for EB/BEB/variable/systematic. |
| **5 Confidence** | **Deep ensemble + MC-dropout** (epistemic) → **temperature scaling** → **conformal prediction** | Distribution-free coverage guarantee + an explicit **abstain** region → trustworthy, competition-grade confidence rather than an uncalibrated score. (Evidential DL is a lighter-weight fallback.) |
| **Fallback** | Standard **TLS** (+ SPOC-DV diagnostics) on the minority | Keep the proven exhaustive search for stars with no local evidence — recall insurance. |

**Minimum-viable core** (if time/compute is tight for the challenge): Stage 0 + a Stage-1 CNN detector + Stage-3 TLS-seeded fit + a single-model Stage-4 classifier with temperature scaling. The full design adds self-supervision, posteriors, ensembles, and conformal calibration.

---

## 4. TRAINING STRATEGY

**Label sources.** TOI catalog (confirmed planets + known false positives), TESS EB catalogs, stellar-variability samples, and SPOC TCEs. These are scarce and imbalanced → augment heavily with injections.

1. **Self-supervised pretraining (detector).** Mask spans of unlabeled TESS light curves and reconstruct (or contrastive learning with physically-motivated augmentations: jitter, momentum-dump injection, scattered-light ramps, variability). Learns a robust representation of "normal" stellar behavior before ever seeing a transit.
2. **Injection-recovery as the primary training signal.** Inject **physical** transits (Mandel–Agol, sampled over P, Rp, b, limb-darkening) into **real** TESS light curves — preserving genuine correlated noise. This (a) trains the detector with realistic positives, (b) yields the completeness map for free, and (c) **fixes the prior validation flaw** (which used uniform-random noise).
3. **Hard-negative mining.** EBs and BEBs are the adversaries — over-sample them; mine the classifier's confident mistakes and re-train. Secondary eclipses, V-shapes, and centroid shifts are the features that separate them.
4. **Domain-shift handling (the genesis concern, finally addressed).** Train the classifier on candidates drawn from **all routing paths** (fast / monotransit / fallback) and feed the **routing-path id** as a feature, so one classifier generalizes across the three statistical regimes.
5. **Calibration split.** Hold out a dedicated calibration set (never used for training) for temperature scaling and conformal quantiles — coverage guarantees are only valid on exchangeable held-out data.
6. **Leakage-safe validation.** Split by **sky region / sector**, not randomly, so the same star/blend can't appear in train and test. Report cross-sector generalization explicitly.
7. **Loss & objective.** Detector: focal/Dice segmentation loss (rare-positive). Classifier: class-balanced focal loss; optimize **recall at fixed high precision** (challenge-aligned), not raw accuracy.

---

## 5. EVALUATION METRICS

**Detection (Stage 1–3), from injection-recovery into real LCs:**
- **Completeness (recall)** as a 2-D map over (period, depth/Rp) and over (#transits, magnitude) — the honest deliverable, not a single number.
- **Reliability / precision** and recovered-**period accuracy** (|P̂−P|/P within tolerance, harmonics scored).
- **Monotransit recovery rate** (TESS-specific strength).

**Classification / FP rejection (Stage 4):**
- **AUC-PR** (precision-recall; the right curve under heavy class imbalance) and **recall @ 99% precision**.
- **Per-class confusion** across {planet, EB, BEB, variable, systematic}.

**Parameter estimation (Stage 3):**
- Residual χ²; and crucially **posterior calibration / coverage** — do the 1σ intervals for P, depth, duration contain truth ~68% of the time?

**Confidence (Stage 5):**
- **Expected Calibration Error (ECE)** + reliability diagrams.
- **Conformal coverage vs nominal** (e.g., 90% sets contain truth ≥90%) and **abstention rate**.

**System-level:**
- **Recall at the ISRO challenge's scoring metric** (primary).
- **Throughput** (stars / GPU-hour) and **fast-path fraction** — to substantiate the scaling claim.
- **Head-to-head vs BLS/TLS + standard vetting on the identical injection set** — same noise, same stars, paired comparison.

---

## 6. EXPECTED ADVANTAGES OVER STANDARD BLS/TLS PIPELINES

1. **Scaling.** A GPU-batched learned detector is O(N) per star and folds **only seeded** periods; full search is reserved for the minority — orders-of-magnitude higher throughput at fixed recall.
2. **Single-transit / monotransit sensitivity (decisive for TESS).** 27-day sectors give long-period planets only 1–2 transits; evidence-first detection finds them as individual events, where BLS/TLS — which need several folded transits — systematically weaken.
3. **Model-agnostic detection.** A learned shape detector flags asymmetric, TTV-jittered, or otherwise non-box transits that BLS's box / TLS's fixed template miss by construction.
4. **Integrated, calibrated decisioning.** BLS/TLS output an SDE and stop. TRINETRA-X outputs **p(planet) with a distribution-free confidence interval**, an explicit **false-positive class**, and an **abstain** option — turning detection into a trustworthy, reviewable verdict.
5. **Parameters with uncertainty.** Physics-model **posteriors** for P, duration, depth (and b, limb darkening) — not point estimates — enabling principled downstream science.
6. **Honest, noise-faithful validation.** Completeness measured by injection into **real** TESS noise gives a defensible recall map; the prior approach's optimism (validation against uniform noise) is structurally avoided.
7. **Recall-first with a real gate.** High-recall triage up front, but **photometric significance** (not timing coincidence) as the arbiter — capturing TRINETRA's philosophy while closing the exact loophole that made the previous version manufacture false positives.

---

*Design only — no code. Implementation would begin with the Stage-0 conditioning + Stage-1 detector on a single well-studied TESS sector as a vertical slice.*
