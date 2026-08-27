# SESSION HANDOFF — 2026-08-27

**Supersedes** [`SESSION_HANDOFF_2026-08-17.md`](./SESSION_HANDOFF_2026-08-17.md). Read that one for the INN-3 state, which is unchanged and still local/uncommitted.

## 1. What this session did

A full **mathematical audit** of VESPER, requested as: *"the biggest bottleneck in Project VESPER is the mathematics — fix that"*, with the deliverable a findings report distinguishing what can be **proved**, what can be **validated experimentally**, and what remains an **open hypothesis**.

**Deliverable:** [`research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md`](../../research/math_audit/MATHEMATICAL_AUDIT_2026-08-27.md)
**Code:** `research/math_audit/` — `surrogate_table.py`, `lambda_null.py`, `grid_identity.py`, `surrogate_contamination.py`, `findings.py`
**Artifacts:** `data/manifests/math_audit/` — 10 files incl. `findings.json` and `verify_surrogate_table.json`

## 2. Compliance (verified, not asserted)

| Check | Result |
|---|---|
| TEST TICs read | **0** (P-5 intact) — every input is `data/processed/m1/*.npz` or an existing calibration artifact |
| Sealed docs vs `phase1-prereg-v3`, branding-normalised | HYP **0** · VAL **0** · MATH **0** differing lines |
| Seal #2 SHA-256 | `5baf15df61…a453d38` — matches DR-001 §5a post-rebrand value |
| `frozen_rerun/` | clean |
| Sealed statistic reproduced | `ge` **bit-identical on 1,126/1,126** calibration nulls |
| Files modified | **none tracked**; everything is new under `research/math_audit/` + `data/manifests/math_audit/` (plus the vault sync) |

## 3. Method (the thing worth reusing)

Instead of re-running the FAP per candidate statistic, the session **recorded the full block-bootstrap surrogate table once** — per-surrogate `(k_b, R_b, span, n_freq)` for 1,236 calibration nulls × 1,000 surrogates (1.24 M realisations) and 669 routed calibration injections. Every candidate statistic's FAP is then a post-hoc computation on that table, with no light curve touched again. `surrogate_table.py verify` asserts the stored table reproduces the sealed exceedance counts exactly.

## 4. Findings (short form; full detail in the report)

**New — the routing ceiling.** $W \equiv k\hat R^2 \ge \ln(N_{\rm eff}/\alpha)$, $W \le N_{\rm tr}/(1+\rho_{\rm FP})$ ⟹ $P \lesssim T_{\rm base}/\ln(N_{\rm eff}/\alpha)$. Validated: zero-free-parameter gate prediction on 1,233 nulls at precision 87.5% / recall 75.7%; out-of-sample baseline scaling (predicted 2.94/5.80 d, measured 2.51/5.00 d; ratio 1.97 vs 1.99); mechanism (at P≥8 d the gate opens for 20%/0% of *correct* seeds). **Falsification attempt failed** — sweeping $T_\beta = \hat R k^\beta$ at matched null FAR gains ≤ +1.49 pp and the *exactly pivotal* statistic loses 10.31 pp.

**New — subset region.** Fast-path eligibility ⟹ SNR_tot ≳ 10.2 vs sealed T = 10.74. Measured: 17/17 fast-path recoveries also found by full TLS, 0 fast-path-only (excluding the known P=0.5 d edge artifact). E1's PASS was structurally guaranteed; this is why.

**Roadmap items closed.** **MATH-4** — Λ's null is 18× over-dispersed at q99 and 6.3e4× at Λ=25; binding T_red would be ≈4,340; `no_secondary`'s "~5σ" is ≈2.1σ; at T_red=0 the gate is a *circular* sign test (P(δ̂>0) 0.859 at seed vs 0.444 at random; P(confirm|null)=66.8%). **MATH-3** — executed and its assumed direction **reversed**: 79% of fast-path routings exist only because the bootstrap null is contaminated by the signal it tests.

**Corrections of record.** MATH §4b fragility is linear, not quadratic · MATH §9's "identical grid" premise is false in code and the deviation is load-bearing (spec as written: null FAR 2.99% → 4.37%) · Seal #2's N_min=2 is inoperative (0/128 k≤2 candidates ever routed) · the residuals are red on transit timescales (κ to 9.0) while certified white from acf₁.

**Confirmed.** M3's null cleaning was load-bearing (1.06× nominal cleaned vs 6.45× excluded). But the FAP is not a uniform p-value — **the α=0.01 calibration does not extrapolate**.

## 5. State of the repository

- Branch `phase1/inn3-fap-acceleration`, local, **uncommitted** — now carries the INN-3 work *and* this audit. Nothing pushed.
- `main` == `origin/main` @ `77037d4`. **PR #22 still open** (doc-only sync).
- No compute running at session end.
- Sealed verdict unchanged: **E1 PASS · E2 INCONCLUSIVE**.

## 6. Open decisions, in priority order

1. **⚠️ The 2026-07-28 scope + paper-framing decision is STILL open and still first in line.** This audit is directly relevant: the ceiling is a closed-form negative result that survives falsification and generalises beyond VESPER, which strengthens the case for reframing the paper around methodology + a provable limit rather than around routing performance. If accepted → **DR-005**.
2. **Does the ceiling become the paper's central result?** It is the strongest defensible novel content in the project.
3. **Should f_p be re-measured against a signal-free null before the paper quotes it?** MATH-3 says the measured 0.237 is inflated by self-contamination; a first-order rescale gives ≈0.11 and roughly doubles π\*. That estimate comes from 128 calibration rows and should be measured properly, not asserted.
4. **Where do §N-1/§N-2 and §C-1/§C-2/§C-3 land?** Proposal: fold the ceiling and subset-region into `docs/VESPER_MATH_ADDENDUM.md` as §F/§G; record the three corrections as corrections of record. Nothing sealed is edited either way.
5. Carried from 2026-08-17: adopt `fast_period_fap` as estimator of record (DR-006+); paper placement of the INN-3 counterfactual; whether §7.1 warrants a RES-4 addendum.
6. Still queued for a compute window: **RES-6** (η-paid injection; needs MAST, `data/raw` empty) + the small **TLS-epoch re-run**.

## 7. How to reproduce

```bash
.venv/bin/python research/math_audit/surrogate_table.py nulls      --workers 8
.venv/bin/python research/math_audit/surrogate_table.py verify        # must print BIT-IDENTICAL True
.venv/bin/python research/math_audit/surrogate_table.py injections --workers 7 --per-cell 30
.venv/bin/python research/math_audit/lambda_null.py                --workers 6 --n-rand 20
.venv/bin/python research/math_audit/grid_identity.py              --workers 8
.venv/bin/python research/math_audit/surrogate_contamination.py    --workers 8 --per-cell 6
.venv/bin/python research/math_audit/findings.py
```

~35 min on 8 cores. Seeds fixed (20260616 / 20260619 / 20260827); the null surrogate stream is the sealed one.
