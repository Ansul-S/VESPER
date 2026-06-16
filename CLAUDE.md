# CLAUDE.md — TRINETRA-X Operating Rules

> Project rules for any Claude Code session in this repository. Read this first. Keep edits to this file under ~200 lines.

## What this project is

TRINETRA-X is an **evidence-first** exoplanet-detection research program for the **TESS** era (ISRO exoplanet challenge). It tests whether *routing on evidence* — detect transit-like events cheaply, infer the period from their spacing, confirm with physics, and run a full search only where no evidence exists — can cut compute without sacrificing recall. Authoritative charter: [`docs/TRINETRA-X.md`](./docs/TRINETRA-X.md).

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
> A false positive is acceptable; a missed planet is not. **Photometric significance — depth, shape, repetition — not timing coincidence — is what makes a candidate a planet.** (This is the corrected lesson of the prior version; see [`docs/TRINETRA_CONCEPT_RECONSTRUCTION.md`](./docs/TRINETRA_CONCEPT_RECONSTRUCTION.md) §E.)

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
- **Pre-registration discipline.** [`docs/TRINETRA_X_PHASE1_VALIDATION.md`](./docs/TRINETRA_X_PHASE1_VALIDATION.md) and [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) freeze the experiment. **Changing a frozen parameter after data is touched is forbidden.** Amendments made *before* data is read are legitimate but must be **re-dated** as a new pre-registration version.
- **Documents remain the authoritative deliverables.** Specs/decisions are Markdown with LaTeX math (`$…$`). Milestone **execution tooling now exists** under `research/m0_manifest/`, `research/m1_conditioning/`, `research/m2_injection/` (M0–M2); the sealed protocol still governs and "no premature Phase II machinery" still holds.
- **Negative results are results.** A clean falsification of the hypothesis is a successful Phase I, to be reported with equal rigor.
- **Ask before scope expansion.** If a task implies building Phase II machinery (learned detector, classifier, habitability), confirm first.

## Document map (canonical sources)

| Document | Role |
|----------|------|
| [`docs/TRINETRA-X.md`](./docs/TRINETRA-X.md) | Master charter (author: Vesper) |
| [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) | Formal H1/H0 + secondary hypotheses, assumptions, success/failure criteria |
| [`docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](./docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md) | Canonical theory (math only) |
| [`docs/TRINETRA_X_ARCHITECTURE.md`](./docs/TRINETRA_X_ARCHITECTURE.md) | 7-stage system design (full vision) |
| [`docs/TRINETRA_X_PHASE1_VALIDATION.md`](./docs/TRINETRA_X_PHASE1_VALIDATION.md) | Pre-registered Phase I protocol |
| [`docs/TRINETRA_CONCEPT_RECONSTRUCTION.md`](./docs/TRINETRA_CONCEPT_RECONSTRUCTION.md) | Concept lineage & v3 post-mortem |
| [`docs/PAPER_NOTES.md`](./docs/PAPER_NOTES.md) | Publication notebook |
| [`docs/REPOSITORY_GAP_ANALYSIS.md`](./docs/REPOSITORY_GAP_ANALYSIS.md) | Critical cross-document review (12 findings) |
| [`docs/PHASE1_REMEDIATION.md`](./docs/PHASE1_REMEDIATION.md) | Plan to fix the Critical + Must-fix findings (**resolved** — see DR-001) |
| [`docs/PHASE1_READINESS_REPORT.md`](./docs/PHASE1_READINESS_REPORT.md) | Phase I scientific-readiness assessment |
| [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md) | DR-001 — F1 compute-scope decision + seal record |
| [`PHASE1_EXECUTION_PLAN.md`](./PHASE1_EXECUTION_PLAN.md) · [`PHASE1_M0_CHOICES.md`](./PHASE1_M0_CHOICES.md) | M0 execution plan + signed frozen choices (Seal #1) |
| [`PHASE1_M1_PLAN.md`](./PHASE1_M1_PLAN.md) | M1 Stage-0 conditioning plan + signed choices |
| [`PHASE1_M2_PLAN.md`](./PHASE1_M2_PLAN.md) | M2 injection + η transit-preservation; detrend-window finalization (2.5 d) |
| [`SESSION_HANDOFF_2026-06-16.md`](./SESSION_HANDOFF_2026-06-16.md) | Latest session handoff (resume point) |
| [`archive/`](./archive/) | Historical (Revival-era audit & review) — context only, not current |

## Directory map

```
docs/        canonical specifications and theory
src/         pipeline-stage scaffold (Phase-I tooling lives in research/):
             conditioning, detector, period_recovery, confirmation, classifier, evaluation
data/        manifests/{m0,m1,m2} = provenance + results (tracked);
             raw/processed/injections/benchmark = local caches (gitignored)
research/    m0_manifest, m1_conditioning, m2_injection (M0–M2 tooling);
             + experiments, benchmarks, validation, literature
results/     outputs (empty)
notebooks/   exploratory notebooks (empty)
papers/      manuscript drafts (empty)
archive/     prior-project audit & review (reference only)
```

## Current status & immediate next step

> The bullets below are **operational status**, not editable specifications. The sealed protocol (next bullet) is the spec; do not treat status lines as commitments to amend.

- **Pre-registration is SEALED (v2, 2026-06-15).** All Critical/Must-fix (F1, F2, F6, F8) + should-fix (R-4..R-7) resolved in the seal. Remaining gap items are Low hygiene only (F9 BLS wording).
- **F1 decision (DR-001):** compute claim scoped to the fast-path-eligible population; survey-representative compute is a pre-registered *secondary* endpoint (ρ_d, π\*); clean-skip deferred to Phase II. [`docs/decisions/F1_DECISION_RECORD.md`](./docs/decisions/F1_DECISION_RECORD.md).
- **Sealed documents (do not edit without a new re-registration):** `SCIENTIFIC_HYPOTHESIS.md` v2.0, `TRINETRA_X_PHASE1_VALIDATION.md` v2 (incl. Appendix A), `TRINETRA_MATHEMATICAL_FOUNDATIONS.md` v1.1. Seal = git tag **`phase1-prereg-v2`** (commit `723087e`), pushed (`origin` = github.com/Ansul-S/TRINETRA-X). Content hashes in DR-001.
- **M0 / M1 / M2 EXECUTED (2026-06-15 → 16):**
  - **M0** — manifest + leakage-safe split. **Seal #1** (manifest SHA-256 `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`). Sectors **S1–S3**; **22,723** targets; calibration 6,925 / test 15,798. Manifest table = release asset `m0-manifest-v1` (hash + provenance in git).
  - **M1** — Stage-0 conditioning (wotan biweight + noise model). η-sample 188/200; σ ~1067 ppm.
  - **M2** — injection + η transit-preservation. **Detrend window finalized at 2.5 d.** η gate PASS on Rₚ≥2; **Rₚ=1 row excluded as noise-limited** (detectability bimodality); 0.5/2 documented borderline.
- **The TEST split is untouched (sealed until the single M4 run). No detection thresholds set yet** — those are **M3 → Seal #2** (calibration-derived, hash-sealed before M4; VAL A.10). Anti-tuning (non-negotiable #2) intact.
- **Immediate next step: M3 — threshold calibration → Seal #2.** Prerequisite: **recompute the M1 noise model at the finalized 2.5 d window** (the 0.5 d model is superseded). Then draft `PHASE1_M3_PLAN.md` + a frozen-parameter choices proposal and get owner sign-off **before** deriving/sealing thresholds. First merge PR #4 (M2) and sync `main`.
- **Latest handoff:** [`SESSION_HANDOFF_2026-06-16.md`](./SESSION_HANDOFF_2026-06-16.md). PR-based landing: PRs #1–3 merged, **PR #4 (M2) open**. GSD Core is globally installed but **not used** here (no local `.planning/`). Archive material is reference only; prefer repository documents over chat summaries.

## Conventions

- One claim → one table → one milestone → one frozen dataset. Keep figure/table indices stable.
- Convert relative dates to absolute. Cite the source document + section for any non-obvious claim.
- Do not modify `archive/` contents; they are historical record.
