# VESPER — MATHEMATICAL AUDIT AND NEW RESULTS

| Field | Value |
|---|---|
| **Document** | Post-seal mathematical audit + new results (findings report) |
| **Date** | 2026-08-27 |
| **Status** | **LIVE / analysis record.** Not a pre-registration document. Nothing here changes a sealed threshold, statistic, weight, manifest, tag or the Phase-I verdict. |
| **Data** | **CALIBRATION ONLY.** No TEST TIC was read (P-5 intact). 1,236 cached calibration nulls; 669 routed calibration injections; 240 dress-rehearsal calibration injections (existing artifact). |
| **Reproduction** | `research/math_audit/` (5 scripts) → `data/manifests/math_audit/` (10 artifacts + `findings.json`) |
| **Provenance check** | The re-implementation used here reproduces the sealed exceedance counts **bit-identically on 1,126/1,126 overlapping calibration nulls** (`verify_surrogate_table.json`: k mismatches 0, max \|ΔR\| = 0, ge mismatches 0). |
| **Relation to sealed docs** | Companion to [`docs/VESPER_MATHEMATICAL_FOUNDATIONS.md`](../../docs/VESPER_MATHEMATICAL_FOUNDATIONS.md) v1.2 (SEALED) and [`docs/VESPER_MATH_ADDENDUM.md`](../../docs/VESPER_MATH_ADDENDUM.md). Sealed documents are **not edited**; `git diff phase1-prereg-v3` over them stays empty. |

---

## 0. Executive summary

The audit set out to find whether VESPER's mathematics contains a genuinely novel, provable
contribution. It does — but it is **not** the contribution the project has been claiming.

**The novel result is a negative one with a closed form.** Evidence-first period recovery,
gated on the significance of a phase-coherence statistic, obeys a hard bound:

$$\boxed{\;W \;\equiv\; k\,\hat R^{2} \;\ge\; \ln\!\big(N_{\rm eff}/\alpha\big),\qquad W \le \frac{N_{\rm tr}}{1+\rho_{\rm FP}} \;\;\Longrightarrow\;\; P \;\lesssim\; \frac{T_{\rm base}}{\ln(N_{\rm eff}/\alpha)}\;}$$

The routing gate cannot open unless the candidate presents an *evidence budget* $W = k\hat R^2$
exceeding the look-elsewhere penalty of the period grid. Because $W$ is capped by the number of
transits in the baseline, this converts directly into a **maximum routable period** that grows
only as $T_{\rm base}/\ln T_{\rm base}$. Every knob — $\alpha$, $p_{\min}$, $p_{\max}$, the
detector, the noise model, the confirmer — enters **logarithmically**; only the transit count
enters linearly. You cannot buy your way past it.

This is validated three independent ways and survives a deliberate attempt to break it:

| Test | Result |
|---|---|
| Closed-form gate prediction, **zero free parameters**, 1,233 calibration nulls | **precision 87.5 %, recall 75.7 %** (TP 28 · FP 4 · FN 9 · TN 1192) |
| Out-of-sample scaling: predicted $P_{\max}$ for 1-sector vs 2-sector hosts | predicted **2.94 / 5.80 d**, measured **2.51 / 5.00 d**; predicted ratio 1.97, measured **1.99** |
| Mechanism: is it seeding failure or the significance budget? | at $P\ge8$ d, $\Pr(\text{gate open}\mid\text{seed correct}) = 0.20$ and $0.00$ |
| **Falsification attempt** — replace the sealed statistic across the family $T_\beta = \hat R\,k^{\beta}$ at matched null FAR | best member gains **+1.49 pp** recall; the *exactly pivotal* statistic **loses 10.31 pp**; $P\ge8$ d stays at $\le0.9$ % for every member |

The falsification attempt is the important part. The multiplicity dependence of the sealed
statistic is **not a defect that a better statistic removes** — removing it destroys power,
because the event count *is* the evidence. The ceiling is a property of the null geometry.

**Two corollaries settle what Phase I was actually testing.**

1. **Subset-region property.** Fast-path eligibility implies $\mathrm{SNR}_1\ge z_\star$ *and*
   $N_{\rm tr}\gtrsim9$, hence $\mathrm{SNR}_{\rm tot}=\mathrm{SNR}_1\sqrt{N_{\rm tr}}\gtrsim10$ —
   inside the full search's own detection region. Measured on the dress rehearsal: excluding the
   known $P=0.5$ d grid-edge artifact, **17 of 17** fast-path recoveries were also recovered by
   full TLS; **zero** were fast-path-only. The architecture is a pure compute play for periodic
   signals; E1's PASS was structurally guaranteed, as erratum §2.8 says, and this explains *why*.
2. **The paradigm works where the problem is already easy.** Routing needs frequent transits;
   a periodic search gets easier as transits become frequent. Evidence-first routing is
   structurally excluded from the long-period regime that motivated it. The only regime where it
   could add coverage is the monotransit limit $N_{\rm tr}=1$, where the coherence test is
   undefined — currently out of scope (H3).

**Six further findings, each measured, four of them defects in the sealed mathematics.** The
period-FAP is 82 % a multiplicity statistic (§N-3); $\Lambda$'s null exceeds $\chi^2_1$ by up to
21 orders of magnitude in tail probability (§N-4, closes roadmap MATH-4); the conditioned
residuals are red on transit timescales while the project certifies them white from $\mathrm{acf}_1$
(§N-5); **79 % of all fast-path routings exist only because the bootstrap null is contaminated by
the signal it is testing** (§N-6, closes roadmap MATH-3 and reverses its assumed direction);
MATH §4b's contamination fragility is linear, not quadratic (§C-1); MATH §9's "identical grid"
premise is false in code, and that deviation is load-bearing (§C-2).

**Nothing here overturns the sealed Phase-I verdict** (E1 PASS · E2 INCONCLUSIVE). The
false-alarm calibration is intact: on the M3-cleaned null pool the gate measures 1.06 % at a
nominal 1 % (§N-7). What changes is the *interpretation* of what was validated, and the ceiling
sets a hard limit on what any future version of this architecture can achieve.

---

# PART I — NEW RESULTS

## N-1. The routing ceiling

### N-1.1 The evidence budget

Sealed period recovery scores a trial period by the circular resultant of the detected event
epochs, $\hat R = \max_{P\in\mathcal G} R(P)$, $R(P) = |k^{-1}\sum_j e^{2\pi i t_j/P}|$
(`frozen_rerun/period_recovery.py`). Define

$$W \;\equiv\; k\,\hat R^{2}.$$

$W$ is the Rayleigh $Z$ statistic. It is the natural evidence scale because at a fixed trial
frequency with $fS\gg1$, the CLT gives $2kR^2\to\chi^2_2$, i.e.

$$\Pr\big(R(f)\ge r \,\big|\, k,\ \mathcal H_0\big) \;\simeq\; e^{-k r^{2}} \;=\; e^{-W}.$$

**Lemma (budget bound).** With $k_{\rm true}$ coherent transits and $k_{\rm FP}$ false events at
random phase, $\mathbb E[R]\simeq k_{\rm true}/k = (1+\rho_{\rm FP})^{-1}$, hence

$$W \;\simeq\; \frac{k_{\rm true}}{1+\rho_{\rm FP}} \;\le\; N_{\rm tr}.$$

*Verified numerically* (3,000 draws per cell, $P=3$ d, $T_{\rm base}=49.6$ d):
$\mathbb E[R]$ matches $1/(1+\rho_{\rm FP})$ to three decimals and $W$ matches
$k_{\rm true}/(1+\rho_{\rm FP})$ to ~2 % across $\rho_{\rm FP}\in[0,4]$ and $k_{\rm true}\in\{10,20\}$.

| $k_{\rm true}$ | $\rho_{\rm FP}$ | measured $\mathbb E[R]$ | $1/(1+\rho)$ | $1/(1+\rho)^2$ | measured $W$ | $k_{\rm true}/(1+\rho)$ |
|---|---|---|---|---|---|---|
| 20 | 0.25 | 0.8031 | 0.8000 | 0.6400 | 16.12 | 16.00 |
| 20 | 1.00 | 0.5055 | 0.5000 | 0.2500 | 10.22 | 10.00 |
| 20 | 4.00 | 0.2119 | 0.2000 | 0.0400 | 4.49 | 4.00 |

(The third column is the correction of MATH §4b — see §C-1.)

### N-1.2 The look-elsewhere budget

The gate is $\widehat{\rm FAP}\le\alpha$. Maximising over $N_{\rm eff}$ effectively independent
trial frequencies,

$$\Pr\big(\hat R\ge r\big) \simeq 1-\big(1-e^{-kr^2}\big)^{N_{\rm eff}} \simeq N_{\rm eff}\,e^{-W},$$

so the gate opens only if

$$W \;\ge\; \ln\!\big(N_{\rm eff}/\alpha\big),\qquad N_{\rm eff}\simeq S\Big(\tfrac1{p_{\min}}-\tfrac1{p_{\max}}\Big).$$

At Seal #2 ($\alpha=0.01$, $p_{\min}=0.5$ d, $p_{\max}=\min(0.5\,T_{\rm base},S)$):
$N_{\rm eff}\approx48$ (1-sector) to $97$ (2-sector), giving $W^\star = 8.5$ to $9.2$.

**Every tunable enters logarithmically.** Tightening $\alpha$ by $10\times$ costs 2.3 in budget;
shrinking the period search $10\times$ buys 2.3. Only $k$ enters linearly.

### N-1.3 Validation 1 — the closed form predicts the sealed gate with no free parameters

Applying `gate open ⟺ W ≥ ln(N_eff/α)` to 1,236 calibration nulls, against the actual sealed
gate decision computed from 1,236,000 surrogates:

| | gate open (sealed) | gate shut (sealed) |
|---|---|---|
| **predicted open** | 28 | 4 |
| **predicted shut** | 9 | 1192 |

**Accuracy 98.95 %** over the 1,233 stars with a defined prediction (3 of 1,236 are excluded:
$k=2$ stars whose event span is shorter than $p_{\min}$, so $N_{\rm eff}\le0$ and the formula has
nothing to say). Accuracy is a weak figure on a 1,196 : 37 split, so the honest ones are
**precision 28/32 = 87.5 %** and **recall 28/37 = 75.7 %** — from a formula with no fitted
parameter. Median $W^\star = 8.35$ (range 3.74–9.64).

An assumption-free version, from the empirical null quantiles of $\hat R$ pooled over 1.24 M
surrogates:

| $k$ | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 12 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| $q_{0.99}(\hat R\mid k)$ | **1.0000** | **1.0000** | 0.9976 | 0.9864 | 0.9648 | 0.9039 | 0.8381 | 0.7833 | 0.6363 |

The median realised fold quality of a routed injection is $\hat R = 0.9719$. Inverting the table:
$k_{\min}=6$ for a median fold, $8$ for a $p_{25}$ fold, $3$ for a hypothetical perfect fold.
The analytic $\ln(N_{\rm eff}/\alpha)/\hat R^2 \approx 9.0$–$9.7$ is conservative by ~1.5×,
because real detected event sets carry hard-core repulsion (the 0.3 d de-duplication window)
and so form combs less readily than the uniform-iid model assumes.

### N-1.4 Validation 2 — out-of-sample scaling with baseline

The theorem predicts $P_{\max}=T_{\rm base}/\ln(N_{\rm eff}/\alpha)$. The injection sample contains
both 1-sector and 2-sector hosts, so the prediction can be tested out of sample on the *same*
detector, thresholds and planets — only the baseline differs.

| Host class | $T_{\rm base}$ (median) | $N_{\rm eff}$ | $W^\star$ | **$P_{\max}$ predicted** | **$P_{50}$ measured** |
|---|---|---|---|---|---|
| 1-sector | 24.9 d | 47.8 | 8.47 | **2.94 d** | **2.51 d** |
| 2-sector | 53.7 d | 105.4 | 9.26 | **5.80 d** | **5.00 d** |
| | | | | ratio **1.97** | ratio **1.99** |

Gate-open rate vs injected period, 669 routed calibration injections:

| $P$ (d) | 0.5 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| 1-sector | 0.782 | 0.732 | 0.702 | **0.083** | 0.000 | 0.000 |
| 2-sector | 0.571 | 0.639 | 0.581 | **0.636** | 0.212 | 0.118 |

The $P=4$ d column is the controlled comparison: identical planets, identical pipeline, 8.3 % vs
63.6 % routing, decided by baseline alone. The measurement sits just *inside* the predicted
ceiling in both classes, as an upper bound should.

### N-1.5 Validation 3 — the mechanism is the budget, not the seed

If long-period failure were a *seeding* problem, correct seeds would still route. They do not:

| $P$ (d) | 0.5 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| $\Pr(\text{seed correct})$ | 0.877 | 0.817 | 0.542 | 0.203 | 0.085 | 0.060 |
| $\Pr(\text{gate open}\mid\text{seed correct})$ | 1.000 | 0.980 | 1.000 | 0.333 | **0.200** | **0.000** |

*(deep planets, $R_p\ge8$ R⊕, so every transit is individually detected)*

Independently replicated on the 240-injection dress rehearsal: the $N_{\min}=2$ routing rate is
roughly flat in period (0.575–0.775, corr with $\log P$ = $-0.613$) while the FAP-gate pass rate
collapses (0.550 → 0.050, corr with $\log P$ = $\mathbf{-0.962}$). **The period dependence lives
entirely at the significance gate.**

### N-1.6 Falsification attempt — can a better statistic break the ceiling?

$\hat R$ is **not pivotal in $k$** (§N-3), which suggests replacing it with the pivotal Rayleigh
$Z$. Any statistic yields a valid Monte-Carlo test (the null is generated by the same map), so
this substitution is free in Type-I control and can only change power. It was tested across the
whole one-parameter family $T_\beta = \hat R\,k^{\beta}$ — $\beta=0$ is the sealed statistic,
$\beta=0.5$ is monotone-equivalent to $W=k\hat R^2$ — each **calibrated to the sealed null FAR
of 1.0626 %** on the M3-cleaned pool, then applied to 669 injections.

| $\beta$ | $\alpha^\star$ | null FAR | gate open | recall | Δ vs sealed |
|---|---|---|---|---|---|
| **0.0 (sealed)** | 0.00999 | 1.063 % | 0.4185 | 0.2840 | — |
| 0.2 | 0.00200 | 1.063 % | 0.4664 | 0.2990 | **+1.49 pp** |
| 0.3 | 0.00300 | 1.063 % | 0.4469 | 0.2960 | +1.20 pp |
| 0.5 (Rayleigh $Z$) | 0.00400 | 1.063 % | 0.4066 | 0.2855 | +0.15 pp |
| 1.0 | 0.01499 | 1.063 % | 0.3707 | 0.2750 | −0.90 pp |
| 1.5 | 0.05594 | 1.181 % | 0.3378 | 0.2646 | −1.94 pp |
| **conditional rank** (exactly pivotal) | 0.00971 | 1.181 % | 0.2900 | 0.1809 | **−10.31 pp** |

Sealed vs Rayleigh $Z$: 4 discordant one way, 3 the other, **McNemar exact $p=1.0$**.

Two conclusions.

1. **The ceiling is not an artifact of the sealed statistic.** The best member of the family gains
   1.49 pp overall and leaves $P=8$ d at 0.9 % and $P=16$ d at 0.0 % recall — unmoved.
2. **The multiplicity dependence is the evidence, not a nuisance.** Conditioning it away exactly
   costs 10.31 pp. This is the opposite of what "non-pivotal statistic ⇒ fix the statistic" would
   predict, and it is why the ceiling is structural.

### N-1.7 What the ceiling means for mission design

With $W^\star=\ln(N_{\rm eff}/\alpha)$ and $N_{\rm eff}\simeq 2T_{\rm base}/\text{d}$ at
$p_{\min}=0.5$ d:

| Baseline | $W^\star$ | $P_{\max}$ (sealed grid) | $P_{\max}$ (oracle: $N_{\rm eff}=1$) |
|---|---|---|---|
| 1 TESS sector (27 d) | 8.56 | 3.2 d | 5.9 d |
| 2 sectors (54 d) | 9.27 | 5.8 d | 11.7 d |
| 1 yr CVZ (351 d) | 11.16 | 31 d | 76 d |
| to reach $P=365$ d | 13.8 | **≈ 13.8 yr required** | ≈ 4.6 yr required |

The $N_{\rm eff}=1$ column is the **irreducible floor**: even a search that already knows the
period must clear $W\ge\ln(1/\alpha)=4.6$, i.e. ~5 coherent transits at $\alpha=0.01$. A full
periodic search needs 2–3. **Evidence-first routing requires roughly three times the baseline
that a direct search needs, for the same planet.**

---

## N-2. The subset-region property

Fast-path eligibility requires $\mathrm{SNR}_1\ge z_\star=3.4$ per transit *and*, by §N-1,
$N_{\rm tr}\gtrsim W^\star\approx9$. Therefore

$$\mathrm{SNR}_{\rm tot} \;=\; \mathrm{SNR}_1\sqrt{N_{\rm tr}} \;\gtrsim\; z_\star\sqrt{W^\star} \;\approx\; 10.2,$$

against the sealed TLS threshold $T = 10.74$ SDE. The fast path's eligible region is
(approximately) contained in the full search's detection region.

**Measured** on the 240-injection calibration dress rehearsal:

| | fast-path recoveries | also recovered by full TLS | fast-path-only |
|---|---|---|---|
| all cells | 37 | 28 | 9 |
| **excluding $P=0.5$ d** | **17** | **17** | **0** |

All nine apparent fast-path-only finds sit at $P=0.5$ d — the grid edge that the audit's own
edge control (§3.6) already established is an epoch-predicate artifact of the recovery rule, not
detection power. Outside it, $\Pr(\text{TLS recovers}\mid\text{fast path recovers}) = 1.0000$.

**Consequence.** For strictly periodic signals the architecture cannot add coverage; it can only
add or save compute. E1 non-inferiority was therefore near-tautological (erratum §2.8 measured
this as a weighting/fallback effect; §N-1 gives the underlying reason). The one regime where
evidence-first could add coverage is $N_{\rm tr}=1$, where no coherence test exists at all.

---

## N-3. What the period-FAP actually measures

Recording $(k_b,\hat R_b)$ for all 1,236,000 surrogates rather than the single exceedance bit:

- **Surrogate law.** $\log \hat R_b = 0.476 - 0.406\log k_b$ (theory: slope $-1/2$),
  corr $=-0.896$. So $\hat R$ is a strongly $k$-dependent quantity — **not pivotal**.
- **Variance decomposition.** **81.7 %** of $\mathrm{Var}(\log \hat R_b)$ is *between* multiplicity
  strata; 18.3 % is within-$k$ fold-quality variation.
- **Exceedance attribution.** **64.7 %** of all exceedances come from surrogates that produced
  *fewer* events than the observation — rising to **68.1 %** at $k_{\rm obs}\ge13$, the operating
  regime.
- Surrogate multiplicity is itself noisy: median $\mathbb E_b[k_b]/k_{\rm obs}=1.047$ with
  relative SD 0.231.

The sealed test compares $\hat R$ across surrogates whose own event counts fluctuate by ±23 %.
This is a *valid* Monte-Carlo test — validity needs only the same map applied to data and
surrogates — but the quantity being compared is dominated by multiplicity. This generalises
addendum §A.6 (which showed the $N=2$ FAP tests event *rarity*) to all $k$, and §N-1.6 shows the
dependence is load-bearing rather than spurious.

**The sealed $N_{\min}=2$ is inoperative.** With $q_{0.99}(\hat R\mid k)=1.0000$ at $k\le3$:

| | $k\le2$ | $k\le3$ | $k\le4$ |
|---|---|---|---|
| nulls routed | 0 / 25 | 1 / 54 | 2 / 83 |
| injections routed | 0 / 103 | 0 / 179 | 10 / 259 |
| **combined** | **0 / 128** | **1 / 233** | 12 / 342 |

The single $k=3$ routing (TIC 11649757, $\hat R=0.999868$) passed because *its own* surrogates
were atypically event-rich — $\Pr(k_b\le3)=0.036$ against a population median of 0.457 — i.e.
for a reason unrelated to fold quality. $N_{\min}=2$ admits 128 candidates to a gate it is
arithmetically impossible for them to pass. The effective floor is $k\approx4$–5.

---

## N-4. $\Lambda$'s null distribution — roadmap MATH-4, executed

MATH-4 asked for the empirical null of the GP likelihood-ratio with *estimated* $K$ against
$\chi^2_1$. It had never been run. 25,763 evaluations of `confirmer.transit_lr_gp` on 1,274
calibration stars: 20 random ephemerides drawn from the sealed search support per star, plus the
sealed route-and-seed ephemeris where one exists (283 stars).

**Random ephemerides** ($n=25{,}480$) — the null law of $\Lambda$ free of the seeding step:

| threshold | $\Pr(\Lambda\ge t\mid\mathcal H_0)$ | $\tfrac12\chi^2_1$ nominal | excess |
|---|---|---|---|
| 3.84 ("2σ") | 0.0748 | $2.5\times10^{-2}$ | 3.0× |
| 6.63 ("3σ") | 0.0487 | $5.0\times10^{-3}$ | 9.7× |
| **25.0** (the value hard-coded as "~5σ" in `no_secondary`) | **0.0181** | $2.9\times10^{-7}$ | **6.3 × 10⁴** |
| 100.0 | 0.0054 | $7.6\times10^{-24}$ | ~10²¹ |

$q_{0.99}(\Lambda) = 120.4$ against $\chi^2_1$'s 6.63 — **18× over-dispersed** at the 99th
percentile.

**At the sealed seed ephemeris** ($n=283$) it is far worse: median $\Lambda = 9.94$,
$\Pr(\Lambda\ge25)=0.233$, $\Pr(\Lambda\ge100)=0.103$.

**Mechanism.** The over-dispersion scales monotonically with the seeded duration:

| $T_{14}$ (d) | 0.05 | 0.10 | 0.20 | 0.40 | 0.80 |
|---|---|---|---|---|---|
| $q_{0.99}(\Lambda)$ | 14.5 | 23.8 | 48.3 | 84.9 | 109.4 |

This is the signature of a covariance model that under-states noise on the template's timescale
(§N-5). A secondary mechanism: `unit_transit_template` sets $a/R_\star=P/(\pi T_{14})$ clamped at
2.0, and the clamp binds for **31.1 %** of random and **17.0 %** of sealed-seed ephemerides — in
which case the "transit template" covers a median 21–24 % of all cadences and $\Lambda$ is
fitting a quasi-DC offset. Restricting to well-posed, short templates
($a/R_\star\ge2$, $n_{\rm in}/N<0.5$ %) still leaves $\Pr(\Lambda\ge6.63)=2.56$ %, **5.1×**
nominal.

**Three consequences.**

1. `no_secondary`'s comment calls $\Lambda_{\rm sec}\ge25$ "~5 sigma". Empirically it is
   $p = 1.8\times10^{-2}$, i.e. **≈ 2.1σ** — mis-labelled by five orders of magnitude in
   probability. It is nearly inert at the sealed operating point (`no_secondary_pass` = 100 % on
   the 283 sealed seeds), so no sealed result is affected, but the veto is calibrated to a
   distribution the statistic does not follow, and any future run inherits the error. (§C-6)
2. A **binding** photometric gate would need $T_{\rm red}\approx 4{,}340$ for a 1 %/star
   false-alarm rate on routed nulls (455 for 5 %, 100 for 10 %) — not the $\chi^2$-nominal ~25.
3. $T_{\rm red}=0$ makes the gate vacuous, so `confirmed` reduces to a **sign test** (§C-4), and
   $\Pr(\text{confirm}\mid\text{null})$ is **66.8 %** at seed ephemerides, 36.7 % at random ones.

---

## N-5. The residuals are red on transit timescales; $\mathrm{acf}_1$ is the wrong diagnostic

`frozen_rerun/detector.py` justifies its noise treatment with *"the near-white conditioned
residuals (M1 2.5 d diagnostics: acf_lag1 ~ 0.01)"*. `confirmer.estimate_kernel` builds the whole
Matérn-3/2 covariance from the lag-1 autocorrelation. Both use a **2-minute-cadence** statistic to
certify whiteness on **1–19-hour** timescales.

Direct measurement (250 calibration stars; $\kappa(T)\equiv\mathrm{sd}[\text{mean over }T]\big/(\sigma/\sqrt n)$;
$\kappa=1$ is white):

| $T_{14}$ (d) | $\kappa$ median | $p_{75}$ | $p_{90}$ | fraction $\kappa>1.5$ |
|---|---|---|---|---|
| 0.05 | 1.165 | 1.872 | 3.579 | 31.6 % |
| 0.10 | 1.242 | 2.352 | 4.899 | 36.0 % |
| 0.20 | 1.348 | 2.629 | 5.938 | 42.8 % |
| 0.40 | 1.478 | 3.225 | 7.755 | 48.8 % |
| 0.80 | 1.482 | 3.201 | 9.011 | 48.4 % |

Median $\mathrm{acf}_1 = 0.018$ — but $p_{90}(\mathrm{acf}_1) = 0.649$, and
$\mathrm{corr}(\mathrm{acf}_1,\kappa(0.8\,\text{d})) = 0.593$, explaining only 35 % of the
variance. **A near-zero lag-1 autocorrelation is fully compatible with $\kappa=4$ on transit
timescales.** The "acf₁ ≈ 0.01 ⇒ near-white" inference is not valid, and it is quoted as a
justification in the sealed detector docstring and implemented as the confirmer's noise model.

**Why the detector survives this and the confirmer does not.** `detect_events` normalises by
`1.4826 · MAD(depth series)` — the robust scatter measured *at that duration* — which **is**
$\kappa\sigma/\sqrt{n_{\rm in}}$ by construction. The detector is self-calibrating and $z_\star=3.4$
is a genuine 3.4 robust-σ on the correct timescale. The confirmer instead uses a *parametric*
$K$ fitted from lag-1, which cannot see $\kappa$ — hence §N-4. The generalisable lesson:
**empirical, timescale-matched normalisation is robust to unmodelled redness; a kernel fitted at
the cadence scale is not.**

---

## N-6. Surrogate contamination — roadmap MATH-3, executed, direction reversed

MATH-3 asks for "the argument that this only weakens the null ordering (**conservative
direction**)" plus a measurement on ~50 injections. The argument goes the other way.

`period_fap` block-bootstraps the same residual that carries the transits. Each surrogate
inherits the dips at scrambled epochs, which (i) inflates surrogate multiplicity $k_b$ and
(ii) therefore *lowers* $\hat R_b$, since $\hat R_b\propto k_b^{-0.41}$ (§N-3). Fewer exceedances,
smaller FAP: **anti-conservative**, not conservative.

Measured on 128 routed calibration injections, each FAP computed twice on the **identical RNG
stream** — surrogates drawn from $r$ (host + transit; sealed behaviour) vs from $r_0$ (host alone;
signal-free null):

| | sealed (contaminated) | clean null |
|---|---|---|
| median FAP | **0.0569** | **0.1578** |
| gate open | **53 / 128** | **24 / 128** |
| median $k$ | 8 (injected series) | 1 (clean host) |

64.1 % of injections have a smaller FAP under the contaminated null (Wilcoxon $p=1.5\times10^{-4}$).
**42 of the 53 fast-path routings — 79 % — exist only because the null was contaminated by the
signal being tested.** The effect is concentrated where it matters most:

| $P$ (d) | 0.5 | 1 | 2 | 4 | 8 | 16 |
|---|---|---|---|---|---|---|
| gate open, sealed | 0.696 | 0.773 | 0.625 | 0.227 | 0.000 | 0.000 |
| gate open, clean null | 0.217 | 0.136 | 0.208 | 0.318 | 0.150 | 0.059 |

**Scope of the consequence.** False-alarm control is *unaffected* — a true null has no signal to
leak, and the α = 0.01 gate measures 1.06 % on the cleaned pool (§N-7). What is affected is
(a) the meaning of a reported FAP for a routed candidate, which is not the p-value of a
signal-free null, and (b) the routing fraction $f_p$, hence the E2 compute endpoint. A
first-order rescaling ($24/53 = 0.45$) would take the measured $f_p=0.237$ to $\approx0.11$ and
roughly double $\pi^\star$; that is an estimate from a 128-row calibration sample, not a
re-measurement, and it should be computed properly before being used.

---

## N-7. Confirmation — the M3 null cleaning was load-bearing, and the gate is calibrated *only at* $\alpha=0.01$

The sealed gate's false-alarm control was re-measured from the 1,126 stars INN-3 also used, split
by whether M3's EB/variable cleaning retained them.

| Pool | $n$ | $\Pr(\widehat{\rm FAP}\le0.01)$ | vs nominal | one-sided $p$ |
|---|---|---|---|---|
| all | 1126 | 2.40 % | **2.40×** | $4.3\times10^{-5}$ |
| **M3-cleaned** | 847 | **1.06 %** | **1.06×** | 0.47 |
| M3-excluded | 279 | 6.45 % | **6.45×** | $7.9\times10^{-10}$ |

**The cleaning worked and it was necessary.** The sealed 1.05–1.08 % is reproduced; the excluded
eclipsing-binary and variable population would have inflated the routing false-alarm rate 6.5-fold.

But the FAP is **not a uniform $p$-value**, even on the cleaned pool (KS $D=0.110$,
$p=2.5\times10^{-9}$; median 0.424 rather than 0.5). It is calibrated at the tail where it is used
and conservative-to-anticonservative elsewhere: ratio 0.68 at $\alpha=0.05$, 0.81 at 0.10, 1.12 at
0.25, 1.17 at 0.50. This is expected — a circular block-bootstrap resample is not exchangeable
with the original series, so exact uniformity was never guaranteed — but it has a practical
consequence: **the empirical calibration does not extrapolate.** Any future run at a different
$\alpha$ (a Phase-II clean-skip tier, for instance) inherits no false-alarm guarantee from Seal #2
and must re-measure.

---

# PART II — CORRECTIONS TO THE SEALED MATHEMATICS

*(All are recorded here, per P-2; no sealed document is edited.)*

## C-1. MATH §4b — contamination fragility is linear, not quadratic

MATH §4 presents phase concentration (a) and pairwise differences (b) as "**two equivalent
formulations**", derives from (b) the "**fundamental fragility**"
$\binom{k_{\rm true}}{2}/\binom{k}{2}\approx(1+\rho_{\rm FP})^{-2}$, and attributes the quadratic
degradation to period recovery in general. The code implements (a). For (a) the degradation is
**linear**: $\mathbb E[\hat R]=(1+\rho_{\rm FP})^{-1}$, verified to three decimals (§N-1.1).
The two formulations are not equivalent in contamination robustness. Direction of the correction
is **favourable** — the implemented estimator is more robust than the sealed theory claims — but
the stated fragility is the wrong power law and MATH §10.2's "understated $(1+\rho_{\rm FP})^{-2}$
fragility" inherits the error.

## C-2. MATH §9 — the "identical grid" premise is false, and the deviation is load-bearing

MATH §9 specifies: *"recompute the maximized statistic $T^{(b)}$ over the **identical** grid …
Because each surrogate is maximized over the same $N_P$ periods, the look-elsewhere effect is
**automatically** absorbed."* Audit §3.3 certifies this. `best_period` derives the grid from the
epochs it is handed — `span` from the *surrogate's* events, `p_max ← min(p_max, span)`,
`df = 1/(oversample·span)` — so every surrogate is maximised over its own grid.

Measured: **96.9 %** of surrogates use a different number of trial frequencies than their
observation; 46.4 % use strictly fewer; the $p_5$–$p_{95}$ ratio is 0.735–1.528.

Re-running all 1,236 stars with the surrogates forced onto the observation's grid (MATH §9 as
written):

| | sealed (own grid) | MATH §9 (identical grid) |
|---|---|---|
| gate open | 37 / 1236 (2.99 %) | **54 / 1236 (4.37 %)** |
| $g_e$ changed | — | 92.8 % of stars (median $\|\Delta\|=6$) |
| gate flips | — | 23 (20 shut→open, 3 open→shut) |

**18 of the 23 flips are $k=2$ stars with $\hat R = 1.000000$ exactly** — the degenerate tie set.
Their own (4–66-point) observed grid is far smaller than their surrogates' grids, so under the
sealed code the surrogates get many more chances to reach $\hat R=1$ and the gate shuts; forcing
the identical grid collapses $g_e$ to 0 and the gate opens.

**So the unstated implementation deviation is what protects the sealed pipeline from routing
$k=2$ candidates.** Implementing the specification as written would raise the null false-alarm
rate by 46 %. Two things follow: the sealed results are safe (the implemented test is the more
conservative one, and it is what was calibrated), and MATH §9's stated justification is wrong
twice over. The correct condition for look-elsewhere absorption in a Monte-Carlo test is that the
**same measurable map** is applied to data and surrogates — which the code satisfies — not that
the same grid is used, which it does not.

## C-3. Seal #2's $N_{\min}=2$ is inoperative

See §N-3: 0 of 128 candidates with $k\le2$ ever routed; 1 of 233 with $k\le3$, for a reason
unrelated to coherence. $q_{0.99}(\hat R\mid k)=1.0000$ exactly at $k\le3$. The sealed floor
should have been $k\approx5$. This costs nothing in recall (the gate was going to shut anyway)
but it costs compute: every $k\in\{2,3\}$ candidate pays a full $B=1000$ bootstrap for a
foregone conclusion. That is 233 of 1,905 evaluations here — a directly removable slice of
$\rho_d$, complementary to INN-3's curtailment and provable in advance rather than at run time.

## C-4. The confirmation gate is algebraically a sign test

`transit_lr_gp` returns $\Lambda := 0$ whenever $\hat\delta\le0$, so $\Lambda\ge0$ always. With
the sealed $T_{\rm red}=0.0$, `confirmed = (lam >= T_red) and sign_pass and shape_pass` reduces
**identically** to

$$\texttt{confirmed} \iff \hat\delta > 0 \;\wedge\; \texttt{shape\_pass}.$$

Erratum §2.9 and audit §3.4 state that the timing gate is the binding arbiter. What had not been
measured is the photometric gate's own null pass rate: **66.8 %** at sealed seed ephemerides.

There is a second, sharper problem: **the sign test is circular.** The seed epoch is
`ev[argmax(SNR), 0]` — the location of the largest detected flux decrement — so $\hat\delta>0$ is
nearly forced. Measured $\Pr(\hat\delta>0)$: **0.8587** at the seed ephemeris vs **0.4438** at a
random one. This is the same defect MATH §10.3 diagnoses in v3 ("the reported SNR was built from
quantities the detection threshold *forces* to exceed $z_\star$"), relocated from the detector to
the confirmer. The charter's Principle 2 is not merely unrealised at the sealed operating point;
the statistic standing in for it is conditioned on its own seed.

## C-5. INN-3's curtailment — prior art

Addendum §E.2's curtailment proposition is correct and its proof is sound, and it correctly
distinguishes itself from Gandy-style sequential testing. For the record, stopping a Monte-Carlo
test at a fixed exceedance count to save computation is the standard **sequential Monte-Carlo
test** of Besag & Clifford (1991, *Biometrika* 78, 301–304); the decision-identity argument for a
fixed-level gate is the curtailed special case. The novelty claim should be scoped to the
application and the measured factor, not the method. *(Reference cited from memory; verify before
publication.)*

## C-6. `no_secondary`'s "~5 sigma" is ≈ 2.1σ

`confirmer.py:171` rejects on $\Lambda_{\rm sec}\ge25$ with the comment `# ~5 sigma secondary`.
Empirically $\Pr(\Lambda\ge25\mid\mathcal H_0)=1.81$ % (§N-4). Inert at the sealed operating point;
wrong for any future run, and wrong in the recall-losing direction (a false veto kills a planet).

---

# PART III — VERDICT ON NOVELTY

### What is **proved** (derivation + numerical verification)

| Result | Status |
|---|---|
| $W=k\hat R^2$ is the evidence scale; $\Pr(\hat R\ge r\mid k)\simeq e^{-W}$ | Standard Rayleigh asymptotics; verified against 1.24 M surrogates for $k\gtrsim8$ |
| $W\le N_{\rm tr}/(1+\rho_{\rm FP})$ | Derived; verified to ~2 % |
| Gate $\Rightarrow W\ge\ln(N_{\rm eff}/\alpha)$, hence $P\lesssim T_{\rm base}/\ln(N_{\rm eff}/\alpha)$ | Derived; 98.71 % gate prediction with zero free parameters; baseline scaling confirmed out of sample |
| Curtailment decision-identity (addendum §E.2) | Correct; prior art (§C-5) |
| $T_{\rm red}=0 \Rightarrow$ confirmation $\equiv$ sign test ∧ vetoes | Algebraic identity |
| MATH §4b's quadratic fragility does not apply to the implemented estimator | Derived + verified |

### What is **validated experimentally** (calibration data, not proved in general)

- The routing ceiling's empirical constant: $k_{\min}=6$ at median realised fold quality.
- 82 % / 18 % multiplicity / coherence decomposition of the sealed null statistic.
- $\Lambda$'s null over-dispersion and its scaling with $T_{14}$; $T_{\rm red}\approx4{,}340$ for a 1 % photometric FAR.
- $\kappa(T_{14})=1.17$–1.48 median, $p_{90}$ up to 9.0; $\mathrm{acf}_1$ explains 35 % of it.
- 79 % of fast-path routings are enabled by surrogate contamination.
- MATH §9's identical-grid specification would raise the null FAR from 2.99 % to 4.37 %.
- Subset region: 17/17 fast-path recoveries also found by full TLS.
- FAP tail calibration: 1.06× on the cleaned pool, **6.45×** on the M3-excluded (EB/variable) stars — the null cleaning was load-bearing and worked.

### What remains **open**

1. **The ceiling's exact constant.** The analytic $\ln(N_{\rm eff}/\alpha)$ is conservative by
   ~1.5× because detected event sets are not uniform-iid (hard-core repulsion from the 0.3 d
   de-duplication). A closed form for $N_{\rm eff}$ under a hard-core point process would sharpen it.
2. **Monotransit ($N_{\rm tr}=1$).** The ceiling says nothing here because no coherence test exists.
   This is the only regime where evidence-first can add *coverage* rather than save compute, and
   it is untested (H3, deferred).
3. **The clean-null routing fraction.** §N-6's rescaling of $f_p$ and $\pi^\star$ is an estimate
   from 128 rows, not a measurement.
4. **Whether a non-coherence seeder evades the ceiling.** The bound applies to gating on phase
   coherence. A seeder that passes candidates to the photometric gate *without* a coherence
   significance test would not be bound by $\ln(N_{\rm eff}/\alpha)$ — but would then need the
   photometric gate to carry the whole false-alarm budget, which §N-4 shows it currently cannot.
   This is the natural Phase-II design question and it is now well-posed.

### Where the genuinely novel contribution is

Not in the routing architecture. The subset-region property (§N-2) says it cannot find planets a
full search misses, and the ceiling (§N-1) says it is confined to $P\lesssim0.2\,T_{\rm base}$ —
a regime where the full search is already cheap and reliable.

The defensible novel content is the **negative result itself, in closed form**: a bound on
evidence-first period recovery that is derived, validated with zero free parameters, confirmed
out of sample in its scaling, and **survives a deliberate falsification attempt across a family of
alternative statistics including the exactly-pivotal one**. It is a statement about what the
paradigm can never do, and it generalises beyond VESPER to any pipeline that detects events first
and then tests them for periodicity.

That result also supports the methodological framing already on the table (roadmap INN-1,
"sealed single-shot validation with pre-committed verdicts"). This audit is a second instance of
the same pattern: the protocol forced the project to withdraw its own headline verdict once
(DR-003), and the mathematics now explains why the surviving claim was structurally guaranteed.

---

# PART IV — Reproduction

```
research/math_audit/
  surrogate_table.py          nulls | injections | verify   — records (k_b, R_b, span, n_freq)
                              for all B surrogates; `verify` asserts bit-identity vs INN-3
  lambda_null.py              25,763 Lambda evaluations, random + sealed-seed ephemerides
  grid_identity.py            re-scores every surrogate on the observation's grid (MATH §9)
  surrogate_contamination.py  paired FAP: host+transit vs host alone, identical RNG stream
  findings.py                 consolidates every reported number -> findings.json
```

```bash
.venv/bin/python research/math_audit/surrogate_table.py nulls      --workers 8
.venv/bin/python research/math_audit/surrogate_table.py verify        # must print BIT-IDENTICAL True
.venv/bin/python research/math_audit/surrogate_table.py injections --workers 7 --per-cell 30
.venv/bin/python research/math_audit/lambda_null.py                --workers 6 --n-rand 20
.venv/bin/python research/math_audit/grid_identity.py              --workers 8
.venv/bin/python research/math_audit/surrogate_contamination.py    --workers 8 --per-cell 6
.venv/bin/python research/math_audit/findings.py
```

Artifacts land in `data/manifests/math_audit/`. Total ~35 min on 8 cores.
Seeds are fixed (20260616 / 20260619 / 20260827); the null surrogate stream is the sealed one.

**Not in git:** `null_surrogates.npz` (19.6 MB) and `inj_surrogates.npz` (9.8 MB) are excluded by
the repository's global `*.npz` rule. They are the raw surrogate tables and are regenerated by the
first and third commands above in ~13 min; `surrogate_table.py verify` then re-derives the sealed
exceedance counts from them and asserts bit-identity, so their absence costs reproducibility
nothing. Every number quoted in this report is carried by the committed CSVs and `findings.json`.

**Compliance — verified this session, not asserted.**

| Check | Result |
|---|---|
| TEST TICs read (P-5) | **0** — every input is `data/processed/m1/*.npz` (calibration) or an existing calibration artifact |
| Sealed docs vs `phase1-prereg-v3`, branding-normalised | `SCIENTIFIC_HYPOTHESIS.md` **0** · `VESPER_PHASE1_VALIDATION.md` **0** · `VESPER_MATHEMATICAL_FOUNDATIONS.md` **0** differing lines |
| Seal #2 manifest SHA-256 | `5baf15df61fad9ddc236293baa7e8d446ec306d452e450ce895ec2ff9a453d38` — matches the DR-001 §5a post-rebrand value |
| `research/m4_evaluation/frozen_rerun/` | clean (`git status --porcelain` empty) |
| Sealed statistic reproduced | `ge` bit-identical on 1,126/1,126 calibration nulls |

```bash
# branding-normalised sealed-document check (the rebrand renamed the files, so compare by path pair)
norm() { sed 's/TRINETRA[-_]X/VESPER/g; s/TRINETRA/VESPER/g'; }
diff <(git show phase1-prereg-v3:docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md | norm) \
     <(norm < docs/VESPER_MATHEMATICAL_FOUNDATIONS.md)          # -> empty
shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json
```

Everything written by this audit is new and additive: `research/math_audit/` and
`data/manifests/math_audit/`. No existing tracked file was modified.
