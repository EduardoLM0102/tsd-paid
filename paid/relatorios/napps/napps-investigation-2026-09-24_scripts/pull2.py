from h import *
q = """
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, campaign.bidding_strategy_type, segments.month,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date BETWEEN '2024-01-01' AND '2026-09-23'
"""
rows = list(run_query(CID, q))
json.dump(rows, open(OUT+"camp_monthly.json","w"), default=str)
# list campaigns
camps = {}
for r in rows:
    c=r["campaign"]; camps[c["id"]]=(c["name"], c["status"], c["advertising_channel_type"], c.get("bidding_strategy_type"))
for k,v in sorted(camps.items(), key=lambda x:x[1][0]): print(k, v)
print()
# monthly by campaign (spend/clk/conv) 
from collections import defaultdict
d=defaultdict(lambda: defaultdict(lambda:[0,0,0,0,0]))
for r in rows:
    c=r["campaign"]; m=r["metrics"]; mo=r["segments"]["month"][:7]
    x=d[c["name"]][mo]
    x[0]+=f(m.get("cost_micros"))/1e6; x[1]+=f(m.get("clicks")); x[2]+=f(m.get("impressions")); x[3]+=f(m.get("conversions")); x[4]+=f(m.get("all_conversions"))
months=sorted({mo for n in d for mo in d[n]})
for n in sorted(d):
    tot=sum(v[0] for v in d[n].values())
    print(f"\n{n}  total spend ${tot:,.0f}")
    for mo in months:
        if mo in d[n]:
            v=d[n][mo]
            if v[0]>0 or v[1]>0 or v[2]>0:
                print(f"   {mo} spend={v[0]:8.2f} clk={v[1]:7.0f} imp={v[2]:8.0f} conv={v[3]:7.1f} allconv={v[4]:7.1f}")
