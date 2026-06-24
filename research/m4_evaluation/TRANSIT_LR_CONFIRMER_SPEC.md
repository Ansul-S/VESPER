# Transit-LR Confirmer — Implementation Spec (v3; for owner review before Seal #2b)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-19 |
| **Status** | **SPEC LOCKED (owner review 2026-06-19).** Decisions: **D-1a** depth-only linear LR ($\nu=1$); **D-2a** GP marginal likelihood as statistic-of-record, whitened LR admitted **only if validated equal** on calibration nulls; **D-3 (i)** no $t_0$ refinement for the headline statistic (bounded refinement reported only as a robustness check). Ready to implement (`confirmer.py`); no TEST; no seal. |
| **Implements** | VAL v3 §A.11 · MATH v1.2 §6 · DR-002 §2.2 (NN#3 condition #1 = transit-template LR; box depth-SNR rejected). |
| **Replaces** | `epoch_fixed_diagnostic.py::rednoise_snr_fixed` (the dry-run **box** depth-S/N) with a genuine folded-photometry **transit likelihood-ratio** Λ. |
| **Anti-tuning** | The statistic form is fixed **here, from first principles, before its calibration performance is examined** (stopping rule P-3). No parameter is selected on E1/E2. |

> Purpose of this review: lock the exact definition of the Arm-B physics arbiter so that (a) it satisfies NN#3 / MATH §6, (b) it is range-invariant (the Finding-B fix), and (c) its threshold T_red and the period-FAP gate can then be calibrated against a fixed, agreed statistic. Three design decisions (§3) need your explicit ruling.

---

## 1. What the dry-run had, and why it is insufficient

The dry-run confirmer (`rednoise_snr_fixed`) computes, at the fixed seeded ephemeris $(\hat P, \hat t_0)$:
- a **box** (top-hat) in-transit window $|\phi| \le T_{14}/2$,
- box depth $= -\overline{r_{\rm in}}$, red-noise σ from the duration-timescale box-averaged scatter,
- S/N $= \text{depth}\cdot\sqrt{N_{\rm tr}}/\sigma_{\rm dur}$.

It is sign-aware and red-noise-aware — but it is a **box matched filter**, not a transit fit. It does not test transit *shape* (ingress/egress, limb darkening), forms no likelihood ratio, and applies no EB/odd-even/secondary vetting. Per the methodology board it is **borderline** and per DR-002 §2.2 it is **not admissible** as the v3 arbiter. NN#3 stands or falls on replacing it with a genuine transit-template LR.

## 2. The v3 statistic (canonical definition)

At the **fixed** evidence ephemeris $(\hat P, \hat t_0)$ — no period grid, no phase search (range-invariance, the Finding-B property) — on the conditioned residuals $r(t)$ from M1:

- **Null model $\mathcal{M}_0$:** flat baseline (no transit), under the per-star M1 noise model.
- **Transit model $\mathcal{M}_1$:** a **physical limb-darkened transit** (Mandel–Agol) at $(\hat P, \hat t_0)$, with depth $\delta$, duration/shape set by the stellar density $\rho_\star$ and limb-darkening from TIC $(T_{\rm eff}, \log g, R_\star)$ — i.e. the same physical template used for injection (`injection.py`), evaluated, not searched.
- **Statistic:** the likelihood ratio
$$\Lambda = -2\ln\frac{\mathcal{L}(\mathcal{M}_0)}{\mathcal{L}(\mathcal{M}_1)} \xrightarrow{\ \mathcal H_0\ } \chi^2_\nu,\quad\text{(equivalently }\Delta\mathrm{BIC}\text{).}$$
- **Sign-aware:** only dimming admitted ($\delta>0$); a best-fit $\delta\le0$ ⇒ $\Lambda:=0$ (reject).
- **Shape-consistent:** the in-transit profile must be transit-like — ingress/egress consistent with $(R_\star,\rho_\star)$; **odd-even** depth consistency and **no significant secondary** at phase 0.5 (EB rejection) for $N_{\rm tr}\ge2$; the MATH §6 single-event vetting for $N_{\rm tr}=1$ (monotransit, weaker FP control, excluded from headline).
- **Decision:** confirm iff $\Lambda \ge T_{\rm red}$ **and** the shape/sign checks pass. $T_{\rm red}$ calibrated to FAR ≤ 1 %/star (the T_red plan).
- **Look-elsewhere:** handled upstream by the period-FAP gate (A.8/A.8a). The confirmer is a single fixed-ephemeris test → **no additional LEE** (this is the whole point of fixing the ephemeris).

## 3. Three design decisions needing your ruling (P-3: fixed before performance is seen)

**D-1 — Free parameters of $\mathcal{M}_1$ (this sets $\nu$ and whether any hidden search exists).**
The cleaner the parameterization, the more defensible the null distribution and the lower the LEE risk.
- **D-1a (recommended): depth-only linear LR, $\nu=1$.** Fix the template *shape* (duration $T_{14}$ and $b$) from the seed (strongest event's measured duration) and stellar density; fit only depth $\delta$ by linear least squares. $\Lambda$ is then an analytic, single-dof LR with a clean $\chi^2_1$ null — **no nonlinear search, no hidden multiple comparison.** Most defensible under P-3.
- **D-1b: depth + bounded duration/$b$.** Also optimize duration/impact within tight physical bounds around the seed. More power against shape mismatch, but introduces a small nonlinear fit → the null is no longer exactly $\chi^2_1$ and a (small) effective-trials correction is needed; $T_{\rm red}$ then absorbs it via the empirical null calibration.

**Recommendation: D-1a.** It keeps the arbiter a clean, theory-fixed LR; the duration is already evidence-supplied, and the full-TLS fallback catches shape mismatches the fixed-template misses (recall-protected).

**D-2 — Red-noise likelihood (this is the real upgrade over the box-S/N).**
- **D-2a (recommended): GP marginal likelihood.** Evaluate $\mathcal{L}$ under the M1 per-star GP/correlated-noise kernel (reuse the M1 `celerite2`/noise-model parameters), at fixed ephemeris → $O(n)$, cheap relative to full TLS. Canonical; uses the star's own correlation structure.
- **D-2b: whitened linear LR.** Whiten $r(t)$ by the M1 noise model, then the depth-only LR is ordinary least squares. Cheaper/simpler, but the whitening must be validated to reproduce the GP-LR's null FAR (else it inherits the box-S/N's red-noise optimism).

**Recommendation: D-2a**, with D-2b admitted only if validated equal on nulls. (Note: D-2a's per-star likelihood is the natural home for the EVT/precomputed period-FAP equivalence work too.)

**D-3 — Bounded $t_0$ refinement?**
The seed $\hat t_0$ has finite precision. Options: (i) **no refinement** — use $\hat t_0$ as-is (strict range-invariance, no search); (ii) a **bounded** local $t_0$ refinement within $\pm$ the seed's cadence-level uncertainty. Any refinement is a (tiny) search and must be width-bounded and folded into the null calibration.

**Recommendation: (i) no refinement** for the headline statistic (keep it a pure fixed-ephemeris LR); report (ii) only as a robustness check. The recovery predicate already allows epoch tolerance $\pm0.5\,T_{14}$ (VAL §4.1(ii)), so a real transit at the seed is not lost by fixing $t_0$.

## 4. Inputs / outputs (implementation contract)

**Inputs (all already available):**
- conditioned residuals $r(t)$, time $t$ — `data/processed/m1/{tic}.npz` (M1).
- seeded ephemeris $(\hat P, \hat t_0, T_{14}, N_{\rm events})$ — `evidence_ephemeris()` (existing).
- stellar params $(R_\star, \rho_\star, T_{\rm eff}, \log g)$ + limb-darkening — M0 manifest + `injection.constant_ld()` / TIC.
- per-star M1 noise model (σ, CDPP, $\tau_{\rm GP}$, kernel) — M1 noise summary.
- frozen routing params (z⋆, N_min, ε) — `seal_loader.load_frozen()` (Seal #2, unchanged).

**Output per star:** `(Lambda, delta_hat, n_transits, shape_pass, sign_pass, confirmed)` where `confirmed = (Lambda >= T_red) and shape_pass and sign_pass`.

**New function:** `transit_lr_fixed(t, r, P, t0, T14, stellar, noise_model) -> (Lambda, delta, diagnostics)` in a new `confirmer.py`, replacing `rednoise_snr_fixed` in the Arm-B path. The seed/detector/period code is unchanged.

## 5. Anti-tuning & guardrails

- Statistic form (D-1…D-3) is fixed **now**, before any $\Lambda$ distribution is examined (P-3). This spec review *is* that fixing.
- The confirmer is built and exercised on **CALIBRATION only**; `seal_loader.py` blocks TEST; 0 TEST TICs asserted in all outputs.
- $T_{\rm red}$ is set by FAR (T_red plan), never by E1/E2.
- The full-TLS fallback (unchanged) re-searches every non-confirmed routed star → recall is protected even if the fixed template is imperfect (NN#1).

## 6. Validation hooks (after the spec is approved)

1. **Sanity:** AUC(planet/null) of $\Lambda$ on the cleaned null pool + calibration injections must be **≥ the dry-run box-S/N's 0.877** (a true transit LR should separate at least as well). If not, the implementation is wrong — investigate before proceeding.
2. Feeds the **Lever-1b equivalence plan** (the period-FAP gate sits upstream of this confirmer) and the **T_red calibration plan** (calibrates $T_{\rm red}$ on this exact statistic).
3. Odd-even / secondary vetting validated on the known-EB set (M3 cleaning catalog) — must reject EBs the box-S/N would pass.

## 7. What this confirmer is NOT

- Not a box / top-hat depth-S/N (the rejected dry-run statistic).
- Not a period or phase search (no grid; range-invariant — the Finding-B fix).
- Not uncalibrated (threshold from null FAR; LEE from the upstream period-FAP).
- Not tuned on TEST or on E1/E2.

---

## Decision summary for sign-off

| # | Decision | **LOCKED (2026-06-19)** |
|---|---|---|
| D-1 | $\mathcal{M}_1$ free parameters | **D-1a** depth-only linear LR ($\nu=1$, no hidden search) |
| D-2 | red-noise likelihood | **D-2a** GP marginal likelihood (M1 kernel) as statistic-of-record; **whitened LR admitted only if validated equal** on calibration nulls |
| D-3 | $t_0$ refinement | **(i)** none for headline; bounded refinement reported as a robustness check only |

*Decisions locked by owner review. Implementation of `confirmer.py` proceeds to exactly this spec; then the equivalence validation + T_red calibration on CALIBRATION, the v3 manifest, and Seal #2b for the owner's final go before the single TEST run.*
