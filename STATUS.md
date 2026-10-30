# STATUS — Houseplant Helper Printables

Last updated: 2026-10-30

## What was built

A complete, local-first printable pack for beginner houseplant care: eight
HTML/CSS sheet sources that a single build script renders into unbranded,
print-ready US Letter PDFs. Every PDF ships two pages: page 1 is a warm
getting-started page (what the sheet is for, how to print it at 100 % scale,
one practical tip in a terracotta callout), page 2 is the printable itself.

Sheets in `printables/` (all unbranded — no branding, names, or contact info
inside the printables):

1. `plant-profile-cards.pdf` — eight cut-apart profile cards (name, got-it
   date, light level to circle, watering interval, last watered/fed/repotted)
2. `watering-rotation.pdf` — monthly rotation table for 16 plants with the
   three-finger soil rule and a group-rhythm box
3. `repotting-checklist.pdf` — before/during/after checkboxes, sure-signs box,
   session notes
4. `fertilizer-log.pdf` — 16-row feeding record with an N–P–K plain-words
   primer and feed-window rules
5. `diagnosis-yellow-leaves.pdf` — a case worksheet: pattern checklist, soil
   finger test, suspect line-up table, verdict/action plan
6. `propagation-tracker.pdf` — ten numbered jars with water-change ticks,
   first-root date, pot-up date, and best-first-tries tips
7. `plant-sitter-card.pdf` — one-page sitter instructions with an 8-plant crew
   table and the golden rule ("when in doubt, skip the watering")
8. `seasonal-calendar.pdf` — landscape four-panel year strip (spring/summer/
   fall/winter) with "my dates" lines

Supporting pieces: `scripts/build.py` (CLI: all sheets, single-sheet filter,
custom `--out`), `src/style.css` (shared WeasyPrint print stylesheet: US
Letter pages, cover and landscape named pages, table/checkbox/line styles),
`tests/test_build.py`, `README.md`, MIT `LICENSE`, `requirements.txt`.

No secrets, API keys, personal data, or signups anywhere; nothing is fetched
over the network during build or tests.

## How to run it

```bash
python3 -m pip install -r requirements.txt   # weasyprint; pypdf+pytest for checks
python3 scripts/build.py                     # build all 8 PDFs into printables/
python3 scripts/build.py watering-rotation   # rebuild one sheet
python3 scripts/build.py --out /tmp/pdfs     # build elsewhere
python3 -m pytest tests/                     # verify everything
```

## Verification results

- `python3 scripts/build.py` — builds all 8 sheets cleanly, no warnings/errors.
- `python3 -m pytest tests/` — **60 passed**: for every sheet the suite checks
  a valid PDF header + EOF marker, a distinct getting-started page and
  printable page with expected content on both, US Letter page size
  (landscape for the calendar strip), PDF Title metadata ("… — Getting
  Started"), >1 KB file size, and that no branding appears in page text or
  metadata. Also verifies a bogus sheet name fails the CLI cleanly.
- Visual check via `pdftoppm`: cover pages, card grid, and all printables
  render as designed at 100 % scale on Letter; no sheet's printable content
  overflows past page 2.

## Known gaps / notes

- The pack is US Letter only; A4 users must scale prints slightly (~97 %) or
  add an A4 `@page` rule in `src/style.css`.
- The seasonal calendar uses northern-hemisphere season defaults; southern
  hemisphere users can re-map the month labels in
  `src/sheets/seasonal-calendar.html`.
- Tests assert PDF *validity and content*, not pixel-perfect layout; a layout
  regression could still pass assuming page counts are unchanged (the two-page
  minimum does guard against a printable overflowing its page).
- Only WeasyPrint 70.x is tested as the render engine; other engines
  (wkhtmltopdf, Chrome headless) may render slightly differently.
- Walkthrough docs beyond README/STATUS (e.g. screenshots in the repo) are not
  included to keep the pack lean.
