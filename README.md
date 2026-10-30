# Houseplant Helper Printables

Free printable PDFs for keeping the greenery alive: plain-English, fill-by-hand
sheets for real plant parents. Build everything locally from HTML/CSS with one
script — no accounts, no signups, no tracking, no internet needed.

Maintained by **Asdale Dynamics, LLC**. Built in the friendly, step-by-step
style of Dylan Asdale's beginner AI guides: plain English, never condescending.

## What's inside (`printables/`)

Every PDF has two pages: a warm getting-started page (what it's for, how to
print it, one good tip) and the printable itself. The printables themselves
are unbranded — just the tool.

| Sheet | Use it for |
| --- | --- |
| `plant-profile-cards.pdf` | A profile card for each plant: light level, watering rhythm, got-it date, notes |
| `watering-rotation.pdf` | A monthly watering rotation so every plant gets its day |
| `repotting-checklist.pdf` | Before / during / after checkboxes for a calm repotting day |
| `fertilizer-log.pdf` | A feeding record with an N–P–K primer and feed windows |
| `diagnosis-yellow-leaves.pdf` | A yellow-leaves worksheet: patterns, soil test, suspect list, plan |
| `propagation-tracker.pdf` | Ten numbered jars and their water-change, root, and pot-up dates |
| `plant-sitter-card.pdf` | One-page instructions for a vacation plant-sitter |
| `seasonal-calendar.pdf` | The whole year in four panels (landscape strip) |

Companion to a houseplant-care **web** tracker if you like screens — these are
for the counter, the fridge, and the watering-can drawer.

## Build it yourself

Requires Python 3.9+ and the packages in `requirements.txt`:

```bash
python3 -m pip install -r requirements.txt   # weasyprint (+ pypdf for checks)
python3 scripts/build.py                     # build every sheet into printables/
python3 scripts/build.py watering-rotation   # rebuild a single sheet
python3 scripts/build.py --out /tmp/pdfs     # build somewhere else
```

Sources live in `src/sheets/*.html` (one file per sheet) with shared print
styles in `src/style.css`. Output filenames come from the sheet filenames.

## Print tips (also on every getting-started page)

- US Letter paper. All sheets except the seasonal calendar strip are portrait;
  the calendar strip is landscape.
- Print at **100 % scale** (“Actual size”) so the writing lines stay where they
  were designed to be.
- Card stock or a plastic sleeve makes sheets sturdy enough to live next to the pot.

## Tests

The test suite builds every sheet into a scratch directory and verifies each
PDF: valid header/EOF, a getting-started page plus a printable page, expected
content on both, US Letter page size, set titles, and no branding anywhere:

```bash
python3 -m pip install pytest pypdf
python3 -m pytest tests/ -v
```

## Contribute

Edit or add `src/sheets/<your-sheet>.html` (copy an existing one for the
getting-started structure), then rebuild. Keep new printables unbranded and
printer-friendly.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Asdale Dynamics, LLC.
