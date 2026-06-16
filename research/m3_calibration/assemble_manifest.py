"""M3 threshold-manifest assembly (VAL Appendix A.1-A.10). PROVISIONAL — presented for owner review.

Consolidates every [sealed at M3] value + the frozen Appendix-A configuration into one manifest,
organized by clause. Computes a CANDIDATE content hash for reference ONLY — this becomes Seal #2
*only* upon explicit owner approval (the manifest is written with seal2_status='UNSEALED').
TEST remains sealed until M4.

Run:  python research/m3_calibration/assemble_manifest.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

REPORT = Path("data/manifests/m3")


def _load(p):
    return json.loads((REPORT / p).read_text())


def run() -> None:
    thr = _load("m3_thresholds_cleaned_PROVISIONAL.json")
    stab = _load("m3_stability_audit.json")
    occ = _load("m3_occurrence_weights.json")
    machine = json.loads(Path("/tmp/machine.json").read_text())
    after = thr["after_cleaned"]
    bt = stab["bootstrap_thresholds"]
    m3cfg_sha = hashlib.sha256(Path("research/m3_calibration/config/m3_config.yaml").read_bytes()).hexdigest()

    manifest = {
        "title": "TRINETRA-X Phase I — M3 Threshold Manifest (Seal #2 content)",
        "seal2_status": "UNSEALED — provisional; awaiting explicit owner approval",
        "created": "2026-06-16",
        "binds_to": {"prereg_tag": "phase1-prereg-v2", "seal1_manifest_sha256":
                     "1f2d49e194b0960f1eacb0c72c25087b4c299620e38f299e2d55706199e83f1f"},
        "calibration_basis": {
            "set": "cleaned 1000-star null calibration (854 after 146 contaminant exclusions)",
            "m0_null_definition": "PRESERVED (TOI-removed); cleaned set is a derived M3 subset",
            "exclusions": {"total": 146, "by_reason": thr["cleaning"]["by_reason"],
                           "table": "data/manifests/m3/calibration_exclusions.csv"},
            "retained_high_sde_survivors": {"n": 31, "table": "data/manifests/m3/retained_high_sde_audit.csv"},
            "m3_config_sha256": m3cfg_sha, "seed": 20260616, "detrend_window_days": 2.5},

        # ---- Appendix A clauses ----
        "A1_TLS_baseline": {"engine": "transitleastsquares", "version": "1.32",
                            "oversampling_factor": 3, "period_min_days": 0.5,
                            "period_max": "0.5 * baseline (>=2 transits)",
                            "identical_both_arms": True, "no_BLS_substitute": True},
        "A2_common_threshold_T": {"T_sde": after["T_sde"], "rule": "FAR <= 1%/star on null calibration stars",
                                  "achieved_far_basis": "p99 of cleaned null SDE distribution (n=854)",
                                  "bootstrap_95CI": [bt["T_sde"]["p2.5"], bt["T_sde"]["p97.5"]],
                                  "bootstrap_sd": bt["T_sde"]["sd"]},
        "A3_detector_routing": {"z_star": after["z_star"], "z_star_rule": "<=1 false event/LC (null)",
                                "z_star_achieved": after["false_events_at_z_star"],
                                "z_mono": after["z_mono"], "z_mono_rule": "<=0.1 false event/LC (null)",
                                "z_mono_achieved": after["false_events_at_z_mono"],
                                "N_min": 2, "z_mono_gt_z_star": True,
                                "detector": "GP-whitened box matched filter; duration grid {0.05,0.1,0.2,0.4,0.8} d",
                                "z_star_95CI": [bt["z_star"]["p2.5"], bt["z_star"]["p97.5"]],
                                "z_mono_95CI": [bt["z_mono"]["p2.5"], bt["z_mono"]["p97.5"]]},
        "A4_recovery_predicate": {"period_tol": "1% / harmonics m in {2,3}", "epoch_tol": "+/-0.5 T14",
                                  "significance": "SDE >= T"},
        "A5_occurrence_weights_wc": {"w_P": "log-uniform over {0.5,1,2,4,8,16} d",
                                     "w_R_normalized": occ["w_R_radius_prior"]["w_R_normalized"],
                                     "w_c": occ["w_c"], "source": occ["source"],
                                     "assumptions": occ["assumptions_for_review"]},
        "A6_prevalence_pi_hat": occ["pi_hat"],
        "A7_runtime_machine": {**machine, "protocol": "single-thread CPU-core-seconds; median >=5 repeats; "
                               "warm cache; Stage-0 conditioning excluded; rho_d reported separately"},
        "A8_bootstrap_FAP": {"scheme": "noise-model-aware circular block bootstrap",
                             "block_length": "L_b = 3 * max(tau_GP, T14)", "B": 1000,
                             "alpha_fap": after_alpha(thr), "achieved_null_exceedance": null_exc(thr)},
        "A9_conditioning": {"method": "wotan biweight", "window_days": 2.5, "cval": 5,
                            "masking": "SPOC default quality + momentum-dump + scattered-light",
                            "eta_min": 0.90, "eta_gate": "PASS on Rp>=2 (M2); Rp=1 row noise-limited"},
        "epsilon_fast_path": {"epsilon": 0.01, "window": "[P_hat(1-eps), P_hat(1+eps)]"},

        "anti_tuning": {"split": "CALIBRATION-null only", "TEST": "sealed until single M4 run",
                        "sealed_docs_unmodified": "git diff phase1-prereg-v2 empty"},
    }

    candidate = hashlib.sha256(json.dumps(manifest, sort_keys=True, default=str).encode()).hexdigest()
    out = {"manifest": manifest,
           "candidate_content_sha256": candidate,
           "candidate_note": "Reference only. Becomes Seal #2 ONLY upon explicit owner approval; "
                             "not yet sealed (seal2_status=UNSEALED)."}
    (REPORT / "m3_threshold_manifest_PROVISIONAL.json").write_text(json.dumps(out, indent=2, default=str))
    print("candidate content hash (NOT sealed):", candidate)
    print("wrote data/manifests/m3/m3_threshold_manifest_PROVISIONAL.json")


def after_alpha(thr):
    return thr["targets"]["alpha_fap"]


def null_exc(thr):
    return thr["after_cleaned"]["alpha_fap_null_exceedance"]


if __name__ == "__main__":
    run()
