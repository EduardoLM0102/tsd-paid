from h import *
from collections import defaultdict
q = """
SELECT campaign.name, campaign.advertising_channel_type, segments.month, segments.ad_network_type,
       metrics.cost_micros, metrics.clicks, metrics.impressions, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '2024-04-01' AND '2026-09-23'
"""
rows = list(run_query(CID, q))
json.dump(rows, open(OUT+"camp_network_monthly.json","w"), default=str)
# account-level by network by month
d=defaultdict(lambda: defaultdict(lambda:[0,0,0,0,0]))
for r in rows:
    mo=r["segments"]["month"][:7]; net=r["segments"]["ad_network_type"]; m=r["metrics"]
    x=d[mo][net]
    x[0]+=f(m.get("cost_micros"))/1e6; x[1]+=f(m.get("clicks")); x[2]+=f(m.get("impressions")); x[3]+=f(m.get("conversions")); x[4]+=f(m.get("all_conversions"))
for mo in sorted(d):
    print(mo)
    for net,v in sorted(d[mo].items(), key=lambda x:-x[1][0]):
        cpc = v[0]/v[1] if v[1] else 0
        print(f"    {net:16s} spend={v[0]:8.2f} clk={v[1]:7.0f} imp={v[2]:8.0f} cpc={cpc:6.2f} conv={v[3]:7.1f} all={v[4]:7.1f}")
