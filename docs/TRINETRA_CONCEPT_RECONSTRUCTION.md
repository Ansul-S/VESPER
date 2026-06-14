# TRINETRA — CONCEPT RECONSTRUCTION

**Author's stance:** scientific historian & systems architect
**Method:** reconstructed from the genesis design conversation (19–20 Mar 2026), the MASTER blueprint, the Q1–Q4 experimental record, and the recorded search outputs — deliberately ignoring current code, bugs, folder layout, and deployment state.
**Question:** *Not* "what does the code do?" but "**what was TRINETRA trying to be?**"

---

## SECTION A — ORIGINAL VISION

Imagine you are handed the Kepler archive: ~200,000 stars, four years of brightness measurements each. Somewhere in that ocean of noise are the faint, repeating dimmings caused by planets crossing their stars. The established way to find them — Box Least Squares (BLS) and its refined successor Transit Least Squares (TLS) — works by **hypothesis**: pick a trial period, fold the light curve at that period, ask "is there a transit here?", score it, then repeat for tens of thousands of periods. It is exhaustive, it is sensitive, and it is *crushingly* slow: TLS costs roughly an hour of compute per star, which at Kepler scale is more than two decades of single-core time. The original TRINETRA pipeline did exactly this — detect with TLS, classify the candidates with a convolutional neural network, then score the survivors for habitability — and it worked, but it could never scale.

TRINETRA (in its decisive "v3" reconception) is the attempt to break that scaling wall **without losing a single real planet.** Its founding move is to refuse the brute-force search as the *first* step. Instead of asking every star "do you have a planet at period P?" ten-thousand times, it asks one cheap question once: *"does this star show any brief, isolated dimming that the noise cannot explain?"* Where the answer is yes — and for big planets it usually is — the period is not searched but **inferred**, from the spacing between the dimming events. Only the stars that show no local evidence inherit the expensive, exhaustive fold-based search. The expensive computation is thereby spent only where it is actually needed.

So TRINETRA is best understood not as an algorithm but as a **triage philosophy for discovery at scale**: detect the obvious cheaply, infer structure from evidence, and reserve exhaustive search for the genuinely hard minority — with the non-negotiable constraint that nothing detectable is ever thrown away. The downstream stages it inherited from the original pipeline (CNN classification, habitability scoring) remain; what TRINETRA reinvents is the **front door** — how a transit is first found at all.

---

## SECTION B — FOUNDING HYPOTHESIS

> **If a meaningful fraction of transiting planets produce individual transits that rise above their star's local noise, then for those planets the orbital period can be recovered from the *spacing* of directly-detected dips rather than from a brute-force period search — collapsing detection from an O(N·P·D) hypothesis test into an O(N) + O(k²) evidence-then-inference process — with no loss of recall, because any star lacking local evidence simply falls back to full BLS/TLS.**

The conversation that birthed it compressed this to seven words: ***"Detection should start with evidence, not hypothesis."***

---

## SECTION C — FIRST-PRINCIPLES ARCHITECTURE

Described purely as a concept, independent of any implementation.

### Input
A single star's photometric time series (brightness vs. time), conditioned so that slow stellar and instrumental trends are removed and only short-timescale residuals remain. The residual must be expressed as deviation from a flat baseline, so that a transit appears as a *negative* excursion.

### Processing stages

**Stage 1 — Local anomaly detection (the trigger).**
Scan the time axis *once* for brief, downward flux decrements that are inconsistent with the star's noise model. No period is assumed. The output is a small set of candidate **event times**.
*Scientific reasoning:* a real transit has a recognizable local shape (drop → flat floor → recovery, symmetric, of transit-like duration). For large planets this shape is visible in a single event, so periodicity is unnecessary to *find* it. Scanning once is O(N); folding thousands of periods is not.

**Stage 2 — Period inference from event spacing.**
Given event times {t₁, t₂, …}, find the period P at which the events share a common phase — a combinatorial / voting problem over the *sparse event set*, not a fold over the *dense light curve*.
*Scientific reasoning:* if events are real repeating transits, their pairwise time differences are integer multiples of one period. Recovering that period from a handful of events is cheap (O(k²)); the search space has collapsed from "all periods × all data points" to "periods consistent with these few events."

**Stage 3 — Targeted confirmation.**
Take the inferred period as a *seed* and run a narrow, physically-motivated transit fit (a targeted TLS/BLS over P ± a small window) to confirm that a statistically significant, transit-shaped, *repeating* signal actually exists.
*Scientific reasoning:* finding events and guessing a period is not yet a detection. Confirmation is where a candidate earns the name "transit" — it is the arbiter that separates signal from coincidence, done cheaply because the period is already known.

**Stage 4 — Classification.**
Pass confirmed candidates to a learned classifier (CNN) that distinguishes genuine planetary transits from the standard impostors (eclipsing binaries, stellar variability, systematics).
*Scientific reasoning:* even significant periodic dips have astrophysical false-positive sources; a classifier trained on vetted examples encodes that discrimination.

**Stage 5 — Habitability scoring.**
For surviving planet candidates, estimate physical properties and score habitability (insolation / habitable-zone position, equilibrium temperature, Earth-similarity, with uncertainty propagated).
*Scientific reasoning:* the scientific payload is not "a planet exists" but "*what kind*, and could it host life?" This is the question that motivated the whole system.

**The router (the connective tissue).**
Between Stage 1 and the rest sits the decisive idea: **route by observed evidence strength, not by assumed planet type.** Strong local evidence → fast path (Stages 2–3). Weak/absent evidence → slow path (full fold-based search), but *only* there.
*Scientific reasoning:* you cannot route by planet type because the planet type is the unknown you are trying to determine; the only thing you can condition on is the evidence the data actually presents. This is an epistemic stance, and it is the heart of the architecture.

### Outputs
A ranked list of planet candidates, each with: a recovered/confirmed period, a detection significance, a classifier disposition (planet vs. false positive), and — for planets — a habitability score with uncertainties. Alongside, a *compute ledger*: which stars took the fast path vs. the slow path, i.e. the realized scaling.

---

## SECTION D — CORE INNOVATIONS

Only the genuinely novel ideas. (Honest note: single-transit / "monotransit" detection and period-from-spacing exist in the literature; TRINETRA's novelty is in their *synthesis into a recall-preserving triage architecture* and the explicit framing below.)

**1. Evidence-first decoupling of detection from period search.**
- *Why it matters:* it separates two problems that BLS/TLS fuse — "where are the dips?" and "what period do they share?" — and only the first must be paid on every star.
- *Evidence:* Q1 showed ~46% of candidate-hosting stars are fast-path-viable; the BLS comparison measured a 263× per-star speedup on the fast path.
- *Survived testing?* The **principle** survived (the speedup and routing fraction are real). The **closure** did not: the confirmation stage that turns "events found" into "planet detected" was never built, so the loop was never honestly closed.

**2. The complexity-class reframing: O(N·P·D) → O(N) + O(k²).**
- *Why it matters:* it reframes the speedup as a *change of computational kind*, not a tuning gain — the right framing for a methods paper.
- *Evidence:* mathematically valid; empirically the fast path ran in milliseconds vs. seconds for BLS.
- *Survived testing?* Yes, as an efficiency claim. (It says nothing about correctness — which is where the trouble lay.)

**3. Routing by evidence strength, not planet type (the epistemic move).**
- *Why it matters:* it is the only physically honest way to allocate compute when the quantity you'd route on (planet size) is unknown a priori.
- *Evidence:* Q1's bimodal detectability distribution (large planets locally visible, small ones not) is exactly the structure that makes evidence-routing meaningful.
- *Survived testing?* Yes, conceptually intact.

**4. Period recovery as robust voting (Hough transform over sparse events).**
- *Why it matters:* recovering a period from a few events contaminated by false positives is a noisy combinatorial problem; a Hough/voting scheme is the principled tool.
- *Evidence:* Q3 simulation reported ~83% recovery at the nominal operating point.
- *Survived testing?* **Only in simulation.** It was validated against uniformly-random false positives; real stellar/instrumental false positives are *correlated*, and on real stars the method manufactured periods from noise. The idea is sound; its validation was not representative.

**5. Model-agnostic generality.**
- *Why it matters:* a detector that flags "something anomalous happened" rather than "a box-shaped dip of the assumed model happened" could, in principle, catch ringed planets, exomoon TTVs, and other non-standard signals that BLS/TLS reject by construction.
- *Evidence:* none — this was an aspiration articulated at genesis, never operationalized.
- *Survived testing?* Untested. It remains a genuinely interesting *promissory* innovation.

---

## SECTION E — WHAT FAILED

Kept strictly separated by kind.

### Concept failures
- **One, and it is subtle:** the philosophy "start with evidence" was applied to the wrong evidence. In practice the system treated the *phase-coherence of event times* as the evidence of a planet, while the actual photometric evidence (depth, shape, repetition) was deferred to a downstream "vetting" step that could not veto. The concept inverted its own hierarchy — coincidence in timing was allowed to stand in for significance in photometry.
- The **generality claim** (rings/exomoons) was never part of what was built; as a *concept* it neither failed nor succeeded — it was simply never engaged.
- The remainder of the concept (triage, evidence-routing, fast/slow split, recall-first) did **not** fail.

### Statistical failures
- The period-recovery score was **never calibrated against a null** — no false-alarm probability, so "how coherent would random event times look?" was never asked.
- The **look-elsewhere effect** of scanning ~1000 trial periods was uncorrected; with few events, high coherence is essentially guaranteed by chance.
- The candidate "SNR" was a **circular statistic** — built from quantities that the detection threshold forces to be large — so it could not discriminate.

### Validation failures
- The pivotal Q3 robustness test modeled false positives as **uniform i.i.d.**, which does not represent real correlated noise — so a passing simulation coexisted with a failing reality.
- End-to-end completeness rested on an **underpowered** injection-recovery (n=5 per cell).
- The architecture's keystone — targeted confirmation — was **never validated** because it was never implemented; the loop from "events" to "confirmed planet" was open.
- Some claimed results (a third search iteration) are **unverified** — their outputs are not in the record.

### Engineering failures
*(Listed for completeness; by mandate, not the focus.)* A silently-wrong interpolation in the even/odd check; detrending applied across stitched quarter boundaries (manufacturing ~30-day artifacts); no single-event/artifact guards; a period-grid edge pile-up. These are fixable defects of execution, not of idea.

---

## SECTION F — TRINETRA v4 BLUEPRINT (rebuild from zero)

### What remains unchanged
- The **problem statement**: scale exoplanet detection across ~10⁵–10⁶ stars without sacrificing recall.
- The **evidence-first philosophy** — *as a trigger*: scan once, cheaply, for local transit-like events.
- **Routing by evidence strength, not planet type** — the epistemic core.
- The **fast/slow split** and the principle that brute-force search is paid only on the hard minority.
- **Recall over precision** as the governing value.
- The **Q1 detectability-bimodality result** (large planets locally visible; small ones not) — the empirical foundation that justifies triage.
- The **end-to-end vision**: detect → confirm → classify → score for habitability.

### What is redesigned
- **The arbiter of "is this a planet?" moves to photometry.** Make a depth-significant, transit-shaped, *repeating* phase-folded signal the **gate** — not the phase-coherence of event times.
- **Period significance is calibrated.** Bootstrap the recovery score against scrambled event times for a real false-alarm probability; correct for the multi-period search.
- **The confirmation stage is actually built** and becomes the decision-maker; event-spacing only *seeds* it.
- **Validation is made representative:** test period recovery against *correlated* noise (real planet-free light curves), and power the injection-recovery sufficiently.
- **The CNN is trained across all routing paths** (a domain-shift problem flagged at genesis but never resolved), or the path is given to it as a feature.
- Conditioning respects data structure (per-segment detrending; artifact/jackknife guards).

### What is removed completely
- The **circular SNR** statistic.
- **Grading on timing coherence** as a stand-in for detection.
- The **uncalibrated coherence-score-as-verdict**.
- The broken **even/odd interpolation** check (replaced by a correct, sign-aware, binned depth comparison).

---

## SECTION G — ONE-PARAGRAPH SUMMARY

**What is TRINETRA, really?** It is an attempt to make planet-finding *scale* by inverting the question at the heart of transit detection — from "test every possible period on every star" to "find the evidence first, then explain it." Rather than fold every light curve thousands of times, TRINETRA looks once for the individual dimmings that big planets make plainly, infers the orbit from how those dimmings are spaced, and spends the expensive exhaustive search only on the stars that hide their planets too well to be seen in a single pass — all under an absolute rule that no detectable planet may be lost. Its lasting contributions are conceptual: the epistemic discipline of *routing by observed evidence rather than by the unknown you're hunting*, and the recognition that this is a change in the *kind* of computation, not merely its speed. Its unfinished business is equally clear: TRINETRA must learn to let **photometric significance — depth, shape, repetition — and not the mere coincidence of timing — be the judge of what counts as evidence**. Get that one ordering right, and the idea stands.

---

*End of reconstruction. No source files were modified.*
