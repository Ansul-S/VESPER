# SESSION HANDOFF — 2026-06-15

| Field | Value |
|-------|-------|
| **Purpose** | Let a fresh Claude Code session resume VESPER with **zero reliance on chat history**. |
| **Phase** | Phase I — Scientific Validation |
| **Status** | Pre-registration **v2 SEALED**. No data read. Implementation not started. |
| **Read first** | [`CLAUDE.md`](../../CLAUDE.md) → this file → [`docs/decisions/F1_DECISION_RECORD.md`](../../docs/decisions/F1_DECISION_RECORD.md) |

> Authority order: repository documents are authoritative; the Obsidian `vault/` mirrors them; this handoff is a convenience pointer. If anything here conflicts with a sealed document, the sealed document governs.

---

## 1. Current repository state

- **Sealed pre-registration (v2, 2026-06-15).** Three documents are frozen; do **not** edit them without a new, re-dated pre-registration:
  - `docs/SCIENTIFIC_HYPOTHESIS.md` — v2.0 — `6adae7f10bda28f9f86c74e8221939d9f3604a6d9935e2d7750731c826680f5e`
  - `docs/VESPER_PHASE1_VALIDATION.md` — v2 (incl. Appendix A) — `441b2c94d9ed37c2883bb55cf24f71ca2fa992e0389fea3efc7f0642b8846b40`
  - `docs/VESPER_MATHEMATICAL_FOUNDATIONS.md` — v1.1 — `4f8d95c661aba61b8bb6d43736d0685acdf9ef52b6623d0e3543b27a82034537`
- **Seal:** git tag `phase1-prereg-v2` → commit `723087e`. Verify with `git diff phase1-prereg-v2 -- docs/SCIENTIFIC_HYPOTHESIS.md docs/VESPER_PHASE1_VALIDATION.md docs/VESPER_MATHEMATICAL_FOUNDATIONS.md` (must be empty).
- **GitHub:** `origin = https://github.com/Ansul-S/VESPER`; `main` and the tag are pushed. `gh` is authenticated (account `Ansul-S`).
- **Code/data:** none. `src/ data/ research/ results/ notebooks/ papers/` are empty scaffolds by design. No data has been read.
- **Decision records:** `docs/decisions/F1_DECISION_RECORD.md` (DR-001).
- **Other key docs:** `docs/PHASE1_READINESS_REPORT.md`, `docs/REPOSITORY_GAP_ANALYSIS.md` (F1–F12), `docs/PHASE1_REMEDIATION.md`, `docs/PAPER_NOTES.md`.

## 2. Current milestone

- **Done:** pre-registration completion + seal.
- **Current:** **M0 planning** (no data touched yet).
- **M0 scope:** freeze the TESS SPOC 2-min sector/target manifest and the leakage-safe calibration/test split (split by sky region / TIC; no training split — the Phase I detector is untrained).

## 3. Recent decisions

- **DR-001 (F1).** Compute claim scoped to the **fast-path-eligible population**; survey-representative compute is a pre-registered **secondary** endpoint reporting `C_comb/C_full(π)` and break-even `π* = ρ_d/f_p`; **clean-skip routing deferred to Phase II**. Three guardrails: (1) eligibility frozen on calibration; (2) detector overhead ρ_d measured; (3) π̂ pre-registered + frontier reported.
- **F6 prior frozen:** log-uniform in period × **Kunimoto & Matthews (2020)** radius occurrence; same framework defines π̂.
- **Should-fix folded into v2:** R-4 (block-bootstrap FAP), R-5 (transit preservation η≥0.90), R-6 (single-planet / strict-periodicity scope), R-7 (monotransit vetting).

## 4. Sealed specifications (what is now fixed)

- **Endpoints:** E1 recall non-inferiority on the occurrence-weighted primary estimand ΔR̄ (lower 95% CI > −2 pp); E2 compute ≥30% reduction on fast-path-eligible population (ρ_d included); E3 survey-representative compute (secondary, expected ≈0/negative at TESS π).
- **Recovery predicate (both arms):** period 1% (harmonics m∈{2,3} flagged) · epoch ±0.5 T₁₄ · SDE ≥ T.
- **Frozen parameters & procedure:** `VESPER_PHASE1_VALIDATION.md` Appendix A (TLS baseline, threshold targets, weight prior, π̂, runtime protocol, block-bootstrap, conditioning/η, manifest-hash step).
- **Deferred to M3 (calibration-derived, NOT tunable on test):** numeric values of z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP — hash-sealed into the manifest before the single M4 test run.

## 5. Open tasks

1. **Author `PHASE1_EXECUTION_PLAN.md`** (recommended first task — see §7).
2. **Begin M0:** freeze sector/target manifest + leakage-safe split (Table T1).
3. **Non-blocking follow-ons** (do not affect sealed hashes): create `references.bib` (Kunimoto & Matthews 2020 is load-bearing); add the one-line Phase-I scoping note to the charter `docs/VESPER.md` (F7).

## 6. Risks (carried forward; full list in PHASE1_READINESS_REPORT.md §6)

- **R-1 / PR-A:** compute external validity — the scoped claim holds only if ρ_d is genuinely small (π f_p > ρ_d). Measure ρ_d at M3/M4.
- **R-2 process:** never read data before M0 begins under the sealed protocol; any post-data change to frozen parameters violates non-negotiable #2.
- **R-3:** seed-accuracy collapse under red noise (the v3 failure mode) is a real possible null — and a publishable one.
- **R-4 mitigated:** bootstrap exchangeability under red noise (block bootstrap committed); verify calibration on null stars (H4).
- **R-5/R-8:** conditioning recall cost (η≥0.90 check) and straw-man-baseline avoidance (optimized TLS).

## 7. Recommended first task for the next session

**Author `PHASE1_EXECUTION_PLAN.md`** — a Phase I execution plan that turns the sealed protocol into an ordered M0→M7 work plan (deliverables, data sources, manifests, the M3 calibration seal, and the single M4 test run), **without reading any data**. Then execute **M0**. Do not begin M1+ data steps until M0's manifest and split are frozen. Keep all sealed documents immutable.

---

*Handoff generated 2026-06-15 at session end. Pre-registration sealed; M0 not started; no data read.*
