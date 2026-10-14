import json
from collections import defaultdict
def f(x):
    try: return float(x)
    except: return 0.0
rows=json.load(open("daily_all.json"))
D=defaultdict(lambda: defaultdict(lambda:[0,0,0,0]))
for r in rows:
    day=r["segments"]["date"]
    if "2026-06-20"<=day<="2026-07-12":
        m=r["metrics"]; x=D[day][r["campaign"]["name"]]
        x[0]+=f(m.get("cost_micros"))/1e6; x[1]+=f(m.get("clicks")); x[2]+=f(m.get("impressions")); x[3]+=f(m.get("conversions"))
for day in sorted(D):
    tot=sum(v[0] for v in D[day].values())
    print(day, f"TOTAL ${tot:7.2f}", " | ".join(f"{n.replace('TSD_','')[:28]}: ${v[0]:.0f}/{v[1]:.0f}c/{v[2]:.0f}i/{v[3]:.0f}cv" for n,v in D[day].items() if v[0]>0 or v[2]>0))
