# VESPER — Full Technical Audit (2026-07-19, second pass)

| Field | Value |
|---|---|
| **Scope** | Entire repository: code, docs, research notes, experiments, manifests, git history (86 commits, 2026-06-15 → 2026-07-19) |
| **Stance** | Adversarial peer review (top-tier venue standard). Every claim checked against repository evidence; no reliance on chat history. |
| **Relationship to the morning audit** | The 2026-07-19 morning audit's findings are recorded in [`M4_ERRATUM_2026-07-19.md`](../../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) and [`DR-003`](../decisions/DR-003_E2_REMEASUREMENT.md). This pass **independently re-verified** those findings from the artifacts and code, and adds **new findings** (marked **NEW**) — most materially on the occurrence weighting, the epoch mechanics, and the edge-control result obtained today. |
| **Remediation state at audit time** | Branch `phase1/audit-remediation`: DR-003 + M4 addendum committed; erratum drafted (§5/§7 pending); edge control **done**; E2 re-timing **paused at 26/300** by owner instruction. |

---

## 1. Executive Summary

**Current state.** Phase I (scientific validation of evidence-first routing on TESS) executed end-to-end under a genuinely sealed pre-registration: M0 manifest (22,723 targets, leakage-safe split), M1 conditioning, M2 injection + η gate, M3 threshold calibration (Seal #2), v3 re-registration (Seal #2b), one irreversible TEST read (15,000 injections, 2026-06-24), M5/M6 supporting studies, a paper draft, and a submitted hackathon package. The morning audit found the sealed run deviated from its own frozen protocol in specific, disclosed ways; remediation is mid-flight.

**Completeness.** The *recall* half of the Phase-I question is answered and robust. The *compute* half — the headline of the recorded verdict — is currently **unanswered**: the sealed "E2 FAIL" rested on a 12-star × 1-repeat timing with a bootstrap ratio CI of [0.42, 1.14], and its protocol-compliant re-measurement is 26/300 tasks in.

**Biggest accomplishments.**
1. A real, hash-sealed, single-shot pre-registered experiment — with the anti-tuning discipline actually enforced in code (`seal_loader.assert_split_allowed`, fail-closed hash checks) rather than just promised in prose.
2. A clean, well-characterized negative-leaning result the project did not flinch from (E1 pass / compute claim in doubt), plus an audit-and-erratum culture almost never seen at this scale of project.
3. E1 recall non-inferiority that survives three interval constructions including a host-cluster bootstrap (−0.82 pp vs −2 pp margin; `e1_corrected_inference.json`).

**Biggest blockers.**
1. **The headline verdict is not currently supported by evidence.** "H1 FALSIFIED — compute branch" is withdrawn in the addendum; its replacement awaits the frozen-rule E2 re-measurement (~19 h of compute remaining).
2. **What E1 demonstrates is narrower than the paper's framing (partially corrected today):** 30.3% of the estimand's weight sits in cells where both arms recover nothing; 78.9% of injections took the fallback where `rec_comb ≡ rec_tls` by construction; and (**NEW**, §3.6 below) the P=0.5 d "gain region" and 80% of the losses are *epoch-predicate* phenomena, not detection-power differences.
3. Absolute completeness numbers are optimistic (residual-space injection; η paid by neither arm) and host diversity was half of what was documented (40, not 80).

---

## 2. Architecture Review

**System (as realized in Phase I).** Two arms over conditioned TESS residuals (wotan biweight, 2.5 d window):
- **Arm A:** full-grid TLS; recovered iff SDE ≥ T=10.74 + period/epoch match.
- **Arm B:** box matched-filter detector (`frozen_rerun/detector.py`) → route if ≥N_min=2 events → period-from-spacing via circular-resultant comb (`period_recovery.best_period`) → B=1000 circular-block-bootstrap period-FAP gate (α=1%) → GP likelihood-ratio confirmer at the seeded ephemeris (`confirmer.py`, T_red=0, sign + odd/even + secondary vetoes) → confirmed = cheap recovery; otherwise full-TLS fallback (= Arm A).

**Strengths.**
- The **fallback-suppression design** makes recall loss attributable to exactly one mechanism (cheap-confirm suppressing a fallback that would have succeeded) — and the instrumentation (`decision_path`, `outcome_vs_armA` in `m4_driver._recover_worker`) captures it per injection.
- **Fail-closed seals as code**: `load_frozen()` refuses to run on any manifest drift; the TEST split needs an explicit token. This is the strongest part of the engineering.
- The `frozen_rerun/` snapshot pattern gives byte-level provenance for re-analysis of the sealed run.
- Crash-robust incremental ledgers (`recovery_partial.csv`, append-as-you-go) — proven valuable twice this week.

**Weaknesses / debt.**
- **Deliberate duplication with drift risk:** `e2_retiming._route_seed_sealed` re-implements `m4_driver._route_and_seed`; `edge_control._run_tls` duplicates `arms._run_tls`; M3 has its own `detector.py`/`period_recovery.py` copies. Each copy is justified (sealed fidelity) but nothing *tests* that the copies agree.
- **No package structure**: everything is `sys.path.insert` chains (`e2_retiming.py:33-35` inserts three paths, order-sensitive — frozen must shadow live). One wrong ordering silently swaps sealed for live code; nothing asserts which module won.
- Path-literal coupling: `CACHE = Path("data/processed/m1")` etc. hardcoded in six files; scripts only run from repo root.
- The empty `src/` scaffold was removed in remediation (correct call); `hackathon/` (29 MB) is a self-contained fork of ideas that shares no code with the sealed pipeline — fine, but it doubles the surface a reader must understand.

**Recommendation.** Do not "productionize" — Phase I is done. The one architectural investment worth making before Phase II: a tiny installed package (`vesper_core`) holding the *single* implementation of detector/period/confirmer with the frozen snapshot imported as data-versioned modules, plus an equivalence test pinning frozen-vs-live behavior on a fixture light curve.

---

## 3. Scientific & Mathematical Audit (highest priority)

Verified line-by-line this pass. Items marked ✓ are correct as implemented; ✗ are defects; ⚠ are disclosed approximations or framing risks.

### 3.1 Transit physics and injection — ✓ with disclosed deviations
- `m2_pipeline._geometry`: a/R★ from stellar density $(g P^2 / 4\pi^2 R_\star)^{1/3}$ — **correct** (Kepler's third law with $M=gR_\star^2/G$). T₁₄ $= (P/\pi)\arcsin[\sqrt{(1+k)^2-b^2}/(a/R_\star \sin i)]$ — **correct** (Winn 2010 eq. 14). Depth $=k^2$ with LD handled by batman — correct.
- ⚠ Sealed TEST injections used `cached_residual` mode (linear addition of the transit to the *conditioned* residual): the M2-measured detrending attenuation η is paid by **neither** arm. Paired ΔR unaffected; absolute recall optimistic. Disclosed (erratum §2.3).
- ⚠ Constant LD (u₁=0.4, u₂=0.30) vs confirmer template u₂=0.25 — a real inconsistency, negligible effect; fixed for future runs.
- ✗ `injection.n_transits = ⌊baseline/P⌋+1` ignores gaps and epoch: 892 of 15,000 injections (5.9%, concentrated at P=16 d) presented ≤1 *observed* transit while counted as ≥2 (erratum §4). Both arms faced identical injections, so paired ΔR stands; "the grid contains no monotransits" does not, except at formula level.

### 3.2 Detector — ✓ mechanics, ✗ two structural issues, ⚠ one overclaim
- The box filter normalizes the depth series by its own duration-timescale MAD scatter — a sensible, self-calibrated CDPP normalization. ⚠ The sealed docstring's claim that this "is exactly … the GP-whitened matched filter" is an overclaim (it is a white-ish approximation justified post-hoc by M1's acf₁≈0.01); corrected in the live module.
- ✗ **Gap-naive windows (sealed version):** `_box_depth_series` uses index-space cumsum windows and epoch `t[i] + 0.5·width`, so any window spanning a data gap averages non-contiguous flux and reports a mis-centred epoch. Fixed in the live detector (gap-aware segmentation, regression-tested); the sealed run used the gap-naive version.
- ✗→**NEW quantification of the epoch pathway:** event epochs are quantized to `stride = 0.5·duration` (`detect_events` strides the trial grid), so seed epochs carry ~±0.25·T₁₄ granularity *before* any noise; combined with gap-induced mis-centring this is the mechanistic origin of the dominant loss mode (80% of the 869 losses are right-period/wrong-epoch) — and of the gains (§3.6). The local-maximum scan also excludes the first/last trial epoch (`range(1, n-1)`), blinding the detector to edge events; minor at S1–S3 baselines.

### 3.3 Period recovery + FAP — ✓ statistically sound design, ⚠ two caveats
- The comb statistic (1 − circular resultant R̄ of event phases) is a legitimate phase-concentration measure; the max-over-grid selection effect is handled **correctly** because the null distribution is built from the same max-over-grid statistic on surrogates (`period_fap` compares best-R to surrogate best-R). Laplace smoothing (g+1)/(B+1) — correct; min attainable FAP 1/1001 ≈ 0.001 < α=0.01, so the gate is decidable. ✓
- ⚠ With exactly N_min=2 events, every P = spacing/m has R̄=1 (perfect degeneracy); `best_period`'s argmin then returns the longest such period. The FAP is honest about this (surrogates share the degeneracy), but routing on 2 events means the *period estimate itself* is weakly identified — consistent with the 20% wrong-period loss mode.
- ⚠ Circular block bootstrap with L_b = 3·max(τ_GP, T₁₄): with the sealed run's flat τ=0.005 d, L_b is set by T₁₄ (~0.1–0.3 d) — masking the τ error (erratum §2.4) but leaving surrogate redness under-modeled for stars with genuine τ > T₁₄/3. Direction: anti-conservative FAP for red stars. Second-order; the M3 null calibration (measured exceedance at α) bounds the practical effect.

### 3.4 Confirmer (GP likelihood ratio) — ✓ core statistic, ⚠ three approximations, ✗ one weak veto
- Λ = δ̂²·(mᵀK⁻¹m) with δ̂ = (mᵀK⁻¹y)/(mᵀK⁻¹m) is the correct GLS/Wald statistic (χ²₁ under H₀ with known K). ✓ Sign-aware zeroing for δ̂≤0 is a legitimate one-sided test.
- ⚠ K is *estimated from the same series* (out-of-transit MAD + lag-1 ACF → Matérn-3/2): Λ's null is only asymptotically χ²₁. In practice irrelevant — T_red was calibrated **empirically** on nulls, and calibrated to 0.
- ⚠ Template shape from the *detector's* seed duration (biased ~31% short per M6) with a/R★ = P/(π·T₁₄) (small-angle, central-transit approximation): template mismatch → the measured ~20%-low depth bias (M6 `depth_recovery`). Self-consistent, disclosed, but it means the "physics confirmation" is run against a knowingly distorted template.
- ✗ `odd_even_consistent` uses white-noise SEM (`std/√n`) on correlated residuals — anticonservative error bars for the 3σ consistency test. Bidirectionally weak: M6 measured only 50% EB rejection at the confirmer (8 reached it, 4 rejected by shape, 0 by sign) → ~25% of known EBs pass end-to-end. The vetting is partial and its error model is wrong; both facts are now disclosed, neither is fixed.
- **⚠ Charter inversion (confirmed):** with T_red=0 the Λ threshold does no work; binding FP control is the *period-FAP timing gate* (M6 ablation: removing it takes null FP 0.0%→12.3%; removing shape/sign costs nothing on clean nulls). The prime directive "photometric significance, not timing coincidence, decides" is **not realized** by the sealed operating point. Now stated in the paper; must never be walked back.

### 3.5 E1 estimand, weighting, and inference
- Point estimate $\bar{\Delta R} = \sum_c w_c (R_{B,c} - R_{A,c})$ and the paired within-cell bootstrap are implemented correctly (`endpoints.e1_recall`; paired resample uses the same index vector for both arms ✓). The missing-weight guard (raise, don't zero-weight) is a good remediation fix.
- ✗ (found this morning, re-verified): the injection-level CI ignores that 15,000 injections share **40** host noise realizations; the host-cluster bootstrap widens lo95 from −0.60 pp to −0.82 pp. Still passes. Wilson-style combination (the method the sealed HYP actually named) agrees (−0.60 pp). E1 is robust *as an estimand*.
- **NEW — the "occurrence weight" is only half occurrence.** `occurrence_weights.py` builds $w_c = w_P \cdot w_R$ with $w_R$ from Kunimoto & Matthews (2020) radius occurrence but $w_P$ **log-uniform by fiat** (1/6 per period node). KM's own broken power law (df/dlogP ∝ P^1.9 below P₀) puts *vanishing* occurrence at P=0.5 d — a node that is **entirely below KM's 0.78 d support** (acknowledged in the π̂ integration note, `m3_occurrence_weights.json`, but not propagated to w_c). Consequence: the cell family where Arm B books nearly all its gains (P=0.5 d, +19 pp) receives ~17% of total weight that a KM-consistent period prior would strip to ≈0, while Arm B's loss cells (P=2–8 d, large Rp) are radius-down-weighted. The sealed ΔR̄=−0.48 pp therefore **benefits from a weighting choice that is not occurrence-derived in the period dimension**. This was pre-registered (legal under NN#2) — but the paper calls the estimand "occurrence-weighted," which overstates it. **Required:** a sensitivity row reporting ΔR̄ under a KM-period-weighted w_P. Direction of the correction is *against* Arm B; given near-parity at Rp≤2 (−0.37 pp), E1 would most likely still pass — but that must be computed, not asserted.
- ⚠ Cluster bootstrap on 40 clusters with a raw 5th percentile: with so few clusters, percentile intervals are rough (no BCa/studentization). Acceptable, worth a footnote.

### 3.6 The gain/loss mechanism — **NEW result (today's edge control)**
99.6% of Arm B's 563 gains sit at P=0.5 d = the TLS grid's `period_min`. The paired control (`edge_control.py`, 60 injections/condition, Rp=8, calibration nulls) rules the grid edge **out**: extending the grid to p_min=0.3 changes nothing, per-row bit-identically. Instead, **TLS at P=0.5 d finds the right period at high SDE (period_ok 98%, SDE_ok 97%) and fails the recovery predicate on epoch** — 36/38 failures epoch-only — while P=0.62 d recovers 98%. So the sealed interpretation ("SDE just below T") is wrong; the gains are the mirror of the losses: **both arms' headline asymmetries at short period are ±0.5 T₁₄ epoch-predicate phenomena, not detection power.** This materially reframes §3.1–3.2 of the paper (now corrected in the draft) and further narrows what E1 says about the cheap path.

### 3.7 E2 compute claim — ✗ as sealed; re-measurement pending
- Sealed measurement: 12 stars × 1 wall-clock repeat, against a frozen rule specifying ≥10/cell, cap 300, ≥5 warm repeats, CPU-core-seconds. Bootstrap over the sealed ledger: ratio CI [0.42, 1.14], P(reduction ≥30%) ≈ 0.37 → **statistically undecided**; VAL §5's own INCONCLUSIVE branch should have fired but the sealed tooling computed no interval at all. The recorded FAIL is withdrawn (DR-003, addendum) — verified correct this pass.
- The re-timing tooling is sound: reconstruction validated bit-exactly against the sealed run (identical host multisets per cell, routed fraction equal to 7 s.f.); ledger columns match `e2_compute`; decision taken on a host-clustered CI. Paused at 26/300 (owner instruction); interim ratio ~0.94–1.01 — consistent with FAIL or INCONCLUSIVE, **not** with PASS, but 26 rows decide nothing.
- **NEW — π\* formula inconsistency (minor):** MATH §8.3a boxes $\pi^\star = \rho_d/f_p$; `endpoints.py` implements $\rho_d/(f_p(1-\rho))$; the exact zero of §8.3a's own survey expression is $\rho_d/(f_p(1-\rho+\rho_d))$. Numerically all ≈0.68 here (the erratum's headline "3× worse than the reported 0.236" is unaffected), but docs and code should state the same formula.
- The corrected π\*≈0.68 ≫ TESS-realistic π ≈ 0.03 confirms — more starkly than the sealed text did — that survey-scale saving is impossible in this architecture without a clean-skip tier.

### 3.8 Threshold calibration (M3) — ✓ sound, with honest reporting
z⋆ from a mean-false-events sweep, T as the null 99th-percentile SDE (FAR 1%/star), α_FAP checked against measured null exceedance, null pool cleaned of EBs/variables (854/1000) with the M0 null definition preserved. Correct constructions throughout. ⚠ T=10.74 from ~850 nulls has 99th-percentile sampling error of a few tenths; both arms share T, so E1 pairing absorbs it.

### 3.9 Not present / correctly absent
BLS (wording hygiene only, F9), Hough transform (concept-era; not in Phase I), habitability (correctly deferred), precision/F1 (recall-first by design; FP control via calibrated FAR instead — legitimate but the paper should say explicitly that precision was not an endpoint).

---

## 4. Experimental Audit

| Experiment | Valid? | Notes |
|---|---|---|
| M0 manifest/split | ✓ | Leakage-safe by sky region; sealed; release asset for the table. |
| M1 conditioning + noise | ✓ | η-sample 188; window superseded 0.5→2.5 d with the 0.5 d artifacts preserved. |
| M2 injection/η gate | ✓ | Rp=1 exclusion (noise-limited) pre-registered and documented. |
| M3 calibration | ✓ | Including the EB/variable null-pool cleaning episode — done properly, on calibration only. |
| M4 E1 | ✓ robust | With the §3.5–3.6 framing constraints; host count 40 not 80. |
| M4 E2 | ✗ invalid as sealed | Undecided at n=12×1; re-measurement in flight (26/300). |
| M5 recovery calibration | ✓ | Supporting. |
| M6 reality check | ✓ and under-used | TOI recall 26/30 both arms; EB leakage ~25%; the ablation that exposes the FAP gate as the real arbiter is one of the most informative artifacts in the repo. |
| Edge control (today) | ✓ | Paired design, off-node control, calibration-only. Should be promoted into the paper's supplement. |

**Missing:** (1) the KM-period-weight sensitivity for E1 (§3.5 — the single most important missing analysis); (2) an epoch-tolerance sensitivity (recovery predicate at ±0.75/±1.0 T₁₄ — since both gains and losses live at the predicate boundary, ΔR̄'s stability under the tolerance choice is unknown); (3) any deliberate monotransit campaign (deferred, correctly); (4) per-star τ_GP re-run of the FAP gate (future-runs fix exists; effect on the sealed result argued-away, not measured).

**Conclusions currently overstated anywhere they appear without the erratum:** "over 80 test hosts" (T1 fixed in working tree), "grid contains zero monotransits," "confirmer recovers planets whose SDE fell just below T" (fixed today), and every citation of the 24.4%/0.756 E2 point estimate as decision-grade.

---

## 5. Code Quality Review

**Good:** small, single-purpose modules with unusually complete docstring provenance (each file states its sealed authority and what deviates); incremental ledgers; deterministic seeding everywhere; fail-closed guards; 11 regression tests now pin the audit's code fixes (parity bug, gap-aware windows, e2 decision logic, π\* definition); CI (`tests.yml`).

**Debt, ranked:**
1. **Duplicated sealed/live implementations with no equivalence tests** (highest risk of silent scientific drift — §2).
2. **`sys.path` shadowing as the frozen/live switch** — one import-order mistake re-runs "sealed" analyses on live code with no error.
3. **Test coverage is thin where the math lives:** zero tests for `confirmer.py` (GLS, vetoes), `period_recovery.py` (comb statistic, FAP), `injection` geometry, M1–M3 pipelines.
4. Hardcoded repo-root-relative paths in six entry points.
5. Config sprawl: thresholds live in the sealed JSON, but grids/strides also appear as literals (`stride_frac=0.5`, dedup `0.3` d, secondary Λ≥25, `k_sigma=3.0`) — none calibrated, none centralized.
6. Minor: `edge_control` A/B share injections but recompute them per job (wasted CPU); `e1_recall` cluster bootstrap re-concatenates DataFrames per replicate (slow at B=2000); both fine at current scale.

---

## 6. Project Timeline Assessment

- **2026-06-15/16 (35 commits):** charter → gap analysis (12 findings) → remediation → **pre-registration v2 sealed** → M0–M3 executed with two mid-flight corrections done right (detrend window 0.5→2.5 d before sealing thresholds; null-pool EB cleaning before Seal #2).
- **2026-06-19:** **Finding B** — targeted-TLS Arm B proven internally inconsistent (SDE is grid-normalized) → v3 re-registration, confirmer-only, keystone relaxed to common-FAR; Lever-1b cheap FAP **dropped** because both candidates failed the pre-registered equivalence gate. A failed idea handled exactly as the protocol demanded.
- **2026-06-24:** single TEST read; verdict recorded.
- **2026-06-25/26:** M5/M6, tables, paper draft.
- **2026-06-29/30:** rebrand TRINETRA-X→VESPER + v1.0.0 release — which **silently broke every seal-verification loader for 19 days** (found and fixed in remediation; disclosed in `seal_loader.py` and F1 §5a).
- **2026-07-01:** hackathon submission (separate prototype).
- **2026-07-19:** independent audit → DR-003 remediation (this work).

**Lessons the history teaches:** pre-registration discipline held under pressure three times (window change, null cleaning, Finding B); the one process failure (rebrand) came from treating a *naming* change as risk-free while the integrity chain hashed names; and the sealed run's two real defects (host stride, E2 sample) were **execution** failures a dry-run checklist keyed to the frozen plan's numbers would have caught.

## 7. Successes

1. **Enforced pre-registration** — seals as code, one-shot TEST token, verified-empty diffs against the seal tag (re-verified this pass: 0 non-branding diff lines across all three sealed docs). This is rarer and more valuable than any positive result.
2. **A publishable negative result**: recall preserved, compute claim honestly in doubt, failure localized to a replaceable component (the B=1000 FAP entry tax, ρ_d≈14%).
3. **Correct hard calls under the freeze**: Finding B → v3; equivalence-gate discipline dropping Lever-1b; Rp=1 noise-limited exclusion.
4. **Instrumentation quality**: per-injection decision paths made the erratum's mechanism analyses (and today's edge control) possible without touching TEST.
5. **The audit-remediation loop itself**: erratum + DR-003 + append-only addendum + regression tests, with sealed artifacts untouched — a model for how to correct a sealed experiment.
6. M6's ablation: a genuine, pre-planned probe that exposed the system's real arbiter — and the project *kept* the unflattering answer.

## 8. Failures

1. **E2 executed off-protocol** (12×1 wall-clock vs frozen 300×5 CPU) → the recorded headline verdict was decision-grade in appearance only. *Recoverable*: re-measurement running.
2. **Host-assignment stride bug** — 40 of 80 hosts, undetected because nothing asserted host coverage. *Recovered*: fixed + tested; E1 re-inferred.
3. **Rebrand broke the seal chain silently for 19 days** — the fail-closed design worked (nothing could run) but nothing *ran* to notice. *Recovered*: dual-digest loaders with content verification.
4. **Charter inversion at the operating point** (T_red=0 → timing gate decides) — a design outcome, not a bug, but it contradicts the prime directive and was previously buried in a sub-document. *Not recoverable within v3*; must be a headline caveat.
5. **Targeted-TLS Arm B (v2)** — conceptually broken (grid-normalized SDE); caught pre-TEST. *Fully recovered* via v3.
6. **Epoch imprecision as the dominant loss/gain channel** — a foreseeable consequence of stride-quantized seeds + a tight ±0.5 T₁₄ predicate; the dress rehearsal saw it and the design still shipped without a confirmer epoch refit. *Recoverable in future work* (T₀ refinement is explicitly spec'd out of v3 by D-3i).

## 9. Risk Assessment (ranked)

1. **Scientific/publication — verdict in flux:** any current artifact quoting "H1 FALSIFIED (compute)" or 24.4%/0.756 as decision-grade is wrong until the re-measurement lands. Includes the public v1.0.0 release notes and the submitted hackathon deck (both predate DR-003). *Severity: high.*
2. **Scientific — E1 framing:** if a reviewer computes the KM-period-weighted ΔR̄ or an epoch-tolerance sensitivity and the pass degrades, the paper's primary claim wobbles post-publication. Run both *before* submission. *High.*
3. **Integrity — frozen/live drift:** `sys.path` shadowing + untested duplicates could silently corrupt any future re-analysis. *Medium-high.*
4. **Reproducibility — data availability:** 310 MB of caches are gitignored; an external reader can verify hashes but not re-run conditioning without MAST access and ~hours of compute; no archived environment beyond `requirements.txt`. *Medium.*
5. **Maintainability — bus factor 1**, research-script layout, no releases of intermediate artifacts beyond m0. *Medium.*
6. **Engineering — timing fidelity of the re-measurement** on a heterogeneous M4 (4P+6E cores): workers must stay ≤6 or E-core contamination biases CPU-seconds. Documented in the resume note. *Low-medium (managed).*

## 10. Missing Components

- **Research-grade (nearly there):** E2 re-measurement + erratum §5/§7; KM-period-weight and epoch-tolerance sensitivities; promotion of the edge control into the paper; a statement that precision was not an endpoint.
- **Publication-ready:** the above + affiliation/venue decision, figure regeneration from corrected tables (T1 done; F3/F8 captions still say 80 hosts), data/code availability statement with archived environment (e.g., zenodo DOI + lockfile), and reconciliation of the public release notes with DR-003.
- **Open-source-ready:** LICENSE/CI/tests exist (remediation); missing: CONTRIBUTING, environment lockfile, any packaging, coverage of the mathematical core.
- **Portfolio-ready:** effectively is one already; the erratum culture is the differentiator worth showcasing.
- **Production-ready:** not applicable and correctly not attempted (Phase I is a principle test; π\*≈0.68 says the current architecture should *not* be productized).

## 11. Prioritized Roadmap

**Critical (this week).**
1. Finish the E2 re-timing (≈19 h compute remaining); fill erratum §5/§7; propagate the verdict per DR-003 D3 (paper, CLAUDE.md, vault). *Impact: the project's headline claim becomes evidence-backed.*
2. E1 sensitivity analyses (KM-period w_P; epoch tolerance ±0.75/±1.0 T₁₄) on the existing `recovery.csv` — hours of work, no new data. *Impact: converts the E1 pass from "pre-registered estimand" to "robust conclusion."*
3. Reconcile public-facing artifacts (release notes; a hackathon-status note) with the withdrawn verdict. *Impact: closes the integrity gap between repo truth and public claims.*

**High.**
4. Frozen-vs-live equivalence test on a fixture LC; assert module identity after path shadowing. 5. Tests for confirmer/period_recovery math. 6. Regenerate figures/captions at 40 hosts.

**Medium.**
7. Package the core; centralize path/config literals. 8. Archive environment + data DOI. 9. Correct the odd/even SEM to a cluster-robust error (future runs).

**Nice-to-have.**
10. BCa/studentized cluster CI; 11. per-star τ_GP FAP sensitivity on calibration; 12. a short "how the seal chain broke and how it fails closed now" write-up (genuinely useful to the community).

## 12. Overall Assessment

| Dimension | Score | Basis |
|---|---|---|
| Engineering quality | 6.5 | Fail-closed guards + ledgers excellent; duplication, path-shadowing, thin tests. |
| Research quality | 7.5 | Process (pre-reg, seals, erratum) is top-decile; sealed-run execution errors cost it. |
| Mathematical rigor | 6.5 | Theory docs correct and honest; implementation-level statistics repeatedly wrong (CI clustering, E2 sample, SEM under correlation, w_P fiat) — though all found and disclosed by its own audit. |
| Software architecture | 6 | Right shape for a research program; not built for reuse; frozen/live risk. |
| Code quality | 6 | Readable, documented, seeded; low coverage where it matters most. |
| Documentation | 8.5 | Unusually complete and self-critical; sprawl is the only cost. |
| Innovation | 7 | Routing idea is incremental; the *validation methodology* (equivalence gates, pre-committed verdicts, sealed one-shot test) is the real contribution. |
| Reproducibility | 8 | Seeds/hashes/tags/bit-exact reconstruction; −2 for the 19-day broken chain and non-archived data/env. |
| Publication readiness | 5 | Draft is good; blocked on E2, sensitivities, figure regeneration. |
| Production readiness | 2 | Not a goal; the science says don't. |

**1. Exceptionally well:** epistemic discipline. The project catches its own errors, writes them down, and preserves the evidence — including three separate occasions (Finding B, Lever-1b, this audit) where the honest answer was the inconvenient one.

**2. Greatest weaknesses:** the gap between protocol and execution in the sealed run (E2, host bug); statistics done correctly on paper but wrong in code at exactly the decision-bearing points; and an E1 headline whose strength depends on weighting/predicate choices that were pre-registered but not stress-tested.

**3. Single most important issue:** finish the E2 re-measurement. Until erratum §5 is filled, the project's central public claim — the verdict of its only sealed experiment — is a withdrawn statement with no replacement.

**4. Technical lead's next month:** Week 1: complete E2 → erratum → verdict propagation → commit/tag the remediation; run both E1 sensitivity analyses. Week 2: public reconciliation (release notes, README, hackathon note); regenerate figures; frozen/live equivalence tests + confirmer/period tests. Week 3: finalize the paper (edge control into supplement, all caveats in the main text), archive environment + data DOI, external-reader dry run of the reproduction instructions. Week 4: decide the Phase-II question honestly — given π\*≈0.68, the defensible directions are (a) a provably-equivalent cheap FAP estimator, or (b) the clean-skip tier with an explicit recall budget; write that decision record *before* touching Kepler data, and keep the seal discipline that made Phase I credible.

---

*Audit completed 2026-07-19 (second pass, post-session-loss). All findings verified against repository artifacts; no chat-history claims relied upon. Sealed artifacts untouched.*
