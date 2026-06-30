# VESPER

### Validation Engine for Stellar Photometric Evidence and Recovery
#### Evidence-First Exoplanet Discovery for the TESS Era

> **Find evidence first. Spend computation second. Let physics decide.**

**VESPER** (*Validation Engine for Stellar Photometric Evidence and Recovery*; named for the evening star) is a research program testing whether **evidence-first routing** can reduce the computational cost of exoplanet transit detection **without sacrificing recall**. Instead of folding every star's light curve at thousands of trial periods (the BLS/TLS approach), it detects individual transit-like events directly, infers the orbital period from their spacing, confirms candidates with a physics-based transit model, and reserves a full periodogram search only for the minority of stars showing no local evidence.

**Status:** Phase I — Scientific Validation (pre-registered). · **Data:** TESS. · **Charter author:** Ansul Suryawanshi.

---

## What's here

| Path | Contents |
|------|----------|
| [`docs/`](./docs/) | Canonical specifications and theory (start with [`docs/VESPER.md`](./docs/VESPER.md)) |
| [`CLAUDE.md`](./CLAUDE.md) | Operating rules for AI-agent sessions (non-negotiables, doc map) |
| [`REPOSITORY_GAP_ANALYSIS.md`](./docs/REPOSITORY_GAP_ANALYSIS.md) | Critical cross-document review |
| [`PHASE1_REMEDIATION.md`](./docs/PHASE1_REMEDIATION.md) | Fix plan for the critical / must-fix findings |
| `src/` · `data/` · `research/` · `results/` · `notebooks/` · `papers/` | Project scaffold (no code yet — Phase I is validation-only) |
| `archive/` | Prior-project forensic audit & scientific review (historical reference) |

## Read in this order

1. [`docs/VESPER.md`](./docs/VESPER.md) — the master charter (mission, philosophy, architecture, milestones).
2. [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) — the formal, falsifiable claims.
3. [`docs/VESPER_PHASE1_VALIDATION.md`](./docs/VESPER_PHASE1_VALIDATION.md) — the pre-registered experiment.
4. [`docs/VESPER_MATHEMATICAL_FOUNDATIONS.md`](./docs/VESPER_MATHEMATICAL_FOUNDATIONS.md) — the theory.
5. [`docs/VESPER_ARCHITECTURE.md`](./docs/VESPER_ARCHITECTURE.md) — the full system design.

## The core idea in one line

A transit search normally asks *"is there a planet at period P?"* ten-thousand times per star. VESPER asks once: *"does this star show any dimming the noise can't explain?"* — and only searches for a period where the evidence says to. The scientific test is whether that routing preserves recall (within 2 percentage points of full TLS) while measurably reducing compute.

## Status & next step

Phase I is at document/specification stage. The immediate next step is to resolve the four critical/must-fix items in [`PHASE1_REMEDIATION.md`](./docs/PHASE1_REMEDIATION.md), reissue the pre-registration as v2, then freeze the TESS sector/target manifest (milestone M0). No project code has been written yet — by design, validation comes first.

---

*Math in these documents uses LaTeX (`$…$`); view in a math-aware Markdown renderer (Obsidian, VS Code, GitHub) for proper formatting.*
