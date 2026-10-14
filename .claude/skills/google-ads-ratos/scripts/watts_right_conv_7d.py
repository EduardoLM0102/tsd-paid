import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
q = """
SELECT segments.conversion_action_name, segments.conversion_action_category,
       metrics.conversions, metrics.all_conversions
FROM customer
WHERE segments.date DURING LAST_7_DAYS
  AND metrics.conversions > 0
"""
rows = list(run_query(CID, q))
if not rows:
    print("No conversions found for LAST_7_DAYS")
else:
    for r in rows:
        print(json.dumps(r, indent=2))
