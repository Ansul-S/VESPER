# RES-2 — KM-period-weighted E1 sensitivity

Source: Kunimoto & Matthews 2020, Table 7 / Eqn 22-25 (arXiv:2004.05296). Margin: **-2 pp**. n=15000 injections, 40 hosts. w_R held at sealed KM values; only the period dimension changes.

| Weighting | ΔR̄ (pp) | injection lo95 | host-cluster lo95 | Wilson lo95 | PASS |
|---|---|---|---|---|---|
| log-uniform w_P (sealed A.5) | -0.48 | -0.60 | -0.82 | -0.60 | ✅ |
| KM Eqn-25 w_P, P=0.5 extrapolated below KM support | -0.16 | -0.18 | -0.22 | -0.18 | ✅ |
| KM Eqn-25 w_P, P=0.5 node excluded (renormalized) | -0.16 | -0.18 | -0.22 | -0.18 | ✅ |

**Period weight by node (summed over radius):**

| scheme | P=0.5 | P=1 | P=2 | P=4 | P=8 | P=16 |
|---|---|---|---|---|---|---|
| sealed | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 | 0.167 |
| km_extrap | 0.002 | 0.010 | 0.036 | 0.121 | 0.300 | 0.530 |
| km_excl | 0.000 | 0.010 | 0.037 | 0.122 | 0.301 | 0.531 |

**Conclusion.** E1 PASS is robust to the period-weighting scheme: all three interval constructions clear the -2 pp margin under sealed log-uniform AND KM occurrence weighting (both P=0.5 handlings).
