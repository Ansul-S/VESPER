# PS7 Idea-Submission Deck

The dashboard requires a **PDF deck (≤5 MB)**. We build it directly with matplotlib
(no LibreOffice/PowerPoint needed) so it's reproducible from source.

## Build
```bash
.venv/bin/python hackathon/deck/figures.py      # architecture + 4-class concept figures
.venv/bin/python hackathon/deck/build_deck.py   # -> BAH2026_PS7_idea_deck.pdf (9 slides, ~0.4 MB)
```

## Files
- `figures.py` — generates `figs/arch_diagram.png` and `figs/four_class_concept.png`.
- `build_deck.py` — assembles the PDF (title, team, opportunity, features, process flow,
  architecture, technologies, cost, proof-of-concept), embedding the prototype figures.
- `BAH2026_PS7_idea_deck.pdf` — the deliverable.

## Slide order (mirrors the official PPTX template)
1 Title · 2 Team · 3 Opportunity (different/solves/USP) · 4 Features · 5 Process flow ·
6 Architecture · 7 Technologies · 8 Cost · 9 Proof-of-concept (fresh MAST validation).

## TODO before submitting (deadline 2026-07-01)
- [ ] Fill **team name, leader, 3 members + colleges** (placeholders on slides 1–2),
      then re-run `build_deck.py`.
- [ ] Paste the Part-A web-form fields from `../BAH2026_PS7_PROPOSAL_DRAFT.md`.
- [ ] Upload the PDF on the dashboard; select PS7 in the Challenge dropdown.
