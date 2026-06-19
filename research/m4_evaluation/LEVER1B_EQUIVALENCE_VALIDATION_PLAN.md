# Lever-1b Equivalence-Validation Plan (v3; CALIBRATION-only)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-19 |
| **Status** | **DRAFT — pending owner sign-off.** Execution plan only; no new frozen parameter; CALIBRATION-only; **TEST not read.** |
| **Authority** | [`DR-002`](../../docs/decisions/DR-002_DECISION_RECORD.md) §2.3 / §2.3a · VAL v3 §A.8a · MATH v1.2 §9.1a |
| **Gate it implements** | The **numerical-equivalence gate** that admits the v3 cheap period-FAP estimator (Lever 1b) as an estimator-of-record, OR drops it (→ confirmer-only v3). |
| **Anti-tuning** | The statistic, the null model, and $\alpha_{\rm FAP}$ are **unchanged**. Only the *estimator of an already-sealed quantity* is substituted, and only if proven equivalent. The tolerance is **pre-stated here, before any equivalence number is examined** (stopping rule P-3). |

> Decided on CALIBRATION; sealed (into the v3 manifest, #2b) **before** the single TEST run. This plan does not set or move any threshold — it tests whether a cheaper estimator reproduces the sealed $\widehat{\mathrm{FAP}}$ closely enough to be used operationally.

---

## 1. Objective

The sealed period-FAP is the $B\!\ge\!1000$ circular block bootstrap (VAL A.8, MATH §9.1). It costs ρ_d ≈ 12.4% of a full TLS on every routed star — the measured driver of the M4 dry-run E2 shortfall (DR-002 §1). Lever 1b replaces the **live** bootstrap with a **cheaper estimator of the same $\widehat{\mathrm{FAP}}$**. This plan decides, on CALIBRATION only, whether that estimator is **numerically equivalent** to the bootstrap. If yes → it is the operational estimator-of-record (the bootstrap remains the reference definition). If no → it is dropped and v3 runs the bootstrap ("confirmer-only v3"), with the E2 outcome reported as-is.

This is the **load-bearing warrant** for Lever 1b (DR-002 §2.3): the gate, not the compute motivation, licenses the substitution.

## 2. Candidate estimators (form fixed by theory, P-3)

Both are theory-justified estimators of the **same** null exceedance; neither changes the statistic or α. Estimator *form* is fixed here, before performance is seen:

- **E-EVT (preferred).** Per-star **extreme-value (GPD) tail fit** to the surrogate maxima $\{T^{(b)}\}$ from a *reduced* bootstrap ($B' \ll 1000$, e.g. $B'\in\{50,100\}$), extrapolating the tail to obtain $\widehat{\mathrm{FAP}}(T_{\rm obs})$. Preserves each star's own red-noise structure; cost scales with $B'$.
- **E-LUT (alternative).** A **precomputed red-noise null distribution** over a grid of (baseline, event count $k$, noise level / CDPP), computed offline once, retrieved at runtime by interpolation → O(1). Cheapest, but its per-star fidelity is the open risk (a generic grid may not capture an individual star's autocorrelation) — which is exactly what the gate tests.

The two are validated **independently**; selection between them is by **equivalence + cost**, never by E1/E2 (P-3). If both pass, prefer the cheaper that passes; if only one passes, it is the estimator-of-record; if neither passes, fallback (§6).

## 3. Reference data (CALIBRATION-only; TEST hard-blocked)

- **Null pool:** the M3 **cleaned null pool** (the 854-star cleaned draw; EB/variable-contamination removed per M3; M0 null definition preserved). Used for FAP equivalence + gate-membership.
- **Injection set:** a calibration-host injection campaign for recall-safety. **Larger and broader than the §7b n≈40 set** that produced the provisional 5.5·α margin — span the full $(P, R_p)$ grid (not only strong P≤4 d, R≥2 cells), fixed RNG seed. Each injection carries BOTH the reference bootstrap FAP and the cheap-estimator FAP plus the period-match truth flag.
- `seal_loader.py` guards TEST and verifies Seal #2; **0 TEST TICs** asserted in every output (as in the dry-run).

## 4. Pre-stated equivalence tolerance (fixed BEFORE looking — P-3)

The estimator is **equivalent** iff **all three** hold on CALIBRATION. Tolerances are set from the reference estimator's own Monte-Carlo error, not from any downstream outcome:

- **(i) FAP agreement.** Across the null pool, the cheap $\widehat{\mathrm{FAP}}$ matches the bootstrap $\widehat{\mathrm{FAP}}$ within the bootstrap's own sampling error: $|\widehat{\mathrm{FAP}}_{\rm cheap} - \widehat{\mathrm{FAP}}_{\rm boot}| \le \tau_{\rm abs}$ near the gate, with $\tau_{\rm abs} = $ the $B=1000$ add-one bootstrap standard error at $\alpha_{\rm FAP}$ (i.e. $\sqrt{\alpha(1-\alpha)/B}$, ≈0.0031 at α=0.01, B=1000) — rounded to a pre-stated $\tau_{\rm abs}=0.005$. Report median and 95th-percentile $|\Delta\mathrm{FAP}|$ and the rank correlation (reference: the dry-run white-vs-red corr 0.868 is a *proxy*, not equivalence).
- **(ii) Gate-membership invariance.** The set of null stars with $\widehat{\mathrm{FAP}}\le\alpha_{\rm FAP}$ must not change beyond tolerance: **discordant gate decisions ≤ 1% of the null pool**, AND **zero** discordance that would *admit* a null the bootstrap rejects in the operating region (no FP inflation).
- **(iii) Recall-safety on injections (NN#1, hard).** Among injections the bootstrap **keeps** (FAP_boot ≤ α) **and** period-matched to truth, the cheap estimator must clip **exactly zero**. This is non-negotiable; a single clipped recoverable planet fails the gate outright.

> Note: criterion (iii) is *stricter* than the §7b "margined pre-filter" framing. Lever 1b as scoped in v3 is an **estimator substitution** (compute the same FAP cheaper), not the §7b *early-reject pre-filter* (Lever 1a, excluded from v3, DR-002 §2.3). There is no `5.5·α` margin here: the cheap estimator is required to *reproduce* the bootstrap decision, not to add a new rejection rule.

## 5. Procedure

1. **Reference pass.** On the null pool + injection set, compute the sealed $B=1000$ bootstrap FAP (the M3 scheme, VAL A.8) — the ground truth. (Reuse the M3 `Pool`/`imap_unordered` pattern.)
2. **Candidate pass.** Compute E-EVT (and E-LUT) FAP on the identical inputs. For E-LUT, build the offline grid first (record its axes + resolution + provenance).
3. **Equivalence test.** Evaluate criteria (i)–(iii) at the pre-stated tolerances of §4. No tolerance is adjusted after seeing results (P-3).
4. **Cost ledger.** Measure per-star wall-cost of each candidate vs the bootstrap → the projected ρ_d reduction. (Reported for the record; **does not** affect admissibility, only the choice among *passing* estimators.)
5. **Verdict + record.** PASS → name the estimator-of-record + its validated tolerance; freeze both into the v3 manifest and hash (Seal #2b). FAIL → §6.

## 6. Fallback (gate fails)

If no candidate satisfies §4, Lever 1b is **dropped**. v3 reverts to **confirmer-only**: the operational period-FAP is the sealed $B=1000$ bootstrap, ρ_d stays ≈12%, and the M4 E2 outcome is reported **as-is** (a likely E2-fail → the pre-committed compute falsification, VAL §7a). This is the honest result: if the cheap estimator cannot reproduce the sealed decision, the cost is not a removable artifact and the compute claim genuinely does not clear (DR-002 §2.3a, §4.1).

## 7. Outputs / artifacts

- `data/manifests/m4/equivalence/` — per-star reference vs candidate FAP, gate-membership diff, injection recall-safety table, cost ledger (CSV) + a summary JSON.
- A short result memo (`LEVER1B_EQUIVALENCE_RESULT.md`) stating the verdict, the admitted estimator (or fallback), the validated tolerance, and the projected ρ_d.
- The admitted estimator config + tolerance enter the **v3 threshold manifest** (Seal #2b).

## 8. What this plan does NOT do

- It does **not** set or move $\alpha_{\rm FAP}$, the statistic, the null model, or any sealed threshold.
- It does **not** introduce the §7b early-reject pre-filter (Lever 1a) or multi-harmonic testing (Lever 2) — both excluded/deferred (DR-002 §2.3, P-8).
- It does **not** touch TEST. Equivalence is decided entirely on CALIBRATION; the result is sealed before M4.

---

*Lever-1b equivalence-validation plan (DRAFT). Execution-only; CALIBRATION-only; no TEST read; sealed into #2b before the single M4 run.*
