import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"

q = """
SELECT segments.conversion_action_name, segments.conversion_action_category, metrics.conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS AND metrics.conversions > 0
"""
rows = list(run_query(CID, q))
agg = {}
for r in rows:
    seg = r.get("segments", {})
    aname = seg.get("conversion_action_name") or seg.get("conversionActionName")
    acat = seg.get("conversion_action_category") or seg.get("conversionActionCategory")
    m = r.get("metrics", {})
    conv = m.get("conversions") or 0.0
    key = (aname, acat)
    agg[key] = agg.get(key, 0.0) + conv

total = sum(agg.values())
print(f"Total conversions (sum of actions): {total:.4f}")
print()
for (aname, acat), v in sorted(agg.items(), key=lambda x: -x[1]):
    print(f"  {aname:40s} | category={acat:25s} conversions={v:.4f}  ({v/total*100:.1f}%)")
