from h import *
q="""SELECT campaign.name, ad_group.name, ad_group.status, metrics.cost_micros, metrics.clicks, metrics.conversions, metrics.impressions
FROM ad_group WHERE campaign.status='ENABLED' AND segments.date BETWEEN '2026-07-21' AND '2026-09-23'"""
from collections import defaultdict
d=defaultdict(lambda:[0,0,0,0])
st={}
for r in run_query(CID,q):
    k=(r["campaign"]["name"], r["ad_group"]["name"]); st[k]=r["ad_group"]["status"]
    m=r["metrics"]; d[k][0]+=f(m.get("cost_micros"))/1e6; d[k][1]+=f(m.get("clicks")); d[k][2]+=f(m.get("conversions")); d[k][3]+=f(m.get("impressions"))
for k,v in sorted(d.items()): print(k, st[k], f"${v[0]:.0f} clk={v[1]:.0f} conv={v[2]:.0f} imp={v[3]:.0f}")
