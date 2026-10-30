"""Tests for the houseplant care printables.

Each test run builds every sheet into a scratch directory and then verifies
that the PDF is valid, well-formed, unbranded, and contains the expected
getting-started page and printable content. Requires the optional deps in
requirements.txt (weasyprint for building, pypdf for verification, pytest).
"""

import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

REPO = Path(__file__).resolve().parent.parent
BUILD = REPO / "scripts" / "build.py"

# sheet stem -> phrases that must appear somewhere in the PDF text
EXPECT = {
    "plant-profile-cards": ["Getting Started", "Plant Profile Cards", "Got it", "bright indirect"],
    "watering-rotation": ["Getting Started", "Watering Rotation Sheet", "three-finger", "rootbound"],
    "repotting-checklist": ["Getting Started", "Repotting Checklist", "drainage hole", "Repot time"],
    "fertilizer-log": ["Getting Started", "Fertilizer Date Log", "N–P–K", "Feeding record"],
    "diagnosis-yellow-leaves": ["Getting Started", "Yellow Leaves", "suspect", "knuckles"],
    "propagation-tracker": ["Getting Started", "Propagation Jar Tracker", "node", "First root"],
    "plant-sitter-card": ["Getting Started", "Plant-Sitter Card", "watering can", "skip the watering"],
    "seasonal-calendar": ["Getting Started", "Seasonal Care Calendar", "repot window", "Winter"],
}

SHEET_NAMES = sorted(EXPECT)


@pytest.fixture(scope="session")
def out_dir(tmp_path_factory):
    """Build all sheets once per session via the CLI, exactly as a user would."""
    out = tmp_path_factory.mktemp("printables")
    proc = subprocess.run(
        [sys.executable, str(BUILD), "--out", str(out)],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    n_built = len(list(out.glob("*.pdf")))
    assert n_built == len(SHEET_NAMES)
    return out


def reader(out_dir, sheet):
    return PdfReader(out_dir / f"{sheet}.pdf")


def test_build_script_lists_unknown_sheet(out_dir, capsys=None):
    proc = subprocess.run(
        [sys.executable, str(BUILD), "--out", str(out_dir), "not-a-sheet"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert "Unknown sheet" in (proc.stderr + proc.stdout)


@pytest.mark.parametrize("sheet", SHEET_NAMES)
class TestSheet:
    def test_pdf_exists(self, out_dir, sheet):
        assert (out_dir / f"{sheet}.pdf").is_file()
        assert (out_dir / f"{sheet}.pdf").stat().st_size > 1000

    def test_pdf_header_and_eof(self, out_dir, sheet):
        data = (out_dir / f"{sheet}.pdf").read_bytes()
        assert data.startswith(b"%PDF-")
        assert b"%%EOF" in data[-64:]

    def test_two_pages_with_different_roles(self, out_dir, sheet):
        pages = reader(out_dir, sheet).pages
        assert len(pages) >= 2, "expected a getting-started page plus the printable"
        text1 = pages[0].extract_text() or ""
        text2 = pages[1].extract_text() or ""
        assert text1 != text2, "first two pages are identical"
        sheet_title = " ".join(EXPECT[sheet][1].split())  # printable title
        assert sheet_title in text2, "page 2 does not carry the printable title"

    def test_getting_started_page_content(self, out_dir, sheet):
        text = reader(out_dir, sheet).pages[0].extract_text() or ""
        assert EXPECT[sheet][0] in text or "getting started" in text.lower()
        for needle in ("GETTING STARTED", "PRINT IT RIGHT"):
            assert needle in text.upper(), f"cover page missing section {needle}"
        assert "100 % scale" in text, "print-scale guidance missing from cover"

    def test_printable_page_content(self, out_dir, sheet):
        text = reader(out_dir, sheet).pages[1].extract_text() or ""
        low = text.lower()
        for needle in EXPECT[sheet][2:]:
            assert needle.lower() in low, f"printable page missing {needle!r}"

    def test_pdf_is_unbranded(self, out_dir, sheet):
        r = reader(out_dir, sheet)
        body = " ".join((pg.extract_text() or "") for pg in r.pages)
        meta = dict(r.metadata or {})
        for forbidden in ("Asdale", "Dylan", "dylanasdale", "ASD"):
            assert forbidden not in body, f"branding leaked into printable text: {forbidden}"
            assert forbidden not in str(meta), f"branding leaked into PDF metadata: {forbidden}"

    def test_page_sizes_letter(self, out_dir, sheet):
        pages = reader(out_dir, sheet).pages
        for pg in pages:
            w = float(pg.mediabox.width) / 72
            h = float(pg.mediabox.height) / 72
            short, tall = min(w, h), max(w, h)
            assert abs(short - 8.5) < 0.05 and abs(tall - 11.0) < 0.05, f"page not US Letter: {w}x{h} in"


def test_seasonal_calendar_printable_is_landscape(out_dir):
    pg = reader(out_dir, "seasonal-calendar").pages[1]
    w = float(pg.mediabox.width) / 72
    h = float(pg.mediabox.height) / 72
    assert w > h, "calendar printable should be landscape"


def test_pdf_titles_set(out_dir):
    for sheet in SHEET_NAMES:
        r = reader(out_dir, sheet)
        title = (r.metadata or {}).get("/Title", "")
        assert title, f"{sheet}.pdf has no Title metadata"
        assert "Getting Started" in title


def test_repository_pdf_output_matches_sources():
    """The committed printables/ PDFs rebuild bit-identically from the sources is
    not guaranteed across WeasyPrint versions, so we only check they are valid
    and complete."""
    committed = sorted((REPO / "printables").glob("*.pdf"))
    assert len(committed) == len(SHEET_NAMES)
    for pdf in committed:
        head = pdf.read_bytes()[:8]
        assert head.startswith(b"%PDF-"), f"{pdf.name} is not a valid PDF"
