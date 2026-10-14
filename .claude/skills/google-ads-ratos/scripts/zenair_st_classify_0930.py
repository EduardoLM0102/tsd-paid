"""Zen Air: classify search terms (clean window 08-27..09-29) into own-brand / generic service / other (competitor, supply, DIY)."""
import re
import sys
from collections import defaultdict
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"
S, E = "2026-08-27", "2026-09-29"
BR = "23675783172"

GENERIC = set("""
hvac ac a c a/c air conditioning conditioner conditioners heating cooling heat and repair repairs service services servicing near me
company companies contractor contractors furnace furnaces pump pumps installation install installer installers replacement replace
unit units system systems cost costs price prices pricing estimate estimates free quote quotes local emergency 24 7 24/7 hour hours best top
duct ducts cleaning maintenance tune up tuneup technician technicians tech the in for of my to near by fix fixing new central home house
residential commercial affordable cheap same day open now around nearby area mini split splits ductless thermostat not working blowing
cold warm hot leaking leak check inspection inspections plan plans diagnostic diagnostics appointment schedule book specialist specialists
expert experts professional pros pro man guy guys heater heaters conditioners compressor coil coils refrigerant freon recharge evaporator
condenser blower motor vent vents ventilation quality indoor iq georgia ga atlanta duluth lawrenceville suwanee cumming buford alpharetta
johns creek norcross snellville gainesville roswell milton sugar hill dacula lilburn tucker chamblee doraville peachtree corners
berkeley lake flowery branch oakwood sandy springs brookhaven marietta dunwoody forsyth gwinnett county loganville braselton hoschton
decatur stone mountain grayson jefferson winder hvacs heatpump airconditioner airconditioning contracting mechanical services? what how
much does is do you an companys co inc llc
""".split())


def cls(t):
    t2 = t.lower()
    if "zen" in t2 or "callzenair" in t2:
        return "own_brand"
    toks = re.findall(r"[a-z0-9/']+", t2)
    if toks and all(x in GENERIC for x in toks):
        return "generic_service"
    return "other"


if __name__ == "__main__":
    q = f"""
    SELECT campaign.id, search_term_view.search_term, metrics.cost_micros, metrics.clicks, metrics.conversions
    FROM search_term_view
    WHERE campaign.id IN (23675783172, 24100030790) AND segments.date BETWEEN '{S}' AND '{E}'
    """
    agg = defaultdict(lambda: defaultdict(float))
    terms = defaultdict(lambda: defaultdict(float))
    for r in run_query(CID, q):
        m = r.get("metrics", {})
        camp = "BR" if r["campaign"]["id"] == BR else "NB"
        t = r["search_term_view"]["search_term"]
        c = cls(t)
        for k, v in (("cost", int(m.get("cost_micros", 0)) / 1e6), ("clk", int(m.get("clicks", 0))), ("conv", float(m.get("conversions", 0)))):
            agg[(camp, c)][k] += v
            terms[(camp, c, t)][k] += v

    for k, v in sorted(agg.items()):
        print(f"{k[0]} {k[1]:16s} cost=${v['cost']:8.2f} clk={v['clk']:4.0f} conv={v['conv']:4.1f} cpc={v['cost']/max(v['clk'],1):6.2f}")

    print("\nTop 60 'other' terms by cost (to eyeball competitor vs genuinely generic):")
    oth = [(k, v) for k, v in terms.items() if k[1] == "other" and v["clk"] > 0]
    for k, v in sorted(oth, key=lambda x: -x[1]["cost"])[:60]:
        print(f"  {k[0]} {k[2][:55]:55s} ${v['cost']:7.2f} clk={v['clk']:.0f} conv={v['conv']:.0f}")
    print("\nTop 40 'generic_service' terms by cost:")
    gen = [(k, v) for k, v in terms.items() if k[1] == "generic_service" and v["clk"] > 0]
    for k, v in sorted(gen, key=lambda x: -x[1]["cost"])[:40]:
        print(f"  {k[0]} {k[2][:55]:55s} ${v['cost']:7.2f} clk={v['clk']:.0f} conv={v['conv']:.0f}")
    print(f"\nterms with clicks: other={len(oth)} generic={len(gen)}")
