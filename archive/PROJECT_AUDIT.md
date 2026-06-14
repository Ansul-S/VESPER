# TRINETRA — FORENSIC PROJECT AUDIT

**Audit date:** 2026-06-13
**Auditor:** Automated forensic analysis (read-only; no code written or modified)
**Scope:** `/Users/ansulsuryawanshi/Desktop/Revival/` — 548 MB across 5 top-level units
**Purpose:** Reconstruct project state, untangle versions/duplicates, and define a resurrection path.

---

## 0. EXECUTIVE SUMMARY

TRINETRA is an exoplanet detection-and-habitability project that exists in this folder as **two parallel technical tracks that share a name but not an architecture**:

- **Track A — "The Deployed Product"** (4-phase deep-learning pipeline): Kepler data → BLS/TLS transit analysis → AstroNet CNN (AUC 0.979) → habitability scoring → FastAPI + Next.js dashboard. This track reached **deployment** (Hugging Face Spaces API + Vercel dashboard, Supabase DB) by **Mar 18, 2026**.
- **Track B — "The Research Pivot" (TRINETRA v3)**: an *evidence-first* detection redesign (matched-filter dip detection + Hough period recovery instead of brute-force TLS-on-every-star). Born from a research conversation on **Mar 19, 2026**. It produced complete validation experiments (Q1–Q4), a 263× speedup benchmark, an unknown-star search, and an 8-page draft paper — but **stalled** on a false-positive/vetting problem and was never integrated with Track A.

**The single most important finding:** *"V3" is not a newer release of the deployed product.* It is a separate research line that reimagines only the **detection front-end**. The product shipped; the research stalled. Any "revival" must first decide **which track is being revived** — they are not continuous.

**Most complete directory:** `TRINETRA 2/` (501 MB — the only place the trained models, light curves, and all results coexist).
**Canonical versioned code:** `trinetra-exoplanet-ai/` (the Git repo; but its data/models are git-ignored).

---

## 1. PROJECT INVENTORY

### 1.1 Top-level units

| Unit | Size | Last touched* | Git? | Role |
|------|------|--------------|------|------|
| `trinetra-exoplanet-ai/` | 13 MB | Mar 18 (last commit) | ✅ `github.com/Ansul-S/trinetra-exoplanet-ai` | **Deployment monorepo** — code source of truth (notebooks + FastAPI + Next.js dashboard). Data/models git-ignored. |
| `TRINETRA 2/` | 501 MB | Jun 13 (assembled) | ❌ | **Consolidated data superset** — all 5 phase notebooks + every artifact (.pt models, .npz light curves, CSV/JSON/PNG results) + full v3 research code + 442 MB MAST cache. |
| `TRINETRA/` | 33 MB | Apr 21 | ❌ | **Documentation + archive** — the MASTER blueprint, reference papers, 8-page draft paper, v3 code (3 redundant copies). |
| `trinetra_hf/` | 84 KB | Mar 20 | ❌ | **Hugging Face Spaces deployment** copy of the FastAPI app (Docker SDK). |
| `Chats/` | 652 KB | Jun 13 | ❌ | The **13,653-line research conversation** that designed Track B (v3). |

\* For Git-tracked files, mtimes reflect when the folder was copied into `Revival/` (Jun 13); the reliable Track A timeline comes from Git commit dates.

### 1.2 Key assets by type

**Trained models** (only in `TRINETRA 2/phase3_model/`, ~6.9 MB each):
- `astronet_trinetra.pt`, `astronet_trinetra_finetuned.pt`, `astronet_v2.pt`, `astronet_v2_finetuned.pt`

**Authoritative dataset:** `trinetra_v4_corrected.json` — **15 scored planets** (the deployed product's data). Present identically in `TRINETRA 2/phase4_habitability/` and `trinetra-exoplanet-ai/data/results/`.

**Light curves:** 15 `.npz` files (12 MB) in `TRINETRA 2/phase1_processed_data/light_curves/`.

**MAST/Kepler FITS cache:** 442 MB in `TRINETRA 2/TRINETRA V3/TRINETRA_v3/lk_cache/` (Track B download cache).

**Notebooks (9 total, across 3 locations):** Phase1 Data Pipeline, Phase2 Transit Analysis/TCE, Phase3 CNN, Phase4 Habitability, Step4_Complete, plus Track B's `Q1_Q2_Q3_Q4.ipynb` and `The_Search.ipynb`.

**Documents:**
- `TRINETRA/MASTER/TRINETRA_v3_PROJECT_REPORT.md` — **the authoritative blueprint** (1,268 lines; full architecture, experiments, bugs, roadmap).
- `TRINETRA/TRINETRA_v3_Paper.pdf` — 8-page draft paper (created Mar 22, MS Word).
- `TRINETRA/Books/TRINETRA_Master_Document.docx` — early narrative doc (29 KB).
- Reference papers: `Shallue & Vanderburg (2018).pdf` (AstroNet), `exominer.pdf`.

**Deployment code:** FastAPI app (`app/`: main 416 LOC, habitability 242, models 132, database 128 — Supabase-backed) + Next.js 14 dashboard (TypeScript, Tailwind, Framer Motion, D3, Recharts, React Query).

---

## 2. VERSION COMPARISON — "TRINETRA" vs "TRINETRA 2" vs "V3"

⚠️ **These names mix two meanings:** (a) folder names on disk, and (b) the conceptual v1→v2→v3 evolution described in the MASTER report. They do **not** line up one-to-one. Disambiguated below.

### 2.1 The conceptual evolution (from the MASTER report)

| Concept | Architecture | Status |
|---------|-------------|--------|
| **v1** | Raw LC → preprocess → **TLS on every star** | Conceptual only — infeasible (~1 hr/star × 200k = 22 yr) |
| **v2** | Raw LC → preprocess → **BLS prefilter** → TLS → CNN → scoring | The basis of the **deployed product** (Track A) |
| **v3** | Raw LC → preprocess → **matched-filter dip detector → Hough period recovery → targeted TLS** → CNN → scoring | **Track B research** — front-end redesign, "evidence-first" |

### 2.2 The folders on disk

| Folder | What it actually is | Track | Completeness |
|--------|--------------------|-------|--------------|
| **`TRINETRA/`** | Documentation + archive snapshot. Holds the blueprint, papers, and 3 redundant copies of v3 code. | Mostly B + docs | Docs ✅ / code redundant & partly stale |
| **`TRINETRA 2/`** | The consolidated working master. Holds **both** tracks: phases 1–4 (Track A) results/models **and** the `TRINETRA V3/` subtree (Track B). | A **and** B | **Most complete on disk** |
| **`TRINETRA V3` / `TRINETRA_v3`** (subfolder of both above) | The evidence-first research code + results + cache. | B | Code ✅ / not integrated, not deployed |

### 2.3 Track A vs Track B (the comparison that matters)

| Dimension | **Track A — Deployed Product** | **Track B — TRINETRA v3 Research** |
|-----------|-------------------------------|-----------------------------------|
| **Core idea** | Phase-folding detection (BLS/TLS) + CNN classification + habitability | Replace TLS-everywhere with O(N) local dip detection → infer period from dip spacing |
| **Detection** | BLS/TLS on each star (Phase 2) | Matched filter (MAD threshold) + Hough transform |
| **Classifier** | AstroNet CNN, AUC=0.979, 5/5 recall (Phase 3) | None integrated (planned, not done) |
| **Habitability** | ESI + HZ + Monte Carlo → 15 planets (Phase 4) | None integrated (planned, not done) |
| **Validation** | Training metrics; 15 stars, 7 TCEs | Q1–Q4 + injection-recovery + BLS bench (263× speedup) + 3 search iterations |
| **Output artifact** | Live API + dashboard + 15-planet dataset | 8-page draft paper + result CSVs |
| **Deployment** | ✅ HF Spaces + Vercel + Supabase | ❌ Colab scripts only |
| **Blocking issue** | Dormant; needs DB re-provision to run | False positives — **0/68** candidates pass vetting (even/odd interpolation bug) |
| **Last activity** | Mar 18 (Git) | Mar 22 (paper); search iter 3 reported, CSVs absent |

**Verdict:** Track A is *finished and was live*. Track B is *the more ambitious science but unfinished*. They share preprocessing philosophy and the Kepler data domain, but the v3 detector was never wired into the CNN/habitability/deployment stack.

---

## 3. FOLDER RELATIONSHIP MAP

```
Revival/  (548 MB)
│
├── Chats/  ──────────────────────────────────┐  GENESIS of Track B
│   └── "Scaling exoplanet detection…" .md     │  (Mar 19 → updated today)
│       (13,653 lines, design conversation)    │
│                                              ▼
├── TRINETRA/  (docs + archive, Apr 21) ─── distills ──► MASTER/TRINETRA_v3_PROJECT_REPORT.md
│   ├── MASTER/      → the blueprint (authoritative spec)        │
│   ├── Books/       → reference papers + early .docx            │  describes
│   ├── The Search/  → v3 search results (iter1, iter2)          │  Track B
│   ├── Trinetra v3/ → v3 code in 3 copies:                      │
│   │     ├── New Model/      (faithful copy)  ───┐              │
│   │     ├── Q1 files/       (partial subset) ───┤ identical    │
│   │     └── untitled folder/(DIVERGENT/older)───┘ hashes*      │
│   └── TRINETRA_v3_Paper.pdf → 8-pg draft (Mar 22)              │
│                                                                │
├── TRINETRA 2/  (master superset, 501 MB) ◄── superset of ─────┘
│   ├── Notebooks/            → Track A phases 1–4 + Step4_Complete (5 nbks)
│   ├── phase1_processed_data → 15 .npz light curves
│   ├── phase2_results        → TCE table, phase-fold summaries
│   ├── phase3_model          → 4× AstroNet .pt weights  ◄── ONLY copy of models
│   ├── phase4_habitability   → v4 dataset (15 planets) + MC results
│   ├── phase4_validation     → ground_truth.csv
│   └── TRINETRA V3/TRINETRA_v3/  → Track B code (superset) + lk_cache (442 MB)
│         └── (== TRINETRA/Trinetra v3/New Model + bls_comparison + notebooks)
│
├── trinetra-exoplanet-ai/  (Git repo, code-of-record) ◄── deploys ── Track A
│   ├── notebooks/   → phases 1–4 (re-saved variants; no Step4)
│   ├── data/results → v4_corrected.json  (== TRINETRA 2 copy)
│   ├── trinetra_api/→ FastAPI app  ──────────┐ identical app/ code
│   └── dashboard/   → Next.js 14 UI          │
│                                             │
└── trinetra_hf/  (HF Spaces deploy) ◄── mirror of ──┘ trinetra_api/app
    └── app/ (== trinetra_api/app, byte-identical)
```

\* See §4 for the exact divergence in `untitled folder/`.

**Dependency / data-flow relationships:**
- `Chats/` → conceived → MASTER report → specifies → Track B code.
- Track A code lives in **two** places that must be paired: `trinetra-exoplanet-ai/` (code, version-controlled) **needs** `TRINETRA 2/` (models + data, since the repo git-ignores `*.pt`, `*.npz`, `*.csv`).
- API (`trinetra_api` / `trinetra_hf`) reads from **Supabase** at runtime (`database.py` requires `SUPABASE_URL`/`SUPABASE_KEY`), seeded from `trinetra_v4_corrected.json`.
- Dashboard proxies the HF API URL (`ansul-s-trinetra-api.hf.space`).

---

## 4. DUPLICATE WORK DETECTION

Verified by MD5 checksums across all `.py` and `.ipynb` files.

### 4.1 API application code — **100% duplicated**
`trinetra_hf/app/*` and `trinetra-exoplanet-ai/trinetra_api/app/*` are **byte-identical** for all 5 files (`__init__`, `database`, `habitability`, `main`, `models`). Differences are only:
- Top-level `main.py` entry point (HF vs Railway/local launch wrapper).
- `requirements.txt`: pydantic `2.7.1` (HF) vs `2.6.4` (repo).
→ **These are the same app deployed two ways.** One should be the source; the other generated.

### 4.2 Track B (v3) pipeline scripts — duplicated 2–4×
| File | Locations | Status |
|------|-----------|--------|
| `transit_physics.py` | New Model, Q1 files, untitled folder, TRINETRA 2/V3 | **All identical** |
| `kepler_catalog.py` | New Model, Q1 files, untitled folder, TRINETRA 2/V3 | **All identical** |
| `q2/q3/q4/injection_recovery/q1_threshold` | New Model + TRINETRA 2/V3 | **Identical pairs** |
| `q1_snr_analysis.py` | New Model = Q1 files = TRINETRA 2/V3 ✅ … **but** `untitled folder/` differs ⚠️ | **Divergent copy** |
| `run_q1_colab.py` | New Model = Q1 files = TRINETRA 2/V3 ✅ … **but** `untitled folder/` differs ⚠️ | **Divergent copy** |
| `trinetra_app_database_fixed.py` | **only** `untitled folder/` | Unique (orphan) |
| `bls_comparison.py`, `Q1_Q2_Q3_Q4.ipynb`, `Unknown star search/` | **only** `TRINETRA 2/V3` | Unique to superset |

→ **`TRINETRA 2/TRINETRA V3/TRINETRA_v3/` is the superset** and supersedes `TRINETRA/Trinetra v3/New Model/` (faithful subset), `Q1 files/` (partial), and `untitled folder/` (stale + 1 orphan file).

### 4.3 `unknown_star_search.py` — **two divergent versions**
`TRINETRA/The Search/` vs `TRINETRA 2/…/Unknown star search/` have **different hashes**. Must diff before trusting either.

### 4.4 Phase notebooks — 3 locations, **none byte-identical**
Phase 1/2/3/4 notebooks exist in `TRINETRA/Notebooks/`, `TRINETRA 2/Notebooks/`, and `trinetra-exoplanet-ai/notebooks/` — all re-saved/re-executed variants (different outputs/metadata).
- `TRINETRA 2/Notebooks/` is the **most complete** (5 notebooks, including `TRINETRA_Step4_Complete.ipynb`, which the Git repo lacks).
- The Git repo has only 4 (no Step4).

### 4.5 Dataset duplication — benign
`trinetra_v4_corrected.json` is identical in `TRINETRA 2/phase4_habitability/` and `trinetra-exoplanet-ai/data/results/` (intentional — repo carries the small authoritative result).

---

## 5. CURRENT PROJECT STATUS

### 5.1 Timeline (reconstructed)
| Date | Event |
|------|-------|
| Mar 9–11 | Reference papers added; Git repo "Initial TRINETRA project structure" |
| Mar 13–14 | Phase 1 (data pipeline) + Phase 2 (TCE, 15 stars, 7 TCEs) committed |
| Mar 15 | Phase 3 CNN — AstroNet AUC 0.969 → V2 final **AUC 0.979, recall 5/5** |
| Mar 16 | Phase 4 Habitability Engine + FastAPI API; Railway build fixes |
| Mar 17 | Phase 4 **V4 corrected — 15 planets** (authoritative dataset) |
| Mar 18 | Dashboard replaced with scientific UI ("Step 3 complete") — **last Git commit** |
| Mar 19 | **Track B born** — "Scaling exoplanet detection" research conversation |
| Mar 20 | `trinetra_hf` HF deployment copy; `Q1_Q2_Q3_Q4.ipynb` |
| Mar 22 | `The_Search.ipynb` + **8-page draft paper** |
| Apr 21 | `TRINETRA/` archive last modified (MASTER report consolidated) |
| **Jun 13 (today)** | `Revival/` assembled; research chat re-exported → **intent to resurrect** |

### 5.2 Track A (Deployed Product) — **COMPLETE, now DORMANT**
- ✅ Phases 1–4 complete and validated (AUC 0.979; 15 scored planets; top candidate Kepler-22b, score 0.8826).
- ✅ FastAPI backend + Next.js dashboard built and previously deployed.
- ⚠️ **Dormant ~3 months.** Cannot run as-is: no Supabase credentials present, no `node_modules`, no `.next` build. Live URLs likely offline (free-tier HF/Vercel/Supabase).

### 5.3 Track B (v3 Research) — **STALLED, unfinished**
- ✅ Q1–Q4 experiments, injection-recovery, BLS comparison (263× speedup) complete.
- ✅ Unknown-star search ran 3 iterations (~483 stars).
- 🛑 **Blocking issue:** every candidate is a false positive. **0/68 pass vetting** (even/odd interpolation bug). Quarter-boundary artifacts (P≈30 d) and single-event artifacts dominate.
- ❌ Targeted-TLS confirmation, CNN integration, habitability integration: **never built**.

### 5.4 Security/hygiene observations
- ✅ No real `.env` or secrets committed (only `.env.example`). `.gitignore` correctly excludes `*.env`, `*.pt`, `*.npz`, `*.csv`, `*.fits`.
- ⚠️ Consequence: the repo **alone cannot reproduce or run** the product — models and data live only in the un-versioned `TRINETRA 2/`. Loss of `TRINETRA 2/` = loss of all trained weights.
- ⚠️ `.DS_Store` files scattered throughout (cosmetic).

---

## 6. MISSING COMPONENTS

### 6.1 To run Track A (product)
- ❌ Supabase instance + credentials (`SUPABASE_URL`, `SUPABASE_KEY`) — API hard-requires them (raises `ValueError` otherwise). DB must be re-provisioned and **seeded from `trinetra_v4_corrected.json`**.
- ❌ Dashboard `node_modules` + production build (`npm install` / `next build` never run here).
- ❓ Live deployment status (HF Space, Vercel project) — unverified, presumed offline.
- ⚠️ A documented seed script to load the 15-planet JSON into the `planet_candidates` table is not evident.

### 6.2 To finish Track B (research)
- ❌ Vetting fix — replace broken even/odd interpolation with direct phase-fold depth check (Priority 1 in the blueprint).
- ❌ Quarter-boundary masking (kills P≈30/15/90 d instrumental false positives).
- ❌ Single-event artifact rejection (>10σ spike guard).
- ❌ Targeted-TLS confirmation step (fast-path Step 3 — never implemented).
- ❌ CNN + habitability integration into the v3 path.
- ❌ SIMBAD/Gaia/VSX cross-match for candidate rejection.

### 6.3 Provenance/reproducibility gaps
- ❌ **Phase 3 training set** (the ~5,087-star dataset) is not on disk — only the 4 `.pt` weights survived (Colab-only data).
- ❌ **Search iteration 3 CSVs** — the blueprint reports iter 3 (17 candidates) complete, but only `iter1`/`iter2` CSVs exist on disk.
- ❌ Several Track B result CSVs named in the blueprint's §6.1 (e.g. `trinetra_q3_input.csv`, `iter3` files) are absent.
- ❓ `TRINETRA_Master_Document.docx` content not auditable here (binary).

---

## 7. RECOMMENDED CANONICAL VERSION

**There is no single canonical folder — the canonical project is a *pairing*:**

> **Canonical code = `trinetra-exoplanet-ai/` (Git repo).**
> **Canonical data/models = `TRINETRA 2/` (the only copy of weights + light curves + full results).**
> **Canonical spec = `TRINETRA/MASTER/TRINETRA_v3_PROJECT_REPORT.md`.**
> **Canonical Track-B code = `TRINETRA 2/TRINETRA V3/TRINETRA_v3/` (superset).**

**Rationale**
- The Git repo is the only version-controlled, deployable code of record, but it deliberately excludes the heavy assets.
- `TRINETRA 2/` is the only place those assets survive — it is effectively the project's working master, but unversioned and at risk.
- The MASTER report is the most coherent, self-consistent description of intent and validated parameters.

**Therefore the recommended target state is to merge these into one versioned home** (see §8), treating:
- `TRINETRA/Trinetra v3/{New Model, Q1 files, untitled folder}` → **archive/delete** (subsumed by the TRINETRA 2 superset; verify the one divergent `q1_snr_analysis.py`/`run_q1_colab.py` first).
- `trinetra_hf/` → **regenerate from** the repo's `trinetra_api/` (don't maintain two hand-copies).
- Duplicate notebook copies → keep `TRINETRA 2/Notebooks/` (most complete), reconcile into repo.

---

## 8. PROJECT RESURRECTION ROADMAP

**Step 0 — Decide the mission (blocking).** Resurrecting the **product** (Track A: get the live demo back online) and resurrecting the **research** (Track B: produce a credible candidate / finish the paper) are different projects. Pick one as primary; they can later reconnect.

### Phase R0 — Consolidate & preserve (1 day, do first regardless of mission)
1. **Back up `TRINETRA 2/` now** (it holds the only model weights — 4× `.pt` — and light curves; it is unversioned).
2. Establish one canonical repo from `trinetra-exoplanet-ai/`; bring large assets under **Git LFS** or an external bucket (don't fight the existing `.gitignore`).
3. Run a diff on the two `unknown_star_search.py` and the divergent `untitled folder/` scripts; keep the correct one, delete the rest.
4. Strip `.DS_Store`; fold `trinetra_hf` back to "generated from `trinetra_api`."

### Track A path — "Relight the product" (≈2–4 days)
1. **Stand up Supabase**, create the `planet_candidates` (+ `stars`, `tce`) tables, and **seed from `trinetra_v4_corrected.json`** (15 planets). Set `SUPABASE_URL`/`SUPABASE_KEY`.
   - *Resilience win:* add a local-JSON fallback in `database.py` so the API runs without Supabase.
2. **Redeploy the API** (HF Spaces Docker or Railway) using `trinetra_api/`; verify `/health`, `/planets`, `/score`.
3. **Build & deploy the dashboard:** `npm install && npm run build`; point `TRINETRA_API_URL` at the live API; redeploy to Vercel.
4. Smoke-test end-to-end (home stats, planet detail + MC histogram, HZ map, live `/score`).

### Track B path — "Finish the science" (≈2–4 weeks, follows the blueprint's roadmap)
1. **Fix vetting** (Priority 1): direct phase-fold depth check (depth > 3σ in the in-transit bins).
2. **Add quarter-boundary masking** + **single-event artifact rejection** (>10σ guard).
3. Re-run **search iteration 4** with fixes; target <3% candidate rate; **persist iter-3/4 CSVs** (currently missing).
4. Implement **targeted-TLS confirmation** (narrow grid P_hough ± 1%, require SDE ≥ 9).
5. **Cross-match** survivors against SIMBAD/VSX/Gaia.
6. Raise injection-recovery to **n=20/cell**; refresh the 8-page draft → arXiv (astro-ph.EP).

### Phase R-merge — Reunite the tracks (stretch goal)
- Wire the **v3 evidence-first detector** in as the fast front-end *ahead of* Track A's CNN + habitability stages, realizing the full blueprint pipeline (detect → confirm → classify → score → serve).

### Immediate next actions (this week)
- [ ] Confirm **mission** (product vs research) — §8 Step 0.
- [ ] **Back up the 4 `.pt` models** out of `TRINETRA 2/`.
- [ ] Verify whether the HF Space / Vercel / Supabase deployments still exist.
- [ ] De-duplicate v3 code to the single superset; archive `TRINETRA/Trinetra v3/*` copies.

---

## APPENDIX — Evidence base
- **Git:** 28 commits, Mar 11–18 2026, `main` only, remote `github.com/Ansul-S/trinetra-exoplanet-ai`, last commit `56ee8b0`.
- **Checksums:** MD5 over all `.py`/`.ipynb` confirmed the duplicate/divergence map in §4.
- **Datasets:** `trinetra_v4_corrected.json` = 15 planets; `mc_results_summary.json` = 15 Monte-Carlo entries; `phase_fold_summary.json` = TCE table.
- **Models:** 4× `astronet_*.pt` (~6.9 MB each), exclusively in `TRINETRA 2/phase3_model/`.
- **Cache:** 442 MB Kepler FITS in `TRINETRA 2/.../lk_cache/`.
- **Docs:** MASTER report (1,268 lines), 8-page paper (PDF, Mar 22), 13,653-line design chat.

*End of audit. No source files were modified; this report is the only file written.*
