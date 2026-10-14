"""HVAC search-term sweep (read-only): Search HVAC 23848895678, last 30 days. Buckets + competitor-looking names + top terms."""
import sys, os, re
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import run_query
CID, CAMP = "1051843378", "23848895678"; S, U = "2026-09-08", "2026-10-07"
f = lambda x: float(x or 0)
terms = defaultdict(lambda: {"clk": 0.0, "cost": 0.0, "conv": 0.0, "kw": set(), "mt": set()})
for r in run_query(CID, f"""SELECT search_term_view.search_term, segments.keyword.info.text, segments.search_term_match_type, metrics.clicks, metrics.cost_micros, metrics.all_conversions
FROM search_term_view WHERE campaign.id = {CAMP} AND segments.date BETWEEN '{S}' AND '{U}'"""):
    d = terms[r["search_term_view"]["search_term"]]; m = r["metrics"]
    d["clk"] += f(m.get("clicks")); d["cost"] += f(m.get("cost_micros")) / 1e6; d["conv"] += f(m.get("all_conversions"))
    d["kw"].add(r.get("segments", {}).get("keyword", {}).get("info", {}).get("text", "?")); d["mt"].add(str(r.get("segments", {}).get("search_term_match_type", "")))
tot = sum(d["cost"] for d in terms.values())
print(f"{len(terms)} distinct terms, ${tot:,.0f} visible spend; terms with spend: {sum(1 for d in terms.values() if d['cost'] > 0)}")
B = {
 "off-service": r"\b(plumb\w*|drain|sewer|water heater|electric\w*|roof\w*|solar|appliance|refrigerator|fridge|washer|dryer|dishwasher|oven|stove|garage door|pool|handyman|pest|car|auto|vehicle|truck)\b",
 "support / account lookups": r"\b(phone number|customer service|login|warranty claim|contact number|hours|reviews?|complaints?)\b",
 "diy / parts / info": r"\b(how|diy|what|why|capacitor|freon|refrigerant|r410a|r22|filter|thermostat|parts?|manual|reset|symptoms|cost to|youtube)\b",
 "jobs / training": r"\b(job|jobs|hiring|career|salary|apprentic\w*|school|course|training|certification|technician jobs)\b",
 "other cities": r"\b(houston|austin|dallas|fort worth|el paso|corpus|laredo|mcallen|killeen|waco|lubbock|midland|odessa|beaumont)\b",
 "own brand": r"\b(proud pops|pops|problem solvers)\b",
 "commercial": r"\b(commercial|industrial|business|office|warehouse|restaurant)\b",
 "car ac": r"\b(car|auto|automotive|vehicle)\b",
}
for name, pat in B.items():
    hit = {t: d for t, d in terms.items() if re.search(pat, t)}
    c = sum(d["cost"] for d in hit.values())
    print(f"\n== {name}: {len(hit)} terms, {sum(d['clk'] for d in hit.values()):.0f} clk, ${c:,.0f}")
    for t, d in sorted(hit.items(), key=lambda x: -x[1]["cost"])[:10]:
        print(f"     ${d['cost']:7,.2f} clk {d['clk']:3.0f} conv {d['conv']:4.1f}  {t}   <- {sorted(d['kw'])[:2]}")
GEN = set("""ac a/c air conditioner conditioning conditioners hvac heating cooling heat pump furnace repair repairs service services servicing company
companies contractor contractors near me san antonio tx texas local best top rated cheap affordable emergency 24 hour 7 same day residential home
house install installation installer replacement replace new unit units maintenance tune up tuneup check inspection duct ducts cleaning system
systems central mini split ductless technician tech techs and for the a in my of to on 24/7 cost price prices estimate quote free boerne new braunfels
helotes schertz converse universal city live oak cibolo selma stone oak alamo heights leon valley window not working blowing warm hot cold air
fix fixing broken out leaking leak noise smell frozen coil compressor condenser fan motor blower outside inside heater heaters gas electric
specialist specialists experts expert professional professionals pros reliable fast quick emergency open now today tonight weekend sunday saturday""".split())
print("\n== competitor-looking terms (words outside a generic HVAC vocabulary), cost > $15")
for t, d in sorted(terms.items(), key=lambda x: -x[1]["cost"]):
    odd = [w for w in re.findall(r"[a-z0-9'&/]+", t) if w not in GEN and not w.isdigit()]
    if odd and d["cost"] > 15:
        print(f"     ${d['cost']:7,.2f} clk {d['clk']:3.0f} conv {d['conv']:4.1f}  {t}   <- odd: {odd}")
print("\n== top 40 terms by cost")
for t, d in sorted(terms.items(), key=lambda x: -x[1]["cost"])[:40]:
    print(f"     ${d['cost']:7,.2f} clk {d['clk']:3.0f} conv {d['conv']:4.1f}  {t}   <- {sorted(d['kw'])[:1]} {sorted(d['mt'])[:1]}")
