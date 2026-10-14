#!/usr/bin/env python3
"""
Builds the Watt's Right ad spend review: markdown -> styled HTML -> PDF.

The .md is the source of truth. HTML and PDF are artifacts — never edit them by hand.
Styling matches the Cool Hand Electric media plan precedent (plain black-and-white
document look), not the navy/gold TSD report template.

Usage:
    python3 build_report.py

Requires: `pip install markdown pymupdf` and Google Chrome (headless, used to print the PDF).
"""
import subprocess
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent
SRC = HERE / "ad-spend-review-sep-2026.md"
OUT = "Watts-Right-Ad-Spend-Review_Sep-2026"

CLIENT = "Watt's Right Electric"
H1 = "WATT'S RIGHT ELECTRIC"
H2 = "PPC Spend Review &amp; Increase Recommendation"
META = [
    "Tulsa, OK &nbsp;&middot;&nbsp; callwattsright.com",
]
FACTS = [
    ("Period:", "Trailing 30 days (August 10 to September 8, 2026)"),
    ("Channels:", "Google Search &amp; Performance Max (PPC only, Local Services Ads excluded)"),
    ("Prepared by:", "TopServ Digital"),
]

CSS = """
@page { size: Letter; margin: 16mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000; font-size: 10pt;
       line-height: 1.32; margin: 0; }
h1.title { font-size: 19pt; margin: 0 0 3px; letter-spacing: -.01em; }
h2.sub { font-size: 12pt; margin: 0 0 12px; font-weight: 700; }
.meta { font-size: 8.5pt; color: #666; padding-bottom: 9px; border-bottom: 1px solid #bbb; margin-bottom: 10px; }
.facts { font-size: 9.5pt; margin-bottom: 14px; }
.facts div { margin: 2px 0; }
.facts b { display: inline-block; min-width: 78px; }
h2 { font-size: 13pt; margin: 14px 0 6px; padding-bottom: 4px; border-bottom: 1px solid #999;
     page-break-after: avoid; break-after: avoid; }
h3 { font-size: 10.5pt; margin: 13px 0 4px; page-break-after: avoid; break-after: avoid; }
p { margin: 6px 0; }
ul { margin: 5px 0; padding-left: 17px; }
li { margin: 4px 0; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 8px 0 10px; font-size: 8.5pt;
        page-break-inside: avoid; break-inside: avoid; }
th { background: #ededed; text-align: left; padding: 6px 7px; font-weight: 700;
     border: 1px solid #bbb; }
td { padding: 6px 7px; border: 1px solid #ccc; vertical-align: top; }
"""

FOOT_L = f"{CLIENT}  ·  Ad Spend Review"


def build():
    body = markdown.markdown(SRC.read_text(), extensions=["tables", "sane_lists"])

    facts = "\n".join(f"<div><b>{k}</b> {v}</div>" for k, v in FACTS)
    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{CLIENT} PPC Spend Review</title><style>{CSS}</style></head><body>
<h1 class="title">{H1}</h1>
<h2 class="sub">{H2}</h2>
<div class="meta">{"<br>".join(META)}</div>
<div class="facts">{facts}</div>
{body}
<p class="meta" style="border:0;margin-top:10px;padding:0;font-style:italic;page-break-before:avoid;break-before:avoid">Prepared for {CLIENT} &nbsp;&middot;&nbsp; September 2026</p>
</body></html>"""

    html_path = HERE / f"{OUT}.html"
    pdf_path = HERE / f"{OUT}.pdf"
    html_path.write_text(html)

    subprocess.run(
        ["/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
         "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", str(html_path)],
        check=True, capture_output=True,
    )
    stamp_footers(pdf_path)
    print(f"built {pdf_path.name}")


def stamp_footers(pdf_path):
    """Draw the running footer + page number on every page."""
    import fitz

    doc = fitz.open(pdf_path)
    gray = (0.47, 0.47, 0.47)
    for i, page in enumerate(doc, start=1):
        w, h = page.rect.width, page.rect.height
        y = h - 40
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
