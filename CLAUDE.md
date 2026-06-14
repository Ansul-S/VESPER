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
- **Documents are the current deliverables.** No project source code has been written yet. Prefer Markdown docs with LaTeX math (`$…$`); they render in math-aware viewers.
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
| [`docs/PHASE1_REMEDIATION.md`](./docs/PHASE1_REMEDIATION.md) | Plan to fix the Critical + Must-fix findings |
| [`archive/`](./archive/) | Historical (Revival-era audit & review) — context only, not current |

## Directory map

```
docs/        canonical specifications and theory
src/         pipeline stages (empty; no code yet): conditioning, detector,
             period_recovery, confirmation, classifier, evaluation
data/        raw, processed, injections, benchmark (empty)
research/    experiments, benchmarks, validation, literature (empty)
results/     outputs (empty)
notebooks/   exploratory notebooks (empty)
papers/      manuscript drafts (empty)
archive/     prior-project audit & review (reference only)
```

## Current status & immediate next step

- **Open decision:** the four Critical/Must-fix remediation items (F1, F2, F6, F8 in [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md)) must be resolved and the pre-registration reissued as **v2** before any data is read. **F1 (compute-measurement population) needs a human scoping decision.**
- **Then:** Phase I milestone **M0** — freeze the sector/target manifest and the leakage-safe calibration/test split.
- Revival repository is archival reference only and should not be consulted unless a specific historical artifact is required.
- **Tooling note:** GSD Core (a spec-driven workflow toolkit) is installed **globally** in `~/.claude`; this project has no local `.claude/` overrides yet.
- Claude should prefer repository documents over chat summaries whenever the two conflict.

## Conventions

- One claim → one table → one milestone → one frozen dataset. Keep figure/table indices stable.
- Convert relative dates to absolute. Cite the source document + section for any non-obvious claim.
- Do not modify `archive/` contents; they are historical record.
