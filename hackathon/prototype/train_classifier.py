"""BAH2026 PS7 prototype — train the physics-branch (GBT) classifier.

Trains a gradient-boosted classifier on the injected labeled feature set
(make_labeled_set.py), reports a confusion matrix + feature importances on a
held-out split, and saves a figure. This proves the trained-classifier path;
swap in the organizer's curated labels when available (same interface).

Usage: .venv/bin/python hackathon/prototype/train_classifier.py
"""
from __future__ import annotations
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "out"); FIGS = os.path.join(HERE, "figs")
os.makedirs(FIGS, exist_ok=True)
CSV = os.path.join(OUT, "labeled_features.csv")
CLASSES = ["transit", "eclipse", "blend", "other"]


def main():
    if not os.path.exists(CSV):
        print("Run make_labeled_set.py first."); sys.exit(1)
    df = pd.read_csv(CSV)
    y = df["label"].values
    X = df.drop(columns=["label"]).replace([np.inf, -np.inf], np.nan)
    feat_names = list(X.columns)

    Xtr, Xte, ytr, yte = train_test_split(X.values, y, test_size=0.3,
                                          stratify=y, random_state=0)
    clf = HistGradientBoostingClassifier(max_iter=300, learning_rate=0.08,
                                         max_depth=4, l2_regularization=1.0,
                                         random_state=0)
    clf.fit(Xtr, ytr)
    acc = clf.score(Xte, yte)
    print(f"Held-out accuracy: {acc:.3f}\n")
    yp = clf.predict(Xte)
    print(classification_report(yte, yp, labels=CLASSES, digits=3, zero_division=0))

    cm = confusion_matrix(yte, yp, labels=CLASSES)

    # permutation importance (model-agnostic, robust)
    from sklearn.inspection import permutation_importance
    imp = permutation_importance(clf, Xte, yte, n_repeats=10, random_state=0)
    order = np.argsort(imp.importances_mean)[::-1][:10]

    fig, ax = plt.subplots(1, 2, figsize=(13, 5))
    im = ax[0].imshow(cm, cmap="Blues")
    ax[0].set(xticks=range(4), yticks=range(4), xticklabels=CLASSES,
              yticklabels=CLASSES, xlabel="predicted", ylabel="true",
              title=f"Confusion matrix (held-out)\naccuracy={acc:.3f}")
    for i in range(4):
        for j in range(4):
            ax[0].text(j, i, cm[i, j], ha="center", va="center",
                       color="white" if cm[i, j] > cm.max() / 2 else "black")
    ax[1].barh([feat_names[i] for i in order][::-1],
               [imp.importances_mean[i] for i in order][::-1], color="#2c6fbb")
    ax[1].set(title="Top physics features (permutation importance)", xlabel="Δ accuracy")
    fig.suptitle("PS7 physics-branch classifier — injected labels (proof of path)",
                 fontsize=13, weight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    p = os.path.join(FIGS, "classifier_eval.png"); fig.savefig(p, dpi=120)
    print("saved", p)


if __name__ == "__main__":
    main()
