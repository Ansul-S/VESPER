# M0 manifest — external artifact pointer

The frozen M0 manifest **table** (22,723 targets) is **not stored in git** (keep the repo
lightweight; standard research practice). Git holds only the **hashes + provenance**; the
table lives as a **GitHub release asset**. This file is the pointer.

## Seal of record

- **Seal #1 (manifest content hash, SHA-256):**
  `1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f`
  — hash of the *canonical CSV serialization* of the manifest (sorted by `tic`, fixed
  columns, `float_format=%.6f`). This is the anti-tuning seal; see
  [`m0_manifest_provenance.json`](./m0_manifest_provenance.json).

## Release assets

Release tag **`m0-manifest-v1`** →
<https://github.com/Ansul-S/TRINETRA-X/releases/tag/m0-manifest-v1>

| Asset | Role | File SHA-256 |
|-------|------|--------------|
| `m0_manifest.parquet` | Frozen manifest table (Table T1: targets + split + labels + feasibility inputs) | `7d1aa7e72ac990c4034a4839728edcd83dff29a3e5b7ca5d790027a05900de22` |
| `m0_targets.parquet` | Pre-label target cross-match (regeneration aid; avoids re-querying MAST/TIC) | `66a51c7af7cea12b3102e4444735703329de09815e30360dab93ffc8214ccc1b` |
| `m0_toi_snapshot.csv` | Pinned TOI label snapshot (also tracked in git) | `20c2a2499fdb8962d4b8ac016ddc4020c62199d3bb56b94dff98eb2775cce137` |

> The two SHA-256 kinds are distinct: **Seal #1** is the canonical-CSV content hash (the
> seal); the per-asset hashes above verify **download integrity** of the parquet/CSV files.

## Verify / regenerate

```bash
# 1. download the manifest asset, then verify file integrity:
shasum -a 256 m0_manifest.parquet   # expect 7d1aa7e7...

# 2. verify it reproduces Seal #1 (canonical content hash):
python - <<'PY'
import hashlib, pandas as pd
m = pd.read_parquet("m0_manifest.parquet")
csv = m.sort_values("tic").to_csv(index=False, float_format="%.6f").encode()
print(hashlib.sha256(csv).hexdigest())   # expect 1f2d49e1...
PY

# OR regenerate from scratch (re-queries archives; needs network + research/m0_manifest/requirements.txt):
python research/m0_manifest/m0_pipeline.py --config research/m0_manifest/config/m0_config.yaml
```
