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

**Status:** Phase I (TESS, Sectors 1–3) is **complete and sealed**; an independent
audit and remediation pass (2026-07-19) corrected the statistics of the sealed result.
Phase II (Kepler scaling) is a pending decision.

## Phase-I result (sealed 2026-06-24; corrected 2026-07-19)

- **Recall non-inferiority (E1): PASS, robust.** On 15,000 sealed-test injections the
  occurrence-weighted recall difference vs full TLS is −0.48 pp; the one-sided 95%
  lower bound clears the pre-registered −2 pp margin under all three interval
  constructions, including a host-cluster bootstrap (−0.82 pp).
- **Scoped compute (E2):** the originally recorded "FAIL (24.4% < 30%)" rested on a
  12-star timing subset in deviation from the frozen measurement rule and was
  statistically undecided (ratio CI [0.42, 1.14]). It was re-measured under the frozen
  rule in the audit remediation — see
  [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](./research/m4_evaluation/M4_ERRATUM_2026-07-19.md)
  for the corrected verdict and the full deviations register.
- Integrity: thresholds and protocol were sealed (git tags `phase1-prereg-v2/v3`) before
  the single test read; the test split was read exactly once; sealed documents are
  byte-identical to their tags modulo the TRINETRA-X→VESPER rebrand strings.

## Read in this order

1. [`docs/VESPER.md`](./docs/VESPER.md) — master charter.
2. [`docs/SCIENTIFIC_HYPOTHESIS.md`](./docs/SCIENTIFIC_HYPOTHESIS.md) — the falsifiable claims (sealed).
3. [`docs/VESPER_PHASE1_VALIDATION.md`](./docs/VESPER_PHASE1_VALIDATION.md) — the pre-registered protocol (sealed).
4. [`research/m4_evaluation/M4_TEST_RESULT.md`](./research/m4_evaluation/M4_TEST_RESULT.md) — the sealed result + addendum.
5. [`research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](./research/m4_evaluation/M4_ERRATUM_2026-07-19.md) — corrections, deviations register, re-measured E2.
6. [`papers/phase1_evidence_first_triage.md`](./papers/phase1_evidence_first_triage.md) — manuscript draft.

## Repository map

| Path | Contents |
|------|----------|
| `docs/` | Canonical specs + theory; `docs/decisions/` decision records DR-001…DR-003 |
| `research/` | Milestone tooling M0–M6 (`m0_manifest` … `m6_reality_check`), Phase-I plans (`phase1/`) |
| `data/manifests/` | Sealed manifests, thresholds, and the single-test artifacts (tracked); light-curve caches are gitignored |
| `papers/` | Manuscript draft |
| `tests/` | Fast unit tests (run in CI) |
| `hackathon/` | BAH 2026 PS7 track (separate, submitted 2026-07-01) |
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
