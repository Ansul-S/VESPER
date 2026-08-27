# VESPER — Document index and reading paths

| Field | Value |
|---|---|
| **Document** | Master document index (roadmap DOC-2) |
| **Status** | LIVE — update whenever a document is added, sealed, or superseded |
| **Updated** | 2026-07-28 |

This is the map. It labels every document with its **status class**, so a reader knows at a glance whether a file may be edited, whether it can still change, and how much authority it carries. Two recommended reading paths follow in §3.

---

## 1. Status classes

| Class | Meaning | May it be edited? |
|---|---|---|
| **SEALED** | Pre-registration artifact frozen at a git tag. The anti-tuning guarantee (NN#2, P-2) depends on it never changing. | **No.** Not even to fix a typo. Corrections go in an APPEND-ONLY companion. |
| **APPEND-ONLY** | Correction/extension of a sealed artifact. Grows forward; existing statements are never rewritten. | Append only. |
| **LIVE** | Current working document. Reflects present state and is expected to change. | Yes. |
| **HISTORICAL** | Record of a past state or a discontinued track. Kept for provenance. | **No** — read-only record. |

> **Reading the sealed set.** Sealed documents describe the experiment *as pre-registered*, not as it turned out. Several of their statements were later corrected. **Never read a sealed document without its erratum** (§2.2). Where they conflict, the erratum and DR-003 govern the *findings*; the sealed document still governs what was *pre-registered*.

> **Digest caveat.** The 2026-06-30 rebrand changed the sealed files' SHA-256 digests by renaming only. A `shasum` against the originally recorded values will mismatch. Read [`decisions/F1_DECISION_RECORD.md`](./decisions/F1_DECISION_RECORD.md) §5a and [`SEAL_CHAIN_POSTMORTEM.md`](./SEAL_CHAIN_POSTMORTEM.md) first.

---

## 2. The documents

### 2.1 SEALED — pre-registration (tags `phase1-prereg-v2`, `phase1-prereg-v3`)

| Document | Role |
|---|---|
| [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) | v2.1 — H1/H0, secondary hypotheses, assumptions, success/failure criteria |
| [`VESPER_PHASE1_VALIDATION.md`](./VESPER_PHASE1_VALIDATION.md) | v3 — the pre-registered Phase-I protocol (incl. Appendix A) |
| [`VESPER_MATHEMATICAL_FOUNDATIONS.md`](./VESPER_MATHEMATICAL_FOUNDATIONS.md) | v1.2 — canonical theory (math only) |
| `data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` | Seal #2 — the frozen thresholds themselves |
| `data/manifests/m4/v3/m4_v3_threshold_manifest.json` | v3 manifest (confirmer-only Arm B) |

### 2.2 APPEND-ONLY — the correction chain

**Start here if you want to know what is actually true.**

| Document | Role |
|---|---|
| [`../research/m4_evaluation/M4_ERRATUM_2026-07-19.md`](../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) | **The single most important document in the repository.** Deviations register (§2.1–2.11), reconstruction validation, re-measured E2 (§5), corrected conclusion (§7). |
| [`decisions/DR-003_E2_REMEASUREMENT.md`](./decisions/DR-003_E2_REMEASUREMENT.md) | Authority for withdrawing the sealed E2 verdict and re-measuring under the frozen rule |
| [`decisions/DR-002_DECISION_RECORD.md`](./decisions/DR-002_DECISION_RECORD.md) | Finding B → v3 re-registration (confirmer-only Arm B) |
| [`decisions/F1_DECISION_RECORD.md`](./decisions/F1_DECISION_RECORD.md) | DR-001 — F1 compute-scope decision, seal record, §5a rebrand provenance |
| [`../research/m4_evaluation/M4_TEST_RESULT.md`](../research/m4_evaluation/M4_TEST_RESULT.md) | The sealed single-run result + its correcting addendum |

### 2.3 LIVE — current state, theory extensions, and plans

| Document | Role |
|---|---|
| [`VESPER.md`](./VESPER.md) | Master charter |
| [`../CLAUDE.md`](../CLAUDE.md) | Operating rules + authoritative status bullets |
| [`ROADMAP_TO_10.md`](./ROADMAP_TO_10.md) | Wave 0–6 execution plan; the Phase-II gate checklist |
| [`VESPER_MATH_ADDENDUM.md`](./VESPER_MATH_ADDENDUM.md) | Post-seal math closure (MATH-6 comb identifiability; MATH-7 notation table) |
| [`SEAL_CHAIN_POSTMORTEM.md`](./SEAL_CHAIN_POSTMORTEM.md) | The rebrand incident, for an external audience |
| [`VESPER_ARCHITECTURE.md`](./VESPER_ARCHITECTURE.md) | 7-stage design (**full vision**, not the realized Phase-I system — see caveat below) |
| [`VESPER_PHASE2_PROGRAM.md`](./VESPER_PHASE2_PROGRAM.md) | Re-scoped Phase II (DRAFT; hard-gated behind the roadmap + DR-004) |
| [`MONOTRANSIT_CAMPAIGN_DESIGN.md`](./MONOTRANSIT_CAMPAIGN_DESIGN.md) | RES-7 pre-registered design (execution = Phase II) |
| [`PAPER_NOTES.md`](./PAPER_NOTES.md) · [`../papers/phase1_evidence_first_triage.md`](../papers/phase1_evidence_first_triage.md) | Publication notebook; manuscript draft |
| [`../research/phase1/`](../research/phase1/) | M0–M6 milestone plans + signed frozen choices |

> **Caveat.** `VESPER_ARCHITECTURE.md` describes the *intended* 7-stage system. Phase I realized a subset. A document describing the realized system is roadmap task DOC-1 and does not exist yet — until it does, read the architecture doc as ambition, and the M0–M6 plans plus the erratum as fact.

### 2.4 LIVE — audits and reviews (findings, not specifications)

| Document | Role |
|---|---|
| [`audits/PROJECT_AUDIT_2026-07-19.md`](./audits/PROJECT_AUDIT_2026-07-19.md) | Second-pass full audit — the source of every roadmap task |
| [`reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md`](./reviews/DEEP_SCIENTIFIC_REVIEW_2026-07-19.md) | Deep scientific review |
| [`REPOSITORY_GAP_ANALYSIS.md`](./REPOSITORY_GAP_ANALYSIS.md) | First-pass cross-document review (12 findings) |
| [`PHASE1_READINESS_REPORT.md`](./PHASE1_READINESS_REPORT.md) · [`PHASE1_REMEDIATION.md`](./PHASE1_REMEDIATION.md) | Pre-execution readiness; remediation plan (resolved — DR-001) |
| [`VESPER_CONCEPT_RECONSTRUCTION.md`](./VESPER_CONCEPT_RECONSTRUCTION.md) | Concept lineage and the v3 post-mortem (§E is the charter's central correction) |

### 2.5 HISTORICAL — read-only

| Path | Role |
|---|---|
| [`../archive/`](../archive/) | Revival-era audit and review; `session_handoffs/` (all dated handoffs) |
| `research/m4_evaluation/superseded_v2/` | Dead v2 targeted-TLS path (Findings A+B) |
| `data/manifests/m1/superseded_0.5d/` | Superseded 0.5 d detrend-window noise model |

---

## 3. Reading paths

### 3.1 For a reviewer or referee (≈ 90 min)

Goal: judge whether the claim is supported and whether the corrections are complete.

1. [`../README.md`](../README.md) — the claim in one screen.
2. [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) §§1–6 — what was pre-registered, including the non-inferiority margin.
3. **[`M4_ERRATUM_2026-07-19.md`](../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) in full** — deviations register, re-measured E2 (§5), corrected verdict (§7). Do not skip §2.8 (structural context for E1) or §2.9 (the realized arbiter is the timing gate); they are the two disclosures that most constrain how the result may be read.
4. [`decisions/DR-003_E2_REMEASUREMENT.md`](./decisions/DR-003_E2_REMEASUREMENT.md) — why the sealed E2 verdict was withdrawn.
5. [`audits/PROJECT_AUDIT_2026-07-19.md`](./audits/PROJECT_AUDIT_2026-07-19.md) §3 — the project's own list of everything wrong with it.
6. Sensitivity results: `data/manifests/m4/wave1/res2_*` (E1 under occurrence weighting), `res3_*` (epoch tolerance), `res4_*` (per-star τ_GP).
7. [`../papers/phase1_evidence_first_triage.md`](../papers/phase1_evidence_first_triage.md) — the manuscript.
8. Optional: [`SEAL_CHAIN_POSTMORTEM.md`](./SEAL_CHAIN_POSTMORTEM.md) — how the seal machinery failed and was repaired.

**Verify rather than trust:** `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` (read §5a first), and `git diff phase1-prereg-v3` over the sealed documents — empty modulo branding strings is the anti-tuning guarantee.

### 3.2 For a contributor (≈ 60 min, then start)

Goal: change something without breaking a guarantee.

1. [`../CLAUDE.md`](../CLAUDE.md) — operating rules. The non-negotiables are not stylistic.
2. This index — learn which files are SEALED before you touch anything.
3. [`ROADMAP_TO_10.md`](./ROADMAP_TO_10.md) — find your task ID; work strictly wave-by-wave.
4. [`M4_ERRATUM_2026-07-19.md`](../research/m4_evaluation/M4_ERRATUM_2026-07-19.md) §2 — the deviations register doubles as the list of known code defects and which ones are deliberately preserved.
5. `research/m4_evaluation/frozen_rerun/` — the sealed code snapshot. **Never edit it.** Live code lives in `research/m3_calibration/` and `research/m4_evaluation/`; scripts that re-measure sealed behavior import `frozen_rerun/` first (see `e2_retiming.py`, `res4_tau_fap_sensitivity.py`).
6. `research/phase1/PHASE1_M*_PLAN.md` — the milestone your change touches.

**Rules that will bite you:**
- Editing a SEALED document or manifest breaks `git diff phase1-prereg-v3`. Use an APPEND-ONLY companion instead.
- Importing the live `detector.py` when reproducing a sealed number silently changes the answer — the 2026-07-19 gap-aware fix shifts event SNRs. Import from `frozen_rerun/`.
- Never measure CPU-seconds on battery or in Low Power Mode (see erratum §5.1).
- The TEST split has been read exactly once and will not be read again (P-5, P-2).

---

*Maintained as roadmap task DOC-2. When adding a document, add a row here and give it a status class.*
