# M1 conditioning tooling

Tooling for milestone **M1** of [`PHASE1_M1_PLAN.md`](../../PHASE1_M1_PLAN.md): download SPOC
2-min light curves for the **calibration** pool and apply **Stage-0 conditioning** — per-sector
`wotan` biweight detrend + masking → zero-centred residual `r(t)` — plus a per-target
**celerite2 GP noise model** (σ, CDPP(T₁₄), τ_GP).

## Guarantees (inherited from the plan)

- **Calibration-only.** Reads CALIBRATION rows of the M0 manifest. **The TEST split is never
  touched at M1** (sealed until M4 — plan G1); the pipeline asserts no TEST TIC enters M1.
- **No thresholds.** M1 sets no detection threshold (those are M3 / Seal #2).
- **Window is η-provisional.** `window_length_days` is a starting value, **finalized by the M2
  transit-preservation check** (median η = δ_post/δ_true ≥ 0.90; VAL §4.2) before any M3 threshold.
- **Reproducible.** Config + resolved library versions + seeds recorded in the M1 provenance.

## Layout

```
research/m1_conditioning/
├── README.md
├── requirements.txt            # lightkurve, wotan, celerite2 (+ M0 stack)
├── config/
│   └── m1_config.yaml          # SIGNED-OFF conditioning config
└── m1_pipeline.py              # M1.1–M1.5 (added after the deps install + LC probe)
```

## Run order (after deps install)

1. `pip install -r requirements.txt`
2. `python m1_pipeline.py --config config/m1_config.yaml`
   - M1.1 freeze config → M1.2 retrieve η-sample LCs → M1.3 detrend+mask → r(t) →
     M1.4 celerite2 noise model (σ, CDPP, τ_GP) → M1.5 stationarity/whiteness diagnostics.
3. Validate η-sample, then scale `data_scope.eta_sample_size` toward the full calibration pool.

Outputs: LC cache + conditioned residuals are gitignored (`data/raw/`, `data/processed/`);
the per-target noise/QA **summary + provenance** go to `data/manifests/m1/` (small; tracked).
