# PHASE 1 REMEDIATION — VESPER

| Field | Value |
|-------|-------|
| **Document** | Pre-execution remediation plan |
| **Version** | 1.0 |
| **Scope** | **Critical + Must-fix findings only** from [`REPOSITORY_GAP_ANALYSIS.md`](./REPOSITORY_GAP_ANALYSIS.md) (F1, F2, F6, F8). Medium/Low and "should-fix" items deliberately excluded. |
| **Date** | 2026-06-15 |
| **Status** | Proposed edits — **not yet applied** |

> **Cross-cutting fact (read first).** All four items below touch parameters or endpoints that the Phase I pre-registration is supposed to freeze ([`VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md), [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md)). **Every one requires re-registration.** Because **no data has been touched yet** (Phase I has not executed), resolving them now is a legitimate pre-registration *completion*, not post-hoc tuning — the anti-tuning rule (non-negotiable #2) is violated only by changes made *after* seeing test results. **Action: resolve all four, then issue a single re-dated `VESPER_PHASE1_VALIDATION.md` v2 and seal before any sector data is read.**

---

## F1 — Compute-measurement population (Critical)

**1. Problem.**
H1b claims a ≥30 % reduction in *total* compute, and the theory gives saving ≈ *f* (fast-path routing fraction). But the primary truth is injection into real light curves, so every test star carries a planet. On a real survey the **planetless majority** (~99 %) presents no local evidence → routes to the full-TLS fallback → cost = detector + full TLS > baseline. The fast path is therefore *net overhead* on planetless stars, and the all-injected sample silently overstates survey-scale saving.

**2. Why it matters.**
This determines whether H1b is even meaningful. Quantitatively, for a population with planet prevalence π, fast-path fraction among planet hosts $f_p$, detector overhead $\rho_d = C_{\rm det}/C_{\rm full}$, and fast-path ratio $\rho = C_{\rm fast}/C_{\rm full}$:

$$\frac{C_{\rm comb}}{C_{\rm full}} \approx (1+\rho_d) - \pi f_p\,(1-\rho+\rho_d)\;\Rightarrow\;\text{saving}\approx \pi f_p - \rho_d.$$

For survey-realistic $\pi \sim 10^{-2}$ this saving is **near zero or negative**. So as currently posed, evidence-first routing demonstrably cannot deliver survey-scale compute saving without a mechanism to *skip* the full search on no-evidence stars — which trades recall. A reviewer (PR-A) invalidates the headline compute claim immediately. This is the single most consequential gap.

**3. Exact document(s) to edit.**
- [`docs/SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) → H1b, §6, §9.
- [`docs/VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) → §1 (datasets), §4 (compute accounting), §5 (decision rule).
- [`docs/VESPER_MATHEMATICAL_FOUNDATIONS.md`](./VESPER_MATHEMATICAL_FOUNDATIONS.md) → §8.3 (add the two-regime cost model above).

**4. Proposed fix (recommended decision; requires sign-off).**
Adopt **all three** of:
- **(a) Scope the Phase I compute claim** to the *fast-path-eligible population*: restate H1b as "≥30 % compute reduction **on stars presenting exploitable local evidence**," measured on the planet-enriched injection sample. This is honest and provable in Phase I.
- **(b) Add the two-regime cost model** (equation above) to the theory and report a **survey-representative** compute figure as a *secondary* endpoint: build a mixed sample at a pre-registered prevalence $\hat\pi$ (from TESS occurrence × geometric transit probability), injecting planets into only a $\hat\pi$ fraction and leaving the rest as real (known-TOI-removed) light curves; report $C_{\rm comb}/C_{\rm full}$ over it. This makes the survey-scale limitation explicit and quantified rather than hidden.
- **(c) Defer survey-scale saving to a clean-skip tier (Phase II).** State plainly that survey-scale compute reduction *requires* a calibrated noise-floor skip on no-evidence stars (the v3 "CDPP-skip"), which trades recall and therefore demands its own non-inferiority test — out of Phase I scope.

*Net effect:* Phase I makes a **defensible, narrower** compute claim and openly documents the survey-scale path, instead of an over-broad claim that fails external validity.
*Alternative (not recommended for Phase I):* implement the clean-skip tier now and fold its recall cost into H1a — larger scope, more recall risk, slower.

**5. Re-registration required?** **Yes.** Changes the H1b estimand and the compute-evaluation population.

---

## F2 — Operational definition of "recall / recovery" (Critical)

**1. Problem.**
"Recall," "completeness," and "recovery" are used throughout as the **primary endpoint**, but the predicate for *"an injected planet was recovered"* is never defined: no period tolerance, harmonic policy, epoch criterion, or significance requirement.

**2. Why it matters.**
The entire experiment's headline number is a recall comparison. Without a fixed recovery predicate the result is **not reproducible**, not comparable between arms, and not defensible to reviewers — and an undefined predicate is itself a degree of freedom that could be (even unintentionally) tuned.

**3. Exact document to edit.**
[`docs/VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) → §4 (add subsection **"Operational recovery predicate"**); referenced from [`docs/SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) §6.

**4. Proposed fix (concrete predicate, identical for both arms).**
An injected planet $(P_{\rm true}, t_{0,\rm true}, \delta_{\rm true})$ is **recovered** by an arm iff that arm returns a detection satisfying **all** of:
- **(i) Period.** $|\hat P - P_{\rm true}|/P_{\rm true} < 0.01$, **or** $\hat P$ matches a harmonic $\{P_{\rm true}/m,\ m P_{\rm true}\}$ for $m\in\{2,3\}$ within the same 1 % tolerance (harmonic recoveries counted as recovered but **flagged** and reported separately).
- **(ii) Epoch.** the recovered ephemeris aligns to a true transit within $\pm\,0.5\,T_{14}$.
- **(iii) Significance.** the arm's detection statistic (TLS SDE) $\ge T$, the **single common threshold** of F8.

The predicate is applied **identically** to Arm A (full TLS) and Arm B (combined), preserving the fairness keystone. Completeness $R$ is the fraction of injected planets recovered, per cell and aggregated per F6.

**5. Re-registration required?** **Yes.** Pins the primary-endpoint definition, currently unspecified.

---

## F6 — Multiple-testing across completeness cells / primary estimand (Must-fix)

**1. Problem.**
Non-inferiority is to be evaluated "overall and per $(P, R_p)$ cell," but with **no multiplicity correction and no single pre-specified primary estimand**. Testing dozens of cells makes the decision statistically ill-posed: one can pass in aggregate while failing important cells, or fail a cell by chance.

**2. Why it matters.**
The pass/fail decision is the output of Phase I. An uncontrolled multi-cell decision is not a valid test (PR-E) and would not survive review; it also leaves the "did we pass?" question ambiguous.

**3. Exact document(s) to edit.**
- [`docs/SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) → §6 (non-inferiority definitions / decision).
- [`docs/VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) → §4–§5 (endpoints, decision rule).

**4. Proposed fix.**
Define one **primary estimand**: the occurrence-weighted marginal completeness difference

$$\overline{\Delta R} = \sum_{c\,:\,N_{\rm tr}\ge 2} w_c\,\bigl(R_{\text{comb},c}-R_{\text{TLS},c}\bigr),\qquad \sum_c w_c = 1,$$

with weights $w_c$ from a **pre-registered** prior over $(P, R_p)$ (e.g. log-uniform in $P$ × a stated radius-occurrence distribution), normalized over the eligible grid. **Primary decision:** non-inferiority is declared iff the lower bound of the one-sided 95 % CI on $\overline{\Delta R}$ exceeds $-\delta_{\rm NI} = -0.02$. Per-cell $\Delta R_c$ are reported as **secondary/descriptive**; if cell-level screening is wanted, apply a pre-specified Holm correction and report it as secondary only (never as the gate). This collapses the decision to a single, well-posed test.

**5. Re-registration required?** **Yes.** Defines the primary estimand, weighting, and decision rule.

---

## F8 — Pin thresholds, TLS baseline configuration, and runtime protocol (Must-fix)

**1. Problem.**
The detection threshold $z_\star$, routing parameters ($\theta$, $N_{\min}$, "strong event"), the common significance threshold $T$, the **TLS baseline configuration** (implementation, period grid, oversampling, duration grid), and the **runtime-measurement protocol** are all symbolic/unspecified.

**2. Why it matters.**
These parameters jointly set *both arms'* recall and cost. "Set on the calibration set" is asserted but the **target** they are tuned to, and the baseline's own configuration, are not pinned — so the result is not reproducible, the fairness keystone (equal-threshold comparison) cannot be verified, and the entire compute claim rests on an unspecified runtime protocol (PR-F).

**3. Exact document to edit.**
[`docs/VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) → §2 (pipelines/thresholds), §4 (compute accounting); add an appendix **"Frozen parameters & baseline configuration."**

**4. Proposed fix (commit these values on the calibration set, then freeze).**
- **TLS baseline (both arms).** Implementation `transitleastsquares` (Hippke & Heller 2019); optimal period sampling (Ofir 2014) over $[P_{\min}, P_{\max}]$ matched to the injection grid; default duration grid; limb-darkening from TIC stellar parameters. Record exact version + parameters.
- **Common significance threshold $T$.** Set the TLS SDE threshold so the empirical false-alarm rate on **null (planetless) calibration stars** equals a pre-registered $\alpha$ (recommend FAR $\le 1\%$ per star). **Both arms use this identical $T$** (fairness keystone; also satisfies the F-level null-FP target).
- **Detector threshold $z_\star$ & routing.** $z_\star$ set on the calibration set to a target local false-event yield (recommend $\le 1$ expected false event per null light curve); $N_{\min}=2$ events for the multi-event fast path; "strong event" $\equiv$ a single event with $\mathrm{SNR}_1 \ge z_{\rm mono}$ for a stated $z_{\rm mono} > z_\star$ (monotransit branch).
- **Runtime protocol.** One specified machine; single-thread **CPU-core-seconds**; median over $\ge 5$ repeats; warm cache; **shared conditioning cost excluded** (or charged equally to both arms); report the full distribution, not just the mean.

All values fixed on the calibration set, hashed into the manifest, then sealed.

**5. Re-registration required?** **Yes.** These are precisely the parameters the pre-registration exists to freeze; committing numeric values completes/amends it.

---

## Consolidated Re-Registration Checklist

| # | Finding | Edits | Re-register? |
|---|---------|-------|:---:|
| F1 | Compute population | HYPOTHESIS H1b/§6/§9 · VALIDATION §1/§4/§5 · MATH §8.3 | ✅ |
| F2 | Recovery predicate | VALIDATION §4 · HYPOTHESIS §6 | ✅ |
| F6 | Primary estimand / multiplicity | HYPOTHESIS §6 · VALIDATION §4–§5 | ✅ |
| F8 | Thresholds + baseline + runtime | VALIDATION §2/§4 + new appendix | ✅ |

**Procedure:** (1) obtain sign-off on the F1 scoping decision; (2) apply F1, F2, F6, F8 edits to the named documents; (3) reissue [`VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) and [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) as **v2, dated 2026-06-15**; (4) **then** freeze and begin M0 (sector/target manifest + leakage-safe split). No sector data may be read until step 4.

> Only **F1** requires a human decision (the scoping choice). F2, F6, and F8 have concrete proposed fixes ready to apply as-is.

---

*Remediation plan v1.0. Restricted to Critical + Must-fix findings per request. Proposed edits not yet applied.*
