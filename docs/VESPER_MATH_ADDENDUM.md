# VESPER — MATHEMATICAL ADDENDUM (post-seal)

| Field | Value |
|-------|-------|
| **Document** | Post-seal mathematical closure notes (Wave 2 of [`ROADMAP_TO_10.md`](./ROADMAP_TO_10.md)) |
| **Version** | 0.1 |
| **Created** | 2026-07-28 |
| **Status** | **LIVE / APPEND-ONLY.** Not a pre-registration document. Nothing here is sealed, and nothing here changes any sealed threshold, estimand, or the Phase-I verdict. |
| **Relation to the sealed theory** | Companion to [`VESPER_MATHEMATICAL_FOUNDATIONS.md`](./VESPER_MATHEMATICAL_FOUNDATIONS.md) v1.2 (SEALED at tag `phase1-prereg-v3`). That document is **not edited** — it remains byte-frozen modulo the DR-001 §5a rebrand strings. This addendum records analysis performed *after* the seal. |
| **Authority** | Where this addendum and the sealed MATH document differ in emphasis, the sealed document governs the *pre-registered* experiment; this addendum governs *interpretation and future runs*. |

> **Why a separate file.** Non-negotiable NN#2 and P-2 require that `git diff phase1-prereg-v3` over the sealed documents stay empty (modulo branding). Appending sections to the sealed MATH document would break that check, which is the project's principal anti-tuning guarantee. Post-seal mathematics therefore lands here and is cross-referenced, never inlined.

---

## A. MATH-6 — Identifiability of the integer-comb period estimator at $N=2$

**Artifact:** [`data/manifests/m4/wave2/math6_comb_degeneracy.json`](../data/manifests/m4/wave2/math6_comb_degeneracy.json)
**Script:** [`research/m4_evaluation/math6_comb_degeneracy.py`](../research/m4_evaluation/math6_comb_degeneracy.py) (runs the **frozen** `period_recovery`)
**Addresses:** audit §3.3 (N=2 comb degeneracy); roadmap MATH-6.

### A.1 The estimator

Sealed period recovery (MATH §4; `frozen_rerun/period_recovery.py`) scores a trial period $P$ by the circular spread of the detected event epochs $\{t_j\}_{j=1}^{k}$ about a common phase:

$$R(P)=\Big|\tfrac{1}{k}\textstyle\sum_j e^{2\pi i\,t_j/P}\Big|\in[0,1],\qquad s(P)=1-R(P),\qquad \hat P=\arg\min_{P\in\mathcal{G}} s(P),$$

on the frequency grid $\mathcal{G}$ spanning $[p_{\min},p_{\max}]$, with $p_{\max}\leftarrow\min(p_{\max},\,\mathrm{span})$ and $\mathrm{span}=\max_j t_j-\min_j t_j$. Seal #2 fixes $N_{\min}=2$, so **two events suffice to seed a period.**

### A.2 The degeneracy (exact)

For $k=2$ with spacing $D=t_2-t_1$, both events share a phase exactly when $D/P\in\mathbb{Z}$. Hence

$$s(P)=0 \iff P=D/m,\quad m\in\mathbb{N},\ D/m\ge p_{\min}.$$

Every member of this **tie set** is a *global* minimum, so $\hat P$ is **not identifiable** from two events. The statistic $R$ *is* identified: it equals $1$ on the entire tie set. Verified numerically — on-comb scores $\le 1.1\times10^{-16}$ for $m=1\dots10$, off-comb scores $>10^{-3}$ (`tie_set.tie_set_confirmed = true`).

### A.3 What breaks the tie — a correction to the roadmap's premise

The roadmap states the realized convention as "$\arg\min\to$ longest-$P$". **Measurement shows this is approximately, not exactly, true**, and that the mechanism is not a period preference at all: the tie members differ only by IEEE-754 rounding of $1-R$ at the $\sim10^{-16}$ level, and `np.argmin` returns the first index attaining the numerically smallest value. Which harmonic that is, is decided by float rounding.

Two strata must be separated, because their mixture depends on the (data-dependent) spacing distribution and a pooled number would be meaningless:

| Stratum | $m=1$ (longest $P$) | $m\in\{1,2,3\}$ | $m\ge4$ | not a harmonic of $D$ | $R$ saturated at 1 |
|---|---|---|---|---|---|
| **In range** ($D\le p_{\max}$; $P=D$ is on the grid) | 74.2–75.2% | 98.1–98.6% | 1.4–1.9% | ~0% | yes |
| **Out of range** ($D>p_{\max}$; $P=D$ unreachable) | ~0% | ~0.2–0.3% | — | 99.3–99.5% | **no** |

*(ranges span baselines 24.9 d and 49.6 d; 4000 draws per stratum per baseline, seed 20260616)*

- **In range** is the genuine degeneracy: $P=D$ is reachable and is chosen only ~3/4 of the time; the remainder are sub-harmonics selected by float noise.
- **Out of range** is a *different failure* — the true spacing lies outside the sealed search range, no harmonic of $D$ need land on the grid, and $R$ does **not** saturate. This presents to the FAP as an ordinary weak fold, not a perfect one, and should not be described as the comb degeneracy.

### A.4 Consequence: a recall cost, never a false positive

`recovery._period_match` accepts $m\in\{2,3\}$ as a (flagged) harmonic match. That tolerance therefore absorbs **98.1–98.6%** of in-range $N=2$ seeds; only **1.4–1.9%** leak to $m\ge4$ and fail the sealed period predicate. Every such leak is a *missed* recovery — it can only lower recall, never manufacture a detection. This is consistent with the prime directive's asymmetry (a false positive is acceptable; a missed planet is not) in the conservative direction.

### A.5 Why the FAP remains valid under the degeneracy

The block-bootstrap FAP (MATH §9.1) compares the **observed $R$** against surrogate $R$ values — it never uses $\hat P$:

$$\widehat{\mathrm{FAP}}=\frac{1+\#\{b: R^{(b)}_{\max}\ge R_{\rm obs}\}}{1+B}.$$

$R$ is constant on the tie set, and each surrogate is scored by the *identical* degenerate procedure. Observed and null statistics are therefore inflated in exactly the same way, and the degeneracy **cannot** inflate the false-alarm rate. Formally: the test statistic is a well-defined function of the data even where the parameter is unidentifiable, and the null is generated by the same map. The degeneracy costs period *accuracy*, not false-alarm *control*.

### A.6 What the $N=2$ FAP actually tests

Because $R_{\rm obs}=1$ is saturated at $N=2$, the FAP degenerates into "how often does a surrogate also reach $R=1$?" — and any surrogate producing only two events does so automatically. Measured null probability of $R\ge0.999$ against event multiplicity $k$ (baseline 24.9 d, sealed grid):

| $k$ | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 15 |
|---|---|---|---|---|---|---|---|---|
| $\Pr(R\ge0.999)$ | 0.735 | 0.163 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| median $R$ | 1.000 | 0.992 | 0.952 | 0.901 | 0.843 | 0.749 | 0.677 | 0.562 |

*(1500 draws per $k$; uniform event epochs over the baseline — an upper bound on how easily the null folds, since real surrogate events cluster)*

**At $N=2$ the period-FAP is a test of event *rarity* under the null, not of period coherence.** This is a substantive interpretive point: the fast path's binding gate at the sealed operating point is the period-FAP (erratum §2.9), and at the minimum admissible event count that gate is measuring how unusual it is to see so *few* events, not how well they fold. It should be read alongside erratum §2.9 when describing what the realized arbiter tests.

### A.7 Reproducibility caveat (feeds ENG/REPRO)

Because the tie is broken by floating-point rounding, the selected harmonic is deterministic for a given input **and numpy build**, but is not guaranteed stable across architectures or numpy versions. Sealed Phase-I results are unaffected — they were produced once, on one build, and are preserved verbatim in `frozen_rerun/`. Any future (Phase-II) run should **pin the convention explicitly** — e.g. round scores to $10^{-12}$ before `argmin`, then break remaining ties toward the longest period — rather than inherit float noise. Recommended as a Wave-3 item alongside CODE-2 ("degeneracy convention pinned").

---

## B. MATH-7 — Notation cross-reference (MATH ↔ code ↔ paper)

**Addresses:** roadmap MATH-7. Units are given in the unit column; "—" denotes dimensionless.

### B.1 Signal and noise

| MATH symbol | Meaning | Units | Code identifier | Module | Paper |
|---|---|---|---|---|---|
| $f(t)$ | observed flux series | normalized flux | `flux`, `1.0 + r` | `arms.arm_a_full` | — |
| $r(t)$ | conditioned residual (transit = negative) | normalized flux | `r`, `resid` | `m1_pipeline`, cache `*.npz` | — |
| $t$ | time stamps | d (BTJD) | `t`, `time` | all | — |
| $\Delta t$ | cadence | d | `cad` | `detector`, `period_recovery` | — |
| $N$ | number of cadences | count | `t.size`, `n_cadences` | — | — |
| $\sigma$ | robust per-cadence noise scale ($1.4826\,$MAD) | normalized flux | `sigma`, `sigma_ppm` (×10⁶) | `m1_pipeline._noise_model` | — |
| $\Sigma$ | noise covariance | flux² | `K`, `diag`, `sig_red` | `confirmer.estimate_kernel` | — |
| $\tau_{\rm GP}$ | residual correlation timescale (ACF e-folding) | d | `tau_gp_days`, `tau` | `m1_pipeline._tau_gp` | — |
| $\mathrm{CDPP}(T_{14})$ | precision on the duration timescale | ppm | `cdpp_{1.0,2.0,4.0}h_ppm` | `m1_pipeline._noise_model` | — |
| — | residual lag-1 autocorrelation | — | `acf_lag1` | `m1_pipeline` | — |

### B.2 Transit geometry

| MATH symbol | Meaning | Units | Code identifier | Module | Paper |
|---|---|---|---|---|---|
| $\delta$ | fractional transit depth $(R_p/R_\star)^2$ | — | `depth`, `delta`, `delta_hat` | `injection`, `confirmer` | — |
| $R_p$ | planet radius | R⊕ | `radius_rearth` | `recovery.csv` | $R_p$ |
| $P$ | orbital period | d | `period`, `period_days`, `P` | everywhere | $P$ |
| $\hat P$ | recovered/seeded period | d | `p_hat` | `period_recovery.best_period` | — |
| $t_0$ | transit epoch | d (BTJD) | `t0` | `confirmer`, `arms` | — |
| $T_{14}$ | first-to-fourth-contact duration | d | `t14`, `duration` | `injection`, `confirmer` | $T_{14}$ |
| $n_{\rm in}$ | in-transit cadence count | count | `nin` | `confirmer.transit_lr_gp` | — |
| $N_{\rm tr}$ | transits in baseline | count | `n_transits` | `recovery.csv`, `confirmer.n_transits` | $\lfloor T_{\rm base}/P\rfloor+1$ |
| $T_{\rm base}$ | observing baseline | d | `baseline`, `baseline_days` | `m4_driver`, `arms._pmax` | $T_{\rm base}$ |
| $u_1,u_2$ | quadratic limb-darkening coefficients | — | `u1`, `u2`, `STELLAR` | `injection.constant_ld` | — |

### B.3 Detection and period recovery

| MATH symbol | Meaning | Units | Code identifier | Module | Paper |
|---|---|---|---|---|---|
| $d(t_0)$ | box-averaged depth series | normalized flux | `depth` | `detector._box_depth_series` | — |
| — | duration-timescale robust scatter | normalized flux | `scatter` | `detector.detect_events` | — |
| $\mathrm{SNR}_1$ | single-event significance $d/\mathrm{scatter}$ | $\sigma$ | `snr`, `max_event_snr` | `detector` | — |
| $z_\star$ | local-detection threshold | $\sigma$ | `z_star` | `FrozenThresholds` | $z_\star$ |
| $z_{\rm mono}$ | monotransit routing threshold | $\sigma$ | `z_mono` | `FrozenThresholds` | — |
| $k$ | number of detected events | count | `n_events`, `n_events_ge2` | `detector`, RES-4 | — |
| $N_{\min}$ | minimum events to seed a period | count | `n_min` | `FrozenThresholds` | $N_{\min}$ |
| $R$ | comb resultant length (fold quality) | — | `obs_R`, `R` | `period_recovery.best_period` | — |
| $s(P)$ | fold score $1-R$ | — | (return of) `_fold_score` | `period_recovery` | — |
| $N_P,N_d$ | period-, duration-grid sizes | count | `duration_grid_days`, grid len | `detector`, config | — |
| $\varepsilon$ | period-recovery tolerance | — (fractional) | `epsilon` | `FrozenThresholds` | — |

### B.4 FAP and confirmation

| MATH symbol | Meaning | Units | Code identifier | Module | Paper |
|---|---|---|---|---|---|
| $\widehat{\mathrm{FAP}}$ | block-bootstrap period FAP | probability | `fap`, `period_fap` | `period_recovery.period_fap` | — |
| $\alpha_{\rm FAP}$ | FAP gate ($\text{route iff }\mathrm{FAP}\le\alpha$) | probability | `alpha_fap` | `FrozenThresholds` | $\alpha_{\rm FAP}=0.01$ |
| $B$ | bootstrap surrogate count | count | `B`, `n_surrogates` | `FrozenThresholds` | — |
| $L_b$ | bootstrap block length $=3\max(\tau_{\rm GP},T_{14})$ | d | `L_b_days`, `block_len` | `period_recovery.period_fap` | — |
| — | block-length multiple (sealed = 3) | — | `block_len_multiple` | `FrozenThresholds` | — |
| $\Lambda$ | folded transit likelihood ratio | — ($\chi^2_1$ scale) | `lam`, `Lambda` | `confirmer.transit_lr_gp` | $\Lambda$ |
| $T_{\rm red}$ | confirmer threshold (sealed $=0.0$) | — | `T_red` | v3 manifest | $T_{\rm red}$ |
| $T$ | full-TLS SDE threshold | SDE | `T_sde` | `FrozenThresholds` | $\mathrm{SDE}\ge T$ |
| — | TLS signal-detection efficiency | SDE | `sde` | `arms._run_tls` | SDE |
| $k_\sigma$ | odd/even + secondary veto width | $\sigma$ | `k_sigma` (=3.0) | `confirmer` | — |

### B.5 Endpoints and economics

| MATH symbol | Meaning | Units | Code identifier | Module | Paper |
|---|---|---|---|---|---|
| $f$ | fraction routed to the fast path | — | `routed` (per-row) | `recovery.csv` | — |
| $f_p$ | fast-path fraction among planet hosts | — | `f_p` | `endpoints` | $f_p$ |
| $\rho$ | per-star fast-path cost ratio | — | `ratio` (context-dependent) | `endpoints` | $\rho$ |
| $\rho_d$ | per-star detector overhead $C_{\rm det}/C_{\rm full}$ | — | `rho_d` | `endpoints` | $\rho_d$ |
| $\pi$ | planet prevalence | — | `pi_hat` (=0.0317) | `FrozenThresholds` | $\pi\approx0.03$ |
| $\pi^\star$ | break-even prevalence | — | `pi_star_breakeven` | `endpoints` | $\pi^\star$ |
| $\overline{\Delta R}$ | occurrence-weighted recall difference | pp | `delta_R_bar` | `endpoints` | $\overline{\Delta R}$ |
| $\delta_{\rm NI}$ | non-inferiority margin ($-2$ pp) | pp | `MARGIN` (=-0.02) | `res3_*`, `endpoints` | $-2$ |
| $w_c$ | occurrence weight of cell $c$ | — | `w_c` | Seal #2 A.5 | — |
| $\eta$ | transit-preservation factor (M2) | — | `eta` | M2 artifacts | $\eta\ge0.90$ |
| $C_{\rm comb}/C_{\rm full}$ | compute ratio (E2 endpoint) | — | `ratio`, `reduction` | `endpoints` | $\ge30\%$ |

### B.6 $\pi^\star$ — see §C

The break-even prevalence appears in three non-identical forms across MATH, the paper, and the roadmap. This is resolved in **§C (MATH-1)** below.

---

## C. MATH-1 — the break-even prevalence $\pi^\star$, derived

**Addresses:** audit §3.7 ($\pi^\star$ formula inconsistency); roadmap MATH-1.
**Outcome:** the code and the paper are correct; the roadmap's "exact form" is not.

### C.1 The discrepancy

| Source | Form | Value at the run's operating point |
|---|---|---|
| Sealed MATH §8.3a (stated) | $\pi^\star=\rho_d/f_p$ | 0.4887 |
| Paper draft **and** `endpoints.py` | $\pi^\star=\rho_d/\big(f_p(1-\rho)\big)$ | 0.4887 |
| Roadmap MATH-1 ("exact") | $\pi^\star=\rho_d/\big(f_p(1-\rho+\rho_d)\big)$ | 0.4380 |

*(using the re-measured $\rho_d=0.11565$, $f_p=0.23667$, $\rho=2.5\times10^{-5}$)*

### C.2 Derivation

Work in units of the baseline per-star cost, $C_{\rm full}=1$. In the combined arm **every** star must run the detector to be routed at all, at cost $\rho_d$. Then:

- a star that is routed **and** confirmed on the cheap path additionally pays the narrow confirm, $\rho$ → total $\rho_d+\rho$;
- every other star falls back to the full search → total $\rho_d+1$.

Let $q$ be the fraction of *all* stars that are confirmed-cheap. On a survey-representative population with planet prevalence $\pi$ and cheap-path fraction $f_p$ among planet hosts, $q=\pi f_p$ (planetless stars present no evidence and never confirm). Then

$$\frac{C_{\rm comb}}{C_{\rm full}} = q(\rho_d+\rho)+(1-q)(\rho_d+1) = 1+\rho_d-q\,(1-\rho),$$

$$\text{saving} = 1-\frac{C_{\rm comb}}{C_{\rm full}} = \pi f_p(1-\rho)-\rho_d.$$

Setting the saving to zero:

$$\boxed{\ \pi^\star = \frac{\rho_d}{f_p\,(1-\rho)}\ }$$

which is exactly what `endpoints.py:156` computes and what the paper states.

### C.3 Why the other two forms differ

- **MATH §8.3a's stated $\rho_d/f_p$** is the **first-order** form: it drops $\rho$ from the bracket. Since the measured $\rho=2.5\times10^{-5}$, the two agree to four decimal places here. MATH is *self-consistent*: it writes "saving $\approx \pi f_p-\rho_d$" and solves that. **No correction needed** — it is an approximation, correctly labelled as one, and it happens to be numerically exact at this operating point.

- **The roadmap's $\rho_d/\big(f_p(1-\rho+\rho_d)\big)$** derives from the bracket $(1-\rho+\rho_d)$ that appears in MATH §8.3a's displayed cost equation. That bracket implies fast-path stars pay $\rho$ **without** $\rho_d$ — i.e. that a routed star is not charged for the detector that routed it. That contradicts the same section's own premise ("the per-star detector overhead $\rho_d$, charged on **every** routed star") and double-counts the relief. **The roadmap's "exact form" is therefore wrong and should not be adopted.** The displayed bracket in the sealed section carries the same error; it is sealed and stays as written, and this note is the correction of record.

### C.4 Approximation chain (state explicitly)

$$\pi^\star=\frac{\rho_d}{f_p(1-\rho)} \;\xrightarrow[\ \rho\,\ll\,1\ ]{}\; \frac{\rho_d}{f_p}$$

with relative error exactly $\rho$. At $\rho=2.5\times10^{-5}$ the approximation is exact to 4 decimals; it should still be written in the exact form wherever a number is reported, because $\rho$ is a measured quantity that could be non-negligible for a cheaper baseline or a wider confirmation grid.

### C.5 Status of MATH-1's success criterion

The roadmap asks for "one formula, three places (MATH, endpoints, paper), all agree; unit test pins it."

- `endpoints.py` — already correct; only its `pi_star_note` was misattributed (it credited the formula to "MATH §8.3a definition", but §8.3a states the first-order form). **Attribution fixed.**
- Paper — already correct.
- Sealed MATH — cannot be edited (P-2). §C is the correction of record and is cross-referenced from the code.
- Unit test — `tests/test_fast_units.py::test_e2_pi_star_matches_derived_break_even` now pins the exact form against an independent recomputation and asserts the two rejected forms do **not** match. (The previous test was tautological — it compared a value to itself.)

### C.6 Does this change any conclusion?

No. $\pi^\star$ is a **descriptive secondary endpoint** (H1b-survey); the E2 verdict is decided on the measured compute ratio and its host-clustered CI, not on $\pi^\star$. All three candidate forms give $\pi^\star\in[0.44,0.49]$, each an order of magnitude above TESS-realistic $\pi\approx0.03$, so the qualitative finding — **the routing architecture is not a survey-scale compute saver** — is unchanged and robust to the choice.

---

## D. MATH-5 — BCa host-cluster interval for E1

**Artifact:** [`data/manifests/m4/wave2/math5_bca_cluster_ci.json`](../data/manifests/m4/wave2/math5_bca_cluster_ci.json) · [`.md`](../data/manifests/m4/wave2/math5_bca_cluster_ci.md)
**Script:** [`research/m4_evaluation/math5_bca_cluster_ci.py`](../research/m4_evaluation/math5_bca_cluster_ci.py)
**Addresses:** audit §3.5 (40-cluster percentile CI roughness); roadmap MATH-5.

E1's sealed endpoint is a one-sided 95% lower bound on $\overline{\Delta R}$, taken as the 5th percentile of a host-clustered bootstrap. The percentile interval is only first-order accurate: it assumes the bootstrap distribution is median-unbiased and free of skewness drift. With ~40 clusters and a weighted ratio of correlated proportions, neither is guaranteed. BCa corrects both — median bias via $z_0$, skewness via an acceleration $a$ from a leave-one-**host**-out jackknife.

| Quantity | Value |
|---|---|
| Point estimate $\overline{\Delta R}$ | **−0.48 pp** (bit-exact against `endpoints.e1_recall`) |
| One-sided 95% lower bound — percentile (**sealed endpoint**) | **−0.83 pp** |
| One-sided 95% lower bound — **BCa** | **−1.04 pp** |
| Difference (BCa − percentile) | −0.21 pp |
| Sealed margin | −2 pp |
| $z_0$ / $a$ | −0.127 / −0.133 |
| Effective lower-tail probability | 0.0072 (vs 0.05 nominal) |

*(15,000 eligible injections, 40 hosts, 30 cells, $B=20{,}000$, seed 20260616)*

**Reading.** The negative acceleration is not negligible: BCa places the bound at the 0.72nd percentile rather than the 5th, i.e. **the sealed percentile interval is somewhat optimistic**. But the correction is 0.21 pp against a 2 pp margin, so **both bounds clear it comfortably and the E1 non-inferiority conclusion is unchanged** under second-order-accurate inference. The pre-registered decision rule is not re-decided here; BCa is reported alongside, per MATH-5.

**Small-cluster caveat.** $a$ is a third-moment estimate from 40 jackknife values and is itself noisy; a cluster bootstrap with $\lesssim50$ units tends to under-cover regardless of interval method. The honest statement is that *both* bounds sit well inside the margin — not that either is exact to the last decimal.

**Side effect (roadmap CODE-7).** The bootstrap is vectorized: each (host, cell) is reduced once to counts and success sums, so a replicate is two matrix products instead of a `pd.concat`. This is exact rather than approximate — verified bit-exact against `endpoints.e1_recall` — and makes $B=20{,}000$ cheaper than the sealed $B=1{,}000$ loop.

---

## Change log

| Date | Change |
|---|---|
| 2026-07-28 | Created. §A MATH-6 (comb identifiability at $N=2$); §B MATH-7 (notation cross-reference). |
| 2026-07-28 | §C MATH-1 — $\pi^\star$ derived. Code and paper confirmed correct ($\rho_d/(f_p(1-\rho))$); the roadmap's "exact form" rejected as inconsistent with its own cost premise; §B.6 now points here. |
| 2026-07-28 | §D MATH-5 — BCa host-cluster interval for E1: −1.04 pp vs the sealed percentile −0.83 pp; both inside the −2 pp margin, conclusion unchanged. Bootstrap vectorized (CODE-7), bit-exact against `endpoints.e1_recall`. |
