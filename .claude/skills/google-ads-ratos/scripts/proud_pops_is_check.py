import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"
q = """
SELECT campaign.name, metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING THIS_MONTH AND campaign.advertising_channel_type = 'SEARCH' AND campaign.status = 'ENABLED'
"""
for r in run_query(CID, q):
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    print(c.get("name"),
          "IS=%.1f%%" % (100*(m.get("search_impression_share") or 0)),
          "budget_lost=%.1f%%" % (100*(m.get("search_budget_lost_impression_share") or 0)),
          "rank_lost=%.1f%%" % (100*(m.get("search_rank_lost_impression_share") or 0)))
