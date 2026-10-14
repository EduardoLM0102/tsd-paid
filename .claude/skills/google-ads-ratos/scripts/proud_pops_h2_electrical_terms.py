"""Checklist H2 (read-only): Search Electrical 23866999121 search terms, last 30 days.
Match source split (AI Max vs keywords) + all terms by cost, flagged by intent bucket."""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, CAMP = "1051843378", "23866999121"
S, U = "2026-09-08", "2026-10-07"
f = lambda x: float(x or 0)
q = f"""SELECT search_term_view.search_term, search_term_view.status, segments.search_term_match_source, segments.search_term_match_type,
metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S}' AND '{U}'"""
try:
    rows = run_query(CID, q); has_src = True
except SystemExit:
    rows = run_query(CID, q.replace("segments.search_term_match_source, ", "")); has_src = False
terms = defaultdict(lambda: {"impr": 0.0, "clk": 0.0, "cost": 0.0, "conv": 0.0, "src": set(), "mt": set(), "status": ""})
src_tot = defaultdict(lambda: [0.0, 0.0])
for r in rows:
    t = r["search_term_view"]["search_term"]; m = r["metrics"]; sg = r.get("segments", {})
    d = terms[t]; d["impr"] += f(m.get("impressions")); d["clk"] += f(m.get("clicks")); d["cost"] += f(m.get("cost_micros")) / 1e6
    d["conv"] += f(m.get("all_conversions")); d["status"] = str(r["search_term_view"].get("status", ""))
    src = str(sg.get("search_term_match_source", "n/a")); d["src"].add(src); d["mt"].add(str(sg.get("search_term_match_type", "")))
    src_tot[src][0] += f(m.get("clicks")); src_tot[src][1] += f(m.get("cost_micros")) / 1e6
total = sum(d["cost"] for d in terms.values())
print(f"{len(terms)} distinct terms, ${total:,.0f} visible search-term spend (campaign spend in window ~ $18.5k)")
print("MATCH SOURCE:", {k: f"{v[0]:.0f} clk / ${v[1]:,.0f} ({v[1] / total * 100:.0f}%)" for k, v in src_tot.items()} if has_src else "not available")
B = {
 "off-service (hvac/plumb/roof/solar/etc)": r"\b(hvac|a/?c|air ?condition\w*|furnace|heat(er|ing)?|plumb\w*|drain|sewer|water heater|roof\w*|solar|pool|appliance|garage door|handyman|security|camera|alarm|internet|cable|tv mount\w*)\b",
 "diy / info / how-to": r"\b(how|diy|what|why|code|codes|diagram|wiring diagram|youtube|reddit|forum|definition|meaning|vs)\b",
 "parts / retail / supply": r"\b(home depot|lowes|lowe's|amazon|supply|supplies|store|parts|wholesale|menards|harbor freight)\b",
 "jobs / training": r"\b(job|jobs|hiring|career|salary|apprentic\w*|school|course|class|training|license|licensing|exam|certification)\b",
 "other cities (outside SA area)": r"\b(houston|austin|dallas|fort worth|el paso|corpus|laredo|mcallen|killeen|waco|lubbock|midland|odessa|beaumont|amarillo)\b",
 "own brand (belongs in Branded)": r"\b(proud pops|proudpops|problem solvers|pops)\b",
 "commercial / industrial": r"\b(commercial|industrial|warehouse|office building|business)\b",
}
print()
for name, pat in B.items():
    hit = {t: d for t, d in terms.items() if re.search(pat, t)}
    c = sum(d["cost"] for d in hit.values())
    print(f"== {name}: {len(hit)} terms, {sum(d['clk'] for d in hit.values()):.0f} clicks, ${c:,.0f}")
    for t, d in sorted(hit.items(), key=lambda x: -x[1]["cost"])[:12]:
        print(f"     ${d['cost']:7,.2f} clk {d['clk']:3.0f} allconv {d['conv']:4.1f}  {t}  [{'/'.join(sorted(d['src']))[:30]}]")
print("\n== TOP 60 TERMS BY COST (all)")
for t, d in sorted(terms.items(), key=lambda x: -x[1]["cost"])[:60]:
    print(f"   ${d['cost']:7,.2f} clk {d['clk']:3.0f} allconv {d['conv']:4.1f}  {t}  [{'/'.join(sorted(d['src']))[:28]}|{d['status']}]")
print("\n== competitor-looking terms (contain 'electric'/'electrical' + a word not in a generic list)")
GEN = set("electric electrical electrician electricians near me san antonio tx texas service services repair repairs company companies contractor contractors local best top rated cheap affordable emergency 24 hour 7 residential home house licensed in my area the a for of and to install installation installer panel upgrade outlet outlets wiring rewire light lights lighting fixture fixtures ceiling fan fans breaker box circuit ev charger generator cost price estimate quote boerne new braunfels helotes seguin schertz converse universal city live oak cibolo stone oak alamo heights".split())
for t, d in sorted(terms.items(), key=lambda x: -x[1]["cost"]):
    w = re.findall(r"[a-z0-9']+", t)
    if re.search(r"electric", t) and [x for x in w if x not in GEN and not x.isdigit()] and d["cost"] > 15:
        print(f"   ${d['cost']:7,.2f} clk {d['clk']:3.0f}  {t}   <- odd words: {[x for x in w if x not in GEN and not x.isdigit()]}")
