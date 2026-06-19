# M4 Combined-Arm System Dry-Run — Result (CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **What** | System-level E1 + E2 for the full recall-safe Option-2 architecture (route → red-noise epoch-fixed confirm → full-TLS fallback), measured on CALIBRATION. **No TEST. No seal change. No drafting.** |
| **Config** | 150 injections (30 cells ×5), 200 cleaned nulls for T_red, 12-star serial E2 timing. Confirmer = red-noise epoch-fixed MF (R2 LR-upgrade still pending). |
| **Headline** | **E1 PASS, E2 FAIL.** Recall is protected; the compute advantage does not materialize. |

## Results
- **E1 (recall non-inferiority):** ΔR̄ = **−0.39 pp**, one-sided 95% lower bound = **−0.80 pp** → **PASS** (margin −2 pp). The full-TLS fallback + occurrence weighting protect combined recall, exactly as the review board (F-2) anticipated. H1 is *supported* on calibration.
- **E2 (compute, fast-path-eligible/routed population):** combined/full = **0.799 → 20.1% reduction → FAIL** (needs ≥30%). A population mean-cost estimate gives **~29%** (the 12-star Σ-cost is dominated by long-baseline fallback stars); **both are below 30%.**
- routed 74% · confirmed-cheap 31% (= **41% of routed**) · **ρ_d = 0.124**.

## Why E2 fails (structural, not subset noise)
1. **ρ_d = 12.4%** — the sealed **B=1000 block-bootstrap period-FAP** is charged on *every* routed star (~10–22 s vs full TLS ~38 s). This is the R-1 risk materialized.
2. **59% of routed stars fail the FAP gate** (α_FAP=0.01, sealed) → forced **fallback to full TLS**, paying ρ_d **plus** the full search (cost > baseline). Only 41% confirm cheaply.
3. **T_red = 0 (degenerate)** — on the cleaned null pool almost no star produces a *confirmed* candidate (the FAP gate rejects them first), so the MF threshold is non-binding; the **FAP gate, not the confirmer, does the FP rejection.**

So even confirmed stars only save down to ρ_d≈12%, and the majority (59%) cost *more* than baseline → net reduction ~20–29% < 30%. The drivers (ρ_d and the FAP-gate fallback rate) are measured on the full 150 injections and are robust to the small timing subset.

## Pre-registered verdict mapping
VAL §7: **FALSIFIED** iff ΔR̄ lower bound < −2 pp **OR** E2 reduction < 30% at non-inferior recall. Here (on CALIBRATION) E1 is non-inferior **and** E2 < 30% → this is the **E2-falsification branch**. (Calibration, not the sealed TEST run — but it is a strong, mechanism-level predictor, and the cause is protocol-level, not data-specific.)

## Caveats
- E2 timing subset is **12 stars** (noisy Σ-cost); the population estimate (~29%) and the structural drivers corroborate "below 30%", but a larger timing pass would tighten it.
- Confirmer is the validated red-noise MF, **not** the R2 likelihood-ratio upgrade (which could change recall slightly but not ρ_d / the FAP-gate fallback rate — so unlikely to rescue E2).
- E2's failure is driven by **sealed** machinery (B=1000 FAP, α_FAP=0.01); rescuing it means re-opening A.8/routing, not just the Arm-B confirmer.

## Bottom line
On calibration, the Option-2 combined system **preserves recall (E1 pass) but does not deliver the ≥30% compute advantage (E2 fail)** — because the period-significance overhead and the FAP-gate fallback rate consume the saving. Combined with the review board's F-1 (non-neg #3) and F-4 (H2 redefinition), the evidence indicates **Option 2 does not salvage the compute claim**, and Finding B + this E2 shortfall together constitute a **Phase-I falsification of H2 (compute superiority), with H1 (recall non-inferiority) supported.**
