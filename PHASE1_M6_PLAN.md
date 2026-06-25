# PHASE1_M6_PLAN — Reality check + ablation + parameter-recovery completion

| Field | Value |
|-------|-------|
| **Milestone** | M6 (+ M5 remainder) — paper artifacts requiring new tooling/compute/data |
| **Date** | 2026-06-25 |
| **Status** | **DRAFT — owner sign-off required before ANY network or compute fires.** Execution-only milestone; no new frozen parameter, no hypothesis re-test. |
| **Produces** | T6 (reality check: TOI recall + EB false-positive rejection), T8 (gate ablation), T5-complete + F5-depth (depth/T₁₄ recovery), optional F7 (monotransit), F9 (gate before/after) |
| **Builds on** | Sealed result (`research/m4_evaluation/M4_TEST_RESULT.md`); M5 partial (F5/F6, T4/T5 period/epoch) |

> This is a **characterization** milestone for the paper, not a re-test of H1. The verdict (H1 falsified, compute branch) is final and unchanged. M6 strengthens the manuscript's rebuttals (R3, R4) by showing the gate works on *real* astrophysics and quantifying the gate's contribution.

---

## 1. HARD CONSTRAINTS (non-negotiable)

1. **NO TEST re-read (P-5).** The sealed test injections were read exactly once. M6 touches **only** (a) **CALIBRATION** injections (depth/T₁₄, ablation, monotransit) and (b) **real TOI/EB stars** (reality check) — never the test split. The single test evaluation stands.
2. **Sealed thresholds frozen (P-2 / NN#2).** `z⋆, z_mono, N_min, T, α_FAP, ε, w_c, π̂, T_red` are unchanged. M6 sets no threshold and tunes nothing. The ablation (W3) *removes/replaces* a component to measure its contribution — it does not re-tune the sealed system.
3. **Not a new amendment.** v3 remains the terminal protocol (no v4). M6 outputs are descriptive figures/tables, not hypothesis decisions.
4. **Network sandbox-off only for catalog/LC fetches**, as in M1/M4 conditioning. Conditioning uses the **frozen Stage-0** (2.5 d biweight, sectors 1–3) via the existing tooling.

---

## 2. Work items & deliverables

### W1 — Depth/T₁₄ recovery (completes M5 → T5-full, F5-depth)
The recovery driver did not log fitted depth/T₁₄ per injection. Re-run the **combined-arm confirmer with depth/T₁₄ logging on a CALIBRATION injection set** (the same grid; the dress-rehearsal hosts), and produce recovered-vs-true depth and duration scatter + median fractional errors and interval coverage. *Calibration, not test.*

### W2 — Reality check (→ T6)
- **TOI recall:** does the combined arm recover **real confirmed planets**? Sample = confirmed/known TOIs (disposition CP/KP) in sectors S1–S3, 2-min cadence. Condition (frozen Stage-0) → run Arm A (full TLS) + Arm B (route→FAP→confirmer→fallback) → report recall and where it differs.
- **EB false-positive rejection:** does the confirmer/gate **reject known eclipsing binaries**? Sample = the **158 already-identified EB/variable TICs** (`data/manifests/m3/calibration_exclusions.csv`, Prša 2022 + VSX) — many already conditioned in the M3 null draw (reduces fetch burden). Report the fraction rejected by (i) the period-FAP gate, (ii) the transit-LR confirmer's sign/odd-even/secondary vetting.

### W3 — Gate ablation (→ T8)
On **CALIBRATION** injections + nulls, re-run the combined arm in two ablated variants and compare to the sealed gate:
- **(a) no photometric gate** — confirm on the seed without the transit-LR shape/sign test;
- **(b) uncalibrated score** — replace the bootstrap period-FAP with a raw coherence/SDE cut.
Quantify the recall and false-positive change → shows what the calibrated photometric gate buys (defends novel-contribution #4; rebuts the v3 "FP = noise artifact" critique, R3).

### W4 (optional) — F7 monotransit + F9 before/after
- **F7:** a small single-event injection campaign (long period / partial-coverage) to exercise the monotransit regime absent from the sealed grid. *Calibration.*
- **F9:** a single illustrative star — timing-coherence "detection" vs photometric-gate rejection (dramatizes contribution #4). *Calibration / a known EB.*

---

## 3. DESIGN DECISIONS FOR SIGN-OFF (choose before execution)

| # | Decision | Options / recommendation |
|---|----------|--------------------------|
| D1 | **TOI sample size** | **LOCKED: the 30 CALIBRATION-split CP/KP TOIs only.** Inspection found 67 of the 97 CP/KP TOIs are TEST-split; running them would touch the test split (violates §1.1). Restricting to the 30 calibration-split TOIs keeps the reality check fully test-blind. ~28 need conditioning (2 already cached). |
| D2 | **EB sample** | **LOCKED: the 16 labeled eclipsing-binary TICs (all already conditioned, calibration-split) — zero network.** Optionally extend to all 146 EB/variable exclusions (also all conditioned) as a secondary FP-rejection set. |
| D3 | **W4 optional pieces** | Rec: include **F9** (cheap, one star); **defer F7** (a full single-event campaign is heavier and the regime is acknowledged as future work in the draft). |
| D4 | **Depth/T₁₄ re-run size (W1)** | Rec: per-cell ~50 on calibration (fast; enough for recovered-vs-true scatter). |
| D5 | **Compute window** | Rec: run W1+W3 (calibration, compute-bound) and W2 (network + compute) in one gated session, `caffeinate` + AC, with the same monitoring as M4. |

## 4. Tooling to build (new — none exists)
- `research/m6_reality_check/toi_eb_reality_check.py` — sample selection, frozen-Stage-0 conditioning (reuse `condition_test_hosts.py`/`m1_pipeline._condition_one`), run both arms, TOI-recall + EB-FP metrics.
- `research/m6_reality_check/ablation.py` — gate-ablation variants on calibration.
- extend the recovery worker to log depth/T₁₄ (W1) on calibration.

## 5. Compute / network / time estimate (honest)
- **W2 conditioning:** ~50 TOIs + (≤158 − already-conditioned) EBs → network fetch, ~30–60 min (like the 80-host TEST conditioning).
- **W2 runs:** ~150–200 stars × Arm A full TLS (~90 s) on 8 workers ≈ **~30–45 min**; Arm B cheap.
- **W1 + W3:** calibration injection re-runs, **~1–3 h** depending on D4 size and ablation breadth.
- **Total: roughly a half-day of mixed network + compute on the laptop** (AC + `caffeinate`, monitored as in M4). Far shorter than M4's 3-day test run.

## 6. Metrics
- **T6:** TOI recall (Arm A, Arm B, combined); EB rejection fraction by stage; any TOI lost only on the cheap path (the wrong-epoch pathway, cross-checked against §3.2).
- **T8:** Δrecall and Δfalse-positive vs the sealed gate, per ablation variant.
- **T5-full/F5-depth:** median fractional depth & T₁₄ error + interval coverage.

## 7. Risks
- **R-1:** TOI light curves may not all have S1–S3 2-min data → sample attrition; over-draw and report realized n (as in TEST conditioning).
- **R-2:** the EB set is calibration-split; that is fine for an FP-rejection characterization (no leakage concern — no thresholds are set).
- **R-3:** ablation must remove a component cleanly without accidentally re-tuning a sealed value — code review before running.
- **R-4:** another laptop compute session (power/thermal) — mitigated by the short duration and the M4 monitoring playbook.

## 8. Sign-off
Owner approves §3 (D1–D5) + authorizes building the W1–W3 tooling and running the gated session. **Nothing fetches or computes until this is signed.** On completion: artifacts + manuscript T6/T8/T5-full/F5-depth (+F9), a Daily-Log entry, and a PR — no seal touched.

---

*M6 plan, 2026-06-25 — DRAFT for sign-off. Characterization only; no TEST re-read; sealed protocol frozen; v3 final.*
