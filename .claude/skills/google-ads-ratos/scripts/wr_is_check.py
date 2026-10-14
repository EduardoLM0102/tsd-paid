import sys, json
sys.path.insert(0, ".")
from lib import run_query

CID = "3651667805"
for rng in ["LAST_7_DAYS", "LAST_30_DAYS"]:
    print(f"=== {rng} ===")
    q = f"""
    SELECT campaign.name, campaign.advertising_channel_type, campaign_budget.amount_micros,
           metrics.search_impression_share, metrics.search_budget_lost_impression_share,
           metrics.search_rank_lost_impression_share, metrics.cost_micros, metrics.conversions
    FROM campaign
    WHERE segments.date DURING {rng}
      AND campaign.status = 'ENABLED'
      AND campaign.advertising_channel_type IN ('SEARCH','PERFORMANCE_MAX')
    """
    for r in run_query(CID, q):
        print(json.dumps(r))
