# Part 6 — Mathematics (verbatim from `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md` v1.2)

> **Rule honored:** equations below are reproduced **exactly** as in the canonical math doc (notation unchanged). Each is followed by a plain-English, step-by-step gloss — the gloss explains, it does not alter, the equation. Section numbers (§) reference the source doc.

## §0 Notation (the symbols you must know)
- $f(t)$ = observed flux; $r(t)$ = conditioned residual (a transit is a **negative** dip).
- $\sigma = 1.4826\,\mathrm{median}|r-\mathrm{med}(r)|$ — robust noise scale (MAD-based).
- $\Sigma$ = noise covariance (white $=\sigma^2 I$; red = non-diagonal).
- $\delta=(R_p/R_\star)^2$ = fractional depth; $T_{14}$ = transit duration; $n_{\rm in}=T_{14}/\Delta t$.
- $P$ period, $t_0$ epoch, $N_{\rm tr}$ transits in baseline; $k$ detected events; $z_\star$ detection threshold; $\Phi,\phi$ = normal CDF/PDF.

## §1 Evidence-first = inverting the quantifier order
Classical search tests, for each trial $(P,t_0,T_{14})$:
$$\mathcal{H}_1(P,t_0,T_{14}):\ r(t)= -\delta\,\Pi_{P,t_0,T_{14}}(t)+\varepsilon(t)\quad\text{vs.}\quad \mathcal{H}_0:\ r(t)=\varepsilon(t),$$
Evidence-first instead does a **local** test at each time, then asks which period explains the events:
$$\underbrace{\max_{P}\ \max_{t_0,T_{14}}\ \mathrm{LRT}(P,t_0,T_{14})}_{\text{hypothesis-first (BLS/TLS)}} \;\Longrightarrow\; \underbrace{\Big(\text{detect } \mathcal{E}\ \text{by local LRT}\Big)\ \to\ \Big(\inf_P \text{ explaining }\mathcal{E}\Big)}_{\text{evidence-first (TRINETRA)}}.$$
**Gloss:** instead of *assuming* a period and testing it across a giant grid (left), we *first* find dips (events $\mathcal{E}$), *then* deduce the period (right). Legitimate **iff** a real transit is individually significant (that's §2).

## §2 Local transit significance — the single most important equation
$$\boxed{\ \mathrm{SNR}_1=\frac{\delta\,\sqrt{n_{\rm in}}}{\sigma}=\frac{\delta}{\mathrm{CDPP}(T_{14})}\ }\qquad \mathrm{CDPP}(T_{14})\equiv \frac{\sigma}{\sqrt{n_{\rm in}}}.$$
**Gloss:** loudness of one transit = depth × √(in-transit points) ÷ noise. CDPP is "noise averaged over a transit." Folding many transits:
$$\mathrm{SNR}_{\rm tot}=\mathrm{SNR}_1\sqrt{N_{\rm tr}}=\frac{\delta\sqrt{N_{\rm tr} n_{\rm in}}}{\sigma}.$$
Duration from Kepler's third law:
$$T_{14}\simeq \frac{P}{\pi}\,\frac{R_\star}{a}=\frac{R_\star\,P}{\pi a},\qquad a=\left(\frac{G M_\star P^2}{4\pi^2}\right)^{1/3}\ \Rightarrow\ T_{14}\propto \rho_\star^{-1/3}P^{1/3}.$$
Red-noise-optimal (whitened) matched filter:
$$\mathrm{SNR}_1^{\rm GP}=\frac{g^{\mathsf T}\Sigma^{-1}r}{\sqrt{g^{\mathsf T}\Sigma^{-1}g}},$$
**Gloss:** with correlated noise, weight the data by $\Sigma^{-1}$; reduces to the boxed form when noise is white.

## §3 Event extraction
Threshold crossing of the matched-filter response:
$$s(t)=(r\star g)(t)<-z_\star\,\sigma_s,\qquad \sigma_s^2=\mathrm{Var}[s\,|\,\mathcal{H}_0].$$
True-event probability and false-event rate:
$$p_{\rm det}^{\rm (1)}=\Pr\!\big(\mathrm{SNR}_1\ \text{exceeds } z_\star \text{ given depth }\delta\big)=\Phi\!\big(\mathrm{SNR}_1-z_\star\big),\qquad \mathbb{E}[k_{\rm true}]=N_{\rm tr}\,p_{\rm det}^{(1)}.$$
$$\mathbb{E}[k_{\rm FP}]\approx \underbrace{\frac{T_{\rm base}}{T_{14}}}_{N_{\rm indep}}\ \Phi(-z_\star),\qquad \rho_{\rm FP}\equiv \frac{k_{\rm FP}}{k_{\rm true}}.$$
**Gloss:** recovered-transit count = #transits × detection prob; false events = #independent windows × tail prob. **Caveat (carried to §10):** the FP formula assumes *white* noise; real red noise inflates it — the root of v3's FP problem.

## §4 Period recovery
Rayleigh (circular) concentration:
$$Z(P)=k\,\bar R^2(P),\qquad \bar R(P)=\frac{1}{k}\left|\sum_{i=1}^{k} e^{\,\mathrm i\varphi_i(P)}\right|,\qquad \hat P=\arg\max_P Z(P).$$
Pairwise (number-theoretic) signal fraction:
$$\frac{\text{coherent pairs}}{\text{total pairs}}=\frac{\binom{k_{\rm true}}{2}}{\binom{k}{2}}\approx\frac{1}{(1+\rho_{\rm FP})^2}.$$
**Gloss:** if events are truly spaced by $P$, their phases pile up (R→1, Z≫1). False events degrade recovery **quadratically** $O((1+\rho_{\rm FP})^{-2})$ — the fundamental fragility. **Scope:** single, strictly-periodic body only (no multi-planet/TTV in Phase I).

## §5 Hough/voting + the look-elsewhere problem
$$\mathcal{H}(P,\varphi)=\sum_{i=1}^{k}\mathbb{1}\!\big[\,|\varphi_i(P)-\varphi|<w\,\big],\qquad \hat P=\arg\max_{P}\ \max_{\varphi}\ \mathcal{H}(P,\varphi).$$
The v3 uncalibrated score and why it's fatal:
$$\text{score}(P)=\frac{\max_{\rm bin}\text{count}}{k}\in[0,1],\qquad \Pr\!\big[\text{score}=1 \text{ somewhere}\big]\approx 1-\big(1-b^{1-k}\big)^{N_P}.$$
**Gloss:** for $k=3,b=10,N_P=10^3$ this ≈ 0.9999 — a *perfect score is essentially guaranteed from pure noise*. This is the precise mathematics of v3's false-positive engine; the fix is §9 (calibrate against the distribution of the maximum).

## §6 Photometric confirmation — the arbiter (the v3 gate)
$$\Lambda = -2\ln\frac{\mathcal{L}(\mathcal{M}_0)}{\mathcal{L}(\mathcal{M}_1)}\ \xrightarrow{\ \mathcal{H}_0\ }\ \chi^2_{\nu},\qquad \text{or, Bayesian, } \ \ln\!\frac{\mathcal{Z}_1}{\mathcal{Z}_0}\ (\text{evidence ratio}).$$
**Gloss:** compare a transit model $\mathcal{M}_1$ vs flat $\mathcal{M}_0$; large $\Lambda$ ⇒ transit preferred. **In v3 the fast-path gate IS exactly this $\Lambda$** — epoch-fixed at $(\hat P,\hat t_0)$, sign-aware, calibrated to a null false-alarm rate $T_{\rm red}$. Because it uses **no period grid**, $\Lambda$ is **range-invariant** — unlike TLS SDE (normalized across the searched grid) → that incomparability is **Finding B**. Arms held to a **common false-alarm rate**: Arm A via SDE $\ge T$, Arm B via $\Lambda\ge T_{\rm red}$ (the v3 fairness keystone).

## §7 Why Jupiters route efficiently (the bimodality)
$$\left(\frac{R_p}{R_\star}\right)^2\ge z_\star\,\mathrm{CDPP}(T_{14})\ \Longleftrightarrow\ R_p\ge R_{p,\rm crit}=R_\star\sqrt{z_\star\,\mathrm{CDPP}},\qquad \frac{\mathrm{SNR}_1^{\rm Jup}}{\mathrm{SNR}_1^{\oplus}}\approx 11.2^2\approx 1.3\times10^2.$$
**Gloss:** there's a **critical radius**; above it one transit is significant (Jupiters → fast path, $r_{\rm seed}\to1$); below it (Earths) you must fold many transits → correctly fall through to full search. The paradigm claims its win *only* on the high-SNR$_1$ tail.

## §8 Complexity, routing fraction, and the master tradeoff
Costs:
$$C_{\rm full}=\mathcal{O}\!\big(N_P\,(N+N_\varphi N_d)\big)=\mathcal{O}(N\,N_P\,N_d),\qquad C_{\rm fast}=\mathcal{O}(N N_d)\ (\text{linear; }k\ll N).$$
Total compute and the **first-order saving = routed fraction**:
$$\boxed{\ \frac{C_{\rm comb}}{C_{\rm full}} = f\,\rho + (1-f) = 1 - f(1-\rho)\ \approx\ 1-f\quad(\rho\ll1).\ }$$
Two-regime cost (restoring detector overhead $\rho_d$):
$$\frac{C_{\rm comb}}{C_{\rm full}}\bigg|_{\rm elig} \approx \rho_d + \rho,\qquad \frac{C_{\rm comb}}{C_{\rm full}}\bigg|_{\rm survey} \approx (1+\rho_d) - \pi f_p\,(1 - \rho + \rho_d),\qquad \boxed{\ \pi^\star = \frac{\rho_d}{f_p}\ }.$$
The **master equation** (recall–compute frontier):
$$\boxed{\ \Delta R = R_{\rm comb}-R_{\rm full} = -\,f\,\big(1-r_{\rm seed}\,g\big)\ },\qquad \text{saving}\approx f(1-\rho),\ \ \text{recall loss}\approx f(1-r_{\rm seed}g).$$
**Gloss:** $f$ = fraction routed to fast path; $\rho$ = per-star cost ratio; $\rho_d$ = detector overhead; $\pi$ = planet prevalence; $r_{\rm seed}$ = P(correct period seed | routed), $g$ = P(gate confirms | correct seed). **Saving ≈ f; recall loss ≈ f(1−r_seed·g).** Non-inferiority condition: $f(1-r_{\rm seed}g)\le\delta_{\rm NI}=0.02$. **The whole scientific bet reduces to one inequality.** Survey-scale saving exists **iff** $\pi>\pi^\star=\rho_d/f_p$ — and at TESS prevalence this needs a clean-skip mechanism (deferred to Phase II). *This $\pi^\star$/$\rho_d$ structure is exactly why E2 failed: the detector+bootstrap overhead $\rho_d$ was too large.*

## §9 Bootstrap False-Alarm-Probability (the calibration cure)
$$\widehat{\mathrm{FAP}}(\hat P)=\frac{1}{B}\sum_{b=1}^{B}\mathbb{1}\!\big[T^{(b)}\ge T_{\rm obs}\big]\ \ (\text{add-one smoothing for }B\ \text{finite}),\qquad T_{\rm obs}=\max_P Z(P).$$
**Gloss:** simulate $B$ noise surrogates (Phase I: **circular block bootstrap**, block $L_b$ = multiple of max(τ_GP, $T_{14}$)), recompute the maximized statistic, count how often noise beats you. Because each surrogate is maximized over the same $N_P$ periods, **look-elsewhere is absorbed automatically**. Proceed to the gate (§6) iff $\widehat{\mathrm{FAP}}\le\alpha$. **§9.1a:** v3 allowed a *cheaper equivalence-gated* estimator (EVT/GPD or precomputed null) — but it had to be numerically equivalent; **both candidates failed the gate, so the B≥1000 bootstrap stands** (the un-cheapenable entry tax).

## §10→§11 v3 weaknesses → TRINETRA fixes (one-to-one)
1. Uncalibrated score (Pr[score=1]→1) → **bootstrap FAP** (§9).
2. White-noise model understated red-noise FPs → **GP-whitened detection + block bootstrap**.
3. Circular "SNR" (forced ≳ $z_\star\sqrt{k}$) → **sign-aware folded $\Lambda$** (§6).
4. Timing coherence used as verdict → **photometry is the judge** (§6).
5. Harmonic/grid-edge pile-ups → **explicit alias enumeration + resolve by photometric significance**.
(+ conformal calibration downstream.)

## §12 The theory in one line (verbatim)
> Evidence-first detection is the legitimate quantifier-inversion of the transit search **whenever** $\mathrm{SNR}_1\ge z_\star$ for the target population (§1–§2, §7); it buys a complexity-class reduction with compute saving $\approx f$ and recall cost $f(1-r_{\rm seed}g)$, so its entire validity is the inequality $f(1-r_{\rm seed}g)\le\delta_{\rm NI}$ (§8); and it is scientifically sound **only** when the verdict is the calibrated photometric significance of §6 and §9 — not the timing coincidence that undid v3 (§10–§11).
