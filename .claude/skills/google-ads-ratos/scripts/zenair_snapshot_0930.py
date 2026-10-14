"""Zen Air 2026-09-30: pre-change snapshot (bidding, keyword statuses, negatives) + brand kw IS. Read-only."""
import json
import sys
sys.path.insert(0, ".")
from lib import run_query
CID = "4360840956"
OUT = sys.argv[1] if len(sys.argv) > 1 else None
snap = {}
snap["campaigns"] = run_query(CID, """SELECT campaign.id, campaign.name, campaign.bidding_strategy_type,
  campaign.maximize_conversions.target_cpa_micros, campaign.target_impression_share.location,
  campaign.target_impression_share.location_fraction_micros, campaign.target_impression_share.cpc_bid_ceiling_micros,
  campaign.target_spend.cpc_bid_ceiling_micros, campaign_budget.amount_micros
  FROM campaign WHERE campaign.id IN (23675783172, 24100030790)""")
snap["keywords"] = run_query(CID, """SELECT campaign.id, ad_group.id, ad_group_criterion.criterion_id, ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type, ad_group_criterion.status, ad_group_criterion.negative
  FROM ad_group_criterion WHERE campaign.id IN (23675783172, 24100030790) AND ad_group_criterion.type = 'KEYWORD'
  AND ad_group_criterion.status != 'REMOVED'""")
snap["campaign_negatives"] = run_query(CID, """SELECT campaign.id, campaign_criterion.criterion_id, campaign_criterion.keyword.text,
  campaign_criterion.keyword.match_type FROM campaign_criterion WHERE campaign.id IN (23675783172, 24100030790)
  AND campaign_criterion.type = 'KEYWORD' AND campaign_criterion.negative = TRUE""")
if OUT:
    json.dump(snap, open(OUT, "w"), indent=1)
    print(f"saved {OUT}: {len(snap['campaigns'])} campaigns, {len(snap['keywords'])} keywords, {len(snap['campaign_negatives'])} campaign negatives")
for c in snap["campaigns"]:
    print(c["campaign"])
print("\nbrand exact/phrase keyword IS, last 30d:")
for r in run_query(CID, """SELECT ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type,
  metrics.impressions, metrics.clicks, metrics.average_cpc, metrics.search_impression_share,
  metrics.search_top_impression_share, metrics.search_rank_lost_impression_share
  FROM keyword_view WHERE campaign.id = 23675783172 AND segments.date DURING LAST_30_DAYS AND metrics.impressions > 0"""):
    k, m = r["ad_group_criterion"]["keyword"], r["metrics"]
    if k["match_type"] != "BROAD":
        print(f"  {k['text']:32s} [{k['match_type'][:5]}] imp={m.get('impressions')} clk={m.get('clicks',0)} "
              f"cpc=${int(m.get('average_cpc',0) or 0)/1e6:.2f} IS={m.get('search_impression_share')} "
              f"topIS={m.get('search_top_impression_share')} rankLost={m.get('search_rank_lost_impression_share')}")
