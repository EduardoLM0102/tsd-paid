import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
q = """
SELECT campaign.name, campaign.advertising_channel_type,
       segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
  AND metrics.conversions > 0
ORDER BY campaign.name
"""
rows = list(run_query(CID, q))
for r in rows:
    print(json.dumps(r))
