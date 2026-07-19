# Superseded v2 arm code (historical provenance — do not use)

This folder preserves the **v2 (targeted-TLS) realization** that Finding B proved
non-executable (DR-002, 2026-06-19): the TLS SDE is normalized across the searched
grid, so a narrow-grid SDE is not comparable to the full-grid threshold `T`, and
`transitleastsquares` additionally ignores period windows holding < 100 trial
periods (Finding A) — the "targeted" arm silently ran a full search.

- `m4_run.py` — the v2 dual-arm driver. It produced the `data/manifests/m4/dry_run/`
  artifacts cited by DR-002 §1; it is kept so those artifacts remain reproducible.
- `arms_v2.py` — `route()` + `arm_b_combined()` (targeted-TLS Arm B), extracted from
  `arms.py` during the 2026-07-19 audit remediation so the live module no longer
  carries a falsified architecture.

The sealed v3 TEST run used `m4_driver.py` + `confirmer.py` (transit-LR confirmer),
not this code.
