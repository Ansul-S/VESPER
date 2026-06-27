"""Assemble the BAH2026 PS7 idea-submission deck as a PDF (matplotlib PdfPages).

Mirrors the official PPTX template slide order. Team fields are PLACEHOLDERS
(fill before submitting). Embeds the real prototype figures.

Run:  .venv/bin/python hackathon/deck/build_deck.py
Out:  hackathon/deck/BAH2026_PS7_idea_deck.pdf
"""
from __future__ import annotations
import os
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(__file__)
FIGS = os.path.join(HERE, "figs")
PROTO_FIGS = os.path.join(HERE, "..", "prototype", "figs")
OUT = os.path.join(HERE, "BAH2026_PS7_idea_deck.pdf")

NAVY, ACCENT, GREY = "#13294b", "#2c6fbb", "#444444"
W, H = 13.33, 7.5


def _page(pdf, draw):
    fig = plt.figure(figsize=(W, H)); fig.patch.set_facecolor("white")
    draw(fig)
    pdf.savefig(fig); plt.close(fig)


def _header(fig, title, n):
    fig.text(0.06, 0.90, title, fontsize=24, weight="bold", color=NAVY)
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.86, 0.86], color=ACCENT, lw=2.5))
    fig.text(0.94, 0.04, f"BAH 2026 · PS7 · TRINETRA   |   {n}", fontsize=8,
             color=GREY, ha="right")


def _bullets(fig, items, x=0.08, y0=0.76, dy=0.075, fs=14, wrap=120):
    for i, (txt, sub) in enumerate(items):
        yy = y0 - i * dy
        fig.text(x, yy, "•", fontsize=fs + 2, color=ACCENT, weight="bold")
        fig.text(x + 0.025, yy, "\n".join(textwrap.wrap(txt, wrap - 25)),
                 fontsize=fs, color="#111", weight="bold", va="top")
        if sub:
            fig.text(x + 0.025, yy - 0.032, "\n".join(textwrap.wrap(sub, wrap)),
                     fontsize=fs - 3.5, color=GREY, va="top", linespacing=1.3)


def _img(fig, path, rect):
    if not os.path.exists(path):
        fig.text(0.5, 0.5, f"[missing: {os.path.basename(path)}]", ha="center", color="red")
        return
    ax = fig.add_axes(rect); ax.imshow(mpimg.imread(path)); ax.axis("off")


def title_slide(fig):
    fig.patch.set_facecolor(NAVY)
    fig.text(0.5, 0.66, "TRINETRA", fontsize=58, weight="bold", color="white", ha="center")
    fig.text(0.5, 0.57, "Evidence-first, physics-grounded AI detection &\nclassification of exoplanet transits in noisy TESS light curves",
             fontsize=17, color="#cfe0f5", ha="center")
    fig.add_artist(plt.Line2D([0.3, 0.7], [0.50, 0.50], color=ACCENT, lw=2))
    fig.text(0.5, 0.42, "Bharatiya Antariksh Hackathon 2026 — Problem Statement 7", fontsize=15, color="white", ha="center")
    fig.text(0.5, 0.30, "Team Name:  TRINETRA-X", fontsize=15, color="#cfe0f5", ha="center")
    fig.text(0.5, 0.25, "Team Leader:  Ansul Suryawanshi", fontsize=13, color="#cfe0f5", ha="center")
    fig.text(0.5, 0.14, "AI-enabled Detection of Exoplanets from Noisy Astronomical Light Curves",
             fontsize=11, color="#9fb8d8", ha="center", style="italic")


def team_slide(fig):
    _header(fig, "Team", "2")
    rows = [("Team Leader", "Ansul Suryawanshi", "Indira Gandhi National Open University (IGNOU)"),
            ("Member 1", "Riddhi Jain", "Indira Gandhi National Open University (IGNOU)"),
            ("Member 2", "Samiksha Choudhary", "Priyadarshini College of Engineering (Hingna), Nagpur"),
            ("Member 3", "[optional — 4th member]", "team of 3 is valid (BAH allows 3–4)")]
    fig.text(0.08, 0.78, "Role", fontsize=13, weight="bold", color=ACCENT)
    fig.text(0.24, 0.78, "Name", fontsize=13, weight="bold", color=ACCENT)
    fig.text(0.52, 0.78, "College / Institution", fontsize=13, weight="bold", color=ACCENT)
    for i, (role, name, coll) in enumerate(rows):
        yy = 0.70 - i * 0.12
        last = i == len(rows) - 1
        fig.text(0.08, yy, role, fontsize=13, weight="bold", color="#111" if not last else GREY)
        fig.text(0.24, yy, name, fontsize=13, color=GREY)
        fig.text(0.52, yy, coll, fontsize=12, color=GREY)
    fig.text(0.08, 0.10, "Suggested roles: data/conditioning · ML/classifier · physics/parameter-fit · visualization/report",
             fontsize=10, color=GREY, style="italic")


def opportunity_slide(fig):
    _header(fig, "Opportunity", "3")
    _bullets(fig, [
        ("Different from existing ideas", "Most pipelines detect OR classify, often with uncalibrated scores. TRINETRA is evidence-first + physics-grounded, fusing interpretable physics features with a CNN, on a spine already benchmarked vs full TLS."),
        ("How it solves the problem", "Detect periodic dips → classify (transit/eclipse/blend/other) with explicit crowded-field/blend discriminators → attach SNR + calibrated confidence → fit period/depth/duration → visualize."),
        ("USP", "Hybrid physics+DL (interpretable, small-data robust); calibrated confidence by construction; physics decides detection (recall-prioritized); explicit blend handling; extends a validated, pre-registered spine."),
        ("Already demonstrated on fresh MAST data", "Pi Mensae c blindly recovered (P=6.262 d, 289 ppm, SDE 12.3); TIC 100029948 flagged as an eclipsing binary (depth ~25%, odd-even 0.23)."),
    ], dy=0.165, fs=14)


def features_slide(fig):
    _header(fig, "Features", "4")
    _bullets(fig, [
        ("Robust periodic-dip detection in noisy crowded fields", ""),
        ("4-class AI classification: transit / eclipse / blend / other", ""),
        ("SNR / significance per event", ""),
        ("Transit parameter fit: period, depth, duration (+ uncertainties)", ""),
        ("Calibrated confidence + annotated visualizations", ""),
        ("Reproducible; benchmarked vs full TLS", ""),
    ], x=0.06, y0=0.74, dy=0.085, fs=13, wrap=48)
    _img(fig, os.path.join(FIGS, "four_class_concept.png"), [0.50, 0.08, 0.46, 0.60])


def flow_slide(fig):
    _header(fig, "Process Flow — mirrors the PS7 5-step methodology", "5")
    steps = [("01 Detrend", "wotan biweight\n→ flat LC"),
             ("02 Identify", "dip detection +\nperiod, phase-fold"),
             ("03 Characterize", "trapezoid fit:\ndepth, dur,\ningress, flat-bottom"),
             ("04 Classify", "shape params →\ntransit/eclipse/\nblend/other"),
             ("05 Significance", "SNR + formal\nsignificance")]
    n = len(steps); x0, x1 = 0.07, 0.93; y = 0.55
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    for i, (x, (h, s)) in enumerate(zip(xs, steps)):
        fig.text(x, y + 0.06, h, fontsize=13, ha="center", va="center", color=NAVY, weight="bold")
        fig.text(x, y - 0.05, s, fontsize=10, ha="center", va="center", color="#111",
                 bbox=dict(boxstyle="round,pad=0.5", fc="#eaf2ff", ec=ACCENT, lw=1.3))
        if i < n - 1:
            fig.add_artist(plt.Line2D([x + 0.045, xs[i + 1] - 0.045], [y, y], color=GREY, lw=1.4))
    fig.text(0.5, 0.26, "Steps 01–02 reuse the validated TRINETRA-X spine (already benchmarked vs full TLS).",
             fontsize=12, ha="center", color=GREY)
    fig.text(0.5, 0.21, "Step 03 trapezoid shape-fit feeds Step 04 — the committee's stated approach:\n\"build the AI classifier on the transit shape parameters.\"",
             fontsize=12, ha="center", color=ACCENT, weight="bold")


def char_slide(fig):
    _header(fig, "Characterization & shape-based discrimination (step 03)", "6")
    _img(fig, os.path.join(PROTO_FIGS, "characterization.png"), [0.04, 0.20, 0.92, 0.62])
    fig.text(0.5, 0.13, "Depth is nearly identical for the EB and the planet — the TRAPEZOID SHAPE separates them:",
             fontsize=12, ha="center", color="#111")
    fig.text(0.5, 0.08, "EB flat-fraction 0.26 (V-shape, false positive)  vs  planet flat-fraction 0.67 (U-shape) — on real MAST data.",
             fontsize=12, ha="center", color=ACCENT, weight="bold")


def arch_slide(fig):
    _header(fig, "Architecture", "7")
    _img(fig, os.path.join(FIGS, "arch_diagram.png"), [0.06, 0.06, 0.88, 0.76])


def tech_slide(fig):
    _header(fig, "Technologies", "8")
    _bullets(fig, [
        ("Core scientific Python", "numpy · scipy · pandas · matplotlib"),
        ("Astronomy", "lightkurve · astropy · astroquery/MAST · wotan · transitleastsquares · batman"),
        ("Machine learning", "scikit-learn · XGBoost/LightGBM (physics branch) · PyTorch (CNN branch) · conformal (MAPIE)"),
        ("Method", "injection–recovery into real LCs · bootstrap FAP · conformal prediction · benchmark vs full TLS"),
        ("All open-source", "no specialized or licensed software; data is public (MAST)"),
    ], dy=0.135, fs=14)


def cost_slide(fig):
    _header(fig, "Estimated Implementation Cost", "9")
    _bullets(fig, [
        ("Software: ₹0", "entirely open-source stack"),
        ("Data: ₹0", "public TESS archive (MAST); one sector ~40–55 GB raw, kept slim by condition-then-discard"),
        ("Compute", "standard laptops for dev + a GPU session for CNN training; optional free cloud credits"),
        ("Net", "negligible cost — feasibility is high; the spine already runs on real data"),
    ], dy=0.135, fs=14)


def poc_slide(fig):
    _header(fig, "Proof of Concept — fresh MAST data (validated 2026-06-26)", "10")
    _img(fig, os.path.join(PROTO_FIGS, "eb_vs_planet.png"), [0.06, 0.30, 0.88, 0.50])
    fig.text(0.5, 0.20, "Left: TIC 100029948 — eclipsing binary flagged by physics features (depth ~25%, V-shape, odd–even 0.23).",
             fontsize=12, ha="center", color="#111")
    fig.text(0.5, 0.15, "Right: Pi Mensae c — blindly recovered (P=6.262 d vs lit. 6.268; depth 289 ppm vs lit. ~315; SDE 12.3).",
             fontsize=12, ha="center", color="#111")
    fig.text(0.5, 0.08, "The detection spine works end-to-end today; only the trained 4-class classifier remains to be built.",
             fontsize=12, ha="center", color=ACCENT, weight="bold")


def validation_slide(fig):
    _header(fig, "Validation on known objects (real labels)", "11")
    _img(fig, os.path.join(PROTO_FIGS, "validation_known.png"), [0.12, 0.17, 0.76, 0.62])
    fig.text(0.5, 0.11, "12 known objects — confirmed planets (fresh from MAST) + known eclipsing binaries. "
             "Clean transiters recovered with literature-matching periods.",
             fontsize=11.5, ha="center", color="#111")
    fig.text(0.5, 0.06, "Classes separate cleanly in depth × shape space — neither feature alone suffices → "
             "empirically justifies the multi-feature classifier.",
             fontsize=11.5, ha="center", color=ACCENT, weight="bold")


def main():
    slides = [title_slide, team_slide, opportunity_slide, features_slide,
              flow_slide, char_slide, arch_slide, tech_slide, cost_slide,
              poc_slide, validation_slide]
    with PdfPages(OUT) as pdf:
        for fn in slides:
            _page(pdf, fn)
    size_mb = os.path.getsize(OUT) / 1e6
    print(f"deck -> {OUT}  ({size_mb:.2f} MB, {len(slides)} slides)")


if __name__ == "__main__":
    main()
