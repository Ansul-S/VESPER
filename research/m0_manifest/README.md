# M0 manifest tooling

Tooling that executes milestone **M0** of [`PHASE1_EXECUTION_PLAN.md`](../../PHASE1_EXECUTION_PLAN.md):
freeze the TESS sector/target manifest and the leakage-safe calibration/test split,
then content-hash it (**Seal #1**).

> **Status: scaffold (stubs).** Function bodies that touch archives are intentionally
> unimplemented until the [M0 frozen-choices proposal](../../PHASE1_M0_CHOICES.md) is
> **signed off**. This package does **not** query any archive or compute a hash until
> the config is filled and execution is authorized.

## Guarantees (inherited from the plan)

- **Metadata only.** Queries target catalog/product-availability metadata (TIC, SPOC
  2-min availability, TOI/EB labels, coordinates, stellar params). **No light-curve
  flux is downloaded here** — that is M1.
- **No thresholds.** M0 sets *which stars*, never *how significant*. The calibration
  thresholds (`z⋆, θ, …`) are M3 (Seal #2).
- **TEST sealed.** No detection statistic is computed on the TEST split (plan G1).
- **Reproducible.** Catalog versions, query timestamps, resolved library versions
  (`pip freeze`), and RNG seeds are pinned into the manifest provenance (plan G5).

## Layout

```
research/m0_manifest/
├── README.md                     # this file
├── requirements.txt              # archive-query stack (metadata-only)
├── config/
│   └── m0_config.template.yaml   # frozen-choices schema (filled on sign-off → m0_config.yaml)
└── m0_pipeline.py                # M0.1–M0.6 orchestrator (stubs until sign-off)
```

## Run order (after sign-off)

1. Fill `config/m0_config.yaml` from the signed [`PHASE1_M0_CHOICES.md`](../../PHASE1_M0_CHOICES.md).
2. `python m0_pipeline.py --config config/m0_config.yaml`
   - M0.1 freeze sectors → M0.2 target manifest → M0.3 labels/null pool →
     M0.4 leakage-safe split → M0.5 feasibility/power → M0.6 assemble + hash (**Seal #1**).
3. Record the Seal #1 hash in `PHASE1_EXECUTION_PLAN.md` §3.7 and the daily research log.

## Setup

```
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip freeze > config/pip-freeze.lock   # captured into manifest provenance at Seal #1
```
