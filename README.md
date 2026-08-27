# VESPER

### Validation Engine for Stellar Photometric Evidence and Recovery
#### Evidence-First Exoplanet Detection for the TESS Era

> **Find evidence first. Spend computation second. Let physics decide.**

**VESPER** (named for the evening star) is a research program that tested — in a
pre-registered, hash-sealed, single-evaluation experiment — whether **evidence-first
routing** can reduce the computational cost of exoplanet transit detection **without
sacrificing recall**. Instead of folding every star's light curve at thousands of trial
periods (BLS/TLS), it detects individual transit-like events directly, infers the
orbital period from their spacing, gates candidates with a bootstrap-calibrated period
false-alarm probability, confirms with a transit-model likelihood ratio, and reserves
the full periodogram search for stars showing no local evidence.

**Status (2026-07-27):** Phase I (TESS, Sectors 1–3) is **complete and sealed**; an
independent audit (2026-07-19) found the sealed compute verdict was not produced by the
frozen measurement rule — **"H1 FALSIFIED (compute branch)" is withdrawn** (decision
record [`DR-003`](./docs/decisions/DR-003_E2_REMEASUREMENT.md)). The frozen-rule
re-measurement is now **complete**: the corrected verdict is **E1 PASS (recall
non-inferiority, robust) · E2 INCONCLUSIVE** (27.3% compute reduction, 95% CI on the
cost ratio [0.636, 0.826], straddling the 30% threshold) — the compute claim is neither
confirmed nor falsified at decision-grade precision. The recall result (E1) survived the
audit and is robust. **Phase II has been re-scoped** away from Kepler routing-scaling —
see *Where this is going* below.

## Phase-I result (sealed 2026-06-24; corrected 2026-07-19 → 07-27)

- **Recall non-inferiority (E1): PASS, robust.** On 15,000 sealed-test injections the
  occurrence-weighted recall difference vs full TLS is −0.48 pp; the one-sided 95%
  lower bound clears the pre-registered −2 pp margin under all three interval
  constructions, including a host-cluster bootstrap (−0.82 pp). The pass is robust to
  the period-weighting scheme: under KM-occurrence period weighting it is if anything
  stronger (−0.16 pp; RES-2).
- **Scoped compute (E2): INCONCLUSIVE.** The originally recorded "FAIL (24.4% < 30%)"
  rested on a 12-star timing subset in deviation from the frozen measurement rule and was
  statistically undecided (ratio CI [0.42, 1.14]). Re-measured under the frozen rule
  (300 injections × 5 repeats, 39 hosts): compute ratio **0.727** (27.3% reduction),
  host-clustered 95% CI **[0.636, 0.826]** — straddling the 0.70 boundary, so the
  compute claim is **neither confirmed nor falsified**. Break-even prevalence
  π\* ≈ 0.49 ≫ TESS π ≈ 0.03. See
  [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](./research/m4_evaluation/M4_ERRATUM_2026-07-19.md) §5/§7
  for the full result and the deviations register.
- Integrity: thresholds and protocol were sealed (git tags `phase1-prereg-v2/v3`) before
  the single test read; the test split was read exactly once; sealed documents are
  byte-identical to their tags modulo the TRINETRA-X→VESPER rebrand strings.

## Where this is going (re-scoped 2026-07-20)

A full technical audit ([`docs/audits/PROJECT_AUDIT_2026-07-19.md`](./docs/audits/PROJECT_AUDIT_2026-07-19.md))
and an idea-level scientific review ([`docs/reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md`](./docs/reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md))
concluded that per-star routing cannot materially cut *survey-scale* transit-search
compute for any router of this class — occurrence is dominated by planets below
single-event visibility (measured break-even prevalence π\* ≈ 0.49 under the frozen-rule
re-measurement — 0.68 under the sealed-run values — vs TESS-realistic ≈ 0.03). Phase II is therefore **re-scoped** ([`docs/VESPER_PHASE2_PROGRAM.md`](./docs/VESPER_PHASE2_PROGRAM.md),
draft pending owner adoption as DR-004):

- **Track A — Theory:** formalize the *triage impossibility bound*, with the sealed
  Phase-I run as its empirical witness.
- **Track B — Infrastructure:** release the sealed injection-recovery machinery as
  **VESPER-Bench** — a pre-registered, leakage-safe benchmark for transit-search
  pipelines (Kepler DR25 extension).
- **Track C — Science:** an **event-wise monotransit detection pipeline** — the K=1
  regime where fold-based search provably cannot operate and photometric physics is
  structurally forced to be the arbiter.
- **G0 (gating experiment):** a fast-folding / single-event-statistic search is priced
  against TLS first, with pre-registered decision rules.

Near-term execution (verdict completion, robustness sensitivities, engineering
hardening, publication) is governed by [`docs/ROADMAP_TO_10.md`](./docs/ROADMAP_TO_10.md).
The original Kepler routing-scaling sketch is superseded and archived on its branch.

## Read in this order

> **Full document index with status labels and role-specific reading paths:** [`docs/INDEX.md`](./docs/INDEX.md). It marks every document `SEALED` / `APPEND-ONLY` / `LIVE` / `HISTORICAL` and gives separate paths for reviewers and contributors. **Sealed documents must be read with the erratum** — several of their statements were later corrected.

1. [`docs/VESPER.md`](./docs/VESPER.md) — master charter.
2. [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) — the falsifiable claims (sealed).
3. [`docs/VESPER_PHASE1_VALIDATION.md`](./docs/VESPER_PHASE1_VALIDATION.md) — the pre-registered protocol (sealed).
4. [`research/m4_evaluation/M4_TEST_RESULT.md`](./research/m4_evaluation/M4_TEST_RESULT.md) — the sealed result + addendum.
5. [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](./research/m4_evaluation/M4_ERRATUM_2026-07-19.md) — corrections, deviations register, re-measured E2.
6. [`docs/audits/PROJECT_AUDIT_2026-07-19.md`](./docs/audits/PROJECT_AUDIT_2026-07-19.md) — full second-pass audit.
7. [`docs/VESPER_PHASE2_PROGRAM.md`](./docs/VESPER_PHASE2_PROGRAM.md) — the re-scoped future.
8. [`papers/phase1_evidence_first_triage.md`](./papers/phase1_evidence_first_triage.md) — manuscript draft.

## Repository map

| Path | Contents |
|------|----------|
| `docs/` | Canonical specs + theory; `decisions/` DR-001…DR-003; `audits/` + `reviews/` (2026-07-19 audit & review); Phase-II program + roadmap |
| `research/` | Milestone tooling M0–M6 (`m0_manifest` … `m6_reality_check`), Phase-I plans (`phase1/`) |
| `data/manifests/` | Sealed manifests, thresholds, and the single-test artifacts (tracked); light-curve caches are gitignored |
| `papers/` | Manuscript draft |
| `tests/` | Fast unit tests (run in CI) |
| `archive/` | Prior-project audit (historical; do not modify) |
| `vault/` | Obsidian research memory (mirrors the repo; repo is authoritative) |

## Reproducing

```bash
python -m venv .venv && .venv/bin/pip install -r research/m4_evaluation/requirements.txt
.venv/bin/python -m pytest tests/ -q                 # fast unit tests
.venv/bin/python research/m4_evaluation/e1_corrected_inference.py   # E1 re-analysis (needs sealed artifacts)
```

Light curves are fetched from MAST (TESS SPOC 2-min); the sealed target manifest and
all thresholds are content-hashed in `data/manifests/` (verify with `shasum -a 256`,
noting the rebrand caveat in `docs/decisions/F1_DECISION_RECORD.md` §5a).

## License

MIT — see [`LICENSE`](./LICENSE). Charter author: Ansul Suryawanshi.

---

*Math in these documents uses LaTeX (`$…$`); view in a math-aware renderer (Obsidian, VS Code, GitHub).*
