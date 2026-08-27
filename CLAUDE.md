# CLAUDE.md — VESPER Operating Rules

> Project rules for any Claude Code session in this repository. Read this first. Keep edits to this file under ~200 lines.

## What this project is

VESPER is an **evidence-first** exoplanet-detection research program for the **TESS** era (ISRO exoplanet challenge). It tests whether *routing on evidence* — detect transit-like events cheaply, infer the period from their spacing, confirm with physics, and run a full search only where no evidence exists — can cut compute without sacrificing recall. Authoritative charter: [`docs/VESPER.md`](./docs/VESPER.md).

**Current phase: Phase I — Scientific Validation.** Goal: prove (or falsify) that evidence-first routing beats full TLS on TESS. We are *validating a principle*, not building a product.

## Session Initialization Rule

Do not assume prior chat history exists.

All project knowledge must be derived from repository documents.

If information is missing from the repository, explicitly identify the gap rather than assuming historical context.

## Knowledge Management

Repository documents are authoritative.

Obsidian is the long-term research memory system.

Important discoveries must be written into repository documents and/or Obsidian notes.

No critical project knowledge should remain only inside chat history.

Chats are temporary.

Documents are memory.

## Obsidian Vault

A project Obsidian vault exists at:

vault/

Purpose:

- Long-term research memory
- Literature notes
- Discovery tracking
- Experiment logs
- Publication planning

Repository documents remain authoritative.

Obsidian notes are working research notes and knowledge-management artifacts.

When a significant discovery, benchmark result, mathematical insight, experimental lesson, or publication idea emerges, recommend recording it in the appropriate vault note.

Do not treat Obsidian notes as authoritative specifications unless explicitly promoted into repository documentation.

### Vault synchronization (after major project-state changes)

After any major change to project state — a resolved finding, a decision record, a re-registration, a seal/tag, a milestone start or completion, or a GitHub publish — **synchronize the vault in the same session**:

1. `vault/00_Home/Current_Mission.md` — current status, blockers, current + next milestone, next action.
2. `vault/00_Home/Dashboard.md` — phase, milestone ladder, completion checklist, document list.
3. `vault/01_Research_log/Daily_Research_Log.md` — append a dated entry (decisions, artifacts, risks, next action).
4. On session end, create `SESSION_HANDOFF_<YYYY-MM-DD>.md` so a fresh session can resume with zero reliance on chat history.

The vault must never contradict the repository. The repository is authoritative; the vault mirrors it. Convert relative dates to absolute.

## Prime directive

> **Find evidence first. Spend computation second. Let physics decide.**
> A false positive is acceptable; a missed planet is not. **Photometric significance — depth, shape, repetition — not timing coincidence — is what makes a candidate a planet.** (This is the corrected lesson of the prior version; see [`docs/VESPER_CONCEPT_RECONSTRUCTION.md`](./docs/VESPER_CONCEPT_RECONSTRUCTION.md) §E.)

## Non-negotiables (do not violate)

1. **Recall > precision.** Never trade away a real planet to improve precision.
2. **No tuning on test data.** Thresholds are set on the calibration set, then sealed. One evaluation on the test set.
3. **Physics decides detection.** The confirmation gate (transit-model significance), not a coherence score, is the arbiter.
4. **Benchmark everything.** Every claim is measured against full TLS on identical data.
5. **Calibrate every confidence.** No uncalibrated scores; period FAP is bootstrap-calibrated, probabilities are conformal.
6. **Reproducible by construction.** Frozen manifests, seeds, versions; provenance carried end-to-end.
7. **Evidence overrides assumptions; physics overrides heuristics; recall over elegance.**

## Working agreement for agents

- **Do not build prematurely.** Phase I has **no learned models, no dashboards, no deployment**. Phase I uses a *simple, untrained* detector on purpose, so a pass/fail is attributable to the routing *principle*, not a model.
- **Pre-registration discipline.** [`docs/VESPER_PHASE1_VALIDATION.md`](./docs/VESPER_PHASE1_VALIDATION.md) and [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) freeze the experiment. **Changing a frozen parameter after data is touched is forbidden.** Amendments made *before* data is read are legitimate but must be **re-dated** as a new pre-registration version.
- **Sign-off gates.** Frozen-parameter decisions, threshold calibrations, and seal creation require **explicit owner review/sign-off before execution** — present choices (and provisional results) for approval first; never derive or seal without it.
- **Documents remain the authoritative deliverables.** Specs/decisions are Markdown with LaTeX math (`$…$`). Milestone **execution tooling now exists** under `research/m0_manifest/`, `research/m1_conditioning/`, `research/m2_injection/` (M0–M2); the sealed protocol still governs and "no premature Phase II machinery" still holds.
- **Negative results are results.** A clean falsification of the hypothesis is a successful Phase I, to be reported with equal rigor.
- **Ask before scope expansion.** If a task implies building Phase II machinery (learned detector, classifier, habitability), confirm first.

## Document map (canonical sources)

| Document | Role |
|----------|------|
| [`docs/VESPER.md`](./docs/VESPER.md) | Master charter (author: Ansul Suryawanshi) |
| [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) | Formal H1/H0 + secondary hypotheses, assumptions, success/failure criteria |
| [`docs/VESPER_MATHEMATICAL_FOUNDATIONS.md`](./docs/VESPER_MATHEMATICAL_FOUNDATIONS.md) | Canonical theory (math only) |
| [`docs/VESPER_ARCHITECTURE.md`](./docs/VESPER_ARCHITECTURE.md) | 7-stage system design (full vision) |
| [`docs/VESPER_PHASE1_VALIDATION.md`](./docs/VESPER_PHASE1_VALIDATION.md) | Pre-registered Phase I protocol |
| [`docs/VESPER_CONCEPT_RECONSTRUCTION.md`](./docs/VESPER_CONCEPT_RECONSTRUCTION.md) | Concept lineage & v3 post-mortem |
| [`docs/PAPER_NOTES.md`](./docs/PAPER_NOTES.md) | Publication notebook |
| [`docs/REPOSITORY_GAP_ANALYSIS.md`](./docs/REPOSITORY_GAP_ANALYSIS.md) | Critical cross-document review (12 findings) |
| [`docs/PHASE1_REMEDIATION.md`](./docs/PHASE1_REMEDIATION.md) | Plan to fix the Critical + Must-fix findings (**resolved** — see DR-001) |
| [`docs/PHASE1_READINESS_REPORT.md`](./docs/PHASE1_READINESS_REPORT.md) | Phase I scientific-readiness assessment |
| [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md) | DR-001 — F1 compute-scope decision + seal record |
| [`PHASE1_EXECUTION_PLAN.md`](./research/phase1/PHASE1_EXECUTION_PLAN.md) · [`PHASE1_M0_CHOICES.md`](./research/phase1/PHASE1_M0_CHOICES.md) | M0 execution plan + signed frozen choices (Seal #1) |
| [`PHASE1_M1_PLAN.md`](./research/phase1/PHASE1_M1_PLAN.md) | M1 Stage-0 conditioning plan + signed choices |
| [`PHASE1_M2_PLAN.md`](./research/phase1/PHASE1_M2_PLAN.md) | M2 injection + η transit-preservation; detrend-window finalization (2.5 d) |
| [`PHASE1_M3_PLAN.md`](./research/phase1/PHASE1_M3_PLAN.md) | M3 threshold calibration + signed choices; null-pool cleaning; **Seal #2** record |
| [`archive/session_handoffs/SESSION_HANDOFF_2026-08-17.md`](./archive/session_handoffs/SESSION_HANDOFF_2026-08-17.md) | Latest session handoff (resume point). All handoffs live in `archive/session_handoffs/`; `NEXT_SESSION_PROMPT.md` is now untracked/gitignored (local AI-workflow scratch) |
| [`research/m4_evaluation/INN3_FAP_ACCELERATION.md`](./research/m4_evaluation/INN3_FAP_ACCELERATION.md) | INN-3 — the period-FAP entry tax removed exactly (bit-identical estimator + exact curtailment); E2 re-diagnosed as a variance result |
| [`research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md`](./research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md) | Mathematical audit + new results — the routing ceiling; MATH-3/MATH-4 closed; corrections of record |
| [`docs/VESPER_MATH_ADDENDUM.md`](./docs/VESPER_MATH_ADDENDUM.md) | Post-seal mathematics (append-only companion to the sealed MATH doc): §A comb identifiability · §B notation · §C π⋆ · §D BCa · §E curtailment |
| [`archive/`](./archive/) | Historical (Revival-era audit & review) — context only, not current |

## Directory map

```
docs/        canonical specifications and theory
src/         pipeline-stage scaffold (Phase-I tooling lives in research/):
             conditioning, detector, period_recovery, confirmation, classifier, evaluation
data/        manifests/{m0,m1,m2,m3} = provenance + results (tracked; m3 holds Seal #2);
             raw/processed/injections/benchmark = local caches (gitignored)
research/    m0_manifest … m4_evaluation, m6_reality_check (milestone tooling);
             phase1/ = Phase-I planning docs (PHASE1_EXECUTION_PLAN, M0_CHOICES, M1–M4/M6 plans);
             + experiments, benchmarks, validation, literature
results/     outputs (empty)
notebooks/   exploratory notebooks (empty)
papers/      manuscript drafts
archive/     prior-project audit & review (reference only);
             session_handoffs/ = historical SESSION_HANDOFF_*.md logs
```

## Current status & immediate next step

> The bullets below are **operational status**, not editable specifications. The sealed protocol (next bullet) is the spec; do not treat status lines as commitments to amend.

- **Pre-registration is SEALED (v2, 2026-06-15).** All Critical/Must-fix (F1, F2, F6, F8) + should-fix (R-4..R-7) resolved in the seal. Remaining gap items are Low hygiene only (F9 BLS wording).
- **F1 decision (DR-001):** compute claim scoped to the fast-path-eligible population; survey-representative compute is a pre-registered *secondary* endpoint (ρ_d, π\*); clean-skip deferred to Phase II. [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md).
- **Sealed documents (do not edit without a new re-registration):** `SCIENTIFIC_HYPOTHESIS.md` v2.0, `VESPER_PHASE1_VALIDATION.md` v2 (incl. Appendix A), `VESPER_MATHEMATICAL_FOUNDATIONS.md` v1.1. Seal = git tag **`phase1-prereg-v2`** (commit `723087e`), pushed (`origin` = github.com/Ansul-S/VESPER). Content hashes in DR-001.
- **M0 / M1 / M2 / M3 EXECUTED (2026-06-15 → 16):**
  - **M0** — manifest + leakage-safe split. **Seal #1** (manifest SHA-256 `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`). Sectors **S1–S3**; **22,723** targets; calibration 6,925 / test 15,798. Manifest table = release asset `m0-manifest-v1` (hash + provenance in git).
  - **M1** — Stage-0 conditioning (wotan biweight + noise model). η-sample 188/200. **Noise model recomputed at the finalized 2.5 d window** (188/188; 0.5 d superseded → `data/manifests/m1/superseded_0.5d/`).
  - **M2** — injection + η transit-preservation. **Detrend window finalized at 2.5 d.** η gate PASS on Rₚ≥2; **Rₚ=1 row excluded as noise-limited** (detectability bimodality); 0.5/2 documented borderline.
  - **M3** — threshold calibration on the cleaned null pool → **Seal #2** (threshold manifest SHA-256 `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`). Sealed: **z⋆=3.4 · z_mono=5.3 · N_min=2 · T=10.74 · α_FAP=1% · ε=0.01**; **w_c** (A.5; 92.8% weight on Rₚ≤2 R⊕) · **π̂=3.17%** (A.6; Kunimoto & Matthews 2020). **Null-pool EB/variable contamination found + cleaned** (Prša 2022 + VSX + automated vetting; 854 of a 1000-star null draw; M0 null definition preserved). Verify: `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`.
- **v3 RE-REGISTRATION SEALED (#2b, 2026-06-19) + M4 DRESS REHEARSAL (2026-06-20).** Finding B made targeted-TLS non-executable → v3 re-registration (DR-002), sealed **confirmer-only** (Arm-B = folded transit likelihood-ratio at common FAR; keystone A6 relaxed). Lever-1b period-FAP cheapening DROPPED (both candidates failed the equivalence gate) → sealed B=1000 bootstrap stands, ρ_d retained; T_red=0.0. Tag `phase1-prereg-v3` (→ `ff869d4b`); v3 manifest `54f06a94…c9b18`. VAL v3 / MATH v1.2 / HYP v2.1 sealed.
- **M4 SINGLE SEALED-TEST RUN EXECUTED — ✅ DONE (2026-06-24). VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** One irreversible read (P-5): 15,000 injections (30 cells × 500, literal ≥500/cell). **E1** recall non-inferiority PASS (ΔR̄=−0.48 pp, one-sided 95% lo −0.60 pp; margin −2 pp). **E2** scoped compute FAIL (reduction 24.4%, ratio 0.756, ρ_d=14.4%; target ≥30%). Recall principle holds; compute claim is the falsified branch (un-cheapenable B=1000 period-FAP entry tax). Pre-committed verdict (VAL §7a) applied — a **successful negative Phase I**. Result record: [`research/m4_evaluation/M4_TEST_RESULT.md`](./research/m4_evaluation/M4_TEST_RESULT.md); artifacts `data/manifests/m4/test_run/`. TEST conditioning (first-touch) via frozen Stage-0: `research/m1_conditioning/condition_test_hosts.py` (80/80 hosts).
- **TEST read exactly once (P-5); will not be read again (P-2: v3 is final; no v4).** Anti-tuning (NN#2) intact end-to-end: `git diff phase1-prereg-v3` over sealed docs + manifests empty; both seals hash-verified in-run + intact; verdict pre-committed before the read.
- **⚠️ AUDIT REMEDIATION (2026-07-19 → 07-27, DR-003 — branch `phase1/audit-remediation`): the sealed M4 "H1 FALSIFIED — compute" verdict above is SUPERSEDED.** The recorded E2 "FAIL" (sealed timing = 12 stars × 1 repeat; ratio CI [0.42, 1.14] undecided) was withdrawn, and the frozen-rule E2 re-measurement is now **COMPLETE**. **CORRECTED PHASE-I VERDICT: E1 PASS (robust; host-cluster lo95 −0.82 pp; host count corrected to 40) · E2 INCONCLUSIVE** — frozen §6 rule on 300 injections × 5 repeats / 39 hosts → compute ratio **0.727** (27.3% reduction; target ≥30%), host-clustered CI **[0.636, 0.826]** straddles the 0.70 boundary; ρ_d 11.6%, f_p 23.7%, **π\*≈0.489 ≫ π≈0.03** (not a survey-scale compute-saver). Recall principle validated; compute claim neither confirmed nor falsified at decision-grade precision. Robust to a Low-Power-Mode timing window (leave-out 0.713, still INCONCLUSIVE; erratum §5.1). Edge control (2026-07-19): P=0.5 d gains/losses are **epoch-predicate** phenomena, not detection power. **Wave 0 status:** V-1 (resume guard + tests) ✅ committed `2941175`; V-2 (E2 campaign 300/300) ✅; V-3 (erratum §5/§7 filled) ✅; V-4 (verdict propagated to paper §3.3/§3.4/abstract/§4/§5, M4_TEST_RESULT addendum, this bullet, vault) ✅; **V-5 ✅ (PR #18 merged).** **WAVE 0 COMPLETE. Wave 1 no-compute cluster ✅ (RES-2/3/5/7/8, PUB-6; PR #19 merged)** — E1 robust to KM period weighting (ΔR̄ −0.16 pp) + losses are epoch-predicate. **RES-4 ✅ + Wave-2/4 closure ✅ (2026-07-28, PR #21 merged):** **RES-4** per-star τ_GP FAP sensitivity on all 1163 cached calibration nulls → at the sealed T₁₄=0.2 d convention, gate flips **0/1126** (arm B, as the driver applies it; Wilson 95% [0, 0.0034]) and **1/1126** (arm C, complete per-star coverage; [0.0002, 0.0050]) — erratum §2.4's masking argument is now **measured**, sealed FAPs reproduced **bitwise 968/968**. New findings: §2.4's own premise is imprecise (M3 used per-star τ for only **22 of 968** overlapping stars — it was overwhelmingly flat-τ too); the lone flip is flat-OPEN→per-star-SHUT (sealed gate slightly *more permissive* on red-noise nulls — benign direction); the masking is bought by the **T₁₄=median convention**, so any future run that duration-matches T₁₄ **must** use per-star τ (24/1126 flips at a counterfactual T₁₄=0.05 d). **MATH-1** π⋆ derived = ρ_d/(f_p(1−ρ)) — code+paper correct, the roadmap's "exact form" rejected (it implies a routed star isn't charged for its own detector); a tautological unit test replaced. **MATH-5** BCa host-cluster lo95 −1.04 pp vs sealed percentile −0.83 pp → sealed interval mildly optimistic, **E1 non-inferiority unchanged**. **MATH-6** N=2 comb degeneracy proven+measured ("argmin→longest-P" only ~74% true; at N=2 the FAP tests event *rarity*, not coherence). **MATH-7** notation cross-reference. **CODE-7** cluster bootstrap vectorized (bit-exact). **DOC-2** [`docs/INDEX.md`](./docs/INDEX.md) · **DOC-3** [`docs/SEAL_CHAIN_POSTMORTEM.md`](./docs/SEAL_CHAIN_POSTMORTEM.md). Post-seal math lives in [`docs/VESPER_MATH_ADDENDUM.md`](./docs/VESPER_MATH_ADDENDUM.md) — a companion doc, never inlined into the sealed MATH file, so `git diff phase1-prereg-v3` stays empty modulo branding (re-verified post-merge: 0 differing lines on all three sealed docs). **Still queued for a compute window: RES-6 (η-paid injection; needs MAST) + a small TLS-epoch re-run.** Authorities: `docs/decisions/DR-003_E2_REMEASUREMENT.md` · `research/m4_evaluation/M4_ERRATUM_2026-07-19.md` (§5/§7 now filled) · `data/manifests/m4/e2_retiming/e2_retiming_summary.json` · `docs/audits/PROJECT_AUDIT_2026-07-19.md`. Execution plan: `docs/ROADMAP_TO_10.md` (Wave 0 + Wave-1 no-compute cluster done; Wave-1 compute tail + Waves 2–6 follow). **Phase II re-scoped** (bound/benchmark/monotransit; Kepler routing-scaling superseded): `docs/VESPER_PHASE2_PROGRAM.md` (DRAFT, pending DR-004; hard-gated behind the roadmap). This bullet is authoritative and supersedes every verdict line above it.
- **INN-3 POST-SEAL ANALYSIS (2026-08-17, branch `phase1/inn3-fap-acceleration`, local): the period-FAP entry tax IS removable — exactly. The sealed verdict above is UNCHANGED.** DR-002/Lever-1b recorded the B=1000 block-bootstrap period-FAP (ρ_d = 11.6%) as "**not** a removable artifact" after E-EVT and E-LUT each failed the equivalence gate 3/3. That is right about the *estimator* and wrong about its *cost*: both candidates tried to approximate the null distribution, and the tax was never in the distribution. Two levers, neither statistical. **(A) Exact vectorization** — 49% of the FAP's cost is `np.median(np.diff(np.sort(t)))` (`detector.py:26,55`), a loop invariant recomputed twice per duration per surrogate (**10,000 full sorts of an N-vector per star**) while the bootstrap resamples the *flux*, not the epochs; hoisting it + vectorizing the local-max scan, the bucketed dedup and the (n_f×k) comb scan gives **6.31× at bit-identical output**. **(B) Exact curtailment** — the sealed gate (g_e+1)/1001 ≤ 0.01 is *exactly* `g_e ≤ 9`, and g_e is monotone, so the **10th exceedance decides the gate**; stopping there is curtailed sampling (decision identical with probability 1, no error to bound) and is one-sided, so it can never clip a planet. Combined **73.2× on nulls, 12.7× on injections**. **Equivalence measured: 1126/1126 calibration nulls reproduce the sealed exceedance count (max |Δ| = 0); 149/149 calibration injections bitwise; all three Lever-1b criteria met with exact zeros.** **E2 counterfactual** (arithmetic on `timing_ledger_full.csv` + the sealed `recovery.csv`; **no TEST light curve re-read**, P-5 intact): reduction **27.3% → 38.0%**, ρ_d **11.6% → 0.85%**, **π\* 0.489 → 0.036** (≈16× → ≈1.2× of π≈0.03), P(ratio≤0.70) **0.27 → 0.96**. **⚠️ The frozen-rule decision stays INCONCLUSIVE, and that is the second finding: with the routing cost set to exactly zero the host-clustered CI is still [0.522, 0.703].** E2's INCONCLUSIVE is a **variance** result — between-host variance at H=39 clusters — not a cost result. The two causes are separable and both were necessary: the entry tax put the point estimate out of reach at *any* host count (as-recorded numbers stay INCONCLUSIVE even at H=100), and the erratum §2.1 parity bug (40 of 80 hosts drawn, 39 in the E2 subset) made the interval too wide at *any* cost; **remove both and E2 PASSES at H=79 — the count `m4_driver` was written to use** (hosts needed: 49 lever A+B · 65 lever A · 41 free-detector · never as-recorded). This promotes §2.1 from an E1 diversity concern to a causal contributor to the undecided compute verdict. **Side finding:** `m4_driver.py:117` sets `t14 = median(duration_grid)` but **line 120 overwrites it** with the seeded event's duration before the FAP call on line 126 (`e2_retiming.py:67` replicates it; `m3_calibrate` genuinely uses 0.2 d) — so **M4 duration-matched T₁₄**, RES-4's "counterfactual" strata are the realized ones for the M4 arm, and the M4-realized flip exposure is ≈**1.4%** vs the 0.09% RES-4 reports (~16×). RES-4's conclusion survives; its stated mechanism does not. **Parity bound:** Arm A's TLS is numba-compiled and Arm B was interpreted numpy; a numba port of the surrogate loop reproduces g_e exactly and is only **1.4–1.7×** faster than the vectorized numpy, so ≲2× of the routing cost is language. Authorities: [`research/m4_evaluation/INN3_FAP_ACCELERATION.md`](./research/m4_evaluation/INN3_FAP_ACCELERATION.md) · [`docs/VESPER_MATH_ADDENDUM.md`](./docs/VESPER_MATH_ADDENDUM.md) §E · artifacts `data/manifests/m4/inn3/` · code `research/m4_evaluation/{fast_period_fap,inn3_fap_acceleration,nb_period_fap}.py` · `tests/test_inn3_fap_acceleration.py`. **Nothing sealed touched** (no doc, threshold, weight, manifest or tag; `frozen_rerun/` untouched). Roadmap **INN-3** (Wave 6) delivered ~5 waves early with its proof obligations discharged. **Owner decisions open:** adopt as estimator-of-record (needs DR-006+; DR-004 reserved for the Phase-II gate, DR-005 for the scope decision) · paper placement of the counterfactual + two-cause diagnosis · whether §7.1 warrants a RES-4 addendum.
- **MATHEMATICAL AUDIT (2026-08-27, same local branch): the routing ceiling — a closed-form bound on evidence-first period recovery. Sealed verdict UNCHANGED (E1 PASS · E2 INCONCLUSIVE).** Calibration only; **no TEST read (P-5 intact)**; sealed docs verified **0 differing lines** vs `phase1-prereg-v3` (branding-normalised), Seal #2 SHA-256 matches DR-001 §5a, `frozen_rerun/` clean, sealed exceedance counts reproduced **bit-identically 1,126/1,126**. Method: record the **full** block-bootstrap surrogate table once — per-surrogate (k_b, R_b, span, n_freq) for 1,236 nulls × 1,000 surrogates + 669 routed injections — then every candidate statistic's FAP is post-hoc. **Result:** routing requires an evidence budget **W ≡ k·R̂² ≥ ln(N_eff/α)**, and **W ≤ N_tr/(1+ρ_FP)**, hence **P ≲ T_base/ln(N_eff/α)**. Every tunable (α, p_min, p_max, detector, noise model, confirmer) enters **logarithmically**; only the transit count enters linearly. Validated three ways — zero-free-parameter prediction of the sealed gate on 1,233 nulls at **precision 87.5% / recall 75.7%** (TP 28/FP 4/FN 9/TN 1192); **out-of-sample baseline scaling** (predicted P_max 2.94 d 1-sector / 5.80 d 2-sector, measured P50 **2.51 / 5.00 d**; ratio predicted 1.97, measured **1.99**; at P=4 d, 8.3% routing on 1-sector vs 63.6% on 2-sector, same planets same pipeline); and mechanism (at P≥8 d the gate opens for **20% / 0%** of *correct* seeds). **Falsification attempt failed:** sweeping T_β = R̂·k^β at matched null FAR gains at most **+1.49 pp** and the *exactly pivotal* statistic **loses 10.31 pp** — the multiplicity dependence is the evidence, not a defect; the ceiling is a property of the null geometry. **Corollary (subset region):** fast-path eligibility ⇒ SNR_tot ≳ z⋆√W⋆ ≈ 10.2 vs sealed T = 10.74; measured **17/17** fast-path recoveries also found by full TLS, **0** fast-path-only (excluding the known P=0.5 d edge artifact) — E1's PASS was structurally guaranteed and this is *why*; the fast path cannot add coverage for periodic signals, only compute. **Roadmap MATH-4 closed:** Λ's null is not χ²₁ — q99 = 120.4 vs 6.63 (18×), Pr(Λ≥25) = 1.81% vs 2.9e-7 (6.3×10⁴), Pr(Λ≥100) = 0.54% vs 7.6e-24; over-dispersion scales with seeded duration; a binding photometric gate would need **T_red ≈ 4,340**; `confirmer.py:171`'s hard-coded "~5σ" Λ≥25 is really **≈2.1σ**; at T_red=0 the gate reduces algebraically to a **circular sign test** (Pr(δ̂>0) = **0.859** at the seed vs **0.444** at random — the seed *is* the deepest event; Pr(confirm|null) = **66.8%**) — the MATH §10.3 circularity relocated to the confirmer. **Roadmap MATH-3 closed and its assumed direction REVERSED:** the bootstrap null is built from the series containing the signal; 128 paired runs on identical RNG streams give median FAP **0.0569** (sealed) vs **0.1578** (signal-free), Wilcoxon p=1.5e-4, gate open **53 vs 24** — **79% of fast-path routings exist only because the null is contaminated by the signal it tests**. FAR control is unaffected (nulls carry no signal) but **f_p — hence E2 — is inflated**. **Corrections of record:** MATH §4b's contamination fragility is **linear** (E[R̂]=1/(1+ρ_FP), verified to 3 dp), not quadratic — that law belongs to the pairwise-difference formulation, which is not what the code implements · **MATH §9's "identical grid" premise is false in code** (96.9% of surrogates use a different trial-frequency count) **and the deviation is load-bearing** — implementing the specification as written takes null FAR **2.99% → 4.37%** with 23 gate flips, **18 of them k=2 stars with R̂ = 1.000000**; the unstated deviation is what keeps N_min=2 survivable, and look-elsewhere absorption needs the same *map*, not the same *grid* · **Seal #2's N_min = 2 is inoperative** — q99(R̂|k) = 1.0000 exactly at k≤3 and **0 of 128** candidates with k≤2 ever routed (1 of 233 at k≤3, for a reason unrelated to coherence); effective floor k≈4–5 · **the conditioned residuals are red on transit timescales** — κ(T₁₄) median 1.17→1.48, p90 to **9.0**, 32–49% of stars above 1.5 — while the sealed detector docstring certifies "near-white" from acf₁≈0.01 (median 0.018 but **p90 0.649**; corr(acf₁,κ)=0.593): **lag-1 ACF is not a whiteness test on transit timescales**. The detector survives it (self-calibrated MAD normalisation absorbs κ); the confirmer does not (parametric Matérn fitted from lag-1). **Confirmed:** M3's null cleaning was load-bearing (FAP tail **1.06×** nominal on the cleaned pool vs **6.45×** on the excluded EB/variable pool), but the FAP is **not a uniform p-value** even cleaned (KS p=2.5e-9) — **the α=0.01 calibration does not extrapolate to any other α**. **Verdict on novelty:** the defensible novel content is the negative result itself — derived, zero-parameter-validated, confirmed out of sample in its scaling, surviving falsification, and general to any detect-then-test-periodicity pipeline. Authorities: [`research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md`](./research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md) · artifacts `data/manifests/math_audit/` · code `research/math_audit/`. **Owner decisions open:** does the ceiling become the paper's central result · re-measure f_p against a signal-free null before quoting it · fold §N-1/§N-2 into the MATH addendum as §F/§G. **The 2026-07-28 scope decision remains first in line.**
- **IDENTITY (2026-06-30): project rebranded `TRINETRA-X` → `VESPER` and shipped as the first public release `v1.0.0` — branding only; no algorithm, methodology, equation, threshold, result, or figure changed.** Acronym: *Validation Engine for Stellar Photometric Evidence and Recovery*. Folder `~/Desktop/VESPER`; repo `github.com/Ansul-S/VESPER`. ⚠️ Rebranding the sealed docs/manifests **changed their recorded SHA-256 digests by the rename only** — provenance in [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md) §5a; original sealed bytes remain intact at tags `phase1-prereg-v2/v3`. A `shasum` against the *old* recorded hashes will mismatch — read §5a first.
- **Phase I COMPLETE / SEALED / FINAL** (M0–M7). Phase II is gated solely by the `docs/ROADMAP_TO_10.md` completion gate + DR-004 (see the audit-remediation bullet above).
- **REPO REORGANIZED (2026-06-30, structure-only; history preserved):** Phase-I planning docs → [`research/phase1/`](./research/phase1/); session handoffs → [`archive/session_handoffs/`](./archive/session_handoffs/); `NEXT_SESSION_PROMPT.md` untracked + gitignored (local AI-workflow scratch). Root holds only `README.md · CLAUDE.md · VESPER.md · references.bib · .gitignore`. No source code or research content changed.
- **⚠️ OPEN DECISION carried from 2026-07-28 — project scope + paper framing (NOT decided; settle before resuming task work).** Recommendation on the table: finish Phase I in ~2 weeks (RES-6 → paper → submit) rather than the roadmap's ~50 days; **cut Waves 3 and 6** (package/CLI/container/API-docs/seal-library — none changes a number in the paper); do not start Phase II on momentum; and **reframe the paper around the methodology** — sealed single-shot validation with pre-committed verdicts, demonstrated by the protocol forcing withdrawal of this project's own headline verdict — with the routing result as the case study rather than the point (roadmap **INN-1**, currently scheduled last in Wave 6). **Until the owner rules, `docs/ROADMAP_TO_10.md` stands as written.** If accepted → record as **DR-005** (DR-004 stays reserved for the Phase-II gate) + amend the roadmap. Full text: [`archive/session_handoffs/SESSION_HANDOFF_2026-07-28.md`](./archive/session_handoffs/SESSION_HANDOFF_2026-07-28.md) §6.
- **Latest handoff:** [`archive/session_handoffs/SESSION_HANDOFF_2026-08-27.md`](./archive/session_handoffs/SESSION_HANDOFF_2026-08-27.md) (supersedes 2026-08-17; mathematical audit + the routing ceiling, same local branch `phase1/inn3-fap-acceleration`, uncommitted/unpushed). Prior: [`SESSION_HANDOFF_2026-08-17.md`](./archive/session_handoffs/SESSION_HANDOFF_2026-08-17.md) (INN-3), [`SESSION_HANDOFF_2026-07-28.md`](./archive/session_handoffs/SESSION_HANDOFF_2026-07-28.md). `main` == `origin/main` @ `77037d4`; release `v1.0.0` on the remote; Phase-I verdict corrected (E1 PASS · E2 INCONCLUSIVE); Wave 0, Wave-1 (less RES-6 + TLS-epoch re-run), half of Wave 2, and CODE-7/DOC-2/DOC-3 merged. **PR #22 open** (doc-only sync). GSD Core is globally installed but **not used** here (no local `.planning/`). Archive material is reference only; prefer repository documents over chat summaries.

## Conventions

- One claim → one table → one milestone → one frozen dataset. Keep figure/table indices stable.
- Convert relative dates to absolute. Cite the source document + section for any non-obvious claim.
- Do not modify `archive/` contents; they are historical record.
