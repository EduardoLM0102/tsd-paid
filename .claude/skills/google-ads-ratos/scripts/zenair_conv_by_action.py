import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4360840956"

print("=" * 100)
print(f"ZEN AIR — CONVERSIONS BY ACTION, LAST 7 DAYS")
print("=" * 100)
q = """
SELECT segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS AND metrics.conversions > 0
"""
rows = list(run_query(CID, q))
agg = {}
for r in rows:
    aname = r.get("segments", {}).get("conversionActionName") or r.get("segments", {}).get("conversion_action_name")
    acat = r.get("segments", {}).get("conversionActionCategory") or r.get("segments", {}).get("conversion_action_category")
    m = r.get("metrics", {})
    key = (aname, acat)
    conv = agg.get(key, {"conversions": 0.0, "all_conversions": 0.0})
    conv["conversions"] += (m.get("conversions") or 0.0)
    conv["all_conversions"] += (m.get("allConversions") or m.get("all_conversions") or 0.0)
    agg[key] = conv

total_conv = 0.0
for (aname, acat), v in sorted(agg.items(), key=lambda x: -x[1]["conversions"]):
    print(f"  {aname:40s} | cat={acat:25s} conversions={v['conversions']:.2f}  all_conversions={v['all_conversions']:.2f}")
    total_conv += v["conversions"]

print(f"\nSum of segmented conversions: {total_conv:.2f}")

print("\n" + "=" * 100)
print("ALL CONVERSION ACTIONS CONFIGURED ON ACCOUNT (incl. call-duration thresholds)")
print("=" * 100)
q2 = """
SELECT conversion_action.name, conversion_action.type, conversion_action.category,
       conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric,
       conversion_action.phone_call_duration_seconds
FROM conversion_action
"""
for r in run_query(CID, q2):
    ca = r.get("conversionAction", r.get("conversion_action", {}))
    print(f"  {ca.get('name'):40s} type={ca.get('type'):20s} cat={ca.get('category'):20s} status={ca.get('status'):10s} primary={ca.get('primaryForGoal', ca.get('primary_for_goal'))} includeInConv={ca.get('includeInConversionsMetric', ca.get('include_in_conversions_metric'))} callDur={ca.get('phoneCallDurationSeconds', ca.get('phone_call_duration_seconds'))}")
