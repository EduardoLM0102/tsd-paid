# READ-ONLY. ./tsd.sh <abs path>. Did Max Clicks (10-31..) do any good? Per campaign and bidding period, real leads = Calls from ads + forms (all_conversions), taps shown apart.
import sys; sys.path.insert(0, ".")
from lib import run_query
CID="9865206319"; M=lambda x:int(x or 0)/1e6; F=lambda x:float(x or 0)
P = {"HVAC": [("MaxConv  10-13..10-30", "2026-10-13", "2026-10-30"), ("MaxClk$8 10-31..11-16", "2026-10-31", "2026-11-16"), ("MaxConv  11-17..11-18", "2026-11-17", "2026-11-18")],
     "Electrical": [("MaxConv  10-13..10-30", "2026-10-13", "2026-10-30"), ("MaxClk$9 10-31..11-06", "2026-10-31", "2026-11-06"), ("MaxConv  11-07..11-18", "2026-11-07", "2026-11-18")]}
REAL = ("Calls from ads", "[TSD] Contact Form", "[TSD] Book Now Form")
for camp, periods in P.items():
    print(f"== TSD_Search_{camp}")
    for lab, a, b in periods:
        days = (int(b[-2:]) - int(a[-2:]) + 1) if a[5:7] == b[5:7] else None
        w = f"segments.date BETWEEN '{a}' AND '{b}' AND campaign.name = 'TSD_Search_{camp}'"
        r = run_query(CID, f"SELECT metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.search_impression_share, metrics.search_top_impression_share FROM campaign WHERE {w}")[0]["metrics"]
        conv = {}
        for x in run_query(CID, f"SELECT segments.conversion_action_name, metrics.all_conversions FROM campaign WHERE {w} AND metrics.all_conversions > 0"):
            conv[x["segments"]["conversion_action_name"]] = conv.get(x["segments"]["conversion_action_name"], 0) + F(x["metrics"]["all_conversions"])
        s = M(r.get("cost_micros")); c = int(r.get("clicks", 0)); real = sum(v for k, v in conv.items() if k in REAL); taps = conv.get("Click to call", 0)
        nd = {"2026-10-13":18,"2026-10-31":17 if camp=="HVAC" else 7,"2026-11-17":2,"2026-11-07":12}[a]
        print(f"  {lab}  {nd:>2}d  ${s:8.2f} (${s/nd:5.1f}/d)  clk {c:>4} ({c/nd:4.1f}/d)  CPC ${s/c if c else 0:5.2f}  IS {F(r.get('search_impression_share'))*100:3.0f} top {F(r.get('search_top_impression_share'))*100:3.0f}  REAL {real:4.1f} (calls {conv.get('Calls from ads',0):.0f}, forms {conv.get('[TSD] Contact Form',0)+conv.get('[TSD] Book Now Form',0):.1f})  ${s/real if real else 0:6.0f}/real  taps {taps:.0f}  CVR {real/c*100 if c else 0:4.1f}%")
