# PS7 Idea-Submission Deck (official ISRO BAH 2026 template)

The organisers require their **official PowerPoint template** be used as-is. The deck
is therefore built by **populating that template** — never redesigning it. The
background art, theme, colours and slide size are the template's; we only fill content.

## Deliverables
- **`BAH2026_PS7_idea_deck.pptx`** — the official template, filled (primary submission file).
- **`BAH2026_PS7_idea_deck.pdf`** — a PDF export of that PPTX (≤5 MB, portal-friendly).

## Build
```bash
.venv/bin/python hackathon/deck/figures.py             # arch_diagram · four_class_concept · process_flow
.venv/bin/python hackathon/prototype/make_poc_fig.py   # eb_vs_planet (proof-of-concept)
.venv/bin/python hackathon/deck/build_pptx.py          # -> BAH2026_PS7_idea_deck.pptx (fills the template)
```
Export the PDF from PowerPoint / Google Slides (best font fidelity), or headless
LibreOffice: `soffice --headless --convert-to pdf --outdir . BAH2026_PS7_idea_deck.pptx`.

## Files
- `build_pptx.py` — opens `[Pub] ISRO BAH 2026 _ Idea Submission Template (2).pptx` and fills every
  section; adds two evidence slides (Proof-of-Concept, Validation) carrying the template's own
  content background so the look is identical.
- `figures.py` — `arch_diagram.png` (clean orthogonal connectors), `four_class_concept.png`,
  `process_flow.png` (PS7 five-step methodology).
- `build_deck.py` — **legacy** non-template matplotlib deck (writes `*_legacy.pdf`; kept for reference).

## Slide order (12)
1 Title · 2 Team · 3 Opportunity · 4 Features · 5 Process Flow · 6 Characterization ·
7 Architecture · 8 Technologies · 9 Estimated Cost · 10 Proof-of-Concept · 11 Validation · 12 Thank-You.

## Fixes applied (2026-07-01)
- **Features** — text overlap eliminated (native template text, not a crammed image).
- **Architecture** — flowchart rebuilt with clean orthogonal connectors; every arrow enters its box squarely.
- **Proof-of-Concept** — the Pi Mensae c curve is now fully inside the axes (robust y-limits + marker overlay).

## Before submitting (deadline 2026-07-01)
- [ ] Open the PPTX, glance through all 12 slides, tweak if desired.
- [ ] Upload `BAH2026_PS7_idea_deck.pdf` (or the PPTX, per the portal); select **PS7** in the dropdown.
