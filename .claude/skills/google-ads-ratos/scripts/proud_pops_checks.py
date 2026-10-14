import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "1051843378"

print("=" * 100)
print("CONVERSION ACTIONS — primary_for_goal / status / category")
print("=" * 100)
q1 = """
SELECT conversion_action.name, conversion_action.status, conversion_action.type,
       conversion_action.category, conversion_action.primary_for_goal,
       conversion_action.include_in_conversions_metric
FROM conversion_action
WHERE conversion_action.status = 'ENABLED'
"""
for r in run_query(CID, q1):
    ca = r.get("conversion_action", {})
    print(f"  {ca.get('name','')[:45]:45s} | primary_for_goal={ca.get('primaryForGoal', ca.get('primary_for_goal'))!s:6s} | "
          f"include_in_conv={ca.get('includeInConversionsMetric', ca.get('include_in_conversions_metric'))!s:6s} | "
          f"type={ca.get('type')} | category={ca.get('category')}")

print()
print("=" * 100)
print("IMPRESSION SHARE — last 7 days, live non-branded + branded campaigns")
print("=" * 100)
q2 = """
SELECT campaign.name, campaign.id, campaign.status,
       metrics.search_impression_share, metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share, metrics.cost_micros, metrics.conversions
FROM campaign
WHERE segments.date DURING LAST_7_DAYS
AND campaign.status = 'ENABLED'
"""
for r in run_query(CID, q2):
    c = r.get("campaign", {})
    m = r.get("metrics", {})
    isb = m.get("searchImpressionShare") or m.get("search_impression_share")
    ibl = m.get("searchBudgetLostImpressionShare") or m.get("search_budget_lost_impression_share")
    irl = m.get("searchRankLostImpressionShare") or m.get("search_rank_lost_impression_share")
    cost = (m.get("costMicros") or m.get("cost_micros") or 0)
    conv = m.get("conversions") or 0
    if isb is None and ibl is None and irl is None:
        continue
    print(f"  {c.get('name','')[:45]:45s} | IS={float(isb or 0)*100:5.1f}% | lost_budget={float(ibl or 0)*100:5.1f}% | "
          f"lost_rank={float(irl or 0)*100:5.1f}% | cost=${float(cost):.2f} | conv={conv}")
