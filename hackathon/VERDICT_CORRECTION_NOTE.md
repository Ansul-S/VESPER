# ⚠️ Verdict-correction note for the hackathon materials (2026-07-27)

**This note annotates — it does not rewrite — the BAH 2026 · PS7 submission.** The deck,
proposal, report skeleton, and course materials in this directory were prepared for the
round-1 submission (2026-07-01) and are preserved as submitted history.

**What changed after submission.** An independent audit (2026-07-19) and the frozen-rule
E2 re-measurement (completed 2026-07-27) corrected the project's headline Phase-I
compute verdict. Any statement in these materials that presents the compute result as
**"H1 FALSIFIED — compute branch"** or a **"24.4% compute reduction / E2 FAIL"** is
**superseded**.

**Corrected verdict (authoritative):**
- **E1 — recall non-inferiority: PASS (robust).** Unchanged; strengthened by the audit
  (host-cluster lower bound −0.82 pp vs the −2 pp margin; robust to KM period weighting).
- **E2 — scoped compute: INCONCLUSIVE.** 27.3% reduction, host-clustered 95% CI on the
  cost ratio [0.636, 0.826] straddling the 30% threshold — neither confirmed nor
  falsified. Break-even prevalence π\* ≈ 0.49 ≫ TESS π ≈ 0.03.

The materials' framing of the recall result and the evidence-first *principle* stands.
Only the compute-branch verdict line is corrected.

**Authorities:** [`../docs/decisions/DR-003_E2_REMEASUREMENT.md`](../docs/decisions/DR-003_E2_REMEASUREMENT.md) ·
[`../research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) §5/§7 ·
[`../CHANGELOG.md`](../CHANGELOG.md) (v1.0.1).

*No submitted artifact in this directory has been edited; this note is the annotation.*
