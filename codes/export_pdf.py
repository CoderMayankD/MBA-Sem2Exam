#!/usr/bin/env python3
"""Export Markdown notes to PDF. Pure-Python (markdown + xhtml2pdf), no system dependencies.

Usage: ../.venv/bin/python3 export_pdf.py "Managerial Accounting"
"""

import re
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from xhtml2pdf import pisa

from lib.common import REPO_ROOT, subject_dir

DEJAVU_DIR = "/usr/share/fonts/truetype/dejavu"

# DejaVu Sans, not the default Helvetica, because Helvetica has no glyph for the Rupee sign
# (confirmed: ₹ rendered as a black missing-glyph box in a real PDF) — DejaVu covers it.
FONT_FACES = (
    "@font-face { font-family: DejaVuSans; src: url(" + DEJAVU_DIR + "/DejaVuSans.ttf); }\n"
    "@font-face { font-family: DejaVuSans; font-weight: bold; src: url(" + DEJAVU_DIR + "/DejaVuSans-Bold.ttf); }\n"
)

CSS = FONT_FACES + """
body { font-family: DejaVuSans; font-size: 10pt; line-height: 1.4; }
h1 { font-size: 18pt; margin-bottom: 4pt; }
.meta { color: #555; font-size: 9pt; margin-bottom: 14pt; border-bottom: 0.5pt solid #ccc; padding-bottom: 8pt; }
h2 { font-size: 13pt; margin-top: 16pt; border-bottom: 0.5pt solid #ccc; }
h3 { font-size: 11pt; margin-top: 10pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; }
td, th { border: 0.5pt solid #888; padding: 3pt 5pt; font-size: 7.5pt; word-wrap: break-word; overflow-wrap: break-word; vertical-align: top; }
code { background: #f2f2f2; }
"""


def _equalize_table_columns(html_body: str) -> str:
    """xhtml2pdf ignores CSS `table-layout: fixed` AND a <colgroup> with width styles (both
    confirmed by direct visual test against a real rendered PDF — a long-text column just keeps
    hogging the width regardless). What it does respect is an explicit `width` percentage on
    every cell of the table. Set that on every <th>/<td>, not just the header row, since
    xhtml2pdf's layout pass reads per-cell widths rather than a single column definition."""
    soup = BeautifulSoup(html_body, "html.parser")
    for table in soup.find_all("table"):
        header_row = table.find("tr")
        if not header_row:
            continue
        n_cols = len(header_row.find_all(["th", "td"]))
        if n_cols == 0:
            continue
        width_pct = f"{100 / n_cols:.2f}%"
        for row in table.find_all("tr"):
            for cell in row.find_all(["th", "td"]):
                cell["width"] = width_pct
    return str(soup)


def _fix_missing_blank_lines_before_tables(text: str) -> str:
    """python-markdown's `tables` extension silently refuses to render a table (falls back to
    plain text with literal pipe characters) unless it's preceded by a blank line. The notes
    generator sometimes emits a table right after a bold label line with no blank line between
    — confirmed in several real notes files. Insert the missing blank line mechanically rather
    than regenerating notes (which would cost real LLM time for a pure formatting fix)."""
    lines = text.split("\n")
    fixed = []
    for i, line in enumerate(lines):
        is_table_row = line.startswith("|")
        prev_is_blank_or_table = i == 0 or lines[i - 1].strip() == "" or lines[i - 1].startswith("|")
        if is_table_row and not prev_is_blank_or_table:
            fixed.append("")
        fixed.append(line)
    return "\n".join(fixed)


def md_to_pdf(md_path: Path, pdf_path: Path) -> bool:
    text = md_path.read_text()
    text = _fix_missing_blank_lines_before_tables(text)

    meta_line = ""
    fm_match = re.match(r"^---\n(.*?)\n---\n\n?", text, re.DOTALL)
    if fm_match:
        fm = dict(
            line.split(":", 1) for line in fm_match.group(1).splitlines() if ":" in line
        )
        fm = {k.strip(): v.strip() for k, v in fm.items()}
        meta_line = (
            f"{fm.get('subject', '')} &middot; "
            f"{fm.get('duration_minutes', '?')} min &middot; processed {fm.get('processed_on', '')}"
        )
        text = text[fm_match.end():]

    html_body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html_body = _equalize_table_columns(html_body)
    html = f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
    if meta_line:
        html += f'<div class="meta">{meta_line}</div>'
    html += f"{html_body}</body></html>"

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pdf_path, "wb") as f:
        result = pisa.CreatePDF(html, dest=f)
    return not result.err


def main():
    if len(sys.argv) < 2:
        print("Usage: export_pdf.py <Subject name>")
        sys.exit(1)
    subject = sys.argv[1]
    s_dir = subject_dir(subject)
    n_dir = s_dir / "Notes"

    targets = sorted(n_dir.glob("*.md"))
    practice = s_dir / "Practice-Questions.md"
    if practice.exists():
        targets.append(practice)

    print(f"Exporting {len(targets)} file(s) to PDF...")
    for md_path in targets:
        pdf_path = md_path.with_suffix(".pdf")
        ok = md_to_pdf(md_path, pdf_path)
        status = "ok" if ok else "ERRORS"
        print(f"  {pdf_path.relative_to(REPO_ROOT)} [{status}]")


if __name__ == "__main__":
    main()
