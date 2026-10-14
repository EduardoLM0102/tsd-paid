import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"

q = """
SELECT campaign.name, segments.conversion_action_name, metrics.conversions, metrics.cost_micros
FROM campaign
WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_7_DAYS
"""
rows = list(run_query(CID, q))

agg = {}
cost_check = {}
for r in rows:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    conv = m.get("conversions") or 0.0
    cost = m.get("costMicros") or m.get("cost_micros") or 0
    if aname:
        key = (cname, aname)
        agg.setdefault(key, {"conv": 0.0, "cost": 0})
        agg[key]["conv"] += conv
        agg[key]["cost"] += int(cost)
    cost_check.setdefault(cname, 0)
    cost_check[cname] += int(cost)

print("Raw segmented cost per campaign (sum across conversion_action_name rows, to check for duplication):")
for cname, c in sorted(cost_check.items()):
    print(f"  {cname:45s} raw_segmented_cost_sum=${c/1_000_000:.2f}")

print()
print("Per (campaign, conversion_action) rows:")
for (cname, aname), v in sorted(agg.items()):
    if v["conv"] > 0:
        print(f"  {cname:45s} | {aname:30s} conv={v['conv']:6.2f} row_cost=${v['cost']/1_000_000:.2f}")
