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
brand=re.compile(r"napp", re.I)
# Branded campaign: terms classification by month
for camp in ["TSD_03.22_Search_Branded_Evergreen","TSD_07.21_Search_Nonbranded_AC_Summer"]:
    print("=====", camp)
    for mo in ["2026-04","2026-05","2026-06","2026-07","2026-08","2026-09"]:
        L=[t for t in T if t["camp"]==camp and t["mo"]==mo]
        if not L: continue
        b=[t for t in L if brand.search(t["term"])]; nb=[t for t in L if not brand.search(t["term"])]
        def s(X): return (sum(t["cost"] for t in X), sum(t["clk"] for t in X), sum(t["conv"] for t in X), sum(t["imp"] for t in X))
        sb=s(b); sn=s(nb)
        print(f" {mo} brand-terms: ${sb[0]:8.2f} clk={sb[1]:3.0f} conv={sb[2]:4.1f} imp={sb[3]:4.0f} | non-brand terms: ${sn[0]:8.2f} clk={sn[1]:3.0f} conv={sn[2]:4.1f} imp={sn[3]:4.0f}")
print()
print("Branded campaign Aug-Sep: top terms")
agg=defaultdict(lambda:[0,0,0,0])
for t in T:
    if t["camp"]=="TSD_03.22_Search_Branded_Evergreen" and t["mo"]>="2026-08":
        a=agg[t["term"]]; a[0]+=t["cost"]; a[1]+=t["clk"]; a[2]+=t["conv"]; a[3]+=t["imp"]
for k,v in sorted(agg.items(), key=lambda x:-x[1][0])[:25]:
    print(f"  ${v[0]:8.2f} clk={v[1]:3.0f} cpc={v[0]/v[1] if v[1] else 0:6.2f} conv={v[2]:3.1f} imp={v[3]:4.0f} {k}")
print("\nBranded campaign Apr-Jul: top terms")
agg=defaultdict(lambda:[0,0,0,0])
for t in T:
    if t["camp"]=="TSD_03.22_Search_Branded_Evergreen" and "2026-04"<=t["mo"]<="2026-07":
        a=agg[t["term"]]; a[0]+=t["cost"]; a[1]+=t["clk"]; a[2]+=t["conv"]; a[3]+=t["imp"]
for k,v in sorted(agg.items(), key=lambda x:-x[1][0])[:15]:
    print(f"  ${v[0]:8.2f} clk={v[1]:3.0f} cpc={v[0]/v[1] if v[1] else 0:6.2f} conv={v[2]:3.1f} imp={v[3]:4.0f} {k}")
# Clicks expensive
print("\nSearch-term rows where cost/click >= $50 (2026-04+):")
tot=0; n=0
for t in T:
    if t["mo"]>="2026-04" and t["clk"]>0 and t["cost"]/t["clk"]>=50:
        tot+=t["cost"]; n+=t["clk"]
print(" clicks", n, "cost", round(tot,2))
