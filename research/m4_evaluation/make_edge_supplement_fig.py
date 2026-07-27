"""RES-5 (Wave 1): S-edge supplement figure from the completed edge control.

Two panels from data/manifests/m4/e2_retiming/edge_control.csv (edge_control.py,
2026-07-19; matches the main-paper figure house-style F3/F8):
  (a) SDE distributions by condition (A: P=0.5 on the sealed grid; B: same injections,
      grid extended to pmin=0.3; C: P=0.62 off-node) with the sealed threshold T=10.74.
  (b) recovery-outcome breakdown (recovered / epoch-only failure / period-or-SDE failure)
      showing the P=0.5 d shortfall is an EPOCH-predicate failure, not detection power.

Analysis/plot only on the already-computed calibration control; no TEST data, no compute
beyond plotting. (Per-injection T0 errors were not persisted to the CSV, so panel (b)
uses the failure-mode counts derivable from period_ok/sde_ok/recovered; a T0-error
histogram would need re-running the control to store T0 — noted in the supplement.)

Run:  .venv/bin/python research/m4_evaluation/make_edge_supplement_fig.py
Out:  research/m4_evaluation/figures/S1_edge_control.png
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CSV = "data/manifests/m4/e2_retiming/edge_control.csv"
FIG = Path("research/m4_evaluation/figures")
T_SDE = 10.740887727255977
LABELS = {"A_edge_pmin0.5": "A: P=0.5, sealed grid",
          "B_extended_pmin0.3": "B: P=0.5, grid→0.3",
          "C_offnode_P0.62_pmin0.5": "C: P=0.62, off-node"}
COLORS = {"A_edge_pmin0.5": "#e76f51", "B_extended_pmin0.3": "#f4a261",
          "C_offnode_P0.62_pmin0.5": "#2a9d8f"}


def main():
    d = pd.read_csv(CSV)
    conds = list(LABELS)
    FIG.mkdir(parents=True, exist_ok=True)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.6))

    # (a) SDE distributions
    data = [d[d.arm == c].sde.to_numpy() for c in conds]
    parts = a1.boxplot(data, positions=range(len(conds)), widths=0.5, patch_artist=True,
                       showfliers=True, medianprops=dict(color="black"))
    for patch, c in zip(parts["boxes"], conds):
        patch.set_facecolor(COLORS[c]); patch.set_alpha(0.75)
    a1.axhline(T_SDE, ls="--", color="#264653", lw=1.2, label=f"sealed T = {T_SDE:.2f}")
    a1.set_xticks(range(len(conds))); a1.set_xticklabels([LABELS[c] for c in conds], fontsize=8)
    a1.set_ylabel("TLS SDE"); a1.set_title("(a) Detection significance is not the problem")
    a1.legend(fontsize=8)

    # (b) recovery-outcome breakdown
    rec, epoch_fail, other_fail = [], [], []
    for c in conds:
        g = d[d.arm == c]
        ps = g.period_ok.astype(bool) & g.sde_ok.astype(bool)
        r = int(g.recovered.sum())
        ef = int((ps & ~g.recovered.astype(bool)).sum())          # right period+SDE, epoch failed
        of = len(g) - r - ef
        rec.append(r); epoch_fail.append(ef); other_fail.append(of)
    x = np.arange(len(conds))
    a2.bar(x, rec, 0.6, label="recovered", color="#2a9d8f")
    a2.bar(x, epoch_fail, 0.6, bottom=rec, label="epoch-only failure", color="#e76f51")
    a2.bar(x, other_fail, 0.6, bottom=np.array(rec) + np.array(epoch_fail),
           label="period/SDE failure", color="#8d99ae")
    for i in range(len(conds)):
        if epoch_fail[i]:
            a2.text(i, rec[i] + epoch_fail[i] / 2, str(epoch_fail[i]), ha="center",
                    va="center", fontsize=9, color="white", fontweight="bold")
    a2.set_xticks(x); a2.set_xticklabels([LABELS[c] for c in conds], fontsize=8)
    a2.set_ylabel("injections (n=60 each)")
    a2.set_title("(b) The P=0.5 d shortfall is an epoch failure")
    a2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(FIG / "S1_edge_control.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", FIG / "S1_edge_control.png")
    print("failure breakdown:", {LABELS[c]: dict(recovered=rec[i], epoch_only=epoch_fail[i],
          other=other_fail[i]) for i, c in enumerate(conds)})


if __name__ == "__main__":
    main()
