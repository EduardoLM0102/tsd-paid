import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "2524618054"

print("=" * 100)
print("CONVERSION ACTIONS (category, origin, status, counting)")
print("=" * 100)
q0 = """
SELECT conversion_action.id, conversion_action.name, conversion_action.type,
       conversion_action.category, conversion_action.origin,
       conversion_action.status, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric,
       conversion_action.phone_call_duration_seconds
FROM conversion_action
WHERE conversion_action.status != 'REMOVED'
"""
for r in run_query(CID, q0):
    ca = r.get("conversion_action", {})
    print(f"\n  {ca.get('name')}  (id {ca.get('id')})")
    print(f"    type={ca.get('type')}  category={ca.get('category')}  origin={ca.get('origin')}")
    print(f"    status={ca.get('status')}  primary_for_goal={ca.get('primary_for_goal')}  in_conv_metric={ca.get('include_in_conversions_metric')}")
    if ca.get("phone_call_duration_seconds"):
        print(f"    call_duration_threshold={ca.get('phone_call_duration_seconds')}s")

print("\n" + "=" * 100)
print("ACCOUNT-LEVEL CONVERSION GOALS (biddable = what actually counts for bidding)")
print("=" * 100)
q1 = """
SELECT conversion_goal_campaign_config.campaign,
       conversion_goal_campaign_config.custom_conversion_goal
FROM conversion_goal_campaign_config
"""
try:
    for r in run_query(CID, q1):
        print(r)
except Exception as e:
    print(f"(skipped campaign config: {e})")

print("\n" + "=" * 100)
print("CAMPAIGN CONVERSION GOAL (biddable per category/origin) - ENABLED campaigns only")
print("=" * 100)
q2 = """
SELECT campaign.id, campaign.name,
       campaign_conversion_goal.category, campaign_conversion_goal.origin,
       campaign_conversion_goal.biddable
FROM campaign_conversion_goal
WHERE campaign.status = 'ENABLED'
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    g = r.get("campaign_conversion_goal", {})
    print(f"  {c.get('name')} (id {c.get('id')})  category={g.get('category')}  origin={g.get('origin')}  biddable={g.get('biddable')}")
