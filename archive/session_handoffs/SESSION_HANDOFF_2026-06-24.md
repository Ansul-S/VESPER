# SESSION HANDOFF — 2026-06-24 — M4 single sealed-TEST read DONE → H1 FALSIFIED (compute branch)

| Field | Value |
|-------|-------|
| **Purpose** | Resume VESPER with **zero reliance on chat history**. |
| **Phase** | Phase I — Scientific Validation — **PRIMARY RESULT IN.** |
| **Status** | M0–M3 sealed; v3 sealed (#2b, confirmer-only); **M4 single TEST read EXECUTED once (2026-06-24). VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** A successful negative Phase I. |
| **Read first** | `CLAUDE.md` → this file → `research/m4_evaluation/M4_TEST_RESULT.md` → `docs/decisions/DR-002_DECISION_RECORD.md`. |

> Authority: repository documents are authoritative; vault mirrors them; this handoff is a pointer. Sealed documents govern on conflict. Supersedes `SESSION_HANDOFF_2026-06-20.md`.

---

## 1. One-paragraph state
The single irreversible TEST read (P-5) was executed once on 2026-06-24 against sealed v3, and the pre-committed verdict (VAL §7a) was applied: **H1 FALSIFIED — compute branch.** 15,000 injections (30 (P,Rₚ) cells × 500 — the literal pre-registered ≥500/cell scale). **E1 recall non-inferiority PASS** (occurrence-weighted ΔR̄ = −0.48 pp, one-sided 95% lower bound −0.60 pp; margin −2 pp). **E2 scoped compute FAIL** (reduction 24.4%, ratio 0.756, ρ_d = 14.4%; target ≥30%). The recall principle holds; the compute claim is the falsified branch, driven by the un-cheapenable sealed B=1000 block-bootstrap period-FAP entry tax (the Lever-1b equivalence gate had already proven it un-cheapenable). This is a legitimate, successful negative Phase I (prime directive: negative results are results). Integrity is clean end-to-end: both seals hash-verified in-run and intact, `git diff phase1-prereg-v3` empty, TEST read exactly once, verdict pre-committed before the read.

## 2. Integrity (verify on resume)
- `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` → `6292c018…32692` (Seal #2) ✓
- `shasum -a 256 data/manifests/m4/v3/m4_v3_threshold_manifest.json` → `54f06a94…c9b18` (Seal #2b) ✓
- `git diff phase1-prereg-v3 -- docs/SCIENTIFIC_HYPOTHESIS.md docs/VESPER_PHASE1_VALIDATION.md docs/VESPER_MATHEMATICAL_FOUNDATIONS.md data/manifests/m3 data/manifests/m4/v3` → **empty** (NN#2 intact).
- Tags `phase1-prereg-v2`, `phase1-prereg-v3` (→ `ff869d4b`). Branch `phase1/m4-v3-seal2b`. Seal #1 = `1f2d49e1…`.
- `data/manifests/m4/test_run/summary.json`: `test_accessed:true`, `n_injections:15000`, verdict string = "FALSIFIED — compute branch (E1 pass, E2 fail)".

## 3. The result (E1 / E2)
| Endpoint | Result | Decision |
|---|---|---|
| **E1 — recall non-inferiority** | ΔR̄ = −0.48 pp, one-sided 95% lo −0.60 pp (margin −2 pp); combined recall 0.488 vs full-TLS 0.509; outcomes both 6761 / neither 6807 / loss 869 / gain 563 | ✅ PASS |
| **E2 — scoped compute** | reduction 24.4% (ratio 0.756), ρ_d 14.4%, π*_breakeven 0.236; timed on 12 eligible stars | ❌ FAIL (<30%) |

- ΔR̄ is small because the K&M-2020 occurrence weight concentrates on Rₚ≤2 (arms agree, ΔR≈0); larger per-cell losses are at Rₚ=4–12 (low weight). The cheap path **beats** full TLS at P=0.5 d, Rₚ≥4 (+0.24..+0.39). All 30 cells at n=500 → no INCONCLUSIVE.
- Full record + interpretation: `research/m4_evaluation/M4_TEST_RESULT.md`.

## 4. How TEST got conditioned (a gap the prior handoff missed)
The TEST split had never been conditioned through Stage-0 (the M1 pipeline is calibration-locked by design; the M4 driver only consumes a residual cache). New tooling `research/m1_conditioning/condition_test_hosts.py` (reuses `m1_pipeline._condition_one`/`_noise_model` verbatim; frozen-param + threshold-key guards; idempotent) conditioned **exactly** the driver's `test_pool.sample(80, random_state=22)` draw — verified set-identical to the driver's host selection. 80/80 conditioned (5 transient network failures recovered on retry). Sanctioned first-touch; no threshold set or read. Provenance: `data/manifests/m4/test_conditioning/`.

## 5. The §6 scale decision (resolved)
The prior handoff's "<500/cell is within §6's realized-CI rule" read was **corrected**: VAL §6 fixes ≥500/cell as a pre-registered **floor**; the realized-CI clause only licenses *increasing* above it (for INCONCLUSIVE cells). So the owner locked the **literal ≥500/cell** (15,000 injections, ~65 h) — the defensible choice for a negative result. No deviation.

## 6. What is NOT licensed (P-2 / P-8)
- **No v4.** v3 is the terminal amendment; a compute shortfall is a pre-committed falsification, not grounds to amend (P-6). TEST will not be read again (P-5).
- **Future ideas → new, separately pre-registered experiments (P-8):** equivalence-proven cheaper period-FAP (the failed Lever-1b direction), multi-harmonic testing (Lever 2), a recall-protective confirmer floor (the T_red=0 fallback-suppression cost characterized in the dress rehearsal), clean-skip tier. None is a continuation of this experiment.

## 7. Next steps
1. **M7 — Phase-I write-up** from `research/m4_evaluation/M4_TEST_RESULT.md` + `docs/PAPER_NOTES.md`. Report the negative result with equal rigor: recall non-inferiority supported, compute claim falsified, traced to the un-cheapenable period-FAP.
2. **Optional owner action:** open a PR `phase1/m4-v3-seal2b` → `main` (the branch holds all v3 + M4 work; not yet merged).
3. M5/M6 (parameter coverage, reality check, ablation) are optional extensions, not gates on the headline verdict.

## 8. Uncommitted / branch state
All post-seal work is committed on `phase1/m4-v3-seal2b` as of this session (M4 result doc, TEST conditioning tooling + provenance, test_run artifacts, vault sync, this handoff). The branch is **not merged to `main`** and **not pushed** unless the owner asks — PR/merge/push are owner actions. The frozen tag `phase1-prereg-v3` is unaffected.

## 9. Operational notes
- The run survived two power cuts (battery carried it; no work lost). MacBook Air M4: Condition Normal, no thermal alarms — sustained all-core load is in-spec; the fanless Air throttles gracefully (hence ~65 h, not faster).
- Conditioning/catalog queries run **sandbox-disabled (host network)**.

---

*Handoff 2026-06-24. M4 read executed once → H1 FALSIFIED (compute branch); recall non-inferiority supported; v3 is final; TEST read once and will not be read again; integrity clean.*
