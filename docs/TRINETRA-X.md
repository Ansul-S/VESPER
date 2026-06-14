# TRINETRA-X

### Evidence-First Exoplanet Discovery for the TESS Era

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Status** | Research Program Initialization |
| **Author** | Vesper |
| **Codename** | TRINETRA-X |

---

## Mission

TRINETRA-X is a next-generation AI-assisted exoplanet detection framework designed to identify planetary transit signals in noisy astronomical light curves while minimizing computational cost and maximizing scientific reliability.

The project is built around a single core principle:

> Detection should start with evidence, not hypothesis.

Traditional exoplanet search pipelines evaluate thousands of possible orbital periods for every star regardless of whether any evidence of a transit exists.

TRINETRA-X reverses this process. It first searches for localized evidence of transit-like events and only performs expensive orbital searches and transit modeling when evidence warrants further investigation.

The objective is to create a scalable exoplanet discovery architecture capable of processing large-scale TESS datasets while preserving scientific rigor.

---

## Core Scientific Hypothesis

If a meaningful fraction of exoplanet transits generate locally detectable transit signatures, then:

1. Transit evidence can be detected before orbital period estimation.
2. Orbital periods can be inferred from event spacing.
3. Expensive transit searches can be restricted to a minority of stars.
4. Computational cost can be reduced substantially while maintaining comparable recall.

---

## Research Objectives

### Primary Objective

Demonstrate that evidence-first routing can reduce computational cost without significantly reducing exoplanet detection recall.

### Secondary Objectives

Develop a robust AI pipeline capable of:

- Detecting transit-like events in noisy TESS light curves
- Classifying astrophysical signals
- Rejecting false positives
- Estimating orbital parameters
- Providing calibrated confidence estimates
- Scaling to tens of thousands of stars

---

## Scientific Philosophy

### Principle 1 — Evidence Before Hypothesis

Do not search every possible orbital period first. Search for observable evidence first.

### Principle 2 — Photometry Is The Judge

Timing coherence alone is insufficient. A candidate becomes a planet candidate only after demonstrating:

- Transit depth
- Transit shape
- Repeatability
- Statistical significance

### Principle 3 — Recall Is Sacred

The system must prefer:

| Outcome | Verdict |
|---------|---------|
| False Positive | Acceptable |
| False Negative | Dangerous |

Unknown planets must never be discarded simply to improve precision.

### Principle 4 — Route By Evidence Strength

Never route based on planet type. Planet type is unknown. Route based on observable evidence.

---

## System Architecture

### Stage 0 — TESS Conditioning

**Input:**
- TESS PDCSAP Flux
- Quality Flags
- TIC Metadata

**Tasks:**
- Sector-aware detrending
- Noise estimation
- Artifact masking
- Normalization

**Output:** Clean light curve representation.

---

### Stage 1 — Evidence Detector

**Purpose:** Identify local transit-like events without assuming an orbital period.

**Methods:**
- 1D U-Net
- Temporal CNN
- Self-supervised representation learning

**Output — Event candidates:**

```
Time
Depth
Duration
Confidence
```

---

### Stage 2 — Period Inference

**Purpose:** Recover orbital periods from event spacing.

**Methods:**
- Sparse event analysis
- Phase coherence
- Event-space BLS
- Bootstrap significance estimation

**Output:**

```
Period
False Alarm Probability
Confidence
```

---

### Stage 3 — Physics Confirmation

> **Critical Decision Gate**

Transit candidates are validated using physical transit models.

**Methods:**
- Mandel–Agol Transit Models
- JAX-based fitting
- Bayesian inference
- Posterior estimation

**Outputs:**

```
Period
Depth
Duration
Impact Parameter
Transit Significance
```

Only candidates passing this gate continue.

---

### Stage 4 — Astrophysical Classification

**Purpose:** Determine the nature of detected signals.

**Classes:**
- Exoplanet
- Eclipsing Binary
- Background Eclipsing Binary
- Stellar Variability
- Instrumental Artifact

**Methods — Multi-branch neural networks using:**
- Local views
- Global views
- Phase folded curves
- Odd-even transit analysis
- Centroid diagnostics

---

### Stage 5 — Confidence Calibration

**Purpose:** Produce trustworthy probabilities.

**Methods:**
- Deep Ensembles
- Monte Carlo Dropout
- Temperature Scaling
- Conformal Prediction

**Outputs:**

```
Planet Probability
Confidence Interval
Abstain Decision
```

---

## Dataset Strategy

### Source Data

**Primary:**
- TESS 2-minute cadence light curves

**Secondary:**
- TESS Full Frame Images

**Auxiliary:**
- TIC Catalog
- TOI Catalog
- Eclipsing Binary Catalogs

### Validation Sets

| Set | Target |
|-----|--------|
| Confirmed Planets | 500+ |
| False Positives | 200+ |
| Null Stars | 500+ |

---

## Evaluation Framework

### Detection Metrics
- Recall
- Precision
- Period Recovery Accuracy
- Completeness Maps

### Classification Metrics
- PR-AUC
- Recall at Fixed Precision
- Confusion Matrix

### Parameter Metrics
- Depth Error
- Duration Error
- Period Error

### Calibration Metrics
- Expected Calibration Error
- Reliability Curves
- Conformal Coverage

### System Metrics
- Runtime per Star
- Throughput
- GPU Hours
- Fast Path Fraction

---

## Success Criteria

| Level | Criteria |
|-------|----------|
| **Minimum** | Comparable Jupiter-class recall · Significant runtime reduction · Stable false positive control |
| **Target** | Match or exceed TLS recall on large planets · Detect monotransits effectively · Operate at substantially lower compute cost |
| **Stretch Goal** | Establish a new paradigm for large-scale exoplanet search |

---

## Research Milestones

### Phase I — Scientific Validation

**Goal:** Prove evidence-first routing works.

**Deliverables:**
- Benchmark Dataset
- Baseline Comparisons
- Initial Recall Curves

### Phase II — AI Pipeline

**Goal:** Build full TRINETRA-X architecture.

**Deliverables:**
- Detector
- Period Recovery
- Transit Confirmation

### Phase III — Classification

**Goal:** Robust astrophysical categorization.

**Deliverables:**
- Planet Classifier
- False Positive Rejection

### Phase IV — Publication

**Goal:** Produce publishable scientific results.

**Deliverables:**
- Validation Study
- Benchmark Results
- Research Paper

---

## Non-Negotiable Rules

1. No tuning on test data.
2. Every claim must be benchmarked.
3. Every confidence score must be calibrated.
4. Every experiment must be reproducible.
5. Physics overrides heuristics.
6. Evidence overrides assumptions.
7. Recall is more important than elegance.

---

## Project Motto

> Find evidence first.
>
> Spend computation second.
>
> Let physics decide.
