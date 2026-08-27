# VESPER Dashboard

> **AUTHORITATIVE CURRENT STATE — updated 2026-08-27.** Sections below this banner are Phase-I historical record. ⚠️ The historical sections state "H1 FALSIFIED (compute)" — that verdict is **SUPERSEDED** per DR-003: the frozen-rule E2 re-measurement (300/300, 2026-07-27) returns **E2 INCONCLUSIVE**. **Corrected Phase-I verdict: E1 PASS (robust) · E2 INCONCLUSIVE** (ratio 0.727, CI [0.636, 0.826]; π\*≈0.489). See the 2026-07-27 block below.

## ▶ 2026-08-27: MATHEMATICAL AUDIT — the routing ceiling (new closed-form result); MATH-3 + MATH-4 closed

- **Phase:** Phase I (COMPLETE / SEALED / FINAL). Post-seal analysis, **calibration only** (TEST not read, P-5 intact). Sealed verdict **E1 PASS · E2 INCONCLUSIVE — unchanged**.
- **Milestone ladder:** W2 advances — **MATH-3 ☑** and **MATH-4 ☑** (both were open and unexecuted). Remaining W2: MATH-2, MATH-8.
- **Headline — the routing ceiling.** $W \equiv k\hat R^2 \ge \ln(N_{\rm eff}/\alpha)$ and $W \le N_{\rm tr}/(1+\rho_{\rm FP})$, hence $P \lesssim T_{\rm base}/\ln(N_{\rm eff}/\alpha)$. Every tunable enters logarithmically; only the transit count enters linearly. zero-free-parameter prediction of the sealed gate on 1,233 nulls at **precision 87.5% / recall 75.7%**; **out-of-sample scaling confirmed** (predicted 2.94 / 5.80 d, measured 2.51 / 5.00 d; ratio 1.97 vs 1.99); mechanism verified (at $P\ge8$ d, gate opens for 20% / 0% of *correct* seeds).
- **Falsification attempt failed.** Sweeping $T_\beta=\hat R k^\beta$ at matched null FAR gains ≤ **+1.49 pp**; the exactly-pivotal statistic **loses 10.31 pp**. Multiplicity dependence is the evidence, not a defect. The ceiling is a property of the null geometry.
- **Subset region.** Fast-path eligibility ⇒ $\mathrm{SNR}_{\rm tot}\gtrsim10.2$ vs sealed $T=10.74$. Measured (excl. the known $P{=}0.5$ d edge artifact): **17/17** fast-path recoveries also found by full TLS, **0** fast-path-only. E1's PASS was structurally guaranteed — this is the reason.
- **MATH-4 ☑** — $\Lambda$'s null is not $\chi^2_1$: $q_{99}$ = 120.4 vs 6.63 (18×); $\Pr(\Lambda\ge25)$ = 1.81% vs 2.9e-7 (6.3e4×). Binding $T_{\rm red}$ would be ≈ **4,340**. `no_secondary`'s "~5σ" is ≈ **2.1σ**. At $T_{\rm red}=0$ the gate is a **circular sign test**: $\Pr(\hat\delta>0)$ = 0.859 at the seed vs 0.444 at random; $\Pr(\text{confirm}\mid\text{null})$ = **66.8%**.
- **MATH-3 ☑, direction REVERSED** — the bootstrap null contains the signal. 128 paired runs: median FAP **0.0569** vs **0.1578** signal-free; gate open **53 vs 24**. **79% of fast-path routings exist only because the null is contaminated.** Anti-conservative, not conservative as the roadmap assumed. FAR control unaffected; $f_p$ (hence E2) inflated.
- **Red noise on transit timescales.** $\kappa(T_{14})$ median 1.17→1.48, $p_{90}$ to **9.0**, 32–49% of stars > 1.5 — while the sealed detector docstring certifies "near-white" from $\mathrm{acf}_1\approx0.01$. **Lag-1 ACF is not a whiteness test on transit timescales.** Detector survives (self-calibrated MAD); confirmer does not (parametric Matérn from lag-1).
- **Corrections of record:** MATH §4b fragility is **linear** not quadratic (verified to 3 dp) · MATH §9's "identical grid" premise is **false in code**, and that deviation is what keeps $N_{\min}=2$ survivable (implementing the spec as written: null FAR 2.99% → **4.37%**, 23 gate flips, 18 of them $k{=}2$) · Seal #2's $N_{\min}=2$ is **inoperative** (0 of 128 $k\le2$ candidates ever routed).
- **Confirmation:** M3's null cleaning was load-bearing — FAP tail 1.06× nominal on the cleaned pool vs **6.45×** on the excluded EB/variable pool. But the FAP is not a uniform $p$-value (KS $p$=2.5e-9): **the calibration does not extrapolate to any other $\alpha$.**
- **Documents:** `research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md` · artifacts `data/manifests/math_audit/` (incl. `findings.json`) · code `research/math_audit/` (5 scripts).
- **Anti-tuning intact:** sealed docs verified **0 differing lines** vs `phase1-prereg-v3` (branding-normalised); Seal #2 SHA-256 matches DR-001 §5a; `frozen_rerun/` clean; sealed exceedance counts reproduced **bit-identically 1,126/1,126**.
- **Open:** does the ceiling become the paper's central result · re-measure $f_p$ against a signal-free null · fold §N-1/§N-2 into `VESPER_MATH_ADDENDUM.md` as §F/§G. **The 2026-07-28 scope decision is still first in line.**

## ▶ 2026-08-17: INN-3 — the period-FAP entry tax is removable, exactly (Wave 6 item, delivered early)

- **Phase:** Phase I (COMPLETE / SEALED / FINAL). This is **post-seal analysis**, calibration-only; the sealed verdict (**E1 PASS · E2 INCONCLUSIVE**) is **unchanged**.
- **Milestone ladder:** unchanged (W0 ☑ · W1 all-but-RES-6 ☑ · W2 partial · W3/W4 partial · W5 ☐ · W6 ☐) — with **INN-3 (Wave 6) now ☑**, delivered ~5 waves early with its proof obligations discharged rather than stated.
- **Result.** The $B{=}1000$ period-FAP entry tax ($\rho_d = 11.6\%$), recorded by DR-002/Lever-1b as "not a removable artifact", **is removable exactly**. Two levers, neither statistical: **(A)** 49% of the FAP's cost was a loop invariant (`np.median(np.diff(np.sort(t)))` recomputed 10,000× per star while the bootstrap resamples the flux, not the epochs) → **6.31×, bit-identical**; **(B)** the gate $(g_e{+}1)/1001\le0.01$ is exactly $g_e\le9$, so the 10th exceedance decides it → **curtailed sampling, decision identical with probability 1**, one-sided so it cannot clip a planet. Combined **73.2× on nulls**, 12.7× on injections.
- **Equivalence measured:** 1126/1126 calibration nulls reproduce the sealed exceedance count (max |Δ| 0); 149/149 calibration injections bitwise. All three Lever-1b criteria met with **exact zeros** (E-EVT and E-LUT failed 3/3 each).
- **E2 counterfactual** (arithmetic on recorded artifacts; **no TEST re-read**): reduction **27.3% → 38.0%**, ρ_d **11.6% → 0.85%**, **π⋆ 0.489 → 0.036** (≈16× → ≈1.2× of π≈0.03), P(ratio≤0.70) **0.27 → 0.96**. **Decision still INCONCLUSIVE.**
- **⚠️ Second finding — the two-cause diagnosis.** With the routing cost set to **zero**, the CI is still [0.522, **0.703**]. E2's INCONCLUSIVE is a **variance** result (between-host variance at H=39), not a cost result. Both causes were necessary: the entry tax put the point estimate out of reach at any H (sealed numbers stay INCONCLUSIVE even at H=100); the erratum §2.1 parity bug (40 of 80 hosts) made the interval too wide at any cost. **Fix both → E2 PASSES at H=79, the count `m4_driver` was written to use.** Hosts needed: 49 / 65 / 41 / never.
- **Side finding:** `m4_driver.py:120` overwrites `t14` with the seeded event duration before the FAP call, so **M4 duration-matched T₁₄** — RES-4's "counterfactual" strata are the realised ones for M4. M4-realised flip exposure ≈**1.4%** vs the 0.09% reported (~16×). RES-4's *conclusion* survives; its stated mechanism and stratum labelling do not.
- **Documents:** `research/m4_evaluation/INN3_FAP_ACCELERATION.md` · `docs/VESPER_MATH_ADDENDUM.md` §E · artifacts `data/manifests/m4/inn3/` · code `fast_period_fap.py` / `inn3_fap_acceleration.py` / `nb_period_fap.py` · `tests/test_inn3_fap_acceleration.py` (9 tests green).
- **Anti-tuning intact:** no sealed doc, threshold, weight, manifest or tag touched; `frozen_rerun/` untouched; TEST light curves not re-read (P-5).
- **Open:** the 2026-07-28 scope decision (still first in line) · adopt the estimator of record (DR-006+) · paper placement of §6/§6.1a · RES-4 addendum · RES-6 + TLS-epoch re-run.

## ▶ 2026-07-27: E2 re-measurement COMPLETE → verdict INCONCLUSIVE; Wave-0 V-1→V-4 done

- **Corrected verdict: E1 PASS (robust) · E2 INCONCLUSIVE.** Frozen §6 rule, 300 inj × 5 repeats / 39 hosts → ratio **0.727** (27.3% reduction), host-clustered CI **[0.636, 0.826]** straddles 0.70; ρ_d 11.6%, f_p 23.7%, **π\*≈0.489 ≫ π≈0.03**. Neither confirmed nor falsified on compute; recall principle validated. Robust to a Low-Power-Mode window (leave-out 0.713; erratum §5.1). Results `data/manifests/m4/e2_retiming/e2_retiming_summary.json`.
- **Wave-0 checklist:** V-1 ☑ (`2941175`) · V-2 E2 300/300 ☑ · V-3 erratum ☑ · V-4 propagation ☑ · **V-5 PR/merge ☑ (PR #18 merged)**. **WAVE 0 COMPLETE.**
- **Wave-1 checklist (PR #19 + PR #21 merged):** RES-2 ☑ (E1 robust to KM period weighting, ΔR̄ −0.16 pp) · RES-3 ☑ (losses epoch-predicate) · RES-5 ☑ (supplement S-edge + fig S1) · RES-8 ☑ (endpoint disclosure) · RES-7 ☑ (monotransit design doc) · PUB-6 ☑ (public reconciliation) · **RES-4 ☑** (per-star τ_GP FAP on 1163 nulls: 0/1126 arm-B flips, 1/1126 arm-C, at the sealed T₁₄=0.2 d; sealed FAPs reproduced bitwise 968/968). **Still queued (compute):** RES-6 (η-paid injection; needs MAST) · TLS-epoch re-run.
- **Wave-2 checklist (2026-07-28, PR #21):** MATH-1 ☑ (π⋆ = ρ_d/(f_p(1−ρ)) derived; roadmap's "exact form" rejected) · MATH-5 ☑ (BCa lo95 −1.04 pp vs percentile −0.83 pp; E1 unchanged) · MATH-6 ☑ (N=2 comb degeneracy proven+measured) · MATH-7 ☑ (notation cross-reference). **Open:** MATH-2, MATH-3, MATH-4, MATH-8.
- **Wave-3 / Wave-4 partial:** CODE-7 ☑ (cluster bootstrap vectorized, bit-exact) · DOC-2 ☑ (`docs/INDEX.md`) · DOC-3 ☑ (`docs/SEAL_CHAIN_POSTMORTEM.md`).
- **⚠️ OPEN DECISION (2026-07-28, not decided):** project scope + paper framing — finish in ~2 weeks and cut Waves 3/6, reframing around the methodology (INN-1) rather than the routing result? Settle first. See `Current_Mission.md` and `SESSION_HANDOFF_2026-07-28.md` §6. **The roadmap stands as written until ruled on.**
- Next: settle the scope decision, then **RES-6** (η-paid injection; needs MAST) + the small **TLS-epoch re-run**. PR #22 (doc-only sync) open. Phase II hard-gated until DR-004.

## ▶ 2026-07-20: Phase II re-scoped (bound · benchmark · monotransit); repo pushed + draft PR open

- **Deep scientific review persisted** (`docs/reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md`): routing claim structurally capped (saving ≤ π·f_p ≈ 0.6% at zero tax; SES/FFA attacks the premise); assets = protocol, bound, monotransit regime.
- **`docs/VESPER_PHASE2_PROGRAM.md` DRAFT v0.1 (pending DR-004):** G0 (SES/FFA gating, sealed decision rules) → Track A (impossibility bound) · Track B (VESPER-Bench + Kepler DR25) · Track C (monotransit flagship; Λ_mono binding by NN-P2-10; raw+recondition injections; 892-monotransit free pre-study). Kepler routing-scaling sketch **superseded**.
- **Public reconciliation advanced:** README now states the withdrawn verdict + re-scoped future on the repo front page; CLAUDE.md carries an interim supersession bullet (full rewrite at V-4). Remaining PUB-6 item: v1.0.0 release notes annotation.
- **Pushed:** branch `phase1/audit-remediation` → origin (3 commits: remediation analysis · strategy docs · sync/publish); **draft PR → `main`** open; merge = owner decision at V-5 (after E2 verdict).
- **Wave-0 checklist:** V-1 resume guard ☐ · V-2 E2 campaign 26/300 (~19 h) ☐ · V-3 erratum §5/§7 ☐ · V-4 verdict propagation ☐ · V-5 finalize PR/merge ☐.

## ▶ 2026-07-19: audit remediation — E2 verdict withdrawn; re-measurement paused 26/300; roadmap adopted

- **Status: Phase I under AUDIT REMEDIATION** on branch `phase1/audit-remediation` (5 commits + uncommitted work). Verdict now: **E1 PASS (robust, 3 interval methods) · E2 UNDECIDED pending frozen-rule re-measurement** (sealed 12-star timing → ratio CI [0.42, 1.14]). Authority **DR-003**; register `M4_ERRATUM_2026-07-19.md`. Seals untouched; independently re-verified vs `phase1-prereg-v3` (0 non-branding diffs).
- **Milestone ladder addition:** ~~M4 verdict final~~ → **W0 Verdict** (E2 re-timing 26/300, PAUSED; erratum §5/§7 pending) → **W1 Robustness** (KM-period E1 sensitivity, epoch tolerance, PUB-6 public reconciliation) → W2 Math → W3 Engineering → W4 Repro/Docs → W5 Publication → W6 Tool/Phase-II-prep. Full plan: **`docs/ROADMAP_TO_10.md`**. **Phase II hard-gated until DR-004.**
- **Today's science:** edge control ruled out the grid-edge artifact and identified the P=0.5 d gain/loss mechanism as **TLS T₀ epoch-predicate failure** (36/38 epoch-only); erratum §6 + paper corrected. Second-pass audit: `docs/audits/PROJECT_AUDIT_2026-07-19.md` (new findings: log-uniform w_P not occurrence-based; π* formula inconsistency; detector epoch quantization).
- **Completion checklist (Wave 0):** V-1 resume guard ☐ · V-2 E2 campaign (~19 h) ☐ · V-3 erratum §5/§7 ☐ · V-4 verdict propagation ☐ · V-5 commit+merge ☐.
- **Key documents added:** `docs/decisions/DR-003_E2_REMEASUREMENT.md` · `research/m4_evaluation/M4_ERRATUM_2026-07-19.md` · `docs/audits/PROJECT_AUDIT_2026-07-19.md` · `docs/ROADMAP_TO_10.md` · M4_TEST_RESULT addendum · seal-loader dual-digest fix (rebrand had silently broken seal verification 2026-06-30 → 07-19).

## ▶ 2026-06-30: identity rebrand + first public release v1.0.0

- **Rebranded `TRINETRA-X` → `VESPER`** (branding only; no science changed). Acronym: **Validation Engine for Stellar Photometric Evidence and Recovery**. Folder `~/Desktop/VESPER`; repo `github.com/Ansul-S/VESPER`.
- **`v1.0.0` released** on `main` (HEAD `0118548`) — GitHub Release "VESPER v1.0.0 — Initial Public Release". Tree clean; `main` == `origin/main`.
- **Sealed-doc/manifest SHA-256 digests changed by design** (owner-authorized) — provenance in `docs/decisions/F1_DECISION_RECORD.md` §5a; original bytes intact at tags `phase1-prereg-v2/v3`. ⚠️ old `shasum` values will mismatch.
- **Repo reorganized (structure-only, history preserved):** Phase-I plans → `research/phase1/`; handoffs → `archive/session_handoffs/`; `NEXT_SESSION_PROMPT.md` untracked+gitignored; root limited to the 5 canonical files. No code/research changed.
- Phase I unchanged (COMPLETE/SEALED/FINAL). Handoff: `archive/session_handoffs/SESSION_HANDOFF_2026-06-30.md`.


## Current Phase (Phase-I historical record)

Phase I — Scientific Validation

## Current Goal

Determine whether evidence-first routing can reduce computational cost while preserving recall.

## Program Status Checklist

- Repository Reconstruction — ✅ Complete
- Scientific Audit (gap analysis, F1–F12) — ✅ Complete
- Remediation (F1, F2, F6, F8 + R-4..R-7) — ✅ Complete
- Pre-registration (v2) — ✅ Complete
- Seal (`phase1-prereg-v2`) — ✅ Complete
- GitHub (push + tag) — ✅ Complete
- PHASE1_EXECUTION_PLAN.md (M0 increment) — ✅ Authored + APPROVED (2026-06-15)
- M0 — Manifest freeze + leakage-safe split — ✅ DONE (Seal #1 `1f2d49e1…`, 2026-06-15)
- M1 — Stage-0 conditioning (η-sample) — ✅ DONE (188/200; 99% stationary / 88% white, 2026-06-15)
- M2 — Injection + η transit-preservation — ✅ DONE (window 2.5 d; gate PASS Rₚ≥2, 2026-06-16)
- M1 noise model recomputed at 2.5 d (M3 prerequisite) — ✅ DONE (188/188; 0.5 d archived, 2026-06-16)
- **M3 — threshold calibration → Seal #2 — ✅ DONE** (cleaned 854 null; Seal #2 `6292c018…`, 2026-06-16)
- **M4 dry-run — ✅ DONE (2026-06-18); TEST UNREAD** — harness built + validated; **Finding B blocks M4**
- **v3 re-registration — ✅ SEALED #2b (2026-06-19)** — tag `phase1-prereg-v3`; manifest `54f06a94…`; **confirmer-only** (both Lever-1b equivalence candidates failed); T_red=0 non-binding; ρ_d≈12.4% retained
- **M4 driver + dress rehearsal — ✅ DONE (2026-06-20)** — E1 PASS (−0.17pp, lo −0.51pp) · E2 FAIL (−5.6%, ρ_d 0.138) → verdict FALSIFIED–compute; recall-loss = one sub-margin pathway (cheap-confirm fallback-suppression). Machinery ready.
- **M4 SINGLE SEALED-TEST RUN — ✅ DONE (2026-06-24). VERDICT: H1 FALSIFIED — compute branch.** One irreversible read (P-5): 15,000 inj (30 cells × 500). **E1 PASS** (ΔR̄=−0.48pp, lo95 −0.60pp) · **E2 FAIL** (24.4%, ratio 0.756, ρ_d=14.4%; <30%). Recall non-inferiority supported; compute claim falsified (un-cheapenable B=1000 period-FAP). Seals intact, `git diff phase1-prereg-v3` empty (NN#2), TEST read once. A **successful negative Phase I**. → `research/m4_evaluation/M4_TEST_RESULT.md`.
- **Current milestone — M7 Phase-I write-up** (M5/M6 optional). Report the negative result; future ideas are P-8 (new pre-registered experiments). No v4 (P-2).

## Milestone Ladder

- Pre-registration completion + seal — ✅ DONE (2026-06-15)
- M0 execution plan authored + approved — ✅ DONE (2026-06-15)
- **M0 — Freeze sector/target manifest + leakage-safe split** — ✅ DONE — Seal #1 `1f2d49e1…`; 22,723 targets (S1–S3); cal 6,925 / test 15,798 (2026-06-15)
- **M1 — Stage-0 conditioning** (per-sector biweight detrend + masking → r(t); noise model σ/CDPP/τ_GP) — ✅ DONE (η-sample 188/200, 2026-06-15)
- **M2 — Injection + η ≥ 0.90 transit-preservation** — ✅ DONE — window finalized 2.5 d; gate PASS (Rₚ≥2); Rₚ=1 row noise-limited, 0.5/2 borderline (2026-06-16)
- **M3 — Threshold calibration (calibration only) → Seal #2** — ✅ DONE — untrained machinery built (whitened MF detector · integer-comb period + block bootstrap · pinned TLS 1.32); M1 noise model recomputed at 2.5 d; null-pool contamination found + cleaned (Prša 2022 + VSX + vetting → 854 of 1000); thresholds bootstrap-stable; w_c/π̂ instantiated; **Seal #2 `6292c018…`** (2026-06-16)
- **M4 dry-run (CALIBRATION/synthetic; TEST untouched)** — ✅ DONE (2026-06-18) — harness validated; guards block TEST; **Findings A + B surfaced**
- **M4 — Sealed-test evaluation (single run) → E1/E2** — ⛔ BLOCKED by Finding B (SDE not comparable across grid widths) — awaiting protocol amendment
- **Governance: adopt v3-as-final stopping rule (P-1…P-9)** — ✅ ADOPTED (2026-06-19)
- **Option-2 v3 re-registration (DR-002)** — ✅ DRAFTED + OWNER-APPROVED (2026-06-19) — transit-LR Arm-B arbiter (common-FAR keystone) + Lever-1b equivalence-gated period-FAP; VAL v3 / MATH v1.2 / HYP v2.1
- **Seal #2b** — ✅ CUT (2026-06-19) — confirmer-only v3 (both Lever-1b candidates failed equivalence); tag `phase1-prereg-v3`, manifest `54f06a94…`
- **M4 driver + CALIBRATION dress rehearsal** — ✅ DONE (2026-06-20) — E1 PASS / E2 FAIL → verdict FALSIFIED–compute; recall-loss = one sub-margin pathway; machinery ready
- **M4 — single sealed-TEST run → E1/E2** — ✅ DONE (2026-06-24) — one irreversible read; **E1 PASS (−0.48pp, lo −0.60pp) / E2 FAIL (24.4%, ρ_d 14.4%) → H1 FALSIFIED — compute branch.** Pre-committed verdict (VAL §7a) applied; seals intact; NN#2 clean. Successful negative Phase I.
- **M5 — parameter recovery + FAP calibration — ✅ DONE (2026-06-25)** — F5/F6, T4/T5 from existing data (period match 45.9%, median |ΔP/P| 0.0022 matched; FAP FAR 1.08% cleaned, reproduces sealed M3).
- **M6 — reality check + ablation + depth recovery — ✅ DONE (2026-06-25, test-blind)** — T6: TOI recall **86.7% (Arm B = Arm A)** on 30 real planets; EB rejection 12/16 (4 FP slip through). T8: FAP gate controls null FP (0→12.3% if removed); shape vetting trims recall (its value = EB rejection). T5-depth: fitted depth −20%, seed T14 −31%. Calibration + real TOI/EB only; TEST untouched; sealed thresholds unchanged. → `research/m6_reality_check/`.
- **M7 — Phase-I write-up — ▶ IN PROGRESS** — draft v0.1 (`papers/phase1_evidence_first_triage.md`) + references.bib + all T2–T8/F3–F8 generated. PRs #9/#10/#11 merged; M6 PR pending. Future ideas → P-8; no v4 (P-2).

## Sealed Documents (pre-registration set, hash-verified)

- SCIENTIFIC_HYPOTHESIS.md — **v2.1 SEALED** (`phase1-prereg-v3`)
- VESPER_PHASE1_VALIDATION.md — **v3 SEALED** (incl. App A; §7a stopping rule)
- VESPER_MATHEMATICAL_FOUNDATIONS.md — **v1.2 SEALED**
- v3 threshold manifest `data/manifests/m4/v3/m4_v3_threshold_manifest.json` (Seal #2b `54f06a94…`).
- Tags: `phase1-prereg-v2` (v2 baseline) · `phase1-prereg-v3` (v3 final, → commit `ff869d4b`). TEST read once (2026-06-24); v3 is the terminal amendment (P-2).

## Other Repository Documents

- VESPER.md (charter) · VESPER_ARCHITECTURE.md · VESPER_CONCEPT_RECONSTRUCTION.md
- REPOSITORY_GAP_ANALYSIS.md (F1–F12) · PHASE1_REMEDIATION.md
- PHASE1_READINESS_REPORT.md · decisions/F1_DECISION_RECORD.md (DR-001)
- PAPER_NOTES.md · references.bib · **SESSION_HANDOFF_2026-06-18.md** (latest; supersedes 2026-06-16)
- **Execution plans / choices:** PHASE1_EXECUTION_PLAN.md (M0) · PHASE1_M0_CHOICES.md · PHASE1_M1_PLAN.md · PHASE1_M2_PLAN.md · PHASE1_M3_PLAN.md (signed) · **PHASE1_M4_PLAN.md**
- **Tooling:** research/m0_manifest/ · research/m1_conditioning/ · research/m2_injection/ · research/m3_calibration/ · **research/m4_evaluation/** (harness + Finding-B diagnostics + 3 reports)
- **Artifacts/provenance:** data/manifests/m0 (Seal #1) · m1 (noise summary, 2.5 d + superseded_0.5d) · m2 (η table) · m3 (Seal #2 + exclusions; diagnostic_185/) · **m4/dry_run (dry-run + diagnostic CSVs; TEST untouched)**

## Findings Status

- Critical/Must-fix: F1, F2, F6, F8 — ✅ resolved and sealed
- Should-fix: R-4, R-5, R-6, R-7 — ✅ folded into v2 seal
- F7 (charter scoping note) — ✅ done; references.bib — ✅ created
- Remaining: Low hygiene only (F9 BLS wording) — non-blocking
- **M3 finding — null-pool contamination (R0-3/H4):** TOI-removed "null" pool retains unlabeled EBs/variables that inflate T and z_mono; resolved by Prša 2022 + VSX cross-match + automated EB vetting (derived M3 calibration subset; M0 null definition preserved). z⋆ unaffected.
- **M4 dry-run Finding A (fixable):** TLS narrow-window fallback to full grid (< 100 in-window periods) — implementation fix only; no sealed-value impact.
- **M4 dry-run Finding B (BLOCKING):** TLS SDE not comparable across grid widths → sealed Arm-B "SDE≥T on narrow window, single common T" rule invalid. **Blocks M4.** Resolution = Option-2 epoch-fixed arbiter (validated on CALIBRATION) → requires re-registration + Seal #2b. TEST unread; Seal #2 unchanged.

## M3 SEALED thresholds (Seal #2 `6292c018…`, cleaned 854-star null basis)

- **z⋆ = 3.4** (95% CI [3.30, 3.40]) · **z_mono = 5.3** ([5.0, 5.8]) · **T(SDE) = 10.74** ([9.74, 11.34]) · **α_FAP = 1%** (null exceedance 1.08%) · ε = 0.01 · N_min = 2.
- **w_c** (A.5): log-uniform period × K&M-2020 radius prior → 92.8% weight on Rₚ≤2 R⊕. **π̂ = 3.17%** (A.6). A.7 machine: Apple M4 (10 cores).
- Cleaning: 146 excluded (16 EB + 128 variable [overlap] + 14 vetted); **31 high-SDE survivors retained + audited**. M0 null definition preserved.
- **Seal #2 = `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`** (owner-approved 2026-06-16). Verify `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.

## M4 dry-run findings + board decisions (2026-06-18) — TEST UNREAD

- **Finding A (fixable):** TLS discards the narrow `[P̂(1±ε)]` window when it holds < 100 periods → returns the full grid; "targeted" search secretly ran full (cost ratio 0.995). In-window-grid fix → ratio 0.010.
- **Finding B (blocking):** TLS SDE is normalized over the searched grid → narrow-grid SDE (3.55) not comparable to full-grid SDE (40.36) / T=10.74. Sealed "targeted TLS, SDE≥T, single common T both arms" is internally inconsistent → E1 fails by construction.
- **Resolution diagnostics:** Option 1 (per-arm T_B, AUC 0.43) + Option 3 (wider window, AUC ≤0.72) **rejected**; **Option 2 — epoch-fixed matched-filter S/N** validated on the cleaned 854-null pool: **AUC 0.877**, range-invariant.
- **Combined-arm system dry-run:** recall-safe route→confirm→full-TLS-fallback. **E1 PASS** (ΔR̄=−0.39 pp, lo −0.80 pp) · **E2 FAIL** (~20–29% < 30%; ρ_d≈12% from B=1000 FAP + 59% FAP-gate fallback). T_red degenerate.
- **Methodology board:** Option-2 **APPROVED CONDITIONALLY as an AMENDMENT** (MATH §6 admits "transit-fit SNR"; NN#3 satisfied). Amends the fairness keystone ("same engine" → "common FAR"). Principle survives; targeted-TLS realization does not.
- **Governance board:** proposed **v3 = FINAL amendment + stopping rule (P-1…P-9)**; pre-commit outcomes; failure → falsification (no v4); new ideas → new experiments. **Pending owner adoption.**
- **E2-fix R&D (exploratory, CALIBRATION-only, no seal change):** the E2 failure is driven by the sealed **B=1000 period-FAP** (ρ_d≈12%) + 59% FAP-gate fallback. A **margined white-noise pre-filter** (reject only at white-FAP > ~5.5·α) skips the bootstrap on **97.5% of noise while clipping ZERO recoverable planets** (validated on injections; the bare white>α loses ~5%) → ρ_d→~0 → projected **E2 ~40% (PASS)**. **E2 is fixable**, but the fix touches **sealed A.8** → expands v3 scope (governance call). Not adopted.
- Reports: `research/m4_evaluation/` — `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Pre-filter R&D: `validate_prefilter{,_injections}.py` + `data/manifests/m4/dry_run/prefilter_*.csv`.

## Next Action

**M4 complete — H1 FALSIFIED (compute branch), a successful negative Phase I (2026-06-24).** Begin the **Phase-I write-up** (M7) from `research/m4_evaluation/M4_TEST_RESULT.md` + `docs/PAPER_NOTES.md`. Optional: open a PR `phase1/m4-v3-seal2b` → `main` (owner action). **No further amendment (P-2/P-8); v3 final; TEST read once and will not be read again.** Seal #1/#2/#2b intact.

## Notes

Repository is authoritative. Obsidian stores research memory. GitHub: github.com/Ansul-S/VESPER.
