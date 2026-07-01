"""BAH2026 PS7 — feature ablation on the synthetic 4-class proof set.

Quantifies the committee's central point ("depth does NOT discriminate — you need
the full feature set"). Uses LEAKAGE-SAFE StratifiedGroupKFold: no injection host
LC is shared between train and test, so the score cannot be inflated by host-noise
memorisation. Reports macro-F1 mean ± std across folds.

SCOPE: labels are SYNTHETIC (injected signals on real TESS noise). This validates
the feature design + pipeline, NOT real-world accuracy. Round-2 uses the
organisers' curated labels via the same interface.

Run:  .venv/bin/python hackathon/prototype/ablation.py
Out:  out/ablation.csv  +  figs/ablation.png
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedGroupKFold, cross_validate

import _deckstyle as ds

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out"); FIGS = os.path.join(HERE, "figs")
CSV = os.path.join(OUT, "labeled_features.csv")

SUBSETS = {
    "Duration only":                 ["duration_frac", "best_dur_days", "t_total_h"],
    "Shape only (U vs V)":           ["flat_frac", "ingress_frac", "v_over_u"],
    "EB tells (odd-even, secondary)": ["odd_even_diff", "secondary_depth", "secondary_ratio"],
    "Depth only":                    ["depth", "fit_depth_ppm", "depth_snr"],
    "Detection (SNR, counts)":       ["n_events", "max_snr", "total_snr", "has_evidence"],
    "ALL physics features":          None,
}


def _clf():
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08,
                                          max_depth=4, l2_regularization=1.0,
                                          random_state=0)


def main():
    ds.apply()
    df = pd.read_csv(CSV).replace([np.inf, -np.inf], np.nan)
    y = df["label"].values
    groups = df["host"].values
    Xall = df.drop(columns=["host", "label"])
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)

    rows = []
    for name, cols in SUBSETS.items():
        cols = list(Xall.columns) if cols is None else [c for c in cols if c in Xall.columns]
        res = cross_validate(_clf(), Xall[cols].values, y, groups=groups, cv=cv,
                             scoring=["accuracy", "f1_macro"], n_jobs=-1)
        acc_m, acc_s = res["test_accuracy"].mean(), res["test_accuracy"].std()
        f1_m, f1_s = res["test_f1_macro"].mean(), res["test_f1_macro"].std()
        rows.append((name, len(cols), acc_m, acc_s, f1_m, f1_s))
        print(f"  {name:34s} n={len(cols):2d}  acc={acc_m:.3f}±{acc_s:.3f}  macroF1={f1_m:.3f}±{f1_s:.3f}")

    out = pd.DataFrame(rows, columns=["subset", "n_feat", "acc", "acc_std", "macroF1", "macroF1_std"])
    out.to_csv(os.path.join(OUT, "ablation.csv"), index=False)

    o = out.sort_values("macroF1")
    fig, ax = plt.subplots(figsize=(9.2, 4.7))
    colors = [ds.GREEN if s == "ALL physics features" else ds.BLUE for s in o["subset"]]
    ax.barh(o["subset"], o["macroF1"], xerr=o["macroF1_std"], color=colors,
            edgecolor="0.25", capsize=3.5, height=0.66)
    ax.axvline(0.25, ls="--", color="0.45", lw=1.2, label="random (4 classes) = 0.25")
    for yi, (f1, s) in enumerate(zip(o["macroF1"], o["macroF1_std"])):
        ax.text(f1 + s + 0.012, yi, f"{f1:.2f}", va="center", fontsize=9.5, weight="bold", color=ds.INK)
    ax.set_xlim(0, 1.02)
    ax.set_xlabel("macro-F1  (leakage-safe 5-fold group CV, mean ± std)")
    ax.set_title("No single feature family suffices — the full physics set is required")
    ax.legend(loc="lower right")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    ds.synthetic_banner(fig)
    p = os.path.join(FIGS, "ablation.png"); fig.savefig(p); plt.close(fig)
    print("saved", p)


if __name__ == "__main__":
    main()
