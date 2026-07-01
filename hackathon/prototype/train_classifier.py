"""BAH2026 PS7 — physics-branch (GBT) classifier: leakage-safe evaluation.

Evaluates the HistGBT 4-class classifier with StratifiedGroupKFold out-of-fold
predictions (every sample scored by a model that never saw its injection host),
so the confusion matrix and metrics cannot be inflated by host-noise leakage.
Reports accuracy, macro-F1 with a bootstrap 95% CI, per-class precision/recall/F1,
a confusion matrix, and fold-averaged permutation importance.

SCOPE: SYNTHETIC labels (injected signals on real TESS noise) — proof of the
trained-classifier path, NOT real-world accuracy. Swap in the organisers' curated
labels via the same interface (Round-2).

Usage: .venv/bin/python hackathon/prototype/train_classifier.py
Out:   figs/classifier_eval.png  +  out/classifier_metrics.json
"""
from __future__ import annotations
import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import StratifiedGroupKFold, cross_val_predict
from sklearn.metrics import (accuracy_score, f1_score, confusion_matrix,
                             classification_report, precision_recall_fscore_support)

import _deckstyle as ds

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out"); FIGS = os.path.join(HERE, "figs")
CSV = os.path.join(OUT, "labeled_features.csv")
CLASSES = ["transit", "eclipse", "blend", "other"]


def _clf():
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08,
                                          max_depth=4, l2_regularization=1.0,
                                          random_state=0)


def _bootstrap_macro_f1(y_true, y_pred, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    yt, yp = np.asarray(y_true), np.asarray(y_pred)
    n = len(yt)
    vals = np.empty(B)
    for b in range(B):
        idx = rng.integers(0, n, n)
        vals[b] = f1_score(yt[idx], yp[idx], average="macro", labels=CLASSES, zero_division=0)
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))


def main():
    ds.apply()
    if not os.path.exists(CSV):
        print("Run make_labeled_set.py first."); sys.exit(1)
    df = pd.read_csv(CSV).replace([np.inf, -np.inf], np.nan)
    y = df["label"].values
    groups = df["host"].values
    X = df.drop(columns=["host", "label"])
    feat_names = list(X.columns)
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0)

    # leakage-safe out-of-fold predictions (each sample scored by a model blind to its host)
    yp = cross_val_predict(_clf(), X.values, y, groups=groups, cv=cv, n_jobs=-1)
    acc = accuracy_score(y, yp)
    mf1 = f1_score(y, yp, average="macro", labels=CLASSES, zero_division=0)
    lo, hi = _bootstrap_macro_f1(y, yp)
    print(f"OOF accuracy: {acc:.3f} | macro-F1: {mf1:.3f}  (95% CI [{lo:.3f}, {hi:.3f}])\n")
    print(classification_report(y, yp, labels=CLASSES, digits=3, zero_division=0))
    cm = confusion_matrix(y, yp, labels=CLASSES)
    P, R, F, _ = precision_recall_fscore_support(y, yp, labels=CLASSES, zero_division=0)

    # fold-averaged permutation importance (leakage-safe: permute on held-out host fold)
    imps = []
    for tr, te in cv.split(X.values, y, groups):
        clf = _clf().fit(X.values[tr], y[tr])
        r = permutation_importance(clf, X.values[te], y[te], n_repeats=8,
                                   random_state=0, scoring="f1_macro", n_jobs=-1)
        imps.append(r.importances_mean)
    imp = np.mean(imps, axis=0)
    order = np.argsort(imp)[::-1][:10]

    json.dump({"oof_accuracy": acc, "macro_f1": mf1, "macro_f1_ci95": [lo, hi],
               "per_class": {c: {"precision": float(P[i]), "recall": float(R[i]), "f1": float(F[i])}
                             for i, c in enumerate(CLASSES)},
               "confusion_matrix": cm.tolist(), "classes": CLASSES,
               "n_samples": int(len(y)), "n_hosts": int(df["host"].nunique()),
               "cv": "StratifiedGroupKFold(5)", "labels": "synthetic"},
              open(os.path.join(OUT, "classifier_metrics.json"), "w"), indent=2)

    # ---- figure: confusion matrix + permutation importance ----
    fig, ax = plt.subplots(1, 2, figsize=(12.4, 5.0), gridspec_kw={"width_ratios": [1, 1.05]})
    cmn = cm / cm.sum(axis=1, keepdims=True)
    im = ax[0].imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    ax[0].set(xticks=range(4), yticks=range(4), xticklabels=CLASSES, yticklabels=CLASSES,
              xlabel="predicted", ylabel="true")
    ax[0].set_title(f"Confusion matrix — out-of-fold (n={len(y)})\n"
                    f"accuracy {acc:.2f} · macro-F1 {mf1:.2f} [{lo:.2f}, {hi:.2f}]", fontsize=11)
    for i in range(4):
        for j in range(4):
            ax[0].text(j, i, f"{cm[i,j]}\n{cmn[i,j]*100:.0f}%", ha="center", va="center",
                       fontsize=9.5, color="white" if cmn[i, j] > 0.5 else ds.INK)
    fig.colorbar(im, ax=ax[0], fraction=0.046, pad=0.04, label="row fraction")

    ax[1].barh([feat_names[i] for i in order][::-1],
               [imp[i] for i in order][::-1], color=ds.BLUE, edgecolor="0.25")
    ax[1].set_title("Top features — permutation importance\n(fold-averaged, Δ macro-F1)", fontsize=11)
    ax[1].set_xlabel("Δ macro-F1 when feature is shuffled")
    fig.suptitle("PS7 physics-branch classifier — leakage-safe evaluation",
                 fontsize=13.5, weight="bold", color=ds.NAVY)
    fig.tight_layout(rect=(0, 0.05, 1, 0.95))
    ds.synthetic_banner(fig)
    p = os.path.join(FIGS, "classifier_eval.png"); fig.savefig(p); plt.close(fig)
    print("saved", p)


if __name__ == "__main__":
    main()
