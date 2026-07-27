# SESSION HANDOFF — 2026-07-27 (EOD)

> **Supersedes** `SESSION_HANDOFF_2026-07-20.md`. Assume zero chat history. Repository is authoritative; this file mirrors it.

## 1. Repository state

- **Branch `main` @ `9b12181`**, clean working tree, `main == origin/main`. **No open PRs.**
- Two PRs merged today: **#18** (Wave-0 verdict) and **#19** (Wave-1 no-compute cluster + hackathon discontinuation).
- Merged local branches deleted. Stale *remote* branches remain (`origin/phase1/audit-remediation`, `origin/phase1/wave1-robustness`, older `phase1/*`, `phase2/kepler-scaling-prereg`) — safe to prune on GitHub at leisure; not required.
- Sealed artifacts untouched all session (NN#2/P-2). TEST never re-read.

## 2. Phase / milestone

- **Phase I — audit remediation (`docs/ROADMAP_TO_10.md`).** **Wave 0 COMPLETE** (verdict resolved). **Wave 1 no-compute cluster COMPLETE**; Wave-1 compute tasks (RES-4, RES-6) remain.
- **Corrected Phase-I verdict (authoritative): E1 PASS (recall non-inferiority, robust) · E2 INCONCLUSIVE.**

## 3. Completed this session

**Wave 0 (V-1..V-5) — E2 re-measurement → verdict:**
- V-1 resume guard (`EP.pending_timing_tasks`) + 4 unit tests (`2941175`).
- V-2 frozen §6 E2 campaign, **300/300** tasks × 5 repeats / 39 hosts. **E2 = INCONCLUSIVE**: ratio **0.727** (27.3% reduction; target ≥30%), host-clustered 95% CI **[0.636, 0.826]** (straddles 0.70); ρ_d 11.6%, f_p 23.7%, π\* ≈ 0.489. Robust to a Low-Power-Mode timing window (leave-out 0.713; erratum §5.1).
- V-3 erratum §5/§5.1/§5.2/§7 filled (no PENDING markers).
- V-4 verdict propagated: paper v0.3, `M4_TEST_RESULT.md` addendum, `CLAUDE.md`, vault.
- V-5 committed/pushed/PR — **PR #18 merged** by owner.

**Wave 1 (no-compute cluster):**
- **RES-2** KM-period-weighted E1 sensitivity → E1 **robust** (ΔR̄ −0.16 pp under KM occurrence vs sealed log-uniform −0.48 pp). `data/manifests/m4/wave1/res2_*`.
- **RES-3** epoch-tolerance sensitivity → losses are epoch-predicate (loosening to ±1.0 T₁₄ → combined-side ΔR̄ ≈ 0). Combined-side only (TLS epoch not stored). `res3_*`.
- **RES-5** edge control → paper supplement **S-edge** + figure **S1** (`research/m4_evaluation/figures/S1_edge_control.png`).
- **RES-8** endpoint-disclosure paragraph (§2.6: precision not an endpoint).
- **RES-7** `docs/MONOTRANSIT_CAMPAIGN_DESIGN.md` (grid/endpoints/power; Phase-II execution).
- **PUB-6** README + `CHANGELOG.md` (v1.0.1) + `hackathon/VERDICT_CORRECTION_NOTE.md`.
- **PR #19 merged** by owner.

**Decision:** hackathon track discontinued (see §5).

## 4. Decisions made (all persisted)

| Decision | Persisted in | Authoritative? |
|---|---|---|
| E2 verdict = INCONCLUSIVE (frozen-rule re-measurement) | erratum §5/§7, `M4_TEST_RESULT.md` addendum, DR-003 outcome, CLAUDE.md, paper, README, CHANGELOG, vault | Yes (erratum + DR-003) |
| LPM-window tasks NOT re-timed (robustness check sufficed) | erratum §5.1 | Yes |
| E1 robust to KM period weighting (log-uniform not flattering) | RES-2 (`res2_*`), paper §3.1 | Yes |
| E1 loss channel is epoch-predicate | RES-3 (`res3_*`), paper §3.2 | Yes |
| Precision was not a pre-registered endpoint (disclosed) | paper §2.6 (RES-8) | Yes |
| **Hackathon track discontinued** | CLAUDE.md, README, `hackathon/{README,CLAUDE}.md` banners, vault, research log | Yes |
| `hackathon/` kept in place (not deleted/moved) | this handoff, research log, vault | Yes |
| "Phase II frozen until after hackathon" gating **void** → gated by ROADMAP + DR-004 | CLAUDE.md, vault | Yes |

**No unresolved/unpersisted decisions.**

## 5. Active blockers / risks

- **None blocking.** RES-4/RES-6 need a compute+MAST window (not a blocker, a schedule).
- **Timing-measurement hygiene** (lesson): assert **AC power + Low Power Mode off** before any CPU-second measurement (the V-2 slowdown was battery+LPM). Fold into ENG-7.
- **Data gap:** the sealed run did not persist TLS per-injection epochs → RES-3 symmetric sweep and the S-edge T₀ histogram need a small re-run (queued with RES-4/6).
- Paper Table T7 / Figure F8 still derive from the sealed 12-star run — regenerate at PUB-4 (Wave 5).

## 6. Open questions

- Compute-window scheduling for RES-4/RES-6 (+ TLS-epoch re-run) — owner to trigger.
- Prune stale remote branches? (cosmetic).
- v1.0.1 GitHub release/tag + annotating the v1.0.0 release page — owner action (outward-facing publishing; CHANGELOG.md content is ready).

## 7. Next recommended actions (in order)

1. **RES-4** — per-star τ_GP FAP sensitivity on ≥100 calibration nulls (compute; background like V-2, AC/no-LPM, workers ≤6).
2. **RES-6** — η-paid injection sub-study (MAST downloads + recondition; ~200 injections / 4 cells).
3. **TLS-epoch re-run** (small) → RES-3 symmetric sweep + S-edge T₀ histogram.
4. Wave-1 exit gate met → start **Wave 2 (math closure)** + **Wave 3 (engineering)** in parallel.
5. Phase II stays hard-gated until Waves 0–6 complete + **DR-004**.

## 8. Files requiring review

- `research/m4_evaluation/M4_ERRATUM_2026-07-19.md` §5/§7 (corrected verdict).
- `papers/phase1_evidence_first_triage.md` (v0.3 — verdict + RES-2/3/5/8 integrated).
- `data/manifests/m4/wave1/res2_*`, `res3_*` (sensitivity results).
- `docs/MONOTRANSIT_CAMPAIGN_DESIGN.md` (RES-7).
- `docs/ROADMAP_TO_10.md` (Waves 2–6 plan).

## 9. Startup prompt

See `NEXT_SESSION_PROMPT.md` (repo root, untracked).

---
*2026-07-27 EOD. Verdict resolved (E1 PASS · E2 INCONCLUSIVE); Wave-0 + Wave-1 no-compute cluster merged to `main`; hackathon discontinued. Repository safe to close: no compute running, tree clean, knowledge fully persisted in repo + vault + memory.*
