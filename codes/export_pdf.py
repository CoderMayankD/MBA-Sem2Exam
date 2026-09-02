#!/usr/bin/env python3
"""Export Markdown notes to PDF. Pure-Python (markdown + xhtml2pdf), no system dependencies.

Usage: ../.venv/bin/python3 export_pdf.py "Managerial Accounting"
"""

import re
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

from lib.common import REPO_ROOT, subject_dir

CSS = """
body { font-family: Helvetica; font-size: 10pt; line-height: 1.4; }
h1 { font-size: 18pt; margin-bottom: 4pt; }
.meta { color: #555; font-size: 9pt; margin-bottom: 14pt; border-bottom: 0.5pt solid #ccc; padding-bottom: 8pt; }
h2 { font-size: 13pt; margin-top: 16pt; border-bottom: 0.5pt solid #ccc; }
h3 { font-size: 11pt; margin-top: 10pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; }
td, th { border: 0.5pt solid #888; padding: 3pt 5pt; font-size: 8pt; }
code { background: #f2f2f2; }
"""


def md_to_pdf(md_path: Path, pdf_path: Path) -> bool:
    text = md_path.read_text()

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
