# Deliverable 2 — TRINETRA-X Knowledge Base & Interview Prep (200 Q&A)

> 50 Beginner · 50 Intermediate · 50 Advanced · 50 Expert. Answers are grounded in the repo; equations follow `docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md`.

---

## A. BEGINNER (1–50)

1. **What is an exoplanet?** A planet orbiting a star other than the Sun.
2. **What is a transit?** A planet passing in front of its star, briefly dimming it.
3. **What is a light curve?** A graph of a star's brightness over time.
4. **Why does a transit dim the star?** The planet blocks a small fraction of the star's light.
5. **How big is the dip for Earth?** ~0.008% (84 parts per million) of the Sun's light.
6. **How big for Jupiter?** ~1% (about 130× deeper than Earth).
7. **What does the dip's depth tell us?** The planet's size relative to the star: depth = (Rₚ/R⋆)².
8. **What does the spacing between dips tell us?** The orbital period (how long a "year" is).
9. **Why isn't one dip enough?** It could be noise, a glitch, or a cosmic ray; repetition proves a planet.
10. **What is TESS?** A NASA space telescope that measures the brightness of many stars to find transits.
11. **What is an eclipsing binary (EB)?** Two stars orbiting each other and blocking each other's light — a common planet impostor.
12. **What is a blend?** Light from another star mixed into the aperture, diluting/faking a signal.
13. **What is a "false positive" here?** A dip that looks planet-like but isn't a planet.
14. **What is the goal of TRINETRA-X?** Detect transits cheaply and tell real planets from impostors.
15. **What does TRINETRA mean?** "Third eye" — seeing what brute-force search misses.
16. **What is the "evidence-first" idea?** Do a cheap look first; do the expensive search only where there's evidence.
17. **What is TLS?** Transit Least Squares — the gold-standard transit search algorithm we compare against.
18. **Why is searching expensive?** Millions of stars, each needing thousands of trial periods.
19. **What shape is a planet's dip?** A rounded, flat-bottomed "U".
20. **What shape is an eclipsing binary's dip often?** A pointy "V".
21. **Why U vs V?** Geometry: a planet fully crosses the disk (flat bottom); grazing/stellar eclipses are pointier.
22. **What is detrending?** Removing slow drifts/systematics so the small dips stand out.
23. **What tool do we detrend with?** wotan (biweight method), 2.5-day window.
24. **What is noise in a light curve?** Random and systematic fluctuations that hide the signal.
25. **What is SNR?** Signal-to-noise ratio — how loud the signal is vs the background.
26. **What is recall?** The fraction of real planets we successfully find.
27. **What is precision?** The fraction of our "planet" calls that are actually planets.
28. **Why do we care more about recall?** A missed planet is unrecoverable; a false alarm is cheap to clear.
29. **What is the orbital period?** The time between consecutive transits.
30. **What is phase-folding?** Stacking the data by a trial period so repeated transits overlap.
31. **What is a "dip"?** A short decrease in brightness in the light curve.
32. **What is the hackathon (BAH 2026)?** ISRO's national space hackathon; we're on Problem Statement 7.
33. **What is PS7 asking?** AI detection + classification of exoplanet signals in noisy TESS light curves.
34. **What classes does PS7 want?** Transit, eclipse, blend, and other (systematics/spots).
35. **What is significance?** A number saying how unlikely the signal is to be noise.
36. **Is TRINETRA-X an AI model?** Phase I had no learned model (on purpose); the hackathon version adds a classifier.
37. **What data do we use?** Real TESS light curves from the MAST archive.
38. **What is MAST?** NASA's archive where TESS/Kepler data live.
39. **What is a "pipeline"?** A sequence of steps from raw data to a final answer.
40. **What is a starspot?** A dark patch on a star that makes brightness wiggle (not a planet).
41. **What is a secondary eclipse?** A smaller dip when the companion passes behind — an EB tell.
42. **What is odd-even depth difference?** Alternating transit depths — a sign of two stars, not a planet.
43. **Why is a deep dip suspicious?** Very deep dips are usually two stars, not a planet.
44. **What is a confirmed planet (TOI)?** A TESS Object of Interest verified as a real planet.
45. **Did TRINETRA-X find new planets?** No — it's a *method* test, validated on known objects.
46. **What was the main result?** It kept all the planets but didn't save enough compute on TESS.
47. **Is that a failure?** No — it's an honest, useful negative result that taught us where the idea works.
48. **What's next after the hackathon?** Test the idea on Kepler's longer data (Phase II).
49. **Who built this?** Ansul Suryawanshi (lead) and team, in the ISRO challenge context.
50. **In one sentence?** Find planet dips cheaply, tell real planets from impostors by shape, honestly tested.

---

## B. INTERMEDIATE (51–100)

51. **Write the transit depth formula.** δ = (Rₚ/R⋆)² — fractional dip = area ratio.
52. **Write single-transit SNR.** SNR₁ = δ√n_in/σ = δ/CDPP(T₁₄).
53. **What is CDPP?** Combined Differential Photometric Precision — noise averaged over a transit duration.
54. **Why does folding help?** SNR_tot = SNR₁·√N_tr — averaging N transits cuts noise by √N_tr.
55. **What sets transit duration?** T₁₄ ≈ (R⋆·P)/(πa); from Kepler's third law T₁₄ ∝ ρ⋆^(−1/3)·P^(1/3).
56. **What is BLS?** Box Least Squares — fits a rectangular dip across trial periods (fast, crude).
57. **How is TLS better than BLS?** It uses a realistic limb-darkened transit shape → more sensitive.
58. **What is SDE?** TLS's Signal Detection Efficiency — its significance score.
59. **What is a matched filter?** Sliding a known shape across data to find where it best matches.
60. **Why is a matched filter optimal?** It's the Neyman-Pearson optimal linear detector for a known shape in noise.
61. **What is red noise?** Correlated noise with slow drifts that mimics signals.
62. **Why is red noise dangerous?** Assuming white noise overstates significance → false planets.
63. **What is a Gaussian Process (GP)?** A model of correlated noise via a covariance kernel (timescale τ_GP).
64. **What is the whitened matched filter?** SNR₁^GP = gᵀΣ⁻¹r / √(gᵀΣ⁻¹g) — optimal under covariance Σ.
65. **How do we recover period from events?** Integer-comb / Rayleigh concentration of event phases.
66. **What is the Rayleigh statistic?** Z(P) = k·R̄², R̄ = |(1/k)Σe^{iφᵢ}| — measures phase clustering.
67. **What is a False-Alarm Probability (FAP)?** Probability noise produces a signal this strong.
68. **How do we compute FAP?** Block bootstrap: FAP = (1/B)Σ 1[T^(b) ≥ T_obs], B=1000.
69. **Why block (not point) bootstrap?** Blocks preserve correlation; point-shuffling fakes white noise.
70. **What is the look-elsewhere effect?** Searching many periods inflates the chance of a fluke; bootstrap absorbs it.
71. **What is the likelihood-ratio confirmer?** Λ = −2 ln[L(flat)/L(transit)] — compares transit vs no-transit.
72. **Why use Λ instead of just SNR?** It's the physical "is this a transit?" test, FAR-calibratable.
73. **What is ROC/AUC?** TPR-vs-FPR curve; AUC=1 perfect, 0.5 random. Our confirmer scored AUC≈0.88.
74. **What's sensitivity vs specificity?** Sensitivity=recall (TP rate); specificity=TN rate.
75. **What's the trapezoid model (hackathon)?** A symmetric transit: baseline, depth, total duration, ingress/egress, flat-bottom.
76. **What is flat-fraction?** flat-bottom ÷ total duration — high (~U/planet), low (~V/EB).
77. **Why does depth fail as a discriminator?** Planets and EBs/blends can share depth (~1.4%); shape separates them.
78. **What features does the classifier use?** Depth, duration, odd-even, secondary, flat-fraction, ingress-fraction, SNR, contamination.
79. **What model is the classifier?** Gradient-boosted trees (HistGradientBoosting), optional CNN ensemble.
80. **What is conformal prediction?** A calibration giving distribution-free confidence + abstention.
81. **What is occurrence weighting?** Weighting recall by real planet demographics (small planets dominate).
82. **Why weight by occurrence?** So "recall" reflects the planet population that actually exists.
83. **What does π̂ mean in the seal?** Prior detectable-planet fraction (3.17%) used in weighting.
84. **What is the routing fraction f?** Fraction of stars sent to the cheap fast path.
85. **What is the first-order compute saving?** ≈ f (the fraction routed): C_comb/C_full ≈ 1−f.
86. **What is ρ (rho)?** Per-star cost ratio of fast path vs full search (≪1).
87. **What is ρ_d?** Per-star detector+overhead cost charged on every routed star.
88. **What is the recall-loss formula?** ΔR = −f(1 − r_seed·g).
89. **What are r_seed and g?** P(correct period seed | routed) and P(gate confirms | correct seed).
90. **What's the non-inferiority condition?** f(1 − r_seed·g) ≤ δ_NI = 0.02.
91. **What is a leakage-safe split?** Splitting by star so one star's transits never span train and test.
92. **Why pre-register?** To freeze the experiment before seeing data, preventing self-deception.
93. **What is a seal?** A hash-frozen manifest of thresholds/data so results are tamper-evident.
94. **What is the fallback?** If the cheap path is unsure, run full TLS — never miss a planet.
95. **Why does fallback hurt compute?** Each fallback pays full TLS plus the bootstrap already spent.
96. **What is injection-recovery?** Inserting fake transits into real light curves to measure recovery.
97. **What is η (eta) in M2?** Transit-preservation fraction after detrending (we required ≥0.90).
98. **Why 2.5-day detrend window?** Short enough to kill systematics, long enough to keep transits (η≥0.90).
99. **What is the null pool?** Supposedly planet-free stars used to calibrate thresholds.
100. **What contaminated the null pool?** Unlabeled EBs/variables — cleaned via Prša 2022 + VSX + vetting.

---

## C. ADVANCED (101–150)

101. **State H1 and H0 precisely.** H1: evidence-first routing cuts compute vs full TLS while preserving recall; H0: it doesn't.
102. **What are E1 and E2?** E1 = recall non-inferiority (lo95 Δrecall ≥ −2 pp); E2 = scoped compute reduction ≥ 30%.
103. **What was the M4 verdict?** E1 PASS (Δrecall −0.48 pp, lo95 −0.60 pp); E2 FAIL (24.4%, ρ_d 14.4%) → H1 falsified (compute branch).
104. **Why did E2 fail mechanistically?** The un-cheapenable B=1000 bootstrap entry tax (ρ_d) + high fallback rate.
105. **What is Finding A?** TLS discards a narrow period window when it holds <100 periods → "targeted" search secretly ran full.
106. **What is Finding B?** TLS SDE is normalized across the searched grid → narrow-grid SDE not comparable to full-grid threshold.
107. **Why is Finding B fatal to targeted-TLS?** Arm B would reject planets Arm A keeps → E1 fails by construction.
108. **How did v3 repair it?** Replace targeted-TLS with epoch-fixed folded-transit Λ at a common false-alarm rate.
109. **What is the v3 fairness keystone?** "Same engine both arms" → "common false-alarm rate" (Arm A SDE≥T, Arm B Λ≥T_red).
110. **Why is Λ range-invariant?** It's computed at a fixed ephemeris over no period grid, so no grid-normalization.
111. **What is Lever-1b?** An attempt to replace the costly bootstrap with a cheaper equivalent FAP estimator.
112. **Why was Lever-1b dropped?** Both candidates (EVT/GPD, precomputed null) failed the TOST equivalence gate.
113. **What is equivalence (TOST) testing?** Proving a difference lies within a pre-set margin — "same," not just "not different."
114. **What is T_red?** The null false-alarm-rate threshold for the confirmer Λ; set to 0.0 (non-binding) in v3.
115. **What is the break-even prevalence π⋆?** π⋆ = ρ_d/f_p — survey-scale saving exists only if π > π⋆.
116. **Why no survey-scale saving on TESS?** At π~10⁻² you'd need ρ_d ≲ 10⁻²·f_p — far smaller than our overhead.
117. **What is the clean-skip tier?** Skipping full search on no-evidence stars — recall-risky, deferred to Phase II.
118. **What is the master equation?** ΔR = −f(1 − r_seed·g) (recall loss) with saving ≈ f(1−ρ).
119. **Why does the design self-select a safe regime?** High-SNR₁ stars route to fast path where r_seed·g→1, so ΔR→0 there.
120. **What are the sealed thresholds?** z⋆=3.4, z_mono=5.3, N_min=2, T=10.74, α_FAP=1%, ε=0.01.
121. **What is z_mono and why separate?** Monotransit threshold; single events are weaker, reported separately, excluded from headline.
122. **What is the contamination ratio ρ_FP?** k_FP/k_true; period recovery degrades as (1+ρ_FP)⁻².
123. **Why is period recovery quadratically fragile?** Coherent pairs / total pairs ≈ 1/(1+ρ_FP)².
124. **What is the v3 uncalibrated-score failure?** score=max_bin/k → Pr[score=1] ≈ 1 from noise at small k (≈0.9999 for k=3).
125. **How was the confirmer validated pre-test?** ROC/AUC on the cleaned null pool: epoch-fixed S/N AUC=0.877 (others 0.43, ≤0.72).
126. **How was anti-tuning enforced?** Frozen seals (hash-verified in-run), git diff over sealed docs empty, verdict pre-committed, TEST read once.
127. **What replicated on real planets?** M6 TOI recall 86.7%, Arm B = Arm A — corroborating E1 on real data.
128. **What was EB rejection in M6?** 12/16 known EBs rejected; 4 slipped through (genuine confirmer limit).
129. **What does T5-depth show?** Fitted depth biased −20% (coarse detector grid) — part of the wrong-epoch loss pathway.
130. **What is the dominant recall-loss pathway?** Cheap-confirm suppresses fallback; detector epoch less precise than TLS T₀.
131. **What is the two-regime cost model (§8.3a)?** Eligible: C/C_full ≈ ρ_d+ρ; survey: includes (1+ρ_d) − π f_p(1−ρ+ρ_d).
132. **Why is Phase I a "successful negative"?** It cleanly isolated where the principle holds (recall) vs fails (compute, short baseline).
133. **What stopping rule governs Phase I?** P-1…P-9; v3 is terminal — no v4; new ideas become new pre-registered experiments (P-8).
134. **What is the Phase II hypothesis?** The compute advantage scales with search-space size (fold k events vs TLS N points).
135. **Why might Kepler show savings TESS didn't?** TLS cost ∝ N_periods ∝ baseline; Kepler's 4-yr baseline → far larger N_periods.
136. **What is the M0 manifest?** Frozen target list + leakage-safe split (22,723 stars S1–S3; 6,925 cal / 15,798 test); Seal #1.
137. **What is Seal #2 / #2b?** M3 threshold seal (6292c018…) / v3 re-registration seal (54f06a94…).
138. **What is the GP-whitened detector advantage?** Avoids white-noise CDPP underestimating true noise on transit timescales for active stars.
139. **Why injection into *real* light curves?** Preserves real Σ (red noise) so the recall map has no white-noise assumption.
140. **What is the harmonic/alias problem?** P is degenerate under P/2, 2P, P/3…; resolved by photometric significance, not phase score.
141. **What is the hackathon's trapezoid validation result?** EB flat-frac 0.26 (V) vs Pi Men c 0.67 (U) — on real MAST data.
142. **What was the known-object validation accuracy?** Single-feature shape verdict 0.58; classes cleanly separable in 2-D depth×shape.
143. **Why is 0.58 not the real number?** It's a deliberately naive single feature; the multi-feature classifier is the actual system.
144. **What were the validation failure modes?** AU Mic (active star, wrong period), LHS 3844 (2× alias), WASP-18 (phase curve).
145. **What's the named pipeline weak spot?** Period recovery on pathological stars — the priority round-2 fix.
146. **Why can't light curves alone resolve blends?** Shallow blends mimic planets; need pixel-level centroid/difference imaging.
147. **What is the classifier's honest synthetic result?** 0.82 held-out; eclipse/other F1=1.00; transit↔blend the hard case.
148. **What does the depth×shape figure argue?** Neither feature alone suffices, but together the classes separate → multi-feature classifier justified.
149. **What is the conformal abstention for?** Output "uncertain" when classes overlap rather than force a wrong label.
150. **Why is reporting limitations a strength?** It signals expert-level understanding and avoids overclaiming to scientist judges.

---

## D. EXPERT (151–200)

151. **Is evidence-first ever provably optimal?** It's a recall-constrained triage; optimality depends on ρ_d vs fallback rate — both measured, per §8.
152. **Could a learned detector flip E2?** Possibly (fewer fallbacks/lower ρ_d), but Phase I excluded learning to isolate the principle; it's Phase II+ territory.
153. **Derive why saving ≈ f.** C_comb/C_full = fρ+(1−f) = 1−f(1−ρ) ≈ 1−f for ρ≪1.
154. **Derive π⋆.** Survey saving ≈ π f_p − ρ_d; set to 0 → π⋆ = ρ_d/f_p.
155. **Why is the look-elsewhere absorbed by bootstrap?** Each surrogate is maximized over the same N_P periods, so the max-distribution includes the trials factor.
156. **What breaks exchangeability and how is it handled?** Red noise; restored at block scale via circular block bootstrap (L_b = multiple of max(τ_GP,T₁₄)).
157. **Why common-FAR over common-engine?** Finding B made "same engine" statistically unfair across grid widths; FAR is the comparable currency.
158. **What's the statistical form of E1's test?** One-sided lower confidence bound on occurrence-weighted Δrecall vs a −2 pp non-inferiority margin.
159. **Why one-sided?** Non-inferiority only cares that recall isn't *worse* by more than the margin.
160. **What threatens the Kepler scaling test?** Different red-noise → re-calibrate thresholds; activity/alias period failures; bigger compute campaign.
161. **How would you falsify the scaling hypothesis?** A flat or non-monotonic compute-reduction-vs-baseline curve on Kepler.
162. **What's the danger of cheapening the bootstrap to win E2?** Tuning-to-win; only admissible behind an equivalence gate (which Lever-1b failed).
163. **Why is ΔBIC sometimes preferred to raw Λ?** It penalizes the transit model's extra parameters, guarding against overfitting noise.
164. **Limit of the trapezoid model?** Symmetric, ignores limb-darkening curvature; good for discrimination, not precise parameters (use batman/MCMC).
165. **How would you parameterize transits properly?** A limb-darkened model (e.g., Mandel-Agol via batman) with MCMC posteriors for uncertainties.
166. **Why is recall sacred vs precision?** Asymmetric loss: false negatives (missed planets) are unrecoverable; false positives are cheaply cleared by fallback.
167. **What's the role of CDPP in routing?** It sets the critical radius R_p,crit = R⋆√(z⋆·CDPP) — the bimodal fast-path boundary.
168. **Why are Jupiters efficient and Earths not (numerically)?** SNR₁^Jup/SNR₁^⊕ ≈ 11.2² ≈ 130; Jupiters single-transit-detectable, Earths need folding.
169. **What is the circular-significance pathology of v3?** "SNR" built from thresholded quantities is forced ≳ z⋆√k regardless of truth — non-discriminating.
170. **How does conformal prediction guarantee coverage?** Uses calibration-set nonconformity scores to build prediction sets with finite-sample marginal coverage.
171. **Why by-star (not by-transit) splits?** Transits of one star share systematics/noise; splitting by transit leaks information → optimistic metrics.
172. **What's the survey-representative endpoint?** A descriptive C_comb/C_full(π) curve + π⋆, reported (H1b-survey) rather than claimed.
173. **Why is monotransit excluded from the headline?** No repetition → FP control weaker by construction (can't distinguish a flare/one-off systematic).
174. **What's the Hough peak's meaning?** Number of phase-coherent events; it's the binned Rayleigh statistic, robust to missed transits.
175. **How do false events raise the Hough background?** By ~k_FP·w (flat background), while true events make a localized peak.
176. **What's the deepest reason TESS was the wrong stage?** Short 27-day baseline → small N_periods → small f / advantage; the win needs large search spaces.
177. **How does occurrence weighting change recall optimization?** It up-weights small planets (92.8% on Rₚ≤2), preventing optimizing for rare giants.
178. **Why validate completeness empirically not analytically?** Analytic recall assumes a noise model; injection into real LCs measures it with real Σ.
179. **What's the formal correction over v3 (one line)?** Photometric significance (§6, §9), not timing coincidence (§5), is the verdict.
180. **Why is the project credible despite falsifying H1?** Pre-registration + single sealed read make the negative trustworthy — unlike post-hoc positive claims.
181. **For the hackathon, what's the principled blend pipeline?** LC proxies (depth-consistency, odd-even, secondary, contamination) first; pixel-level centroid/difference imaging as the strong tier.
182. **How would a CNN complement the feature branch?** Global+local folded views capture morphology (asymmetry, ingress shape) hand features miss; ensemble for accuracy + interpretability.
183. **How do you prevent the classifier from learning survey artifacts?** Augment with injection-recovery into diverse real LCs; leakage-safe splits; calibrate thresholds off-test.
184. **What's the right metric suite for PS7 evaluation?** Per-class precision/recall/F1, macro-F1, confusion matrix, parameter |Δ|/true, calibration curve — recall-weighted.
185. **Why is the "massive planet" class subtle?** Deep but still U-shaped; depth→radius distinguishes giant planet from brown dwarf/star — needs stellar params.
186. **What's the statistical risk of the 0.82 synthetic number?** Synthetic labels may not match the organizer's distribution; real curated labels (round 2) are the true test.
187. **How does ρ_d connect theory to the E2 failure?** ρ_d=14.4% is exactly the §8.3a overhead term that pushes survey/eligible saving below 30%.
188. **Why keep B=1000 rather than fewer surrogates?** FAP resolution and tail accuracy at α=1% require enough surrogates; fewer would bias the gate.
189. **What's the add-one smoothing for?** Avoids FAP=0 for finite B (Laplace correction), giving a conservative, well-defined estimate.
190. **How would you scale the campaign cheaply (Kepler)?** Condition each 4-yr LC once then truncate to baselines; checkpoint; co-locate compute with MAST on AWS us-east-1 (zero egress).
191. **What's the cross-domain caution?** Evidence-first only beats the *right* incumbent in genuinely periodic-search domains — not aperiodic-anomaly strawmen.
192. **Why is "same data both arms" essential to E2?** Compute comparison is only fair on identical inputs; otherwise the ratio is meaningless.
193. **How do you defend the −2 pp margin?** Pre-registered, occurrence-weighted; reflects the maximum recall sacrifice deemed scientifically acceptable.
194. **What's the relationship between f and baseline?** Larger baseline → more transits per planet → higher SNR₁ at fixed depth → larger f (more routed) → bigger saving.
195. **Why is the negative result reusable?** It quantifies the overhead/π⋆ structure, giving a predictive model for *when* routing pays — a contribution beyond TESS.
196. **What would make routing win on TESS specifically?** A near-zero-overhead detector + a recall-safe clean-skip — i.e., Phase II machinery, not Phase I.
197. **How do you handle TTVs / multi-planet (out of scope)?** Phase I assumes single strictly-periodic body; interleaved periods/TTVs violate §4 and are excluded.
198. **What's the ethical/scientific value of reporting EB slip-through (4/16)?** Honest FP accounting; tells judges the confirmer's true operating point, not a cherry-picked one.
199. **If a judge says "just use TLS," your rebuttal?** TLS is the gold standard we *benchmark against*; our claim is about *triage efficiency at scale* — falsified on TESS, testable on Kepler, with a validated detection/classification spine that's directly useful now.
200. **Summarize TRINETRA-X as an expert.** A pre-registered evidence-first transit triage whose compute claim is honestly falsified on TESS (recall preserved, saving 24.4%<30% from un-cheapenable bootstrap overhead), whose mathematics and self-correction (Finding B→v3) are rigorous, and whose validated spine powers a calibrated, shape-based detection+classification pipeline for ISRO PS7 — with a Kepler scaling experiment as the principled next step.
