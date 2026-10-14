from h import *
from collections import defaultdict
q = """
SELECT segments.month, segments.conversion_action_name, segments.conversion_action_category, metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date BETWEEN '2024-04-01' AND '2026-09-23'
"""
rows = list(run_query(CID, q))
json.dump(rows, open(OUT+"conv_by_action_monthly.json","w"), default=str)
d=defaultdict(lambda: defaultdict(lambda:[0,0]))
cat={}
for r in rows:
    s=r["segments"]; m=r["metrics"]
    n=s.get("conversion_action_name"); mo=s["month"][:7]
    cat[n]=s.get("conversion_action_category")
    d[n][mo][0]+=f(m.get("conversions")); d[n][mo][1]+=f(m.get("all_conversions"))
months=sorted({mo for n in d for mo in d[n]})
print("action | category | (conv/allconv) per month")
for n in sorted(d, key=lambda n:-sum(v[1] for v in d[n].values())):
    print(f"\n{n} [{cat[n]}]")
    print("   "+"  ".join(f"{mo[2:]}:{d[n][mo][0]:.0f}/{d[n][mo][1]:.0f}" for mo in months if mo in d[n] and (d[n][mo][0] or d[n][mo][1])))
