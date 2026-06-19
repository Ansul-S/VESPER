"""M4 Seal #2 loader + TEST-access guard (Phase I).

Loads the FROZEN Seal #2 thresholds read-only and refuses to run if either the
threshold manifest or the bound M3 config has drifted from its sealed hash. M4
introduces NO new frozen parameter: every value here comes from the seal.

Two guards protect the single-shot discipline:
  * verify_seal()        — SEALED_CORE sha256 == 6292c018... AND m3_config sha256 == 0400e2db...
  * assert_split_allowed — dry-run may NEVER touch TEST; the TEST run requires an
                           explicit confirmation token AND a verified seal.

Nothing in this module reads any light curve; it only loads frozen scalars.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType

import yaml

SEAL2_SHA256 = "6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692"
M3_CONFIG_SHA256 = "0400e2db20884ecfb6ecfb5bcd2686282e80c6ad377e78ff7476b11b7e96454d"
SEAL1_SHA256 = "1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f"

SEALED_CORE = Path("data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json")
M3_CONFIG = Path("research/m3_calibration/config/m3_config.yaml")

# M4 must read these from the seal — never set them. Any attempt to override is rejected.
_FROZEN_KEYS = {"z_star", "z_mono", "n_min", "t_sde", "epsilon", "alpha_fap",
                "duration_grid", "oversampling", "period_min_days",
                "period_max_frac_baseline", "block_len_multiple", "b_surrogates"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class FrozenThresholds:
    """Read-only Seal #2 values. Frozen dataclass — assignment raises."""
    z_star: float
    z_mono: float
    n_min: int
    T_sde: float
    epsilon: float
    alpha_fap: float
    duration_grid: tuple
    oversampling: int
    period_min_days: float
    period_max_frac_baseline: float
    block_len_multiple: int
    B: int
    w_c: MappingProxyType
    pi_hat: float
    seal2_sha256: str
    m3_config_sha256: str

    def tls_cfg(self) -> dict:
        """The A.1 TLS config, identical for both arms (the fairness keystone)."""
        return {"oversampling_factor": self.oversampling,
                "period_min_days": self.period_min_days,
                "period_max_frac_baseline": self.period_max_frac_baseline}


def verify_seal() -> tuple[str, str]:
    """Verify both sealed hashes. Raises SystemExit on any drift (fail closed)."""
    if not SEALED_CORE.exists():
        raise SystemExit(f"[M4] FATAL: sealed manifest missing: {SEALED_CORE}")
    core_h = _sha256(SEALED_CORE)
    if core_h != SEAL2_SHA256:
        raise SystemExit(f"[M4] FATAL: Seal #2 drift. got {core_h} expected {SEAL2_SHA256}")
    cfg_h = _sha256(M3_CONFIG)
    if cfg_h != M3_CONFIG_SHA256:
        raise SystemExit(f"[M4] FATAL: m3_config drift. got {cfg_h} expected {M3_CONFIG_SHA256}")
    return core_h, cfg_h


def load_frozen() -> FrozenThresholds:
    """Load Seal #2 thresholds read-only after verifying both hashes."""
    import json
    core_h, cfg_h = verify_seal()
    core = json.loads(SEALED_CORE.read_text())
    m3cfg = yaml.safe_load(M3_CONFIG.read_text())  # bound by hash above

    a1, a2, a3, a8 = core["A1_TLS_baseline"], core["A2_common_threshold_T"], \
        core["A3_detector_routing"], core["A8_bootstrap_FAP"]
    return FrozenThresholds(
        z_star=float(a3["z_star"]),
        z_mono=float(a3["z_mono"]),
        n_min=int(a3["N_min"]),
        T_sde=float(a2["T_sde"]),
        epsilon=float(core["epsilon_fast_path"]["epsilon"]),
        alpha_fap=float(a8["alpha_fap"]),
        duration_grid=tuple(m3cfg["detector"]["duration_grid_days"]),
        oversampling=int(a1["oversampling_factor"]),
        period_min_days=float(a1["period_min_days"]),
        period_max_frac_baseline=float(m3cfg["tls"]["period_max_frac_baseline"]),
        block_len_multiple=int(m3cfg["period_recovery"]["block_len_multiple"]),
        B=int(a8["B"]),
        w_c=MappingProxyType({k: float(v) for k, v in core["A5_occurrence_weights_wc"]["w_c"].items()}),
        pi_hat=float(core["A6_prevalence_pi_hat"]["value"]),
        seal2_sha256=core_h,
        m3_config_sha256=cfg_h,
    )


def reject_frozen_overrides(run_cfg: dict) -> None:
    """Fail if the M4 run config tries to set any Seal #2 value (M1/M3 guard, A.10)."""
    def _flatten(o):
        ks = set()
        if isinstance(o, dict):
            for k, v in o.items():
                ks.add(str(k).lower().replace("-", "_")); ks |= _flatten(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                ks |= _flatten(v)
        return ks
    leaked = _flatten(run_cfg) & _FROZEN_KEYS
    if leaked:
        raise SystemExit(f"[M4] FATAL: run config attempts to override sealed keys: {sorted(leaked)}")


def assert_split_allowed(mode: str, split: str, confirm_token: str | None = None) -> None:
    """The single-shot TEST guard.

    mode == 'dry_run'  -> split MUST NOT be 'test' (no TEST access whatsoever).
    mode == 'test'     -> split MUST be 'test', the seal MUST verify, and the caller
                          MUST pass the exact confirmation token (set only after the
                          dry-run is reviewed and the owner signs §10).
    """
    mode = (mode or "").lower()
    split = (split or "").lower()
    if mode == "dry_run":
        if split == "test":
            raise SystemExit("[M4] FATAL: dry-run is FORBIDDEN from reading the TEST split.")
        if split not in {"calibration", "synthetic"}:
            raise SystemExit(f"[M4] FATAL: dry-run split must be calibration/synthetic, got '{split}'.")
        return
    if mode == "test":
        if split != "test":
            raise SystemExit(f"[M4] FATAL: TEST run requires split=='test', got '{split}'.")
        verify_seal()
        if confirm_token != "READ-TEST-ONCE-SEAL2-APPROVED":
            raise SystemExit("[M4] FATAL: TEST read blocked — owner §10 confirmation token absent.")
        return
    raise SystemExit(f"[M4] FATAL: unknown mode '{mode}' (expected dry_run|test).")


if __name__ == "__main__":
    fr = load_frozen()
    print("[M4] Seal #2 verified:", fr.seal2_sha256[:12], "| m3_config:", fr.m3_config_sha256[:12])
    print(f"  z_star={fr.z_star} z_mono={fr.z_mono} N_min={fr.n_min} T={fr.T_sde:.4f} "
          f"eps={fr.epsilon} alpha_fap={fr.alpha_fap}")
    print(f"  duration_grid={fr.duration_grid} oversampling={fr.oversampling} "
          f"P=[{fr.period_min_days},{fr.period_max_frac_baseline}*base] L_b={fr.block_len_multiple}x B={fr.B}")
    wsmall = sum(v for k, v in fr.w_c.items() if k.endswith("_R1") or k.endswith("_R2"))
    print(f"  w_c cells={len(fr.w_c)} sum={sum(fr.w_c.values()):.4f} weight(Rp<=2)={wsmall:.4f} pi_hat={fr.pi_hat:.5f}")
