# Monotransit Campaign — Pre-Registered Protocol Design (RES-7)

| Field | Value |
|-------|-------|
| **Status** | DRAFT design doc (Wave 1, RES-7). **Design only — no data touched, no light curve read.** |
| **Role** | Concrete injection grid, endpoints, and power analysis for the event-wise monotransit campaign. Expands the Track-C sketch in [`docs/VESPER_PHASE2_PROGRAM.md`](./VESPER_PHASE2_PROGRAM.md) §6 into an executable protocol. |
| **Execution** | **Phase II only**, hard-gated behind the `docs/ROADMAP_TO_10.md` gate and **DR-004** owner sign-off. RES-7× (Wave 6) folds this into the sealed P2C pre-registration. Numeric margins here are *drafting anchors*, to be finalized from calibration (never test) at P2C-prereg. |
| **Why now** | Monotransit (K=1) is the regime where evidence-first routing has a *structural* advantage: no fold exists, so full TLS's only edge (folding to build SNR) is void, the Phase-I entry-tax economics vanish (the cheap path is the only path), and the charter's "photometry decides" is forced (no timing coherence to lean on). This design makes the claim falsifiable. |

---

## 1. Objective

Test whether a calibrated event-wise pipeline (detector at `z_mono` → physics likelihood-ratio confirmer with a **binding** Λ_mono → vetoes) detects single-transit ("monotransit", K=1) planets at useful recall and a controlled false-alarm rate, in the regime where fold-based search cannot operate. This is the native regime for the evidence-first principle and the flagship Phase-II science act.

**K=1 by construction.** A planet with orbital period `P` greater than the observing baseline `T_base` presents at most one transit. The campaign injects `P > T_base` so every injection is a genuine monotransit — no fold is possible for either the pipeline or any baseline.

## 2. Baseline (what we compare against)

No fold-based method exists at K=1, so full TLS is **not** the comparator. The baseline is the **uncalibrated single-event matched filter** (the detector alone at `z_mono`, physics gates removed). The endpoints then measure what the calibrated-FAP + physics-confirmation stack *adds over the raw detector*: purity at matched recall. This isolates the value of confirmation in the one regime where routing is not competing with a fold search.

## 3. Injection grid

Injections into **real** conditioned residuals of multi-sector S1–S3 overlap targets (baselines 27–82 d), preserving genuine correlated noise (Phase-I convention), leakage-safe split reusing the M0 sky-region rule. Raw-flux-then-recondition injection (the Phase-I RES-6 lesson: pay η in both arms).

| Axis | Nodes | Rationale |
|---|---|---|
| Period `P` (d) | {40, 80, 160, 320, 640} | all `> T_base` for the target set ⇒ K=1 by construction; spans single-sector to PLATO-era long-period demographics |
| Radius `R_p` (R⊕) | {4, 6, 8, 11, 14} | monotransit detectability needs depth; small planets are single-event-invisible at TESS noise (bounded, not claimed) |
| Impact parameter `b` | {0, 0.3, 0.6} | grazing geometry stresses the duration/shape gates |
| **Stratifier: SNR₁** (single-event S/N) | computed per injection; endpoints reported **on the SNR₁-visible class** (SNR₁ ≥ a pre-registered floor, drafting anchor 7.0) | the honest denominator: recall is meaningful only where a single event is in principle detectable |

Primary endpoints are evaluated on the **SNR₁-visible** subpopulation (the class the detector can see); the full grid is reported for completeness and to locate the visibility floor.

## 4. Endpoints (formalized)

Applied to the SNR₁-visible class; inference by **host-cluster bootstrap** (Phase-I lesson: injections share host noise realizations — RES-2/audit). All margins are *drafting anchors*, set from the calibration achievable-region at P2C-prereg, never from test.

- **H-C1 (detection).** Monotransit recall `R_mono ≥ R_min` at a calibrated false-alarm rate `≤ α_mono` per star.
  *Anchors:* `R_min = 0.70` on the SNR₁-visible class; `α_mono = 1%/star` (matches Phase-I FAR discipline). PASS iff the one-sided 95% lower bound (host-cluster bootstrap) on `R_mono` exceeds `R_min`, with the null FAR calibrated `≤ α_mono`.
- **H-C2 (added value).** Recall/purity of the full stack is non-inferior in recall and **superior in purity** to the uncalibrated single-event matched-filter baseline at matched FAR (quantifies what confirmation buys).
- **H-C3 (purity).** `≥ V_min` of injected eclipsing-binary / systematic contaminants are rejected by the physics gates. At K=1 odd/even is unavailable, so the veto set is: **sign**, **shape-template consistency**, **secondary search at posterior-implied phases**, and **duration–stellar-density consistency**. *Anchor:* `V_min = 0.75`, from the calibration achievable-region.
- **H0.** Any of H-C1..C3 misses its sealed margin → reported as a **falsification** of the event-wise monotransit realization, with Phase-I finality discipline (single read, pre-committed mapping).

## 5. Power analysis

Binomial-proportion sizing, one-sided 95% (`z = 1.645`), CI half-width `ε = z·√(p(1−p)/n_eff)`; host clustering inflates variance by a design effect `DEFF = 1 + (m−1)·ICC` (m = injections/host).

**Recall endpoint** (worst-case variance near `p = R_min = 0.70`):

| CI half-width ε | required `n_eff` per cell |
|---|---|
| 7 pp | 116 |
| 5 pp | 227 |
| 4 pp | 355 |
| 3 pp | 631 |

**Plan:** target **≥ 300 SNR₁-visible injections per (P, SNR₁) cell** across **≥ 50 hosts** (m ≈ 6, ICC ≲ 0.05 ⇒ DEFF ≲ 1.25). This yields per-cell recall CI half-widths ≈ 4–5 pp after the design-effect penalty — adequate to resolve a 0.70 margin — and a marginal (occurrence-weighted) recall CI comfortably tighter. Cells below the SNR₁ floor are reported but excluded from the pass/fail denominator.

**Purity endpoint** (near `V_min = 0.75`): a known-EB/contaminant sample of **≥ 100** gives ε ≈ 7 pp; ≥ 50 gives ε ≈ 10 pp. Phase I had only **16** EBs (§3.6) — an explicit, quantified limitation this campaign must fix by assembling a larger labeled contaminant set (community single-transit EB catalogs + injected systematics).

## 6. Free pre-study (already available; no new TEST read)

The sealed Phase-I grid accidentally contains **892 effective monotransits** (≤1 observed transit; 852 at P=16 d — erratum §4). Re-analysis of the already-recorded `recovery.csv` rows (no light-curve access ⇒ no new TEST read under the DR-003 boundary) yields empirical anchors: both arms' behavior at K_obs ≤ 1, the fast path's seed quality on single events, and starting values for the §4 margins. Deliverable: a short memo feeding the P2C-prereg numbers. This is the first Phase-II science act and it is free — but it remains **gated behind DR-004** like the rest of Track C.

## 7. Governance

- **Design only.** This document touches no data and reads no light curve. It is not a pre-registration; it is the input to one.
- **Sealed at P2C-prereg**, with margins fixed from calibration achievable-regions before any test access; the Track-C TEST split is defined at P2C-M0, read exactly once at P2C-M5, then closed — the Phase-I single-shot discipline verbatim.
- **Hard-gated** behind the ROADMAP_TO_10 completion gate + **DR-004**. Nothing here executes until then.
- Consistency: this refines, and must not contradict, `VESPER_PHASE2_PROGRAM.md` §6; on any divergence the sealed P2C-prereg (once written) is authoritative.

---
*RES-7 design doc, Wave 1. Grid, endpoints, and power analysis for the monotransit campaign; execution is Phase II, gated behind DR-004. No data touched.*
