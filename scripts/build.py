#!/usr/bin/env python3
"""Build the printable PDFs from the HTML/CSS sources.

Usage:
    python3 scripts/build.py                 # build every sheet into printables/
    python3 scripts/build.py --out /tmp/pdfs # build somewhere else
    python3 scripts/build.py watering-rotation fertilizer-log  # only these sheets

Each sheet in src/sheets/*.html is rendered with its stylesheet into
printables/<name>.pdf. Page 1 of every PDF is a warm getting-started page;
page 2 is the printable itself. No signups, no network, fully local.

Requires: weasyprint (see requirements.txt)
"""

import argparse
import logging
import sys
from pathlib import Path

from weasyprint import HTML

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
SHEETS_DIR = SRC / "sheets"
DEFAULT_OUT = ROOT / "printables"


def discover_sheets(only=()):
    """Return sorted (stem, path) pairs for the sheet sources."""
    sources = sorted(SHEETS_DIR.glob("*.html"))
    if not sources:
        logging.error("No sheet HTML sources found in %s", SHEETS_DIR)
        return []
    if only:
        wanted = {o.lower() for o in only}
        sources = [s for s in sources if s.stem.lower() in wanted]
        missing = wanted - {s.stem.lower() for s in sources}
        for name in sorted(missing):
            logging.error("Unknown sheet: %s", name)
    return [(s.stem, s) for s in sources]


def build_sheet(stem, path, out_dir):
    """Render one HTML sheet to <out_dir>/<stem>.pdf and return the PDF path."""
    target = out_dir / f"{stem}.pdf"
    document = HTML(filename=str(path), base_url=str(SRC))
    document.write_pdf(str(target))
    return target


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build the houseplant care printables."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Output directory for PDFs (default: printables/)",
    )
    parser.add_argument(
        "sheets",
        nargs="*",
        help="Optional list of sheet names to build (default: all)",
    )
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

    out_dir = args.out if args.out.is_absolute() else (ROOT / args.out).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    sheets = discover_sheets(args.sheets)
    if not sheets:
        logging.error("Nothing to build.")
        return 1

    failures = 0
    for stem, path in sheets:
        try:
            pdf = build_sheet(stem, path, out_dir)
            print(f"built {pdf.name}")
        except Exception as exc:  # noqa: BLE001 - report and keep building
            failures += 1
            logging.error("Failed to build %s: %s", stem, exc)

    if failures:
        print(f"{failures} sheet(s) failed.", file=sys.stderr)
        return 1
    print(f"Done: {len(sheets)} PDF(s) in {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
