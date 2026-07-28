# VESPER — MATHEMATICAL ADDENDUM (post-seal)

| Field | Value |
|-------|-------|
| **Document** | Post-seal mathematical closure notes (Wave 2 of [`ROADMAP_TO_10.md`](./ROADMAP_TO_10.md)) |
| **Version** | 0.1 |
| **Created** | 2026-07-28 |
| **Status** | **LIVE / APPEND-ONLY.** Not a pre-registration document. Nothing here is sealed, and nothing here changes any sealed threshold, estimand, or the Phase-I verdict. |
| **Relation to the sealed theory** | Companion to [`VESPER_MATHEMATICAL_FOUNDATIONS.md`](./VESPER_MATHEMATICAL_FOUNDATIONS.md) v1.2 (SEALED at tag `phase1-prereg-v3`). That document is **not edited** — it remains byte-frozen modulo the DR-001 §5a rebrand strings. This addendum records analysis performed *after* the seal. |
| **Authority** | Where this addendum and the sealed MATH document differ in emphasis, the sealed document governs the *pre-registered* experiment; this addendum governs *interpretation and future runs*. |

> **Why a separate file.** Non-negotiable NN#2 and P-2 require that `git diff phase1-prereg-v3` over the sealed documents stay empty (modulo branding). Appending sections to the sealed MATH document would break that check, which is the project's principal anti-tuning guarantee. Post-seal mathematics therefore lands here and is cross-referenced, never inlined.

---

## A. MATH-6 — Identifiability of the integer-comb period estimator at $N=2$

**Artifact:** [`data/manifests/m4/wave2/math6_comb_degeneracy.json`](../data/manifests/m4/wave2/math6_comb_degeneracy.json)
**Script:** [`research/m4_evaluation/math6_comb_degeneracy.py`](../research/m4_evaluation/math6_comb_degeneracy.py) (runs the **frozen** `period_recovery`)
**Addresses:** audit §3.3 (N=2 comb degeneracy); roadmap MATH-6.

### A.1 The estimator

Sealed period recovery (MATH §4; `frozen_rerun/period_recovery.py`) scores a trial period $P$ by the circular spread of the detected event epochs $\{t_j\}_{j=1}^{k}$ about a common phase:

$$R(P)=\Big|\tfrac{1}{k}\textstyle\sum_j e^{2\pi i\,t_j/P}\Big|\in[0,1],\qquad s(P)=1-R(P),\qquad \hat P=\arg\min_{P\in\mathcal{G}} s(P),$$

on the frequency grid $\mathcal{G}$ spanning $[p_{\min},p_{\max}]$, with $p_{\max}\leftarrow\min(p_{\max},\,\mathrm{span})$ and $\mathrm{span}=\max_j t_j-\min_j t_j$. Seal #2 fixes $N_{\min}=2$, so **two events suffice to seed a period.**

### A.2 The degeneracy (exact)

For $k=2$ with spacing $D=t_2-t_1$, both events share a phase exactly when $D/P\in\mathbb{Z}$. Hence

$$s(P)=0 \iff P=D/m,\quad m\in\mathbb{N},\ D/m\ge p_{\min}.$$

Every member of this **tie set** is a *global* minimum, so $\hat P$ is **not identifiable** from two events. The statistic $R$ *is* identified: it equals $1$ on the entire tie set. Verified numerically — on-comb scores $\le 1.1\times10^{-16}$ for $m=1\dots10$, off-comb scores $>10^{-3}$ (`tie_set.tie_set_confirmed = true`).

### A.3 What breaks the tie — a correction to the roadmap's premise

The roadmap states the realized convention as "$\arg\min\to$ longest-$P$". **Measurement shows this is approximately, not exactly, true**, and that the mechanism is not a period preference at all: the tie members differ only by IEEE-754 rounding of $1-R$ at the $\sim10^{-16}$ level, and `np.argmin` returns the first index attaining the numerically smallest value. Which harmonic that is, is decided by float rounding.

Two strata must be separated, because their mixture depends on the (data-dependent) spacing distribution and a pooled number would be meaningless:

| Stratum | $m=1$ (longest $P$) | $m\in\{1,2,3\}$ | $m\ge4$ | not a harmonic of $D$ | $R$ saturated at 1 |
|---|---|---|---|---|---|
| **In range** ($D\le p_{\max}$; $P=D$ is on the grid) | 74.2–75.2% | 98.1–98.6% | 1.4–1.9% | ~0% | yes |
| **Out of range** ($D>p_{\max}$; $P=D$ unreachable) | ~0% | ~0.2–0.3% | — | 99.3–99.5% | **no** |

*(ranges span baselines 24.9 d and 49.6 d; 4000 draws per stratum per baseline, seed 20260616)*

- **In range** is the genuine degeneracy: $P=D$ is reachable and is chosen only ~3/4 of the time; the remainder are sub-harmonics selected by float noise.
- **Out of range** is a *different failure* — the true spacing lies outside the sealed search range, no harmonic of $D$ need land on the grid, and $R$ does **not** saturate. This presents to the FAP as an ordinary weak fold, not a perfect one, and should not be described as the comb degeneracy.

### A.4 Consequence: a recall cost, never a false positive

`recovery._period_match` accepts $m\in\{2,3\}$ as a (flagged) harmonic match. That tolerance therefore absorbs **98.1–98.6%** of in-range $N=2$ seeds; only **1.4–1.9%** leak to $m\ge4$ and fail the sealed period predicate. Every such leak is a *missed* recovery — it can only lower recall, never manufacture a detection. This is consistent with the prime directive's asymmetry (a false positive is acceptable; a missed planet is not) in the conservative direction.

### A.5 Why the FAP remains valid under the degeneracy

The block-bootstrap FAP (MATH §9.1) compares the **observed $R$** against surrogate $R$ values — it never uses $\hat P$:

$$\widehat{\mathrm{FAP}}=\frac{1+\#\{b: R^{(b)}_{\max}\ge R_{\rm obs}\}}{1+B}.$$

$R$ is constant on the tie set, and each surrogate is scored by the *identical* degenerate procedure. Observed and null statistics are therefore inflated in exactly the same way, and the degeneracy **cannot** inflate the false-alarm rate. Formally: the test statistic is a well-defined function of the data even where the parameter is unidentifiable, and the null is generated by the same map. The degeneracy costs period *accuracy*, not false-alarm *control*.

### A.6 What the $N=2$ FAP actually tests

Because $R_{\rm obs}=1$ is saturated at $N=2$, the FAP degenerates into "how often does a surrogate also reach $R=1$?" — and any surrogate producing only two events does so automatically. Measured null probability of $R\ge0.999$ against event multiplicity $k$ (baseline 24.9 d, sealed grid):

| $k$ | 2 | 3 | 4 | 5 | 6 | 8 | 10 | 15 |
|---|---|---|---|---|---|---|---|---|
| $\Pr(R\ge0.999)$ | 0.735 | 0.163 | 0.007 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| median $R$ | 1.000 | 0.992 | 0.952 | 0.901 | 0.843 | 0.749 | 0.677 | 0.562 |

*(1500 draws per $k$; uniform event epochs over the baseline — an upper bound on how easily the null folds, since real surrogate events cluster)*

**At $N=2$ the period-FAP is a test of event *rarity* under the null, not of period coherence.** This is a substantive interpretive point: the fast path's binding gate at the sealed operating point is the period-FAP (erratum §2.9), and at the minimum admissible event count that gate is measuring how unusual it is to see so *few* events, not how well they fold. It should be read alongside erratum §2.9 when describing what the realized arbiter tests.

### A.7 Reproducibility caveat (feeds ENG/REPRO)

Because the tie is broken by floating-point rounding, the selected harmonic is deterministic for a given input **and numpy build**, but is not guaranteed stable across architectures or numpy versions. Sealed Phase-I results are unaffected — they were produced once, on one build, and are preserved verbatim in `frozen_rerun/`. Any future (Phase-II) run should **pin the convention explicitly** — e.g. round scores to $10^{-12}$ before `argmin`, then break remaining ties toward the longest period — rather than inherit float noise. Recommended as a Wave-3 item alongside CODE-2 ("degeneracy convention pinned").

---

## Change log

| Date | Change |
|---|---|
| 2026-07-28 | Created. §A MATH-6 (comb identifiability at $N=2$). |
