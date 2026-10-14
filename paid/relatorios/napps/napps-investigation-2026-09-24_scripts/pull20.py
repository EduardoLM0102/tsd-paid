from h import *
from collections import defaultdict
L="9239407401"
try:
    for r in run_query(L, "SELECT customer.descriptive_name, customer.status, customer.time_zone FROM customer"): print(json.dumps(r,default=str))
except Exception as e:
    print("ERR customer", str(e)[:300])
q="""SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type, segments.month,
 metrics.cost_micros, metrics.impressions, metrics.clicks, metrics.conversions, metrics.all_conversions
FROM campaign WHERE segments.date BETWEEN '2025-01-01' AND '2026-09-23'"""
try:
    rows=list(run_query(L,q))
    d=defaultdict(lambda:[0,0,0,0])
    for r in rows:
        mo=r["segments"]["month"][:7]; m=r["metrics"]
        x=d[(r["campaign"]["name"],r["campaign"]["status"],r["campaign"]["advertising_channel_type"],mo)]
        x[0]+=f(m.get("cost_micros"))/1e6; x[1]+=f(m.get("impressions")); x[2]+=f(m.get("clicks")); x[3]+=f(m.get("all_conversions"))
    for k in sorted(d, key=lambda k:(k[0],k[3])):
        v=d[k]
        if v[0]>0 or v[1]>0: print(k, [round(a,1) for a in v])
except Exception as e:
    print("ERR campaign", str(e)[:600])
