import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "4467722415"

q = """
SELECT campaign.name, campaign.bidding_strategy_type, campaign.target_cpa.target_cpa_micros,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share, metrics.cost_micros, metrics.conversions,
       campaign_budget.amount_micros
FROM campaign
WHERE campaign.status = 'ENABLED' AND segments.date DURING LAST_7_DAYS
"""
rows = list(run_query(CID, q))
for r in rows:
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    b = r.get("campaignBudget", r.get("campaign_budget", {}))
    print(f"{c.get('name')}")
    print(f"  bidding_strategy_type = {c.get('biddingStrategyType', c.get('bidding_strategy_type'))}")
    tcpa = c.get('targetCpa', c.get('target_cpa', {}))
    print(f"  target_cpa_micros = {tcpa.get('targetCpaMicros', tcpa.get('target_cpa_micros'))}")
    print(f"  daily_budget = ${int(b.get('amountMicros', b.get('amount_micros', 0)))/1_000_000:.2f}")
    print(f"  search_IS = {m.get('searchImpressionShare', m.get('search_impression_share'))}")
    print(f"  budget_lost_IS = {m.get('searchBudgetLostImpressionShare', m.get('search_budget_lost_impression_share'))}")
    print(f"  rank_lost_IS = {m.get('searchRankLostImpressionShare', m.get('search_rank_lost_impression_share'))}")
    print(f"  cost = ${int(m.get('costMicros', m.get('cost_micros', 0)))/1_000_000:.2f}  conv = {m.get('conversions')}")
    print()
