# Next-Session Bootstrap Prompt

> Paste the block below into a fresh Claude Code session. Assumes **zero chat history**.

---

Resume **TRINETRA-X Phase I** (evidence-first exoplanet detection, TESS). Assume zero chat history; **repository documents are authoritative**, the Obsidian `vault/` mirrors them.

**Read in order:** `CLAUDE.md` → `SESSION_HANDOFF_2026-06-18.md` → `research/m4_evaluation/M4_OPTION2_METHODOLOGY_DECISION.md` → `research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md` → `research/m4_evaluation/M4_COMBINED_ARM_RESULT.md`.

**State (M0–M3 sealed; M4 dry-run done; TEST UNREAD).** Verify integrity before any work:
- `git diff phase1-prereg-v2 -- docs/SCIENTIFIC_HYPOTHESIS.md docs/TRINETRA_X_PHASE1_VALIDATION.md docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` → must be **empty**.
- `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` → must equal `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692` (Seal #2).
- Seal #1 (M0) = `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`.

**What happened:** The M4 dry-run (CALIBRATION-only; TEST never read) found **Finding B** — the sealed Arm-B confirmation (targeted TLS, SDE≥T, single common T) is internally inconsistent (TLS SDE isn't comparable across grid widths), so **M4 is blocked**. The fix, **Option-2** (an epoch-fixed *folded-photometry* transit confirmer + full-TLS fallback), was **conditionally APPROVED by a methodology board as an amendment** (satisfies Non-Negotiable #3 per MATH §6; amends the fairness keystone "same engine" → "common FAR"; the evidence-first *principle* survives, the targeted-TLS *realization* does not). A **combined-arm calibration dry-run** gave **E1 PASS** (ΔR̄=−0.39 pp) / **E2 FAIL** (~20–29% < 30%, driven by the sealed B=1000 FAP overhead ρ_d≈12% + 59% FAP-gate fallback). A **governance board** proposed **v3 as the FINAL permissible amendment** + stopping rule **P-1…P-9** (`PHASE1_AMENDMENT_STOPPING_RULE.md`), **pending adoption**. **E2-fix R&D (exploratory, CALIBRATION-only, not adopted):** a **margined white-noise pre-filter** (skip the B=1000 bootstrap when a cheap white FAP exceeds ~5.5·α) was validated on injections to clip **ZERO recoverable planets** while skipping the bootstrap on **97.5% of noise** → ρ_d→~0 → projected **E2 ~40% (PASS)** — so **E2 is fixable**, but the fix touches **sealed A.8** (expands v3 scope). See `validate_prefilter_injections.py`.

**This session — decisions are the owner's; do not begin re-registration until told. In order:**
1. **Adopt (or revise) the v3-as-final stopping rule (P-1…P-9)** and pre-commit the E1/E2/inconclusive outcome mapping (handoff §6) **before** any drafting.
2. **Rule on methodology condition #1:** is a **folded-photometry transit likelihood-ratio** an acceptable physics arbiter (NN#3)? (The dry-run's box depth-SNR is borderline.) If **no** → write up the narrow negative result (targeted-TLS infeasible; principle untested — note E2 is fixable, so this is a choice to stop, not a forced falsification). If **yes** → 3.
3. **Decide v3 SCOPE:** confirmer-only, OR confirmer + the period-FAP cheapening (the E2-fix R&D; re-opens sealed A.8, bigger amendment, bumps v3-as-final).
4. **Authorize drafting** DR-002 (Finding B + Option-2 amendment + stopping rule + outcome mapping) + VAL v3 / MATH v1.2 governance + **T_red calibration plan** (full cleaned null pool, FAR≤1%/star) + (if in scope) the **margined pre-filter plan** → **Seal #2b**, sealed **before** the single TEST run. Then M4 (one TEST run → E1/E2 → pre-committed verdict).

**Hard constraints:** TEST is read **exactly once**, only after v3 is sealed. **No sealed value, threshold, grid, statistic, or config may change** except via the (final) v3 re-registration. Anti-tuning (NN#2) intact: TEST never read; decide on CALIBRATION only. Conditioning/catalog queries run **sandbox-disabled (host network)**. This repo uses **Markdown docs as deliverables (no GSD / `.planning/`)**.

Report the verified integrity status + the proposed stopping rule and the NN#3 decision point first; **do not draft DR-002 / VAL v3 / Seal #2b until the owner adopts the stopping rule and rules on condition #1.**

---

*Generated 2026-06-18 (EOD). Mirrors `SESSION_HANDOFF_2026-06-18.md`; the handoff is authoritative on any conflict.*
