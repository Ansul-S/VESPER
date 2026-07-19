# DECISION RECORD — F1: Compute-Measurement Population & Phase I v2 Scope

| Field | Value |
|-------|-------|
| **ID** | DR-001 (F1) |
| **Date** | 2026-06-15 |
| **Status** | **ADOPTED** — applied to the v2 re-registration; pending seal (M0 not started) |
| **Decision owner** | Project lead (approved); drafted by Principal Research Scientist review |
| **Supersedes** | The open F1 scoping question in [`PHASE1_REMEDIATION.md`](../PHASE1_REMEDIATION.md) |
| **Affects** | [`SCIENTIFIC_HYPOTHESIS.md`](../SCIENTIFIC_HYPOTHESIS.md) v2.0 · [`VESPER_PHASE1_VALIDATION.md`](../VESPER_PHASE1_VALIDATION.md) v2 · [`VESPER_MATHEMATICAL_FOUNDATIONS.md`](../VESPER_MATHEMATICAL_FOUNDATIONS.md) v1.1 |

> Durable record of the F1 decision and the scope change it implies, per the repository's "documents are memory" rule ([`CLAUDE.md`](../../CLAUDE.md)). This record is authoritative for *why* the v2 compute claim is scoped as it is; the normative *what* lives in the three documents above.

---

## 1. Context

The Phase I compute claim (H1b) originally required a **≥30 % reduction in *total* compute** vs full TLS, with the theory giving saving ≈ *f* (fast-path routing fraction). But the primary truth is **injection into real light curves** — every test star carries a planet. On a survey-representative population the planetless majority (~99 %) presents no local evidence, routes to the full-TLS fallback, and so pays *detector + full TLS > baseline*. The fast path is therefore **net overhead on the planetless majority**, and the all-injected sample silently **overstates** survey-scale saving (gap-analysis finding **F1**, the single most consequential gap; reviewer attack **PR-A**).

Two-regime cost (now in [`VESPER_MATHEMATICAL_FOUNDATIONS.md`](../VESPER_MATHEMATICAL_FOUNDATIONS.md) §8.3a):

- Fast-path-eligible: saving ≈ 1 − (ρ_d + ρ).
- Survey-representative: saving ≈ π·f_p − ρ_d, with break-even prevalence **π\* = ρ_d / f_p**. At TESS-realistic π ∼ 10⁻², saving is near zero or negative.

## 2. Decision

**Adopt all three parts of the F1 recommendation:**

- **(a) Scope the Phase I compute claim to the fast-path-eligible population** — stars whose detector evidence meets the pre-registered routing threshold θ. H1b is restated as "≥30 % compute reduction on the fast-path-eligible population," measured on the planet-enriched injection sample. Provable in Phase I.
- **(b) Report survey-representative compute as a pre-registered secondary endpoint** (H1b-survey / E3) — a mixed sample at a pre-registered prevalence π̂, reporting C_comb/C_full as a function of π and the break-even π\*. Descriptive, **non-gating**. Expected ≈ 0/negative at TESS-realistic π̂ — by construction, not a failure.
- **(c) Defer clean-skip routing to Phase II** — survey-scale saving requires a calibrated noise-floor skip of full TLS on no-evidence stars, which trades recall and demands its own non-inferiority test. Out of Phase I scope.

**Plus the three approved guardrails:**

1. **Fast-path eligibility is defined by the pre-registered routing rule and frozen through calibration** (set on the calibration set, never on the test outcome) — defeats the circularity objection.
2. **Detector overhead ρ_d is explicitly measured and reported** — the scoped claim is meaningful only net of detector cost; ρ_d also fixes π\*.
3. **π̂ is pre-registered and the compute–prevalence frontier (including π\*) is reported** — pre-empts "cherry-picked prevalence."

**Modifications approved at sign-off:**
- F6 weight prior frozen: **log-uniform in period** × **Kunimoto & Matthews (2020)** radius occurrence.
- π̂ uses the **same Kunimoto & Matthews (2020) occurrence framework** for internal consistency.
- The four should-fix items (**R-4** block-bootstrap FAP, **R-5** transit preservation, **R-6** single-planet/strict-periodicity scope, **R-7** monotransit vetting) were folded into the **same v2 seal** to avoid a second pre-data re-registration.

## 3. Alternative rejected

Implement the clean-skip tier now and fold its recall cost into H1a. **Rejected:** larger scope, higher recall risk, slower, and it couples the compute mechanism to the protected recall endpoint — contrary to "recall is sacred" and "don't build prematurely." Phase I was never chartered to make a survey-scale deployment claim.

## 4. Consequences

- **Stronger:** H1b becomes internally valid and provable; theory–claim domains coincide; H2 gains relevance; a new deliverable (compute–prevalence frontier, π\*) is added; PR-A is neutralized.
- **Weaker (accepted):** the survey-scale "scalability" headline is **retracted for Phase I** and becomes Phase-II-conditional; the survey-representative secondary figure is expected ≈ 0/negative.
- **Eliminated reviewer criticisms:** PR-A (all-planet-sample artifact); the hidden-scoping/overstatement objection; the population facet of R6.
- **Residual:** "doesn't help at survey scale" (answered: Phase II clean-skip, with its own test); and the **new** circularity risk, managed by guardrail 1.

Full analysis archived in the decision memo that preceded this record (in-session; consequences §1–§5).

## 5. Sealing status (preparation; M0 NOT started)

The v2 edits are applied. **Content hashes (SHA-256) of the reissued set**, recorded to support a reproducible seal:

| Document | Version | SHA-256 |
|----------|---------|---------|
| `docs/SCIENTIFIC_HYPOTHESIS.md` | v2.0 | `6adae7f10bda28f9f86c74e8221939d9f3604a6d9935e2d7750731c826680f5e` |
| `docs/VESPER_PHASE1_VALIDATION.md` | v2 | `441b2c94d9ed37c2883bb55cf24f71ca2fa992e0389fea3efc7f0642b8846b40` |
| `docs/VESPER_MATHEMATICAL_FOUNDATIONS.md` | v1.1 | `4f8d95c661aba61b8bb6d43736d0685acdf9ef52b6623d0e3543b27a82034537` |

### 5a. Provenance note — cosmetic rebrand TRINETRA-X → VESPER (2026-06-30)

On **2026-06-30**, after all of the seals above had been created, the repository underwent a **repository-wide cosmetic rebrand** from the codename **TRINETRA-X** to **VESPER** (*Validation Engine for Stellar Photometric Evidence and Recovery*). The rename was made because "TRINETRA-X" was already in use elsewhere; a unique identity was required.

This rebrand was **branding-only**. It changed project-name strings, file/folder names, internal links, and presentation source. It **did not** modify any algorithm, methodology, hypothesis, equation, threshold, experimental result, figure, or scientific claim.

> **Addendum (2026-07-19, DR-003 remediation).** The concrete post-rebrand digests, each verified byte-identical to its `phase1-prereg-v3` tag version modulo pure branding strings: `m3_threshold_manifest_SEALED_CORE.json` = `5baf15df61fad9ddc236293baa7e8d446ec306d452e450ce895ec2ff9a453d38`; `m4_v3_threshold_manifest.json` = `0e600b50ec3b3fc40f8adbe810b5d541d71a9da67a9687789a597e60a8698d83`; `m3_config.yaml` unchanged = `0400e2db…`. Note: the fail-closed loaders were not updated at rebrand time, so seal verification (and thus any sealed pipeline run) was broken from 2026-06-30 until this fix — see `research/m4_evaluation/M4_ERRATUM_2026-07-19.md` §2.10.

**Consequence for the hashes recorded in this document (and in the M3/M4 threshold manifests):** because the project-name string appeared inside the sealed documents and manifests, replacing it changes their byte content and therefore their SHA-256 digests. **Any difference between a freshly recomputed SHA-256 and the value recorded above (or in `data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json`, `data/manifests/m4/v3/m4_v3_threshold_manifest.json`, etc.) is attributable solely to the TRINETRA-X → VESPER naming change and to nothing scientific or methodological.** The original sealed bytes remain recoverable from git history at the pre-registration tags (`phase1-prereg-v2`, `phase1-prereg-v3`) and the manifest release asset (`m0-manifest-v1`), which are preserved unchanged. The anti-tuning guarantee (no parameter altered after data was read) is therefore intact; only the project's name has changed.

**Two distinct seals (do not conflate):**
1. **Pre-registration seal (now, before M0):** freeze the three documents above at these hashes via a git commit + tag (e.g. `phase1-prereg-v2`). This is the anti-tuning freeze that must precede reading any data.
2. **Calibration manifest hash (later, at M3):** the numeric thresholds marked `[sealed at M3]` (z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP) are derived on the calibration set and hashed into the frozen manifest *before* the single sealed-test run (M4). See [`VESPER_PHASE1_VALIDATION.md`](../VESPER_PHASE1_VALIDATION.md) Appendix A.10.

**Remaining before the pre-registration seal can be cut:** owner confirms; commit + tag (left to the owner — no commit made by this session). Non-blocking follow-ons (`references.bib`, charter scoping note) do not affect these three documents' hashes and may be done after the seal.

---

*Decision record DR-001. The decision is adopted and applied; the seal (git tag) is the owner's action. No data has been read; M0 has not started.*
