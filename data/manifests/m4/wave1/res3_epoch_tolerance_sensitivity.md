# RES-3 — Epoch-tolerance sensitivity of E1

**Scope:** COMBINED-side only (TLS per-injection epoch not stored); ΔR̄ curve is an upper bound on the symmetric improvement. Symmetric sweep = compute task.

## ΔR̄ vs combined-arm epoch tolerance (occurrence-weighted, sealed w_c)

| tolerance (T14) | ΔR̄ (pp) | host-cluster lo95 (pp) | combined recall (unwtd) |
|---|---|---|---|
| ±0.5 | -0.48 | -0.82 | 0.4883 |
| ±0.625 | -0.30 | -0.57 | 0.4992 |
| ±0.75 | -0.17 | -0.40 | 0.5078 |
| ±0.875 | -0.08 | -0.31 | 0.5134 |
| ±1.0 | -0.00 | -0.23 | 0.5185 |

## Loss reclassification (losses = TLS-recovered, combined-missed at ±0.5)

- Total losses: **869** — 693 right-period, 176 wrong-period (epoch tolerance cannot recover wrong-period).

| loosen tolerance to | right-period losses recovered |
|---|---|
| ±0.5 T14 | 0 |
| ±0.625 T14 | 145 |
| ±0.75 T14 | 260 |
| ±0.875 T14 | 334 |
| ±1.0 T14 | 402 |

Gains: 563 total, 561 at P=0.5 d (TLS epoch failures per the edge control, erratum §6).

**Conclusion.** E1's loss structure is dominated by the +/-0.5 T14 epoch predicate: all 869 losses are confirmed-cheap seeds, 693 right-period; loosening the combined epoch tolerance to 0.75/1.0 T14 recovers 260/402 of them, lifting the combined-side ΔR̄ from -0.48 pp to -0.00 pp. The losses are a predicate/epoch-precision artifact, not a detection-power gap — motivating an epoch-refit confirmer (INN-4). A fair symmetric sweep (needs stored TLS epochs) would recover TLS's own wrong-epoch cases too (the P=0.5 d gains), so these are upper bounds.
