import json, re
from collections import defaultdict
rows=json.load(open("search_terms.json"))
def f(x):
    try: return float(x)
    except: return 0.0
T=[]
for r in rows:
    s=r["search_term_view"]; m=r["metrics"]
    T.append(dict(term=s["search_term"], camp=r["campaign"]["name"], ag=r["ad_group"]["name"], mo=r["segments"]["month"][:7],
      cost=f(m.get("cost_micros"))/1e6, clk=f(m.get("clicks")), imp=f(m.get("impressions")), conv=f(m.get("conversions"))))
print("rows", len(T))
# window last 6 months: 2026-03-24..; month granularity: use 2026-04..2026-09 
W=[t for t in T if t["mo"]>="2026-04"]
print("window rows", len(W), "cost", round(sum(t['cost'] for t in W)), "clk", sum(t['clk'] for t in W), "conv", sum(t['conv'] for t in W))
# Aggregate by term
agg=defaultdict(lambda: dict(cost=0,clk=0,imp=0,conv=0))
for t in W:
    a=agg[t["term"]]; a["cost"]+=t["cost"]; a["clk"]+=t["clk"]; a["imp"]+=t["imp"]; a["conv"]+=t["conv"]
print("distinct terms", len(agg))
print("\nTop 40 terms by cost (Apr-Sep 2026):")
for k,v in sorted(agg.items(), key=lambda x:-x[1]["cost"])[:40]:
    print(f"  {v['cost']:8.2f} clk={v['clk']:4.0f} conv={v['conv']:4.1f} imp={v['imp']:5.0f}  {k}")
# Cost by campaign in window w/ terms with 0 conv
zero=sum(v["cost"] for v in agg.values() if v["conv"]==0)
print("\nspend on terms with 0 conv:", round(zero), "of", round(sum(v['cost'] for v in agg.values())))
