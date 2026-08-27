# SESSION HANDOFF — 2026-07-28 (EOD)

> **Supersedes** `SESSION_HANDOFF_2026-07-27.md`. Assume zero chat history. Repository is authoritative; this file mirrors it.

## 1. Repository state

- **`main` @ `77037d4`**, clean, `main == origin/main`. CI (`fast-units`) green, 16 tests pass.
- **PR #21 MERGED** (7 commits: RES-4 + MATH-1/5/6/7 + CODE-7 + DOC-2/3); branch deleted.
- **PR #22 OPEN** — `phase1/sync-2026-07-28`, documentation-only sync (CLAUDE.md status bullet + vault). Not merged; awaiting owner.
- Sealed artifacts untouched all session. `git diff phase1-prereg-v3` over the three sealed docs = **0 differing lines** (brand-normalized), re-verified after the merge. `verify_seal()` → z⋆=3.4 · z_mono=5.3 · N_min=2 · T=10.741 · α=0.01 · B=1000. TEST never read.
- No compute running. `data/raw` empty (RES-6 will need MAST; MAST reachable, HTTP 200).

## 2. Phase / milestone

- **Phase I — audit remediation** (`docs/ROADMAP_TO_10.md`). Wave 0 ✅ · Wave 1 **all but RES-6 + TLS-epoch re-run** ✅ · Wave 2 **half** ✅ · Wave 3 (CODE-7 only) · Wave 4 (DOC-2/3 only).
- **Corrected Phase-I verdict (unchanged today): E1 PASS (robust) · E2 INCONCLUSIVE.**

## 3. Completed this session

**RES-4 (Wave 1) — the compute task.** Per-star τ_GP FAP sensitivity on **all 1163** cached calibration nulls (1126 with ≥2 events), both arms × 3 T₁₄ strata, ~3.2 h on 6 workers, AC power / LPM off.

| Arm | Gate flips at sealed T₁₄ = 0.2 d | Wilson 95% |
|---|---|---|
| B — as the post-audit driver applies it | **0 / 1126** | [0, 0.0034] |
| C — complete per-star coverage | **1 / 1126** | [0.0002, 0.0050] |

Sealed fidelity **bitwise 968/968** (max |Δ| = 0.00e+00), arm-aware. Four findings:
- **F1** erratum §2.4's masking argument is empirically upheld, bounded <0.5%.
- **F2 (new)** §2.4's *premise* is imprecise — `m3_calibrate.py:151` falls back to 0.005 for any star lacking an M1 noise-summary row, and only **22 of 968** overlapping stars had one. M3 was itself overwhelmingly flat-τ, so the calibration/test gap is much smaller than that section implies.
- **F3 (new)** the lone flip runs flat-OPEN → per-star-SHUT (TIC 80427281, τ = 0.289 d): the sealed gate was slightly *more permissive* on red-noise nulls — the benign direction.
- **F4 (new)** the masking is bought by the **T₁₄ = median(duration grid) convention**, not by τ being harmless (24/1126 flips at a counterfactual T₁₄ = 0.05 d). Any future run that duration-matches T₁₄ **must** use per-star τ.

**Wave 2 (math closure) — 4 of 8 tasks.**
- **MATH-1** π⋆ derived = **ρ_d/(f_p(1−ρ))**. Code and paper were already correct; the **roadmap's "exact form" ρ_d/(f_p(1−ρ+ρ_d)) is wrong** (it implies a routed star isn't charged for the detector that routed it). A **tautological unit test** — it asserted `x == x` — was replaced with one that pins the derived form and rejects both alternatives.
- **MATH-5** BCa host-cluster lo95 **−1.04 pp** vs sealed percentile **−0.83 pp** (a = −0.133; effective tail 0.05 → 0.0072). Sealed interval is mildly optimistic; **both clear the −2 pp margin, E1 unchanged.**
- **MATH-6** N=2 comb degeneracy proven + measured. **"argmin → longest-P" is only ~74% true** — the tie is broken by IEEE-754 rounding at ~1e-16, not by design. Sealed m∈{2,3} tolerance absorbs 98.1–98.6%; 1.4–1.9% leak to m≥4 as recall costs, never FPs. **New:** at N=2, R saturates at 1, so the period-FAP tests event *rarity*, not coherence (reads with erratum §2.9).
- **MATH-7** notation cross-reference (MATH ↔ code ↔ paper ↔ units), 5 tables.

**Wave 3 / 4 (partial).** **CODE-7** cluster bootstrap vectorized, bit-exact vs `endpoints.e1_recall`. **DOC-2** `docs/INDEX.md`. **DOC-3** `docs/SEAL_CHAIN_POSTMORTEM.md`.

**Two errors self-caught and fixed before shipping** (both worth remembering):
1. The first RES-4 draft imported the **live** `detector.py`, which carries the 2026-07-19 gap-aware fix and does **not** reproduce sealed FAPs. Switched to `frozen_rerun/` (the `e2_retiming.py` convention).
2. The sealed-fidelity check compared arm A everywhere and reported a spurious 967/968 with |Δ| = 5.9e-02. M3 used per-star τ on the 22 stars with M1 rows, so the faithful comparison is arm-aware → **968/968 bitwise**. The generated conclusion now degrades to an explicit failure statement if reproduction is ever incomplete.
3. RES-4 originally held results only in memory (the paused-E2-campaign failure mode) → relaunched with an append-only resume ledger (gitignored scratch).

## 4. Decisions made (all persisted)

| Decision | Persisted in | Authoritative? |
|---|---|---|
| RES-4 runs the **frozen** code path, not live | `res4_tau_fap_sensitivity.py` docstring + commit `28b7714` | Yes |
| Sealed-fidelity comparison is **arm-aware** | same script + `res4_*.json` `sealed_reproduction_check` | Yes |
| RES-4 resume ledger is **gitignored scratch** (result = `res4_per_star.csv`) | `.gitignore` + commit | Yes |
| Post-seal math goes in a **companion doc**, never inlined into sealed MATH | `docs/VESPER_MATH_ADDENDUM.md` header + §0 rationale | Yes |
| π⋆ = ρ_d/(f_p(1−ρ)); roadmap's "exact form" **rejected** | addendum §C, `endpoints.py` note, unit test | Yes |
| MATH-5 BCa is **reported alongside**, does not re-decide the sealed E1 rule | addendum §D + `math5_*.json` `scope` | Yes |
| PR #21 **merged** (owner instruction) | git history, PR #21 | Yes |

**Unresolved / not decided — see §6.**

## 5. Active blockers / risks

- **None blocking.** RES-6 needs a MAST + compute window (a schedule, not a blocker).
- **Data gap (carried):** the sealed run did not persist TLS per-injection epochs → RES-3's symmetric sweep + the S-edge T₀ histogram still need the small re-run.
- **Carried:** paper Table T7 / Figure F8 still derive from the sealed 12-star run — regenerate at PUB-4.
- **Risk (new, strategic):** `docs/ROADMAP_TO_10.md` is ~50 working days and includes a production CLI, container, API docs, and a reusable seal library — substantial engineering for a result whose own conclusion is that the architecture should not be deployed. Scope is materially larger than the scientific payload. **See §6.**
- **Known, unchanged:** E1's pass is partly structural (erratum §2.8 — 78.9% fallback where `rec_comb` is copied from `rec_tls`; 30.3% of weight in cells with 0.000 recall in both arms). Any use of E1 must carry that framing.

## 6. Open questions — **the significant one is new and strategic**

**⚠️ OPEN DECISION: project scope and the shape of the paper.** The owner asked directly whether the project is worth continuing. The assistant's recommendation, **offered and discussed but NOT accepted, rejected, or decided**:

1. **Finish Phase I — roughly two weeks.** RES-6 (the last real scientific gap: absolute recall is optimistic because neither arm paid the conditioning cost η), fix the paper, submit. The work is ~90% done; abandoning converts it to zero output.
2. **Cut `ROADMAP_TO_10.md` Waves 3 and 6** (package, CLI, container, API docs, seal library). None of it changes a number in the paper; it optimizes an invented ten-category scorecard rather than a deliverable.
3. **Do not start Phase II on momentum** — make it a separate decision after submission.
4. **Reframe the paper.** The routing result is thin on its own (π⋆ ≈ 0.49 vs π ≈ 0.03 is close to a-priori derivable, and a referee may say so). The stronger contribution is the **methodology**: sealed single-shot validation with pre-committed verdicts, demonstrated by a case in which the protocol *forced the authors to withdraw their own headline verdict* (E2 FAIL → INCONCLUSIVE), plus the 40-vs-80 host bug and the 19-day seal-chain break, all self-found and published. That corresponds to roadmap **INN-1**, currently scheduled last in Wave 6 — the recommendation is to promote it to the primary deliverable.

**This is the first thing to settle tomorrow.** If accepted, it warrants a decision record (next free ID: **DR-005**; DR-004 remains reserved for the Phase-II gate) and an amendment to `docs/ROADMAP_TO_10.md`. Until then the roadmap stands as written.

Other open questions (carried, minor): prune stale remote branches; v1.0.1 GitHub release/tag (CHANGELOG content ready).

## 7. Next recommended actions (in order)

1. **Settle the §6 scope decision** — it changes everything below it. Record as DR-005 if accepted.
2. **Merge PR #22** (documentation-only sync) or close it if the §6 decision rewrites the status text first.
3. **RES-6** — η-paid injection sub-study: raw-mode injection + recondition, ~200 injections / 4 cells, calibration only. Needs MAST (`data/raw` is empty). `injection.build_injection(host_mode="raw")` and `m2_pipeline.inject_measure` already implement the path. Run on AC power, LPM off, workers ≤6.
4. **TLS-epoch re-run** (small) → unlocks RES-3's symmetric sweep + the S-edge T₀ histogram.
5. Then either (a) the reduced path — PUB-1/2/4/7 + INN-1 → submit, or (b) the roadmap as written, depending on §6.

## 8. Files requiring review

- `data/manifests/m4/wave1/res4_tau_fap_sensitivity.md` — RES-4 result + four findings.
- `docs/VESPER_MATH_ADDENDUM.md` — §A MATH-6, §B MATH-7, §C MATH-1, §D MATH-5.
- `docs/INDEX.md` — document taxonomy + reading paths (DOC-2).
- `docs/SEAL_CHAIN_POSTMORTEM.md` — the rebrand incident (DOC-3).
- `docs/ROADMAP_TO_10.md` — **read with §6 above in mind**; its MATH-1 "exact form" is now known wrong.
- PR #22 diff (CLAUDE.md + vault).

## 9. Startup prompt

See `NEXT_SESSION_PROMPT.md` (repo root, untracked/gitignored).

---
*2026-07-28 EOD. RES-4 complete and merged; Wave-2 half done; Wave-3/4 partially opened. No compute running, tree clean, seals verified. **One significant open decision carried into tomorrow (§6): project scope and the shape of the paper.***
