import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "7410489772"
q = """
SELECT campaign.id, campaign.name,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share
FROM campaign
WHERE campaign.id = 24155674204 AND segments.date DURING LAST_7_DAYS
"""
for r in run_query(CID, q):
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    print(f"{c.get('name')}: IS={m.get('searchImpressionShare', m.get('search_impression_share'))} | lost_to_budget={m.get('searchBudgetLostImpressionShare', m.get('search_budget_lost_impression_share'))} | lost_to_rank={m.get('searchRankLostImpressionShare', m.get('search_rank_lost_impression_share'))}")
