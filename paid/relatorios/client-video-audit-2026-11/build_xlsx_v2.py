import sys, re, html
from html.parser import HTMLParser
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

src, out = sys.argv[1], sys.argv[2]
doc = open(src, encoding="utf-8").read()
tbody = doc.split("<tbody>")[1].split("</tbody>")[0]


class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.rows = []; s.cur = None; s.cell = None; s.mode = None

    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "tr":
            s.cur = {"group": "group" in (a.get("class") or ""), "cells": []}
        elif t == "td":
            s.cell = {"pill": "", "main": "", "small": ""}; s.mode = "main"
        elif t == "span" and "pill" in (a.get("class") or ""):
            s.mode = "pill"
        elif t == "small":
            s.mode = "small"

    def handle_endtag(s, t):
        if t in ("span", "small") and s.cell is not None:
            s.mode = "main"
        elif t == "td":
            s.cur["cells"].append(s.cell); s.cell = None
        elif t == "tr":
            s.rows.append(s.cur); s.cur = None

    def handle_data(s, d):
        if s.cell is not None:
            s.cell[s.mode] += d


p = P(); p.feed(tbody)
clean = lambda x: " ".join(html.unescape(x or "").split())

GREEN_BG, GREEN_FG = "D9F2E3", "1D7A4A"
RED_BG, RED_FG = "F9D6D3", "B3261E"
NAVY = "1F3A5F"
thin = Side(style="thin", color="D5DAE1"); border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")

wb = Workbook(); ws = wb.active; ws.title = "Clients"
ws["A1"] = "Who is running video, who isn't, and why"; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
ws["A2"] = "Paid Ads, Nov 18, 2026. Running = the client's own video is live in ads on Meta or YouTube (Meta: last 14 days to Nov 18; Google: Nov 4-17)."
ws["A2"].font = Font(italic=True, size=9, color="5B6678")
ws["A3"] = "Colors: green = running, red = not running"
ws["A3"].font = Font(size=9, color="5B6678")

hdr = ["Client", "Video ads", "Video files we have", "Why / what's going on"]
r = 5
for i, h in enumerate(hdr, 1):
    c = ws.cell(r, i, h); c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY); c.alignment = wrap; c.border = border

group = None
for row in p.rows:
    if row["group"]:
        group = clean(row["cells"][0]["main"]); continue
    cl = row["cells"]; r += 1
    running = group == "Running video"
    files = clean(cl[3]["main"] + (" (" + cl[3]["small"] + ")" if cl[3]["small"] else ""))
    vals = [clean(cl[0]["main"]), "Running" if running else "Not running", files, clean(cl[4]["main"])]
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.alignment = wrap; c.border = border
    ws.cell(r, 1).font = Font(bold=True)
    ws.cell(r, 2).fill = PatternFill("solid", fgColor=GREEN_BG if running else RED_BG)
    ws.cell(r, 2).font = Font(bold=True, color=GREEN_FG if running else RED_FG)
for i, w in enumerate([24, 14, 42, 85], 1):
    ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "B6"
ws.auto_filter.ref = f"A5:D{r}"

s = wb.create_sheet("Summary")
sec = lambda a, b: doc.split(a)[1].split(b)[0]
items = lambda chunk: [clean(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<li>(.*?)</li>", chunk, re.S)]


def block(title, lines, start):
    s.cell(start, 1, title).font = Font(bold=True, size=12, color=NAVY); start += 1
    for l in lines:
        s.cell(start, 1, l).alignment = Alignment(wrap_text=True, vertical="top"); start += 1
    return start + 1


bottom = items(sec('<section class="bottom">', '</section>'))
stats = [clean(re.sub(r"<[^>]+>", " ", x)) for x in re.findall(r'<div class="stat">(.*?)</div>', doc, re.S)]
lists = sec("<h2>The two lists</h2>", "</section>")
l1 = items(lists.split("<h3")[1]); l2 = items(lists.split("<h3")[2])
why = sec("Why it keeps happening, and the fix</h2>", "</section>")
whyp = clean(re.sub(r"<[^>]+>", "", re.search(r"<p>(.*?)</p>", why, re.S).group(1)))
foot = [clean(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r"<div>(.*?)</div>", doc.split('<div class="foot">')[1])]
s["A1"] = "Summary"; s["A1"].font = Font(bold=True, size=14, color=NAVY)
n = block("Bottom line", bottom, 3)
n = block("Numbers", stats, n)
n = block("No usable video (set up video or shut ads off)", l1, n)
n = block("Video exists but isn't running", l2, n)
n = block("Why it keeps happening, and the fix", [whyp] + items(why), n)
block("Sources and gaps", foot, n)
s.column_dimensions["A"].width = 130
wb.move_sheet("Summary", offset=-1)
wb.save(out)
print("client rows", r - 5)
