# Phase-I Governance Review — Amendment Policy & Stopping Rule (proposal)

| Field | Value |
|-------|-------|
| **Date** | 2026-06-18 |
| **Type** | Governance recommendation memo + proposed stopping-rule policy. **No implementation / code / re-registration / VAL v3 text.** |
| **Trigger** | Methodology board APPROVED Option-2 conditionally as an *amendment* (v3); flagged anti-tuning & amendment-creep risk. TEST unread. |
| **Recommendation** | **Declare v3 the FINAL permissible amendment before the single TEST run.** Adopt the stopping rule below and pre-commit the outcome mapping **before** any re-registration drafting begins. |

---

## Part A — Recommendation memo

### A core distinction the whole policy rests on
- **Amendment** = correction of a *logical or implementation defect* discovered **before** the TEST read (e.g., Finding B: the targeted-TLS arbiter is internally inconsistent). Justified by a *defect*, independent of any performance outcome.
- **Tuning** = any design change motivated by a *measured outcome* ("it doesn't look good enough"). Forbidden by Non-Negotiable #2 — and forbidden whether the outcome is on TEST **or** on calibration.

The danger is not a single forced amendment; it is an *open-ended* amendment budget, which silently converts NN#2 ("no tuning on test") into "tune the design against calibration until confident, then take one TEST look." That is the same disease in a different organ.

### 1. Strongest argument that v3 should be the FINAL amendment
Falsifiability requires a **finite, pre-committed design**. v2 contained exactly one *forced, defect-driven* correction (Finding B — a provable internal inconsistency, not an outcome-driven tweak). v3 incorporates the complete, now-fully-understood fix. **After v3 there is no remaining *known defect* compelling change** — therefore any v4 could only be motivated by a *calibration outcome*, which is tuning, not amendment. v3 is thus the natural terminal point: it is the last change justifiable by a logical defect rather than by performance. Drawing the line here is what converts an open-ended "amend until ready" into a single committed, falsifiable test — restoring the property (SCIENTIFIC_HYPOTHESIS §3/§7) that *H0 can genuinely win*.

### 2. Risks if v4, v5, … remain possible
- **Unfalsifiability.** Any TEST failure becomes "wrong realization → amend again"; H1 can always be rescued, H0 can never win. The experiment loses its scientific point.
- **Garden of forking paths / α-inflation.** Each calibration-informed amendment is an implicit multiple comparison; the eventual "pass" loses statistical meaning.
- **Calibration overfitting.** The design fits idiosyncrasies of the specific 854 cleaned nulls; TEST generalization is unknowable and unguaranteed.
- **Loss of attributability.** Phase I's purpose is that a pass/fail is attributable to the *principle* (CLAUDE.md: simple untrained detector "on purpose"). Each added amendment makes the result attributable to accumulated engineering instead.
- **Motivated stopping.** Without a rule, amendment stops precisely when calibration looks good — selection bias baked into *when* you decide to test.
- **Seal/provenance erosion.** Proliferating seals (#2b, #2c, …) each re-open the "frozen by construction" guarantee.

### 3. Does integrity *require* declaring v3 the last amendment before TEST?
**Yes — within this Phase-I evaluation.** Integrity requires the hypothesis *and* its design be fixed before the outcome that could refute it, and that further change be justified by a *pre-data defect*, not a future outcome. It does **not** require that the science be frozen forever: a genuinely new idea is legitimate, but only as a **new, separately pre-registered experiment** — not as a continuation that retroactively "improves" this Phase-I result. So: v3 is the last amendment *of this experiment*; a hypothetical v4 *starts a different experiment*, disclosed as such.

### 4. If v3 fails E1 or E2 on the sealed TEST — the correct (pre-committed) conclusion
- **E1 fails** (one-sided 95% lower bound on ΔR̄ < −2 pp): **recall falsification** — evidence-first routing, in its best faithful realization, drops real planets beyond the margin. H1a rejected → **H1 FALSIFIED.** Report as a successful negative Phase I; do not proceed to Phase II on the routing-recall claim.
- **E2 fails** (compute reduction < 30 % at non-inferior recall): **compute falsification** — evidence-first does not earn ≥30 % even on the fast-path-eligible population. H1b rejected → **H1 FALSIFIED** (compute branch). (A near-zero *survey-representative* figure is expected and is **not** a failure — only the *scoped* E2 gates.)
- **Inconclusive** (CI wider than margin): **not a pass.** The *only* permitted response (SCIENTIFIC_HYPOTHESIS §7) is the pre-planned increase in injection count, **truth and thresholds unchanged** — not an amendment.
- A TEST failure **must not** trigger a v4. Because Finding B already showed the targeted-TLS realization infeasible, a v3 failure would mean *both* faithful realizations of the cheap confirmer fail on TESS — a strong, honest statement about the principle's Phase-I viability, not a prompt to keep amending.

### 5. Should further architectural changes be prohibited after v3?
**Yes, within this evaluation.** After the v3 seal: no architectural/threshold/statistic/grid/config change until the single TEST run is executed and reported. Permitted post-seal actions are exactly two: (i) the single TEST run; (ii) if INCONCLUSIVE, the pre-planned sample-size increase (truth/thresholds fixed). After the TEST result is reported, new architectures are pursued only as **new pre-registered experiments**. One narrow exception (high bar) is governed in P-7 below.

---

## Part B — Proposed stopping-rule policy (governance text)

> Drop-in policy for CLAUDE.md (Working Agreement), DR-002 (decision record), and VAL v3 governance notes. This is *policy about amendments* — not re-registration content.

**P-1 — Amendment vs. tuning.** Only *amendments* (corrections of logical/implementation defects discovered **before** the TEST read) are permitted. *Tuning* (any change motivated by a measured outcome, on TEST **or** calibration) is prohibited (NN#2).

**P-2 — v3 is the terminal amendment.** v3 (resolving Finding B via the conditionally-approved Option-2 confirmer) is the **final** amendment of the Phase-I protocol. On sealing v3 (Seal #2b), the protocol is frozen.

**P-3 — Design-by-theory, threshold-by-calibration.** v3's confirmation statistic must be fixed from **first principles** (matched-filter / likelihood-ratio theory per MATH §6) *before* its calibration performance is examined. Calibration may only set the threshold to a pre-stated false-alarm rate — never select among statistic variants by performance.

**P-4 — Pre-committed outcomes.** Before the TEST read, the E1/E2/inconclusive conclusions (memo §4) are written and sealed. The TEST run has exactly one of three pre-defined outcomes; **none of them is "amend."**

**P-5 — One evaluation.** TEST is read exactly once, against sealed v3. No design/threshold/statistic/grid/config change after the v3 seal.

**P-6 — Failure is a result.** If v3 fails E1 or E2 on TEST, the conclusion is the pre-committed falsification (negative result), reported with equal rigor. A TEST failure does **not** authorize a v4.

**P-7 — Narrow defect exception (high bar, governed).** If, during v3 *calibration* (pre-TEST), a **new logical/implementation defect of the Finding-B class** (a provable inconsistency — never a performance shortfall) is discovered, work **stops** and the owner makes an explicit, documented governance decision. Any resulting change is the absolute final amendment; a *second* such defect is grounds to conclude the realization space is exhausted (a feasibility negative result). Dissatisfaction with calibration performance never qualifies.

**P-8 — New ideas → new experiments.** After the TEST result is reported, further architectural changes (alternative confirmers, clean-skip tier, etc.) are pursued only as **new, separately pre-registered experiments** (Phase I-bis / Phase II), disclosed as distinct — never as retroactive improvements to this Phase-I result.

**P-9 — Amendment ledger.** Every protocol version (v1, v2, v3) and its justification (defect addressed; pre-data status; seal hash) is recorded and the count kept visible, so amendment creep is auditable.

---

## Bottom line
Adopt **v3 as the final permissible amendment**, governed by P-1…P-9, with the outcome mapping (§4) pre-committed **before** DR-002 / VAL v3 / Seal #2b are drafted. This is the discipline that lets v3 be a *legitimate amendment* rather than the first step of amendment creep — and it is the precondition under which the methodology board's conditional APPROVE remains valid.
