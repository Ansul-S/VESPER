# M2 injection + transit-preservation tooling

Tooling for milestone **M2** of [`PHASE1_M2_PLAN.md`](../phase1/PHASE1_M2_PLAN.md): build the injection
harness (batman Mandel–Agol, quadratic Claret-2017 LD from TIC stellar params, injected into real
**null-pool calibration** light curves) and run the **η ≥ 0.90 transit-preservation check**
(VAL §4.2) that **finalizes the M1 detrend window** before M3.

## Guarantees (inherited from the plan)

- **Calibration-only, null-pool hosts.** Injects into `is_null & split==calibration` targets;
  the TEST split is never touched (sealed until M4 — G1).
- **Grid + η_min sealed.** Injection grid (P,R_p,b) and η_min = 0.90 come from the seal (VAL §3,§4.2);
  the config mirrors them read-only and must not change them.
- **No thresholds.** M2 sets no detection threshold (those are M3 / Seal #2).
- **Inject → condition → measure.** Inject in relative-flux space into real pre-detrend PDCSAP,
  then re-run the *same* Stage-0 conditioning, then recover δ_post at the known ephemeris.

## Layout

```
research/m2_injection/
├── README.md
├── requirements.txt           # batman-package (+ astroquery for the Claret LD table)
├── config/
│   └── m2_config.yaml         # SIGNED-OFF injection/η config
└── m2_pipeline.py             # M2.1–M2.5 (added after deps install + single-injection probe)
```

## Run order (after deps install)

1. `pip install -r requirements.txt`
2. `python m2_pipeline.py --config config/m2_config.yaml`
   - M2.1 freeze config → M2.2 build harness (LD table, batman) → M2.3 inject grid → re-condition →
     δ_post → η per (P,R_p) cell → M2.4 window finalization (widen where η<0.90) → M2.5 η table + frozen window.
3. Hand the finalized conditioning window + η table to M3.

Outputs: injected/conditioned residuals gitignored (`data/processed/m2/`); the **η table + provenance**
go to `data/manifests/m2/` (small; tracked).
