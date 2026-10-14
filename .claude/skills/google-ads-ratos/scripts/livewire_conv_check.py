import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "1056617442"

print("=== conversion_action (all defined actions in account) ===")
q1 = """
SELECT conversion_action.id, conversion_action.name, conversion_action.type,
       conversion_action.category, conversion_action.status,
       conversion_action.counting_type, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric,
       conversion_action.origin
FROM conversion_action
ORDER BY conversion_action.name
"""
for r in run_query(CID, q1):
    print(json.dumps(r, indent=2, ensure_ascii=False))

print()
print("=== campaign_conversion_goal (biddable = what actually counts per campaign) ===")
q2 = """
SELECT campaign.id, campaign.name,
       campaign_conversion_goal.category, campaign_conversion_goal.origin,
       campaign_conversion_goal.biddable
FROM campaign_conversion_goal
WHERE campaign.status = ENABLED
"""
for r in run_query(CID, q2):
    print(json.dumps(r, indent=2, ensure_ascii=False))

print()
print("=== last 30d volume by conversion action ===")
q3 = """
SELECT segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date DURING LAST_30_DAYS
  AND metrics.all_conversions > 0
"""
for r in run_query(CID, q3):
    print(json.dumps(r, indent=2, ensure_ascii=False))
