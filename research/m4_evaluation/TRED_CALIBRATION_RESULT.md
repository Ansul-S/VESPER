# T_red Calibration — RESULT (CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-19 |
| **Status** | **COMPLETE.** T_red set by FAR target (P-3); recall preview reported (non-setting). |
| **Run** | 854 cleaned-null stars (163 routed) + 114 routed injections; genuine transit-LR confirmer (`confirmer.py`, D-1a/D-2a/D-3-i); 0 TEST TICs. |

## Calibrated threshold

| Quantity | Value |
|---|---|
| **T_red** | **0.0 (non-binding)** — FAR target met without a binding confirmer threshold |
| FAR target | ≤ 1 %/star (= Arm A's target) |
| FAP-gate pass rate (nulls) | 9/854 = 1.05 % (≈ M3 sealed 1.08 % ✓) |
| Achieved end-to-end Arm-B FAR | **0.12 %** (1/854) |
| allowed false confirmations at FAR≤1% | 8 |

T_red is set **solely** from the FAR target (the smallest threshold whose end-to-end false-confirmation rate ≤ 1%). Because only **1** of the 9 FAP-gate-passing nulls survives the confirmer, the count (1) is already below the allowed 8, so T_red is **non-binding (0)**. It was **not** tuned to any recall/E1/E2 objective.

## The genuine transit-LR confirmer adds real FP rejection

Of the **9** nulls passing the period-FAP gate, the confirmer rejects **8**:
- Λ = 0 (no transit-shaped dimming at the seed), or
- shape-vetting failure (e.g. tic 155944894: Λ=25 but fails odd-even/secondary → EB-like, correctly killed).

→ FAR **1.05 % → 0.12 %**. Unlike the dry-run **box** depth-S/N (T_red degenerate, confirmer did nothing), the transit-template LR with shape vetting performs genuine false-positive rejection. NN#3 arbiter is functioning.

## Recall preview (REPORTED only; T_red set by FAR, not recall — P-3)

| Metric | Value |
|---|---|
| AUC(planet vs null Λ) | **0.894** (≥ dry-run box-S/N 0.877 ✓) |
| Fast-path recall (all routed inj) | 46 % |
| Fast-path recall (Rₚ≥4) | 51 % |
| Fallback fraction | 54 % |

**The 54 % fallback is dominated by period-seed error, not the confirmer:** of 62 non-confirmed routed injections, **54 had the wrong period seeded** (the known evidence-first failure mode); **0** period-matched planets were lost to Λ=0; only **8** period-matched ones failed shape vetting. Non-confirmed stars fall back to full TLS → **combined recall protected** (consistent with the dry-run E1 PASS).

## Attribution caveat (for the record)

Arm B's achieved FAR (0.12 %) is **below** Arm A's (~1.08 %), and T_red is floored at 0 (sign-aware Λ≥0), so the **period-FAP gate is the binding FP constraint** — Arm B is held to *stricter* precision than Arm A at the common-FAR operating point. This is conservative for Arm B's recall comparison (Arm B is not credited with a looser FAR) and is reported, not hidden.

## Artifacts
`data/manifests/m4/tred/` — `tred_nulls.csv`, `tred_injections.csv`, `tred_summary.json`, `run_full.log`.
