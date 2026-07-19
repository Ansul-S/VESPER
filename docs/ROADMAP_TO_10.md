# VESPER — Roadmap to 10/10 (all categories)

| Field | Value |
|---|---|
| **Date** | 2026-07-19 |
| **Basis** | [`docs/audits/PROJECT_AUDIT_2026-07-19.md`](./audits/PROJECT_AUDIT_2026-07-19.md) (second-pass full audit). Every task below traces to a named audit finding. |
| **Governing constraints** | NN#1–7 (CLAUDE.md); P-2 (v3 is final — **no sealed doc, threshold, weight, or tag is ever edited**); sealed artifacts append-only (erratum/addendum pattern). |
| **Hard gate** | **Phase II (Kepler) does not begin until every task in Waves 0–6 is complete and verified.** The Phase-II decision record (INN-3/INN-4 designs) may be *written* during Wave 6 but no Kepler data is touched. |

**Scores at baseline (audit 2026-07-19):**
Engineering 6.5 · Research 7.5 · Math rigor 6.5 · Architecture 6 · Code quality 6 · Documentation 8.5 · Innovation 7 · Reproducibility 8 · Publication readiness 5 · Production readiness 2.

**Honesty clauses (read before executing).**
1. **The sealed run's history cannot be rewritten.** "10/10 Research" here means: every conclusion stress-tested, every deviation quantitatively bounded, nothing left to a reviewer to discover. It cannot mean "the sealed run was executed flawlessly" — it wasn't, and the record says so.
2. **Innovation is judged by others.** The tasks raise the ceiling (methodology contribution, novel estimator designs); they cannot guarantee the score.
3. **Production readiness is redefined honestly.** The charter forbids a product and the science (π\*≈0.68 ≫ TESS π≈0.03) says the routing architecture should *not* be deployed as a compute-saver. 10/10 = the **validation pipeline as an installable, operable, deterministic research tool**, built last, regression-locked so it cannot alter any sealed output.

---

## Wave structure (dependency order)

```
Wave 0  VERDICT        finish the in-flight remediation (E2, erratum, commit)   ← everything blocks on this
Wave 1  ROBUSTNESS     E1 sensitivities + supporting studies + public reconciliation
Wave 2  MATH CLOSURE   formula consistency, derivations, error models, proofs
Wave 3  ENGINEERING    package, frozen/live safety, tests, CI, config hygiene
Wave 4  REPRO + DOCS   lockfile, DOI, tiered reproduction, doc consolidation
Wave 5  PUBLICATION    paper finalization → external review → submission
Wave 6  TOOL + PHASE-II PREP   production-grade research tool; Phase-II designs (no Kepler data)
```

Waves 2 and 3 can run in parallel after Wave 1. Wave 5 needs 1, 2, 4. Wave 6 is strictly last.

---

## Wave 0 — VERDICT (critical path; ~1 day of attention + ~19 h compute)

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| V-1 | Resume-guard patch for `e2_retiming.py` (skip task IDs already in ledger) | — | 0.5 h | Rerun appends only unseen tasks; no duplicates; guard unit-tested |
| V-2 | Complete E2 re-timing campaign (274 tasks remaining; workers ≤6 on the 4P+6E M4) | V-1 | ~19 h compute | `e2_retiming_summary.json` written; decision per CI rule (hi≤0.70 PASS / lo>0.70 FAIL / else INCONCLUSIVE) |
| V-3 | Fill erratum §5 (E2 result) and §7 (corrected Phase-I conclusion) | V-2 | 1 h | No `[PENDING-*]` markers remain |
| V-4 | Propagate verdict per DR-003 D3: paper §3.3/§3.4/abstract/§5, `CLAUDE.md` status, vault sync (Current_Mission, Dashboard, research log, session handoff) | V-3 | 1.5 h | Zero occurrences of unqualified "H1 FALSIFIED (compute)" outside sealed/append-only records |
| V-5 | Commit + push `phase1/audit-remediation`; open PR to `main`; merge after review | V-4 | 0.5 h | Branch merged; audit + roadmap + erratum in `main`'s history |

**Exit gate:** the project's headline verdict is evidence-backed and consistent across repo, paper draft, and memory systems.

---

## Wave 1 — ROBUSTNESS (Research 7.5→9, Publication 5→6.5; ~1 week)

Addresses audit §3.5, §3.6, §4-missing, §9-risks 1–2. All analyses run on **existing** artifacts (`recovery.csv`, calibration caches) — no TEST access, ever.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| RES-2 | **KM-period-weighted E1 sensitivity** (audit's #1 missing analysis): recompute ΔR̄ + all three CIs under w_P ∝ KM Eqn-25 broken power law (per radius bin), with the P=0.5 d node handled two ways (extrapolated; excluded). Report alongside the sealed log-uniform result. | V-5 | 1 d | Table: ΔR̄ + lo95 under {sealed, KM-extrapolated, KM-excl-P0.5} × {injection, cluster, Wilson} CIs; conclusion stated either way |
| RES-3 | **Epoch-tolerance sensitivity**: recompute rec_A/rec_B/ΔR̄ at ±0.5/0.75/1.0 T₁₄ from stored `epoch_err_t14` + arm T0s. Quantifies how much of E1's structure is predicate choice. | V-5 | 0.5 d | ΔR̄(tolerance) curve + gains/losses reclassification table in supplement |
| RES-4 | **Per-star τ_GP FAP sensitivity** on ≥100 calibration nulls: FAP with flat 0.005 vs per-star τ; measure gate-decision flips. Bounds erratum §2.4 empirically instead of by argument. | V-5 | 1 d (compute) | Flip rate reported with CI; statement "the flat-τ masking argument is measured, not asserted" |
| RES-5 | Edge control → paper supplement: methods paragraph, table, and the epoch-mechanism figure (SDE distributions + T0-error histogram at P=0.5 vs 0.62) | V-5 | 0.5 d | Supplement section S-edge complete; F3/§3.1 cross-referenced |
| RES-6 | **η-paid injection sub-study** (calibration only): raw-mode injection + recondition for ~200 injections across 4 cells; measure absolute-recall optimism of `cached_residual` directly | V-5 | 1–2 d (network+compute) | Measured Δ(absolute recall) with CI; cited wherever absolute figures appear |
| RES-7 | Monotransit campaign **design** (pre-registered protocol doc; execution = Phase II) | — | 0.5 d | Design doc with grid, endpoints, power analysis; no data touched |
| RES-8 | Endpoint-disclosure section: precision was not an endpoint; FP control = calibrated FAR; M6 EB-leakage quantified as the precision proxy | — | 2 h | Paper §2 states it; no reviewer can claim it was hidden |
| PUB-6 | **Public reconciliation**: v1.0.1 release notes correcting the verdict line; README badge/status; hackathon-status note in repo (deck itself is submitted history — annotate, don't rewrite) | V-5 | 0.5 d | No public VESPER surface states the withdrawn verdict as current |

**Exit gate:** every decision-bearing number has a sensitivity row; repo truth == public truth.

---

## Wave 2 — MATHEMATICAL CLOSURE (Math 6.5→10; ~1 week, parallel with Wave 3)

Addresses audit §3.2–3.4, §3.7.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| MATH-1 | **π\* consistency**: adopt the exact break-even $\pi^\star=\rho_d/(f_p(1-\rho+\rho_d))$ in MATH §8.3a (appendix note, not a sealed-section edit — new subsection 8.3b "exact form"), align `endpoints.py`, state the approximation chain explicitly | V-5 | 2 h | One formula, three places (MATH, endpoints, paper), all agree; unit test pins it |
| MATH-2 | **Detector-normalization derivation note**: conditions under which the MAD-normalized box filter approximates the Σ-whitened matched filter; bound the SNR bias using M1's measured acf₁ distribution (188 stars); state where the approximation fails (red stars) | — | 1 d | New MATH appendix; numerical bound (e.g. "SNR bias <x% for acf₁<0.05, covering y% of the sample") |
| MATH-3 | **Surrogate-contamination analysis** (audit §3.3 / implicit assumption): the FAP's block bootstrap scrambles a series *containing* the injected/true signal; write the argument that this only weakens the null ordering (conservative direction) and verify empirically on 50 calibration injections (FAP with vs without signal stripped) | — | 1 d | Written proof-sketch + measurement; direction and magnitude documented |
| MATH-4 | **Λ null-distribution study**: empirical null of the GP-LR statistic with *estimated* K on calibration nulls vs χ²₁; quantify the deviation T_red calibration absorbed | — | 1 d (compute) | QQ plot + KS distance in supplement; statement that empirical calibration covers the gap |
| MATH-5 | **Better cluster inference**: BCa (or studentized) host-cluster bootstrap for E1 beside the percentile CI; document small-cluster (n=40) caveat | RES-2 | 0.5 d | Both intervals reported; conclusions unchanged or the change is front-page |
| MATH-6 | **Comb-statistic identifiability note**: formal statement of the N=2 degeneracy (any P=spacing/m gives R̄=1), why argmin→longest-P is the realized convention, and how the FAP remains valid under the degeneracy | — | 0.5 d | MATH appendix subsection; cross-referenced from period_recovery docstring |
| MATH-7 | Notation/symbol cross-reference table (MATH symbols ↔ code identifiers ↔ paper notation), units column included | — | 0.5 d | Table in MATH §0a; CI check greps for orphaned symbols |
| MATH-8 | **Odd/even veto error model** (future-runs fix): replace white SEM with per-epoch depth scatter (cluster-robust over epochs); keep sealed behavior in `frozen_rerun` untouched; measure the veto's ROC on M6's EB set before/after | — | 1 d | New veto in live confirmer + test; EB rejection ≥ old at equal true-planet retention on calibration |

**Exit gate:** zero implementation-level statistical constructions without either a correctness argument or an empirical calibration; docs and code state identical formulas.

---

## Wave 3 — ENGINEERING & ARCHITECTURE & CODE (Eng 6.5→10, Arch 6→10, Code 6→10; ~2 weeks, parallel with Wave 2)

Addresses audit §2-weaknesses, §5-debt 1–6, §9-risk 3.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| ENG-1 | **Frozen/live equivalence harness** (debt #1): fixture LC (synthetic, committed) run through frozen_rerun and live {detector, period_recovery, confirmer, injection}; assert bit-equal where intended-identical; **explicit allowlist** of intentional divergences (gap-aware windows, per-star τ, u₂) with a test that the allowlist is exhaustive | V-5 | 1.5 d | CI job `frozen-equivalence` green; any unlisted divergence fails the build |
| ENG-2 | **Module-identity assertions** (debt #2): every entry script logs+asserts the resolved `__file__` of each scientific import (frozen vs live) against its declared intent | — | 0.5 d | Import-order mistakes become hard errors, not silent substitutions |
| ARCH-1 | **`vesper_core` package**: pyproject.toml, `pip install -e .`; live modules move to `src/vesper_core/{conditioning,detect,period,confirm,inject,endpoints,seals}`; research scripts become thin callers | ENG-1 | 3 d | All entry points import from the package; no `sys.path.insert` outside frozen loading; editable install in CI |
| ARCH-2 | **Frozen-code-as-data**: load `frozen_rerun` modules via `importlib` with recorded SHA-256 per file, verified at load (extends the seal pattern to code) | ARCH-1 | 1 d | `load_frozen_module("detector")` verifies digest; path shadowing eliminated |
| ARCH-3 | Typed stage interfaces: dataclasses for `LightCurve`, `EventSet`, `Seed`, `GateResult`, `ArmResult` with units in docstrings | ARCH-1 | 1 d | mypy clean on the package; interfaces documented |
| ARCH-4 | `hackathon/README.md`: provenance note (no shared code with sealed pipeline; deck predates DR-003 — see PUB-6 note) | — | 0.5 h | Present |
| ARCH-5 | Config/paths: single `vesper_core.config` (repo-root discovery, env override); kill all hardcoded `data/...` literals (6 files); centralize orphan constants (stride_frac 0.5, dedup 0.3 d, Λ_sec 25, k_σ 3.0) with provenance comments | ARCH-1 | 1 d | `grep -rn "data/processed\|data/manifests" src/ research/*.py` → only config module; constants have one home |
| CODE-1 | **Confirmer tests**: GLS δ̂/Λ vs analytic OLS on white noise (K=σ²I limit); sign-veto; odd/even both error models; secondary threshold; batman-absent trapezoid path | ARCH-1 | 1 d | ≥12 cases; branch coverage of `confirmer.py` ≥90% |
| CODE-2 | **Period/FAP tests**: comb statistic exact on synthetic combs (R̄=1); degeneracy convention pinned; FAP uniformity on white noise (distributional test, B small, seeded); block-bootstrap length logic | ARCH-1 | 1 d | FAP p-values ~U(0,1) at n=200 (KS α=0.01); deterministic under seed |
| CODE-3 | **Injection-geometry tests**: depth k², a/R★, T₁₄ vs published values for 3 known systems (tolerance 1%); n_transits formula vs data-driven counter on gapped fixtures | ARCH-1 | 0.5 d | Green |
| CODE-4 | Property-based tests (hypothesis) for `recovery.py` predicates (period/harmonic/epoch fold invariants) | ARCH-1 | 0.5 d | Green; no counterexamples at 10⁴ cases |
| CODE-5 | Ruff + mypy + format in CI; zero warnings policy on `src/` | ARCH-1 | 0.5 d | CI gate |
| CODE-6 | De-duplicate `_run_tls` (arms/edge_control), share via package; error-handling pass: no silent `except Exception` (confirmer GP fallback logs a warning + counter) | ARCH-1 | 0.5 d | One TLS wrapper; fallback events observable |
| CODE-7 | Perf micro-fixes: edge-control paired-injection reuse; vectorized cluster bootstrap (numpy group indices, no per-replicate concat) | — | 0.5 d | Cluster bootstrap ≥10× faster; results bit-identical under seed |
| ENG-6 | **CI matrix**: {macOS, ubuntu} × {3.11, 3.12}; jobs: unit, frozen-equivalence, lint/type, table-regeneration (see REPRO-4); coverage ≥85% on `src/vesper_core` | ARCH-1, CODE-1..5 | 1 d | All green on PRs; coverage badge |
| ENG-7 | Timing-measurement harness as a reusable module (process_time, BLAS pinning, warm-cache, P-core guidance doc) | — | 0.5 d | e2-style timing importable; documented hardware caveats |

**Exit gate:** one implementation per algorithm; frozen code digest-verified; the mathematical core is the *most*-tested code in the repo, not the least.

---

## Wave 4 — REPRODUCIBILITY & DOCUMENTATION (Repro 8→10, Docs 8.5→10; ~1 week)

Addresses audit §9-risk 4, §10.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| REPRO-1 | Environment lock: `uv.lock` (or pip-tools) + Dockerfile; image digest recorded; python/BLAS versions pinned | ARCH-1 | 0.5 d | `docker run vesper make tables` works offline from tracked manifests |
| REPRO-2 | **Zenodo DOI**: archive sealed manifests, erratum, reconstruction artifacts, code release (v1.1.0) | V-5, PUB-6 | 0.5 d | DOI minted; cited in paper's data-availability |
| REPRO-3 | `REPRODUCING.md`, tiered: (T1) verify hashes/seals — 5 min; (T2) regenerate all tables/figures from tracked artifacts — 30 min, offline; (T3) full re-run from MAST — documented runtime + caveats | REPRO-1 | 1 d | An external reader can execute T1/T2 verbatim |
| REPRO-4 | **CI table-regeneration job**: T2 runs in CI; generated tables diffed against committed ones | REPRO-1, ENG-6 | 0.5 d | Any drift between code and published numbers fails the build — the strongest anti-rot guarantee available |
| REPRO-5 | MAST provenance script (sector/target query → manifest rows) + data-availability statement | — | 0.5 d | Statement in paper; script in repo |
| REPRO-6 | Seed registry: one doc listing every seed (20260616, 20260619, 22, 7-xor conventions…) and exactly what each controls | — | 0.5 d | Complete; referenced by REPRODUCING.md |
| DOC-1 | `ARCHITECTURE_CURRENT.md`: the *realized* Phase-I system (vs the 7-stage vision doc), one diagram, links to code | ARCH-1 | 0.5 d | A new reader understands the realized system in 10 minutes |
| DOC-2 | Reading-order index: every doc labeled {SEALED, LIVE, HISTORICAL, APPEND-ONLY} with a recommended path for (a) reviewers (b) contributors | — | 0.5 d | In README + docs/INDEX.md |
| DOC-3 | Seal-chain postmortem (the rebrand break): timeline, root cause, fail-closed behavior, the dual-digest fix — written for an external audience | — | 0.5 d | Standalone doc; candidate blog/appendix (feeds INN) |
| DOC-4 | API docs for `vesper_core` (mkdocs, auto from docstrings) | ARCH-1 | 1 d | Built in CI; published on repo pages or in-repo |
| DOC-5 | CORRECTIONS.md: single index of erratum → DR-003 → addendum → sensitivity results, so the correction chain has one entry point | V-5 | 2 h | Every corrected number reachable in ≤2 clicks from README |

**Exit gate:** a stranger with the repo URL and no chat history can verify every published number in ≤30 min offline, or fully re-derive it with documented cost.

---

## Wave 5 — PUBLICATION (Pub 5→10; ~2 weeks calendar, incl. external review)

Depends on Waves 1, 2, 4.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| PUB-1 | Paper revision to verdict-final: abstract, §3.3/3.4, §5 conclusions from erratum §5/§7 | V-4 | 1 d | Internally consistent; no number without a tracked source |
| PUB-2 | Sensitivity results into main text (RES-2/3) + supplement (RES-4/6, MATH-3/4) | Wave 1, 2 | 1 d | Every audit §3 caveat appears in the paper, not just the erratum |
| PUB-3 | Supplement assembly: edge control, reconstruction validation, Λ-null study, seal postmortem summary | RES-5, MATH-4, DOC-3 | 1 d | Compiled; cross-referenced |
| PUB-4 | Regenerate **all** figures/tables at 40 hosts via `make_paper_artifacts.py`; captions audited (the "80 hosts" strings in F3/F8 captions die here) | V-5 | 0.5 d | `grep -rn "80 test hosts\|over 80" papers/ research/*/tables research/*/figures` → 0 |
| PUB-5 | Venue + authorship: pick target (AJ/PSJ/MNRAS for the science; alternatively a methods venue for the pre-registration framework — decide, don't drift); resolve affiliation ("TBD" on the byline is a desk-reject risk); ORCID | — | decision | Named venue, formatted to its style |
| PUB-7 | Compliance pass: references vs ADS (finish), limitations section (audit §3 is the checklist), author contributions, facility/software acknowledgments (TESS/SPOC, wotan, TLS, batman, celerite2 — citation completeness) | PUB-1 | 0.5 d | Venue checklist satisfied |
| PUB-8 | **External review before submission**: at least one qualified external reader; prepare a referee-anticipation pack (the audit's §3 findings + prepared responses — the strongest defense is that the project found them first) | PUB-1..4 | 1 wk calendar | Written external feedback addressed; anticipation pack in repo |
| PUB-9 | Submit; archive preprint (arXiv) with DOI cross-links | all above | 0.5 d | Submission receipt; preprint live |

**Definition of 10/10:** submitted (not just "ready"), with a supplement that answers every criticism this audit could construct, and a public correction chain a referee can verify independently.

---

## Wave 6 — RESEARCH TOOL + PHASE-II PREP (Prod 2→10, Innovation 7→ceiling; ~2 weeks; strictly last)

Production tasks are regression-locked: the CI table-regeneration job (REPRO-4) must stay green after every change — the tool may never alter a sealed output.

| ID | Task | Depends | Effort | Success criterion |
|---|---|---|---|---|
| PROD-1 | CLI: `vesper condition|inject|calibrate|evaluate|verify-seals` with config-file inputs; `--deterministic` mode | ARCH-1..5 | 2 d | Full calibration-side pipeline runnable from CLI on a fresh machine |
| PROD-2 | Container as the supported runtime; resource/env pinning; graceful degradation offline (cache-only mode) | REPRO-1 | 1 d | T2/T3 reproduction runs in-container |
| PROD-3 | Structured logging + auto-generated run manifests (config hash, seeds, module digests, timings) for every invocation — the seal pattern applied to *every* run, not just sealed ones | ARCH-2 | 1 d | Each run leaves a self-describing manifest |
| PROD-4 | Input validation + standardized MAST retry/backoff (promote M3's pattern); clear operator errors | PROD-1 | 1 d | Fuzzed bad inputs → clean errors, never partial artifacts |
| PROD-5 | Versioned releases + CHANGELOG; output-schema versioning | PROD-1 | 0.5 d | v1.1.0 released with the remediation + tool |
| PROD-6 | Runbooks: add-a-sector, re-run-a-stage, verify-everything; failure playbook (incl. the P-core timing note) | PROD-1..4 | 1 d | An operator who isn't the author can run each playbook |
| INN-1 | **Methodology contribution**: "Sealed single-shot validation with equivalence gates and pre-committed verdicts" — standalone short paper / extended methods section; this is the project's most defensible novel content | PUB-9 | 3 d | Draft complete; venue chosen (e.g. RNAAS/methods track or workshop) |
| INN-2 | Extract the seal tooling (digest-verified configs + code-as-data loaders + split tokens) into a small reusable library with docs | ARCH-2 | 2 d | Separate repo/package; VESPER consumes it; README shows a 5-line adoption |
| INN-3 | **Phase-II design record (no Kepler data):** the provably-equivalent cheap period-FAP estimator (EVT/precomputed-null with equivalence-gate obligations) — the replacement for the falsified lever, designed with proof obligations stated | Wave 5 | 2 d | Pre-registered design doc; equivalence criteria numeric before any data |
| INN-4 | **Epoch-refit confirmer design** + calibration-only prototype (fixes the dominant loss channel found by the edge control; D-3i forbade it in v3 — it is the natural Phase-II Arm-B upgrade) | Wave 5 | 2 d | Prototype measured on calibration: right-period/wrong-epoch loss rate at fixed FAR, before/after |
| RES-7× | Monotransit campaign protocol finalized into the Phase-II pre-registration draft | RES-7 | 0.5 d | Included in the Phase-II prereg draft |

**Phase-II gate checklist (all must be checked before any Kepler byte is read):**
- [ ] Waves 0–6 complete; CI fully green (unit, equivalence, tables, lint/type, matrix)
- [ ] Paper submitted; preprint + DOI live; public record reconciled
- [ ] Phase-II pre-registration drafted (INN-3, INN-4, RES-7×), owner-reviewed, **sealed with the Wave-3 digest tooling before first data access**
- [ ] Explicit owner sign-off recorded as DR-004

---

## Traceability: audit finding → task

| Audit finding | Task(s) |
|---|---|
| E2 verdict unsupported (§3.7, risk 1) | V-1..V-5 |
| w_P log-uniform not occurrence (§3.5 NEW) | RES-2 |
| Epoch-predicate structure of gains/losses (§3.6 NEW) | RES-3, RES-5, INN-4 |
| Flat τ_GP in FAP (§3.3) | RES-4 |
| Residual-space injection / η unpaid (§3.1) | RES-6 |
| No monotransit coverage (§3.1) | RES-7, RES-7× |
| Precision not an endpoint, undisclosed (§3.9) | RES-8 |
| Public artifacts state withdrawn verdict (risk 1) | PUB-6 |
| π\* formula inconsistency (§3.7 NEW) | MATH-1 |
| Detector "whitened filter" overclaim (§3.2) | MATH-2 |
| Surrogate contamination implicit (§3.3) | MATH-3 |
| Λ null vs χ²₁ with estimated K (§3.4) | MATH-4 |
| 40-cluster percentile CI roughness (§3.5) | MATH-5 |
| N=2 comb degeneracy (§3.3) | MATH-6 |
| Odd/even white-SEM veto (§3.4) | MATH-8 |
| Frozen/live duplication untested (debt 1) | ENG-1, ENG-2, ARCH-2 |
| No package / path shadowing (debt 2) | ARCH-1, ARCH-5 |
| Math core untested (debt 3) | CODE-1..4 |
| Hardcoded paths/constants (debt 4–5) | ARCH-5 |
| Perf micro-issues (debt 6) | CODE-7 |
| Data/env not archived (risk 4) | REPRO-1..5 |
| Figures/captions say 80 hosts (§4) | PUB-4 |
| Affiliation TBD, venue undecided (§10) | PUB-5 |
| Bus factor / operator docs (risk 5) | PROD-6, DOC-1..4 |
| Innovation ceiling (§12) | INN-1..4 |

## Definitions of done (per category)

- **Engineering 10:** CI matrix green with coverage ≥85% on the core; frozen-equivalence job; zero silent exception paths; timing harness reusable; no path/imports footguns possible without a red build.
- **Research 10:** every conclusion carries a sensitivity analysis; every sealed-run deviation *measured*, not argued; negative results reported with the same machinery as positive ones. (Ceiling note 1 applies.)
- **Math rigor 10:** every statistic in the codebase has either a derivation in MATH or an empirical calibration in a manifest; docs/code/paper state identical formulas; approximations carry numerical bounds.
- **Architecture 10:** one implementation per algorithm; frozen code loaded as digest-verified data; typed interfaces; config single-sourced.
- **Code quality 10:** the mathematical core is the best-tested code in the repo; lint/type clean; property tests on predicates; no duplication.
- **Documentation 10:** labeled doc taxonomy with reading paths; realized-architecture doc; API docs; single corrections index; postmortem published.
- **Innovation ceiling:** methodology paper drafted, seal tooling released, two novel Phase-II designs pre-registered with proof obligations. (Score is externally judged.)
- **Reproducibility 10:** tiered reproduction verified by CI (T2) and by an external human (T1/T2); DOI-archived artifacts; locked environment; seed registry.
- **Publication 10:** submitted with supplement + referee-anticipation pack; public record fully reconciled.
- **Production 10 (as defined honestly):** installable, containerized, deterministic CLI research tool with run manifests and runbooks — regression-locked against every sealed number.

## Effort summary

| Wave | Working effort | Calendar (solo, part-time) |
|---|---|---|
| 0 | ~4 h + 19 h compute | 1–2 days |
| 1 | ~5 days | 1 week |
| 2+3 (parallel) | ~5 + 12 days | 2.5 weeks |
| 4 | ~6 days | 1 week |
| 5 | ~5 days + external review | 2 weeks |
| 6 | ~16 days | 2.5 weeks |
| **Total** | **~50 working days** | **~9–10 weeks** |

---

*Execution rule: work strictly wave-by-wave; inside a wave, tasks marked with dependencies wait, everything else may interleave. Every completed task gets a one-line entry in the vault research log. Phase II remains frozen until the gate checklist is signed as DR-004.*
