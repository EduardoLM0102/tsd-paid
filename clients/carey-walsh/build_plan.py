#!/usr/bin/env python3
"""
Builds the Carey & Walsh media plan: markdown -> styled HTML -> PDF.

The .md is the source of truth. HTML and PDF are artifacts — never edit them by hand.
Styling matches the Lilypad / Cool Hand media plans (Gillespie's precedent: plain
black-and-white document look), not the navy/gold TSD report template.

Usage:
    python3 build_plan.py

Requires: `pip install markdown pymupdf playwright` (+ `playwright install chromium`).
Google Chrome is not installed on this Mac, so the PDF prints through Playwright's Chromium.
"""
import pathlib
import markdown
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
SRC = HERE / "media-plan-nov-2026-jan-2027.md"
OUT = "Carey-Walsh-Media-Plan_Nov-2026-Jan-2027"

CLIENT = "Carey &amp; Walsh Inc."
FOOT_CLIENT = "Carey & Walsh Inc."
H1 = "CAREY &amp; WALSH INC."
H2 = "Paid Media Plan: November 2026 &ndash; January 2027"
META = [
    "Briarcliff Manor, NY &nbsp;&middot;&nbsp; careyandwalsh.com &nbsp;&middot;&nbsp; 914-762-9600",
]
FACTS = [
    ("Budget:", "Ratio-based. Scenarios modeled at $4,000 / $6,000 / $9,000 per month"),
    ("Platforms:", "Google LSA (HVAC) &nbsp;&middot;&nbsp; Google Ads (Search / PPC) &nbsp;&middot;&nbsp; Meta Ads (Facebook &amp; Instagram, awareness only)"),
    ("Market:", "All of Westchester County, NY"),
    ("Tagline:", "<em>&ldquo;Built In-House. Built to Last.&rdquo;</em>"),
]

CSS = """
@page { size: Letter; margin: 16mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000; font-size: 10pt;
       line-height: 1.42; margin: 0; }
h1.title { font-size: 19pt; margin: 0 0 3px; letter-spacing: -.01em; }
h2.sub { font-size: 12pt; margin: 0 0 12px; font-weight: 700; }
.meta { font-size: 8.5pt; color: #666; padding-bottom: 9px; border-bottom: 1px solid #bbb; margin-bottom: 10px; }
.facts { font-size: 9.5pt; margin-bottom: 20px; }
.facts div { margin: 2px 0; }
.facts b { display: inline-block; min-width: 68px; }
h2 { font-size: 13pt; margin: 20px 0 7px; padding-bottom: 4px; border-bottom: 1px solid #999;
     page-break-after: avoid; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 13px 0 4px; page-break-after: avoid; break-after: avoid; }
p { margin: 6px 0; }
ul { margin: 6px 0; padding-left: 17px; }
li { margin: 4px 0; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 9px 0 13px; font-size: 8.5pt;
        page-break-inside: avoid; break-inside: avoid; }
th { background: #ededed; text-align: left; padding: 6px 7px; font-weight: 700;
     border: 1px solid #bbb; }
td { padding: 6px 7px; border: 1px solid #ccc; vertical-align: top; }
"""

# A position:fixed footer prints once, mid-document, so the running footer and page
# numbers are stamped onto every page with PyMuPDF after the PDF is printed.
FOOT_L = f"{FOOT_CLIENT}  ·  Media Plan"


def build():
    body = markdown.markdown(SRC.read_text(), extensions=["tables", "sane_lists"])

    facts = "\n".join(f"<div><b>{k}</b> {v}</div>" for k, v in FACTS)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{CLIENT} &mdash; Media Plan</title><style>{CSS}</style></head><body>
<h1 class="title">{H1}</h1>
<h2 class="sub">{H2}</h2>
<div class="meta">{"<br>".join(META)}</div>
<div class="facts">{facts}</div>
{body}
<p class="meta" style="border:0;margin-top:14px;padding:0;font-style:italic">
Prepared for {CLIENT} &nbsp;&middot;&nbsp; November 2026&ndash;January 2027</p>
</body></html>"""

    html_path = HERE / f"{OUT}.html"
    pdf_path = HERE / f"{OUT}.pdf"
    html_path.write_text(html)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri())
        page.pdf(path=str(pdf_path), prefer_css_page_size=True, print_background=True)
        browser.close()

    stamp_footers(pdf_path)
    print(f"built {pdf_path.name}")


def stamp_footers(pdf_path):
    """Draw the running footer + page number on every page."""
    import fitz

    doc = fitz.open(pdf_path)
    gray = (0.47, 0.47, 0.47)
    for i, page in enumerate(doc, start=1):
        w, h = page.rect.width, page.rect.height
        y = h - 40  # baseline, sits inside the 20mm bottom margin
        page.draw_line(fitz.Point(46, y - 10), fitz.Point(w - 46, y - 10),
                       color=(0.8, 0.8, 0.8), width=0.5)
        page.insert_text(fitz.Point(46, y), FOOT_L, fontname="helv",
                         fontsize=8, color=gray)
        label = f"Page {i}"
        page.insert_text(fitz.Point(w - 46 - fitz.get_text_length(label, "helv", 8), y),
                         label, fontname="helv", fontsize=8, color=gray)
    doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
    doc.close()


if __name__ == "__main__":
    build()
