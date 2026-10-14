import json
from collections import defaultdict
def f(x):
    try: return float(x)
    except: return 0.0
rows=json.load(open("daily_all.json"))
D=defaultdict(list)
for r in rows:
    m=r["metrics"]; D[r["campaign"]["name"]].append((r["segments"]["date"], f(m.get("cost_micros"))/1e6, f(m.get("clicks")), f(m.get("impressions")), f(m.get("conversions")), f(m.get("all_conversions"))))
def period(lo,hi):
    out=[]
    for n,L in D.items():
        S=[x for x in L if lo<=x[0]<=hi]
        c=sum(x[1] for x in S)
        if c>0:
            sp=[x for x in S if x[1]>0]
            out.append((n,c,sum(x[2] for x in S),sum(x[3] for x in S),sum(x[4] for x in S),sum(x[5] for x in S),min(x[0] for x in sp),max(x[0] for x in sp),len(sp)))
    return sorted(out,key=lambda x:x[6])
for lo,hi,label in [("2025-03-24","2025-09-23","LY same window (2025-03-24..2025-09-23)"),("2025-09-24","2026-03-23","prior 6 mo (2025-09-24..2026-03-23)"),("2026-03-24","2026-09-23","LAST 6 MO (2026-03-24..2026-09-23)")]:
    P=period(lo,hi)
    print("\n###",label)
    print(f"{'campaign':46s} {'spend':>9s} {'clk':>6s} {'imp':>7s} {'conv':>6s} {'all':>6s}  first_spend  last_spend  days")
    for n,c,k,i,cv,al,a,b,d in P:
        print(f"{n:46s} {c:9.2f} {k:6.0f} {i:7.0f} {cv:6.1f} {al:6.1f}  {a}  {b}  {d}")
    print(f"{'TOTAL':46s} {sum(x[1] for x in P):9.2f} {sum(x[2] for x in P):6.0f} {sum(x[3] for x in P):7.0f} {sum(x[4] for x in P):6.1f} {sum(x[5] for x in P):6.1f}")
