import json, datetime
from collections import defaultdict
def f(x):
    try: return float(x)
    except: return 0.0
calls=[(r["call_view"]["start_call_date_time"], int(r["call_view"].get("call_duration_seconds") or 0), r["call_view"]["call_status"], r["campaign"]["name"], r["ad_group"]["name"]) for r in json.load(open("call_view.json"))]
print("=== 2026 calls by campaign & ad group with duration list (Apr-Sep) ===")
by=defaultdict(list)
for t,d,s,c,a in calls:
    if t>="2026-04-01": by[(c,a)].append((t[:10],d,s))
for k in sorted(by, key=lambda k:-len(by[k])):
    L=by[k]; ds=sorted(x[1] for x in L)
    print(f"{k[0][:44]:44s} | {k[1][:28]:28s} n={len(L):3d} <30s={sum(1 for x in ds if x<30):2d} 30-59={sum(1 for x in ds if 30<=x<60):2d} 60+={sum(1 for x in ds if x>=60):2d} median={ds[len(ds)//2]}s")
# HVAC vs plumbing by campaign/ad group name in 2026
def cat(c,a):
    s=(c+" "+a).lower()
    if "brand" in s: return "BRANDED"
    if any(w in s for w in ["hvac","ac ","air","cool","aircon"]): return "HVAC"
    if any(w in s for w in ["plumb","drain","leak","sewer"]): return "PLUMB"
    return "OTHER"
print("\n=== calls by category per month (2026) ===")
cm=defaultdict(lambda: defaultdict(int))
for t,d,s,c,a in calls:
    if t>="2026-04-01": cm[t[:7]][cat(c,a)]+=1
for mo in sorted(cm): print(mo, dict(cm[mo]))
print("\nAll 2026-04+ ad groups seen:", sorted({(c,a,cat(c,a)) for t,d,s,c,a in calls if t>='2026-04-01'}))
