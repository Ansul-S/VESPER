# VESPER — Deep Scientific & Mathematical Review (panel format)

| Field | Value |
|---|---|
| **Date** | 2026-07-19 (delivered in-session; persisted 2026-07-20) |
| **Nature** | Idea-level review — *is the core scientific idea sound, novel, scalable, worth years of investment?* No implementation content. Panel stance: mathematician · ML researcher · exoplanet astrophysicist · statistician · signal-processing expert · systems architect · hostile referee · skeptical VC. |
| **Basis** | Sealed Phase-I record incl. DR-003 chain, the 2026-07-19 second-pass audit, line-level knowledge of the sealed code, the edge-control result. |
| **Consequence** | Directly motivates the Phase-II re-scoping ([`VESPER_PHASE2_PROGRAM.md`](../VESPER_PHASE2_PROGRAM.md)). |

## 1. The core idea, sharpened

Folding exists only to build SNR by coherent stacking. If a transit is individually visible (per-event SNR₁ ≥ threshold), the fold is redundant for *detection* and needed only for *characterization*. Evidence-first routing bets that the individually-visible population is large enough, and the cheap path cheap enough, to change survey economics. Phase I falsified the economics honestly — and the falsification is **structural, not implementational**:

**The bound the project never wrote down.** Coherent SNR ≈ SNR₁√K; the fast path serves SNR₁ ≥ z while the full search serves SNR₁ ≥ z/√K. Occurrence is dominated by small planets in the stacking-required band (92.8% of the frozen weight at Rₚ ≤ 2 R⊕, where the sealed run measured both arms near zero recall at Rₚ=1). Hence for any router in this class: survey saving ≤ π·f_p(z)·(1−ρ) − ρ_d. With the sealed numbers (f_p ≈ 0.211, π̂ ≈ 0.032), even ρ_d → 0 leaves ≈ 0.6%. E2's failure is the empirical shadow of population structure. π\* ≈ 0.68 ≫ π̂ is the same fact.

**Two premise-level attacks the project had not faced:**
1. **Kepler-TPS/FFA decomposition.** Precompute per-cadence single-event statistics (≈ the VESPER detector) and fold *them* cheaply (fast-folding algorithm, O(N log N) over all periods). The "expensive coherent search" is largely an artifact of pricing against TLS. VESPER routed around a tollbooth on a road with a free parallel lane. → Phase-II gating experiment **G0**.
2. **Wrong scarce resource.** Survey CPU is cheap; vetting attention and followup are not. VESPER's calibrated-evidence machinery is a candidate-management engine wearing a compute-saver costume.

## 2. First-principles reformulation

The optimal form of "evidence-first" is **sequential analysis** (SPRT/generalized sequential tests): accumulate evidence per star in cheap increments, stop at calibrated error boundaries. VESPER's 2-stage binary router is its 1-bit quantization, and the measured pathology (61% of routed stars fail the FAP gate and pay entry tax **plus** the full search) is the textbook failure of 2-stage designs with high inconclusive rates. Lifted to the survey: a budgeted allocation problem (compute assigned across stars by marginal detection-probability per CPU-second) — unformalized in the transit literature; the strong version of the idea.

## 3. Mathematical findings (idea-level)

- **The comb statistic is the Rayleigh test** (mean resultant length of folded event phases) — the workhorse of γ-ray/X-ray pulsar timing (Zₙ², H-test; de Jager et al. 1989), whose null asymptotics are long solved. VESPER prices this null with a B=1000 block-bootstrap of *re-detections* — the single component that generated ρ_d ≈ 0.144. The failed Lever-1b EVT candidate lacked per-star conditioning (event count, clustering); the pulsar literature's machinery + one-time null-pool calibration is the principled cheap replacement.
- **N_min = 2 makes the period evidence nearly vacuous:** two events give R̄ = 1 at every P = Δt/m; the gate then tests event multiplicity, not periodicity (FAP remains *valid* — surrogates share the degeneracy — but the narrated evidence isn't the priced evidence). Elegant replacement for small k: **period recovery = exact arithmetic-progression finding** among event times (O(k²) DP; no grid, no oversampling; interleaved APs = multi-planet systems for free).
- **The realized arbiter inverts the threat model.** With T_red = 0, false-positive control rests on timing coherence (M6 ablation: FAP-gate removal takes null FP 0→12.3%) — yet the most dangerous survey false positives (momentum dumps, scattered-light cycles) are *instrumentally quasi-periodic*: excellent timing coherence, wrong shape. The sealed operating point is maximally exposed to exactly the threat class the charter's "photometry decides" was written against. Injected-null calibration cannot reveal this; real deployment would.
- **Estimand entanglement:** the ±0.5 T₁₄ epoch predicate + detector stride quantization generate both the P=0.5 d gains (edge control: TLS epoch failures at 97% SDE-pass) and 80% of the losses. The headline ΔR̄'s stability under the tolerance choice is load-bearing and was unmeasured (now Roadmap RES-3).
- **Occurrence weighting is half fiat:** w_c = log-uniform(P) × KM(R); KM's own dN/dlogP ∝ P^1.9 puts ~zero occurrence at P = 0.5 d (below KM support), the node family carrying Arm B's gains (now RES-2).
- Verified sound: injection physics (density a/R★, Winn T₁₄), GLS/Wald confirmer, max-vs-max FAP construction, paired E1 bootstrap, §8.3a cost algebra (modulo the π\* denominator inconsistency, numerically irrelevant).

## 4. Hidden opportunities (ranked)

1. **Turn the negative into a theorem** — the triage impossibility bound with the sealed run as witness (→ Phase-II Track A). Changes the paper's class from "we tried X" to "X is closed; here is the boundary."
2. **The benchmark harness is the sleeper asset** — no community-standard, leakage-safe, sealed injection-recovery benchmark for transit search exists; M0–M3 + seal tooling *is* one (→ Track B, likely the most-cited artifact).
3. **The monotransit pivot** — K=1 is the regime where folding provably cannot help; entry-tax economics vanish; photometry is *forced* to be the arbiter (repairing the inversion); the duration–density prior (P ≈ π²Gρ⋆T₁₄³/3(1−b²)^{3/2}) is unexploited; **892 accidental effective monotransits already sit in `recovery.csv`** as a free pre-study (→ Track C).
4. FFA/SES adoption rather than competition (→ G0).
5. Conditioned analytic FAP (Rayleigh/EVT) as Lever-1b's principled successor.
6. Sequential/bandit survey allocation (methods paper).
7. **Under-claimed genuine advantages:** event-time methods are cadence-agnostic and TTV-tolerant — neither claimed anywhere.
8. Analytic completeness function: the fast path's completeness is nearly closed-form (thresholded MF + explicit gates) — more *modelable* than TLS's, which occurrence-rate science values above raw recall. Unnoticed by the project.
9. Explicitly rejected despite fashion: TDA, manifold learning, compressed sensing, symbolic AI — nothing in the problem structure rewards them.

## 5. Five-year failure modes

GPU/FFA erases the compute premise (most likely) · mission-shape overfit (every calibrated number is TESS-S1–S3-2min-shaped; only the *procedure* transfers) · 40-host distributional narrowness · instrumental-comb false positives in the wild · SPOC reprocessing vs identity-pinned manifests (pin data digests) · P-2 finality as brittleness · bus factor 1.

## 6. Thought experiments (selected)

Flaring M dwarf: science survives, economics fail first (entry tax on gate-failures). Irregular cadence: spacing inference barely notices — *stronger than claimed*. Multis: single-comb mis-association; AP formulation fixes. Adversarial: two commensurable dips with non-transit shape pass FAP, face no Λ threshold, no odd/even at k=2 — one veto (secondary) from spoofable-by-timing. PLATO multi-camera: per-camera event coincidence is a natural fold-free veto — a future hook.

## 7–8. Against the future; novelty grading

Timeless: the sealed pre-registration protocol (needed *more* in an ML-dominated field), the bound, event-wise/monotransit reasoning, the benchmark. Temporary: every threshold, TLS cost ratios, the routing architecture, the B=1000 bootstrap (obsolete against 1989 theory). Novelty: routing per se **incremental** (cascades; broker triage); honest entry-tax economics **moderately novel**; the sealed-validation governance in an astronomy pipeline paper **highly novel in practice**; bound + benchmark (unwritten/unbuilt) **potentially field-touching**.

## 9. Questions not asked

Optimizing the wrong scarce resource? Strongest baseline (SES/FFA) never priced? Recall the only currency (vs analytic completeness)? Why binary routing? Unlimited funding → drop compute claim, build PLATO-era event-wise pipeline + benchmark + allocation theory. Minimal compute → FFA + AP combinatorics + analytic FAP: no bootstrap anywhere. Benchmark-paper version → stop being a detector, become the *referee*.

## 10. Brutal truths

1–3. Original claim: **not** worth years (capped, measured, avoidable). Pivoted program: **yes** (bound + benchmark + monotransit).
4. Weakest assumption: "the coherent search is the irreducible expensive unit" (SES/FFA breaks it).
5. Strongest: recall-by-construction via fallback — held under a sealed test, three interval methods.
6. Biggest hidden opportunity: impossibility theorem + benchmark; runner-up: analytic completeness.
7. Biggest hidden risk: timing-coherence-as-arbiter meets instrumentally periodic systematics.
8. World-class researcher's first month: conditioned Rayleigh null; AP search; reframe E2 as the bound.
9. Reviewer surprise: the project audited itself into withdrawing its own headline verdict — rigor is the surprise.
10. Memorable as: *"pre-registered a plausible idea, sealed the test, killed the claim properly, proved the general bound, left the field a benchmark."*

## Scores (idea-level)

Mathematical depth 6 · Scientific rigor 8.5 · Originality 5.5 · Long-term potential 6.5 (conditional on pivot) · Engineering philosophy 9 · Scalability 4 (current idea) · Theoretical soundness 7 · Publication potential 7 · Real-world usefulness 4 (as compute-saver) · Future impact 5–7 (pivot-dependent).

**Grant verdict.** As proposed (routing to cut transit-survey compute): do not fund — the project's own sealed measurement plus population structure caps the upside, and the SES/FFA lane renders the premise avoidable. The pivoted program (bound, benchmark, monotransit, same governance): fund without hesitation. The decisive factor: this team demonstrated the rarest research behavior — sealing a falsifiable claim before looking and executing the verdict against itself. Fund the people; aim them at the question mathematics hasn't already answered.

---
*Persisted 2026-07-20 from the 2026-07-19 in-session review; the Phase-II program document operationalizes §§4–10.*
