import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
q = """
SELECT campaign.name, campaign.bidding_strategy_type, campaign.maximize_conversions.target_cpa_micros,
       campaign.target_cpa.target_cpa_micros, campaign.status
FROM campaign
WHERE campaign.status = 'ENABLED'
"""
for r in run_query(CID, q):
    print(json.dumps(r))

print("=== conversion goals (customer level) ===")
q2 = """
SELECT customer_conversion_goal.category, customer_conversion_goal.origin, customer_conversion_goal.biddable
FROM customer_conversion_goal
"""
for r in run_query(CID, q2):
    print(json.dumps(r))
