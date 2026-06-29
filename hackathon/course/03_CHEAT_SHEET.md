# TRINETRA-X — ONE-PAGE CHEAT SHEET (print me)
**Team TRINETRA-X · BAH 2026 · PS7 — AI exoplanet detection/classification from noisy TESS light curves**

### THE 10-SECOND LINE
Find planet dips cheaply → tell real planets from impostors **by shape (U vs V), not depth** → calibrated confidence. Built on a pre-registered, TLS-benchmarked research pipeline; validated on real MAST data.

### THE 5 PS7 STEPS (our pipeline mirrors them)
1. **Detrend** — wotan biweight, 2.5 d → flat residual.
2. **Identify** — cheap matched-filter detect dips → period from event *spacing*.
3. **Characterize** — trapezoid fit: depth, duration, **ingress/egress, flat-bottom**.
4. **Classify** — transit / eclipse / blend / other (physics features → GBT, optional CNN), conformal confidence.
5. **Significance** — per-event SNR + transit likelihood-ratio.

### THE ONE INSIGHT JUDGES WANT
Planet ≈ false positive in **depth** (~1.4%). **Shape separates them:** planet = **U** (long flat bottom, sharp ingress); EB/FP = **V** (pointy, short flat bottom, often secondary + odd-even). *Real data:* EB TIC 100029948 flat-frac **0.26**; Pi Men c **0.67**.

### KEY EQUATIONS (verbatim notation)
- Depth: **δ = (Rₚ/R⋆)²**
- Single-transit SNR: **SNR₁ = δ√n_in / σ = δ / CDPP(T₁₄)**; folded: **SNR_tot = SNR₁√N_tr**
- Period concentration: **Z(P)=k·R̄²**, R̄=|(1/k)Σe^{iφᵢ}|
- Bootstrap FAP: **FAP = (1/B)Σ 1[T^(b) ≥ T_obs]**, B=1000 (block bootstrap)
- Confirmer: **Λ = −2 ln[L(flat)/L(transit)]** (range-invariant; common FAR both arms)
- Compute: **C_comb/C_full ≈ 1 − f**; saving ≈ f; **recall loss ΔR = −f(1−r_seed·g)**
- Break-even: **π⋆ = ρ_d/f_p** (why survey-scale saving needs tiny overhead)

### RESEARCH RESULT (be proud of the honesty)
Pre-registered, sealed, TEST read **once**. **E1 recall PASS** (Δrecall −0.48 pp, lo95 −0.60 pp; replicated on real TOIs: Arm B = Arm A = 86.7%). **E2 compute FAIL** (24.4% < 30%; ρ_d 14.4%). → **H1 falsified on the compute branch** = a *successful negative result*. Cause: un-cheapenable B=1000 bootstrap entry tax + fallbacks; TESS baseline too short. Next: **Kepler scaling** (fold k events vs TLS N points; advantage should grow with baseline).

### VALIDATION (real labelled objects, 12)
Clean transiters (Pi Men, WASP-121, WASP-100) → U + literature-matching periods. EBs (RZ Cas + deep cache EBs) → V. Single-feature verdict 0.58 **but classes separate in 2-D depth×shape** → justifies multi-feature classifier. Misses = period recovery on pathological stars (AU Mic active, LHS 3844 alias, WASP-18 phase curve).

### HONEST LIMITS (say them — it's a strength)
- Shallow **blend vs planet** needs **pixel-level centroid/difference imaging** (round 2).
- **Period recovery** on active/short-period stars = the named round-2 fix.
- Classifier 0.82 is **synthetic** proof-of-path; real labels arrive round 2.

### ANALOGY KIT
Whisper in a stadium (signal vs noise) · airport metal-detector-first (routing) · cancer screen never-miss (recall>precision) · footsteps at 3:00/3:05/3:10 → period · U=cross spotlight center, V=clip edge · doctor uses many symptoms (multi-feature classifier).

### IF ASKED "WHY NOT JUST TLS?"
"TLS is the gold standard we *benchmark against*. Our claim is triage *efficiency at scale* — honestly falsified on TESS, testable on Kepler — plus a validated detection+classification spine that's useful right now. We don't replace TLS; we route to it."

### STACK
Python · lightkurve/astroquery (MAST) · wotan · transitleastsquares · batman · scikit-learn · (PyTorch optional) · conformal. Reproducible: frozen manifests, hash-sealed thresholds, by-star splits, one test read.

### TEAM
Ansul Suryawanshi (lead, IGNOU) · Riddhi Jain (IGNOU) · Samiksha Choudhary (Priyadarshini CoE, Nagpur).
