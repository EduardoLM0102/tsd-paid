import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "9509605037"
q = """
SELECT campaign.name, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_30_DAYS
"""
for r in run_query(CID, q):
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    print(c.get("name"), "IS=", m.get("search_impression_share"), "budget_lost=", m.get("search_budget_lost_impression_share"), "rank_lost=", m.get("search_rank_lost_impression_share"))
