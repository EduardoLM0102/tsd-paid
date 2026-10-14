import sys
sys.path.insert(0, ".")
from lib import run_query

CID = "2198608170"
CAMPAIGN_ID = "23805382277"

print("=" * 100)
print("CAMPAIGN — bidding strategy + budget")
print("=" * 100)
q0 = f"""
SELECT campaign.id, campaign.name, campaign.bidding_strategy_type,
       campaign.target_cpa.target_cpa_micros,
       campaign.maximize_conversions.target_cpa_micros,
       campaign_budget.amount_micros, campaign_budget.delivery_method
FROM campaign
WHERE campaign.id = {CAMPAIGN_ID}
"""
for r in run_query(CID, q0):
    print(r)

print("\n" + "=" * 100)
print("AD GROUP — effective target/cpc bids")
print("=" * 100)
q1 = f"""
SELECT ad_group.id, ad_group.name, ad_group.status,
       ad_group.effective_target_cpa_micros,
       ad_group.effective_cpc_bid_micros
FROM ad_group
WHERE campaign.id = {CAMPAIGN_ID} AND ad_group.status = 'ENABLED'
"""
for r in run_query(CID, q1):
    print(r)

print("\n" + "=" * 100)
print("AD STRENGTH — RSA quality per ad group")
print("=" * 100)
q2 = f"""
SELECT ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
       ad_group_ad.ad_strength,
       ad_group_ad.ad.responsive_search_ad.headlines,
       ad_group_ad.ad.responsive_search_ad.descriptions
FROM ad_group_ad
WHERE campaign.id = {CAMPAIGN_ID} AND ad_group_ad.status = 'ENABLED'
"""
for r in run_query(CID, q2):
    ad = r.get("ad_group_ad", {})
    print(f"\n  Ad group: {r.get('ad_group', {}).get('name')}  |  ad_strength: {ad.get('ad_strength')}  |  ad id {ad.get('ad', {}).get('id')}")

print("\n" + "=" * 100)
print("KEYWORD — bid vs first-page / top-of-page CPC estimates + QS (top keywords by cost, ENABLED, current)")
print("=" * 100)
q3 = f"""
SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
       ad_group_criterion.effective_cpc_bid_micros,
       ad_group_criterion.position_estimates.first_page_cpc_micros,
       ad_group_criterion.position_estimates.top_of_page_cpc_micros,
       ad_group_criterion.position_estimates.first_position_cpc_micros,
       ad_group_criterion.quality_info.quality_score,
       ad_group.name,
       metrics.impressions, metrics.clicks, metrics.cost_micros
FROM keyword_view
WHERE campaign.id = {CAMPAIGN_ID} AND ad_group_criterion.status = 'ENABLED'
ORDER BY metrics.cost_micros DESC
LIMIT 15
"""
for r in run_query(CID, q3):
    crit = r.get("ad_group_criterion", {})
    kw = crit.get("keyword", {})
    pos = crit.get("position_estimates", {})
    m = r.get("metrics", {})
    print(f"\n  '{kw.get('text')}' ({kw.get('match_type')})  [{r.get('ad_group',{}).get('name')}]")
    print(f"    impressions: {m.get('impressions')}  clicks: {m.get('clicks')}  cost: ${float(m.get('cost_micros',0))/1e6:.2f}")
    print(f"    effective_cpc_bid: ${float(crit.get('effective_cpc_bid_micros',0) or 0)/1e6:.2f}")
    print(f"    first_page_cpc_est: ${float(pos.get('first_page_cpc_micros',0) or 0)/1e6:.2f}  top_of_page_cpc_est: ${float(pos.get('top_of_page_cpc_micros',0) or 0)/1e6:.2f}  first_position_cpc_est: ${float(pos.get('first_position_cpc_micros',0) or 0)/1e6:.2f}")
    print(f"    quality_score: {crit.get('quality_info',{}).get('quality_score')}")

print("\n" + "=" * 100)
print("IMPRESSION SHARE detail (7d) — budget lost / rank lost / search abs top / top IS")
print("=" * 100)
q4 = f"""
SELECT campaign.name,
       metrics.search_impression_share,
       metrics.search_budget_lost_impression_share,
       metrics.search_rank_lost_impression_share,
       metrics.search_top_impression_share,
       metrics.search_absolute_top_impression_share,
       metrics.search_rank_lost_top_impression_share,
       metrics.search_rank_lost_absolute_top_impression_share
FROM campaign
WHERE campaign.id = {CAMPAIGN_ID} AND segments.date DURING LAST_7_DAYS
"""
for r in run_query(CID, q4):
    print(r)
