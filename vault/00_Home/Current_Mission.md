# Current Mission

> **AUTHORITATIVE CURRENT STATE — updated 2026-08-27.** The detailed fields below this block are **Phase-I historical record** (kept for provenance); read this block first.

## ▶ Latest event (2026-08-27): MATHEMATICAL AUDIT — the routing ceiling

**Local, uncommitted. Calibration only (TEST not read, P-5 intact). Nothing sealed touched; all three sealed docs verified 0 differing lines vs `phase1-prereg-v3` (branding-normalised); Seal #2 hash matches DR-001 §5a; `frozen_rerun/` clean.**

Report: [`research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md`](../../research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md) · artifacts `data/manifests/math_audit/` · code `research/math_audit/` (5 scripts).

**The headline is a closed-form negative result.** Evidence-first period recovery gated on coherence significance obeys

$$W \equiv k\hat R^2 \ge \ln(N_{\rm eff}/\alpha),\qquad W \le \frac{N_{\rm tr}}{1+\rho_{\rm FP}} \;\Longrightarrow\; P \lesssim \frac{T_{\rm base}}{\ln(N_{\rm eff}/\alpha)}$$

Every tunable enters **logarithmically**; only the transit count enters linearly. Validated three ways and it survives a deliberate falsification attempt:

- Zero-free-parameter prediction of the sealed gate on 1,233 calibration nulls at **precision 87.5% / recall 75.7%** (TP 28 / FP 4 / FN 9 / TN 1192).
- **Out-of-sample scaling:** predicted $P_{\max}$ 2.94 d (1-sector) / 5.80 d (2-sector); measured $P_{50}$ **2.51 / 5.00 d**; predicted ratio 1.97, measured **1.99**. At $P=4$ d: 8.3% routing on 1-sector hosts vs 63.6% on 2-sector — identical planets, identical pipeline.
- **Mechanism:** at $P\ge8$ d, $\Pr(\text{gate open}\mid\text{seed correct}) = 0.20$ and $0.00$. Not a seeding failure — the significance budget.
- **Falsification failed:** sweeping $T_\beta = \hat R k^\beta$ at matched null FAR gains at most **+1.49 pp**; the *exactly pivotal* statistic **loses 10.31 pp**. The multiplicity dependence is the evidence, not a defect.

**Two corollaries settle what Phase I tested.** (1) **Subset region** — fast-path eligibility implies $\mathrm{SNR}_{\rm tot}\gtrsim10.2$ vs the sealed TLS $T=10.74$; measured, excluding the known $P=0.5$ d edge artifact, **17/17** fast-path recoveries were also found by full TLS and **0** were fast-path-only. E1's PASS was structurally guaranteed, and this is *why*. (2) The paradigm works only where transits are frequent — i.e. where a periodic search is already easy. The one regime it could add coverage in is monotransit ($N_{\rm tr}=1$), where no coherence test exists.

**Six further measured findings** — period-FAP is **82%** a multiplicity statistic; $\Lambda$'s null exceeds $\chi^2_1$ by up to 21 orders of magnitude in tail probability (**roadmap MATH-4 closed**); residuals are **red on transit timescales** ($\kappa$ to 9.0) while certified white from $\mathrm{acf}_1$; **79% of fast-path routings exist only because the bootstrap null is contaminated by the signal it tests** (**roadmap MATH-3 closed, its assumed direction reversed**); MATH §4b's fragility is linear not quadratic; MATH §9's "identical grid" premise is false in code and that deviation is what keeps $N_{\min}=2$ survivable (implementing the spec as written takes null FAR 2.99% → 4.37%).

**Sealed verdict UNCHANGED:** E1 PASS · E2 INCONCLUSIVE. FAR control intact (1.06% at nominal 1% on the cleaned pool).

**Owner decisions now open:** (1) does the ceiling become the paper's central result (it is the strongest defensible novel content and generalises beyond VESPER); (2) should $f_p$ be re-measured against a signal-free null before the paper quotes it; (3) do §C-1/§C-2/§C-3 go into `VESPER_MATH_ADDENDUM.md` as corrections of record. **The 2026-07-28 scope decision remains open and still first in line — this audit strengthens the methodology-reframing case.**

## ▶ Latest event (2026-08-17): INN-3 — the period-FAP entry tax is removable, **exactly**

**Branch `phase1/inn3-fap-acceleration` (local, not pushed). Nothing sealed touched; TEST not re-read.**

The blocker on the compute branch was the $B=1000$ period-FAP "entry tax" ($\rho_d = 11.6\%$), which DR-002/Lever-1b recorded as **not a removable artifact** after E-EVT and E-LUT both failed the equivalence gate 3/3. That verdict is right about the *estimator* and wrong about its *cost*. Both candidates tried to approximate the null distribution; the tax was never in the distribution.

- **Lever A — 49% of the FAP's cost was a loop invariant.** `detector.py:26,55` recompute `np.median(np.diff(np.sort(t)))` twice per duration per surrogate — **10,000 full sorts of an N-vector per star** — while the block bootstrap resamples the *flux*, not the epochs. Hoisting it + vectorising the local-max scan, the dedup (bucketed, identical greedy semantics) and the comb scan (one $(n_f\times k)$ matrix) gives **6.31×** with **bit-identical** output.
- **Lever B — the gate is exactly curtailable.** $(g_e+1)/1001 \le 0.01 \iff g_e \le 9$, so the **tenth exceedance decides the gate** and the run can stop. Curtailed sampling: the routing decision is identical *with probability one* (no error to bound), and one-sided, so it can never clip a planet. Total **73.2× on nulls**, 12.7× on injections.
- **Measured equivalence.** 1126/1126 calibration nulls reproduce the sealed recorded exceedance count (max |Δ| = 0); 149/149 calibration injections reproduce the sealed FAP bitwise. All three sealed Lever-1b criteria met with **exact zeros** (p95 |ΔFAP| 0.000; 0 discordant; 0 clipped; 0 FPs admitted) — the criteria E-EVT and E-LUT each failed 3/3.
- **E2 counterfactual** (arithmetic on the recorded ledger + `recovery.csv`; **no TEST re-read**): reduction **27.3% → 38.0%** (target ≥30%), $\rho_d$ **11.6% → 0.85%**, $\pi^\star$ **0.489 → 0.036** (≈16× → ≈1.2× the TESS $\pi\approx0.03$), $P(\text{ratio}\le0.70)$ **0.27 → 0.96**.
- **⚠️ But the frozen-rule decision stays INCONCLUSIVE — and *that* is the second finding.** With the routing cost set to **exactly zero** the host-clustered CI is still [0.522, **0.703**]. **E2's INCONCLUSIVE is a variance result, not a cost result:** between-host variance at $H=39$ clusters. The two causes are separable and both were necessary — the entry tax put the point estimate out of reach at *any* host count (sealed numbers stay INCONCLUSIVE even at $H=100$), and the erratum §2.1 parity bug (40 of 80 hosts drawn, 39 in the E2 subset) made the interval too wide at *any* cost. **Fix both and E2 PASSES at $H=79$ — the host count `m4_driver` was written to use.** Hosts needed: 49 (lever A+B), 65 (lever A), 41 (free detector), **never** (as recorded).
- **Side finding — RES-4 measured the wrong stratum for the M4 arm.** `m4_driver.py:117` sets `t14 = median(duration_grid)` but **line 120 overwrites it** with the seeded event's own duration before the FAP call on line 126 (`e2_retiming.py:67` replicates this; `m3_calibrate` genuinely uses 0.2 d). So M4 **duration-matched** $T_{14}$ — RES-4's "counterfactual" strata are the realised ones for M4 and its primary stratum is not. Seeded $T_{14}$ on 1126 nulls: 0.05 d 61.5%, 0.1 d 17.9%, 0.2 d 9.9%, 0.4 d 6.0%, 0.8 d 4.6%. Folding RES-4's own per-stratum flip counts through that mixture gives an M4-realised exposure of **≈1.4%** vs the 0.09% reported (~16×). **RES-4's conclusion survives; its stated mechanism and stratum labelling do not.**
- **Implementation-parity bound.** Arm A's TLS is numba-JIT-compiled; Arm B was interpreted numpy. A numba port of the surrogate loop reproduces $g_e$ exactly and is only **1.4–1.7×** faster than the vectorised numpy — so ≲2× of the routing cost is language, and the 6.31× is removal of unnecessary work, not a compilation trick.

**Deliverables:** `research/m4_evaluation/INN3_FAP_ACCELERATION.md` (result record) · `fast_period_fap.py` · `inn3_fap_acceleration.py` · `nb_period_fap.py` · `tests/test_inn3_fap_acceleration.py` (9 equivalence tests, green) · `docs/VESPER_MATH_ADDENDUM.md` §E (curtailment proposition + proof) · artifacts `data/manifests/m4/inn3/`.

**Sealed verdict UNCHANGED:** E1 PASS (robust) · E2 INCONCLUSIVE · P-2 holds (v3 final, no v4, TEST read exactly once). Roadmap **INN-3** (Wave 6) is delivered ~5 waves early with its proof obligations discharged rather than stated.

**Owner decisions now open:** (1) adopt `fast_period_fap` as the estimator of record for future runs → needs a decision record (DR-006+; DR-004 reserved for the Phase-II gate, DR-005 for the scope decision); (2) does the §6 counterfactual + §6.1a two-cause diagnosis go in the paper (it is the strongest answer to "was your compute result an implementation artifact?"); (3) does §7.1 warrant a RES-4 addendum. **The 2026-07-28 scope decision is still open and still first in line.**

## ▶ Latest event (2026-07-28): RES-4 DONE + Wave-2/4 closure — PR #21 MERGED

**`main` @ `77037d4`, clean, == `origin/main`. Seven commits merged; branch deleted; CI (`fast-units`) green.**

- **RES-4 COMPLETE (Wave 1)** — per-star τ_GP FAP sensitivity on **all 1163 cached calibration nulls** (1126 with ≥2 events). Erratum §2.4's masking *argument* is now a *measurement*. Gate flips at the sealed T₁₄ = 0.2 d convention: **arm B (as the post-audit driver applies it) 0/1126**, Wilson 95% [0, 0.0034]; **arm C (complete per-star coverage) 1/1126**, [0.0002, 0.0050]. Artifacts: `data/manifests/m4/wave1/res4_tau_fap_sensitivity.{json,md}` + `res4_per_star.csv`.
  - **Sealed fidelity BITWISE: 968/968** of M3's recorded FAPs reproduced (max |Δ| = 0.00e+00), comparing arm C on the 22 stars where M3 had an M1 τ row and arm A on the other 946.
  - **F2 (new) — erratum §2.4's own premise is imprecise.** `m3_calibrate.py:151` falls back to 0.005 for any star lacking an M1 noise-summary row, and only **22 of 968** overlapping stars had one: M3 was itself overwhelmingly flat-τ, so the calibration/test gap is far smaller than §2.4 implies.
  - **F3 (new)** — the single flip runs flat-OPEN → per-star-SHUT (TIC 80427281, τ = 0.289 d): the sealed gate was very slightly *more permissive* on red-noise nulls — the benign direction.
  - **F4 (new)** — the masking is bought by the **T₁₄ = median(duration grid) convention**, not by τ being harmless (arm C flips 24/1126 at a counterfactual T₁₄ = 0.05 d). Any future run that duration-matches T₁₄ **must** use per-star τ.
- **Wave 2 (math closure) — MATH-1, MATH-5, MATH-6, MATH-7 done.** Post-seal math lives in a new companion doc `docs/VESPER_MATH_ADDENDUM.md` (never inlined into the sealed MATH file, so `git diff phase1-prereg-v3` stays empty modulo branding — re-verified 0 differing lines on all three sealed docs after the merge).
  - **MATH-6** corrects the roadmap's own premise: "argmin → longest-P" is only ~74% true; the N=2 tie is broken by IEEE-754 rounding at ~1e-16. Sealed m∈{2,3} tolerance absorbs 98.1–98.6%; the 1.4–1.9% leaking to m≥4 are recall costs, never FPs. **New:** at N=2 the period-FAP tests event *rarity*, not coherence (reads with erratum §2.9).
  - **MATH-1** rejects the roadmap's "exact" π⋆. Derivation gives **π⋆ = ρ_d/(f_p(1−ρ))** — what `endpoints.py` and the paper already use; the roadmap's ρ_d/(f_p(1−ρ+ρ_d)) implies a routed star isn't charged for the detector that routed it. A **tautological unit test** (asserted `x == x`) was replaced with one that pins the derived form.
  - **MATH-5** — BCa host-cluster lo95 **−1.04 pp** vs sealed percentile **−0.83 pp** (a = −0.133 moves the effective tail 0.05 → 0.0072). The sealed interval is mildly optimistic, but **both clear the −2 pp margin: E1 non-inferiority UNCHANGED.**
- **Wave 3 — CODE-7** delivered as a side effect of MATH-5 (cluster bootstrap vectorized; verified **bit-exact** against `endpoints.e1_recall`).
- **Wave 4 — DOC-2** (`docs/INDEX.md`: every doc labeled SEALED/APPEND-ONLY/LIVE/HISTORICAL + reviewer and contributor reading paths) and **DOC-3** (`docs/SEAL_CHAIN_POSTMORTEM.md`: the 19-day rebrand break, for an external audience).
- Anti-tuning intact: **no sealed doc, threshold, manifest, or tag touched; `frozen_rerun/` untouched; TEST not read.** `verify_seal()` re-checked post-merge → z⋆=3.4 · z_mono=5.3 · N_min=2 · T=10.741 · α=0.01 · B=1000.

### ⚠️ OPEN DECISION carried into 2026-07-29 — project scope and the shape of the paper

**Status: DISCUSSED, NOT DECIDED.** The owner asked directly whether the project is worth continuing. The assistant's recommendation — *offered, not accepted or rejected*:

1. **Finish Phase I in ~2 weeks**, not 9–10. RES-6 is the last real scientific gap (absolute recall is optimistic: neither arm paid the conditioning cost η). Then fix the paper and submit. The work is ~90% done; abandoning now converts it to zero output.
2. **Cut `ROADMAP_TO_10.md` Waves 3 and 6** — package, CLI, container, API docs, seal library. None of it changes a number in the paper; it optimizes an invented ten-category scorecard rather than a deliverable.
3. **Do not start Phase II on momentum** — decide it separately, after submission.
4. **Reframe the paper.** The routing result is thin alone (π⋆ ≈ 0.49 vs π ≈ 0.03 is near a-priori derivable, and a referee may say so). The stronger contribution is the **methodology**: sealed single-shot validation with pre-committed verdicts, demonstrated by a case where the protocol *forced the authors to withdraw their own headline verdict* (E2 FAIL → INCONCLUSIVE), plus the 40-vs-80 host bug and the 19-day seal-chain break — all self-found and published. This is roadmap **INN-1**, currently scheduled last in Wave 6; the recommendation is to promote it to the **primary deliverable**.

**Settle this first tomorrow.** If accepted → record as **DR-005** (DR-004 stays reserved for the Phase-II gate) + amend `ROADMAP_TO_10.md`. Until then **the roadmap stands as written**. Full text: `archive/session_handoffs/SESSION_HANDOFF_2026-07-28.md` §6.

**Next action:** settle the scope decision above; then **RES-6** (η-paid injection; needs MAST, `data/raw` is empty) + the small **TLS-epoch re-run** (unlocks RES-3's symmetric sweep + the S-edge T₀ histogram). PR #22 (doc-only sync) is open and unmerged. Phase II hard-gated until DR-004.

## ▶ Latest event (2026-07-27): E2 RE-MEASUREMENT COMPLETE → verdict INCONCLUSIVE; Wave-0 V-1→V-4 done

**The frozen-rule E2 re-timing campaign finished (300/300 tasks × 5 repeats, 39 hosts).** The corrected Phase-I verdict is now settled and propagated:

- **CORRECTED VERDICT: E1 PASS (robust) · E2 INCONCLUSIVE.** Compute ratio **0.727** (27.3% reduction; target ≥30%), host-clustered bootstrap 95% CI **[0.636, 0.826]** straddles the 0.70 decision boundary → per VAL §5 the compute branch is *neither confirmed nor falsified*. ρ_d 11.6%, f_p 23.7%, **π\*≈0.489 ≫ π≈0.03** (routing is not a survey-scale compute-saver either way). This **supersedes** the sealed "H1 FALSIFIED — compute" AND the interim "E2 pending" lines. Results: `data/manifests/m4/e2_retiming/e2_retiming_summary.json`.
- **Robust to a Low-Power-Mode timing episode** (~28 tasks ran clock-capped on battery mid-run; caught + fixed to AC). Leave-out sensitivity: 0.713, still INCONCLUSIVE (erratum §5.1). No re-timing needed; disclosed.
- **Wave-0 progress:** V-1 resume guard + 4 unit tests ✅ (committed `2941175`); V-2 campaign ✅; V-3 erratum §5/§7 filled (no PENDING markers) ✅; V-4 verdict propagated to paper (abstract/§3.3/§3.4/§4/§5, v0.3), `M4_TEST_RESULT.md` addendum, `CLAUDE.md` status bullet, and this vault ✅. **V-5 pending:** commit the V-3/V-4 doc changes, push, un-draft the PR — **merge is the owner's call.**
- Anti-tuning intact: this work touched no sealed doc/threshold/tag (only V-1 code + `m4/e2_retiming/` outputs); TEST not re-read (frozen §6 re-times already-read injections; DR-003).

**Update (2026-07-27, cont.):** V-5 merged (PR #18 → `main`). **Wave 1 no-compute cluster COMPLETE** on branch `phase1/wave1-robustness`: RES-2 (KM-period E1 sensitivity → PASS robust, ΔR̄ −0.16 pp), RES-3 (epoch-tolerance → losses are epoch-predicate), RES-5 (edge-control supplement S-edge + fig S1), RES-8 (endpoint disclosure), RES-7 (monotransit design doc), PUB-6 (README/CHANGELOG reconciled). Each committed. **MERGED to `main` via PR #19** (owner, 2026-07-27); branch deleted. **Queued for a compute window:** RES-4 (per-star τ_GP FAP, ≥100 cal nulls) + RES-6 (η-paid injection, MAST) + a small TLS-epoch re-run (unlocks RES-3 symmetric sweep + S-edge T₀ histogram). **Next action:** run the RES-4/RES-6 compute batch (background, AC power / no Low Power Mode), then Waves 2 (math) + 3 (engineering) in parallel. Phase II hard-gated until DR-004. Resume point: `archive/session_handoffs/SESSION_HANDOFF_2026-07-27.md`.

**Prior next action (done):** V-5 (commit + push + un-draft PR; ask before merge), then Wave 1 (RES-2 first; PUB-6).

## ▶ 2026-07-20: deep scientific review → PHASE II RE-SCOPED; everything pushed to GitHub

**An idea-level panel review (persisted: `docs/reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md`) concluded the routing claim is structurally capped** (survey saving ≤ π·f_p ≈ 0.6% even at zero entry tax; the SES/FFA cheap coherent search attacks the premise itself) **and the project's real assets are the protocol, the unwritten impossibility bound, and the monotransit regime.** Owner accepted the pivot direction.

- **`docs/VESPER_PHASE2_PROGRAM.md` (DRAFT v0.1, pending DR-004):** G0 gating experiment (SES/FFA confrontation, pre-registered decision rules) + Track A (triage impossibility bound) + Track B (VESPER-Bench; Kepler DR25 enters only here) + Track C (event-wise **monotransit** pipeline, flagship — K=1 forces photometry-as-arbiter, repairing the Phase-I inversion; free pre-study = the 892 effective monotransits already in `recovery.csv`). Old Kepler routing-scaling sketch **superseded** (revivable only under G0-R3 + owner writing).
- **README updated** for the re-scoped future (public reconciliation partially executed: the withdrawn verdict is now stated on the repo front page). CLAUDE.md carries an interim supersession bullet (full rewrite at V-4).
- **All work committed + pushed** to `origin/phase1/audit-remediation`; draft PR to `main` opened (merge = owner call at V-5).
- **Wave 0 unchanged and still first:** E2 re-timing paused at 26/300 (resume V-1 guard, workers ≤6); erratum §5/§7 pending.

## ▶ 2026-07-19: FULL AUDIT → E2 VERDICT WITHDRAWN → remediation in flight (branch `phase1/audit-remediation`)

**An independent full-repository technical audit (2026-07-19) found the sealed M4 E2 verdict was not produced by the frozen protocol.** Authority: **DR-003** (`docs/decisions/DR-003_E2_REMEASUREMENT.md`); full defect register: **`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`**. No sealed doc/threshold/tag changed (NN#2, P-2 intact).

- **E2 "FAIL" WITHDRAWN as recorded** — the sealed run timed 12 stars × 1 wall-clock repeat vs the frozen §6 rule (≥10/cell, cap 300, ≥5 warm CPU-time repeats); bootstrap ratio CI **[0.42, 1.14]** = statistically undecided. Headline "H1 FALSIFIED — compute branch" is **superseded**: now *E1 PASS (robust) · E2 pending re-measurement*.
- **E1 PASS is robust** across three interval methods incl. a 40-host cluster bootstrap (lo95 −0.82 pp vs −2 pp margin). Host-count corrected: a stride bug used **40 of 80** drawn hosts.
- **E2 re-measurement under the frozen rule: PAUSED at 26/300 tasks** (owner needed the machine, ~23:20 IST). Ledger persists (`data/manifests/m4/e2_retiming/timing_ledger_full.csv`); resume needs a skip-done guard (V-1); keep **workers ≤6** (M4 = 4P+6E cores). ~19 h compute remain.
- **NEW (edge control, 2026-07-19 evening):** the P=0.5 d "gain region" is **not** a TLS grid-edge artifact — it is a **TLS epoch (T₀) failure**: 36/38 failures epoch-only at P=0.5 vs 98% recall at P=0.62. Gains and 80% of losses are ±0.5 T₁₄ predicate phenomena. Written into erratum §6 + paper §3.1/§3.2.
- **Second-pass audit report:** `docs/audits/PROJECT_AUDIT_2026-07-19.md` (scores: Docs 8.5, Repro 8, Research 7.5 … Pub 5, Prod 2). Key NEW findings: **w_c period dimension is log-uniform, NOT occurrence** (KM-period sensitivity = top missing analysis); π* formula inconsistency (MATH vs endpoints); seal integrity independently re-verified (0 non-branding diff lines vs `phase1-prereg-v3`).
- **Roadmap adopted:** `docs/ROADMAP_TO_10.md` — 6 waves (Verdict → Robustness → Math → Engineering → Repro/Docs → Publication → Tool/Phase-II-prep), ~50 working days. **Phase II (Kepler) is HARD-GATED until all waves complete + DR-004 sign-off.**
- **Uncommitted working tree** (intentional): erratum (§5/§7 pending E2), paper v0.2 edits, T1.csv (40 hosts), edge-control artifacts, audit report, roadmap. Commit = Wave-0 V-5.
- ⚠️ **Public surfaces (v1.0.0 release notes) still state the withdrawn verdict** — reconciliation is PUB-6 (Wave 1).

**Next action:** Wave 0 — V-1 resume-guard patch → V-2 finish E2 (~19 h) → V-3 erratum §5/§7 → V-4 propagate verdict (paper/CLAUDE.md/vault) → V-5 commit+merge. See `archive/session_handoffs/SESSION_HANDOFF_2026-07-19.md`.

## ▶ 2026-06-30: identity rebrand + first public release (v1.0.0)

**The project was rebranded from codename `TRINETRA-X` to `VESPER`** (the old name was already in use elsewhere). **Branding only — no science, methodology, equations, thresholds, results, or figures changed.** Acronym locked: **VESPER = Validation Engine for Stellar Photometric Evidence and Recovery** (also the evening star). The root folder is now `~/Desktop/VESPER` and the GitHub repo is **`github.com/Ansul-S/VESPER`**.

- **First public release `v1.0.0` cut** — annotated tag on `main` HEAD `0118548` + GitHub Release "VESPER v1.0.0 — Initial Public Release". `main` == `origin/main`; tree clean.
- **Sealed-artifact hash note:** rebranding the sealed docs/manifests **changed their recorded SHA-256 digests by design** (owner-authorized). See **`docs/decisions/F1_DECISION_RECORD.md` §5a** — any mismatch is from the naming change only; original sealed bytes are intact at tags `phase1-prereg-v2/v3`. ⚠️ `shasum` against the *old* recorded hashes will mismatch — read §5a first.
- **Repo reorganized (2026-06-30, structure-only, history preserved):** Phase-I plans → `research/phase1/`; handoffs → `archive/session_handoffs/`; `NEXT_SESSION_PROMPT.md` untracked+gitignored. Root holds only `README.md · CLAUDE.md · VESPER.md · references.bib · .gitignore`. No code/research content changed.
- **Phase I unchanged:** still COMPLETE / SEALED / FINAL. See `archive/session_handoffs/SESSION_HANDOFF_2026-06-30.md`.

## ▶ Where the project is now (2026-06-29)

- **Phase I (TESS) — COMPLETE & SEALED & FINAL.** M0–M7 done and merged (PRs #1–#13). H1 **falsified on the compute branch** (E1 recall non-inferiority PASS; E2 scoped compute FAIL 24.4% < 30%); recall principle **supported**. v3 is terminal — **no v4** (P-2). Seals intact: #2 `6292c018…`, #2b `54f06a94…`.
- **Phase II (Kepler scaling) — FROZEN** (owner decision 2026-06-26). The compute-path decision (HPC vs AWS) is likewise deferred. Sketch: `docs/PHASE2_KEPLER_SCALING_PREREG.md` (on the unmerged `phase2/kepler-scaling-prereg` branch).

---

*(Phase-I historical record follows — provenance only.)*

Project:
VESPER

Current Phase:
Phase I — Scientific Validation

Current Goal:
Determine whether evidence-first routing can reduce computational cost while preserving recall.

Current Status:
- Pre-registration **v2 SEALED** — git tag `phase1-prereg-v2` (commit `723087e`), pushed to GitHub.
- Decision **DR-001** recorded (F1 compute-scope decision).
- **No remaining Critical, Must-fix, or Should-fix findings.** (F1, F2, F6, F8 resolved; R-4, R-5, R-6, R-7 folded into v2.)
- **M0 EXECUTED (2026-06-15).** Seal #1 (manifest hash) `1f2d49e1…` cut; 22,723 SPOC 2-min targets (S1–S3 south); leakage-safe 30/70 split; TEST set sealed (read once at M4). M0.5 feasibility passed — no sector widening needed.

Current Milestone:
**M4 — single sealed-TEST run — ✅ DONE (2026-06-24). VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** The single irreversible TEST read was executed once (P-5): 15,000 injections (30 cells × 500, literal ≥500/cell), ~65 h on M4. **E1 recall non-inferiority PASS** (ΔR̄=−0.48 pp, one-sided 95% lo −0.60 pp; margin −2 pp). **E2 scoped compute FAIL** (reduction 24.4%, ratio 0.756, ρ_d=14.4%; target ≥30%). Pre-committed verdict (VAL §7a) applied. Recall principle holds; compute claim is the falsified branch (un-cheapenable B=1000 period-FAP entry tax — the Lever-1b gate had already proven it un-cheapenable). A **successful negative Phase I**. Integrity: both seals hash-verified in-run + intact; `git diff phase1-prereg-v3` empty (NN#2); TEST read exactly once. Result record: `research/m4_evaluation/M4_TEST_RESULT.md`; artifacts `data/manifests/m4/test_run/`. **TEST conditioning** (sanctioned first-touch): 80/80 hosts via frozen Stage-0 (`research/m1_conditioning/condition_test_hosts.py`, exactly the driver's `sample(80, random_state=22)` draw).
- **M3 — Threshold calibration → Seal #2 — ✅ DONE (2026-06-16).** z⋆=3.4 · z_mono=5.3 · T=10.74 · α_FAP=1% · ε=0.01 · N_min=2; w_c (92.8% on Rₚ≤2) · π̂=3.17%; Seal #2 `6292c018…`. Cleaned 854-null basis (146 EB/variable exclusions). Sealed pre-reg docs unmodified.
- **Finding A (implementation, fixable):** TLS discards the narrow `[P̂(1±ε)]` window when it holds < 100 periods (returns full grid) → "targeted" search secretly ran full (ratio 0.995). Feeding in-window periods directly → real saving (ratio 0.010).
- **Finding B (methodology, BLOCKING — confirmed):** TLS **SDE is normalized across the searched grid**, so a narrow-grid SDE (3.55) is not comparable to the full-grid SDE (40.36) that calibrated T=10.74. The sealed "targeted TLS, SDE≥T, single common T both arms" rule is internally inconsistent → Arm B would reject planets Arm A accepts → E1 fails by construction.
- **Resolution (CALIBRATION-only diagnostics):** Option 1 (per-arm narrow-SDE T_B) and Option 3 (wider window) **rejected on evidence** (AUC 0.43 and ≤0.72). **Option 2 — epoch-fixed matched-filter S/N** (evidence-first P̂ + t̂₀; no grid) **validated**: AUC 0.877, FAR-controllable, range-invariant.
- **Combined-arm system dry-run (CALIBRATION-only, 2026-06-18):** full recall-safe Option-2 architecture (route→confirm→full-TLS fallback). **E1 PASS** (ΔR̄=−0.39 pp, one-sided 95% lo −0.80 pp) · **E2 FAIL** (ratio 0.799 → ~20% reduction; population estimate ~29%; <30%). E2 shortfall is structural: ρ_d≈12.4% (sealed B=1000 FAP charged on every routed star) + 59% of routed stars fail the FAP gate → full-TLS fallback. T_red degenerate (FAP gate, not MF, does FP rejection). **Ignore E1/E2 for the philosophical question.**
- **Methodology review-board (2026-06-18): Option-2 APPROVED CONDITIONALLY as an AMENDMENT (not a replacement).** MATH §6 admits "transit-fit SNR" as an arbiter form, so Option-2 complies with Non-Negotiable #3 (folded-photometry significance, not timing coherence; repairs the v3 errors). It **amends the fairness keystone** ("same TLS engine both arms" → "common false-alarm rate"). Conditions: (1) arbiter must be a genuine folded-photometry transit LR (the box depth-SNR is borderline); (2) re-register the keystone change transparently; (3) anti-tuning discipline. The evidence-first **principle survives**; the **targeted-TLS realization does not** (Finding B).
- **Governance review-board (2026-06-18): proposed v3 = FINAL permissible amendment + Phase-I stopping rule (P-1…P-9).** Pre-commit the E1/E2/inconclusive outcome mapping before TEST; one evaluation; failure → pre-committed falsification (no v4); new ideas → new pre-registered experiments. `research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md`. **Pending owner adoption.**
- **E2-fix R&D (2026-06-18, EXPLORATORY — CALIBRATION-only, no seal change):** diagnosed *why* E2 fails (ρ_d≈12% from the sealed **B=1000 period-FAP** + 59% FAP-gate fallback). A **margined white-noise pre-filter** was validated on injections: the *bare* "reject if white-FAP > α" loses ~5% of real planets, but rejecting only at **white-FAP > ~5.5·α** clips **ZERO recoverable planets while still skipping the bootstrap on 97.5% of noise** → ρ_d→~0 → projected **E2 ~25%→~40% (PASS)**. **Implication: E2 is *fixable*, not a fundamental falsification.** BUT the fix touches **sealed A.8 (period-FAP) machinery**, so adopting it would **expand the v3 scope beyond the Option-2 confirmer** (a governance call that bumps the v3-as-final rule). Not adopted; informs the pending decisions. Artifacts: `research/m4_evaluation/validate_prefilter{,_injections}.py`, `data/manifests/m4/dry_run/prefilter_*.csv`.

- **OWNER 4-STEP GATE DECIDED + v3 PACKAGE DRAFTED & APPROVED (2026-06-19).** Owner adopted, in order: **(1)** the v3-as-final stopping rule **P-1…P-9** + pre-committed outcome mapping; **(2)** NN#3 condition #1 = **YES** — the arbiter is a genuine **transit-template likelihood-ratio** (Λ/ΔBIC), box depth-SNR **rejected**; **(3)** v3 **SCOPE = Option-2 confirmer + Lever 1b (period-FAP cheapening), equivalence-gated** — Lever 1a subsumed/excluded, Lever 2 (harmonics) deferred to P-8; **(4)** drafting authorized. **DR-002 ADOPTED** (`docs/decisions/DR-002_DECISION_RECORD.md`). v3 re-registration drafted & owner-approved on governance / consistency / anti-tuning / equivalence-gate / T_red logic: **VAL v3, MATH v1.2, SCIENTIFIC_HYPOTHESIS v2.1** (keystone A6 → common-FAR; Arm-B confirm → transit-LR + full-TLS fallback; A.8a equivalence-gated cheap period-FAP; A.11 confirmer + T_red; §7a stopping rule). Plans: `LEVER1B_EQUIVALENCE_VALIDATION_PLAN.md`, `TRED_CALIBRATION_PLAN.md`. **No sealed numeric value changed; TEST unread; nothing committed/tagged/sealed.**

- **SEAL #2b CUT (2026-06-19) — v3 = CONFIRMER-ONLY.** Tag `phase1-prereg-v3` (annotated → commit `ff869d4b`); v3 manifest `54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18`. **Confirmer spec locked** (transit-LR: D-1a depth-only linear GLS · D-2a GP marginal likelihood · D-3-i no t₀ refinement; box depth-SNR rejected). **Lever-1b equivalence FAILED both candidates** (E-EVT: p95 ΔFAP 0.085, 7 FP-admit, 2 clipped; E-LUT: 0.104, 9 FP-admit, 2 clipped) → pre-committed fallback → period-FAP stays sealed B=1000 bootstrap, **ρ_d≈12.4% retained**. **T_red=0.0** (non-binding, FAR-calibrated; end-to-end Arm-B FAR 0.12%; confirmer rejects 8/9 FAP-gate-passing nulls; AUC 0.894). No sealed numeric value changed; TEST unread; Seal #1/#2 intact. Evidence: `research/m4_evaluation/LEVER1B_EQUIVALENCE_RESULT.md`, `TRED_CALIBRATION_RESULT.md`; manifest `data/manifests/m4/v3/`.

- **M4 DRIVER BUILT + DRESS REHEARSAL COMPLETE (2026-06-20, CALIBRATION-only).** `m4_driver.py` (one driver for dry-run + token-gated TEST): Arm A full TLS; Arm B route→B=1000 FAP gate→transit-LR confirmer (sealed T_red=0)→full-TLS fallback; E1 occurrence-weighted ΔR̄+one-sided 95% CI; E2 compute ledger; dual hash-verify + TEST token guard. Instrumented dress rehearsal (240 injections, per-cell 8): **E1 PASS** (ΔR̄=−0.17 pp, lo95=−0.51 pp; the earlier per-cell-5 "fail" lo −5.19 was underpowered noise) · **E2 FAIL** (reduction −5.6%, ρ_d=0.138). **Verdict: FALSIFIED — compute branch (E1 pass, E2 fail).** Recall-loss fully characterized: 14/240 losses, **ALL one pathway** (cheap-confirm suppresses fallback), 11 right-period/wrong-epoch (detector t̂₀ less precise than TLS T₀) + 3 wrong-period; **sub-margin**, does not threaten E1. Genuine limitation = E2 (un-cheapenable B=1000 FAP entry tax), not a confirmer bug. Readiness: `research/m4_evaluation/M4_DRESS_REHEARSAL_READINESS.md`.

Next Milestone:
**M7 — Phase-I write-up (well advanced).** Draft v0.1 in `papers/phase1_evidence_first_triage.md`; tables T2/T3/T7 + figures F3/F8 (M4), T4/T5 + F5/F6 (M5), T6/T8/T5-depth + F5b/c (M6) generated. `docs/references.bib` compiled (ADS-verify pending). PRs #9/#10/#11 merged to `main`; M6 PR pending. **M5 + M6 EXECUTED (2026-06-25, test-blind characterization)** — see Current Milestone history below. Remaining for M7: compile/verify references, optional F1/F4/F7/F9/T1, venue decision. Future architectural ideas are **P-8 only** (new pre-registered experiments); no v4 (P-2).

Next Action:
**Finish the M7 write-up** from the manuscript draft + PAPER_NOTES (M4/M5/M6 results all folded in). Bundle the M6 PR (`phase1/m6-plan` → `main`). No further amendment (P-2/P-8); v3 is final; TEST read once and will not be read again. M6 was characterization only (calibration + real TOI/EB objects; TEST never touched; sealed thresholds unchanged).

Execution Plan:
`PHASE1_M4_PLAN.md` (M4 execution plan). Dry-run + diagnostics + governance: `research/m4_evaluation/` — reports `M4_DRYRUN_VALIDATION.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_COMBINED_ARM_RESULT.md`, `M4_OPTION2_REVIEW_BOARD.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `PHASE1_AMENDMENT_STOPPING_RULE.md`. Diagnostic data: `data/manifests/m4/dry_run/`.

Sealed Documents (SEALED at `phase1-prereg-v3`, 2026-06-19; do not edit without a new re-registration — but P-2 forbids a v4):
- SCIENTIFIC_HYPOTHESIS.md — **v2.1 SEALED**
- VESPER_PHASE1_VALIDATION.md — **v3 SEALED** (incl. App A: A.8a no cheap estimator, A.11 transit-LR + T_red; §7a stopping rule)
- VESPER_MATHEMATICAL_FOUNDATIONS.md — **v1.2 SEALED**
- v3 threshold manifest `data/manifests/m4/v3/m4_v3_threshold_manifest.json` (Seal #2b `54f06a94…`).
- Tags: `phase1-prereg-v2` (v2 baseline) · `phase1-prereg-v3` (v3, → commit `ff869d4b`).

Decision Records:
docs/decisions/F1_DECISION_RECORD.md (DR-001) · docs/decisions/DR-002_DECISION_RECORD.md (DR-002 — Finding B, Option-2 v3 amendment, stopping rule)

GitHub:
origin = https://github.com/Ansul-S/VESPER — `main` pushed; tags `phase1-prereg-v2`, `phase1-prereg-v3`, `m0-manifest-v1`, and release `v1.0.0` (2026-06-30) on the remote.

Anti-tuning status:
M0 read **catalog metadata only** (no flux). All calibration/amendment decisions (M1–M3, v3/Seal #2b, dress rehearsal) were made TEST-blind. **TEST was read exactly once (2026-06-24, P-5)** — the single sealed M4 evaluation. The sealed protocol was frozen *before* the read: `git diff phase1-prereg-v3` over sealed docs + manifests is **empty**, both seals hash-verified in-run and intact, no threshold/statistic/weight/config moved. The verdict (E1 pass / E2 fail) was pre-committed (VAL §7a) before the read. Anti-tuning (NN#2) intact end-to-end. **TEST will not be read again** (P-2: v3 is final; no v4).

Non-blocking follow-ons (do not affect sealed hashes):
- Create references.bib (Kunimoto & Matthews 2020 is load-bearing)
- Add the one-line Phase-I scoping note to the charter (docs/VESPER.md)
