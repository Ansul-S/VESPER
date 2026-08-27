# INN-3 — The period-FAP entry tax is removable, exactly

| Field | Value |
|-------|-------|
| **Date** | 2026-08-17 |
| **Status** | **LIVE result document.** Nothing sealed is edited. The recorded Phase-I verdict (E1 PASS · E2 INCONCLUSIVE) is **unchanged** — see §8. |
| **Roadmap** | **INN-3** ("the provably-equivalent cheap period-FAP estimator — the replacement for the falsified lever, designed with proof obligations stated"), scheduled Wave 6; delivered here with the proof obligations *discharged* rather than stated. |
| **Scope** | CALIBRATION only. No TEST light curve is read (P-5). No network. No sealed document, threshold, weight, manifest or tag is modified. |
| **Code** | [`fast_period_fap.py`](./fast_period_fap.py) · [`inn3_fap_acceleration.py`](./inn3_fap_acceleration.py) · [`tests/test_inn3_fap_acceleration.py`](../../tests/test_inn3_fap_acceleration.py) |
| **Artifacts** | `data/manifests/m4/inn3/` |
| **Theory** | [`docs/VESPER_MATH_ADDENDUM.md`](../../docs/VESPER_MATH_ADDENDUM.md) §E |

---

## 0. Summary

The Phase-I compute claim was blocked by the $B=1000$ period-FAP "entry tax", and
DR-002 recorded it as un-removable after both pre-registered cheap estimators failed
the equivalence gate. **It is removable, exactly.** Two levers, neither of them a
statistical approximation:

* **Lever A — 49% of the FAP's cost was a loop invariant.** The sealed detector
  recomputes `np.median(np.diff(np.sort(t)))` twice per duration per surrogate — 10,000
  sorts of an $N$-vector per star — although the bootstrap resamples the *flux*, not the
  epochs. Hoisting it and vectorising the scans gives **6.31×** at a **bit-identical**
  output: 1126/1126 calibration nulls and 149/149 calibration injections reproduce the
  sealed float exactly.
* **Lever B — the gate is exactly curtailable.** $(g_e{+}1)/1001\le 0.01 \iff g_e\le 9$,
  so the tenth exceedance decides the gate and the run can stop. This is curtailed
  sampling: the routing decision is identical *with probability one*, and one-sided, so
  it can never clip a planet. Total **73.2×** on nulls, 12.7× on injections.

All three sealed Lever-1b criteria — which E-EVT and E-LUT failed 3/3 each — are met
with **exact zeros**.

Consequences, as arithmetic on already-recorded artifacts (no TEST re-read):

| | as recorded | with both levers |
|---|---|---|
| compute reduction | 27.3% (target ≥30%) | **38.0%** |
| $\rho_d$ | 11.6% | **0.85%** |
| $\pi^\star$ vs $\pi\approx0.03$ | 0.489 (~16×) | **0.036** (~1.2×) |
| $P(\text{ratio}\le0.70)$ | 0.27 | **0.96** |
| frozen-rule decision | INCONCLUSIVE | INCONCLUSIVE |

The decision does not move, and **that is the second finding**: setting the routing cost
to exactly zero still leaves the CI at [0.522, 0.703]. E2's INCONCLUSIVE is a
*variance* result — between-host variance at $H=39$ clusters — not a cost result. The
two causes are separable and both were necessary: the entry tax put the point estimate
out of reach at any $H$; the erratum §2.1 host-parity bug (40 of 80 hosts drawn, 39 in
the E2 subset) made the interval too wide at any cost. Fix both and E2 **passes at the
$H=79$ the driver was written to use** (§6.1a).

**Nothing sealed changes.** The recorded Phase-I verdict stands; §6 is labelled a
counterfactual throughout; P-2 holds.

---

## 1. The problem, stated exactly

Phase I's compute hypothesis is the one that did not survive. The corrected verdict
([`M4_ERRATUM_2026-07-19.md`](./M4_ERRATUM_2026-07-19.md) §5, §7) records

$$\frac{C_{\rm comb}}{C_{\rm full}} = 0.727,\qquad \rho_d = 11.6\%,\qquad \pi^\star \approx 0.489 \gg \pi \approx 0.03,$$

and DR-002's Lever-1b study ([`LEVER1B_EQUIVALENCE_RESULT.md`](./LEVER1B_EQUIVALENCE_RESULT.md))
concluded, after both pre-registered cheap estimators failed all three equivalence
criteria, that

> "the compute cost is **not** a removable artifact and the compute claim is not
> salvaged on these terms."

That conclusion is correct about the **estimator** and wrong about its **cost**. Both
candidates (E-EVT: a GPD tail fit to $B'=100$ surrogates; E-LUT: a precomputed
uniform-epoch null) tried to *approximate the null distribution*. The tax they were
attacking is not in the distribution. It is in the arithmetic used to sample it.

## 2. Diagnosis — where the 16.9 s actually goes

`e2_retiming_summary.json` charges the routing stage 16.89 CPU-s per star
(`cost_period` is 0.0 — the FAP is folded into `cost_detector`). Profiling the sealed
`period_fap` on a cached calibration null (TIC 100029948, $N=27{,}523$ cadences) gives
**18.4 CPU-s** for $B=1000$, decomposed as:

| Component | share of the FAP |
|---|---|
| `detect_events` on the surrogate | 82% |
| `best_period` comb scan | 16% |
| circular block bootstrap | 2% |

and *inside* `detect_events`, the single largest line is

```python
cad = float(np.median(np.diff(np.sort(t))))     # detector.py:26 and :55
```

**49% of the entire FAP cost is `np.sort(t)`.** It appears twice per duration, i.e. ten
full sorts of an $N$-vector per surrogate and **10,000 per star**, and every one of them
returns the same constant, because `t` never changes: the block bootstrap resamples the
*flux residual*, not the epochs. The remainder is a Python `for` loop over window
positions (local maxima), an $O(k\times\text{kept})$ Python de-duplication, and a Python
loop over frequencies inside `best_period`.

None of that is the statistic. It is the implementation of the statistic.

## 3. Lever A — exact vectorisation

Every quantity inside the surrogate loop that is a function of the epoch vector $t$
alone — cadence, box widths $n_{\rm bin}$, window-centre epochs $t_0$, stride indices —
is hoisted to construction time. The local-maximum scan becomes three array
comparisons; the greedy de-duplication becomes a bucketed search with identical
semantics (a conflict needs $|t_i-t_j|\le 0.3$ d, so only neighbouring 0.3 d buckets can
hold one); the comb scan becomes a single $(n_f\times k)$ matrix.

**This is an identity, not an approximation.** The same IEEE operations run on the same
operands in the same order, and the same RNG stream is consumed (one vector draw of
`nblk` block starts is bit-identical to `nblk` scalar draws on numpy's PCG64 — asserted
in the test suite). Two floating-point subtleties are preserved deliberately:

* the sealed $\hat R = 1-\min_P\!\big(1-R(P)\big)$ round-trip is kept verbatim rather
  than simplified to $\max_P R(P)$, because $1-(1-x)\ne x$ in float64 near $x=1$;
* the comb scan's $(n_f,k)$ reduction is bit-identical to the per-frequency 1-D
  reduction, since numpy applies the same pairwise summation along the contiguous axis.

## 4. Lever B — exact curtailment

**Proposition.** *The sealed gate is a curtailable Bernoulli test, and curtailing it
changes no routing decision.*

The sealed FAP is Laplace-smoothed, $\widehat{\rm FAP} = (g_e+1)/(B+1)$ with $g_e$ the
number of surrogates whose comb statistic reaches $\hat R_{\rm obs}$. With the Seal #2
values $B=1000$, $\alpha_{\rm FAP}=0.01$,

$$\frac{g_e+1}{1001}\le 0.01 \iff g_e+1\le 10.01 \iff \boxed{g_e\le 9}.$$

$g_e$ is non-decreasing in the number of surrogates drawn. Therefore the instant a run
records its **tenth** exceedance, $g_e\ge 10$ holds for every continuation, the gate is
shut, and the remaining $B-b$ surrogates cannot change it. Stopping there is *curtailed
sampling*: the decision is identical with probability one — not within a tolerance —
and the reported FAP is a certified lower bound on the full-$B$ value.

Two facts make this safe rather than merely clever:

1. **The driver consumes the FAP only through the gate.** `m4_driver.py:171` and `:309`
   evaluate `fap <= alpha_fap`; the value itself is recorded, never compared to anything
   else. (A curtailed run reports `curtailed=True` so the record stays honest.)
2. **Curtailment is one-sided.** It can only stop a run whose gate is already shut. It
   can never open a gate, so under the prime directive's asymmetry it cannot cost a
   planet. Criterion (iii) of the Lever-1b gate — "0 recoveries clipped" — is satisfied
   *by construction*, and is measured anyway in §5.

The threshold generalises: `curtail_threshold(alpha, B) = floor(alpha*(B+1)-1)+1`.

## 5. Measured equivalence and speed (calibration only)

### 5.1 All 1126 cached calibration nulls

Reference: RES-4 arm A at $T_{14}=0.2$ d, itself verified bitwise against the sealed M3
per-star FAPs (968/968). Identity is tested on the **discrete exceedance count**
$g_e = \widehat{\rm FAP}\cdot(B{+}1)-1$, because the recorded FAPs passed through a CSV
text round-trip that perturbs the last ULP of the float, whereas $g_e$ is the sufficient
statistic.

| Check | Result |
|---|---|
| $g_e$ identical to the sealed recorded value | **1126 / 1126** (max abs diff **0**) |
| Gate decision identical, full $B$ | **1126 / 1126** |
| Gate decision identical, curtailed | **1126 / 1126** |
| Live re-run of the sealed implementation (timing subset) | **60 / 60** identical |
| Gate open (sealed) | 27 / 1126 (2.4%) |
| Curtailed | 1099 / 1126 (97.6%) |
| Surrogates used under curtailment | mean **66.3**, median **23** of 1000 |

| Path | CPU s / star | speed-up |
|---|---|---|
| sealed `period_fap` | 14.27 | 1× |
| lever A (exact vectorisation) | 2.48 | **6.31×** |
| lever A + B (exact curtailment) | 0.169 | **73.2×** |

*(single-thread `time.process_time`, BLAS/OMP pinned to 1; the sealed column is a live
re-run of `frozen_rerun/period_recovery.period_fap` on the first 60 stars, which also
supplies the 60/60 identity check.)*

### 5.2 Calibration injections — the sealed Lever-1b criteria

The sealed M4 routing path replayed on calibration injections across the sealed
$(P,R_p)$ grid, including the driver's *actual* $T_{14}$ (§7.1). Same three criteria
that E-EVT and E-LUT failed:

| Criterion | Threshold | E-EVT | E-LUT | **This estimator** |
|---|---|---|---|---|
| (i) FAP agreement, p95 $|\Delta{\rm FAP}|$ | ≤ 0.005 | 0.085 ✗ | 0.104 ✗ | **0.000 ✓** |
| (ii) gate discordant / nulls admitted | ≤ 8 / 0 | 9 / 7 ✗ | 11 / 9 ✗ | **0 / 0 ✓** |
| (iii) recoveries clipped | 0 | 2 ✗ | 2 ✗ | **0 ✓** |

Measured on **149 routed calibration injections** (210 attempted across the 30 sealed
$(P,R_p)$ cells, 80 calibration hosts, sealed grid, `cached_residual` host mode):

| Quantity | Value |
|---|---|
| FAP bit-identical to the sealed implementation | **149 / 149** |
| p95 (and max) $|\Delta{\rm FAP}|$ | **0.000** |
| Gate identical, full $B$ / curtailed | **149 / 149** in both |
| Gate open under the sealed FAP | 65 / 149 |
| Recoveries clipped / nulls admitted | **0 / 0** |
| Surrogates used under curtailment | mean 510, median 378 of 1000 |
| Speed-up, lever A / lever A+B | **6.94× / 12.67×** |

Curtailment is worth much less here than on nulls (12.7× vs 73×) and that is the
expected structure, not a disappointment: a planet-bearing star's comb is *hard* for its
own surrogates to beat, so its run rarely reaches ten exceedances and rightly pays the
full $B$. **The saving is concentrated exactly where the compute is wasted** — on stars
whose gate was going to shut anyway.

## 6. What it does to the compute endpoints

**This is arithmetic on two already-recorded artifacts** — `e2_retiming/timing_ledger_full.csv`
(the DR-003 frozen-rule timing) and `test_run/recovery.csv` (the sealed per-injection
FAP, from which $g_e$ and hence the per-task curtailment depth follow). **No TEST light
curve is re-read** and the sealed E2 outcome is not amended. It answers one question:
*how much of the recorded compute cost was the estimator, and how much was its
implementation?*

Per task $i$: lever A divides the routing cost by the measured factor, lever B replaces
$B$ by $\mathbb{E}[\min(B,T_{10})]=\sum_{n<B}F_{\rm Bin}(9;n,p_i)$ with $p_i=g_{e,i}/B$.

| | ratio $C_{\rm comb}/C_{\rm full}$ | reduction | $\rho_d$ | $\pi^\star$ | 95% host-cluster CI | frozen-rule decision |
|---|---|---|---|---|---|---|
| **as recorded (sealed)** | 0.727 | 27.3% | 11.6% | 0.489 | [0.636, 0.826] | INCONCLUSIVE |
| lever A | 0.630 | 37.0% | 1.82% | 0.077 | [0.540, 0.722] | INCONCLUSIVE |
| **lever A + B** | **0.620** | **38.0%** | **0.85%** | **0.036** | **[0.532, 0.710]** | INCONCLUSIVE |
| free-detector limit | 0.612 | 38.9% | 0 | 0 | [0.522, 0.703] | INCONCLUSIVE |

$P(\text{ratio}\le 0.70)$ moves from **0.27 to 0.96**. The pre-registered 30% target is
met by more than 8 points on the point estimate. The E2 *evidence* changes character
completely — and the **decision does not**, which is §6.1.

### 6.1 The boundary result: E2's INCONCLUSIVE was never the entry tax

Set the routing cost to **exactly zero** and re-run the frozen §6 decision rule. The
host-clustered CI is [0.522, **0.703**] — the upper limit still sits above 0.70.

> **Even a free detector leaves E2 INCONCLUSIVE.** The verdict is not limited by the
> period-FAP, by $B=1000$, or by any property of the estimator. It is limited by
> between-host variance at $n=39$ clusters. No acceleration can resolve it; only more
> hosts can.

That is the honest diagnosis the compute branch was missing. The entry tax was the
**scientific** obstacle (it is what made $\pi^\star$ hopeless and what capped the point
estimate below target); the **decision-grade** obstacle is sample size.

### 6.1a How many hosts would have decided it — and why the answer indicts §2.1

The frozen §6 decision is a host-clustered CI, so its width falls as $H^{-1/2}$. Solving
for the $H$ at which the upper limit first clears 0.70 (design calculation: resamples
the 39 observed hosts, so it assumes they represent the pool; it cannot re-decide the
sealed run):

| configuration | ratio | hosts needed | decision at $H=39$ | decision at $H=79$ |
|---|---|---|---|---|
| as recorded (sealed) | 0.727 | **never** (point estimate is above 0.70) | INCONCLUSIVE | INCONCLUSIVE (also at $H{=}100$) |
| lever A | 0.630 | 65 | INCONCLUSIVE | **PASS** |
| **lever A + B** | **0.620** | **49** | INCONCLUSIVE | **PASS** |
| free-detector limit | 0.612 | 41 | INCONCLUSIVE | PASS |

`m4_driver` draws **80** hosts; the erratum §2.1 parity bug (`hosts[(j+sc) % 80]` with
both indices incrementing) used only the 40 even-indexed ones, of which the E2 timing
subset occupied 39. **$H=79$ is therefore the counterfactual for the design that was
actually written.** Reading the table across:

> The compute branch failed for **two** independent reasons, and neither alone explains
> it. The entry tax put the point estimate out of reach — with it, no host count decides
> E2, not even 100. The host-parity bug made the interval too wide — without the tax but
> at $H=39$, the CI still straddles. Remove **both** and E2 passes at the host count the
> driver was written to use.

This also promotes erratum §2.1 from "halved host noise diversity, E1 re-inferred and
still passes" to a **causal contributor to the undecided compute verdict**. It was
recorded as an E1 concern; its sharper consequence was on E2.

### 6.2 $\pi^\star$ — the survey-scale conclusion changes qualitatively

$\pi^\star=\rho_d/(f_p(1-\rho))$ (MATH addendum §C). On the eligible-injection
population as the sealed analysis measured it, $\pi^\star$ falls **0.489 → 0.036**: from
$\sim16\times$ the TESS transiting-planet prevalence $\pi\approx0.03$ to $\sim1.2\times$.

But $\pi^\star$ is a *survey* quantity, and a survey-representative star is
overwhelmingly planetless. Under the sealed uncurtailed estimator that distinction was
immaterial ($B=1000$ always); under curtailment it is decisive, because a null's own
comb is easy for its surrogates to beat — nulls curtail **73×**, injections far less.

On the calibration-null population the FAP costs **0.169 CPU-s** per star instead of
14.27 — a 73.2× reduction in exactly the term $\pi^\star$ is built from. Measured
$\rho_d$ for a survey-representative star, and the resulting $\pi^\star$, are in
`data/manifests/m4/inn3/inn3_survey.json` (full-grid TLS timed on the same machine and
metric, so the ratio is like-for-like).

Read carefully, this is a **qualitative** change, not a rescue. At $\pi^\star = 0.036$
against $\pi \approx 0.03$ the eligible-population figure sits *at* break-even, not
comfortably below it, and the survey-population figure (which curtails harder) sits below
it. Either way the honest restatement is:

> Erratum §7.3's "evidence-first routing is not a compute-saver at real survey occurrence
> **regardless** of the scoped outcome" is a property of the **sealed implementation**,
> not of the paradigm. With an estimator that does not pay the entry tax, $\pi^\star$
> lands at or below TESS prevalence, and the survey-scale question becomes open rather
> than settled-negative.

That is a weaker claim than "routing saves compute at survey scale" — it is not
established here, and the routing fraction $f_p = 23.7\%$ remains the binding term. What
*is* established is that the sealed number ruling it out was ~14× too pessimistic.

## 7. Secondary findings

### 7.1 The M4 driver duration-matched $T_{14}$; RES-4 measured the wrong stratum for it

`m4_driver.py:117` initialises `t14` to `median(duration_grid)` = 0.2 d — but **line 120
overwrites it** with `ev[argmax snr, 2]`, the seeded event's own duration, and *that* is
what reaches `period_fap` on line 126. (`e2_retiming.py:67` faithfully replicates this;
`m3_calibrate.py` genuinely does use 0.2 d.)

RES-4 states the mechanism as "both `m3_calibrate` and `m4_driver.py:117` pass
$T_{14}=$ median(duration grid) $=0.2$ d" and therefore reports $T_{14}=0.2$ d as the
**sealed, decision-bearing** stratum and $T_{14}\in\{0.05,0.1\}$ d as **counterfactual**.
For the M4 arm that labelling is inverted. Measured on the same 1126 calibration nulls,
the seeded duration is

| seeded $T_{14}$ (d) | 0.05 | 0.1 | 0.2 | 0.4 | 0.8 |
|---|---|---|---|---|---|
| stars | 693 (61.5%) | 201 (17.9%) | 112 (9.9%) | 68 (6.0%) | 52 (4.6%) |

Folding RES-4's own per-stratum arm-C flip counts (24/1126 at 0.05 d, 7/1126 at 0.1 d,
1/1126 at 0.2 d) through this mixture gives an M4-realised flip exposure of
**≈1.4%**, against the 0.09% RES-4 reports — about **16× larger**, and 4.7% of stars
(not 2.8%) have $\tau_\star$ large enough to change $L_b$ at all.

**RES-4's conclusion survives** (the flat-$\tau$ inconsistency still changes no sealed
conclusion, and the flip direction is still the benign one), but its headline number is
measured at a stratum the M4 arm did not use, and its finding F4 — "any future run that
duration-matches $T_{14}$ must use per-star $\tau$" — describes the sealed M4 run rather
than a hypothetical one.

### 7.2 Implementation parity: the vectorised estimator is already near the floor

Arm A's baseline is `transitleastsquares`, which is numba-JIT-compiled
(`core.py`, `helpers.py`, `grid.py`, `interpolation.py`). Arm B's detector and FAP were
interpreted numpy. A compute-ratio endpoint measured in CPU seconds between a compiled
baseline and an interpreted challenger is partly measuring the two implementations.

A numba port of the whole surrogate loop ([`nb_period_fap.py`](./nb_period_fap.py))
reproduces $g_e$ exactly on the stars tested and is only **1.4–1.7×** faster than the
vectorised numpy. So the fairness gap is bounded: after lever A, ≲2× of the routing cost
is attributable to language, and the rest is genuine floating-point work. **The
6.31× is not a compilation trick — it is the removal of work that was never needed.**

## 8. What this does *not* change

* The **sealed Phase-I verdict stands as recorded**: E1 PASS (robust) · E2 INCONCLUSIVE
  · $\pi^\star \gg \pi$. P-2 holds: v3 is final, there is no v4, the TEST set is not read
  again. §6 is a counterfactual re-analysis and is labelled as one everywhere it appears.
* No sealed document, threshold, weight, manifest or tag is edited.
  `frozen_rerun/` is untouched; the sealed run remains reproducible from it.
* This module is **not** the estimator of record for anything. Making it so — for
  Phase II or for any future run — is an owner decision.

## 9. Decisions this puts on the owner's desk

1. **Adopt `fast_period_fap` as the operational estimator of record for future runs?**
   MATH §9.1a admits an estimator substitution "provided it is numerically equivalent to
   the reference". Here the equivalence relation is the identity map at full $B$, and
   provable decision-identity under curtailment. If adopted, record it as a decision
   record (DR-006 or later — DR-004 is reserved for the Phase-II gate and DR-005 for the
   open scope decision) with the §5 evidence attached.
2. **Does §6 belong in the paper?** It is the strongest available answer to the referee
   question "was your compute result an artifact of your implementation?" — and the
   answer is *partly yes, and here is exactly how much*: the point estimate moves
   27.3% → 38.0%, and $\pi^\star$ moves 0.489 → 0.036, while the decision does not move,
   for a reason (§6.1) that is itself a finding.
3. **Does §7.1 warrant a RES-4 addendum?** RES-4's conclusion is unaffected; its stated
   mechanism and stratum labelling are not.

---

*INN-3 result record, 2026-08-17. Calibration-only. Sealed artifacts untouched.*
