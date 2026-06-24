# M4 — Single Sealed-TEST Result (Phase I primary endpoints E1 / E2)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-24 |
| **Status** | **COMPLETE — the single irreversible TEST read was executed once (P-5) and the pre-committed verdict applied.** |
| **Verdict** | **H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** A legitimate, successful negative Phase I. |
| **Protocol** | Sealed v3 (`phase1-prereg-v3`); confirmer-only. No sealed value, threshold, statistic, or config changed (NN#2 / P-2). |
| **Authority** | Pre-committed outcome mapping VAL §7a / DR-002 §2.1. This document records the *result*; it is not an amendment. |

> Per CLAUDE.md "documents are memory." This is the authoritative record of the Phase-I primary result. The sealed specs (VAL v3 / MATH v1.2 / HYP v2.1) and manifests are unchanged; the TEST split was read exactly once.

---

## 1. Headline

The evidence-first router, evaluated once on the sealed TEST split (15,000 injections, 30 (P, Rₚ) cells × 500, the literal pre-registered ≥500/cell scale), **preserves recall but does not reach the pre-registered ≥30 % compute saving.**

| Endpoint | Definition (sealed) | Result | Decision |
|---|---|---|---|
| **E1 — recall non-inferiority** | occurrence-weighted ΔR̄ with one-sided 95 % lower bound ≥ −2 pp | ΔR̄ = **−0.48 pp**, lo95 = **−0.60 pp** | ✅ **PASS** |
| **E2 — scoped compute** | combined/full compute reduction ≥ 30 % at non-inferior recall | reduction **24.4 %** (ratio 0.756), ρ_d = **14.4 %** | ❌ **FAIL** |

**→ Pre-committed verdict (VAL §7a): H1 FALSIFIED — compute branch.** Recall non-inferiority is *supported*; the compute claim is the falsified branch.

---

## 2. Run provenance & integrity

- Command: `m4_driver.py --mode test --split test --confirm-token READ-TEST-ONCE-SEAL2-APPROVED --per-cell 500 --workers 8` (wrapped in `caffeinate -i -s`). Exit 0. Wall time ≈ 65 h on Apple M4 (10-core), 8 workers.
- `test_accessed: true`; **15,000 injections**; routed fraction 0.752; confirmed-cheap fraction 0.211.
- **Seals hash-verified in-run (fail-closed):** Seal #2 `6292c018…32692` ✓; v3 manifest `54f06a94…c9b18` ✓. Both intact post-run.
- **Anti-tuning (NN#2):** `git diff phase1-prereg-v3` over the sealed docs + manifests is **empty** — no threshold, statistic, weight, or config moved.
- **One evaluation (P-5):** TEST read exactly once. No re-run; the result stands as the single shot.
- **TEST conditioning (sanctioned first-touch):** the 80 host residuals were produced by `research/m1_conditioning/condition_test_hosts.py` through the **frozen Stage-0** (2.5 d biweight, frozen sectors 1–3, Seal #1 manifest), conditioning exactly the sealed driver's `test_pool.sample(80, random_state=22)` draw (80/80 conditioned; provenance `data/manifests/m4/test_conditioning/`). No threshold set or read.

---

## 3. E1 — recall non-inferiority (PASS)

- Occurrence-weighted (w_c; K&M-2020 radius prior, 92.8 % weight on Rₚ≤2) ΔR̄ = **−0.0048 (−0.48 pp)**; one-sided 95 % lower bound **−0.0060 (−0.60 pp)** (bootstrap B=2000); margin = −2 pp. lo95 ≫ margin → **non-inferior**.
- Combined recall 0.488 vs Arm-A (full TLS) recall 0.509 over the injected grid; outcomes vs Arm A: both 6 761 · neither 6 807 · **loss 869 · gain 563**.
- **Why ΔR̄ is small:** the occurrence weight concentrates on Rₚ≤2, where the cheap path matches full TLS (per-cell ΔR ≈ 0.000 to −0.008). The larger per-cell losses are at Rₚ=4–12, intermediate periods (ΔR −0.10 to −0.26) — real, but low-weight.
- **Notable gain region:** at P=0.5 d, Rₚ≥4 the cheap path **beats** full TLS (ΔR +0.24 to +0.39): the folded transit-LR confirmer recovers short-period larger planets whose full-grid TLS SDE fell just below T. (Per-cell table: `e1_per_cell.csv`.)
- All 30 cells ran at the full n=500 → no cell triggered the §6 INCONCLUSIVE clause; the primary endpoint is decisively powered.

**Reading:** evidence-first routing + transit-LR confirmer + full-TLS fallback does **not** sacrifice recall on the test set (NN#1 honored).

---

## 4. E2 — scoped compute (FAIL)

- Compute ratio combined/full = **0.756** → reduction **24.4 %** (timed on the 12-star fast-path-eligible subset; serial, warm-JIT). Target ≥30 % → **FAIL**.
- **ρ_d = 14.4 %** — the routing entry tax (detector + the sealed B=1000 block-bootstrap period-FAP) charged on every routed star. Per-stage means (s): detector 5.65 · period-FAP folded into route · combined-TLS 23.9 · full-TLS 39.1.
- Break-even occurrence π*_breakeven = 0.236; f_p_search 0.612.
- **Cause is structural and pre-identified.** The dress rehearsal (CALIBRATION) projected this exactly, and the Lever-1b equivalence gate had already proven the B=1000 FAP **un-cheapenable** (both E-EVT and E-LUT failed). So the shortfall is the *un-cheapenable period-FAP entry tax*, not a confirmer defect or a recall failure. (The TEST 24.4 % is in fact a better compute number than the rehearsal's −5.6 %, but still below the pre-registered bar — the threshold-based verdict does not move.)

---

## 5. Interpretation — what Phase I concludes

- **The recall principle held.** Routing on cheap evidence (detect → period-from-spacing → calibrated folded transit-LR confirm → full-TLS fallback) recovers planets non-inferiorly to full TLS at a common false-alarm rate (E1 pass). This is the central recall-safety claim, and it survives.
- **The compute claim is falsified, honestly.** In its sealed v3 realization, evidence-first routing saves ~24 % — real, but short of the pre-registered ≥30 %. The bottleneck is the bootstrap period-FAP entry tax (ρ_d ≈ 14 %), which the protocol proved it cannot cheapen without changing outcomes.
- **This is a successful Phase I, not a failure of process.** Per the prime directive — *negative results are results*. H1's compute branch is falsified at the pre-committed threshold, with recall non-inferiority supported, under a fully sealed, single-shot, anti-tuning-clean evaluation.
- **A near-zero survey-representative figure (E3) is expected by construction** (DR-001) and is not a separate failure.

## 6. What is NOT licensed by this result (P-2 / P-8)

- **No v4.** v3 is the terminal amendment. A compute shortfall is a pre-committed falsification, not grounds to amend (P-6).
- **Future, separately pre-registered experiments only (P-8):** a cheaper-but-equivalent period-FAP (the failed Lever-1b direction, with a passing equivalence proof), multi-harmonic testing (Lever 2), a recall-protective confirmer floor (the T_red=0 fallback-suppression cost characterized in the dress rehearsal), or a clean-skip tier. None of these is a continuation of *this* experiment.

---

## 7. Artifacts

- `data/manifests/m4/test_run/` — `summary.json` (verdict + E1/E2), `recovery.csv` (15 000 rows, full pathway instrumentation), `e1_per_cell.csv`, `timing_ledger.csv`.
- `data/manifests/m4/test_conditioning/` — TEST host conditioning provenance (80/80, frozen Stage-0).
- Driver: `research/m4_evaluation/m4_driver.py`; conditioning: `research/m1_conditioning/condition_test_hosts.py`.

*M4 result record, 2026-06-24. TEST read once; verdict pre-committed and applied; v3 is final; no seal changed.*
