# DECISION RECORD — DR-003: Audit Remediation & the E2 Re-measurement

| Field | Value |
|-------|-------|
| **ID** | DR-003 |
| **Date** | 2026-07-19 |
| **Status** | ADOPTED (owner instruction 2026-07-19: "full fix for this project — everything in the audit — before moving to Phase 2") |
| **Authority** | Owner instruction = the sign-off for every action in this record. Extends DR-001/DR-002; **changes no sealed value, threshold, statistic, weight, or document** (NN#2, P-2). |
| **Trigger** | Independent full-repository technical audit (2026-07-19), findings recorded in [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](../../research/m4_evaluation/M4_ERRATUM_2026-07-19.md). |

---

## 1. The problem this record resolves

The sealed TEST evaluation (2026-06-24) recorded the pre-committed verdict
**"H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL)."** The audit found that the E2
component of that verdict was not produced by the protocol the owner had frozen:

1. **The frozen timing rule was not followed.** `PHASE1_M4_PLAN.md` §6 (owner-confirmed
   2026-06-18, *before* the TEST read) froze the E2 measurement procedure: *stratified
   ≥10 fast-path-eligible LCs per occupied (P, Rₚ) cell, capped at 300, seed 20260616,
   ≥5 warm-cache repeats, single-thread CPU-core-seconds*. The sealed run instead used
   the driver defaults — **12 stars, one wall-clock repeat each**.
2. **The verdict is statistically undecided at that sample size.** A bootstrap over the
   sealed `timing_ledger.csv` gives a 95% CI on the compute ratio of **[0.42, 1.14]**
   (P(reduction ≥ 30%) ≈ 0.37). VAL §5's own decision rule contains an INCONCLUSIVE
   branch for exactly this case ("the CI on ΔR̄ **or on E2** is too wide to decide");
   the sealed tooling never computed an E2 interval, so that branch could not fire.

The recorded compute-branch falsification therefore reflects a **procedural deviation**,
not a protocol outcome.

## 2. Decision

**D1 — Re-measure E2 by executing the frozen §6 timing rule, exactly, on the already-read
TEST injection set.** Tooling: `reconstruct_m4_tasks.py` (deterministic reconstruction of
the sealed 15,000-task list from the frozen seeds, validated cell-by-cell against the
sealed `recovery.csv`) + `e2_retiming.py` (frozen-module snapshot `frozen_rerun/`, sealed
configuration reproduced verbatim: flat τ_GP = 0.005, confirmer u₂ = 0.25, T_red = 0,
B = 1000 bootstrap FAP). Decision taken on the bootstrap CI per VAL §5:
CI-high ≤ 0.70 → PASS · CI-low > 0.70 → FAIL · else → INCONCLUSIVE.

**Why this is not a second TEST read (P-5).** The single sealed evaluation already read
every host light curve and every injection consumed here; the reconstruction reproduces
that same set (validated: identical host multisets and routed counts per cell). The
re-measurement extracts **no new scientific information from unread data** — it re-runs
already-evaluated computations under a stopwatch. What changes is the *precision of the
cost measurement*, which VAL A.7/§6 always specified and the sealed run under-delivered.
This is the same category as the sanctioned §6 "pre-planned sample-size increase, truth
and thresholds unchanged" that the sealed protocol prescribes for an inconclusive CI.

**D2 — E1 stands, with a corrected uncertainty statement.** The audit found the E1 CI
ignored host clustering (all 15,000 injections share **40** noise realizations — see D4)
and that the pre-registration named a Wilson/Clopper–Pearson combination the code did not
implement. Re-analysis (`e1_corrected_inference.py`) reports all three constructions:
injection bootstrap **−0.60 pp**, host-cluster bootstrap **−0.82 pp**, Wilson-weighted
combination **−0.60 pp** — every one clears the sealed −2 pp margin. **E1 PASS is robust.**

**D3 — The recorded verdict line is superseded as follows:** "E1 PASS" is unchanged;
"E2 FAIL → H1 FALSIFIED (compute branch)" is replaced by the outcome of D1, recorded in
the erratum and in an addendum appended to `M4_TEST_RESULT.md` (the original text is
preserved unedited above the addendum; sealed documents and tags are untouched).

**D4 — Defect disclosures (full register in the erratum):** the host-assignment stride
bug (40 of 80 drawn hosts used), residual-space injection (η paid by neither arm),
constant LD (u₂ mismatch), flat τ_GP, formula-level n_transits, and the π\* definition
error are disclosed and fixed in code **for future runs**; no sealed artifact is edited.

**D5 — Independent controls:** a CALIBRATION-only grid-edge control (`edge_control.py`)
tests whether the P = 0.5 d "gain region" is a TLS grid-boundary artifact (the injected
period equals the sealed grid's period_min).

## 3. What this record does NOT do

- It does **not** amend the protocol (no v4; P-2 stands). No threshold, grid, weight,
  statistic, or sealed document changes.
- It does **not** re-run recovery, re-tune anything, or alter E1's estimand.
- It does **not** touch `hackathon/` (submitted 2026-07-01) or `archive/`.

## 4. Outcome

Recorded in [`M4_ERRATUM_2026-07-19.md`](../../research/m4_evaluation/M4_ERRATUM_2026-07-19.md)
§5 after the campaign completes, and mirrored in the `M4_TEST_RESULT.md` addendum,
`CLAUDE.md` status, and the paper draft.

---

*DR-003, 2026-07-19. Owner-instructed remediation; seals intact; TEST information set unchanged.*
