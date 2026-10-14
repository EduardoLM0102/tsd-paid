import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "9865206319"
SINCE = "2026-08-10"
UNTIL = "2026-08-25"

print("=" * 100)
print(f"COOL HAND ELECTRIC — CONVERSIONS BY ACTION + CAMPAIGN, {SINCE} to {UNTIL}")
print("=" * 100)
q = f"""
SELECT campaign.name, campaign.id, segments.conversion_action_name, metrics.conversions, metrics.all_conversions
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
rows = list(run_query(CID, q))
agg = {}
agg_all = {}
for r in rows:
    cname = r.get("campaign", {}).get("name")
    aname = r.get("segments", {}).get("conversion_action_name")
    m = r.get("metrics", {})
    if not aname:
        continue
    key = (cname, aname)
    agg[key] = agg.get(key, 0.0) + (m.get("conversions") or 0.0)
    agg_all[key] = agg_all.get(key, 0.0) + (m.get("allConversions") or m.get("all_conversions") or 0.0)

print("Using metrics.conversions (primary, matches report totals):")

q_cost = f"""
SELECT campaign.name, metrics.cost_micros
FROM campaign
WHERE segments.date BETWEEN '{SINCE}' AND '{UNTIL}'
"""
cost_rows = list(run_query(CID, q_cost))
cost_by_campaign = {}
for r in cost_rows:
    cname = r.get("campaign", {}).get("name")
    m = r.get("metrics", {})
    cost = (m.get("costMicros") or m.get("cost_micros") or 0)
    cost_by_campaign[cname] = cost_by_campaign.get(cname, 0) + int(cost or 0)

for (cname, aname), v in sorted(agg.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:30s} | {aname:35s}  conversions={v:.2f}")

print("\nUsing metrics.all_conversions (includes secondary/local actions, for comparison):")
for (cname, aname), v in sorted(agg_all.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:30s} | {aname:35s}  all_conversions={v:.2f}")

print()
print("Cost by campaign (sanity check against report):")
for cname, c in sorted(cost_by_campaign.items()):
    print(f"  {cname:30s}  cost=${c/1_000_000:.2f}")
