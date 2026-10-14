import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "5563867754"
SINCE = "2026-08-08"
UNTIL = "2026-09-07"

print("=" * 100)
print(f"C&S AIR — CONVERSIONS BY ACTION + CAMPAIGN, {SINCE} to {UNTIL}")
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
for (cname, aname), v in sorted(agg.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  conversions={v:.2f}")

print("\nUsing metrics.all_conversions (includes secondary/local actions, for comparison):")
for (cname, aname), v in sorted(agg_all.items(), key=lambda x: (x[0][0] or "", -x[1])):
    if v > 0:
        print(f"  {cname:45s} | {aname:35s}  all_conversions={v:.2f}")

# All conversion actions on the account, regardless of whether they fired
print("\n" + "=" * 100)
print("ALL CONVERSION ACTIONS ON ACCOUNT (config, not just fired ones)")
print("=" * 100)
q2 = """
SELECT conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric
FROM conversion_action
"""
for r in run_query(CID, q2):
    ca = r.get("conversionAction") or r.get("conversion_action") or {}
    print(f"  {str(ca.get('name')):40s} type={str(ca.get('type')):25s} status={str(ca.get('status')):10s} "
          f"primary_for_goal={ca.get('primaryForGoal')} include_in_conv={ca.get('includeInConversionsMetric')}")
