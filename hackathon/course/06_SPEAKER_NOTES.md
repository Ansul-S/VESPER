# Deliverable 5 — Complete Speaker Notes (Teaching Deck, 26 slides)
### For each slide: what to SAY, where to PAUSE, the ANALOGY, and likely FOLLOW-UPS. This is the script behind `TRINETRA_X_course.pdf`.

> Delivery rules: one idea per slide; pause after every analogy (let it land); never read bullets verbatim — expand them; always end a technical slide with the intuition.

---

**S1 — Title.** SAY: "TRINETRA‑X — teaching an AI to find planets in starlight, and to be honest about it." PAUSE. "By the end you'll explain this to a 10-year-old *or* a NASA scientist." FOLLOW-UP: *What's TRINETRA?* → "Sanskrit 'third eye' — seeing what brute force misses."

**S2 — The big question.** SAY: humanity knew one planetary system; since 1995 we've found ~6,000. Core questions: are we alone, how common are Earths. ANALOGY: we thought ours was the only house; then a telescope showed a city of lights. PAUSE. FOLLOW-UP: *Found life?* → "No — planets and sizes; biosignatures are the next telescopes."

**S3 — Needle in the haystack.** SAY: a star is blinding; a planet is a dark speck — we detect its *effect*, not the planet. ANALOGY (land hard): "finding a planet is hearing one whisper in a stadium of 50,000 fans." PAUSE 2s. NUMBER: Earth dims the Sun by 84 ppm. FOLLOW-UP: *Bigger telescope?* → "It's contrast, not size — indirect methods sidestep it."

**S4 — Four methods.** SAY: wobble (radial velocity), dim (transit ← ours), image (rare), microlens. Transit dominates because one camera watches 10⁴–10⁵ stars. ANALOGY: feeling a rope tug vs noticing a moth cross a streetlight. FOLLOW-UP: *Best method?* → "Complementary — transit gives size, RV gives mass; together → density."

**S5 — The compute enemy.** SAY: you don't know the period, so you try thousands per star, across millions of stars — cost ≈ N_periods×N_data×N_stars. ANALOGY: a million locked doors, trying *every key* on each. PAUSE. KEY: most stars are empty, yet blind TLS pays full price on all. FOLLOW-UP: *Just buy compute?* → "You can; the *science* question is whether you can be smarter."

**S6 — Light curve & transit.** SAY: brightness vs time = a star's EKG; a planet crossing makes a tiny repeating dip. EQUATION (define first): depth = (Rₚ/R⋆)² — area ratio. ANALOGY: a bug crossing a flashlight beam. FOLLOW-UP: *Why repeating?* → "It orbits; it crosses every period."

**S7 — Imposters & the U/V tell.** SAY: a dip can be a planet, two stars (EB), a blend, or junk/spots. The shape betrays them: planet = rounded **U**; EB = pointy **V**, often with a secondary dip and unequal odd/even depths. ANALOGY (doctor): same symptom (cough), different disease — you need more features. PAUSE. THIS IS THE HACKATHON KEYSTONE — say it twice. FOLLOW-UP: *Isn't a dip always a planet?* → "No — that's the central trap; deep V's are usually two stars."

**S8 — Depth, spacing, period.** SAY: depth→size, spacing→period, repetition→reality. One dip could be a glitch; three evenly-spaced identical dips is a planet's signature. ANALOGY: a knock at exactly every 10 minutes isn't the wind. FOLLOW-UP: *One dip (monotransit)?* → "Period ambiguous; out of Phase-I scope, reported separately."

**S9 — BLS vs TLS (+ a landmine).** SAY: BLS fits a box (fast, crude); TLS fits the *real* transit shape (sensitive, slow) and outputs SDE — it's our gold-standard benchmark. ANALOGY: square cookie-cutter (BLS) vs custom mold (TLS). LANDMINE (foreshadow): "TLS's SDE is normalized over *the grid you search* — remember this, it later breaks a naive idea." FOLLOW-UP: *Is TLS bad?* → "No — excellent, just uniformly expensive."

**S10 — Birth of TRINETRA‑X.** SAY: blind TLS treats empty and promising stars identically — so route on *evidence*: cheap glance first, expensive search only where it beeped. ANALOGY (fixed airport): metal-detector first; full search only on beeps — same safety, far less work *if* the cheap step never misses a threat. FOLLOW-UP: *What's the cheap glance?* → "A matched-filter dip detector — Slide 14."

**S11 — Prime directive.** SAY: "Find evidence first, spend computation second, let physics decide." Recall > precision — a false alarm is fine; a *missed planet* is unforgivable. Physics (depth/shape/repetition), not timing luck, decides. ANALOGY (cancer screen): never miss the tumor, tolerate false alarms. FOLLOW-UP: *Why tolerate false positives?* → "A cheap second look clears them; a missed planet is gone forever."

**S12 — The hypothesis.** SAY: H1 = cut compute vs TLS *without* losing planets; H0 = it doesn't. Two endpoints: E1 recall non-inferiority (don't lose planets), E2 compute reduction ≥30%. PAUSE. "We froze this *before* touching test data — that's what makes the answer trustworthy." FOLLOW-UP: *What if only one passes?* → "Then the claim is partly falsified — exactly what happened."

**S13 — Architecture (show arch_diagram.png).** SAY: condition → cheap detect → period from spacing → bootstrap FAP → likelihood-ratio confirmer → full-TLS fallback → evaluate. The savings come from folding **k events** instead of searching **N points × grid**. ANALOGY: triage in an ER — quick vitals route you; only some get the CT scan. FOLLOW-UP: *Where's the saving exactly?* → "Only on the confirmed-cheap path; fallbacks pay full price — Slide 18."

**S14 — Module deep-dive.** SAY (walk each): Detector = box matched filter, SNR=depth/scatter. Period-from-spacing = read P off event spacing (Rayleigh Z=k·R̄²). FAP = block bootstrap, 'is this periodicity real or lucky noise?' Confirmer = Λ, the *physics* arbiter. Fallback = if unsure, run full TLS (never miss). PAUSE per module. FOLLOW-UP: *Why block bootstrap?* → "Real noise is correlated; shuffling blocks preserves that, so significance isn't faked."

**S15 — Five math anchors.** SAY: (1) δ=(Rₚ/R⋆)² depth↔size; (2) SNR₁=δ/CDPP detectability; (3) FAP=Σ1[T^b≥T_obs]/B honesty; (4) Λ=−2ln[L₀/L₁] the judge; (5) saving≈f, ΔR=−f(1−r_seed·g) the whole bet. ANALOGY: five load-bearing pillars; everything rests on them. FOLLOW-UP: *Intuition for SNR₁?* → "100 people whispering the same word become audible — √N averaging."

**S16 — The research journey (timeline).** SAY: idea → build/calibrate (M0–M3, sealed) → **crisis: Finding B** (TLS SDE grid-normalized → 'targeted TLS' design invalid) → **repair: v3** (Λ at common FAR; tried to cheapen the bootstrap but equivalence test said no) → the one sealed test. ANALOGY (detective): caught a flaw in our own case *before* the verdict and fixed it in the open. FOLLOW-UP: *Isn't changing the design cheating?* → "Not if you re-register transparently before seeing test data — which we did."

**S17 — The verdict (show numbers).** SAY: test read **once**, verdict pre-committed. **E1 PASS** (Δrecall −0.48 pp) — recall preserved. **E2 FAIL** (24.4% < 30%) — compute claim falsified. PAUSE 3s. "H1 falsified on the compute branch — and that's a *successful* negative result." FOLLOW-UP: *Why believe it?* → "Pre-registered, sealed, read once — credible by construction."

**S18 — Why it failed + the scaling insight.** SAY: the killer was an un-cheapenable B=1000 bootstrap 'entry tax' (ρ_d≈14.4%) + too many fallbacks; theory says π⋆=ρ_d/f_p, so short baselines can't win. INSIGHT: the fast lane folds k events while TLS cost grows with baseline → **the advantage should grow with search-space size** → test on Kepler. ANALOGY: a shortcut that only pays off on a long highway, not a short street. FOLLOW-UP: *So routing is useless?* → "On TESS, yes; the math points to Kepler — and the detection spine is validated regardless."

**S19 — Milestones M0–M7.** SAY (one line each): M0 sealed dataset; M1 conditioning; M2 picked 2.5-day window by injection; M3 calibrated thresholds (+cleaned EB-contaminated null); M4 the verdict; M5–M7 characterization + reality check (real TOIs: Arm B=Arm A=86.7%) + manuscript. ANALOGY: building+pressure-testing a bridge before driving across once. FOLLOW-UP: *Why so much before one test?* → "Because you only get one honest read."

**S20 — The hackathon pivot (PS7).** SAY: same validated spine, new mission — *classify* dips for ISRO PS7: detrend → identify → characterize → classify → significance. The committee's key point = our keystone: depth doesn't separate planet from FP, **shape does**. ANALOGY: same engine, new race. FOLLOW-UP: *Is this the falsified part?* → "No — this uses the *validated* detection/classification spine; compute-routing isn't what PS7 grades."

**S21 — Characterization (show characterization.png).** SAY: we fit a trapezoid and report exactly the committee's parameters; on real data the EB is flat-fraction 0.26 (V), Pi Men c is 0.67 (U). PAUSE. "Depth is nearly equal — the *shape* decides." FOLLOW-UP: *Trapezoid too crude?* → "For discrimination it's robust; for precise params we'd use batman+MCMC."

**S22 — Classification + validation (show validation_known.png).** SAY: physics features → gradient-boosted classifier with calibrated confidence; validated on 12 known objects — clean planets U + literature periods, EBs V; a single feature gives 0.58 but the classes separate cleanly in 2-D depth×shape → that's why we use *many* features. ANALOGY: a doctor uses many symptoms, not one. FOLLOW-UP: *82%?* → "Synthetic proof-of-path; real labels arrive round 2; eclipse/other already near-perfect."

**S23 — Current status + roadmap.** SAY: Phase I sealed/final; round-1 package complete (submit by July 1); round-2 = robust period recovery, pixel-level centroid for blends, CNN ensemble, full report; research future = Kepler scaling. FOLLOW-UP: *Biggest risk?* → "Period recovery on active/short-period stars — named and planned."

**S24 — The story.** SAY (slow, narrative): humanity learns to hear planets by watching stars blink; the gold-standard detective interrogates everyone; a 'third eye' proposes to glance first; a hidden statistical trap nearly fakes a failure; we catch and fix it; the one honest look says 'planets kept, savings missed'; the lesson points to a bigger stage. PAUSE. "Failure with a lesson is how science moves."

**S25 — Pitch ladder.** SAY: practice 30s / 1m / 3m / 5m / 10m / 15m / 30m versions (see audience scripts). For judges default to the 2-minute judge script. FOLLOW-UP: handle by switching to the matching script.

**S26 — Master summary + why it matters.** SAY: one hypothesis, one architecture, one honest verdict, one forward path. "It's rare — a project with the integrity to falsify its own headline while proving its core works, and turn that into both a future experiment and a working tool." CLOSE: "That story — intuition + mathematics + honesty — is what makes me the expert on my own work." PAUSE. Thank the audience.

---
### Universal follow-ups (have these ready on any slide)
- *"Did you find a new planet?"* → "No — it's a method test, validated on known objects; discovery isn't the claim."
- *"Why should I trust the numbers?"* → "Pre-registered, hash-sealed, test read once."
- *"What's genuinely new?"* → "Evidence-first routing as a falsifiable, quantified triage + shape-based calibrated classification."
- *"What's the weakest part?"* → "Period recovery on pathological stars and shallow-blend ID — both named, both round-2."
