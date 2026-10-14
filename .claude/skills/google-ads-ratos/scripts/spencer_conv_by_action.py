import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "2524618054"

print("=" * 100)
print("CONVERSIONS BY ACTION NAME, LAST 30 DAYS (account-level, all campaigns)")
print("=" * 100)
q = """
SELECT segments.conversion_action_name, metrics.all_conversions, metrics.conversions
FROM customer
WHERE segments.date DURING LAST_30_DAYS
"""
rows = list(run_query(CID, q))
agg = {}
for r in rows:
    name = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not name:
        continue
    a = agg.setdefault(name, {"conversions": 0.0, "all_conversions": 0.0})
    a["conversions"] += m.get("conversions", 0.0) or 0.0
    a["all_conversions"] += m.get("all_conversions", 0.0) or 0.0

for name, v in sorted(agg.items(), key=lambda x: -x[1]["all_conversions"]):
    print(f"  {name:45s}  conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")

print("\n" + "=" * 100)
print("CONVERSIONS BY ACTION NAME + CAMPAIGN, LAST 30 DAYS")
print("=" * 100)
q2 = """
SELECT campaign.name, segments.conversion_action_name, metrics.all_conversions
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
"""
rows2 = list(run_query(CID, q2))
agg2 = {}
for r in rows2:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not aname:
        continue
    key = (cname, aname)
    agg2[key] = agg2.get(key, 0.0) + (m.get("all_conversions", 0.0) or 0.0)

for (cname, aname), v in sorted(agg2.items(), key=lambda x: (x[0][0], -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  all_conversions={v:.2f}")
