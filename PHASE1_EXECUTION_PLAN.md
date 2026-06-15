# TRINETRA-X — Phase I Execution Plan

| Field | Value |
|-------|-------|
| **Document** | Phase I Execution Plan |
| **Increment** | **v0.1 — M0 only** (Manifest Freeze & Leakage-Safe Split) |
| **Created** | 2026-06-15 |
| **Status** | **APPROVED** to start M0 (owner approval in-session, 2026-06-15); **no data read; M0 not started** |
| **Authority** | Subordinate to the sealed pre-registration. This plan **executes** the protocol; it does **not** change it. |
| **Governs** | Ordered work to realize milestone **M0** of the sealed Phase I protocol |

> **What this document is.** An execution artifact that turns the sealed Phase I protocol into an ordered, checkable work plan. It is *not* a specification and carries **no normative authority** over the experiment. Where this plan and any sealed document differ, the **sealed document governs**.
>
> **What this increment covers.** **M0 only** — freeze the TESS sector/target manifest and the leakage-safe calibration/test split. M1–M7 appear once, as a non-binding forward map (§2), and are deferred to their own planning increments. This plan does **not** redesign the experiment, introduce Phase II machinery, download data, or write implementation code.

---

## 0. Binding inputs (sealed; immutable)

This plan is derived from and bound by the three sealed documents (git tag **`phase1-prereg-v2`**, commit `723087e`):

| Sealed document | Version | SHA-256 (DR-001) |
|---|---|---|
| `docs/SCIENTIFIC_HYPOTHESIS.md` | v2.0 | `6adae7f1…26680f5e` |
| `docs/TRINETRA_X_PHASE1_VALIDATION.md` | v2 (incl. Appendix A) | `441b2c94…b8846b40` |
| `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` | v1.1 | `4f8d95c6…82034537` |

Decision context: [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md) (DR-001).

**Non-negotiables carried into every task below:** (1) recall > precision; (2) **no tuning on test data**; (3) physics decides detection; (4) every metric benchmarked against full TLS; (5) every confidence calibrated; (6) reproducible by construction.

---

## 1. Plan-wide guardrails (apply to all milestones)

| # | Guardrail | Source |
|---|-----------|--------|
| G1 | **The TEST set is sealed at M0 and is not inspected until the single M4 run.** No statistic, plot, or count is computed on TEST rows before M4. | VAL §7; HYP §7 |
| G2 | **No thresholds are set in M0.** All calibration-derived values (`z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP`) are derived on the CALIBRATION set at **M3** and hashed before M4. M0 freezes *which stars*, never *how significant*. | VAL App. A (two-step freeze), A.10 |
| G3 | **Manifest decisions are outcome-independent.** Every inclusion/exclusion/split rule is fixed from catalog metadata and pre-registered reasoning — never from any detection or recovery outcome. | VAL §7; HYP §5 (A6) |
| G4 | **Sealed documents are immutable.** Any change to a frozen parameter requires a new, re-dated pre-registration, not an edit here. | CLAUDE.md; VAL preamble |
| G5 | **Reproducible by construction.** Catalog versions, query timestamps, tool/library versions, and RNG seeds are pinned and recorded in the manifest; the manifest is content-hashed (the **M0 seal**). | VAL App. A.10; non-negotiable #6 |
| G6 | **No clean-skip / survey-scale skipping is designed or built.** That mechanism is Phase II. M0 may *enable measurement* of the survey-representative frontier (E3) but builds none of its routing. | VAL §8; HYP §10; DR-001(c) |

---

## 2. Forward milestone map (non-binding context — NOT part of this increment)

Shown only so M0 sits in context. **Each of M1–M7 is deferred to its own planning increment** and is subordinate to the sealed protocol; the one-line descriptions below are an indicative reading of the protocol's stages, not new design.

| Milestone | One-line scope | First/second seal |
|-----------|----------------|-------------------|
| **M0** | **Manifest freeze + leakage-safe calibration/test split** ← *this increment* | **Seal #1: manifest hash** |
| M1 | Stage-0 conditioning (per-sector detrend + masking) over the manifest pool (VAL A.9) | — |
| M2 | Injection–recovery harness; the simple **untrained** detector; period-from-spacing; shared TLS engine (both arms); transit-preservation η-check (VAL §4.2, pre-M3 gate) | — |
| M3 | **Calibration**: derive + freeze thresholds on the CALIBRATION set; compute manifest hash (VAL A.10) | **Seal #2: threshold manifest hash** |
| M4 | **Single sealed TEST run** (one evaluation) → primary endpoints **E1, E2** | — |
| M5 | Survey-representative compute **E3** + break-even `π⋆` frontier (secondary) | — |
| M6 | Reality-check on real labels (TOIs / EBs); calibration & coverage diagnostics (H4/H5); monotransit sub-analysis (H3) | — |
| M7 | Analysis → verdict (**VALIDATED / FALSIFIED / INCONCLUSIVE**) → write-up | — |

---

## 3. Milestone M0 — Manifest Freeze & Leakage-Safe Split

### 3.1 Objective

Produce a single, frozen, content-hashed **manifest** that fixes — before any light-curve photometry is analyzed and before any threshold is set — exactly which TESS observations and target stars enter Phase I, and how they are partitioned into a leakage-safe **CALIBRATION** set and a sealed **TEST** set. The manifest is the reproducible substrate on which M1–M7 run.

### 3.2 Boundary — what M0 does and does NOT do

**M0 does:** select + freeze sectors; build the target manifest from **catalog/metadata** (TIC, SPOC 2-min product availability, sky coordinates, stellar parameters, per-target baseline); pin label catalogs (TOIs, EBs); construct the leakage-safe split; verify feasibility against the frozen injection grid and power requirement; pin provenance; compute the manifest hash (Seal #1).

**M0 does NOT:** download or condition light-curve flux (M1); run the detector, period inference, or TLS (M2+); inject transits (M2+); set or estimate any threshold (M3); inspect the TEST set (M4); touch the sealed specification documents; build any clean-skip/survey-scale routing (Phase II).

> **Data-touching note.** M0 is the first milestone that queries data **archives**, but it operates on **catalog metadata** (target lists, coordinates, stellar params, label catalogs, product availability). Bulk light-curve retrieval and conditioning begin at **M1**. The leakage-safe split needs only TIC IDs and sky coordinates, not photometry.

### 3.3 Dependencies

| Dependency | Status |
|------------|--------|
| Pre-registration seal `phase1-prereg-v2` cut (anti-tuning freeze precedes any data touch) | ✅ DONE (commit `723087e`) |
| `references.bib` with Kunimoto & Matthews (2020) — load-bearing for occurrence prior (A.5) and π̂ (A.6) | ⬜ Non-blocking follow-on; pin the citation in the manifest provenance |
| Approval of this plan by the project owner | ⬜ Pending (gates start of M0) |

M0 has **no** dependency on any threshold value (those are M3) and **must not** anticipate one (G2).

### 3.4 Sub-milestone decomposition

Ordered M0.1 → M0.6. Each lists tasks, the sealed clause it satisfies, dependencies, and its deliverable.

---

#### M0.1 — Sector selection & freeze

*Satisfies:* VAL §3 ("Source"; FFI/QLP excluded). *Depends on:* plan approval.

- **T0.1.1** Choose the fixed list of TESS **SPOC 2-minute** sectors for Phase I. Selection criterion is **outcome-independent**: prioritize sectors whose observing baseline maximizes the fraction of injection-grid cells reaching `n_transits ≥ 2` (so the §6 power requirement is attainable). FFI/QLP products are excluded to remove a pipeline confound.
- **T0.1.2** Record the rationale and the exact sector identifiers in the manifest. The sector list is **frozen** once recorded.

**Deliverable D0.1:** frozen sector list + selection rationale (manifest §Sectors).

---

#### M0.2 — Target pool construction (metadata manifest)

*Satisfies:* VAL §3 (source, splits); VAL §4.2 / A.1 / A.9 (injections need stellar params); HYP §5 (A1, A2, A4 checkable). *Depends on:* M0.1.

- **T0.2.1** Enumerate all stars with **SPOC 2-min PDCSAP_FLUX** availability in the frozen sectors (archive product-availability query — metadata only).
- **T0.2.2** Apply **pre-registered, outcome-independent** inclusion/exclusion criteria (e.g., 2-min cadence present; data-quality availability; documented stellar/crowding bounds). Each criterion and its threshold is **recorded and justified before application** (G3). No criterion may reference any detection outcome.
- **T0.2.3** Cross-match the **TIC** for the fields downstream stages require, and record per target:
  - sky coordinates (RA/Dec) and **camera/CCD + sector pointing** (for leakage blocking, M0.4);
  - stellar radius `R⋆`, limb-darkening inputs, `Tmag` (for Mandel–Agol injections with LD from stellar params, VAL §3 / A.1);
  - **observing baseline** per target (for the `n_transits` axis and feasibility, M0.5).
- **T0.2.4** Flag known **multi-planet** systems (assumption A9 scope) and any flagged-TTV systems (A10) so they can be reported separately and excluded from the single-planet headline.

**Deliverable D0.2:** candidate target manifest with per-target metadata + applied inclusion/exclusion criteria (manifest §Targets). *No flux downloaded.*

---

#### M0.3 — Label & truth-set assembly

*Satisfies:* VAL §3 (reality-check; "known-TOI-removed" survey sample; null calibration stars); VAL §4.2 / A.2 (FAR on null stars); HYP §5 (A5), H4. *Depends on:* M0.2.

- **T0.3.1** Pin and **version** the catalogs restricted to the frozen sectors:
  - **confirmed TESS planets / TOIs** (the reality-check planet labels);
  - **known false positives** — eclipsing binaries (EB/BEB), variables, systematics (the reality-check FP labels).
- **T0.3.2** Define the **null (planetless) pool** as the target pool with all known planet hosts and known FPs removed — used for FAR/threshold calibration (M3) and the survey-representative remainder. Record the catalog incompleteness caveat: residual undetected planets in "null" stars bound H4 calibration and are **reported, not hidden**.
- **T0.3.3** Record the four logical sub-samples drawn from the pool (assigned to splits in M0.4): **(a)** injection-recovery hosts, **(b)** null/FAR stars, **(c)** reality-check labeled stars, **(d)** survey-representative mixed sample (π̂ fraction injected, remainder known-TOI-removed).

**Deliverable D0.3:** versioned label tables + null-pool definition + sub-sample roster (manifest §Labels).

---

#### M0.4 — Leakage-safe calibration/test split

*Satisfies:* VAL §3 (disjoint by sky region / TIC; **no training split**); VAL §7; HYP §5 (A6). *Depends on:* M0.2, M0.3.

- **T0.4.1** Partition the target pool into **CALIBRATION** and **TEST**, **disjoint by TIC** *and* **blocked by sky region** (whole spatial blocks — e.g., camera/CCD footprint or HEALPix cells — assigned entirely to one side) so that no shared instrumental systematic (same CCD column, same sector pointing) bridges the two sets. **No training split** is created (the detector is untrained).
- **T0.4.2** Fix and record the blocking scheme, the **split ratio**, and the **RNG seed**. The split ratio is an M0 pre-registration parameter, chosen so CALIBRATION holds enough null stars for stable threshold estimation (M3) and TEST holds enough hosts to reach the §6 sample size; the chosen value is recorded before any analysis.
- **T0.4.3** Assign all four sub-samples (M0.3 T0.3.3) **consistently** under the single split, so the TEST seal is global (a star is calibration-or-test in every role).
- **T0.4.4** **Leakage audit:** verify zero shared TIC across sets; verify spatial/camera-CCD separation; report residual adjacency risk. Audit result recorded in the manifest.

**Deliverable D0.4:** CALIBRATION/TEST split tables + leakage-audit report (manifest §Split).

---

#### M0.5 — Feasibility & power coverage check

*Satisfies:* VAL §3 (injection grid; ≥500/cell; n_transits axis), §6 (power). *Depends on:* M0.2, M0.4. *No injections executed — counting/coverage only.*

- **T0.5.1** For the **frozen injection grid** — period `P ∈ {0.5,1,2,4,8,16}` d, radius `R_p ∈ {1,2,4,8,12} R⊕`, impact `b ∈ {0,0.3,0.6}` — compute, from per-target baselines, the number of available host–cell combinations reaching **`n_transits ≥ 2`** in **each split**.
- **T0.5.2** Confirm each eligible `(P, R_p)` cell can supply **≥ 500 injections** (VAL §3) and that realized counts support the §6 power target (≈90% power, 2 pp margin, α=0.05). Flag at-risk cells.
- **T0.5.3** For any at-risk cell, record the §6 contingency (increase injections per cell with truth and thresholds unchanged) — **no grid or margin change** (that would be a re-registration).

**Deliverable D0.5:** per-cell feasibility table (counts of `n_tr ≥ 2` hosts and max injections per split) + at-risk-cell list with §6 contingency.

---

#### M0.6 — Manifest assembly & seal (Seal #1)

*Satisfies:* VAL §7, A.10; non-negotiables #2, #6. *Depends on:* M0.1–M0.5.

- **T0.6.1** Assemble the machine-readable **frozen manifest (Table T1)** consolidating: sector list; target table; label tables; split tables; sub-sample roster; feasibility table.
- **T0.6.2** Pin **provenance**: catalog names + versions + query timestamps; archive/tool/library versions; all RNG seeds; the Kunimoto & Matthews (2020) occurrence-framework reference used by A.5/A.6 (cite via `references.bib`).
- **T0.6.3** Compute the manifest **content hash (SHA-256)** and record it as **Seal #1** in this plan and in the daily research log. State explicitly that Seal #1 (the *who/what* of the data) is **distinct from** Seal #2 (the M3 *threshold* manifest hash, VAL A.10).
- **T0.6.4** State the **TEST-set access rule** (G1): TEST rows are read for the first and only time at M4; until then they are sealed.

**Deliverable D0.6:** frozen, hashed manifest (Table T1) + provenance block + Seal #1 record + TEST-set access rule.

---

### 3.5 M0 risk register

| ID | Risk | Mitigation | Owner clause |
|----|------|------------|--------------|
| **R0-1** | **Systematic leakage** survives a TIC-disjoint split (shared camera/CCD/pointing correlates calibration↔test). | Block by sky region / camera-CCD (whole blocks per side), not just by TIC; run the M0.4 leakage audit and record residual adjacency. | VAL §3; G3 |
| **R0-2** | **Selection bias**: a target/quality cut correlates with planet detectability and inflates apparent recall. | All cuts outcome-independent, recorded + justified *before* application; cuts reference only catalog metadata. | HYP A6; G3 |
| **R0-3** | **Null-pool contamination**: undetected real planets remain in "planetless" stars, biasing FAR/threshold calibration (H4). | Remove all known TOI/EB hosts; record catalog incompleteness as a reported bound on H4, not a hidden error. | VAL §3, A.2; H4 |
| **R0-4** | **Non-reproducibility**: catalog/tool drift makes the manifest unrebuildable. | Pin catalog versions, query timestamps, tool/library versions, and seeds in provenance; content-hash the manifest. | VAL A.10; G5 |
| **R0-5** | **Power shortfall**: too few `n_tr ≥ 2` hosts to reach ≥500 injections/cell in the TEST split. | M0.5 feasibility gate before seal; revisit sector selection (M0.1) *before* freeze, or invoke §6 contingency (more injections, truth/thresholds fixed). | VAL §3, §6 |
| **R0-6** | **Premature TEST inspection** (anti-tuning violation). | Seal #1 + explicit TEST access rule; no per-split statistics computed on TEST in M0 (feasibility counts use baselines/coordinates only and are reported per split without revealing outcomes). | VAL §7; G1 |
| **R0-7** | **Scope creep** into thresholds (G2) or Phase II clean-skip (G6) during manifest work. | Boundary §3.2 enumerates exclusions; any threshold or clean-skip work is out-of-increment and blocked. | VAL §8; HYP §10 |

### 3.6 M0 deliverables (summary)

| ID | Artifact |
|----|----------|
| D0.1 | Frozen sector list + rationale |
| D0.2 | Target manifest with per-target metadata + inclusion/exclusion criteria |
| D0.3 | Versioned label tables + null-pool definition + four-sub-sample roster |
| D0.4 | CALIBRATION/TEST split tables + leakage-audit report |
| D0.5 | Per-cell feasibility / power-coverage table + at-risk-cell contingency |
| D0.6 | **Frozen, content-hashed manifest (Table T1)** + provenance + **Seal #1** + TEST-set access rule |

### 3.7 M0 completion criteria (binary; all must hold)

M0 is **DONE** iff:

1. ☐ The TESS SPOC 2-min **sector list is frozen** and recorded (FFI/QLP excluded).
2. ☐ The **target manifest** is built from metadata, with all inclusion/exclusion criteria recorded and justified **before** application; required stellar params, coordinates, camera/CCD, and per-target baseline present.
3. ☐ **Label catalogs** (TOIs, EBs/variables) are pinned + versioned for the frozen sectors; the **null pool** is defined as known-host-removed, with the incompleteness caveat recorded.
4. ☐ A **leakage-safe CALIBRATION/TEST split** exists — TIC-disjoint **and** sky-region/camera-CCD-blocked, seeded, with **no training split** — and the **leakage audit passes** (zero shared TIC; spatial separation verified).
5. ☐ All four sub-samples are assigned **consistently** under the single split (global TEST seal).
6. ☐ The **feasibility check** confirms each eligible `(P,R_p)` cell supports ≥500 injections at `n_tr ≥ 2` per the §6 power target, or at-risk cells carry the §6 contingency.
7. ☐ The manifest is **content-hashed (Seal #1)**; provenance (catalog/tool versions, timestamps, seeds, occurrence-framework citation) is pinned.
8. ☐ The **TEST-set access rule** is stated; **no threshold was set**, **no TEST statistic was computed**, and **no sealed document was modified**.

### 3.8 M0 sign-off

Approval to **start** M0 (this plan): **Ansul — approved in-session**  Date: **2026-06-15**
Sign-off that M0 is **DONE** (§3.7 all ☑, Seal #1 recorded): ____________________  Date: __________

---

## 4. Data sources referenced by M0 (pinned at execution, not now)

Named here for completeness; **none are queried by this planning document**. Exact endpoints, catalog versions, and access dates are pinned in the manifest provenance during M0 execution.

- **MAST / TESS SPOC** — 2-minute target product availability per sector (metadata).
- **TIC** — stellar parameters, coordinates, magnitudes for cross-match.
- **TOI / ExoFOP** — confirmed-planet and TOI labels (reality-check).
- **Eclipsing-binary / variable catalogs** — known-FP labels (reality-check; null-pool removal).
- **Kunimoto & Matthews (2020)** — occurrence framework for the A.5 weight prior and A.6 prevalence π̂ (cited, not invoked in M0; pinned in `references.bib`).

---

## 5. Out of scope for this increment

- **Thresholds / calibration** (`z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP`) — M3, on CALIBRATION only, then Seal #2 (VAL A.10).
- **Light-curve retrieval, conditioning, injection, detection, TLS** — M1–M2+.
- **TEST-set evaluation** — exactly one run, at M4.
- **Survey-representative routing / clean-skip / any survey-scale compute mechanism** — Phase II (VAL §8; HYP §10; DR-001).
- **Learned models, classifiers, dashboards, deployment, habitability** — out of all of Phase I.

---

## 6. Traceability — M0 deliverable → sealed clause

| M0 deliverable | Sealed clause satisfied |
|----------------|-------------------------|
| D0.1 sector freeze | VAL §3 (Source; FFI/QLP excluded) |
| D0.2 target manifest + stellar params | VAL §3; A.1 (LD from TIC params); HYP A1/A2/A4 checkability |
| D0.3 labels + null pool | VAL §3 (reality-check, known-TOI-removed); A.2 (null FAR stars); HYP A5; H4 |
| D0.4 leakage-safe split | VAL §3 (disjoint by sky region/TIC; no training split); §7; HYP A6 |
| D0.5 feasibility/power | VAL §3 (grid, ≥500/cell, n_tr axis); §6 (power) |
| D0.6 hashed manifest + Seal #1 | VAL §7; A.10; non-negotiables #2, #6 |

---

*Phase I Execution Plan v0.1 — M0 increment. Subordinate to the sealed pre-registration (`phase1-prereg-v2`). No data read; M0 not started; no sealed document modified. References: VAL = `docs/TRINETRA_X_PHASE1_VALIDATION.md` v2; HYP = `docs/SCIENTIFIC_HYPOTHESIS.md` v2.0; DR-001 = `docs/decisions/F1_DECISION_RECORD.md`.*
