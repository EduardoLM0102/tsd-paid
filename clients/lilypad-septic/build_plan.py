#!/usr/bin/env python3
"""
Builds the Lilypad Septic media plan: markdown -> styled HTML -> PDF.

The .md is the source of truth. HTML and PDF are artifacts — never edit them by hand.
Styling deliberately matches the Gillespie's Heating and Cooling media plan
(plain black-and-white document look), not the navy/gold TSD report template.

Usage:
    python3 build_plan.py

Requires: `pip install markdown` and Google Chrome (headless, used to print the PDF).
"""
import subprocess
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent
SRC = HERE / "media-plan-q4-2026.md"
OUT = "Lilypad-Septic-Media-Plan_Q4-2026"

CLIENT = "Lilypad Septic Company"
H1 = "LILYPAD SEPTIC COMPANY"
H2 = "Quarterly Media Plan: October &ndash; December 2026"
META = [
    "Salina &amp; Hutchinson, KS &nbsp;&middot;&nbsp; lilypadseptic.com &nbsp;&middot;&nbsp; (785) 268-8523",
]
FACTS = [
    ("Budget:", "Ratio-based. Scenarios modeled at $2,000 / $3,000 / $5,000 per month"),
    ("Platforms:", "Google LSA (Sewage system) &nbsp;&middot;&nbsp; Google Ads (Search / PPC) &nbsp;&middot;&nbsp; Meta Ads (Facebook &amp; Instagram)"),
    ("Market:", "Salina orbit + Hutchinson orbit, central Kansas (two separate service areas)"),
    ("Tagline:", "<em>&ldquo;Service that is Un-frog-gettable!&rdquo;</em>"),
]

CSS = """
@page { size: Letter; margin: 16mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #000; font-size: 10pt;
       line-height: 1.45; margin: 0; padding-bottom: 6mm; }
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

# Chrome's CLI cannot render a repeating per-page footer (position:fixed prints once,
# landing mid-document and overlapping the text). So the footer is stamped onto every
# page with PyMuPDF after Chrome is done.
FOOT_L = f"{CLIENT}  ·  Media Plan"


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
<p class="meta" style="border:0;margin-top:22px;padding:0;font-style:italic">
Prepared for {CLIENT} &nbsp;&middot;&nbsp; October&ndash;December 2026</p>
</body></html>"""

    html_path = HERE / f"{OUT}.html"
    pdf_path = HERE / f"{OUT}.pdf"
    html_path.write_text(html)

    subprocess.run(
        ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
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
        y = h - 40  # baseline, sits inside the 16mm bottom margin
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
