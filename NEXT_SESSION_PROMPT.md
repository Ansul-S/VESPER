# Next-Session Bootstrap Prompt

> Paste the block below into a fresh Claude Code session. Assumes **zero chat history**.

---

Resume **TRINETRA-X Phase I** (evidence-first exoplanet detection, TESS). Assume zero chat history; **repository documents are authoritative**, the Obsidian `vault/` mirrors them. This repo uses **Markdown docs as deliverables (no GSD / `.planning/`)**.

**Read in order:** `CLAUDE.md` → `SESSION_HANDOFF_2026-06-24.md` → `research/m4_evaluation/M4_TEST_RESULT.md` → `docs/decisions/DR-002_DECISION_RECORD.md`.

**State: the Phase-I PRIMARY RESULT IS IN.** The single irreversible TEST read (P-5) was executed once on 2026-06-24 against sealed v3 → **VERDICT: H1 FALSIFIED — compute branch (E1 PASS, E2 FAIL).** A successful negative Phase I. Verify integrity first:
- `shasum -a 256 data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json` → `6292c018…32692` (Seal #2).
- `shasum -a 256 data/manifests/m4/v3/m4_v3_threshold_manifest.json` → `54f06a94…c9b18` (Seal #2b).
- `git diff phase1-prereg-v3 -- docs/SCIENTIFIC_HYPOTHESIS.md docs/TRINETRA_X_PHASE1_VALIDATION.md docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md data/manifests/m3 data/manifests/m4/v3` → **empty** (NN#2 intact).
- Tags `phase1-prereg-v2` + `phase1-prereg-v3` (→ `ff869d4b`); branch `phase1/m4-v3-seal2b`. Seal #1 = `1f2d49e1…`.

**The result (`data/manifests/m4/test_run/summary.json`):** 15,000 injections (30 cells × 500, literal ≥500/cell). **E1** recall non-inferiority PASS (occurrence-weighted ΔR̄ = −0.48 pp, one-sided 95% lower bound −0.60 pp; margin −2 pp; combined recall 0.488 vs full-TLS 0.509). **E2** scoped compute FAIL (reduction 24.4%, ratio 0.756, ρ_d = 14.4%; target ≥30%). Recall principle holds; compute claim is the falsified branch — the un-cheapenable sealed B=1000 block-bootstrap period-FAP entry tax (Lever-1b had already proven it un-cheapenable). Pre-committed verdict (VAL §7a) applied. TEST conditioned (sanctioned first-touch) via frozen Stage-0: `research/m1_conditioning/condition_test_hosts.py`, exactly the driver's `sample(80, random_state=22)` draw, 80/80.

**Integrity / anti-tuning:** both seals hash-verified in-run + intact; `git diff phase1-prereg-v3` empty; `test_accessed:true`; TEST read **exactly once**; verdict pre-committed before the read. Clean end-to-end.

**Immediate next step: M7 — the Phase-I write-up** from `research/m4_evaluation/M4_TEST_RESULT.md` + `docs/PAPER_NOTES.md`. Report the negative result with equal rigor (recall supported, compute falsified, traced to the period-FAP). Optional owner action: open a PR `phase1/m4-v3-seal2b` → `main`. M5/M6 (coverage/ablation) are optional extensions, not gates.

**Hard constraints:** TEST has been read once and **will not be read again** (P-5). **No sealed value, threshold, statistic, or config may change — v3 is the FINAL amendment (P-2); NO v4.** Any new idea (cheaper period-FAP with a passing equivalence proof, harmonics, recall-protective confirmer floor, clean-skip tier) is **P-8 territory only** — a new, separately pre-registered experiment, not a continuation of this one.

**Housekeeping:** all v3 + M4 work (incl. this result) is committed on `phase1/m4-v3-seal2b`; the branch is **not merged to `main`** and not pushed unless asked — PR/merge/push are owner actions; the frozen tag is unaffected.

---

*Generated 2026-06-24. Mirrors `SESSION_HANDOFF_2026-06-24.md`; the handoff is authoritative on any conflict.*
