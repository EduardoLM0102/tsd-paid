#!/usr/bin/env python3
"""
Builds the Spencer Air 2027 marketing plan/calendar: markdown -> plain HTML -> PDF.

The .md is the source of truth. HTML and PDF are artifacts — never edit them by hand.
Plain Word-style look (Times New Roman, black on white), per the TSD internal/production
doc convention — not the navy/gold client-report template. Mirrors
clients/gc-home-service/build_calendar_pdf.py.

Usage:
    python3 build_calendar_pdf.py

Requires: `pip install markdown` and Playwright with the Chromium browser installed.
"""
import pathlib
import markdown
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
SRC = HERE / "marketing-calendar-2027.md"
OUT = "Spencer-Air-Marketing-Calendar-2027"

TITLE = "Spencer Air &mdash; 2027 Marketing Plan &amp; Forward Calendar (Internal)"

CSS = """
@page { size: Letter; margin: 0.85in 1in; }
* { box-sizing: border-box; }
body { font-family: 'Times New Roman', Times, serif; color: #000; font-size: 12pt;
       line-height: 1.3; margin: 0; }
h1 { font-size: 16pt; margin: 0 0 4px; font-weight: 700; }
h2 { font-size: 13.5pt; margin: 18px 0 6px; font-weight: 700; page-break-after: avoid; }
h3 { font-size: 12pt; margin: 12px 0 4px; font-weight: 700; font-style: italic;
     page-break-after: avoid; }
hr { border: none; border-top: 1px solid #000; margin: 14px 0; }
p { margin: 6px 0; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
li p { margin: 0; }
strong { font-weight: 700; }
em { font-style: italic; }
code { font-family: 'Courier New', monospace; font-size: 11pt; }
table { width: 100%; border-collapse: collapse; margin: 10px 0 14px; font-size: 10.5pt;
        page-break-inside: avoid; }
th, td { border: 1px solid #000; padding: 5px 6px; text-align: left; vertical-align: top; }
th { font-weight: 700; }
"""


def build():
    body = markdown.markdown(
        SRC.read_text(), extensions=["tables", "sane_lists"]
    )

    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{TITLE}</title><style>{CSS}</style></head><body>
{body}
</body></html>"""

    html_path = HERE / f"{OUT}.html"
    pdf_path = HERE / f"{OUT}.pdf"
    html_path.write_text(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(path=str(pdf_path), format="Letter",
                 margin={"top": "0.85in", "bottom": "0.85in",
                         "left": "1in", "right": "1in"},
                 print_background=True)
        browser.close()

    print(f"built {pdf_path.name}")


if __name__ == "__main__":
    build()
