# DECISION RECORD — DR-002: Finding B, the Option-2 Amendment (v3), and the v3-as-Final Stopping Rule

| Field | Value |
|-------|-------|
| **ID** | DR-002 |
| **Date** | 2026-06-19 |
| **Status** | **ADOPTED + SEALED** (owner sign-off 2026-06-19; two wording revisions; Seal #2b cut as **confirmer-only v3** after both Lever-1b candidates failed the equivalence gate). v3 manifest `54f06a94…`; tag `phase1-prereg-v3`. **TEST still UNREAD** — single run pending explicit owner go (P-5). |
| **Decision owner** | Project lead (adopted the four decisions §2.1–§2.4); drafted by the resuming research session. |
| **Supersedes** | Nothing. **Extends** DR-001 (F1). The targeted-TLS confirmation realization that DR-001/Seal #2 assumed is superseded *only* in its mechanism (see §3, Finding B). |
| **Affects** | [`SCIENTIFIC_HYPOTHESIS.md`](../SCIENTIFIC_HYPOTHESIS.md) (H1 mechanism clause) · [`TRINETRA_X_PHASE1_VALIDATION.md`](../TRINETRA_X_PHASE1_VALIDATION.md) (keystone A6, Arm-B confirmation, period-FAP estimator, App A) · [`TRINETRA_MATHEMATICAL_FOUNDATIONS.md`](../TRINETRA_MATHEMATICAL_FOUNDATIONS.md) (§6 arbiter form, period-FAP estimator) → reissued as **VAL v3 / MATH v1.2** under a new pre-registration seal (**#2b**). |

> Durable record of the v3 amendment, per the repository's "documents are memory" rule ([`CLAUDE.md`](../../CLAUDE.md)). This record is authoritative for *why* Phase I is being re-registered a final time; the normative *what* lives in the reissued VAL v3 / MATH v1.2. **No TEST data has been read.** All evidence cited below is from the M4 **CALIBRATION-only** dry-run.

---

## 1. Context

M0–M3 are sealed (Seal #1 manifest `1f2d49e1…`; Seal #2 thresholds `6292c018…`). The M4 harness was built and the full pipeline exercised on the **CALIBRATION / synthetic** split only — the **TEST split was never read** (hard-blocked by `seal_loader.py`; verified 0 TEST TICs across all `data/manifests/m4/dry_run/*.csv`). Two defects and one system-level shortfall were found, all pre-TEST:

- **Finding A (implementation, fixable, no sealed-value impact).** `transitleastsquares` discards the targeted period window `[P̂(1±ε)]` when it holds `< MINIMUM_PERIOD_GRID_SIZE = 100` periods and silently returns the *full* grid. At the sealed ε=0.01 a ±1% window holds ~20–35 periods → the "targeted" arm secretly ran a full search (cost ratio ≈0.995). Feeding the in-window periods directly restores the intended saving (1.7 s vs 164 s). Finding A serves below only as a *supporting* illustration — not the warrant — for the period-FAP estimator decision: it shows that an over-expensive implementation inflating *measured* compute is a measurement artifact, not a property of the principle. The warrant for Lever 1b is the equivalence gate (§2.3a).
- **Finding B (methodology, BLOCKING).** TLS **SDE is normalized across the searched grid**. A narrow-grid SDE (e.g. 3.55) is therefore **not comparable** to the full-grid SDE (40.36) that calibrated the sealed threshold **T = 10.74**. The pre-registered rule "targeted TLS, SDE ≥ T, single common T both arms" is **internally inconsistent** → Arm B would reject planets Arm A accepts. **The targeted-TLS confirmation realization is non-executable.** M4 cannot run as sealed.
- **Combined-arm system dry-run (CALIBRATION).** With the recall-safe Option-2 architecture (route → epoch-fixed confirm → full-TLS fallback): **E1 PASS** (ΔR̄ = −0.39 pp, one-sided 95% lower bound −0.80 pp; margin −2 pp) / **E2 FAIL** (combined/full = 0.799 → ~20% reduction; population estimate ~29%; both < 30%). Structural cause: ρ_d ≈ 12.4% (the sealed B=1000 block-bootstrap period-FAP charged on every routed star) + 59% of routed stars fail the FAP gate → full-TLS fallback.

Finding B forces an amendment regardless of any performance number. The combined-arm result establishes that, with the forced fix, **recall is protected but the compute claim is at risk** — and the §7b E2-fix R&D (`M4_E2_FIX_BRAINSTORM_LOG.md`) shows the compute shortfall is driven by a **replaceable estimator** (B=1000 live bootstrap), not by the evidence-first principle.

Two review boards reported (CALIBRATION-only, TEST-blind):
- **Methodology board → APPROVE (conditional):** Option-2 (an epoch-fixed *folded-photometry* transit-significance confirmer + full-TLS fallback) is an *amendment of the same experiment*. It satisfies NN#3 (MATH §6 admits the transit-fit SNR / likelihood-ratio as an arbiter form), preserves recall-sacred routing, and amends the fairness keystone A6. Conditions: (1) the arbiter must be a genuine transit likelihood-ratio (not a box depth-SNR); (2) re-register the keystone change transparently; (3) anti-tuning discipline with a pre-committed stopping rule. ([`M4_OPTION2_METHODOLOGY_DECISION.md`](../../research/m4_evaluation/M4_OPTION2_METHODOLOGY_DECISION.md).)
- **Governance board → propose v3 as the FINAL permissible amendment** with stopping rule P-1…P-9 and a pre-committed outcome mapping. ([`PHASE1_AMENDMENT_STOPPING_RULE.md`](../../research/m4_evaluation/PHASE1_AMENDMENT_STOPPING_RULE.md).)

---

## 2. Decision

The owner adopted, in a four-step sign-off gate this session, the following. **Each step was decided on CALIBRATION evidence only, before any TEST read.**

### 2.1 — Adopt the v3-as-final stopping rule (P-1…P-9) + pre-committed outcome mapping

Binding policy (normative text reproduced in VAL v3 governance notes and CLAUDE.md Working Agreement):

- **P-1 — Amendment vs. tuning.** Only *amendments* (corrections of logical/implementation defects discovered **before** the TEST read) are permitted. *Tuning* (any change motivated by a measured outcome, on TEST **or** calibration) is prohibited (NN#2).
- **P-2 — v3 is the terminal amendment.** On sealing v3 (Seal #2b) the protocol is frozen.
- **P-3 — Design-by-theory, threshold-by-calibration.** v3's confirmation statistic is fixed from first principles (MATH §6) *before* its calibration performance is examined; calibration may only set a threshold to a pre-stated false-alarm rate, never select among statistic variants by performance.
- **P-4 — Pre-committed outcomes.** The E1/E2/inconclusive conclusions (§2.1 mapping) are sealed before the TEST read; none of them is "amend."
- **P-5 — One evaluation.** TEST is read exactly once, against sealed v3.
- **P-6 — Failure is a result.** A TEST failure → the pre-committed falsification, reported with equal rigor; it does **not** authorize a v4.
- **P-7 — Narrow defect exception (high bar, governed).** Only a *new Finding-B-class provable inconsistency* found during v3 calibration can force a stop + explicit owner decision; a performance shortfall never qualifies; a *second* such defect = a feasibility negative result.
- **P-8 — New ideas → new experiments.** After the TEST result is reported, further architectural changes (the deferred Levers 1a / multi-harmonic / clean-skip tier, etc.) are pursued only as **new, separately pre-registered experiments**, disclosed as distinct.
- **P-9 — Amendment ledger.** Every protocol version + justification + seal hash is recorded and the count kept visible (see §6).

**Pre-committed TEST-outcome mapping (sealed before TEST):**
- **E1 fail** — one-sided 95% lower bound on ΔR̄ < −2 pp → **recall falsification → H1 FALSIFIED**; report as a successful negative Phase I; do not proceed to Phase II on the routing-recall claim.
- **E2 fail** — compute reduction < 30% at non-inferior recall → **compute falsification → H1 FALSIFIED (compute branch)**. A near-zero *survey-representative* figure (E3) is expected by construction (DR-001) and is **not** a failure.
- **Inconclusive** — CI wider than margin → **not a pass**; the only permitted response (SCIENTIFIC_HYPOTHESIS §7) is the pre-planned increase in injection count with **truth and thresholds unchanged** — not an amendment.

### 2.2 — NN#3 condition #1 ruled YES (transit-template likelihood-ratio required)

A folded-photometry **transit likelihood-ratio** at the seeded ephemeris (Λ, equivalently ΔBIC or the transit-fit SNR) **is** an acceptable physics arbiter under NN#3 and MATH §6. **Required form:** a genuine transit-template LR — sign-aware, shape-consistent (a limb-darkened / trapezoidal transit template, not a box), calibrated to a null FAR, with look-elsewhere handled by the period-FAP. The dry-run's **box depth-SNR is rejected as insufficient** (borderline per the methodology board). NN#3 stands or falls on this being a true transit-shape LR.

### 2.3 — v3 scope: Option-2 confirmer + Lever 1b (equivalence-gated)

v3 comprises exactly two changes to the sealed protocol:

1. **Confirmation gate (Arm B):** replace targeted TLS (non-executable, Finding B) with the **epoch-fixed folded-photometry transit-LR confirmer** (§2.2) + **full-TLS fallback**. This amends the fairness keystone **A6** from "same TLS engine + threshold both arms" → "common false-alarm rate both arms," and H1's mechanism clause from "seeds the same search" → "seeds a calibrated folded-photometry confirmer."
2. **Period-FAP estimator (Lever 1b):** replace the sealed **B=1000 live block-bootstrap** period-FAP with a **cheaper estimator** (per-star EVT / GPD tail-fit preferred; precomputed null grid as alternative) that computes **the same sealed FAP quantity at the sealed α_FAP = 0.01**. **Primary admissibility justification: the equivalence gate (§2.3a).** Lever 1b is an amendment rather than a design change or a tune *only because* it is required to be — and proven — numerically equivalent to the sealed bootstrap (same statistic, same threshold, no change to which stars pass the gate); it is the gate, not the motivation, that licenses it, and absent a passing equivalence proof it is dropped (§2.3a fallback). Finding A is cited only as a *supporting* precedent — it illustrates that an over-expensive estimator inflating *measured* compute is a measurement artifact rather than a property of the principle — and is not itself the warrant.

**Explicitly excluded from v3:**
- **Lever 1a (margined white-noise pre-filter)** — *subsumed* by 1b (1b makes the FAP cheap for all routed stars, so the obvious-noise skip saves ≈nothing) and it carries an NN#1 recall risk (the bare form drops ~5% of recoverable planets; §6 of the brainstorm log). Excluded.
- **Lever 2 (multi-period harmonic testing)** — a genuine, recall-affecting, look-elsewhere-inflating, **performance-motivated** design change; not needed (1b alone projects E2 ≈ 39% on calibration). Excluded; **deferred to a new pre-registered experiment (P-8)**.
- **Levers 3/4 (O(N) reframe, monotransit emphasis)** — narrative/presentation, not protocol. The monotransit sensitivity is a *secondary recall* property (already in Seal #2 via z_mono = 5.3); the "different complexity class" framing remains **motivation, not evidence** (NN#4: the measured E2 number is the deliverable). Paper discussion only.

#### 2.3a — Lever-1b equivalence gate (admissibility condition)

Lever 1b is admitted into v3 **only if** validated, on CALIBRATION, to be numerically equivalent to the sealed B=1000 bootstrap:
- the cheap estimator's FAP matches the bootstrap FAP within a pre-stated tolerance across the cleaned null pool, **and**
- it does not shift which routed stars pass/fail the α_FAP gate (no gate-membership change beyond tolerance), **and**
- it is recall-safe on injections (no recoverable planet that the bootstrap keeps is clipped).

**Fallback rule:** if equivalence fails, Lever 1b is **dropped** and v3 reverts to **confirmer-only**; the honest E2 outcome (likely fail) is then reported as-is. (If the cheap estimator *materially changes outcomes*, it is a design change we cannot claim is free — so failing the gate correctly collapses it back to a true result rather than a tune.) The detailed protocol is the separate **Lever-1b equivalence-validation plan** (to be drafted next).

### 2.4 — Authorize the v3 re-registration drafting (CALIBRATION-only)

Authorize drafting, for owner sign-off and **before** any seal or TEST run: this record (DR-002, drafted first), then VAL v3 / MATH v1.2, the Lever-1b equivalence-validation plan, and the **T_red calibration plan** (calibrate the transit-LR confirmer threshold on the full cleaned null pool to FAR ≤ 1%/star; the dry-run's T_red was degenerate because the FAP gate, not the confirmer, performed FP rejection). Nothing is committed, tagged, sealed, or run against TEST until the owner approves.

---

## 3. What is preserved, amended, replaced

| Element | Disposition | Note |
|---|---|---|
| Core hypothesis (recall non-inferiority + scoped ≥30% compute) | **Preserved** | H1a/H1b intact; E1/E2 endpoints unchanged. |
| NN#1 (recall sacred) | **Preserved** | Full-TLS fallback + occurrence weighting protect combined recall (E1 PASS on calibration). |
| NN#3 (physics arbiter) | **Preserved** | Realized via a §6-admissible folded-transit LR (§2.2) instead of TLS-SDE. |
| Evidence-first architecture (detect → period-from-spacing → confirm → fallback) | **Preserved** | Unchanged. |
| Fairness keystone A6 ("same engine both arms") | **Amended** | → "common false-alarm rate both arms." |
| H1 mechanism clause ("seeds the same search") | **Amended** | → "seeds a calibrated folded-photometry confirmer." |
| Period-FAP estimator (B=1000 block-bootstrap) | **Amended (equivalence-gated)** | → cheaper estimator computing the *same* FAP at the *same* α_FAP; reverts on gate failure. |
| Sealed thresholds z⋆, z_mono, N_min, T(=10.74 full-grid), α_FAP, ε, w_c, π̂ | **Unchanged** | No threshold, grid, or occurrence value is altered by v3. T = 10.74 remains the **full-grid** SDE threshold for Arm A and the fallback. |
| Targeted-TLS confirmation realization | **Replaced** | Non-executable (Finding B). |
| The *hypothesis itself* | **Not replaced** | The principle under test is unchanged (methodology board §6). |

**Attribution caveat (documented per methodology condition #2):** with A6 relaxed to common-FAR, an E1/E2 difference now also reflects the intrinsic power gap between the LR confirmer and TLS, not routing alone. This is mitigated by the full-TLS fallback (a routed star that fails the cheap gate is still searched at full power) and is disclosed in VAL v3.

---

## 4. Alternatives rejected

1. **Confirmer-only v3 (accept the negative result now).** Rejected as the *primary* path: we hold CALIBRATION evidence that the E2 shortfall is attributable to the replaceable B=1000 estimator rather than to the evidence-first principle. Reporting a compute falsification without first removing that identified measurement artifact would attribute to the principle a cost the protocol can compute away — an outcome the evidence does not support and that the equivalence gate (§2.3a) exists to test cleanly. Retained only as the **§2.3a fallback**: if the equivalence gate fails, the artifact is *not* removable and the confirmer-only result is then reported as-is.
2. **Full lever set incl. Lever 2 (harmonics).** Rejected: purely performance-motivated, recall-affecting, look-elsewhere-inflating → classified as tuning under P-1, and unnecessary (1b alone clears 30% on calibration). Deferred to P-8.
3. **Per-arm narrow-SDE threshold T_B** (Option 1). Rejected on calibration evidence (AUC 0.43; no separation).
4. **Wider targeted window** (Option 3). Rejected: comparability and savings are mutually exclusive (AUC ≤ 0.72).
5. **Abandon the fast path (full TLS everywhere).** Rejected: discards the evidence-first principle entirely — there is no experiment left to run.

---

## 5. Consequences

- **Stronger:** Finding B is resolved with a §6-admissible arbiter; recall is protected (E1 PASS on calibration); the compute claim becomes testable rather than artifact-bound; the amendment is minimal (two changes) and each is defect/equivalence-justified, keeping it inside "amendment" not "tuning."
- **Weaker (accepted):** the experiment shifts from "does seeding the *same* search preserve recall?" to "does seeding a *calibrated, cheaper, different* confirmer preserve recall at common FAR?" — a related but slightly weaker claim (attribution caveat §3). A6 is relaxed.
- **Governance cost:** v3 re-opens sealed A.8 (period-FAP), a larger amendment than a pure confirmer swap; this is the reason for the equivalence gate (§2.3a) and the v3-as-final discipline (§2.1).
- **Eliminated risk:** "the E2 failure is fundamental" — shown on calibration to be a configuration cost (the brainstorm log §7), addressed by 1b.
- **Residual risk:** (i) the transit-LR confirmer must actually be implemented as a true shape LR (NN#3, §2.2), not a box; (ii) the equivalence gate may fail → confirmer-only fallback → likely E2-fail negative result; (iii) single-shot M4 must be executed correctly against sealed v3.

---

## 6. Amendment ledger (P-9)

| Version | Date | Justification | Pre-data status | Seal |
|---|---|---|---|---|
| v1 | 2026-06-14 | Initial Phase I pre-registration | pre-data | (superseded) |
| v2 | 2026-06-15 | F1 compute scope (DR-001) + R-4…R-7 should-fix, folded into one re-registration | pre-data | git tag `phase1-prereg-v2`; M3 thresholds Seal #2 `6292c018…` |
| **v3** | **2026-06-19** | **Finding B (forced defect) + Option-2 confirmer (A6 → common-FAR); Lever 1b period-FAP DROPPED — both candidates (E-EVT, E-LUT) failed the equivalence gate → confirmer-only** | **pre-TEST (CALIBRATION-only)** | **Seal #2b CUT — manifest `54f06a94…`; tag `phase1-prereg-v3`** |

**v3 is declared the FINAL permissible amendment (P-2).** After Seal #2b, the protocol is frozen; the only permitted actions are the single TEST run and, if INCONCLUSIVE, the pre-planned sample-size increase (P-5, mapping §2.1).

---

## 7. Sealing status (preparation; TEST NOT read)

**Two seals already cut and intact** (verified this session, *before* the v3 edits): Seal #1 manifest `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`; Seal #2 thresholds `6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692`. The v2 baseline was confirmed clean (`git diff phase1-prereg-v2` empty) *prior* to drafting; the v3 amendments below now make that diff intentionally non-empty (the re-registration itself). The `phase1-prereg-v2` tag preserves v2 immutably.

**Seal #2b (CUT 2026-06-19; owner-authorized). v3 = confirmer-only** (both Lever-1b candidates failed the equivalence gate — E-EVT and E-LUT; CALIBRATION evidence in [`LEVER1B_EQUIVALENCE_RESULT.md`](../../research/m4_evaluation/LEVER1B_EQUIVALENCE_RESULT.md)). Period-FAP = sealed B=1000 bootstrap (A.8a admits no cheap estimator); ρ_d ≈ 12.4% retained. T_red = 0.0 (non-binding, FAR-calibrated; [`TRED_CALIBRATION_RESULT.md`](../../research/m4_evaluation/TRED_CALIBRATION_RESULT.md)).

**Seal #2b record:**
- **v3 threshold manifest SHA-256 = `54f06a947a096bd496830858595dbc74a667d00dec580a92e0c92b10395c9b18`** (`data/manifests/m4/v3/m4_v3_threshold_manifest.json`). Verify: `shasum -a 256 data/manifests/m4/v3/m4_v3_threshold_manifest.json`.
- Frozen content hashes (SHA-256): VAL v3 `ce1c92c8…`; MATH v1.2 `9980d0ca…`; HYP v2.1 `4e505df6…`; confirmer.py `89d06a62…`; confirmer spec `df0143ff…`; equivalence_summary `cc32e826…`; elut_summary `0effc4f3…`; tred_summary `44f56b51…`.
- Git tag: **`phase1-prereg-v3`** (annotated; → seal commit). The tag freezes the whole tree incl. this DR-002.
1. (done) Reissued the **three** sealed docs — **VAL v3** (§2, §4, §7a, App A), **MATH v1.2** (§6, §9.1a), **SCIENTIFIC_HYPOTHESIS v2.1** (H₁ mechanism clause, A6).
2. Execute the Lever-1b equivalence-validation + T_red calibration **on CALIBRATION**; record the resulting estimator + threshold into a v3 threshold manifest; hash it (Seal #2b).
3. Tag the re-registration (e.g. `phase1-prereg-v3`) + record hashes here.
4. *Only then* the single M4 TEST run → E1/E2 → the §2.1 pre-committed verdict.

**Reconciliation (RESOLVED 2026-06-19):** `phase1-prereg-v2` is an **annotated tag** — the tag object is `5164438…`, its **target commit is `723087e…`** (`git rev-parse phase1-prereg-v2^{commit}`), matching CLAUDE.md/DR-001. No discrepancy; standard annotated-tag-object vs. target-commit distinction. The v3 tag (`phase1-prereg-v3`) will likewise be annotated.

---

*Decision record DR-002. The four decisions (§2.1–§2.4) are adopted by the owner; the drafting of VAL v3 / MATH v1.2 and the validation/calibration plans, and the seal (#2b) and TEST run, are subsequent gated steps. **No TEST data has been read; all evidence is CALIBRATION-only.***
