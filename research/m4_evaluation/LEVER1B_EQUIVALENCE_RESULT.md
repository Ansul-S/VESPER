# Lever-1b Equivalence Validation — RESULT (CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-19 |
| **Status** | **COMPLETE. VERDICT: FAIL → confirmer-only fallback** (pre-registered, DR-002 §2.3a / plan §6). |
| **Run** | 854 cleaned-null stars (833 routed) + 155 routed injections across 13 (P,Rₚ) cells; B=1000 reference vs E-EVT(GPD, B′=100) on the **same** surrogate draw; 42.8 min, 6 workers. |
| **Integrity** | 0 TEST TICs (asserted); 0 contaminants; sealed config unchanged; null FAP-gate pass rate 9/854 = 1.05% ≈ M3 sealed 1.08% (provenance check ✓). |

## Verdict per pre-stated criterion (plan §4 — tolerances fixed before results; not relaxed)

| Criterion | Threshold | Observed | Result |
|---|---|---|---|
| **(i) FAP agreement** | p95 \|ΔFAP\| ≤ 0.005 | **0.085** (17×); median 0.013; corr 0.988 | **FAIL** |
| **(ii) gate-membership** | discordant ≤ 8 **and** 0 FP-admit | discordant **9**; **7** admit nulls the bootstrap rejects | **FAIL** |
| **(iii) recall-safety (NN#1)** | 0 recoveries clipped | **2 of 38** ref-pass period-matched clipped | **FAIL** |

**All three fail.** E-EVT is **not** numerically equivalent to the sealed B=1000 bootstrap.

## Why it fails (interpretable, not an artifact)

- **FP inflation (ii)** is driven by **low-event-count stars**: 4 of the 7 wrongly-admitted nulls have n_events=2 (rest 5,7). With few events the resultant length R is **discrete/lumpy**, violating the GPD smooth-tail assumption → EVT extrapolates FAP→1e-6 while the bootstrap correctly returns 0.08–0.13. EVT cannot represent the discrete small-n tail.
- **Recall loss (iii)**: the opposite error — for 2 injected planets EVT over-estimates FAP (0.054, 0.011) vs bootstrap (0.009, 0.002), clipping them at the α=0.01 gate.
- The B′=100 GPD fit is unstable in the gate-relevant tail **in both directions**. A larger B′ would defeat the purpose (it is the bootstrap). The per-star EVT — the *higher-fidelity* candidate — fails decisively.

## Consequence (pre-committed)

Per DR-002 §2.3a and plan §6: **Lever 1b is dropped; v3 reverts to confirmer-only.** The operational period-FAP **is** the sealed B=1000 circular block bootstrap (VAL A.8, unchanged). ρ_d stays ≈ 12.4%. The estimator-of-record is **the bootstrap (fallback)**; A.8a admits **no** cheap estimator.

**Implication for M4:** with ρ_d ≈ 12.4% retained, E2 is expected to remain < 30% (the dry-run gave ~20–29%). The honest projected M4 outcome under confirmer-only v3 is **E1 pass (recall protected) / E2 fail → the pre-committed compute falsification** (VAL §7a). This is the discipline functioning: the cheap estimator was *required* to be equivalent, it is not, so the compute cost is **not** a removable artifact and the compute claim is not salvaged on these terms.

## Second candidate (E-LUT) — EVALUATED → also FAIL (owner-requested completeness)

E-LUT (precomputed uniform-epoch null R-distribution keyed on event-count k + baseline; "O(1) lookup", nsim=4000) was built and tested against the **same** stored bootstrap reference with the **identical** pre-stated criteria:

| Criterion | Threshold | E-LUT | E-EVT (for comparison) |
|---|---|---|---|
| (i) FAP agreement | p95 \|ΔFAP\| ≤ 0.005 | **0.104** (corr 0.82) | 0.085 (corr 0.99) |
| (ii) gate-membership | discord ≤ 8, 0 FP-admit | **discord 11, 9 FP-admit** | discord 9, 7 FP-admit |
| (iii) recall-safety | 0 clipped | **2 clipped** | 2 clipped |

**E-LUT FAILS all three, and worse than E-EVT** (corr 0.82 vs 0.99). Reason: the uniform-epoch null ignores each star's red-noise **event clustering** that the per-star block bootstrap preserves — a generic grid cannot reproduce per-star residual structure. Confirmed a-priori expectation.

**Both pre-registered candidates fail → the confirmer-only fallback stands**, now with a verdict on record for each named candidate (constraint #5). Artifacts: `elut_nulls.csv`, `elut_injections.csv`, `elut_summary.json`, `elut_run.log`.

## Artifacts
`data/manifests/m4/equivalence/` — `equiv_nulls.csv`, `equiv_injections.csv`, `equivalence_summary.json`, `run_full.log`.
