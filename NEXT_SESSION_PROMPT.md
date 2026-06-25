# Next-Session Bootstrap Prompt

> Paste the block below into a fresh Claude Code session. Assumes **zero chat history**.

---

Resume **TRINETRA-X**. Assume zero chat history; **repository documents are authoritative**, the Obsidian `vault/` mirrors them. Markdown docs are the deliverables (no GSD / `.planning/`).

**Read in order:** `CLAUDE.md` → `SESSION_HANDOFF_2026-06-25.md` → `papers/phase1_evidence_first_triage.md` → `docs/PHASE2_KEPLER_SCALING_PREREG.md`.

**State: PHASE I COMPLETE; starting PHASE II (Kepler scaling).**
- Phase I (TESS) is done and merged to `main` (PRs #9–#13): the single sealed TEST read (P-5) → **H1 FALSIFIED — compute branch** (E1 recall non-inferiority PASS, ΔR̄ −0.48 pp / lo95 −0.60 pp; E2 scoped compute FAIL, 24.4% < 30%, ρ_d 14.4%). Recall principle **supported** (corroborated on real planets: T6 Arm B = Arm A = 86.7%). Manuscript v0.1 (author **Ansul Suryawanshi**), T1–T8, F3–F8, `references.bib` (8 core ADS-verified). Phase I is **sealed and final — no v4** (P-2).
- Verify integrity: Seal #2 `6292c018…`, Seal #2b `54f06a94…` (`shasum -a 256` the manifests); `git diff phase1-prereg-v3` over the 3 sealed docs is empty. TEST read once, never again.

**Phase II = Kepler scaling experiment** (new, separately pre-registered, P-8 — does NOT reopen Phase I). Hypothesis: the compute advantage **scales with search-space size** because the fast lane folds **k events** vs TLS **N points** per period (k≪N); TESS's short baseline under-powered it. Design (D1–D5 decided, in `docs/PHASE2_KEPLER_SCALING_PREREG.md`): Kepler **long-cadence**, ~2000 FGK / 30-70 split / ~150 hosts, baselines **{27 d, 0.25, 1, 2, 4 yr}** (27 d anchors to TESS), PASS = monotone-↑ reduction **AND ≥30% at 4 yr**, recall non-inferiority preserved. Re-calibrate thresholds on a Kepler calibration split; one sealed test read.

**Two open gates (owner decisions):**
1. **Compute path** — university/national HPC (NSM/C-DAC PARAM, free if eligible) vs **AWS `us-east-1` spot** (Kepler in MAST Open Data → no egress). Campaign is too big for the local MacBook Air. This gates tooling packaging.
2. **Paper venue** (AJ vs MNRAS) — non-blocking.

**Immediate next step:** confirm the compute path, then (a) open a PR for branch `phase2/kepler-scaling-prereg` → `main` (lands the sketch + EOD sync), (b) promote the sketch to a full Phase-II pre-registration, (c) build the cloud-portable Kepler M0-analogue (manifest + leakage-safe split), smoke-test on a few Kepler stars locally, pilot, then the full run. **Nothing is sealed or run until the Phase-II pre-registration is signed.**

**Deferred to separate future experiments (not Phase II):** Lever 3 (calibrated clean-skip — the survey-scale lever, recall-risky); cross-domain generalization (only vs correct incumbents in genuinely periodic-search domains — not the aperiodic-anomaly strawman).

Report verified integrity + the two open gates first; do not start building tooling until the compute path is chosen.

---

*Generated 2026-06-25 (EOD). Mirrors `SESSION_HANDOFF_2026-06-25.md`; the handoff is authoritative on any conflict.*
