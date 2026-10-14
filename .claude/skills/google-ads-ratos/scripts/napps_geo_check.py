import sys
sys.path.insert(0, ".")
from lib import run_query

q = """
SELECT campaign.id, campaign_criterion.type, campaign_criterion.criterion_id
FROM campaign_criterion
WHERE campaign.id = 24049055193 AND campaign_criterion.type IN ('LOCATION','PROXIMITY','LOCATION_GROUP')
"""
rows = list(run_query("9509605037", q))
print(f"{len(rows)} geo criteria found")
for r in rows[:10]:
    print(r)
