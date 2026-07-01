"""Shared publication styling for PS7 deck figures (consistent typography/palette)."""
from __future__ import annotations
import matplotlib as mpl

NAVY = "#13294b"; BLUE = "#2c6fbb"; GREEN = "#1e8449"; RED = "#c0392b"
GOLD = "#b9770e"; GREY = "#566573"; INK = "#20272e"
CLASS_COLORS = {"transit": GREEN, "eclipse": RED, "blend": "#7d3c98", "other": GREY}


def apply():
    mpl.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.dpi": 160,
        "font.family": "DejaVu Sans", "font.size": 11,
        "axes.titlesize": 12.5, "axes.titleweight": "bold", "axes.titlecolor": NAVY,
        "axes.labelsize": 11, "axes.labelcolor": INK,
        "axes.edgecolor": "#556", "axes.linewidth": 1.0,
        "xtick.labelsize": 10, "ytick.labelsize": 10,
        "xtick.color": INK, "ytick.color": INK,
        "legend.fontsize": 9, "legend.frameon": True, "legend.framealpha": 0.9,
        "axes.grid": False,
    })


def synthetic_banner(fig, text="SYNTHETIC LABELS — injected signals on real TESS noise (proof of pipeline; not real-world accuracy)"):
    fig.text(0.5, 0.005, text, ha="center", va="bottom", fontsize=8.2,
             style="italic", color="#8a5a00",
             bbox=dict(boxstyle="round,pad=0.3", fc="#fff6e6", ec="#e0b060", lw=0.8))
