# T_red Calibration Plan — Fast-Path Confirmer Threshold (v3; CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-19 |
| **Status** | **DRAFT — pending owner sign-off.** Execution plan; CALIBRATION-only; **TEST not read.** |
| **Authority** | [`DR-002`](../../docs/decisions/DR-002_DECISION_RECORD.md) §2.2 / §2.3 · VAL v3 §2, §A.11 · MATH v1.2 §6 |
| **Produces** | The sealed value of **$T_{\rm red}$**, the Arm-B fast-path confirmer threshold, calibrated to **FAR ≤ 1 %/star** — the v3 common-FAR keystone. Hashed into the v3 manifest (Seal #2b). |
| **Anti-tuning** | $T_{\rm red}$ is set to a **pre-stated false-alarm-rate target** (the same target as Arm A's $T$), **not** to optimize E1/E2. Statistic form fixed by theory (MATH §6) before performance is examined (P-3). CALIBRATION-only. |

> Why this plan exists: in the M4 dry-run, `T_red` was **degenerate** — almost no null star produced a *confirmed* candidate because the period-FAP gate rejected them first, so the confirmer threshold was non-binding (the FAP gate, not the confirmer, did the FP rejection; `M4_COMBINED_ARM_RESULT.md` §"Why E2 fails", pt 3). v3 promotes the confirmer to a genuine **transit-template likelihood-ratio** (A.11) and gives it a properly calibrated threshold so the common-FAR keystone holds.

---

## 1. Objective

Calibrate $T_{\rm red}$ such that the **end-to-end Arm-B fast path** (route → cheap period-FAP gate → confirmer $\Lambda \ge T_{\rm red}$) has empirical **false-alarm rate ≤ 1 % per star** on null calibration stars — the *same* target to which Arm A's TLS SDE threshold $T = 10.74$ was calibrated (VAL A.2). This is what makes the two arms comparable "at a common false-alarm rate" (the v3 fairness keystone, §2), replacing the v2 "same engine, same $T$" requirement that Finding B invalidated.

## 2. Prerequisite — the confirmer must be the genuine transit-LR (NN#3)

This plan calibrates a threshold; it presumes the confirmer of VAL A.11 / MATH §6 is implemented as specified and **not** the dry-run's box depth-SNR:

- Fold the conditioned light curve at the seeded $(\hat P, \hat t_0)$.
- Fit a **physical transit template** (Mandel–Agol / limb-darkened from TIC stellar params; trapezoid permitted only as the degenerate limb-darkening case) against a flat-baseline null.
- Form $\Lambda = -2\ln(\mathcal{L}_0/\mathcal{L}_1)$ (equivalently $\Delta\mathrm{BIC}$ or transit-fit S/N), **sign-aware** (dimming only) and **shape-consistent** (rejects V-shaped/secondary/odd-even-inconsistent forms).
- Look-elsewhere is handled upstream by the period-FAP (A.8/A.8a); $\Lambda$ is computed at a fixed ephemeris (range-invariant — the property Finding B showed the TLS SDE lacks).

Building this confirmer is part of v3 execution; this plan's threshold is meaningless without it. The implementation is recorded with the calibration run.

## 3. Data (CALIBRATION-only; TEST hard-blocked)

- **Null stars (for FAR):** the **full cleaned null pool** (M3 cleaned draw; EB/variable contamination removed; M0 null definition preserved). Planetless → any $\Lambda \ge T_{\rm red}$ at a seeded ephemeris is a **false confirmation**.
- **Injection set (for the recall sanity check, §5):** the calibration-host injection campaign (shared with the equivalence plan; full $(P,R_p)$ grid, fixed seed).
- `seal_loader.py` guards TEST + verifies Seal #2; **0 TEST TICs** asserted in all outputs.

## 4. Procedure (set $T_{\rm red}$ by FAR — P-3)

1. **Run the Arm-B fast path on every null star**, end to end: detect → seed $(\hat P, \hat t_0)$ → cheap period-FAP gate (the v3 admitted estimator, or bootstrap fallback) → for stars passing the FAP gate, compute the confirmer $\Lambda$.
2. **Tabulate the null $\Lambda$ distribution** among FAP-gate survivors. A star false-confirms iff it passes the FAP gate **and** $\Lambda \ge T_{\rm red}$.
3. **Set $T_{\rm red}$** = the smallest threshold for which the **end-to-end per-star false-confirmation rate ≤ α (1 %)**, i.e. $\Pr_{\rm null}[\text{FAP-gate pass} \wedge \Lambda \ge T_{\rm red}] \le 0.01$. (Calibrate on the *joint* event so the keystone compares the *whole* fast path against Arm A's whole search at equal FAR.)
4. **Report both rates:** the marginal per-star FAR and the FAP-gate-conditional confirmer FAR, so the division of labor between the two gates is transparent (and the dry-run's degeneracy cannot recur silently).
5. **Freeze** $T_{\rm red}$ into the v3 threshold manifest; hash (Seal #2b).

## 5. Recall sanity check (reported, non-setting)

After $T_{\rm red}$ is fixed **by FAR**, verify on the injection set that the confirmer retains recoverable planets (a calibration-side preview of E1). Report:
- confirmer ROC / separation (AUC) on injections vs nulls — must improve on, or match, the dry-run epoch-fixed MF (AUC 0.877; `M4_EPOCH_FIXED_DIAGNOSTIC.md`). A true transit-template LR is expected to separate at least as well.
- fast-path recall at $T_{\rm red}$ and the resulting full-TLS fallback fraction (the dry-run's 59% fallback is the quantity v3 hopes to reduce — but **fallback rate is an outcome, not a setting**; $T_{\rm red}$ is fixed by FAR regardless, P-3).

If the recall preview is poor, that is **information about the principle**, not license to lower $T_{\rm red}$ below its FAR-calibrated value (doing so would be tuning, NN#2 / P-1).

## 6. Outputs / artifacts

- `data/manifests/m4/tred/` — null $\Lambda$ distribution, marginal + conditional FAR curves, the chosen $T_{\rm red}$, injection ROC/recall preview (CSV + summary JSON).
- A short result memo (`TRED_CALIBRATION_RESULT.md`): the sealed $T_{\rm red}$, the achieved null FAR, and the recall preview.
- $T_{\rm red}$ + the confirmer implementation hash enter the **v3 threshold manifest** (Seal #2b), alongside the admitted period-FAP estimator (equivalence plan) and the unchanged v2 thresholds.

## 7. Ordering & dependencies

1. Implement the transit-LR confirmer (A.11 / §2 of this plan).
2. Run the **Lever-1b equivalence-validation** (decides the operational period-FAP estimator that gates entry to the confirmer).
3. Run **this** $T_{\rm red}$ calibration (uses that gate).
4. Assemble the v3 threshold manifest → **Seal #2b** → single M4 TEST run.

## 8. What this plan does NOT do

- It does **not** set $T_{\rm red}$ to hit any E1/E2 target — only the FAR target (P-3).
- It does **not** change Arm A's $T$ (=10.74), $\alpha_{\rm FAP}$, $z_\star$, $z_{\rm mono}$, $N_{\min}$, $\varepsilon$, $w_c$, or $\hat\pi$ — all carry over from Seal #2 unchanged.
- It does **not** read TEST.

---

*T_red calibration plan (DRAFT). Execution-only; CALIBRATION-only; no TEST read; $T_{\rm red}$ sealed into #2b before the single M4 run.*
