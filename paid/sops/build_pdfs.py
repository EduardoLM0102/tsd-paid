#!/usr/bin/env python3
"""
Builds the Paid Ads launch SOPs: markdown -> styled HTML -> PDF.

The .md files are the source of truth. HTML and PDF are artifacts — never edit them by hand.

Usage:
    python3 build_pdfs.py            # rebuild all four SOPs
    python3 build_pdfs.py meta       # rebuild one (meta | google | youtube | tiktok)

Requires: `pip install markdown` and Google Chrome (headless, used to print the PDF).
Outputs the PDF next to the .md AND into ./PDFs/ (the folder we send to Ryan).
"""
import subprocess
import sys
import pathlib
import markdown

HERE = pathlib.Path(__file__).parent
PDF_DIR = HERE / "PDFs"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SOPS = {
    "meta": {
        "md": "meta-ads-launch-buildout.md",
        "out": "Meta-Ads-Launch-Buildout-Process",
        "title": "Meta Ads Launch &amp; Buildout Process",
        "h1": "Meta Ads &mdash; New Campaign Launch &amp; Buildout",
    },
    "google": {
        "md": "google-ads-launch-buildout.md",
        "out": "Google-Ads-Launch-Buildout-Process",
        "title": "Google Ads (PPC) Launch &amp; Buildout Process",
        "h1": "Google Ads (PPC) &mdash; New Campaign Launch &amp; Buildout",
    },
    "youtube": {
        "md": "youtube-ads-launch-buildout.md",
        "out": "YouTube-Ads-Launch-Buildout-Process",
        "title": "YouTube Ads Launch &amp; Buildout Process",
        "h1": "YouTube Ads &mdash; New Campaign Launch &amp; Buildout",
    },
    "tiktok": {
        "md": "tiktok-ads-launch-buildout.md",
        "out": "TikTok-Ads-Launch-Buildout-Process",
        "title": "TikTok Ads Launch &amp; Buildout Process",
        "h1": "TikTok Ads &mdash; New Campaign Launch &amp; Buildout",
    },
}

CSS = """
@page { size: Letter; margin: 18mm 16mm 16mm 16mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; color: #1c2430; font-size: 10.5pt; line-height: 1.5; margin: 0; }
.cover { border-bottom: 3px solid #c8a349; padding-bottom: 14px; margin-bottom: 22px; }
.kicker { font-size: 8.5pt; letter-spacing: .16em; text-transform: uppercase; color: #c8a349; font-weight: 700; }
h1.title { font-size: 22pt; margin: 6px 0 8px; color: #0f2340; letter-spacing: -.01em; }
.sub { font-size: 9.5pt; color: #5b6675; }
h2 { font-size: 12.5pt; color: #0f2340; margin: 24px 0 8px; padding-bottom: 5px; border-bottom: 1px solid #dde2e8; page-break-after: avoid; }
h3 { font-size: 10.5pt; color: #0f2340; margin: 14px 0 6px; page-break-after: avoid; }
p { margin: 7px 0; }
ul, ol { margin: 7px 0 7px 0; padding-left: 18px; }
li { margin: 3px 0; }
strong { color: #0f2340; }
em { color: #5b6675; }
hr { border: 0; border-top: 1px solid #e6e9ee; margin: 22px 0; }
table { width: 100%; border-collapse: collapse; margin: 10px 0 14px; font-size: 9pt; page-break-inside: avoid; }
th { background: #0f2340; color: #fff; text-align: left; padding: 7px 8px; font-weight: 600; }
td { padding: 6px 8px; border-bottom: 1px solid #e6e9ee; vertical-align: top; }
tr:nth-child(even) td { background: #f7f8fa; }
code { background: #f1f3f6; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }
blockquote { border-left: 3px solid #c8a349; margin: 10px 0; padding: 2px 0 2px 12px; color: #47525f; }
h2, h3 { break-after: avoid; }
.note { font-size: 8.5pt; font-style: italic; color: #6b7684; margin: 4px 0 0; }
"""


def build(key):
    cfg = SOPS[key]
    src = HERE / cfg["md"]
    md_text = src.read_text()

    # drop the H1 — the cover renders its own
    body_md = "\n".join(md_text.split("\n")[1:])
    body = markdown.markdown(body_md, extensions=["tables", "sane_lists", "attr_list"])
    body = body.replace("[ ]", "&#9744;")  # checkboxes

    html = f"""<!doctype html><html><head><meta charset="utf-8">
<title>{cfg['title']}</title><style>{CSS}</style></head><body>
<div class="cover">
  <div class="kicker">TopServ Digital &middot; Paid Ads Division</div>
  <h1 class="title">{cfg['h1']}</h1>
  <div class="sub">Owner: Eduardo Marinho, Head of Paid Ads</div>
</div>
{body}
</body></html>"""

    html_path = HERE / f"{cfg['out']}.html"
    pdf_path = HERE / f"{cfg['out']}.pdf"
    html_path.write_text(html)

    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={pdf_path}", str(html_path)],
        check=True, capture_output=True,
    )

    PDF_DIR.mkdir(exist_ok=True)
    (PDF_DIR / pdf_path.name).write_bytes(pdf_path.read_bytes())
    print(f"built {pdf_path.name}")


if __name__ == "__main__":
    targets = sys.argv[1:] or list(SOPS)
    for t in targets:
        if t not in SOPS:
            sys.exit(f"unknown SOP '{t}' — pick from: {', '.join(SOPS)}")
        build(t)
