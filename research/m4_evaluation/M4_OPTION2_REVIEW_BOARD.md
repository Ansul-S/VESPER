# Option-2 Amendment — Protocol Review-Board Report (adversarial)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Mandate** | Aggressively challenge / attempt to falsify the approved Option-2 amendment scope before any draft. |
| **Inputs** | `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, dry-run CSVs in `data/manifests/m4/dry_run/`. CALIBRATION-only. **No TEST accessed.** |
| **VERDICT** | **DOES NOT SURVIVE AS SCOPED.** The amendment is *repairable* and probably sound in spirit, but it has **one near-fatal consistency issue (non-neg #3), one architectural underspecification that flips which endpoint fails, a misstated E2 cost, post-hoc statistic-selection risk, and unmeasured combined-system E1/E2.** Do **not** draft DR-002 / VAL v3 / MATH v1.2 until conditions R1–R7 are resolved. |

---

## Summary of the attack

The amendment replaces Arm B's confirmation (targeted TLS, SDE≥T) with an epoch-fixed matched-filter S/N ≥ T_red, and reframes fairness from "same engine, same T" to "common FAR." Six of the eight review axes raise material objections; two are clean.

| Axis | Result |
|------|--------|
| 1. Scientific validity | **Challenged** — confirmer may be a coherence proxy, not independent transit-model physics (non-neg #3). |
| 2. Internal consistency | **Challenged** — collides with MATH §9 v3-circularity warning and the corrected-lesson arbiter definition. |
| 3. Fairness vs original hypotheses | **Challenged** — "common FAR" ≠ "equal power"; H2 mechanism silently changes. |
| 4. Hidden anti-tuning risks | **Challenged** — the statistic + its variant were chosen post-hoc on calibration AUC. |
| 5. Leakage | **Clean** (with one caveat on null-pool vetting completeness). |
| 6. T_red statistical validity | **Challenged** — 1% quantile from ~170 routed nulls; contaminated tail; mixture-FAR ill-defined. |
| 7. E1/E2 compatibility | **Challenged hard** — architecture choice flips which endpoint fails; E2 cost misstated; combined E1/E2 unmeasured. |
| 8. Cross-document consistency | **Challenged** — touches VAL §2/§4 + A.1/A.4, MATH §2/§9, SCIENTIFIC_HYPOTHESIS H2, non-neg #3. |

---

## Falsification attempts (with evidence)

### F-1 (near-fatal) — The confirmer may violate non-negotiable #3 (physics, not a coherence score, is the arbiter)
The project's corrected v3 lesson (CLAUDE.md non-neg #3; MATH §9 ¶3; `TRINETRA_CONCEPT_RECONSTRUCTION` §E) is that **an independent physics gate (transit-model significance), not the detector's own coherence/SNR score, must arbitrate**. The original design honored this with a clean split: cheap detector **proposes**, independent TLS **disposes**. Option 2 makes the disposer a **box matched-filter S/N coadded at the detector's own inferred ephemeris** — i.e., the detector's statistic re-summed. That is structurally close to "route on the detector alone," the v3 error.
- *Partial rebuttal (evidence):* corr(detector n_events, MF S/N) over routed nulls = **0.086** — weak, so the MF is **not** merely the event count re-summed; it adds folded depth/repetition information.
- *Residual concern:* low numerical correlation ≠ methodological independence. Detector and confirmer share the **same box-matched-filter form** on the **same residual**, and the confirmer is evaluated at the **detector-selected** (P̂, t̂₀). It is not an independent method the way TLS is.
- **Condition R2:** the confirmer must be a genuine **transit-model likelihood-ratio** (transit vs flat, limb-darkened template consistent with the injection model), explicitly argued to satisfy non-neg #3 as "depth + shape + repetition" physics — **not** a bare depth/σ SNR. The reduced detector↔confirmer independence must be documented as a stated limitation, and this requires **owner adjudication against non-neg #3** (possibly a charter note). The box depth-SNR used in the diagnostic does **not** clear this bar.

### F-2 (critical) — Architecture underspecification flips which endpoint fails
The scope says "fallback = full TLS" but never states whether a **routed star whose cheap confirm FAILS** falls back to full TLS. This single choice determines everything:
- **No fallback for routed stars** → recall of the fast-path population depends on MF power. Occurrence-weighted exposure: w_c on Rp>2 (the routed population) = **0.072**. Worst-case ΔR̄ ≈ −0.072·d where d = MF miss-rate on routed-recoverable planets. Anchor: **2 of 5** Arm-A-recovered planets had MF < T_red → d≈0.40 → ΔR̄ ≈ **−2.9 pp → E1 FAILS** (margin −2 pp). Even d=0.3 → −2.2 pp fails.
- **Fallback for routed stars** (routed → MF; if MF<T_red → full TLS) → d≈0, E1 ≈ non-inferior (PASS), **but** unconfirmed-routed stars cost detector+FAP+full TLS > full TLS (negative saving), so **E2 must be re-derived** and the "fast-path-eligible compute" estimand changes.
- The Prime Directive ("a missed planet is not acceptable; recall > precision", non-neg #1) **mandates the fallback design**. So E1 is protected — but then the earlier claim "near-zero cost" and the E2 saving are the things at risk, not recall.
- **Condition R1:** the amendment must **explicitly specify** routed→MF→(MF<T_red ? full-TLS-fallback). This is recall-safe (consistent with non-neg #1) and means **E2, not E1, carries the residual risk** — the opposite of how the scope was framed.

### F-3 (critical) — The E2 "near-zero cost" claim is false
The methodology review/handoff cite cost ≈ **3.3e-5 × full TLS**. That is only the **MF-eval** cost. The actual Arm-B fast-path cost is dominated by the **B=1000 block-bootstrap period-FAP** (sealed). Dry-run ledger medians: detector 0.011 s, **period-FAP 10.5 s**, full TLS 42.3 s → fast-path ≈ **10.5 s, ~75 % saving** — not 99.997 %. Under the recall-safe fallback (F-2), the realized E2 saving is *further* diluted by unconfirmed-routed stars that incur fast-path cost **plus** full TLS.
- **Condition R3:** restate E2 honestly (fast-path cost is period-FAP-dominated; ~75 % per-confirmed-star), and **re-derive the E2 estimand under the fallback architecture** (saving on confirmed fraction minus overhead on unconfirmed-routed). Confirm ≥30 % is still attainable — currently **unproven**.

### F-4 (major) — "Common FAR" is not "equal power"; H2's mechanism silently changes
The original fairness keystone (VAL §2) — *same engine, same SDE threshold* — guaranteed any recall difference was attributable to **routing/seeding alone**. "Common FAR with different statistics" does **not**: two detectors at equal FAR can have different ROC/power, so an Arm-A–vs–Arm-B difference now confounds routing with the **intrinsic power gap** between full-TLS-SDE and the MF. More fundamentally, H2 was "route the **same** search cheaply"; Option 2 tests "route to a **cheaper, different** confirmer." That is a **different (weaker) scientific claim**.
- **Condition R4:** SCIENTIFIC_HYPOTHESIS H2 and VAL §2 must be amended to state the new mechanism explicitly (evidence-first with a cheap fixed-ephemeris **surrogate** confirmer + full-TLS fallback), and acknowledge it is a redefinition, not a cosmetic edit. Confirm the redefined claim is still the ISRO-relevant contribution.

### F-5 (major) — Anti-tuning: the statistic was selected post-hoc on calibration performance
The MF statistic has multiple free choices made **after** observing the dry-run: template (box), in-transit window (T₁₄ of the strongest event), noise model (duration-timescale σ), effective N (N_transits vs N_cadences), and the **white-vs-red variant chosen because red had marginally better calibration AUC (0.877 vs 0.873) and a tighter tail**. Choosing among Options 1/2/3 and among statistic variants on calibration AUC is a large researcher-DOF surface, all exercised post-discovery. Legitimate *only* if frozen + sealed before TEST — but "forced by a pre-TEST discovery" is too generous: the **specific** resolution was *chosen*, not forced.
- **Condition R5:** freeze **one** fully-specified statistic, justified on **first-principles matched-filter theory** (not calibration AUC); pre-commit every choice; document the DOF and the post-hoc selection honestly in DR-002.

### F-6 (major) — Combined-system E1/E2 are UNMEASURED
The dry-run `m4_run.py` implemented *targeted-TLS-then-fallback*, **not** *MF-then-fallback*. The epoch-fixed diagnostics measured only the **statistic's ROC** (AUC, FAR, cost) on isolated stars — **never the combined Arm-B system** (route → MF → fallback) end-to-end. Therefore **no ΔR̄ and no compute ratio for Option 2 exist yet.** The recommendation rests on extrapolation.
- **Condition R6:** before re-registration, run a **CALIBRATION-only combined-arm dry-run** of the actual Option-2 architecture (inject into calibration hosts; route → MF(T_red) → full-TLS fallback; full-TLS Arm A) and report calibration-side ΔR̄ and compute ratio. This de-risks the single TEST run without touching TEST.

### F-7 (moderate) — T_red statistical validity + leakage caveat
- T_red is a 1 % quantile estimated from ~170 routed nulls (≈ the 1.7 highest scores) — **noisy**; the cleaned-pool tail still reaches **21.8** (vs T_red≈5.5), and M3 vetting covered only the 1000-star draw, so residual unvetted variables may inflate T_red or, on the full pool, under-estimate FAR.
- The **combined** system's FAR is a **mixture** (route&MF≥T_red ∪ fallback&SDE≥T_A), not a clean 1 % — the "equal FAR" comparison needs a consistent combined-FAR definition.
- **Leakage:** clean — no TEST tics in any artifact; T_red is calibration-only. Caveat: calibrate T_red on the **same** cleaned 854 pool used for T_A (consistency), and acknowledge the vetting-completeness limit.
- **Condition R7:** calibrate T_red on the **full** cleaned null pool with a stated quantile-uncertainty; define combined-system FAR explicitly; re-confirm null-pool vetting adequacy.

---

## Unproven assumptions (must be retired before TEST)
1. That a transit-model LR confirmer satisfies non-neg #3 as independent physics (F-1). **Unproven; owner adjudication.**
2. That combined Arm-B (MF + fallback) achieves E1 non-inferiority on calibration (F-2/F-6). **Unmeasured.**
3. That E2 ≥ 30 % survives the fallback overhead + period-FAP cost (F-3/F-6). **Unmeasured.**
4. That T_red controls FAR ≤ 1 %/star on the full cleaned pool, not just 300 stars (F-7). **Under-powered.**
5. That MF recall is not gated by period-from-spacing error under red noise (R-3 risk) — the operational MF recall already folds in P̂ errors; the routed-population recall is hostage to seed accuracy.

## Clean axes
- **Leakage (axis 5):** no TEST access anywhere; diagnostics used calibration cached residuals + the M3 cleaned-null definition; Seal #2 unchanged. (Caveat F-7 only.)
- The **range-invariance** and **cost-of-the-MF-itself** claims are correct as far as they go (the MF has no period grid and is ~free *per eval*) — but they do not carry the E2 case (F-3).

## Required conditions before any draft (R1–R7)
- **R1** Specify routed→MF→full-TLS-fallback explicitly (recall-safe). *(flips risk to E2)*
- **R2** Confirmer = transit-model likelihood-ratio; argue non-neg #3 compliance; document reduced independence. *(owner adjudication)*
- **R3** Restate + re-derive E2 honestly under the fallback architecture.
- **R4** Amend H2 / VAL §2 to the redefined mechanism; confirm it is still the intended claim.
- **R5** Freeze one first-principles statistic; document post-hoc DOF in DR-002.
- **R6** CALIBRATION-only combined-arm dry-run → calibration ΔR̄ + compute ratio, before re-registration.
- **R7** Calibrate T_red on the full cleaned pool with uncertainty; define combined-FAR; confirm vetting adequacy.

## Recommendation
**Hold.** Do not draft DR-002 / VAL v3 / MATH v1.2 / SCIENTIFIC_HYPOTHESIS diff / T_red plan yet. The amendment is promising but **fails this review as scoped**; the gating issues are R1 (architecture), R2 (non-neg #3 adjudication), and R6 (combined-system E1/E2 are unmeasured). Recommended path: owner rules on R2 and R4; I then run the R6 combined-arm calibration dry-run; if E1/E2 hold on calibration and R1–R5/R7 are satisfied, re-submit the revised scope for a second review, *then* draft.
