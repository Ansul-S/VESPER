# Daily Research Log

---

## 2026-06-15 — Phase I pre-registration completed and sealed (v2)

Worked On:
- Full readiness review of the reconstructed repository + vault → produced docs/PHASE1_READINESS_REPORT.md.
- Resolved the four pre-registration blockers and folded in the four should-fix items, then re-registered to v2 and sealed.

Discoveries / Decisions:
- **F1 decision (DR-001):** scope the Phase I compute claim to the fast-path-eligible population; report survey-representative compute as a pre-registered secondary endpoint (with detector overhead ρ_d and break-even prevalence π* = ρ_d/f_p); defer clean-skip routing to Phase II. Adopted with three guardrails (eligibility frozen on calibration; ρ_d measured; π̂ pre-registered + frontier reported).
- Key insight: at TESS-realistic prevalence π ~ 10⁻², survey-scale saving ≈ π·f_p − ρ_d is near zero/negative by construction — so a near-zero E3 is an *expected, honest* result, not a failure. This is what motivates the Phase II clean-skip tier.
- F2: operational recovery predicate pinned (period 1% / harmonics m∈{2,3} flagged · epoch ±0.5 T₁₄ · SDE ≥ T), applied identically to both arms.
- F6: single occurrence-weighted primary estimand ΔR̄ with log-uniform period prior × Kunimoto & Matthews (2020) radius occurrence; per-cell results secondary (Holm) and never gating.
- F8: TLS baseline, thresholds/targets, and runtime protocol pinned in Validation Appendix A; numeric thresholds correctly deferred to M3 (calibration-derived), sealed before M4.
- R-4: committed circular block-bootstrap FAP scheme (L_b = 3·max(τ_GP, T₁₄), B ≥ 1000) — closes the red-noise exchangeability gap.
- R-5: transit-preservation requirement (median η = δ_post/δ_true ≥ 0.90) as a required pre-M3 check.
- R-6: single-planet + strict-periodicity scope stated explicitly; "model-agnostic" claim scoped to event detection only.
- R-7: monotransit single-event vetting criterion (shape, ingress/egress, no secondary, centroid); weaker FP control acknowledged; excluded from headline.

Artifacts created/updated:
- Re-registered: SCIENTIFIC_HYPOTHESIS.md v2.0, TRINETRA_X_PHASE1_VALIDATION.md v2, TRINETRA_MATHEMATICAL_FOUNDATIONS.md v1.1.
- Created: docs/decisions/F1_DECISION_RECORD.md (DR-001), docs/PHASE1_READINESS_REPORT.md.
- Seal: commit 723087e, annotated tag `phase1-prereg-v2`; content hashes verified against the tagged tree.

Problems / Risks carried forward:
- Top residual risk remains F1/PR-A external validity — mitigated but the scoped claim only holds if ρ_d is genuinely small; must be measured at M3/M4.
- Other live risks (tracked in readiness report §6): seed-accuracy collapse under red noise (the v3 failure mode, a real possible null), bootstrap exchangeability under red noise (mitigated by R-4), conditioning recall cost (R-5), straw-man-baseline avoidance (F8), underpowered cells.

Next Action:
- Begin M0: freeze the TESS sector/target manifest + leakage-safe calibration/test split (first data-touching step). Data must not be read before M0 begins under the sealed protocol.
- Non-blocking: create references.bib; add Phase-I scoping note to the charter.

---

## 2026-06-15 (cont.) — Seal, GitHub publication, and project-memory synchronization

Worked On:
- Cut the pre-registration seal, published the repository to GitHub, and synchronized all project memory for clean session handoff.

Summary of the day's major changes (consolidated for handoff):
- **F1 decision** adopted (a+b+c with three guardrails): compute claim scoped to the fast-path-eligible population; survey-representative compute as a pre-registered secondary endpoint (ρ_d, π* = ρ_d/f_p); clean-skip deferred to Phase II.
- **DR-001 created** — docs/decisions/F1_DECISION_RECORD.md (rationale, consequences, guardrails, seal hashes).
- **v2 re-registration** applied across the three frozen documents.
- **F1, F2, F6, F8 resolved**; **R-4, R-5, R-6, R-7 incorporated** into the same v2 seal (no second pre-data re-registration needed).
- **Seal created** — commit `723087e`, annotated tag `phase1-prereg-v2`; frozen-doc SHA-256 hashes verified.
- **GitHub repository created + pushed** — origin = https://github.com/Ansul-S/TRINETRA-X; `main` and tag `phase1-prereg-v2` are on the remote; `.obsidian/workspace.json` now gitignored.
- **Vault synchronized** — Current_Mission, Dashboard, this log; SESSION_HANDOFF_2026-06-15.md created.
- **CLAUDE.md** "Current status" + document map updated; Obsidian-sync operational guidance added.

Status after session:
- Pre-registration SEALED. No Critical/Must-fix/should-fix findings open. No data read. M0 not started.

Next Action:
- Author PHASE1_EXECUTION_PLAN.md, then begin M0 (freeze sector/target manifest + leakage-safe split).

---

## 2026-06-15 (cont.) — M0 execution plan authored and approved

Worked On:
- Authored `PHASE1_EXECUTION_PLAN.md` (v0.1, **M0 increment only**) from the sealed protocol and got in-session owner approval to start M0.

Discoveries / Decisions:
- **Tooling note:** the `/gsd-plan-phase` skill is built for a GSD `.planning/` software project (hard-errors without ROADMAP.md; spawns research/planner agents emitting GSD `PLAN.md` files). TRINETRA-X has no `.planning/` and treats documents as deliverables, so running GSD would have meant unrequested scaffolding + web-searching agents. Decision: apply GSD's *discipline* (milestones → tasks → deps → risks → deliverables → completion criteria) in the project's native research-doc form; no agents spawned. Recorded here so the choice isn't lost to chat.
- **M0 scope clarified:** M0 operates on **catalog metadata only** (TIC, SPOC 2-min availability, coordinates, stellar params, baselines, TOI/EB labels). Bulk light-curve retrieval + conditioning is **M1**. The leakage-safe split needs only TIC IDs + sky coordinates — no photometry — so M0 honors "no data download" cleanly while still being the first archive-touching step.
- **Two seals kept distinct:** **Seal #1** = M0 manifest content-hash (who/what data). **Seal #2** = M3 threshold manifest hash (VAL A.10) — numeric thresholds (z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP) stay deferred to calibration. M0 sets **no** thresholds.
- M0 decomposed into M0.1 sectors → M0.2 metadata target manifest → M0.3 labels/null pool → M0.4 leakage-safe split (TIC-disjoint **and** sky-region/camera-CCD-blocked, no training split) → M0.5 feasibility/power check (≥500 injections/cell at n_tr≥2 vs §6) → M0.6 manifest assembly + Seal #1. Includes a 7-row risk register, deliverables table, 8 binary completion criteria, and a traceability matrix to the sealed clauses.

Artifacts created/updated:
- Created: `PHASE1_EXECUTION_PLAN.md` (status **APPROVED**, M0 not started, no data read; sealed docs verified byte-identical to `phase1-prereg-v2`).
- Vault synchronized: Current_Mission, Dashboard, this log.

Problems / Risks carried forward:
- Same Phase I risk register (readiness report §6). M0-specific risks now tracked in the plan: systematic leakage surviving a TIC-only split (→ sky-region/camera-CCD blocking + audit), selection bias (outcome-independent cuts), null-pool contamination (catalog incompleteness bounds H4), reproducibility (pin versions/seeds + hash), power shortfall (M0.5 gate), premature TEST inspection (Seal #1 + access rule).

Next Action:
- Execute **M0** per `PHASE1_EXECUTION_PLAN.md` §3. Non-blocking: create `references.bib` (Kunimoto & Matthews 2020), add the charter scoping note (F7).

---

## 2026-06-15 (cont.) — M0 executed and sealed (Seal #1)

Worked On:
- Implemented the M0 manifest pipeline (`research/m0_manifest/m0_pipeline.py`) and ran M0 end-to-end against live TESS archives. First data-touching milestone — **catalog metadata only, no flux**.

Discoveries / Decisions:
- **Sectors S1–S3 (south) are feasible — no widening needed.** 32,960 unique SPOC 2-min TICs → **22,723** after cuts. n_sectors: 15,450 (1) / 3,841 (2) / 3,432 (3, CVZ). M0.5: every period node ≥ 500 eligible test hosts at n_tr≥2; binding **P=16 d = 5,794 test hosts**. (Owner rule: widen only if metrics demand — they don't.)
- **Leakage-safe split:** HEALPix nside=8 whole-block, seed 20260615, 30/70 → calibration 6,925 / test 15,798; **leakage audit PASS** (0 shared pixels; TIC-disjoint).
- **Seal #1 (manifest SHA-256): `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`** — deterministic across 3 runs. Provenance + TOI snapshot in `data/manifests/m0/m0_manifest_provenance.json` (tracked); bulk manifest parquet gitignored (regenerable).
- **Three faithful realizations (flagged, reversible pre-seal):**
  1. `CROWDSAP` is a per-LC FITS-header value, not a catalog field → crowding applied via TIC `contratio ≤ 0.25` (CROWDSAP≈1/(1+contratio)); literal CROWDSAP confirmed at M1.
  2. ExoFOP timed out → TOI labels from **NASA Exoplanet Archive TAP** (table `toi`): 97 confirmed-planet hosts, 224 planet/cand, 45 known-FP, 41 multi-planet, null 22,458.
  3. FP labels = TOI FP/FA dispositions (largely EBs); dedicated EB catalog (Prša et al. 2022) deferred to M1+.
- Tooling stack installed in `.venv` (astroquery 0.4.11 etc.); `pip freeze` pinned into provenance.

Artifacts created/updated:
- `research/m0_manifest/m0_pipeline.py` (M0.1–M0.6 implemented); `config/m0_config.yaml` (signed choices).
- `data/manifests/m0/`: provenance JSON + TOI snapshot + pip-freeze lock (tracked); manifest/intermediate parquets (gitignored).
- `PHASE1_EXECUTION_PLAN.md` §3.7–3.8 updated — all completion criteria ☑, Seal #1 recorded, M0 signed DONE.

Problems / Risks carried forward:
- R0-3 null-pool incompleteness (undetected planets in "null" stars) recorded — bounds H4 FAR calibration.
- Manifest table not in git (data-gitignore policy) — seal anchored to hash + provenance + TOI snapshot + pinned versions; decide later whether to archive the frozen table (release asset/DVC).

Next Action:
- Land M0 (PR #2 from `phase1/m0-setup`) and/or begin **M1** (Stage-0 conditioning on the calibration pool). TEST sealed until M4; **Seal #2** (thresholds) at M3.

---

## Template for future entries

Date:

Worked On:

Discoveries:

Questions:

Problems:

Next Action:
