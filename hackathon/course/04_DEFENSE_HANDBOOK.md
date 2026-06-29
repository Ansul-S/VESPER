# Deliverable 6 — Defense & Judge Handbook
### Difficult questions, criticisms, and evidence-based responses. Defend the *science*, not just the demo.

> **Golden rules of defense:** (1) Concede what's true, then reframe. (2) Always cite evidence (a number, a figure, a doc). (3) Never close on the negative — end on the forward path. (4) If you don't know, say "we haven't tested that yet; here's how we would."

---

## A. The hardest single question, fully scripted
**"You falsified your own hypothesis — why is this a project, not a failure?"**
> "Because it's a *trustworthy* result, which is rare. We pre-registered the experiment, sealed the thresholds with hashes, and read the test set exactly once with the verdict committed in advance — so our negative is credible in a way most positive claims aren't. And it's a *precise* negative: recall non-inferiority **passed** (Δrecall −0.48 pp, and on real confirmed planets our routed arm matched full TLS at 86.7%); only the compute branch failed (24.4% vs a 30% bar). We even diagnosed the exact cause — an un-cheapenable bootstrap overhead, ρ_d ≈ 14.4%, which our own theory (π⋆ = ρ_d/f_p) predicts kills savings on a short baseline like TESS. That diagnosis *generated* a testable follow-up: the advantage should grow with search-space size, which Kepler can test. Meanwhile the detection/classification spine the test validated is exactly what powers this hackathon entry. Honest falsification that produces a new hypothesis and a working tool is science working as intended."

---

## B. Skeptical hackathon judge
- **"Your accuracy is 82% — that's mediocre."** → "That 82% is on *synthetic* labels as a proof-of-path; the real classifier trains on your curated set in round 2. More importantly, eclipse and 'other' are near-perfect; the only confusion is transit↔blend, which is *physically* degenerate at low SNR — and our validation figure shows the classes separate cleanly once you use depth *and* shape together. The single-feature 0.58 baseline is there precisely to motivate the multi-feature model."
- **"Anyone can run lightkurve + a classifier."** → "The differentiator isn't the libraries; it's (1) the committee-aligned **shape-based** discrimination reproducing your slide-5/6 output on real data, (2) **calibrated** confidence (conformal, not raw softmax), and (3) a **pre-registered, TLS-benchmarked** research foundation with honest limitation analysis. We validated on 12 known objects — most teams won't have touched real labelled data by round 1."
- **"Show me it works on a planet we didn't pick."** → "Pi Mensae c: blindly recovered by TLS at P=6.262 d (lit 6.268), depth 289 ppm (lit ~315), and characterized as U-shape. We can run any TIC you name live."
- **"What if your detrending erased a real transit?"** → "We tested exactly that in M2: injection-recovery measured transit-preservation η; we chose the 2.5-day window because it keeps η ≥ 0.90 for Rₚ ≥ 2 R⊕. We don't assume preservation, we measured it."

## C. The professor (methodology)
- **"How do you know you didn't tune to the test set?"** → "Structurally impossible by design: thresholds are hash-sealed on calibration before the test; `git diff` over the sealed docs is empty at test time; the verdict mapping was pre-committed; the test was read once. This is the anti-tuning contract (Non-Negotiable #2)."
- **"Your null sample — was it actually planet-free?"** → "No, and we caught it: the null pool was contaminated with unlabeled EBs/variables. We cleaned it with Prša 2022 + VSX cross-match + automated vetting (146 of 1000 removed) before calibration. Auditing the control is part of the rigor."
- **"Isn't a trapezoid a crude transit model?"** → "Yes — deliberately. For *discrimination* (U vs V) it's robust and fast; for *precise parameters* we'd use a limb-darkened model (batman) with MCMC posteriors. We use the right tool per task and say so."
- **"Why is your recall metric occurrence-weighted?"** → "Because unweighted recall would let us optimize for rare giant planets. Weighting by real demographics (Kunimoto & Matthews 2020; 92.8% of weight on Rₚ ≤ 2 R⊕) makes 'recall' reflect the population that actually exists."

## D. NASA scientist
- **"TLS is well-calibrated and fast enough. What do I gain?"** → "On TESS, by our own test: not enough (24%). The value is at long baselines — TLS cost scales with N_periods ∝ baseline, while our fast lane folds k events regardless. That's the Kepler scaling experiment we've designed. We're not claiming a TESS win; we're reporting an honest TESS result and a principled path to where it should pay off."
- **"Red noise destroys naive significance — how do you handle it?"** → "Two ways: a GP-whitened matched filter (gᵀΣ⁻¹r/√(gᵀΣ⁻¹g)) for detection, and a circular *block* bootstrap for the period FAP so the look-elsewhere correction holds without assuming white noise. We verified the FAP empirically on null calibration stars."
- **"Your confirmer — why a likelihood ratio at common FAR, not a shared engine?"** → "Because of Finding B: TLS's SDE is normalized across the searched grid, so a narrow-grid SDE isn't comparable to the full-grid threshold — a 'same engine' comparison is statistically unfair. A fixed-ephemeris Λ is range-invariant; holding both arms to a common false-alarm rate is the fair currency."

## E. ISRO scientist
- **"Crowded fields and blends dominate real data — are you robust?"** → "Partially, honestly. Light-curve features (depth-consistency vs stellar radius, odd-even, secondary, TIC contamination ratio) give a first cut. Robust blend rejection needs **pixel-level centroid / difference imaging** from Target Pixel Files — that's explicitly our round-2 build. We report this limit rather than overclaim."
- **"Can this run on PARAM / our infrastructure?"** → "Yes — it's containerizable and CPU-parallel; MAST data is co-located on AWS Open Data (us-east-1) for zero egress, or it runs on HPC batch. The campaign is embarrassingly parallel."
- **"What's the scientific contribution beyond a tool?"** → "A quantified model of *when* evidence-first routing pays: saving ≈ f, recall loss ≈ f(1−r_seed·g), break-even π⋆ = ρ_d/f_p — a reusable predictor, validated by an honest TESS falsification."

## F. AI researcher
- **"Why gradient boosting, not deep learning?"** → "Interpretability, small-data robustness, and the committee's explicit steer to classify on *shape parameters*. The GBT feature branch is the core; a CNN on global+local folded views is an optional ensemble for morphology we can't hand-craft. We don't add DL for fashion."
- **"How is your confidence calibrated?"** → "Conformal prediction — distribution-free marginal coverage with an abstention option, rather than an uncalibrated softmax. Calibrated confidence is a project non-negotiable."
- **"Data leakage?"** → "Splits are by *star*, never by transit, so one star's systematics can't leak across train/test; thresholds set on calibration then frozen; augmentation via injection into real light curves."
- **"Your classes are imbalanced and the hard case is transit↔blend — isn't that fatal?"** → "It's the *real* difficulty, not an artifact. We handle imbalance with class weights and recall-weighted evaluation, and we resolve transit↔blend with pixel-level features rather than overfitting the light curve. Reporting where it's hard is the point."

## G. Methodology & experimental-design defense (the deep cut)
- **Pre-registration:** the experiment (H1/H0, E1/E2, thresholds, verdict mapping) was frozen and tagged (`phase1-prereg-v2`, then `-v3`) before the test read.
- **Single read:** the TEST set was quarantined at M0 and read once at M4 — the one irreversible evaluation.
- **Amendment discipline:** when Finding B invalidated the design, we *re-registered transparently* (DR-002, v3) and re-dated the seal — we did not silently move goalposts.
- **Equivalence gating:** the attempted bootstrap speedup (Lever-1b) had to pass a TOST equivalence test; it failed, so we kept the expensive reference — refusing a speedup that would have manufactured an E2 pass.
- **Benchmark fairness:** both arms run on identical injected data; compute is compared like-for-like; arms held to a common false-alarm rate.
- **External validity:** recall replicated on *real* confirmed planets (not just synthetic injections).

## H. Traps to avoid (don't do these)
- ❌ Claiming the compute thesis succeeded. (It didn't on TESS — say so.)
- ❌ Citing 0.82 as "our accuracy" without "synthetic / proof-of-path / round-2 real labels."
- ❌ Overclaiming blend rejection from light curves alone.
- ❌ Saying "we beat TLS." (We benchmark against it; we route to it.)
- ❌ Hiding the period-recovery weak spot. (Naming it builds credibility.)

## I. One-line rebuttals (rapid fire)
- "Negative result?" → "Trustworthy because pre-registered; recall passed, compute didn't, on a baseline too short — Kepler tests the fix."
- "Just libraries?" → "Calibrated, shape-based, benchmarked, validated on real labels — and honest about limits."
- "Why shape not depth?" → "Your own slides: same depth, different shape. We fit the shape."
- "Will it scale?" → "That's the literal next experiment; the math says yes, the data will judge."
