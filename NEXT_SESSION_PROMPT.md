# Next-Session Bootstrap Prompt

> Paste the block below into a fresh Claude Code session. Assumes **zero chat history**.

---

Resume **TRINETRA-X**. Assume zero chat history; **repository documents are authoritative**, the vault mirrors them. Markdown docs are the deliverables (no GSD / `.planning/` in this repo).

**Read in order:** `CLAUDE.md` → `hackathon/CLAUDE.md` → `SESSION_HANDOFF_2026-06-29.md` → `hackathon/BAH2026_PS7_CHALLENGE.md` → `hackathon/BAH2026_PS7_PROPOSAL_DRAFT.md`.

**State.** The project pivoted to the **ISRO BAH 2026 hackathon, Problem Statement 7** (AI exoplanet detection/classification from noisy TESS light curves) — a new *applied* track that **extends** TRINETRA-X. **Phase I (TESS) is COMPLETE / SEALED / FINAL** (H1 falsified on the compute branch, recall supported; no v4). **Phase II (Kepler scaling) + its compute-path decision are FROZEN until after the hackathon.** The full **round-1 package is built and merged to `main` (PR #14)**: proposal, 11-slide PDF deck (`hackathon/deck/BAH2026_PS7_idea_deck.pdf`), classifier design, report skeleton, and a working prototype validated on real MAST data (all 5 PS7 steps; trapezoid shape-fit reproduces the committee's slide-5/6 output; 12 known-object validation). Team **TRINETRA-X** (Ansul Suryawanshi/IGNOU lead, Riddhi Jain/IGNOU, Samiksha Choudhary/Priyadarshini CoE Nagpur).

**Immediate priority: the hackathon round-1 deadline is 2026-07-01** — the only blocker is the **owner submitting** (paste Part-A fields from `BAH2026_PS7_PROPOSAL_DRAFT.md` + upload the deck PDF; select PS7). If already submitted, move to round-2 prep.

**Run env:** `.venv/bin/python` (lightkurve/astropy/wotan/transitleastsquares/batman/sklearn/matplotlib; no xgboost/torch). Reused spine: `research/m3_calibration/{detector,period_recovery}.py`; cached LCs: `data/processed/m1/*.npz`. Prototype: `hackathon/prototype/` (run scripts have READMEs).

**Round-2 prep (if/when shortlisted, ~Aug):** plug the organizer's curated labels into `train_classifier.py`; the named priorities are **robust period recovery + phase-curve handling** (the validation's weak spot), **pixel-level centroid/blend features**, an optional **CNN** branch (install torch), and fleshing out `BAH2026_PS7_REPORT_SKELETON.md`.

**Known issue:** root `CLAUDE.md` on `main` is stale (M4-era); a proposed status update is in `SESSION_HANDOFF_2026-06-29.md` §11 — apply it (owner approval) so memory reflects the hackathon pivot.

**Do NOT** reopen Phase I (sealed, no v4) or resume Phase II / the compute decision (frozen until after the hackathon). Report verified state + the round-1 submission status first.

---

*Generated 2026-06-29 (EOD). Mirrors `SESSION_HANDOFF_2026-06-29.md`; the handoff is authoritative on any conflict.*
