# M4 Dry-Run Validation Report

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Mode** | DRY-RUN — CALIBRATION cached residuals, fully offline, **no TEST access** |
| **Purpose** | Validate the complete M4 code path before the single sealed-TEST run (per owner approval 2026-06-18) |
| **Verdict** | **Machinery validated; TWO findings on the targeted (Arm B) search must be resolved before the TEST run.** One is a fixable implementation bug; one is a methodology issue that likely needs owner sign-off / re-registration. |
| **TEST status** | **Untouched.** No TEST row read. |

---

## 1. Objectives & results

| # | Dry-run objective | Result |
|---|-------------------|--------|
| 1 | Validate complete M4 code path end-to-end | ✅ Runs to completion (exit 0); all artifacts written |
| 2 | Verify split guards prevent TEST access | ✅ All guard tests pass (§2) |
| 3 | Injection, conditioning, recovery accounting, artifact generation | ✅ Validated (offline host mode); production raw+recondition path = M2 code (network) |
| 4 | Arm A & Arm B use identical sealed TLS configuration | ✅ Same engine/config — **and this exposed Finding A** |
| 5 | E1 weighting/bootstrap machinery | ✅ w_c loaded from Seal #2 (Σ=1, 92.83% on Rₚ≤2); paired bootstrap runs |
| 6 | E2 timing ledger + repeat-timing workflow | ✅ Ledger produced — **and this exposed Findings A & B**; one efficiency fix noted (§5) |
| 7 | Final artifact inventory | ✅ §6 |

## 2. Guards (single-shot discipline) — ALL PASS

- `dry_run` reading TEST → **blocked** (`dry-run is FORBIDDEN from reading the TEST split`).
- `test` run without / with wrong confirmation token → **blocked**.
- `test` mode with `split=calibration` → **blocked**.
- Run config attempting to override a sealed key (`z_star`, `T_sde`, …) → **blocked**.
- Seal #2 hash verified (`6292c018…`) and m3_config hash verified (`0400e2db…`) on every load; mismatch → fail closed.

## 3. Machinery validated (sane behaviour)

- **Recovery accounting** is physically correct: an Rₚ=4 / 1036 ppm injection recovered by both arms at SDE 18.8 ≥ T (harmonic-flagged); Rₚ=1 / 57 ppm and Rₚ=2 / 425 ppm correctly **not** recovered (SDE 5.95, 8.17 < T=10.74).
- **Routing** behaves per spec: 1-event signal → `fallback_full`; 2-event weak-FAP (0.16 > α=0.01) → `fallback_weak_fap`; strong 44-event signal (FAP 0.001 ≤ 0.01) → **`targeted`**.
- **E1** weighting + paired injection bootstrap execute and produce a one-sided 95% lower bound + PASS/FAIL.
- **E2** per-stage ledger + ≥5 warm-cache repeats on the stratified subset execute.

## 4. FINDINGS (block the TEST run until resolved)

### Finding A — TLS silently discards the narrow targeted window (implementation; fixable)
`transitleastsquares.grid.period_grid` restricts the optimal-frequency grid to `[P̂(1−ε), P̂(1+ε)]`, but if the in-window count `< MINIMUM_PERIOD_GRID_SIZE = 100` it **warns and recursively returns the full default grid** (`grid.py:146–154`). At the sealed ε=0.01 and oversampling=3, a ±1% window naturally holds only **~20–35 periods** (< 100), so the targeted arm **always reverts to the full search**:

| Call | Periods searched | Range | Cost |
|------|------------------|-------|------|
| Full | 4971 | 0.60–24.8 d | 164 s |
| "Targeted" via `power(period_min,period_max)` | **4971 (fell back)** | 0.60–24.8 d | 162 s → **ratio 0.995** |
| Targeted via explicit in-window grid (35 periods) | 35 | 1.376–1.403 d | **1.7 s → ratio 0.0103** |

M3 never hit this because calibration only ran `full_tls`. **Fix:** feed TLS the in-window optimal-frequency subset directly (preserves "TLS optimal-frequency sampling, oversampling 3", just the periods inside the sealed window). Compute savings are then real (~99%).

### Finding B — TLS SDE is not comparable across grid widths (methodology; needs sign-off)
TLS **SDE = (peak − mean)/std of the power spectrum over the searched grid**. On a narrow window every period sits near the peak, so the contrast collapses. At the **identical** period (1.389 d) on the **same** light curve:

| Grid | SDE | vs T=10.74 |
|------|-----|------------|
| Full (4971 periods) | **40.36** | PASS |
| Targeted (35 in-window periods) | **3.55** | **FAIL** |

Δ = **−36.8**. A real planet that clears T on the full grid **fails T on the targeted grid**. The sealed protocol's "**targeted TLS on [P̂(1±ε)], SDE ≥ T**, single common T both arms" (VAL §2/§4.1, A.1/A.4) is therefore **internally inconsistent**: SDE is not invariant to search range, so one threshold cannot serve both arms. As written, Arm B would reject planets Arm A accepts → **E1 recall non-inferiority would fail by construction**, while Arm A and Arm B "agreeing at equal precision" (the fairness keystone) does not hold for the SDE statistic.

This directly couples the two primary endpoints: the grid restriction that delivers E2's compute saving is the same restriction that destroys Arm B's SDE and would fail E1.

## 5. Efficiency note (non-blocking)
The E2 timing loop currently re-runs `arm_b_combined` (full B=1000 FAP + TLS) once for the `cost_tls` stage *and* separately times `route`+`period_fap` — double-counting the heavy stages. Restructure to run Arm B once per repeat and decompose its internal stage timers. Also: the recall pass is serial; the full campaign must use the M3 `Pool`/`imap_unordered` pattern. Indicative full-campaign cost (≥15k injections, dual-arm, parallel over ~8 cores): **~3–5 days** wall-clock — heavier than "overnight"; plan batching.

## 6. Artifact inventory (the M4 run will generate)
- `m4_per_injection.csv` — per-injection, both arms: period/epoch/SDE, recovered, harmonic, route, FAP, n_events.
- `m4_e1_per_cell.csv` — per-(P,Rₚ): n, w_c, R_comb, R_tls, ΔR.
- `m4_e2_ledger.csv` — fast-path-eligible subset: cost_full / cost_detector / cost_period / cost_tls / cost_comb (+ sd), ≥5 repeats.
- `m4_provenance.json` — mode/split, both sealed hashes, frozen values used, E1 + E2 summaries, anti-tuning attestation, seed, machine.
- (production adds) survey-sample per-star ledger for E3/π⋆ (collected, not interpreted at M4).

## 7. Recommendation
- **Finding A:** apply the in-window-grid fix in `arms.py` (implementation; no sealed value changes). Re-validate on the dry-run.
- **Finding B:** **stop and consult.** The targeted-arm confirmation statistic vs a full-grid-calibrated T is a sealed-methodology question. Resolving it (e.g., a period-fixed depth-SNR arbiter, a separately-calibrated targeted threshold, or a minimum-width window that preserves SDE) likely requires a **new pre-registration**, since it changes A.1/A.4 and possibly adds/changes a frozen threshold. Do **not** read TEST until this is settled.
