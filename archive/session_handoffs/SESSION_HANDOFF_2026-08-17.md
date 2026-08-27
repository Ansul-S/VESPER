# SESSION HANDOFF — 2026-08-17

> Supersedes `SESSION_HANDOFF_2026-07-28.md`. That handoff's §6 open scope decision is **still open** and still first in line — see §6 below.

## 1. Repository state

- Branch **`phase1/inn3-fap-acceleration`** (created this session from `phase1/sync-2026-07-28`). **Local only — not pushed, not committed unless the owner asks.**
- `main` == `origin/main` @ `77037d4`. **PR #22 (doc-only sync) still open and unmerged** from 2026-07-28.
- **Nothing sealed was touched.** `git diff main -- docs/SCIENTIFIC_HYPOTHESIS.md docs/VESPER_PHASE1_VALIDATION.md docs/VESPER_MATHEMATICAL_FOUNDATIONS.md data/manifests/m3 data/manifests/m4/test_run research/m4_evaluation/frozen_rerun` → **empty**.
- No TEST light curve was read (P-5 intact). No network access. Calibration caches only.

## 2. Phase / milestone

Phase I remains **COMPLETE / SEALED / FINAL**, verdict **E1 PASS (robust) · E2 INCONCLUSIVE**. This session was post-seal analysis. Roadmap **INN-3** (scheduled Wave 6) is now delivered, ~5 waves early, with its proof obligations *discharged* rather than stated.

## 3. Completed this session — INN-3

The single mathematical obstacle behind the failed compute branch was the $B{=}1000$ block-bootstrap period-FAP "entry tax" ($\rho_d = 11.6\%$). DR-002 / `LEVER1B_EQUIVALENCE_RESULT.md` recorded it as **"not a removable artifact"** after both pre-registered cheap estimators (E-EVT, E-LUT) failed the equivalence gate 3/3. **That is correct about the estimator and wrong about its cost.** Both candidates tried to approximate the null distribution; the tax was never in the distribution.

| Lever | What it is | Gain | Exactness |
|---|---|---|---|
| **A** | Hoist the loop invariants + vectorise the scans. `np.median(np.diff(np.sort(t)))` (`detector.py:26,55`) is **49% of the entire FAP cost** — 10,000 full sorts of an N-vector per star, all the same constant, because the bootstrap resamples the *flux* and never touches the epochs. | **6.31×** | **bit-identical** |
| **B** | Exact curtailment. $(g_e{+}1)/1001\le0.01 \iff g_e\le9$, and $g_e$ is monotone → the **10th exceedance decides the gate**. | **73.2×** on nulls, 12.7× on injections (cumulative) | decision identical **with probability 1**; one-sided, so it cannot clip a planet |

**Equivalence, measured:**

- **1126 / 1126** cached calibration nulls reproduce the sealed recorded exceedance count (max |Δ| = **0**); gate identical at full $B$ and curtailed.
- **60 / 60** agreement against a live re-run of the sealed `period_fap`.
- **149 / 149** calibration injections reproduce the sealed FAP **bitwise**.
- All three sealed Lever-1b criteria met with **exact zeros**: p95 |ΔFAP| **0.000** (threshold ≤ 0.005) · **0** discordant, **0** nulls admitted (thresholds ≤ 8, 0) · **0** recoveries clipped.

**E2 counterfactual** — arithmetic on `data/manifests/m4/e2_retiming/timing_ledger_full.csv` and the sealed `data/manifests/m4/test_run/recovery.csv`; **no TEST light curve re-read**:

| | ratio | reduction | $\rho_d$ | $\pi^\star$ | 95% host-cluster CI | decision |
|---|---|---|---|---|---|---|
| as recorded | 0.727 | 27.3% | 11.6% | 0.489 | [0.636, 0.826] | INCONCLUSIVE |
| lever A | 0.630 | 37.0% | 1.82% | 0.077 | [0.540, 0.722] | INCONCLUSIVE |
| **lever A+B** | **0.620** | **38.0%** | **0.86%** | **0.036** | **[0.532, 0.710]** | INCONCLUSIVE |
| free-detector limit | 0.612 | 38.9% | 0 | 0 | [0.522, 0.703] | INCONCLUSIVE |

**The second finding is the one to carry forward.** Even a **free** detector leaves the frozen-rule decision INCONCLUSIVE. **E2's INCONCLUSIVE is a variance result, not a cost result** — between-host variance at $H=39$ clusters. The two causes are separable and both were necessary:

- the **entry tax** put the point estimate out of reach at *any* host count (as-recorded numbers stay INCONCLUSIVE even at $H=100$);
- the **erratum §2.1 host-parity bug** (40 of 80 hosts drawn; 39 in the E2 subset) made the interval too wide at *any* cost;
- **remove both and E2 PASSES at $H=79$** — the host count `m4_driver` was written to use. Hosts needed: **49** (lever A+B) · 65 (lever A) · 41 (free detector) · **never** (as recorded).

This promotes §2.1 from an E1 noise-diversity concern to a **causal contributor to the undecided compute verdict**.

**Side finding (real, small in effect).** `m4_driver.py:117` initialises `t14 = median(duration_grid)` but **line 120 overwrites it** with the seeded event's own duration before the FAP call on line 126 (`e2_retiming.py:67` faithfully replicates this; `m3_calibrate.py` genuinely does use 0.2 d). So the M4 arm **duration-matched** $T_{14}$: RES-4's "counterfactual" 0.05/0.1 d strata are the *realised* ones for M4 and its primary 0.2 d stratum is not. Measured seeded $T_{14}$ over the same 1126 nulls: 0.05 d 61.5% · 0.1 d 17.9% · 0.2 d 9.9% · 0.4 d 6.0% · 0.8 d 4.6%. Folding RES-4's own per-stratum arm-C flip counts through that mixture gives an M4-realised exposure of **≈1.4%** against the **0.09%** RES-4 reports (~16×), and τ moves $L_b$ on 4.7% of stars rather than 2.8%. **RES-4's conclusion survives; its stated mechanism and stratum labelling do not.**

**Implementation-parity bound.** Arm A's `transitleastsquares` is numba-JIT-compiled; Arm B was interpreted numpy, so the sealed CPU-seconds ratio was partly comparing implementations. A numba port of the whole surrogate loop reproduces $g_e$ exactly and is only **1.4–1.7×** faster than the vectorised numpy — ≲2× of the routing cost is language, and the 6.31× is removal of work that was never needed.

**Deliverables:**

| File | Role |
|---|---|
| `research/m4_evaluation/INN3_FAP_ACCELERATION.md` | result record (read this first) |
| `research/m4_evaluation/fast_period_fap.py` | the exact accelerated estimator |
| `research/m4_evaluation/inn3_fap_acceleration.py` | validation campaigns (`nulls` / `injections` / `survey` / `project`) |
| `research/m4_evaluation/nb_period_fap.py` | numba parity probe (measurement instrument, not the recommended estimator) |
| `tests/test_inn3_fap_acceleration.py` | 9 float64-equality equivalence tests, green |
| `docs/VESPER_MATH_ADDENDUM.md` §E | curtailment proposition + proof; the integer-boundary form of the gate |
| `data/manifests/m4/inn3/` | artifacts (nulls, injections, survey, E2 counterfactual + host-power) |

## 4. Decisions made

**None binding.** No threshold, weight, estimator of record, seal or verdict was changed. Everything in §3 is analysis; every downstream adoption is left to the owner (§6).

## 5. Active blockers / risks

- The 2026-07-28 **scope decision is still unmade** and still gates everything else.
- The §6.1a host-power table resamples $H>39$ from the 39 observed hosts, so it assumes they represent the pool. It is a **design calculation, not a measurement**, and cannot re-decide the sealed run (P-2).
- Work is uncommitted on a local branch; PR #22 is still open.
- RES-6 (η-paid injection; needs MAST, `data/raw` empty) and the small TLS-epoch re-run remain the last queued compute.

## 6. Open questions

1. **The 2026-07-28 scope + paper-framing decision — unchanged and first in line.** INN-3 strengthens the methodology framing: the protocol has now forced a *second* self-correction, this time of a published "not removable" claim, by the project's own machinery.
2. **Adopt `fast_period_fap` as the estimator of record for future runs?** MATH §9.1a permits a substitution "provided it is numerically equivalent to the reference"; here the equivalence relation is the identity map at full $B$ and provable decision-identity under curtailment. Needs a decision record: **DR-006 or later** (DR-004 reserved for the Phase-II gate, DR-005 for the scope decision).
3. **Does the §6 counterfactual + §6.1a two-cause diagnosis go in the paper?** It is the strongest available answer to "was your compute result an artifact of your implementation?" — *partly yes, and here is exactly how much* — and it converts "INCONCLUSIVE" from a dead end into a design parameter (49 hosts).
4. **Does §7.1 warrant a formal RES-4 addendum**, or is a cross-reference from the RES-4 artifacts enough?

## 7. Next recommended actions (in order)

1. Settle the scope decision (§6.1). Record as DR-005 if accepted.
2. Read `research/m4_evaluation/INN3_FAP_ACCELERATION.md` §0 and §6.1a; rule on §6.2–§6.4 above.
3. Commit + push `phase1/inn3-fap-acceleration`, open a PR (nothing here needs to merge before the scope call, but it should not sit uncommitted).
4. RES-6 (η-paid injection, MAST) + the TLS-epoch re-run — the last queued Phase-I compute.

## 8. Files requiring review

`research/m4_evaluation/INN3_FAP_ACCELERATION.md` (esp. §0, §6.1a, §7.1) · `docs/VESPER_MATH_ADDENDUM.md` §E · `research/m4_evaluation/fast_period_fap.py` · `CLAUDE.md` (new INN-3 status bullet) · `vault/00_Home/{Current_Mission,Dashboard}.md` · `vault/01_Research_log/Daily_Research_Log.md` (2026-08-17 entry).

## 9. Startup prompt

> Read `CLAUDE.md`, then `archive/session_handoffs/SESSION_HANDOFF_2026-08-17.md`, then `research/m4_evaluation/INN3_FAP_ACCELERATION.md`. Phase I is sealed and final (E1 PASS · E2 INCONCLUSIVE); INN-3 is post-seal analysis on the local branch `phase1/inn3-fap-acceleration` and changes no sealed artifact. Two owner decisions are open and unmade: the 2026-07-28 project-scope/paper-framing call (first in line) and whether to adopt `fast_period_fap` as the estimator of record. Do not start Phase II (hard-gated behind DR-004). Do not read the TEST split.
