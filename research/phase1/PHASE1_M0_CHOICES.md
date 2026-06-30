# Phase I — M0 Frozen-Choices Proposal

| Field | Value |
|-------|-------|
| **Document** | M0 frozen-parameter proposal (decision-support) |
| **Status** | **SIGNED OFF** (owner, in-session 2026-06-15) — values frozen into `m0_config.yaml`; M0.6 will hash them (Seal #1) |
| **Created** | 2026-06-15 |
| **Governs** | The values frozen by milestone **M0** of [`PHASE1_EXECUTION_PLAN.md`](./PHASE1_EXECUTION_PLAN.md) |
| **Authority** | Subordinate to the sealed pre-registration (`phase1-prereg-v2`). Proposes *manifest* choices left open by the seal; changes **nothing** in the sealed documents. |

> **Why this exists.** M0 freezes a handful of parameters the sealed protocol deliberately left to the manifest: *which* TESS sectors, *which* stars (inclusion/exclusion cuts), and *how* they split into calibration vs. test. These are outcome-independent (set from catalog metadata, never from a detection result) but they are **pre-registration choices** — once hashed into the manifest (Seal #1) they bind the rest of Phase I. This document proposes them for your sign-off **before** any archive is queried or hashed. Final numeric feasibility (target counts, per-cell `n_transits`) is confirmed by **M0.5** *after* the sectors/cuts are chosen; if a cell fails, sectors/cuts are revised **before** the freeze (plan risk R0-5), never after.

---

## Decision 1 — TESS sector selection (M0.1)

**Constraint from the seal.** Source = **TESS SPOC 2-minute PDCSAP_FLUX** (FFI/QLP excluded; VAL §3). The injection grid spans periods `P ∈ {0.5,1,2,4,8,16}` d; the headline estimand counts only cells with `n_transits ≥ 2`. A single TESS sector (~27.4 d) yields `n_tr ≥ 2` only up to `P ≈ 13 d`, so the **`P = 16 d` cells require multi-sector baseline**. Sector choice is therefore driven by *baseline coverage for the long-period cells* and *enough sky area to block the leakage-safe split*.

| Option | Baseline for `n_tr ≥ 2` | Target volume / sky area | Split blocking | Verdict |
|--------|------------------------|--------------------------|----------------|---------|
| **A. Single sector** | Fails `P = 16 d` (and marginal at `P = 8 d`) | High, but narrow | Hard (one footprint) | ✗ Cannot support the frozen grid |
| **B. Contiguous multi-sector block (3–4 adjacent sectors), incl. CVZ overlap** | Good — overlap regions reach `n_tr ≥ 2` across the grid incl. `P = 16 d` | Broad sky area, ample targets | Clean (multiple cameras/CCDs/regions) | ✓ **Recommended** |
| **C. Continuous Viewing Zone only** | Excellent (up to ~351 d) | Small sky area, fewer targets, concentrated systematics | Harder (one region) | ◐ Good baseline, weak for split + volume |

**Recommendation: Option B** — a contiguous block of **primary-mission (Sectors 1–26)** 2-min sectors that includes a continuous-viewing-zone overlap to carry the longest-period cells, while spanning enough cameras/CCDs to block the split cleanly.

- **Candidate to confirm:** a 3-sector adjacent block in one hemisphere (e.g. a southern triplet such as **S1–S3**, or a northern triplet such as **S14–S16**), pooled with their CVZ overlap targets for the `P = 8,16 d` cells.
- **Decision rule (recorded in the manifest):** the exact sector list is fixed here, then **M0.5 verifies** every eligible `(P, R_p)` cell can reach ≥ 500 injections at `n_tr ≥ 2`. If any headline cell falls short, the block is widened (more/longer-overlap sectors) **before** Seal #1 — the injection grid and margins are frozen and are **not** changed.

> **Your call:** confirm the hemisphere + exact sector list (or accept the candidate block as the M0.5 starting point).

---

## Decision 2 — Target inclusion / exclusion criteria (M0.2)

All criteria are **outcome-independent** (catalog metadata only; never reference a detection/recovery outcome — plan G3) and are recorded with their thresholds **before** application.

| # | Criterion | Proposed rule | Why |
|---|-----------|---------------|-----|
| C1 | 2-min product exists | SPOC PDCSAP_FLUX available in ≥ 1 chosen sector | VAL §3 source definition |
| C2 | Stellar params present | TIC has `R⋆`, `Teff`, `logg` (→ limb-darkening) | Needed to inject Mandel–Agol transits (VAL §3 / A.1) |
| C3 | Photometric regime | `Tmag` within a documented bound *(propose ~7–15)* | Avoid saturated/too-faint stars; keep CDPP meaningful |
| C4 | Crowding/contamination | `CROWDSAP`/contamination within a documented bound *(propose ≥ 0.8)* | PDCSAP dilution control; supports A2/A4 |
| C5 | Minimum usable baseline | enough good-quality cadences to support the grid | Feeds `n_transits` axis + M0.5 |
| C6 | Multi-planet / TTV flag | known multi-planet & flagged-TTV systems **tagged**, not dropped | Reported separately; excluded from single-planet headline (HYP A9/A10) |

> **Your call:** accept the proposed `Tmag` and crowding thresholds, or set your own values. They are frozen once recorded.

---

## Decision 3 — Leakage-safe calibration/test split (M0.4)

**Constraint from the seal.** Disjoint by **sky region / TIC**; **no training split** (untrained detector); TEST sealed until M4 (VAL §3, §7).

- **Blocking scheme (recommended):** partition the sky into **whole spatial blocks** — by `(camera, CCD)` footprint and/or **HEALPix** cells — and assign each *entire block* to calibration **or** test. This guarantees (a) TIC-disjointness and (b) no shared instrumental systematic (same CCD column / pointing) bridges the two sets. Recommend HEALPix blocking at a fixed `nside` (records cleanly; tunable to balance counts).
- **Split ratio (propose):** **30 % calibration / 70 % test** — calibration large enough for stable threshold/FAR estimation (M3), test large enough to reach ≥ 500 injections/cell (§6). Fixed before any analysis; verified sufficient at M0.5.
- **Seed:** one fixed RNG seed, recorded.
- **Consistency:** the four sub-samples (injection hosts · null/FAR stars · reality-check labels · survey-representative mix) are assigned under the *single* split so the TEST seal is global.
- **Audit:** zero shared TIC across sets; spatial/camera-CCD separation verified and reported.

> **Your call:** confirm blocking scheme (HEALPix `nside` vs. camera/CCD) and the 30/70 ratio.

---

## Decision 4 — Catalog & tooling provenance to pin (M0.6)

Frozen into the manifest provenance at Seal #1 (plan G5): catalog **names + versions + query timestamps** (TIC, TOI/ExoFOP, EB/variable catalogs), the resolved **tool/library versions** (`pip freeze`), all **RNG seeds**, and the **Kunimoto & Matthews (2020)** occurrence-framework citation (now in `references.bib`). No numeric choice here — provenance only.

---

## What this does NOT touch

- **No thresholds.** `z⋆, θ, z_mono, T, α, α_FAP, ε, τ_GP` stay deferred to **M3** (Seal #2). M0 sets *who/what*, never *how significant* (plan G2).
- **No TEST inspection.** M0.5 feasibility uses baselines/coordinates per split; it computes no detection statistic on TEST (plan G1).
- **No light-curve flux.** M0 is metadata-only; bulk retrieval + conditioning is **M1**.
- **No sealed-document edits.** This proposal is subordinate to `phase1-prereg-v2`.

---

## Sign-off

| Decision | Owner choice (2026-06-15) |
|----------|---------------------------|
| 1 — Sector list | **S1–S3, southern hemisphere** (primary-mission triplet incl. southern CVZ overlap for the P=8/16 d cells) |
| 2 — `Tmag` bound · crowding bound | **Accepted as recommended** — require TIC stellar params; `Tmag ∈ [7, 15]`; `CROWDSAP ≥ 0.8` |
| 3 — Blocking scheme · split ratio · seed | **Accepted as recommended** — HEALPix whole-block; **30 % cal / 70 % test**; fixed seed; no training split |
| 4 — Catalog sources to pin | TIC (stellar params), ExoFOP-TESS TOI table (planet labels), TESS EB/variable catalog (FP labels) — versions + timestamps pinned at execution |

**M0.5 widen rule (owner-directed):** run M0 with S1–S3, validate per-cell coverage at M0.5, and **widen the sector block only if coverage metrics demand it** (a headline `(P,R_p)` cell cannot reach ≥ 500 injections at `n_tr ≥ 2`). Grid and margins remain frozen.

Approved to freeze these into the M0 manifest: **Ansul — approved in-session**  Date: **2026-06-15**

*Values are written into `research/m0_manifest/config/m0_config.yaml`; M0.1–M0.6 run (metadata-only); the manifest is hashed (Seal #1).*
