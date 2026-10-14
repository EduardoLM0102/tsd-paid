from h import *
from collections import defaultdict
# daily by campaign since 2026-03-01
q = """
SELECT campaign.name, segments.date, metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share,
       metrics.search_top_impression_share, metrics.search_absolute_top_impression_share
FROM campaign
WHERE segments.date BETWEEN '2026-06-15' AND '2026-09-23' AND campaign.status = 'ENABLED'
"""
rows=list(run_query(CID,q))
json.dump(rows, open(OUT+"daily_enabled.json","w"), default=str)
d=defaultdict(dict)
for r in rows:
    d[r["campaign"]["name"]][r["segments"]["date"]]=r
for name in d:
    print("\n==",name)
    for day in sorted(d[name]):
        m=d[name][day]["metrics"]
        c=f(m.get("cost_micros"))/1e6
        if c>0 or f(m.get("impressions"))>0:
            print(f"  {day} ${c:7.2f} clk={f(m.get('clicks')):3.0f} imp={f(m.get('impressions')):4.0f} conv={f(m.get('conversions')):3.1f} IS={m.get('search_impression_share')} lostB={m.get('search_budget_lost_impression_share')} lostR={m.get('search_rank_lost_impression_share')}")
