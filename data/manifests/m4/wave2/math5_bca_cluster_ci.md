# MATH-5 — BCa host-cluster interval for E1

**Scope.** Robustness check reported ALONGSIDE the sealed percentile bound. The pre-registered E1 decision rule is unchanged and is not re-decided here.

Sample: 15000 eligible injections across 40 hosts and 30 cells; B = 20000, seed 20260616.

| Quantity | Value |
|---|---|
| Point estimate $\overline{\Delta R}$ | -0.48 pp |
| One-sided 95% lower bound — **percentile** (sealed endpoint) | -0.83 pp |
| One-sided 95% lower bound — **BCa** | -1.04 pp |
| Difference (BCa − percentile) | -0.21 pp |
| Sealed margin | -2 pp |
| Bias correction $z_0$ | -0.1273 |
| Acceleration $a$ | -0.1331 |
| Effective lower-tail probability | 0.0072 (vs 0.05 nominal) |

**Conclusion.** E1 point estimate -0.48 pp. One-sided 95% lower bound: -0.83 pp (percentile) vs -1.04 pp (BCa), a difference of -0.21 pp. Both are above the sealed -2 pp margin, so the E1 non-inferiority conclusion is unchanged under second-order-accurate inference.

**Small-cluster caveat.** The acceleration is estimated from a leave-one-out jackknife over only 40 host clusters. With that few units the third-moment estimate is itself noisy, so BCa's correction is indicative rather than definitive; it is reported as a robustness check, not as a replacement for the sealed percentile endpoint. A cluster bootstrap with <~50 units is known to under-cover somewhat regardless of the interval method — the honest reading is that both bounds sit well inside the -2 pp margin, not that either is exact to the last decimal.
