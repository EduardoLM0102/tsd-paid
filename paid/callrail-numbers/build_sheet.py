"""trackers_raw.json -> CallRail-Tracking-Numbers-by-Client.xlsx (tab 1 = paste blocks for Agency Titan, tab 2 = every number)."""
import json, os, collections, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "trackers_raw.json")))

# Trackers that are internal, tests or hiring: listed on tab 2, kept out of the Agency Titan block.
SKIP_WORDS = ("internal", "test number", "hiring", "otp", "call back")
CLIENT_NOTES = {
    "All Heart Heating and Cooling": "Offboarded client. Numbers still active in CallRail.",
    "TopServ Digital": "Our own numbers, not a client.",
    "Coolhand Electrics": "Ads now use ServiceTitan numbers, not CallRail (PPC 469-270-1146, LSA 469-300-0557, per Angela 10-12). CallRail Google Ads number below is no longer in the ads.",
    "All Seasons Air": "Tracker named 'Meta Ads Number' is set up in CallRail as a Google call extension source. Confirm which channel it really runs on before AI uses it.",
    "Watt's Right Electric": "Has two 'Tulsa LSA' numbers.",
    "Integrate Comfort Systems": "Has two 'Google Local Services Ads' numbers.",
    "C&S Air": "'Test Number' left out of the block.",
}


def fmt(n):
    n = (n or "").removeprefix("+1")
    return f"({n[:3]}) {n[3:6]}-{n[6:]}" if len(n) == 10 else n


rows, clients = [], {}
for x in data:
    acct = x["account"]["name"].strip()
    if "error" in x:
        clients[acct] = {"acct": acct, "main": "", "block": "NOT PULLED YET (CallRail rate limit). Retry later.", "note": "", "count": 0}
        continue
    by_co = collections.defaultdict(list)
    for t in x["trackers"]:
        if t["status"] == "active":
            by_co[t["company"]["name"].strip()].append(t)
    for co, ts in by_co.items():
        main = collections.Counter(t["destination_number"] for t in ts).most_common(1)[0][0]
        lines, count = [f"Main business line: {fmt(main)}"], 0
        singles = [t for t in ts if t["type"] == "source"]
        pools = [t for t in ts if t["type"] == "session"]
        for t in sorted(singles, key=lambda t: t["name"].lower()):
            nums = ", ".join(fmt(n) for n in t["tracking_numbers"])
            skip = any(w in t["name"].lower() for w in SKIP_WORDS)
            rows.append([co, acct, t["name"].strip(), "Single number", nums, fmt(t["destination_number"]),
                         t["source"].get("type") or "", "Left out of AT block" if skip else ""])
            count += len(t["tracking_numbers"])
            if not skip:
                lines.append(f"{t['name'].strip()}: {nums}")
        for t in pools:
            for n in t["tracking_numbers"]:
                rows.append([co, acct, t["name"].strip(), "Website pool (rotating)", fmt(n), fmt(t["destination_number"]),
                             t["source"].get("type") or "", "Do not use in content"])
            count += len(t["tracking_numbers"])
        if pools:
            lines.append("Website: shows a rotating tracking number to each visitor. Do not put website pool numbers in content or creatives.")
        clients[co] = {"acct": acct, "main": fmt(main), "block": "\n".join(lines), "note": CLIENT_NOTES.get(co, ""), "count": count}

wb = Workbook()
hdr_font, hdr_fill = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="1F2A44")
wrap = Alignment(wrap_text=True, vertical="top")

ws = wb.active
ws.title = "For Agency Titan"
ws.append(["Client (as named in CallRail)", "CallRail account", "Main line (calls ring to)", "Paste into Agency Titan profile", "Notes"])
for co in sorted(clients, key=lambda c: c.lower()):
    c = clients[co]
    ws.append([co, c["acct"], c["main"], c["block"], c["note"]])
for col, w in zip("ABCDE", (32, 28, 20, 80, 50)):
    ws.column_dimensions[col].width = w

ws2 = wb.create_sheet("All Numbers")
ws2.append(["Client", "CallRail account", "Tracker name", "Type", "Tracking number", "Rings to", "CallRail source rule", "Note"])
for r in sorted(rows, key=lambda r: (r[0].lower(), r[3], r[2].lower())):
    ws2.append(r)
for col, w in zip("ABCDEFGH", (32, 28, 36, 22, 40, 16, 26, 24)):
    ws2.column_dimensions[col].width = w

for sh in (ws, ws2):
    for cell in sh[1]:
        cell.font, cell.fill = hdr_font, hdr_fill
    for row in sh.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = wrap
    sh.freeze_panes = "A2"

ws3 = wb.create_sheet("Read Me")
for line in [
    f"Pulled from the CallRail API on {datetime.date.today():%Y-%m-%d}. Active tracking numbers only (disabled trackers have no numbers).",
    "Covers every CallRail account TopServ can see: the TopServ Digital Clients agency account plus the client-owned accounts.",
    "Single number = one fixed number for one channel (Google Ads, LSA, GBP, Meta, mailers, etc). These are the ones AI should use, matched to the channel the content is for.",
    "Website pool = rotating numbers swapped on the website per visitor. Never print these in ads, posts or creatives.",
    "Internal, test and hiring numbers are listed in 'All Numbers' but left out of the Agency Titan blocks.",
    "Active in CallRail but no active numbers: Iceberg Mechanical Corp.",
]:
    ws3.append([line])
ws3.column_dimensions["A"].width = 140

out = os.path.join(HERE, "CallRail-Tracking-Numbers-by-Client.xlsx")
wb.save(out)
print(out, len(clients), "clients", len(rows), "number rows")
