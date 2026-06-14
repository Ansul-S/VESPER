# TRINETRA — MATHEMATICAL FOUNDATIONS

| Field | Value |
|-------|-------|
| **Document** | Canonical Theoretical Reference |
| **Version** | 1.1 |
| **Revised** | 2026-06-15 (v1.1: §8.3a two-regime cost model [F1]; §9.1 committed block-bootstrap [R-4]; §4 single-planet/strict-periodicity scope [R-6]; §6 monotransit confirmation [R-7]) |
| **Scope** | Mathematics, statistics, and scientific reasoning **only** — no implementation |
| **Project** | TRINETRA-X (see [`TRINETRA-X.md`](./TRINETRA-X.md)) |
| **Companions** | [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md) · [`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md) · [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) · [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) |

> This document reconstructs the mathematical backbone of the evidence-first detection paradigm from first principles. It is the theoretical authority for the project: where prose and equations conflict elsewhere, these derivations govern. Notation is fixed in §0 and used consistently throughout.

---

## 0. Notation and Conventions

| Symbol | Meaning |
|--------|---------|
| $f(t)$ | observed flux time series, $t \in \{t_1,\dots,t_N\}$, cadence $\Delta t$ |
| $r(t)$ | conditioned residual flux, zero-centred: a transit is a **negative** excursion |
| $\sigma$ | robust per-cadence noise scale (e.g. $\sigma = 1.4826\,\mathrm{median}|r-\mathrm{med}(r)|$) |
| $\Sigma$ | noise covariance matrix (white: $\sigma^2 I$; red: non-diagonal) |
| $\delta$ | fractional transit depth, $\delta=(R_p/R_\star)^2$ |
| $T_{14}$ | transit (first-to-fourth contact) duration |
| $n_{\rm in}$ | in-transit cadence count, $n_{\rm in}=T_{14}/\Delta t$ |
| $P$ | orbital period; $t_0$ epoch; $N_{\rm tr}$ number of transits in baseline $T_{\rm base}$ |
| $k$ | number of detected events ($k_{\rm true}$ real + $k_{\rm FP}$ false) |
| $z_\star$ | local-detection threshold (in $\sigma$ units) |
| $\Phi,\ \phi$ | standard normal CDF and PDF |

Throughout, "evidence" denotes a **photometrically significant local flux decrement**, never a mere coincidence of event times — the central correction of TRINETRA-X over v3 ([`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §E).

---

## 1. Evidence-First Detection: the Formal Inversion

Classical transit search is a **composite hypothesis test over a period grid**. For each trial $(P,t_0,T_{14})$ one folds the light curve and tests

$$\mathcal{H}_1(P,t_0,T_{14}):\ r(t)= -\delta\,\Pi_{P,t_0,T_{14}}(t)+\varepsilon(t)\quad\text{vs.}\quad \mathcal{H}_0:\ r(t)=\varepsilon(t),$$

with $\Pi$ the periodic in-transit indicator. The generalized likelihood-ratio search maximizes a detection statistic over the full grid $\{P\}\times\{t_0\}\times\{T_{14}\}$. This is hypothesis-driven: structure ($P$) is **assumed**, then tested.

Evidence-first detection inverts the quantifier order. It first solves a **simple (non-periodic) hypothesis test at each time**,

$$\mathcal{H}_1^{\rm loc}(t):\ \text{a transit-shaped decrement is present near } t \quad\text{vs.}\quad \mathcal{H}_0^{\rm loc}(t):\ \text{noise only},$$

producing an event set $\mathcal{E}=\{\hat t_1,\dots,\hat t_k\}$, and **only then** asks whether a period explains $\mathcal{E}$. Symbolically:

$$\underbrace{\max_{P}\ \max_{t_0,T_{14}}\ \mathrm{LRT}(P,t_0,T_{14})}_{\text{hypothesis-first (BLS/TLS)}} \;\Longrightarrow\; \underbrace{\Big(\text{detect } \mathcal{E}\ \text{by local LRT}\Big)\ \to\ \Big(\inf_P \text{ explaining }\mathcal{E}\Big)}_{\text{evidence-first (TRINETRA)}}.$$

The inversion is legitimate **iff** the local test has high recall on the planets one cares about — i.e. iff a real transit is individually significant. That condition is exactly §2, and its truth is population-dependent (§7), which is why the paradigm is a *triage*, not a replacement.

---

## 2. Local Transit Significance

Model a single transit as a depth-$\delta$ decrement over $n_{\rm in}$ cadences, each with noise $\sigma$. The **matched filter** (Neyman–Pearson optimal linear detector for a known shape in additive noise) correlates $r$ with the unit-energy transit template $g$. The single-transit detection statistic and its noise-normalized form give

$$\boxed{\ \mathrm{SNR}_1=\frac{\delta\,\sqrt{n_{\rm in}}}{\sigma}=\frac{\delta}{\mathrm{CDPP}(T_{14})}\ }\qquad\text{with}\qquad \mathrm{CDPP}(T_{14})\equiv \frac{\sigma}{\sqrt{n_{\rm in}}}.$$

CDPP (combined differential photometric precision) is the effective noise **averaged over the transit duration**; the second equality is its definition. Over $N_{\rm tr}$ transits the folded (phase-averaged) SNR grows as

$$\mathrm{SNR}_{\rm tot}=\mathrm{SNR}_1\sqrt{N_{\rm tr}}=\frac{\delta\sqrt{N_{\rm tr} n_{\rm in}}}{\sigma}.$$

The transit duration for a central, circular-orbit transit of a star of mean density $\rho_\star$ follows from Kepler's third law:

$$T_{14}\simeq \frac{P}{\pi}\,\frac{R_\star}{a}=\frac{R_\star\,P}{\pi a},\qquad a=\left(\frac{G M_\star P^2}{4\pi^2}\right)^{1/3}\ \Rightarrow\ T_{14}\propto \rho_\star^{-1/3}P^{1/3}.$$

**Red-noise correction.** Real photometric noise is correlated. With covariance $\Sigma$, the optimal statistic is the *generalized* (whitened) matched filter,

$$\mathrm{SNR}_1^{\rm GP}=\frac{g^{\mathsf T}\Sigma^{-1}r}{\sqrt{g^{\mathsf T}\Sigma^{-1}g}},$$

which reduces to the boxed expression when $\Sigma=\sigma^2 I$. Replacing $\sigma^2 I$ by a Gaussian-process $\Sigma$ is one of the principal TRINETRA-X improvements (§11), because the white-noise CDPP systematically *under*-estimates the true noise on transit timescales for active stars and TESS systematics.

---

## 3. Event Extraction Theory

Detection declares an event where the matched-filter response crosses a threshold,

$$s(t)=(r\star g)(t)<-z_\star\,\sigma_s,\qquad \sigma_s^2=\mathrm{Var}[s\,|\,\mathcal{H}_0],$$

with clustering of contiguous crossings into a single event at the local minimum. Two quantities govern everything downstream.

**(a) True-event yield (recall of the local test).** A real transit is flagged with probability

$$p_{\rm det}^{\rm (1)}=\Pr\!\big(\mathrm{SNR}_1\ \text{exceeds } z_\star \text{ given depth }\delta\big)=\Phi\!\big(\mathrm{SNR}_1-z_\star\big),$$

so the expected number of recovered true transits is $\mathbb{E}[k_{\rm true}]=N_{\rm tr}\,p_{\rm det}^{(1)}$.

**(b) False-event rate (contamination).** Under white Gaussian $\mathcal{H}_0$, threshold down-crossings of a smooth process follow Rice's formula; to leading order the expected count over the baseline is

$$\mathbb{E}[k_{\rm FP}]\approx \underbrace{\frac{T_{\rm base}}{T_{14}}}_{N_{\rm indep}}\ \Phi(-z_\star),$$

i.e. the number of independent transit-duration windows times the per-window tail probability. For $z_\star=3$, $\Phi(-3)=1.35\times10^{-3}$.

> **Critical caveat (carried into §10).** Equation (b) assumes **white** noise. Real residuals are red: their heavy-tailed, correlated excursions inflate $\mathbb{E}[k_{\rm FP}]$ by an order of magnitude or more. The mismatch between the white-noise prediction and the measured event rate is the mathematical root of v3's false-positive problem.

The ratio that controls period recovery is the **contamination ratio**

$$\rho_{\rm FP}\equiv \frac{k_{\rm FP}}{k_{\rm true}},$$

which §4–§5 show is the single most important quantity for whether a period can be recovered at all.

---

## 4. Period Recovery Mathematics

Given $\mathcal{E}=\{\hat t_i\}$, recover $P$ such that the true subset shares a common phase. Two equivalent formulations.

**(a) Phase concentration (circular statistics).** At trial period $P$, define phases $\varphi_i(P)=2\pi\,(\hat t_i \bmod P)/P$. The **Rayleigh statistic** measures concentration:

$$Z(P)=k\,\bar R^2(P),\qquad \bar R(P)=\frac{1}{k}\left|\sum_{i=1}^{k} e^{\,\mathrm i\varphi_i(P)}\right|.$$

Under $\mathcal{H}_0$ (uniform phases, all events false) and for moderate $k$, $2Z\sim\chi^2_2$, so $\mathbb{E}[Z]\approx1$; a coherent transit train at $P_{\rm true}$ produces $Z\gg1$. The recovered period is $\hat P=\arg\max_P Z(P)$.

**(b) Pairwise differences (number theory).** True transit times satisfy $\hat t_j-\hat t_i = m_{ij}P$ for integers $m_{ij}$; the period is the approximate generator (greatest common divisor under tolerance) of the true differences. With $k$ events there are $\binom{k}{2}$ differences, of which only $\binom{k_{\rm true}}{2}$ are coherent. The **signal-to-background in difference space** is therefore

$$\frac{\text{coherent pairs}}{\text{total pairs}}=\frac{\binom{k_{\rm true}}{2}}{\binom{k}{2}}\approx\frac{1}{(1+\rho_{\rm FP})^2}.$$

This $O\big((1+\rho_{\rm FP})^{-2}\big)$ scaling is the **fundamental fragility** of period recovery: false events degrade it *quadratically*. It is why §3(b)'s contamination — and especially its red-noise underestimate — is decisive.

**Harmonics.** Both formulations are invariant under $P\to P/2,\,2P,\,P/3,\dots$; the alias set $\{mP/n\}$ must be scored and resolved, conventionally by preferring the period whose folded profile yields the most significant *photometric* transit (§6), not the highest phase concentration.

**Scope (Phase I).** The relations above assume a **single, strictly periodic** transiting signal: $\hat t_j - \hat t_i = m_{ij}P$ requires a constant period and one transiting body in the event set $\mathcal{E}$. Multiple planets (interleaved periods) and significant TTVs violate these premises and are **out of Phase I scope** (assumptions A9, A10 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md)). The "model-agnostic" generality of the detector (§1) pertains to *event detection* — flagging non-box / asymmetric decrements — and does **not** extend to this period-recovery step.

---

## 5. Voting / Hough-Space Formulation

Cast period recovery as a Hough transform: each event $\hat t_i$ votes for the locus of $(P,\varphi)$ consistent with it, and true transits accumulate at a common point while false events scatter.

$$\mathcal{H}(P,\varphi)=\sum_{i=1}^{k}\mathbb{1}\!\big[\,|\varphi_i(P)-\varphi|<w\,\big],\qquad \hat P=\arg\max_{P}\ \max_{\varphi}\ \mathcal{H}(P,\varphi).$$

The peak height equals the number of phase-coherent events; the accumulator is the binned realization of the Rayleigh statistic (§4a). Voting is robust to *missed* transits (they merely lower the peak) and to a modest number of false events (they raise the flat background by $\sim k_{\rm FP}w$), which is why a voting scheme is the principled estimator — **provided its output is calibrated**, which the next subsection makes precise and which v3 omitted.

**The look-elsewhere problem, exactly.** Scanning $N_P$ trial periods and reporting the maximum induces a multiple-comparison (look-elsewhere) effect. The naive normalized score used by v3,

$$\text{score}(P)=\frac{\max_{\rm bin}\text{count}}{k}\in[0,1],$$

has no calibrated meaning. For $k$ events and $b$ phase bins, the probability that all $k$ fall in one bin at a *single* random period is $b\cdot b^{-k}=b^{1-k}$; over $N_P$ approximately-independent trial periods,

$$\Pr\!\big[\text{score}=1 \text{ somewhere}\big]\approx 1-\big(1-b^{1-k}\big)^{N_P}.$$

For $k=3,\ b=10,\ N_P=10^3$: $b^{1-k}=10^{-2}$ and $\Pr\approx 1-0.99^{1000}\approx 0.9999$. **A perfect score is therefore essentially guaranteed from pure noise** at small $k$ — the precise mathematics of v3's false-positive engine (§10). The remedy is to calibrate against the *distribution of the maximum*, §9.

---

## 6. Photometric Confirmation: the Significance Gate

Phase concentration establishes *timing*; it does not establish that a *transit* exists. The arbiter is a likelihood-ratio test on the **folded photometry** at the seeded period. Comparing a transit model $\mathcal{M}_1$ (depth, duration, shape) against a flat model $\mathcal{M}_0$,

$$\Lambda = -2\ln\frac{\mathcal{L}(\mathcal{M}_0)}{\mathcal{L}(\mathcal{M}_1)}\ \xrightarrow{\ \mathcal{H}_0\ }\ \chi^2_{\nu},\qquad \text{or, Bayesian, } \ \ln\!\frac{\mathcal{Z}_1}{\mathcal{Z}_0}\ (\text{evidence ratio}).$$

A candidate is confirmed iff $\Lambda$ (equivalently $\Delta\mathrm{BIC}$ or the transit-fit SNR) exceeds a pre-registered threshold **and** the folded depth is significant and shape-consistent (sign-aware, binned — never the absolute value of a single interpolated sample, the v3 even/odd bug; [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §E). This is the formal content of Principle 2, *"photometry is the judge"* ([`TRINETRA-X.md`](./TRINETRA-X.md)). In Phase I the gate is a narrow-grid TLS using the **same engine and threshold as the baseline**, so confirmation physics is identical across arms (fairness keystone; [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md), §2).

**Monotransit confirmation (no repetition available).** For a single event ($N_{\rm tr}=1$) the repeatability criterion is unavailable, so confirmation is defined on a **single-event** basis and is explicitly weaker. A monotransit candidate is confirmed iff: (i) the transit-shaped likelihood ratio $\Lambda$ over a flat model exceeds the pre-registered threshold; (ii) ingress/egress and duration are consistent with a physical $(R_\star, \rho_\star)$; (iii) **no secondary eclipse** is present at the candidate phase; (iv) **no centroid shift** (where pixel/diff-image data are available); and (v) the event is not coincident with known systematics (momentum dumps, scattered light). Monotransit false-positive control is **weaker by construction** than the repeating-transit gate — a single event cannot be discriminated from a flare or one-off systematic by repetition — so monotransit recoveries are reported separately and **excluded from the headline** (H3 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md); routing threshold $z_{\rm mono}$ in [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) Appendix A.3).

---

## 7. Why Jupiter-Class Planets Are Recovered Efficiently

From §2, local detectability requires $\mathrm{SNR}_1=\delta/\mathrm{CDPP}\ge z_\star$, i.e.

$$\left(\frac{R_p}{R_\star}\right)^2\ge z_\star\,\mathrm{CDPP}(T_{14})\ \Longleftrightarrow\ R_p\ge R_{p,\rm crit}=R_\star\sqrt{z_\star\,\mathrm{CDPP}}.$$

There is thus a **critical radius** above which a single transit is individually significant. Because depth scales as radius squared,

$$\frac{\mathrm{SNR}_1^{\rm Jup}}{\mathrm{SNR}_1^{\oplus}}=\left(\frac{R_{\rm Jup}}{R_\oplus}\right)^2\approx 11.2^2\approx 1.3\times10^2 .$$

Numerically, for a Sun-like star a Jupiter gives $\delta\approx10^{-2}$ ($10^4$ ppm) while an Earth gives $\delta\approx8.4\times10^{-5}$ (84 ppm); against TESS CDPP of tens-to-hundreds of ppm, $\mathrm{SNR}_1^{\rm Jup}\gg1$ (single transit trivially detectable) whereas $\mathrm{SNR}_1^{\oplus}\ll1$ (undetectable without folding $N_{\rm tr}$ transits). This is the **bimodality** (§1, A1 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md)): large planets fall on the fast path with $r_{\rm seed}\to1$; small planets correctly fall through to the full-search fallback. The paradigm earns its advantage precisely on the high-$\mathrm{SNR}_1$ tail — and *only* claims it there.

---

## 8. Routing Fraction, Complexity, and the Recall–Compute Tradeoff

### 8.1 Complexity derivations

Let $N$ be the number of cadences, $N_P$ the period-grid size, $N_d$ the duration-grid size, $N_\varphi$ the phase bins.

**Full search (BLS/TLS):** fold and score at every grid node,
$$C_{\rm full}=\mathcal{O}\!\big(N_P\,(N+N_\varphi N_d)\big)=\mathcal{O}(N\,N_P\,N_d).$$
With near-optimal period sampling $N_P\propto T_{\rm base}f_{\max}N^{1/3}$, this is the familiar super-linear cost.

**Evidence-first fast path:**
$$\underbrace{\mathcal{O}(N N_d)}_{\text{matched filter}}+\underbrace{\mathcal{O}(N)}_{\text{event extraction}}+\underbrace{\mathcal{O}(k N_P)\ \text{or}\ \mathcal{O}(k^2)}_{\text{period recovery}}+\underbrace{\mathcal{O}(N N_P^{\rm narrow})}_{\text{targeted confirm}}.$$
Since $k\ll N$ and the confirmation grid $N_P^{\rm narrow}\ll N_P$, the fast path is **linear**, $C_{\rm fast}=\mathcal{O}(N N_d)$, against the full search's $\mathcal{O}(N N_P N_d)$ — a *complexity-class* separation (the $O(N\!\cdot\!P\!\cdot\!D)\to O(N)+O(k^2)$ reframing of [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md), §D). Define the per-star cost ratio $\rho\equiv C_{\rm fast}/C_{\rm full}\ll1$.

### 8.2 Routing fraction

Let $f$ be the fraction of stars routed to the fast path (those presenting exploitable local evidence). For the planet-hosting population, $f$ is governed by the detectability law of §7:

$$f_{\rm planets}=\Pr\big(\mathrm{SNR}_1\ge z_\star\big)=\Pr\!\left[\Big(\tfrac{R_p}{R_\star}\Big)^2\ge z_\star\,\mathrm{CDPP}(T_{14})\right],$$

an integral over the joint radius / stellar-noise distribution. (For field stars, $f$ also includes the detector's false-trigger rate, §3b.)

### 8.3 Total compute

$$\boxed{\ \frac{C_{\rm comb}}{C_{\rm full}} = f\,\rho + (1-f) = 1 - f(1-\rho)\ \approx\ 1-f\quad(\rho\ll1).\ }$$

Compute saving $\approx f$: **the fraction routed to the fast path is, to first order, the fractional compute saved.** H1b ($C_{\rm comb}/C_{\rm full}\le0.70$) therefore requires $f\gtrsim0.30/(1-\rho)\approx0.30$.

### 8.3a Two-regime cost: fast-path-eligible vs. survey-representative

The boxed result omits the cost of *running the detector itself*. Restoring the per-star detector overhead $\rho_d \equiv C_{\rm det}/C_{\rm full}$, charged on **every** routed star, splits the accounting into two populations.

**Fast-path-eligible population** (every star presents exploitable local evidence; the Phase I injection sample). Each routed star costs $\rho_d + \rho$ instead of $1$:
$$\frac{C_{\rm comb}}{C_{\rm full}}\bigg|_{\rm elig} \approx \rho_d + \rho,\qquad \text{saving} \approx 1 - (\rho_d + \rho).$$
The scoped H1b ($\le 0.70$) is attainable here whenever $\rho_d + \rho \le 0.30$ — easily met for a cheap CPU detector and a narrow confirmation grid.

**Survey-representative population** (planet prevalence $\pi \ll 1$; planetless stars find no events and pay detector + full fallback). With fast-path fraction among planet hosts $f_p$:
$$\frac{C_{\rm comb}}{C_{\rm full}}\bigg|_{\rm survey} \approx (1+\rho_d) - \pi f_p\,(1 - \rho + \rho_d) \;\Rightarrow\; \text{saving} \approx \pi f_p - \rho_d.$$
Setting the saving to zero gives the **break-even prevalence**
$$\boxed{\ \pi^\star = \frac{\rho_d}{f_p}\ }.$$
Survey-scale saving exists **iff** $\pi > \pi^\star$. At TESS-realistic $\pi \sim 10^{-2}$ this demands $\rho_d \lesssim 10^{-2} f_p$ — an overhead so small that, in practice, **no survey-scale saving is available without a mechanism that skips the full search on no-evidence stars** (the clean-skip tier, which trades recall and is deferred to Phase II; [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md) §10, [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) §8). Phase I therefore claims compute superiority **only** on the fast-path-eligible population (H1b) and reports the survey curve $C_{\rm comb}/C_{\rm full}(\pi)$ and $\pi^\star$ descriptively (H1b-survey).

### 8.4 Recall–compute tradeoff (the master equation)

Because the fallback is full TLS, recall is lost only on fast-path-routed true planets that are mis-seeded or unconfirmed:

$$\boxed{\ \Delta R = R_{\rm comb}-R_{\rm full} = -\,f\,\big(1-r_{\rm seed}\,g\big)\ }$$

with $r_{\rm seed}=\Pr(\text{correct period seed}\mid\text{planet routed})$ and $g=\Pr(\text{gate confirms}\mid\text{correct seed})$. Juxtaposing §8.3 and §8.4 gives the **frontier**:

$$\text{saving}\approx f(1-\rho),\qquad \text{recall loss}\approx f(1-r_{\rm seed}g).$$

The design self-selects its safe regime: routing sends to the fast path exactly the high-$\mathrm{SNR}_1$ stars for which $r_{\rm seed}g\to1$ (§7), so $\Delta R\to0$ there even as $f$ — hence saving — grows. Non-inferiority is the operating condition $f(1-r_{\rm seed}g)\le\delta_{\rm NI}=0.02$ ([`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md), §6). **The whole scientific bet reduces to a single testable inequality.**

---

## 9. Bootstrap False-Alarm-Probability Framework

The cure for §5's uncalibrated score is a distribution-free null for the *maximized* statistic. Let $T_{\rm obs}=\max_P Z(P)$ be the observed peak over the scanned grid. Generate $B$ surrogate event sets $\{\hat t_i^{(b)}\}$ under $\mathcal{H}_0$ — either by **phase-scrambling** the event times or by drawing $k$ uniform times over the same span (preserving $k$ and baseline) — and recompute the maximized statistic $T^{(b)}=\max_P Z^{(b)}(P)$ over the **identical grid**. The false-alarm probability is the empirical exceedance

$$\widehat{\mathrm{FAP}}(\hat P)=\frac{1}{B}\sum_{b=1}^{B}\mathbb{1}\!\big[T^{(b)}\ge T_{\rm obs}\big]\ \ (\text{add-one smoothing for }B\ \text{finite}).$$

Because each surrogate is maximized over the same $N_P$ periods, the look-elsewhere effect is **automatically** absorbed — no analytic trials-factor approximation is needed. This $\widehat{\mathrm{FAP}}$ is the calibrated quantity that replaces v3's score; a candidate proceeds to the photometric gate (§6) only if $\widehat{\mathrm{FAP}}\le\alpha$ for a pre-registered $\alpha$ (H4 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md)). Validity rests on **exchangeability** of event times under $\mathcal{H}_0$; correlated noise weakens strict exchangeability, motivating block- or noise-model-aware resampling (§11).

**9.1 Committed resampling scheme (Phase I).** To preserve validity under correlated (red) noise — where strict i.i.d. phase-scrambling over-rejects — the surrogate null is generated by **noise-model-aware circular block bootstrap**, not i.i.d. scrambling:
1. Fit the per-sector GP / robust noise model (§2) to the conditioned residuals.
2. Generate $B$ surrogate residual series by **circular block bootstrap** with block length $L_b$ set to a fixed multiple of the larger of the GP correlation timescale and $T_{14}$ (multiple and $B$ frozen in [`TRINETRA_X_PHASE1_VALIDATION.md`](./TRINETRA_X_PHASE1_VALIDATION.md) Appendix A.8), preserving local correlation structure.
3. Re-run detection + period recovery on each surrogate over the **identical** period grid; record $T^{(b)} = \max_P Z^{(b)}(P)$.
4. Compute $\widehat{\mathrm{FAP}}(\hat P)$ as the add-one-smoothed exceedance of $T_{\rm obs}$ over $\{T^{(b)}\}$ (as above).

Block resampling restores approximate exchangeability at the block scale, so the look-elsewhere correction holds without assuming white noise. Validity is **verified empirically** on null calibration stars (H4 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md)): a nominal-$\alpha$ FAP cutoff must yield empirical false-alarm rate $\le \alpha$. This closes the open exchangeability assumption flagged above.

---

## 10. Known Mathematical Weaknesses Inherited from v3

Stated precisely so each has a corresponding fix in §11.

1. **Uncalibrated coherence score / unhandled look-elsewhere.** $\text{score}=\max_{\rm bin}/k$ saturates to 1 from noise at small $k$ over a fine period grid (§5): $\Pr[\text{score}=1]\to1$. No false-alarm probability existed. *(Dominant failure.)*
2. **White-noise contamination model.** Event-rate and recovery analyses assumed white noise (§3b) and, in simulation, **uniform i.i.d.** false events. Real noise is red and clustered; $\mathbb{E}[k_{\rm FP}]$ was underestimated and the $(1+\rho_{\rm FP})^{-2}$ fragility (§4b) understated — a passing simulation coexisted with a failing reality.
3. **Circular significance statistic.** The reported "SNR" was built from quantities the detection threshold *forces* to exceed $z_\star$, so by construction $\mathrm{SNR}_{\rm est}\gtrsim z_\star\sqrt{k}$ regardless of truth — non-discriminating.
4. **Timing coherence used as the verdict.** Phase concentration (§4–§5) was treated as detection; the photometric likelihood-ratio (§6) was never the gate. The evidence hierarchy was inverted.
5. **Harmonic / grid-edge pathologies.** Alias periods and period-grid boundary pile-ups were unscored, producing spurious accumulations at instrumental timescales.

---

## 11. Mathematical Improvements in TRINETRA-X

Each repair is a change of *statistics*, not of engineering.

1. **Calibrated period significance (§9).** Rayleigh/Hough peak with **bootstrap FAP** over the maximized statistic ⇒ look-elsewhere-correct, distribution-free. Replaces weakness 10.1.
2. **Photometric significance as the gate (§6).** Likelihood-ratio / Bayesian-evidence transit test on the folded data is the arbiter; timing only *seeds* it. Replaces 10.4. Closes the open loop of [`TRINETRA_CONCEPT_RECONSTRUCTION.md`](./TRINETRA_CONCEPT_RECONSTRUCTION.md) §E–§F.
3. **Red-noise-aware detection (§2).** Gaussian-process whitened matched filter $g^{\mathsf T}\Sigma^{-1}r/\sqrt{g^{\mathsf T}\Sigma^{-1}g}$ and noise-model-aware resampling. Replaces 10.2; restores validity of §3 yields under correlated noise.
4. **Empirical completeness, not modeled.** Recovery is measured by **injection into real light curves** (real $\Sigma$ preserved), so no white-noise assumption enters the recall map. Operationalizes A3/A4 of [`SCIENTIFIC_HYPOTHESIS.md`](./SCIENTIFIC_HYPOTHESIS.md).
5. **A true, sign-aware significance.** The discriminating statistic is the folded-transit $\Lambda$/SNR of §6, never the circular estimator of 10.3.
6. **Explicit alias and edge handling (§4 harmonics).** The alias set $\{mP/n\}$ is enumerated and resolved by photometric significance, not phase score; grid edges are guarded.
7. **Calibrated confidence downstream.** Conformal prediction supplies distribution-free coverage on the final planet probability ([`TRINETRA_X_ARCHITECTURE.md`](./TRINETRA_X_ARCHITECTURE.md), Stage 5) — the calibration mandate of [`TRINETRA-X.md`](./TRINETRA-X.md) at the system level.

---

## 12. Summary — the Theory in One Line

Evidence-first detection is the legitimate quantifier-inversion of the transit search **whenever** $\mathrm{SNR}_1\ge z_\star$ for the target population (§1–§2, §7); it buys a complexity-class reduction with compute saving $\approx f$ and recall cost $f(1-r_{\rm seed}g)$, so its entire validity is the inequality $f(1-r_{\rm seed}g)\le\delta_{\rm NI}$ (§8); and it is scientifically sound **only** when the verdict is the calibrated photometric significance of §6 and §9 — not the timing coincidence that undid v3 (§10–§11).

---

*Theoretical reference v1.1 (2026-06-15). Derivations are normative for the project. No implementation, results, or code appear here by design.*
