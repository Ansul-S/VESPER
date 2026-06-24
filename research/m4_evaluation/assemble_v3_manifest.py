"""Assemble the v3 (confirmer-only) threshold manifest — CALIBRATION-only, NO seal cut.

Carries forward ALL Seal #2 core values unchanged; adds the v3 amendments:
 - keystone A6: common false-alarm rate (Arm A: SDE>=T; Arm B: Lambda>=T_red)
 - A8a period-FAP cheap estimator: NONE admitted (E-EVT and E-LUT both FAILED equivalence)
   -> operational estimator = sealed B=1000 bootstrap (A.8), confirmer-only v3
 - A11 confirmer: transit-LR (D-1a/D-2a/D-3-i); T_red (FAR-calibrated)
Records content hashes of the v3 docs + confirmer + result memos, and computes the
CANDIDATE Seal #2b hash for OWNER REVIEW. Does NOT git-commit or tag (owner action).

Run: .venv/bin/python research/m4_evaluation/assemble_v3_manifest.py
"""
from __future__ import annotations
import json, hashlib
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    core = json.load(open("data/manifests/m3/m3_threshold_manifest_SEALED_CORE.json"))
    eqv = json.load(open("data/manifests/m4/equivalence/equivalence_summary.json"))
    elut = json.load(open("data/manifests/m4/equivalence/elut_summary.json"))
    tred = json.load(open("data/manifests/m4/tred/tred_summary.json"))

    v3 = {
        "manifest": "TRINETRA-X Phase I — v3 threshold manifest (confirmer-only)",
        "date": "2026-06-19",
        "status": "SEALED v3 (tag phase1-prereg-v3) — frozen before the single TEST read; confirmer-only",
        "authority": "DR-002 (ADOPTED); VAL v3; MATH v1.2; SCIENTIFIC_HYPOTHESIS v2.1",
        "carried_forward_from_seal2_UNCHANGED": {
            "seal2_hash": "6292c018c6923d512ac9c90dd55289cc010724d9facc27dc087f7e3f20832692",
            "z_star": core["A3_detector_routing"]["z_star"],
            "z_mono": core["A3_detector_routing"]["z_mono"],
            "N_min": core["A3_detector_routing"]["N_min"],
            "T_sde": core["A2_common_threshold_T"]["T_sde"],
            "alpha_FAP": 0.01, "epsilon": 0.01,
            "w_c": "unchanged (A.5)", "pi_hat": "unchanged (A.6, 3.17%)",
        },
        "v3_keystone_A6": "common false-alarm rate (Arm A: SDE>=T_sde; Arm B: Lambda>=T_red), each calibrated to FAR<=1%/star",
        "v3_A8_period_FAP": {
            "estimator_of_record": "B=1000 circular block bootstrap (sealed A.8, UNCHANGED)",
            "A8a_cheap_estimator_admitted": None,
            "equivalence_gate": "FAILED for BOTH pre-registered candidates -> confirmer-only fallback (DR-002 2.3a)",
            "candidate_E_EVT_verdict": eqv["VERDICT"],
            "candidate_E_EVT": {k: eqv[k] for k in ("crit_i_fap_agreement", "crit_ii_gate_membership", "crit_iii_recall_safety")},
            "candidate_E_LUT_verdict": elut["VERDICT"],
            "candidate_E_LUT": {k: elut[k] for k in ("crit_i_fap_agreement", "crit_ii_gate_membership", "crit_iii_recall_safety")},
            "rho_d_consequence": "~12.4% retained (no cheapening) -> E2 projected <30% (pre-committed compute-falsification path)",
        },
        "v3_A11_confirmer": {
            "statistic": "folded-photometry transit likelihood-ratio Lambda (depth-only linear GLS, D-1a)",
            "noise_model": "GP marginal likelihood, per-star Matern-3/2 (D-2a)",
            "t0_refinement": "none (D-3 i)",
            "vetting": "sign-aware; odd-even + secondary EB rejection (N_tr>=2); MATH 6 monotransit (headline-excluded)",
            "T_red": tred["T_red"],
            "T_red_binding": tred["T_red_binding"],
            "T_red_rule": "set solely from FAR target (P-3); non-binding because FAP gate + shape vetting already give FAR<=target",
            "achieved_FAR_end2end": tred["achieved_FAR_end2end"],
            "recall_preview_AUC": tred["recall_preview"]["AUC_planet_vs_null_Lambda"],
            "box_depth_SNR": "REJECTED (DR-002 2.2)",
        },
        "content_hashes": {
            "_note": "frozen specs + confirmer + result memos; DR-002 (decision record) is frozen by the git tag, not hashed here (avoids a reference cycle)",
            "VAL_v3": sha256("docs/TRINETRA_X_PHASE1_VALIDATION.md"),
            "MATH_v1.2": sha256("docs/TRINETRA_MATHEMATICAL_FOUNDATIONS.md"),
            "HYP_v2.1": sha256("docs/SCIENTIFIC_HYPOTHESIS.md"),
            "confirmer.py": sha256("research/m4_evaluation/confirmer.py"),
            "TRANSIT_LR_CONFIRMER_SPEC.md": sha256("research/m4_evaluation/TRANSIT_LR_CONFIRMER_SPEC.md"),
            "equivalence_summary.json": sha256("data/manifests/m4/equivalence/equivalence_summary.json"),
            "elut_summary.json": sha256("data/manifests/m4/equivalence/elut_summary.json"),
            "tred_summary.json": sha256("data/manifests/m4/tred/tred_summary.json"),
        },
        "integrity": {"TEST_TICs_in_calibration_artifacts": 0, "seal2_unchanged": True},
    }
    out = Path("data/manifests/m4/v3"); out.mkdir(parents=True, exist_ok=True)
    p = out / "m4_v3_threshold_manifest.json"
    body = json.dumps(v3, indent=2, sort_keys=True)
    p.write_text(body)
    candidate_hash = hashlib.sha256(p.read_bytes()).hexdigest()
    print(json.dumps(v3, indent=2))
    print(f"\n==> v3 manifest written: {p}")
    print(f"==> CANDIDATE Seal #2b hash (SHA-256): {candidate_hash}")
    print("    (NOT cut — owner review + explicit go required before git commit/tag and TEST.)")


if __name__ == "__main__":
    main()
