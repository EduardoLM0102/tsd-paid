import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "8634274092"

print("=" * 100)
print("LIVE CAMPAIGNS + bidding strategy + whether they use account-default conversion goals")
print("=" * 100)
q0 = """
SELECT campaign.id, campaign.name, campaign.status,
       campaign.advertising_channel_type,
       campaign.bidding_strategy_type,
       campaign.selective_optimization.conversion_actions
FROM campaign
WHERE campaign.status = 'ENABLED'
"""
for r in run_query(CID, q0):
    c = r.get("campaign", {})
    print(f"\n  {c.get('name')}  (id {c.get('id')})")
    print(f"    channel : {c.get('advertising_channel_type')}")
    print(f"    bidding : {c.get('bidding_strategy_type')}")
    so = c.get("selective_optimization") or {}
    print(f"    selective_optimization: {so.get('conversion_actions')}")

print("\n" + "=" * 100)
print("CAMPAIGN CONVERSION GOALS (per-campaign overrides of what counts for bidding)")
print("=" * 100)
q1 = """
SELECT campaign.id, campaign.name,
       campaign_conversion_goal.category,
       campaign_conversion_goal.origin,
       campaign_conversion_goal.biddable
FROM campaign_conversion_goal
WHERE campaign.status = 'ENABLED'
"""
try:
    rows = run_query(CID, q1)
    cur = None
    for r in rows:
        c = r.get("campaign", {})
        g = r.get("campaign_conversion_goal", {})
        if not g.get("biddable"):
            continue
        if c.get("name") != cur:
            cur = c.get("name")
            print(f"\n  CAMPAIGN: {cur}")
        print(f"    BIDDABLE -> category={g.get('category'):<20} origin={g.get('origin')}")
except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 100)
print("ACCOUNT-LEVEL CONVERSION GOALS (customer_conversion_goal) — biddable only")
print("=" * 100)
q2 = """
SELECT customer_conversion_goal.category,
       customer_conversion_goal.origin,
       customer_conversion_goal.biddable
FROM customer_conversion_goal
"""
try:
    for r in run_query(CID, q2):
        g = r.get("customer_conversion_goal", {})
        if g.get("biddable"):
            print(f"  BIDDABLE -> category={str(g.get('category')):<22} origin={g.get('origin')}")
except Exception as e:
    print(f"  ERROR: {e}")
