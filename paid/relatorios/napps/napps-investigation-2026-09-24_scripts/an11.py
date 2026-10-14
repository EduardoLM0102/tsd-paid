import json
from collections import defaultdict
def f(x):
    try: return float(x)
    except: return 0.0
rows=json.load(open("daily_all.json"))
P={}
for r in rows:
    if r["campaign"]["name"]=="TSD_02.20_PMAX_Plumbing_CoreServices":
        m=r["metrics"]; P[r["segments"]["date"]]=(f(m.get("cost_micros"))/1e6,f(m.get("clicks")),f(m.get("impressions")),f(m.get("conversions")))
import datetime
d0=datetime.date(2026,2,20)
# weekly aggregation
wk=defaultdict(lambda:[0,0,0,0])
for day,v in P.items():
    dt=datetime.date.fromisoformat(day); w=dt-datetime.timedelta(days=dt.weekday())
    for i in range(4): wk[w][i]+=v[i]
print("PMax Plumbing weekly (week starting Monday): spend clicks imps conv")
for w in sorted(wk):
    v=wk[w]; print(w, f"${v[0]:8.2f} clk={v[1]:7.0f} imp={v[2]:8.0f} conv={v[3]:6.1f}  cpc={v[0]/v[1] if v[1] else 0:5.2f}")
print("\nLast 25 spend days:")
for day in sorted(P)[-25:]: print(day, P[day])
