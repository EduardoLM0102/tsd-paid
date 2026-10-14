import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "3797438623"

q = """
SELECT segments.date, segments.conversion_action_name, metrics.all_conversions
FROM customer
WHERE segments.date BETWEEN '2026-08-20' AND '2026-09-14'
  AND segments.conversion_action_name = '[EB] Click to call'
"""
rows = list(run_query(CID, q))
for r in rows:
    d = r.get("segments", {}).get("date")
    v = r.get("metrics", {}).get("all_conversions")
    if v and v > 0:
        print(d, v)
