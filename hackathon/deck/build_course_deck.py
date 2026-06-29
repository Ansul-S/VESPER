"""Build the TRINETRA-X teaching-deck PDF (26 slides) from the course material.

Data-driven: each slide is a dict (title, bullets, optional image, optional note).
Matches hackathon/course/06_SPEAKER_NOTES.md slide-for-slide. matplotlib only.

Run:  .venv/bin/python hackathon/deck/build_course_deck.py
Out:  hackathon/deck/TRINETRA_X_course.pdf
"""
from __future__ import annotations
import os, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.image as mpimg

HERE = os.path.dirname(__file__)
FIGS = os.path.join(HERE, "figs")
PFIGS = os.path.join(HERE, "..", "prototype", "figs")
OUT = os.path.join(HERE, "TRINETRA_X_course.pdf")
NAVY, ACCENT, GREY, RED, GREEN = "#13294b", "#2c6fbb", "#444444", "#c0392b", "#1e8449"
W, H = 13.33, 7.5


def header(fig, title, n):
    fig.text(0.06, 0.905, title, fontsize=21, weight="bold", color=NAVY, wrap=True)
    fig.add_artist(plt.Line2D([0.06, 0.94], [0.862, 0.862], color=ACCENT, lw=2.2))
    fig.text(0.94, 0.035, f"TRINETRA-X · course · {n}/26", fontsize=8, color=GREY, ha="right")


def bullets(fig, items, x=0.07, y0=0.78, dy=0.092, fs=14, wrap=92, color="#111"):
    for i, it in enumerate(items):
        yy = y0 - i * dy
        fig.text(x, yy, "•", fontsize=fs + 2, color=ACCENT, weight="bold")
        fig.text(x + 0.022, yy, "\n".join(textwrap.wrap(it, wrap)),
                 fontsize=fs, color=color, va="top", linespacing=1.25)


def img(fig, path, rect):
    if os.path.exists(path):
        ax = fig.add_axes(rect); ax.imshow(mpimg.imread(path)); ax.axis("off")
    else:
        fig.text(0.5, 0.45, f"[missing {os.path.basename(path)}]", ha="center", color="red")


def note(fig, text, y=0.08, color=ACCENT):
    fig.text(0.5, y, text, ha="center", fontsize=12.5, color=color, weight="bold",
             wrap=True)


def title_slide(fig):
    fig.patch.set_facecolor(NAVY)
    fig.text(0.5, 0.62, "TRINETRA-X", fontsize=60, weight="bold", color="white", ha="center")
    fig.text(0.5, 0.52, "Finding planets in starlight — and being honest about it",
             fontsize=18, color="#cfe0f5", ha="center")
    fig.add_artist(plt.Line2D([0.28, 0.72], [0.46, 0.46], color=ACCENT, lw=2))
    fig.text(0.5, 0.38, "A complete course: from \"what is a star?\" to defending it at ISRO",
             fontsize=14, color="white", ha="center")
    fig.text(0.5, 0.27, "Team TRINETRA-X · BAH 2026 · Problem Statement 7", fontsize=13, color="#9fb8d8", ha="center")
    fig.text(0.94, 0.035, "course · 1/26", fontsize=8, color="#9fb8d8", ha="right")


# ---- slide specifications (S2..S26) ----
SLIDES = [
    ("The big question", ["Until 1995 we knew one planetary system. Now: ~6,000 exoplanets.",
        "Core questions: Are we alone? How common are Earth-like worlds? How do planets form?",
        "We are the first generation that can answer this with data."], None, None),
    ("The needle in a cosmic haystack", ["A star is blinding; a planet is a tiny dark speck — we detect its EFFECT, not the planet.",
        "An Earth dims the Sun by only ~84 parts per million.",
        "Analogy: hearing one whisper in a stadium of 50,000 fans."], None,
        "It's contrast, not telescope size — indirect methods sidestep the wall."),
    ("Four ways to find a planet", ["Radial velocity — the star wobbles.   Transit — the star dims  (← ours).",
        "Direct imaging — rare, big planets.   Microlensing/astrometry — gravity/position.",
        "Transit dominates: one camera monitors 10,000-100,000 stars at once."], None, None),
    ("The hidden enemy: computation", ["You don't know the period → you must try thousands per star.",
        "Cost ~ (trial periods) x (data points) x (millions of stars).",
        "Most stars are EMPTY, yet blind search pays full price on every one.",
        "Analogy: a million locked doors, trying every key on each."], None, None),
    ("Light curves & transits", ["Light curve = brightness vs time (a star's EKG).",
        "A planet crossing makes a small, repeating dip.",
        "Depth = (Rp/Rstar)^2  -> the planet-to-star size ratio."], None,
        "Bug crossing a flashlight beam: dims a hair, then returns — on a schedule."),
    ("Dips have impostors — the U vs V tell", ["A dip can be: planet / eclipsing binary / blend / junk (spots, systematics).",
        "Planet = rounded U (flat bottom). EB = pointy V, often + secondary dip + odd-even.",
        "THE KEYSTONE: depth alone can't tell them apart — SHAPE can."], None,
        "Same symptom (a cough), different disease — you need more features to diagnose."),
    ("Depth, spacing, period", ["Depth -> size.  Spacing -> orbital period.  Repetition -> reality.",
        "One dip could be a glitch; three evenly-spaced identical dips = a planet.",
        "Monotransits (one dip) are ambiguous -> out of Phase-I scope."], None, None),
    ("The incumbents: BLS & TLS", ["BLS fits a box (fast, crude). TLS fits the real transit shape (sensitive, slow).",
        "TLS outputs SDE and is our gold-standard benchmark.",
        "Landmine: TLS's SDE is normalized over the grid you search (remember this!)."], None, None),
    ("Birth of TRINETRA-X", ["Blind TLS treats empty & promising stars identically.",
        "Idea: spend cheap effort to find EVIDENCE; spend expensive effort only where it exists.",
        "TRINETRA = 'third eye' — seeing what brute force misses."], None,
        "Airport: metal-detector first; full search only on the people who beep."),
    ("The prime directive", ["Find evidence first. Spend computation second. Let physics decide.",
        "Recall > precision: a false alarm is OK; a MISSED planet is not.",
        "Physics (depth/shape/repetition), not timing luck, is the arbiter."], None,
        "Cancer screen: never miss the tumor, tolerate false alarms."),
    ("The hypothesis (pre-registered)", ["H1: routing cuts compute vs TLS WITHOUT losing recall.  H0: it doesn't.",
        "E1 = recall non-inferiority (lose no planets).  E2 = compute reduction >= 30%.",
        "Frozen BEFORE touching test data — that's what makes the answer trustworthy."], None, None),
    ("Architecture", ["Condition -> detect events -> period from spacing -> bootstrap FAP -> Lambda confirmer -> TLS fallback.",
        "Savings come from folding k EVENTS, not searching N points x a period grid."],
        os.path.join(FIGS, "arch_diagram.png"), None),
    ("Module deep-dive", ["Detector: cheap box matched filter, SNR = depth / scatter.",
        "Period-from-spacing: read P off event spacing (Rayleigh Z = k R^2).",
        "Bootstrap FAP: is the periodicity real or lucky noise? (block bootstrap).",
        "Confirmer: likelihood ratio Lambda = the PHYSICS arbiter.  Fallback: if unsure, full TLS."], None, None),
    ("Five math anchors", ["1) delta = (Rp/Rstar)^2  — depth <-> size",
        "2) SNR1 = delta / CDPP  — detectability",
        "3) FAP = (1/B) sum 1[T_b >= T_obs]  — honesty/calibration",
        "4) Lambda = -2 ln[L(flat)/L(transit)]  — the judge",
        "5) saving ~ f ,  recall loss = -f(1 - r_seed g)  — the whole bet"], None, None),
    ("The research journey", ["Idea -> build & calibrate (M0-M3, sealed) -> CRISIS: Finding B.",
        "Finding B: TLS SDE is grid-normalized -> 'targeted TLS' design is invalid.",
        "Repair: v3 -> Lambda confirmer at a COMMON false-alarm rate (re-registered openly).",
        "Tried to cheapen the bootstrap; an equivalence test said no -> kept it."], None,
        "We caught a flaw in our own case BEFORE the verdict and fixed it in the open."),
    ("The verdict (read once)", ["TEST read exactly once; verdict pre-committed.",
        "E1 PASS: recall preserved (delta-recall -0.48 pp).",
        "E2 FAIL: compute reduction 24.4% < 30%.",
        "=> H1 falsified on the compute branch — a SUCCESSFUL negative result."],
        os.path.join(PFIGS, "eb_vs_planet.png"), None),
    ("Why it failed + the scaling insight", ["Killer: un-cheapenable B=1000 bootstrap 'entry tax' (rho_d~14.4%) + fallbacks.",
        "Theory: break-even prevalence pi* = rho_d / f_p -> short baselines can't win.",
        "Insight: fast lane folds k events while TLS cost grows with baseline.",
        "=> the advantage should GROW with search-space size -> test on Kepler."], None,
        "A shortcut that only pays off on a long highway, not a short street."),
    ("Milestones M0-M7", ["M0 sealed dataset + leak-safe split.  M1 conditioning.  M2 chose 2.5-d window by injection.",
        "M3 calibrated thresholds (+ cleaned EB-contaminated null pool).",
        "M4 the single sealed test (the verdict).",
        "M5-M7 characterization + reality check (real TOIs: Arm B = Arm A = 86.7%) + manuscript."], None, None),
    ("The hackathon pivot (PS7)", ["Same validated spine, new mission: CLASSIFY dips for ISRO PS7.",
        "5 steps: detrend -> identify -> characterize -> classify -> significance.",
        "Committee's key point = our keystone: depth doesn't separate planet from FP; shape does."],
        os.path.join(FIGS, "four_class_concept.png"), None),
    ("Characterization: U vs V (real data)", ["Trapezoid fit reproduces the committee's slide-5/6 parameters.",
        "EB (TIC 100029948): flat-fraction 0.26 -> V (false positive).",
        "Pi Mensae c: flat-fraction 0.67 -> U (planet). Depth nearly equal; SHAPE decides."],
        os.path.join(PFIGS, "characterization.png"), None),
    ("Classification + validation", ["Physics features -> gradient-boosted classifier, conformal-calibrated confidence.",
        "Validated on 12 known objects: planets U + literature periods; EBs V.",
        "Single feature = 0.58, but classes separate in 2-D depth x shape -> multi-feature justified."],
        os.path.join(PFIGS, "validation_known.png"), None),
    ("Current status + roadmap", ["Phase I sealed/final (no v4). Round-1 package complete (submit by 2026-07-01).",
        "Round 2: robust period recovery, pixel-level centroid for blends, CNN ensemble, full report.",
        "Research future: Kepler scaling experiment.",
        "Named risk: period recovery on active/short-period stars."], None, None),
    ("The story in one slide", ["Humanity learns to hear planets by watching stars blink.",
        "The gold-standard detective interrogates everyone; a 'third eye' glances first.",
        "A hidden statistical trap nearly fakes a failure; we catch & fix it openly.",
        "One honest look: 'planets kept, savings missed' -> a bigger stage (Kepler)."], None,
        "Failure with a lesson is how science moves forward."),
    ("Pitch ladder", ["Practice 7 lengths: 30s / 1m / 3m / 5m / 10m / 15m / 30m.",
        "Default for judges: the 2-minute judge script.",
        "Always open with the honesty spine; always close on the forward path."], None, None),
    ("Master summary — why it matters", ["One hypothesis, one architecture, one honest verdict, one forward path.",
        "Rare: a project with the integrity to falsify its own headline while proving its core works.",
        "It produced BOTH a future experiment (Kepler scaling) AND a working tool (PS7 pipeline)."], None,
        "Intuition + mathematics + honesty — that's what makes you the expert on your own work."),
]


def render_slide(idx):
    """Build one slide figure. idx=1 is the title slide; idx 2..26 map to SLIDES."""
    fig = plt.figure(figsize=(W, H))
    if idx == 1:
        title_slide(fig)
        return fig
    title, blts, image, footnote = SLIDES[idx - 2]
    fig.patch.set_facecolor("white")
    header(fig, title, idx)
    if image:
        bullets(fig, blts, y0=0.80, dy=0.075, fs=12.5, wrap=120)
        img(fig, image, [0.16, 0.10, 0.68, 0.46])
    else:
        bullets(fig, blts)
    if footnote:
        note(fig, footnote)
    return fig


N_SLIDES = 1 + len(SLIDES)


def build_pdf():
    with PdfPages(OUT) as pdf:
        for i in range(1, N_SLIDES + 1):
            fig = render_slide(i); pdf.savefig(fig); plt.close(fig)
    mb = os.path.getsize(OUT) / 1e6
    print(f"course deck -> {OUT}  ({mb:.2f} MB, {N_SLIDES} slides)")


def build_pngs(dpi=150):
    out_dir = os.path.join(HERE, "figs_course")
    os.makedirs(out_dir, exist_ok=True)
    for i in range(1, N_SLIDES + 1):
        fig = render_slide(i)
        p = os.path.join(out_dir, f"slide_{i:02d}.png")
        fig.savefig(p, dpi=dpi); plt.close(fig)
    print(f"{N_SLIDES} slide PNGs -> {out_dir}/slide_01..{N_SLIDES:02d}.png  (dpi={dpi})")


def main():
    import sys
    if "--png" in sys.argv:
        build_pngs()
    else:
        build_pdf()


if __name__ == "__main__":
    main()
