# Next-Session Bootstrap Prompt

> Copy-paste the block below into a fresh Claude Code session. It assumes **zero chat history**.

---

Resume **TRINETRA-X Phase I** (evidence-first exoplanet detection, TESS era). Assume zero chat history; **repository documents are authoritative**, the Obsidian `vault/` mirrors them.

**Read in order:** `CLAUDE.md` → `SESSION_HANDOFF_2026-06-16.md` → `PHASE1_M3_PLAN.md`.

**State:** M0–M3 complete. **Seal #1** (M0 data manifest) = `1f2d49e1…`; **Seal #2** (M3 threshold manifest) = `6292c018…`. Confirm both intact before any work:
- `git diff phase1-prereg-v2 -- docs/SCIENTIFIC_HYPOTHESIS.md docs/TRINETRA_X_PHASE1_VALIDATION.md docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` → must be **empty**.
- `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` → must equal `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`.

**Sealed thresholds (Seal #2, do not change):** z⋆=3.4 · z_mono=5.3 · N_min=2 · T=10.74 · α_FAP=1% · ε=0.01 · w_c (92.8% on Rₚ≤2 R⊕) · π̂=3.17%.

**Current milestone — M4: the single sealed-TEST run** → E1 (occurrence-weighted recall non-inferiority vs full TLS, pass iff one-sided 95% CI lower bound > −2 pp) and E2 (scoped compute, with detector overhead ρ_d). The **TEST split (15,798 targets) has never been read — it is read exactly once, at M4.** No threshold/weight/conditioning/detector/bootstrap change is permitted under Seal #2 (any change needs a new pre-registration).

**Objective this session:** draft `PHASE1_M4_PLAN.md` (execution-only — reuses Seal #2, introduces no new frozen parameters; plan TEST conditioning + dual-arm shared-TLS recovery + the compute ledger), **confirm scope with me before touching TEST**, then execute the single run. Expect E1 to be dominated by Rₚ≤2 (report the Rₚ=1 noise-limited bound honestly).

**Env:** `.venv/` (transitleastsquares 1.32, lightkurve, wotan, celerite2, astroquery). Conditioning/catalog queries (MAST/Vizier) are **blocked in the sandbox — run sandbox-disabled (host network)**; PyPI reachable. This repo uses **Markdown docs as deliverables (no GSD / `.planning/`)**.

Report current state + the proposed M4 plan first; do not read TEST until the plan is approved.

---

*Generated 2026-06-16 (end of session). Mirrors `SESSION_HANDOFF_2026-06-16.md`. The handoff is authoritative on any conflict.*
