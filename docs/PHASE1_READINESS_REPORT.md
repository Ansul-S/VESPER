# PHASE I READINESS REPORT — TRINETRA-X

| Field | Value |
|-------|-------|
| **Document** | Phase I scientific-readiness assessment |
| **Author role** | Principal Research Scientist (session handoff review) |
| **Scope** | All repository documents + Obsidian vault, as of the date below |
| **Date** | 2026-06-15 |
| **Verdict (summary)** | **NOT YET READY to read data.** Specification is scientifically strong; one human decision (F1) and a single re-registration (v2) stand between the project and milestone M0. |

> This report is an assessment, not a specification change. It does not alter any frozen parameter, does not write implementation code, and does not introduce new project goals. It evaluates whether Phase I can begin and what must happen first. Authority remains with the canonical documents in [`docs/`](.); where this report and a canonical document conflict, the canonical document governs.

---

## 1. Repository Understanding

**What TRINETRA-X is.** An evidence-first exoplanet-detection *research program* for TESS, currently in **Phase I — Scientific Validation**. The program is the reconstructed successor to an earlier project (TRINETRA, through "v3") that was fragmented across repositories and chats. This repository is now the canonical source of truth; the prior project is archival reference only ([`archive/`](../archive/)).

**The single scientific question.** *Can evidence-first routing reduce computational cost without sacrificing recall on TESS?* Everything in Phase I serves a falsifiable test of that claim and nothing more.

**The core idea.** A classical transit search asks *"is there a planet at period P?"* across thousands of trial periods per star. TRINETRA-X asks once: *"does this star show a dimming the noise cannot explain?"* — detects local transit-like events, infers the period from their spacing, confirms with a physics-based transit fit, and pays a full TLS search only on the minority of stars with no local evidence.

**The corrected lesson (the spine of the whole program).** v3's principle survived; its execution did not. v3 let **timing coherence** stand in for **photometric significance** and never calibrated its detection statistic against a null. TRINETRA-X repairs exactly that defect: *photometric significance — depth, shape, repetition — not timing coincidence — is the arbiter of detection*, and every significance statistic is calibrated ([`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md) §E–§F; [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) §10–§11).

**Document set, and how the documents relate.**

| Document | Role | Assessment |
|----------|------|------------|
| [`TRINETRA-X.md`](./TRINETRA-X.md) | Master charter (mission, philosophy, 7-stage vision, milestones) | Sound; describes the *full vision*, including learned/AI stages that are **out of Phase I scope**. |
| [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) | Formal H1/H0 + secondary H2–H6, assumptions A1–A6, success/failure criteria | Rigorous; non-inferiority framing is correct. Still v1 — must reissue v2 (F1, F2, F6). |
| [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) | Canonical theory (math only) | Strong. The master equation $\Delta R = -f(1-r_{\rm seed}g)$ reduces the entire claim to one testable inequality. Needs the two-regime cost model added (F1). |
| [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) | Pre-registered Phase I protocol | The operative pre-registration. Frozen 2026-06-14, **still v1**. Must become v2 (F1, F2, F6, F8). |
| [`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md) | 7-stage full-system design | Forward-looking (Phase II–IV); correctly flags a "minimum-viable core." Not load-bearing for Phase I pass/fail. |
| [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md) | Concept lineage / v3 post-mortem | Excellent diagnostic record; the source of the program's central correction. |
| [`REPOSITORY_GAP_ANALYSIS.md`](./REPOSITORY_GAP_ANALYSIS.md) | Adversarial internal referee (12 findings, F1–F12) | High quality; the right document to drive readiness. |
| [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) | Fix plan for the Critical + Must-fix subset (F1, F2, F6, F8) | Concrete and ready; F2/F6/F8 fixes are drop-in, F1 needs a decision. |
| [`PAPER_NOTES.md`](./PAPER_NOTES.md) | Publication notebook (venues, figures F1–F9, tables T1–T8, milestones M0–M7, reviewer rebuttals R1–R8) | Mature; pre-empts most reviewer attacks; PR-A (compute external validity) is the open one. |

**Internal consistency.** The document set is unusually well-cross-referenced and internally coherent. The fairness keystone (identical TLS engine + identical SDE threshold in both arms) is stated consistently everywhere and is the methodological centre of gravity. The non-negotiables in [`CLAUDE.md`](../CLAUDE.md) match the charter's rules and the validation protocol's anti-tuning safeguards.

**Repository hygiene (F12) — largely resolved since the gap analysis was written.**
- ✅ Root `TRINETRA-X.md` is now a pointer, not an empty duplicate.
- ✅ `README.md` populated (overview + doc map + read order + rendering note).
- ✅ `CLAUDE.md` populated (non-negotiables, doc map, "don't build prematurely," current phase).
- ✅ `.gitignore` is reproducibility-aware: tracks manifests + small frozen results, ignores bulk data (`*.fits`, `*.npz`, `*.h5`, `*.pkl`, …), caches, and `.DS_Store`.
- ⚠️ **Still open:** no `references.bib` (despite [`PAPER_NOTES.md`](./PAPER_NOTES.md) §11 listing the citation set); `archive/legacy/` empty; `src/ data/ research/ results/ notebooks/ papers/` are empty scaffolds (correct for this phase — no code by design).

---

## 2. Vault Understanding

**Structure** (`vault/`, an Obsidian vault):

```
00_Home/          Current_Mission.md, Dashboard.md          ← populated
01_Research_log/  Daily_Research_Log.md (empty template)
02_Mathematics/   (empty)
03_Literature/    (empty)
04_Experiments/   Failed_Ideas.md (v3 coherence metric — rejected)
05_Publication/   (empty)
99_Archive/       (empty)
```

**State.** The vault is correctly *scaffolded but mostly empty*, consistent with pre-implementation. The populated notes are faithful to the repository:
- `00_Home/Current_Mission.md` and `Dashboard.md` correctly state the phase, goal, blockers (F1/F2/F6/F8), and next milestone (M0).
- `04_Experiments/Failed_Ideas.md` records the v3 coherence-metric rejection and its lesson ("photometric significance must drive confirmation") — the right kind of durable memory.

**Role (per [`CLAUDE.md`](../CLAUDE.md)).** The vault is *long-term research memory and working notes*; the repository is *authoritative*. Vault notes are not specifications unless explicitly promoted into `docs/`. This separation is correct and should be preserved. See §9 for the recommended working protocol.

**Gap.** The vault does not yet carry: literature notes (`03_Literature`), the mathematical derivation notes that mirror the canonical theory (`02_Mathematics`), or per-milestone experiment logs (`04_Experiments`). These are not blockers, but they are where Phase I day-to-day memory should accumulate once M0 starts.

---

## 3. Current Project State

- **Phase:** I — Scientific Validation. **Stage:** pre-implementation (specification + pre-registration completion).
- **Code:** none, by design. The Phase I detector is deliberately *simple and untrained*, so a pass/fail is attributable to the routing *principle*, not to model quality.
- **Data:** none read. No sector data has been touched — this is what keeps the pre-registration completion legitimate rather than post-hoc tuning.
- **Pre-registration:** [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) frozen at **v1 (2026-06-14)**. Four findings (F1, F2, F6, F8) require edits that touch frozen parameters → **a v2 reissue is mandatory before M0**.
- **What is done:** concept reconstruction, architecture design, formal hypothesis, validation protocol, mathematical foundations, an adversarial gap analysis (12 findings), and a remediation plan for the critical subset.
- **What is not done:** the F1 scoping *decision*; application of the F2/F6/F8 edits; the v2 reissue and seal; then M0 (manifest + leakage-safe split).

**One-line state:** *The science is specified and stress-tested on paper; the experiment is one decision and one re-registration away from being allowed to start.*

---

## 4. Remaining Blockers

The four pre-registration blockers, in dependency order:

| Blocker | Type | Status | Gating? |
|---------|------|--------|:--:|
| **F1** — compute-measurement population | **Needs human decision** | Recommended fix specified; awaiting sign-off | **Yes — hard gate** |
| **F2** — operational recovery/recall predicate | Drop-in fix ready | Concrete predicate written, not applied | Yes |
| **F6** — primary estimand + multiplicity rule | Drop-in fix ready (one sub-choice: the weight prior) | Estimand specified, not applied | Yes |
| **F8** — thresholds + TLS baseline + runtime protocol | Protocol/targets ready; numeric values set later on calibration set | Structure specified, not applied | Yes (procedure); values sealed at M3 |

**Sequencing constraint (non-negotiable #2).** All four touch parameters the pre-registration exists to freeze. They are legitimate to resolve **now** *only because no data has been read*. The procedure is fixed: (1) sign off F1; (2) apply F1/F2/F6/F8 edits; (3) reissue `TRINETRA_X_PHASE1_VALIDATION.md` and `SCIENTIFIC_HYPOTHESIS.md` as **v2, dated 2026-06-15**; (4) seal; (5) only then read sector data. Reading data before step 4 forfeits the anti-tuning guarantee and would invalidate the headline result.

**Highest-priority next actions (in order):**
1. **Obtain the F1 scoping decision** (the only true bottleneck — see §5).
2. **Apply F2, F6, F8 edits** to the named documents (mechanical once F1 is decided; F6 needs the weight prior chosen).
3. **Reissue + seal v2** of the pre-registration and hypothesis; hash-record.
4. **Begin M0:** freeze the TESS sector/target manifest and the leakage-safe calibration/test split.

---

## 5. Assessment of F1, F2, F6, F8

### F1 — Compute-measurement population *(Critical; the decisive item)*

**The problem, restated.** The primary truth is injection into **real** light curves, so every test star carries a planet. The theory gives compute saving $\approx f$ (fast-path routing fraction). But on a real survey the **planetless majority** (~99%) shows no local evidence → routes to the full-TLS fallback → cost = detector + full TLS > baseline. On a survey-representative sample the prefilter is **net overhead**:

$$\frac{C_{\rm comb}}{C_{\rm full}} \approx (1+\rho_d) - \pi f_p(1-\rho+\rho_d)\;\Rightarrow\;\text{saving}\approx \pi f_p - \rho_d,$$

which for survey-realistic prevalence $\pi\sim10^{-2}$ is near zero or negative. As written, H1b's "≥30% *total* compute reduction" is attainable/measurable only on a planet-enriched population, and no document states that scoping. This is the reviewer's single most dangerous attack (PR-A).

**My scientific assessment.** This is correctly diagnosed and is the right thing to gate on. The recommended fix in [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) — **adopt all three of (a) scope the Phase I compute claim to the fast-path-eligible population, (b) add the two-regime cost model and report a survey-representative figure as a *secondary* endpoint at a pre-registered prevalence $\hat\pi$, (c) defer survey-scale saving to a Phase II clean-skip tier** — is the scientifically honest path. It converts an over-broad claim that fails external validity into a narrower claim that is provable in Phase I, while documenting the survey-scale limitation openly.

**Recommendation: adopt (a)+(b)+(c).** The alternative (implement the clean-skip tier now and fold its recall cost into H1a) expands scope, adds recall risk, and slows the program — reject it for Phase I.

**Two conditions I attach to the fix (to make it airtight):**
1. The detector overhead $\rho_d = C_{\rm det}/C_{\rm full}$ **must be measured and reported**, not assumed negligible — the scoped claim still requires $\pi f_p > \rho_d$ on the relevant population, and the survey-representative secondary figure is meaningless without it.
2. The survey-representative prevalence $\hat\pi$ must be **pre-registered with its source** (TESS occurrence rate × geometric transit probability), and the planetless light curves must be **real, known-TOI-removed** stars — so the secondary figure measures genuine overhead, not a modelling artifact.

**Why this is a human decision and not mine to seal.** (a)+(b)+(c) narrows the headline claim of the program. That is a scope choice with publication consequences (the paper's compute claim becomes "on fast-path-eligible stars," with survey-scale as a characterized limitation). It should be signed off explicitly and the decision recorded in the repository — not left implicit. **This is the one item I recommend escalating before any further edits.**

### F2 — Operational recovery/recall predicate *(Critical; fix ready)*

**Assessment.** The proposed predicate is sound and applies identically to both arms (preserving the fairness keystone): an injected planet is *recovered* iff (i) period within $|\hat P - P_{\rm true}|/P_{\rm true} < 0.01$ **or** a harmonic $\{P/m, mP\},\,m\in\{2,3\}$ within the same tolerance (harmonics counted but **flagged and reported separately**); (ii) epoch aligns within $\pm 0.5\,T_{14}$; (iii) TLS SDE $\ge T$ (the F8 common threshold). This is reproducible, defensible, and the *single most important reproducibility fix* — without it no recall number means anything. **Ready to apply as written.** Minor note: state explicitly that harmonic-flagged recoveries are included in the primary completeness count (they are real recoveries of the planet, even at the wrong alias) but are tracked so the alias rate is visible — confirm this is the intended convention.

### F6 — Primary estimand + multiplicity rule *(Must-fix; fix ready, one sub-choice)*

**Assessment.** Collapsing the multi-cell decision to a single pre-registered primary estimand — the occurrence-weighted marginal completeness difference $\overline{\Delta R}=\sum_c w_c(R_{\text{comb},c}-R_{\text{TLS},c})$, with non-inferiority declared iff the lower bound of the one-sided 95% CI on $\overline{\Delta R}$ exceeds $-0.02$, and per-cell $\Delta R_c$ reported as descriptive secondary (with Holm correction if cell screening is wanted) — is the correct way to make the decision well-posed. **Ready to apply,** with one embedded decision: **the weight prior $w_c$ is itself a researcher degree of freedom and must be pre-registered and justified** (e.g., log-uniform in $P$ × a stated radius-occurrence distribution, normalized over the $N_{\rm tr}\ge 2$ grid). Freeze $w_c$ in v2 before any data is read; do not let it be chosen after seeing per-cell results.

### F8 — Thresholds + TLS baseline + runtime protocol *(Must-fix; protocol ready, values sealed later)*

**Assessment.** The structure is correct: pin the TLS implementation (`transitleastsquares`, Ofir 2014 sampling, recorded version + grid), set the **common** SDE threshold $T$ to a pre-registered per-null-star false-alarm rate (recommend FAR $\le 1\%$), set $z_\star$ to a target local false-event yield (recommend $\le 1$ expected false event per null light curve), $N_{\min}=2$, a stated monotransit threshold $z_{\rm mono}>z_\star$, and a runtime protocol (single machine, single-thread CPU-core-seconds, median over $\ge 5$ repeats, shared conditioning cost excluded or charged equally).

**Critical process nuance (this affects the readiness verdict).** F8 **cannot be fully numerically resolved before reading data** — the actual values of $z_\star, \theta, T, \alpha, \varepsilon$ are *set on the CALIBRATION set*, which is an experimental step (milestone M3). What v2 must freeze **now** is the *protocol, the targets, and the calibration procedure* (e.g., "$T$ is whatever value yields FAR = 1% on null calibration stars"). The numeric thresholds are then derived during M3 and **hash-sealed before the single sealed-test run (M4)**. This is fully consistent with anti-tuning discipline (thresholds come from calibration data, never test data), but it means "resolve F8" = "freeze the procedure," not "write the numbers." This two-step structure should be stated explicitly in v2 so no one mistakes the calibration step for tuning.

**Net on the four.** F2, F6, F8 are mechanically ready (F6 needs the weight prior chosen; F8 freezes procedure now / values at M3). **F1 is the only true gate**, and it needs a human scope decision plus the two conditions I attached above.

---

## 6. Risks to Phase I

Ranked by likely impact on a credible result.

| # | Risk | Why it matters | Mitigation / current coverage |
|---|------|----------------|-------------------------------|
| R-1 | **Compute external validity (F1).** Even after scoping, the survey-scale story is the headline reviewer attack (PR-A). | Determines whether the compute claim survives review. | Adopt F1 (a)+(b)+(c); measure $\rho_d$; pre-register $\hat\pi$. **§5.** |
| R-2 | **Process slip: data read before v2 sealed.** | Forfeits anti-tuning guarantee; invalidates headline. | Hard gate in §4; record seal hash; vault `Current_Mission` already lists this ordering. |
| R-3 | **Seed-accuracy collapse under red noise** ($r_{\rm seed}g$ too low on routed planets). | This is *exactly* how v3 failed and how H0a wins. A real, expected possible outcome — and a publishable null. | Injection into **real** correlated noise; bootstrap-FAP; photometric gate. The experiment is built to detect this honestly. |
| R-4 | **Bootstrap-FAP exchangeability under red noise (F10).** | If the null surrogate isn't valid under correlated noise, H4 calibration is unsound. | [`MATH`](./TRINETRA_MATHEMATICAL_FOUNDATIONS.md) §9 flags it but **commits to no resampling scheme** — should commit to block/noise-model-aware resampling before M3. |
| R-5 | **Detrending destroys transits (F11, PR-H).** | Caps absolute recall; over-aggressive conditioning is a known recall sink. Cancels in the *comparison* (shared) but must be reported. | A2 asserts stationarity but **not transit preservation** — add a transit-injection-through-conditioning check. |
| R-6 | **Multi-planet systems (F4) & TTVs (F3) break period-from-spacing.** | Event-spacing recovery assumes one strict period; multiplicity/TTVs are common and defeat it. | Should-fix: state single-planet + strict-periodicity assumptions; scope "model-agnostic" to *detection only*; note TTV tolerance as a measured quantity. |
| R-7 | **Monotransit confirmation without repetition (F5, PR-D).** | A lone event can't be period-confirmed; a flare/systematic could masquerade. H3 is descriptive (excluded from headline), which limits exposure, but the vetting criterion is undefined. | Define a single-event vetting criterion (shape + ingress/egress + secondary + centroid, explicitly without repetition); state weaker FP control. |
| R-8 | **Straw-man TLS baseline (PR-F).** | If the baseline isn't an optimized TLS, the compute win is illusory. | F8 pins `transitleastsquares` + Ofir sampling; ensure it's a fair, optimized configuration and report the runtime protocol fully. |
| R-9 | **Underpowered cells → INCONCLUSIVE.** | Wide CIs trigger pre-planned sample-size increases → time/compute cost; not a failure but a schedule risk. | ≥500 injections/cell fixed; the *shown* power analysis (assumed recall, α, power → N) is still owed (F-level "power analysis shown"). |
| R-10 | **Stellar-parameter reliability.** | $\mathrm{SNR}_1$, duration, depth→radius all depend on TIC radii/density; uncertainty is assumed negligible but never stated. | Add an assumption + a propagation note; cross-check on the reality-check set. |

**Balance (what is *not* at risk).** The core logic is sound and well-guarded: the fairness keystone, the photometric-significance gate replacing timing coincidence, the bootstrap-FAP calibration, the recall-first non-inferiority framing, the master equation, and the honest, falsifiable pre-registration. None of the risks above require redesigning the architecture; all are scoping, specification, or measurement-protocol fixes.

---

## 7. Recommended Implementation Order

Front-loads the re-registration; maps onto the [`PAPER_NOTES.md`](./PAPER_NOTES.md) M0–M7 milestones. **No data is read until step 3 completes.**

**Step 0 — Resolve the blockers (no data).**
- 0.1 Obtain F1 sign-off (adopt (a)+(b)+(c); attach $\rho_d$ measurement + pre-registered $\hat\pi$).
- 0.2 Choose the F6 weight prior $w_c$ and justify it.
- 0.3 Apply F1/F2/F6/F8 edits to `SCIENTIFIC_HYPOTHESIS.md`, `TRINETRA_X_PHASE1_VALIDATION.md`, `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` (per the [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) edit map).
- 0.4 *Recommended (cheap, de-risks R-4/R-5):* also commit the bootstrap resampling scheme (R-4) and add the transit-preservation + power-analysis-shown notes; state single-planet/strict-periodicity scoping (R-6) and a monotransit vetting criterion (R-7). These are "should-fix" but resolving them now avoids a second re-registration later.
- 0.5 Reissue `TRINETRA_X_PHASE1_VALIDATION.md` + `SCIENTIFIC_HYPOTHESIS.md` as **v2, dated 2026-06-15**; **seal and hash-record.**

**Step 1 — M0: Freeze manifest + splits.** Fixed TESS SPOC 2-min sector list; leakage-safe calibration/test split by sky region/TIC; data/catalog version pinning (TESS release, TIC/TOI/EB catalog versions + access dates). → Table T1.

**Step 2 — M1: Detectability census.** Compute the $\mathrm{SNR}_1$ distribution of the confirmed TESS planet population; test assumption **A1** (bimodality). Use a general/calibration sample — **never the sealed test set.** → Figure F1. *(A1 failing here is itself a finding.)*

**Step 3 — M2: Conditioning + injection campaign.** Per-sector detrend + masking; inject Mandel–Agol transits into real LCs over the frozen $(P, R_p, b)$ grid; verify A2/A3 (stationarity, transit preservation, injection fidelity). → Table T1.

**Step 4 — M3: Threshold calibration (calibration set only).** Derive $z_\star, \theta, T, \alpha, \varepsilon$ to their pre-registered targets; compute the recall–compute frontier on calibration data; **hash-seal all numeric thresholds.** → Figures F4, F6.

**Step 5 — M4: Sealed-test evaluation (exactly one run).** Headline recall + compute on the sealed test set; primary estimand $\overline{\Delta R}$; routing fraction $f$; detector overhead $\rho_d$; survey-representative secondary figure. → Figures F3, F8; Tables T2, T3, T7.

**Step 6 — M5/M6: Parameter coverage, reality check, ablation.** Posterior interval coverage; TOI recall + EB/BEB rejection; the **required** gate-on/off and calibrated/uncalibrated-score ablation (substantiates the core contribution). → Figures F5, F7, F9; Tables T4, T5, T6, T8.

**Step 7 — M7: Write-up.** Phase I manuscript; positive or null reported with equal rigor.

**Decision gate after M4/M6:** proceed to Phase II *only* if H1 passes (or a clean, well-characterized null justifies a methods/null paper). Do not begin Phase II machinery before this gate.

---

## 8. Is Phase I Ready to Begin?

**No — not the data-touching part. Yes — the readiness work that precedes it.**

- **Ready:** the conceptual foundation, mathematical theory, hypothesis structure, fairness design, and falsifiability are in place and have survived an adversarial internal review. The repository is the authoritative source of truth and is internally consistent.
- **Not ready:** the pre-registration is still v1 with four open blockers that touch frozen parameters. Reading any sector data before resolving them and sealing v2 would violate the anti-tuning non-negotiable and compromise the headline result.
- **Distance to ready:** **short, and it is decision/documentation work, not research.** The critical path is a single human decision (F1) plus mechanical edits (F2/F6/F8) and a v2 reissue. F8's numeric thresholds are correctly deferred to the calibration step (M3) and do not block the start of M0.

**Verdict:** *TRINETRA-X is one signed-off decision and one re-registration away from a legitimate Phase I start. Resolve F1 → apply F2/F6/F8 → reissue + seal v2 → begin M0.*

---

## 9. Recommended Repository ↔ Vault Workflow

The goal ([`CLAUDE.md`](../CLAUDE.md)) is to **minimize context-window dependency over the project's lifetime**: knowledge must live in documents, not chats. The following protocol operationalizes that.

**Authority model (unchanged, restated for the record).**
- **Repository `docs/` = authoritative, citable, version-controlled, frozen specs.** The pre-registration, hypotheses, theory, and any promoted discovery live here. On conflict, repository wins.
- **Vault `vault/` = working research memory.** Daily logs, literature notes, derivation scratch, experiment logs, discovery capture, publication drafting. Never a specification unless explicitly promoted.

**The promotion rule (one direction).** Discoveries are *born* in the vault and, once significant or validated, are *distilled* into the repository (and, if they touch frozen parameters, re-dated under the pre-registration discipline). Nothing scientifically load-bearing stays only in the vault or only in chat.

**Concrete routing of artifacts.**

| Artifact | Lives in | Promotion trigger → destination |
|----------|----------|--------------------------------|
| Per-session work, questions, dead ends | `vault/01_Research_log/Daily_Research_Log.md` (one entry per session) | A confirmed result → distilled note + repo update |
| Math derivations / sanity checks | `vault/02_Mathematics/` (mirrors the canonical theory) | A correction or new derivation → `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` (re-dated) |
| Literature notes + citations | `vault/03_Literature/` | The citation set → **a real `references.bib` in the repo** (closes an open hygiene gap) |
| Per-milestone experiment logs (M0–M7) | `vault/04_Experiments/` | Frozen results → `results/` + Tables T1–T8 / Figures F1–F9 |
| Rejected ideas + lessons | `vault/04_Experiments/Failed_Ideas.md` | Durable lesson → cited where relevant (e.g., the v3 coherence lesson) |
| Manuscript drafting | `vault/05_Publication/` (working) | Frozen draft → `papers/` + `docs/PAPER_NOTES.md` index |
| **Decisions** (e.g., the F1 sign-off) | Recorded in the **repository** (validation v2 + a Key-Decisions entry); pointer in vault | — decisions are never vault-only |

**Three rules that protect Phase I specifically.**
1. **The pre-registration is repository-only and sealed.** It must carry an explicit freeze date and hash; it must never be edited in the vault or post-data. The vault may *discuss* it but not *hold* it.
2. **Calibration vs. test discipline is logged.** Every artifact that touches data records which split it used. The sealed-test run (M4) is logged once, with its date and the threshold hash it ran against — the auditable proof that anti-tuning held.
3. **Keep `PAPER_NOTES.md` indices stable.** Figure/table IDs (F1–F9, T1–T8) and milestone IDs (M0–M7) are already fixed; vault experiment logs should reference these IDs so drafts can cite results before they are finalized.

**Immediate vault housekeeping (low effort, high memory value).**
- Update `00_Home/Current_Mission.md` after the F1 decision and the v2 seal (it currently lists F1/F2/F6/F8 as open).
- Seed `02_Mathematics/`, `03_Literature/`, `05_Publication/` with stub notes mirroring the corresponding `docs/` sections so memory has a home from day one.
- Start a real `Daily_Research_Log.md` entry the moment Step 0 begins.

---

## Appendix — Readiness Checklist (single glance)

| Gate | State |
|------|:-----:|
| Repository is authoritative & internally consistent | ✅ |
| Mathematical theory complete & normative | ✅ |
| Hypotheses falsifiable, pre-registered (v1) | ✅ |
| Fairness keystone (identical TLS engine/threshold) specified | ✅ |
| Adversarial gap analysis performed | ✅ |
| Repo hygiene (root pointer, README, CLAUDE, .gitignore) | ✅ |
| **F1 scoping decision signed off** | ❌ **(gate)** |
| F2 recovery predicate applied | ❌ |
| F6 primary estimand + weight prior frozen | ❌ |
| F8 protocol/targets frozen (values → M3) | ❌ |
| Pre-registration reissued + sealed as **v2** | ❌ |
| `references.bib` created | ❌ (hygiene) |
| Bootstrap resampling scheme committed (R-4) | ⚠️ recommended in Step 0 |
| **M0 — manifest + leakage-safe split** | ⏸ blocked on v2 seal |

---

*Readiness report v1.0. Assessment only — no specification changed, no code written, no architecture redesigned, no new goals introduced. Resolve F1, apply F2/F6/F8, reissue and seal v2, then begin M0.*
