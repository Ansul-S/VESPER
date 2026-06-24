# SESSION HANDOFF — 2026-06-18 (EOD) — M4 dry-run + Finding B + methodology & governance boards

| Field | Value |
|-------|-------|
| **Purpose** | Resume TRINETRA-X with **zero reliance on chat history**. |
| **Phase** | Phase I — Scientific Validation |
| **Status** | M0–M3 done (Seal #1 + Seal #2 intact). **M4 dry-run complete; TEST UNREAD.** Finding B blocks the sealed Arm-B mechanism. Option-2 fix **conditionally approved as an amendment**; **system-level calibration result: E1 pass, E2 fail**. A **v3-as-final stopping rule** is proposed and **pending owner adoption**. **No sealed value changed.** |
| **Read first** | [`CLAUDE.md`](./CLAUDE.md) → this file → `research/m4_evaluation/M4_OPTION2_METHODOLOGY_DECISION.md` → `PHASE1_AMENDMENT_STOPPING_RULE.md` → `M4_COMBINED_ARM_RESULT.md` → `M4_DRYRUN_VALIDATION.md` |

> Authority: repository documents are authoritative; the vault mirrors them; this handoff is a pointer. Sealed documents govern on any conflict. Supersedes the mid-session handoff of the same date.

---

## 1. One-paragraph state
M0–M3 are sealed (Seal #1 data manifest `1f2d49e1…`; Seal #2 thresholds `6292c018…`). This session built the M4 harness, ran the **CALIBRATION/synthetic dry-run end-to-end** (TEST never read — hard-blocked), and discovered **Finding B**: the pre-registered Arm-B confirmation (targeted TLS, SDE≥T, single common T) is **internally inconsistent** (TLS SDE is not comparable across grid widths). Two cheaper fixes were rejected on calibration evidence; **Option-2** (an epoch-fixed folded-photometry confirmer + full-TLS fallback) was validated and, by a **methodology review board**, **conditionally approved as an *amendment*** (it satisfies Non-Negotiable #3 per MATH §6; it amends the fairness keystone). A **combined-arm system dry-run** on calibration gave **E1 PASS / E2 FAIL** (the E2 shortfall is structural, rooted in the sealed B=1000 FAP overhead). A **governance review board** proposed making **v3 the final permissible amendment** with an explicit stopping rule. **Nothing is sealed/changed; TEST is untouched; the next step is owner adoption of the stopping rule + an NN#3 ruling.**

## 2. Integrity (verified this session)
- Seal #2 hash == `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692` ✓
- `git diff phase1-prereg-v2` on the 3 sealed docs = **empty** ✓
- **0 TEST TICs** across all `data/manifests/m4/dry_run/*.csv` ✓ (TEST split never read)
- Branch `main` @ `2f2ed05` (no commits this session; all work is **untracked** working files).

## 3. Findings
- **Finding A (implementation, fixable):** `transitleastsquares.grid.period_grid` discards the `[P̂(1±ε)]` window when it holds < `MINIMUM_PERIOD_GRID_SIZE=100` periods and returns the full grid. At sealed ε=0.01 a ±1% window holds ~20–35 periods → the "targeted" arm secretly ran a full search (cost ratio 0.995). Feeding the in-window periods directly → real saving (1.7 s vs 164 s). No sealed-value impact.
- **Finding B (methodology, BLOCKING):** TLS **SDE is normalized across the searched grid**, so a narrow-grid SDE (e.g. 3.55) is not comparable to the full-grid SDE (40.36) that calibrated T=10.74. The sealed "targeted TLS, SDE≥T, single common T both arms" rule is internally inconsistent → Arm B would reject planets Arm A accepts. The targeted-TLS realization is **non-executable**.

## 4. Resolution path + system result
- Option 1 (per-arm narrow-SDE T_B): **rejected** (AUC 0.43, no separation). Option 3 (wider window): **rejected** (AUC ≤0.72; comparability and savings mutually exclusive).
- **Option 2 — epoch-fixed folded-photometry confirmer** (evidence-first P̂ + t̂₀; no period grid → range-invariant): validated on the cleaned 854-null pool (AUC 0.877, FAR-controllable).
- **Combined-arm system dry-run (CALIBRATION; route→confirm→full-TLS fallback):** **E1 PASS** (ΔR̄ = −0.39 pp, one-sided 95% lo −0.80 pp). **E2 FAIL** (combined/full = 0.799 → ~20% reduction; population estimate ~29%; both < 30%). Structural cause: **ρ_d ≈ 12.4%** (sealed B=1000 block-bootstrap FAP charged on every routed star) + **59% of routed stars fail the FAP gate** → full-TLS fallback. **T_red = 0 (degenerate)** — the FAP gate, not the MF, does FP rejection.

## 5. Board decisions (this session)
- **Methodology board → APPROVE (conditional).** Option-2 is the *same experiment, amended*, not a different one. Basis: MATH §6 admits "the transit-fit SNR" as an arbiter form, so a folded-photometry significance satisfies **NN#3** (photometry, not timing coherence; repairs all four v3 errors). It **amends the fairness keystone** (A6) from "same TLS engine both arms" → "common false-alarm rate". Conditions: (1) arbiter must be a genuine **transit likelihood-ratio** (the dry-run's box depth-SNR is borderline — NN#3 stands or falls here); (2) re-register the keystone change transparently; (3) anti-tuning discipline. **Principle survives; targeted-TLS realization does not.** (`M4_OPTION2_METHODOLOGY_DECISION.md`.)
- **Governance board → propose v3 = FINAL amendment + stopping rule P-1…P-9.** Amendment (pre-TEST defect fix) vs tuning (outcome-driven, forbidden by NN#2 — incl. on calibration). After v3 no known defect compels change, so any v4 would be outcome-driven → unfalsifiability/creep. Pre-commit outcomes before TEST; one evaluation; failure → pre-committed falsification (no v4); new ideas → new pre-registered experiments. (`PHASE1_AMENDMENT_STOPPING_RULE.md`.) **Pending owner adoption.**

## 6. Pre-committed TEST-outcome mapping (proposed, to be sealed before TEST)
- **E1 fail** (ΔR̄ lower bound < −2 pp) → recall falsification → **H1 FALSIFIED**; negative Phase I; do not proceed to Phase II on the routing-recall claim.
- **E2 fail** (<30% reduction at non-inferior recall) → compute falsification → **H1 FALSIFIED** (compute branch). (A near-zero *survey-representative* figure is expected and does NOT count.)
- **Inconclusive** (CI wider than margin) → not a pass; pre-planned injection-count increase only (truth/thresholds fixed). No amendment.

## 7. Active blockers
1. **Finding B blocks M4** — the sealed Arm-B mechanism is non-executable. M4 cannot run until a v3 amendment is sealed.
2. **Governance gate** — the v3-as-final stopping rule is proposed but **not adopted**; per project discipline, adopt it (and pre-commit outcomes) **before** any re-registration drafting.
3. **NN#3 condition (methodology condition #1)** — owner must rule whether a folded-photometry transit likelihood-ratio is an acceptable physics arbiter. If not, the verdict flips to REJECT and §8-of-the-decision (a narrow negative result) becomes the outcome.

## 7b. E2-fix R&D (2026-06-18, EXPLORATORY — CALIBRATION-only, NOT adopted, no seal change)
Diagnosed the E2 failure and validated a fix candidate:
- **Root cause:** the sealed **B=1000 period-FAP** (ρ_d≈12%, on every routed star) + 59% FAP-gate fallback. A *configuration* cost, not a property of the principle.
- **Margined white-noise pre-filter** (skip the bootstrap when a cheap white-noise FAP already exceeds a margin): validated on 100 injected planets (B=1000). The **bare** "reject if white-FAP > α" **loses ~5% of real planets**; but **white-FAP > 5.5·α clips ZERO recoverable planets** while still skipping the bootstrap on **97.5% of noise** → ρ_d→~0 → projected **E2 ~25%→~40% (PASS)**. (Premise check: per-star "white ≤ red" holds only 18.3%, corr 0.868 — so it's a *margined heuristic*, not a proof.)
- **Conclusion: E2 is fixable, not a fundamental falsification.** Strengthens the "salvage" side of the decision.
- **Governance:** the fix touches **sealed A.8 (period-FAP)** → adopting it **expands the v3 scope** beyond the Option-2 confirmer and bumps the v3-as-final rule. Owner must decide v3 scope.
- Caveats: margin from n~40 red-passers on strong cells (P≤4 d, R≥2) — use a buffer (~6–8·α) and re-validate on a larger, full-grid injection set; margin is statistic-specific.
- Artifacts: `research/m4_evaluation/validate_prefilter{,_injections}.py`, `data/manifests/m4/dry_run/prefilter_*.csv`.

## 8. Open questions
- Does a true transit-template likelihood-ratio (not the box depth-SNR) satisfy §6 as physics AND keep the cheap cost? (Confirmer-integrity, condition #1.)
- **v3 scope:** confirmer-only, OR confirmer + the period-FAP cheapening (the E2-fix, which re-opens sealed A.8 — a *larger* amendment that may breach v3-as-final)? Owner call.
- The margined pre-filter's exact margin needs locking on a larger/full-grid injection set (5.5·α is from n~40).

## 9. Risks
- **R-1 (compute external validity) — now measured and live:** ρ_d ≈ 12% + 59% FAP-gate fallback push E2 below 30%; the shortfall sits in sealed machinery.
- **Anti-tuning / amendment creep** — mitigated by the proposed stopping rule; must be adopted before drafting.
- **Single-shot M4** — one TEST evaluation against sealed v3; must be right.
- **Compute logistics** — full TLS 30–180 s/LC; the full ≥15k-injection campaign is a multi-day parallel job (use the M3 `Pool`/`imap_unordered` pattern).

## 10. Next recommended actions (in order)
1. **Owner: adopt** (or revise) the **v3-as-final stopping rule (P-1…P-9)** and the §6 outcome mapping.
2. **Owner: rule on NN#3 condition #1** (folded-photometry transit-LR as physics arbiter).
3. **Owner: decide v3 SCOPE** — confirmer-only, OR confirmer + period-FAP cheapening (the §7b E2-fix; re-opens sealed A.8, bigger amendment, bumps v3-as-final).
4. **If approved:** draft **DR-002** (Finding B, Option-2 amendment, stopping rule, outcome mapping) + **VAL v3 / MATH v1.2** governance + the **T_red calibration plan** (full cleaned null pool, FAR≤1%/star) + (if in scope) the **margined pre-filter plan** → **Seal #2b**, sealed **before** the single TEST run.
5. **Then M4:** the one sealed-TEST run against v3 → E1/E2 → pre-committed verdict.
- **If owner rejects condition #1:** write up the **narrow negative result** (targeted-TLS realization infeasible; principle untested) per the methodology decision §8. (Note: §7b shows compute is *fixable*, so a negative result would be a choice to stop, not a forced falsification.)

## 11. Files to review on resume
- **Governance/decisions:** `research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md`, `M4_OPTION2_METHODOLOGY_DECISION.md`, `M4_OPTION2_REVIEW_BOARD.md`.
- **E2-fix R&D:** `research/m4_evaluation/validate_prefilter.py`, `validate_prefilter_injections.py`; `data/manifests/m4/dry_run/prefilter_validation.csv`, `prefilter_injection_safety.csv`.
- **Results:** `M4_COMBINED_ARM_RESULT.md`, `M4_EPOCH_FIXED_DIAGNOSTIC.md`, `M4_FINDING_B_METHODOLOGY_REVIEW.md`, `M4_DRYRUN_VALIDATION.md`; data in `data/manifests/m4/dry_run/`.
- **Harness (no sealed change):** `research/m4_evaluation/` (`seal_loader.py` guards TEST + verifies Seal #2; `arms.py`, `injection.py`, `recovery.py`, `endpoints.py`, `combined_arm_dryrun.py`, `epoch_fixed_diagnostic.py`).
- **Plan:** `PHASE1_M4_PLAN.md`.
- **Sealed (read-only):** `docs/SCIENTIFIC_HYPOTHESIS.md` v2.0, `docs/TRINETRA_X_PHASE1_VALIDATION.md` v2, `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` v1.1.

## 12. Recommended startup prompt
See [`NEXT_SESSION_PROMPT.md`](./NEXT_SESSION_PROMPT.md) (also reproduced in the EOD status report).

---

*Handoff generated 2026-06-18 (EOD). M0–M3 done; Seal #1 + Seal #2 intact; M4 dry-run complete; TEST unread; Finding B blocks M4; Option-2 conditionally approved (amendment); E1 pass / E2 fail on calibration; v3-as-final stopping rule pending adoption; no re-registration begun.*
